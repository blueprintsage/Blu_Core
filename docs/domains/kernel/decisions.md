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
