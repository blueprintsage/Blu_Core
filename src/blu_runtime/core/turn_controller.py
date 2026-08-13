"""Turn Controller for the single supported Phase-1 route.

Exactly one route exists: `ordinary_conversation`. There is no fallback route
and no generic "let the model decide" router. Route entry requires a PASS
SecurityDecision plus verified canon, provider, and context evidence.
"""

from __future__ import annotations

from blu_runtime.contracts.models import (
    PASS,
    ROUTE_UNSUPPORTED,
    SECURITY_DECISION_NOT_EXECUTABLE,
    UNAVAILABLE,
    ControlDecision,
    SecurityDecision,
    TurnRequest,
)

ORDINARY_CONVERSATION = "ordinary_conversation"
MODEL_EXECUTION_BOUNDARY = "model_execution_boundary"
SCOPE_LOCK = "phase1_ordinary_conversation_single_owner"

#: Routes that are architecturally named but deliberately not implemented.
UNSUPPORTED_ROUTES = (
    "slash_command",
    "protected_source_access",
    "authentication",
    "protected_authorization",
    "protected_continuation",
    "tools",
    "tool_execution",
    "source_retrieval",
    "artifacts",
    "durable_continuity_mutation",
    "reminders",
    "scheduling",
    "memory_program",
    "simcode",
    "mmu",
    "statetree",
    "mood_service",
    "school_engine",
    "skillforge",
    "pass_program",
)


def select_route(text: str) -> str:
    """Classify one turn.

    Phase 1 supports ordinary conversation only. Anything that presents as a
    command is refused as unsupported rather than partially implemented.
    """
    if text.lstrip().startswith("/"):
        return "slash_command"
    return ORDINARY_CONVERSATION


def control(request_id: str, decision: SecurityDecision, text: str) -> ControlDecision:
    """Lock the route, owner, and ScopeLock for one turn.

    Only PASS reaches here in normal operation. An unexpected ASK is not
    executable in Phase 1: it terminates safely and never invokes the model.
    """
    if decision.decision != PASS or not decision.eligible_for_turn_controller:
        return ControlDecision(
            request_id=request_id,
            route=ORDINARY_CONVERSATION,
            owner=MODEL_EXECUTION_BOUNDARY,
            scope_lock=SCOPE_LOCK,
            side_effects=False,
            status=UNAVAILABLE,
            safe_error_code=SECURITY_DECISION_NOT_EXECUTABLE,
        )

    route = select_route(text)
    if route != ORDINARY_CONVERSATION:
        return ControlDecision(
            request_id=request_id,
            route=route,
            owner=MODEL_EXECUTION_BOUNDARY,
            scope_lock=SCOPE_LOCK,
            side_effects=False,
            status=UNAVAILABLE,
            safe_error_code=ROUTE_UNSUPPORTED,
        )

    return ControlDecision(
        request_id=request_id,
        route=ORDINARY_CONVERSATION,
        owner=MODEL_EXECUTION_BOUNDARY,
        scope_lock=SCOPE_LOCK,
        side_effects=False,
        status=PASS,
        safe_error_code=None,
    )


def build_turn_request(request_id: str, text: str) -> TurnRequest:
    return TurnRequest(request_id=request_id, route=ORDINARY_CONVERSATION, text=text)
