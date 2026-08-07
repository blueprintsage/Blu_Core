# BC-017-C1 Validation

status: review
owner: Codex
last_reviewed: 2026-08-07
assignment: BC-017-C1

## Scope

Validation covers the three blocking corrections, complete repository
validator/test suites required by the packet, canonical manifest bytes, golden
checksums, protected paths, and archive-payload exclusion. Green validation
does not itself prove document semantics; B-01/B-02/B-03 are also checked
manually.

## Commands

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
git grep -n "^+#" -- "*.md"
canonical LF/git-blob MANIFEST verification from the staged index
golden CTS SHA-256 verification
```

## Results

```text
runtime contract validator: passed
contract tests: Ran 21, OK
viability audit validator: passed
viability tests: Ran 9, OK
historical inventory validator: passed
historical inventory tests: Ran 12, OK
historical archaeology validator: passed
historical archaeology tests: Ran 18, OK
git diff --check: passed
malformed archaeology README headings: none
protected-path diff: empty
golden CTS SHA-256: 8/8 passed
```

Manual acceptance checks:

- B-01: the README begins with a normal heading and no line retains a systematic
  leading diff marker.
- B-02: both README commands match BC-017 `validation.md` and resolve to the
  committed validator and test module.
- B-03: the direct contraction is v0.16.0; no v0.20 contraction label or delta
  remains; later v0.20/v0.21 restructuring is distinct; and the BC-016 v0.21
  structural-representative framing is disclosed.
- Claude's triggering review is byte-unchanged.

The canonical staged-index manifest contains 167 entries, excludes itself, and
verified against staged canonical bytes with zero missing entries and zero hash
mismatches.
