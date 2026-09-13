"""ADR 0014: MÄTTAKET, alltså det högsta tal Täckning kan anta i en kategori.

Tio REGELTESTER, ett per punkt i ADR 0014:s godkännandetest. Inget tal om täckningens
nivå, spridning eller rangordning står här (ADR 0006 punkt 7, ADR 0011:s godkännandetest
punkt 6). Regel 5, alltså att betyg och band står still utom i klimat, är en DIFF mot
baslinjen och inte en invariant: den prövas med pipeline.tools.score_diff i slicen, inte
här, eftersom ett test inte kan bära ett före-tillstånd.

Regel 9 är den viktigaste. Den låser det beslut biljetten kom för att fatta: vår tystnad
räknas kvar i krympningens nämnare. Utan den kan en senare omskrivning flytta 77 procent
av krympningen utan att ett enda test faller.

Warehouse körs :memory:, aldrig data/warehouse.duckdb.
"""

from __future__ import annotations

import copy
import json
import re
from pathlib import Path

import pytest

from pipeline import DIST_DIR, ROOT, config, score, scorerun, warehouse
from pipeline.sources import government
from pipeline.tools import coverage_report

CEILING_FIELD = "coverage_ceiling"


def _seed_con():
    """Warehouse UTAN observationer: D blir ej tillämplig i varje cell. :memory:, alltid."""
    con = warehouse.connect(":memory:")
    warehouse.upsert(con, "responsibility", government.build_national_responsibility())
    return con


def _built() -> dict:
    con = _seed_con()
    try:
        return scorerun.build(con)["scores"]
    finally:
        con.close()


def _submeasures() -> list[tuple[str, dict, bool]]:
    """(kategori, undermått, har minst en indikator) för samtliga 35 undermått."""
    out = []
    for cat in config.categories()["categories"]:
        med_ind = {ind["submeasure"] for ind in cat.get("indicators", [])}
        out += [(cat["id"], s, s["id"] in med_ind) for s in cat["submeasures"]]
    return out


# --- regel 1: indikator eller Uteslutningsskäl, aldrig ingetdera ----------------------


def test_varje_undermatt_bar_indikator_eller_uteslutningsskal() -> None:
    """ADR 0014 punkt 5: ADR 0011 punkt 4:s form ett steg upp, med återöppningsvillkor."""
    for cid, sub, har_ind in _submeasures():
        ref = f"{cid}/{sub['id']}"
        har_exc = "exclusion" in sub
        assert har_ind or har_exc, f"{ref} saknar både indikator och Uteslutningsskäl"
        assert not (har_ind and har_exc), f"{ref} bär både indikatorer och Uteslutningsskäl"
        if har_exc:
            assert sub["exclusion"] in config.VALID_EXCLUSIONS, ref
            assert str(sub.get("reopen_if", "")).strip(), f"{ref} saknar återöppningsvillkor"


def test_undermatt_utan_indikator_och_utan_skal_hard_failar(monkeypatch: pytest.MonkeyPatch) -> None:
    """Regeln ska FÄLLA, inte bara beskrivas. Ett tomt undermått utan skäl är ett tyst hål."""
    cats = copy.deepcopy(config.categories())
    klimat = next(c for c in cats["categories"] if c["id"] == "klimat")
    sub = next(s for s in klimat["submeasures"] if s["id"] == "industriell_konkurrenskraft")
    sub.pop("exclusion")
    sub.pop("reopen_if", None)
    monkeypatch.setattr(config, "categories", lambda: cats)
    with pytest.raises(config.ConfigError, match="industriell_konkurrenskraft"):
        config.validate()


def test_uteslutet_undermatt_utan_reopen_if_hard_failar(monkeypatch: pytest.MonkeyPatch) -> None:
    """Uteslutning utan återöppningsvillkor är ett beslut utan väg tillbaka (ADR 0011 punkt 8)."""
    cats = copy.deepcopy(config.categories())
    klimat = next(c for c in cats["categories"] if c["id"] == "klimat")
    sub = next(s for s in klimat["submeasures"] if s["id"] == "industriell_konkurrenskraft")
    sub["reopen_if"] = "   "
    monkeypatch.setattr(config, "categories", lambda: cats)
    with pytest.raises(config.ConfigError, match="reopen_if"):
        config.validate()


def test_undermatt_med_bade_indikator_och_skal_hard_failar(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ett undermått vars indikatorer alla är uteslutna bär INGET eget skäl (ADR 0014 punkt 5).
    Två skäl för samma fall vore ADR 0011 punkt 11:s varning en gång till."""
    cats = copy.deepcopy(config.categories())
    ekonomi = next(c for c in cats["categories"] if c["id"] == "ekonomi")
    sub = next(s for s in ekonomi["submeasures"] if s["id"] == "inflation_prisstabilitet")
    sub["exclusion"] = "giltighetsfel"
    sub["reopen_if"] = "aldrig"
    monkeypatch.setattr(config, "categories", lambda: cats)
    with pytest.raises(config.ConfigError, match="inflation_prisstabilitet"):
        config.validate()


# --- regel 2: uteslutet undermått ur krympningen, 0 täckt i Täckningen ----------------


def test_uteslutet_undermatt_ligger_utanfor_krympningens_namnare() -> None:
    """ADR 0011 punkt 9, tillämpad på undermåttsnivå: skälet är att vi VÄGRAR poängsätta."""
    uteslutna = config.excluded_submeasures()
    assert uteslutna, "fixturen förutsätter minst ett uteslutet undermått"
    den = scorerun._non_excluded_submeasures()
    for (cid, sid), skal in uteslutna.items():
        assert sid not in den[cid], f"{cid}/{sid} ligger kvar i krympningens nämnare"
        assert skal in config.VALID_EXCLUSIONS


def test_uteslutet_undermatt_raknas_noll_takt_i_tackningen(
    monkeypatch: pytest.MonkeyPatch
) -> None:
    """Uteslutningen tar undermåttet ur KRYMPNINGENS nämnare och lämnar TÄCKNINGENS orörd.

    Provet ställer configen mot sig själv: samma kategori med och utan skälet. Krympningens
    nämnare faller med undermåttets vikt, täckningens står kvar på hela kategorianspråket.
    Det är skillnaden mellan att stryka ett hål och att räkna det 0 täckt (ADR 0011 punkt 9),
    och den syns inte på en mängd som byggts genom att filtrera bort undermåttet.
    """
    uteslutna = config.excluded_submeasures()
    assert uteslutna, "fixturen förutsätter minst ett uteslutet undermått"
    vikter = scorerun._submeasure_weights()

    def _krympningens_namnare() -> dict[str, float]:
        return {c: sum(vikter[c][s] for s in ss)
                for c, ss in scorerun._non_excluded_submeasures().items()}

    med_skal = _krympningens_namnare()
    tackningen = scorerun._coverage_denominators()
    assert set(tackningen.values()) == {100}

    cats = copy.deepcopy(config.categories())
    for cid, sid in uteslutna:
        sub = next(s for c in cats["categories"] if c["id"] == cid
                   for s in c["submeasures"] if s["id"] == sid)
        sub.pop("exclusion")
    monkeypatch.setattr(config, "categories", lambda: cats)
    utan_skal = _krympningens_namnare()

    for cid, sid in uteslutna:
        assert vikter[cid][sid] > 0
        assert med_skal[cid] == utan_skal[cid] - vikter[cid][sid], cid
    assert tackningen == scorerun._coverage_denominators()


# --- regel 3: Mättaket räknas i pipen -------------------------------------------------


def test_mattaket_raknas_i_pipen_for_varje_kategori() -> None:
    """Talet står i utdatan och räknas där, aldrig i frontend (ADR 0008 punkt 8)."""
    cats = _built()["categories"]
    assert {c["id"] for c in cats} == set(config.category_ids())
    for c in cats:
        assert CEILING_FIELD in c, f"{c['id']} saknar Mättak"
        assert 0.0 < c[CEILING_FIELD] <= 1.0


def test_mattaket_blandas_med_delpoangvikterna_ur_configen() -> None:
    """ADR 0008 punkt 5:s vikter, lästa ur configen och aldrig inskrivna för hand."""
    res = _built()
    comp = config.scoring()["A_agerande"]["components"]
    w_a1 = float(comp["a1_budgetprioritering"])
    w_a2 = float(comp["a2_lagstiftningsprioritering"])
    sub_w = scorerun._submeasure_weights()
    cov_den = scorerun._coverage_denominators()
    b_cov = scorerun._b_covered_submeasures()
    d_cov = scorerun._d_covered_submeasures()
    for c in res["categories"]:
        cid = c["id"]
        # A:s tak är en kategorikonstant och står i cellens A-flagga (ADR 0008 punkt 3).
        flaggor = next(iter(res["scores"].values()))[cid]["flags"]
        a = w_a1 + w_a2 if "A_a1_active" in flaggor else w_a2
        b = sum(sub_w[cid][s] for s in b_cov[cid]) / cov_den[cid]
        d = sum(sub_w[cid][s] for s in d_cov[cid]) / cov_den[cid]
        assert c[CEILING_FIELD] == pytest.approx(score.cell_coverage(a, b, d), abs=1e-9)


# --- regel 4: uppmätt Täckning överstiger aldrig Mättaket -----------------------------


@pytest.mark.parametrize("mode", ["weighted_submeasure_depth", "policy_type_count"])
def test_uppmatt_tackning_overstiger_aldrig_mattaket(
    mode: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Regeln gäller i BÅDA täckningslägena, inte bara i det committade.

    Legacy-läget policy_type_count körs skarpt: pipeline.robustness drar B_coverage_mode som
    reglage i varje känslighetskörning. Räknas Mättaket på undermåttsvikt medan cellen räknar
    åtgärdstyper är talet inget tak, utan bara ett annat tal på en annan skala.
    """
    sc = copy.deepcopy(config.scoring())
    sc["B_evidens"]["coverage_mode"] = mode
    monkeypatch.setattr(config, "scoring", lambda: sc)
    res = _built()
    tak = {c["id"]: c[CEILING_FIELD] for c in res["categories"]}
    for p, cats in res["scores"].items():
        for c, cell in cats.items():
            assert cell["coverage"] <= tak[c] + 1e-9, f"{p}/{c} över taket i läget {mode}"


@pytest.mark.skipif(
    not (DIST_DIR / "scores.json").exists(), reason="dist saknas; kör pipeline.scorerun"
)
def test_uppmatt_tackning_overstiger_aldrig_mattaket_i_dist() -> None:
    """Samma regel på den byggda artefakten, alltså med hela warehouset bakom sig."""
    data = json.loads((DIST_DIR / "scores.json").read_text(encoding="utf-8"))
    tak = {c["id"]: c[CEILING_FIELD] for c in data["categories"]}
    for p, cats in data["scores"].items():
        for c, cell in cats.items():
            assert cell["coverage"] <= tak[c] + 1e-9, f"{p}/{c} över taket"


# --- regel 6: båda B-flaggorna sänker säkerheten ETT steg -----------------------------


def test_de_tva_b_flaggorna_ar_omsesidigt_uteslutande() -> None:
    """Kategorins tak och partiets egen täckning är skilda besked, och cellen bär ett av dem.

    Taket BINDER partiet: ligger taket under tröskeln ligger varje parti där också, alltså
    säger partiflaggan ingenting i den kategorin. Två flaggor skulle dessutom sänka
    säkerheten två steg och flytta bandet, vilket ADR 0014 punkt 7 förbjuder.
    """
    for p, cats in _built()["scores"].items():
        for c, cell in cats.items():
            bada = {scorerun.B_THIN_CATEGORY, scorerun.B_THIN_PARTY} & set(cell["flags"])
            assert len(bada) <= 1, f"{p}/{c} bär båda B-flaggorna: {sorted(bada)}"


def test_bada_b_flaggorna_sanker_sakerheten_exakt_ett_steg() -> None:
    cl = config.claims()["numeric"]["confidence"]
    for conf_cat, n_claims in ((cl["high"], 99), (cl["medium"], 99), (0.0, 0)):
        utan = scorerun._b_confidence(conf_cat, n_claims, False)
        med = scorerun._b_confidence(conf_cat, n_claims, True)
        assert med == scorerun._step_down_confidence(utan, 1)


def test_tunn_tackning_i_cellen_ger_alltid_exakt_en_av_flaggorna() -> None:
    """Flaggorna PARTITIONERAR tunn täckning: ingen tunn cell står oflaggad, och ingen
    väl täckt cell bär en flagga.

    Cellens eget tal läses ur B_shrink-flaggan, alltså ur utdatan och inte ur samma
    hjälpare som satte flaggan. Utan den jämförelsen kan en tunn cell tappa sin flagga
    utan att något test faller.
    """
    thr = float(config.scoring()["B_evidens"]["thin_coverage_threshold"])
    sub_w = scorerun._submeasure_weights()
    den = scorerun._non_excluded_submeasures()
    b_cov = scorerun._b_covered_submeasures()
    provade = 0
    for p, cats in _built()["scores"].items():
        for c, cell in cats.items():
            flagga = next((f for f in cell["flags"] if f.startswith("B_shrink_")), None)
            if flagga is None:
                assert "B_no_party_evidence" in cell["flags"], f"{p}/{c} saknar B-flaggor"
                continue
            tackt, total = (float(x) for x in flagga.removeprefix("B_shrink_").split("/"))
            tak = sum(sub_w[c][s] for s in b_cov[c]) / sum(sub_w[c][s] for s in den[c])
            vantad = ([scorerun.B_THIN_CATEGORY if tak < thr else scorerun.B_THIN_PARTY]
                      if tackt / total < thr else [])
            tunn = [f for f in cell["flags"]
                    if f in (scorerun.B_THIN_CATEGORY, scorerun.B_THIN_PARTY)]
            assert tunn == vantad, f"{p}/{c}"
            provade += 1
    assert provade >= 40, "för få celler prövade; fixturen bär inte regeln"


# --- regel 7: de gamla flaggnamnen läses inte längre ----------------------------------

# Namnen byggs av delar, så testfilen själv inte är en träff. Config- och reglagenycklarna
# (B_coverage_mode, B_coverage_shrink, D_coverage_shrink, B_thin_coverage_threshold) är
# INTE flaggnamn och står kvar; mönstren undantar dem uttryckligen.
_GAMLA = (
    re.compile("B" + r"_coverage_(?!mode|shrink)"),
    re.compile("D" + r"_coverage_(?!shrink)"),
    re.compile(r"\)" + "_coverage_"),  # regex-stavningen (B|D)_coverage_ i ett test
    re.compile("B" + r"_thin_coverage(?!_threshold)"),
)


def _kallfiler() -> list[Path]:
    ut = []
    for mönster in ("pipeline/**/*.py", "tests/*.py", "web/*.js", "web/tests/*.mjs",
                    "config/*.yaml", "schemas/*.json"):
        ut += [p for p in ROOT.glob(mönster) if p.name != Path(__file__).name]
    return ut


def test_ingen_kod_och_inget_test_laser_de_gamla_flaggnamnen() -> None:
    traffar = []
    for p in _kallfiler():
        text = p.read_text(encoding="utf-8")
        for rx in _GAMLA:
            if rx.search(text):
                traffar.append(f"{p.relative_to(ROOT).as_posix()}: {rx.pattern}")
    assert not traffar, "gamla flaggnamn kvar efter ADR 0014 punkt 8: " + "; ".join(traffar)


# --- regel 8: inget D-tak ligger under D:s tröskel ------------------------------------


def test_inget_d_tak_ligger_under_d_troskeln() -> None:
    """ADR 0014 punkt 7: D delas INTE, eftersom kategoriflaggan skulle ha noll medlemmar.

    Kontrollen är nedskriven i stället för tyst. Försvarets tak ligger på EXAKT tröskeln,
    så villkoret är strikt mindre än. Sjunker något tak under den faller det här testet,
    och då ska delningen prövas igen.
    """
    rep = coverage_report.d_submeasure_breadth()
    thr = float(config.scoring()["D_resultat"]["thin_coverage_threshold"])
    under = [c["id"] for c in rep["categories"] if c["ratio"] < thr]
    assert not under, f"D-tak under tröskeln {thr} — pröva delningen igen: {under}"


# --- regel 9: tomt men EJ uteslutet undermått ligger kvar i krympningens nämnare ------


def test_tomt_men_ej_uteslutet_undermatt_ligger_kvar_i_namnaren() -> None:
    """DEN VIKTIGASTE REGELN (ADR 0014 punkt 2).

    Ett undermått utan kodbar åtgärdstyp är VÅR tystnad, inte partiets, och krympningen
    räknar den rätt: full vikt i nämnaren, noll i täljaren, alltså 2,5 för den delen. Att
    flytta ut den skulle låta betyget göra ett helt kategorianspråk på en delmängd, vilket
    ADR 0008 punkt 4 avvisade en gång.

    Demokrati bär testet: tre av dess fem undermått är tomma utan att vara uteslutna.
    """
    den = scorerun._non_excluded_submeasures()["demokrati"]
    tomma = set(den) - scorerun._b_covered_submeasures()["demokrati"]
    assert len(tomma) >= 3, f"demokratis tomma undermått: {sorted(tomma)}"
    # Tomt är inte uteslutet. Skulle ett tomt undermått få ett skäl vore det inte längre vår
    # tystnad utan en vägran, och 55 procent av demokrati skulle lämna nämnaren.
    uteslutna = config.excluded_submeasures()
    for sid in tomma:
        assert ("demokrati", sid) not in uteslutna, sid
    sub_w = scorerun._submeasure_weights()["demokrati"]
    assert sum(sub_w[s] for s in den) == 100
    assert sum(sub_w[s] for s in tomma) > 0


def test_krympningens_namnare_faller_bara_pa_uteslutning() -> None:
    """Nämnaren rör sig när ett undermått UTESLUTS, aldrig när det bara är tomt.

    Talen är configens, alltså: ekonomi 73 (två undermått vars indikatorer alla är
    uteslutna, ADR 0011), klimat 85 (industriell_konkurrenskraft utesluten, ADR 0014
    punkt 6) och 100 för de fem övriga, som alla bär tomma undermått utan att någon
    av dem lämnar nämnaren.
    """
    sub_w = scorerun._submeasure_weights()
    den = scorerun._non_excluded_submeasures()
    namnare = {c: sum(sub_w[c][s] for s in den[c]) for c in config.category_ids()}
    assert namnare["ekonomi"] == 73
    assert namnare["klimat"] == 85
    ovriga = {c: v for c, v in namnare.items() if c not in ("ekonomi", "klimat")}
    assert set(ovriga.values()) == {100}


# --- regel 10: talet står på categories[], aldrig på cellen ---------------------------


def test_mattaket_star_pa_kategorin_och_aldrig_pa_cellen() -> None:
    """En kategorikonstant, alltså sju tal och inte 56 kopior (ADR 0014 punkt 4)."""
    res = _built()
    for p, cats in res["scores"].items():
        for c, cell in cats.items():
            assert CEILING_FIELD not in cell, f"{p}/{c} bär Mättaket"


def test_metodrutan_laser_mattaket_ur_kategorin() -> None:
    """Frontend ska LÄSA talet, aldrig räkna det (ADR 0008 punkt 8), och rutan ska finnas.

    Grinden speglar tests/test_cell_coverage.py: CI kör bara pytest, så den här raden håller
    anropsstället kvar. Beteendet prövas i web/tests. Utan grinden kan takstycket tyst
    försvinna ur metodrutan, och då är hela ADR 0014 punkt 3 osynlig för läsaren.
    """
    app_js = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
    assert f"c.{CEILING_FIELD}" in app_js, "metodrutan läser inte Mättaket ur kategorin"
    assert "ceilingMethodHTML()" in app_js, "takstycket renderas inte i metodrutan"


def test_schemat_stanger_kategoriobjektet() -> None:
    """additionalProperties: false — annars kan ett fält tyst byta namn och försvinna."""
    schema = json.loads((ROOT / "schemas" / "scores.schema.json").read_text(encoding="utf-8"))
    items = schema["properties"]["categories"]["items"]
    assert items.get("additionalProperties") is False
    assert CEILING_FIELD in items["properties"]
    assert CEILING_FIELD in items["required"]
