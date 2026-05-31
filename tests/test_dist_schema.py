"""Fas 6: deploy-kontrakt. dist/scores.json + dist/evidence.json måste validera mot
schemas/{scores,evidence}.schema.json (Draft 2020-12), och ett medvetet trasigt betyg
(score=6 eller ci0>score) ska FAILA — annars biter inte kontraktet."""

from __future__ import annotations

import copy
import json

import pytest
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

from pipeline import DIST_DIR, SCHEMA_DIR


def _load(p):
    with p.open(encoding="utf-8") as fh:
        return json.load(fh)


def _validator(name):
    return Draft202012Validator(_load(SCHEMA_DIR / name))


@pytest.mark.skipif(not (DIST_DIR / "scores.json").exists(), reason="dist saknas; kör pipeline.scorerun")
def test_scores_json_validates_against_schema():
    _validator("scores.schema.json").validate(_load(DIST_DIR / "scores.json"))


@pytest.mark.skipif(not (DIST_DIR / "evidence.json").exists(), reason="dist saknas")
def test_evidence_json_validates_against_schema():
    _validator("evidence.schema.json").validate(_load(DIST_DIR / "evidence.json"))


@pytest.mark.skipif(not (DIST_DIR / "scores.json").exists(), reason="dist saknas")
def test_broken_score_is_rejected():
    v = _validator("scores.schema.json")
    data = _load(DIST_DIR / "scores.json")
    party = next(iter(data["scores"]))
    cat = next(iter(data["scores"][party]))
    bad = copy.deepcopy(data)
    bad["scores"][party][cat]["score"] = 6  # utanför [0,5]
    with pytest.raises(ValidationError):
        v.validate(bad)


@pytest.mark.skipif(not (DIST_DIR / "scores.json").exists(), reason="dist saknas")
def test_ci_brackets_score_in_every_cell():
    # invariant frontend förlitar sig på: ci0 <= score <= ci1.
    data = _load(DIST_DIR / "scores.json")
    for party, cats in data["scores"].items():
        for cid, cs in cats.items():
            lo, hi = cs["ci"]
            assert lo <= cs["score"] <= hi, f"{party}/{cid}: {lo} <= {cs['score']} <= {hi} bröts"
