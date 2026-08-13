"""Shared BC-050 authorization mutation matrix (BC-050-C2 / B-01).

Every validator that relaxes a pre-implementation prohibition must reject each
mutation below on its own. Validator ordering is not an authorization
mechanism, so the same matrix is applied independently in the readiness,
security, and continuity suites.

This module holds data only. It imports nothing from `blu_runtime` and is not a
test module.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

CHECKLIST = "readiness/python_phase1_readiness_checklist.json"
SLICE = "readiness/phase1_executable_slice.json"

Mutation = tuple[str, Callable[[dict[str, Any], dict[str, Any]], None]]


def _record(checklist: dict[str, Any]) -> dict[str, Any]:
    return checklist["bc050_implementation_authorization"]


def _nested(executable_slice: dict[str, Any]) -> dict[str, Any]:
    return executable_slice["implementation_authorization"]


#: Codex's reproduction matrix, plus the nested-record and date cases.
MUTATIONS: tuple[Mutation, ...] = (
    ("wrong_authorized_by", lambda c, s: _record(c).__setitem__("authorized_by", "Mallory")),
    ("empty_authorized_by", lambda c, s: _record(c).__setitem__("authorized_by", "")),
    ("missing_authorized_by", lambda c, s: _record(c).pop("authorized_by")),
    ("wrong_packet_path", lambda c, s: _record(c).__setitem__("packet", "docs/domains/runtime/assignments/BC-999/assignment.md")),
    ("empty_packet_path", lambda c, s: _record(c).__setitem__("packet", "")),
    ("missing_packet", lambda c, s: _record(c).pop("packet")),
    ("wrong_assignment", lambda c, s: _record(c).__setitem__("assignment", "BC-999")),
    ("unstated_state", lambda c, s: _record(c).__setitem__("state", "proposed")),
    ("missing_state", lambda c, s: _record(c).pop("state")),
    ("missing_authorization_date", lambda c, s: _record(c).pop("authorization_date")),
    ("empty_authorization_date", lambda c, s: _record(c).__setitem__("authorization_date", "")),
    ("missing_record", lambda c, s: c.pop("bc050_implementation_authorization")),
    ("non_mapping_record", lambda c, s: c.__setitem__("bc050_implementation_authorization", "authorized")),
    ("checklist_flag_false", lambda c, s: c.__setitem__("implementation_authorized", False)),
    ("automatic_start_allowed", lambda c, s: c.__setitem__("automatic_start_prohibited", False)),
    ("slice_flag_disagrees", lambda c, s: s.__setitem__("implementation_authorized", False)),
    ("nested_assignment_bc999", lambda c, s: _nested(s).__setitem__("assignment", "BC-999")),
    ("nested_authorizer_wrong", lambda c, s: _nested(s).__setitem__("authorized_by", "Mallory")),
    ("nested_packet_wrong", lambda c, s: _nested(s).__setitem__("packet", "docs/elsewhere.md")),
    ("nested_date_disagrees", lambda c, s: _nested(s).__setitem__("authorization_date", "1999-01-01")),
    ("missing_nested_record", lambda c, s: s.pop("implementation_authorization")),
    ("non_mapping_nested_record", lambda c, s: s.__setitem__("implementation_authorization", ["BC-050"])),
)


def apply_mutation(root: Path, mutate: Callable[[dict[str, Any], dict[str, Any]], None]) -> None:
    """Apply one authorization mutation to the readiness records under `root`."""
    checklist_path = root / CHECKLIST
    slice_path = root / SLICE
    checklist = json.loads(checklist_path.read_text(encoding="utf-8"))
    executable_slice = json.loads(slice_path.read_text(encoding="utf-8"))
    mutate(checklist, executable_slice)
    checklist_path.write_text(json.dumps(checklist, indent=2) + "\n", encoding="utf-8")
    slice_path.write_text(json.dumps(executable_slice, indent=2) + "\n", encoding="utf-8")
