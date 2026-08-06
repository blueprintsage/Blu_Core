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
