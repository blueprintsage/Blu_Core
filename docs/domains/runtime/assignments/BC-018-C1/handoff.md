# BC-018-C1 — Implementation Handoff

status: review
owner: Codex
last_reviewed: 2026-08-08

## Identity

- Assignment: BC-018-C1
- Parent: BC-018
- Base commit: `7796c7e738e0ff66b677c79314b80cf2bbb09a63`
- Work branch: `bc-018-c1-security-state-correction`
- Work commit: `a87e7d7ea57688212c7c8461b5630c6ddb55a00f`
- Push status: pending at substantive handoff; final push reported externally
- Working-tree status: expected clean after the two authorized commits

## Result

Complete specification correction ready for independent semantic re-review.
BF-1, BF-2, and BF-3 are addressed without changing the component or packet
count and without implementing a runtime.

## Files changed

```text
MANIFEST.sha256
contracts/successor/README.md
contracts/successor/behavior_placement.json
contracts/successor/component_registry.json
contracts/successor/error_model.json
contracts/successor/interface_registry.json
contracts/successor/packet_registry.json
contracts/successor/traceability.json
contracts/successor/unresolved_register.json
docs/architecture/successor_boundaries.md
docs/architecture/successor_component_graph.md
docs/architecture/successor_kernel.md
docs/architecture/successor_migration_sequence.md
docs/dev/docs_index.md
docs/domains/runtime/assignments/BC-018-C1/assignment.md
docs/domains/runtime/assignments/BC-018-C1/handoff.md
docs/domains/runtime/assignments/BC-018-C1/review.md
docs/domains/runtime/assignments/BC-018-C1/validation.md
docs/domains/runtime/decisions.md
docs/domains/runtime/failures.md
docs/domains/runtime/next_steps.md
docs/domains/runtime/worklog.md
docs/worklogs/assignments.md
tests/successor_kernel/test_validate_successor_kernel_spec.py
tools/validate_successor_kernel_spec.py
```

## Deliverables completed

- Explicit Turn N / Turn N+1 pre-ingress authorization model with exactly one
  terminal packet per host turn.
- Four-class state lifetime model: `none`, `turn`, evidenced `host_session`,
  and receipted `durable_external`.
- Generic host-session evidence boundary and fail-closed unavailable result.
- `PendingAuthorizationState` state record with finite-attempt, expiry,
  binding, replay, exhaustion, cancellation/reset, status, and provenance
  semantics.
- Evidenced `AuthorizationResult` validity scope.
- Turn-local Turn Controller plus N1 time/profile ownership correction.
- Typed `ServiceExchange` authority classes resolving N5.
- Revised lifetime traceability resolving N8.
- Twelve-item unresolved register preserving protected policy and host-binding
  details for future authorized work.
- Ten focused negative tests plus the full existing suite.

## Unresolved items

- Exact maximum-attempt values, lockout/backoff rules, cancellation/reset
  details, and new-request-after-exhaustion policy.
- Accepted authorization evidence classes and assurance thresholds.
- Chat/Codex-specific host-session binding, freshness, expiry, correlation, and
  replay evidence mechanics.
- These are blocking inputs for implementation where marked, not gaps in the
  public finite-bound/expiry/binding/replay/fail-closed contract.

## Known risks

- Structural validation does not prove a host can furnish the required
  evidence or that a future runtime enforces the policy correctly.
- BC-020 must map real host evidence honestly; BC-030 remains separate and is
  not required for ordinary authorization when evidenced host-session state is
  available.

## Domain continuity updates

- Worklog: updated with C1 scope and validation summary
- Failures: updated with reusable cross-turn security-state failure rules
- Next steps: independent C1 semantic re-review, then Dad/Blu disposition

## Reviewer focus

- Verify the ASK ends Turn N and a new event begins Turn N+1, with one terminal
  packet in each host turn.
- Verify Security Restraint alone owns attempt permission; Auth owns evidence
  and result semantics; Host Adapter owns only substrate/correlation evidence.
- Verify no bare session lifetime, hidden controller state, replay-by-string,
  unbounded retries, or ordinary service authority remains.
- Verify N1, N5, and N8 are resolved without broadening into other review notes.

## Pre-review terminal-authority correction — 2026-08-08

### Identity

- Correction base: `b1e0f5c7ce3fddd7d71f6b2fa8050b0b55875b3c`
- Substantive correction commit: `311c572f3a28fe4e1cca04b75856faae3cfd6c60`
- Metadata/head commit: reported externally after creation
- Branch: `bc-018-c1-security-state-correction`
- Push status: pending at substantive handoff; final push reported externally

### Result

- Preserved `SecurityDecision` statuses `PASS`, `BLOCK`, and `ASK` only.
- Made the host-session binding attempt precede terminal selection.
- Binding success activates the pending interaction and emits one terminal
  `ASK` under the originating `SecurityDecision`.
- Binding `UNAVAILABLE` leaves the proposal inactive, non-resumable, and
  permanently non-correlatable, then emits one safe terminal `UNAVAILABLE`
  under the originating `SecurityDecision` with owner `security_restraint`.
- No `ControlDecision`, ordinary routing, new component, new packet, runtime,
  CTS, BC-020/BC-030, or PASS/SkillForge work was introduced.

### Exact substantive correction files

```text
MANIFEST.sha256
contracts/successor/error_model.json
contracts/successor/interface_registry.json
contracts/successor/packet_registry.json
docs/architecture/successor_boundaries.md
docs/architecture/successor_component_graph.md
docs/architecture/successor_kernel.md
docs/domains/runtime/assignments/BC-018-C1/assignment.md
docs/domains/runtime/assignments/BC-018-C1/handoff.md
docs/domains/runtime/assignments/BC-018-C1/validation.md
docs/domains/runtime/decisions.md
docs/domains/runtime/failures.md
docs/domains/runtime/next_steps.md
docs/domains/runtime/worklog.md
docs/worklogs/assignments.md
tests/successor_kernel/test_validate_successor_kernel_spec.py
tools/validate_successor_kernel_spec.py
```

### Reviewer focus

- Confirm provider-caused terminal `UNAVAILABLE` is an egress result under the
  originating `SecurityDecision`, not a fourth SecurityDecision status.
- Confirm an unbound proposed pending interaction can never be resumed or
  correlated.
- Confirm binding success `ASK` and binding failure `UNAVAILABLE` are mutually
  exclusive and still yield one terminal packet per host turn.
