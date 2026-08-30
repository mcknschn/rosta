"""ADR 0012: A:s nåbara tak följer förankringen. Godkännandetest till biljett #35.

Provet är ett REGELTEST. Det säger ingenting om spridning eller rangordning, eftersom ADR 0003
punkt 1 förbjuder ökad separation som mål och ADR 0012 punkt 8 deklarerar att utfallet var känt
när beslutet fattades.

Kärnan i provet är att TALET RÄKNAS, inte skrivs in. En ändrad förankring i
`config/a_forankring.yaml` ska följa med ut i metodrutan utan att någon rör texten.

Allt kör mot `:memory:`, aldrig mot data/warehouse.duckdb: CI har inget lager, och ett test som
läser disklagret passerar lokalt och fäller CI.
"""

from __future__ import annotations

import copy

import pytest

from pipeline import anchor, budget, config, score, scorerun, warehouse
from pipeline.sources import government

_A2_PERIOD = "/".join(anchor.a2_period())


def _seed() -> object:
    con = warehouse.connect(":memory:")
    warehouse.upsert(con, "responsibility", government.build_national_responsibility())
    warehouse.upsert(con, "party_activity", [
        {"party": "S", "category": "ekonomi", "committee": "FiU",
         "kind": "motion", "period": _A2_PERIOD, "count": 100, "source_ref": "u"},
    ], validate=False)
    return con


def _mix() -> tuple[float, float]:
    comp = config.scoring()["A_agerande"]["components"]
    return float(comp["a1_budgetprioritering"]), float(comp["a2_lagstiftningsprioritering"])


def _hogst(forankring: float) -> float:
    """Taket för en halva, skrivet ut ur ADR 0012 och inte lånat ur koden."""
    return 5.0 * ((1.0 - forankring) / (1.0 + forankring) + 1.0) / 2.0


def _forvantade_tak(cfg: dict | None = None) -> dict[str, float]:
    """Taket per kategori, räknat vid sidan av koden ur samma config."""
    cats, parties = config.category_ids(), config.party_codes()
    _shares, active, years = budget.a1_shares(cats, parties)
    a1 = anchor.a1_anchor_shares(cats, years=years, cfg=cfg)
    a2 = anchor.a2_anchor_shares(cats, cfg=cfg)
    w_a1, w_a2 = _mix()
    return {
        c: (w_a1 * _hogst(a1[c]) + w_a2 * _hogst(a2[c]) if c in active else _hogst(a2[c]))
        for c in cats
    }


def _sv(x: float) -> str:
    return f"{x:.2f}".replace(".", ",")


# --- 1. Taket är kvoten mot förankringen, avbildad med samma skala som betyget --------------

def test_taket_ar_kvotens_ovre_ande_avbildad() -> None:
    """(1 - förankring)/(1 + förankring) genom net_support_to_score, inget annat."""
    for forankring in (0.05, 0.21, 0.426, 0.5, 0.9):
        assert score.max_reachable_score(forankring) == pytest.approx(
            score.net_support_to_score((1.0 - forankring) / (1.0 + forankring))
        )


def test_taket_nar_5_bara_vid_en_forankring_pa_noll() -> None:
    """Metodrutans gamla mening, prövad: 5,00 kräver en förankring som inte finns."""
    assert score.max_reachable_score(0.0) == pytest.approx(5.0)
    for forankring in (0.001, 0.05, 0.426):
        assert score.max_reachable_score(forankring) < 5.0


def test_taket_sjunker_nar_forankringen_stiger() -> None:
    """Riktningen är hela poängen: en stor förankring ger ett lågt tak."""
    tak = [score.max_reachable_score(a) for a in (0.05, 0.10, 0.25, 0.45)]
    assert tak == sorted(tak, reverse=True), tak


# --- 2. Taket per kategori blandar halvorna precis som betyget gör -------------------------

def test_taket_per_kategori_blandar_halvorna_nar_a1_star() -> None:
    cats = config.category_ids()
    a1 = {c: 0.10 for c in cats}
    a2 = {c: 0.20 for c in cats}
    w_a1, w_a2 = 0.6, 0.4
    tak = scorerun._a_ceilings(cats, a1, a2, set(cats), w_a1, w_a2)
    vantat = w_a1 * score.max_reachable_score(0.10) + w_a2 * score.max_reachable_score(0.20)
    for c in cats:
        assert tak[c] == pytest.approx(vantat), c


def test_taket_vilar_pa_a2_ensam_nar_a1_faller_ur_grinden() -> None:
    """Faller a1 ur grinden är A a2 ensam, och taket ska följa med dit."""
    cats = config.category_ids()
    a1 = {c: 0.10 for c in cats}
    a2 = {c: 0.20 for c in cats}
    tak = scorerun._a_ceilings(cats, a1, a2, set(), 0.6, 0.4)
    for c in cats:
        assert tak[c] == pytest.approx(score.max_reachable_score(0.20)), c


def test_taket_haerleds_ur_configen_som_den_star() -> None:
    """Körningens tal mot ett tal räknat vid sidan av koden ur samma config."""
    cats, parties = config.category_ids(), config.party_codes()
    _shares, active, years = budget.a1_shares(cats, parties)
    w_a1, w_a2 = _mix()
    tak = scorerun._a_ceilings(
        cats, anchor.a1_anchor_shares(cats, years=years), anchor.a2_anchor_shares(cats),
        active, w_a1, w_a2,
    )
    for c, vantat in _forvantade_tak().items():
        assert tak[c] == pytest.approx(vantat), c


# --- 3. Metodrutan bär talen, ett per kategori ---------------------------------------------

def test_metodrutan_ger_taket_for_varje_kategori() -> None:
    con = _seed()
    text = scorerun.build(con)["scores"]["meta"]["coverage_technical"]
    con.close()
    for c, tak in _forvantade_tak().items():
        assert f"{c} {_sv(tak)}" in text, f"{c}: {_sv(tak)}"


def test_metodrutan_sager_att_golvet_ar_nabart_overallt() -> None:
    """Snedheten gäller taket. Golvet 0,00 nås i varje kategori (ADR 0012 punkt 4)."""
    con = _seed()
    text = scorerun.build(con)["scores"]["meta"]["coverage_technical"]
    con.close()
    assert "Golvet 0,00 är däremot nåbart överallt" in text, text


# --- 4. Talet räknas, det skrivs inte in ---------------------------------------------------

def test_metodrutans_tak_foljer_en_andrad_forankring(monkeypatch: pytest.MonkeyPatch) -> None:
    """Kärnprovet i ADR 0012 punkt 5. En inskriven konstant faller här.

    Förankringen för en a2-kategori dubblas i configen. Varje kategoris tak ska då röra sig,
    eftersom kammarens nämnare är gemensam, och metodrutan ska bära de nya talen.
    """
    andrad = copy.deepcopy(config.a_forankring())
    andrad["a2"]["chamber_motions"]["committees"]["FöU"] *= 2
    fore = _forvantade_tak()
    efter = _forvantade_tak(andrad)
    assert fore != efter, "provet biter inte: förankringen rörde inte taket"

    monkeypatch.setattr(config, "a_forankring", lambda: andrad)
    con = _seed()
    try:
        text = scorerun.build(con)["scores"]["meta"]["coverage_technical"]
    finally:
        con.close()

    for c, tak in efter.items():
        assert f"{c} {_sv(tak)}" in text, f"{c}: {_sv(tak)} saknas"
    for c, tak in fore.items():
        if _sv(tak) != _sv(efter[c]):
            assert f"{c} {_sv(tak)}" not in text, f"{c}: det gamla talet {_sv(tak)} står kvar"
