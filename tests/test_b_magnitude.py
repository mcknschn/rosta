"""ADR 0004 - B bär storlek och inte bara riktning, med anspråket begränsat av ADR 0018.

Två lås:
  * Formen (pipeline/effects.py). net_support är ett KVALITETSVIKTAT medel av storlekar med
    tecken, net = Σ(q·m) / Σ q där q = evidence_level × confidence och
    m = effect_strength × tecken(riktning). Storleksskalan står i täljaren men inte i
    nämnaren, så formen kan aldrig kollapsa till tecknet. Det är regressionen ADR 0004
    diagnostiserade: den gamla nämnaren Σ|w| gjorde varje enhällig cell till exakt ±1.
  * Säkerheten (pipeline/scorerun.py). B:s grundnivå härleds ur evidensaggregatets
    confidence med min_claims_for_high_confidence, och sänks ett steg vid tunn täckning.
    B kan för första gången nå high.
  * Anspråket (metodrutan). ADR 0018 punkt 3 tog anspråket om den väntade förbättringens
    storlek ifrån B, eftersom Σ q i nämnaren gör talet till ett medelvärde. Formen står
    orörd tills biljett #50 avgör nämnaren, så texten är det enda som rättas här, och
    den låses nedan.
"""

from __future__ import annotations

import copy
from collections import Counter

import pytest

from pipeline import config, effects, positions, scorerun, warehouse
from pipeline.sources import government


def _k() -> float:
    """Budgeten K = R x max(effect_strength), räknad ur configen (ADR 0019 beslut 4)."""
    cl = config.claims()
    return (
        int(config.scoring()["B_evidens"]["saturation_action_types"])
        * max(cl["numeric"]["effect_strength"].values())
    )


def _claim(
    cid: str, direction: str, strength: str, level: str, conf: str, policy: str = "typ_a"
) -> dict:
    return {
        "id": cid, "type": "evidence_effect", "party": "M", "category": "ekonomi",
        "indicator": "arbetsloshet", "direction": direction, "policy_type": policy,
        "evidence_level": level, "effect_strength": strength, "confidence": conf,
    }


# --- formen -------------------------------------------------------------------------


@pytest.mark.parametrize(("strength", "expected"), [("low", 0.3), ("medium", 0.6), ("high", 1.0)])
def test_ensamt_claim_ger_sin_egen_effektstyrka(strength: str, expected: float) -> None:
    """Regressionen ADR 0004 handlar om, nu på ÅTGÄRDSTYPENS nivå (ADR 0019 beslut 1).

    Ett ensamt claim ger x_t = m, alltså sin egen storlek med tecken och aldrig tecknet. Det är
    den egenskapen som håller ADR 0004 beslut 2 sant: q är relativ poolningsvikt och aldrig
    amplitudfaktor. Cellens net är sedan x_t / K, eftersom summan går mot en fast budget."""
    eff = effects.aggregate_effects(
        [_claim("c1", "positive", strength, "authority_evaluation", "medium")]
    )
    assert eff[0]["net_support"] == pytest.approx(expected / _k(), abs=1e-4)


def test_ensamt_negativt_claim_behaller_tecknet() -> None:
    eff = effects.aggregate_effects([_claim("c1", "negative", "low", "systematic_review", "high")])
    assert eff[0]["net_support"] == pytest.approx(-0.3 / _k(), abs=1e-4)


def test_enhallig_cell_kollapsar_inte_till_taket() -> None:
    """Två claims på SAMMA åtgärdstyp åt samma håll: poolningen ger medelstorleken, inte taket."""
    eff = effects.aggregate_effects([
        _claim("c1", "positive", "low", "authority_evaluation", "medium"),   # q=0.48, m=0.3
        _claim("c2", "positive", "medium", "single_study_report", "low"),    # q=0.15, m=0.6
    ])
    net = eff[0]["net_support"]
    x_t = (0.48 * 0.3 + 0.15 * 0.6) / (0.48 + 0.15)
    assert net == pytest.approx(x_t / _k(), abs=1e-4)
    assert 0.3 < x_t < 0.6


def test_evidensgraderingen_nar_betyget() -> None:
    """Diagnos punkt 2: graderingen tog ut sig själv i normaliseraren. Nu ska en starkare
    källa väga tyngre - samma två storlekar, bytta kvaliteter ger olika net."""
    stark_bar_stor_storlek = effects.aggregate_effects([
        _claim("c1", "positive", "high", "systematic_review", "high"),
        _claim("c2", "positive", "low", "expert_opinion", "low"),
    ])[0]["net_support"]
    svag_bar_stor_storlek = effects.aggregate_effects([
        _claim("c1", "positive", "high", "expert_opinion", "low"),
        _claim("c2", "positive", "low", "systematic_review", "high"),
    ])[0]["net_support"]
    assert stark_bar_stor_storlek > svag_bar_stor_storlek


def test_mixed_drar_mot_neutral_men_behaller_sin_vikt() -> None:
    """ADR 0004 punkt 3: mixed/unclear ger m = 0 men behåller sitt q - en källa som säger
    att effekten är oklar drar cellen mot neutral i stället för att falla ur nämnaren."""
    ensam = effects.aggregate_effects(
        [_claim("c1", "positive", "high", "authority_evaluation", "high")]
    )[0]["net_support"]
    med_oklar = effects.aggregate_effects([
        _claim("c1", "positive", "high", "authority_evaluation", "high"),   # q=0.68, m=1.0
        _claim("c2", "mixed", "medium", "authority_evaluation", "high"),    # q=0.68, m=0
    ])[0]["net_support"]
    assert ensam == pytest.approx(1.0 / _k(), abs=1e-4)
    assert med_oklar == pytest.approx(0.5 / _k(), abs=1e-4)


def test_unknown_effect_strength_ger_ingen_storlek() -> None:
    eff = effects.aggregate_effects(
        [_claim("c1", "positive", "unknown", "authority_evaluation", "high")]
    )
    assert eff[0]["net_support"] == pytest.approx(0.0, abs=1e-4)


def test_unknown_effect_strength_drar_mot_neutral_som_mixed() -> None:
    """unknown har ingen storlek att bidra med, men lämnar inte nämnaren: källan drar cellen
    mot neutral i stället för att försvinna. Före ADR 0004 föll den ur båda leden."""
    med_unknown = effects.aggregate_effects([
        _claim("c1", "positive", "high", "authority_evaluation", "high"),      # q=0.68, m=1.0
        _claim("c2", "positive", "unknown", "authority_evaluation", "high"),   # q=0.68, m=0
    ])[0]["net_support"]
    assert med_unknown == pytest.approx(0.5 / _k(), abs=1e-4)


def test_claims_delas_pa_tecknet_som_forut() -> None:
    eff = effects.aggregate_effects([
        _claim("stod", "positive", "low", "authority_evaluation", "medium"),
        _claim("emot", "negative", "high", "authority_evaluation", "medium"),
    ])[0]
    assert eff["supporting_claims"] == ["stod"]
    assert eff["contradicting_claims"] == ["emot"]


def test_net_support_stannar_i_intervallet() -> None:
    """x_t når som mest 1.0 och net klipps mot budgeten, så net lämnar aldrig [-1, 1]."""
    for strength in ("low", "medium", "high"):
        for direction in ("positive", "negative"):
            net = effects.aggregate_effects(
                [_claim("c1", direction, strength, "systematic_review", "high")]
            )[0]["net_support"]
            assert -1.0 <= net <= 1.0


# --- säkerheten ----------------------------------------------------------------------


def _num() -> dict[str, float]:
    return config.claims()["numeric"]["confidence"]


def _min_claims() -> int:
    return int(config.claims()["aggregation"]["min_claims_for_high_confidence"])


def test_b_confidence_trosklarna_ar_claims_yaml_baklanges() -> None:
    num, mc = _num(), _min_claims()
    assert scorerun._b_confidence(num["high"], mc, False) == "high"
    assert scorerun._b_confidence(num["high"] - 0.01, mc, False) == "medium"
    assert scorerun._b_confidence(num["medium"], mc, False) == "medium"
    assert scorerun._b_confidence(num["medium"] - 0.01, mc, False) == "low"


def test_b_confidence_kraver_min_claims_for_high() -> None:
    """min_claims_for_high_confidence i claims.yaml användes av ingenting (diagnos punkt 3)."""
    num, mc = _num(), _min_claims()
    assert scorerun._b_confidence(num["high"], mc - 1, False) == "medium"


def test_b_confidence_sanks_ett_steg_vid_tunn_tackning() -> None:
    """Evidenssäkerhet och täckningssäkerhet förstärker varandra (ADR 0004 punkt 5)."""
    num, mc = _num(), _min_claims()
    assert scorerun._b_confidence(num["high"], mc, True) == "medium"
    assert scorerun._b_confidence(num["medium"], mc, True) == "low"
    assert scorerun._b_confidence(0.0, mc, True) == "low"


def test_b_kan_na_high(monkeypatch: pytest.MonkeyPatch) -> None:
    """Diagnos punkt 3: ingen B-cell nådde någonsin high. Med en kategori vars kodbara
    åtgärdstyper alla har confidence high, full täckning och minst
    min_claims_for_high_confidence ståndpunkter, ska B nå high."""
    mc = _min_claims()
    led = copy.deepcopy(config.evidence_ledger())
    led["entries"] = [
        e for e in led["entries"] if e["category"] != "klimat" or e["confidence"] == "high"
    ]
    for i in range(mc):
        led["entries"].append({
            "category": "klimat", "indicator": "territoriella_utslapp",
            "policy_type": f"test_hogsaker_{i}", "direction": "positive",
            "evidence_level": "systematic_review", "effect_strength": "medium",
            "confidence": "high", "source": "test",
        })
    pos = copy.deepcopy(config.party_positions())
    pos["entries"] = [
        {"party": "S", "policy_type": e["policy_type"], "stance": "supports", "source": "test"}
        for e in led["entries"] if e["category"] == "klimat"
    ]
    monkeypatch.setattr(config, "evidence_ledger", lambda: led)
    monkeypatch.setattr(config, "party_positions", lambda: pos)

    con = warehouse.connect(":memory:")
    warehouse.upsert(con, "responsibility", government.build_national_responsibility())
    cell = scorerun.build(con)["scores"]["scores"]["S"]["klimat"]
    con.close()
    assert not {scorerun.B_THIN_CATEGORY, scorerun.B_THIN_PARTY} & set(cell["flags"])
    assert cell["confidence"]["B"] == "high"


def test_n_claims_raknas_per_parti_och_kategori(monkeypatch: pytest.MonkeyPatch) -> None:
    """min_claims_for_high_confidence grindar på kategorins ALLA evidence_effect-claims, inte
    på en enskild indikatorcells. En kategori med tre indikatorer som var för sig vilar på ett
    claim ska alltså kunna nå high. Låser vilken storhet grinden mäter."""
    sedda: list[int] = []
    orig = scorerun._b_confidence
    monkeypatch.setattr(
        scorerun, "_b_confidence",
        lambda conf_cat, n, thin: sedda.append(n) or orig(conf_cat, n, thin),
    )
    con = warehouse.connect(":memory:")
    warehouse.upsert(con, "responsibility", government.build_national_responsibility())
    res = scorerun.build(con)["scores"]
    con.close()
    sc = res["scores"]

    per_kategori = Counter(
        (c["party"], c["category"]) for c in positions.build_evidence_effect_claims()
    )
    vantade = [
        per_kategori[(p, c)]
        for p in res["meta"]["parties"] for c in (k["id"] for k in res["categories"])
        if "B_no_party_evidence" not in sc[p][c]["flags"]
    ]
    assert sedda == vantade
    assert max(sedda) > 1  # annars säger testet ingenting om vilken storhet som räknas


def _metodrutan() -> str:
    """Metodrutan ur en ren körning. Warehouse UTAN observationer, `:memory:`, aldrig
    data/warehouse.duckdb."""
    con = warehouse.connect(":memory:")
    warehouse.upsert(con, "responsibility", government.build_national_responsibility())
    text = scorerun.build(con)["scores"]["meta"]["coverage_technical"]
    con.close()
    return text


def test_metodrutan_bar_formen_i_tva_led() -> None:
    """Metodrutan följer med dist/scores.json och är därmed det anspråk som når en granskare
    utanför repot. Varken den gamla medelvärdesformen eller det retirerade anspråket får stå kvar."""
    text = _metodrutan()
    assert "B mäter VÄNTAD STORLEK" not in text
    assert "B mäter GENOMSNITTLIG BELAGD EFFEKTSTYRKA" not in text
    assert "B RÄKNAS I TVÅ LED" in text
    assert "ADR 0019 beslut 1" in text
    assert str(config.scoring()["B_evidens"]["saturation_action_types"]) in text


def test_metodrutan_skriver_ut_garantins_rackvidd() -> None:
    """ADR 0019 beslut 2: monotoniciteten gäller i tre led och inte fler. Utan den gränsen läser
    en granskare ett fall i publicerat B som ett besked om partiet, när det är krympningens
    förstärkning av avvikelsen från neutral."""
    text = _metodrutan()
    assert "GARANTINS RÄCKVIDD" in text
    assert "oförändrat indikatormedlemskap" in text
    assert "KVARSTÅENDE FEL" in text  # upprullningen rättas inte här, och det ska stå


def test_metodrutan_namner_registret_och_sparren() -> None:
    """Två låsningar som annars är osynliga: registret är slutet, och en evidensgodkänd post kan
    ändå sakna jämförelseberättigande. De är skilda uteslutningar och får inte läsas ihop."""
    text = _metodrutan()
    assert "ÅTGÄRDSTYPSREGISTRET" in text
    assert "SKALÄNDRING" in text
    assert "JÄMFÖRELSEBERÄTTIGAD" in text


def test_metodrutan_skiljer_konsensus_fran_partiellt_kodad_ensidighet() -> None:
    """ADR 0018 punkt 5. En post som bara några partier är kodade på skiljer partier åt på
    kodningsflit och inte på hållning, så den får aldrig heta konsensus. En saknad position bär
    inget besked alls och ska stå som okänd."""
    text = _metodrutan()
    assert "KONSENSUS KRÄVER ALLA" in text
    assert "PARTIELLT KODAD ENSIDIGHET" in text
    assert "UTTRYCKLIGEN OKÄND" in text


def test_skilda_atgardstyper_summeras_och_hojer_alltid() -> None:
    """ADR 0019 beslut 1 och 2: skilda ingrepp adderas, och en tillagd typ med q*m > 0 får
    aldrig sänka talet. Det är felet ADR 0018 diagnostiserade, rättat på rätt nivå."""
    en = effects.aggregate_effects(
        [_claim("c1", "positive", "medium", "authority_evaluation", "medium", "typ_a")]
    )[0]["net_support"]
    tva = effects.aggregate_effects([
        _claim("c1", "positive", "medium", "authority_evaluation", "medium", "typ_a"),
        _claim("c2", "positive", "low", "authority_evaluation", "medium", "typ_b"),
    ])[0]["net_support"]
    assert tva > en, "en tillagd åtgärdstyp med belagd positiv effekt måste höja talet"
    assert tva == pytest.approx((0.6 + 0.3) / _k(), abs=1e-4)


def test_negativ_post_kan_aldrig_hoja() -> None:
    """Symmetrin till beslut 2: en post med q*m < 0 sänker alltid eller lämnar talet orört."""
    en = effects.aggregate_effects(
        [_claim("c1", "positive", "high", "authority_evaluation", "medium", "typ_a")]
    )[0]["net_support"]
    med_negativ = effects.aggregate_effects([
        _claim("c1", "positive", "high", "authority_evaluation", "medium", "typ_a"),
        _claim("c2", "negative", "medium", "authority_evaluation", "medium", "typ_b"),
    ])[0]["net_support"]
    assert med_negativ < en


def test_full_skala_kraver_R_skilda_typer() -> None:
    """R = antalet fullt verksamma åtgärdstyper som definierar full skala (ADR 0019 beslut 4).
    Färre än R maximala typer når inte 1,0; R stycken gör det exakt."""
    r = int(config.scoring()["B_evidens"]["saturation_action_types"])
    maxad = [
        _claim(f"c{i}", "positive", "high", "systematic_review", "high", f"typ_{i}")
        for i in range(r)
    ]
    assert effects.aggregate_effects(maxad)[0]["net_support"] == pytest.approx(1.0, abs=1e-9)
    assert effects.aggregate_effects(maxad[:-1])[0]["net_support"] < 1.0


def test_claim_utan_policy_type_hard_failar() -> None:
    """Utan grupperingsnyckel går formen inte att räkna, och en tyst hopslagning av skilda
    ingrepp vore precis det fel som rättas. Hård fail, aldrig en gissning (ADR 0019 beslut 1)."""
    trasig = _claim("c1", "positive", "medium", "authority_evaluation", "medium")
    del trasig["policy_type"]
    with pytest.raises(config.ConfigError, match="policy_type"):
        effects.aggregate_effects([trasig])


# --- invariansproven (ADR 0019 beslut 13) -------------------------------------------


def _net(ledger: list[dict]) -> float:
    pos = [{"party": "M", "policy_type": "typ_a", "stance": "supports", "source": "s"}]
    cl = positions.build_evidence_effect_claims(positions=pos, ledger=ledger)
    return effects.aggregate_effects(cl)[0]["net_support"]


def _post(**over) -> dict:
    bas = {
        "category": "ekonomi", "indicator": "arbetsloshet", "policy_type": "typ_a",
        "direction": "positive", "evidence_level": "authority_evaluation",
        "effect_strength": "medium", "confidence": "medium",
        "source": "Myndigheten, Rapport 1", "source_url": "https://ex.test/rapport-1",
    }
    bas.update(over)
    return bas


def test_invarians_duplicerat_estimand_andrar_ingenting() -> None:
    """Samma utvärdering två gånger väger lika mycket som en gång."""
    assert _net([_post()]) == pytest.approx(_net([_post(), _post()]), abs=1e-9)


def test_invarians_redaktionell_uppdelning_andrar_ingenting() -> None:
    """Samma utvärdering uppdelad i två rader med olika formulering väger lika mycket som en."""
    delad = [_post(), _post(source="Myndigheten, Rapport 1 (del 2)")]
    assert _net([_post()]) == pytest.approx(_net(delad), abs=1e-9)


def test_invarians_bytt_dokumentrepresentation_andrar_ingenting() -> None:
    """Samma utvärdering hämtad som .text respektive .html är samma utvärdering."""
    bytt = [_post(source_url="http://EX.test/rapport-1.html/")]
    assert _net([_post()]) == pytest.approx(_net(bytt), abs=1e-9)


def test_motsagelse_inom_samma_estimand_hard_failar() -> None:
    """Två rader som delar utvärdering och estimand men bär olika storlek är en motsägelse om
    analysenheten, aldrig ett tyst medelvärde."""
    with pytest.raises(config.ConfigError, match="motsägelsefull"):
        _net([_post(), _post(effect_strength="high")])
