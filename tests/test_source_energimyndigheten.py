"""Offline-test för Energimyndigheten-adaptern (PxWeb v1 json-stat2 -> fossil-summa).

Facit mot den verkliga (beskurna) EN0202_8-fixturen: slutlig fossil energianvändning
(kol+petroleum+gas) per år. Ingen nätverkstrafik — parsern testas direkt mot fixturen.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from pipeline.sources import energimyndigheten as em

FIXTURE = Path(__file__).parent / "fixtures" / "energimyndigheten_en0202_8_fossil.json"


def _fixture() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_annual_sum_over_summerar_fossila_energivaror_per_ar() -> None:
    """Summerar de tre fossila energivarorna per år; året läses ur category.label."""
    series = em.annual_sum_over(_fixture(), em.CARRIER_DIM)
    # 2014: 14.541+92.995+5.91 ; 2023: 12.895+71.022+3.838 ; 2024: 12.189+85.173+4.245
    assert series == {
        "2014": pytest.approx(113.446),
        "2023": pytest.approx(87.755),
        "2024": pytest.approx(101.607),
    }


def test_periods_ar_artal_inte_pxweb_koder() -> None:
    """Tidsnycklarna ska vara årtal (labels), inte interna PxWeb-index ('44','53','54')."""
    series = em.annual_sum_over(_fixture(), em.CARRIER_DIM)
    assert set(series) == {"2014", "2023", "2024"}


def test_icke_eliminerad_extra_dimension_ger_hard_fail() -> None:
    """Om en oväntad dimension inte är eliminerad (storlek 1) ska parsern faila högt."""
    j = _fixture()
    j["size"] = [2, 3, 3]  # ContentsCode låtsas ha storlek 2 (ej eliminerad)
    with pytest.raises(ValueError, match="icke-eliminerad"):
        em.annual_sum_over(j, em.CARRIER_DIM)


def test_fossila_energivaror_finns_i_modellens_klimatkategori() -> None:
    """INDICATORS pekar på en kanonisk klimatindikator (annars faller gaten)."""
    from pipeline import config

    klimat = next(c for c in config.categories()["categories"] if c["id"] == "klimat")
    inds = {i["id"] for i in klimat["indicators"]}
    assert set(em.INDICATORS) <= inds
    assert "fossil_energianvandning" in inds
