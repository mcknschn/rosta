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

NATIONAL = ("Riket", "0000")
EVIDENCE_TARGET = 3  # ROADMAP T3.9: >=3 evidence_effect-poster per kategori


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
    ledger = config.evidence_ledger().get("entries") or []
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


if __name__ == "__main__":
    main()
