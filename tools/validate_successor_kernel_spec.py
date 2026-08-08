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
CORRECTION_ASSIGNMENT_DIR = Path("docs/domains/runtime/assignments/BC-018-C1")
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
    CORRECTION_ASSIGNMENT_DIR / "assignment.md",
    CORRECTION_ASSIGNMENT_DIR / "handoff.md",
    CORRECTION_ASSIGNMENT_DIR / "validation.md",
    CORRECTION_ASSIGNMENT_DIR / "review.md",
}
JSON_FILES = {path for path in REQUIRED if path.suffix == ".json"}
ALLOWED_DOMAINS = {
    "model_facing", "deterministic_core", "host_service", "host_adapter",
    "continuity_provider", "hybrid", "deferred", "reject",
}
ALLOWED_COMPONENT_STATUS = {"approved_boundary", "candidate", "deferred", "rejected"}
ALLOWED_LIFETIMES = {"none", "turn", "host_session", "durable_external"}
PENDING_AUTH_REQUIRED_FIELDS = {
    "state_record_ref", "authorization_request_ref", "protected_action_scope",
    "protected_resource_scope", "request_binding", "issued_at", "expires_at",
    "attempt_count", "maximum_attempts", "retry_allowed",
    "lockout_or_block_state", "host_session_binding",
    "last_authorization_result_ref", "status", "storage_lifetime",
    "provenance_receipt_ref",
}
HOST_SESSION_EVIDENCE_FIELDS = {
    "host_session_id_or_opaque_binding_ref", "provider",
    "verification_or_binding_method", "scope", "created_or_observed_at",
    "state_record_identity", "expires_at_or_lifetime_boundary",
    "receipt_or_evidence_ref", "availability_or_failure_result",
}
PRE_INGRESS_FORBIDDEN_SERVICES = {
    "arbitrary_tool", "source_lookup", "scheduling", "unrelated_continuity_write",
    "model_execution", "ordinary_service_dispatch",
}
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
    state_records = packet_contract.get("state_records", [])

    for records, key, label in (
        (components, "component_id", "component"),
        (behaviors, "behavior_id", "behavior"),
        (interfaces, "interface_id", "interface"),
        (packets, "packet_id", "packet"),
        (statuses, "status", "status"),
        (unresolved, "id", "unresolved item"),
        (evidence_catalog, "evidence_ref", "evidence"),
        (requirements, "successor_requirement_id", "traceability requirement"),
        (state_records, "state_record_id", "state record"),
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
        if isinstance(lifetimes, list) and "session" in lifetimes:
            errors.append(f"bare session lifetime claims unexplained cross-turn kernel persistence: {component_id}")
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
        if component.get("domain") == "deterministic_core" and set(lifetimes or []) - {"none", "turn"}:
            errors.append(f"deterministic component declares hidden cross-turn state: {component_id}")

    lifetime_values = set(data["component_registry.json"].get("state_lifetime_values", []))
    lifetime_contract = data["component_registry.json"].get("state_lifetime_contract", {})
    if lifetime_values != ALLOWED_LIFETIMES or lifetime_contract.get("bare_session_allowed") is not False:
        errors.append("state lifetime taxonomy permits bare session persistence")
    if "evidenced host_session" not in str(lifetime_contract.get("cross_turn_rule", "")):
        errors.append("cross-turn state rule lacks evidenced host_session or durable_external substrate")

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

    attempt_owners = [
        item.get("component_id") for item in components
        if "authorization_attempt_permission" in item.get("owns", [])
    ]
    if attempt_owners != ["security_restraint"]:
        errors.append("authorization attempt policy is not owned solely by security_restraint")
    if controller.get("state_lifetime") != ["turn"] or "cross_turn_state_storage" not in controller.get("does_not_own", []):
        errors.append("Turn Controller declares hidden cross-turn state")

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
    if auth_loop.get("turn_model") != "cross_turn" or interface_auth.get("turn_model") != "cross_turn":
        errors.append("pre-ingress authorization path is not explicitly cross-turn")
    if auth_loop.get("maximum_terminal_packets_per_host_turn") != 1 or interface_auth.get("one_terminal_packet_per_host_turn") is not True:
        errors.append("cross-turn authorization path can produce two TerminalPackets for one host turn")
    if auth_loop.get("turn_n", {}).get("ordinary_routing") is not False:
        errors.append("authorization ASK turn enters ordinary routing")

    terminal_authority = packet_contract.get("pre_ingress_terminal_authority_contract", {})
    security_decision = by_packet.get("SecurityDecision", {})
    validation_result = by_packet.get("ValidationResult", {})
    terminal_packet = by_packet.get("TerminalPacket", {})
    security_invariants = " ".join(security_decision.get("invariants", [])).lower()
    validation_invariants = " ".join(validation_result.get("invariants", [])).lower()
    terminal_invariants = " ".join(terminal_packet.get("invariants", [])).lower()
    if (set(terminal_authority.get("security_decision_statuses", [])) != {"PASS", "BLOCK", "ASK"} or
            "status is pass, block, or ask" not in security_invariants):
        errors.append("SecurityDecision status vocabulary is expanded beyond PASS, BLOCK, ASK")
    if terminal_authority.get("control_decision_required") is not False:
        errors.append("pre-ingress UNAVAILABLE improperly requires ControlDecision")
    if (terminal_authority.get("authority_ref_type") != "SecurityDecision" or
            "originating securitydecision" not in validation_invariants or
            "originating securitydecision" not in terminal_invariants):
        errors.append("pre-ingress UNAVAILABLE lacks SecurityDecision authority")
    if (set(terminal_authority.get("pre_ingress_terminal_statuses", [])) != {"BLOCK", "ASK", "UNAVAILABLE"} or
            terminal_authority.get("owner") != "security_restraint" or
            terminal_authority.get("ordinary_routing") is not False):
        errors.append("pre-ingress terminal authority contract is incomplete")
    if (terminal_authority.get("binding_resolution_terminal_count") != 1 or
            "mutually exclusive" not in str(auth_loop.get("turn_n", {}).get("terminal_selection_point", "")).lower() or
            "instead of a second terminal packet" not in terminal_invariants):
        errors.append("binding failure can emit ASK followed by UNAVAILABLE")

    pending = next((item for item in state_records if item.get("state_record_id") == "PendingAuthorizationState"), {})
    pending_fields = set(pending.get("required_fields", []))
    if not pending or pending.get("semantic_owner") != "security_restraint":
        errors.append("PendingAuthorizationState lacks security_restraint semantic ownership")
    allowed_pending_lifetimes = set(pending.get("allowed_storage_lifetimes", []))
    if (pending.get("substrate_provider") != "host_adapter_boundary" or
            not allowed_pending_lifetimes or
            allowed_pending_lifetimes - {"host_session", "durable_external"}):
        errors.append("pending authorization request lacks evidenced host_session or continuity-backed substrate")
    if not PENDING_AUTH_REQUIRED_FIELDS <= pending_fields:
        errors.append("PendingAuthorizationState required fields are incomplete")
    repetition = auth_loop.get("repetition_contract", {})
    if "expires_at" not in pending_fields or repetition.get("expiry_required") is not True:
        errors.append("outstanding authorization request lacks expiry")
    max_attempts = repetition.get("maximum_attempts")
    if "maximum_attempts" not in pending_fields or max_attempts != "policy_defined_finite_positive_integer":
        errors.append("outstanding authorization request lacks finite retry/attempt bound")
    pending_invariants = " ".join(pending.get("invariants", [])).lower()
    if repetition.get("replay_rule_required") is not True or "replay" not in pending_invariants:
        errors.append("replayable authorization request lacks replay rule")
    if (repetition.get("request_binding_required") is not True or
            "request_binding" not in pending_fields or "host_session_binding" not in pending_fields):
        errors.append("pending authorization request lacks request and host-session binding")
    if "fail_closed" not in str(repetition.get("exhaustion_behavior", "")):
        errors.append("authorization exhaustion does not fail closed")
    activation = pending.get("activation_contract", {})
    if (activation.get("unbound_request_correlatable") is not False or
            activation.get("unavailable_binding_becomes_active") is not False or
            "never becomes active or resumable" not in str(activation.get("binding_unavailable", "")).lower()):
        errors.append("unbound PendingAuthorizationState remains resumable after substrate failure")

    host_session_contract = interface_contract.get("host_session_state_contract", {})
    if not HOST_SESSION_EVIDENCE_FIELDS <= set(host_session_contract.get("required_evidence_fields", [])):
        errors.append("host_session state boundary lacks required provider evidence fields")
    host_security_rules = " ".join(host_session_contract.get("security_rules", [])).lower()
    if "model memory" not in host_security_rules or "conversation history" not in host_security_rules:
        errors.append("host_session state boundary permits model memory or conversation history as security storage")
    if ("evidenced_host_session_state_substrate" not in adapter.get("owns", []) or
            "pending_request_event_correlation" not in adapter.get("owns", [])):
        errors.append("host adapter lacks evidenced host-session substrate and request correlation ownership")

    authorization_result = by_packet.get("AuthorizationResult", {})
    authorization_result_fields = set(authorization_result.get("required_fields", []))
    validity = packet_contract.get("authorization_result_validity_contract", {})
    allowed_validity = set(validity.get("allowed_validity_lifetimes", []))
    required_result_fields = {
        "authorization_result_ref", "action_scope", "resource_scope", "result",
        "assurance", "issued_at", "expires_at", "validity_lifetime",
        "provider_ref", "evidence_refs", "revocation_reset_state",
    }
    if not required_result_fields <= authorization_result_fields:
        errors.append("AuthorizationResult evidenced validity fields are incomplete")
    if allowed_validity != {"turn", "host_session", "durable_external"} or validity.get("bare_session_allowed") is not False:
        errors.append("AuthorizationResult claims session validity without evidenced lifetime binding")

    service_exchange = by_packet.get("ServiceExchange", {})
    authority_contract = packet_contract.get("service_exchange_authority_contract", {})
    pre_ingress_authority = authority_contract.get("pre_ingress_authorization", {})
    if "authority_class" not in service_exchange.get("required_fields", []):
        errors.append("ServiceExchange authority class is not machine-checkable")
    if set(authority_contract.get("allowed_authority_classes", [])) != {"ordinary_control", "pre_ingress_authorization"}:
        errors.append("ServiceExchange authority classes are incomplete or expanded")
    if (pre_ingress_authority.get("allowed_interface") != "IF-AUTHORIZATION-PROVIDER" or
            pre_ingress_authority.get("allowed_service_id") != "authorization_evidence" or
            pre_ingress_authority.get("ordinary_control_decision_authority") is not False or
            not {"authorization_request_ref", "host_session_binding_ref"} <= set(pre_ingress_authority.get("required_fields", [])) or
            not PRE_INGRESS_FORBIDDEN_SERVICES <= set(pre_ingress_authority.get("forbidden_service_classes", []))):
        errors.append("pre_ingress_authorization ServiceExchange can authorize an ordinary service")

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
    lifetime_requirement = next(
        (item for item in requirements if item.get("successor_requirement_id") == "SKR-015"), {}
    )
    if "bare session" not in str(lifetime_requirement.get("requirement", "")):
        errors.append("revised state-lifetime rule lacks traceability")

    time_arithmetic = by_behavior.get("time arithmetic", {})
    if (time_arithmetic.get("deterministic_owner") != "turn_controller" or
            "supplied_time_arithmetic" not in controller.get("owns", [])):
        errors.append("supplied-time arithmetic ownership is inconsistent")
    mood = by_behavior.get("Mood", {})
    if mood.get("deterministic_owner") is not None or "model_execution_boundary" not in str(mood.get("model_owner", "")):
        errors.append("optional profile behavior is incorrectly owned by Turn Controller")

    expected_statuses = {"PASS", "BLOCK", "ASK", "UNAVAILABLE", "INVALID", "ERROR"}
    if {item.get("status") for item in statuses} != expected_statuses:
        errors.append("error model status vocabulary is incomplete or expanded")

    for runtime_root in PROHIBITED_RUNTIME_ROOTS:
        if (root / runtime_root).exists():
            errors.append(f"Python runtime package added in BC-018: {runtime_root}")
    for base in (
        root / SPEC_DIR, root / "docs/architecture", root / ASSIGNMENT_DIR,
        root / CORRECTION_ASSIGNMENT_DIR,
    ):
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
