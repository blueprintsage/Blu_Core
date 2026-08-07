import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "tools"))

from validate_historical_behavioral_archaeology import validate  # noqa: E402


class HistoricalBehavioralArchaeologyValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        for source in (
            "docs/sources/historical_archives/kernel_archive_inventory.json",
            "docs/sources/historical_archives/behavioral_archaeology",
            "docs/domains/runtime/assignments/BC-017",
            "kernel/golden/v0.22.0",
        ):
            src = REPO_ROOT / source
            dst = self.root / source
            dst.parent.mkdir(parents=True, exist_ok=True)
            if src.is_dir():
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
        self.boundary_path = self.root / "docs/sources/historical_archives/behavioral_archaeology/boundary_specimens.json"
        self.evidence_path = self.root / "docs/sources/historical_archives/behavioral_archaeology/evidence_register.json"
        self.matrix_path = self.root / "docs/sources/historical_archives/behavioral_archaeology/behavior_recovery_matrix.md"

    def tearDown(self):
        self.temp.cleanup()

    @staticmethod
    def load(path):
        return json.loads(path.read_text(encoding="utf-8"))

    @staticmethod
    def save(path, data):
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    def assert_error(self, expected):
        errors = validate(self.root)
        self.assertTrue(any(expected in error for error in errors), errors)

    def test_canonical_records_pass(self):
        self.assertEqual([], validate(REPO_ROOT))

    def test_unknown_archive_id_fails(self):
        data = self.load(self.boundary_path)
        data["families"][0]["first_specimen_archive_id"] = "BLU-HIST-9999"
        self.save(self.boundary_path, data)
        self.assert_error("unknown archive ID")

    def test_path_leakage_forms_fail(self):
        readme = self.root / "docs/sources/historical_archives/behavioral_archaeology/README.md"
        original = readme.read_text(encoding="utf-8")
        for leak in ("C:\\private\\x", "\\\\host\\share", "file://secret", "../secret", "%2e%2e/secret"):
            with self.subTest(leak=leak):
                readme.write_text(original + "\n" + leak, encoding="utf-8")
                self.assert_error("path leakage")
                readme.write_text(original, encoding="utf-8")

    def test_missing_selection_basis_fails(self):
        data = self.load(self.boundary_path)
        data["families"][0]["selection_basis"] = ""
        self.save(self.boundary_path, data)
        self.assert_error("missing selection basis")

    def test_null_boundary_without_reason_fails(self):
        data = self.load(self.boundary_path)
        data["families"][0]["last_specimen_archive_id"] = None
        data["families"][0]["boundary_ambiguity"] = None
        self.save(self.boundary_path, data)
        self.assert_error("null last boundary")

    def test_unsupported_specimen_fails(self):
        inventory = self.load(self.root / "docs/sources/historical_archives/kernel_archive_inventory.json")
        unsupported = next(item["archive_id"] for item in inventory["inventory"]
                           if item["integrity_status"] != "readable" and item["archive_id"].startswith("BLU-HIST"))
        data = self.load(self.boundary_path)
        data["families"][0]["first_specimen_archive_id"] = unsupported
        self.save(self.boundary_path, data)
        self.assert_error("unsupported/unavailable specimen")

    def test_disallowed_matrix_disposition_fails(self):
        text = self.matrix_path.read_text(encoding="utf-8")
        self.matrix_path.write_text(text.replace("recover_model_facing_guidance", "restore_module", 1), encoding="utf-8")
        self.assert_error("disallowed disposition")

    def test_matrix_locator_required(self):
        text = self.matrix_path.read_text(encoding="utf-8")
        self.matrix_path.write_text(text.replace("E-00020-TEACH |", " |", 1), encoding="utf-8")
        self.assert_error("lacks evidence locator")

    def test_factual_finding_requires_locator(self):
        data = self.load(self.evidence_path)
        finding = next(item for item in data["findings"] if item["label"] == "historical_declared")
        finding["locator_ids"] = []
        self.save(self.evidence_path, data)
        self.assert_error("factual historical finding lacks evidence locator")

    def test_owner_observation_requires_owner_link(self):
        data = self.load(self.evidence_path)
        finding = next(item for item in data["findings"] if item["label"] == "owner_observation")
        finding.pop("owner_observation_id")
        self.save(self.evidence_path, data)
        self.assert_error("owner observation is not linked/labeled")

    def test_current_claim_requires_current_source(self):
        data = self.load(self.evidence_path)
        finding = next(item for item in data["findings"] if item["label"] == "current_source_truth")
        finding["locator_ids"] = ["E-00020-TEACH"]
        self.save(self.evidence_path, data)
        self.assert_error("not sourced as current_source_truth")

    def test_inference_requires_supported_findings(self):
        data = self.load(self.evidence_path)
        finding = next(item for item in data["findings"] if item["label"] == "inference")
        finding["supporting_finding_ids"] = []
        self.save(self.evidence_path, data)
        self.assert_error("inference is mislabeled")

    def test_legacy_pass_must_be_chronology_only(self):
        text = self.matrix_path.read_text(encoding="utf-8")
        line = next(line for line in text.splitlines() if line.startswith("| legacy PASS |"))
        changed = line.replace("| chronology_only |", "| recover_lightweight_profile |")
        self.matrix_path.write_text(text.replace(line, changed), encoding="utf-8")
        self.assert_error("legacy PASS receives a recovery disposition")

    def test_faithfulness_cannot_be_shipped(self):
        data = self.load(self.evidence_path)
        data["faithfulness_sidecar"]["classification"] = "shipped_historical_component"
        self.save(self.evidence_path, data)
        self.assert_error("Faithfulness sidecar is labeled shipped")

    def test_archive_payload_fails(self):
        payload = self.root / "docs/sources/historical_archives/behavioral_archaeology/private.zip"
        payload.write_bytes(b"not a real archive")
        self.assert_error("archive payload present")

    def test_golden_change_fails(self):
        target = self.root / "kernel/golden/v0.22.0/03_Exec.md"
        target.write_text(target.read_text(encoding="utf-8") + "\nchanged", encoding="utf-8")
        self.assert_error("golden checksum mismatch")

    def test_python_runtime_in_assignment_fails(self):
        target = self.root / "docs/domains/runtime/assignments/BC-017/runtime.py"
        target.write_text("print('runtime')\n", encoding="utf-8")
        self.assert_error("Python runtime/control-plane implementation")

    def test_review_must_remain_pending(self):
        review = self.root / "docs/domains/runtime/assignments/BC-017/review.md"
        review.write_text("# Review\n\nstatus: approved\n", encoding="utf-8")
        self.assert_error("review.md is not pending")


if __name__ == "__main__":
    unittest.main()
