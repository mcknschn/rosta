"""Fas 4: claims -> indicator_effects-aggregering."""

from __future__ import annotations

import pytest

from pipeline import effects


def test_aggregate_effects_net_support_direction_and_confidence() -> None:
    claims = [
        {"id": "claim:evidence_effect:1", "type": "evidence_effect", "party": "M",
         "category": "ekonomi", "indicator": "arbetsloshet", "direction": "positive",
         "evidence_level": "authority_evaluation", "effect_strength": "high", "confidence": "high"},
        {"id": "claim:evidence_effect:2", "type": "evidence_effect", "party": "M",
         "category": "ekonomi", "indicator": "arbetsloshet", "direction": "negative",
         "evidence_level": "single_study_report", "effect_strength": "medium", "confidence": "medium"},
    ]
    eff = effects.aggregate_effects(claims)
    assert len(eff) == 1
    e = eff[0]
    assert (e["party"], e["category"], e["indicator"]) == ("M", "ekonomi", "arbetsloshet")
    assert e["expected_direction"] == "down"  # ur categories.yaml
    # w1=0.8*1.0*0.85=0.68 (+), w2=0.5*0.6*0.6=0.18 (-): net=(0.68-0.18)/0.86
    assert e["net_support"] == pytest.approx(0.5814, abs=1e-3)
    assert e["confidence"] == pytest.approx(0.725, abs=1e-3)
    assert "claim:evidence_effect:1" in e["supporting_claims"]
    assert "claim:evidence_effect:2" in e["contradicting_claims"]


def test_aggregate_effects_ignores_non_effect_and_partyless() -> None:
    claims = [
        {"id": "x", "type": "action", "party": "S", "category": "ekonomi"},
        {"id": "y", "type": "evidence_effect", "category": "ekonomi",
         "indicator": "arbetsloshet", "direction": "positive"},  # saknar party
    ]
    assert effects.aggregate_effects(claims) == []


# --- Fas 4b: partikopplad B (party_positions × evidence_ledger) ----------------

_LEDGER = [{
    "policy_type": "subv", "category": "ekonomi", "indicator": "arbetsloshet",
    "direction": "positive", "evidence_level": "systematic_review",
    "effect_strength": "high", "confidence": "high", "source": "SBU (test)",
}]


def test_positions_join_supports_keeps_direction_with_sources() -> None:
    from pipeline import positions
    pos = [{"party": "M", "policy_type": "subv", "stance": "supports", "source": "motion X"}]
    claims = positions.build_evidence_effect_claims(pos, _LEDGER)
    assert len(claims) == 1
    c = claims[0]
    assert c["type"] == "evidence_effect" and c["party"] == "M"
    assert c["category"] == "ekonomi" and c["indicator"] == "arbetsloshet"
    assert c["direction"] == "positive"
    assert c["source_refs"] == ["motion X", "SBU (test)"]   # spårbarhet: båda källorna


def test_positions_opposes_flips_direction() -> None:
    from pipeline import positions
    pos = [{"party": "M", "policy_type": "subv", "stance": "opposes", "source": "motion X"}]
    assert positions.build_evidence_effect_claims(pos, _LEDGER)[0]["direction"] == "negative"


def test_b_chain_activates_when_curated() -> None:
    # Hela B-kedjan: ståndpunkt (supports, evidens positiv) -> net_support>0 -> B>2.5.
    from pipeline import positions, score
    pos = [{"party": "M", "policy_type": "subv", "stance": "supports", "source": "motion X"}]
    eff = effects.aggregate_effects(positions.build_evidence_effect_claims(pos, _LEDGER))
    assert len(eff) == 1 and eff[0]["net_support"] > 0
    b = score.aggregate_B({eff[0]["indicator"]: eff[0]["net_support"]}, {eff[0]["indicator"]: 25})
    assert b > 2.5


def test_shipped_party_positions_are_sourced_not_fabricated() -> None:
    # Integritetsvakt: deployad config får bara innehålla KÄLLBELAGDA ståndpunkter (ingen fabrikation).
    # Tom fil var den tidigare garantin; med klimat-piloten verifieras i stället VARJE rad:
    # giltigt parti, en åtgärdstyp som finns i evidensliggaren, giltig stance, och spårbar
    # källa (kort beteckning + URL + dok-id + ordagrant utdrag).
    from pipeline import config
    pp = config.party_positions()
    assert pp.get("version") == 2  # sign-off 2026-06-07 (B-grön + integration-svepen); v1 = 2026-06-05
    assert pp.get("status") == "expert_reviewed"
    parties = set(config.party_codes())
    ledger_policies = {e["policy_type"] for e in config.evidence_ledger()["entries"]}
    for e in pp.get("entries") or []:
        assert e["party"] in parties, e
        assert e["policy_type"] in ledger_policies, f"policy_type saknar evidens i liggaren: {e}"
        assert e["stance"] in {"supports", "opposes"}, e
        for field in ("source", "source_url", "doc_id", "quote"):
            assert e.get(field, "").strip(), f"rad saknar {field} (källbeläggning): {e}"


def test_evidence_ledger_entries_valid_and_sourced() -> None:
    # Varje evidenspost: kanonisk indikator, giltiga etiketter (claims.yaml), och en källa.
    from pipeline import config
    allinds = {
        (c["id"], i["id"])
        for c in config.categories()["categories"] for i in c.get("indicators", [])
    }
    cl = config.claims()
    levels, dirs = set(cl["evidence_levels"]), set(cl["enums"]["direction"])
    strengths, confs = set(cl["enums"]["effect_strength"]), set(cl["enums"]["confidence"])
    entries = config.evidence_ledger()["entries"]
    assert entries
    for e in entries:
        assert (e["category"], e["indicator"]) in allinds, f"okänd indikator: {e}"
        assert e["direction"] in dirs, e
        assert e["evidence_level"] in levels, e
        assert e["effect_strength"] in strengths, e
        assert e["confidence"] in confs, e
        assert e.get("source", "").strip(), f"saknar source: {e}"


def test_empty_positions_yield_no_claims() -> None:
    # Enhetsinvariant: utan ståndpunkter genereras inga claims (B faller tillbaka på neutral).
    # (Tidigare testades shipped config; den är nu icke-tom efter klimat-piloten.)
    from pipeline import positions
    assert positions.build_evidence_effect_claims([], _LEDGER) == []
    assert positions.build_evidence_effect_claims([], []) == []


def test_shipped_klimat_pilot_activates_b() -> None:
    # Klimat-piloten (shipped config) ska generera evidence_effect-claims -> B aktiveras för klimat,
    # med både supports- och opposes-sidan representerad (reduktionsplikt-voteringen).
    from pipeline import positions
    claims = positions.build_evidence_effect_claims()  # shipped party_positions × evidence_ledger
    klimat = [c for c in claims if c["category"] == "klimat"]
    assert klimat, "klimat-piloten gav inga claims"
    assert {"S", "M", "SD", "V"} <= {c["party"] for c in klimat}
    # supports behåller positiv riktning, opposes vänder till negativ (reduktionsplikt):
    by_party_dir = {(c["party"], c["direction"]) for c in klimat if c["indicator"] == "territoriella_utslapp"}
    assert ("S", "positive") in by_party_dir   # S röstade för bibehållen plikt
    assert ("M", "negative") in by_party_dir   # M röstade för sänkt plikt
