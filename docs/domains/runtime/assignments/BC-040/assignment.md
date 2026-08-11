# BC-040 — One-Blu Portability and Python Runtime Readiness

status: done
owner: Codex
reviewer: Claude
project_lead: Blu
project_owner: Dad
domain: runtime
last_reviewed: 2026-08-11

## Authorization and identity

Dad, Project Owner, and Blu, Project Lead, authorized this final
implementation-readiness specification assignment in the packet supplied to
Codex on 2026-08-11.

- Exact base commit: `66e7ed52f5777bdef2e32c71a5e83b439b0d0ade`
- Starting branch: `main`
- Work branch: `bc-040-one-blu-readiness`
- Owner: Codex
- Independent semantic reviewer: Claude
- Assignment class: successor specification and validation hardening
- Production runtime implementation authorized: no

BC-040 may tighten contracts, schemas, validators, fixtures, deployment and
readiness specifications, and the next implementation-slice definition. It may
not implement Python Blu, an LM Studio client, a Local Mirror provider, Codex
Blu, tools, a daemon, a UI, a runtime CLI, or protected policy values.

## Objective

Freeze the minimum canon, portability, security posture, provider boundary,
source rules, implementation-gap mapping, Python layout, and executable-slice
definition needed to decide whether Python Runtime Phase 1 can be authorized
without forcing implementers to make architectural decisions while coding.

The target architecture is one Blu, one canonical behavioral source, and two
required deployment environments: ChatGPT Custom GPT and Python Blu using a
locally served model through LM Studio. Codex is optional best effort and may
not drive the architecture.

## Required source and startup checks

Before editing, verify the exact base and a clean tree; confirm BC-020,
BC-020-C1, and BC-030 are done; confirm no Python successor runtime or LM Studio
adapter exists; then read governance, documentation indexes, runtime and
continuity domain continuity, BC-030 review N1-N8, the successor 7/8/9
architecture, current gap registers, host contracts, and current official LM
Studio developer documentation.

If `main` moved beyond the named base, stop rather than rebasing. Do not change
the base without new Dad/Blu authority.

## Governing invariants

- The immutable current runtime remains `kernel/golden/v0.22.0/**`.
- Current CTS behavior is not rewritten retroactively.
- Preserve behavior and law while reconsidering the component graph.
- Successor counts remain exactly seven components, eight packets, and nine
  interfaces.
- There is no Portability Manager, LM Studio component, Canon Manager, Session
  Manager, Memory Manager, mega-Exec, Exec Library, School Engine, Mood
  service, MMU service, or restored legacy PASS.
- Persona, Operations Law, identity, security semantics, continuity truth,
  validation truth, and source authority cannot fork by host.
- `host_session != durable_external`.
- LM Studio is only a Model Execution provider. Local Mirror is only a
  Continuity Provider candidate. They are not coupled.
- Model tool-call output is a candidate, not authorization, approval, attempt,
  completion, or receipt.

## Required outcomes

Create machine- and human-readable contracts for:

1. One-Blu canon and deployment mapping, including drift detection and the
   deterministic/semantic-review boundary.
2. Required ChatGPT and Python/LM Studio targets and optional Codex.
3. Provider-neutral Model Execution semantics backed by exact official LM
   Studio evidence.
4. Portable configuration and a future `src/` package layout.
5. A finite first executable slice centered on one ordinary conversation turn,
   with LM Studio as the initial provider and no tool execution or streaming.
6. Explicit Phase 1 dispositions for every successor implementation blocker.
7. Explicit implementation-gap dispositions for all 28 current-source gaps,
   resolving SUR-010 sufficiently for the first slice.
8. Custom GPT/Python behavioral parity dimensions and scenario fixtures.
9. A machine-readable Phase 1 authorization checklist that distinguishes
   `ready_for_python_phase1` from full successor feature completeness.

## BC-030 required tightening

- N1: add `ContinuityMutationRequest` with caller-owned expected-version
  binding.
- N2: prevent `not_found` records and completed receipts on non-completed
  retrievals.
- N3: define `availability_probe` as receipt-only observation with no record
  transition.
- N4: mechanically enforce `requested_action == operation`.
- N5: reject portable-field drive-letter, UNC, file-URI, and POSIX absolute
  paths while preserving legitimate opaque provider references.
- N6: prohibit successful version/supersession outcomes on non-completed
  receipts.
- N7: regression-test Git scope, protected paths, disallowed Python,
  PASS/SkillForge bleed, LM Studio code bleed, and manifest coverage with real
  Git fixtures.
- N8: recompute manifest digests using canonical Git blob/line-ending rules.

Select and pin the Python JSON Schema runtime. Exercise valid and invalid
instances for all five BC-030 schemas plus the new mutation request schema,
including conditionals for completed/failed/conflict results, action binding,
expected versions, `not_found`, availability, paths, supersession, and
non-completed outcomes.

## Security gate

Inspect every successor item marked `blocking_for_implementation: true`, at
minimum SUR-001, SUR-002, SUR-003, SUR-010, SUR-011, and SUR-012. Do not clear a
blocker merely to reach coding. Protected values may not be published or
reconstructed.

Ordinary behavior may proceed only if protected operations and protected
source disclosure can fail closed without missing policy. If a real ordinary
turn cannot be proven safe without SUR-001, the correct BC-040 result is
`not_ready_for_python_phase1` with only the actual blocker recorded.

## Allowed collision domain

```text
readiness/**
requirements-contracts.txt
continuity/**
tools/validate_continuity_contracts.py
tests/continuity/**
tools/validate_python_readiness.py
tests/readiness/**
docs/domains/runtime/assignments/BC-040/**
docs/domains/runtime/one_blu_python_readiness.md
docs/domains/runtime/{decisions,worklog,failures,next_steps}.md
docs/domains/continuity/{decisions,worklog,failures,next_steps}.md
docs/worklogs/assignments.md
docs/dev/docs_index.md
MANIFEST.sha256
```

The active successor unresolved register may receive additive BC-040
disposition metadata if needed, but architecture counts, packet/interface
registries, current CTS contracts, adapters, source authority, and golden files
remain protected.

## Protected and prohibited areas

Do not modify `kernel/golden/v0.22.0/**`, current CTS semantics, Persona,
Operations Law, source precedence, historical review records, or modern
PASS/SkillForge. Do not implement production files under the future runtime
source root. Do not add LM Studio, Local Mirror, Chat, or Codex runtime code.
Do not claim protected authorization, persistence, model capability, inference
completion, host parity, or provider availability without qualifying evidence.

## Required validation

Run the seven existing validator/test pairs, the focused BC-040 validator and
tests, `git diff --check`, canonical manifest coverage/digests, all eight golden
checksums, exact-base protected-path checks, 7/8/9 counts, no-runtime/provider
checks, and PASS/SkillForge isolation. Record actual failures and limitations.

## Completion and commits

End in exactly one of `ready_for_python_phase1` or
`not_ready_for_python_phase1`. If ready, name the exact runtime implementation
packet that may be authored next. If not ready, enumerate only actual blockers.

Use two commits:

1. `spec(BC-040): define One-Blu Python readiness`
2. `docs(BC-040): record readiness specification commit`

The first contains substantive specifications, schemas, validators, fixtures,
records, and manifest changes. The second records the exact first SHA. Push the
branch, move status to `review`, and stop for Claude's independent semantic
review. Do not begin Python Runtime Phase 1 automatically.

## Final closure amendment — 2026-08-11

Dad, Project Owner, and Blu, Project Lead, authorized administrative final
closure after the specification and Claude review were integrated. This
amendment records closure receipts; it does not change the original assignment
scope or authorize implementation.

- Original authorized base:
  `66e7ed52f5777bdef2e32c71a5e83b439b0d0ade`
- Substantive specification:
  `8516bd6845edaa3ef9b18077d91853ccc21e3c3b`
- Metadata/review head:
  `dc5429cabf03aff4ea8b383cbc1290789c370ebb`
- BC-040 work integration:
  `a24cffc2fb3b3b7ffe3e0291915d0319a4db3e5f`
- Claude semantic review:
  `127ae61e296fe0d07072e1320dec8ca8c4b1dfed`
- Claude disposition: `approve-with-notes`
- Claude blocking findings: `0`
- Final reviewed/integrated base:
  `8801ae138deb0261deff47d02269c7a16773c892`
- Closure branch: `bc-040-closure`
- Closure substantive commit:
  `d78f58972327434c83d7e79a2cb9372e487a9629`
- Final assignment status: `done`
- Final BC-040 readiness result: `not_ready_for_python_phase1`

`BC-040 done` does not mean `Python Phase 1 ready`. BC-040 completed its
readiness-specification job by establishing that SUR-001 is the sole actual
Phase 1 blocker. The minimum OPSEC match/redaction condition remains failed,
`runtime_phase1_packet_may_be_authored_next` remains `false`, and Python Runtime
Phase 1 remains unauthorized until separately authorized SUR-001 work closes
and the checklist is deterministically re-evaluated.
