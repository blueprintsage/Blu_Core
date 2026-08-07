"""Validate the BC-015 viability audit without executing or simulating Blu."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


CLASSIFICATIONS = {
    "live_and_stable",
    "live_but_nondeterministic_or_host_dependent",
    "declared_but_not_observably_functioning",
    "conflicting_or_underspecified",
    "explicitly_deferred_or_removed",
    "new_successor_runtime_capability",
}
CONFIDENCE = {"high", "medium", "low", "unresolved"}
DISPOSITIONS = {
    "implement_deterministically",
    "keep_model_facing",
    "recover_as_lightweight_profile",
    "keep_contract_and_defer",
    "remove",
    "hybrid_split",
    "architecture_decision_required",
}
EVIDENCE_CLASSES = {
    "golden_declaration",
    "contract_extraction",
    "project_decision",
    "owner_observation",
    "current_live_probe",
    "host_capability_observation",
    "historical_baseline",
    "automated_static_check",
    "extraction_inference",
    "unavailable_evidence",
}
REPEATABLE_EVIDENCE = {"current_live_probe", "host_capability_observation"}
RESPONSIBILITY_KEYS = {"python", "model", "profile", "host", "deferred"}
REQUIRED_FILES = {
    "README.md",
    "evidence_register.json",
    "viability_matrix.json",
    "probe_catalog.md",
    "audit_report.md",
}
EVIDENCE_FIELDS = {
    "id",
    "evidence_class",
    "source_role",
    "source_identity",
    "source_location",
    "source_heading_or_locator",
    "summary",
    "supports",
    "limitations",
    "observed_by",
    "observed_date",
}
CAPABILITY_FIELDS = {
    "id",
    "name",
    "kind",
    "current_source_ids",
    "contract_ids",
    "covered_component_ids",
    "covered_route_ids",
    "covered_parity_ids",
    "covered_unresolved_ids",
    "current_viability_class",
    "classification_confidence",
    "evidence_ids",
    "observable_behavior",
    "known_failure_modes",
    "host_dependencies",
    "current_owner",
    "current_definition_status",
    "legacy_behavior_evidence",
    "successor_delta",
    "proposed_disposition",
    "responsibility_split",
    "required_live_probes",
    "required_regression_tests",
    "open_decisions",
    "notes",
}


def load_json(path: Path, errors: list[str]) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{path}: {exc}")
        return {}


def duplicates(values: list[str]) -> set[str]:
    seen: set[str] = set()
    return {value for value in values if value in seen or seen.add(value)}  # type: ignore[func-returns-value]


def route_inventory_ids(route: dict[str, Any]) -> list[str]:
    values: list[str] = []
    values.extend(
        f"restraint:{item['order']}:{item['owner']}"
        for item in route["mandatory_restraint_order"]["steps"]
    )
    values.extend(f"ingress:{item}" for item in route["runtimegate_ingress_order"]["steps"])
    lanes = route["declared_lane_classes"]
    values.extend(f"lane:{item}" for item in lanes["values"])
    values.append(f"lane:{lanes['route_table_only_value']}")
    values.extend(f"slash:{item['stem']}" for item in route["live_slash_routes"])
    values.extend(f"command:active:{item}" for item in route["active_command_forms"]["values"])
    values.extend(f"command:deferred:{item}" for item in route["deferred_command_forms"]["values"])
    values.extend(
        f"command:unavailable:{item}"
        for item in route["unavailable_command_surfaces"]["values"]
    )
    values.extend(
        f"feature:{item['label']}" for item in route["non_live_feature_declarations"]
    )
    values.extend(item["id"] for item in route["non_slash_routes"])
    values.append("hook:artifact_context")
    values.append("behavior:unknown_slash")
    values.extend(
        f"owner_rule:{index}"
        for index, _ in enumerate(route["one_owner_constraints"]["rules"], start=1)
    )
    return values


def check_exact_coverage(
    label: str, expected: list[str], covered: list[str], errors: list[str]
) -> None:
    expected_set = set(expected)
    covered_set = set(covered)
    for item in sorted(expected_set - covered_set):
        errors.append(f"uncovered {label} entry: {item}")
    for item in sorted(covered_set - expected_set):
        errors.append(f"unknown covered {label} entry: {item}")


def validate_audit(root: Path) -> list[str]:
    errors: list[str] = []
    audit_root = root / "docs" / "domains" / "runtime" / "viability"
    contract_root = root / "contracts" / "runtime"

    for name in sorted(REQUIRED_FILES):
        if not (audit_root / name).is_file():
            errors.append(f"missing required audit file: {name}")

    evidence_doc = load_json(audit_root / "evidence_register.json", errors)
    matrix = load_json(audit_root / "viability_matrix.json", errors)
    components_doc = load_json(contract_root / "component_registry.json", errors)
    route_doc = load_json(contract_root / "route_registry.json", errors)
    parity_doc = load_json(contract_root / "parity_matrix.json", errors)
    unresolved_doc = load_json(contract_root / "unresolved_register.json", errors)
    if errors:
        return errors

    evidence = evidence_doc.get("entries", [])
    capabilities = matrix.get("capabilities", [])
    evidence_ids = [item.get("id") for item in evidence]
    capability_ids = [item.get("id") for item in capabilities]

    for value in sorted(duplicates(evidence_ids)):
        errors.append(f"duplicate evidence id: {value}")
    for value in sorted(duplicates(capability_ids)):
        errors.append(f"duplicate capability id: {value}")

    capability_id_set = set(capability_ids)
    evidence_by_id = {item.get("id"): item for item in evidence}

    for item in evidence:
        missing = EVIDENCE_FIELDS - set(item)
        if missing:
            errors.append(
                f"evidence {item.get('id')}: missing fields {sorted(missing)}"
            )
        evidence_class = item.get("evidence_class")
        if evidence_class not in EVIDENCE_CLASSES:
            errors.append(
                f"evidence {item.get('id')}: unknown evidence_class {evidence_class!r}"
            )
        for supported in item.get("supports", []):
            if supported not in capability_id_set:
                errors.append(
                    f"evidence {item.get('id')}: unknown supported capability {supported}"
                )
        if evidence_class == "golden_declaration":
            if item.get("source_role") not in {
                "deployment_instruction",
                "kernel_runtime_capsule",
            }:
                errors.append(
                    f"evidence {item.get('id')}: successor/project evidence projected "
                    "backward as a golden declaration"
                )
            location = item.get("source_location")
            if not isinstance(location, str) or not location.startswith(
                "kernel/golden/v0.22.0/"
            ):
                errors.append(
                    f"evidence {item.get('id')}: golden declaration lacks golden source location"
                )
        if evidence_class == "historical_baseline":
            for field in ("archive_filename", "archive_sha256", "member_path"):
                if not item.get(field):
                    errors.append(
                        f"evidence {item.get('id')}: historical evidence missing {field}"
                    )

    probe_text = (audit_root / "probe_catalog.md").read_text(encoding="utf-8")

    for item in capabilities:
        item_id = item.get("id")
        missing = CAPABILITY_FIELDS - set(item)
        if missing:
            errors.append(f"capability {item_id}: missing fields {sorted(missing)}")
        classification = item.get("current_viability_class")
        if classification not in CLASSIFICATIONS:
            errors.append(f"capability {item_id}: unknown classification {classification!r}")
        confidence = item.get("classification_confidence")
        if confidence not in CONFIDENCE:
            errors.append(f"capability {item_id}: unknown confidence {confidence!r}")
        disposition = item.get("proposed_disposition")
        if disposition not in DISPOSITIONS:
            errors.append(f"capability {item_id}: invalid proposed disposition {disposition!r}")
        split = item.get("responsibility_split")
        if not isinstance(split, dict) or set(split) != RESPONSIBILITY_KEYS:
            errors.append(
                f"capability {item_id}: responsibility_split must contain "
                f"{sorted(RESPONSIBILITY_KEYS)}"
            )
        referenced_evidence = item.get("evidence_ids", [])
        missing_evidence = [
            evidence_id
            for evidence_id in referenced_evidence
            if evidence_id not in evidence_by_id
        ]
        for evidence_id in missing_evidence:
            errors.append(f"capability {item_id}: missing evidence reference {evidence_id}")
        for evidence_id in referenced_evidence:
            evidence_item = evidence_by_id.get(evidence_id)
            if evidence_item is not None and item_id not in evidence_item.get("supports", []):
                errors.append(
                    f"capability {item_id}: evidence {evidence_id} does not list it in supports"
                )
        if classification == "live_and_stable" and not any(
            evidence_by_id.get(evidence_id, {}).get("evidence_class")
            in REPEATABLE_EVIDENCE
            for evidence_id in referenced_evidence
        ):
            errors.append(
                f"capability {item_id}: live_and_stable lacks repeatable observable evidence"
            )
        if classification == "new_successor_runtime_capability" and (
            item.get("covered_component_ids") or item.get("covered_route_ids")
        ):
            errors.append(
                f"capability {item_id}: successor-only capability covers current registry entries"
            )
        for probe_id in item.get("required_live_probes", []):
            if f"## {probe_id} " not in probe_text:
                errors.append(f"capability {item_id}: missing probe catalog entry {probe_id}")

    expected_components = [item["id"] for item in components_doc["components"]]
    expected_routes = route_inventory_ids(route_doc)
    expected_parity = [item["id"] for item in parity_doc["requirements"]]
    expected_unresolved = [item["id"] for item in unresolved_doc["items"]]
    check_exact_coverage(
        "component",
        expected_components,
        [value for item in capabilities for value in item["covered_component_ids"]],
        errors,
    )
    check_exact_coverage(
        "route",
        expected_routes,
        [value for item in capabilities for value in item["covered_route_ids"]],
        errors,
    )
    check_exact_coverage(
        "parity",
        expected_parity,
        [value for item in capabilities for value in item["covered_parity_ids"]],
        errors,
    )
    check_exact_coverage(
        "unresolved",
        expected_unresolved,
        [value for item in capabilities for value in item["covered_unresolved_ids"]],
        errors,
    )
    if matrix.get("route_inventory_ids") != expected_routes:
        errors.append("viability_matrix route_inventory_ids does not match route registry")
    expected_counts = {
        "components": len(expected_components),
        "routes": len(expected_routes),
        "parity_requirements": len(expected_parity),
        "unresolved_items": len(expected_unresolved),
    }
    if matrix.get("inventory_counts") != expected_counts:
        errors.append(
            f"inventory_counts mismatch: expected {expected_counts}, "
            f"got {matrix.get('inventory_counts')}"
        )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = validate_audit(args.root.resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("PASS: BC-015 viability audit structure, evidence links, and inventory coverage validate")
    return 0


if __name__ == "__main__":
    sys.exit(main())
