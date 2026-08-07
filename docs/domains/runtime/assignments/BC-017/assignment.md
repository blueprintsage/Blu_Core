# BC-017 — Assignment Record

status: review
owner: docs/domains/runtime
last_reviewed: 2026-08-07
approved_by: Dad and Blu
implementation_owner: Codex
semantic_reviewer: Claude
exact_base: 4abae4865067d8a6ae0651017d4a564c09dde47b
branch: bc-017-historical-behavioral-archaeology

## Approved packet

The following handoff is preserved verbatim as the approved BC-017 packet.

# BC-017 — Historical Behavioral Archaeology
# Codex Implementation Handoff

## Authorization

Project Owner: Dad
Project Lead / integration reviewer: Blu
Implementation owner / Git steward: Codex
Semantic reviewer: Claude

Dad and Blu authorize BC-017.

This assignment performs historical behavioral archaeology only.

It does NOT authorize:
- Python Blu runtime implementation;
- successor-control-plane implementation;
- restoration of historical modules;
- modification of the current CTS;
- replacement of current source authority;
- import of historical kernel ZIPs into Blu_Core;
- revival of legacy PASS;
- final successor architecture selection.

---

## Exact base

Start from:

4abae4865067d8a6ae0651017d4a564c09dde47b

This is the closed BC-016 base.

Before creating the branch:

git fetch origin --prune
git checkout main
git pull --ff-only origin main
git rev-parse HEAD
git status --short

HEAD MUST equal:

4abae4865067d8a6ae0651017d4a564c09dde47b

If main has advanced, STOP and report the new SHA before proceeding.
Do not silently rebase this assignment onto a different base.

Create:

bc-017-historical-behavioral-archaeology

Use a fresh Codex thread for this assignment.

Do not force-push, rewrite, squash, or rebase published history.

---

# 1. Purpose

Determine what historical Blu actually gained, lost, retained, or compensated for across kernel generations.

The centerline is:

PRESERVE THE BEHAVIOR AND LAW;
RECONSIDER THE COMPONENT GRAPH.

BC-017 is not a module-restoration exercise.

Its job is to identify useful behavior and the machinery that supported it, distinguish functioning/scaffolded behavior from declarations, locate important behavioral transitions, and recommend how behavior should be treated in later successor design.

The assignment must answer:

1. What made historical Blu useful?
2. What behaviors survived across multiple generations?
3. What capabilities were declared but weakly supported?
4. What capabilities had concrete implementation/scaffolding?
5. What did Exec genuinely improve?
6. Where did Exec or other orchestration become compensatory complexity?
7. What behavior is worth recovering?
8. What historical architecture should NOT be restored?
9. Which behavior is best expressed later as:
   - model-facing guidance;
   - lightweight profile;
   - deterministic machinery;
   - regression test;
   - chronology only;
   - reject / do not recover?

No Python implementation is permitted in this assignment.

---

# 2. Source authority

Preserve these source classes distinctly.

## Current authority

Current runtime authority remains:

kernel/golden/v0.22.0/**

Role distinction:

00_Instructions.md
= deployment_instruction

01_Persona.md through 06_Programs.md
= kernel_runtime_capsule

The current CTS is the endpoint/current-authority comparison source.

It must NOT be treated as proof that every later design choice was historically superior.

## Historical evidence

Historical kernels are behavioral evidence only.

They are NOT current authority.

Use the canonical BC-016 inventory and source map to identify historical specimens.

Do not let historical content redefine the current CTS.

## Project Owner observations

Dad's recollections are valuable behavioral observations.

They must be labeled:

owner_observation

They are not archive-derived proof.

Archive evidence may:
- support them;
- contradict them;
- partially support them;
- remain insufficient.

Do not rewrite owner observations into source-derived facts.

## Extracted contracts

Existing extracted runtime contracts remain descriptive indexes.

They do not outrank the CTS.

## Proposed successor implications

Recommendations produced by BC-017 are recommendations only.

They must be labeled as successor implications or recovery recommendations.

They do not become approved architecture merely by appearing in the report.

---

# 3. External source boundary

Use Dad's historical Kernel source and/or the stable Kernel snapshot already reconciled under BC-016.

Do NOT commit:

Kernel.zip

or any historical nested ZIP.

Do NOT copy historical kernels into Blu_Core.

Do NOT commit temporary extraction directories.

Do NOT commit Dad's absolute filesystem paths.

Use sanitized source aliases and BC-016 archive IDs.

The known stable Kernel snapshot receipt from the completed inventory work is:

filename: Kernel.zip
sha256:
0195ab2623e2bdd9d2da5b8f18170f238bb4dbd5df489e543589de112eba6613

Before relying on an external snapshot, verify its identity against committed BC-016 receipt data.

Use temporary extraction outside the repository.

Clean temporary extraction after analysis.

Seven Deflate64 archives were previously classified:

availability_status: unsupported_format
integrity_status: not_tested

Do not call them corrupt.

Do not invent behavior from unreadable archives.

---

# 4. Mandatory BC-016 preflight corrections

BC-017 may not rely on the affected records until NB-1 and NB-4 are resolved.

These corrections are in scope because BC-016 explicitly carried them forward as prerequisites for BC-017.

Do not broaden this into a general BC-016 cleanup assignment.

## NB-1

Affected record:

BLU-BRANCH-DEV

Current note incorrectly references:

BLU-HIST-0247

The canonical BLU-HIST range ends at:

BLU-HIST-0246

Resolve conservatively.

Unless the external discovery source positively proves an external-numbering identity, replace the invalid canonical reference with an honest statement equivalent to:

"The DevBuild file-set content manifest has no recorded canonical-inventory content-manifest match."

Do not invent the intended ID.

Maintain JSON/CSV agreement if the corresponding field is represented in both.

## NB-4

Affected milestone:

BLU-HIST-0211

Current combined characterization overstates Read Lane evidence.

Preserve the selected archive.

Reframe it as:

MMU representative; Read Lane secondary

The evidence supporting MMU is strong.
Read Lane is secondary and must not be presented as the primary reason for selection.

If the existing scalar `selection_confidence` semantically applies to the complete combined claim, lower it to `medium`.

Do not change the inventory schema merely to express separate confidence values.

Update both canonical JSON and milestone Markdown as required.

Do not change the milestone selection itself.

## Other BC-016 notes

NB-2, NB-3, NB-5, NB-6, NB-7, NB-8, NB-9, and NB-10 remain preserved.

Do not expand BC-017 into a broad validator-hardening assignment.

Address another NB only if BC-017 necessarily touches the exact affected evidence and the smallest truthful correction is required.

Otherwise carry it forward.

---

# 5. Project Owner observations / hypotheses

Create a clearly labeled owner-observation record for BC-017.

Record these as hypotheses and historical recollections, NOT archive truth.

## O-1 — v0.7.4

Dad remembers the v0.7.4 generation as the best historical Blu in terms of feel / heuristic behavior.

This does NOT mean it was the most reliable Blu.

Dad specifically remembers that pre-Exec Blu:
- hallucinated relatively easily;
- drifted relatively easily;
- relied heavily on brute-force/model-facing Markdown.

v0.7.4 should therefore be treated as:

a behavioral / qualitative control specimen,
NOT an architectural target.

The archive specimen is expected to include the v0.7.4.1 line.
Resolve its canonical archive ID from BC-016 rather than hardcoding one.

## O-2 — Exec

Dad remembers Blu becoming better after Exec appeared.

BC-017 must NOT begin from the hypothesis that Exec harmed Blu.

Instead test:

Which Exec additions solved real reliability, hallucination, drift, routing, validation, or state problems?

Then:

At what point, if any, did additional Exec/orchestration complexity stop producing proportional behavioral benefit and begin compensating for unreliable components?

Do not presume a breakpoint.
Find evidence.

## O-3 — School Engine / classroom goal

The original School Engine goal was:

Blu could be a classroom.

Dad remembers the classroom/teaching system as strong and useful, approximately during the v0.8.x through v0.13.x period.

Dad also remembers imperfections in state/workflow integrity.

One owner-observed incident involved Kiddo being unable to remember a password and creating a new class schedule rather than continuing the prior one.

Treat that incident only as:

owner_observation

unless historical source evidence supports the exact mechanism.

Do NOT begin with the assumption that School Engine itself should migrate.

Investigate:

What teaching/classroom behaviors were valuable?

Which were School Engine-specific machinery?

Could the valuable teaching behavior survive without restoring School Engine?

## O-4 — high-priority recovery behaviors

Dad identifies these historical capabilities as known-value investigation targets:

- Teaching / Blu-as-classroom
- Reminders
- Time
- Mood
- MMU
- Auth
- OPSEC

These receive priority archaeology.

This priority does NOT pre-decide their future architecture.

## O-5 — uncertain / secondary behavior

Other behavior, including Read Lane and miscellaneous historical modules, is evidence-driven.

Do not assume it deserves migration simply because it existed.

Promote secondary behavior into recovery consideration only when evidence shows material value.

---

# 6. Historical sampling method

Use a:

BOUNDARY-FIRST, CHANGE-POINT DRILL-DOWN

method.

Do NOT exhaustively perform equal-depth analysis on all 244 archives.

Dad's preferred first-pass method is:

inspect the first and last meaningful specimen of each historical semver family.

This should expose major behavior changes cheaply.

Then inspect intermediate specimens only where the boundary pair shows a meaningful transition.

## 6.1 Re-derive family set

Do not trust this handoff blindly.

Re-derive the available historical version families from the canonical BC-016 inventory.

The stable Kernel snapshot is expected to contain Release archive families approximately:

v0.3.x
v0.4.x
v0.6.x
v0.7.x
v0.8.x
v0.10.x
v0.11.x
v0.12.x
v0.13.x
v0.14.x
v0.15.x
v0.16.x
v0.20.x

and later DevBuild material for approximately:

v0.21.x
v0.22.x

A v0.9-era source-folder record also exists in BC-016 evidence, but it must not be treated as a complete archive unless its contents actually support that classification.

Known gaps must remain gaps.

Do not invent v0.5, v0.9 archive completeness, v0.17, v0.18, v0.19, or any other missing version line.

If the canonical inventory disagrees with the expectation above, the canonical inventory wins and the discrepancy must be reported.

## 6.2 "First" and "last" definition

Do NOT use:
- ZIP entry ordering;
- filesystem timestamp fallback;
- arbitrary filename sorting;
- inventory ID order;

as proof of chronology.

Determine boundary specimens using the strongest available combination of:

1. semantic version progression;
2. explicit timestamp/date encoded in archive identity;
3. internal kernel version/date metadata;
4. other explicit historical metadata already accepted by BC-016.

Filesystem fallback dates may not establish chronology.

If exact ordering remains ambiguous:
- record the ambiguity;
- identify boundary candidates;
- do not fabricate an exact first/last ordering.

For families with one valid specimen:

first = last

and mark:

single_specimen_family: true

## 6.3 Same-version repeated builds

Some historical families contain many builds with the same semantic version but different timestamps, patches, revisions, or phase labels.

These are meaningful.

If the semantic version is identical but the family evolved materially under timestamped/revision builds:

compare the earliest and latest reliably ordered specimens.

Do not collapse them merely because the SemVer string is unchanged.

---

# 7. Boundary comparison rubric

Run the same compact behavioral-source rubric against each first/last pair.

This is not a live historical-runtime claim.

For each behavior surface record:

- present / absent
- declared owner
- source member(s)
- trigger / ingress
- state model
- persistence model
- host/tool dependency
- user-visible behavior
- validation/gate involvement
- Exec involvement
- failure/fallback behavior
- source-authority behavior
- evidence class
- confidence
- first→last delta

Do not interpret file-name presence as proof of functioning behavior.

---

# 8. Evidence classes

Every behavioral claim must carry an evidence class.

Use at least:

## current_source_truth

Current CTS statement.

## historical_declared

Historical source explicitly declares behavior.

Declaration alone is not proof that it worked.

## historical_mechanically_scaffolded

Historical source includes concrete ownership, inputs, state, branching, routing, validation, or workflow machinery sufficient to show more than a bare declaration.

## cross_version_persistent

Substantially similar behavior/mechanics recur across multiple independent historical specimens.

## owner_observation

Dad reports the behavior from actual historical use.

## owner_observed_failure

Dad reports a concrete historical failure or limitation.

## replay_observation

Only if a current-host replay is deliberately performed.

Replay observation MUST be labeled host/model-dependent and MUST NOT be presented as proof of how the original historical model behaved.

Replay testing is optional and not required for BC-017.

## inference

Analytical conclusion drawn from evidence.

Must identify its supporting evidence.

## unavailable

Source cannot be read or evidence is insufficient.

---

# 9. Evidence strength

Use a compact evidence grade to avoid pretending we have original runtime telemetry.

Suggested:

A
= owner observation + concrete historical mechanism + repeated/cross-version support

B
= concrete historical mechanism + repeated/cross-version support

C
= concrete mechanism but weak persistence or no owner observation

D
= declaration only / suggestive structure only

U
= unavailable / unreadable / insufficient evidence

Do not mechanically promote an owner recollection to A if the source contradicts it.

Explain exceptions.

---

# 10. Primary behavior tracks

## 10.1 Teaching / Blu-as-classroom

This is a primary Tier-1 track.

Inspect:

- tutoring posture;
- explanation/scaffolding;
- curriculum behavior;
- lesson generation;
- checks for understanding;
- adaptation to student ability;
- practice/drills;
- class/course structure;
- schedule handling;
- student/class state;
- continuity;
- identity/password/access mechanics if present;
- progress tracking;
- School Engine ownership;
- relationship between Teaching and School Engine;
- relationship between School Engine and Exec;
- what behavior existed before School Engine;
- what behavior survived after School Engine.

Answer separately:

A. What made Blu capable of teaching?

B. What made Blu capable of behaving like a classroom?

C. Which of those behaviors were valuable independent of School Engine?

D. Which School Engine mechanics were brittle, redundant, or not worth recovering?

Do not recommend restoring School Engine merely because the teaching behavior was good.

The preferred recovery target is behavior, not container.

## 10.2 Reminders

Inspect:

- reminder creation;
- representation of due time;
- queue/state ownership;
- recurrence if any;
- acknowledgement behavior;
- persistence claims;
- host limitation handling;
- failure behavior;
- Exec integration;
- user-visible confirmation;
- whether reminders were actually scaffolded or mostly prompt-declared.

Separate:
"reminder reasoning"
from
"real future wake/scheduling capability."

Historical Markdown must not be credited with daemon/background behavior it could not actually provide.

## 10.3 Time

Inspect:

- date/time source;
- current-time lookup;
- timezone handling;
- date arithmetic;
- host/tool dependencies;
- fallback behavior;
- fabricated-time prevention;
- relation to reminders;
- evolution into a dedicated Time Service if present.

## 10.4 Mood

Inspect:

- source of mood;
- whether mood drove behavior or reflected behavior;
- rendering;
- glyph/swatch/trait output;
- Persona involvement;
- Exec/command involvement;
- state storage;
- command surface;
- changes in ownership over generations;
- whether later complexity improved behavior or merely constrained rendering.

Do not project current Persona mood law backward onto history.

## 10.5 MMU / memory machinery

Inspect:

- memory categories;
- retrieval;
- staging;
- commit;
- preload;
- context paging;
- persistence claims;
- state transitions;
- archive/source handling;
- relationship to StateTree where applicable;
- relationship to current-model continuity;
- what MMU solved that Persona/model memory alone did not.

Do not equate organizational machinery with durable platform persistence.

## 10.6 Auth

Inspect:

- authorization purpose;
- route position;
- challenge/answer flow;
- session state;
- logout/reset;
- host dependence;
- nondeterminism;
- failure handling;
- relationship to protected actions.

Do not publish protected challenge answers, secrets, or sensitive source text.

## 10.7 OPSEC

Inspect:

- protected-source objective;
- ingress position;
- route/gate behavior;
- clone/recreation protections;
- source-disclosure restraint;
- Auth interaction;
- Exec interaction;
- whether it operated as route, restraint, service, or mixed mechanism across generations;
- concrete enforcement machinery versus declaration.

Do NOT project the approved successor decision backward.

Successor decision is:

OPSEC becomes a mandatory pre-ingress security restraint.

Historical report must separately state what old kernels actually declared.

Never publish sensitive OPSEC source text.

---

# 11. Exec archaeology

Exec gets its own cross-version analysis because Dad reports a real behavioral improvement after its introduction.

Track at least:

- first appearance;
- early role;
- routing responsibilities;
- validation;
- gates;
- anti-drift;
- source authority;
- ownership discipline;
- output/print control;
- error/fail-closed behavior;
- state orchestration;
- ScopeLock/Wu Sao emergence where relevant;
- module count;
- line count / structural size where already available;
- number/type of compensating gates;
- relationship to known unstable components.

The central question is NOT:

"Was Exec bad?"

The central questions are:

1. What real problems did Exec solve?
2. Which Exec behaviors should survive?
3. Which later Exec responsibilities were accumulated because other components were unreliable?
4. Which responsibilities belong in a future deterministic control plane?
5. Which responsibilities should remain model-facing rather than be reproduced as orchestration code?
6. What should never be rebuilt as a mega-Exec?

Do not infer causation merely from file size.

Large Exec != bad.
Small Exec != good.

Tie claims to behavior and ownership.

---

# 12. Change-point drill-down

For each semver family:

1. Compare first boundary specimen.
2. Compare last boundary specimen.
3. If no material delta appears for priority behavior:
   - record no material boundary delta;
   - stop for that track/family.
4. If a material delta exists:
   - inspect the smallest useful number of intermediate specimens necessary to localize the transition.

Prefer change-point narrowing over linear exhaustive reading.

Where reliable chronology exists, a binary-search-like intermediate strategy is encouraged.

A drill-down is justified when any of these materially changes:

- capability appears/disappears;
- ownership changes;
- route changes;
- state model changes;
- persistence claim changes;
- gate/validation changes;
- user-visible workflow changes;
- primary behavior becomes materially stronger/weaker;
- Exec absorbs or releases responsibility;
- component changes from declaration to concrete machinery;
- historical behavior relevant to a Tier-1 recovery target changes.

Do not drill down merely because wording changed.

---

# 13. BC-016 milestone anchors

The eight BC-016 milestones remain approved deep-analysis anchors.

They are NOT the only archives BC-017 may inspect.

Use them to:
- cross-check the boundary scan;
- anchor major eras;
- deepen known high-signal behavior;
- verify that boundary sampling did not miss obvious transitions.

Do not treat milestone labels as behavioral conclusions.

The BC-016 milestone set was selected structurally.

BC-017 supplies the behavioral analysis.

---

# 14. v0.7.4 control specimen

Regardless of whether it lands as a family boundary or BC-016 milestone:

inspect the available v0.7.4.x specimen directly.

Use it as a qualitative pre-Exec control.

Questions:

- How much behavior lived directly in Persona/Teaching/Commands?
- How much routing/orchestration existed before Exec?
- What anti-drift controls existed?
- What source grounding existed?
- What made the build simple?
- What left it vulnerable to hallucination/drift?
- Which desirable behaviors later survived Exec?
- Which desirable behaviors were lost or obscured?

Do NOT recommend reverting to pre-Exec architecture.

---

# 15. Legacy PASS exclusion

Legacy PASS is chronology-only.

Historical PASS may be inspected only when necessary to:

- establish chronology;
- explain old Exec coupling;
- explain orchestration compensation;
- distinguish historical capability transitions.

Legacy PASS must NOT be:

- a recovery candidate;
- recommended for restoration;
- treated as an architectural precedent;
- used as successor PASS design;
- compared competitively with modern PASS;
- allowed to redefine current SkillForge/PASS work.

Do not spend BC-017 effort deciding whether legacy PASS should return.

Modern PASS/SkillForge belongs to a separate workstream and is owned by the other Blu instance.

Do not inspect or modify the modern PASS archives for this assignment unless Dad explicitly changes scope.

---

# 16. Faithfulness sidecar

An owner-supplied historical draft exists:

EXECLIB.FAITHFULNESS.001.md

It is dated 2026-05-08 and marked draft.

Prior inspection found no copy of the filename/lib_id/text inside the 244 archived kernel ZIPs.

BC-017 should independently verify that classification if the sidecar is available.

If confirmed, classify it as:

unshipped_sidecar_design

NOT:

shipped_historical_behavior

It may be discussed in a short adjacent-design appendix because it appears to preserve a potentially useful behavioral requirement:

source-bound factual output should require positive source support, not merely absence of contradiction.

Do not restore the historical library.

Do not select its future architectural location.

Record the principle as successor-design evidence only.

---

# 17. Security / publication boundary

Blu_Core is public.

Historical kernels are private/protected evidence.

BC-017 MUST NOT publish protected historical source text into the repository.

Do not copy:
- full historical kernel sections;
- Auth challenge answers;
- protected ID material;
- OPSEC implementation secrets;
- private family content;
- private continuity vault material;
- protected prompts;
- private local paths.

Use sanitized evidence locators.

Preferred evidence locator:

archive_id
member_path
member_sha256 or normalized evidence hash
section/heading where safe
evidence_class
sanitized semantic summary

Short non-sensitive labels may be used where necessary.

For Auth/OPSEC, prefer semantic summaries over quotations.

The report must be auditable without becoming a kernel-leak artifact.

---

# 18. Required deliverables

Follow repository assignment-record standards and existing conventions.

Create at minimum:

docs/domains/runtime/assignments/BC-017/assignment.md
docs/domains/runtime/assignments/BC-017/handoff.md
docs/domains/runtime/assignments/BC-017/validation.md
docs/domains/runtime/assignments/BC-017/review.md
docs/domains/runtime/assignments/BC-017/owner_observations.md

Create a sanitized archaeology area under the existing historical-source domain, for example:

docs/sources/historical_archives/behavioral_archaeology/

with at minimum:

README.md
boundary_specimens.json
behavior_recovery_matrix.md
behavioral_evidence_report.md
transition_map.md

If repository conventions strongly prefer different names, preserve equivalent separation and explain the deviation.

Also add:

tools/validate_historical_behavioral_archaeology.py

and:

tests/historical_archaeology/test_validate_historical_behavioral_archaeology.py

or the repository-standard equivalent.

Update:

docs/worklogs/assignments.md
docs/domains/runtime/worklog.md
docs/domains/runtime/next_steps.md
MANIFEST.sha256

Do not update current architecture documents with successor decisions.

---

# 19. boundary_specimens.json minimum content

Each family record should contain at least:

family
family_source_type
first_specimen_archive_id
last_specimen_archive_id
first_version_label
last_version_label
selection_basis
chronology_confidence
single_specimen_family
boundary_ambiguity
primary_behavior_deltas[]
drilldown_required
drilldown_specimens[]
notes

Do not require a fake first/last ID when unavailable.

Use null plus an explicit reason.

---

# 20. Behavior recovery matrix

The matrix must be behavior-centered, not module-centered.

At minimum include rows for:

- teaching / tutoring
- classroom / course behavior
- School Engine schedule/state behavior
- reminders
- time
- mood
- MMU / memory organization
- Auth
- OPSEC
- Exec anti-drift / stability
- source-grounding / faithfulness behavior
- continuity
- Read Lane if evidence warrants
- any unexpected behavior promoted by evidence

Suggested columns:

behavior
historical_era
first_strong_evidence
last_strong_evidence
evidence_classes
evidence_grade
owner_observation
mechanism_summary
known_failure_or_limit
exec_dependency
host_dependency
survived_to_current_cts
recovery_value
recommended_disposition
rationale
evidence_locators

Allowed recommended_disposition values:

recover_model_facing_guidance
recover_lightweight_profile
specify_deterministic_mechanism
retain_regression_test
chronology_only
reject
needs_more_evidence

Do not create a "restore module" disposition.

---

# 21. Behavioral evidence report

The report must distinguish:

A. current source truth
B. owner observation
C. historical archive evidence
D. cross-version inference
E. successor recommendation

Never blend these into one prose voice.

The report should include:

## Executive findings

What changed materially across Blu history?

## Pre-Exec control

v0.7.4.x findings.

## Exec emergence

What improved and how?

## Teaching/classroom lineage

Teaching and School Engine evolution.

## Reminder/time lineage

## Mood lineage

## MMU lineage

## Auth/OPSEC lineage

## Exec complexity / compensation analysis

## Secondary discoveries

## Rejected restoration candidates

## Legacy PASS chronology note

## Faithfulness sidecar appendix

## Recovery recommendations

## Unknowns / evidence gaps

---

# 22. Transition map

Create a concise chronology of major behavioral changes.

Do not pretend every semver boundary is significant.

Record only meaningful transitions such as:

- capability introduction;
- ownership move;
- major state-model change;
- major validation change;
- Exec absorption;
- Exec simplification;
- behavior disappearance;
- behavior survival under new architecture.

Each transition must cite sanitized evidence locators.

---

# 23. Validator requirements

The new validator should remain small.

Do not build a giant behavioral inference engine.

It should validate the integrity of the produced evidence records.

At minimum verify:

- every archive_id resolves to the canonical BC-016 inventory;
- no unknown archive IDs;
- no absolute/local path leakage;
- no `..`, UNC, file://, or encoded traversal leakage in published records;
- every boundary record has a selection basis;
- unsupported/unavailable specimens cannot carry invented behavior;
- every recovery-matrix row has an allowed disposition;
- every factual historical finding has at least one evidence locator;
- owner observations are labeled as owner observations;
- current CTS claims are labeled current_source_truth;
- inference is not mislabeled archive fact;
- legacy PASS cannot receive a recovery disposition;
- Faithfulness sidecar cannot be labeled shipped unless direct archive evidence exists;
- no committed ZIP/archive payload was added;
- current golden CTS files remain unchanged;
- no Python runtime/control-plane implementation appears in BC-017 output;
- review.md begins pending/read-only-review-ready rather than self-approving.

Add focused negative tests for each invariant.

Do not modify BC-016's validator merely because BC-017 has a new validator.

---

# 24. No live-runtime theater

BC-017 is historical archaeology.

Do not claim:

"this build worked"

solely because Markdown declares a behavior.

Use evidence language such as:

declared
mechanically scaffolded
persistent across builds
owner observed
replay observed
unproven

If a current-model replay is performed, state:

"This is current-model behavior under historical instructions; it is not original historical runtime proof."

Do not use replay results to override archive evidence or Dad's direct historical observation.

---

# 25. Current CTS comparison

At the end of each primary behavior track, compare against the current v0.22.0 golden CTS.

Ask:

- survived?
- disappeared?
- weakened?
- strengthened?
- changed owner?
- became more deterministic-looking?
- became more model-facing?
- remains underspecified?

The current CTS is authority for present source truth.

The historical archive is evidence for lineage.

Keep those roles separate.

If comparing the historical v0.22 archive identity with the golden CTS, preserve their distinct source roles even if byte identity is independently verified.

Do not collapse them into one source identity.

---

# 26. Success criteria

BC-017 succeeds when we can answer, with evidence:

1. Which historical behaviors are worth preserving?
2. Which are not?
3. Which current behaviors have strong historical lineage?
4. Which historical systems were mostly orchestration containers?
5. Which Exec mechanisms solved real problems?
6. Which later Exec mechanisms appear compensatory?
7. What did Blu-as-classroom actually consist of?
8. Which pieces of School Engine are behaviorally valuable without restoring School Engine?
9. Which primary capabilities deserve later deterministic specification?
10. What is the smallest evidence-backed set of successor design questions?

BC-017 does NOT answer:

"What Python architecture do we implement?"

That comes later.

---

# 27. Explicit non-goals

Do NOT:

- implement Python;
- create runtime packages;
- implement Auth;
- implement OPSEC;
- implement reminders;
- implement Time;
- implement MMU;
- implement Mood;
- implement Teaching;
- port School Engine;
- port Exec;
- restore old modules;
- create a new mega-Exec;
- alter current CTS;
- alter Persona identity;
- change current source authority;
- integrate modern PASS/SkillForge;
- recommend legacy PASS restoration;
- import historical archives;
- publish protected kernel text;
- rewrite BC-015 history;
- claim BC-015 was wrong because archives later became available;
- begin BC-020;
- begin BC-030.

---

# 28. BC-015 preservation

BC-015 honestly recorded that v0.15.2 historical evidence was unavailable during that assignment.

The later availability of Kernel archives does not retroactively invalidate BC-015.

BC-017 may now use the newly available evidence prospectively.

Do not rewrite BC-015 to pretend the evidence was available earlier.

---

# 29. Validation commands

Run existing repository validation plus the new BC-017 validation.

At minimum:

git diff --check

python tools/validate_runtime_contracts.py
python -m unittest discover -s tests/contracts -p "test_*.py"

python tools/validate_viability_audit.py
python -m unittest discover -s tests/viability -p "test_*.py"

python tools/validate_historical_archive_inventory.py
python -m unittest discover -s tests/historical_archives -p "test_*.py"

python tools/validate_historical_behavioral_archaeology.py
python -m unittest discover -s tests/historical_archaeology -p "test_*.py"

Run the repository's canonical MANIFEST verification procedure.

Do not assume literal `sha256sum -c MANIFEST.sha256` is authoritative on a Windows checkout where CRLF materialization can differ from the canonical LF/git-blob convention.

Verify golden CTS checksums using the established repository procedure.

Verify that:

kernel/golden/v0.22.0/**
contracts/runtime/**
docs/architecture/**
config/**

remain unchanged unless a path is explicitly part of BC-017's documentation surface.

BC-017 should not modify those protected paths.

---

# 30. Work commit

Create one substantive work commit containing:

- BC-017 assignment records;
- owner-observation record;
- NB-1/NB-4 prerequisite corrections;
- boundary specimen map;
- behavioral archaeology evidence;
- recovery matrix;
- transition map;
- validator/tests;
- worklog/next-step updates appropriate to review state;
- manifest updates required for substantive files.

Suggested commit:

docs(BC-017): add historical behavioral archaeology

Capture the exact SHA.

Do not attempt to write that commit's own SHA inside itself.

---

# 31. Metadata-only commit

After the substantive work commit succeeds and validation passes:

create exactly one metadata-only commit recording the work SHA.

Follow the established repository assignment convention.

Expected metadata-only surfaces should be limited to repository-standard assignment metadata, such as:

docs/domains/runtime/assignments/BC-017/handoff.md
docs/worklogs/assignments.md
MANIFEST.sha256

Use the smallest exact set required by repository convention.

Do not change substantive archaeology findings in the metadata commit.

Suggested commit:

docs(BC-017): record archaeology work commit

Record:

- exact assignment base;
- exact work commit SHA;
- branch name;
- validation results;
- review target;
- status: review.

Do not require the metadata commit to contain its own SHA.

---

# 32. Review preparation

After pushing the Codex branch:

BC-017 status should be:

review

NOT done.

Claude will later receive a separate read-only semantic review assignment.

Claude's future review branch should start from the metadata commit.

Claude should modify only:

docs/domains/runtime/assignments/BC-017/review.md

Do not self-approve BC-017.

Do not merge to main.

Dad merges approved work.
Blu gives closure authorization.

---

# 33. Push

Push normally:

git push -u origin bc-017-historical-behavioral-archaeology

No force push.

---

# 34. Final Codex report

Return:

1. exact base SHA;
2. branch name;
3. BC-016 NB-1 correction performed;
4. BC-016 NB-4 correction performed;
5. re-derived historical version-family set;
6. first/last specimen selection table;
7. any chronology ambiguities;
8. drill-down specimens selected and why;
9. primary behavioral findings;
10. v0.7.4 findings;
11. Exec emergence/stability findings;
12. Teaching/School Engine findings;
13. Reminders findings;
14. Time findings;
15. Mood findings;
16. MMU findings;
17. Auth findings;
18. OPSEC findings;
19. Faithfulness sidecar disposition;
20. behavior-recovery disposition counts;
21. evidence gaps;
22. unsupported-format archives encountered;
23. validator results;
24. test results;
25. manifest verification result;
26. golden checksum verification result;
27. substantive work commit SHA;
28. metadata commit SHA;
29. exact files changed in each commit;
30. confirmation no archives were committed;
31. confirmation no protected kernel text was published;
32. confirmation current CTS was unchanged;
33. confirmation no Python runtime was implemented;
34. confirmation modern PASS/SkillForge was untouched;
35. confirmation BC-020 and BC-030 were not started;
36. confirmation branch was pushed;
37. confirmation working tree is clean.

Stop after reporting.

Do not start Claude review yourself.
Do not start successor design.
Do not begin BC-018/020/030 unless Dad and Blu explicitly authorize it.
