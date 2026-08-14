"""Typed Phase-1 packets and records.

Non-component support layer (BC-050 §14). Nothing here decides routing,
security, authorization, or truth; these are data carriers between the seven
approved components. Status vocabulary comes from
`contracts/successor/error_model.json`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# Successor error-model statuses.
PASS = "PASS"
BLOCK = "BLOCK"
ASK = "ASK"
UNAVAILABLE = "UNAVAILABLE"
INVALID = "INVALID"
ERROR = "ERROR"

TERMINAL_STATUSES = (PASS, BLOCK, ASK, UNAVAILABLE, INVALID, ERROR)

# SecurityDecision vocabulary is exactly PASS | BLOCK | ASK. Phase 1 cannot
# generate ASK (minimum OPSEC contract maps no_match -> PASS and
# protected_match -> BLOCK with authorization_case_created false), but the
# vocabulary is retained because the successor architecture defines it.
SECURITY_DECISIONS = (PASS, BLOCK, ASK)

EGRESS_RESULTS = ("CLEAR", "REDACTED", "BLOCKED", UNAVAILABLE, INVALID)

# Continuity lifetime vocabulary. Bare "session" is not a substrate.
CONTINUITY_LIFETIMES = ("none", "turn", "host_session", "durable_external")

# Runtime-local canon error codes. Deliberately NOT part of the OPSEC
# safe_error_codes set, which is BC-041 specific and protected.
CANON_SOURCE_UNAVAILABLE = "CANON_SOURCE_UNAVAILABLE"
CANON_SOURCE_INTEGRITY_MISMATCH = "CANON_SOURCE_INTEGRITY_MISMATCH"
CANON_PROJECTION_INVALID = "CANON_PROJECTION_INVALID"

CANON_ERROR_CODES = (
    CANON_SOURCE_UNAVAILABLE,
    CANON_SOURCE_INTEGRITY_MISMATCH,
    CANON_PROJECTION_INVALID,
)

# Runtime-local configuration error code.
CONFIG_INVALID = "CONFIG_INVALID"

# Runtime-local provider error codes.
PROVIDER_ENDPOINT_UNAVAILABLE = "PROVIDER_ENDPOINT_UNAVAILABLE"
PROVIDER_MODEL_ABSENT = "PROVIDER_MODEL_ABSENT"
PROVIDER_MODEL_NOT_LOADED = "PROVIDER_MODEL_NOT_LOADED"
PROVIDER_MODEL_INCOMPATIBLE = "PROVIDER_MODEL_INCOMPATIBLE"
PROVIDER_CONTEXT_UNKNOWN = "PROVIDER_CONTEXT_UNKNOWN"
PROVIDER_CONTEXT_INSUFFICIENT = "PROVIDER_CONTEXT_INSUFFICIENT"
PROVIDER_TIMEOUT = "PROVIDER_TIMEOUT"
PROVIDER_RESPONSE_MALFORMED = "PROVIDER_RESPONSE_MALFORMED"
PROVIDER_IDENTITY_MISMATCH = "PROVIDER_IDENTITY_MISMATCH"
PROVIDER_TOOL_CALL_UNSUPPORTED = "PROVIDER_TOOL_CALL_UNSUPPORTED"
# BC-050-C2 B-04/B-07: completion must be positively evidenced. Absence of a
# terminal observation, an unresolved provider error, or missing provider-bound
# completion evidence are distinct from a malformed body.
PROVIDER_COMPLETION_UNVERIFIED = "PROVIDER_COMPLETION_UNVERIFIED"
PROVIDER_ERROR_REPORTED = "PROVIDER_ERROR_REPORTED"
PROVIDER_COMPLETION_EVIDENCE_MISSING = "PROVIDER_COMPLETION_EVIDENCE_MISSING"

# BC-050-C5: what a completion proof actually rests on. A provider profile
# either assigns a per-completion identifier or it does not; both are truthful,
# and the difference must be stated rather than papered over. Nothing here
# licenses inventing an identifier: `SYNCHRONOUS_RESPONSE` asserts that the
# provider returned a complete synchronous response and assigned no id, which
# is exactly what LM Studio native REST v1 does with `store: false`.
COMPLETION_PROOF_PROVIDER_ID = "provider_assigned_completion_id"
COMPLETION_PROOF_SYNCHRONOUS_RESPONSE = "synchronous_provider_response"

COMPLETION_PROOFS = (COMPLETION_PROOF_PROVIDER_ID, COMPLETION_PROOF_SYNCHRONOUS_RESPONSE)

ROUTE_UNSUPPORTED = "ROUTE_UNSUPPORTED"
SECURITY_DECISION_NOT_EXECUTABLE = "SECURITY_DECISION_NOT_EXECUTABLE"


@dataclass(frozen=True)
class RawHostEvent:
    """One normalized event as received by a host adapter."""

    host: str
    event_id: str
    text: Any


@dataclass(frozen=True)
class HostInput:
    """Host input submitted through the Generic Host Adapter Boundary."""

    host: str
    request_id: str
    text: Any


@dataclass(frozen=True)
class SecurityDecision:
    """Pre-ingress restraint result. Only PASS may reach Turn Controller."""

    decision: str | None
    eligible_for_turn_controller: bool
    safe_error_code: str | None
    evidence: dict[str, Any]
    terminal_status: str | None = None


@dataclass(frozen=True)
class CanonProjection:
    """Verified, byte-exact model-facing envelope."""

    system_prompt_bytes: bytes
    digest: str
    source_digests: dict[str, str]

    @property
    def system_prompt(self) -> str:
        return self.system_prompt_bytes.decode("utf-8")


@dataclass(frozen=True)
class TurnRequest:
    """Turn Controller input for one ordinary conversation turn."""

    request_id: str
    route: str
    text: str


@dataclass(frozen=True)
class ControlDecision:
    """Turn Controller route lock. Phase 1 permits one owner and no effects."""

    request_id: str
    route: str
    owner: str
    scope_lock: str
    side_effects: bool
    status: str
    safe_error_code: str | None = None


@dataclass(frozen=True)
class ProviderObservation:
    """Operationally observed provider evidence. Never derived from config."""

    observation_id: str
    provider_id: str
    endpoint_state: str
    configured_model_key: str | None = None
    observed_model_key: str | None = None
    model_instance_id: str | None = None
    observed_context_length: int | None = None
    usable: bool = False
    safe_error_code: str | None = None
    limitations: tuple[str, ...] = ()


@dataclass(frozen=True)
class ModelExecutionRequest:
    """Request submitted through IF-MODEL-EXECUTION."""

    request_id: str
    model_instance_id: str
    canon_projection_digest: str
    turn_request_ref: str
    control_decision_ref: str
    system_prompt: str
    user_input: str
    context_budget: int
    stream: bool = False
    store: bool = False


@dataclass(frozen=True)
class NormalizedModelResult:
    """Normalized, still-untrusted provider output."""

    request_id: str
    provider_id: str
    model_instance_id: str | None
    status: str
    candidate_text: str | None
    output_kinds: tuple[str, ...]
    safe_error_code: str | None = None
    #: Provider-assigned completion identifier, or None when the provider
    #: profile assigns none. None is never a placeholder for a value that was
    #: expected and lost -- `completion_proof` says which case this is.
    completion_evidence_ref: str | None = None
    #: One of COMPLETION_PROOFS on success. None means the boundary claimed no
    #: completion proof at all, which cannot become a successful turn.
    completion_proof: str | None = None


@dataclass(frozen=True)
class ValidationResult:
    """Validation and Egress outcome."""

    request_id: str
    egress_result: str
    eligible_for_print: bool
    public_output: str | None
    safe_error_code: str | None
    evidence: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ContinuityState:
    """Phase-1 continuity truth. No durable provider exists."""

    lifetime: str = "turn"
    provider_available: bool = False
    durability_claimed: bool = False
    reason: str = "no continuity provider is configured in Phase 1"


@dataclass(frozen=True)
class TerminalPacket:
    """The single authorized terminal result for one turn."""

    request_id: str
    status: str
    public_output: str | None
    safe_error_code: str | None
    model_invoked: bool
    tool_executed: bool = False
    continuity: ContinuityState = field(default_factory=ContinuityState)


@dataclass(frozen=True)
class TurnReceipt:
    """Current-turn evidence binding. Proves only what its evidence supports."""

    request_id: str
    provider_id: str
    model_instance_id: str
    canon_projection_digest: str
    turn_request_ref: str
    control_decision_ref: str
    validation_result_ref: str
    terminal_packet_ref: str
    #: The provider's own completion identifier, or None when the provider
    #: assigned none. A receipt states what the provider supplied; it never
    #: fills this in from a request id, a hash, or the model instance id.
    provider_completion_evidence_ref: str | None
    #: Which member of COMPLETION_PROOFS this receipt rests on, so a null
    #: reference reads as "the provider assigns none" rather than "unknown".
    provider_completion_proof: str

    def as_dict(self) -> dict[str, str | None]:
        return {
            "request_id": self.request_id,
            "provider_id": self.provider_id,
            "model_instance_id": self.model_instance_id,
            "canon_projection_digest": self.canon_projection_digest,
            "turn_request_ref": self.turn_request_ref,
            "control_decision_ref": self.control_decision_ref,
            "validation_result_ref": self.validation_result_ref,
            "terminal_packet_ref": self.terminal_packet_ref,
            "provider_completion_evidence_ref": self.provider_completion_evidence_ref,
            "provider_completion_proof": self.provider_completion_proof,
        }
