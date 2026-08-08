# BC-018-C1 — Validation Record

status: done
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
- The first substantive commit attempt was denied the same Git index lock and
  left `HEAD` at the exact base with all staged content intact. The authorized
  retry succeeded as `a87e7d7ea57688212c7c8461b5630c6ddb55a00f`.

## Validation boundary

Passing checks prove the published structural constraints, internal references,
required negative fixtures, repository manifest, protected paths, and golden
checksums. They do not prove that any host implements the interface, that a
security policy is correct, or that a successor runtime exists.

## Pre-review terminal-authority correction validation — 2026-08-08

Correction base: `b1e0f5c7ce3fddd7d71f6b2fa8050b0b55875b3c`.
Substantive correction commit:
`311c572f3a28fe4e1cca04b75856faae3cfd6c60`.

Commands:

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
git diff --name-only b1e0f5c7ce3fddd7d71f6b2fa8050b0b55875b3c --
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
successor specification tests: Ran 39, OK
component count: 7, unchanged
packet count: 8, unchanged
SecurityDecision statuses: PASS, BLOCK, ASK, unchanged
canonical manifest: 188 entries, self-excluded, 0 missing, 0 mismatch
golden CTS SHA-256: 8/8 passed
protected-path diff: empty
modern PASS/SkillForge diff: empty
successor runtime implementation diff: empty
```

Four focused negative cases reject:

1. pre-ingress `UNAVAILABLE` requiring a `ControlDecision`;
2. pre-ingress `UNAVAILABLE` without originating `SecurityDecision` authority;
3. an unbound `PendingAuthorizationState` remaining resumable after substrate
   failure; and
4. an `ASK` terminal followed by a second `UNAVAILABLE` terminal for the same
   binding attempt.

The previous 35 successor tests remain present and passing. Structural success
does not prove host support or runtime enforcement.

## Closure-prep correction validation — 2026-08-08

Exact base / Claude review commit:
`1f440546a076c9359afaf5e832882e588d71dfa6`.
Substantive correction commit:
`90e30c6d685eaa35c9bdf1a666179c9882877d85`.

Commands:

```text
git diff --cached --check
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
PowerShell/Python SHA-256 verification against
  kernel/golden/v0.22.0/SHA256SUMS
canonical LF/Git-blob MANIFEST regeneration and complete tracked-set
  verification from the staged index
protected-path, runtime-implementation, modern PASS/SkillForge, review-blob,
  component, packet, interface, and SecurityDecision-status checks
```

Results:

```text
git diff --cached --check: passed
runtime contract validator: passed
contract tests: Ran 21, OK
viability audit validator: passed
viability tests: Ran 9, OK
historical inventory validator: passed
historical inventory tests: Ran 12, OK
historical archaeology validator: passed
historical archaeology tests: Ran 18, OK
successor specification validator: passed
successor specification tests: Ran 40, OK
canonical manifest: 189 entries, self-excluded, 0 missing, 0 extra,
  0 duplicate, 0 mismatch
golden CTS SHA-256: 8/8 passed
component count: 7, unchanged
packet count: 8, unchanged
interface count: 9, unchanged
SecurityDecision statuses: PASS, BLOCK, ASK, unchanged
protected/current-CTS diff: empty
successor runtime implementation diff: empty
modern PASS/SkillForge diff: empty
Claude review blob: unchanged
```

The successor suite increased from 39 to 40 tests only to add
`test_manifest_coverage_rejects_missing_tracked_file`, which proves the
validator rejects a tracked file omitted from `MANIFEST.sha256`. Existing
successor tests remain present and passing.

NN-2 now has a diagram path through Security Restraint attempt permission before
Authorization Evaluator. NN-3 sets only SUR-012 `blocking_for_BC020` to `true`;
SUR-002 remains unchanged. NN-4 and NN-5 remain unresolved, explicit future
inputs under SUR-011 and SUR-012/BC-020 respectively. Neither assignment was
marked done, and BC-020/BC-030 were not started.

## Final closure validation — 2026-08-08

Commands run from `bc-018-closure` at exact base
`ce1cc235057a5de3d71fefbcee32e5617197cbb0`:

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
canonical LF/Git-blob MANIFEST regeneration and complete tracked-set
  verification from the staged index
PowerShell SHA-256 verification against
  kernel/golden/v0.22.0/SHA256SUMS
protected-path, architecture/contract, review-record, runtime-implementation,
  historical-module, publication-safety, and PASS/SkillForge isolation checks
```

Results:

```text
git diff --check: passed
runtime contract validator: passed
contract tests: Ran 21, OK
viability audit validator: passed
viability tests: Ran 9, OK
historical inventory validator: passed
historical inventory tests: Ran 12, OK
historical archaeology validator: passed
historical archaeology tests: Ran 18, OK
successor specification validator: passed
successor specification tests: Ran 40, OK
components: 7
packets: 8
interfaces: 9
SecurityDecision statuses: PASS, BLOCK, ASK
PendingAuthorizationState: state record, not a packet
state lifetimes: none, turn, host_session, durable_external
bare session lifetime: absent
canonical manifest: complete, self-excluded, 0 missing, 0 extra,
  0 duplicate, 0 mismatch; .gitattributes covered
golden CTS SHA-256: 8/8 passed
protected-path diff: empty
architecture/contract diff: empty
BC-018 and BC-018-C1 review-record diff: empty
successor runtime implementation diff: empty
historical module/archive payload diff: empty
modern PASS/SkillForge and Blu_KB_Preview diff: empty
private or protected publication hits: 0
```

SUR-011 remains an unresolved future security-policy input. SUR-012 remains
`blocking_for_BC020: true`. BC-020 and BC-030 remain `spec-needed` and
unstarted; no runtime implementation occurred.
