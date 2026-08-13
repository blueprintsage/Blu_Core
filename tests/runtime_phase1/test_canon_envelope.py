"""Byte-exact model-facing envelope, digest reproducibility, and One-Blu law."""

from __future__ import annotations

import hashlib
import shutil
import tempfile
import unittest
from pathlib import Path

from tests.runtime_phase1.support import ROOT

from blu_runtime.canon import loader
from blu_runtime.contracts.models import (
    CANON_SOURCE_INTEGRITY_MISMATCH,
    CANON_SOURCE_UNAVAILABLE,
)

#: Pinned by BC-050 §3.4 against base 973589ee.
PINNED_DIGEST = "103e0e2dd94183c914dc8c46e3ac376af516382548e17af40c14c27d3319f142"
PINNED_LENGTH = 36887

GOLDEN = ROOT / "kernel/golden/v0.22.0"


class EnvelopeCompositionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.projection = loader.load_projection(GOLDEN)
        self.envelope = self.projection.system_prompt_bytes

    def test_reproduces_pinned_vector(self) -> None:
        self.assertEqual(self.projection.digest, PINNED_DIGEST)
        self.assertEqual(len(self.envelope), PINNED_LENGTH)

    def test_digest_is_lowercase_hex_of_length_64(self) -> None:
        self.assertEqual(len(self.projection.digest), 64)
        self.assertEqual(self.projection.digest, self.projection.digest.lower())
        int(self.projection.digest, 16)

    def test_digest_is_over_the_rendered_envelope(self) -> None:
        self.assertEqual(hashlib.sha256(self.envelope).hexdigest(), self.projection.digest)
        persona = (GOLDEN / "01_Persona.md").read_bytes()
        operations_law = (GOLDEN / "02_Operations_Law.md").read_bytes()
        # Explicitly NOT any of the rejected derivations.
        self.assertNotEqual(self.projection.digest, hashlib.sha256(persona).hexdigest())
        self.assertNotEqual(self.projection.digest, hashlib.sha256(operations_law).hexdigest())
        self.assertNotEqual(
            self.projection.digest, hashlib.sha256(persona + operations_law).hexdigest()
        )
        concatenated_source_digests = "".join(
            hashlib.sha256(part).hexdigest() for part in (persona, operations_law)
        ).encode("utf-8")
        self.assertNotEqual(
            self.projection.digest, hashlib.sha256(concatenated_source_digests).hexdigest()
        )

    def test_final_byte_is_the_closing_delimiter(self) -> None:
        self.assertTrue(self.envelope.endswith(b"[/BLU_RUNTIME_BINDING]"))
        self.assertEqual(self.envelope[-1:], b"]")
        self.assertNotEqual(self.envelope[-1:], b"\n")

    def test_canonical_bytes_appear_verbatim_and_unmodified(self) -> None:
        persona = (GOLDEN / "01_Persona.md").read_bytes()
        operations_law = (GOLDEN / "02_Operations_Law.md").read_bytes()
        self.assertIn(persona, self.envelope)
        self.assertIn(operations_law, self.envelope)

    def test_source_asymmetry_is_preserved_at_both_seams(self) -> None:
        """Persona ends with LF and Operations Law does not.

        The seams therefore differ. Normalizing them would change the Persona
        block and break the digest.
        """
        self.assertTrue((GOLDEN / "01_Persona.md").read_bytes().endswith(b"\n"))
        self.assertFalse((GOLDEN / "02_Operations_Law.md").read_bytes().endswith(b"\n"))
        self.assertIn(b"\n\n[/BLU_CANON_PERSONA]\n", self.envelope)
        self.assertIn(b".\n[/BLU_CANON_OPERATIONS_LAW]\n", self.envelope)

    def test_segment_order_is_persona_then_operations_law_then_binding(self) -> None:
        order = [
            self.envelope.index(b"[BLU_CANON_PERSONA]"),
            self.envelope.index(b"[/BLU_CANON_PERSONA]"),
            self.envelope.index(b"[BLU_CANON_OPERATIONS_LAW]"),
            self.envelope.index(b"[/BLU_CANON_OPERATIONS_LAW]"),
            self.envelope.index(b"[BLU_RUNTIME_BINDING]"),
            self.envelope.index(b"[/BLU_RUNTIME_BINDING]"),
        ]
        self.assertEqual(order, sorted(order))

    def test_envelope_starts_exactly_at_the_opening_delimiter(self) -> None:
        self.assertTrue(self.envelope.startswith(b"[BLU_CANON_PERSONA]\n"))

    def test_envelope_is_valid_utf8(self) -> None:
        self.assertIsInstance(self.projection.system_prompt, str)

    def test_runtime_binding_declares_only_host_mechanics(self) -> None:
        binding = loader.render_runtime_binding().decode("utf-8")
        for declaration in (
            "deployment=python_lm_studio",
            "route=ordinary_conversation",
            "tools=unavailable",
            "protected_authorization=unavailable",
            "durable_continuity=unavailable",
            "artifacts=unavailable",
            "reminders_and_scheduling=unavailable",
            "streaming=unavailable",
        ):
            self.assertIn(declaration, binding)
        self.assertFalse(binding.endswith("\n"))

    def test_excluded_golden_artifacts_do_not_enter_the_envelope(self) -> None:
        """`00_Instructions.md` and the runtime capsules stay out of the payload."""
        for name in loader.EXCLUDED_FROM_ENVELOPE:
            with self.subTest(name=name):
                body = (GOLDEN / name).read_bytes()
                self.assertNotIn(body, self.envelope)

    def test_00_instructions_distinctive_text_is_absent(self) -> None:
        for phrase in (b"## Runtime Entry Boundary", b"## Bootloader", b"## Repo Bootstrap Bridge"):
            self.assertNotIn(phrase, self.envelope)

    def test_source_digests_match_golden_manifest(self) -> None:
        expected = loader.read_expected_digests(GOLDEN)
        for name, digest in self.projection.source_digests.items():
            self.assertEqual(digest, expected[name])


class CanonFailureTests(unittest.TestCase):
    def setUp(self) -> None:
        self._temp = tempfile.TemporaryDirectory()
        self.directory = Path(self._temp.name)
        self.addCleanup(self._temp.cleanup)
        for name in ("SHA256SUMS", *loader.MODEL_FACING_SOURCES):
            shutil.copy(GOLDEN / name, self.directory / name)

    def test_missing_source_fails_closed(self) -> None:
        (self.directory / "01_Persona.md").unlink()
        with self.assertRaises(loader.CanonError) as caught:
            loader.load_projection(self.directory)
        self.assertEqual(caught.exception.safe_error_code, CANON_SOURCE_UNAVAILABLE)

    def test_digest_mismatch_fails_closed(self) -> None:
        target = self.directory / "02_Operations_Law.md"
        target.write_bytes(target.read_bytes() + b" tampered")
        with self.assertRaises(loader.CanonError) as caught:
            loader.load_projection(self.directory)
        self.assertEqual(caught.exception.safe_error_code, CANON_SOURCE_INTEGRITY_MISMATCH)

    def test_line_ending_conversion_is_detected_before_rendering(self) -> None:
        """A CRLF-converted checkout must fail integrity, not silently drift."""
        target = self.directory / "01_Persona.md"
        target.write_bytes(target.read_bytes().replace(b"\n", b"\r\n"))
        with self.assertRaises(loader.CanonError) as caught:
            loader.load_projection(self.directory)
        self.assertEqual(caught.exception.safe_error_code, CANON_SOURCE_INTEGRITY_MISMATCH)

    def test_missing_checksum_manifest_fails_closed(self) -> None:
        (self.directory / "SHA256SUMS").unlink()
        with self.assertRaises(loader.CanonError) as caught:
            loader.load_projection(self.directory)
        self.assertEqual(caught.exception.safe_error_code, CANON_SOURCE_UNAVAILABLE)


class OneBluCanonTests(unittest.TestCase):
    """There is one Blu canon and no Python-specific behavioral fork."""

    FORBIDDEN = (
        "python_persona.md",
        "local_blu_persona.md",
        "lm_studio_persona.md",
        "blu_persona.md",
        "persona.md",
    )

    def test_no_provider_or_python_specific_persona_exists(self) -> None:
        for path in (ROOT / "src").rglob("*"):
            if path.is_file():
                self.assertNotIn(path.name.lower(), self.FORBIDDEN, f"behavioral fork: {path}")

    def test_runtime_ships_no_markdown_behavioral_source(self) -> None:
        self.assertEqual(list((ROOT / "src").rglob("*.md")), [])

    def test_model_facing_sources_are_exactly_persona_and_operations_law(self) -> None:
        self.assertEqual(
            loader.MODEL_FACING_SOURCES, ("01_Persona.md", "02_Operations_Law.md")
        )

    def test_canon_is_loaded_from_the_golden_tree(self) -> None:
        self.assertEqual(loader.GOLDEN_ROOT, Path("kernel/golden/v0.22.0"))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
