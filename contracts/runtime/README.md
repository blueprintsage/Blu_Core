# Blu v0.22.0 Runtime Contracts

status: extracted
owner: docs/domains/runtime
source_runtime: kernel/golden/v0.22.0
assignment_lineage:
  - BC-010
  - BC-010-C1
  - BC-010-C2

## Purpose

This directory is a machine-readable extraction of declarations in Blu's
current CTS Markdown runtime. It describes the v0.22.0 model-executed runtime;
it is not a Python implementation, a replacement runtime, or a new source of
behavioral authority.

The seven-file CTS source set remains authoritative. It contains one GPT
deployment instruction and six kernel/runtime capsules. If a contract here
differs from either source role, the golden source wins. Registry presence does
not prove that a host capability or executable implementation exists.

## Golden source roles

- Deployment instruction (`deployment_instruction`):
  `kernel/golden/v0.22.0/00_Instructions.md`. It is loaded in the GPT
  instruction box and owns host/bootstrap declarations; it is not one of the
  six main kernel/runtime capsules.
- Kernel/runtime capsules (`kernel_runtime_capsule`):
  `01_Persona.md`, `02_Operations_Law.md`, `03_Exec.md`,
  `04_Exec_Library.md`, `05_Commands.md`, and `06_Programs.md` under
  `kernel/golden/v0.22.0/`.

All seven files remain golden and authoritative. A deployment-only reference
is a host/deployment declaration or a referenced-only declaration, not a
kernel component definition. Generated contracts are downstream-only and do
not outrank either source role.

## Contract set

- `source_map.json` maps extracted objects to a golden file and section.
- `component_registry.json` records declared owners and referenced components.
- `route_registry.json` records restraint, ingress, command, and fallback routes.
- `schemas/` contains JSON Schemas for the packet shapes required by BC-010.
- `parity_matrix.json` records behavioral requirements and future parity cases.
- `unresolved_register.json` preserves conflicts and underspecified declarations.

## Extraction rules

- Preserve CTS terminology when it is structurally usable.
- Record explicit declarations separately from extraction inference, conflicts,
  and expressive prose.
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

The project-local validator uses only Python's standard library. It is not a
general JSON Schema implementation. Its supported validation subset is:
`$ref`, `allOf`, `type`, `enum`, `const`, `minLength`, `uniqueItems`, `items`,
`required`, `properties`, and boolean `additionalProperties`. It permits the
annotations `$schema`, `$id`, `title`, `description`, and `x-*`. Any other
schema validation/applicator keyword or unknown type fails clearly.

The standalone command parses every contract JSON file, checks required
contract/schema/fixture files, resolves every source-map entry to exactly one
declared source role and an exact Markdown heading anchor, checks source-map
references, component ID uniqueness, public command-stem ownership, schema IDs
and local references, and validates all canonical positive and negative
fixtures under the supported subset.

These checks prove only the stated structural constraints and fixture results.
They do not prove full JSON Schema compliance, runtime implementation, host
capability, behavioral parity, persistence, routing execution, or artifact
creation.
