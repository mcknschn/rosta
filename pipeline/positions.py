"""Lager 3b': partikopplade evidence_effect-claims ur config (delpoäng B).

Joinar config/party_positions.yaml (åtgärdstyper ett parti faktiskt driver, med källa)
mot config/evidence_ledger.yaml (åtgärdstyp -> indikatoreffekt enligt officiell svensk
utvärdering). Resultatet matar effects.aggregate_effects -> indicator_effects -> B.

INGA partiståndpunkter hittas på här. party_positions är en kurerings-gated seed (tom tills
en människa fyllt den med källbelagda ståndpunkter), så normalt returneras [] och B faller
tillbaka på neutral i scorerun. Ren funktion med injicerbara fixturer -> testbar.
"""

from __future__ import annotations

from typing import Any

from . import config

# Om partiet är EMOT en åtgärdstyp vänds åtgärdstypens evidensriktning.
_FLIP = {"positive": "negative", "negative": "positive", "mixed": "mixed", "unclear": "unclear"}


def _dedup_estimands(ledger: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Ett estimand bidrar EN gång i sin nod (ADR 0019 beslut 10).

    Noden är (evaluation_id, indikator, åtgärdstyp). Två rader som delar nod OCH estimand men
    bär olika storlek eller riktning är en motsägelse om analysenheten, aldrig ett tyst
    medelvärde: hård fail, så redaktören tvingas lösa den.

    Regeln har noll aktiva fall i dagens liggare. Den byggs ändå, eftersom estimatorn annars
    gör något tyst och fel den dag en andra rad landar i samma nod, och antalet rader då blir
    en dold vikt.
    """
    sedda: dict[tuple[str, str, str, str], dict[str, Any]] = {}
    ut: list[dict[str, Any]] = []
    for e in ledger:
        nyckel = (
            config.evaluation_id(e), config.estimand_id(e), e["indicator"], e["policy_type"],
        )
        tidigare = sedda.get(nyckel)
        if tidigare is None:
            sedda[nyckel] = e
            ut.append(e)
            continue
        samma = all(
            tidigare.get(f) == e.get(f)
            for f in ("direction", "effect_strength", "evidence_level", "confidence")
        )
        if not samma:
            raise config.ConfigError(
                "samma utvärdering och estimand med olika storlek i noden "
                f"{nyckel[0]} / {e['indicator']} / {e['policy_type']}: analysenheten är "
                "motsägelsefull och måste lösas i liggaren"
            )
    return ut


def build_evidence_effect_claims(
    positions: list[dict[str, Any]] | None = None,
    ledger: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """party_positions × evidence_ledger -> evidence_effect-claims (en per indikatoreffekt).

    stance=supports behåller evidensens riktning; stance=opposes vänder den. Varje claim får
    source_refs från både partiets förslag och evidenskällan (spårbarhet, krav i claims.yaml).
    """
    if positions is None:
        positions = config.party_positions().get("entries") or []
    if ledger is None:
        # Bara poster som passerar den symmetriska evidensgrinden (rubriken §5, ADR 0006)
        # OCH vars åtgärdstyp inte är spärrad från jämförande poängsättning (ADR 0019).
        # En utlyft eller spärrad post står kvar i liggaren med källa och skäl men ger
        # inga claims. De två uteslutningarna är skilda och blandas aldrig ihop.
        ledger = config.scoring_eligible_ledger_entries()

    by_policy: dict[str, list[dict[str, Any]]] = {}
    for e in _dedup_estimands(ledger):
        by_policy.setdefault(e["policy_type"], []).append(e)

    claims: list[dict[str, Any]] = []
    for pos in positions:
        party = pos["party"]
        policy = pos["policy_type"]
        stance = pos.get("stance", "supports")
        for e in by_policy.get(policy, []):
            direction = e["direction"] if stance == "supports" else _FLIP.get(e["direction"], "unclear")
            verb = "driver" if stance == "supports" else "motsätter sig"
            claims.append({
                "id": f"claim:evidence_effect:{party}:{policy}:{e['category']}:{e['indicator']}",
                "type": "evidence_effect", "party": party,
                "policy_type": policy,
                "category": e["category"], "indicator": e["indicator"],
                "direction": direction,
                "evidence_level": e["evidence_level"],
                "effect_strength": e["effect_strength"],
                "confidence": e["confidence"],
                "statement": (
                    f"{party} {verb} {policy}; evidens ({e['evidence_level']}) talar för "
                    f"riktning {direction} på {e['indicator']}."
                ),
                "source_refs": [pos["source"], e["source"]],
            })
    return claims
