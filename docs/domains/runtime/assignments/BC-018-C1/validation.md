# BC-018-C1 — Validation Record

status: review
owner: Codex
last_reviewed: 2026-08-08

## Environment

- Host: Windows / PowerShell
- Python: 3.12.10
- Dependencies: standard library only for the successor validator/tests
- Known limitation: structural validation does not prove runtime behavior,
  host capability, security-policy correctness, or semantic parity

## Commands and results

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
python tools/validate_successor_kernel_spec.py
python -m unittest discover -s tests/successor_kernel -p "test_*.py"
PowerShell SHA-256 verification against kernel/golden/v0.22.0/SHA256SUMS
git diff --name-only 7796c7e738e0ff66b677c79314b80cf2bbb09a63 --
  kernel/golden/v0.22.0 contracts/runtime docs/sources/historical_archives
canonical LF/git-blob MANIFEST regeneration and verification from the index
```

Results:

```text
git diff --check: passed (line-ending warnings only)
runtime contract validator: passed
contract tests: Ran 21, OK
viability audit validator: passed
viability tests: Ran 9, OK
historical inventory validator: passed
historical inventory tests: Ran 12, OK
historical archaeology validator: passed
historical archaeology tests: Ran 18, OK
successor specification validator: passed
successor specification tests: Ran 35, OK
component count: 7 -> 7
packet count: 8 -> 8
state records added: PendingAuthorizationState (not a packet)
canonical manifest: 188 entries, self-excluded, 0 missing, 0 mismatch
```

## Golden-source verification

All eight entries in `kernel/golden/v0.22.0/SHA256SUMS` passed using
PowerShell `Get-FileHash -Algorithm SHA256`:

```text
GOLDEN_CHECKSUMS=8/8
PROTECTED_PATH_DIFF=empty
MODERN_PASS_SKILLFORGE_DIFF=empty
SUCCESSOR_RUNTIME_DIFF=empty
```

The protected-path check covers `kernel/golden/v0.22.0`, `contracts/runtime`,
and `docs/sources/historical_archives` against the exact C1 base.

## Negative tests

The successor suite has 35 tests. Ten C1 negative cases require rejection of:

1. bare `session` cross-turn kernel persistence;
2. pending authorization without evidenced host-session or continuity-backed
   substrate;
3. two terminal packets in one host turn;
4. a pending request without expiry;
5. a pending request without a finite attempt bound;
6. a pending request without replay protection;
7. `AuthorizationResult` session validity without evidenced binding;
8. pre-ingress authority used for an ordinary service;
9. duplicate authoritative attempt-policy ownership; and
10. hidden cross-turn state in Turn Controller.

## Failed attempts

- The initial branch-creation command was denied access to `.git/index.lock`
  before changing repository state; the exact authorized operation succeeded
  after repository metadata permission was granted.
- The first attempt to stage the regenerated manifest was likewise denied
  `.git/index.lock`; verification correctly read the old 185-entry staged
  manifest and reported it stale. After the required repository permission,
  the regenerated 188-entry manifest staged and verified 188/188 with zero
  missing entries or mismatches.

## Validation boundary

Passing checks prove the published structural constraints, internal references,
required negative fixtures, repository manifest, protected paths, and golden
checksums. They do not prove that any host implements the interface, that a
security policy is correct, or that a successor runtime exists.
