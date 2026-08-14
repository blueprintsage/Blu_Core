# Blu Core

Blu Core is the canonical development repository for migrating Blu v0.22.0
from a complete Markdown-defined, model-executed runtime into a lighter hybrid
architecture without making her less Blu.

## Current truth

- Blu's current CTS deployment is a Markdown source set with two source roles:
  - `00_Instructions.md` is the GPT host/deployment instruction document.
  - `01_Persona.md` through `06_Programs.md` are the six Blu kernel/runtime
    capsules loaded as Markdown sources.
- The complete golden CTS source set is preserved byte-for-byte under
  `kernel/golden/v0.22.0/`.
- A Phase 1 Python Blu runtime now exists for boot and ordinary conversation through the LM Studio model boundary; later runtime phases remain unimplemented.
- `Blu_KB_Preview` is the current continuity/reference repository.
- `agent-kit` supplies the repository coordination scaffold.
- Alice supplies a profile-controller reference, not an identity merge target.

## Authority

- Dad is Project Owner and final authority.
- Blu is Project Lead.
- Claude and Codex work through bounded assignments.
- `AGENTS.md` is the canonical repository entrypoint.

## Start here

```text
AGENTS.md
docs/dev/docs_index.md
docs/architecture/current_runtime.md
docs/sources/cts_source_roles.md
docs/architecture/migration_centerline.md
docs/worklogs/assignments.md
```

## Validate the bootstrap

```bash
git diff --check
sha256sum -c kernel/golden/v0.22.0/SHA256SUMS
```

## Git setup

See `SETUP.md` for cloning the supplied bundle or publishing this checkout to a
new remote.
