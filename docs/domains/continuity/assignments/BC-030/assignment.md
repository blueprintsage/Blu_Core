# BC-030 — Local Mirror Continuity Schema and Lifecycle

status: review
owner: Codex
reviewer: Claude
project_lead: Blu
project_owner: Dad
domain: continuity
last_reviewed: 2026-08-10

## Authorization and identity

Dad and Blu authorized this successor specification assignment in the packet
supplied to Codex on 2026-08-10. It authorizes continuity contracts,
documentation, validator tooling, tests, assignment records, and repository
metadata only. It does not authorize a successor Python runtime, a Local Mirror
provider implementation, an LM Studio adapter, Chat live probing, SUR-011 policy,
or PASS/SkillForge work.

- Exact base commit: `a5f149355bd68b2aea1695e5f25ec60a2cb88b0c`
- Starting branch: `main`
- Work branch: `bc-030-local-mirror-continuity`
- Global index row: `docs/worklogs/assignments.md` (`BC-030`)
- Assignment class: successor specification
- Semantic reviewer: Claude

## Objective

Specify how a Local Mirror/MPLPB-backed provider may satisfy the approved
Generic Continuity Provider Boundary for `durable_external` continuity. Define
record, receipt, query, retrieval, availability, lifecycle, rehydration,
portability, corruption, and security-evidence contracts without implementing a
provider or changing the current CTS runtime.

## Required source order

1. `AGENTS.md` and `CODEX.md`.
2. `docs/dev/docs_index.md` and `docs/dev/assistant_coding_behavior.md`.
3. `docs/worklogs/assignments.md` and this approved packet.
4. Continuity domain index and continuity quartet.
5. BC-018/BC-018-C1 successor boundaries, packets, interfaces, and unresolved
   register.
6. BC-020/BC-020-C1 host-session and security-evidence contracts.
7. The supplied Local Mirror/MPLPB corpus, identified by the registered SHA-256
   `77745fa1fa726859edd0caf496241c2ba930e653a86a23ba0b2792ff9e8717f2`,
   as reference evidence only.
8. Exact-base, status, protected-path, and golden checksum verification.

## Governing invariants

- The successor graph remains seven components, eight packets, and nine
  interfaces. Continuity is not an eighth component.
- State lifetimes remain exactly `none`, `turn`, `host_session`, and
  `durable_external`; bare `session` is not a substrate.
- `host_session != durable_external`.
- A request, attempt, path, serialized object, conversation history, or model
  claim cannot prove persistence. Durable success requires provider evidence.
- The Generic Host Adapter owns host-substrate evidence. The Generic Continuity
  Provider owns durable-external evidence. Model context is turn-local input.
- `PendingAuthorizationState` remains a state record, not a service, component,
  or packet. Durable storage cannot make it trusted without the existing
  security evidence.
- SUR-011 remains unresolved.

## Required contract outcomes

- Stable logical record identity plus version-specific identity and provenance.
- Finite schemas for continuity records, receipts, queries, retrieval results,
  and provider availability.
- Deterministic create, retrieve, update, supersede, retire, historical recovery,
  validate, unavailable/failure, and integrity-failure behavior.
- Expected-version conflict handling and non-destructive history. BC-030 exposes
  no delete/destroy operation.
- Explicit distinction between source presence, discovery, retrieval, mutation
  request/attempt, durable mutation completion, validation, failure, and
  provider availability.
- Portable provider references that do not depend on absolute filesystem paths.
- Stateless restart/rehydration gates that require availability, retrieval,
  provider receipt, integrity validation, and bounded context staging.
- Separate ordinary-continuity and protected-authorization evidence profiles.
  The supplied Local Mirror reference must not be claimed to satisfy the latter.
- A future LM Studio-backed model remains a Model Execution Boundary concern and
  cannot change continuity semantics.

## Allowed collision domain

```text
continuity/**
docs/domains/continuity/assignments/BC-030/**
docs/domains/continuity/local_mirror_continuity.md
tools/validate_continuity_contracts.py
tests/continuity/**
docs/domains/continuity/decisions.md
docs/domains/continuity/worklog.md
docs/domains/continuity/failures.md
docs/domains/continuity/next_steps.md
docs/worklogs/assignments.md
docs/dev/docs_index.md
MANIFEST.sha256
```

## Protected and prohibited areas

Do not modify:

```text
kernel/golden/v0.22.0/**
contracts/runtime/**
contracts/successor/component_registry.json
contracts/successor/behavior_placement.json
contracts/successor/interface_registry.json
contracts/successor/packet_registry.json
contracts/successor/error_model.json
contracts/successor/unresolved_register.json
contracts/successor/traceability.json
docs/architecture/**
adapters/**
config/source_authority.json
Local Mirror source material
modern PASS/SkillForge material
```

Do not implement persistence, crawling, indexing, retrieval, a Python runtime,
an LM Studio adapter, a Chat/Codex adapter, a service, a daemon, a database, or
security policy. Do not resolve SUR-011 or claim provider availability from
configuration or reference source alone.

## Required deliverables

- The four assignment records in this folder.
- Human-readable specification at
  `docs/domains/continuity/local_mirror_continuity.md`.
- Machine-readable successor continuity contracts and JSON Schemas under
  `continuity/`.
- `tools/validate_continuity_contracts.py` and focused negative tests under
  `tests/continuity/`.
- Continuity decisions/worklog/failures/next-steps, global assignment index,
  docs index, and canonical manifest updates.
- One substantive specification commit and one metadata-only commit recording
  the substantive SHA, followed by a normal push of the work branch.

## Required checks

```text
git diff --check
python tools/validate_runtime_contracts.py
python -m unittest discover -s tests/contracts -p "test_*.py"
python tools/validate_viability_audit.py
python -m unittest discover -s tests/viability -p "test_*.py"
python tools/validate_historical_archive_inventory.py
python -m unittest discover -s tests/historical_archives -p "test_*.py"
python tools/validate_historical_behavioral_archaeology.py
python -m unittest discover -s tests/historical_archaeology -p "test_*.py"
python tools/validate_successor_kernel_spec.py
python -m unittest discover -s tests/successor_kernel -p "test_*.py"
python tools/validate_host_adapter_contracts.py
python -m unittest discover -s tests/host_adapters -p "test_*.py"
python tools/validate_continuity_contracts.py
python -m unittest discover -s tests/continuity -p "test_*.py"
```

Also verify the canonical manifest, all eight golden CTS checksums, exact-base
protected-path diffs, unchanged successor counts and existing registries,
absence of runtime/provider/LM Studio implementation, and PASS/SkillForge
isolation. Record actual results in `validation.md`.

## Completion conditions

Move BC-030 to `review`, not `done`, only after all deliverables exist, required
checks pass, the substantive and metadata commits exist, the branch is pushed,
and the working tree is clean. Claude performs the independent semantic review.
Dad retains merge authority; Blu retains integration/closure authorization.

## Approved amendments

No amendments.
