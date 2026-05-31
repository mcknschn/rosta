"""Verifierar att JSON-schemana är välformade och att fixturerna validerar."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema.exceptions import ValidationError

from pipeline import schema

FIXTURES = Path(__file__).parent / "fixtures"


def _load(name: str) -> object:
    with (FIXTURES / name).open(encoding="utf-8") as fh:
        return json.load(fh)


@pytest.mark.parametrize("name", schema.SCHEMAS)
def test_schema_is_wellformed(name: str) -> None:
    schema.validator(name)  # check_schema körs internt


@pytest.mark.parametrize(
    "schema_name, fixture",
    [
        ("observation", "sample_observation.json"),
        ("action", "sample_action.json"),
        ("responsibility", "sample_responsibility.json"),
        ("claim", "sample_claim.json"),
        ("indicator_effect", "sample_indicator_effect.json"),
        ("scores", "sample_scores.json"),
        ("evidence", "sample_evidence.json"),
    ],
)
def test_fixture_validates(schema_name: str, fixture: str) -> None:
    schema.validate(schema_name, _load(fixture))


def test_claim_requires_source_refs() -> None:
    bad = _load("sample_claim.json")
    assert isinstance(bad, dict)
    bad = {**bad, "source_refs": []}  # bryter minItems=1 (spårbarhetskravet)
    with pytest.raises(ValidationError):
        schema.validate("claim", bad)


def test_score_out_of_range_rejected() -> None:
    scores = _load("sample_scores.json")
    scores["scores"]["M"]["ekonomi"]["score"] = 9.9  # utanför 0-5
    with pytest.raises(ValidationError):
        schema.validate("scores", scores)
