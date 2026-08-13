"""Validation and Egress.

One independent validator authorizes one terminal result. Every candidate
assistant text passes through here before public print, under the same
protected policy and the same Cf-removed, separator-tolerant, outer-boundary
provenance semantics used at ingress. LM Studio cannot bypass this stage.
"""

from __future__ import annotations

from typing import Any

from blu_runtime.contracts.models import INVALID, UNAVAILABLE, ValidationResult
from blu_runtime.core.security_restraint import (
    EGRESS_PROTECTED_MATCH,
    EGRESS_REDACTION_INVALID,
    INPUT_INVALID,
    POLICY_UNUSABLE,
    REDACTION_REPLACEMENT,
    collect_matches,
    normalized_match_candidate,
    safe_evidence,
)

CLEAR = "CLEAR"
REDACTED = "REDACTED"
BLOCKED = "BLOCKED"


def _has_overlapping_spans(matches: list[dict[str, Any]]) -> bool:
    return any(current["start"] < previous["end"] for previous, current in zip(matches, matches[1:]))


def evaluate_egress(
    request_id: str,
    text: Any,
    policy: dict[str, Any] | None,
    policy_error: str | None = None,
) -> ValidationResult:
    """Clear, redact, or withhold one candidate assistant text."""
    if policy is None:
        return ValidationResult(
            request_id=request_id,
            egress_result=UNAVAILABLE,
            eligible_for_print=False,
            public_output=None,
            safe_error_code=policy_error or POLICY_UNUSABLE,
            evidence=safe_evidence("egress", UNAVAILABLE, None, None, ()),
        )
    try:
        candidate = normalized_match_candidate(text)
    except TypeError:
        return ValidationResult(
            request_id=request_id,
            egress_result=INVALID,
            eligible_for_print=False,
            public_output=None,
            safe_error_code=INPUT_INVALID,
            evidence=safe_evidence("egress", INVALID, None, None, ()),
        )

    normalized = candidate["normalized"]
    matches = collect_matches(candidate, policy, "egress")
    refs = [item["rule"]["rule_ref"] for item in matches]

    if not matches:
        return ValidationResult(
            request_id=request_id,
            egress_result=CLEAR,
            eligible_for_print=True,
            public_output=text,
            safe_error_code=None,
            evidence=safe_evidence("egress", CLEAR, policy, normalized, ()),
        )

    def blocked(code: str) -> ValidationResult:
        return ValidationResult(
            request_id=request_id,
            egress_result=BLOCKED,
            eligible_for_print=False,
            public_output=None,
            safe_error_code=code,
            evidence=safe_evidence("egress", BLOCKED, policy, normalized, refs),
        )

    # Redaction is authorized only when every matched rule permits it.
    if any(item["rule"]["egress_action"] == "BLOCK" for item in matches):
        return blocked(EGRESS_PROTECTED_MATCH)

    if _has_overlapping_spans(matches):
        return blocked(EGRESS_REDACTION_INVALID)

    pieces: list[str] = []
    cursor = 0
    for item in matches:
        pieces.extend((normalized[cursor:item["start"]], REDACTION_REPLACEMENT))
        cursor = item["end"]
    pieces.append(normalized[cursor:])

    # The public form is the canonicalized candidate only. The raw candidate is
    # never reconstructed for print.
    redacted = " ".join("".join(pieces).split())
    residual = redacted.replace(REDACTION_REPLACEMENT, "")
    rescanned = collect_matches(normalized_match_candidate(redacted), policy, "egress")

    if not any(char.isalnum() for char in residual) or rescanned:
        return blocked(EGRESS_REDACTION_INVALID)

    return ValidationResult(
        request_id=request_id,
        egress_result=REDACTED,
        eligible_for_print=True,
        public_output=redacted,
        safe_error_code=None,
        evidence=safe_evidence("egress", REDACTED, policy, normalized, refs),
    )
