# Blu v0.22.0 Golden Runtime

status: active
owner: docs/domains/kernel
last_reviewed: 2026-08-05
immutable: true

This directory preserves the complete current Blu Markdown runtime from the CTS
archive.

## Rules

- Do not edit these files in place.
- Do not normalize line endings or metadata.
- Use them as the behavioral and authority baseline for migration.
- Put experiments and successor implementations outside `kernel/golden/`.
- Run `sha256sum -c SHA256SUMS` from this directory before and after work that
  depends on the golden runtime.

The source archive is retained beside the extracted files for provenance.
