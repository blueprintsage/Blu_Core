# Chat and Codex Host Adapter Contracts

status: review
owner: docs/domains/runtime
last_reviewed: 2026-08-08
assignment: BC-020

BC-020 binds the BC-018 Generic Host Adapter Boundary to two normalized host
families: `chatgpt` and `codex`. It defines contracts and evidence snapshots;
it implements neither adapter.

The stable family ID is paired with a required `surface_id`. Surface metadata
records only values a provider or bounded probe can truthfully supply. Current
product documentation is recorded as `documented_possible`; only a current
local probe or host receipt can establish `verified_available` for a binding.

Machine-readable records are under `adapters/`. The common contracts define
capability, surface, receipt, error, session-evidence, and authorization-
transport semantics. The family folders contain adapter specialization,
evidence registers, and capability matrices. `adapters/security/` carries the
cross-host matrix and SUR-012 disposition.

The approved ingress remains:

```text
raw_host_event
-> Host Adapter
-> raw_host_input
-> Pre-ingress Security Restraint
```

The Host Adapter does not produce `TurnRequest`, select routes, construct
`ScopeLock`, own OPSEC/Auth policy, decide retries, perform Persona/model
reasoning, own continuity truth, or claim durability. The Turn Controller is
the only `TurnRequest` producer after `SecurityDecision PASS`.

## Reading order

1. `host_capability_truth.md`
2. `chat_adapter.md` or `codex_adapter.md`
3. `security_evidence.md`
4. `receipts_and_failures.md`
5. `adapters/README.md` and the referenced JSON contracts

Repository validation is offline and structural. It never converts current
documentation into a permanent product claim and never proves that a future
host operation will succeed.
