# One-Blu Portability and Python Runtime Readiness

status: review
owner: docs/domains/runtime
last_reviewed: 2026-08-11
assignment: BC-040

## Result

BC-040 defines the implementation-ready architecture and first executable
slice, but the authorization result is:

```text
not_ready_for_python_phase1
```

The only actual blocker is SUR-001: the repository does not contain the
separately authorized minimum OPSEC match/redaction contract needed to prove
that arbitrary natural-language ingress and egress cannot request or reproduce
protected Blu source. Explicit protected routes, tools, Auth, continuity,
commands, and side effects can all fail closed, but an ordinary text lane still
needs that boundary. BC-040 does not invent it.

## One Blu

Custom GPT Blu and Python Blu are deployments of one canon. Persona, Operations
Law, identity, relational posture, teaching behavior, security and
authorization semantics, continuity truth, validation truth, receipt
discipline, and source authority never receive host-specific behavioral copies.

The current CTS remains authoritative for current behavior. Persona and
Operations Law remain exact model-facing sources. Historical Exec, ExecLib,
Commands, and Programs remain authoritative for the current CTS, but they are
not automatically future canon. Only explicitly traced behaviors migrate into
the seven-component successor architecture.

Host-specific deployment material may bind capabilities, translate events,
load canonical sources, and express honest limitations. It may not redefine
behavior. Generated projections carry canonical mapping IDs, source digests,
role declarations, and allowed transformation types. Deterministic checks catch
missing/stale sources and role violations; semantic reviewers compare tone,
relationship, teaching, and refusal posture where mechanical proof ends.

## Required deployments

ChatGPT Custom GPT remains a required deployment and continues using the
current CTS projection until a separately approved generated successor
projection exists. Host limitations are allowed and must be named; invented
deterministic enforcement is not.

Python plus LM Studio is the second required deployment. Python owns the four
deterministic core components. LM Studio binds only behind the Model Execution
Boundary. A selected local model is neither Blu nor Blu's canon, and changing a
compatible model cannot require Persona, law, security, continuity, or
validation changes. Codex is optional best effort and cannot block or reshape
the primary design.

## LM Studio Phase 1 profile

Official LM Studio documentation supports a native v1 REST profile. The first
binding is specified as:

```text
GET  /api/v1/models   observe model keys, loaded instances, context, capabilities
POST /api/v1/chat     non-streaming inference with store=false
```

The operator starts LM Studio and loads the model before Blu boots. Phase 1
does not own model loading. Configuration names an endpoint and selected model,
but those values prove nothing. Boot observes the endpoint, matches the selected
key to a loaded model instance, checks context evidence, and later requires a
completed inference response before claiming model completion.

Ordinary chat completion is required. Structured output and tool-call
generation are provider-dependent and not required for the ordinary slice.
Streaming and tool execution are unsupported. A model-emitted tool call remains
a non-executing candidate and terminates safely. Provider timeout, malformed
response, missing model, unknown capacity, or insufficient evidence is
`UNAVAILABLE` or `INVALID`; partial text is never completion.

## Phase 1 slice

The planned runtime uses a normal `src/blu_runtime/` package with small modules
mapped beneath exactly seven approved components. It loads portable
configuration and canonical source digests, observes LM Studio, accepts one
terminal ingress path, runs pre-ingress restraint, locks the sole
`ordinary_conversation` route and model owner, invokes the model once, validates
the normalized result, and returns one terminal packet and current-turn
receipt.

There are no slash commands, tools, source retrieval, artifacts, reminders,
scheduling, Memory Program, SimCode, MMU, StateTree, Mood service, School
Engine, Local Mirror provider, or PASS/SkillForge path in the slice. Continuity
may be unavailable; ordinary turn-local behavior continues without a
persistence claim.

## Security and blocker reconciliation

SUR-002, SUR-011, and SUR-012 block protected features only. Phase 1 exposes no
protected action, Auth interaction, or protected cross-turn continuation, so
those paths return `UNAVAILABLE` without attempt. SUR-003 is resolved by the
finite one-route catalog. SUR-010 is resolved sufficiently for the slice by an
explicit disposition for every UR-001 through UR-028 current-source gap.

SUR-001 remains different. A real text turn cannot safely bypass pre-ingress
policy merely because explicit protected commands are absent. Until a
security-authorized minimum matcher/redaction contract exists, test fixtures
may exercise downstream interfaces but a real user turn must not reach the
local model.

## Continuity hardening

BC-040 adds a mutation request carrying caller-owned expected versions, binds
receipts to that value, prevents records on `not_found`, prevents completed
receipts on non-completed retrievals, defines availability probes as
receipt-only observations, mechanically binds requested action to operation,
rejects machine-specific absolute portable references, and prevents failed or
conflicting receipts from claiming successful versions or supersession.

The selected consumer is `jsonschema==4.26.0` using Draft 2020-12 with format
checking and registered local references. Valid and invalid instances exercise
all six schemas and their actual conditionals. Git-backed tests also exercise
protected scope, disallowed Python, PASS/SkillForge, LM Studio code bleed,
manifest coverage, and canonical blob digest validation.

## Next safe step

Dad/Blu may authorize `Protected Security Phase 1 Minimum OPSEC Match and
Redaction Contract`. After that packet closes with independent review, they may
consider the already named runtime packet:

```text
Python Runtime Phase 1 — Boot + Ordinary Turn + LM Studio Model Boundary
```

Neither assignment starts automatically from BC-040.
