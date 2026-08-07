# BC-015 — Runtime Viability Audit Report

status: review
owner: docs/domains/runtime
last_reviewed: 2026-08-06

## Executive result

The current CTS contains valuable behavioral law and many detailed support contracts, but the available evidence does not support treating its component graph as an executing control plane. BC-015 inventories 30 capability groups covering all 47 component entries, 76 normalized route-surface entries, 12 parity requirements, and 28 unresolved items.

No capability qualifies as `live_and_stable`. Dad and Blu's observations support three current capabilities as live but nondeterministic: Persona warmth/presence, Auth, and OPSEC. Eight groups are declared but unproven, twelve are conflicting or underspecified, five are explicitly removed/deferred, and two are successor-only mechanisms.

The historical v0.15.2 baseline was unavailable. Historical recovery conclusions therefore remain limited to owner observation; no checksum, member path, or archive-derived behavior claim is made.

## Inventory coverage

| Inventory | Covered | Total |
|---|---:|---:|
| Component registry entries | 47 | 47 |
| Normalized route-surface entries | 76 | 76 |
| Parity requirements | 12 | 12 |
| Unresolved-register items | 28 | 28 |

The 76 route identifiers normalize restraint steps, ingress steps, declared and route-table-only lanes, live stems, active/deferred/unavailable forms, non-live features, non-slash routes, the artifact hook, unknown-slash behavior, and one-owner rules. `viability_matrix.json` lists the exact normalized inventory.

## Classification totals

| Current classification | Count |
|---|---:|
| `live_and_stable` | 0 |
| `live_but_nondeterministic_or_host_dependent` | 3 |
| `declared_but_not_observably_functioning` | 8 |
| `conflicting_or_underspecified` | 12 |
| `explicitly_deferred_or_removed` | 5 |
| `new_successor_runtime_capability` | 2 |

## Strongest current capabilities

The strongest current evidence is behavioral rather than mechanical:

- Persona warmth, presence, and relational posture remain observable, though model/context pressure makes consistency unproven.
- Auth has observably authorized Admin-level users, but recognition and enforcement are nondeterministic and its service/render contract is absent.
- OPSEC refusal/interception has observably protected ID challenges and kernel-copy/clone requests, but its current owner is undefined in the kernel capsule, its lane class is absent, and enforcement remains model/host-dependent.
- The source-truth, work-state, artifact-proof, and hosted-single-turn distinctions are coherent and useful contracts. They are not execution proof.

## Declared but unproven machinery

The CTS richly declares Exec scheduling, restraint order, ingress priority, owner locking, ScopeLock, terminal packets, egress validation, fail-closed behavior, current-turn receipts, EchoTrace, Programs, source intake, Read Lane, time support, Memory, and multiple deterministic libraries. No current GPT-host probes were run, so those declarations remain unproven. Static status `ACTIVE`, exact packet prose, and BC-010 registry presence do not change that conclusion.

The highest-risk illusion is packet theater: the model can describe a route, gate, receipt, or validation step without an independent mechanism proving it happened.

## Conflicts and source gaps

The most consequential gaps are:

- AntiDrift and Operations restraint are mandatory but undefined.
- Auth, OPSEC, RepoBoot, EchoTrace support, BluCode, runtime configuration, GateKernel, and Program gates are referenced but undefined.
- StateTree is both `ALPHA` and `ACTIVE`.
- `/memory` uses `workflow`, absent from Exec's declared lane enum.
- Task packet and capability-report fields are missing; the current-turn receipt is an alias, not a distinct structure.
- Memory Program lacks complete Universal Program inputs/outputs/result declarations.
- Error catalog identities/render behavior, Humor owners, Persona Engine, and alias coverage remain incomplete.
- Current OPSEC route-lane/pre-ingress semantics remain unresolved in the CTS. The approved successor restraint must not be projected backward.

## Explicitly retired or deferred surfaces

The current build excludes public `/mood`, `/remind`, `/verbosity`, `/cpm`, and `/DevMode`. PASS is explicitly not live. Manual/destructive memory forms—tag mutation, keep, archive, trash, and purge—are deferred. Relational warmth remains a Persona behavior even though the public mood command is absent.

## Legacy recovery

Direct historical evidence is unavailable. Owner observation supports only this cautious conclusion:

- Teaching-oriented behavior may be worth recovering as a lightweight profile or playbook.
- The gate-heavy legacy Exec architecture is not worth restoring.
- PASS should not be restored from historical presence alone.
- Reminder/time, mood, PersonaLib, MMU, Read Lane, continuity, and artifact behaviors remain unresolved until the supplied archive is directly inspected.

The audit deliberately separates `behavior_worth_recovering` from `architecture_worth_reusing`; the latter defaults to false for every currently discussed legacy candidate.

## Deterministic, model, profile, and host responsibilities

Likely deterministic Python candidates:

- configuration and adapter capability reports;
- versioned task, ScopeLock, terminal, and receipt schemas;
- route and owner locks;
- dependency allowlists;
- packet and egress validation;
- source/work-state transitions and artifact-proof checks;
- safe receipt-backed diagnostics;
- pure date/time parsing and math;
- Auth workflow state support and the approved OPSEC pre-ingress hook.

Likely model-facing responsibilities:

- Persona identity, warmth, presence, relational judgment, and internal mood-source formation;
- Operations truth, correction, anti-drift, and semantic scope judgment;
- ordinary task execution and source interpretation;
- safe, approved user-facing wording for Auth/OPSEC outcomes.

Likely profile candidates:

- Teaching first;
- task-specific reading/source-handling posture rather than six preserved Read Lane services;
- Companion, Focused, Creative, and Hard Reality as already named by the migration centerline.

Host responsibilities:

- actual deployment loading;
- repository/tool/artifact access;
- secure Auth state/secrets;
- clock, scheduler, and notifications;
- sandboxing;
- any real persistence.

## Hypothesis assessment

| # | Hypothesis | Result | Basis |
|---|---|---|---|
| 1 | Persona and Operations remain primarily model-facing. | supported | They define semantic identity/law and explicitly deny routing/print ownership. |
| 2 | Packets, locks, capability detection, ScopeLock mechanics, terminal validation, and receipts are deterministic candidates. | supported | They are bounded mechanics, match the approved first implementation boundary, and address packet theater. |
| 3 | Auth needs deterministic workflow support. | supported | Owner observation shows value; undefined service/state makes model-only enforcement unreliable. |
| 4 | OPSEC needs deterministic successor pre-ingress enforcement. | supported | Explicit Dad/Blu successor decision; current nondeterminism remains separate. |
| 5 | Teaching is more likely a lightweight profile. | partially_supported | Owner observation and migration profiles support it; direct v0.15.2 archive evidence is unavailable. |
| 6 | Public reminders require real host scheduling. | supported | Hosted loop denies self-wake; /remind is unavailable; current-turn record shaping is not notification delivery. |
| 7 | Date math can be deterministic while live-time acquisition is host-dependent. | supported | DateLib/Time Service explicitly separate those roles. |
| 8 | Read Lane may reduce to source handling, citation discipline, and profiles. | partially_supported | Current behavior contracts support a smaller split, but no live or historical comparative evidence was available. |
| 9 | PASS should not be restored from historical presence. | supported | Current CTS explicitly removes it and no unique behavioral evidence supports recovery. |
| 10 | Current component names should not determine future service boundaries. | supported | Many names are undefined, conflicting, or overly granular; behavior is the migration unit. |

## Smallest honest successor-runtime control plane

The smallest control plane supported by current evidence is:

1. a versioned configuration and host-capability report;
2. a typed current-turn task packet and ScopeLock;
3. deterministic pre-ingress security hook placement for the approved OPSEC boundary and an Auth workflow hook;
4. exact route/stem matching, one lane/one owner lock, and dependency allowlists;
5. terminal-packet, artifact-proof, and egress validation;
6. a current-turn execution receipt and safe receipt-backed diagnostics;
7. adapters that report real repository, artifact, time, scheduler, and persistence capabilities.

Persona and Operations remain model-facing inputs to that shell. The shell does not initially include durable memory, reminders without a real scheduler, SimCode, PASS, restored public mood commands, legacy Read Lane topology, or a general Program framework.

Available evidence is sufficient to begin specifying this smallest shell, but not to claim it works and not to select final packet fields or security contracts without Dad/Blu approval.

## Decisions reserved for Dad and Blu

- Exact task, capability, terminal, and receipt schemas.
- Security-authorized Auth and OPSEC matching/render contracts.
- Whether Program gates and EchoTrace support survive as separate services.
- Whether GreetingLib, PersonaLib, MoodLib, and the six Read Lane names survive.
- Whether/when public mood, reminders, SimCode, or memory durability enter scope.
- All 28 unresolved-register items.
- Historical recovery after the exact archive is supplied.
