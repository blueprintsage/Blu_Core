# Historical Archive Discovery Receipt

status: review
owner: docs/domains/runtime
last_reviewed: 2026-08-06
assignment: BC-016

## Sources consumed

- `dad_kernel_root`: scanned recursively.
- `external_discovery_output`: consumed
  `blu_historical_archive_inventory.json`,
  `blu_historical_archive_inventory.csv`,
  `blu_historical_archive_milestones.md`, and
  `blu_historical_archive_discovery_log.md`.
- `blu_kernel_snapshot`: stable `Kernel.zip` independently verified without
  committing the archive.

External discovery generated at: `2026-08-07T01:08:55.635385+00:00`.
BC-016 integration generated at: `2026-08-07T02:07:25.807078+00:00`.

## Methods

- Archive checksum: SHA-256 over archive-file bytes.
- Outer snapshot checksum: SHA-256 over `Kernel.zip` container bytes.
- Folder/file-set manifest: SHA-256 over sorted UTF-8 relative-path, NUL,
  lowercase file SHA-256, and LF records.
- Snapshot payload manifest: the same method over all 279 paths after removing
  the stable `Kernel/` wrapper.
- Structural metrics: preserved from the documented external discovery rules.

## Scope and exclusions

- Formats encountered: 244 nested `.zip` archive files plus Markdown source
  files and one outer ZIP snapshot.
- `.git`, dependency caches, build outputs, and temporary/cache directories
  were excluded by discovery.
- No neighboring source directories were scanned.
- No archive was copied into or extracted inside Blu_Core.
- Temporary extraction policy: isolated scratch extraction only if needed;
  none was used in discovery or BC-016.

## Counts

- Canonical inventory records: 249.
- Archive-file records: 244.
- Current branch file-set records: 3.
- Historical source-folder records: 2.
- Available/readable records: 242.
- Unsupported-format/not-tested records: 7.
- Corrupt or permission-blocked records: 0.
- Exact duplicate groups: 2.
- Milestones: 8.

## Integrity and limitations

- Live source manifest before integration: `38bc729f012243446ca29c3aed31802f2ec8d77473487cbd45a5bb710e3c88ff`.
- Live source manifest after integration: verified unchanged by the generator.
- Source files modified: no.
- Temporary extractions removed: yes; none created.
- Absolute source paths were converted to approved aliases plus relative paths.
- Two ambiguous short-date parses were corrected to filesystem-timestamp
  fallbacks; filesystem timestamps remain non-proof of build date.
- Marker presence and structural measurements are not behavioral proof.
