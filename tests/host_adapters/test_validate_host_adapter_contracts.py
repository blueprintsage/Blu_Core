from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "validate_host_adapter_contracts",
    ROOT / "tools/validate_host_adapter_contracts.py",
)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class HostAdapterContractValidationTests(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        for relative in {
            *validator.REQUIRED,
            Path("kernel/golden/v0.22.0/SHA256SUMS"),
            *[Path("kernel/golden/v0.22.0") / line.split(None, 1)[1].strip()
              for line in (ROOT / "kernel/golden/v0.22.0/SHA256SUMS").read_text(encoding="utf-8").splitlines()
              if line.strip()],
        }:
            source = ROOT / relative
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def load(self, relative: str) -> dict:
        return json.loads((self.root / relative).read_text(encoding="utf-8"))

    def save(self, relative: str, value: dict) -> None:
        (self.root / relative).write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

    def errors(self) -> list[str]:
        return validator.validate(self.root)

    def assert_has(self, fragment: str) -> None:
        errors = self.errors()
        self.assertTrue(any(fragment in error for error in errors), errors)

    def test_canonical_contracts_pass(self) -> None:
        self.assertEqual([], self.errors())

    def test_missing_required_file_fails(self) -> None:
        (self.root / "adapters/common/capability_contract.json").unlink()
        self.assert_has("missing required file")

    def test_malformed_json_fails(self) -> None:
        (self.root / "adapters/chat/capability_matrix.json").write_text("{", encoding="utf-8")
        self.assert_has("invalid JSON")

    def test_duplicate_capability_id_fails(self) -> None:
        path = "adapters/chat/capability_matrix.json"
        data = self.load(path)
        data["capabilities"].append(dict(data["capabilities"][0]))
        self.save(path, data)
        self.assert_has("duplicate chatgpt capability ID")

    def test_unknown_evidence_ref_fails(self) -> None:
        path = "adapters/codex/capability_matrix.json"
        data = self.load(path)
        data["capabilities"][0]["evidence_refs"] = ["NO-SUCH-EVIDENCE"]
        self.save(path, data)
        self.assert_has("unknown codex evidence ref")

    def test_documentation_alone_cannot_verify_available(self) -> None:
        path = "adapters/chat/capability_matrix.json"
        data = self.load(path)
        data["capabilities"][0]["status"] = "verified_available"
        self.save(path, data)
        self.assert_has("verified_available lacks current runtime evidence")

    def test_verified_rule_requires_semantic_evidence_relevance(self) -> None:
        path = "adapters/common/capability_contract.json"
        data = self.load(path)
        data["capability_record"]["verified_available_rule"] = (
            "At least one referenced evidence entry must be local_probe or host_receipt. "
            "official_documentation alone is insufficient."
        )
        self.save(path, data)
        self.assert_has("verified capability rule lacks semantic evidence relevance")

    def test_unknown_status_is_permitted(self) -> None:
        path = "adapters/codex/capability_matrix.json"
        data = self.load(path)
        record = next(item for item in data["capabilities"] if item["capability_id"] == "action.git.commit")
        record["status"] = "unknown"
        self.save(path, data)
        self.assertEqual([], self.errors())

    def test_corrected_unknown_scheduling_rows_pass(self) -> None:
        data = self.load("adapters/codex/capability_matrix.json")
        scheduling = {
            item["capability_id"]: item["status"]
            for item in data["capabilities"]
            if item["capability_id"] in {
                "schedule.create", "schedule.recurring", "schedule.update_cancel"
            }
        }
        self.assertEqual(
            {
                "schedule.create": "unknown",
                "schedule.recurring": "unknown",
                "schedule.update_cancel": "unknown",
            },
            scheduling,
        )
        self.assertEqual([], self.errors())

    def _assert_interface_only_schedule_fails(self, capability_id: str) -> None:
        path = "adapters/codex/capability_matrix.json"
        data = self.load(path)
        record = next(item for item in data["capabilities"] if item["capability_id"] == capability_id)
        record["status"] = "verified_available"
        record["evidence_refs"] = ["CODEX-EVID-PROBE-TOOLS"]
        self.save(path, data)
        self.assert_has(f"lacks semantically relevant current evidence: {capability_id}")
        self.assert_has(f"verified scheduling lacks operational evidence: codex {capability_id}")

    def test_schedule_create_interface_exposure_cannot_verify_available(self) -> None:
        self._assert_interface_only_schedule_fails("schedule.create")

    def test_schedule_recurring_interface_exposure_cannot_verify_available(self) -> None:
        self._assert_interface_only_schedule_fails("schedule.recurring")

    def test_schedule_update_cancel_interface_exposure_cannot_verify_available(self) -> None:
        self._assert_interface_only_schedule_fails("schedule.update_cancel")

    def test_unrelated_time_receipt_cannot_verify_git_push(self) -> None:
        path = "adapters/codex/capability_matrix.json"
        data = self.load(path)
        record = next(item for item in data["capabilities"] if item["capability_id"] == "action.git.push")
        record["status"] = "verified_available"
        record["evidence_refs"] = ["CODEX-EVID-RECEIPT-TIME"]
        self.save(path, data)
        self.assert_has("lacks semantically relevant current evidence: action.git.push")

    def test_web_search_evidence_cannot_verify_raw_network(self) -> None:
        path = "adapters/codex/capability_matrix.json"
        data = self.load(path)
        record = next(item for item in data["capabilities"] if item["capability_id"] == "action.raw_network")
        record["status"] = "verified_available"
        record["evidence_refs"] = ["CODEX-EVID-RECEIPT-WEB"]
        self.save(path, data)
        self.assert_has("lacks semantically relevant current evidence: action.raw_network")

    def test_negative_attempt_gap_cannot_verify_positive_integrity(self) -> None:
        path = "adapters/codex/capability_matrix.json"
        data = self.load(path)
        record = next(
            item for item in data["capabilities"]
            if item["capability_id"] == "security.attempt_count_integrity"
        )
        record["status"] = "verified_available"
        record["evidence_refs"] = ["CODEX-EVID-PROBE-SECURITY-GAP"]
        self.save(path, data)
        self.assert_has(
            "lacks semantically relevant current evidence: security.attempt_count_integrity"
        )

    def test_existing_valid_verified_rows_have_relevant_evidence(self) -> None:
        self.assertEqual([], self.errors())

    def test_host_adapter_cannot_produce_turn_request(self) -> None:
        path = "adapters/common/capability_contract.json"
        data = self.load(path)
        data["host_adapter_constraints"]["does_not_produce"] = "none"
        self.save(path, data)
        self.assert_has("permitted to produce TurnRequest")

    def test_host_adapter_cannot_own_auth_policy(self) -> None:
        path = "adapters/common/capability_contract.json"
        data = self.load(path)
        data["host_adapter_constraints"]["does_not_own"].remove("Auth_policy")
        self.save(path, data)
        self.assert_has("fails to disown OPSEC/Auth")

    def test_product_sign_in_cannot_become_blu_auth(self) -> None:
        path = "adapters/common/authorization_transport_contract.json"
        data = self.load(path)
        data["authorization_evidence_transport"]["sign_in_rule"] = "Product sign-in is Blu authorization."
        self.save(path, data)
        self.assert_has("product sign-in can become Blu Auth")

    def test_host_approval_cannot_become_blu_auth(self) -> None:
        path = "adapters/common/authorization_transport_contract.json"
        data = self.load(path)
        data["host_approval_evidence"]["rule"] = "Host approval grants AuthorizationResult."
        self.save(path, data)
        self.assert_has("host approval can become Blu authorization")

    def test_conversation_history_cannot_create_session_evidence(self) -> None:
        path = "adapters/common/session_evidence_contract.json"
        data = self.load(path)
        data["host_session_evidence"]["truth_rule"] = "Conversation history is sufficient."
        self.save(path, data)
        self.assert_has("inferred from conversation history")

    def test_request_string_equality_is_insufficient(self) -> None:
        path = "adapters/common/authorization_transport_contract.json"
        data = self.load(path)
        data["authorization_result_binding"]["string_equality_sufficient"] = True
        self.save(path, data)
        self.assert_has("request-ref equality")

    def test_security_grade_requires_rollback_evidence(self) -> None:
        path = "adapters/common/capability_contract.json"
        data = self.load(path)
        data["security_evidence_grade_values"]["security_grade"] = "Binding, integrity, freshness, and replay only."
        self.save(path, data)
        self.assert_has("security_grade lacks explicit")

    def test_mutable_attempt_state_cannot_qualify(self) -> None:
        path = "adapters/common/session_evidence_contract.json"
        data = self.load(path)
        data["attempt_count_integrity"]["client_local_mutable_state_qualifies"] = True
        self.save(path, data)
        self.assert_has("untrusted mutable attempt state")

    def test_attempt_state_requires_rollback_resistance(self) -> None:
        path = "adapters/common/session_evidence_contract.json"
        data = self.load(path)
        data["attempt_count_integrity"]["required_properties_for_protected_cross_turn_use"].remove("monotonic_or_rollback_resistant_attempt_state")
        self.save(path, data)
        self.assert_has("lacks rollback-resistant state")

    def test_current_time_requires_provider_receipt(self) -> None:
        path = "adapters/codex/capability_matrix.json"
        data = self.load(path)
        record = next(item for item in data["capabilities"] if item["capability_id"] == "time.current_time")
        record["evidence_refs"] = ["CODEX-EVID-DOC-WEB"]
        self.save(path, data)
        self.assert_has("verified current time lacks provider receipt")

    def test_side_effect_success_requires_receipt(self) -> None:
        path = "adapters/common/receipt_contract.json"
        data = self.load(path)
        data["side_effect_rule"] = "A requested action is completed."
        self.save(path, data)
        self.assert_has("external side-effect success")

    def test_filesystem_scopes_must_be_explicit(self) -> None:
        path = "adapters/common/host_surface_contract.json"
        data = self.load(path)
        data["filesystem_scope_values"].remove("unknown")
        self.save(path, data)
        self.assert_has("filesystem scope vocabulary")

    def test_network_classes_must_be_separate(self) -> None:
        path = "adapters/common/host_surface_contract.json"
        data = self.load(path)
        data["network_classes"] = ["network"]
        self.save(path, data)
        self.assert_has("network classes")

    def test_local_probe_requires_surface_and_freshness(self) -> None:
        path = "adapters/codex/evidence_register.json"
        data = self.load(path)
        record = next(item for item in data["entries"] if item["evidence_class"] == "local_probe")
        record["surface_id"] = "all_bindings"
        record["freshness"] = "unknown"
        self.save(path, data)
        self.assert_has("local probe lacks actual surface scope")
        self.assert_has("local probe lacks bounded freshness")

    def test_sur011_must_remain_unresolved(self) -> None:
        path = "adapters/security/sur012_disposition.json"
        data = self.load(path)
        data["sur011_state"] = "resolved"
        self.save(path, data)
        self.assert_has("SUR-011 is resolved")

    def test_sur012_requires_explicit_disposition(self) -> None:
        path = "adapters/security/sur012_disposition.json"
        data = self.load(path)
        data["disposition"] = "unresolved"
        self.save(path, data)
        self.assert_has("SUR-012 lacks explicit")

    def test_host_session_cannot_claim_durable_persistence(self) -> None:
        path = "adapters/common/session_evidence_contract.json"
        data = self.load(path)
        data["durability_boundary"] = "host_session is durable_external."
        self.save(path, data)
        self.assert_has("durable persistence is claimed")

    def test_runtime_adapter_implementation_is_rejected(self) -> None:
        path = self.root / "adapters/chat/adapter.py"
        path.write_text("pass\n", encoding="utf-8")
        self.assert_has("runtime adapter implementation exists")


if __name__ == "__main__":
    unittest.main()
