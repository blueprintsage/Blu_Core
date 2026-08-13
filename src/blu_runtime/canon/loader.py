"""Canonical source verification and frozen model-facing envelope rendering.

Non-component support layer (BC-050 §14). This module does NOT own canon,
choose canon, rewrite canon, or determine behavioral precedence. It verifies
golden bytes and mechanically renders the frozen Phase-1 projection. It is not
a Canon Manager.

The envelope is frozen byte-for-byte by BC-050 §3.3. Two golden artifacts enter
the model-facing payload, in this order: Persona, then Operations Law.
`00_Instructions.md` deliberately does not participate; it is deployment and
runtime-entry authority, realized through deterministic wrapper mechanics and
accounted for by the BC-050 §17.2 parity mapping.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

from blu_runtime.contracts.models import (
    CANON_PROJECTION_INVALID,
    CANON_SOURCE_INTEGRITY_MISMATCH,
    CANON_SOURCE_UNAVAILABLE,
    CanonProjection,
)

GOLDEN_ROOT = Path("kernel/golden/v0.22.0")
CHECKSUM_FILE = "SHA256SUMS"

PERSONA_FILE = "01_Persona.md"
OPERATIONS_LAW_FILE = "02_Operations_Law.md"

#: Exactly the two model-facing canon artifacts, in envelope order.
MODEL_FACING_SOURCES = (PERSONA_FILE, OPERATIONS_LAW_FILE)

#: Golden artifacts that must never enter the Python model-facing payload.
EXCLUDED_FROM_ENVELOPE = (
    "00_Instructions.md",
    "03_Exec.md",
    "04_Exec_Library.md",
    "05_Commands.md",
    "06_Programs.md",
)

LF = b"\n"

PERSONA_OPEN = b"[BLU_CANON_PERSONA]"
PERSONA_CLOSE = b"[/BLU_CANON_PERSONA]"
OPERATIONS_LAW_OPEN = b"[BLU_CANON_OPERATIONS_LAW]"
OPERATIONS_LAW_CLOSE = b"[/BLU_CANON_OPERATIONS_LAW]"
BINDING_OPEN = b"[BLU_RUNTIME_BINDING]"
BINDING_CLOSE = b"[/BLU_RUNTIME_BINDING]"

#: Host-mechanics declaration only. Not Persona, not law, not a canon source.
BINDING_LINES = (
    b"deployment=python_lm_studio",
    b"route=ordinary_conversation",
    b"tools=unavailable",
    b"protected_authorization=unavailable",
    b"durable_continuity=unavailable",
    b"artifacts=unavailable",
    b"reminders_and_scheduling=unavailable",
    b"streaming=unavailable",
    b"Do not claim unavailable host capabilities or side effects occurred.",
)


class CanonError(Exception):
    """Canon verification or rendering failure. Always fails closed."""

    def __init__(self, safe_error_code: str, detail: str) -> None:
        super().__init__(detail)
        self.safe_error_code = safe_error_code
        self.detail = detail


@dataclass(frozen=True)
class GoldenSource:
    name: str
    raw: bytes
    digest: str


def render_runtime_binding() -> bytes:
    """Return the frozen host-mechanics block, without a trailing LF."""
    body = b"".join(line + LF for line in BINDING_LINES)
    return BINDING_OPEN + LF + body + BINDING_CLOSE


def read_expected_digests(root: Path) -> dict[str, str]:
    """Parse the golden SHA256SUMS manifest."""
    manifest = root / CHECKSUM_FILE
    if not manifest.is_file():
        raise CanonError(CANON_SOURCE_UNAVAILABLE, "golden checksum manifest is missing")
    expected: dict[str, str] = {}
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        parts = line.split(None, 1)
        if len(parts) != 2:
            raise CanonError(CANON_SOURCE_UNAVAILABLE, "golden checksum manifest is malformed")
        expected[parts[1].strip()] = parts[0].strip().lower()
    return expected


def load_verified_source(root: Path, name: str, expected: dict[str, str]) -> GoldenSource:
    """Read one golden artifact as raw bytes and verify it before any decoding.

    Byte order matters: the digest is taken over the bytes exactly as stored.
    No CRLF/LF normalization, no BOM stripping, no decode-then-reencode. A
    line-ending-converted checkout therefore fails here and never reaches
    rendering, which is what makes the rendered envelope digest portable.
    """
    target = root / name
    if not target.is_file():
        raise CanonError(CANON_SOURCE_UNAVAILABLE, f"golden source is missing: {name}")
    try:
        raw = target.read_bytes()
    except OSError as exc:  # pragma: no cover - filesystem dependent
        raise CanonError(CANON_SOURCE_UNAVAILABLE, f"golden source is unreadable: {name}") from exc
    if name not in expected:
        raise CanonError(CANON_SOURCE_UNAVAILABLE, f"golden source is unpinned: {name}")
    digest = hashlib.sha256(raw).hexdigest()
    if digest != expected[name]:
        raise CanonError(
            CANON_SOURCE_INTEGRITY_MISMATCH, f"golden source digest mismatch: {name}"
        )
    return GoldenSource(name=name, raw=raw, digest=digest)


def render_envelope(persona: bytes, operations_law: bytes) -> bytes:
    """Render the frozen Phase-1 system prompt as an exact byte sequence.

    Segment order is fixed by BC-050 §3.3. Canonical bytes are never trimmed,
    padded, re-encoded, or line-ending converted, and no trailing LF follows the
    final `[/BLU_RUNTIME_BINDING]`.

    The source asymmetry is expected and must not be "fixed": `01_Persona.md`
    ends with LF and `02_Operations_Law.md` does not, so the two blocks render
    with different closing seams. Guaranteeing a newline before each closing
    delimiter would change the Persona block and break the digest.
    """
    return b"".join(
        (
            PERSONA_OPEN,
            LF,
            persona,
            LF,
            PERSONA_CLOSE,
            LF,
            OPERATIONS_LAW_OPEN,
            LF,
            operations_law,
            LF,
            OPERATIONS_LAW_CLOSE,
            LF,
            render_runtime_binding(),
        )
    )


def load_projection(root: Path | str = GOLDEN_ROOT) -> CanonProjection:
    """Verify the golden model-facing sources and render the frozen projection."""
    golden_root = Path(root)
    expected = read_expected_digests(golden_root)
    sources = [load_verified_source(golden_root, name, expected) for name in MODEL_FACING_SOURCES]
    persona, operations_law = sources

    envelope = render_envelope(persona.raw, operations_law.raw)

    # The projection must be valid UTF-8 and must end exactly at the closing
    # delimiter. Both are structural guarantees the digest depends on.
    try:
        envelope.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise CanonError(CANON_PROJECTION_INVALID, "rendered projection is not valid UTF-8") from exc
    if not envelope.endswith(BINDING_CLOSE):
        raise CanonError(CANON_PROJECTION_INVALID, "rendered projection has a trailing byte")

    return CanonProjection(
        system_prompt_bytes=envelope,
        digest=hashlib.sha256(envelope).hexdigest(),
        source_digests={source.name: source.digest for source in sources},
    )
