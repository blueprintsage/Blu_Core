# Host Capability Truth and Surface Variability

status: review
owner: docs/domains/runtime
last_reviewed: 2026-08-08
assignment: BC-020

## Status vocabulary

- `documented_possible`: current first-party documentation describes support
  on some named/configured surface. It is not availability in this turn.
- `verified_available`: a current binding supplies a safe local probe or host
  receipt proving availability inside explicit scope and freshness bounds.
- `verified_unavailable`: a current probe or provider result proves
  unavailability inside explicit scope.
- `unknown`: evidence cannot decide.
- `not_applicable`: the capability does not belong to the named surface or
  boundary.

A documentation page alone cannot produce `verified_available`. A past success
does not prove present availability. Each current claim records `surface_id`,
provider, evidence class/ref, observation time, freshness, scope, limitations,
approval/side-effect/security classes, receipt requirement, and failure
behavior through `CapabilityRecord`.

## Evidence vocabulary

`repo_contract`, `official_documentation`, `local_probe`, `host_receipt`,
`project_owner_observation`, and `unverified` express different proof strength.
A generic repository obligation does not prove provider support. Official docs
can establish possibility or limitation. A local probe is bounded to the
observed surface. A host receipt is strongest only for the actual operation and
scope it records. Dad's observation remains labeled unless independently
verified. `unverified` leaves the status unknown.

## Surface and freshness model

`chatgpt` and `codex` are host-family IDs, not fixed toolsets. An actual binding
requires `surface_id`; version, client, OS, execution environment, sandbox,
approval, network, and workspace metadata are optional because unknown values
must not be manufactured.

Evidence freshness is `turn`, `host_session`, `timestamped`,
`configuration_version`, or `unknown`. Refresh is required at adapter startup,
new binding/session boundaries, before security- or side-effect-sensitive use,
after configuration/permission/tool changes, and after denial, outage, or stale
evidence. Cached records retain their evidence ref, observation time, freshness
scope, and invalidation conditions. There is no invented universal TTL.

Variability includes surface/version, sandbox, approvals, network, workspace
policy, connected integrations, user/organization permissions, plan, current
tool exposure, conversation context, and provider health.

## Distinctions the adapter preserves

- `host_attachment`, `filesystem_object`, and `external_source_object` are
  distinct. Chat attachments receive no invented filesystem path.
- Filesystem read, write, create, delete, rename, and execute are separate,
  with workspace/additional-root/host-defined/unrestricted/unknown scope.
- Web search, raw network, and integration calls are separate network classes.
- Git repository detection, read, write, branch, commit, push, remote, and PR
  capabilities are separate. Local commit never implies remote push.
- Deployment date context is not current-time evidence. Exact time requires a
  timestamp, offset/timezone, provider, observation time, and receipt.
- Natural-language reminder intent is not scheduling. Provider-backed create,
  update, cancel, recurrence, and schedule receipt are separate.
- Conversation/thread identity is not automatically security-grade
  `host_session` evidence or durable continuity.

Source/context retrieval maps to `IF-SOURCE-CONTEXT` and preserves identity,
provenance, covered scope, completeness, verification state, and limitations.
Partial retrieval remains partial; search metadata is not full source content.
