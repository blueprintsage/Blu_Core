# BC-030 — Review Record

status: reviewed
owner: Claude
last_reviewed: 2026-08-10

## Review identity

- Assignment: BC-030 — Local Mirror Continuity Schema and Lifecycle
- Reviewed base: `a5f149355bd68b2aea1695e5f25ec60a2cb88b0c`
- Reviewed work commit: `6812513d10eeb69f1e5b477617ffdccc52e5067b`
- Reviewed metadata/head commit: `4c4ef004aef2d93937de3fdb4bbbdeae4f2d9843`
- Work branch: `bc-030-local-mirror-continuity`
- Review branch: `bc-030-semantic-review`
- Reviewer: Claude
- Review type: independent semantic review, review-only
- Integration commit or merge identity: pending

The exact tree at `4c4ef00` was reviewed. No moving branch tip was substituted.

## Sources compared

Machine-readable contracts:

- `continuity/README.md`
- `continuity/evidence_stages.json`
- `continuity/lifecycle.json`
- `continuity/local_mirror_profile.json`
- `continuity/rehydration.json`
- `continuity/security_evidence.json`
- `continuity/sur007_disposition.json`
- `continuity/schemas/continuity_record.schema.json`
- `continuity/schemas/continuity_receipt.schema.json`
- `continuity/schemas/continuity_query.schema.json`
- `continuity/schemas/continuity_retrieval_result.schema.json`
- `continuity/schemas/continuity_provider_availability.schema.json`

Human-readable specification and records:

- `docs/domains/continuity/local_mirror_continuity.md`
- `docs/domains/continuity/assignments/BC-030/{assignment,handoff,validation}.md`
- `docs/domains/continuity/{decisions,failures,next_steps,worklog}.md`
- `docs/worklogs/assignments.md`, `docs/dev/docs_index.md`

Protected and referenced material:

- `contracts/successor/{component,interface,packet,unresolved}_registry.json`
  (`unresolved_register.json` for SUR-007/SUR-011)
- `config/source_authority.json`
- `kernel/golden/v0.22.0/SHA256SUMS`
- `MANIFEST.sha256`

Tooling:

- `tools/validate_continuity_contracts.py`
- `tests/continuity/test_validate_continuity_contracts.py`

## Findings

### Blocking

None.

No defect was found that violates BC-030 authority, inflates evidence into an
unearned durable-success or protected-authorization claim, expands the successor
architecture, resolves SUR-011, or introduces runtime implementation.

### Non-blocking

#### N1 — The write path has no request contract; `expected_version` has no machine-readable carrier

- Affected: `continuity/lifecycle.json` (`conflict_rule`), `continuity/schemas/**`
- Observed: `lifecycle.json` states "Every mutation after create supplies an
  expected-version value," and `security_evidence.json` requires
  `atomic_expected_version_transition` for protected authorization. BC-030 ships
  a bounded request schema for the read path (`ContinuityQuery`) but no
  corresponding mutation-request schema. `ContinuityReceipt` carries
  `prior_version` and `resulting_version`, but no field binds a receipt to a
  caller-supplied expected version.
- Effect: silent overwrite is forbidden by a guarded normative rule in a
  machine-readable contract file, but the JSON Schema surface cannot express or
  carry the value that makes the rule checkable. Read-path and write-path rigor
  are asymmetric.
- Not blocking because: `lifecycle.json` is a registered contract, the validator
  guards the rule text against removal, and BC-030 is specification-only with
  `implementation_authorized: false`.
- Smallest correction: add a `ContinuityMutationRequest` schema carrying
  `request_id`, `provider_id`, `operation`, `scope`, `record_id`, and a required
  `expected_version` (nullable only for `create`), and add a receipt field
  echoing the requested expected version. Suitable for the implementation packet.

#### N2 — `not_found` retrieval results are not constrained to zero records

- Affected: `continuity/schemas/continuity_retrieval_result.schema.json:41-44`
- Observed: the empty-records constraint applies to `unavailable`, `forbidden`,
  `invalid`, `integrity_failure`, and `failed`. `not_found` is omitted, and the
  embedded `receipt.status` is constrained only when the result status is
  `completed`. A result with `status: not_found`, a populated `records` array,
  and `receipt.status: completed` is schema-valid.
- Effect: an internally incoherent result shape. The distinctions Review
  Question 6 requires are preserved at the status-value level, and rehydration
  remains safe because `rehydration.json` requires both result and receipt
  `completed`, so this does not enable a false durable-success claim.
- Smallest correction: add `not_found` to the empty-records enum, and constrain
  the embedded receipt status to be non-`completed` when the result status is
  non-`completed`.

#### N3 — `availability_probe` is undocumented outside the receipt schema

- Affected: `continuity/schemas/continuity_receipt.schema.json:33-38`,
  `continuity/lifecycle.json:5`, `docs/domains/continuity/local_mirror_continuity.md`
- Observed: `availability_probe` appears in the receipt `operation` and
  `requested_action` enums but not in `lifecycle.json:operation_values`, not in
  the availability schema's `supported_operations`, not in `lifecycle.json`
  transitions, and nowhere in the prose specification. The divergence is
  deliberate in the validator (`RECEIPT_OPERATIONS = OPERATIONS | {"availability_probe"}`),
  so it is intentional rather than accidental, but it is unexplained.
- Smallest correction: one sentence in `continuity/README.md` or
  `lifecycle.json` recording that `availability_probe` is a receipt-only
  observation operation with no record-state transition.

#### N4 — Receipt action-binding equality is normative prose only

- Affected: `continuity/schemas/continuity_receipt.schema.json:137`
- Observed: `x-blu-action-binding-rule` requires `requested_action` to equal
  `operation`, but no schema constraint enforces it and no test exercises a
  receipt instance with mismatched values. A receipt with `operation: create`
  and `requested_action: retrieve` is schema-valid.
- Assessment: the receipt is nonetheless strongly bound in structure. All of
  `receipt_id`, `request_id`, `provider_id`, `record_id`, `scope`,
  `prior_version`, `resulting_version`, and `related_record_refs` are required,
  so a completed receipt names exactly one operation instance and cannot be
  read as evidence for a different request, provider, record, scope, or
  resulting version without contradicting its own fields. The gap is
  enforcement mechanism, not contract intent.
- Smallest correction: express the equality as an eight-branch `allOf` of
  `if`/`then` pairs, or record it explicitly as a consumer-side obligation.

#### N5 — The absolute-path prohibition is unenforced by pattern

- Affected: `continuity/schemas/continuity_record.schema.json:78-82`,
  `continuity/local_mirror_profile.json:39-44`
- Observed: `provider_native_ref` forbids machine-specific absolute paths in its
  `description` and in the profile's `forbidden_references` list, but carries no
  `pattern` constraint. A drive-letter, UNC, POSIX-absolute, or `file:` value
  is schema-valid.
- Assessment: the portability contract itself is sound. `relocation_rule`
  correctly requires that moving the provider root change neither `record_id`,
  `version_id`, scope, lineage, nor normalized corpus-relative references, and
  the authoritative root is explicitly held outside portable record identity.
- Smallest correction: add a negative `pattern` to `provider_native_ref` and
  `payload_ref.locator` when `kind` is `corpus_relative`.

#### N6 — Non-completed receipts leave mutation-outcome fields unconstrained

- Affected: `continuity/schemas/continuity_receipt.schema.json:89-135`
- Observed: the conditional blocks tighten fields only when `status: completed`.
  A receipt with `status: conflict` may still carry
  `supersession_result: recorded` and a `resulting_version`, though
  `lifecycle.json` states no state change occurs. The prose and the failure rule
  govern; the schema does not.
- Effect: contradictory, not permissive — the `status` value still decides, and
  `x-blu-failure-rule` is guarded by the validator.
- Smallest correction: for non-`completed` statuses, constrain
  `resulting_version` to `null` and `supersession_result` to
  `not_applicable`/`not_recorded`/`conflict`.

#### N7 — Two validator guards are unreachable under test

- Affected: `tests/continuity/test_validate_continuity_contracts.py:24-41`
- Observed: the fixture copies files into a temporary root with no `.git`
  directory. Both `_validate_git_scope` and `_validate_manifest_coverage` return
  early in that condition, so protected-path scope bleed, disallowed Python,
  PASS/SkillForge bleed, LM Studio path changes, and manifest coverage are
  exercised by no test. They do execute on a real run of the validator, which I
  reproduced against the repository, so the guards work — they are simply not
  regression-protected.
- Smallest correction: initialize a throwaway Git repository in the fixture, or
  add focused unit tests for the two helpers.

#### N8 — Manifest coverage checks paths, not digests

- Affected: `tools/validate_continuity_contracts.py:177-204`
- Observed: `_validate_manifest_coverage` compares the manifest path set against
  `git ls-files` and detects duplicates, but never recomputes SHA-256. Content
  drift in an already-listed file would pass. I verified the digests separately
  (see Validation review); they are correct at the reviewed head.
- Smallest correction: recompute and compare digests, reading content in a
  line-ending-normalized form (see N11).

#### N9 — SUR-007 register reconciliation remains outstanding

- Affected: `continuity/sur007_disposition.json`,
  `docs/domains/continuity/decisions.md`,
  `contracts/successor/unresolved_register.json`
- Observed: BC-030 declares SUR-007 `resolved_at_generic_continuity_contract_level`
  and `decisions.md` records it as resolved at the generic specification level,
  while the canonical register still carries SUR-007 with
  `blocking_for_BC030: true` and `what_future_assignment_can_resolve_it: BC-030`.
- Assessment: correct behavior, not a defect. `contracts/successor/**` is a
  protected tree under the BC-020 regression boundary and BC-030 rightly left it
  byte-unchanged. The disposition is explicitly scoped to the contract level with
  `implementation_authorized: false`, so it does not overclaim.
- Required at closure: an authorized step must reconcile the register, or record
  that SUR-007 stays open pending the implementation packet. Flagged so the
  divergence is not read later as an undeclared contradiction.

#### N10 — Stale push-status line in the handoff

- Affected: `docs/domains/continuity/assignments/BC-030/handoff.md:13`
- Observed: "Push status: pending at metadata commit; final Git receipt
  required," while `origin/bc-030-local-mirror-continuity` exists.
- Assessment: bookkeeping only. It creates no semantic or audit defect — it
  understates rather than overstates a Git receipt, which is the safe direction.
  No rework warranted.

#### N11 — Manifest verification is line-ending sensitive (audit note)

- Observed: verifying `MANIFEST.sha256` against Windows working-tree bytes under
  `core.autocrlf=true` reports 117 of 239 mismatches. Verifying the same manifest
  against committed blob bytes reports 239 entries, 0 missing, 0 mismatched.
  `.gitattributes` sets `* text=auto`, and `validation.md:96-97` correctly
  records that the manifest was generated from staged Git blob bytes.
- Assessment: not a defect. Recorded so a future reviewer on a CRLF checkout does
  not mistake the artifact for manifest corruption.

### Preserved unresolved declarations

- **SUR-011 remains unresolved.** `security_evidence.json:49` and
  `sur007_disposition.json:12` both carry
  `sur011_state: "unresolved_security_policy_input"`, and
  `sur011_not_decided` explicitly disclaims unrelated-turn behavior, retry
  policy and attempt values, lockout/backoff, cancellation/reset, and
  new-request-after-exhaustion. `local_mirror_continuity.md:158-159` repeats the
  disclaimer. I found no contract that indirectly chooses any of those policies:
  BC-030 defines no attempt counter, no timer, no exhaustion transition, and no
  pending-interaction disposition. The validator enforces the unresolved state in
  two files.
- **Protected durable authorization remains unavailable.**
  `security_evidence.json` sets `ordinary_continuity_receipt_sufficient: false`,
  `model_or_conversation_fallback_allowed: false`, requires all ten protected
  properties, and fails closed on any absent, stale, mismatched, rolled-back,
  replayed, corrupted, or unverified property. The Local Mirror reference is
  dispositioned `insufficient_evidence` with its missing properties enumerated.
  `pending_authorization_state_rule` correctly states that durable storage of
  `PendingAuthorizationState` does not make the state active, trusted,
  resumable, or authorized, leaving that decision to Security Restraint and the
  Authorization Evaluator.
- **No implementation is authorized.** `implementation_authorized: false`;
  provider technology, durability/crash-consistency mechanism, security model,
  retention/backup operations, and deployment bindings remain future inputs.

## Validation review

### Independently reproduced

All seven suites were executed directly at the reviewed head. Counts match the
reported figures exactly:

```text
runtime contracts:        Ran 21, OK
viability:                Ran  9, OK
historical archives:      Ran 12, OK
historical archaeology:   Ran 18, OK
successor kernel:         Ran 40, OK
host adapters:            Ran 34, OK
continuity:               Ran 34, OK
python tools/validate_continuity_contracts.py -> passed
```

Structural claims independently confirmed:

```text
components 7   security_restraint, authorization_evaluator, turn_controller,
               validation_egress, model_execution_boundary,
               host_adapter_boundary, continuity_provider_boundary
packets    8   TurnRequest, SecurityDecision, CapabilityReport,
               AuthorizationResult, ControlDecision, ServiceExchange,
               ValidationResult, TerminalPacket
interfaces 9   IF-CONTINUITY-PROVIDER present exactly once,
               ServiceExchange request and response, no invented packet
lifetimes      none, turn, host_session, durable_external (exact set)
continuity schemas 5; continuity tree files 12, all .json/.md
changed files 26; changed Python 2 (validator and tests only)
protected-path diff from base (kernel/golden, contracts/runtime,
  contracts/successor, docs/architecture, adapters,
  config/source_authority.json): empty
implementation roots (src, runtime, blu_core, providers, local_mirror,
  lm_studio, pass, skillforge): none present
golden CTS: 8/8 verified
MANIFEST.sha256: 239 entries, 0 missing, 0 extra, 0 mismatched
  against committed blob bytes (see N11)
Local Mirror archive SHA-256 matches config/source_authority.json
```

### Assessment of validator adequacy

The validator is genuinely useful and correctly scoped, but its enforcement
model should be understood precisely.

**What it enforces structurally and well.** Counts, exact vocabulary sets
(lifetimes, record statuses, receipt statuses, receipt operations, evidence
stages, availability states, protected-authorization properties), required-field
sets, the interface/packet binding, `PendingAuthorizationState` not becoming a
packet, the rehydration sequence as an ordered list, the query `limit` bound,
pinned archive identity, boolean flags such as `bare_session_allowed`,
`implementation_authorized`, `ordinary_continuity_receipt_sufficient`, and
`sur011_state`, plus golden checksums, exact-base protected-path isolation,
disallowed Python, and absence of implementation trees. These are real
constraints on real values.

**What it enforces as text presence.** A large share of the semantic guarantees
— durable success, model boundary, conflict handling, history/no-deletion,
corruption behavior, scope merging, staging, availability truth, action binding,
conformance, and overclaim limits — are checked with `_contains_all`, a
lowercased substring test over prose strings. This meaningfully rejects the
tested defect classes as they are actually mutated in the tests: each negative
test replaces the rule with a genuinely wrong rule ("Use last writer wins",
"Configured means available", "Delete old versions", "Model confidence is
evidence"), and the check fires. It is not merely syntactic — the tests encode
real inversions of meaning, not cosmetic edits.

But the mechanism is defeatable by a rule that retains the keywords while
negating the meaning. `_contains_all` on `conflict_rule` requires the tokens
"expected-version", "conflict", "no mutation", "silent overwrite", "forbidden";
a rewrite that keeps those tokens in a permissive sentence would pass. The
guard is therefore best characterized as a **contract-text regression guard**:
strong against deletion, weakening-by-removal, and casual rewording; weak
against adversarial rewording.

**The principal untested class: instance-level conformance.** BC-030 ships five
JSON Schemas but the suite never validates a single document instance against
them, and no `jsonschema` runtime is present. Every conditional block that does
the real semantic work — the completed-status tightening, the mutation-completed
requirements, the supersede `minItems: 2` reciprocity requirement, the
empty-records constraint, the availability evidence requirement — is entirely
unexercised. This departs from the pattern the repository already uses
elsewhere: `tests/contracts/fixtures/` carries `invalid_*.json` negative
instances. The handoff discloses this honestly as a known risk
(`handoff.md:60-62`), which is why it is recorded here as a gap rather than an
overclaim. It is the reason findings N2, N4, and N6 survived to this review: a
single valid/invalid fixture pair per schema would likely have surfaced all
three.

**On the `validation.md` negative-test claims.** The listed rejections are
accurate as descriptions of what the tests do, with one nuance worth recording:
"silent conflict overwrite", "history deletion", and "corruption repair" are
rejected at the level of the governing rule text, not at the level of a
provider instance attempting the act. `validation.md:146-152` already draws this
boundary correctly and does not claim runtime or provider proof.

### Question-by-question outcome

| # | Area | Outcome |
|---|------|---------|
| 1 | Provider boundary | Pass — candidate binding only; no component, memory service, MMU, session manager, or model-owned memory |
| 2 | Evidence ladder | Pass — 13 finite stages, `no_implicit_promotion`, all six non-implication pairs preserved |
| 3 | ContinuityReceipt | Pass with N4, N6 — strong structural operation binding; enforcement partly prose |
| 4 | Identity and versioning | Pass — `record_id`/`version_id` cleanly separated; update preserves lineage, supersede may create a linked successor lineage, both stated in `lifecycle.json:9` and the prose; no delete/destroy anywhere |
| 5 | Concurrency | Pass with N1 — silent overwrite forbidden normatively; no machine-readable carrier for expected version |
| 6 | Retrieval and scope | Pass with N2 — one provider/namespace/scope, finite selector, bounded limit, provenance preserved |
| 7 | Availability | Pass — `available`/`degraded` require `evidence_ref` and non-empty `supported_operations`; the four states are adequate and consistently used across three artifacts |
| 8 | Integrity | Pass — quarantine, no repair, no inference of correct version, no promotion of history to current, recovery is an explicit receipted operation |
| 9 | Evidence restraint | Pass — no source-inflated claim found; the eight `not_proven_by_reference` entries and the prose disclaimer are mutually consistent and cover every item in the assignment's restraint list |
| 10 | Portability | Pass with N5 — root held outside record identity; relocation rule correct |
| 11 | Rehydration | Pass — seven-step ordered gate; success requires availability, `completed` result, matching `completed` receipt, validation, bounded staging |
| 12 | Protected authorization | Pass — ten required properties, fail-closed, no fallback, reference dispositioned insufficient |
| 13 | SUR-011 | Pass — unresolved in two files; no indirect policy choice found |
| 14 | One Blu / cross-host | Pass — host- and model-neutral; no separate Python memory canon; LM Studio appears only as a Model Execution Boundary statement and a prohibition |
| 15 | No runtime implementation | Pass — 2 Python files, both validator/tests; `continuity/` is `.json`/`.md` only |
| 16 | Human/machine alignment | Pass with N3 — one undocumented vocabulary item; no contradiction found |
| 17 | Validator adequacy | Adequate with N7, N8 and the instance-conformance gap above |
| 18 | Regression / protected boundaries | Pass — protected diff empty, golden 8/8, 7/8/9 intact, current CTS unchanged |

## Disposition

`approve-with-notes`

BC-030 is a disciplined specification-only deliverable. It keeps Local Mirror as
a candidate binding behind the existing Generic Continuity Provider Boundary,
preserves the seven/eight/nine successor graph and the four-value lifetime
vocabulary exactly, refuses every premature promotion in the evidence ladder,
holds protected authorization unavailable, preserves SUR-011, and introduces no
runtime, provider, or LM Studio code. Its treatment of the supplied Local Mirror
reference is notably restrained: the corpus is mapped for structural evidence
only and explicitly disclaimed for durability, atomicity, receipts, crash
consistency, security, availability, and protected-authorization capability.

Eleven non-blocking notes are recorded above. None blocks merge. The substantive
ones (N1, N2, N6) are schema-tightening opportunities on a contract that is not
yet implemented, and the enforcement gaps (N4, N5, N7, N8) are all mitigations
rather than defects in the specified semantics.

## Required follow-up

Not blocking, and none is authorized by this review:

1. Carry N1, N2, N4, N5, and N6 into the implementation packet as schema
   tightenings, with N1 (mutation-request contract carrying `expected_version`)
   as the highest priority.
2. Add instance-level conformance fixtures for the five schemas, following the
   existing `tests/contracts/fixtures/` pattern, and select the schema runtime
   the handoff defers.
3. Close the N7 and N8 validator gaps.
4. Reconcile SUR-007 in `contracts/successor/unresolved_register.json` under
   authorized closure, or record that it stays open pending implementation (N9).
5. Correct the stale push-status line at closure (N10). Cosmetic.

## Final status authorization

- Authorized by: pending — Dad retains merge authority; Blu retains integration
  and closure authorization
- Assignment status: reviewed, not merged, not `done`
- Date: 2026-08-10
