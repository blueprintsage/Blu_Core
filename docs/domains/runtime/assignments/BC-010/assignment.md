# BC-010 — Golden Runtime Contract Extraction

status: review
owner: Codex
semantic_reviewer: Claude
record_status: backfilled
backfilled_on: 2026-08-05
source_record: docs/worklogs/assignments.md inline approved packet

> This task-specific record was backfilled from the approved inline packet.
> Original base, owner, scope, amendment, completion rules, and receipt text are
> preserved below without rewriting the original assignment history.

### Assignment identity

- **Implementation owner:** Codex
- **Semantic reviewer:** Claude
- **Project Lead / integration reviewer:** Blu
- **Project Owner / final authority:** Dad
- **Exact base commit:** `7aed76e`
- **Starting branch:** clean `main` at `7aed76e`
- **Recommended work branch:** `bc-010-runtime-contracts`
- **Status at handoff:** `ready`

### Amendment — commit identity bookkeeping

- **Approved by:** Dad, by explicit instruction on 2026-08-05.
- **Defective original requirement:** BC-010 required one implementation commit
  while also requiring that commit's exact SHA to be recorded inside a tracked
  file in the same commit.
- **Why defective:** A Git commit cannot contain its own final hash. Changing
  the recorded hash changes the tree and therefore produces a different commit
  hash.
- **Authorized method:** Create one reviewable implementation commit, capture
  its exact SHA, then create one metadata-only commit that records the work SHA
  in the assignment handoff and this index.
- **Review target:** Claude's semantic review targets the implementation commit,
  not the metadata-only record commit.
- **Metadata boundary:** The record commit must not modify
  `contracts/runtime/**`, `tools/**`, `tests/**`, or `kernel/golden/**`.

### Objective

Extract the current CTS Markdown runtime into machine-readable contracts without
changing, replacing, normalizing, or reinterpreting the golden runtime.

BC-010 documents what Blu v0.22.0 currently declares. It does not implement the
future Python runtime and does not change current behavior.

### Required source order

Before changing files:

1. Read `AGENTS.md`.
2. Read `CODEX.md`.
3. Read `docs/dev/docs_index.md`.
4. Read `docs/dev/assistant_coding_behavior.md`.
5. Read this assignment.
6. Read:
   - `docs/architecture/current_runtime.md`
   - `docs/architecture/migration_centerline.md`
   - `docs/sources/authority_map.md`
   - `docs/domains/runtime/decisions.md`
   - `docs/domains/runtime/worklog.md`
   - `docs/domains/runtime/failures.md`
   - `docs/domains/runtime/next_steps.md`
7. Verify that `HEAD` descends from exact base `7aed76e`.
8. Verify the golden checksums before extraction.

### Authoritative inputs

Only the following files define the extraction source:

```text
kernel/golden/v0.22.0/00_Instructions.md
kernel/golden/v0.22.0/01_Persona.md
kernel/golden/v0.22.0/02_Operations_Law.md
kernel/golden/v0.22.0/03_Exec.md
kernel/golden/v0.22.0/04_Exec_Library.md
kernel/golden/v0.22.0/05_Commands.md
kernel/golden/v0.22.0/06_Programs.md
```

Project governance and architecture documents may constrain the extraction but
must not be used to invent runtime declarations absent from the golden files.

### Allowed collision domain

BC-010 may create or modify only:

```text
contracts/runtime/**
tools/validate_runtime_contracts.py
tests/contracts/**
docs/domains/runtime/worklog.md
docs/domains/runtime/failures.md
docs/domains/runtime/next_steps.md
docs/worklogs/assignments.md
docs/dev/docs_index.md
```

`tools/validate_runtime_contracts.py`, if created, is contract-validation tooling.
It is not Blu runtime implementation.

Any additional file requires assignment amendment by Blu or Dad before editing.

### Protected and prohibited areas

Do not modify:

```text
kernel/golden/**
AGENTS.md
CLAUDE.md
CODEX.md
config/source_authority.json
docs/architecture/**
docs/sources/**
```

Do not:

- rewrite Persona or Operations Law;
- infer missing components into existence;
- merge duplicate or conflicting declarations silently;
- normalize source wording into a different behavioral rule;
- import Alice, SkillForge, Local Mirror, or `Blu_KB_Preview` content into the CTS contracts;
- implement routing, reminders, memory persistence, Local Mirror, PASS, or adapters;
- claim behavioral parity from schema validity alone;
- edit Git history or force-push.

### Required deliverables

Create a documented contract set under `contracts/runtime/` containing at least:

1. `README.md`
   - purpose and non-authority boundary;
   - golden source list;
   - extraction rules;
   - explanation that contracts describe the current Markdown runtime.

2. `source_map.json`
   - each extracted object mapped to its golden file and source section;
   - classification as explicit declaration, unresolved conflict, or intentionally unmodeled prose;
   - no invented source claims.

3. `component_registry.json`
   - declared component, service, library, Program, command owner, and runtime owner IDs;
   - status and ownership;
   - dependencies;
   - declared inputs and outputs when present;
   - source provenance;
   - unresolved or externally referenced components clearly marked as declared-but-not-implemented.

4. `route_registry.json`
   - mandatory restraint order;
   - RuntimeGate ingress order;
   - live slash-command routes;
   - ordinary-conversation fallback lane as declared by the golden runtime;
   - active, deferred, and unavailable route surfaces;
   - one-owner constraints.

5. JSON Schemas under `contracts/runtime/schemas/` for:
   - task packet;
   - ScopeLock;
   - terminal packet;
   - capability report;
   - current-turn execution receipt.

6. `parity_matrix.json`
   - behavioral requirements and test cases for:
     - ordinary conversation;
     - command routing;
     - one-owner enforcement;
     - restraint ordering;
     - ScopeLock containment;
     - fail-closed behavior;
     - artifact proof;
     - source and capability honesty;
     - Persona non-routing boundary;
     - Operations truth and anti-drift boundary;
     - active versus deferred commands;
     - hosted single-turn limitations.

7. `unresolved_register.json`
   - conflicts, underspecified fields, referenced-but-unimplemented owners, and
     declarations that cannot be converted deterministically without a later
     design decision;
   - each item must preserve source provenance and must not resolve itself.

8. Contract validation:
   - every JSON file parses;
   - registry IDs are unique within their declared namespace;
   - command stems have no duplicate public owner;
   - all source-map targets exist;
   - required schema files exist;
   - validator fails when a required contract file is missing or malformed.

9. Runtime-domain continuity updates:
   - work performed and files changed in `worklog.md`;
   - failed or unsafe extraction paths in `failures.md`;
   - the next safe step in `next_steps.md`.

### Extraction rules

- Preserve CTS terminology where it is structurally usable.
- Separate explicit source declaration from extraction inference.
- When declarations conflict, preserve the conflict in `unresolved_register.json`.
- When prose is expressive or semantic rather than deterministic, leave it
  model-facing and record why it was not reduced to a runtime field.
- Persona and Operations remain authoritative model-facing sources.
- Contract files are downstream representations and never outrank the CTS files.
- A missing implementation is recorded as missing; it is not created by registry entry.
- Do not treat a Markdown declaration as proof that a host capability exists.
- Keep the smallest schema that accurately represents the declared contract.

### Required checks

Run and record exact results for:

```text
git status --short
git rev-parse HEAD
git merge-base --is-ancestor 7aed76e HEAD
git diff --check
sha256sum -c kernel/golden/v0.22.0/SHA256SUMS
git diff --exit-code 7aed76e -- kernel/golden/v0.22.0
```

Also run the contract validator and JSON parse/schema checks introduced by the
assignment.

On Windows, an equivalent checksum command is acceptable, but the exact command
and output must be recorded.

### Completion conditions

Move BC-010 from `active` to `review` only when:

- all required deliverables exist;
- protected golden files remain byte-identical;
- all validation checks pass;
- runtime-domain logs are updated;
- the work is committed as one reviewable, revertible commit;
- the exact commit ID is recorded in this file;
- no behavior implementation was added.

### Implementation receipt

- **Work commit:** `40138b6e16f28c01904aae97158878468ee47ad0`
- **Review status:** `review`
- **Semantic review target:** `40138b6e16f28c01904aae97158878468ee47ad0`
- **Handoff:** `docs/domains/runtime/assignments/BC-010/handoff.md`
- **Record method:** authorized metadata-only follow-up commit under the
  amendment above
- **Push status:** not pushed

### Handoff format

Codex must report:

```text
Assignment: BC-010
Base commit:
Work commit:
Files changed:
Contracts created:
Validation commands:
Validation results:
Golden checksum result:
Known unresolved items:
Known risks:
Recommended semantic-review focus:
Working tree status:
Push status:
```

Claude then performs a read-only semantic review against the golden CTS source.
Claude does not modify the BC-010 implementation branch unless Blu or Dad issues
a separate correction assignment.
