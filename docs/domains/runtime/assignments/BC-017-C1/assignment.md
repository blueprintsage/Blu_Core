# BC-017-C1 — Historical Archaeology Review Corrections

status: review
owner: docs/domains/runtime
last_reviewed: 2026-08-07
approved_by: Dad
implementation_owner: Codex
semantic_reviewer: Claude
parent_assignment: BC-017
triggering_review: c323cff06c9f111408f4a416817d78fc0f3e2d2b
exact_base: c323cff06c9f111408f4a416817d78fc0f3e2d2b
branch: bc-017-c1-review-corrections

## Objective

Address only Claude's three blocking BC-017 findings:

- B-01: strip erroneous leading diff-marker `+` characters from the
  archaeology README.
- B-02: correct that README's validator and test reproduction commands to the
  real committed paths.
- B-03: place the directly evidenced BLU-HIST-0195 to BLU-HIST-0200 Exec
  contraction within v0.16.0, keep later v0.20/v0.21 restructuring distinct,
  and disclose the different BC-016 v0.21 milestone framing.

## Allowed collision domain

- `docs/sources/historical_archives/behavioral_archaeology/README.md`
- `docs/sources/historical_archives/behavioral_archaeology/transition_map.md`
- `docs/sources/historical_archives/behavioral_archaeology/behavioral_evidence_report.md`
- `docs/sources/historical_archives/behavioral_archaeology/boundary_specimens.json`
- `docs/sources/historical_archives/behavioral_archaeology/behavior_recovery_matrix.md`
- this BC-017-C1 assignment quartet
- repository-standard assignment index and runtime continuity metadata
- `MANIFEST.sha256`

## Protected and prohibited

Do not modify BC-017's Claude review, current CTS, historical evidence
identities, runtime contracts, architecture, configuration, validator behavior,
modern PASS/SkillForge, or runtime implementation. Do not address Claude's
non-blocking notes, redo archaeology, merge, or start another review.

## Required validation

Run all four repository validator/test suites, `git diff --check`, canonical
manifest verification, golden checksum verification, the malformed-heading
grep, and manual B-01/B-02/B-03 acceptance checks. Confirm protected paths and
archive payloads remain unchanged.

## Completion

Create a substantive correction commit and, because its SHA must be recorded,
one metadata-only commit. Push the correction branch normally. Status remains
`review`.
