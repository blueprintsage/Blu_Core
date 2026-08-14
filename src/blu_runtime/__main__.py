"""Process assembly and terminal orchestration for BC-050.

Non-component support layer (BC-050 §14). This module wires the seven approved
components together and owns no behavior of its own. Every decision below is
delegated to the component that owns it.

Boot order is fixed by `readiness/phase1_executable_slice.json`: configuration,
protected policy, canon, runtime graph, provider observation, model match,
context verification, continuity truth, then host ingress.
"""

from __future__ import annotations

import argparse
import os
import sys
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping

from blu_runtime import config as configuration
from blu_runtime.adapters.host.terminal import TerminalHostAdapter
from blu_runtime.canon.loader import CanonError, load_projection
from blu_runtime.contracts.models import (
    BLOCK,
    INVALID,
    PASS,
    PROVIDER_COMPLETION_EVIDENCE_MISSING,
    UNAVAILABLE,
    CanonProjection,
    ContinuityState,
    ModelExecutionRequest,
    TerminalPacket,
    TurnReceipt,
)
from blu_runtime.core import turn_controller
from blu_runtime.core.security_restraint import evaluate_ingress, load_policy
from blu_runtime.core.validation_egress import evaluate_egress
from blu_runtime.providers.continuity.base import UnavailableContinuityProvider
from blu_runtime.providers.model.base import ModelExecutionBoundary
from blu_runtime.providers.model.lm_studio import LMStudioProvider


@dataclass(frozen=True)
class BootFailure:
    status: str
    safe_error_code: str
    detail: str


@dataclass
class Runtime:
    """The assembled Phase-1 runtime graph."""

    config: configuration.RuntimeConfig
    policy: dict[str, Any]
    projection: CanonProjection
    boundary: ModelExecutionBoundary
    model_instance_id: str
    context_budget: int
    continuity: ContinuityState
    request_id_factory: Callable[[], str]
    receipts: list[TurnReceipt]


def boot(
    config_path: Path | str,
    environment: Mapping[str, str] | None = None,
    boundary: ModelExecutionBoundary | None = None,
    golden_root: Path | str | None = None,
    request_id_factory: Callable[[], str] | None = None,
) -> Runtime | BootFailure:
    """Bring the runtime to a state where an ordinary turn may be attempted."""
    env = os.environ if environment is None else environment
    factory = request_id_factory or (lambda: uuid.uuid4().hex)

    try:
        settings = configuration.load(config_path)
    except configuration.ConfigError as exc:
        return BootFailure(INVALID, exc.safe_error_code, exc.detail)

    policy_load = load_policy(settings.protected_policy_ref.as_dict(), env)
    if not policy_load.usable or policy_load.policy is None:
        return BootFailure(UNAVAILABLE, policy_load.error_code or "POLICY_UNUSABLE", "protected policy is unusable")

    try:
        projection = (
            load_projection(golden_root) if golden_root is not None else load_projection()
        )
    except CanonError as exc:
        return BootFailure(BLOCK, exc.safe_error_code, exc.detail)

    execution = boundary or ModelExecutionBoundary(
        LMStudioProvider(endpoint=settings.endpoint, timeout_seconds=settings.timeout_seconds)
    )

    observation = execution.observe(settings.selected_model, settings.requested_tokens)
    if not observation.usable or not observation.model_instance_id:
        return BootFailure(
            UNAVAILABLE,
            observation.safe_error_code or "PROVIDER_ENDPOINT_UNAVAILABLE",
            "provider evidence was not established",
        )

    return Runtime(
        config=settings,
        policy=policy_load.policy,
        projection=projection,
        boundary=execution,
        model_instance_id=observation.model_instance_id,
        context_budget=settings.requested_tokens,
        continuity=UnavailableContinuityProvider().state(),
        request_id_factory=factory,
        receipts=[],
    )


def _valid_completion_evidence(value: Any) -> bool:
    """Accept only a non-blank string reference to observed provider evidence.

    Any other type is malformed provider output and fails closed here, at the
    evidence boundary, rather than reaching string handling deeper in the turn.
    """
    return isinstance(value, str) and bool(value.strip())


def run_turn(runtime: Runtime, text: Any, request_id: str | None = None) -> TerminalPacket:
    """Run exactly one ordinary turn and return exactly one terminal packet."""
    identifier = request_id or runtime.request_id_factory()

    def terminal(status: str, code: str | None, tool_executed: bool = False) -> TerminalPacket:
        return TerminalPacket(
            request_id=identifier,
            status=status,
            public_output=None,
            safe_error_code=code,
            model_invoked=False,
            tool_executed=tool_executed,
            continuity=runtime.continuity,
        )

    decision = evaluate_ingress(text, runtime.policy)
    if not decision.eligible_for_turn_controller:
        return terminal(decision.terminal_status or BLOCK, decision.safe_error_code)

    control = turn_controller.control(identifier, decision, text)
    if control.status != PASS:
        return terminal(control.status, control.safe_error_code)

    request = turn_controller.build_turn_request(identifier, text)
    execution_request = ModelExecutionRequest(
        request_id=identifier,
        model_instance_id=runtime.model_instance_id,
        canon_projection_digest=runtime.projection.digest,
        turn_request_ref=f"turn-request:{identifier}",
        control_decision_ref=f"control-decision:{identifier}",
        system_prompt=runtime.projection.system_prompt,
        user_input=request.text,
        context_budget=runtime.context_budget,
    )

    result = runtime.boundary.infer(execution_request)
    # B-07: completion evidence is observed or the turn is not a success. A
    # generated label is not evidence, so there is deliberately no fallback,
    # and a malformed type is rejected here rather than coerced with str() --
    # coercion would fabricate apparent evidence out of invalid input.
    if result.status == PASS and not _valid_completion_evidence(result.completion_evidence_ref):
        return TerminalPacket(
            request_id=identifier,
            status=INVALID,
            public_output=None,
            safe_error_code=PROVIDER_COMPLETION_EVIDENCE_MISSING,
            model_invoked=True,
            tool_executed=False,
            continuity=runtime.continuity,
        )
    if result.status != PASS or result.candidate_text is None:
        return TerminalPacket(
            request_id=identifier,
            status=result.status,
            public_output=None,
            safe_error_code=result.safe_error_code,
            model_invoked=True,
            tool_executed=False,
            continuity=runtime.continuity,
        )

    validation = evaluate_egress(identifier, result.candidate_text, runtime.policy)
    if not validation.eligible_for_print or validation.public_output is None:
        return TerminalPacket(
            request_id=identifier,
            status=UNAVAILABLE if validation.egress_result == UNAVAILABLE else BLOCK,
            public_output=None,
            safe_error_code=validation.safe_error_code,
            model_invoked=True,
            tool_executed=False,
            continuity=runtime.continuity,
        )

    runtime.receipts.append(
        TurnReceipt(
            request_id=identifier,
            provider_id=result.provider_id,
            model_instance_id=result.model_instance_id or runtime.model_instance_id,
            canon_projection_digest=runtime.projection.digest,
            turn_request_ref=execution_request.turn_request_ref,
            control_decision_ref=execution_request.control_decision_ref,
            validation_result_ref=f"validation-result:{identifier}",
            terminal_packet_ref=f"terminal-packet:{identifier}",
            provider_completion_evidence_ref=result.completion_evidence_ref,
        )
    )

    return TerminalPacket(
        request_id=identifier,
        status=PASS,
        public_output=validation.public_output,
        safe_error_code=None,
        model_invoked=True,
        tool_executed=False,
        continuity=runtime.continuity,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="blu_runtime", description=__doc__)
    parser.add_argument("--config", required=True, type=Path, help="portable runtime configuration")
    args = parser.parse_args(argv)

    booted = boot(args.config)
    if isinstance(booted, BootFailure):
        sys.stderr.write(f"boot failed: {booted.status} {booted.safe_error_code}\n")
        return 1

    adapter = TerminalHostAdapter()
    sys.stdout.write(
        # B-06: advertise only what the host adapter actually does. Slash
        # commands are ordinary unsupported input, not termination controls.
        "Blu Core Python Runtime Phase 1. Ordinary conversation only; "
        "durable continuity unavailable. End input (Ctrl-Z then Enter on "
        "Windows, Ctrl-D elsewhere) to end the session.\n"
    )
    while True:
        event = adapter.receive()
        if event is None:
            return 0
        host_input = adapter.submit(event)
        packet = run_turn(booted, host_input.text, request_id=host_input.request_id)
        adapter.render(packet)


if __name__ == "__main__":  # pragma: no cover - process entrypoint
    raise SystemExit(main())
