"""Golden/property-tester för delpoäng A:s a1 (budgetprioritering), pipeline/budget.py.

Rena funktioner mot injicerade fixturer (ingen livedata, ingen config-disk). Bevisar:
andelsmatten, den hårda grinden (alla 8 partier × alla kategori-UO), a2-fallback,
hård fail i stället för tyst 0, fleråriga snitt + snitt-skärning, och strukturvalidering.
"""

from __future__ import annotations

import pytest

from pipeline import budget, config

# Syntetisk UO->kategori-karta (2 kategorier, ett delat UO).
UO_MAP = {
    "UO1": {"name": "x", "map": {"ekonomi": 1.0}},
    "UO2": {"name": "y", "map": {"valfard": 1.0}},
    "UO3": {"name": "z", "map": {"ekonomi": 0.5, "valfard": 0.5}},
}
CATS = ["ekonomi", "valfard"]
PARTIES = ["A", "B"]


def _cfg(ramar_a=None, ramar_b=None) -> dict:
    ra = ramar_a or {"source_ref": "riksdag:mot:A", "UO1": 100, "UO2": 50, "UO3": 50}
    rb = ramar_b or {"source_ref": "riksdag:mot:B", "UO1": 10, "UO2": 180, "UO3": 10}
    return {"budget_years": {2025: {
        "decided_in": "bet. 2024/25:FiU1",
        "ramar": {"fa": ra, "fb": rb},
        "party_frame": {"A": {"frame": "fa", "role": "opposition"},
                        "B": {"frame": "fb", "role": "opposition"}},
    }}}


def test_andelar_ar_anslag_till_kategori_delat_med_total() -> None:
    shares, active = budget.a1_shares(CATS, PARTIES, ramar_cfg=_cfg(), uo_map=UO_MAP)
    assert active == {"ekonomi", "valfard"}
    # A: total=200; ekonomi=(100*1+50*0.5)/200=0.625 ; valfard=(50*1+50*0.5)/200=0.375
    assert shares[("A", "ekonomi")] == pytest.approx(0.625)
    assert shares[("A", "valfard")] == pytest.approx(0.375)
    # B: total=200; ekonomi=(10+5)/200=0.075 ; valfard=(180+5)/200=0.925
    assert shares[("B", "ekonomi")] == pytest.approx(0.075)
    assert shares[("B", "valfard")] == pytest.approx(0.925)


def test_tom_config_ger_inga_aktiva_kategorier() -> None:
    """Tomt budget_years => a1 inaktiv => A faller på a2 (ingen regression)."""
    assert budget.a1_shares(CATS, PARTIES, ramar_cfg={"budget_years": {}}, uo_map=UO_MAP) == ({}, set())


def test_grind_saknat_uo_inaktiverar_just_den_kategorin() -> None:
    """Om ett parti saknar ram för ett kategori-UO blir bara DEN kategorin inaktiv (a2-fallback)."""
    rb = {"source_ref": "riksdag:mot:B", "UO1": 10, "UO3": 10}  # saknar UO2 (valfard)
    _shares, active = budget.a1_shares(CATS, PARTIES, ramar_cfg=_cfg(ramar_b=rb), uo_map=UO_MAP)
    assert active == {"ekonomi"}  # valfard kräver UO2 -> inaktiv


def test_grind_saknat_parti_inaktiverar_allt() -> None:
    cfg = _cfg()
    del cfg["budget_years"][2025]["party_frame"]["B"]
    _shares, active = budget.a1_shares(CATS, ["A", "B"], ramar_cfg=cfg, uo_map=UO_MAP)
    assert active == set()


def test_total_noll_ger_hard_fail_inte_tyst_noll() -> None:
    ra = {"source_ref": "x", "UO1": 0, "UO2": 0, "UO3": 0}
    with pytest.raises(ValueError, match="totala ram"):
        budget.a1_shares(CATS, PARTIES, ramar_cfg=_cfg(ramar_a=ra), uo_map=UO_MAP)


def test_okand_frame_ger_hard_fail() -> None:
    cfg = _cfg()
    cfg["budget_years"][2025]["party_frame"]["A"]["frame"] = "saknas"
    with pytest.raises(ValueError, match="okänd frame"):
        budget.a1_shares(CATS, PARTIES, ramar_cfg=cfg, uo_map=UO_MAP)


def test_icke_numeriskt_belopp_ger_hard_fail() -> None:
    ra = {"source_ref": "x", "UO1": "mycket", "UO2": 50, "UO3": 50}
    with pytest.raises(ValueError, match="numeriskt"):
        budget.a1_shares(CATS, PARTIES, ramar_cfg=_cfg(ramar_a=ra), uo_map=UO_MAP)


def test_flerarig_aktivitet_ar_snitt_skarning() -> None:
    """a1 aktiv för en kategori endast om aktiv i VARJE inkluderat budgetår."""
    y1 = _cfg()["budget_years"][2025]
    y2 = _cfg(ramar_b={"source_ref": "y", "UO1": 10, "UO3": 10})["budget_years"][2025]  # saknar UO2
    cfg = {"budget_years": {2024: y1, 2025: y2}}
    shares, active = budget.a1_shares(CATS, PARTIES, ramar_cfg=cfg, uo_map=UO_MAP)
    assert active == {"ekonomi"}  # valfard aktiv bara 2024 -> ute ur snittet
    # ekonomi-andel för A = snitt över båda åren (samma frame) = 0.625
    assert shares[("A", "ekonomi")] == pytest.approx(0.625)


def test_determinism() -> None:
    a = budget.a1_shares(CATS, PARTIES, ramar_cfg=_cfg(), uo_map=UO_MAP)
    b = budget.a1_shares(CATS, PARTIES, ramar_cfg=_cfg(), uo_map=UO_MAP)
    assert a == b


# --- validate() -----------------------------------------------------------------

def test_validate_godkanner_valformad_och_tom() -> None:
    budget.validate(cfg={"budget_years": {}}, parties=PARTIES)
    budget.validate(cfg=_cfg(), parties=PARTIES)


def test_validate_kraver_source_ref() -> None:
    ra = {"UO1": 100, "UO2": 50, "UO3": 50}  # saknar source_ref
    with pytest.raises(ValueError, match="source_ref"):
        budget.validate(cfg=_cfg(ramar_a=ra), parties=PARTIES)


def test_validate_kraver_alla_partier_i_party_frame() -> None:
    cfg = _cfg()
    del cfg["budget_years"][2025]["party_frame"]["B"]
    with pytest.raises(ValueError, match="party_frame"):
        budget.validate(cfg=cfg, parties=PARTIES)


def test_validate_kraver_samma_uo_mangd_i_alla_frames() -> None:
    rb = {"source_ref": "y", "UO1": 10, "UO2": 180}  # saknar UO3 -> annan UO-mängd
    with pytest.raises(ValueError, match="olika UO"):
        budget.validate(cfg=_cfg(ramar_b=rb), parties=PARTIES)


def test_incheckad_budget_ramar_ar_giltig() -> None:
    """Den faktiska config/budget_ramar.yaml (oavsett innehåll) ska klara strukturvalideringen."""
    budget.validate()
    # och UO-koderna i ev. frames måste finnas i expenditure_areas
    uo_map = config.mappings()["expenditure_areas"]
    years = (config.budget_ramar() or {}).get("budget_years") or {}
    for y, block in years.items():
        for fname, frame in (block.get("ramar") or {}).items():
            for k in frame:
                if budget._UO_RE.match(str(k)):
                    assert k in uo_map, f"{y}/{fname}: okänt UO {k}"
