# BC-041-C1 - Validation Record

status: complete
owner: Codex
last_reviewed: 2026-08-12

## Environment and lineage

- Host: Windows, PowerShell
- Python: 3.12.10
- Schema runtime: `jsonschema==4.26.0`, Draft 2020-12
- Original authorized base: `33b44608cb634d1fedeed7f5f70d405c3999ed02`
- Correction starting point: `c6a447679c0ca07fb38a1e35eeb00231b0cb91e1`
- Branch: `bc-041-c1-outer-edge-cf-correction`
- Claude review evidence only:
  `f87588d0fa094c203fde3b847ab9bc3c28d1b3fe`

The correction branch was created directly from `c6a4476`. Claude's review
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
Python readiness: validator passed; 17 tests OK
BC-041-C1 OPSEC: validator passed; 36 tests OK
```

The preserved host-adapter output is:

```text
ERROR: protected path changed from BC-020 base: contracts/successor/unresolved_register.json
host adapter contract validation failed: 1 error(s)
```

This is the known BC-020 fixed-base protected-path finding. The correction does
not change that path. It was not suppressed and is not reported as a pass.

## B-1â€³ expanded proof

The mechanism still uses one candidate: remove all Unicode general-category
`Cf`, apply the existing normalization pipeline, and let normalized inter-word
rule separators match zero-or-more spaces. The candidate now also carries
normalized offsets for removed-`Cf` boundaries. An outer phrase guard accepts a
real non-word neighbour or such an offset; no offset means ordinary Unicode
word adjacency remains a nonmatch. Contiguous repeated matches of the same rule
form one fail-safe run. Candidate count is constant one.

```text
required code points: U+200B, U+00AD, U+200D, U+200C, U+FEFF, U+2060
per-phase exact Cf fixtures: 42
per-phase exact outer-edge matrix: 6 code points x 3 outer positions = 18
per-phase additional attack classes: 5
ingress protected fixtures: 42/42 BLOCK; model eligible 0/42
egress protected fixtures: 42/42 REDACTED or BLOCKED; CLEAR 0/42
deterministic adversarial probes: 54,740
adversarial ingress/egress failures: 0
ordinary ASCII/Unicode adjacency probes without Cf: 6
ordinary adjacency false matches: 0
existing negative ingress fixtures: 5/5 PASS
```

The 54,740 probes include all six code points at every single interior
position, every pair of interior positions with every ordered code-point pair,
2,000 seeded mixed-code-point triples, 45,000 seeded 4-12 insertion cases, and
leading/trailing/both outer edges at repeat counts 1, 2, and 8. Each probe was
evaluated symmetrically at ingress and egress. This re-proves B-1' while adding
B-1â€³ coverage.

Direct controls cover outer+interior mixing, mixed-code-point outer edges,
repeated outer edges, outer plus repeated interior insertions, unseparated
self-repetition, no-`Cf` prefix/suffix/both adjacency, and non-ASCII Unicode
word neighbours. Protected ingress never reaches Turn Controller/model
eligibility. Protected egress never returns `CLEAR` or printable raw protected
content.

Redaction proof includes multi-span redaction, outer-edge spans,
self-repetition, post-redaction rescan using the same matcher, redaction-only
output blocking, policy `BLOCK`, and overlapping-span fail-closed behavior.
`_has_overlapping_spans` remains the primary integrity guard; its direct test
passes and B-1â€³ exposed no defect requiring redesign.

## Readiness coupling and documentation

`validate_python_readiness.py` executes the OPSEC validator. One mutation test
deletes mixed ingress fixtures; another deletes outer-edge egress fixtures and
their attack classes. Both make green readiness fail. Technical
`ready_for_python_phase1` is therefore earned only with B-1'/B-1â€³ proof intact.

Independent Claude re-review remains `required_pending` and incomplete;
`implementation_authorized` remains false; automatic start remains prohibited;
Dad/Blu closure remains required.

The paragraph above records the correction-branch handoff state and is
superseded by the final closure validation below. It is retained as historical
evidence rather than rewritten.

The contract and README disclose that non-`Cf` default-ignorable/invisible
characters and general confusable/homoglyph mechanisms are outside this bounded
Phase-1 matcher. They also state that zero-space protected-rule separators are
intentional fail-safe recovery when `Cf` removal destroys separation, not an
accidental fuzzy-match claim.

## Evidence, policy, and negative behavior

- Evidence HMAC uses the sole normalized decision candidate.
- Ingress and non-clear egress results are scanned for synthetic protected
  values and the synthetic evidence key; results remain content-safe.
- Missing, unavailable, malformed, schema-invalid, integrity-mismatched, and
  unusable policies continue to fail closed.
- SecurityDecision remains exactly `PASS | BLOCK | ASK`; only `PASS` is model
  eligible.
- The five pinned negatives remain `PASS`, including
  `punctuation_adjacent_nonmatch`, `shared_words`, and `near_match`.

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

No production protected value, policy location/digest, credential, private key,
runtime/provider/Auth path, continuity mutation, tool, or PASS/SkillForge
crossover was added. The golden CTS and Claude-owned review evidence remain
unchanged.

## Limitations

These checks establish only the bounded public contract and synthetic
conformance proof. They do not prove production policy completeness or
classification, non-`Cf` invisible/default-ignorable resistance, general
confusable/homoglyph resistance, semantic paraphrase detection, live model/LM
Studio behavior, Auth, protected continuation, or a production runtime.

## Commit identity

- Substantive outer-edge correction:
  `85e18f56f88ab113646cc3aab477687eda8b85af`.
- Metadata method: the follow-up receipt records the substantive SHA; its own
  final SHA is reported externally rather than embedded in its tree.

## Final integration and administrative closure validation — 2026-08-12

### Integration and review provenance

```text
fetched current origin/main: 131a527a8fef1f42df327443c9966c9e2f66f528
reviewed correction tip: 204a229e2c01b255f1a940129cb724fa33fb4755
correction tip is ancestor of current main: true
final Claude review source: f0998f78aaada899a16d4413170ef3689f04fe28
imported-review integration: 3e77111b6d86879f591c7ab8c52a571c51e7c48e
review source/imported blob: 25907b4bd76400c6c01238da771c6a62c783b5de
review blob exact: true
review changes after import: 0
```

Claude's final disposition is `approve-with-notes` with zero blocking
findings. The review branch was not merged. The original BC-041
`return-for-correction` record remains byte-identical to its original review
commit.

### Complete validation commands and results

The final staged closure state was validated with:

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
python tools/validate_opsec_contracts.py
python -m unittest discover -s tests/security -p "test_*.py"
python tools/validate_python_readiness.py
python -m unittest discover -s tests/readiness -p "test_*.py"
```

Observed final results:

```text
cached diff check: passed
runtime contracts: validator passed; 21 tests OK
viability audit: validator passed; 9 tests OK
historical archives: validator passed; 12 tests OK
historical archaeology: validator passed; 18 tests OK
successor kernel: validator passed; 40 tests OK
host adapters: standalone validator retained one known fixed-base finding; 34 tests OK
continuity: validator passed; 42 tests OK
OPSEC: validator passed; 36 tests OK
Python readiness: validator passed; 18 tests OK
```

The host-adapter finding remains exactly:

```text
ERROR: protected path changed from BC-020 base: contracts/successor/unresolved_register.json
host adapter contract validation failed: 1 error(s)
```

It is the established BC-020 fixed-base finding and was neither suppressed nor
reported as clean. The first closure run also correctly exposed that the OPSEC
and readiness validators still required the pre-closure `required_pending`
review state. Their exact state assertions were transitioned to require the
approved final review and Dad/Blu closure receipts; focused validators and all
54 OPSEC/readiness tests then passed. The implementation-authorization mutation
still fails.

### Integrity, scope, and final state

```text
golden CTS checksums: 8/8 passed
golden changed paths: 0
successor components / packets / interfaces: 7 / 8 / 9
canonical manifest entries: 278
manifest missing / extra / duplicate / digest mismatch: 0 / 0 / 0 / 0
original BC-041 review unchanged: true
final C1 review exact and unchanged after import: true
production Python outside tools/tests: 0
production runtime/provider roots present: 0
SUR-002 / SUR-011 / SUR-012 broadened: false
real protected-policy values in tracked content: 0
```

Final readiness is `ready_for_python_phase1`; `actual_blockers` is `[]`;
`runtime_phase1_packet_may_be_authored_next` is `true`; independent correction
review and Dad/Blu closure are complete. `implementation_authorized` remains
`false`, `automatic_start_prohibited` remains `true`, and Python Runtime Phase 1
has not started. Closure adds no production runtime, LM Studio provider, Local
Mirror provider, Auth implementation, protected policy value, architecture
change, continuity mutation, or PASS/SkillForge work.

The closure substantive commit is recorded by the metadata-only closure
receipt after creation.
