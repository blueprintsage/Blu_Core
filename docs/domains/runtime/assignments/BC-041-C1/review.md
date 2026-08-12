# BC-041-C1 - Review Record

status: approve-with-notes
owner: Claude
last_reviewed: 2026-08-12

## Review identity

- Assignment: BC-041-C1
- Review pass: third and final independent review
- Reviewed branch tip: `204a229e2c01b255f1a940129cb724fa33fb4755`
- Reviewer: Claude
- Review type: independent correction review
- Review branch: `bc-041-c1-final-independent-review`
- Integration commit or merge identity: none

### Lineage reviewed

| Stage | Commit |
| --- | --- |
| Last verified pre-C1 `main` base | `33b44608cb634d1fedeed7f5f70d405c3999ed02` |
| First C1 substantive correction | `80e5b8554639c274f7baa69155ea9b83910f604c` |
| First C1 metadata receipt | `54519493189a332e984409504c45210e759f18fc` |
| Claude first review / B-1' finding | `874852c1b548ba4a2539d796d23ab9d803a966c8` |
| B-1' substantive repair | `2a9d6a28111ca9576bf6811e67ccca37f4d5dd39` |
| B-1' metadata receipt | `c6a447679c0ca07fb38a1e35eeb00231b0cb91e1` |
| Claude second review / B-1″ finding | `f87588d0fa094c203fde3b847ab9bc3c28d1b3fe` |
| **B-1″ substantive repair** | `85e18f56f88ab113646cc3aab477687eda8b85af` |
| **B-1″ metadata receipt** | `d1c283ab21681f8a0550da32c2ec87e08eb2852d` |
| **Metadata/readiness truth cleanup** | `204a229e2c01b255f1a940129cb724fa33fb4755` |

Prior Claude review commits were treated as review evidence only. No branch was
merged into the implementation branch.

## Mechanism verified

`normalized_match_candidate` now returns the `Cf`-removed candidate plus
`removed_cf_boundaries`: the normalized-coordinate offsets at which a `Cf` was
deleted. Each raw removal offset is mapped into normalized coordinates by
normalizing the left and right halves independently and accepting the offset
only when `startswith`/`endswith` agree, with explicit fallbacks at offset `0`
and end-of-string.

`_matches` drops the regex lookarounds and applies explicit guards:
`leading_boundary(start)` and `trailing_boundary(end)` accept a string edge, a
non-word neighbour, **or** an offset carrying removed-`Cf` provenance. A
run-merging rule additionally accepts a chain of exactly adjacent matches when
the run's outer edges qualify, which is what makes unseparated self-repetition
fail safe.

I confirmed the implementation satisfies all eight declared semantics, including
that candidate count stays at one and that provenance is offset-specific rather
than a blanket guard relaxation.

## Adversarial testing performed

Roughly 113,000 synthetic candidates, all using the fictional synthetic policy
values only.

**B-1' interior re-verification (13,686 candidates).** Exhaustive single and
pairwise interior insertion at every position across the protected phrase for
every combination of the six required code points, plus 6,000 randomized 3–10
insertion candidates with mixed code points, alternating and repeated placements,
across three surrounding contexts. Zero ingress or egress failures. **The B-1″
provenance repair did not regress B-1'.**

**B-1″ outer-edge attack matrix (17,280 candidates).** Every required code point
at the leading edge, trailing edge, both edges, repeated at one edge, multiple
consecutive at one edge, and mixed code points across the two edges — each
crossed with five interior insertion profiles (none, single boundary, single
inside-token, mixed, four-position) and with ASCII, Cyrillic, CJK, Greek,
alphanumeric and underscore neighbour tokens. Shapes covered
`foo<Cf><phrase>`, `<phrase><Cf>foo`, `foo<Cf><phrase><Cf>bar`,
`<phrase><Cf><phrase>`, and doubled-`Cf` variants. Zero failures.

**Provenance index-mapping hunt (11,944 candidates).** The offset mapping is a
heuristic, so I attacked it directly. I enumerated the entire Unicode space for
characters that present a word character at the weld and whose NFKC form is
non-trivial — 5,972 exotic neighbours including ligatures, fullwidth and
compatibility forms, combining marks, and the multi-word Arabic ligature
expansions — and welded each to both edges of the phrase through a `Cf`. Zero
bypasses. NFKC non-locality at the split point does occur, but in every observed
case it also corrupts the phrase itself, so no case both dropped provenance and
left a recoverable protected phrase.

**Egress and redaction integrity (30,000 candidates).** 22,500 REDACT-rule shapes
and 7,500 BLOCK-rule shapes over randomized 1–5 insertion mutations combined with
outer-edge welds, self-repetition, multiple protected matches in one candidate,
and separated repeats. For every printable result I asserted the replacement
token is present, no residual protected match survives a rescan, and no `Cf`
character reaches public output. Zero failures. Cross-rule overlapping spans fail
closed to `BLOCKED` / `EGRESS_REDACTION_INVALID`.

**Combined final fuzz (40,000 candidates).** Both synthetic rules, 1–8 insertions
at arbitrary positions including both outer edges, random neighbour tokens on
each side, and a 25% chance of appending a `Cf`-welded second copy of the phrase.
Zero ingress failures, zero `CLEAR` leaks, zero unsafe printable outputs.

## B-1' disposition

**Resolved.** Arbitrary interior `Cf` placement combinations — boundary,
inside-token, mixed, repeated, multi-token, multi-boundary, alternating,
cross-code-point, and saturation — produce neither ingress `PASS`/model
eligibility nor egress `CLEAR`/printability. The constant-one candidate property
holds; no placement enumeration occurs.

## B-1″ disposition

**Resolved.** The outer-edge adjacency bypass I reported at `f87588d` is closed.
The exact reproductions from that review now behave correctly:

```text
cerulean comet charter<U+200B>foo   ->  ingress BLOCK (not model-eligible)
                                        egress  REDACTED, phrase not in output
foo<U+200B>cerulean comet charter   ->  ingress BLOCK (not model-eligible)
                                        egress  REDACTED, phrase not in output
<phrase><phrase> unseparated        ->  ingress BLOCK
```

Verified for all six required code points at both edges, and the repair does not
depend on the specific neighbour token.

## False-positive and precision results

**No material precision loss.** All five committed negative ingress fixtures
still `PASS`, including `punctuation_adjacent_nonmatch`, `shared_words`, and
`near_match`.

The provenance exception is correctly tied to actual removal history and has not
become a generic token-guard bypass. Ordinary word adjacency with no removed-`Cf`
provenance still blocks the match, verified across ASCII, Cyrillic, CJK, Greek,
accented, and numeric neighbours:

```text
foo<phrase>            PASS     <phrase>foo             PASS
foo<phrase>bar         PASS     ЖУК<phrase>             PASS
<phrase>日本語          PASS     12<phrase>34            PASS
cerulean comet charterhouse  PASS     precerulean comet charter  PASS
xceruleancometcharterx       PASS     cerulean comot charter     PASS
```

The run-merging rule does not leak past the outer guard: `foo<phrase><phrase>`,
`<phrase><phrase>bar`, `foo<phrase><phrase>bar`, and the three-copy variant all
`PASS`, because the run's outer edges lack qualifying provenance.

**Zero-space separator semantics.** The contract intentionally treats
unseparated concatenation of rule words as a protected match, and this is now
explicitly declared rather than accidental: `unseparated_self_repetition_matches:
true` and `ordinary_word_adjacency_without_removed_Cf_matches: false`, both
enforced by the validator. `ceruleancometcharter` and `<phrase><phrase>` match
with no `Cf` present; this is the conservative direction, is bounded to the
rule's own words, and is documented. I did not silently redefine it.

One interaction worth recording for completeness: `_` is a member of the
declared `separator_set`, so `foo_<phrase>` normalizes the underscore to a space
and matches even though `_` is a `\w` character. This is pre-existing contract
behavior — verified identical at the pre-C1 base `33b4460` — not a C1 regression
and not a provenance defect.

## Egress and redaction results

Protected output could not be made `CLEAR` or otherwise printable under any
B-1' or B-1″ attack shape. `REDACT` rules produce canonicalized output carrying
the replacement token with no `Cf` characters and no residual match; `BLOCK`
rules withhold the whole output; post-redaction rescanning remains active and
uses the same provenance-aware matcher.

On the prior review's note that `_has_overlapping_spans` had become the primary
redaction-integrity guard: **verified safe.** It fires correctly on cross-rule
overlapping spans, and the surrounding postconditions (empty-residual check,
rescan, block-action precedence) each remain independently reachable. Recorded
as a verified condition, not a defect.

## Ingress enforcement

Structurally verified, not only through fixtures. `SecurityDecision` remains
exactly `["PASS", "BLOCK", "ASK"]`; no protected match maps to `ASK`. Across all
attack shapes the only pairing observed was `PASS`/model-eligible and
`BLOCK`/not-eligible — no recovered protected match ever reached Turn Controller
or model eligibility. All six policy-failure paths plus non-string input fail
closed: never model-eligible, never printable, always a safe error code.

## Evidence and logging

Content-safe under attack shapes. Evidence carries only the allowed fields
(`evaluation_phase`, `result`, `policy_revision`, `opaque_rule_refs`,
`candidate_hmac_sha256`); no forbidden field appears; no protected value and no
`evidence_hmac_key` leaks into any result, log, or validator output. Only
synthetic policy values exist in the repository.

The three prior non-blocking notes remain resolved and are now enforced rather
than merely fixed: the `rule_ref` opacity guard and the `Cf`-in-rule-value guard
both fire when tested against reintroduced violations, and the ambiguous
`normalize_text` helper remains replaced by `normalize_rule_text` and
`normalized_match_candidate`.

## Cleanup-commit review (`204a229`)

The two-line change to `tools/validate_python_readiness.py` re-pins the required
`correction_state` from `b1_prime_closed_pending_independent_rereview` to
`b1_prime_and_b1_double_prime_closed_pending_independent_rereview`, matching the
canonical checklist value updated in the same commit.

**This is necessary alignment, not a weakened gate.** The assertion remains an
exact-string equality check of the same form and strength; only the pinned value
changed. I probed the gate by mutation: a stale `correction_state`, a removed
`correction_state`, a review marked `completed`, and `implementation_authorized:
true` each still fail the validator with exit 1. The readiness validator also
still runs the expanded OPSEC proof transitively, so readiness cannot go green if
the `Cf` probe matrix or the outer-edge attack classes are removed. No
readiness/truth defect. I reviewed the substantive effect rather than the
originally described five-file metadata boundary, as instructed.

## Scope, architecture, and repository boundaries

- Successor architecture unchanged: **7 components, 8 packets, 9 interfaces**.
  No file under `contracts/successor/` was modified anywhere in C1.
- No prohibited architecture restored or created. Matches for mega-Exec, Exec
  Library, MMU service, School Engine, Mood service, SecuritySessionManager,
  AuthSessionManager, eighth continuity component, LM Studio component, Canon
  Manager, and Portability Manager occur only as golden-CTS filename references
  and explicit `prohibited_divergence` declarations, in untouched files.
- `PendingAuthorizationState` remains a state record; the seven components are
  unchanged and none is an authorization or session manager.
- Golden CTS untouched: zero changed files under `kernel/golden/`, and all eight
  `SHA256SUMS` entries verify OK. Current CTS authority remains
  `kernel/golden/v0.22.0/**`. No CTS rewrite of any kind.
- SUR dispositions not broadened. SUR-002, SUR-011, and SUR-012 all remain
  `blocking_for_implementation: true` with no disposition change; only SUR-001
  carries `resolved_at_minimum_phase1_contract_level`, unchanged since BC-041.
- No production implementation of Python Blu runtime, LM Studio provider, Local
  Mirror provider, Auth, protected authorization state, tools, or PASS/SkillForge.
  No `.py` file exists outside `tests/` and `tools/`; the only Python changed
  across all of C1 is the two nonproduction validators and their two test modules.
- The immutable BC-041 review is unmodified across the full range.
- `MANIFEST.sha256`: 278 entries, zero digest mismatches, zero tracked files
  missing, zero untracked entries.
- C1 changed 20 files in total, all within the declared collision domain.

**Validators and tests:** `validate_opsec_contracts.py` passed;
`validate_python_readiness.py` passed; 53 security and readiness tests OK; the
remaining 176 repository tests OK. `validate_host_adapter_contracts.py` reports
its single known BC-020 fixed-base finding on
`contracts/successor/unresolved_register.json` — accurately preserved, not
suppressed, not falsified, not misreported as clean. Not treated as a C1 blocker.

## Unicode scope limitation

Honestly stated and now enforced. `scope_exclusions` names both "general Unicode
confusable or homoglyph substitution detection" and, newly, "non-Cf
default-ignorable or invisible Unicode characters outside the Phase-1
general-category `Cf` contract"; the README states the same limitation, and the
validator asserts both appear in both places. `semantic_paraphrase_detection`
remains `false`, so the confusable/homoglyph limitation is not mislabeled as
semantic paraphrase. My prior N-1 note is fully addressed. No confusables engine
was required or added.

## Findings

### Blocking

None.

### Non-blocking

**N-1 — Provenance is dropped silently when the offset mapping disagrees, and no
test pins the invariant.** In `normalized_match_candidate`, when neither
`startswith`/`endswith` agreement nor the two edge fallbacks hold, the removal
offset is discarded with no signal. That is the correct conservative choice for
precision, but it is the one path that could silently weaken detection under a
future normalization change. I could not exploit it across 5,972 exotic
neighbours. Recommend an explicit invariant test — a removed `Cf` flanked by word
characters on both sides must always yield a provenance offset — so a future
pipeline edit cannot erode this without failing a gate.

**N-2 — Provenance construction is quadratic in the number of removed `Cf`
characters.** Each removal renormalizes both halves of the candidate. Measured in
the harness: 200 removals ≈ 1.6 ms, 800 ≈ 22 ms, 3,200 ≈ 347 ms. Not a defect in
a nonproduction conformance harness and not in scope for C1, but a `Cf`-saturated
egress candidate is attacker-influenced, so the Python Phase 1 implementation
should compute the offsets in a single pass rather than porting this shape
directly. Recorded for the runtime packet, not for C1.

**N-3 — Separator-set membership overlaps `\w`.** `_` is both a declared
separator and a word character, so `foo_<phrase>` matches while `foo<phrase>`
does not. Pre-existing and identical at the pre-C1 base, contract-declared via
`separator_set`, and outside C1's boundary. Noted only so the interaction between
`separator_set` and the token guards is on record for the runtime packet.

### Verified conditions (previously raised, now confirmed safe)

- `_has_overlapping_spans` as primary redaction-integrity guard — fires
  correctly; surrounding postconditions independently reachable.
- Non-`Cf` invisible and default-ignorable characters — remain out of scope by
  design, now explicitly disclosed in contract and README and enforced.
- Zero-space concatenation and unseparated self-repetition matching — intentional
  conservative behavior, explicitly declared and enforced.
- Opaque synthetic `rule_ref`, evidence digest fidelity, and unambiguous
  normalization helpers — all still resolved and now guarded.

## Readiness truth

The three states remain distinct, correctly ordered, and independently enforced:

1. **Technical readiness** — `result: ready_for_python_phase1`,
   `result_semantics: technical_conditions_satisfied_pending_independent_correction_review_and_Dad_Blu_closure`,
   `correction_state: b1_prime_and_b1_double_prime_closed_pending_independent_rereview`.
2. **Independent Claude review** — `state: required_pending`, `completed: false`,
   `required_before_implementation_authorization: true` at the reviewed tip.
3. **Dad/Blu authorization** — `implementation_authorized: false`,
   `automatic_start_prohibited: true`, `phase1.implementation_authorized: false`.

Each was mutation-tested: collapsing any one of them fails the validator. Python
Runtime Phase 1 has not started.

Because B-1' and B-1″ are both genuinely closed and no new blocking security or
precision defect exists, **technical `ready_for_python_phase1` is earned.**

## Disposition

`approve-with-notes`

B-1' is resolved and was not regressed by the B-1″ repair. B-1″ is resolved; my
own prior reproductions now block at ingress and redact or block at egress across
all six required code points and every attack shape I could construct. The
boundary-provenance mechanism is precise rather than permissive — it did not
degrade into a generic token-guard bypass, and no negative fixture or precision
probe regressed. Scope, architecture, CTS, SUR, manifest, evidence safety, and
readiness truth are all preserved, and the cleanup commit's validator change is
honest alignment rather than a weakened gate.

The three notes are advisory and none blocks: N-1 asks for an invariant test
around an already-correct conservative path, N-2 is a performance shape to fix
when porting to production Python, and N-3 records pre-existing contract
behavior.

**Technical `ready_for_python_phase1` is earned.**

**Python Runtime Phase 1 is still not implementation-authorized.** Dad/Blu final
closure remains required before any implementation begins. This approval
completes independent review only; it does not authorize implementation, merge,
release, or automatic start.

## Required follow-up

1. Dad/Blu integration and BC-041-C1 closure.
2. Carry N-1 and N-2 into the Python Runtime Phase 1 packet as implementation
   guidance, not as C1 rework.

Do not merge this review branch. Do not merge prior Claude review branches into
the implementation branch. Do not begin Python implementation.

## Final status authorization

- Authorized by: Claude independent review complete (`approve-with-notes`);
  Dad/Blu closure pending
- Assignment status: approve-with-notes
- Date: 2026-08-12
