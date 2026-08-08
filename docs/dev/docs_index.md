# Documentation Index

status: active
owner: docs/dev
last_reviewed: 2026-08-05

## Read first

```text
AGENTS.md
docs/dev/assistant_coding_behavior.md
docs/dev/domain_assignment_record_standard.md
docs/worklogs/assignments.md
```

## Architecture and authority

```text
docs/architecture/current_runtime.md
docs/sources/cts_source_roles.md
docs/architecture/migration_centerline.md
docs/sources/authority_map.md
config/source_authority.json
```

## Domains

| Domain | Path | Owns |
|---|---|---|
| Kernel | `docs/domains/kernel/` | golden source protection; CTS source roles; Persona/Operations boundaries |
| Runtime | `docs/domains/runtime/` | Exec, ExecLib, Programs, routing, validation, receipts |
| Repository | `docs/domains/repository/` | live repo identity, indexed retrieval, source receipts |
| Continuity | `docs/domains/continuity/` | MMU, StateTree, memcaps, reminders, Local Mirror |
| Adapters | `docs/domains/adapters/` | Chat/Codex capability adapters |
| Build and release | `docs/domains/build-release/` | deterministic builds, parity, manifests, releases |

Each domain stores cumulative continuity in its quartet and task-specific
evidence under:

```text
docs/domains/<domain>/assignments/<assignment-id>/
```

## Assignment records

```text
docs/dev/domain_assignment_record_standard.md
docs/dev/templates/domain_assignment/assignment.md
docs/dev/templates/domain_assignment/handoff.md
docs/dev/templates/domain_assignment/validation.md
docs/dev/templates/domain_assignment/review.md
docs/worklogs/assignments.md
```

`docs/worklogs/assignments.md` is the project-wide index. The approved packet,
handoff, validation evidence, and review live under the owning domain.

## Extracted runtime contracts

```text
contracts/runtime/README.md
contracts/runtime/source_map.json
contracts/runtime/component_registry.json
contracts/runtime/route_registry.json
contracts/runtime/parity_matrix.json
contracts/runtime/unresolved_register.json
contracts/runtime/schemas/
```

These files are downstream extractions of the CTS source set, not runtime
authority or Python implementation. The earlier 2026-08-05 AGENTS/docs-index
governance update was authorized by Dad and Blu. BC-010-C1 restores discovery
here without modifying `AGENTS.md`.

## Runtime viability audit

```text
docs/domains/runtime/viability/README.md
docs/domains/runtime/viability/evidence_register.json
docs/domains/runtime/viability/viability_matrix.json
docs/domains/runtime/viability/probe_catalog.md
docs/domains/runtime/viability/audit_report.md
```

BC-015 classifies current evidence separately from successor disposition. It is
an audit and inventory layer, not runtime implementation or behavioral proof.

## Successor kernel specification

```text
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
```

BC-018 specifies deterministic, model-facing, host, adapter, and continuity
boundaries. These records are design artifacts, not a Python runtime and not a
replacement for the current CTS.

## Historical archive source map

```text
docs/sources/historical_archives/README.md
docs/sources/historical_archives/kernel_archive_inventory.json
docs/sources/historical_archives/kernel_archive_inventory.csv
docs/sources/historical_archives/snapshot_receipt.json
docs/sources/historical_archives/reconciliation_report.md
docs/sources/historical_archives/milestone_recommendations.md
docs/sources/historical_archives/discovery_receipt.md
docs/sources/historical_archives/behavioral_archaeology/README.md
docs/sources/historical_archives/behavioral_archaeology/boundary_specimens.json
docs/sources/historical_archives/behavioral_archaeology/evidence_register.json
docs/sources/historical_archives/behavioral_archaeology/behavior_recovery_matrix.md
docs/sources/historical_archives/behavioral_archaeology/behavioral_evidence_report.md
docs/sources/historical_archives/behavioral_archaeology/transition_map.md
```

BC-016 integrates path-sanitized historical source identities and representative
milestones. These records are non-authoritative for the current runtime and do
not prove historical behavior. BC-017 adds sanitized boundary-first behavioral
archaeology and recovery dispositions without importing archive payloads or
changing current authority.

## Project-wide guides

```text
docs/dev/assistant_coding_behavior.md
docs/dev/doc_status_header_standard.md
docs/dev/domain_assignment_record_standard.md
docs/dev/bootstrap_commit_plan.md
```

## Assistant packets

```text
docs/assistants/index.md
docs/assistants/agents/index.md
```
