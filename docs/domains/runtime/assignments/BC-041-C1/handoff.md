# BC-041-C1 - Implementation Handoff

status: ready-for-review
owner: Codex
last_reviewed: 2026-08-12

## Identity

- Assignment: BC-041-C1 B-1' return for correction
- Original authorized base: `33b44608cb634d1fedeed7f5f70d405c3999ed02`
- Correction starting point: `54519493189a332e984409504c45210e759f18fc`
- First C1 correction: `80e5b8554639c274f7baa69155ea9b83910f604c`
- First C1 metadata receipt: `54519493189a332e984409504c45210e759f18fc`
- Claude review evidence: `874852c1b548ba4a2539d796d23ab9d803a966c8`
- Work branch: `bc-041-c1-mixed-cf-correction`
- Substantive mixed-placement correction: pending creation
- Metadata receipt: pending creation
- Push status: pending final two-commit push
- Working-tree status: reported externally after the metadata receipt

Claude's review branch was not merged or cherry-picked. Its commit was used
only as the authorized review evidence for this correction.

## Result

```text
BC-041-C1 result: ready_for_fresh_independent_correction_review
B-1': closed by one Cf-removed candidate plus separator-tolerant phrase matching
SUR-001: resolved_at_minimum_phase1_contract_level
Python technical readiness: ready_for_python_phase1
independent correction re-review: required_pending
implementation authorized: false
automatic runtime start: prohibited
```

Technical readiness was set to `not_ready_for_python_phase1` while B-1' was an
active correction and returned to green only after the corrected mechanism and
expanded mixed-placement proof passed. Python Runtime Phase 1 remains unstarted
and unauthorized. Fresh Claude re-review and Dad/Blu integration and closure
remain required.

## Deterministic mechanism

Every Unicode general-category `Cf` code point is removed once before the
existing NFKC, whitespace, separator, collapse, trim, and case-comparison
pipeline. For matching, each normalized inter-word space in a protected rule
matches zero-or-more normalized ASCII spaces in the candidate, while Unicode
word-token guards still bound the complete phrase.

This recovers both cases that formerly conflicted: removal repairs an insertion
inside a token, and a zero-space rule separator recovers a boundary erased by
removal. One candidate handles arbitrary mixtures and repeated insertions, so
candidate count is constant and no placement combination is enumerated.

## Expanded proof

- Same-code-point fixture matrix: six required `Cf` code points x three
  position classes (`boundary`, `inside_token`, `mixed`) x two phases = 36
  safe cases.
- Cross-code-point mixed fixtures: one ingress and one egress case using
  U+200B plus U+FEFF.
- Mutation/adversarial proof: all six required code points at repeat counts 1,
  2, and 4, plus a cross-code-point phrase with repeated insertions throughout;
  every ingress result is `BLOCK` and never model eligible, and every egress
  result is `REDACTED` or `BLOCKED`, never `CLEAR`.
- Existing negative ingress fixtures: 5/5 `PASS`, including
  `punctuation_adjacent_nonmatch`, `shared_words`, and `near_match`.
- Redaction uses the sole decision candidate, rescans with the same matcher,
  and fails closed on overlapping spans, redaction-only output, or a policy
  `BLOCK` action.
- Results, evidence, receipts, and logs remain free of synthetic protected
  values and the synthetic HMAC key.
- Readiness invokes the expanded OPSEC validator; deleting the mixed ingress
  fixture class makes readiness validation fail.

## Claude non-blocking notes

- **N-1 addressed:** synthetic rule references are now opaque numeric fixture
  identifiers, and policy usability rejects a rule reference that reconstructs
  its own normalized value.
- **N-2 addressed:** evidence HMAC is computed from the sole normalized
  candidate used for the match decision.
- **N-3 addressed:** `normalize_text` was replaced with the explicit
  `normalize_rule_text`; candidate normalization has its own separately named
  function, and policy values containing `Cf` are unusable.

## Boundaries and unresolved items

- General Unicode confusable/homoglyph substitution remains explicitly outside
  the minimum matcher and is not classified as semantic paraphrase.
- Production protected policy values, completeness/classification, policy
  location, and expected digest remain external and untested. Missing, invalid,
  or unusable production policy still fails closed.
- SUR-002, SUR-011, and SUR-012 remain unchanged.
- Architecture remains 7 components, 8 packets, and 9 interfaces.
- Golden CTS and the immutable BC-041 review remain unchanged.
- BC-041-C1 `review.md` remains Claude-owned and was not modified in this pass.
- No runtime, LM Studio, Local Mirror, Auth, protected continuation, tool,
  production policy, continuity mutation, or PASS/SkillForge implementation was
  added.
- The known BC-020 fixed-base host-adapter validator finding remains preserved,
  unsuppressed, and is not reported as a pass.

## Next action

Fresh independent Claude C1 review of the exact substantive and metadata
commits. Do not merge this branch and do not start Python Runtime Phase 1.
