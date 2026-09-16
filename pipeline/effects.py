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

    mixed/unclear ger m = 0 men behåller sitt q inom typen, alltså drar en källa som fann oklar
    VERKAN sin egen åtgärdstyp mot noll. Okänd STORLEK är något annat och står UTANFÖR hela
    formen (ADR 0020 beslut 10): okänd effektstorlek är frånvaro av en skattning, aldrig en
    skattning om exakt neutral verkan, så en sådan post får varken täljare eller nämnare. Bär
    cellen minst en storlek redovisas den storlekslösa posten under `size_unknown_claims`. Bär
    ingen post i cellen en storlek finns cellen inte alls, och då finns heller inget fält att
    redovisa den i: källspåret ligger kvar i claimet och i dist/evidence.json, aldrig i ett
    indicator_effect utan tal. Regeln har noll medlemmar i dag och skrevs före dem, som ADR
    0003 punkt 1 kräver.

    Fältet confidence är oförändrat ett medel av claimens confidence och bär osäkerheten kring
    storleken (scorerun läser det till B:s säkerhetsetikett).
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
        size_unknown: list[str] = []
        per_type: dict[str, list[tuple[float, float]]] = {}
        for c in cs:
            policy = c.get("policy_type")
            if not policy:
                # Utan grupperingsnyckel går formen inte att räkna. Hård fail, aldrig en
                # tyst hopslagning av skilda ingrepp (ADR 0019 beslut 1).
                raise config.ConfigError(
                    f"claim saknar policy_type och kan inte grupperas: {c.get('id')}"
                )
            strength = c.get("effect_strength", "unknown")
            if strength == "unknown":
                # ADR 0020 beslut 10: frånvaro av skattning, aldrig en skattning om neutral
                # verkan. Posten lämnar både täljare och nämnare och räknas som dokumentation.
                size_unknown.append(c.get("id", ""))
                continue
            if strength not in num["effect_strength"]:
                raise config.ConfigError(
                    f"claim {c.get('id')} bär effect_strength {strength!r}, som saknas i "
                    "claims.yaml numeric.effect_strength: storleken går inte att mappa"
                )
            conf_num = num["confidence"].get(c.get("confidence", "low"), 0.0)
            # q = kvalitet: vems storlek man tror på. m = storlek med tecken, i [-1, 1].
            q = ev_levels.get(c.get("evidence_level", ""), 0.0) * conf_num
            s = signed.get(c.get("direction", "unclear"), 0)
            m = num["effect_strength"][strength] * s
            per_type.setdefault(policy, []).append((q, m))
            conf_vals.append(conf_num)
            (supporting if s >= 0 else contradicting).append(c.get("id", ""))

        if not per_type:
            # Ingen post i cellen bär en storlek, alltså finns cellen inte i B_rått. Den står
            # utanför medlet i stället för att dra det mot neutral (ADR 0020 beslut 10).
            continue

        x_sum = 0.0
        sign_conflict: list[str] = []
        for policy, qm in per_type.items():
            q_t = sum(q for q, _ in qm)
            if q_t <= 0:
                # Onåbart under den symmetriska grinden (minsta admissibla q är 0,48), men
                # regeln skrivs ändå: hård fail, aldrig en tyst nolla (ADR 0019 beslut 8).
                raise config.ConfigError(
                    f"Σq = 0 för åtgärdstypen {policy} i {party}/{cat}/{ind}: "
                    "poolningen är odefinierad"
                )
            # ADR 0019 beslut 8, andra halvan: utvärderingar inom EN typ som är oense om
            # tecknet bär en RENT DESKRIPTIV flagga. Poolen medelvärdesbildar dem, så utan
            # flaggan syns oenigheten inte alls. Ingen automatisk verkan: en nedgradering av
            # säkerheten avvisades som ospecificerad, eftersom den lämnar öppet hur svag en
            # motröst får vara och om +0,01 mot -0,01 är samma konflikt som +1 mot -1.
            # m = 0 (mixed/unclear/unknown) är ingen motröst och räknas inte som oenighet.
            if len({m > 0 for _, m in qm if m}) > 1:
                sign_conflict.append(policy)
            x_sum += sum(q * m for q, m in qm) / q_t
        # ADR 0019 beslut 7: klippningen döljer hur stort det oklippta överskottet var, så
        # summan redovisas diagnostiskt. Talet är x_sum/K, alltså exakt det net klipper.
        unclipped = x_sum / k_budget if per_type else 0.0
        net = max(-1.0, min(1.0, unclipped))
        conf = sum(conf_vals) / len(conf_vals) if conf_vals else 0.0
        effects.append({
            "party": party, "category": cat, "indicator": ind,
            "expected_direction": directions.get((cat, ind), "up"),
            "net_support": round(net, 4), "confidence": round(conf, 4),
            "net_support_unclipped": round(unclipped, 4),
            "sign_conflict_types": sorted(sign_conflict),
            "supporting_claims": [s for s in supporting if s],
            "contradicting_claims": [c for c in contradicting if c],
            "size_unknown_claims": [s for s in size_unknown if s],
        })
    return effects
