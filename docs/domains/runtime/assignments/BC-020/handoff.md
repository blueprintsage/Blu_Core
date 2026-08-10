# BC-020 — Specification Handoff

status: review
owner: Codex
last_reviewed: 2026-08-08

## Identity

- Assignment: BC-020 — Chat and Codex Capability Adapter Contracts
- Base commit: `d4157e79fc7e2df6e1bd53b589cabfa19cd7238f`
- Work branch: `bc-020-chat-codex-adapter-contracts`
- Substantive work commit: `09c484418e51365cf9b156cf304eebae7fecde5d`
- Metadata commit: pending
- Push status: pending
- Working-tree status: substantive commit created; metadata commit and final clean check pending

## Result

Complete at specification level and ready for independent semantic review after
the substantive and metadata commits are pushed. No Chat/Codex adapter,
successor runtime, capability detector, Auth/session store, scheduler, plugin,
MCP server, Local Mirror, or PASS/SkillForge implementation was created.

BC-020 defines stable `chatgpt` and `codex` family IDs with required dynamic
surface identity, five capability statuses, six evidence classes, normalized
capability/surface/session/approval/receipt/error records, 52-row capability
matrices for each family, a 15-row host-security evidence matrix, and an
explicit SUR-012 disposition.

Dad's live Chat binding was not probed; documentary possibilities remain
documentary and current availability remains unknown. The observed Codex
desktop local Windows snapshot records only evidence from this turn/configuration.
It proves bounded workspace, shell, Git, web, time, tool-interface, and artifact
operations without generalizing them to Codex as a product.

SUR-012 is resolved at the generic host-evidence level. Both current surface
dispositions fail closed for protected cross-turn authorization: Chat remains
unknown pending future self-report, and observed Codex is verified unavailable
because no adapter-visible provider supplies replay/consumption or monotonic
rollback-resistant attempt state. SUR-011 remains unresolved policy input.

## Files changed

```text
MANIFEST.sha256
adapters/README.md
adapters/chat/adapter_contract.json
adapters/chat/capability_matrix.json
adapters/chat/evidence_register.json
adapters/codex/adapter_contract.json
adapters/codex/capability_matrix.json
adapters/codex/evidence_register.json
adapters/common/authorization_transport_contract.json
adapters/common/capability_contract.json
adapters/common/error_mapping.json
adapters/common/host_surface_contract.json
adapters/common/receipt_contract.json
adapters/common/session_evidence_contract.json
adapters/security/host_evidence_matrix.json
adapters/security/sur012_disposition.json
docs/dev/docs_index.md
docs/domains/runtime/adapters/README.md
docs/domains/runtime/adapters/chat_adapter.md
docs/domains/runtime/adapters/codex_adapter.md
docs/domains/runtime/adapters/host_capability_truth.md
docs/domains/runtime/adapters/receipts_and_failures.md
docs/domains/runtime/adapters/security_evidence.md
docs/domains/runtime/assignments/BC-020/assignment.md
docs/domains/runtime/assignments/BC-020/handoff.md
docs/domains/runtime/assignments/BC-020/review.md
docs/domains/runtime/assignments/BC-020/validation.md
docs/domains/runtime/next_steps.md
docs/domains/runtime/worklog.md
docs/worklogs/assignments.md
tests/host_adapters/test_validate_host_adapter_contracts.py
tools/validate_host_adapter_contracts.py
```

## Deliverables completed

- Assignment packet and four records.
- Six focused adapter-domain documents.
- Six common machine-readable contract files.
- Chat and Codex adapter contracts, evidence registers, and 52-row matrices.
- Fifteen-row security evidence matrix and explicit SUR-012 disposition.
- Offline validator and 25-test suite with meaningful negative cases.
- Docs index, runtime worklog/next-step, assignment index, and canonical
  manifest updates.
- All 18 acceptance questions from the authorized handoff are answered yes at
  specification level without forcing capability availability.

## Unresolved items

- Dad's actual Chat surface/tool exposure, current provider receipts, exact time
  provider, account/Auth evidence, and security-grade host-session mechanics
  remain unknown until a supported future runtime self-report.
- Codex client/surface version remains unknown because the safe version probe
  could not execute the packaged binary inside the bounded environment.
- Codex Git commit, push, and PR capability remain unknown in the substantive
  capability snapshot; fetch/pull and branch creation receipts do not imply them.
- The exposed Codex scheduling interface is current evidence of interface
  availability, but no task was created merely to prove it and the normalized
  success-receipt shape remains unknown until a real requested operation.
- No current host qualifies for security-grade protected cross-turn
  continuation under the complete BC-020 evidence gate.
- SUR-011 protected policy values and unrelated-intervening-turn disposition
  remain unresolved by design.

## Known risks

- Current product documentation and local probes are surface-scoped snapshots;
  they cannot establish permanent product-wide capability.
- Static validation cannot prove provider integrity, replay protection,
  rollback resistance, runtime security, or future adapter behavior.
- Reviewer should attack every `verified_available` scope and evidence link,
  especially exposed-tool metadata versus actual provider operation receipts.

## Domain continuity updates

- Worklog: BC-020 scope, evidence, dispositions, validation boundary, and next
  review action recorded.
- Failures: no collision-domain-authorized reusable failure entry; the
  assignment-specific version-probe and initial wording-check failures are in
  `validation.md`.
- Next steps: Claude review only; BC-030 remains ready for spec but unstarted;
  runtime implementation remains unauthorized.

## Reviewer focus

Capability overclaiming, surface conflation, session/Auth false assurance,
attempt-state rollback, replay/correlation gaps, approval/Auth separation,
receipt honesty, time/scheduling honesty, generic-contract leakage, and
accidental implementation.
