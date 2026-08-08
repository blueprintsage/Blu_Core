# BC-018-C1 — Cross-Turn Security State Correction

status: done
owner: Codex
reviewer: Claude
project_lead: Blu
project_owner: Dad
domain: runtime
parent: BC-018
last_reviewed: 2026-08-08

## Authorization and identity

Dad and Blu authorized this correction on 2026-08-08.

- Exact base and triggering review: `7796c7e738e0ff66b677c79314b80cf2bbb09a63`
- Work branch: `bc-018-c1-security-state-correction`
- Implementation owner / Git steward: Codex
- Semantic reviewer: Claude
- Blocking findings: `BF-1`, `BF-2`, `BF-3`
- Global index: `docs/worklogs/assignments.md`

## Objective

Correct only the cross-turn Auth/OPSEC state defects identified in the BC-018
semantic review. Define an evidenced, bounded cross-turn authorization model
without changing the seven-component boundary set, adding a top-level packet,
implementing a runtime, or exposing protected policy values.

## Required source order

1. `AGENTS.md` and `CODEX.md`.
2. `docs/dev/docs_index.md` and `docs/dev/assistant_coding_behavior.md`.
3. `docs/worklogs/assignments.md` and this packet.
4. Runtime domain index and continuity quartet.
5. BC-018 assignment, handoff, validation, and review.
6. Successor architecture and machine-readable contracts.
7. Exact-base and clean-tree verification before editing.

## Authorized correction

- Make the pre-ingress authorization flow explicitly cross-turn with exactly
  one `TerminalPacket` per host turn.
- Replace bare `session` persistence claims with `none`, `turn`, evidenced
  `host_session`, or receipted `durable_external` lifetimes.
- Extend the Generic Host Adapter Boundary with an evidenced host-session state
  contract; do not add a component.
- Define `PendingAuthorizationState` as a state record, not a packet.
- Make Security Restraint the sole semantic owner of authorization-attempt
  permission, Auth the evidence/result evaluator, and Host Adapter the
  host-session substrate/correlation provider.
- Require finite attempts, expiry, binding, replay protection, and fail-closed
  exhaustion without publishing protected values.
- Bind `AuthorizationResult` validity to evidenced lifetime and scope.
- Keep Turn Controller turn-local; accept optional cross-turn context only as
  evidenced current-turn input.
- Resolve directly related review notes N1, N5, and N8 only.
- Preserve the original BC-018 review unchanged.

## Allowed collision domain

```text
docs/domains/runtime/assignments/BC-018-C1/**
docs/architecture/successor_*.md
contracts/successor/**
tools/validate_successor_kernel_spec.py
tests/successor_kernel/**
docs/domains/runtime/decisions.md
docs/domains/runtime/worklog.md
docs/domains/runtime/failures.md
docs/domains/runtime/next_steps.md
docs/worklogs/assignments.md
docs/dev/docs_index.md
MANIFEST.sha256
```

## Protected and prohibited areas

Do not modify `kernel/golden/v0.22.0/**`, `contracts/runtime/**`,
`docs/sources/historical_archives/**`, the BC-018 review, modern
PASS/SkillForge, or current Persona/Operations Law. Do not add runtime Python,
security/Auth/session-storage implementations, host adapters, Local Mirror,
scheduling, Time, persistence, PASS, or SkillForge. Do not expose protected
challenge material, values, thresholds, or answers.

## Required deliverables

- Consistent successor contracts and architecture for BF-1/BF-2/BF-3.
- Machine-checkable `ServiceExchange` authority classes.
- Traceability for the revised state-lifetime rule.
- Explicit unresolved security-policy details.
- At least ten focused negative tests named in the authorization.
- Standard C1 handoff, validation, review placeholder, continuity, index, and
  manifest records.

## Required checks

```text
git diff --check
python tools/validate_runtime_contracts.py
python -m unittest discover -s tests/contracts -p "test_*.py"
python tools/validate_viability_audit.py
python -m unittest discover -s tests/viability -p "test_*.py"
python tools/validate_historical_archive_inventory.py
python -m unittest discover -s tests/historical_archives -p "test_*.py"
python tools/validate_historical_behavioral_archaeology.py
python -m unittest discover -s tests/historical_archaeology -p "test_*.py"
python tools/validate_successor_kernel_spec.py
python -m unittest discover -s tests/successor_kernel -p "test_*.py"
```

Also verify the canonical manifest, golden CTS checksums, protected paths,
component and packet counts, absence of runtime implementation, protected
policy publication safety, and modern PASS/SkillForge isolation.

## Completion conditions

Create one substantive commit and one metadata-only receipt commit, push the
branch, and leave BC-018-C1 at `review`, not `done`. Do not merge or start the
Claude re-review, BC-020, BC-030, or runtime implementation.

## Approved amendments

### 2026-08-08 — Pre-review terminal-authority correction

Authorized by Dad through direct instruction on existing branch
`bc-018-c1-security-state-correction` at exact head
`b1e0f5c7ce3fddd7d71f6b2fa8050b0b55875b3c`.

This amendment corrects only the provider-caused pre-ingress `UNAVAILABLE`
terminal path before any `ControlDecision` exists:

- keep `SecurityDecision` status vocabulary exactly `PASS`, `BLOCK`, `ASK`;
- attempt evidenced host-session binding before publicly emitting a resumable
  authorization `ASK`;
- on successful binding, activate the pending interaction and emit exactly one
  `ASK` `TerminalPacket` under the originating `SecurityDecision`;
- on unavailable binding, leave the proposed pending interaction inactive and
  non-resumable, prohibit future correlation to its request reference, and emit
  exactly one safe `UNAVAILABLE` `TerminalPacket` under the originating
  `SecurityDecision` with owner `security_restraint`;
- require no `ControlDecision`, ordinary routing, component, packet, runtime,
  or protected status/policy expansion;
- add four focused negative tests while preserving all existing tests;
- append one narrow substantive commit and one metadata-only receipt commit,
  then push without merging or starting re-review.

### 2026-08-08 — Closure-prep integrity and consistency correction

Authorized by Dad through direct instruction at Claude's exact review commit
`1f440546a076c9359afaf5e832882e588d71dfa6` on branch
`bc-018-c1-closure-prep`.

This amendment authorizes only the pre-closure corrections identified as
NN-1 through NN-5 in Claude's immutable `approve-with-notes` review:

- regenerate the canonical self-excluding manifest from complete tracked
  Git-blob/LF-normalized coverage and add a narrow completeness guard;
- make the Turn N+1 component graph show Security Restraint attempt permission
  before Authorization Evaluator evaluation;
- set SUR-012 `blocking_for_BC020` to `true` without changing SUR-002;
- carry NN-4 into SUR-011 security-policy work and NN-5 into the BC-020/SUR-012
  host-evidence matrix without resolving either question;
- preserve the seven components, eight packets, nine interfaces,
  `SecurityDecision` statuses, current CTS, runtime boundary, BC-020/BC-030
  authorization state, modern PASS/SkillForge sources, and Claude's review;
- create one substantive correction commit and the normal metadata-only receipt
  commit, push the branch, and leave BC-018 and BC-018-C1 at `review`.

### 2026-08-08 — Final closure authorization

Dad and Blu authorized administrative closure from exact integrated main base
`ce1cc235057a5de3d71fefbcee32e5617197cbb0` on branch
`bc-018-closure`.

- Final status: `done`.
- Final semantic disposition: `approve-with-notes`.
- Final blocking findings: zero.
- Claude re-review commit:
  `1f440546a076c9359afaf5e832882e588d71dfa6`.
- Closure preserves the seven-component, eight-packet, nine-interface design;
  `PendingAuthorizationState` remains a state record and
  `SecurityDecision` remains `PASS`, `BLOCK`, or `ASK`.
- SUR-011 remains unresolved for future security-authorized policy work.
  SUR-012 remains `blocking_for_BC020: true` for the future BC-020 host-evidence
  matrix.
- Closure is administrative only and authorizes no runtime implementation,
  BC-020 work, or BC-030 work.
