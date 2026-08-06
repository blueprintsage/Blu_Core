# Bootstrap Validation Receipt

status: active
owner: docs/domains/build-release
last_reviewed: 2026-08-05

## Repository

- Branch: `main`
- Bootstrap version: `0.1.0-bootstrap`
- Current runtime implementation: Markdown only
- Python Blu runtime: not present

## Golden source checks

The CTS archive was copied into `kernel/golden/v0.22.0/`, extracted, and each
extracted file was compared byte-for-byte with the corresponding ZIP member.
All seven comparisons passed.

`sha256sum -c kernel/golden/v0.22.0/SHA256SUMS` passed for:

- `00_Instructions.md`
- `01_Persona.md`
- `02_Operations_Law.md`
- `03_Exec.md`
- `04_Exec_Library.md`
- `05_Commands.md`
- `06_Programs.md`
- the retained CTS source archive

## Governance checks

- Dad is recorded as Project Owner.
- Blu is recorded as Project Lead.
- Claude and Codex are bounded development agents.
- Codex is the preferred Git steward.
- Golden kernel mutation is prohibited.
- `Blu_KB_Preview` and `libraries/` are recorded as current.
- `Blu_KB` and `library/` are recorded as retired/legacy.
