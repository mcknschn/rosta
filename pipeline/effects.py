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
    """(kategori, indikator) -> riktning (up/down) ur categories.yaml.

    Uteslutna indikatorer (ADR 0011) har ingen riktning och står inte här. De kan ändå
    aldrig nå hit: config.validate hard-failar på en evidenspost mot en utesluten indikator
    (ADR 0011 punkt 7), så det finns inga claims att gruppera.
    """
    out: dict[tuple[str, str], str] = {}
    for cat in config.categories()["categories"]:
        for ind in cat.get("indicators", []):
            if "direction" in ind:
                out[(cat["id"], ind["id"])] = ind["direction"]
    return out


def aggregate_effects(claims: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """Effekt-claims -> indicator_effects. net_support i [-1,1], confidence i [0,1].

    TVÅ LED, eftersom en cell blandar två väsensskilda slags poster (ADR 0019 beslut 1):

        inom åtgärdstypen:   x_t = Σ(q·m) / Σ q          POOLNING
        över åtgärdstyper:   net = clip(Σ_t x_t / K)     SUMMA,  K = R × max(effect_strength)

    Flera utvärderingar av SAMMA åtgärdstyp är upprepade mätningar av EN storhet, så de poolas
    kvalitetsviktat: en andra studie som finner en mindre effekt ska sänka skattningen av just
    den åtgärdens effekt. Det är att lära av data och inget monotonicitetsbrott. Flera
    ÅTGÄRDSTYPER är skilda ingrepp med var sin effekt på samma indikator, så deras bidrag
    summeras: en ytterligare åtgärd som bevisligen fungerar ska alltid höja talet.

    Kvoten var aldrig fel i sig. Den användes över fel enheter, och ADR 0018 namngav bara den
    ena halvan av felet.

    `q` är därmed RELATIV POOLNINGSVIKT och aldrig amplitudfaktor: en ensam utvärdering av en
    åtgärdstyp ger x_t = m, alltså exakt sin egen effektstyrka med tecken. Det är den egenskapen
    som håller ADR 0004 beslut 2 sant, alltså att effect_strength bär storleken medan
    evidence_level och confidence bär säkerheten.

    mixed/unclear ger m = 0 men behåller sitt q inom typen, alltså drar en källa som säger
    "oklart" sin egen åtgärdstyp mot noll; effect_strength unknown beter sig likadant. Fältet
    confidence är oförändrat ett medel av claimens confidence och bär osäkerheten kring
    storleken (scorerun läser det till B:s säkerhetsnivå).
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

    # K = R × m_max. R är mättnadsbredden och står i configen, låst i modellversionen
    # (ADR 0019 beslut 4). m_max räknas ur tabellen och skrivs aldrig in som konstant.
    r = int(config.scoring()["B_evidens"]["saturation_action_types"])
    if r < 1:
        raise config.ConfigError(f"B_evidens.saturation_action_types måste vara >= 1, är {r}")
    k_budget = r * max(num["effect_strength"].values())

    effects: list[dict[str, Any]] = []
    for (party, cat, ind), cs in groups.items():
        conf_vals: list[float] = []
        supporting: list[str] = []
        contradicting: list[str] = []
        per_type: dict[str, list[tuple[float, float]]] = {}
        for c in cs:
            conf_num = num["confidence"].get(c.get("confidence", "low"), 0.0)
            # q = kvalitet: vems storlek man tror på. m = storlek med tecken, i [-1, 1].
            q = ev_levels.get(c.get("evidence_level", ""), 0.0) * conf_num
            s = signed.get(c.get("direction", "unclear"), 0)
            m = num["effect_strength"].get(c.get("effect_strength", "unknown"), 0.0) * s
            policy = c.get("policy_type")
            if not policy:
                # Utan grupperingsnyckel går formen inte att räkna. Hård fail, aldrig en
                # tyst hopslagning av skilda ingrepp (ADR 0019 beslut 1).
                raise config.ConfigError(
                    f"claim saknar policy_type och kan inte grupperas: {c.get('id')}"
                )
            per_type.setdefault(policy, []).append((q, m))
            conf_vals.append(conf_num)
            (supporting if s >= 0 else contradicting).append(c.get("id", ""))

        x_sum = 0.0
        for policy, qm in per_type.items():
            q_t = sum(q for q, _ in qm)
            if q_t <= 0:
                # Onåbart under den symmetriska grinden (minsta admissibla q är 0,48), men
                # regeln skrivs ändå: hård fail, aldrig en tyst nolla (ADR 0019 beslut 8).
                raise config.ConfigError(
                    f"Σq = 0 för åtgärdstypen {policy} i {party}/{cat}/{ind}: "
                    "poolningen är odefinierad"
                )
            x_sum += sum(q * m for q, m in qm) / q_t
        net = max(-1.0, min(1.0, x_sum / k_budget)) if per_type else 0.0
        conf = sum(conf_vals) / len(conf_vals) if conf_vals else 0.0
        effects.append({
            "party": party, "category": cat, "indicator": ind,
            "expected_direction": directions.get((cat, ind), "up"),
            "net_support": round(net, 4), "confidence": round(conf, 4),
            "supporting_claims": [s for s in supporting if s],
            "contradicting_claims": [c for c in contradicting if c],
        })
    return effects
