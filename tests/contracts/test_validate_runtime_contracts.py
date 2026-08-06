import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
VALIDATOR_PATH = REPO_ROOT / "tools" / "validate_runtime_contracts.py"
SPEC = importlib.util.spec_from_file_location("validate_runtime_contracts", VALIDATOR_PATH)
VALIDATOR = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(VALIDATOR)


class RuntimeContractValidationTests(unittest.TestCase):
    def test_repository_contract_set_passes(self):
        self.assertEqual([], VALIDATOR.validate_contracts(REPO_ROOT))

    def test_required_contract_missing_fails(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            shutil.copytree(REPO_ROOT / "contracts", root / "contracts")
            (root / "contracts" / "runtime" / "route_registry.json").unlink()
            errors = VALIDATOR.validate_contracts(root)
            self.assertTrue(any("missing required contract" in error for error in errors))

    def test_malformed_json_fails(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            shutil.copytree(REPO_ROOT / "contracts", root / "contracts")
            (root / "contracts" / "runtime" / "route_registry.json").write_text("{", encoding="utf-8")
            errors = VALIDATOR.validate_contracts(root)
            self.assertTrue(any("malformed JSON" in error for error in errors))

    def test_schema_fixtures(self):
        schema_root = REPO_ROOT / "contracts" / "runtime" / "schemas"
        fixture_root = REPO_ROOT / "tests" / "contracts" / "fixtures"
        pairs = {
            "task_packet.schema.json": "valid_task_packet.json",
            "scope_lock.schema.json": "valid_scope_lock.json",
            "terminal_packet.schema.json": "valid_terminal_packet.json",
            "capability_report.schema.json": "valid_capability_report.json",
            "current_turn_execution_receipt.schema.json": "valid_current_turn_execution_receipt.json",
        }
        for schema_name, fixture_name in pairs.items():
            with self.subTest(schema=schema_name):
                schema_path = schema_root / schema_name
                schema = json.loads(schema_path.read_text(encoding="utf-8"))
                fixture = json.loads((fixture_root / fixture_name).read_text(encoding="utf-8"))
                self.assertEqual([], VALIDATOR.validate_instance(fixture, schema, schema_path))


if __name__ == "__main__":
    unittest.main()
