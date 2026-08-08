# BC-018 — Independent Semantic Review

status: reviewed
review_state: complete
owner: Claude
last_reviewed: 2026-08-08
assignment: BC-018

## Review identity

- Review date: 2026-08-08
- Reviewer: Claude
- Review type: independent read-only semantic architecture review
- Review branch: `bc-018-semantic-review`
- Exact reviewed head: `34af2d6bad00430215bb7a7476f4eae582449ff2`
- Authorized base: `a5e68b3189c60e2d5b8acbe8a212d69b720dec58`
- Original substantive work: `413574097f8426d10ce5cf284282ddab87f4bc93`
- Original metadata: `ec4a3c14e6aedb7164fc500b0c9a31486bcd11e8`
- Correction substantive: `3384db41996d975d079d2d7f83a8e8fea9f4fce5`
- Corrected metadata / reviewed head: `34af2d6bad00430215bb7a7476f4eae582449ff2`
- Scope reviewed: the complete BC-018 result through the corrected head, not the
  initial work commit alone.
- Integration commit or merge identity: none

## Disposition

```text
return-for-correction
```

BC-018 is a strong, honest, largely minimal successor design. The centerline is
respected: behavior and law are preserved, the component graph is genuinely
reconsidered, no Exec successor exists, and false capability claims are
consistently refused. The disposition is `return-for-correction` for three
interlocking defects concentrated in one place — cross-turn state in the
security path — not for the architecture as a whole.

All three blocking findings are narrow and correctable within the existing
component count, packet count, and boundary set. None requires redesign.

## Blocking findings

### BF-1 — The corrected pre-ingress authorization loop has no consistent turn model

Normative sources: `docs/architecture/successor_kernel.md` control-flow steps
3-5; `docs/architecture/successor_boundaries.md` pre-ingress loop steps 1-7;
`contracts/successor/packet_registry.json` `pre_ingress_authorization_loop`.

The loop is: `ASK` -> Validation and Egress authorizes the safe pre-ingress
request -> Host Adapter obtains explicit evidence -> Authorization Evaluator
returns `AuthorizationResult` -> re-entry to Security Restraint -> new
`SecurityDecision`. Both possible readings of that sequence contradict a
declared invariant:

- **In-turn reading.** Validation and Egress authorizes the safe `ASK` as a
  terminal output, evidence is collected, re-entry produces `PASS`, the turn
  routes normally and produces a second terminal output. This violates the
  `TerminalPacket` invariant *"one terminal packet per host turn"*
  (`packet_registry.json`, `TerminalPacket.invariants`).
- **Cross-turn reading.** The `ASK` ends the host turn (`error_model.json`
  marks `ASK` `terminal: true`) and evidence arrives on a later turn. Nothing
  is declared to hold the outstanding `authorization_request_ref` between
  turns. `security_restraint.state_lifetime` is `["turn"]`
  (`component_registry.json`), yet `SecurityDecision.lifetime` states *"turn;
  re-entry may reference a prior terminal ASK"* and the packet carries
  `prior_decision_ref` and `authorization_request_ref`.

Concrete failure: a host returns evidence bound to a `request_ref` that no
component is authorized or scoped to recognize as outstanding. An
implementation then either fails closed permanently — making the entire
authorization path unusable — or invents session state inside the Security
Restraint, which the spec's own state-lifetime rule forbids without a
destination provider and receipt.

Required correction: state which reading is normative; if cross-turn, name the
owner, lifetime class, substrate, binding, and expiry of the pending pre-ingress
authorization request; if in-turn, reconcile it with the one-terminal-per-turn
invariant explicitly.

### BF-2 — The `session` state lifetime class has no provider, substrate, or evidence rule

Normative sources: `docs/architecture/successor_kernel.md` "State lifetime
classes"; `component_registry.json` (`turn_controller` and
`authorization_evaluator` both declare `session`);
`docs/architecture/successor_boundaries.md` "Authorization boundary".

The spec defines `session` as *"kernel-managed logical state scoped to the
active conversation"*, and separately rules that *"Moving state to a longer
lifetime is a state transition requiring the destination provider and receipt; a
Markdown declaration or model statement cannot perform the move."*

`host_session` has a declared holder (the Host Adapter). `durable_external` has
a declared holder and a mandatory receipt (the Continuity Provider). `session`
has neither. The transition rule is therefore unsatisfiable for the one class
the deterministic core actually claims, while two core components declare it and
Auth's session-scoped authorization depends on it.

This is the same false-determinism failure the design correctly refuses
elsewhere, applied one lifetime class lower. Current evidence is explicit that a
turn-invoked hosted runtime cannot claim cross-turn continuation:
`contracts/runtime/parity_matrix.json` PARITY-012 — *"cannot claim a daemon,
background task, self-wake, hidden continuation, cross-turn cached live time, or
unproven persistence."* BC-015 proved no live-and-stable capability, and BC-017
recorded persistence as unproven.

Concrete failure: an implementation reports a session-scoped authorization
`PASS` as still valid on a later turn with no `host_session` binding and no
continuity receipt — a fabricated security state, created exactly the way
durable persistence is forbidden to be created.

Required correction: either give `session` a declared provider and evidence
requirement (most plausibly binding it to `host_session` or to a continuity
receipt), or remove `session` from the deterministic core and require Auth
session effects to be carried by an evidenced lifetime.

### BF-3 — The "bounded" pre-ingress authorization loop is unbounded in repetition

Normative sources: `packet_registry.json` `pre_ingress_authorization_loop`;
`docs/architecture/successor_boundaries.md` pre-ingress loop;
`contracts/successor/unresolved_register.json`.

The loop is bounded in *scope* — it never enters ordinary routing, and only
`SecurityDecision PASS` reaches the Turn Controller. That property is correct
and I confirm it holds. It is not bounded in *repetition*. No attempt limit,
lockout, backoff, request-ref expiry, or replay rule is specified, and no
component is named as the owner of attempt state.

The approved OPSEC decision (`docs/domains/runtime/decisions.md`, 2026-08-06)
states OPSEC protects against *unauthorized ID challenge access*. An
unbounded `ASK` -> evidence -> re-entry cycle against an identity challenge is
the corresponding attack surface, and it is reachable pre-`PASS`, before any
ordinary control applies.

This is not recorded as a deliberate deferral. `SUR-001` covers OPSEC match and
redaction policy; `SUR-002` covers evidence types and assurance levels. Neither
covers repetition bounding or its owner. It is therefore an unregistered
unknown, not an honestly deferred one.

Required correction: name the owner of pre-ingress authorization attempt state
and its lifetime class (this interacts with BF-1 and BF-2), or register the
question explicitly in the unresolved register as blocking for implementation
under the security-authorized packet.

## Non-blocking notes

- **N1 — Ownership coverage gaps not caught by the validator.**
  `behavior_placement.json` assigns two responsibilities to `turn_controller`
  that do not appear in `component_registry.json` `turn_controller.owns`:
  BEH-015 time arithmetic (`"turn_controller service policy"`) and BEH-018
  optional lightweight session profile metadata. The validator enforces
  *no duplicate* deterministic ownership but not ownership *coverage*, so both
  pass green. For BEH-015 the spec simultaneously calls time arithmetic
  `deterministic_core` and says the model "may reason over supplied values" —
  pick one. For BEH-018, if optional profile metadata is retained it should ride
  on `TurnRequest`/session context rather than being owned by the routing
  component, given the stated rule that it "must not control cognition,
  routing, or identity".

- **N2 — `deterministic_owner` is used for non-deterministic boundaries.**
  BEH-020, BEH-035, BEH-036, and BEH-037 populate `deterministic_owner` with
  `continuity_provider_boundary` or `host_adapter_boundary`. Terminology only;
  no authority is misassigned, but it weakens the field's meaning.

- **N3 — `ValidationResult` is the weakest retained packet.** It is the only
  packet whose declared producer and consumer are the same component
  (`validation_egress` -> `"validation_egress terminal assembly"`). It never
  crosses a boundary, so by BC-018's own collapse rationale — the one used to
  embed `ExecutionReceipt` in `TerminalPacket` rather than keep a ninth packet —
  it is a candidate for embedding via `TerminalPacket.validation_ref`. If it is
  retained, justify it explicitly as a required audit record rather than a
  control contract.

- **N4 — `receipt_backed_diagnostics` is mild creep in the minimal core.** It
  traces legitimately to EVID-BC010-UR005, but a diagnostic view has not earned
  a place in the first successor core. Consider deferring it out of
  `validation_egress.owns` until receipts exist to view.

- **N5 — `ServiceExchange.authority_ref` is a permissive union guarded only in
  prose.** `authority_ref` may be a `ControlDecision` *or* a safe pre-ingress
  `authorization_request_ref`, and the restriction to the bounded evidence
  exchange lives in an invariant sentence rather than a typed field. Make the
  authority class explicit and machine-checkable so no implementation accepts a
  pre-`PASS` exchange for an ordinary service.

- **N6 — The current mandatory restraint chain is absent from the Exec
  decomposition table.** PARITY-004 requires AntiDrift first and the Operations
  restraint second, both returning terminal-valid PERMIT packets before
  `RuntimeGate.Ingress` may begin, and PARITY-001 makes ordinary-conversation
  admission conditional on both. The successor decomposition table
  (`successor_component_graph.md`) names "pre-ingress security scheduling" and
  "Operations semantic anti-drift" but never states that the two-restraint
  pre-execution gate is deliberately dissolved into model-facing judgment plus
  egress validation. That is a defensible decision, but §17 asks for a complete
  decomposition; state the disposition of the restraint chain explicitly so the
  loss of a pre-execution gate is a recorded decision rather than an omission.

- **N7 — Ordinary conversation should get an explicit conversational profile.**
  `TurnRequest` requires `task_intent` and `requested_deliverable` on every
  turn, and a ScopeLock is frozen for every turn including warm chat. The
  turn-scoped nature of ScopeLock and the `reduced_candidate` mechanism in
  `ValidationResult` keep this from being a real defect — this is close to the
  current PARITY-005 REDUCE behavior. Still, name an explicit
  ordinary-conversation intent with a null deliverable and a permissive
  conversational ScopeLock profile, so warmth, asides, and follow-through are
  handled by `reduced_candidate` rather than treated as scope escape.

- **N8 — The state-lifetime taxonomy carries no traceability requirement.** No
  SKR item covers the five-class lifetime model or the introduction of
  `host_session`. Given BF-2, this taxonomy deserves its own traced requirement.

- **N9 — `validation.md` retains a pre-correction result line** ("successor
  specification tests: Ran 21, OK") above the correction block that records 25.
  Both are historically accurate as written; a one-line note that the first
  block predates the correction would prevent misreading.

### Preserved unresolved declarations

`contracts/successor/unresolved_register.json` is preserved as authored. SUR-001
through SUR-010 are genuine unknowns, correctly left open rather than solved by
assertion. BF-3 identifies one unknown that is missing from that register.

## Answers to Q1-Q12

### Q1 — Do the four deterministic core components form a genuinely minimal control plane, or has mega-Exec been redistributed/renamed?

Genuinely minimal, and not a rename. The four components map onto boundaries
that already exist as *distinct* declarations in the current CTS contracts —
the pre-ingress restraint position, `RuntimeGate.Ingress` (route resolver, lane
lock, owner lock, ScopeLock construction), and `RuntimeGate.Egress` (terminal
validation, containment, print authorization) — plus a separated Authorization
Evaluator. Mega-Exec's actual defects were the hosted scheduler role, the
subcomponent sprawl (`Exec.BootScheduler`, `Exec.Scheduler`, the spine-trace
owner), and the catch-all dispatch of Programs and Libs. None of those returns.
There is no scheduler component, no Program framework, no Lib registry, no
catch-all owner, and no component named Exec. The minimality argument in
`successor_kernel.md` is sound: each merge candidate would collapse either
policy authority into protected state, or route authorization into
self-certifying egress.

The one preservation delta is recorded in N6: the two-restraint pre-execution
gate has no deterministic successor.

### Q2 — Is Turn Controller internally coherent, or does it combine responsibilities requiring separate authority?

Coherent. All seven responsibilities answer one question — *what is this turn
permitted to do* — under one lifetime, one failure boundary, and one authority
class. `capability_report_validation` must precede dispatch, so it cannot move
to Validation and Egress. `ingress_normalization` must follow `PASS` and
precede routing, so it belongs here and nowhere else. Testing it as one control
function is reasonable: given `SecurityDecision PASS` plus capability records,
it emits exactly one `ControlDecision` or a typed failure.

I would not require decomposition. The list is long but not conflicted. The one
genuine problem in this component is its `session` lifetime claim (BF-2), not
its responsibility set.

### Q3 — Is Validation and Egress internally coherent, or is it becoming a catch-all validation subsystem?

Coherent today, with a named creep risk. The grouping is justified by one
property: independent final proof must not be owned by the component that
authorized the route. It validates only artifacts produced elsewhere
(`SecurityDecision`, `ControlDecision`, candidate, receipts) and self-certifies
nothing.

The catch-all risk is real and partly materialized: `receipt_backed_diagnostics`
is already an eighth responsibility that is not proof (N4). The spec's own
guard — *"Extra gates are not permitted unless a later assignment demonstrates a
distinct responsibility and concrete failure caused by their absence"* — is the
right control and should be applied to this component's own growth, not only to
new gates. Future semantic source verification (SUR-004) must arrive as a
separate provider *consumed by* Validation and Egress, never as a responsibility
absorbed into it. State that explicitly.

### Q4 — Does the corrected OPSEC/Auth loop preserve mandatory pre-ingress security without creating an authority cycle or routing bypass?

Partly. The security properties hold; the turn and state model does not.

Confirmed sound:
- No authority cycle. The declared dependency graph is acyclic: adapter <- auth
  <- security <- {controller, egress}. `security_restraint` does not depend on
  `validation_egress`; the `ASK` edge is expressed as egress depending on the
  Security Restraint's output.
- No routing bypass. `ControlDecision` requires the invariant
  `"SecurityDecision PASS exists"`; `TurnRequest` requires
  `security_decision_ref`; ingress ownership in both `packet_registry.json` and
  `interface_registry.json` sets `ordinary_routing_precondition` to
  `SecurityDecision status=PASS`; the validator enforces all of these with
  negative tests.
- No self-certification. Pre-ingress terminal output uses the `SecurityDecision`
  as `authority_ref` and `security_restraint` as owner, validated by a component
  that produced neither.
- Auth and OPSEC remain separate owners, enforced structurally
  (`auth_loop.authorization_owner != auth_loop.security_owner`), and
  conversational identity inference is explicitly excluded.
- Auth is correctly kept off the ordinary route: the validator rejects
  `authorization_evaluator` appearing in `turn_controller.dependencies`.

Not sound: the loop's turn model and its pending state (BF-1), the lifetime it
implicitly depends on (BF-2), and its lack of repetition bounding (BF-3).

### Q5 — Does the model retain enough responsibility for Blu to remain Blu?

Yes. This is the strongest part of BC-018. Persona, ordinary conversation,
warmth and presence, pedagogy, explanation, contextual interpretation,
natural-language generation, Operations semantic judgment where proof is
unavailable, and model-dependent source interpretation are all explicitly
model-facing. The deterministic core constrains and validates; it does not
generate. `behavior_placement.json` BEH-001 states the principle directly —
"deterministic code constrains but does not replace Blu" — and BEH-002 keeps
Persona non-routing, which the validator enforces.

The ordinary-turn cost is proportionate: one mandatory OPSEC evaluation and five
packets, with no Auth, no host call, no persistence, no capability proof for
unused capabilities, no source validation outside source-bound lanes, and no
service packet when no service is used. `error_model.json` states the necessary
invariant explicitly: *"Ordinary conversation does not fail closed for an unused
optional capability."*

Two residual over-control risks, both notes rather than defects: mandatory
`allowed_input` minimization sits between the user and Blu on every turn
(mitigated by the rule that redaction requires explicit policy authorization),
and every turn is framed as task plus deliverable plus ScopeLock (N7).

### Q6 — Does ServiceExchange function as a healthy generic envelope, or is it semantically overloaded?

Healthy, with one exception. The generic envelope works because the
provider-specific semantics live in the interfaces and payloads, not in the
packet: nine interfaces each declare their own required behavior, failure
behavior, and receipt obligations, and the envelope carries only what is common
— direction, service, operation, authority, status, payload, limitations,
receipt, failure reason. That is the right level of genericity, and it avoids
inventing a packet per service type.

The exception is authority, not payload semantics: the pre-ingress
authorization-evidence exchange is the only `ServiceExchange` that occurs before
`SecurityDecision PASS` and outside `ControlDecision` authority. That is a
different authority class riding in the same envelope, guarded only by prose
(N5). Lifetime differences (continuity's `durable_external` versus turn-scoped
exchanges) are handled correctly by receipts and do not require separate
top-level contracts.

### Q7 — Are Time and Reminders represented honestly?

Yes, and cleanly. The separations are correct and consistently maintained: time
arithmetic over supplied values (deterministic) versus verified current time
(host service with timestamp, timezone, verification method, scope, receipt);
reminder interpretation (model) versus real scheduling (provider with schedule
ID, normalized schedule, operation, receipt). `IF-TIME-PROVIDER` explicitly
states it must "never perform scheduling by implication." The rule *"prompt text
is never a wake mechanism"* is stated in the boundaries document, mirrored in
BEH-017's rationale, and enforced by a validator check requiring a
`scheduling_provider` dependency for both reminders and future scheduling. This
correctly preserves PARITY-012.

The only wrinkle is the time-arithmetic ownership ambiguity in N1.

### Q8 — Are MMU, continuity, and persistence separated honestly?

Yes for the durable boundary; no for the intermediate one. The six-way
separation — memory organization, retrieval, context staging, session state,
durable persistence, continuity provider — is the right decomposition, and no
MMU component survives merely because historical MMU existed. Promotion to
`durable_external` correctly requires a continuity request, a version/conflict
result, and a receipt, and the validator enforces that any durable-lifetime
component depends on the continuity provider.

The honesty breaks one level down, at `session` (BF-2). Durable persistence is
guarded; cross-turn kernel state is asserted.

The generic continuity boundary itself is sufficient for BC-030.

### Q9 — Is the source-grounding design useful without claiming deterministic semantic entailment?

Yes. This is handled with unusual discipline. The five source modes are
meaningful and distinct; the four result classes (unsupported, contradiction,
outside scope, unverifiable) are genuinely different control outcomes, not
synonyms; `source_only` correctly requires positive support rather than absence
of contradiction. Critically, the design states its own limit plainly in three
places: natural-language claim extraction, entailment, and source mapping remain
model-dependent, and *"A JSON claim list authored solely from model confidence
is not proof."*

Validation and Egress can truthfully enforce the mechanical portion — declared
mode, declared scope, presence and provenance of evidence references, receipt
sufficiency, and the distinction between result classes — while leaving semantic
support mapping to the model. FaithfulnessLib does not return: BEH-027 recovers
the principle and rejects the library name and object model, and SUR-004 keeps
the verifier question honestly open.

### Q10 — Are BC-020 and BC-030 genuinely ready to receive separate specification packets?

**BC-020: yes.** The generic target is real and specific — `CapabilityReport`
with `verification_method`, `provider`, `scope`, `limitations`, freshness or
turn scope, `receipt`, and `failure_reason`; `ServiceExchange`; authorized
`TerminalPacket` delivery; nine interfaces; error translation; and an explicit
prohibition on host assumptions in the core, enforced by validator checks on
`host_specific` and `provider_binding`. The adapter's exclusions are stated
correctly and now include `TurnRequest_construction` and
`ingress_task_normalization`. `SUR-002`, `SUR-005`, and `SUR-006` are correctly
framed as BC-020 *inputs*. One caveat: BF-1 and BF-3 land inside BC-020's
identity-evidence surface, so the authorization-evidence portion of the adapter
spec should not be drafted until the pre-ingress loop's turn and state model is
fixed. The rest of BC-020 is unblocked.

**BC-030: yes, without caveat.** The continuity boundary defines namespace and
scope, read and write, version, expected version, conflict result, provenance,
lifetime, receipt, and unavailable behavior, and explicitly refuses Local Mirror
storage decisions. `does_not_own` correctly excludes memory interpretation,
context selection, route policy, storage design, and silent persistence claims.
SUR-007 is the right BC-030 input.

### Q11 — Is there any component, packet, interface, or responsibility you would remove before implementation?

Components: none. All seven earn their existence; each passes the removal test
with a concrete failure.

Interfaces: none. Nine is not excessive given that each declares distinct
required behavior and receipt semantics, and none is host-specific.

Packets: one candidate — `ValidationResult` (N3), the only packet that never
crosses a component boundary.

Responsibilities: `receipt_backed_diagnostics` (N4). Also resolve rather than
retain the two unowned/mis-owned responsibilities in N1.

Nothing else. The eight packets are otherwise individually justified: each
carries a distinct authority reference and a distinct control transition, and
the collapses that were made (IngressPacket + TaskPacket, ScopeLock +
RouteDecision, ServiceRequest + ServiceResult, embedded SourceScope, embedded
ExecutionReceipt) are all defensible on control semantics rather than aesthetics.

### Q12 — Is there any missing boundary whose absence would create a concrete correctness/security/parity failure?

Yes — one, and it is the substance of BF-1 through BF-3: **there is no owner for
security-relevant state that must survive between turns.** The pending
pre-ingress authorization request, its binding, its expiry, its attempt count,
and Auth's session effect all require a holder that the architecture does not
name and the `session` lifetime class cannot honestly provide.

This is a missing boundary, not merely a missing field. It should be resolved by
naming a holder with an evidenced lifetime — most plausibly binding it to
`host_session` under the Host Adapter, or requiring a continuity receipt — not
by adding a component.

No other boundary is missing. In particular, I do not think Mood, MMU, a
Faithfulness component, a diagnostics service, a classroom/School component, or
a separate ProofGate is needed, and I confirm the decisions to reject each.

## Conclusions

### Component minimality

Confirmed minimal. Seven components/boundaries all earn their existence. The
four deterministic core components each have one distinct responsibility, and
the merge analysis in `successor_kernel.md` correctly identifies why each merge
would mix authority. No component is retained on historical identity, and the
validator's `FORBIDDEN_COMPONENT_TERMS` check plus the rejection of School
Engine and legacy PASS is backed by negative tests. No hidden mega-Exec has
accumulated inside Turn Controller or Validation and Egress; both are long but
internally coherent, with one creep item (N4) flagged.

### Ownership

Confirmed exclusive for every significant deterministic responsibility, with two
coverage gaps (N1). I traced ingress normalization, `TurnRequest` construction,
capability validation, route selection, one-owner locking, ScopeLock
construction, authorization, OPSEC, source policy, artifact validation,
completion validation, egress authorization, receipt assembly, continuity
reads/writes, and host delivery across `component_registry.json`,
`packet_registry.json`, `interface_registry.json`, `behavior_placement.json`,
and the four architecture documents. No responsibility has two authoritative
owners. The construction/validation split (Turn Controller builds ScopeLock,
Validation and Egress checks against it) is correctly *not* duplicate ownership.

### False determinism

Confirmed sound in almost every dimension. The spec consistently distinguishes
`deterministically_specifiable` from implemented, proven, or available:
`implementation_state` is declared as
`deterministically_specifiable_not_implemented`; declared capability is
separated from verified availability with a mandatory receipt; typed
`AuthorizationResult` is explicitly not verified identity; a schedule request is
not a future wake; a source policy is not an entailment proof; an artifact
request is not artifact existence; a `TerminalPacket` is not host delivery; a
continuity packet is not durable persistence. The `contracts/successor/README.md`
interpretation rules state this directly.

The single material exception is `session` (BF-2) — a state class asserted
without the evidence discipline the design applies everywhere else.

### Source authority

Confirmed unchanged and correctly subordinated. `00_Instructions.md` remains
`deployment_instruction` and `01_Persona.md` through `06_Programs.md` remain the
six kernel/runtime capsules, per `config/source_authority.json`, which BC-018
did not modify. I independently verified all eight
`kernel/golden/v0.22.0/SHA256SUMS` entries pass, and that
`git diff --name-only a5e68b31 -- kernel/golden contracts/runtime
docs/sources/historical_archives` is empty. BC-018 correctly and repeatedly
states that successor decisions do not retroactively repair current-source gaps;
`decisions.md` and BEH-013 both preserve the OPSEC source gap rather than
pretending it away.

### Model-facing preservation

Confirmed strong. See Q5. Python does not replace the model's job of being Blu.
The ordinary conversational path is not gate-bound, does not require fake Auth,
host calls, persistence, capability proofs for unused capabilities, source
validation outside source-bound lanes, or service packets when no service is
used. Fail-closed behavior is scoped to security, authorization-required,
`source_only`, owner-locked, and proof-required lanes, with safe degradation
explicitly permitted for ordinary conversation.

### OPSEC/Auth

Security properties confirmed; turn and state model returned for correction. See
Q4. OPSEC stays before ordinary routing and outside route ownership, owns only
the pre-ingress decision, minimization, and its result, and does not own
authentication, routing, generation, or secret storage. Auth is a real bounded
contract over action, resource, scope, policy reference, assurance, explicit
evidence, session effect, and expiry/reset, with unavailable evidence handled
honestly and conversational inference excluded. The design admits that real
identity depends on the host. No protected policy, challenge material, or
secret content appears anywhere in the specification, and this review did not
request or expose any. BF-1, BF-2, and BF-3 are the blocking items.

### BC-020 readiness

`ready_for_spec` — confirmed, with the scoping caveat in Q10 that the
authorization-evidence portion should follow the BF-1/BF-3 correction.

### BC-030 readiness

`ready_for_spec` — confirmed without caveat.

### Implementation eligibility

**Not eligible.** No successor runtime implementation may begin.

This is not solely a consequence of the blocking findings. BC-018 is a design
artifact by construction, and its own register marks `SUR-001`, `SUR-002`,
`SUR-003`, and `SUR-010` as blocking for implementation. The migration sequence
is correctly planning-only, respects dependency ordering, allows small testable
increments, and explicitly requires separate authorization for each step;
BC-020 and BC-030 remain separately authorized and unstarted, and the global
assignment index still lists both as `spec-needed`. Nothing in BC-018 quietly
authorizes implementation.

## Validation review

I re-ran the full suite independently at the reviewed head. Confirmed:

```text
runtime contract validator: passed
contract tests: Ran 21, OK
viability audit validator: passed
viability tests: Ran 9, OK
historical inventory validator: passed
historical inventory tests: Ran 12, OK
historical archaeology validator: passed
historical archaeology tests: Ran 18, OK
successor specification validator: passed
successor specification tests: Ran 25, OK
golden CTS SHA-256: 8/8 passed
canonical manifest: 185 entries, self-excluded, 0 missing, 0 mismatch
protected-path diff from authorized base: empty
```

The manifest was verified independently against staged Git-blob bytes rather
than by re-reading the recorded result. The four correction negative tests are
present and real: `test_turn_request_producer_must_be_turn_controller`,
`test_ordinary_routing_requires_security_pass`,
`test_opsec_authorization_requires_auth_reentry`, and
`test_auth_cannot_merge_into_opsec`, alongside the strengthened
`test_opsec_must_be_pre_ingress`.

Green validation is not evidence of semantic correctness. The validator checks
structural integrity and a specific set of architectural guardrails. It does not
detect ownership *coverage* gaps (N1), packet-boundary redundancy (N3), the
turn-model contradiction in BF-1, the missing lifetime substrate in BF-2, or the
missing repetition bound in BF-3 — all three blocking findings pass every
existing check.

## Pre-review correction verification

### A. TurnRequest ownership — verified correct

The required sequence is normative and consistent across every named surface:

```text
raw_host_event -> Host Adapter -> raw_host_input -> Security Restraint
-> SecurityDecision PASS + minimized allowed_input -> Turn Controller
-> normalized TurnRequest
```

- `component_registry.json`: `host_adapter_boundary.does_not_own` includes
  `ingress_task_normalization` and `TurnRequest_construction`; its outputs are
  `raw_host_input` and provider records, not `TurnRequest`. `turn_controller`
  owns `ingress_normalization` and outputs `TurnRequest`.
- `packet_registry.json`: `ingress_ownership` sets the adapter's output to
  `raw_host_input` with `does_not_produce: TurnRequest`, and
  `turn_controller.sole_turn_request_producer: true`. `TurnRequest.producer` is
  `turn_controller`, with invariants requiring `PASS` and `allowed_input`
  equality.
- `interface_registry.json`: `ingress_contract.turn_request_producer` is
  `turn_controller`; `IF-HOST-CAPABILITY.required_behavior` includes
  "never construct TurnRequest".
- `behavior_placement.json`: BEH-008 output contract is "normalized TurnRequest
  produced only by turn_controller".
- `successor_kernel.md` steps 1 and 5, `successor_component_graph.md` graph plus
  narrative, `successor_boundaries.md` packet-ownership paragraph and host
  adapter boundary, `traceability.json` SKR-003, and the migration sequence all
  agree.

No residual text anywhere assigns `TurnRequest` construction to the Host
Adapter. Enforced by validator checks and a negative test.

### B. Pre-ingress Auth loop — semantics verified, turn/state model returned

Verified correct: authorization not required yields `PASS`/`BLOCK` as policy
permits; adequate existing bounded authorization may be consumed by the Security
Restraint; absent required evidence yields `ASK` with a safe
`authorization_request_ref`; the safe terminal goes through Validation and
Egress; the Host obtains explicit evidence; the Authorization Evaluator returns
an `AuthorizationResult` bound to the request; the result re-enters the Security
Restraint for a new decision; only `SecurityDecision PASS` reaches the Turn
Controller; ordinary routing is bypassed throughout; Auth stays separate from
OPSEC; OPSEC stays before ordinary routing; conversational identity inference is
excluded. All of this is consistent across `packet_registry.json`,
`interface_registry.json`, `component_registry.json`, `behavior_placement.json`
BEH-012/BEH-013, all four architecture documents, `decisions.md`, and
`traceability.json` SKR-001/SKR-002, and is enforced by validator checks with
negative tests.

Returned for correction: the loop's turn model (BF-1), the lifetime class it
depends on (BF-2), and its lack of repetition bounding (BF-3).

## Additional verifications

- **Exec decomposition (§17).** Arbitration, route/owner discipline, ScopeLock,
  validation, capability honesty, fail-closed paths, artifact and completion
  proof, and egress discipline are all preserved and assigned. No Exec
  component, no catch-all owner, no re-embedded feature workflows, no mega-Exec
  under another name. One decomposition-completeness note (N6).
- **Error model (§20).** All six statuses change control semantics and remain
  distinct. `ASK` (one bounded user decision can resolve it) versus
  `UNAVAILABLE` (no provider) is clean, and reinforced by the invariant
  "UNAVAILABLE does not become ERROR merely because a capability is absent."
  `BLOCK` (policy/evidence forbids) versus `INVALID` (contract violation) is
  clean. Provider `ERROR` versus policy `BLOCK` is clean.
- **Capability truth (§12).** `verification_method`, `provider`, `scope`,
  `limitations`, freshness/turn scope, `receipt`, and `failure_reason` are
  sufficient generic concepts for BC-020, with no host-specific implementation
  present.
- **Teaching/classroom (§15).** Pedagogy stays model-facing; schedules, class
  state, durable records, and curriculum providers are correctly separated.
  School Engine is rejected without rejecting the classroom goal; BEH-023
  defers state schema and SUR-009 keeps it open.
- **Mood (§16).** The no-dedicated-component decision is correct and evidenced.
  Persona guidance is sufficient; SUR-008 keeps optional metadata open. See N1
  for the one placement inconsistency.
- **SkillForge/PASS isolation (§24).** `IF-SKILL-CONTEXT` is optional, external,
  versioned, provenance-bearing, consumed by the model boundary, and fails
  `UNAVAILABLE` without core failure. Kernel viability is not coupled to
  SkillForge; no Blu-specific Skill Cards are required; no PASS or SkillForge
  source was touched; legacy PASS remains rejected. Validator-enforced.
- **Evidence traceability (§26).** All 38 catalog entries resolve to real files
  and real locators, and every component, behavior, and requirement reference
  resolves to the catalog. Successor-only decisions are labeled as such
  (`successor_design_decision`,
  `approved_successor_decision_not_current_source_repair`) rather than
  disguised as recovered evidence, and old-module existence is nowhere used as
  sufficient justification. Gap noted in N8.
- **Unresolved register (§27).** Ten items, all genuine. None blocks the BC-018
  *architecture* itself; four correctly block implementation. One unknown is
  missing (BF-3).
- **Architecture creep (§29).** Minor and contained: `receipt_backed_diagnostics`
  (N4) and optional profile metadata placement (N1). No speculative classroom
  abstractions, no extra service types, no unearned source-validation layers,
  no packet-field sprawl.
- **Security publication boundary (§30).** No Auth answers, challenge material,
  OPSEC secrets, protected kernel passages, or private information were
  requested, inspected, or are reproduced in this review.

## Required follow-up

Dad and Blu decide integration and closure. BC-018 is **not** marked done by
this review.

Recommended path: authorize a narrow BC-018 correction addressing BF-1, BF-2,
and BF-3 — all three are the same weak spot and can be fixed together without
changing the component count, packet count, or boundary set — and treat N1
through N9 as optional cleanups for the same pass. BC-030 specification work is
unaffected by the blocking findings. BC-020 specification work is unaffected
except for its authorization-evidence surface.

Do not begin BC-020, BC-030, or runtime implementation.

## Final status authorization

- Authorized by: pending Dad/Blu decision
- Assignment status: review
- Reviewer disposition: return-for-correction
- Date: 2026-08-08
