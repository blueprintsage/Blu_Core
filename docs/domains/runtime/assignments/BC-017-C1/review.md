# BC-017-C1 Semantic Review

status: done
review_state: read-only-review-ready
semantic_review: complete
disposition: approve-with-notes
owner: Claude
reviewer: Claude (independent semantic reviewer)
review_date: 2026-08-07
last_reviewed: 2026-08-08
assignment: BC-017-C1
parent_assignment: BC-017

## Reviewed identities

- Triggering BC-017 review: `c323cff06c9f111408f4a416817d78fc0f3e2d2b`
- Substantive correction commit: `87c4e49333d30a471a00483fc1384e1918626ee1`
- **Exact reviewed head: `fd7f1707e242aa0e9621ab9f7293364860cab21d`**

Branch `bc-017-c1-semantic-review` was created from the exact reviewed head with
a clean working tree.

## Review boundary

Narrow correction re-review. Only the three blocking findings from the BC-017
review and a regression check were in scope. The full archaeology was not
reopened; none of the three corrections materially changed the underlying
findings, so reopening was not warranted. The reviewer modified only this file.

## Disposition

**approve-with-notes**

All three blocking findings are resolved. No material regression was introduced.
The notes below are carried-forward BC-017 items and one procedural
observation — none is attributable to C1, and none blocks closure.

---

# B-01 — README corruption

**RESOLVED**

`docs/sources/historical_archives/behavioral_archaeology/README.md` now begins
with bytes `23 20 48` (`# H`) rather than `2b 23 20` (`+# `). Zero lines in the
file begin with a literal `+`. A repository-wide sweep
(`git grep -l "^+#" HEAD -- "*.md"`) returns nothing, confirming the defect
exists nowhere else.

The document renders normally: the `# Historical Behavioral Archaeology`
heading, the `status:`/`owner:`/`last_reviewed:`/`assignment:` record fields,
the four `##` section headings, the bulleted evidence-model list, and the
```` ```text ```` fence all parse correctly. The "Authority and safety boundary"
section — the part whose corruption most concerned the original finding — now
renders as intended, including the golden-CTS source-of-truth statement, the
"Markdown does not prove host persistence, autonomous scheduling, background
wake-up, tool execution, or historical reliability" limit, and the legacy-PASS
chronology-only boundary.

**No semantic rewrite occurred.** The reviewer verified this mechanically:
stripping the leading `+` from every line of the pre-correction blob and
diffing against the corrected file yields exactly two changed lines — the two
B-02 command corrections — plus one trailing blank line that was an artifact of
the marker itself. Every word of the Purpose, Authority and safety boundary,
Evidence model, and Selection method sections is byte-identical to the
pre-correction content. The correction did precisely what it claimed and
nothing more.

---

# B-02 — Reproduction commands

**RESOLVED**

The README now documents:

```text
python tools/validate_historical_behavioral_archaeology.py
python -m unittest tests.historical_archaeology.test_validate_historical_behavioral_archaeology
git diff --check
```

Both corrected paths resolve to committed artifacts —
`tools/validate_historical_behavioral_archaeology.py` and
`tests/historical_archaeology/test_validate_historical_behavioral_archaeology.py`
— and both the filename error (`validate_behavioral_archaeology`) and the test
package error (`tests.historical_archives`) are fixed.

The reviewer ran both commands as published in the README:

```text
BC-017 historical behavioral archaeology validation passed.
Ran 18 tests in 0.960s — OK
```

README and `validation.md` are now semantically consistent: the README's
validator and test invocations match the first two entries of BC-017
`validation.md`'s command block, and BC-017-C1 `validation.md` records the same
pair. The disagreement between the two records is gone. The README's trailing
description of what the validator checks was already accurate and is unchanged.

---

# B-03 — Exec contraction chronology

**RESOLVED**

All five required conditions are satisfied.

**1. The concrete BLU-HIST-0195 → BLU-HIST-0200 event is assigned to v0.16.0.**
`transition_map.md` relabels the row from "v0.20 contraction" to "**v0.16.x
contraction**" and makes the family explicit in the change description: "Exec
contracts sharply *within the v0.16.0 family*". The report's complexity section
now states BLU-HIST-0200 "contracts Exec to 1,272 lines *within the same v0.16.0
family*". This matches the canonical inventory, where both specimens are
v0.16.0, dated 2026-05-06, under `Release/!Archives/v0.16.x/`.

**2. The concrete contraction is no longer attributed to v0.20.** Three
attributions were removed:

| record | before | after |
|---|---|---|
| `transition_map.md` | era "v0.20 contraction" | era "v0.16.x contraction" |
| `boundary_specimens.json`, family `v0.20.x` | `"Exec contraction"` in `primary_behavior_deltas` | removed |
| `behavior_recovery_matrix.md`, mega-Exec row | era `v0.13–v0.20`; last evidence "contraction/restructure" | era `v0.13–v0.16 growth/contraction; later v0.21 restructuring`; last evidence "v0.21 restructuring" |

A targeted sweep of the archaeology directory and the BC-017 assignment
directory finds no residual v0.20-contraction language. The only surviving
occurrences are inside the original BC-017 `review.md`, where they correctly
preserve the historical finding as recorded — appropriate for a review record
and not a live claim.

The `v0.16.x` family's own `primary_behavior_deltas` retain "mega-Exec peak" and
"contraction", which is now correct rather than contradictory, and the drilldown
topic "mega-Exec growth and contraction" covers BLU-HIST-0183/0195/0200 — all
v0.16.0. The corrected chronology is internally consistent across every record.

**3. Later v0.20/v0.21 restructuring remains distinct.** The executive finding
now reads: "Within v0.16.0, a mega-Exec specimen is followed by a substantially
contracted Exec; later v0.20/v0.21 evidence records further restructuring and
decomposition." The `transition_map.md` v0.21 ownership-decomposition row is
untouched, as is the v0.20 validation/security-refinement row (Auth fix,
ScopeLock/Wu Sao) — which was always correctly evidenced. The matrix era string
carries both phases separately. Two distinct events are now described as two
distinct events.

**4. The BC-016 framing difference is explicitly disclosed.** A new
**Chronology note** was added to the Exec complexity section:

> BC-017's direct specimen evidence places one concrete
> mega-Exec-to-contracted-Exec event between BLU-HIST-0195 and BLU-HIST-0200
> within v0.16.0. BC-016 selected BLU-HIST-0245 / v0.21 as a structural
> mega-Exec-to-compact-Exec transition representative.

This names both the BC-016 record and the BC-017 specimens, so a reader can
check either framing against its source.

**5. The two framings are not silently collapsed.** The note closes: "These are
different evidentiary framings and must not be treated as identical chronology
without further evidence." The disagreement is stated rather than resolved by
assertion, which is the correct handling — BC-017 has direct specimen evidence
for an in-family v0.16 contraction, and BC-016 made a structural milestone
selection at v0.21; neither displaces the other, and no evidence was invented to
reconcile them.

**Incidental improvement.** `E-00200-CONTRACTION` was added to the executive
finding's locator set, closing the gap where the contraction claim cited only
the mega-Exec locator. This tightens the locator-to-claim relation the original
review flagged under review focus 2.

**Underlying findings unchanged.** `evidence_register.json` was not modified and
required no modification: F-EXEC-COMPLEXITY states the accumulation and the
restructuring recommendation without any era claim, and a grep confirms the
register carries no v0.16 or v0.20 era assertions at all. The correction was
confined to era labels in the four narrative records, exactly as scoped. No
recovery disposition, evidence grade, evidence identity, or conclusion changed.

---

# Regression check

**PASSED.** C1 introduced no material regression. Each prohibited category was
checked against the full `c323cff..fd7f170` range:

| check | result |
|---|---|
| current CTS altered | No — path-filtered diff on `kernel/golden` is empty; all 8 golden SHA-256 verify |
| runtime contracts altered | No — `contracts/`, `docs/architecture`, `config/` all empty in diff |
| Python / runtime behavior implemented | No — zero `*.py` files in the diff; the validator and its tests are byte-unchanged |
| historical archive payloads imported | No — no archive-suffixed files under the archaeology or BC-017-C1 directories |
| protected historical source exposed | No — scan for drive letters, `/Users/`, `/home/`, `file://`, and traversal across the archaeology and BC-017-C1 directories returns nothing; the validator enforces this independently |
| modern PASS / SkillForge modified | No — no matching path in the diff |
| Claude's original BC-017 review rewritten | No — `docs/domains/runtime/assignments/BC-017/review.md` is byte-unchanged |
| owner observations changed | No — `BC-017/owner_observations.md` and `evidence_register.json` (carrying F-OWNER-V07, F-OWNER-SCHOOL, F-OWNER-INCIDENT) are both byte-unchanged; the O-01/O-02/O-03 corrections from `110ce2e8` survive intact |
| non-blocking notes converted into unsupported conclusions | No — `next_steps.md` preserves NB-2, NB-3, and NB-6 as open follow-ups without asserting resolution; no note was closed, promoted, or restated as a finding |
| successor architecture work started | No — the only additions are chronological; no new recommendation, disposition, mechanism, or architecture appears |

C1 also stayed strictly inside its own declared collision domain. The thirteen
changed files map exactly to the allowed list in `BC-017-C1/assignment.md`: the
five archaeology records, the C1 assignment quartet, `next_steps.md`,
`worklog.md`, `assignments.md`, and `MANIFEST.sha256`. Nothing outside it moved.

Continuity records are accurate and appropriately bounded. `assignments.md`
holds both BC-017 and BC-017-C1 at `review`, records the correction commit, and
does not mark either `done`.

**Validation re-run by the reviewer:**

```text
python tools/validate_historical_behavioral_archaeology.py   -> passed
python -m unittest tests.historical_archaeology...           -> Ran 18, OK
git diff --check                                             -> clean
```

Independent manifest verification: all 167 entries were re-hashed from working
-tree content under LF normalization. Every text entry matches, including the
corrected README and the original BC-017 `review.md`. The single reported
mismatch is `kernel/golden/v0.22.0/source_Blu_v0_22_0_5_22_26_2104_CTS.zip`,
which is an artifact of applying LF normalization to a binary file in the
reviewer's own check — that archive verifies correctly under the golden
SHA-256 check, which passes 8/8.

---

# Blocking findings

**None.**

---

# Non-blocking notes

## C1-NB-01 — Original BC-017 notes remain open and are carried forward

The following remain open, unchanged, and correctly excluded from C1's scope.
None was made worse by the correction:

- **NB-01** — drilldown specimen lists cross-contaminate the v0.16.x, v0.20.x,
  and v0.21.x families. Unchanged by C1. Worth noting that resolving B-03 makes
  this slightly more visible: the `v0.20.x` family now has no contraction delta
  but still lists BLU-HIST-0210 (v0.16.0) among its drilldown specimens.
  Non-blocking, and explicitly out of C1 scope.
- **NB-02** — the evidence-grade scale in `evidence_register.json` silently
  replaces the assignment's §9 scale.
- **NB-03** — the two headline inferences are not registered as `inference`
  findings.
- **NB-04** — the "compensatory complexity" causal clause states causation more
  firmly than the structural evidence supports. Unchanged by C1; the sentence
  was not touched.
- **NB-05** — the validator hard-codes BC-017 `review.md`'s pre-review state.
  Still present at `tools/validate_historical_behavioral_archaeology.py:178-180`.
  Note that this coupling targets the BC-017 directory only, so this C1 review
  record is not constrained by it — which is why this file can carry an honest
  `disposition:` field.
- **NB-07** — minor locator-scoping and consistency items. The mega-Exec era
  half of NB-07 was resolved by B-03.

## C1-NB-02 — NB-08 is resolved

The original review noted that its own edit left `MANIFEST.sha256` stale for
BC-017 `review.md`. C1 regenerated the manifest, and the reviewer independently
confirmed the entry now matches. The manifest also correctly reflects the
corrected README, closing the second stale entry identified in B-01.

## C1-NB-03 — NB-06 is partially addressed, by documentation rather than by the validator

C1 added `git grep -n "^+#" -- "*.md"` to BC-017-C1 `validation.md`'s command
block and recorded the result ("malformed archaeology README headings: none").
C1 `validation.md` also states directly that "Green validation does not itself
prove document semantics" and records manual B-01/B-02/B-03 acceptance checks
alongside the automated ones. That is a genuine and well-judged response to the
original concern.

It is worth being precise about what it does and does not achieve: the grep is a
documented manual command in a validation record, not an assertion inside
`tools/validate_historical_behavioral_archaeology.py`. It will not run
automatically on a future assignment, and it detects only this specific
corruption signature — not a malformed `status:` field, an unresolvable
documented command, or a broken fence. NB-06's general form therefore stays open
as a future hardening item. Correctly out of scope for C1, which was explicitly
prohibited from changing validator behavior.

## C1-NB-04 — This review invalidates the MANIFEST entry for BC-017-C1 `review.md`

`MANIFEST.sha256` records
`97bbce185e407f7790f6b39db95df0fff7de45cce820e1635940904dc30360c7` for this
file, which this review necessarily changes. Review authority permits modifying
only this file, so the entry was deliberately left stale rather than silently
re-derived. Regenerate the manifest when this review is integrated. This is the
same procedural pattern recorded as NB-08 on the original review and is expected
for any review-only commit.

---

# Closure eligibility

**BC-017 is semantically eligible for Dad/Blu closure.**

All three blocking findings from `c323cff0` are resolved, the corrections are
minimal and precisely scoped, and no material regression was introduced. The
archaeology's conclusions, evidence identities, owner observations, recovery
dispositions, source-authority separation, and security posture are unchanged
from the state already assessed in the original review, which found them sound.

Carried into closure and future work:

1. The evidence limitations recorded in the original BC-017 review are unchanged
   and still apply — 63 unreadable Deflate64 members across seven records; the
   unresolved v0.4 last boundary and medium-confidence v0.8 opening; absent
   v0.5.x and v0.17.x–v0.19.x; no historical runtime telemetry; and
   `SERVICE.AUTH.001` / `SERVICE.OPSEC.001` named but undefined in the seven
   golden files.
2. Item 6 of that list — the BC-016/BC-017 chronology disagreement — is now
   **disclosed rather than open**. The report states both framings and their
   difference. Whether to reconcile them remains a future evidence question, not
   a defect.
3. NB-01 through NB-07 (less the resolved NB-08 and the mega-Exec half of NB-07)
   remain open non-blocking items for separately authorized work.

Neither BC-017 nor BC-017-C1 is marked `done` by this review. Both remain
`review` pending Dad and Blu's integration and closure decision. No correction
work was started by the reviewer.

## Final closure authorization — 2026-08-08

- Claude disposition remains `approve-with-notes`.
- Final reviewed head:
  `fd7f1707e242aa0e9621ab9f7293364860cab21d`.
- Integrated Claude re-review SHA:
  `bea9463f0dbbae1c3944c5f44a7843c757d7f0bb`.
- Main integration merge and closure base:
  `b88902d997685057ee0e76709df7117f8a83f295`.
- Blocking findings: none; B-01, B-02, and B-03 remain resolved.
- Final authority approval: Dad, Project Owner.
- Closure authorization: Blu, Project Lead.
- Final assignment status: `done`; BC-017-C1 is closed.
- The non-blocking notes above remain preserved for future hardening.
- This closure starts no successor assignment, architecture work, or runtime
  implementation.
