"""Offline golden-test för Polisen-serien (skjutningar + sprängningar, transkriberad config).

Indikatorn skjutningar_sprangningar = summan av bekräftade skjutningar + sprängningar per år
(config/skjutningar_sprangningar.yaml). Pinnar de korsverifierade kombinerade årstotalerna
(varje komponent: regionsumma == PDF:ens Totalt-rad vid transkribering, se
pipeline/tools/skjutningar_transcribe.py) och kontrollerar radform + kanonisk indikator. Ingen nätverkstrafik.
"""

from __future__ import annotations

from pipeline import config
from pipeline.sources import polisen

# Facit: skjutningar + sprängningar (Polisen), nationell summa per år, transkriberade 2026-06-03.
GOLDEN = {
    "2018": 415, "2019": 493, "2020": 486, "2021": 423,
    "2022": 481, "2023": 527, "2024": 435, "2025": 352,
}


def test_kombinerad_serie_matchar_pinnade_varden() -> None:
    rows = polisen.build_skjutningar_sprangningar_observations()
    by_year = {r["period"]: int(r["value"]) for r in rows}
    assert by_year == GOLDEN


def test_borjar_2018_ej_2017() -> None:
    """Serien börjar 2018 (då sprängningskomponenten finns); 2017 (skjutningar-only) utelämnas."""
    rows = polisen.build_skjutningar_sprangningar_observations()
    assert min(r["period"] for r in rows) == "2018"


def test_radform_kanonisk() -> None:
    r = next(r for r in polisen.build_skjutningar_sprangningar_observations() if r["period"] == "2023")
    assert r["indicator"] == "skjutningar_sprangningar"
    assert r["category"] == "trygghet"
    assert r["submeasure"] == "grov_brottslighet"
    assert r["geography"] == "Riket"
    assert r["id"] == "obs:polisen:skjutningar_sprangningar:2023"
    assert r["source_ref"] == "polisen:skjutningar_sprangningar:2023"
    assert "skjutningar_sprangningar" in polisen.INDICATORS


def test_builder_summerar_komponenterna_ren_funktion() -> None:
    """Ren funktion: värdet = skjutningar + sprängningar för en injicerad cfg (ingen fil-IO)."""
    cfg = {
        "indicator": "skjutningar_sprangningar", "category": "trygghet",
        "submeasure": "grov_brottslighet", "unit": "antal",
        "years": {
            2019: {"skjutningar": 360, "sprangningar": 133, "skjutningar_source": "a",
                   "sprangningar_source": "b"},
            2020: {"skjutningar": 379, "sprangningar": 107, "skjutningar_source": "c",
                   "sprangningar_source": "d"},
        },
    }
    rows = polisen.build_skjutningar_sprangningar_observations(cfg)
    assert [(r["period"], r["value"]) for r in rows] == [("2019", 493.0), ("2020", 486.0)]


def test_indikator_kanonisk_trygghet_riktning_down() -> None:
    trygghet = next(c for c in config.categories()["categories"] if c["id"] == "trygghet")
    ind = next(i for i in trygghet["indicators"] if i["id"] == "skjutningar_sprangningar")
    assert ind["direction"] == "down"
    assert ind["submeasure"] == "grov_brottslighet"


def test_config_har_bada_komponenter_med_kalla_per_ar() -> None:
    """Varje år har skjutningar + sprängningar (heltal) och en Polis-källa per komponent."""
    cfg = config.skjutningar_sprangningar()
    assert cfg["indicator"] == "skjutningar_sprangningar"
    for year, e in cfg["years"].items():
        assert isinstance(e["skjutningar"], int) and isinstance(e["sprangningar"], int), f"{year}"
        assert e["skjutningar_source"].startswith("https://polisen.se/"), f"{year}: skjut-källa"
        assert e["sprangningar_source"].startswith("https://polisen.se/"), f"{year}: spräng-källa"
