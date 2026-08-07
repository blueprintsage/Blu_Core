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

BC-017 remains in review after Claude returned three blocking record-production
defects. BC-017-C1 corrects only the corrupted README, reproduction commands,
and Exec-contraction chronology. Its next safe step is a separately authorized
read-only semantic re-review of the BC-017-C1 metadata commit, modifying only
the C1 `review.md`. Dad and Blu decide integration and closure.

NB-2, NB-3, and NB-6 remain validator and evidence-hardening follow-ups. The
remaining BC-016 notes stay preserved for an assignment that legitimately
touches their records.

### Legacy PASS exclusion

Historical PASS may be inspected only when necessary to establish chronology or
explain how old Exec orchestration compensated for unreliable components.

Legacy PASS must not be treated as a behavior-recovery candidate, recommended
for restoration, treated as an architectural precedent, used as the successor
PASS design, or allowed to displace or redefine the newer PASS specification.

Historical archaeology must not spend analysis effort evaluating whether old PASS should return.
The newer PASS is the relevant successor reference and remains separate from
historical archaeology.

Do not begin successor design, BC-018, BC-020, or BC-030; implement a Python
runtime or successor control plane; restore historical capabilities; or resolve
the 28 current-source gaps without an approved packet and named base.
