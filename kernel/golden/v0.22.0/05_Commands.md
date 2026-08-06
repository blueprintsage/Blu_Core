---
capsule_id: blu__05_commands
title: "05 Commands"
date: 2026-04-04
updated: 2026-05-21
version: 2.3.1-pass-removed
status: active
topic: blu
type: spec
tags: [commands, boot-surface, auth, echotrace, memory, simcode, help]
sensitivity: medium
visibility: shared
source: doc
domain: core
---

# 05 Commands — Boot Surface

## §1 — Command Surface Canon

Purpose:
- Define the live boot-kernel command surface.
- Own the canonical slash route registry used by RuntimeGate.Ingress.
- Keep `/commands` as short inventory only.
- Keep detailed usage under `/help`.

Authority:
- Commands route only.
- Commands never own workflow behavior.
- RuntimeGate.Ingress owns command resolution.
- Selected owners own command behavior after route lock.
- Public command renders must not include source footers, file citations, source file names, source document titles, local paths, or “Relevant sources” blocks.

## §2 — Live Commands

AUTH:
- `/ID <target> <answer>`
- `/ID logout`
- `/ID reset`

ECHOTRACE:
- `/echotrace ingress`
- `/echotrace scheduler`
- `/echotrace egress`
- `/echotrace all`
- `/echotrace last`
- `/echotrace <target>`

SIMCODE:
- `/simcode <command>`

MEMORY:
- `/memory`
- `/memory list`
- `/memory list staged`
- `/memory list <tag>`
- `/memory tag auto`
- `/memory import`
- `/memory export`

HELP:
- `/commands`
- `/help`

## §3 — Commands Not Live in This Build

These commands must not be listed by `/commands` as live:
- `/mood`
- `/verbosity`
- `/remind`
- `/cpm`
- `/DevMode`
- `/memory tag <id> <tag>`
- `/memory keep`
- `/memory archive`
- `/memory trash`
- `/memory purge`

## §4 — Canonical Slash Route Registry

RuntimeGate.Ingress delegates leading-slash input resolution to this dispatch matrix.

A dispatch row routes only. It must not contain workflow behavior.

Unknown slash stems return no route and must fail closed.

| Stem | Lane Class | Owner | Source / Contract | Terminal Packet Required |
|---|---|---|---|---|
| `/ID` | auth | SERVICE.AUTH.001 | SERVICE.AUTH.001::auth_gate | true |
| `/echotrace` | diagnostic | EXEC.SPINE_TRACE | EXEC.SPINE_TRACE::safe_trace_render | true |
| `/simcode` | sandbox | PROGRAM.SIMCODE.001 | PROGRAM.SIMCODE.001::simcode_program | true |
| `/memory` | workflow | PROGRAM.MEMORY.001 | PROGRAM.MEMORY.001::memory_program | true |
| `/commands` | static_render | COMMANDS | COMMANDS::boot_command_render | true |
| `/help` | static_render | COMMANDS | COMMANDS::boot_help_render | true |

## §5 — Static Render Blocks

Static render blocks must print exactly when their route is selected.

Static render blocks must not include citations, source footers, source filenames, local paths, or source paths.

### §5.1 — `/commands`

```text
COMMANDS (Boot)

AUTH
- /ID <target> <answer>
- /ID logout
- /ID reset

ECHOTRACE
- /echotrace <target>

SIMCODE
- /simcode <command>

MEMORY
- /memory
- /memory list
- /memory list staged
- /memory list <tag>
- /memory tag auto
- /memory import
- /memory export


HELP
- /commands
- /help
```

### §5.2 — `/help`

```text
HELP (Boot)

AUTH
- /ID <target> <answer> — authenticate with a valid target and answer.
- /ID logout — end the current authenticated session.
- /ID reset — reset authentication state.

ECHOTRACE
- /echotrace <target> — show safe diagnostic state.
  Common targets: ingress, scheduler, egress, all, last, MMU, Memory, StateTree, SimCode.

SIMCODE
- /simcode <command> — run sandbox-related SimCode commands when SimCode is enabled.

MEMORY (alpha)
- /memory — show compact Memory alpha help.
- /memory list — show visible staged and committed-in-session memory entries.
- /memory list staged — show staged entries only.
- /memory list <tag> — filter by tag.
  Examples:
  - /memory list Teaching
  - /memory list Teaching/Textbooks
  - /memory list Projects/Finance
- /memory tag auto — non-destructively auto-tags untagged staged entries.
- /memory import — validate an uploaded MemoryPacket and stage it as source/preview only.
- /memory export — create a MemoryPacket artifact from safe visible session memory.

MEMORY TERMS
- staged: visible for this session/preload governance, not durable storage.
- committed_in_session: accepted as session canon after validation.
- persistent_storage: only true when a real persistence path confirms it.
- preload:on_demand: cataloged and retrievable, not loaded into every response.

TAG RULES
- User tags win.
- MMU tags are suggestions.
- Tags may use one subcategory: Category/Subcategory.
- Empty tags are hidden.
- Destructive mutation commands such as purge are not live yet.
- Import/export are MemoryPacket artifact commands; import does not canonize or persist memory.


HELP
- /commands — short command inventory.
- /help — detailed command usage.
```

## §6 — Command Render OPSEC

Public deterministic command output must be citationless unless the user explicitly asks to review source files.

Public deterministic command output must not include:
- `Sources`
- `Supporting sources`
- `Relevant sources`
- `Relevant source notes`
- source file names
- local paths
- file citations
- source line references
- source document titles

## §7 — Memory List Render Contract

`/memory list` renders grouped Category/Subcategory headers by default.

`/memory list staged` renders grouped Category/Subcategory headers by default.

`/memory list <tag>` preserves grouped headers after filtering.

Flat numbered memory lists are compact mode only, not default.

Detailed behavior belongs to PROGRAM.MEMORY.001.

## §8 — ContextIntake Command Boundary

ContextIntake has no public slash command in this build.

ContextIntake is an ExecLib service scheduled by Exec when artifact/source context support is needed.

`/commands` must not list ContextIntake as a user command.

`/echotrace ContextIntake` may resolve if EchoTrace supports service aliases.

## §9 — Command Surface Validation Rules

The live command inventory, dispatch matrix, and static render blocks must agree.

`/commands` must list live commands only.

`/help` may explain usage for live commands only.

A command entry in the live inventory must have a dispatch row.

A dispatch row must resolve to exactly one owner.

A static render command must preserve the exact render block.

Command output must remain citationless and source-footer-free unless the user explicitly asks to review source files.

Commands do not mutate state, execute workflows, or print owner behavior directly. They only route.

## PASS Removal Note

The PASS command is not live in this build. PASS extraction is externalized to a staged absolute spec and is not implemented as a kernel Program, command, service, or ExecLib component.
