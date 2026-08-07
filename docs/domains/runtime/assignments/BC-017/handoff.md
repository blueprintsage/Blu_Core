# BC-017 Implementation Handoff

status: review
owner: Codex
last_reviewed: 2026-08-07
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
