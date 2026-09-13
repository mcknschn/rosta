"""ADR 0015: A:s två kanaler väger lika. Godkännandetest till biljett #43.

Provet är ett REGELTEST. Det säger ingenting om betyg, band eller rangordning, eftersom
ADR 0003 punkt 1 förbjuder ökad separation som mål och ADR 0015 punkt 8 deklarerar vad som var
känt när beslutet fattades.

Kärnan i provet är MUTATIONEN. Koden ska följa blandningen i configen och aldrig bära ett eget
tal. Ett enda mutationsvärde räcker inte: en hårdkodad fallback på 0,75 passerar mutationen
0,25/0,75 men är fel vid standardvärdet. En fixtur som bara kör med aktiv grind missar vägen där
A blir a2 ensam och täckningen sätts ur a2:s vikt. Repot har haft just den sortens fel förut, i
biljett #37.

Regel 6, alltså reglagets spann, ligger i tests/test_robustness.py där reglagetabellen prövas.

Allt kör mot `:memory:`, aldrig mot data/warehouse.duckdb: CI har inget lager, och ett test som
läser disklagret passerar lokalt och fäller CI.
"""

from __future__ import annotations

import copy
import random

import pytest

from pipeline import anchor, config, robustness, scorerun, warehouse
from pipeline.sources import government

_A2_PERIOD = "/".join(anchor.a2_period())

# Configen som den står på disk, läst en gång. Mutationerna utgår alltid härifrån, aldrig från
# en redan utbytt loader, så ett par aldrig kan ärva ett annat pars tal.
_SCORING = copy.deepcopy(config.scoring())

# Två viktpar utöver produktionens, ett på vardera sidan om jämnhöjd
# (ADR 0015 godkännandetest regel 2).
_MUTATIONER = ((0.25, 0.75), (0.75, 0.25))

# Tidöåren ensamma fäller villkorsklausulen i ADR 0007 punkt 4, och då vilar A på a2 i varje
# cell. Det är den enda vägen till A_a2_only som inte kräver att grinden i budget.py rörs.
_KORT_FONSTER = (2023, 2024, 2025)


def _seed() -> object:
    con = warehouse.connect(":memory:")
    warehouse.upsert(con, "responsibility", government.build_national_responsibility())
    warehouse.upsert(con, "party_activity", [
        {"party": p, "category": c, "committee": k,
         "kind": "motion", "period": _A2_PERIOD, "count": n, "source_ref": "u"}
        for p, c, k, n in (
            ("S", "ekonomi", "FiU", 100),
            ("M", "forsvar", "FöU", 80),
            ("M", "ekonomi", "FiU", 20),
            ("V", "valfard", "SoU", 50),
        )
    ], validate=False)
    return con


def _mix() -> tuple[float, float]:
    comp = config.scoring()["A_agerande"]["components"]
    return float(comp["a1_budgetprioritering"]), float(comp["a2_lagstiftningsprioritering"])


def _med_mix(monkeypatch: pytest.MonkeyPatch, w_a1: float, w_a2: float) -> None:
    """Lägger blandningen på PRODUKTIONENS väg (ADR 0015 godkännandetest regel 4).

    `config.scoring()` är @cache-dekorerad, så att skriva in talet i den cachade dicten vore att
    ändra configen för hela processen och inte att pröva vägen pipen går. Loadern byts i stället
    ut, precis som robustness.build_matrix gör i känslighetsanalysen.
    """
    sc = copy.deepcopy(_SCORING)
    sc["A_agerande"]["components"]["a1_budgetprioritering"] = w_a1
    sc["A_agerande"]["components"]["a2_lagstiftningsprioritering"] = w_a2
    monkeypatch.setattr(config, "scoring", lambda: sc)


def _bygg(con: object, monkeypatch: pytest.MonkeyPatch, w_a1: float, w_a2: float,
          budget_cfg: dict | None = None) -> dict:
    _med_mix(monkeypatch, w_a1, w_a2)
    return scorerun.build(con, budget_cfg=budget_cfg)["scores"]["scores"]


def _a(scores: dict) -> dict[tuple[str, str], float]:
    return {(p, c): float(cell["components"]["A"])
            for p, cats in scores.items() for c, cell in cats.items()}


def _flaggor(scores: dict) -> set[str]:
    return {f for cats in scores.values() for cell in cats.values() for f in cell["flags"]}


def _bygg_utan_a1(con: object, monkeypatch: pytest.MonkeyPatch, w_a1: float, w_a2: float) -> dict:
    """Bygger med villkorsklausulen fälld, alltså A_a2_only i varje cell.

    Fönsterprovet i ADR 0007 punkt 1 gäller täljarens år, så förankringen får följa med ned till
    det korta fönstret. Här prövas punkt 4, och bytet gäller bara den här byggningen.
    """
    kort = copy.deepcopy(config.budget_ramar())
    kort["budget_years"] = {y: b for y, b in kort["budget_years"].items() if y in _KORT_FONSTER}
    original = anchor.a1_years
    anchor.a1_years = lambda cfg=None: list(_KORT_FONSTER)
    try:
        return _bygg(con, monkeypatch, w_a1, w_a2, budget_cfg=kort)
    finally:
        anchor.a1_years = original


# --- 1. Configen bär talet, och ingenting annat gör det ------------------------------------

def test_configen_bar_lika_vikt_i_varje_kanal() -> None:
    """ADR 0015 punkt 1. Blandningen är härledd, och den står på ett enda ställe."""
    assert _mix() == (0.5, 0.5)


# --- 2. Mutationen: A följer configen, i båda grindlägena ----------------------------------

def test_a_foljer_blandningen_nar_a1_star(monkeypatch: pytest.MonkeyPatch) -> None:
    """Godkännandetest regel 2 och 4. Tre viktpar, och A ska följa vart och ett.

    Kanalernas egna betyg hämtas ur ytterlägena 1/0 och 0/1. Nollkontrollen strax under kräver
    att de två skiljer sig: vore de lika skulle vilken blandning som helst ge samma tal, och
    provet kunde inte se skillnad på en läst vikt och en inskriven.
    """
    con = _seed()
    produktion = _mix()
    try:
        bara_a1 = _a(_bygg(con, monkeypatch, 1.0, 0.0))
        bara_a2 = _a(_bygg(con, monkeypatch, 0.0, 1.0))
        skilda = [k for k in bara_a1 if abs(bara_a1[k] - bara_a2[k]) > 0.01]
        assert len(skilda) > len(bara_a1) / 2, "kanalerna ger samma tal: provet biter inte"

        for w_a1, w_a2 in (produktion, *_MUTATIONER):
            scores = _bygg(con, monkeypatch, w_a1, w_a2)
            assert "A_a1_active" in _flaggor(scores)
            assert "A_a2_only" not in _flaggor(scores)
            for nyckel, varde in _a(scores).items():
                vantat = w_a1 * bara_a1[nyckel] + w_a2 * bara_a2[nyckel]
                assert varde == pytest.approx(vantat, abs=0.0015), f"{nyckel} vid {w_a1}/{w_a2}"
    finally:
        con.close()


def test_a_ar_a2_ensam_och_tackningen_foljer_blandningen_nar_grinden_stanger(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Godkännandetest regel 3 och 5. Faller a1 ur grinden bär a2 hela A, och cellens täckning
    blir a2:s vikt.

    Betyget ska då stå still hur blandningen än ser ut, medan täckningen ska röra sig med den
    (ADR 0008 punkt 3, ADR 0015 punkt 6). Vägen är vilande i dag, eftersom A_a1_active står i
    alla 56 celler, men otestad vore den fel den dag grinden stänger.
    """
    con = _seed()
    produktion = _mix()
    vikt_a = float(_SCORING["subscore_weights"]["A"])
    try:
        a2_ensam = _a(_bygg(con, monkeypatch, 0.0, 1.0))
        vantade_tapp = []
        for w_a1, w_a2 in (produktion, *_MUTATIONER):
            med_a1 = _bygg(con, monkeypatch, w_a1, w_a2)
            utan_a1 = _bygg_utan_a1(con, monkeypatch, w_a1, w_a2)
            assert "A_a2_only" in _flaggor(utan_a1)
            assert "A_a1_active" not in _flaggor(utan_a1)

            for nyckel, varde in _a(utan_a1).items():
                assert varde == pytest.approx(a2_ensam[nyckel], abs=0.0015), nyckel

            # Täckningen publiceras med tre decimaler, så två avrundade tal kan missa med en
            # tusendel åt vardera hållet. Det väntade tappet härleds ur configen, aldrig skrivet.
            for p, cats in utan_a1.items():
                for c, cell in cats.items():
                    tapp = med_a1[p][c]["coverage"] - cell["coverage"]
                    assert tapp == pytest.approx(vikt_a * w_a1, abs=0.0011), f"{p}/{c}"
            vantade_tapp.append(round(vikt_a * w_a1, 6))
        # Tre skilda tapp: täckningen FÖLJER blandningen och står inte still under den.
        assert len(set(vantade_tapp)) == len(vantade_tapp), vantade_tapp
    finally:
        con.close()


# --- 3. Ingen ordning mellan kanalerna, varken i koden eller i analysen ---------------------

def test_analysen_drar_bada_ordningarna_mellan_kanalerna() -> None:
    """Godkännandetest regel 7, vänd rätt.

    Det gamla provet hävdade att a1 väger mer, och ADR 0015 punkt 2 fällde påståendet. Reglaget
    ska därför ligga omkring jämnhöjd och pröva båda ordningarna, aldrig bara den ena.
    """
    src = next(s for s in robustness.SOURCES if s.name == "A_component_mix")
    assert src.spec[0] < 0.5 < src.spec[1], src.spec
    rng = random.Random(robustness.SEED)
    dragna = [robustness.draw(rng)["A_component_mix"] for _ in range(500)]
    assert any(v > 0.5 for v in dragna), "ingen dragning ger a1 mer än a2"
    assert any(v < 0.5 for v in dragna), "ingen dragning ger a2 mer än a1"
