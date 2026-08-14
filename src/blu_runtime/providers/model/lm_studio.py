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
    PROVIDER_COMPLETION_EVIDENCE_MISSING,
    PROVIDER_COMPLETION_UNVERIFIED,
    PROVIDER_ERROR_REPORTED,
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

#: Native v1 model-record identity (BC-050-C4). The live `/api/v1/models`
#: document identifies each model record with `key`; `id` appears only on the
#: loaded instance. Matching is exact against this one field: display names,
#: publishers, filenames, and substrings are not identity.
MODEL_RECORD_KEY_FIELD = "key"

#: Loaded-instance identity, in precedence order.
INSTANCE_ID_FIELDS = ("instance_id", "id")

#: Observed loaded-instance capacity (BC-050-C4). The live document reports the
#: capacity the instance was actually loaded with at
#: `loaded_instances[].config.context_length`. The record-level
#: `max_context_length` is maximum model capability, not loaded configuration,
#: and is deliberately never read as capacity evidence.
INSTANCE_CONFIG_FIELD = "config"
INSTANCE_CONTEXT_FIELD = "context_length"

#: Output item kinds this Phase-1 profile can normalize.
MESSAGE_KIND = "message"
REASONING_KIND = "reasoning"
TOOL_CALL_KINDS = frozenset({"tool_call", "invalid_tool_call"})

#: Positive terminal-completion evidence (B-04). Repository evidence
#: (LM-EVID-003) records that responses identify the model instance and carry
#: typed output plus statistics, but does not pin the terminal-state spelling,
#: so this set is a fail-closed assumption to confirm during live smoke.
TERMINAL_COMPLETION_STATES = frozenset({"completed", "complete", "finished", "succeeded", "done"})
TIMEOUT_STATES = frozenset({"timeout", "timed_out"})
ERROR_STATES = frozenset({"error", "failed", "failure", "cancelled", "canceled", "aborted"})

#: Provider-assigned identifiers accepted as completion evidence (B-07).
COMPLETION_EVIDENCE_FIELDS = ("id", "response_id", "completion_id")


def _looks_like_timeout(error: object) -> bool:
    return "timeout" in str(error).lower() or "timed out" in str(error).lower()


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

        matched = [
            record for record in records if self._record_key(record) == configured_model_key
        ]
        if not matched:
            return unusable(PROVIDER_MODEL_ABSENT)

        record = matched[0]
        observed_model_key = self._record_key(record)
        # B-03: positive compatibility evidence is required. Absent, null, or
        # malformed type evidence is not "probably compatible" -- compatibility
        # is never inferred from the configured name, the filename, successful
        # loading, context capacity, or endpoint availability.
        model_type = record.get("type")
        if not isinstance(model_type, str) or model_type not in CHAT_COMPATIBLE_TYPES:
            return unusable(PROVIDER_MODEL_INCOMPATIBLE)

        instances = record.get("loaded_instances")
        if not isinstance(instances, list) or not instances:
            return unusable(PROVIDER_MODEL_NOT_LOADED)

        instance = instances[0]
        if not isinstance(instance, dict):
            return unusable(PROVIDER_RESPONSE_MALFORMED)
        instance_id = self._instance_id(instance)
        if instance_id is None:
            return unusable(PROVIDER_RESPONSE_MALFORMED)

        # Capacity is whatever the instance was actually loaded with. A missing,
        # malformed, or non-positive value is unknown capacity, never a default.
        context_length = self._instance_context_length(instance)
        if context_length is None:
            return unusable(
                PROVIDER_CONTEXT_UNKNOWN,
                observed_model_key=observed_model_key,
                model_instance_id=instance_id,
            )
        if context_length < required_context:
            return unusable(
                PROVIDER_CONTEXT_INSUFFICIENT,
                observed_model_key=observed_model_key,
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
            observed_model_key=observed_model_key,
            model_instance_id=instance_id,
            observed_context_length=context_length,
            usable=True,
            safe_error_code=None,
            limitations=tuple(limitations),
        )

    @staticmethod
    def _record_key(record: dict[str, Any]) -> str | None:
        """Return the record's provider identity, or None when it asserts none."""
        key = record.get(MODEL_RECORD_KEY_FIELD)
        if isinstance(key, str) and key:
            return key
        return None

    @staticmethod
    def _instance_id(instance: dict[str, Any]) -> str | None:
        for field in INSTANCE_ID_FIELDS:
            value = instance.get(field)
            if isinstance(value, str) and value:
                return value
        return None

    @staticmethod
    def _instance_context_length(instance: dict[str, Any]) -> int | None:
        """Return observed loaded capacity, or None when it is not evidenced."""
        config = instance.get(INSTANCE_CONFIG_FIELD)
        if not isinstance(config, dict):
            return None
        value = config.get(INSTANCE_CONTEXT_FIELD)
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            return None
        return value

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

        # B-04: completion is established before any candidate text is read.
        # An unresolved error, a nonterminal state, or a conflicting identity
        # cannot coexist with accepted output.
        error = document.get("error")
        if error not in (None, "", {}, [], False):
            code = PROVIDER_TIMEOUT if _looks_like_timeout(error) else PROVIDER_ERROR_REPORTED
            return failure(UNAVAILABLE, code)

        status = document.get("status")
        if not isinstance(status, str):
            return failure(INVALID, PROVIDER_COMPLETION_UNVERIFIED)
        if status in TIMEOUT_STATES:
            return failure(UNAVAILABLE, PROVIDER_TIMEOUT)
        if status in ERROR_STATES:
            return failure(UNAVAILABLE, PROVIDER_ERROR_REPORTED)
        if status not in TERMINAL_COMPLETION_STATES:
            # Queued, processing, cancelled, or any unknown state.
            return failure(INVALID, PROVIDER_COMPLETION_UNVERIFIED)

        instance_id = document.get("model_instance_id") or document.get("model")
        if not isinstance(instance_id, str) or not instance_id:
            return failure(INVALID, PROVIDER_RESPONSE_MALFORMED)
        if instance_id != request.model_instance_id:
            return failure(INVALID, PROVIDER_IDENTITY_MISMATCH, instance_id)

        # Provider and request identity, when the response asserts them, must
        # agree with the boundary's own evidence.
        for field in ("provider_id", "provider"):
            claimed = document.get(field)
            if claimed is not None and claimed not in (self.provider_id, self.provider_type):
                return failure(INVALID, PROVIDER_IDENTITY_MISMATCH, instance_id)
        claimed_request = document.get("request_id")
        if claimed_request is not None and claimed_request != request.request_id:
            return failure(INVALID, PROVIDER_IDENTITY_MISMATCH, instance_id)

        # B-07: completion evidence is observed, never synthesized. Without a
        # provider-assigned identifier there is no completion to reference.
        evidence_ref = self._completion_evidence_ref(document, instance_id)
        if evidence_ref is None:
            return failure(INVALID, PROVIDER_COMPLETION_EVIDENCE_MISSING, instance_id)

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
            completion_evidence_ref=evidence_ref,
        )

    def _completion_evidence_ref(self, document: dict[str, Any], instance_id: str) -> str | None:
        """Bind completion evidence to a provider-assigned identifier.

        Returns None when the provider asserted no identifier. Fabricating one
        from the request id would make the receipt claim evidence that was
        never observed.
        """
        for field in COMPLETION_EVIDENCE_FIELDS:
            value = document.get(field)
            if isinstance(value, str) and value.strip():
                return f"{self.provider_id}:{instance_id}:{value}"
        return None

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
