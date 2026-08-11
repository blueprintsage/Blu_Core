from __future__ import annotations

import copy
import importlib.util
import hashlib
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "validate_continuity_contracts",
    ROOT / "tools/validate_continuity_contracts.py",
)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class ContinuityContractValidationTests(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.original_base_commit = validator.BASE_COMMIT
        golden_manifest = ROOT / "kernel/golden/v0.22.0/SHA256SUMS"
        golden_paths = {
            Path("kernel/golden/v0.22.0/SHA256SUMS"),
            *{
                Path("kernel/golden/v0.22.0") / line.split(None, 1)[1].strip()
                for line in golden_manifest.read_text(encoding="utf-8").splitlines()
                if line.strip()
            },
        }
        for relative in {*validator.REQUIRED, *golden_paths}:
            source = ROOT / relative
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)

    def tearDown(self) -> None:
        validator.BASE_COMMIT = self.original_base_commit
        self.temp.cleanup()

    def git(self, *args: str) -> str:
        result = subprocess.run(
            ["git", "-C", str(self.root), *args],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()

    def init_git_scope_fixture(self) -> None:
        self.git("init")
        self.git("config", "user.email", "bc040-fixture@example.invalid")
        self.git("config", "user.name", "BC-040 Fixture")
        self.git("add", ".")
        paths = [
            path for path in self.git("ls-files").splitlines()
            if path and path != "MANIFEST.sha256"
        ]
        lines = []
        for path in paths:
            blob = subprocess.run(
                ["git", "-C", str(self.root), "show", f":{path}"],
                check=True,
                capture_output=True,
            ).stdout
            lines.append(f"{hashlib.sha256(blob).hexdigest()}  {path}")
        (self.root / "MANIFEST.sha256").write_text(
            "\n".join(lines) + "\n", encoding="utf-8"
        )
        self.git("add", "MANIFEST.sha256")
        self.git("commit", "-m", "fixture baseline")
        validator.BASE_COMMIT = self.git("rev-parse", "HEAD")
        self.assertEqual([], validator._validate_git_scope(self.root))
        self.assertEqual([], validator._validate_manifest_coverage(self.root))

    def load(self, relative: str) -> dict:
        return json.loads((self.root / relative).read_text(encoding="utf-8"))

    def save(self, relative: str, value: dict) -> None:
        (self.root / relative).write_text(
            json.dumps(value, indent=2) + "\n", encoding="utf-8"
        )

    def errors(self) -> list[str]:
        return validator.validate(self.root)

    def assert_has(self, fragment: str) -> None:
        errors = self.errors()
        self.assertTrue(any(fragment in error for error in errors), errors)

    def test_canonical_contracts_pass(self) -> None:
        self.assertEqual([], self.errors())

    def test_missing_required_file_fails(self) -> None:
        (self.root / "continuity/lifecycle.json").unlink()
        self.assert_has("missing required file")

    def test_malformed_json_fails(self) -> None:
        path = self.root / "continuity/rehydration.json"
        path.write_text("{", encoding="utf-8")
        self.assert_has("invalid JSON")

    def test_component_count_must_remain_seven(self) -> None:
        path = "contracts/successor/component_registry.json"
        data = self.load(path)
        data["components"].append(dict(data["components"][0]))
        self.save(path, data)
        self.assert_has("component count is not seven")

    def test_packet_count_must_remain_eight(self) -> None:
        path = "contracts/successor/packet_registry.json"
        data = self.load(path)
        data["packets"].append(dict(data["packets"][0]))
        self.save(path, data)
        self.assert_has("packet count is not eight")

    def test_interface_count_must_remain_nine(self) -> None:
        path = "contracts/successor/interface_registry.json"
        data = self.load(path)
        data["interfaces"].append(dict(data["interfaces"][0]))
        self.save(path, data)
        self.assert_has("interface count is not nine")

    def test_bare_session_cannot_become_a_lifetime(self) -> None:
        path = "contracts/successor/component_registry.json"
        data = self.load(path)
        data["state_lifetime_values"].append("session")
        data["state_lifetime_contract"]["bare_session_allowed"] = True
        self.save(path, data)
        self.assert_has("state lifetime vocabulary changed")
        self.assert_has("bare session is allowed")

    def test_continuity_cannot_invent_a_new_packet(self) -> None:
        path = "contracts/successor/interface_registry.json"
        data = self.load(path)
        interface = next(
            item for item in data["interfaces"]
            if item["interface_id"] == "IF-CONTINUITY-PROVIDER"
        )
        interface["request_packets"] = ["ContinuityPacket"]
        self.save(path, data)
        self.assert_has("invents a new packet")

    def test_record_identity_fields_are_required(self) -> None:
        path = "continuity/schemas/continuity_record.schema.json"
        data = self.load(path)
        data["required"].remove("version_id")
        self.save(path, data)
        self.assert_has("ContinuityRecord required fields are incomplete")

    def test_record_path_cannot_prove_persistence(self) -> None:
        path = "continuity/schemas/continuity_record.schema.json"
        data = self.load(path)
        data["x-blu-invariants"] = ["record_id exists"]
        self.save(path, data)
        self.assert_has("path-proof invariant")

    def test_receipt_status_vocabulary_is_finite(self) -> None:
        path = "continuity/schemas/continuity_receipt.schema.json"
        data = self.load(path)
        data["properties"]["status"]["enum"].append("probably_ok")
        self.save(path, data)
        self.assert_has("ContinuityReceipt status vocabulary is incomplete")

    def test_receipt_binds_requested_action_and_related_records(self) -> None:
        path = "continuity/schemas/continuity_receipt.schema.json"
        data = self.load(path)
        data["required"].remove("requested_action")
        data["x-blu-action-binding-rule"] = "Any action may use the receipt."
        self.save(path, data)
        self.assert_has("action or related-record binding is incomplete")
        self.assert_has("not bound to its requested action")

    def test_durable_success_requires_completed_provider_receipt(self) -> None:
        path = "continuity/schemas/continuity_receipt.schema.json"
        data = self.load(path)
        data["x-blu-durable-success-rule"] = "A requested write is durable."
        self.save(path, data)
        self.assert_has("self-certified")

    def test_failed_write_cannot_change_state(self) -> None:
        path = "continuity/schemas/continuity_receipt.schema.json"
        data = self.load(path)
        data["x-blu-failure-rule"] = "Failure may keep partial state."
        self.save(path, data)
        self.assert_has("failed writes can become durable state")

    def test_model_context_cannot_certify_persistence(self) -> None:
        path = "continuity/evidence_stages.json"
        data = self.load(path)
        data["rules"]["model_boundary"] = "Model confidence is evidence."
        self.save(path, data)
        self.assert_has("model or context can self-certify")

    def test_provider_availability_requires_evidence(self) -> None:
        path = "continuity/schemas/continuity_provider_availability.schema.json"
        data = self.load(path)
        data["x-blu-truth-rule"] = "Configured means available."
        self.save(path, data)
        self.assert_has("configuration alone")

    def test_query_cannot_merge_incompatible_scopes(self) -> None:
        path = "continuity/schemas/continuity_query.schema.json"
        data = self.load(path)
        data["x-blu-scope-rule"] = "Merge all scopes."
        self.save(path, data)
        self.assert_has("incompatible-scope merge")

    def test_query_limit_remains_bounded(self) -> None:
        path = "continuity/schemas/continuity_query.schema.json"
        data = self.load(path)
        data["properties"]["limit"]["maximum"] = 10000
        self.save(path, data)
        self.assert_has("not deterministically bounded")

    def test_lifecycle_requires_all_operations(self) -> None:
        path = "continuity/lifecycle.json"
        data = self.load(path)
        data["transitions"] = data["transitions"][:-1]
        self.save(path, data)
        self.assert_has("transitions are incomplete")

    def test_conflict_cannot_silently_overwrite(self) -> None:
        path = "continuity/lifecycle.json"
        data = self.load(path)
        data["conflict_rule"] = "Use last writer wins."
        self.save(path, data)
        self.assert_has("conflict handling is inconsistent")

    def test_history_and_no_delete_are_required(self) -> None:
        path = "continuity/lifecycle.json"
        data = self.load(path)
        data["history_rule"] = "Delete old versions."
        self.save(path, data)
        self.assert_has("no-deletion rule")

    def test_corruption_cannot_silently_repair(self) -> None:
        path = "continuity/lifecycle.json"
        data = self.load(path)
        data["corruption_rule"] = "Ask the model to repair the record."
        self.save(path, data)
        self.assert_has("silently repair state")

    def test_rehydration_requires_provider_result_before_context(self) -> None:
        path = "continuity/rehydration.json"
        data = self.load(path)
        data["sequence"].remove("receive_provider_result_and_receipt")
        self.save(path, data)
        self.assert_has("rehydration sequence")

    def test_host_session_cannot_become_durable_external(self) -> None:
        path = "continuity/rehydration.json"
        data = self.load(path)
        data["host_session_rule"] = "host_session is durable_external."
        self.save(path, data)
        self.assert_has("are conflated")

    def test_protected_authorization_requires_rollback_resistance(self) -> None:
        path = "continuity/security_evidence.json"
        data = self.load(path)
        data["profiles"]["protected_authorization"]["required_properties"].remove(
            "monotonic_or_rollback_resistant_attempt_state"
        )
        self.save(path, data)
        self.assert_has("protected authorization continuity evidence is incomplete")

    def test_ordinary_receipt_cannot_become_protected_auth_evidence(self) -> None:
        path = "continuity/security_evidence.json"
        data = self.load(path)
        data["profiles"]["protected_authorization"]["ordinary_continuity_receipt_sufficient"] = True
        self.save(path, data)
        self.assert_has("promoted to protected authorization evidence")

    def test_sur011_must_remain_unresolved(self) -> None:
        path = "continuity/security_evidence.json"
        data = self.load(path)
        data["sur011_state"] = "resolved"
        self.save(path, data)
        self.assert_has("SUR-011 is resolved")

    def test_reference_corpus_cannot_claim_provider_implementation(self) -> None:
        path = "continuity/local_mirror_profile.json"
        data = self.load(path)
        data["implementation_status"] = "implemented"
        self.save(path, data)
        self.assert_has("claims a provider implementation")

    def test_reference_archive_identity_is_pinned(self) -> None:
        path = "continuity/local_mirror_profile.json"
        data = self.load(path)
        data["reference_archive"]["sha256"] = "0" * 64
        self.save(path, data)
        self.assert_has("archive identity changed")

    def test_absolute_paths_are_forbidden_portable_refs(self) -> None:
        path = "continuity/local_mirror_profile.json"
        data = self.load(path)
        data["portability_contract"]["forbidden_references"] = []
        self.save(path, data)
        self.assert_has("permits absolute paths")

    def test_reference_cannot_self_certify_conformance(self) -> None:
        path = "continuity/local_mirror_profile.json"
        data = self.load(path)
        data["conformance_rule"] = "The archive is conforming."
        self.save(path, data)
        self.assert_has("self-certify provider conformance")

    def test_sur007_does_not_authorize_implementation(self) -> None:
        path = "continuity/sur007_disposition.json"
        data = self.load(path)
        data["implementation_authorized"] = True
        self.save(path, data)
        self.assert_has("authorizes implementation")

    def test_runtime_implementation_tree_is_rejected(self) -> None:
        path = self.root / "src/blu_runtime.py"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("pass\n", encoding="utf-8")
        self.assert_has("runtime or provider implementation exists")

    def test_executable_file_in_contract_tree_is_rejected(self) -> None:
        path = self.root / "continuity/provider.py"
        path.write_text("pass\n", encoding="utf-8")
        self.assert_has("executable continuity implementation exists")

    def test_schema_instance_matrix_exercises_required_conditionals(self) -> None:
        matrix = self.load("tests/continuity/fixtures/schema_instances.json")
        case_ids = {case["case_id"] for case in matrix["cases"]}
        required = {
            "receipt_completed_create_valid",
            "receipt_failed_valid",
            "receipt_stale_expected_version_conflict_valid",
            "receipt_mismatched_action_invalid",
            "mutation_expected_version_update_valid",
            "retrieval_not_found_valid",
            "retrieval_not_found_with_records_invalid",
            "retrieval_noncompleted_with_completed_receipt_invalid",
            "availability_unavailable_valid",
            "availability_degraded_valid",
            "record_invalid_drive_absolute_ref",
            "receipt_supersession_reciprocity_valid",
            "receipt_supersession_reciprocity_invalid",
            "receipt_noncompleted_success_fields_invalid",
        }
        self.assertTrue(required.issubset(case_ids), required - case_ids)
        self.assertEqual([], self.errors())

    def test_git_scope_guard_rejects_protected_path_change(self) -> None:
        self.init_git_scope_fixture()
        path = "contracts/successor/component_registry.json"
        data = self.load(path)
        data["fixture_mutation"] = True
        self.save(path, data)
        self.assert_has("protected path changed")

    def test_git_scope_allows_only_exact_bc041_sur001_resolution(self) -> None:
        path = "contracts/successor/unresolved_register.json"
        resolved = self.load(path)
        baseline = copy.deepcopy(resolved)
        sur001 = next(item for item in baseline["items"] if item["id"] == "SUR-001")
        for field in ("disposition", "resolution", "resolution_record", "remaining_security_inputs"):
            sur001.pop(field, None)
        sur001["blocking_for_implementation"] = True
        self.save(path, baseline)
        self.init_git_scope_fixture()
        self.save(path, resolved)
        self.assertEqual([], validator._validate_git_scope(self.root))
        current = self.load(path)
        next(item for item in current["items"] if item["id"] == "SUR-002")["risk"] = "mutated"
        self.save(path, current)
        self.assertTrue(any("protected path changed" in error for error in validator._validate_git_scope(self.root)))

    def test_git_scope_guard_rejects_disallowed_python(self) -> None:
        self.init_git_scope_fixture()
        path = self.root / "tools/unauthorized_runtime.py"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("pass\n", encoding="utf-8")
        self.git("add", "tools/unauthorized_runtime.py")
        self.assert_has("runtime or provider Python implementation changed")

    def test_git_scope_guard_rejects_pass_skillforge_bleed(self) -> None:
        self.init_git_scope_fixture()
        path = self.root / "pass/README.md"
        path.parent.mkdir(parents=True)
        path.write_text("not allowed\n", encoding="utf-8")
        self.git("add", "pass/README.md")
        self.assert_has("PASS/SkillForge scope bleed")

    def test_git_scope_guard_rejects_lm_studio_runtime_bleed(self) -> None:
        self.init_git_scope_fixture()
        path = self.root / "lm_studio/client.txt"
        path.parent.mkdir(parents=True)
        path.write_text("not allowed\n", encoding="utf-8")
        self.git("add", "lm_studio/client.txt")
        self.assert_has("LM Studio adapter implementation path changed")

    def test_manifest_coverage_guard_is_regression_protected(self) -> None:
        self.init_git_scope_fixture()
        path = self.root / "readiness/new-contract.json"
        path.parent.mkdir(parents=True)
        path.write_text("{}\n", encoding="utf-8")
        self.git("add", "readiness/new-contract.json")
        self.assert_has("missing from MANIFEST.sha256")

    def test_manifest_digest_guard_uses_index_blob_bytes(self) -> None:
        self.init_git_scope_fixture()
        path = "continuity/lifecycle.json"
        data = self.load(path)
        data["fixture_digest_mutation"] = True
        self.save(path, data)
        self.git("add", path)
        self.assert_has("MANIFEST.sha256 digest mismatch")


if __name__ == "__main__":
    unittest.main()
