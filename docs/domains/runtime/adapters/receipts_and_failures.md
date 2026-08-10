# Host Receipts, Artifacts, Delivery, and Failures

status: review
owner: docs/domains/runtime
last_reviewed: 2026-08-08
assignment: BC-020

## HostActionReceipt

Every receipt records ID, family/surface/provider, capability, operation,
status, start/completion time or turn refs, scope, limitations, and evidence
ref. Optional result, artifact, and provider-operation IDs are included only
when exposed. Status is `completed`, `failed`, `partial`, `unavailable`, or
`denied`; these are host outcomes, not kernel PASS/BLOCK policy.

No side effect is completed because a model requested it, the adapter attempted
it, a host approval was granted, or a command was generated. Success requires
appropriate provider/host evidence. When no receipt is exposed, the adapter
states that limitation and cannot claim completion.

## Artifacts and delivery

Artifact state distinguishes `requested`, `attempted`, `created`, and
`verified`, plus failure/unavailability. Evidence can be a host object ref,
filesystem path plus stat/read/hash, provider object ID, or another supported
receipt. Size, hash, MIME type, and timestamps are optional because some hosts
cannot expose them. A filename emitted by a model proves nothing.

Output delivery distinguishes adapter acceptance, host display, and human read.
A host-render/delivery receipt cannot claim that Dad read the result unless the
provider supplies explicit read evidence.

Scheduling receipts require provider schedule identity, normalized schedule,
operation, result, and limitations. Shell/process receipts record working
directory/sandbox/approval/network scope, timeout, exit code, output
availability, and limitations. Git and integration operations keep their own
provider scopes.

## Error normalization

The adapter distinguishes capability unavailable, permission denied, approval
required/denied, sandbox/network denial, timeout, provider error, partial
result, stale evidence, correlation failure, replay detection, missing receipt,
unsupported surface, and unknown host failure.

The adapter reports the host condition. Higher-level kernel policy decides
ASK, BLOCK, UNAVAILABLE, INVALID, or ERROR as appropriate. For example,
`approval_required` does not mean authorized, and
`same_host_session_uncorrelated` does not decide whether a pending challenge is
cancelled, retained, or consumes an attempt.
