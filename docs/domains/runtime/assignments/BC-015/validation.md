# BC-015 — Validation Record

status: review
owner: Codex
last_reviewed: 2026-08-06
python_version: 3.12.10

## Boundary

Passing checks prove only structural coverage, reference integrity, checksum integrity, and recorded static constraints. They do not prove runtime execution, GPT-host behavior, behavioral parity, or successor implementation.

## Startup evidence

```text
git fetch origin --prune
git switch main
git pull --ff-only origin main
git status --short
git rev-parse HEAD
```

Results:

- `origin/main` already up to date.
- Initial working tree clean.
- HEAD exactly `4b51427b361283715a24110409e031e191b52452`.
- Created `bc-015-runtime-viability-audit`.
- Golden checksum verification before audit: 8/8 passed.

## Inventory and classification receipts

```text
Capabilities: 30
Component entries covered: 47/47
Normalized route-surface entries covered: 76/76
Parity requirements covered: 12/12
Unresolved entries covered: 28/28
Live probes executed: 0
Live probes cataloged: 24
```

Classification totals:

```text
live_and_stable=0
live_but_nondeterministic_or_host_dependent=3
declared_but_not_observably_functioning=8
conflicting_or_underspecified=12
explicitly_deferred_or_removed=5
new_successor_runtime_capability=2
```

## Required command results

### Git and protected paths

```text
git status --short
git rev-parse HEAD
git diff --check
git diff --exit-code 4b51427b361283715a24110409e031e191b52452 -- kernel/golden contracts/runtime docs/architecture config
```

Results:

- Pre-commit status contained only files inside the BC-015 collision domain.
- HEAD remained the exact base before the work commit.
- `git diff --check`: passed; only expected LF-to-CRLF working-copy warnings appeared.
- Protected-path diff: passed with no differences.

### Golden checksums

The requested GNU command was unavailable on this Windows host:

```text
sha256sum -c kernel/golden/v0.22.0/SHA256SUMS
```

The repository-approved PowerShell equivalent was run:

```powershell
Get-Content kernel/golden/v0.22.0/SHA256SUMS | ForEach-Object {
  # Compare each recorded hash with Get-FileHash -Algorithm SHA256.
}
```

Result: `GOLDEN_CHECKSUMS=8/8`.

### Existing runtime contracts

```text
python tools/validate_runtime_contracts.py
python -m unittest discover -s tests/contracts -p "test_*.py"
```

Results:

- Runtime contract validator: passed.
- Existing contract tests: `Ran 21 tests`, `OK`.

### BC-015 viability audit

```text
python tools/validate_viability_audit.py
python -m unittest discover -s tests/viability -p "test_*.py"
```

Results:

- Viability audit validator: passed.
- Viability tests: `Ran 9 tests`, `OK`.
- Negative coverage includes unknown classification, missing evidence, uncovered component, duplicate capability ID, invalid disposition, declaration-only `live_and_stable`, missing historical archive identity, and successor-as-golden projection.

### Manifest

```text
Regenerate MANIFEST.sha256 from tracked and BC-015 untracked non-ignored files.
Verify each recorded SHA-256 with Get-FileHash.
```

Results:

- Manifest entries: 137.
- Missing entries: 0.
- Hash mismatches: 0.
- `MANIFEST.sha256` excludes itself.

## Historical evidence limitation

The expected `2026-05-02_1333_Blu_v0.15.2_Baseline.zip` file was not present in the attachment bundle or repository. No checksum or member-path evidence is claimed. The audit uses `unavailable_evidence`, not `historical_baseline`, for this source.

## Final pre-commit result

All required checks passed after audit content was complete. Work and metadata commit identities are recorded in the handoff/index by the approved two-commit method.
