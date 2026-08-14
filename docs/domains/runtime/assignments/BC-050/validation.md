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
| Runtime Phase 1 | `PYTHONPATH=src python -m unittest discover -s tests/runtime_phase1 -p "test_*.py"` | **162 tests, OK** |
| Security | `python -m unittest discover -s tests/security -p "test_*.py"` | **50 tests, OK** |
| Readiness | `python -m unittest discover -s tests/readiness -p "test_*.py"` | **53 tests, OK** |
| Continuity | `python -m unittest discover -s tests/continuity -p "test_*.py"` | **58 tests, OK** |

Post-BC-050-C3. Counts across the lineage: runtime 119 -> 154 -> 162,
security 36 -> 49 -> 50, readiness 18 -> 32 -> 35 -> 53, continuity
42 -> 50 -> 58. C2A added 18 instruction-layer classification tests; C3 added
8 terminal-guidance and malformed-evidence tests plus 9 date mutations.

## Contract validation

```bash
python tools/validate_opsec_contracts.py
python tools/validate_python_readiness.py
python tools/validate_continuity_contracts.py
```

All **pass** after BC-050-C3.

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

> **Historical analysis — superseded as a BC-050 completion gate by the
> Dad/Blu BC-050-C2A authority decision (2026-08-13).** Retained because it
> is the evidence showing why the old parity assumption failed. It is no
> longer a completion requirement, and its GAP rows are no longer open
> obligations. See "BC-050-C2A B-02 Resolution" below.

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

## BC-050-C2 Authority Contradictions (resolved by C2A)

> Both contradictions below are **resolved** by the BC-050-C2A source
> reclassification. Retained as the record of what was escalated and why.

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

`not_performed` through BC-050-C3. No live environment was supplied and no live
evidence was fabricated or implied. **Performed under BC-050-C4** — see
"BC-050-C4 correction pass" below for the observed results.

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

## BC-050-C2A B-02 Resolution

Correction base `b6333a761e9dbfe310fd1ce0e3203beabe3fefdf`, branch
`bc-050-c2a-instruction-classification`.

B-02 is resolved by a Dad/Blu source-classification correction, not by claiming
semantic equivalence. The premise that every Phase-1-applicable
`00_Instructions.md` rule requires a successor parity destination is withdrawn.

| Item | Final state |
| --- | --- |
| Codex B-02 | resolved by source reclassification |
| C2-AC-01 (Verb Lock) | **resolved by source reclassification** — not by claimed equivalence, not by a runtime subsystem |
| C2-AC-02 (Execution Law / Compliance Gate / Completion Proof residue) | **resolved by source reclassification** |

What was **not** done, by design:

- no claimed semantic equivalence was added anywhere;
- no third behavioral prompt was created;
- no generated `00_Instructions.md` projection exists;
- no semantic-judge component was introduced;
- no Verb Lock runtime subsystem was built;
- no golden source changed;
- no Python prompt material was added;
- no envelope re-freeze occurred;
- no `src/blu_runtime/**` file changed.

Successor invariants remain sourced from their actual owners: Persona and
Operations Law for model-facing behavior, and approved deterministic contracts
for mechanical behavior.

### Contract changes

| File | Change |
| --- | --- |
| `readiness/one_blu_canon_manifest.json` | CANON-001 removed from `mappings`; recorded as `legacy_deployment_artifacts[DEPLOY-PROV-001]` with `successor_invariant: false`, `python_projection: none`, `cross_deployment_parity_required: false`, `automatic_behavior_migration: false`, `immutable_golden: true`. `host_binding_projection` is no longer authorized for it. |
| `readiness/one_blu_canon_manifest.json` | CANON-006 no longer cites `00_Instructions.md`; security semantics bind to the minimum OPSEC contract, `03_Exec.md`, successor boundary law, and the unresolved register. A prohibited-divergence entry forbids treating the instruction surface as the successor security authority. |
| `readiness/deployment_targets.json` | ChatGPT projection no longer requires "current CTS deployment instruction plus six golden capsules"; a `host_instruction_surface` block classifies it as deployment-local mechanics, not invariant or parity-determining. A repository-level `host_instruction_surface_rule` was added. |
| `readiness/custom_gpt_python_parity_matrix.json` | All eleven real parity dimensions preserved and each bound to its authoritative source; `non_parity_rule` and `non_parity_examples` added excluding bootstrap text, host compensators, prompt choreography, and repository-location hints. |

Mapping count is 11 (was 12); the validator's minimum of 10 and every required
behavioral subject term still hold. CANON-001's subject,
`host_and_deployment_instructions`, was never one of the required subjects.

### Validator enforcement added

`tools/validate_python_readiness.py` now rejects:

- `00_Instructions.md` appearing in any invariant mapping's
  `canonical_source_artifact`, including CANON-006;
- a provenance record claiming `successor_invariant`, a Python projection,
  parity requirement, automatic migration, or a non-immutable golden source;
- `host_binding_projection` reappearing anywhere in the provenance collection;
- absence of exactly one provenance record for the instruction surface;
- a parity matrix without the non-parity rule;
- deployment targets without the host-instruction-surface classification, or a
  ChatGPT projection that still requires the legacy instruction surface.

Seventeen negative tests in `tests/readiness/test_validate_python_readiness.py`
pin these, including a mutation that restores CANON-001 verbatim with a
`host_binding_projection` and a mutation that appends `00_Instructions.md` to
CANON-009. Both fail readiness validation.

### Documentation sweep

Active successor and readiness material carrying the successor implication was
updated. Historical material was annotated, never rewritten.

| Path | Disposition |
| --- | --- |
| `readiness/one_blu_canon_manifest.json` | updated (reclassified) |
| `readiness/deployment_targets.json` | updated |
| `readiness/custom_gpt_python_parity_matrix.json` | updated |
| `docs/sources/cts_source_roles.md` | historical role preserved; successor distinction appended |
| `docs/sources/authority_map.md` | historical role preserved; successor distinction appended |
| `docs/domains/kernel/decisions.md` | historical role preserved; successor distinction appended |
| `docs/architecture/migration_centerline.md` | **unchanged** — it carried no instruction-surface reference, and `docs/architecture` is a continuity-validator protected path; an annotation was drafted and reverted |
| `config/source_authority.json` | unchanged — records the CTS source set truthfully and is outside the C2A domain |
| `contracts/security/opsec/minimum_contract.json` | unchanged — `recovered_current_law` correctly records where current OPSEC law was recovered from; protected |
| `contracts/runtime/**`, `docs/architecture/current_runtime.md` | unchanged — describe v0.22.0 CTS as it actually existed |
| closed BC-010/015/017/018/040/041 records, `BC-050/review.md`, historical archives | unchanged — historical evidence |

The old deployment authority remains historical truth; only the successor
invariant authority changes, and only prospectively.

## BC-050-C3 final micro-correction evidence

Correction base `157441d3ea224760e8c800cdd19202cbb230d01d` (Codex second
review), branch `bc-050-c3-final-micro-correction`. Three blockers, no redesign.

### Files changed

```text
tools/validate_python_readiness.py        B-01
tools/validate_opsec_contracts.py         B-01
tools/validate_continuity_contracts.py    B-01
tests/readiness/bc050_authorization_matrix.py  B-01 date mutations
src/blu_runtime/__main__.py               B-06, B-07
tests/runtime_phase1/test_end_to_end.py   B-06, B-07
```

`src/blu_runtime/__main__.py` is the **only** production file changed. No other
runtime module was touched.

### B-01 — exact authorization-date authentication

`BC050_AUTHORIZATION_DATE = "2026-08-12"` was added to the shared predicate, and
both date comparisons now bind to that constant instead of to each other. The
predicate and its six constants remain byte-identical across all three
validators, verified by hash.

Codex's finding was that cross-file equality is not authentication: the same
wrong value in every record satisfied the old check. It no longer does.

Date mutation matrix, written into **both** readiness records and evaluated
against each validator independently:

| Date written to every record | readiness | OPSEC | continuity |
| --- | --- | --- | --- |
| `1999-01-01` | reject | reject | reject |
| `2026-08-13` (off by one) | reject | reject | reject |
| `""` | reject | reject | reject |
| `" "` | reject | reject | reject |
| `7` (integer) | reject | reject | reject |
| `null` | reject | reject | reject |
| `true` (boolean) | reject | reject | reject |
| `["2026-08-12"]` (list) | reject | reject | reject |
| `{"date": "2026-08-12"}` (dict) | reject | reject | reject |

Nine wrong dates x three validators, **0 acceptances**. The unmutated baseline
still authenticates in all three.

All prior B-01 mutations are retained: wrong/empty/missing authorizer,
wrong/empty/missing packet, wrong assignment, unstated and missing state,
missing record, non-mapping record, checklist flag false, automatic start
allowed, slice flag disagreement, nested wrong assignment/authorizer/packet/date,
missing and non-mapping nested record. The shared matrix is now 31 mutations,
executed independently by the readiness, security, and continuity suites.

### B-06 — truthful terminal guidance

The startup banner no longer claims `/exit` ends the session. It now names the
mechanism the host adapter actually implements: end-of-input (Ctrl-Z then Enter
on Windows, Ctrl-D elsewhere).

No `/exit` interception was restored and no slash-command subsystem was added.

| Probe | Result |
| --- | --- |
| banner contains `/exit` or `/quit` | no |
| banner names the real termination mechanism | yes |
| EOF actually ends the session | yes |
| `/exit` enters the ordinary user-input path | yes |
| `/quit` enters the ordinary user-input path | yes |
| provider invocations for each | `0` |
| terminal results rendered per input | exactly `1` |

### B-07 — malformed completion-evidence types fail closed

`_valid_completion_evidence` validates at the evidence boundary before any
string operation or receipt construction:

```python
isinstance(value, str) and bool(value.strip())
```

No `str()` coercion, because coercion would fabricate apparent evidence from
invalid input. No fallback reference. No generic top-level exception catch.

| `completion_evidence_ref` | accepted | terminal PASS | receipt | public output | exception |
| --- | --- | --- | --- | --- | --- |
| `None` | no | no | no | none | none |
| `""` | no | no | no | none | none |
| `"   "` | no | no | no | none | none |
| `7` (integer) | no | no | no | none | none |
| `1.5` (float) | no | no | no | none | none |
| `True` (boolean) | no | no | no | none | none |
| `["resp-1"]` (list) | no | no | no | none | none |
| `{"id": "resp-1"}` (dict) | no | no | no | none | none |
| `b"resp-1"` (bytes) | no | no | no | none | none |
| `"resp-9"` (valid) | yes | yes | yes | rendered | none |

Codex's `7` reproduction previously raised `AttributeError` from `.strip()`; it
now produces one deterministic fail-closed terminal result. A test asserts the
request id never appears in any failure path, so nothing is fabricated.

### Preserved

| Item | State |
| --- | --- |
| B-02 | resolved under C2A; not reopened |
| B-03 positive chat compatibility | closed; 28-test spot regression green |
| B-04 provider completion evidence | closed |
| B-05 canonical CLEAR output | closed |
| Frozen envelope | 36887 bytes, `103e0e2dd94183c914dc8c46e3ac376af516382548e17af40c14c27d3319f142`, final byte `0x5D` |
| OPSEC oracle | byte-identical to `708101d` across all twelve functions |
| OPSEC differential | 40,000 fresh cases, 0 mismatches |
| Architecture | 7 / 8 / 9 |
| Golden CTS | unchanged; zero non-`OK` checksum lines |

### Suites and validators

| Suite | Result |
| --- | --- |
| Runtime Phase 1 | 162 OK (was 154) |
| Security | 50 OK |
| Readiness | 53 OK |
| Continuity | 58 OK |

Eight validators pass. `validate_host_adapter_contracts.py` still reports the
known BC-020 fixed-base finding on
`contracts/successor/unresolved_register.json`, preserved and unsuppressed.

`git diff --check` clean; `MANIFEST.sha256` 312 entries with no missing, stale,
or duplicate paths. Golden verified with
`cd kernel/golden/v0.22.0 && sha256sum -c SHA256SUMS`.

### Outstanding nonblocking notes

- Editable install (`pip install -e .`) still not performed; the approved build
  backend is unavailable locally. External `PYTHONPATH=src` fallback in use.
- Live LM Studio smoke test: `not_performed`. The B-04/B-07 terminal-state and
  response-identifier field names remain fail-closed assumptions awaiting live
  confirmation.
- B-05 canonicalization still strips punctuation from otherwise safe output
  (`"Hello, Dad."` prints as `Hello Dad`). Carried as a presentation-quality
  note; not redesigned during C3 because no frozen contract is violated.
- The root `README.md` may still say no Python runtime exists. Not changed:
  C3 was not broadened into general documentation cleanup. Recorded as an
  integration cleanup note.
- N-03 continuity defensive invariant remains carried to the
  continuity-provider phase.
- BC-020 fixed-base host-adapter guard remains open and unrelated.


## BC-050-C4 correction pass

Bounded LM Studio provider-contract correction driven by the first real live
smoke. Correction base `be19ea16b61088e78850d15662943357fb3ee9b0`, branch
`bc-050-c4-lmstudio-provider-contract`. One production file changed:
`src/blu_runtime/providers/model/lm_studio.py`. No architecture, canon,
envelope, security, host-adapter, or continuity surface was touched.

### The two defects, as the live provider proved them

LM Studio was reachable and the configured model was loaded, yet boot failed
`UNAVAILABLE PROVIDER_MODEL_ABSENT`. The C3 boundary read two fields the native
v1 document does not supply.

| Defect | C3 read | Live `/api/v1/models` supplies |
| --- | --- | --- |
| D-1 model identity | `record["id"]` | `record["key"]` |
| D-2 observed capacity | `instance["context_length"]`, falling back to `record["loaded_context_length"]` | `instance["config"]["context_length"]` |

D-2 was latent behind D-1: correcting identity alone would have produced
`PROVIDER_CONTEXT_UNKNOWN` on the next boot.

### What changed

- Model-record identity is exactly `key`, matched exactly. `display_name`,
  `publisher`, `format`, and substrings are not identity, and a record-level
  `id` can no longer claim a configured key. Matching was not loosened; it was
  moved to the field the provider actually publishes.
- Observed capacity is read only from `loaded_instances[].config.context_length`
  — the capacity the instance was actually loaded with. The record-level
  `max_context_length` describes model capability, not loaded configuration,
  and is never read as capacity evidence. The former
  `record["loaded_context_length"]` fallback was removed rather than kept
  alongside: it was an unobserved spelling, and inferring capacity from a
  model-level field would report capability as though it were configuration.
- Loaded-instance identity is unchanged (`instance_id`, then `id`); the live
  document supplies `id`, which the existing precedence already accepted.
- `observed_model_key` is now the identity read from the record instead of an
  echo of the configured key, so the observation reports what was seen.

Fail-closed behavior is unchanged. Absent, null, non-`dict`, non-integer,
boolean, float, zero, and negative capacity all yield `PROVIDER_CONTEXT_UNKNOWN`;
capacity below the requested window still yields
`PROVIDER_CONTEXT_INSUFFICIENT` with the observed value recorded. No capacity
value is synthesized, defaulted, or inferred.

### Regression coverage

`LiveProviderContractTests` in `tests/runtime_phase1/test_lm_studio_provider.py`
reproduces the observed live record shape (13 tests): recognition of the live
record, selection among a multi-model inventory containing unloaded neighbours,
`display_name` rejected as identity, record `id` rejected as identity,
a conflicting `id` unable to claim the configured key, six malformed `key`
forms, not-loaded and identity-less instances, the ten-case malformed-capacity
matrix, capacity below request, model capability rejected as loaded-instance
capacity, and incompatible `type` on an otherwise live record.

`tests/runtime_phase1/support.py::model_inventory` now emits the live record
shape (`key`, `loaded_instances[].id`, `config.context_length`), so the
end-to-end suite exercises the real contract rather than the shape that
encoded the defect.

### Live LM Studio smoke — performed 2026-08-14

Environment: Windows 10 Pro, Python 3.12, LM Studio at `http://127.0.0.1:1234`,
model key `granite-4.0-h-micro` ("Granite 4.0 H Micro"), GGUF, Q4_K_M, loaded
instance context `1048576`.

The protected policy used for the smoke was the repository's **synthetic** test
fixture (`synthetic test policy != production protected policy`); the
production protected policy was not available in this environment. It gates
OPSEC evaluation only and is not part of the model-execution boundary under
test.

| Stage | Result |
| --- | --- |
| Boot before C4 | `UNAVAILABLE PROVIDER_MODEL_ABSENT` (operator's reproduction) |
| Boot after C4 | **OK** — `observed_model_key=granite-4.0-h-micro`, `model_instance_id=granite-4.0-h-micro`, observed context `1048576` |
| Turn, `requested_tokens: 4096` | `UNAVAILABLE PROVIDER_ENDPOINT_UNAVAILABLE` |
| Turn, `requested_tokens: 16384` | `INVALID PROVIDER_COMPLETION_UNVERIFIED`, `model_invoked: true`, no public output |

The provider boundary this assignment corrects is passed live. The two turn
failures are the next surface and were deliberately **not** corrected in C4.

### Next-surface evidence captured, not corrected

1. **The Phase-1 envelope does not fit a 4096-token window.** A direct probe
   with the real 36,887-byte envelope returned HTTP 500 wrapping the engine's
   `exceed_context_size_error`: `request (8021 tokens) exceeds the available
   context size (4096 tokens)`. The envelope alone is ~8,021 prompt tokens, so
   `requested_tokens: 4096` cannot carry it. This is a configuration
   observation about the smoke config, not a defect in the corrected boundary.
2. **HTTP error responses are classified as endpoint-unavailable.** LM Studio
   returned a structured provider error body with an HTTP error status;
   `urllib.error.HTTPError` is a `URLError` subclass, so `infer` reports
   `PROVIDER_ENDPOINT_UNAVAILABLE`. The endpoint was reachable and did report an
   error, which `PROVIDER_ERROR_REPORTED` already describes. Recorded for a
   separate bounded correction.
3. **The live chat response carries no `status` and no top-level `id`.** The
   observed 200 response body was `{model_instance_id, output[], stats{}}`. The
   B-04 terminal-state assumption and the B-07 completion-evidence identifier
   assumption are therefore both unconfirmed by this provider; both failed
   closed exactly as designed (`PROVIDER_COMPLETION_UNVERIFIED`, no public
   output, no fabricated evidence).
4. **Chat and inventory report different instance identities.** The chat
   response asserted `model_instance_id: "granite-4.0-h-micro:2"` while
   `/api/v1/models` reported the loaded instance as `granite-4.0-h-micro`. Had
   the completion check passed, `PROVIDER_IDENTITY_MISMATCH` would have
   followed. This needs its own live-evidenced correction.

### Suites and validators after C4

| Suite | Result |
| --- | --- |
| Runtime Phase 1 | **175 OK** (was 162; +13 live-contract tests) |
| Security | **50 OK** |
| Readiness | **53 OK** |
| Continuity | **58 OK** |

Eight validators pass; `validate_host_adapter_contracts.py` still reports the
known BC-020 fixed-base finding, unchanged and unsuppressed.

Envelope `36887` bytes, digest
`103e0e2dd94183c914dc8c46e3ac376af516382548e17af40c14c27d3319f142`, final byte
`0x5D`. Architecture 7 / 8 / 9. Golden CTS unmodified. `SecurityDecision`
vocabulary, protected ingress/egress semantics, completion-evidence fail-closed
handling, authorization-date enforcement, and `/exit` / `/quit` ordinary-ingress
behavior are all unchanged. `00_Instructions.md` parity was not reopened.

Two working-tree artifacts of the live smoke sit outside the commit and make
`validate_python_readiness.py` and `validate_continuity_contracts.py` report
errors while they are present: the untracked operator config `smoke.runtime.json`
(absent from `MANIFEST.sha256`) and the gitignored `src/blu_runtime.egg-info/`
build directory left by a local editable install. Neither is repository content
and neither is caused by C4 — every reported error names one of those two
artifacts and none names a repository file. Verified by moving both aside and
re-running: **both validators pass**, after which both artifacts were restored.
`smoke.runtime.json` was deliberately not committed and not added to the
manifest; it is the operator's local file, and a manifest entry for it would go
stale on any checkout that lacks it.

A `git worktree` checkout is not a usable verification vehicle here: this
Windows clone converts line endings on checkout, so a fresh worktree fails the
golden checksum and several digest-sensitive validators for reasons unrelated to
any commit. Golden verification was therefore run in the working clone, where it
reports zero non-`OK` lines.

## BC-050-C5 correction pass

Bounded completion-proof correction for the LM Studio native REST v1 stateless
profile, driven by the live turn that C4 unblocked. Correction base
`ac784f0cb136593b73f65a128eee658918dbb023`, branch
`bc-050-c5-lmstudio-completion-proof`.

### The defect the live provider proved

After C4, boot succeeded and the model was invoked, but every real completion
was rejected as `INVALID` with `PROVIDER_COMPLETION_UNVERIFIED` and
`model_invoked=True`.

The live native-v1 success body is:

```json
{
  "model_instance_id": "granite-4.0-h-micro:3",
  "output": [{"type": "message", "content": "Hey there! ..."}],
  "stats": {"input_tokens": 30, "total_output_tokens": 27}
}
```

Three assumptions in the C3 boundary do not hold against it:

| # | C3 required | Live native v1 with `stream: false`, `store: false` |
| --- | --- | --- |
| 1 | a terminal `status` string | no `status` field at all |
| 2 | a provider-assigned completion id (`id` / `response_id` / `completion_id`) | none — nothing is stored, so nothing is identified |
| 3 | `model_instance_id` equal to the requested instance | answers with a per-load ordinal: `granite-4.0-h-micro:3` where `/api/v1/models` reported `granite-4.0-h-micro` |

Defect 3 sat behind defects 1 and 2. Removing only the `status` check would
have moved the same rejection one step later, which the assignment explicitly
forbids, so all three were corrected together.

### How native-v1 synchronous completion is now verified

`normalize_response` establishes completion before reading any candidate text,
in this order:

1. body is an object;
2. no unresolved `error` (timeout-classified errors still map to
   `PROVIDER_TIMEOUT`, others to `PROVIDER_ERROR_REPORTED`);
3. `status` **if present** must be a string and must be terminal —
   non-terminal, error, timeout, and non-string states all still reject. Its
   absence is normal for this profile and is no longer a rejection;
4. `model_instance_id` (or `model`) is a non-blank string naming the instance
   Blu selected;
5. asserted provider/request identities, when present, must agree;
6. completion evidence resolves to one of the two proofs below;
7. `output` is a non-empty list of typed items, tool-call candidates are
   refused without execution, reasoning never becomes public text, and the
   assembled message text is non-blank.

`stats` is read nowhere. It cannot become proof of anything.

### Instance identity

`_instance_identity_agrees` accepts the requested identity exactly, or the
requested identity followed by `:` and a non-empty per-load ordinal. The model
portion must still match exactly, so `some-other-model:3`,
`granite-4.0-h-micro-instruct:3`, `granite-4.0-h:3`, `granite-4.0-h-micro:`,
and `prefix-granite-4.0-h-micro:3` all remain `PROVIDER_IDENTITY_MISMATCH`.

This suffix rule is inferred from three live observations (`:2` twice, `:3`
once) against an inventory that reported the instance unsuffixed. The published
LM Studio evidence (LM-EVID-002, LM-EVID-004) records that loaded instances
carry an identity but does not pin this format. Recorded as a live-evidenced
inference, not a documented provider guarantee.

### How an absent provider completion id is represented

New vocabulary in `contracts/models.py`:

```text
COMPLETION_PROOF_PROVIDER_ID           = "provider_assigned_completion_id"
COMPLETION_PROOF_SYNCHRONOUS_RESPONSE  = "synchronous_provider_response"
```

- `NormalizedModelResult.completion_proof: str | None` — which proof the
  boundary established. `None` means it claimed none.
- `TurnReceipt.provider_completion_evidence_ref: str | None` — was `str`. It is
  now nullable so a receipt can say "the provider assigned none" instead of
  being forced to hold something.
- `TurnReceipt.provider_completion_proof: str` — names which proof the receipt
  rests on, so a null reference reads as a provider fact rather than as missing
  data. `as_dict()` returns both keys and is typed `dict[str, str | None]`.
- `readiness/phase1_executable_slice.json` adds `provider_completion_proof` to
  `success_receipt_requires` plus a `provider_completion_proof_semantics`
  statement of what each proof asserts.

`run_turn` no longer tests the reference alone. `_completion_proof_holds`
requires the proof and the evidence to agree:

| Claimed proof | Required evidence |
| --- | --- |
| `provider_assigned_completion_id` | a non-blank string reference (B-07 unchanged) |
| `synchronous_provider_response` | the reference is exactly `None` |
| anything else, including none | fails closed |

A provider that returns a successful-looking result while claiming no proof is
still not a completed turn — the original B-07 defence is intact and still
covered by `test_boundary_level_result_without_evidence_is_not_success`.

### Proof that no completion id is fabricated

- The only value ever placed in `completion_evidence_ref` is
  `f"{provider_id}:{instance_id}:{value}"` where `value` came from the provider
  document. No other assignment to that field exists in the file.
- When the provider asserts no identifier field, the boundary returns `None`
  and the receipt stores `None`. There is no uuid, hash, `str()` coercion,
  request-id fallback, or `model_instance_id` relabelling anywhere on that
  path.
- `store` remains `False` in the request payload; it was not flipped to obtain
  an id. The payload field set is unchanged and still asserted by
  `test_request_profile_uses_only_evidenced_native_fields`.
- Tests pin it: `test_nothing_in_the_response_is_recycled_as_a_completion_id`
  checks the proof carries no instance id, model key, request id, or statistic;
  `test_no_evidence_identifier_is_synthesized_when_the_provider_assigns_none`
  scans every other receipt field for an invented completion reference.
- Absence is not confused with malformation:
  `test_asserted_but_unusable_identifier_still_fails_closed` keeps `""`,
  `"   "`, `7`, `True`, `None`, `["resp-1"]`, and `{"id": "resp-1"}` rejecting
  with `PROVIDER_COMPLETION_EVIDENCE_MISSING`.

### Fail-closed coverage

`test_malformed_live_shaped_responses_fail_closed` runs 24 malformed bodies
against the live shape — `None`, list, string, and integer bodies; empty
object; missing, blank, whitespace, null, and non-string `model_instance_id`;
missing, null, object, and empty `output`; non-dict and untyped output items;
message without content; null, numeric, blank, and whitespace content;
unsupported-kinds-only; reasoning-only; malformed content part lists. Every
case yields a non-`PASS` status, no candidate text, no proof, no reference, a
safe error code, and no exception.

### Tests changed rather than added

Seven assertions encoded the pre-C5 rule that the authority decision overturns.
They were re-aimed at the corrected contract, not deleted:

| Test | Was | Now |
| --- | --- | --- |
| `test_ordinary_completion_is_accepted` | required a reference | live stateless shape passes with a null reference and a named proof |
| `test_missing_terminal_completion_evidence_rejects` | absent `status` rejected | renamed `test_absent_terminal_status_is_accepted` |
| `test_missing_completion_evidence_rejects` | absent id rejected | renamed `test_absent_completion_identifier_is_represented_not_rejected` |
| `test_receipt_is_evidence_bound` | every receipt field truthy | the proof must be bound; the reference is asserted present-and-null |
| `test_missing_completion_evidence_yields_no_success` | absence failed the turn | renamed `test_absent_provider_identifier_still_completes_the_turn` |
| `test_no_evidence_identifier_is_synthesized_from_the_request` | asserted no receipt | asserts a receipt with no invented reference anywhere |
| `test_valid_evidence_still_succeeds` | evidence without a proof | the synthetic provider now declares `provider_assigned_completion_id` |

`chat_response` in `support.py` now defaults to the live stateless shape (no
`status`, no `id`, with `stats`), so the end-to-end suite exercises the real
contract; tests that need either field pass it explicitly.

### Live LM Studio smoke — performed 2026-08-14, full turn PASS

Same environment as C4 (LM Studio at `127.0.0.1:1234`, `granite-4.0-h-micro`,
loaded context `1048576`, repository synthetic protected-policy fixture,
`requested_tokens: 16384`).

```text
BOOT: OK   model_instance_id: granite-4.0-h-micro   context_budget: 16384
TURN:  status: PASS   safe_error_code: None   model_invoked: True   tool_executed: False
       public_output: Greetings! How can I assist you today?
RECEIPT:
  provider_id                       : lm_studio_native_rest_v1
  model_instance_id                 : granite-4.0-h-micro:2
  canon_projection_digest           : 103e0e2dd94183c914dc8c46e3ac376af516382548e17af40c14c27d3319f142
  provider_completion_evidence_ref  : None
  provider_completion_proof         : synchronous_provider_response
```

The full ordinary-turn path — ingress, control, envelope, live inference,
normalization, egress, terminal packet, receipt — completes against the real
provider. The receipt records the observed instance ordinal, states its proof,
and claims no provider identifier.

The one deviation from the operator's `smoke.runtime.json` is
`requested_tokens`: 4096 cannot carry the ~8,021-token frozen envelope (C4
finding 1), so 16384 was used. That remains a configuration decision for the
operator; no code compensates for it.

### Suites and validators after C5

| Suite | Result |
| --- | --- |
| Runtime Phase 1 | **190 OK** (was 175) |
| Security | **50 OK** |
| Readiness | **53 OK** |
| Continuity | **58 OK** |

Eight validators pass; `validate_host_adapter_contracts.py` still reports the
known BC-020 fixed-base finding. The readiness and continuity validators report
only the two untracked local smoke artifacts described under C4
(`smoke.runtime.json`, `src/blu_runtime.egg-info/`); with both moved aside they
pass, and both were restored.

Envelope `36887` bytes, digest
`103e0e2dd94183c914dc8c46e3ac376af516382548e17af40c14c27d3319f142`, final byte
`0x5D`. Architecture 7 / 8 / 9. Golden CTS zero non-`OK` lines. `store: false`,
stateless provider behavior, no durable continuity, `SecurityDecision`
vocabulary, protected ingress/egress semantics, authorization-date enforcement,
`/exit` and `/quit` ordinary-ingress behavior, and the `00_Instructions.md`
exclusion are all unchanged.

### Remaining risks

- The instance-ordinal rule is inferred from live observation, not from
  published LM Studio documentation. If LM Studio ever answers with an
  unrelated instance identity format, turns fail closed with
  `PROVIDER_IDENTITY_MISMATCH` rather than accepting the wrong model.
- `PROVIDER_ERROR_REPORTED` is still not used for HTTP-level provider errors
  (C4 finding 2): an error body returned with an HTTP error status is reported
  as `PROVIDER_ENDPOINT_UNAVAILABLE`. Unchanged in C5; it is a classification
  defect, not a truth defect, and belongs to its own bounded correction.
- The terminal-state vocabulary (`TERMINAL_COMPLETION_STATES` and friends)
  remains an assumption for providers that do assert a state. Native v1 never
  exercises it, so it stays unconfirmed by live evidence.
- Only one provider profile exists, so `synchronous_provider_response` is
  correct for it by construction. A future provider that does assign ids must
  declare `provider_assigned_completion_id`; nothing in the runtime prevents a
  future adapter from declaring the weaker proof incorrectly, so adapter
  review remains the control there.

## BC-050-C5A correction pass

Micro-correction closing the two malformed-response holes Blu's bounded review
found in C5. Correction base `374cc29da43d104f7ed6e9628e3fd8ebe9c4ff25`, branch
`bc-050-c5a-completion-failclosed`. One production file changed:
`src/blu_runtime/providers/model/lm_studio.py`. C5's live-success contract is
untouched.

### Blocker 1 — `model_instance_id` is required

Was:

```python
instance_id = document.get("model_instance_id") or document.get("model")
```

A response could omit the instance identity entirely and still be accepted by
echoing back the `model` the request had asked for. That echo says nothing
about which loaded instance answered, so it was never identity evidence. The
fallback is removed; `model_instance_id` must be present, a string, and
non-blank after trimming. Nothing is synthesized, coerced, or inferred from
another field, and the falsy-value bug in the old `or` chain goes with it — a
blank identity no longer silently reaches the second operand.

Trimming is used only to test blankness. The value itself is compared as the
provider sent it, so `_instance_identity_agrees` still decides expected-model
and loaded-instance consistency exactly as C5 established it.

### Blocker 2 — every asserted completion id is validated before selection

Was: the scan returned the first usable identifier, so
`{"id": "good", "response_id": 7}` passed on the readable half. Now the loop
validates every field the provider asserted — each must be a non-blank string —
and only then selects, in the declared order `id`, `response_id`,
`completion_id`. A response that is internally inconsistent about its own
completion fails closed with `PROVIDER_COMPLETION_EVIDENCE_MISSING` rather than
having the inconsistency hidden.

Absence is still absence: when none of the three fields is present, the
stateless path is unchanged — reference `None`, proof
`synchronous_provider_response`, completion valid. No coercion, no synthesis,
no silent discard, and `model_instance_id` is still never relabelled as a
completion identifier.

### Regression tests (+17, runtime 190 -> 207)

`InstanceIdentityIsRequiredTests` (6): missing identity; `model` present with
no `model_instance_id`; `model` unable to rescue seven malformed identity
values; thirteen malformed identity types including `None`, empty, whitespace,
`0`, `7`, `True`, `False`, `1.5`, lists, and dicts; the valid live identity
still completing; and expected-model consistency unchanged.

`AssertedCompletionIdentifierTests` (11): all five mixed-validity payloads the
assignment names, plus whitespace and boolean siblings; no-identifier,
one-identifier, and multiple-valid-identifier cases preserved; deterministic
selection pinned in field order (`id` first, `response_id` when `id` is
absent); and a rejected identifier set proven to yield no candidate text and no
output kinds.

### C5 live-success behavior confirmed intact

The C5 shape still normalizes to a valid synchronous completion with extracted
content, an absent provider reference, no fabricated id, and neither
`PROVIDER_COMPLETION_UNVERIFIED` nor `PROVIDER_COMPLETION_EVIDENCE_MISSING`.
`store` remains `false`.

Live LM Studio smoke re-run 2026-08-14 after the tightening (same environment,
synthetic protected-policy fixture, `requested_tokens: 16384`):

```text
TURN:  status: PASS   safe_error_code: None   model_invoked: True
       public_output: Greetings! How may I assist you today?
RECEIPT:
  model_instance_id                 : granite-4.0-h-micro:2
  provider_completion_evidence_ref  : None
  provider_completion_proof         : synchronous_provider_response
```

### Suites and validators after C5A

| Suite | Result |
| --- | --- |
| Runtime Phase 1 | **207 OK** (was 190) |
| Security | **50 OK** |
| Readiness | **53 OK** |
| Continuity | **58 OK** |

Envelope `36887` bytes, digest
`103e0e2dd94183c914dc8c46e3ac376af516382548e17af40c14c27d3319f142`, final byte
`0x5D`. Architecture 7 / 8 / 9. Golden CTS zero non-`OK` lines. OPSEC oracle,
differential suites, `SecurityDecision` vocabulary, protected ingress/egress
semantics, authorization-date enforcement, `/exit` and `/quit` ordinary-ingress
behavior, C5's synchronous stateless proof, and `store: false` all unchanged.
Eight validators pass; `validate_host_adapter_contracts.py` still reports the
known BC-020 fixed-base finding, and the readiness/continuity validators still
report only the two untracked local smoke artifacts recorded under C4.

### Remaining risks

- Unchanged from C5: the instance-ordinal rule is a live-evidenced inference,
  HTTP-level provider errors are still classified
  `PROVIDER_ENDPOINT_UNAVAILABLE` rather than `PROVIDER_ERROR_REPORTED`, and
  the terminal-state vocabulary stays unexercised by this provider.
- Blocker 2 rejects a response that asserts one usable and one malformed
  identifier. If some future LM Studio build emits a null placeholder beside a
  real id, that response now fails closed rather than being read past. That is
  the intended direction under this assignment, and it would surface as a
  live-smoke observation rather than as silent acceptance.
