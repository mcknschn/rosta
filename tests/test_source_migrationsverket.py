"""Offline golden-test för Migrationsverket-serien (asyl_handlaggningstid, transkriberad config).

Indikatorn asyl_handlaggningstid = genomsnittlig handläggningstid (dagar) för avgjorda
förstagångsärenden om asyl per kalenderår (config/asyl_handlaggningstid.yaml, ur Migrationsverkets
"Avgjorda asylärenden", deltabellen Asyl exkl. massflykt). Öppnar submåttet migrationssystem
(integration). Pinnar årsvärdena + kontrollerar radform, kanonisk indikator (riktning down) och
att serien bär den genuina teckenväxlingen 2022->2023 (inte monoton -> diskriminerande). Inget nät.
"""

from __future__ import annotations

from pipeline import config
from pipeline.sources import migrationsverket

# Facit: handläggningstid (dagar), avgjorda förstagångsärenden om asyl (deltabell Asyl), per år,
# verifierad direkt ur Migrationsverkets officiella per-års-xlsx 2026-06-12.
GOLDEN = {"2021": 257.0, "2022": 166.0, "2023": 198.0, "2024": 187.0, "2025": 180.0}


def test_serie_matchar_pinnade_varden() -> None:
    rows = migrationsverket.build_asyl_handlaggningstid_observations()
    by_year = {r["period"]: float(r["value"]) for r in rows}
    assert by_year == GOLDEN


def test_serie_har_genuin_teckenvaxling() -> None:
    """Serien är INTE monoton: förbättring 2021->2022, försämring 2022->2023 -> diskriminerande D."""
    rows = sorted(migrationsverket.build_asyl_handlaggningstid_observations(), key=lambda r: r["period"])
    vals = [r["value"] for r in rows]
    # riktning down: en nedgång = förbättring, en uppgång = försämring. Serien innehåller båda.
    diffs = [b - a for a, b in zip(vals, vals[1:], strict=False)]
    assert any(d < 0 for d in diffs) and any(d > 0 for d in diffs)
    assert vals[0] > vals[1] < vals[2]  # 257 > 166 < 198 (teckenväxling 2022->2023)


def test_radform_kanonisk() -> None:
    r = next(r for r in migrationsverket.build_asyl_handlaggningstid_observations() if r["period"] == "2023")
    assert r["indicator"] == "asyl_handlaggningstid"
    assert r["category"] == "integration"
    assert r["submeasure"] == "migrationssystem"
    assert r["geography"] == "Riket"
    assert r["id"] == "obs:migrationsverket:asyl_handlaggningstid:2023"
    assert r["source_ref"] == "migrationsverket:asyl_handlaggningstid:2023"
    assert "asyl_handlaggningstid" in migrationsverket.INDICATORS


def test_builder_ren_funktion_injicerad_cfg() -> None:
    """Ren funktion: värdet = entry['value'] för en injicerad cfg (ingen fil-IO)."""
    cfg = {
        "indicator": "asyl_handlaggningstid", "category": "integration",
        "submeasure": "migrationssystem", "unit": "dagar",
        "years": {
            2021: {"value": 257, "source": "a"},
            2022: {"value": 166, "source": "b"},
        },
    }
    rows = migrationsverket.build_asyl_handlaggningstid_observations(cfg)
    assert [(r["period"], r["value"]) for r in rows] == [("2021", 257.0), ("2022", 166.0)]


def test_indikator_kanonisk_integration_riktning_down() -> None:
    integration = next(c for c in config.categories()["categories"] if c["id"] == "integration")
    ind = next(i for i in integration["indicators"] if i["id"] == "asyl_handlaggningstid")
    assert ind["direction"] == "down"
    assert ind["submeasure"] == "migrationssystem"


def test_config_har_kalla_per_ar() -> None:
    """Varje år har ett värde och en migrationsverket.se-källa (ingen tyst siffra)."""
    cfg = config.asyl_handlaggningstid()
    assert cfg["indicator"] == "asyl_handlaggningstid"
    for year, e in cfg["years"].items():
        assert isinstance(e["value"], (int, float)), f"{year}: värde ej tal"
        assert str(e["source"]).startswith("https://"), f"{year}: saknar källa"
