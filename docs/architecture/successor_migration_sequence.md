# Successor Migration Sequence

status: review
owner: docs/domains/runtime
last_reviewed: 2026-08-08
assignment: BC-018
correction: BC-018-C1

## Boundary

This is a dependency-ordered implementation plan only. BC-018 implements none
of these steps. Each future step requires its own approved packet, exact base,
collision domain, tests, review, and revertible commit.

## Proposed sequence

1. **Core data contracts and fixtures**
   - implement the eight packet types and six statuses;
   - implement `PendingAuthorizationState` as a state record, not a packet;
   - validate field, evidenced lifetime, identity, authority-class, and
     cross-reference invariants;
   - use no host, model, or continuity implementation.

2. **Capability and state-transition validation primitives**
   - distinguish declared from verified capability;
   - validate expiry/scope, state lifetime transitions, provider receipts, and
     durable/scheduling dependency rules.

3. **Pre-ingress Security Restraint**
   - begin only after a security-authorized OPSEC policy packet resolves
     `SUR-001`;
   - test ordering, content minimization, redaction authorization, the
     cross-turn Auth re-entry loop, sole attempt-policy ownership, finite
     repetition, expiry, replay rejection, fail-closed exhaustion, deliberate
     handling of an uncorrelated intervening turn under `SUR-011`, and one
     terminal packet per host turn without publishing protected details or
     entering ordinary routing.

4. **Authorization Evaluator**
   - begin only after accepted evidence and assurance rules resolve `SUR-002`;
   - test action/resource scope, evidence sufficiency, assurance,
     host-session-bound or continuity-receipted validity, expiry/reset,
     unavailable evidence, safe request binding, and return to OPSEC for a new
     pre-ingress decision without owning retry policy.

5. **Turn Controller**
   - normalize allowed turns;
   - remain turn-local and accept any optional cross-turn context only as
     evidenced input supplied for the current turn;
   - perform only deterministic arithmetic over supplied time values; current
     time still requires provider evidence;
   - validate capabilities;
   - implement a separately approved minimal route catalog;
   - lock one owner, build/revise ScopeLock, and authorize declared exchanges.

6. **Validation and Egress**
   - validate owner, scope, authorization, capability, artifact, completion,
     and receipt invariants;
   - implement source-policy result vocabulary without claiming semantic claim
     verification;
   - assemble TerminalPacket and receipt-backed diagnostics.

7. **Generic adapter conformance harness**
   - create provider-neutral tests for capability discovery, service exchange,
     host-session state evidence, pending-request correlation, receipts, host
     errors, and output delivery;
   - keep all concrete hosts out of the core.

8. **BC-020 Chat and Codex adapter specification, then implementations**
   - map each host's real capabilities, freshness, errors, receipts, time,
     scheduling, artifacts, tools, identity evidence, and limitations;
   - require the `SUR-012` host-evidence matrix to cover integrity and rollback
     resistance for host-provided authorization attempt state;
   - do not claim parity when a host cannot furnish equivalent evidence.

9. **Model execution integration and behavioral parity matrix**
   - load current Persona and Operations as model-facing authority;
   - test ordinary conversation, teaching, clarification, source modes, and
     service-request behavior without assigning capability truth to the model.

10. **BC-030 Local Mirror specification, then provider implementation**
    - define namespace, schema, lifecycle, provenance, versions, conflicts,
      retention, deletion, and receipts against the generic continuity
      interface;
    - make no persistence claim before provider tests pass.

11. **Optional behavior increments**
    - evaluate lightweight public mood/profile metadata, classroom state,
      curriculum/SkillForge context, and stronger source verification only
      after the core and adapters pass their matrices;
    - each increment must pass the component-minimality test.

## Dependency rules

- Steps 3 and 4 require separate security authorization.
- Step 5 requires steps 1 and 2 and a resolved minimal route catalog.
- Step 6 requires steps 1, 2, and 5.
- Concrete adapter implementation requires steps 1, 2, 6, and the BC-020 spec.
- Model integration requires the controller and egress interfaces but does not
  require continuity.
- Local Mirror implementation requires BC-030 and the generic continuity
  conformance tests; it is not a prerequisite for turn-local core parity.
- Optional profiles and classroom state are not on the critical path.

## BC-020 readiness

Result: `ready_for_spec`.

BC-020 now has a generic adapter target: `CapabilityReport`, `ServiceExchange`,
`PendingAuthorizationState` correlation, evidenced `host_session` state, and
`TerminalPacket` delivery; nine generic interfaces; explicit capability truth;
typed ordinary versus pre-ingress service authority; receipt and error
requirements; and a prohibition on host assumptions in the core. Its packet
should require a per-host capability/freshness matrix, host-session and pending-
request binding matrix, receipt matrix, identity-evidence matrix,
scheduling/time distinction, authorization attempt-state integrity and rollback
resistance, error mapping, and conformance fixtures.
`SUR-002`, `SUR-005`, `SUR-006`, and `SUR-012` are BC-020 inputs, not reasons to
postpone the specification.

BC-018 does not activate BC-020 and implements no adapter.

## BC-030 readiness

Result: `ready_for_spec`.

BC-030 now has a generic continuity target: versioned read/write,
namespace/scope, lifetime, provenance, expected-version conflict handling,
receipt, and unavailable behavior. Its packet should resolve `SUR-007` and
define Local Mirror schema, lifecycle, retention/deletion, migrations,
authorization, conflict semantics, receipts, and conformance fixtures.

BC-018 does not activate BC-030, choose storage details, or implement
persistence.
