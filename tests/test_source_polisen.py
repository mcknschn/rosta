"""Offline golden-test för Polisen-skjutningsserien (transkriberad config/skjutningar.yaml).

Pinnar de korsverifierade nationella årstotalerna (regionsumma == PDF:ens Totalt-rad vid
transkribering, se pipeline/tools/skjutningar_transcribe.py) och kontrollerar radform +
att indikatorn är kanonisk (trygghet, riktning down). Ingen nätverkstrafik.
"""

from __future__ import annotations

from pipeline import config
from pipeline.sources import polisen

# Facit: nationella bekräftade skjutningar per år (Polisen), transkriberade 2026-06-03.
GOLDEN = {
    "2017": 281, "2018": 325, "2019": 360, "2020": 379, "2021": 344,
    "2022": 391, "2023": 368, "2024": 296, "2025": 158,
}


def test_skjutningar_serie_matchar_pinnade_varden() -> None:
    rows = polisen.build_skjutningar_observations()
    by_year = {r["period"]: int(r["value"]) for r in rows}
    assert by_year == GOLDEN


def test_radform_kanonisk() -> None:
    r = next(r for r in polisen.build_skjutningar_observations() if r["period"] == "2022")
    assert r["indicator"] == "skjutningar_sprangningar"
    assert r["category"] == "trygghet"
    assert r["submeasure"] == "grov_brottslighet"
    assert r["geography"] == "Riket"
    assert r["id"] == "obs:polisen:skjutningar_sprangningar:2022"
    assert r["source_ref"] == "polisen:skjutningar:2022"
    assert "skjutningar_sprangningar" in polisen.INDICATORS


def test_builder_ren_funktion_injicerbar_cfg() -> None:
    """Ren funktion: en injicerad cfg ger exakt motsvarande rader (ingen fil-IO krävs)."""
    cfg = {
        "indicator": "skjutningar_sprangningar", "category": "trygghet",
        "submeasure": "grov_brottslighet", "unit": "antal",
        "years": {2019: {"value": 360, "source": "x"}, 2020: {"value": 379, "source": "y"}},
    }
    rows = polisen.build_skjutningar_observations(cfg)
    assert [(r["period"], r["value"]) for r in rows] == [("2019", 360.0), ("2020", 379.0)]


def test_indikator_kanonisk_trygghet_riktning_down() -> None:
    """INDICATORS pekar på en categories.yaml-indikator i trygghet med riktning down."""
    trygghet = next(c for c in config.categories()["categories"] if c["id"] == "trygghet")
    ind = next(i for i in trygghet["indicators"] if i["id"] == "skjutningar_sprangningar")
    assert ind["direction"] == "down"
    assert ind["submeasure"] == "grov_brottslighet"


def test_config_pinnad_och_korsverifierbar_form() -> None:
    """config/skjutningar.yaml har alla år med value + source (källspår per årssiffra)."""
    cfg = config.skjutningar()
    assert cfg["indicator"] == "skjutningar_sprangningar"
    for year, entry in cfg["years"].items():
        assert isinstance(entry["value"], int), f"{year}: värde ej heltal"
        assert entry["source"].startswith("https://polisen.se/"), f"{year}: saknar Polis-källa"
