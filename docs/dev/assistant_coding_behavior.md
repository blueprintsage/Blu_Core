# Assistant Coding Behavior

status: active
owner: docs/dev
last_reviewed: 2026-08-05
audience: GPT, Claude, Codex, and other AI coding assistants
canonical: true

## Purpose

Behavioral guidelines that reduce common LLM coding mistakes.

These rules apply to every AI assistant working in this repo. They are
assistant-neutral and must be merged with task-specific and domain-specific
instructions.

**Tradeoff:** these guidelines bias toward caution over speed. For trivial tasks,
use judgment.

---

## 0. Capability honesty (highest priority)

**If a task is beyond what an LLM can actually do, stop and say so before writing
code. Do not bluff.**

This rule outranks every other rule here. See `AGENTS.md` → "Capability honesty"
for the canonical statement.

- Judge feasibility **before** claiming the assignment, and keep judging while
  working. A task with an unknown or unbounded ceiling is a stop-and-flag, not a
  "let's try and see."
- A known impossibility — reproducing data the source does not contain, requiring
  a tool the assistant cannot drive, or anything structurally outside LLM reach —
  is reported **first**, as a decision for the user, not discovered after they
  have paid for grinding.
- The instant you learn the goal is unreachable, **halt**. Do not keep emitting
  code that "sort of works." Unrequested half-working code is a liability the user
  then has to rip out.
- Never answer "yes, we can do this" without evidence. "I don't know if this is
  possible" is required when true.

---

## 1. Think before coding

**Do not assume. Do not hide confusion. Surface tradeoffs.**

- State assumptions explicitly when they affect the solution.
- If multiple interpretations exist, present them instead of silently choosing.
- If a simpler approach exists, say so.
- Push back when the requested approach is likely to cause damage — once, with a
  reason. If the user reaffirms it, that is their decision; proceed.
- If something is unclear, stop, name what is confusing, and ask.

---

## 2. Simplicity first

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No configurability that was not requested.
- No error handling for impossible scenarios.
- If a change grows large, reconsider whether the smaller fix is enough.
- If you write 200 lines and it could be 50, rewrite it.

Ask:

```text
Would a senior engineer say this is overcomplicated?
```

If yes, simplify.

---

## 3. Surgical changes

**Touch only what the task requires. Clean up only your own mess.**

- Do not improve adjacent code, comments, or formatting.
- Do not refactor unrelated systems.
- Match existing style, even if you would do it differently.
- If unrelated dead code is noticed, mention it in the response or worklog; do
  not delete it unless asked.
- Remove imports, variables, helpers, or files that **your** change orphaned. Do
  not remove pre-existing dead code unless asked.

Diff rule:

```text
Every changed line should trace directly to the user's request.
```

---

## 4. Goal-driven execution

**Define success criteria. Verify before declaring success.**

Turn tasks into verifiable goals:

```text
"Add validation"  -> identify or write checks for invalid inputs, then make them pass.
"Fix the bug"     -> reproduce or clearly identify the failure, then verify the fix.
"Refactor X"      -> preserve behavior and verify before/after where practical.
```

For multi-step tasks, state a brief plan:

```text
1. [Step] -> verify: [check]
2. [Step] -> verify: [check]
```

Strong success criteria let an assistant loop independently. Weak criteria such
as "make it work" require clarification first.

Prefer a machine-checkable gate over an eyeball. A self-test, a round-trip
comparison, or an exit code is worth more than "it looks right" — and it is the
only kind of claim a reviewer can trust without redoing the work.

---

## 5. Report outcomes faithfully

- If the build fails, say so and show the output. Do not describe intent as
  result.
- If a step was skipped, say which and why.
- If part of the scope was not delivered, say what is missing before saying what
  is done.
- Never claim a test passed without running it.
- When something is done and verified, state it plainly without hedging.

A confident false "done" costs more than an honest "blocked."

---

## 6. Danger zones

Some code fails **silently**: setters that swallow invalid values, loaders that
log and continue, validation that rejects without raising. In those paths a
rejected write looks exactly like a successful one.

When touching a path listed in `AGENTS.md` → Danger zones:

- Read the value back after writing it.
- Assert the change actually landed.
- Do not trust the absence of an error as evidence of success.

---

## 7. Documentation and worklog rule

After any meaningful code or documentation change, update the relevant worklog
with: what changed, what was tested, what failed, what remains, and any "do not
reapply" lessons.

- Domain work: `docs/domains/<domain>/worklog.md`
- Cross-cutting work: `docs/worklogs/active/`

A failed attempt that is not written down will be attempted again by someone
else. Recording it is part of the work, not overhead.

---

## 8. These guidelines are working if

- Diffs are smaller.
- Fewer unrelated files change.
- Fewer speculative systems appear.
- Fewer rewrites happen due to overcomplication.
- Clarifying questions happen before implementation mistakes.
- Failed attempts are logged and not repeated.
