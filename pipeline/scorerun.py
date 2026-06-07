"""Fas 5: warehouse -> dist/scores.json + dist/evidence.json (deploy-artefakten).

Beräknar A/B/C/D per (parti, kategori) deterministiskt och skriver de enda filer som
deployas. Täckningsbunden preliminär körning:
  A = motionsprioritering: andel av egna motioner per kategori (rank-norm.) -> hög säkerhet
  C = regeringsmakt (andel av fönstret, rank-normaliserad, nationellt)  -> hög/medel
  B = neutral 2.5 (ingen partikopplad evidens än)                       -> låg säkerhet
  D = not_applicable 2.5 (attribution byggs i Fas 5b)                   -> låg säkerhet
Osäkerheten speglar detta ärligt. Kör: python -m pipeline.scorerun
"""

from __future__ import annotations

import json
import sys
from datetime import date

from . import DIST_DIR, budget, config, effects, positions, schema, score, warehouse
from . import claims as claims_mod

WINDOW_END = date(2026, 9, 13)  # nästa riksdagsval = fönstrets slut


def _as_date(v: object) -> date:
    """PyYAML kan ge date-objekt eller sträng — coerca till date."""
    return v if isinstance(v, date) else date.fromisoformat(str(v))


def government_fractions() -> dict[str, float]:
    """Andel av fönstret varje parti haft regeringsmakt (stöd vägs 0.5)."""
    gps = config.mappings()["government_periods"]
    parsed = []
    for gp in gps:
        s = _as_date(gp["start"])
        e = _as_date(gp["end"]) if gp.get("end") else WINDOW_END
        parsed.append((s, e, gp.get("parties", []), gp.get("support_parties", [])))
    win_start = min(s for s, _, _, _ in parsed)
    total = (WINDOW_END - win_start).days
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


def _parsed_periods() -> list[tuple[date, date, list[str], list[str]]]:
    out = []
    for gp in config.mappings()["government_periods"]:
        s = _as_date(gp["start"])
        e = _as_date(gp["end"]) if gp.get("end") else WINDOW_END
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


def category_d(
    con: object, parties: list[str], cats: list[str]
) -> dict[tuple[str, str], tuple[float, bool, bool]]:
    """D per (parti, kategori): (betyg, uppmätt?, tunt_underlag?).

    För varje nationell årsindikator tillskrivs riktningsjusterade årsförändringar den
    regering som satt lag-år tidigare (score.attribute_series). Per submått medelvärdesbildas
    indikatorernas net, sedan submåttsviktat medel -> net i [-1,1] -> betyg. Gate: kategorins
    net finns OCH partiets maktandel av fönstret >= min_responsibility, annars ej tillämplig.
    """
    cfg = config.scoring()["D_resultat"]
    lag = int(cfg["attribution_lag_years"])
    dead = float(cfg["change_dead_zone"])
    min_resp = float(cfg["min_responsibility"])
    thin = float(cfg["thin_basis_threshold"])
    na_score = float(cfg["not_applicable_score"])

    yp = year_power_fractions()
    series = _annual_series(con)
    meta = _indicator_meta()
    sub_w = _submeasure_weights()

    out: dict[tuple[str, str], tuple[float, bool, bool]] = {}
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
            cat_net = score.submeasure_weighted_mean(sub_nets, sub_w.get(c, {}))
            # Gate på kategorins EGNA ansvarsunderlag (Σ maktvikt över attribuerade år) — samma
            # storhet som thin-flaggan. Konsekvent: < min_resp = ej tillämplig, [min_resp, thin) =
            # uppmätt men tunt, >= thin = uppmätt. (Partier utan ansvarsår får cat_net=None.)
            measured = cat_net is not None and basis >= min_resp
            if measured:
                out[(p, c)] = (score.net_support_to_score(cat_net), True, basis < thin)
            else:
                out[(p, c)] = (na_score, False, False)
    return out


_CONF_ORDER = ["high", "medium", "low"]


def _step_down_confidence(level: str, steps: int) -> str:
    """Sänker en säkerhetsnivå 'steps' steg (high->medium->low), klampat i botten."""
    i = min(len(_CONF_ORDER) - 1, _CONF_ORDER.index(level) + max(0, steps))
    return _CONF_ORDER[i]


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
    a2_by_cat = {c: score.rank_normalize({p: a2_share[(p, c)] for p in parties}) for c in cats}

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
            a1_norm = score.rank_normalize({p: a1_share[(p, c)] for p in parties})
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

    # B: partikopplad evidens (Fas 4b). Tom party_positions -> inga effekter -> neutral fallback.
    ee_claims = positions.build_evidence_effect_claims()
    ind_effects = effects.aggregate_effects(ee_claims)
    b_net: dict[tuple[str, str], dict[str, float]] = {}
    for e in ind_effects:
        b_net.setdefault((e["party"], e["category"]), {})[e["indicator"]] = e["net_support"]
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
            # B: partikopplad evidens, coverage-viktad krympning mot neutral (Fas 4b').
            b_inputs = b_net.get((p, c))
            den = len(cov_den.get(c, ()))
            num = len(cov_num.get((p, c), ()))
            coverage = (num / den) if den else 0.0
            b_flags: list[str] = []
            if b_inputs and coverage > 0:
                b_weights = {
                    ind: sub_w.get(c, {}).get(meta[(c, ind)][0], 0.0)
                    for ind in b_inputs if (c, ind) in meta
                }
                b_raw = score.aggregate_B(b_inputs, b_weights, missing_all_score=b_missing)
                b_val = 2.5 + (b_raw - 2.5) * coverage  # krymp mot neutral efter täckning
                b_flags.append(f"B_coverage_{num}/{den}")
                if coverage < thin_cov:
                    b_conf = "low"
                    b_flags.append("B_thin_coverage")
                else:
                    b_conf = "medium"
            else:
                b_val, b_conf = b_missing, b_missing_conf
                b_flags.append("B_no_party_evidence")

            d_score, d_measured, d_thin = d_res[(p, c)]
            comps = {"A": a_by_cat[c][p], "B": b_val, "C": c_by_cat[c][p], "D": d_score}
            overrides = {"B": b_conf, "C": c_conf_by_cat[c]}
            flags = list(b_flags)
            flags.append(a_flag_by_cat[c])
            flags += c_flags_by_cat[c]
            if d_measured:
                overrides["D"] = d_measured_conf
                if d_thin:
                    flags.append("D_thin_basis")
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
    out = {
        "meta": {
            "generated": date.today().isoformat(), "window": "2014-2026",
            "parties": parties, "model_version": 1,
            "coverage": (f"Preliminär: A=agerande (a2 motionsprioritering, andel av egna "
                         f"motioner, full; a1 budgetprioritering gated — aktiv för "
                         f"{len(a1_active)}/{len(cats)} kategorier ur officiella utgiftsramar "
                         "(2023–2025), expertgranskad v1 2026-06-05, annars a2-fallback); "
                         "C=makt per kategori: nationell regeringsmakt blandad med subnationell "
                         "makt (SKR-styren, 21 regioner + 290 kommuner × 3 mandatperioder) via en "
                         "per-kategori region/kommun-split efter lagstadgat ansvar; forsvar "
                         "nationellt per design; c2 finansiering ännu ej byggd (C=c1 makt); "
                         "D=resultatattribution från officiella "
                         "årsserier för ALLA 7 kategorier (ekonomi/välfärd/trygghet/klimat/"
                         "integration/försvar/demokrati) där partiet haft nationell makt (medel "
                         "säkerhet, ej tillämplig för partier utan makt i fönstret, t.ex. V). B är AKTIVERAD "
                         f"för ALLA 7 kategorier via {n_positions} källbelagda, adversariellt "
                         "verifierade + panel-harmoniserade partiståndpunkter (riksdagsvotering/"
                         "motion, Fas 4c); coverage-viktad (B krymps mot neutral efter andel kodade "
                         "åtgärdstyper, B_thin_coverage-flagga vid tunn täckning). party_positions + "
                         "evidence_ledger expertgranskade v1 (mänsklig sign-off 2026-06-05)."),
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
    print("\n   OBS: preliminär ranking: A (aktivitet) + B (coverage-viktade partiståndpunkter,")
    print("   alla kategorier) + C (makt) + D (resultat där makt funnits). v1 expertgranskad. Ej röstråd.")


if __name__ == "__main__":
    main()
