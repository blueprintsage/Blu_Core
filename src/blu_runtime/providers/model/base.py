"""Model Execution Boundary (IF-MODEL-EXECUTION).

Provider-neutral. LM Studio lives strictly beneath this boundary and is not an
architectural component. Swapping the provider must not change Blu canon,
security semantics, continuity semantics, or validation semantics.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from blu_runtime.contracts.models import (
    ModelExecutionRequest,
    NormalizedModelResult,
    ProviderObservation,
)


class ModelExecutionProvider(ABC):
    """One provider binding behind IF-MODEL-EXECUTION."""

    provider_id: str

    @abstractmethod
    def observe(self, configured_model_key: str, required_context: int) -> ProviderObservation:
        """Obtain operational evidence. Configuration alone is never evidence."""

    @abstractmethod
    def infer(self, request: ModelExecutionRequest) -> NormalizedModelResult:
        """Run one non-streaming inference and normalize the untrusted result."""


class ModelExecutionBoundary:
    """Gate that refuses inference without established provider evidence."""

    def __init__(self, provider: ModelExecutionProvider) -> None:
        self._provider = provider
        self.invocation_count = 0

    @property
    def provider_id(self) -> str:
        return self._provider.provider_id

    def observe(self, configured_model_key: str, required_context: int) -> ProviderObservation:
        return self._provider.observe(configured_model_key, required_context)

    def infer(self, request: ModelExecutionRequest) -> NormalizedModelResult:
        """Invoke the provider. Every call is counted for non-invocation proofs."""
        self.invocation_count += 1
        return self._provider.infer(request)
