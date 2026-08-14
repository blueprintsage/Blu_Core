# Source Authority Map

status: active
owner: docs/domains/repository
last_reviewed: 2026-08-05

## Locked decisions

- The CTS archive is the golden truth for Blu's current deployment.
- The CTS golden source set contains:
  - `00_Instructions.md` as the GPT host/deployment instruction document.
  - `01_Persona.md` through `06_Programs.md` as the six Blu kernel/runtime
    capsules.
- `00_Instructions.md` remains authoritative and immutable, but it is not one of
  the six main kernel/runtime capsules.
- `Blu_KB_Preview` on `main` is the current continuity/reference repository.
- `Blu_KB` without `_Preview` is retired.
- `libraries/` is current.
- `library/` is old SkillForge material and is not used by the current runtime.
- The agent kit is the canonical startup scaffold for Blu Core repositories.
- Alice is a behavioral-mode reference only.
- Standalone SkillForge and Local Mirror are external reference/compatibility
  inputs, not current Blu runtime code.

## Source order

1. Dad's current explicit instruction.
2. Approved Blu Core decisions.
3. CTS golden source set:
   - GPT host/deployment instruction;
   - six kernel/runtime capsules.
4. Active Blu Core documents.
5. Indexed sources from the live continuity repository.
6. Approved reference material.
7. Legacy or experimental sources.

Conflicts are recorded; they are never silently merged.

See `docs/sources/cts_source_roles.md` for extraction and classification rules.

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
