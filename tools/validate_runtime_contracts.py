"""Validate the downstream BC-010 runtime contract extraction.

This is contract-validation tooling, not Blu runtime implementation.
"""

from __future__ import annotations

import argparse
import json
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

SOURCE_CLASSIFICATIONS = {
    "explicit declaration",
    "unresolved conflict",
    "intentionally unmodeled prose",
}


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
    return True


def validate_instance(
    value: Any,
    schema: dict[str, Any],
    schema_path: Path,
    location: str = "$",
) -> list[str]:
    """Validate the small JSON Schema subset used by the BC-010 schemas."""
    errors: list[str] = []
    if "$ref" in schema:
        ref_path = (schema_path.parent / schema["$ref"]).resolve()
        if not ref_path.is_file():
            return [f"{location}: unresolved schema reference {schema['$ref']}"]
        return validate_instance(value, load_json(ref_path), ref_path, location)
    for child_schema in schema.get("allOf", []):
        errors.extend(validate_instance(value, child_schema, schema_path, location))
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
                errors.extend(validate_instance(item, item_schema, schema_path, f"{location}[{index}]"))
    if isinstance(value, dict):
        required = schema.get("required", [])
        for key in required:
            if key not in value:
                errors.append(f"{location}: missing required property {key}")
        properties = schema.get("properties", {})
        for key, child in value.items():
            if key in properties:
                errors.extend(validate_instance(child, properties[key], schema_path, f"{location}.{key}"))
            elif schema.get("additionalProperties") is False:
                errors.append(f"{location}: additional property {key} is not allowed")
    return errors


def validate_contracts(repo_root: Path) -> list[str]:
    errors: list[str] = []
    contract_root = repo_root / "contracts" / "runtime"
    schema_root = contract_root / "schemas"

    for relative in REQUIRED_CONTRACTS:
        if not (contract_root / relative).is_file():
            errors.append(f"missing required contract: contracts/runtime/{relative}")
    for relative in REQUIRED_SCHEMAS:
        if not (schema_root / relative).is_file():
            errors.append(f"missing required schema: contracts/runtime/schemas/{relative}")
    if errors:
        return errors

    documents: dict[Path, Any] = {}
    for path in sorted(contract_root.rglob("*.json")):
        try:
            documents[path] = load_json(path)
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            errors.append(f"malformed JSON: {path.relative_to(repo_root)}: {exc}")
    if errors:
        return errors

    source_map_path = contract_root / "source_map.json"
    source_map = documents[source_map_path]
    entries = source_map.get("entries", []) if isinstance(source_map, dict) else []
    source_ids: set[str] = set()
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
        target = repo_root / entry.get("source_file", "")
        if not target.is_file():
            errors.append(f"missing source-map target: {entry_id}: {target}")
            continue
        section = entry.get("source_section")
        if not isinstance(section, str) or section not in target.read_text(encoding="utf-8"):
            errors.append(f"missing source-map section: {entry_id}: {section!r}")

    for path, document in documents.items():
        if path == source_map_path:
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
        if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            errors.append(f"unexpected schema dialect: {path.relative_to(repo_root)}")
        schema_id = schema.get("$id")
        if not isinstance(schema_id, str) or not schema_id:
            errors.append(f"schema missing $id: {path.relative_to(repo_root)}")
        elif schema_id in schema_ids:
            errors.append(f"duplicate schema $id: {schema_id}")
        schema_ids.add(schema_id)
        for ref in collect_schema_refs(schema):
            if not (path.parent / ref).is_file():
                errors.append(f"unresolved schema reference in {path.relative_to(repo_root)}: {ref}")

    return errors


def collect_schema_refs(value: Any) -> set[str]:
    refs: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "$ref" and isinstance(child, str) and "://" not in child and not child.startswith("#"):
                refs.add(child)
            refs.update(collect_schema_refs(child))
    elif isinstance(value, list):
        for child in value:
            refs.update(collect_schema_refs(child))
    return refs


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
    print("PASS: runtime contracts are structurally valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
