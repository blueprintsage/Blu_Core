# BC-010 — Review Record

status: review
owner: Claude
last_reviewed: 2026-08-05

## Review identity

- Assignment: BC-010 — Golden Runtime Contract Extraction
- Reviewed base: `7aed76e`
- Reviewed work commit: `40138b6e16f28c01904aae97158878468ee47ad0`
- Reviewer: Claude (semantic reviewer)
- Review type: read-only semantic review against the seven CTS v0.22.0 golden files
- Review branch: `bc-010-semantic-review`
- Integration commit or merge identity: none; Blu or Dad decides disposition

This review changed no implementation file. It did not modify
`contracts/runtime/**`, `tools/**`, `tests/**`, `kernel/golden/**`, or the
BC-010 assignment, handoff, or index records.

## Sources compared

Authoritative golden sources read in full:

```text
kernel/golden/v0.22.0/00_Instructions.md
kernel/golden/v0.22.0/01_Persona.md
kernel/golden/v0.22.0/02_Operations_Law.md
kernel/golden/v0.22.0/03_Exec.md
kernel/golden/v0.22.0/04_Exec_Library.md   (all 4071 lines, read in three passes)
kernel/golden/v0.22.0/05_Commands.md
kernel/golden/v0.22.0/06_Programs.md
```

Generated artifacts inspected in full:

```text
contracts/runtime/README.md
contracts/runtime/source_map.json
contracts/runtime/component_registry.json
contracts/runtime/route_registry.json
contracts/runtime/parity_matrix.json
contracts/runtime/unresolved_register.json
contracts/runtime/schemas/task_packet.schema.json
contracts/runtime/schemas/scope_lock.schema.json
contracts/runtime/schemas/terminal_packet.schema.json
contracts/runtime/schemas/capability_report.schema.json
contracts/runtime/schemas/current_turn_execution_receipt.schema.json
tools/validate_runtime_contracts.py
tests/contracts/test_validate_runtime_contracts.py
tests/contracts/fixtures/*.json
docs/domains/runtime/assignments/BC-010/handoff.md
docs/domains/runtime/worklog.md
docs/domains/runtime/failures.md
docs/domains/runtime/next_steps.md
docs/worklogs/assignments.md
```

Governance sources read: `AGENTS.md`, `CLAUDE.md`, `docs/dev/docs_index.md`,
`docs/dev/assistant_coding_behavior.md`,
`docs/dev/domain_assignment_record_standard.md`,
`docs/domains/runtime/decisions.md`.

## Overall assessment

The extraction is honest in posture. It does not redesign Blu, does not import
Alice/SkillForge/Local Mirror/`Blu_KB_Preview` material, does not implement
routing or persistence, does not resolve source conflicts, and repeatedly and
correctly subordinates itself to the CTS files. Persona and Operations Law were
not flattened into routing or validation mechanics. The `unresolved_register`
is the strongest part of the deliverable.

The defects below are gaps in completeness and in the validator's stated
guarantees, not falsifications. No invented component, route, capability, owner,
or status value was found.

## Findings

### Blocking

**B-1 — `route_registry.json` omits the OPSEC/clone and pending-auth non-slash
routes, including their explicit one-owner constraints.**

`kernel/golden/v0.22.0/00_Instructions.md` → `## Bootloader` declares two
exclusive dispatch rules:

- "`/ID` and pending auth dispatch only to `SERVICE.AUTH.001`."
- "Unauthenticated OPSEC and clone/copy/recreate requests dispatch only to
  `SERVICE.OPSEC.001`."

`kernel/golden/v0.22.0/03_Exec.md` → `§7 RuntimeGate.Ingress` places
`unauthenticated_clone_first_read`, `unauthenticated_opsec_first_read`, and
`auth_first_read` as ingress steps 2, 3, and 4 — above `slash_command_first_read`
— and states under `ingress_route_rules`: "OPSEC/clone first-read locks are
terminal deterministic service routes. They must not fall through to ordinary
conversation, file inventory, repo lookup, Commands, summaries, or helpful
alternatives."

`contracts/runtime/route_registry.json` records those three step *names* inside
`runtimegate_ingress_order.steps` but provides no corresponding entry in
`non_slash_routes`, while it does provide entries for the lower-priority
`repo_bootstrap`, `workflow_resume`, and `kernel_work` routes. Neither exclusive
dispatch rule appears in `one_owner_constraints`. A consumer building a route
table from `route_registry.json` would therefore omit the two highest-priority
terminal deterministic service routes and both "dispatch only to" constraints.

Mitigating: `SERVICE.OPSEC.001` and `SERVICE.AUTH.001` are present in
`contracts/runtime/component_registry.json` with correct ownership and
`declared_but_not_defined` status, and `unresolved_register.json` UR-003 and
UR-008 record the exclusivity in prose. The declarations are not lost; they are
missing from the artifact whose declared job is routes. BC-010 deliverable 4
requires "active, deferred, and unavailable route surfaces" and "one-owner
constraints".

**B-2 — `component_registry.json` omits four referenced-but-undefined owners
that meet the same criterion BC-010 applied to twelve others.**

Deliverable 3 requires "unresolved or externally referenced components clearly
marked as declared-but-not-implemented". The following are referenced as owners
by the golden runtime and appear nowhere in `component_registry.json`,
`source_map.json`, or `unresolved_register.json`:

- `HumorLib` and the `Humor service` —
  `kernel/golden/v0.22.0/01_Persona.md` → `## Humor Relation`: "trigger
  evaluation, eligibility, frequency, placement, and rendering are owned by
  HumorLib and the Humor service." Humor is also named as a suppressed
  decoration class in `03_Exec.md` → `§9 RuntimeGate.Egress` and as a
  non-satisfying route source in `§7 ingress_route_rules`.
- The `ErrorMacros` / `Error Macros` catalog and the `error renderer` —
  `03_Exec.md` → `§3 Terminal Packet Contract`: "Exec may carry `error_code` but
  must not own the ErrorMacros catalog or render catalog prose."
  `04_Exec_Library.md` → `### Error Coverage Boundary`: "the Error Macros catalog
  must be reviewed and updated in the same change pass."
  `04_Exec_Library.md` → `### Validation + Regression Model` defines
  `RAW_MACRO_LEAK` against "the error renderer or built-in fallback". The
  declared macro IDs `TIME_LOOKUP_BLOCKED` (`### Time Service`) and
  `GENERIC_BLOCKED` (`### PersonaLib`, `### MoodLib`, `### MMULib`) are likewise
  unextracted.
- `Persona Engine` — `01_Persona.md` → `## Continuity` and
  `## Anchor Precedence`; `04_Exec_Library.md` → `### PersonaLib` notes:
  "PersonaLib is the hosted-runtime bridge for Persona Engine."

These are exactly the class BC-010 handled correctly for `EXECLIB.ANTIDRIFT.001`,
`SERVICE.OPSRESTRAINT.001`, `GateKernel`, `SIMCODE_GATE`, and `MEMORY_GATE`. The
omission is inconsistent, not wrong.

**B-3 — The validator silently ignores unsupported JSON Schema keywords instead
of failing clearly, and never applies the schemas during a standalone run.**

`tools/validate_runtime_contracts.py::validate_instance` implements `$ref`,
`allOf`, `type`, `enum`, `const`, `minLength`, `uniqueItems`, `items`,
`required`, `properties`, and `additionalProperties: false`. Every other keyword
— `anyOf`, `oneOf`, `not`, `pattern`, `minimum`, `maxItems`, `dependentRequired`,
`patternProperties`, `if`/`then`, and schema-valued `additionalProperties` — is
dropped without comment. `check_type` (line 74) also returns `True` for any
unrecognized `type` value. A future schema edit using an unsupported keyword
would pass validation while asserting nothing.

Separately, `validate_contracts()` never calls `validate_instance()`. Running
`python tools/validate_runtime_contracts.py` performs file-presence, JSON-parse,
source-map, uniqueness, stem-ownership, dialect, `$id`, and `$ref`-resolution
checks only. No contract or fixture is checked against any schema. Only
`tests/contracts/test_validate_runtime_contracts.py::test_schema_fixtures`
exercises `validate_instance`, and only with positive fixtures — there is no
negative case proving an invalid packet is rejected.

`contracts/runtime/README.md` states the validator "resolves local schema
references, and validates the contract fixtures used by the tests", which reads
as a stronger guarantee than the standalone tool provides.

**B-4 — The BC-010 assignment record is missing `assignment.md` and
`validation.md`.**

`docs/domains/runtime/assignments/BC-010/` contains only `handoff.md`.
`docs/dev/domain_assignment_record_standard.md` → "Canonical location" and
"File ownership" require `assignment.md` (the approved packet) and
`validation.md` (exact commands, outputs, limitations). `AGENTS.md` →
"Branch and assignment rules" requires every index row to point to
`docs/domains/<domain>/assignments/<assignment-id>/assignment.md`; the BC-010
row in `docs/worklogs/assignments.md` instead reads "Inline below".

This is a governance/backfill gap, not a Codex extraction defect: the packet is
owned by Blu or Dad. It is blocking for this review because the review was
required to assess `validation.md`, and that file does not exist. The validation
evidence that does exist (`handoff.md` "Validation commands and results",
`docs/domains/runtime/worklog.md`) is adequate in substance but is not in the
required location or format.

### Non-blocking

**N-1 — `/PASS` is a synthesized stem attributed to a section that does not
contain it.** `contracts/runtime/route_registry.json` →
`unavailable_command_surfaces` lists `"/PASS"` with
`source_map_id: "commands.not_live"`.
`kernel/golden/v0.22.0/05_Commands.md` → `## §3 — Commands Not Live in This
Build` does not mention PASS. The supporting text is
`05_Commands.md` → `## PASS Removal Note` ("The PASS command is not live in this
build"), which never writes a leading-slash form and is not represented in
`source_map.json`. The behavioral claim is correct; the stem string and the
provenance citation are extraction inference presented as source-backed.

**N-2 — Five Operations Law doctrines are absent from `source_map.json` and
uncited by the parity matrix.** Missing:
`02_Operations_Law.md` → `Artifact & Working Context Doctrine`,
`Operational Continuity Doctrine`, `Kernel Change Doctrine`,
`System Component Doctrine`, and `Error & Recovery Doctrine`.

Two carry load-bearing declarations:

- `System Component Doctrine` assigns ownership explicitly — "ContextIntake owns
  artifact/source intake chains. MMU owns memory organization semantics.
  StateTree validates state transitions. Time Service owns supported current-turn
  time lookup." — and is the only Operations-level ownership statement for those
  components. `contracts/runtime/component_registry.json` sources them only from
  `04_Exec_Library.md`.
- `Artifact & Working Context Doctrine` states "MemoryPacket export is artifact
  delivery; export completion may be claimed only when a real artifact exists in
  the same turn", which is the Operations-level basis for
  `contracts/runtime/parity_matrix.json` PARITY-007-B; PARITY-007 cites
  `execlib.artifact_proof` and `programs.universal` but not this doctrine.
- `Error & Recovery Doctrine` states "Corrupted or invalid packets fail closed",
  which PARITY-006 does not cite.

No requirement is stated incorrectly; the provenance is thinner than the source
supports.

**N-3 — `00_Instructions.md` → `## Precedence` is not extracted anywhere.** The
declaration "Safety > Operations(Law) > Identity(Core) > User request >
Skills/Repo" is a deterministic global precedence chain distinct from the
`centerline_order` captured through `operations.coherence_guard`. It appears in
no contract file and in no unresolved item. No BC-010 deliverable names it
explicitly, so this is recorded as an omission rather than a deliverable failure.

**N-4 — Schema closure is tighter than the source declares.**
`contracts/runtime/schemas/terminal_packet.schema.json` and
`scope_lock.schema.json` both set `additionalProperties: false`.
`03_Exec.md` → `§3 Terminal Packet Contract` declares `required_fields` and
`optional_fields` but never forbids additional fields, and `§4` lists
`scope_lock_fields` without declaring all eight mandatory on every packet.
Component contracts elsewhere in `04_Exec_Library.md` return packets carrying
extra fields (for example `EXECLIB.STATETREE.001` returns `terminal` and
`blocked_fields[]`). Closing both schemas is a defensible reading of a file that
calls itself a "FLAT CONTRACT", but it is an extraction-added strengthening and
is not recorded in `unresolved_register.json`.

**N-5 — Several `source_section` values are line fragments, and the validator
matches them by substring.** `contracts/runtime/source_map.json` uses
`"CAPABILITY_OVERRUN"` (`schema.capability_report`),
`"active_task: one-line statement"` (`schema.task_packet`),
`"required_fields:"` (`schema.terminal_packet`), and
`"Every scheduled service, library, or Program call must return a same-turn
terminal packet/proposal"` (`schema.current_turn_execution_receipt`) as section
identifiers. `tools/validate_runtime_contracts.py` line 168 checks
`section not in target.read_text(...)`, a plain substring test, so a fragment
that appears anywhere in the file passes. `"### Active Component Registry"`
(`execlib.active_registry`) is also a proper prefix of the distinct heading
`"### Active Component Registry Stabilization"`, so that entry cannot be
distinguished from its neighbour by this check.

**N-6 — Two declared dependency values paraphrase away source content.**
`contracts/runtime/component_registry.json` gives `EXECLIB.MOODLIB.001` the
dependency `"Persona-shaped state"`. `04_Exec_Library.md` → `### MoodLib` has no
`depends_on` block; its rule reads "MoodLib is downstream of Identity, Persona
Engine, and Anchors." Identity and Anchors are dropped.
`EXECLIB.PERSONALIB.001` is given `"Persona source"`, which is not a declared
ID. Both are prose strings in fields that otherwise hold component IDs.

**N-7 — The `Exec` component's dependency list is incomplete relative to Exec
§8.** `component_registry.json` lists `EXECLIB.ANTIDRIFT.001`,
`SERVICE.OPSRESTRAINT.001`, and `COMMANDS`. `03_Exec.md` → `§8 Exec.Scheduler`
additionally requires Scheduler calls to `SERVICE.AUTH.001`,
`SERVICE.ECHOTRACE.001`, `SERVICE.REPOBOOT.001`, `PROGRAM.SIMCODE.001`,
`PROGRAM.MEMORY.001`, and `EXECLIB.BLUCODE.001`, and `§7` permits scheduling
`SERVICE.CONTEXTINTAKE.001`.

**N-8 — UR-012's count of StateTree declarations is narrower than the source.**
`unresolved_register.json` UR-012 says StateTree "is declared in four component
blocks". That is correct for `lib_id`-bearing blocks. `04_Exec_Library.md` also
declares `StateTree ... status: ACTIVE` in `### Active Component Registry
Stabilization` and `### Active Component Registry`, and `05_Commands.md` §5.2
lists StateTree as a live `/echotrace` target. The status conflict is preserved
correctly; only the provenance list is short.

**N-9 — `route.kernel_work` binds an ingress step to a lane and owner that the
source never joins directly.** `contracts/runtime/route_registry.json`
`non_slash_routes[route.kernel_work]` maps `kernel_work_first_read` to
`lane_class: internal_library` / `owner: EXECLIB.BLUCODE.001`. `03_Exec.md` →
`§7` names the step; `§8` separately states "Scheduler must call
`EXECLIB.BLUCODE.001` when Ingress locks internal_library/EXECLIB.BLUCODE.001."
The join is a reasonable inference but is not an explicit declaration, and
`source_map.json`'s three permitted classification values offer no way to mark
it as inference. The entry's `status` field
(`active_route_with_undefined_owner_component`) partially signals the
uncertainty.

**N-10 — Integration-state observation outside the reviewed commit.** Commit
`f743ee8` ("BC-010 update"), which is the current branch tip and is *not* the
reviewed work commit, removed the `## Extracted runtime contracts` section that
the work commit added to `docs/dev/docs_index.md`, and modified `AGENTS.md`.
`AGENTS.md` is named in BC-010's prohibited-areas list. At the reviewed work
commit `40138b6` the docs-index entry is present and `AGENTS.md` is untouched,
so this is not a BC-010 implementation defect — but the checkout no longer
indexes the contract set, and Blu or Dad should confirm `f743ee8` was
authorized. Reported factually; not adjudicated here.

### Preserved unresolved declarations

The following were correctly left unresolved and must not be treated as defects:

- **`EXECLIB.STATETREE.001` ALPHA vs ACTIVE** (UR-012). `04_Exec_Library.md`
  `### StateTree Library` declares `status: ALPHA`; `### StateTree Explicit
  Validation Packet`, `### StateTree Tag Validation`, and `### StateTree
  MemoryPacket Import Validation` each declare `status: ACTIVE`, with differing
  versions and field sets. `component_registry.json` records
  `"status": "unresolved_conflict"`, `"declared_statuses": ["ALPHA", "ACTIVE"]`,
  and all four source sections. No status was chosen. Correct.
- **`workflow` lane class** (UR-011). `03_Exec.md` `§7 lane_classes` omits
  `workflow`; `05_Commands.md` `§4` assigns `lane_class = workflow` to `/memory`
  and `03_Exec.md` `§8` schedules `PROGRAM.MEMORY.001` for that lock.
  `route_registry.json` keeps the route value and flags
  `route_table_only_value: "workflow"`, and `terminal_packet.schema.json` leaves
  `lane_class` an open string rather than closing the enum against the source.
  Correct on both counts.
- **Mandatory owners referenced by Exec with no component definition** (UR-001,
  UR-002, UR-003, UR-004, UR-006, UR-007, UR-008, UR-009, UR-020):
  `EXECLIB.ANTIDRIFT.001`, `SERVICE.OPSRESTRAINT.001`, `SERVICE.AUTH.001`,
  `SERVICE.REPOBOOT.001`, `EXECLIB.BLUCODE.001`, `SYSTEM.RUNTIME.001`,
  `SERVICE.OPSEC.001`, `SIMCODE_GATE`, `MEMORY_GATE`, `GateKernel`. All carry
  `definition_status: declared_but_not_defined`. None was invented into
  existence. Correct.
- **`SERVICE.ECHOTRACE.001` vs `EXEC.SPINE_TRACE`** (UR-005). The division of
  responsibility between the defined public owner and the undefined support
  service is left open rather than merged. Correct.
- **`/mood` route vs active MoodLib** (UR-010). `05_Commands.md` `§3` lists
  `/mood` as not live while `04_Exec_Library.md` `### MoodLib` is `ACTIVE` and
  describes a `/mood show` force path and mode semantics. No `/mood` route was
  created and MoodLib was not downgraded. Correct.
- **Empty Program compatibility headings** (UR-016). `06_Programs.md` `§1`
  contains bare `Compatibility phase owners:` and `Compatibility rule:` headings
  with no values; no owners were inferred. Correct.
- **`PROGRAM.MEMORY.001` incomplete universal contract** (UR-021).
  `06_Programs.md` `§3` requires declared inputs, outputs, and terminal result
  states; `§5` supplies none, while `§4` supplies them for SimCode.
  `component_registry.json` leaves `"inputs": null, "outputs": null` rather than
  synthesizing them from prose. Correct.
- **Task-packet and capability-report schemas** (UR-013, UR-014). Neither
  structure is named in the golden runtime. Both schemas assert object shape
  only, carry `x-blu-contract-status: underspecified`, and state in their own
  `description` that they must not be read as completed designs. Correct.
- **Current-turn execution receipt** (UR-015). No separate receipt structure is
  declared, so the schema is an explicit `allOf` alias of the terminal packet
  adding no fields, with `x-blu-contract-status: extraction_alias`. Correct.
- **Alias-registry incompleteness** (UR-022). `03_Exec.md` `§10
  alias_registry_contract` requires every ACTIVE Library, Service, and Program to
  declare exactly one stable alias, while most `04_Exec_Library.md` blocks
  declare `name:` only and the active trace registry lists five aliases. No
  aliases were synthesized from names. Correct.
- **PEL and Identity_Lore** (UR-018). Declared by `01_Persona.md` as continuity
  source inputs but outside the seven authoritative files; recorded as external
  and not imported. Correct.
- **Host capability** (UR-019). Live time, persistence, artifact creation, and
  background execution are held conditional, consistent with `03_Exec.md`
  `hosted_runtime_boundary` and `00_Instructions.md` `## No Runtime Theater`.
  Correct.

### Boundary checks that passed

- **Persona was not flattened.** `component_registry.json` records Persona as
  `kind: model_facing_source` / `definition_status:
  defined_in_golden_model_facing`, with ownership copied from `01_Persona.md`
  `## Authority Boundary`. Its `inputs`/`outputs` match `## Core Loop` steps 1–3
  and `## Output Contract` and add nothing. No ribbon palette, mood word list,
  anchor library, swatch mapping, or touchstone set was converted into a runtime
  enum or routing field. PARITY-009 restates the non-routing boundary correctly.
- **Operations Law was not weakened into schema fields.** Doctrines are
  referenced as model-facing sources; `Execution Discipline Doctrine` is
  explicitly classified `intentionally unmodeled prose`. No doctrine text was
  reduced to a validator rule.
- **Contracts are not presented as equal or superior to the CTS source.**
  `contracts/runtime/README.md` states "The seven golden Markdown files remain
  authoritative. If a contract here differs from a golden source, the golden
  source wins," and `component_registry.json` carries a `boundary` field denying
  that registry presence proves implementation or host capability.
- **Markdown declaration is not treated as host-capability proof.** UR-019 and
  the `defined_in_golden_host_capability_conditional` /
  `defined_in_golden_host_tool_conditional` statuses hold this line.
- **Active / deferred / unavailable command classification matches the source.**
  All 19 live forms in `05_Commands.md` `§2` are present in
  `active_command_forms`; the five deferred `/memory` forms match `§3` and
  `06_Programs.md` `§5 Deferred commands`; `/mood`, `/verbosity`, `/remind`,
  `/cpm`, `/DevMode` match `§3`. (See N-1 for `/PASS`.)
- **ScopeLock and terminal-packet fields are unaltered.**
  `scope_lock.schema.json` reproduces all eight `scope_lock_fields`, the eight
  `requested_deliverable` values, and the eight `prohibited_moves` values from
  `03_Exec.md` `§4` verbatim. `terminal_packet.schema.json` reproduces all
  eleven `required_fields`, the `error_code` optional field, and the
  `terminal_state`, `validation_result`, and `scope_validation` value sets from
  `§3` verbatim. (See N-4 for the added closure.)
- **One-owner and fail-closed rules are not weakened.**
  `route_registry.json` `one_owner_constraints` and PARITY-003 preserve one lane
  / one owner / one packet; PARITY-006 preserves fail-closed behaviour including
  the exact authorized line "Runtime blocked: terminal packet invalid." from
  `03_Exec.md` `§11`. (See B-1 for the two missing exclusivity rules.)
- **Artifact proof requirements are present.** PARITY-007 covers `artifact_output`
  requirement, `/memory export` payload proof, and the `PROPOSED_PATH` /
  `BODY_EMITTED` / `FILE_EMITTED` / `COMPLETE_SCOPE` ladder from
  `04_Exec_Library.md` `### Artifact Proof Boundary`.
- **Hosted single-turn limits are not obscured.** PARITY-012 and UR-019 preserve
  "No daemon, background task, self-wake, hidden continuation, or unproven
  persistence exists" from `03_Exec.md` `hosted_runtime_boundary`.
- **No behavior implementation was added.** `tools/validate_runtime_contracts.py`
  declares itself "contract-validation tooling, not Blu runtime implementation"
  in its module docstring and imports only `argparse`, `json`, `sys`,
  `pathlib`, and `typing`. It contains no routing, gate, packet-construction, or
  persistence logic.

## Validation review

### Commands run by this review

```text
git status --short                                        -> clean
git rev-parse HEAD                                        -> f743ee8bec1f809f66e5b63f04c3441beddaf4f3
git show -s --format=%H 40138b6e16f28c01904aae97158878468ee47ad0
                                                          -> 40138b6e16f28c01904aae97158878468ee47ad0 (commit present)
git diff --check                                          -> exit 0, no output
PowerShell Get-FileHash -Algorithm SHA256 vs kernel/golden/v0.22.0/SHA256SUMS
                                                          -> 8/8 OK
git diff --exit-code 40138b6 -- contracts/runtime tools tests kernel/golden
                                                          -> exit 0 (no drift in reviewed artifacts)
python tools/validate_runtime_contracts.py                -> "PASS: runtime contracts are structurally valid", exit 0
python -m unittest discover -s tests/contracts -p "test_*.py"
                                                          -> Ran 4 tests, OK, exit 0
```

`sha256sum` is unavailable on this Windows host, matching the limitation Codex
recorded in `docs/domains/runtime/failures.md`. The PowerShell SHA-256
comparison is the assignment-authorized equivalent and was run against all eight
`SHA256SUMS` entries — the seven Markdown files and the source ZIP. All passed.

### Handoff claims verified

Every count in `handoff.md` was recomputed from the JSON and is accurate:

| Claim | Verified |
|---|---|
| 41 registry components | 41 (library 15, referenced_component 12, runtime_owner 8, command_owner 2, program 2, service 2) |
| 6 live slash stems | 6, one owner each |
| 69 source-map entries | 69 (explicit 61, unmodeled prose 4, unresolved conflict 4) |
| 22 unresolved items | 22 (UR-001 … UR-022) |
| 12 parity requirements | 12 |
| 34 parity cases | 34 |
| No `kernel/golden/**` change | confirmed |
| 23 files in the work commit | confirmed |

### Validation-evidence assessment

Adequate for what it claims, but narrower than the README implies.

What the evidence supports:

- every contract JSON parses;
- required contract and schema files are present;
- source-map IDs are unique, classifications are from the declared set, and each
  `source_file` exists and contains the `source_section` string;
- every `source_map_id` / `source_map_ids` / `x-source-map-id` reference across
  the contract set resolves to a source-map entry;
- component IDs are unique within namespace;
- each live slash stem has exactly one owner and no duplicate rows;
- schema dialect and `$id` uniqueness hold, and local `$ref` targets exist;
- the validator fails on a missing required contract and on malformed JSON —
  both proven by `test_required_contract_missing_fails` and
  `test_malformed_json_fails`;
- the five positive fixtures satisfy their schemas under
  `validate_instance`.

What the evidence does **not** support, and is not claimed as behavioral parity
anywhere in the deliverable:

- no negative schema fixture exists, so schema *rejection* is unproven;
- the standalone validator run applies no schema to any instance (B-3);
- unsupported schema keywords are silently ignored (B-3);
- `source_section` verification is substring-based (N-5).

The implementation does **not** claim full JSON Schema compliance, and
`handoff.md` "Known risks" states plainly that "Structural/schema validity does
not prove behavioral parity" and "Registry presence does not prove executable
implementation or host support." That framing is correct and matches
`00_Instructions.md` `## No Runtime Theater`. The validator is correctly
identified as development tooling rather than Blu runtime code, in its module
docstring, in `contracts/runtime/README.md`, and in the assignment packet.

The single overstatement is the `contracts/runtime/README.md` sentence "The
validator ... resolves local schema references, and validates the contract
fixtures used by the tests", which attributes fixture validation to the
standalone tool.

## Disposition

**return-for-correction**

The extraction's semantics are sound and no source meaning was falsified,
inverted, or silently resolved. The disposition is driven by four completeness
and guarantee gaps (B-1 … B-4), each of which maps to an explicit BC-010
deliverable requirement or to the record standard. None requires re-doing the
extraction; all are additive.

If Blu or Dad judges B-1 through B-3 to be acceptable scope for a follow-up
assignment and B-4 to be a governance action rather than a BC-010 correction,
`approve-with-notes` is a defensible alternative disposition. That call is not
mine to make.

## Required follow-up

Correction work (same assignment folder unless Blu or Dad opens a new one):

1. **B-1** — Add `non_slash_routes` entries to
   `contracts/runtime/route_registry.json` for `unauthenticated_clone_first_read`
   and `unauthenticated_opsec_first_read` (owner `SERVICE.OPSEC.001`) and for
   `auth_first_read` pending auth (owner `SERVICE.AUTH.001`), each marked
   `active_route_with_undefined_owner_component`. Add both "dispatch only to"
   rules from `00_Instructions.md` `## Bootloader` to `one_owner_constraints`.
   Add a source-map entry for `00_Instructions.md` `## Bootloader` if the
   existing `instructions.bootloader` entry is not reused.
2. **B-2** — Add `HumorLib`, the `Humor service`, the `ErrorMacros` catalog and
   error renderer, and `Persona Engine` to `component_registry.json` as
   `referenced_component` / `declared_but_not_defined`, with matching
   `unresolved_register.json` items. Record the declared blocked-macro IDs
   (`TIME_LOOKUP_BLOCKED`, `GENERIC_BLOCKED`) or record explicitly why they are
   not extracted.
3. **B-3** — Make `validate_instance` collect and report unrecognized schema
   keywords as errors, make `check_type` reject unknown `type` values, and
   either apply the schemas to the fixtures inside `validate_contracts()` or
   correct the `contracts/runtime/README.md` sentence to say the standalone run
   performs structural checks only. Add at least one negative fixture per closed
   schema. State the limited-subset boundary in `contracts/runtime/README.md`,
   not only in `docs/domains/runtime/failures.md` and the module docstring.
4. **B-4** — Blu or Dad: create
   `docs/domains/runtime/assignments/BC-010/assignment.md` from the packet
   currently inline in `docs/worklogs/assignments.md`, create
   `docs/domains/runtime/assignments/BC-010/validation.md` from the evidence in
   `handoff.md` and `docs/domains/runtime/worklog.md` (marked `backfilled`, with
   no invented output), and repoint the BC-010 index row from "Inline below" to
   the packet path per `AGENTS.md`.

Recommended but optional (non-blocking):

5. N-1 — Correct the `/PASS` provenance or drop the synthesized stem.
6. N-2, N-3 — Extend `source_map.json` to the five missing Operations Law
   doctrines and `00_Instructions.md` `## Precedence`, and add the corresponding
   citations to PARITY-006 and PARITY-007.
7. N-4 — Record the `additionalProperties: false` strengthening in
   `unresolved_register.json`, or relax it.
8. N-5 — Anchor `source_section` values to real headings and tighten the
   validator's section check beyond substring matching.
9. N-6, N-7, N-8 — Normalize dependency values to declared IDs, complete Exec's
   dependency list against `03_Exec.md` `§8`, and extend UR-012's provenance.
10. N-10 — Blu or Dad: confirm whether `f743ee8` was authorized to modify
    `AGENTS.md` and to remove the `## Extracted runtime contracts` section from
    `docs/dev/docs_index.md`.

Decisions reserved to Blu or Dad, per
`docs/domains/runtime/next_steps.md`: every item in
`contracts/runtime/unresolved_register.json`. This review does not resolve any of
them and recommends that BC-020 and BC-030 stay unstarted until their packets are
approved and bases named.

## Final status authorization

- Authorized by: pending — Blu or Dad
- Assignment status: unchanged at `review`; this reviewer does not set `done`
- Date: 2026-08-05
