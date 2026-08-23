"""ADR 0008: cellens TÄCKNING, alltså hur stor del av betyget som vilar på mätt underlag.

Ett REGELTEST. Inget tal om hur hög täckningen blev står här (ADR 0008 godkännandetest
punkt 6), bara reglerna: vikterna, nämnaren och vad en ej tillämplig D gör.

Täckningen är inte samma sak som säkerheten. Bandet säger hur säkert det mätta är;
täckningen säger hur stor del som är mätt. De två hålls isär (ADR 0008 punkt 1).
"""

from __future__ import annotations

import json
import re

import pytest

from pipeline import DIST_DIR, ROOT, config, score, scorerun, warehouse
from pipeline.sources import government

# Flaggan B_coverage/D_coverage avrundar den täckta vikten till en decimal, så (a, b, d)
# läst tillbaka ur den kan skilja sig från den oavrundade i tredje decimalen.
_FLAGGTOLERANS = 0.002


def _weights() -> dict[str, float]:
    return config.scoring()["subscore_weights"]


def _a_weights() -> tuple[float, float]:
    """A:s blandning 0,6 a1 + 0,4 a2. Talet 40 i ADR 0008 punkt 3 ÄRVER den (ADR 0008 följder)."""
    comp = config.scoring()["A_agerande"]["components"]
    return float(comp["a1_budgetprioritering"]), float(comp["a2_lagstiftningsprioritering"])


def _denominators() -> dict[str, float]:
    """Kategorins egen täckningsnämnare, alltså den B och D delar (ADR 0008 punkt 5)."""
    sub = scorerun._submeasure_weights()
    nontarget = scorerun._non_target_submeasures()
    return {c: sum(sub[c][s] for s in nontarget[c]) for c in config.category_ids()}


def _d_flag_emitted() -> bool:
    """D_coverage-flaggan skrivs bara när D-breddskrympningen är på (scorerun.build).

    Utan flaggan går d inte att läsa tillbaka ur utdatan, och efterräkningen nedan skulle
    falla på FLAGGAN och skylla på formeln. Läget avgör alltså om testet kan köras, aldrig
    vad det förväntar sig.
    """
    return bool(config.scoring()["D_resultat"].get("coverage_shrink", False))


def _parts_from_flags(flags: list[str], w_a1: float, w_a2: float) -> tuple[float, float, float]:
    """Läser tillbaka (a, b, d) ur cellens flaggor, som bär samma tal som täckningen räknar på.

    Flaggorna finns kvar i scores.json. Det är bara flaggKOLUMNEN i frontend som slutar
    visa dem (ADR 0008 punkt 9), så utdatan går fortfarande att räkna efter.
    """
    a = w_a1 + w_a2 if "A_a1_active" in flags else w_a2
    b = d = 0.0
    for f in flags:
        m = re.fullmatch(r"(B|D)_coverage_([\d.]+)/([\d.]+)", f)
        if not m:
            continue
        tackt, total = float(m.group(2)), float(m.group(3))
        if m.group(1) == "B":
            b = tackt / total
        else:
            d = tackt / total
    return a, b, d


# --- regeln: vikterna (ADR 0008 punkt 5) ---------------------------------------


def test_tackningen_vager_med_delpoangvikterna() -> None:
    """Varje del bidrar med exakt sin ADR 0002-vikt, aldrig med ett ovägt medel."""
    w = _weights()
    assert score.cell_coverage(1.0, 0.0, 0.0) == pytest.approx(w["A"])
    assert score.cell_coverage(0.0, 1.0, 0.0) == pytest.approx(w["B"])
    assert score.cell_coverage(0.0, 0.0, 1.0) == pytest.approx(w["D"])


def test_full_tackning_ar_ett_och_tom_tackning_ar_noll() -> None:
    """De tre summerar till 1,00 eftersom C väger 0, så ingen omnormalisering behövs."""
    assert score.cell_coverage(1.0, 1.0, 1.0) == pytest.approx(1.0)
    assert score.cell_coverage(0.0, 0.0, 0.0) == pytest.approx(0.0)


def test_c_raknas_aldrig() -> None:
    """C har ingen täckningsstorhet: den väger 0 och ingår inte i betyget (ADR 0008 punkt 2).

    Grinden ligger här och inte i cell_coverage, eftersom det är den COMMITTADE configen som
    måste hålla. Får C en vikt slutar täckningen vara en andel av betyget, och då är formeln
    fel. Talet 1,00 för en fullt mätt cell vilar på den här raden.
    """
    assert _weights()["C"] == 0
    assert sum(_weights()[k] for k in score.COVERAGE_SUBSCORES) == pytest.approx(1.0)


def test_tackning_utanfor_intervallet_hard_failar() -> None:
    """En andel utanför [0,1] är ett räknefel uppströms och får aldrig passera tyst."""
    with pytest.raises(ValueError):
        score.cell_coverage(1.5, 0.0, 0.0)
    with pytest.raises(ValueError):
        score.cell_coverage(0.0, -0.1, 0.0)


# --- regeln: nämnaren (ADR 0008 punkt 5) ---------------------------------------


def test_namnaren_ar_kategorins_egen() -> None:
    """B och D räknar båda mot kategorins samlade undermåttsvikt: ekonomi 73, övriga 100."""
    den = _denominators()
    assert den["ekonomi"] == 73
    ovriga = {c: v for c, v in den.items() if c != "ekonomi"}
    assert set(ovriga.values()) == {100}


# --- regeln: ej tillämplig D (ADR 0008 punkt 4) --------------------------------


def test_ej_tillamplig_d_faller_aldrig_ur_namnaren() -> None:
    """d = 0 sänker täckningen. Ett test som klarar sig genom att utelämna D ur nämnaren faller
    här: renormalisering över A och B skulle ge 1,00 för en cell som i själva verket är 0,80."""
    w = _weights()
    utan_d = score.cell_coverage(1.0, 1.0, 0.0)
    assert utan_d == pytest.approx(w["A"] + w["B"])
    renormaliserad = (w["A"] * 1.0 + w["B"] * 1.0) / (w["A"] + w["B"])
    assert utan_d < renormaliserad


def _seed_con():
    """Warehouse UTAN observationer: varje cell blir D_not_applicable. Kör :memory:,
    aldrig data/warehouse.duckdb."""
    con = warehouse.connect(":memory:")
    warehouse.upsert(con, "responsibility", government.build_national_responsibility())
    return con


def test_pipen_ger_ej_tillamplig_d_noll_tackning_med_orord_namnare() -> None:
    """Hela pipen, inte bara formeln: när D är ej tillämplig i varje cell ska täckningen bli
    A- och B-delen ENSAM, aldrig samma tal uppblåst över en krympt nämnare."""
    con = _seed_con()
    sc = scorerun.build(con)["scores"]["scores"]
    con.close()
    w = _weights()
    w_a1, w_a2 = _a_weights()
    den = _denominators()
    for p, cats in sc.items():
        for c, cell in cats.items():
            flaggor = cell["flags"]
            assert "D_not_applicable" in flaggor, f"{p}/{c} har D-underlag i en tom warehouse"
            a, b, d = _parts_from_flags(flaggor, w_a1, w_a2)
            assert d == 0.0
            vantad = w["A"] * a + w["B"] * b
            assert cell["coverage"] == pytest.approx(vantad, abs=_FLAGGTOLERANS), f"{p}/{c}"
            # Nämnaren är kategorins egen, inte en som krympt för att D saknas.
            for f in flaggor:
                m = re.fullmatch(r"B_coverage_[\d.]+/([\d.]+)", f)
                if m:
                    assert float(m.group(1)) == den[c], f"{p}/{c}"
            # Renormalisering över A och B skulle ge ett HÖGRE tal. Den grinden ska bita.
            if vantad > 0:
                assert cell["coverage"] < vantad / (w["A"] + w["B"]), f"{p}/{c}"


# --- betyget står still (ADR 0008 punkt 7 + godkännandetest punkt 1) -----------


def test_tackningen_ror_aldrig_betyget() -> None:
    """Täckningen läggs till cellen, den räknas aldrig in i den. score, ci och components
    är identiska med och utan fältet."""
    komponenter = {"A": 4.0, "B": 3.0, "C": 2.0, "D": 1.0}
    cell = score.category_score_from_components(komponenter, flags=[])
    fore = json.dumps({k: cell[k] for k in ("score", "ci", "components")}, sort_keys=True)
    cell["coverage"] = score.cell_coverage(1.0, 0.5, 0.25)
    efter = json.dumps({k: cell[k] for k in ("score", "ci", "components")}, sort_keys=True)
    assert fore == efter


@pytest.mark.skipif(
    not (DIST_DIR / "scores.json").exists(), reason="dist saknas; kör pipeline.scorerun"
)
def test_varje_cell_i_dist_bar_talet_och_det_stammer_mot_flaggorna() -> None:
    """Den byggda artefakten räknas efter mot sina egna flaggor, cell för cell."""
    if not _d_flag_emitted():
        pytest.skip("D_coverage-flaggan skrivs inte i det här läget; d går inte att läsa tillbaka")
    data = json.loads((DIST_DIR / "scores.json").read_text(encoding="utf-8"))
    w = _weights()
    w_a1, w_a2 = _a_weights()
    for p, cats in data["scores"].items():
        for c, cell in cats.items():
            assert "coverage" in cell, f"{p}/{c} saknar täckning"
            a, b, d = _parts_from_flags(cell["flags"], w_a1, w_a2)
            vantad = w["A"] * a + w["B"] * b + w["D"] * d
            assert cell["coverage"] == pytest.approx(vantad, abs=_FLAGGTOLERANS), f"{p}/{c}"


@pytest.mark.skipif(
    not (DIST_DIR / "scores.json").exists(), reason="dist saknas; kör pipeline.scorerun"
)
def test_betyget_ar_fortfarande_bara_en_funktion_av_delpoangen() -> None:
    """Täckningen har ingen verkan på betyget (ADR 0008 punkt 7): score går fortfarande att
    räkna fram ur components ensamt.

    components skrivs avrundade till tre decimaler i utdatan medan score räknas på de
    oavrundade, så efterräkningen får samma tolerans som avrundningen kan flytta talet.
    """
    data = json.loads((DIST_DIR / "scores.json").read_text(encoding="utf-8"))
    vikter = _weights()
    for p, cats in data["scores"].items():
        for c, cell in cats.items():
            raknat = score.weighted_category_score(cell["components"], vikter)
            assert cell["score"] == pytest.approx(raknat, abs=0.002), f"{p}/{c}"


# --- frontend: talet ersätter flaggorna (ADR 0008 punkt 9) ---------------------
#
# Beteendet prövas i web/tests/score.test.mjs (visibleFlags/fmtCoverage) och i
# web/tests/e2e.spec.mjs mot den renderade sidan. CI kör bara pytest, så grindarna nedan
# håller anropsstället kvar. De speglar test_config.test_metodrutan_visar_samma_vikter.


def _web(name: str) -> str:
    return (ROOT / "web" / name).read_text(encoding="utf-8")


def test_detaljtabellen_har_en_egen_tackningskolumn() -> None:
    app_js = _web("app.js")
    assert "Täckning</th>" in app_js, "detaljtabellen saknar täckningskolumn"
    assert "fmtCoverage(cs.coverage)" in app_js, (
        "täckningen läses inte ur cellen. Frontend får aldrig räkna A/B/C/D-logik själv "
        "(ADR 0008 punkt 8)"
    )


def test_flaggkolumnen_gar_genom_filtret() -> None:
    assert "visibleFlags(cs.flags)" in _web("app.js"), (
        "flaggkolumnen renderar råa flaggor igen; täckningsflaggorna slipper då tillbaka"
    )
    format_js = _web("format.js")
    for flagga in ("A_a1_active", "A_a2_only", "B_coverage_", "D_coverage_"):
        assert flagga in format_js, f"{flagga} saknas i täckningsfiltret"
