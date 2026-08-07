# BC-016 — Validation Record

status: review
owner: Codex
last_reviewed: 2026-08-06
python_version: 3.12.10

## Boundary

Passing checks prove source identity, structural consistency, path
sanitization, reference closure, and checksum integrity only. They do not prove
historical behavior, current-host parity, or successor implementation.

## Startup evidence

```text
git fetch origin --prune
git switch main
git pull --ff-only origin main
git status --short
git rev-parse HEAD
```

Results:

- Pre-closure main was clean and exactly
  `1f07333457b18895fbb04d5c776e3259d870f2f6`.
- BC-015 closure committed and pushed as
  `fdb6c7e150d3717172e08a1bc349a428187df45a`.
- BC-016 branch created from that exact closure commit.

## Source reconciliation receipts

```text
Outer snapshot SHA-256:
0195ab2623e2bdd9d2da5b8f18170f238bb4dbd5df489e543589de112eba6613

Outer snapshot size: 19221667 bytes
ZIP entries: 302
File entries: 279
Nested ZIP files: 244
Top-level root: Kernel
Live/snapshot matched payload files: 279/279
Live-only payload files: 0
Snapshot-only payload files: 0
Payload hash mismatches: 0
```

Live source manifest before and after integration:

```text
38bc729f012243446ca29c3aed31802f2ec8d77473487cbd45a5bb710e3c88ff
```

No source archive was modified and no temporary extraction was used.

## Inventory receipts

```text
Canonical inventory records: 249
Archive-file records: 244
Current branch file-set records: 3
Historical source-folder records: 2
Available/readable records: 242
Unsupported-format/not-tested records: 7
Exact shared-SHA duplicate groups: 2
Milestones: 8
Reconciliation matched_path_and_hash: 496
Reconciliation matched_hash_different_path: 2
Reconciliation live_directory_only: 2
Reconciliation hash_mismatch: 0
```

The eight milestones cover all ten requested categories because the v0.16 and
v0.21 records intentionally serve multiple related structural questions.

## Historical inventory validation

```text
python tools/validate_historical_archive_inventory.py
python -m unittest discover -s tests/historical_archives -p "test_*.py"
```

Results:

- Historical inventory validator: passed.
- Historical inventory tests: `Ran 12 tests`, `OK`.
- Negative cases cover duplicate ID, unknown branch, invalid SHA-256, absolute
  Windows path, absolute POSIX path, missing milestone ID, unequal duplicate
  hashes, CSV/JSON count mismatch, historical current-authority claim, marker
  behavior proof, and unverified independent snapshot claim.

## Full repository validation

```text
git status --short
git rev-parse HEAD
git diff --check
git diff --exit-code fdb6c7e150d3717172e08a1bc349a428187df45a -- \
  kernel/golden contracts/runtime docs/architecture \
  docs/domains/runtime/viability config
```

Results:

- Pre-commit HEAD remained the exact base.
- Status contained only BC-016 collision-domain changes.
- `git diff --check`: passed; Git emitted only expected working-copy
  LF-to-CRLF warnings.
- Protected-path diff: passed with no differences.

Golden and existing validator results:

```text
Golden CTS SHA-256 entries: 8/8 passed
python tools/validate_runtime_contracts.py: passed
python -m unittest discover -s tests/contracts -p "test_*.py": Ran 21, OK
python tools/validate_viability_audit.py: passed
python -m unittest discover -s tests/viability -p "test_*.py": Ran 9, OK
python tools/validate_historical_archive_inventory.py: passed
python -m unittest discover -s tests/historical_archives -p "test_*.py": Ran 12, OK
```

Repository-content checks:

- No ZIP, 7z, tar, tgz, or tar.gz file was added.
- No committed BC-016 file contains an external-source placeholder, drive path,
  home-directory path, or local-machine path.
- JSON inventory records: 249; CSV rows: 249; ID sets equal.
- All milestones reference real archive IDs and matching checksums.
- Both exact duplicate groups contain one shared canonical SHA-256.
- All reconciliation entries reference declared source identities.
- The stable snapshot remains separate from live-folder and payload-manifest
  identities.
- Source manifest before and after: identical.
- Temporary extraction directories: none created.

## Repository manifest

`MANIFEST.sha256` was regenerated from the complete normalized Git index after
all BC-016 files were staged, excluding the manifest itself. All 150 entries
were verified against their staged canonical bytes with zero missing entries or
hash mismatches.

## Known limitations

- Deflate64 member decompression is unavailable on this host for seven ZIPs;
  those records remain `not_tested`, not falsely classified corrupt.
- Filesystem timestamps are explicitly not build-date proof.
- Structural metrics and marker presence are not behavior proof.
