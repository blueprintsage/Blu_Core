# Runtime Decisions

status: active
owner: docs/domains/runtime
last_reviewed: 2026-08-08

- Bootstrap authority is defined by `AGENTS.md` and
  `docs/sources/authority_map.md`.

## 2026-08-06 — Successor-runtime Auth and OPSEC route boundary

Approved for successor-runtime design; this is not a retroactive change to the
golden CTS source:

- Auth authorizes Admin-level users and owns the user-facing authentication
  workflow.
- Auth may use the declared `auth` lane.
- OPSEC protects against unauthorized ID challenge access and unauthorized
  copying, cloning, recreation, or disclosure of Blu's protected kernel/runtime
  sources.
- OPSEC is a mandatory pre-ingress security restraint, not an ordinary
  RuntimeGate lane.
- The current CTS source preserves OPSEC interception behavior but does not
  formally declare its lane or pre-ingress restraint contract.
- Generated BC-010 contracts must preserve that source gap rather than
  pretending the successor decision already exists in the golden kernel.

## 2026-08-08 — BC-018 successor kernel boundary

Approved specification decisions, pending independent semantic review:

- The proposed successor graph has four deterministic-core components:
  Pre-ingress Security Restraint, Authorization Evaluator, Turn Controller, and
  Validation and Egress.
- Model execution, host adaptation, and durable continuity remain separate
  boundaries; host services do not become kernel components.
- Persona, ordinary conversation, teaching judgment, and expressive adaptation
  remain model-facing. Operations Law remains primarily model-facing, with only
  independently provable invariants supported deterministically.
- OPSEC is mandatory before ordinary ingress. Auth is a separate bounded
  authorization contract over action, resource, policy, and explicit evidence.
- Exec is decomposed rather than restored. There is no Exec successor
  component, mega-Exec, School Engine, Mood service, MMU service, legacy PASS,
  or historical Faithfulness library.
- `source_only` factual output requires positive source support, while semantic
  claim/source matching remains model-dependent until real verification tooling
  proves otherwise.
- Future scheduling, current time, tools, artifacts, credentials, and durable
  storage require verified host/provider capabilities and receipts.
- BC-020 is `ready_for_spec` against the generic host-adapter boundary. BC-030
  is `ready_for_spec` against the generic continuity-provider boundary. Neither
  assignment is activated or implemented by BC-018.
