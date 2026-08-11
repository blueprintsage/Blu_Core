# Continuity Failures

status: active
owner: docs/domains/continuity
last_reviewed: 2026-08-10

## Reference corpus is not a continuity receipt

- **Observed:** the supplied Local Mirror/MPLPB reference provides a bounded
  relative-link corpus, discovery/audit paths, metadata, current/retired status,
  retrieval, and structural validation.
- **Missing:** it does not provide a durable mutation API, atomic expected-version
  transition, crash-consistent receipt, current availability evidence,
  authentication/authorization enforcement, replay state, or rollback-resistant
  attempt state.
- **Prevention:** never promote corpus presence, crawl output, a path, or a
  serialized record to durable success. Require the BC-030 provider receipt and
  the appropriate ordinary or protected evidence profile.

## Checksum helper names must be discovered, not guessed

- **Observed:** `python tools/verify_checksums.py` was attempted during baseline
  setup but that helper does not exist in this repository.
- **Prevention:** verify the golden source directly against
  `kernel/golden/v0.22.0/SHA256SUMS` or use an actually present repository tool;
  record the exact command and result.

## Generic successor registries are a protected specialization boundary

- **Observed:** placing BC-030 files under `contracts/successor/continuity/`
  passed the focused continuity suite but failed the existing BC-020 validator,
  which protects the whole generic `contracts/successor/**` tree from later
  specialization changes.
- **Prevention:** keep provider-specific successor continuity contracts under
  the top-level `continuity/` namespace, analogous to `adapters/`, unless a
  separately authorized generic-boundary correction changes that protection.
  Always run the prior assignment regression validators before committing.
