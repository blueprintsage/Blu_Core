from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "validate_python_readiness", ROOT / "tools/validate_python_readiness.py"
)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


_MATRIX_SPEC = importlib.util.spec_from_file_location(
    "bc050_authorization_matrix", ROOT / "tests/readiness/bc050_authorization_matrix.py"
)
assert _MATRIX_SPEC and _MATRIX_SPEC.loader
matrix = importlib.util.module_from_spec(_MATRIX_SPEC)
_MATRIX_SPEC.loader.exec_module(matrix)


class _ReadinessHarness(unittest.TestCase):
    """Shared temp-root harness. Holds no test methods."""

    maxDiff = None

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
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
        self.temp.cleanup()

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


class PythonReadinessValidationTests(_ReadinessHarness):
    def test_canonical_readiness_contracts_pass(self) -> None:
        self.assertEqual([], self.errors())

    def test_component_count_remains_seven(self) -> None:
        path = "contracts/successor/component_registry.json"
        data = self.load(path)
        data["components"].append(dict(data["components"][0]))
        self.save(path, data)
        self.assert_has("count is not seven")

    def test_required_targets_and_optional_codex_are_guarded(self) -> None:
        path = "readiness/deployment_targets.json"
        data = self.load(path)
        next(item for item in data["targets"] if item["target_id"] == "codex")["classification"] = "required"
        self.save(path, data)
        self.assert_has("Codex target is not optional_best_effort")

    def test_phase1_route_catalog_is_finite(self) -> None:
        path = "readiness/phase1_executable_slice.json"
        data = self.load(path)
        data["route_catalog"].append({"route_id": "memory"})
        self.save(path, data)
        self.assert_has("not finite ordinary conversation only")

    def test_every_current_gap_requires_disposition(self) -> None:
        path = "readiness/implementation_gap_dispositions.json"
        data = self.load(path)
        data["dispositions"] = data["dispositions"][:-1]
        self.save(path, data)
        self.assert_has("does not cover all 28")

    def test_every_implementation_blocker_requires_disposition(self) -> None:
        path = "readiness/implementation_blocker_dispositions.json"
        data = self.load(path)
        data["dispositions"] = [item for item in data["dispositions"] if item["id"] != "SUR-012"]
        self.save(path, data)
        self.assert_has("not every successor unresolved item")

    def test_sur001_requires_bounded_resolution_contract(self) -> None:
        path = "readiness/implementation_blocker_dispositions.json"
        data = self.load(path)
        item = next(item for item in data["dispositions"] if item["id"] == "SUR-001")
        item.pop("disposition")
        item["phase1_resolved"] = False
        self.save(path, data)
        self.assert_has("not resolved at the minimum")

    def test_provider_configuration_cannot_imply_chat_capability(self) -> None:
        path = "readiness/model_execution_provider_contract.json"
        data = self.load(path)
        next(item for item in data["phase1_capabilities"] if item["capability"] == "ordinary_chat_completion")["classification"] = "configured"
        self.save(path, data)
        self.assert_has("ordinary chat completion is not required")

    def test_streaming_and_tool_execution_remain_unsupported(self) -> None:
        path = "readiness/model_execution_provider_contract.json"
        data = self.load(path)
        next(item for item in data["phase1_capabilities"] if item["capability"] == "streaming")["classification"] = "required"
        next(item for item in data["phase1_capabilities"] if item["capability"] == "tool_execution")["classification"] = "required"
        self.save(path, data)
        self.assert_has("streaming policy")
        self.assert_has("permits tool execution")

    def test_lm_studio_remains_model_boundary_only(self) -> None:
        path = "readiness/model_execution_provider_contract.json"
        data = self.load(path)
        data["architectural_component"] = "lm_studio_component"
        data["new_component_added"] = True
        self.save(path, data)
        self.assert_has("new architectural component")

    def test_layout_maps_beneath_seven_boundaries(self) -> None:
        path = "readiness/python_package_layout.json"
        data = self.load(path)
        data["architecture_mapping"]["session_manager"] = ["session.py"]
        self.save(path, data)
        self.assert_has("exactly seven components")

    def test_readiness_cannot_retain_stale_blocker_state(self) -> None:
        path = "readiness/python_phase1_readiness_checklist.json"
        data = self.load(path)
        data["result"] = "not_ready_for_python_phase1"
        data["runtime_phase1_packet_may_be_authored_next"] = False
        data["actual_blockers"] = [{"id": "SUR-001"}]
        self.save(path, data)
        self.assert_has("does not reflect resolved SUR-001")
        self.assert_has("retains stale blockers")
        self.assert_has("may not be authored")

    def test_independent_review_completion_cannot_regress_to_pending(self) -> None:
        path = "readiness/python_phase1_readiness_checklist.json"
        data = self.load(path)
        checks = {item["id"]: item for item in data["checks"]}
        checks["independent_Claude_correction_review"]["status"] = "required_pending"
        data["independent_correction_review"]["state"] = "required_pending"
        data["independent_correction_review"]["completed"] = False
        self.save(path, data)
        self.assert_has("not complete")
        self.assert_has("completion is not recorded")

    def test_authorization_without_evidence_is_rejected(self) -> None:
        """BC-050-C1: the flag alone never authorizes implementation.

        Before BC-050 this asserted that `implementation_authorized` could
        never be true. It is now true under explicit Dad/Blu evidence, so the
        test asserts the property that actually matters: stripping the
        authorization record while leaving the flag set must still fail.
        """
        path = "readiness/python_phase1_readiness_checklist.json"
        data = self.load(path)
        del data["bc050_implementation_authorization"]
        data["implementation_authorized"] = True
        self.save(path, data)
        self.assert_has("authorization disagrees with the BC-050 authorization record")

    def test_closure_receipts_are_pinned(self) -> None:
        path = "readiness/python_phase1_readiness_checklist.json"
        data = self.load(path)
        checks = {item["id"]: item for item in data["checks"]}
        checks["BC_041_and_BC_041_C1_Dad_Blu_closure"]["status"] = "required_pending"
        data["dad_blu_closure"]["state"] = "required_pending"
        data["dad_blu_closure"]["review_source_commit"] = "0" * 40
        self.save(path, data)
        self.assert_has("closure is not complete")
        self.assert_has("does not bind the final Claude review")

    def test_readiness_cannot_turn_green_without_expanded_mixed_cf_proof(self) -> None:
        path = "tests/security/fixtures/synthetic_cases.json"
        data = self.load(path)
        data["ingress"] = [item for item in data["ingress"] if item.get("cf_position") != "mixed"]
        self.save(path, data)
        self.assert_has("expanded OPSEC proof failed: ingress Cf probe matrix is incomplete")
        self.assert_has("expanded OPSEC proof failed: ingress cross-code-point mixed Cf probe is missing")

    def test_readiness_cannot_turn_green_without_outer_edge_cf_proof(self) -> None:
        path = "tests/security/fixtures/synthetic_cases.json"
        data = self.load(path)
        data["egress"] = [
            item for item in data["egress"]
            if item.get("cf_position") not in {"leading_outer_edge", "trailing_outer_edge", "both_outer_edges"}
            and item.get("attack_class") is None
        ]
        self.save(path, data)
        self.assert_has("expanded OPSEC proof failed: egress Cf probe matrix is incomplete")
        self.assert_has("expanded OPSEC proof failed: egress outer-edge attack classes are incomplete")

    def test_projection_guard_detects_missing_stale_and_redefinition(self) -> None:
        manifest = self.load("readiness/one_blu_canon_manifest.json")
        first = manifest["mappings"][0]
        projection = {
            "target_id": "python_lm_studio",
            "entries": [{
                "mapping_id": first["mapping_id"],
                "source_digest_current": False,
                "transformation_type": "independent_copy",
                "canonical_subject_override": "Python-only Persona",
            }],
        }
        errors = validator.validate_projection(manifest, projection)
        self.assertTrue(any("missing canonical mapping" in item for item in errors), errors)
        self.assertTrue(any("source digest is stale" in item for item in errors), errors)
        self.assertTrue(any("transformation is not allowed" in item for item in errors), errors)
        self.assertTrue(any("redefines canonical behavior" in item for item in errors), errors)


if __name__ == "__main__":
    unittest.main()


class BC050AuthorizationGateTests(_ReadinessHarness):
    """BC-050-C1: authorized implementation is permitted; stale states fail."""

    CHECKLIST = "readiness/python_phase1_readiness_checklist.json"
    SLICE = "readiness/phase1_executable_slice.json"
    LAYOUT = "readiness/python_package_layout.json"

    def test_authorized_state_passes(self) -> None:
        self.assertEqual([], self.errors())

    def test_authorization_record_is_required_for_authorized_state(self) -> None:
        checklist = self.load(self.CHECKLIST)
        del checklist["bc050_implementation_authorization"]
        self.save(self.CHECKLIST, checklist)
        self.assert_has("authorization disagrees with the BC-050 authorization record")

    def test_authorization_record_must_name_assignment_bc050(self) -> None:
        checklist = self.load(self.CHECKLIST)
        checklist["bc050_implementation_authorization"]["assignment"] = "BC-999"
        self.save(self.CHECKLIST, checklist)
        self.assert_has("authorization disagrees with the BC-050 authorization record")

    def test_authorization_record_must_bind_authorizing_party_and_packet(self) -> None:
        """B-01: a wrong authorizer restores the prohibition in this validator."""
        checklist = self.load(self.CHECKLIST)
        checklist["bc050_implementation_authorization"]["authorized_by"] = "someone else"
        self.save(self.CHECKLIST, checklist)
        self.assertFalse(validator._bc050_authorized(self.root))
        self.assertNotEqual([], self.errors())

    def test_slice_and_checklist_authorization_must_agree(self) -> None:
        """B-01: cross-file disagreement is not authorization."""
        document = self.load(self.SLICE)
        document["implementation_authorized"] = False
        self.save(self.SLICE, document)
        self.assertFalse(validator._bc050_authorized(self.root))
        self.assertNotEqual([], self.errors())

    def test_implementation_present_must_match_authorization(self) -> None:
        layout = self.load(self.LAYOUT)
        layout["implementation_present"] = False
        self.save(self.LAYOUT, layout)
        self.assert_has("implementation state disagrees with BC-050 authorization")

    def test_automatic_start_prohibition_is_ungated(self) -> None:
        checklist = self.load(self.CHECKLIST)
        checklist["automatic_start_prohibited"] = False
        self.save(self.CHECKLIST, checklist)
        self.assert_has("readiness automatically starts runtime implementation")

    def test_stale_result_semantics_fail_under_authorization(self) -> None:
        checklist = self.load(self.CHECKLIST)
        checklist["result_semantics"] = (
            "technical_conditions_satisfied_independent_correction_review_and_"
            "Dad_Blu_closure_complete_implementation_authorization_pending"
        )
        self.save(self.CHECKLIST, checklist)
        self.assert_has("readiness result does not distinguish technical status")

    def test_stale_no_runtime_code_assertion_is_rejected(self) -> None:
        checklist = self.load(self.CHECKLIST)
        checklist["checks"].append({"id": "no_runtime_code_introduced", "status": "pass"})
        self.save(self.CHECKLIST, checklist)
        self.assert_has("stale pre-implementation runtime-code assertion")

    def test_authorized_state_requires_the_scope_check(self) -> None:
        checklist = self.load(self.CHECKLIST)
        checklist["checks"] = [
            item
            for item in checklist["checks"]
            if item.get("id") != "runtime_phase1_code_introduced_only_under_BC050_authorization"
        ]
        self.save(self.CHECKLIST, checklist)
        self.assert_has("does not record the BC-050 scope check")

    def test_support_module_cannot_claim_a_component(self) -> None:
        layout = self.load(self.LAYOUT)
        layout["architecture_mapping"]["turn_controller"].append("config.py")
        self.save(self.LAYOUT, layout)
        self.assert_has("support module claims an architectural component")

    def test_every_phase1_path_needs_a_classification(self) -> None:
        layout = self.load(self.LAYOUT)
        del layout["paths"][0]["classification"]
        self.save(self.LAYOUT, layout)
        self.assert_has("no declared classification")

    def test_support_roster_must_match_declared_classifications(self) -> None:
        layout = self.load(self.LAYOUT)
        layout["support_layer"]["modules"].pop()
        self.save(self.LAYOUT, layout)
        self.assert_has("support layer roster disagrees")

    def test_canon_loader_constraints_are_required(self) -> None:
        layout = self.load(self.LAYOUT)
        layout["support_layer"]["canon_loader_prohibitions"] = []
        self.save(self.LAYOUT, layout)
        self.assert_has("does not constrain the canonical source loader")


class BC050AuthorizationMutationMatrixTests(_ReadinessHarness):
    """B-01: this validator rejects every malformed record on its own."""

    def test_authorized_baseline_passes(self) -> None:
        self.assertEqual([], self.errors())

    def test_every_mutation_is_rejected_independently(self) -> None:
        for label, mutate in matrix.MUTATIONS:
            with self.subTest(mutation=label):
                self.setUp()
                try:
                    matrix.apply_mutation(self.root, mutate)
                    self.assertNotEqual(
                        [], self.errors(), f"{label} did not restore the prohibition"
                    )
                finally:
                    self.tearDown()

    def test_predicate_rejects_every_mutation(self) -> None:
        self.assertTrue(validator._bc050_authorized(self.root))
        for label, mutate in matrix.MUTATIONS:
            with self.subTest(mutation=label):
                self.setUp()
                try:
                    matrix.apply_mutation(self.root, mutate)
                    self.assertFalse(
                        validator._bc050_authorized(self.root), f"{label} authenticated"
                    )
                finally:
                    self.tearDown()
