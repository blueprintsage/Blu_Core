# Documentation Index

status: active
owner: docs/dev
last_reviewed: 2026-08-12

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

BC-018-C1 adds the evidenced cross-turn authorization state correction under
`docs/domains/runtime/assignments/BC-018-C1/`. It preserves the seven-component,
eight-packet design and adds no runtime implementation.

## Chat and Codex host adapter contracts

```text
docs/domains/runtime/adapters/README.md
docs/domains/runtime/adapters/host_capability_truth.md
docs/domains/runtime/adapters/chat_adapter.md
docs/domains/runtime/adapters/codex_adapter.md
docs/domains/runtime/adapters/security_evidence.md
docs/domains/runtime/adapters/receipts_and_failures.md
adapters/README.md
adapters/common/
adapters/chat/
adapters/codex/
adapters/security/
```

BC-020 specializes only the Generic Host Adapter Boundary. These records
separate documentary possibility from current-surface availability, define
normalized capability/evidence/receipt/session/Auth-transport contracts, and
resolve SUR-012 at the generic host-evidence level. They are specifications,
not Chat/Codex adapters, provider implementations, or a successor runtime.

BC-020-C1 is the bounded scheduling-evidence correction under
`docs/domains/runtime/assignments/BC-020-C1/`. It leaves the exposed Codex
automation interface recorded while classifying the three operational
scheduling capabilities as unknown and requiring semantically relevant current
evidence for verified capability claims.

## Local Mirror continuity contracts

```text
docs/domains/continuity/local_mirror_continuity.md
docs/domains/continuity/assignments/BC-030/
continuity/README.md
continuity/schemas/
continuity/evidence_stages.json
continuity/lifecycle.json
continuity/rehydration.json
continuity/security_evidence.json
continuity/local_mirror_profile.json
continuity/sur007_disposition.json
```

BC-030 specializes the existing Generic Continuity Provider Boundary for
receipted `durable_external` continuity. It defines schemas and lifecycle only;
it does not implement Local Mirror, a Python runtime, an LM Studio adapter, or
provider-backed persistence. SUR-007 is resolved at the generic specification
level while SUR-011 remains unresolved.

## One-Blu portability and Python readiness

```text
docs/domains/runtime/one_blu_python_readiness.md
docs/domains/runtime/assignments/BC-040/
readiness/
```

BC-040 freezes the One-Blu deployment/canon map, provider and configuration
contracts, package layout, finite ordinary-turn slice, gap and blocker
dispositions, and parity/readiness gates. It also hardens BC-030 continuity
schemas and instance validation. Its final result was
`not_ready_for_python_phase1` because SUR-001's separately authorized minimum
OPSEC match/redaction contract was unavailable at BC-040 closure; BC-041 below
is the later bounded resolution. BC-040 introduced no production Blu runtime,
LM Studio client, Local Mirror provider, or Codex implementation.

## Minimum OPSEC contract

```text
contracts/security/opsec/README.md
contracts/security/opsec/minimum_contract.json
contracts/security/opsec/schemas/
docs/domains/runtime/assignments/BC-041/
docs/domains/runtime/assignments/BC-041-C1/
tools/validate_opsec_contracts.py
tests/security/
```

BC-041 defines the public deterministic mechanism for an externally supplied
protected policy without committing production values. It resolves SUR-001 at
the bounded minimum Phase 1 contract level and re-evaluates readiness to
`ready_for_python_phase1`. It remains specification/validation work only; the
runtime packet may be authored next but is not automatically authorized or
started.

BC-041-C1 closes the returned B-1/B-1'/B-1″ Unicode general-category `Cf`
insertion bypass with one deterministic `Cf`-removed candidate,
separator-tolerant phrase matching, and normalized provenance for removed outer
boundaries. Its explicit proof covers boundary, inside-token, mixed, outer-edge,
cross-code-point, repeated, and self-repetition classes without enumerating
placement combinations. Non-`Cf` default-ignorable/invisible characters and
general Unicode confusable/homoglyph substitution remain excluded, and
independent correction review is complete at `f0998f78aaada899a16d4413170ef3689f04fe28`
with `approve-with-notes` and zero blocking findings. BC-041 and BC-041-C1 are
closed. Technical readiness remains distinct from implementation authorization;
Python Runtime Phase 1 remains unstarted and unauthorized.

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
