# Skill Card - Worklog Update

status: active
owner: docs/assistants/skills
last_reviewed: 2026-08-05

## Use when

Any meaningful code, doc, or design change is made.

## Procedure

Append to the relevant worklog:

```text
Date
Area
What changed
What was tested or reviewed
What worked
What failed
Known risks
Next safe step
Files changed
```

## Rules

- Failed attempts must be recorded. Do not log only successful work - an
  unrecorded failure gets retried by the next assistant.
- Domain work goes in that domain's worklog. Cross-cutting work goes in
  `docs/worklogs/active/`.
- Record "do not reapply" lessons explicitly.
