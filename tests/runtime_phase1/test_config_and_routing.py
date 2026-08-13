"""Configuration validation, Turn Controller route lock, and egress law."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tests.runtime_phase1.support import (
    BLOCK_ONLY_PHRASE,
    PROTECTED_PHRASE,
    REQUIRED_CF,
    runtime_config_document,
    synthetic_policy,
)

from blu_runtime import config as configuration
from blu_runtime.contracts.models import (
    PASS,
    ROUTE_UNSUPPORTED,
    SECURITY_DECISION_NOT_EXECUTABLE,
    UNAVAILABLE,
    SecurityDecision,
)
from blu_runtime.core import turn_controller
from blu_runtime.core import validation_egress
from blu_runtime.core.security_restraint import EGRESS_PROTECTED_MATCH


class ConfigurationTests(unittest.TestCase):
    def setUp(self) -> None:
        self._temp = tempfile.TemporaryDirectory()
        self.directory = Path(self._temp.name)
        self.addCleanup(self._temp.cleanup)

    def _write(self, document: object) -> Path:
        target = self.directory / "config.json"
        target.write_text(json.dumps(document), encoding="utf-8")
        return target

    def test_valid_configuration_projects_typed_record(self) -> None:
        settings = configuration.load(self._write(runtime_config_document()))
        self.assertEqual(settings.selected_model, "synthetic-model-key")
        self.assertFalse(settings.stream)
        self.assertFalse(settings.store)
        self.assertEqual(settings.protected_policy_ref.kind, "environment_file")

    def test_missing_file_is_invalid(self) -> None:
        with self.assertRaises(configuration.ConfigError):
            configuration.load(self.directory / "absent.json")

    def test_malformed_json_is_invalid(self) -> None:
        target = self.directory / "config.json"
        target.write_text("{not json", encoding="utf-8")
        with self.assertRaises(configuration.ConfigError):
            configuration.load(target)

    def test_streaming_is_rejected_by_contract(self) -> None:
        document = runtime_config_document()
        document["model_provider"]["stream"] = True
        with self.assertRaises(configuration.ConfigError):
            configuration.load(self._write(document))

    def test_provider_side_storage_is_rejected_by_contract(self) -> None:
        document = runtime_config_document()
        document["model_provider"]["store"] = True
        with self.assertRaises(configuration.ConfigError):
            configuration.load(self._write(document))

    def test_protected_routes_cannot_be_enabled(self) -> None:
        document = runtime_config_document()
        document["development"]["allow_protected_routes"] = True
        with self.assertRaises(configuration.ConfigError):
            configuration.load(self._write(document))

    def test_unverified_capabilities_cannot_be_enabled(self) -> None:
        document = runtime_config_document()
        document["development"]["allow_unverified_capabilities"] = True
        with self.assertRaises(configuration.ConfigError):
            configuration.load(self._write(document))

    def test_missing_protected_policy_reference_is_invalid(self) -> None:
        document = runtime_config_document()
        del document["runtime"]["protected_policy_ref"]
        with self.assertRaises(configuration.ConfigError):
            configuration.load(self._write(document))

    def test_configuration_holds_no_policy_payload(self) -> None:
        settings = configuration.load(self._write(runtime_config_document()))
        serialized = json.dumps(settings.raw)
        self.assertNotIn(PROTECTED_PHRASE, serialized)
        self.assertIn("locator_env", serialized)


class TurnControllerTests(unittest.TestCase):
    def _pass(self) -> SecurityDecision:
        return SecurityDecision(
            decision=PASS, eligible_for_turn_controller=True, safe_error_code=None, evidence={}
        )

    def _blocked(self) -> SecurityDecision:
        return SecurityDecision(
            decision="BLOCK", eligible_for_turn_controller=False, safe_error_code="X", evidence={}
        )

    def _ask(self) -> SecurityDecision:
        return SecurityDecision(
            decision="ASK", eligible_for_turn_controller=True, safe_error_code=None, evidence={}
        )

    def test_ordinary_conversation_locks_route_owner_and_scope(self) -> None:
        decision = turn_controller.control("r1", self._pass(), "hello there")
        self.assertEqual(decision.status, PASS)
        self.assertEqual(decision.route, "ordinary_conversation")
        self.assertEqual(decision.owner, "model_execution_boundary")
        self.assertEqual(decision.scope_lock, turn_controller.SCOPE_LOCK)
        self.assertFalse(decision.side_effects)

    def test_non_pass_decision_cannot_enter(self) -> None:
        decision = turn_controller.control("r2", self._blocked(), "hello")
        self.assertEqual(decision.status, UNAVAILABLE)
        self.assertEqual(decision.safe_error_code, SECURITY_DECISION_NOT_EXECUTABLE)

    def test_unexpected_ask_is_not_executable(self) -> None:
        """Phase 1 generates no ASK; an unexpected one must terminate safely."""
        decision = turn_controller.control("r3", self._ask(), "hello")
        self.assertEqual(decision.status, UNAVAILABLE)
        self.assertEqual(decision.safe_error_code, SECURITY_DECISION_NOT_EXECUTABLE)

    def test_slash_commands_are_unsupported(self) -> None:
        for text in ("/auth", "/help", "  /source", "/pass"):
            with self.subTest(text=text):
                decision = turn_controller.control("r4", self._pass(), text)
                self.assertEqual(decision.status, UNAVAILABLE)
                self.assertEqual(decision.safe_error_code, ROUTE_UNSUPPORTED)

    def test_no_route_other_than_ordinary_conversation_is_executable(self) -> None:
        self.assertNotIn("ordinary_conversation", turn_controller.UNSUPPORTED_ROUTES)
        self.assertEqual(turn_controller.select_route("plain text"), "ordinary_conversation")


class ValidationEgressTests(unittest.TestCase):
    def setUp(self) -> None:
        self.policy = synthetic_policy()

    def test_clear_output_is_printable(self) -> None:
        result = validation_egress.evaluate_egress("r", "an ordinary reply", self.policy)
        self.assertEqual(result.egress_result, "CLEAR")
        self.assertTrue(result.eligible_for_print)
        self.assertEqual(result.public_output, "an ordinary reply")

    def test_redactable_match_is_redacted_and_rescanned(self) -> None:
        result = validation_egress.evaluate_egress(
            "r", f"the answer involves {PROTECTED_PHRASE} today", self.policy
        )
        self.assertEqual(result.egress_result, "REDACTED")
        self.assertTrue(result.eligible_for_print)
        self.assertIn("[protected content omitted]", result.public_output or "")
        self.assertNotIn("cerulean", result.public_output or "")

    def test_block_rule_is_never_redacted(self) -> None:
        result = validation_egress.evaluate_egress("r", f"about {BLOCK_ONLY_PHRASE}", self.policy)
        self.assertEqual(result.egress_result, "BLOCKED")
        self.assertFalse(result.eligible_for_print)
        self.assertIsNone(result.public_output)
        self.assertEqual(result.safe_error_code, EGRESS_PROTECTED_MATCH)

    def test_residual_without_alphanumeric_content_is_blocked(self) -> None:
        result = validation_egress.evaluate_egress("r", PROTECTED_PHRASE, self.policy)
        self.assertEqual(result.egress_result, "BLOCKED")
        self.assertIsNone(result.public_output)

    def test_every_cf_attack_shape_is_caught_at_egress(self) -> None:
        for code_point in REQUIRED_CF:
            candidates = (
                code_point + PROTECTED_PHRASE,
                PROTECTED_PHRASE + code_point,
                code_point + PROTECTED_PHRASE + code_point,
                code_point.join(PROTECTED_PHRASE.split(" ")),
            )
            for candidate in candidates:
                with self.subTest(code_point=hex(ord(code_point))):
                    result = validation_egress.evaluate_egress("r", f"text {candidate} tail", self.policy)
                    self.assertIn(result.egress_result, {"REDACTED", "BLOCKED"})
                    if result.public_output is not None:
                        self.assertNotIn("cerulean", result.public_output)

    def test_unusable_policy_is_never_printable(self) -> None:
        result = validation_egress.evaluate_egress("r", "anything", None, "POLICY_INTEGRITY_MISMATCH")
        self.assertEqual(result.egress_result, UNAVAILABLE)
        self.assertFalse(result.eligible_for_print)
        self.assertIsNone(result.public_output)

    def test_non_string_candidate_is_invalid(self) -> None:
        result = validation_egress.evaluate_egress("r", object(), self.policy)
        self.assertFalse(result.eligible_for_print)
        self.assertIsNone(result.public_output)

    def test_evidence_never_carries_matched_text(self) -> None:
        result = validation_egress.evaluate_egress("r", f"about {BLOCK_ONLY_PHRASE}", self.policy)
        serialized = json.dumps(result.evidence)
        self.assertNotIn(BLOCK_ONLY_PHRASE, serialized)
        self.assertNotIn(self.policy["evidence_hmac_key"], serialized)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()


class CanonicalEgressOutputTests(unittest.TestCase):
    """B-05: CLEAR publishes the canonical candidate policy evaluated."""

    def setUp(self) -> None:
        self.policy = synthetic_policy()

    def _clear(self, text: str):
        result = validation_egress.evaluate_egress("r", text, self.policy)
        self.assertEqual(result.egress_result, "CLEAR")
        self.assertTrue(result.eligible_for_print)
        return result

    def test_harmless_cf_is_not_published(self) -> None:
        """Codex's reproduction: raw `ordinary<U+200B> reply` must not print."""
        result = self._clear("ordinary​ reply")
        self.assertEqual(result.public_output, "ordinary reply")
        for code_point in REQUIRED_CF:
            self.assertNotIn(code_point, result.public_output)

    def test_every_required_cf_is_stripped_from_public_output(self) -> None:
        for code_point in REQUIRED_CF:
            with self.subTest(code_point=hex(ord(code_point))):
                result = self._clear(f"safe{code_point} text")
                self.assertNotIn(code_point, result.public_output)

    def test_separator_normalization_is_published(self) -> None:
        self.assertEqual(self._clear("a.b,c:d").public_output, "a b c d")

    def test_collapsible_whitespace_is_published_collapsed(self) -> None:
        self.assertEqual(self._clear("  spaced   out  ").public_output, "spaced out")

    def test_nfkc_forms_are_published_normalized(self) -> None:
        self.assertEqual(self._clear("ﬁre").public_output, "fire")

    def test_combined_normalization(self) -> None:
        result = self._clear("  ﬁre​:  bright  ")
        self.assertEqual(result.public_output, "fire bright")

    def test_public_output_equals_the_evaluated_candidate(self) -> None:
        from blu_runtime.core.security_restraint import normalized_match_candidate

        for text in ("plain", "a​b", " x , y ", "ﬁn"):
            with self.subTest(text=text.encode("unicode_escape").decode()):
                result = self._clear(text)
                self.assertEqual(
                    result.public_output, normalized_match_candidate(text)["normalized"]
                )

    def test_protected_content_still_redacts_after_canonicalization(self) -> None:
        result = validation_egress.evaluate_egress(
            "r", f"see {PROTECTED_PHRASE} now", self.policy
        )
        self.assertEqual(result.egress_result, "REDACTED")
        self.assertNotIn("cerulean", result.public_output or "")

    def test_protected_content_still_blocks_after_canonicalization(self) -> None:
        result = validation_egress.evaluate_egress("r", BLOCK_ONLY_PHRASE, self.policy)
        self.assertEqual(result.egress_result, "BLOCKED")
        self.assertIsNone(result.public_output)

    def test_cf_obfuscated_protected_content_never_becomes_clear(self) -> None:
        for code_point in REQUIRED_CF:
            for candidate in (
                code_point + PROTECTED_PHRASE,
                PROTECTED_PHRASE + code_point,
                code_point.join(PROTECTED_PHRASE.split(" ")),
            ):
                with self.subTest(code_point=hex(ord(code_point))):
                    result = validation_egress.evaluate_egress("r", candidate, self.policy)
                    self.assertNotEqual(result.egress_result, "CLEAR")
