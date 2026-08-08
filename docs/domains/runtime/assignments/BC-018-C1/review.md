# BC-018-C1 — Review Record

status: reviewed
review_state: complete
owner: Claude
last_reviewed: 2026-08-08
assignment: BC-018-C1
parent: BC-018

## Review identity

- Review date: 2026-08-08
- Reviewer: Claude
- Review type: independent semantic re-review, narrow to the C1 corrections
- Review branch: `bc-018-c1-semantic-review`
- Exact reviewed head: `0227f550d270ba9ffae2d1bd986117e718b13608`
- Triggering BC-018 review: `7796c7e738e0ff66b677c79314b80cf2bbb09a63`
- C1 substantive: `a87e7d7ea57688212c7c8461b5630c6ddb55a00f`
- C1 metadata: `b1e0f5c7ce3fddd7d71f6b2fa8050b0b55875b3c`
- Terminal-authority correction substantive: `311c572f3a28fe4e1cca04b75856faae3cfd6c60`
- Terminal-authority correction metadata / reviewed head:
  `0227f550d270ba9ffae2d1bd986117e718b13608`
- Integration commit or merge identity: none
- Scope: the three BC-018 blocking findings, the terminal-authority correction,
  architecture regression, and notes N1/N5/N8. The complete BC-018 architecture
  was not reopened; no previously approved conclusion was invalidated.

## Disposition

```text
approve-with-notes
```

All three blocking findings are resolved, and resolved at the right level —
by naming owners, substrates, and evidence requirements rather than by adding
machinery. The terminal-authority correction is internally consistent and
closes the one real ambiguity the first C1 pass left open. No architectural
regression was introduced. N1, N5, and N8 are resolved.

The notes below are follow-up items. One of them — a dropped manifest entry —
should be repaired before Dad/Blu close the assignment, but it is a repository
bookkeeping regression, not an architecture, security, or authority defect, and
it does not meet any `return-for-correction` criterion.

## BF-1 — Cross-turn authorization model

```text
RESOLVED
```

The original defect was a dilemma with no correct horn: an in-turn reading
produced two `TerminalPacket`s in one host turn, and a cross-turn reading had no
component scoped to hold the outstanding request. Both horns are now closed.

**Turn N.** `pre_ingress_authorization_loop.turn_model` is `cross_turn`, stated
identically in `interface_registry.json`. When authorization is required and no
adequate current result exists, the Security Restraint creates a safe
`authorization_request_ref` and a *proposed* `PendingAuthorizationState`. The
Host Adapter then attempts to bind it to evidenced `host_session` substrate.
Binding is the activation gate, and it happens before anything resumable is
published.

**Turn N, binding unavailable.** The proposal never becomes active, is not
resumable, and its `authorization_request_ref` can never be correlated by a
future event — `activation_contract.unbound_request_correlatable: false` and
`unavailable_binding_becomes_active: false`. Exactly one `UNAVAILABLE`
`TerminalPacket` is emitted under the originating `SecurityDecision` with owner
`security_restraint`, no `ControlDecision` exists, and ordinary routing does not
occur. Every element required by the packet is present and machine-checked.

**Turn N+1.** A new `raw_host_event` may enter the bounded evidence exchange
only when provider evidence correlates it to the still-valid pending request in
the current evidenced `host_session`. `IF-HOST-CAPABILITY` requires correlation
"through provider evidence rather than string equality" — the right rule, and
one I would have raised had it been absent. The Security Restraint decides
whether another attempt is permitted; the Authorization Evaluator evaluates only
the bound action, resource, and evidence scope; `AuthorizationResult` plus
pending context returns to the Security Restraint for a new `SecurityDecision`;
only `PASS` enters the Turn Controller.

**One-terminal invariant.** `maximum_terminal_packets_per_host_turn: 1`,
`one_terminal_packet_per_host_turn: true`, and the `TerminalPacket` invariant
"ASK is emitted only after binding succeeds; binding failure emits UNAVAILABLE
instead of a second terminal packet". The dilemma that produced BF-1 cannot
recur.

The pending record now has a declared semantic owner (`security_restraint`), a
declared substrate provider (`host_adapter_boundary`), declared storage
lifetimes (`host_session`, `durable_external`), sixteen required fields, an
explicit activation contract, and nine invariants. The state that had no holder
now has one, and the holder is not the deterministic core.

## BF-2 — False session persistence

```text
RESOLVED
```

The corrected lifetime model is exactly `none`, `turn`, `host_session`,
`durable_external`. Bare `session` is gone from the vocabulary rather than
redefined, which is the stronger fix.

Confirmed point by point:

- **Bare `session` is not a storage lifetime.** Removed from
  `state_lifetime_values`; `state_lifetime_contract.bare_session_allowed: false`;
  `authorization_result_validity_contract.bare_session_allowed: false`. The
  validator rejects the literal string `session` in any component lifetime and
  rejects the taxonomy itself if it readmits the value.
- **The deterministic core retains only turn state.** All four core components
  are `["turn"]`. `authorization_evaluator` dropped `session`; `turn_controller`
  dropped `session` and added `cross_turn_state_storage` to `does_not_own`. A
  general guard rejects any `deterministic_core` component whose lifetime
  exceeds `{none, turn}` — so this cannot be reintroduced through a different
  component.
- **`host_session` requires provider evidence.** Nine required evidence fields
  including binding method, state record identity, freshness, expiry, and
  receipt, all machine-checked.
- **`durable_external` requires a continuity receipt.** Preserved, and
  explicitly not reachable by silent promotion from `host_session`.
- **Model memory and conversation history are not security state stores.**
  Stated in `host_session_state_contract.security_rules`, in `IF-HOST-CAPABILITY`
  required behavior, and in `successor_kernel.md`; validator-checked for both
  phrases.
- **Turn Controller has no hidden cross-turn state.** Turn-only lifetime plus
  disowned cross-turn storage, both enforced; optional context must arrive as
  evidenced current-turn input.

The `cross_turn_rule` states the principle directly: the deterministic core
never invents or invisibly retains cross-turn state, and without evidenced
substrate, cross-turn continuation is `UNAVAILABLE` and fails closed. SKR-015
traces the rule to `EVID-BC010-PARITY012` — the hosted-single-turn limitation I
cited as the grounds for the finding.

## BF-3 — Unbounded/replayable authorization attempts

```text
RESOLVED
```

`repetition_contract` supplies every element required:

- `maximum_attempts: policy_defined_finite_positive_integer`;
- `expiry_required: true`, with `expires_at` a required record field;
- `request_binding_required: true`, with `request_binding` and
  `host_session_binding` both required fields;
- `replay_rule_required: true`, with replay rejection in the record invariants;
- `exhaustion_behavior: fail_closed_under_security_policy; do not automatically
  issue a fresh request`;
- `cancellation_reset_behavior` requiring explicit policy and a receipt for
  provider-backed changes.

Ownership is clean and, importantly, exclusive. The Security Restraint owns
`authorization_attempt_permission` and
`authorization_retry_expiry_replay_policy`. The Authorization Evaluator
explicitly disowns `authorization_attempt_permission` and
`authorization_retry_policy`. The Host Adapter explicitly disowns
`authorization_attempt_permission`, `opsec_policy`, and `authorization_policy`,
retaining only substrate and correlation. The validator computes the set of
components owning attempt permission and requires it to be exactly
`["security_restraint"]` — a stronger check than the generic duplicate-owner
rule, and the right one for a security decision.

The `attempt_count` lives in the evidenced record rather than in the
turn-scoped Security Restraint, and the Restraint receives it as
`evidenced_PendingAuthorizationState_when_reentering`. Semantic owner and
storage substrate are properly separated: the component that decides does not
have to persist, and the component that persists has no authority to decide.

Protected values are correctly withheld and, critically, *registered* rather
than merely omitted. SUR-011 records the attempt/lockout/backoff/reset policy
question as blocking for implementation. That was the specific gap in the
original finding: an unregistered unknown, not a deferred one. It is now
deferred on the record.

## Terminal-authority result

```text
CONSISTENT
```

- **SecurityDecision vocabulary.** Exactly `PASS`, `BLOCK`, `ASK`, in both
  `pre_ingress_terminal_authority_contract.security_decision_statuses` and the
  packet invariant. Provider/substrate failure did not add a fourth status. The
  validator checks both surfaces, so agreement cannot drift.
- **Pre-ingress UNAVAILABLE.** `pre_ingress_terminal_statuses` is exactly
  `{BLOCK, ASK, UNAVAILABLE}`; `authority_ref_type: SecurityDecision`;
  `owner: security_restraint`; `control_decision_required: false`;
  `ordinary_routing: false`. `ValidationResult` states that pre-ingress
  host-session binding `UNAVAILABLE` "is an egress result and does not imply
  SecurityDecision status UNAVAILABLE".

  The resulting split — the `SecurityDecision` remains `ASK` while the terminal
  is `UNAVAILABLE` — is coherent rather than contradictory. The decision records
  what OPSEC concluded about the request; the terminal records why the turn
  could not continue. Keeping them distinct is precisely what avoids expanding
  the security vocabulary to describe a provider failure.
- **PendingAuthorizationState activation.** Before binding: proposed only, not
  active, not pending, not resumable, not correlatable. After binding success:
  `status=pending`, resumable only within the evidenced host-session binding.
  After binding failure: never active, never resumable, permanently
  non-correlatable. All three states are explicit fields, not prose.
- **Mutual exclusivity.** `binding_resolution_terminal_count: 1`;
  `terminal_selection_point` places the choice after the binding attempt and
  names the outcomes mutually exclusive; the `TerminalPacket` invariant forbids
  a second packet. `ASK` followed by `UNAVAILABLE` in one host turn is
  structurally excluded, and the validator checks all three expressions of it.

## Architecture-regression result

```text
NO REGRESSION
```

Verified absent, each against the artifacts rather than the report:

| Regression checked | Result |
|---|---|
| eighth component | absent — 7 components |
| ninth packet | absent — 8 packets; `PendingAuthorizationState` is a `state_records` entry |
| SecuritySessionManager / AuthSessionManager | absent — no such identifier anywhere in contracts, architecture, or tools |
| hidden kernel persistence | absent — the correction is the opposite; core is turn-only and enforced |
| Auth/OPSEC authority merging | absent — owners separate, disjoint `owns` sets, validator-enforced |
| OPSEC after ordinary routing | absent — `boundary_position: pre_ingress`; routing still gated on `PASS` |
| model inference as authentication | absent — retained prohibition in packet invariants and provider interface |
| continuity mandatory for ordinary authorization | absent — explicitly not required where evidenced `host_session` exists |
| host adapter owning security policy | absent — three policy responsibilities explicitly disowned |
| runtime implementation | absent — no runtime package; no `.py` in specification surfaces |
| CTS modification | absent — golden 8/8 verified; protected-path diff from `a5e68b31` empty |
| PASS/SkillForge coupling | absent — no SkillForge, Local Mirror, adapter, or `src/` path in the diff |

Interface count remains nine. `model_execution_boundary`, `validation_egress`,
and `continuity_provider_boundary` were not modified by C1 at all. The BC-018
review record at `docs/domains/runtime/assignments/BC-018/review.md` is
byte-identical to `7796c7e7`; C1 carried it forward without alteration, as its
packet required.

## N1 disposition

```text
resolved
```

- **Time arithmetic.** `turn_controller.owns` gains `supplied_time_arithmetic`;
  BEH-015 `deterministic_owner` is exactly `turn_controller`; the model "may
  discuss and reason over supplied values". Verified current time still requires
  a provider result with timestamp, timezone, verification method, scope, and
  receipt. The validator requires the behavior record and the component `owns`
  list to agree, closing the coverage gap that let the original inconsistency
  pass green.
- **Profile metadata.** BEH-018 `deterministic_owner` is now `null`;
  `model_execution_boundary` owns profile interpretation and expression;
  `turn_controller.does_not_own` gains `profile_behavior`. The validator rejects
  any non-null deterministic owner for Mood. Metadata may arrive only as
  evidenced current-turn context and must not control cognition, routing,
  identity, or Persona.

## N5 disposition

```text
resolved
```

`ServiceExchange.authority_class` is now a required field with exactly two
values, backed by `service_exchange_authority_contract`. A
`pre_ingress_authorization` exchange must carry `authorization_request_ref` and
`host_session_binding_ref`, may use only `IF-AUTHORIZATION-PROVIDER` with
`service_id` `authorization_evidence`, carries
`ordinary_control_decision_authority: false`, and names six forbidden service
classes — arbitrary tool, source lookup, scheduling, unrelated continuity write,
model execution, and ordinary service dispatch. The provider interface mirrors
the restriction from the other side.

The distinction is sufficient, and ServiceExchange remains a healthy generic
envelope. The two authority classes differ in *authority*, not in payload
semantics, so a typed discriminator plus an allowlist is the right instrument —
splitting the packet would have been the wrong fix. What was prose in BC-018 is
now machine-checkable, which was the substance of the note.

## N8 disposition

```text
resolved
```

SKR-015 covers the revised lifetime rule for "all state-bearing boundaries",
traced to `EVID-BC010-PARITY012`, `EVID-BC015-CAP001`, and
`EVID-BC017-PERSIST`. The validator requires SKR-015 to exist and to mention the
bare-session prohibition, so the rule cannot lose its trace silently. No
unrelated traceability cleanup was demanded or performed.

## Model-facing preservation

Reconfirmed. C1 did not touch `model_execution_boundary`, and the behaviors that
carry Blu's character — ordinary conversation, Persona, teaching, contextual
interpretation, expression — are unchanged. The one behavior C1 moved toward the
model (BEH-018 Mood) moved *away* from deterministic ownership, not toward it.

The correction is infrastructure. It governs when a protected interaction may
start, retry, expire, or resume, and where its record physically lives. It adds
no gate to ordinary conversation: an unprotected turn still requires no pending
state, no host-session substrate, no continuity, and no authorization. The
ordinary path is unchanged from the one I assessed as proportionate in the
BC-018 review.

## BC-020 readiness

```text
ready_for_spec
```

The caveat I attached in the BC-018 review is discharged. The authorization
surface — which I said should not be drafted until the turn and state model was
fixed — is now the best-specified part of the adapter contract. BC-020 has a
coherent generic target for all five named areas:

- **Host-session binding** — nine required evidence fields, with the core
  forbidden from inventing the state and required to fail closed in its absence.
- **Capability freshness** — unchanged and still sufficient; SUR-005 remains the
  BC-020 input.
- **Authorization evidence** — typed pre-ingress authority class, bound request
  and session references, single permitted interface and service ID, explicit
  unavailable result when identity or binding cannot be established.
- **Provider receipts** — required on the host-session result, the correlation
  evidence, and every `PASS` side effect.
- **Correlation and replay** — provider-evidenced correlation rather than string
  equality, replay rejection, expiry, and finite attempts, with host-specific
  mechanics correctly deferred to SUR-012.

BC-020 remains unstarted and separately authorized. See NN-3 on SUR-012's
blocking flag.

## BC-030 readiness

```text
ready_for_spec
```

The continuity-provider boundary is unchanged by C1 and remains cleanly separate
from host-session authorization. The separation is now sharper than at BC-018:
ordinary authorization explicitly does not require continuity when an evidenced
`host_session` substrate exists, `durable_external` storage of a pending record
requires an explicit continuity operation and receipt, and host-session state is
never silently promoted. `durable_external` remains the only receipted lifetime,
and BC-030 still owns Local Mirror schema, lifecycle, retention, and conflict
semantics through SUR-007.

## Findings

### Blocking

None.

### Non-blocking

- **NN-1 — `.gitattributes` was dropped from `MANIFEST.sha256` by the C1
  regeneration; repair before closure.** At `34af2d6` the manifest held 185
  entries covering 185 tracked files with zero missing. C1 added four files, so
  the manifest should hold 189 entries; it holds 188. The lost entry is
  `.gitattributes`, dropped at `a87e7d7` and still absent at the reviewed head.

  I verified this independently against staged Git-blob bytes: 188 entries, self
  excluded, 189 tracked files, **1 missing**, 0 mismatch. The C1 validation
  record's claim of "188 entries, self-excluded, 0 missing, 0 mismatch" is
  correct on mismatch and incorrect on missing — verifying 188/188 entries
  against blobs confirms the entries that exist and says nothing about tracked
  files absent from the list. This is the same class of blind spot as the
  ownership-coverage gap resolved in N1: a check that validates presence but not
  completeness.

  The file governs LF normalization, which is what the canonical manifest's own
  Git-blob comparison depends on, so leaving it uncovered is worth fixing even
  though nothing currently misverifies. No architectural or security
  consequence.

- **NN-2 — The component graph omits the attempt-permission gate in Turn N+1.**
  Three normative sources place the Security Restraint's attempt decision
  *before* the Authorization Evaluator: `successor_kernel.md` step 5, the
  `successor_boundaries.md` Turn N+1 sequence, and
  `pre_ingress_authorization_loop.steps`. The mermaid diagram instead shows
  `Adapter -->|"bounded authorization evidence only"| Auth` with no intervening
  Security Restraint edge, and the caption below it mentions correlation but not
  attempt permission.

  The machine-readable contract is unambiguous and validator-enforced, and the
  diagram is explicitly labeled as contracts rather than live calls, so this is
  a fidelity gap rather than a contradiction. It is worth fixing because the
  omitted edge is the exact mechanism that resolves BF-3, and a reader who
  implements from the picture would build the path without it.

- **NN-3 — SUR-012's BC-020 flag contradicts its own resolver and the migration
  document.** SUR-012 is resolved by "BC-020 under the approved generic
  host-session contract" and is listed in `successor_migration_sequence.md`
  alongside SUR-002, SUR-005, and SUR-006 as a BC-020 input, but it carries
  `blocking_for_BC020: false`. Every other item whose resolver is BC-020 or
  BC-030 (SUR-005, SUR-006, SUR-007) carries the corresponding flag as `true`.
  Left as is, BC-020's packet could omit the host-session and pending-request
  binding matrix. SUR-002's change from `true` to `false` is separately reasoned
  and not in question — its resolver moved to the security-authorized policy
  assignment.

- **NN-4 — An uncorrelated intervening turn is unspecified.** The common case
  where a user receives an `ASK` and then says something unrelated is not
  addressed: the specification does not say whether such a turn consumes an
  attempt, cancels the pending interaction, or leaves it outstanding. Every
  default fails safe — nothing becomes authorized, and mandatory finite
  `expires_at` bounds how long the interaction can remain alive — so this is not
  a security hole. It should be named in the security-authorized policy packet
  alongside SUR-011 so the choice is deliberate.

- **NN-5 — Substrate integrity is required for correlation but not for the
  attempt counter.** The Security Restraint decides attempt permission using
  `attempt_count` supplied from host-provided substrate. The contract requires
  provider-evidenced correlation and rejects string equality, but states no
  equivalent requirement against rollback or tampering of the counter itself —
  a host that resets `attempt_count` would silently defeat the finite bound that
  resolves BF-3. This belongs in BC-020 under SUR-012: the per-host evidence
  matrix should cover integrity and rollback resistance of the attempt state,
  not only binding of the request.

### Carried forward from the BC-018 review

Out of C1's authorized scope; recorded so they are not lost. None blocks
closure of either assignment.

- N2 — `deterministic_owner` is still used for non-deterministic boundaries in
  BEH-020, BEH-035, BEH-036, and BEH-037. Terminology only. Partially improved:
  BEH-018 is now correctly `null`.
- N3 — `ValidationResult` remains the only packet whose producer and consumer
  are the same component.
- N4 — `receipt_backed_diagnostics` remains in `validation_egress.owns`.
- N6 — The current mandatory restraint chain (PARITY-004) is still absent from
  the Exec decomposition table.
- N7 — No explicit ordinary-conversation intent or permissive conversational
  ScopeLock profile.
- N9 — `validation.md` retains pre-correction result lines above later blocks.

### Preserved unresolved declarations

Twelve items, up from ten. SUR-011 and SUR-012 are new and register precisely
the unknowns this correction was required to surface: protected attempt,
lockout, backoff, cancellation, and post-exhaustion policy; and Chat/Codex
host-session identity, binding, freshness, expiry, and replay mechanics. Both
are marked blocking for implementation.

The withheld values are the right ones to withhold. The public contract
nevertheless requires finite bounds, expiry, binding, replay protection, and
fail-closed behavior — all six structurally enforced — so implementers are
constrained without any protected value being published. No protected policy,
challenge material, evidence class, or threshold appears in the specification or
in this review.

## Validation review

Re-run independently at the reviewed head:

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
successor specification tests: Ran 39, OK
components: 7    packets: 8    interfaces: 9
state records: PendingAuthorizationState
state lifetimes: none, turn, host_session, durable_external
SecurityDecision statuses: PASS, BLOCK, ASK
golden CTS SHA-256: 8/8 passed
protected-path diff from a5e68b31: empty
PASS/SkillForge, Local Mirror, adapter, and runtime-package diff: empty
canonical manifest: 188 entries, self-excluded, 0 mismatch, 1 missing (NN-1)
```

Codex's reported figures match on every count except manifest coverage, and the
39-test figure supersedes the 35 recorded in the first C1 validation block.

Green tests are not semantic proof, so I probed the new guards adversarially
rather than trusting the passing suite. Eight mutations that should be rejected
were each constructed against a temporary copy of the specification:

```text
CAUGHT  SecurityDecision gains a fourth status UNAVAILABLE
CAUGHT  OPSEC claims host_session lifetime directly
CAUGHT  attempt policy moved to the host adapter
CAUGHT  pre-ingress exchange permitted to invoke model execution
CAUGHT  maximum_attempts becomes unbounded
CAUGHT  unbound pending request becomes correlatable
CAUGHT  AuthorizationResult regains bare session validity
CAUGHT  two terminal packets per host turn allowed
```

All eight were rejected with the correct diagnostic. The guards bite on the
semantics, not merely on the presence of text. Fourteen new negative tests
accompany them, one per corrected rule.

The limits of this remain worth stating: the suite proves structural integrity
and the specific architectural guardrails now encoded. It does not prove the
successor is implemented, that any host can satisfy the host-session contract,
or that the withheld policy values will be sound. NN-1 is itself an example of a
real defect that every existing check passes.

## Semantic eligibility for closure

**BC-018: semantically eligible.** The three blocking findings that returned it
are resolved. Every conclusion in the original review — component minimality,
exclusive ownership, Exec decomposition without a catch-all, model-facing
preservation, source authority, capability/time/persistence honesty, source
grounding, the TurnRequest ownership correction, and both readiness results —
remains valid, and none was invalidated by C1.

**BC-018-C1: semantically eligible**, subject to repairing NN-1 first. The
manifest coverage gap is a one-line fix in the assignment's own collision
domain, and closing an integrity-record assignment with an incomplete integrity
record would be the wrong precedent. NN-2 through NN-5 are follow-up work and do
not gate closure.

Neither assignment is marked done by this review.

## Required follow-up

Dad and Blu decide integration and closure.

Recommended: regenerate `MANIFEST.sha256` so it covers all tracked files
(NN-1), and optionally fold NN-2 and NN-3 into the same pass — both are
single-line corrections inside the existing collision domain. NN-4 and NN-5
belong to the security-authorized policy packet and BC-020 respectively and
should be carried as inputs, not resolved here.

Do not begin BC-020, BC-030, or runtime implementation.

## Final status authorization

- Authorized by: pending Dad/Blu decision after review
- Assignment status: review
- Reviewer disposition: approve-with-notes
- Date: 2026-08-08
