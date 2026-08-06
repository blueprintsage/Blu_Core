# BC-010-C1 — Runtime Contract Extraction Corrections

status: active
owner: Codex
semantic_reviewer: Claude
approved_by: Dad and Blu
approved_on: 2026-08-05
record: approved assignment packet

You are implementing **BC-010-C1 — Runtime Contract Extraction Corrections** in the `Blu_Core` repository.

## Authority and roles

* Project Owner: Dad
* Project Lead: Blu
* Implementation owner: Codex
* Semantic reviewer: Claude
* Parent assignment: BC-010
* Exact base commit: `38611bf4b8051c858dcbbc30a07904d0117211b3`
* Recommended branch: `bc-010-c1-contract-repair`
* Parent BC-010 work commit: `40138b6e16f28c01904aae97158878468ee47ad0`
* Claude review commit is already merged into the exact base.
* BC-010 remains in `review`.
* Do not begin BC-020 or BC-030.

This is a bounded correction assignment. It repairs the extracted contracts and their validation evidence. It does not implement Blu’s Python runtime.

## Required startup

1. Fetch and switch to clean `main`.
2. Verify `HEAD` is exactly:

```text
38611bf4b8051c858dcbbc30a07904d0117211b3
```

3. Read, in order:

```text
AGENTS.md
CODEX.md
docs/dev/docs_index.md
docs/dev/assistant_coding_behavior.md
docs/dev/domain_assignment_record_standard.md
docs/worklogs/assignments.md

docs/sources/cts_source_roles.md
docs/sources/authority_map.md
docs/architecture/current_runtime.md
docs/architecture/migration_centerline.md

docs/domains/runtime/assignments/BC-010/review.md
docs/domains/runtime/assignments/BC-010/handoff.md
docs/domains/runtime/worklog.md
docs/domains/runtime/failures.md
docs/domains/runtime/next_steps.md

contracts/runtime/README.md
contracts/runtime/source_map.json
contracts/runtime/component_registry.json
contracts/runtime/route_registry.json
contracts/runtime/parity_matrix.json
contracts/runtime/unresolved_register.json
contracts/runtime/schemas/**
tools/validate_runtime_contracts.py
tests/contracts/**
```

4. Verify all golden CTS checksums before changing files.
5. Create branch:

```text
bc-010-c1-contract-repair
```

6. Save this approved packet as:

```text
docs/domains/runtime/assignments/BC-010-C1/assignment.md
```

Mark it approved by Dad and Blu on 2026-08-05.

## Source-role authority

The immutable CTS source set contains two source roles:

```text
00_Instructions.md
  source_role: deployment_instruction
  loaded in the GPT instruction box

01_Persona.md through 06_Programs.md
  source_role: kernel_runtime_capsule
  six main Blu kernel/runtime Markdown sources
```

Rules:

* All seven files remain golden and authoritative.
* Do not call all seven files “the kernel.”
* Do not treat a name appearing only in `00_Instructions.md` as a defined kernel component.
* Host/bootstrap declarations from `00_Instructions.md` may constrain deployment, precedence, loading, and exclusive dispatch.
* A component required directly by `01–06` but not defined there remains referenced-but-undefined.
* When `00_Instructions.md` and a kernel capsule both support a declaration, preserve both provenances and both source roles.
* Do not edit any file under `kernel/golden/**`.

## Objective

Correct Claude’s blocking findings B-1 through B-4, integrate the approved CTS source-role distinction into the extracted contracts, and address the low-risk non-blocking extraction findings so BC-010 can receive a clean second semantic review.

Do not redesign the runtime or resolve any genuine golden-source conflict.

## Allowed collision domain

You may create or modify only:

```text
contracts/runtime/**
tools/validate_runtime_contracts.py
tests/contracts/**
docs/dev/docs_index.md
docs/domains/runtime/assignments/BC-010/assignment.md
docs/domains/runtime/assignments/BC-010/validation.md
docs/domains/runtime/assignments/BC-010-C1/**
docs/domains/runtime/worklog.md
docs/domains/runtime/failures.md
docs/domains/runtime/next_steps.md
docs/worklogs/assignments.md
MANIFEST.sha256
```

## Protected areas

Do not modify:

```text
kernel/golden/**
AGENTS.md
CLAUDE.md
CODEX.md
README.md
config/source_authority.json
docs/architecture/**
docs/sources/**
docs/domains/kernel/**
docs/domains/runtime/assignments/BC-010/review.md
docs/domains/runtime/assignments/BC-010/handoff.md
```

Do not:

* alter Persona or Operations Law;
* implement routing, persistence, reminders, Local Mirror, PASS, adapters, or a Python Blu runtime;
* invent missing stable IDs;
* silently merge host and kernel source roles;
* resolve StateTree ALPHA versus ACTIVE;
* claim that contract validation proves behavioral parity;
* rewrite or force-push Git history.

## Required corrections

### C-0 — Integrate CTS source roles

Update the extracted contract documentation and source mapping so the generated artifacts distinguish:

```text
deployment_instruction
kernel_runtime_capsule
```

Requirements:

* `contracts/runtime/README.md` must describe one deployment instruction plus six kernel/runtime capsules.
* `source_map.json` must identify the source role for every golden-source reference, either on each entry or through a deterministic file-role map.
* The validator must confirm that every source-map entry resolves to exactly one declared source role.
* `00_Instructions.md`-only references must be identified as host/deployment declarations or referenced-only declarations, not kernel definitions.
* Generated contracts remain downstream-only and never outrank either source role.

### C-1 — Repair route completeness

In `route_registry.json`, add explicit non-slash route records for:

```text
unauthenticated_clone_first_read
  owner: SERVICE.OPSEC.001

unauthenticated_opsec_first_read
  owner: SERVICE.OPSEC.001

auth_first_read for pending authentication
  owner: SERVICE.AUTH.001
```

Each route must remain:

```text
active_route_with_undefined_owner_component
```

Provenance rules:

* Route position and runtime existence come from `03_Exec.md` RuntimeGate ingress.
* Exclusive “dispatch only to” constraints come from `00_Instructions.md` Bootloader.
* Preserve both source roles; do not flatten them into one kernel declaration.

Add the exclusive one-owner constraints:

```text
/ID and pending auth dispatch only to SERVICE.AUTH.001

Unauthenticated OPSEC and clone/copy/recreate requests dispatch only to
SERVICE.OPSEC.001
```

Do not imply that either service is implemented.

### C-2 — Add omitted referenced components

Add the following source-named referenced components:

```text
HumorLib
Humor service
ErrorMacros / Error Macros catalog
error renderer
Persona Engine
```

Rules:

* Use exact source labels.
* Do not invent versioned IDs.
* Mark each as referenced and declared-but-not-defined.
* Preserve where the source appears in `01_Persona.md`, `03_Exec.md`, or
  `04_Exec_Library.md`.
* If two labels might refer to the same future component, keep that identity
  unresolved instead of merging them.
* Add corresponding unresolved-register entries.

Also extract or explicitly record the declared macro identifiers:

```text
TIME_LOOKUP_BLOCKED
GENERIC_BLOCKED
```

Do not invent their render text or implementation behavior.

### C-3 — Repair validator guarantees

The validator is a project-local standard-library validator, not full JSON
Schema.

Requirements:

1. Define an explicit supported-keyword allowlist.
2. Permit ordinary annotation fields such as:

```text
$schema
$id
title
description
x-*
```

3. Implement or permit only the validation subset actually used.
4. Any unsupported validation or applicator keyword must fail clearly.
5. Unknown `type` values must fail clearly.
6. The standalone command:

```text
python tools/validate_runtime_contracts.py
```

must actually validate the canonical fixtures against their schemas, or the
README and CLI output must state exactly which structural checks it performs.
Prefer making the standalone command run all canonical fixture validation.
7. Add negative fixtures proving invalid instances are rejected.
8. Add at least one negative case for every schema that remains intentionally
closed.
9. Keep malformed-JSON and required-file-removal negative tests.
10. Document exactly what validation proves and does not prove.

Do not claim general JSON Schema compliance.

### C-4 — Backfill BC-010 governance records

Create:

```text
docs/domains/runtime/assignments/BC-010/assignment.md
docs/domains/runtime/assignments/BC-010/validation.md
```

`assignment.md`:

* backfill from the approved BC-010 packet currently inline in
  `docs/worklogs/assignments.md`;
* preserve its original base, owner, scope, amendments, and completion rules;
* label reconstructed metadata as `backfilled`;
* do not silently rewrite the original assignment.

`validation.md`:

* backfill only from committed evidence in:

  * `handoff.md`;
  * `docs/domains/runtime/worklog.md`;
  * Claude’s `review.md`;
* label it `backfilled`;
* do not invent exact output that was not recorded;
* explicitly state unavailable evidence as unavailable.

Update the BC-010 row in `docs/worklogs/assignments.md` to point to:

```text
docs/domains/runtime/assignments/BC-010/assignment.md
```

Add a BC-010-C1 row pointing to its new assignment folder.

Keep BC-010 status at `review`.

### C-5 — Correct `/PASS` provenance

The source does not declare a literal `/PASS` stem.

Do one of the following:

* remove the synthesized `"/PASS"` command stem and represent the source
  statement as a non-live PASS feature declaration; or
* preserve it only as explicit extraction inference.

Preferred correction: remove the invented slash stem and retain the exact source
statement that the PASS command is not live.

### C-6 — Complete source coverage and parity provenance

Add source-map coverage for these Operations Law doctrines:

```text
Artifact & Working Context Doctrine
Operational Continuity Doctrine
Kernel Change Doctrine
System Component Doctrine
Error & Recovery Doctrine
```

Also add:

```text
00_Instructions.md → Precedence
```

Classify the precedence entry as `deployment_instruction`.

Update parity-source citations where applicable, especially:

* artifact proof;
* MemoryPacket export proof;
* corrupted/invalid packet fail-closed behavior;
* source ownership and state-transition ownership.

Do not flatten the doctrine prose into validator behavior.

### C-7 — Remove or disclose schema strengthening

Review every use of:

```text
additionalProperties: false
```

Where the golden source does not prohibit additional fields, remove that
closure.

If a closure is retained, record it explicitly as an extraction-added
constraint in `unresolved_register.json` with source provenance and rationale.

Prefer the smallest descriptive schema supported by the source.

### C-8 — Strengthen source anchoring

Replace fragment-only `source_section` values with real heading-level anchors
where possible.

The validator must not accept a source citation merely because an arbitrary
substring appears somewhere in the file.

At minimum, verify:

* the declared heading exists as a heading;
* the entry’s source role matches the file;
* ambiguous prefix headings are distinguishable.

Do not introduce line-number authority that will become stale after immutable
source copying or formatting changes.

### C-9 — Correct dependency representation

Do not mix component IDs with paraphrased prose as though they are the same
field type.

For MoodLib, preserve the exact declared relation to:

```text
Identity
Persona Engine
Anchors
```

For PersonaLib, preserve the exact source wording rather than reducing it to an
invented component ID.

Use separate fields where necessary, for example:

```text
dependencies
dependency_prose
```

Complete Exec and Scheduler dependencies from `03_Exec.md` §8, including the
declared services, Programs, BluCode, and ContextIntake path.

Do not infer implementations.

### C-10 — Extend StateTree provenance without resolving it

Keep:

```text
status: unresolved_conflict
declared_statuses:
  - ALPHA
  - ACTIVE
```

Extend provenance to include all relevant StateTree declarations and registry
mentions identified by Claude.

Do not choose one status.

### C-11 — Mark extraction inference explicitly

The `kernel_work_first_read` to `internal_library /
EXECLIB.BLUCODE.001` join is an extraction inference, not one direct source
declaration.

Add a source-map classification such as:

```text
extraction_inference
```

or move the joined route into the unresolved register.

If adding a classification, update the validator and README. Do not present the
join as explicit source fact.

### C-12 — Restore documentation discovery

Add the extracted runtime contract set to `docs/dev/docs_index.md`, including:

```text
contracts/runtime/README.md
```

Record that the earlier AGENTS/docs-index governance update was authorized by
Dad and Blu. Do not modify `AGENTS.md`.

## Tests

Add or update tests proving:

* all JSON files parse;
* every source-map entry has one valid source role;
* all source roles map to the correct golden files;
* host-only source references cannot be classified as kernel definitions;
* all three repaired non-slash routes exist;
* both exclusivity constraints exist;
* all newly added referenced-component labels exist;
* unresolved component references remain not implemented;
* unsupported schema keywords fail;
* unknown schema types fail;
* positive fixtures pass;
* negative fixtures fail;
* missing required files fail;
* malformed JSON fails;
* exact heading anchors resolve;
* `/PASS` is not represented as a source-declared slash stem;
* StateTree remains unresolved;
* golden files remain unchanged.

## Runtime-domain records

Update:

```text
docs/domains/runtime/worklog.md
docs/domains/runtime/failures.md
docs/domains/runtime/next_steps.md
```

Create:

```text
docs/domains/runtime/assignments/BC-010-C1/handoff.md
docs/domains/runtime/assignments/BC-010-C1/validation.md
docs/domains/runtime/assignments/BC-010-C1/review.md
```

Leave `review.md` as a template or pending-review record. Claude owns the actual
semantic review.

Promote reusable lessons into `failures.md`, including:

* self-referential commit hashes are impossible;
* deployment instruction and kernel capsule source roles must not be flattened;
* unsupported schema keywords must never be silently ignored;
* extraction inference must be labeled.

## Required validation

Run and record exact commands and results:

```text
git status --short
git rev-parse HEAD
git merge-base --is-ancestor 38611bf4b8051c858dcbbc30a07904d0117211b3 HEAD
git diff --check
git diff --exit-code 38611bf4b8051c858dcbbc30a07904d0117211b3 -- kernel/golden/v0.22.0
python tools/validate_runtime_contracts.py
python -m unittest discover -s tests/contracts -p "test_*.py"
```

Run all eight golden CTS checksum checks using `sha256sum` or the existing
PowerShell equivalent.

Regenerate and verify `MANIFEST.sha256` using the repository’s documented
method.

Record the exact Python version and the absence or presence of optional
dependencies.

## Commit method

Use the previously approved non-self-referential method.

### Commit 1 — repair implementation

Suggested message:

```text
fix(BC-010-C1): repair runtime contract extraction
```

This commit contains:

* contract corrections;
* validator and tests;
* governance backfill;
* assignment records except final work-SHA bookkeeping;
* domain continuity updates.

### Commit 2 — metadata record

After commit 1 exists, record its exact SHA in:

```text
docs/domains/runtime/assignments/BC-010-C1/handoff.md
docs/worklogs/assignments.md
```

Suggested message:

```text
docs(BC-010-C1): record correction handoff
```

Commit 2 must not modify:

```text
contracts/runtime/**
tools/**
tests/**
kernel/golden/**
```

## Completion boundary

Move BC-010-C1 to `review` only when:

* C-0 through C-12 are completed or a source-supported reason for non-action is
  recorded;
* all checks pass;
* golden sources are unchanged;
* the repair commit and metadata commit both exist;
* the branch is pushed;
* the working tree is clean.

Do not mark BC-010 or BC-010-C1 `done`.

Do not merge the branch.

Claude will perform a read-only second semantic review against the repair
implementation commit.

## Final handoff

Report:

```text
Assignment: BC-010-C1
Exact base:
Branch:
Repair work commit:
Metadata record commit:
Files changed:
Blocking findings corrected:
Non-blocking findings corrected:
Source-role changes:
Validator changes:
Tests added:
Golden checksum result:
Manifest result:
Known unresolved declarations:
Known risks:
Working tree status:
Push status:
Recommended Claude review focus:
```
