# BC-041-C1 - Validation Record

status: complete
owner: Codex
last_reviewed: 2026-08-12

## Environment and lineage

- Host: Windows, PowerShell
- Python: 3.12.10
- Schema runtime: `jsonschema==4.26.0`, Draft 2020-12
- Original authorized base: `33b44608cb634d1fedeed7f5f70d405c3999ed02`
- Correction starting point: `54519493189a332e984409504c45210e759f18fc`
- Branch: `bc-041-c1-mixed-cf-correction`
- Claude review evidence only:
  `874852c1b548ba4a2539d796d23ab9d803a966c8`

The correction branch was created directly from `5451949`. Claude's review
branch was not merged or cherry-picked.

## Full validation commands

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

## Full suite results

```text
cached diff check: passed
runtime contracts: validator passed; 21 tests OK
viability audit: validator passed; 9 tests OK
historical archives: validator passed; 12 tests OK
historical archaeology: validator passed; 18 tests OK
successor kernel: validator passed; 40 tests OK
host adapters: standalone validator retained one fixed-base finding; 34 tests OK
continuity: validator passed; 42 tests OK
Python readiness: validator passed; 16 tests OK
BC-041-C1 OPSEC: validator passed; 33 tests OK
```

The preserved host-adapter output is:

```text
ERROR: protected path changed from BC-020 base: contracts/successor/unresolved_register.json
host adapter contract validation failed: 1 error(s)
```

This is the known BC-020 fixed-base protected-path finding already recorded by
BC-041/C1. The correction does not change that path. It was not suppressed and
is not reported as a pass.

## B-1' expanded proof

The corrected mechanism uses one candidate: remove every Unicode
general-category `Cf` code point, run the existing normalization pipeline, then
match each normalized inter-word rule separator against zero-or-more normalized
ASCII spaces under whole-phrase Unicode token guards. Candidate count remains
one regardless of insertion count.

```text
required code points: U+200B, U+00AD, U+200D, U+200C, U+FEFF, U+2060
same-code-point ingress: 6 x 3 positions = 18/18 BLOCK; model eligible 0/18
same-code-point egress: 6 x 3 positions = 18/18 REDACTED; CLEAR 0/18
cross-code-point mixed fixtures: ingress 1/1 BLOCK; egress 1/1 REDACTED
fixture Cf total: 38/38 safe
mutation matrix: 6 code points x repeat counts 1, 2, 4 at arbitrary positions
mutation ingress: 18/18 BLOCK; model eligible 0/18
mutation egress: 18/18 REDACTED or BLOCKED; CLEAR 0/18
repeated cross-code-point arbitrary placement: ingress BLOCK; egress not CLEAR
existing negative ingress fixtures: 5/5 PASS
```

The five pinned negative fixtures are `ordinary`, `near_match`, `shared_words`,
`partial_fragment`, and `punctuation_adjacent_nonmatch`. The validator requires
the exact boundary/inside-token/mixed same-code-point matrix and a distinct
cross-code-point mixed case at both ingress and egress.

Redaction proof includes multi-span redaction, mixed placements, post-redaction
rescan using the same matcher, redaction-only output blocking, policy `BLOCK`
action, and overlapping-span fail-closed behavior. Protected ingress never
reaches Turn Controller/model eligibility. Protected egress never returns
`CLEAR` or printable raw protected content.

## Readiness coupling

During active correction, the checklist was set to
`not_ready_for_python_phase1`, the OPSEC gate was `fail`, B-1' was listed as an
actual blocker, and packet authoring was false. It returned to
`ready_for_python_phase1` only after the corrected mechanism and expanded proof
passed.

`validate_python_readiness.py` loads and executes the OPSEC validator against
the same root. The readiness mutation test deletes the entire mixed ingress
fixture class while leaving the readiness record green; validation then fails
for both incomplete Cf matrix and missing cross-code-point mixed proof. Green
readiness therefore cannot survive removal of the expanded B-1' proof.

Independent Claude re-review remains `required_pending` and incomplete;
`implementation_authorized` remains false; automatic start remains prohibited;
Dad/Blu closure remains required.

## Evidence, policy, and negative behavior

- Synthetic policy references are opaque numeric identifiers; the usability
  validator rejects a reference that reconstructs its protected rule value.
- Evidence HMAC uses the sole candidate that produced the decision.
- Rule and candidate normalization are separately named; protected policy rule
  values containing `Cf` are unusable.
- Ingress and non-clear egress results are scanned for both synthetic protected
  values and the synthetic evidence key. The 38 fixture Cf results and mutation
  paths remain content-safe.
- Missing, unavailable, malformed, schema-invalid, integrity-mismatched, and
  unusable policies continue to fail closed.
- SecurityDecision remains exactly `PASS | BLOCK | ASK`; only `PASS` is model
  eligible.
- General Unicode confusable/homoglyph substitution remains explicitly outside
  this minimum matcher and distinct from semantic paraphrase.

## Golden, manifest, architecture, and repository boundaries

```text
golden CTS checksums: 8/8 passed
golden changed paths from correction start: 0
successor components / packets / interfaces: 7 / 8 / 9
canonical manifest entries: 278
manifest missing / extra / duplicate / digest mismatch: 0 / 0 / 0 / 0
BC-041 immutable review changed: false
BC-041-C1 Claude review changed: false
SUR-002 / SUR-011 / SUR-012 changed: false
architecture registries changed: 0
production src/blu_runtime roots present: false
```

Manifest validation uses canonical staged Git blob bytes, not CRLF working-tree
bytes. Changed Python files are the two nonproduction validators and their two
test modules only. Changed-path and added-line inspection found no production
protected value, production policy location/digest, credential, private key,
runtime/provider/Auth path, continuity mutation, tool, or PASS/SkillForge
crossover.

## Failed attempts and limitations

- The first branch-creation attempt could not write `.git/index.lock` inside
  the restricted filesystem. The exact authorized operation succeeded after
  repository metadata permission was granted; no edit preceded the successful
  exact-base checkout.
- The first focused security test run produced 32 passing tests plus one
  expected canonical validation failure while readiness was deliberately red
  during correction. After the corrected mechanism and expanded proof passed,
  readiness was truthfully restored and the complete focused suite passed.
- The prior two-static-view design is preserved only as superseded history. It
  must not be reused as proof for arbitrary placement combinations.

These checks establish only the bounded public contract and synthetic
conformance proof. They do not prove production policy completeness or
classification, general confusable/homoglyph resistance, semantic paraphrase
detection, live model/LM Studio behavior, Auth, protected continuation, or a
production runtime. No real protected policy was loaded or tested.

## Commit identity

- Substantive mixed-placement correction:
  `2a9d6a28111ca9576bf6811e67ccca37f4d5dd39`.
- Metadata method: the follow-up receipt records the substantive SHA; its own
  final SHA is reported externally rather than embedded in its tree.
