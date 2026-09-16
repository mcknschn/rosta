"""ADR 0020 - säkerheten är sekventiell, och hög räknar evaluationer och aldrig rader.

Fyra lås, ett per halva av beslutet:

  * KEDJAN (beslut 1, 2). `evidence_level` verkar genom INTRÄDESGRINDEN, `confidence` sätter
    etiketten, tunn täckning ger ett steg ned. Efter inträdet skiljer `evidence_level` inte
    mellan band. Kedjan är sekventiell och ordinal, aldrig en sammanvägning av två tal.
  * GRINDEN (beslut 5, 7). Hög säkerhet kräver minst tre VÄSENTLIGEN OBEROENDE evaluationer.
    En rad är inte en studie. `evaluation_id` är det mekaniska golvet, en deklaration av känt
    delat analysunderlag lägger till, och saknad deklaration betyder oberoende.
  * STORLEKEN (beslut 10). En post utan känd storlek står UTANFÖR `B_rått`. Okänd
    effektstorlek är frånvaro av en skattning, aldrig en skattning om exakt neutral verkan.
  * BENÄMNINGEN (beslut 3, 4, 6, 9, 13-17). Bandet är heuristiskt och aldrig kalibrerat, och
    skalans tomma ändar, krympningens innebörd och den rådande ordningen står i klartext.
"""

from __future__ import annotations

import copy

import pytest

from pipeline import config, effects, positions, scorerun, warehouse
from pipeline.sources import government

# --- gemensamma fixturer -------------------------------------------------------------


def _post(**over: object) -> dict:
    bas = {
        "category": "ekonomi", "indicator": "arbetsloshet", "policy_type": "typ_a",
        "direction": "positive", "evidence_level": "authority_evaluation",
        "effect_strength": "medium", "confidence": "medium",
        "source": "Myndigheten, Rapport 1", "source_url": "https://ex.test/rapport-1",
    }
    bas.update(over)
    return bas


def _claims(ledger: list[dict], party: str = "M") -> list[dict]:
    pos = [
        {"party": party, "policy_type": pt, "stance": "supports", "source": "s"}
        for pt in dict.fromkeys(e["policy_type"] for e in ledger)
    ]
    return positions.build_evidence_effect_claims(positions=pos, ledger=ledger)


def _independence(entries: list[dict], monkeypatch: pytest.MonkeyPatch) -> dict[str, str]:
    ledger = copy.deepcopy(config.evidence_ledger())
    ledger["entries"] = entries
    monkeypatch.setattr(config, "evidence_ledger", lambda: ledger)
    return config.evaluation_independence()


def _min_evaluations() -> int:
    return int(config.claims()["aggregation"]["min_evaluations_for_high_confidence"])


def _ee(
    cid: str, strength: str, policy: str = "typ_a", direction: str = "positive",
    niva: str = "authority_evaluation",
) -> dict:
    return {
        "id": cid, "type": "evidence_effect", "party": "M", "category": "ekonomi",
        "indicator": "arbetsloshet", "direction": direction, "policy_type": policy,
        "evidence_level": niva, "effect_strength": strength, "confidence": "medium",
    }


def _bygg() -> dict:
    """En ren körning. Warehouse i `:memory:`, aldrig data/warehouse.duckdb."""
    con = warehouse.connect(":memory:")
    warehouse.upsert(con, "responsibility", government.build_national_responsibility())
    res = scorerun.build(con)["scores"]
    con.close()
    return res


# --- grinden: hög räknar evaluationer, inte rader ------------------------------------


def test_claimet_bar_sin_evaluation() -> None:
    """Räkningen kan bara vara oberoende av redaktionell uppdelning om identiteten följer med
    claimet. Utan fältet måste scorerun slå upp liggaren igen och gissa vilken rad som gav
    claimet."""
    cl = _claims([_post()])
    assert cl[0]["evaluation_id"] == config.evaluation_id(_post())


def test_tre_rader_ur_samma_utvardering_ar_en_evaluation() -> None:
    """Beslut 5: en rad är inte en studie. Tre estimand ur samma studie är EN studie."""
    led = [
        _post(policy_type="typ_a"),
        _post(policy_type="typ_b"),
        _post(policy_type="typ_c"),
    ]
    assert scorerun._b_evaluations(_claims(led)) == {("M", "ekonomi"): 1}


def test_skilda_utvarderingar_raknas_var_for_sig() -> None:
    led = [
        _post(policy_type="typ_a", source_url="https://ex.test/rapport-1"),
        _post(policy_type="typ_b", source_url="https://ex.test/rapport-2"),
        _post(policy_type="typ_c", source_url="https://ex.test/rapport-3"),
    ]
    assert scorerun._b_evaluations(_claims(led)) == {("M", "ekonomi"): 3}


def test_delat_analysunderlag_slar_ihop_tva_evaluationer(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Beslut 7: `evaluation_id` är GOLVET. En liggarpost får deklarera känt delat
    analysunderlag, och då räknas de två som en."""
    led = [
        _post(policy_type="typ_a", source_url="https://ex.test/rapport-1"),
        _post(policy_type="typ_b", source_url="https://ex.test/rapport-2",
              shared_analysis_with="https://ex.test/rapport-1"),
        _post(policy_type="typ_c", source_url="https://ex.test/rapport-3"),
    ]
    karta = _independence(led, monkeypatch)
    assert scorerun._b_evaluations(_claims(led), karta) == {("M", "ekonomi"): 2}


def test_delat_analysunderlag_ar_transitivt(monkeypatch: pytest.MonkeyPatch) -> None:
    """A delar med B och B delar med C: alla tre är ETT analysunderlag. Utan transitiviteten
    beror talet på vilken post redaktören råkade peka från."""
    led = [
        _post(policy_type="typ_a", source_url="https://ex.test/rapport-1"),
        _post(policy_type="typ_b", source_url="https://ex.test/rapport-2",
              shared_analysis_with="https://ex.test/rapport-1"),
        _post(policy_type="typ_c", source_url="https://ex.test/rapport-3",
              shared_analysis_with="https://ex.test/rapport-2"),
    ]
    karta = _independence(led, monkeypatch)
    assert scorerun._b_evaluations(_claims(led), karta) == {("M", "ekonomi"): 1}


def test_pekare_utan_mottagare_hard_failar(monkeypatch: pytest.MonkeyPatch) -> None:
    """Beslut 7: en pekare utan mottagare ger HÅRD FAIL. En tyst pekare vore värre än ingen:
    den ser ut som en deklaration men lämnar räkningen orörd."""
    with pytest.raises(config.ConfigError, match="delat analysunderlag"):
        _independence([_post(shared_analysis_with="https://ex.test/finns-inte")], monkeypatch)


def test_pekare_till_sig_sjalv_hard_failar(monkeypatch: pytest.MonkeyPatch) -> None:
    """En post som pekar på sin egen utvärdering deklarerar ingenting och är sannolikt ett
    klipp-och-klistra-fel."""
    with pytest.raises(config.ConfigError, match="samma utvärdering"):
        _independence([_post(shared_analysis_with="https://ex.test/rapport-1")], monkeypatch)


def test_saknad_deklaration_antas_oberoende() -> None:
    """Beslut 7: motsatsen, att anta beroende när inget sägs, gör hög säkerhet onåbar för
    alltid och byter en empirisk lucka mot en strukturell. Dagens liggare deklarerar
    ingenting, alltså är kartan tom."""
    assert config.evaluation_independence() == {}


def test_b_confidence_kraver_min_evaluations_for_high() -> None:
    num, mc = config.claims()["numeric"]["confidence"], _min_evaluations()
    assert scorerun._b_confidence(num["high"], mc, False) == "high"
    assert scorerun._b_confidence(num["high"], mc - 1, False) == "medium"


def test_evidensnivan_skiljer_inte_mellan_band_efter_intradet() -> None:
    """Beslut 1 och 11: efter inträdet bär `confidence` etiketten ensam.

    Två celler som skiljer sig ENBART i evidensnivå ger samma säkerhetstal, alltså samma
    etikett. Evidensklassen verkar genom grinden och finns kvar i datamodellen, men den är
    skild från etiketten. Skulle någon väga in nivån i etiketten faller provet.

    Grinden släpper bara in de två nivåer som prövas här, så paret är hela den mängd där
    frågan alls kan ställas.
    """
    tal = [
        effects.aggregate_effects([_ee("c1", "medium", niva=niva)])[0]["confidence"]
        for niva in ("systematic_review", "authority_evaluation")
    ]
    assert tal[0] == tal[1]
    assert scorerun._b_confidence(tal[0], 9, False) == scorerun._b_confidence(tal[1], 9, False)


def test_evidensnivan_star_kvar_i_datamodellen() -> None:
    """Beslut 11: att slå ihop klass och etikett vore att låta en regel om INTRÄDE se ut som
    en regel om säkerhet. Klassen ska därför finnas kvar som eget fält på claimet."""
    cl = _claims([_post()])
    assert cl[0]["evidence_level"] == "authority_evaluation"
    assert cl[0]["confidence"] == "medium"


# --- det låsta utfallet ---------------------------------------------------------------


def test_hog_sakerhet_har_noll_medlemmar() -> None:
    """Beslut 5, mätt och godtaget FÖRE låsningen: hög går från 7 celler till 0.

    De sju var alla försvar, med 3 råa rader men 2 evaluationer, eftersom nato_medlemskap och
    dca_avtal_usa är kodade ur samma riksdagsdokument. Faller utfallet annorlunda ska det
    utredas, aldrig accepteras tyst - därför står talet här och inte bara i ADR:n."""
    res = _bygg()
    hoga = [
        (p, c) for p, kats in res["scores"].items()
        for c, cell in kats.items() if cell["confidence"]["B"] == "high"
    ]
    assert hoga == []


def test_forsvarscellerna_ligger_kvar_pa_mellan() -> None:
    """Grinden sänker sju celler ETT steg och aldrig två. Låg nås bara genom
    täckningsnedgradering, och försvar är inte tunt täckt."""
    res = _bygg()
    forsvar = {p: kats["forsvar"]["confidence"]["B"] for p, kats in res["scores"].items()}
    for p in ("C", "KD", "L", "M", "S", "SD", "V"):
        assert forsvar[p] == "medium"


def test_oberoenderakningen_ar_det_som_sanker_forsvar() -> None:
    """Låser ORSAKEN och inte bara utfallet: de sju cellerna bär fortfarande tre råa claims,
    men bara två evaluationer. Skulle någon räkna rader igen fångar provet det."""
    cl = positions.build_evidence_effect_claims()
    ev = scorerun._b_evaluations(cl)
    rader: dict[tuple[str, str], int] = {}
    for c in cl:
        nyckel = (c["party"], c["category"])
        rader[nyckel] = rader.get(nyckel, 0) + 1
    for p in ("C", "KD", "L", "M", "S", "SD", "V"):
        assert rader[(p, "forsvar")] == 3
        assert ev[(p, "forsvar")] == 2


# --- storleken: okänd storlek står utanför B_rått --------------------------------------


def test_okand_storlek_andrar_inte_b_ratt() -> None:
    """Beslut 10: okänd effektstorlek är FRÅNVARO av en skattning, aldrig en skattning om
    exakt neutral verkan. Posten drar alltså inte cellen mot neutral."""
    ensam = effects.aggregate_effects([_ee("c1", "high")])[0]["net_support"]
    med_okand = effects.aggregate_effects([_ee("c1", "high"), _ee("c2", "unknown")])
    assert med_okand[0]["net_support"] == pytest.approx(ensam, abs=1e-9)


def test_okand_storlek_redovisas_som_dokumentation() -> None:
    """Posten får räknas mot en separat dokumentationstäckning, men aldrig som belägg för
    neutral verkan. Utan fältet försvinner källspåret."""
    eff = effects.aggregate_effects([_ee("c1", "high"), _ee("c2", "unknown")])[0]
    assert eff["size_unknown_claims"] == ["c2"]
    assert "c2" not in eff["supporting_claims"]


def test_atgardstyp_med_bara_okand_storlek_ger_ingen_cell() -> None:
    """En åtgärdstyp vars enda post saknar storlek bidrar inte, och en cell där ingen post
    bär storlek finns inte i B_rått alls."""
    assert effects.aggregate_effects([_ee("c1", "unknown")]) == []


def test_oklar_riktning_drar_fortfarande_mot_neutral() -> None:
    """Gränsen går vid STORLEKEN. En källa som fann oklar riktning HAR en skattning och
    behåller sitt q (ADR 0004 punkt 3). Beslut 10 rör inte den."""
    ensam = effects.aggregate_effects([_ee("c1", "high")])[0]["net_support"]
    med_oklar = effects.aggregate_effects(
        [_ee("c1", "high"), _ee("c2", "medium", direction="mixed")]
    )[0]["net_support"]
    assert med_oklar == pytest.approx(ensam / 2, abs=1e-4)


def test_regeln_har_noll_medlemmar_i_dag() -> None:
    """Beslut 10 skrevs FÖRE medlemmar, som ADR 0003 punkt 1 kräver. Mätt: 0 av liggarens
    poängberättigade påståenden saknar storlek. Rör sig talet är det en dataändring och
    inte en kodändring."""
    cl = positions.build_evidence_effect_claims()
    assert [c["id"] for c in cl if c["effect_strength"] == "unknown"] == []


# --- benämningen: metodrutan --------------------------------------------------------


def _metodrutan() -> str:
    return _bygg()["meta"]["coverage_technical"]


def test_bandets_markning_ar_permanent_och_maskinlast() -> None:
    """Beslut 3: `provisional` ERSÄTTS och lyfts inte. Ett preliminärt tillstånd väntar på en
    rättelse, medan detta är en bestående egenskap."""
    meta = _bygg()["meta"]
    assert "safety_model_status" not in meta
    assert meta["uncertainty_band_status"] == "heuristic_never_calibrated"


def test_metodrutan_skriver_ut_sakerhetskedjan() -> None:
    """Beslut 1: kedjan står skriven, och med den att `evidence_level` inte skiljer mellan
    band efter inträdet. Annars läses fältets frånvaro ur bandet som en glömska."""
    text = _metodrutan()
    assert "SÄKERHETEN ÄR SEKVENTIELL" in text
    assert "INTE mellan band" in text


def test_metodrutan_skriver_ut_skalans_tomma_andar() -> None:
    """Beslut 6: tre saker redovisas, eftersom skalan annars ser ut att mäta mer än den gör."""
    text = _metodrutan()
    assert "NOLL MEDLEMMAR" in text
    assert "täckningsnedgradering" in text
    assert "särskiljningsförmåga" in text


def test_metodrutan_kallar_bandet_heuristiskt() -> None:
    """Beslut 3: bandet kallas hädanefter ett heuristiskt osäkerhetsband och aldrig ett
    kalibrerat intervall."""
    text = _metodrutan()
    assert "HEURISTISKT OSÄKERHETSBAND" in text
    assert "aldrig kalibrerat" in text


def test_metodrutan_skriver_krympningen_ratt() -> None:
    """Beslut 9: krympningen mäter EVIDENSDJUP, aldrig neutral imputering av saknade
    indikatorer. De två täckningsbegreppen går isär med median 0,225."""
    text = _metodrutan()
    assert "EVIDENSDJUP" in text
    assert "0,225" in text
    assert "55 av 56" in text


def test_metodrutan_skriver_ut_radande_ordning() -> None:
    """Beslut 13, 14 och 17: klipp per indikator, sedan vikt, sedan yttre klamp; tunn
    täckning vid viktat undermåttsdjup under 0,50; och medianvarianten är nedlagd."""
    text = _metodrutan()
    assert "KLIPP PER INDIKATOR" in text
    assert "0,50" in text
    assert "MEDIAN" in text
