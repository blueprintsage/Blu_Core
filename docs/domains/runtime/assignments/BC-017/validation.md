# BC-017 Validation

status: review
owner: Codex
last_reviewed: 2026-08-07
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
