# BC-010-C2 — Review Record

status: done
owner: Claude
last_reviewed: 2026-08-06

## Review identity

- Assignment: BC-010-C2 — OPSEC Route Classification Repair
- Parent assignments: BC-010, BC-010-C1
- Base before C2: `424f80b254a02f057da6c82db5230377076fc415`
- Reviewed repair work commit: `06292ce0e2f326ef84988e030c7fe14402192859`
- Metadata record commit / review-branch base: `f8aa77f43b27e0d9d49f4fd23d4f097fa4a262bc`
- Review branch: `bc-010-c2-semantic-review`
- Reviewer: Claude
- Review type: read-only final semantic review against the CTS source set
- Integration commit or merge identity: none; Blu and Dad own final closure

This review changed no implementation file. It did not modify contracts, tests,
validator code, golden sources, assignment packets, handoff records, validation
records, domain decisions, the global assignment index, or Git history.

The metadata record commit was verified not to alter the implementation surface.
`git diff --exit-code 06292ce f8aa77f -- contracts/runtime tools tests
kernel/golden` returned exit 0; that commit changed only `MANIFEST.sha256`,
`docs/domains/runtime/assignments/BC-010-C2/handoff.md`, and
`docs/worklogs/assignments.md`.

## Golden sources compared

All seven CTS files were used as the authoritative comparison, with source roles
honored per `docs/sources/cts_source_roles.md`.

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

Sections load-bearing for this review, re-read directly at the reviewed commit:
`03_Exec.md` → `## §7 — RuntimeGate.Ingress` (`ingress_order`,
`ordered_ingress_execution`, `lane_classes`, `ingress_route_rules`),
`## §8 — Exec.Scheduler`, `## §9 — RuntimeGate.Egress`;
`00_Instructions.md` → `## Bootloader` and `## OPSEC / Privacy`;
`04_Exec_Library.md` → `### DateLib`, `### Read Lane SourceLib`,
`### Staged Memory Integration`, `### Archive Index + MMU Trace Integration`;
`05_Commands.md` → `## §4 — Canonical Slash Route Registry`.

Generated artifacts inspected: `contracts/runtime/README.md`,
`source_map.json`, `component_registry.json`, `route_registry.json`,
`unresolved_register.json`, `parity_matrix.json`, `schemas/**`,
`tools/validate_runtime_contracts.py`,
`tests/contracts/test_validate_runtime_contracts.py`, all fixtures, plus
`docs/domains/runtime/decisions.md`, the runtime quartet, the BC-010-C2 quartet,
and `docs/worklogs/assignments.md`.

## C1 blocker: corrected

**C1 B-5 — invented `opsec` lane class: CORRECTED, and correctly.**

`contracts/runtime/route_registry.json` `non_slash_routes` now records both
OPSEC routes as:

```json
"lane_class": null,
"lane_class_status": "undeclared_in_golden_source",
"unresolved_register_id": "UR-028"
```

Verified mechanically: `grep -rn '"lane_class": *"opsec"' contracts/runtime/`
returns no matches, and a full case-insensitive `opsec` sweep of
`contracts/runtime/**` shows the token surviving only as the real source
identifier `SERVICE.OPSEC.001`, the real Exec ingress step name
`unauthenticated_opsec_first_read`, the exact deployment-instruction exclusivity
rule, and UR-028 / the join record — never as a lane value.

Each of the four sub-conditions holds:

- **Neither route was reassigned to `auth`.** Both are `null`.
  `route.auth_first_read` alone retains `lane_class: "auth"`, which is directly
  declared: `03_Exec.md` → `## §7` lists `auth` in `lane_classes:`, and `## §9 —
  RuntimeGate.Egress` states "When Ingress locks auth/SERVICE.AUTH.001".
- **`opsec` was not added to Exec's declared lane enum.**
  `declared_lane_classes.values` is unchanged and still exactly the eight values
  from `03_Exec.md` `## §7 lane_classes:` — `auth`, `diagnostic`,
  `static_render`, `repo_lookup`, `workflow_resume`, `internal_library`,
  `ordinary_conversation`, `sandbox`.
- **No contract claims the golden source already defines OPSEC as a pre-ingress
  restraint.** The only occurrence of that phrasing anywhere under
  `contracts/`, `tools/`, or `tests/` is UR-028's summary, which states the
  opposite: the golden source "does not ... formally resolve whether OPSEC is a
  route lane or a pre-ingress restraint." That is preservation of the gap, not a
  claim.
- **The unresolved register records the gap.** UR-028,
  `category: route_classification_underspecified`,
  `preserved_state: null_lane_class_with_cross_role_owner_join`, requires a later
  decision "without projecting that later decision backward into the golden CTS
  extraction."

The `null` representation is the exactly correct reading rather than merely a
safe one. `03_Exec.md` → `## §7 ordered_ingress_execution` states: "Each step
must either return NO_MATCH and continue, or return LOCKED with lane_class,
owner, source_or_contract, and terminal_expected." Exec therefore *requires* a
lane class to exist when these steps lock, while never declaring which value it
is. A null value plus an explicit undeclared status plus a register entry is the
only representation that preserves both facts — that the field is mandatory and
that its value is absent from the source.

## Findings

### Blocking

None.

### Non-blocking

**N-1 — the two join records anchor at different precision levels.**

Path: `contracts/runtime/source_map.json`, entries `route.opsec_owner_join` and
`route.kernel_work_join`.

`route.kernel_work_join` pins an exact line via `source_locator`
("- Scheduler must call `EXECLIB.BLUCODE.001` when Ingress locks
internal_library/EXECLIB.BLUCODE.001."). `route.opsec_owner_join` anchors only
to the `03_Exec.md` → `## §7 — RuntimeGate.Ingress` heading with no
`source_locator`, relying on `joined_source_map_ids` plus its `inference` prose
to carry the detail.

Why non-blocking: the design is sound and arguably necessary. The validator
requires each source-map entry to resolve to exactly one source role, so a join
spanning `03_Exec.md` and `00_Instructions.md` cannot carry both roles on the
entry itself; `joined_source_map_ids` is the correct compensating mechanism, and
the validator now checks that those ids resolve. Nothing is misstated — only the
line-level precision differs between two structurally different joins (one
within-file, one cross-role). A `source_locator` such as the
`- OPSEC/clone first-read locks are terminal deterministic service routes.` line
would tighten it.

**N-2 — one component dependency ID is resolved from a source *name* rather than
a declared ID, with no inference marker available in that field.**

Path: `contracts/runtime/component_registry.json`,
`EXECLIB.READLANE.SOURCELIB.001` → `dependencies: ["EXECLIB.DATELIB.001"]`.

Source: `04_Exec_Library.md` → `### Read Lane SourceLib` declares no
`depends_on:` and refers only to "use DateLib.offset_date for deterministic date
math only after a date anchor exists". The literal string
`EXECLIB.DATELIB.001` occurs in that file only at DateLib's own `lib_id:` and in
Time Service's `depends_on:`. The ID is therefore resolved from the declared
name, not quoted from a dependency declaration.

Why non-blocking: the lib_id is real and belongs to the same file, so nothing is
invented; C2-4's "invent no component IDs" is satisfied; and the accompanying
`dependency_prose` now carries the source wording almost verbatim. The
component registry simply has no per-dependency `provenance_classification`
field, so the name-to-ID resolution cannot currently be marked the way route
joins are. Recorded for completeness, not as a defect.

For contrast, the sibling repair is fully source-backed:
`EXECLIB.MMU.001 → EXECLIB.STATETREE.001` is literally named in
`04_Exec_Library.md` → `### Staged Memory Integration`
("State validation: EXECLIB.STATETREE.001") and
`### Archive Index + MMU Trace Integration`, so that ID is quoted, not inferred.

**N-3 — one prior assertion was loosened to accommodate the new join id.**

Path: `tests/contracts/test_validate_runtime_contracts.py`,
`test_repaired_non_slash_routes_and_exclusivity_constraints_exist`, changed from
`assertEqual({"exec.ingress", "instructions.bootloader"}, set(...))` to
`assertTrue(expected_sources.issubset(...))`.

Why non-blocking: the relaxation is required — `route.opsec_owner_join` was
legitimately added to `source_map_ids` — and it is more than compensated by the
new `test_opsec_routes_preserve_undeclared_lane_and_cross_role_inference`, which
asserts the join id is present and that its two joined sources resolve to
exactly `{kernel_runtime_capsule, deployment_instruction}`.

**N-4 — bookkeeping: BC-010-C2 `review.md` carried `status: pending` at the
reviewed commit.**

Correct and intended: the C2 packet §C2-7 instructs Codex to "leave `review.md`
pending for Claude". This record supersedes it. Recorded only so the status
transition is traceable. No other record-status inconsistency was found — see
the bookkeeping assessment below.

## Correctly preserved unresolved declarations

C2 added one item and resolved none. All twenty-eight remain open:

- **UR-028 (new)** — the absent lane class for
  `unauthenticated_clone_first_read` and `unauthenticated_opsec_first_read`, and
  the unresolved route-lane versus pre-ingress-restraint question. Neither is
  answered by the extraction, and the approved successor decision is explicitly
  excluded from being read backward into it.
- `SERVICE.OPSEC.001` (UR-008) and `SERVICE.AUTH.001` (UR-003) remain
  `status: referenced` / `definition_status: declared_but_not_defined`. C2 did
  not upgrade either owner, and both routes still carry
  `status: active_route_with_undefined_owner_component`.
- `EXECLIB.STATETREE.001` (UR-012) remains `status: unresolved_conflict` with
  `declared_statuses: ["ALPHA", "ACTIVE"]` and seven-source provenance. No
  winner chosen.
- The `workflow` lane conflict (UR-011) remains, still carried as
  `route_table_only_value` with its conflict register link — and the new
  validator closure explicitly re-validates that linkage rather than
  regularizing it away.
- All remaining referenced-but-undefined owners (18 components at
  `declared_but_not_defined`), including `EXECLIB.ANTIDRIFT.001`,
  `SERVICE.OPSRESTRAINT.001`, `SERVICE.REPOBOOT.001`, `EXECLIB.BLUCODE.001`,
  `SYSTEM.RUNTIME.001`, `SIMCODE_GATE`, `MEMORY_GATE`, `GateKernel`, `HumorLib`,
  `Humor service`, both `ErrorMacros`/`Error Macros catalog` spellings,
  `error renderer`, and `Persona Engine`.
- `TIME_LOOKUP_BLOCKED` and `GENERIC_BLOCKED` (UR-027) remain identifiers only,
  with `render_text: null` and `implementation_behavior: null`.
- `/mood` (UR-010), empty Program compatibility headings (UR-016),
  `PROGRAM.MEMORY.001` universal-contract incompleteness (UR-021), permissive
  task/capability schemas (UR-013, UR-014), the receipt alias (UR-015),
  alias-registry incompleteness (UR-022), PEL/Identity_Lore as external
  (UR-018), and host capability conditionality (UR-019).

## Source-role assessment

Preserved and, for the OPSEC join, strengthened.

- `source_map.json` `source_roles` is unchanged and still maps
  `00_Instructions.md` alone to `deployment_instruction` and `01`–`06` to
  `kernel_runtime_capsule`, matching `docs/sources/cts_source_roles.md`.
- The new `route.opsec_owner_join` entry resolves to exactly one role, as the
  validator requires, and carries the cross-role pair in
  `joined_source_map_ids: ["exec.ingress", "instructions.bootloader"]`. The
  validator now verifies those ids resolve to real source-map entries.
- Both roles are preserved on the routes themselves:
  `source_map_ids: ["exec.ingress", "instructions.bootloader",
  "route.opsec_owner_join"]`.
- The role split is now *asserted*, not merely present.
  `test_opsec_routes_preserve_undeclared_lane_and_cross_role_inference` resolves
  each joined id through `declared_source_roles` and asserts the resulting role
  set equals `{"kernel_runtime_capsule", "deployment_instruction"}`. That test
  fails if the two provenances are ever collapsed into one role.
- The C1 deployment-only guard is untouched and still active:
  `SERVICE.OPSEC.001`, whose only citation is `instructions.opsec`, remains
  `declared_but_not_defined`, and the validator still rejects a deployment-only
  reference reclassified as a kernel definition.
- Terminology is now consistent. `docs/worklogs/assignments.md` standing
  guardrails replaced "Blu's current runtime is the Markdown CTS kernel" with
  "Blu's current CTS deployment is one GPT deployment instruction plus six
  kernel/runtime capsules." The only surviving occurrences of the old phrase are
  the C1 review quoting it as a finding and the C2 packet instructing the fix —
  both legitimate.

## Extraction-inference assessment

Correct and now consistent across both joins.

- Both OPSEC routes carry `"provenance_classification": "extraction_inference"`,
  matching the treatment `route.kernel_work` received in C1.
- The dedicated join record `route.opsec_owner_join` is classified
  `"extraction inference"` — one of the four values in
  `source_map.classification_values` and in the validator's
  `SOURCE_CLASSIFICATIONS` — and its `inference` field states plainly that it
  "Joins the separately declared unauthenticated_clone_first_read and
  unauthenticated_opsec_first_read ingress steps to the
  deployment-instruction-only SERVICE.OPSEC.001 owner while preserving both
  source roles."
- The join is accurate to the source. `SERVICE.OPSEC.001` occurs exactly once
  across all seven CTS files — `00_Instructions.md:35`, the deployment
  instruction. `03_Exec.md` → `## §7` declares the two ingress steps and states
  "OPSEC/clone first-read locks are terminal deterministic service routes" but
  never names the owner. Calling the binding an inference is factually right,
  and the word "deployment-instruction-only" in the inference text is literally
  true.
- The join is not presented as one direct declaration: the route's three
  `source_map_ids` keep the two originating declarations addressable separately
  from the join record itself.

This closes C1 finding N-1.

## Successor-decision separation

Clean. The approved Auth/OPSEC boundary is recorded in
`docs/domains/runtime/decisions.md` under a dated heading that opens with
"Approved for successor-runtime design; this is not a retroactive change to the
golden CTS source", and closes by requiring that "Generated BC-010 contracts must
preserve that source gap rather than pretending the successor decision already
exists in the golden kernel."

I searched `contracts/`, `tools/`, and `tests/` for the decision's distinctive
language ("pre-ingress restraint", "mandatory pre-ingress", "Admin-level"). The
sole hit is UR-028's summary, and it asserts the source does *not* resolve the
question. The decision text itself appears only in
`docs/domains/runtime/decisions.md` and the approved C2 packet. No generated
contract claims the CTS defines OPSEC as a pre-ingress restraint, an OPSEC lane,
or a complete OPSEC service.

## Validator and test assessment

**Lane-class closure is genuinely enforced.**
`tools/validate_runtime_contracts.py` adds `route_lane_class_errors`, wired into
`validate_contracts`, covering both `live_slash_routes` and `non_slash_routes`:

- a non-null `lane_class` must be in `declared_lane_classes.values`, or equal
  `route_table_only_value` *and* have a `conflict_register_id` that resolves to a
  real unresolved item; anything else yields
  `undeclared route lane_class '<value>': <route id>`;
- a null `lane_class` requires all three of `lane_class_status` in
  `UNDECLARED_LANE_STATUSES`, source refs that all resolve to real source-map
  ids, and an `unresolved_register_id` that resolves to a real unresolved item;
- a non-string, empty `lane_class` is rejected outright;
- the `route_table_only_value` / `conflict_register_id` pairing is itself
  validated, so the `workflow` escape hatch cannot be reused without a live
  register entry.

`validate_contracts` also now checks that every `joined_source_map_ids` value
resolves, which protects the new join record from silent decay.

**All eight required test propositions are proven, and I inspected the bodies
rather than the names:**

| Required proposition | Test | How it is proven |
|---|---|---|
| Both OPSEC lane classes null | `test_opsec_routes_preserve_undeclared_lane_and_cross_role_inference` | `assertIsNone(route["lane_class"])` per route |
| Both carry undeclared status | same | `assertEqual("undeclared_in_golden_source", ...)` |
| Both owner joins are extraction inference | same | `assertEqual("extraction_inference", ...)` plus join classification and the two-role assertion |
| `opsec` rejected as undeclared | `test_lane_class_closure_rejects_opsec_and_arbitrary_inventions` | deep-copies the registry, sets `lane_class="opsec"`, asserts the exact error string |
| Arbitrary lane rejected | same | second sub-test with `"invented_lane"` |
| `auth` remains valid | `test_lane_class_closure_accepts_declared_auth_and_unresolved_workflow` | whole-registry closure returns `[]`; asserts `route.auth_first_read` is `auth` |
| Route-table-only `workflow` remains valid | same | asserts `/memory` is `workflow` and closure still passes |
| Null without unresolved status rejected | `test_null_lane_class_without_unresolved_status_is_rejected` | pops `lane_class_status`, asserts the exact error string |

The `opsec` rejection test is also a standing guard against the enum being
widened: if `opsec` were ever added to `declared_lane_classes.values`, that test
would fail.

**Negative-fixture precision is fixed.** C1 finding N-3 is closed.
`test_positive_and_negative_schema_fixtures` now compares the validator's error
list to an exact `expected_negative_errors` map with `assertEqual`, so rejection
for an unrelated reason fails the test. The asserted reasons match what I
computed independently in the C1 review:

```text
invalid_task_packet.json                    -> $: expected type ['object'], got list
invalid_capability_report.json              -> $: expected type ['object'], got list
invalid_scope_lock.json                     -> $: missing required property active_task
invalid_terminal_packet.json                -> $.validation_result: value is not in enum
invalid_current_turn_execution_receipt.json -> the 11 missing required properties, in order
```

**The `additionalProperties: false` path is now covered without corrupting a
canonical schema.** C1 finding N-4 is closed.
`test_additional_properties_false_rejects_synthetic_extra_property` builds a
throwaway schema in the test body and asserts the exact error
`"$: additional property extra is not allowed"`. No canonical schema was closed
to create coverage, which is precisely what C2-5 required.

**Dependency separation is asserted, not just performed.**
`test_dependency_ids_are_separated_from_dependency_prose` pins
`EXECLIB.MMU.001 → ["EXECLIB.STATETREE.001"]`,
`EXECLIB.READLANE.SOURCELIB.001 → ["EXECLIB.DATELIB.001"]`,
`RuntimeGate.Egress → []`, and requires non-empty `dependency_prose` on all
three. This closes C1 finding N-2.

**The validator has not become a runtime implementation.** It still imports only
`argparse`, `json`, `re`, `sys`, `pathlib`, and `typing`. `route_lane_class_errors`
reads contract JSON and returns strings; it performs no routing, dispatch, gate,
or packet construction. The module docstring still declares it "contract-validation
tooling, not Blu runtime implementation or a general JSON Schema validator."

## No regression of previous corrections

Verified item by item against the reviewed commit. The C2 diff touched only five
files under `contracts/runtime/` — `README.md`, `source_map.json`,
`component_registry.json`, `route_registry.json`, `unresolved_register.json` —
leaving `parity_matrix.json` and all five schemas byte-identical, so no C1
schema or parity repair could regress.

- **Auth and OPSEC route existence** — all three non-slash routes present with
  correct `ingress_step` values and owners; both exclusivity rules still verbatim
  in `one_owner_constraints.rules` (7 rules total, both present).
- **Source-role separation** — `source_roles` map intact; deployment-only guard
  intact; role assertions strengthened.
- **Referenced-but-undefined owners** — 18 components at
  `declared_but_not_defined`, including all six labels C1 added; both catalog
  spellings still separate; both macro identifiers still `render_text: null`.
- **StateTree** — `unresolved_conflict`, `["ALPHA", "ACTIVE"]`, seven sources.
- **PASS provenance** — `/PASS` still absent from
  `unavailable_command_surfaces.values`; `non_live_feature_declarations` still
  carries `literal_slash_stem_declared: false` and the exact source statement.
- **Validator keyword handling** — `SUPPORTED_SCHEMA_KEYWORDS`,
  `ANNOTATION_KEYWORDS`, `SUPPORTED_TYPES`, and the unsupported-keyword and
  unknown-type rejections are unchanged; their tests still pass.
- **Source anchoring** — `source_anchor_errors` unchanged; exact-heading
  matching, single-resolution requirement, and section-scoped locator matching
  all intact, and the new join entry passes them.
- **Persona and Operations boundaries** — untouched by C2. Persona remains
  `model_facing_source`; no doctrine was converted into a rule; the parity matrix
  is unchanged.

Source-map entries grew 83 → 84 (the join record) and unresolved items 27 → 28
(UR-028). Both increments are exactly the intended additions.

## Bookkeeping and terminology

- BC-010-C1 `assignment.md` and `validation.md` status headers changed from
  `active` to `review`; C1 finding N-5 is closed.
- BC-010, BC-010-C1, and BC-010-C2 are all `review` in
  `docs/worklogs/assignments.md`, and every record header under the three
  assignment folders reads `review` except this file, which was correctly left
  `pending` for me.
- Assignment lineage `["BC-010", "BC-010-C1", "BC-010-C2"]` is recorded in
  `contracts/runtime/README.md` front matter and in `source_map.json`,
  `component_registry.json`, `route_registry.json`, and
  `unresolved_register.json`. This closes C1 finding N-6.
- Terminology now distinguishes one GPT deployment instruction from six
  kernel/runtime capsules in `contracts/runtime/README.md` and in the
  `docs/worklogs/assignments.md` standing guardrails.
- No golden file was edited:
  `git diff --exit-code 424f80b -- kernel/golden/v0.22.0` returned exit 0, and I
  recomputed all eight checksums before and after the review commit.
- Protected paths were untouched by C2: `git diff --name-only` across
  `AGENTS.md`, `CLAUDE.md`, `CODEX.md`, `config/`, `docs/sources/`,
  `docs/architecture/`, `kernel/`, and
  `docs/domains/runtime/assignments/BC-010-C1/review.md` returned empty.
- The runtime quartet is updated: `decisions.md` records the successor boundary,
  `worklog.md` records the work, `failures.md` promotes the three required
  reusable lessons (a route name does not prove a lane-class enum value;
  cross-role owner joins must be labeled extraction inference; successor
  decisions must not be projected backward), and `next_steps.md` keeps all three
  assignments in `review` and BC-020/BC-030 unstarted.

## No runtime implementation

Confirmed. The C2 commit changed 19 files: five contract JSON/Markdown files,
the validator, the test module, four C2 records, two C1 record headers, four
runtime-domain documents, the global index, and `MANIFEST.sha256`. The entire
repository still contains exactly two `.py` files —
`tools/validate_runtime_contracts.py` and
`tests/contracts/test_validate_runtime_contracts.py` — both validation tooling,
both standard-library only. No route execution, Auth, OPSEC, persistence,
reminders, Local Mirror, PASS, or Chat/Codex adapter was implemented. The
approved OPSEC pre-ingress restraint exists only as a written decision.

## Validation-evidence assessment

Every reported value was recomputed independently rather than accepted from
Codex's records. All matched.

```text
git status --short                                  -> clean
git rev-parse HEAD                                  -> f8aa77f43b27e0d9d49f4fd23d4f097fa4a262bc (branch base)
git show -s --format=%H 06292ce0...                 -> 06292ce0e2f326ef84988e030c7fe14402192859 (present)
git show -s --format=%H f8aa77f4...                 -> f8aa77f43b27e0d9d49f4fd23d4f097fa4a262bc (present)
git diff --check                                    -> exit 0, no output
git diff --exit-code 06292ce f8aa77f
  -- contracts/runtime tools tests kernel/golden    -> exit 0
git diff --exit-code 424f80b -- kernel/golden/v0.22.0 -> exit 0
python tools/validate_runtime_contracts.py          -> "PASS: runtime contracts and canonical
                                                       fixtures satisfy the supported structural
                                                       subset", exit 0
python -m unittest discover -s tests/contracts
  -p "test_*.py"                                    -> Ran 21 tests, OK, exit 0
PowerShell Get-FileHash SHA256 vs SHA256SUMS        -> GOLDEN_CHECKSUMS=8/8
PowerShell Get-FileHash SHA256 vs MANIFEST.sha256   -> MANIFEST_VERIFIED=125/125 (0 fail, 0 missing)
grep -rn '"lane_class": *"opsec"' contracts/runtime -> no matches
```

`sha256sum` is unavailable on this Windows host; the repository's PowerShell
`Get-FileHash -Algorithm SHA256` equivalent was used, matching the limitation
recorded in `docs/domains/runtime/failures.md`.

The handoff and validation records are accurate. Every claim I could test held:
the removed lane class, UR-028, the extraction-inference labeling, the lane
closure, the dependency and negative-fixture cleanup, the decision recorded only
in project documentation, `Ran 21 tests`, `GOLDEN_CHECKSUMS=8/8`, and
`MANIFEST_VERIFIED=125/125`. The validation record's boundary statement —
"Passing checks prove the recorded structural, fixture, checksum, and Git-diff
conditions only. They do not prove executable runtime behavior, host capability,
behavioral parity, or resolution of UR-028." — is accurate and appropriately
scoped. No overclaim was found in any C2 record.

## Disposition

**approve-with-notes**

The single C1 blocker is fully corrected, and corrected in the most faithful way
available: not by picking a plausible lane, not by widening Exec's enum, and not
by importing the approved successor decision into the extraction, but by
recording that `03_Exec.md` requires a lane class at lock time and does not
declare one. Every additional C1 non-blocking finding (N-1 through N-4, N-5, N-6)
is also closed. The new validator closure and its eight targeted tests make this
class of defect mechanically unrepeatable rather than merely fixed once.

The three substantive notes above are observations about precision and
representation, not defects; none misstates the source and none needs to block
integration.

## Required follow-up

None blocking. Optional, at Blu's or Dad's discretion:

1. **N-1** — Add a `source_locator` to `route.opsec_owner_join` (for example the
   `03_Exec.md` `## §7` line "- OPSEC/clone first-read locks are terminal
   deterministic service routes.") so both join records anchor at line
   precision.
2. **N-2** — If per-dependency provenance is ever wanted, consider a
   `dependency_provenance` marker for IDs resolved from a source *name* rather
   than a declared dependency, which today affects only
   `EXECLIB.READLANE.SOURCELIB.001 → EXECLIB.DATELIB.001`.
3. When BC-020 or a successor-runtime assignment implements the approved OPSEC
   pre-ingress restraint, resolve UR-028 there — in the successor contract, not
   by amending the BC-010 extraction.

Reserved to Blu and Dad: all twenty-eight items in
`contracts/runtime/unresolved_register.json`, including UR-028. This review
resolves none of them. BC-020 and BC-030 should remain unstarted until their
packets are approved and bases named, per `docs/domains/runtime/next_steps.md`.

## Final closure authorization

- Integrated main state before closure: `8a37ae3c62829f16f949f5896d2bef0542721565`
- Authorized by: Dad, Project Owner; Blu, Project Lead
- Assignment status: `done`
- Date: 2026-08-06
- Closure basis: Claude disposition `approve-with-notes`; no blocking findings.
  Non-blocking notes remain preserved in this review record.
