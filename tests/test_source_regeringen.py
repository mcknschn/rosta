"""Offline golden-test för Regeringen-serien (ukraina_stod, transkriberad config).

Indikatorn ukraina_stod = värdet av Sveriges militära stöd till Ukraina per kalenderår
(config/ukraina_stod.yaml, ur Regeringens samlade redovisning). Öppnar submåttet nato_ukraina
(försvar). Pinnar årsvärdena + kontrollerar radform, kanonisk indikator och att serien är
strikt monoton uppåt (sign-only D robust). Ingen nätverkstrafik.
"""

from __future__ import annotations

from pipeline import config
from pipeline.sources import regeringen

# Facit: militärt stöd (mdr kr), nationell siffra per år, transkriberat 2026-06-08.
GOLDEN = {"2022": 6.1, "2023": 17.0, "2024": 25.0, "2025": 40.0}


def test_serie_matchar_pinnade_varden() -> None:
    rows = regeringen.build_ukraina_stod_observations()
    by_year = {r["period"]: float(r["value"]) for r in rows}
    assert by_year == GOLDEN


def test_serie_strikt_monoton_upp() -> None:
    """Serien är strikt monoton uppåt 2022->2025 -> alla D-tecken +, robust mot sifferosäkerhet."""
    rows = sorted(regeringen.build_ukraina_stod_observations(), key=lambda r: r["period"])
    vals = [r["value"] for r in rows]
    assert all(b > a for a, b in zip(vals, vals[1:], strict=False))


def test_exkluderar_framatram_2026_2027() -> None:
    """2026-2027 (beslutad framåtram, ej utfall) ingår inte i D-serien."""
    rows = regeringen.build_ukraina_stod_observations()
    assert max(r["period"] for r in rows) == "2025"


def test_radform_kanonisk() -> None:
    r = next(r for r in regeringen.build_ukraina_stod_observations() if r["period"] == "2024")
    assert r["indicator"] == "ukraina_stod"
    assert r["category"] == "forsvar"
    assert r["submeasure"] == "nato_ukraina"
    assert r["geography"] == "Riket"
    assert r["id"] == "obs:regeringen:ukraina_stod:2024"
    assert r["source_ref"] == "regeringen:ukraina_stod:2024"
    assert "ukraina_stod" in regeringen.INDICATORS


def test_builder_ren_funktion_injicerad_cfg() -> None:
    """Ren funktion: värdet = entry['value'] för en injicerad cfg (ingen fil-IO)."""
    cfg = {
        "indicator": "ukraina_stod", "category": "forsvar",
        "submeasure": "nato_ukraina", "unit": "mdr",
        "years": {
            2022: {"value": 6.1, "source": "a"},
            2023: {"value": 17.0, "source": "b"},
        },
    }
    rows = regeringen.build_ukraina_stod_observations(cfg)
    assert [(r["period"], r["value"]) for r in rows] == [("2022", 6.1), ("2023", 17.0)]


def test_indikator_kanonisk_forsvar_riktning_up() -> None:
    forsvar = next(c for c in config.categories()["categories"] if c["id"] == "forsvar")
    ind = next(i for i in forsvar["indicators"] if i["id"] == "ukraina_stod")
    assert ind["direction"] == "up"
    assert ind["submeasure"] == "nato_ukraina"


def test_config_har_kalla_per_ar() -> None:
    """Varje år har ett värde och en regeringen.se-källa (ingen tyst siffra)."""
    cfg = config.ukraina_stod()
    assert cfg["indicator"] == "ukraina_stod"
    for year, e in cfg["years"].items():
        assert isinstance(e["value"], (int, float)), f"{year}: värde ej tal"
        assert str(e["source"]).startswith("https://"), f"{year}: saknar källa"
