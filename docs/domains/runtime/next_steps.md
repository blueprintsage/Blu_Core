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

BC-018 has produced a successor-kernel specification on exact base
`a5e68b3189c60e2d5b8acbe8a212d69b720dec58` and is in `review`.

Claude performs the separately authorized independent semantic review of the
corrected BC-018 head after the pre-review ownership/Auth contract correction.
Dad and Blu decide integration and closure.

BC-018 concludes that BC-020 and BC-030 are both `ready_for_spec` against the
generic adapter and continuity boundaries. Their global rows remain
`spec-needed`; neither has an approved packet, owner, or named base and neither
has started. No successor runtime implementation is eligible to begin.

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
