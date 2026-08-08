# Successor Kernel Specification Records

status: review
owner: docs/domains/runtime
last_reviewed: 2026-08-08
assignment: BC-018

## Purpose

This namespace is the machine-readable design companion to the BC-018
successor-kernel architecture. It specifies boundaries and contracts only. It
does not implement a Python runtime, prove host capability, create persistence,
or supersede the current Blu v0.22.0 CTS.

The immutable current source authority remains the seven-file CTS source set:
`00_Instructions.md` as `deployment_instruction`, and `01_Persona.md` through
`06_Programs.md` as `kernel_runtime_capsule`.

## Records

- `component_registry.json`: seven proposed components/boundaries, including
  four deterministic-core components.
- `behavior_placement.json`: one primary architectural domain for every
  required recoverable behavior.
- `interface_registry.json`: generic model, host, authorization, source,
  skill, artifact, scheduling, time, and continuity interfaces.
- `packet_registry.json`: the minimum eight-packet control vocabulary.
- `error_model.json`: common terminal statuses and failure policies.
- `unresolved_register.json`: questions BC-018 does not force closed.
- `traceability.json`: evidence catalog and backward requirement traces.

## Interpretation rules

- `deterministically_specifiable` is not `actually_implemented`.
- A typed request is not proof that a provider exists or acted.
- Host services are credited only through verified capability evidence and
  receipts.
- Durable state is credited only through a continuity-provider receipt.
- Natural-language source support remains partly model-dependent until a real
  verifier can establish claim/evidence relations.
- Historical module identity never justifies a successor component.

## Validation

```text
python tools/validate_successor_kernel_spec.py
python -m unittest discover -s tests/successor_kernel -p "test_*.py"
```

The validator checks record integrity and architectural guardrails. It does not
validate runtime behavior or semantic parity.
