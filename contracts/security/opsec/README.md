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

The matcher accepts text only. It deterministically derives exactly two
candidate views. In
`cf_to_ascii_space`, every Unicode general-category `Cf` code point becomes an
ASCII space. In `cf_removed`, every `Cf` code point is removed. Each view then
continues independently through the full existing normalization pipeline:
Unicode NFKC, line-break and whitespace normalization, bounded common-separator
mapping, repeated-space collapse, trim, and per-rule case folding. The matcher
evaluates both views, and a match in either view is a protected match. This
applies symmetrically to ingress and candidate egress output.

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
replaced by `[protected content omitted]`, then re-runs the full matcher. Empty
residual content, a remaining match, an overlapping/invalid span, or any rule
requiring block makes the whole output non-printable. If divergent candidate
views contain protected matches that cannot be represented by one safe span
set, redaction fails closed to whole-output `BLOCKED`. Raw protected candidate
text is never used as a diagnostic.

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

The bounded `Cf` correction closes invisible Unicode format-character insertion
for the specified deterministic matcher. It does not claim general protection
against Unicode confusable or homoglyph substitution, including characters from
another script that visually resemble Latin letters. That character-level
evasion class is explicitly outside this minimum matcher unless a future
security assignment authorizes a bounded confusable policy; it is not being
classified as semantic paraphrase.
