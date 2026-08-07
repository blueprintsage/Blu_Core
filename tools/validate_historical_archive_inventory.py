#!/usr/bin/env python3
"""Validate BC-016's sanitized historical archive source map."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any


REQUIRED_FILES = {
    "README.md",
    "kernel_archive_inventory.json",
    "kernel_archive_inventory.csv",
    "snapshot_receipt.json",
    "reconciliation_report.md",
    "milestone_recommendations.md",
    "discovery_receipt.md",
}
TOP_LEVEL_FIELDS = {
    "schema_version",
    "generated_at",
    "integration_assignment",
    "source_roots",
    "snapshots",
    "inventory",
    "duplicate_groups",
    "reconciliation",
    "milestone_recommendations",
    "limitations",
}
INVENTORY_FIELDS = {
    "archive_id",
    "display_name",
    "version",
    "version_confidence",
    "date",
    "date_source",
    "branch",
    "source_type",
    "source_root_id",
    "relative_path",
    "filename",
    "file_size_bytes",
    "sha256",
    "availability_status",
    "integrity_status",
    "duplicate_group",
    "probable_architecture_era",
    "top_level_members",
    "key_files_present",
    "notable_capability_markers",
    "structural_metrics",
    "source_observation_class",
    "notes",
}
ALLOWED_BRANCHES = {"dev", "preview", "release", "unknown"}
ALLOWED_SOURCE_TYPES = {
    "archive_file",
    "current_branch_file_set",
    "historical_source_folder",
    "snapshot_outer_zip",
    "unknown",
}
ALLOWED_OBSERVATIONS = {
    "direct_file_inspection",
    "archive_member_listing",
    "folder_manifest",
    "external_inventory_import",
    "owner_supplied_snapshot_receipt",
    "unavailable",
}
ALLOWED_AVAILABILITY = {
    "available",
    "permission_blocked",
    "missing_target",
    "corrupt",
    "unsupported_format",
    "partially_readable",
}
ALLOWED_INTEGRITY = {"readable", "corrupt", "checksum_error", "not_applicable", "not_tested"}
ALLOWED_CONFIDENCE = {"high", "medium", "low", "unknown"}
ALLOWED_RECONCILIATION = {
    "matched_path_and_hash",
    "matched_hash_different_path",
    "live_directory_only",
    "snapshot_only",
    "inventory_only",
    "hash_mismatch",
    "unavailable_for_verification",
    "not_applicable",
}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
WINDOWS_ABSOLUTE_RE = re.compile(r"(?i)(?<![A-Za-z0-9])[A-Za-z]:[\\/]")
HOME_SEGMENT_RE = re.compile(r"(?i)(?:users|home)[\\/][^\\/\s]+")
POSIX_LOCAL_PREFIXES = tuple("/" + name + "/" for name in ("home", "Users", "private", "tmp", "var", "etc", "root", "mnt"))
PROOF_KEYS = {"worked", "stable", "implemented", "reliable", "approved_for_recovery", "behavior_status"}


def load_json(path: Path, errors: list[str]) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"cannot parse JSON {path.name}: {exc}")
        return None


def has_path_leak(text: str) -> bool:
    return bool(
        WINDOWS_ABSOLUTE_RE.search(text)
        or HOME_SEGMENT_RE.search(text)
        or any(prefix in text for prefix in POSIX_LOCAL_PREFIXES)
    )


def is_relative_path(value: Any) -> bool:
    if not isinstance(value, str) or not value or has_path_leak(value):
        return False
    path = PurePosixPath(value.replace("\\", "/"))
    return not path.is_absolute() and ".." not in path.parts


def validate(repo_root: Path) -> list[str]:
    errors: list[str] = []
    archive_dir = repo_root / "docs/sources/historical_archives"
    if not archive_dir.is_dir():
        return ["required historical archive directory is missing"]

    present = {p.name for p in archive_dir.iterdir() if p.is_file()}
    for name in sorted(REQUIRED_FILES - present):
        errors.append(f"required file missing: {name}")

    inventory_path = archive_dir / "kernel_archive_inventory.json"
    snapshot_path = archive_dir / "snapshot_receipt.json"
    if not inventory_path.exists() or not snapshot_path.exists():
        return errors
    data = load_json(inventory_path, errors)
    snapshot = load_json(snapshot_path, errors)
    if not isinstance(data, dict) or not isinstance(snapshot, dict):
        return errors

    missing_top = TOP_LEVEL_FIELDS - set(data)
    if missing_top:
        errors.append(f"missing top-level fields: {sorted(missing_top)}")
    if data.get("schema_version") != "1.0":
        errors.append("schema_version must be 1.0")
    if data.get("integration_assignment") != "BC-016":
        errors.append("integration_assignment must be BC-016")

    roots = data.get("source_roots")
    if not isinstance(roots, list):
        errors.append("source_roots must be a list")
        roots = []
    root_ids: set[str] = set()
    for root in roots:
        if not isinstance(root, dict) or not isinstance(root.get("source_root_id"), str):
            errors.append("source root missing source_root_id")
            continue
        root_id = root["source_root_id"]
        if root_id in root_ids:
            errors.append(f"duplicate source_root_id: {root_id}")
        root_ids.add(root_id)
        if root.get("authority") != "non_authoritative_for_current_runtime":
            errors.append(f"historical source root marked current CTS authority: {root_id}")

    inventory = data.get("inventory")
    if not isinstance(inventory, list):
        errors.append("inventory must be a list")
        inventory = []
    ids: list[str] = []
    by_id: dict[str, dict[str, Any]] = {}
    for index, record in enumerate(inventory):
        if not isinstance(record, dict):
            errors.append(f"inventory record {index} must be an object")
            continue
        missing = INVENTORY_FIELDS - set(record)
        if missing:
            errors.append(f"inventory record {index} missing fields: {sorted(missing)}")
        archive_id = record.get("archive_id")
        if not isinstance(archive_id, str) or not archive_id:
            errors.append(f"inventory record {index} has invalid archive_id")
            continue
        ids.append(archive_id)
        by_id.setdefault(archive_id, record)
        if record.get("branch") not in ALLOWED_BRANCHES:
            errors.append(f"unknown branch for {archive_id}: {record.get('branch')}")
        if record.get("source_type") not in ALLOWED_SOURCE_TYPES:
            errors.append(f"unknown source_type for {archive_id}: {record.get('source_type')}")
        if record.get("source_observation_class") not in ALLOWED_OBSERVATIONS:
            errors.append(f"unknown source_observation_class for {archive_id}")
        if record.get("availability_status") not in ALLOWED_AVAILABILITY:
            errors.append(f"unknown availability_status for {archive_id}")
        if record.get("integrity_status") not in ALLOWED_INTEGRITY:
            errors.append(f"unknown integrity_status for {archive_id}")
        if record.get("version_confidence") not in ALLOWED_CONFIDENCE:
            errors.append(f"unknown version_confidence for {archive_id}")
        sha256 = record.get("sha256")
        if not isinstance(sha256, str) or not SHA256_RE.fullmatch(sha256):
            errors.append(f"invalid SHA-256 for {archive_id}")
        if record.get("source_root_id") not in root_ids:
            errors.append(f"unknown source_root_id for {archive_id}")
        if not is_relative_path(record.get("relative_path")):
            errors.append(f"absolute or unsafe relative_path for {archive_id}")
        markers = record.get("notable_capability_markers")
        if not isinstance(markers, list):
            errors.append(f"notable_capability_markers must be a list for {archive_id}")
        else:
            for marker in markers:
                if not isinstance(marker, dict):
                    errors.append(f"marker must be an object for {archive_id}")
                    continue
                if any(marker.get(key) not in (None, False, "", [], {}) for key in PROOF_KEYS):
                    errors.append(f"marker presence represented as behavior proof for {archive_id}")

    if len(ids) != len(set(ids)):
        errors.append("duplicate archive ID")

    duplicate_groups = data.get("duplicate_groups")
    if not isinstance(duplicate_groups, list):
        errors.append("duplicate_groups must be a list")
        duplicate_groups = []
    seen_group_ids: set[str] = set()
    for group in duplicate_groups:
        if not isinstance(group, dict):
            errors.append("duplicate group must be an object")
            continue
        group_id = group.get("duplicate_group")
        members = group.get("archive_ids")
        digest = group.get("sha256")
        if not isinstance(group_id, str) or group_id in seen_group_ids:
            errors.append(f"invalid or duplicate duplicate-group ID: {group_id}")
        seen_group_ids.add(group_id)
        if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
            errors.append(f"invalid duplicate-group SHA-256: {group_id}")
        if not isinstance(members, list) or len(members) < 2:
            errors.append(f"duplicate group needs at least two members: {group_id}")
            continue
        member_records = [by_id.get(member) for member in members]
        if any(record is None for record in member_records):
            errors.append(f"duplicate group references missing archive ID: {group_id}")
            continue
        hashes = {record.get("sha256") for record in member_records if record}
        if hashes != {digest}:
            errors.append(f"duplicate group members have unequal hashes: {group_id}")
        for record in member_records:
            if record and record.get("duplicate_group") != group_id:
                errors.append(f"duplicate group backlink mismatch: {group_id}")

    milestones = data.get("milestone_recommendations")
    if not isinstance(milestones, list):
        errors.append("milestone_recommendations must be a list")
        milestones = []
    milestone_ids: set[str] = set()
    for milestone in milestones:
        archive_id = milestone.get("archive_id") if isinstance(milestone, dict) else None
        if archive_id not in by_id:
            errors.append(f"milestone references missing archive: {archive_id}")
            continue
        milestone_ids.add(archive_id)
        if milestone.get("sha256") != by_id[archive_id].get("sha256") or not SHA256_RE.fullmatch(str(milestone.get("sha256", ""))):
            errors.append(f"selected milestone lacks matching checksum: {archive_id}")
        if not is_relative_path(milestone.get("relative_path")):
            errors.append(f"milestone has unsafe relative_path: {archive_id}")

    reconciliation = data.get("reconciliation")
    if not isinstance(reconciliation, list):
        errors.append("reconciliation must be a list")
        reconciliation = []
    reconciliation_ids: set[str] = set()
    valid_identities = root_ids | {snapshot.get("snapshot_id")}
    for entry in reconciliation:
        if not isinstance(entry, dict):
            errors.append("reconciliation entry must be an object")
            continue
        rec_id = entry.get("reconciliation_id")
        if not isinstance(rec_id, str) or rec_id in reconciliation_ids:
            errors.append(f"invalid or duplicate reconciliation ID: {rec_id}")
        reconciliation_ids.add(rec_id)
        archive_id = entry.get("inventory_archive_id")
        if archive_id is not None and archive_id not in by_id:
            errors.append(f"reconciliation references missing archive: {archive_id}")
        if entry.get("status") not in ALLOWED_RECONCILIATION:
            errors.append(f"unknown reconciliation status: {entry.get('status')}")
        for side in ("left_source_identity", "right_source_identity"):
            identity = entry.get(side)
            if not isinstance(identity, dict) or identity.get("identity_id") not in valid_identities:
                errors.append(f"reconciliation references invalid source identity: {rec_id}")
                continue
            rel = identity.get("relative_path")
            if rel is not None and not is_relative_path(rel):
                errors.append(f"reconciliation has unsafe path: {rec_id}")
            digest = identity.get("sha256")
            if digest is not None and (not isinstance(digest, str) or not SHA256_RE.fullmatch(digest)):
                errors.append(f"reconciliation has invalid SHA-256: {rec_id}")

    required_snapshot_fields = {
        "snapshot_id", "filename", "sha256", "size_bytes", "zip_entries",
        "file_entries", "nested_zip_files", "top_level_root", "branches",
        "verification_status", "verified_by", "verified_at", "source_role",
        "authority", "limitations",
    }
    missing_snapshot = required_snapshot_fields - set(snapshot)
    if missing_snapshot:
        errors.append(f"snapshot receipt missing fields: {sorted(missing_snapshot)}")
    if not SHA256_RE.fullmatch(str(snapshot.get("sha256", ""))):
        errors.append("snapshot receipt has invalid SHA-256")
    if snapshot.get("authority") != "non_authoritative_for_current_runtime":
        errors.append("snapshot marked current CTS authority")
    if snapshot.get("verification_status") == "independently_verified" and (not snapshot.get("verified_by") or not snapshot.get("verified_at")):
        errors.append("snapshot marked independently verified without verifier metadata")

    csv_path = archive_dir / "kernel_archive_inventory.csv"
    if csv_path.exists():
        try:
            with csv_path.open("r", encoding="utf-8", newline="") as f:
                csv_rows = list(csv.DictReader(f))
            csv_ids = [row.get("archive_id") for row in csv_rows]
            if len(csv_rows) != len(inventory):
                errors.append("CSV/JSON count mismatch")
            if set(csv_ids) != set(ids):
                errors.append("CSV archive IDs do not equal JSON archive IDs")
        except OSError as exc:
            errors.append(f"cannot read inventory CSV: {exc}")

    for path in archive_dir.iterdir():
        if path.is_file():
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                errors.append(f"non-text historical deliverable: {path.name}")
                continue
            if has_path_leak(text):
                errors.append(f"absolute local path or home-directory leakage in {path.name}")

    for path in repo_root.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        rel = path.relative_to(repo_root).as_posix()
        if rel.startswith("kernel/golden/"):
            continue
        lower = path.name.casefold()
        if lower.endswith((".zip", ".7z", ".tar", ".tgz", ".tar.gz")):
            errors.append(f"historical archive embedded in repository: {rel}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = validate(args.root.resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("PASS: BC-016 historical archive inventory is sanitized and internally consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
