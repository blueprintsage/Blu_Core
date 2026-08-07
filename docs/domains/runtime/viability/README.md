# Runtime Viability Audit

status: review
owner: docs/domains/runtime
last_reviewed: 2026-08-06
assignment: BC-015

## Purpose

This directory records what the Blu v0.22.0 CTS deployment currently declares, what Dad and Blu have observed, what remains unproven or conflicted, and which future mechanisms are approved only for the successor runtime. It prevents static Markdown structure from being mistaken for executable behavior.

This is an evidence and classification audit. It is not a Python runtime implementation, behavior port, source rewrite, or architecture approval.

## Authority boundary

Authority remains:

1. Dad's explicit instruction.
2. Approved runtime decisions.
3. The immutable seven-file CTS source set.
4. Active project governance and architecture.
5. Downstream extracted contracts.
6. Non-authoritative historical evidence.

The extracted contracts supply the inventory floor and provenance aids. They do not outrank the CTS and do not prove execution. Proposed dispositions in the matrix are Codex's evidence-based proposals; Dad and Blu retain final authority.

## Source roles

- `00_Instructions.md`: `deployment_instruction`.
- `01_Persona.md` through `06_Programs.md`: `kernel_runtime_capsule`.
- `contracts/runtime/*.json`: `downstream_descriptive_contract`.
- Approved Dad/Blu statements: `approved_owner_observation`.
- `2026-05-02_1333_Blu_v0.15.2_Baseline.zip`: expected `historical_behavioral_reference`, non-authoritative for the current runtime. The archive was unavailable, so no member evidence or checksum is claimed.

## Current viability classifications

- `live_and_stable`: repeatable current behavior supported by observable evidence.
- `live_but_nondeterministic_or_host_dependent`: observed current behavior whose recognition, enforcement, tools, or host path is inconsistent or conditional.
- `declared_but_not_observably_functioning`: current source declares the behavior, but current execution evidence is absent.
- `conflicting_or_underspecified`: source conflict, undefined owner, absent fields, ambiguous ownership, or incomplete contract prevents an honest determination.
- `explicitly_deferred_or_removed`: current source says the surface is unavailable, deferred, removed, or not live.
- `new_successor_runtime_capability`: approved future mechanism that is not a complete current-runtime capability.

No capability is classified `live_and_stable` in this audit because no repeatable current GPT-host probe was executed.

## Evidence classes

- `golden_declaration`: direct CTS text; proves declaration only.
- `contract_extraction`: downstream registry/provenance representation.
- `project_decision`: approved architecture for the successor or project.
- `owner_observation`: Dad/Blu observation; not automated proof.
- `current_live_probe`: directly executed current-host probe. None were produced in BC-015.
- `host_capability_observation`: directly observed host capability.
- `historical_baseline`: direct evidence from the supplied historical archive. None was available.
- `automated_static_check`: syntax, integrity, coverage, or reference check.
- `extraction_inference`: explicit audit or extraction join, labeled as inference.
- `unavailable_evidence`: required evidence that could not be accessed.

Every conclusion keeps `declared`, `observed`, `inferred`, `proposed`, and `approved_for_successor` distinct.

## Files

- `evidence_register.json`: evidence identities, source locators, support links, and limitations.
- `viability_matrix.json`: 30 capability records covering all registry inventories.
- `probe_catalog.md`: safe GPT-host probes for later execution by Dad or Blu.
- `audit_report.md`: findings, hypothesis results, successor boundary, and reserved decisions.

## Known limitations

- No current GPT-host probes were executed.
- The historical v0.15.2 archive was unavailable; historical member paths, checksum, and direct behavior evidence remain unresolved.
- Static validation can prove inventory coverage and reference integrity only.
- Auth and OPSEC details remain protected; the audit records behavior classes and safe boundaries, not challenges, secrets, or protected render strings.
- A grouped viability record preserves member IDs but does not assert that current component names are appropriate successor service boundaries.

## Current viability versus successor disposition

`current_viability_class` answers what the available evidence supports about the current CTS deployment. `proposed_disposition`, `successor_delta`, and `responsibility_split` answer what may be worth specifying later. A successor decision never upgrades a current classification or becomes a golden declaration.
