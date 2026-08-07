#!/usr/bin/env python3
"""Validate BC-017's published behavioral-archaeology evidence records."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

ARCHIVE_DIR = Path("docs/sources/historical_archives")
ARCHAEOLOGY_DIR = ARCHIVE_DIR / "behavioral_archaeology"
ASSIGNMENT_DIR = Path("docs/domains/runtime/assignments/BC-017")
REQUIRED = {
    ARCHAEOLOGY_DIR / "README.md",
    ARCHAEOLOGY_DIR / "boundary_specimens.json",
    ARCHAEOLOGY_DIR / "evidence_register.json",
    ARCHAEOLOGY_DIR / "behavior_recovery_matrix.md",
    ARCHAEOLOGY_DIR / "behavioral_evidence_report.md",
    ARCHAEOLOGY_DIR / "transition_map.md",
    ASSIGNMENT_DIR / "assignment.md",
    ASSIGNMENT_DIR / "handoff.md",
    ASSIGNMENT_DIR / "validation.md",
    ASSIGNMENT_DIR / "review.md",
    ASSIGNMENT_DIR / "owner_observations.md",
}
ALLOWED_DISPOSITIONS = {
    "recover_model_facing_guidance",
    "recover_lightweight_profile",
    "specify_deterministic_mechanism",
    "retain_regression_test",
    "chronology_only",
    "reject",
    "needs_more_evidence",
}
FACT_LABELS = {
    "historical_declared",
    "historical_mechanically_scaffolded",
    "cross_version_persistent",
}
OWNER_LABELS = {"owner_observation", "owner_observed_failure"}
PROHIBITED_PATH = re.compile(
    r"(?i)(?:[a-z]:[\\/]|(?:^|[^\\])\\\\|file://|%2e|(?:^|[^A-Za-z0-9])\.\.(?:[\\/]|$))"
)
ARCHIVE_SUFFIXES = {".zip", ".7z", ".rar", ".tar", ".gz", ".bz2", ".xz"}
SHA_RE = re.compile(r"^[0-9a-f]{64}$")


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _matrix_rows(path: Path) -> list[dict[str, str]]:
    lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.startswith("|")]
    if len(lines) < 3:
        return []
    headers = [part.strip() for part in lines[0].strip("|").split("|")]
    rows = []
    for line in lines[2:]:
        values = [part.strip() for part in line.strip("|").split("|")]
        if len(values) == len(headers):
            rows.append(dict(zip(headers, values)))
    return rows


def _collect_archive_ids(value: Any) -> set[str]:
    ids: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            if key in {"record_id", "source_record_id", "first_specimen_archive_id",
                       "last_specimen_archive_id"} and isinstance(item, str) and item.startswith("BLU-"):
                ids.add(item)
            elif key in {"record_ids", "drilldown_specimens", "affected_record_ids"} and isinstance(item, list):
                ids.update(x for x in item if isinstance(x, str) and x.startswith("BLU-"))
            ids.update(_collect_archive_ids(item))
    elif isinstance(value, list):
        for item in value:
            ids.update(_collect_archive_ids(item))
    return ids


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    missing = [str(path) for path in sorted(REQUIRED) if not (root / path).is_file()]
    if missing:
        errors.extend(f"missing required file: {path}" for path in missing)
        return errors

    inventory = _load(root / ARCHIVE_DIR / "kernel_archive_inventory.json")
    records = {record["archive_id"]: record for record in inventory["inventory"]}
    boundary = _load(root / ARCHAEOLOGY_DIR / "boundary_specimens.json")
    evidence = _load(root / ARCHAEOLOGY_DIR / "evidence_register.json")

    for source_name, value in (("boundary", boundary), ("evidence", evidence)):
        unknown = sorted(_collect_archive_ids(value) - set(records))
        errors.extend(f"{source_name} references unknown archive ID: {item}" for item in unknown)

    for path in sorted(ARCHAEOLOGY_DIR.glob("*")):
        full = root / path
        if full.is_file() and PROHIBITED_PATH.search(full.read_text(encoding="utf-8")):
            errors.append(f"absolute/local or traversal path leakage: {path}")

    supported_boundary_ids: set[str] = set()
    for family in boundary.get("families", []):
        if not family.get("selection_basis"):
            errors.append(f"boundary missing selection basis: {family.get('family')}")
        for key in ("first_specimen_archive_id", "last_specimen_archive_id"):
            item = family.get(key)
            if item:
                supported_boundary_ids.add(item)
        if family.get("last_specimen_archive_id") is None and not family.get("boundary_ambiguity"):
            errors.append(f"null last boundary lacks ambiguity reason: {family.get('family')}")
        if family.get("first_specimen_archive_id") is None and not family.get("boundary_ambiguity"):
            errors.append(f"null first boundary lacks ambiguity reason: {family.get('family')}")
        supported_boundary_ids.update(family.get("drilldown_specimens", []))

    for item in sorted(supported_boundary_ids):
        record = records.get(item)
        if record and record.get("integrity_status") != "readable":
            errors.append(f"unsupported/unavailable specimen carries behavioral selection: {item}")

    rows = _matrix_rows(root / ARCHAEOLOGY_DIR / "behavior_recovery_matrix.md")
    if not rows:
        errors.append("recovery matrix has no parseable rows")
    for row in rows:
        behavior = row.get("behavior", "<unknown>")
        disposition = row.get("recommended_disposition")
        if disposition not in ALLOWED_DISPOSITIONS:
            errors.append(f"matrix row has disallowed disposition: {behavior}")
        if not row.get("evidence_locators"):
            errors.append(f"matrix row lacks evidence locator: {behavior}")
        if "legacy PASS" in behavior and disposition != "chronology_only":
            errors.append("legacy PASS receives a recovery disposition")

    locators = {item["id"]: item for item in evidence.get("locators", [])}
    findings = {item["id"]: item for item in evidence.get("findings", [])}
    for finding in findings.values():
        label = finding.get("label")
        locator_ids = finding.get("locator_ids", [])
        if label in FACT_LABELS and not locator_ids:
            errors.append(f"factual historical finding lacks evidence locator: {finding.get('id')}")
        if label in OWNER_LABELS and not finding.get("owner_observation_id"):
            errors.append(f"owner observation is not linked/labeled: {finding.get('id')}")
        if label == "current_source_truth":
            if not locator_ids or any(locators.get(item, {}).get("source_class") != "current_source_truth" for item in locator_ids):
                errors.append(f"current CTS claim is not sourced as current_source_truth: {finding.get('id')}")
        if label == "inference":
            support = finding.get("supporting_finding_ids", [])
            if not support or any(item not in findings for item in support):
                errors.append(f"inference is mislabeled or lacks finding support: {finding.get('id')}")
        for item in locator_ids:
            if item not in locators:
                errors.append(f"finding references unknown evidence locator: {finding.get('id')} -> {item}")

    sidecar = evidence.get("faithfulness_sidecar", {})
    if sidecar.get("classification") != "unshipped_sidecar_design":
        errors.append("Faithfulness sidecar is labeled shipped without direct archive evidence")
    if sidecar.get("archive_scan", {}).get("filename_hits", 0) == 0 and "shipped" in sidecar.get("classification", "") and not sidecar.get("classification", "").startswith("unshipped"):
        errors.append("Faithfulness sidecar shipping claim lacks direct archive evidence")

    for base in (root / ARCHAEOLOGY_DIR, root / ASSIGNMENT_DIR):
        for path in base.rglob("*"):
            if path.is_file() and path.suffix.lower() in ARCHIVE_SUFFIXES:
                errors.append(f"archive payload present in BC-017 output: {path.relative_to(root)}")

    allowed_python = {
        root / "tools/validate_historical_behavioral_archaeology.py",
        root / "tests/historical_archaeology/test_validate_historical_behavioral_archaeology.py",
    }
    for path in root.rglob("*.py"):
        if "BC-017" in path.as_posix() or "behavioral_archaeology" in path.as_posix():
            if path not in allowed_python:
                errors.append(f"Python runtime/control-plane implementation in BC-017 output: {path.relative_to(root)}")

    review = (root / ASSIGNMENT_DIR / "review.md").read_text(encoding="utf-8").lower()
    if "status: pending" not in review or "read-only-review-ready" not in review:
        errors.append("review.md is not pending/read-only-review-ready")

    sums_path = root / "kernel/golden/v0.22.0/SHA256SUMS"
    for line in sums_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected, name = line.split(None, 1)
        name = name.strip()
        target = sums_path.parent / name
        if not SHA_RE.fullmatch(expected) or hashlib.sha256(target.read_bytes()).hexdigest() != expected:
            errors.append(f"golden checksum mismatch: {name}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = validate(args.root.resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("BC-017 historical behavioral archaeology validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
