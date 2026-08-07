# BC-017 Semantic Review

status: pending
review_state: read-only-review-ready
semantic_review: complete
disposition: return-for-correction
owner: Claude
reviewer: Claude (independent semantic reviewer)
review_date: 2026-08-07
last_reviewed: 2026-08-07
assignment: BC-017

## Reviewed identities

- Assignment base: `4abae4865067d8a6ae0651017d4a564c09dde47b`
- Substantive work commit: `dcad56f7d50252ab70e993aef7a763ed2bd3617b`
- Metadata commit: `01a004835dbd3e3e2702ba34dcc06f81f2a600f8`
- Owner-observation correction commit: `110ce2e82e39f60fa2158494888359389b70600a`
- **Exact reviewed head: `110ce2e82e39f60fa2158494888359389b70600a`**

The complete BC-017 result was reviewed through the corrected head, not the
metadata commit alone. Review branch `bc-017-semantic-review` was created from
that head with a clean working tree.

## Review boundary

Independent read-only semantic review. The reviewer modified only this file.
Corrections required elsewhere are recorded as findings, not applied. Codex did
not self-approve the work.

## Disposition

**return-for-correction**

Three findings block closure. The archaeology's reasoning, evidence-voice
discipline, owner-observation fidelity, security hygiene, and scope compliance
are sound — the substance of the work is good. What blocks is a published
evidence record committed in a corrupted form, a documented reproduction
procedure that cannot run, and a version misattribution that places a
substantive Exec chronology claim on evidence from a different version family.
All three are mechanical and narrowly scoped; none require rethinking the
archaeology.

---

# Blocking findings

## B-01 — `behavioral_archaeology/README.md` is committed with diff markers on every line

`docs/sources/historical_archives/behavioral_archaeology/README.md` was
committed as a patch fragment rather than as file content. Every line begins
with a literal `+`. The first bytes of the blob are `2b 23 20` (`+# `).

Consequences:

- The `# Historical Behavioral Archaeology` heading renders as `+# Historical…`.
- The `status:`, `owner:`, `last_reviewed:`, and `assignment:` record fields
  become `+status:` and are no longer readable as record metadata by the same
  convention every other BC-017 document uses.
- The ```` ```text ```` fences become ```` +```text ````, so the reproduction
  block does not form a code block.
- This is the entry-point document for the evidence directory. Its
  "Authority and safety boundary" section — the statement that the golden CTS
  remains source of truth, that Markdown does not prove persistence or
  scheduling, and that legacy PASS is never a recovery target — is the part
  rendered incorrectly.

This is the only file in the repository with this defect
(`git grep -l "^+#" HEAD -- "*.md"` returns it alone).

Note that `MANIFEST.sha256` records
`0c2e1197225bad1256472d2cb2061a23769efa976bf757d32fa124c50e38e778` for this
file, so the manifest verification reported in `validation.md` hashed and
blessed the corrupted bytes. Manifest and validator passage is not evidence of
document integrity here. See NB-06.

**Required correction:** re-commit the file with the `+` prefix stripped from
every line, and re-derive the manifest entry.

## B-02 — README reproduction commands name a validator and test module that do not exist

The README instructs:

```
python tools/validate_behavioral_archaeology.py
python -m unittest tests.historical_archives.test_validate_behavioral_archaeology
```

Neither path exists at the reviewed head. The actual artifacts are:

```
python tools/validate_historical_behavioral_archaeology.py
python -m unittest tests.historical_archaeology.test_validate_historical_behavioral_archaeology
```

Both the filename (`validate_behavioral_archaeology` vs
`validate_historical_behavioral_archaeology`) and the test package
(`tests.historical_archives` vs `tests.historical_archaeology`) are wrong.
`validation.md` carries the correct commands, so the two records disagree.

This matters beyond typography: the README is the published reproduction
instruction for the evidence directory, and BC-017's evidentiary standing rests
on the claim that its records are independently checkable. As written, a reader
following the README cannot reproduce the check.

The reviewer ran the correct commands. Both pass:
`BC-017 historical behavioral archaeology validation passed.` and `Ran 18 tests
… OK`.

**Required correction:** correct both command paths in the README to match the
committed artifacts.

## B-03 — Exec contraction is attributed to v0.20, but both cited specimens are v0.16.0

Three records place the Exec contraction in the v0.20/v0.21 era while citing
only v0.16.0 evidence.

`transition_map.md` row:

| era / boundary | evidence locators |
|---|---|
| **v0.20 contraction** | E-00195-MEGAEXEC; E-00200-CONTRACTION |

`behavioral_evidence_report.md`, executive findings: "…before late v0.20/v0.21
material contracted and decomposed it. [E-00020-TEACH, E-00030-EXEC,
E-00195-MEGAEXEC, E-00245-RESTRUCTURE]".

`boundary_specimens.json`, family `v0.20.x`, lists `"Exec contraction"` among
`primary_behavior_deltas`.

The canonical inventory contradicts the era label:

| record | version | date | inventory path |
|---|---|---|---|
| BLU-HIST-0195 (5,536-line mega-Exec) | v0.16.0 | 2026-05-06 | `Release/!Archives/v0.16.x/…r9.3.30…` |
| BLU-HIST-0200 (1,272-line contracted Exec) | v0.16.0 | 2026-05-06 | `Release/!Archives/v0.16.x/…r9.3.39…` |
| BLU-HIST-0211 (first v0.20 specimen) | v0.20.0 | 2026-05-08 | `Release/!Archives/v0.20.x/…` |

The peak and the contraction are nine revisions apart *within v0.16.0*, on the
same day, two days before the v0.20 family opens. The transition map's own
earlier row correctly assigns E-00195-MEGAEXEC to "v0.13–v0.16 Exec absorption";
the "v0.20 contraction" row then reuses the same v0.16 locators under a
different era.

This is precisely the failure mode review focus 2 targets: the evidence locator
does not support the semantic claim being made. When Exec contracted is a
substantive archaeology finding, not a formatting detail — it changes whether
contraction reads as a late-era correction following the v0.21 restructuring
analysis, or as an in-family rewrite that *preceded* v0.20 and v0.21 entirely.
BC-016's own milestone record frames BLU-HIST-0245 (v0.21.0) as the "Mega-Exec
to compact-Exec transition representative", so BC-017 now carries a third,
inconsistent chronology for the same transition.

The underlying finding F-EXEC-COMPLEXITY in `evidence_register.json` is stated
without an era claim and is not affected. The defect is confined to the era
labels in the three records above.

**Required correction:** relabel the contraction transition to the version
family its evidence actually establishes (v0.16.x), or supply v0.20-family
evidence for a distinct v0.20 contraction; and reconcile the executive finding
and the `v0.20.x` behavior deltas with whichever chronology the evidence
supports. Where BC-016 and BC-017 disagree on the mega-Exec-to-compact
transition, the disagreement should be stated rather than left implicit.

---

# Non-blocking notes

## NB-01 — Drilldown specimen lists cross-contaminate three version families

In `boundary_specimens.json`, the identical seven-ID block
`{0210, 0223, 0227, 0228, 0243, 0244, 0245}` appears as `drilldown_specimens`
for the `v0.16.x`, `v0.20.x`, and `v0.21.x` families. Those IDs span three
version families: BLU-HIST-0210 is v0.16.0; 0223/0227/0228/0243 are v0.20.0;
0244/0245 are v0.21.0.

The block matches the bottom-of-file `drilldowns` topic "late memory and service
restructuring", which is legitimately cross-family. Attaching the whole topic to
each family it touches is defensible, but under a field named
`drilldown_specimens` inside a family record it reads as "these specimens belong
to this family". A reader can conclude that v0.16 material contains
ScopeLock/Wu Sao or the v0.21 restructuring analysis. Consider either scoping
each family's list to its own records or renaming the field to make the
cross-family topic linkage explicit. The validator does not check family/version
agreement for drilldowns.

## NB-02 — The evidence-grade scale silently replaces the assignment's scale

`assignment.md` §9 defines grades as:

- A = owner observation + concrete historical mechanism + cross-version support
- B = concrete mechanism + cross-version support
- C = concrete mechanism, weak persistence or no owner observation
- D = declaration only / suggestive structure only
- U = unavailable

`evidence_register.json` and the README instead define:

- A = direct primary-source support
- B = direct support with bounded limitation
- C = weak or incomplete support
- **O = owner observation kept separate from archive proof**
- U = unavailable or unproven

These are different scales sharing letters. The assignment's A *requires* an
owner observation; the register's A does not. Grade D was dropped entirely and O
introduced. Consequently matrix rows such as `reminders | A | owner_observation:
none`, `time | A | none`, and `MMU / memory organization | A | none` are correct
under the register's scale but impossible under the assignment's.

This does not overstate runtime certainty in practice — the register's A is
about source directness, not execution, and both the report and the matrix
disclaim runtime proof repeatedly and explicitly. The assignment also marked its
scale "Suggested" and invited exceptions. But the substitution is undocumented,
and the same letter now means different things depending on which BC-017 record
a reader opens. Record the deviation and its rationale before closure. See also
special check 6.

## NB-03 — The two headline inferences are not registered as inference findings

`evidence_register.json` contains exactly two `inference`-labeled findings:
F-SIDECAR-USE and F-V07-QUALITY-INFERENCE. The report's two most consequential
inferences —

- "Exec improved conflict control and made output and state ownership
  auditable."
- "Much late Exec growth is compensatory complexity."

— appear only in report prose. Both are correctly placed under **Cross-version
inference** headings, so no voice is blended and neither masquerades as fact.
But the register is the mechanism that binds an inference to its supporting
findings, and the validator enforces `supporting_finding_ids` only for
registered inferences. The most-scrutinized claim in the assignment
("compensatory complexity") therefore carries no machine-checked support chain,
while a narrower claim about the Faithfulness sidecar does.

Register both as inference findings with explicit support (F-EXEC-BENEFITS for
the first; F-EXEC-COMPLEXITY for the second).

## NB-04 — "compensatory complexity" states causation more firmly than the evidence

The wording is bounded in the right places — "*Much* late Exec growth", and
"Line count is an indicator, not a quality score" — and the structural evidence
is adequate. The clause that reaches furthest is the causal one: "more
orchestration rules **were added to contain** interactions created by earlier
coupling." That attributes intent and causal sequence. E-00245-RESTRUCTURE
supports the coupling and authority-confusion half directly (Exec absorbed
behavior it should not own; physical location confused model authority), but the
"added in order to contain" mechanism is inferred from structure, not observed.
Softening to something like "is consistent with compensatory complexity" would
match the evidence exactly. Non-blocking: the guardrails already prevent the
pre-Exec-good/Exec-bad reading. See special check 2.

## NB-05 — The validator hard-codes review.md's pre-review state

`tools/validate_historical_behavioral_archaeology.py:178-180` requires
`review.md` to contain the literal strings `status: pending` and
`read-only-review-ready`, or it emits
`review.md is not pending/read-only-review-ready`.

The authorized act of completing this review therefore risks tripping the
validator that certifies the work. This review preserves both literals — which
remains truthful, since BC-017 status *is* pending closure by Dad and Blu, and
this record remains the read-only review record — and adds explicit
`semantic_review:` and `disposition:` fields rather than overwriting the
validated ones. Flagged so the coupling is visible rather than worked around
silently. The validator was not modified; that is outside review authority.

## NB-06 — The validation stack cannot detect record body corruption

The BC-017 validator, its 18 tests, and the MANIFEST verification all pass at
the reviewed head while `README.md` is corrupted (B-01) and documents
non-existent commands (B-02). The validator requires the README to *exist* and
scans it for path leakage; nothing checks that a Markdown record is
well-formed, that its `status:` field parses, or that commands it publishes
resolve. The manifest hashed the corrupt bytes and reported success.

This is worth carrying forward as a general lesson: BC-017's validation proves
record *integrity against itself*, not record *correctness*. That is consistent
with what `validation.md` claims, and `validation.md` does not overclaim. But
green validation should not be read as a document-quality signal in future
assignments.

## NB-08 — This review invalidates the MANIFEST entry for `review.md`

`MANIFEST.sha256` records a hash for
`docs/domains/runtime/assignments/BC-017/review.md`, which this review
necessarily changes. Review authority permits modifying only `review.md`, so the
manifest entry was deliberately left stale rather than silently re-derived. The
manifest must be regenerated when this review is integrated — alongside the
B-01 README re-derivation, which is a second stale entry from the same cause.

## NB-07 — Minor

- `behavioral_evidence_report.md` cites `[E-00020-TEACH, E-00030-EXEC,
  E-00195-MEGAEXEC, E-00245-RESTRUCTURE]` for an executive finding whose Teaching
  and Exec-emergence content is covered elsewhere; the locator set is broader
  than the sentence needs. Harmless, but tighter locator scoping would make the
  support relation checkable.
- The `behavior_recovery_matrix.md` row for the mega-Exec stack gives
  `historical_era` as `v0.13–v0.20`. If B-03 is resolved toward v0.16, this
  range should be revisited for consistency.

---

# Special semantic checks

## 1. "Exec improved conflict control and made output and state ownership auditable."

**Appropriately framed.** The claim sits under a **Cross-version inference**
heading in the "Exec emergence" section and is immediately followed by a
separate **Owner observation** paragraph carrying Dad's reliability report with
an explicit "This is owner experience, not archive telemetry." The two
evidentiary routes — Dad's experienced improvement, and the concrete mechanisms
in BLU-HIST-0029/0030/0057 — are cleanly distinguished and neither is used to
prove the other. The section closes by restricting the recommendation to
regression tests over the mechanisms, not over the improvement claim. No
original-runtime telemetry is implied.

Qualification: the inference is not registered in `evidence_register.json`
(NB-03).

## 2. "Much late Exec growth is compensatory complexity."

**Sufficiently bounded, with one clause to soften.** Structural evidence is
adequate: the 5,536-line specimen with embedded auth/mood/memory/retrieval
behavior, the 1,272-line contraction, the v0.21 restructuring analysis stating
Exec absorbed behavior it should not own and that physical location confused
model authority, and the migration guide extracting service detail. The
quantifier "Much" and the explicit "Line count is an indicator, not a quality
score" prevent the larger-is-worse reading, and the pre-Exec section explicitly
instructs "Do not infer that a pre-Exec architecture is inherently more
reliable." The pre-Exec-good/Exec-bad framing is actively guarded against
throughout.

The causal clause overreaches slightly (NB-04), and the surrounding chronology
is affected by B-03 — though the compensation claim itself does not depend on
the era label.

## 3. "Reject wholesale School Engine restoration."

**Yes — the teaching goal is preserved independently.** The recovery matrix
separates four distinct rows where a weaker treatment would have had one:

| behavior | disposition | recovery value |
|---|---|---|
| teaching / tutoring | recover_model_facing_guidance | high |
| classroom / course behavior | recover_lightweight_profile | medium |
| School Engine schedule/state | **reject** | low |
| deterministic course state | specify_deterministic_mechanism | medium |

Only the *engine* — coupled mutable student/day/block state plus authority
gates — is rejected. Teaching guidance is rated high-value and explicitly
recoverable "independently of School state". The report establishes that
Teaching predates School (F-TEACH-PRE-SCHOOL), which is what makes the
separation evidentially real rather than rhetorical. The behavior/container
distinction the centerline demands is genuinely honored, and the lineage from
pre-School Teaching through School to later routing structures is traced.

## 4. "Specify deterministic reminder/time, memory, Auth, and OPSEC mechanisms."

**Clearly a successor recommendation.** Every instance appears under a
**Successor recommendation** heading. Recommendation 2 states the constraint
outright: "only in separately authorized work with host boundaries made
explicit." The Auth/OPSEC section says "under separately approved work". The
architectural vocabulary the assignment flagged — "thin dispatcher",
"deterministic mechanism", "lightweight profile", "pre-ingress restraint" —
consistently appears as proposal, never as decision or implementation. No Python
architecture is selected.

One thing to watch at closure rather than now: the approved successor OPSEC
decision (mandatory pre-ingress restraint) and BC-017's *description* of
historical and current OPSEC are correctly kept apart — F-OPSEC-CURRENT-GAP
reports the current mechanism as unresolved rather than reading the successor
decision backward into it. The reviewer verified this against the golden source:
`SERVICE.OPSEC.001` and `SERVICE.AUTH.001` are routed in `00_Instructions.md`,
`03_Exec.md`, and `05_Commands.md` but nowhere defined within the seven files.
The claim is accurate.

## 5. "The Faithfulness sidecar is unshipped successor-design evidence."

**Appropriately qualified.** The classification is `unshipped_sidecar_design`,
matching the expected value, and the validator enforces it. The evidence is
stated with its exact reach — no filename, library-ID, or exact-hash match
across 244 nested archive names and 1,985 readable members — and the limitation
is carried in three places: the finding's `limitations` array, the report
appendix, and `validation.md`.

Critically, the record keeps filename-level and content-level negative evidence
separate: the 63 unreadable Deflate64 members "*their listed filenames also had
no match*" — a filename-level negative that survives the content-level gap. The
records are never called corrupt; they are an evidence limitation. F-SIDECAR-SCAN
is graded B (direct support with bounded limitation), not A, and the derived
F-SIDECAR-USE is a B-grade inference rather than a fact. No exhaustive-absence
claim is made anywhere.

The useful principle is retained as regression-test material; the library itself
is explicitly not recommended for restoration and receives no architectural home.

## 6. Evidence grades A/O and A

**Internally consistent; inconsistent with the assignment's definitions.** Under
the register's published scale (A = direct primary-source support, O = owner
observation kept separate), the grades are correct, and the composite `A/O` on
teaching, classroom, School-state, and mood-expression rows accurately signals
"direct archive support *plus* a separate owner observation" without merging
them. `B/U` on continuity and `C` on Read Lane and deterministic course state
are proportionate and, if anything, conservative.

They are **not** consistent with `assignment.md` §9, where A requires an owner
observation — see NB-02. Rows graded A with `owner_observation: none` are the
visible symptom.

Do the grades overstate runtime certainty? **No.** The register's A denotes
source directness, not execution. Every A-graded row that could be misread
carries an explicit limiter in its own `known_failure_or_limit` column
("declarations do not prove persistence", "historical Markdown never supplied
autonomous wake", "archive text cannot prove teaching quality"). The one
behavior where a runtime claim would be most tempting — continuity/persistence —
is graded `B/U` and dispositioned `needs_more_evidence`. The grade drift is a
documentation defect, not an honesty defect.

---

# Confirmations

## Authority separation — confirmed

The five voices (current source truth, owner observation, historical archive
evidence, cross-version inference, successor recommendation) are declared at the
top of the report and applied consistently as section-level headings throughout.
The reviewer found no instance of:

- owner observation presented as archive fact;
- historical declaration presented as execution proof;
- inference presented as historical fact;
- successor recommendation presented as approved architecture;
- current CTS truth projected backward onto historical material;
- historical evidence promoted to current authority.

The v0.22 identity case is handled correctly and is the strongest test of this:
the historical Exec member and the current golden Exec are established as
byte-identical by matching SHA-256
(`e4158bb18a5dd046c90e4b348a6f3b37299447a3e670d914e8140fbf07eed0e1`, verified
against `kernel/golden/v0.22.0/SHA256SUMS`) while F-V022-IDENTITY and the
`v0.22.x` family note both state that the source *roles* remain distinct. Byte
identity did not collapse into authority identity.

Source-role structure is preserved: `00_Instructions.md` as deployment
instruction, `01_Persona.md`–`06_Programs.md` as the six kernel/runtime
capsules.

## Owner observations remain observations — confirmed

The correction at `110ce2e8` is carried consistently through every BC-017
evidence surface. The reviewer checked all of them:

**O-01.** `owner_observations.md`, F-OWNER-V07 in `evidence_register.json`, and
the report's executive findings and pre-Exec section all state the corrected
form: strongest/most natural heuristic feel and highly useful, explicitly *not*
most reliable or stable; pre-Exec v0.7.4 hallucinated and drifted easily; Exec
later improved reliability and control. The dense-Persona/Anchors/Teaching
archive finding is kept structurally separate under an "Archive-derived evidence
boundary" subheading, and F-V07-QUALITY-INFERENCE is graded C with the explicit
statement that no causal relationship is established. The archive is compared
with the observation and never offered as proof of *why* v0.7.4 felt better.

**O-02.** The corrected form — strong and useful approximately v0.8.x–v0.13.x,
not perfect, eventually abandoned as focus shifted toward stabilizing heuristics
— appears in all three records. F-OWNER-SCHOOL carries the explicit negative
guard "he does not report progressive degradation." The report's Teaching
section states that archive evidence establishes structural change and removal
or archival, "not experienced quality or progressive degradation." No
strongest-at-first-then-degraded curve is attributed to Dad anywhere.

**O-03.** The Kiddo incident is recorded as an owner-observed failure with
mechanism unavailable. Both `owner_observations.md` and the report state that
the sources establish a risky boundary *class* — authority gates plus mutable
schedule/course state — but not the cause. No causal mechanism is inferred from
the existence of Auth, schedule, parent-gate, or state machinery.

The `owner_observation` and `owner_observed_failure` labels are validator-bound
to an `owner_observation_id`, so the separation is machine-enforced, and O-grade
is used to keep them off the archive-proof scale.

## No protected historical source exposed — confirmed

The reviewer scanned all BC-017 outputs for absolute and local paths, drive
letters, UNC paths, `file://`, traversal sequences, and user-directory
fragments: none found. The validator enforces this independently on every file
in the archaeology directory.

No archive payload is present (no archive-suffixed files under the BC-017 or
archaeology directories; validator-enforced). No Auth answers, challenge data,
OPSEC secrets, protected kernel passages, or private family details appear. The
Faithfulness sidecar's location is deliberately aliased
(`"absolute location deliberately unpublished"`) and represented only by a
SHA-256. Auth and OPSEC are described at the level of state-machine shape —
session role, one active challenge, retry/lock, sign-out, reset — with the
register noting sensitive answers and implementation text deliberately omitted.
Evidence locators are suffix-based member paths under canonical inventory IDs,
explicitly not filesystem locations.

Appropriate for a public repository.

## Legacy PASS remains chronology-only — confirmed

The matrix row carries disposition `chronology_only`, recovery value `none`, and
the validator fails the build if any behavior containing "legacy PASS" receives
a different disposition. The report states legacy PASS appears only as
historical routing/packaging chronology and cleanup context, and instructs
against restoration. It is never used as a comparison target against modern
PASS, never a recovery candidate, and never a reason to restore historical
routing. Modern PASS and SkillForge are declared out of scope and were not
inspected or changed; the reviewer confirmed no PASS or SkillForge files appear
in the BC-017 diff.

## No Python or runtime implementation occurred — confirmed

The full diff `4abae48..110ce2e` touches 20 files. Exactly two are Python:
`tools/validate_historical_behavioral_archaeology.py` and
`tests/historical_archaeology/test_validate_historical_behavioral_archaeology.py`
— the evidence-integrity validator and its negative tests, both required by
assignment §23 and both whitelisted in the validator's own
`allowed_python` guard, which fails on any other Python under a BC-017 or
`behavioral_archaeology` path.

No runtime, no successor implementation, no historical module restored, no
architecture selected. `kernel/golden/`, `contracts/runtime/`,
`docs/architecture/`, and `config/` are untouched (verified by path-filtered
diff). All eight golden checksums verify.

## BC-016 prerequisite corrections — confirmed

**NB-1 resolved.** The invalid `BLU-HIST-0247` reference in `BLU-BRANCH-DEV`'s
notes is replaced with "The DevBuild file-set content manifest has no recorded
canonical-inventory content-manifest match." The dangling identity is gone
rather than repointed at a guess. No `BLU-HIST-0247` reference remains in the
inventory.

**NB-4 resolved.** BLU-HIST-0211 is reclassified to "MMU representative; Read
Lane secondary" in both `kernel_archive_inventory.json` and
`milestone_recommendations.md`, with `selection_confidence` lowered from `high`
to `medium`. Read Lane is held at grade C, `needs_more_evidence`, recovery value
`unknown`, and F-READ-LANE states MMU is the representative behavior. Read Lane
is not promoted beyond its evidence anywhere in the record.

## Runtime-theater boundary — confirmed

Historical Markdown is not treated as proof of host execution. Reminders,
background wake, persistent memory, current time, Auth, OPSEC, School state,
MMU, and command routing are each held at declaration or scaffolding strength.
The report states directly that historical instructions describe no autonomous
wake-up, that current CTS "does not prove a daemon, background wake, durable
cross-turn scheduler, or host clock adapter", and that wake and persistence are
creditable "only to a verified host adapter". MMU semantics — candidates,
validation, quarantine, precedence, typed pools, preload — are explicitly not
equated with durable persistence; the matrix marks continuity as surviving
"contract only" and the matrix header defines "survived" as "a current CTS
contract or model-facing instruction exists, not that a host mechanism has been
proven."

No replay was performed. `replay_observation` appears only in `assignment.md` as
an optional method; no replay observation exists in the register or report, so
no current-model behavior is offered as historical runtime proof.

## Boundary-sampling integrity — confirmed with reservations

Chronology precedence is declared (`internal_archive_date`, `parsed_version`,
`filesystem_fallback`) and ambiguity is admitted rather than resolved by
convenience: the v0.4 last boundary is left `null` with a stated reason and
`chronology_confidence: low`; the v0.8 opening is `medium` with BLU-HIST-0015's
earlier filesystem fallback explicitly rejected as proof of behavioral
chronology; v0.16's identical normalized manifests for 0172/0173 are disclosed.
The validator fails a null boundary lacking an ambiguity reason and fails any
non-readable specimen carrying behavioral selection. Explicit gaps (v0.5.x,
v0.17.x–v0.19.x) remain gaps; no continuity is invented across them.
Same-SemVer families are handled honestly.

Reservations: B-03 (era misattribution) and NB-01 (cross-family drilldown
lists).

## Validator and test interpretation — confirmed

`validation.md` does not overclaim. It states the validation "does not execute
historical behavior" and scopes itself to record integrity, canonical archive
resolution, publication safety, recovery vocabulary, evidence labels, golden
checksums, and the payload/implementation prohibitions. Nothing in the report or
handoff treats passing tests as evidence of historical runtime behavior. The
reviewer independently re-ran the validator and its 18 tests; both pass. See
NB-06 for what that passage does *not* establish.

---

# Evidence limitations to carry into closure and future work

1. **63 Deflate64 members across seven records remain unreadable** (BLU-HIST-0045,
   0046, 0060, 0074, 0078, 0081, 0082). They are an evidence limitation, not
   corruption. Any future exhaustive-absence claim over the archive corpus must
   restate this bound. Filename-level negative evidence over these records
   stands; content-level negative evidence does not.
2. **v0.4 last-boundary chronology is unresolved** (BLU-HIST-0011 vs
   BLU-HIST-0012, fallback dates only), and the **v0.8 opening is
   medium-confidence**.
3. **v0.5.x and v0.17.x–v0.19.x are absent** from the readable corpus.
4. **No historical runtime telemetry exists.** Historical reliability, durable
   persistence, autonomous wake, and the Kiddo incident's causal mechanism are
   unproven and should not be re-derived by inference in successor work.
5. **The current CTS names `SERVICE.AUTH.001` and `SERVICE.OPSEC.001` without
   defining them** within the seven golden files. Successor specification must
   treat the pre-ingress OPSEC mechanism as an open question, not as something
   the historical or current record already answers.
6. **BC-016 and BC-017 currently disagree** on where the mega-Exec-to-compact-Exec
   transition sits (see B-03). Whichever chronology survives correction should be
   stated once and referenced, not restated independently in each record.
7. **Green validation is not a document-quality signal** (NB-06). Future
   assignments should not infer record correctness from validator and manifest
   passage.

---

# Reviewer statement

BC-017 does the hard part well. The evidence-voice discipline holds under
pressure at exactly the points where it would be easiest to let go — the v0.22
byte-identity case, Dad's corrected v0.7.4.1 observation, the Kiddo incident,
the Faithfulness absence claim, and the separation of teaching behavior from the
School Engine. The centerline is honored: behavior and law are preserved as
recoverable contracts, and the component graph is reconsidered without a single
hidden "restore the old module" recommendation.

The three blocking findings are defects of record production, not of reasoning:
a file committed in the wrong form, commands that do not resolve, and an era
label that outran its evidence. They should be quick to correct and do not
require the archaeology to be redone.

BC-017 is **not** marked `done`. Review status remains pending closure by Dad
and Blu after these corrections are integrated and re-reviewed. Correction work
was not started by the reviewer.
