# Runtime Next Steps

status: active
owner: docs/domains/runtime
last_reviewed: 2026-08-05

## BC-010

1. Commit the validated BC-010 implementation as one reviewable work commit.
2. Record the work SHA in one metadata-only receipt commit under the authorized
   amendment; do not change contracts, tools, tests, or golden files in it.
3. Have Claude perform the assigned read-only semantic review against all seven
   golden files, focusing on unresolved declarations, route/lane fidelity,
   schema non-invention, and Persona/Operations non-reduction.
4. Let Blu or Dad decide every item in `contracts/runtime/unresolved_register.json`;
   BC-010 must not resolve those items itself.
5. Do not begin BC-020 or BC-030 until their packets are approved and bases are
   named.
