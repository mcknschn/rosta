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
        # Bara poster som passerar den symmetriska evidensgrinden (rubriken §5, ADR 0006).
        # En utlyft post står kvar i liggaren med källa och skäl men ger inga claims.
        ledger = config.admitted_ledger_entries()

    by_policy: dict[str, list[dict[str, Any]]] = {}
    for e in ledger:
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
