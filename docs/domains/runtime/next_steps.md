# Runtime Next Steps

status: active
owner: docs/domains/runtime
last_reviewed: 2026-08-12

## BC-041-C1 correction review gate

BC-041-C1 is in bounded handoff after correcting Claude's B-1' finding. The
minimum matcher now removes all general-category `Cf` code points into one
candidate and uses separator-tolerant rule matching to cover arbitrary mixtures
of boundary and inside-token insertion without placement enumeration. Its
bounded state is:

```text
SUR-001: resolved_at_minimum_phase1_contract_level
Python technical readiness: ready_for_python_phase1
independent correction review: required_pending
implementation authorized: false
runtime_phase1_packet_may_be_authored_next: true
```

Production policy values remain external; a missing or invalid policy fails
closed. The deterministic matcher does not claim arbitrary semantic-paraphrase
or general Unicode confusable/homoglyph coverage. Auth and protected
continuation remain unavailable, and SUR-002, SUR-011, and SUR-012 retain their
prior dispositions.

The expanded proof covers six code points across boundary, inside-token, and
mixed placement at ingress and egress, cross-code-point mixing, repeated
arbitrary insertions, the five negative fixtures, redaction rescan/fail-closed
paths, and content-safe evidence. The next safe step is a fresh Claude review
of the exact BC-041-C1 substantive/metadata head on a separate branch,
modifying only the C1 review record. Dad/Blu then decide integration, closure,
and whether to issue the separate `Python Runtime Phase 1 — Boot + Ordinary
Turn + LM Studio Model Boundary` packet. Do not begin that implementation
automatically.

## Prior BC-040 closed gate

BC-040 is `done`. The One-Blu portability/readiness specification and Claude's
independent review are complete. Claude's disposition is
`approve-with-notes`, with zero blocking findings in BC-040 itself.

The final project result remains `not_ready_for_python_phase1`. SUR-001 is the
sole actual blocker: arbitrary natural-language ingress and egress cannot
safely reach a local model until a separately authorized minimum deterministic
OPSEC match/redaction contract can distinguish safe ordinary text from a
protected-source reproduction request. SUR-002 blocks protected features only;
SUR-003 and SUR-010 are sufficiently resolved for the Phase 1 finite route
catalog; SUR-011 blocks protected continuation behavior only; and SUR-012
remains resolved only at the generic host-evidence-contract level.

The next separately authorized assignment is:

```text
Protected Security Phase 1 — Minimum OPSEC Match and Redaction Contract
```

Python Runtime Phase 1 remains unauthorized. Only after SUR-001 closes and the
readiness checklist is deterministically re-evaluated may Dad/Blu consider the
conditional coding packet:

```text
Python Runtime Phase 1 — Boot + Ordinary Turn + LM Studio Model Boundary
```

Do not start either assignment automatically. BC-040 closure does not implement
Python Blu, LM Studio access, Local Mirror, Chat/Codex support, protected
authorization, or PASS/SkillForge.

## Closed lineage

BC-010, BC-010-C1, BC-010-C2, BC-015, BC-016, BC-017, BC-017-C1,
BC-018, BC-018-C1, BC-020, BC-020-C1, BC-030, and BC-040 are complete.

The runtime-contract extraction records the CTS source faithfully, including
unresolved declarations. It does not prove behavioral parity or implement a
Python runtime.

## Next safe step

Open only the separately authorized `Protected Security Phase 1 — Minimum OPSEC
Match and Redaction Contract` packet. It must preserve protected-value secrecy,
may reopen `runtime_config.schema.json#runtime.protected_policy_ref` under its
own protected authority, and must close with deterministic readiness
re-evaluation. It must not be folded into BC-040 closure or Python coding.

Claude's ten nonblocking notes remain future inputs, not current blockers:

- Python Runtime Phase 1: classify every Phase 1 support path (N-1) and freeze
  the exact model-facing canon projection/envelope and digest rule (N-2).
- Future gap-model hardening: clarify `changes_current_behavior` (N-3).
- Continuity Provider Implementation: normalize receipt/provenance portability
  constraints (N-4) and add cross-object request/receipt mismatch coverage
  (N-5).
- Continuity vocabulary hardening: resolve `availability_probe` terminology
  (N-6).
- Review/checklist hardening: distinguish review required, pending, and complete
  without rewriting the completed review history (N-7).
- Protected Security Phase 1: amend the null-only protected-policy reference
  only under separate authority (N-8).
- Readiness hardening: add real Git fixtures for readiness scope/manifest guards
  (N-9) and distinguish dependency mismatch from contract failure (N-10).

The closed BC-018 lineage includes the successor boundary specification and
BC-018-C1 cross-turn security-state correction. Claude's original BC-018
`return-for-correction` review and the C1 `approve-with-notes` re-review remain
immutable history. Final closure has zero blocking findings.

BC-020 and BC-020-C1 are closed after Claude's original
`return-for-correction` review, the bounded BF-1 scheduling-evidence correction,
and Claude's final `approve-with-notes` C1 re-review with zero blockers. The
closure is administrative and changes no adapter semantics.

SUR-012 remains resolved at the generic host-evidence contract level: protected
cross-turn continuation requires provider-bound identity/state/request/result
scope, freshness/expiry, replay/consumption state, integrity, and monotonic
rollback-resistant attempt state. Insufficient evidence returns unavailable
rather than inventing safety.

This resolution does not claim current surface availability. Dad's live Chat
binding was not probed and remains unknown. The observed Codex desktop binding
is unavailable for protected cross-turn authorization continuation because the
adapter-visible interface lacks replay/consumption and rollback-resistant
attempt-state evidence.

BC-020-C1 corrected the review blocker without changing the generic architecture.
The observed Codex scheduling interface remains recorded, while
`schedule.create`, `schedule.recurring`, and `schedule.update_cancel` are
`unknown` pending operationally relevant provider evidence. Corrected Codex
totals are 52 capabilities: 24 verified available, 6 verified unavailable, 4
documented possible, 17 unknown, and 1 not applicable.

SUR-011 remains unresolved as a future security-authorized policy input for
protected attempt values, retry/lockout/backoff, cancellation/reset,
new-request-after-exhaustion, and unrelated intervening turns. BC-030 is
closed at the generic continuity-contract level: `host_session` remains
host-local and `durable_external` still requires an explicit
continuity-provider receipt. Provider implementation remains separately
unauthorized. Chat live probing is also a separate future assignment requiring
explicit authorization. Successor runtime implementation remains unauthorized.

The following non-blocking archaeology-quality notes remain preserved for
separately authorized hardening work:

- drilldown-list family semantics and cleanup;
- evidence-grade vocabulary consistency;
- inference-registration cleanup;
- wording around compensatory complexity;
- validator and review-state coupling;
- document-quality validation hardening;
- minor locator-scoping and consistency cleanup.

The evidence limitations preserved in the review records also remain in force,
including unreadable Deflate64 members, chronology gaps, lack of historical
runtime telemetry, and undefined current CTS Auth/OPSEC services.

### Legacy PASS exclusion

Historical PASS may be inspected only when necessary to establish chronology or
explain how old Exec orchestration compensated for unreliable components.

Legacy PASS must not be treated as a behavior-recovery candidate, recommended
for restoration, treated as an architectural precedent, used as the successor
PASS design, or allowed to displace or redefine the newer PASS specification.

Historical archaeology must not spend analysis effort evaluating whether old PASS should return.
The newer PASS is the relevant successor reference and remains separate from
historical archaeology.

Do not begin Chat live probing, continuity-provider implementation, Python
runtime implementation, or a successor control plane; restore historical
capabilities; or reopen the 28 current-source gaps without an approved packet
and named base.
