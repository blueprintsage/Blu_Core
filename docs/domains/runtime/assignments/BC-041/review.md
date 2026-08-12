# BC-041 — Review Record

status: reviewed
owner: Claude
last_reviewed: 2026-08-11

## Review identity

- Assignment: BC-041
- Reviewed base: `699ee1485cef39ffbe70c3b8e848763af02596e0`
- Reviewed work commits: `9ccd17d75955db4b64e5df27a5751d36b6964330` (substantive),
  `9849c60138940068a0fd900eb49ce7444531109d` (metadata receipt)
- Review branch: `bc-041-semantic-review`
- Reviewer: Claude
- Review type: independent semantic security-contract review
- Integration commit or merge identity: none

## Required review focus

Determine whether the public contract genuinely resolves SUR-001 at the bounded
Phase 1 level; remains mandatory pre-ingress; keeps Auth separate; fails closed
for every unusable policy state; prevents protected ingress reaching the model
and protected egress reaching print; keeps redaction deterministic and
non-leaking; keeps evidence/logs content-safe; uses genuinely synthetic
fixtures; states the semantic-paraphrase limit honestly; makes the policy
reference portable and opaque; preserves 7/8/9 and SUR-002/SUR-011/SUR-012; and
introduces zero production runtime code.

## Findings

### Blocking

**B-1 — The normalization pipeline does not neutralize Unicode format
characters, so a one-character insertion defeats the ingress boundary.**

`minimum_contract.json#normalization.ordered_steps` and
`tools/validate_opsec_contracts.py:72` (`normalize_text`) apply NFKC, whitespace
and line-break collapse, and bounded separator collapse. None of those steps
touches Unicode general-category `Cf` (format / default-ignorable) code points.
NFKC preserves them. `str.isspace()` is `False` for them, so the whitespace step
does not catch them, and they are not in the `SEPARATORS` set.

Observed against the shipped harness and the synthetic policy, inserting a
single format character into the protected phrase — either between two words or
inside one word — yields `SecurityDecision = PASS`:

```text
cerulean<U+200B>comet charter   ZERO WIDTH SPACE       -> PASS
cerulean co<U+00AD>met charter  SOFT HYPHEN            -> PASS
cerulean<U+200D>comet charter   ZERO WIDTH JOINER      -> PASS
cerulean<U+200C>comet charter   ZERO WIDTH NON-JOINER  -> PASS
cerulean<U+FEFF>comet charter   ZERO WIDTH NO-BREAK    -> PASS
cerulean<U+2060>comet charter   WORD JOINER            -> PASS
```

This is not the semantic-paraphrase class the contract honestly disclaims. It is
byte-for-byte the protected phrase with an invisible character added, and it is
the "trivial formatting bypass" that the assignment's Text Normalization section
requires the pipeline to prevent and that its Bypass / Robustness Tests section
asks to be exercised. The gap is in the normative `ordered_steps` list, not only
in the harness, so a Phase 1 runtime implementing the contract verbatim
reproduces it. The same gap applies symmetrically at egress, though it is far
less likely to be reached there because the local model would have to emit the
format characters itself.

The class is deterministically closable, so the assignment's "fail honestly
rather than advertise protection you cannot provide" escape does not apply —
the correct outcome is to close it, not to document it.

Recommended remedy, verified against the shipped harness and fixtures. A single
transform cannot serve both positions: mapping `Cf` to space repairs a format
character *substituted for* a space but splits a word when one is inserted
*inside* it; dropping `Cf` does the reverse. Evaluating both bounded variants
and matching if either matches is still fully deterministic:

1. add a normalization step producing two candidate views — `Cf` mapped to
   ASCII space, and `Cf` removed — each then run through the existing pipeline;
2. treat the input as matched if either view matches;
3. record the step in `minimum_contract.json#normalization.ordered_steps` and in
   `contracts/security/opsec/README.md`;
4. add ingress and egress fixtures for the six forms above in both positions.

With that change all twelve probes return `BLOCK`, and every existing ingress
and egress fixture — including all five negative cases — retains its expected
result. No false positive was introduced.

Because `python_phase1_readiness_checklist.json` has already been flipped to
`ready_for_python_phase1` on the strength of this mechanism, this should be
corrected before the runtime packet is authored rather than carried as a note.
Approving green readiness over a known trivially-exploitable ingress bypass is
the "middle state that falsely authorizes coding" the assignment prohibits.

### Non-blocking

**N-1 — Redaction canonicalizes the whole message, so a redacted reply prints
as punctuation-stripped prose.** `evaluate_egress` builds `public_output` from
the *normalized* candidate, and normalization maps `.`, `,`, `-`, `_`, `/`,
`\`, `|`, `:`, `;` to spaces across the entire message, not just the removed
span. Observed:

```text
in:  Hello, world! Before cerulean comet charter -- after.
out: Hello world! Before [protected content omitted] after
```

This is a stated design choice (`redaction.public_form`) and it is safe — it
avoids raw-span mapping bugs — but it is a user-visible degradation that the
contract does not spell out. The Phase 1 runtime author should know that any
redacted reply reaches the terminal with its punctuation destroyed. Consider
either mapping spans back onto the raw candidate, or declaring that a
degraded-prose result is preferable to `BLOCKED` and saying so explicitly.

**N-2 — `independent_Claude_review_required` is still `pass` while the review is
pending, and the stakes are now higher.** This is a recurrence of BC-040 N-7,
unaddressed. At BC-040 the surrounding aggregate was
`not_ready_for_python_phase1`, so the ambiguity was inert. BC-041 flips the
aggregate to `ready_for_python_phase1` in the same commit whose `review.md`
reads `status: review-needed`. Read as "a review is required" it remains true;
read in context it can be mistaken for "this change was reviewed." Recommend a
distinct status such as `required_pending`, or a per-assignment review field.

**N-3 — The readiness validator's overclaim guards were inverted rather than
extended.** `test_readiness_cannot_overclaim_authorization` became
`test_readiness_cannot_retain_stale_blocker_state`, and
`validate_python_readiness.py` now *requires* `ready_for_python_phase1` and
`runtime_phase1_packet_may_be_authored_next: true`. This matches the repository
convention of pinning exact expected state, and `automatic_start_prohibited`
plus `implementation_authorized: false` are still asserted. But the checklist
validator no longer independently resists an overclaim; that duty now rests
entirely on the SUR-001 disposition checks and `validate_opsec_contracts.py`.
Worth stating in the runtime packet so the guard's meaning is not misread.

**N-4 — The continuity-validator SUR-001 exception does not pin field
removal.** `_is_authorized_bc041_sur001_update` requires every other register
item to be byte-identical and pins `disposition`, `resolution_record`,
`blocking_for_implementation`, and six preserved fields. It does not object to
new fields appearing on SUR-001 or to the removal of
`what_future_assignment_can_resolve_it`, which BC-041 did remove. The exception
is narrow, is exercised by a Git-backed adjacent-mutation negative test, and the
unpinned fields are documentation-only — but an allowlist of permitted added
fields would close the gap.

**N-5 — The host-adapter finding is correctly reported as no longer purely
historical.** `validate_host_adapter_contracts.py` still fails with
`protected path changed from BC-020 base: contracts/successor/unresolved_register.json`.
Unlike BC-040, where the diff over that path was empty, BC-041 genuinely changed
it — under explicit assignment authorization. Codex stated exactly this in
`handoff.md` and `validation.md` rather than reusing BC-040's "unrelated"
framing, did not suppress the error, and did not report it as a pass. That is
the honest disposition. Recommend a future assignment refresh the BC-020 base
pointer rather than leaving this validator permanently red.

**N-6 — The validator's leak scan is narrower than the unit test.**
`validate_opsec_contracts.py:422` scans serialized results for protected fixture
values only for non-`CLEAR` *egress* cases. Ingress results are not scanned
there. `test_receipts_and_logs_do_not_contain_protected_text_or_key` does cover
ingress and also scans for the HMAC key, so the property is proven — but the
standalone validator is the artifact a future assignment will lean on. Recommend
extending the validator scan to ingress results and to the evidence key.

**N-7 — Homoglyph substitution is not named in the limitations list.**
`cerulean comet chartеr` with a Cyrillic `е` returns `PASS`. This one genuinely
belongs outside a deterministic minimum matcher, and it is arguably covered by
`semantic_paraphrase_detection: false`. But it is a *character-level* rather
than semantic evasion, and readers will not find it under a paraphrase
disclaimer. Recommend naming confusable/homoglyph substitution explicitly in
`scope_exclusions` and the README limitations, alongside paraphrase — so the
boundary between "closed deterministically" (B-1) and "honestly out of scope"
(this) is legible.

### Preserved unresolved declarations

- SUR-002 — protected Auth actions remain unavailable in Phase 1. The register
  item and its blocker disposition are byte-identical to the base.
- SUR-011 — pending-authorization unrelated-turn policy remains unresolved and
  untouched. Named in `scope_exclusions` and asserted by test.
- SUR-012 — generic host-evidence contract remains resolved only at its existing
  level. No new host claim.
- SUR-003, SUR-004, SUR-010 and all remaining register items are unchanged.
- Only SUR-001 was modified, in both `unresolved_register.json` and
  `implementation_blocker_dispositions.json`.

## Review of the sixteen required determinations

1. **Does the contract solve SUR-001?** Substantially, at the bounded level —
   with B-1 outstanding. Eight of the nine disposition conditions hold. Condition
   7, "synthetic test coverage proves the mechanism," is undercut by B-1: the
   coverage proves the mechanism it specifies, and that mechanism has an open
   trivial ingress bypass.
2. **Is OPSEC still mandatory pre-ingress?** Yes.
   `phase1_executable_slice.json#turn_sequence` places
   `pre_ingress_opsec_normalize_and_match` before `SecurityDecision_PASS_required`
   and before `turn_controller_constructs_TurnRequest`. Both
   `validate_opsec_contracts.py` and `validate_python_readiness.py` enforce the
   ingress and egress steps as a required subset.
3. **Is Auth still separate?** Yes. `authorization_case_created: false`, no
   fourth `SecurityDecision` value, no protected match maps to `ASK`, Auth is in
   `scope_exclusions`, the policy schema carries
   `x-blu-auth-fields-forbidden: true` with `additionalProperties: false`, and
   `test_matcher_has_no_model_or_auth_dependency` asserts no `auth` token in the
   ingress evaluator's source or signature.
4. **Are production protected values absent?** Yes. Scanned all added lines for
   machine paths, home directories, `file://`, private-key headers, and
   credential assignments — none. The canonical config carries environment
   variable *names* only; location and expected digest are supplied by the
   environment. Fixture values are unmistakably fictional and the fixture key is
   labelled synthetic.
5. **Can missing/invalid policy accidentally PASS?** No. `load_policy` gates six
   ordered stages and returns `usable: False` with a safe error code at each
   failure. `evaluate_ingress(text, None, ...)` yields
   `security_decision: null`, `terminal_status: UNAVAILABLE`,
   `eligible_for_turn_controller: false`. Proven by the six-case loader matrix
   inside the validator and six standalone unit tests.
6. **Can a protected ingress reach the model?** **Yes — see B-1.** For
   contiguous matches under the specified normalization, no.
7. **Can protected egress reach public print?** Not for contiguous matches. A
   `BLOCK`-action rule withholds the entire output; a `REDACT`-action rule
   replaces every span and re-runs the full matcher. B-1 applies symmetrically
   but is low-likelihood at egress. Note that a rule omitting `egress` from
   `applies_to` is not checked at egress — that is policy-authoring risk, not a
   mechanism defect.
8. **Is redaction deterministic and non-leaking?** Yes. Every matched span is
   replaced; the redacted result is re-normalized and re-matched; residual
   content must contain an alphanumeric outside the replacement tokens;
   overlapping or invalid spans force `BLOCKED`; a redaction-only message forces
   `BLOCKED`. Verified that the replacement token always separates surviving
   text, so redaction cannot join fragments into a new protected phrase.
9. **Are logs and receipts content-safe?** Yes. Evidence fields are a closed
   set; the candidate digest is HMAC-SHA-256 under a policy-scoped key, with
   unkeyed protected-text digests explicitly forbidden; log entries are limited
   to three event types and a code pattern; error codes are a fixed vocabulary
   enforced by set equality. Verified that neither rule values nor the HMAC key
   appear in serialized ingress or egress results. See N-6 on scan asymmetry.
10. **Are the synthetic fixtures genuinely synthetic?** Yes. `cerulean comet
    charter` and `zircon café protocol` cannot be confused with Blu material, the
    key is `synthetic-only-evidence-key-…`, and both fixture files carry
    `synthetic test policy != production protected policy`, enforced by the
    validator.
11. **Does the contract avoid pretending to solve paraphrase?** Yes.
    `semantic_paraphrase_detection: false` is asserted by two validators and a
    test; README and handoff state the limit plainly. The contract's problem is
    the opposite of overclaiming: B-1 is a class it could close and did not, and
    N-7 is a class it should have named.
12. **Is `protected_policy_ref` portable and opaque?** Yes. It is an
    `environment_file` object of environment-variable *names* under
    `additionalProperties: false` with an uppercase-identifier pattern; the digest
    is also an environment binding; validators reject embedded machine paths and
    reject `rules`/`value` properties appearing under the reference. The
    six-stage contract correctly separates "reference configured" from "policy
    usable." This discharges BC-040 N-8.
13. **Are 7 components / 8 packets / 9 interfaces unchanged?** Yes — 7/8/9
    confirmed by direct count; the three registries are untouched by the diff;
    `architecture.component_added|packet_added|interface_added|route_added` are
    all `false` and validator-enforced.
14. **Are SUR-002, SUR-011, SUR-012 untouched?** Yes — see preserved
    declarations above.
15. **Is there zero production Python Blu runtime code?** Yes. Six `.py` files
    changed, all validators or tests; no `src/`, `adapters/`, or package root
    exists or was added; `python_package_layout.json#implementation_present`
    remains `false`; the OPSEC harness declares itself nonproduction in its
    module docstring and is allowlisted as such.
16. **Is the new `ready_for_python_phase1` state earned?** Not yet. It is earned
    on everything except the ingress boundary itself. Recommend the checklist
    return to green after B-1 is closed, rather than being held green with a
    known bypass. Should Dad and Blu judge B-1 acceptable as a documented Phase 1
    limitation instead, the correct form is an explicit entry in
    `scope_exclusions` and `remaining_limitations` — not silence.

## Validation review

Independently re-ran every suite named in the assignment from the reviewed tip.
Results match Codex's record.

```text
git diff --check                                          clean
tools/validate_runtime_contracts.py                       PASS   tests/contracts             21 OK
tools/validate_viability_audit.py                         PASS   tests/viability              9 OK
tools/validate_historical_archive_inventory.py            PASS   tests/historical_archives   12 OK
tools/validate_historical_behavioral_archaeology.py       PASS   tests/historical_archaeology 18 OK
tools/validate_successor_kernel_spec.py                   PASS   tests/successor_kernel      40 OK
tools/validate_host_adapter_contracts.py                  FAIL 1 tests/host_adapters         34 OK
tools/validate_continuity_contracts.py                    PASS   tests/continuity            42 OK
tools/validate_python_readiness.py                        PASS   tests/readiness             13 OK
tools/validate_opsec_contracts.py                         PASS   tests/security              22 OK
```

The single host-adapter failure is the fixed-base protected-path finding
discussed in N-5. It is reported, not suppressed.

Additional checks performed independently:

```text
golden CTS SHA256SUMS                     8/8 OK
golden paths changed vs authorized base   0
components / packets / interfaces         7 / 8 / 9
MANIFEST.sha256 entries                   274
manifest digest mismatches                0
manifest paths not tracked                0
tracked paths absent from manifest        0
production runtime roots                  0
Python files changed                      6, all validators/tests
prior assignment/review records changed   0
development.allow_protected_routes        const false, unchanged
development.allow_unverified_capabilities const false, unchanged
protected-value scan over added lines     0 hits
origin/main == authorized base            699ee14, confirmed
```

Manifest digests were verified against canonical Git blob content rather than
worktree bytes, which is the correct rule for this repository on Windows.

What this review does **not** establish: production policy completeness or
correct classification, live model behavior, LM Studio behavior, Auth,
protected continuation, or the security of a runtime that does not yet exist.
No real protected policy was loaded, referenced, or inspected at any point in
this review, and no protected value appears in this record.

## Disposition

`return-for-correction`

The work is otherwise strong and I would approve it on every other axis. The
architecture boundary, fail-closed loading, evidence design, portability of the
policy reference, fixture syntheticity, honest scope statements, and the refusal
to synthesize an `ASK` case are all correct, and the readiness re-evaluation is
mechanically consistent. The single blocking item is narrow, is a defect in the
normative normalization list rather than a disagreement about scope, and has a
verified remedy that breaks no existing fixture.

Requested for correction:

- **B-1** — close the Unicode format-character bypass in
  `minimum_contract.json#normalization`, `README.md`, `normalize_text`, and the
  ingress/egress fixtures.

Requested to be addressed or explicitly declined with reasons:

- **N-7** — name confusable/homoglyph substitution in the limitations.
- **N-2** — disambiguate `independent_Claude_review_required`.

The remaining notes (N-1, N-3, N-4, N-5, N-6) are informational and may be
carried into the runtime packet or a later assignment.

Readiness should remain as Codex left it until B-1 is resolved, at which point
`ready_for_python_phase1` is earned. It is not earned at this commit.

Python Runtime Phase 1 — Boot + Ordinary Turn + LM Studio Model Boundary —
remains unstarted and unauthorized. Nothing in this review authorizes it.

## Final status authorization

- Authorized by: pending Dad/Blu disposition
- Assignment status: review-complete, returned for correction
- Date: 2026-08-11
