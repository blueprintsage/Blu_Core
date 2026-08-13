"""Blu Core Python Runtime Phase 1 (BC-050).

One Blu canon, two deployments. This package is the Python deployment wrapper.
It holds no Persona, no behavioral law, and no independent Blu identity; the
model-facing behavioral authority is loaded verbatim from the golden CTS by
`blu_runtime.canon.loader`.
"""

from __future__ import annotations

__all__ = ["PHASE", "SUPPORTED_ROUTE"]

PHASE = "phase1_ordinary_conversation"
SUPPORTED_ROUTE = "ordinary_conversation"
