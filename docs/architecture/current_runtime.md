# Current Blu Runtime

status: active
owner: docs/domains/kernel
last_reviewed: 2026-08-05

## Baseline

Blu v0.22.0 is a complete Markdown-defined, model-executed runtime.

The current runtime consists of:

1. `00_Instructions.md`
2. `01_Persona.md`
3. `02_Operations_Law.md`
4. `03_Exec.md`
5. `04_Exec_Library.md`
6. `05_Commands.md`
7. `06_Programs.md`

These files are not documentation for an undiscovered Python implementation.
They are the current operational source and golden migration baseline.

## Ownership centerline

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
