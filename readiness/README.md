# One-Blu Python Runtime Readiness Contracts

status: review
owner: docs/domains/runtime
last_reviewed: 2026-08-11
assignment: BC-040

## Purpose

This namespace freezes the deployment, canon, provider, configuration,
package-layout, executable-slice, gap, parity, and authorization-gate contracts
needed before a successor Python runtime may begin. It contains specifications,
schemas, fixtures, and evidence only. It contains no Blu runtime, LM Studio
client, Local Mirror provider, tool executor, daemon, UI, or CLI.

The current CTS source under `kernel/golden/v0.22.0/` remains the current Blu
runtime. Successor contracts preserve behavior and law while allowing a
different component graph. The fixed successor architecture remains exactly
seven components, eight packets, and nine interfaces.

## Records

- `one_blu_canon_manifest.json`: one canonical behavioral source mapped to
  ChatGPT and Python projections without host-specific forks.
- `deployment_targets.json`: required ChatGPT and Python/LM Studio targets plus
  optional Codex classification.
- `model_execution_provider_contract.json`: provider-neutral model execution
  semantics and Phase 1 capability policy.
- `lm_studio_official_evidence.json`: official LM Studio evidence used for
  protocol decisions.
- `schemas/runtime_config.schema.json`: portable, secret-free Phase 1
  configuration contract.
- `python_package_layout.json`: future `src/` layout contract only.
- `phase1_executable_slice.json`: finite ordinary-turn route and failure
  catalog.
- `implementation_gap_dispositions.json`: explicit dispositions for all 28
  current-source gaps.
- `implementation_blocker_dispositions.json`: Phase 1 gate classification for
  every successor item currently marked blocking for implementation.
- `custom_gpt_python_parity_matrix.json`: cross-deployment scenario contract.
- `python_phase1_readiness_checklist.json`: authorization result distinct from
  full successor feature completeness.
- `schema_runtime.json`: selected Python JSON Schema runtime and validation
  policy.

## Interpretation boundary

Configuration is not capability evidence. A visible or loaded model name is
not completed inference. A submitted request is not a completed response. A
model tool-call candidate is not authorization, host approval, attempted
execution, completion, or a verified receipt. Missing protected policy never
receives a permissive fallback.
