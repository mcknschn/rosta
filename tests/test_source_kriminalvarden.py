"""Offline golden-test för Kriminalvården-serien (aterfall_i_brott, transkriberade råtal).

Indikatorn aterfall_i_brott = andel klienter med starthändelse som återföll i brott inom 3 år
(config/aterfall_i_brott.yaml, ur KOS 2025 Tabell 6.1). Öppnar submåttet aterfall_kriminalvard
(trygghet). Pinnar beräknade andelar (ur råtal), radform, kanonisk indikator, korsverifiering mot
publicerad andel och att loadern hård-failar vid orimliga råtal. Ingen nätverkstrafik.
"""

from __future__ import annotations

import pytest

from pipeline import config
from pipeline.sources import kriminalvarden

# Facit: andel (%) = aterfall / klienter * 100 (2 dec) ur Tabell 6.1, ankarår.
GOLDEN = {"1999": 41.70, "2012": 29.27, "2022": 31.11}


def test_andelar_matchar_pinnade_ankarvarden() -> None:
    rows = kriminalvarden.build_aterfall_observations()
    by_year = {r["period"]: float(r["value"]) for r in rows}
    for year, val in GOLDEN.items():
        assert by_year[year] == val


def test_serie_29_ar_1994_2022() -> None:
    rows = kriminalvarden.build_aterfall_observations()
    years = sorted(r["period"] for r in rows)
    assert len(years) == 29
    assert years[0] == "1994" and years[-1] == "2022"


def test_alla_andelar_korsverifierade_mot_publicerad() -> None:
    """Varje beräknad andel ligger inom 0,6 pp av Kriminalvårdens publicerade heltalsandel."""
    cfg = config.aterfall_i_brott()
    rows = kriminalvarden.build_aterfall_observations()
    by_year = {r["period"]: float(r["value"]) for r in rows}
    for year, e in cfg["years"].items():
        assert abs(by_year[str(year)] - float(e["andel_publicerad"])) <= 0.6


def test_radform_kanonisk() -> None:
    r = next(r for r in kriminalvarden.build_aterfall_observations() if r["period"] == "2022")
    assert r["indicator"] == "aterfall_i_brott"
    assert r["category"] == "trygghet"
    assert r["submeasure"] == "aterfall_kriminalvard"
    assert r["geography"] == "Riket"
    assert r["id"] == "obs:kriminalvarden:aterfall_i_brott:2022"
    assert r["source_ref"] == "kriminalvarden:aterfall_i_brott:2022"
    assert "aterfall_i_brott" in kriminalvarden.INDICATORS


def test_builder_ren_funktion_injicerad_cfg() -> None:
    """Ren funktion: andel = aterfall/klienter*100 för en injicerad cfg (ingen fil-IO)."""
    cfg = {
        "indicator": "aterfall_i_brott", "category": "trygghet",
        "submeasure": "aterfall_kriminalvard", "unit": "%",
        "years": {2021: {"klienter": 18607, "aterfall": 5697, "andel_publicerad": 31}},
    }
    rows = kriminalvarden.build_aterfall_observations(cfg)
    assert [(r["period"], r["value"]) for r in rows] == [("2021", 30.62)]


def test_orimliga_ratal_hard_failar() -> None:
    cfg = {
        "indicator": "aterfall_i_brott", "category": "trygghet",
        "submeasure": "aterfall_kriminalvard", "unit": "%",
        "years": {2020: {"klienter": 100, "aterfall": 200}},  # aterfall > klienter
    }
    with pytest.raises(ValueError):
        kriminalvarden.build_aterfall_observations(cfg)


def test_korsverifiering_fangar_transkriptionsfel() -> None:
    """En beräknad andel som avviker >0,6 pp från publicerad andel ska hård-faila."""
    cfg = {
        "indicator": "aterfall_i_brott", "category": "trygghet",
        "submeasure": "aterfall_kriminalvard", "unit": "%",
        "years": {2020: {"klienter": 17547, "aterfall": 5555, "andel_publicerad": 25}},  # fel publicerad
    }
    with pytest.raises(ValueError):
        kriminalvarden.build_aterfall_observations(cfg)


def test_indikator_kanonisk_trygghet_riktning_down() -> None:
    trygghet = next(c for c in config.categories()["categories"] if c["id"] == "trygghet")
    ind = next(i for i in trygghet["indicators"] if i["id"] == "aterfall_i_brott")
    assert ind["direction"] == "down"
    assert ind["submeasure"] == "aterfall_kriminalvard"
