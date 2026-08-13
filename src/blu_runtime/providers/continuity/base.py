"""Generic Continuity Provider Boundary.

Architectural only in Phase 1. No durable provider is authorized, and the
runtime reports continuity honestly rather than inferring it.

A live Python process is not durable continuity. Prompt history is not
persistence. Model context is not memory. LM Studio stateful chat is not Blu
continuity. A filename is not continuity evidence.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from blu_runtime.contracts.models import CONTINUITY_LIFETIMES, ContinuityState


class ContinuityProvider(ABC):
    """A durable continuity provider. None is implemented in Phase 1."""

    @abstractmethod
    def state(self) -> ContinuityState:
        """Report continuity truth, backed by provider evidence."""


class UnavailableContinuityProvider(ContinuityProvider):
    """The only Phase-1 binding: truthfully unavailable.

    Ordinary conversation still succeeds, because Phase 1 does not require
    durable continuity. It simply must not claim any.
    """

    def state(self) -> ContinuityState:
        return ContinuityState(
            lifetime="turn",
            provider_available=False,
            durability_claimed=False,
            reason="no durable continuity provider is implemented in Phase 1",
        )


def assert_supported_lifetime(lifetime: str) -> str:
    if lifetime not in CONTINUITY_LIFETIMES:
        raise ValueError(f"unsupported continuity lifetime: {lifetime}")
    return lifetime
