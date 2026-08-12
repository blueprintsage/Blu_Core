# Minimum OPSEC Match and Redaction Contract

status: review
owner: docs/domains/runtime
last_reviewed: 2026-08-11
assignment: BC-041-C1

## Authority and boundary

This directory defines the public minimum successor mechanism authorized by
BC-041. It does not replace or reinterpret the current CTS. The recovered
current law remains the immutable CTS privacy/OPSEC boundary; BC-041 supplies a
newly authorized successor implementation contract where the CTS did not
define deterministic matcher values.

The mechanism belongs beneath the existing **Pre-ingress Security Restraint**
and **Validation and Egress**. It adds no component, packet, interface, route,
Auth behavior, protected continuation, or production runtime.

## Public mechanism and protected payload

Public and committed here:

- policy and result schemas;
- normalization and matching semantics;
- policy-reference and loading stages;
- ingress and egress mappings;
- redaction safety rules;
- content-safe evidence and diagnostics;
- synthetic fixtures and a nonproduction conformance harness.

Never committed here:

- production phrases, aliases, fingerprints, thresholds, exceptions, source
  identifiers, credentials, challenge answers, or authorization evidence;
- production policy locations or integrity digests;
- raw matched ingress or candidate output.

The canonical runtime configuration contains only environment-variable names.
The environment supplies the machine-local policy location and expected
SHA-256 digest. A configured reference is not proof that the policy was found,
loaded, schema-valid, integrity-valid, or usable.

## Minimum matcher

The matcher accepts text only. It deterministically removes every Unicode
general-category `Cf` code point, producing one candidate regardless of how
many format characters were inserted or where they were placed. Alongside that
candidate it retains normalized boundary offsets showing where one or more
`Cf` code points were removed. This is provenance metadata on the same
candidate, not another candidate view. The candidate continues through the
existing normalization pipeline: Unicode NFKC, line-break and whitespace
normalization, bounded common-separator mapping, repeated-space collapse, trim,
and per-rule case folding.

For matching only, every normalized inter-word space in a protected rule may
match zero or more normalized ASCII spaces in the candidate. Zero spaces are
intentional: they recover rule words whose separation was destroyed by `Cf`
removal, so an unseparated concatenation of a rule's words is deliberately a
fail-safe match rather than accidental fuzzy matching. At the phrase's outer
edges, a guard is satisfied only by a genuine non-word neighbour or a retained
offset where `Cf` removal created the apparent word adjacency. Ordinary
prefix/suffix word adjacency with no such provenance remains a nonmatch.
Contiguous unseparated repetition of the same protected rule is also collected
as one protected run; this does not admit an unrelated prefix or suffix token.
The matcher therefore covers arbitrary mixtures and counts of boundary,
inside-token, and outer-edge `Cf` insertions with one linear candidate. It does
not enumerate placement combinations or generate a candidate set that grows
with insertion count. These semantics apply symmetrically to ingress and
candidate egress output.

The matcher supports only token-bounded `normalized_phrase` rules. It does not
call a model, infer intent, assign confidence, or authenticate. It does not
claim arbitrary semantic-equivalence detection.

Ingress is evaluated before Turn Controller. No usable policy means terminal
`UNAVAILABLE`, no `SecurityDecision`, and no model eligibility. A protected
match means `SecurityDecision=BLOCK`; a nonmatch means `PASS`. BC-041 defines no
new case that maps a protected match to `ASK`.

Candidate model output is evaluated before terminal print. A nonmatch is
`CLEAR`. A matched rule may require whole-output `BLOCKED` or may permit
`REDACTED`. Redaction emits the canonicalized candidate with every matched span
replaced by `[protected content omitted]`, then re-runs the same `Cf`-removed,
separator-tolerant matcher. Empty residual content, a remaining match, an
overlapping/invalid span, or any rule requiring block makes the whole output
non-printable. If matching spans cannot be represented by one non-overlapping
safe span set, redaction fails closed to whole-output `BLOCKED`. Raw protected
candidate text is never used as a diagnostic.

## Evidence and diagnostics

Safe evidence is structural: evaluation phase, result, policy revision, opaque
rule references, safe reason/error codes, and an HMAC-SHA-256 of the normalized
candidate using a production-policy-only evidence key. The key and candidate
are never emitted. Plain unkeyed digests of protected text are forbidden.

## Synthetic fixture boundary

`tests/security/fixtures/synthetic_policy.json` is deliberately fictional and
is marked `synthetic test policy != production protected policy`. Passing its
tests proves only conformance of the public mechanism. It does not prove that a
production policy is complete, correctly classified, or resistant to arbitrary
paraphrase and obfuscation.

## Limitations

The bounded `Cf` correction closes Unicode general-category `Cf` insertion for
the specified deterministic matcher. It does not claim comprehensive handling
of every non-`Cf` default-ignorable or invisible Unicode character, nor general
protection against Unicode confusable or homoglyph substitution, including
characters from another script that visually resemble Latin letters. Those
character-level evasion classes are explicitly outside this minimum Phase-1
matcher unless a future security assignment authorizes a bounded policy; they
are not being classified as semantic paraphrase.
