# Blu Core Assignment Log

status: active
owner: docs/worklogs
last_reviewed: 2026-08-06
canonical_base: 7aed76e

## Rules

1. Read `AGENTS.md` before claiming work.
2. One owner per assignment and collision domain.
3. Every implementation packet names its base branch or commit.
4. One assignment per checkout; parallel work uses branches and worktrees.
5. The implementing agent runs checks and commits verified work.
6. Completion moves to `review`; Dad or Blu authorizes integration.
7. Golden kernel files are never an implementation collision domain.
8. Assignment status follows: `spec-needed` → `ready` → `active` → `review` → `done`.
9. Use `blocked` when an assignment cannot safely continue; record the reason before changing scope.

## Implementation assignments

| ID | Assignment | Owner | Status | Packet | Base | Collision domain / notes |
|---|---|---|---|---|---|---|
| BC-010 | Extract machine-readable runtime contracts from CTS | Codex | done | `docs/domains/runtime/assignments/BC-010/assignment.md` | `7aed76e` | Work commit `40138b6e16f28c01904aae97158878468ee47ad0`; closed after corrective assignments BC-010-C1 and BC-010-C2; integrated reviewed state before closure `8a37ae3c62829f16f949f5896d2bef0542721565` |
| BC-010-C1 | Runtime contract extraction corrections | Codex | done | `docs/domains/runtime/assignments/BC-010-C1/assignment.md` | `38611bf4b8051c858dcbbc30a07904d0117211b3` | Repair work commit `63c8b692403fe5ec1a9433a8313a7980fbd55437`; closed after its remaining OPSEC classification issue was corrected by BC-010-C2; integrated reviewed state before closure `8a37ae3c62829f16f949f5896d2bef0542721565` |
| BC-010-C2 | OPSEC route classification repair | Codex | done | `docs/domains/runtime/assignments/BC-010-C2/assignment.md` | `424f80b254a02f057da6c82db5230377076fc415` | Repair work commit `06292ce0e2f326ef84988e030c7fe14402192859`; closed after Claude's `approve-with-notes` review with no blockers; integrated reviewed state before closure `8a37ae3c62829f16f949f5896d2bef0542721565` |
| BC-015 | Runtime viability audit | Codex | done | `docs/domains/runtime/assignments/BC-015/assignment.md` | `4b51427b361283715a24110409e031e191b52452` | Audit work commit `9936cc4be2f7f397deebccdf7400e8b7b774df08`; review commit `4ed7626`; Claude disposition `approve-with-notes` with no blockers; integrated reviewed state before closure `1f07333457b18895fbb04d5c776e3259d870f2f6` |
| BC-016 | Historical Archive Inventory Integration | Codex | done | `docs/domains/runtime/assignments/BC-016/assignment.md` | `fdb6c7e150d3717172e08a1bc349a428187df45a` | Work commit `9f6d705723a3ee6d26e47b80c634bc3c58495c83`; metadata commit `2685dd5a3d4e81498e5b72cc83fad5d664a4d76a`; Claude review `1e7796191360cb5b81ab70a716ffda1e97f77264`; disposition `approve-with-notes` with no blockers; all NB-1 through NB-10 remain preserved and carried forward; no archives or behavioral archaeology |
| BC-020 | Define Chat and Codex capability adapter contracts |  | spec-needed |  | main after BC-010 integration | `adapters/` and adapter-domain documentation |
| BC-030 | Define Local Mirror continuity schema and lifecycle |  | spec-needed |  | main after approved prerequisites | continuity schema and continuity-domain documentation; no persistence claim |

## Design assignments

| ID | Assignment | Owner | Status | Notes |
|---|---|---|---|---|
| BC-001 | Establish bootstrap authority and golden source | Blu | done | Verified on clean `main` at `7aed76e`; live history has two commits rather than the four-commit bootstrap plan, but all protected artifacts and checksums passed |

## Completed

- BC-016 — Historical Archive Inventory Integration closed after Claude's
  `approve-with-notes` review with no blocking findings. Inventory work commit:
  `9f6d705723a3ee6d26e47b80c634bc3c58495c83`; metadata commit:
  `2685dd5a3d4e81498e5b72cc83fad5d664a4d76a`; Claude review commit:
  `1e7796191360cb5b81ab70a716ffda1e97f77264`. All non-blocking findings NB-1
  through NB-10 remain preserved and carried forward. The closure performed no
  archive import, behavioral archaeology, or runtime implementation.
- BC-015 — Runtime viability audit closed after Claude's
  `approve-with-notes` review with no blocking findings. Audit work commit:
  `9936cc4be2f7f397deebccdf7400e8b7b774df08`; review commit: `4ed7626`;
  integrated reviewed state before closure:
  `1f07333457b18895fbb04d5c776e3259d870f2f6`. The audit classified current
  viability and did not implement a runtime.
- BC-010 — Runtime contract extraction closed after corrective assignments
  BC-010-C1 and BC-010-C2; integrated reviewed state before closure:
  `8a37ae3c62829f16f949f5896d2bef0542721565`.
- BC-010-C1 — Corrections closed after BC-010-C2 repaired the remaining OPSEC
  classification issue; integrated reviewed state before closure:
  `8a37ae3c62829f16f949f5896d2bef0542721565`.
- BC-010-C2 — OPSEC route classification repair closed after Claude's
  `approve-with-notes` review with no blockers; integrated reviewed state before
  closure: `8a37ae3c62829f16f949f5896d2bef0542721565`.
- BC-001 — Blu Core bootstrap authority and CTS golden source verified at `7aed76e`.
- Governance, source authority, migration boundaries, golden CTS runtime, validation evidence, and completion records are present.
- All eight golden checksums passed.
- All repository manifest checksums passed.
- All seven extracted runtime files are byte-identical to their ZIP members.
- `git diff --check` passed.
- Working tree was clean and synchronized with `origin/main`.
- The documented four-commit bootstrap plan versus two-commit live history is a non-blocking provenance discrepancy. History was not rewritten.

## BC-010 — Golden Runtime Contract Extraction

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

## Standing guardrails

- Bootstrap checks: `git diff --check` and
  `sha256sum -c kernel/golden/v0.22.0/SHA256SUMS`.
- Do not touch `kernel/golden/`.
- Blu's current CTS deployment is one GPT deployment instruction plus six
  kernel/runtime capsules.
- No Python Blu runtime exists yet.
- Contract-validation tooling is not runtime implementation.
- Do not restore legacy `library/` SkillForge routing.
- Do not begin BC-020 or BC-030 before its packet is approved and its base is named.
