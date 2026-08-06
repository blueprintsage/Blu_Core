# External Input Registry

status: active
owner: docs/domains/repository
last_reviewed: 2026-08-05

Large source archives remain outside this repository bootstrap. Their identity
and authority are recorded in `config/source_authority.json`.

## Current inputs

- `Blu_KB_Preview(1).zip` — current repository snapshot/reference.
- `agent-kit.zip` — scaffold used to create this repository.
- Alice formal specification — profile-controller reference.
- Local Mirror ZIP — experimental continuity-store reference.
- SkillForge ZIP — external PASS compatibility reference; not current kernel.

Do not vendor large snapshots into Blu Core unless a bounded assignment requires
it. Prefer the authoritative live repository and record the exact source
identity used by the assignment.
