# BC-015 — Assignment Record

status: review
owner: Dad
approved_by: Dad and Blu
implementation_owner: Codex
semantic_reviewer: Claude
exact_base: 4b51427b361283715a24110409e031e191b52452

## Approved packet

You are implementing:

# BC-015 — Runtime Viability Audit

in the `Blu_Core` repository.

## Authority and roles

* Project Owner and final authority: Dad
* Project Lead and integration reviewer: Blu
* Implementation owner: Codex
* Semantic reviewer: Claude
* Assignment domain: runtime
* Exact approved base:

```text
4b51427b361283715a24110409e031e191b52452
```

* Recommended branch:

```text
bc-015-runtime-viability-audit
```

BC-015 is an evidence and classification assignment. It does not implement the successor Python runtime.

## Objective

Determine what the current Blu runtime genuinely contributes before any behavior is ported into Python.

The audit must distinguish:

1. behavior that currently works;
2. behavior that works only nondeterministically or through host/model cooperation;
3. behavior that is declared but not observably functioning;
4. behavior that is conflicting or underspecified;
5. behavior that is explicitly deferred or removed;
6. capability that belongs only to the approved successor architecture.

The purpose is to prevent both:

* blindly porting an elaborate component graph whose behavior is mostly simulated or unproven;
* discarding useful Blu behaviors merely because their prior implementation was bloated or unreliable.

## Required startup

Run:

```text
git fetch origin --prune
git switch main
git pull --ff-only origin main
git status --short
git rev-parse HEAD
```

Requirements:

* `HEAD` must be exactly:

```text
4b51427b361283715a24110409e031e191b52452
```

* The working tree must be clean.
* If `main` has moved, stop and report the new SHA. Do not silently rebase the assignment onto a different base.
* Create:

```text
bc-015-runtime-viability-audit
```

## Required reading order

Read before changing files:

```text
AGENTS.md
CODEX.md
docs/dev/docs_index.md
docs/dev/assistant_coding_behavior.md
docs/dev/domain_assignment_record_standard.md
docs/worklogs/assignments.md

docs/architecture/current_runtime.md
docs/architecture/migration_centerline.md

docs/sources/authority_map.md
docs/sources/cts_source_roles.md
docs/sources/external_inputs.md
docs/sources/migration_memcap_2026-08-05.md

docs/domains/runtime/index.md
docs/domains/runtime/decisions.md
docs/domains/runtime/worklog.md
docs/domains/runtime/failures.md
docs/domains/runtime/next_steps.md

contracts/runtime/README.md
contracts/runtime/source_map.json
contracts/runtime/component_registry.json
contracts/runtime/route_registry.json
contracts/runtime/parity_matrix.json
contracts/runtime/unresolved_register.json

docs/domains/runtime/assignments/BC-010/review.md
docs/domains/runtime/assignments/BC-010-C1/review.md
docs/domains/runtime/assignments/BC-010-C2/review.md
```

Read all seven immutable CTS sources:

```text
kernel/golden/v0.22.0/00_Instructions.md
kernel/golden/v0.22.0/01_Persona.md
kernel/golden/v0.22.0/02_Operations_Law.md
kernel/golden/v0.22.0/03_Exec.md
kernel/golden/v0.22.0/04_Exec_Library.md
kernel/golden/v0.22.0/05_Commands.md
kernel/golden/v0.22.0/06_Programs.md
```

Verify all golden checksums before beginning the audit.

## Source roles and authority

The current CTS source set has two roles:

```text
00_Instructions.md
  deployment_instruction

01_Persona.md through 06_Programs.md
  kernel_runtime_capsule
```

All seven files are authoritative for what the current CTS declares.

The extracted contracts are descriptive indexes. They assist inventory and provenance analysis but do not outrank the golden CTS and do not prove execution.

Project decisions may define successor architecture, but they must not be projected backward into the current CTS.

Historical Blu versions may demonstrate intended or formerly observable behavior. They do not define current behavior and cannot override the current CTS.

## Historical source supplied with this assignment

Dad will supply:

```text
2026-05-02_1333_Blu_v0.15.2_Baseline.zip
```

Treat it as:

```text
source_role: historical_behavioral_reference
authority: non-authoritative-for-current-runtime
```

Requirements:

* compute and record its SHA-256;
* inspect it directly rather than relying on conversation summaries;
* do not vendor the archive or its full extracted contents into the repository;
* do not copy legacy contracts into current runtime contracts;
* cite exact archive member paths and headings for any historical evidence used;
* distinguish historical declaration from evidence that a feature actually worked.

If the archive is unavailable in the execution environment:

* continue the current-runtime portion of BC-015;
* record the historical source as unavailable;
* leave affected historical-evidence fields unresolved;
* do not invent or reconstruct its contents from memory.

## Approved owner observations

The following are explicit observations supplied by Dad and Blu. Record them as:

```text
evidence_class: owner_observation
```

They are evidence, but they are not golden-source declarations or repeatable automated tests.

### Auth

* Auth authorizes Admin-level users.
* Auth has observably worked.
* Its recognition and enforcement are nondeterministic and host/model-dependent.
* Preliminary current classification:

```text
live_but_nondeterministic_or_host_dependent
```

### OPSEC

* OPSEC protects against unauthorized ID challenge access and unauthorized copying, cloning, recreation, or disclosure of Blu’s protected kernel/runtime sources.
* OPSEC has observably worked.
* Its recognition and enforcement are nondeterministic and host/model-dependent.
* Preliminary current classification:

```text
live_but_nondeterministic_or_host_dependent
```

The approved successor-runtime decision is separate:

```text
OPSEC becomes a mandatory pre-ingress security restraint rather than an ordinary route lane.
```

Represent that successor mechanism as its own successor-capability record. Do not rewrite the current CTS classification to pretend the present kernel already defines that complete contract.

### Persona warmth and mood

* Blu’s warmth, presence, and relational posture remain observable.
* The public `/mood` command is not live.
* Do not classify relational warmth as absent merely because the command surface was removed.
* Distinguish:

  * model-facing Persona behavior;
  * internal mood/source shaping;
  * public mood command or render behavior.

### Legacy Teaching and capability Markdown

* Older Blu versions contained Teaching-oriented Markdown and broader libraries that sometimes produced useful behavior.
* The older Exec was heavily bloated and attempted to brute-force behavior with feature-specific gates.
* “Kinda worked” is historical owner observation, not proof of stability or evidence that the legacy architecture should be restored.

## Viability classifications

Every audited record must receive exactly one current classification:

```text
live_and_stable
live_but_nondeterministic_or_host_dependent
declared_but_not_observably_functioning
conflicting_or_underspecified
explicitly_deferred_or_removed
new_successor_runtime_capability
```

### Classification rules

#### `live_and_stable`

Requires current observable evidence of repeatable behavior.

A source declaration, active status, component-registry entry, or well-written Markdown contract is not sufficient.

Use this classification only when evidence supports repeatability rather than isolated success.

#### `live_but_nondeterministic_or_host_dependent`

Use when the behavior is currently observable, but depends on model recognition, context pressure, host tooling, tool availability, or inconsistent contract following.

#### `declared_but_not_observably_functioning`

Use when the current source declares a capability but no current execution evidence supports that it functions.

Do not equate this with “broken.” It may simply be unproven.

#### `conflicting_or_underspecified`

Use when source conflicts, missing owners, missing fields, undefined services, ambiguous ownership, or incomplete contracts prevent an honest behavioral determination.

#### `explicitly_deferred_or_removed`

Use when current Commands, Programs, project governance, or CTS text explicitly says a surface is unavailable, deferred, removed, or not live.

#### `new_successor_runtime_capability`

Use only for an approved future mechanism that does not already exist as a complete current-runtime capability.

Do not use this category merely because an existing behavior will later be reimplemented in Python.

## Evidence classes

Use only these evidence classes unless the assignment documents a justified extension:

```text
golden_declaration
contract_extraction
project_decision
owner_observation
current_live_probe
host_capability_observation
historical_baseline
automated_static_check
extraction_inference
unavailable_evidence
```

Every material conclusion must reference one or more evidence records.

Explicitly distinguish:

```text
declared
observed
inferred
proposed
approved_for_successor
```

Do not collapse those states into one another.

## Required audit coverage

Use the current extracted registries as the inventory floor.

Every entry in these files must either:

* map to an individual viability record; or
* map to an explicitly documented grouped record whose membership is listed.

```text
contracts/runtime/component_registry.json
contracts/runtime/route_registry.json
contracts/runtime/parity_matrix.json
contracts/runtime/unresolved_register.json
```

The audit must explicitly cover at least:

### Identity and model-facing law

* Persona
* relational warmth and presence
* internal mood formation
* public mood surface
* Operations Law
* truth discipline
* anti-drift and correction behavior
* source and capability honesty

### Runtime control

* deployment entry boundary
* Exec
* mandatory restraint scheduling
* RuntimeGate.Ingress
* route locking
* owner locking
* dependency scheduling
* RuntimeGate.Egress
* ScopeLock
* terminal packets
* current-turn receipts
* fail-closed behavior
* artifact proof
* EchoTrace or equivalent diagnostics

### Security and authorization

* Auth
* pending-auth handling
* OPSEC interception
* unauthorized ID challenge handling
* kernel-copy and clone protection
* approved successor OPSEC pre-ingress restraint

### Commands and routes

* every currently live command family;
* every explicitly deferred or removed command family;
* unknown slash-command behavior;
* `/commands`;
* `/help`;
* `/ID`;
* `/memory`;
* `/simcode`;
* `/echotrace`;
* `/mood`;
* `/remind`;
* PASS;
* destructive memory forms;
* any other command surface present in the registries.

### Programs and workflows

* SimCode
* Memory Program
* natural-language memory intent
* memory import
* memory export
* memory list/help
* workflow resume
* kernel-work/BluCode route
* repository bootstrap behavior

### ExecLib and support components

Include all extracted components, with explicit attention to:

* AntiDrift
* Operations restraint
* ArtifactLens
* DateLib
* Time Service
* ReminderLib
* GreetingLib
* PersonaLib
* MoodLib
* MMU
* StateTree
* MemoryPacket
* ContextIntake
* staged memory
* continuity packets
* source-truth and work-state mechanisms
* validation/regression support
* Read Lane libraries
* Humor-related references
* ErrorMacros and error rendering
* undefined or externally referenced owners and services

### Legacy behavior recovery

Inspect the supplied v0.15.2 baseline for behavioral evidence concerning:

* Teaching behavior;
* reminders and time;
* mood;
* PersonaLib;
* MMU;
* Read Lane;
* PASS;
* continuity;
* artifact handling;
* feature-specific Exec gates.

For each useful legacy behavior, distinguish:

```text
behavior_worth_recovering
architecture_worth_reusing
```

The default must not be that both are true.

## Deliverables

Create:

```text
docs/domains/runtime/viability/README.md
docs/domains/runtime/viability/evidence_register.json
docs/domains/runtime/viability/viability_matrix.json
docs/domains/runtime/viability/probe_catalog.md
docs/domains/runtime/viability/audit_report.md
```

### `README.md`

Document:

* purpose;
* authority boundary;
* source roles;
* classification definitions;
* evidence definitions;
* known limitations;
* distinction between current viability and successor disposition;
* statement that the audit is not runtime implementation.

### `evidence_register.json`

Each evidence entry must include:

```text
id
evidence_class
source_role
source_identity
source_location
source_heading_or_locator
summary
supports
limitations
observed_by
observed_date
```

Use `null` where a field legitimately does not apply. Do not invent data to avoid nulls.

Historical archive evidence must include:

```text
archive_filename
archive_sha256
member_path
```

Owner observations must identify Dad and/or Blu and must not masquerade as automated proof.

### `viability_matrix.json`

Each capability record must include at least:

```text
id
name
kind
current_source_ids
contract_ids
covered_component_ids
covered_route_ids
covered_parity_ids
covered_unresolved_ids
current_viability_class
classification_confidence
evidence_ids
observable_behavior
known_failure_modes
host_dependencies
current_owner
current_definition_status
legacy_behavior_evidence
successor_delta
proposed_disposition
responsibility_split
required_live_probes
required_regression_tests
open_decisions
notes
```

Allowed `classification_confidence` values:

```text
high
medium
low
unresolved
```

Allowed proposed dispositions:

```text
implement_deterministically
keep_model_facing
recover_as_lightweight_profile
keep_contract_and_defer
remove
hybrid_split
architecture_decision_required
```

These are Codex’s evidence-based proposals, not final architecture decisions.

`responsibility_split` must separately address:

```text
python
model
profile
host
deferred
```

Do not force a mixed capability into a false single-owner migration answer.

### `probe_catalog.md`

Create bounded current-runtime probes that Dad and Blu can later run in the GPT host.

Each probe must include:

```text
Probe ID
Capability
Purpose
Required host conditions
Input
Expected observable behavior
Failure indicators
Safety or OPSEC restrictions
Evidence produced
Classification impact
```

Do not include a probe that requests disclosure of protected kernel text.

OPSEC probes must test refusal/interception behavior without requiring the protected content to be revealed.

Do not claim a probe was executed unless it was directly executed and recorded.

### `audit_report.md`

Summarize:

* inventory coverage;
* classification totals;
* strongest current capabilities;
* nondeterministic capabilities;
* declared but unproven machinery;
* conflicts and source gaps;
* explicitly retired surfaces;
* useful legacy behavior candidates;
* legacy architecture that should not be restored;
* likely deterministic Python candidates;
* model-facing responsibilities;
* profile candidates;
* decisions reserved for Dad and Blu;
* whether available evidence is sufficient to begin specifying the smallest Python shell.

The report must explicitly answer:

> What is the smallest honest successor-runtime control plane supported by current evidence?

Do not implement that control plane.

## Preliminary architectural hypotheses to test, not assume

Evaluate these hypotheses against the evidence:

1. Persona and Operations should remain primarily model-facing.
2. Packet validation, route locking, capability detection, ScopeLock mechanics, terminal validation, and receipts are strong deterministic candidates.
3. Auth requires deterministic authorization workflow support.
4. OPSEC requires deterministic pre-ingress enforcement in the successor runtime.
5. Teaching is more likely a lightweight profile than a restored Program or large library.
6. Public reminders require real host scheduling and cannot be made reliable through Markdown alone.
7. Time formatting and date math may be deterministic, while live-time acquisition remains host-dependent.
8. Legacy Read Lane behavior may reduce to source handling, citation discipline, and task-specific profiles rather than six separate runtime libraries.
9. PASS should not be restored merely because older versions contained it.
10. Current component names should not automatically determine future service boundaries.

Mark each hypothesis:

```text
supported
partially_supported
unsupported
insufficient_evidence
```

## Static validation tooling

You may create:

```text
tools/validate_viability_audit.py
tests/viability/**
```

The validator must use Python 3.12 standard library only.

It may validate:

* JSON syntax;
* required files;
* required fields;
* allowed enum values;
* unique IDs;
* resolved evidence references;
* coverage of every component-registry entry;
* coverage of every route-registry entry;
* coverage of every parity requirement;
* coverage of every unresolved-register entry;
* historical-source metadata when historical evidence is cited;
* distinction between current classification and successor disposition.

It must not:

* execute Blu;
* simulate GPT behavior;
* infer that a capability works;
* implement routing;
* implement Auth or OPSEC;
* claim behavioral parity.

Tests must include negative cases for:

* unknown classification;
* missing evidence reference;
* uncovered registry entry;
* duplicate capability ID;
* invalid proposed disposition;
* `live_and_stable` supported only by a static declaration;
* historical evidence missing archive identity;
* successor decision projected backward as a golden declaration.

## Assignment records

Create:

```text
docs/domains/runtime/assignments/BC-015/assignment.md
docs/domains/runtime/assignments/BC-015/handoff.md
docs/domains/runtime/assignments/BC-015/validation.md
docs/domains/runtime/assignments/BC-015/review.md
```

Requirements:

* Save this approved packet as `assignment.md`.
* Set assignment status to `active` while implementing.
* Leave `review.md` pending for Claude.
* Add BC-015 to `docs/worklogs/assignments.md`.
* Record the exact base.
* Do not change BC-020 or BC-030 from `spec-needed`.

Update as appropriate:

```text
docs/domains/runtime/worklog.md
docs/domains/runtime/failures.md
docs/domains/runtime/next_steps.md
docs/dev/docs_index.md
docs/sources/external_inputs.md
```

Update `external_inputs.md` only to record the supplied v0.15.2 archive identity, checksum, source role, and non-authoritative status.

## Allowed collision domain

You may create or modify only:

```text
docs/domains/runtime/viability/**
docs/domains/runtime/assignments/BC-015/**
docs/domains/runtime/worklog.md
docs/domains/runtime/failures.md
docs/domains/runtime/next_steps.md
docs/worklogs/assignments.md
docs/dev/docs_index.md
docs/sources/external_inputs.md
tools/validate_viability_audit.py
tests/viability/**
MANIFEST.sha256
```

Any additional path requires an approved amendment from Dad or Blu.

## Protected paths

Do not modify:

```text
kernel/golden/**
contracts/runtime/**
docs/architecture/**
docs/sources/authority_map.md
docs/sources/cts_source_roles.md
docs/sources/migration_memcap_2026-08-05.md
docs/domains/runtime/decisions.md
AGENTS.md
CLAUDE.md
CODEX.md
config/**
tools/validate_runtime_contracts.py
tests/contracts/**
```

## Prohibited work

Do not:

* create a Python Blu runtime;
* implement Auth;
* implement OPSEC;
* implement routing or ScopeLock;
* implement reminders;
* implement persistence or Local Mirror;
* restore PASS;
* alter current commands;
* alter current Programs or libraries;
* rewrite Persona or Operations Law;
* edit the golden CTS;
* edit extracted contracts;
* resolve current source conflicts;
* claim that active Markdown status proves executable behavior;
* claim that one successful observation proves stability;
* treat Codex’s proposed disposition as final approval;
* vendor the supplied legacy ZIP;
* force-push or rewrite history.

## Required validation

Run:

```text
git status --short
git rev-parse HEAD
git diff --check

git diff --exit-code \
  4b51427b361283715a24110409e031e191b52452 \
  -- kernel/golden contracts/runtime docs/architecture config

sha256sum -c kernel/golden/v0.22.0/SHA256SUMS
python tools/validate_runtime_contracts.py
python -m unittest discover -s tests/contracts -p "test_*.py"

python tools/validate_viability_audit.py
python -m unittest discover -s tests/viability -p "test_*.py"
```

Use the repository’s PowerShell SHA-256 equivalent if `sha256sum` is unavailable.

Regenerate and verify:

```text
MANIFEST.sha256
```

Confirm mechanically that every entry from:

```text
component_registry.json
route_registry.json
parity_matrix.json
unresolved_register.json
```

is covered by the viability matrix.

Record exact counts in `validation.md`.

## Completion conditions

BC-015 may move to `review` only when:

* the current runtime inventory is complete;
* all required registry records are covered;
* every classification is evidence-linked;
* static declarations are not misrepresented as working behavior;
* Auth and OPSEC preserve the approved owner observations;
* current OPSEC behavior remains distinct from the successor pre-ingress decision;
* historical v0.15.2 evidence is clearly non-authoritative;
* useful legacy behavior is separated from legacy architecture;
* live probes are cataloged but not falsely marked executed;
* proposed dispositions are clearly non-final;
* no runtime implementation was added;
* protected paths are unchanged;
* validators and tests pass;
* golden checksums pass;
* the manifest verifies;
* assignment records are complete;
* the working tree is clean;
* the branch is pushed.

## Commit method

Use the established two-commit method.

### Commit 1 — audit work

Suggested message:

```text
docs(BC-015): audit current runtime viability
```

This is Claude’s semantic review target.

### Commit 2 — metadata record

After Commit 1 exists, record its exact SHA in:

```text
docs/domains/runtime/assignments/BC-015/handoff.md
docs/worklogs/assignments.md
```

Suggested message:

```text
docs(BC-015): record viability audit handoff
```

The metadata commit must not modify:

```text
docs/domains/runtime/viability/**
tools/**
tests/**
kernel/golden/**
contracts/runtime/**
```

## Claude review boundary

Claude’s later semantic review must determine whether:

* classifications are supported by evidence;
* declarations and observations remain distinct;
* historical evidence is represented honestly;
* current and successor architecture are not conflated;
* useful behavior is not confused with legacy component structure;
* proposed migration dispositions follow from the evidence;
* coverage is complete;
* no runtime implementation occurred.

Dad and Blu retain final authority over all successor dispositions.

## Final handoff

Report:

```text
Assignment: BC-015
Exact base:
Branch:
Audit work commit:
Metadata record commit:
Historical archive available:
Historical archive SHA-256:
Capabilities inventoried:
Component entries covered:
Route entries covered:
Parity requirements covered:
Unresolved entries covered:
Classification totals:
Live probes executed:
Live probes remaining:
Likely deterministic candidates:
Likely model-facing responsibilities:
Likely profile-recovery candidates:
Decision-required items:
Files changed:
Golden checksum result:
Runtime contract validation result:
Viability audit validation result:
Unit-test results:
Manifest result:
Protected-path diff result:
Known unresolved evidence:
Known risks:
Working-tree status:
Push status:
```
