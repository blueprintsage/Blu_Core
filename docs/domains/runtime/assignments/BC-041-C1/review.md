# BC-041-C1 - Review Record

status: return-for-correction
owner: Claude
last_reviewed: 2026-08-12

## Review identity

- Assignment: BC-041-C1
- Review pass: second independent review (post B-1' correction)
- Last verified pre-C1 base: `33b44608cb634d1fedeed7f5f70d405c3999ed02`
- First C1 substantive correction: `80e5b8554639c274f7baa69155ea9b83910f604c`
- First C1 metadata receipt: `54519493189a332e984409504c45210e759f18fc`
- Prior Claude review / B-1' finding: `874852c1b548ba4a2539d796d23ab9d803a966c8`
- Reviewed substantive correction: `2a9d6a28111ca9576bf6811e67ccca37f4d5dd39`
- Reviewed metadata receipt: `c6a447679c0ca07fb38a1e35eeb00231b0cb91e1`
- Source branch: `bc-041-c1-mixed-cf-correction`
- Reviewer: Claude
- Review type: independent correction review
- Review branch: `bc-041-c1-mixed-cf-independent-review`
- Integration commit or merge identity: none

## Mechanism under review

The two-static-view mechanism is replaced by a single deterministic candidate:
every Unicode general-category `Cf` code point is removed, the remainder runs
through the existing normalization pipeline, and protected rules match with
separator-tolerant inter-word matching (`normalized_rule_inter_word_separator_matches:
zero_or_more_ASCII_spaces`, implemented as `r" *".join(...)` at
`tools/validate_opsec_contracts.py:120`), retaining the whole-phrase Unicode
token guards `(?<!\w)` and `(?!\w)` at `:121`.

The design intent — one candidate whose count does not grow with insertion
count — is sound and is the right correction to the prior enumeration approach.
The implementation applies the tolerance to the phrase's **interior** word
separators only. The phrase's **outer** boundary guards are still evaluated
against a candidate from which `Cf` removal has already deleted the outer
boundary. That asymmetry reintroduces the B-1 failure mode.

## Findings

### Blocking

**B-1″ — `Cf` removal welds the protected phrase to an adjacent word token, and
the outer token guard is not separator-tolerant. A single `Cf` at the leading or
trailing edge of a protected phrase defeats ingress and egress.**

Separator tolerance was applied between the rule's words but not at the rule's
outer edges. When a `Cf` sits at the phrase boundary and any word character is
adjacent on the far side, removal joins them into one token. `(?<!\w)` /
`(?!\w)` then reject the match that removal was supposed to recover.

Minimal synthetic reproduction (synthetic policy only, no real protected
values), single insertion, one code point:

```text
ingress: cerulean comet charter<U+200B>foo
  Cf-removed candidate: 'cerulean comet charterfoo'
  pattern (?<!\w)cerulean *comet *charter(?!\w) -> trailing guard sees 'f'
  SecurityDecision = PASS, eligible_for_turn_controller = True

egress:  cerulean comet charter<U+200B>foo
  EgressResult = CLEAR, eligible_for_print = True
  public_output = 'cerulean comet charter​foo'   (phrase intact)
```

Reproduces identically for the leading edge (`foo<U+200B>cerulean comet
charter`) and for all six required code points at both edges, at both phases:

```text
code point   trailing ingress   leading ingress   trailing egress   leading egress
U+200B       PASS (elig)        PASS (elig)       CLEAR/printable   CLEAR/printable
U+00AD       PASS (elig)        PASS (elig)       CLEAR/printable   CLEAR/printable
U+200D       PASS (elig)        PASS (elig)       CLEAR/printable   CLEAR/printable
U+200C       PASS (elig)        PASS (elig)       CLEAR/printable   CLEAR/printable
U+FEFF       PASS (elig)        PASS (elig)       CLEAR/printable   CLEAR/printable
U+2060       PASS (elig)        PASS (elig)       CLEAR/printable   CLEAR/printable
```

A second reachable form needs no foreign token at all — the protected phrase
concatenated to itself, which is what an adversary gets for free by repeating
it:

```text
egress:  <phrase with mixed Cf><phrase with mixed Cf>   (no separator)
  candidate: 'ceruleancomet charterceruleancomet charter'
  EgressResult = CLEAR, eligible_for_print = True, both copies intact
```

**This is a regression, not a residual gap.** The same inputs were correctly
handled by the mechanism this correction replaced. Re-running them against
`tools/validate_opsec_contracts.py` at `5451949`:

```text
cerulean comet charter<U+200B>foo   ->  ingress BLOCK   egress REDACTED
```

The retired `cf_to_ascii_space` view was the only thing preserving outer word
boundaries. Removing it closed the interior mixed-placement case and opened the
edge case. Severity is the same class B-1 and B-1' named: a protected phrase
reaches the Turn Controller and the model at ingress, and reaches public print
verbatim at egress. Because no match is produced, the `BLOCK` egress action, the
redaction postconditions, the overlapping-span guard, and the post-redaction
rescan are all unreachable — every downstream control is individually correct
and all are bypassed.

Why the committed gates are green: every `mixed` fixture added in this
correction (`cf_*_mixed`, `cf_cross_code_point_mixed`) places the protected
phrase either at a string edge or inside `"Before … after."`, so the phrase's
outer boundaries are always adjacent to a real ASCII space. The fixture schema
records `cf_position` and `cf_insertion_count` but has no notion of an insertion
at the phrase's outer edge against an adjacent token, so the class is not
expressible. 49 passing tests and two clean validators are fully consistent with
this bypass.

Property the correction must satisfy (stated, not prescribed): a removed `Cf`
must be treated as a potential word boundary **at the phrase's outer edges on
the same terms as it is already treated between the phrase's words** — that is,
the outer guard must be satisfied by either a genuine non-word neighbour or a
position where a `Cf` was removed. Any mechanism with that property, evaluated
symmetrically at ingress and egress, closes B-1″ without reintroducing
candidate-set growth.

### Non-blocking

**N-1 — Invisible characters outside general-category `Cf` defeat the matcher
and the limitation is not disclosed.** Removal is scoped to `Cf`, so invisible
or default-ignorable code points in other categories survive and break the
phrase:

```text
character                          category   ingress   egress
U+FE00 VARIATION SELECTOR-1        Mn         PASS      CLEAR
U+034F COMBINING GRAPHEME JOINER   Mn         PASS      CLEAR
U+3164 HANGUL FILLER               Lo         PASS      CLEAR
U+1160 HANGUL JUNGSEONG FILLER     Lo         PASS      CLEAR
```

This is outside the declared B-1' boundary — the contract scopes itself to `Cf`
throughout, and the handoff explicitly forbids broadening into general Unicode
spoofing — so it is **not** promoted to blocking. But it is also not a
confusable or homoglyph substitution, so N-7's exclusion does not honestly cover
it. `scope_exclusions` and the README should name non-`Cf` invisible and
default-ignorable code points as a known, deliberate Phase-1 limitation, so that
"format-character insertion is closed" cannot be read as "invisible-character
insertion is closed". Disclosure only; no mechanism change requested.

**N-2 — Zero-or-more space tolerance makes zero-space concatenation a protected
match, which is undocumented.** `ceruleancometcharter` and `ceruleancomet
charter` now return `BLOCK` with no `Cf` present. This is the fail-safe
direction and causes no negative-fixture regression, but for a rule whose words
concatenate into an ordinary word it would over-match. The contract states the
tolerance mechanically (`zero_or_more_ASCII_spaces`) without stating that
consequence; `separator_tolerance_purpose` should say that unseparated
concatenation of rule words is intentionally treated as a match.

**N-3 — `_has_overlapping_spans` is now the sole redaction-integrity guard.**
With one candidate the divergent-view fail-closed branch is correctly gone. The
remaining guard was independently confirmed to fire (two rules overlapping on a
shared token return `BLOCKED` / `EGRESS_REDACTION_INVALID`, not printable), but
it is now load-bearing alone. No defect; noted for future review attention.

### Disposition of the prior review's non-blocking notes

All three are genuinely resolved; the claim is accurate.

1. **Synthetic `rule_ref` opacity — resolved and enforced.** Fixture refs are now
   `SYNTH-RULE-0001` / `SYNTH-RULE-0002`, and a new guard in
   `validate_policy_usability` rejects a `rule_ref` whose alphanumeric-compacted
   form contains the compacted rule value. Independently confirmed to fire on a
   reintroduced descriptive ref. A related new guard rejects a policy rule value
   containing a `Cf` code point; also confirmed to fire.
2. **Evidence digest fidelity — resolved by construction.** With a single
   candidate, the value passed to `_evidence` is the candidate that actually
   matched. The prior view-0/view-1 mismatch cannot occur.
3. **`normalize_text` ambiguity — resolved.** The helper is gone, replaced by
   `normalize_rule_text` (rule canonicalization) and `normalized_match_candidate`
   (candidate derivation). Names now state which side of the matcher they serve.

### Preserved unresolved declarations

- SUR-002, SUR-011, SUR-012 — unchanged. `contracts/successor/unresolved_register.json`
  has zero changed files across `33b4460..c6a4476`; C1 has never touched the
  register in either correction pass.
- SUR-001 — remains `resolved_at_minimum_phase1_contract_level`. Not modified by
  this review. B-1″ means the disposition's "synthetic test coverage proves the
  mechanism" condition is still not met.

## Validation review

Independently executed at `c6a4476` on the review branch.

Adversarial `Cf` testing (beyond the committed fixtures):

- Exhaustive interior insertion, all single and all pairwise positions across
  the protected phrase, every code point combination; sampled triples —
  15,666 candidates. Zero ingress or egress failures.
- Randomized 4–12 simultaneous insertions with mixed code points including
  leading and trailing positions — 36,000 candidates. Zero failures.
- Saturation: a `Cf` in every inter-character gap, and additionally at both
  edges, for all six code points. All blocked.
- Second rule (`BLOCK` egress action, non-ASCII, NFKC-decomposed and
  precomposed forms) — 1,000 candidates. Zero failures.
- Surrounding-context matrix (string edge, sentence, ellipsis, brackets,
  tab/newline, leading/trailing spaces, hyphen adjacency, parenthesised
  repetition, space-separated repetition, **unseparated repetition**).
  Only unseparated adjacency failed — this is B-1″.
- Ordering check: no non-`Cf` code point in the entire Unicode space has an NFKC
  form containing a `Cf` character (0 of 1,114,112), so removing `Cf` before
  NFKC cannot leak a format character back into the candidate.

The interior mixed-placement class the prior review raised as B-1' **is
resolved**. The mechanism does have the claimed constant-one candidate property.
B-1″ is a distinct, newly introduced edge-boundary defect.

False-positive and regression testing:

- All five negative ingress fixtures still `PASS` (`ordinary`, `near_match`,
  `shared_words`, `partial_fragment`, `punctuation_adjacent_nonmatch`).
- Fourteen additional over-matching probes: suffix/prefix words, protected words
  embedded in longer Unicode tokens, shared words at distance, near matches
  differing by a real character, word-order permutation, an inserted extra word,
  multiple spaces, tabs/newlines, and punctuation adjacency all behave
  correctly. No false-positive regression from separator tolerance except the
  documented-as-N-2 zero-space concatenation case.

Structural and boundary verification:

- `python tools/validate_opsec_contracts.py` — passed.
- `python tools/validate_python_readiness.py` — passed.
- `python -m unittest tests.security.test_validate_opsec_contracts
  tests.readiness.test_validate_python_readiness` — 49 tests, OK.
- `python tools/validate_host_adapter_contracts.py` — 1 error, the known BC-020
  fixed-base finding on `contracts/successor/unresolved_register.json`. Verified
  accurately preserved: not suppressed, not falsified, not reported as clean.
  Not treated as a C1 blocker.
- SecurityDecision vocabulary is exactly `PASS`/`BLOCK`/`ASK`; no protected match
  maps to `ASK`; `authorization_case_created: false`. Only `PASS` sets
  `eligible_for_turn_controller`, asserted structurally in `validate` and not
  only by fixture.
- Policy failure paths independently exercised through the loader matrix:
  missing reference, unavailable target, malformed payload, schema-invalid
  payload, integrity mismatch, and unusable policy each fail closed with a safe
  error code, never model-eligible and never printable.
- Evidence restricted to the seven allowed fields; candidate digest HMAC-keyed;
  logs carry only event/code pairs. No raw input, matched text, span, rule value,
  or key appears in any evaluated result, including on the B-1″ path.
- Architecture: 7 components / 8 packets / 9 interfaces, read directly from the
  registries. `component_added`, `packet_added`, `interface_added`,
  `route_added` all `false`. No file under `contracts/successor/` was modified.
- No prohibited architecture restored or introduced. Matches for mega-Exec, Exec
  Library, MMU, School Engine, Mood service, SecuritySessionManager,
  AuthSessionManager, eighth continuity component, LM Studio component, Canon
  Manager, and Portability Manager occur only as golden-CTS filename references
  and explicit `prohibited_divergence` declarations, in files C1 did not touch.
  `PendingAuthorizationState` remains a state record only.
- Golden CTS: zero changed files under `kernel/golden/` across the full range;
  current CTS authority remains `kernel/golden/v0.22.0/**`.
- The immutable BC-041 review is unmodified across the full range.
- `MANIFEST.sha256`: 278 entries, zero digest mismatches against git-stored
  content, zero tracked files absent from the manifest, zero manifest entries
  untracked.
- No production Python runtime, LM Studio provider, Local Mirror provider, Auth,
  protected-authorization state, tool, or PASS/SkillForge implementation. The
  four Python files changed are the two nonproduction validators and their two
  test modules.
- No real protected-policy values. Only the fictional synthetic fixtures under
  the production-separation notice.

## Readiness-state review

The three states remain distinct and correctly ordered:

1. Technical deterministic readiness — `result: ready_for_python_phase1`.
2. Independent Claude review completion — `independent_correction_review.state:
   required_pending`, `completed: false`,
   `required_before_implementation_authorization: true`; the checklist check
   `independent_Claude_correction_review` is `required_pending`.
3. Dad/Blu implementation authorization — `implementation_authorized: false`,
   `automatic_start_prohibited: true`, `phase1.implementation_authorized: false`.

Claude review was pending and incomplete at the reviewed commit, implementation
was unauthorized, and no Python runtime work had begun. The separation is
enforced by validator assertions and by
`test_pending_review_cannot_authorize_implementation` and
`test_independent_review_pending_is_not_completion`.

Because B-1″ is open, technical `ready_for_python_phase1` is **not** earned at
`c6a4476`. The readiness record is honest about authorization state but
overstates technical state, exactly as in the prior pass and for a related
reason.

## Disposition

`return-for-correction`

The correction achieves what it set out to achieve: B-1' — the interior
mixed-placement `Cf` bypass — is genuinely closed, verified against 52,000+
adversarial candidates rather than against the fixtures. The single-candidate
design is the right shape, the constant-one property holds, the three prior
non-blocking notes are properly resolved with new enforcement, and every
boundary, architecture, scope, CTS, manifest, and readiness-separation check is
clean.

It cannot be approved because retiring the boundary-preserving view opened
B-1″ at the phrase edges, and that defect delivers a protected phrase to the
model at ingress and to public print at egress from a **single** invisible
character — a strictly simpler attack than the one this pass fixed, and one the
previous mechanism caught.

## Required follow-up

1. Close B-1″ by making the outer phrase guard satisfied by a removed-`Cf`
   position, symmetrically at ingress and egress, without reintroducing
   candidate-set growth.
2. Extend the fixture schema with an edge-adjacency position class — protected
   phrase joined by `Cf` to a neighbouring word token on the leading edge, the
   trailing edge, and both — for all six code points at ingress and egress, plus
   the unseparated self-repetition case.
3. Re-run the negative fixtures and the over-matching probes against the
   corrected mechanism; the outer guard must still reject `charterhouse`-style
   suffix and prefix adjacency where no `Cf` is present.
4. Disclose N-1 in `scope_exclusions` and the README; document N-2's
   concatenation semantics in `separator_tolerance_purpose`.
5. Re-assert technical `ready_for_python_phase1` only after 1–3 hold.

Do not merge this review branch, the prior review branch, or either Codex
correction branch as part of this review. Independent review of `c6a4476` is
complete; implementation authorization remains a separate Dad/Blu decision and
is not granted by this record. Do not start Python Runtime Phase 1.

## Final status authorization

- Authorized by: Claude independent review complete; Dad/Blu disposition pending
- Assignment status: return-for-correction
- Date: 2026-08-12
