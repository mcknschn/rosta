"""Offline golden-test för Svk-serien (effektbrist, transkriberad config).

Indikatorn effektbrist (klimat, riktning down) bärs av nettoimporten vid vinterns
topplasttimme (MWh/h; positivt = nettoimport, negativt = nettoexport), etiketterad på
vinterns SLUTÅR, ur Svk:s lagstadgade "Kraftbalansen på den svenska elmarknaden"
(config/effektbrist.yaml). Pinnar årsvärdena (inkl. teckenhantering för nettoexport-åren)
+ kontrollerar radform, kanonisk indikator och att sekundärserien (prognos_normalvinter)
inte läcker in i D. Ingen nätverkstrafik.
"""

from __future__ import annotations

from pipeline import config
from pipeline.sources import svk

# Facit: nettoimport vid vinterns topplasttimme (MWh/h), vintrarna 2019/20-2025/26,
# maskinverifierat ur Svk-original-PDF:erna (PyMuPDF) 2026-06-12.
GOLDEN = {
    "2020": -1700.0,  # vinter 2019/20: nettoexport (rapport 2020)
    "2021": 500.0,    # vinter 2020/21 (rapport 2021, Tabell 6)
    "2022": 1600.0,   # vinter 2021/22 (rapport 2022, Tabell 7)
    "2023": 3290.0,   # vinter 2022/23: seriens högsta importberoende (rapport 2023)
    "2024": 2430.0,   # vinter 2023/24 (rapport 2024)
    "2025": -2690.0,  # vinter 2024/25: mild-outliern, ovanlig nettoexport (rapport 2025)
    "2026": 200.0,    # vinter 2025/26 (rapport vår 2026)
}


def test_serie_matchar_pinnade_varden() -> None:
    rows = svk.build_effektbrist_observations()
    by_year = {r["period"]: float(r["value"]) for r in rows}
    assert by_year == GOLDEN


def test_negativa_varden_bevaras_med_tecken() -> None:
    """Nettoexport-åren (2020, 2025) ska vara strikt negativa — tecknet ÄR signalen
    (riktning down: lägre nettoimport/mer export = bättre, ingen teckenmappning)."""
    rows = svk.build_effektbrist_observations()
    by_year = {r["period"]: r["value"] for r in rows}
    assert by_year["2020"] < 0
    assert by_year["2025"] < 0
    assert by_year["2023"] > 0


def test_sju_konsekutiva_vinterar() -> None:
    """7 konsekutiva slutår 2020-2026 (vintrarna 2019/20-2025/26), inga luckor."""
    rows = svk.build_effektbrist_observations()
    assert [r["period"] for r in sorted(rows, key=lambda r: r["period"])] == [
        str(y) for y in range(2020, 2027)
    ]


def test_radform_kanonisk() -> None:
    r = next(r for r in svk.build_effektbrist_observations() if r["period"] == "2023")
    assert r["indicator"] == "effektbrist"
    assert r["category"] == "klimat"
    assert r["submeasure"] == "energi_elpriser"
    assert r["geography"] == "Riket"
    assert r["unit"] == "MWh/h (nettoimport topplasttimme)"
    assert r["id"] == "obs:svk:effektbrist:2023"
    assert r["source_ref"] == "svk:effektbrist:2023"
    assert "effektbrist" in svk.INDICATORS


def test_builder_ren_funktion_injicerad_cfg() -> None:
    """Ren funktion: värdet = entry['value'] för en injicerad cfg (ingen fil-IO);
    negativa värden flyter igenom oförändrade."""
    cfg = {
        "indicator": "effektbrist", "category": "klimat",
        "submeasure": "energi_elpriser", "unit": "MWh/h",
        "years": {
            2020: {"value": -1700, "source": "a"},
            2021: {"value": 500, "source": "b"},
        },
    }
    rows = svk.build_effektbrist_observations(cfg)
    assert [(r["period"], r["value"]) for r in rows] == [("2020", -1700.0), ("2021", 500.0)]


def test_prognosserien_lacker_inte_in_i_d() -> None:
    """Sekundärserien prognos_normalvinter (prognos, ej utfall) får ALDRIG bli observations-
    rader — readern läser bara 'years'. T.ex. 2021: utfall +500, prognos −1700."""
    cfg = config.effektbrist()
    assert "prognos_normalvinter" in cfg, "robusthetsreferensen ska finnas dokumenterad i configen"
    rows = svk.build_effektbrist_observations()
    assert {r["period"]: r["value"] for r in rows}["2021"] == 500.0
    assert len(rows) == len(cfg["years"])


def test_indikator_kanonisk_klimat_riktning_down() -> None:
    klimat = next(c for c in config.categories()["categories"] if c["id"] == "klimat")
    ind = next(i for i in klimat["indicators"] if i["id"] == "effektbrist")
    assert ind["direction"] == "down"
    assert ind["submeasure"] == "energi_elpriser"


def test_config_har_kalla_per_ar() -> None:
    """Varje år har ett värde, en Svk-källa och en källrad; wayback-hämtväg för 404-årgångarna."""
    cfg = config.effektbrist()
    assert cfg["indicator"] == "effektbrist"
    assert cfg["version"] == 0
    for year, e in cfg["years"].items():
        assert isinstance(e["value"], (int, float)), f"{year}: värde ej tal"
        assert str(e["source"]).startswith("https://www.svk.se/"), f"{year}: saknar Svk-källa"
        assert e.get("source_note", "").strip(), f"{year}: saknar källrad"
    for year in (2020, 2021, 2022, 2023):  # flyttade/404 på svk.se -> wayback-hämtväg krävs
        assert str(cfg["years"][year]["wayback"]).startswith("https://web.archive.org/"), year
