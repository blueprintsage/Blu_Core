# Domain Assignment Record Standard

status: active
owner: docs/dev
last_reviewed: 2026-08-05
canonical: true

## Purpose

Keep each assignment's approved scope, implementation handoff, validation
evidence, and review decision together under the domain that owns the work.

This standard separates:

- the project-wide assignment index;
- task-specific evidence;
- cumulative domain continuity.

## Canonical location

```text
docs/domains/<domain>/assignments/<assignment-id>/
├── assignment.md
├── handoff.md
├── validation.md
└── review.md
```

Use the exact assignment ID from `docs/worklogs/assignments.md`.

## File ownership

### `assignment.md`

Owned by Blu as Project Lead or Dad as Project Owner.

Contains:

- assignment identity;
- objective;
- owner and reviewer;
- exact base branch or commit;
- allowed collision domain;
- protected and prohibited areas;
- required deliverables;
- required checks;
- completion conditions;
- approved amendments.

The approved packet must exist before the assignment becomes `active`.

Do not silently rewrite the original scope after work begins. Append an
authorized, dated amendment that identifies who approved it and why.

### `handoff.md`

Owned by the implementing agent.

Contains:

- base and work commit;
- branch;
- files changed;
- result summary;
- deliverables completed;
- known unresolved items;
- known risks;
- blocked work, if any;
- working-tree and push status.

A blocked assignment still requires a handoff.

### `validation.md`

Owned by the implementing agent, with reviewer additions clearly labeled.

Contains:

- exact commands run;
- exact result summaries;
- environment or dependency limitations;
- golden-source checks when required;
- failed validation attempts;
- any validation that was not possible.

A passing validator proves only the checks it actually performs.

### `review.md`

Owned by the assigned reviewer and finalized by Blu or Dad.

Contains:

- reviewed commit;
- source comparison performed;
- semantic findings;
- required corrections;
- disposition: approve, approve-with-notes, return-for-correction, or blocked;
- integration commit or merge identity when real;
- final assignment status.

## Global assignment index

`docs/worklogs/assignments.md` is an index, not the packet body.

Each row should include:

- assignment ID;
- short title;
- owner;
- status;
- domain packet path;
- exact base;
- work commit when available;
- review or integration commit when available;
- collision-domain summary.

Allowed status flow:

```text
spec-needed -> ready -> active -> review -> done
```

Use `blocked` when work cannot safely continue. A blocked status must link to
the handoff or failure record explaining why.

## Domain continuity relationship

The domain quartet remains cumulative:

```text
decisions.md
worklog.md
failures.md
next_steps.md
```

Use it as follows:

- `decisions.md`: approved design or authority decisions that survive one task;
- `worklog.md`: concise chronological record with links to assignment folders;
- `failures.md`: reusable failure knowledge, unsafe paths, and prevention rules;
- `next_steps.md`: current safe continuation, not a duplicate assignment packet.

Assignment-specific command output, detailed diffs, and handoff evidence belong
in the assignment folder.

Do not copy every minor failed command into `failures.md`. Promote a failure
there when it teaches a reusable lesson, exposes a danger zone, or should stop a
future agent from repeating the same path.

## Lifecycle

### Before implementation

1. Blu or Dad approves the packet.
2. Create the domain assignment folder.
3. Save the approved packet as `assignment.md`.
4. Add or update the global assignment-index row.
5. Verify the named base.
6. Move status to `active`.

### At implementation handoff

1. Write `handoff.md`.
2. Write `validation.md`.
3. Update the domain `worklog.md`.
4. Update `failures.md` when a reusable failure was found.
5. Update `next_steps.md`.
6. Record the real work commit.
7. Move status to `review`.

### At review and integration

1. Reviewer writes `review.md`.
2. Corrections use the same assignment folder unless Blu or Dad opens a new
   assignment.
3. Record the approved work and integration identities.
4. Update cumulative domain continuity.
5. Move status to `done`, `blocked`, or back to `active` for correction.

## Backfilling assignments created before this standard

A prior assignment may be backfilled only from committed evidence and the
approved packet that actually governed the work.

Rules:

- preserve the original base, scope, and owner;
- do not invent missing validation output;
- label reconstructed metadata as `backfilled`;
- link to the real commit and existing domain logs;
- record unavailable evidence as unavailable;
- do not rewrite implementation history merely to produce the folder.

## Authority boundary

Assignment records document work. They do not outrank:

1. Dad's current explicit instruction;
2. approved domain decisions;
3. the golden CTS kernel;
4. active project governance.

A record must never claim a commit, push, test, source read, or validation that
was not directly observed.
