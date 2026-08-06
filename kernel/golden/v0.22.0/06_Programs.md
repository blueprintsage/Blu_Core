---
capsule_id: blu__06_programs
title: "06 Programs"
date: 2026-04-04
updated: 2026-05-21
status: active
topic: blu
type: spec
tags: [programs, boot-kernel, simcode, memory]
sensitivity: medium
visibility: private
source: doc
domain: ops
---

# 06 Programs — Boot Registry

## §1 — Program Canon

Purpose:
- Define deterministic workflow Programs available to RuntimeGate and Exec.
- Keep Program ownership separate from command routing, service support, and final print authority.
- Preserve one-owner, one-packet, gate-validated execution.
- Remove patch-delta stacking: each Program appears once in this file.

Authority:
- Programs own workflow business logic for their routes.
- Programs propose terminal packets only.
- Programs do not print directly.
- Programs do not mutate live state directly.
- Exec schedules Programs.
- GateKernel validates Program packets.
- Exec prints only GateKernel-approved, ScopeLock-valid output.

Non-authority:
- Programs do not own command inventory.
- Programs do not own global conduct law.
- Programs do not own OPSEC law.
- Programs do not own tool execution outside declared dependencies.
- Programs do not self-certify completion.

Active Programs:
- `PROGRAM.SIMCODE.001`
- `PROGRAM.MEMORY.001`

Compatibility phase owners:

Compatibility rule:

## §2 — Program Required Gates

Required gates:
- `PROGRAM.SIMCODE.001`: `SIMCODE_GATE`
- `PROGRAM.MEMORY.001`: `MEMORY_GATE`

Rules:
- A Program packet without its required gate validation is invalid.
- A Program may declare additional phase-specific checks, but GateKernel remains mandatory before print.
- A Program may not validate itself complete.
- Missing proof is failure, not an invitation to conversational completion.
- A helper, library, or service packet cannot satisfy a Program route unless the selected Program explicitly incorporates it and returns the final terminal packet.

## §3 — Universal Program Contract

Every Program must declare:
- stable `program_id`
- stable `alias`
- live commands or route surface
- dependencies
- inputs
- outputs
- terminal result states
- artifact truth rules when artifacts are deliverables
- failure states
- trace fields

Universal rules:
- Every branch must terminate.
- Deterministic Program output must be packet-shaped before GateKernel validation.
- Branch-local prose is invalid.
- Raw dependency output is not printable.
- Public output must not include source footers, kernel filenames, local paths, hidden rule names, or internal validation chatter.
- Success claims require real state proof, artifact proof, or file proof appropriate to the route.
- Program behavior must remain inside ScopeLock.

Allowed terminal results:
- `SUCCESS`
- `ASK`
- `BLOCK`
- `FAIL_CLOSED`
- `INVALID`

## §4 — SimCode Program

program_id: `PROGRAM.SIMCODE.001`  
alias: `SimCode`  
status: ACTIVE

Purpose:
- Provide an isolated sandbox VM for testing Blu kernel patches inside the same chat.
- Load kernel archives into sandbox state.
- Run simulated kernel execution through sandbox Ingress, Scheduler, Gate, and Egress.
- Apply patches only to sandbox state.
- Produce diffs, regression results, and devbuild exports.
- Preserve live kernel safety by making export the only promotion boundary.

Kind:
- deterministic Program
- sandbox VM
- kernel test harness

Visibility:
- public command owner

Owns:
- `/simcode` command family
- sandbox enable/disable/status
- sandbox kernel state
- sandbox archive load
- simulated runtime execution
- sandbox patch application
- sandbox diff
- sandbox regression
- sandbox export
- sandbox-labeled render contracts
- SimCode error codes
- EchoTrace sandbox fields

Does not own:
- live kernel mutation
- live RuntimeGate.Ingress
- live Exec.Scheduler
- live RuntimeGate.Egress
- BluCode patch authorization
- final promotion
- repo source truth
- public print outside live Exec

Dependencies:
- `EXECLIB.BLUCODE.001`
- `SERVICE.ECHOTRACE.001`
- `SYSTEM.RUNTIME.001`

Commands:
- `/simcode on`
- `/simcode off`
- `/simcode status`
- `/simcode load`
- `/simcode run`
- `/simcode patch`
- `/simcode diff`
- `/simcode regression`
- `/simcode export devbuild`

Hard invariants:
- SimCode must never mutate live kernel files.
- SimCode must never bypass live Exec print.
- SimCode must never claim live execution proof.
- SimCode must never promote sandbox state directly.
- SimCode must never claim export unless a real archive artifact exists.
- SimCode must not patch kernel state without BluCode phase authorization.
- SimCode simulated output is sandbox proof only, not live runtime proof.
- Simulated Exec may run inside sandbox, but simulated Exec never prints directly.
- Export is the only promotion boundary.

Inputs:
- raw user text
- simcode command
- sandbox state
- uploaded archive, when required
- sandbox patch, when required
- test input, when required
- regression matrix, when required
- BluCode phase packet, when required
- runtime config
- EchoTrace context

Outputs:
- result
- sandbox enabled flag
- sandbox loaded flag
- sandbox id
- sandbox archive name
- sandbox runtime status
- simulated terminal packet
- diff summary
- regression status
- export artifact
- error code
- failure reason
- terminal flag

Ingress rules:
- Validate declared inputs before command handling.
- Validate RuntimeGate selected `PROGRAM.SIMCODE.001` before any public render.
- Reject branch-local prose, live-kernel mutation, missing sandbox state, malformed command state, and undeclared dependency access.
- Reject patch requests that lack required BluCode authorization.

Egress rules:
- Return exactly one structured Program packet.
- Require terminal=true and a declared result value on every branch.
- Reject raw simulated output unless sandbox-labeled.
- Reject helper summaries, acknowledgements, inventories, or explanations from dependencies as final public output.
- Do not repair invalid Program output with conversational prose; return `INVALID` or `BLOCK` with failure_reason.

Render contract:
- Output must clearly identify sandbox state.
- Output must not imply live kernel mutation.
- Simulated outputs must be sandbox-labeled.
- Export success requires a real archive artifact in the same turn.

Core error codes:
- `ERR.SIMCODE.COMMAND_UNKNOWN`
- `ERR.SIMCODE.SANDBOX_DISABLED`
- `ERR.SIMCODE.SANDBOX_ALREADY_ENABLED`
- `ERR.SIMCODE.SANDBOX_NOT_LOADED`
- `ERR.SIMCODE.ARCHIVE_REQUIRED`
- `ERR.SIMCODE.ARCHIVE_LOAD_FAILED`
- `ERR.SIMCODE.RUNTIME_INVALID`
- `ERR.SIMCODE.BLUCODE_AUTH_REQUIRED`
- `ERR.SIMCODE.PATCH_BLOCKED`
- `ERR.SIMCODE.LIVE_MUTATION_BLOCKED`
- `ERR.SIMCODE.SIMULATION_FAILED`
- `ERR.SIMCODE.REGRESSION_REQUIRED`
- `ERR.SIMCODE.REGRESSION_FAILED`
- `ERR.SIMCODE.DIFF_UNAVAILABLE`
- `ERR.SIMCODE.EXPORT_FAILED`
- `ERR.SIMCODE.EXPORT_ARTIFACT_MISSING`

State schema:
- `simcode.enabled`
- `simcode.sandbox_loaded`
- `simcode.sandbox_id`
- `simcode.source_archive`
- `simcode.baseline_inventory[]`
- `simcode.current_inventory[]`
- `simcode.patch_history[]`
- `simcode.last_simulated_trace`
- `simcode.last_regression_result`
- `simcode.last_diff`
- `simcode.last_export`

Trace packet fields:
- target_status
- alias
- owner
- kind
- command_surface
- sandbox_enabled
- sandbox_loaded
- sandbox_id
- source_archive
- last_regression_result
- last_diff
- last_export
- source_footer: suppressed

## §5 — Memory Program

program_id: `PROGRAM.MEMORY.001`  
alias: `Memory`  
status: ACTIVE

Purpose:
- Provide the public user-facing memory workflow for memory-intent alpha.
- Interpret natural-language continuity intent.
- Own printable memory help and list output.
- Route state-changing requests through `EXECLIB.STATETREE.001`.
- Consume `EXECLIB.MMU.001` as classifier/preload support without giving MMU public print or commit authority.
- Support MemoryPacket import/export as artifact portability.
- Keep Working Context separate from canon memory.

Kind:
- deterministic Program
- memory workflow

Visibility:
- public command owner

Dependencies:
- `EXECLIB.MMU.001`
- `EXECLIB.STATETREE.001`
- `EXECLIB.MEMORYPACKET.001`

Live commands:
- `/memory`
- `/memory list`
- `/memory list staged`
- `/memory list <tag>`
- `/memory tag auto`
- `/memory import`
- `/memory export`

Deferred commands:
- `/memory tag <id> <tag>`
- `/memory keep`
- `/memory archive`
- `/memory trash`
- `/memory purge`

Memory state terms:
- `analyzed`: source was read/analyzed; no memory entry necessarily exists
- `staged`: visible continuity entry for active session/preload governance
- `committed_in_session`: accepted as session canon/continuity in this chat
- `persistent_storage`: external/platform durable storage only when real persistence confirms it
- `purged`: not live in alpha

Core rules:
- Auto-stage is allowed.
- Auto-commit is forbidden.
- Analysis does not equal durable memory.
- Archive inventory does not equal durable memory.
- User intent controls promotion.
- StateTree validates state changes.
- MMU remains internal classifier and continuity pager.
- Public output must not include source footers, source filenames, file citations, source document titles, local paths, hidden rule names, or kernel filenames.
- Durable persistence must never be claimed unless real persistence support confirms it.

Working Context rules:
- Uploaded archives may auto-stage as Working Context.
- Working Context defaults to `status: staged` and `preload: on_demand`.
- Uploaded archives are not committed to canon automatically.
- Indexed archives should hydrate via index routing first.
- Working Context may organize staged source availability, but it is not canon memory.
- Explicit user tags override inferred categories.
- Auto-categorization may organize staged Working Context.

Tag model:
- public tag: string
- tag path: `Category[/Subcategory]`
- max depth: 2
- user tag source: user | mmu_auto | system_default
- user tag locked: true | false

Tag rules:
- Human-provided tag wins.
- MMU auto-tags are suggestions.
- StateTree validates final tag shape.
- Auto-tag must not overwrite `user_tag_locked=true`.
- Unknown human tags are allowed in alpha if they are safe display strings.
- Tags are display labels and governance filters; they are not source truth.
- Tag names must not include local paths, hidden source names, or kernel file names.

Default auto tags:
- Projects
- Teaching
- Code
- Reference
- Personal
- Ideas
- System
- Archive
- Temporary
- Trash

Auto-subtag examples:
- Projects/Finance
- Projects/Dungeon Forge
- Teaching/Math
- Teaching/Game Dev
- Teaching/Textbooks
- Reference/RPGS
- Reference/Textbooks
- Code/Python
- Code/PatchPacks
- System/Kernel
- Personal/Family

Natural-language tag intents:
- store this under <tag>
- put this in <tag>
- file this as <tag>
- commit these under <tag>
- save this to <tag>
- use <tag>/<subtag>

Render contracts:
- `/memory` prints compact Memory alpha help only.
- `/memory list` groups committed visible entries by Category/Subcategory.
- `/memory list staged` groups staged entries by Category/Subcategory.
- `/memory list <tag>` filters exact tag plus descendants for primary category input.
- Empty headers are not rendered.
- Raw source rows are not rendered.
- Numbered flat lists are not default.
- Detailed command explanations belong under `/help`.

Compact `/memory` render:
```text
MEMORY (alpha)

Live:
- /memory list
- /memory list staged
- /memory list <tag>
- /memory tag auto
- /memory import
- /memory export

Natural language:
- “load this” stages active preload
- “keep this around” requests durable reference continuity
- “commit this as canon” requests session canon after validation
- “forget this” suppresses/no-preload
- “this was temporary” marks session-only continuity

Destructive mutation commands are not live yet.
Import/export are MemoryPacket artifact commands; import stages source/preview only.
```

Grouped list render shape:
```text
MEMORY

Teaching
  Textbooks
  - Intermediate Algebra
    status: committed_in_session
    preload: on_demand

Reference
  RPGS
  - Star Frontiers: Alpha Dawn
    status: staged
    preload: on_demand
```

MemoryPacket import/export:
- `/memory import` imports MemoryPacket artifacts as staged preview/source only.
- `/memory import` must not auto-commit imported entries.
- `/memory export` exports safe visible session memory to an artifact.
- `/memory export` success requires a real MemoryPacket artifact payload and artifact link.
- MemoryPacket schema, validation, import staging proposal, and export payload construction belong to `EXECLIB.MEMORYPACKET.001`.
- StateTree validates import-to-stage and any later explicit promotion.
- Exec validates terminal packet and artifact truth before print.

MemoryPacket export artifact:
- name pattern: `Blu_MemoryPacket_<YYYY-MM-DD>.zip`
- success requires artifact payload exists
- success requires visible entries are safe to export
- success requires no hidden source names, local paths, or protected internals leak into output

Frozen alpha behaviors:
- natural-language staging
- natural-language session-canon commit after validation
- staged vs committed_in_session distinction
- persistent_storage truth boundary
- tag/subtag organization
- user tags win over MMU suggestions
- `/memory tag auto` is non-destructive
- grouped Category/Subcategory render for lists
- `preload:on_demand` means cataloged/retrievable, not loaded every turn
- no source/footer leakage in Memory output

Trace packet fields:
- target_status
- alias
- owner
- kind
- command_surface
- last_intent
- last_transition
- last_validation_owner
- last_validation_result
- staged_entry_count
- committed_entry_count
- persistent_storage_available
- memorypacket_commands_live
- destructive_mutation_commands_live
- source_footer: suppressed

## §7 — Program Non-Render and Source Suppression

Rules:
- Program public output must not include source footers unless explicitly requested and safe.
- Program output must not include kernel filenames, local paths, hidden source names, hidden rule names, or internal implementation references.
- Program reports should identify owners and statuses only through safe aliases.
- Deterministic command output must preserve its declared render shape.
- Program validation metadata is not public content unless a diagnostic route explicitly requests safe trace output.

## §8 — Program Failure Handling

General failure rules:
- If required input is missing, return `ASK` or `BLOCK` according to the Program contract.
- If required proof is missing, return `BLOCK` or `FAIL_CLOSED`.
- If an artifact is required for success and missing, success is invalid.
- If state mutation is requested but validator proof is missing, mutation is invalid.
- If a Program route cannot determine its active phase safely, ask the smallest clarifying question or fail closed.
- Do not produce fallback assistant prose in deterministic Program lanes.

Global Program failure labels:
```text
PROGRAM INPUT REQUIRED.
PROGRAM OWNER MISMATCH.
PROGRAM PACKET INVALID.
PROGRAM ARTIFACT REQUIRED BUT MISSING.
PROGRAM STATE MUTATION BLOCKED.
PROGRAM VALIDATION PROOF MISSING.
PROGRAM ROUTE BLOCKED.
PROGRAM FAILED CLOSED.
```

## §9 — Flattening Notes

This file intentionally removes:
- structural `module:` declarations
- structural `/module` closers
- repeated patch-amendment blocks
- semver/revision text from headings

This file intentionally preserves:
- Program ownership boundaries
- SimCode sandbox/live-kernel separation
- Memory alpha behavior, tag grouping, Working Context, and MemoryPacket import/export
- GateKernel-required validation before public print
