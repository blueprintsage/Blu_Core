"""Portable Phase-1 configuration loading and validation.

Non-component support layer (BC-050 §14).

Configuration is a claim, never capability evidence. `selected_model = X` does
not prove X is loaded; `endpoint = localhost` does not prove LM Studio is
running. Operational evidence is obtained by the Model Execution Boundary at
boot, not inferred from these values.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from blu_runtime.contracts.models import CONFIG_INVALID

CONFIG_SCHEMA = Path("readiness/schemas/runtime_config.schema.json")


class ConfigError(Exception):
    """Configuration is absent, unreadable, or contract-invalid."""

    def __init__(self, detail: str) -> None:
        super().__init__(detail)
        self.safe_error_code = CONFIG_INVALID
        self.detail = detail


@dataclass(frozen=True)
class ProtectedPolicyRef:
    """Opaque, portable binding. Environment variable NAMES only."""

    kind: str
    locator_env: str
    sha256_env: str

    def as_dict(self) -> dict[str, str]:
        return {"kind": self.kind, "locator_env": self.locator_env, "sha256_env": self.sha256_env}


@dataclass(frozen=True)
class RuntimeConfig:
    endpoint: str
    selected_model: str
    timeout_seconds: float
    requested_tokens: int
    require_observed_capacity: bool
    stream: bool
    store: bool
    authentication_env: str | None
    continuity_type: str
    host_adapter: str
    mode: str
    logging: str
    protected_policy_ref: ProtectedPolicyRef
    raw: dict[str, Any]


def _load_schema(schema_path: Path) -> dict[str, Any]:
    if not schema_path.is_file():
        raise ConfigError(f"configuration schema is missing: {schema_path}")
    return json.loads(schema_path.read_text(encoding="utf-8"))


def validate_document(document: Any, schema_path: Path | str = CONFIG_SCHEMA) -> None:
    """Validate a configuration document against the frozen portable schema."""
    schema = _load_schema(Path(schema_path))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(document), key=lambda item: list(item.path))
    if errors:
        first = errors[0]
        location = "/".join(str(part) for part in first.path) or "<root>"
        raise ConfigError(f"configuration is contract-invalid at {location}: {first.message}")


def from_document(document: Any, schema_path: Path | str = CONFIG_SCHEMA) -> RuntimeConfig:
    """Validate and project a configuration document into a typed record."""
    validate_document(document, schema_path)
    provider = document["model_provider"]
    runtime = document["runtime"]
    reference = runtime["protected_policy_ref"]
    return RuntimeConfig(
        endpoint=provider["endpoint"],
        selected_model=provider["selected_model"],
        timeout_seconds=float(provider["timeout_seconds"]),
        requested_tokens=int(provider["context"]["requested_tokens"]),
        require_observed_capacity=bool(provider["context"]["require_observed_capacity"]),
        stream=bool(provider["stream"]),
        store=bool(provider["store"]),
        authentication_env=provider["authentication_env"],
        continuity_type=document["continuity_provider"]["type"],
        host_adapter=document["host_adapter"]["type"],
        mode=runtime["mode"],
        logging=runtime["logging"],
        protected_policy_ref=ProtectedPolicyRef(
            kind=reference["kind"],
            locator_env=reference["locator_env"],
            sha256_env=reference["sha256_env"],
        ),
        raw=document,
    )


def load(path: Path | str, schema_path: Path | str = CONFIG_SCHEMA) -> RuntimeConfig:
    """Load and validate portable runtime configuration from disk."""
    target = Path(path)
    if not target.is_file():
        raise ConfigError(f"configuration file is missing: {target}")
    try:
        document = json.loads(target.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ConfigError(f"configuration file is malformed: {target}") from exc
    return from_document(document, schema_path)
