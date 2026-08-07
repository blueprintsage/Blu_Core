# Runtime Next Steps

status: active
owner: docs/domains/runtime
last_reviewed: 2026-08-06

## Closed lineage

BC-010, BC-010-C1, BC-010-C2, BC-015, and BC-016 are complete.

The runtime-contract extraction records the CTS source faithfully, including
unresolved declarations. It does not prove behavioral parity or implement a
Python runtime.

## Next safe step

BC-016 is closed. BC-017 is the next eligible assignment, but it has not started
and is not authorized by this closure. It requires a separate approved
assignment packet and named base.

Claude's NB-1 through NB-10 remain available as review evidence. NB-1 and NB-4
must be resolved or explicitly bounded before BC-017 relies on the affected
records. NB-2, NB-3, and NB-6 remain validator and evidence-hardening follow-ups.
The remaining notes stay preserved for the next assignment that legitimately
touches their records.

### Legacy PASS exclusion

Historical PASS may be inspected only when necessary to establish chronology or
explain how old Exec orchestration compensated for unreliable components.

Legacy PASS must not be treated as a behavior-recovery candidate, recommended
for restoration, treated as an architectural precedent, used as the successor
PASS design, or allowed to displace or redefine the newer PASS specification.

BC-017 must not spend analysis effort evaluating whether old PASS should return.
The newer PASS is the relevant successor reference and remains separate from
historical archaeology.

Do not begin BC-020 or BC-030, implement a Python runtime or successor control
plane, restore historical capabilities, or resolve the 28 current-source gaps
without an approved packet and named base.
