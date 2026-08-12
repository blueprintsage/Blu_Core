# BC-041 — Protected Security Phase 1

status: done
owner: Codex
reviewer: Claude
project_lead: Blu
project_owner: Dad
domain: runtime
last_reviewed: 2026-08-12

## Assignment identity

- Exact base commit: `699ee1485cef39ffbe70c3b8e848763af02596e0`
- Starting branch: `main`
- Work branch: `bc-041-protected-opsec-phase1`
- Global index row: `docs/worklogs/assignments.md#BC-041`
- Assignment class: security contract and Python Phase 1 readiness
- Production runtime implementation authorized: no

Dad and Blu authorized this packet in the assignment supplied to Codex on
2026-08-11. The source packet remains the governing authorization; this record
captures its repository-native scope and acceptance gates.

## Objective

Resolve SUR-001 only at the minimum Phase 1 contract level by defining a public,
deterministic, secret-safe OPSEC match, policy-loading, ingress, egress,
redaction, evidence, and diagnostic contract. Re-evaluate Python Phase 1
readiness without implementing the runtime.

## Required source order

Read `AGENTS.md`, `CODEX.md`, repository and source-authority indexes, BC-040's
assignment/handoff/validation/review and closure records, the successor
security-restraint contracts, SUR-001 evidence sources, the runtime continuity
quartet, and this packet. Verify a clean tree and exact base before editing.

## Authoritative inputs

- Dad/Blu's supplied BC-041 authorization packet.
- `kernel/golden/v0.22.0/00_Instructions.md`,
  `02_Operations_Law.md`, and `03_Exec.md` for recovered current law.
- `docs/domains/runtime/decisions.md` for the approved successor OPSEC/Auth
  boundary.
- `docs/architecture/successor_{kernel,boundaries,component_graph,migration_sequence}.md`.
- `contracts/successor/{component,packet,interface,error_model,behavior_placement,traceability,unresolved_register}.json`.
- `docs/domains/runtime/assignments/BC-040/**` and `readiness/**`.
- `contracts/runtime/{route_registry,unresolved_register}.json` and BC-017/BC-015
  evidence referenced by SUR-001.

## Allowed collision domain

```text
contracts/security/opsec/**
tests/security/**
tools/validate_opsec_contracts.py
readiness/**
tools/validate_python_readiness.py
tests/readiness/**
tools/validate_continuity_contracts.py
tests/continuity/test_validate_continuity_contracts.py
contracts/successor/unresolved_register.json
docs/domains/runtime/assignments/BC-041/**
docs/domains/runtime/one_blu_python_readiness.md
docs/domains/runtime/{decisions,worklog,failures,next_steps}.md
docs/worklogs/assignments.md
docs/dev/docs_index.md
MANIFEST.sha256
```

No unrelated domain may be changed.

## Protected and prohibited areas

Do not modify the golden CTS, Persona, Operations Law, source precedence,
existing review records, architecture counts/ownership, adapters, continuity,
Auth policy, SUR-011 policy, or PASS/SkillForge. Do not commit production
protected values, machine-local policy paths/digests, credentials, challenge
answers, raw protected text, or reversible fingerprints. Do not add production
runtime, LM Studio, Local Mirror, tool, daemon, UI, or CLI code.

## Required deliverables

1. Public minimum OPSEC mechanism and human-readable boundary.
2. Protected-policy and safe-evaluation schemas.
3. Portable opaque protected-policy reference and fail-closed load stages.
4. Deterministic normalization, phrase matching, ingress mapping, and egress
   block/redaction mapping.
5. Content-safe evidence, receipts, logs, diagnostics, and error codes.
6. Explicitly synthetic policy/case fixtures and a nonproduction reference
   validator/harness.
7. Tests for policy loading, trivial normalization bypasses, false positives,
   ingress/egress, redaction, non-disclosure, and architecture boundaries.
8. Bounded SUR-001 disposition and deterministic readiness re-evaluation.
9. Assignment records, runtime continuity, documentation index, and canonical
   manifest updates.

## Required invariants

- OPSEC remains mandatory pre-ingress and separate from Auth and routing.
- `SecurityDecision` remains exactly `PASS`, `BLOCK`, `ASK`; only `PASS` reaches
  Turn Controller.
- Policy missing/invalid/unreadable/integrity-mismatched is terminal
  `UNAVAILABLE`, never `PASS`, and never reaches the model.
- Candidate output is checked before print; protected output is safely redacted
  only when policy-authorized and postvalidated, otherwise fully blocked.
- No protected value appears in public output, logs, receipts, diagnostics,
  fixtures claimed as production, or Git metadata.
- Architecture remains 7 components, 8 packets, and 9 interfaces.
- SUR-002, SUR-011, and SUR-012 retain their BC-040 semantic dispositions.

## Required checks

Run the focused OPSEC validator/tests, every existing validator/test pair named
in the supplied packet, `git diff --check`, all eight golden checksums,
architecture counts, manifest completeness/digests using canonical Git blobs,
protected-path and production-code exclusions, synthetic/publication scans, and
the known host-adapter validator without suppressing its historical finding.

## Completion conditions

Move to `review` only if the public mechanism, schemas, portable reference,
ingress/egress mappings, fail-closed behavior, synthetic proof, protected-value
separation, and implementation sufficiency all pass. Then record:

```text
BC-041 result: ready_for_review
SUR-001: resolved_at_minimum_phase1_contract_level
Python readiness: ready_for_python_phase1
runtime_phase1_packet_may_be_authored_next: true
```

This permits Dad/Blu to consider authoring the named runtime packet. It does not
authorize Codex to start Python Runtime Phase 1.

Use two commits: substantive work, then a metadata-only receipt that records
the substantive SHA. Push the branch, do not merge, and stop for Claude's
independent semantic review.

## Approved amendments

No amendments.

## Final closure amendment — 2026-08-12

Dad and Blu authorized final integration and administrative closure of BC-041
together with BC-041-C1. This amendment records the final disposition without
rewriting the immutable original BC-041 `return-for-correction` review.

- Original substantive work:
  `9ccd17d75955db4b64e5df27a5751d36b6964330`
- Original metadata:
  `9849c60138940068a0fd900eb49ce7444531109d`
- Original Claude review:
  `ade01082a7bf4ebe389af6deafc68ea207d989d9`
- Original disposition: `return-for-correction`
- Governing correction tip:
  `204a229e2c01b255f1a940129cb724fa33fb4755`
- Correction integration on current `main`:
  `131a527a8fef1f42df327443c9966c9e2f66f528`
- Final Claude correction review:
  `f0998f78aaada899a16d4413170ef3689f04fe28`
- Final disposition: `approve-with-notes`
- Blocking findings: `0`
- Final assignment status: `done`

B-1 is resolved through BC-041-C1. SUR-001 is
`resolved_at_minimum_phase1_contract_level`; technical readiness is
`ready_for_python_phase1`; actual blockers are empty; and the runtime Phase 1
packet may be authored next. Python Runtime Phase 1 implementation is not
started or authorized, and automatic start remains prohibited.
