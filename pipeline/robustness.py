"""ADR 0003 / biljett #20: skiljbarhet mätt som ordningens stabilitet.

Bandöverlappet är inget skiljbarhetstest. Halvbredden är `max_halfwidth x Σ vikt x
(1 - säkerhet)` och varierar bara med deklarerad säkerhetsnivå, aldrig med spridningen i
underlaget. Att två sådana band går omlott säger därför ingenting om just det partiparet.

Det här verktyget mäter i stället **andelen metodvarianter där två partiers inbördes ordning
håller**. Monte Carlo bär statistiken: alla osäkra val dras samtidigt (ADR 0003 punkt 4), så
körningen kan svara på vilket reglage som dominerar. Ett reglage är en dragen variationspunkt
(ADR 0010 punkt 8); nycklarna `SOURCES`, `Source` och `source_influence` står kvar tills en
schemaändring ändå görs, så att ordbytet inte drar med sig ett gränssnittsbrott. Sju namngivna
scenarier körs var för sig och bär kommunikationen; scenario 6 och 7 är FILTER som byter vad
indexet mäter och redovisas skilt (punkt 9).

Byggt som `pipeline/tools/c3_sensitivity.py`: kopiera `config.scoring()` och `config.claims()`,
ändra i minnet, monkeypatcha loaderna och kör `scorerun.build(con)`. Ingen fil på disk ändras.
Analysen DRAR `numeric.effect_strength`, den ÄNDRAR den aldrig (ADR 0004 punkt 4).

Ingen tröskel (ADR 0003 punkt 3). Andelen redovisas som den är. Ökad separation är aldrig ett
mål (punkt 1).

    python -m pipeline.robustness                    # 10 000 dragningar -> dist/robustness.json
    python -m pipeline.robustness --draws 200        # snabb rökkörning
"""

from __future__ import annotations

import argparse
import copy
import json
import math
import random
import sys
import time
from collections.abc import Callable, Iterable, Sequence
from datetime import date
from typing import Any, NamedTuple

from . import DIST_DIR, config, schema, scorerun, warehouse

# Fast seed -> körningen är reproducerbar. Ändras aldrig utan att diffen redovisas.
SEED = 20260821
N_DRAWS = 10_000          # statistiken räknas på så här många dragningar
N_DRAWS_SHIPPED = 2_000   # så här många kategorimatriser skickas till webbläsaren
N_INFLUENCE_BINS = 4      # kvartilfack för kontinuerliga reglage (diskreta får sina alternativ)

# --- Spannregeln (ADR 0003 punkt 6) ---------------------------------------------------
# Diskreta val får sina BYGGDA alternativ, varken fler eller färre. Kontinuerliga parametrar
# får ett spann som täcker varje värde repot faktiskt använt eller dokumenterat som alternativ,
# plus en symmetrisk marginal. Två regler räcker för hela tabellen nedan:
#
#   R1  ett enda använt värde v      -> [v/2, 3v/2], alltså v ± 50 procent.
#   R2  en nivåtabell med flera tal  -> varje tal ± 40 procent av det MINSTA avståndet mellan
#                                       talen. 2 x 0,40 < 1, så facken kan aldrig gå omlott och
#                                       ordningen låg < medel < hög håller i varje dragning.
#
# Ett undantag, uttryckligen begärt i ADR 0003 punkt 6: `max_interval_halfwidth` får ett brett
# spann just för att 1,5 saknar härledning. Det står som R3 nedan.
_R1 = "R1: enda använda värdet ± 50 procent"
_R2_ES = "R2: ± 0,12 (40 procent av minsta avståndet 0,30) — ordningen låg < medel < hög håller"
_R2_CN = "R2: ± 0,10 (40 procent av minsta avståndet 0,25) — ordningen låg < medel < hög håller"
_R3 = "R3: brett spann, 1,5 ± 1,0, eftersom 1,5 saknar härledning (ADR 0003 punkt 6)"
_BUILT = "byggda alternativ"


def _span(value: float, frac: float = 0.5) -> tuple[float, float]:
    """R1: symmetrisk marginal kring det enda värde repot använt."""
    return (value * (1 - frac), value * (1 + frac))


class Source(NamedTuple):
    """Ett draget reglage: namn, spann eller alternativlista, och hur det skrivs in."""

    name: str
    kind: str                                   # "range" | "choice" | "simplex"
    spec: Any                                   # (lo, hi) | tuple av alternativ | None
    note: str                                   # varför spannet ser ut så
    apply: Callable[[Any, dict, dict], None]    # (värde, scoring, claims) -> None
    bin_key: Callable[[Any], float] | None = None   # skalär för kvartilfacken (simplex)
    band_only: bool = False                     # rör bara bandet, aldrig betyget -> nollkontroll


def _set_weights(v: tuple[float, float, float], sc: dict, _cl: dict) -> None:
    a, b, d = v
    sc["subscore_weights"] = {"A": a, "B": b, "C": 0.0, "D": d}


def _set_halfwidth(v: float, sc: dict, _cl: dict) -> None:
    sc["uncertainty"]["max_interval_halfwidth"] = v


def _set_conf(level: str) -> Callable[[Any, dict, dict], None]:
    """confidence_numeric är EN storhet med två kopior i configen.

    tests/test_config.py låser att claims.yaml numeric.confidence och scoring.yaml
    uncertainty.confidence_numeric håller samma tal. Dragningen skriver därför båda, annars
    skulle analysen pröva ett tillstånd repot förbjuder.
    """
    def apply(v: float, sc: dict, cl: dict) -> None:
        sc["uncertainty"]["confidence_numeric"][level] = v
        cl["numeric"]["confidence"][level] = v
    return apply


def _set_default_certainty(v: str, sc: dict, _cl: dict) -> None:
    sc["uncertainty"]["default_subscore_certainty"]["A"] = v


def _set_component_mix(v: float, sc: dict, _cl: dict) -> None:
    """Skriver BÅDA nycklarna: bara den ena vore ett par som inte summerar till 1."""
    comps = sc["A_agerande"]["components"]
    comps["a1_budgetprioritering"] = v
    comps["a2_lagstiftningsprioritering"] = 1 - v


def _set_effect_strength(level: str) -> Callable[[Any, dict, dict], None]:
    def apply(v: float, _sc: dict, cl: dict) -> None:
        cl["numeric"]["effect_strength"][level] = v
    return apply


def _set_d(key: str) -> Callable[[Any, dict, dict], None]:
    def apply(v: Any, sc: dict, _cl: dict) -> None:
        sc["D_resultat"][key] = v
    return apply


def _set_b(key: str) -> Callable[[Any, dict, dict], None]:
    def apply(v: Any, sc: dict, _cl: dict) -> None:
        sc["B_evidens"][key] = v
    return apply


def _set_subnational(key: str) -> Callable[[Any, dict, dict], None]:
    def apply(v: Any, sc: dict, _cl: dict) -> None:
        sc["D_resultat"]["subnational"][key] = v
    return apply


SOURCES: tuple[Source, ...] = (
    # Delpoängvikterna dras ur den mängd ADR 0002:s härledning tillåter: B störst, A näst,
    # D minst, C noll. Likformigt på simplexet, sedan sorterat -> analysen prövar härledningens
    # slutsats i stället för en godtycklig omviktning (ADR 0003 punkt 6).
    Source("subscore_weights", "simplex", None,
           f"{_BUILT}: B > A > D > 0, C = 0, summa 1 (ADR 0002). Likformigt på simplexet.",
           _set_weights, bin_key=lambda v: v[0]),
    Source("max_interval_halfwidth", "range", (0.5, 2.5), _R3, _set_halfwidth, band_only=True),
    Source("confidence_numeric.high", "range", (0.75, 0.95), _R2_CN, _set_conf("high")),
    Source("confidence_numeric.medium", "range", (0.50, 0.70), _R2_CN, _set_conf("medium")),
    Source("confidence_numeric.low", "range", (0.20, 0.40), _R2_CN, _set_conf("low")),
    # default_subscore_certainty: scorerun sätter ALLTID en override för B, C och D per cell,
    # så bara A:s defaultnivå kan nå ett band. B/C/D lämnas därför orörda — att dra dem vore
    # att lägga till ett reglage som bevisligen inte kan flytta något.
    Source("default_subscore_certainty.A", "choice", ("high", "medium", "low"),
           f"{_BUILT}: nivåerna i confidence_numeric. Bara A:s default når ett band; "
           "B, C och D överskrids i varje cell.",
           _set_default_certainty, band_only=True),
    # A:s normalisering STRUKEN 2026-08-21 (ADR 0005, biljett #21). A normaliseras inte längre:
    # båda halvorna mäts mot en historisk förankring och avbildas med net_support_to_score, så
    # reglaget hade inget att dra i (strykningsregeln i ADR 0010 punkt 9). A:s reglage är i
    # stället blandningen nedan: koden läser A_agerande.components och tar emot vilket par som
    # helst utan ny kod (ADR 0010 punkt 4). Fönstret är inget reglage: a2:s förankring är ett
    # aggregat utan år, så configen kan inte uttrycka ett annat fönster (ADR 0010 punkt 6).
    Source("A_component_mix", "range", (0.50, 0.80),
           "a1 i (0,50, 0,80], a2 = 1 - a1. Nedre änden ur ADR 0001, som härleder att a1 väger "
           "mer än a2. Övre änden ur R1 på a2: _span(0.4) ger a2 minst 0,20, alltså a1 högst "
           "0,80. Ingen av ändarna är vald (ADR 0010 punkt 5).",
           _set_component_mix),
    Source("B_coverage_mode", "choice", ("policy_type_count", "weighted_submeasure_depth"),
           f"{_BUILT}: de två lägen scorerun bygger.", _set_b("coverage_mode")),
    Source("B_coverage_shrink", "choice", (True, False),
           f"{_BUILT}: krympningen på eller av.", _set_b("coverage_shrink")),
    Source("B_thin_coverage_threshold", "range", _span(0.5), _R1,
           _set_b("thin_coverage_threshold"), band_only=True),
    Source("effect_strength.high", "range", (0.88, 1.12), _R2_ES, _set_effect_strength("high")),
    Source("effect_strength.medium", "range", (0.48, 0.72), _R2_ES, _set_effect_strength("medium")),
    Source("effect_strength.low", "range", (0.18, 0.42), _R2_ES, _set_effect_strength("low")),
    # Lagget är ett heltal år. Repot använder 1 och ADR 0003 punkt 8 dokumenterar 2 som
    # alternativ -> {1, 2} plus ett års symmetrisk marginal.
    Source("D_attribution_lag_years", "choice", (0, 1, 2, 3),
           "använt 1, dokumenterat 2, plus ett års symmetrisk marginal",
           _set_d("attribution_lag_years")),
    Source("D_change_dead_zone", "range", _span(0.005), _R1, _set_d("change_dead_zone")),
    Source("D_min_responsibility", "range", _span(0.15), _R1, _set_d("min_responsibility")),
    Source("D_thin_basis_threshold", "range", _span(1.0), _R1, _set_d("thin_basis_threshold"),
           band_only=True),
    Source("D_coverage_shrink", "choice", (True, False),
           f"{_BUILT}: krympningen på eller av.", _set_d("coverage_shrink")),
    Source("D_thin_coverage_threshold", "range", _span(0.75), _R1,
           _set_d("thin_coverage_threshold"), band_only=True),
    Source("D_subnational_enabled", "choice", (True, False),
           f"{_BUILT}: subnationellt läge på eller av.", _set_subnational("enabled")),
    # region_weighting har PRECIS ETT byggt alternativ. config.validate släpper igenom
    # 'population', men ingenting i pipen läser det värdet — befolkningsvikt finns bara i
    # auditverktyget pipeline/tools/c3_sensitivity.py, som hämtar folkmängd live. Spannregeln
    # ger då en alternativlista med ett element, och reglaget kan per konstruktion inte flytta
    # något. Det står kvar i tabellen för att frånvaron ska synas.
    Source("D_region_weighting", "choice", ("equal",),
           f"{_BUILT}: bara 'equal' är byggd i pipen; 'population' finns bara i auditverktyget.",
           _set_subnational("region_weighting")),
)


def draw(rng: random.Random) -> dict[str, Any]:
    """En dragning: reglagenamn -> draget värde. Alla reglage dras SAMTIDIGT (ADR 0003 punkt 4)."""
    out: dict[str, Any] = {}
    for s in SOURCES:
        if s.kind == "range":
            lo, hi = s.spec
            out[s.name] = rng.uniform(lo, hi)
        elif s.kind == "choice":
            out[s.name] = rng.choice(s.spec)
        elif s.kind == "simplex":
            # Likformigt på 3-simplexet via två snitt, sedan sorterat B >= A >= D.
            cuts = sorted((rng.random(), rng.random()))
            parts = sorted((cuts[0], cuts[1] - cuts[0], 1.0 - cuts[1]), reverse=True)
            out[s.name] = (parts[1], parts[0], parts[2])   # (A, B, D)
        else:  # pragma: no cover - tabellen ovan är uttömmande
            raise ValueError(f"Okänd reglagetyp: {s.kind}")
    return out


def configs_for(values: dict[str, Any]) -> tuple[dict, dict]:
    """Dragningen -> (scoring, claims) som kopior i minnet. Rör aldrig config/*.yaml."""
    sc = copy.deepcopy(config.scoring())
    cl = copy.deepcopy(config.claims())
    for s in SOURCES:
        s.apply(values[s.name], sc, cl)
    return sc, cl


def build_matrix(con: object, scoring_cfg: dict | None = None,
                 claims_cfg: dict | None = None,
                 patch: Callable[[], Callable[[], None]] | None = None) -> list[list[float]]:
    """Kör scorerun.build under en given config och returnerar kategoribetygen [parti][kategori].

    Monkeypatchar config-loaderna, precis som pipeline/tools/c3_sensitivity.py. `patch` är en
    krok för scenarier som måste byta en funktion i stället för ett configvärde; den returnerar
    sin egen återställare.
    """
    parties, cats = config.party_codes(), config.category_ids()
    orig_scoring, orig_claims = config.scoring, config.claims
    undo = patch() if patch else None
    try:
        if scoring_cfg is not None:
            config.scoring = lambda: scoring_cfg      # type: ignore[assignment]
        if claims_cfg is not None:
            config.claims = lambda: claims_cfg        # type: ignore[assignment]
        scores = scorerun.build(con)["scores"]["scores"]
    finally:
        config.scoring = orig_scoring                 # type: ignore[assignment]
        config.claims = orig_claims                   # type: ignore[assignment]
        if undo:
            undo()
    return [[float(scores[p][c]["score"]) for c in cats] for p in parties]


# --- Ordning och stabilitet -----------------------------------------------------------


def order_of(values: Sequence[float], parties: Sequence[str]) -> list[str]:
    """Fallande betyg, alfabetisk tie-break — SAMMA regel som web/score.js partyTotals."""
    return [p for _, p in sorted((-v, p) for v, p in zip(values, parties, strict=True))]


def _pair_keys(order: Sequence[str]) -> list[tuple[str, str]]:
    """Alla partipar, riktade så att det parti som ligger före i baslinjen står först."""
    return [(order[i], order[j]) for i in range(len(order)) for j in range(i + 1, len(order))]


def pair_shares(
    matrices: Sequence[Sequence[Sequence[float]]], parties: Sequence[str],
    pairs: Sequence[tuple[str, str]],
    col: int | None = None, weights: Sequence[float] | None = None,
) -> dict[str, float]:
    """Andelen dragningar där `a` ligger före `b`, för varje par.

    `col` väljer en kategori; `weights` väger ihop kategorierna till en total. Exakt en av dem
    ska anges. Oavgjort räknas inte som "före" åt något håll — talet svarar på frågan sajten
    ställer, alltså hur ofta ett parti faktiskt ligger före ett annat.
    """
    if (col is None) == (weights is None):
        raise ValueError("Ange antingen col (en kategori) eller weights (en total), inte båda")
    idx = {p: i for i, p in enumerate(parties)}
    wins = dict.fromkeys(pairs, 0)
    for m in matrices:
        if col is not None:
            vals = [row[col] for row in m]
        else:
            vals = [sum(v * w for v, w in zip(row, weights, strict=True)) for row in m]
        for pair in pairs:
            if vals[idx[pair[0]]] > vals[idx[pair[1]]]:
                wins[pair] += 1
    n = len(matrices)
    return {f"{a}|{b}": round(wins[(a, b)] / n, 4) for a, b in pairs}


class Analysis(NamedTuple):
    category_stability: dict[str, dict[str, float]]
    standard_weight_stability: dict[str, float]
    source_influence: dict[str, dict[str, Any]]
    baseline_order: list[str]


def _mean(xs: Iterable[float]) -> float:
    vals = list(xs)
    return sum(vals) / len(vals) if vals else 0.0


def _bins_for(source: Source, draws: Sequence[dict[str, Any]]) -> dict[Any, list[int]]:
    """Dragningarnas index grupperade per fack: alternativet, eller kvartilen för ett spann."""
    n = len(draws)
    buckets: dict[Any, list[int]] = {}
    if source.kind == "choice":
        for k in range(n):
            buckets.setdefault(draws[k][source.name], []).append(k)
        return buckets
    key = source.bin_key or (lambda v: v)
    order = sorted(range(n), key=lambda k: key(draws[k][source.name]))
    for pos, k in enumerate(order):
        buckets.setdefault(min(N_INFLUENCE_BINS - 1, pos * N_INFLUENCE_BINS // n), []).append(k)
    return buckets


def analyse(
    matrices: Sequence[Sequence[Sequence[float]]], draws: Sequence[dict[str, Any]],
    baseline: Sequence[Sequence[float]], parties: Sequence[str], cats: Sequence[str],
    std_weights: Sequence[float],
) -> Analysis:
    """Kategori- och totalstabilitet plus varje reglages förstaordningseffekt på andelen.

    Reglageinflytandet läses ur SAMMA samtidiga dragning (ADR 0003 punkt 4): för varje fack av
    reglaget räknas andelen om, och inflytandet är hur många procentenheter andelen rör sig
    mellan det högsta och det lägsta facket, i medeltal över partiparen. Allt annat är då
    utmedelvärdat, alltså är det reglaget ENSAMT som flyttar talet.
    """
    base_total = [sum(v * w for v, w in zip(row, std_weights, strict=True)) for row in baseline]
    total_order = order_of(base_total, parties)
    total_pairs = _pair_keys(total_order)
    cat_pairs = {
        c: _pair_keys(order_of([row[i] for row in baseline], parties)) for i, c in enumerate(cats)
    }

    cat_stability = {
        c: pair_shares(matrices, parties, cat_pairs[c], col=i) for i, c in enumerate(cats)
    }
    total_stability = pair_shares(matrices, parties, total_pairs, weights=std_weights)

    def mean_cat_share(subset: Sequence[Sequence[Sequence[float]]]) -> float:
        return _mean(
            v for i, c in enumerate(cats)
            for v in pair_shares(subset, parties, cat_pairs[c], col=i).values()
        )

    influence: dict[str, dict[str, Any]] = {}
    for s in SOURCES:
        buckets = _bins_for(s, draws)
        if len(buckets) < 2:
            influence[s.name] = {"category_points": 0.0, "total_points": 0.0,
                                 "n_bins": len(buckets), "single_bin": True}
            continue
        cat_means, tot_means = {}, {}
        for b, ks in buckets.items():
            subset = [matrices[k] for k in ks]
            cat_means[b] = mean_cat_share(subset)
            tot_means[b] = _mean(
                pair_shares(subset, parties, total_pairs, weights=std_weights).values()
            )
        influence[s.name] = {
            "category_points": round(100 * (max(cat_means.values()) - min(cat_means.values())), 3),
            "total_points": round(100 * (max(tot_means.values()) - min(tot_means.values())), 3),
            "n_bins": len(buckets),
            "bins": {str(b): round(100 * cat_means[b], 2) for b in sorted(buckets, key=str)},
        }
    return Analysis(cat_stability, total_stability, influence, total_order)


# --- De sju namngivna scenarierna (ADR 0003 punkt 8) ----------------------------------


def _old_weights(sc: dict) -> None:
    sc["subscore_weights"] = {"A": 0.40, "B": 0.35, "C": 0.15, "D": 0.10}


def _halve_a(sc: dict) -> None:
    """A halveras. B och D skalas upp så vikterna fortfarande summerar till 1.

    Utan omviktningen skulle scenariot både halvera A OCH krympa hela skalan, alltså pröva
    två saker på en gång. Här prövas bara det scenariot heter.
    """
    w = sc["subscore_weights"]
    a = w["A"] / 2
    scale = (1.0 - a) / (w["B"] + w["D"])
    sc["subscore_weights"] = {"A": a, "B": w["B"] * scale, "C": 0.0, "D": w["D"] * scale}


def _b_shrink_off(sc: dict) -> None:
    sc["B_evidens"]["coverage_shrink"] = False


def _d_lag_two(sc: dict) -> None:
    sc["D_resultat"]["attribution_lag_years"] = 2


def _b_confidence_one_step_down() -> Callable[[], None]:
    """Scenario 4: B:s säkerhet ett steg ned. Reglaget finns inte i config, så funktionen byts."""
    orig = scorerun._b_confidence

    def stepped(conf_cat: float, n_claims: int, thin_coverage: bool) -> str:
        return scorerun._step_down_confidence(orig(conf_cat, n_claims, thin_coverage), 1)

    scorerun._b_confidence = stepped   # type: ignore[assignment]
    return lambda: setattr(scorerun, "_b_confidence", orig)


SCENARIOS: tuple[dict[str, Any], ...] = (
    {"id": 1, "name": "gamla vikterna", "kind": "uncertainty",
     "description": "0,40 A + 0,35 B + 0,15 C + 0,10 D, alltså vikterna före ADR 0002.",
     "mutate": _old_weights},
    {"id": 2, "name": "A halveras", "kind": "uncertainty",
     "description": "A:s vikt halveras; B och D skalas upp så summan står kvar på 1.",
     "mutate": _halve_a},
    {"id": 3, "name": "B utan coverage-krympning", "kind": "uncertainty",
     "description": "B = B_raw, alltså ingen krympning mot 2,5 efter täckning.",
     "mutate": _b_shrink_off},
    {"id": 4, "name": "B:s säkerhet ett steg ned", "kind": "uncertainty",
     "description": "Varje B-cell får en nivå lägre säkerhet, alltså ett bredare band.",
     "mutate": None, "patch": _b_confidence_one_step_down},
    {"id": 5, "name": "D-lagg 2 år", "kind": "uncertainty",
     "description": "Utfallsförändring år y tillskrivs den som styrde år y-2 i stället för y-1.",
     "mutate": _d_lag_two},
    {"id": 6, "name": "bara kategorier med hög D-täckning", "kind": "filter",
     "description": ("Filter. Bara kategorier vars D-täckning, i medeltal över de partier som "
                     "har uppmätt D, når D_resultat.thin_coverage_threshold. Byter vad indexet "
                     "mäter, inte hur osäkert det är."),
     "mutate": None},
    {"id": 7, "name": "bara partier med nationellt ansvar", "kind": "filter",
     "description": ("Filter. Bara partier med maktandel > 0 i fönstret, alltså de som suttit i "
                     "regering eller stött en. Byter vad indexet mäter, inte hur osäkert det är."),
     "mutate": None},
)


def high_d_coverage_categories(con: object) -> list[str]:
    """Kategorier vars D-täckning når tröskeln, i medeltal över partier med uppmätt D.

    Icke-uppmätta celler har covered_weight 0 per konstruktion och säger inget om kategorins
    täckning, så de hålls utanför medlet. Tröskeln är repots egen gräns för tunn D-bredd.
    """
    parties, cats = config.party_codes(), config.category_ids()
    cells = scorerun.category_d(con, parties, cats)
    threshold = float(config.scoring()["D_resultat"].get("thin_coverage_threshold", 0.75))
    out = []
    for c in cats:
        covs = [
            cells[(p, c)].covered_weight / cells[(p, c)].total_weight
            for p in parties if cells[(p, c)].measured and cells[(p, c)].total_weight
        ]
        if covs and _mean(covs) >= threshold:
            out.append(c)
    return out


def national_responsibility_parties() -> list[str]:
    """Partier med maktandel > 0 i fönstret (regering eller stödparti)."""
    frac = scorerun.government_fractions()
    return [p for p in config.party_codes() if frac.get(p, 0.0) > 0]


def run_scenarios(con: object, baseline: list[list[float]],
                  std_weights: Sequence[float]) -> list[dict[str, Any]]:
    """De sju scenarierna, var för sig. Filter kör ingen ombyggnad — de plockar ur baslinjen."""
    parties, cats = config.party_codes(), config.category_ids()
    out = []
    for sc_def in SCENARIOS:
        inc_parties, inc_cats = list(parties), list(cats)
        if sc_def["kind"] == "filter":
            matrix = [list(row) for row in baseline]
            if sc_def["id"] == 6:
                inc_cats = high_d_coverage_categories(con)
            else:
                inc_parties = national_responsibility_parties()
        else:
            cfg = None
            if sc_def["mutate"]:
                cfg = copy.deepcopy(config.scoring())
                sc_def["mutate"](cfg)
            matrix = build_matrix(con, cfg, patch=sc_def.get("patch"))
        keep = [i for i, c in enumerate(cats) if c in inc_cats]
        wsum = sum(std_weights[i] for i in keep)
        # Ett filter kan tömma indexet (ingen kategori når tröskeln). Då finns ingen total och
        # ingen ordning att redovisa. Tomheten göms inte: included_categories blir tom och
        # report() skriver ut hur många som kom med.
        totals = {} if wsum == 0 else {
            p: sum(matrix[parties.index(p)][i] * std_weights[i] for i in keep) / wsum
            for p in inc_parties
        }
        out.append({
            "id": sc_def["id"], "name": sc_def["name"], "kind": sc_def["kind"],
            "description": sc_def["description"],
            "matrix": [[round(v, 3) for v in row] for row in matrix],
            "included_parties": inc_parties, "included_categories": inc_cats,
            "order": order_of(list(totals.values()), list(totals)),
            "totals": {p: round(v, 3) for p, v in totals.items()},
        })
    return out


# --- Utdatan ---------------------------------------------------------------------------


def _mc_error(n: int) -> float:
    """Värsta standardfel för en andel skattad ur n dragningar, i procentenheter.

    Noll dragningar bär ingen skattning alls. Talet blir då 100, alltså hela skalan, i stället
    för 0. Ett fel på noll skulle påstå full säkerhet där det inte finns någon dragning.
    """
    if n <= 0:
        return 100.0
    return round(100 * 0.5 / math.sqrt(n), 3)


def _source_meta() -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for s in SOURCES:
        entry: dict[str, Any] = {"kind": s.kind, "note": s.note}
        if s.band_only:
            entry["band_only"] = True
        if s.kind == "range":
            entry["range"] = [round(s.spec[0], 6), round(s.spec[1], 6)]
        elif s.kind == "choice":
            entry["alternatives"] = [str(v) for v in s.spec]
        out[s.name] = entry
    return out


def run(con: object, n_draws: int = N_DRAWS, n_shipped: int = N_DRAWS_SHIPPED,
        seed: int = SEED, progress: bool = True) -> dict[str, Any]:
    """Hela analysen: baslinje, dragningar, stabilitet, reglageinflytande och scenarier."""
    parties, cats = config.party_codes(), config.category_ids()
    std_weights = [float(c["standard_weight"]) for c in config.categories()["categories"]]

    baseline = build_matrix(con)
    rng = random.Random(seed)
    draws: list[dict[str, Any]] = []
    matrices: list[list[list[float]]] = []
    t0 = time.perf_counter()
    for i in range(n_draws):
        values = draw(rng)
        sc, cl = configs_for(values)
        draws.append(values)
        matrices.append(build_matrix(con, sc, cl))
        if progress and (i + 1) % 250 == 0:
            done = time.perf_counter() - t0
            left = done / (i + 1) * (n_draws - i - 1)
            print(f"  {i + 1}/{n_draws} dragningar  ({done:.0f} s, ~{left:.0f} s kvar)",
                  file=sys.stderr, flush=True)

    an = analyse(matrices, draws, baseline, parties, cats, std_weights)
    shipped = matrices[:n_shipped]
    values_flat = [round(v * 100) for m in shipped for row in m for v in row]

    return {
        "meta": {
            "generated": date.today().isoformat(),
            "seed": seed,
            "n_draws": n_draws,
            "n_draws_shipped": len(shipped),
            "monte_carlo_error": _mc_error(n_draws),
            "monte_carlo_error_shipped": _mc_error(len(shipped)),
            "monte_carlo_error_bins": _mc_error(max(1, n_draws // N_INFLUENCE_BINS)),
            "parties": parties,
            "categories": cats,
            "standard_weights": dict(zip(cats, std_weights, strict=True)),
            "sources": _source_meta(),
            "measure": ("Andelen metodvarianter där två partiers inbördes ordning håller "
                        "(ADR 0003 punkt 2). Ingen tröskel: andelen redovisas som den är."),
            "influence_note": (
                "source_influence är reglagets förstaordningseffekt: hur många procentenheter "
                "andelen rör sig mellan reglagets högsta och lägsta fack, i medeltal över "
                "partiparen, med allt annat utmedelvärdat. Statistiken är max minus min över "
                "facken och ligger därför en bit över noll även för ett reglage utan effekt. "
                "Reglage märkta band_only rör per konstruktion bara osäkerhetsbandet och aldrig "
                "betyget (låst i tests/test_robustness.py), så deras tal läser av brusgolvet."),
        },
        "draws": {"parties": parties, "categories": cats, "scale": 100, "values": values_flat},
        "baseline": {
            "matrix": [[round(v, 3) for v in row] for row in baseline],
            "order": an.baseline_order,
        },
        "category_stability": an.category_stability,
        "standard_weight_stability": an.standard_weight_stability,
        "source_influence": an.source_influence,
        "scenarios": run_scenarios(con, baseline, std_weights),
    }


def report(out: dict[str, Any]) -> None:
    """Godkännandetestets tal, utskrivna som de blev."""
    print("\n== Andelen per partipar i totalen, standardvikterna ==")
    for key, share in sorted(out["standard_weight_stability"].items(), key=lambda kv: -kv[1]):
        a, b = key.split("|")
        print(f"  {a} ligger före {b} i {100 * share:.1f} procent av metodvarianterna")

    print("\n== Reglageinflytande (procentenheter som reglaget ENSAMT flyttar andelen) ==")
    srcs = out["meta"]["sources"]
    ranked = sorted(out["source_influence"].items(), key=lambda kv: -kv[1]["category_points"])
    for name, inf in ranked:
        marks = []
        if inf.get("single_bin"):
            marks.append("ett enda byggt alternativ")
        if srcs.get(name, {}).get("band_only"):
            marks.append("bara bandet, alltså brusgolvet")
        note = f"  ({'; '.join(marks)})" if marks else ""
        print(f"  {name:32} kategori {inf['category_points']:6.2f}   "
              f"total {inf['total_points']:6.2f}{note}")
    floor = [inf["category_points"] for n, inf in out["source_influence"].items()
             if srcs.get(n, {}).get("band_only")]
    if floor:
        print(f"  brusgolv (band_only-reglagen): {min(floor):.2f} till {max(floor):.2f} "
              "procentenheter")

    print("\n== Scenarier ==")
    n_cats, n_parties = len(out["meta"]["categories"]), len(out["meta"]["parties"])
    for s in out["scenarios"]:
        mark = ""
        if s["kind"] == "filter":
            mark = (f" [FILTER: {len(s['included_categories'])}/{n_cats} kategorier, "
                    f"{len(s['included_parties'])}/{n_parties} partier]")
        print(f"  {s['id']}. {s['name']}{mark}: {' > '.join(s['order']) or '(tomt index)'}")
    print(f"\n  baslinjen: {' > '.join(out['baseline']['order'])}")


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="Monte Carlo över modellens osäkra val (ADR 0003).")
    ap.add_argument("--draws", type=int, default=N_DRAWS)
    ap.add_argument("--shipped", type=int, default=N_DRAWS_SHIPPED)
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--out", default=str(DIST_DIR / "robustness.json"))
    args = ap.parse_args()

    con = warehouse.connect()
    t0 = time.perf_counter()
    out = run(con, n_draws=args.draws, n_shipped=min(args.shipped, args.draws), seed=args.seed)
    con.close()
    schema.validate("robustness", out)

    DIST_DIR.mkdir(parents=True, exist_ok=True)
    text = json.dumps(out, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(text)

    print(f"skrev {args.out}  ({len(text) / 1024:.0f} kB, {time.perf_counter() - t0:.0f} s)")
    print(f"seed {out['meta']['seed']}, {out['meta']['n_draws']} dragningar, "
          f"Monte Carlo-fel {out['meta']['monte_carlo_error']} procentenheter")
    report(out)


if __name__ == "__main__":
    main()
