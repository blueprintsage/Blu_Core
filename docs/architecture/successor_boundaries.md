# Successor Boundaries

status: review
owner: docs/domains/runtime
last_reviewed: 2026-08-08
assignment: BC-018

## Pre-ingress security boundary

The Pre-ingress Security Restraint receives raw host input, an approved policy
reference, and only the authorization summary the policy permits it to inspect.
It may inspect features necessary to identify protected-source, identity-
challenge, clone/copy/recreation, disclosure, or related policy categories. It
must minimize retained content.

It returns `SecurityDecision`:

- `PASS`: provides minimized `allowed_input` and explicit redactions;
- `BLOCK`: provides a safe reason code and no protected details;
- `ASK`: provides one safe authorization or clarification request.

Redaction is allowed only when policy explicitly authorizes a transformation
that leaves a safe, meaningful task. It may not redact merely to force an
otherwise blocked request into ordinary routing. Protected-source handling is
represented by policy and reason references, never embedded challenge content.

OPSEC may consume an `AuthorizationResult`, but it does not authenticate. Auth
may be invoked when OPSEC says authorization is required, but it does not
rewrite OPSEC policy. OPSEC remains outside ordinary route ownership. Missing,
ambiguous, invalid, or unavailable required evidence fails closed. This design
does not claim conversational identity inference is authentication.

## Authorization boundary

Auth authorizes a specific action over a specific resource scope. An
authorization request names the subject if known, action, resource, requested
scope, policy reference, and required assurance. Evidence is an explicit host,
user, credential, role, consent, or policy receipt accepted by that policy.

The host supplies evidence or an honest unavailable result. The kernel receives
no magical identity truth from the model. The Authorization Evaluator returns
`PASS`, `BLOCK`, `ASK`, or `UNAVAILABLE`, evidence references, assurance,
session effect, and a reason code.

Session-scoped authorization may exist only when a successful result explicitly
creates it and names its scope and expiry/reset behavior. It must never be
assumed from prior tone, names, memory, or an earlier unrelated authorization.
Logout, reset, expiry, host-session loss, policy change, or explicit revocation
clears state; clearing that affects a provider-backed state requires a receipt.
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

Time reasoning is arithmetic over supplied timestamps, timezones, durations,
and recurrence rules. Verified current time is a host service. A statement such
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
- context staging: turn or session material offered to the model;
- session state: explicitly scoped non-durable control state;
- durable persistence: external write proven by receipt;
- continuity provider: the generic read/write/version/conflict boundary.

There is no MMU component. The Turn Controller validates state classes and
transitions; the model interprets relevance; the continuity provider proves
external reads and writes. `turn`, `session`, `host_session`, and
`durable_external` are distinct. Promotion to `durable_external` requires a
continuity request, version/conflict result, and receipt. BC-030 owns Local
Mirror schema, lifecycle, retention, and storage decisions.

## Teaching and classroom behavior

Pedagogical judgment, scaffolding, checks for understanding, explanation, and
lesson sequencing remain model-facing. Curriculum assets may arrive through an
optional source or skill/context provider. Class/session state, schedules, and
durable student records are separate service and continuity concerns.

There is no School Engine. Any future classroom state must earn a separate
minimal schema, authorization boundary, deterministic transitions, scheduling
contract, continuity receipt, and regression matrix. Modern SkillForge/PASS may
later supply external skill or curriculum context; it is not kernel-owned.

## Mood disposition

Natural affect and expressive adaptation remain Persona guidance. The only
deterministic representation that may later be useful is explicit lightweight
public/session profile metadata, and it must not control cognition, routing, or
identity. No current evidence earns a Mood component or durable mood state.
Absent optional metadata, Persona guidance is sufficient.

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

## Error and terminal model

The common statuses are `PASS`, `BLOCK`, `ASK`, `UNAVAILABLE`, `INVALID`, and
`ERROR`. They remain distinct because each changes control flow. Security,
authorization-required, `source_only`, owner-locked, and proof-required lanes
fail closed when evidence is absent or invalid. Ordinary conversation may
degrade safely when an unused optional host capability is absent.

## Host adapter boundary

The generic adapter discovers capabilities, normalizes host input, translates
service invocation, delivers authorized output, returns artifact and side-
effect receipts, exposes time/scheduling where supported, translates
host-specific errors, and passes identity/authorization evidence where the host
can establish it. It does not decide kernel policy. BC-020 maps Chat and Codex
to this contract and must document differences rather than simulate parity.

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
