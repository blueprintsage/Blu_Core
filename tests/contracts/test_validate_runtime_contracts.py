import copy
import hashlib
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


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class RuntimeContractValidationTests(unittest.TestCase):
    def setUp(self):
        self.contract_root = REPO_ROOT / "contracts" / "runtime"
        self.schema_root = self.contract_root / "schemas"
        self.fixture_root = REPO_ROOT / "tests" / "contracts" / "fixtures"

    def copy_validation_tree(self, destination: Path) -> None:
        shutil.copytree(REPO_ROOT / "contracts", destination / "contracts")
        shutil.copytree(self.fixture_root, destination / "tests" / "contracts" / "fixtures")
        shutil.copytree(
            REPO_ROOT / "kernel" / "golden" / "v0.22.0",
            destination / "kernel" / "golden" / "v0.22.0",
        )

    def test_repository_contract_set_passes(self):
        self.assertEqual([], VALIDATOR.validate_contracts(REPO_ROOT))

    def test_all_json_files_parse(self):
        json_paths = sorted(self.contract_root.rglob("*.json")) + sorted(self.fixture_root.glob("*.json"))
        self.assertGreater(len(json_paths), 0)
        for path in json_paths:
            with self.subTest(path=path.relative_to(REPO_ROOT)):
                read_json(path)

    def test_source_roles_are_exact_and_every_entry_resolves_once(self):
        source_map = read_json(self.contract_root / "source_map.json")
        roles_by_file, errors = VALIDATOR.declared_source_roles(source_map)
        self.assertEqual([], errors)
        self.assertEqual(VALIDATOR.SOURCE_ROLE_FILES, {key: set(value) for key, value in source_map["source_roles"].items()})
        for entry in source_map["entries"]:
            with self.subTest(entry=entry["id"]):
                self.assertEqual(1, len(roles_by_file.get(entry["source_file"], set())))

        precedence = next(entry for entry in source_map["entries"] if entry["id"] == "instructions.precedence")
        self.assertEqual({"deployment_instruction"}, roles_by_file[precedence["source_file"]])

    def test_host_only_reference_cannot_be_kernel_definition(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.copy_validation_tree(root)
            path = root / "contracts" / "runtime" / "component_registry.json"
            registry = read_json(path)
            instructions = next(component for component in registry["components"] if component["id"] == "00 Instructions")
            instructions["definition_status"] = "defined_in_golden"
            path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
            errors = VALIDATOR.validate_contracts(root)
            self.assertTrue(any("deployment-only reference classified as kernel definition" in error for error in errors))

    def test_repaired_non_slash_routes_and_exclusivity_constraints_exist(self):
        registry = read_json(self.contract_root / "route_registry.json")
        routes = {route["ingress_step"]: route for route in registry["non_slash_routes"] if "ingress_step" in route}
        expected = {
            "unauthenticated_clone_first_read": "SERVICE.OPSEC.001",
            "unauthenticated_opsec_first_read": "SERVICE.OPSEC.001",
            "auth_first_read": "SERVICE.AUTH.001",
        }
        for ingress_step, owner in expected.items():
            with self.subTest(ingress_step=ingress_step):
                self.assertEqual(owner, routes[ingress_step]["owner"])
                self.assertEqual("active_route_with_undefined_owner_component", routes[ingress_step]["status"])
                expected_sources = {"exec.ingress", "instructions.bootloader"}
                self.assertTrue(expected_sources.issubset(set(routes[ingress_step]["source_map_ids"])))

        rules = registry["one_owner_constraints"]["rules"]
        self.assertIn("/ID and pending auth dispatch only to SERVICE.AUTH.001.", rules)
        self.assertIn(
            "Unauthenticated OPSEC and clone/copy/recreate requests dispatch only to SERVICE.OPSEC.001.",
            rules,
        )

    def test_referenced_component_labels_and_macro_ids_remain_unimplemented(self):
        registry = read_json(self.contract_root / "component_registry.json")
        components = {component["id"]: component for component in registry["components"]}
        expected_labels = {
            "HumorLib",
            "Humor service",
            "ErrorMacros catalog",
            "Error Macros catalog",
            "error renderer",
            "Persona Engine",
        }
        for label in expected_labels:
            with self.subTest(label=label):
                self.assertEqual("referenced", components[label]["status"])
                self.assertEqual("declared_but_not_defined", components[label]["definition_status"])

        macros = {macro["id"]: macro for macro in registry["declared_macro_identifiers"]}
        self.assertEqual({"TIME_LOOKUP_BLOCKED", "GENERIC_BLOCKED"}, set(macros))
        for macro in macros.values():
            self.assertEqual("declared_identifier_only", macro["status"])
            self.assertIsNone(macro["render_text"])
            self.assertIsNone(macro["implementation_behavior"])

    def test_unsupported_schema_keyword_fails(self):
        schema_path = self.schema_root / "task_packet.schema.json"
        errors = VALIDATOR.validate_instance({}, {"type": "object", "oneOf": []}, schema_path)
        self.assertTrue(any("unsupported schema keyword oneOf" in error for error in errors))

    def test_unknown_schema_type_fails(self):
        schema_path = self.schema_root / "task_packet.schema.json"
        errors = VALIDATOR.validate_instance({}, {"type": "packet"}, schema_path)
        self.assertTrue(any("unknown or invalid schema type" in error for error in errors))

    def test_positive_and_negative_schema_fixtures(self):
        expected_negative_errors = {
            "invalid_task_packet.json": ["$: expected type ['object'], got list"],
            "invalid_scope_lock.json": ["$: missing required property active_task"],
            "invalid_terminal_packet.json": ["$.validation_result: value is not in enum"],
            "invalid_capability_report.json": ["$: expected type ['object'], got list"],
            "invalid_current_turn_execution_receipt.json": [
                f"$: missing required property {name}"
                for name in (
                    "lane_class",
                    "owner",
                    "source_or_contract",
                    "executed_action",
                    "validation_result",
                    "terminal_state",
                    "printable_output",
                    "artifact_output",
                    "failure_reason",
                    "scope_lock",
                    "scope_validation",
                )
            ],
        }
        for schema_name, valid_name, invalid_name in VALIDATOR.CANONICAL_FIXTURES:
            with self.subTest(schema=schema_name, fixture=valid_name):
                schema_path = self.schema_root / schema_name
                schema = read_json(schema_path)
                self.assertEqual([], VALIDATOR.validate_instance(read_json(self.fixture_root / valid_name), schema, schema_path))
            with self.subTest(schema=schema_name, fixture=invalid_name):
                schema_path = self.schema_root / schema_name
                schema = read_json(schema_path)
                self.assertEqual(
                    expected_negative_errors[invalid_name],
                    VALIDATOR.validate_instance(read_json(self.fixture_root / invalid_name), schema, schema_path),
                )

    def test_additional_properties_false_rejects_synthetic_extra_property(self):
        schema_path = self.schema_root / "task_packet.schema.json"
        schema = {
            "type": "object",
            "properties": {"known": {"type": "string"}},
            "additionalProperties": False,
        }
        self.assertEqual(
            ["$: additional property extra is not allowed"],
            VALIDATOR.validate_instance({"known": "value", "extra": True}, schema, schema_path),
        )

    def test_opsec_routes_preserve_undeclared_lane_and_cross_role_inference(self):
        route_registry = read_json(self.contract_root / "route_registry.json")
        source_map = read_json(self.contract_root / "source_map.json")
        routes = {route["id"]: route for route in route_registry["non_slash_routes"]}
        opsec_ids = {
            "route.unauthenticated_clone_first_read",
            "route.unauthenticated_opsec_first_read",
        }
        for route_id in opsec_ids:
            with self.subTest(route=route_id):
                route = routes[route_id]
                self.assertIsNone(route["lane_class"])
                self.assertEqual("undeclared_in_golden_source", route["lane_class_status"])
                self.assertEqual("extraction_inference", route["provenance_classification"])
                self.assertEqual("UR-028", route["unresolved_register_id"])
                self.assertIn("route.opsec_owner_join", route["source_map_ids"])

        entries = {entry["id"]: entry for entry in source_map["entries"]}
        join = entries["route.opsec_owner_join"]
        self.assertEqual("extraction inference", join["classification"])
        self.assertEqual({"exec.ingress", "instructions.bootloader"}, set(join["joined_source_map_ids"]))
        roles_by_file, errors = VALIDATOR.declared_source_roles(source_map)
        self.assertEqual([], errors)
        joined_roles = {
            next(iter(roles_by_file[entries[source_id]["source_file"]]))
            for source_id in join["joined_source_map_ids"]
        }
        self.assertEqual({"kernel_runtime_capsule", "deployment_instruction"}, joined_roles)

    def test_lane_class_closure_accepts_declared_auth_and_unresolved_workflow(self):
        route_registry = read_json(self.contract_root / "route_registry.json")
        unresolved = read_json(self.contract_root / "unresolved_register.json")
        source_map = read_json(self.contract_root / "source_map.json")
        source_ids = {entry["id"] for entry in source_map["entries"]}
        self.assertEqual([], VALIDATOR.route_lane_class_errors(route_registry, unresolved, source_ids))
        self.assertEqual(
            "auth",
            next(route for route in route_registry["non_slash_routes"] if route["id"] == "route.auth_first_read")[
                "lane_class"
            ],
        )
        self.assertEqual(
            "workflow",
            next(route for route in route_registry["live_slash_routes"] if route["stem"] == "/memory")["lane_class"],
        )

    def test_lane_class_closure_rejects_opsec_and_arbitrary_inventions(self):
        route_registry = read_json(self.contract_root / "route_registry.json")
        unresolved = read_json(self.contract_root / "unresolved_register.json")
        source_map = read_json(self.contract_root / "source_map.json")
        source_ids = {entry["id"] for entry in source_map["entries"]}
        for invented in ("opsec", "invented_lane"):
            with self.subTest(lane_class=invented):
                changed = copy.deepcopy(route_registry)
                route = next(
                    item
                    for item in changed["non_slash_routes"]
                    if item["id"] == "route.unauthenticated_clone_first_read"
                )
                route["lane_class"] = invented
                route.pop("lane_class_status", None)
                errors = VALIDATOR.route_lane_class_errors(changed, unresolved, source_ids)
                self.assertIn(
                    f"undeclared route lane_class '{invented}': route.unauthenticated_clone_first_read",
                    errors,
                )

    def test_null_lane_class_without_unresolved_status_is_rejected(self):
        route_registry = read_json(self.contract_root / "route_registry.json")
        unresolved = read_json(self.contract_root / "unresolved_register.json")
        source_map = read_json(self.contract_root / "source_map.json")
        source_ids = {entry["id"] for entry in source_map["entries"]}
        changed = copy.deepcopy(route_registry)
        route = next(
            item
            for item in changed["non_slash_routes"]
            if item["id"] == "route.unauthenticated_clone_first_read"
        )
        route.pop("lane_class_status")
        errors = VALIDATOR.route_lane_class_errors(changed, unresolved, source_ids)
        self.assertIn(
            "null lane_class requires unresolved status: route.unauthenticated_clone_first_read",
            errors,
        )

    def test_dependency_ids_are_separated_from_dependency_prose(self):
        registry = read_json(self.contract_root / "component_registry.json")
        components = {component["id"]: component for component in registry["components"]}
        self.assertEqual(["EXECLIB.STATETREE.001"], components["EXECLIB.MMU.001"]["dependencies"])
        self.assertEqual(["EXECLIB.DATELIB.001"], components["EXECLIB.READLANE.SOURCELIB.001"]["dependencies"])
        self.assertEqual([], components["RuntimeGate.Egress"]["dependencies"])
        for component_id in (
            "EXECLIB.MMU.001",
            "EXECLIB.READLANE.SOURCELIB.001",
            "RuntimeGate.Egress",
        ):
            self.assertTrue(components[component_id]["dependency_prose"])

    def test_required_contract_missing_fails(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.copy_validation_tree(root)
            (root / "contracts" / "runtime" / "route_registry.json").unlink()
            errors = VALIDATOR.validate_contracts(root)
            self.assertTrue(any("missing required contract" in error for error in errors))

    def test_malformed_json_fails(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.copy_validation_tree(root)
            (root / "contracts" / "runtime" / "route_registry.json").write_text("{", encoding="utf-8")
            errors = VALIDATOR.validate_contracts(root)
            self.assertTrue(any("malformed JSON" in error for error in errors))

    def test_source_sections_are_exact_heading_anchors(self):
        source_map = read_json(self.contract_root / "source_map.json")
        entries = {entry["id"]: entry for entry in source_map["entries"]}
        self.assertEqual("### Active Component Registry Stabilization", entries["execlib.active_registry_stabilization"]["source_section"])
        self.assertEqual("### Active Component Registry", entries["execlib.active_registry"]["source_section"])

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.copy_validation_tree(root)
            path = root / "contracts" / "runtime" / "source_map.json"
            copied = read_json(path)
            entry = next(item for item in copied["entries"] if item["id"] == "execlib.active_registry")
            entry["source_section"] = "### Active Component Reg"
            path.write_text(json.dumps(copied, indent=2) + "\n", encoding="utf-8")
            errors = VALIDATOR.validate_contracts(root)
            self.assertTrue(any("source-map heading must resolve exactly once" in error for error in errors))

    def test_pass_is_not_a_source_declared_slash_stem(self):
        registry = read_json(self.contract_root / "route_registry.json")
        self.assertNotIn("/PASS", registry["unavailable_command_surfaces"]["values"])
        pass_feature = next(item for item in registry["non_live_feature_declarations"] if item["label"] == "PASS command")
        self.assertFalse(pass_feature["literal_slash_stem_declared"])
        self.assertEqual("commands.pass_removal", pass_feature["source_map_id"])

    def test_statetree_conflict_and_extended_provenance_are_preserved(self):
        registry = read_json(self.contract_root / "component_registry.json")
        state_tree = next(component for component in registry["components"] if component["id"] == "EXECLIB.STATETREE.001")
        self.assertEqual("unresolved_conflict", state_tree["status"])
        self.assertEqual(["ALPHA", "ACTIVE"], state_tree["declared_statuses"])
        self.assertTrue(
            {"execlib.active_registry_stabilization", "execlib.active_registry", "commands.help"}.issubset(
                state_tree["source_map_ids"]
            )
        )

    def test_golden_checksum_manifest_still_matches_all_eight_entries(self):
        golden_root = REPO_ROOT / "kernel" / "golden" / "v0.22.0"
        manifest_lines = (golden_root / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
        self.assertEqual(8, len(manifest_lines))
        for line in manifest_lines:
            expected, relative = line.split(None, 1)
            path = golden_root / relative.strip()
            with self.subTest(path=relative.strip()):
                self.assertEqual(expected, hashlib.sha256(path.read_bytes()).hexdigest())


if __name__ == "__main__":
    unittest.main()
