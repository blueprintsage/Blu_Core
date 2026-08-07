# Historical Archive Reconciliation Report

status: review
owner: docs/domains/runtime
last_reviewed: 2026-08-06
assignment: BC-016

## Result

The external discovery and live historical root agree on 247 imported source
records. The two additional live-only reconciliation entries are the Preview
and Release branch-root Markdown file sets required by BC-016; discovery had
intentionally omitted them because their normalized content matched recorded
archives.

The independently verified stable snapshot contains 279 files, including 244
nested ZIPs, and matches the live root on every relative path and file SHA-256.
No live-only file, snapshot-only file, or hash mismatch was found in that full
payload comparison. The outer snapshot container hash remains distinct from the
matching payload manifests.

## Reconciliation counts

- `matched_path_and_hash`: 496
- `matched_hash_different_path`: 2
- `live_directory_only`: 2
- `snapshot_only`: 0
- `inventory_only`: 0
- `hash_mismatch`: 0
- `unavailable_for_verification`: 0

## Exact duplicate groups

- `DUP-001`: `02cf65e61f836a28083a880e971c1d786020fe244e2f388270da950aa162b69b` — `Release/!Archives/v0.16.x/2026-05-07_1554_Blu_v0_16_0_DevBuild_r9_3_43_PATCHED.zip`, `Release/!Archives/v0.16.x/2026-05-07_1554_Blu_v0_16_0_DevBuild_r9_3_43_PATCHED_memory_mmu_statetree_commands_instructions_cleanup_datenorm.zip`
- `DUP-002`: `d48a2995487043919674ccfb0b28dc1ad8d785a1df2a69f1ad96075dc70ed258` — `Release/!Archives/v0.13.x/2026-04-07_1545_Blu_v0.13.2_Preview.zip`, `Release/!Archives/v0.13.x/2026-04-07_1600_Blu_v0.13.2_Baseline.zip`

Both differently named files in each group are retained. Two additional pairs
have identical normalized member-content manifests but different ZIP-file
hashes; they remain separate near-duplicate records rather than exact groups.

## Readability

7 archives use Deflate64 compression unsupported by installed
readers. Their central directories and archive-file hashes are available, but
member decompression and CRC validation remain `not_tested`. No archive is
classified corrupt or permission-blocked.

## Unresolved identity questions

- Filesystem modification timestamps remain non-authoritative date fallbacks.
- Matching member content does not establish identical container provenance or
  historical intent.
- Historical marker prominence does not establish successful behavior.
- The Preview and Release branch-root file sets match archive content, but each
  remains a separately recorded live organizational identity.

The uploaded snapshot appears complete relative to the scanned root because all
279 live files have one path-and-hash-identical snapshot member and there are no
extra snapshot files.
