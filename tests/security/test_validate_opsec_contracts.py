from __future__ import annotations

import copy
import hashlib
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
        self.assertEqual("Cerulean Comet Charter", validator.normalize_text("  Cerulean---Comet\r\nCharter  "))
        self.assertEqual("zircon café protocol", validator.normalize_text("zircon café protocol"))

    def test_cf_candidate_views_are_distinct_and_both_match(self) -> None:
        boundary = validator.normalized_candidate_views("cerulean\u200bcomet charter")
        inside = validator.normalized_candidate_views("cerulean co\u200bmet charter")
        self.assertEqual(validator.CF_VIEW_NAMES, [item["name"] for item in boundary])
        self.assertEqual("cerulean comet charter", boundary[0]["normalized"])
        self.assertEqual("ceruleancomet charter", boundary[1]["normalized"])
        self.assertEqual("cerulean co met charter", inside[0]["normalized"])
        self.assertEqual("cerulean comet charter", inside[1]["normalized"])
        for views in (boundary, inside):
            evaluated = validator._matches_by_candidate_view(views, self.policy, "ingress")
            self.assertTrue(any(item["matches"] for item in evaluated))

    def test_cf_fixture_matrix_is_complete_and_category_correct(self) -> None:
        expected = {
            (code_point, position)
            for code_point in validator.REQUIRED_CF_CODE_POINTS
            for position in ("boundary", "inside_token")
        }
        for phase in ("ingress", "egress"):
            cases = [item for item in self.cases[phase] if item.get("cf_code_point")]
            self.assertEqual(expected, {(item["cf_code_point"], item["cf_position"]) for item in cases})
            for item in cases:
                code_point = int(item["cf_code_point"][2:], 16)
                self.assertEqual("Cf", unicodedata.category(chr(code_point)))

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
        for case in (item for item in self.cases["ingress"] if item.get("cf_code_point")):
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
        for case in (item for item in self.cases["egress"] if item.get("cf_code_point")):
            with self.subTest(case=case["id"]):
                result = validator.evaluate_egress(case["text"], self.policy)
                self.assertEqual("REDACTED", result["egress_result"])
                self.assertTrue(result["eligible_for_print"])
                self.assertIn(validator.REDACTION_REPLACEMENT, result["public_output"])
                rescanned = validator._matches_by_candidate_view(
                    validator.normalized_candidate_views(result["public_output"]), self.policy, "egress"
                )
                self.assertFalse(any(item["matches"] for item in rescanned))

    def test_egress_matches_split_across_cf_views_fail_closed(self) -> None:
        result = validator.evaluate_egress(
            "Before cerulean\u200bcomet charter and cerulean co\u200bmet charter after.",
            self.policy,
        )
        self.assertEqual("BLOCKED", result["egress_result"])
        self.assertFalse(result["eligible_for_print"])
        self.assertIsNone(result["public_output"])

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
            for case in (item for item in self.cases[phase] if item.get("cf_code_point")):
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
