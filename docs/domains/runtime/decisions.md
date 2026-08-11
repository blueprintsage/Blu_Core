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

### Pre-review ownership and authorization clarification

- The Host Adapter translates `raw_host_event` to `raw_host_input` only.
- The Security Restraint converts `raw_host_input` into `SecurityDecision` and
  owns minimization of `allowed_input`.
- The Turn Controller is the sole producer of normalized `TurnRequest`, and it
  may begin only after `SecurityDecision PASS`.
- When pre-ingress authorization is required but absent, the Security Restraint
  returns a safe `ASK`; Validation and Egress / Host obtains explicit evidence;
  the separate Authorization Evaluator returns `AuthorizationResult`; and that
  result re-enters the Security Restraint for a new decision.
- Pre-ingress Auth does not use ordinary routing. Auth does not merge into
  OPSEC, and OPSEC remains before the Turn Controller.

### BC-018-C1 cross-turn security-state correction

- Pre-ingress authorization is explicitly cross-turn. Turn N ends with one
  safe `ASK` terminal packet; any evidence response arrives as a new host event
  in Turn N+1. Each host turn has exactly one `TerminalPacket`.
- The deterministic core retains only turn state. The lifetime set is `none`,
  `turn`, evidenced `host_session`, and receipted `durable_external`; bare
  `session` is not a persistence lifetime or security-state substrate.
- `PendingAuthorizationState` is a state record, not a component or packet.
  Security Restraint owns attempt permission and retry/expiry/replay policy;
  Authorization Evaluator owns evidence and result semantics; Host Adapter
  provides evidenced host-session storage and correlation when supported.
- Every pending authorization interaction has a policy-supplied finite positive
  attempt bound, expiry, request binding, replay rejection, and fail-closed
  exhaustion. Protected values remain unpublished and unresolved for a later
  security-authorized policy packet.
- `AuthorizationResult` validity is turn-bound, evidenced host-session-bound,
  or explicitly continuity-receipted; it is never merely session-valid.
- `ServiceExchange` distinguishes `ordinary_control` from
  `pre_ingress_authorization`; pre-ingress authority can reach only the bounded
  authorization-evidence interface and grants no ordinary service authority.
- Turn Controller remains turn-local. Supplied-time arithmetic is its
  deterministic current-turn utility; verified current time still requires a
  provider. Optional profile metadata is current-turn evidenced context owned
  behaviorally by Persona/model, not by Turn Controller.
- A proposed pre-ingress authorization interaction becomes resumable only after
  evidenced host-session binding succeeds. Success emits one terminal `ASK`;
  unavailable binding emits one terminal `UNAVAILABLE` instead, leaves the
  proposal inactive and non-correlatable, and requires no `ControlDecision`.
  Both terminal paths use the originating `SecurityDecision` authority and
  owner `security_restraint`; `SecurityDecision` remains limited to `PASS`,
  `BLOCK`, and `ASK`.

## 2026-08-11 — BC-040 One-Blu readiness boundary

- ChatGPT Custom GPT and Python/LM Studio are required deployments of one Blu
  canon. Codex is optional best effort and cannot drive the architecture.
- Persona and Operations Law remain exact model-facing authority. Historical
  Exec/ExecLib/Commands/Programs remain current CTS authority but do not become
  future canon without explicit behavioral traceability.
- LM Studio binds only beneath the existing Model Execution Boundary. Phase 1
  uses the official native v1 inventory/chat profile, non-streaming and
  `store=false`; configuration or a loaded name never proves inference.
- The planned first slice has one route, `ordinary_conversation`, and no tools,
  slash commands, protected action, durable continuity, scheduling, artifacts,
  Programs, MMU, Mood service, School Engine, or PASS/SkillForge.
- SUR-003 is resolved for that finite slice. SUR-010 is mapped across all 28
  current-source gaps. SUR-002, SUR-011, and SUR-012 block protected features
  only and fail closed.
- BC-040's readiness result is `not_ready_for_python_phase1`. SUR-001 is the
  only actual blocker because arbitrary natural-language ingress/egress cannot
  be proven safe from protected-source requests without the separately
  authorized minimum OPSEC match/redaction contract.
- No protected value is invented. The next safe assignment is the minimum
  protected security contract, not Python runtime implementation.
