"""Verifierar att config/*.yaml troget kodifierar modellen i IDEA.md."""

from __future__ import annotations

import re
from pathlib import Path

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
    # ADR 0002: 0,30 A + 0,50 B + 0,20 D. C behålls som nyckel men ger noll poäng.
    sw = config.categories()["subscore_weights"]
    assert (sw["A_agerande"], sw["B_evidens"], sw["C_ansvar"], sw["D_resultat"]) == (30, 50, 0, 20)


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


def test_metodrutan_visar_samma_vikter_som_configen() -> None:
    """Metodrutan i web/app.js skriver vikterna som text och kan inte läsa dem ur configen.

    Utan den här grinden kan en viktändring i scoring.yaml gå igenom medan sajten står
    kvar och påstår de gamla talen. Då beskriver sajten en annan formel än den räknar
    med, vilket är precis vad ADR 0002 och biljett #15 finns för att stoppa.
    """
    app_js = (Path(__file__).resolve().parents[1] / "web" / "app.js").read_text(encoding="utf-8")
    visade = {m[0]: int(m[1]) for m in re.findall(r"<li><b>([ABCD])\.[^(]*\((\d+) %\)", app_js)}
    sw = config.categories()["subscore_weights"]
    vantade = {"A": sw["A_agerande"], "B": sw["B_evidens"], "D": sw["D_resultat"]}
    assert visade == vantade, f"metodrutan visar {visade}, configen säger {vantade}"


def test_metodrutan_listar_inte_maktandelen_som_delpoang() -> None:
    """C väger 0 och får inte stå med bland delarna som ger poäng (ADR 0002 punkt 5)."""
    app_js = (Path(__file__).resolve().parents[1] / "web" / "app.js").read_text(encoding="utf-8")
    assert config.categories()["subscore_weights"]["C_ansvar"] == 0
    assert not re.search(r"<li><b>C\.", app_js), "C står kvar som en delpoäng i metodrutan"
