"""LM Studio provider binding: evidence before inference, untrusted output.

Deterministic mocks only. No live LM Studio instance is required.
"""

from __future__ import annotations

import unittest
import urllib.error

from tests.runtime_phase1.support import RecordingTransport, chat_response, model_inventory

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
)
from blu_runtime.providers.model.lm_studio import LMStudioProvider

MODEL = "synthetic-model-key"
INSTANCE = f"{MODEL}:0"


def provider(transport: RecordingTransport) -> LMStudioProvider:
    return LMStudioProvider(
        endpoint="http://127.0.0.1:1234",
        timeout_seconds=5,
        transport=transport,
        request_id_factory=lambda: "obs-1",
    )


def execution_request(instance_id: str = INSTANCE) -> ModelExecutionRequest:
    return ModelExecutionRequest(
        request_id="r1",
        model_instance_id=instance_id,
        canon_projection_digest="0" * 64,
        turn_request_ref="turn-request:r1",
        control_decision_ref="control-decision:r1",
        system_prompt="ENVELOPE",
        user_input="hello",
        context_budget=4096,
    )


class ObservationTests(unittest.TestCase):
    def test_successful_match_records_instance_and_context(self) -> None:
        transport = RecordingTransport(inventory=model_inventory())
        observation = provider(transport).observe(MODEL, 4096)
        self.assertTrue(observation.usable)
        self.assertEqual(observation.model_instance_id, INSTANCE)
        self.assertEqual(observation.observed_context_length, 8192)
        self.assertEqual(transport.get_calls, ["http://127.0.0.1:1234/api/v1/models"])

    def test_endpoint_unavailable(self) -> None:
        transport = RecordingTransport(raises=urllib.error.URLError("refused"))
        observation = provider(transport).observe(MODEL, 4096)
        self.assertFalse(observation.usable)
        self.assertEqual(observation.safe_error_code, PROVIDER_ENDPOINT_UNAVAILABLE)
        self.assertEqual(observation.endpoint_state, "unreachable")

    def test_malformed_inventory(self) -> None:
        for inventory in ({"data": "not-a-list"}, {"data": ["not-a-record"]}, 7):
            with self.subTest(inventory=inventory):
                observation = provider(RecordingTransport(inventory=inventory)).observe(MODEL, 4096)
                self.assertEqual(observation.safe_error_code, PROVIDER_RESPONSE_MALFORMED)

    def test_configured_key_absent(self) -> None:
        transport = RecordingTransport(inventory=model_inventory(model_key="other-model"))
        observation = provider(transport).observe(MODEL, 4096)
        self.assertEqual(observation.safe_error_code, PROVIDER_MODEL_ABSENT)

    def test_configured_key_present_but_not_loaded(self) -> None:
        transport = RecordingTransport(inventory=model_inventory(loaded=False))
        observation = provider(transport).observe(MODEL, 4096)
        self.assertEqual(observation.safe_error_code, PROVIDER_MODEL_NOT_LOADED)

    def test_wrong_model_type(self) -> None:
        transport = RecordingTransport(inventory=model_inventory(model_type="embeddings"))
        observation = provider(transport).observe(MODEL, 4096)
        self.assertEqual(observation.safe_error_code, PROVIDER_MODEL_INCOMPATIBLE)

    def test_unknown_context(self) -> None:
        transport = RecordingTransport(inventory=model_inventory(context_length=None))
        observation = provider(transport).observe(MODEL, 4096)
        self.assertEqual(observation.safe_error_code, PROVIDER_CONTEXT_UNKNOWN)

    def test_insufficient_context(self) -> None:
        transport = RecordingTransport(inventory=model_inventory(context_length=1024))
        observation = provider(transport).observe(MODEL, 4096)
        self.assertEqual(observation.safe_error_code, PROVIDER_CONTEXT_INSUFFICIENT)
        self.assertEqual(observation.observed_context_length, 1024)

    def test_multiple_loaded_instances_records_limitation(self) -> None:
        transport = RecordingTransport(inventory=model_inventory(instances=3))
        observation = provider(transport).observe(MODEL, 4096)
        self.assertTrue(observation.usable)
        self.assertEqual(observation.model_instance_id, INSTANCE)
        self.assertTrue(observation.limitations)

    def test_configuration_alone_is_not_evidence(self) -> None:
        """An empty inventory cannot satisfy a configured model key."""
        transport = RecordingTransport(inventory={"data": []})
        observation = provider(transport).observe(MODEL, 4096)
        self.assertFalse(observation.usable)


class InferenceTests(unittest.TestCase):
    def test_ordinary_message_response(self) -> None:
        transport = RecordingTransport(chat=chat_response(INSTANCE, "Hello there."))
        result = provider(transport).infer(execution_request())
        self.assertEqual(result.status, PASS)
        self.assertEqual(result.candidate_text, "Hello there.")
        self.assertEqual(result.model_instance_id, INSTANCE)

    def test_request_profile_uses_only_evidenced_native_fields(self) -> None:
        transport = RecordingTransport(chat=chat_response(INSTANCE))
        provider(transport).infer(execution_request())
        url, payload = transport.post_calls[0]
        self.assertEqual(url, "http://127.0.0.1:1234/api/v1/chat")
        self.assertEqual(
            set(payload), {"model", "input", "system_prompt", "stream", "store", "context_length"}
        )
        self.assertIs(payload["stream"], False)
        self.assertIs(payload["store"], False)
        self.assertEqual(payload["system_prompt"], "ENVELOPE")

    def test_no_state_continuation_fields_are_sent(self) -> None:
        transport = RecordingTransport(chat=chat_response(INSTANCE))
        provider(transport).infer(execution_request())
        _, payload = transport.post_calls[0]
        for forbidden in ("previous_response_id", "response_id", "tools", "tool_choice", "integrations", "mcp"):
            self.assertNotIn(forbidden, payload)

    def test_timeout_is_unavailable_without_partial_output(self) -> None:
        transport = RecordingTransport(chat=TimeoutError("timed out"))
        result = provider(transport).infer(execution_request())
        self.assertEqual(result.status, UNAVAILABLE)
        self.assertEqual(result.safe_error_code, PROVIDER_TIMEOUT)
        self.assertIsNone(result.candidate_text)

    def test_transport_failure_is_unavailable(self) -> None:
        transport = RecordingTransport(chat=urllib.error.URLError("refused"))
        result = provider(transport).infer(execution_request())
        self.assertEqual(result.status, UNAVAILABLE)
        self.assertIsNone(result.candidate_text)

    def test_malformed_response_is_invalid(self) -> None:
        for document in ("not-a-dict", {}, {"model_instance_id": INSTANCE}, {"model_instance_id": INSTANCE, "output": []}):
            with self.subTest(document=document):
                result = provider(RecordingTransport(chat=document)).infer(execution_request())
                self.assertEqual(result.status, INVALID)
                self.assertIsNone(result.candidate_text)

    def test_model_identity_mismatch_is_invalid(self) -> None:
        transport = RecordingTransport(chat=chat_response("a-different-instance"))
        result = provider(transport).infer(execution_request())
        self.assertEqual(result.status, INVALID)
        self.assertEqual(result.safe_error_code, PROVIDER_IDENTITY_MISMATCH)
        self.assertIsNone(result.candidate_text)

    def test_tool_call_is_never_executed(self) -> None:
        for kind in ("tool_call", "invalid_tool_call"):
            with self.subTest(kind=kind):
                transport = RecordingTransport(chat=chat_response(INSTANCE, kinds=(kind,)))
                result = provider(transport).infer(execution_request())
                self.assertEqual(result.status, UNAVAILABLE)
                self.assertEqual(result.safe_error_code, PROVIDER_TOOL_CALL_UNSUPPORTED)
                self.assertIsNone(result.candidate_text)

    def test_reasoning_never_becomes_public_text(self) -> None:
        transport = RecordingTransport(
            chat=chat_response(INSTANCE, "The visible answer.", kinds=("reasoning", "message"))
        )
        result = provider(transport).infer(execution_request())
        self.assertEqual(result.status, PASS)
        self.assertEqual(result.candidate_text, "The visible answer.")
        self.assertNotIn("internal reasoning", result.candidate_text or "")
        self.assertIn("reasoning", result.output_kinds)

    def test_reasoning_only_response_yields_no_candidate(self) -> None:
        transport = RecordingTransport(chat=chat_response(INSTANCE, kinds=("reasoning",)))
        result = provider(transport).infer(execution_request())
        self.assertEqual(result.status, INVALID)
        self.assertIsNone(result.candidate_text)

    def test_structured_message_content_is_supported(self) -> None:
        document = {
            "model_instance_id": INSTANCE,
            "output": [{"type": "message", "content": [{"type": "text", "text": "Chunked reply."}]}],
        }
        result = provider(RecordingTransport(chat=document)).infer(execution_request())
        self.assertEqual(result.status, PASS)
        self.assertEqual(result.candidate_text, "Chunked reply.")

    def test_unknown_output_kind_is_invalid(self) -> None:
        document = {"model_instance_id": INSTANCE, "output": [{"type": "surprise"}]}
        result = provider(RecordingTransport(chat=document)).infer(execution_request())
        self.assertEqual(result.status, INVALID)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
