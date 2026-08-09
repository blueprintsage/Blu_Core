# BC-020-C1 — Correction Handoff

status: review
owner: Codex
last_reviewed: 2026-08-09
assignment: BC-020-C1
parent_assignment: BC-020

## Identity

- Base commit: `370278cd91fd9ecca2c64cd0953cae7ed63c4d16`
- Work branch: `bc-020-c1-scheduling-evidence-correction`
- Substantive correction commit: pending metadata-only receipt
- Metadata commit: reported externally because a commit cannot contain its own
  final SHA
- Push status: pending
- Working-tree status: substantive correction prepared; final Git receipts
  pending

## Result

BC-020 BF-1 and the directly coupled validator defects are corrected. The three
operational Codex scheduling capabilities are `unknown`; interface exposure is
preserved as an observation rather than promoted to operational availability.
No schedule was created, no adapter/runtime was implemented, and Claude's
original review remains unchanged.

## Corrected capability totals

```text
Codex capabilities: 52
verified_available: 24
verified_unavailable: 6
documented_possible: 4
unknown: 17
not_applicable: 1
Codex evidence entries: 22
```

## Files changed

```text
MANIFEST.sha256
adapters/common/capability_contract.json
adapters/codex/capability_matrix.json
adapters/codex/evidence_register.json
docs/dev/docs_index.md
docs/domains/runtime/adapters/codex_adapter.md
docs/domains/runtime/adapters/host_capability_truth.md
docs/domains/runtime/assignments/BC-020-C1/assignment.md
docs/domains/runtime/assignments/BC-020-C1/handoff.md
docs/domains/runtime/assignments/BC-020-C1/review.md
docs/domains/runtime/assignments/BC-020-C1/validation.md
docs/domains/runtime/failures.md
docs/domains/runtime/next_steps.md
docs/domains/runtime/worklog.md
docs/worklogs/assignments.md
tests/host_adapters/test_validate_host_adapter_contracts.py
tools/validate_host_adapter_contracts.py
```

## Deliverables completed

- Corrected scheduling statuses and limitations, including the narrowly scoped
  desktop execution dependency.
- Preserved `schedule.receipt = unknown`, receipt-required fields, and operation
  completion rules.
- Added an explicit documentary evidence entry for the desktop limitation.
- Added curated status-specific support-token validation for verified
  capability claims.
- Added focused regressions for scheduling interface exposure, unrelated Git
  and network evidence, opposite-polarity security evidence, valid rows, Chat
  documentary evidence, current time, and side-effect receipts.
- Added the C1 assignment quartet and runtime continuity/index updates.

## Unresolved items

- Operational scheduling availability and normalized schedule receipts remain
  unknown until a future authorized operation produces appropriate provider
  evidence.
- SUR-011 remains unresolved by design; BC-030 remains unstarted.

## Known risks

- The semantic validator uses a deliberately curated capability-to-support
  token map. New verified capability claims must add an explicit profile rather
  than relying on evidence class alone.
- Static validation cannot prove provider availability, permission, future
  execution, or receipt integrity.

## Domain continuity updates

- Worklog: correction, counts, validation boundary, and immutable review noted.
- Failures: reusable evidence-class-versus-relevance lesson recorded.
- Next steps: Claude re-review only; no BC-030 or runtime work.

## Reviewer focus

Confirm BF-1 is resolved, the validator rejects all demonstrated relevance
defects without invalidating truthful verified rows, scheduling receipt and
side-effect semantics remain intact, desktop limitation scope is not
generalized, and no protected boundary changed.
