# Blu Core Assignment Log

status: active
owner: docs/worklogs
last_reviewed: 2026-08-05

## Rules

1. Read `AGENTS.md` before claiming work.
2. One owner per assignment and collision domain.
3. Every implementation packet names its base branch or commit.
4. One assignment per checkout; parallel work uses branches and worktrees.
5. The implementing agent runs checks and commits verified work.
6. Completion moves to `review`; Dad or Blu authorizes integration.
7. Golden kernel files are never an implementation collision domain.

## Implementation assignments

| ID | Assignment | Owner | Status | Packet | Base | Collision domain / notes |
|---|---|---|---|---|---|---|
| BC-010 | Extract machine-readable runtime contracts from CTS |  | spec-needed |  | main | runtime contracts only; no behavior rewrite |
| BC-020 | Define Chat and Codex capability adapter contracts |  | spec-needed |  | main | adapters |
| BC-030 | Define Local Mirror continuity schema and lifecycle |  | spec-needed |  | main | continuity; no persistence claim |

## Design assignments

| ID | Assignment | Owner | Status | Notes |
|---|---|---|---|---|
| BC-001 | Establish bootstrap authority and golden source | Blu | done | Prepared and locally verified; recheck after remote setup |

## Completed

- BC-001 — Blu Core bootstrap authority and CTS golden source prepared and verified.
- Initial agent-kit scaffold installed on `main`.

## Standing guardrails

- Bootstrap checks: `git diff --check` and
  `sha256sum -c kernel/golden/v0.22.0/SHA256SUMS`.
- Do not touch `kernel/golden/`.
- No Python runtime exists yet.
- Do not restore legacy `library/` SkillForge routing.
