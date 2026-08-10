# BC-020 — Chat and Codex Capability Adapter Contracts

status: review
owner: Codex
reviewer: Claude
project_lead: Blu
project_owner: Dad
domain: runtime
last_reviewed: 2026-08-08

## Authorization and identity

Dad and Blu authorized this specification/contract assignment in the handoff
supplied to Codex on 2026-08-08. It authorizes host-adapter contracts,
documentation, validator tooling, tests, assignment records, and repository
metadata only. It does not authorize Chat or Codex adapter implementation, the
successor Python runtime, BC-030, Local Mirror, or PASS/SkillForge work.

- Exact base commit: `d4157e79fc7e2df6e1bd53b589cabfa19cd7238f`
- Starting branch: `main`
- Work branch: `bc-020-chat-codex-adapter-contracts`
- Global index row: `docs/worklogs/assignments.md` (`BC-020`)
- Assignment class: specification
- Semantic reviewer: Claude

## Objective

Specialize the approved BC-018 Generic Host Adapter Boundary for the `chatgpt`
and `codex` host families without changing the seven-component successor graph
or generic successor contracts. Define truthful capability discovery,
surface-specific evidence, receipts, errors, authorization transport,
host-session evidence, freshness, replay/correlation, and rollback-resistance
semantics. Resolve SUR-012 at the generic host-evidence contract level while
leaving SUR-011 policy unresolved.

## Required source order

1. `AGENTS.md` and `CODEX.md`.
2. `docs/dev/docs_index.md` and `docs/dev/assistant_coding_behavior.md`.
3. `docs/worklogs/assignments.md` and this approved packet.
4. Runtime domain index and continuity quartet.
5. BC-018/BC-018-C1 boundaries, packets, interfaces, unresolved register, and
   assignment records.
6. Current first-party OpenAI documentation for moving product claims.
7. Safe, bounded evidence from the actual Codex surface.
8. Exact-base, ancestry, status, and golden checksum verification.

## Governing invariants

```text
raw_host_event
-> Host Adapter
-> raw_host_input
-> Pre-ingress Security Restraint
```

The Host Adapter never constructs `TurnRequest`, chooses ordinary routes,
constructs `ScopeLock`, owns OPSEC/Auth policy, reasons as Persona, owns durable
continuity, or invents capability. Host approval and Blu authorization remain
separate. Product sign-in is not usable Auth evidence unless a supported host
interface supplies verifiable identity/role/credential evidence.

Capability status values are `documented_possible`, `verified_available`,
`verified_unavailable`, `unknown`, and `not_applicable`. Official documentation
alone cannot establish current-surface availability. Past success does not
prove current availability. Unknown is preferable to fabricated precision.

## Required contract outcomes

- Stable host-family IDs plus surface/configuration metadata.
- `CapabilityRecord`, `HostSessionEvidence`, `HostApprovalEvidence`,
  `HostActionReceipt`, artifact/delivery receipts, and normalized host errors.
- Chat and Codex capability matrices covering input, retrieval, actions, time,
  scheduling, continuity/session, security/Auth transport, and output.
- Explicit separation of attachments, filesystem objects, and external-source
  objects; web search, raw network, and integration calls; and local Git from
  remote/PR operations.
- Freshness, variability, runtime self-report, cache invalidation, provider
  receipt, failure, and side-effect honesty rules.
- SUR-012 disposition for host-session identity, request/result binding,
  freshness, expiry, replay, correlation, attempt-count integrity, and rollback
  resistance. Insufficient evidence must make protected cross-turn continuation
  unavailable; model memory and request-ref equality never qualify.
- SUR-011 remains the future security-policy decision for unrelated intervening
  turns and protected retry/lockout values.
- BC-030 remains separate and may use the generic continuity-provider boundary;
  host-session state never becomes durable persistence by implication.

## Evidence rules

Allowed evidence classes are `repo_contract`, `official_documentation`,
`local_probe`, `host_receipt`, `project_owner_observation`, and `unverified`.
Every current product claim records source/observation, scope, host surface,
freshness, limitations, what it supports, and what it does not prove. No live
web access is required by deterministic repository validation.

Safe probes may inspect OS/client metadata, workspace and Git state, sandbox,
approval/network policy, exposed tool metadata, and bounded command results.
They must not inspect credentials, tokens, cookies, private account state, or
unsupported internal endpoints, and must not escalate access merely to produce
stronger evidence.

## Allowed collision domain

```text
docs/domains/runtime/assignments/BC-020/**
docs/domains/runtime/adapters/**
adapters/**
tools/validate_host_adapter_contracts.py
tests/host_adapters/**
docs/domains/runtime/worklog.md
docs/domains/runtime/next_steps.md
docs/worklogs/assignments.md
docs/dev/docs_index.md
MANIFEST.sha256
```

## Protected and prohibited areas

Do not modify:

```text
kernel/golden/v0.22.0/**
contracts/runtime/**
contracts/successor/**
docs/architecture/successor_*.md
docs/sources/historical_archives/**
modern PASS/SkillForge material
Local Mirror source
```

Do not implement adapters, a runtime capability detector, Auth/session stores,
scheduling, MCP servers, plugins, apps, CLI wrappers, or any successor runtime.
Do not publish secrets, private session/account data, or protected OPSEC/Auth
content. If host specialization exposes a defect in the generic BC-018
interface, stop and request a corrective assignment rather than editing it.

## Required deliverables

- The four assignment records in this folder.
- Focused documentation under `docs/domains/runtime/adapters/`.
- Machine-readable common, Chat, Codex, and security contracts under
  `adapters/`, including evidence registers and capability/security matrices.
- `tools/validate_host_adapter_contracts.py` and meaningful negative tests in
  `tests/host_adapters/`.
- Runtime worklog/next-step, global assignment-index, docs-index, and canonical
  manifest updates.
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
```

Also verify the canonical manifest, all eight golden CTS checksums, exact-base
protected-path diffs, unchanged `contracts/successor`, absence of adapter/runtime
implementation, publication safety, and PASS/SkillForge isolation. Record actual
counts and results in `validation.md`.

## Completion conditions

Move BC-020 to `review`, not `done`, only after all acceptance questions are
answered by the contracts, required checks pass, records and continuity are
current, the substantive and metadata commits exist, the branch is pushed, and
the working tree is clean. Claude performs the independent semantic review.

## Approved amendments

No amendments.
