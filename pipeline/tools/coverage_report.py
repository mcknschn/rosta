"""T3.0: täckningsmatris — vilka (kategori, submått, indikator) har data, vilka saknar?

Läser categories.yaml + warehouse (read-only) och rapporterar:
  - per indikator: finns nationell observation? finns ANNUELL serie (D-duglig)?
  - per submått: täckt (>=1 indikator med obs)?
  - per kategori: har minst en D-duglig (up/down + annuell) indikator?
  - evidensliggaren: antal poster per kategori mot målet >=3 (delpoäng B).

Styr Fas 3: fyll bara submått som faktiskt saknas (undvik att dubblera Fas 2/2b).
Kör: python -m pipeline.tools.coverage_report
"""

from __future__ import annotations

import sys
from typing import Any

from .. import config, score, warehouse
from ..scorerun import (
    _b_codable_types_by_submeasure,
    _d_denominator_submeasures,
    _non_target_submeasures,
)

NATIONAL = ("Riket", "0000")
EVIDENCE_TARGET = 3  # ROADMAP T3.9: >=3 evidence_effect-poster per kategori
# B5-spec §6.4: kategori vars viktade cov_B-TAK ligger under denna grindtröskel måste stå i
# coverage_allowlist.b_thin_breadth_accepted med skäl (tests/test_b_breadth_gate.py). Samma
# nivå som D-grinden (0.75) — taket är kategori-globalt och strängare än runtime-flaggans
# per-parti-tröskel (B_evidens.thin_coverage_threshold 0.5 på cov_B).
B_BREADTH_GATE_THRESHOLD = 0.75


def _observed_series(con: Any) -> dict[tuple[str, str], dict[str, Any]]:
    """(kategori, indikator) -> {n, span, n_annual} ur nationella observationer."""
    rows = con.execute(
        "SELECT category, indicator, period, value FROM observations "
        "WHERE geography IN ('Riket', '0000')"
    ).fetchall()
    out: dict[tuple[str, str], dict[str, Any]] = {}
    for cat, ind, period, val in rows:
        if val is None:
            continue
        rec = out.setdefault((cat, ind), {"n": 0, "periods": [], "years": set()})
        rec["n"] += 1
        rec["periods"].append(str(period))
        y = score.period_to_year(period)
        if y is not None:
            rec["years"].add(y)
    for rec in out.values():
        ps = sorted(rec.pop("periods"))
        rec["span"] = f"{ps[0]}..{ps[-1]}" if ps else "-"
        rec["n_annual"] = len(rec.pop("years"))
    return out


def coverage(con: Any | None = None) -> dict[str, Any]:
    """Strukturerad täckningsrapport (testbar)."""
    created = con is None
    con = con or warehouse.connect(read_only=True)
    observed = _observed_series(con)
    # Bara admitterade poster räknas: en utlyft post (ADR 0006) matar inte B, så en kategori
    # som når EVIDENCE_TARGET enbart tack vare utlyfta poster ska inte rapporteras som täckt.
    ledger = config.admitted_ledger_entries()
    ev_per_cat: dict[str, int] = {}
    for e in ledger:
        ev_per_cat[e["category"]] = ev_per_cat.get(e["category"], 0) + 1

    cats_out: list[dict[str, Any]] = []
    total_ind = covered_ind = annual_ind = 0
    for cat in config.categories()["categories"]:
        cid = cat["id"]
        subs: dict[str, list[dict[str, Any]]] = {s["id"]: [] for s in cat["submeasures"]}
        for ind in cat.get("indicators", []):
            total_ind += 1
            rec = observed.get((cid, ind["id"]))
            has_obs = rec is not None
            d_eligible = ind["direction"] in ("up", "down")
            has_annual = bool(rec and rec["n_annual"] >= 2)
            if has_obs:
                covered_ind += 1
            if has_annual and d_eligible:
                annual_ind += 1
            subs.setdefault(ind["submeasure"], []).append({
                "indicator": ind["id"], "direction": ind["direction"],
                "has_obs": has_obs, "d_eligible": d_eligible,
                "has_annual": has_annual,
                "n": rec["n"] if rec else 0, "span": rec["span"] if rec else "-",
            })
        sub_status = {
            sid: any(i["has_obs"] for i in inds) for sid, inds in subs.items()
        }
        cats_out.append({
            "id": cid,
            "submeasures": subs,
            "submeasure_covered": sub_status,
            "has_d_eligible": any(
                i["has_annual"] and i["d_eligible"] for inds in subs.values() for i in inds
            ),
            "evidence_entries": ev_per_cat.get(cid, 0),
            "evidence_ok": ev_per_cat.get(cid, 0) >= EVIDENCE_TARGET,
        })
    if created:
        con.close()
    return {
        "categories": cats_out,
        "totals": {
            "indicators": total_ind, "indicators_with_obs": covered_ind,
            "indicators_d_eligible_annual": annual_ind,
            "evidence_entries": len(ledger),
            "evidence_target_per_cat": EVIDENCE_TARGET,
        },
    }


def d_submeasure_breadth() -> dict[str, Any]:
    """D-undermåttsbredd (docs/done/d_coverage_krympning_spec.md): viktad icke-target-täckning per kategori.

    Offline-härledning (endast config, jfr b_submeasure_spread): ett undermått räknas D-täckt
    om det har minst en up/down-indikator som INTE är coverage-allowlistad — per Fas 3-gatens
    invariant (test_fas3_gate: inläst ELLER allowlistad, aldrig båda) är en sådan indikator
    inläst med D-duglig serie. Nämnaren = icke-target-undermått (scorerun). Kategori-global
    översikt; scoringens numerator är per (parti, kategori) eftersom attribution kan saknas
    i korta serier.
    """
    allow = {(e["category"], e["indicator"]) for e in config.coverage_allowlist()["allowlist"]}
    d_den = _d_denominator_submeasures()
    thr = float(config.scoring()["D_resultat"].get("thin_coverage_threshold", 0.75))
    cats_out: list[dict[str, Any]] = []
    for cat in config.categories()["categories"]:
        cid = cat["id"]
        weights = {s["id"]: float(s["weight"]) for s in cat["submeasures"]}
        den = d_den[cid]
        covered = {
            ind["submeasure"] for ind in cat.get("indicators", [])
            if ind["direction"] in ("up", "down") and (cid, ind["id"]) not in allow
        } & den
        total_w = sum(weights[s] for s in den)
        covered_w = sum(weights[s] for s in covered)
        ratio = covered_w / total_w if total_w else 0.0
        cats_out.append({
            "id": cid,
            "covered_weight": covered_w, "total_weight": total_w, "ratio": ratio,
            "covered_submeasures": sorted(covered),
            "uncovered_submeasures": sorted(den - covered),
            "thin": ratio < thr,
        })
    return {"threshold": thr, "categories": cats_out}


def b_submeasure_breadth() -> dict[str, Any]:
    """B-undermåttsbredd (docs/done/b_coverage_krympning_spec.md §6.3–6.4): viktat cov_B-TAK per kategori.

    Offline-spegel av d_submeasure_breadth (endast config): ett icke-target-undermått räknas
    B-täckbart om det har minst en kodbar åtgärdstyp (T_s != tom mängd — DELADE regler med
    scoringen via scorerun._b_codable_types_by_submeasure: signed_direction != 0, ej
    coverage_exclude). Viktad andel täckbara undermått = kategorins cov_B-TAK: det värde
    scoringens per-parti-täckning når när ALLA kodbara typer är kodade — B-väggar (T_s tom)
    sänker taket permanent tills de byggs bort (Spår B/B2). Nämnaren = icke-target-undermått
    (scorerun._non_target_submeasures, samma som D). Kategori-global översikt; scoringens
    cov_B är per (parti, kategori) och har dessutom djupledet |K_s|/|T_s|.
    """
    t_by_cat = _b_codable_types_by_submeasure()
    nontarget = _non_target_submeasures()
    thr = B_BREADTH_GATE_THRESHOLD
    cats_out: list[dict[str, Any]] = []
    for cat in config.categories()["categories"]:
        cid = cat["id"]
        weights = {s["id"]: float(s["weight"]) for s in cat["submeasures"]}
        den = nontarget[cid]
        t_subs = t_by_cat.get(cid, {})
        covered = {s for s in den if t_subs.get(s)}
        total_w = sum(weights[s] for s in den)
        covered_w = sum(weights[s] for s in covered)
        ratio = covered_w / total_w if total_w else 0.0
        cats_out.append({
            "id": cid,
            "covered_weight": covered_w, "total_weight": total_w, "ratio": ratio,
            "covered_submeasures": sorted(covered),
            "uncovered_submeasures": sorted(den - covered),
            "thin": ratio < thr,
        })
    return {"threshold": thr, "categories": cats_out}


def b_submeasure_spread() -> dict[str, Any]:
    """BACKLOG B4 — anti-binär audit: hur många DISTINKTA submått har AKTIV B-evidens per kategori?

    Bakgrund: score.aggregate_B är submåttsviktat (b_raw = submåttsviktat medel över de
    indikatorer som har en effekt). Vilar all aktiv evidens i en kategori på ETT submått kan
    en enda ståndpunkt svinga b_raw mellan ytterlägen (0/2.5/5) — kategorin blir "nära-binär".
    Hur mycket coverage-krympningen dämpar detta beror på B_evidens.coverage_mode (B5-spec
    §3.5): i legacy-läget (policy_type_count) är även ett fullkodat enda submått binärt (full
    åtgärdstyps-täckning -> oavkortat anspråk); i weighted_submeasure_depth är gaming
    ekonomiskt verkningslöst (cov_B <= max(w_s)/W -> B kan som mest nå 2.5 ± 0.875). Grinden
    behålls i båda lägena som offline-/sign-off-lager (b_near_binary_accepted) och
    reproducerar BACKLOG-tabellen.

    Aktiv B-evidens i ett submått = en åtgärdstyp som
      (1) har en evidensliggar-post med signed_direction != 0 (ej mixed/unclear) och
          inte ligger i B_evidens.coverage_exclude  (= modellens "kodbara" mängd, cov_den),
      (2) refereras av minst en partiståndpunkt (annars genereras ingen indicator_effect),
      (3) vars indikator hör till submåttet.
    Endast config läses (offline, ingen warehouse).
    """
    signed = config.claims()["aggregation"]["signed_direction"]
    b_exclude = set(config.scoring()["B_evidens"].get("coverage_exclude", []))
    ind_sub: dict[tuple[str, str], str] = {}
    for cat in config.categories()["categories"]:
        for ind in cat.get("indicators", []):
            ind_sub[(cat["id"], ind["id"])] = ind["submeasure"]
    covered_policies = {
        p["policy_type"] for p in (config.party_positions().get("entries") or [])
    }

    # Per kategori: kodbara åtgärdstyper, partitäckta dito, och submått med aktiv evidens.
    codable: dict[str, set[str]] = {}
    party_covered: dict[str, set[str]] = {}
    active_subs: dict[str, set[str]] = {}
    for e in config.admitted_ledger_entries():
        if signed.get(e["direction"], 0) == 0 or e["policy_type"] in b_exclude:
            continue  # inert (mixed/unclear) eller medvetet coverage-exkluderad
        cat = e["category"]
        codable.setdefault(cat, set()).add(e["policy_type"])
        if e["policy_type"] in covered_policies:
            party_covered.setdefault(cat, set()).add(e["policy_type"])
            sub = ind_sub.get((cat, e["indicator"]))
            if sub:
                active_subs.setdefault(cat, set()).add(sub)

    cats_out: list[dict[str, Any]] = []
    for cat in config.categories()["categories"]:
        cid = cat["id"]
        all_subs = [s["id"] for s in cat["submeasures"]]
        covered = active_subs.get(cid, set())
        n_active = len(covered)
        cats_out.append({
            "id": cid,
            "submeasures_total": len(all_subs),
            "submeasures_with_evidence": n_active,
            "covered_submeasures": sorted(covered),
            "uncovered_submeasures": [s for s in all_subs if s not in covered],
            "codable_policy_types": sorted(codable.get(cid, set())),
            "party_covered_policy_types": sorted(party_covered.get(cid, set())),
            "near_binary": n_active <= 1,
        })
    return {"categories": cats_out}


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    rep = coverage()
    print("== Täckningsmatris (T3.0) ==")
    print("  ✓ = nationell observation finns · A = annuell serie (D-duglig) · — = saknas\n")
    for c in rep["categories"]:
        ev = c["evidence_entries"]
        ev_mark = "✓" if c["evidence_ok"] else f"<{rep['totals']['evidence_target_per_cat']}"
        d_mark = "D-data" if c["has_d_eligible"] else "INGEN D-data"
        print(f"[{c['id']}]  ({d_mark}; evidens-poster: {ev} {ev_mark})")
        for sid, inds in c["submeasures"].items():
            scov = "✓" if c["submeasure_covered"][sid] else "—"
            print(f"   {scov} {sid}")
            for i in inds:
                if i["has_obs"]:
                    a = "A" if i["has_annual"] and i["d_eligible"] else " "
                    mark = f"✓{a}"
                    extra = f"{i['n']:>4} obs {i['span']}"
                else:
                    mark = "— "
                    extra = "(saknas)"
                tgt = "" if i["d_eligible"] else "  [target/ej D]"
                print(f"        {mark} {i['indicator']:34} {extra}{tgt}")
    t = rep["totals"]
    print(f"\nSUMMA: {t['indicators_with_obs']}/{t['indicators']} indikatorer har obs · "
          f"{t['indicators_d_eligible_annual']} är D-dugliga (annuell up/down).")
    missing_ev = [c["id"] for c in rep["categories"] if not c["evidence_ok"]]
    print(f"Evidensliggaren: {t['evidence_entries']} poster totalt; "
          f"kategorier under målet ({t['evidence_target_per_cat']}/kat): {', '.join(missing_ev) or 'inga'}")

    # --- D-undermåttsbredd (coverage-krympning): viktad icke-target-täckning per kategori ---
    dsb = d_submeasure_breadth()
    d_on = bool(config.scoring()["D_resultat"].get("coverage_shrink", False))
    print(f"\n== D-undermåttsbredd (coverage_shrink: {'på' if d_on else 'av'},"
          f" tröskel {dsb['threshold']}) ==")
    print("  Viktad icke-target-undermåttstäckning per kategori (kategori-global översikt;"
          " scoringens\n  numerator är per parti/kategori). ⚠ = under tröskeln (D_thin_coverage).\n")
    for c in dsb["categories"]:
        thin = "  ⚠ THIN" if c["thin"] else ""
        print(f"  {c['id']:12} {c['covered_weight']:>4g}/{c['total_weight']:<4g}"
              f"  {c['ratio']:.2f}{thin}")
        if c["uncovered_submeasures"]:
            print(f"        otäckta: {', '.join(c['uncovered_submeasures'])}")

    # --- B-undermåttsbredd (B5): viktat cov_B-tak per kategori (icke-target-nämnare) ---
    bsb = b_submeasure_breadth()
    b_mode = config.scoring()["B_evidens"].get("coverage_mode", "policy_type_count")
    print(f"\n== B-undermåttsbredd (coverage_mode: {b_mode},"
          f" grindtröskel {bsb['threshold']}) ==")
    print("  Viktat cov_B-TAK per kategori (alla kodbara åtgärdstyper kodade; nämnare ="
          " icke-target,\n  delad med D). ⚠ = tak under grindtröskeln"
          " (b_thin_breadth_accepted, spec §6.4).\n")
    for c in bsb["categories"]:
        thin = "  ⚠ THIN" if c["thin"] else ""
        print(f"  {c['id']:12} {c['covered_weight']:>4g}/{c['total_weight']:<4g}"
              f"  {c['ratio']:.2f}{thin}")
        if c["uncovered_submeasures"]:
            print(f"        otäckta: {', '.join(c['uncovered_submeasures'])}")

    # --- B-anti-binär audit (BACKLOG B4): submåttsspridning i partikopplad evidens ---
    accepted = {
        e["category"]: e.get("reason", "")
        for e in (config.coverage_allowlist().get("b_near_binary_accepted") or [])
    }
    bsp = b_submeasure_spread()
    print("\n== B-submåttsspridning (B4: anti-binär) ==")
    print("  Distinkta submått med AKTIV partikopplad evidens / antal submått."
          " ⚠ = nära-binär (≤1).\n")
    for c in sorted(bsp["categories"], key=lambda x: x["submeasures_with_evidence"]):
        n, tot = c["submeasures_with_evidence"], c["submeasures_total"]
        flag = " ⚠ NÄRA-BINÄR" if c["near_binary"] else ""
        acc = "  [accepterad: B2]" if c["near_binary"] and c["id"] in accepted else ""
        print(f"  {n}/{tot}  {c['id']:12}{flag}{acc}")
        if c["covered_submeasures"]:
            print(f"        täckta: {', '.join(c['covered_submeasures'])}")
        if c["near_binary"] and c["uncovered_submeasures"]:
            print(f"        otäckta: {', '.join(c['uncovered_submeasures'])}")
    near = [c["id"] for c in bsp["categories"] if c["near_binary"]]
    unaccounted = [c for c in near if c not in accepted]
    print(f"\nNära-binära kategorier: {', '.join(near) or 'inga'}"
          f"{'  (alla accepterade i allowlist)' if near and not unaccounted else ''}")
    if unaccounted:
        print(f"  ⚠ EJ ACCEPTERADE (regression — lägg i allowlist eller bredda liggaren): "
              f"{', '.join(unaccounted)}")


if __name__ == "__main__":
    main()
