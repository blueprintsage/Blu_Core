# BC-041-C1 - Review Record

status: return-for-correction
owner: Claude
last_reviewed: 2026-08-12

## Review identity

- Assignment: BC-041-C1
- Reviewed base: `33b44608cb634d1fedeed7f5f70d405c3999ed02`
- Reviewed work commit: `80e5b8554639c274f7baa69155ea9b83910f604c`
- Reviewed metadata commit: `54519493189a332e984409504c45210e759f18fc`
- Reviewer: Claude
- Review type: independent correction review
- Review branch: `bc-041-c1-independent-review`
- Integration commit or merge identity: none

## Required review questions

1. Is original B-1 fully resolved?
2. Does the normative contract require both `Cf -> space` and `Cf -> removed` views?
3. Does either matching view cause a protected match?
4. Do all six required `Cf` code points block at ingress in both positions?
5. Do all six block or redact safely at egress in both positions?
6. Do existing negative fixtures retain their expected behavior?
7. Can any corrected protected ingress reach Turn Controller/model execution?
8. Can corrected protected egress reach public print?
9. Are logs and receipts still non-leaking?
10. Is homoglyph/confusable substitution explicitly and honestly out of scope?
11. Is independent-review state clearly distinguished from review completion?
12. Are SUR-002, SUR-011, and SUR-012 unchanged?
13. Are 7 components, 8 packets, and 9 interfaces unchanged?
14. Are real protected values absent?
15. Is there still zero production Python Blu runtime code?
16. After C1, is `ready_for_python_phase1` technically earned?

## Determinations

1. **Is original B-1 fully resolved?** **No.** The six single-insertion cases
   enumerated in the BC-041 review now block, but the defect class B-1 names —
   deterministic `Cf` insertion defeating the boundary — remains open. Two
   format characters placed in *different position classes* within one protected
   phrase evade both required candidate views. See B-1' below.
2. **Does the contract require both views?** Yes.
   `minimum_contract.json#normalization.candidate_views` declares
   `cf_to_ascii_space` and `cf_removed`;
   `candidate_view_generation_applies_to` is `["ingress","egress"]` and
   `both_views_continue_through_remaining_ordered_steps` is `true`.
   `validate_opsec_contracts.py:495-500` enforces all three.
3. **Does either matching view cause a protected match?** Yes, as specified and
   as implemented. `match_in_either_view_is_protected_match: true` is enforced
   at `validate_opsec_contracts.py:501`, and `evaluate_ingress`/`evaluate_egress`
   flatten matches across both views (`:261`, `:303`). The defect in B-1' is not
   that either-view matching fails; it is that two views are provably
   insufficient to cover the input space.
4. **Do all six `Cf` code points block at ingress in both positions?** Yes, for
   the two probed positions. All 12 ingress probes return `BLOCK` with
   `eligible_for_turn_controller: false`. Verified independently.
5. **Do all six block or redact safely at egress in both positions?** Yes, for
   the two probed positions. All 12 egress probes return `REDACTED` with the
   replacement present and a clean dual-view rescan. Verified independently.
6. **Do existing negative fixtures retain their expected behavior?** Yes. All
   five negative ingress fixtures (`ordinary`, `near_match`, `shared_words`,
   `partial_fragment`, `punctuation_adjacent_nonmatch`) still return `PASS`, and
   `test_existing_negative_ingress_fixtures_remain_pass` pins the set by id so
   silent deletion is caught. No regression introduced by the dual-view change.
7. **Can corrected protected ingress reach Turn Controller/model execution?**
   **Yes, via B-1'.** A mixed-placement `Cf` insertion yields
   `security_decision: PASS` and `eligible_for_turn_controller: true`. For the
   probed single-insertion cases, no — `eligible_for_turn_controller` is `false`
   on every non-`PASS` path, and `validate_opsec_contracts.py:464` asserts it
   globally.
8. **Can corrected protected egress reach public print?** **Yes, via B-1'.** A
   mixed-placement insertion yields `CLEAR` / `eligible_for_print: true` with
   `public_output` carrying the protected phrase verbatim. This defeats both
   `REDACT` and `BLOCK` egress actions.
9. **Are logs and receipts still non-leaking?** Yes on the code path. Evidence
   is restricted to the seven allowed fields, the candidate digest is HMAC-keyed
   under `evidence_hmac_key`, and logs carry only event/code pairs. No raw
   input, matched text, span, or key appears in any evaluated result. One
   fixture-hygiene concern is recorded as N-1.
10. **Is confusable/homoglyph substitution explicitly out of scope?** Yes, and
    honestly. `scope_exclusions` carries "general Unicode confusable or homoglyph
    substitution detection" as an entry distinct from "arbitrary semantic
    paraphrase or obfuscation detection", and
    `contracts/security/opsec/README.md:94-97` states the limitation in prose.
    `validate_opsec_contracts.py:503-508` enforces both the contract entry and
    the README statement. N-7 is correctly resolved: the limitation is not
    mislabeled as semantic paraphrase.
11. **Is independent-review state distinguished from completion?** Yes.
    `independent_correction_review` carries `state: required_pending`,
    `completed: false`, and `required_before_implementation_authorization: true`;
    `implementation_authorized` is `false` and `automatic_start_prohibited` is
    `true`. Four separate validator assertions (`:547-557`) plus
    `test_pending_review_cannot_authorize_implementation` and
    `test_independent_review_pending_is_not_completion` prevent the three states
    from collapsing. N-2 is resolved.
12. **Are SUR-002, SUR-011, SUR-012 unchanged?** Yes. `git diff` of
    `contracts/successor/unresolved_register.json` across
    `33b4460..5451949` is empty; C1 touched no register entry at all.
13. **Are 7 components, 8 packets, 9 interfaces unchanged?** Yes. Counts
    verified directly as 7/8/9. `architecture.component_added`, `packet_added`,
    `interface_added`, and `route_added` are all `false` and enforced at `:512`.
14. **Are real protected values absent?** Yes. The only phrase values are the
    fictional synthetic fixtures `cerulean comet charter` and
    `zircon café protocol`, under the production-separation notice. The runtime
    config schema still forbids embedded `rules`/`value` and machine-specific
    paths (`:515-522`).
15. **Is there still zero production Python Blu runtime code?** Yes. The four
    Python files touched are the two nonproduction validators under `tools/` and
    their two test modules. No package, adapter, daemon, CLI, or UI code exists.
16. **Is `ready_for_python_phase1` technically earned?** **No.** The checklist
    reports `result: ready_for_python_phase1` with
    `minimum_OPSEC_match_and_redaction_contract_available: pass`. Because B-1'
    leaves a deterministic protected-content bypass open at both ingress and
    egress, that gate is not technically earned. The readiness record is
    accurate about *authorization* state but overstates *technical* state.

## Findings

### Blocking

**B-1' — Two `Cf` candidate views are insufficient; mixed-placement format-character
insertion still defeats ingress and egress.**

The correction closes the six single-insertion cases the BC-041 review
enumerated, but not the class it named. The two required views are complementary
in opposite directions and neither is a superset:

- `cf_to_ascii_space` recovers a `Cf` that stood **at a word boundary**, but
  **splits** a token when the `Cf` was **inside** it.
- `cf_removed` recovers a `Cf` that stood **inside a token**, but **joins** two
  words when the `Cf` was at a **boundary**.

When one protected phrase contains at least one `Cf` in each position class,
every view is corrupted somewhere and neither reconstructs the phrase. Observed
against the shipped harness at `80e5b85` and the synthetic policy, using two
format characters:

```text
input: cerulean<Cf>co<Cf>met charter
  cf_to_ascii_space -> 'cerulean co met charter'   (no match)
  cf_removed        -> 'ceruleancomet charter'     (no match)

code point   ingress   model_eligible   egress   printable
U+200B       PASS      True             CLEAR    True
U+00AD       PASS      True             CLEAR    True
U+200D       PASS      True             CLEAR    True
U+200C       PASS      True             CLEAR    True
U+FEFF       PASS      True             CLEAR    True
U+2060       PASS      True             CLEAR    True
```

Scope of the failure:

- **Ingress.** `SecurityDecision = PASS` and
  `eligible_for_turn_controller = true`. The protected phrase reaches the Turn
  Controller and the model. This is the same terminal outcome B-1 recorded.
- **Egress.** `EgressResult = CLEAR`, `eligible_for_print = true`, and
  `public_output` is the raw candidate with the protected phrase intact. This is
  strictly worse than the ingress case: protected content reaches public print.
- **Both egress actions defeated.** The `REDACT`-action rule
  (`cerulean comet charter`) and the `BLOCK`-action rule
  (`zircon café protocol`) both go `CLEAR`. Because there is no match, the
  `BLOCK` branch (`:322`), the divergent-view fail-closed branch (`:332-342`),
  the redaction postconditions, and the dual-view rescan are all unreachable.
  Every downstream safety mechanism is correct and every one is bypassed.
- **Code-point agnostic.** Reproduces for all six required code points and
  across mixed code points (`U+200B` + `U+FEFF`).
- **Not the disclaimed class.** This is byte-for-byte the protected phrase with
  two invisible characters added. It is not confusable substitution and not
  semantic paraphrase, so N-7's honest exclusion does not cover it.

Why the gates did not catch it: `REQUIRED_CF_CODE_POINTS` × `("boundary",
"inside_token")` (`:442`) defines the probe matrix over exactly the two
single-position classes, and the fixture matrix is asserted equal to it. The
mixed class is not expressible in the current fixture schema, so 44 passing
tests and a green validator are consistent with the bypass.

Direction for correction (not prescriptive): two static views cannot cover this
input space, because the number of position-class combinations grows with the
number of inserted characters. A single `Cf`-removed view combined with
separator-tolerant phrase matching — where the inter-word separators of the
normalized rule value match zero-or-more normalized spaces — collapses all
placement combinations into one deterministic view without reintroducing the
negative fixtures. The corrected fixture matrix should add a mixed-placement
position class alongside `boundary` and `inside_token`, and the negative set
(`punctuation_adjacent_nonmatch`, `shared_words`, `near_match`) must be re-proved
against whatever mechanism is chosen.

### Non-blocking

**N-1 — The synthetic policy models a `rule_ref` that reconstructs the protected
value.** `SYNTH-RULE-CERULEAN-COMET` embeds the protected phrase in the field
the contract designates as opaque. `safe_evidence.allowed_fields` includes
`opaque_rule_refs` while `forbidden_fields` includes `rule_value`; a rule_ref
derived from the phrase makes that distinction cosmetic, and this fixture is the
reference example a production policy author would follow. The leak assertions
at `:477` and `test_cf_results_receipts_and_logs_do_not_leak` do not catch it,
because the joined form does not normalize to the phrase. Recommend an opaque
identifier in the fixture and, if cheap, an assertion that no `rule_ref`
normalizes to a superstring of its own `value`.

**N-2 — Evidence digest is always computed from view 0.** `evaluate_ingress:262`
and `evaluate_egress:305` set `normalized = views[0]["normalized"]`
(`cf_to_ascii_space`) unconditionally, including when the match occurred only in
`cf_removed`. The receipt's `candidate_hmac_sha256` therefore does not
correspond to the view that produced the decision. Content-safe and
non-blocking, but it weakens receipt fidelity for exactly the inputs the
correction was written to catch.

**N-3 — `normalize_text` is now a partial view of its own pipeline.** It returns
`normalized_candidate_views(value)[0]` and is used for rule canonicalization,
policy usability, and the leak scan. That is correct for rule values, which
should not contain `Cf`, but the name no longer signals that it is one of two
views. A policy value containing a `Cf` character would be canonicalized under
only one view.

### Preserved unresolved declarations

- SUR-002 — protected Auth actions remain unavailable in Phase 1. Untouched by
  C1; the register file is byte-identical to the reviewed base.
- SUR-011 — pending-authorization unrelated-turn policy remains unresolved and
  untouched; still named in `scope_exclusions`.
- SUR-012 — generic host-evidence contract remains resolved only at its existing
  level. No new host claim.
- SUR-001 — remains `resolved_at_minimum_phase1_contract_level`. This review
  does not modify it, but B-1' means condition 7 of that disposition
  ("synthetic test coverage proves the mechanism") is still not met, for the
  same reason the BC-041 review gave.
- No register item was modified by C1.

## Validation review

Independently executed at `5451949` on the review branch:

- `python tools/validate_opsec_contracts.py` — passed.
- `python tools/validate_python_readiness.py` — passed.
- `python -m unittest tests.security.test_validate_opsec_contracts
  tests.readiness.test_validate_python_readiness` — 44 tests, OK.
- `git diff --check 33b4460 5451949` — clean.
- Golden CTS: `git diff` over `kernel/golden/` across the range is empty, and
  `sha256sum -c SHA256SUMS` reports OK for all 8 entries.
- Immutable BC-041 review: `git diff` over
  `docs/domains/runtime/assignments/BC-041/review.md` is empty.
- Architecture counts: 7 components / 8 packets / 9 interfaces, read directly
  from the registries.
- `MANIFEST.sha256`: 278 entries, zero mismatches against git-stored content,
  zero tracked files missing from the manifest, zero manifest entries not
  tracked. (Digests are over LF-normalized git content; a working-tree byte
  comparison shows 117 false mismatches from CRLF checkout and is not the
  correct check.)
- Collision domain: all 19 changed paths fall inside the declared allowed set.
  No protected or prohibited path was touched.

The validation record is accurate for what it claims. Its limitation is scope,
not honesty: every probe it defines passes, and the probe set does not span the
defect class. `validation.md` should not be read as evidence that B-1 is closed.

Independent probes beyond the supplied fixtures were run for mixed-placement
insertion (single and cross code point), `Cf` between every character, repeated
same-class insertion, divergent-view egress, and the `BLOCK`-action egress rule.
The divergent-view fail-closed branch was independently confirmed reachable and
correct: a candidate matching in both views with differing normalized forms
returns `BLOCKED` / `EGRESS_REDACTION_INVALID` / not printable. Only the
mixed-placement class failed.

## Disposition

`return-for-correction`

The correction is well-built, stays inside its boundary, preserves the golden
CTS and the immutable BC-041 review, leaves the architecture and the SUR
register untouched, and resolves N-7 and N-2 cleanly. It does not close B-1. A
two-character invisible insertion still delivers a protected phrase to the model
at ingress and to public print at egress, which is the outcome B-1 was raised to
prevent.

Because the same defect keeps `ready_for_python_phase1` from being technically
earned, this disposition also declines determination 16.

## Required follow-up

1. Close B-1' with a mechanism that covers arbitrary `Cf` placement
   combinations, not an enumerated position list.
2. Extend the fixture matrix with a mixed-placement position class for all six
   required code points at ingress and egress, and re-prove the five negative
   ingress fixtures against the new mechanism.
3. Re-assert the readiness OPSEC gate only after 1 and 2 hold.
4. Address N-1, N-2, and N-3 at the correcting author's discretion; none blocks.

Do not merge this review branch. Do not start Python Runtime Phase 1.
Independent review is complete; implementation authorization remains a separate
Dad/Blu decision and is not granted by this record.

## Final status authorization

- Authorized by: Claude independent review complete; Dad/Blu disposition pending
- Assignment status: return-for-correction
- Date: 2026-08-12
