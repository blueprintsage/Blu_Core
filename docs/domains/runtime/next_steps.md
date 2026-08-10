# Runtime Next Steps

status: active
owner: docs/domains/runtime
last_reviewed: 2026-08-08

## Closed lineage

BC-010, BC-010-C1, BC-010-C2, BC-015, BC-016, BC-017, BC-017-C1,
BC-018, and BC-018-C1 are complete.

The runtime-contract extraction records the CTS source faithfully, including
unresolved declarations. It does not prove behavioral parity or implement a
Python runtime.

## Next safe step

The closed BC-018 lineage includes the successor boundary specification and
BC-018-C1 cross-turn security-state correction. Claude's original BC-018
`return-for-correction` review and the C1 `approve-with-notes` re-review remain
immutable history. Final closure has zero blocking findings.

BC-020 is in `review` on its authorized exact base after producing the Chat/Codex
host-adapter specification. SUR-012 is resolved at the
generic host-evidence contract level: protected cross-turn continuation requires
provider-bound identity/state/request/result scope, freshness/expiry, replay/
consumption state, integrity, and monotonic rollback-resistant attempt state.
Insufficient evidence returns unavailable rather than inventing safety.

This resolution does not claim current surface availability. Dad's live Chat
binding was not probed and remains unknown. The observed Codex desktop binding
is unavailable for protected cross-turn authorization continuation because the
adapter-visible interface lacks replay/consumption and rollback-resistant
attempt-state evidence.

SUR-011 remains a future security-authorized policy input for protected attempt
values, retry/lockout/backoff, cancellation/reset, new-request-after-exhaustion,
and unrelated intervening turns. BC-030 remains `spec-needed` globally and
`ready_for_spec` architecturally: `host_session` remains host-local and
`durable_external` still requires an explicit continuity-provider receipt.

The next safe action after the substantive/metadata commits and branch push is
Claude's independent semantic review. Do not begin BC-030 or successor runtime
implementation.

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

Do not begin successor design, BC-020, or BC-030; implement a Python runtime or
successor control plane; restore historical capabilities; or resolve the 28
current-source gaps without an approved packet and named base.
