# BC-010-C1 — Review Record

status: review
owner: Claude
last_reviewed: 2026-08-06

## Review identity

- Assignment: BC-010-C1 — Runtime Contract Extraction Corrections
- Parent assignment: BC-010
- Base before repair: `38611bf4b8051c858dcbbc30a07904d0117211b3`
- Reviewed repair work commit: `63c8b692403fe5ec1a9433a8313a7980fbd55437`
- Metadata record commit / review-branch base: `2d7198c653af0f9d78277822064920def77b78cb`
- Review branch: `bc-010-c1-semantic-review`
- Reviewer: Claude
- Review type: read-only second semantic review against the CTS source set
- Integration commit or merge identity: none; Blu and Dad own final disposition

This review changed no implementation file. It did not modify contracts,
validator code, tests, golden sources, assignment packets, handoff records,
validation records, the global assignment index, or Git history.

The metadata record commit was verified not to touch the implementation
surface. `git diff --exit-code 63c8b69 2d7198c -- contracts/runtime tools tests
kernel/golden` returned exit 0; that commit changed only `MANIFEST.sha256`,
`docs/domains/runtime/assignments/BC-010-C1/handoff.md`, and
`docs/worklogs/assignments.md`.

## Golden sources compared

All seven CTS files were read in full and used as the authoritative comparison.
Source roles were honored per `docs/sources/cts_source_roles.md`.

Deployment instruction (`deployment_instruction`):

```text
kernel/golden/v0.22.0/00_Instructions.md
```

Kernel/runtime capsules (`kernel_runtime_capsule`):

```text
kernel/golden/v0.22.0/01_Persona.md
kernel/golden/v0.22.0/02_Operations_Law.md
kernel/golden/v0.22.0/03_Exec.md
kernel/golden/v0.22.0/04_Exec_Library.md
kernel/golden/v0.22.0/05_Commands.md
kernel/golden/v0.22.0/06_Programs.md
```

Generated artifacts inspected in full at the repair work commit:
`contracts/runtime/README.md`, `source_map.json`, `component_registry.json`,
`route_registry.json`, `parity_matrix.json`, `unresolved_register.json`, all
five files under `contracts/runtime/schemas/`,
`tools/validate_runtime_contracts.py`,
`tests/contracts/test_validate_runtime_contracts.py`, and all ten fixtures
under `tests/contracts/fixtures/`.

Governance and record sources read: `AGENTS.md`, `CLAUDE.md`,
`docs/dev/docs_index.md`, `docs/dev/assistant_coding_behavior.md`,
`docs/dev/domain_assignment_record_standard.md`, `docs/worklogs/assignments.md`,
`docs/sources/cts_source_roles.md`, `docs/sources/authority_map.md`,
`docs/architecture/current_runtime.md`,
`docs/architecture/migration_centerline.md`, the BC-010 and BC-010-C1
assignment quartets, and the runtime domain quartet.

## Overall assessment

This is a substantial and largely faithful repair. All four original blocking
findings are corrected, the deployment-instruction versus kernel-capsule source
role separation is implemented in both data and enforcement, the validator's
guarantees now match its documentation, and nothing was invented to fill a
source gap in the component registry, the macro identifiers, the PASS
provenance, or the StateTree conflict.

One new defect was introduced by the repair itself, in the same artifact it was
repairing. It is narrow and surgically fixable.

## Corrected original blockers

**B-1 — missing OPSEC and pending-auth route records: CORRECTED.**
`contracts/runtime/route_registry.json` `non_slash_routes` now contains
`route.unauthenticated_clone_first_read`, `route.unauthenticated_opsec_first_read`
(owner `SERVICE.OPSEC.001`), and `route.auth_first_read` (owner
`SERVICE.AUTH.001`). Each carries `ingress_step`, matching
`03_Exec.md` → `## §7 — RuntimeGate.Ingress` `ingress_order` steps 2, 3, and 4,
and each retains `status: active_route_with_undefined_owner_component`. Both
exclusive constraints from `00_Instructions.md` → `## Bootloader` are now in
`one_owner_constraints.rules` verbatim: "/ID and pending auth dispatch only to
SERVICE.AUTH.001." and "Unauthenticated OPSEC and clone/copy/recreate requests
dispatch only to SERVICE.OPSEC.001." `one_owner_constraints.source_map_ids` now
leads with `instructions.bootloader`, preserving the deployment-instruction
provenance alongside the kernel-capsule provenance. See B-5 below for the one
defect introduced inside this otherwise correct repair.

**B-2 — omitted referenced components and macro identifiers: CORRECTED.**
`contracts/runtime/component_registry.json` now registers `HumorLib`,
`Humor service` (`01_Persona.md` → `## Humor Relation`), `ErrorMacros catalog`
(`03_Exec.md` → `## §3 — Terminal Packet Contract`), `Error Macros catalog`
(`04_Exec_Library.md` → `### Error Coverage Boundary`), `error renderer`
(`04_Exec_Library.md` → `### Validation + Regression Model`), and
`Persona Engine` (`01_Persona.md` → `## Continuity` and `## Anchor Precedence`;
`04_Exec_Library.md` → `### PersonaLib` and `### MoodLib`). All six use exact
source labels, carry `status: referenced` and
`definition_status: declared_but_not_defined`, and have no invented versioned
IDs, inputs, outputs, or render prose. UR-023 through UR-026 record them, and
UR-024 explicitly refuses to collapse the two catalog spellings into one
identity. A new `declared_macro_identifiers` block records
`TIME_LOOKUP_BLOCKED` and `GENERIC_BLOCKED` with
`status: declared_identifier_only`, `render_text: null`, and
`implementation_behavior: null`, backed by UR-027.

**B-3 — validator guarantees weaker than documented: CORRECTED.**
`tools/validate_runtime_contracts.py` now publishes an explicit
`SUPPORTED_SCHEMA_KEYWORDS` allowlist and an `ANNOTATION_KEYWORDS` set,
`validate_schema_keywords` rejects any keyword outside the allowlist plus `x-*`,
`SUPPORTED_TYPES` rejects unknown `type` values, schema-valued
`additionalProperties` is rejected explicitly, and `check_type` raises on an
unknown type as a backstop. `validate_contracts()` now loads the fixture
directory and validates all five canonical positive fixtures and all five
canonical negative fixtures through `validate_instance`, so the standalone CLI
performs the fixture validation the README describes.
`contracts/runtime/README.md` now lists the supported subset by name, states
"It is not a general JSON Schema implementation", and closes with an explicit
statement that the checks "do not prove full JSON Schema compliance, runtime
implementation, host capability, behavioral parity, persistence, routing
execution, or artifact creation." Verified independently — see the validator
assessment below.

**B-4 — missing BC-010 assignment and validation records: CORRECTED.**
`docs/domains/runtime/assignments/BC-010/assignment.md` and
`docs/domains/runtime/assignments/BC-010/validation.md` now exist. Both carry
`record_status: backfilled`, name their evidence sources, and preserve the
original base `7aed76e`, owner, scope, amendment, and completion rules. The
validation record explicitly enumerates unavailable evidence rather than
inventing console output. The BC-010 row in `docs/worklogs/assignments.md` now
points to `docs/domains/runtime/assignments/BC-010/assignment.md` as required by
`AGENTS.md` → "Branch and assignment rules", and BC-010 remains `review`.

## Findings

### Blocking

**B-5 — `route_registry.json` assigns two routes the lane class `opsec`, a value
that appears in no CTS file, without flagging it as undeclared.**

Path: `contracts/runtime/route_registry.json`,
`non_slash_routes[route.unauthenticated_clone_first_read].lane_class` and
`non_slash_routes[route.unauthenticated_opsec_first_read].lane_class`, both
`"opsec"`.

Source authority: `kernel/golden/v0.22.0/03_Exec.md` →
`## §7 — RuntimeGate.Ingress` declares `lane_classes:` as exactly eight values —
`auth`, `diagnostic`, `static_render`, `repo_lookup`, `workflow_resume`,
`internal_library`, `ordinary_conversation`, `sandbox`. `## §3 — Terminal Packet
Contract` states "`lane_class` must match RuntimeGate.Ingress." The string
`opsec` appears in the CTS source only inside the ingress *step* name
`unauthenticated_opsec_first_read`, the `## OPSEC / Privacy` heading of the
deployment instruction, and Exec's `- OPSEC rule bodies` / `- OPSEC/clone
first-read locks ...` prose. Neither source role declares a lane class named
`opsec`. Exec declares that these steps lock a route but never declares which
lane class they lock.

I verified this mechanically: the only lane-class value used anywhere in
`route_registry.json` that is neither in `declared_lane_classes.values` nor
carried by `declared_lane_classes.route_table_only_value` is `opsec`.

Why blocking: this is an invented enum value presented as source-derived, which
is the failure class BC-010 and BC-010-C1 both prohibit ("do not invent missing
stable IDs"; "infer missing components into existence"). The same file already
demonstrates the correct handling for a lane value outside Exec's declared set —
`workflow` is carried in `declared_lane_classes.route_table_only_value` with
`conflict_register_id: UR-011` — so the convention the file establishes is that
an out-of-enum lane is flagged. `opsec` silently breaks that convention, and a
consumer building a lane validator from `declared_lane_classes` would either
reject both repaired routes or be forced to add a lane class Exec never
declared. It is also a regression introduced by the repair commit: the value did
not exist at base `38611bf`.

Smallest correct fix: set both to `null` (or omit `lane_class`) with a note that
Exec does not declare the locked lane class for these steps, or retain `"opsec"`
only as an explicitly flagged extraction-added label with an unresolved-register
entry in the style of UR-011.

Note: `route.auth_first_read` is not affected. Its `lane_class: "auth"` is
declared in Exec `§7 lane_classes` and confirmed by `03_Exec.md` → `## §9 —
RuntimeGate.Egress`, "When Ingress locks auth/SERVICE.AUTH.001".

### Non-blocking

**N-1 — the two OPSEC route records join a kernel-capsule ingress step to a
deployment-instruction-only owner without the `extraction_inference` label used
for the analogous join in the same file.**

Paths: `contracts/runtime/route_registry.json`
`non_slash_routes[route.unauthenticated_clone_first_read]` and
`[route.unauthenticated_opsec_first_read]`.

Source authority: `SERVICE.OPSEC.001` occurs exactly once across all seven CTS
files — `00_Instructions.md:35`, the deployment instruction. `03_Exec.md` →
`## §7` names the two ingress steps and states "OPSEC/clone first-read locks are
terminal deterministic service routes" but never names the owner. Binding the
kernel-declared step to the host-declared owner is therefore a cross-role
inference, structurally identical to `route.kernel_work`, which Codex correctly
marked `"provenance_classification": "extraction_inference"` and anchored to the
dedicated source-map entry `route.kernel_work_join`.

Why non-blocking: both provenances are preserved via
`source_map_ids: ["exec.ingress", "instructions.bootloader"]`, the owner binding
was directed by the approved BC-010-C1 packet §C-1, and
`SERVICE.OPSEC.001` remains `declared_but_not_defined`. The gap is inconsistent
labeling, not lost or falsified provenance.

**N-2 — three `dependencies` arrays still mix prose into an ID-shaped field,
after C-9 added `dependency_prose` precisely to separate them.**

Path: `contracts/runtime/component_registry.json`:

- `EXECLIB.MMU.001` → `["EXECLIB.STATETREE.001 for staged transition validation"]`
- `EXECLIB.READLANE.SOURCELIB.001` → `["EXECLIB.DATELIB.001 for anchored relative-date math"]`
- `RuntimeGate.Egress` → `["selected owner contract", "mandatory restraint packets"]`

Source authority: `04_Exec_Library.md` → `### MMULib` declares no `depends_on`;
`### Read Lane SourceLib` declares no `depends_on`; `03_Exec.md` → `## §9 —
RuntimeGate.Egress` describes what Egress verifies rather than declaring
dependencies. None of these strings is a resolvable component ID.

Why non-blocking: the annotations are accurate to the source and nothing is
misstated. C-9 was correctly applied to `Exec`, `Exec.Scheduler`,
`EXECLIB.PERSONALIB.001`, and `EXECLIB.MOODLIB.001`; these three were missed.
(`Persona` → `["Personal Experience Library (PEL)", "Identity_Lore"]` is an exact
source label set and is correct as written.)

**N-3 — negative-fixture tests assert only that errors were produced, not the
intended reason.**

Path: `tests/contracts/test_validate_runtime_contracts.py`
`test_positive_and_negative_schema_fixtures`, which ends in
`self.assertTrue(VALIDATOR.validate_instance(...))`. A fixture that failed for
an unintended reason — for example a schema-keyword error rather than the
intended instance violation — would still pass.

I verified the reasons independently and all five are correct and intentional:

```text
invalid_task_packet.json                    -> $: expected type ['object'], got list
invalid_capability_report.json              -> $: expected type ['object'], got list
invalid_scope_lock.json                     -> $: missing required property active_task
invalid_terminal_packet.json                -> $.validation_result: value is not in enum
invalid_current_turn_execution_receipt.json -> 11 missing required properties via allOf/$ref
```

Why non-blocking: the coverage is real and correct today; only the assertion is
weaker than it could be.

**N-4 — no schema retains `additionalProperties: false`, so the validator's
closure branch has no canonical fixture coverage.**

Paths: `contracts/runtime/schemas/scope_lock.schema.json` and
`terminal_packet.schema.json` (closure removed by the repair);
`tools/validate_runtime_contracts.py` `_validate_instance`, which still
implements `additionalProperties is False`.

Why non-blocking: the removal itself is correct — `03_Exec.md` → `## §3` declares
`required_fields` and `optional_fields` but never forbids additional fields, and
`## §4` lists `scope_lock_fields` without closing the object, so C-7's preferred
"remove the closure" outcome is the right reading and leaves nothing undisclosed.
C-3 item 8 ("a negative case for every schema that remains intentionally closed")
is therefore vacuously satisfied. Only an untested code path remains.

**N-5 — bookkeeping: BC-010-C1 record status headers disagree with the handoff
and the global index.**

`docs/domains/runtime/assignments/BC-010-C1/assignment.md` and
`.../validation.md` both carry `status: active`, while
`.../handoff.md` carries `status: review` and the BC-010-C1 row in
`docs/worklogs/assignments.md` reads `review`. Per the review instruction these
are recorded, not edited. They do not materially misrepresent the implementation
state: the handoff, the global index, and the runtime `next_steps.md` all
consistently place BC-010-C1 in `review` awaiting this review.

**N-6 — bookkeeping: minor stale metadata.**
`contracts/runtime/README.md` front matter still reads `assignment: BC-010` and
does not name BC-010-C1, although the body is fully updated.
`docs/worklogs/assignments.md:321` still reads "Blu's current runtime is the
Markdown CTS kernel", which is the undifferentiated phrasing
`docs/sources/cts_source_roles.md` → "Terminology" asks agents to avoid. That
file is inside the BC-010-C1 collision domain but the line was not named by any
C-item. No generated contract uses that phrasing; `contracts/runtime/README.md`
correctly says "one GPT deployment instruction and six kernel/runtime capsules".

## Source-role assessment

Implemented correctly, in both data and enforcement.

- `contracts/runtime/source_map.json` declares a deterministic file-role map
  under `source_roles`, with `00_Instructions.md` as the sole
  `deployment_instruction` and `01`–`06` as `kernel_runtime_capsule`, matching
  `docs/sources/cts_source_roles.md` exactly.
- Every one of the 83 source-map entries names a `source_file` inside that map,
  so every entry resolves to exactly one role. The validator enforces this at
  `validate_contracts` — `"source-map entry must resolve to exactly one source
  role"` — and separately enforces that the declared role sets equal
  `SOURCE_ROLE_FILES`, so the map cannot be quietly re-pointed.
- Host-only declarations are not presented as kernel definitions. The validator
  computes each component's roles from its source references and, when they
  resolve only to `deployment_instruction`, restricts `definition_status` to
  `declared_but_not_defined` or `defined_in_golden_deployment_instruction`. Both
  host-only components satisfy it: `00 Instructions` is
  `kind: deployment_instruction_entry` /
  `definition_status: defined_in_golden_deployment_instruction`, and
  `SERVICE.OPSEC.001` is `referenced` / `declared_but_not_defined`. The rule has
  real bite —
  `test_host_only_reference_cannot_be_kernel_definition` flips `00 Instructions`
  to `defined_in_golden` in a temp tree and the validator rejects it.
- Dual-role declarations preserve both provenances rather than collapsing them.
  `SERVICE.AUTH.001` carries `["instructions.bootloader", "commands.routes",
  "exec.scheduler"]`, matching its real occurrences in `00_Instructions.md:33`,
  `05_Commands.md:89`, and `03_Exec.md:319/354/375`. `SYSTEM.RUNTIME.001`
  carries both `instructions.bootloader` and `exec.runtime_configuration`. The
  repaired routes carry both `exec.ingress` and `instructions.bootloader`.
- `00_Instructions.md` authority is not weakened. `## Precedence` is now
  extracted as `instructions.precedence` and cited by PARITY-008, and the
  deployment instruction supplies both exclusivity rules now recorded in
  `one_owner_constraints`.
- `contracts/runtime/README.md` describes one deployment instruction plus six
  kernel/runtime capsules and states that generated contracts "are
  downstream-only and do not outrank either source role."

## Auth and OPSEC routing assessment

- All three ingress steps are recorded with their exact
  `03_Exec.md` → `## §7` step names and in source order (steps 2, 3, 4).
- Route ordering provenance comes from Exec; exclusivity provenance comes from
  the deployment instruction. Both are cited.
- `SERVICE.AUTH.001` and `SERVICE.OPSEC.001` remain
  `definition_status: declared_but_not_defined`, backed by UR-003 and UR-008,
  and every route carries `status: active_route_with_undefined_owner_component`.
- Registry presence is not represented as execution or host-capability proof:
  `component_registry.json` carries the `boundary` disclaimer,
  `contracts/runtime/README.md` repeats it, and UR-019 keeps host capability
  conditional.
- Two defects sit inside this otherwise correct repair: the invented `opsec`
  lane class (B-5) and the unlabeled cross-role inference (N-1).

## Referenced components and unresolved declarations

Nothing was invented. Verified against source for each label:

- `HumorLib` and `Humor service` are kept as two distinct entries with identical
  declared ownership, matching `01_Persona.md` → `## Humor Relation` which names
  both. UR-023 explicitly declines to merge them.
- `ErrorMacros catalog` (Exec spelling) and `Error Macros catalog` (ExecLib
  spelling) are kept distinct. UR-024 states the spelling variants "are not
  enough evidence to collapse them into one future identity."
- `error renderer` and `Persona Engine` are recorded with declared ownership
  only, no IDs, inputs, or outputs. UR-025 and UR-026 require later definition
  "without inventing macro prose" and "without reducing Persona or inventing a
  versioned ID."
- `TIME_LOOKUP_BLOCKED` and `GENERIC_BLOCKED` appear only as identifiers with
  `render_text: null` and `implementation_behavior: null`. UR-027 records that
  the source declares no render text or behavior.
- Possible identity relationships remain unresolved wherever the CTS leaves them
  open — the two humor labels, the two catalog spellings, and
  `SERVICE.ECHOTRACE.001` versus `EXEC.SPINE_TRACE` (UR-005).

## StateTree

Preserved correctly and extended without resolution.
`component_registry.json` `EXECLIB.STATETREE.001` retains
`"status": "unresolved_conflict"` and
`"declared_statuses": ["ALPHA", "ACTIVE"]`, and its provenance now spans seven
source-map ids: the four `lib_id`-bearing blocks
(`### StateTree Library` at `status: ALPHA`, `### StateTree Explicit Validation
Packet`, `### StateTree Tag Validation`, `### StateTree MemoryPacket Import
Validation`, all `ACTIVE`), plus the two registry mentions
(`### Active Component Registry Stabilization`, `### Active Component
Registry`) and the `/help` trace-target listing in `05_Commands.md` `§5.2`.
This closes the provenance gap I raised as N-8 in the BC-010 review. No status
was chosen. `test_statetree_conflict_and_extended_provenance_are_preserved`
asserts all of it.

## Extraction inference

`source_map.json` adds `"extraction inference"` to `classification_values`, and
the validator adds it to `SOURCE_CLASSIFICATIONS`. The
`kernel_work_first_read` → `internal_library` → `EXECLIB.BLUCODE.001` join is now
represented by a dedicated source-map entry `route.kernel_work_join`, classified
`extraction inference`, anchored to `03_Exec.md` → `## §8 — Exec.Scheduler` with
the exact locator line, and carrying an `inference` field that states plainly
that it "Joins the separately declared kernel_work_first_read ingress step to the
internal_library/EXECLIB.BLUCODE.001 Scheduler lock."
`route_registry.json` `route.kernel_work` now carries
`"provenance_classification": "extraction_inference"` and references that entry.
This is exactly the treatment C-11 required. It is also the pattern the two
OPSEC routes should have followed (N-1).

## PASS provenance

Corrected. `"/PASS"` is gone from
`route_registry.json` `unavailable_command_surfaces.values`, which now holds only
the five stems `05_Commands.md` → `## §3 — Commands Not Live in This Build`
actually lists. A new `non_live_feature_declarations` block records
`label: "PASS command"`, `status: "not_live"`,
`statement: "The PASS command is not live in this build."` — byte-identical to
`05_Commands.md` → `## PASS Removal Note` — and
`"literal_slash_stem_declared": false`. The section is now anchored as the
source-map entry `commands.pass_removal` and cited by PARITY-011.
`test_pass_is_not_a_source_declared_slash_stem` asserts the stem is absent and
the flag is false. The CTS statement is preserved and the invented command
surface is gone.

## Schema strengthening

Fully resolved by removal, which C-7 named as the preferred outcome.
`additionalProperties: false` no longer appears in any schema. The only remaining
uses are `additionalProperties: true` in
`task_packet.schema.json` and `capability_report.schema.json`, which are
permissive rather than strengthening and are already disclosed by UR-013 and
UR-014 and by each schema's own `description` and
`x-blu-contract-status: underspecified`. This is the correct reading:
`03_Exec.md` `## §3` and `## §4` declare field sets without prohibiting
additional fields. No silent strengthening remains, so nothing needed disclosure
in `unresolved_register.json`.

## Dependencies and provenance

Mostly corrected.

- `EXECLIB.MOODLIB.001` now carries
  `dependency_prose: ["MoodLib is downstream of Identity, Persona Engine, and
  Anchors."]` — the exact `04_Exec_Library.md` → `### MoodLib` wording, with
  Identity and Anchors restored — and `dependencies: []`.
- `EXECLIB.PERSONALIB.001` now carries the exact source note "PersonaLib is the
  hosted-runtime bridge for Persona Engine." in `dependency_prose` with
  `dependencies: []`, instead of the previous invented `"Persona source"` ID.
- `Exec` and `Exec.Scheduler` dependency lists are now complete against
  `03_Exec.md` → `## §8 — Exec.Scheduler`, adding `SERVICE.AUTH.001`,
  `SERVICE.ECHOTRACE.001`, `SERVICE.REPOBOOT.001`, `PROGRAM.SIMCODE.001`,
  `PROGRAM.MEMORY.001`, `EXECLIB.BLUCODE.001`, and `SERVICE.CONTEXTINTAKE.001`,
  with the `workflow_resume` owner rule and the ContextIntake support path held
  in `dependency_prose` rather than forced into IDs.
- Residual mixing in three components is recorded as N-2.

## Persona and Operations boundaries

No flattening or weakening found.

- Persona remains `kind: model_facing_source` /
  `definition_status: defined_in_golden_model_facing` with ownership copied from
  `01_Persona.md` → `## Authority Boundary`. The newly added
  `persona.continuity`, `persona.anchor_precedence`, and
  `persona.humor_relation` entries exist only to anchor referenced-component
  provenance; no ribbon palette, mood word list, anchor library, swatch mapping,
  or touchstone set was converted into a schema field, enum, or route.
  PARITY-009 still states the non-routing boundary.
- Operations Law was strengthened as provenance, not converted into validator
  behavior. The five previously missing doctrines are now anchored
  (`operations.artifact_context`, `operations.operational_continuity`,
  `operations.kernel_change`, `operations.system_component`,
  `operations.error_recovery`) and cited where they belong: `System Component
  Doctrine` on PARITY-003 and PARITY-008, `Artifact & Working Context Doctrine`
  on PARITY-007, `Error & Recovery Doctrine` on PARITY-006, `Operational
  Continuity Doctrine` on PARITY-005 and PARITY-008. `Execution Discipline
  Doctrine` remains classified `intentionally unmodeled prose`. No doctrine text
  was reduced to a deterministic rule.
- Contract files are not treated as equal to the CTS source.
  `contracts/runtime/README.md`: "If a contract here differs from either source
  role, the golden source wins."

## No runtime implementation

Confirmed. The repair commit touched 27 files, of which the only executable
surface is `tools/validate_runtime_contracts.py`,
`tests/contracts/test_validate_runtime_contracts.py`, and five JSON fixtures.
The whole repository contains exactly two `.py` files, both validation tooling.
The validator imports only `argparse`, `json`, `re`, `sys`, `pathlib`, and
`typing`. It contains no Blu runtime execution, routing enforcement, Auth or
OPSEC service, persistence, reminders, Local Mirror, PASS, or Chat/Codex
adapter. Its module docstring states it "is contract-validation tooling, not Blu
runtime implementation or a general JSON Schema validator." No file under
`kernel/golden/**` changed.

## Validator assessment

Verified by reading the code and by execution, not by test name.

Working as documented:

- `SUPPORTED_SCHEMA_KEYWORDS` is an explicit 11-entry allowlist; anything else
  that is not in `ANNOTATION_KEYWORDS` and does not start with `x-` produces
  `unsupported schema keyword <name>`. Confirmed by
  `test_unsupported_schema_keyword_fails` using `oneOf`.
- `SUPPORTED_TYPES` rejects unknown `type` values with `unknown or invalid schema
  type`. Confirmed by `test_unknown_schema_type_fails` using `"packet"`.
  `check_type` raises `ValueError` on an unknown type as a second line of
  defense.
- Annotations `$schema`, `$id`, `title`, `description`, and any `x-*` key are
  permitted, which is what the extraction's `x-blu-contract-status` and
  `x-source-map-id` fields require.
- `validate_schema_keywords` recurses through `allOf`, `properties`, and `items`,
  and rejects schema-valued `additionalProperties`.
- `validate_instance` runs the keyword check before instance checking, so a
  schema outside the subset fails loudly rather than silently asserting nothing.
- The standalone CLI validates fixtures. `validate_contracts` iterates
  `CANONICAL_FIXTURES`, requires each fixture file to exist, fails if a positive
  fixture produces errors, and fails if a negative fixture produces none
  (`canonical negative fixture was accepted`).
- Source anchoring is now exact. `source_anchor_errors` requires
  `source_section` to match `^(#{1,6})[ \t]+\S`, to equal a full line, and to
  occur exactly once; `source_locator`, when present, must match a stripped line
  exactly once inside that heading's own section, bounded by the next
  same-or-higher-level heading. Substring matching is gone. The prefix ambiguity
  I raised in the BC-010 review is resolved by full-line equality —
  `### Active Component Registry` no longer matches
  `### Active Component Registry Stabilization`, and both are now separate
  entries. `test_source_sections_are_exact_heading_anchors` proves the truncated
  heading `### Active Component Reg` is rejected.
- Malformed JSON and missing required contracts still fail, proven in temp trees
  by `test_malformed_json_fails` and `test_required_contract_missing_fails`.
- Full JSON Schema compliance is not claimed anywhere; the module docstring,
  `contracts/runtime/README.md`, and
  `docs/domains/runtime/assignments/BC-010-C1/validation.md` all disclaim it.
- Validator success is not represented as behavioral parity. The CLI success
  line is "PASS: runtime contracts and canonical fixtures satisfy the supported
  structural subset", and `parity_matrix.json` retains its `boundary` field
  stating presence "is not proof that any adapter or future implementation
  passes them."

Limits found:

- The validator performs no lane-class validation, which is why B-5 passes
  undetected. `declared_lane_classes` is data only; nothing checks that a route's
  `lane_class` appears there or is flagged.
- N-3 and N-4 above.

## Validation-evidence assessment

Codex's handoff and validation claims were checked against the actual diff and
test surface. Every claim I could test was accurate.

| Claim | Independently verified |
|---|---|
| 27 files in the repair commit | 27 |
| 8 runtime contract files incl. 2 relaxed schemas | 8 contract paths; both `additionalProperties: false` removals confirmed in the diff |
| 1 validator, 1 test module, 5 new negative fixtures | confirmed by `git diff --name-status` |
| No `kernel/golden/**` change | confirmed; checksums re-verified after review |
| `python tools/validate_runtime_contracts.py` exit 0 | PASS, exit 0, exact banner matches |
| `python -m unittest discover ...` 15 tests OK | Ran 15 tests, OK, exit 0 |
| `GOLDEN_CHECKSUMS=8/8` | recomputed independently: 8/8 |
| `MANIFEST_VERIFIED=121/121` | recomputed independently: 121/121, 0 failed, 0 missing |
| UR-023 – UR-027 added, UR-001 – UR-022 retained | 27 items total, ids contiguous |
| StateTree conflict preserved | confirmed |
| Metadata commit touched no implementation surface | `git diff --exit-code` exit 0 |

Recomputed contract totals at the repair commit: 83 source-map entries (74
explicit declaration, 4 intentionally unmodeled prose, 4 unresolved conflict, 1
extraction inference), 47 registry components, 2 declared macro identifiers, 6
live slash routes, 7 non-slash routes, 27 unresolved items, 12 parity
requirements, 34 parity cases.

The validation record's "What validation proves / does not prove" split is
accurate. One phrase in it is slightly generous: "Golden checksum and diff
preservation when the required Git/hash checks pass" describes checks run
alongside the validator rather than by it — the validator itself verifies golden
checksums only through the separate unit test
`test_golden_checksum_manifest_still_matches_all_eight_entries`. Not a finding;
noted for accuracy.

## Correctly preserved unresolved declarations

All of the following remain open and were not resolved by the repair:

- `EXECLIB.STATETREE.001` `ALPHA` versus `ACTIVE` (UR-012), now with seven-source
  provenance and still no chosen status.
- The `workflow` lane class absent from Exec's declared list (UR-011), with the
  terminal-packet schema still leaving `lane_class` an open string.
- All referenced-but-undefined owners: `EXECLIB.ANTIDRIFT.001`,
  `SERVICE.OPSRESTRAINT.001`, `SERVICE.AUTH.001`, `SERVICE.REPOBOOT.001`,
  `EXECLIB.BLUCODE.001`, `SYSTEM.RUNTIME.001`, `SERVICE.OPSEC.001`,
  `SIMCODE_GATE`, `MEMORY_GATE`, `GateKernel` (UR-001 – UR-009, UR-020).
- `SERVICE.ECHOTRACE.001` versus `EXEC.SPINE_TRACE` ownership split (UR-005).
- `/mood` declared not live while `MoodLib` is `ACTIVE` with a `force_show` path
  (UR-010).
- Empty `Compatibility phase owners:` / `Compatibility rule:` headings in
  `06_Programs.md` `§1` (UR-016).
- `PROGRAM.MEMORY.001` universal-contract incompleteness (UR-021), still
  `inputs: null` / `outputs: null` rather than synthesized from prose.
- Permissive task-packet and capability-report schemas (UR-013, UR-014) and the
  receipt-as-terminal-packet alias (UR-015).
- Alias-registry incompleteness (UR-022); no aliases synthesized from names.
- PEL and Identity_Lore as external, unimported sources (UR-018).
- Host capability, persistence, background execution, and artifact proof held
  conditional (UR-019).
- New: HumorLib / Humor service (UR-023), the two ErrorMacros catalog spellings
  (UR-024), error renderer (UR-025), Persona Engine (UR-026), and the two macro
  identifiers (UR-027).

## Required checks

```text
git status --short                                  -> clean
git rev-parse HEAD                                  -> 2d7198c653af0f9d78277822064920def77b78cb (branch base)
git show -s --format=%H 63c8b692...                 -> 63c8b692403fe5ec1a9433a8313a7980fbd55437 (present)
git show -s --format=%H 2d7198c6...                 -> 2d7198c653af0f9d78277822064920def77b78cb (present)
git diff --check                                    -> exit 0, no output
git diff --exit-code 63c8b692 2d7198c6
  -- contracts/runtime tools tests kernel/golden    -> exit 0
python tools/validate_runtime_contracts.py          -> "PASS: runtime contracts and canonical
                                                       fixtures satisfy the supported structural
                                                       subset", exit 0
python -m unittest discover -s tests/contracts
  -p "test_*.py"                                    -> Ran 15 tests, OK, exit 0
PowerShell Get-FileHash SHA256 vs SHA256SUMS        -> GOLDEN_CHECKSUMS=8/8
PowerShell Get-FileHash SHA256 vs MANIFEST.sha256   -> MANIFEST_VERIFIED=121/121 (0 fail, 0 missing)
```

`sha256sum` is absent on this Windows host; the repository's PowerShell
`Get-FileHash -Algorithm SHA256` equivalent was used, matching the limitation
recorded in `docs/domains/runtime/failures.md`. Both checksum results were
computed independently by this review, not copied from Codex's report.

## Disposition

**return-for-correction**

Scoped narrowly. All four original blockers (B-1 – B-4) are genuinely corrected,
the source-role separation is implemented and enforced, the validator now keeps
the promises its documentation makes, and nothing was invented to close a source
gap in the registry, macros, PASS, schemas, or StateTree. The single blocking
item is B-5: two route records assign a lane class that no CTS file declares,
introduced by this repair commit, in the one artifact where the file's own
`declared_lane_classes` convention shows how an out-of-enum lane is supposed to
be flagged.

The correction is a one-field change in two records plus, if `opsec` is retained
as a label, one unresolved-register entry.

If Blu or Dad judge `lane_class` in `non_slash_routes` to be a descriptive
grouping label rather than a claimed source-declared value, then
`approve-with-notes` is a defensible alternative with B-5 demoted to a
non-blocking follow-up. That call is theirs, not mine.

## Required follow-up

Blocking correction:

1. **B-5** — In `contracts/runtime/route_registry.json`, replace
   `"lane_class": "opsec"` in `route.unauthenticated_clone_first_read` and
   `route.unauthenticated_opsec_first_read` with either a null/omitted value plus
   a note that `03_Exec.md` `## §7` does not declare the locked lane class for
   these steps, or an explicitly flagged extraction-added label carrying an
   `unresolved_register.json` entry in the UR-011 style. Consider adding a
   validator check that every route `lane_class` is either in
   `declared_lane_classes.values`, equal to `route_table_only_value`, or flagged,
   so the class of defect cannot recur silently.

Recommended, non-blocking:

2. **N-1** — Add `"provenance_classification": "extraction_inference"` to the two
   OPSEC routes, with a source-map inference entry in the style of
   `route.kernel_work_join`, since `SERVICE.OPSEC.001` is declared only in the
   deployment instruction while the ingress steps are declared only in Exec.
3. **N-2** — Move the three residual prose annotations out of `dependencies` and
   into `dependency_prose` for `EXECLIB.MMU.001`,
   `EXECLIB.READLANE.SOURCELIB.001`, and `RuntimeGate.Egress`.
4. **N-3** — Assert the intended failure reason in
   `test_positive_and_negative_schema_fixtures` rather than a truthy error list.
5. **N-4** — Optionally add a unit test for the validator's
   `additionalProperties: false` branch, which no canonical schema now exercises.
6. **N-5, N-6** — Blu or Dad: align the BC-010-C1 `assignment.md` and
   `validation.md` status headers with the `review` state recorded in the handoff
   and global index, refresh the `assignment:` front-matter line in
   `contracts/runtime/README.md`, and decide whether
   `docs/worklogs/assignments.md:321` should adopt the
   `docs/sources/cts_source_roles.md` terminology.

Reserved to Blu and Dad: every item in
`contracts/runtime/unresolved_register.json` (UR-001 – UR-027). This review
resolves none of them. BC-020 and BC-030 should remain unstarted until their
packets are approved and bases named, per
`docs/domains/runtime/next_steps.md`.

## Final status authorization

- Authorized by: pending — Blu and Dad
- Assignment status: BC-010 and BC-010-C1 both remain `review`; this reviewer
  does not set `done`
- Date: 2026-08-06
