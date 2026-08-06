# BC-010-C2 — Validation Record

status: review
owner: Codex
last_reviewed: 2026-08-06

## Environment

- Exact base: `424f80b254a02f057da6c82db5230377076fc415`
- Branch: `bc-010-c2-opsec-route-repair`
- Python version: `Python 3.12.10`
- `sha256sum`: unavailable on this Windows host; PowerShell SHA-256 equivalent used
- Validator dependencies: Python standard library only

## Required command results

```text
git status --short
```

Result before the repair work commit: all changes were inside the approved C2
collision domain and staged after final manifest generation. No unrelated
working-tree change was present.

```text
git rev-parse HEAD
```

Result before the repair work commit:
`424f80b254a02f057da6c82db5230377076fc415`.

```text
git diff --check
git diff --cached --check
```

Final result: exit 0; no whitespace errors. The first staged check found a new
blank line at EOF in each of the four new C2 records. Those blank lines were
removed before the final checks.

```text
git diff --exit-code 424f80b254a02f057da6c82db5230377076fc415 -- kernel/golden/v0.22.0
```

Result: exit 0; no golden-source change.

```text
python tools/validate_runtime_contracts.py
```

Result: exit 0:

```text
PASS: runtime contracts and canonical fixtures satisfy the supported structural subset
```

```text
python -m unittest discover -s tests/contracts -p "test_*.py"
```

Result: exit 0; `Ran 21 tests`; `OK`.

## OPSEC mechanical checks

```text
rg -n '"lane_class": "opsec"' contracts/runtime
```

Result: exit 1 with no matches, the expected no-match result.

The approved successor-runtime statements that Auth authorizes Admin-level
users and OPSEC is a mandatory pre-ingress restraint occur only in project
documentation (`docs/domains/runtime/decisions.md` and this approved assignment
packet). They do not occur in `contracts/runtime/**`, validator code, tests, or
the golden CTS source.

## Golden CTS checksums

PowerShell `Get-FileHash -Algorithm SHA256` was compared with every entry in
`kernel/golden/v0.22.0/SHA256SUMS`:

```text
OK 00_Instructions.md
OK 01_Persona.md
OK 02_Operations_Law.md
OK 03_Exec.md
OK 04_Exec_Library.md
OK 05_Commands.md
OK 06_Programs.md
OK source_Blu_v0_22_0_5_22_26_2104_CTS.zip
GOLDEN_CHECKSUMS=8/8
```

## Repository manifest

`MANIFEST.sha256` was regenerated from the complete staged tracked-file set,
sorted by repository path, excluding `.gitattributes` and the self-referential
manifest file.

```text
MANIFEST_ENTRIES=125
MANIFEST_VERIFIED=125/125
```

## Validation boundary

Passing checks prove the recorded structural, fixture, checksum, and Git-diff
conditions only. They do not prove executable runtime behavior, host
capability, behavioral parity, or resolution of UR-028.
