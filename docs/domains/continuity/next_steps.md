# Continuity Next Steps

status: active
owner: docs/domains/continuity
last_reviewed: 2026-08-11

- BC-030 is closed at the specification boundary. SUR-007 is resolved at the
  generic continuity-contract level; SUR-011 remains unresolved.
- No Local Mirror provider, successor Python runtime, or LM Studio adapter exists
  yet. No Chat/Codex adapter implementation was added by BC-030.
- Protected durable authorization remains unavailable unless a future provider
  supplies the complete stronger evidence profile, including atomic replay and
  rollback-resistant attempt state. Ordinary continuity receipts are
  insufficient.
- Claude notes N1-N8 remain implementation-readiness inputs: add a mutation
  request with `expected_version`; tighten `not_found` and non-completed receipt
  constraints; document `availability_probe`; mechanically enforce action
  binding and absolute-path prohibition; regression-protect Git-scope and
  manifest guards; and validate manifest digests. Add instance-level schema
  conformance fixtures and select the consuming schema runtime.
- The next successor assignment is the separately authorized
  implementation-readiness / One-Blu portability contract. Do not begin it from
  this closure.
- Do not implement a provider, Python runtime, LM Studio adapter, Chat live
  probe, Codex Blu work, SUR-011 policy, or PASS/SkillForge integration without
  a new bounded assignment.
