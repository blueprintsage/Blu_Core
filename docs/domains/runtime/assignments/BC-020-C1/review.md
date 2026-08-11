# BC-020-C1 — Review Record

status: reviewed
review_state: complete
owner: Claude
last_reviewed: 2026-08-09
assignment: BC-020-C1
parent_assignment: BC-020

## Review identity

- Review date: 2026-08-09
- Reviewer: Claude
- Review type: independent read-only semantic correction re-review
- Review branch: `bc-020-c1-semantic-review`
- Exact reviewed head: `8eb29165d5d59b99ccaa3b06fe6d8613dcaa11e2`
- Reviewed base: `370278cd91fd9ecca2c64cd0953cae7ed63c4d16`
- Substantive correction commit: `b770be849d625e924f7e65cae4efb8894a7e4c23`
- Metadata commit: `8eb29165d5d59b99ccaa3b06fe6d8613dcaa11e2`
- Parent review returning BF-1: BC-020 `review.md` at `ccf3206ad033d588246e09001d47ddce3ac50a31`
- Integration commit or merge identity: none

## Disposition

```text
approve-with-notes
```

BF-1 is fully resolved. The three operational Codex scheduling capabilities are
`unknown`, the exposed automation interface survives as an observation rather
than as proof of availability, and the corrected limitations name every property
interface exposure fails to establish. The validator hardening does what NN-1
and NN-2 asked for and, importantly, **fails closed**: a `verified_available` or
`verified_unavailable` capability with no curated support profile is now an
error rather than a pass. I reproduced every reported validation result
independently and confirmed all three rejection classes adversarially against a
working copy.

No blocking findings. Seven non-blocking notes follow. None of them require
rework before integration; NB-1 and NB-2 are the two a project lead should read
before closing BC-020.

## Blocking findings

None.

## Answers to the review questions

### Q1 — Is original BF-1 fully resolved?

**Yes.** BF-1 was that `schedule.create`, `schedule.recurring`, and
`schedule.update_cancel` were `verified_available` on `CODEX-EVID-PROBE-TOOLS`
alone, an evidence entry whose own `supports` list said only
`scheduling_interface_exposed` and whose `does_not_prove` list contained
`schedule_operation_success` and `external_account_connection`.

All three rows are now `unknown`. The evidence register entry is unchanged in
its scheduling semantics — it still supports only `scheduling_interface_exposed`
and still disclaims operation success — so the contradiction between the
capability rows and their own evidence annotation is gone. The correction also
addressed the three coupled non-blocking items the original review named as the
same defect class: NN-1 (semantic relevance, now enforced), NN-2 (the no-op
scheduling check, now a real constraint), and NN-3 (the missing documented
desktop limitation, now recorded).

The correction was reached by downgrade rather than by introducing a separate
`schedule.interface_exposed` capability. Both options were offered; the downgrade
is the more conservative of the two and does not add a capability ID a consumer
could misread.

### Q2 — Are all three scheduling capabilities correctly classified as `unknown`?

**Yes.** Read directly from `adapters/codex/capability_matrix.json` at the
reviewed head:

| Capability | Status | Evidence refs |
|---|---|---|
| `schedule.create` | `unknown` | `CODEX-EVID-PROBE-TOOLS`, `CODEX-EVID-DOC-SCHEDULING` |
| `schedule.recurring` | `unknown` | `CODEX-EVID-PROBE-TOOLS`, `CODEX-EVID-DOC-SCHEDULING` |
| `schedule.update_cancel` | `unknown` | `CODEX-EVID-PROBE-TOOLS`, `CODEX-EVID-DOC-SCHEDULING` |
| `schedule.receipt` | `unknown` | `CODEX-EVID-PROBE-TOOLS` |

Each of the three operational rows carries a limitation naming, explicitly, that
interface exposure does not prove provider/account connection, required
permission, operational usability, the successful operation, future execution,
or receipt availability. `receipt_required: true` and
`security_relevance: high` are retained on all four rows. The interface
observation itself is preserved in `surface_scope` ("current exposed Codex app
automation interface" and variants) and in the first clause of each limitation,
so nothing observed was discarded to reach the correction.

Corrected totals independently recomputed from the matrix: 52 capabilities — 24
`verified_available`, 6 `verified_unavailable`, 4 `documented_possible`, 17
`unknown`, 1 `not_applicable`; 22 Codex evidence entries. These match the
reported figures exactly.

### Q3 — Does the validator reject interface/schema exposure as sufficient evidence?

**Yes.** Confirmed adversarially, not merely by reading the code. Against a full
temporary copy of the tree I promoted each row in turn and ran `validate()`:

| Mutation | Result |
|---|---|
| `schedule.create` → `verified_available`, refs `[CODEX-EVID-PROBE-TOOLS]` | rejected — "lacks semantically relevant current evidence" + "verified scheduling lacks operational evidence" |
| `schedule.recurring` → same | rejected, both errors |
| `schedule.update_cancel` → same | rejected, both errors |
| `schedule.create` → `verified_available` citing **every** strong Codex entry (tools probe, Git receipt, time receipt, shell probe, files receipt, turn receipt) | rejected, both errors |

The mechanism is sound. `VERIFIED_CAPABILITY_SUPPORTS` requires the token
`schedule_create_available` (and the recurring/update-cancel equivalents), and no
evidence entry in the register supplies any of them — correctly, because no such
operation was performed. Piling on unrelated strong evidence does not help,
which is the property that matters: the old check could be satisfied by any
`local_probe`, so quantity of evidence substituted for relevance.

The scheduling-specific block at `tools/validate_host_adapter_contracts.py`
is now a genuine constraint rather than the duplicate of the general rule that
NN-2 flagged. It is narrower than the general check (it does not consult
`does_not_prove`), but the general check runs on the same row and is strictly
stronger, so combined behavior is correct.

### Q4 — Does the validator reject semantically unrelated strong evidence?

**Yes.** Confirmed adversarially against the same defect cases the original
review used to demonstrate the gap:

| Mutation | Old behavior (BC-020) | New behavior |
|---|---|---|
| `action.git.push` → `verified_available` citing `CODEX-EVID-RECEIPT-TIME` | passed | rejected |
| `action.raw_network` → `verified_available` citing `CODEX-EVID-RECEIPT-WEB` | passed | rejected |
| `action.git.push` → `verified_available` citing `CODEX-EVID-RECEIPT-GIT` (which disclaims `push`) | passed | rejected |

The third case is worth naming separately: the Git receipt is the *most*
on-topic strong evidence available for a Git capability, and it is still
correctly refused for `push`, because the curated profile demands the `push`
token and `CODEX-EVID-RECEIPT-GIT` supports only `repo_detected`, `git_read`,
`branch_create`, `remote_access_operation_scoped`, and `host_action_confirmation`.
Family adjacency does not substitute for the specific claimed operation. Refs
pointing at another family's evidence register are also rejected (unknown-ref
error plus both relevance errors).

### Q5 — Does the validator reject opposite-polarity evidence?

**Yes**, and by two independent mechanisms.

Positive-token separation: `security.attempt_count_integrity` requires
`attempt_count_integrity` when `verified_available` and
`attempt_integrity_unavailable` when `verified_unavailable`.
`CODEX-EVID-PROBE-SECURITY-GAP` supplies only the negative tokens. Flipping the
row to `verified_available` on that probe is rejected. The same separation holds
for `session.host_session_binding`, `session.cross_turn_security_correlation`,
`security.identity_role_credential_evidence`, and `security.replay_evidence`,
all of which are `verified_unavailable` on negative tokens only.

Contradiction guard: I tested the `does_not_prove` path directly by adding
`push` to `CODEX-EVID-RECEIPT-GIT.supports` while leaving `push` in its
`does_not_prove`. The row is still rejected — a self-contradicting entry cannot
carry a claim. I also tested adding a fabricated `schedule_create_available`
token to the tools probe: still rejected, because the probe's existing
`does_not_prove` disclaimers (`external_account_connection`,
`write_authorization`, `schedule_operation_success`) are mapped as disclaimers
for the scheduling profiles. That is real defense in depth on the highest-risk
capability class. See NB-2 for the residual boundary.

### Q6 — Do previously valid, truthfully supported verified rows still validate?

**Yes.** The full validator passes clean at the reviewed head with zero errors,
and all 30 `verified_*` rows (24 available, 6 unavailable) satisfy the new
semantic requirement. I re-walked each row against the `supports` list of its
referenced strong evidence; every one has at least one entry that genuinely
bears on the claim.

Two rows deserve a note rather than a finding, and both predate C1 — see NB-3.

The one place C1 widened evidence semantics to keep a row passing is
`CODEX-EVID-RECEIPT-GIT`, which gained `host_action_confirmation` — see NB-1.

### Q7 — Are the receipt and completion distinctions preserved?

**Yes, entirely.**

- `schedule.receipt` remains `unknown` with the limitation that schema exposure
  does not prove the normalized provider receipt returned after success.
- `side_effect_success_rule` is unchanged: "A side-effect capability may be
  available, but a particular operation is completed only by an appropriate
  HostActionReceipt or provider evidence."
- `receipts_and_failures.md` is untouched by C1 and still carries the
  `requested` / `attempted` / `created` / `completed` artifact-state
  distinction, the `completed` / `failed` / `partial` / `unavailable` receipt
  status vocabulary, the rule that no side effect is completed because a model
  requested it or the adapter attempted it, and the requirement that scheduling
  receipts carry provider schedule identity, normalized schedule, operation,
  result, and limitations.
- `receipt_required: true` is retained on all four scheduling rows.

A model request, a generated command, an exposed schema, a host approval, and an
attempted invocation each remain distinct from a completed operation, and none
of them is treated as capability availability. The correction actually
strengthens this: previously the availability layer overclaimed while the
completion layer held; now both layers are honest, and the distinction no longer
has to carry the weight of a wrong row above it.

### Q8 — Is the desktop scheduling limitation correctly scoped?

**Yes.** The limitation is worded "For documented desktop scheduled tasks only,
future local execution may depend on the relevant machine and app remaining
powered on and available," and the qualifier appears in all three places it
occurs: the three matrix rows, `codex_adapter.md`, and the new evidence entry.

`CODEX-EVID-DOC-SCHEDULING` is registered as `official_documentation` with
`scope: "documented desktop scheduled-task execution limitation only"`, a
limitation stating it "does not establish that the observed Codex binding has a
connected, permitted, or usable scheduling provider," `supports:
[desktop_schedule_execution_dependency]`, and `does_not_prove:
[current_codex_scheduler, schedule_operation_availability,
schedule_operation_success, schedule_receipt]`.

Nothing generalizes it to cloud, CLI, IDE, or worktree Codex surfaces. The
entry is documentation-class and therefore cannot produce `verified_available`
under the unchanged rule, and it appears only on rows that are `unknown`, so it
carries a limitation without carrying a claim. This is the correct shape for
NN-3.

### Q9 — Did C1 leave the protected boundaries untouched?

**Yes.** Verified by exact-base diff from `370278c` to `8eb2916` rather than by
assertion. The complete changed-path set is 17 files, all inside the declared
collision domain. The following paths have an **empty** diff:

- `kernel/` — including `kernel/golden/`
- `contracts/` — including `contracts/successor/` and `contracts/runtime/`
- `docs/architecture/` — all four successor documents
- `docs/domains/runtime/assignments/BC-020/` — Claude's original review is
  byte-identical

Counts read from the untouched registries: **7** successor components, **8**
packets, **9** interfaces, **1** state record. `PendingAuthorizationState`
remains a state record. SUR-011 is unchanged and still open, with its
uncorrelated-intervening-turn question intact and `blocking_for_BC020: false`;
SUR-012 is unchanged and still scoped to the generic host-evidence contract,
with `blocking_for_BC020: true`. Neither was decided by C1, and the corrected
Codex matrix continues to report the security capabilities as
`verified_unavailable` for the observed binding — which is the honest input to
SUR-012, not a resolution of it.

I scanned the full diff for `mega-Exec`, `Exec Library`, `School Engine`, `MMU`,
`Mood service`, `SecuritySessionManager`, and `AuthSessionManager`: zero
additions. No eighth component appears anywhere.

Also confirmed:

- **No adapter runtime implementation.** `adapters/` contains zero `.py` files.
- **No successor Python runtime.** The repository's only `.py` files remain
  under `tools/` (validators) and `tests/`. C1 added no source file outside
  those two trees.
- **No real scheduling operation was performed.** Consistent with the evidence
  register, which still records no operational scheduling evidence.

### Q10 — Is BC-020 ready for integration/closure?

**From the semantic-correctness standpoint, yes.** The single blocking finding
that produced `return-for-correction` is resolved, the defect class behind it is
now mechanically prevented and fails closed, and nothing outside the narrow
correction moved. I hold no integration or merge authority; Dad or Blu decides.

Two process observations for whoever closes it, neither semantic: the C1 handoff
still records "Push status: pending" although `origin` carries the branch at the
reviewed head (NB-6), and six non-blocking notes from the original BC-020 review
were out of C1's authorized scope and remain open (NB-7).

## Independent validation

I ran every reported check myself at the reviewed head on a clean tree. All
reported figures reproduce exactly.

```text
runtime contract validator:      passed
runtime contract tests:          Ran 21, OK
viability validator:             passed
viability tests:                 Ran 9,  OK
historical archive tests:        Ran 12, OK
historical archaeology tests:    Ran 18, OK
successor kernel validator:      passed
successor kernel tests:          Ran 40, OK
host adapter validator:          passed
host adapter tests:              Ran 34, OK
```

Golden CTS, recomputed SHA-256 over every file named by
`kernel/golden/v0.22.0/SHA256SUMS`:

```text
golden checked: 8
golden failed:  0
```

Canonical manifest, recomputed against staged Git blob bytes:

```text
manifest entries:  220
tracked expected:  220
missing:  0
extra:    0
mismatch: 0
```

Adversarial validator probes against a temporary full-tree copy (baseline: zero
errors):

```text
interface-only -> schedule.create verified          rejected
interface-only -> schedule.recurring verified       rejected
interface-only -> schedule.update_cancel verified   rejected
all strong evidence -> schedule.create verified     rejected
time receipt -> action.git.push verified            rejected
git receipt -> action.git.push verified             rejected
web receipt -> action.raw_network verified          rejected
security-gap -> positive attempt integrity          rejected
contradictory supports+does_not_prove entry         rejected
cross-family evidence ref on verified row           rejected
unmapped capability -> verified_available           rejected (fails closed)
unmapped capability -> verified_unavailable         rejected (fails closed)
```

The last two lines are the property I consider most valuable in this correction
and it was not in the required-test list: a future capability promoted to a
verified status without an explicit support profile is refused rather than
waved through. The hardening protects claims nobody has written yet.

## Non-blocking notes

- **NB-1 — One evidence entry's semantics were widened to keep a row passing.**
  C1 added `host_action_confirmation` to `CODEX-EVID-RECEIPT-GIT.supports`. It
  is the only change to an existing evidence entry's meaning in this correction,
  and without it `security.host_action_confirmation` would have failed the new
  check. The addition is defensible on the record: the entry's own source
  description says the Git operations were an "authorized origin fetch and
  fast-forward pull," its claim says "under approval," and
  `CODEX-EVID-PROBE-SURFACE` independently records `approval_mode`. The row's
  status did not change and the original review already accepted it (Q6 of the
  BC-020 review cites it approvingly as proof the sign-in/approval/authorization
  separation works). So this is a token made explicit, not a claim invented.
  Flagged only because "add a support token to an existing entry" is the exact
  motion that could be used to defeat the new check, and it should be a
  deliberate, reviewed act every time — as it was here.

- **NB-2 — The residual trust boundary is the evidence author, and it now has a
  named shape.** I confirmed that a claim can still be promoted if an author both
  adds a fabricated support token *and* strips the contradicting
  `does_not_prove` entries: adding `schedule_create_available` to the tools probe
  alone is rejected, but adding it while also removing the three scheduling
  disclaimers is accepted. This is inherent — the validator checks contract
  consistency, not truth, and `failures.md` correctly warns against replacing it
  with free-form inference. The useful consequence is narrower than a defect:
  **removing a `does_not_prove` token is a governance-significant edit**, because
  those tokens are now load-bearing rather than documentary. Worth one sentence
  in `host_capability_truth.md` at some future opportunity, not here.

- **NB-3 — Two curated profiles are looser than the rest.**
  `retrieval.filesystem_read` is satisfied by `filesystem_scope` (surface
  metadata declaring a writable root) or `working_directory` (a shell probe
  field) — neither of which is literally a read receipt, though the shell probe
  did read repository state, and `CODEX-EVID-RECEIPT-ATTACHMENT` is also
  referenced on the row. `output.structured_result` is satisfied by
  `structured_tool_result_input`, an input-side token carrying an output-side
  capability. Both rows predate C1 and neither status changed, so this is not a
  new overclaim; the note is that the profile map now *blesses* the two
  conflations rather than leaving them unexamined. If either capability is ever
  tightened, these are the two profiles to revisit. Related: NN-6 from the
  original review anticipated that the hardening might trip
  `action.artifact_create` and `output.structured_result` on their secondary
  `CODEX-EVID-PROBE-TOOLS` reference. It does not — the check requires only that
  *at least one* referenced strong entry be relevant and non-disclaiming, which
  is the right design — but `output.structured_result` is now carried by the
  tools probe as well as by the turn receipt, which is the looser of the two.

- **NB-4 — `output.external_side_effect_receipt` still reads oddly, as NN-7
  said.** Its profile accepts `exit_code_receipt` from the read-only shell probe,
  whose own `does_not_prove` contains `external_side_effect`. The disclaimer does
  not fire because the token vocabularies differ (`external_side_effect` is not
  in the expected set). The row is independently and genuinely carried by
  `remote_access_operation_scoped` from the authorized origin fetch/pull, so the
  claim is sound and this is not a defect — but the shell-probe path is the one
  loose match in an otherwise tight profile.

- **NB-5 — Manifest verification is blob-normalized; do not read a working-tree
  check as corruption.** `MANIFEST.sha256` is computed over staged Git blob
  bytes. Verifying it against Windows working-tree bytes reports 86 differences
  purely from CRLF translation; against blob bytes it is 220/220 clean. This is
  stated in `validation.md` and is pre-existing repository practice, recorded
  here so a future reviewer who checks the fast way does not raise a false alarm.

- **NB-6 — The C1 handoff Git status is stale, in the safe direction.** It
  records "Push status: pending" and "final Git receipts pending", but `origin`
  carries `bc-020-c1-scheduling-evidence-correction` at
  `8eb29165d5d59b99ccaa3b06fe6d8613dcaa11e2`. The record understates what
  happened rather than overstating it, which is the correct failure direction
  under `AGENTS.md`, but the branch-push completion condition is in fact
  satisfied and the packet does not say so.

- **NB-7 — Original review notes NN-4, NN-5, NN-7, NN-8, and NN-9 remain open.**
  All were outside C1's authorized scope and correctly untouched. NN-8 in
  particular is still visible: the trailing standing-prohibition block in
  `next_steps.md` still reads "Do not begin successor design, BC-020, or
  BC-030," while the top of the same file now records BC-020-C1 in review. As
  the original review said, the top-of-file statement governs and the trailing
  sentence conditions everything on an approved packet and named base, so this
  is untidy rather than contradictory. These are carry-forward items for BC-020
  closure or a later tidy-up, not C1 defects.

### Preserved unresolved declarations

- **SUR-011** remains open and untouched. C1 decided no policy on maximum
  attempts, lockout/backoff, cancellation/reset, new-request-after-exhaustion,
  or the disposition of an uncorrelated intervening turn.
- **SUR-012** remains resolved only at the generic host-evidence-contract level.
  The corrected Codex matrix continues to report `verified_unavailable` for
  host session binding, cross-turn security correlation, pending-request
  correlation, replay evidence, and attempt-count integrity on the observed
  binding, and Chat remains entirely `unknown` — so nothing in C1 implies that
  either surface currently supplies sufficient evidence for protected cross-turn
  authorization continuation.
- Operational Codex scheduling availability and the normalized schedule receipt
  shape remain `unknown` pending a future authorized operation that produces
  provider evidence.
- Codex `commit`, `push`, and `pr_operation` remain `unknown`.
- Chat current-binding availability remains `unknown`; no Chat probe was run by
  C1 or by this review.

## Review boundary

This review inspected repository state at
`8eb29165d5d59b99ccaa3b06fe6d8613dcaa11e2` and ran the repository's validators,
unit tests, golden checksum verification, manifest verification, and my own
adversarial validator mutations against a temporary copy. No file in the
repository was modified by this review except this record. No merge, push, tag,
or integration was performed.

Static validation proves repository contract consistency. It does not prove
provider connection, permission, operational usability, successful scheduling
operations, future execution, or receipt integrity — and the corrected contract
now says so in the matrix rather than only in prose. I did not re-fetch
`https://learn.chatgpt.com/docs/automations`; I verified that page directly
during the original BC-020 review, and the limitation it supports sits on rows
that are `unknown`, where documentation-class evidence cannot promote a claim.

## Required follow-up

Dad or Blu decides integration and closure. This record carries no integration
or merge authority. Do not close BC-020, start BC-030, begin Chat live-probe
work, or begin runtime implementation from this review.
