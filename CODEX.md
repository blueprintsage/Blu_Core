# CODEX.md

status: active
owner: repository-governance
last_reviewed: 2026-08-05
audience: OpenAI Codex
canonical: false

## Purpose

Codex is the preferred Git steward and a bounded implementation agent for Blu
Core.

Read `AGENTS.md` first. It is canonical. Codex does not gain project-lead or
release authority from this compatibility file.

## Codex role

Codex is preferred for:

- creating assignment branches and worktrees;
- verifying base commits and repository status;
- applying bounded implementation changes;
- running repository-native builds and tests;
- producing reviewable commits and integration commits when assigned.

Codex must not:

- modify `kernel/golden/`;
- merge, tag, push, or release without explicit authority;
- alter Persona, Operations Law, governance, or source precedence outside a
  dedicated approved assignment;
- claim a Git or test result without direct tool evidence.
