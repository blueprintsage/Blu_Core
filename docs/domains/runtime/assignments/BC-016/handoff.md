# BC-016 — Handoff

status: review
owner: Codex
last_reviewed: 2026-08-06

## Assignment identity

- Assignment: BC-016 — Historical Archive Inventory Integration
- Exact base: `fdb6c7e150d3717172e08a1bc349a428187df45a`
- Branch: `bc-016-historical-archive-inventory`
- Inventory work commit: `9f6d705723a3ee6d26e47b80c634bc3c58495c83`
- Metadata record commit: pending; exact SHA reported externally
- Semantic reviewer: Claude
- Push status: pending

## Result summary

BC-016 integrated the external discovery as a path-sanitized historical source
map without importing archive bytes or performing behavioral archaeology. The
canonical inventory contains 249 records: 244 archive files, three required
branch-root Markdown file sets, and two unique historical source folders.

The exact outer `Kernel.zip` was available and independently verified. Its
SHA-256, size, entry counts, branch layout, and top-level root match Dad and
Blu's receipt. All 279 snapshot payload files match the live historical root by
relative path and SHA-256.

Historical sources remain
`authority: non_authoritative_for_current_runtime`. The immutable current CTS
under `kernel/golden/v0.22.0/` remains the current runtime authority.

## Deliverables completed

- Sanitized JSON and CSV inventory.
- Separately verified outer-snapshot receipt.
- Live/discovery/snapshot reconciliation records and report.
- Eight representative milestone recommendations covering all requested
  structural categories, with several categories intentionally sharing a
  milestone.
- Sanitized discovery receipt and authority-boundary README.
- Standard-library validator and twelve tests, including all ten required
  negative cases.
- BC-016 assignment quartet, source registry update, runtime continuity, docs
  index, and repository manifest.

## Reconciliation summary

- `matched_path_and_hash`: 496
- `matched_hash_different_path`: 2
- `live_directory_only`: 2
- `snapshot_only`: 0
- `inventory_only`: 0
- `hash_mismatch`: 0
- `unavailable_for_verification`: 0

The two live-directory-only entries are the required Preview and Release
branch-root file sets. The external discovery deliberately omitted them because
their normalized content matched recorded archives. The stable snapshot itself
contains both and matches them.

## Known unresolved identities and risks

- Seven Deflate64 archives are `unsupported_format` with integrity
  `not_tested`; their archive hashes and central-directory paths remain
  available.
- Twenty-five dates use filesystem timestamp fallbacks. Two incorrect external
  short-date parses were rejected and converted to the same explicit fallback.
- Matching content manifests do not establish identical ZIP-container
  provenance or historical intent.
- Feature names, marker frequency, headings, and structural metrics do not prove
  behavior, stability, or suitability for recovery.
- BC-015's historically accurate unavailable-evidence record remains unchanged;
  later source availability does not retroactively alter it.

## Files changed

- `docs/sources/historical_archives/**`
- `docs/sources/external_inputs.md`
- `docs/domains/runtime/assignments/BC-016/**`
- `docs/domains/runtime/worklog.md`
- `docs/domains/runtime/failures.md`
- `docs/domains/runtime/next_steps.md`
- `docs/worklogs/assignments.md`
- `docs/dev/docs_index.md`
- `tools/validate_historical_archive_inventory.py`
- `tests/historical_archives/**`
- `MANIFEST.sha256`

## Working tree and push

- Pre-commit working tree: contains only BC-016 collision-domain changes.
- Inventory work commit: `9f6d705723a3ee6d26e47b80c634bc3c58495c83`; this is Claude's semantic-review target.
- Metadata record and push status: pending.
