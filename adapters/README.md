# BC-020 Host Adapter Contracts

status: review
owner: docs/domains/runtime
last_reviewed: 2026-08-08
assignment: BC-020

These artifacts specialize the BC-018 Generic Host Adapter Boundary for the
`chatgpt` and `codex` host families. They are specifications and evidence
snapshots, not executable adapters, capability detectors, security policy, or
a successor runtime.

The contracts consume the approved generic ingress and packet semantics without
modifying `contracts/successor/**`. A future adapter translates
`raw_host_event` to `raw_host_input`, reports evidence-backed capabilities,
transports bounded host services and approvals, and returns receipts. It never
constructs `TurnRequest`, owns OPSEC/Auth policy, selects ordinary routes,
constructs `ScopeLock`, supplies Persona reasoning, or invents persistence.

`official_documentation` proves product/surface possibility or limitation only.
`verified_available` requires evidence from the current binding, such as a
bounded local probe or provider receipt. All observations are scoped and may
be invalidated by surface, configuration, permissions, sandbox, network,
workspace policy, integrations, or provider state.

## Layout

```text
common/       normalized records, vocabularies, receipts, failures, and auth transport
chat/         Chat/ChatGPT family contract, capability snapshot, evidence register
codex/        Codex family contract, capability snapshot, evidence register
security/     cross-host security-evidence matrix and SUR-012 disposition
```

Use `python tools/validate_host_adapter_contracts.py` for deterministic contract
integrity. It deliberately performs no live web access and proves no provider
capability.
