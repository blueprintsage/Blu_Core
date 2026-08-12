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

### Final closure disposition

- BC-040 is `done` after work integration, independent Claude review, and
  reviewed-state integration at
  `8801ae138deb0261deff47d02269c7a16773c892`.
- Claude's disposition is `approve-with-notes` with zero blocking findings.
- Assignment closure does not upgrade readiness. The final result remains
  `not_ready_for_python_phase1`; SUR-001 remains the sole actual Phase 1
  blocker, and `runtime_phase1_packet_may_be_authored_next` remains `false`.
- The next separately authorized assignment is `Protected Security Phase 1 —
  Minimum OPSEC Match and Redaction Contract`. It may amend the currently
  null-only protected-policy reference only under that separate protected
  authority.
- Python Runtime Phase 1 remains unauthorized. If SUR-001 closes and readiness
  is deterministically re-evaluated, the conditional coding packet remains
  `Python Runtime Phase 1 — Boot + Ordinary Turn + LM Studio Model Boundary`.
- Claude N-1 through N-10 remain nonblocking implementation and hardening
  inputs at their recorded targets. Closure does not convert them into BC-040
  blockers or begin their work.

## 2026-08-11 — BC-041 minimum OPSEC mechanism

- Recovered current law remains the CTS privacy/OPSEC boundary; BC-041 defines
  an explicitly authorized successor mechanism where current sources did not
  provide deterministic matcher values.
- Production policy values remain external. Canonical configuration stores only
  environment-variable names for a machine-local policy location and expected
  SHA-256 digest.
- A reference is not evidence of usability. The mandatory stages are reference
  configured, target located, payload loaded, schema validated, integrity
  validated, and policy usable. Any insufficient stage is terminal
  `UNAVAILABLE` without model invocation.
- The minimum matcher is Unicode NFKC plus bounded whitespace/separator
  normalization and token-bounded normalized phrase matching. It does not use a
  model, confidence, likely intent, Auth, or arbitrary semantic equivalence.
- Ingress protected matches map to `SecurityDecision=BLOCK`; nonmatches map to
  `PASS`. `ASK` remains in the exact three-value vocabulary but BC-041 invents
  no new authorization case.
- Candidate output is checked before print. Policy-authorized redaction must
  remove all matches, rescan cleanly, retain meaningful residual text, and emit
  no protected value in evidence or diagnostics; otherwise the output is fully
  blocked.
- SUR-001 is resolved only as
  `resolved_at_minimum_phase1_contract_level`. SUR-002, SUR-011, and SUR-012 are
  unchanged. The architecture remains 7 components, 8 packets, and 9
  interfaces.
- Contract-level readiness is `ready_for_python_phase1`, with no actual
  blockers and `runtime_phase1_packet_may_be_authored_next: true`. Runtime
  implementation remains unstarted and requires a separate Dad/Blu packet.

### Final BC-041 / BC-041-C1 closure disposition — 2026-08-12

- Current `main` integrates the correction lineage through
  `204a229e2c01b255f1a940129cb724fa33fb4755` at merge
  `131a527a8fef1f42df327443c9966c9e2f66f528`.
- Claude's final independent review at
  `f0998f78aaada899a16d4413170ef3689f04fe28` is
  `approve-with-notes` with zero blocking findings. The original BC-041
  `return-for-correction` review remains immutable history.
- B-1 is resolved through BC-041-C1; B-1' and B-1″ are resolved. SUR-001 remains
  `resolved_at_minimum_phase1_contract_level`.
- Technical readiness is `ready_for_python_phase1`; `actual_blockers` is empty;
  and the named runtime Phase 1 packet may be authored next.
- Claude N-1 and N-2 are future Python Runtime Phase 1 packet inputs. N-3 is
  pre-existing separator-set/word-character behavior, not a C1 defect.
- BC-041 and BC-041-C1 are `done`. Closure does not authorize implementation:
  `implementation_authorized` remains `false`, automatic start remains
  prohibited, and Python Runtime Phase 1 has not started.
