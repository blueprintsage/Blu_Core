# Runtime Next Steps

status: active
owner: docs/domains/runtime
last_reviewed: 2026-08-06

## BC-010

1. Have Claude perform the assigned read-only semantic review of work commit
   `40138b6e16f28c01904aae97158878468ee47ad0` against all seven golden files,
   focusing on unresolved declarations, route/lane fidelity, schema
   non-invention, and Persona/Operations non-reduction.
2. Let Blu or Dad decide every item in `contracts/runtime/unresolved_register.json`;
   BC-010 must not resolve those items itself.
3. Do not begin BC-020 or BC-030 until their packets are approved and bases are
   named.

## BC-010-C1

1. Claude performs a read-only second semantic review against the repair work
   commit recorded in the BC-010-C1 handoff.
2. Review source-role separation, repaired routes/exclusivity, referenced
   component non-invention, validator guarantees, exact anchoring, PASS
   provenance, dependency wording, and StateTree conflict preservation.
3. Blu or Dad decides integration. Keep both BC-010 and BC-010-C1 in `review`
   until that disposition; do not begin BC-020 or BC-030.

## BC-010-C2

1. Claude performs a read-only semantic review against the C2 repair work
   commit recorded in its handoff.
2. Review the null OPSEC lane-class representation, UR-028, cross-role inference
   provenance, lane closure, dependency cleanup, and reason-specific negative
   tests.
3. Blu or Dad decides integration. Keep BC-010, BC-010-C1, and BC-010-C2 in
   `review`; do not merge this branch or begin BC-020 or BC-030.
