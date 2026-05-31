"""Verifierar att config/*.yaml troget kodifierar modellen i IDEA.md."""

from __future__ import annotations

import pytest

from pipeline import config


def test_validate_passes() -> None:
    config.validate()  # höjer ConfigError vid brott mot invariant


def test_seven_categories() -> None:
    assert len(config.category_ids()) == 7


def test_eight_parties() -> None:
    assert config.party_codes() == ["S", "M", "SD", "C", "V", "KD", "L", "MP"]


def test_standard_weights_sum_to_100() -> None:
    cats = config.categories()["categories"]
    assert sum(c["standard_weight"] for c in cats) == pytest.approx(100)


@pytest.mark.parametrize("category", config.categories()["categories"], ids=lambda c: c["id"])
def test_submeasure_weights_sum_to_100(category: dict) -> None:
    assert sum(s["weight"] for s in category["submeasures"]) == pytest.approx(100)


def test_subscore_weights_match_idea_formula() -> None:
    sw = config.categories()["subscore_weights"]
    assert (sw["A_agerande"], sw["B_evidens"], sw["C_ansvar"], sw["D_resultat"]) == (40, 35, 15, 10)


def test_every_indicator_maps_to_known_submeasure() -> None:
    for cat in config.categories()["categories"]:
        sub_ids = {s["id"] for s in cat["submeasures"]}
        for ind in cat.get("indicators", []):
            assert ind["submeasure"] in sub_ids, f"{cat['id']}/{ind['id']}"
            assert ind["direction"] in {"up", "down", "target"}


def test_sources_feeds_reference_valid_categories() -> None:
    cat_ids = set(config.category_ids())
    for sid, src in config.sources()["sources"].items():
        for feed in src.get("feeds", []):
            if ":" in feed:
                letter, cat = feed.split(":", 1)
                assert letter in {"A", "B", "C", "D"}, f"{sid}: {feed}"
                assert cat in cat_ids, f"{sid}: okänd kategori '{cat}'"
            else:
                assert feed in {"A", "B", "C", "D"}, f"{sid}: {feed}"


def test_scoring_uncertainty_block_is_consistent() -> None:
    unc = config.scoring()["uncertainty"]
    conf = unc["confidence_numeric"]
    assert all(0.0 <= v <= 1.0 for v in conf.values())
    assert set(unc["default_subscore_certainty"]) == {"A", "B", "C", "D"}
    assert all(level in conf for level in unc["default_subscore_certainty"].values())


def test_normalization_neutral_matches_score_default() -> None:
    assert config.scoring()["normalization"]["default"]["neutral"] == 2.5
