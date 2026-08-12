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


class PythonReadinessValidationTests(unittest.TestCase):
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

    def test_independent_review_pending_is_not_completion(self) -> None:
        path = "readiness/python_phase1_readiness_checklist.json"
        data = self.load(path)
        checks = {item["id"]: item for item in data["checks"]}
        checks["independent_Claude_correction_review"]["status"] = "pass"
        data["independent_correction_review"]["state"] = "complete"
        data["independent_correction_review"]["completed"] = True
        self.save(path, data)
        self.assert_has("not required_pending")
        self.assert_has("mistaken for completion")

    def test_pending_review_cannot_authorize_implementation(self) -> None:
        path = "readiness/python_phase1_readiness_checklist.json"
        data = self.load(path)
        data["implementation_authorized"] = True
        self.save(path, data)
        self.assert_has("authorizes implementation before independent review")

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
