# BC-041 — Validation Record

status: complete
owner: Codex
last_reviewed: 2026-08-11

## Environment

- Host: Windows, PowerShell
- Python: 3.12.10
- Schema runtime: `jsonschema==4.26.0`, Draft 2020-12
- Exact base: `699ee1485cef39ffbe70c3b8e848763af02596e0`
- Branch: `bc-041-protected-opsec-phase1`

## Commands and results

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
python tools/validate_host_adapter_contracts.py
python -m unittest discover -s tests/host_adapters -p "test_*.py"
python tools/validate_continuity_contracts.py
python -m unittest discover -s tests/continuity -p "test_*.py"
python tools/validate_python_readiness.py
python -m unittest discover -s tests/readiness -p "test_*.py"
python tools/validate_opsec_contracts.py
python -m unittest discover -s tests/security -p "test_*.py"
```

Observed results:

```text
cached diff check: passed after EOF normalization
runtime contracts: validator passed; 21 tests OK
viability audit: validator passed; 9 tests OK
historical archives: validator passed; 12 tests OK
historical archaeology: validator passed; 18 tests OK
successor kernel: validator passed; 40 tests OK
host adapters: 34 tests OK; standalone validator retained one fixed-base protected-path finding
continuity: validator passed; 42 tests OK
Python readiness: validator passed; 13 tests OK
BC-041 OPSEC: validator passed; 22 tests OK
```

The preserved host-adapter output is:

```text
ERROR: protected path changed from BC-020 base: contracts/successor/unresolved_register.json
host adapter contract validation failed: 1 error(s)
```

This validator intentionally compares against the older BC-020 base. The path
contains the historical BC-030 SUR-007 disposition and now the explicitly
authorized BC-041 SUR-001 disposition. It is therefore not wholly unrelated to
BC-041. The finding was not suppressed or reported as a pass. The continuity
and readiness validators independently constrain the BC-041 change to the exact
SUR-001 resolution shape and prove SUR-002, SUR-011, and SUR-012 unchanged.

## Golden-source verification

```text
golden CTS checksums: 8/8 passed
golden exact-base changed paths: 0
successor components / packets / interfaces: 7 / 8 / 9
manifest entries: 274; complete staged-path coverage and canonical Git-blob digests passed
changed files at pre-receipt validation: 30
changed Python: 6, all validators/tests
production runtime/provider roots present: 0
architecture documents changed: 0
adapter files changed: 0
continuity contract files changed: 0
prior review files changed: 0
SUR-002 / SUR-011 / SUR-012 objects changed: false
```

The changed Python files are the focused OPSEC validator/test, readiness
validator/test, and the narrowly scoped continuity-validator/test update. No
production module exists.

## Negative tests

- Policy loading: valid reference; missing reference; unavailable target;
  malformed JSON; schema-invalid policy; integrity mismatch; unusable duplicate
  normalized rule.
- Ingress: ordinary PASS; exact/case/whitespace/line-break/separator/Unicode
  matches BLOCK; safe near-match/common-word/partial/punctuation negatives PASS;
  only PASS is Turn Controller eligible.
- Egress: clear output; single/multiple/beginning/end redaction; full-block rule;
  redaction-only invalid result; repetition removal; protected text/key absent
  from serialized result/log/evidence.
- Boundaries: exact three-value `SecurityDecision`, no model/Auth dependency,
  no tool/continuity/SUR-011 behavior, 7/8/9 unchanged, runtime implementation
  authorization remains false.

## Failed attempts

- Initial branch creation inside the restricted filesystem could not create
  `.git/index.lock`; the same exact authorized branch operation succeeded after
  repository metadata permission was granted. No file edit preceded the
  successful exact-base checkout.
- The first readiness validation correctly reported 12 missing manifest entries
  for the new files. The manifest was regenerated from staged Git blobs.
- The first full regression run exposed trailing blank EOFs and continuity
  fixed-base scope errors for the newly authorized register/Python files. EOFs
  were normalized. The continuity validator received a narrow exact-shape
  SUR-001 exception and explicit validator/test allowlist entries; a Git-backed
  negative test proves adjacent SUR-002 mutation still fails.

## Validation boundary

These checks prove the public schemas/mechanism are coherent, the synthetic
fixture follows the same contract, specified trivial bypasses and false-positive
cases behave deterministically, unusable policy cannot pass, protected fixture
text does not leak through matched results, readiness records agree, and the
repository boundaries remain intact. They do not prove production policy
completeness, arbitrary semantic leakage detection, live model behavior, Auth,
protected continuation, or production runtime security. No real protected
policy was loaded or tested.
