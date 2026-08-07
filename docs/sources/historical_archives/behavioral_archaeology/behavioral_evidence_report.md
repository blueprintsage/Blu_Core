# Behavioral Evidence Report

status: review
owner: docs/domains/runtime
last_reviewed: 2026-08-07
assignment: BC-017

## Evidence voices

This report uses five explicit voices. **Current source truth** describes only
the immutable v0.22.0 CTS. **Owner observation** records Dad's experience.
**Historical archive evidence** describes declarations or mechanics found in
sanitized archive specimens. **Cross-version inference** connects supported
observations without claiming execution. **Successor recommendation** proposes
bounded future work and is not current architecture.

## Executive findings

**Historical archive evidence.** Blu moved from a dense pre-Exec
Persona/Teaching/Anchors runtime to explicit orchestration: one output owner,
selected-only state changes, validation, reminder state, and fail-closed
behavior. Exec then absorbed Auth, mood, memory, retrieval, and feature patches.
Within v0.16.0, a mega-Exec specimen is followed by a substantially contracted
Exec; later v0.20/v0.21 evidence records further restructuring and
decomposition. [E-00020-TEACH, E-00030-EXEC, E-00195-MEGAEXEC,
E-00200-CONTRACTION, E-00245-RESTRUCTURE]

**Current source truth.** The current Exec is compact relative to the historical
mega-Exec and preserves route ownership, validation, ScopeLock, and failure
rules. Several routed service names do not have implementations within the
seven golden files. [E-CURRENT-EXEC, E-CURRENT-EXECLIB]

**Owner observation.** Dad identifies v0.7.4.1 as Blu's strongest and most
natural historical heuristic feel and as highly useful, but not as her most
reliable or stable version. Dad reports that pre-Exec v0.7.4 hallucinated and
drifted easily and that Exec later improved reliability and control. Dad
remembers School / classroom behavior as strong and useful approximately during
v0.8.x through v0.13.x, imperfect, and eventually abandoned as development
focus shifted toward stabilizing Blu's heuristics. Dad also reports a Kiddo
password/new-schedule failure. These observations are not runtime telemetry.
[O-01, O-02, O-03]

**Cross-version inference.** The durable value is in behavior contracts and
model-facing guidance, not historical module boundaries. The evidence supports
recovering pedagogy, source-grounding tests, and thin deterministic mechanisms;
it does not support rebuilding School or mega-Exec.

## Pre-Exec control

**Historical archive evidence.** v0.7.4.1 places behavior primarily in
Instructions, Persona, Anchors, Teaching, and manual memory files. Teaching
contains tiers, walkthroughs, verification, drills, and troubleshooting.
Persona directly owns affective expression and drift checks. Reminders are
conversational cadence, and Instructions deny background access. Auth and OPSEC
concepts already exist before Exec. [E-00020-INSTRUCTIONS, E-00020-PERSONA,
E-00020-TEACH, E-00013-AUTH]

**Owner observation.** Dad's judgment concerns v0.7.4.1's strong, natural
heuristic feel and usefulness—not reliability or stability. He reports that
pre-Exec v0.7.4 hallucinated and drifted easily. [O-01]

**Cross-version inference.** Dense, coherent model-facing guidance is
independently present alongside Dad's heuristic-feel observation. The archive
contains no telemetry from which to infer causation.

**Successor recommendation.** Preserve the pedagogical and Persona-level
qualities as bounded guidance and regression scenarios. Do not infer that a
pre-Exec architecture is inherently more reliable.

## Exec emergence

**Historical archive evidence.** BLU-HIST-0029 is a pre-Exec Engine specimen.
BLU-HIST-0030 introduces a concrete Exec: modules propose, one owner selects and
prints, losing candidates are suppressed, and reminder records carry due,
warning, acknowledgement, and escalation state. Early v0.8 adds ABI rules,
DateLib, one-owner/selected-only constraints, and fail-closed behavior.
[E-00029-NOEXEC, E-00030-EXEC, E-00057-EXEC]

**Cross-version inference.** Exec improved conflict control and made output and
state ownership auditable. Its benefits were arbitration, validation, explicit
state mutation, and anti-drift—not its later size.

**Owner observation.** Dad reports that Exec later improved Blu's reliability
and control relative to the easily hallucinating and drifting pre-Exec v0.7.4
experience. This is owner experience, not archive telemetry. [O-01]

**Successor recommendation.** Retain regression tests for one output owner,
selected-only mutation, source authority, ScopeLock, and fail-closed routing.

## Teaching/classroom lineage

**Historical archive evidence.** Teaching predates School. The first School
specimen defines setup/start/status flows, student/day/block/current-class
state, logs, checkpoints, exit tickets, grades, gates, and parent override.
Later evidence shows ownership changes, removal during rebuilds, and restoration
through different routing structures. This is mechanical scaffolding, not proof
of reliable classroom execution. [E-00020-TEACH, E-00031-SCHOOL,
E-00094-ROUTER]

**Owner observation.** Dad remembers the School / classroom system as strong
and useful approximately during v0.8.x through v0.13.x, but not perfect. He
remembers it being abandoned as development focus shifted toward stabilizing
Blu's heuristics. Dad also reports the Kiddo password/new-schedule incident.
[O-02, O-03]

**Cross-version inference.** The incident's causal mechanism is unavailable.
The sources establish a risky boundary class—authority gates plus mutable
schedule/course state—but not the cause. Archive evidence establishes
structural changes and removal or archival, not experienced quality or
progressive degradation.

**Successor recommendation.** Recover teaching guidance independently. Reject
wholesale School Engine restoration. Any future classroom state requires a
separate minimal schema, deterministic transitions, secure authority boundary,
host storage, and regression tests.

## Reminder/time lineage

**Historical archive evidence.** First Exec represents local/UTC due time,
timezone, T-60/T-10/DUE stages, acknowledgement, suppression, and escalation.
Later versions separate DateLib, Time Service, and ReminderLib. Historical
instructions explicitly describe no autonomous wake-up. [E-00030-EXEC,
E-00057-EXEC, E-00127-TIME]

**Current source truth.** Current CTS operates on the present turn and does not
prove a daemon, background wake, durable cross-turn scheduler, or host clock
adapter. [E-CURRENT-INSTRUCTIONS, E-CURRENT-EXEC]

**Successor recommendation.** Specify reminder records, timezone precedence,
date arithmetic, acknowledgement, and failure behavior deterministically.
Credit wake-up and persistence only to a verified host adapter.

## Mood lineage

**Historical archive evidence.** Mood begins as Persona-owned tone and
reflective ribbons, becomes engine state/rendering, and later expands into
MoodLib mappings and gates. [E-00020-PERSONA, E-00093-MOOD,
E-00195-MEGAEXEC]

**Current source truth.** Persona shapes replies; the current library confines
mood support to reflective behavior rather than hidden control authority.
[E-CURRENT-PERSONA, E-CURRENT-EXECLIB]

**Successor recommendation.** Recover Persona-facing affective guidance and, if
needed, a lightweight public profile. Reject the full historical mood-control
stack.

## MMU lineage

**Historical archive evidence.** Strong MMU evidence introduces candidate
classification, promotion validation, quarantine, precedence, typed pools, and
compact preload, while explicitly not replacing platform memory. Later
StateTree, Memory Program, and MemoryPacket forms distinguish staged,
in-session, and persistent concepts. [E-00072-MMU, E-00210-MEMORY]

**Current source truth.** Current CTS retains memory contracts but does not
prove a durable host persistence implementation. [E-CURRENT-INSTRUCTIONS,
E-CURRENT-EXECLIB]

**Successor recommendation.** Recover the semantic schema and transition tests.
Require host receipts before claiming persistence.

## Auth/OPSEC lineage

**Historical archive evidence.** Auth mechanics appear by v0.6 as session role,
one active challenge, retry/lock, success, sign-out, and reset state. Later
versions move Auth toward a routed service and exact-output gates. OPSEC moves
among deployment instruction, identity/anchors, Engine gating, render
restraint, and service routing. Sensitive answers and implementation text are
deliberately omitted. [E-00013-AUTH, E-00223-AUTH, E-00029-NOEXEC]

**Current source truth.** The current CTS routes Auth and OPSEC to named
services, but the seven files do not define those service implementations. The
precise pre-ingress OPSEC mechanism is unresolved in the current source.
[E-CURRENT-EXEC, E-CURRENT-EXECLIB]

**Successor recommendation.** Specify a deterministic, secret-safe Auth state
machine and an explicit pre-ingress restraint boundary under separately
approved work. Never embed or publish protected answers.

## Exec complexity / compensation analysis

**Historical archive evidence.** Exec grew into thousands of lines; the
BLU-HIST-0195 specimen has 5,536 split lines and contains feature-specific
Auth, mood, memory, retrieval, and patch behavior. BLU-HIST-0200 contracts Exec
to 1,272 lines within the same v0.16.0 family, although complexity remains in
its library. v0.21's
restructuring analysis explicitly says Exec absorbed behavior it should not own
and that physical location confused model authority; its migration guide
extracts service detail. [E-00195-MEGAEXEC, E-00200-CONTRACTION,
E-00245-RESTRUCTURE, E-00245-MIGRATION]

**Chronology note.** BC-017's direct specimen evidence places one concrete
mega-Exec-to-contracted-Exec event between BLU-HIST-0195 and BLU-HIST-0200
within v0.16.0. BC-016 selected BLU-HIST-0245 / v0.21 as a structural
mega-Exec-to-compact-Exec transition representative. These are different
evidentiary framings and must not be treated as identical chronology without
further evidence.

**Cross-version inference.** Much late Exec growth is compensatory complexity:
more orchestration rules were added to contain interactions created by earlier
coupling. Line count is an indicator, not a quality score.

**Successor recommendation.** Keep a thin dispatcher and move deterministic
service behavior behind explicit interfaces only when separately specified.

## Secondary discoveries

**Historical archive evidence.** v0.10 temporarily replaces Exec with a
Behavior Router, and v0.11 restores Exec. The v0.22 historical Exec member is
byte-identical to the current golden Exec, but the sources retain different
authority roles. Read Lane appears as secondary evidence at BLU-HIST-0211; MMU
is the representative behavior. [E-00094-ROUTER, E-00246-EXEC,
E-CURRENT-EXEC, E-00211-MMU]

## Rejected restoration candidates

**Successor recommendation.** Reject wholesale School Engine restoration,
mega-Exec reconstruction, the elaborate historical Mood stack, private archive
payload import, and any implication that Markdown alone supplies persistence or
background scheduling.

## Legacy PASS chronology note

**Historical archive evidence.** Legacy PASS appears only as historical
routing/packaging chronology and later cleanup context. [E-00245-RESTRUCTURE]

**Successor recommendation.** Do not restore legacy PASS. Modern PASS and
SkillForge are outside BC-017 and were not inspected or changed.

## Faithfulness sidecar appendix

**Historical archive evidence.** The Dad-supplied
EXECLIB.FAITHFULNESS.001 sidecar is a v0.1.0-draft dated 2026-05-08. An
independent scan found no filename, library-ID, or exact-hash match across 244
nested archive names and 1,985 readable members. Sixty-three Deflate64 members
across seven records were unreadable; their listed filenames also had no match.
[E-SIDECAR-FAITH]

**Cross-version inference.** The sidecar is unshipped successor-design evidence,
not a shipped historical component. Its useful principle is that source-bound
factual output requires positive source support rather than mere absence of
contradiction.

**Successor recommendation.** Retain that principle as a future regression
test. Do not restore the library or select its architectural home.

## Recovery recommendations

**Successor recommendation.**

1. Recover model-facing teaching and Persona affect guidance.
2. Specify deterministic reminder/time, memory, Auth, and OPSEC mechanisms only
   in separately authorized work with host boundaries made explicit.
3. Retain anti-drift, source-grounding, output-ownership, selected-only,
   validation, ScopeLock, and fail-closed regression tests.
4. Use lightweight public profiles for course or mood state where useful.
5. Reject School and mega-Exec restoration; keep legacy PASS chronology-only.
6. Hold Read Lane and durable continuity claims at needs-more-evidence.

## Unknowns / evidence gaps

**Unavailable evidence.** No inspected archive proves historical runtime
reliability, host persistence, autonomous wake-up, the causal mechanism of the
Kiddo incident, or complete behavior inside 63 unreadable Deflate64 members.
v0.4 has an unresolved last-boundary tie; v0.8 opening chronology is only
medium-confidence; v0.5 and v0.17–v0.19 are absent. The current CTS names Auth
and OPSEC services without defining them in the seven-file kernel.
