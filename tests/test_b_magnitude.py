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


def _claim(cid: str, direction: str, strength: str, level: str, conf: str) -> dict:
    return {
        "id": cid, "type": "evidence_effect", "party": "M", "category": "ekonomi",
        "indicator": "arbetsloshet", "direction": direction,
        "evidence_level": level, "effect_strength": strength, "confidence": conf,
    }


# --- formen -------------------------------------------------------------------------


@pytest.mark.parametrize(("strength", "expected"), [("low", 0.3), ("medium", 0.6), ("high", 1.0)])
def test_ensamt_claim_ger_sin_egen_effektstyrka(strength: str, expected: float) -> None:
    """Regressionen hela ADR 0004 handlar om: ett ensamt claim ska ge sin egen storlek med
    tecken, inte tecknet. 184 av 228 celler har exakt ett claim, och den gamla formen gav
    dem alla ±1 oavsett hur svag evidensen var."""
    eff = effects.aggregate_effects(
        [_claim("c1", "positive", strength, "authority_evaluation", "medium")]
    )
    assert eff[0]["net_support"] == pytest.approx(expected, abs=1e-4)


def test_ensamt_negativt_claim_behaller_tecknet() -> None:
    eff = effects.aggregate_effects([_claim("c1", "negative", "low", "systematic_review", "high")])
    assert eff[0]["net_support"] == pytest.approx(-0.3, abs=1e-4)


def test_enhallig_cell_kollapsar_inte_till_taket() -> None:
    """Två claims åt samma håll, båda svaga: gamla formen gav +1.0, nya ger medelstorleken."""
    eff = effects.aggregate_effects([
        _claim("c1", "positive", "low", "authority_evaluation", "medium"),   # q=0.48, m=0.3
        _claim("c2", "positive", "medium", "single_study_report", "low"),    # q=0.15, m=0.6
    ])
    net = eff[0]["net_support"]
    assert net == pytest.approx((0.48 * 0.3 + 0.15 * 0.6) / (0.48 + 0.15), abs=1e-4)
    assert 0.3 < net < 0.6


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
    assert ensam == pytest.approx(1.0, abs=1e-4)
    assert med_oklar == pytest.approx(0.5, abs=1e-4)


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
    assert med_unknown == pytest.approx(0.5, abs=1e-4)


def test_claims_delas_pa_tecknet_som_forut() -> None:
    eff = effects.aggregate_effects([
        _claim("stod", "positive", "low", "authority_evaluation", "medium"),
        _claim("emot", "negative", "high", "authority_evaluation", "medium"),
    ])[0]
    assert eff["supporting_claims"] == ["stod"]
    assert eff["contradicting_claims"] == ["emot"]


def test_net_support_stannar_i_intervallet() -> None:
    """Storleksskalan når som mest 1.0, så medlet kan aldrig lämna [-1, 1]."""
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


def test_metodrutan_bar_inte_kvar_anspraket_om_vantad_storlek() -> None:
    """ADR 0018 punkt 3 ändrade ADR 0004 beslut 1. Metodrutan följer med dist/scores.json och är
    därmed det anspråk som når en granskare utanför repot. Den gamla lydelsen får inte stå kvar."""
    text = _metodrutan()
    assert "B mäter VÄNTAD STORLEK" not in text
    assert "B mäter GENOMSNITTLIG BELAGD EFFEKTSTYRKA" in text
    assert "INTE LÄNGRE B:s" in text
    assert "ADR 0018 punkt 3" in text


def test_metodrutan_skriver_ut_icke_monotoniciteten() -> None:
    """ADR 0018 punkt 3 kräver att följden skrivs ut. Utan den läser en granskare ett fall i B som
    ett besked om partiet, när det är en egenskap hos medelvärdet."""
    text = _metodrutan()
    assert "KAN SÄNKA B" in text
    assert "#50" in text  # rättelsen har en adress, annars läses felet som accepterat


def test_metodrutan_skiljer_konsensus_fran_partiellt_kodad_ensidighet() -> None:
    """ADR 0018 punkt 5. En post som bara några partier är kodade på skiljer partier åt på
    kodningsflit och inte på hållning, så den får aldrig heta konsensus. En saknad position bär
    inget besked alls och ska stå som okänd."""
    text = _metodrutan()
    assert "KONSENSUS KRÄVER ALLA" in text
    assert "PARTIELLT KODAD ENSIDIGHET" in text
    assert "UTTRYCKLIGEN OKÄND" in text
