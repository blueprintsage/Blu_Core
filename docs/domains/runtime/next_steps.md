# Runtime Next Steps

## Immediate — independent Codex re-review of BC-050

B-02 is resolved by the BC-050-C2A source-classification decision, and B-01 plus
B-03 through B-07 were corrected in BC-050-C2. All applicable validators pass
except the known BC-020 fixed-base host-adapter condition.

Codex should rerun all seven original reproductions and assess B-02 against the
amended premise rather than the withdrawn rule-destination requirement.

Still open and unchanged by C2A:

- editable-install verification (`pip install -e .`) blocked by a missing local
  build backend; external `PYTHONPATH=src` fallback in use;
- live LM Studio smoke test `not_performed`, including confirmation of the two
  B-04/B-07 field-name assumptions;
- the B-05 consequence that canonical public output strips punctuation, which may
  warrant a follow-on print-safe canonicalization decision;
- N-03 continuity defensive invariant, carried to the continuity-provider phase;
- the BC-020 fixed-base host-adapter guard.

Deliberately deferred: reducing or removing the live Custom GPT instruction
surface is a separate deployment task and was not performed.

## Immediate — Dad/Blu decision on B-02 authority contradictions

BC-050-C2 corrected six of Codex's seven blockers. B-02 is escalated as two
authority contradictions recorded in `assignments/BC-050/validation.md`:

- **C2-AC-01** Verb Lock and "structural scan is not reading".
- **C2-AC-02** Execution Law residue, the Compliance Gate checks, the
  Completion Proof enumeration, and the Truth Discipline placeholder rule.

Both stem from excluding `00_Instructions.md` from the model-facing envelope
while those rules live nowhere else. Three options are recorded for each;
whichever is chosen should cover both. Until one is chosen, BC-050 cannot claim
full One-Blu parity for Python Phase 1.

After that decision, Codex re-reviews BC-050 and should rerun all seven
original reproductions.

Also open: two LM Studio field-name assumptions from B-04/B-07 need live-smoke
confirmation, and B-05 now strips punctuation from ordinary replies, which may
warrant a follow-on print-safe canonicalization decision.

## Immediate — independent Codex review of BC-050

BC-050-C1 resolved contradiction C-1. All four suites and every applicable
validator pass except the known BC-020 fixed-base host-adapter finding.

BC-050 now goes to Codex for independent implementation review. Claude authored
the implementation and must not be its sole independent reviewer. Codex should
review packet compliance, architecture preservation, security and control flow,
OPSEC equivalence, provider non-invocation proofs, envelope and digest
construction, LM Studio evidence handling, continuity truth, readiness-validator
integrity, test adequacy, and scope discipline. Codex must not assume approval.

Outstanding environment item: editable-install verification
(`python -m pip install -e .`) has not been performed because the approved build
backend is unavailable locally. The authorized external `PYTHONPATH=src`
fallback works and the package-layout import test passes under it.

Still open, unrelated to BC-050: `tools/validate_host_adapter_contracts.py`
fails at the authorized base because its BC-020 fixed-base protected-path guard
predates BC-041's legitimate change to
`contracts/successor/unresolved_register.json`. Do not fold this into BC-050.
## BC-041 / BC-041-C1 closed gate

BC-041 and BC-041-C1 are `done`. Current `main` integrates the correction
lineage through `204a229e2c01b255f1a940129cb724fa33fb4755` at
`131a527a8fef1f42df327443c9966c9e2f66f528`. Claude's final independent review
at `f0998f78aaada899a16d4413170ef3689f04fe28` is `approve-with-notes` with zero
blocking findings. B-1 is resolved through C1; B-1' and B-1″ are resolved.

The final bounded state is:

```text
SUR-001: resolved_at_minimum_phase1_contract_level
Python technical readiness: ready_for_python_phase1
independent correction review: complete
Dad/Blu closure: complete
implementation authorized: false
automatic_start_prohibited: true
runtime_phase1_packet_may_be_authored_next: true
Python Runtime Phase 1: not started
```

Production policy values remain external; a missing or invalid policy fails
closed. The deterministic matcher does not claim arbitrary semantic-paraphrase
or general Unicode confusable/homoglyph coverage. Auth and protected
continuation remain unavailable, and SUR-002, SUR-011, and SUR-012 retain their
prior dispositions.

Claude N-1 and N-2 carry into the future Python Runtime Phase 1 packet as an
invariant-test requirement and a bounded/single-pass provenance-construction
requirement. N-3 records pre-existing `_` separator/word-character behavior and
requires no C1 repair. The next safe action is a separate Dad/Blu decision on
the `Python Runtime Phase 1 — Boot + Ordinary Turn + LM Studio Model Boundary`
packet. Do not begin implementation automatically.

## Prior BC-040 closed gate

BC-040 is `done`. The One-Blu portability/readiness specification and Claude's
independent review are complete. Claude's disposition is
`approve-with-notes`, with zero blocking findings in BC-040 itself.

At BC-040 closure the project was `not_ready_for_python_phase1` because SUR-001
was the sole actual blocker. BC-041 and BC-041-C1 subsequently resolved SUR-001
at the bounded minimum Phase 1 contract level and completed independent review
and closure. The current technical result is now `ready_for_python_phase1` with
no actual blockers.

Python Runtime Phase 1 remains separately unauthorized. Dad/Blu may next
consider the packet:

```text
Python Runtime Phase 1 — Boot + Ordinary Turn + LM Studio Model Boundary
```

Do not start it automatically. No closure implemented Python Blu, LM Studio
access, Local Mirror, Chat/Codex support, protected authorization, or
PASS/SkillForge.

## Closed lineage

BC-010, BC-010-C1, BC-010-C2, BC-015, BC-016, BC-017, BC-017-C1,
BC-018, BC-018-C1, BC-020, BC-020-C1, BC-030, BC-040, BC-041, and
BC-041-C1 are complete.

The runtime-contract extraction records the CTS source faithfully, including
unresolved declarations. It does not prove behavioral parity or implement a
Python runtime.

## Next safe step

Dad/Blu may separately author the `Python Runtime Phase 1 — Boot + Ordinary
Turn + LM Studio Model Boundary` packet. Authoring the packet is not
implementation authorization. Until a later explicit Dad/Blu action grants
that authority, `implementation_authorized` remains `false`, automatic start is
prohibited, and no runtime code may begin.

Carry the final BC-041-C1 review notes forward:

- N-1: add an invariant test so normalization changes cannot silently lose
  removed-`Cf` boundary provenance.
- N-2: compute production provenance offsets in a bounded/single-pass form; do
  not port the conformance harness's quadratic construction.
- N-3: retain as a record of pre-existing `_` separator/Unicode-word-character
  overlap, not as C1 rework.

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
