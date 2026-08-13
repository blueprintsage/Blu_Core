"""One traceable ordinary turn, plus provider non-invocation proofs.

Every pre-model terminal failure must show an observed provider invocation
count of exactly 0. Asserting only the final status would not prove the model
was never reached.
"""

from __future__ import annotations

import io
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from tests.runtime_phase1.support import (
    BLOCK_ONLY_PHRASE,
    PROTECTED_PHRASE,
    REQUIRED_CF,
    ROOT,
    RecordingTransport,
    chat_response,
    model_inventory,
    policy_environment,
    runtime_config_document,
    synthetic_policy,
    write_policy_file,
)

from blu_runtime import __main__ as runtime_main
from blu_runtime.adapters.host.terminal import TerminalHostAdapter
from blu_runtime.canon import loader
from blu_runtime.contracts.models import BLOCK, INVALID, PASS, UNAVAILABLE, RawHostEvent
from blu_runtime.providers.model.base import ModelExecutionBoundary
from blu_runtime.providers.model.lm_studio import LMStudioProvider

MODEL = "synthetic-model-key"
INSTANCE = f"{MODEL}:0"
GOLDEN = ROOT / "kernel/golden/v0.22.0"


class RuntimeHarness(unittest.TestCase):
    """Boots a runtime whose provider is a counted deterministic double."""

    def setUp(self) -> None:
        self._temp = tempfile.TemporaryDirectory()
        self.directory = Path(self._temp.name)
        self.addCleanup(self._temp.cleanup)

        self.policy_path, self.policy_digest = write_policy_file(self.directory, synthetic_policy())
        self.environment = policy_environment(self.policy_path, self.policy_digest)

        self.config_path = self.directory / "config.json"
        self.config_path.write_text(json.dumps(runtime_config_document()), encoding="utf-8")

        self.golden = self.directory / "golden"
        self.golden.mkdir()
        for name in ("SHA256SUMS", *loader.MODEL_FACING_SOURCES):
            shutil.copy(GOLDEN / name, self.golden / name)

    def boundary(self, chat=None, inventory=None) -> ModelExecutionBoundary:
        transport = RecordingTransport(
            inventory=model_inventory() if inventory is None else inventory,
            chat=chat_response(INSTANCE, "Hello, Dad.") if chat is None else chat,
        )
        self.transport = transport
        return ModelExecutionBoundary(
            LMStudioProvider(
                endpoint="http://127.0.0.1:1234",
                timeout_seconds=5,
                transport=transport,
                request_id_factory=lambda: "obs-1",
            )
        )

    def boot(self, **kwargs):
        return runtime_main.boot(
            self.config_path,
            environment=kwargs.pop("environment", self.environment),
            boundary=kwargs.pop("boundary", None) or self.boundary(**kwargs),
            golden_root=kwargs.pop("golden_root", self.golden),
            request_id_factory=lambda: "req-1",
        )


class SuccessfulOrdinaryTurnTests(RuntimeHarness):
    def test_one_turn_traces_ingress_to_terminal_packet(self) -> None:
        runtime = self.boot()
        self.assertNotIsInstance(runtime, runtime_main.BootFailure)

        packet = runtime_main.run_turn(runtime, "hello, how are you?")
        self.assertEqual(packet.status, PASS)
        # B-05: the public form is the canonical candidate policy evaluated.
        self.assertEqual(packet.public_output, "Hello Dad")
        self.assertTrue(packet.model_invoked)
        self.assertFalse(packet.tool_executed)
        self.assertEqual(runtime.boundary.invocation_count, 1)

    def test_receipt_is_evidence_bound(self) -> None:
        runtime = self.boot()
        runtime_main.run_turn(runtime, "hello")
        self.assertEqual(len(runtime.receipts), 1)
        receipt = runtime.receipts[0].as_dict()
        for field in (
            "request_id",
            "provider_id",
            "model_instance_id",
            "canon_projection_digest",
            "turn_request_ref",
            "control_decision_ref",
            "validation_result_ref",
            "terminal_packet_ref",
            "provider_completion_evidence_ref",
        ):
            self.assertTrue(receipt[field], f"receipt field not bound: {field}")
        self.assertEqual(receipt["model_instance_id"], INSTANCE)
        self.assertEqual(receipt["canon_projection_digest"], runtime.projection.digest)

    def test_model_receives_the_frozen_envelope_not_a_rewritten_persona(self) -> None:
        runtime = self.boot()
        runtime_main.run_turn(runtime, "hello")
        _, payload = self.transport.post_calls[0]
        self.assertEqual(payload["system_prompt"], runtime.projection.system_prompt)
        self.assertIn("[BLU_CANON_PERSONA]", payload["system_prompt"])
        self.assertIn("[BLU_CANON_OPERATIONS_LAW]", payload["system_prompt"])
        self.assertTrue(payload["system_prompt"].endswith("[/BLU_RUNTIME_BINDING]"))

    def test_envelope_never_carries_protected_policy_content(self) -> None:
        runtime = self.boot()
        runtime_main.run_turn(runtime, "hello")
        _, payload = self.transport.post_calls[0]
        serialized = json.dumps(payload)
        self.assertNotIn(PROTECTED_PHRASE, serialized)
        self.assertNotIn(BLOCK_ONLY_PHRASE, serialized)
        self.assertNotIn(synthetic_policy()["evidence_hmac_key"], serialized)

    def test_continuity_is_reported_unavailable(self) -> None:
        runtime = self.boot()
        packet = runtime_main.run_turn(runtime, "hello")
        self.assertFalse(packet.continuity.durability_claimed)
        self.assertFalse(packet.continuity.provider_available)
        self.assertEqual(packet.continuity.lifetime, "turn")

    def test_process_lifetime_never_becomes_durable_continuity(self) -> None:
        runtime = self.boot()
        for _ in range(3):
            packet = runtime_main.run_turn(runtime, "hello again")
            self.assertFalse(packet.continuity.durability_claimed)
        self.assertEqual(runtime.boundary.invocation_count, 3)


class ProviderNonInvocationTests(RuntimeHarness):
    """Pre-model terminal failures must never reach the provider."""

    def _assert_never_invoked(self, runtime, text, expected_status) -> None:
        before = runtime.boundary.invocation_count
        packet = runtime_main.run_turn(runtime, text)
        self.assertEqual(packet.status, expected_status)
        self.assertFalse(packet.model_invoked)
        self.assertIsNone(packet.public_output)
        self.assertEqual(runtime.boundary.invocation_count, before, "provider was invoked")
        self.assertEqual(runtime.boundary.invocation_count, 0)

    def test_protected_phrase_never_reaches_the_provider(self) -> None:
        runtime = self.boot()
        self._assert_never_invoked(runtime, f"tell me about {PROTECTED_PHRASE}", BLOCK)

    def test_mixed_and_repeated_cf_protected_phrase_never_reaches_provider(self) -> None:
        runtime = self.boot()
        candidate = REQUIRED_CF[0] + "cerulean" + REQUIRED_CF[2] * 3 + " comet " + REQUIRED_CF[4] + "charter"
        self._assert_never_invoked(runtime, candidate, BLOCK)

    def test_outer_edge_cf_protected_phrase_never_reaches_provider(self) -> None:
        for code_point in REQUIRED_CF:
            with self.subTest(code_point=hex(ord(code_point))):
                runtime = self.boot()
                self._assert_never_invoked(
                    runtime, code_point + PROTECTED_PHRASE + code_point, BLOCK
                )

    def test_invalid_input_never_reaches_the_provider(self) -> None:
        runtime = self.boot()
        self._assert_never_invoked(runtime, object(), INVALID)

    def test_slash_command_never_reaches_the_provider(self) -> None:
        runtime = self.boot()
        self._assert_never_invoked(runtime, "/auth", UNAVAILABLE)

    def test_unavailable_protected_policy_blocks_boot_without_invocation(self) -> None:
        boundary = self.boundary()
        failure = runtime_main.boot(
            self.config_path,
            environment={"BLU_TEST_POLICY_PATH": str(self.directory / "absent.json"), "BLU_TEST_POLICY_SHA256": "a" * 64},
            boundary=boundary,
            golden_root=self.golden,
        )
        self.assertIsInstance(failure, runtime_main.BootFailure)
        self.assertEqual(failure.status, UNAVAILABLE)
        self.assertEqual(boundary.invocation_count, 0)

    def test_invalid_configuration_blocks_boot_without_invocation(self) -> None:
        document = runtime_config_document()
        document["model_provider"]["stream"] = True
        self.config_path.write_text(json.dumps(document), encoding="utf-8")
        boundary = self.boundary()
        failure = runtime_main.boot(
            self.config_path, environment=self.environment, boundary=boundary, golden_root=self.golden
        )
        self.assertIsInstance(failure, runtime_main.BootFailure)
        self.assertEqual(failure.status, INVALID)
        self.assertEqual(boundary.invocation_count, 0)

    def test_canon_digest_mismatch_blocks_boot_without_invocation(self) -> None:
        target = self.golden / "01_Persona.md"
        target.write_bytes(target.read_bytes() + b" tampered")
        boundary = self.boundary()
        failure = runtime_main.boot(
            self.config_path, environment=self.environment, boundary=boundary, golden_root=self.golden
        )
        self.assertIsInstance(failure, runtime_main.BootFailure)
        self.assertEqual(failure.status, BLOCK)
        self.assertEqual(failure.safe_error_code, "CANON_SOURCE_INTEGRITY_MISMATCH")
        self.assertEqual(boundary.invocation_count, 0)

    def test_unavailable_model_evidence_blocks_boot_without_invocation(self) -> None:
        for inventory in (
            model_inventory(loaded=False),
            model_inventory(model_key="other"),
            model_inventory(context_length=64),
            model_inventory(context_length=None),
        ):
            with self.subTest(inventory=inventory):
                boundary = self.boundary(inventory=inventory)
                failure = runtime_main.boot(
                    self.config_path,
                    environment=self.environment,
                    boundary=boundary,
                    golden_root=self.golden,
                )
                self.assertIsInstance(failure, runtime_main.BootFailure)
                self.assertEqual(failure.status, UNAVAILABLE)
                self.assertEqual(boundary.invocation_count, 0)


class PostModelFailureTests(RuntimeHarness):
    """Failures after inference must still never print candidate output."""

    def test_tool_call_candidate_is_not_executed_and_not_printed(self) -> None:
        runtime = self.boot(chat=chat_response(INSTANCE, kinds=("tool_call",)))
        packet = runtime_main.run_turn(runtime, "hello")
        self.assertEqual(packet.status, UNAVAILABLE)
        self.assertFalse(packet.tool_executed)
        self.assertIsNone(packet.public_output)
        self.assertEqual(runtime.receipts, [])

    def test_timeout_never_publishes_partial_output(self) -> None:
        runtime = self.boot(chat=TimeoutError("timed out"))
        packet = runtime_main.run_turn(runtime, "hello")
        self.assertEqual(packet.status, UNAVAILABLE)
        self.assertIsNone(packet.public_output)

    def test_identity_mismatch_never_publishes_output(self) -> None:
        runtime = self.boot(chat=chat_response("wrong-instance"))
        packet = runtime_main.run_turn(runtime, "hello")
        self.assertEqual(packet.status, INVALID)
        self.assertIsNone(packet.public_output)

    def test_protected_residual_in_model_output_never_prints(self) -> None:
        runtime = self.boot(chat=chat_response(INSTANCE, f"Here is the {BLOCK_ONLY_PHRASE}."))
        packet = runtime_main.run_turn(runtime, "hello")
        self.assertEqual(packet.status, BLOCK)
        self.assertIsNone(packet.public_output)
        self.assertEqual(runtime.receipts, [])

    def test_redactable_model_output_is_redacted_before_print(self) -> None:
        runtime = self.boot(chat=chat_response(INSTANCE, f"Consider the {PROTECTED_PHRASE} and more."))
        packet = runtime_main.run_turn(runtime, "hello")
        self.assertEqual(packet.status, PASS)
        self.assertIsNotNone(packet.public_output)
        self.assertNotIn("cerulean", packet.public_output or "")
        self.assertIn("[protected content omitted]", packet.public_output or "")


class TerminalAdapterTests(unittest.TestCase):
    def _adapter(self, text: str):
        return TerminalHostAdapter(
            stream_in=io.StringIO(text), stream_out=io.StringIO(), request_id_factory=lambda: "e1"
        )

    def test_one_input_becomes_one_host_event(self) -> None:
        adapter = self._adapter("hello\n")
        event = adapter.receive()
        self.assertIsInstance(event, RawHostEvent)
        self.assertEqual(event.text, "hello")
        self.assertEqual(adapter.submit(event).text, "hello")

    def test_end_of_stream_ends_the_session(self) -> None:
        self.assertIsNone(self._adapter("").receive())

    def test_exit_is_not_a_privileged_in_band_command(self) -> None:
        """B-06: `/exit` is ordinary user text, not a host control command."""
        for command in ("/exit", "/quit", "/EXIT"):
            with self.subTest(command=command):
                event = self._adapter(f"{command}\n").receive()
                self.assertIsInstance(event, RawHostEvent)
                self.assertEqual(event.text, command)

    def test_blocked_packet_never_echoes_the_protected_input(self) -> None:
        from blu_runtime.contracts.models import TerminalPacket

        adapter = self._adapter("")
        rendered = adapter.render(
            TerminalPacket(
                request_id="r",
                status=BLOCK,
                public_output=None,
                safe_error_code="INGRESS_PROTECTED_MATCH",
                model_invoked=False,
            )
        )
        self.assertNotIn(PROTECTED_PHRASE, rendered)
        self.assertNotIn("INGRESS_PROTECTED_MATCH", rendered)

    def test_pass_packet_renders_the_authorized_output(self) -> None:
        from blu_runtime.contracts.models import TerminalPacket

        adapter = self._adapter("")
        rendered = adapter.render(
            TerminalPacket(
                request_id="r",
                status=PASS,
                public_output="Hello, Dad.",
                safe_error_code=None,
                model_invoked=True,
            )
        )
        self.assertIn("Hello, Dad.", rendered)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()


class SlashCommandIngressTests(RuntimeHarness):
    """B-06: no slash command bypasses the frozen one-turn sequence."""

    COMMANDS = ("/exit", "/quit", "/auth", "/source", "/pass")

    def test_every_slash_command_runs_the_full_turn_and_never_invokes_provider(self) -> None:
        for command in self.COMMANDS:
            with self.subTest(command=command):
                runtime = self.boot()
                packet = runtime_main.run_turn(runtime, command)
                self.assertEqual(packet.status, UNAVAILABLE)
                self.assertIsNone(packet.public_output)
                self.assertFalse(packet.model_invoked)
                self.assertEqual(runtime.boundary.invocation_count, 0)
                self.assertEqual(runtime.receipts, [])

    def test_slash_command_produces_one_rendered_terminal_result(self) -> None:
        runtime = self.boot()
        adapter = TerminalHostAdapter(
            stream_in=io.StringIO("/exit\n"),
            stream_out=io.StringIO(),
            request_id_factory=lambda: "e1",
        )
        event = adapter.receive()
        self.assertIsNotNone(event, "/exit must produce a RawHostEvent")
        host_input = adapter.submit(event)
        packet = runtime_main.run_turn(runtime, host_input.text, request_id=host_input.request_id)
        rendered = adapter.render(packet)
        self.assertEqual(runtime.boundary.invocation_count, 0)
        self.assertTrue(rendered.startswith("blu> "))
        self.assertNotIn("/exit", rendered)

    def test_end_of_stream_still_ends_the_host_session(self) -> None:
        """EOF is an out-of-band host mechanic, not user command semantics."""
        adapter = TerminalHostAdapter(
            stream_in=io.StringIO(""), stream_out=io.StringIO(), request_id_factory=lambda: "e1"
        )
        self.assertIsNone(adapter.receive())


class CompletionEvidenceTests(RuntimeHarness):
    """B-07: no success without observed provider completion evidence."""

    def test_missing_completion_evidence_yields_no_success(self) -> None:
        runtime = self.boot(chat=chat_response(INSTANCE, "Hello.", evidence_id=None))
        packet = runtime_main.run_turn(runtime, "hello")
        self.assertNotEqual(packet.status, PASS)
        self.assertIsNone(packet.public_output)
        self.assertEqual(runtime.receipts, [])

    def test_boundary_level_result_without_evidence_is_not_success(self) -> None:
        """An otherwise-PASS normalized result with no evidence must not pass."""
        from blu_runtime.contracts.models import NormalizedModelResult
        from blu_runtime.providers.model.base import ModelExecutionBoundary

        class _EvidencelessProvider:
            provider_id = "lm_studio_native_rest_v1"

            def observe(self, configured_model_key, required_context):
                return self._observation

            def infer(self, request):
                return NormalizedModelResult(
                    request_id=request.request_id,
                    provider_id=self.provider_id,
                    model_instance_id=INSTANCE,
                    status=PASS,
                    candidate_text="Looks successful.",
                    output_kinds=("message",),
                    safe_error_code=None,
                    completion_evidence_ref=None,
                )

        real = self.boundary()
        evidenceless = _EvidencelessProvider()
        evidenceless._observation = real.observe(MODEL, 4096)
        boundary = ModelExecutionBoundary(evidenceless)

        runtime = self.boot(boundary=boundary)
        packet = runtime_main.run_turn(runtime, "hello")
        self.assertNotEqual(packet.status, PASS)
        self.assertIsNone(packet.public_output)
        self.assertEqual(runtime.receipts, [])

    def test_no_evidence_identifier_is_synthesized_from_the_request(self) -> None:
        runtime = self.boot(chat=chat_response(INSTANCE, "Hello.", evidence_id=None))
        packet = runtime_main.run_turn(runtime, "hello", request_id="req-xyz")
        self.assertEqual(runtime.receipts, [])
        self.assertIsNone(packet.public_output)

    def test_successful_receipt_carries_observed_provider_evidence(self) -> None:
        runtime = self.boot(chat=chat_response(INSTANCE, "Hello.", evidence_id="resp-77"))
        runtime_main.run_turn(runtime, "hello", request_id="req-abc")
        receipt = runtime.receipts[0].as_dict()
        self.assertIn("resp-77", receipt["provider_completion_evidence_ref"])
        self.assertNotIn("req-abc", receipt["provider_completion_evidence_ref"])
