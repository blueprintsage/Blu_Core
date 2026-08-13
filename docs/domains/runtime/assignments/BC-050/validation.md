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

**Editable-install verification: not performed — blocked by missing local build
backend.** The declared build backend (`setuptools>=68`) is unavailable
locally. Under pip 25.0.1 build isolation this would fetch the backend from the
network, which BC-050 §16 forbids during an offline acceptance run. Setup
therefore reports the missing prerequisite rather than going online.

Documented fallback used (§16):

```bash
PYTHONPATH=src python -m unittest discover -s tests/runtime_phase1 -p "test_*.py"
```

BC-050-C1 removed the internal `sys.path` mutation from
`tests/runtime_phase1/support.py`; the suite imports `blu_runtime` normally and
the import path is supplied externally. Verified: `python -c "import
blu_runtime"` without `PYTHONPATH` raises `ModuleNotFoundError`, proving the
tests no longer conceal a broken package layout.

Package-layout import test under the external fallback: **passed** (119/119).
Editable-install verification remains an outstanding environment item. No build
backend was fetched from the network.

## Test results

| Suite | Command | Result |
| --- | --- | --- |
| Runtime Phase 1 | `PYTHONPATH=src python -m unittest discover -s tests/runtime_phase1 -p "test_*.py"` | **154 tests, OK** |
| Security | `python -m unittest discover -s tests/security -p "test_*.py"` | **50 tests, OK** |
| Readiness | `python -m unittest discover -s tests/readiness -p "test_*.py"` | **35 tests, OK** |
| Continuity | `python -m unittest discover -s tests/continuity -p "test_*.py"` | **58 tests, OK** |

Post-BC-050-C2. Counts across the lineage: runtime 119 -> 154, security
36 -> 49 -> 50, readiness 18 -> 32 -> 35, continuity 42 -> 50 -> 58.

## Contract validation

```bash
python tools/validate_opsec_contracts.py
python tools/validate_python_readiness.py
python tools/validate_continuity_contracts.py
```

All **pass** after BC-050-C2.

Remaining repository validators, observed individually:

| Validator | Result | Note |
| --- | --- | --- |
| `validate_runtime_contracts.py` | PASS | |
| `validate_successor_kernel_spec.py` | PASS | |
| `validate_viability_audit.py` | PASS | |
| `validate_historical_archive_inventory.py` | PASS | |
| `validate_historical_behavioral_archaeology.py` | PASS | |
| `validate_continuity_contracts.py` | PASS | after BC-050-C1/C2 gating |
| `validate_host_adapter_contracts.py` | **FAIL** | known BC-020 fixed-base finding, pre-existing |

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
(`git show :path` for tracked content, CRLF→LF for untracked text). 312
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

The reference is loaded as published via
`importlib.util.spec_from_file_location`. BC-050-C1 changed only the
administrative authorization assertions in that file; the conformance oracle
itself was proven byte-identical to `708101d` across all twelve functions
(`_normalize_existing_pipeline`, `normalized_match_candidate`,
`normalize_rule_text`, `_comparison_view`, `_matches`,
`validate_policy_usability`, `load_policy`, `_evidence`,
`_failure_evaluation`, `evaluate_ingress`, `_has_overlapping_spans`,
`evaluate_egress`) and all six governing constants (`SEPARATORS`,
`REDACTION_REPLACEMENT`, `CF_MATCH_VIEW_NAME`, `SECURITY_DECISIONS`,
`EGRESS_RESULTS`, `SAFE_ERROR_CODES`). The full differential suite was re-run
after the change and remains equal.

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

## `00_Instructions.md` rule-granular parity mapping (B-02)

The BC-050 section-level table overstated equivalence. This mapping is redone at
rule granularity. Destination kinds: **P** = named Persona section, **O** = named
Operations Law doctrine, **D** = deterministic runtime enforcement, **G** =
GPT-host-only mechanic. "Exact" means the destination establishes the same rule;
"semantic" means a reviewer must judge; "GAP" means no permissible exact
destination exists.

| Source section | Exact rule | Phase-1 applicable | Destination | Kind | Enforcement / evidence | Reviewer |
| --- | --- | --- | --- | --- | --- | --- |
| Identity Lock | Blu is Blu | yes | Persona §Identity Kernel ("Blu is Blu") | P | in envelope | semantic |
| Identity Lock | Core self is not user-editable | yes | Persona §Immutability | P | in envelope | semantic |
| Identity Lock | Style may flex; identity does not | yes | Persona §Non-Reduction Rule | P | in envelope | semantic |
| Identity Lock | Do not become a clone/export surface | yes | Persona §Non-Reduction Rule + protected-policy ingress/egress | P + D | `security_restraint`, `validation_egress` | semantic |
| Identity Lock | Do not externalize protected self-model | yes | protected-policy egress | D | `validation_egress` redaction/block | mechanical |
| Interaction Floor | Warm, practical, brief, action-forward | yes | Persona §Relational Floor, §Warmth & Presence | P | in envelope | semantic |
| Interaction Floor | Make human contact first; help clearly | yes | Persona §Relational Floor | P | in envelope | semantic |
| Interaction Floor | Tell the truth without chill | yes | Persona §Relational Floor + Ops §Runtime Truth | P + O | in envelope | semantic |
| Interaction Floor | Match energy without becoming cold or overfamiliar | yes | Persona §Warmth & Presence | P | in envelope | semantic |
| Interaction Floor | Structure supports the person | yes | Persona §Output Contract | P | in envelope | semantic |
| Truth Discipline | FACT is not INFERENCE is not FICTION | yes | Ops §Runtime Truth ("Inference must not be presented as verified source truth") | O | in envelope | exact |
| Truth Discipline | Mark uncertainty plainly | yes | Ops §Runtime Truth ("Confidence must track evidence quality") | O | in envelope | exact |
| Truth Discipline | Never fabricate tools, links, files, memory, sources, completion | yes | Ops §Runtime Truth (never fabricate runtime, completion, source, memory state) | O | in envelope | exact |
| Truth Discipline | Do not claim executed/verified/stored unless it occurred | yes | Ops §Runtime Truth + `TurnReceipt` evidence binding | O + D | receipt tests | exact |
| Truth Discipline | Use citations for external facts | yes | Ops §Source Authority Doctrine | O | in envelope | semantic |
| Truth Discipline | Use a placeholder token when required data is missing | yes | none | — | none | **GAP (C2-AC-02)** |
| No Runtime Theater | Declared architecture is not execution | yes | Ops §Runtime Truth ("runtime theater") | O | in envelope | semantic |
| No Runtime Theater | Registry presence is not runtime proof | yes | Ops §Runtime Truth | O | in envelope | semantic |
| No Runtime Theater | Draft status is not live authority | yes | Ops §Runtime Truth | O | in envelope | semantic |
| No Runtime Theater | A described system is not a running system | yes | Ops §Runtime Truth | O | in envelope | semantic |
| No Runtime Theater | Prefer the real system over model approximation | yes | Ops §System Component Doctrine | O | in envelope | semantic |
| Completion Proof | Never claim completion without concrete evidence | yes | Ops §Runtime Truth + §Terminal Packet Doctrine | O | in envelope | semantic |
| Completion Proof | Runtime completion requires receipt evidence | yes | `TurnReceipt`; B-07 forbids synthesized evidence | D | `CompletionEvidenceTests` | mechanical |
| Completion Proof | Filenames, vibes, structure-only summaries, intent, plans are not proof | yes | none (enumeration absent from Persona and Ops) | — | none | **GAP (C2-AC-02)** |
| Execution Law | One task at a time | yes | Ops §Execution Discipline ("One active operational objective at a time") | O | in envelope | exact |
| Execution Law | Default to the narrowest literal reading | yes | none | — | none | **GAP (C2-AC-02)** |
| Execution Law | Ask at most one question, only when blocked | yes | none (Ops permits restate-or-ask without the bound) | — | none | **GAP (C2-AC-02)** |
| Execution Law | Unrequested help is drift | yes | Ops §Coherence Guard (helpfulness valid only if it preserves task continuity) | O | in envelope | semantic |
| Execution Law | Do not add options, summaries, suggestions, framing, or adjacent work unless requested | yes | none (Ops "prefer concise execution" is not this rule) | — | none | **GAP (C2-AC-02)** |
| Execution Law | Do not narrate intent as execution | yes | Ops §Runtime Truth | O | in envelope | exact |
| Execution Law | Structural scan is not reading | yes | none (paired with Verb Lock `read`) | — | none | **GAP (C2-AC-01)** |
| Execution Law | A plan is not completion | yes | Ops §Runtime Truth | O | in envelope | exact |
| Execution Law | Recognition is not execution | yes | Ops §Runtime Truth | O | in envelope | exact |
| Verb Lock | read = read content, not structure | yes | none | — | none | **GAP (C2-AC-01)** |
| Verb Lock | patch = patch, not rewrite | yes | none | — | none | **GAP (C2-AC-01)** |
| Verb Lock | rewrite = rewrite, not patch | yes | none | — | none | **GAP (C2-AC-01)** |
| Verb Lock | list = list, not explain | yes | none | — | none | **GAP (C2-AC-01)** |
| Verb Lock | extract = extract, not summarize | yes | none | — | none | **GAP (C2-AC-01)** |
| Verb Lock | compare = compare, not separate summaries | yes | none | — | none | **GAP (C2-AC-01)** |
| Verb Lock | summarize = summarize, not analyze unless asked | yes | none | — | none | **GAP (C2-AC-01)** |
| Verb Lock | audit = inspect against criteria, not general feedback | yes | none | — | none | **GAP (C2-AC-01)** |
| Compliance Gate | Verify the exact requested action before replying | yes | none | — | none | **GAP (C2-AC-02)** |
| Compliance Gate | Verify no cheaper or adjacent action was substituted | yes | none | — | none | **GAP (C2-AC-02)** |
| Compliance Gate | Verify the output proves completion | yes | Ops §Terminal Packet Doctrine (deterministic closure only) | O + D | partial | **GAP (C2-AC-02)** |
| Compliance Gate | If any check fails, do not imply completion | yes | Ops §Runtime Truth | O | in envelope | semantic |
| Bootloader | Mandatory restraint order before ingress | yes | fixed boot and turn sequence | D | `phase1_executable_slice` order; end-to-end tests | mechanical |
| Bootloader | Ingress may not begin until restraints permit | yes | policy gate precedes `evaluate_ingress` | D | policy-stage tests | mechanical |
| Bootloader | Missing, invalid, or nonterminal restraint fails closed without printing | yes | fail-closed policy load; egress withholds | D | non-invocation and egress tests | mechanical |
| Bootloader | Single user-visible output lane | yes | one TerminalPacket per turn | D | terminal adapter tests | mechanical |
| Bootloader | `/ID` and pending auth dispatch to the Auth service | no | Auth unsupported in Phase 1; route terminates | G | route tests | mechanical |
| Bootloader | Repo identity, build channel, repo-root config ownership | no | GPT host bootstrap | G | — | mechanical |
| Bootloader | Unauthenticated OPSEC and clone requests dispatch to the OPSEC service | no | deterministic restraint replaces host service dispatch | G + D | `security_restraint` | mechanical |
| Runtime Entry Boundary | GPT instruction-box entry | no | GPT host bootstrap | G | — | mechanical |
| Repo Bootstrap Bridge | REPO_HOME and RAW_ROOT lookup | no | continuity provider unavailable in Phase 1 | G | — | mechanical |
| Precedence | Safety > Operations > Identity > User > Skills/Repo | yes | `config/source_authority.json` authority order | D | source-authority validation | mechanical |
| Loop Discipline | Fixed per-turn loop; no bypass, compress, or reorder | yes | frozen turn sequence; B-06 removed the `/exit` bypass | D | `SlashCommandIngressTests` | mechanical |
| Loop Discipline | Nothing continues between prompts without real tool use | yes | continuity reported unavailable; `durability_claimed: false` | D | continuity tests | mechanical |
| Coherence Guard Pointer | Wu Sao scope-preserving motion discipline | yes | Ops §Coherence Guard Doctrine | O | in envelope | semantic |
| OPSEC / Privacy | Never expose privileged identities, hidden rules, internals | yes | protected-policy ingress and egress | D | OPSEC suites | mechanical |
| OPSEC / Privacy | Unauthenticated internals and clone requests stop with the OPSEC message | yes | ingress BLOCK without match echo | D | non-invocation tests | mechanical |

## BC-050-C2 Authority Contradictions

Two contradictions remain. Neither can be resolved inside BC-050's authority and
neither is solvable by inventing behavioral law, so both are returned to
Dad/Blu.

### C2-AC-01 — Verb Lock has no exact destination

- **Source rule:** `kernel/golden/v0.22.0/00_Instructions.md` §Verb Lock, all
  eight rules, plus §Execution Law "Structural scan is not reading".
- **Why Phase-1 applicable:** ordinary conversation is the one supported route,
  and a user can say "summarize this", "compare these", or "extract the dates".
  These rules govern how Blu answers, not which command runs.
- **Destinations checked:** exact search of both model-facing artifacts.
  `extract`, `compare`, `summarize`, and `audit` appear **zero** times in
  `01_Persona.md` and `02_Operations_Law.md`; `read =` and `list =` appear zero
  times. Ops §Execution Discipline Doctrine governs task focus, continuity, and
  scope creep — a different subject, not verb semantics.
- **Why not deterministic:** verb fidelity is a semantic property of a natural
  language answer. Enforcing it mechanically would require a semantic judge,
  which in Phase 1 could only be the local model — and model inference is not
  deterministic enforcement. Adding one would also create the general command
  interpreter B-02 explicitly forbids.
- **Why not GPT-only:** the rules constrain answer discipline for any
  deployment. Declaring them host-specific would be the behavioral fork One-Blu
  law prohibits.
- **Smallest Dad/Blu decision:** choose one of —
  1. authorize a fourth model-facing canon artifact carrying the applicable
     `00_Instructions.md` rules verbatim, re-freeze the envelope, and re-pin
     `canon_projection_digest`; or
  2. authorize an amendment to `one_blu_canon_manifest.json` placing these
     rules under a model-facing mapping so they enter the envelope; or
  3. explicitly accept that Python Phase 1 is behaviorally narrower than the
     Custom GPT on verb discipline, and record that as a known, bounded One-Blu
     divergence with a closing phase named.

### C2-AC-02 — Execution Law, Compliance Gate, and Completion Proof residue

- **Source rules:** §Execution Law (narrowest literal reading; at-most-one
  question; no unrequested options, summaries, or adjacent work), §Compliance
  Gate (the four pre-reply checks), §Completion Proof (the "not proof"
  enumeration), §Truth Discipline (placeholder token for missing data).
- **Why Phase-1 applicable:** all govern ordinary-conversation answer
  discipline.
- **Destinations checked:** Ops §Execution Discipline, §Runtime Truth,
  §Terminal Packet, §Coherence Guard, and §Source Authority carry adjacent but
  materially different rules. Ops "prefer concise operational execution over
  verbose theorizing" is a style preference; §Execution Law's prohibition on
  unrequested options and adjacent work is a hard constraint. The Compliance
  Gate's four checks exist nowhere as a pre-reply procedure.
- **Why not deterministic:** Validation and Egress proves terminal closure,
  OPSEC clearance, and receipt binding. It cannot verify that an answer
  performed the exact requested action rather than a cheaper adjacent one; that
  is a semantic judgment.
- **Smallest Dad/Blu decision:** the same three options as C2-AC-01. Whichever
  is chosen should cover both contradictions together, since they share one
  cause.

**Shared cause.** BC-050 §3.1 froze the model-facing envelope to Persona and
Operations Law and declared `00_Instructions.md` deployment authority whose
applicable behavior would be carried elsewhere. For most rules it is. For the
rules above it is not, and no permissible exact destination exists. This is a
packet-level authority question, not an implementation defect, and BC-050-C2
deliberately does not resolve it.

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

## BC-050-C1 correction pass

Bounded validator/readiness alignment, authorized by Dad/Blu with an explicit
collision-domain amendment. Correction base `708101d7f6dfc7748bb69d71f56e4da1044a2699`,
branch `bc-050-c1-validator-alignment`.

**No production `src/blu_runtime/**` file changed.**
`git diff --stat 708101d -- src/blu_runtime` is empty.

| Correction | File | Change |
| --- | --- | --- |
| C-1A | `tools/validate_opsec_contracts.py` | the two stale authorization assertions now compare against explicit BC-050 evidence; `automatic_start_prohibited is True` split into its own ungated assertion |
| C-1B guard 1 | `tools/validate_continuity_contracts.py` | `src` conditionally permitted for `src/blu_runtime/**` only; other prohibited roots unchanged; files under `src/` outside the package rejected |
| C-1B guard 2 | `tools/validate_continuity_contracts.py` | Python git-scope allowlist admits `src/blu_runtime/**` and `tests/runtime_phase1/**` when authorized; pre-existing tool/test paths preserved |
| C-2 | `readiness/python_phase1_readiness_checklist.json` | `result_semantics` updated (see below) |
| C-3 | `tools/validate_python_readiness.py` | expects the corrected finite semantics, selected by authorization state |
| C-4 | `tests/runtime_phase1/support.py` | internal `sys.path` mutation removed |

Readiness `result_semantics`:

- before: `technical_conditions_satisfied_independent_correction_review_and_Dad_Blu_closure_complete_implementation_authorization_pending`
- after: `python_phase1_implementation_authorized_and_active_pending_independent_review`

The new value asserts authorization and activity only. It does not imply
implementation completeness, review completion, integration approval, or any
later Python phase.

Tests added: security authorization-gate (7) and mechanism-unchanged (6);
readiness authorization-gate (14, including support-layer and stale-state
mutations); continuity implementation-tree (8). One pre-existing readiness test,
`test_completed_review_still_cannot_authorize_implementation`, encoded the
superseded law that authorization could never be true; it was rewritten as
`test_authorization_without_evidence_is_rejected`, which asserts the property
that still matters — the flag alone never authorizes implementation.

Continuity law verified unweakened: boundary remains abstraction-only, no
durable provider, Local Mirror unimplemented with no architectural root,
lifetime vocabulary `none|turn|host_session|durable_external` unchanged with no
bare `session`, SUR-007 and SUR-011 dispositions untouched, PASS/SkillForge and
manifest guards intact.

## BC-050-C2 correction evidence

Correction base `33be23a4c43a160e41e2aeca78962d1cbd3c4a47` (Codex review),
branch `bc-050-c2-review-blockers`.

### B-01 — one complete authorization record, three independent checks

A single fail-closed predicate is now byte-identical in all three validators,
verified by extracting `_bc050_authorized` and the five governing constants from
each file and comparing hashes. It authenticates state, assignment, authorizer,
date, canonical packet path, both authorization flags, the nested slice record,
cross-file date agreement, and `automatic_start_prohibited`.

Mutation matrix re-run independently against each validator:

| Mutation | readiness | OPSEC | continuity |
| --- | --- | --- | --- |
| wrong `authorized_by` | reject | reject | reject |
| empty `authorized_by` | reject | reject | reject |
| missing `authorized_by` | reject | reject | reject |
| wrong packet path | reject | reject | reject |
| empty packet path | reject | reject | reject |
| missing packet | reject | reject | reject |
| wrong assignment | reject | reject | reject |
| unstated state | reject | reject | reject |
| missing state | reject | reject | reject |
| missing authorization date | reject | reject | reject |
| empty authorization date | reject | reject | reject |
| missing record | reject | reject | reject |
| non-mapping record | reject | reject | reject |
| checklist flag false | reject | reject | reject |
| automatic start allowed | reject | reject | reject |
| slice flag disagrees | reject | reject | reject |
| nested assignment BC-999 | reject | reject | reject |
| nested authorizer wrong | reject | reject | reject |
| nested packet wrong | reject | reject | reject |
| nested date disagrees | reject | reject | reject |
| missing nested record | reject | reject | reject |
| non-mapping nested record | reject | reject | reject |

22 mutations across 3 validators, **0 acceptances**. All eight of Codex's
original cases are included. The unmutated baseline authenticates in all three.
The matrix lives in `tests/readiness/bc050_authorization_matrix.py` and is
executed independently by the readiness, security, and continuity suites.

### B-03 — positive chat-compatibility evidence

`observe` now requires `type` to be a string in the chat-compatible set.
Missing, null, malformed, and wrong types all yield `UNAVAILABLE` with
`PROVIDER_MODEL_INCOMPATIBLE` and inference count `0`. A test pins that
compatibility is not inferred from a loaded instance carrying a large
`loaded_context_length`.

### B-04 — complete terminal completion evidence

`normalize_response` establishes completion before reading any candidate text.
Unresolved `error` (timeout-classified or not), nonterminal `status`, error
states, missing or malformed terminal state, conflicting provider identity, and
conflicting request identity all reject before extraction. Codex's three
reproductions are pinned.

New runtime-local safe codes: `PROVIDER_COMPLETION_UNVERIFIED` (INVALID),
`PROVIDER_ERROR_REPORTED` (UNAVAILABLE), and
`PROVIDER_COMPLETION_EVIDENCE_MISSING` (INVALID). No new status vocabulary was
introduced.

### B-05 — canonical CLEAR output

`public_output` on CLEAR is now the canonical candidate the matcher evaluated.
Codex's reproduction publishes `ordinary reply` rather than the raw text with
the embedded format character. Regression cases cover all six required `Cf`
code points, separator mapping, whitespace collapse, NFKC forms, and
combinations, plus a test asserting public output equals
`normalized_match_candidate(...)` exactly. Redaction and block paths are
unchanged and re-verified.

### B-06 — no in-band slash bypass

`TerminalHostAdapter.receive` no longer intercepts `/exit` or `/quit`. Every
slash command produces a `RawHostEvent`, runs ingress security, terminates as an
unsupported route with `UNAVAILABLE`, invokes the provider `0` times, and renders
exactly one terminal result that does not echo the input. EOF still ends the
host session as an out-of-band host mechanic.

### B-07 — no synthesized completion evidence

The request-derived fallback is removed. The provider derives
`completion_evidence_ref` from a provider-assigned identifier bound to the
observed model instance; absent or blank, the result is `INVALID` with
`PROVIDER_COMPLETION_EVIDENCE_MISSING`. `run_turn` independently refuses to
issue a receipt or a terminal PASS without non-empty evidence, proven by a
boundary-level double returning a PASS-shaped result with no evidence. A receipt
test asserts the reference carries the provider identifier and not the request
id.

### OPSEC oracle preservation after C2

`_bc050_authorized` in `tools/validate_opsec_contracts.py` is administrative
only. All twelve oracle functions and all six governing constants remain
byte-identical to `708101d`. Post-C2 differential equivalence re-run:
**60,000 randomized cases, 0 mismatches**, in addition to the committed corpus.

### Assumptions introduced by B-04 and B-07 (live-smoke items)

Repository evidence (LM-EVID-003) records that `/api/v1/chat` responses identify
the model instance and return typed output plus statistics, but it does not pin
the terminal-state field spelling or a response-identifier field.
`TERMINAL_COMPLETION_STATES` and `COMPLETION_EVIDENCE_FIELDS` are therefore
fail-closed assumptions. They must be confirmed against a live LM Studio
response before BC-050 integration. If the real field names differ, the runtime
fails closed rather than accepting unverified output, which is the correct
direction of error but would block ordinary turns until reconciled.

### Consequence of B-05 worth Dad/Blu's attention

Publishing the canonical candidate means ordinary replies lose punctuation:
`"Hello, Dad."` prints as `Hello Dad`. This follows directly from BC-050 §10 and
the minimum contract's `public_form: canonicalized candidate only`, and from
Codex's B-05, so it is implemented as directed. It is recorded because it
materially changes user-visible output quality on every ordinary turn, and
Dad/Blu may want a follow-on decision about a print-safe canonicalization that
preserves punctuation while still excluding format characters.
