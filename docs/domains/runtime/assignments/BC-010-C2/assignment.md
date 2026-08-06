# BC-010-C2 — OPSEC Route Classification Repair

status: review
owner: Codex
semantic_reviewer: Claude
approved_by: Dad
approved_on: 2026-08-06
record: approved assignment packet

## Authority and roles

- Project Owner: Dad
- Project Lead: Blu
- Implementation owner: Codex
- Semantic reviewer: Claude
- Parent assignments: BC-010 and BC-010-C1
- Exact base commit: `424f80b254a02f057da6c82db5230377076fc415`
- Branch: `bc-010-c2-opsec-route-repair`

This is a narrow correction assignment. It does not reopen the full
runtime-contract extraction.

## Base resolution

Resolve the base by fetching `origin`, switching to `main`, and fast-forwarding
only. Confirm that
`docs/domains/runtime/assignments/BC-010-C1/review.md` is present, record the
exact base, and create `bc-010-c2-opsec-route-repair`.

## Required startup reading

Read:

```text
AGENTS.md
CODEX.md
docs/dev/docs_index.md
docs/dev/assistant_coding_behavior.md
docs/dev/domain_assignment_record_standard.md
docs/worklogs/assignments.md
docs/sources/cts_source_roles.md
docs/architecture/current_runtime.md
docs/architecture/migration_centerline.md
docs/domains/runtime/assignments/BC-010-C1/assignment.md
docs/domains/runtime/assignments/BC-010-C1/handoff.md
docs/domains/runtime/assignments/BC-010-C1/validation.md
docs/domains/runtime/assignments/BC-010-C1/review.md
contracts/runtime/README.md
contracts/runtime/source_map.json
contracts/runtime/component_registry.json
contracts/runtime/route_registry.json
contracts/runtime/unresolved_register.json
tools/validate_runtime_contracts.py
tests/contracts/**
```

Verify all golden checksums before editing.

## Approved architecture decision

Record in `docs/domains/runtime/decisions.md` that:

- Auth authorizes Admin-level users and owns the user-facing authentication
  workflow.
- Auth may use the declared `auth` lane.
- OPSEC protects against unauthorized ID challenge access and unauthorized
  copying, cloning, recreation, or disclosure of Blu's protected kernel/runtime
  sources.
- OPSEC is a mandatory pre-ingress security restraint, not an ordinary
  RuntimeGate lane.
- The current CTS source preserves OPSEC interception behavior but does not
  formally declare its lane or pre-ingress restraint contract.
- Generated BC-010 contracts must preserve that source gap rather than
  pretending the successor decision already exists in the golden kernel.

This is a successor-runtime design decision, not a retroactive change to the
golden CTS source. Do not modify `kernel/golden/**`.

## Allowed collision domain

Only these paths may change:

```text
contracts/runtime/README.md
contracts/runtime/source_map.json
contracts/runtime/component_registry.json
contracts/runtime/route_registry.json
contracts/runtime/unresolved_register.json
tools/validate_runtime_contracts.py
tests/contracts/**
docs/dev/docs_index.md
docs/domains/runtime/decisions.md
docs/domains/runtime/worklog.md
docs/domains/runtime/failures.md
docs/domains/runtime/next_steps.md
docs/domains/runtime/assignments/BC-010-C1/assignment.md
docs/domains/runtime/assignments/BC-010-C1/validation.md
docs/domains/runtime/assignments/BC-010-C2/**
docs/worklogs/assignments.md
MANIFEST.sha256
```

Do not modify:

```text
kernel/golden/**
AGENTS.md
CLAUDE.md
CODEX.md
config/source_authority.json
docs/sources/**
docs/architecture/**
docs/domains/runtime/assignments/BC-010-C1/review.md
```

## C2-1 — Remove the invented OPSEC lane class

For `route.unauthenticated_clone_first_read` and
`route.unauthenticated_opsec_first_read`, replace `lane_class: opsec` with a null
lane and `lane_class_status: undeclared_in_golden_source`.

- Do not assign either route to `auth`.
- Do not add `opsec` to Exec's declared lane enum.
- Do not treat the successor decision as golden-source provenance.
- Preserve that Exec declares ingress order and terminal route behavior but not
  the lane class.
- Preserve that `SERVICE.OPSEC.001` is referenced but not defined.
- Add an unresolved item for the absent lane classification and unresolved
  route-lane versus pre-ingress-restraint relationship.

## C2-2 — Mark the OPSEC owner join as extraction inference

Both OPSEC records join ingress declarations in `03_Exec.md` to the
`SERVICE.OPSEC.001` owner in `00_Instructions.md`. Mark both records
`extraction_inference` and add a dedicated source-map join entry comparable to
`route.kernel_work_join`. Preserve both source roles and do not present the join
as a single direct declaration.

## C2-3 — Enforce lane-class closure

Every non-null route lane class must be one of Exec's declared lane classes or
an explicitly recorded route-table-only value linked to an unresolved entry. A
null lane class is permitted only with explicit unresolved status and source
provenance proving the route exists.

Tests must prove:

1. both OPSEC lane classes are null;
2. both carry the undeclared status;
3. both are extraction inferences;
4. `opsec` is rejected as undeclared;
5. an arbitrary invented lane is rejected;
6. `auth` remains valid;
7. route-table-only `workflow` remains valid;
8. a null lane without unresolved status is rejected.

## C2-4 — Finish dependency cleanup

Move prose out of ID-shaped dependency arrays for `EXECLIB.MMU.001`,
`EXECLIB.READLANE.SOURCELIB.001`, and `RuntimeGate.Egress`. Use separate
`dependencies` and `dependency_prose` fields, invent no component IDs, and
preserve source meaning.

## C2-5 — Strengthen negative-test assertions

Assert the intended validation reason for all five canonical negative fixtures
so rejection for an unrelated error fails the test. Add a synthetic unit test
for `additionalProperties: false`; do not close a canonical schema merely to
exercise that branch.

## C2-6 — Bookkeeping cleanup

- Change the BC-010-C1 assignment and validation status headers from `active`
  to `review`; do not mark them done.
- Record assignment lineage `BC-010`, `BC-010-C1`, `BC-010-C2` in contract
  metadata.
- Replace the stale phrase "Blu's current runtime is the Markdown CTS kernel"
  with terminology consistent with one GPT deployment instruction plus six
  kernel/runtime capsules.
- Do not change the golden source.

## C2-7 — Assignment records

Create this assignment quartet, leave `review.md` pending for Claude, add C2 to
the global assignment index, keep BC-010, BC-010-C1, and BC-010-C2 in `review`,
and update the runtime domain quartet. Promote these reusable lessons:

- a route name does not prove a lane-class enum value;
- cross-role owner joins must be labeled as extraction inference;
- successor architecture decisions must not be projected backward into
  golden-source extraction.

## Required validation

Run and record:

```text
git status --short
git rev-parse HEAD
git diff --check
git diff --exit-code 424f80b254a02f057da6c82db5230377076fc415 -- kernel/golden/v0.22.0
python tools/validate_runtime_contracts.py
python -m unittest discover -s tests/contracts -p "test_*.py"
```

Run all eight golden checksum checks, regenerate and verify `MANIFEST.sha256`,
confirm `"lane_class": "opsec"` is absent from the contract set, and confirm the
successor-runtime decision appears only in project decision documentation, not
as fabricated CTS source truth.

## Commit method

Commit 1 contains the correction and may use:

```text
fix(BC-010-C2): preserve undeclared OPSEC lane class
```

After it exists, record its exact SHA in the C2 handoff and global assignment
index. Commit 2 is metadata-only and may use:

```text
docs(BC-010-C2): record OPSEC repair handoff
```

The metadata commit must not modify `contracts/runtime/**`, `tools/**`,
`tests/**`, or `kernel/golden/**`.

## Completion boundary

Move BC-010-C2 to `review` only when the invented lane is gone, the golden gap
and extraction inference are explicit, lane closure and cleanup are tested,
golden sources remain unchanged, all checks pass, both commits are pushed, and
the working tree is clean. Do not merge the branch.
