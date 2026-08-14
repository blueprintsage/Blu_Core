#!/usr/bin/env python3
"""Validate BC-030 continuity contracts plus BC-040 schema hardening."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource


BASE_COMMIT = "66e7ed52f5777bdef2e32c71a5e83b439b0d0ade"
SPEC_DIR = Path("continuity")
ASSIGNMENT_DIR = Path("docs/domains/continuity/assignments/BC-030")
REQUIRED = {
    SPEC_DIR / "README.md",
    SPEC_DIR / "schemas/continuity_record.schema.json",
    SPEC_DIR / "schemas/continuity_receipt.schema.json",
    SPEC_DIR / "schemas/continuity_query.schema.json",
    SPEC_DIR / "schemas/continuity_retrieval_result.schema.json",
    SPEC_DIR / "schemas/continuity_provider_availability.schema.json",
    SPEC_DIR / "schemas/continuity_mutation_request.schema.json",
    SPEC_DIR / "evidence_stages.json",
    SPEC_DIR / "lifecycle.json",
    SPEC_DIR / "rehydration.json",
    SPEC_DIR / "security_evidence.json",
    SPEC_DIR / "local_mirror_profile.json",
    SPEC_DIR / "sur007_disposition.json",
    Path("contracts/successor/component_registry.json"),
    Path("contracts/successor/interface_registry.json"),
    Path("contracts/successor/packet_registry.json"),
    Path("contracts/successor/unresolved_register.json"),
    Path("docs/domains/continuity/local_mirror_continuity.md"),
    ASSIGNMENT_DIR / "assignment.md",
    ASSIGNMENT_DIR / "handoff.md",
    ASSIGNMENT_DIR / "validation.md",
    ASSIGNMENT_DIR / "review.md",
    Path("MANIFEST.sha256"),
    Path("tests/continuity/fixtures/schema_instances.json"),
    Path("requirements-contracts.txt"),
}
JSON_FILES = {path for path in REQUIRED if path.suffix == ".json"}
LIFETIMES = {"none", "turn", "host_session", "durable_external"}
RECORD_STATUSES = {"current", "superseded", "retired"}
OPERATIONS = {
    "create", "retrieve", "update", "supersede", "retire",
    "recover_history", "validate",
}
RECEIPT_OPERATIONS = OPERATIONS | {"availability_probe"}
RECEIPT_STATUSES = {
    "completed", "conflict", "not_found", "unavailable", "degraded",
    "forbidden", "invalid", "integrity_failure", "failed",
}
AVAILABILITY = {"available", "degraded", "unavailable", "unknown"}
EVIDENCE_STAGES = {
    "source_present", "record_discovered", "record_retrieved",
    "write_requested", "write_attempted", "record_created", "record_updated",
    "supersession_recorded", "record_retired", "record_validated",
    "durable_receipt_emitted", "operation_failed", "provider_unavailable",
}
PROTECTED_AUTH_PROPERTIES = {
    "state_record_identity", "authorization_request_binding",
    "protected_action_scope", "protected_resource_scope",
    "issued_at_and_finite_expiry", "integrity",
    "prior_consumption_and_replay_state", "atomic_expected_version_transition",
    "monotonic_or_rollback_resistant_attempt_state",
    "provider_operation_receipt_ref",
}
PROTECTED_PATHS = [
    "kernel/golden/v0.22.0",
    "contracts/runtime",
    "contracts/successor/component_registry.json",
    "contracts/successor/behavior_placement.json",
    "contracts/successor/interface_registry.json",
    "contracts/successor/packet_registry.json",
    "contracts/successor/error_model.json",
    "contracts/successor/unresolved_register.json",
    "contracts/successor/traceability.json",
    "docs/architecture",
    "adapters",
    "config/source_authority.json",
]
PROHIBITED_IMPLEMENTATION_ROOTS = {
    Path("src"), Path("runtime"), Path("blu_core"), Path("providers"),
    Path("local_mirror"), Path("lm_studio"), Path("pass"), Path("skillforge"),
}
# BC-050-C1: `src` is conditionally permitted, and only for the authorized
# BC-050 Phase-1 package. Every other root above stays prohibited outright.


# BC-050-C2: one complete authorization record, authenticated independently at
# every enforcement point. Validator ordering is not an authorization mechanism.
BC050_ASSIGNMENT = "BC-050"
BC050_AUTHORIZED_BY = "Dad/Blu"
BC050_PACKET = "docs/domains/runtime/assignments/BC-050/assignment.md"
BC050_AUTHORIZATION_DATE = "2026-08-12"
BC050_CHECKLIST = Path("readiness/python_phase1_readiness_checklist.json")
BC050_SLICE = Path("readiness/phase1_executable_slice.json")
BC050_PRODUCTION_PREFIX = "src/blu_runtime/"
BC050_TEST_PREFIX = "tests/runtime_phase1/"
BC050_ROOT_FILES = {"pyproject.toml"}


def _bc050_authorized(root: Path) -> bool:
    """Authenticate the complete BC-050 implementation authorization record.

    Fail-closed. Any missing, malformed, contradictory, or non-exact value
    restores this validator's pre-implementation prohibition, independently of
    what any other validator concludes.

    Every field is compared to its exact approved value. Cross-file equality is
    not authentication: the same wrong date in every record is still the wrong
    date, so the authorization date is bound to the approved constant rather
    than merely to its own copies.
    """
    try:
        checklist = json.loads((root / BC050_CHECKLIST).read_text(encoding="utf-8"))
        executable_slice = json.loads((root / BC050_SLICE).read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return False
    if not isinstance(checklist, dict) or not isinstance(executable_slice, dict):
        return False
    record = checklist.get("bc050_implementation_authorization")
    nested = executable_slice.get("implementation_authorization")
    if not isinstance(record, dict) or not isinstance(nested, dict):
        return False
    return (
        record.get("state") == "authorized"
        and record.get("assignment") == BC050_ASSIGNMENT
        and record.get("authorized_by") == BC050_AUTHORIZED_BY
        and record.get("authorization_date") == BC050_AUTHORIZATION_DATE
        and record.get("packet") == BC050_PACKET
        and nested.get("assignment") == BC050_ASSIGNMENT
        and nested.get("authorized_by") == BC050_AUTHORIZED_BY
        and nested.get("authorization_date") == BC050_AUTHORIZATION_DATE
        and nested.get("packet") == BC050_PACKET
        and checklist.get("implementation_authorized") is True
        and executable_slice.get("implementation_authorized") is True
        and checklist.get("automatic_start_prohibited") is True
    )


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _contains_all(value: Any, terms: set[str]) -> bool:
    text = str(value).lower()
    return all(term.lower() in text for term in terms)


def _required(schema: dict[str, Any]) -> set[str]:
    value = schema.get("required", [])
    return set(value) if isinstance(value, list) else set()


def _enum(schema: dict[str, Any], property_name: str) -> set[str]:
    value = schema.get("properties", {}).get(property_name, {}).get("enum", [])
    return set(value) if isinstance(value, list) else set()


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


def _git_changed_paths(root: Path, paths: list[str] | None = None) -> tuple[list[str], str | None]:
    if not (root / ".git").exists():
        return [], None
    command = ["git", "-C", str(root), "diff", "--name-only", BASE_COMMIT, "--"]
    if paths:
        command.extend(paths)
    result = subprocess.run(command, check=False, capture_output=True, text=True)
    if result.returncode != 0:
        return [], "unable to verify Git diff from BC-030 base"
    return [line.strip() for line in result.stdout.splitlines() if line.strip()], None


def _is_authorized_bc041_sur001_update(root: Path) -> bool:
    """Permit only BC-041's bounded SUR-001 metadata change in the protected register."""
    relative = "contracts/successor/unresolved_register.json"
    baseline = subprocess.run(
        ["git", "-C", str(root), "show", f"{BASE_COMMIT}:{relative}"],
        check=False,
        capture_output=True,
        text=True,
    )
    if baseline.returncode != 0:
        return False
    try:
        before = json.loads(baseline.stdout)
        after = _load(root / relative)
    except (json.JSONDecodeError, OSError):
        return False
    if {key: value for key, value in before.items() if key != "items"} != {
        key: value for key, value in after.items() if key != "items"
    }:
        return False
    before_items = {item.get("id"): item for item in before.get("items", [])}
    after_items = {item.get("id"): item for item in after.get("items", [])}
    if set(before_items) != set(after_items):
        return False
    if any(before_items[item_id] != after_items[item_id] for item_id in before_items if item_id != "SUR-001"):
        return False
    original = before_items.get("SUR-001", {})
    resolved = after_items.get("SUR-001", {})
    preserved_fields = {"id", "question", "why_unresolved", "evidence", "blocking_for_BC020", "blocking_for_BC030"}
    if any(original.get(field) != resolved.get(field) for field in preserved_fields):
        return False
    required = {
        "disposition": "resolved_at_minimum_phase1_contract_level",
        "resolution_record": "contracts/security/opsec/minimum_contract.json",
        "blocking_for_implementation": False,
    }
    return all(resolved.get(field) == value for field, value in required.items())


def _validate_git_scope(root: Path) -> list[str]:
    errors: list[str] = []
    changed, failure = _git_changed_paths(root, PROTECTED_PATHS)
    if failure:
        return [failure]
    if "contracts/successor/unresolved_register.json" in changed and _is_authorized_bc041_sur001_update(root):
        changed.remove("contracts/successor/unresolved_register.json")
    errors.extend(f"protected path changed from BC-030 base: {path}" for path in changed)

    all_changed, failure = _git_changed_paths(root)
    if failure:
        return [failure]
    allowed_python = {
        "tools/validate_continuity_contracts.py",
        "tests/continuity/test_validate_continuity_contracts.py",
        "tools/validate_python_readiness.py",
        "tests/readiness/test_validate_python_readiness.py",
        # BC-050-C2: shared authorization mutation matrix (test support only).
        "tests/readiness/bc050_authorization_matrix.py",
        "tools/validate_opsec_contracts.py",
        "tests/security/test_validate_opsec_contracts.py",
    }
    authorized = _bc050_authorized(root)
    for path in all_changed:
        forward = path.replace("\\", "/")
        normalized = forward.lower()
        if normalized.endswith(".py") and forward not in allowed_python:
            # BC-050-C1: authorized Phase-1 code is permitted under exactly the
            # BC-050 production and test roots. Everything else still fails.
            if not (
                authorized
                and (
                    forward.startswith(BC050_PRODUCTION_PREFIX)
                    or forward.startswith(BC050_TEST_PREFIX)
                )
            ):
                errors.append(f"runtime or provider Python implementation changed: {path}")
        if re.search(r"(^|/)(pass|skillforge)(/|$)", normalized):
            errors.append(f"PASS/SkillForge scope bleed: {path}")
        if re.search(r"(^|/)(lm[_-]?studio)(/|$)", normalized):
            errors.append(f"LM Studio adapter implementation path changed: {path}")
    return errors


def _validate_no_implementation_tree(root: Path) -> list[str]:
    errors: list[str] = []
    authorized = _bc050_authorized(root)
    for relative in PROHIBITED_IMPLEMENTATION_ROOTS:
        path = root / relative
        if not (path.exists() and any(item.is_file() for item in path.rglob("*"))):
            continue
        # BC-050-C1: an authorized BC-050 runtime under src/blu_runtime/** is no
        # longer itself a continuity-contract violation. Unauthorized trees, and
        # any file under src/ outside that package, remain violations.
        if relative == Path("src") and authorized:
            for item in path.rglob("*"):
                if item.is_file():
                    entry = item.relative_to(root).as_posix()
                    if not entry.startswith(BC050_PRODUCTION_PREFIX):
                        errors.append(f"runtime or provider implementation exists: {entry}")
            continue
        errors.append(f"runtime or provider implementation exists: {relative.as_posix()}")
    for path in (root / SPEC_DIR).rglob("*"):
        if path.is_file() and path.suffix.lower() not in {".json", ".md"}:
            errors.append(f"executable continuity implementation exists: {path.relative_to(root).as_posix()}")
    return errors


def _git_index_bytes(root: Path, path: str) -> bytes | None:
    result = subprocess.run(
        ["git", "-C", str(root), "show", f":{path}"],
        check=False,
        capture_output=True,
    )
    return result.stdout if result.returncode == 0 else None


def _canonical_worktree_bytes(path: Path) -> bytes:
    value = path.read_bytes()
    if b"\x00" not in value:
        value = value.replace(b"\r\n", b"\n")
    return value


def _validate_manifest_coverage(root: Path) -> list[str]:
    if not (root / ".git").exists():
        return []
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "--cached", "--others", "--exclude-standard"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return ["unable to enumerate repository files for manifest coverage"]
    expected = {line.strip() for line in result.stdout.splitlines() if line.strip()} - {"MANIFEST.sha256"}
    actual: list[str] = []
    manifest_digests: dict[str, str] = {}
    for line in (root / "MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        parts = line.split(None, 1)
        if len(parts) != 2:
            return ["invalid MANIFEST.sha256 entry"]
        digest, path = parts[0].lower(), parts[1].strip()
        actual.append(path)
        manifest_digests[path] = digest
    errors: list[str] = []
    for path in sorted(expected - set(actual)):
        errors.append(f"tracked or assignment file missing from MANIFEST.sha256: {path}")
    for path in sorted(set(actual) - expected):
        errors.append(f"stale path present in MANIFEST.sha256: {path}")
    for path in sorted({item for item in actual if actual.count(item) > 1}):
        errors.append(f"duplicate MANIFEST.sha256 path: {path}")
    for path in sorted(expected & set(actual)):
        canonical = _git_index_bytes(root, path)
        if canonical is None:
            target = root / path
            if not target.is_file():
                continue
            canonical = _canonical_worktree_bytes(target)
        digest = hashlib.sha256(canonical).hexdigest()
        if manifest_digests.get(path) != digest:
            errors.append(f"MANIFEST.sha256 digest mismatch: {path}")
    return errors


def _schema_registry(schemas: list[dict[str, Any]]) -> Registry:
    resources = []
    for schema in schemas:
        Draft202012Validator.check_schema(schema)
        resources.append((schema["$id"], Resource.from_contents(schema)))
    return Registry().with_resources(resources)


def _validate_schema_instances(root: Path, data: dict[Path, Any]) -> list[str]:
    errors: list[str] = []
    schema_paths = sorted(path for path in JSON_FILES if path.name.endswith(".schema.json"))
    schemas = [data[path] for path in schema_paths]
    try:
        registry = _schema_registry(schemas)
    except Exception as exc:  # schema errors must be explicit validation failures
        return [f"invalid Draft 2020-12 continuity schema: {exc}"]

    try:
        fixtures = _load(root / "tests/continuity/fixtures/schema_instances.json")
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        return [f"invalid schema instance fixture matrix: {exc}"]

    by_name = {path.name: data[path] for path in schema_paths}
    covered: set[tuple[str, bool]] = set()
    for case in fixtures.get("cases", []):
        case_id = case.get("case_id", "<missing>")
        schema_name = case.get("schema")
        expected_valid = case.get("valid")
        if schema_name not in by_name or not isinstance(expected_valid, bool):
            errors.append(f"invalid schema fixture metadata: {case_id}")
            continue
        covered.add((schema_name, expected_valid))
        validator = Draft202012Validator(
            by_name[schema_name], registry=registry, format_checker=FormatChecker()
        )
        instance_errors = list(validator.iter_errors(case.get("instance")))
        if expected_valid and instance_errors:
            errors.append(f"valid schema fixture rejected: {case_id}: {instance_errors[0].message}")
        if not expected_valid and not instance_errors:
            errors.append(f"invalid schema fixture accepted: {case_id}")
    for schema_name in sorted(by_name):
        for expected_valid in (True, False):
            if (schema_name, expected_valid) not in covered:
                errors.append(
                    f"schema lacks {'valid' if expected_valid else 'invalid'} instance fixture: {schema_name}"
                )
    return errors


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

    components = data[Path("contracts/successor/component_registry.json")]
    interfaces = data[Path("contracts/successor/interface_registry.json")]
    packets = data[Path("contracts/successor/packet_registry.json")]
    unresolved = data[Path("contracts/successor/unresolved_register.json")]

    if len(components.get("components", [])) != 7:
        errors.append("successor component count is not seven")
    if len(packets.get("packets", [])) != 8:
        errors.append("successor packet count is not eight")
    if len(interfaces.get("interfaces", [])) != 9:
        errors.append("successor interface count is not nine")
    if set(components.get("state_lifetime_values", [])) != LIFETIMES:
        errors.append("state lifetime vocabulary changed")
    lifetime = components.get("state_lifetime_contract", {})
    if lifetime.get("bare_session_allowed") is not False:
        errors.append("bare session is allowed as a persistence substrate")
    if not _contains_all(lifetime.get("host_session", ""), {"host-owned", "receipt"}):
        errors.append("host_session evidence contract was weakened")
    if not _contains_all(lifetime.get("durable_external", ""), {"external", "explicit", "receipt"}):
        errors.append("durable_external receipt contract was weakened")

    continuity_components = [
        item for item in components.get("components", [])
        if item.get("component_id") == "continuity_provider_boundary"
    ]
    if len(continuity_components) != 1:
        errors.append("generic continuity provider boundary is missing or duplicated")
    continuity_interfaces = [
        item for item in interfaces.get("interfaces", [])
        if item.get("interface_id") == "IF-CONTINUITY-PROVIDER"
    ]
    if len(continuity_interfaces) != 1:
        errors.append("IF-CONTINUITY-PROVIDER is missing or duplicated")
    elif set(continuity_interfaces[0].get("request_packets", [])) != {"ServiceExchange"} or set(
        continuity_interfaces[0].get("response_packets", [])
    ) != {"ServiceExchange"}:
        errors.append("continuity interface invents a new packet")

    packet_ids = {item.get("packet_id") for item in packets.get("packets", [])}
    if "PendingAuthorizationState" in packet_ids:
        errors.append("PendingAuthorizationState became a packet")

    record = data[SPEC_DIR / "schemas/continuity_record.schema.json"]
    record_required = {
        "record_id", "version_id", "record_type", "scope", "schema_version",
        "version", "created_evidence", "updated_evidence", "status",
        "predecessor", "successor", "payload_ref", "integrity_ref",
        "sensitivity", "visibility", "provider_id", "provider_native_ref",
        "provenance_refs",
    }
    if not record_required.issubset(_required(record)):
        errors.append("ContinuityRecord required fields are incomplete")
    if _enum(record, "status") != RECORD_STATUSES:
        errors.append("ContinuityRecord status vocabulary is incomplete")
    invariants = " ".join(record.get("x-blu-invariants", []))
    if not _contains_all(invariants, {"record_id", "stable", "version_id", "immutable", "path", "never persistence proof"}):
        errors.append("ContinuityRecord identity or path-proof invariant is incomplete")

    receipt = data[SPEC_DIR / "schemas/continuity_receipt.schema.json"]
    if not {"requested_action", "expected_version", "related_record_refs"}.issubset(_required(receipt)):
        errors.append("ContinuityReceipt action or related-record binding is incomplete")
    if _enum(receipt, "operation") != RECEIPT_OPERATIONS:
        errors.append("ContinuityReceipt operation vocabulary is incomplete")
    if _enum(receipt, "status") != RECEIPT_STATUSES:
        errors.append("ContinuityReceipt status vocabulary is incomplete")
    durable_rule = receipt.get("x-blu-durable-success-rule", "")
    if not _contains_all(durable_rule, {"only", "status=completed", "provider", "requested", "attempted", "model", "path"}):
        errors.append("durable success can be self-certified without a completed provider receipt")
    if not _contains_all(receipt.get("x-blu-action-binding-rule", ""), {"requested_action", "equal", "operation", "request_id", "scope", "related"}):
        errors.append("ContinuityReceipt is not bound to its requested action and related records")
    if not _contains_all(receipt.get("x-blu-failure-rule", ""), {"non-completed", "unchanged", "failure"}):
        errors.append("failed writes can become durable state")

    mutation = data[SPEC_DIR / "schemas/continuity_mutation_request.schema.json"]
    mutation_required = {"request_id", "provider_id", "operation", "scope", "record_id", "expected_version"}
    if not mutation_required.issubset(_required(mutation)):
        errors.append("ContinuityMutationRequest required fields are incomplete")
    if _enum(mutation, "operation") != {"create", "update", "supersede", "retire"}:
        errors.append("ContinuityMutationRequest operation vocabulary is incomplete")
    if not _contains_all(mutation.get("x-blu-receipt-binding-rule", ""), {"request_id", "provider_id", "operation", "scope", "record_id", "expected_version", "exactly"}):
        errors.append("mutation request is not checkably bound to its receipt")

    query = data[SPEC_DIR / "schemas/continuity_query.schema.json"]
    if query.get("properties", {}).get("limit", {}).get("maximum") != 100:
        errors.append("ContinuityQuery is not deterministically bounded")
    if not _contains_all(query.get("x-blu-scope-rule", ""), {"one", "exact scope", "not silently merge", "incompatible"}):
        errors.append("ContinuityQuery permits silent incompatible-scope merge")

    retrieval = data[SPEC_DIR / "schemas/continuity_retrieval_result.schema.json"]
    if _enum(retrieval, "availability") != AVAILABILITY:
        errors.append("retrieval availability vocabulary is incomplete")
    if not _contains_all(retrieval.get("x-blu-staging-rule", ""), {"only after", "identity", "scope", "version", "provenance", "integrity"}):
        errors.append("retrieved material can enter context without validation")

    availability = data[SPEC_DIR / "schemas/continuity_provider_availability.schema.json"]
    if _enum(availability, "state") != AVAILABILITY:
        errors.append("provider availability vocabulary is incomplete")
    if not _contains_all(availability.get("x-blu-truth-rule", ""), {"configured", "does not prove", "current", "evidence"}):
        errors.append("provider availability can be inferred from configuration alone")

    stages = data[SPEC_DIR / "evidence_stages.json"]
    if set(stages.get("stage_values", [])) != EVIDENCE_STAGES:
        errors.append("continuity evidence-stage vocabulary is incomplete")
    stage_rules = stages.get("rules", {})
    if not _contains_all(stage_rules.get("durable_success", ""), {"only", "provider", "status=completed", "receipt"}):
        errors.append("evidence stages permit durable success without provider receipt")
    if not _contains_all(stage_rules.get("model_boundary", ""), {"model", "conversation", "prompt", "cannot"}):
        errors.append("model or context can self-certify persistence")

    lifecycle = data[SPEC_DIR / "lifecycle.json"]
    if set(lifecycle.get("record_status_values", [])) != RECORD_STATUSES:
        errors.append("lifecycle record status vocabulary is incomplete")
    if set(lifecycle.get("operation_values", [])) != OPERATIONS:
        errors.append("lifecycle operation vocabulary is incomplete")
    if set(lifecycle.get("receipt_status_values", [])) != RECEIPT_STATUSES:
        errors.append("lifecycle receipt status vocabulary is incomplete")
    if {item.get("operation") for item in lifecycle.get("transitions", [])} != OPERATIONS:
        errors.append("lifecycle transitions are incomplete or duplicated")
    if not _contains_all(lifecycle.get("conflict_rule", ""), {"expected-version", "conflict", "no mutation", "silent overwrite", "forbidden"}):
        errors.append("expected-version conflict handling is inconsistent")
    if not _contains_all(lifecycle.get("history_rule", ""), {"preserve", "history", "no delete", "destroy"}):
        errors.append("history retention or no-deletion rule is incomplete")
    if not _contains_all(lifecycle.get("corruption_rule", ""), {"integrity_failure", "no", "repair", "historical", "receipt"}):
        errors.append("corruption behavior can fabricate or silently repair state")
    if not _contains_all(lifecycle.get("availability_probe_rule", ""), {"receipt-only", "observation", "no record-state transition"}):
        errors.append("availability_probe record-state semantics are unclear")

    rehydration = data[SPEC_DIR / "rehydration.json"]
    required_sequence = [
        "new_runtime_or_hosted_turn", "observe_provider_availability",
        "issue_bounded_continuity_query", "receive_provider_result_and_receipt",
        "validate_identity_scope_status_version_provenance_authorization_integrity",
        "stage_authorized_bounded_turn_context", "invoke_model_if_appropriate",
    ]
    if rehydration.get("sequence") != required_sequence:
        errors.append("stateless rehydration sequence is incomplete or reordered")
    if not _contains_all(rehydration.get("model_context_rule", ""), {"turn-local", "not", "durable", "receipt", "remembered"}):
        errors.append("model context is treated as persistence")
    if not _contains_all(rehydration.get("host_session_rule", ""), {"host_session", "cannot substitute", "durable_external", "cannot establish"}):
        errors.append("host_session and durable_external are conflated")

    security = data[SPEC_DIR / "security_evidence.json"]
    protected = security.get("profiles", {}).get("protected_authorization", {})
    if set(protected.get("required_properties", [])) != PROTECTED_AUTH_PROPERTIES:
        errors.append("protected authorization continuity evidence is incomplete")
    if protected.get("model_or_conversation_fallback_allowed") is not False:
        errors.append("protected authorization permits model or conversation fallback")
    if protected.get("ordinary_continuity_receipt_sufficient") is not False:
        errors.append("ordinary continuity receipt is promoted to protected authorization evidence")
    if security.get("sur011_state") != "unresolved_security_policy_input":
        errors.append("SUR-011 is resolved by BC-030")

    profile = data[SPEC_DIR / "local_mirror_profile.json"]
    if profile.get("implementation_status") != "specification_only_no_provider_implementation":
        errors.append("Local Mirror profile claims a provider implementation")
    expected_hash = "77745fa1fa726859edd0caf496241c2ba930e653a86a23ba0b2792ff9e8717f2"
    if profile.get("reference_archive", {}).get("sha256") != expected_hash:
        errors.append("Local Mirror reference archive identity changed")
    forbidden_refs = set(profile.get("portability_contract", {}).get("forbidden_references", []))
    if not {"drive-letter absolute path", "UNC absolute path", "file URI", "POSIX absolute path"}.issubset(forbidden_refs):
        errors.append("Local Mirror portability contract permits absolute paths")
    if not _contains_all(profile.get("conformance_rule", ""), {"future", "schemas", "if-continuity-provider", "real", "evidence", "not"}):
        errors.append("reference corpus can self-certify provider conformance")
    unproven = " ".join(profile.get("not_proven_by_reference", []))
    if not _contains_all(unproven, {"durable", "receipt", "availability", "protected authorization", "rollback"}):
        errors.append("Local Mirror reference overclaims durable or security evidence")

    sur007 = data[SPEC_DIR / "sur007_disposition.json"]
    if sur007.get("disposition") != "resolved_at_generic_continuity_contract_level":
        errors.append("SUR-007 lacks a BC-030 contract disposition")
    if sur007.get("implementation_authorized") is not False:
        errors.append("SUR-007 disposition authorizes implementation")
    if sur007.get("sur011_state") != "unresolved_security_policy_input":
        errors.append("SUR-011 is resolved in SUR-007 disposition")
    if not _contains_all(sur007.get("deletion", ""), {"no delete", "destroy", "failure", "not"}):
        errors.append("SUR-007 disposition invents deletion semantics")

    source_sur007 = next(
        (item for item in unresolved.get("items", []) if item.get("id") == "SUR-007"), None
    )
    if source_sur007 is None:
        errors.append("source SUR-007 record is missing")
    source_sur011 = next(
        (item for item in unresolved.get("items", []) if item.get("id") == "SUR-011"), None
    )
    if source_sur011 is None:
        errors.append("source SUR-011 record is missing")

    try:
        installed_jsonschema = importlib.metadata.version("jsonschema")
    except importlib.metadata.PackageNotFoundError:
        errors.append("selected jsonschema runtime is not installed")
    else:
        if installed_jsonschema != "4.26.0":
            errors.append(f"selected jsonschema runtime version mismatch: {installed_jsonschema}")

    errors.extend(_validate_schema_instances(root, data))
    errors.extend(_validate_golden(root))
    errors.extend(_validate_git_scope(root))
    errors.extend(_validate_no_implementation_tree(root))
    errors.extend(_validate_manifest_coverage(root))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    errors = validate(args.root.resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"continuity contract validation failed: {len(errors)} error(s)")
        return 1
    print("continuity contract validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
