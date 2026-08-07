# Historical Archive Source Map

status: review
owner: docs/domains/runtime
last_reviewed: 2026-08-06
assignment: BC-016

## Purpose

This directory integrates a sanitized, machine-readable map of historical Blu
kernel archives for later bounded archaeology. It records stable identities,
structure, duplicates, reconciliation, and representative milestones. It does
not import archive bytes or determine which historical behaviors worked.

## Authority boundary

The immutable current CTS remains `kernel/golden/v0.22.0/**`. Every source in
this directory has `source_role: historical_behavioral_reference` or is a
generated discovery input, and every historical source has
`authority: non_authoritative_for_current_runtime`.

Archive declarations, filenames, feature markers, structural metrics, and
implementation-style Markdown do not prove execution, stability, reliability,
or fitness for recovery. BC-017, if separately approved, may perform bounded
behavioral archaeology against selected milestones.

## Source identities

- `dad_kernel_root`: live historical development archive tree.
- `blu_kernel_snapshot`: stable outer `Kernel.zip` container supplied by Dad
  and independently verified during BC-016.
- `external_discovery_output`: generated inventory inputs consumed and checked
  during integration.

The outer snapshot SHA-256, live-root payload manifest, archive-file SHA-256,
archive content manifest, and branch file-set manifest are distinct identities.
They are never substituted for one another.

## Path sanitization

Repository records contain only `source_root_id` plus normalized
`relative_path`. Drive letters, usernames, home directories, machine names,
and neighboring paths are excluded. Snapshot member paths retain the stable
`Kernel/` wrapper only.

## Duplicate and reconciliation policy

Exact duplicate groups require identical canonical record SHA-256 values.
Duplicates remain separate inventory records. Identical normalized member
content with different container hashes is described as a relationship, not an
exact duplicate. Hash mismatches remain unresolved; timestamps never select an
authority winner.

Reconciliation compares the external discovery, live root, and stable snapshot
without modifying any source. The stable snapshot matched all 279 live files by
relative path and SHA-256.

## Milestone policy

The milestone set is small and representative rather than exhaustive. It
covers major structural eras and feature-marker prominence while explicitly
denying behavioral proof. Overlapping archives are retained even when one is a
better later sampling target.

## Structural metrics

Imported metrics use case-insensitive, documented discovery rules: Python
`splitlines()` for line count; ATX headings; declaration lines beginning with
module/component/service/library/program; RuntimeGate/gate tokens; exact
`must`; `validat*` forms; and `if|when|unless|otherwise` conditionals. Metrics
are structural indicators only.

## Known limitations

- Seven Deflate64 archives were listable and hashable but not decompressible by
  installed readers, so their integrity is `not_tested`.
- Twenty-five external dates originally relied on filesystem timestamps; two
  additional ambiguous short-date parses were corrected to that same explicit
  fallback during integration.
- Security-related non-heading excerpts were omitted; marker presence remains.
- No historical behavior was executed, compared, restored, or migrated.
