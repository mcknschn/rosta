"""Deterministisk betygsmatematik (delpoäng -> kategoribetyg -> totalpoäng + osäkerhet).

Rena funktioner utan beroende på livedata, så de kan golden-testas direkt.
Den datadrivna populeringen av A/B/C/D byggs i Fas 4-5; matten nedan är kontraktet.

Kategoribetyg = 0.40*A + 0.35*B + 0.15*C + 0.10*D     (A,B,C,D i [0,5])

Skalsemantik (se scoring.yaml): A och C är RELATIVA (rangordnas över de 8 partierna),
B och D är ABSOLUTA (net_support=0 -> 2.5 oberoende av andra partier).
"""

from __future__ import annotations

import re
from collections.abc import Mapping

from . import config

SUBSCORES = ("A", "B", "C", "D")


def clamp(x: float, lo: float = 0.0, hi: float = 5.0) -> float:
    return max(lo, min(hi, x))


def weighted_category_score(components: Mapping[str, float], weights: Mapping[str, float]) -> float:
    """Viktad summa av delpoängen A/B/C/D. Validerar både components och weights."""
    for name, m in (("delpoäng", components), ("vikter", weights)):
        missing = set(SUBSCORES) - m.keys()
        if missing:
            raise ValueError(f"Saknar {name}: {sorted(missing)}")
    return clamp(sum(components[k] * weights[k] for k in SUBSCORES))


# --- Normalisering (relativa delpoäng) ------------------------------------------

def minmax_normalize(
    values: Mapping[str, float], lo: float = 0.0, hi: float = 5.0, neutral: float = 2.5
) -> dict[str, float]:
    """Skalar partivärden till [lo, hi]. Vid noll spridning faller alla på neutral."""
    if not values:
        return {}
    vmin, vmax = min(values.values()), max(values.values())
    if vmax - vmin == 0:
        return {k: neutral for k in values}
    span = vmax - vmin
    return {k: lo + (v - vmin) / span * (hi - lo) for k, v in values.items()}


def rank_normalize(
    values: Mapping[str, float], lo: float = 0.0, hi: float = 5.0, neutral: float = 2.5
) -> dict[str, float]:
    """Rangordnar partivärden till [lo, hi] (medelrang vid lika). Outlier-robust."""
    if not values:
        return {}
    n = len(values)
    if n == 1:
        return {k: neutral for k in values}
    ordered = sorted(values.items(), key=lambda kv: kv[1])
    keys = [k for k, _ in ordered]
    vals = [v for _, v in ordered]
    if vals[0] == vals[-1]:
        return {k: neutral for k in values}
    ranks: dict[str, float] = {}
    i = 0
    while i < n:
        j = i
        while j + 1 < n and vals[j + 1] == vals[i]:
            j += 1
        avg = (i + j) / 2
        for t in range(i, j + 1):
            ranks[keys[t]] = avg
        i = j + 1
    return {k: lo + ranks[k] / (n - 1) * (hi - lo) for k in values}


def normalize(values: Mapping[str, float], method: str = "minmax", **kw: float) -> dict[str, float]:
    """Dispatch på normaliseringsmetod (minmax | rank) enligt scoring.yaml."""
    if method == "rank":
        return rank_normalize(values, **kw)
    if method == "minmax":
        return minmax_normalize(values, **kw)
    raise ValueError(f"Okänd normaliseringsmetod: {method!r}")


# --- B-rollup (absolut delpoäng) ------------------------------------------------

def net_support_to_score(net_support: float) -> float:
    """net_support i [-1, 1] -> betyg i [0, 5] (linjärt). 0 -> 2.5."""
    return clamp(5.0 * (net_support + 1.0) / 2.0)


def aggregate_B(
    indicator_net_support: Mapping[str, float | None],
    indicator_weights: Mapping[str, float],
    missing_all_score: float = 2.5,
) -> float:
    """B per kategori = submåttsviktat medel av indikatorernas net_support_to_score.

    Indikatorer med None (saknad effekt) utelämnas. Saknas alla -> missing_all_score.
    """
    present = {k: v for k, v in indicator_net_support.items() if v is not None}
    wsum = sum(indicator_weights.get(k, 0.0) for k in present)
    if not present or wsum == 0:
        return missing_all_score
    return clamp(
        sum(net_support_to_score(present[k]) * indicator_weights.get(k, 0.0) for k in present) / wsum
    )


def submeasure_weighted_mean(
    values: Mapping[str, float | None], weights: Mapping[str, float]
) -> float | None:
    """Viktat medel där None-poster utelämnas. None om inget värde/vikt finns.

    Generisk submåttsupprullning (B och D delar den). Skiljer sig från aggregate_B
    genom att returnera None (ej en neutral fallback) när underlag saknas — anroparen
    avgör vad "saknas" ska bli.
    """
    present = {k: v for k, v in values.items() if v is not None}
    wsum = sum(weights.get(k, 0.0) for k in present)
    if not present or wsum == 0:
        return None
    return sum(v * weights.get(k, 0.0) for k, v in present.items()) / wsum


# --- D-attribution (absolut delpoäng): rörde sig indikatorn rätt under partiets ansvar? ---

_YEAR_RE = re.compile(r"^(\d{4})(?:-(\d{4}))?$")


def period_to_year(period: str) -> int | None:
    """Tolkar en observations-period till ett ENSKILT kalenderår för D-attribution.

    'YYYY' -> året. 'YYYY-YYYY' med samma start och slut (SCB:s enkelår, t.ex. '2021-2021')
    -> det året. Äkta flerårsspann ('2018-2019', SCB:s ULF-dubbelår) är ett tvåårsmedelvärde,
    inte en enskild årspunkt, och ger None — annars skulle det bilda en falsk år-för-år-
    förändring mot en intilliggande enkelårspunkt vid kadensbytet. Månads-/kvartalsperioder
    ('YYYYMmm', 'YYYYKn') saknar också årsupplösning och ger None.
    """
    m = _YEAR_RE.match(str(period).strip())
    if not m:
        return None
    start, end = m.group(1), m.group(2)
    if end is not None and end != start:
        return None  # äkta flerårsspann -> ingen enskild årsupplösning
    return int(start)


def relative_change(v_prev: float, v: float) -> float | None:
    """Relativ årsförändring (v - v_prev) / |v_prev|. None om v_prev == 0 (odefinierad)."""
    if v_prev == 0:
        return None
    return (v - v_prev) / abs(v_prev)


def direction_adjusted_change(v_prev: float, v: float, direction: str) -> float | None:
    """Relativ förändring justerad för indikatorns positiva riktning.

    Positivt = förbättring oavsett om indikatorn ska upp eller ned. 'target'-indikatorer
    saknar definierad målnivå och returnerar None (kan inte poängsättas som förbättring).
    """
    rc = relative_change(v_prev, v)
    if rc is None:
        return None
    if direction == "up":
        return rc
    if direction == "down":
        return -rc
    return None  # target: ingen mållnivå -> ej poängsättbar i D


def change_sign(adjusted: float, dead_zone: float) -> int:
    """Tecken på en riktningsjusterad förändring med en relativ dödzon (brusgräns)."""
    if adjusted > dead_zone:
        return 1
    if adjusted < -dead_zone:
        return -1
    return 0


def attribute_series(
    series: Mapping[int, float],
    direction: str,
    year_power: Mapping[int, Mapping[str, float]],
    party: str,
    lag: int,
    dead_zone: float,
) -> tuple[float | None, float]:
    """Viktat teckenmedel av en indikators årsförändringar under partiets ansvarsår.

    series: {år -> värde} (nationell årsserie). year_power: {år -> {parti -> maktvikt 0-1}}.
    En förändring mellan konsekutiva år (y-1 -> y) tillskrivs regeringen som satt år
    (y - lag), viktad med dess maktvikt. Returnerar (net i [-1,1] eller None om partiet
    saknar ansvarsunderlag, total_ansvarsvikt). Bara konsekutiva år används (ingen
    interpolation), och target-indikatorer ger None.
    """
    years = sorted(series)
    num = 0.0
    den = 0.0
    for i in range(1, len(years)):
        y_prev, y = years[i - 1], years[i]
        if y - y_prev != 1:
            continue  # hoppa över glapp i serien
        adj = direction_adjusted_change(series[y_prev], series[y], direction)
        if adj is None:
            continue
        weight = year_power.get(y - lag, {}).get(party, 0.0)
        if weight <= 0:
            continue
        num += weight * change_sign(adj, dead_zone)
        den += weight
    if den == 0:
        return None, 0.0
    return num / den, den


# --- Osäkerhet (datadriven) -----------------------------------------------------

def resolve_confidence_numeric(
    default_levels: Mapping[str, str],
    confidence_numeric: Mapping[str, float],
    overrides: Mapping[str, str] | None = None,
) -> dict[str, float]:
    """Löser per-delpoäng-säkerhet (nivå -> tal). overrides per (parti,kategori) vinner."""
    overrides = overrides or {}
    out: dict[str, float] = {}
    for letter in SUBSCORES:
        level = overrides.get(letter, default_levels[letter])
        out[letter] = confidence_numeric[level]
    return out


def category_uncertainty_halfwidth(
    subscore_weights: Mapping[str, float],
    resolved_confidence: Mapping[str, float],
    max_halfwidth: float,
) -> float:
    """Halvbredd = max_halfwidth * Σ vikt*(1 - säkerhet). Aldrig negativ."""
    hw = max_halfwidth * sum(
        subscore_weights[k] * (1.0 - resolved_confidence[k]) for k in SUBSCORES
    )
    return max(0.0, hw)


def confidence_interval(score: float, halfwidth: float) -> list[float]:
    return [clamp(score - halfwidth), clamp(score + halfwidth)]


def total_score(category_scores: Mapping[str, float], user_weights: Mapping[str, float]) -> float:
    """Väljarens viktade totalpoäng (client-side-beräkningen). Vikterna normaliseras."""
    if any(user_weights.get(c, 0.0) < 0 for c in category_scores):
        raise ValueError("Negativa kategorivikter är inte tillåtna")
    wsum = sum(user_weights.get(c, 0.0) for c in category_scores)
    if wsum <= 0:
        raise ValueError("Kategorivikterna måste summera till ett positivt tal")
    return clamp(sum(category_scores[c] * user_weights.get(c, 0.0) for c in category_scores) / wsum)


# --- Bekvämlighetsomslag som läser regler ur config/scoring.yaml -----------------

def category_score_from_components(
    components: Mapping[str, float],
    confidence_overrides: Mapping[str, str] | None = None,
    flags: list[str] | None = None,
) -> dict[str, object]:
    """Räknar kategoribetyg + datadrivet osäkerhetsintervall enligt config/scoring.yaml.

    confidence_overrides: per-delpoäng-nivå som överskrider defaults (t.ex. {"B": "low"}
    när effekter saknas, {"D": "low"} vid not_applicable, {"C": "medium"} vid saknad subnational).
    flags: markörer som följer med i utdata (t.ex. ["D_not_applicable"]).
    """
    for k in SUBSCORES:
        if not (0.0 <= components[k] <= 5.0):
            raise ValueError(f"Delpoäng {k} utanför [0,5]: {components[k]}")
    sc = config.scoring()
    weights = sc["subscore_weights"]
    unc = sc["uncertainty"]
    defaults = unc["default_subscore_certainty"]
    score = weighted_category_score(components, weights)
    resolved = resolve_confidence_numeric(defaults, unc["confidence_numeric"], confidence_overrides)
    halfwidth = category_uncertainty_halfwidth(weights, resolved, unc["max_interval_halfwidth"])
    result: dict[str, object] = {
        "score": round(score, 3),
        "ci": [round(x, 3) for x in confidence_interval(score, halfwidth)],
        "components": {k: round(components[k], 3) for k in SUBSCORES},
        "confidence": {k: (confidence_overrides or {}).get(k, defaults[k]) for k in SUBSCORES},
    }
    result["flags"] = list(flags) if flags else []
    return result
