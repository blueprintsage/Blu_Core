# Runtime Next Steps

status: active
owner: docs/domains/runtime
last_reviewed: 2026-08-10

## Closed lineage

BC-010, BC-010-C1, BC-010-C2, BC-015, BC-016, BC-017, BC-017-C1,
BC-018, BC-018-C1, BC-020, and BC-020-C1 are complete.

The runtime-contract extraction records the CTS source faithfully, including
unresolved declarations. It does not prove behavioral parity or implement a
Python runtime.

## Next safe step

The closed BC-018 lineage includes the successor boundary specification and
BC-018-C1 cross-turn security-state correction. Claude's original BC-018
`return-for-correction` review and the C1 `approve-with-notes` re-review remain
immutable history. Final closure has zero blocking findings.

BC-020 and BC-020-C1 are closed after Claude's original
`return-for-correction` review, the bounded BF-1 scheduling-evidence correction,
and Claude's final `approve-with-notes` C1 re-review with zero blockers. The
closure is administrative and changes no adapter semantics.

SUR-012 remains resolved at the generic host-evidence contract level: protected
cross-turn continuation requires provider-bound identity/state/request/result
scope, freshness/expiry, replay/consumption state, integrity, and monotonic
rollback-resistant attempt state. Insufficient evidence returns unavailable
rather than inventing safety.

This resolution does not claim current surface availability. Dad's live Chat
binding was not probed and remains unknown. The observed Codex desktop binding
is unavailable for protected cross-turn authorization continuation because the
adapter-visible interface lacks replay/consumption and rollback-resistant
attempt-state evidence.

BC-020-C1 corrected the review blocker without changing the generic architecture.
The observed Codex scheduling interface remains recorded, while
`schedule.create`, `schedule.recurring`, and `schedule.update_cancel` are
`unknown` pending operationally relevant provider evidence. Corrected Codex
totals are 52 capabilities: 24 verified available, 6 verified unavailable, 4
documented possible, 17 unknown, and 1 not applicable.

SUR-011 remains unresolved as a future security-authorized policy input for protected attempt
values, retry/lockout/backoff, cancellation/reset, new-request-after-exhaustion,
and unrelated intervening turns. BC-030 remains `spec-needed` globally and
`ready_for_spec` architecturally: `host_session` remains host-local and
`durable_external` still requires an explicit continuity-provider receipt.

BC-030 is unstarted and must not be promoted to active without a separately
approved packet and named base. Chat live probing is a separate future
assignment requiring explicit authorization. Successor runtime implementation
remains unauthorized.

The following non-blocking archaeology-quality notes remain preserved for
separately authorized hardening work:

- drilldown-list family semantics and cleanup;
- evidence-grade vocabulary consistency;
- inference-registration cleanup;
- wording around compensatory complexity;
- validator and review-state coupling;
- document-quality validation hardening;
- minor locator-scoping and consistency cleanup.

The evidence limitations preserved in the review records also remain in force,
including unreadable Deflate64 members, chronology gaps, lack of historical
runtime telemetry, and undefined current CTS Auth/OPSEC services.

### Legacy PASS exclusion

Historical PASS may be inspected only when necessary to establish chronology or
explain how old Exec orchestration compensated for unreliable components.

Legacy PASS must not be treated as a behavior-recovery candidate, recommended
for restoration, treated as an architectural precedent, used as the successor
PASS design, or allowed to displace or redefine the newer PASS specification.

Historical archaeology must not spend analysis effort evaluating whether old PASS should return.
The newer PASS is the relevant successor reference and remains separate from
historical archaeology.

Do not begin BC-030 or Chat live probing; implement a Python runtime or successor
control plane; restore historical capabilities; or resolve the 28 current-source
gaps without an approved packet and named base.
