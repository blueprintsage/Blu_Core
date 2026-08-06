# Current Blu Runtime

status: active
owner: docs/domains/kernel
last_reviewed: 2026-08-05

## Baseline

Blu v0.22.0 is a complete Markdown-defined, model-executed runtime deployment.

The CTS archive contains one deployment instruction document and six
kernel/runtime capsules. They are operational sources, not documentation for an
undiscovered Python implementation.

## Source roles

### GPT host/deployment instruction

```text
00_Instructions.md
```

`00_Instructions.md` is loaded into the GPT instruction box. It defines the
host-facing bootstrap, loading, precedence, and operating expectations for the
Markdown runtime.

It is part of the golden CTS source set, but it is not one of Blu's six main
kernel/runtime capsules.

### Blu kernel/runtime capsules

```text
01_Persona.md
02_Operations_Law.md
03_Exec.md
04_Exec_Library.md
05_Commands.md
06_Programs.md
```

These six files are loaded as Markdown sources and comprise Blu's current main
kernel/runtime.

Together, the deployment instruction and six capsules form the complete current
CTS deployment and golden migration baseline.

## Ownership centerline

- `00_Instructions.md` owns GPT host/deployment bootstrap instructions.
- Persona makes the agent Blu.
- Operations Law keeps Blu coherent and truthful.
- Exec schedules the hosted single-turn loop and owns final validation/print.
- ExecLib defines deterministic support contracts.
- Commands defines the active route surface.
- Programs owns the current workflow contracts.

## Migration truth

Python does not exist yet as Blu's runtime. Any future Python code is a new
implementation of selected deterministic contracts and must preserve the golden
behavior until an approved change explicitly supersedes it.

Source-role separation does not reduce the authority of `00_Instructions.md`.
It prevents host/bootstrap declarations from being silently classified as
kernel component definitions.
