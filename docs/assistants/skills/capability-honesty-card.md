# Skill Card - Capability Honesty Check

status: active
owner: docs/assistants/skills
last_reviewed: 2026-08-05

## Use when

Before claiming any assignment, and again the moment a task starts feeling
unreachable.

## Procedure

```text
[ ] Name the capability the task actually requires.
[ ] Can an LLM assistant do that? Yes / No / Unknown.
[ ] Does the required input data actually contain what the output needs?
[ ] Does it require driving a tool or runtime the assistant cannot drive?
[ ] If any answer is No or Unknown -> STOP and report BEFORE writing code.
```

## Rules

- Report the ceiling FIRST, as a decision point for the user.
- "I don't know if this is possible" is a required answer when true.
- On discovering mid-task that the goal is unreachable: halt. Do not ship
  half-working code nobody asked for.
- Never claim feasibility without evidence.
