"""Offline-test för Energimyndigheten-adaptern (PxWeb v1 json-stat2).

Två serier: fossil-summan (EN0202_8) och elprisvolatiliteten (EN_IND12-5A, spotpris
månadsmedel -> årlig CV). Facit mot verkliga (beskurna) fixturer; CV-måttvalet (ddof=0,
likaviktning SE1-SE4, 12/12-regeln) PINNAS här. Ingen nätverkstrafik.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from pipeline.sources import energimyndigheten as em

FIXTURE = Path(__file__).parent / "fixtures" / "energimyndigheten_en0202_8_fossil.json"
SPOT_FIXTURE = Path(__file__).parent / "fixtures" / "energimyndigheten_en_ind12_5a_spotpris.json"


def _fixture() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def _spot_fixture() -> dict:
    return json.loads(SPOT_FIXTURE.read_text(encoding="utf-8"))


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
    """INDICATORS pekar på kanoniska klimatindikatorer (annars faller gaten)."""
    from pipeline import config

    klimat = next(c for c in config.categories()["categories"] if c["id"] == "klimat")
    inds = {i["id"]: i for i in klimat["indicators"]}
    assert set(em.INDICATORS) <= set(inds)
    assert "fossil_energianvandning" in inds
    assert inds["elprisvolatilitet"]["direction"] == "down"
    assert inds["elprisvolatilitet"]["submeasure"] == "energi_elpriser"


# --- EN_IND12-5A: elspotpris månadsmedel -> årlig CV (elprisvolatilitet) ---


def test_monthly_by_area_ger_ankarpriser_med_artal_manad_labels() -> None:
    """Parsern ger {elområde -> {YYYYMmm -> pris}}; perioder är labels, inte PxWeb-index.

    Ankarvärden SE3 (kr/MWh) mot publicerade värden: 2021M01=491, 2022M08=2230, 2022M12=2690."""
    monthly = em.monthly_by_area(_spot_fixture())
    assert set(monthly) == {"SE1", "SE2", "SE3", "SE4"}
    assert all(len(m) == 26 for m in monthly.values())  # 2011M11-M12 + hela 2021 + hela 2022
    assert monthly["SE3"]["2021M01"] == pytest.approx(491.0)
    assert monthly["SE3"]["2022M08"] == pytest.approx(2230.0)
    assert monthly["SE3"]["2022M12"] == pytest.approx(2690.0)


def test_annual_cv_pinnar_berakningen_mot_fixturen() -> None:
    """CV (ddof=0, likaviktat SE1-SE4) pinnas mot fixturåren; 2011 (2/12 månader) utesluts
    av 12/12-regeln. Värdena är våra beräknade ur live-datat 2026-06-12 (sonderingens
    referens med ddof=1 vore x sqrt(12/11): 43.6 resp. 65.3 — dokumenterad avvikelse)."""
    series = em.annual_cv(em.monthly_by_area(_spot_fixture()))
    assert series == {
        "2021": pytest.approx(41.774, abs=0.001),
        "2022": pytest.approx(62.560, abs=0.001),
    }


def test_annual_cv_handraknat_varde_later_ddof0_vara_last() -> None:
    """Handräknat facit som LÅSER populations-stdev (ddof=0): 12 månader alternerande
    100/300 -> medel 200, pstdev 100 -> CV exakt 50.0 %. Med sample-stdev (ddof=1)
    vore CV 52.2 % — testet faller om ddof-valet ändras tyst."""
    months = {f"2020M{m:02d}": (100.0 if m % 2 else 300.0) for m in range(1, 13)}
    series = em.annual_cv({"SE1": months})
    assert series == {"2020": pytest.approx(50.0)}


def test_annual_cv_kraver_alla_elomraden_kompletta() -> None:
    """Saknar ETT elområde en månad faller hela året bort (i stället för tyst snedviktning)."""
    full = {f"2020M{m:02d}": 100.0 + m for m in range(1, 13)}
    partial = dict(full)
    del partial["2020M07"]
    assert em.annual_cv({"SE1": full, "SE2": partial}) == {}


def test_spot_icke_eliminerad_extra_dimension_ger_hard_fail() -> None:
    """Om ContentsCode inte är eliminerad (storlek 1) ska parsern faila högt."""
    j = _spot_fixture()
    j["size"][0] = 2
    with pytest.raises(ValueError, match="icke-eliminerad"):
        em.monthly_by_area(j)


def test_spot_ovantat_periodformat_ger_hard_fail() -> None:
    """Månadsetiketter som inte matchar YYYYMmm (formatdrift) ska faila högt, inte tyst
    ge tomma årsgrupper."""
    j = _spot_fixture()
    tcat = j["dimension"]["År/Månad"]["category"]
    first_code = next(iter(tcat["label"]))
    tcat["label"][first_code] = "2022-08"
    with pytest.raises(ValueError, match="periodformat"):
        em.monthly_by_area(j)


def test_build_volatility_observations_radform_och_id_monster() -> None:
    """Observations-raderna bär kanonisk kategori/submått/indikator + id-/source_ref-mönster."""
    rows = em.build_volatility_observations(em.annual_cv(em.monthly_by_area(_spot_fixture())))
    assert [r["period"] for r in rows] == ["2021", "2022"]
    r = rows[1]
    assert r["id"] == "obs:energimyndigheten:elprisvolatilitet:2022"
    assert r["category"] == "klimat"
    assert r["submeasure"] == "energi_elpriser"
    assert r["indicator"] == "elprisvolatilitet"
    assert r["value"] == pytest.approx(62.56, abs=0.001)
    assert r["unit"] == "CV % (månadsmedel, likaviktat SE1-SE4)"
    assert r["geography"] == "Riket"
    assert r["source_ref"] == "energimyndigheten:EN_IND12-5A:2022"
