"""ADR 0011: Uteslutningsskälet är ett eget besked, inte en riktning.

Ett REGELTEST. Inget tal om täckningens nivå, spridning eller rangordning står här
(ADR 0011 godkännandetest punkt 6). Ett sådant tal vore ett täckningsmål, och det förbjuder
ADR 0006:s godkännandetest av samma skäl.

Reglerna som låses:
  1. `direction` godkänner bara `up` och `down`.
  2. Varje indikator bär antingen en Riktning eller ett Uteslutningsskäl, aldrig båda och
     aldrig ingetdera.
  3. Varje Uteslutningsskäl är ett av de tre värdena, och varje utesluten indikator bär ett
     återöppningsvillkor.
  4. En liggarpost mot en utesluten indikator hard-failar, oavsett vad dess syskonindikatorer
     bär.
  5. Täckningen får en egen nämnare. Krympningen behåller sin, så betygen står still.

Tester rör aldrig disklagret: warehouse körs i `:memory:`, aldrig `data/warehouse.duckdb`.
"""

from __future__ import annotations

import copy

import pytest

from pipeline import config, scorerun, warehouse
from pipeline.sources import government

# De tre indikatorer som föll på var sitt steg i regelns prövning (ADR 0011 punkt 6). Talen
# står här som en LÅST förteckning över vad som är uteslutet och varför, aldrig som ett
# påstående om hur mycket täckning det kostar.
UTESLUTNA = {
    ("forsvar", "forsvarsanslag_andel_bnp"): "gransfel",
    ("ekonomi", "inflation"): "giltighetsfel",
    ("ekonomi", "statsskuld_underskott"): "neutralitetsfel",
}


def _indicators() -> list[tuple[str, dict]]:
    return [
        (cat["id"], ind)
        for cat in config.categories()["categories"]
        for ind in cat.get("indicators", [])
    ]


def _patch_indicator(monkeypatch: pytest.MonkeyPatch, cat_id: str, ind_id: str, **fields) -> None:
    """Byter ut ETT indikatorobjekt i en kopia av categories.yaml och validerar mot den."""
    cats = copy.deepcopy(config.categories())
    for cat in cats["categories"]:
        if cat["id"] != cat_id:
            continue
        for i, ind in enumerate(cat["indicators"]):
            if ind["id"] == ind_id:
                cat["indicators"][i] = {"id": ind_id, "submeasure": ind["submeasure"], **fields}
                monkeypatch.setattr(config, "categories", lambda: cats)
                return
    raise AssertionError(f"okänd indikator {cat_id}/{ind_id}")


# --- 1. Riktningen håller bara upp och ned (godkännandetest punkt 1) ------------


def test_riktningen_haller_bara_upp_och_ned() -> None:
    for cat_id, ind in _indicators():
        if "direction" in ind:
            assert ind["direction"] in config.VALID_DIRECTIONS, f"{cat_id}/{ind['id']}"


def test_ett_tredje_riktningsvarde_faller_i_valideringen(monkeypatch: pytest.MonkeyPatch) -> None:
    """`target` var det tredje värdet fram till 2026-08-26. Det får inte kunna skrivas igen."""
    _patch_indicator(monkeypatch, "ekonomi", "sysselsattning", direction="target")
    with pytest.raises(config.ConfigError, match="Ogiltig riktning"):
        config.validate()


# --- 2. Riktning eller Uteslutningsskäl, aldrig båda (godkännandetest punkt 2) --


def test_varje_indikator_bar_det_ena_eller_det_andra() -> None:
    for cat_id, ind in _indicators():
        assert ("direction" in ind) != ("exclusion" in ind), f"{cat_id}/{ind['id']}"


def test_bade_riktning_och_uteslutning_faller(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ett fält som bar båda skulle dölja det ena med det andra, vilket `target` gjorde."""
    _patch_indicator(
        monkeypatch, "ekonomi", "sysselsattning",
        direction="up", exclusion="gransfel", reopen_if="aldrig",
    )
    with pytest.raises(config.ConfigError, match="båda"):
        config.validate()


def test_varken_riktning_eller_uteslutning_faller(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_indicator(monkeypatch, "ekonomi", "sysselsattning", note="utan besked")
    with pytest.raises(config.ConfigError, match="ingetdera"):
        config.validate()


# --- 3. Tre värden och ett återöppningsvillkor (godkännandetest punkt 3) --------


def test_de_tre_uteslutna_bar_sitt_skal() -> None:
    """Regeln kördes på de tre indikatorer som bar `target`, och de föll på tre olika steg."""
    assert config.excluded_indicators() == UTESLUTNA


def test_varje_uteslutningsskal_ar_ett_av_de_tre() -> None:
    assert set(config.excluded_indicators().values()) <= set(config.VALID_EXCLUSIONS)


def test_ett_fjarde_uteslutningsskal_faller(monkeypatch: pytest.MonkeyPatch) -> None:
    """Namnen pekar på en beslutad regel. Ett symtomnamn går inte att återanvända."""
    _patch_indicator(
        monkeypatch, "ekonomi", "sysselsattning",
        exclusion="omtvistad_malniva", reopen_if="aldrig",
    )
    with pytest.raises(config.ConfigError, match="Ogiltigt uteslutningsskäl"):
        config.validate()


def test_varje_utesluten_indikator_bar_ett_ateroppningsvillkor() -> None:
    for cat_id, ind in _indicators():
        if "exclusion" not in ind:
            continue
        assert str(ind.get("reopen_if", "")).strip(), f"{cat_id}/{ind['id']}"


def test_utesluten_utan_ateroppningsvillkor_faller(monkeypatch: pytest.MonkeyPatch) -> None:
    """Villkoret säger vad som måste ändras för att felet ska vara borta (ADR 0011 punkt 8).
    De tre stod i dag som "behålls som kontext", utan slut."""
    _patch_indicator(monkeypatch, "ekonomi", "sysselsattning", exclusion="gransfel")
    with pytest.raises(config.ConfigError, match="reopen_if"):
        config.validate()


def test_ateroppningsvillkoret_pekar_pa_nagot_provbart() -> None:
    """Villkoret ska gå att pröva, alltså namnge en källa eller en fil att pröva det mot."""
    for cat_id, ind in _indicators():
        if "exclusion" not in ind:
            continue
        assert "Prövas mot" in ind["reopen_if"], f"{cat_id}/{ind['id']}"


# --- 4. Ingen evidenspost mot en utesluten indikator (godkännandetest punkt 4) --


def _ledger_with(entry_overrides: dict) -> dict:
    led = copy.deepcopy(config.evidence_ledger())
    led["entries"].append({
        "policy_type": "test_typ", "direction": "positive",
        "evidence_level": "authority_evaluation", "effect_strength": "medium",
        "confidence": "medium", "source": "test", **entry_overrides,
    })
    return led


@pytest.mark.parametrize(("cat_id", "ind_id"), sorted(UTESLUTNA))
def test_liggarpost_mot_utesluten_indikator_hard_failar(
    monkeypatch: pytest.MonkeyPatch, cat_id: str, ind_id: str
) -> None:
    """Grinden går på uteslutningsfältet och ALDRIG på om ett syskon råkar bära riktning.

    De tre täcker båda formerna. `inflation` och `statsskuld_underskott` ligger i undermått
    där varje indikator är utesluten, medan `forsvarsanslag_andel_bnp` har en syskonindikator
    med riktning `up`. Före grinden ignorerades den första formen tyst och den andra räknades
    tyst. Båda är fel svar.
    """
    led = _ledger_with({"category": cat_id, "indicator": ind_id})
    monkeypatch.setattr(config, "evidence_ledger", lambda: led)
    with pytest.raises(config.ConfigError, match=ind_id):
        config.validate()


def test_grinden_bryr_sig_inte_om_admitted(monkeypatch: pytest.MonkeyPatch) -> None:
    """Utlyftningen (`admitted: false`) är ADR 0006:s evidensgrind och svarar på en annan
    fråga, alltså om posten HÅLLER, inte om indikatorn går att poängsätta."""
    led = _ledger_with({
        "category": "ekonomi", "indicator": "inflation",
        "admitted": False, "admission_note": "test",
    })
    monkeypatch.setattr(config, "evidence_ledger", lambda: led)
    with pytest.raises(config.ConfigError, match="inflation"):
        config.validate()


def test_liggarpost_mot_en_indikator_med_riktning_passerar(monkeypatch: pytest.MonkeyPatch) -> None:
    """Grinden får bara bita på uteslutna indikatorer. En syskonpost ska gå igenom."""
    led = _ledger_with({
        "category": "forsvar", "indicator": "forsvarsfinansiering_upptrappning_mot_mal",
    })
    monkeypatch.setattr(config, "evidence_ledger", lambda: led)
    config.validate()


def test_liggaren_som_den_star_passerar_grinden() -> None:
    """Noll poster pekar på en utesluten indikator i dag. Grinden låser en form."""
    excluded = config.excluded_indicators()
    for e in config.evidence_ledger()["entries"]:
        assert (e["category"], e["indicator"]) not in excluded, e["policy_type"]


# --- 5. Täckningen får en egen nämnare, krympningen behåller sin ---------------


# Krympningsnämnarens egen regel, alltså vilka undermått som faller ur den, står i
# tests/test_d_breadth_gate.py och prövas inte om här.


def test_tackningens_namnare_ar_kategorins_fulla_undermattsvikt() -> None:
    """Ett uteslutet undermått räknas 0 täckt i stället för att strykas ur nämnaren."""
    assert set(scorerun._coverage_denominators().values()) == {100}


def test_de_tva_namnarna_ar_skilda_dar_ett_undermatt_ar_uteslutet() -> None:
    sub_w = scorerun._submeasure_weights()
    shrink = scorerun._non_excluded_submeasures()
    cov = scorerun._coverage_denominators()
    for c, kvar in shrink.items():
        krympt = sum(sub_w[c][s] for s in kvar)
        utesluten_vikt = cov[c] - krympt
        assert utesluten_vikt >= 0
        # Ekonomi är den enda kategorin där alla indikatorer i ett undermått är uteslutna.
        assert (utesluten_vikt > 0) == (c == "ekonomi"), c


# --- metodrutan namnger de uteslutna och skälen (ADR 0011 punkt 10) ------------


def _seed_con():
    """Warehouse UTAN observationer. Kör `:memory:`, aldrig data/warehouse.duckdb."""
    con = warehouse.connect(":memory:")
    warehouse.upsert(con, "responsibility", government.build_national_responsibility())
    return con


def test_metodrutan_namnger_varje_utesluten_indikator_med_sitt_skal() -> None:
    """Ett samlingsord räcker inte: hela beslutet är att de tre felen är olika."""
    con = _seed_con()
    text = scorerun.build(con)["scores"]["meta"]["coverage_technical"]
    con.close()
    for (cat_id, ind_id), reason in config.excluded_indicators().items():
        assert ind_id in text, ind_id
        assert f"{cat_id}/{ind_id} ({reason}" in text, ind_id
        assert config.EXCLUSION_REASONS[reason] in text, reason


def test_metodrutan_forklarar_varfor_talet_sjonk() -> None:
    """Ett sjunkande täckningstal utan förklaring inbjuder till slutsatsen att ekonomidata
    blivit sämre. Rutan säger vad som ändrades, och att inget betyg rör sig."""
    con = _seed_con()
    text = scorerun.build(con)["scores"]["meta"]["coverage_technical"]
    con.close()
    assert "0 TÄCKT" in text
    assert "inget betyg rör sig" in text
    # Rutan får bara påstå 0 täckt om de undermått där VARJE indikator är utesluten. Ett
    # undermått med en syskonindikator som bär riktning står kvar och rör sig inte.
    sub_w = scorerun._submeasure_weights()
    kvar = scorerun._non_excluded_submeasures()
    for c, w in sub_w.items():
        for sm in w:
            assert (f"{c}/{sm}" in text) == (sm not in kvar[c]), f"{c}/{sm}"
