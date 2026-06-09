"""Offline golden-test för Sverigesmiljomal-serien (hackande_faglar_skog, transkriberat index).

Indikatorn hackande_faglar_skog = samlat skogsfågelindex (basår 2002=100, Svensk Fågeltaxering/
Lunds universitet via sverigesmiljomal.se). Öppnar submåttet biologisk_mangfald (klimat). Pinnar
ankarvärden, radform, kanonisk indikator (ny, riktning up) och att basåret är 100. Ingen nätverkstrafik.
"""

from __future__ import annotations

from pipeline import config
from pipeline.sources import sverigesmiljomal

# Facit: indexvärden (basår 2002=100), ankarår ur portalens Highcharts-serie.
GOLDEN = {"2002": 100.0, "2018": 89.54, "2022": 121.32, "2024": 109.07}


def test_serie_matchar_pinnade_ankarvarden() -> None:
    rows = sverigesmiljomal.build_faglar_observations()
    by_year = {r["period"]: float(r["value"]) for r in rows}
    for year, val in GOLDEN.items():
        assert by_year[year] == val


def test_basar_2002_ar_100() -> None:
    rows = sverigesmiljomal.build_faglar_observations()
    by_year = {r["period"]: float(r["value"]) for r in rows}
    assert by_year["2002"] == 100.0


def test_serie_23_ar_2002_2024() -> None:
    rows = sverigesmiljomal.build_faglar_observations()
    years = sorted(r["period"] for r in rows)
    assert len(years) == 23
    assert years[0] == "2002" and years[-1] == "2024"


def test_radform_kanonisk() -> None:
    r = next(r for r in sverigesmiljomal.build_faglar_observations() if r["period"] == "2024")
    assert r["indicator"] == "hackande_faglar_skog"
    assert r["category"] == "klimat"
    assert r["submeasure"] == "biologisk_mangfald"
    assert r["geography"] == "Riket"
    assert r["id"] == "obs:sverigesmiljomal:hackande_faglar_skog:2024"
    assert r["source_ref"] == "sverigesmiljomal:hackande_faglar_skog:2024"
    assert "hackande_faglar_skog" in sverigesmiljomal.INDICATORS


def test_builder_ren_funktion_injicerad_cfg() -> None:
    cfg = {
        "indicator": "hackande_faglar_skog", "category": "klimat",
        "submeasure": "biologisk_mangfald", "unit": "index",
        "years": {2002: 100.0, 2003: 106.42},
    }
    rows = sverigesmiljomal.build_faglar_observations(cfg)
    assert [(r["period"], r["value"]) for r in rows] == [("2002", 100.0), ("2003", 106.42)]


def test_indikator_kanonisk_klimat_riktning_up() -> None:
    klimat = next(c for c in config.categories()["categories"] if c["id"] == "klimat")
    ind = next(i for i in klimat["indicators"] if i["id"] == "hackande_faglar_skog")
    assert ind["direction"] == "up"
    assert ind["submeasure"] == "biologisk_mangfald"
