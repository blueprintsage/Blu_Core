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
