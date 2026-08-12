# BC-041-C1 - Validation Record

status: complete
owner: Codex
last_reviewed: 2026-08-11

## Environment

- Host: Windows, PowerShell
- Python: 3.12.10
- Schema runtime: `jsonschema==4.26.0`, Draft 2020-12
- Exact base: `33b44608cb634d1fedeed7f5f70d405c3999ed02`
- Branch: `bc-041-c1-unicode-format-correction`

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

Observed results before the final metadata-only receipt:

```text
cached diff check: passed
runtime contracts: validator passed; 21 tests OK
viability audit: validator passed; 9 tests OK
historical archives: validator passed; 12 tests OK
historical archaeology: validator passed; 18 tests OK
successor kernel: validator passed; 40 tests OK
host adapters: 34 tests OK; standalone validator retained one fixed-base protected-path finding
continuity: validator passed; 42 tests OK
Python readiness: validator passed; 15 tests OK
BC-041-C1 OPSEC: validator passed; 29 tests OK
```

The preserved host-adapter output is:

```text
ERROR: protected path changed from BC-020 base: contracts/successor/unresolved_register.json
host adapter contract validation failed: 1 error(s)
```

This compares against the historical BC-020 base and is the same finding
recorded by the immutable BC-041 review. C1 does not change the named path. The
finding was not suppressed or reported as a pass.

## Focused C1 behavior

```text
Cf ingress matrix: 6 code points x 2 positions = 12/12 BLOCK
Cf ingress Turn Controller eligibility: 0/12
Cf egress matrix: 6 code points x 2 positions = 12/12 safely REDACTED
Cf egress dual-view rescan: 12/12 clean
mixed divergent-view egress: BLOCKED, not printable
existing negative ingress fixtures: 5/5 PASS
Cf result/log/evidence leak checks: 24/24 clean
```

The six tested general-category `Cf` code points are U+200B, U+00AD, U+200D,
U+200C, U+FEFF, and U+2060. Each was tested where a protected word boundary
belongs and inside a protected token for both ingress and egress.

## Golden, manifest, architecture, and protected boundaries

```text
golden CTS checksums: 8/8 passed before edits and after correction
golden exact-base changed paths: 0
successor components / packets / interfaces: 7 / 8 / 9
canonical manifest entries: 278
manifest missing / extra / duplicate / digest mismatch: 0 / 0 / 0 / 0
changed files: 19
changed Python files: 4, all validators/tests
production src/blu_runtime root present: false
architecture registry changes: 0
contracts/successor/unresolved_register.json changes: 0
readiness/implementation_blocker_dispositions.json changes: 0
BC-041 immutable review blob unchanged: true
SUR-002 / SUR-011 / SUR-012 changed: false
```

The manifest was generated and verified from canonical staged Git blobs rather
than Windows working-tree bytes. Successor, continuity, and readiness validators
all independently accepted its complete path set and digests.

Changed-line and changed-path review found only explicitly synthetic protected
phrases in the synthetic fixtures. No production protected value, private key,
credential, machine-local policy binding, production policy digest, or
production policy location was introduced. No production runtime/provider/Auth
path was added.

## Negative and mutation tests

- Both candidate views are exposed in deterministic order and produce the
  expected boundary/inside-token contrast.
- Either matching view blocks ingress; no non-PASS ingress becomes model
  eligible.
- Egress redaction rescans both views; divergent matching views fail closed.
- The five existing ordinary/common-word/partial/punctuation/near-match
  negatives remain PASS.
- A readiness review state changed to `pass`/`complete` is rejected, and a
  pending review cannot set implementation authorization true.
- Policy-loader missing, unavailable, malformed, schema-invalid, integrity-
  mismatched, and unusable cases continue to fail closed.
- Evidence/log serialization excludes synthetic policy values and the
  synthetic HMAC key for all 24 C1 probes.

## Failed attempts

- The initial branch-creation attempt inside the restricted filesystem could
  not create `.git/index.lock`. The exact authorized operation succeeded after
  repository metadata permission was granted. No file edit preceded the
  successful exact-base checkout.
- A pre-manifest readiness run correctly reported the four new C1 assignment
  files missing from `MANIFEST.sha256`. The manifest was then regenerated from
  the complete staged Git path set and validated.

Two one-line diagnostic probes were mistyped at the shell quoting boundary and
did not execute Python. They changed no file or repository state and were
superseded by the focused validator and unit tests above.

## Validation boundary

These checks prove the bounded public contract, synthetic dual-view mechanism,
required `Cf` matrices, prior negative behavior, content-safe results, readiness
state semantics, repository integrity, and protected boundaries. They do not
prove production policy completeness/classification, general Unicode
confusable/homoglyph resistance, semantic paraphrase detection, live model or
LM Studio behavior, Auth, protected continuation, or production runtime
security. No real protected policy was loaded or tested.

## Commit identity

- Substantive correction commit: recorded by the metadata-only follow-up.
- Metadata method: the follow-up records the substantive SHA; its own final SHA
  is reported externally rather than embedded in its tree.
