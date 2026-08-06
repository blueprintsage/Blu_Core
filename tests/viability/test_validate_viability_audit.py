import copy
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
VALIDATOR_PATH = REPO_ROOT / "tools" / "validate_viability_audit.py"
SPEC = importlib.util.spec_from_file_location("validate_viability_audit", VALIDATOR_PATH)
VALIDATOR = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(VALIDATOR)


class ViabilityAuditValidationTests(unittest.TestCase):
    def setUp(self):
        self.audit_rel = Path("docs/domains/runtime/viability")

    def copy_tree(self, destination: Path) -> None:
        shutil.copytree(REPO_ROOT / self.audit_rel, destination / self.audit_rel)
        contract_target = destination / "contracts/runtime"
        contract_target.mkdir(parents=True)
        for name in (
            "component_registry.json",
            "route_registry.json",
            "parity_matrix.json",
            "unresolved_register.json",
        ):
            shutil.copy2(REPO_ROOT / "contracts/runtime" / name, contract_target / name)

    def mutate(self, root: Path, filename: str, callback) -> None:
        path = root / self.audit_rel / filename
        document = json.loads(path.read_text(encoding="utf-8"))
        callback(document)
        path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")

    def errors_after(self, callback, filename="viability_matrix.json"):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.copy_tree(root)
            self.mutate(root, filename, callback)
            return VALIDATOR.validate_audit(root)

    def test_repository_audit_passes(self):
        self.assertEqual([], VALIDATOR.validate_audit(REPO_ROOT))

    def test_unknown_classification_fails(self):
        errors = self.errors_after(
            lambda doc: doc["capabilities"][0].__setitem__(
                "current_viability_class", "certainly_live"
            )
        )
        self.assertTrue(any("unknown classification" in error for error in errors))

    def test_missing_evidence_reference_fails(self):
        errors = self.errors_after(
            lambda doc: doc["capabilities"][0]["evidence_ids"].append("EV-MISSING")
        )
        self.assertTrue(any("missing evidence reference EV-MISSING" in error for error in errors))

    def test_uncovered_component_fails(self):
        errors = self.errors_after(
            lambda doc: doc["capabilities"][0].__setitem__("covered_component_ids", [])
        )
        self.assertTrue(any("uncovered component entry: 00 Instructions" in error for error in errors))

    def test_duplicate_capability_id_fails(self):
        def duplicate(doc):
            item = copy.deepcopy(doc["capabilities"][0])
            doc["capabilities"].append(item)

        errors = self.errors_after(duplicate)
        self.assertTrue(any("duplicate capability id" in error for error in errors))

    def test_invalid_proposed_disposition_fails(self):
        errors = self.errors_after(
            lambda doc: doc["capabilities"][0].__setitem__(
                "proposed_disposition", "ship_everything"
            )
        )
        self.assertTrue(any("invalid proposed disposition" in error for error in errors))

    def test_live_and_stable_requires_observable_repeatable_evidence(self):
        def static_only(doc):
            item = doc["capabilities"][0]
            item["current_viability_class"] = "live_and_stable"
            item["evidence_ids"] = ["EV-001"]

        errors = self.errors_after(static_only)
        self.assertTrue(any("lacks repeatable observable evidence" in error for error in errors))

    def test_historical_evidence_requires_archive_identity(self):
        def broken_history(doc):
            item = next(entry for entry in doc["entries"] if entry["id"] == "EV-032")
            item["evidence_class"] = "historical_baseline"
            item.pop("archive_filename", None)
            item.pop("archive_sha256", None)
            item.pop("member_path", None)

        errors = self.errors_after(broken_history, "evidence_register.json")
        self.assertTrue(any("historical evidence missing archive_filename" in error for error in errors))
        self.assertTrue(any("historical evidence missing archive_sha256" in error for error in errors))
        self.assertTrue(any("historical evidence missing member_path" in error for error in errors))

    def test_successor_decision_cannot_be_golden_declaration(self):
        def project_as_golden(doc):
            item = next(entry for entry in doc["entries"] if entry["id"] == "EV-029")
            item["evidence_class"] = "golden_declaration"

        errors = self.errors_after(project_as_golden, "evidence_register.json")
        self.assertTrue(any("projected backward as a golden declaration" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
