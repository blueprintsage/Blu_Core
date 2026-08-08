# BC-017 Validation

status: done
owner: Codex
last_reviewed: 2026-08-08
assignment: BC-017

## Validation scope

Validation checks evidence-record integrity, canonical archive resolution,
publication safety, recovery vocabulary, evidence labels, protected golden
checksums, and the prohibition on archive payloads and runtime implementation.
It does not execute historical behavior.

## Commands

```text
python tools/validate_historical_behavioral_archaeology.py
python -m unittest tests.historical_archaeology.test_validate_historical_behavioral_archaeology
python tools/validate_historical_archive_inventory.py
python -m unittest tests.historical_archives.test_validate_historical_archive_inventory
git diff --check
sha256sum -c kernel/golden/v0.22.0/SHA256SUMS
canonical LF/git-blob MANIFEST verification from the staged index
```

## Results

All required checks passed before the substantive work commit:

```text
runtime contract validator: passed
contract tests: Ran 21, OK
viability audit validator: passed
viability tests: Ran 9, OK
historical inventory validator: passed
historical inventory tests: Ran 12, OK
BC-017 archaeology validator: passed
BC-017 archaeology tests: Ran 18, OK
git diff --check: passed (line-ending warnings only)
golden CTS SHA-256: 8/8 passed
protected-path diff: no kernel/golden, contracts/runtime, docs/architecture, or config changes
```

The normalized staged-index manifest contains 163 entries, excludes itself, and
verified against staged canonical bytes with zero missing entries and zero hash
mismatches.

## Known validation boundary

The Faithfulness archive scan covered 244 nested-archive filenames and 1,985
readable members. Sixty-three Deflate64 members in seven archives were
unreadable. This limitation is preserved rather than treated as a match or as
proof of absence.

## Closure validation — 2026-08-08

Commands run from `bc-017-closure` at base
`b88902d997685057ee0e76709df7117f8a83f295`:

```text
git diff --check
python tools/validate_runtime_contracts.py
python -m unittest discover -s tests/contracts -p "test_*.py"
python tools/validate_viability_audit.py
python -m unittest discover -s tests/viability -p "test_*.py"
python tools/validate_historical_archive_inventory.py
python -m unittest discover -s tests/historical_archives -p "test_*.py"
python tools/validate_historical_behavioral_archaeology.py
python -m unittest discover -s tests/historical_archaeology -p "test_*.py"
canonical LF/git-blob MANIFEST regeneration and verification from the index
PowerShell SHA-256 verification against kernel/golden/v0.22.0/SHA256SUMS
git diff --exit-code b88902d997685057ee0e76709df7117f8a83f295 -- kernel/golden/v0.22.0 contracts/runtime docs/architecture config
closure-diff archive, implementation, PASS/SkillForge, source-surface, and
private/protected-text scans
```

Results:

```text
runtime contract validator: passed
contract tests: Ran 21, OK
viability audit validator: passed
viability tests: Ran 9, OK
historical inventory validator: passed
historical inventory tests: Ran 12, OK
historical archaeology validator: passed
historical archaeology tests: Ran 18, OK
canonical manifest: 167/167 verified; 0 missing; 0 mismatches
golden CTS SHA-256: 8/8 passed
protected paths: unchanged
archive path hits: 0
Python/runtime implementation path hits: 0
modern PASS/SkillForge path hits: 0
protected source-surface hits: 0
private or protected-text leak hits: 0
git diff --check: passed
```

The closure changed assignment and continuity Markdown plus the canonical
manifest only. It added no historical archive, raw historical kernel payload,
protected Auth/OPSEC material, successor design, or runtime implementation.
