# Skill Card - Authoring a Handoff Packet

status: active
owner: docs/assistants/skills
last_reviewed: 2026-08-05

## Use when

Turning an approved decision into work another assistant will execute.

## Procedure

```text
[ ] Copy docs/assistants/handoffs/TEMPLATE_handoff.md
[ ] Name the BASE BRANCH explicitly
[ ] List prerequisites as VERIFIABLE facts (a file, a symbol, a commit)
[ ] Give it a STOP condition: what makes the assistant halt and report
[ ] Write the "Explicitly NOT in this slice" list before the deliverables
[ ] Name the danger-zone files
[ ] Give an exit gate a machine can check
[ ] Add the row to docs/worklogs/assignments.md with a collision domain
```

## Rules

- One slice = one reviewable, revertable diff.
- Prescribe the approach only where a wrong approach is expensive, and say why.
- Prefer an automated acceptance gate over "looks right."
- If the packet cannot state how success is verified, it is not ready to hand off.
