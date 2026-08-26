"""Deterministisk betygsmatematik (delpoäng -> kategoribetyg -> totalpoäng + osäkerhet).

Rena funktioner utan beroende på livedata, så de kan golden-testas direkt.
Den datadrivna populeringen av A/B/C/D byggs i Fas 4-5; matten nedan är kontraktet.

Kategoribetyg = 0.30*A + 0.50*B + 0.20*D              (A,B,D i [0,5])
C väger 0 och ger inga poäng. Den räknas ut som förut och redovisas som maktandel
(ADR 0002). Vikterna läses ur scoring.yaml, aldrig härifrån.

Skalsemantik (se scoring.yaml): C är RELATIV (rangordnas över de 8 partierna). A, B och D är
ABSOLUTA (net_support=0 -> 2.5 oberoende av andra partier). A blev absolut i ADR 0005: dess båda
halvor mäts mot en historisk förankring med bounded_quotient och avbildas med
net_support_to_score, samma avbildning som B.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from collections.abc import Set as AbstractSet

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

def bounded_quotient(share: float, anchor: float) -> float:
    """Andel mot förankring som en begränsad kvot: (andel - förankring) / (andel + förankring).

    A:s form efter ADR 0005 punkt 3. Kvoten ligger i [-1, 1] av konstruktion och är 0 vid
    jämnhöjd, alltså precis den storhet net_support_to_score redan avbildar på [0, 5]. Ingen
    konstant väljs. Måttet mättar mjukt: tre gånger förankringen ger 0,50 och fem gånger 0,67,
    en deklarerad kostnad i ADR 0005.

    Båda talen är andelar och därför icke-negativa; ett negativt tal är ett fel i underlaget och
    ger hård fail (aldrig en tyst kvot utanför intervallet). Saknas underlag helt (båda 0) finns
    ingen kvot, och 0 betyder då jämnhöjd.
    """
    if share < 0 or anchor < 0:
        raise ValueError(f"Andel och förankring måste vara >= 0, fick {share} och {anchor}")
    total = share + anchor
    if total == 0:
        return 0.0
    return (share - anchor) / total


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


def coverage_shrink(raw: float, coverage: float, neutral: float = 2.5) -> float:
    """Krymper ett betyg mot neutral proportionellt mot täckning i [0,1].

    coverage=1 -> oförändrat, coverage=0 -> neutral. Samma matte som B:s inline-krympning
    (scorerun) och ekvivalent med D:s neutral-missing-rollup (se spec §3.3) eftersom
    net_support_to_score är linjär.
    """
    return neutral + (raw - neutral) * coverage


def weighted_mean_with_neutral_missing(
    values: Mapping[str, float],
    weights: Mapping[str, float],
    denominator_keys: Iterable[str],
    neutral: float = 0.0,
) -> float | None:
    """Viktat medel över en FAST nämnare där saknade keys bidrar med neutral.

    Till skillnad från submeasure_weighted_mean (som renormaliserar över närvarande keys)
    behåller denna hela nämnaren: saknad bredd drar mot neutral i stället för att försvinna.
    Keys i values utanför nämnaren ignoreras. None om nämnarens totalvikt är 0.
    """
    den = list(denominator_keys)
    wsum = sum(weights.get(k, 0.0) for k in den)
    if wsum == 0:
        return None
    return sum(weights.get(k, 0.0) * values.get(k, neutral) for k in den) / wsum


def weighted_depth_coverage(
    coded: Mapping[str, AbstractSet[str]],
    codable: Mapping[str, AbstractSet[str]],
    weights: Mapping[str, float],
    denominator_keys: Iterable[str],
) -> tuple[float, float]:
    """(covered_weight, total_weight) för viktad undermåttsdjuptäckning (B5-spec §3.3).

    covered_weight = Σ w_s · |K_s| / |T_s| över en FAST nämnare (denominator_keys), där
    T_s = kodbara åtgärdstyper i undermåttet och K_s = partiets kodade av dem (K_s snittas
    mot T_s — typer utanför den kodbara mängden kan aldrig bidra). Undermått utan kodbar
    typ (T_s = ∅, B-vägg) bidrar 0 i täljaren men behåller sin vikt i nämnaren: B vet
    faktiskt ingenting om den delen av kategorianspråket. Undermått utanför nämnaren
    (helt uteslutna, ADR 0011) ignoreras helt, även om de har kodade typer (spec §3.6). Mängdsemantiken
    gör måttet dedup-säkert: dubblerade liggarposter inom samma undermått ändrar varken
    |T_s| eller |K_s| (spec §7, anti-gaming).
    """
    covered = 0.0
    total = 0.0
    for s in denominator_keys:
        w = weights.get(s, 0.0)
        total += w
        t_s = codable.get(s) or frozenset()
        if not t_s:
            continue
        k_s = set(coded.get(s) or frozenset()) & set(t_s)
        covered += w * len(k_s) / len(t_s)
    return covered, total


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


_SUBYEAR_RE = re.compile(r"^(\d{4})[A-Za-z]\d+$")  # 'YYYYMmm', 'YYYYKn'


def period_end_year(period: str) -> int | None:
    """Sista kalenderår en period TÄCKER. None om perioden saknar årtal.

    Ligger bredvid period_to_year för att de två läsningarna ska drifta synligt: samma
    periodsträng, olika frågor. period_to_year ger det ENSKILDA år en period får bilda en
    årsförändring för, så ett äkta dubbelår ger None. Här räcker serien ändå fram till
    dubbelårets slutår, så '2018-2019' ger 2019 och en månads-/kvartalsperiod ger sitt år.
    Används av scorerun.data_freshness för meta.data_as_of, aldrig i betygslogiken.
    """
    s = str(period).strip()
    m = _YEAR_RE.match(s)
    if m:
        return int(m.group(2) or m.group(1))
    m = _SUBYEAR_RE.match(s)
    return int(m.group(1)) if m else None


def relative_change(v_prev: float, v: float) -> float | None:
    """Relativ årsförändring (v - v_prev) / |v_prev|. None om v_prev == 0 (odefinierad)."""
    if v_prev == 0:
        return None
    return (v - v_prev) / abs(v_prev)


def direction_adjusted_change(v_prev: float, v: float, direction: str) -> float | None:
    """Relativ förändring justerad för indikatorns positiva riktning.

    Positivt = förbättring oavsett om indikatorn ska upp eller ned. Riktningen håller bara
    upp och ned (ADR 0011 punkt 3); ett tredje värde är ett fel i configen och hard-failar
    här i stället för att tyst ge None. En UTESLUTEN indikator når aldrig funktionen: den
    har ingen riktning, står därför inte i scorerun._indicator_meta, och har ingen serie
    att attribuera.
    """
    rc = relative_change(v_prev, v)
    if rc is None:
        return None
    if direction == "up":
        return rc
    if direction == "down":
        return -rc
    raise ValueError(f"Okänd riktning {direction!r} (tillåtna: up, down)")


def change_sign(adjusted: float, dead_zone: float) -> int:
    """Tecken på en riktningsjusterad förändring med en relativ dödzon (brusgräns)."""
    if adjusted > dead_zone:
        return 1
    if adjusted < -dead_zone:
        return -1
    return 0


def attribute_subnational_indicator(
    series_by_region: Mapping[str, Mapping[int, float]],
    direction: str,
    region_year_power: Mapping[str, Mapping[int, Mapping[str, float]]],
    party: str,
    lag: int,
    dead_zone: float,
) -> tuple[float | None, float, int]:
    """Region-poolat teckenmedel för EN indikator (C3 — subnationell D).

    Som attribute_series men över FLERA regioner: varje regions konsekutiva årsförändring
    tillskrivs det parti som styrde DEN regionen år (y-lag), viktat med dess regionala maktvikt
    (region_year_power[region][år][parti], 1/antal styrande partier). num/den ackumuleras över
    alla regioner med EQUAL per-region-vikt (ej befolkningsviktat — neutralt, jfr regional_fractions).

    Returnerar (net i [-1,1] eller None, den_raw, n_regions_med_data) där:
      - den_raw = Σ regional maktvikt över attribuerade region-år (rå, EJ år-ekvivalent),
      - n_regions_med_data = regioner med >=1 brukbar konsekutiv årsförändring (oavsett partiets
        makt) -> nämnaren när anroparen normaliserar den_raw till ÅR-EKVIVALENT basis (den_raw /
        n_regions), så D-grindens trösklar behåller samma skala som nationellt.
    """
    num = 0.0
    den = 0.0
    n_regions = 0
    for code, series in series_by_region.items():
        years = sorted(series)
        ryp = region_year_power.get(code, {})
        region_has_change = False
        for i in range(1, len(years)):
            y_prev, y = years[i - 1], years[i]
            if y - y_prev != 1:
                continue
            adj = direction_adjusted_change(series[y_prev], series[y], direction)
            if adj is None:
                continue
            region_has_change = True
            weight = ryp.get(y - lag, {}).get(party, 0.0)
            if weight <= 0:
                continue
            num += weight * change_sign(adj, dead_zone)
            den += weight
        if region_has_change:
            n_regions += 1
    net = num / den if den > 0 else None
    return net, den, n_regions


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
    interpolation).
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


# Täckningen räknar A, B och D. C har ingen täckningsstorhet (ADR 0008 punkt 2).
COVERAGE_SUBSCORES = ("A", "B", "D")


def cell_coverage(a: float, b: float, d: float) -> float:
    """Cellens TÄCKNING: hur stor del av betyget som vilar på mätt underlag (ADR 0008).

    a, b och d är per-delpoängstäckningen i [0,1], var och en räknad på kategorins EGEN
    nämnare. Vikterna är ADR 0002:s delpoängvikter ur config/scoring.yaml, aldrig valda tal
    här. De tre summerar redan till 1,00 eftersom C väger 0, så ingen omnormalisering behövs.

    Storheten säger inget om hur säkert det mätta är. Det beskedet bär bandet, och de två
    hålls isär (ADR 0008 punkt 1). Täckningen har heller ingen verkan på betyget (punkt 7):
    den räknas ur färdiga tal och matas aldrig tillbaka in i score, ci eller components.

    Att de tre summerar till 1,00 är ett drag hos den COMMITTADE configen, inte hos formeln.
    Grinden på det står i tests/test_cell_coverage.py, inte här: pipeline.robustness kör
    scenariot "gamla vikter" med C = 0,15, och ett hårt fall här skulle spränga en känslighets-
    körning som varken läser eller skriver täckningen.
    """
    parts = dict(zip(COVERAGE_SUBSCORES, (a, b, d), strict=True))
    for k, v in parts.items():
        if not (0.0 <= v <= 1.0):
            raise ValueError(f"Täckning {k} utanför [0,1]: {v}")
    weights = config.scoring()["subscore_weights"]
    return round(sum(weights[k] * v for k, v in parts.items()), 3)
