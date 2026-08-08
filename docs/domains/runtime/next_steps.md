# Runtime Next Steps

status: active
owner: docs/domains/runtime
last_reviewed: 2026-08-08

## Closed lineage

BC-010, BC-010-C1, BC-010-C2, BC-015, BC-016, BC-017, and BC-017-C1
are complete.

The runtime-contract extraction records the CTS source faithfully, including
unresolved declarations. It does not prove behavioral parity or implement a
Python runtime.

## Next safe step

BC-017 and BC-017-C1 are closed after Claude's independent C1 re-review at
`bea9463f0dbbae1c3944c5f44a7843c757d7f0bb` returned
`approve-with-notes` with zero blocking findings.

Next eligible assignment: none. BC-020 and BC-030 remain `spec-needed`; neither
has an approved packet, owner, or closure-authorized base for implementation.
Started: no.

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
