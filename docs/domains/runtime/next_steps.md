# Runtime Next Steps

status: active
owner: docs/domains/runtime
last_reviewed: 2026-08-06

## Closed lineage

BC-010, BC-010-C1, and BC-010-C2 are complete.

The runtime-contract extraction records the CTS source faithfully, including
unresolved declarations. It does not prove behavioral parity or implement a
Python runtime.

## Next safe step

Prepare a bounded assignment packet for a Runtime Viability Audit before
starting Python runtime implementation.

The audit must distinguish:

1. live and stable behavior;
2. live but nondeterministic or host-dependent behavior;
3. declared but not observably functioning behavior;
4. conflicting or underspecified behavior;
5. explicitly deferred or removed behavior;
6. new successor-runtime capability.

Do not begin BC-020, BC-030, or Python implementation until the applicable
assignment packet is approved and its exact base is named.
