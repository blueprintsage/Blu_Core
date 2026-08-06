# Runtime Worklog

status: active
owner: docs/domains/runtime
last_reviewed: 2026-08-05

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
