# CTS Source Roles

status: active
owner: docs/domains/kernel
last_reviewed: 2026-08-05

## Purpose

Define the source-role boundary inside the immutable Blu v0.22.0 CTS archive so
migration work does not flatten GPT host instructions and kernel/runtime
capsules into one undifferentiated component source.

This document classifies the golden files. It does not modify or supersede them.

## Golden source set

### Deployment instruction

```text
kernel/golden/v0.22.0/00_Instructions.md
```

Source role: `deployment_instruction`

`00_Instructions.md` is loaded into the GPT instruction box. It is authoritative
for host-facing bootstrap, source loading, precedence, and operating
expectations.

It is part of the CTS golden source set, but it is not one of Blu's six main
kernel/runtime capsules.

### Kernel/runtime capsules

```text
kernel/golden/v0.22.0/01_Persona.md
kernel/golden/v0.22.0/02_Operations_Law.md
kernel/golden/v0.22.0/03_Exec.md
kernel/golden/v0.22.0/04_Exec_Library.md
kernel/golden/v0.22.0/05_Commands.md
kernel/golden/v0.22.0/06_Programs.md
```

Source role: `kernel_runtime_capsule`

These six Markdown sources comprise Blu's current main kernel/runtime.

## Extraction rules

1. Preserve the authority and immutability of all seven CTS files.
2. Record `00_Instructions.md` as `deployment_instruction`, not as a
   `kernel_runtime_capsule`.
3. Record `01_Persona.md` through `06_Programs.md` as
   `kernel_runtime_capsule`.
4. Do not treat a component name in `00_Instructions.md` as a complete kernel
   component definition unless a kernel/runtime capsule also defines it.
5. A host/bootstrap dependency named only in `00_Instructions.md` must be
   identified as host-declared or referenced-only, with source provenance.
6. A component required directly by a kernel/runtime capsule but not defined in
   the six-capsule kernel remains a referenced-but-undefined runtime
   declaration.
7. When both source roles mention the same owner or rule, preserve both
   provenances; do not silently collapse them.
8. A Markdown declaration does not prove that the host supplies a real
   capability or that Python implementation exists.
9. Generated contracts remain descriptive and downstream-only. They never
   outrank the CTS source set.
10. Source-role correction does not authorize repair of conflicts inside the
    golden source. Conflicts remain unresolved unless an approved successor
    specification explicitly resolves them.

## Terminology

Use:

- **CTS source set** for all seven golden files.
- **deployment instruction** for `00_Instructions.md`.
- **kernel** or **kernel/runtime capsules** for `01_Persona.md` through
  `06_Programs.md`.
- **current CTS deployment** for the combined host instruction plus six
  Markdown capsules.

Avoid calling all seven files the kernel.

## Successor classification (BC-050-C2A, 2026-08-13)

The classification above records the current and historical CTS deployment
truthfully and is unchanged. Dad/Blu added a prospective successor distinction:

- current/historical CTS role: GPT host/deployment instruction — unchanged.
- successor invariant canon: **no**.
- automatic migration into the successor: **no**.
- Python parity obligation: **no**.

`00_Instructions.md` remains immutable golden provenance. It primarily
stabilized a hosted model that was not running Blu's deterministic
architecture, and instruction text cannot be assumed to have made those
behaviors persistent. Appearing in that surface is therefore not evidence that a
behavior is invariant Blu canon.

Surviving successor behavior is owned by Persona, Operations Law, and approved
deterministic successor contracts. A behavior found only in the instruction
surface may be promoted later by explicit Dad/Blu action into its proper owner,
with tests. There is no automatic resurrection.

Recorded in `readiness/one_blu_canon_manifest.json#legacy_deployment_artifacts`.
