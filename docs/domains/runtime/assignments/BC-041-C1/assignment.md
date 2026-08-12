# BC-041-C1 - Unicode Format-Character OPSEC Correction

status: review
owner: Codex
reviewer: Claude
project_lead: Blu
project_owner: Dad
domain: runtime
parent: BC-041
last_reviewed: 2026-08-12

## Authorization and identity

Dad and Blu authorized this bounded correction in the assignment supplied to
Codex on 2026-08-11. It corrects only BC-041 B-1 plus the explicitly requested
N-2 review-state ambiguity and N-7 confusable/homoglyph limitation. It does not
redesign BC-041, reopen BC-040, or authorize Python Runtime Phase 1.

- Exact base commit: `33b44608cb634d1fedeed7f5f70d405c3999ed02`
- Starting branch: integrated `main` at the exact base
- Work branch: `bc-041-c1-unicode-format-correction`
- Global index row: `docs/worklogs/assignments.md` (`BC-041-C1`)
- Triggering review: `docs/domains/runtime/assignments/BC-041/review.md`
- Triggering disposition: `return-for-correction`
- Blocking finding: B-1 only

The BC-041 review is immutable audit history. C1 records its correction and
receives an independent review in this assignment folder.

## Objective

Close the deterministic Unicode general-category `Cf` insertion bypass by
evaluating both `Cf -> ASCII space` and `Cf -> removed` candidate views at
ingress and egress, while preserving existing negative behavior, explicitly
excluding general Unicode confusable/homoglyph substitution, and making the
pending independent-review state unambiguous.

## Required source order

1. `AGENTS.md` and `CODEX.md`.
2. `docs/dev/docs_index.md` and `docs/dev/assistant_coding_behavior.md`.
3. `docs/worklogs/assignments.md`, the supplied authorization, and this packet.
4. BC-041 assignment, handoff, validation, and immutable Claude review.
5. The runtime domain index and continuity quartet.
6. OPSEC contracts, synthetic fixtures, nonproduction harness, readiness
   records, validators, and tests.
7. Exact-base, clean-tree, review-finding, and golden-checksum verification.

## Allowed collision domain

```text
contracts/security/opsec/minimum_contract.json
contracts/security/opsec/README.md
tests/security/fixtures/synthetic_cases.json
tools/validate_opsec_contracts.py
tests/security/test_validate_opsec_contracts.py
readiness/python_phase1_readiness_checklist.json
readiness/README.md
tools/validate_python_readiness.py
tests/readiness/test_validate_python_readiness.py
docs/domains/runtime/assignments/BC-041-C1/**
docs/domains/runtime/{worklog,failures,next_steps}.md
docs/worklogs/assignments.md
docs/dev/docs_index.md
MANIFEST.sha256
```

## Protected and prohibited areas

Do not modify `docs/domains/runtime/assignments/BC-041/review.md`, the golden
CTS, Persona, Operations Law, source precedence, architecture registries,
Auth, adapters, continuity contracts, model providers, production policy
values, SUR-002, SUR-011, SUR-012, or PASS/SkillForge. Do not add production
runtime, LM Studio, Local Mirror, Auth, protected-continuation, tool, daemon,
UI, or CLI code.

## Required deliverables

1. Normative dual-view `Cf` treatment for every ingress and egress candidate.
2. Nonproduction harness support that exposes and evaluates both views.
3. Synthetic ingress and egress probes for U+200B, U+00AD, U+200D, U+200C,
   U+FEFF, and U+2060 at a protected word boundary and inside a protected token.
4. Regression proof for all existing negative fixtures.
5. An explicit general Unicode confusable/homoglyph scope exclusion.
6. A finite `required_pending` independent-correction-review state that cannot
   be interpreted as review completion or implementation authorization.
7. Truthful bounded SUR-001 and technical Python-readiness records.
8. Assignment handoff, validation, review placeholder, continuity, index, and
   canonical manifest updates.

## Required checks

Run every validator/test pair named in Dad/Blu's supplied C1 assignment, plus
`git diff --check`, all eight golden checksums, exact architecture counts,
canonical Git-blob manifest completeness/digests, protected-path and
production-code exclusions, synthetic/publication scans, and the known
host-adapter validator without suppressing its fixed-base finding.

## Completion conditions

- B-1 is closed by both required candidate views and match-on-either behavior.
- All 24 required `Cf` ingress/egress position probes fail safely.
- Existing negative fixtures retain their expected behavior.
- N-7 and N-2 are explicitly resolved within the authorized boundary.
- SUR-001 remains honestly resolved at the minimum Phase 1 contract level.
- Technical readiness is green while independent review is `required_pending`
  and runtime implementation is explicitly unauthorized.
- The architecture remains 7 components, 8 packets, and 9 interfaces.
- Golden CTS and the immutable BC-041 review remain unchanged.
- Two reviewable commits are created and the branch is pushed without merge or
  history rewriting.

## Handoff format

Use `handoff.md` and `validation.md` in this folder. Claude modifies only
`review.md` during the separately authorized C1 re-review.

## Approved amendments

### 2026-08-12 - B-1' mixed-placement return for correction

- **Approved by:** Dad and Blu, by explicit instruction supplied to Codex on
  2026-08-12.
- **Correction starting point:**
  `54519493189a332e984409504c45210e759f18fc`.
- **Review authority/evidence:** Claude's independent review commit
  `874852c1b548ba4a2539d796d23ab9d803a966c8`, which must not be merged or
  cherry-picked.
- **Correction branch:** `bc-041-c1-mixed-cf-correction`.
- **Blocking finding:** B-1' only. The two static candidate views are
  complementary rather than complete; mixed boundary and inside-token `Cf`
  insertions can corrupt both views in one protected phrase.
- **Superseded claim:** the prior completion statement that exactly two static
  views close B-1 is withdrawn. The corrected deterministic mechanism must
  cover arbitrary mixtures and counts of general-category `Cf` insertions
  without enumerating placement combinations or generating an exponential
  candidate set.
- **Expanded proof:** preserve all six required code points and both original
  position classes; add a mixed-placement class for every code point at ingress
  and egress, cross-code-point mixed probes, repeated/mutation probes, the five
  existing negative fixtures, safe redaction/rescan behavior, content-safe
  evidence, and a readiness guard that cannot turn green without this proof.
- **Readiness during correction:** B-1' is an active technical blocker. The
  repository must report `not_ready_for_python_phase1` until the corrected
  mechanism and expanded proof pass. Independent Claude re-review, Dad/Blu
  closure, `implementation_authorized: false`, and automatic-start prohibition
  remain separate even after technical readiness is re-earned.
- **Scope:** the original collision domain and protected/prohibited areas remain
  authoritative. `BC-041/review.md` and this assignment's Claude-owned
  `review.md` must not be changed during correction.
- **Commit method:** one substantive correction commit followed by one metadata
  receipt recording its SHA; push without merge, then stop for a fresh Claude
  review.

### 2026-08-12 - B-1â€³ outer-edge return for correction

- **Approved by:** Dad and Blu, by explicit instruction supplied to Codex on
  2026-08-12.
- **Correction starting point:**
  `c6a447679c0ca07fb38a1e35eeb00231b0cb91e1`.
- **Review authority/evidence:** Claude's second independent review commit
  `f87588d0fa094c203fde3b847ab9bc3c28d1b3fe`, which must not be merged or
  cherry-picked.
- **Correction branch:** `bc-041-c1-outer-edge-cf-correction`.
- **Blocking finding:** B-1â€³ only. B-1' is independently verified closed. The
  single `Cf`-removed candidate loses evidence that a removed outer-edge `Cf`
  separated the protected phrase from an adjacent Unicode word token, so the
  outer token guard can reject a protected match.
- **Corrected property:** retain normalized boundary provenance for removed
  `Cf` runs on the same single candidate. An outer guard may pass at a genuine
  non-word boundary or a retained removed-`Cf` boundary, while ordinary word
  adjacency without such provenance remains a nonmatch. Unseparated repeated
  instances of the same protected rule must also fail safely.
- **Expanded proof:** for all six required code points at ingress and egress,
  add explicit leading, trailing, and both-outer-edge fixtures, plus outer and
  interior mixing, mixed code points, repeated outer insertions, repeated
  interior insertions, unseparated self-repetition, Unicode adjacency negative
  controls, preserved B-1' adversarial coverage, redaction rescan, content-safe
  evidence, and readiness coupling.
- **Documentation notes:** disclose non-`Cf` default-ignorable/invisible
  characters as outside the bounded Phase-1 claim, and state that zero-space
  protected-rule separators are intentional fail-safe recovery rather than
  accidental fuzzy matching. Record `_has_overlapping_spans` disposition
  without redesign unless a defect is found.
- **Readiness:** B-1â€³ is a technical blocker until the expanded matrix passes.
  Technical readiness may then return to `ready_for_python_phase1`, but Claude
  re-review remains pending, `implementation_authorized` remains false,
  automatic startup remains prohibited, and Dad/Blu closure remains required.
- **Scope and commit method:** the existing collision domain and prohibitions
  remain authoritative. Create one substantive correction commit and one
  metadata receipt, push without merge, and stop for another Claude review.
