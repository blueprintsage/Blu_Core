# Kernel Decisions

status: active
owner: docs/domains/kernel
last_reviewed: 2026-08-05

- Bootstrap authority is defined by `AGENTS.md` and
  `docs/sources/authority_map.md`.
- The CTS golden source set has two source roles:
  - `00_Instructions.md` is the GPT host/deployment instruction document loaded
    into the GPT instruction box.
  - `01_Persona.md` through `06_Programs.md` are Blu's six main kernel/runtime
    capsules loaded as Markdown sources.
- `00_Instructions.md` remains golden and authoritative, but it must not be
  classified as a kernel capsule during contract extraction.
- Source-role classification does not authorize edits to any file under
  `kernel/golden/`.
