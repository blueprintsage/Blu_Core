"""Validate the downstream BC-010 runtime contract extraction.

This project-local, standard-library tool implements only the explicit JSON
Schema subset listed in SUPPORTED_SCHEMA_KEYWORDS. It is contract-validation
tooling, not Blu runtime implementation or a general JSON Schema validator.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


REQUIRED_CONTRACTS = (
    "README.md",
    "source_map.json",
    "component_registry.json",
    "route_registry.json",
    "parity_matrix.json",
    "unresolved_register.json",
)

REQUIRED_SCHEMAS = (
    "task_packet.schema.json",
    "scope_lock.schema.json",
    "terminal_packet.schema.json",
    "capability_report.schema.json",
    "current_turn_execution_receipt.schema.json",
)

CANONICAL_FIXTURES = (
    ("task_packet.schema.json", "valid_task_packet.json", "invalid_task_packet.json"),
    ("scope_lock.schema.json", "valid_scope_lock.json", "invalid_scope_lock.json"),
    ("terminal_packet.schema.json", "valid_terminal_packet.json", "invalid_terminal_packet.json"),
    ("capability_report.schema.json", "valid_capability_report.json", "invalid_capability_report.json"),
    (
        "current_turn_execution_receipt.schema.json",
        "valid_current_turn_execution_receipt.json",
        "invalid_current_turn_execution_receipt.json",
    ),
)

SOURCE_CLASSIFICATIONS = {
    "explicit declaration",
    "extraction inference",
    "unresolved conflict",
    "intentionally unmodeled prose",
}

SOURCE_ROLE_FILES = {
    "deployment_instruction": {
        "kernel/golden/v0.22.0/00_Instructions.md",
    },
    "kernel_runtime_capsule": {
        "kernel/golden/v0.22.0/01_Persona.md",
        "kernel/golden/v0.22.0/02_Operations_Law.md",
        "kernel/golden/v0.22.0/03_Exec.md",
        "kernel/golden/v0.22.0/04_Exec_Library.md",
        "kernel/golden/v0.22.0/05_Commands.md",
        "kernel/golden/v0.22.0/06_Programs.md",
    },
}

SUPPORTED_SCHEMA_KEYWORDS = {
    "$ref",
    "allOf",
    "type",
    "enum",
    "const",
    "minLength",
    "uniqueItems",
    "items",
    "required",
    "properties",
    "additionalProperties",
}

ANNOTATION_KEYWORDS = {"$schema", "$id", "title", "description"}
SUPPORTED_TYPES = {"null", "object", "array", "string", "boolean", "integer", "number"}
HEADING_RE = re.compile(r"^(#{1,6})[ \t]+\S")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def collect_source_refs(value: Any) -> set[str]:
    refs: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            if key in {"source_map_id", "x-source-map-id"} and isinstance(child, str):
                refs.add(child)
            elif key == "source_map_ids" and isinstance(child, list):
                refs.update(item for item in child if isinstance(item, str))
            refs.update(collect_source_refs(child))
    elif isinstance(value, list):
        for child in value:
            refs.update(collect_source_refs(child))
    return refs


def collect_schema_refs(value: Any) -> set[str]:
    refs: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "$ref" and isinstance(child, str):
                refs.add(child)
            refs.update(collect_schema_refs(child))
    elif isinstance(value, list):
        for child in value:
            refs.update(collect_schema_refs(child))
    return refs


def validate_schema_keywords(
    schema: Any,
    schema_path: Path,
    location: str = "$",
) -> list[str]:
    """Reject schema behavior outside the locally supported subset."""
    if not isinstance(schema, dict):
        return [f"{schema_path.name} {location}: schema must be an object"]

    errors: list[str] = []
    for key, child in schema.items():
        if key not in SUPPORTED_SCHEMA_KEYWORDS and key not in ANNOTATION_KEYWORDS and not key.startswith("x-"):
            errors.append(f"{schema_path.name} {location}: unsupported schema keyword {key}")
            continue

        if key == "type":
            declared = child if isinstance(child, list) else [child]
            if not declared or any(not isinstance(item, str) or item not in SUPPORTED_TYPES for item in declared):
                errors.append(f"{schema_path.name} {location}: unknown or invalid schema type {child!r}")
        elif key == "$ref":
            if not isinstance(child, str) or "://" in child or child.startswith("#"):
                errors.append(f"{schema_path.name} {location}: only local file $ref values are supported")
        elif key == "allOf":
            if not isinstance(child, list):
                errors.append(f"{schema_path.name} {location}: allOf must be an array")
            else:
                for index, item in enumerate(child):
                    errors.extend(validate_schema_keywords(item, schema_path, f"{location}.allOf[{index}]"))
        elif key == "properties":
            if not isinstance(child, dict):
                errors.append(f"{schema_path.name} {location}: properties must be an object")
            else:
                for property_name, property_schema in child.items():
                    errors.extend(
                        validate_schema_keywords(
                            property_schema,
                            schema_path,
                            f"{location}.properties[{property_name!r}]",
                        )
                    )
        elif key == "items":
            errors.extend(validate_schema_keywords(child, schema_path, f"{location}.items"))
        elif key == "additionalProperties" and not isinstance(child, bool):
            errors.append(
                f"{schema_path.name} {location}: schema-valued additionalProperties is unsupported; use a boolean"
            )

    return errors


def check_type(value: Any, expected: str) -> bool:
    if expected == "null":
        return value is None
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    raise ValueError(f"unknown schema type {expected!r}")


def validate_instance(
    value: Any,
    schema: dict[str, Any],
    schema_path: Path,
    location: str = "$",
) -> list[str]:
    """Validate an instance under the explicitly supported local subset."""
    keyword_errors = validate_schema_keywords(schema, schema_path)
    if keyword_errors:
        return keyword_errors
    return _validate_instance(value, schema, schema_path, location)


def _validate_instance(
    value: Any,
    schema: dict[str, Any],
    schema_path: Path,
    location: str,
) -> list[str]:
    errors: list[str] = []
    if "$ref" in schema:
        ref_path = (schema_path.parent / schema["$ref"]).resolve()
        if not ref_path.is_file():
            return [f"{location}: unresolved schema reference {schema['$ref']}"]
        return validate_instance(value, load_json(ref_path), ref_path, location)

    for child_schema in schema.get("allOf", []):
        errors.extend(_validate_instance(value, child_schema, schema_path, location))

    expected_type = schema.get("type")
    if expected_type is not None:
        allowed_types = expected_type if isinstance(expected_type, list) else [expected_type]
        if not any(check_type(value, item) for item in allowed_types):
            return [f"{location}: expected type {allowed_types}, got {type(value).__name__}"]

    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{location}: value is not in enum")
    if "const" in schema and value != schema["const"]:
        errors.append(f"{location}: value does not match const")
    if isinstance(value, str) and len(value) < schema.get("minLength", 0):
        errors.append(f"{location}: string is shorter than minLength")

    if isinstance(value, list):
        if schema.get("uniqueItems"):
            encoded = [json.dumps(item, sort_keys=True) for item in value]
            if len(encoded) != len(set(encoded)):
                errors.append(f"{location}: array items are not unique")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                errors.extend(_validate_instance(item, item_schema, schema_path, f"{location}[{index}]"))

    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{location}: missing required property {key}")
        properties = schema.get("properties", {})
        for key, child in value.items():
            if key in properties:
                errors.extend(_validate_instance(child, properties[key], schema_path, f"{location}.{key}"))
            elif schema.get("additionalProperties") is False:
                errors.append(f"{location}: additional property {key} is not allowed")
    return errors


def source_anchor_errors(path: Path, heading: Any, locator: Any, entry_id: str) -> list[str]:
    if not isinstance(heading, str) or not HEADING_RE.match(heading):
        return [f"source_map entry must use an exact Markdown heading: {entry_id}: {heading!r}"]

    lines = path.read_text(encoding="utf-8").splitlines()
    heading_indexes = [index for index, line in enumerate(lines) if line == heading]
    if len(heading_indexes) != 1:
        return [f"source-map heading must resolve exactly once: {entry_id}: {heading!r}"]

    start = heading_indexes[0]
    level = len(heading.split(" ", 1)[0])
    end = len(lines)
    for index in range(start + 1, len(lines)):
        match = HEADING_RE.match(lines[index])
        if match and len(match.group(1)) <= level:
            end = index
            break

    if locator is None:
        return []
    if not isinstance(locator, str) or not locator:
        return [f"invalid source locator: {entry_id}: {locator!r}"]
    matches = [line for line in lines[start + 1 : end] if line.strip() == locator]
    if len(matches) != 1:
        return [f"source locator must resolve exactly once inside heading: {entry_id}: {locator!r}"]
    return []


def declared_source_roles(source_map: dict[str, Any]) -> tuple[dict[str, set[str]], list[str]]:
    errors: list[str] = []
    declared = source_map.get("source_roles")
    if not isinstance(declared, dict):
        return {}, ["source_map source_roles must be an object"]

    roles_by_file: dict[str, set[str]] = {}
    if set(declared) != set(SOURCE_ROLE_FILES):
        errors.append(f"source roles must be exactly {sorted(SOURCE_ROLE_FILES)}")
    for role, expected_files in SOURCE_ROLE_FILES.items():
        files = declared.get(role)
        if not isinstance(files, list) or any(not isinstance(item, str) for item in files):
            errors.append(f"source role {role} must declare a list of files")
            continue
        actual_files = set(files)
        if actual_files != expected_files:
            errors.append(f"source role {role} maps to incorrect golden files")
        for source_file in files:
            roles_by_file.setdefault(source_file, set()).add(role)
    return roles_by_file, errors


def validate_contracts(repo_root: Path) -> list[str]:
    errors: list[str] = []
    contract_root = repo_root / "contracts" / "runtime"
    schema_root = contract_root / "schemas"
    fixture_root = repo_root / "tests" / "contracts" / "fixtures"

    for relative in REQUIRED_CONTRACTS:
        if not (contract_root / relative).is_file():
            errors.append(f"missing required contract: contracts/runtime/{relative}")
    for relative in REQUIRED_SCHEMAS:
        if not (schema_root / relative).is_file():
            errors.append(f"missing required schema: contracts/runtime/schemas/{relative}")
    for _, valid_fixture, invalid_fixture in CANONICAL_FIXTURES:
        for relative in (valid_fixture, invalid_fixture):
            if not (fixture_root / relative).is_file():
                errors.append(f"missing canonical fixture: tests/contracts/fixtures/{relative}")
    if errors:
        return errors

    documents: dict[Path, Any] = {}
    json_paths = sorted(contract_root.rglob("*.json")) + sorted(fixture_root.glob("*.json"))
    for path in json_paths:
        try:
            documents[path] = load_json(path)
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            errors.append(f"malformed JSON: {path.relative_to(repo_root)}: {exc}")
    if errors:
        return errors

    source_map_path = contract_root / "source_map.json"
    source_map = documents[source_map_path]
    if not isinstance(source_map, dict):
        return ["source_map must be an object"]
    roles_by_file, role_errors = declared_source_roles(source_map)
    errors.extend(role_errors)

    entries = source_map.get("entries", [])
    source_ids: set[str] = set()
    source_roles_by_id: dict[str, set[str]] = {}
    for entry in entries:
        entry_id = entry.get("id")
        if not isinstance(entry_id, str) or not entry_id:
            errors.append("source_map entry missing id")
            continue
        if entry_id in source_ids:
            errors.append(f"duplicate source_map id: {entry_id}")
        source_ids.add(entry_id)
        if entry.get("classification") not in SOURCE_CLASSIFICATIONS:
            errors.append(f"invalid source classification: {entry_id}")

        source_file = entry.get("source_file")
        entry_roles = roles_by_file.get(source_file, set()) if isinstance(source_file, str) else set()
        source_roles_by_id[entry_id] = entry_roles
        if len(entry_roles) != 1:
            errors.append(f"source-map entry must resolve to exactly one source role: {entry_id}")

        target = repo_root / source_file if isinstance(source_file, str) else repo_root
        if not target.is_file():
            errors.append(f"missing source-map target: {entry_id}: {target}")
            continue
        errors.extend(
            source_anchor_errors(
                target,
                entry.get("source_section"),
                entry.get("source_locator"),
                entry_id,
            )
        )

    for path, document in documents.items():
        if path == source_map_path or fixture_root in path.parents:
            continue
        for source_ref in sorted(collect_source_refs(document)):
            if source_ref not in source_ids:
                errors.append(f"unknown source_map reference in {path.relative_to(repo_root)}: {source_ref}")

    component_registry = documents[contract_root / "component_registry.json"]
    seen_components: set[tuple[str, str]] = set()
    for component in component_registry.get("components", []):
        key = (component.get("namespace"), component.get("id"))
        if not all(isinstance(part, str) and part for part in key):
            errors.append("component registry entry missing namespace or id")
        elif key in seen_components:
            errors.append(f"duplicate component id in namespace: {key[0]}::{key[1]}")
        seen_components.add(key)

        refs = collect_source_refs(component)
        roles = set().union(*(source_roles_by_id.get(ref, set()) for ref in refs)) if refs else set()
        if roles == {"deployment_instruction"}:
            allowed_statuses = {
                "declared_but_not_defined",
                "defined_in_golden_deployment_instruction",
            }
            if component.get("definition_status") not in allowed_statuses:
                errors.append(f"deployment-only reference classified as kernel definition: {component.get('id')}")

    route_registry = documents[contract_root / "route_registry.json"]
    owners_by_stem: dict[str, set[str]] = {}
    for route in route_registry.get("live_slash_routes", []):
        stem = route.get("stem")
        owner = route.get("owner")
        if not isinstance(stem, str) or not stem.startswith("/"):
            errors.append(f"invalid public command stem: {stem!r}")
            continue
        owners_by_stem.setdefault(stem.casefold(), set()).add(str(owner))
    for stem, owners in owners_by_stem.items():
        if len(owners) != 1:
            errors.append(f"duplicate public owners for command stem {stem}: {sorted(owners)}")
    if len(route_registry.get("live_slash_routes", [])) != len(owners_by_stem):
        errors.append("duplicate public command stem row")

    schema_ids: set[str] = set()
    for relative in REQUIRED_SCHEMAS:
        path = schema_root / relative
        schema = documents[path]
        if not isinstance(schema, dict):
            errors.append(f"schema must be an object: {path.relative_to(repo_root)}")
            continue
        errors.extend(validate_schema_keywords(schema, path))
        if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            errors.append(f"unexpected schema dialect: {path.relative_to(repo_root)}")
        schema_id = schema.get("$id")
        if not isinstance(schema_id, str) or not schema_id:
            errors.append(f"schema missing $id: {path.relative_to(repo_root)}")
        elif schema_id in schema_ids:
            errors.append(f"duplicate schema $id: {schema_id}")
        schema_ids.add(schema_id)
        for ref in collect_schema_refs(schema):
            if "://" in ref or ref.startswith("#") or not (path.parent / ref).is_file():
                errors.append(f"unresolved or unsupported schema reference in {path.relative_to(repo_root)}: {ref}")

    for schema_name, valid_name, invalid_name in CANONICAL_FIXTURES:
        schema_path = schema_root / schema_name
        schema = documents[schema_path]
        valid_errors = validate_instance(documents[fixture_root / valid_name], schema, schema_path)
        if valid_errors:
            errors.append(f"canonical positive fixture failed {valid_name}: {'; '.join(valid_errors)}")
        invalid_errors = validate_instance(documents[fixture_root / invalid_name], schema, schema_path)
        if not invalid_errors:
            errors.append(f"canonical negative fixture was accepted: {invalid_name}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root (defaults to the parent of tools/)",
    )
    args = parser.parse_args()
    errors = validate_contracts(args.root.resolve())
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("PASS: runtime contracts and canonical fixtures satisfy the supported structural subset")
    return 0


if __name__ == "__main__":
    sys.exit(main())
