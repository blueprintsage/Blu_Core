# Drill - Domain Continuity

status: active
owner: docs/assistants/drills
last_reviewed: 2026-08-05

## Use when

Starting or ending work on any domain.

## Start checklist

```text
[ ] Read AGENTS.md
[ ] Read docs/worklogs/assignments.md and claim the assignment
[ ] Read docs/domains/<domain>/index.md
[ ] Read worklog.md
[ ] Read decisions.md
[ ] Read failures.md   <- so a known dead end is not retried
[ ] Read next_steps.md
[ ] Confirm the current stable checkpoint and the base branch
```

## End checklist

```text
[ ] Update worklog.md (what changed / tested / worked / failed / risks / next / files)
[ ] Update decisions.md if a decision was made or reversed
[ ] Update failures.md if anything was tried and abandoned
[ ] Update next_steps.md
[ ] Set the assignment to review in assignments.md, noting what was tested
[ ] State the build command and its exit code
```
