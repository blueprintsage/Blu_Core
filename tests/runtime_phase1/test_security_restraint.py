"""Pre-ingress Security Restraint: C1 obligations and policy fail-closed law.

Carries BC-041-C1 N-1 (provenance invariant) and N-2 (bounded construction)
into production, and proves the optimized construction did not drift from the
approved reference semantics.
"""

from __future__ import annotations

import itertools
import json
import random
import tempfile
import time
import unittest
from pathlib import Path

from tests.runtime_phase1.support import (
    BLOCK_ONLY_PHRASE,
    PROTECTED_PHRASE,
    REQUIRED_CF,
    load_reference,
    policy_environment,
    policy_reference,
    synthetic_policy,
    write_policy_file,
)

from blu_runtime.contracts.models import BLOCK, PASS
from blu_runtime.core import security_restraint as restraint

REFERENCE = load_reference()


def _cf_variants(phrase: str, code_point: str):
    """Every attack shape the C1 corpus requires, for one code point."""
    words = phrase.split(" ")
    yield "leading_outer_edge", code_point + phrase
    yield "trailing_outer_edge", phrase + code_point
    yield "both_outer_edges", code_point + phrase + code_point
    yield "inter_word", (" " + code_point).join(words)
    yield "inter_word_unseparated", code_point.join(words)
    yield "inside_token", phrase[:4] + code_point + phrase[4:]
    yield "repeated_interior", (code_point * 3).join(words)
    yield "repeated_outer_edge", code_point * 3 + phrase + code_point * 3
    yield "outer_plus_interior", code_point + phrase[:4] + code_point + phrase[4:]
    yield "saturated", code_point.join(phrase)
    yield "self_repetition", phrase + code_point + phrase


class ProvenanceDifferentialTests(unittest.TestCase):
    """Production output must equal the C1 reference, pair for pair."""

    def _assert_equivalent(self, value: str, label: str = "") -> None:
        produced = restraint.normalized_match_candidate(value)
        expected = REFERENCE.normalized_match_candidate(value)
        self.assertEqual(produced["normalized"], expected["normalized"], label)
        self.assertEqual(
            sorted(produced["removed_cf_boundaries"]),
            expected["removed_cf_boundaries"],
            label,
        )

    def test_required_code_points_across_every_attack_shape(self) -> None:
        for code_point in REQUIRED_CF:
            for shape, candidate in _cf_variants(PROTECTED_PHRASE, code_point):
                with self.subTest(code_point=hex(ord(code_point)), shape=shape):
                    self._assert_equivalent(candidate, shape)

    def test_mixed_code_points(self) -> None:
        for combination in itertools.permutations(REQUIRED_CF, 3):
            candidate = combination[0] + "cerulean" + combination[1] + " comet " + combination[2] + "charter"
            self._assert_equivalent(candidate, "mixed_code_points")

    def test_surrounding_context_variants(self) -> None:
        contexts = ("", "prefix ", " suffix", "_", ".", "  ", "ünïcode ")
        for code_point, before, after in itertools.product(REQUIRED_CF, contexts, contexts):
            candidate = before + code_point + PROTECTED_PHRASE + code_point + after
            self._assert_equivalent(candidate)

    def test_false_positive_corpus(self) -> None:
        """Ordinary text must normalize identically and stay unmatched."""
        corpus = [
            "",
            "hello world",
            "cerulean",
            "comet charter",
            "cerulean comet",
            "the charter was ceruleanish",
            "a_b.c/d|e",
            "ﬁre ①  Ａ",
            "é combining",
            "  leading and trailing  ",
            "cerulean  comet  charter is discussed elsewhere",
        ]
        for candidate in corpus:
            with self.subTest(candidate=candidate):
                self._assert_equivalent(candidate)

    def test_generated_multi_placement_cases(self) -> None:
        """Randomized multi-placement cases beyond the pinned fixtures."""
        alphabet = list("abcXY 09_.-/|:;,\\") + ["é", "ﬁ", "①", "Ａ", "́", "　", "\t", "カ", "̸"]
        rng = random.Random(20260812)
        for _ in range(4000):
            length = rng.randint(0, 14)
            candidate = "".join(rng.choice(alphabet + list(REQUIRED_CF) * 2) for _ in range(length))
            self._assert_equivalent(candidate)

    def test_generated_multi_placement_inside_protected_phrase(self) -> None:
        rng = random.Random(4104)
        for _ in range(3000):
            characters = list(PROTECTED_PHRASE)
            for _ in range(rng.randint(1, 6)):
                position = rng.randint(0, len(characters))
                characters.insert(position, rng.choice(REQUIRED_CF))
            self._assert_equivalent("".join(characters))


class ProvenanceInvariantTests(unittest.TestCase):
    """BC-041-C1 N-1: provenance must never be silently discarded."""

    def test_cf_between_word_characters_always_yields_provenance(self) -> None:
        for code_point in REQUIRED_CF:
            for left, right in itertools.product("aZ9é", "aZ9é"):
                candidate = left + code_point + right
                with self.subTest(code_point=hex(ord(code_point)), pair=left + right):
                    result = restraint.normalized_match_candidate(candidate)
                    self.assertTrue(
                        result["removed_cf_boundaries"],
                        "a removed Cf flanked by word characters must yield a boundary offset",
                    )

    def test_invariant_holds_for_repeated_removals(self) -> None:
        for code_point in REQUIRED_CF:
            candidate = "a" + code_point * 5 + "b" + code_point * 2 + "c"
            result = restraint.normalized_match_candidate(candidate)
            self.assertEqual(result["normalized"], "abc")
            self.assertEqual(result["removed_cf_boundaries"], [1, 2])


class ProvenanceBoundednessTests(unittest.TestCase):
    """BC-041-C1 N-2: production must not reproduce quadratic behavior."""

    def _elapsed(self, removals: int) -> float:
        candidate = ("a" + "​") * removals + "b"
        start = time.perf_counter()
        restraint.normalized_match_candidate(candidate)
        return time.perf_counter() - start

    def test_cf_saturated_input_scales_sub_quadratically(self) -> None:
        small = max(self._elapsed(500), 1e-4)
        large = self._elapsed(4000)
        # An 8x input growth under a quadratic construction costs ~64x. A
        # generous ceiling still separates linear from quadratic decisively.
        self.assertLess(large / small, 20.0, f"growth ratio {large / small:.1f} suggests quadratic behavior")

    def test_saturated_input_completes_promptly(self) -> None:
        self.assertLess(self._elapsed(8000), 2.0)


class NormalizationContractTests(unittest.TestCase):
    def test_non_string_input_is_rejected(self) -> None:
        for value in (None, 7, b"bytes", ["list"]):
            with self.assertRaises(TypeError):
                restraint.normalized_match_candidate(value)

    def test_separator_set_maps_to_space(self) -> None:
        result = restraint.normalized_match_candidate("a.b,c:d;e-f_g/h\\i|j")
        self.assertEqual(result["normalized"], "a b c d e f g h i j")


class PolicyBootGateTests(unittest.TestCase):
    """The policy gate fails closed at every stage."""

    def setUp(self) -> None:
        self._temp = tempfile.TemporaryDirectory()
        self.directory = Path(self._temp.name)
        self.addCleanup(self._temp.cleanup)

    def test_usable_policy_completes_every_stage(self) -> None:
        path, digest = write_policy_file(self.directory, synthetic_policy())
        load = restraint.load_policy(policy_reference(), policy_environment(path, digest))
        self.assertTrue(load.usable)
        self.assertIsNone(load.error_code)
        self.assertTrue(all(load.stages.values()))

    def test_missing_reference(self) -> None:
        load = restraint.load_policy(None, {})
        self.assertFalse(load.usable)
        self.assertEqual(load.error_code, restraint.POLICY_REF_MISSING)
        self.assertFalse(load.stages["reference_configured"])

    def test_target_unavailable(self) -> None:
        load = restraint.load_policy(
            policy_reference(),
            {"BLU_TEST_POLICY_PATH": str(self.directory / "absent.json"), "BLU_TEST_POLICY_SHA256": "a" * 64},
        )
        self.assertFalse(load.usable)
        self.assertEqual(load.error_code, restraint.POLICY_TARGET_UNAVAILABLE)

    def test_malformed_payload(self) -> None:
        path, digest = write_policy_file(self.directory, "{not json")
        load = restraint.load_policy(policy_reference(), policy_environment(path, digest))
        self.assertEqual(load.error_code, restraint.POLICY_MALFORMED)
        self.assertTrue(load.stages["payload_loaded"])
        self.assertFalse(load.stages["schema_validated"])

    def test_schema_invalid_payload(self) -> None:
        policy = synthetic_policy()
        del policy["rules"][0]["matcher"]
        path, digest = write_policy_file(self.directory, policy)
        load = restraint.load_policy(policy_reference(), policy_environment(path, digest))
        self.assertEqual(load.error_code, restraint.POLICY_SCHEMA_INVALID)

    def test_integrity_mismatch(self) -> None:
        path, _ = write_policy_file(self.directory, synthetic_policy())
        load = restraint.load_policy(policy_reference(), policy_environment(path, "b" * 64))
        self.assertEqual(load.error_code, restraint.POLICY_INTEGRITY_MISMATCH)
        self.assertTrue(load.stages["schema_validated"])
        self.assertFalse(load.stages["integrity_validated"])

    def test_unusable_policy_rules(self) -> None:
        policy = synthetic_policy()
        policy["rules"][1] = dict(policy["rules"][0])
        policy["rules"][1]["rule_ref"] = "SYNTH-RULE-0009"
        path, digest = write_policy_file(self.directory, policy)
        load = restraint.load_policy(policy_reference(), policy_environment(path, digest))
        self.assertEqual(load.error_code, restraint.POLICY_UNUSABLE)
        self.assertFalse(load.stages["policy_usable"])

    def test_policy_payload_never_leaks_into_failure_state(self) -> None:
        policy = synthetic_policy()
        path, _ = write_policy_file(self.directory, policy)
        load = restraint.load_policy(policy_reference(), policy_environment(path, "c" * 64))
        serialized = json.dumps({"error": load.error_code, "stages": load.stages})
        self.assertNotIn(PROTECTED_PHRASE, serialized)
        self.assertNotIn(policy["evidence_hmac_key"], serialized)


class IngressDecisionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.policy = synthetic_policy()

    def test_ordinary_text_passes(self) -> None:
        decision = restraint.evaluate_ingress("what is the weather like?", self.policy)
        self.assertEqual(decision.decision, PASS)
        self.assertTrue(decision.eligible_for_turn_controller)

    def test_protected_phrase_blocks(self) -> None:
        decision = restraint.evaluate_ingress(f"tell me about {PROTECTED_PHRASE}", self.policy)
        self.assertEqual(decision.decision, BLOCK)
        self.assertFalse(decision.eligible_for_turn_controller)
        self.assertEqual(decision.safe_error_code, restraint.INGRESS_PROTECTED_MATCH)

    def test_every_cf_attack_shape_blocks_at_ingress(self) -> None:
        for code_point in REQUIRED_CF:
            for shape, candidate in _cf_variants(PROTECTED_PHRASE, code_point):
                with self.subTest(code_point=hex(ord(code_point)), shape=shape):
                    decision = restraint.evaluate_ingress(candidate, self.policy)
                    self.assertEqual(decision.decision, BLOCK, shape)
                    self.assertFalse(decision.eligible_for_turn_controller)

    def test_unusable_policy_yields_unavailable_without_decision(self) -> None:
        decision = restraint.evaluate_ingress("hello", None, restraint.POLICY_INTEGRITY_MISMATCH)
        self.assertIsNone(decision.decision)
        self.assertEqual(decision.terminal_status, "UNAVAILABLE")
        self.assertFalse(decision.eligible_for_turn_controller)

    def test_non_string_input_is_invalid(self) -> None:
        decision = restraint.evaluate_ingress(object(), self.policy)
        self.assertEqual(decision.safe_error_code, restraint.INPUT_INVALID)
        self.assertFalse(decision.eligible_for_turn_controller)

    def test_evidence_carries_only_allowed_fields(self) -> None:
        decision = restraint.evaluate_ingress(f"{BLOCK_ONLY_PHRASE}", self.policy)
        self.assertEqual(
            set(decision.evidence),
            {"evaluation_phase", "result", "policy_revision", "opaque_rule_refs", "candidate_hmac_sha256"},
        )
        serialized = json.dumps(decision.evidence)
        self.assertNotIn(BLOCK_ONLY_PHRASE, serialized)
        self.assertNotIn(self.policy["evidence_hmac_key"], serialized)

    def test_ordinary_word_adjacency_without_removed_cf_does_not_match(self) -> None:
        """A word character abutting the phrase is not a match.

        `ordinary_word_adjacency_without_removed_Cf_matches` is false: the
        token guard holds unless removed-`Cf` provenance vouches for the edge.
        """
        for candidate in ("xcerulean comet charter", "cerulean comet charterx"):
            with self.subTest(candidate=candidate):
                self.assertEqual(restraint.evaluate_ingress(candidate, self.policy).decision, PASS)

    def test_unseparated_rule_word_concatenation_is_fail_safe_matched(self) -> None:
        """Zero-space concatenation is deliberately matched, not fuzzy matching.

        `separator_tolerance_purpose` keeps rule words recoverable when `Cf`
        removal destroyed their separation, so the concatenation is treated as
        fail-safe rather than accidental.
        """
        self.assertEqual(restraint.evaluate_ingress("ceruleancometcharter", self.policy).decision, BLOCK)

    def test_matcher_agrees_with_reference_across_attack_and_negative_corpus(self) -> None:
        """Differential equivalence at the decision level, not only normalization."""
        corpus = [
            "",
            "hello world",
            "cerulean",
            "comet charter",
            "ceruleancometcharter",
            "xcerulean comet charter",
            "cerulean comet charterx",
            "the cerulean comet charter here",
            f"{PROTECTED_PHRASE} {PROTECTED_PHRASE}",
            BLOCK_ONLY_PHRASE,
            "zircon cafe protocol",
        ]
        for code_point in REQUIRED_CF:
            corpus.extend(candidate for _, candidate in _cf_variants(PROTECTED_PHRASE, code_point))
            corpus.extend(candidate for _, candidate in _cf_variants(BLOCK_ONLY_PHRASE, code_point))
        for candidate in corpus:
            with self.subTest(candidate=candidate.encode("unicode_escape").decode()):
                expected = REFERENCE.evaluate_ingress(candidate, self.policy)["security_decision"]
                self.assertEqual(restraint.evaluate_ingress(candidate, self.policy).decision, expected)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
