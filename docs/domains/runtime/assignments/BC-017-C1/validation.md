# BC-017-C1 Validation

status: done
owner: Codex
last_reviewed: 2026-08-08
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

## Closure validation — 2026-08-08

The complete closure validation matrix was re-run after the final Claude review
was integrated. Exact commands are recorded in the parent BC-017 validation
record. Results were:

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

No BC-017-C2 was required. No successor work was started.
