# BC-010 Implementation Handoff

status: review
owner: Codex
semantic_reviewer: Claude
project_lead: Blu
project_owner: Dad
last_reviewed: 2026-08-05

## Identity

- Assignment: BC-010 — Golden Runtime Contract Extraction
- Base commit: `7aed76e`
- Packet commit at checkout: `3c421914d2b449f63f9b7ba73e24cc59539c1c3b`
- Work commit: `40138b6e16f28c01904aae97158878468ee47ad0`
- Semantic review target: `40138b6e16f28c01904aae97158878468ee47ad0`
- Branch: `bc-010-runtime-contracts`
- Push status: not pushed

Claude's semantic review targets the work commit, not the later metadata-only
record commit.

## Files changed

The work commit contains 23 files in the authorized BC-010 collision domain:

- `contracts/runtime/**`
- `tools/validate_runtime_contracts.py`
- `tests/contracts/**`
- `docs/dev/docs_index.md`
- `docs/domains/runtime/worklog.md`
- `docs/domains/runtime/failures.md`
- `docs/domains/runtime/next_steps.md`
- `docs/worklogs/assignments.md`

No file under `kernel/golden/**` changed.

## Contracts created

- Runtime contract boundary and extraction rules
- Source provenance map
- Component, service, library, Program, command-owner, and runtime-owner registry
- Restraint, ingress, live command, fallback, deferred, and unavailable route registry
- JSON Schemas for task packet, ScopeLock, terminal packet, capability report,
  and current-turn execution receipt
- Behavioral parity matrix
- Unresolved declaration register
- Standard-library validator and validation fixtures/tests

Extraction totals:

- 41 registry components
- 6 live slash stems
- 69 source-map entries
- 22 unresolved items
- 12 parity requirements
- 34 parity cases

## Validation commands and results

```text
git status --short
git rev-parse HEAD
git merge-base --is-ancestor 7aed76e HEAD
python tools/validate_runtime_contracts.py
python -m unittest discover -s tests/contracts -p "test_*.py"
git diff --check
git diff --exit-code 7aed76e -- kernel/golden/v0.22.0
PowerShell Get-FileHash -Algorithm SHA256 comparison against kernel/golden/v0.22.0/SHA256SUMS
```

Results before the work commit:

- Base ancestry: passed
- Runtime contract validator: passed
- Unit tests: 4 passed
- Diff hygiene: passed after removing two extra end-of-file blank lines
- Golden diff against `7aed76e`: passed
- Golden checksum comparison: all eight manifest entries passed
- Protected behavior implementation: none added

`sha256sum` was unavailable on this Windows host. The PowerShell SHA-256
comparison is the assignment-authorized equivalent and checked all seven
Markdown files plus the source ZIP.

## Known unresolved items

The complete set is in `contracts/runtime/unresolved_register.json`. Review
focus should include:

- mandatory referenced-but-undefined owners and gates;
- the StateTree `ALPHA` versus `ACTIVE` conflict;
- `/memory` using `lane_class=workflow` while Exec omits that lane from its
  declared lane-class list;
- active component alias incompleteness;
- Memory Program's incomplete universal field declaration;
- intentionally permissive task-packet and capability-report schemas;
- current-turn receipt represented as an alias of the terminal packet;
- host capability, persistence, background execution, and artifact proof
  remaining conditional rather than assumed.

## Known risks

- Structural/schema validity does not prove behavioral parity.
- Registry presence does not prove executable implementation or host support.
- Persona and Operations remain authoritative model-facing sources and were not
  reduced into replacement behavioral schemas.
- The contracts deliberately do not resolve any unresolved register item.

## Recommended semantic-review focus

1. Compare every registry and route declaration to the seven golden files.
2. Verify missing definitions remain missing rather than inferred.
3. Verify repeated/conflicting StateTree declarations were preserved without a
   chosen status.
4. Verify route surface, one-owner rules, restraint ordering, and ScopeLock
   containment match CTS terminology.
5. Verify task/capability schema permissiveness accurately reflects absent field
   contracts.
6. Verify Persona and Operations were kept model-facing and non-routing.

## Working tree receipt

The working tree was clean immediately after the implementation commit. This
handoff and assignment-index update are the authorized metadata-only follow-up.
