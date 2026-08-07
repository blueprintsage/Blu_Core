# Runtime Worklog

status: active
owner: docs/domains/runtime
last_reviewed: 2026-08-06

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
