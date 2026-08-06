# Runtime Decisions

status: active
owner: docs/domains/runtime
last_reviewed: 2026-08-06

- Bootstrap authority is defined by `AGENTS.md` and
  `docs/sources/authority_map.md`.

## 2026-08-06 — Successor-runtime Auth and OPSEC route boundary

Approved for successor-runtime design; this is not a retroactive change to the
golden CTS source:

- Auth authorizes Admin-level users and owns the user-facing authentication
  workflow.
- Auth may use the declared `auth` lane.
- OPSEC protects against unauthorized ID challenge access and unauthorized
  copying, cloning, recreation, or disclosure of Blu's protected kernel/runtime
  sources.
- OPSEC is a mandatory pre-ingress security restraint, not an ordinary
  RuntimeGate lane.
- The current CTS source preserves OPSEC interception behavior but does not
  formally declare its lane or pre-ingress restraint contract.
- Generated BC-010 contracts must preserve that source gap rather than
  pretending the successor decision already exists in the golden kernel.
