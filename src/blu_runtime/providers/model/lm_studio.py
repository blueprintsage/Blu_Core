"""LM Studio native REST v1 provider binding.

Beneath IF-MODEL-EXECUTION. LM Studio is not Blu, is not an architectural
component, is not an authorization authority, and is not a continuity store.

The operator owns LM Studio: installation, model download, model load, model
unload, and server lifecycle. This binding observes provider state and never
manages it. Model-load and download endpoints are deliberately not called.

Only repository-evidenced native fields are used (BC-050 §8.3). There is no
provider-side state continuation of any kind: `previous_response_id` and
Responses-API continuation vocabulary are not set, not read, and not referenced.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
import uuid
from typing import Any, Callable

from blu_runtime.contracts.models import (
    INVALID,
    PASS,
    PROVIDER_CONTEXT_INSUFFICIENT,
    PROVIDER_CONTEXT_UNKNOWN,
    PROVIDER_ENDPOINT_UNAVAILABLE,
    PROVIDER_IDENTITY_MISMATCH,
    PROVIDER_MODEL_ABSENT,
    PROVIDER_MODEL_INCOMPATIBLE,
    PROVIDER_MODEL_NOT_LOADED,
    PROVIDER_RESPONSE_MALFORMED,
    PROVIDER_TIMEOUT,
    PROVIDER_TOOL_CALL_UNSUPPORTED,
    UNAVAILABLE,
    ModelExecutionRequest,
    NormalizedModelResult,
    ProviderObservation,
)
from blu_runtime.providers.model.base import ModelExecutionProvider

MODELS_PATH = "/api/v1/models"
CHAT_PATH = "/api/v1/chat"

CHAT_COMPATIBLE_TYPES = frozenset({"llm", "vlm"})

#: Output item kinds this Phase-1 profile can normalize.
MESSAGE_KIND = "message"
REASONING_KIND = "reasoning"
TOOL_CALL_KINDS = frozenset({"tool_call", "invalid_tool_call"})


class Transport:
    """Minimal JSON transport. Standard library only."""

    def __init__(self, timeout_seconds: float) -> None:
        self.timeout_seconds = timeout_seconds

    def get(self, url: str) -> Any:
        request = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
            return json.loads(response.read().decode("utf-8"))

    def post(self, url: str, payload: dict[str, Any]) -> Any:
        body = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            url, data=body, method="POST", headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
            return json.loads(response.read().decode("utf-8"))


class LMStudioProvider(ModelExecutionProvider):
    """Native LM Studio v1 binding for one non-streaming ordinary turn."""

    provider_id = "lm_studio_native_rest_v1"
    provider_type = "lm_studio"
    api_profile = "native_rest_v1"

    def __init__(
        self,
        endpoint: str,
        timeout_seconds: float,
        transport: Transport | None = None,
        request_id_factory: Callable[[], str] | None = None,
    ) -> None:
        self.endpoint = endpoint.rstrip("/")
        self.timeout_seconds = timeout_seconds
        self._transport = transport or Transport(timeout_seconds)
        self._request_id_factory = request_id_factory or (lambda: uuid.uuid4().hex)

    # -- observation -------------------------------------------------------

    def observe(self, configured_model_key: str, required_context: int) -> ProviderObservation:
        """Establish loaded-instance and context evidence before any inference."""
        observation_id = self._request_id_factory()

        def unusable(code: str, **extra: Any) -> ProviderObservation:
            return ProviderObservation(
                observation_id=observation_id,
                provider_id=self.provider_id,
                endpoint_state=extra.pop("endpoint_state", "reachable"),
                configured_model_key=configured_model_key,
                usable=False,
                safe_error_code=code,
                **extra,
            )

        try:
            document = self._transport.get(f"{self.endpoint}{MODELS_PATH}")
        except (urllib.error.URLError, OSError, TimeoutError, json.JSONDecodeError):
            return unusable(PROVIDER_ENDPOINT_UNAVAILABLE, endpoint_state="unreachable")

        records = self._model_records(document)
        if records is None:
            return unusable(PROVIDER_RESPONSE_MALFORMED)

        matched = [record for record in records if record.get("id") == configured_model_key]
        if not matched:
            return unusable(PROVIDER_MODEL_ABSENT)

        record = matched[0]
        model_type = record.get("type")
        if model_type is not None and model_type not in CHAT_COMPATIBLE_TYPES:
            return unusable(PROVIDER_MODEL_INCOMPATIBLE)

        instances = record.get("loaded_instances")
        if not isinstance(instances, list) or not instances:
            return unusable(PROVIDER_MODEL_NOT_LOADED)

        instance = instances[0]
        if not isinstance(instance, dict):
            return unusable(PROVIDER_RESPONSE_MALFORMED)
        instance_id = instance.get("instance_id") or instance.get("id")
        if not isinstance(instance_id, str) or not instance_id:
            return unusable(PROVIDER_RESPONSE_MALFORMED)

        context_length = instance.get("context_length", record.get("loaded_context_length"))
        if not isinstance(context_length, int) or isinstance(context_length, bool) or context_length <= 0:
            return unusable(
                PROVIDER_CONTEXT_UNKNOWN,
                observed_model_key=configured_model_key,
                model_instance_id=instance_id,
            )
        if context_length < required_context:
            return unusable(
                PROVIDER_CONTEXT_INSUFFICIENT,
                observed_model_key=configured_model_key,
                model_instance_id=instance_id,
                observed_context_length=context_length,
            )

        limitations: list[str] = []
        if len(instances) > 1:
            limitations.append("multiple loaded instances observed; first stable instance selected")

        return ProviderObservation(
            observation_id=observation_id,
            provider_id=self.provider_id,
            endpoint_state="reachable",
            configured_model_key=configured_model_key,
            observed_model_key=record.get("id"),
            model_instance_id=instance_id,
            observed_context_length=context_length,
            usable=True,
            safe_error_code=None,
            limitations=tuple(limitations),
        )

    @staticmethod
    def _model_records(document: Any) -> list[dict[str, Any]] | None:
        if isinstance(document, dict):
            data = document.get("data", document.get("models"))
        else:
            data = document
        if not isinstance(data, list):
            return None
        if any(not isinstance(item, dict) for item in data):
            return None
        return data

    # -- inference ---------------------------------------------------------

    def infer(self, request: ModelExecutionRequest) -> NormalizedModelResult:
        """Run one bounded, non-streaming inference and normalize the result."""
        payload: dict[str, Any] = {
            "model": request.model_instance_id,
            "input": request.user_input,
            "system_prompt": request.system_prompt,
            "stream": False,
            "store": False,
            "context_length": request.context_budget,
        }

        def failure(status: str, code: str) -> NormalizedModelResult:
            return NormalizedModelResult(
                request_id=request.request_id,
                provider_id=self.provider_id,
                model_instance_id=None,
                status=status,
                candidate_text=None,
                output_kinds=(),
                safe_error_code=code,
            )

        try:
            document = self._transport.post(f"{self.endpoint}{CHAT_PATH}", payload)
        except (TimeoutError, urllib.error.URLError) as exc:
            reason = getattr(exc, "reason", None)
            if isinstance(exc, TimeoutError) or isinstance(reason, TimeoutError):
                return failure(UNAVAILABLE, PROVIDER_TIMEOUT)
            return failure(UNAVAILABLE, PROVIDER_ENDPOINT_UNAVAILABLE)
        except (OSError, json.JSONDecodeError):
            return failure(UNAVAILABLE, PROVIDER_ENDPOINT_UNAVAILABLE)

        return self.normalize_response(request, document)

    def normalize_response(self, request: ModelExecutionRequest, document: Any) -> NormalizedModelResult:
        """Treat the response as untrusted; a 200 does not prove a completion."""

        def failure(status: str, code: str, instance: str | None = None) -> NormalizedModelResult:
            return NormalizedModelResult(
                request_id=request.request_id,
                provider_id=self.provider_id,
                model_instance_id=instance,
                status=status,
                candidate_text=None,
                output_kinds=(),
                safe_error_code=code,
            )

        if not isinstance(document, dict):
            return failure(INVALID, PROVIDER_RESPONSE_MALFORMED)

        instance_id = document.get("model_instance_id") or document.get("model")
        if not isinstance(instance_id, str) or not instance_id:
            return failure(INVALID, PROVIDER_RESPONSE_MALFORMED)
        if instance_id != request.model_instance_id:
            return failure(INVALID, PROVIDER_IDENTITY_MISMATCH, instance_id)

        output = document.get("output")
        if not isinstance(output, list) or not output:
            return failure(INVALID, PROVIDER_RESPONSE_MALFORMED, instance_id)

        kinds: list[str] = []
        message_texts: list[str] = []
        for item in output:
            if not isinstance(item, dict):
                return failure(INVALID, PROVIDER_RESPONSE_MALFORMED, instance_id)
            kind = item.get("type")
            if not isinstance(kind, str):
                return failure(INVALID, PROVIDER_RESPONSE_MALFORMED, instance_id)
            kinds.append(kind)

            # A tool-call candidate is never executed. Phase 1 has no tools.
            if kind in TOOL_CALL_KINDS:
                return NormalizedModelResult(
                    request_id=request.request_id,
                    provider_id=self.provider_id,
                    model_instance_id=instance_id,
                    status=UNAVAILABLE,
                    candidate_text=None,
                    output_kinds=tuple(kinds),
                    safe_error_code=PROVIDER_TOOL_CALL_UNSUPPORTED,
                )

            if kind == MESSAGE_KIND:
                text = self._message_text(item)
                if text is None:
                    return failure(INVALID, PROVIDER_RESPONSE_MALFORMED, instance_id)
                message_texts.append(text)
            elif kind == REASONING_KIND:
                # Reasoning never becomes public assistant text.
                continue
            else:
                return failure(INVALID, PROVIDER_RESPONSE_MALFORMED, instance_id)

        candidate = "".join(message_texts)
        if not candidate.strip():
            return failure(INVALID, PROVIDER_RESPONSE_MALFORMED, instance_id)

        return NormalizedModelResult(
            request_id=request.request_id,
            provider_id=self.provider_id,
            model_instance_id=instance_id,
            status=PASS,
            candidate_text=candidate,
            output_kinds=tuple(kinds),
            safe_error_code=None,
            completion_evidence_ref=f"provider-completion:{request.request_id}",
        )

    @staticmethod
    def _message_text(item: dict[str, Any]) -> str | None:
        content = item.get("content")
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            parts: list[str] = []
            for part in content:
                if not isinstance(part, dict):
                    return None
                if part.get("type") not in {"text", None}:
                    return None
                text = part.get("text")
                if not isinstance(text, str):
                    return None
                parts.append(text)
            return "".join(parts)
        return None
