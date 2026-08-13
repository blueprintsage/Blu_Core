"""Pre-ingress Security Restraint and protected-policy boot gate.

Implements `contracts/security/opsec/minimum_contract.json` v1.3.0. This module
owns protected-policy loading and ingress OPSEC enforcement. Only
SecurityDecision PASS may reach Turn Controller.

Provenance construction (BC-050 §5.3) is bounded and single-pass. The BC-041-C1
conformance reference renormalizes both halves of the candidate for every
removed `Cf` code point, which is quadratic in the number of removals; a
`Cf`-saturated candidate is attacker-influenced, so production must not
reproduce that shape. Semantics are unchanged and are pinned by the
differential-equivalence tests in `tests/runtime_phase1`.

The model is never consulted here. Inference is not authentication,
conversation familiarity is not authorization, and the local model never
decides whether protected ingress may proceed.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import re
import unicodedata
from bisect import bisect_right
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

from jsonschema import Draft202012Validator

from blu_runtime.contracts.models import BLOCK, PASS, SecurityDecision

POLICY_SCHEMA = Path("contracts/security/opsec/schemas/protected_policy.schema.json")

SEPARATORS = frozenset(".,:;-_/\\|")
REDACTION_REPLACEMENT = "[protected content omitted]"
CF_MATCH_VIEW_NAME = "cf_removed_separator_tolerant"

# OPSEC safe error codes. Canon and provider failures use their own runtime
# vocabulary and are deliberately absent from this set.
POLICY_REF_MISSING = "POLICY_REF_MISSING"
POLICY_TARGET_UNAVAILABLE = "POLICY_TARGET_UNAVAILABLE"
POLICY_MALFORMED = "POLICY_MALFORMED"
POLICY_SCHEMA_INVALID = "POLICY_SCHEMA_INVALID"
POLICY_INTEGRITY_MISMATCH = "POLICY_INTEGRITY_MISMATCH"
POLICY_UNUSABLE = "POLICY_UNUSABLE"
INPUT_INVALID = "INPUT_INVALID"
INGRESS_PROTECTED_MATCH = "INGRESS_PROTECTED_MATCH"
EGRESS_PROTECTED_MATCH = "EGRESS_PROTECTED_MATCH"
EGRESS_REDACTION_INVALID = "EGRESS_REDACTION_INVALID"

POLICY_STAGES = (
    "reference_configured",
    "target_located",
    "payload_loaded",
    "schema_validated",
    "integrity_validated",
    "policy_usable",
)


# --------------------------------------------------------------------------
# Normalization and bounded provenance
# --------------------------------------------------------------------------


def _map_separators(value: str) -> str:
    """Map Unicode whitespace and the bounded separator set to ASCII space."""
    return "".join(" " if char.isspace() or char in SEPARATORS else char for char in value)


def _collapse(value: str) -> str:
    return " ".join(value.split())


def _normalize_pipeline(value: str) -> str:
    """The contract's ordered normalization steps, applied to Cf-removed text."""
    return _collapse(_map_separators(unicodedata.normalize("NFKC", value)))


def _collapsed_prefix_lengths(spaced: str) -> list[int]:
    """P[w] = len(collapse(spaced[:w])) for every w, in one pass."""
    lengths = [0] * (len(spaced) + 1)
    settled = 0  # collapsed length of all completed words
    current = 0  # length of the in-progress word
    for index, char in enumerate(spaced):
        lengths[index] = settled + (1 if settled and current else 0) + current
        if char == " ":
            if current:
                settled += (1 if settled else 0) + current
                current = 0
        else:
            current += 1
    lengths[len(spaced)] = settled + (1 if settled and current else 0) + current
    return lengths


def _collapsed_suffix_lengths(spaced: str) -> list[int]:
    """S[w] = len(collapse(spaced[w:])) for every w, in one reverse pass."""
    lengths = [0] * (len(spaced) + 1)
    settled = 0
    current = 0
    for index in range(len(spaced) - 1, -1, -1):
        char = spaced[index]
        if char == " ":
            if current:
                settled += (1 if settled else 0) + current
                current = 0
        else:
            current += 1
        lengths[index] = settled + (1 if settled and current else 0) + current
    lengths[len(spaced)] = 0
    return lengths


def _starter_chunks(text: str) -> list[tuple[int, int]]:
    """Split at Unicode starters so NFKC can be composed chunk-wise."""
    starts = [index for index, char in enumerate(text) if index == 0 or unicodedata.combining(char) == 0]
    if not starts:
        return [(0, len(text))] if text else []
    return [
        (start, starts[position + 1] if position + 1 < len(starts) else len(text))
        for position, start in enumerate(starts)
    ]


def normalized_match_candidate(value: Any) -> dict[str, Any]:
    """Return one Cf-removed candidate plus its removed-boundary provenance.

    Behaviourally identical to the BC-041-C1 reference, computed in bounded
    time. The reference asks, for each removal, whether normalizing the prefix
    and the suffix independently reconstructs the whole normalization and
    agrees on one offset. That predicate is equivalent to asking whether the
    collapsed prefix and collapsed suffix lengths sum to the whole length --
    i.e. whether removing the `Cf` welded two non-space runs together. Both
    length arrays are precomputed in single passes, so each removal costs O(1).
    """
    if not isinstance(value, str):
        raise TypeError("OPSEC candidate must be Unicode text")

    characters: list[str] = []
    raw_boundaries: set[int] = set()
    for char in value:
        if unicodedata.category(char) == "Cf":
            raw_boundaries.add(len(characters))
        else:
            characters.append(char)
    cf_removed = "".join(characters)

    normalized_nfkc = unicodedata.normalize("NFKC", cf_removed)
    spaced = _map_separators(normalized_nfkc)
    normalized = _collapse(spaced)

    if not raw_boundaries:
        return {
            "name": CF_MATCH_VIEW_NAME,
            "normalized": normalized,
            "removed_cf_boundaries": [],
        }

    chunks = _starter_chunks(cf_removed)
    chunk_parts = [unicodedata.normalize("NFKC", cf_removed[start:end]) for start, end in chunks]
    composable = "".join(chunk_parts) == normalized_nfkc

    chunk_starts: list[int] = []
    chunk_offsets: dict[int, tuple[int, int, int, str]] = {}
    running = 0
    for (start, end), part in zip(chunks, chunk_parts):
        chunk_starts.append(start)
        chunk_offsets[start] = (running, start, end, part)
        running += len(part)

    prefix_lengths = _collapsed_prefix_lengths(spaced)
    suffix_lengths = _collapsed_suffix_lengths(spaced)
    total = len(normalized)

    boundaries: set[int] = set()
    for boundary in sorted(raw_boundaries):
        position = _nfkc_position(boundary, cf_removed, normalized_nfkc, composable, chunk_starts, chunk_offsets)
        if position is not None and prefix_lengths[position] + suffix_lengths[position] == total:
            boundaries.add(prefix_lengths[position])
        elif boundary == 0:
            boundaries.add(0)
        elif boundary == len(cf_removed):
            boundaries.add(total)

    return {
        "name": CF_MATCH_VIEW_NAME,
        "normalized": normalized,
        "removed_cf_boundaries": sorted(boundaries),
    }


def _nfkc_position(
    boundary: int,
    cf_removed: str,
    normalized_nfkc: str,
    composable: bool,
    chunk_starts: Sequence[int],
    chunk_offsets: Mapping[int, tuple[int, int, int, str]],
) -> int | None:
    """Map a Cf-removed index onto the NFKC string, or None when unclean.

    Returning None reproduces the reference's conservative drop: when NFKC does
    not split cleanly at the boundary, the reference's prefix/suffix agreement
    test fails and the offset is discarded.
    """
    if not composable:
        return None
    if boundary == len(cf_removed):
        return len(normalized_nfkc)
    if boundary in chunk_offsets:
        return chunk_offsets[boundary][0]
    index = bisect_right(chunk_starts, boundary) - 1
    if index < 0:
        return None
    chunk_offset, start, end, part = chunk_offsets[chunk_starts[index]]
    segment = cf_removed[start:end]
    inner = boundary - start
    head = unicodedata.normalize("NFKC", segment[:inner])
    tail = unicodedata.normalize("NFKC", segment[inner:])
    if head + tail != part:
        return None
    return chunk_offset + len(head)


def normalize_rule_text(value: Any) -> str:
    """Canonicalize a Cf-free policy rule through the bounded text pipeline."""
    if not isinstance(value, str):
        raise TypeError("OPSEC rule value must be Unicode text")
    return _normalize_pipeline(value)


# --------------------------------------------------------------------------
# Matching
# --------------------------------------------------------------------------


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


def _is_word(character: str) -> bool:
    return bool(re.match(r"\w", character, re.UNICODE))


def collect_matches(candidate: dict[str, Any] | str, policy: dict[str, Any], phase: str) -> list[dict[str, Any]]:
    """Evaluate every applicable rule against one candidate view.

    Separator tolerance permits normalized rule words to match zero spaces, so
    rule words stay recoverable when `Cf` removal destroyed their separation.
    Removed-`Cf` boundary offsets additionally satisfy the word-token guard,
    which is what closes the outer-edge case.
    """
    if isinstance(candidate, dict):
        normalized = candidate["normalized"]
        removed = set(candidate.get("removed_cf_boundaries", ()))
    else:
        normalized = candidate
        removed = set()

    def leading_boundary(start: int) -> bool:
        return start == 0 or not _is_word(normalized[start - 1]) or start in removed

    def trailing_boundary(end: int) -> bool:
        return end == len(normalized) or not _is_word(normalized[end]) or end in removed

    found: list[dict[str, Any]] = []
    for rule in sorted(policy["rules"], key=lambda item: item["rule_ref"]):
        if phase not in rule["applies_to"]:
            continue
        candidate_view, candidate_map = _comparison_view(normalized, rule["case_sensitive"])
        phrase_view, _ = _comparison_view(normalize_rule_text(rule["value"]), rule["case_sensitive"])
        pattern = re.compile(r" *".join(re.escape(token) for token in phrase_view.split(" ")), re.UNICODE)

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


# --------------------------------------------------------------------------
# Protected-policy boot gate
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class PolicyLoad:
    usable: bool
    policy: dict[str, Any] | None
    error_code: str | None
    stages: dict[str, bool]


def validate_policy_usability(policy: dict[str, Any]) -> list[str]:
    """Reject policies whose rules cannot be enforced safely."""
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
    reference: Mapping[str, Any] | None,
    environment: Mapping[str, str],
    schema_path: Path | str = POLICY_SCHEMA,
) -> PolicyLoad:
    """Resolve, load, schema-validate, and integrity-check the protected policy.

    Fails closed. There is deliberately no permissive development fallback: an
    unusable required policy yields terminal UNAVAILABLE and no ordinary user
    text reaches Turn Controller or the model. The policy payload never appears
    in the returned error state.
    """
    stages = {name: False for name in POLICY_STAGES}

    def failure(code: str) -> PolicyLoad:
        return PolicyLoad(usable=False, policy=None, error_code=code, stages=dict(stages))

    if not isinstance(reference, Mapping) or reference.get("kind") != "environment_file":
        return failure(POLICY_REF_MISSING)
    locator_env = reference.get("locator_env")
    sha256_env = reference.get("sha256_env")
    if not isinstance(locator_env, str) or not isinstance(sha256_env, str):
        return failure(POLICY_REF_MISSING)
    stages["reference_configured"] = True

    location = environment.get(locator_env)
    expected_digest = environment.get(sha256_env)
    if not location or not expected_digest or not re.fullmatch(r"[0-9a-fA-F]{64}", expected_digest):
        return failure(POLICY_TARGET_UNAVAILABLE)
    target = Path(location)
    if not target.is_file():
        return failure(POLICY_TARGET_UNAVAILABLE)
    stages["target_located"] = True

    try:
        payload = target.read_bytes()
    except OSError:
        return failure(POLICY_TARGET_UNAVAILABLE)
    stages["payload_loaded"] = True

    try:
        policy = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return failure(POLICY_MALFORMED)

    schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
    if list(Draft202012Validator(schema).iter_errors(policy)):
        return failure(POLICY_SCHEMA_INVALID)
    stages["schema_validated"] = True

    if not hmac.compare_digest(hashlib.sha256(payload).hexdigest(), expected_digest.lower()):
        return failure(POLICY_INTEGRITY_MISMATCH)
    stages["integrity_validated"] = True

    if validate_policy_usability(policy):
        return failure(POLICY_UNUSABLE)
    stages["policy_usable"] = True
    return PolicyLoad(usable=True, policy=policy, error_code=None, stages=dict(stages))


# --------------------------------------------------------------------------
# Evidence and ingress
# --------------------------------------------------------------------------


def safe_evidence(
    phase: str,
    result: str,
    policy: dict[str, Any] | None,
    normalized: str | None,
    rule_refs: Sequence[str],
) -> dict[str, Any]:
    """Build content-safe evidence.

    Only the contract's allowed fields appear. Raw input, matched text, rule
    values, original spans, the HMAC key, and unkeyed protected digests are
    never recorded.
    """
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
        "opaque_rule_refs": sorted(set(rule_refs)),
        "candidate_hmac_sha256": digest,
    }


def evaluate_ingress(text: Any, policy: dict[str, Any] | None, policy_error: str | None = None) -> SecurityDecision:
    """Evaluate raw host input. Only PASS is eligible for Turn Controller."""
    if policy is None:
        return SecurityDecision(
            decision=None,
            eligible_for_turn_controller=False,
            safe_error_code=policy_error or POLICY_UNUSABLE,
            evidence=safe_evidence("ingress", "UNAVAILABLE", None, None, ()),
            terminal_status="UNAVAILABLE",
        )
    try:
        candidate = normalized_match_candidate(text)
    except TypeError:
        return SecurityDecision(
            decision=None,
            eligible_for_turn_controller=False,
            safe_error_code=INPUT_INVALID,
            evidence=safe_evidence("ingress", "INVALID", None, None, ()),
            terminal_status="INVALID",
        )

    normalized = candidate["normalized"]
    matches = collect_matches(candidate, policy, "ingress")
    if matches:
        refs = [item["rule"]["rule_ref"] for item in matches]
        return SecurityDecision(
            decision=BLOCK,
            eligible_for_turn_controller=False,
            safe_error_code=INGRESS_PROTECTED_MATCH,
            evidence=safe_evidence("ingress", BLOCK, policy, normalized, refs),
            terminal_status=BLOCK,
        )
    return SecurityDecision(
        decision=PASS,
        eligible_for_turn_controller=True,
        safe_error_code=None,
        evidence=safe_evidence("ingress", PASS, policy, normalized, ()),
        terminal_status=None,
    )
