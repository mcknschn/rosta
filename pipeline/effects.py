"""Lager 3b: claims -> indicator_effects.

Aggregerar evidens-/effekt-claims per (parti, kategori, indikator) till net_support +
confidence enligt aggregeringsreglerna i config/claims.yaml. Matar delpoäng B.
Ren funktion — testas mot fixturer i tests/test_fas4.py.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from . import config


def _expected_directions() -> dict[tuple[str, str], str]:
    """(kategori, indikator) -> riktning (up/down/target) ur categories.yaml."""
    out: dict[tuple[str, str], str] = {}
    for cat in config.categories()["categories"]:
        for ind in cat.get("indicators", []):
            out[(cat["id"], ind["id"])] = ind["direction"]
    return out


def aggregate_effects(claims: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """Effekt-claims -> indicator_effects. net_support i [-1,1], confidence i [0,1].

    net_support är ett KVALITETSVIKTAT MEDEL AV STORLEKAR MED TECKEN (ADR 0004):
    net = Σ(q·m) / Σ q, där q = evidence_level × confidence bär kvaliteten och
    m = effect_strength × tecken(riktning) bär storleken. Storleksskalan står i täljaren
    men inte i nämnaren, så formen kan inte kollapsa till tecknet: ett ensamt claim ger
    exakt sin egen effektstyrka med tecken. mixed/unclear ger m = 0 men behåller sitt q
    och drar därmed cellen mot neutral; effect_strength unknown beter sig likadant, alltså
    som en källa utan storleksbesked. Fältet confidence är oförändrat ett medel av
    claimens confidence och bär osäkerheten kring storleken (scorerun läser det till B:s
    säkerhetsnivå).
    """
    cfg = config.claims()
    ev_levels: dict[str, float] = cfg["evidence_levels"]
    num = cfg["numeric"]
    agg = cfg["aggregation"]
    signed: dict[str, int] = agg["signed_direction"]
    directions = _expected_directions()

    groups: dict[tuple[str, str, str], list[dict[str, Any]]] = {}
    for c in claims:
        if c.get("type") not in ("evidence_effect", "claimed_effect"):
            continue
        key = (c.get("party"), c.get("category"), c.get("indicator"))
        if None in key:
            continue
        groups.setdefault(key, []).append(c)

    effects: list[dict[str, Any]] = []
    for (party, cat, ind), cs in groups.items():
        num_sum = 0.0
        q_sum = 0.0
        conf_vals: list[float] = []
        supporting: list[str] = []
        contradicting: list[str] = []
        for c in cs:
            conf_num = num["confidence"].get(c.get("confidence", "low"), 0.0)
            # q = kvalitet: vems storlek man tror på. m = storlek med tecken, i [-1, 1].
            q = ev_levels.get(c.get("evidence_level", ""), 0.0) * conf_num
            s = signed.get(c.get("direction", "unclear"), 0)
            m = num["effect_strength"].get(c.get("effect_strength", "unknown"), 0.0) * s
            num_sum += q * m
            q_sum += q
            conf_vals.append(conf_num)
            (supporting if s >= 0 else contradicting).append(c.get("id", ""))
        net = max(-1.0, min(1.0, num_sum / q_sum)) if q_sum > 0 else 0.0
        conf = sum(conf_vals) / len(conf_vals) if conf_vals else 0.0
        effects.append({
            "party": party, "category": cat, "indicator": ind,
            "expected_direction": directions.get((cat, ind), "up"),
            "net_support": round(net, 4), "confidence": round(conf, 4),
            "supporting_claims": [s for s in supporting if s],
            "contradicting_claims": [c for c in contradicting if c],
        })
    return effects
