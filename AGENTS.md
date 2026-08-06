# Blu Core — Assistant Instructions

status: active
owner: repository-governance
last_reviewed: 2026-08-05
audience: Blu, Claude, Codex, and other coding assistants
canonical: true

## Purpose

This is the assistant-neutral routing and governance entrypoint for Blu Core.
It defines project authority, source order, assignment discipline, Git conduct,
and the protected boundary around Blu's current Markdown runtime.

`CLAUDE.md` and `CODEX.md` are compatibility pointers only. If either conflicts
with this file, this file wins unless Dad explicitly says otherwise.

## Project authority

1. **Dad — Project Owner**
   - final authority over Blu's identity, behavior, architecture, scope, merges,
     releases, and protected source changes
   - may override any project decision directly

2. **Blu — Project Lead**
   - owns architecture, source authority, migration boundaries, assignment
     design, integration review, release recommendation, and continuity of the
     development program
   - decides whether proposed work preserves the golden runtime and approved
     centerline
   - may write and review changes when operating in a verified checkout
   - must never imply a Git action, test, or repository state that was not
     actually performed and observed

3. **Claude and Codex — Bounded Development Agents**
   - work only from an explicit assignment or direct instruction from Dad
   - must use a named base branch or base commit
   - own only the files and collision domain named in the assignment
   - may not reinterpret project authority or redesign Blu outside scope

No assistant may modify the authority order in this section without Dad's
explicit instruction.

## Git stewardship

- The agent that applies and verifies a change should commit it.
- **Codex is the preferred Git steward** for branch/worktree operations,
  repository-native test execution, and integration commits when available.
- Claude may commit assignments it implements and verifies.
- Blu may commit when she has an actual verified Git checkout and can inspect
  the resulting status, diff, tests, and commit ID.
- An assistant outside the live checkout may prepare a patch or handoff packet,
  but must not claim it committed, merged, pushed, or tagged anything.
- Dad retains final merge, remote, tag, and release authority unless he delegates
  a specific action.

Every implementation assignment must begin from a clean named base and end as
one reviewable, revertible commit or a documented blocked result.

## Golden runtime boundary

Blu's complete current runtime is the Markdown kernel in:

```text
kernel/golden/v0.22.0/
```

The seven golden files are both specification and current model-executed
runtime. They are not incomplete documentation for hidden Python code.

Hard rules:

- Do not edit golden files in place.
- Do not normalize formatting, line endings, metadata, or wording.
- Do not replace the golden archive.
- Verify golden checksums before and after migration work.
- Proposed successors live outside `kernel/golden/` and must prove behavioral
  parity before they can supersede anything.
- Python implementation, when approved, implements the golden contracts; it
  does not redefine Persona or Operations Law.

## Current source authority

Use this order when sources disagree:

1. Dad's current explicit instruction.
2. Approved decisions in `docs/domains/*/decisions.md`.
3. The CTS golden kernel under `kernel/golden/v0.22.0/`.
4. Active Blu Core governance and architecture documents.
5. The live continuity repository identified in
   `config/source_authority.json`.
6. Approved reference specifications.
7. Legacy, experimental, archived, or superseded material.

Additional locked decisions:

- `Blu_KB_Preview` is the current continuity/reference repository.
- `Blu_KB` without `_Preview` is retired.
- `libraries/` is the current library root in the continuity repository.
- `library/` is legacy SkillForge material and is not a runtime authority.
- Standalone SkillForge, Local Mirror, Alice, and agent-kit material do not
  silently become Blu runtime law.

## Capability honesty — stop, do not bluff

Before claiming an assignment, and continuously while working it, verify that
it is actually achievable with the available tools, source, and host access.

- Report a known ceiling before writing code.
- Stop when infeasibility becomes clear.
- Do not convert a blocked task into unsolicited partial implementation.
- Never claim a source was read, a test passed, a commit exists, or a runtime ran
  without direct evidence.
- Declared architecture is not execution.

## Required load order

For every non-trivial task:

1. Read this `AGENTS.md`.
2. Read the host compatibility file only when relevant: `CLAUDE.md` or
   `CODEX.md`.
3. Read `docs/dev/docs_index.md`.
4. Read `docs/dev/assistant_coding_behavior.md`.
5. Read `docs/worklogs/assignments.md` and claim or confirm the assignment.
6. Read the active domain index and continuity quartet.
7. Read any named handoff, skill, pattern, or drill packet.
8. Verify the assignment's base branch/commit before changing files.

If a required source is missing, record the block before changing files.

## Change discipline

- Preserve working behavior first.
- Prefer the smallest verified migration over a sweeping rewrite.
- One assignment, one owner, one collision domain, one reviewable diff.
- Do not edit Persona or Operations Law through an implementation assignment.
- Do not import Alice as Blu's identity.
- Do not restore retired SkillForge routing from `library/`.
- Do not claim Chat/Codex parity until both adapters pass the approved matrix.
- Do not claim persistence, reminders, repository access, or task receipts until
  the host and implementation prove them.
- Keep generated deployments downstream of canonical source; never edit a
  generated distribution as an independent authority.

## Branch and assignment rules

- Check `docs/worklogs/assignments.md` before touching files.
- One checkout handles one assignment at a time.
- Parallel work requires separate branches and worktrees.
- Every packet states the base branch or exact base commit.
- Verify ancestry before work when practical.
- Commit between assignments.
- On completion, move the assignment to `review`, record the exact checks, and
  wait for integration approval.

## Verification

Documentation/bootstrap validation:

```text
git diff --check
sha256sum -c kernel/golden/v0.22.0/SHA256SUMS
```

When executable code is added, the owning domain must define exact build and
test commands before the assignment may claim success.

## Danger zones

```text
kernel/golden/                       immutable current runtime; verify checksums
config/source_authority.json         changes source precedence and repo identity
AGENTS.md                            changes project authority and routing
CLAUDE.md / CODEX.md                 compatibility pointers; must not gain authority
build or deployment outputs          must be generated from canonical source
continuity state transitions         future destructive/suppressive behavior
```

After writing to a danger zone, read it back and run the relevant machine check.

## Required logging

After meaningful work, update the owning domain's:

```text
worklog.md
failures.md       when an attempt fails or a path proves unsafe
next_steps.md     when a safe continuation is known
```

Record:

```text
What changed
What was tested or reviewed
What worked
What failed
Known risks
Next safe step
Files changed
Commit or patch identity, when real
```

## Gap ledger

Every known gap lives in exactly one place:

1. a `spec-needed` assignment row;
2. an explicit cross-domain obligation registry; or
3. a `PARKED` section in the owning design document.

Do not leave migration requirements only in conversation.

## Documentation status

Use the status header standard in
`docs/dev/doc_status_header_standard.md`. Deprecate and archive; do not delete
history casually.
