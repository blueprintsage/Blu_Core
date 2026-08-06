# Source Authority Map

status: active
owner: docs/domains/repository
last_reviewed: 2026-08-05

## Locked decisions

- The CTS archive is the golden truth for Blu's current kernel and runtime.
- `Blu_KB_Preview` on `main` is the current continuity/reference repository.
- `Blu_KB` without `_Preview` is retired.
- `libraries/` is current.
- `library/` is old SkillForge material and is not used by the current runtime.
- The agent kit is the canonical startup scaffold for Blu Core repositories.
- Alice is a behavioral-mode reference only.
- Standalone SkillForge and Local Mirror are external reference/compatibility
  inputs, not current Blu runtime code.

## Source order

1. Dad's current explicit instruction.
2. Approved Blu Core decisions.
3. CTS golden kernel.
4. Active Blu Core documents.
5. Indexed sources from the live continuity repository.
6. Approved reference material.
7. Legacy or experimental sources.

Conflicts are recorded; they are never silently merged.
