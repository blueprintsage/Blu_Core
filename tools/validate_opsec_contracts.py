#!/usr/bin/env python3
"""Validate BC-041 public OPSEC contracts with synthetic data only.

This module is a nonproduction conformance harness. It deliberately contains no
production policy values, model call, Auth implementation, or runtime adapter.
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import re
import sys
import tempfile
import unicodedata
from pathlib import Path
from typing import Any, Mapping

from jsonschema import Draft202012Validator


CONTRACT_ROOT = Path("contracts/security/opsec")
POLICY_SCHEMA = CONTRACT_ROOT / "schemas/protected_policy.schema.json"
EVALUATION_SCHEMA = CONTRACT_ROOT / "schemas/security_evaluation.schema.json"
SYNTHETIC_POLICY = Path("tests/security/fixtures/synthetic_policy.json")
SYNTHETIC_CASES = Path("tests/security/fixtures/synthetic_cases.json")
REQUIRED = {
    CONTRACT_ROOT / "README.md",
    CONTRACT_ROOT / "minimum_contract.json",
    POLICY_SCHEMA,
    EVALUATION_SCHEMA,
    SYNTHETIC_POLICY,
    SYNTHETIC_CASES,
    Path("readiness/schemas/runtime_config.schema.json"),
    Path("readiness/phase1_executable_slice.json"),
    Path("readiness/python_phase1_readiness_checklist.json"),
    Path("readiness/implementation_blocker_dispositions.json"),
    Path("contracts/successor/component_registry.json"),
    Path("contracts/successor/packet_registry.json"),
    Path("contracts/successor/interface_registry.json"),
    Path("contracts/successor/unresolved_register.json"),
    Path("docs/domains/runtime/assignments/BC-041/assignment.md"),
    Path("docs/domains/runtime/assignments/BC-041/handoff.md"),
    Path("docs/domains/runtime/assignments/BC-041/validation.md"),
    Path("docs/domains/runtime/assignments/BC-041/review.md"),
    Path("docs/domains/runtime/assignments/BC-041-C1/assignment.md"),
    Path("docs/domains/runtime/assignments/BC-041-C1/handoff.md"),
    Path("docs/domains/runtime/assignments/BC-041-C1/validation.md"),
    Path("docs/domains/runtime/assignments/BC-041-C1/review.md"),
}
SYNTHETIC_NOTICE = "synthetic test policy != production protected policy"
REDACTION_REPLACEMENT = "[protected content omitted]"
SEPARATORS = frozenset(".,:;-_/\\|")
SECURITY_DECISIONS = ["PASS", "BLOCK", "ASK"]
EGRESS_RESULTS = ["CLEAR", "REDACTED", "BLOCKED", "UNAVAILABLE", "INVALID"]
CF_MATCH_VIEW_NAME = "cf_removed_separator_tolerant"
REQUIRED_CF_CODE_POINTS = ["U+200B", "U+00AD", "U+200D", "U+200C", "U+FEFF", "U+2060"]
REQUIRED_CF_INTERIOR_POSITIONS = ["boundary", "inside_token", "mixed"]
REQUIRED_CF_OUTER_EDGE_POSITIONS = ["leading_outer_edge", "trailing_outer_edge", "both_outer_edges"]
REQUIRED_CF_POSITIONS = REQUIRED_CF_INTERIOR_POSITIONS + REQUIRED_CF_OUTER_EDGE_POSITIONS
REQUIRED_CF_ATTACK_CLASSES = {
    "outer_edge_plus_interior_mixed",
    "mixed_code_point_outer_edge",
    "repeated_outer_edge",
    "outer_edge_plus_repeated_interior",
    "unseparated_self_repetition",
}
SAFE_ERROR_CODES = {
    "POLICY_REF_MISSING",
    "POLICY_TARGET_UNAVAILABLE",
    "POLICY_MALFORMED",
    "POLICY_SCHEMA_INVALID",
    "POLICY_INTEGRITY_MISMATCH",
    "POLICY_UNUSABLE",
    "INPUT_INVALID",
    "INGRESS_PROTECTED_MATCH",
    "EGRESS_PROTECTED_MATCH",
    "EGRESS_REDACTION_INVALID",
}


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _normalize_existing_pipeline(value: str) -> str:
    """Apply the pre-C1 deterministic normalization pipeline."""
    normalized = unicodedata.normalize("NFKC", value)
    separated = "".join(" " if char.isspace() or char in SEPARATORS else char for char in normalized)
    return " ".join(separated.split())


def normalized_match_candidate(value: str) -> dict[str, Any]:
    """Return one Cf-removed candidate plus its removed-boundary provenance."""
    if not isinstance(value, str):
        raise TypeError("OPSEC candidate must be Unicode text")
    characters: list[str] = []
    raw_cf_boundaries: set[int] = set()
    for char in value:
        if unicodedata.category(char) == "Cf":
            raw_cf_boundaries.add(len(characters))
        else:
            characters.append(char)
    cf_removed = "".join(characters)
    normalized = _normalize_existing_pipeline(cf_removed)
    normalized_cf_boundaries: set[int] = set()
    for boundary in raw_cf_boundaries:
        left = _normalize_existing_pipeline(cf_removed[:boundary])
        right = _normalize_existing_pipeline(cf_removed[boundary:])
        left_position = len(left) if normalized.startswith(left) else None
        right_position = len(normalized) - len(right) if normalized.endswith(right) else None
        if left_position is not None and left_position == right_position:
            normalized_cf_boundaries.add(left_position)
        elif boundary == 0:
            normalized_cf_boundaries.add(0)
        elif boundary == len(cf_removed):
            normalized_cf_boundaries.add(len(normalized))
    return {
        "name": CF_MATCH_VIEW_NAME,
        "normalized": normalized,
        "removed_cf_boundaries": sorted(normalized_cf_boundaries),
    }


def normalize_rule_text(value: str) -> str:
    """Canonicalize a Cf-free policy rule through the bounded text pipeline."""
    if not isinstance(value, str):
        raise TypeError("OPSEC rule value must be Unicode text")
    return _normalize_existing_pipeline(value)


def _comparison_view(normalized: str, case_sensitive: bool) -> tuple[str, list[int]]:
    if case_sensitive:
        return normalized, list(range(len(normalized)))
    characters: list[str] = []
    source_indexes: list[int] = []
    for index, char in enumerate(normalized):
        folded = char.casefold()
        characters.append(folded)
        source_indexes.extend([index] * len(folded))
    return "".join(characters), source_indexes


def _matches(candidate: str | dict[str, Any], policy: dict[str, Any], phase: str) -> list[dict[str, Any]]:
    if isinstance(candidate, dict):
        normalized = candidate["normalized"]
        removed_cf_boundaries = set(candidate.get("removed_cf_boundaries", []))
    else:
        normalized = candidate
        removed_cf_boundaries = set()

    def is_word(character: str) -> bool:
        return bool(re.match(r"\w", character, re.UNICODE))

    def leading_boundary(start: int) -> bool:
        return start == 0 or not is_word(normalized[start - 1]) or start in removed_cf_boundaries

    def trailing_boundary(end: int) -> bool:
        return end == len(normalized) or not is_word(normalized[end]) or end in removed_cf_boundaries

    found: list[dict[str, Any]] = []
    for rule in sorted(policy["rules"], key=lambda item: item["rule_ref"]):
        if phase not in rule["applies_to"]:
            continue
        candidate_view, candidate_map = _comparison_view(normalized, rule["case_sensitive"])
        phrase = normalize_rule_text(rule["value"])
        phrase_view, _ = _comparison_view(phrase, rule["case_sensitive"])
        separator_tolerant_phrase = r" *".join(re.escape(token) for token in phrase_view.split(" "))
        pattern = re.compile(separator_tolerant_phrase, re.UNICODE)
        rule_matches: list[dict[str, Any]] = []
        for match in pattern.finditer(candidate_view):
            start = candidate_map[match.start()]
            end = candidate_map[match.end() - 1] + 1
            rule_matches.append({"rule": rule, "start": start, "end": end})

        accepted: set[tuple[int, int]] = {
            (item["start"], item["end"])
            for item in rule_matches
            if leading_boundary(item["start"]) and trailing_boundary(item["end"])
        }
        run_start = 0
        while run_start < len(rule_matches):
            run_end = run_start + 1
            while run_end < len(rule_matches) and rule_matches[run_end - 1]["end"] == rule_matches[run_end]["start"]:
                run_end += 1
            run = rule_matches[run_start:run_end]
            if len(run) > 1 and leading_boundary(run[0]["start"]) and trailing_boundary(run[-1]["end"]):
                accepted.update((item["start"], item["end"]) for item in run)
            run_start = run_end
        found.extend(item for item in rule_matches if (item["start"], item["end"]) in accepted)
    return sorted(found, key=lambda item: (item["start"], item["end"], item["rule"]["rule_ref"]))


def validate_policy_usability(policy: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    refs = [rule.get("rule_ref") for rule in policy.get("rules", [])]
    if len(refs) != len(set(refs)):
        errors.append("policy rule_ref values are not unique")
    seen: set[tuple[str, bool, str]] = set()
    replacement = normalize_rule_text(REDACTION_REPLACEMENT).casefold()
    for rule in policy.get("rules", []):
        raw_value = rule.get("value")
        if isinstance(raw_value, str) and any(unicodedata.category(char) == "Cf" for char in raw_value):
            errors.append(f"policy rule contains a forbidden Cf code point: {rule.get('rule_ref')}")
        try:
            value = normalize_rule_text(raw_value)
        except TypeError:
            continue
        if not value or not any(char.isalnum() for char in value):
            errors.append(f"policy rule is not usable: {rule.get('rule_ref')}")
            continue
        comparison, _ = _comparison_view(value, bool(rule.get("case_sensitive")))
        compact_value = "".join(char for char in comparison.casefold() if char.isalnum())
        compact_ref = "".join(char for char in str(rule.get("rule_ref", "")).casefold() if char.isalnum())
        if compact_value and compact_value in compact_ref:
            errors.append(f"policy rule_ref is not opaque: {rule.get('rule_ref')}")
        if comparison.casefold() == replacement:
            errors.append(f"policy rule conflicts with redaction replacement: {rule.get('rule_ref')}")
        for phase in rule.get("applies_to", []):
            key = (comparison, bool(rule.get("case_sensitive")), phase)
            if key in seen:
                errors.append(f"policy contains duplicate normalized rule for {phase}")
            seen.add(key)
    return errors


def load_policy(
    reference: dict[str, Any] | None,
    environment: Mapping[str, str],
    policy_schema: dict[str, Any],
) -> dict[str, Any]:
    """Resolve an environment-file reference and return content-safe load state."""
    stages = {
        "reference_configured": False,
        "target_located": False,
        "payload_loaded": False,
        "schema_validated": False,
        "integrity_validated": False,
        "policy_usable": False,
    }

    def failure(code: str) -> dict[str, Any]:
        return {"usable": False, "policy": None, "error_code": code, "stages": stages}

    if not isinstance(reference, dict) or reference.get("kind") != "environment_file":
        return failure("POLICY_REF_MISSING")
    locator_env = reference.get("locator_env")
    sha256_env = reference.get("sha256_env")
    if not isinstance(locator_env, str) or not isinstance(sha256_env, str):
        return failure("POLICY_REF_MISSING")
    stages["reference_configured"] = True
    location = environment.get(locator_env)
    expected_digest = environment.get(sha256_env)
    if not location or not expected_digest or not re.fullmatch(r"[0-9a-fA-F]{64}", expected_digest):
        return failure("POLICY_TARGET_UNAVAILABLE")
    target = Path(location)
    if not target.is_file():
        return failure("POLICY_TARGET_UNAVAILABLE")
    stages["target_located"] = True
    try:
        payload = target.read_bytes()
    except OSError:
        return failure("POLICY_TARGET_UNAVAILABLE")
    stages["payload_loaded"] = True
    try:
        policy = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return failure("POLICY_MALFORMED")
    if list(Draft202012Validator(policy_schema).iter_errors(policy)):
        return failure("POLICY_SCHEMA_INVALID")
    stages["schema_validated"] = True
    if not hmac.compare_digest(hashlib.sha256(payload).hexdigest(), expected_digest.lower()):
        return failure("POLICY_INTEGRITY_MISMATCH")
    stages["integrity_validated"] = True
    if validate_policy_usability(policy):
        return failure("POLICY_UNUSABLE")
    stages["policy_usable"] = True
    return {"usable": True, "policy": policy, "error_code": None, "stages": stages}


def _evidence(phase: str, result: str, policy: dict[str, Any] | None, normalized: str | None, refs: list[str]) -> dict[str, Any]:
    digest = None
    revision = None
    if policy is not None and normalized is not None:
        revision = policy["revision"]
        digest = hmac.new(
            policy["evidence_hmac_key"].encode("utf-8"),
            normalized.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
    return {
        "evaluation_phase": phase,
        "result": result,
        "policy_revision": revision,
        "opaque_rule_refs": sorted(set(refs)),
        "candidate_hmac_sha256": digest,
    }


def _failure_evaluation(phase: str, code: str, terminal_status: str = "UNAVAILABLE") -> dict[str, Any]:
    return {
        "phase": phase,
        "security_decision": None,
        "egress_result": "UNAVAILABLE" if terminal_status == "UNAVAILABLE" and phase == "egress" else ("INVALID" if phase == "egress" else None),
        "terminal_status": terminal_status,
        "eligible_for_turn_controller": False,
        "eligible_for_print": False,
        "public_output": None,
        "safe_error_code": code,
        "evidence": _evidence(phase, terminal_status, None, None, []),
        "logs": [{"event": "policy" if code.startswith("POLICY_") else "evaluation", "code": code}],
    }


def evaluate_ingress(text: Any, policy: dict[str, Any] | None, policy_error: str | None = None) -> dict[str, Any]:
    if policy is None:
        return _failure_evaluation("ingress", policy_error or "POLICY_UNUSABLE")
    try:
        candidate = normalized_match_candidate(text)
    except TypeError:
        return _failure_evaluation("ingress", "INPUT_INVALID", "INVALID")
    normalized = candidate["normalized"]
    matches = _matches(candidate, policy, "ingress")
    refs = [item["rule"]["rule_ref"] for item in matches]
    if matches:
        return {
            "phase": "ingress",
            "security_decision": "BLOCK",
            "egress_result": None,
            "terminal_status": None,
            "eligible_for_turn_controller": False,
            "eligible_for_print": False,
            "public_output": None,
            "safe_error_code": "INGRESS_PROTECTED_MATCH",
            "evidence": _evidence("ingress", "BLOCK", policy, normalized, refs),
            "logs": [{"event": "policy", "code": "POLICY_USABLE"}, {"event": "evaluation", "code": "INGRESS_PROTECTED_MATCH"}],
        }
    return {
        "phase": "ingress",
        "security_decision": "PASS",
        "egress_result": None,
        "terminal_status": None,
        "eligible_for_turn_controller": True,
        "eligible_for_print": False,
        "public_output": None,
        "safe_error_code": None,
        "evidence": _evidence("ingress", "PASS", policy, normalized, []),
        "logs": [{"event": "policy", "code": "POLICY_USABLE"}, {"event": "evaluation", "code": "INGRESS_PASS"}],
    }


def _has_overlapping_spans(matches: list[dict[str, Any]]) -> bool:
    return any(current["start"] < previous["end"] for previous, current in zip(matches, matches[1:]))


def evaluate_egress(text: Any, policy: dict[str, Any] | None, policy_error: str | None = None) -> dict[str, Any]:
    if policy is None:
        return _failure_evaluation("egress", policy_error or "POLICY_UNUSABLE")
    try:
        candidate = normalized_match_candidate(text)
    except TypeError:
        return _failure_evaluation("egress", "INPUT_INVALID", "INVALID")
    normalized = candidate["normalized"]
    matches = _matches(candidate, policy, "egress")
    refs = [item["rule"]["rule_ref"] for item in matches]
    base = {
        "phase": "egress",
        "security_decision": None,
        "terminal_status": None,
        "eligible_for_turn_controller": False,
    }
    if not matches:
        return {
            **base,
            "egress_result": "CLEAR",
            "eligible_for_print": True,
            "public_output": text,
            "safe_error_code": None,
            "evidence": _evidence("egress", "CLEAR", policy, normalized, []),
            "logs": [{"event": "policy", "code": "POLICY_USABLE"}, {"event": "evaluation", "code": "EGRESS_CLEAR"}],
        }
    if any(item["rule"]["egress_action"] == "BLOCK" for item in matches):
        return {
            **base,
            "egress_result": "BLOCKED",
            "eligible_for_print": False,
            "public_output": None,
            "safe_error_code": "EGRESS_PROTECTED_MATCH",
            "evidence": _evidence("egress", "BLOCKED", policy, normalized, refs),
            "logs": [{"event": "policy", "code": "POLICY_USABLE"}, {"event": "evaluation", "code": "EGRESS_PROTECTED_MATCH"}],
        }
    if matches and not _has_overlapping_spans(matches):
        pieces: list[str] = []
        cursor = 0
        for item in matches:
            pieces.extend((normalized[cursor:item["start"]], REDACTION_REPLACEMENT))
            cursor = item["end"]
        pieces.append(normalized[cursor:])
        redacted = " ".join("".join(pieces).split())
        residual = redacted.replace(REDACTION_REPLACEMENT, "")
        rescanned = _matches(normalized_match_candidate(redacted), policy, "egress")
        redaction_valid = any(char.isalnum() for char in residual) and not rescanned
        if redaction_valid:
            return {
                **base,
                "egress_result": "REDACTED",
                "eligible_for_print": True,
                "public_output": redacted,
                "safe_error_code": None,
                "evidence": _evidence("egress", "REDACTED", policy, normalized, refs),
                "logs": [{"event": "policy", "code": "POLICY_USABLE"}, {"event": "redaction", "code": "EGRESS_REDACTED"}],
            }
    return {
        **base,
        "egress_result": "BLOCKED",
        "eligible_for_print": False,
        "public_output": None,
        "safe_error_code": "EGRESS_REDACTION_INVALID",
        "evidence": _evidence("egress", "BLOCKED", policy, normalized, refs),
        "logs": [{"event": "policy", "code": "POLICY_USABLE"}, {"event": "redaction", "code": "EGRESS_REDACTION_INVALID"}],
    }


def _loader_matrix(policy: dict[str, Any], policy_schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        valid = root / "policy.json"
        valid_payload = json.dumps(policy, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        valid.write_bytes(valid_payload)
        reference = {"kind": "environment_file", "locator_env": "SYNTH_POLICY_PATH", "sha256_env": "SYNTH_POLICY_SHA256"}
        environment = {"SYNTH_POLICY_PATH": str(valid), "SYNTH_POLICY_SHA256": hashlib.sha256(valid_payload).hexdigest()}
        cases = [
            ("valid", reference, environment, None),
            ("missing_ref", None, environment, "POLICY_REF_MISSING"),
            ("unavailable", reference, {**environment, "SYNTH_POLICY_PATH": str(root / "absent.json")}, "POLICY_TARGET_UNAVAILABLE"),
        ]
        malformed = root / "malformed.json"
        malformed.write_text("{", encoding="utf-8")
        cases.append(("malformed", reference, {"SYNTH_POLICY_PATH": str(malformed), "SYNTH_POLICY_SHA256": hashlib.sha256(b"{").hexdigest()}, "POLICY_MALFORMED"))
        invalid = root / "invalid.json"
        invalid_payload = json.dumps({"schema_version": "1.0.0"}).encode("utf-8")
        invalid.write_bytes(invalid_payload)
        cases.append(("schema_invalid", reference, {"SYNTH_POLICY_PATH": str(invalid), "SYNTH_POLICY_SHA256": hashlib.sha256(invalid_payload).hexdigest()}, "POLICY_SCHEMA_INVALID"))
        cases.append(("integrity", reference, {**environment, "SYNTH_POLICY_SHA256": "0" * 64}, "POLICY_INTEGRITY_MISMATCH"))
        for name, ref, env, expected_error in cases:
            result = load_policy(ref, env, policy_schema)
            if expected_error is None:
                if not result["usable"] or not all(result["stages"].values()):
                    errors.append(f"policy loader case failed: {name}")
            elif result["error_code"] != expected_error or result["usable"]:
                errors.append(f"policy loader case did not fail closed: {name}")
    return errors


def validate(root: Path) -> list[str]:
    missing = [str(path) for path in sorted(REQUIRED) if not (root / path).is_file()]
    if missing:
        return [f"missing required file: {path}" for path in missing]
    errors: list[str] = []
    try:
        contract = _load(root / CONTRACT_ROOT / "minimum_contract.json")
        policy_schema = _load(root / POLICY_SCHEMA)
        evaluation_schema = _load(root / EVALUATION_SCHEMA)
        fixture = _load(root / SYNTHETIC_POLICY)
        cases = _load(root / SYNTHETIC_CASES)
        config_schema = _load(root / "readiness/schemas/runtime_config.schema.json")
        phase1 = _load(root / "readiness/phase1_executable_slice.json")
        checklist = _load(root / "readiness/python_phase1_readiness_checklist.json")
        blocker = _load(root / "readiness/implementation_blocker_dispositions.json")
        components = _load(root / "contracts/successor/component_registry.json")
        packets = _load(root / "contracts/successor/packet_registry.json")
        interfaces = _load(root / "contracts/successor/interface_registry.json")
        unresolved = _load(root / "contracts/successor/unresolved_register.json")
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        return [f"invalid JSON in required OPSEC artifact: {exc}"]

    for schema_name, schema in (("protected policy", policy_schema), ("security evaluation", evaluation_schema)):
        try:
            Draft202012Validator.check_schema(schema)
        except Exception as exc:
            errors.append(f"{schema_name} schema is invalid: {exc}")

    if fixture.get("fixture_notice") != SYNTHETIC_NOTICE or cases.get("fixture_notice") != SYNTHETIC_NOTICE:
        errors.append("synthetic fixture production-separation notice is missing")
    expected_cf_matrix = {
        (code_point, position)
        for code_point in REQUIRED_CF_CODE_POINTS
        for position in REQUIRED_CF_POSITIONS
    }
    for phase in ("ingress", "egress"):
        actual_cf_matrix = {
            (item.get("cf_code_point"), item.get("cf_position"))
            for item in cases.get(phase, [])
            if item.get("cf_code_point") is not None
        }
        if actual_cf_matrix != expected_cf_matrix:
            errors.append(f"{phase} Cf probe matrix is incomplete")
        cross_code_point = [
            item for item in cases.get(phase, [])
            if item.get("cf_position") == "mixed"
            and len(item.get("cf_code_points", [])) > 1
        ]
        if not cross_code_point:
            errors.append(f"{phase} cross-code-point mixed Cf probe is missing")
        attack_classes = {
            item.get("attack_class")
            for item in cases.get(phase, [])
            if item.get("attack_class") is not None
        }
        missing_attack_classes = REQUIRED_CF_ATTACK_CLASSES - attack_classes
        if missing_attack_classes:
            errors.append(f"{phase} outer-edge attack classes are incomplete")
    policy = fixture.get("policy")
    schema_errors = list(Draft202012Validator(policy_schema).iter_errors(policy)) if isinstance(policy, dict) else ["missing"]
    if schema_errors:
        errors.append("synthetic policy does not validate against production schema")
    else:
        errors.extend(validate_policy_usability(policy))
        result_validator = Draft202012Validator(evaluation_schema)
        protected_values = [rule["value"] for rule in policy["rules"]]
        for item in cases.get("ingress", []):
            result = evaluate_ingress(item.get("text"), policy)
            if result.get("security_decision") != item.get("expected"):
                errors.append(f"ingress synthetic case failed: {item.get('id')}")
            if list(result_validator.iter_errors(result)):
                errors.append(f"ingress result schema failed: {item.get('id')}")
            if result.get("security_decision") != "PASS" and result.get("eligible_for_turn_controller"):
                errors.append(f"non-PASS ingress became model-eligible: {item.get('id')}")
            if (item.get("cf_code_point") or item.get("cf_code_points")) and result.get("security_decision") != "BLOCK":
                errors.append(f"Cf ingress probe did not block: {item.get('id')}")
            serialized = json.dumps(result, ensure_ascii=False).casefold()
            if any(normalize_rule_text(value).casefold() in normalized_match_candidate(serialized)["normalized"].casefold() for value in protected_values):
                errors.append(f"protected fixture value leaked through ingress result: {item.get('id')}")
            if policy["evidence_hmac_key"].casefold() in serialized:
                errors.append(f"synthetic evidence key leaked through ingress result: {item.get('id')}")
        for item in cases.get("egress", []):
            result = evaluate_egress(item.get("text"), policy)
            if result.get("egress_result") != item.get("expected") or result.get("eligible_for_print") is not item.get("printable"):
                errors.append(f"egress synthetic case failed: {item.get('id')}")
            if list(result_validator.iter_errors(result)):
                errors.append(f"egress result schema failed: {item.get('id')}")
            if result.get("egress_result") != "CLEAR":
                serialized = json.dumps(result, ensure_ascii=False).casefold()
                if any(normalize_rule_text(value).casefold() in normalized_match_candidate(serialized)["normalized"].casefold() for value in protected_values):
                    errors.append(f"protected fixture value leaked through result: {item.get('id')}")
                if policy["evidence_hmac_key"].casefold() in serialized:
                    errors.append(f"synthetic evidence key leaked through egress result: {item.get('id')}")
            if (item.get("cf_code_point") or item.get("cf_code_points")) and (
                result.get("egress_result") not in {"REDACTED", "BLOCKED"}
                or (result.get("eligible_for_print") and REDACTION_REPLACEMENT not in (result.get("public_output") or ""))
            ):
                errors.append(f"Cf egress probe did not fail safely: {item.get('id')}")
        errors.extend(_loader_matrix(policy, policy_schema))

    if contract.get("security_decision_values") != SECURITY_DECISIONS:
        errors.append("SecurityDecision vocabulary changed")
    if contract.get("egress", {}).get("result_values") != EGRESS_RESULTS:
        errors.append("egress result vocabulary changed")
    if contract.get("matcher", {}).get("model_invocation_allowed") is not False:
        errors.append("OPSEC matcher permits model invocation")
    if contract.get("normalization", {}).get("semantic_paraphrase_detection") is not False:
        errors.append("minimum matcher overclaims semantic paraphrase detection")
    normalization = contract.get("normalization", {})
    if normalization.get("candidate_view", {}).get("id") != CF_MATCH_VIEW_NAME:
        errors.append("normalization does not define the single Cf-removed match candidate")
    if normalization.get("candidate_view_generation_applies_to") != ["ingress", "egress"]:
        errors.append("Cf match candidate does not apply symmetrically to ingress and egress")
    matcher = contract.get("matcher", {})
    if matcher.get("normalized_rule_inter_word_separator_matches") != "zero_or_more_ASCII_spaces":
        errors.append("matcher is not separator-tolerant after deterministic Cf removal")
    if matcher.get("removed_Cf_outer_boundary_provenance") != "normalized_candidate_boundary_offsets":
        errors.append("matcher does not preserve removed-Cf outer-boundary provenance")
    if matcher.get("ordinary_word_adjacency_without_removed_Cf_matches") is not False:
        errors.append("matcher permits ordinary word adjacency without removed-Cf provenance")
    if matcher.get("unseparated_self_repetition_matches") is not True:
        errors.append("matcher does not fail safely on unseparated self-repetition")
    if matcher.get("Cf_placement_combination_enumeration_allowed") is not False:
        errors.append("matcher permits enumerating Cf placement combinations")
    if matcher.get("candidate_count_growth_with_Cf_insertions") != "constant_one":
        errors.append("matcher candidate count can grow with Cf insertion count")
    exclusion_text = " ".join(contract.get("scope_exclusions", [])).casefold()
    if "confusable" not in exclusion_text or "homoglyph" not in exclusion_text:
        errors.append("general Unicode confusable/homoglyph substitution is not explicitly excluded")
    if "non-cf" not in exclusion_text or "default-ignorable" not in exclusion_text or "invisible" not in exclusion_text:
        errors.append("non-Cf default-ignorable/invisible limitation is not explicitly excluded")
    readme = (root / CONTRACT_ROOT / "README.md").read_text(encoding="utf-8").casefold()
    if "confusable" not in readme or "homoglyph" not in readme:
        errors.append("OPSEC README does not state the confusable/homoglyph limitation")
    if "non-`cf`" not in readme or "default-ignorable" not in readme or "invisible" not in readme:
        errors.append("OPSEC README does not state the non-Cf invisible limitation")
    if set(contract.get("safe_error_codes", [])) != SAFE_ERROR_CODES:
        errors.append("safe error-code vocabulary is incomplete")
    architecture = contract.get("architecture", {})
    if any(architecture.get(field) is not False for field in ("component_added", "packet_added", "interface_added", "route_added")):
        errors.append("OPSEC mechanism changes the successor architecture")

    protected_ref = config_schema.get("properties", {}).get("runtime", {}).get("properties", {}).get("protected_policy_ref", {})
    if protected_ref.get("type") != "object" or protected_ref.get("properties", {}).get("kind", {}).get("const") != "environment_file":
        errors.append("runtime protected_policy_ref is not a portable environment-file reference")
    serialized_config = json.dumps(config_schema)
    if re.search(r"(?:[A-Za-z]:\\\\|/home/|file://)", serialized_config):
        errors.append("runtime configuration embeds a machine-specific policy path")
    if "rules" in protected_ref.get("properties", {}) or "value" in protected_ref.get("properties", {}):
        errors.append("runtime configuration can embed protected policy values")

    if len(components.get("components", [])) != 7 or len(packets.get("packets", [])) != 8 or len(interfaces.get("interfaces", [])) != 9:
        errors.append("successor architecture is not 7 components / 8 packets / 9 interfaces")
    if phase1.get("opsec_contract_ref") != "contracts/security/opsec/minimum_contract.json":
        errors.append("Phase 1 slice does not bind the BC-041 OPSEC contract")
    required_turn_steps = {"pre_ingress_opsec_normalize_and_match", "egress_opsec_normalize_match_and_redact_or_block"}
    if not required_turn_steps.issubset(phase1.get("turn_sequence", [])):
        errors.append("Phase 1 slice does not gate both ingress and egress")

    sur001 = next((item for item in blocker.get("dispositions", []) if item.get("id") == "SUR-001"), {})
    unresolved_sur001 = next((item for item in unresolved.get("items", []) if item.get("id") == "SUR-001"), {})
    if sur001.get("disposition") != "resolved_at_minimum_phase1_contract_level" or sur001.get("phase1_resolved") is not True:
        errors.append("SUR-001 readiness disposition is not resolved at the bounded contract level")
    if unresolved_sur001.get("disposition") != "resolved_at_minimum_phase1_contract_level" or unresolved_sur001.get("blocking_for_implementation") is not False:
        errors.append("SUR-001 successor register disposition is stale")
    if blocker.get("actual_blockers") != [] or blocker.get("phase1_gate_result") != "ready_for_python_phase1":
        errors.append("blocker contract disagrees with resolved SUR-001")
    checks = {item.get("id"): item for item in checklist.get("checks", [])}
    if checks.get("minimum_OPSEC_match_and_redaction_contract_available", {}).get("status") != "pass":
        errors.append("readiness checklist has not passed the OPSEC contract gate")
    if checklist.get("result") != "ready_for_python_phase1" or checklist.get("actual_blockers") != []:
        errors.append("readiness result disagrees with resolved SUR-001")
    if checklist.get("runtime_phase1_packet_may_be_authored_next") is not True:
        errors.append("readiness does not permit the next packet to be authored")
    review = checklist.get("independent_correction_review", {})
    if checks.get("independent_Claude_correction_review", {}).get("status") != "pass":
        errors.append("independent correction review check is not complete")
    if review.get("state") != "complete" or review.get("completed") is not True:
        errors.append("independent correction review completion is not recorded")
    if review.get("review_commit") != "f0998f78aaada899a16d4413170ef3689f04fe28":
        errors.append("independent correction review commit is not the approved final review")
    if review.get("disposition") != "approve-with-notes" or review.get("blocking_findings") != 0:
        errors.append("independent correction review disposition is not approve-with-notes with zero blockers")
    if review.get("required_before_implementation_authorization") is not True:
        errors.append("independent correction review is not required before implementation authorization")
    closure = checklist.get("dad_blu_closure", {})
    if checks.get("BC_041_and_BC_041_C1_Dad_Blu_closure", {}).get("status") != "pass":
        errors.append("BC-041 and BC-041-C1 closure check is not complete")
    if closure.get("state") != "complete" or closure.get("assignments") != ["BC-041", "BC-041-C1"]:
        errors.append("Dad/Blu closure does not cover both BC-041 assignments")
    if closure.get("correction_tip") != "204a229e2c01b255f1a940129cb724fa33fb4755":
        errors.append("Dad/Blu closure does not bind the reviewed correction tip")
    if closure.get("review_source_commit") != "f0998f78aaada899a16d4413170ef3689f04fe28":
        errors.append("Dad/Blu closure does not bind the final Claude review")
    if checklist.get("implementation_authorized") is not False:
        errors.append("readiness checklist authorizes implementation without separate runtime authorization")
    if checklist.get("automatic_start_prohibited") is not True or phase1.get("implementation_authorized") is not False:
        errors.append("BC-041 improperly starts or authorizes runtime implementation")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    errors = validate(args.root.resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"OPSEC contract validation failed: {len(errors)} error(s)")
        return 1
    print("OPSEC contract validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
