"""Issue #3: sajten får inte påstå att underlaget når ett datum som inte inträffat.

WINDOW_END är mandatperiodens FORMELLA slut (nästa valdag). Det ligger i framtiden under hela
mandatperioden och säger inget om hur färska serierna är. meta.data_as_of är något annat: sista
dagen i det senaste observationsår som hunnit ta slut. De två får aldrig blandas ihop.
"""

from __future__ import annotations

from datetime import date

import pytest

from pipeline import score, scorerun, warehouse


def _obs(period: str, value: float = 6.0) -> dict[str, object]:
    """En giltig observationsrad; bara perioden varierar."""
    return {
        "id": f"obs:test:arbetsloshet:{period}", "category": "ekonomi",
        "submeasure": "sysselsattning_arbetsloshet", "indicator": "arbetsloshet",
        "period": period, "value": value, "unit": "%", "geography": "Riket",
        "source_ref": f"scb:test:{period}",
    }


def _con(periods: list[str]) -> object:
    con = warehouse.connect(":memory:")
    if periods:
        warehouse.upsert(con, "observations", [_obs(p) for p in periods])
    return con


@pytest.mark.parametrize(
    ("period", "expected"),
    [
        ("2025", 2025),           # enkelt år
        ("2021-2021", 2021),      # SCB:s enkelår skrivet som spann
        ("2018-2019", 2019),      # äkta dubbelår -> SLUTåret, serien når dit
        ("2025M03", 2025),        # månad
        ("2025K2", 2025),         # kvartal
        ("  2024  ", 2024),       # blanktecken
        ("w", None),              # testfixturernas platshållare
        ("", None),
    ],
)
def test_period_end_year(period: str, expected: int | None) -> None:
    assert score.period_end_year(period) == expected


def test_period_end_year_skiljer_sig_fran_period_to_year_pa_dubblear() -> None:
    """De två läsningarna av samma sträng får INTE glida ihop: dubbelåret är kärnan i skillnaden.

    period_to_year ger None (inget enskilt attributionsår), period_end_year ger slutåret
    (serien räcker dit). Enkelår ska däremot ge samma svar.
    """
    assert score.period_to_year("2018-2019") is None
    assert score.period_end_year("2018-2019") == 2019
    assert score.period_to_year("2021-2021") == score.period_end_year("2021-2021") == 2021


def test_data_freshness_stannar_pa_senaste_avslutade_ar() -> None:
    """Ett år som fortfarande pågår flyttar inte fram data_as_of - det är hela poängen."""
    con = _con(["2024", "2025", "2026"])
    fresh = scorerun.data_freshness(con, today=date(2026, 8, 17))
    assert fresh.as_of == "2025-12-31"
    assert fresh.latest_year == 2026
    con.close()


def test_data_freshness_tar_slutaret_ur_ett_dubbelar() -> None:
    con = _con(["2016-2017", "2018-2019"])
    fresh = scorerun.data_freshness(con, today=date(2026, 8, 17))
    assert fresh.as_of == "2019-12-31"
    assert fresh.latest_year == 2019
    con.close()


def test_data_freshness_utan_avslutat_ar_ger_inget_datum() -> None:
    """Bara innevarande år i lagret -> hellre inget påstående än ett för färskt."""
    con = _con(["2026"])
    fresh = scorerun.data_freshness(con, today=date(2026, 8, 17))
    assert fresh.as_of is None
    assert fresh.latest_year == 2026
    con.close()


def test_data_freshness_pa_tomt_lager() -> None:
    con = _con([])
    assert scorerun.data_freshness(con, today=date(2026, 8, 17)) == (None, None)
    con.close()


def _built_meta() -> dict[str, object]:
    con = warehouse.connect(":memory:")
    warehouse.upsert(con, "observations", [_obs("2024"), _obs("2025")])
    meta = scorerun.build(con)["scores"]["meta"]
    con.close()
    return meta


def test_meta_skiljer_fonstrets_slut_fran_underlagets_slut() -> None:
    meta = _built_meta()
    assert meta["window_end"] == scorerun.WINDOW_END.isoformat()
    assert meta["data_as_of"] == "2025-12-31"
    assert meta["data_as_of"] != meta["window_end"]


def test_meta_data_as_of_ligger_aldrig_i_framtiden() -> None:
    """Invarianten buggen bröt: fönstrets slut får vara framtida, underlagets slut aldrig."""
    meta = _built_meta()
    assert date.fromisoformat(str(meta["data_as_of"])) <= date.today()
    assert date.fromisoformat(str(meta["generated"])) == date.today()


def test_meta_flaggar_pagaende_mandatperiod_som_preliminar() -> None:
    meta = _built_meta()
    assert meta["window_open"] is (date.today() < scorerun.WINDOW_END)
    assert meta["latest_observation_year"] == 2025
