# BC-050 / BC-050-C1 — Independent Implementation Review

status: return-for-correction
owner: Codex
reviewer: Codex
project_lead: Blu
project_owner: Dad
domain: runtime
last_reviewed: 2026-08-13

## Review identity

- Assignment: `BC-050 — Python Runtime Phase 1 — Boot + Ordinary Turn + LM Studio Model Boundary`
- Correction: `BC-050-C1 — Authorized-Implementation Validator Alignment`
- Authorized base: `973589eea05fe42deeb829c5435bd09faf8cbe70`
- Implementation commit: `708101d7f6dfc7748bb69d71f56e4da1044a2699`
- C1 correction / branch tip reviewed: `218f3aed941afe0476d3d211af0146426d1be32e`
- Branch: `bc-050-c1-validator-alignment`
- Reviewer: Codex, independently of implementation author Claude
- Review type: implementation, security/control-flow, One-Blu parity, and C1 validator alignment
- Integration commit or merge identity: none
- Live LM Studio smoke test: `not_performed`; no live environment was supplied

The checkout was clean at review start, on the expected branch, exactly at the
C1 correction commit. The authorized base is an ancestor of the tip. No
implementation fix was made during review.

## Sources compared

The review read the required governance and runtime continuity sources, the
canonical assignment packet, handoff, validation record, full implementation
and test suite, C1 diff, frozen readiness/provider/configuration/OPSEC/
successor/continuity contracts, and the relevant golden source files. It also
inspected the complete base-to-tip path diff and protected boundaries.

## Executive result

Disposition: `return-for-correction`.

The branch preserves the 7/8/9 architecture and frozen canon envelope. Its
production OPSEC normalization also remained differential-equivalent to the
protected reference in additional review probes. Seven blocking findings
remain, so BC-050 is not `ready_for_Dad_Blu_integration_review`.

## Blocking findings

### B-01 — C1 authorization gates do not authenticate one complete record

- Affected functions: the three validators' `_bc050_authorized` functions and
  their authorization-dependent implementation guards.
- Violated contract: the BC-050-C1 decision that one authorization record has
  three independent enforcement points and malformed evidence restores every
  validator's pre-implementation rejection.

Each validator was run independently in a clean temporary clone after one
authorization mutation at a time:

| Mutation | Python readiness | OPSEC | Continuity |
| --- | --- | --- | --- |
| wrong `authorized_by` (`Mallory`) | reject | **accept** | **accept** |
| empty `authorized_by` | reject | reject | **accept** |
| wrong non-empty packet path | **accept** | **accept** | **accept** |
| empty packet path | reject | reject | **accept** |
| missing packet field | reject | reject | **accept** |
| wrong assignment | reject | reject | reject |
| slice authorization flag disagrees | reject | reject | **accept** |
| slice authorization record names `BC-999` | **accept** | **accept** | **accept** |

Minimum reproduction: change checklist `authorized_by` to `Mallory` and run
the OPSEC validator; it passes and relaxes its pre-implementation guard. Change
the packet to a wrong non-empty path; all three validators pass independently.

Continuity checks only state, assignment, and the checklist boolean before
allowing `src/blu_runtime/**` and runtime Python diffs. OPSEC accepts any
non-empty authorizer and packet. Readiness checks the exact authorizer only
after its weaker predicate selects the authorized path, accepts any non-empty
packet, and does not authenticate the slice's nested authorization record.

Expected: every validator that relaxes a no-implementation guard authenticates
the same complete exact BC-050 record itself. Validator ordering is not an
authorization mechanism.

Smallest correction property: use one identical fail-closed predicate at all
three enforcement points, binding at least exact state, assignment, authorizer,
date, canonical packet path, authorization flags, and cross-file agreement.
Add the complete mutation matrix above to each independent validator suite.

### B-02 — The One-Blu parity mapping silently drops applicable law

- Affected record: `BC-050/validation.md`, `00_Instructions.md` parity mapping.
- Runtime cause: `00_Instructions.md` is excluded from the frozen prompt, while
  missing behavior is neither in Persona/Operations Law nor deterministically
  enforced.
- Violated contract: BC-050 §§3.1 and 17.2; One-Blu law.

Minimum source comparison: `00_Instructions.md` defines exact Verb Lock rules
such as `read = read content`, `compare = compare`, and
`summarize = summarize`. The table maps Verb Lock to Operations Law's general
Execution Discipline Doctrine, but exact search and semantic inspection found
no equivalent verb rules in Persona or Operations Law. The wrapper implements
no deterministic verb lock.

Material parts of Execution Law, Completion Proof, and Compliance Gate are
similarly mapped to broader, non-equivalent prose. The whole Bootloader section
is called a correctly omitted GPT-only mechanic even though its restraint order
and fail-closed rules are directly applicable and implemented by the wrapper.

Observed: broadly similar operational prose is treated as semantic
equivalence. An ordinary Python/local-model turn can therefore receive a
“compare” or “summarize” request without the current exact Verb Lock.

Expected: every applicable instruction has an exact authoritative destination
or deterministic enforcement. Similar tone or general discipline is not
semantic parity.

Smallest correction property: redo parity at rule granularity. Any applicable
rule with no permissible exact destination is a packet/authority contradiction
for Dad/Blu to resolve, not a semantic-equivalence claim. Do not modify golden
canon through the correction.

### B-03 — Missing chat-compatibility evidence is accepted as usable

- Affected function: `src/blu_runtime/providers/model/lm_studio.py::observe`.
- Affected condition: it rejects an incompatible type only when `type` is
  present.
- Violated contract: BC-050 §8.2 requires positive chat-compatibility evidence.

Minimum reproduction: return the correct model key, a loaded instance with a
valid ID, and sufficient context, but omit `type`.

Observed: `usable=True`, `safe_error_code=None`.

Expected: `UNAVAILABLE` and zero inference because absent type/capability data
does not prove chat compatibility.

Smallest correction property: require explicitly observed chat-compatible
type/capability; absent or malformed compatibility fails closed. Add a
missing-type test alongside the existing wrong-type test.

### B-04 — Error, nonterminal, and identity-conflicting results become success

- Affected function:
  `src/blu_runtime/providers/model/lm_studio.py::normalize_response`.
- Violated contract: BC-050 §9 and the provider contract's
  `response_completion` rule.

Independent synthetic results using the expected model instance and a message:

| Mutation | Observed |
| --- | --- |
| add `provider_id: not_lm_studio` | `PASS`, candidate accepted |
| add timeout/error and `status: error` | `PASS`, partial candidate accepted |
| add `status: processing` | `PASS`, nonterminal candidate accepted |

The normalizer checks model instance and output items but does not reject a
provider error, require terminal response evidence, validate request/provider
identity evidence, or reject conflicting identity fields when present.

Expected: unresolved provider error, partial/nonterminal result, or identity
conflict never yields candidate text or a terminal reply.

Smallest correction property: validate the complete evidenced native
completion shape before consuming output. Provider/request identity may be
bound through the frozen transport contract, but present conflicts must reject,
and terminal completion with no unresolved error must be positively observed.
Pin all three reproductions.

### B-05 — CLEAR egress prints raw instead of canonicalized output

- Affected function:
  `src/blu_runtime/core/validation_egress.py::evaluate_egress`.
- Affected property: the no-match path assigns `public_output=text`.
- Violated contract: BC-050 §10 requires the public form to be the canonicalized
  candidate only and forbids reconstructing raw candidate text for output.

Minimum reproduction: evaluate safe text `ordinary<U+200B> reply`.

Observed:

```text
egress_result=CLEAR
normalized_candidate='ordinary reply'
public_output='ordinary\u200b reply'
raw_preserved=True
```

Expected: printable CLEAR output is the canonical candidate used by OPSEC,
never raw untrusted provider text.

Smallest correction property: authorize and print only the canonical candidate
on CLEAR and REDACTED paths. Add harmless-`Cf`, separator, whitespace-collapse,
and NFKC regression cases.

### B-06 — `/exit` and `/quit` bypass the turn and terminal result

- Affected functions: `TerminalHostAdapter.receive` and runtime `main`.
- Violated contract: BC-050 §§6 and 7.1 and the frozen one-terminal turn
  sequence. All slash commands are unsupported; no exception is defined.

Minimum reproduction: submit `/exit\n` through `receive()`.

Observed: `None`; no RawHostEvent, SecurityDecision, ControlDecision,
TerminalPacket, or terminal reply. The CLI advertises `/exit` as operative.

Expected: text beginning with `/` follows the pre-ingress/controller path,
terminates unsupported before inference, and produces one safe terminal result.
End-of-file may end the host session out of band.

Smallest correction property: remove in-band slash interception or define a
separately authorized non-text host control. Pin `/exit` and `/quit` to zero
provider invocations plus one terminal packet/reply.

### B-07 — Missing completion evidence is replaced with invented evidence

- Affected function: `src/blu_runtime/__main__.py::run_turn`.
- Affected expression: `result.completion_evidence_ref or
  f"provider-completion:{identifier}"`.
- Violated contract: BC-050 §§9 and 12, Completion Proof, and Truth Discipline.

Minimum reproduction: return an otherwise PASS `NormalizedModelResult` with
`completion_evidence_ref=None`.

Observed:

```text
terminal status=PASS
receipt count=1
provider_completion_evidence_ref=provider-completion:review-request
```

The fallback is a generated label, not observed completion evidence.

Expected: absent completion evidence prevents a successful receipt and terminal
success; proof is never synthesized.

Smallest correction property: require validated non-empty completion evidence
for PASS and remove the fallback. Add a boundary-level negative test proving
missing evidence cannot produce output or a receipt.

## Non-blocking notes

### N-01 — Editable install remains unverified, accurately disclosed

`setuptools` is absent (`find_spec("setuptools") -> None`), so an offline
editable install was not attempted. The authorized external `PYTHONPATH=src`
fallback imports the package and runs tests normally. No `.egg-info` artifact
exists, and the handoff does not falsely claim `pip install -e .` passed.

### N-02 — Live LM Studio smoke test was not performed

No live environment was supplied. No live-provider result is claimed.

### N-03 — Internal continuity mutation lacks a defensive invariant

The supported boot path always returns `lifetime=turn`, provider unavailable,
and `durability_claimed=false`. Directly replacing the mutable runtime's
internal record with `provider_available=false`, `durability_claimed=true` is
carried into a successful packet without validation. No supported external
Phase-1 path performs that mutation, so this is not a current blocker. A future
provider must add a boundary invariant rather than trusting arbitrary data.

## Packet-compliance findings

### Architecture and support layer

- Architecture remains exactly 7 components, 8 packets, and 9 interfaces.
- `PendingAuthorizationState` remains a state record.
- No prohibited service, LM Studio component, or eighth component was added.
- `contracts/successor/**` is unchanged from the authorized base.
- Canon/config/contracts support modules do not choose canon or add architecture.
- `__main__.py` does not fully satisfy zero authority because B-07 invents
  provider completion evidence.

Architecture counts pass; support-layer evidence authority does not.

### One-Blu

The runtime loads golden Persona and Operations Law and ships no Python-,
provider-, or model-specific Persona. No Markdown behavioral source exists
under `src`. B-02 nevertheless creates a behavioral fork for applicable
Instructions law absent from both prompt and deterministic enforcement.

### Canon envelope and digest

Independent packet-derived construction—not runtime helpers—produced:

```text
rendered envelope bytes 36887
canon_projection_digest 103e0e2dd94183c914dc8c46e3ac376af516382548e17af40c14c27d3319f142
final byte              0x5D
Persona seam            double LF before close
Operations Law seam     single LF before close
```

Raw golden bytes matched checksums before decoding. The two model-facing
sources and exclusions are exact. This finding passes.

### Configuration and protected-policy boot

Independent probes returned `UNAVAILABLE`, with provider observation and
inference both zero, for missing, unreadable, malformed, schema-invalid,
digest-mismatched, and unusable policies. Invalid configuration returned
`INVALID` with both counts zero. No permissive fallback or production protected
value was found. This finding passes.

### OPSEC differential, boundedness, and provenance

An additional seeded corpus of 6,036 generated and targeted cases covered the
six required `Cf` code points, mixed/repeated placement, edges, outer/interior
combinations, separators, NFKC-relevant text, and self-repetition.

```text
(normalized_candidate, removed_cf_boundaries) mismatches: 0
2,000 removals x3:   0.256 ms
8,000 removals x3:   1.018 ms
32,000 removals x3:  3.902 ms
```

Inspection and observed scaling support bounded, non-quadratic construction.
No provenance loss was found. The C1 diff leaves the twelve OPSEC mechanism
functions and six governing constants unchanged. This finding passes.

### Ingress, route, and egress

Independent protected-ingress, `/auth`, and unexpected-ASK probes all observed
provider invocation count zero. The required committed invalid-config, canon,
policy, and provider-evidence cases also passed. B-06 is a separate terminal
adapter bypass.

Forty-two additional protected egress candidates produced zero CLEAR results.
Redaction/blocking worked for those attacks. Overall egress still fails B-05
because safe CLEAR prints the raw candidate.

### LM Studio boundary

LM Studio remains below Model Execution Boundary. No lifecycle, fallback model,
multi-model routing, tools, MCP, streaming, storage, or provider continuation
was introduced. Request fields match the frozen native profile. The finding
fails B-03 and B-04.

### Continuity and receipt

The supported path claims no durable provider, persistence, model memory, or LM
Studio continuity. Lifetimes remain `none|turn|host_session|durable_external`,
with no bare `session`; SUR-011 remains unresolved. This passes with N-03 noted.

The success receipt has the nine required fields when evidence is present, but
B-07 makes the receipt finding fail when evidence is absent.

### C1 alignment and readiness truth

C1 correctly restricts authorized Python to `src/blu_runtime/**` and
`tests/runtime_phase1/**`; an independent `src/blu_runtime_evil/engine.py`
mutation was rejected. Other prohibited roots remain guarded, automatic start
remains independently true, and the OPSEC mechanism is unchanged.

B-01 means C1 does not complete its fail-closed goal. Disposition on the
explicit review question: **blocking fail-closed defect requiring validator
alignment**.

Readiness records truthfully distinguish technical readiness, explicit
authorization, implementation presence, pending independent review, and absent
integration approval. They no longer claim authorization pending. Their
authentication is insufficient under B-01.

### Repository boundaries and known BC-020 finding

- Golden CTS, closed OPSEC evidence, successor architecture, source authority,
  Local Mirror, Auth, tools/MCP, PASS/SkillForge, Custom GPT configuration, and
  production protected values are unchanged.
- SUR dispositions are preserved; SUR-011 remains unresolved.
- No untracked `.egg-info` exists.
- Temporary review probes were removed before this record was written.

The host-adapter validator's one known fixed-base finding was reproduced at the
authorized base `973589ee`: it reports the historical change to
`contracts/successor/unresolved_register.json`. BC-050 did not touch that path.
There is no suppression, widening, or new BC-050 host-adapter regression, so it
is not a BC-050 blocker.

## Validation executed

### Required suites

| Command | Result |
| --- | --- |
| `$env:PYTHONPATH='src'; python -m unittest discover -s tests/runtime_phase1 -p "test_*.py"` | 119 tests, OK |
| `python -m unittest discover -s tests/security -p "test_*.py"` | 49 tests, OK |
| `python -m unittest discover -s tests/readiness -p "test_*.py"` | 32 tests, OK |
| `python -m unittest discover -s tests/continuity -p "test_*.py"` | 50 tests, OK |

Other suites passed: contracts 21, successor kernel 40, viability 9,
historical archives 12, historical archaeology 18, and host adapters 34.

The following validators passed independently:

```text
python tools/validate_opsec_contracts.py
python tools/validate_python_readiness.py
python tools/validate_continuity_contracts.py
python tools/validate_runtime_contracts.py
python tools/validate_successor_kernel_spec.py
python tools/validate_viability_audit.py
python tools/validate_historical_archive_inventory.py
python tools/validate_historical_behavioral_archaeology.py
```

`python tools/validate_host_adapter_contracts.py` returned only the known
BC-020 fixed-base finding described above.

The requested `sha256sum` executable is unavailable on this Windows host. The
PowerShell `Get-FileHash -Algorithm SHA256` equivalent verified all seven
golden Markdown files and the source ZIP as OK.

## Required follow-up

Return BC-050/BC-050-C1 to the implementation owner for bounded correction of
B-01 through B-07. Do not merge, close BC-050, begin Python Phase 2, or begin
Local Mirror, Auth, tools, PASS, SkillForge, or Custom GPT work.

The next independent review must rerun the complete suite and every minimum
reproduction above. Dad/Blu retains final integration authority.

## Disposition

`return-for-correction`

## Final status authorization

- Authorized by: not applicable; integration is not authorized by this review
- Assignment status: return to active correction under Dad/Blu direction
- Date: 2026-08-13

---

# Independent Re-Review After BC-050-C2 / BC-050-C2A

## Re-review identity

- Date: 2026-08-13
- Exact target: `25ef59adc6c79edeb3f6347f5f51a5cb072da500`
- Branch: `bc-050-c2a-instruction-classification`
- Authorized base: `973589eea05fe42deeb829c5435bd09faf8cbe70`
- Implementation: `708101d7f6dfc7748bb69d71f56e4da1044a2699`
- C1: `218f3aed941afe0476d3d211af0146426d1be32e`
- Prior independent review: `33be23a4c43a160e41e2aeca78962d1cbd3c4a47`
- C2: `b6333a761e9dbfe310fd1ce0e3203beabe3fefdf`
- C2A: `25ef59adc6c79edeb3f6347f5f51a5cb072da500`
- Reviewer: Codex, independently of implementation author Claude
- Live LM Studio smoke test: `not_performed`

The checkout was clean, exactly at the requested target, and the authorized
base was an ancestor. C2A changed no file under `src/blu_runtime/**`. No
implementation fix was made during review.

## Executive result

Disposition: `return-for-correction`.

C2/C2A resolve the amended B-02 question and the substantive B-03 through B-05
defects. The slash-command control flow and the missing/blank completion-
evidence cases are also corrected. Three fresh adversarial findings remain:

1. B-01 still accepts a jointly wrong or non-string authorization date at all
   three independent enforcement points.
2. B-06 still advertises `/exit` as an operative exit command even though the
   corrected runtime classifies it as unsupported and continues the session.
3. B-07 raises `AttributeError` for a truthy non-string completion-evidence
   reference instead of returning one terminal fail-closed result.

BC-050 is therefore not `ready_for_Dad_Blu_integration_review`.

## Remaining blocking findings

### B-01 — authorization date is cross-file-consistent but not authenticated

- Affected functions: `_bc050_authorized` in
  `tools/validate_python_readiness.py`, `tools/validate_opsec_contracts.py`, and
  `tools/validate_continuity_contracts.py`.
- Minimal reproduction: change both `authorization_date` values in
  `readiness/python_phase1_readiness_checklist.json` and
  `readiness/phase1_executable_slice.json` from `2026-08-12` to `1999-01-01`,
  or to integer `7`, then evaluate each validator's gate independently.
- Observed: all three return authorized. Every originally requested mutation
  (wrong/empty authorizer, wrong/empty/missing packet, wrong assignment,
  checklist/slice disagreement, nested other assignment, malformed partial
  record, malformed/missing JSON, and `automatic_start_prohibited: false`)
  correctly returns unauthorized.
- Expected: the authorization record must bind the actual Dad/Blu authorization
  date `2026-08-12` as an exact string, not merely require two truthy equal
  values.
- Governing rule: BC-050 authorization gate; prior B-01 smallest correction
  property requiring exact state, assignment, authorizer, date, canonical
  packet, flags, and cross-file agreement; C2's stated complete-record,
  fail-closed predicate.
- Smallest bounded correction property: bind an exact approved date constant in
  all three predicates, require the same exact string in both records, and add
  jointly wrong and non-string date cases to the shared independent matrix.

### B-06 — startup text falsely advertises `/exit`

- Affected location: `src/blu_runtime/__main__.py::main`, startup banner.
- Minimal reproduction: boot successfully, observe `"/exit to end."`, then
  submit `/exit`.
- Observed: the corrected adapter creates a `RawHostEvent`; ingress runs; Turn
  Controller returns `UNAVAILABLE / ROUTE_UNSUPPORTED`; provider invocation
  count is `0`; one terminal result is rendered; the session continues. The
  preceding banner nevertheless claimed `/exit` would end it.
- Expected: no in-band slash command is represented as an operative host
  bypass. Only EOF/out-of-band stream end terminates the session in Phase 1.
- Governing rule: BC-050 sections 6, 7.1, and the fixed terminal sequence;
  One-Blu truthfulness/runtime-truth discipline; B-06's no-magic-command rule.
- Smallest bounded correction property: remove the `/exit to end` claim from
  the startup text (or replace it with truthful EOF/out-of-band guidance)
  without restoring any slash interception.

### B-07 — truthy malformed completion evidence crashes the turn

- Affected function: `src/blu_runtime/__main__.py::run_turn`, expression
  `(result.completion_evidence_ref or "").strip()`.
- Minimal reproduction: return an otherwise PASS `NormalizedModelResult` with
  `completion_evidence_ref=7` from the Model Execution Boundary and call
  `run_turn`.
- Observed: `AttributeError: 'int' object has no attribute 'strip'`; no receipt
  is written, but no terminal packet/result is produced. `None`, empty string,
  whitespace-only string, empty mapping, and empty list do fail closed as
  `INVALID / PROVIDER_COMPLETION_EVIDENCE_MISSING` with no output or receipt.
- Expected: malformed completion evidence is untrusted provider output and must
  yield one terminal failure, never an exception or success receipt.
- Governing rule: BC-050 sections 9, 12, and 13; provider-contract malformed-
  response rule; Completion Proof and one-terminal-result discipline.
- Smallest bounded correction property: require
  `isinstance(completion_evidence_ref, str)` and a nonblank value before any
  string operation or receipt construction; pin truthy non-string values at the
  boundary-level negative test.

## Prior blocker disposition

### B-02 — resolved under the Dad/Blu C2A authority amendment

The review applied the amended question, not the superseded instruction-parity
premise.

- Golden `00_Instructions.md` passes its recorded SHA-256 and is unchanged from
  the authorized base.
- It appears exactly once under `legacy_deployment_artifacts` with
  `successor_invariant: false`, `python_projection: none`,
  `cross_deployment_parity_required: false`,
  `automatic_behavior_migration: false`, and `immutable_golden: true`.
- It appears in no invariant mapping. CANON-006 does not cite it. CANON-009
  remains Persona + Operations Law plus approved successor/provider contracts.
- Deployment targets classify host instruction surfaces as deployment-local
  and non-parity-determining. The parity matrix retains eleven actual Blu
  dimensions: identity, relational posture, tone floor, behavioral law,
  truthfulness, teaching, privacy/security, refusal/boundary posture,
  continuity truth, source authority, and unsupported-completion discipline.
- No instruction text entered the envelope, no generated projection or third
  prompt appeared, no semantic judge was added, and no golden source changed.
- Fresh temporary mutations restoring an invariant mapping, CANON-009 source,
  successor security source, Python projection, `host_binding_projection`, or
  parity dependency all caused readiness validation to fail. An unmodified
  temporary repository copy returned zero readiness errors.

Independent inspection found the successor invariant still owned by Persona,
Operations Law, and deterministic successor contracts. B-02 is resolved by
source reclassification, not by false equivalence.

### B-03 — resolved

Fresh inventory probes for missing, null, list-valued, and explicitly
incompatible model `type` all returned unusable
`PROVIDER_MODEL_INCOMPATIBLE`; Model Execution Boundary invocation count stayed
`0`. An exact compatible `llm` type was the only usable case. Compatibility was
not inferred from model name, loaded state, or context capacity.

### B-04 — resolved for the supported LM Studio normalizer

Fresh responses with conflicting provider identity, provider error plus text,
timeout plus text, `processing`, missing status, non-string status, or
conflicting model identity produced no candidate and returned `INVALID` or
`UNAVAILABLE` with the matching safe code. A completed, identity-matching
response with provider-assigned evidence was the only PASS case.

### B-05 — resolved

`ordinary<U+200B> reply` publicly returned exactly `ordinary reply`.
Whitespace collapse, separator mapping, NFKC full-width forms, a compatibility
ligature, and mixed normalization all returned the exact canonical candidate.
Protected output returned REDACTED canonical text, never CLEAR raw text. Source
inspection found no post-authorization reintroduction of the raw provider text.

### B-06 — control-flow defect resolved; truthful-banner residue blocks

Fresh `/exit`, `/quit`, and `/auth` probes each created a `RawHostEvent`, ran
ingress and unsupported routing, produced one terminal result, and invoked the
provider `0` times. EOF returned no event and remained distinct. The residual
blocking banner defect is recorded above.

### B-07 — missing/blank defect resolved; malformed-value defect blocks

`None`, empty, and whitespace-only evidence produced no PASS, public output,
receipt, or synthesized reference. `__main__.py` contains no fallback evidence
generation. The residual truthy non-string exception is recorded above.

## Foundational and adversarial evidence

### Required suites

| Suite | Result |
| --- | --- |
| Runtime Phase 1 | 154 tests, OK |
| Security | 50 tests, OK |
| Readiness | 53 tests, OK |
| Continuity | 58 tests, OK |

Additional suites passed: contracts 21, successor kernel 40, viability 9,
historical archives 12, historical archaeology 18, and host adapters 34.

### Validators

Passed independently:

```text
python tools/validate_opsec_contracts.py
python tools/validate_python_readiness.py
python tools/validate_continuity_contracts.py
python tools/validate_runtime_contracts.py
python tools/validate_successor_kernel_spec.py
python tools/validate_viability_audit.py
python tools/validate_historical_archive_inventory.py
python tools/validate_historical_behavioral_archaeology.py
```

`python tools/validate_host_adapter_contracts.py` returned only the known BC-020
fixed-base finding: `contracts/successor/unresolved_register.json` changed after
the validator's BC-020 base. BC-050/C2/C2A did not modify that protected path;
no suppression or new host-adapter regression was found.

### Canon, golden, manifest, and architecture

Independent assignment-derived envelope construction reproduced:

```text
rendered envelope bytes  36887
canon_projection_digest  103e0e2dd94183c914dc8c46e3ac376af516382548e17af40c14c27d3319f142
final byte               0x5D
```

All seven golden Markdown files and the CTS ZIP passed the PowerShell
`Get-FileHash -Algorithm SHA256` equivalent against `SHA256SUMS`. Base-to-target
golden diff was empty. `git diff --check` passed. The readiness, continuity, and
successor validators independently accepted `MANIFEST.sha256` coverage and
digests. Architecture remains 7 components, 8 packets, and 9 interfaces.

### OPSEC differential and performance

A fresh seeded corpus of 6,035 cases covered all six required `Cf` code points,
edges, inside-token and inter-word placement, separators, NFKC and compatibility
forms, repetitions, and negative controls. Production and
`tools/validate_opsec_contracts.py::normalized_match_candidate` had zero
mismatches for normalized text and removed-`Cf` boundaries.

Three-run timings for 2,000, 8,000, and 32,000 removals were 3.866 ms,
16.906 ms, and 72.334 ms. The approximately linear scaling remains bounded and
non-quadratic.

Fresh protected-ingress input terminated BLOCK with provider invocation count
`0`. Protected egress was REDACTED, not CLEAR. An unsupported `/memory` route
terminated UNAVAILABLE with provider invocation count `0`.

### Continuity truth

No durable provider appeared. Phase 1 still reports `lifetime=turn`,
`provider_available=false`, and `durability_claimed=false`. Model context,
process memory, LM Studio state, and filenames are explicitly rejected as
continuity evidence. SUR-011 remains unresolved.

### Packaging and import truth

No internal `sys.path` mutation returned. The external `PYTHONPATH=src` fallback
worked for the runtime suite. `setuptools` remains absent, so editable install
was not performed and is not reported as passed. No tracked or untracked
`.egg-info` affected manifest validation.

## Nonblocking notes and prerequisites

### N-01 — live LM Studio compatibility smoke remains `not_performed`

Deterministic provider-contract validation is internally coherent and fails
closed. Repository evidence does not pin the native response terminal-state or
provider-response identifier field names. A live LM Studio smoke test remains
a nonblocking live-smoke prerequisite before integration/operational use; if
the names differ, ordinary turns will safely remain unavailable until a bounded
contract-aligned correction is reviewed. No live success is claimed.

### N-02 — punctuation canonicalization is contract-conforming but poor presentation

`Hello, Dad.` becomes `Hello Dad`. This is the intended consequence of the
frozen OPSEC `public_form: canonicalized candidate only` contract, not a
security bypass or a semantic defect in B-05. It is a presentation-quality note
for a future explicitly authorized print-safe canonicalization decision.

### N-03 — root README current-truth line is stale for an integrated BC-050

Root `README.md` still says `No Python Blu runtime exists in this bootstrap
release.` In historical bootstrap context that sentence is understandable, but
under the `Current truth` heading it becomes stale once BC-050 is integrated.
Treat this as a bounded integration cleanup item; it was not edited during
review and is not independently blocking the correction branch.

## Required follow-up

Return BC-050/C2/C2A to the implementation owner for bounded correction of the
three findings above. Re-review the exact correction target. Do not merge,
close BC-050, begin Python Phase 2, or begin Local Mirror, Auth, tools, PASS,
SkillForge, or Custom GPT changes. Dad/Blu retains final integration authority.

## Final disposition

`return-for-correction`

---

# BC-050 Final Authority Reconciliation and Freeze Review

status: accepted_and_frozen
reviewer: Codex
authority: Dad/Blu
review_target: `ed76f311976fba62e26356af6c4e145aa8ee2d6e`
superseded_review_record: `31476a1309589a989d709e45cb8c0fbdce2f7e6a`
review_date: 2026-08-14
disposition: approve-with-notes

## Executive result

Disposition: `approve-with-notes`.

Dad/Blu superseded the sole blocking requirement in the immediately preceding
review. For LM Studio native REST v1 synchronous stateless inference, `stats`
is non-authoritative telemetry and is not used as completion proof, identity,
authorization, authentication, security, routing, model-output, continuity, or
other evidence. Missing or malformed telemetry does not invalidate an otherwise
structurally valid completion when no authoritative claim depends on it.

That clarification corrects the review requirement; it is not a runtime-code
waiver. The reviewed C5A implementation already treats `stats` as irrelevant to
proof. No production correction is authorized or required for that behavior.

No other blocker remains in the C5A review record, and this reconciliation
identified no new independently reproducible blocker. BC-050 is accepted and
frozen as the completed Phase-1 experimental/local runtime slice.

## Blocking findings

None.

### C5A-B01 — superseded as a blocker

The prior reproduction remains historically accurate: malformed `stats` was
ignored and the otherwise valid response completed. Dad/Blu authority now
establishes that this is the required evidentiary treatment because `stats` is
irrelevant telemetry. Promoting that malformed telemetry into authoritative
failure evidence would exceed its role.

Retained nonblocking note: if a future contract makes a public, routing,
security, authorization, identity, completion-proof, or continuity claim depend
on a telemetry field, that new use must define and validate the field under its
own separately authorized contract. BC-050 makes no such claim.

## C5A actual correction targets

### Mandatory native-v1 model instance identity — independently closed

The C5A review at `31476a1309589a989d709e45cb8c0fbdce2f7e6a`
independently reproduced that missing, blank, whitespace-only, and malformed
`model_instance_id` values fail closed and that `model` cannot rescue an absent
instance identity. No coercion, inference, or synthesis was accepted. That
finding remains authoritative.

### All asserted completion IDs — independently closed

The same review independently reproduced that every asserted `id`,
`response_id`, and `completion_id` must be a valid nonblank string before
deterministic selection. A valid field cannot hide a malformed asserted
sibling. The valid no-ID native-v1 path remains a null reference with
`synchronous_provider_response` proof; it fabricates nothing, never relabels
`model_instance_id`, and preserves `store:false`.

## Live LM Studio evidence

Dad/Blu supplied the completed real local-path observation:

```text
you> Hey, Blu.
blu> Hello! How can I assist you today?
```

`live_lm_studio_smoke: PASS`

The accepted evidence covers terminal ingress, Pre-ingress Security Restraint,
`ordinary_conversation`, Turn Controller, Model Execution Boundary, LM Studio,
Granite, normalized provider result, Validation and Egress, and terminal reply.
It is not fixture evidence. Codex did not rerun or fabricate this live
observation during the documentation reconciliation.

## Freeze and deployment disposition

- BC-050 final status: `accepted and frozen`.
- No Python Phase 2 or further parity campaign is authorized.
- No CLI expansion, additional continuity, Auth, tools/MCP, artifacts, or
  primary-Python deployment work is authorized.
- ChatGPT Custom GPT is Blu's mandatory primary, family-facing deployment and
  the next active product workstream.
- Python/LM Studio is a secondary local capability and portability deployment.
- One Blu remains authoritative: shared kernel, canon, behavior, and law where
  applicable; deployment mechanics remain wrapper-specific. This does not
  require two feature-complete runtimes.

## Scope and change review

This reconciliation changes documentation and review/status records only. No
production runtime code, golden CTS source, Persona, Operations Law,
`00_Instructions.md`, 7/8/9 architecture, OPSEC implementation,
authorization-date behavior, completion-evidence semantics, model envelope,
Custom GPT implementation, ComfyUI work, or future Python phase was changed or
started.

## Final disposition

`approve-with-notes`

---

# Final Independent Re-Review After BC-050-C3

status: complete
reviewer: Codex
review_target: `9f5a9e695622064ead37cf2da5208eb79a0a53de`
correction_base: `157441d3ea224760e8c800cdd19202cbb230d01d`
review_date: 2026-08-13
disposition: approve-with-notes

## Executive result

Disposition: `approve-with-notes`.

No reproducible BC-050-C3 blocker remains. The exact authorization date is
authenticated independently by all three validators; startup guidance names
end-of-input rather than a slash command; `/exit` and `/quit` remain ordinary
unsupported inputs; and malformed completion evidence fails closed without an
exception, receipt, PASS, or public success output.

BC-050-C3 is approved for Dad/Blu integration review. This review does not
merge, close, push, or begin any later runtime phase.

## Blocking findings

None.

## Final blocker disposition

### B-01 — resolved

All three `_bc050_authorized` predicates bind both authorization-date fields to
the exact string `2026-08-12`. Their function ASTs and six governing constants
are identical across the readiness, OPSEC, and continuity validators.

A fresh temporary-directory probe authenticated the valid baseline in all
three. It then wrote the same invalid value into both authorization records for
`1999-01-01`, `2026-08-13`, empty string, whitespace-only string, integer,
null, boolean, list, and dictionary. All 27 validator/value combinations
returned unauthorized; there were zero acceptances.

### B-06 — resolved

Executing `main` through end-of-input produced startup text containing neither
`/exit` nor `/quit` and truthfully named end-of-input. Fresh `/exit` and `/quit`
submissions each produced a normal `RawHostEvent`, entered ordinary ingress,
terminated `UNAVAILABLE` as an unsupported route, invoked the provider zero
times, created no receipt, and rendered exactly one `blu>` terminal result.

### B-07 — resolved

Fresh boundary-level probes supplied `None`, empty string, whitespace-only
string, integer, float, boolean, list, dictionary, and bytes as
`completion_evidence_ref`. Every value returned one deterministic
`INVALID / PROVIDER_COMPLETION_EVIDENCE_MISSING` terminal packet with no
exception, PASS, receipt, public output, coercion, or synthesized evidence. A
valid nonblank string produced PASS, one public result, and one receipt carrying
the exact provider evidence reference. The predicate is exactly equivalent to:

```python
isinstance(value, str) and bool(value.strip())
```

## Foundational regression evidence

| Check | Result |
| --- | --- |
| Runtime Phase 1 suite | 162 tests, OK |
| Security suite | 50 tests, OK |
| Readiness suite | 53 tests, OK |
| Continuity suite | 58 tests, OK |
| Frozen envelope | 36,887 bytes; pinned SHA-256; final byte `0x5D` |
| Architecture | 7 components / 8 packets / 9 interfaces |
| Golden CTS | all seven Markdown files and CTS ZIP OK; base-to-target diff empty |
| OPSEC differential | 20,000 fresh cases; 0 normalized/provenance mismatches |
| Removed-`Cf` provenance | 16,353 corpus cases plus all six focused code points equivalent |
| Protected ingress | BLOCK; provider invocation count `0` |
| Protected egress | REDACTED or BLOCKED; never CLEAR |

Median production timings for 2,000, 8,000, and 32,000 removals were 0.973 ms,
5.502 ms, and 23.326 ms. Fourfold size increases produced 5.65x and 4.24x
timing increases, remaining bounded and inconsistent with quadratic growth.

The continuity, historical archive, historical archaeology, OPSEC, Python
readiness, runtime-contract, successor-kernel, and viability validators passed.
`git diff --check` passed and the target checkout was clean before this review
record was added.

The host-adapter validator returned only the preserved BC-020 fixed-base
finding on `contracts/successor/unresolved_register.json`. The condition
predates BC-050, is unchanged by C3, and was neither suppressed nor reported as
a new blocker.

## Review execution note

The first combined fresh probe completed B-01, then stopped before B-06/B-07
because the standalone process lacked the documented `PYTHONPATH=src` fallback.
The runtime probes were rerun with that external fallback and passed. This was
review-harness setup, not a product failure; no internal `sys.path` mutation was
introduced.

## Nonblocking notes

- Live LM Studio smoke remains accurately `not_performed`; no live-provider
  evidence is claimed.
- Editable-install verification remains unperformed because the approved local
  build backend is unavailable; the external `PYTHONPATH=src` fallback passed.
- Punctuation canonicalization and root README wording remain bounded
  integration-quality notes, not reproduced semantic or security defects.
- The prior continuity defensive-invariant note remains future continuity work.

## Final disposition

`approve-with-notes`

---

# BC-050-C5A Final Independent Codex Review

status: complete
reviewer: Codex
review_target: `ed76f311976fba62e26356af6c4e145aa8ee2d6e`
correction_base: `374cc29da43d104f7ed6e9628e3fd8ebe9c4ff25`
implementation_branch: `bc-050-c5a-completion-failclosed`
review_branch: `bc-050-c5a-final-independent-review`
review_date: 2026-08-14
disposition: return-for-correction

## Executive result

Disposition: `return-for-correction`.

C5A closes both defects named by Blu's bounded C5 review. `model_instance_id`
is mandatory and cannot fall back to `model`; every asserted completion-ID
field is validated before deterministic selection. The real synchronous
native-v1 success shape remains valid, keeps a null completion reference with
`synchronous_provider_response` proof, and sends `store: false`.

One independently reproduced blocker remains on the assignment's required
malformed-response surface: an asserted malformed `stats` value is ignored.
The provider boundary returns PASS, and the end-to-end runtime emits public
output and a success receipt. This directly violates the assignment's explicit
requirement that malformed stats fail closed.

The review was performed from the independent Codex branch above, created
directly from the exact implementation target. No review artifact was committed
to Claude's implementation branch.

## Blocking findings

### C5A-B01 - malformed asserted stats produce public success

- **Affected path:** `src/blu_runtime/providers/model/lm_studio.py`,
  `LMStudioProvider.normalize_response`, immediately before output parsing.
- **Contradictory test:**
  `tests/runtime_phase1/test_lm_studio_provider.py::LiveStatelessCompletionTests::test_statistics_are_never_promoted_into_completion_proof`
  explicitly expects malformed stats to PASS.
- **Violated contract:** the C5A final-review packet's "Malformed Native-v1
  Response Regression Surface" includes malformed stats and requires every
  malformed case to fail closed without exception. BC-050 sections 9 and 13
  likewise require untrusted malformed provider responses to terminate without
  candidate output.
- **Reproducible mutations:** otherwise-valid native-v1 responses with `stats`
  equal to `None`, `[]`, `"bad"`, `{"input_tokens": "many"}`, or
  `{"total_output_tokens": -1}`.
- **Observed normalization result:** every mutation returned `PASS`, usable
  candidate text, a null completion reference, and
  `synchronous_provider_response` proof.
- **Observed end-to-end result:**
  `{"stats": {"input_tokens": "many", "total_output_tokens": -1}}`
  returned `PASS`, public output `Hello`, and one success receipt.
- **Expected result:** deterministic non-PASS failure, no candidate or public
  output, no success receipt, no coercion, and no exception.

This is a concrete fail-closed regression on an expressly required mutation,
not a speculative provider or architecture concern.

## C5A target disposition

### Mandatory model instance identity - resolved

Fresh probes covered missing, null, integer, float, boolean, list, dictionary,
empty, and whitespace-only `model_instance_id`. Every case returned
`INVALID / PROVIDER_RESPONSE_MALFORMED` with no candidate, reference, or proof.
A valid `model` field with no `model_instance_id` also failed closed. No value
was coerced, inferred, synthesized, or trimmed into accepted evidence.

### Mixed completion-ID validation - resolved

All five required mixed mutations returned
`INVALID / PROVIDER_COMPLETION_EVIDENCE_MISSING`, with no candidate, completion
reference, or proof. End-to-end, the representative `{"id": "good",
"response_id": 7}` case produced no public output and zero receipts.

No completion-ID fields remained valid with a null reference and synchronous
proof. Exactly one valid nonblank string remained valid. Multiple valid strings
remained valid and selected deterministically in declared order: `id`, then
`response_id`, then `completion_id`.

### Native-v1 success contract - preserved

The exact required success shape with `model_instance_id`, one message output,
and valid token stats returned PASS with assistant content `Hello.`, no
provider completion reference, and `synchronous_provider_response` proof. It
did not produce `PROVIDER_COMPLETION_UNVERIFIED` or
`PROVIDER_COMPLETION_EVIDENCE_MISSING`. The outbound payload retained
`store: false` and `stream: false` and contained only the six evidenced native
fields.

## Foundational regression evidence

| Check | Result |
| --- | --- |
| Runtime Phase 1 suite | 207 tests, OK |
| Security suite | 50 tests, OK |
| Readiness suite | 53 tests, OK |
| Continuity suite | 58 tests, OK |
| Frozen envelope | 36,887 bytes; pinned SHA-256; final byte `0x5D` |
| Architecture | 7 components / 8 packets / 9 interfaces |
| Golden CTS | all seven Markdown files and CTS ZIP OK; C5-to-C5A diff empty |
| Authorization date | exact `2026-08-12` in both records |
| Target diff check | clean |

The runtime/security regressions retain ordinary unsupported `/exit` and
`/quit` ingress, provider invocation count `0` for protected ingress,
protected egress never CLEAR, OPSEC differential equivalence, and the
`00_Instructions.md` successor-canon exclusion. No architecture component,
provider-side continuity, fabricated completion ID, content hash, UUID proof,
or `model_instance_id` relabeling was introduced.

Eight repository validators passed against an isolated exact-target snapshot.
The host-adapter validator reproduced only the known BC-020 fixed-base finding
on `contracts/successor/unresolved_register.json`; C5A did not change that path.
Direct readiness/continuity validation in the shared working directory also
reported only pre-existing local smoke/install artifacts, so those artifacts
were excluded from target evidence rather than moved or modified.

`live_lm_studio_smoke: not_performed`. The implementation handoff records an
earlier live PASS, but this independent review does not relabel fixture or prior
author evidence as a live Codex observation.

## Required follow-up

Return C5A to the implementation owner for the smallest bounded correction that
validates asserted native-v1 stats and pins malformed values to fail-closed
end-to-end behavior. Re-review the exact correction target. Do not redesign
BC-050 or reopen the already-resolved identity, completion-ID, architecture,
canon, continuity, or provider decisions.

## Final disposition

`return-for-correction`

---

# Controlling Final BC-050 Disposition

status: accepted_and_frozen
authority: Dad/Blu
reviewer: Codex
review_date: 2026-08-14
disposition: approve-with-notes

This is the controlling final disposition. It incorporates the detailed
authority reconciliation above and supersedes the immediately preceding C5A
`return-for-correction` disposition and required follow-up. Malformed
non-authoritative `stats` telemetry is not a blocker and no runtime correction
is authorized for it. C5A's mandatory `model_instance_id` and
all-asserted-completion-ID targets remain independently closed.

`live_lm_studio_smoke: PASS`

BC-050 is accepted and frozen. ChatGPT Custom GPT is the mandatory primary
deployment and next active workstream; Python/LM Studio is secondary local
capability and portability. No further Python phase or parity work is
authorized.
