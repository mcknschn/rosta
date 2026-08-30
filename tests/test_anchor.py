"""Golden-tester för förankringen till delpoäng A (ADR 0005), pipeline/anchor.py.

Rena funktioner med injicerbara fixturer -> ingen livedata och ingen fil-IO.
"""

from __future__ import annotations

import pytest

from pipeline import anchor, config

CATS = ["ekonomi", "valfard"]
UO_MAP = {
    "UO1": {"name": "ett", "map": {"ekonomi": 1.0}},
    "UO2": {"name": "två", "map": {"valfard": 1.0}},
    "UO3": {"name": "tre", "map": {}},          # utan kategori: bara i nämnaren
}
COMMITTEES = {"FiU": "ekonomi", "SkU": "ekonomi", "SoU": "valfard"}


def _cfg(**over: object) -> dict[str, object]:
    cfg: dict[str, object] = {
        "window": {"start": 2020, "end": 2021,
                   "a1_bound": 2018, "a1_frames_bound": 2020, "a2_bound": 2020},
        "a1": {"unit": "mnkr", "decided_frames": {
            2020: {"source_ref": "x", "UO1": 100, "UO2": 100, "UO3": 200},
            2021: {"source_ref": "x", "UO1": 200, "UO2": 100, "UO3": 100},
        }},
        "a2": {"chamber_motions": {"source_ref": "x", "period": "2020-01-01/2021-12-31",
                                   "committees": {"FiU": 30, "SkU": 10, "SoU": 60}}},
    }
    cfg.update(over)
    return cfg


def test_window_lases_ur_configen() -> None:
    assert anchor.window(cfg=_cfg()) == (2020, 2021)


def test_a1_forankring_ar_medel_over_fonstrets_ar() -> None:
    """2020 ger ekonomi 100/400 = 0,25 och 2021 ger 200/400 = 0,50 -> medel 0,375."""
    out = anchor.a1_anchor_shares(CATS, cfg=_cfg(), uo_map=UO_MAP)
    assert out["ekonomi"] == pytest.approx(0.375)
    assert out["valfard"] == pytest.approx(0.25)


def test_a1_forankring_raknar_bara_fonstrets_ar() -> None:
    """Ett år utanför fönstret finns i configen men får inte påverka medlet."""
    cfg = _cfg()
    cfg["a1"]["decided_frames"][2019] = {"source_ref": "x", "UO1": 400, "UO2": 0, "UO3": 0}
    assert anchor.a1_anchor_shares(CATS, cfg=cfg, uo_map=UO_MAP)["ekonomi"] == pytest.approx(0.375)


def test_a1_saknat_ar_i_fonstret_ar_hard_fail() -> None:
    cfg = _cfg()
    del cfg["a1"]["decided_frames"][2021]
    with pytest.raises(ValueError, match="2021"):
        anchor.a1_anchor_shares(CATS, cfg=cfg, uo_map=UO_MAP)


def test_a1_saknat_utgiftsomrade_ar_hard_fail() -> None:
    """En saknad UO-cell får aldrig bli en tyst nolla i nämnaren."""
    cfg = _cfg()
    del cfg["a1"]["decided_frames"][2020]["UO2"]
    with pytest.raises(ValueError, match="UO2"):
        anchor.a1_anchor_shares(CATS, cfg=cfg, uo_map=UO_MAP)


def test_a2_forankring_ar_kammarens_kategoriandel() -> None:
    out = anchor.a2_anchor_shares(CATS, cfg=_cfg(), committee_map=COMMITTEES)
    assert out["ekonomi"] == pytest.approx(0.4)
    assert out["valfard"] == pytest.approx(0.6)


def _kategoriandelar(counts: dict[str, int]) -> dict[str, float]:
    """Kategoriandelen av ett utskottsaggregat, räknad i provet och inte av koden."""
    per_cat = {cat: 0.0 for cat in CATS}
    for org, cat in COMMITTEES.items():
        per_cat[cat] += float(counts[org])
    return {cat: n / sum(float(counts[org]) for org in COMMITTEES) for cat, n in per_cat.items()}


def test_a2_forankring_ar_andelen_av_summan_inte_medlet_av_arsandelarna() -> None:
    """a2:s förankring poolar åren, alltså varje år vägt efter sitt eget underlag.

    ADR 0013 punkt 1 och 4. Formen är a2:s, inte a1:s: a1 har ett tal per år och inget naturligt
    antal att poola, medan a2 har ett antal. Configen bär kammarens tal som ett enda aggregat per
    utskott, så provet bär årsuppdelningen själv och prövar formen mot den.

    Årsvolymen varierar mellan åren. Utan den variationen sammanfaller de två formerna och provet
    blir tomt, så den första satsen prövar att provet har något att skilja på.
    """
    per_year = {
        2020: {"FiU": 30, "SkU": 10, "SoU": 60},     # 100 motioner, ekonomi 0,40
        2021: {"FiU": 6, "SkU": 2, "SoU": 2},        # 10 motioner, ekonomi 0,80
    }
    aggregate = {org: sum(year[org] for year in per_year.values()) for org in COMMITTEES}
    poolad = _kategoriandelar(aggregate)
    arsmedel = {
        cat: sum(_kategoriandelar(year)[cat] for year in per_year.values()) / len(per_year)
        for cat in CATS
    }
    assert poolad["ekonomi"] != pytest.approx(arsmedel["ekonomi"]), "fixturen skiljer inte formerna"

    cfg = _cfg()
    cfg["a2"]["chamber_motions"]["committees"] = aggregate
    out = anchor.a2_anchor_shares(CATS, cfg=cfg, committee_map=COMMITTEES)

    for cat in CATS:
        assert out[cat] == pytest.approx(poolad[cat])
        assert out[cat] != pytest.approx(arsmedel[cat])


def test_a2_saknat_utskott_ar_hard_fail() -> None:
    cfg = _cfg()
    del cfg["a2"]["chamber_motions"]["committees"]["SkU"]
    with pytest.raises(ValueError, match="SkU"):
        anchor.a2_anchor_shares(CATS, cfg=cfg, committee_map=COMMITTEES)


def test_forankringarna_summerar_till_ett_over_kategorierna() -> None:
    """Båda halvorna är andelar av samma helhet, så de kan jämföras med partiernas andelar."""
    a1 = anchor.a1_anchor_shares(CATS, cfg=_cfg(), uo_map=UO_MAP)
    a2 = anchor.a2_anchor_shares(CATS, cfg=_cfg(), committee_map=COMMITTEES)
    assert sum(a2.values()) == pytest.approx(1.0)
    assert sum(a1.values()) < 1.0            # UO3 saknar kategori och stannar i nämnaren


def test_validate_godtar_den_incheckade_configen() -> None:
    anchor.validate()


def test_validate_faller_pa_fonster_i_fel_ordning() -> None:
    cfg = _cfg(window={"start": 2021, "end": 2020})
    with pytest.raises(ValueError):
        anchor.validate(cfg=cfg)


def test_incheckad_config_tacker_hela_fonstret() -> None:
    """Varje år i fönstret har en beslutad ram med 27 UO och en källhänvisning."""
    cfg = config.a_forankring()
    start, end = anchor.window(cfg=cfg)
    frames = cfg["a1"]["decided_frames"]
    for year in range(start, end + 1):
        assert year in frames, f"budgetår {year} saknas"
        assert str(frames[year].get("source_ref", "")).strip(), f"{year} saknar source_ref"
        assert {f"UO{n}" for n in range(1, 28)} <= set(frames[year]), f"{year} saknar UO"


def test_incheckad_config_tacker_varje_utskott_i_mappningen() -> None:
    committees = config.a_forankring()["a2"]["chamber_motions"]["committees"]
    assert set(config.mappings()["committee_to_category"]) <= set(committees)


# --- Godkännandetest ur biljett #21, skrivna före körningen -------------------------

def _a1_scores(category: str) -> dict[str, float]:
    """a1-delbetyget per parti i en kategori, mot den incheckade förankringen."""
    from pipeline import budget, score
    cats, parties = config.category_ids(), config.party_codes()
    shares, _active, years = budget.a1_shares(cats, parties)
    a1_anchor = anchor.a1_anchor_shares(cats, years=years)
    return {
        p: score.net_support_to_score(
            score.bounded_quotient(shares[(p, category)], a1_anchor[category])
        )
        for p in parties
    }


def test_godkannande_nastan_lika_andelar_ger_nastan_lika_betyg() -> None:
    """Två partier vars andelar nästan sammanfaller ska få nästan samma betyg.

    Provet stod i biljett #21 som ett tal om klimat, där 8,73e-06 skilde S från M-blocket
    under det treåriga fönstret. Efter ADR 0007 mäter a1 femton år, och just det paret finns
    inte längre. Egenskapen provet skyddar är avbildningens KONTINUITET, som rangnormaliseringen
    bröt, och den skrivs här som den egenskapen i stället för som ett tal om ett visst par.
    """
    from pipeline import budget
    cats, parties = config.category_ids(), config.party_codes()
    shares, _active, _years = budget.a1_shares(cats, parties)
    pairs = 0
    for category in cats:
        a1 = _a1_scores(category)
        for i, first in enumerate(parties):
            for second in parties[i + 1:]:
                if abs(shares[(first, category)] - shares[(second, category)]) >= 1e-4:
                    continue
                pairs += 1
                assert abs(a1[first] - a1[second]) < 0.01, f"{category}: {first} mot {second}"
    assert pairs, "inget nära par i underlaget: provet skulle vara tomt"


def test_godkannande_samma_ram_ger_fortfarande_samma_a1() -> None:
    """Partier på samma ram ett år ska ha samma andel det året, aldrig utjämnas isär.

    Biljett #21 skrev provet som ett tal om M, KD, L och SD, som delade ram i alla tre år det
    fönstret bar. Över femton år delar de ram bara de år de regerade tillsammans, medan andra
    par delar ram andra år: S, MP och V lade en gemensam budgetmotion 2011, och M, C, L och KD
    en gemensam 2015. Provet läses därför per år, ur configens egen party_frame.
    """
    from pipeline import budget
    cfg = config.budget_ramar()["budget_years"]
    umap = config.mappings()["expenditure_areas"]
    cat_uo_w = budget.category_uo_weights(umap)
    shared_years = 0
    for year, block in cfg.items():
        frames = budget.resolve_frames(block)
        by_frame: dict[str, list[str]] = {}
        for party, spec in block["party_frame"].items():
            by_frame.setdefault(spec["frame"], []).append(party)
        for frame, members in by_frame.items():
            if len(members) < 2:
                continue
            shared_years += 1
            per_party = {p: budget.category_shares_for_party(frames[p], cat_uo_w)
                         for p in members}
            for category in config.category_ids():
                values = {round(per_party[p][category], 12) for p in members}
                assert len(values) == 1, f"{year}/{frame}/{category}: {values}"
    assert shared_years, "ingen gemensam ram i configen: provet skulle vara tomt"


def test_godkannande_a1_ar_inte_langre_spant_over_hela_skalan() -> None:
    """Rangnormaliseringen lade alltid lägsta partiet på 0,00 och högsta på 5,00."""
    for category in config.category_ids():
        a1 = _a1_scores(category)
        assert min(a1.values()) > 0.0
        assert max(a1.values()) < 5.0


def test_a1_kategori_utan_utgiftsomrade_ar_hard_fail() -> None:
    """En förankring på noll ger kvoten +1, alltså 5,00 till alla åtta. Aldrig tyst."""
    with pytest.raises(ValueError, match="trygghet"):
        anchor.a1_anchor_shares(CATS + ["trygghet"], cfg=_cfg(), uo_map=UO_MAP)


def test_a2_kategori_utan_utskott_ar_hard_fail() -> None:
    with pytest.raises(ValueError, match="trygghet"):
        anchor.a2_anchor_shares(CATS + ["trygghet"], cfg=_cfg(), committee_map=COMMITTEES)
