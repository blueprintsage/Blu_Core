# Documentation Status Header Standard

status: active
owner: docs/dev
last_reviewed: 2026-08-05

## Required status block

Every new or revised markdown file gets a small status block near the top:

```yaml
status: active
owner: docs/domains/<domain>
last_reviewed: YYYY-MM-DD
superseded_by:
notes:
```

## Status values

| Status | Meaning |
|---|---|
| `active` | Current canonical guidance. |
| `working` | Useful draft or work in progress. |
| `untouched` | Preserved but not reviewed in the current pass. Do not delete. |
| `review-needed` | Correctness uncertain. Verify before relying on it. |
| `stale-review` | Probably outdated but may contain useful history. |
| `superseded` | Replaced by another doc. Keep until references are checked. |
| `archive-candidate` | Likely ready to move to `docs/archive/`, not deleted. |
| `archived` | Historical material under `docs/archive/`. |

## Owner values

Use an owner **path**, never a person. People change; paths do not.

## The rule

Do not delete a document because it looks old. First mark it:

```yaml
status: archive-candidate
notes: why it appears superseded
```

Then archive in a later pass, after references are checked. A deleted doc takes
its history with it; a marked doc does not.
