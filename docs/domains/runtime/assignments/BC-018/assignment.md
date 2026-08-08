# BC-018 — Successor Kernel Boundary Specification

status: review
owner: Codex
reviewer: Claude
project_lead: Blu
project_owner: Dad
domain: runtime
assignment_class: design
last_reviewed: 2026-08-08

## Authorization and identity

Dad and Blu authorized BC-018 in the design handoff supplied to Codex on
2026-08-08.

- Exact base: `a5e68b3189c60e2d5b8acbe8a212d69b720dec58`
- Starting branch: clean `main` at the exact base
- Work branch: `bc-018-successor-kernel-boundary-spec`
- Owner / Git steward: Codex
- Independent semantic reviewer: Claude
- Project Lead / integration reviewer: Blu
- Project Owner: Dad
- Global index: `docs/worklogs/assignments.md`

This is a design/specification assignment. It does not authorize implementation
of a successor Python runtime.

## Objective

Translate BC-010, BC-015, BC-016, and BC-017/BC-017-C1 evidence into the
smallest explicit successor control architecture that preserves useful Blu
behavior and law without porting historical modules one-for-one.

Centerline:

```text
PRESERVE THE BEHAVIOR AND LAW;
RECONSIDER THE COMPONENT GRAPH.
```

The design classifies behavior into `model_facing`, `deterministic_core`,
`host_service`, `host_adapter`, `continuity_provider`, `hybrid`, `deferred`, or
`reject`; defines generic boundaries for later BC-020 and BC-030 work; and
records uncertainty rather than inventing completeness.

## Required source order

1. `AGENTS.md` and `CODEX.md`.
2. `docs/dev/docs_index.md` and `docs/dev/assistant_coding_behavior.md`.
3. `docs/worklogs/assignments.md` and this packet.
4. Runtime domain index and continuity quartet.
5. Current architecture, source-role, authority, and assignment-record standards.
6. The immutable seven-file CTS source set.
7. BC-010 extracted contracts and unresolved register.
8. BC-015 viability evidence and audit.
9. BC-016 historical inventory as provenance/index only.
10. BC-017/BC-017-C1 archaeology, owner observations, corrections, and review limits.
11. Exact-base and clean-tree verification before editing.

## Authoritative inputs and evidence limits

- The current CTS remains authoritative and immutable.
- BC-010 is downstream extraction, not authority over CTS.
- BC-015 separates observation, declaration, host dependence, and successor
  proposal; no live-and-stable capability was proven.
- BC-016 is provenance/index evidence only and imports no behavioral authority.
- BC-017 is the primary historical recovery evidence, with no runtime telemetry,
  63 unreadable Deflate64 members, chronology gaps, and explicit separation of
  archive fact, owner observation, inference, and current truth.
- Faithfulness is unshipped sidecar design evidence. Only its positive-support
  candidate requirement may be evaluated.

## Approved boundaries

- CTS remains unchanged during design.
- Persona owns identity, presence, tone, relational behavior, and expressive
  adaptation; it is not a router.
- Operations remains primarily model-facing law. Deterministic support is
  limited to independently justified mechanics.
- OPSEC is a mandatory successor pre-ingress security restraint. This does not
  retroactively change current CTS history.
- Auth is a bounded contract over actions, resources, policy, and evidence; it
  is not cryptographic identity inferred from conversation.
- No mega-Exec, School Engine, legacy PASS, historical Faithfulness library, or
  module-for-module restoration is allowed.
- Modern PASS/SkillForge is an external optional provider workstream.
- Chat/Codex specifics remain BC-020; Local Mirror specifics remain BC-030.

## Component existence test

Every deterministic component must state its problem, evidence, deterministic
correctness benefit, inputs, outputs, state lifetime, failure behavior,
authority, host dependencies, exclusions, and why another component cannot
safely own the responsibility. A component justified only by an old name is
rejected. Removing a component must create a concrete correctness, security, or
parity failure.

## Required specification content

- behavior-placement matrix covering every behavior named in the authorization;
- normative control flow from raw host input through OPSEC, capability truth,
  Auth where needed, route/owner/ScopeLock, execution, source/artifact/completion
  validation, egress, and current-turn receipt;
- OPSEC and Auth boundaries without protected content;
- capability truth, time, reminder/scheduling, memory/continuity/persistence,
  teaching/classroom, Mood, Exec decomposition, source-grounding, ScopeLock,
  packet, error, model, adapter, continuity, SkillForge/PASS, and Alice boundaries;
- explicit state lifetimes;
- component-minimality review;
- dependency-ordered future implementation sequence;
- BC-020 and BC-030 readiness results;
- traceability and unresolved registers.

## Required deliverables

```text
docs/domains/runtime/assignments/BC-018/assignment.md
docs/domains/runtime/assignments/BC-018/handoff.md
docs/domains/runtime/assignments/BC-018/validation.md
docs/domains/runtime/assignments/BC-018/review.md
docs/architecture/successor_kernel.md
docs/architecture/successor_component_graph.md
docs/architecture/successor_boundaries.md
docs/architecture/successor_migration_sequence.md
contracts/successor/README.md
contracts/successor/component_registry.json
contracts/successor/behavior_placement.json
contracts/successor/interface_registry.json
contracts/successor/packet_registry.json
contracts/successor/error_model.json
contracts/successor/unresolved_register.json
contracts/successor/traceability.json
tools/validate_successor_kernel_spec.py
tests/successor_kernel/**
```

Update the allowed runtime decisions, worklog, next steps, global assignment
index, docs index, and canonical manifest.

## Generic interfaces required

Model execution; host capability provider; time provider; scheduling provider;
authorization evidence provider; continuity provider; source/context provider;
skill/context provider; and artifact provider/validator.

## Validation requirements

The design validator must check required files, JSON parsing, unique IDs,
evidence resolution, explicit ownership, exclusive deterministic ownership,
state lifetime, host dependencies, durable/scheduling provider dependencies,
OPSEC ordering, Persona non-routing, historical-container rejection, external
SkillForge, generic-only adapters and continuity, absence of runtime packages,
and golden checksums. Meaningful invariants require negative tests.

Run:

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
```

Also verify the canonical manifest, all golden checksums, protected paths,
current CTS unchanged, no runtime implementation, no historical module
restoration, and modern PASS/SkillForge untouched.

## Collision domain

```text
docs/domains/runtime/assignments/BC-018/**
docs/architecture/successor_*.md
contracts/successor/**
tools/validate_successor_kernel_spec.py
tests/successor_kernel/**
docs/domains/runtime/decisions.md
docs/domains/runtime/worklog.md
docs/domains/runtime/next_steps.md
docs/worklogs/assignments.md
docs/dev/docs_index.md
MANIFEST.sha256
```

No additional path is authorized.

## Protected and prohibited areas

Do not modify `kernel/golden/v0.22.0/**`, `contracts/runtime/**`,
`docs/sources/historical_archives/**`, prior assignment evidence, modern
PASS/SkillForge, `Blu_KB_Preview`, Local Mirror source, Alice source/reference
payloads, or historical kernels.

Do not implement Python runtime behavior, Auth, OPSEC, Time, reminders,
scheduling, MMU, persistence, Mood, Teaching, SkillForge/PASS, adapters, Local
Mirror, or begin BC-020/BC-030. Do not alter Blu identity or silently resolve all
28 current-source gaps.

## Commit and review protocol

Create one substantive specification commit, then one metadata-only commit that
records the substantive SHA on repository-standard metadata surfaces. Push the
branch normally. Do not merge. Status moves to `review`, not `done`. Claude
performs a separately authorized independent semantic review.

## Completion conditions

- all deliverables exist and validate;
- one understandable graph and unique ownership are explicit;
- model, core, host, adapter, and continuity authority are distinct;
- OPSEC and Auth boundaries are honest and secret-safe;
- capability, time, reminders, and persistence cannot be falsely claimed;
- Persona and teaching remain model-facing;
- Exec properties are recovered without Exec restoration;
- BC-020 and BC-030 receive usable generic boundaries;
- uncertainty remains in the unresolved register;
- protected paths are unchanged;
- work is committed, pushed, and handed off at `review`.

## Approved amendments

No amendments.
