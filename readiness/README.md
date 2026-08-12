# One-Blu Python Runtime Readiness Contracts

status: done
owner: docs/domains/runtime
last_reviewed: 2026-08-11
assignment: BC-041-C1

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
- `../contracts/security/opsec/`: BC-041's public minimum OPSEC mechanism,
  protected-policy and result schemas, normalization/matching rules, redaction
  postconditions, and safe evidence contract.

## Interpretation boundary

Configuration is not capability evidence. A configured protected-policy
reference is not a located, loaded, schema-valid, integrity-valid, or usable
policy. A visible or loaded model name is
not completed inference. A submitted request is not a completed response. A
model tool-call candidate is not authorization, host approval, attempted
execution, completion, or a verified receipt. Missing or invalid protected
policy is terminal `UNAVAILABLE`, never `PASS`, and never reaches the model.

BC-041 resolves SUR-001 only at the minimum Phase 1 contract level. Production
policy values remain outside the repository, and deterministic normalized-
phrase matching does not claim arbitrary paraphrase or semantic-equivalence
detection. It also does not claim general Unicode confusable/homoglyph
substitution protection.

The `ready_for_python_phase1` result remains technical only. Its OPSEC gate invokes
the expanded B-1'/B-1â€³ proof: all six required `Cf` code points must pass
boundary, inside-token, mixed, leading-outer-edge, trailing-outer-edge, and
both-outer-edge ingress/egress probes. Cross-code-point, repeated, outer plus
interior, and unseparated self-repetition behavior must fail safely; ordinary
word adjacency without removed-`Cf` provenance must remain a nonmatch; and
removing either the mixed or outer-edge proof must make readiness validation
fail. Claude's independent correction review is complete at
`f0998f78aaada899a16d4413170ef3689f04fe28` with `approve-with-notes` and zero
blocking findings. Dad/Blu closure of BC-041 and BC-041-C1 is also complete.
These completed gates do not authorize implementation: `implementation_authorized`
remains `false`, automatic start remains prohibited, and Python Runtime Phase 1
has not started. The named runtime packet may be authored next only under a
separate Dad/Blu action.
