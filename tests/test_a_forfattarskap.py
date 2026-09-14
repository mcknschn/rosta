"""ADR 0017: a1 läser författarskap, inte uppslutning. Godkännandetest till biljett #48.

Ett REGELTEST. Ingen rad här påstår något om a1:s spann, om separationen mellan partier eller
om rangordningen (godkännandetest regel 10), eftersom ADR 0003 punkt 1 förbjuder ökad
separation som mål och ADR 0017 punkt 14 deklarerar vad som var känt när beslutet fattades.

Provet är skrivet mot REGELN och inte mot de tolv posterna: fixturerna nedan bygger sin egen
budgetconfig, så en ändrad källa aldrig kan göra ett regeltest grönt eller rött av fel skäl.
De tal som ändå står här, alltså delningstalet per parti, står där ADR 0017 godkännandetest
regel 9 kräver att hela åttavektorn låses.

Allt kör mot `:memory:`, aldrig mot data/warehouse.duckdb: CI har inget lager, och ett test som
läser disklagret passerar lokalt och fäller CI.
"""

from __future__ import annotations

import copy
import re

import pytest

from pipeline import anchor, budget, config, score, scorerun, warehouse
from pipeline.sources import government

_A2_PERIOD = "/".join(anchor.a2_period())
_SCORING = copy.deepcopy(config.scoring())

# Syntetisk UO->kategori-karta (2 kategorier, ett delat UO), som tests/test_budget.py.
UO_MAP = {
    "UO1": {"name": "x", "map": {"ekonomi": 1.0}},
    "UO2": {"name": "y", "map": {"valfard": 1.0}},
    "UO3": {"name": "z", "map": {"ekonomi": 0.5, "valfard": 0.5}},
}
CATS = ["ekonomi", "valfard"]
PARTIES = ["A", "B"]

# Klassregeln som produktionen bär, skriven här så fixturerna inte behöver disken.
REGEL = [{"basis": "votering", "exclusion": "giltighetsfel",
          "reopen_if": "en citerbar officiell svensk källa belägger författarskap"}]

_NOTER = {
    "egen_ram": "egen budgetmotion i bet. FiU1 (kolumn {p})",
    "regeringsstallning": "regeringsparti bakom prop. 1; röst i rambeslutet: Ja",
    "votering": "uppslutning bakom regeringens ram: samma röst (Ja) i voteringen om "
                "rambeslutet, bet. FiU1 punkt 2",
}


def _rad(frame: str, basis: str, party: str, note: str | None = None) -> dict:
    return {"frame": frame, "role": "opposition", "basis": basis,
            "note": _NOTER[basis].format(p=party) if note is None else note}


def _ar(basis_b: str = "egen_ram") -> dict:
    """Ett budgetår med två partier på var sin ram. B:s grund är ställbar."""
    return {
        "decided_in": "bet. FiU1",
        "ramar": {
            "fa": {"source_ref": "riksdag:mot:A", "UO1": 100, "UO2": 50, "UO3": 50},
            "fb": {"source_ref": "riksdag:mot:B", "UO1": 10, "UO2": 180, "UO3": 10},
        },
        "party_frame": {"A": _rad("fa", "egen_ram", "A"), "B": _rad("fb", basis_b, "B")},
    }


def _cfg(basis_b_2025: str = "egen_ram") -> dict:
    return {"budget_years": {2024: _ar(), 2025: _ar(basis_b_2025)}}


def _seed() -> object:
    con = warehouse.connect(":memory:")
    warehouse.upsert(con, "responsibility", government.build_national_responsibility())
    warehouse.upsert(con, "party_activity", [
        {"party": p, "category": c, "committee": k,
         "kind": "motion", "period": _A2_PERIOD, "count": n, "source_ref": "u"}
        for p, c, k, n in (("S", "ekonomi", "FiU", 100), ("M", "forsvar", "FöU", 80),
                           ("V", "valfard", "SoU", 50))
    ], validate=False)
    return con


def _mix() -> tuple[float, float]:
    comp = config.scoring()["A_agerande"]["components"]
    return float(comp["a1_budgetprioritering"]), float(comp["a2_lagstiftningsprioritering"])


def _med_mix(monkeypatch: pytest.MonkeyPatch, w_a1: float, w_a2: float) -> None:
    """Lägger blandningen på PRODUKTIONENS väg: config.scoring() är @cache-dekorerad."""
    sc = copy.deepcopy(_SCORING)
    sc["A_agerande"]["components"]["a1_budgetprioritering"] = w_a1
    sc["A_agerande"]["components"]["a2_lagstiftningsprioritering"] = w_a2
    monkeypatch.setattr(config, "scoring", lambda: sc)


def _arsandel() -> dict[str, float]:
    """parti -> giltiga år delat med fönstrets år, alltså a1:s andel av A:s täckning."""
    _shares, _active, ar = budget.a1_shares(config.category_ids(), config.party_codes())
    fonster = len(anchor.a1_years())
    return {p: len(ar[p]) / fonster for p in ar}


def _b_d_ur_flaggorna(flags: list[str], cov_den: float) -> tuple[float, float]:
    """(b, d) lästa tillbaka ur cellens krympningsflaggor, som tests/test_cell_coverage.py."""
    b = d = 0.0
    for f in flags:
        m = re.fullmatch(r"(B|D)_shrink_([\d.]+)/([\d.]+)", f)
        if not m:
            continue
        if m.group(1) == "B":
            b = float(m.group(2)) / cov_den
        else:
            d = float(m.group(2)) / cov_den
    return b, d


# --- regel 1: klassregeln väljer voteringsåren och bär skäl + återöppningsvillkor ----------

def test_klassregeln_valjer_exakt_de_parti_ar_vars_grund_ar_votering() -> None:
    """Regeln selekterar på `basis`, och den träffar varken mer eller mindre än den grunden."""
    ur_configen = {
        (p, int(y))
        for y, block in config.budget_ramar()["budget_years"].items()
        for p, pf in block["party_frame"].items() if pf["basis"] == "votering"
    }
    utesluten = budget.excluded_party_years()
    assert {(p, y) for p, ar in utesluten.items() for y in ar} == ur_configen
    assert ur_configen, "configen bär ingen voteringspost: regeltestet skulle vara tomt"


def test_klassregeln_bar_uteslutningsskal_och_atteroppningsvillkor() -> None:
    """Skälet är ett av ADR 0011:s tre, och varje regel säger vad som häver den."""
    regler = config.a1_exclusions()
    assert regler, "ingen klassregel i configen"
    for regel in regler:
        assert regel["exclusion"] in config.VALID_EXCLUSIONS, regel
        assert str(regel["reopen_if"]).strip(), regel


@pytest.mark.parametrize("falt", ["exclusion", "reopen_if"])
def test_klassregel_utan_skal_eller_villkor_faller_i_valideringen(
    monkeypatch: pytest.MonkeyPatch, falt: str
) -> None:
    sc = copy.deepcopy(_SCORING)
    sc["A_agerande"]["a1_exclusions"][0].pop(falt)
    monkeypatch.setattr(config, "scoring", lambda: sc)
    with pytest.raises(config.ConfigError, match="a1_exclusions"):
        config.validate()


def test_klassregel_med_okant_skal_faller_i_valideringen(monkeypatch: pytest.MonkeyPatch) -> None:
    """Skälet ska peka på en regel som fäller, alltså får bara de tre namnen passera."""
    sc = copy.deepcopy(_SCORING)
    sc["A_agerande"]["a1_exclusions"][0]["exclusion"] = "hittepafel"
    monkeypatch.setattr(config, "scoring", lambda: sc)
    with pytest.raises(config.ConfigError, match="a1_exclusions"):
        config.validate()


# --- regel 2: källraden bär grunden, aldrig rollen ----------------------------------------

def test_varje_voteringsnot_citerar_en_votering_och_ingen_annan_not_gor_det() -> None:
    """Provet går på `note`, alltså på källraden, och aldrig på `role` (ADR 0017 diagnos 4)."""
    for y, block in config.budget_ramar()["budget_years"].items():
        for p, pf in block["party_frame"].items():
            citerar = budget.note_cites_votering(str(pf.get("note", "")))
            assert citerar == (pf["basis"] == "votering"), f"{y}/{p}: {pf.get('note')}"


def test_rollen_faller_ingenting_och_kallraden_faller_allt() -> None:
    """En rad med rollen support men egen ram passerar; en voteringsrad utan votering faller.

    De tre fälten `role`, `basis` och källraden delar i dag exakt samma 120 parti-år, så det
    här är det enda provet som visar vilket av dem regeln vilar på.
    """
    cfg = _cfg()
    cfg["budget_years"][2025]["party_frame"]["B"]["role"] = "support"
    budget.validate(cfg=cfg, parties=PARTIES)

    fel = _cfg(basis_b_2025="votering")
    fel["budget_years"][2025]["party_frame"]["B"]["note"] = "egen budgetmotion i bet. FiU1"
    with pytest.raises(ValueError, match="votering"):
        budget.validate(cfg=fel, parties=PARTIES)

    ocksa_fel = _cfg()
    ocksa_fel["budget_years"][2025]["party_frame"]["B"]["note"] = "ja i voteringen om rambeslutet"
    with pytest.raises(ValueError, match="votering"):
        budget.validate(cfg=ocksa_fel, parties=PARTIES)


# --- regel 3: olika antal år utan förklarande klassregel är hård fail ----------------------

def test_olika_antal_ar_per_parti_utan_klassregel_ar_hard_fail() -> None:
    """Det tysta medlet i ADR 0017 diagnos 6: en avvikelse per parti passerade osedd."""
    cfg = _cfg()
    del cfg["budget_years"][2025]["party_frame"]["B"]
    with pytest.raises(ValueError, match="klassregel"):
        budget.a1_shares(CATS, PARTIES, ramar_cfg=cfg, uo_map=UO_MAP, exclusions=REGEL)


def test_olika_antal_ar_med_klassregel_gar_igenom_och_syns_i_arsmangden() -> None:
    cfg = _cfg(basis_b_2025="votering")
    _shares, _active, ar = budget.a1_shares(
        CATS, PARTIES, ramar_cfg=cfg, uo_map=UO_MAP, exclusions=REGEL
    )
    assert ar == {"A": [2024, 2025], "B": [2024]}


def test_parti_utan_giltiga_ar_ar_hard_fail_inte_en_tyst_grind() -> None:
    """Grinden får inte avgöras av de sju andra när ett parti saknar underlag helt.

    Utan provet passerar ett parti vars alla år är uteslutna rakt igenom: det snävar inte av
    någon kategori, och ingen andel skrivs för det. Det är samma tystnad som ADR 0017
    diagnos 6 tog fram i ljuset, ett steg längre in.
    """
    cfg = {"budget_years": {2024: _ar("votering"), 2025: _ar("votering")}}
    with pytest.raises(ValueError, match="inga giltiga budgetår"):
        budget.a1_shares(CATS, PARTIES, ramar_cfg=cfg, uo_map=UO_MAP, exclusions=REGEL)


def test_klausulen_traffar_aldrig_utan_ett_provat_ar() -> None:
    """En årsmängd utan gemensamma år med configen ger noll prövningar, alltså ingen träff.

    Klausulen fäller ett parti som saknar egen NOLLPUNKT. Ett parti vars år aldrig jämförs
    har inte visat något alls, och en vakuös träff skulle fälla a1 globalt på tomt underlag.
    """
    cfg = _cfg()
    decided = {2024: {"UO1": 100, "UO2": 50, "UO3": 50},
               2025: {"UO1": 100, "UO2": 50, "UO3": 50}}
    ok, offenders = budget.a1_admissible(
        PARTIES, decided, ramar_cfg=cfg, years_by_party={"A": [1999], "B": [1999]}
    )
    assert ok and offenders == [], offenders


def test_uteslutna_ar_vager_inte_in_i_medlet() -> None:
    """Andelen är medel över partiets GILTIGA år, aldrig över alla år i configen."""
    cfg = _cfg(basis_b_2025="votering")
    cfg["budget_years"][2025]["ramar"]["fb"] = {
        "source_ref": "riksdag:mot:B", "UO1": 200, "UO2": 0, "UO3": 0,
    }
    shares, _active, _ar = budget.a1_shares(
        CATS, PARTIES, ramar_cfg=cfg, uo_map=UO_MAP, exclusions=REGEL
    )
    # B:s giltiga år är 2024 ensamt: (10 + halva UO3) / 200 = 0,075 i ekonomi.
    assert shares[("B", "ekonomi")] == pytest.approx(0.075)


# --- regel 4: validate låser basis och kräver note -----------------------------------------

def test_validate_laser_basis_till_en_sluten_mangd() -> None:
    cfg = _cfg()
    cfg["budget_years"][2025]["party_frame"]["B"]["basis"] = "eget_tycke"
    with pytest.raises(ValueError, match="basis"):
        budget.validate(cfg=cfg, parties=PARTIES)


def test_validate_kraver_note_pa_varje_rad() -> None:
    cfg = _cfg()
    del cfg["budget_years"][2025]["party_frame"]["B"]["note"]
    with pytest.raises(ValueError, match="note"):
        budget.validate(cfg=cfg, parties=PARTIES)


def test_validate_kraver_basis_pa_varje_rad() -> None:
    cfg = _cfg()
    del cfg["budget_years"][2025]["party_frame"]["B"]["basis"]
    with pytest.raises(ValueError, match="basis"):
        budget.validate(cfg=cfg, parties=PARTIES)


# --- regel 5: täljarens år är förankringens år, per parti ----------------------------------

def test_taljarens_ar_ar_forankringens_ar_for_varje_parti() -> None:
    """ADR 0007 godkännandetest 1 ett steg ned, från kategori till parti."""
    cats, parties = config.category_ids(), config.party_codes()
    _shares, _active, ar = budget.a1_shares(cats, parties)
    fonster = set(anchor.a1_years())
    assert set(ar) == set(parties)
    union: set[int] = set()
    utesluten = budget.excluded_party_years()
    for p in parties:
        assert ar[p], f"{p} har inga giltiga budgetår kvar"
        assert set(ar[p]) <= fonster, p
        assert fonster - set(ar[p]) <= set(utesluten.get(p, ())), f"{p} tappar år utan skäl"
        union |= set(ar[p])
    assert union == fonster, "fönstret har krympt tyst"


def test_a1_kvoten_raknas_mot_partiets_egna_ars_forankring(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Förankringen följer partiets giltiga år (ADR 0017 punkt 6), hela vägen ut i betyget.

    Blandningen läggs på 1/0 så A ÄR a1, och talet räknas sedan vid sidan av koden ur samma
    config. Utan mutationen skulle a2 dölja skillnaden.
    """
    cats, parties = config.category_ids(), config.party_codes()
    shares, active, ar = budget.a1_shares(cats, parties)
    hela = anchor.a1_anchor_shares(cats)
    egna = {p: anchor.a1_anchor_shares(cats, years=ar[p]) for p in parties}
    assert any(egna[p] != hela for p in parties), \
        "ingen förankring skiljer sig från fönstrets: provet biter inte"

    _med_mix(monkeypatch, 1.0, 0.0)
    con = _seed()
    try:
        ut = scorerun.build(con)["scores"]["scores"]
    finally:
        con.close()
    for p in parties:
        for c in active:
            vantat = score.net_support_to_score(
                score.bounded_quotient(shares[(p, c)], egna[p][c])
            )
            assert ut[p][c]["components"]["A"] == pytest.approx(vantat, abs=0.01), f"{p}/{c}"


# --- regel 6: villkorsklausulen prövas på partiets egna år, rättsverkan global -------------

def test_klausulen_provas_pa_partiets_egen_giltiga_arsmangd() -> None:
    """Ett parti som matchar den antagna ramen i varje år det har KVAR fäller a1.

    Fixturen är byggd så att svaret skiljer sig mot den gamla regeln: A avviker från den
    antagna ramen 2025, men 2025 är uteslutet för A, så bara 2024 prövas.
    """
    cfg = {"budget_years": {2024: _ar(), 2025: _ar()}}
    cfg["budget_years"][2025]["party_frame"]["A"] = _rad("fa", "votering", "A")
    decided = {
        2024: {"UO1": 100, "UO2": 50, "UO3": 50},      # A:s ram 2024
        2025: {"UO1": 10, "UO2": 180, "UO3": 10},      # B:s ram 2025, alltså inte A:s
    }
    ar = budget.valid_party_years(cfg, exclusions=REGEL, parties=PARTIES)
    assert ar["A"] == [2024]
    ok, offenders = budget.a1_admissible(PARTIES, decided, ramar_cfg=cfg, years_by_party=ar)
    assert not ok and offenders == ["A"], offenders

    # Prövad över ALLA år i configen fäller klausulen inte, alltså biter provet på rätt sak.
    ok_alla, _ = budget.a1_admissible(PARTIES, decided, ramar_cfg=cfg)
    assert ok_alla


def test_klausulens_rattsverkan_ar_global() -> None:
    """Fyrar den för ett parti faller a1 ur A för alla åtta, alltså i varje kategori."""
    decided = config.a_forankring()["a1"]["decided_frames"]
    kort = copy.deepcopy(config.budget_ramar())
    kort["budget_years"] = {y: b for y, b in kort["budget_years"].items() if y <= 2014}
    ar = budget.valid_party_years(kort)
    ok, offenders = budget.a1_admissible(
        config.party_codes(), decided, ramar_cfg=kort, years_by_party=ar
    )
    assert not ok and offenders, "ett kort fönster ska fälla klausulen"

    original = anchor.a1_years
    anchor.a1_years = lambda cfg=None: sorted(int(y) for y in kort["budget_years"])  # noqa: ARG005
    con = _seed()
    try:
        ut = scorerun.build(con, budget_cfg=kort)["scores"]["scores"]
    finally:
        anchor.a1_years = original
        con.close()
    for p, cats in ut.items():
        for c, cell in cats.items():
            assert "A_a2_only" in cell["flags"], f"{p}/{c}"
            assert f"A_a1_inadmissible:{','.join(sorted(offenders))}" in cell["flags"]


# --- regel 7 och 8: Mättaket är kategorikonstant, cellens A-täckning är per parti ----------

def test_mattaket_ar_kategorikonstant_medan_cellens_a_tackning_ar_per_parti() -> None:
    """Godkännandetest regel 7. De två prövas i SAMMA test, annars kan delningen göras åt
    fel håll utan att något faller (ADR 0017 punkt 12)."""
    andel = _arsandel()
    assert len(set(andel.values())) > 1, "alla partier har lika många år: provet biter inte"
    w_a1, w_a2 = _mix()
    w = config.scoring()["subscore_weights"]
    cov_den = scorerun._coverage_denominators()
    sub_w = scorerun._submeasure_weights()
    b_tak = scorerun._b_covered_submeasures()
    d_tak = scorerun._d_covered_submeasures()

    con = _seed()
    try:
        res = scorerun.build(con)["scores"]
    finally:
        con.close()
    tak = {c["id"]: c["coverage_ceiling"] for c in res["categories"]}

    for cid, taket in tak.items():
        b = sum(sub_w[cid][s] for s in b_tak[cid]) / cov_den[cid]
        d = sum(sub_w[cid][s] for s in d_tak[cid]) / cov_den[cid]
        flaggor = next(iter(res["scores"].values()))[cid]["flags"]
        a_konstant = w_a1 + w_a2 if "A_a1_active" in flaggor else w_a2
        assert taket == pytest.approx(score.cell_coverage(a_konstant, b, d), abs=1e-9), cid
        if "A_a1_active" in flaggor:
            # Taket får inte vara räknat på ett partis andel: det vore åtta tal per kategori.
            minsta = w_a1 * min(andel.values()) + w_a2
            assert taket != pytest.approx(score.cell_coverage(minsta, b, d), abs=1e-9), cid

    # Cellens A-täckning följer partiet, och den är aldrig högre än takets A-del.
    for p, cats in res["scores"].items():
        for cid, cell in cats.items():
            b, d = _b_d_ur_flaggorna(cell["flags"], cov_den[cid])
            a = (w_a1 * andel[p] + w_a2) if "A_a1_active" in cell["flags"] else w_a2
            vantat = w["A"] * a + w["B"] * b + w["D"] * d
            assert cell["coverage"] == pytest.approx(vantat, abs=0.002), f"{p}/{cid}"


@pytest.mark.parametrize("mix", [(0.5, 0.5), (0.25, 0.75), (0.75, 0.25)])
def test_a_tackningen_arver_blandningen_ur_configen(
    monkeypatch: pytest.MonkeyPatch, mix: tuple[float, float]
) -> None:
    """Godkännandetest regel 8, med a1 aktiv. Talet ska följa configen, aldrig bäras av koden."""
    w_a1, w_a2 = mix
    andel = _arsandel()
    cov_den = scorerun._coverage_denominators()
    w = config.scoring()["subscore_weights"]
    _med_mix(monkeypatch, w_a1, w_a2)
    con = _seed()
    try:
        ut = scorerun.build(con)["scores"]["scores"]
    finally:
        con.close()
    for p, cats in ut.items():
        for cid, cell in cats.items():
            assert "A_a1_active" in cell["flags"], f"{p}/{cid}"
            b, d = _b_d_ur_flaggorna(cell["flags"], cov_den[cid])
            vantat = w["A"] * (w_a1 * andel[p] + w_a2) + w["B"] * b + w["D"] * d
            assert cell["coverage"] == pytest.approx(vantat, abs=0.002), f"{p}/{cid}"


@pytest.mark.parametrize("mix", [(0.5, 0.5), (0.25, 0.75)])
def test_grindfallet_ar_orort_och_bar_a2s_vikt_ensam(
    monkeypatch: pytest.MonkeyPatch, mix: tuple[float, float]
) -> None:
    """Godkännandetest regel 8, andra grindläget: faller a1 ur grinden är A-täckningen w_a2."""
    w_a1, w_a2 = mix
    cov_den = scorerun._coverage_denominators()
    w = config.scoring()["subscore_weights"]
    kort = copy.deepcopy(config.budget_ramar())
    kort["budget_years"] = {y: b for y, b in kort["budget_years"].items() if y <= 2014}
    _med_mix(monkeypatch, w_a1, w_a2)
    original = anchor.a1_years
    anchor.a1_years = lambda cfg=None: sorted(int(y) for y in kort["budget_years"])  # noqa: ARG005
    con = _seed()
    try:
        ut = scorerun.build(con, budget_cfg=kort)["scores"]["scores"]
    finally:
        anchor.a1_years = original
        con.close()
    for p, cats in ut.items():
        for cid, cell in cats.items():
            assert "A_a2_only" in cell["flags"], f"{p}/{cid}"
            b, d = _b_d_ur_flaggorna(cell["flags"], cov_den[cid])
            vantat = w["A"] * w_a2 + w["B"] * b + w["D"] * d
            assert cell["coverage"] == pytest.approx(vantat, abs=0.002), f"{p}/{cid}"


def test_as_nabara_tak_matas_aldrig_med_den_partivisa_forankringen() -> None:
    """Taket är modellens och inte partiets (ADR 0014 punkt 3): en förankring per kategori."""
    cats = config.category_ids()
    partivis = {p: {c: 0.10 for c in cats} for p in config.party_codes()}
    with pytest.raises(ValueError, match="EN förankring per kategori"):
        scorerun._a_ceilings(cats, partivis, {c: 0.20 for c in cats}, set(cats), *_mix())


# --- regel 9: hela åttavektorn är låst, och delningstalet redovisas per grund --------------

def test_delningstalet_ar_last_for_alla_atta_och_per_grund() -> None:
    """Talet räknas på de år a1 faktiskt mäter, och uteslutningen står i en egen kolumn."""
    delad = {r.party: (r.shared, r.valid, r.excluded) for r in budget.shared_frame_years()}
    assert delad == {
        "MP": (9, 15, 0), "S": (9, 15, 0), "KD": (8, 15, 0), "M": (8, 15, 0),
        "L": (8, 13, 2), "C": (5, 13, 2), "V": (1, 10, 5), "SD": (0, 12, 3),
    }


def test_delningstalet_ar_tomt_utan_budgetkalla() -> None:
    assert budget.shared_frame_years({}) == []


def test_metodrutan_bar_bada_kolumnerna_och_namnger_uteslutningen() -> None:
    """Rutan ska bära både delningen och uteslutningen, aldrig byta det ena mot det andra."""
    con = _seed()
    try:
        text = scorerun.build(con)["scores"]["meta"]["coverage_technical"]
    finally:
        con.close()
    for r in budget.shared_frame_years():
        assert f"{r.party} {r.shared} av {r.valid}" in text, r
    assert "giltighetsfel" in text, text
    assert config.EXCLUSION_REASONS["giltighetsfel"] in text, text
    assert "uteslutna ur a1" in text, text
