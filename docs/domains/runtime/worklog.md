# Runtime Worklog

status: active
owner: docs/domains/runtime
last_reviewed: 2026-08-08

## 2026-08-05 — Bootstrap

- Created the domain continuity lane.
- No implementation work has begun.

## 2026-08-05 — BC-010 runtime contract extraction

### What changed

- Extracted downstream machine-readable contracts for the v0.22.0 golden
  Markdown runtime under `contracts/runtime/`.
- Added source provenance, component and route registries, five JSON Schemas, a
  behavioral parity matrix, and an unresolved register.
- Added standard-library-only validation tooling and contract fixtures/tests.
- Added the extracted contract set to the documentation index.
- Did not add runtime behavior or modify the golden kernel.

### What was tested or reviewed

- Read all seven authoritative golden runtime files in full.
- Ran `python tools/validate_runtime_contracts.py`.
- Ran `python -m unittest discover -s tests/contracts -p "test_*.py"`.
- The initial validator and four tests passed.
- Final structural validation passed.
- Final unit validation passed: 4 tests.
- `git diff --check` passed (Git reported only expected LF-to-CRLF working-copy
  warnings for modified Markdown files).
- `git diff --exit-code 7aed76e -- kernel/golden/v0.22.0` passed.
- PowerShell SHA-256 verification passed for all seven Markdown files and the
  source ZIP listed in `SHA256SUMS`.
- `git merge-base --is-ancestor 7aed76e HEAD` passed at pre-commit HEAD
  `3c421914d2b449f63f9b7ba73e24cc59539c1c3b`.
- The contract set contains 41 registry components, 6 live slash stems, 69
  source-map entries, 22 unresolved items, 12 parity requirements, and 34
  parity cases.

### What worked

- Every JSON file parsed.
- Source-map targets and sections resolved.
- Component IDs were unique within namespace after repeated StateTree
  declarations were represented by one unresolved registry identity.
- Every live public command stem had one owner.
- The validator failed in tests when a required contract was removed or JSON
  was malformed.

### What failed

- The host did not provide `sha256sum`; an equivalent PowerShell
  `Get-FileHash -Algorithm SHA256` check was used successfully.
- The optional third-party `jsonschema` package was not installed. Validation
  remains dependency-free and covers the JSON Schema subset used by BC-010.

### Known risks

- Several mandatory runtime owners are referenced but not defined by the seven
  golden files; they remain `declared_but_not_defined`.
- StateTree has conflicting `ALPHA` and `ACTIVE` declarations.
- The `/memory` route uses `lane_class=workflow`, which is absent from Exec's
  declared lane-class list.
- Schema fields for task packets and capability reports are not declared by the
  golden source, so those schemas intentionally assert object shape only.
- Contract/schema validity is not behavioral parity or host-capability proof.
- The assignment packet requires one work commit and also requires that exact
  commit ID to be stored inside `docs/worklogs/assignments.md` in that same
  commit. A Git commit cannot contain its own hash because changing the file
  changes the tree and therefore the hash.

### Next safe step

- Request Claude's read-only semantic review against the seven golden files at
  work commit `40138b6e16f28c01904aae97158878468ee47ad0`.

### Files changed

- `contracts/runtime/**`
- `tools/validate_runtime_contracts.py`
- `tests/contracts/**`
- `docs/dev/docs_index.md`
- `docs/domains/runtime/worklog.md`
- `docs/domains/runtime/failures.md`
- `docs/domains/runtime/next_steps.md`
- `docs/worklogs/assignments.md`

### Commit or patch identity

- Work branch: `bc-010-runtime-contracts`
- Work commit: `40138b6e16f28c01904aae97158878468ee47ad0`
- Record commit: this authorized metadata-only follow-up; its exact SHA is
  reported externally because a commit cannot contain its own final hash

## 2026-08-05 — BC-010-C1 runtime contract extraction corrections

### What changed

- Separated the deployment instruction from the six kernel/runtime capsules in
  source mapping and documentation.
- Added the three missing non-slash routes and both deployment-level exclusive
  dispatch constraints.
- Added omitted referenced components and declared macro identifiers without
  inventing implementations, stable IDs, or render text.
- Replaced fragment-only source citations with exact Markdown heading anchors
  plus scoped exact locators where a file lacks doctrine subheadings.
- Corrected PASS, dependency, StateTree, schema-closure, parity-provenance, and
  extraction-inference representations.
- Replaced the permissive schema checker with a strict documented subset
  validator and canonical positive/negative fixture validation.
- Backfilled BC-010 assignment and validation records and created the approved
  BC-010-C1 assignment quartet.
- Restored runtime-contract discovery in the documentation index.

### What was tested or reviewed

- `python tools/validate_runtime_contracts.py` passed during implementation.
- `python -m unittest discover -s tests/contracts -p "test_*.py"` passed 15
  tests during implementation.
- Final Git, checksum, manifest, Python-version, and dependency receipts are in
  `assignments/BC-010-C1/validation.md`.

### What worked

- Every source-map entry resolves to one declared role and one exact heading.
- Unsupported schema keywords and unknown types fail clearly.
- All five positive fixtures pass and all five negative fixtures fail.
- StateTree remains `unresolved_conflict` with `ALPHA` and `ACTIVE` preserved.

### What failed

- No implementation path failed. The pre-existing untracked
  `.claude/settings.local.json` remains outside assignment scope and is not
  committed.

### Known risks

- Structural validation is not behavioral parity or runtime proof.
- Referenced components and macro identifiers remain undefined.
- Claude's second semantic review remains required.

### Next safe step

- Review the repair work commit read-only against the CTS source set, then let
  Blu or Dad decide integration. Do not begin BC-020 or BC-030.

### Commit or patch identity

- Repair work commit: recorded by the authorized metadata-only follow-up.
- Metadata record commit: reported externally after creation.

## 2026-08-06 — BC-010-C2 OPSEC route classification repair

### What changed

- Replaced the two unsupported `opsec` route lane values with null lane classes,
  explicit undeclared status, and UR-028.
- Marked the cross-role OPSEC owner join as extraction inference and added a
  dedicated source-map join entry preserving both source roles.
- Added route lane-class closure validation for Exec-declared lanes,
  unresolved route-table-only values, and source-proven null lanes.
- Separated component IDs from dependency prose in the three records identified
  by Claude's C1 review.
- Strengthened negative fixture reasons and added synthetic object-closure
  coverage.
- Recorded assignment lineage, the approved successor-runtime Auth/OPSEC
  decision, C2 assignment evidence, and C1 status cleanup.
- Did not modify the golden CTS source or implement runtime behavior.

### What was tested or reviewed

- Final exact command and checksum receipts are recorded in
  `assignments/BC-010-C2/validation.md`.

### What worked

- The validator rejects `opsec` and arbitrary invented lane classes.
- Declared `auth`, unresolved route-table-only `workflow`, and the two
  source-proven null OPSEC lane classes validate.
- All five canonical negative fixtures are asserted against their intended
  failure reasons.

### Known risks

- Contract validation remains structural and does not prove runtime behavior.
- The successor OPSEC decision is deliberately not represented as golden CTS
  provenance.

### Next safe step

- Claude performs a read-only semantic review of the C2 repair work commit;
  Blu or Dad decides integration. Do not merge or mark BC-010, BC-010-C1, or
  BC-010-C2 done.

### Commit or patch identity

- Exact base: `424f80b254a02f057da6c82db5230377076fc415`
- Branch: `bc-010-c2-opsec-route-repair`
- Repair work commit: recorded by the authorized metadata-only follow-up.

## 2026-08-06 — BC-010 lineage closed

- Dad and Blu authorized final closure.
- BC-010, BC-010-C1, and BC-010-C2 moved from review to done.
- Claude's final disposition was approve-with-notes with no blocking findings.
- Non-blocking notes remain preserved in the BC-010-C2 review record.
- Integrated reviewed state before closure:
  `8a37ae3c62829f16f949f5896d2bef0542721565`.
- No runtime contracts, validator code, tests, or golden sources changed.
+
## 2026-08-06 — BC-015 runtime viability audit

### What changed

- Created an evidence register, 30-record viability matrix, 24-probe safe host
  catalog, audit guide, and audit report under
  `docs/domains/runtime/viability/`.
- Covered all 47 component entries, 76 normalized route-surface entries, 12
  parity requirements, and 28 unresolved items.
- Classified no capability as `live_and_stable`; preserved Dad and Blu's
  Auth, OPSEC, and Persona warmth observations as
  `live_but_nondeterministic_or_host_dependent`.
- Kept current OPSEC behavior separate from the approved successor pre-ingress
  restraint.
- Recorded the v0.15.2 historical archive as unavailable without reconstructing
  its contents.
- Added standard-library-only validation and nine required negative tests.
- Added the BC-015 assignment quartet and documentation discovery.
- Did not implement runtime behavior or modify golden sources, runtime
  contracts, architecture, configuration, or runtime decisions.

### What was tested or reviewed

- Verified the exact base and clean startup state.
- Read the required governance, architecture, source, runtime continuity,
  extracted contract, prior review, and golden CTS inputs.
- Verified all eight golden checksum entries before audit work.
- `python tools/validate_viability_audit.py` passed.
- `python -m unittest discover -s tests/viability -p "test_*.py"` passed nine
  tests during implementation.
- Final Git, manifest, protected-path, contract, checksum, and unit-test
  receipts are recorded in `assignments/BC-015/validation.md`.

### What worked

- Mechanical coverage is complete and exact.
- Evidence and successor provenance remain separate.
- The validator rejects unknown classifications, missing evidence, incomplete
  coverage, duplicate IDs, invalid dispositions, declaration-only stable
  claims, incomplete historical evidence, and successor-as-golden projection.

### What failed or remains unavailable

- The historical v0.15.2 archive was unavailable.
- No current Blu GPT-host probe was executed; all 24 probes remain for Dad or
  Blu.

### Known risks

- Grouped records must not be interpreted as approval of current component
  topology.
- Proposed dispositions remain non-final.
- Auth and OPSEC details remain protected and require security-authorized
  specification work.

### Next safe step

- Claude reviews the BC-015 audit work commit read-only; Dad and Blu decide
  probe execution, historical-source reopening, and any successor
  specification assignment.

### Commit or patch identity

- Exact base: `4b51427b361283715a24110409e031e191b52452`
- Branch: `bc-015-runtime-viability-audit`
- Audit work commit: `9936cc4be2f7f397deebccdf7400e8b7b774df08`
- Metadata record commit: reported externally because a commit cannot contain
  its own final SHA

## 2026-08-06 — BC-015 runtime viability audit closed

- Dad and Blu authorized final closure of BC-015.
- Claude's semantic-review disposition remains `approve-with-notes`; all nine
  non-blocking findings are preserved and no blocking findings remained.
- The audit classified current viability and did not implement a runtime.
- Historical evidence was unavailable during BC-015. The broader historical
  archive source is introduced only through the separate BC-016 source-
  integration assignment and does not retroactively change the BC-015 record.
- Integrated main state before closure:
  `1f07333457b18895fbb04d5c776e3259d870f2f6`.

## 2026-08-06 — BC-016 historical archive inventory integration

### What changed

- Integrated 249 path-sanitized historical source records: 244 archives, three
  branch-root Markdown file sets, and two historical source folders.
- Independently verified the stable outer `Kernel.zip` receipt and confirmed
  all 279 snapshot payload files match the live historical root by relative
  path and SHA-256.
- Added two exact shared-SHA duplicate groups, 500 reconciliation entries, and
  eight representative milestones covering all requested structural eras.
- Added standard-library-only static validation and twelve tests.
- Preserved the current CTS authority boundary and imported no archive bytes.

### What was tested or reviewed

- Verified external JSON/CSV agreement and consumed all four discovery outputs.
- Recomputed live archive/file-set identities and compared them with the stable
  snapshot.
- Ran the historical inventory validator and twelve tests successfully during
  implementation; final full-repository receipts are in
  `assignments/BC-016/validation.md`.

### What worked

- All local paths were converted to approved source-root aliases plus relative
  paths.
- Snapshot, live root, and discovery identities remain distinct and explicit.
- Exact duplicate grouping now requires one shared canonical SHA-256.
- Two ambiguous external short-date parses were rejected rather than silently
  accepted.

### What failed or remains unavailable

- Seven Deflate64 archives cannot be decompressed by installed readers. Their
  central directories and archive hashes are available; integrity is
  `not_tested`.
- No historical behavior was executed or compared.

### Known risks and next safe step

- Marker prominence and implementation-style Markdown can be mistaken for
  behavioral proof; BC-017 must not make that inference.
- Claude performs a read-only semantic review of the BC-016 inventory work
  commit. Do not begin archaeology, BC-020, BC-030, or Python implementation.

### Commit or patch identity

- Exact base: `fdb6c7e150d3717172e08a1bc349a428187df45a`
- Branch: `bc-016-historical-archive-inventory`
- Inventory work commit: recorded by the authorized metadata-only follow-up.

## 2026-08-06 — BC-016 historical archive inventory closed

- Dad and Blu authorized final closure after Claude's review was integrated.
- Claude's disposition is `approve-with-notes`; no blocking findings remained,
  and BC-016 moved to `done`.
- All NB-1 through NB-10 remain preserved in the review record and carried
  forward under the runtime next-step boundaries.
- Inventory identities and the immutable current CTS authority boundary remain
  unchanged.
- No archive import, behavioral archaeology, or runtime implementation occurred
  during review integration or closure.

## 2026-08-07 — BC-017 historical behavioral archaeology

### What changed

- Re-derived 16 available version families and preserved explicit gaps.
- Selected readable family boundaries and focused change-point drilldowns.
- Separated current truth, owner observations, archive evidence, inference, and
  successor recommendations in a sanitized evidence register and report.
- Added a behavior-centered recovery matrix and transition map.
- Corrected BC-016 NB-1 and NB-4 without broadening the prior assignment.
- Added evidence-integrity validation and focused negative tests.

### What was tested or reviewed

- Checked canonical archive-ID resolution, path sanitization, evidence labels,
  recovery vocabulary, Faithfulness shipping status, payload exclusion, review
  state, and golden checksums.
- Re-ran the existing BC-016 inventory validator and tests after its two narrow
  evidence corrections.
- No historical behavior was executed; no Markdown declaration was treated as
  runtime telemetry.

### What worked

- Boundary-first analysis exposed Exec emergence, School's explicit state
  model, MMU introduction, reminder/time contracts, mega-Exec compensation, and
  v0.21 service decomposition.
- The archive evidence supports recovery of teaching/Persona guidance and thin
  deterministic contracts, not historical module restoration.

### What failed or remains unavailable

- Sixty-three members in seven Deflate64 archives remain unreadable.
- v0.4 boundary chronology, the v0.8 opening, durable host persistence,
  autonomous wake, and the Kiddo incident mechanism remain unproven.

### Known risks and next safe step

- Historical declarations may still be mistaken for working runtime behavior;
  the source-class labels and validator are mandatory safeguards.
- Claude performs a separate read-only semantic review. Dad and Blu decide
  integration. Do not start successor design, BC-018, BC-020, or BC-030.

## 2026-08-07 — BC-017-C1 archaeology review corrections

### What changed

- Removed systematic leading diff markers from the archaeology README and
  corrected its validator/test reproduction commands.
- Corrected the direct mega-Exec-to-contracted-Exec event from v0.20 to its
  evidenced v0.16.0 family.
- Kept later v0.20/v0.21 restructuring distinct and disclosed BC-016's
  different v0.21 structural-milestone framing.
- Preserved Claude's review and all non-blocking notes.

### What was tested or reviewed

- Re-ran all required repository validator/test suites, canonical manifest
  verification, golden checksums, protected-path checks, and the three manual
  acceptance checks.

### Known risks and next safe step

- The correction resolves record-production blockers only; it does not close
  BC-017 or convert green validation into semantic proof.
- Claude may perform a separately authorized read-only re-review of BC-017-C1.
  Dad and Blu decide integration and closure.

## 2026-08-08 — BC-017 and BC-017-C1 closed

### What changed

- Dad and Blu authorized final closure of BC-017 and BC-017-C1.
- The global assignment index and both assignment records moved to `done`.
- Claude's original `return-for-correction` review remains intact as audit
  history; C1 resolved B-01, B-02, and B-03.
- Claude's final C1 re-review at
  `bea9463f0dbbae1c3944c5f44a7843c757d7f0bb` remains
  `approve-with-notes` with zero blocking findings.
- The manifest was regenerated after the final review record and closure
  metadata changed.

### What was tested or reviewed

- Re-ran all four repository validator and unit-test suites.
- Verified canonical manifest bytes, all eight golden CTS checksums, protected
  paths, archive exclusion, publication safety, and PASS/SkillForge isolation.
- Exact commands and results are recorded in the BC-017 and BC-017-C1
  validation records.

### Known risks and next safe step

- All non-blocking archaeology-quality notes remain preserved; none is a
  closure blocker or an approved successor requirement.
- No assignment is currently eligible to start. BC-020 and BC-030 remain
  `spec-needed` and were not started.
- No archaeology, successor design, Python runtime, protected-source change, or
  modern PASS/SkillForge work occurred during closure.

### Commit identity

- Closure base: `b88902d997685057ee0e76709df7117f8a83f295`.
- Branch: `bc-017-closure`.
- Substantive closure commit:
  `b0182581c16bbb4dbeced715ae6e35bcee8bf097`.

## 2026-08-08 — BC-018 successor kernel boundary specification

### What changed

- Specified one seven-node successor graph: four deterministic core components,
  plus model-execution, generic host-adapter, and generic continuity-provider
  boundaries.
- Classified 37 required behaviors, decomposed Exec, defined eight packets,
  nine generic interfaces, six statuses, state lifetimes, source-grounding
  modes, and a dependency-ordered migration plan.
- Preserved OPSEC before ingress, bounded Auth to explicit evidence, and kept
  Persona, teaching, host services, and persistence in their proper authority
  domains.
- Rejected mega-Exec, School Engine, legacy PASS, dedicated Mood/MMU services,
  and the historical Faithfulness object model.
- Added machine-readable traceability and unresolved registers plus a
  standard-library design validator and negative tests.
- Created the BC-018 assignment quartet and marked the assignment `review`.

### What was tested or reviewed

- Exact command and result receipts are recorded in
  `assignments/BC-018/validation.md`.
- Validation covers all prior repository validators/tests, the BC-018 validator
  and negative suite, canonical manifest, golden checksums, and protected paths.

### What worked

- Every deterministic responsibility has one exclusive owner.
- Capability, time, scheduling, artifacts, and persistence require provider
  evidence rather than declaration.
- BC-020 and BC-030 both receive generic plug-in contracts and are
  `ready_for_spec` without being started.

### What failed or remains unavailable

- No runtime behavior, host adapter, scheduling, persistence, Auth, or OPSEC
  implementation exists.
- Protected Auth/OPSEC policy details, initial route catalog, semantic source
  verification, host receipt capabilities, and Local Mirror lifecycle remain
  explicit future questions.

### Known risks and next safe step

- Structured contracts can still be mistaken for execution; the design labels
  all components as specifiable, not implemented.
- Claude performs independent semantic review of the substantive work commit.
  Dad and Blu decide integration. Do not begin BC-020, BC-030, or runtime
  implementation.

### Commit identity

- Exact base: `a5e68b3189c60e2d5b8acbe8a212d69b720dec58`
- Branch: `bc-018-successor-kernel-boundary-spec`
- Substantive work commit: `a87e7d7ea57688212c7c8461b5630c6ddb55a00f`

## 2026-08-08 — BC-018-C1 pre-review terminal-authority correction

### What changed

- Defined successful host-session binding and unavailable binding as mutually
  exclusive Turn N terminal outcomes.
- Kept `SecurityDecision` at `PASS`, `BLOCK`, and `ASK`; provider-caused
  `UNAVAILABLE` is selected by Validation and Egress under the originating
  `SecurityDecision` before any `ControlDecision` exists.
- Made unbound proposed pending state inactive, non-resumable, and permanently
  non-correlatable by future host events.
- Updated packet, interface, error, architecture, validator, assignment, and
  continuity surfaces without changing the seven-component/eight-packet design.
- Added four focused negative tests while preserving the existing 35.

### Validation and next step

- Exact final suite, manifest, golden, and protected-path receipts are appended
  to `assignments/BC-018-C1/validation.md`.
- Claude may perform the separately authorized semantic re-review only after
  this correction is committed and pushed. Do not begin BC-020, BC-030, or
  runtime implementation.

### Commit identity

- Correction base: `b1e0f5c7ce3fddd7d71f6b2fa8050b0b55875b3c`
- Substantive correction commit: `311c572f3a28fe4e1cca04b75856faae3cfd6c60`

## 2026-08-08 — BC-018 pre-review contract correction

### What changed

- Corrected `TurnRequest` ownership so only Turn Controller produces it after a
  passing SecurityDecision; Host Adapter now owns only raw host-event
  translation.
- Defined one bounded pre-ingress Auth loop: safe ASK, explicit evidence,
  separate Auth evaluation, result returned to OPSEC, and PASS required before
  ordinary routing.
- Aligned components, packets, interfaces, traceability, graph, normative flow,
  boundary text, migration notes, and runtime decisions.
- Added focused validator invariants and four negative tests without changing
  the seven-component design or eight-packet set.

### What was tested or reviewed

- Exact final commands and results are recorded in
  `assignments/BC-018/validation.md`.

### What worked

- The validator rejects non-controller TurnRequest production, routing before
  SecurityDecision PASS, missing Auth re-entry, merged Auth/OPSEC ownership,
  and OPSEC placement behind Turn Controller.

### What failed or remains unavailable

- No implementation was attempted. Protected Auth/OPSEC policy and evidence
  details remain unresolved as designed.

### Known risks and next safe step

- This correction removes contract ambiguity only; it is not runtime proof.
- After push, Claude performs the independently authorized semantic review of
  the corrected BC-018 head. Do not begin BC-020, BC-030, or implementation.

### Commit identity

- Correction base: `ec4a3c14e6aedb7164fc500b0c9a31486bcd11e8`
- Correction substantive commit: recorded by the metadata-only follow-up

## 2026-08-08 — BC-018-C1 cross-turn security state correction

### What changed

- Replaced the ambiguous pre-ingress loop with an explicit Turn N / Turn N+1
  model and one terminal packet per host turn.
- Removed bare `session` from persistence lifetimes; all deterministic-core
  components are now turn-local, with cross-turn state accepted only from an
  evidenced `host_session` or explicit receipted continuity operation.
- Added `PendingAuthorizationState` as a state record while preserving seven
  components and eight packets.
- Separated attempt-policy authority (Security Restraint), evidence/result
  authority (Authorization Evaluator), and substrate/correlation evidence
  (Host Adapter).
- Required finite attempts, expiry, binding, replay rejection, fail-closed
  exhaustion, and explicit cancellation/reset behavior without publishing
  protected values.
- Bound `AuthorizationResult` validity to turn, evidenced host-session, or
  receipted durable-external scope; made ServiceExchange authority classes
  machine-checkable.
- Resolved directly related N1, N5, and N8 ownership, service-authority, and
  state-lifetime traceability notes.

### What was tested or reviewed

- All five repository validators passed.
- Unit suites passed: contracts 21, viability 9, historical archives 12,
  historical archaeology 18, successor kernel 35.
- The successor suite includes ten new required negative cases for bare
  session, missing substrate, two-terminal turns, expiry, finite attempts,
  replay, AuthorizationResult validity, pre-ingress service authority,
  duplicate attempt ownership, and Turn Controller cross-turn state.
- Final Git, manifest, golden, protected-path, and publication-safety receipts
  are recorded in `assignments/BC-018-C1/validation.md`.

### What worked

- The correction validates without an eighth component or ninth packet.
- BC-020 retains a coherent generic authorization-evidence target and BC-030's
  continuity boundary remains unchanged in authority.

### What failed or remains unavailable

- The first branch-creation attempt was denied Git metadata access before any
  checkout change; retry with the required repository permission succeeded.
- Exact protected attempt values, lockout/backoff rules, evidence classes,
  assurance thresholds, and host-specific binding mechanics remain future
  security/BC-020 inputs.
- No runtime, host adapter, Auth/OPSEC code, session store, persistence, or
  modern PASS/SkillForge work was implemented.

### Known risks and next safe step

- Static validation proves the declared structure, not host capability or
  runtime security behavior.
- Claude performs the separately authorized semantic re-review of the C1
  substantive commit. Dad and Blu decide integration. Do not begin BC-020,
  BC-030, or runtime implementation.

### Commit identity

- Exact base: `7796c7e738e0ff66b677c79314b80cf2bbb09a63`
- Branch: `bc-018-c1-security-state-correction`
- Substantive work commit: recorded by the metadata-only follow-up

## 2026-08-08 — BC-018-C1 closure-prep correction

### What changed

- Restored complete canonical manifest coverage, including `.gitattributes`,
  and added a narrow tracked-path completeness check to the successor validator.
- Corrected the Turn N+1 component graph so Host Adapter correlation returns to
  Security Restraint for attempt permission before Authorization Evaluator.
- Set SUR-012 `blocking_for_BC020` to `true` without changing SUR-002.
- Carried NN-4 to SUR-011 security-policy work and NN-5 to the BC-020/SUR-012
  host-evidence matrix without resolving either future policy question.
- Preserved Claude's review, the approved authority model, and all scope
  exclusions.

### Validation and next safe step

- Exact command, test-count, manifest, golden, count, and protected-path
  receipts are recorded in `assignments/BC-018-C1/validation.md`.
- BC-018 and BC-018-C1 remain in `review`. Dad and Blu decide closure; BC-020,
  BC-030, and runtime implementation remain unstarted.

### Commit identity

- Exact base / Claude review: `1f440546a076c9359afaf5e832882e588d71dfa6`
- Branch: `bc-018-c1-closure-prep`
- Substantive correction commit:
  `90e30c6d685eaa35c9bdf1a666179c9882877d85`

## 2026-08-08 — BC-018 and BC-018-C1 closed

### What changed

- Dad and Blu authorized final administrative closure from integrated main at
  `ce1cc235057a5de3d71fefbcee32e5617197cbb0`.
- BC-018 and BC-018-C1 moved from `review` to `done` in their assignment
  records and the global assignment index.
- The original BC-018 `return-for-correction` review remains immutable history.
  The final C1 re-review remains `approve-with-notes`, with BF-1, BF-2, and
  BF-3 resolved and zero blocking findings.
- Exact lineage through the specification, corrections, reviews, closure-prep
  correction, metadata, and main integration merge was recorded without
  rewriting history.
- Runtime next steps now identify BC-020 and BC-030 as `ready_for_spec` while
  retaining their global `spec-needed`, unstarted state.
- SUR-011 remains a future security-policy input. SUR-012 remains
  `blocking_for_BC020: true` for host-session evidence integrity and rollback
  resistance.
- The canonical manifest was regenerated after closure metadata changed.

### What was tested or reviewed

- Re-ran all five repository validators and unit-test suites.
- Verified complete canonical manifest coverage including `.gitattributes`,
  all eight golden CTS checksums, protected paths, architecture invariants,
  review-record immutability, publication safety, runtime non-implementation,
  and PASS/SkillForge isolation.
- Exact commands and results are recorded in the BC-018 and BC-018-C1
  validation records.

### Known risks and next safe step

- All Claude non-blocking notes remain preserved. Closure resolves none of the
  remaining future policy or host-specific mechanics.
- BC-020 and BC-030 may proceed only after Dad or Blu supplies a separately
  approved packet, named base, and owner. Neither assignment was started.
- No successor runtime implementation is authorized.

### Commit identity

- Closure base: `ce1cc235057a5de3d71fefbcee32e5617197cbb0`.
- Branch: `bc-018-closure`.
- Substantive closure commit:
  `373092e98fef4d291365462baaa7f1ea2a8f065b`.

## 2026-08-08 — BC-020 Chat and Codex host adapter contracts

### What changed

- Activated the Dad/Blu-authorized BC-020 specification from exact base
  `d4157e79fc7e2df6e1bd53b589cabfa19cd7238f` on branch
  `bc-020-chat-codex-adapter-contracts`.
- Added common capability, host-surface, receipt, error, host-session, replay,
  approval, and authorization-transport contracts under `adapters/`.
- Added independent Chat and Codex family/surface contracts, evidence registers,
  and normalized capability matrices covering input, retrieval, actions,
  filesystem/shell/network/Git, time, scheduling, continuity/session, security,
  and output.
- Added the cross-host security evidence matrix and resolved SUR-012 at the
  generic host-evidence contract level without claiming that current surfaces
  can satisfy it.
- Added focused adapter documentation, an offline structural validator, and 25
  negative/positive tests.

### Evidence and dispositions

- Used current first-party OpenAI documentation only for moving product claims;
  every such claim remains `documented_possible` rather than current runtime
  truth.
- Safely observed only the current Codex desktop local Windows binding. The
  snapshot proved bounded workspace/shell/Git/web/time/tool-interface operations
  and recorded their scope, freshness, receipts, and limitations.
- Dad's separate live Chat binding was not probed; its runtime statuses remain
  unknown unless a future adapter self-report supplies evidence.
- Product sign-in remains distinct from usable Blu Auth evidence; host approval
  remains distinct from Blu authorization.
- The current Chat binding is unknown for security-grade host-session evidence.
  The observed Codex binding is verified unavailable for protected cross-turn
  authorization continuation because it exposes no provider-backed replay/
  consumption state or monotonic rollback-resistant attempt state.
- SUR-011 remains unresolved security-policy input. BC-030 remains
  `ready_for_spec` because host-session and durable-external continuity remain
  separate.

### What was tested

- Focused BC-020 validator and 25-test suite passed before the complete
  repository validation run.
- Exact complete-suite, manifest, golden, protected-path, and publication-safety
  results are recorded in `assignments/BC-020/validation.md`.

### Limitations and next safe step

- Static validation proves contract coherence and guardrails, not a live
  provider guarantee, runtime implementation, or behavioral parity.
- The safe client-version probe could not execute the packaged Codex binary;
  client/surface version remains unknown rather than inferred from a path.
- After substantive and metadata commits are pushed, Claude performs the
  independent semantic review. Do not begin BC-030 or runtime implementation.

### Commit identity

- Exact base: `d4157e79fc7e2df6e1bd53b589cabfa19cd7238f`
- Substantive specification commit:
  `09c484418e51365cf9b156cf304eebae7fecde5d`
- Metadata receipt commit: reported externally because a commit cannot contain
  its own final SHA

## 2026-08-09 — BC-020-C1 scheduling capability evidence correction

### What changed

- Corrected `schedule.create`, `schedule.recurring`, and
  `schedule.update_cancel` from `verified_available` to `unknown` on the
  observed Codex surface while preserving scheduling-interface exposure.
- Expanded each row's limitations to separate interface presence from
  provider/account connection, permission, operational usability, operation
  success, future execution, and receipt availability.
- Carried the documented desktop-only limitation that future local scheduled
  execution may depend on the relevant machine and app remaining available.
- Hardened verified capability validation with a curated mapping from
  capability/status to existing `supports[]` tokens and `does_not_prove[]`
  boundaries.
- Added focused regression tests for the three scheduling rows and Claude's
  three demonstrated evidence-relevance defects.

### Evidence and counts

- Corrected Codex totals are 52 capabilities: 24 `verified_available`, 6
  `verified_unavailable`, 4 `documented_possible`, 17 `unknown`, and 1
  `not_applicable`.
- `schedule.receipt` remains `unknown`; scheduling operations remain
  receipt-required; the side-effect completion rule is unchanged.
- Codex evidence now has 22 entries after adding the narrowly scoped desktop
  scheduling limitation source.

### Boundaries and next safe step

- No schedule was created. No adapter, runtime, Local Mirror, BC-030, or
  successor architecture work was started.
- Claude's original BC-020 review remains byte-unchanged.
- Exact validation and commit receipts are in
  `assignments/BC-020-C1/validation.md` and `handoff.md`.
- Claude performs an independent semantic re-review of the C1 metadata head;
  Dad or Blu decides integration and closure.
