# Blu v0.22.0 Runtime Contracts

status: extracted
owner: docs/domains/runtime
source_runtime: kernel/golden/v0.22.0
assignment: BC-010

## Purpose

This directory is a machine-readable extraction of declarations in Blu's
current CTS Markdown runtime. It describes the v0.22.0 model-executed runtime;
it is not a Python implementation, a replacement runtime, or a new source of
behavioral authority.

The seven golden Markdown files remain authoritative. If a contract here
differs from a golden source, the golden source wins. Registry presence does
not prove that a host capability or executable implementation exists.

## Golden sources

- `kernel/golden/v0.22.0/00_Instructions.md`
- `kernel/golden/v0.22.0/01_Persona.md`
- `kernel/golden/v0.22.0/02_Operations_Law.md`
- `kernel/golden/v0.22.0/03_Exec.md`
- `kernel/golden/v0.22.0/04_Exec_Library.md`
- `kernel/golden/v0.22.0/05_Commands.md`
- `kernel/golden/v0.22.0/06_Programs.md`

## Contract set

- `source_map.json` maps extracted objects to a golden file and section.
- `component_registry.json` records declared owners and referenced components.
- `route_registry.json` records restraint, ingress, command, and fallback routes.
- `schemas/` contains JSON Schemas for the packet shapes required by BC-010.
- `parity_matrix.json` records behavioral requirements and future parity cases.
- `unresolved_register.json` preserves conflicts and underspecified declarations.

## Extraction rules

- Preserve CTS terminology when it is structurally usable.
- Record explicit declarations separately from conflicts and expressive prose.
- Collapse repeated declarations into one registry object only when provenance
  for every declaration is retained.
- Do not resolve conflicts or fill absent component definitions.
- Keep Persona and Operations Law model-facing; schemas do not replace them.
- Treat a referenced owner without a defining component block as
  `declared_but_not_defined`.
- Treat schemas for absent packet definitions as intentionally permissive and
  record the missing definition in `unresolved_register.json`.
- Do not treat Markdown declarations as proof of host capability, persistence,
  background execution, or artifact creation.

## Validation

Run:

```text
python tools/validate_runtime_contracts.py
python -m unittest discover -s tests/contracts -p "test_*.py"
```

The validator parses every JSON file, checks required contract files and schema
files, verifies source-map targets and references, checks component ID
uniqueness by namespace, checks public command-stem ownership, resolves local
schema references, and validates the contract fixtures used by the tests.
