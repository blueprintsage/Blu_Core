# BC-018 — Design Handoff

status: review
owner: Codex
last_reviewed: 2026-08-08

## Identity

- Assignment: BC-018 — Successor Kernel Boundary Specification
- Base commit: `a5e68b3189c60e2d5b8acbe8a212d69b720dec58`
- Work branch: `bc-018-successor-kernel-boundary-spec`
- Substantive work commit: `413574097f8426d10ce5cf284282ddab87f4bc93`
- Metadata commit: reported externally because a commit cannot contain its own SHA
- Push status: pending
- Working-tree status: pending final verification

## Result

Complete at specification level and ready for independent semantic review. No
successor runtime was implemented.

BC-018 proposes seven components/boundaries: four deterministic core
components, one model-facing boundary, one generic host-adapter boundary, and
one generic continuity-provider boundary. It classifies 37 behaviors and
defines eight packets, nine interfaces, six terminal/error statuses, four
state-lifetime classes plus stateless, fourteen traceable requirements, and ten
explicit unresolved items.

## Key dispositions

- Persona, ordinary conversation, and teaching remain model-facing.
- Operations, Auth, OPSEC, reminders, Mood, MMU, classroom behavior, source
  lookup, source grounding, and Faithfulness are explicit hybrid splits.
- OPSEC is pre-ingress; Auth evaluates bounded action/resource authorization
  against explicit evidence.
- Current time, scheduling, tools, artifacts, credentials, and durable storage
  remain host services.
- Mood and MMU do not earn dedicated successor components.
- Exec is decomposed; mega-Exec, School Engine, legacy PASS, and the historical
  Faithfulness library are rejected.
- Modern PASS/SkillForge is an optional external context provider.
- BC-020 and BC-030 are both `ready_for_spec`; neither was started.

## Files changed

```text
MANIFEST.sha256
contracts/successor/README.md
contracts/successor/behavior_placement.json
contracts/successor/component_registry.json
contracts/successor/error_model.json
contracts/successor/interface_registry.json
contracts/successor/packet_registry.json
contracts/successor/traceability.json
contracts/successor/unresolved_register.json
docs/architecture/successor_boundaries.md
docs/architecture/successor_component_graph.md
docs/architecture/successor_kernel.md
docs/architecture/successor_migration_sequence.md
docs/dev/docs_index.md
docs/domains/runtime/assignments/BC-018/assignment.md
docs/domains/runtime/assignments/BC-018/handoff.md
docs/domains/runtime/assignments/BC-018/review.md
docs/domains/runtime/assignments/BC-018/validation.md
docs/domains/runtime/decisions.md
docs/domains/runtime/next_steps.md
docs/domains/runtime/worklog.md
docs/worklogs/assignments.md
tests/successor_kernel/test_validate_successor_kernel_spec.py
tools/validate_successor_kernel_spec.py
```

## Unresolved items

`contracts/successor/unresolved_register.json` preserves security-authorized
OPSEC/Auth details, initial route catalog, semantic source verification,
capability freshness and host receipts, Local Mirror lifecycle, optional Mood
state, classroom state, and per-gap implementation decisions.

## Known risks

- Structured source policy does not make natural-language support verification
  deterministic.
- Adapter and continuity contracts do not prove a provider exists.
- Auth and OPSEC cannot be implemented safely until protected policy/evidence
  questions are resolved under separate authority.
- Component minimality and behavioral preservation require independent semantic
  review; green validation proves structural integrity only.

## Domain continuity updates

- Decisions: successor component graph and boundary decisions recorded.
- Worklog: BC-018 specification work and checks recorded.
- Failures: no new reusable failure added.
- Next steps: Claude semantic review; later BC-020/BC-030 remain unstarted.

## Reviewer focus

Component minimality, evidence traceability, false determinism, duplicate
ownership, source authority, OPSEC/Auth secrecy and ordering, host/persistence
truth, Exec decomposition, model-facing preservation, packet collapse, and
architecture creep.

## Pre-review contract correction — 2026-08-08

- Correction base: `ec4a3c14e6aedb7164fc500b0c9a31486bcd11e8`
- Correction substantive commit: pending metadata record
- Correction metadata commit: reported externally because a commit cannot
  contain its own SHA
- Push status: pending correction push

The correction makes Turn Controller the sole `TurnRequest` producer and
defines the bounded pre-ingress authorization loop:

```text
raw_host_event
-> Host Adapter raw_host_input
-> Security Restraint SecurityDecision
-> ASK / safe authorization_request_ref when evidence is absent
-> Validation and Egress / Host evidence collection
-> Authorization Evaluator AuthorizationResult
-> Security Restraint re-entry
-> only PASS reaches Turn Controller and TurnRequest normalization
```

Auth remains separate from OPSEC; OPSEC remains before ordinary routing. The
component count, behavior placement, packet count, host/continuity boundaries,
and migration architecture are otherwise unchanged.

Exact correction files are recorded by the metadata-only follow-up.
