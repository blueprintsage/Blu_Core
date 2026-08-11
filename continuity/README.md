# Successor Continuity Provider Contracts

status: review
owner: docs/domains/continuity
last_reviewed: 2026-08-10
assignment: BC-030

## Purpose

This namespace specializes the existing BC-018 Generic Continuity Provider
Boundary for Local Mirror/MPLPB-backed `durable_external` continuity. It defines
schemas and lifecycle rules only. It does not implement a provider, crawler,
index, Python runtime, model adapter, or persistence mechanism.

The successor architecture remains seven components, eight packets, and nine
interfaces. These records do not add a component or packet; requests and results
continue to cross `IF-CONTINUITY-PROVIDER` through `ServiceExchange`.

## Records

- `schemas/continuity_record.schema.json`: stable record lineage and version
  metadata.
- `schemas/continuity_receipt.schema.json`: finite provider outcome evidence.
- `schemas/continuity_query.schema.json`: bounded single-scope retrieval request.
- `schemas/continuity_retrieval_result.schema.json`: provenance-preserving result.
- `schemas/continuity_provider_availability.schema.json`: observed provider
  availability.
- `evidence_stages.json`: stages that must not be collapsed into durable success.
- `lifecycle.json`: create, update, supersede, retire, historical recovery,
  validation, conflict, failure, and corruption transitions.
- `rehydration.json`: stateless restart and bounded context-staging gates.
- `security_evidence.json`: ordinary versus protected-authorization evidence.
- `local_mirror_profile.json`: bounded mapping from the supplied reference
  corpus to the generic contract.
- `sur007_disposition.json`: BC-030 disposition of continuity lifecycle and
  provenance while preserving SUR-011.

## Interpretation rules

- A record identity or path is not a receipt.
- A request or attempt is not a completed durable operation.
- Only a continuity-provider receipt with `status=completed` may support a
  durable-success claim, and only for the operation, record, scope, version, and
  provider named by that receipt.
- `host_session` evidence is host-local and never becomes `durable_external`
  without an explicit continuity operation and receipt.
- Retrieved material becomes turn-local staged context after validation. The
  model does not remember or persist it.
- Absolute filesystem paths are provider configuration, not portable record
  references.
- Failed, unavailable, conflicting, or integrity-failed mutations make no state
  transition.
- The contract exposes no deletion or destruction operation.
- Protected authorization state requires stronger evidence than ordinary
  continuity. The supplied reference corpus does not prove that capability.
