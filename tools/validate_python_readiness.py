#!/usr/bin/env python3
"""Validate One-Blu portability and BC-041 Python Phase 1 readiness."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


BASE_COMMIT = "699ee1485cef39ffbe70c3b8e848763af02596e0"
READINESS = Path("readiness")
ASSIGNMENT = Path("docs/domains/runtime/assignments/BC-041")
REQUIRED = {
    READINESS / "README.md",
    READINESS / "one_blu_canon_manifest.json",
    READINESS / "deployment_targets.json",
    READINESS / "model_execution_provider_contract.json",
    READINESS / "lm_studio_official_evidence.json",
    READINESS / "schemas/runtime_config.schema.json",
    READINESS / "python_package_layout.json",
    READINESS / "phase1_executable_slice.json",
    READINESS / "implementation_gap_dispositions.json",
    READINESS / "implementation_blocker_dispositions.json",
    READINESS / "custom_gpt_python_parity_matrix.json",
    READINESS / "python_phase1_readiness_checklist.json",
    READINESS / "schema_runtime.json",
    Path("requirements-contracts.txt"),
    Path("contracts/runtime/unresolved_register.json"),
    Path("contracts/successor/component_registry.json"),
    Path("contracts/successor/packet_registry.json"),
    Path("contracts/successor/interface_registry.json"),
    Path("contracts/successor/unresolved_register.json"),
    Path("contracts/security/opsec/README.md"),
    Path("contracts/security/opsec/minimum_contract.json"),
    Path("contracts/security/opsec/schemas/protected_policy.schema.json"),
    Path("contracts/security/opsec/schemas/security_evaluation.schema.json"),
    Path("tests/security/fixtures/synthetic_policy.json"),
    Path("tests/security/fixtures/synthetic_cases.json"),
    Path("continuity/schemas/continuity_mutation_request.schema.json"),
    Path("tests/continuity/fixtures/schema_instances.json"),
    Path("docs/domains/runtime/one_blu_python_readiness.md"),
    ASSIGNMENT / "assignment.md",
    ASSIGNMENT / "handoff.md",
    ASSIGNMENT / "validation.md",
    ASSIGNMENT / "review.md",
    Path("MANIFEST.sha256"),
}
JSON_FILES = {path for path in REQUIRED if path.suffix == ".json"}
GAP_DECISIONS = {
    "implement in Phase 1",
    "implement in later named phase",
    "deliberately unsupported",
    "preserved current behavior via model-facing canon",
    "requires provider evidence",
    "requires protected security assignment",
    "optional/non-core",
    "obsolete architecture mechanism whose behavior is preserved elsewhere",
}
BLOCKER_CATEGORIES = {
    "must_resolve_before_phase1",
    "phase1_fail_closed_supported",
    "not_in_phase1_scope",
    "blocks_protected_feature_only",
    "requires_separate_security_authority",
}
ALLOWED_PYTHON = {
    "tools/validate_continuity_contracts.py",
    "tests/continuity/test_validate_continuity_contracts.py",
    "tools/validate_python_readiness.py",
    "tests/readiness/test_validate_python_readiness.py",
    "tools/validate_opsec_contracts.py",
    "tests/security/test_validate_opsec_contracts.py",
}


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _git(root: Path, *args: str, text: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        check=False,
        capture_output=True,
        text=text,
    )


def _validate_golden(root: Path) -> list[str]:
    errors: list[str] = []
    manifest = root / "kernel/golden/v0.22.0/SHA256SUMS"
    if not manifest.is_file():
        return ["missing golden checksum manifest"]
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected, relative = line.split(None, 1)
        target = manifest.parent / relative.strip()
        if not target.is_file():
            errors.append(f"missing golden file: {relative.strip()}")
        elif hashlib.sha256(target.read_bytes()).hexdigest().lower() != expected.lower():
            errors.append(f"golden checksum mismatch: {relative.strip()}")
    return errors


def _validate_git_scope(root: Path) -> list[str]:
    if not (root / ".git").exists():
        return []
    result = _git(root, "diff", "--name-only", BASE_COMMIT, "--")
    if result.returncode != 0:
        return ["unable to verify Git diff from BC-041 base"]
    errors: list[str] = []
    for path in [line.strip() for line in result.stdout.splitlines() if line.strip()]:
        normalized = path.replace("\\", "/")
        lower = normalized.lower()
        if lower.startswith("kernel/golden/v0.22.0/"):
            errors.append(f"golden CTS changed: {path}")
        if lower.endswith(".py") and normalized not in ALLOWED_PYTHON:
            errors.append(f"production or disallowed Python changed: {path}")
        if re.search(r"(^|/)(pass|skillforge)(/|$)", lower):
            errors.append(f"PASS/SkillForge crossover: {path}")
        if re.search(r"(^|/)(lm[_-]?studio|local_mirror)(/|$)", lower):
            errors.append(f"provider implementation path changed: {path}")
    for root_name in ("src", "runtime", "blu_core", "providers", "lm_studio", "local_mirror"):
        candidate = root / root_name
        if candidate.exists() and any(item.is_file() for item in candidate.rglob("*")):
            errors.append(f"runtime/provider implementation tree exists: {root_name}")
    return errors


def _validate_manifest(root: Path) -> list[str]:
    if not (root / ".git").exists():
        return []
    listed = _git(root, "ls-files", "--cached", "--others", "--exclude-standard")
    if listed.returncode != 0:
        return ["unable to enumerate manifest scope"]
    expected = {line.strip() for line in listed.stdout.splitlines() if line.strip()} - {"MANIFEST.sha256"}
    entries: dict[str, str] = {}
    duplicates: set[str] = set()
    for line in (root / "MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        parts = line.split(None, 1)
        if len(parts) != 2:
            return ["invalid MANIFEST.sha256 entry"]
        digest, path = parts[0].lower(), parts[1].strip()
        if path in entries:
            duplicates.add(path)
        entries[path] = digest
    errors = [f"manifest missing path: {path}" for path in sorted(expected - set(entries))]
    errors.extend(f"manifest has stale path: {path}" for path in sorted(set(entries) - expected))
    errors.extend(f"manifest duplicate path: {path}" for path in sorted(duplicates))
    for path in sorted(expected & set(entries)):
        blob = _git(root, "show", f":{path}", text=False)
        if blob.returncode == 0:
            value = blob.stdout
        else:
            value = (root / path).read_bytes()
            if b"\x00" not in value:
                value = value.replace(b"\r\n", b"\n")
        if hashlib.sha256(value).hexdigest() != entries[path]:
            errors.append(f"manifest digest mismatch: {path}")
    return errors


def validate_projection(manifest: dict[str, Any], projection: dict[str, Any]) -> list[str]:
    """Validate a future generated deployment projection without claiming semantics."""
    mappings = {item["mapping_id"]: item for item in manifest.get("mappings", [])}
    entries = {item.get("mapping_id"): item for item in projection.get("entries", [])}
    errors: list[str] = []
    for mapping_id, mapping in mappings.items():
        target_key = f"{projection.get('target_id', '').split('_')[0]}_projection"
        if mapping.get(target_key) and mapping_id not in entries:
            errors.append(f"projection missing canonical mapping: {mapping_id}")
    for mapping_id, entry in entries.items():
        mapping = mappings.get(mapping_id)
        if mapping is None:
            errors.append(f"projection has unknown mapping: {mapping_id}")
            continue
        if entry.get("source_digest_current") is not True:
            errors.append(f"projection source digest is stale: {mapping_id}")
        if entry.get("transformation_type") != mapping.get("allowed_transformation_type"):
            errors.append(f"projection transformation is not allowed: {mapping_id}")
        if entry.get("canonical_subject_override") not in (None, ""):
            errors.append(f"host projection redefines canonical behavior: {mapping_id}")
    return errors


def validate(root: Path) -> list[str]:
    missing = [str(path) for path in sorted(REQUIRED) if not (root / path).is_file()]
    if missing:
        return [f"missing required file: {path}" for path in missing]
    errors: list[str] = []
    data: dict[Path, Any] = {}
    for path in sorted(JSON_FILES):
        try:
            data[path] = _load(root / path)
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            errors.append(f"invalid JSON: {path}: {exc}")
    if errors:
        return errors

    components = data[Path("contracts/successor/component_registry.json")]
    packets = data[Path("contracts/successor/packet_registry.json")]
    interfaces = data[Path("contracts/successor/interface_registry.json")]
    if len(components.get("components", [])) != 7:
        errors.append("successor component count is not seven")
    if len(packets.get("packets", [])) != 8:
        errors.append("successor packet count is not eight")
    if len(interfaces.get("interfaces", [])) != 9:
        errors.append("successor interface count is not nine")
    component_ids = {item.get("component_id") for item in components.get("components", [])}
    if component_ids != {
        "security_restraint", "authorization_evaluator", "turn_controller",
        "validation_egress", "model_execution_boundary", "host_adapter_boundary",
        "continuity_provider_boundary",
    }:
        errors.append("successor architectural component set changed")

    canon = data[READINESS / "one_blu_canon_manifest.json"]
    mapping_ids = [item.get("mapping_id") for item in canon.get("mappings", [])]
    if len(mapping_ids) < 10 or len(mapping_ids) != len(set(mapping_ids)):
        errors.append("One-Blu canon mapping is incomplete or duplicated")
    required_subject_terms = {
        "Persona", "Operations_Law", "teaching", "security", "authorization",
        "continuity", "model_execution", "validation", "source_and_receipt", "source_authority",
    }
    subjects = " ".join(str(item.get("subject")) for item in canon.get("mappings", []))
    if not all(term.lower() in subjects.lower() for term in required_subject_terms):
        errors.append("One-Blu canon mapping lacks a required behavioral subject")
    for item in canon.get("mappings", []):
        required_keys = {
            "canonical_source_artifact", "source_role", "current_cts_authority_relationship",
            "successor_behavioral_relationship", "chatgpt_projection", "python_projection",
            "exact_identity_required", "transformation_allowed", "allowed_transformation_type",
            "validation_method", "prohibited_divergence",
        }
        if not required_keys.issubset(item):
            errors.append(f"canon mapping fields incomplete: {item.get('mapping_id')}")

    targets = data[READINESS / "deployment_targets.json"].get("targets", [])
    target_map = {item.get("target_id"): item for item in targets}
    if target_map.get("chatgpt_custom_gpt", {}).get("classification") != "required":
        errors.append("ChatGPT target is not required")
    if target_map.get("python_lm_studio", {}).get("classification") != "required":
        errors.append("Python/LM Studio target is not required")
    if target_map.get("codex", {}).get("classification") != "optional_best_effort":
        errors.append("Codex target is not optional_best_effort")
    if target_map.get("codex", {}).get("blocks_python") is not False:
        errors.append("Codex blocks the primary Python architecture")

    phase1 = data[READINESS / "phase1_executable_slice.json"]
    routes = phase1.get("route_catalog", [])
    if len(routes) != 1 or routes[0].get("route_id") != "ordinary_conversation":
        errors.append("Phase 1 route catalog is not finite ordinary conversation only")
    if phase1.get("implementation_authorized") is not False:
        errors.append("BC-041 authorizes runtime implementation")
    if phase1.get("opsec_contract_ref") != "contracts/security/opsec/minimum_contract.json":
        errors.append("Phase 1 slice does not bind the BC-041 OPSEC contract")
    required_security_steps = {
        "pre_ingress_opsec_normalize_and_match",
        "egress_opsec_normalize_match_and_redact_or_block",
    }
    if not required_security_steps.issubset(phase1.get("turn_sequence", [])):
        errors.append("Phase 1 slice does not gate ingress and egress through OPSEC")

    source_gaps = data[Path("contracts/runtime/unresolved_register.json")].get("items", [])
    gap_contract = data[READINESS / "implementation_gap_dispositions.json"]
    gap_map = {item.get("gap_id"): item for item in gap_contract.get("dispositions", [])}
    source_gap_ids = {item.get("id") for item in source_gaps}
    if set(gap_map) != source_gap_ids or len(source_gap_ids) != 28:
        errors.append("SUR-010 gap mapping does not cover all 28 current-source gaps")
    for gap_id, item in gap_map.items():
        if item.get("implementation_decision") not in GAP_DECISIONS:
            errors.append(f"invalid gap disposition: {gap_id}")
        required = {"source_evidence", "behavior_at_risk", "rationale", "target_phase", "changes_current_behavior", "validation_requirement"}
        if not required.issubset(item):
            errors.append(f"gap disposition fields incomplete: {gap_id}")
        if item.get("changes_current_behavior") is not False:
            errors.append(f"gap disposition projects a behavior change into CTS: {gap_id}")

    source_unresolved = data[Path("contracts/successor/unresolved_register.json")].get("items", [])
    source_blocking = {item.get("id") for item in source_unresolved if item.get("blocking_for_implementation") is True}
    blocker_contract = data[READINESS / "implementation_blocker_dispositions.json"]
    dispositions = {item.get("id"): item for item in blocker_contract.get("dispositions", [])}
    if set(dispositions) != {item.get("id") for item in source_unresolved}:
        errors.append("not every successor unresolved item is dispositioned")
    if set(blocker_contract.get("source_blocking_for_implementation", [])) != source_blocking:
        errors.append("implementation blocker source set is stale")
    for item_id in source_blocking:
        if item_id not in dispositions:
            continue
        if dispositions[item_id].get("phase1_category") not in BLOCKER_CATEGORIES:
            errors.append(f"blocking item lacks a Phase 1 category: {item_id}")
    if blocker_contract.get("actual_blockers") != []:
        errors.append("actual Phase 1 blocker set is not exact")
    sur001 = dispositions.get("SUR-001", {})
    if sur001.get("disposition") != "resolved_at_minimum_phase1_contract_level" or sur001.get("phase1_resolved") is not True:
        errors.append("SUR-001 is not resolved at the minimum Phase 1 contract level")
    source_sur001 = next((item for item in source_unresolved if item.get("id") == "SUR-001"), {})
    if source_sur001.get("disposition") != "resolved_at_minimum_phase1_contract_level" or source_sur001.get("blocking_for_implementation") is not False:
        errors.append("successor SUR-001 disposition is stale")

    opsec = data[Path("contracts/security/opsec/minimum_contract.json")]
    if opsec.get("security_decision_values") != ["PASS", "BLOCK", "ASK"]:
        errors.append("SecurityDecision vocabulary changed")
    if opsec.get("matcher", {}).get("model_invocation_allowed") is not False:
        errors.append("OPSEC matcher depends on model invocation")
    if opsec.get("normalization", {}).get("semantic_paraphrase_detection") is not False:
        errors.append("OPSEC contract overclaims semantic paraphrase detection")

    provider = data[READINESS / "model_execution_provider_contract.json"]
    if provider.get("architectural_component") != "model_execution_boundary" or provider.get("new_component_added") is not False:
        errors.append("model provider became a new architectural component")
    capability_map = {item.get("capability"): item for item in provider.get("phase1_capabilities", [])}
    if capability_map.get("ordinary_chat_completion", {}).get("classification") != "required":
        errors.append("ordinary chat completion is not required")
    if capability_map.get("streaming", {}).get("classification") != "unsupported":
        errors.append("Phase 1 streaming policy is not frozen unsupported")
    if capability_map.get("tool_execution", {}).get("classification") != "unsupported":
        errors.append("Phase 1 permits tool execution")
    truth_chain = provider.get("tool_candidate_truth_chain", [])
    if len(truth_chain) != 6 or truth_chain[0] != "model_tool_call_candidate":
        errors.append("tool-call candidate truth chain is incomplete")

    evidence = data[READINESS / "lm_studio_official_evidence.json"]
    if not evidence.get("records") or any(
        not item.get("url", "").startswith("https://lmstudio.ai/docs/")
        for item in evidence.get("records", [])
    ):
        errors.append("LM Studio assumptions are not backed by exact official evidence")
    protocol = evidence.get("phase1_protocol_decision", {})
    if protocol.get("inference_endpoint") != "POST /api/v1/chat" or protocol.get("stream") is not False or protocol.get("store") is not False:
        errors.append("LM Studio Phase 1 protocol decision is incomplete")

    config_schema = data[READINESS / "schemas/runtime_config.schema.json"]
    try:
        Draft202012Validator.check_schema(config_schema)
    except Exception as exc:
        errors.append(f"runtime configuration schema is invalid: {exc}")
    if "C:\\Users" in json.dumps(config_schema) or "/home/" in json.dumps(config_schema):
        errors.append("runtime configuration embeds a personal machine path")
    protected_ref = config_schema.get("properties", {}).get("runtime", {}).get("properties", {}).get("protected_policy_ref", {})
    if protected_ref.get("type") != "object" or protected_ref.get("properties", {}).get("kind", {}).get("const") != "environment_file":
        errors.append("protected policy reference is not portable and opaque")
    if "rules" in protected_ref.get("properties", {}) or "value" in protected_ref.get("properties", {}):
        errors.append("protected policy values can be embedded in runtime configuration")

    layout = data[READINESS / "python_package_layout.json"]
    if layout.get("layout_type") != "src" or layout.get("implementation_present") is not False:
        errors.append("Python package layout is not a spec-only src layout")
    mapping = layout.get("architecture_mapping", {})
    if set(mapping) != component_ids:
        errors.append("Python package layout does not map beneath exactly seven components")

    parity = data[READINESS / "custom_gpt_python_parity_matrix.json"]
    if len(parity.get("parity_dimensions", [])) < 11 or len(parity.get("scenarios", [])) < 8:
        errors.append("Custom GPT/Python parity contract is incomplete")
    if parity.get("comparison_method", {}).get("live_chat_execution_required_by_BC040") is not False:
        errors.append("BC-040 requires unauthorized live Chat probing")

    checklist = data[READINESS / "python_phase1_readiness_checklist.json"]
    checks = {item.get("id"): item for item in checklist.get("checks", [])}
    if checks.get("minimum_OPSEC_match_and_redaction_contract_available", {}).get("status") != "pass":
        errors.append("minimum OPSEC contract readiness check is not pass")
    if checklist.get("result") != "ready_for_python_phase1":
        errors.append("readiness result does not reflect resolved SUR-001")
    if checklist.get("actual_blockers") != []:
        errors.append("readiness checklist retains stale blockers")
    if checklist.get("runtime_phase1_packet_may_be_authored_next") is not True:
        errors.append("runtime packet may not be authored despite resolved SUR-001")
    if checklist.get("automatic_start_prohibited") is not True:
        errors.append("readiness automatically starts runtime implementation")
    if checklist.get("full_successor_feature_complete") is not False:
        errors.append("BC-040 claims full successor feature completeness")

    runtime_selection = data[READINESS / "schema_runtime.json"]
    if runtime_selection.get("package") != "jsonschema" or runtime_selection.get("version") != "4.26.0":
        errors.append("Python JSON Schema runtime selection changed")
    try:
        installed = importlib.metadata.version("jsonschema")
    except importlib.metadata.PackageNotFoundError:
        errors.append("selected jsonschema runtime is not installed")
    else:
        if installed != "4.26.0":
            errors.append(f"selected jsonschema runtime version mismatch: {installed}")

    errors.extend(_validate_golden(root))
    errors.extend(_validate_git_scope(root))
    errors.extend(_validate_manifest(root))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    errors = validate(args.root.resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"Python readiness validation failed: {len(errors)} error(s)")
        return 1
    print("Python readiness validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
