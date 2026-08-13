# BC-050 — Handoff Record

status: blocked_on_contradiction
owner: Claude
reviewer: Codex
project_lead: Blu
project_owner: Dad
domain: runtime
last_reviewed: 2026-08-12

## Result

Python Runtime Phase 1 is implemented and its deterministic suite passes in
full. One genuine contract contradiction blocks the readiness-state transition
and therefore blocks BC-050 from moving to `review`. Per the packet's §21
deviation protocol it is recorded here rather than solved by editing a
protected contract or expanding scope.

## Identity

- Exact base commit: `973589eea05fe42deeb829c5435bd09faf8cbe70`
- Base verification: `origin/main` equals the authorized base exactly; zero
  intervening commits; no overlap to report.
- Branch: `bc-050-python-runtime-phase1`
- Implementation owner: Claude (BC-050 only, by explicit Dad/Blu authorization)
- Independent implementation reviewer: Codex
- Live LM Studio smoke test: `not_performed` (no live environment supplied)

## BLOCKING CONTRADICTION — C-1

**Frozen requirements cannot all hold.** The "no runtime implementation"
assertion is duplicated across **three** validators. BC-050's collision domain
covers only the first.

| Validator | Assertion | In collision domain? |
| --- | --- | --- |
| `tools/validate_python_readiness.py` | `src` tree, `.py` scope, `implementation_present`, `implementation_authorized` | yes — amended and gated |
| `tools/validate_opsec_contracts.py:652-655` | `implementation_authorized is False` (checklist and slice) | **no — explicitly protected** |
| `tools/validate_continuity_contracts.py:91-94,217-222` | `PROHIBITED_IMPLEMENTATION_ROOTS` includes `src` | **no** |

### C-1a — protected OPSEC validator

`tools/validate_opsec_contracts.py` lines 652-655:

```python
if checklist.get("implementation_authorized") is not False:
    errors.append("readiness checklist authorizes implementation without separate runtime authorization")
if checklist.get("automatic_start_prohibited") is not True or phase1.get("implementation_authorized") is not False:
    errors.append("BC-041 improperly starts or authorizes runtime implementation")
```

This hard-requires `python_phase1_readiness_checklist.implementation_authorized`
and `phase1_executable_slice.implementation_authorized` to be exactly `false`.

Against that:

- BC-050 §15 requires both to become `true` once Dad/Blu explicitly authorize
  implementation, and requires the readiness state to be truthful.
- BC-050 "Protected and prohibited areas" forbids modifying
  `tools/validate_opsec_contracts.py`, which must stay byte-identical because
  it is the C1 conformance oracle and the differential-test oracle.
- BC-050 completion criterion 21 requires existing repository validators to
  still pass.

All four cannot be satisfied simultaneously. Dad/Blu must resolve this.

### C-1b — continuity validator

`tools/validate_continuity_contracts.py` lines 91-94 define
`PROHIBITED_IMPLEMENTATION_ROOTS` including `Path("src")`, and lines 217-222
reject any `src` tree containing files. It is not in the BC-050 collision
domain and needs the same authorization gate the readiness validator now has.

### Observed failures traced to C-1

C-1a — one root cause, three failing assertions across two suites:

```text
python tools/validate_opsec_contracts.py
  ERROR: readiness checklist authorizes implementation without separate runtime authorization
  ERROR: BC-041 improperly starts or authorizes runtime implementation

python tools/validate_python_readiness.py
  ERROR: expanded OPSEC proof failed: readiness checklist authorizes implementation ...
  ERROR: expanded OPSEC proof failed: BC-041 improperly starts or authorizes runtime implementation

python -m unittest discover -s tests/security  -> 36 tests, 1 failure (same cause)
python -m unittest discover -s tests/readiness -> 18 tests, 2 failures (same cause)
```

C-1b:

```text
python tools/validate_continuity_contracts.py
  ERROR: runtime or provider implementation exists: src
```

`tests/runtime_phase1` (119 tests) and `tests/continuity` (42 tests) pass.

### Separately: one pre-existing failure, not caused by BC-050

```text
python tools/validate_host_adapter_contracts.py
  ERROR: protected path changed from BC-020 base: contracts/successor/unresolved_register.json
```

This fails identically at the authorized base commit with no BC-050 changes
present. `contracts/successor/unresolved_register.json` was last modified by
BC-041 (`9ccd17d`), which post-dates the BC-020 base the guard compares
against, so the guard is stale. BC-050 did not modify that file
(`git diff base -- contracts/successor/unresolved_register.json` is empty). I
did not repair it: it is outside the collision domain and outside this
assignment. Recorded for a future narrow hardening pass.

### Why the tree was left in the failing state

Reverting the readiness files to `implementation_authorized: false` would make
both validators pass, but the repository would then assert that no authorized
runtime implementation exists while authorized runtime implementation is
present in the same commit. Operations Law's Runtime Truth Doctrine and
`00_Instructions.md` Truth Discipline both forbid that record. The truthful
state with a validator that visibly disagrees is the honest posture; the
validator failure names the contradiction instead of hiding it.

### Assessment for Dad/Blu

The two offending assertions are not part of the conformance oracle. They sit
in a readiness/scope-proof function appended to the OPSEC validator, and they
do not touch `normalized_match_candidate`, the matcher, or policy loading —
the surfaces the differential tests bind to. A minimal amendment limited to
those two assertions would not weaken C1 evidence or invalidate any
differential test.

I did not make that change. The packet is explicit that
`tools/validate_opsec_contracts.py` is protected, and §21 directs me to record
a contradiction rather than resolve it by editing a protected contract.

Options for Dad/Blu, in order of my recommendation:

1. Amend BC-050 to add `tools/validate_opsec_contracts.py` and
   `tools/validate_continuity_contracts.py` to the collision domain for changes
   limited to the assertions listed above, gated exactly the way the readiness
   validator now is, with the OPSEC oracle functions unchanged and the
   differential tests re-run to confirm the oracle still behaves identically.
2. Move the authorization and implementation-tree assertions out of both
   validators into the readiness validator, where the BC-050 gate already
   lives, so the rule has one home instead of three.
3. Direct me to revert the readiness transition and record BC-050 as
   implemented-but-unrecorded. I do not recommend this; it makes the
   repository state untruthful.

Whichever path is chosen, the underlying lesson is that the "no runtime
implementation" rule was encoded in three places, so authorizing the first real
implementation was always going to require touching all three.

### Reviewer note on my own pre-flight review

My pre-flight B-1 identified this exact class of defect in
`tools/validate_python_readiness.py` and asserted that extending the collision
domain to that file plus its test would be sufficient. It was not. The same
assertion is duplicated in `tools/validate_opsec_contracts.py`, and I did not
check for the duplicate. Amendment A closed B-1 as scoped, so the gap reached
implementation.

## Completed work

Every packet requirement other than the blocked readiness transition is
implemented and evidenced. See `validation.md` for exact commands and results.

Production files created (13 modules plus 8 package initializers):

```text
src/blu_runtime/__init__.py
src/blu_runtime/__main__.py
src/blu_runtime/config.py
src/blu_runtime/canon/{__init__.py,loader.py}
src/blu_runtime/contracts/{__init__.py,models.py}
src/blu_runtime/core/{__init__.py,security_restraint.py,turn_controller.py,validation_egress.py}
src/blu_runtime/providers/{__init__.py}
src/blu_runtime/providers/model/{__init__.py,base.py,lm_studio.py}
src/blu_runtime/providers/continuity/{__init__.py,base.py}
src/blu_runtime/adapters/{__init__.py}
src/blu_runtime/adapters/host/{__init__.py,base.py,terminal.py}
```

Tests created:

```text
tests/runtime_phase1/{__init__.py,support.py}
tests/runtime_phase1/test_security_restraint.py
tests/runtime_phase1/test_canon_envelope.py
tests/runtime_phase1/test_config_and_routing.py
tests/runtime_phase1/test_lm_studio_provider.py
tests/runtime_phase1/test_end_to_end.py
```

Readiness, validator, packaging, and manifest changes:

```text
readiness/python_package_layout.json
readiness/phase1_executable_slice.json
readiness/python_phase1_readiness_checklist.json
tools/validate_python_readiness.py
pyproject.toml
.gitignore
MANIFEST.sha256
```

`src/blu_runtime/core/authorization.py` is deliberately absent: the layout
marks it `phase1: false`, and the packet forbids inventing authentication
behavior to make the component look implemented.

## Deviations from packet

**D-1 — `tests/runtime_phase1/fixtures/` was not created.** The layout lists it
as a Phase-1 path. Runtime tests reuse the already-approved synthetic policy at
`tests/security/fixtures/synthetic_policy.json` rather than duplicating
protected-policy-shaped fixtures into a second location. Duplicating them would
add a second synthetic-policy surface for no behavioral gain. Flagged for
reviewer judgment; trivially reversible.

**D-2 — build backend absent.** `setuptools` is not installed in this
environment, so `python -m pip install -e .` was not run. Per §16 the documented
`PYTHONPATH=src` fallback was used and is recorded in `validation.md`. No build
dependency was fetched and nothing went online.

**D-3 — no live LM Studio environment.** Live smoke test is `not_performed`.
The deterministic mock/provider suite is complete.

## Dependency changes

None. `pyproject.toml` declares the already-pinned `jsonschema==4.26.0` and
nothing else. `requirements-contracts.txt` is unchanged. The runtime uses only
the standard library plus that existing pin. No agent, orchestration, prompt,
vector, persistence, or tool framework was added.

## Ready for independent Codex review?

**Not yet.** C-1 must be resolved by Dad/Blu first. Once resolved, the
remaining work is to re-run the two affected suites and the two validators; no
production code change is expected.

Do not merge. BC-050 is not self-closed.
