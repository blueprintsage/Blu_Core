"""Shared fixtures and deterministic doubles for BC-050 tests.

Synthetic test policy != production protected policy.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]

# Offline fallback: BC-050 §16 permits running the suite with `src` on the
# import path when the build backend is unavailable for an editable install.
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

SYNTHETIC_POLICY_FIXTURE = ROOT / "tests/security/fixtures/synthetic_policy.json"

#: The six Cf code points the C1 corpus requires.
REQUIRED_CF = ("​", "­", "‍", "‌", "﻿", "⁠")

PROTECTED_PHRASE = "cerulean comet charter"
BLOCK_ONLY_PHRASE = "zircon café protocol"


def load_reference():
    """Load the BC-041-C1 conformance oracle exactly as published."""
    spec = importlib.util.spec_from_file_location(
        "bc041_reference", ROOT / "tools/validate_opsec_contracts.py"
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def synthetic_policy() -> dict[str, Any]:
    return json.loads(SYNTHETIC_POLICY_FIXTURE.read_text(encoding="utf-8"))["policy"]


def write_policy_file(directory: Path, policy: dict[str, Any] | str) -> tuple[Path, str]:
    """Write a policy payload and return its path plus SHA-256."""
    target = directory / "synthetic_policy.json"
    payload = policy if isinstance(policy, str) else json.dumps(policy)
    target.write_bytes(payload.encode("utf-8"))
    return target, hashlib.sha256(target.read_bytes()).hexdigest()


def policy_reference() -> dict[str, str]:
    return {
        "kind": "environment_file",
        "locator_env": "BLU_TEST_POLICY_PATH",
        "sha256_env": "BLU_TEST_POLICY_SHA256",
    }


def policy_environment(path: Path, digest: str) -> dict[str, str]:
    return {"BLU_TEST_POLICY_PATH": str(path), "BLU_TEST_POLICY_SHA256": digest}


def runtime_config_document(**overrides: Any) -> dict[str, Any]:
    """A schema-valid portable configuration document."""
    document: dict[str, Any] = {
        "model_provider": {
            "type": "lm_studio",
            "api_profile": "native_rest_v1",
            "endpoint": "http://127.0.0.1:1234",
            "selected_model": "synthetic-model-key",
            "timeout_seconds": 60,
            "context": {"requested_tokens": 4096, "require_observed_capacity": True},
            "stream": False,
            "store": False,
            "authentication_env": None,
        },
        "continuity_provider": {"type": "unavailable", "required_for_phase1": False},
        "host_adapter": {"type": "terminal"},
        "runtime": {
            "mode": "phase1_ordinary_conversation",
            "logging": "safe",
            "protected_policy_ref": policy_reference(),
        },
        "development": {
            "fixture_provider": None,
            "allow_unverified_capabilities": False,
            "allow_protected_routes": False,
        },
    }
    document.update(overrides)
    return document


def model_inventory(
    model_key: str = "synthetic-model-key",
    loaded: bool = True,
    context_length: int | None = 8192,
    model_type: str = "llm",
    instances: int = 1,
) -> dict[str, Any]:
    record: dict[str, Any] = {"id": model_key, "type": model_type, "loaded_instances": []}
    if loaded:
        for index in range(instances):
            instance: dict[str, Any] = {"instance_id": f"{model_key}:{index}"}
            if context_length is not None:
                instance["context_length"] = context_length
            record["loaded_instances"].append(instance)
    return {"data": [record]}


def chat_response(instance_id: str, text: str = "Hello.", kinds: tuple[str, ...] = ("message",)) -> dict[str, Any]:
    output: list[dict[str, Any]] = []
    for kind in kinds:
        if kind == "message":
            output.append({"type": "message", "content": text})
        elif kind == "reasoning":
            output.append({"type": "reasoning", "content": "internal reasoning must not print"})
        else:
            output.append({"type": kind, "tool_name": "shell", "arguments": "{}"})
    return {"model_instance_id": instance_id, "output": output}


class RecordingTransport:
    """Deterministic transport double that records every call."""

    def __init__(self, inventory: Any = None, chat: Any = None, raises: Exception | None = None) -> None:
        self.inventory = inventory
        self.chat = chat
        self.raises = raises
        self.get_calls: list[str] = []
        self.post_calls: list[tuple[str, dict[str, Any]]] = []

    def get(self, url: str) -> Any:
        self.get_calls.append(url)
        if self.raises is not None:
            raise self.raises
        return self.inventory

    def post(self, url: str, payload: dict[str, Any]) -> Any:
        self.post_calls.append((url, payload))
        if isinstance(self.chat, Exception):
            raise self.chat
        return self.chat
