"""JSON Schema-validering av pipeline-objekt och deploy-artefakter."""

from __future__ import annotations

import json
from functools import cache
from typing import Any

from jsonschema import Draft202012Validator

from . import SCHEMA_DIR

SCHEMAS = (
    "observation",
    "action",
    "responsibility",
    "claim",
    "indicator_effect",
    "scores",
    "evidence",
    "robustness",
)


@cache
def load_schema(name: str) -> dict[str, Any]:
    path = SCHEMA_DIR / f"{name}.schema.json"
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


@cache
def validator(name: str) -> Draft202012Validator:
    schema = load_schema(name)
    Draft202012Validator.check_schema(schema)  # själva schemat är välformat
    return Draft202012Validator(schema)


def validate(name: str, instance: Any) -> None:
    """Validerar instance mot det namngivna schemat. Höjer ValidationError vid fel."""
    validator(name).validate(instance)


def is_valid(name: str, instance: Any) -> bool:
    return validator(name).is_valid(instance)
