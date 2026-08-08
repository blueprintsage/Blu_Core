# Successor Kernel

status: review
owner: docs/domains/runtime
last_reviewed: 2026-08-08
assignment: BC-018
correction: BC-018-C1

## Status and authority

This is the BC-018 successor-kernel specification. It is a design artifact, not
runtime implementation and not a replacement for the current runtime.

Current source authority remains unchanged:

- `00_Instructions.md` is the authoritative `deployment_instruction`.
- `01_Persona.md` through `06_Programs.md` are the authoritative
  `kernel_runtime_capsule` set.
- all seven files under `kernel/golden/v0.22.0/` remain immutable.

The centerline is: preserve the behavior and law; reconsider the component
graph. Historical module identity is evidence of neither correctness nor a
successor component requirement.

## Normative architecture

The successor has seven components or boundaries. Four are
deterministically-specifiable core components; three keep model, host, and
durable-continuity authority outside the core.

| Component | Domain | Sole reason to exist |
|---|---|---|
| Pre-ingress Security Restraint | deterministic core | OPSEC must decide before ordinary ingress and outside route ownership. |
| Authorization Evaluator | deterministic core | Protected actions need bounded policy evaluation over explicit evidence. |
| Turn Controller | deterministic core | One component must normalize the turn, validate capabilities, lock route/owner, and freeze ScopeLock. |
| Validation and Egress | deterministic core | One component must validate proof and authorize the only terminal public result. |
| Model Execution Boundary | model-facing | Blu's identity, judgment, pedagogy, interpretation, and expression belong to the model. |
| Generic Host Adapter Boundary | host adapter | Host events, capabilities, services, receipts, errors, and delivery require translation without contaminating the core. |
| Generic Continuity Provider Boundary | continuity provider | Durable continuity requires external namespaced, versioned reads/writes and receipts. |

No `Exec`, `Exec 2`, Program framework, School Engine, Mood service, MMU
service, Read Lane stack, Faithfulness library, or PASS component is proposed.
Host time, scheduling, tools, network, artifacts, credentials, and durable
storage are services behind interfaces, not kernel components.

## Normative control flow

1. The host adapter translates `raw_host_event` into `raw_host_input`. It does
   not construct `TurnRequest` or perform ingress/task normalization.
2. The Pre-ingress Security Restraint consumes `raw_host_input`, inspects only
   policy-permitted information, and emits `SecurityDecision` with `PASS`,
   `BLOCK`, or `ASK`. A `PASS` contains minimized `allowed_input`.
3. If authorization is not required, the restraint may return `PASS` or
   `BLOCK`. It may consume an existing `AuthorizationResult` only while the
   action, resource, request binding, evidenced lifetime, freshness, and
   revocation/reset state remain valid.
4. The authorization continuation is explicitly cross-turn. In Turn N, when
   authorization is required and an adequate current result is absent, the
   restraint creates a safe `authorization_request_ref` and a policy-bounded
   `PendingAuthorizationState`. The Host Adapter must bind that record to an
   evidenced `host_session` before later correlation is possible. Validation
   and Egress emits exactly one safe `ASK` `TerminalPacket`; Turn N ends and no
   ordinary routing occurs.
5. In Turn N+1, the Host Adapter receives a new `raw_host_event`. It may enter
   the authorization-evidence exchange only when provider evidence binds that
   event to the still-valid pending request in the current evidenced
   `host_session`. The Security Restraint first decides whether another attempt
   is permitted; the Authorization Evaluator then evaluates only the bound
   action, resource, and evidence scope. Its `AuthorizationResult` plus the
   pending context returns to the Security Restraint for a new
   `SecurityDecision`. `BLOCK`, `ASK`, or `UNAVAILABLE` ends Turn N+1 with one
   terminal packet. There is never a two-terminal host turn.
6. Only `SecurityDecision PASS` plus its minimized `allowed_input` reaches the
   Turn Controller. The Turn Controller is the sole owner of ingress/task
   normalization and constructs the normalized `TurnRequest`.
7. The Turn Controller validates `CapabilityReport` records. Declared and
   verified availability remain distinct.
8. The Turn Controller resolves one route and one owner, constructs ScopeLock,
   authorizes dependencies, and emits `ControlDecision`.
9. The locked owner is either model execution or a declared service path. The
   host adapter translates service calls; it does not create capability truth.
10. Source-bound work carries a source policy, allowed source scope, provenance,
   and evidence references.
11. Validation and Egress checks authorization, capability and service receipts,
   source policy, artifact proof, completion claims, owner identity, and
   ScopeLock containment.
12. It emits exactly one `TerminalPacket`, including the current-turn receipt.
    The host adapter delivers only that authorized output.

OPSEC never moves behind route selection. No deterministic-lane public output
bypasses final validation. Extra gates are not permitted unless a later
assignment demonstrates a distinct responsibility and concrete failure caused
by their absence.

## Ownership rules

- Persona is not a router, validator, capability oracle, or persistence proof.
- Operations Law remains model-facing law. Only independently provable packet,
  receipt, source-policy, transition, and containment invariants become code.
- The model may propose service requests and artifacts; it cannot certify host
  availability, current time, persistence, scheduling, or side effects.
- The core may authorize and validate a service request; it cannot perform or
  pretend the host service.
- A continuity provider may prove external durability; it cannot decide what a
  memory means or what context the model should use.
- Host adapters translate. They do not own kernel policy.
- Host adapters translate `raw_host_event` to `raw_host_input`; only the Turn
  Controller may normalize a passed input into `TurnRequest`.
- The Security Restraint owns initiation, re-entry, retry, expiry, exhaustion,
  cancellation, and replay policy for protected authorization interactions.
  Authorization evaluates evidence/results. The Host Adapter provides storage
  and correlation evidence when the host supports it; none may assume another's
  authority.

## Source-grounding modes

Every source-bound task declares one mode:

| Mode | Allowed factual basis |
|---|---|
| `source_only` | Positive support from the declared source scope is required. |
| `source_plus_user_input` | Declared sources plus explicit user-supplied facts. |
| `source_plus_verified_external` | Declared sources plus provider-verified external evidence. |
| `ordinary_background` | General model knowledge is allowed with normal uncertainty discipline. |
| `speculative_allowed` | Clearly labeled hypotheses or invention are allowed. |

For `source_only`, absence of contradiction is not enough. Unsupported claims
block; contradictions block; outside-scope needs are `ASK` when the scope can be
expanded by authority and otherwise `BLOCK`; unverifiable evidence is
`UNAVAILABLE`. BC-018 does not claim natural-language claims can already be
extracted or mechanically matched to sources. That part remains model-dependent
unless later tooling proves it can verify the relation.

## State lifetime classes

- `none`: no retained state.
- `turn`: discarded after the terminal receipt unless explicitly exported.
- `host_session`: host-owned state accepted only with provider, binding method,
  scope, freshness, record identity, expiry/lifetime boundary, and receipt or
  evidence reference.
- `durable_external`: external state proven only by a continuity-provider
  version and receipt.

Every state-bearing component and packet declares its lifetime. Moving state to
a longer lifetime is a state transition requiring the destination provider and
receipt; a Markdown declaration or model statement cannot perform the move. A
bare `session` label is not a lifetime and cannot satisfy a cross-turn
requirement. The deterministic core retains only turn state. Optional profile,
workflow, or other cross-turn context must arrive as evidenced current-turn
input from `host_session` or `durable_external`; the Turn Controller does not
hold it invisibly.

If the host cannot provide evidenced `host_session` state, ordinary cross-turn
authorization continuation is `UNAVAILABLE` and security-sensitive work fails
closed. Conversation history and model memory are never security state stores.
Continuity is not required for ordinary authorization when a verified
`host_session` substrate exists, and host-session state is never silently
promoted to `durable_external`.

## Minimality result

The four core components cannot be safely merged further:

- Security Restraint cannot merge into routing because its approved authority
  is before ordinary ingress.
- Authorization cannot merge into OPSEC because authorization evaluates an
  action/resource and evidence, while OPSEC minimizes or blocks protected
  ingress. Combining them would mix policy authority and protected state.
- Turn Controller cannot own final validation because route authorization and
  independent completion/egress proof would become one self-certifying owner.
- Validation and Egress cannot remain model-facing because capability, receipt,
  owner, artifact, and packet invariants require independent checks.

The three external boundaries cannot move into the core without falsely making
model judgment, platform service, or durable storage a kernel-owned fact.

## Acceptance disposition

The design answers the BC-018 acceptance questions affirmatively at the
specification level: the graph is understandable; each responsibility has one
owner; OPSEC precedes ingress; Auth is bounded; capability and persistence
claims require evidence; time and reminders separate reasoning from service;
Persona and teaching remain model-facing; Exec's useful control properties are
decomposed; BC-020 and BC-030 receive generic plug-in boundaries; SkillForge is
optional and external; and major ownership boundaries are explicit.

This does not assert implementation, parity, host availability, or runtime
behavior.
