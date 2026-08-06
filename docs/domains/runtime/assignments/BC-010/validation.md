# BC-010 — Validation Record

status: review
owner: Codex
record_status: backfilled
backfilled_on: 2026-08-05
evidence_sources:
  - docs/domains/runtime/assignments/BC-010/handoff.md
  - docs/domains/runtime/worklog.md
  - docs/domains/runtime/assignments/BC-010/review.md

## Boundary

This record is backfilled only from committed BC-010 handoff, worklog, and
Claude review evidence. It does not reconstruct console output that was not
recorded and does not add validation claims beyond those sources.

## Recorded implementation checks

The handoff records these commands as run:

```text
git status --short
git rev-parse HEAD
git merge-base --is-ancestor 7aed76e HEAD
python tools/validate_runtime_contracts.py
python -m unittest discover -s tests/contracts -p "test_*.py"
git diff --check
git diff --exit-code 7aed76e -- kernel/golden/v0.22.0
PowerShell Get-FileHash -Algorithm SHA256 comparison against kernel/golden/v0.22.0/SHA256SUMS
```

Recorded results:

- Base ancestry passed at pre-commit HEAD
  `3c421914d2b449f63f9b7ba73e24cc59539c1c3b`.
- Runtime contract validation passed.
- Unit validation passed with 4 tests.
- `git diff --check` passed after two extra end-of-file blank lines were
  removed.
- Golden diff against `7aed76e` passed.
- PowerShell SHA-256 verification passed for all eight entries: the seven
  Markdown files and retained CTS ZIP.
- No runtime behavior implementation was added.

## Independent semantic-review checks

Claude's committed review records:

```text
git status --short                                        -> clean
git rev-parse HEAD                                        -> f743ee8bec1f809f66e5b63f04c3441beddaf4f3
git show -s --format=%H 40138b6e16f28c01904aae97158878468ee47ad0
                                                          -> commit present
git diff --check                                          -> exit 0, no output
PowerShell Get-FileHash comparison                        -> 8/8 OK
git diff --exit-code 40138b6 -- contracts/runtime tools tests kernel/golden
                                                          -> exit 0
python tools/validate_runtime_contracts.py                -> PASS, exit 0
python -m unittest discover -s tests/contracts -p "test_*.py"
                                                          -> Ran 4 tests, OK
```

The review independently recomputed 41 registry components, 6 live slash
stems, 69 source-map entries, 22 unresolved items, 12 parity requirements, and
34 parity cases.

## Limitations and unavailable evidence

- Exact full implementation-run console output was not preserved in the
  committed sources and is unavailable.
- Exact Python version for the BC-010 implementation run was not recorded and
  is unavailable.
- `sha256sum` was unavailable on the Windows host; the approved PowerShell
  equivalent was used.
- The optional `jsonschema` package was recorded as not installed.
- The original standalone validator did not apply schemas to fixtures and
  silently ignored unsupported schema keywords; Claude recorded this as B-3.
- Positive fixture validation was recorded, but no negative schema fixture
  existed in BC-010.
- Structural/schema validation did not prove behavioral parity.

## Disposition

Claude returned BC-010 for correction. BC-010 remains in `review`; BC-010-C1
owns the corrective implementation and validation evidence.
