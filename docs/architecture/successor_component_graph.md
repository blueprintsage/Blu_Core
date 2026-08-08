# Successor Component Graph

status: review
owner: docs/domains/runtime
last_reviewed: 2026-08-08
assignment: BC-018
correction: BC-018-C1

## One-page graph

```mermaid
flowchart LR
    Host["raw_host_event"] -->|"translate only"| Adapter["Generic Host Adapter"]
    Adapter -->|"raw_host_input"| OPSEC["Pre-ingress Security Restraint"]
    OPSEC -->|"PASS + minimized allowed_input"| Controller["Turn Controller constructs TurnRequest"]
    OPSEC -->|"Turn N: BLOCK or proposed ASK"| Egress["Validation and Egress"]
    OPSEC -->|"proposed pending request"| Pending[("PendingAuthorizationState\nstate record, not component")]
    Adapter -->|"attempt evidenced host_session binding"| Pending
    Pending -->|"bound: activate + one ASK terminal"| Egress
    Pending -->|"binding unavailable: inactive + one UNAVAILABLE terminal"| Egress
    Egress -->|"one safe TerminalPacket\nSecurityDecision authority pre-ingress"| Adapter
    NextHost["Turn N+1 raw_host_event"] --> Adapter
    Pending -->|"still-valid request binding"| Adapter
    Adapter -->|"bounded authorization evidence only"| Auth["Authorization Evaluator"]
    Auth -->|"AuthorizationResult + pending context"| OPSEC
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

The Host Adapter never constructs `TurnRequest`. The authorization path is
cross-turn and does not enter the Turn Controller while pending. In Turn N, a
proposed `PendingAuthorizationState` becomes active only if evidenced
host-session binding succeeds; success emits one safe `ASK` terminal packet.
Unavailable binding leaves the proposal inactive and non-resumable and emits
one safe `UNAVAILABLE` terminal packet instead. Both use the originating
`SecurityDecision` authority and owner `security_restraint`; no
`ControlDecision` exists. A new host event in Turn N+1 must be correlated
through provider evidence to the still-valid request before the bounded Auth
exchange. `AuthorizationResult` returns to the Security Restraint, and only a
new `SecurityDecision PASS` permits normalization and ordinary routing. Each
host turn has exactly one terminal packet. The state-record node is not an
eighth component or a ninth packet.

## Exclusive deterministic responsibilities

| Responsibility | Owner |
|---|---|
| OPSEC pre-ingress decision, input minimization, and whether an authorization interaction may start, retry, re-enter, expire, exhaust, cancel, or reject replay | Pre-ingress Security Restraint |
| Authorization evidence sufficiency, assurance, action/resource result, and revocation/reset semantics | Authorization Evaluator |
| Host-session substrate and returned-event/request correlation evidence | Generic Host Adapter Boundary (storage/evidence, not policy authority) |
| `SecurityDecision PASS` + `allowed_input` normalization into `TurnRequest`; supplied-time arithmetic, capability validation, route, owner, ScopeLock, service dispatch authorization | Turn Controller |
| Source policy, artifact/completion proof, terminal status, egress, receipt-backed diagnostics | Validation and Egress |

No responsibility appears twice. Construction and validation are distinct:
the Turn Controller constructs ScopeLock, while Validation and Egress checks the
candidate against it. That is not duplicate ownership.

## Exec decomposition

| Historical/current Exec responsibility | Successor owner | Disposition |
|---|---|---|
| pre-ingress security scheduling | Security Restraint is placed directly at the boundary | deterministic; recovered without scheduler ownership |
| pre-ingress Auth evaluation/state | Security Restraint owns attempt policy; Authorization Evaluator owns evidence/result semantics; Host Adapter carries evidenced `host_session` state; result re-enters Security Restraint in a new host turn | hybrid; bounded cross-turn contract; no ordinary routing |
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
