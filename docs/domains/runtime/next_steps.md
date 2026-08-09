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

Two non-blocking security inputs remain explicit and unresolved: the policy for
an uncorrelated intervening turn travels with SUR-011 to security-authorized
OPSEC/Auth policy work, and integrity/rollback resistance for host-provided
authorization attempt state travels with SUR-012 to the BC-020 host-evidence
matrix.

The next specification-ready assignments are BC-020 and BC-030. Both remain
`spec-needed` and unstarted; neither has an approved packet, owner, or named
base. BC-020 targets Chat and Codex capability adapter contracts against the
corrected host-session/security-evidence boundary. BC-030 targets Local Mirror
continuity schema and lifecycle against the generic continuity-provider
boundary. No successor Python runtime implementation is authorized.

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
