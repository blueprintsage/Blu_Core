#!/usr/bin/env python3
"""Validate BC-020 host-adapter specification integrity and honesty rules."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


BASE_COMMIT = "d4157e79fc7e2df6e1bd53b589cabfa19cd7238f"
REQUIRED = {
    Path("adapters/README.md"),
    Path("adapters/common/capability_contract.json"),
    Path("adapters/common/host_surface_contract.json"),
    Path("adapters/common/receipt_contract.json"),
    Path("adapters/common/error_mapping.json"),
    Path("adapters/common/session_evidence_contract.json"),
    Path("adapters/common/authorization_transport_contract.json"),
    Path("adapters/chat/adapter_contract.json"),
    Path("adapters/chat/capability_matrix.json"),
    Path("adapters/chat/evidence_register.json"),
    Path("adapters/codex/adapter_contract.json"),
    Path("adapters/codex/capability_matrix.json"),
    Path("adapters/codex/evidence_register.json"),
    Path("adapters/security/host_evidence_matrix.json"),
    Path("adapters/security/sur012_disposition.json"),
    Path("docs/domains/runtime/adapters/README.md"),
    Path("docs/domains/runtime/adapters/host_capability_truth.md"),
    Path("docs/domains/runtime/adapters/chat_adapter.md"),
    Path("docs/domains/runtime/adapters/codex_adapter.md"),
    Path("docs/domains/runtime/adapters/security_evidence.md"),
    Path("docs/domains/runtime/adapters/receipts_and_failures.md"),
    Path("docs/domains/runtime/assignments/BC-020/assignment.md"),
    Path("docs/domains/runtime/assignments/BC-020/handoff.md"),
    Path("docs/domains/runtime/assignments/BC-020/validation.md"),
    Path("docs/domains/runtime/assignments/BC-020/review.md"),
}
JSON_FILES = {path for path in REQUIRED if path.suffix == ".json"}
SUPPORT_STATUSES = {
    "documented_possible",
    "verified_available",
    "verified_unavailable",
    "unknown",
    "not_applicable",
}
EVIDENCE_CLASSES = {
    "repo_contract",
    "official_documentation",
    "local_probe",
    "host_receipt",
    "project_owner_observation",
    "unverified",
}
STRONG_CURRENT_EVIDENCE = {"local_probe", "host_receipt"}
REQUIRED_CAPABILITIES = {
    "input.text", "input.host_attachment", "input.image",
    "input.structured_tool_result", "input.workspace_repository_context",
    "retrieval.attached_file", "retrieval.connected_source",
    "retrieval.web_search", "retrieval.integration_context",
    "retrieval.filesystem_read", "action.application",
    "action.filesystem_write", "action.filesystem_create",
    "action.filesystem_delete", "action.filesystem_rename",
    "action.shell_execute", "action.raw_network",
    "action.git.repo_detected", "action.git.read", "action.git.write",
    "action.git.branch_create", "action.git.commit", "action.git.push",
    "action.git.remote_access", "action.git.pr_operation",
    "action.artifact_create", "action.external_tool_invoke",
    "time.current_date", "time.current_time", "time.timezone_offset",
    "time.arithmetic_supplied_values", "schedule.create",
    "schedule.recurring", "schedule.update_cancel", "schedule.receipt",
    "session.host_turn_identity", "session.conversation_thread_identity",
    "session.host_session_binding", "session.cross_turn_security_correlation",
    "session.durable_continuity", "session.saved_memory",
    "security.explicit_user_approval", "security.host_action_confirmation",
    "security.account_session_metadata",
    "security.identity_role_credential_evidence",
    "security.pending_request_correlation", "security.replay_evidence",
    "security.attempt_count_integrity", "output.natural_language",
    "output.structured_result", "output.file_artifact",
    "output.external_side_effect_receipt",
}
REQUIRED_SECURITY_ROWS = {
    "host_session.identity", "host_session.binding", "event.identity",
    "request.correlation", "freshness", "expiry", "replay.detection",
    "state.rollback_resistance", "attempt_count.integrity",
    "authorization_result.binding", "host_action.approval",
    "explicit_user.approval", "account.identity",
    "account.role_or_credential", "provider.operation_receipt",
}
PROTECTED_PATHS = [
    "kernel/golden/v0.22.0",
    "contracts/runtime",
    "contracts/successor",
    "docs/architecture/successor_boundaries.md",
    "docs/architecture/successor_component_graph.md",
    "docs/architecture/successor_kernel.md",
    "docs/architecture/successor_migration_sequence.md",
    "docs/sources/historical_archives",
]


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _duplicates(values: list[str]) -> set[str]:
    return {value for value in values if values.count(value) > 1}


def _contains_all(text: str, terms: set[str]) -> bool:
    lowered = text.lower()
    return all(term.lower() in lowered for term in terms)


def _validate_evidence_register(
    errors: list[str], family: str, register: dict[str, Any]
) -> dict[str, dict[str, Any]]:
    entries = register.get("entries")
    if not isinstance(entries, list) or not entries:
        errors.append(f"{family} evidence register has no entries")
        return {}
    required = {
        "evidence_id", "host_family", "surface_id", "evidence_class",
        "source", "claim", "scope", "accessed_or_observed_at", "freshness",
        "limitations", "supports", "does_not_prove",
    }
    ids = [entry.get("evidence_id") for entry in entries]
    for duplicate in sorted(_duplicates([item for item in ids if isinstance(item, str)])):
        errors.append(f"duplicate {family} evidence ID: {duplicate}")
    result: dict[str, dict[str, Any]] = {}
    for entry in entries:
        evidence_id = entry.get("evidence_id", "<unknown>")
        missing = sorted(required - set(entry))
        if missing:
            errors.append(f"{family} evidence {evidence_id} missing fields: {', '.join(missing)}")
            continue
        if entry.get("host_family") != family:
            errors.append(f"{family} evidence has wrong host_family: {evidence_id}")
        evidence_class = entry.get("evidence_class")
        if evidence_class not in EVIDENCE_CLASSES:
            errors.append(f"invalid evidence class: {evidence_id} -> {evidence_class}")
        if not isinstance(entry.get("limitations"), list) or not entry["limitations"]:
            errors.append(f"evidence lacks limitations: {evidence_id}")
        if not isinstance(entry.get("supports"), list) or not isinstance(entry.get("does_not_prove"), list):
            errors.append(f"evidence lacks support boundaries: {evidence_id}")
        if evidence_class == "official_documentation":
            source = entry.get("source", {})
            parsed = urlparse(str(source.get("url", "")))
            if parsed.scheme != "https" or parsed.netloc not in {"developers.openai.com", "learn.chatgpt.com", "platform.openai.com"}:
                errors.append(f"official documentation URL is invalid or non-primary: {evidence_id}")
            if not source.get("title") or not source.get("accessed_date"):
                errors.append(f"official documentation lacks title/accessed_date: {evidence_id}")
        if evidence_class == "local_probe":
            if entry.get("surface_id") in {None, "", "all_bindings"}:
                errors.append(f"local probe lacks actual surface scope: {evidence_id}")
            if entry.get("freshness") in {None, "", "unknown"}:
                errors.append(f"local probe lacks bounded freshness: {evidence_id}")
        if isinstance(evidence_id, str):
            result[evidence_id] = entry
    return result


def _validate_matrix(
    errors: list[str], family: str, matrix: dict[str, Any], evidence: dict[str, dict[str, Any]]
) -> set[str]:
    records = matrix.get("capabilities")
    if not isinstance(records, list):
        errors.append(f"{family} capability matrix has no capabilities")
        return set()
    ids = [record.get("capability_id") for record in records]
    for duplicate in sorted(_duplicates([item for item in ids if isinstance(item, str)])):
        errors.append(f"duplicate {family} capability ID: {duplicate}")
    id_set = {item for item in ids if isinstance(item, str)}
    missing_required = REQUIRED_CAPABILITIES - id_set
    if missing_required:
        errors.append(f"{family} matrix missing capabilities: {', '.join(sorted(missing_required))}")
    for record in records:
        capability_id = record.get("capability_id", "<unknown>")
        status = record.get("status")
        if status not in SUPPORT_STATUSES:
            errors.append(f"invalid {family} capability status: {capability_id} -> {status}")
        for field in ("family", "surface_scope", "limitations", "freshness", "security_relevance", "receipt_required"):
            if field not in record:
                errors.append(f"{family} capability missing {field}: {capability_id}")
        if not isinstance(record.get("limitations"), list) or not record.get("limitations"):
            errors.append(f"{family} capability lacks limitations: {capability_id}")
        refs = record.get("evidence_refs")
        if not isinstance(refs, list) or not refs:
            errors.append(f"{family} capability lacks evidence refs: {capability_id}")
            continue
        unknown = [ref for ref in refs if ref not in evidence]
        for ref in unknown:
            errors.append(f"unknown {family} evidence ref: {capability_id} -> {ref}")
        classes = {evidence[ref].get("evidence_class") for ref in refs if ref in evidence}
        if status in {"verified_available", "verified_unavailable"} and not classes & STRONG_CURRENT_EVIDENCE:
            errors.append(f"{family} {status} lacks current runtime evidence: {capability_id}")
        if status == "documented_possible" and "official_documentation" not in classes:
            errors.append(f"{family} documented_possible lacks official documentation: {capability_id}")
        if capability_id in {"time.current_date", "time.current_time", "time.timezone_offset"} and status == "verified_available":
            if "host_receipt" not in classes:
                errors.append(f"verified current time lacks provider receipt: {family} {capability_id}")
        if capability_id.startswith("schedule.") and status == "verified_available":
            if not classes & STRONG_CURRENT_EVIDENCE:
                errors.append(f"verified scheduling lacks current provider/tool evidence: {family} {capability_id}")
        if family == "chatgpt" and status == "verified_available" and classes == {"official_documentation"}:
            errors.append(f"Chat documentary claim promoted to verified availability: {capability_id}")
    return id_set


def _validate_golden(root: Path) -> list[str]:
    errors: list[str] = []
    manifest = root / "kernel/golden/v0.22.0/SHA256SUMS"
    if not manifest.is_file():
        return ["missing golden checksum manifest"]
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected, relative = line.split(None, 1)
        target = manifest.parent / relative.strip()
        if not target.is_file():
            errors.append(f"missing golden file: {relative.strip()}")
            continue
        actual = hashlib.sha256(target.read_bytes()).hexdigest()
        if actual.lower() != expected.lower():
            errors.append(f"golden checksum mismatch: {relative.strip()}")
    return errors


def _validate_protected_git_diff(root: Path) -> list[str]:
    if not (root / ".git").exists():
        return []
    result = subprocess.run(
        ["git", "-C", str(root), "diff", "--name-only", BASE_COMMIT, "--", *PROTECTED_PATHS],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return ["unable to verify protected-path diff from BC-020 base"]
    changed = [line for line in result.stdout.splitlines() if line.strip()]
    return [f"protected path changed from BC-020 base: {path}" for path in changed]


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    missing = [str(path) for path in sorted(REQUIRED) if not (root / path).is_file()]
    if missing:
        return [f"missing required file: {path}" for path in missing]

    data: dict[Path, Any] = {}
    for path in sorted(JSON_FILES):
        try:
            data[path] = _load(root / path)
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            errors.append(f"invalid JSON: {path}: {exc}")
    if errors:
        return errors

    capability = data[Path("adapters/common/capability_contract.json")]
    surface = data[Path("adapters/common/host_surface_contract.json")]
    receipt = data[Path("adapters/common/receipt_contract.json")]
    session = data[Path("adapters/common/session_evidence_contract.json")]
    auth = data[Path("adapters/common/authorization_transport_contract.json")]
    chat_adapter = data[Path("adapters/chat/adapter_contract.json")]
    codex_adapter = data[Path("adapters/codex/adapter_contract.json")]
    security_matrix = data[Path("adapters/security/host_evidence_matrix.json")]
    sur012 = data[Path("adapters/security/sur012_disposition.json")]

    if set(capability.get("support_status_values", {})) != SUPPORT_STATUSES:
        errors.append("capability status vocabulary is incomplete")
    if set(capability.get("evidence_class_values", {})) != EVIDENCE_CLASSES:
        errors.append("evidence class vocabulary is incomplete")
    constraints = capability.get("host_adapter_constraints", {})
    if constraints.get("ingress_input") != "raw_host_event" or constraints.get("ingress_output") != "raw_host_input":
        errors.append("Host Adapter ingress contract is not raw_host_event -> raw_host_input")
    if constraints.get("does_not_produce") != "TurnRequest":
        errors.append("Host Adapter is permitted to produce TurnRequest")
    disowned = set(constraints.get("does_not_own", []))
    if not {"OPSEC_policy", "Auth_policy", "ordinary_route_selection", "ScopeLock"}.issubset(disowned):
        errors.append("Host Adapter owns or fails to disown OPSEC/Auth/routing/ScopeLock")

    grade = str(capability.get("security_evidence_grade_values", {}).get("security_grade", ""))
    if not _contains_all(grade, {"binding", "integrity", "freshness", "replay", "rollback"}):
        errors.append("security_grade lacks explicit minimum evidence properties")
    if "official_documentation alone is insufficient" not in capability.get("capability_record", {}).get("verified_available_rule", ""):
        errors.append("official documentation can create verified_available")
    if "unknown" not in capability.get("support_status_values", {}):
        errors.append("unknown capabilities are not permitted")

    if set(surface.get("filesystem_operations", [])) != {"read", "write", "create", "delete", "rename", "execute"}:
        errors.append("filesystem operations are not explicitly separated")
    if set(surface.get("filesystem_scope_values", [])) != {"workspace_only", "additional_roots", "host_defined", "unrestricted", "unknown"}:
        errors.append("filesystem scope vocabulary is incomplete")
    if set(surface.get("network_classes", [])) != {"web_search", "raw_network", "integration_call"}:
        errors.append("network classes are not explicitly separated")
    if not _contains_all(surface.get("continuity_rule", ""), {"conversation", "not", "security-grade", "durable"}):
        errors.append("conversation identity or host_session is conflated with security/durability")

    side_effect_rule = receipt.get("side_effect_rule", "")
    if not _contains_all(side_effect_rule, {"not", "requested", "attempted", "approved", "requires", "receipt"}):
        errors.append("external side-effect success does not require receipt evidence")
    artifact_rule = receipt.get("artifact_receipt", {}).get("verification_rule", "")
    if not _contains_all(artifact_rule, {"created", "provider evidence", "filename", "not"}):
        errors.append("artifact creation can be claimed without evidence")

    approval_rule = auth.get("host_approval_evidence", {}).get("rule", "")
    if not _contains_all(approval_rule, {"host", "never", "authorizationresult", "blu authorization"}):
        errors.append("host approval can become Blu authorization")
    sign_in_rule = auth.get("authorization_evidence_transport", {}).get("sign_in_rule", "")
    if not _contains_all(sign_in_rule, {"signed", "not usable", "identity", "role", "credential"}):
        errors.append("product sign-in can become Blu Auth evidence")
    binding = auth.get("authorization_result_binding", {})
    if binding.get("string_equality_sufficient") is not False or binding.get("conversation_identity_sufficient") is not False:
        errors.append("request-ref equality or conversation identity can satisfy Auth binding")

    truth_rule = session.get("host_session_evidence", {}).get("truth_rule", "")
    if not _contains_all(truth_rule, {"never", "conversation", "model memory", "identifier alone"}):
        errors.append("host_session evidence can be inferred from conversation history")
    replay_rule = session.get("replay_evidence", {}).get("rule", "")
    if not _contains_all(replay_rule, {"timestamp", "does not prove", "request-ref"}):
        errors.append("replay prevention can be claimed from timestamp/string equality")
    attempt = session.get("attempt_count_integrity", {})
    if attempt.get("model_memory_fallback_allowed") is not False or attempt.get("client_local_mutable_state_qualifies") is not False:
        errors.append("untrusted mutable attempt state can qualify")
    attempt_props = set(attempt.get("required_properties_for_protected_cross_turn_use", []))
    if "monotonic_or_rollback_resistant_attempt_state" not in attempt_props:
        errors.append("attempt_count security use lacks rollback-resistant state")
    gate = session.get("protected_cross_turn_resume_gate", {})
    if gate.get("required_grade") != "security_grade" or not {"integrity", "freshness", "expiry", "replay_state", "rollback_resistance"}.issubset(set(gate.get("required_properties", []))):
        errors.append("protected cross-turn state lacks integrity/freshness/replay/rollback gate")
    if not _contains_all(session.get("durability_boundary", ""), {"host_session", "never", "durable_external", "receipt"}):
        errors.append("durable persistence is claimed from host_session")

    for family, adapter in (("chatgpt", chat_adapter), ("codex", codex_adapter)):
        if adapter.get("host_family") != family:
            errors.append(f"wrong host family in {family} adapter contract")
        if adapter.get("event_normalization", {}).get("does_not_produce") != "TurnRequest":
            errors.append(f"{family} adapter produces TurnRequest")
        if adapter.get("implementation_status") != "specification_only":
            errors.append(f"{family} contract claims implementation")

    chat_evidence = _validate_evidence_register(
        errors, "chatgpt", data[Path("adapters/chat/evidence_register.json")]
    )
    codex_evidence = _validate_evidence_register(
        errors, "codex", data[Path("adapters/codex/evidence_register.json")]
    )
    chat_ids = _validate_matrix(
        errors, "chatgpt", data[Path("adapters/chat/capability_matrix.json")], chat_evidence
    )
    codex_ids = _validate_matrix(
        errors, "codex", data[Path("adapters/codex/capability_matrix.json")], codex_evidence
    )
    if chat_ids != codex_ids:
        errors.append("Chat and Codex capability matrices do not inventory the same normalized IDs")

    security_rows = security_matrix.get("rows", [])
    row_ids = [row.get("evidence_capability_id") for row in security_rows]
    for duplicate in sorted(_duplicates([item for item in row_ids if isinstance(item, str)])):
        errors.append(f"duplicate security evidence row: {duplicate}")
    if set(row_ids) != REQUIRED_SECURITY_ROWS:
        errors.append("security evidence matrix is incomplete")
    for row in security_rows:
        row_id = row.get("evidence_capability_id", "<unknown>")
        if not isinstance(row.get("required_properties"), list) or not row.get("required_properties"):
            errors.append(f"security evidence row lacks required properties: {row_id}")
        for family, evidence in (("chat", chat_evidence), ("codex", codex_evidence)):
            cell = row.get(family, {})
            if cell.get("status") not in SUPPORT_STATUSES:
                errors.append(f"invalid {family} security status: {row_id}")
            refs = cell.get("evidence_refs", [])
            for ref in refs:
                if ref not in evidence:
                    errors.append(f"unknown {family} security evidence ref: {row_id} -> {ref}")
            classes = {evidence[ref].get("evidence_class") for ref in refs if ref in evidence}
            if cell.get("status") in {"verified_available", "verified_unavailable"} and not classes & STRONG_CURRENT_EVIDENCE:
                errors.append(f"{family} security claim lacks current evidence: {row_id}")

    if sur012.get("disposition") != "resolved_at_generic_host_evidence_contract_level":
        errors.append("SUR-012 lacks explicit generic host-evidence disposition")
    required_sur012 = set(sur012.get("required_evidence_properties", []))
    if not {"provider_bound_host_session_identity", "pending_request_binding", "authorization_result_binding", "prior_consumption_and_replay_status", "monotonic_or_rollback_resistant_attempt_state"}.issubset(required_sur012):
        errors.append("SUR-012 disposition omits binding/replay/attempt integrity")
    if sur012.get("sur011_state") != "unresolved_security_policy_input":
        errors.append("SUR-011 is resolved by adapter policy")
    if sur012.get("bc030_readiness") != "ready_for_spec":
        errors.append("BC-030 readiness is not derived/preserved")
    if sur012.get("surface_dispositions", {}).get("codex_desktop_local_windows_observed", {}).get("protected_cross_turn_continuation") != "unavailable":
        errors.append("observed Codex surface overclaims protected cross-turn continuation")

    for path in (root / "adapters").rglob("*"):
        if path.is_file() and path.suffix.lower() not in {".json", ".md"}:
            errors.append(f"runtime adapter implementation exists: {path.relative_to(root).as_posix()}")

    errors.extend(_validate_golden(root))
    errors.extend(_validate_protected_git_diff(root))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    errors = validate(args.root.resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"host adapter contract validation failed: {len(errors)} error(s)")
        return 1
    print("host adapter contract validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
