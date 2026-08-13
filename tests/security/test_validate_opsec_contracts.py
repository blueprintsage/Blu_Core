from __future__ import annotations

import copy
import hashlib
import hmac
import importlib.util
import inspect
import json
import tempfile
import unittest
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "validate_opsec_contracts", ROOT / "tools/validate_opsec_contracts.py"
)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class OpsecContractValidationTests(unittest.TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls) -> None:
        fixture = json.loads((ROOT / validator.SYNTHETIC_POLICY).read_text(encoding="utf-8"))
        cls.policy = fixture["policy"]
        cls.policy_schema = json.loads((ROOT / validator.POLICY_SCHEMA).read_text(encoding="utf-8"))
        cls.cases = json.loads((ROOT / validator.SYNTHETIC_CASES).read_text(encoding="utf-8"))

    def test_canonical_contracts_pass(self) -> None:
        self.assertEqual([], validator.validate(ROOT))

    def test_normalization_is_deterministic_and_bounded(self) -> None:
        self.assertEqual("Cerulean Comet Charter", validator.normalize_rule_text("  Cerulean---Comet\r\nCharter  "))
        self.assertEqual("zircon café protocol", validator.normalize_rule_text("zircon café protocol"))

    def test_single_cf_removed_candidate_matches_all_placement_classes(self) -> None:
        candidates = [
            validator.normalized_match_candidate("cerulean\u200bcomet charter"),
            validator.normalized_match_candidate("cerulean co\u200bmet charter"),
            validator.normalized_match_candidate("cerulean\u200bco\ufeffmet charter"),
        ]
        self.assertEqual([validator.CF_MATCH_VIEW_NAME] * 3, [item["name"] for item in candidates])
        self.assertEqual(
            ["ceruleancomet charter", "cerulean comet charter", "ceruleancomet charter"],
            [item["normalized"] for item in candidates],
        )
        for candidate in candidates:
            self.assertTrue(validator._matches(candidate, self.policy, "ingress"))

    def test_outer_edge_cf_provenance_survives_normalization(self) -> None:
        candidate = validator.normalized_match_candidate(
            "foo\u200b\u00adcerulean comet charter\u2060bar"
        )
        self.assertEqual("foocerulean comet charterbar", candidate["normalized"])
        self.assertEqual([3, 25], candidate["removed_cf_boundaries"])
        matches = validator._matches(candidate, self.policy, "ingress")
        self.assertEqual([(3, 25)], [(item["start"], item["end"]) for item in matches])

    def test_cf_fixture_matrix_is_complete_and_category_correct(self) -> None:
        expected = {
            (code_point, position)
            for code_point in validator.REQUIRED_CF_CODE_POINTS
            for position in validator.REQUIRED_CF_POSITIONS
        }
        for phase in ("ingress", "egress"):
            cases = [item for item in self.cases[phase] if item.get("cf_code_point")]
            self.assertEqual(expected, {(item["cf_code_point"], item["cf_position"]) for item in cases})
            for item in cases:
                code_point = int(item["cf_code_point"][2:], 16)
                self.assertEqual("Cf", unicodedata.category(chr(code_point)))
            cross = [
                item for item in self.cases[phase]
                if item.get("cf_position") == "mixed" and len(item.get("cf_code_points", [])) > 1
            ]
            self.assertTrue(cross)
            for item in cross:
                self.assertEqual("mixed", item["cf_position"])
                for code_point in item["cf_code_points"]:
                    self.assertEqual("Cf", unicodedata.category(chr(int(code_point[2:], 16))))
            attack_classes = {
                item.get("attack_class")
                for item in self.cases[phase]
                if item.get("attack_class")
            }
            self.assertEqual(validator.REQUIRED_CF_ATTACK_CLASSES, attack_classes)

    def test_ingress_matrix(self) -> None:
        for case in self.cases["ingress"]:
            with self.subTest(case=case["id"]):
                result = validator.evaluate_ingress(case["text"], self.policy)
                self.assertEqual(case["expected"], result["security_decision"])
                self.assertEqual(case["expected"] == "PASS", result["eligible_for_turn_controller"])

    def test_only_pass_reaches_turn_controller(self) -> None:
        blocked = validator.evaluate_ingress("cerulean comet charter", self.policy)
        self.assertEqual("BLOCK", blocked["security_decision"])
        self.assertFalse(blocked["eligible_for_turn_controller"])
        self.assertIsNone(blocked["public_output"])

    def test_all_cf_ingress_probes_block_before_turn_controller(self) -> None:
        for case in (item for item in self.cases["ingress"] if item.get("cf_code_point") or item.get("cf_code_points")):
            with self.subTest(case=case["id"]):
                result = validator.evaluate_ingress(case["text"], self.policy)
                self.assertEqual("BLOCK", result["security_decision"])
                self.assertFalse(result["eligible_for_turn_controller"])

    def test_egress_matrix(self) -> None:
        for case in self.cases["egress"]:
            with self.subTest(case=case["id"]):
                result = validator.evaluate_egress(case["text"], self.policy)
                self.assertEqual(case["expected"], result["egress_result"])
                self.assertEqual(case["printable"], result["eligible_for_print"])

    def test_all_cf_egress_probes_are_safely_redacted(self) -> None:
        for case in (item for item in self.cases["egress"] if item.get("cf_code_point") or item.get("cf_code_points")):
            with self.subTest(case=case["id"]):
                result = validator.evaluate_egress(case["text"], self.policy)
                self.assertEqual("REDACTED", result["egress_result"])
                self.assertTrue(result["eligible_for_print"])
                self.assertIn(validator.REDACTION_REPLACEMENT, result["public_output"])
                rescanned = validator._matches(
                    validator.normalized_match_candidate(result["public_output"])["normalized"],
                    self.policy,
                    "egress",
                )
                self.assertFalse(rescanned)

    def test_boundary_and_inside_cf_matches_share_one_safe_redaction_view(self) -> None:
        result = validator.evaluate_egress(
            "Before cerulean\u200bcomet charter and cerulean co\u200bmet charter after.",
            self.policy,
        )
        self.assertEqual("REDACTED", result["egress_result"])
        self.assertTrue(result["eligible_for_print"])
        self.assertEqual(2, result["public_output"].count(validator.REDACTION_REPLACEMENT))

    def test_repeated_arbitrary_cf_insertions_do_not_reopen_bypass(self) -> None:
        phrase = "cerulean comet charter"
        code_points = [chr(int(item[2:], 16)) for item in validator.REQUIRED_CF_CODE_POINTS]
        for repeat in (1, 2, 4):
            for cf in code_points:
                inserted = "".join(cf * repeat if char == " " else char + cf * repeat for char in phrase)
                with self.subTest(repeat=repeat, code_point=f"U+{ord(cf):04X}"):
                    ingress = validator.evaluate_ingress(inserted, self.policy)
                    self.assertEqual("BLOCK", ingress["security_decision"])
                    self.assertFalse(ingress["eligible_for_turn_controller"])
                    egress = validator.evaluate_egress(f"Before {inserted} after.", self.policy)
                    self.assertIn(egress["egress_result"], {"REDACTED", "BLOCKED"})
                    if egress["eligible_for_print"]:
                        self.assertIn(validator.REDACTION_REPLACEMENT, egress["public_output"])

        cross_inserted = "".join(
            code_points[index % len(code_points)] * 3 if char == " "
            else char + code_points[index % len(code_points)] * 2
            for index, char in enumerate(phrase)
        )
        self.assertEqual("BLOCK", validator.evaluate_ingress(cross_inserted, self.policy)["security_decision"])
        cross_egress = validator.evaluate_egress(f"Before {cross_inserted} after.", self.policy)
        self.assertIn(cross_egress["egress_result"], {"REDACTED", "BLOCKED"})
        self.assertNotEqual("CLEAR", cross_egress["egress_result"])

    def test_mixed_cf_block_action_withholds_entire_output(self) -> None:
        result = validator.evaluate_egress("prefix zircon\u200bcaf\ufeffé protocol suffix", self.policy)
        self.assertEqual("BLOCKED", result["egress_result"])
        self.assertFalse(result["eligible_for_print"])
        self.assertIsNone(result["public_output"])

    def test_overlapping_redaction_spans_fail_closed(self) -> None:
        policy = copy.deepcopy(self.policy)
        overlapping = copy.deepcopy(policy["rules"][0])
        overlapping["rule_ref"] = "SYNTH-RULE-0099"
        overlapping["value"] = "comet charter"
        policy["rules"].append(overlapping)
        result = validator.evaluate_egress("Before cerulean comet charter after.", policy)
        self.assertEqual("BLOCKED", result["egress_result"])
        self.assertEqual("EGRESS_REDACTION_INVALID", result["safe_error_code"])
        self.assertFalse(result["eligible_for_print"])

    def test_existing_negative_ingress_fixtures_remain_pass(self) -> None:
        expected_negative_ids = {
            "ordinary",
            "near_match",
            "shared_words",
            "partial_fragment",
            "punctuation_adjacent_nonmatch",
        }
        actual = {item["id"] for item in self.cases["ingress"] if item["expected"] == "PASS"}
        self.assertEqual(expected_negative_ids, actual)
        for case in (item for item in self.cases["ingress"] if item["id"] in expected_negative_ids):
            self.assertEqual("PASS", validator.evaluate_ingress(case["text"], self.policy)["security_decision"])

    def test_ordinary_outer_word_adjacency_without_cf_remains_nonmatch(self) -> None:
        for text in (
            "foocerulean comet charter",
            "cerulean comet charterfoo",
            "foobarcerulean comet charterbaz",
            "caf\u00e9cerulean comet charter",
            "cerulean comet charter\u6f22\u5b57",
            "\u03b1cerulean comet charter\u03b2",
        ):
            with self.subTest(text=text):
                result = validator.evaluate_ingress(text, self.policy)
                self.assertEqual("PASS", result["security_decision"])
                self.assertTrue(result["eligible_for_turn_controller"])
                egress = validator.evaluate_egress(text, self.policy)
                self.assertEqual("CLEAR", egress["egress_result"])
                self.assertTrue(egress["eligible_for_print"])

    def test_unseparated_self_repetition_fails_safely_without_weakening_guards(self) -> None:
        repeated = "cerulean\u200bcomet chartercerulean co\u200dmet charter"
        ingress = validator.evaluate_ingress(repeated, self.policy)
        self.assertEqual("BLOCK", ingress["security_decision"])
        self.assertFalse(ingress["eligible_for_turn_controller"])
        egress = validator.evaluate_egress(f"Before {repeated} after.", self.policy)
        self.assertEqual("REDACTED", egress["egress_result"])
        self.assertEqual(2, egress["public_output"].count(validator.REDACTION_REPLACEMENT))

    def test_repetition_is_fully_redacted(self) -> None:
        result = validator.evaluate_egress(
            "cerulean comet charter safe words cerulean comet charter", self.policy
        )
        self.assertEqual("REDACTED", result["egress_result"])
        self.assertEqual(2, result["public_output"].count(validator.REDACTION_REPLACEMENT))
        self.assertNotIn("cerulean comet charter", result["public_output"].casefold())

    def test_redaction_only_output_is_blocked(self) -> None:
        result = validator.evaluate_egress("cerulean comet charter", self.policy)
        self.assertEqual("BLOCKED", result["egress_result"])
        self.assertFalse(result["eligible_for_print"])
        self.assertIsNone(result["public_output"])

    def test_policy_block_action_withholds_entire_output(self) -> None:
        result = validator.evaluate_egress("prefix zircon café protocol suffix", self.policy)
        self.assertEqual("BLOCKED", result["egress_result"])
        self.assertIsNone(result["public_output"])

    def test_receipts_and_logs_do_not_contain_protected_text_or_key(self) -> None:
        for evaluate, text in (
            (validator.evaluate_ingress, "cerulean comet charter"),
            (validator.evaluate_egress, "before cerulean comet charter after"),
            (validator.evaluate_egress, "zircon café protocol"),
        ):
            result = evaluate(text, self.policy)
            serialized = json.dumps(result, ensure_ascii=False).casefold()
            for rule in self.policy["rules"]:
                self.assertNotIn(rule["value"].casefold(), serialized)
            self.assertNotIn(self.policy["evidence_hmac_key"].casefold(), serialized)

    def test_cf_results_receipts_and_logs_do_not_leak(self) -> None:
        for phase, evaluate in (
            ("ingress", validator.evaluate_ingress),
            ("egress", validator.evaluate_egress),
        ):
            for case in (item for item in self.cases[phase] if item.get("cf_code_point") or item.get("cf_code_points")):
                with self.subTest(phase=phase, case=case["id"]):
                    serialized = json.dumps(evaluate(case["text"], self.policy), ensure_ascii=False).casefold()
                    for rule in self.policy["rules"]:
                        self.assertNotIn(rule["value"].casefold(), serialized)
                    self.assertNotIn(self.policy["evidence_hmac_key"].casefold(), serialized)

    def test_evidence_digest_is_keyed_and_stable(self) -> None:
        first = validator.evaluate_ingress("ordinary words", self.policy)
        second = validator.evaluate_ingress("ordinary words", self.policy)
        changed = copy.deepcopy(self.policy)
        changed["evidence_hmac_key"] = "different-synthetic-key-00000000000000000000001"
        third = validator.evaluate_ingress("ordinary words", changed)
        self.assertEqual(first["evidence"]["candidate_hmac_sha256"], second["evidence"]["candidate_hmac_sha256"])
        self.assertNotEqual(first["evidence"]["candidate_hmac_sha256"], third["evidence"]["candidate_hmac_sha256"])

    def test_cf_evidence_digest_uses_the_single_decision_candidate(self) -> None:
        text = "cerulean\u200bco\ufeffmet charter"
        result = validator.evaluate_ingress(text, self.policy)
        normalized = validator.normalized_match_candidate(text)["normalized"]
        digest = hmac.new(
            self.policy["evidence_hmac_key"].encode("utf-8"),
            normalized.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        self.assertEqual(digest, result["evidence"]["candidate_hmac_sha256"])

    def test_missing_policy_is_unavailable_and_not_model_eligible(self) -> None:
        result = validator.evaluate_ingress("ordinary words", None, "POLICY_REF_MISSING")
        self.assertIsNone(result["security_decision"])
        self.assertEqual("UNAVAILABLE", result["terminal_status"])
        self.assertFalse(result["eligible_for_turn_controller"])

    def test_invalid_policy_is_unavailable_and_not_printable(self) -> None:
        result = validator.evaluate_egress("ordinary words", None, "POLICY_SCHEMA_INVALID")
        self.assertEqual("UNAVAILABLE", result["egress_result"])
        self.assertFalse(result["eligible_for_print"])

    def _write_policy(self, directory: Path, policy: dict) -> tuple[Path, bytes]:
        path = directory / "policy.json"
        payload = json.dumps(policy, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        path.write_bytes(payload)
        return path, payload

    def test_policy_loader_valid_reference_reaches_every_stage(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path, payload = self._write_policy(Path(directory), self.policy)
            ref = {"kind": "environment_file", "locator_env": "POLICY_PATH", "sha256_env": "POLICY_SHA"}
            env = {"POLICY_PATH": str(path), "POLICY_SHA": hashlib.sha256(payload).hexdigest()}
            result = validator.load_policy(ref, env, self.policy_schema)
            self.assertTrue(result["usable"])
            self.assertTrue(all(result["stages"].values()))

    def test_policy_loader_missing_reference_fails_closed(self) -> None:
        result = validator.load_policy(None, {}, self.policy_schema)
        self.assertEqual("POLICY_REF_MISSING", result["error_code"])
        self.assertFalse(result["usable"])

    def test_policy_loader_unavailable_target_fails_closed(self) -> None:
        ref = {"kind": "environment_file", "locator_env": "POLICY_PATH", "sha256_env": "POLICY_SHA"}
        result = validator.load_policy(ref, {"POLICY_PATH": "absent", "POLICY_SHA": "0" * 64}, self.policy_schema)
        self.assertEqual("POLICY_TARGET_UNAVAILABLE", result["error_code"])

    def test_policy_loader_malformed_payload_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "policy.json"
            payload = b"{"
            path.write_bytes(payload)
            ref = {"kind": "environment_file", "locator_env": "POLICY_PATH", "sha256_env": "POLICY_SHA"}
            result = validator.load_policy(ref, {"POLICY_PATH": str(path), "POLICY_SHA": hashlib.sha256(payload).hexdigest()}, self.policy_schema)
            self.assertEqual("POLICY_MALFORMED", result["error_code"])

    def test_policy_loader_schema_invalid_payload_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path, payload = self._write_policy(Path(directory), {"schema_version": "1.0.0"})
            ref = {"kind": "environment_file", "locator_env": "POLICY_PATH", "sha256_env": "POLICY_SHA"}
            result = validator.load_policy(ref, {"POLICY_PATH": str(path), "POLICY_SHA": hashlib.sha256(payload).hexdigest()}, self.policy_schema)
            self.assertEqual("POLICY_SCHEMA_INVALID", result["error_code"])

    def test_policy_loader_integrity_mismatch_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path, _ = self._write_policy(Path(directory), self.policy)
            ref = {"kind": "environment_file", "locator_env": "POLICY_PATH", "sha256_env": "POLICY_SHA"}
            result = validator.load_policy(ref, {"POLICY_PATH": str(path), "POLICY_SHA": "0" * 64}, self.policy_schema)
            self.assertEqual("POLICY_INTEGRITY_MISMATCH", result["error_code"])

    def test_duplicate_normalized_rules_make_policy_unusable(self) -> None:
        policy = copy.deepcopy(self.policy)
        duplicate = copy.deepcopy(policy["rules"][0])
        duplicate["rule_ref"] = "SYNTH-RULE-DUPLICATE"
        duplicate["value"] = "CERULEAN---COMET---CHARTER"
        policy["rules"].append(duplicate)
        self.assertTrue(any("duplicate normalized" in item for item in validator.validate_policy_usability(policy)))

    def test_matcher_has_no_model_or_auth_dependency(self) -> None:
        parameters = set(inspect.signature(validator.evaluate_ingress).parameters)
        self.assertEqual({"text", "policy", "policy_error"}, parameters)
        source = inspect.getsource(validator.evaluate_ingress).casefold()
        self.assertNotIn("model", source)
        self.assertNotIn("auth", source)

    def test_security_decision_vocabulary_remains_exact(self) -> None:
        contract = json.loads((ROOT / validator.CONTRACT_ROOT / "minimum_contract.json").read_text(encoding="utf-8"))
        self.assertEqual(["PASS", "BLOCK", "ASK"], contract["security_decision_values"])

    def test_contract_states_semantic_limit_and_scope_exclusions(self) -> None:
        contract = json.loads((ROOT / validator.CONTRACT_ROOT / "minimum_contract.json").read_text(encoding="utf-8"))
        self.assertFalse(contract["normalization"]["semantic_paraphrase_detection"])
        exclusions = " ".join(contract["scope_exclusions"])
        for term in ("Auth", "SUR-011", "model inference", "tool execution", "continuity mutation", "production runtime"):
            self.assertIn(term, exclusions)
        self.assertIn("confusable", exclusions.casefold())
        self.assertIn("homoglyph", exclusions.casefold())


if __name__ == "__main__":
    unittest.main()


class BC050AuthorizationGateTests(unittest.TestCase):
    """BC-050-C1: administrative gate only; OPSEC mechanism is untouched."""

    def setUp(self) -> None:
        self.checklist = json.loads(
            (ROOT / "readiness/python_phase1_readiness_checklist.json").read_text(encoding="utf-8")
        )

    def test_authorized_checklist_is_recognized(self) -> None:
        self.assertTrue(validator._bc050_authorized(self.checklist))

    def test_missing_record_is_unauthorized(self) -> None:
        del self.checklist["bc050_implementation_authorization"]
        self.assertFalse(validator._bc050_authorized(self.checklist))

    def test_wrong_assignment_is_unauthorized(self) -> None:
        self.checklist["bc050_implementation_authorization"]["assignment"] = "BC-999"
        self.assertFalse(validator._bc050_authorized(self.checklist))

    def test_unstated_state_is_unauthorized(self) -> None:
        self.checklist["bc050_implementation_authorization"]["state"] = "proposed"
        self.assertFalse(validator._bc050_authorized(self.checklist))

    def test_record_without_authorizing_party_is_unauthorized(self) -> None:
        self.checklist["bc050_implementation_authorization"]["authorized_by"] = ""
        self.assertFalse(validator._bc050_authorized(self.checklist))

    def test_record_without_packet_is_unauthorized(self) -> None:
        self.checklist["bc050_implementation_authorization"]["packet"] = ""
        self.assertFalse(validator._bc050_authorized(self.checklist))

    def test_non_mapping_record_is_unauthorized(self) -> None:
        self.checklist["bc050_implementation_authorization"] = "authorized"
        self.assertFalse(validator._bc050_authorized(self.checklist))


class OpsecMechanismUnchangedTests(unittest.TestCase):
    """The C1 oracle must be semantically identical after BC-050-C1."""

    CF = ("​", "­", "‍", "‌", "﻿", "⁠")
    PHRASE = "cerulean comet charter"

    @classmethod
    def setUpClass(cls) -> None:
        fixture = json.loads((ROOT / validator.SYNTHETIC_POLICY).read_text(encoding="utf-8"))
        cls.policy = fixture["policy"]

    def test_outer_edge_and_interior_cf_still_block(self) -> None:
        for code_point in self.CF:
            for candidate in (
                code_point + self.PHRASE,
                self.PHRASE + code_point,
                code_point + self.PHRASE + code_point,
                code_point.join(self.PHRASE.split(" ")),
                (code_point * 3).join(self.PHRASE.split(" ")),
            ):
                with self.subTest(code_point=hex(ord(code_point))):
                    result = validator.evaluate_ingress(candidate, self.policy)
                    self.assertEqual("BLOCK", result["security_decision"])

    def test_provenance_offsets_are_unchanged(self) -> None:
        self.assertEqual(
            {"normalized": "abc", "removed_cf_boundaries": [1, 2]},
            {
                key: value
                for key, value in validator.normalized_match_candidate("a​b‌c").items()
                if key in {"normalized", "removed_cf_boundaries"}
            },
        )

    def test_word_adjacency_without_removed_cf_still_does_not_match(self) -> None:
        self.assertEqual(
            "PASS", validator.evaluate_ingress("xcerulean comet charter", self.policy)["security_decision"]
        )

    def test_unseparated_concatenation_still_fail_safe_matches(self) -> None:
        self.assertEqual(
            "BLOCK", validator.evaluate_ingress("ceruleancometcharter", self.policy)["security_decision"]
        )

    def test_redaction_and_rescan_are_unchanged(self) -> None:
        result = validator.evaluate_egress(f"see {self.PHRASE} today", self.policy)
        self.assertEqual("REDACTED", result["egress_result"])
        self.assertNotIn("cerulean", result["public_output"])

    def test_fail_closed_without_policy(self) -> None:
        result = validator.evaluate_ingress("hello", None, "POLICY_INTEGRITY_MISMATCH")
        self.assertIsNone(result["security_decision"])
        self.assertFalse(result["eligible_for_turn_controller"])
