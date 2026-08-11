# Continuity Decisions

status: active
owner: docs/domains/continuity
last_reviewed: 2026-08-11

- Bootstrap authority is defined by `AGENTS.md` and
  `docs/sources/authority_map.md`.

## BC-030 — Durable continuity contracts

- Local Mirror may bind only behind the existing Generic Continuity Provider
  Boundary; it is not a successor component.
- Continuity lifetimes remain `none`, `turn`, `host_session`, and
  `durable_external`. Bare `session` is prohibited and
  `host_session != durable_external`.
- Durable success requires an operation-scoped provider receipt with
  `status=completed`. Source presence, discovery, paths, serialized objects,
  requests, attempts, model claims, and prompt context are insufficient.
- Stable `record_id` identifies a lineage; immutable `version_id` identifies an
  exact version. Updates preserve the lineage, supersession may create a linked
  successor lineage, and all mutations use expected-version conflict handling.
- Completed updates, supersessions, and retirement preserve history and
  provenance. BC-030 exposes no deletion or destruction operation.
- Retrieval is bounded to one explicit scope per query and preserves record
  identity, status, version, provider, integrity, and provenance.
- Stateless rehydration requires observed availability, a provider retrieval
  result and receipt, validation, and bounded context staging. The model does not
  remember or persist the material.
- Ordinary continuity evidence is not sufficient for protected authorization.
  The supplied Local Mirror reference does not prove atomic, replay-resistant,
  rollback-resistant security state.
- SUR-007 is resolved at the generic specification level by BC-030. SUR-011
  remains unresolved security-policy input.
- The canonical successor register retains SUR-007 as a historical source
  record with disposition `resolved_at_generic_continuity_contract_level` and
  `blocking_for_BC030=false`. The resolution does not select or implement a
  provider; provider technology, durability, security, backup/capacity, binding,
  and protected-authorization evidence remain future implementation inputs.
