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
    """Effekt-claims -> indicator_effects. net_support i [-1,1], confidence i [0,1]."""
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
        abs_sum = 0.0
        conf_vals: list[float] = []
        supporting: list[str] = []
        contradicting: list[str] = []
        for c in cs:
            w = (
                ev_levels.get(c.get("evidence_level", ""), 0.0)
                * num["effect_strength"].get(c.get("effect_strength", "unknown"), 0.0)
                * num["confidence"].get(c.get("confidence", "low"), 0.0)
            )
            s = signed.get(c.get("direction", "unclear"), 0)
            num_sum += w * s
            abs_sum += abs(w)
            conf_vals.append(num["confidence"].get(c.get("confidence", "low"), 0.0))
            (supporting if s >= 0 else contradicting).append(c.get("id", ""))
        net = max(-1.0, min(1.0, num_sum / abs_sum)) if abs_sum > 0 else 0.0
        conf = sum(conf_vals) / len(conf_vals) if conf_vals else 0.0
        effects.append({
            "party": party, "category": cat, "indicator": ind,
            "expected_direction": directions.get((cat, ind), "up"),
            "net_support": round(net, 4), "confidence": round(conf, 4),
            "supporting_claims": [s for s in supporting if s],
            "contradicting_claims": [c for c in contradicting if c],
        })
    return effects
