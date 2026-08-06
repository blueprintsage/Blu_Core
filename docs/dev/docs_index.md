# Documentation Index

status: active
owner: docs/dev
last_reviewed: 2026-08-05

## Read first

```text
AGENTS.md
docs/dev/assistant_coding_behavior.md
docs/worklogs/assignments.md
```

## Architecture and authority

```text
docs/architecture/current_runtime.md
docs/architecture/migration_centerline.md
docs/sources/authority_map.md
config/source_authority.json
```

## Domains

| Domain | Path | Owns |
|---|---|---|
| Kernel | `docs/domains/kernel/` | golden source protection; Persona/Operations boundaries |
| Runtime | `docs/domains/runtime/` | Exec, ExecLib, Programs, routing, validation, receipts |
| Repository | `docs/domains/repository/` | live repo identity, indexed retrieval, source receipts |
| Continuity | `docs/domains/continuity/` | MMU, StateTree, memcaps, reminders, Local Mirror |
| Adapters | `docs/domains/adapters/` | Chat/Codex capability adapters |
| Build and release | `docs/domains/build-release/` | deterministic builds, parity, manifests, releases |

## Project-wide guides

```text
docs/dev/assistant_coding_behavior.md
docs/dev/doc_status_header_standard.md
docs/dev/bootstrap_commit_plan.md
```

## Extracted runtime contracts

```text
contracts/runtime/README.md
contracts/runtime/source_map.json
contracts/runtime/component_registry.json
contracts/runtime/route_registry.json
contracts/runtime/schemas/
contracts/runtime/parity_matrix.json
contracts/runtime/unresolved_register.json
tools/validate_runtime_contracts.py
tests/contracts/
```

## Assistant packets

```text
docs/assistants/index.md
docs/assistants/agents/index.md
```
