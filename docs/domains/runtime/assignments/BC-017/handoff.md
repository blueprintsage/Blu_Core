# BC-017 Implementation Handoff

status: done
owner: Codex
last_reviewed: 2026-08-08
assignment: BC-017

## Result

BC-017 completed bounded historical behavioral archaeology from the approved
base. It re-derived version families, selected boundary and change-point
specimens, separated source classes, recorded Dad's observations, analyzed
behavioral lineages, and assigned bounded recovery dispositions.

The work corrects BC-016 NB-1 and NB-4, imports no archive payload or protected
historical text, and leaves the golden CTS unchanged. It does not implement a
runtime, restore a historical module, or decide successor architecture.

## What changed

- Added the BC-017 assignment quartet and owner-observation record.
- Added a structured boundary map and evidence register.
- Added the recovery matrix, behavioral report, and transition map.
- Added a small evidence-integrity validator with focused negative tests.
- Corrected the invalid BLU-HIST-0247 reference.
- Reclassified BLU-HIST-0211 as “MMU representative; Read Lane secondary” at
  medium confidence.
- Updated the runtime continuity records and repository manifest.

## What worked

Boundary-first sampling exposed the main control transitions without treating
all archives equally. Change-point drilldowns established Exec and School
emergence, MMU introduction, reminder/time evolution, mega-Exec growth and
contraction, and late service decomposition. Direct source support remains
traceable through sanitized evidence IDs.

## Limitations and risks

- Historical Markdown establishes declarations and scaffolding, not reliable
  execution.
- Seven Deflate64 archives contain 63 unreadable members.
- v0.4 last-boundary chronology and the v0.8 opening remain ambiguous.
- Durable persistence, autonomous wake, current Auth/OPSEC service
  implementations, and the Kiddo incident mechanism remain unproven.
- Faithfulness is an unshipped draft and only successor-design evidence.

## Next safe step

Claude performs the separately authorized read-only semantic review by changing
only `review.md`, starting from the BC-017 metadata commit. Dad and Blu decide
integration. Do not begin successor design, BC-018, BC-020, or BC-030.

## Commit identity

- Exact base: `4abae4865067d8a6ae0651017d4a564c09dde47b`
- Branch: `bc-017-historical-behavioral-archaeology`
- Substantive work commit: `dcad56f7d50252ab70e993aef7a763ed2bd3617b`
- Metadata commit: reported externally because a commit cannot contain its own
  final SHA.

## Closure receipt

- Closure authority: Dad, Project Owner, and Blu, Project Lead.
- Original Claude review: `c323cff06c9f111408f4a416817d78fc0f3e2d2b`;
  disposition `return-for-correction` with B-01, B-02, and B-03.
- Correction assignment: BC-017-C1; substantive correction
  `87c4e49333d30a471a00483fc1384e1918626ee1`; metadata
  `fd7f1707e242aa0e9621ab9f7293364860cab21d`.
- Final Claude re-review:
  `bea9463f0dbbae1c3944c5f44a7843c757d7f0bb`; disposition
  `approve-with-notes`; zero blocking findings.
- Main integration merge and closure base:
  `b88902d997685057ee0e76709df7117f8a83f295`.
- Final status: `done`.
- Substantive closure commit: recorded by the metadata-only closure commit.
- The closure preserves all non-blocking notes, changes no archaeology
  finding, and authorizes no successor design or runtime implementation.
