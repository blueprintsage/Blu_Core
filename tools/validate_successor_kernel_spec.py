#!/usr/bin/env python3
"""Validate BC-018 successor-kernel specification integrity and guardrails."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


SPEC_DIR = Path("contracts/successor")
ASSIGNMENT_DIR = Path("docs/domains/runtime/assignments/BC-018")
REQUIRED = {
    SPEC_DIR / "README.md",
    SPEC_DIR / "component_registry.json",
    SPEC_DIR / "behavior_placement.json",
    SPEC_DIR / "interface_registry.json",
    SPEC_DIR / "packet_registry.json",
    SPEC_DIR / "error_model.json",
    SPEC_DIR / "unresolved_register.json",
    SPEC_DIR / "traceability.json",
    Path("docs/architecture/successor_kernel.md"),
    Path("docs/architecture/successor_component_graph.md"),
    Path("docs/architecture/successor_boundaries.md"),
    Path("docs/architecture/successor_migration_sequence.md"),
    ASSIGNMENT_DIR / "assignment.md",
    ASSIGNMENT_DIR / "handoff.md",
    ASSIGNMENT_DIR / "validation.md",
    ASSIGNMENT_DIR / "review.md",
}
JSON_FILES = {path for path in REQUIRED if path.suffix == ".json"}
ALLOWED_DOMAINS = {
    "model_facing", "deterministic_core", "host_service", "host_adapter",
    "continuity_provider", "hybrid", "deferred", "reject",
}
ALLOWED_COMPONENT_STATUS = {"approved_boundary", "candidate", "deferred", "rejected"}
ALLOWED_LIFETIMES = {"none", "turn", "session", "host_session", "durable_external"}
REQUIRED_BEHAVIORS = {
    "ordinary conversation", "Persona", "Operations truth law", "command detection",
    "route selection", "owner locking", "ScopeLock", "task packets",
    "terminal packets", "capability reports", "execution receipts", "Auth", "OPSEC",
    "current time", "time arithmetic", "reminders", "future scheduling", "Mood", "MMU",
    "continuity", "durable persistence", "Teaching", "classroom behavior", "School Engine",
    "source lookup", "source grounding", "Faithfulness", "web/tool capability",
    "artifact validation", "egress", "diagnostics", "Exec behaviors", "legacy PASS",
    "modern PASS/SkillForge integration boundary", "Chat adapter boundary",
    "Codex adapter boundary", "Local Mirror boundary",
}
FORBIDDEN_COMPONENT_TERMS = {"megaexec", "mega exec", "exec 2", "school engine", "legacy pass"}
PROHIBITED_RUNTIME_ROOTS = {
    Path("src/successor"), Path("src/blu_core/successor"), Path("blu_core/successor"),
    Path("runtime/successor"), Path("packages/successor_kernel"),
}


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _duplicates(values: list[str]) -> set[str]:
    return {item for item in values if values.count(item) > 1}


def _validate_unique(errors: list[str], records: list[dict[str, Any]], key: str, label: str) -> None:
    values = [item.get(key) for item in records]
    if any(not isinstance(item, str) or not item for item in values):
        errors.append(f"{label} contains missing or invalid {key}")
        return
    for item in sorted(_duplicates(values)):
        errors.append(f"duplicate {label} ID: {item}")


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    missing = [str(path) for path in sorted(REQUIRED) if not (root / path).is_file()]
    if missing:
        errors.extend(f"missing required file: {path}" for path in missing)
        return errors

    data: dict[str, Any] = {}
    for path in sorted(JSON_FILES):
        try:
            data[path.name] = _load(root / path)
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            errors.append(f"invalid JSON: {path}: {exc}")
    if errors:
        return errors

    components = data["component_registry.json"].get("components", [])
    behaviors = data["behavior_placement.json"].get("behaviors", [])
    interfaces = data["interface_registry.json"].get("interfaces", [])
    packets = data["packet_registry.json"].get("packets", [])
    statuses = data["error_model.json"].get("statuses", [])
    unresolved = data["unresolved_register.json"].get("items", [])
    evidence_catalog = data["traceability.json"].get("evidence_catalog", [])
    requirements = data["traceability.json"].get("requirements", [])
    packet_contract = data["packet_registry.json"]
    interface_contract = data["interface_registry.json"]

    for records, key, label in (
        (components, "component_id", "component"),
        (behaviors, "behavior_id", "behavior"),
        (interfaces, "interface_id", "interface"),
        (packets, "packet_id", "packet"),
        (statuses, "status", "status"),
        (unresolved, "id", "unresolved item"),
        (evidence_catalog, "evidence_ref", "evidence"),
        (requirements, "successor_requirement_id", "traceability requirement"),
    ):
        _validate_unique(errors, records, key, label)

    evidence_refs = {item.get("evidence_ref") for item in evidence_catalog}
    for item in evidence_catalog:
        source = root / str(item.get("source_path", ""))
        locator = item.get("source_locator")
        if not source.is_file():
            errors.append(f"evidence source does not exist: {item.get('evidence_ref')}")
        elif not isinstance(locator, str) or locator not in source.read_text(encoding="utf-8"):
            errors.append(f"evidence locator does not resolve: {item.get('evidence_ref')}")

    for component in components:
        component_id = component.get("component_id", "<unknown>")
        owns = component.get("owns")
        does_not_own = component.get("does_not_own")
        if not isinstance(owns, list) or not owns:
            errors.append(f"component lacks owns: {component_id}")
        if not isinstance(does_not_own, list) or not does_not_own:
            errors.append(f"component lacks does_not_own: {component_id}")
        if isinstance(owns, list) and isinstance(does_not_own, list) and set(owns) & set(does_not_own):
            errors.append(f"component owns and disowns same responsibility: {component_id}")
        lifetimes = component.get("state_lifetime")
        if not isinstance(lifetimes, list) or not lifetimes or set(lifetimes) - ALLOWED_LIFETIMES:
            errors.append(f"stateful component lacks valid lifetime: {component_id}")
        if "host_dependencies" not in component or not isinstance(component.get("host_dependencies"), list):
            errors.append(f"component host capability dependencies are not explicit: {component_id}")
        if component.get("status") not in ALLOWED_COMPONENT_STATUS:
            errors.append(f"component has implementation-like or invalid status: {component_id}")
        unknown = set(component.get("evidence_refs", [])) - evidence_refs
        for item in sorted(unknown):
            errors.append(f"component evidence ref is unknown: {component_id} -> {item}")
        if "durable_external" in (lifetimes or []) and component.get("domain") != "continuity_provider":
            if "continuity_provider_boundary" not in component.get("dependencies", []):
                errors.append(f"durable component lacks continuity-provider dependency: {component_id}")

    deterministic_owners: dict[str, str] = {}
    for component in components:
        if component.get("domain") != "deterministic_core":
            continue
        for responsibility in component.get("owns", []):
            prior = deterministic_owners.get(responsibility)
            if prior:
                errors.append(
                    f"duplicate exclusive deterministic owner: {responsibility}: {prior}, {component.get('component_id')}"
                )
            deterministic_owners[responsibility] = component.get("component_id")

    by_component = {item.get("component_id"): item for item in components}
    by_packet = {item.get("packet_id"): item for item in packets}
    security = by_component.get("security_restraint", {})
    authorization = by_component.get("authorization_evaluator", {})
    controller = by_component.get("turn_controller", {})
    egress = by_component.get("validation_egress", {})
    adapter = by_component.get("host_adapter_boundary", {})

    turn_request = by_packet.get("TurnRequest", {})
    if turn_request.get("producer") != "turn_controller":
        errors.append("TurnRequest producer is not solely turn_controller")
    if "TurnRequest" not in controller.get("outputs", []):
        errors.append("turn_controller does not produce TurnRequest")
    if "ingress_normalization" not in controller.get("owns", []):
        errors.append("turn_controller does not solely own ingress/task normalization")
    if "TurnRequest" in adapter.get("outputs", []) or "ingress_normalization" in adapter.get("owns", []):
        errors.append("host_adapter_boundary improperly constructs TurnRequest")

    ingress = packet_contract.get("ingress_ownership", {})
    interface_ingress = interface_contract.get("ingress_contract", {})
    expected_precondition = "SecurityDecision status=PASS"
    if ingress.get("host_adapter_boundary", {}).get("output") != "raw_host_input":
        errors.append("host adapter ingress output is not raw_host_input")
    if ingress.get("host_adapter_boundary", {}).get("does_not_produce") != "TurnRequest":
        errors.append("host adapter ingress contract does not exclude TurnRequest construction")
    if ingress.get("security_restraint", {}).get("input") != "raw_host_input":
        errors.append("security restraint does not consume raw_host_input before routing")
    if ingress.get("turn_controller", {}).get("output") != "TurnRequest" or ingress.get("turn_controller", {}).get("sole_turn_request_producer") is not True:
        errors.append("TurnRequest ingress ownership is not exclusive to turn_controller")
    if ingress.get("ordinary_routing_precondition") != expected_precondition:
        errors.append("ordinary host routing may begin before SecurityDecision PASS")
    if interface_ingress.get("turn_request_producer") != "turn_controller":
        errors.append("interface contract assigns TurnRequest to a non-controller producer")
    if interface_ingress.get("ordinary_routing_precondition") != expected_precondition:
        errors.append("interface contract permits ordinary routing before SecurityDecision PASS")
    control_invariants = by_packet.get("ControlDecision", {}).get("invariants", [])
    if "SecurityDecision PASS exists" not in control_invariants:
        errors.append("ControlDecision does not require SecurityDecision PASS")

    auth_loop = packet_contract.get("pre_ingress_authorization_loop", {})
    interface_auth = interface_contract.get("pre_ingress_authorization_contract", {})
    if not auth_loop or auth_loop.get("reentry_target") != "security_restraint" or auth_loop.get("ordinary_routing_bypassed") is not True or auth_loop.get("pass_required_for_turn_controller") is not True:
        errors.append("OPSEC authorization-required path lacks Auth/re-entry mechanism")
    if auth_loop.get("authorization_owner") != "authorization_evaluator" or auth_loop.get("security_owner") != "security_restraint" or auth_loop.get("authorization_owner") == auth_loop.get("security_owner"):
        errors.append("Auth is merged into OPSEC instead of remaining a separate evaluator")
    if auth_loop.get("safe_ask_egress_owner") != "validation_egress" or auth_loop.get("evidence_channel") != "host_adapter_boundary":
        errors.append("pre-ingress authorization ASK lacks bounded egress/evidence owners")
    if interface_auth.get("owners_separate") is not True or "security_restraint" not in str(interface_auth.get("reentry", "")) or "SecurityDecision PASS" not in str(interface_auth.get("route_gate", "")):
        errors.append("interface contract lacks separate Auth-to-OPSEC re-entry")
    if "authorization_evaluator" not in security.get("dependencies", []):
        errors.append("security restraint lacks authorization evaluator dependency")
    if "host_adapter_boundary" not in authorization.get("dependencies", []):
        errors.append("authorization evaluator lacks explicit evidence channel")
    if "security_restraint" not in egress.get("dependencies", []):
        errors.append("validation egress lacks pre-ingress SecurityDecision dependency")
    if "authorization_evaluator" in controller.get("dependencies", []) or "AuthorizationResult_when_required" in controller.get("inputs", []):
        errors.append("pre-ingress Auth is incorrectly routed through turn_controller")

    component_text = " ".join(
        f"{item.get('component_id', '')} {item.get('name', '')}".lower() for item in components
    )
    for term in sorted(FORBIDDEN_COMPONENT_TERMS):
        if term in component_text:
            errors.append(f"forbidden historical successor component present: {term}")

    by_behavior = {item.get("behavior"): item for item in behaviors}
    missing_behaviors = sorted(REQUIRED_BEHAVIORS - set(by_behavior))
    errors.extend(f"required behavior placement missing: {item}" for item in missing_behaviors)
    for behavior in behaviors:
        behavior_id = behavior.get("behavior_id", "<unknown>")
        if behavior.get("primary_domain") not in ALLOWED_DOMAINS:
            errors.append(f"behavior has invalid primary domain: {behavior_id}")
        if behavior.get("primary_domain") == "hybrid" and not behavior.get("secondary_domain_if_hybrid"):
            errors.append(f"hybrid behavior lacks explicit split: {behavior_id}")
        unknown = (set(behavior.get("source_evidence", [])) |
                   set(behavior.get("archaeology_evidence", []))) - evidence_refs
        for item in sorted(unknown):
            errors.append(f"behavior evidence ref is unknown: {behavior_id} -> {item}")

    if by_behavior.get("legacy PASS", {}).get("primary_domain") != "reject":
        errors.append("legacy PASS is not rejected")
    if by_behavior.get("School Engine", {}).get("primary_domain") != "reject":
        errors.append("School Engine is restored instead of rejected")
    skill = by_behavior.get("modern PASS/SkillForge integration boundary", {})
    if skill.get("primary_domain") in {"deterministic_core", "continuity_provider"}:
        errors.append("modern PASS/SkillForge is embedded in kernel ownership")
    durable = by_behavior.get("durable persistence", {})
    if "continuity" not in str(durable.get("continuity_dependency", "")).lower():
        errors.append("durable-persistence claim lacks continuity-provider dependency")
    for name in ("reminders", "future scheduling"):
        if "scheduling_provider" not in str(by_behavior.get(name, {}).get("host_dependency", "")):
            errors.append(f"future scheduling claim lacks scheduling-provider dependency: {name}")

    if security.get("boundary_position") != "pre_ingress":
        errors.append("OPSEC is moved behind turn_controller instead of remaining pre-ingress")
    model = next((item for item in components if item.get("component_id") == "model_execution_boundary"), {})
    if any("route" in item.lower() for item in model.get("owns", [])):
        errors.append("Persona/model boundary is assigned route ownership")

    for interface in interfaces:
        if interface.get("host_specific") is not False or interface.get("provider_binding") is not None:
            errors.append(f"host-specific implementation appears in generic interface: {interface.get('interface_id')}")
    adapter = next((item for item in components if item.get("component_id") == "host_adapter_boundary"), {})
    if adapter.get("host_specific") is not False or adapter.get("provider_binding") is not None:
        errors.append("Chat/Codex-specific adapter implementation appears in component registry")
    continuity = next((item for item in components if item.get("component_id") == "continuity_provider_boundary"), {})
    if continuity.get("provider_binding") is not None:
        errors.append("Local Mirror implementation appears in generic continuity boundary")

    for requirement in requirements:
        unknown = set(requirement.get("evidence_ref", [])) - evidence_refs
        for item in sorted(unknown):
            errors.append(f"traceability evidence ref is unknown: {requirement.get('successor_requirement_id')} -> {item}")

    expected_statuses = {"PASS", "BLOCK", "ASK", "UNAVAILABLE", "INVALID", "ERROR"}
    if {item.get("status") for item in statuses} != expected_statuses:
        errors.append("error model status vocabulary is incomplete or expanded")

    for runtime_root in PROHIBITED_RUNTIME_ROOTS:
        if (root / runtime_root).exists():
            errors.append(f"Python runtime package added in BC-018: {runtime_root}")
    for base in (root / SPEC_DIR, root / "docs/architecture", root / ASSIGNMENT_DIR):
        if base.is_dir():
            for path in base.rglob("*.py"):
                errors.append(f"Python runtime/control-plane code in specification surface: {path.relative_to(root)}")

    sums_path = root / "kernel/golden/v0.22.0/SHA256SUMS"
    for line in sums_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected, name = line.split(None, 1)
        target = sums_path.parent / name.strip()
        if hashlib.sha256(target.read_bytes()).hexdigest() != expected:
            errors.append(f"golden checksum mismatch: {name.strip()}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = validate(args.root.resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("BC-018 successor kernel specification validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
