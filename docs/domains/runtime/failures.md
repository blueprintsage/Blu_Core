# Runtime Failures

status: active
owner: docs/domains/runtime
last_reviewed: 2026-08-08

## 2026-08-05 — BC-010 safe extraction limits

- `sha256sum -c kernel/golden/v0.22.0/SHA256SUMS` could not run because
  `sha256sum` is unavailable on this Windows host. Do not treat that command
  failure as a checksum failure; the equivalent PowerShell SHA-256 comparison
  passed for all eight manifest entries.
- The optional `jsonschema` Python package is not installed. BC-010 does not
  add an undeclared dependency; its validator implements only the small schema
  subset used by the extracted contracts.
- Consolidating repeated StateTree blocks into a chosen status would silently
  resolve a golden-source conflict. The registry preserves one identity with
  `status=unresolved_conflict` and records all four source sections.
- Filling definitions for AntiDrift, OpsRestraint, Auth, OPSEC, EchoTrace
  support, RepoBoot, BluCode, Runtime configuration, SIMCODE_GATE, or
  MEMORY_GATE would invent declarations absent from the authoritative inputs.
  They remain referenced-but-not-defined.
- A distinct task-packet or capability-report field set cannot be extracted
  deterministically. Their required schema files are intentionally permissive
  and the gap is recorded in `unresolved_register.json`.
- BC-010 cannot simultaneously end as one commit and store that same commit's
  exact ID in a tracked file inside the commit. Git hashes the commit from its
  tree and metadata; inserting the hash changes the tree and produces a
  different hash.
- Reusable Git-governance lesson: never require a commit to contain its own
  final SHA. Use a follow-up metadata-only receipt commit, a tag, or an external
  handoff record. Dad authorized BC-010 to use one implementation commit
  followed by one metadata-only receipt commit; semantic review targets the
  implementation SHA.

## 2026-08-05 — BC-010-C1 reusable extraction failures

- Deployment instructions and kernel/runtime capsules must not be flattened
  into one source role. A host-only declaration can constrain loading,
  precedence, or exclusive dispatch without defining a kernel component.
- Unsupported JSON Schema validation or applicator keywords must never be
  ignored. A small local validator must publish its allowlist and fail clearly
  when a schema exceeds it.
- Extraction inference must be labeled. Joining two separately declared facts
  into one route record is not equivalent to one direct source declaration.
- Fragment substring matching is not source anchoring. Require an exact
  Markdown heading and, where necessary, an exact locator scoped to that
  heading.
- A commit cannot record its own final SHA. BC-010-C1 therefore continues the
  approved work-commit plus metadata-record-commit method.

## 2026-08-06 — BC-010-C2 reusable route-extraction failures

- A route name does not prove a lane-class enum value. An ingress step containing
  `opsec` cannot be promoted to `lane_class=opsec` when Exec's declared lane
  list omits it.
- Cross-role owner joins must be labeled as extraction inference. Preserving two
  source citations is necessary but does not turn separate declarations into
  one direct declaration.
- Successor architecture decisions must not be projected backward into
  golden-source extraction. Record the approved future boundary in project
  decisions while preserving the CTS gap in generated contracts.

## 2026-08-06 — BC-015 evidence limits

- An `ACTIVE` Markdown status, component entry, route row, parity case, or
  passing static validator is not current behavioral evidence. BC-015 therefore
  classifies no capability as `live_and_stable` without repeatable GPT-host
  observations.
- The required `2026-05-02_1333_Blu_v0.15.2_Baseline.zip` archive was not
  present in the attachment bundle or repository. Historical member paths,
  checksum, and direct behavior evidence must remain unavailable; do not
  reconstruct them from conversation memory.
- A successor decision cannot repair current provenance. Current OPSEC remains
  nondeterministic and lane-underspecified even though the successor
  pre-ingress restraint is approved.

## 2026-08-06 — BC-016 historical source-integration limits

- Absolute local paths must not be committed as historical provenance. Use an
  approved `source_root_id` plus a normalized relative path.
- An outer ZIP SHA-256 and a folder or payload manifest SHA-256 are distinct
  identities even when every payload file matches. Never substitute one for
  the other.
- Archive names, feature markers, headings, and implementation-style Markdown
  do not prove behavior, stability, reliability, or recovery value.
- Historical source availability after an audit does not retroactively falsify
  or rewrite that audit's earlier honest unavailable-evidence record.
- Duplicate archives must remain separate inventory records. Exact shared-hash
  groups and near-duplicate relationships may guide sampling, but neither
  authorizes silent deletion.
- Numeric filename suffixes are not automatically dates. Two task-file suffixes
  were initially parsed as short dates by the external discovery and were
  corrected during integration to explicit filesystem-timestamp fallbacks.

## 2026-08-08 — BC-018-C1 cross-turn security-state limits

- A semantic `session` label is not a storage substrate. Cross-turn security
  state requires evidenced `host_session` storage or an explicit receipted
  continuity operation; conversation history and model memory are never proof.
- Matching an `authorization_request_ref` string does not establish request
  binding. Require provider evidence for the current host session, record
  identity, freshness, expiry, action/resource scope, and replay status.
- A loop described as bounded in scope may still be unbounded in repetition.
  Require a finite positive policy-supplied attempt bound and fail closed on
  exhaustion without automatically issuing a fresh request.
- Keep policy authority, evidence evaluation, and state storage distinct.
  Duplicating attempt permission across OPSEC/Auth or giving it to the adapter
  creates an authority ambiguity even when all fields are present.
- A provider-caused terminal status does not need to become a policy-decision
  status. When required pre-ingress substrate is unavailable, retain the
  originating `SecurityDecision` authority and express `UNAVAILABLE` in
  Validation/Egress; requiring a nonexistent `ControlDecision` creates an
  authority gap, while expanding `SecurityDecision` conflates policy with
  provider failure.

## 2026-08-08 — BC-018-C1 closure-prep integrity limits

- Verifying every listed manifest digest does not prove manifest completeness.
  Canonical verification must compare the complete tracked-file set, excluding
  only `MANIFEST.sha256`, with the manifest path set before accepting zero hash
  mismatches. `.gitattributes` is part of that integrity boundary because it
  governs the LF-normalized Git-blob convention.
- A correlated host event must return through Security Restraint attempt-policy
  permission before Authorization Evaluator evaluation; diagrams must preserve
  that authority sequence even when machine-readable contracts are correct.
- Correlation evidence does not by itself prove integrity of host-provided
  `attempt_count`. BC-020/SUR-012 must evaluate tamper and rollback resistance,
  while the disposition of an unrelated intervening turn remains a separate
  security-policy input under SUR-011.

## 2026-08-09 — BC-020-C1 capability-evidence relevance limits

- A strong evidence class is not semantic support. A current receipt or local
  probe must bear on the normalized capability being claimed; current time does
  not prove Git push, and web search does not prove raw network.
- Interface/schema exposure is not operational availability. A visible
  scheduling interface does not prove provider/account connection, permission,
  usability, successful scheduling operations, future execution, or receipts.
- Evidence of absence cannot establish the positive property it says is absent.
  The security-gap probe can support unavailable attempt-count integrity but
  cannot support verified positive integrity.
- Use explicit `supports[]` and `does_not_prove[]` boundaries with a curated
  capability mapping. Do not replace the bounded contract check with free-form
  semantic inference.
