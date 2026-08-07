import csv
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "tools"))

from validate_historical_archive_inventory import validate  # noqa: E402


class HistoricalArchiveInventoryValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        target = self.root / "docs/sources/historical_archives"
        target.parent.mkdir(parents=True)
        shutil.copytree(REPO_ROOT / "docs/sources/historical_archives", target)
        self.inventory_path = target / "kernel_archive_inventory.json"
        self.snapshot_path = target / "snapshot_receipt.json"
        self.csv_path = target / "kernel_archive_inventory.csv"

    def tearDown(self):
        self.temp.cleanup()

    def load_inventory(self):
        return json.loads(self.inventory_path.read_text(encoding="utf-8"))

    def save_inventory(self, data):
        self.inventory_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    def assert_error(self, expected):
        errors = validate(self.root)
        self.assertTrue(any(expected in error for error in errors), errors)

    def test_canonical_inventory_passes(self):
        self.assertEqual([], validate(REPO_ROOT))

    def test_duplicate_archive_id_fails(self):
        data = self.load_inventory()
        data["inventory"][1]["archive_id"] = data["inventory"][0]["archive_id"]
        self.save_inventory(data)
        self.assert_error("duplicate archive ID")

    def test_unknown_branch_fails(self):
        data = self.load_inventory()
        data["inventory"][0]["branch"] = "future"
        self.save_inventory(data)
        self.assert_error("unknown branch")

    def test_invalid_sha256_fails(self):
        data = self.load_inventory()
        data["inventory"][0]["sha256"] = "not-a-checksum"
        self.save_inventory(data)
        self.assert_error("invalid SHA-256")

    def test_absolute_windows_path_fails(self):
        data = self.load_inventory()
        data["inventory"][0]["relative_path"] = "C:" + "\\Users\\example\\archive.zip"
        self.save_inventory(data)
        self.assert_error("absolute or unsafe relative_path")

    def test_absolute_posix_path_fails(self):
        data = self.load_inventory()
        data["inventory"][0]["relative_path"] = "/" + "private/example/archive.zip"
        self.save_inventory(data)
        self.assert_error("absolute or unsafe relative_path")

    def test_missing_milestone_archive_fails(self):
        data = self.load_inventory()
        data["milestone_recommendations"][0]["archive_id"] = "BLU-HIST-MISSING"
        self.save_inventory(data)
        self.assert_error("milestone references missing archive")

    def test_duplicate_group_unequal_hashes_fails(self):
        data = self.load_inventory()
        group = data["duplicate_groups"][0]
        changed_id = group["archive_ids"][0]
        for record in data["inventory"]:
            if record["archive_id"] == changed_id:
                record["sha256"] = "0" * 64
        self.save_inventory(data)
        self.assert_error("duplicate group members have unequal hashes")

    def test_csv_json_count_mismatch_fails(self):
        with self.csv_path.open("r", encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
            fieldnames = rows[0].keys()
        with self.csv_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows[:-1])
        self.assert_error("CSV/JSON count mismatch")

    def test_historical_record_marked_current_authority_fails(self):
        data = self.load_inventory()
        data["source_roots"][0]["authority"] = "current_cts_authority"
        self.save_inventory(data)
        self.assert_error("historical source root marked current CTS authority")

    def test_marker_behavior_proof_fails(self):
        data = self.load_inventory()
        record = next(r for r in data["inventory"] if r["notable_capability_markers"])
        record["notable_capability_markers"][0]["worked"] = True
        self.save_inventory(data)
        self.assert_error("marker presence represented as behavior proof")

    def test_independent_snapshot_without_verifier_fails(self):
        snapshot = json.loads(self.snapshot_path.read_text(encoding="utf-8"))
        snapshot["verification_status"] = "independently_verified"
        snapshot["verified_by"] = None
        snapshot["verified_at"] = None
        self.snapshot_path.write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8")
        self.assert_error("snapshot marked independently verified without verifier metadata")


if __name__ == "__main__":
    unittest.main()
