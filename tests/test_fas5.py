"""Fas 5: scorerun bygger en schema-giltig scores.json ur warehouse."""

from __future__ import annotations

from pipeline import config, scorerun, warehouse
from pipeline.sources import government


def _seed_con():
    con = warehouse.connect(":memory:")
    warehouse.upsert(con, "responsibility", government.build_national_responsibility())
    warehouse.upsert(con, "party_activity", [
        # S ägnar 100% av sina motioner åt ekonomi
        {"party": "S", "category": "ekonomi", "committee": "FiU",
         "kind": "motion", "period": "w", "count": 100, "source_ref": "u"},
        # M ägnar 25% åt ekonomi (50 av 200) och 75% åt klimat (150 av 200)
        {"party": "M", "category": "ekonomi", "committee": "FiU",
         "kind": "motion", "period": "w", "count": 50, "source_ref": "u"},
        {"party": "M", "category": "klimat", "committee": "MJU",
         "kind": "motion", "period": "w", "count": 150, "source_ref": "u"},
    ], validate=False)
    return con


def test_scorerun_build_is_schema_valid_and_complete() -> None:
    con = _seed_con()
    res = scorerun.build(con)  # build() schemavaliderar internt -> höjer vid fel
    sc = res["scores"]
    assert set(sc["scores"]) == set(config.party_codes())
    for _p, cats in sc["scores"].items():
        assert set(cats) == set(config.category_ids())
        for _c, v in cats.items():
            assert 0.0 <= v["score"] <= 5.0
            assert v["ci"][0] <= v["score"] <= v["ci"][1]
            assert "D_not_applicable" in v["flags"]
            # B låg+flaggad utan ståndpunkt ELLER vid tunn coverage; medium vid god täckning.
            if {"B_no_party_evidence", "B_thin_coverage"} & set(v["flags"]):
                assert v["confidence"]["B"] == "low"
            else:
                assert v["confidence"]["B"] == "medium"
    con.close()


def test_scorerun_relative_prioritization_drives_A() -> None:
    """a2 (motionsprioritering) isolerad (budget_cfg={} -> a1 inaktiv): andel, inte rå volym."""
    con = _seed_con()
    sc = scorerun.build(con, budget_cfg={})["scores"]["scores"]
    # S ägnar 100% av sina motioner åt ekonomi men M bara 25% -> S högre ekonomi-A
    assert sc["S"]["ekonomi"]["components"]["A"] > sc["M"]["ekonomi"]["components"]["A"]
    # M ägnar 75% åt klimat, S 0% -> M högre klimat-A (prioritering, inte rå volym)
    assert sc["M"]["klimat"]["components"]["A"] > sc["S"]["klimat"]["components"]["A"]
    # Utan a1-data flaggas A som a2_only (gaten håller A=a2).
    assert sc["S"]["ekonomi"]["flags"].count("A_a2_only") == 1
    con.close()


def test_scorerun_a1_budget_blends_into_A_when_gated_active() -> None:
    """Med incheckad budget_ramar (2025, alla 8 partier) aktiveras a1 och ändrar A; tom config
    faller på a2 (gaten). Bevisar blend + grind end-to-end."""
    a1_on = scorerun.build(_seed_con())["scores"]["scores"]            # produktion: läser configen
    a2_only = scorerun.build(_seed_con(), budget_cfg={})["scores"]["scores"]
    # 2025-ramen täcker alla 8 partier × alla UO -> a1 aktiv för varje kategori.
    assert all("A_a1_active" in a1_on[p][c]["flags"] for p in a1_on for c in a1_on[p])
    assert all("A_a2_only" in a2_only[p][c]["flags"] for p in a2_only for c in a2_only[p])
    # a1 ändrar A för minst en (parti, kategori) jämfört med ren a2.
    assert any(
        a1_on[p][c]["components"]["A"] != a2_only[p][c]["components"]["A"]
        for p in a1_on for c in a1_on[p]
    )
    # Regeringsblocket (M/KD/L/SD) delar samma ram -> identiskt a1-bidrag; A skiljer sig då bara
    # via a2. Här har bara M seedad aktivitet, så KD/L/SD (a2=neutral, samma) får lika A i ekonomi.
    eco = {p: a1_on[p]["ekonomi"]["components"]["A"] for p in ("KD", "L", "SD")}
    assert len(set(round(v, 6) for v in eco.values())) == 1


def _falling_unemployment_obs() -> list[dict]:
    """arbetslöshet (down=bättre) faller stadigt 2014-2021 -> förbättring under S/MP-regeringen."""
    vals = {2014: 8.0, 2015: 7.5, 2016: 7.0, 2017: 6.7, 2018: 6.5, 2019: 6.4, 2020: 6.2, 2021: 6.0}
    return [
        {"id": f"obs:scb:arbetsloshet:{y}", "category": "ekonomi",
         "submeasure": "sysselsattning_arbetsloshet", "indicator": "arbetsloshet",
         "period": str(y), "value": v, "unit": "%", "geography": "Riket",
         "source_ref": f"scb:test:{y}"}
        for y, v in vals.items()
    ]


def test_scorerun_d_attribution_credits_governing_party() -> None:
    con = _seed_con()
    warehouse.upsert(con, "observations", _falling_unemployment_obs())
    sc = scorerun.build(con)["scores"]["scores"]
    s_eco = sc["S"]["ekonomi"]
    v_eco = sc["V"]["ekonomi"]
    # S styrde när arbetslösheten föll (förbättring) -> D uppmätt, > 2.5, medel säkerhet.
    assert s_eco["components"]["D"] > 2.5
    assert "D_not_applicable" not in s_eco["flags"]
    assert s_eco["confidence"]["D"] == "medium"
    # V satt aldrig i regering -> D ej tillämplig (neutral 2.5, flaggad, låg säkerhet).
    assert v_eco["components"]["D"] == 2.5
    assert "D_not_applicable" in v_eco["flags"]
    assert v_eco["confidence"]["D"] == "low"
    # En kategori utan seedad data (försvar) förblir ej tillämplig för alla.
    assert "D_not_applicable" in sc["S"]["forsvar"]["flags"]
    con.close()
