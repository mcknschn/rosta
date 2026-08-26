"""Fas 5: scorerun bygger en schema-giltig scores.json ur warehouse."""

from __future__ import annotations

from pipeline import anchor, config, scorerun, warehouse
from pipeline.sources import government

# a2:s täljare ska ligga på exakt förankringens period (ADR 0007 punkt 1). Fixturen läser
# perioden ur configen i stället för att skriva av den, så provet följer med om den ändras.
_A2_PERIOD = "/".join(anchor.a2_period())


def _seed_con():
    con = warehouse.connect(":memory:")
    warehouse.upsert(con, "responsibility", government.build_national_responsibility())
    warehouse.upsert(con, "party_activity", [
        # S ägnar 100% av sina motioner åt ekonomi
        {"party": "S", "category": "ekonomi", "committee": "FiU",
         "kind": "motion", "period": _A2_PERIOD, "count": 100, "source_ref": "u"},
        # M ägnar 25% åt ekonomi (50 av 200) och 75% åt klimat (150 av 200)
        {"party": "M", "category": "ekonomi", "committee": "FiU",
         "kind": "motion", "period": _A2_PERIOD, "count": 50, "source_ref": "u"},
        {"party": "M", "category": "klimat", "committee": "MJU",
         "kind": "motion", "period": _A2_PERIOD, "count": 150, "source_ref": "u"},
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
            # B:s säkerhet härleds ur evidensen och sänks ett steg vid tunn täckning
            # (ADR 0004). Utan ståndpunkter är den låg per config.
            if "B_no_party_evidence" in v["flags"]:
                assert v["confidence"]["B"] == "low"
            elif "B_thin_coverage" in v["flags"]:
                assert v["confidence"]["B"] in {"medium", "low"}  # steget ned utesluter high
            else:
                assert v["confidence"]["B"] in {"high", "medium", "low"}
    con.close()


def test_b_sakerhet_foljer_inte_langre_tackningsflaggan() -> None:
    """ADR 0004 diagnos punkt 3: B:s etikett följde B_thin_coverage i 56 av 56 celler, alltså
    läste den aldrig evidensen. Testet låser att etiketten INTE är en funktion av flaggan.

    Vittnet bytte form 2026-08-23 (#26, ADR 0006). Fram till dess var vittnet en cell med GOD
    täckning men LÅG säkerhet, alltså svag evidens bakom en väl täckt cell. Den symmetriska
    evidensgrinden tar bort just den möjligheten: varje admitterad liggarpost bär numera
    confidence minst medium, så conf_kat kan aldrig hamna under medium-tröskeln och en låg
    B-etikett kan bara komma ur steget ned vid tunn täckning. Egenskapen prövas därför nu på
    VARIATION i stället: bland cellerna med god täckning ska mer än en säkerhetsnivå förekomma.
    """
    con = _seed_con()
    sc = scorerun.build(con)["scores"]["scores"]
    con.close()
    god_tackning = [
        v["confidence"]["B"] for _p, cats in sc.items() for _c, v in cats.items()
        if not {"B_no_party_evidence", "B_thin_coverage"} & set(v["flags"])
    ]
    assert len(set(god_tackning)) > 1, (
        "B:s säkerhet är konstant över alla väl täckta celler — etiketten läser inte evidensen "
        f"utan följer täckningsflaggan igen: {sorted(set(god_tackning))}"
    )


def test_lag_b_sakerhet_kraver_tunn_tackning_efter_symmetriska_grinden() -> None:
    """Följdinvariant av ADR 0006: grinden kräver confidence minst medium vid dörren, så en
    LÅG B-etikett kan bara komma ur steget ned vid tunn täckning (eller ur att kategorin helt
    saknar partievidens). En låg etikett i en väl täckt cell skulle betyda att en post med
    confidence low tagit sig in i poängen, alltså att grinden läcker."""
    con = _seed_con()
    sc = scorerun.build(con)["scores"]["scores"]
    con.close()
    lackor = [
        (p, c) for p, cats in sc.items() for c, v in cats.items()
        if v["confidence"]["B"] == "low"
        and not {"B_no_party_evidence", "B_thin_coverage"} & set(v["flags"])
    ]
    assert not lackor, f"låg B-säkerhet utan tunn täckning — grinden läcker: {lackor}"


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
    # Bara S och M har seedad motionsaktivitet, så de sex övriga partierna delar exakt samma a2.
    # Deras A skiljer sig därmed bara genom a1, och ska följa a1-andelen: samma andel ger samma A,
    # och en högre andel ger ett högre A. Biljett #21 skrev provet som ett tal om att M, KD, L och
    # SD delade ram, vilket gällde det treåriga fönstret. Över 2011-2025 delar de ram bara de år de
    # regerade tillsammans, så provet skrivs som den egenskap det faktiskt skyddade.
    from pipeline import budget
    cats, parties = config.category_ids(), config.party_codes()
    shares, _active, _years = budget.a1_shares(cats, parties)
    tysta = [p for p in parties if p not in ("S", "M")]
    ordning = sorted(tysta, key=lambda p: shares[(p, "ekonomi")])
    a_values = [a1_on[p]["ekonomi"]["components"]["A"] for p in ordning]
    assert a_values == sorted(a_values), dict(zip(ordning, a_values, strict=True))
    for first, second in zip(ordning, ordning[1:], strict=False):
        if shares[(first, "ekonomi")] == shares[(second, "ekonomi")]:
            assert (a1_on[first]["ekonomi"]["components"]["A"]
                    == a1_on[second]["ekonomi"]["components"]["A"])


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
    # S styrde när arbetslösheten föll (förbättring) -> D uppmätt, > 2.5. Med coverage_shrink
    # (default på) täcker den ensamma serien bara 22/73 av ekonomins icke-target-vikt ->
    # D_thin_coverage + säkerhet sänkt ett steg (medium -> low). Se test_d_breadth_gate.
    assert s_eco["components"]["D"] > 2.5
    assert "D_not_applicable" not in s_eco["flags"]
    assert "D_coverage_22/73" in s_eco["flags"]
    assert "D_thin_coverage" in s_eco["flags"]
    assert s_eco["confidence"]["D"] == "low"
    # V satt aldrig i regering -> D ej tillämplig (neutral 2.5, flaggad, låg säkerhet).
    assert v_eco["components"]["D"] == 2.5
    assert "D_not_applicable" in v_eco["flags"]
    assert v_eco["confidence"]["D"] == "low"
    # En kategori utan seedad data (försvar) förblir ej tillämplig för alla.
    assert "D_not_applicable" in sc["S"]["forsvar"]["flags"]
    con.close()
