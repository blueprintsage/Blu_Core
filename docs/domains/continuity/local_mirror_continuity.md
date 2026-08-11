# Local Mirror Continuity Schema and Lifecycle

status: active
owner: docs/domains/continuity
last_reviewed: 2026-08-11
assignment: BC-030

## Boundary

Local Mirror is a candidate provider binding behind the existing Generic
Continuity Provider Boundary. It is not a new component. The Turn Controller
issues a typed `ServiceExchange`; the provider returns a typed result and
receipt. Model execution, host-session evidence, continuity storage, crawling,
indexing, and reasoning remain separate concerns.

The fixed architecture remains:

```text
7 components
8 packets
9 interfaces
```

Continuity uses `IF-CONTINUITY-PROVIDER` and the existing `ServiceExchange`.
`PendingAuthorizationState` remains a state record rather than a packet or
service.

## Evidence ladder

The provider boundary distinguishes source presence, discovery, retrieval,
mutation intent, mutation attempt, durable mutation completion, validation,
failure, and availability. No earlier stage implies a later one. In particular:

```text
source present != record retrieved
record retrieved != record validated
write requested != write attempted
write attempted != durable mutation completed
path or serialized object != provider receipt
model claim != provider evidence
```

A durable-success claim requires a `ContinuityReceipt` with
`status=completed`, matching provider, operation, request, record, scope, and
resulting version. Receipt evidence is operation-scoped and cannot be reused to
prove a different write or record.

## Record identity and versions

`record_id` identifies one stable logical lineage. `version` and `version_id`
identify an immutable version within that lineage. An update preserves
`record_id`, creates the next version, and marks the prior version superseded.
A supersession may create a different successor `record_id`; both records carry
the reciprocal relationship and the receipt proves the atomic result.

Current, superseded, and retired versions remain distinguishable. Historical
versions remain retrievable when authorization and provider availability permit.
BC-030 exposes no deletion or destruction operation. Provider loss or corruption
is reported as failure evidence; it is not normalized into an authorized delete.

Payload bytes may be inline or provider-referenced, but every returned record
preserves integrity and provenance metadata. A provider-native reference is
opaque or corpus-relative. Machine-specific absolute filesystem paths are not
portable record identities and must not cross the generic boundary.

## Bounded retrieval

A `ContinuityQuery` names one provider, namespace, and exact scope. Its selector
is bounded by record identity, record type, or provider-supported search terms;
it carries an explicit status/version filter and result limit. A provider must
not silently combine incompatible scopes. A caller that needs multiple scopes
issues separate queries and preserves their separate provenance.

Every `ContinuityRetrievalResult` returns the original query identity, outcome,
availability evidence, records with status/version/provenance, limitations, and
a provider receipt. `not_found`, `unavailable`, `degraded`, `forbidden`, and
`integrity_failure` remain distinct from an empty successful result.

## Availability and failure

Provider availability is `available`, `degraded`, `unavailable`, or `unknown`.
Configuration, a mounted directory, or a crawlable source cannot by itself prove
availability. The state requires current observation evidence and names the
operations actually supported.

Unavailable, failed, conflicting, forbidden, and integrity-failed mutations do
not create, update, supersede, or retire a record. Expected-version mismatch
returns `conflict` with the observed version when disclosure is permitted. The
caller must retrieve and make a new authorized decision; the provider never
silently overwrites.

Integrity failure quarantines the returned material from context staging. A
historical version may be recovered only by an explicit authorized query and
successful validation. Recovery does not silently make that historical version
current; any restoration is a new explicit mutation with its own receipt.

## Local Mirror/MPLPB mapping

The supplied Local Mirror archive matches the registered SHA-256 in
`config/source_authority.json`. It is non-authoritative reference evidence. Its
useful contract evidence is limited to:

- a bounded authoritative root and corpus boundary;
- portable relative internal references;
- machine-readable document identity, scope, status, and version metadata;
- current versus retired distinction and explicit supersession links;
- separate graph discovery, retired-history audit, indexing, and reasoning;
- default-current retrieval plus explicit historical lookup;
- validation and falsifier behavior;
- stateless boot orientation.

The reference implementation proves neither a durable mutation API nor provider
receipts, atomic compare-and-set, crash consistency, authentication,
authorization, confidentiality, replay/consumption state, monotonic attempt
state, rollback resistance, or current provider availability. A future Local
Mirror provider must add those behaviors behind the generic boundary before it
may claim conformance. The corpus's presence or crawlability alone proves only
source presence and, when actually observed, discovery/retrieval stages.

## Stateless restart and rehydration

```text
new runtime or hosted turn
-> observe continuity-provider availability
-> issue bounded retrieval request
-> receive provider result and receipt
-> validate identity, scope, version, provenance, and integrity
-> stage only authorized bounded material as turn context
-> invoke the model when appropriate
```

The runtime may say continuity was rehydrated only after the completed retrieval
and validation gates. A new process repeats them. Prompt context and prior
conversational familiarity are not persistence receipts.

## Host-session relationship

`host_session` and `durable_external` are independent substrates. Host-session
identity, binding, freshness, and receipt evidence come from the Generic Host
Adapter. Durable continuity evidence comes from the Generic Continuity Provider.
A host-session record may contain a continuity reference, but the reference does
not promote host state to durability. A durable record may mention a host-session
binding, but that mention does not prove a current host session.

## Protected authorization state

Ordinary continuity evidence is insufficient for protected cross-turn
authorization continuation. A qualifying provider must evidence state-record
identity, request/action/resource binding, scope, freshness and expiry,
integrity, replay/consumption state, and monotonic or rollback-resistant attempt
state, with operation receipts and expected-version conflict protection.

The supplied Local Mirror reference does not establish those properties.
Therefore ordinary continuity may be specifiable while durable protected
authorization continuation remains unavailable. Storing an authorization
attempt does not make it trusted.

SUR-011 remains unresolved. BC-030 defines no retry counts, lockout/backoff,
cancellation/reset, unrelated-turn, or new-request-after-exhaustion policy.

## Cross-host and future model constraint

The schemas are host- and model-neutral. ChatGPT-hosted Blu may use them only
when an authorized provider is exposed; a future Python Blu may bind a local
provider. Neither deployment receives a separate memory canon.

A future Python runtime may use an LM Studio-served model only through the Model
Execution Boundary. Changing model provider must not change Persona, Operations
Law, continuity semantics, security contracts, or validation contracts. BC-030
adds no LM Studio code.
