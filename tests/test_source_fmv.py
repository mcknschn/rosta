"""Offline golden-test för FMV-serien (materielleveransutfall, transkriberad config).

Indikatorn materielleveransutfall (forsvar, riktning up) bärs av FMV:s leveransindex
ap. 1:3.1 (andel av årets planerade materielleveranser till Försvarsmakten som levererats
enligt leveransplan, värdeviktat; kan överstiga 100), ur FMV:s årsredovisningar
(config/materielleveransutfall.yaml). Pinnar årsvärdena + kontrollerar radform, kanonisk
indikator och jämförbarhetsstarten 2021 (FMV: 2020 och tidigare år EXPLICIT ojämförbara —
inga äldre värden får smyga in). Ingen nätverkstrafik.
"""

from __future__ import annotations

from pipeline import config
from pipeline.sources import fmv

# Facit: FMV:s leveransindex ap. 1:3.1 per kalenderår, maskinverifierat ur FMV:s
# original-ÅR-PDF:er (PyMuPDF) 2026-06-12.
GOLDEN = {
    "2021": 79.0,  # AR 2021 Tabell 5: "Det totala indexvardet for 2021 ar 79"
    "2022": 97.0,  # AR 2022 Tabell 8: seriens högsta (tidigarelagda + högvärdiga leveranser)
    "2023": 72.0,  # AR 2023 Tabell 9 (viktningsbas-ordalydelse skiftar, FMV intygar jämförbarhet)
    "2024": 73.0,  # AR 2024 Tabell 4
    "2025": 53.0,  # AR 2025 s.13+27: seriens lägsta (överplanering + JAS 39E-/arméförseningar)
}


def test_serie_matchar_pinnade_varden() -> None:
    rows = fmv.build_materielleveransutfall_observations()
    by_year = {r["period"]: float(r["value"]) for r in rows}
    assert by_year == GOLDEN


def test_fem_konsekutiva_ar_fran_2021() -> None:
    """5 konsekutiva år 2021-2025, inga luckor — och INGET år före 2021 (FMV: ÅR 2020 och
    tidigare bygger på andra principer/indata och är explicit ojämförbara)."""
    rows = fmv.build_materielleveransutfall_observations()
    assert [r["period"] for r in sorted(rows, key=lambda r: r["period"])] == [
        str(y) for y in range(2021, 2026)
    ]


def test_radform_kanonisk() -> None:
    r = next(r for r in fmv.build_materielleveransutfall_observations() if r["period"] == "2022")
    assert r["indicator"] == "materielleveransutfall"
    assert r["category"] == "forsvar"
    assert r["submeasure"] == "genomforbarhet_leverans"
    assert r["geography"] == "Riket"
    assert r["unit"] == "index (andel av leveransplan, %)"
    assert r["id"] == "obs:fmv:materielleveransutfall:2022"
    assert r["source_ref"] == "fmv:materielleveransutfall:2022"
    assert "materielleveransutfall" in fmv.INDICATORS


def test_builder_ren_funktion_injicerad_cfg() -> None:
    """Ren funktion: värdet = entry['value'] för en injicerad cfg (ingen fil-IO)."""
    cfg = {
        "indicator": "materielleveransutfall", "category": "forsvar",
        "submeasure": "genomforbarhet_leverans", "unit": "index",
        "years": {
            2021: {"value": 79, "source": "a"},
            2022: {"value": 97, "source": "b"},
        },
    }
    rows = fmv.build_materielleveransutfall_observations(cfg)
    assert [(r["period"], r["value"]) for r in rows] == [("2021", 79.0), ("2022", 97.0)]


def test_indikator_kanonisk_forsvar_riktning_up() -> None:
    forsvar = next(c for c in config.categories()["categories"] if c["id"] == "forsvar")
    ind = next(i for i in forsvar["indicators"] if i["id"] == "materielleveransutfall")
    assert ind["direction"] == "up"
    assert ind["submeasure"] == "genomforbarhet_leverans"
    # Syskonet leveranstid_materiel BEHÅLLS orört (annat mått, annan riktning — ej återanvänt).
    sibling = next(i for i in forsvar["indicators"] if i["id"] == "leveranstid_materiel")
    assert sibling["direction"] == "down"
    assert sibling["submeasure"] == "genomforbarhet_leverans"


def test_config_har_kalla_per_ar() -> None:
    """Varje år har ett värde, en FMV-källa (fmv.se) och en källrad; serien börjar 2021."""
    cfg = config.materielleveransutfall()
    assert cfg["indicator"] == "materielleveransutfall"
    assert cfg["version"] == 0
    assert min(cfg["years"]) == 2021, "jämförbarhetskedjan börjar 2021 — inga äldre värden"
    for year, e in cfg["years"].items():
        assert isinstance(e["value"], (int, float)), f"{year}: värde ej tal"
        assert str(e["source"]).startswith("https://www.fmv.se/"), f"{year}: saknar FMV-källa"
        assert e.get("source_note", "").strip(), f"{year}: saknar källrad"
