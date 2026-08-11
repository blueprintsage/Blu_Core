# BC-020-C1 — Scheduling Capability Evidence Correction

status: done
owner: Codex
reviewer: Claude
project_lead: Blu
project_owner: Dad
domain: runtime
parent: BC-020
last_reviewed: 2026-08-10

## Authorization and identity

Dad authorized this bounded correction in the assignment supplied to Codex on
2026-08-09. It corrects only BC-020 BF-1 and directly coupled scheduling and
evidence-validation defects identified by Claude. It does not authorize a host
adapter, runtime implementation, real scheduling operation, BC-030, Local
Mirror, or a redesign of BC-020 or BC-018.

- Exact base commit: `370278cd91fd9ecca2c64cd0953cae7ed63c4d16`
- Reviewed BC-020 target: `ccf3206ad033d588246e09001d47ddce3ac50a31`
- Starting branch: `bc-020-semantic-review`
- Work branch: `bc-020-c1-scheduling-evidence-correction`
- Global index row: `docs/worklogs/assignments.md` (`BC-020-C1`)
- Semantic reviewer: Claude

Claude's BC-020 review at the exact base is immutable correction input and must
not be rewritten.

## Objective

Downgrade the observed Codex `schedule.create`, `schedule.recurring`, and
`schedule.update_cancel` operational capabilities from `verified_available` to
`unknown`, preserve the observed scheduling-interface exposure, carry the
documented desktop-only future-execution limitation, and make the validator
reject verified claims supported only by interface exposure, unrelated strong
evidence, or evidence of the opposite property.

## Required source order

1. `AGENTS.md` and `CODEX.md`.
2. `docs/dev/docs_index.md` and `docs/dev/assistant_coding_behavior.md`.
3. `docs/worklogs/assignments.md` and this packet.
4. BC-020 assignment, handoff, validation, next steps, and Claude review.
5. Runtime domain index and continuity quartet.
6. Chat/Codex adapter contracts, capability matrices, evidence registers,
   validator, and tests.
7. Exact-base, ancestry, and clean-tree verification.

## Required correction

- Set the three operational Codex scheduling rows to `unknown`.
- Retain the current observation that an automation/scheduling interface is
  exposed, while stating that interface exposure does not prove provider or
  account connection, permission, usability, successful operations, future
  execution, or receipts.
- Preserve `schedule.receipt = unknown`, receipt-required semantics, the
  side-effect-success rule, and the availability/completion distinction.
- Carry only the documented desktop scheduling limitation that future local
  execution may depend on the relevant machine and app remaining available.
- Produce corrected Codex totals of 52 capabilities: 24
  `verified_available`, 6 `verified_unavailable`, 4 `documented_possible`, 17
  `unknown`, and 1 `not_applicable`.
- Require verified capability evidence to bear semantically on the capability
  by using the existing `supports[]` and `does_not_prove[]` boundaries. Do not
  introduce a generic semantic reasoning engine.

## Allowed collision domain

```text
docs/domains/runtime/assignments/BC-020-C1/**
docs/domains/runtime/adapters/host_capability_truth.md
docs/domains/runtime/adapters/codex_adapter.md
adapters/common/capability_contract.json
adapters/codex/capability_matrix.json
adapters/codex/evidence_register.json
tools/validate_host_adapter_contracts.py
tests/host_adapters/**
docs/dev/docs_index.md
docs/domains/runtime/worklog.md
docs/domains/runtime/failures.md
docs/domains/runtime/next_steps.md
docs/worklogs/assignments.md
MANIFEST.sha256
```

## Protected and prohibited areas

Do not modify Claude's BC-020 review, `kernel/golden/**`, current runtime
contracts, successor contracts or architecture, historical sources, modern
PASS/SkillForge material, Local Mirror, or current CTS behavior. Do not create
a real schedule for proof or implement a Chat/Codex adapter or Python runtime.
Preserve SUR-011, SUR-012, the seven successor components, eight packets, nine
interfaces, receipt semantics, and all BC-020 findings that survived review.

## Required tests

Focused tests must prove:

1. Each of the three operational scheduling claims fails when promoted from
   interface exposure alone.
2. The corrected `unknown` scheduling rows pass.
3. An unrelated current-time receipt cannot verify `action.git.push`.
4. Web-search evidence cannot verify raw network.
5. Negative attempt-integrity evidence cannot establish positive integrity.
6. Existing valid verified rows still pass.
7. Chat documentary-only evidence remains insufficient for
   `verified_available`.
8. Current-time and side-effect receipt requirements remain intact.

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
python tools/validate_host_adapter_contracts.py
python -m unittest discover -s tests/host_adapters -p "test_*.py"
```

Also verify all eight golden checksums, the canonical manifest, exact-base
protected-path integrity, unchanged successor architecture, no adapter/runtime
implementation, and Claude's original review unchanged.

## Completion conditions

Leave BC-020-C1 at `review` after one substantive correction commit, one
metadata-only commit recording the substantive SHA, a normal branch push, clean
status, complete records, and passing validation. Do not merge, close BC-020,
start BC-030, or begin runtime implementation.

## Approved amendments

### 2026-08-10 — Final closure authorization

Dad, Project Owner, and Blu, Project Lead, authorized administrative closure
from exact integrated `main` base
`642a5df7340c4f87ac723bffb4d308fef09bf2b2` on branch
`bc-020-closure`.

- Final status: `done`.
- Work branch: `bc-020-c1-scheduling-evidence-correction`.
- Substantive correction:
  `b770be849d625e924f7e65cae4efb8894a7e4c23`.
- Correction metadata:
  `8eb29165d5d59b99ccaa3b06fe6d8613dcaa11e2`.
- Claude C1 re-review:
  `b51912a655d3f895651eb0bdbbe0c41ba1e7f132`;
  disposition `approve-with-notes`; BF-1 resolved; zero blocking findings.
- Closure preserves all nonblocking review findings as history and creates no
  new closure requirement from them.
- Closure is administrative only. It changes no adapter semantics, authorizes
  no runtime implementation, and does not start BC-030 or Chat live probing.
