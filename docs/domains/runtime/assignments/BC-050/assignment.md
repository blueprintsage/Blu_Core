# BC-050 — Python Runtime Phase 1 — Boot + Ordinary Turn + LM Studio Model Boundary

status: active
owner: Claude
reviewer: Codex
project_lead: Blu
project_owner: Dad
domain: runtime
last_reviewed: 2026-08-12

## Packet provenance

This record reinstates the final canonical BC-050 execution packet authored on
2026-08-12 and delivered to Dad/Blu, which supersedes for execution purposes
the original BC-050 draft and BC-050 Amendment A. It was authored by Claude as
specification author before implementation authority was granted, and reviewed
in two independent pre-flight passes.

If Dad/Blu's delivered copy differs in wording from this reinstated copy,
theirs governs and this file should be replaced with it.

- Pre-flight review pass 1: `return-for-correction` (B-1, B-2, B-3; N-1–N-5)
- Amendment A closed B-1, B-2, B-3 and resolved N-1–N-5
- Pre-flight review pass 2: `approve-with-notes`, zero blocking findings,
  residual notes R-1–R-4 folded into the packet
- Implementation authorization: explicit Dad/Blu action, 2026-08-12
- Implementation owner changed from Codex to Claude for BC-050 only
- Independent implementation review assigned to Codex

## Assignment identity

- Exact base commit: `973589eea05fe42deeb829c5435bd09faf8cbe70`
- Base verification: `origin/main` equals the base; zero intervening commits
- Starting branch: `main`
- Work branch: `bc-050-python-runtime-phase1`
- Global index row: `docs/worklogs/assignments.md#BC-050`

## Authorization gate

Dad/Blu explicitly authorized BC-050 implementation on 2026-08-12. That
authorization is limited to BC-050. It does not authorize later Python phases,
Local Mirror, Auth, tools, PASS, SkillForge, or Custom GPT modification.

`automatic_start_prohibited: true` remains permanently true. Authorization
permits this assignment to begin; it never creates an automatic-start
mechanism. These are separate concepts and the readiness contracts must keep
them distinct.

## Objective

Implement the smallest useful real Python Blu slice, end to end, once:

```text
process boot
  -> portable configuration
  -> canonical Blu source verification and load
  -> terminal host ingress
  -> Pre-ingress Security Restraint
  -> ordinary-conversation Turn Controller route
  -> Model Execution Boundary
  -> LM Studio
  -> local LLM
  -> normalized provider result
  -> Validation and Egress
  -> one terminal Blu reply
```

Exactly one route is supported: `ordinary_conversation`. Everything else
terminates safely as unsupported or unavailable. BC-050 succeeds by being
narrow and truthful, not by answering a prompt impressively.

## One-Blu law

The Blu kernel and canon stay the same. The wrapper changes. There are not two
Blu identities and not two behavioral forks. Required deployment targets remain
the ChatGPT Custom GPT and Python Blu → LM Studio → local LLM.

Canon-level, therefore not host-level or model-level: identity, Persona,
relational posture, tone floor, Operations Law, teaching behavior,
truthfulness, security and privacy semantics, refusal and boundary posture,
continuity truth discipline, source authority.

Prohibited: a Python Persona, an LM Studio Persona, a local-only Blu identity,
a separate behavioral canon, a provider-owned security or identity layer. There
must be no `python_persona.md`, no `local_blu_persona.md`, no
provider-specific behavioral fork. Host and provider instructions describe
mechanics only. LM Studio is not Blu; the selected model is not Blu.

BC-050 implements the Python deployment wrapper, not a separate Blu. It does
not modify, configure, or test the Custom GPT; parity testing is a separate
track.

## Fixed architecture

Exactly 7 components, 8 packets, 9 interfaces. Phase 1 may leave a component
behaviorally unavailable; it must not change the counts.
`PendingAuthorizationState` remains a state record.

Prohibited: mega-Exec, Exec Library architecture, MMU service, School Engine,
Mood service, SecuritySessionManager, AuthSessionManager, an eighth continuity
component, an LM Studio architectural component, Canon Manager, Portability
Manager. Internal modules do not become architectural authorities.

## Phase-1 component scope

Real deterministic behavior: Pre-ingress Security Restraint; Turn Controller
for `ordinary_conversation`; Validation and Egress; Model Execution Boundary
with the LM Studio binding; Generic Host Adapter Boundary with a terminal
binding.

Architecturally represented, behaviorally limited: Authorization Evaluator (no
protected Auth behavior) and Generic Continuity Provider Boundary (no durable
provider). Do not invent behavior to make an unavailable component look
complete.

## Allowed collision domain

```text
src/blu_runtime/**
tests/runtime_phase1/**
tools/validate_python_readiness.py
tests/readiness/test_validate_python_readiness.py
readiness/python_package_layout.json
readiness/phase1_executable_slice.json
readiness/python_phase1_readiness_checklist.json
pyproject.toml
.gitignore
docs/domains/runtime/assignments/BC-050/{assignment,handoff,validation,review}.md
docs/domains/runtime/{decisions,worklog,failures,next_steps}.md
docs/worklogs/assignments.md
docs/dev/docs_index.md
MANIFEST.sha256
requirements-contracts.txt (only if a pinned dependency is genuinely required)
```

Any modification outside this domain requires an explicit written amendment
from Dad or Blu before the change is made.

## Protected and prohibited areas

```text
kernel/golden/v0.22.0/**
current CTS content
closed Claude review records
closed BC-041 / BC-041-C1 security evidence
contracts/successor/** architecture counts
contracts/security/opsec/minimum_contract.json
tools/validate_opsec_contracts.py
config/source_authority.json
AGENTS.md, CLAUDE.md, CODEX.md
production protected-policy values
```

`tools/validate_opsec_contracts.py` is the C1 conformance reference and the
differential-test oracle and must remain byte-identical. If it appears wrong,
that is a contradiction to record under §21, not to edit.

No history rewriting. No force-push. Do not merge. Do not self-close BC-050.

## Executable requirements

### 1. Typed Phase-1 contracts

`contracts/models.py` holds typed packets and records using standard-library
dataclasses. Status vocabulary comes from `contracts/successor/error_model.json`:
`PASS | BLOCK | ASK | UNAVAILABLE | INVALID | ERROR`. Types are data, not
authority.

### 2. Portable configuration

Validate against `readiness/schemas/runtime_config.schema.json` with pinned
`jsonschema==4.26.0` `Draft202012Validator` and format checking. Configuration
is a claim, never capability evidence. No machine-specific absolute paths. The
protected-policy binding stores environment-variable names only. Invalid
configuration is `INVALID`, `model_invoked: false`.

### 3. Canonical source loading and the frozen envelope

**3.1 Sources.** Exactly two artifacts enter the model-facing payload, in
order: `01_Persona.md` (CANON-002) then `02_Operations_Law.md` (CANON-003),
both exact golden bytes with no transformation.

`00_Instructions.md` does not enter the payload. It is deployment and
runtime-entry authority realized through deterministic wrapper mechanics, per
the CANON-001 / CANON-009 split. No behavior may silently disappear; every
Phase-1-applicable section is accounted for by §17.2. Do not invent a third
behavioral prompt. `03_Exec.md`, `04_Exec_Library.md`, `05_Commands.md`, and
`06_Programs.md` are excluded (CANON-005 forbids a bulk prompt copy).

**3.2 Integrity gate.** Read raw bytes and verify SHA-256 against
`SHA256SUMS` before decoding:

```text
01_Persona.md        779bfc47ebcd22386a91db228d3a3d827a92f9c471ccee36546880a16c6e4e79
02_Operations_Law.md d097eee5e5b64243234644b064831afdf42829bef1dddf5e7128343b60045fab
```

No CRLF/LF normalization, no BOM stripping, no decode-then-reencode before the
digest. This ordering is load-bearing: it is what makes the rendered envelope
digest portable, because a line-ending-converted checkout fails here and never
reaches rendering.

**3.3 Exact rendered system prompt.** Concatenate exactly these byte segments.
`LF` is `0x0A`; literal text is ASCII encoded as UTF-8.

| # | Segment |
| --- | --- |
| 1 | `[BLU_CANON_PERSONA]` + LF |
| 2 | raw verified bytes of `01_Persona.md`, unmodified |
| 3 | LF + `[/BLU_CANON_PERSONA]` + LF |
| 4 | `[BLU_CANON_OPERATIONS_LAW]` + LF |
| 5 | raw verified bytes of `02_Operations_Law.md`, unmodified |
| 6 | LF + `[/BLU_CANON_OPERATIONS_LAW]` + LF |
| 7 | `[BLU_RUNTIME_BINDING]` + LF |
| 8 | the nine binding lines below, each terminated by LF |
| 9 | `[/BLU_RUNTIME_BINDING]` with **no** trailing LF |

Segment 8, exactly:

```text
deployment=python_lm_studio
route=ordinary_conversation
tools=unavailable
protected_authorization=unavailable
durable_continuity=unavailable
artifacts=unavailable
reminders_and_scheduling=unavailable
streaming=unavailable
Do not claim unavailable host capabilities or side effects occurred.
```

Byte-precision rules: canonical bytes are never trimmed, padded, re-encoded, or
line-ending converted; no trailing newline is added to or removed from either
file; the wrapper contributes only the bytes above; no BOM; no trailing LF
after the final `[/BLU_RUNTIME_BINDING]`, so the final byte is `]` (`0x5D`);
current user input is not part of the projection and is passed separately as
the native chat `input`.

**The source asymmetry is expected and must not be "fixed."**
`01_Persona.md` ends with LF and `02_Operations_Law.md` does not, so the
closing seams differ:

```text
Persona seam:  ...t validation.\n\n[/BLU_CANON_PERSONA]\n[B...
OpLaw   seam:  ...ion boundaries.\n[/BLU_CANON_OPERATIONS_LAW]\n[B...
```

Guaranteeing a newline before each closing delimiter changes the Persona block
and breaks the digest.

**3.4 `canon_projection_digest`.** SHA-256 over the exact UTF-8 byte sequence
of the fully rendered system prompt; stored lowercase hex, 64 characters. It is
not a digest of Persona alone, Operations Law alone, a concatenation of source
digests, or anything including user input.

Pinned vector, derived against base `973589ee`:

```text
persona bytes           25083
operations law bytes    11371
runtime binding bytes     335
rendered envelope bytes 36887
canon_projection_digest 103e0e2dd94183c914dc8c46e3ac376af516382548e17af40c14c27d3319f142
final byte              0x5D  ']'
```

Tests assert both the construction from §3.3 and equality with this vector. If
they disagree the implementation is wrong, not the vector. Changing the vector
is a canon-envelope change requiring re-authorization.

**3.5 Canon failure semantics.** Runtime-local codes, deliberately not added to
the OPSEC `safe_error_codes` set: `CANON_SOURCE_UNAVAILABLE`,
`CANON_SOURCE_INTEGRITY_MISMATCH`, `CANON_PROJECTION_INVALID`. All three:
`status: BLOCK`, `model_invoked: false`, no protected or source content
printed. Never represent a canon integrity failure as an OPSEC match.

### 4. Protected-policy boot gate

Six ordered stages: `reference_configured`, `target_located`,
`payload_loaded`, `schema_validated`, `integrity_validated`, `policy_usable`.
Only `policy_usable` permits evaluation. Any failure is terminal `UNAVAILABLE`
without a SecurityDecision, and no ordinary user text reaches Turn Controller
or the model. No permissive development fallback. Synthetic fixtures are for
tests only. Production protected values stay outside Git.

### 5. Pre-ingress Security Restraint

Implement the minimum contract v1.3.0 faithfully. `no_match -> PASS`,
`protected_match -> BLOCK`. Only PASS reaches Turn Controller. No match echo,
no model invocation in the matcher, no confidence scoring. Evidence obeys the
allowed/forbidden field lists; the candidate digest is HMAC-SHA-256 over the
normalized candidate using the policy key.

**5.1** `Cf` coverage: interior, inter-word, arbitrary mixtures, repeated,
mixed code points, leading outer edge, trailing outer edge, both outer edges.
Removed-`Cf` provenance must survive normalization.

**5.2 Differential equivalence (mandatory).** Oracle is
`normalized_match_candidate` in `tools/validate_opsec_contracts.py`, loaded via
`importlib.util.spec_from_file_location` and never copied. Assert
`production.normalized == reference["normalized"]` and
`sorted(production.removed_cf_boundaries) == reference["removed_cf_boundaries"]`
across: the six code points; inside-token; inter-word; mixed; repeated; mixed
code points; leading, trailing, and both outer edges; outer plus interior;
unseparated self-repetition; the false-positive corpus; and generated
multi-placement cases beyond the pinned fixtures.

**5.3 Bounded construction (C1 N-2).** Do not port the reference's quadratic
shape. Compute provenance in a bounded, demonstrably non-quadratic single-pass
design, plus one focused saturation stress test. Performance success does not
substitute for semantic equivalence.

**5.4 Provenance-loss invariant (C1 N-1).** A removed `Cf` flanked by word
characters on both sides must always yield a provenance offset.

**5.5 C1 N-3.** The `_` separator / Unicode word-character overlap is recorded
behavior. Do not reopen it.

### 6. Terminal host adapter

One terminal input, one normalized raw host event, one submission through the
boundary, one terminal packet, one rendered response. The adapter may translate
mechanics; it may not redefine Blu, bypass security, invent continuity or
authorization, or treat provider output as validated.

### 7. Turn Controller

One route. Entry requires policy usable, SecurityDecision PASS, verified canon,
observed endpoint, matched loaded model instance, and satisfied context
capacity. Lock route, owner (Model Execution Boundary), ScopeLock, and no side
effects. No fallback routes, no model-decides router.

**7.1** Unsupported routes terminate safely: slash commands, protected source
access, Auth, protected authorization, protected continuation, tools, tool
execution, source retrieval, artifacts, durable continuity mutation, reminders,
scheduling, Memory Program, SimCode, MMU, StateTree, Mood service, School
Engine, SkillForge, PASS.

**7.2 `ASK`.** Vocabulary remains `PASS | BLOCK | ASK` and the enum retains
`ASK`, but Phase 1 has no path that generates it. Do not implement an ASK or
Auth flow. An unexpected `ASK` must not invoke the model and must terminate
safely, proven by test.

### 8. Model Execution Boundary and LM Studio

**8.1** The operator owns LM Studio lifecycle, model download, load, and
unload. Do not call load or download endpoints.

**8.2** `GET /api/v1/models` must establish: configured key exists; type
compatible with chat; a loaded instance exists; instance identity recorded;
context length known; required capacity satisfied. Otherwise `UNAVAILABLE`
with no inference.

**8.3** `POST /api/v1/chat` with only evidenced native fields: `model`,
`input`, `system_prompt`, `stream: false`, `store: false`, `context_length`
where applicable. No integrations, MCP, tools, or provider-side state
continuation. Do not use or refer to `previous_response_id` or Responses-API
continuation semantics. Each request is independently constructed; LM Studio
history is not Blu continuity.

**8.4** The request contains only the frozen envelope plus the current
permitted input — never protected-policy contents, secrets, hidden match
values, unauthorized internals, tool definitions, Local Mirror state, or
invented history.

### 9. Provider response normalization

Untrusted. A 200 does not prove a completion. Verify structure, model instance
identity, provider identity, output item types, the permissible Phase-1 shape,
and usable text. Reasoning never becomes public text. `tool_call` and
`invalid_tool_call` never execute (`UNAVAILABLE`, `tool_executed: false`).
Partial output after timeout or error is never a successful response.

### 10. Validation and Egress

Same policy authority and same match semantics as ingress. Sequence: normalize,
evaluate, block or policy-authorized redact, rescan, authorize or withhold.
`CLEAR` and `REDACTED` printable; `BLOCKED`, `UNAVAILABLE`, `INVALID` not.
Replacement is `[protected content omitted]`, authorized only when every
matched rule permits REDACT. Postcondition failure yields `BLOCKED`. The public
form is the canonicalized candidate only.

### 11. Continuity

Boundary abstraction only. Lifetimes: `none`, `turn`, `host_session`,
`durable_external`. Bare `session` is not a substrate. Process memory, prompt
history, model context, a filename, and LM Studio stateful chat are not durable
continuity. Report unavailable; ordinary turns still succeed.

### 12. Current-turn receipt

Binds `request_id`, `provider_id`, `model_instance_id`,
`canon_projection_digest`, `turn_request_ref`, `control_decision_ref`,
`validation_result_ref`, `terminal_packet_ref`,
`provider_completion_evidence_ref`. A receipt proves only what its evidence
supports.

### 13. Failure behavior

Provider invocation count must be exactly `0` for every pre-model failure.

| Condition | Status | Model invoked |
| --- | --- | --- |
| Invalid configuration | `INVALID` | false |
| Golden source unavailable | `BLOCK` | false |
| Golden digest mismatch | `BLOCK` | false |
| Canon projection invalid | `BLOCK` | false |
| Protected policy unusable | `UNAVAILABLE` | false |
| Protected ingress match | `BLOCK` | false |
| LM Studio endpoint unavailable | `UNAVAILABLE` | false |
| Configured model absent | `UNAVAILABLE` | false |
| Configured model not loaded | `UNAVAILABLE` | false |
| Context capacity unknown | `UNAVAILABLE` | false |
| Context capacity insufficient | `UNAVAILABLE` | false |
| Provider timeout | `UNAVAILABLE` | no partial output |
| Malformed provider response | `INVALID` | no candidate output |
| Model identity mismatch | `INVALID` | no candidate output |
| Tool-call candidate | `UNAVAILABLE` | `tool_executed: false` |
| Egress protected residual | `BLOCKED` | never printed |
| Continuity unavailable | route independent | `durability_claimed: false` |

### 14. Support layer (BC-040 N-1)

Classify every `phase1: true` path. These four are non-component support
infrastructure with zero architectural authority: `__main__.py` (process
assembly and entrypoint), `config.py` (configuration parsing and validation),
`canon/loader.py` (golden verification and frozen-envelope rendering),
`contracts/models.py` (typed packets and data representations).

`canon/loader.py` may not choose, create, or rewrite canon, determine
behavioral precedence, or become a Canon Manager. Add validator coverage
proving the support layer creates no eighth component.

### 15. Readiness-validator transition

Amend `tools/validate_python_readiness.py` to distinguish unauthorized
implementation from authorized BC-050 implementation:

1. Add a BC-050 authorization record to the readiness checklist.
2. Gate on it; while absent, every current guard behaves exactly as today.
3. When present, permit production Python only under `src/blu_runtime/**` and
   runtime tests only under `tests/runtime_phase1/**`; keep the six existing
   `ALLOWED_PYTHON` paths.
4. Keep rejecting `runtime`, `blu_core`, `providers`, `lm_studio`,
   `local_mirror` as top-level roots unconditionally; under `src/`, reject
   anything outside `src/blu_runtime/`.
5. `implementation_present` must equal the authorization state.
6. `implementation_authorized` in the slice and the checklist must equal the
   authorization state and agree with each other.
7. Replace `no_runtime_code_introduced` with
   `runtime_phase1_code_introduced_only_under_BC050_authorization`.

Keep `automatic_start_prohibited is True` ungated. Do not change
`BASE_COMMIT`. Do not weaken golden protection, architecture validation,
manifest completeness, OPSEC validation, PASS/SkillForge protection,
unauthorized-implementation detection, provider-root protection, the
`jsonschema` pin, or the portable protected-policy checks. Cover every amended
guard, including negative tests proving pre-authorization rejection.

### 16. Packaging (R-3)

Minimal `src`-layout `pyproject.toml` with an explicitly declared build
backend. `.gitignore` gains exactly `*.egg-info/`. No heavyweight tooling.

The declared backend must already be present for an offline acceptance run. If
unavailable, setup fails clearly and reports the prerequisite; it must not go
online. Offline fallback for tests is `PYTHONPATH=src`, recorded in
`validation.md`, and is not a substitute for install verification.

## Test strategy

Standard-library `unittest` under `tests/runtime_phase1/**`. Coverage: config
validation; canon digest validation; byte-exact envelope including both seams;
digest reproducibility; policy loading and all failure cases; ingress OPSEC; C1
differential equivalence; provenance invariant; saturation stress;
false-positive controls; one-route lock; unsupported routes; unexpected `ASK`;
provider parsing; tool-call rejection; egress OPSEC, redaction, rescan;
terminal packet formation; continuity truth; receipt binding.

Provider tests use deterministic mocks; no live LM Studio required. Cover
endpoint unavailable, malformed inventory, key absent, key unloaded, multiple
instances, wrong type, unknown context, insufficient context, successful match,
malformed chat response, identity mismatch, timeout, ordinary message,
tool_call, invalid_tool_call, reasoning plus message, and no print after error.

Non-invocation proofs expose an invocation count; assert exactly `0` for
protected phrase, mixed/repeated `Cf`, outer-edge `Cf`, invalid policy, invalid
configuration, invalid canon digest, unavailable model evidence, and unexpected
`ASK`.

One-Blu test proves the runtime loads authorized canon rather than a rewritten
Python Persona, and that no forked behavioral file exists.

**§17.2 parity mapping.** `validation.md` must map every Phase-1-applicable
`00_Instructions.md` section — at minimum Identity Lock, Interaction Floor,
Truth Discipline, No Runtime Theater, Completion Proof, Execution Law, Verb
Lock, Compliance Gate — to a named Persona section, a named Operations Law
section, a named deterministic component, or `GPT-only mechanic — correctly
omitted`. Mark semantic rows as requiring reviewer judgment; do not claim
deterministic proof of natural-language equivalence.

Live smoke test only if Dad/Blu supply an environment; otherwise
`not_performed`. Live success never replaces deterministic tests.

## Exact commands

```bash
python -m pip install -r requirements-contracts.txt
```

```bash
python -m pip install -e .
```

```bash
python -m unittest discover -s tests/runtime_phase1 -p "test_*.py"
```

```bash
python -m unittest discover -s tests/security -p "test_*.py"
```

```bash
python -m unittest discover -s tests/readiness -p "test_*.py"
```

```bash
python tools/validate_opsec_contracts.py
```

```bash
python tools/validate_python_readiness.py
```

```bash
cd kernel/golden/v0.22.0 && sha256sum -c SHA256SUMS
```

```bash
git diff --check
```

Plus every other applicable validator under `tools/`, each result recorded.

## Completion criteria

The original 25 criteria, plus: authorized readiness-validator transition
succeeds without weakening guards; production provenance is
differential-equivalent to the reference; construction is bounded; the
provenance-loss invariant passes; envelope byte-level tests pass;
`canon_projection_digest` reproduces the pinned vector; the parity mapping is
reviewable; support modules create no component; installation and import work
under the declared offline assumptions; no untracked `egg-info` breaks the
manifest; no `ASK` is synthesized; canon failures use runtime error semantics;
the LM Studio request uses only evidenced fields; and the provider is never
invoked after a pre-model terminal failure.

## §21 Deviation and contradiction protocol

If a genuine contradiction appears — a contract that cannot be satisfied as
written, or two frozen contracts that disagree — stop and record it in
`handoff.md` with exact file and line references. Do not solve it by expanding
scope, editing a protected contract, or inventing behavior. If the pinned
envelope digest cannot be reproduced, that is a contradiction, not a vector to
update.

## §22 Required handoff

Report base SHA, branch, implementation SHA, metadata receipt SHA if used,
production files, test files, validator and readiness changes, dependency
changes, commands and results, architecture verification, golden and manifest
results, protected-policy leakage check, non-invocation proofs, live smoke
result or `not_performed`, deviations and contradictions, and readiness for
independent Codex review.

Do not merge. Do not self-close BC-050. Dad and Blu retain integration
authority.

---

# Amendment — BC-050-C2A, 2026-08-13 (Dad/Blu)

## Instruction-Layer Classification Cleanup / B-02 Resolution

This dated amendment supersedes only the `00_Instructions.md` parity
requirement. The original packet text above is preserved unedited as history.

### Authority decision

`kernel/golden/v0.22.0/00_Instructions.md` remains immutable historical and
current CTS deployment provenance. It is **not** a successor invariant
behavioral-canon source, not a required Python model-facing source, not a
cross-deployment parity source, and not a source whose individual rules must be
reproduced, mapped, or projected by Python Blu.

That surface primarily stabilized a hosted model that was not running Blu's
deterministic architecture — bootstrap, runtime binding, loop discipline,
repository location, anti-drift, and execution guidance. Instruction text was
used to attempt persistence inside the hosted model, and that persistence cannot
be assumed. The successor therefore does not treat inclusion in a host
instruction surface as proof that a behavior is invariant Blu canon.

### Superseded requirements

- §3.1, the sentence requiring every Phase-1-applicable `00_Instructions.md`
  behavior to be accounted for.
- §17.2, the mandatory `00_Instructions.md` parity mapping.
- The validation-record requirement to carry that parity table as a gate.
- Completion criterion 32, requiring that table to exist and be reviewable.
- Any equivalent B-02 rule-destination requirement introduced during BC-050-C2.

### Not superseded

The frozen model-facing envelope is unchanged: Persona then Operations Law,
36887 bytes, digest
`103e0e2dd94183c914dc8c46e3ac376af516382548e17af40c14c27d3319f142`, final byte
`0x5D`. No `00_Instructions.md` text may be copied, excerpted, summarized,
paraphrased, mechanically projected, or appended to the runtime binding. No
envelope re-freeze is authorized.

B-01 and B-03 through B-07 are unchanged and remain in force.

### Restated completion question

The B-02 question is now:

> Does Python Blu preserve the actual successor One-Blu invariant from its
> approved canonical owners and deterministic contracts?

It is no longer "where did every rule from `00_Instructions.md` go?"

The successor One-Blu invariant remains identity, Persona, relational posture,
tone floor, Operations Law, teaching behavior, truthfulness, security and
privacy semantics, refusal and boundary posture, continuity truth discipline,
validation truth, receipt discipline, source authority, and explicitly approved
successor architectural invariants.

### Future promotion rule

Nothing useful is deleted from history. A behavior found in
`00_Instructions.md` — Verb Lock, a specific anti-drift micro-rule, anything
else — may be promoted in a future assignment. Promotion requires an explicit
behavior statement, the proper owner, justification that it belongs to Blu
rather than to one deployment, implementation or model-facing placement, tests,
and Dad/Blu approval. No instruction-file archaeology silently becomes canon.

### Live Custom GPT

This amendment does not modify the live Custom GPT. Reducing or removing its
persistent instruction surface is a separate deployment task.
