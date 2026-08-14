"""LM Studio provider binding: evidence before inference, untrusted output.

Deterministic mocks only. No live LM Studio instance is required.
"""

from __future__ import annotations

import unittest
import urllib.error

from tests.runtime_phase1.support import RecordingTransport, chat_response, model_inventory

from blu_runtime.contracts.models import (
    COMPLETION_PROOF_PROVIDER_ID,
    COMPLETION_PROOF_SYNCHRONOUS_RESPONSE,
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
            "status": "completed",
            "id": "resp-0002",
            "output": [{"type": "message", "content": [{"type": "text", "text": "Chunked reply."}]}],
        }
        result = provider(RecordingTransport(chat=document)).infer(execution_request())
        self.assertEqual(result.status, PASS)
        self.assertEqual(result.candidate_text, "Chunked reply.")

    def test_unknown_output_kind_is_invalid(self) -> None:
        document = chat_response(INSTANCE, kinds=("surprise",))
        result = provider(RecordingTransport(chat=document)).infer(execution_request())
        self.assertEqual(result.status, INVALID)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()


class ChatCompatibilityEvidenceTests(unittest.TestCase):
    """B-03: usability requires positive compatibility evidence."""

    def _observe(self, record: dict) -> object:
        return provider(RecordingTransport(inventory={"data": [record]})).observe(MODEL, 4096)

    def _record(self, **overrides) -> dict:
        record = {
            "key": MODEL,
            "type": "llm",
            "loaded_instances": [{"instance_id": INSTANCE, "config": {"context_length": 8192}}],
        }
        record.update(overrides)
        return record

    def test_valid_chat_compatible_type_is_usable(self) -> None:
        for model_type in ("llm", "vlm"):
            with self.subTest(type=model_type):
                observation = self._observe(self._record(type=model_type))
                self.assertTrue(observation.usable)

    def test_missing_type_is_not_usable(self) -> None:
        record = self._record()
        del record["type"]
        observation = self._observe(record)
        self.assertFalse(observation.usable)
        self.assertEqual(observation.safe_error_code, PROVIDER_MODEL_INCOMPATIBLE)

    def test_null_type_is_not_usable(self) -> None:
        observation = self._observe(self._record(type=None))
        self.assertFalse(observation.usable)
        self.assertEqual(observation.safe_error_code, PROVIDER_MODEL_INCOMPATIBLE)

    def test_malformed_type_is_not_usable(self) -> None:
        for value in (7, ["llm"], {"kind": "llm"}, True, ""):
            with self.subTest(value=value):
                observation = self._observe(self._record(type=value))
                self.assertFalse(observation.usable)
                self.assertEqual(observation.safe_error_code, PROVIDER_MODEL_INCOMPATIBLE)

    def test_wrong_type_is_not_usable(self) -> None:
        for value in ("embeddings", "reranker", "unknown"):
            with self.subTest(value=value):
                self.assertFalse(self._observe(self._record(type=value)).usable)

    def test_compatibility_is_not_inferred_from_other_signals(self) -> None:
        """A loaded, well-named, high-context model is still not evidence."""
        record = self._record()
        del record["type"]
        record["loaded_context_length"] = 131072
        observation = self._observe(record)
        self.assertFalse(observation.usable)


class TerminalCompletionEvidenceTests(unittest.TestCase):
    """B-04/B-07: completion must be positively evidenced before any text."""

    def _normalize(self, document) -> object:
        return provider(RecordingTransport()).normalize_response(execution_request(), document)

    def test_ordinary_completion_is_accepted(self) -> None:
        """The live stateless shape: no status, no id, still a completion."""
        result = self._normalize(chat_response(INSTANCE, "Fine."))
        self.assertEqual(result.status, PASS)
        self.assertEqual(result.candidate_text, "Fine.")
        self.assertIsNone(result.completion_evidence_ref)
        self.assertEqual(result.completion_proof, COMPLETION_PROOF_SYNCHRONOUS_RESPONSE)

    def test_provider_assigned_identifier_is_still_referenced(self) -> None:
        result = self._normalize(chat_response(INSTANCE, "Fine.", evidence_id="resp-1"))
        self.assertEqual(result.status, PASS)
        self.assertIn("resp-1", result.completion_evidence_ref)
        self.assertEqual(result.completion_proof, COMPLETION_PROOF_PROVIDER_ID)

    def test_conflicting_provider_identity_rejects(self) -> None:
        for field in ("provider_id", "provider"):
            with self.subTest(field=field):
                document = chat_response(INSTANCE, **{field: "someone-elses-provider"})
                result = self._normalize(document)
                self.assertEqual(result.status, INVALID)
                self.assertEqual(result.safe_error_code, PROVIDER_IDENTITY_MISMATCH)
                self.assertIsNone(result.candidate_text)

    def test_conflicting_request_identity_rejects(self) -> None:
        result = self._normalize(chat_response(INSTANCE, request_id="some-other-request"))
        self.assertEqual(result.status, INVALID)
        self.assertIsNone(result.candidate_text)

    def test_error_state_with_valid_message_rejects(self) -> None:
        result = self._normalize(chat_response(INSTANCE, "Looks fine.", error="model crashed"))
        self.assertEqual(result.status, UNAVAILABLE)
        self.assertEqual(result.safe_error_code, PROVIDER_ERROR_REPORTED)
        self.assertIsNone(result.candidate_text)

    def test_timeout_state_with_valid_message_rejects(self) -> None:
        result = self._normalize(chat_response(INSTANCE, "Partial.", error="request timed out"))
        self.assertEqual(result.status, UNAVAILABLE)
        self.assertEqual(result.safe_error_code, PROVIDER_TIMEOUT)
        self.assertIsNone(result.candidate_text)

    def test_nonterminal_processing_state_rejects(self) -> None:
        for state in ("processing", "queued", "in_progress", "streaming"):
            with self.subTest(state=state):
                result = self._normalize(chat_response(INSTANCE, "Not done.", status=state))
                self.assertEqual(result.status, INVALID)
                self.assertEqual(result.safe_error_code, PROVIDER_COMPLETION_UNVERIFIED)
                self.assertIsNone(result.candidate_text)

    def test_error_status_values_reject_as_unavailable(self) -> None:
        for state in ("error", "failed", "cancelled", "aborted"):
            with self.subTest(state=state):
                result = self._normalize(chat_response(INSTANCE, "Text.", status=state))
                self.assertEqual(result.status, UNAVAILABLE)
                self.assertIsNone(result.candidate_text)

    def test_absent_terminal_status_is_accepted(self) -> None:
        """C5: native v1 defines no terminal state field, so absence is normal.

        This inverts the pre-C5 expectation. The rule it replaces rejected
        every real LM Studio completion.
        """
        result = self._normalize(chat_response(INSTANCE, "Text.", status=None))
        self.assertEqual(result.status, PASS)
        self.assertEqual(result.candidate_text, "Text.")
        self.assertNotIn("status", chat_response(INSTANCE, "Text.", status=None))

    def test_malformed_terminal_state_rejects(self) -> None:
        for value in (7, ["completed"], {"state": "completed"}, True):
            with self.subTest(value=value):
                result = self._normalize(chat_response(INSTANCE, "Text.", status=value))
                self.assertEqual(result.status, INVALID)
                self.assertIsNone(result.candidate_text)

    def test_absent_completion_identifier_is_represented_not_rejected(self) -> None:
        """C5: `store: false` assigns no id, and absence is stated as absence."""
        result = self._normalize(chat_response(INSTANCE, "Text.", evidence_id=None))
        self.assertEqual(result.status, PASS)
        self.assertIsNone(result.completion_evidence_ref)
        self.assertEqual(result.completion_proof, COMPLETION_PROOF_SYNCHRONOUS_RESPONSE)

    def test_blank_completion_evidence_rejects(self) -> None:
        for value in ("", "   "):
            with self.subTest(value=repr(value)):
                result = self._normalize(chat_response(INSTANCE, "Text.", evidence_id=value))
                self.assertEqual(result.safe_error_code, PROVIDER_COMPLETION_EVIDENCE_MISSING)

    def test_completion_evidence_is_provider_bound_not_request_derived(self) -> None:
        result = self._normalize(chat_response(INSTANCE, "Text.", evidence_id="resp-42"))
        self.assertIn("resp-42", result.completion_evidence_ref)
        self.assertIn(INSTANCE, result.completion_evidence_ref)
        self.assertNotIn(execution_request().request_id, result.completion_evidence_ref)


LIVE_MODEL = "granite-4.0-h-micro"
LIVE_CONTEXT = 1048576

#: Distinguishes "field absent" from "field present but null" in the matrices.
_ABSENT = object()


def live_record(**overrides) -> dict:
    """The observed 2026-08-14 LM Studio `/api/v1/models` record shape.

    Reduced to the fields this boundary reads plus enough surrounding fields to
    keep the shape recognizable. Identity is `key`; the loaded instance carries
    `id` and `config.context_length`; `max_context_length` is model capability.
    """
    record = {
        "type": "llm",
        "publisher": "lmstudio-community",
        "key": LIVE_MODEL,
        "display_name": "Granite 4.0 H Micro",
        "loaded_instances": [{"id": LIVE_MODEL, "config": {"context_length": LIVE_CONTEXT}}],
        "max_context_length": LIVE_CONTEXT,
        "format": "gguf",
    }
    record.update(overrides)
    return record


class LiveProviderContractTests(unittest.TestCase):
    """BC-050-C4: the real LM Studio native v1 model-record contract.

    The C3 boundary matched the record field `id` and read capacity from
    `loaded_instances[].context_length`. The live provider supplies neither,
    so a loaded, reachable model was reported `PROVIDER_MODEL_ABSENT`.
    """

    def _observe(self, document, configured: str = LIVE_MODEL, required: int = 4096):
        return provider(RecordingTransport(inventory=document)).observe(configured, required)

    def _observe_record(self, record: dict, **kwargs):
        return self._observe({"models": [record]}, **kwargs)

    # -- model discovery ---------------------------------------------------

    def test_live_record_is_recognized(self) -> None:
        observation = self._observe_record(live_record())
        self.assertTrue(observation.usable)
        self.assertIsNone(observation.safe_error_code)
        self.assertEqual(observation.observed_model_key, LIVE_MODEL)
        self.assertEqual(observation.model_instance_id, LIVE_MODEL)
        self.assertEqual(observation.observed_context_length, LIVE_CONTEXT)

    def test_live_multi_model_inventory_selects_the_configured_record(self) -> None:
        """Unloaded neighbours in the live inventory must not confuse identity."""
        document = {
            "models": [
                {
                    "type": "llm",
                    "key": "qwen3-coder-next-ream-awq",
                    "display_name": "Qwen3 Coder Next Ream Awq 4bit",
                    "loaded_instances": [],
                    "max_context_length": 262144,
                },
                live_record(),
            ]
        }
        observation = self._observe(document)
        self.assertTrue(observation.usable)
        self.assertEqual(observation.observed_model_key, LIVE_MODEL)

    def test_display_name_is_not_identity(self) -> None:
        observation = self._observe_record(live_record(), configured="Granite 4.0 H Micro")
        self.assertFalse(observation.usable)
        self.assertEqual(observation.safe_error_code, PROVIDER_MODEL_ABSENT)

    def test_record_id_is_not_identity(self) -> None:
        """`id` on a model record is not the native v1 model key."""
        record = live_record(id=LIVE_MODEL)
        del record["key"]
        observation = self._observe_record(record)
        self.assertFalse(observation.usable)
        self.assertEqual(observation.safe_error_code, PROVIDER_MODEL_ABSENT)

    def test_conflicting_record_id_cannot_claim_the_configured_key(self) -> None:
        observation = self._observe_record(live_record(key="some-other-model", id=LIVE_MODEL))
        self.assertFalse(observation.usable)
        self.assertEqual(observation.safe_error_code, PROVIDER_MODEL_ABSENT)

    def test_malformed_record_key_is_absent(self) -> None:
        for value in (None, "", 7, True, ["granite-4.0-h-micro"], {"key": LIVE_MODEL}):
            with self.subTest(value=value):
                observation = self._observe_record(live_record(key=value))
                self.assertFalse(observation.usable)
                self.assertEqual(observation.safe_error_code, PROVIDER_MODEL_ABSENT)

    def test_live_record_without_loaded_instances_is_not_loaded(self) -> None:
        observation = self._observe_record(live_record(loaded_instances=[]))
        self.assertEqual(observation.safe_error_code, PROVIDER_MODEL_NOT_LOADED)

    def test_live_instance_without_identity_is_malformed(self) -> None:
        observation = self._observe_record(
            live_record(loaded_instances=[{"config": {"context_length": LIVE_CONTEXT}}])
        )
        self.assertEqual(observation.safe_error_code, PROVIDER_RESPONSE_MALFORMED)

    # -- observed context evidence -----------------------------------------

    def test_live_loaded_instance_capacity_satisfies_the_request(self) -> None:
        observation = self._observe_record(live_record(), required=4096)
        self.assertTrue(observation.usable)
        self.assertEqual(observation.observed_context_length, LIVE_CONTEXT)

    def _instance(self, config) -> dict:
        instance: dict = {"id": LIVE_MODEL}
        if config is not _ABSENT:
            instance["config"] = config
        return live_record(loaded_instances=[instance])

    def test_missing_or_malformed_context_evidence_is_unknown(self) -> None:
        cases = {
            "missing config": self._instance(_ABSENT),
            "null config": self._instance(None),
            "config not a mapping": self._instance("1048576"),
            "missing context_length": self._instance({"flash_attention": True}),
            "null context_length": self._instance({"context_length": None}),
            "string context_length": self._instance({"context_length": "1048576"}),
            "float context_length": self._instance({"context_length": 4096.0}),
            "boolean context_length": self._instance({"context_length": True}),
            "zero context_length": self._instance({"context_length": 0}),
            "negative context_length": self._instance({"context_length": -1}),
        }
        for label, record in cases.items():
            with self.subTest(case=label):
                observation = self._observe_record(record)
                self.assertFalse(observation.usable)
                self.assertEqual(observation.safe_error_code, PROVIDER_CONTEXT_UNKNOWN)
                self.assertEqual(observation.model_instance_id, LIVE_MODEL)
                self.assertIsNone(observation.observed_context_length)

    def test_observed_capacity_below_request_is_insufficient(self) -> None:
        record = self._instance({"context_length": 2048})
        observation = self._observe_record(record, required=4096)
        self.assertFalse(observation.usable)
        self.assertEqual(observation.safe_error_code, PROVIDER_CONTEXT_INSUFFICIENT)
        self.assertEqual(observation.observed_context_length, 2048)

    def test_model_capability_is_not_loaded_instance_capacity(self) -> None:
        """`max_context_length` describes the model, not the loaded instance."""
        record = self._instance(_ABSENT)
        record["max_context_length"] = LIVE_CONTEXT
        record["loaded_context_length"] = LIVE_CONTEXT
        observation = self._observe_record(record, required=4096)
        self.assertFalse(observation.usable)
        self.assertEqual(observation.safe_error_code, PROVIDER_CONTEXT_UNKNOWN)
        self.assertIsNone(observation.observed_context_length)

    def test_incompatible_live_type_still_rejects(self) -> None:
        observation = self._observe_record(live_record(type="embeddings"))
        self.assertEqual(observation.safe_error_code, PROVIDER_MODEL_INCOMPATIBLE)


LIVE_INSTANCE = f"{LIVE_MODEL}:3"


def live_chat_response(**overrides) -> dict:
    """The observed 2026-08-14 LM Studio `/api/v1/chat` success body.

    Stateless native v1: `model_instance_id`, typed `output`, and `stats`. No
    `status`, no `response_id`, no `completion_id`, no per-completion `id`.
    """
    document = {
        "model_instance_id": LIVE_INSTANCE,
        "output": [
            {
                "type": "message",
                "content": (
                    "Hey there! How can I assist you with the API smoke test? "
                    "Let me know if you have any specific questions or requirements."
                ),
            }
        ],
        "stats": {
            "input_tokens": 30,
            "total_output_tokens": 27,
            "reasoning_output_tokens": 0,
            "tokens_per_second": 172.48979435383404,
            "time_to_first_token_seconds": 0.24348,
        },
    }
    document.update(overrides)
    return document


def live_request(instance_id: str = LIVE_MODEL) -> ModelExecutionRequest:
    return ModelExecutionRequest(
        request_id="live-req-1",
        model_instance_id=instance_id,
        canon_projection_digest="0" * 64,
        turn_request_ref="turn-request:live-req-1",
        control_decision_ref="control-decision:live-req-1",
        system_prompt="ENVELOPE",
        user_input="Hey, Blu.",
        context_budget=16384,
    )


class LiveStatelessCompletionTests(unittest.TestCase):
    """BC-050-C5: the real native-v1 stateless completion contract.

    The C3/C4 boundary required a terminal `status` and a provider-assigned
    completion id. LM Studio native v1 with `stream: false` and `store: false`
    supplies neither, so real completions were rejected as
    `PROVIDER_COMPLETION_UNVERIFIED`.
    """

    def _normalize(self, document, request: ModelExecutionRequest | None = None):
        return provider(RecordingTransport()).normalize_response(
            request or live_request(), document
        )

    # -- the live success ---------------------------------------------------

    def test_live_stateless_response_is_a_completion(self) -> None:
        result = self._normalize(live_chat_response())
        self.assertEqual(result.status, PASS)
        self.assertIn("Hey there!", result.candidate_text)
        self.assertNotEqual(result.safe_error_code, PROVIDER_COMPLETION_UNVERIFIED)
        self.assertNotEqual(result.safe_error_code, PROVIDER_COMPLETION_EVIDENCE_MISSING)
        self.assertIsNone(result.safe_error_code)
        self.assertEqual(result.model_instance_id, LIVE_INSTANCE)

    def test_absent_terminal_status_does_not_block_completion(self) -> None:
        self.assertNotIn("status", live_chat_response())
        self.assertEqual(self._normalize(live_chat_response()).status, PASS)

    def test_absent_provider_identifier_is_stated_not_invented(self) -> None:
        document = live_chat_response()
        for field in ("id", "response_id", "completion_id"):
            self.assertNotIn(field, document)
        result = self._normalize(document)
        self.assertIsNone(result.completion_evidence_ref)
        self.assertEqual(result.completion_proof, COMPLETION_PROOF_SYNCHRONOUS_RESPONSE)

    def test_nothing_in_the_response_is_recycled_as_a_completion_id(self) -> None:
        """No id is manufactured from the instance, the request, or the stats."""
        request = live_request()
        result = self._normalize(live_chat_response(), request)
        self.assertIsNone(result.completion_evidence_ref)
        for forbidden in (LIVE_INSTANCE, LIVE_MODEL, request.request_id, "172.4", "30"):
            self.assertNotIn(forbidden, result.completion_proof)

    def test_statistics_are_never_promoted_into_completion_proof(self) -> None:
        for stats in ({"input_tokens": "many"}, None, [], "ok", {}, {"total_output_tokens": -1}):
            with self.subTest(stats=stats):
                result = self._normalize(live_chat_response(stats=stats))
                self.assertEqual(result.status, PASS)
                self.assertEqual(result.completion_proof, COMPLETION_PROOF_SYNCHRONOUS_RESPONSE)
                self.assertIsNone(result.completion_evidence_ref)

    def test_an_asserted_terminal_state_still_binds(self) -> None:
        """Optional does not mean ignored."""
        for state, expected in (("processing", INVALID), ("failed", UNAVAILABLE)):
            with self.subTest(state=state):
                result = self._normalize(live_chat_response(status=state))
                self.assertEqual(result.status, expected)
                self.assertIsNone(result.candidate_text)

    # -- instance identity --------------------------------------------------

    def test_per_load_instance_ordinal_is_accepted(self) -> None:
        """`/api/v1/models` says `granite-4.0-h-micro`; chat answers `:3`."""
        result = self._normalize(live_chat_response(), live_request(LIVE_MODEL))
        self.assertEqual(result.status, PASS)
        self.assertEqual(result.model_instance_id, LIVE_INSTANCE)

    def test_exact_instance_identity_is_accepted(self) -> None:
        result = self._normalize(
            live_chat_response(model_instance_id=LIVE_MODEL), live_request(LIVE_MODEL)
        )
        self.assertEqual(result.status, PASS)

    def test_a_different_model_is_still_an_identity_mismatch(self) -> None:
        cases = (
            "some-other-model",
            "some-other-model:3",
            "granite-4.0-h-micro-instruct:3",
            "granite-4.0-h:3",
            f"{LIVE_MODEL}:",
            f"prefix-{LIVE_MODEL}:3",
        )
        for identity in cases:
            with self.subTest(identity=identity):
                result = self._normalize(
                    live_chat_response(model_instance_id=identity), live_request(LIVE_MODEL)
                )
                self.assertEqual(result.status, INVALID)
                self.assertEqual(result.safe_error_code, PROVIDER_IDENTITY_MISMATCH)
                self.assertIsNone(result.candidate_text)

    # -- fail-closed on malformed stateless bodies --------------------------

    def test_malformed_live_shaped_responses_fail_closed(self) -> None:
        cases = {
            "none": None,
            "list body": [live_chat_response()],
            "string body": "completed",
            "integer body": 7,
            "empty object": {},
            "missing model_instance_id": {"output": live_chat_response()["output"]},
            "blank model_instance_id": live_chat_response(model_instance_id=""),
            "whitespace model_instance_id": live_chat_response(model_instance_id="   "),
            "null model_instance_id": live_chat_response(model_instance_id=None),
            "non-string model_instance_id": live_chat_response(model_instance_id=7),
            "missing output": {"model_instance_id": LIVE_INSTANCE, "stats": {}},
            "null output": live_chat_response(output=None),
            "object output": live_chat_response(output={}),
            "empty output": live_chat_response(output=[]),
            "non-dict output item": live_chat_response(output=["message"]),
            "untyped output item": live_chat_response(output=[{"content": "Hi."}]),
            "message without content": live_chat_response(output=[{"type": "message"}]),
            "null content": live_chat_response(output=[{"type": "message", "content": None}]),
            "numeric content": live_chat_response(output=[{"type": "message", "content": 7}]),
            "blank content": live_chat_response(output=[{"type": "message", "content": ""}]),
            "whitespace content": live_chat_response(
                output=[{"type": "message", "content": "   \n\t"}]
            ),
            "unsupported kinds only": live_chat_response(
                output=[{"type": "audio", "content": "..."}]
            ),
            "reasoning only": live_chat_response(
                output=[{"type": "reasoning", "content": "thinking"}]
            ),
            "malformed part list": live_chat_response(
                output=[{"type": "message", "content": [{"type": "text"}]}]
            ),
        }
        for label, document in cases.items():
            with self.subTest(case=label):
                result = self._normalize(document)
                self.assertNotEqual(result.status, PASS)
                self.assertIsNone(result.candidate_text)
                self.assertIsNone(result.completion_proof)
                self.assertIsNone(result.completion_evidence_ref)
                self.assertTrue(result.safe_error_code)

    def test_asserted_but_unusable_identifier_still_fails_closed(self) -> None:
        """B-07 is unchanged: malformed evidence is not honest absence."""
        for value in ("", "   ", 7, True, None, ["resp-1"], {"id": "resp-1"}):
            with self.subTest(value=value):
                result = self._normalize(live_chat_response(id=value))
                self.assertEqual(result.status, INVALID)
                self.assertEqual(result.safe_error_code, PROVIDER_COMPLETION_EVIDENCE_MISSING)
                self.assertIsNone(result.candidate_text)
                self.assertIsNone(result.completion_proof)

    def test_a_provider_assigned_identifier_is_used_when_present(self) -> None:
        for field in ("id", "response_id", "completion_id"):
            with self.subTest(field=field):
                result = self._normalize(live_chat_response(**{field: "resp-500"}))
                self.assertEqual(result.status, PASS)
                self.assertEqual(result.completion_proof, COMPLETION_PROOF_PROVIDER_ID)
                self.assertIn("resp-500", result.completion_evidence_ref)
                self.assertIn(LIVE_INSTANCE, result.completion_evidence_ref)
                self.assertNotIn("live-req-1", result.completion_evidence_ref)

    def test_error_body_still_rejects_before_any_text(self) -> None:
        result = self._normalize(live_chat_response(error={"message": "engine failed"}))
        self.assertEqual(result.status, UNAVAILABLE)
        self.assertEqual(result.safe_error_code, PROVIDER_ERROR_REPORTED)
        self.assertIsNone(result.candidate_text)


class InstanceIdentityIsRequiredTests(unittest.TestCase):
    """C5A blocker 1: `model_instance_id` is the only accepted instance identity.

    A response may echo the `model` the request asked for while saying nothing
    about which loaded instance answered. That is not identity evidence, so it
    can no longer stand in for a missing `model_instance_id`.
    """

    def _normalize(self, document, request: ModelExecutionRequest | None = None):
        return provider(RecordingTransport()).normalize_response(
            request or live_request(), document
        )

    def _without_identity(self, **overrides) -> dict:
        document = live_chat_response(**overrides)
        document.pop("model_instance_id", None)
        return document

    def test_missing_instance_identity_fails_closed(self) -> None:
        result = self._normalize(self._without_identity())
        self.assertEqual(result.status, INVALID)
        self.assertEqual(result.safe_error_code, PROVIDER_RESPONSE_MALFORMED)
        self.assertIsNone(result.candidate_text)

    def test_model_field_is_not_accepted_as_instance_identity(self) -> None:
        """The exact substitution C5A closes."""
        document = self._without_identity(model=LIVE_MODEL)
        self.assertEqual(document["model"], LIVE_MODEL)
        result = self._normalize(document, live_request(LIVE_MODEL))
        self.assertEqual(result.status, INVALID)
        self.assertEqual(result.safe_error_code, PROVIDER_RESPONSE_MALFORMED)
        self.assertIsNone(result.candidate_text)
        self.assertIsNone(result.completion_proof)

    def test_model_field_cannot_rescue_a_malformed_instance_identity(self) -> None:
        for value in (None, "", "   ", 7, True, ["granite"], {"id": LIVE_MODEL}):
            with self.subTest(value=value):
                document = live_chat_response(model_instance_id=value, model=LIVE_MODEL)
                result = self._normalize(document, live_request(LIVE_MODEL))
                self.assertEqual(result.status, INVALID)
                self.assertEqual(result.safe_error_code, PROVIDER_RESPONSE_MALFORMED)
                self.assertIsNone(result.candidate_text)

    def test_malformed_instance_identity_types_fail_closed(self) -> None:
        for value in (None, "", " ", "\t\n", 0, 7, True, False, 1.5, [], ["x"], {}, {"a": 1}):
            with self.subTest(value=value):
                result = self._normalize(live_chat_response(model_instance_id=value))
                self.assertEqual(result.status, INVALID)
                self.assertEqual(result.safe_error_code, PROVIDER_RESPONSE_MALFORMED)
                self.assertIsNone(result.candidate_text)
                self.assertIsNone(result.completion_proof)

    def test_valid_instance_identity_still_completes(self) -> None:
        result = self._normalize(live_chat_response())
        self.assertEqual(result.status, PASS)
        self.assertEqual(result.model_instance_id, LIVE_INSTANCE)

    def test_expected_model_consistency_is_unchanged(self) -> None:
        """C5A tightens presence, not the identity agreement rule."""
        result = self._normalize(
            live_chat_response(model_instance_id="some-other-model:3"), live_request(LIVE_MODEL)
        )
        self.assertEqual(result.safe_error_code, PROVIDER_IDENTITY_MISMATCH)


class AssertedCompletionIdentifierTests(unittest.TestCase):
    """C5A blocker 2: every asserted completion id is validated before selection.

    A usable identifier in one field must not conceal a malformed identifier
    the provider asserted in another.
    """

    def _normalize(self, document):
        return provider(RecordingTransport()).normalize_response(live_request(), document)

    def _reject(self, **identifiers) -> None:
        result = self._normalize(live_chat_response(**identifiers))
        self.assertEqual(result.status, INVALID)
        self.assertEqual(result.safe_error_code, PROVIDER_COMPLETION_EVIDENCE_MISSING)
        self.assertIsNone(result.candidate_text)
        self.assertIsNone(result.completion_evidence_ref)
        self.assertIsNone(result.completion_proof)

    def test_valid_identifier_does_not_excuse_a_malformed_sibling(self) -> None:
        self._reject(id="good", response_id=7)

    def test_malformed_first_field_is_not_skipped_for_a_valid_later_one(self) -> None:
        self._reject(id=7, response_id="good")

    def test_blank_sibling_rejects(self) -> None:
        self._reject(id="good", completion_id="")

    def test_null_sibling_rejects(self) -> None:
        self._reject(response_id="good", completion_id=None)

    def test_two_valid_identifiers_do_not_excuse_a_third(self) -> None:
        self._reject(id="good", response_id="also-good", completion_id=[])

    def test_whitespace_sibling_rejects(self) -> None:
        self._reject(id="good", response_id="   ")

    def test_boolean_sibling_rejects(self) -> None:
        self._reject(id="good", response_id=True)

    def test_no_identifier_fields_remains_a_valid_stateless_completion(self) -> None:
        result = self._normalize(live_chat_response())
        self.assertEqual(result.status, PASS)
        self.assertIsNone(result.completion_evidence_ref)
        self.assertEqual(result.completion_proof, COMPLETION_PROOF_SYNCHRONOUS_RESPONSE)

    def test_one_valid_identifier_is_referenced(self) -> None:
        for field in ("id", "response_id", "completion_id"):
            with self.subTest(field=field):
                result = self._normalize(live_chat_response(**{field: "resp-7"}))
                self.assertEqual(result.status, PASS)
                self.assertEqual(result.completion_proof, COMPLETION_PROOF_PROVIDER_ID)
                self.assertIn("resp-7", result.completion_evidence_ref)

    def test_multiple_valid_identifiers_select_deterministically(self) -> None:
        """Selection follows the declared field order: id, response_id, completion_id."""
        result = self._normalize(
            live_chat_response(id="first", response_id="second", completion_id="third")
        )
        self.assertEqual(result.status, PASS)
        self.assertEqual(
            result.completion_evidence_ref,
            f"lm_studio_native_rest_v1:{LIVE_INSTANCE}:first",
        )

        without_id = live_chat_response(response_id="second", completion_id="third")
        self.assertEqual(
            self._normalize(without_id).completion_evidence_ref,
            f"lm_studio_native_rest_v1:{LIVE_INSTANCE}:second",
        )

    def test_a_rejected_identifier_set_never_yields_public_text(self) -> None:
        result = self._normalize(live_chat_response(id="good", response_id=7))
        self.assertIsNone(result.candidate_text)
        self.assertEqual(result.output_kinds, ())
