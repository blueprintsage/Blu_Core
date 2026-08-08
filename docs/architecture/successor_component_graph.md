# Successor Component Graph

status: review
owner: docs/domains/runtime
last_reviewed: 2026-08-08
assignment: BC-018

## One-page graph

```mermaid
flowchart LR
    Host["Host input"] --> Adapter["Generic Host Adapter"]
    Adapter --> OPSEC["Pre-ingress Security Restraint"]
    OPSEC -->|"PASS: minimized allowed input"| Controller["Turn Controller"]
    OPSEC -->|"BLOCK / ASK"| Egress["Validation and Egress"]
    Controller <-->|"authorization request / result"| Auth["Authorization Evaluator"]
    Auth <-->|"explicit evidence only"| Adapter
    Controller <-->|"candidate / structured request"| Model["Model Execution Boundary"]
    Controller <-->|"generic service exchange"| Adapter
    Adapter <-->|"time, schedule, tools, source, skill, artifact"| Services["Host Services"]
    Controller <-->|"versioned read/write"| Continuity["Continuity Provider Boundary"]
    Model -->|"candidate result"| Egress
    Adapter -->|"service and artifact receipts"| Egress
    Controller -->|"ControlDecision + ScopeLock"| Egress
    Egress -->|"one TerminalPacket + current-turn receipt"| Adapter
    Adapter --> Output["Host output delivery"]
```

The arrows describe contracts, not live calls. Host services and continuity are
not implied available. Every used path requires a verified capability record;
side effects and durable writes require provider receipts.

## Exclusive deterministic responsibilities

| Responsibility | Owner |
|---|---|
| OPSEC pre-ingress decision and input minimization | Pre-ingress Security Restraint |
| Authorization policy evaluation and session transition validation | Authorization Evaluator |
| Ingress normalization, capability validation, route, owner, ScopeLock, service dispatch authorization | Turn Controller |
| Source policy, artifact/completion proof, terminal status, egress, receipt-backed diagnostics | Validation and Egress |

No responsibility appears twice. Construction and validation are distinct:
the Turn Controller constructs ScopeLock, while Validation and Egress checks the
candidate against it. That is not duplicate ownership.

## Exec decomposition

| Historical/current Exec responsibility | Successor owner | Disposition |
|---|---|---|
| pre-ingress security scheduling | Security Restraint is placed directly at the boundary | deterministic; recovered without scheduler ownership |
| Auth dispatch/state | Authorization Evaluator plus evidence-provider interface | hybrid; bounded contract |
| routing and arbitration | Turn Controller | deterministic |
| one-owner enforcement | Turn Controller | deterministic |
| ScopeLock construction | Turn Controller | deterministic |
| dependency allowlist and dispatch authorization | Turn Controller | deterministic |
| Persona-shaped ordinary execution | Model Execution Boundary | model-facing |
| Operations semantic anti-drift | Model Execution Boundary under current law | model-facing |
| source-policy and claim-result enforcement | Validation and Egress | hybrid policy with model-dependent semantic mapping |
| packet, capability, transition, and artifact validation | Validation and Egress | deterministic |
| final egress and receipt | Validation and Egress | deterministic |
| diagnostics | Validation and Egress receipt view | deterministic; no service |
| host tool execution, time, scheduling, delivery | Host services through adapter | host-owned |
| durable memory | Continuity provider | external |
| feature-specific workflows and mega-Exec accumulation | none | rejected |

There is no catch-all successor owner and no component named Exec.

## Component removal test

Removing any of the four deterministic components creates a concrete failure:
pre-ingress policy moves too late; authorization becomes conversational;
route/owner/scope lose a single control owner; or output becomes
self-certified. Removing a boundary component would falsely assign model,
platform, or durable-storage authority to the core.

No other historical component passes that test, so none is retained.
