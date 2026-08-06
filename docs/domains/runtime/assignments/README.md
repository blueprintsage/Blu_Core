# Runtime Assignment Records

status: active
owner: docs/domains/runtime
last_reviewed: 2026-08-05

This directory stores task-specific records for assignments owned by the runtime
domain.

Canonical shape:

```text
assignments/<assignment-id>/
├── assignment.md
├── handoff.md
├── validation.md
└── review.md
```

Use `docs/dev/domain_assignment_record_standard.md`.

The runtime domain's cumulative files remain:

```text
decisions.md
worklog.md
failures.md
next_steps.md
```

Assignment folders preserve detailed evidence. The cumulative files preserve
knowledge that must carry forward between assignments.

For assignments completed before this directory standard existed, backfill only
from committed evidence. Mark reconstructed metadata as `backfilled`; do not
invent missing command output or rewrite Git history.
