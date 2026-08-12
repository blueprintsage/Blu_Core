# BC-041-C1 - Implementation Handoff

status: ready-for-review
owner: Codex
last_reviewed: 2026-08-12

## Identity

- Assignment: BC-041-C1 B-1â€³ return for correction
- Original authorized base: `33b44608cb634d1fedeed7f5f70d405c3999ed02`
- Correction starting point: `c6a447679c0ca07fb38a1e35eeb00231b0cb91e1`
- First correction: `80e5b8554639c274f7baa69155ea9b83910f604c`
- First metadata receipt: `54519493189a332e984409504c45210e759f18fc`
- First Claude review: `874852c1b548ba4a2539d796d23ab9d803a966c8`
- Mixed-placement correction: `2a9d6a28111ca9576bf6811e67ccca37f4d5dd39`
- Mixed-placement metadata: `c6a447679c0ca07fb38a1e35eeb00231b0cb91e1`
- Second Claude review: `f87588d0fa094c203fde3b847ab9bc3c28d1b3fe`
- Work branch: `bc-041-c1-outer-edge-cf-correction`
- Substantive outer-edge correction:
  `85e18f56f88ab113646cc3aab477687eda8b85af`
- Metadata receipt: pending creation
- Push status: pending metadata receipt and final two-commit push

Claude's review branch was not merged or cherry-picked. Its commit was used
only as review authority/evidence. B-1' was independently verified closed; this
pass changes only B-1â€³ and its bounded proof/documentation surface.

## Result

```text
BC-041-C1 result: ready_for_fresh_independent_correction_review
B-1': remains closed
B-1â€³: closed by normalized removed-Cf outer-boundary provenance
SUR-001: resolved_at_minimum_phase1_contract_level
Python technical readiness: ready_for_python_phase1
independent correction re-review: required_pending
implementation authorized: false
automatic runtime start: prohibited
```

Technical readiness is green only after the corrected mechanism and expanded
outer-edge plus preserved mixed-placement proof pass. Python Runtime Phase 1
remains unstarted and unauthorized. Fresh Claude re-review and Dad/Blu
integration and closure remain required.

## Deterministic mechanism

Every Unicode general-category `Cf` code point is removed once before the
existing NFKC, whitespace, separator, collapse, trim, and case-comparison
pipeline. The same candidate retains normalized offsets where one or more `Cf`
code points were removed. Each normalized inter-word rule space matches
zero-or-more ASCII spaces. A complete phrase's outer guard passes only at a
genuine non-word boundary or one of the retained offsets.

Removal and zero-space separator tolerance preserve B-1' interior coverage.
The offsets prevent removal from welding an outer phrase edge to an adjacent
Unicode word token. With no removed-`Cf` offset, ordinary word adjacency still
fails the outer guard. Contiguous unseparated matches of the same protected rule
are collected as one fail-safe run, while unrelated prefix/suffix tokens remain
nonmatches. Candidate count stays one and no placement combination is
enumerated.

## Expanded proof

- Exact fixture matrix: 42 `Cf` probes per phase. For each of six required code
  points, boundary, inside-token, mixed, leading-outer-edge,
  trailing-outer-edge, and both-outer-edge classes are explicit.
- Five distinct attack classes per phase cover outer+interior mixing,
  mixed-code-point outer edges, repeated outer edges, outer plus repeated
  interior insertion, and unseparated self-repetition.
- Deterministic adversarial proof: 54,740 ingress/egress probes with zero
  failures, including exhaustive single/pair interior placements, sampled
  triples, 45,000 randomized 4-12 insertion cases, and repeated outer edges for
  all six code points. B-1' remains closed.
- Six ordinary ASCII/Unicode word-adjacency controls without `Cf` had zero false
  matches. The five pinned negative fixtures remain `PASS`.
- Protected ingress is always `BLOCK` and never model eligible. Protected
  egress is `REDACTED` or `BLOCKED`, never `CLEAR`.
- Redaction uses the sole decision candidate, rescans with the same matcher, and
  fails closed on overlapping spans, redaction-only output, or a policy `BLOCK`
  action. Results, evidence, receipts, and logs remain content-safe.
- Readiness invokes the expanded OPSEC validator; deleting either the mixed
  ingress class or the outer-edge egress classes makes readiness fail.

## Claude documentation and implementation notes

- **Non-`Cf` invisibles disclosed:** the contract and README state that the
  minimum Phase-1 mechanism covers general-category `Cf`, not every Unicode
  default-ignorable, invisible, confusable, or homoglyph mechanism.
- **Zero-space semantics documented:** separator tolerance intentionally treats
  concatenated protected-rule words as a fail-safe match when `Cf` removal may
  have destroyed separation; it is not presented as accidental fuzzy matching.
- **`_has_overlapping_spans` disposition:** reviewed and directly exercised. It
  remains the primary redaction-integrity guard and correctly fails closed on
  overlapping protected spans. B-1â€³ exposed no defect in that interaction, so
  no redaction redesign was made.

## Boundaries and unresolved items

- Production protected policy values, completeness/classification, location,
  and expected digest remain external and untested. Missing, invalid, or
  unusable production policy still fails closed.
- Non-`Cf` default-ignorable/invisible characters and general Unicode
  confusable/homoglyph substitution remain outside the minimum matcher.
- SUR-002, SUR-011, and SUR-012 remain unchanged.
- Architecture remains 7 components, 8 packets, and 9 interfaces.
- Golden CTS, the immutable BC-041 review, and Claude-owned C1 review remain
  unchanged by the correction branch.
- No runtime, LM Studio, Local Mirror, Auth, protected continuation, tool,
  production policy, continuity mutation, or PASS/SkillForge implementation was
  added.
- The known BC-020 fixed-base host-adapter validator finding remains preserved,
  unsuppressed, and is not reported as a pass.

## Next action

Fresh independent Claude C1 review of the exact substantive and metadata
commits. Do not merge this branch and do not start Python Runtime Phase 1.
