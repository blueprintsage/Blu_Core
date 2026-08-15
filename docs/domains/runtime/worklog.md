# Runtime Worklog

## 2026-08-14 — BC-050 final authority reconciliation and freeze

Codex reconciled final review record
`31476a1309589a989d709e45cb8c0fbdce2f7e6a` under Dad/Blu's clarified
authority. The malformed-`stats` finding is no longer blocking because LM
Studio native-v1 synchronous stateless `stats` is non-authoritative telemetry
and no BC-050 authoritative claim depends on it. The historical reproduction is
retained as a note; no production runtime change was authorized or made.

C5A target `ed76f311976fba62e26356af6c4e145aa8ee2d6e` remains independently
closed on its two real fail-closed targets: mandatory native-v1
`model_instance_id` with no `model` fallback, and validation of every asserted
completion-ID field before selection. The valid no-ID synchronous response
still fabricates nothing and retains `store:false`.

Dad/Blu's real local ordinary-turn evidence is recorded as
`live_lm_studio_smoke: PASS`. Final disposition is `approve-with-notes` and
BC-050 is accepted and frozen as the completed Phase-1 experimental/local
slice.

The assignment record, final review, handoff, validation, global assignment
index, runtime decision/failure/next-step continuity, and documentation index
were reconciled. ChatGPT Custom GPT is recorded as Blu's mandatory primary,
family-facing deployment and next active workstream. Python/LM Studio is
secondary local capability and portability only. No Python Phase 2, further
parity, runtime expansion, continuity, Auth, tools/MCP, artifacts, Custom GPT
implementation, or ComfyUI work was started.

Validation: `git diff --check` passed; exact committed golden blobs matched all
eight `SHA256SUMS` entries; readiness and continuity manifest checks returned
zero errors over 312 staged entries; and all nine repository validators passed
against a raw staged-blob snapshot. The direct Windows checkout and the first
`git archive` snapshot materialized CRLF golden Markdown and reproduced the
known checksum limitation, so neither was misreported as a golden defect and no
golden file was normalized. Runtime suites were not rerun because no runtime,
test, contract, or readiness behavior changed.

## BC-050-C5A — Completion Evidence Fail-Closed Micro-Correction

Blu's bounded C5 review found two malformed-response holes. `model_instance_id`
could fall back to `model`, so a response that never said which loaded instance
answered was accepted for echoing back the requested model; the fallback is
removed and the field must be a non-blank string. Completion-evidence
validation stopped at the first usable identifier, so a provider asserting
`{"id": "good", "response_id": 7}` had its inconsistency hidden; every asserted
identifier is now validated before one is selected, in the declared order.

Absence is still absence -- no identifier fields means a null reference, the
`synchronous_provider_response` proof, and a valid completion. C5's live
success path is untouched, and the live smoke re-run after the tightening still
returns PASS with a truthful receipt.

Runtime tests 190 -> 207. Security 50, readiness 53, continuity 58. Envelope,
golden CTS, architecture 7/8/9, and the frozen invariants unchanged.

## BC-050-C5 — LM Studio Native-v1 Completion Proof Correction

C4 got Blu to the terminal loop; the first live turn then failed with
`PROVIDER_COMPLETION_UNVERIFIED` after the model had already answered. The real
native-v1 stateless response carries `model_instance_id`, typed `output`, and
`stats` — no terminal `status`, no per-completion identifier, and an instance
ordinal (`granite-4.0-h-micro:3`) the inventory does not report. The C3
boundary required all three, so all three were corrected in one pass rather
than exposing the same rejection one step later.

Completion is now established from the response the provider actually returns:
valid structure, consistent instance identity, supported typed output, usable
assistant content, and no provider or transport failure. A terminal state is
honoured when present and not required when absent.

Absence of a provider completion id is stated rather than papered over.
`TurnReceipt.provider_completion_evidence_ref` is nullable and a new
`provider_completion_proof` names what the receipt rests on —
`provider_assigned_completion_id` or `synchronous_provider_response`. Nothing
is fabricated: no uuid, no hash, no coercion, no request-id fallback, no
`model_instance_id` relabelling, and `store` stays `false`. B-07 is intact
where evidence is asserted, and a result claiming no proof still cannot become
a successful turn.

Live smoke, full ordinary turn: `Hey, Blu.` -> `Greetings! How can I assist you
today?`, receipt with instance `granite-4.0-h-micro:2`, null provider
reference, and `synchronous_provider_response` proof.

Suites: runtime 190, security 50, readiness 53, continuity 58. Envelope 36887
bytes and digest `103e0e2d` unchanged, architecture 7/8/9, golden CTS
unmodified, known BC-020 fixed-base finding preserved.

## BC-050-C4 — Live LM Studio Provider-Contract Correction

The first real live LM Studio smoke failed at boot with
`UNAVAILABLE PROVIDER_MODEL_ABSENT` while the endpoint was reachable and
`granite-4.0-h-micro` was loaded. Two adapter field assumptions were wrong:
native v1 identifies a model record with `key`, not `id`, and reports the
loaded instance's capacity at `loaded_instances[].config.context_length`, not
`loaded_instances[].context_length`. The second defect was latent behind the
first.

`src/blu_runtime/providers/model/lm_studio.py` is the only production file
changed. Identity matching stays exact — display names and a record-level `id`
cannot claim a configured key — and the record-level `max_context_length` is
treated as model capability, never as loaded-instance capacity. Every
fail-closed capacity path is preserved and 13 live-shape regression tests were
added.

Live smoke after the fix: boot passes the provider boundary with observed
context `1048576`. The turn then fails further down and was deliberately not
corrected here — the frozen envelope is ~8,021 prompt tokens against the smoke
config's 4,096-token request, and the live chat response carries no `status`,
no top-level `id`, and an instance identity (`granite-4.0-h-micro:2`) that
differs from the inventory's. Those are recorded for a separate assignment.

Suites: runtime 175, security 50, readiness 53, continuity 58. Envelope 36887
bytes and digest `103e0e2d` unchanged, architecture 7/8/9, golden CTS
unmodified, known BC-020 fixed-base finding preserved.

## BC-050-C3 — Final Independent Re-Review Micro-Correction

Codex's second review (`157441d`) closed B-02 through B-05 and left three narrow
defects, all corrected on `bc-050-c3-final-micro-correction`.

B-01: the authorization date is bound to the exact approved value `2026-08-12`
in all three validators. Codex showed that cross-file equality accepted the same
wrong date everywhere; nine wrong dates written consistently into both readiness
records are now rejected by every validator independently. The shared predicate
and its six constants remain byte-identical.

B-06: the startup banner no longer claims `/exit` ends the session. It names
end-of-input, the mechanism the host adapter actually implements. No `/exit`
interception was restored.

B-07: malformed `completion_evidence_ref` types fail closed at the evidence
boundary. Codex's integer reproduction previously raised `AttributeError` from
`.strip()`; it now yields one deterministic terminal failure. No `str()`
coercion, because coercion would fabricate evidence from invalid input.

`src/blu_runtime/__main__.py` is the only production file changed. Suites:
runtime 162, security 50, readiness 53, continuity 58. Envelope, golden,
architecture, and OPSEC oracle unchanged; differential clean over 40,000 fresh
cases. Known BC-020 finding preserved.

## BC-050-C2A — Instruction-Layer Classification Cleanup

Dad/Blu resolved B-02 by correcting a source-classification premise rather than
by accepting a false equivalence. `00_Instructions.md` remains immutable
historical CTS deployment provenance but is no longer successor invariant canon,
no longer a required Python model-facing source, and no longer a
cross-deployment parity source.

The reasoning is that the instruction surface primarily stabilized a hosted
model that was not running Blu's deterministic architecture. Instruction text was
used to attempt persistence inside that model, and persistence cannot be assumed
from instruction text alone. Appearing in that surface is therefore not evidence
that a behavior is invariant Blu canon.

CANON-001 moved out of the invariant mappings into
`legacy_deployment_artifacts`; CANON-006 no longer cites the instruction surface
as a security authority; the ChatGPT deployment projection no longer requires
"deployment instruction plus six golden capsules"; and the parity matrix gained
an explicit non-parity rule for deployment-local mechanics while keeping all
eleven real parity dimensions.

C2-AC-01 and C2-AC-02 are resolved. No third prompt, no generated projection, no
semantic judge, no Verb Lock subsystem, no golden change, no envelope change, and
no `src/blu_runtime/**` change. Seventeen negative tests prevent the
classification from being reverted. Suites: runtime 154, security 50, readiness
53, continuity 58.

## BC-050-C2 — Independent Review Blocker Correction

Codex returned BC-050 for correction at `33be23a` with blockers B-01 to B-07.
Six are corrected on `bc-050-c2-review-blockers`; B-02 is escalated.

B-01 replaced three divergent authorization predicates with one byte-identical
fail-closed predicate. Codex demonstrated eight mutations that some validators
accepted; the matrix now runs 22 mutations against each validator independently
with zero acceptances. B-03 requires positive chat-compatibility evidence.
B-04 establishes terminal completion before any candidate text is read. B-05
publishes the canonical candidate on CLEAR. B-06 removed the in-band `/exit`
and `/quit` bypass so slash commands run the full turn. B-07 removed the
synthesized completion-evidence fallback in both the provider and the
orchestrator.

B-02 could not be closed. Exact search confirms Verb Lock's verbs appear zero
times in Persona and Operations Law, and several Execution Law, Compliance
Gate, and Completion Proof rules have no exact destination either. Two
authority contradictions, C2-AC-01 and C2-AC-02, are returned to Dad/Blu with
the smallest decision each requires. No golden canon was modified and no third
behavioral prompt was invented.

Suites: runtime 154, security 50, readiness 35, continuity 58, all OK. Envelope
digest and architecture unchanged. OPSEC oracle byte-identical; differential
re-run clean over 60,000 additional cases. The known BC-020 fixed-base
host-adapter finding is preserved unchanged.

## BC-050-C1 — Authorized-Implementation Validator Alignment

Bounded correction from `708101d7f6dfc7748bb69d71f56e4da1044a2699` on branch
`bc-050-c1-validator-alignment`, resolving BC-050 contradiction C-1 under an
explicit Dad/Blu collision-domain amendment.

The "no runtime implementation" rule lived in three validators. All three now
gate on the same explicit BC-050 authorization evidence; absent that evidence,
every guard keeps its pre-implementation behavior. The OPSEC conformance oracle
was proven byte-identical across twelve functions and six constants, and the
full differential-equivalence suite was re-run unchanged.

Readiness `result_semantics` now reads
`python_phase1_implementation_authorized_and_active_pending_independent_review`,
which claims authorization and activity without implying completeness, review,
or integration. The internal `sys.path` mutation was removed from the runtime
test helper; imports now come from the external `PYTHONPATH=src` fallback.

All four suites pass: runtime 119, security 49, readiness 32, continuity 50.
Every applicable validator passes except the known BC-020 fixed-base
host-adapter finding, which reproduces at the authorized base. No production
`src/blu_runtime/**` file changed. BC-050 is ready for independent Codex review.

## BC-050 — Python Runtime Phase 1 (implementation, blocked on C-1)

Dad/Blu explicitly authorized BC-050 implementation on 2026-08-12 and moved
implementation ownership from Codex to Claude for BC-050 only. Independent
implementation review is assigned to Codex; Claude does not review her own
implementation.

Base `973589eea05fe42deeb829c5435bd09faf8cbe70`, branch
`bc-050-python-runtime-phase1`. First real Python Blu runtime: boot, portable
configuration, verified canon load, terminal ingress, pre-ingress restraint,
one-route Turn Controller, Model Execution Boundary, LM Studio binding,
untrusted response normalization, Validation and Egress, one terminal packet,
evidence-bound receipt. `tests/runtime_phase1` passes 119/119.

The frozen model-facing envelope reproduces its pinned digest
`103e0e2dd94183c914dc8c46e3ac376af516382548e17af40c14c27d3319f142` at 36887
bytes. Production OPSEC provenance is differential-equivalent to the BC-041-C1
reference across the full corpus and is bounded rather than quadratic
(6400 removals: 5.6 ms production vs 1376.7 ms reference).

**Blocked on contradiction C-1.** The "no runtime implementation" rule is
encoded in three validators, and BC-050's collision domain covers only one.
`tools/validate_opsec_contracts.py:652-655` (protected) and
`tools/validate_continuity_contracts.py:91-94` (out of domain) both reject the
authorized state. Recorded under the packet's §21 protocol rather than resolved
by editing a protected contract. See `assignments/BC-050/handoff.md`.

Separately recorded: `tools/validate_host_adapter_contracts.py` fails at the
authorized base as well, independent of BC-050.

status: active
owner: docs/domains/runtime
last_reviewed: 2026-08-12

## 2026-08-12 - BC-041 and BC-041-C1 final closure

### What changed

- Started the dedicated `bc-041-c1-closure` branch from fetched current
  `origin/main` at `131a527a8fef1f42df327443c9966c9e2f66f528`.
- Verified that current `main` already preserves and integrates the correction
  lineage through `204a229e2c01b255f1a940129cb724fa33fb4755`; no duplicate or
  rewritten correction merge was created.
- Imported Claude's final `review.md` byte-for-byte from
  `f0998f78aaada899a16d4413170ef3689f04fe28` in provenance commit
  `3e77111b6d86879f591c7ab8c52a571c51e7c48e`, without merging the review
  branch.
- Closed BC-041 and BC-041-C1 as `done`, preserving the original BC-041
  `return-for-correction` review and recording the final C1
  `approve-with-notes` disposition with zero blockers.
- Transitioned readiness from pending review/closure to independent review and
  Dad/Blu closure complete while keeping implementation authorization false and
  automatic start prohibited.
- Carried Claude N-1 and N-2 into the future runtime packet and recorded N-3 as
  pre-existing contract behavior. Added no runtime, provider, Auth, protected
  policy value, architecture change, continuity mutation, or PASS/SkillForge
  work.

### Final disposition

```text
B-1: resolved through BC-041-C1
B-1': resolved
B-1″: resolved
SUR-001: resolved_at_minimum_phase1_contract_level
technical readiness: ready_for_python_phase1
actual blockers: []
runtime_phase1_packet_may_be_authored_next: true
independent correction review: complete
implementation_authorized: false
automatic_start_prohibited: true
Python Runtime Phase 1: not started
```

Exact closure validation and commit receipts are recorded in the BC-041-C1
validation and handoff records. The next safe action is a separate Dad/Blu
runtime-packet decision; implementation must not start automatically.

Closure substantive commit:
`1eb33e898b91c5e0de88985ca44530498b255c32`.

## 2026-08-12 - BC-041-C1 B-1â€³ outer-edge correction

### What changed

- Started from the required B-1' metadata receipt
  `c6a447679c0ca07fb38a1e35eeb00231b0cb91e1`; Claude review commit
  `f87588d0fa094c203fde3b847ab9bc3c28d1b3fe` was used as evidence only and was
  not merged or cherry-picked.
- Preserved the one `Cf`-removed normalized candidate and added normalized
  boundary-offset metadata for every representable removed-`Cf` run. Whole
  phrase guards accept a real non-word boundary or such a retained offset;
  ordinary word adjacency without `Cf` provenance remains a nonmatch.
- Added bounded contiguous-run handling so unseparated repetition of the same
  protected rule fails safely without admitting unrelated prefix/suffix words.
- Expanded the synthetic matrix for all six code points at leading, trailing,
  and both outer edges at ingress and egress, plus outer/interior mixtures,
  mixed code points, repeated outer/interior insertions, and self-repetition.
- Documented intentional zero-space separator tolerance and the Phase-1
  exclusion for non-`Cf` default-ignorable/invisible characters.
- Added no production protected value, runtime/provider/Auth implementation,
  architecture change, continuity mutation, tool, or PASS/SkillForge path.

### Validation and next step

Focused OPSEC/readiness validation passed with 53 tests. A deterministic 54,740
probe adversarial run covering preserved interior combinations and new outer
edges had zero ingress/egress failures; six ordinary ASCII/Unicode adjacency
controls had zero false matches. Complete suite, manifest, golden,
publication-safety, repository-boundary, commit, and push receipts are recorded
in `assignments/BC-041-C1/validation.md` and `handoff.md` at handoff. The next
action is another independent Claude C1 review, not Python runtime
implementation.

### Commit identity

- Substantive outer-edge correction:
  `85e18f56f88ab113646cc3aab477687eda8b85af`.
- Metadata receipt: `d1c283ab21681f8a0550da32c2ec87e08eb2852d`.

## 2026-08-12 - BC-041-C1 B-1' mixed-placement correction

### What changed

- Started from the required first C1 metadata receipt
  `54519493189a332e984409504c45210e759f18fc`; Claude review commit
  `874852c1b548ba4a2539d796d23ab9d803a966c8` was used as evidence only and was
  not merged or cherry-picked.
- Superseded the incomplete exactly-two-static-views claim. The matcher now
  removes all general-category `Cf` characters into one normalized candidate
  and lets protected-rule inter-word separators match zero-or-more normalized
  spaces under Unicode word-token guards. Candidate count remains one for any
  insertion count.
- Expanded the synthetic matrix from two to three same-code-point position
  classes for all six required code points at both ingress and egress, and added
  cross-code-point mixed probes plus repeated/arbitrary placement mutations.
- Bound green technical readiness to the expanded OPSEC validator. The
  repository was marked not ready during active correction and returned to
  `ready_for_python_phase1` only after the corrected mechanism and expanded
  proof passed.
- Addressed Claude N-1 with opaque synthetic rule references, N-2 by digesting
  the sole candidate that produced the decision, and N-3 by separating
  `normalize_rule_text` from candidate normalization.
- Added no production protected value, runtime/provider/Auth implementation,
  architecture change, continuity mutation, tool, or PASS/SkillForge path.

### Validation and next step

Focused OPSEC and readiness validation passed. Complete suite, manifest,
golden, publication-safety, repository-boundary, commit, and push receipts are
recorded in `assignments/BC-041-C1/validation.md` and `handoff.md` at handoff.
The next action is a fresh independent Claude C1 review, not Python runtime
implementation.

### Commit identity

- Substantive mixed-placement correction:
  `2a9d6a28111ca9576bf6811e67ccca37f4d5dd39`.
- Metadata receipt: `c6a447679c0ca07fb38a1e35eeb00231b0cb91e1`.

## 2026-08-11 - BC-041-C1 Unicode format-character correction

### What changed

- Closed BC-041 B-1 in the public minimum matcher by deriving exactly two
  deterministic candidate views for every ingress and egress candidate:
  Unicode general-category `Cf` mapped to ASCII space and `Cf` removed.
- Required both views to traverse the existing normalization pipeline and made
  a match in either view sufficient. Egress redaction rescans both views and
  fails closed when divergent matching views cannot share one safe span set.
- Added the required 24-case synthetic matrix: six approved `Cf` code points,
  two positions, and both ingress and egress. The five existing negative
  ingress fixtures remain explicit regression cases.
- Named general Unicode confusable/homoglyph substitution as outside the
  minimum matcher instead of misclassifying it as semantic paraphrase.
- Replaced the ambiguous passing review-required check with a finite
  `required_pending` correction-review state, while preserving technical
  readiness and explicitly keeping implementation unauthorized.
- Added no production protected value, runtime, provider, Auth, architecture,
  continuation, tool, continuity, or PASS/SkillForge implementation.

### Validation and next step

Focused OPSEC and readiness validation passed during implementation. Complete
suite, manifest, golden, publication-safety, commit, and push receipts are
recorded in `assignments/BC-041-C1/validation.md` and `handoff.md` at handoff.
Claude next performs the independent C1 review; Dad/Blu decide integration and
closure. Python Runtime Phase 1 remains unauthorized.

### Commit identity

- Substantive correction:
  `80e5b8554639c274f7baa69155ea9b83910f604c`
- Metadata receipt: reported externally after creation.

## 2026-08-11 — BC-041 minimum OPSEC contract

### What changed

- Added public minimum OPSEC mechanism, policy/evaluation schemas, portable
  environment-file policy reference, deterministic normalization/matching,
  ingress and egress mappings, redaction postconditions, safe evidence, and
  error codes under `contracts/security/opsec/`.
- Added an explicitly synthetic policy/case matrix plus a nonproduction
  conformance harness and focused tests. No production protected value or
  machine-local policy binding was added.
- Re-evaluated SUR-001 to
  `resolved_at_minimum_phase1_contract_level` and Python readiness to
  `ready_for_python_phase1`; the runtime packet may be authored next but does
  not start automatically.
- Preserved Auth separation, SUR-002/SUR-011/SUR-012, the one-route slice, and
  the 7/8/9 successor architecture. Added no runtime/provider implementation,
  tools, continuity mutation, or PASS/SkillForge path.
- Narrowed the continuity validator's fixed-base protected-register exception
  to the exact BC-041 SUR-001 resolution shape; every other successor-register
  item and top-level field must remain byte-equivalent in meaning, and the
  existing protected-path guard remains active. A focused Git-backed regression
  test proves the exception accepts only that exact resolution and still rejects
  an adjacent SUR-002 mutation.

### Validation and next step

Focused OPSEC validation and 22 tests passed during implementation. Complete
suite, manifest, golden, publication-safety, commit, and push receipts are
recorded in `assignments/BC-041/validation.md` and `handoff.md` at handoff.
Claude performs the independent semantic review; Dad/Blu decide integration and
any later Python Runtime Phase 1 authorization.

### Commit identity

- Substantive security-contract work:
  `9ccd17d75955db4b64e5df27a5751d36b6964330`
- Metadata receipt: reported externally after creation.

## 2026-08-11 — BC-040 final closure

### What changed

- Closed BC-040 administratively from exact reviewed/integrated base
  `8801ae138deb0261deff47d02269c7a16773c892` on branch
  `bc-040-closure`.
- Recorded the complete lineage: original base
  `66e7ed52f5777bdef2e32c71a5e83b439b0d0ade`, substantive specification
  `8516bd6845edaa3ef9b18077d91853ccc21e3c3b`, metadata
  `dc5429cabf03aff4ea8b383cbc1290789c370ebb`, work integration
  `a24cffc2fb3b3b7ffe3e0291915d0319a4db3e5f`, Claude review
  `127ae61e296fe0d07072e1320dec8ca8c4b1dfed`, and reviewed integration
  `8801ae138deb0261deff47d02269c7a16773c892`.
- Recorded Claude's `approve-with-notes` disposition, zero blocking findings,
  and all ten nonblocking implementation/hardening notes at their future
  targets.
- Regenerated the canonical manifest after the immutable Claude review changed
  a tracked file.
- Added no production runtime, LM Studio provider, Local Mirror provider,
  protected policy value, adapter implementation, or PASS/SkillForge work.

### Final result and next safe step

- BC-040 status: `done`.
- One-Blu portability/readiness specification: complete.
- Required deployments: ChatGPT Custom GPT and Python/LM Studio.
- Optional best-effort deployment: Codex; it remains non-driving and
  nonblocking for Python.
- Final readiness: `not_ready_for_python_phase1`.
- Sole actual blocker: SUR-001, the unavailable minimum OPSEC match/redaction
  contract for arbitrary natural-language ingress and egress.
- Next separately authorized assignment: `Protected Security Phase 1 — Minimum
  OPSEC Match and Redaction Contract`.
- Python Runtime Phase 1 remains unauthorized. Its conditional future packet is
  `Python Runtime Phase 1 — Boot + Ordinary Turn + LM Studio Model Boundary`.

### Validation and receipts

Exact final commands, suite counts, manifest coverage, golden CTS results,
architecture counts, protected-boundary checks, limitations, and commit
receipts are recorded in `assignments/BC-040/validation.md` and `handoff.md`.
Substantive administrative closure commit:
`d78f58972327434c83d7e79a2cb9372e487a9629`.

## 2026-08-11 — BC-040 One-Blu portability and readiness

### What changed

- Defined one canonical behavioral source mapping across required ChatGPT and
  Python/LM Studio deployments; Codex remains optional best effort.
- Recorded official LM Studio v1 model inventory and chat evidence and froze a
  non-streaming, `store=false`, operator-loaded-model Phase 1 profile.
- Froze a normal `src/blu_runtime/` layout contract, portable configuration,
  provider-neutral model boundary, one-route ordinary-turn slice, parity
  scenarios, all 28 implementation-gap dispositions, and all successor blocker
  dispositions.
- Tightened continuity schemas for mutation requests, action/expected-version
  binding, `not_found`, portable references, non-completed outcomes, and
  receipt-only availability probes.
- Selected `jsonschema==4.26.0` Draft 2020-12 validation and added real instance
  fixtures plus Git-backed scope/manifest regression tests.
- Added no production runtime, LM Studio client, Local Mirror provider, tool
  execution, CLI, daemon, UI, or PASS/SkillForge integration.

### Result and next step

- Preliminary result: `not_ready_for_python_phase1`.
- SUR-001 is the only actual blocker. Explicit protected routes can be absent,
  but an arbitrary ordinary-language turn can still request protected source;
  a real local-model turn therefore requires a separately authorized minimum
  OPSEC match/redaction contract.
- After full validation, commit and push the BC-040 specification for Claude
  review. Do not begin Python Runtime Phase 1.

### Commit identity

- Substantive specification:
  `8516bd6845edaa3ef9b18077d91853ccc21e3c3b`
- Metadata receipt: this follow-up; reported externally after creation.

## 2026-08-05 — Bootstrap

- Created the domain continuity lane.
- No implementation work has begun.

## 2026-08-05 — BC-010 runtime contract extraction

### What changed

- Extracted downstream machine-readable contracts for the v0.22.0 golden
  Markdown runtime under `contracts/runtime/`.
- Added source provenance, component and route registries, five JSON Schemas, a
  behavioral parity matrix, and an unresolved register.
- Added standard-library-only validation tooling and contract fixtures/tests.
- Added the extracted contract set to the documentation index.
- Did not add runtime behavior or modify the golden kernel.

### What was tested or reviewed

- Read all seven authoritative golden runtime files in full.
- Ran `python tools/validate_runtime_contracts.py`.
- Ran `python -m unittest discover -s tests/contracts -p "test_*.py"`.
- The initial validator and four tests passed.
- Final structural validation passed.
- Final unit validation passed: 4 tests.
- `git diff --check` passed (Git reported only expected LF-to-CRLF working-copy
  warnings for modified Markdown files).
- `git diff --exit-code 7aed76e -- kernel/golden/v0.22.0` passed.
- PowerShell SHA-256 verification passed for all seven Markdown files and the
  source ZIP listed in `SHA256SUMS`.
- `git merge-base --is-ancestor 7aed76e HEAD` passed at pre-commit HEAD
  `3c421914d2b449f63f9b7ba73e24cc59539c1c3b`.
- The contract set contains 41 registry components, 6 live slash stems, 69
  source-map entries, 22 unresolved items, 12 parity requirements, and 34
  parity cases.

### What worked

- Every JSON file parsed.
- Source-map targets and sections resolved.
- Component IDs were unique within namespace after repeated StateTree
  declarations were represented by one unresolved registry identity.
- Every live public command stem had one owner.
- The validator failed in tests when a required contract was removed or JSON
  was malformed.

### What failed

- The host did not provide `sha256sum`; an equivalent PowerShell
  `Get-FileHash -Algorithm SHA256` check was used successfully.
- The optional third-party `jsonschema` package was not installed. Validation
  remains dependency-free and covers the JSON Schema subset used by BC-010.

### Known risks

- Several mandatory runtime owners are referenced but not defined by the seven
  golden files; they remain `declared_but_not_defined`.
- StateTree has conflicting `ALPHA` and `ACTIVE` declarations.
- The `/memory` route uses `lane_class=workflow`, which is absent from Exec's
  declared lane-class list.
- Schema fields for task packets and capability reports are not declared by the
  golden source, so those schemas intentionally assert object shape only.
- Contract/schema validity is not behavioral parity or host-capability proof.
- The assignment packet requires one work commit and also requires that exact
  commit ID to be stored inside `docs/worklogs/assignments.md` in that same
  commit. A Git commit cannot contain its own hash because changing the file
  changes the tree and therefore the hash.

### Next safe step

- Request Claude's read-only semantic review against the seven golden files at
  work commit `40138b6e16f28c01904aae97158878468ee47ad0`.

### Files changed

- `contracts/runtime/**`
- `tools/validate_runtime_contracts.py`
- `tests/contracts/**`
- `docs/dev/docs_index.md`
- `docs/domains/runtime/worklog.md`
- `docs/domains/runtime/failures.md`
- `docs/domains/runtime/next_steps.md`
- `docs/worklogs/assignments.md`

### Commit or patch identity

- Work branch: `bc-010-runtime-contracts`
- Work commit: `40138b6e16f28c01904aae97158878468ee47ad0`
- Record commit: this authorized metadata-only follow-up; its exact SHA is
  reported externally because a commit cannot contain its own final hash

## 2026-08-05 — BC-010-C1 runtime contract extraction corrections

### What changed

- Separated the deployment instruction from the six kernel/runtime capsules in
  source mapping and documentation.
- Added the three missing non-slash routes and both deployment-level exclusive
  dispatch constraints.
- Added omitted referenced components and declared macro identifiers without
  inventing implementations, stable IDs, or render text.
- Replaced fragment-only source citations with exact Markdown heading anchors
  plus scoped exact locators where a file lacks doctrine subheadings.
- Corrected PASS, dependency, StateTree, schema-closure, parity-provenance, and
  extraction-inference representations.
- Replaced the permissive schema checker with a strict documented subset
  validator and canonical positive/negative fixture validation.
- Backfilled BC-010 assignment and validation records and created the approved
  BC-010-C1 assignment quartet.
- Restored runtime-contract discovery in the documentation index.

### What was tested or reviewed

- `python tools/validate_runtime_contracts.py` passed during implementation.
- `python -m unittest discover -s tests/contracts -p "test_*.py"` passed 15
  tests during implementation.
- Final Git, checksum, manifest, Python-version, and dependency receipts are in
  `assignments/BC-010-C1/validation.md`.

### What worked

- Every source-map entry resolves to one declared role and one exact heading.
- Unsupported schema keywords and unknown types fail clearly.
- All five positive fixtures pass and all five negative fixtures fail.
- StateTree remains `unresolved_conflict` with `ALPHA` and `ACTIVE` preserved.

### What failed

- No implementation path failed. The pre-existing untracked
  `.claude/settings.local.json` remains outside assignment scope and is not
  committed.

### Known risks

- Structural validation is not behavioral parity or runtime proof.
- Referenced components and macro identifiers remain undefined.
- Claude's second semantic review remains required.

### Next safe step

- Review the repair work commit read-only against the CTS source set, then let
  Blu or Dad decide integration. Do not begin BC-020 or BC-030.

### Commit or patch identity

- Repair work commit: recorded by the authorized metadata-only follow-up.
- Metadata record commit: reported externally after creation.

## 2026-08-06 — BC-010-C2 OPSEC route classification repair

### What changed

- Replaced the two unsupported `opsec` route lane values with null lane classes,
  explicit undeclared status, and UR-028.
- Marked the cross-role OPSEC owner join as extraction inference and added a
  dedicated source-map join entry preserving both source roles.
- Added route lane-class closure validation for Exec-declared lanes,
  unresolved route-table-only values, and source-proven null lanes.
- Separated component IDs from dependency prose in the three records identified
  by Claude's C1 review.
- Strengthened negative fixture reasons and added synthetic object-closure
  coverage.
- Recorded assignment lineage, the approved successor-runtime Auth/OPSEC
  decision, C2 assignment evidence, and C1 status cleanup.
- Did not modify the golden CTS source or implement runtime behavior.

### What was tested or reviewed

- Final exact command and checksum receipts are recorded in
  `assignments/BC-010-C2/validation.md`.

### What worked

- The validator rejects `opsec` and arbitrary invented lane classes.
- Declared `auth`, unresolved route-table-only `workflow`, and the two
  source-proven null OPSEC lane classes validate.
- All five canonical negative fixtures are asserted against their intended
  failure reasons.

### Known risks

- Contract validation remains structural and does not prove runtime behavior.
- The successor OPSEC decision is deliberately not represented as golden CTS
  provenance.

### Next safe step

- Claude performs a read-only semantic review of the C2 repair work commit;
  Blu or Dad decides integration. Do not merge or mark BC-010, BC-010-C1, or
  BC-010-C2 done.

### Commit or patch identity

- Exact base: `424f80b254a02f057da6c82db5230377076fc415`
- Branch: `bc-010-c2-opsec-route-repair`
- Repair work commit: recorded by the authorized metadata-only follow-up.

## 2026-08-06 — BC-010 lineage closed

- Dad and Blu authorized final closure.
- BC-010, BC-010-C1, and BC-010-C2 moved from review to done.
- Claude's final disposition was approve-with-notes with no blocking findings.
- Non-blocking notes remain preserved in the BC-010-C2 review record.
- Integrated reviewed state before closure:
  `8a37ae3c62829f16f949f5896d2bef0542721565`.
- No runtime contracts, validator code, tests, or golden sources changed.
+
## 2026-08-06 — BC-015 runtime viability audit

### What changed

- Created an evidence register, 30-record viability matrix, 24-probe safe host
  catalog, audit guide, and audit report under
  `docs/domains/runtime/viability/`.
- Covered all 47 component entries, 76 normalized route-surface entries, 12
  parity requirements, and 28 unresolved items.
- Classified no capability as `live_and_stable`; preserved Dad and Blu's
  Auth, OPSEC, and Persona warmth observations as
  `live_but_nondeterministic_or_host_dependent`.
- Kept current OPSEC behavior separate from the approved successor pre-ingress
  restraint.
- Recorded the v0.15.2 historical archive as unavailable without reconstructing
  its contents.
- Added standard-library-only validation and nine required negative tests.
- Added the BC-015 assignment quartet and documentation discovery.
- Did not implement runtime behavior or modify golden sources, runtime
  contracts, architecture, configuration, or runtime decisions.

### What was tested or reviewed

- Verified the exact base and clean startup state.
- Read the required governance, architecture, source, runtime continuity,
  extracted contract, prior review, and golden CTS inputs.
- Verified all eight golden checksum entries before audit work.
- `python tools/validate_viability_audit.py` passed.
- `python -m unittest discover -s tests/viability -p "test_*.py"` passed nine
  tests during implementation.
- Final Git, manifest, protected-path, contract, checksum, and unit-test
  receipts are recorded in `assignments/BC-015/validation.md`.

### What worked

- Mechanical coverage is complete and exact.
- Evidence and successor provenance remain separate.
- The validator rejects unknown classifications, missing evidence, incomplete
  coverage, duplicate IDs, invalid dispositions, declaration-only stable
  claims, incomplete historical evidence, and successor-as-golden projection.

### What failed or remains unavailable

- The historical v0.15.2 archive was unavailable.
- No current Blu GPT-host probe was executed; all 24 probes remain for Dad or
  Blu.

### Known risks

- Grouped records must not be interpreted as approval of current component
  topology.
- Proposed dispositions remain non-final.
- Auth and OPSEC details remain protected and require security-authorized
  specification work.

### Next safe step

- Claude reviews the BC-015 audit work commit read-only; Dad and Blu decide
  probe execution, historical-source reopening, and any successor
  specification assignment.

### Commit or patch identity

- Exact base: `4b51427b361283715a24110409e031e191b52452`
- Branch: `bc-015-runtime-viability-audit`
- Audit work commit: `9936cc4be2f7f397deebccdf7400e8b7b774df08`
- Metadata record commit: reported externally because a commit cannot contain
  its own final SHA

## 2026-08-06 — BC-015 runtime viability audit closed

- Dad and Blu authorized final closure of BC-015.
- Claude's semantic-review disposition remains `approve-with-notes`; all nine
  non-blocking findings are preserved and no blocking findings remained.
- The audit classified current viability and did not implement a runtime.
- Historical evidence was unavailable during BC-015. The broader historical
  archive source is introduced only through the separate BC-016 source-
  integration assignment and does not retroactively change the BC-015 record.
- Integrated main state before closure:
  `1f07333457b18895fbb04d5c776e3259d870f2f6`.

## 2026-08-06 — BC-016 historical archive inventory integration

### What changed

- Integrated 249 path-sanitized historical source records: 244 archives, three
  branch-root Markdown file sets, and two historical source folders.
- Independently verified the stable outer `Kernel.zip` receipt and confirmed
  all 279 snapshot payload files match the live historical root by relative
  path and SHA-256.
- Added two exact shared-SHA duplicate groups, 500 reconciliation entries, and
  eight representative milestones covering all requested structural eras.
- Added standard-library-only static validation and twelve tests.
- Preserved the current CTS authority boundary and imported no archive bytes.

### What was tested or reviewed

- Verified external JSON/CSV agreement and consumed all four discovery outputs.
- Recomputed live archive/file-set identities and compared them with the stable
  snapshot.
- Ran the historical inventory validator and twelve tests successfully during
  implementation; final full-repository receipts are in
  `assignments/BC-016/validation.md`.

### What worked

- All local paths were converted to approved source-root aliases plus relative
  paths.
- Snapshot, live root, and discovery identities remain distinct and explicit.
- Exact duplicate grouping now requires one shared canonical SHA-256.
- Two ambiguous external short-date parses were rejected rather than silently
  accepted.

### What failed or remains unavailable

- Seven Deflate64 archives cannot be decompressed by installed readers. Their
  central directories and archive hashes are available; integrity is
  `not_tested`.
- No historical behavior was executed or compared.

### Known risks and next safe step

- Marker prominence and implementation-style Markdown can be mistaken for
  behavioral proof; BC-017 must not make that inference.
- Claude performs a read-only semantic review of the BC-016 inventory work
  commit. Do not begin archaeology, BC-020, BC-030, or Python implementation.

### Commit or patch identity

- Exact base: `fdb6c7e150d3717172e08a1bc349a428187df45a`
- Branch: `bc-016-historical-archive-inventory`
- Inventory work commit: recorded by the authorized metadata-only follow-up.

## 2026-08-06 — BC-016 historical archive inventory closed

- Dad and Blu authorized final closure after Claude's review was integrated.
- Claude's disposition is `approve-with-notes`; no blocking findings remained,
  and BC-016 moved to `done`.
- All NB-1 through NB-10 remain preserved in the review record and carried
  forward under the runtime next-step boundaries.
- Inventory identities and the immutable current CTS authority boundary remain
  unchanged.
- No archive import, behavioral archaeology, or runtime implementation occurred
  during review integration or closure.

## 2026-08-07 — BC-017 historical behavioral archaeology

### What changed

- Re-derived 16 available version families and preserved explicit gaps.
- Selected readable family boundaries and focused change-point drilldowns.
- Separated current truth, owner observations, archive evidence, inference, and
  successor recommendations in a sanitized evidence register and report.
- Added a behavior-centered recovery matrix and transition map.
- Corrected BC-016 NB-1 and NB-4 without broadening the prior assignment.
- Added evidence-integrity validation and focused negative tests.

### What was tested or reviewed

- Checked canonical archive-ID resolution, path sanitization, evidence labels,
  recovery vocabulary, Faithfulness shipping status, payload exclusion, review
  state, and golden checksums.
- Re-ran the existing BC-016 inventory validator and tests after its two narrow
  evidence corrections.
- No historical behavior was executed; no Markdown declaration was treated as
  runtime telemetry.

### What worked

- Boundary-first analysis exposed Exec emergence, School's explicit state
  model, MMU introduction, reminder/time contracts, mega-Exec compensation, and
  v0.21 service decomposition.
- The archive evidence supports recovery of teaching/Persona guidance and thin
  deterministic contracts, not historical module restoration.

### What failed or remains unavailable

- Sixty-three members in seven Deflate64 archives remain unreadable.
- v0.4 boundary chronology, the v0.8 opening, durable host persistence,
  autonomous wake, and the Kiddo incident mechanism remain unproven.

### Known risks and next safe step

- Historical declarations may still be mistaken for working runtime behavior;
  the source-class labels and validator are mandatory safeguards.
- Claude performs a separate read-only semantic review. Dad and Blu decide
  integration. Do not start successor design, BC-018, BC-020, or BC-030.

## 2026-08-07 — BC-017-C1 archaeology review corrections

### What changed

- Removed systematic leading diff markers from the archaeology README and
  corrected its validator/test reproduction commands.
- Corrected the direct mega-Exec-to-contracted-Exec event from v0.20 to its
  evidenced v0.16.0 family.
- Kept later v0.20/v0.21 restructuring distinct and disclosed BC-016's
  different v0.21 structural-milestone framing.
- Preserved Claude's review and all non-blocking notes.

### What was tested or reviewed

- Re-ran all required repository validator/test suites, canonical manifest
  verification, golden checksums, protected-path checks, and the three manual
  acceptance checks.

### Known risks and next safe step

- The correction resolves record-production blockers only; it does not close
  BC-017 or convert green validation into semantic proof.
- Claude may perform a separately authorized read-only re-review of BC-017-C1.
  Dad and Blu decide integration and closure.

## 2026-08-08 — BC-017 and BC-017-C1 closed

### What changed

- Dad and Blu authorized final closure of BC-017 and BC-017-C1.
- The global assignment index and both assignment records moved to `done`.
- Claude's original `return-for-correction` review remains intact as audit
  history; C1 resolved B-01, B-02, and B-03.
- Claude's final C1 re-review at
  `bea9463f0dbbae1c3944c5f44a7843c757d7f0bb` remains
  `approve-with-notes` with zero blocking findings.
- The manifest was regenerated after the final review record and closure
  metadata changed.

### What was tested or reviewed

- Re-ran all four repository validator and unit-test suites.
- Verified canonical manifest bytes, all eight golden CTS checksums, protected
  paths, archive exclusion, publication safety, and PASS/SkillForge isolation.
- Exact commands and results are recorded in the BC-017 and BC-017-C1
  validation records.

### Known risks and next safe step

- All non-blocking archaeology-quality notes remain preserved; none is a
  closure blocker or an approved successor requirement.
- No assignment is currently eligible to start. BC-020 and BC-030 remain
  `spec-needed` and were not started.
- No archaeology, successor design, Python runtime, protected-source change, or
  modern PASS/SkillForge work occurred during closure.

### Commit identity

- Closure base: `b88902d997685057ee0e76709df7117f8a83f295`.
- Branch: `bc-017-closure`.
- Substantive closure commit:
  `b0182581c16bbb4dbeced715ae6e35bcee8bf097`.

## 2026-08-08 — BC-018 successor kernel boundary specification

### What changed

- Specified one seven-node successor graph: four deterministic core components,
  plus model-execution, generic host-adapter, and generic continuity-provider
  boundaries.
- Classified 37 required behaviors, decomposed Exec, defined eight packets,
  nine generic interfaces, six statuses, state lifetimes, source-grounding
  modes, and a dependency-ordered migration plan.
- Preserved OPSEC before ingress, bounded Auth to explicit evidence, and kept
  Persona, teaching, host services, and persistence in their proper authority
  domains.
- Rejected mega-Exec, School Engine, legacy PASS, dedicated Mood/MMU services,
  and the historical Faithfulness object model.
- Added machine-readable traceability and unresolved registers plus a
  standard-library design validator and negative tests.
- Created the BC-018 assignment quartet and marked the assignment `review`.

### What was tested or reviewed

- Exact command and result receipts are recorded in
  `assignments/BC-018/validation.md`.
- Validation covers all prior repository validators/tests, the BC-018 validator
  and negative suite, canonical manifest, golden checksums, and protected paths.

### What worked

- Every deterministic responsibility has one exclusive owner.
- Capability, time, scheduling, artifacts, and persistence require provider
  evidence rather than declaration.
- BC-020 and BC-030 both receive generic plug-in contracts and are
  `ready_for_spec` without being started.

### What failed or remains unavailable

- No runtime behavior, host adapter, scheduling, persistence, Auth, or OPSEC
  implementation exists.
- Protected Auth/OPSEC policy details, initial route catalog, semantic source
  verification, host receipt capabilities, and Local Mirror lifecycle remain
  explicit future questions.

### Known risks and next safe step

- Structured contracts can still be mistaken for execution; the design labels
  all components as specifiable, not implemented.
- Claude performs independent semantic review of the substantive work commit.
  Dad and Blu decide integration. Do not begin BC-020, BC-030, or runtime
  implementation.

### Commit identity

- Exact base: `a5e68b3189c60e2d5b8acbe8a212d69b720dec58`
- Branch: `bc-018-successor-kernel-boundary-spec`
- Substantive work commit: `a87e7d7ea57688212c7c8461b5630c6ddb55a00f`

## 2026-08-08 — BC-018-C1 pre-review terminal-authority correction

### What changed

- Defined successful host-session binding and unavailable binding as mutually
  exclusive Turn N terminal outcomes.
- Kept `SecurityDecision` at `PASS`, `BLOCK`, and `ASK`; provider-caused
  `UNAVAILABLE` is selected by Validation and Egress under the originating
  `SecurityDecision` before any `ControlDecision` exists.
- Made unbound proposed pending state inactive, non-resumable, and permanently
  non-correlatable by future host events.
- Updated packet, interface, error, architecture, validator, assignment, and
  continuity surfaces without changing the seven-component/eight-packet design.
- Added four focused negative tests while preserving the existing 35.

### Validation and next step

- Exact final suite, manifest, golden, and protected-path receipts are appended
  to `assignments/BC-018-C1/validation.md`.
- Claude may perform the separately authorized semantic re-review only after
  this correction is committed and pushed. Do not begin BC-020, BC-030, or
  runtime implementation.

### Commit identity

- Correction base: `b1e0f5c7ce3fddd7d71f6b2fa8050b0b55875b3c`
- Substantive correction commit: `311c572f3a28fe4e1cca04b75856faae3cfd6c60`

## 2026-08-08 — BC-018 pre-review contract correction

### What changed

- Corrected `TurnRequest` ownership so only Turn Controller produces it after a
  passing SecurityDecision; Host Adapter now owns only raw host-event
  translation.
- Defined one bounded pre-ingress Auth loop: safe ASK, explicit evidence,
  separate Auth evaluation, result returned to OPSEC, and PASS required before
  ordinary routing.
- Aligned components, packets, interfaces, traceability, graph, normative flow,
  boundary text, migration notes, and runtime decisions.
- Added focused validator invariants and four negative tests without changing
  the seven-component design or eight-packet set.

### What was tested or reviewed

- Exact final commands and results are recorded in
  `assignments/BC-018/validation.md`.

### What worked

- The validator rejects non-controller TurnRequest production, routing before
  SecurityDecision PASS, missing Auth re-entry, merged Auth/OPSEC ownership,
  and OPSEC placement behind Turn Controller.

### What failed or remains unavailable

- No implementation was attempted. Protected Auth/OPSEC policy and evidence
  details remain unresolved as designed.

### Known risks and next safe step

- This correction removes contract ambiguity only; it is not runtime proof.
- After push, Claude performs the independently authorized semantic review of
  the corrected BC-018 head. Do not begin BC-020, BC-030, or implementation.

### Commit identity

- Correction base: `ec4a3c14e6aedb7164fc500b0c9a31486bcd11e8`
- Correction substantive commit: recorded by the metadata-only follow-up

## 2026-08-08 — BC-018-C1 cross-turn security state correction

### What changed

- Replaced the ambiguous pre-ingress loop with an explicit Turn N / Turn N+1
  model and one terminal packet per host turn.
- Removed bare `session` from persistence lifetimes; all deterministic-core
  components are now turn-local, with cross-turn state accepted only from an
  evidenced `host_session` or explicit receipted continuity operation.
- Added `PendingAuthorizationState` as a state record while preserving seven
  components and eight packets.
- Separated attempt-policy authority (Security Restraint), evidence/result
  authority (Authorization Evaluator), and substrate/correlation evidence
  (Host Adapter).
- Required finite attempts, expiry, binding, replay rejection, fail-closed
  exhaustion, and explicit cancellation/reset behavior without publishing
  protected values.
- Bound `AuthorizationResult` validity to turn, evidenced host-session, or
  receipted durable-external scope; made ServiceExchange authority classes
  machine-checkable.
- Resolved directly related N1, N5, and N8 ownership, service-authority, and
  state-lifetime traceability notes.

### What was tested or reviewed

- All five repository validators passed.
- Unit suites passed: contracts 21, viability 9, historical archives 12,
  historical archaeology 18, successor kernel 35.
- The successor suite includes ten new required negative cases for bare
  session, missing substrate, two-terminal turns, expiry, finite attempts,
  replay, AuthorizationResult validity, pre-ingress service authority,
  duplicate attempt ownership, and Turn Controller cross-turn state.
- Final Git, manifest, golden, protected-path, and publication-safety receipts
  are recorded in `assignments/BC-018-C1/validation.md`.

### What worked

- The correction validates without an eighth component or ninth packet.
- BC-020 retains a coherent generic authorization-evidence target and BC-030's
  continuity boundary remains unchanged in authority.

### What failed or remains unavailable

- The first branch-creation attempt was denied Git metadata access before any
  checkout change; retry with the required repository permission succeeded.
- Exact protected attempt values, lockout/backoff rules, evidence classes,
  assurance thresholds, and host-specific binding mechanics remain future
  security/BC-020 inputs.
- No runtime, host adapter, Auth/OPSEC code, session store, persistence, or
  modern PASS/SkillForge work was implemented.

### Known risks and next safe step

- Static validation proves the declared structure, not host capability or
  runtime security behavior.
- Claude performs the separately authorized semantic re-review of the C1
  substantive commit. Dad and Blu decide integration. Do not begin BC-020,
  BC-030, or runtime implementation.

### Commit identity

- Exact base: `7796c7e738e0ff66b677c79314b80cf2bbb09a63`
- Branch: `bc-018-c1-security-state-correction`
- Substantive work commit: recorded by the metadata-only follow-up

## 2026-08-08 — BC-018-C1 closure-prep correction

### What changed

- Restored complete canonical manifest coverage, including `.gitattributes`,
  and added a narrow tracked-path completeness check to the successor validator.
- Corrected the Turn N+1 component graph so Host Adapter correlation returns to
  Security Restraint for attempt permission before Authorization Evaluator.
- Set SUR-012 `blocking_for_BC020` to `true` without changing SUR-002.
- Carried NN-4 to SUR-011 security-policy work and NN-5 to the BC-020/SUR-012
  host-evidence matrix without resolving either future policy question.
- Preserved Claude's review, the approved authority model, and all scope
  exclusions.

### Validation and next safe step

- Exact command, test-count, manifest, golden, count, and protected-path
  receipts are recorded in `assignments/BC-018-C1/validation.md`.
- BC-018 and BC-018-C1 remain in `review`. Dad and Blu decide closure; BC-020,
  BC-030, and runtime implementation remain unstarted.

### Commit identity

- Exact base / Claude review: `1f440546a076c9359afaf5e832882e588d71dfa6`
- Branch: `bc-018-c1-closure-prep`
- Substantive correction commit:
  `90e30c6d685eaa35c9bdf1a666179c9882877d85`

## 2026-08-08 — BC-018 and BC-018-C1 closed

### What changed

- Dad and Blu authorized final administrative closure from integrated main at
  `ce1cc235057a5de3d71fefbcee32e5617197cbb0`.
- BC-018 and BC-018-C1 moved from `review` to `done` in their assignment
  records and the global assignment index.
- The original BC-018 `return-for-correction` review remains immutable history.
  The final C1 re-review remains `approve-with-notes`, with BF-1, BF-2, and
  BF-3 resolved and zero blocking findings.
- Exact lineage through the specification, corrections, reviews, closure-prep
  correction, metadata, and main integration merge was recorded without
  rewriting history.
- Runtime next steps now identify BC-020 and BC-030 as `ready_for_spec` while
  retaining their global `spec-needed`, unstarted state.
- SUR-011 remains a future security-policy input. SUR-012 remains
  `blocking_for_BC020: true` for host-session evidence integrity and rollback
  resistance.
- The canonical manifest was regenerated after closure metadata changed.

### What was tested or reviewed

- Re-ran all five repository validators and unit-test suites.
- Verified complete canonical manifest coverage including `.gitattributes`,
  all eight golden CTS checksums, protected paths, architecture invariants,
  review-record immutability, publication safety, runtime non-implementation,
  and PASS/SkillForge isolation.
- Exact commands and results are recorded in the BC-018 and BC-018-C1
  validation records.

### Known risks and next safe step

- All Claude non-blocking notes remain preserved. Closure resolves none of the
  remaining future policy or host-specific mechanics.
- BC-020 and BC-030 may proceed only after Dad or Blu supplies a separately
  approved packet, named base, and owner. Neither assignment was started.
- No successor runtime implementation is authorized.

### Commit identity

- Closure base: `ce1cc235057a5de3d71fefbcee32e5617197cbb0`.
- Branch: `bc-018-closure`.
- Substantive closure commit:
  `373092e98fef4d291365462baaa7f1ea2a8f065b`.

## 2026-08-08 — BC-020 Chat and Codex host adapter contracts

### What changed

- Activated the Dad/Blu-authorized BC-020 specification from exact base
  `d4157e79fc7e2df6e1bd53b589cabfa19cd7238f` on branch
  `bc-020-chat-codex-adapter-contracts`.
- Added common capability, host-surface, receipt, error, host-session, replay,
  approval, and authorization-transport contracts under `adapters/`.
- Added independent Chat and Codex family/surface contracts, evidence registers,
  and normalized capability matrices covering input, retrieval, actions,
  filesystem/shell/network/Git, time, scheduling, continuity/session, security,
  and output.
- Added the cross-host security evidence matrix and resolved SUR-012 at the
  generic host-evidence contract level without claiming that current surfaces
  can satisfy it.
- Added focused adapter documentation, an offline structural validator, and 25
  negative/positive tests.

### Evidence and dispositions

- Used current first-party OpenAI documentation only for moving product claims;
  every such claim remains `documented_possible` rather than current runtime
  truth.
- Safely observed only the current Codex desktop local Windows binding. The
  snapshot proved bounded workspace/shell/Git/web/time/tool-interface operations
  and recorded their scope, freshness, receipts, and limitations.
- Dad's separate live Chat binding was not probed; its runtime statuses remain
  unknown unless a future adapter self-report supplies evidence.
- Product sign-in remains distinct from usable Blu Auth evidence; host approval
  remains distinct from Blu authorization.
- The current Chat binding is unknown for security-grade host-session evidence.
  The observed Codex binding is verified unavailable for protected cross-turn
  authorization continuation because it exposes no provider-backed replay/
  consumption state or monotonic rollback-resistant attempt state.
- SUR-011 remains unresolved security-policy input. BC-030 remains
  `ready_for_spec` because host-session and durable-external continuity remain
  separate.

### What was tested

- Focused BC-020 validator and 25-test suite passed before the complete
  repository validation run.
- Exact complete-suite, manifest, golden, protected-path, and publication-safety
  results are recorded in `assignments/BC-020/validation.md`.

### Limitations and next safe step

- Static validation proves contract coherence and guardrails, not a live
  provider guarantee, runtime implementation, or behavioral parity.
- The safe client-version probe could not execute the packaged Codex binary;
  client/surface version remains unknown rather than inferred from a path.
- After substantive and metadata commits are pushed, Claude performs the
  independent semantic review. Do not begin BC-030 or runtime implementation.

### Commit identity

- Exact base: `d4157e79fc7e2df6e1bd53b589cabfa19cd7238f`
- Substantive specification commit:
  `09c484418e51365cf9b156cf304eebae7fecde5d`
- Metadata receipt commit: reported externally because a commit cannot contain
  its own final SHA

## 2026-08-09 — BC-020-C1 scheduling capability evidence correction

### What changed

- Corrected `schedule.create`, `schedule.recurring`, and
  `schedule.update_cancel` from `verified_available` to `unknown` on the
  observed Codex surface while preserving scheduling-interface exposure.
- Expanded each row's limitations to separate interface presence from
  provider/account connection, permission, operational usability, operation
  success, future execution, and receipt availability.
- Carried the documented desktop-only limitation that future local scheduled
  execution may depend on the relevant machine and app remaining available.
- Hardened verified capability validation with a curated mapping from
  capability/status to existing `supports[]` tokens and `does_not_prove[]`
  boundaries.
- Added focused regression tests for the three scheduling rows and Claude's
  three demonstrated evidence-relevance defects.

### Evidence and counts

- Corrected Codex totals are 52 capabilities: 24 `verified_available`, 6
  `verified_unavailable`, 4 `documented_possible`, 17 `unknown`, and 1
  `not_applicable`.
- `schedule.receipt` remains `unknown`; scheduling operations remain
  receipt-required; the side-effect completion rule is unchanged.
- Codex evidence now has 22 entries after adding the narrowly scoped desktop
  scheduling limitation source.

### Boundaries and next safe step

- No schedule was created. No adapter, runtime, Local Mirror, BC-030, or
  successor architecture work was started.
- Claude's original BC-020 review remains byte-unchanged.
- Exact validation and commit receipts are in
  `assignments/BC-020-C1/validation.md` and `handoff.md`.
- Claude performs an independent semantic re-review of the C1 metadata head;
  Dad or Blu decides integration and closure.

## 2026-08-10 — BC-020 and BC-020-C1 closed

- Dad and Blu authorized final administrative closure from integrated `main`
  at `642a5df7340c4f87ac723bffb4d308fef09bf2b2`.
- BC-020 original work `09c484418e51365cf9b156cf304eebae7fecde5d`,
  metadata `ccf3206ad033d588246e09001d47ddce3ac50a31`, and Claude review
  `370278cd91fd9ecca2c64cd0953cae7ed63c4d16` remain preserved; the original
  disposition was `return-for-correction` with BF-1.
- BC-020-C1 corrected BF-1 through substantive commit
  `b770be849d625e924f7e65cae4efb8894a7e4c23` and metadata commit
  `8eb29165d5d59b99ccaa3b06fe6d8613dcaa11e2`.
- Claude's final C1 re-review
  `b51912a655d3f895651eb0bdbbe0c41ba1e7f132` returned
  `approve-with-notes`; BF-1 is resolved and zero blockers remain.
- SUR-011 remains unresolved. SUR-012 remains resolved only at the generic
  host-evidence-contract level; no current Chat/Codex security-grade protected
  cross-turn continuation is implied.
- BC-030 remains `spec-needed`, architecturally `ready_for_spec`, and unstarted.
  No Chat live probe, adapter runtime, successor Python runtime, Local Mirror,
  or PASS/SkillForge work occurred.
- Substantive administrative closure commit:
  `1e42c5dd2ee049fa5ebe4280692d1caecc0a3533`.
