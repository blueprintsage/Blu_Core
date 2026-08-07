# Historical Behavioral Archaeology

status: review
owner: docs/domains/runtime
last_reviewed: 2026-08-07
assignment: BC-017

## Purpose

This directory records bounded behavioral archaeology across Blu's historical
kernel families. It separates current source truth, Dad's observations,
historical declarations, mechanically scaffolded behavior, cross-version
persistence, inference, and unavailable evidence. It recommends recoverable
contracts; it does not restore a historical runtime.

## Authority and safety boundary

The current source of truth remains `kernel/golden/v0.22.0/**`. Historical
archives remain non-authoritative behavioral references. No archive payload,
private path, protected answer, secret, or control-plane source is published
here. Legacy PASS is chronology-only and is never a recovery target. Modern
PASS is outside BC-017.

Markdown can specify behavior and can shape model-facing conduct, but it does
not prove host persistence, autonomous scheduling, background wake-up, tool
execution, or historical reliability. Those claims require positive host and
runtime evidence.

## Evidence model

- `boundary_specimens.json` chooses family boundaries and focused drilldowns.
- `evidence_register.json` gives every factual finding a sanitized locator and
  keeps owner observations distinct from source findings.
- `behavioral_evidence_report.md` explains what the evidence supports.
- `transition_map.md` traces behavior movement and contraction.
- `behavior_recovery_matrix.md` assigns only bounded recovery dispositions.

Evidence grades are A (direct), B (direct with a limitation), C (weak or
incomplete), O (owner observation), and U (unavailable/unproven). Archive member
paths are suffix locators under canonical inventory records; they are not
filesystem locations.

## Selection method

Each readable version family receives a first and last specimen when chronology
supports that choice. Ambiguity is preserved for v0.4 and the v0.8 opening.
Unsupported Deflate64 archives and source-folder records may bound chronology
but cannot support behavioral deltas. Explicit gaps are not filled by
inference.

Focused drilldowns cover Exec emergence, School, MMU, reminders/time, mood,
Auth, OPSEC, mega-Exec contraction, and the v0.21 restructuring. Read Lane is
secondary evidence at the first v0.20 specimen; MMU is the representative
selection.

## Reproduction

Run:

```text
python tools/validate_historical_behavioral_archaeology.py
python -m unittest tests.historical_archaeology.test_validate_historical_behavioral_archaeology
git diff --check
```

The validator checks canonical IDs, supported specimen use, source labels,
locator coverage, path sanitization, disposition vocabulary, the Faithfulness
shipping boundary, review state, absence of copied payloads, and golden
checksums.
