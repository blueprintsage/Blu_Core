# Successor Boundaries

status: review
owner: docs/domains/runtime
last_reviewed: 2026-08-08
assignment: BC-018
correction: BC-018-C1

## Pre-ingress security boundary

The Host Adapter translates `raw_host_event` to `raw_host_input` and stops. The
Pre-ingress Security Restraint receives that `raw_host_input`, an approved policy
reference, and only the bounded `AuthorizationResult` the policy permits it to inspect.
It may inspect features necessary to identify protected-source, identity-
challenge, clone/copy/recreation, disclosure, or related policy categories. It
must minimize retained content.

It returns `SecurityDecision`:

- `PASS`: provides minimized `allowed_input` and explicit redactions;
- `BLOCK`: provides a safe reason code and no protected details;
- `ASK`: provides one safe authorization or clarification request and, when
  authorization is required, a safe `authorization_request_ref`.

Redaction is allowed only when policy explicitly authorizes a transformation
that leaves a safe, meaningful task. It may not redact merely to force an
otherwise blocked request into ordinary routing. Protected-source handling is
represented by policy and reason references, never embedded challenge content.

The bounded pre-ingress authorization loop is normatively cross-turn.

**Turn N — authorization requested**

1. The Security Restraint evaluates `raw_host_input`.
2. If authorization is not required, or an existing `AuthorizationResult` is
   valid for the action, resource, binding, evidenced lifetime, freshness, and
   revocation/reset state, it may return `PASS` or `BLOCK`.
3. Otherwise it creates a safe `authorization_request_ref` and
   `PendingAuthorizationState`. The record includes the protected
   action/resource scope, binding, freshness, expiry, finite attempt policy,
   replay policy, status, and provenance.
4. Before the request can be correlated later, the Host Adapter binds the
   record to evidenced `host_session` state. If it cannot, continuation is
   `UNAVAILABLE` and fails closed for the protected interaction.
5. Validation and Egress emits exactly one safe `ASK` `TerminalPacket`. Turn N
   ends. No Turn Controller routing occurs.

**Turn N+1 — authorization evidence returned**

1. The Host Adapter receives a new `raw_host_event` and accepts it for the
   bounded authorization exchange only when provider evidence correlates it to
   the still-valid pending request in the current evidenced `host_session`.
   Matching a request-ref string is insufficient.
2. Security Restraint is the sole authority deciding whether re-entry and
   another attempt are permitted under retry, expiry, exhaustion, cancellation,
   lockout, action/resource binding, and replay policy.
3. The Authorization Evaluator evaluates only the authorized action, resource,
   and evidence scope and returns an `AuthorizationResult` with an evidenced
   validity lifetime.
4. The result and still-bound pending context return to the Security Restraint,
   which emits a new `SecurityDecision`.
5. Only `PASS` may reach the Turn Controller. `BLOCK`, `ASK`, or `UNAVAILABLE`
   ends Turn N+1 with exactly one terminal packet. There is no two-terminal
   host turn.

OPSEC consumes the result but does not authenticate. Auth evaluates evidence
but does not rewrite OPSEC or attempt policy. The Host Adapter stores/carries
provider-evidenced host-session state and correlation receipts but owns neither
policy. The loop never enters ordinary routing before `PASS`. Missing,
ambiguous, invalid, expired, exhausted, replayed, unbound, or unavailable
required evidence fails closed. Conversational identity inference is not
authentication.

## Authorization boundary

Auth authorizes a specific action over a specific resource scope. An
authorization request names the subject if known, action, resource, requested
scope, policy reference, and required assurance. Evidence is an explicit host,
user, credential, role, consent, or policy receipt accepted by that policy.

The host supplies evidence or an honest unavailable result. The kernel receives
no magical identity truth from the model. The Authorization Evaluator returns
`PASS`, `BLOCK`, `ASK`, or `UNAVAILABLE` plus result identity, action/resource
scope, assurance, issue and expiry evidence, validity lifetime, provider and
evidence references, revocation/reset state, and a safe reason code. For a
pre-ingress request, its `request_ref` must match the safe
`authorization_request_ref` through the provider-evidenced request binding,
and its result returns to the Security Restraint rather than entering the Turn
Controller.

Authorization validity may be `turn`, evidenced `host_session`, or receipted
`durable_external`; bare `session` validity is forbidden. The Security
Restraint consumes an existing result only while its scope, binding, lifetime,
freshness, and status remain valid. Logout, reset, expiry, host-session loss,
policy change, or explicit revocation invalidates scoped state as defined;
changing provider-backed state requires a receipt.

Every `PendingAuthorizationState` has a policy-supplied finite positive attempt
bound, expiry, request binding, replay rule, exhaustion behavior, and
cancellation/reset behavior. Exact counts, thresholds, evidence classes, and
lockout/backoff values remain protected future policy inputs. Exhaustion fails
closed and does not automatically issue a new request that defeats the bound.
A new request after exhaustion requires an explicitly permitted new
authorization interaction under Security Restraint policy.
Protected actions include protected-source access, privileged configuration or
mutation, and any later policy-named action. Exact policy and evidence values
remain unresolved under a security-authorized assignment.

## Capability truth

`CapabilityReport` records:

```text
capability_id, provider, declared, availability, verification_method, scope,
limitations, timestamp_or_turn_scope, receipt, failure_reason
```

`declared=true` means only that a contract or adapter knows the capability.
`availability=verified` requires a receipt or direct observation suitable for
the capability. The Turn Controller rejects stale, out-of-scope, or unverified
reports. The kernel makes no current-time, persistence, future-wake,
filesystem, network, artifact, or tool-execution claim without matching
evidence.

## Time and reminders

The Turn Controller may perform deterministic arithmetic over supplied
timestamps, timezones, durations, and recurrence rules as a current-turn
utility, while the model may discuss the supplied values. Verified current time
is still a host service. A statement such
as “the current time is X” requires a time-provider result containing the
timestamp, timezone/offset, verification method, turn or timestamp scope, and
receipt.

Reminder intent is model interpretation. The Turn Controller normalizes it into
a schedule request with local time, timezone, recurrence, ambiguity state, and
requested action. Future scheduling is a host service. Creation success
requires provider capability plus a receipt containing provider schedule ID,
normalized schedule, operation, and result. Update and cancellation use that
provider identity. Recurrence belongs to the provider contract; prompt text is
never a wake mechanism.

## MMU, continuity, and persistence

The successor separates:

- memory organization: categories, provenance, state, and transition rules;
- retrieval: provider/source request and result;
- context staging: current-turn material offered to the model, optionally from
  an evidenced `host_session` or continuity result;
- host-session state: host-owned cross-turn state with binding, freshness,
  expiry, identity, provider, and receipt evidence;
- durable persistence: external write proven by receipt;
- continuity provider: the generic read/write/version/conflict boundary.

There is no MMU component. The Turn Controller validates state classes and
transitions; the model interprets relevance; the continuity provider proves
external reads and writes. `none`, `turn`, evidenced `host_session`, and
receipted `durable_external` are the lifetime classes. A bare `session` label is
not a substrate. Promotion to `durable_external` requires an explicit
continuity request, version/conflict result, and receipt. The Turn Controller is
turn-local and receives any optional cross-turn context as evidenced input for
the current turn. BC-030 owns Local Mirror schema, lifecycle, retention, and
storage decisions.

## Teaching and classroom behavior

Pedagogical judgment, scaffolding, checks for understanding, explanation, and
lesson sequencing remain model-facing. Curriculum assets may arrive through an
optional source or skill/context provider. Classroom context/state, schedules, and
durable student records are separate service and continuity concerns.

There is no School Engine. Any future classroom state must earn a separate
minimal schema, authorization boundary, deterministic transitions, scheduling
contract, continuity receipt, and regression matrix. Modern SkillForge/PASS may
later supply external skill or curriculum context; it is not kernel-owned.

## Mood disposition

Natural affect and expressive adaptation remain Persona/model behavior. If
lightweight public profile metadata is retained, it is optional context supplied
for the current turn from an evidenced host-session/context source. The Turn
Controller is neither its semantic owner nor its storage owner, and the metadata
must not control cognition, routing, identity, or Persona. No current evidence
earns a Mood component or durable mood state. Absent optional metadata, Persona
guidance is sufficient.

## Source grounding and Faithfulness

Source policy modes are `source_only`, `source_plus_user_input`,
`source_plus_verified_external`, `ordinary_background`, and
`speculative_allowed`. The ControlDecision carries source scope and allowed
evidence classes. ValidationResult distinguishes:

- unsupported claim: no positive support;
- contradiction: evidence conflicts with the claim;
- outside scope: evidence would require an unauthorized expansion;
- unverifiable: the provider or semantic relation cannot be established.

`source_only` factual output requires positive source support. Unsupported and
contradictory claims block. Outside scope asks only when an authorized scope
revision can resolve it. Unverifiable results are unavailable or block when the
lane requires proof. BC-018 recovers this principle from the unshipped
Faithfulness sidecar but rejects its library name and object model.

Natural-language claim extraction, entailment, and source mapping remain
model-dependent unless later deterministic tooling demonstrates real
verification. A JSON claim list authored solely from model confidence is not
proof.

## ScopeLock

ScopeLock freezes the active task, requested deliverable, allowed subjects,
allowed actions, explicit constraints, source requirement, workflow boundary,
and prohibited moves. The raw allowed turn, active receipted workflow context,
explicit constraints, and owner contract establish it.

The user, Project Owner/Lead where project authority applies, or the currently
locked owner may request a revision. Only the Turn Controller authorizes and
versions it. A new subject, action, deliverable shape, source scope, side effect,
or workflow outside the lock is scope escape. Conflict yields `ASK` when one
bounded authorization can resolve it; otherwise `BLOCK`. Clarification and
authorized revision are not scope escapes. Terminal receipts include the
ScopeLock identity and any revision chain.

## Packets and receipts

The minimum packet set is:

1. `TurnRequest`
2. `SecurityDecision`
3. `CapabilityReport`
4. `AuthorizationResult`
5. `ControlDecision` (includes route, owner, ScopeLock, and SourceScope)
6. `ServiceExchange` (request/result union)
7. `ValidationResult`
8. `TerminalPacket` (includes current-turn ExecutionReceipt)

Distinct historical packet names were collapsed when they did not have
distinct control semantics. Exact fields and invariants are normative in
`contracts/successor/packet_registry.json`.

`PendingAuthorizationState` is a normative state record, not a ninth packet or
an eighth component. Security Restraint owns its attempt-policy semantics; the
Host Adapter supplies the evidenced `host_session` substrate and correlation
receipts when available. An explicitly requested continuity operation may store
it as `durable_external`, but ordinary host-session authorization does not
require continuity and is never silently promoted to it.

`ServiceExchange.authority_class` is either `ordinary_control` or
`pre_ingress_authorization`. Ordinary control requires a `ControlDecision`.
Pre-ingress authorization requires the authorization request and host-session
binding references, may use only `IF-AUTHORIZATION-PROVIDER` with service ID
`authorization_evidence`, and carries no authority for tools, source lookup,
scheduling, unrelated continuity writes, model execution, or ordinary service
dispatch.

Packet ownership is also normative: the Host Adapter produces `raw_host_input`,
the Security Restraint produces `SecurityDecision` with minimized
`allowed_input`, and only the Turn Controller produces `TurnRequest` after
`SecurityDecision PASS`. Pre-ingress `BLOCK`/`ASK` terminal validation uses the
`SecurityDecision` as `authority_ref`; routed terminal validation uses the
`ControlDecision`.

## Error and terminal model

The common statuses are `PASS`, `BLOCK`, `ASK`, `UNAVAILABLE`, `INVALID`, and
`ERROR`. They remain distinct because each changes control flow. Security,
authorization-required, `source_only`, owner-locked, and proof-required lanes
fail closed when evidence is absent or invalid. Ordinary conversation may
degrade safely when an unused optional host capability is absent.

## Host adapter boundary

The generic adapter discovers capabilities, translates `raw_host_event` into
`raw_host_input`, translates service invocation, delivers authorized output,
returns artifact and side-effect receipts, exposes time/scheduling where
supported, translates host-specific errors, and passes identity/authorization
evidence where the host can establish it. When genuinely supported, its
host-session state result supplies an opaque session binding, provider,
verification/binding method, scope, freshness, state record identity, expiry or
lifetime boundary, receipt/evidence reference, and unavailable/failure result.
It correlates a new host event to an outstanding request through that evidence.

The adapter does not construct `TurnRequest`, normalize ingress/task semantics,
decide OPSEC/Auth/attempt policy, infer authorization, or treat conversation
history/model memory as security state. If it cannot evidence cross-turn state,
the continuation is unavailable. BC-020 maps Chat and Codex to this contract
and must document differences rather than simulate parity.

## Continuity provider boundary

The provider supports read and write with namespace/scope, lifetime,
provenance, version, expected-version conflict handling, result limitations,
and receipt. Unavailable behavior returns `UNAVAILABLE`; conflict returns an
explicit conflict result. No fallback model prose creates or repairs durable
state. BC-030 maps Local Mirror to this boundary without changing core
ownership.

## SkillForge/PASS and Alice boundaries

Modern SkillForge/PASS may implement the optional Skill and Curriculum Context
Provider. It remains versioned, provenance-bearing, authorized, optional, and
external. The kernel is not dependent on Blu-specific Skill Cards. Legacy PASS
is rejected.

Alice remains a non-authoritative behavioral/profile-controller reference. No
Alice identity, mythos, mode system, or IP-specific architecture is imported.
