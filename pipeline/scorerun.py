"""Fas 5: warehouse -> dist/scores.json + dist/evidence.json (deploy-artefakten).

Beräknar A/B/C/D per (parti, kategori) deterministiskt och skriver de enda filer som
deployas. Kategoribetyg = 0,30 A + 0,50 B + 0,20 D; C väger 0 (ADR 0002). Läget i dag:
  A = prioritering: a1 budgetandel (gated) + a2 motionsandel, rank-norm.  -> hög säkerhet
  B = evidens: partiståndpunkter x evidensliggare -> väntad storlek, krympt efter
      täckning; säkerheten härleds ur evidensen (ADR 0004)                -> hög/medel/låg
  C = maktandel: nationell + subnationell makt, rank-norm. Ger inga poäng -> hög/medel
  D = resultat: attribuerad indikatorförändring där partiet haft ansvar   -> medel/låg
Osäkerheten speglar detta ärligt. Kör: python -m pipeline.scorerun
"""

from __future__ import annotations

import json
import sys
from datetime import date, timedelta
from typing import NamedTuple

from . import DIST_DIR, budget, config, effects, positions, schema, score, warehouse
from . import claims as claims_mod

# Mandatperiodens FORMELLA slut (nästa riksdagsval). Det här är ett fönsterslut för ansvar och
# attribution, INTE ett observationsslut: under hela mandatperioden ligger datumet i framtiden.
# Hur långt underlaget faktiskt räcker är en annan storhet. Se data_freshness().
WINDOW_END = date(2026, 9, 13)

# Maktandelens fönsterslut: sista dagen i sista AVSLUTADE observationsåret. Skilt från
# WINDOW_END, som ligger i framtiden under hela mandatperioden och därför skulle tillgodoräkna
# den sittande regeringen maktdagar den ännu inte suttit, och späda alla fraktioner med en
# framtida nämnare (biljett #14). HANDSATT med flit: höj den manuellt när lagret fått ett helt
# nytt år. Anropa INTE data_freshness() här — den avgör "avslutat år" mot today.year och gör
# storheten beroende av körtidpunkten i stället för av lagret.
POWER_WINDOW_END = date(2025, 12, 31)


def _power_window_stop() -> date:
    """Halvöppen gräns för maktandelens räkning: [fönstrets start, stopp).

    POWER_WINDOW_END är den sista dagen som SKA räknas, så gränsen i räkningen är dagen
    efter. Utan det steget väger 2025 364/365 i year_power_fractions, alltså ett påstående
    om att regeringen inte satt hela året, och D läser 2025. Härledd i en funktion och inte
    i en modulkonstant, så att POWER_WINDOW_END är enda sanningskällan: meta.power_window_end
    publicerar samma tal som räkningen använder, och testerna kan flytta gränsen.
    """
    return POWER_WINDOW_END + timedelta(days=1)


def _as_date(v: object) -> date:
    """PyYAML kan ge date-objekt eller sträng — coerca till date."""
    return v if isinstance(v, date) else date.fromisoformat(str(v))


class DataFreshness(NamedTuple):
    """Hur långt underlaget räcker, skilt från WINDOW_END."""

    as_of: str | None       # ISO-datum: sista dagen i senaste AVSLUTADE observationsåret
    latest_year: int | None # senaste observationsåret, även om året fortfarande pågår


def data_freshness(con: object, today: date | None = None) -> DataFreshness:
    """meta.data_as_of + meta.latest_observation_year ur observationslagret.

    Serierna är årsserier, så finaste ärliga upplösning är ett helt år. Ett år som fortfarande
    pågår flyttar därför INTE fram as_of: sajten ska aldrig påstå att den har data fram till ett
    datum som inte inträffat. Det pågående året göms inte heller. Det syns som latest_year.
    Saknas avslutade år blir as_of None och sajten säger inget alls om underlagets slut.
    """
    today = today or date.today()
    years = {
        y for (p,) in con.execute("SELECT DISTINCT period FROM observations").fetchall()
        if (y := score.period_end_year(p)) is not None
    }
    if not years:
        return DataFreshness(None, None)
    complete = [y for y in years if y < today.year]
    as_of = date(max(complete), 12, 31).isoformat() if complete else None
    return DataFreshness(as_of, max(years))


def government_fractions() -> dict[str, float]:
    """Maktandel: andel av fönstret varje parti haft regeringsmakt (stöd vägs 0.5).

    Fönstret slutar vid POWER_WINDOW_END, inte WINDOW_END: en pågående regeringsperiod räknas
    bara till sista avslutade observationsåret, och nämnaren stannar på samma dag. Storheten
    heter maktandel och är C. Den ska inte förväxlas med ansvarsunderlag, som är D:s grind
    (Σ maktvikt över de attribuerade åren, `basis` i category_d). Se ADR 0002 § Rättelse.
    """
    gps = config.mappings()["government_periods"]
    parsed = []
    for gp in gps:
        s = _as_date(gp["start"])
        e = _as_date(gp["end"]) if gp.get("end") else _power_window_stop()
        parsed.append((s, e, gp.get("parties", []), gp.get("support_parties", [])))
    win_start = min(s for s, _, _, _ in parsed)
    total = (_power_window_stop() - win_start).days
    frac = {p: 0.0 for p in config.party_codes()}
    for s, e, parties, supp in parsed:
        days = (e - s).days
        for p in parties:
            frac[p] += days / total
        for p in supp:
            frac[p] += 0.5 * days / total
    return {p: min(1.0, v) for p, v in frac.items()}


def regional_fractions() -> dict[str, float]:
    """Andel av regionalt styre varje parti haft över fönstret (subnationell makt för C).

    Varje (region, mandatperiod)-cell väger LIKA (mandatperioderna är jämnstora 4-årscykler;
    jfr national som dagväger eftersom regeringsperioder är oregelbundna). I en cell delas
    makten jämnt mellan de ledande riksdagspartierna (1/antal; lokala partier räknas ej).
    Resultat i [0,1] per parti. Tom dict om regiondata saknas -> C faller på nationell makt.
    """
    sg = config.mappings().get("subnational_governance", {})
    regions = sg.get("regions") or {}
    if not regions:
        return {}
    frac = {p: 0.0 for p in config.party_codes()}
    cells = 0
    for region in regions.values():
        for styre in region.get("terms", {}).values():
            cells += 1
            leading = styre.get("leading_parties", [])
            if not leading:
                continue
            share = 1.0 / len(leading)
            for p in leading:
                if p in frac:
                    frac[p] += share
    if cells == 0:
        return {}
    return {p: v / cells for p, v in frac.items()}


def municipal_fractions() -> dict[str, float]:
    """Andel av kommunalt styre varje parti haft över fönstret (subnationell makt för C).

    Samma metod som regional_fractions: varje (kommun, mandatperiod)-cell väger lika; i en cell
    delas makten jämnt mellan de ledande riksdagspartierna (lokala partier räknas ej). Läser
    config/subnational_municipalities.yaml (terms = lista per mandatperiod). Tom dict om data saknas.
    """
    data = config.subnational_municipalities().get("municipalities") or {}
    if not data:
        return {}
    frac = {p: 0.0 for p in config.party_codes()}
    cells = 0
    for entry in data.values():
        for leading in entry.get("terms", []):
            cells += 1
            if not leading:
                continue
            share = 1.0 / len(leading)
            for p in leading:
                if p in frac:
                    frac[p] += share
    if cells == 0:
        return {}
    return {p: v / cells for p, v in frac.items()}


def _region_kolada_code(config_key: str) -> str:
    """Config-regionnyckel ('01') -> Kolada 4-siffrig regionkod ('0001'), så region-år-makten
    nycklas på SAMMA geografi som observationerna (build_subnational)."""
    return f"{int(config_key):04d}"


def region_year_power_fractions() -> dict[str, dict[int, dict[str, float]]]:
    """Per region och kalenderår: maktvikt per parti (C3 — subnationell D-attribution).

    {Kolada-regionkod -> {år -> {parti -> maktvikt 0-1}}}. Mandatperioderna (subnational_
    governance.terms, tillträde 15 okt valåret) DAGVIKTAS per kalenderår precis som den
    nationella year_power_fractions (så ett valår delas mellan gammalt och nytt styre); inom
    ett styre delas makten jämnt mellan de ledande riksdagspartierna (1/antal, jfr skr.py /
    regional_fractions). Inget stödparti-begrepp subnationellt (SKR-datan skiljer ej). Tom dict
    om regiondata saknas -> subnationell D faller bort (ren nationell D).
    """
    sg = config.mappings().get("subnational_governance", {})
    regions = sg.get("regions") or {}
    terms = sg.get("terms") or []
    if not regions or not terms:
        return {}
    parsed = [(t["id"], _as_date(t["start"]), min(_as_date(t["end"]), WINDOW_END)) for t in terms]
    win_start = min(s for _, s, _ in parsed)
    party_set = set(config.party_codes())
    out: dict[str, dict[int, dict[str, float]]] = {}
    for key, region in regions.items():
        term_styre = region.get("terms", {})
        per_year: dict[int, dict[str, float]] = {}
        for year in range(win_start.year, WINDOW_END.year + 1):
            y0, y1 = date(year, 1, 1), date(year + 1, 1, 1)
            year_days = (y1 - y0).days
            frac: dict[str, float] = {}
            for tid, s, e in parsed:
                overlap = (min(e, y1) - max(s, y0)).days
                if overlap <= 0:
                    continue
                leading = [p for p in term_styre.get(tid, {}).get("leading_parties", []) if p in party_set]
                if not leading:
                    continue
                contrib = (overlap / year_days) * (1.0 / len(leading))
                for p in leading:
                    frac[p] = frac.get(p, 0.0) + contrib
            if frac:
                per_year[year] = frac
        out[_region_kolada_code(key)] = per_year
    return out


def _parsed_periods() -> list[tuple[date, date, list[str], list[str]]]:
    out = []
    for gp in config.mappings()["government_periods"]:
        s = _as_date(gp["start"])
        e = _as_date(gp["end"]) if gp.get("end") else _power_window_stop()
        out.append((s, e, gp.get("parties", []), gp.get("support_parties", [])))
    return out


def year_power_fractions() -> dict[int, dict[str, float]]:
    """Per kalenderår: andel av året varje parti haft regeringsmakt (stöd vägs 0.5).

    Används av D-attributionen för att tillskriva en årsförändring rätt regering.
    """
    parsed = _parsed_periods()
    win_start = min(s for s, _, _, _ in parsed)
    out: dict[int, dict[str, float]] = {}
    for year in range(win_start.year, WINDOW_END.year + 1):
        y0, y1 = date(year, 1, 1), date(year + 1, 1, 1)
        year_days = (y1 - y0).days
        frac: dict[str, float] = {}
        for s, e, parties, supp in parsed:
            overlap = (min(e, y1) - max(s, y0)).days
            if overlap <= 0:
                continue
            share = overlap / year_days
            for p in parties:
                frac[p] = min(1.0, frac.get(p, 0.0) + share)
            for p in supp:
                frac[p] = min(1.0, frac.get(p, 0.0) + 0.5 * share)
        out[year] = frac
    return out


def _annual_series(con: object) -> dict[tuple[str, str], dict[int, float]]:
    """(kategori, indikator) -> {år -> värde} ur nationella observationer (Riket/0000).

    Period -> år via score.period_to_year (månads-/kvartalsserier hoppas över). Dubbletter
    på samma år (t.ex. ULF-dubbelår) medelvärdesbildas.
    """
    raw = con.execute(
        "SELECT category, indicator, period, value FROM observations "
        "WHERE geography IN ('Riket', '0000')"
    ).fetchall()
    buckets: dict[tuple[str, str], dict[int, list[float]]] = {}
    for cat, ind, period, val in raw:
        if val is None:
            continue
        year = score.period_to_year(period)
        if year is None:
            continue
        buckets.setdefault((cat, ind), {}).setdefault(year, []).append(float(val))
    return {
        key: {y: sum(vs) / len(vs) for y, vs in years.items()}
        for key, years in buckets.items()
    }


def _subnational_annual_series(
    con: object,
) -> dict[tuple[str, str], dict[str, dict[int, float]]]:
    """(kategori, indikator) -> {regionkod -> {år -> värde}} ur REGION-observationer (C3).

    Läser bara observationer vars geografi är en känd Kolada-regionkod (subnational_governance.
    regions, 4-siffrig) — separat från _annual_series som läser nationellt (Riket/0000), så
    nationell D är orörd. Period->år via score.period_to_year; dubbletter medelvärdesbildas.
    """
    regions = config.mappings().get("subnational_governance", {}).get("regions") or {}
    codes = [_region_kolada_code(k) for k in regions]
    if not codes:
        return {}
    ph = ", ".join("?" for _ in codes)
    raw = con.execute(
        f"SELECT category, indicator, geography, period, value FROM observations "
        f"WHERE geography IN ({ph})",
        codes,
    ).fetchall()
    buckets: dict[tuple[str, str], dict[str, dict[int, list[float]]]] = {}
    for cat, ind, geo, period, val in raw:
        if val is None:
            continue
        year = score.period_to_year(period)
        if year is None:
            continue
        buckets.setdefault((cat, ind), {}).setdefault(geo, {}).setdefault(year, []).append(float(val))
    return {
        key: {geo: {y: sum(vs) / len(vs) for y, vs in years.items()} for geo, years in geos.items()}
        for key, geos in buckets.items()
    }


def _indicator_meta() -> dict[tuple[str, str], tuple[str, str]]:
    """(kategori, indikator) -> (submått, riktning) ur categories.yaml."""
    out: dict[tuple[str, str], tuple[str, str]] = {}
    for cat in config.categories()["categories"]:
        for ind in cat.get("indicators", []):
            out[(cat["id"], ind["id"])] = (ind["submeasure"], ind["direction"])
    return out


def _submeasure_weights() -> dict[str, dict[str, float]]:
    """kategori -> {submått-id -> vikt}."""
    return {
        cat["id"]: {s["id"]: float(s["weight"]) for s in cat["submeasures"]}
        for cat in config.categories()["categories"]
    }


def _non_target_submeasures() -> dict[str, set[str]]:
    """kategori -> icke-target-undermått (täckningsnämnaren som B och D DELAR,
    spec docs/done/d_coverage_krympning_spec.md §3.1 / docs/done/b_coverage_krympning_spec.md §3.4).

    Target-only = undermåttet har minst en indikator OCH alla dess indikatorer har
    direction 'target'. Undermått UTAN indikatorer är inte target-only — de är en del av
    kategorianspråket och ingår i nämnaren (t.ex. klimats industriell_konkurrenskraft).
    """
    out: dict[str, set[str]] = {}
    for cat in config.categories()["categories"]:
        dirs: dict[str, list[str]] = {s["id"]: [] for s in cat["submeasures"]}
        for ind in cat.get("indicators", []):
            dirs[ind["submeasure"]].append(ind["direction"])
        out[cat["id"]] = {
            sid for sid, ds in dirs.items() if not (ds and all(d == "target" for d in ds))
        }
    return out


# B och D ska bevisligen dela nämnardefinition, inte duplicera den (B5-spec §6.2).
# Aliaset behåller D-namnet för D-anrop/tester; tests/test_b_coverage_mode.py låser identiteten.
_d_denominator_submeasures = _non_target_submeasures


def _b_codable_types_by_submeasure() -> dict[str, dict[str, set[str]]]:
    """kategori -> {undermått -> kodbara åtgärdstyper T_s} (B5-spec §3.1).

    Kodbar = samma regler som legacy-nämnaren cov_den (signed_direction != 0, ej
    coverage_exclude), men struktureras per undermått via liggarpostens indikator.
    En policy_type vars liggarposter pekar på indikatorer i FLERA undermått ingår i
    varje (koldioxidskatt-fallet): ståndpunkten informerar båda anspråken. Mängd-
    semantiken deduplicerar dubblerade poster inom samma undermått (anti-gaming, §7).
    """
    signed = config.claims()["aggregation"]["signed_direction"]
    b_exclude = set(config.scoring()["B_evidens"].get("coverage_exclude", []))
    meta = _indicator_meta()
    out: dict[str, dict[str, set[str]]] = {}
    for e in config.evidence_ledger()["entries"]:
        if signed.get(e["direction"], 0) == 0 or e["policy_type"] in b_exclude:
            continue
        key = (e["category"], e["indicator"])
        if key not in meta:
            continue
        out.setdefault(e["category"], {}).setdefault(meta[key][0], set()).add(e["policy_type"])
    return out


def _b_coverage_flag(covered_weight: float, total_weight: float) -> str:
    """B_coverage-flaggan i nya moden — formatet är LÅST (B5-spec §4).

    covered_weight kan bli icke-heltal pga |K_s|/|T_s|-bråken och avrundas till 1 decimal;
    :g skriver heltal utan decimal (86.666… -> '86.7', 73.0 -> '73', aldrig '73.0').
    total_weight är alltid heltal ur categories.yaml.
    """
    return f"B_coverage_{round(covered_weight, 1):g}/{total_weight:g}"


class DCell(NamedTuple):
    """D-resultat för en (parti, kategori)-cell (jfr category_d)."""

    score: float
    measured: bool
    thin_basis: bool        # kombinerat ansvarsunderlag (nat + region år-ekv.) under thin_basis_threshold
    covered_weight: float   # Σ vikt för icke-target-undermått med faktiskt D-underlag för partiet
    total_weight: float     # Σ vikt för kategorins icke-target-undermått (nämnaren)
    thin_coverage: bool     # viktad täckning under thin_coverage_threshold
    subnational_used: bool  # C3: subnationell (region) attribution bidrog till cellen
    region_basis: float     # C3: regionalt ansvarsunderlag, ÅR-EKVIVALENT (Σ power / antal regioner)


def category_d(con: object, parties: list[str], cats: list[str]) -> dict[tuple[str, str], DCell]:
    """D per (parti, kategori) som DCell.

    För varje nationell årsindikator tillskrivs riktningsjusterade årsförändringar den
    regering som satt lag-år tidigare (score.attribute_series). Per submått medelvärdesbildas
    indikatorernas net, sedan submåttsviktat medel -> net i [-1,1] -> betyg. Gate: kategorins
    net finns OCH partiets ansvarsunderlag >= min_responsibility, annars ej tillämplig.

    D-bredd (coverage_shrink, spec docs/done/d_coverage_krympning_spec.md): D mäter kategorins
    utfall, inte bara de undermått som råkar ha en serie. Med coverage_shrink aktiv bidrar
    saknade icke-target-undermått neutralt (net 0) i en FAST nämnare i stället för att
    renormaliseras bort. Numeratorn är per (parti, kategori): korta serier/glapp kan göra
    att ett parti saknar attribution i en serie andra partier täcks av. Gaten använder
    fortsatt det renormaliserade nätet — saknad bredd ska inte göra en tom kategori measured.

    C3 — SUBNATIONELL D (docs/done/c3_subnational_d_metod.md, gated på D_resultat.subnational.
    enabled): för submått i submeasure_level_weights blandas det nationella submåtts-nätet med ett
    REGION-poolat net (score.attribute_subnational_indicator) enligt {national, region}-vikten, så
    ett regionstyrt utfall (vård) attribueras till det parti som styrde regionen. Regionalt
    ansvarsunderlag normaliseras till ÅR-EKVIVALENT och adderas till det nationella i grinden
    (ett parti med enbart regional vård-makt blir measured). enabled:false -> allt nedan är
    no-op och D är byte-identisk med ren nationell attribution.
    """
    cfg = config.scoring()["D_resultat"]
    lag = int(cfg["attribution_lag_years"])
    dead = float(cfg["change_dead_zone"])
    min_resp = float(cfg["min_responsibility"])
    thin = float(cfg["thin_basis_threshold"])
    na_score = float(cfg["not_applicable_score"])
    shrink = bool(cfg.get("coverage_shrink", False))
    thin_cov = float(cfg.get("thin_coverage_threshold", 0.75))

    subn_cfg = cfg.get("subnational") or {}
    subn_on = bool(subn_cfg.get("enabled"))
    slw = (subn_cfg.get("submeasure_level_weights") or {}) if subn_on else {}

    yp = year_power_fractions()
    series = _annual_series(con)
    meta = _indicator_meta()
    sub_w = _submeasure_weights()
    d_den = _d_denominator_submeasures()
    total_w = {c: sum(sub_w.get(c, {}).get(s, 0.0) for s in d_den.get(c, ())) for c in cats}

    ryp = region_year_power_fractions() if slw else {}
    sub_series = _subnational_annual_series(con) if slw else {}

    out: dict[tuple[str, str], DCell] = {}
    for p in parties:
        for c in cats:
            by_sub: dict[str, list[float]] = {}
            basis = 0.0
            for (cat, ind), s in series.items():
                if cat != c or (cat, ind) not in meta:
                    continue
                submeasure, direction = meta[(cat, ind)]
                net, b = score.attribute_series(s, direction, yp, p, lag, dead)
                if net is None:
                    continue
                by_sub.setdefault(submeasure, []).append(net)
                basis += b
            sub_nets = {sub: sum(v) / len(v) for sub, v in by_sub.items()}

            # C3: region-poolade submåtts-net + år-ekvivalent regionalt ansvarsunderlag.
            subn_by_sub: dict[str, list[float]] = {}
            region_den = 0.0
            region_series = 0
            for (cat, ind), by_region in sub_series.items():
                if cat != c or (c, ind) not in meta:
                    continue
                submeasure, direction = meta[(c, ind)]
                if submeasure not in slw:
                    continue
                snet, den_raw, n_reg = score.attribute_subnational_indicator(
                    by_region, direction, ryp, p, lag, dead
                )
                region_den += den_raw
                region_series += n_reg
                if snet is not None:
                    subn_by_sub.setdefault(submeasure, []).append(snet)
            subn_nets = {sub: sum(v) / len(v) for sub, v in subn_by_sub.items()}
            region_basis = region_den / region_series if region_series else 0.0

            # SOUNDNESS-GRIND (C3, audit pipeline/tools/c3_sensitivity.py): blanda bara in den
            # regionala signalen om det regionala ansvaret är MENINGSFULLT (år-ekvivalent
            # region_basis >= min_responsibility). Annars dominerar ett brusigt teckenmedel ur ett
            # pyttigt region-år-urval submåttet via 0.6-vikten (t.ex. SD som knappt styr någon
            # region). Tröskeln är densamma som den nationella measured-grinden — konsekvent.
            region_used = region_basis >= min_resp
            if not region_used:
                subn_nets = {}
                region_basis = 0.0

            # Blanda nat + region på submåttsnivå för konfigurerade submått (renormaliserat över
            # närvarande sidor): en sida saknas -> andra sidan bär hela vikten.
            blended = dict(sub_nets)
            for sm, w in slw.items():
                num = wsum = 0.0
                if sub_nets.get(sm) is not None:
                    num += sub_nets[sm] * float(w["national"])
                    wsum += float(w["national"])
                if subn_nets.get(sm) is not None:
                    num += subn_nets[sm] * float(w["region"])
                    wsum += float(w["region"])
                if wsum > 0:
                    blended[sm] = num / wsum

            combined_basis = basis + region_basis
            subnational_used = region_used
            cat_net = score.submeasure_weighted_mean(blended, sub_w.get(c, {}))
            # Gate på kombinerat ansvarsunderlag (nationellt + regionalt år-ekv.) — samma storhet
            # som thin-flaggan. < min_resp = ej tillämplig, [min_resp, thin) = uppmätt men tunt,
            # >= thin = uppmätt. (Partier utan något ansvarsår får cat_net=None.)
            measured = cat_net is not None and combined_basis >= min_resp
            if not measured:
                out[(p, c)] = DCell(na_score, False, False, 0.0, total_w[c], False,
                                    subnational_used, region_basis)
                continue
            covered_w = sum(
                sub_w.get(c, {}).get(s, 0.0) for s in blended if s in d_den.get(c, ())
            )
            coverage = covered_w / total_w[c] if total_w[c] else 0.0
            final_net = cat_net
            if shrink:
                net_just = score.weighted_mean_with_neutral_missing(
                    blended, sub_w.get(c, {}), d_den.get(c, ())
                )
                if net_just is not None:  # guard: tom nämnare -> behåll legacy-nätet
                    final_net = net_just
            out[(p, c)] = DCell(
                score.net_support_to_score(final_net), True, combined_basis < thin,
                covered_w, total_w[c], coverage < thin_cov,
                subnational_used, region_basis,
            )
    return out


_CONF_ORDER = ["high", "medium", "low"]


def _step_down_confidence(level: str, steps: int) -> str:
    """Sänker en säkerhetsnivå 'steps' steg (high->medium->low), klampat i botten."""
    i = min(len(_CONF_ORDER) - 1, _CONF_ORDER.index(level) + max(0, steps))
    return _CONF_ORDER[i]


def _b_confidence(conf_cat: float, n_claims: int, thin_coverage: bool) -> str:
    """B:s säkerhet ur evidensen (ADR 0004 punkt 5), sänkt ett steg vid tunn täckning.

    conf_cat är evidensaggregatets confidence rullat upp över kategorin med SAMMA
    undermåttsvikter som B_raw använder. Trösklarna är claims.yaml numeric.confidence läst
    baklänges: high-talet kräver dessutom minst min_claims_for_high_confidence claims bakom
    cellen, alltså regeln som stod i configen men aldrig kördes. Evidenssäkerhet och
    täckningssäkerhet är båda osäkerhet och ska förstärka varandra, inte ersätta varandra —
    därför steget ned i stället för en egen låg-nivå.
    """
    cl = config.claims()
    num = cl["numeric"]["confidence"]
    min_claims = int(cl["aggregation"]["min_claims_for_high_confidence"])
    if conf_cat >= num["high"] and n_claims >= min_claims:
        level = "high"
    elif conf_cat >= num["medium"]:
        level = "medium"
    else:
        level = "low"
    return _step_down_confidence(level, int(thin_coverage))


def category_c(
    nat_frac: dict[str, float], reg_frac: dict[str, float], mun_frac: dict[str, float],
    parties: list[str], cats: list[str],
) -> tuple[dict[str, dict[str, float]], dict[str, str], dict[str, list[str]]]:
    """C (genomförbarhet/ansvar) per kategori: rank-normaliserad c1-makt + säkerhet + flaggor.

    c1 = makt. Subnationell makt = per-kategori region/kommun-split av (reg_frac, mun_frac) enligt
    scoring.subnational_split; den blandas sedan med nationell makt enligt level_weights. Alla
    fraktioner är "andel av tillgänglig makt" i [0,1] -> linjär blandning, rank-normaliseras EN
    gång per kategori (relativ delpoäng). c2 (finansiering) är ännu ej byggd -> C = c1 (ingen
    0.7-multiplikation). Tre fall:
      * forsvar (regional_municipal=0): ren nationell makt, säkerhet oförändrad (hög, per design).
      * subnationell data finns (regioner+kommuner): blanda nat + (region/kommun-split per kategori);
        full täckning -> C:s default-säkerhet (hög), ingen caveat-flagga.
      * subnationell data SAKNAS (guard, t.ex. fil borta): missing_subnational-fallback -> omvikta
        till 100 % nationellt, sänk säkerhet, flagga C_missing_subnational.
    """
    sc = config.scoring()
    ca = sc["C_ansvar"]
    lw_default = ca["level_weights_default"]
    lw_over = ca.get("level_weights_overrides", {})
    split_default = ca["subnational_split_default"]
    split_over = ca.get("subnational_split_overrides", {})
    penalty = int(ca.get("missing_subnational", {}).get("confidence_penalty_steps", 1))
    default_c = sc["uncertainty"]["default_subscore_certainty"]["C"]
    have_subnational = bool(reg_frac) and bool(mun_frac)

    by_cat: dict[str, dict[str, float]] = {}
    conf_by_cat: dict[str, str] = {}
    flags_by_cat: dict[str, list[str]] = {}
    for c in cats:
        lw = lw_over.get(c, lw_default)
        w_reg = float(lw["regional_municipal"])
        if w_reg == 0:
            blended = nat_frac
            conf_by_cat[c] = default_c
            flags_by_cat[c] = ["C_national_only_by_design"]
        elif have_subnational:
            split = split_over.get(c, split_default)
            sr, sm = float(split["region"]), float(split["municipal"])
            w_nat = float(lw["national"])
            subnat = {p: sr * reg_frac.get(p, 0.0) + sm * mun_frac.get(p, 0.0) for p in parties}
            blended = {p: w_nat * nat_frac[p] + w_reg * subnat[p] for p in parties}
            conf_by_cat[c] = default_c       # full region+kommun-täckning -> ingen sänkning
            flags_by_cat[c] = []
        else:
            blended = nat_frac               # guard: subnationell data saknas
            conf_by_cat[c] = _step_down_confidence(default_c, penalty)
            flags_by_cat[c] = ["C_missing_subnational"]
        by_cat[c] = score.rank_normalize(blended)
    return by_cat, conf_by_cat, flags_by_cat


def _source_name(ref: str) -> str:
    for key, name in (("riksdagen", "Riksdagen"), ("regeringskansliet", "Regeringskansliet"),
                      ("scb", "SCB"), ("kolada", "Kolada")):
        if key in ref:
            return name
    return ref.split(":")[0]


def build(con: object | None = None, budget_cfg: dict[str, object] | None = None) -> dict[str, object]:
    """Bygger scores/evidence. budget_cfg=None -> läs config/budget_ramar.yaml (produktion);
    skicka {} (eller en fixtur) för att isolera/injicera a1 i test (jfr budget.a1_shares)."""
    created = con is None
    con = con or warehouse.connect()
    parties = config.party_codes()
    cats = config.category_ids()

    # A (faktiskt agerande) = w_a1*a1 + w_a2*a2 (vikter ur scoring.yaml). Båda är RELATIVA
    # prioriteringsmått (rank-normaliserade över de 8 partierna), inte rå volym.
    #   a2 = motionsprioritering: andel av partiets egna motioner som rör kategorin (full täckning).
    #   a1 = budgetprioritering: andel av partiets föreslagna anslag till kategorins UO (Fas 1b,
    #        gated — se budget.py). a1 vägs in ENDAST för kategorier där grinden är uppfylld;
    #        annars faller A tillbaka på a2 helt (A_a2_only-flagga).
    # A:s normalisering läses ur configen (normalization.per_subscore.A). Configen har alltid
    # deklarerat 'rank' medan koden hårdkodade den; nu styr deklarationen, så ADR 0003 punkt 5
    # kan dra reglaget. Saknad eller okänd nyckel hard-failar — aldrig tyst rank (samma mönster
    # som coverage_mode, spegel av kontrollen i config._validate_scoring).
    a_norm = (config.scoring().get("normalization") or {}).get("per_subscore", {}).get("A")
    if a_norm not in ("rank", "minmax"):
        raise config.ConfigError(
            f"normalization.per_subscore.A={a_norm!r} är ogiltigt (tillåtna: rank, minmax)"
        )
    counts = {(p, c): 0.0 for p in parties for c in cats}
    for p, c, t in con.execute(
        "SELECT party, category, sum(count) FROM party_activity GROUP BY party, category"
    ).fetchall():
        counts[(p, c)] = float(t or 0)
    party_total = {p: sum(counts[(p, c)] for c in cats) for p in parties}
    a2_share = {
        (p, c): (counts[(p, c)] / party_total[p] if party_total[p] else 0.0)
        for p in parties for c in cats
    }
    a2_by_cat = {
        c: score.normalize({p: a2_share[(p, c)] for p in parties}, a_norm) for c in cats
    }

    a1_share, a1_active = budget.a1_shares(cats, parties, ramar_cfg=budget_cfg)
    a_comp = config.scoring()["A_agerande"]["components"]
    w_a1 = float(a_comp["a1_budgetprioritering"])
    w_a2 = float(a_comp["a2_lagstiftningsprioritering"])
    a_by_cat: dict[str, dict[str, float]] = {}
    a_flag_by_cat: dict[str, str] = {}
    for c in cats:
        if c in a1_active:
            # a1_share[(p,c)] finns för alla partier när c är aktiv (grinden garanterar det);
            # direkt indexering => hård fail om en cell mot förmodan saknas (aldrig tyst 0).
            a1_norm = score.normalize({p: a1_share[(p, c)] for p in parties}, a_norm)
            a_by_cat[c] = {p: w_a1 * a1_norm[p] + w_a2 * a2_by_cat[c][p] for p in parties}
            a_flag_by_cat[c] = "A_a1_active"
        else:
            a_by_cat[c] = a2_by_cat[c]
            a_flag_by_cat[c] = "A_a2_only"

    # C: per-kategori c1-makt = nationell + subnationell maktandel, blandad enligt level_weights
    # och rank-normaliserad. Subnationell makt = per-kategori region/kommun-split av SKR-styren
    # (21 regioner + 290 kommuner × 3 mandatperioder, Fas 1c); forsvar = nationellt. Se category_c.
    c_by_cat, c_conf_by_cat, c_flags_by_cat = category_c(
        government_fractions(), regional_fractions(), municipal_fractions(), parties, cats
    )

    # D: resultatattribution (Fas 5b) per (parti, kategori).
    d_res = category_d(con, parties, cats)
    d_cfg = config.scoring()["D_resultat"]
    d_measured_conf = d_cfg["measured_confidence"]
    d_na_conf = d_cfg["not_applicable_confidence"]
    d_shrink = bool(d_cfg.get("coverage_shrink", False))

    # B: partikopplad evidens (Fas 4b). Tom party_positions -> inga effekter -> neutral fallback.
    ee_claims = positions.build_evidence_effect_claims()
    ind_effects = effects.aggregate_effects(ee_claims)
    b_net: dict[tuple[str, str], dict[str, float]] = {}
    # Aggregatets confidence per indikator + antalet claims bakom cellen: B:s säkerhet
    # härleds ur dem (ADR 0004 punkt 5). Innan dess slängdes confidence här.
    b_conf_in: dict[tuple[str, str], dict[str, float]] = {}
    b_n_claims: dict[tuple[str, str], int] = {}
    for e in ind_effects:
        b_net.setdefault((e["party"], e["category"]), {})[e["indicator"]] = e["net_support"]
        b_conf_in.setdefault((e["party"], e["category"]), {})[e["indicator"]] = e["confidence"]
    for cl in ee_claims:
        key = (cl["party"], cl["category"])
        b_n_claims[key] = b_n_claims.get(key, 0) + 1
    meta = _indicator_meta()
    sub_w = _submeasure_weights()
    b_evidens = config.scoring()["B_evidens"]
    b_missing = float(b_evidens["missing_all_score"])
    b_missing_conf = b_evidens["missing_all_confidence"]

    # Coverage-viktning (Fas 4b'): B krymps mot neutral proportionellt mot hur stor andel av
    # kategorins KODBARA åtgärdstyper partiet faktiskt har en ståndpunkt på. Frånvaro av ståndpunkt
    # = "vet ej", inte motstånd -> ett ensamt supports-claim kan inte längre ge maxbetyg i kategorin.
    signed = config.claims()["aggregation"]["signed_direction"]
    ledger_entries = config.evidence_ledger()["entries"]
    pol2cat = {e["policy_type"]: e["category"] for e in ledger_entries}
    b_exclude = set(b_evidens.get("coverage_exclude", []))
    cov_den: dict[str, set[str]] = {}  # kategori -> kodbara åtgärdstyper (signed != 0, ej exkluderade)
    for e in ledger_entries:
        if signed.get(e["direction"], 0) != 0 and e["policy_type"] not in b_exclude:
            cov_den.setdefault(e["category"], set()).add(e["policy_type"])
    cov_num: dict[tuple[str, str], set[str]] = {}  # (parti, kategori) -> kodade åtgärdstyper
    for pos in config.party_positions().get("entries") or []:
        pt, cc = pos.get("policy_type"), pol2cat.get(pos.get("policy_type"))
        if cc and pt in cov_den.get(cc, ()):
            cov_num.setdefault((pos["party"], cc), set()).add(pt)
    thin_cov = float(b_evidens.get("thin_coverage_threshold", 0.5))
    # Krympningen på eller av (ADR 0003 punkt 5 kräver reglaget; scenario 3 kör det avstängt).
    # Default true = committat läge och byte-identiskt med före reglaget.
    b_shrink = bool(b_evidens.get("coverage_shrink", True))

    # B5 (docs/done/b_coverage_krympning_spec.md): täckningsmått-läge. policy_type_count = legacy
    # (byte-identisk baseline, antal kodade åtgärdstyper / kategorins kodbara). weighted_
    # submeasure_depth = viktad undermåttsdjuptäckning cov_B = Σ w_s·|K_s|/|T_s| / Σ w_s
    # över kategorins icke-target-undermått (SAMMA nämnare som D). Okänt läge hard-failar —
    # aldrig tyst fallback till legacy (spec §7).
    b_mode = b_evidens.get("coverage_mode", "policy_type_count")
    if b_mode not in ("policy_type_count", "weighted_submeasure_depth"):
        raise config.ConfigError(
            f"B_evidens.coverage_mode={b_mode!r} är ogiltigt "
            "(tillåtna: policy_type_count, weighted_submeasure_depth)"
        )
    b_codable = _b_codable_types_by_submeasure()  # kategori -> {undermått -> T_s}
    b_nontarget = _non_target_submeasures()       # delad B/D-nämnare (icke-target)

    # Claims (provenance för evidence.json) + index. Sorteras på id så provenansen (claim_refs,
    # särskilt obs_by_cat[:3]-urvalet) blir REPRODUCERBAR — claims byggs annars i hash-randomiserad
    # ordning (set-iteration), vilket gjorde dist/ icke-deterministisk mellan körningar och kunde
    # tyst byta vilka 3 observationsclaims ett betyg pekade på. Betygen påverkas ej av ordningen.
    all_claims = sorted(claims_mod.build_claims(con), key=lambda c: str(c["id"]))
    resp_by_party: dict[str, list[str]] = {}
    action_by_pc: dict[tuple[str, str], str] = {}
    obs_by_cat: dict[str, list[str]] = {}
    for cl in all_claims:
        if cl["type"] == "responsibility":
            resp_by_party.setdefault(cl["party"], []).append(cl["id"])
        elif cl["type"] == "action":
            action_by_pc[(cl["party"], cl["category"])] = cl["id"]
        elif cl["type"] == "observed_result":
            obs_by_cat.setdefault(cl["category"], []).append(cl["id"])

    scores: dict[str, dict[str, object]] = {}
    for p in parties:
        scores[p] = {}
        for c in cats:
            # B: partikopplad evidens, coverage-viktad krympning mot neutral (Fas 4b'/B5).
            b_inputs = b_net.get((p, c))
            if b_mode == "weighted_submeasure_depth":
                # B5: viktad undermåttsdjuptäckning över den delade icke-target-nämnaren
                # (spec §3.3). Gaten nedan använder cov_B: en kodad typ mot ett target-only-
                # undermått ligger utanför nämnaren och gör inte kategorin täckt (spec §3.6).
                t_by_sub = b_codable.get(c, {})
                coded = cov_num.get((p, c), set())
                covered_w, total_w = score.weighted_depth_coverage(
                    {s: ts & coded for s, ts in t_by_sub.items()},
                    t_by_sub, sub_w.get(c, {}), b_nontarget.get(c, ()),
                )
                coverage = covered_w / total_w if total_w else 0.0
                cov_flag = _b_coverage_flag(covered_w, total_w)
            else:  # policy_type_count — legacy, byte-identisk (antal kodade åtgärdstyper)
                den = len(cov_den.get(c, ()))
                num = len(cov_num.get((p, c), ()))
                coverage = (num / den) if den else 0.0
                cov_flag = f"B_coverage_{num}/{den}"
            b_flags: list[str] = []
            if b_inputs and coverage > 0:
                b_weights = {
                    ind: sub_w.get(c, {}).get(meta[(c, ind)][0], 0.0)
                    for ind in b_inputs if (c, ind) in meta
                }
                b_raw = score.aggregate_B(b_inputs, b_weights, missing_all_score=b_missing)
                # krymp mot neutral efter täckning (av -> B_raw, se B_evidens.coverage_shrink)
                b_val = score.coverage_shrink(b_raw, coverage) if b_shrink else b_raw
                b_flags.append(cov_flag)
                thin = coverage < thin_cov
                if thin:
                    b_flags.append("B_thin_coverage")  # beskriver täckningen, inte säkerheten
                # conf_cat: samma undermåttsvikter och samma nämnare som B_raw.
                conf_cat = score.submeasure_weighted_mean(
                    b_conf_in.get((p, c), {}), b_weights
                ) or 0.0
                b_conf = _b_confidence(conf_cat, b_n_claims.get((p, c), 0), thin)
            else:
                b_val, b_conf = b_missing, b_missing_conf
                b_flags.append("B_no_party_evidence")

            d_cell = d_res[(p, c)]
            comps = {"A": a_by_cat[c][p], "B": b_val, "C": c_by_cat[c][p], "D": d_cell.score}
            overrides = {"B": b_conf, "C": c_conf_by_cat[c]}
            flags = list(b_flags)
            flags.append(a_flag_by_cat[c])
            flags += c_flags_by_cat[c]
            if d_cell.measured:
                if d_shrink:
                    # D-bredd synlig per cell; säkerheten sänks kumulativt — tunt
                    # ansvarsunderlag (thin_basis) och tunn bredd (thin_coverage) är
                    # ortogonala. Legacy-grenen (shrink av) förblir byte-identisk.
                    flags.append(
                        f"D_coverage_{d_cell.covered_weight:g}/{d_cell.total_weight:g}"
                    )
                    if d_cell.thin_coverage:
                        flags.append("D_thin_coverage")
                    steps = int(d_cell.thin_basis) + int(d_cell.thin_coverage)
                    overrides["D"] = _step_down_confidence(d_measured_conf, steps)
                else:
                    overrides["D"] = d_measured_conf
                if d_cell.thin_basis:
                    flags.append("D_thin_basis")
                if d_cell.subnational_used:  # C3: regional attribution bidrog till D
                    flags.append(f"D_subnational_region_{d_cell.region_basis:.2g}")
            else:
                overrides["D"] = d_na_conf
                flags.append("D_not_applicable")
            cs = score.category_score_from_components(comps, confidence_overrides=overrides, flags=flags)
            crefs = []
            if (p, c) in action_by_pc:
                crefs.append(action_by_pc[(p, c)])
            crefs += resp_by_party.get(p, [])
            crefs += obs_by_cat.get(c, [])[:3]
            cs["claim_refs"] = crefs
            cs["evidence_refs"] = []
            scores[p][c] = cs

    catinfo = [
        {"id": c["id"], "name": c["name"], "standard_weight": c["standard_weight"],
         "submeasures": [s["id"] for s in c["submeasures"]]}
        for c in config.categories()["categories"]
    ]
    n_positions = len(config.party_positions().get("entries") or [])
    # Fönstrets slut och underlagets slut är två skilda datum (issue #3). window_end är
    # mandatperiodens formella slut och ligger i framtiden tills valet hållits; data_as_of är
    # sista dagen serierna faktiskt når. window_open säger att mandatperioden pågår, alltså att
    # betygen för den är preliminära. Inget av detta rör betygen, bara vad sajten påstår.
    # power_window_end är maktandelens (C:s) fönsterslut och är ett TREDJE datum (issue #14):
    # makt räknas bara till sista avslutade observationsåret, så ingen regering tillgodoräknas
    # dagar den ännu inte suttit. Se POWER_WINDOW_END.
    today = date.today()
    fresh = data_freshness(con, today=today)
    out = {
        "meta": {
            "generated": today.isoformat(), "window": "2014-2026",
            "window_end": WINDOW_END.isoformat(), "window_open": today < WINDOW_END,
            "power_window_end": POWER_WINDOW_END.isoformat(),
            "data_as_of": fresh.as_of, "latest_observation_year": fresh.latest_year,
            "parties": parties, "model_version": 1,
            # coverage = banderollen på sajten: vanlig svenska, för en förstagångsbesökare.
            # coverage_technical = samma körning för granskare, med termer och beslut.
            "coverage": (f"Underlaget i den här versionen: alla {len(cats)} kategorier har betyg "
                         f"i alla tre delar som räknas. Partiernas ståndpunkter bygger på "
                         f"{n_positions} belagda röster och motioner i riksdagen. Hur det gick "
                         "mäts med officiella årsserier. Vem som haft makten räknas både "
                         "nationellt och i regioner och kommuner, men det ger inga poäng och "
                         "visas bara som upplysning. Där underlaget är tunt drar vi betyget mot "
                         "mitten i stället för att gissa."),
            "coverage_technical": (
                "Preliminär: formel 0,30 A + 0,50 B + 0,20 D, C=0 (ADR 0002). "
                "A=prioritering, alltså omfattning och aldrig riktning (ADR 0001): "
                "a2 motionsprioritering, andel av egna motioner, full; "
                "a1 budgetprioritering gated, aktiv för "
                f"{len(a1_active)}/{len(cats)} kategorier ur officiella utgiftsramar "
                "(2023-2025), expertgranskad v1 2026-06-05, annars a2-fallback; "
                "C=maktandel, vikt 0: ger inga poäng utan redovisas som upplysning om "
                "vem som haft makten; räknas per kategori som "
                "nationell regeringsmakt blandad med subnationell "
                "makt (SKR-styren, 21 regioner + 290 kommuner x 3 mandatperioder) via en "
                "per-kategori region/kommun-split efter lagstadgat ansvar; forsvar "
                "nationellt per design; c2 finansiering PARKERAD som designbeslut "
                "2026-06-14 (inget riktningsneutralt finansieringsmått går att bygga ur "
                "officiell svensk data), alltså C=c1 makt; "
                "D=resultatattribution från officiella "
                "årsserier för ALLA 7 kategorier (ekonomi/välfärd/trygghet/klimat/"
                "integration/försvar/demokrati) där partiet haft nationell makt (medel "
                "säkerhet, ej tillämplig för partier utan makt i fönstret); för välfärd "
                "blandas nationell nivå med region-nivå vårdutfall attribuerat till "
                "regionstyrande parti (soundness-grindat); D krymps mot neutral efter "
                "viktad undermåttsbredd. B är AKTIVERAD "
                f"för ALLA 7 kategorier via {n_positions} källbelagda, adversariellt "
                "verifierade + panel-harmoniserade partiståndpunkter (riksdagsvotering/"
                "motion, Fas 4c); B krymps mot neutral efter viktad undermåttsdjuptäckning "
                "(B_thin_coverage-flagga vid tunn täckning). B mäter VÄNTAD STORLEK och "
                "inte riktning (ADR 0004): net_support är ett kvalitetsviktat medel av "
                "storlekar med tecken, Σ(q·m)/Σq med q=evidence_level×confidence och "
                "m=effect_strength×tecken(riktning), så ett ensamt claim ger sin egen "
                "effektstyrka i stället för ±1; B:s säkerhet härleds ur evidensens "
                "confidence (tröskel 0,85/0,60 + min_claims_for_high_confidence) och sänks "
                "ett steg vid tunn täckning. party_positions + "
                "evidence_ledger expertgranskade v2 (mänsklig sign-off 2026-06-07)."),
        },
        "categories": catinfo,
        "scores": scores,
    }
    schema.validate("scores", out)

    evidence = {
        cl["id"]: {"kind": "claim", "statement": cl["statement"],
                   "source_name": _source_name(cl["source_refs"][0])}
        for cl in all_claims + ee_claims
    }
    schema.validate("evidence", evidence)
    if created:
        con.close()
    return {"scores": out, "evidence": evidence}


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    res = build()
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    (DIST_DIR / "scores.json").write_text(
        json.dumps(res["scores"], ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )
    (DIST_DIR / "evidence.json").write_text(
        json.dumps(res["evidence"], ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )
    n_parties = len(res["scores"]["scores"])
    n_cats = len(res["scores"]["categories"])
    print("== Fas 5 ==")
    print(f"dist/scores.json: {n_parties} partier × {n_cats} kategorier")
    print(f"dist/evidence.json: {len(res['evidence'])} claims")
    print("\n-- exempel: total per parti (standardvikter) --")
    std = {c["id"]: c["standard_weight"] for c in config.categories()["categories"]}
    ranking = []
    for p, cats in res["scores"]["scores"].items():
        cat_scores = {c: v["score"] for c, v in cats.items()}
        ranking.append((p, score.total_score(cat_scores, std)))
    for p, t in sorted(ranking, key=lambda x: -x[1]):
        print(f"   {p:4} {t:.2f}")
    print("\n   OBS: preliminär ranking: A (prioritering) + B (coverage-viktade")
    print("   partiståndpunkter, alla kategorier) + D (resultat där makt funnits).")
    print("   C redovisas som maktandel och ger inga poäng. v1 expertgranskad. Ej röstråd.")


if __name__ == "__main__":
    main()
