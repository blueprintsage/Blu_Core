# BC-050 — Validation Record

status: recorded
owner: Claude
domain: runtime
last_reviewed: 2026-08-12

## Identity

- Exact base SHA: `973589eea05fe42deeb829c5435bd09faf8cbe70`
- Branch: `bc-050-python-runtime-phase1`
- Base check: `git merge-base --is-ancestor` confirmed `origin/main` equals the
  authorized base; `git log base..origin/main` returned zero commits.

## Environment

- Python 3.12, Windows 10 Pro
- `jsonschema==4.26.0` present (matches `readiness/schema_runtime.json`)
- `setuptools`: **not installed**

## Package installation and build

```bash
python -m pip install -r requirements-contracts.txt
```

Already satisfied; `jsonschema==4.26.0` present.

```bash
python -m pip install -e .
```

**Not run.** The declared build backend (`setuptools>=68`) is unavailable
locally. Under pip 25.0.1 build isolation this would fetch the backend from the
network, which BC-050 §16 forbids during an offline acceptance run. Setup
therefore reports the missing prerequisite rather than going online.

Documented fallback used (§16):

```bash
PYTHONPATH=src python -m unittest discover -s tests/runtime_phase1 -p "test_*.py"
```

`tests/runtime_phase1/support.py` also inserts `src` on `sys.path` so the suite
runs from a clean checkout without an install. This is the recorded fallback,
not a substitute for install verification; install verification remains
outstanding until a backend is present.

## Test results

| Suite | Command | Result |
| --- | --- | --- |
| Runtime Phase 1 | `python -m unittest discover -s tests/runtime_phase1 -p "test_*.py"` | **119 tests, OK** |
| Security | `python -m unittest discover -s tests/security -p "test_*.py"` | 36 tests, **1 failure** (C-1) |
| Readiness | `python -m unittest discover -s tests/readiness -p "test_*.py"` | 18 tests, **2 failures** (C-1) |
| Continuity | `python -m unittest discover -s tests/continuity -p "test_*.py"` | 42 tests, OK |

All three failures share one root cause, recorded as C-1a in `handoff.md`:
`tools/validate_opsec_contracts.py:652-655` requires
`implementation_authorized` to be `false`, which contradicts the authorized
BC-050 readiness transition. No failure is attributable to runtime code.

## Contract validation

```bash
python tools/validate_opsec_contracts.py
```

**2 errors**, both C-1.

```bash
python tools/validate_python_readiness.py
```

**2 errors**, both C-1 surfaced through the expanded OPSEC proof. Every other
readiness check passes, including the amended BC-050 gate, layout
classification, support-layer roster, manifest completeness, and golden digests.

Remaining repository validators, observed individually:

| Validator | Result | Note |
| --- | --- | --- |
| `validate_runtime_contracts.py` | PASS | |
| `validate_successor_kernel_spec.py` | PASS | |
| `validate_viability_audit.py` | PASS | |
| `validate_historical_archive_inventory.py` | PASS | |
| `validate_historical_behavioral_archaeology.py` | PASS | |
| `validate_continuity_contracts.py` | **FAIL** | C-1b: `PROHIBITED_IMPLEMENTATION_ROOTS` includes `src` |
| `validate_host_adapter_contracts.py` | **FAIL** | **pre-existing**, not caused by BC-050 |

The host-adapter failure reproduces at the authorized base commit with no
BC-050 changes present. `contracts/successor/unresolved_register.json` was last
modified by BC-041 (`9ccd17d`), after the BC-020 base the guard compares
against; BC-050 did not touch that file. Recorded, not repaired — it is outside
this assignment's collision domain.

## Golden, manifest, and architecture

```bash
cd kernel/golden/v0.22.0 && sha256sum -c SHA256SUMS
```

All golden artifacts OK (zero non-`OK` lines). The manifest lists paths
relative to its own directory, so the check runs from there. `kernel/golden/v0.22.0/**` is unmodified in this
branch; `git diff --stat base -- kernel/golden` is empty.

```bash
git diff --check
```

Clean.

Manifest: `MANIFEST.sha256` regenerated with the validator's own digest rule
(`git show :path` for tracked content, CRLF→LF for untracked text). 307
entries; readiness manifest guard reports no missing, stale, or duplicate paths.

Architecture: 7 components / 8 packets / 9 interfaces unchanged. No component,
packet, or interface was added. `contracts/successor/**` is untouched.

## Model-facing envelope

Byte-level construction and digest reproduce the pinned §3.4 vector exactly:

```text
persona bytes           25083
operations law bytes    11371
runtime binding bytes     335
rendered envelope bytes 36887
canon_projection_digest 103e0e2dd94183c914dc8c46e3ac376af516382548e17af40c14c27d3319f142
final byte              0x5D  ']'
```

Verified seams confirm the source asymmetry is preserved, not normalized:

```text
Persona:  ...t validation.\n\n[/BLU_CANON_PERSONA]\n
OpLaw:    ...ion boundaries.\n[/BLU_CANON_OPERATIONS_LAW]\n
```

Tests additionally assert the digest is **not** any rejected derivation
(Persona alone, Operations Law alone, raw concatenation, or a concatenation of
source digests), that golden verification happens over raw bytes before
decoding, and that a CRLF-converted source fails integrity before rendering.

## Protected-policy leakage check

- Configuration stores environment-variable names only; no path, payload,
  digest, or protected value.
- Policy payload never appears in load failure state (asserted).
- Ingress and egress evidence carry only the contract's allowed fields;
  matched text, rule values, spans, and the HMAC key are absent (asserted).
- The model-facing request carries no protected-policy content (asserted).
- No production protected value was added to Git. Only the pre-existing
  synthetic fixture is used, which carries the standard notice
  `synthetic test policy != production protected policy`.

## OPSEC differential equivalence (B-2)

Production `normalized_match_candidate` vs the BC-041-C1 reference
`tools/validate_opsec_contracts.py::normalized_match_candidate`, comparing
`(normalized, removed_cf_boundaries)`:

| Corpus | Result |
| --- | --- |
| Six required `Cf` code points × 11 attack shapes | equal |
| Mixed code points (all 3-permutations) | equal |
| Surrounding-context matrix (6 × 7 × 7) | equal |
| False-positive corpus | equal |
| Generated random cases (4,000, seeded) | equal |
| Generated multi-placement inside phrase (3,000, seeded) | equal |
| Pre-commit exploratory sweep (120,000 randomized) | 0 mismatches |

Decision-level differential (`evaluate_ingress`) also equal across the attack
and negative corpus, including `ordinary_word_adjacency` negatives and
`unseparated_self_repetition` positives.

The reference file is unmodified and is loaded as published via
`importlib.util.spec_from_file_location`.

## Provenance boundedness (C1 N-2) and invariant (C1 N-1)

Measured on `Cf`-saturated input:

| Removals | Production | Reference |
| --- | --- | --- |
| 400 | 0.32 ms | 6.24 ms |
| 1600 | 4.50 ms | 92.17 ms |
| 6400 | 5.63 ms | 1376.67 ms |

The reference grows quadratically; production stays near-linear. The stress
test asserts an 8× input growth costs under 20× time, which separates linear
from quadratic decisively.

Construction: one pass for `Cf` removal, one NFKC pass with starter-chunked
composition verified globally, and single forward/reverse passes for the
collapsed prefix and suffix length arrays. Each removal then costs O(1). The
reference's whole-prefix/whole-suffix agreement predicate is equivalent to
`P[w] + S[w] == len(normalized)`; boundaries where NFKC does not split cleanly
return `None`, reproducing the reference's conservative drop.

Invariant test (N-1): a removed `Cf` flanked by word characters on both sides
always yields a provenance offset, asserted across all six code points and 16
flanking pairs, plus a repeated-removal case.

## Provider non-invocation proofs

Model Execution Boundary exposes `invocation_count`. Observed count is exactly
`0` for every pre-model terminal failure:

| Condition | Status | Invocations |
| --- | --- | --- |
| Protected phrase | BLOCK | 0 |
| Mixed + repeated `Cf` protected phrase | BLOCK | 0 |
| Outer-edge `Cf` protected phrase (all six code points) | BLOCK | 0 |
| Invalid input (non-string) | INVALID | 0 |
| Slash command | UNAVAILABLE | 0 |
| Protected policy unavailable | UNAVAILABLE | 0 |
| Invalid configuration | INVALID | 0 |
| Canon digest mismatch | BLOCK | 0 |
| Model absent / not loaded / context unknown / context insufficient | UNAVAILABLE | 0 |

Post-model failures never publish output: tool-call candidate
(`tool_executed: false`), timeout, identity mismatch, and protected egress
residual all yield `public_output: None` and write no receipt.

## LM Studio provider results

All deterministic mocks; no live instance required. Covered and passing:
endpoint unavailable; malformed inventory (three shapes); key absent; key
present but unloaded; wrong model type; unknown context; insufficient context;
multiple loaded instances (limitation recorded); successful match; malformed
chat response (four shapes); identity mismatch; timeout; ordinary message;
tool_call; invalid_tool_call; reasoning + message; reasoning only; structured
content; unknown output kind.

Request profile asserted to contain exactly
`{model, input, system_prompt, stream, store, context_length}` with
`stream=false`, `store=false`, and none of `previous_response_id`,
`response_id`, `tools`, `tool_choice`, `integrations`, `mcp`.

## Continuity truth

`durability_claimed: false` and `provider_available: false` on every turn,
including across repeated turns in one live process, asserting that process
lifetime never becomes durable continuity.

## `00_Instructions.md` Phase-1 parity mapping (R-2)

`00_Instructions.md` does not enter the Python model-facing payload. Each
Phase-1-applicable section is accounted for below. Rows marked **semantic**
require reviewer judgment: no deterministic check proves natural-language
equivalence, consistent with `one_blu_canon_manifest.json#drift_detection`.

| `00_Instructions.md` section | Destination | Kind | Reviewer check |
| --- | --- | --- | --- |
| Identity Lock | `01_Persona.md` — Identity Kernel ("Blu is Blu"), Immutability, Non-Reduction Rule | Persona | semantic |
| Interaction Floor | `01_Persona.md` — Relational Floor, Warmth & Presence, Output Contract | Persona | semantic |
| Truth Discipline | `02_Operations_Law.md` — Runtime Truth Doctrine (line 39) | Operations Law | semantic |
| No Runtime Theater | `02_Operations_Law.md` — Runtime Truth Doctrine, "Prevent fabricated certainty, runtime theater" | Operations Law | semantic |
| Completion Proof | `02_Operations_Law.md` — Terminal Packet Doctrine (line 185) **and** deterministic `TurnReceipt` evidence binding | Operations Law + deterministic | semantic + mechanical |
| Execution Law | `02_Operations_Law.md` — Execution Discipline Doctrine (line 65) **and** Turn Controller one-route lock, `side_effects: false` | Operations Law + deterministic | semantic + mechanical |
| Verb Lock | `02_Operations_Law.md` — Execution Discipline Doctrine | Operations Law | semantic |
| Compliance Gate | `02_Operations_Law.md` — Terminal Packet Doctrine **and** deterministic Validation and Egress (one validator authorizes one terminal result) | Operations Law + deterministic | semantic + mechanical |
| OPSEC / Privacy | Deterministic Pre-ingress Security Restraint and Validation and Egress, under `contracts/security/opsec/minimum_contract.json`, which cites this section as recovered current law | deterministic | mechanical |
| Runtime Binding | `[BLU_RUNTIME_BINDING]` host-mechanics block (capability truth only) | deterministic | mechanical |
| Loop Discipline | Deterministic fixed turn sequence: ingress → restraint → controller → boundary → normalization → egress → one terminal packet | deterministic | mechanical |
| Precedence | `config/source_authority.json` authority order; no deployment or provider may create a higher behavioral authority | deterministic | mechanical |
| Runtime Entry Boundary | GPT-only mechanic — correctly omitted from Python model-facing envelope | GPT-only | mechanical |
| Bootloader | GPT-only mechanic — correctly omitted | GPT-only | mechanical |
| Repo Bootstrap Bridge | GPT-only mechanic — correctly omitted | GPT-only | mechanical |
| Coherence Guard Pointer | `02_Operations_Law.md` — Coherence Guard Doctrine (line 94) | Operations Law | semantic |

No Phase-1-applicable section is unaccounted for. Codex should independently
confirm the semantic rows rather than accept this table.

## One-Blu verification

Asserted by test: no `python_persona.md`, `local_blu_persona.md`,
`lm_studio_persona.md`, or any `.md` behavioral source ships under `src/`; the
model-facing sources are exactly Persona and Operations Law; canon loads from
`kernel/golden/v0.22.0`; and the system prompt sent to the provider is
byte-identical to the verified projection.

## Unsupported features verified absent

No Auth, protected continuation, slash-command execution, Local Mirror, durable
continuity, tools, MCP, artifacts, reminders, scheduling, SkillForge, PASS,
streaming, model loading/downloading, model routing, fallback models, web
service, GUI, or installer. Slash commands and unexpected `ASK` terminate
without provider invocation, asserted by test.

## Live LM Studio smoke test

`not_performed`. No live environment was supplied. No live evidence is
fabricated or implied.
