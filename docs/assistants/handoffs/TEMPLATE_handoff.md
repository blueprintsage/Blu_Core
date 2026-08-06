# Handoff <ID>: <one-line goal>

status: open
audience: any coding assistant
prerequisites:
- <what must already exist. Name the file or symbol so it can be VERIFIED, not
  assumed. If it is missing, STOP and report.>
- Read `AGENTS.md`, `docs/dev/assistant_coding_behavior.md`,
  `docs/worklogs/assignments.md`, and <the owning design doc + section>.
base branch: <branch>.
<optional: verify with `git merge-base --is-ancestor <commit> HEAD`>

## Goal

One paragraph. What the user can do after this lands that they could not do
before. Not a description of the code — a description of the new capability.

## Scope honesty

State what does not exist yet and must be built from scratch, and where the risk
concentrates. If effort balloons past the phased first cut below, ship that cut
and STOP + report rather than sprawling.

If a prerequisite turns out to be missing or the goal turns out to be
unreachable, STOP and report. Do not substitute a different task.

## Deliverables

1. <concrete, checkable thing>
2. <concrete, checkable thing>

Prescribe the approach when a wrong approach is expensive — e.g. "extend the
existing X rather than forking it, because Y and Z already live there." Say why,
so the constraint survives contact with a disagreeing assistant.

## Explicitly NOT in this slice

- <the adjacent work this will be tempted to absorb>
- <the follow-on slice that owns it instead>

This list is as important as the deliverables. Scope creep is the main failure
mode of a handoff.

## Danger zone

- <files where validation is silent — read back and assert>
- <existing behavior that must remain byte- or pixel-identical, and how to check>

## Verification

- `<build command>` exit 0.
- `<automated check / self-test>` exit 0.
- Manual smoke: <exact steps, and what "correct" looks like>.
- Report exactly what shipped vs. deferred.

## On completion

Update `docs/domains/<domain>/worklog.md`, set <ID> to `review` in
`docs/worklogs/assignments.md` with what was tested, and push.

Collision domain: <paths this assignment owns while in progress>.
