"""Offline golden-test för MPF-serien (forsvarsvilja, transkriberad config).

Indikatorn forsvarsvilja = andel som anser att Sverige bör göra väpnat motstånd vid ett militärt
angrepp även om utgången är oviss (config/forsvarsvilja.yaml, ur MPF Opinioner 2025 s.87). Öppnar
submåttet civil_beredskap (forsvar). Pinnar årsvärdena, kontrollerar radform, kanonisk riktning (up),
att värdet = ja_absolut + ja_kanske, och att 2019-luckan respekteras. Ingen nätverkstrafik.
"""

from __future__ import annotations

from pipeline import config
from pipeline.sources import mpf

# Facit: andel JA (ja_absolut + ja_kanske), per mätår, ur MPF Opinioner 2025 s.87 (verifierad 2026-06-12).
GOLDEN = {
    "2014": 75, "2015": 75, "2016": 72, "2017": 71, "2018": 72,
    "2020": 70, "2021": 70, "2022": 78, "2023": 79, "2024": 79, "2025": 75,
}


def test_serie_matchar_pinnade_varden() -> None:
    rows = mpf.build_forsvarsvilja_observations()
    by_year = {r["period"]: int(r["value"]) for r in rows}
    assert by_year == GOLDEN


def test_lucka_2019_utelamnad() -> None:
    """2019 saknar mätning -> året finns ej i serien (D hoppar över icke-konsekutiva övergångar)."""
    rows = mpf.build_forsvarsvilja_observations()
    years = {r["period"] for r in rows}
    assert "2019" not in years
    assert "2018" in years and "2020" in years


def test_varde_ar_ja_summan() -> None:
    """value = ja_absolut + ja_kanske för varje år (intern konsistens i configen)."""
    cfg = config.forsvarsvilja()
    for year, e in cfg["years"].items():
        assert e["value"] == e["ja_absolut"] + e["ja_kanske"], f"{year}: value != ja_absolut+ja_kanske"


def test_radform_kanonisk() -> None:
    r = next(r for r in mpf.build_forsvarsvilja_observations() if r["period"] == "2022")
    assert r["indicator"] == "forsvarsvilja"
    assert r["category"] == "forsvar"
    assert r["submeasure"] == "civil_beredskap"
    assert r["geography"] == "Riket"
    assert r["id"] == "obs:mpf:forsvarsvilja:2022"
    assert r["source_ref"] == "mpf:forsvarsvilja:2022"
    assert "forsvarsvilja" in mpf.INDICATORS


def test_builder_ren_funktion_injicerad_cfg() -> None:
    cfg = {
        "indicator": "forsvarsvilja", "category": "forsvar",
        "submeasure": "civil_beredskap", "unit": "%",
        "years": {2014: {"value": 75}, 2015: {"value": 75}},
    }
    rows = mpf.build_forsvarsvilja_observations(cfg)
    assert [(r["period"], r["value"]) for r in rows] == [("2014", 75.0), ("2015", 75.0)]


def test_indikator_kanonisk_civil_beredskap_riktning_up() -> None:
    forsvar = next(c for c in config.categories()["categories"] if c["id"] == "forsvar")
    ind = next(i for i in forsvar["indicators"] if i["id"] == "forsvarsvilja")
    assert ind["direction"] == "up"
    assert ind["submeasure"] == "civil_beredskap"


def test_config_har_kalla() -> None:
    """En gemensam MPF-källa (source_index) + varje år ett heltalsvärde."""
    cfg = config.forsvarsvilja()
    assert cfg["indicator"] == "forsvarsvilja"
    assert str(cfg["source_index"]).startswith("https://")
    for year, e in cfg["years"].items():
        assert isinstance(e["value"], int), f"{year}: värde ej heltal"
