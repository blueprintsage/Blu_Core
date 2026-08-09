# Host Security Evidence and SUR-012

status: review
owner: docs/domains/runtime
last_reviewed: 2026-08-08
assignment: BC-020

## Host identity is not authorization identity

Conversation, thread, project, account sign-in, and session-like UI identifiers
may help ordinary correlation. They are not sufficient for protected Auth
continuation unless supported provider evidence establishes binding, integrity,
freshness/expiry, action/resource/request scope, replay state, and rollback
resistance. An opaque-looking string receives no special trust.

A product may authenticate an account internally while exposing no identity,
role, or credential evidence usable by Blu's Authorization Evaluator. Tone,
writing style, conversation history, memory, private-fact knowledge, and a
claimed account name are forbidden substitutes. When the adapter cannot verify
the assertion, it returns unavailable or insufficient.

`HostApprovalEvidence` separately records host permission for an operation.
Host approval can coexist with a failed Blu authorization decision; neither
implies the other. The Host Adapter transports approval state and never creates
`AuthorizationResult`.

## HostSessionEvidence

The normalized record includes binding ref, family/surface/provider, binding
method, state-record identity, observation/lifetime boundary, scope, integrity,
freshness, replay, rollback resistance, receipt/evidence ref, availability, and
limitations. It is never synthesized from conversational continuity.

Replay evidence records request binding, optional event identity, event
freshness, prior-consumption state, one-shot/reusable semantics, detection
capability, replay status, and provider evidence. A timestamp does not prove
prior non-consumption.

Correlation classes are `pending_request_match`,
`same_host_session_uncorrelated`, `different_host_session`, `expired_request`,
`replayed_request`, `ambiguous`, and `unavailable`. They report evidence; they
do not decide what OPSEC/Auth does.

## Attempt-count integrity

Protected cross-turn state requires provider-bound state identity, request/
action/resource binding, tamper integrity, freshness/expiry, replay/consumption
state, and monotonic or rollback-resistant attempt state. The contract grades
rollback evidence as `none`, `untrusted`, `integrity_evidenced`, or
`monotonic_or_rollback_resistant`.

A client-local mutable counter can simply be reset. A state record whose
`attempt_count`, request status, expiry, or consumed state can be rewritten or
rolled back without detection is therefore insufficient. Model memory cannot
repair it. The adapter returns insufficient/unavailable and protected
cross-turn continuation stops.

## SUR-012 disposition

SUR-012 is resolved at the generic host-evidence contract level. The required
properties, normalized failure behavior, surface self-report, and
Security-Restraint consumption contract are explicit. Resolution does not mean
that a current surface is available:

- Dad's current Chat binding: unknown and unavailable for protected continuation
  until a future binding provides complete security-grade evidence.
- Observed Codex desktop binding: verified unavailable for protected
  continuation because the adapter-visible interface lacks replay/consumption
  and monotonic rollback-resistant attempt state.

SUR-011 remains unresolved. BC-020 does not choose protected maximum-attempt,
retry/lockout/backoff, cancellation/reset, new-request-after-exhaustion, or
unrelated-intervening-turn policy. It supplies enough correlation evidence for
that future policy to distinguish cases without guessing.

BC-030 remains `ready_for_spec`: evidenced `host_session` is host-local scope;
`durable_external` requires an explicit generic continuity-provider operation
and receipt. BC-020 neither implements nor substitutes for Local Mirror.
