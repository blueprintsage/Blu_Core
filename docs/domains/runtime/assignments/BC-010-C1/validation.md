# BC-010-C1 — Validation Record

status: active
owner: Codex
last_reviewed: 2026-08-05

## Environment

- Python version: `Python 3.12.10`
- Optional `jsonschema` dependency: absent
- `sha256sum`: absent on this Windows host
- Validator dependencies: Python standard library only

## Required command results

```text
git status --short
```

Result before the repair work commit: 27 authorized files staged after manifest
generation; no unstaged or untracked assignment file. The pre-existing local
`.claude/settings.local.json` is preserved through `.git/info/exclude` and is
not part of the repository diff.

```text
git rev-parse HEAD
```

Result before the repair work commit:
`38611bf4b8051c858dcbbc30a07904d0117211b3`.

```text
git merge-base --is-ancestor 38611bf4b8051c858dcbbc30a07904d0117211b3 HEAD
```

Result: exit 0.

```text
git diff --check
```

Result: exit 0; no whitespace errors. Git emitted only expected
LF-to-CRLF working-copy notices.

```text
git diff --exit-code 38611bf4b8051c858dcbbc30a07904d0117211b3 -- kernel/golden/v0.22.0
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

Result: exit 0:

```text
Ran 15 tests in 0.206s
OK
```

The exact elapsed time varied slightly on repeat runs; test count and result
remained 15 and `OK`.

## Golden CTS checksums

Because `sha256sum` is unavailable, the existing PowerShell equivalent compared
`Get-FileHash -Algorithm SHA256` output with all entries in
`kernel/golden/v0.22.0/SHA256SUMS`.

Result:

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
manifest file itself. This matches the bootstrap manifest's documented file-set
semantics.

Result after the final regeneration:

```text
MANIFEST_ENTRIES=121
MANIFEST_VERIFIED=121/121
```

## What validation proves

- Required contract, schema, and canonical fixture presence.
- JSON parsing for contracts, schemas, and canonical fixtures.
- Exact source role mapping and exact Markdown heading anchoring.
- Registry uniqueness and public slash-stem single ownership.
- Supported local schema keyword/type enforcement.
- Canonical positive fixture acceptance and negative fixture rejection.
- Golden checksum and diff preservation when the required Git/hash checks pass.

## What validation does not prove

- General JSON Schema compliance.
- Behavioral parity.
- Executable Blu runtime behavior.
- Host capability, persistence, routing execution, reminders, or artifact proof.
- Resolution of any unresolved declaration.
