import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "tools"))

from validate_successor_kernel_spec import (  # noqa: E402
    _validate_manifest_coverage,
    validate,
)


class SuccessorKernelSpecValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        for source in (
            "AGENTS.md",
            "MANIFEST.sha256",
            "contracts/runtime",
            "contracts/successor",
            "docs/architecture",
            "docs/domains/runtime/assignments/BC-018",
            "docs/domains/runtime/assignments/BC-018-C1",
            "docs/domains/runtime/decisions.md",
            "docs/domains/runtime/viability",
            "docs/sources/historical_archives/behavioral_archaeology",
            "docs/worklogs/assignments.md",
            "kernel/golden/v0.22.0",
        ):
            src = REPO_ROOT / source
            dst = self.root / source
            dst.parent.mkdir(parents=True, exist_ok=True)
            if src.is_dir():
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
        self.components = self.root / "contracts/successor/component_registry.json"
        self.behaviors = self.root / "contracts/successor/behavior_placement.json"
        self.interfaces = self.root / "contracts/successor/interface_registry.json"
        self.packets = self.root / "contracts/successor/packet_registry.json"
        self.trace = self.root / "contracts/successor/traceability.json"

    def tearDown(self):
        self.temp.cleanup()

    @staticmethod
    def load(path):
        return json.loads(path.read_text(encoding="utf-8"))

    @staticmethod
    def save(path, data):
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    def assert_error(self, expected):
        errors = validate(self.root)
        self.assertTrue(any(expected in error for error in errors), errors)

    def test_canonical_records_pass(self):
        self.assertEqual([], validate(REPO_ROOT))

    def test_missing_required_file_fails(self):
        (self.root / "contracts/successor/error_model.json").unlink()
        self.assert_error("missing required file")

    def test_manifest_coverage_rejects_missing_tracked_file(self):
        case_root = self.root / "manifest_case"
        case_root.mkdir()
        (case_root / "MANIFEST.sha256").write_text(
            "0" * 64 + "  AGENTS.md\n", encoding="utf-8"
        )
        errors = _validate_manifest_coverage(
            case_root,
            {".gitattributes", "AGENTS.md", "MANIFEST.sha256"},
        )
        self.assertTrue(
            any("tracked file missing from MANIFEST.sha256: .gitattributes" in error for error in errors),
            errors,
        )

    def test_malformed_json_fails(self):
        self.components.write_text("{not json", encoding="utf-8")
        self.assert_error("invalid JSON")

    def test_duplicate_component_id_fails(self):
        data = self.load(self.components)
        data["components"][1]["component_id"] = data["components"][0]["component_id"]
        self.save(self.components, data)
        self.assert_error("duplicate component ID")

    def test_unknown_component_evidence_fails(self):
        data = self.load(self.components)
        data["components"][0]["evidence_refs"].append("EVID-NOT-REAL")
        self.save(self.components, data)
        self.assert_error("component evidence ref is unknown")

    def test_unresolved_evidence_locator_fails(self):
        data = self.load(self.trace)
        data["evidence_catalog"][0]["source_locator"] = "not present anywhere"
        self.save(self.trace, data)
        self.assert_error("evidence locator does not resolve")

    def test_component_must_own_and_disown(self):
        data = self.load(self.components)
        data["components"][0]["owns"] = []
        data["components"][1]["does_not_own"] = []
        self.save(self.components, data)
        self.assert_error("component lacks owns")
        self.assert_error("component lacks does_not_own")

    def test_duplicate_exclusive_owner_fails(self):
        data = self.load(self.components)
        data["components"][1]["owns"].append(data["components"][0]["owns"][0])
        self.save(self.components, data)
        self.assert_error("duplicate exclusive deterministic owner")

    def test_state_lifetime_required(self):
        data = self.load(self.components)
        data["components"][2]["state_lifetime"] = []
        self.save(self.components, data)
        self.assert_error("lacks valid lifetime")

    def test_host_dependencies_must_be_explicit(self):
        data = self.load(self.components)
        data["components"][2].pop("host_dependencies")
        self.save(self.components, data)
        self.assert_error("host capability dependencies are not explicit")

    def test_durable_claim_requires_continuity_provider(self):
        data = self.load(self.behaviors)
        item = next(x for x in data["behaviors"] if x["behavior"] == "durable persistence")
        item["continuity_dependency"] = "none"
        self.save(self.behaviors, data)
        self.assert_error("durable-persistence claim lacks continuity-provider dependency")

    def test_future_schedule_requires_provider(self):
        data = self.load(self.behaviors)
        item = next(x for x in data["behaviors"] if x["behavior"] == "future scheduling")
        item["host_dependency"] = "prompt text"
        self.save(self.behaviors, data)
        self.assert_error("future scheduling claim lacks scheduling-provider dependency")

    def test_opsec_must_be_pre_ingress(self):
        data = self.load(self.components)
        data["components"][0]["boundary_position"] = "after_turn_controller"
        self.save(self.components, data)
        self.assert_error("OPSEC is moved behind turn_controller")

    def test_turn_request_producer_must_be_turn_controller(self):
        data = self.load(self.packets)
        next(x for x in data["packets"] if x["packet_id"] == "TurnRequest")["producer"] = "host_adapter_boundary"
        self.save(self.packets, data)
        self.assert_error("TurnRequest producer is not solely turn_controller")

    def test_ordinary_routing_requires_security_pass(self):
        data = self.load(self.packets)
        data["ingress_ownership"]["ordinary_routing_precondition"] = "raw_host_input present"
        self.save(self.packets, data)
        self.assert_error("ordinary host routing may begin before SecurityDecision PASS")

    def test_opsec_authorization_requires_auth_reentry(self):
        data = self.load(self.packets)
        data["pre_ingress_authorization_loop"]["reentry_target"] = None
        data["pre_ingress_authorization_loop"]["ordinary_routing_bypassed"] = False
        self.save(self.packets, data)
        self.assert_error("lacks Auth/re-entry mechanism")

    def test_auth_cannot_merge_into_opsec(self):
        data = self.load(self.packets)
        data["pre_ingress_authorization_loop"]["authorization_owner"] = "security_restraint"
        self.save(self.packets, data)
        self.assert_error("Auth is merged into OPSEC")

    def test_bare_session_lifetime_cannot_claim_cross_turn_kernel_persistence(self):
        data = self.load(self.components)
        auth = next(x for x in data["components"] if x["component_id"] == "authorization_evaluator")
        auth["state_lifetime"] = ["turn", "session"]
        self.save(self.components, data)
        self.assert_error("bare session lifetime claims unexplained cross-turn kernel persistence")

    def test_pending_authorization_requires_evidenced_substrate(self):
        data = self.load(self.packets)
        pending = next(x for x in data["state_records"] if x["state_record_id"] == "PendingAuthorizationState")
        pending["substrate_provider"] = None
        pending["allowed_storage_lifetimes"] = []
        self.save(self.packets, data)
        self.assert_error("lacks evidenced host_session or continuity-backed substrate")

    def test_cross_turn_authorization_allows_one_terminal_per_host_turn(self):
        data = self.load(self.packets)
        data["pre_ingress_authorization_loop"]["maximum_terminal_packets_per_host_turn"] = 2
        self.save(self.packets, data)
        self.assert_error("two TerminalPackets for one host turn")

    def test_pre_ingress_unavailable_cannot_require_control_decision(self):
        data = self.load(self.packets)
        data["pre_ingress_terminal_authority_contract"]["control_decision_required"] = True
        self.save(self.packets, data)
        self.assert_error("pre-ingress UNAVAILABLE improperly requires ControlDecision")

    def test_pre_ingress_unavailable_requires_security_decision_authority(self):
        data = self.load(self.packets)
        data["pre_ingress_terminal_authority_contract"]["authority_ref_type"] = None
        self.save(self.packets, data)
        self.assert_error("pre-ingress UNAVAILABLE lacks SecurityDecision authority")

    def test_unbound_pending_authorization_cannot_remain_resumable(self):
        data = self.load(self.packets)
        pending = next(x for x in data["state_records"] if x["state_record_id"] == "PendingAuthorizationState")
        pending["activation_contract"]["unbound_request_correlatable"] = True
        pending["activation_contract"]["unavailable_binding_becomes_active"] = True
        pending["activation_contract"]["binding_unavailable"] = "status=pending and resumable"
        self.save(self.packets, data)
        self.assert_error("unbound PendingAuthorizationState remains resumable")

    def test_binding_failure_cannot_emit_ask_then_unavailable(self):
        data = self.load(self.packets)
        data["pre_ingress_terminal_authority_contract"]["binding_resolution_terminal_count"] = 2
        self.save(self.packets, data)
        self.assert_error("binding failure can emit ASK followed by UNAVAILABLE")

    def test_pending_authorization_requires_expiry(self):
        data = self.load(self.packets)
        pending = next(x for x in data["state_records"] if x["state_record_id"] == "PendingAuthorizationState")
        pending["required_fields"].remove("expires_at")
        data["pre_ingress_authorization_loop"]["repetition_contract"]["expiry_required"] = False
        self.save(self.packets, data)
        self.assert_error("outstanding authorization request lacks expiry")

    def test_pending_authorization_requires_finite_attempt_bound(self):
        data = self.load(self.packets)
        pending = next(x for x in data["state_records"] if x["state_record_id"] == "PendingAuthorizationState")
        pending["required_fields"].remove("maximum_attempts")
        data["pre_ingress_authorization_loop"]["repetition_contract"]["maximum_attempts"] = None
        self.save(self.packets, data)
        self.assert_error("lacks finite retry/attempt bound")

    def test_pending_authorization_requires_replay_rule(self):
        data = self.load(self.packets)
        data["pre_ingress_authorization_loop"]["repetition_contract"]["replay_rule_required"] = False
        pending = next(x for x in data["state_records"] if x["state_record_id"] == "PendingAuthorizationState")
        pending["invariants"] = [x for x in pending["invariants"] if "replay" not in x]
        self.save(self.packets, data)
        self.assert_error("replayable authorization request lacks replay rule")

    def test_authorization_result_requires_evidenced_validity_lifetime(self):
        data = self.load(self.packets)
        data["authorization_result_validity_contract"]["allowed_validity_lifetimes"].append("session")
        data["authorization_result_validity_contract"]["bare_session_allowed"] = True
        self.save(self.packets, data)
        self.assert_error("claims session validity without evidenced lifetime binding")

    def test_pre_ingress_authority_cannot_dispatch_ordinary_service(self):
        data = self.load(self.packets)
        authority = data["service_exchange_authority_contract"]["pre_ingress_authorization"]
        authority["allowed_interface"] = "IF-TIME-PROVIDER"
        authority["allowed_service_id"] = "tool_call"
        authority["ordinary_control_decision_authority"] = True
        self.save(self.packets, data)
        self.assert_error("can authorize an ordinary service")

    def test_attempt_policy_has_one_authoritative_owner(self):
        data = self.load(self.components)
        auth = next(x for x in data["components"] if x["component_id"] == "authorization_evaluator")
        auth["owns"].append("authorization_attempt_permission")
        self.save(self.components, data)
        self.assert_error("attempt policy is not owned solely by security_restraint")

    def test_turn_controller_cannot_declare_hidden_cross_turn_state(self):
        data = self.load(self.components)
        controller = next(x for x in data["components"] if x["component_id"] == "turn_controller")
        controller["state_lifetime"] = ["turn", "host_session"]
        self.save(self.components, data)
        self.assert_error("Turn Controller declares hidden cross-turn state")

    def test_persona_cannot_own_routing(self):
        data = self.load(self.components)
        model = next(x for x in data["components"] if x["component_id"] == "model_execution_boundary")
        model["owns"].append("route_selection")
        self.save(self.components, data)
        self.assert_error("Persona/model boundary is assigned route ownership")

    def test_historical_containers_cannot_return(self):
        data = self.load(self.components)
        clone = dict(data["components"][0])
        clone["component_id"] = "school_engine"
        clone["name"] = "School Engine"
        data["components"].append(clone)
        self.save(self.components, data)
        self.assert_error("forbidden historical successor component")

    def test_legacy_pass_and_school_must_be_rejected(self):
        data = self.load(self.behaviors)
        next(x for x in data["behaviors"] if x["behavior"] == "legacy PASS")["primary_domain"] = "deterministic_core"
        next(x for x in data["behaviors"] if x["behavior"] == "School Engine")["primary_domain"] = "deferred"
        self.save(self.behaviors, data)
        self.assert_error("legacy PASS is not rejected")
        self.assert_error("School Engine is restored")

    def test_skillforge_cannot_be_embedded(self):
        data = self.load(self.behaviors)
        item = next(x for x in data["behaviors"] if x["behavior"] == "modern PASS/SkillForge integration boundary")
        item["primary_domain"] = "deterministic_core"
        self.save(self.behaviors, data)
        self.assert_error("modern PASS/SkillForge is embedded")

    def test_host_specific_adapter_implementation_fails(self):
        data = self.load(self.interfaces)
        data["interfaces"][0]["host_specific"] = True
        data["interfaces"][0]["provider_binding"] = "CodexSDK"
        self.save(self.interfaces, data)
        self.assert_error("host-specific implementation")

    def test_local_mirror_binding_fails(self):
        data = self.load(self.components)
        continuity = next(x for x in data["components"] if x["component_id"] == "continuity_provider_boundary")
        continuity["provider_binding"] = "Local Mirror"
        self.save(self.components, data)
        self.assert_error("Local Mirror implementation")

    def test_runtime_package_fails(self):
        target = self.root / "src/blu_core/successor"
        target.mkdir(parents=True)
        (target / "runtime.py").write_text("pass\n", encoding="utf-8")
        self.assert_error("Python runtime package added")

    def test_golden_change_fails(self):
        target = self.root / "kernel/golden/v0.22.0/03_Exec.md"
        target.write_text(target.read_text(encoding="utf-8") + "\nchanged", encoding="utf-8")
        self.assert_error("golden checksum mismatch")


if __name__ == "__main__":
    unittest.main()
