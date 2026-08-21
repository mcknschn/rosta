"""Biljett #20 / ADR 0003: skiljbarhet mätt som ordningens stabilitet.

Två saker låses här. Först de två configreglagen som dragningen behöver och som är
byte-identiska med dagens betyg i sitt defaultläge (B:s krympning på/av, A:s normalisering).
Sedan själva analysen: seed, dragningsantal, spannen och att analysen DRAR
`numeric.effect_strength` men aldrig ÄNDRAR den.

Alla warehouse-tester kör mot `:memory:` — aldrig mot data/warehouse.duckdb.
"""

from __future__ import annotations

import copy
import json
import random
import re
from pathlib import Path

import pytest

from pipeline import CONFIG_DIR, DIST_DIR, config, robustness, schema, scorerun, warehouse
from pipeline.sources import government

WEB_DIR = Path(__file__).resolve().parent.parent / "web"


def _seed_con():
    con = warehouse.connect(":memory:")
    warehouse.upsert(con, "responsibility", government.build_national_responsibility())
    return con


def _obs(indicator: str, submeasure: str, vals: dict[int, float]) -> list[dict]:
    return [
        {"id": f"obs:test:{indicator}:{y}", "category": "ekonomi", "submeasure": submeasure,
         "indicator": indicator, "period": str(y), "value": v, "unit": "index",
         "geography": "Riket", "source_ref": f"test:{y}"}
        for y, v in vals.items()
    ]


# Tre ekonomiserier över hela fönstret, så att D blir UPPMÄTT för alla partier med maktandel
# och täckningen når 58/73 = 0,795. Det är över D:s täckningströskel, så tunn bredd sänker inte
# säkerheten och tunt ansvarsunderlag går att pröva för sig. Utan uppmätt D vore D:s trösklar
# inerta och testerna nedan skulle inte pröva någonting.
_ARBETSLOSHET = {2014: 8.0, 2015: 7.5, 2016: 7.0, 2017: 6.7, 2018: 6.5, 2019: 6.4,
                 2020: 6.2, 2021: 6.0, 2022: 6.1, 2023: 6.3, 2024: 6.6, 2025: 6.4}
_BNP = {2021: 100.0, 2022: 102.0, 2023: 104.0, 2024: 106.0, 2025: 108.0}
_REALLONER = {2019: 100.0, 2020: 101.0, 2021: 101.5, 2022: 99.0, 2023: 98.0,
              2024: 100.0, 2025: 101.0}


def _seed_con_with_d():
    con = _seed_con()
    warehouse.upsert(
        con, "observations",
        _obs("arbetsloshet", "sysselsattning_arbetsloshet", _ARBETSLOSHET)
        + _obs("bnp_per_capita", "bnp_produktivitet", _BNP)
        + _obs("realloner", "realloner_hushall", _REALLONER),
    )
    return con


def _patch_scoring(monkeypatch: pytest.MonkeyPatch, mutate) -> dict:
    sc = copy.deepcopy(config.scoring())
    mutate(sc)
    monkeypatch.setattr(config, "scoring", lambda: sc)
    return sc


# --- reglage 1: B:s krympning på eller av (ADR 0003 punkt 5, scenario 3) ---------------


def test_b_coverage_shrink_default_ar_pa_och_byte_identisk(monkeypatch: pytest.MonkeyPatch) -> None:
    """Committad config krymper B. Explicit true ger EXAKT samma utdata som defaulten."""
    assert config.scoring()["B_evidens"]["coverage_shrink"] is True
    con = _seed_con()
    base = scorerun.build(con)["scores"]["scores"]
    _patch_scoring(monkeypatch, lambda sc: sc["B_evidens"].__setitem__("coverage_shrink", True))
    assert scorerun.build(con)["scores"]["scores"] == base
    con.close()


def test_b_coverage_shrink_av_ger_okrympt_b(monkeypatch: pytest.MonkeyPatch) -> None:
    """Av -> B = B_raw. Krympningen drar mot 2,5, så avstängd flyttar B bort från mitten.

    Täckningsflaggan står kvar: den beskriver täckningen och inte krympningen.
    """
    con = _seed_con()
    on = scorerun.build(con)["scores"]["scores"]
    _patch_scoring(monkeypatch, lambda sc: sc["B_evidens"].__setitem__("coverage_shrink", False))
    off = scorerun.build(con)["scores"]["scores"]
    cell_on = on["C"]["integration"]["components"]["B"]
    cell_off = off["C"]["integration"]["components"]["B"]
    assert cell_on == pytest.approx(3.475, abs=1e-3)   # 2,5 + (4,00 - 2,5) * 0,65
    assert cell_off == pytest.approx(4.0, abs=1e-3)    # B_raw, okrympt
    assert "B_coverage_65/100" in off["C"]["integration"]["flags"]
    con.close()


# --- reglage 2: A:s normalisering (ADR 0003 punkt 5) ----------------------------------


def test_a_normalisering_default_ar_rank_och_byte_identisk(monkeypatch: pytest.MonkeyPatch) -> None:
    """Configen deklarerar rank för A. Koden läser den nu, och utdatan är oförändrad."""
    assert config.scoring()["normalization"]["per_subscore"]["A"] == "rank"
    con = _seed_con()
    base = scorerun.build(con)["scores"]["scores"]
    _patch_scoring(monkeypatch, lambda sc: sc["normalization"]["per_subscore"].__setitem__("A", "rank"))
    assert scorerun.build(con)["scores"]["scores"] == base
    con.close()


def test_a_normalisering_minmax_flyttar_a(monkeypatch: pytest.MonkeyPatch) -> None:
    """minmax är det andra byggda alternativet (score.normalize) och ger andra A-tal."""
    con = _seed_con()
    rank = scorerun.build(con)["scores"]["scores"]
    _patch_scoring(monkeypatch, lambda sc: sc["normalization"]["per_subscore"].__setitem__("A", "minmax"))
    minmax = scorerun.build(con)["scores"]["scores"]
    a_rank = {p: rank[p]["ekonomi"]["components"]["A"] for p in rank}
    a_minmax = {p: minmax[p]["ekonomi"]["components"]["A"] for p in minmax}
    assert a_rank != a_minmax
    # Fixturen saknar party_activity, så a2 är lika för alla och normaliseras till 2,5 i BÅDA
    # lägena. Skillnaden kommer alltså helt ur a1 (budgetramarna, lästa ur config). minmax
    # spänner ut a1 till [0,5] -> A = 0,6*a1 + 0,4*2,5 landar i [1,0 , 4,0].
    assert min(a_minmax.values()) == pytest.approx(1.0)
    assert max(a_minmax.values()) == pytest.approx(4.0)
    con.close()


@pytest.mark.parametrize("bad", ["rang", None])
def test_okand_eller_saknad_a_normalisering_hard_failar(
    monkeypatch: pytest.MonkeyPatch, bad: str | None
) -> None:
    """Felstavat ELLER saknat läge får ALDRIG tyst falla tillbaka på rank.

    En tyst fallback skulle återskapa exakt det fel ADR 0004 punkt 3 fällde: en config som
    beskriver ett beteende koden inte har. Grinden sitter på båda ställena, som coverage_mode.
    """
    def mutate(sc: dict) -> None:
        if bad is None:
            del sc["normalization"]["per_subscore"]["A"]
        else:
            sc["normalization"]["per_subscore"]["A"] = bad

    _patch_scoring(monkeypatch, mutate)
    with pytest.raises(config.ConfigError, match="per_subscore.A"):
        config.validate()
    con = _seed_con()
    with pytest.raises(config.ConfigError, match="per_subscore.A"):
        scorerun.build(con)
    con.close()


# --- analysen: seed, dragningsantal och spann är LÅSTA (biljett #20 punkt 5) -----------


def test_seed_och_dragningsantal_ar_lasta() -> None:
    """En oavsiktlig ändring ska synas som en diff, inte som ett tyst annat resultat."""
    assert robustness.SEED == 20260821
    assert robustness.N_DRAWS == 10_000
    assert robustness.N_DRAWS_SHIPPED == 2_000
    assert robustness.N_INFLUENCE_BINS == 4


def _source(name: str) -> robustness.Source:
    return next(s for s in robustness.SOURCES if s.name == name)


def test_effect_strength_spannet_ar_last() -> None:
    """Spannet låstes i biljetten FÖRE första körningen och rörs inte efter att diffen visats.

    Talen 0,3 / 0,6 / 1,0 behölls i ADR 0004 punkt 4 för att ett nytt val skulle tas med
    kännedom om vilka partier det gynnar. Samma sak gäller ett spann, så marginalen härleds
    ur tabellen själv: 40 procent av det minsta avståndet mellan talen (0,30).
    """
    assert _source("effect_strength.low").spec == (0.18, 0.42)
    assert _source("effect_strength.medium").spec == (0.48, 0.72)
    assert _source("effect_strength.high").spec == (0.88, 1.12)


def test_effect_strength_i_configen_ar_orord() -> None:
    """Analysen DRAR talen, den ÄNDRAR dem inte (ADR 0004 punkt 4, neutralitetsfråga)."""
    assert config.claims()["numeric"]["effect_strength"] == {
        "low": 0.3, "medium": 0.6, "high": 1.0, "unknown": 0.0
    }


def test_max_interval_halfwidth_ar_orord_i_configen() -> None:
    """Att sänka den är uttryckligen förkastat i ADR 0003. Analysen drar den, inget mer."""
    assert config.scoring()["uncertainty"]["max_interval_halfwidth"] == 1.5


def test_dragningen_haller_nivatabellernas_ordning() -> None:
    """låg < medel < hög i VARJE dragning, för både effect_strength och confidence."""
    rng = random.Random(robustness.SEED)
    for _ in range(500):
        v = robustness.draw(rng)
        for table in ("effect_strength", "confidence_numeric"):
            low, med, high = (v[f"{table}.{lvl}"] for lvl in ("low", "medium", "high"))
            assert low < med < high, f"{table}: {low} {med} {high}"


def test_vikterna_dras_ur_adr_0002s_mangd() -> None:
    """B störst, A näst, D minst, C noll, summa 1 (ADR 0003 punkt 6)."""
    rng = random.Random(robustness.SEED)
    for _ in range(500):
        values = robustness.draw(rng)
        a, b, d = values["subscore_weights"]
        assert b > a > d > 0
        assert a + b + d == pytest.approx(1.0)
    sc, _ = robustness.configs_for(values)
    assert sc["subscore_weights"]["C"] == 0.0


def test_alla_kallor_i_adr_0003_punkt_5_dras() -> None:
    """Källistan täcker ADR 0003 punkt 5 plus effect_strength (biljett #20)."""
    names = {s.name for s in robustness.SOURCES}
    assert names == {
        "subscore_weights", "max_interval_halfwidth",
        "confidence_numeric.high", "confidence_numeric.medium", "confidence_numeric.low",
        "default_subscore_certainty.A", "A_normalization",
        "B_coverage_mode", "B_coverage_shrink", "B_thin_coverage_threshold",
        "effect_strength.high", "effect_strength.medium", "effect_strength.low",
        "D_attribution_lag_years", "D_change_dead_zone", "D_min_responsibility",
        "D_thin_basis_threshold", "D_coverage_shrink", "D_thin_coverage_threshold",
        "D_subnational_enabled", "D_region_weighting",
    }


def test_analysen_skriver_aldrig_till_config() -> None:
    """Dragningen ändrar kopior i minnet. config/*.yaml och loaderna står orörda."""
    before_files = {
        p.name: p.read_bytes() for p in (CONFIG_DIR / "claims.yaml", CONFIG_DIR / "scoring.yaml")
    }
    before_claims = copy.deepcopy(config.claims())
    before_scoring = copy.deepcopy(config.scoring())
    rng = random.Random(robustness.SEED)
    for _ in range(25):
        robustness.configs_for(robustness.draw(rng))
    assert config.claims() == before_claims
    assert config.scoring() == before_scoring
    for name, blob in before_files.items():
        assert (CONFIG_DIR / name).read_bytes() == blob


# --- band_only: nollkontrollen som gör källinflytandet läsbart ------------------------


def _build_with(con: object, source: robustness.Source, value: object) -> dict:
    sc = copy.deepcopy(config.scoring())
    cl = copy.deepcopy(config.claims())
    source.apply(value, sc, cl)
    orig_scoring, orig_claims = config.scoring, config.claims
    try:
        config.scoring = lambda: sc
        config.claims = lambda: cl
        return scorerun.build(con)["scores"]["scores"]
    finally:
        config.scoring = orig_scoring
        config.claims = orig_claims


_BAND_ONLY = [s for s in robustness.SOURCES if s.band_only]

# Värden långt utanför det dragna spannet, valda så att flaggan garanterat vänder. De prövar
# att källan NÅR bandet, inte hur brett den drar. Spannen prövas i testet ovanför.
_EXTREMES: dict[str, tuple[object, object]] = {
    "max_interval_halfwidth": (0.1, 5.0),
    "default_subscore_certainty.A": ("high", "low"),
    "B_thin_coverage_threshold": (0.0, 10.0),
    "D_thin_basis_threshold": (0.0, 1e6),
    "D_thin_coverage_threshold": (0.0, 10.0),
}


@pytest.mark.parametrize("source", _BAND_ONLY, ids=lambda s: s.name)
def test_band_only_kallor_ror_aldrig_betyget(source: robustness.Source) -> None:
    """Fem källor når bara osäkerhetsbandet.

    Det är hela ADR 0003:s poäng: bandet är ingen rangordningsstorhet, så en källa som bara rör
    bandet kan inte flytta ett partipar. Testet gör påståendet prövbart i stället för påstått,
    och gör band_only-talen i source_influence läsbara som ett brusgolv.
    """
    con = _seed_con_with_d()   # D måste vara uppmätt, annars är D:s trösklar inerta
    for lo, hi in (source.spec[0], source.spec[-1]), _EXTREMES[source.name]:
        a = _build_with(con, source, lo)
        b = _build_with(con, source, hi)
        scores_a = {(p, c): a[p][c]["score"] for p in a for c in a[p]}
        scores_b = {(p, c): b[p][c]["score"] for p in b for c in b[p]}
        assert scores_a == scores_b, f"{source.name} flyttade ett betyg mellan {lo} och {hi}"
    con.close()


@pytest.mark.parametrize("source", _BAND_ONLY, ids=lambda s: s.name)
def test_band_only_kallor_nar_bandet(source: robustness.Source) -> None:
    """Motsatsen till testet ovan: källan måste faktiskt röra bandet, annars är den ingen källa."""
    lo, hi = _EXTREMES[source.name]
    con = _seed_con_with_d()
    a = _build_with(con, source, lo)
    b = _build_with(con, source, hi)
    con.close()
    cis_a = {(p, c): a[p][c]["ci"] for p in a for c in a[p]}
    cis_b = {(p, c): b[p][c]["ci"] for p in b for c in b[p]}
    assert cis_a != cis_b, f"{source.name} rör varken betyg eller band"


# --- rena funktioner ------------------------------------------------------------------


def test_order_of_matchar_frontendens_tie_break() -> None:
    """Fallande betyg, alfabetisk tie-break — samma regel som web/score.js partyTotals."""
    assert robustness.order_of([3.0, 4.0, 3.0], ["B", "A", "C"]) == ["A", "B", "C"]


def test_pair_shares_raknar_oavgjort_som_ingens_forsprang() -> None:
    matrices = [[[4.0], [3.0]], [[3.0], [4.0]], [[3.0], [3.0]], [[5.0], [1.0]]]
    shares = robustness.pair_shares(matrices, ["S", "M"], [("S", "M")], col=0)
    assert shares == {"S|M": 0.5}          # 2 av 4; oavgjort räknas inte som "före"
    back = robustness.pair_shares(matrices, ["S", "M"], [("M", "S")], col=0)
    assert back == {"M|S": 0.25}
    assert shares["S|M"] + back["M|S"] < 1.0


def test_pair_shares_kraver_antingen_kategori_eller_vikter() -> None:
    with pytest.raises(ValueError, match="col"):
        robustness.pair_shares([[[1.0]]], ["S"], [], col=0, weights=[1.0])
    with pytest.raises(ValueError, match="col"):
        robustness.pair_shares([[[1.0]]], ["S"], [])


# --- end-to-end mot :memory: ----------------------------------------------------------


def test_run_ger_utdata_som_validerar_mot_deploykontraktet() -> None:
    con = _seed_con_with_d()
    out = robustness.run(con, n_draws=6, n_shipped=3, seed=robustness.SEED, progress=False)
    con.close()
    schema.validate("robustness", out)

    parties, cats = out["meta"]["parties"], out["meta"]["categories"]
    assert out["meta"]["seed"] == robustness.SEED
    assert out["meta"]["monte_carlo_error"] > 0
    assert len(out["draws"]["values"]) == 3 * len(parties) * len(cats)
    assert set(out["category_stability"]) == set(cats)
    assert len(out["standard_weight_stability"]) == len(parties) * (len(parties) - 1) // 2
    assert set(out["source_influence"]) == {s.name for s in robustness.SOURCES}


def test_de_sju_scenarierna_och_filtermarkningen() -> None:
    con = _seed_con_with_d()
    out = robustness.run(con, n_draws=2, n_shipped=1, seed=robustness.SEED, progress=False)
    con.close()
    scen = out["scenarios"]
    assert [s["id"] for s in scen] == [1, 2, 3, 4, 5, 6, 7]
    # Scenario 6 och 7 byter vad indexet mäter -> märks som filter (ADR 0003 punkt 9).
    assert [s["kind"] for s in scen] == ["uncertainty"] * 5 + ["filter"] * 2
    assert scen[6]["included_parties"] == robustness.national_responsibility_parties()
    assert "V" not in scen[6]["included_parties"]   # V har ingen maktandel i fönstret
    # Fixturen har bara ekonomiserier, så bara ekonomi når D-täckningströskeln.
    assert scen[5]["included_categories"] == ["ekonomi"]
    for s in scen:
        assert len(s["matrix"]) == len(out["meta"]["parties"])
        assert len(s["matrix"][0]) == len(out["meta"]["categories"])
        assert sorted(s["order"]) == sorted(s["included_parties"])


def test_samma_seed_ger_samma_resultat() -> None:
    con = _seed_con_with_d()
    a = robustness.run(con, n_draws=4, n_shipped=2, seed=123, progress=False)
    b = robustness.run(con, n_draws=4, n_shipped=2, seed=123, progress=False)
    c = robustness.run(con, n_draws=4, n_shipped=2, seed=124, progress=False)
    con.close()
    assert a["draws"] == b["draws"]
    assert a["category_stability"] == b["category_stability"]
    assert c["draws"] != a["draws"]


def test_scenario_2_behaller_viktsumman() -> None:
    """A halveras ska pröva EN sak. Utan omviktningen skulle skalan krympa samtidigt."""
    sc = copy.deepcopy(config.scoring())
    robustness._halve_a(sc)
    w = sc["subscore_weights"]
    assert w["A"] == pytest.approx(0.15)
    assert w["C"] == 0.0
    assert sum(w.values()) == pytest.approx(1.0)
    assert w["B"] / w["D"] == pytest.approx(0.50 / 0.20)   # inbördes förhållande orört


# --- sajten får aldrig ge ett binärt omdöme (ADR 0003 punkt 3) ------------------------


_BINARA_OMDOMEN = re.compile(
    r"robust\w*\s+skil|oskiljbar|går inte att skilja|kan inte skilja|"
    r"säkert särskilj|inte säkert särskilj|statistiskt säkerställ",
    re.IGNORECASE,
)


def test_ingen_binar_dom_om_skiljbarhet_i_web() -> None:
    """Andelen redovisas som den är. Aldrig 'robust skilda', aldrig 'oskiljbara'."""
    files = sorted(WEB_DIR.glob("*.js")) + sorted(WEB_DIR.glob("*.html"))
    assert files, "hittade inga frontendfiler att granska"
    for path in files:
        text = path.read_text(encoding="utf-8")
        hit = _BINARA_OMDOMEN.search(text)
        assert not hit, f"{path.name} ger ett binärt omdöme om skiljbarhet: {hit.group(0)!r}"


def test_metodrutan_pastar_inte_att_spann_avgor_ordningen() -> None:
    """Meningen om omlottgående spann blir fel när bandet inte längre är skiljbarhetstest."""
    text = (WEB_DIR / "app.js").read_text(encoding="utf-8")
    assert "spann omlott" not in text
    assert "metodvarianter" in text, "andelen ska stå i metodrutan i stället"


# --- deploykontraktet för dist/robustness.json ---------------------------------------


@pytest.mark.skipif(
    not (DIST_DIR / "robustness.json").exists(), reason="dist saknas; kör pipeline.robustness"
)
def test_dist_robustness_validerar_och_har_last_seed() -> None:
    data = json.loads((DIST_DIR / "robustness.json").read_text(encoding="utf-8"))
    schema.validate("robustness", data)
    assert data["meta"]["seed"] == robustness.SEED
    assert data["meta"]["n_draws"] == robustness.N_DRAWS
    assert data["meta"]["n_draws_shipped"] == robustness.N_DRAWS_SHIPPED
    assert len(data["scenarios"]) == 7
