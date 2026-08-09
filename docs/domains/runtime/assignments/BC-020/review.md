# BC-020 — Review Record

status: reviewed
review_state: complete
owner: Claude
last_reviewed: 2026-08-08
assignment: BC-020

## Review identity

- Review date: 2026-08-08
- Reviewer: Claude
- Review type: independent read-only semantic host-contract review
- Review branch: `bc-020-semantic-review`
- Exact reviewed head: `ccf3206ad033d588246e09001d47ddce3ac50a31`
- Authorized base: `d4157e79fc7e2df6e1bd53b589cabfa19cd7238f`
- Substantive work: `09c484418e51365cf9b156cf304eebae7fecde5d`
- Metadata commit / reviewed head: `ccf3206ad033d588246e09001d47ddce3ac50a31`
- Integration commit or merge identity: none

## Disposition

```text
return-for-correction
```

BC-020 is a strong, unusually disciplined evidence document. The Chat matrix is
exemplary: no live probe was run, and nothing was inferred from product
branding, the executing session, or documentation. The Codex matrix is scoped to
one named binding throughout. Sign-in, host approval, and Blu authorization are
cleanly separated. Receipts prevent false side-effect completion. Nothing leaked
into the generic BC-018 architecture.

The disposition is `return-for-correction` for **one** defect: three Codex
scheduling rows are marked `verified_available` on tool-schema exposure alone,
which the document's own evidence register declines to support and which
contradicts how BC-020 treats identical evidence for three other capabilities.
That is a capability overclaim in the highest-risk capability class this project
has, and capability overclaim is a named return-for-correction trigger.

The correction is narrow — three status values and their limitations — and
requires no restructuring. Everything else in BC-020 should stand.

## Blocking findings

### BF-1 — Three Codex scheduling capabilities are `verified_available` on interface metadata alone

**Rows.** `schedule.create`, `schedule.recurring`, `schedule.update_cancel` in
`adapters/codex/capability_matrix.json`, each `verified_available` with exactly
one evidence reference: `CODEX-EVID-PROBE-TOOLS`.

**What that evidence actually says.** The probe is a `local_probe` whose claim
is "Dynamic external tool metadata and an automation management interface are
exposed in the current binding," scoped to "tool names/descriptions exposed to
this turn." Its `supports` list contains `scheduling_interface_exposed` — not
scheduling availability — and its `does_not_prove` list contains
`schedule_operation_success` and `external_account_connection`. Its stated
limitation is "Metadata exposure does not prove credentials, provider
connection, permission, operation success, or receipts."

So BC-020's own semantic annotation of this evidence declines to carry the
claim the capability rows make.

**Why it is a defect rather than a defensible reading.** The common contract
defines `verified_available` as "Current binding evidence proves the capability
is **usable** within the recorded surface, scope, and freshness boundary."
Schema exposure proves an interface is *present*, not that the underlying
provider is connected, permitted, or functional. BC-020 applies exactly that
reasoning to the same probe three other times and reaches the opposite status:

| Capability | Evidence | Status | BC-020's stated reason |
|---|---|---|---|
| `retrieval.connected_source` | `CODEX-EVID-PROBE-TOOLS` | `unknown` | "Tool metadata does not prove connection or readable source." |
| `retrieval.integration_context` | `CODEX-EVID-PROBE-TOOLS` (+doc) | `unknown` | "Exposed metadata does not prove provider connection or result." |
| `action.git.pr_operation` | `CODEX-EVID-PROBE-TOOLS` | `unknown` | "No PR provider operation or receipt." |
| `schedule.create` / `.recurring` / `.update_cancel` | `CODEX-EVID-PROBE-TOOLS` | **`verified_available`** | — |

The same probe also exposed Gmail and Sites tool metadata; BC-020 correctly
declines to derive any capability from those. The scheduling treatment is
anomalous within its own document.

**Prose versus contract.** `codex_adapter.md` and the handoff are precise: they
say the interface "proves a current create/update/delete/recurrence
**interface**" and describe it as "current evidence of **interface
availability**." That is the honest reading. But the capability IDs denote
operations, not interfaces, and `capability_matrix.json` is what a Turn
Controller consumes. A consumer reading the contract gets "creating schedules is
verified available on this surface." Honest prose does not repair an
overclaiming machine record; implementers build from the JSON.

**Concrete consequence.** BC-018 requires the Turn Controller to reject
unverified capability reports, and `ControlDecision` carries the invariant "all
required capabilities verified." A `verified_available` scheduling capability
means the kernel authorizes a scheduling dispatch believing the capability is
proven. This is the precise false-determinism item BC-018 enumerated —
`CapabilityReport` schema is not capability availability — reappearing in the
first specialization of that contract. It is also the capability class with the
strongest false-claim history in this project: PARITY-012 forbids self-wake
claims, BC-017 records `F-REMINDER-WAKE`, and BEH-017's rationale is "Prompt
text must not masquerade as future execution."

**Scope of the harm, stated fairly.** This defect cannot produce a false
"reminder created" claim. `schedule.receipt` is correctly `unknown`,
`receipt_required` is `true` on all three rows, and the `side_effect_success_rule`
requires a provider receipt for operation success. The overclaim is confined to
capability availability, not operation completion. That is why the correction is
narrow — but capability availability is exactly what gates dispatch, so it is
still material.

**Nothing catches it.** The validator's scheduling-specific check
(`tools/validate_host_adapter_contracts.py:208-210`) requires only
`classes & STRONG_CURRENT_EVIDENCE`, which is the same test already applied to
every capability at line 201. It reads like a scheduling guard but adds no
constraint, and a `local_probe` satisfies it. By contrast the time-specific
check at lines 205-207 correctly demands `host_receipt`. The stricter pattern
already exists in the file; it was not applied where it was most needed.

**Required correction (not applied by this review).** Either downgrade the three
rows to `documented_possible` or `unknown`, recording interface exposure as a
limitation; or introduce a distinct capability such as
`schedule.interface_exposed` that states what was actually observed and downgrade
the three operational rows. Whichever is chosen, the scheduling validator check
should require evidence that genuinely bears on scheduling.

## Non-blocking notes

- **NN-1 — The validator cannot detect semantically irrelevant strong evidence.**
  It verifies only that a `verified_*` capability references *some* `local_probe`
  or `host_receipt` for that family. I confirmed the gap adversarially against a
  temporary copy: `action.git.push` marked `verified_available` citing the
  **current-time receipt** passes; `action.raw_network` marked
  `verified_available` citing the **web-search receipt** passes — the exact
  conflation the network contract forbids; and
  `security.attempt_count_integrity` flipped from `verified_unavailable` to
  `verified_available` on the security-*gap* probe passes. The evidence register
  already carries `supports[]` and `does_not_prove[]` on every entry, and they
  are never compared against the capability being claimed. A check requiring at
  least one referenced strong entry to `supports` a token mapped to the
  capability, and forbidding a claim contradicted by a referenced
  `does_not_prove` token, is implementable from data BC-020 already has — and
  would have caught BF-1, since `schedule_operation_success` is explicitly
  disclaimed. Recommended hardening, not a blocker in itself.

- **NN-2 — The scheduling validator check is a no-op duplicate.** Lines 208-210
  restate the general rule at line 201. It should either demand scheduling-bearing
  evidence or be removed, because as written it gives false assurance that
  scheduling claims receive extra scrutiny.

- **NN-3 — A documented scheduling limitation is missing from the Codex rows.**
  I verified `https://learn.chatgpt.com/docs/automations` directly: it documents
  that desktop-app scheduled tasks require the machine and app to remain powered
  on. The Chat side captures this (`CHAT-EVID-DOC-SCHEDULING.does_not_prove`
  includes `always_on_local_execution`). The Codex scheduling rows — on a
  *desktop* binding — record no equivalent limitation, though it bears directly
  on whether a future wake occurs. Add it whichever way BF-1 is resolved.

- **NN-4 — Parent/child Git status relationship should be stated.**
  `action.git.write` is `documented_possible` while its child
  `action.git.branch_create` is `verified_available`. This is the conservative
  and correct call — one verified write must not generalize — but the parent
  status could be misread as a ceiling on its children. One sentence resolves it.

- **NN-5 — Loose documentary provenance for two Chat rows.** `input.text` and
  `output.natural_language` cite `CHAT-EVID-DOC-PROJECTS` (a Projects page) as
  their documentary basis. The claims are not wrong, but the source is not
  on-point. Auditability would improve with a more directly relevant page.

- **NN-6 — Secondary evidence refs that disclaim the claim.**
  `action.artifact_create` and `output.structured_result` both carry
  `CODEX-EVID-PROBE-TOOLS` as a secondary reference whose `does_not_prove`
  includes `artifact_creation_success`. The primary receipts
  (`CODEX-EVID-RECEIPT-FILES`, `CODEX-EVID-RECEIPT-TURN`) genuinely carry these
  claims and the scopes are correct, so the records are sound — but the extra
  reference adds noise and would trip the NN-1 hardening check.

- **NN-7 — `output.external_side_effect_receipt` reads oddly.** It is
  `verified_available` while its evidence union's `does_not_prove` contains
  `external_side_effect` (from the read-only shell probe). The capability is
  *receipt availability*, which four real receipts do prove; the disclaimer is
  about the probe not having caused a side effect. Worth one clarifying word so
  the row is not misread as authorizing side effects.

- **NN-8 — Stale guardrail in `next_steps.md`.** Line 23 authoritatively states
  BC-020 is in `review`; the trailing standing-prohibition block still says "Do
  not begin successor design, BC-020, or BC-030." Both clauses about successor
  design and BC-020 are superseded. Per the review packet this is treated as
  non-blocking: the top-of-file statement governs, and the same sentence
  conditions everything on an approved packet and named base, so no action is
  ambiguously authorized. Untidy rather than contradictory.

- **NN-9 — Documentary URL/title provenance.** `https://learn.chatgpt.com/docs/artifacts-viewer`
  renders under the title "Work with files," which is what `CHAT-EVID-DOC-FILES`
  records. Provenance is intact and auditability is unaffected; noted only so a
  future reader does not mistake it for an error.

### Preserved unresolved declarations

- **SUR-011** remains open and untouched by BC-020, correctly. Protected maximum
  attempts, retry, lockout/backoff, cancellation/reset, new-request-after-
  exhaustion, and the effect of an unrelated intervening turn are all explicitly
  disclaimed in `authorization_transport_contract.json` and
  `sur012_disposition.json`.
- **SUR-012** is resolved at the generic host-evidence contract level only. No
  current surface supports protected cross-turn continuation.
- Chat current-binding availability remains `unknown` pending a future runtime
  self-report or host receipt.
- Codex client/surface version remains `unknown`; the version probe was denied
  and BC-020 correctly declines to infer a version from the package path.
- Codex `commit`, `push`, and `pr_operation` remain `unknown` in the substantive
  snapshot.
- Protected policy values, host-specific correlation and replay mechanics, and
  assurance thresholds remain unpublished.

## Answers to Q1-Q16

### Q1 — Does BC-020 distinguish product possibility from current-surface availability?

Yes, structurally and almost entirely in practice. The six-class evidence
hierarchy is explicit, `official_documentation` is defined as establishing
"possibility or limitation, not current binding availability by itself," the
`verified_available_rule` requires `local_probe` or `host_receipt`, and the
validator enforces both directions. `host_family` versus `surface_id` keeps
"ChatGPT can do X" separate from "this binding can do X now," and the Codex
snapshot rule states the observed binding "does not generalize to Codex as a
product or to another local, worktree, cloud, CLI, or IDE configuration."

The single failure is BF-1, and it is a variant of this exact confusion —
interface exposure treated as current availability.

### Q2 — Are Chat claims appropriately conservative given no live probe?

Yes. This is the strongest part of the document. Zero `verified_available` rows
across 52 capabilities; all fifteen security-matrix Chat cells are `unknown` or
`documented_possible`; every security capability is `unknown`.
`CHAT-EVID-NO-RUNTIME-PROBE` is registered as evidence class `unverified` and
states plainly that BC-020 ran from a Codex host without probing Dad's separate
Chat binding.

Nothing is inferred from the executing session, product branding, prior use,
documentation, Dad's account, or feature existence. The restraint extends
further than required — even `input.text` is only `documented_possible`, which
BC-020 could easily have waved through. There is no statement anywhere
conflating the reviewing session with the future Blu Host Adapter binding.

### Q3 — Are Codex verified-available claims properly scoped to the observed surface?

Yes, with BF-1 excepted. Every one of the 27 rows carries a `surface_scope`, and
the scopes are genuinely narrow rather than decorative: "BC-020 attachment
only," "approved BC-020 collision domain in workspace," "authorized origin
fetch/pull operations," "2026-08-08T23:05:40-05:00 provider result," "bounded
commands in workspace sandbox." The snapshot header repeats the rule, and each
strong evidence entry carries its own `scope` and `does_not_prove`.

I cross-checked all 27 rows against the `supports` lists of their referenced
strong evidence. Twenty-four are properly carried. The three scheduling rows are
not (BF-1).

### Q4 — Are the three verified scheduling-interface claims justified?

**No.** This is BF-1. Of the two interpretations the review packet posed, the
evidence supports the second: schema exposure is metadata and does not prove the
operation is actually usable. BC-020's own evidence register says so
(`supports: scheduling_interface_exposed`; `does_not_prove:
schedule_operation_success`), and BC-020 applies that reasoning to three other
capabilities evidenced by the same probe.

The classification materially overstates capability because
`verified_available` is defined as *usable* and is what gates Turn Controller
dispatch. It does not overstate operation success — `schedule.receipt` is
correctly `unknown` and `receipt_required` is `true` — so the correction is
confined to the three status values and their limitations.

### Q5 — Are filesystem, shell, Git, and network distinctions honest?

Yes, and they are the best-decomposed part of the Codex matrix.

**Filesystem:** six operations reported separately. `write` and `create` are
verified and scoped to the approved collision domain; `delete` and `rename` are
`unknown` because no such operation was performed; `read` is separately scoped.
`RECEIPT-FILES.does_not_prove` lists `filesystem_delete`, `filesystem_rename`,
and `unrestricted_filesystem`. `host_attachment`, `filesystem_object`, and
`external_source_object` are defined as distinct object kinds, so a Chat
attachment cannot become a filesystem path.

**Shell:** verified only for "bounded commands in workspace sandbox," with
`arbitrary_execution` explicitly disclaimed. All ten required report fields —
working directory, sandbox, approval, environment visibility, network policy,
timeout, exit code, stdout/stderr, side-effect limitations — are specified.

**Git:** eight capabilities classified independently. `repo_detected`,
`read`, `branch_create`, and `remote_access` verified and operation-scoped;
`commit`, `push`, `pr_operation` `unknown`. The rule "Local repository or commit
capability never implies remote, push, or PR capability" is stated and honored.

**Network:** `web_search`, `raw_network`, and `integration_call` are separate
classes. `action.raw_network` is `unknown` despite verified web search and
verified approved Git remote access, with the limitation stating exactly that
neither implies arbitrary outbound access. MCP/plugin exposure yields `unknown`
for `retrieval.integration_context`, not availability.

### Q6 — Are product sign-in, host approval, and Blu authorization cleanly separated?

Yes, and this separation is enforced in three places rather than asserted once.

The `sign_in_rule` states a signed-in ChatGPT or Codex user is not usable Blu
authorization evidence absent an interface exposing independently verifiable
identity, role, or credential evidence. Six forbidden inferences are enumerated:
tone, writing style, conversation history, model memory, private-fact knowledge,
and claimed account name. `adapter_authority` is `transport_only` and
`authorization_result_producer` is `authorization_evaluator`, preserving
BC-018/C1.

`HostApprovalEvidence` carries the rule "Host approval permits host transport
only. It never becomes AuthorizationResult or Blu authorization automatically,"
and the error mapping repeats that `approval_required` never becomes Blu
authorization. The observed binding demonstrates the distinction working:
`security.host_action_confirmation` is `verified_available` (a host approval
mechanism gated the Git operations) while `security.explicit_user_approval` is
`unknown` (the reviewer was automatic, so no human approval was observed). I
confirmed against current documentation that "Auto-review" is a real documented
reviewer mode distinct from user approval, and that changing the reviewer does
not expand the sandbox.

### Q7 — Is HostSessionEvidence strong enough to support the BC-018/C1 contract?

Yes. Its sixteen required fields cover every property C1's
`protected_cross_turn_resume_gate` demands: provider-bound identity, binding
method, state-record identity, scope, observation time, finite expiry, integrity
evidence, freshness evidence, replay evidence, rollback resistance, and a
receipt or evidence reference. `rollback_resistance` carries the exact four-value
vocabulary BC-018/C1 requires, and the resume gate requires
`security_grade`, which the capability contract defines as covering binding,
integrity, freshness/expiry, replay state, scope, and rollback-resistant attempt
state — with "Missing any property disqualifies this grade."

An opaque thread ID cannot qualify: the `truth_rule` names it explicitly
alongside conversation continuity, model memory, writing style, account-name
claims, and private-fact knowledge as forbidden constructions. The observed
Codex binding proves the gate bites rather than rubber-stamps — it returns
`verified_unavailable`.

### Q8 — Is SUR-012 genuinely resolved at the generic host-evidence level?

Yes, and the qualifier in the disposition string is doing real work. The test
the packet sets is whether Security Restraint can consume a normalized result
without knowing host-specific internals. It can: it receives normalized
availability, one of seven correlation classes, binding and scope, freshness and
expiry, replay state, integrity, and rollback evidence, with a single normalized
failure result (`insufficient_or_unavailable`) covering ten enumerated failure
conditions. No host-specific cryptography, token format, or session mechanism is
assumed.

The disposition explicitly does not claim any current host supports protected
continuation, and both surface dispositions say so: Chat `unknown`, observed
Codex `verified_unavailable`. `attempt_count_answer` states the attack directly
and disqualifies mutable client-local state. Eight forbidden substitutes are
enumerated.

Resolution at the contract level is the correct and honest scope of the claim.

### Q9 — Does BC-020 handle replay, freshness, and rollback resistance without inventing security state?

Yes. `replay_evidence` requires seven fields — request binding, event freshness,
prior consumption state, one-shot-or-reusable, detection capability, replay
status, provider evidence reference — with the rule that "A timestamp or
request-ref string alone does not prove replay prevention or prior-consumption
state." Correlation is separately governed: string equality is explicitly
insufficient, and the interface requires correlation "through provider evidence
rather than string equality."

Rollback resistance carries the required four-value vocabulary, and the
protected gate requires `monotonic_or_rollback_resistant`. The
`attempt_count_integrity` block lists six required properties, disqualifies
client-local mutable state, and sets `model_memory_fallback_allowed: false`. The
security matrix records the concrete consequence for the observed binding:
"Current binding cannot prevent a client reset from defeating the count."

Nothing is invented. Where evidence is absent, the result is `insufficient` and
protected continuation is unavailable.

### Q10 — Are the Codex `verified_unavailable` security claims justified as surface-scoped negatives?

Yes. All six capability rows and eleven security-matrix cells rest on
`CODEX-EVID-PROBE-SECURITY-GAP`, whose claim is scoped to "the adapter-visible
interface in this observed binding" and whose `does_not_prove` explicitly
includes `product_wide_unavailability` and `internal_account_authentication_state`.
Every consuming row repeats "current adapter-visible binding" in its
`surface_scope`.

A bounded negative probe is sufficient for this claim class specifically,
because the claim is about what the adapter can *see and consume*. If the
adapter-visible interface exposes no such provider record, the adapter genuinely
cannot obtain it — that is a verified negative for the adapter's purposes, and
it fails closed, so the error direction is safe. It never becomes "the Codex
product does not support this."

BC-020 also discriminates correctly at the boundary: `security.explicit_user_approval`
is `unknown` rather than `verified_unavailable`, because absence of use is not
absence of capability.

Worth recording: the negative side of this document is held to a *higher*
standard than the positive side. A bounded inspection finding nothing is
required for `verified_unavailable`, while mere schema exposure was accepted for
the scheduling `verified_available` rows. BF-1 is the asymmetry, not this.

### Q11 — Do HostActionReceipt and ArtifactReceipt prevent false side-effect success?

Yes. The `side_effect_rule` states an external side effect "is not completed
merely because it was requested, attempted, approved, or generated," which
covers all five items the packet lists including model request, generated
command, approval, and schema exposure. `HostActionReceipt` separates
`completed`, `failed`, `partial`, `unavailable`, and `denied`, and its
`policy_separation` clause prevents receipt status from becoming kernel PASS or
Blu authorization.

`ArtifactReceipt`'s six states separate `requested`, `attempted`, `created`,
`verified`, `failed`, and `unavailable`, with the rule that `created` requires
provider evidence, `verified` requires a bounded read/stat/hash/provider-object
check, and "A model-emitted filename is not evidence." `receipt_missing` is a
distinct normalized error mapping to UNAVAILABLE or ERROR, never to success.

Scheduling success specifically cannot be claimed: the `scheduling_rule` states
that create/update/cancel/recurrence success requires a provider schedule
receipt, and `schedule.receipt` is `unknown` on both families.

### Q12 — Is the evidence validator materially strong enough, and if not, is the weakness blocking?

Materially strong on evidence *class*; materially weak on evidence *relevance*.
The weakness is non-blocking on its own; BF-1 is blocking on its own merits.

Confirmed working (adversarially): a Chat security capability promoted to
`verified_available` on documentation alone is caught; `schedule.create`
promoted on documentation alone is caught; verified current time without a
`host_receipt` is caught. It also enforces required fields, non-empty
limitations, evidence-ref resolution, `documented_possible` requiring
documentation, golden checksums, and a protected-path diff.

Confirmed missing (all three passed validation): `action.git.push` marked
`verified_available` citing the current-time receipt; `action.raw_network`
marked `verified_available` citing the web-search receipt; and
`security.attempt_count_integrity` flipped from `verified_unavailable` to
`verified_available` on the security-gap probe. Any strong evidence entry for
the family satisfies the gate regardless of what it is evidence *of*, and
negative evidence can support a positive claim.

See NN-1 for the recommended hardening and NN-2 for the no-op scheduling check.

### Q13 — Has any Chat/Codex-specific assumption leaked into the generic BC-018 architecture?

No. `git diff --name-only d4157e7 ccf3206 -- kernel/golden contracts/ docs/architecture/` is
empty; `contracts/successor/**` and `docs/architecture/successor_*.md` are
untouched, and I re-ran the BC-018 validator and its 40 tests clean at this head.

The direction of dependency is correct: the adapter contracts reference
`contracts/successor/packet_registry.json#CapabilityReport` as a `repo_contract`
evidence entry and specialize it, rather than amending it. No vendor product
name appears in the generic kernel. `surface_identity_rule` states that "Generic
kernel packets consume normalized records and do not depend on vendor marketing
names," and every interface and adapter component retains
`host_specific: false` / `provider_binding: null`. Named integrations appear only
as discovery examples inside adapter records, never as kernel dependencies.

BF-1 is a Codex-matrix status error, not a generic-boundary leak.

### Q14 — Is BC-030 genuinely ready for specification?

```text
ready_for_spec
```

The reason BC-020 gives is the correct one and survives the specialization.
`host_session` and `durable_external` remain firmly distinct: the durability
boundary states "host_session is host-local cross-turn scope. It is never
durable_external continuity without an explicit continuity-provider operation
and receipt," and `continuity_rule` repeats it. No thread, project, chat, or
saved-memory concept is allowed to satisfy BC-030 — `session.durable_continuity`
is `unknown` on both families with the limitations "Thread/project/goal features
do not prove IF-CONTINUITY-PROVIDER receipts" and "Shared project context is not
a continuity-provider write receipt," and `session.saved_memory` is `unknown`
with "never security state."

BC-020 defines and implements no Local Mirror, and the continuity-provider
boundary is unchanged. BF-1 is in the scheduling family and does not touch
continuity.

### Q15 — Is there any capability status you would change before implementation?

Three, and only three: `schedule.create`, `schedule.recurring`, and
`schedule.update_cancel` on Codex, from `verified_available` to
`documented_possible` or `unknown` — or, preferably, split so that a distinct
`schedule.interface_exposed` capability carries the observation that was
actually made. See BF-1.

I would change nothing else. I examined all 27 Codex `verified_available` rows
and all 6 `verified_unavailable` rows against their evidence, and every other
status is proportionate. The Chat matrix needs no status changes.

### Q16 — Is there any missing host-evidence boundary that would force the implementer to guess?

No boundary is missing. The nine capability families, six evidence classes, five
freshness scopes, five security grades, seven correlation classes, fifteen
normalized host errors, three receipt types, and the host-session and
authorization-transport records collectively cover what an adapter implementer
must report. Where a value cannot be known, the vocabulary provides `unknown`
and the `unknown_field_rule` forbids fabricating precision.

Two smaller gaps are worth naming, both non-blocking. First, the self-report
handshake specifies *when* to refresh capability evidence and *what* to cache,
but not who arbitrates a conflict between a cached record still inside its
freshness boundary and a fresh provider denial — the `stale_evidence` error
exists, but precedence is unstated. Second, an implementer following the
scheduling rows as written would treat scheduling as verified and discover the
gap at runtime; that is BF-1, not a missing boundary.

## Judgments

### Chat-evidence judgment

Exemplary. 52 capabilities, 18 `documented_possible`, 33 `unknown`, 1
`not_applicable`, 0 `verified_available` — counts independently confirmed. Nine
evidence entries: one `repo_contract`, seven `official_documentation`, one
`unverified`. Every documentary claim stays documentary. No inference from the
executing session, branding, prior use, account, or feature existence anywhere
in the file.

### Codex-evidence judgment

Strong and properly bounded, with one defect. 52 capabilities — 27
`verified_available`, 6 `verified_unavailable`, 4 `documented_possible`, 14
`unknown`, 1 `not_applicable` — counts independently confirmed. 21 evidence
entries: 1 `repo_contract`, 9 `official_documentation`, 4 `local_probe`, 7
`host_receipt`. Every row is surface-scoped to
`codex_desktop_local_windows`, and no statement generalizes to Codex as a
product. Twenty-four of 27 verified rows are genuinely carried by their
evidence; the three scheduling rows are not.

### Scheduling-interface judgment

The exposed automation interface supports a claim of *interface exposure*, which
is what BC-020's prose and handoff say. It does not support `verified_available`
on capability IDs that denote operations. The machine-readable matrix overstates
what the evidence register itself is willing to assert. Blocking; narrowly
correctable.

### SUR-012 judgment

`resolved_at_generic_host_evidence_contract_level` is warranted and the qualifier
is accurate. The required evidence contract, normalized failure behavior, and
correlation vocabulary are complete enough for Security Restraint to consume
without host-specific knowledge. It correctly claims nothing about current
surface support, and both surfaces are recorded as unable to support protected
continuation today.

### SUR-011 separation judgment

Cleanly preserved. BC-020 supplies correlation evidence and explicitly declines
policy in two contracts and in `next_steps.md`. It does not decide the effect of
`same_host_session_uncorrelated`, nor publish maximum attempts, retry,
lockout/backoff, cancellation/reset, or new-request-after-exhaustion policy. The
seven correlation classes are mutually understandable and sufficient for a future
Security Restraint policy to act on.

### Evidence-validator judgment

Adequate for structure and evidence class; inadequate for evidence relevance.
Three demonstrated misses, all in the direction of permitting overclaim. The
data needed to harden it already exists in every evidence entry. Non-blocking as
a validator issue; recommended before implementation.

### Implementation eligibility judgment

**Not eligible.** BC-020 is a specification-only artifact and correctly contains
no adapter implementation: the only Python added is the validator and its tests,
and `adapters/**` contains no executable code. No MCP server, plugin, runtime
detector, Auth or session store, scheduler, Local Mirror, or kernel code appears
anywhere in the diff.

Beyond that, no current surface supports protected cross-turn continuation, Chat
availability is entirely unknown, and SUR-011 remains an open security-policy
input. Implementation requires separate authorization regardless of this
review's outcome.

## Validation review

Re-run independently at the reviewed head:

```text
runtime contract validator: passed          contract tests: Ran 21, OK
viability tests: Ran 9, OK                  historical inventory tests: Ran 12, OK
historical archaeology tests: Ran 18, OK    successor kernel tests: Ran 40, OK
host adapter contract validator: passed     host adapter tests: Ran 25, OK
golden CTS SHA-256: 8/8 passed
canonical manifest: 216 entries, self-excluded, 216 tracked, 0 missing, 0 extra, 0 mismatch
protected generic/current paths changed (kernel/golden, contracts/, docs/architecture/): 0
Chat: 52 capabilities / 18 documented_possible / 33 unknown / 1 not_applicable / 0 verified_available; 9 evidence entries
Codex: 52 capabilities / 27 verified_available / 6 verified_unavailable / 4 documented_possible / 14 unknown / 1 not_applicable; 21 evidence entries
Security matrix: 15 rows (Chat 13 unknown + 2 documented_possible; Codex 11 verified_unavailable + 2 unknown + 2 verified_available)
```

Every figure Codex reported matches. The manifest was verified independently
against staged Git-blob bytes rather than by re-reading the recorded result, and
`.gitattributes` is present — the coverage gap I raised as NN-1 in the BC-018-C1
review is closed.

I also verified the material first-party documentation directly rather than
trusting the citations, since product behavior is current and unstable:

| URL | Status | Supports the recorded claim? |
|---|---|---|
| `learn.chatgpt.com/docs/automations` | live | Yes — recurrence, management, run history, surface variability all documented |
| `learn.chatgpt.com/docs/sandboxing` | live | Yes — sandbox and approval documented as distinct controls |
| `learn.chatgpt.com/docs/permission-modes` | live | Yes — `workspace-write` and Auto-review are documented terms; reviewer change does not expand sandbox |
| `learn.chatgpt.com/docs/computer-use` | live | Yes — separately installed, permissioned plugin, supported regions/surfaces, GUI operation |

`learn.chatgpt.com` is a genuine first-party domain and the pages are public,
primary, and scoped. No current documentation contradicts a BC-020 documentary
claim. One page surfaced a limitation BC-020 records for Chat but not for Codex
(NN-3).

Passing validation is not evidence of real provider capability, and it is not
evidence of semantic correctness here in particular: BF-1 passes every existing
check, and the three demonstrated relevance misses in NN-1 pass as well.

## Required follow-up

Dad and Blu decide integration, correction, and closure. BC-020 is **not**
marked done by this review.

Recommended: authorize a narrow BC-020 correction addressing BF-1, and fold
NN-2 and NN-3 into the same pass since all three concern the same three rows.
NN-1 is the one item worth doing before any adapter implementation begins,
because it is the check that would have caught BF-1 mechanically. NN-4 through
NN-9 are cleanups.

Do not begin BC-030 or runtime implementation.

## Final status authorization

- Authorized by: pending Dad/Blu decision after review
- Assignment status: review
- Reviewer disposition: return-for-correction
- Date: 2026-08-08
