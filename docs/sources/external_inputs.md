# External Input Registry

status: active
owner: docs/domains/repository
last_reviewed: 2026-08-06

Large source archives remain outside this repository bootstrap. Their identity
and authority are recorded in `config/source_authority.json`.

## Current inputs

- `Blu_KB_Preview(1).zip` — current repository snapshot/reference.
- `agent-kit.zip` — scaffold used to create this repository.
- Alice formal specification — profile-controller reference.
- Local Mirror ZIP — experimental continuity-store reference.
- SkillForge ZIP — external PASS compatibility reference; not current kernel.

- `2026-05-02_1333_Blu_v0.15.2_Baseline.zip` — expected BC-015
  `historical_behavioral_reference`; non-authoritative for the current
  runtime. The archive was unavailable in the BC-015 execution environment, so
  its SHA-256 and member evidence remain unavailable and no contents were
  reconstructed.

Do not vendor large snapshots into Blu Core unless a bounded assignment requires
it. Prefer the authoritative live repository and record the exact source
identity used by the assignment.

## 2026-08-06 — BC-016 historical archive source availability

A broader historical kernel archive source became available after BC-015. Its
path-sanitized canonical inventory, stable snapshot receipt, reconciliation,
and representative milestones are stored under
`docs/sources/historical_archives/`.

The source remains `historical_behavioral_reference` and
`non_authoritative_for_current_runtime`. Its later availability does not
retroactively invalidate or rewrite BC-015's honest handling of the v0.15.2
archive as unavailable evidence during that earlier assignment.
