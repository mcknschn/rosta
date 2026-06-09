"""Offline golden-test för V-Dem-serierna (demokrati, transkriberade V-Dem v16-index).

Fyra V-Dem-index (Göteborgs universitet) ger var sitt tidigare D-tomt demokrati-submått sin första
D-serie (config/vdem_demokrati.yaml). Pinnar ankarvärden, radform, kanoniska indikatorer (alla nya,
riktning up, alla 0-1) och submåttsmappningen. Ingen nätverkstrafik.
"""

from __future__ import annotations

from pipeline import config
from pipeline.sources import vdem

# Facit: V-Dem v16-värden för Sverige, ankarår (korsverifierade mot OWID för de tre OWID har).
GOLDEN = {
    "rattsstatsindex": {"2014": 0.995, "2024": 0.99},
    "yttrandefrihetsindex": {"2014": 0.974, "2023": 0.95, "2024": 0.946},
    "privata_friheter": {"2014": 0.968, "2015": 0.951, "2024": 0.948},
    "horisontellt_ansvarsutkravande": {"2014": 0.98, "2019": 0.99, "2024": 0.989},
}

# Förväntad submåttsmappning (ett index per tidigare D-tomt submått).
SUBMEASURE = {
    "rattsstatsindex": "rattsstat_maktdelning",
    "yttrandefrihetsindex": "yttrandefrihet_medier",
    "privata_friheter": "personlig_frihet",
    "horisontellt_ansvarsutkravande": "transparens_ansvar",
}


def _by_ind_year() -> dict[tuple[str, str], float]:
    return {(r["indicator"], r["period"]): float(r["value"]) for r in vdem.build_vdem_observations()}


def test_ankarvarden_matchar() -> None:
    vals = _by_ind_year()
    for ind, anchors in GOLDEN.items():
        for year, val in anchors.items():
            assert vals[(ind, year)] == val, f"{ind} {year}"


def test_alla_fyra_indikatorer_26_ar_2000_2025() -> None:
    rows = vdem.build_vdem_observations()
    for ind in vdem.INDICATORS:
        years = sorted(r["period"] for r in rows if r["indicator"] == ind)
        assert len(years) == 26, ind
        assert years[0] == "2000" and years[-1] == "2025", ind


def test_submattsmappning_och_riktning_up() -> None:
    demokrati = next(c for c in config.categories()["categories"] if c["id"] == "demokrati")
    by_id = {i["id"]: i for i in demokrati["indicators"]}
    for ind, sub in SUBMEASURE.items():
        assert by_id[ind]["submeasure"] == sub
        assert by_id[ind]["direction"] == "up"


def test_radform_kanonisk() -> None:
    r = next(
        r for r in vdem.build_vdem_observations()
        if r["indicator"] == "yttrandefrihetsindex" and r["period"] == "2024"
    )
    assert r["category"] == "demokrati"
    assert r["submeasure"] == "yttrandefrihet_medier"
    assert r["geography"] == "Riket"
    assert r["id"] == "obs:vdem:yttrandefrihetsindex:2024"
    assert r["source_ref"] == "vdem:yttrandefrihetsindex:2024"


def test_alla_varden_inom_0_1() -> None:
    for r in vdem.build_vdem_observations():
        assert 0.0 <= r["value"] <= 1.0


def test_indicators_matchar_config_keys() -> None:
    cfg = config.vdem_demokrati()
    assert set(vdem.INDICATORS) == set(cfg["indicators"].keys())


def test_builder_ren_funktion_injicerad_cfg() -> None:
    cfg = {
        "category": "demokrati",
        "indicators": {
            "rattsstatsindex": {
                "submeasure": "rattsstat_maktdelning", "unit": "idx",
                "years": {2014: 0.995, 2015: 0.992},
            }
        },
    }
    rows = vdem.build_vdem_observations(cfg)
    assert [(r["indicator"], r["period"], r["value"]) for r in rows] == [
        ("rattsstatsindex", "2014", 0.995), ("rattsstatsindex", "2015", 0.992),
    ]
