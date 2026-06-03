"""O2: synliggör betygsdrift mellan körningar (snapshot + diff av dist/scores.json).

dist/scores.json räknas om varje gång data uppdateras. Utan ett spår är det lätt att en
dataändring tyst flyttar betyg/ranking. Det här verktyget reducerar scores.json till en kompakt
SNAPSHOT (ranking med standardvikter + betyg per parti×kategori + flaggor) och DIFFAR mot en
committad baslinje (dist/scores.snapshot.json). Så varje omräkning kan visa exakt vad som rörde sig.

    python -m pipeline.tools.score_diff           # diffa dist/scores.json mot baslinjen
    python -m pipeline.tools.score_diff --write    # uppdatera baslinjen efter en granskad ändring

Rena funktioner (summarize/diff_snapshots) -> golden-testbara utan fil-IO. Ingen betygslogik här.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from .. import DIST_DIR

SNAPSHOT_PATH = DIST_DIR / "scores.snapshot.json"
_ROUND = 3


def _total(cat_scores: dict[str, float], weights: dict[str, float]) -> float:
    wsum = sum(weights.values())
    return round(sum(cat_scores[c] * weights[c] for c in cat_scores) / wsum, _ROUND) if wsum else 0.0


def summarize(scores: dict[str, Any]) -> dict[str, Any]:
    """scores.json -> kompakt snapshot: total per parti (standardvikt), betyg + flaggor per cell."""
    weights = {c["id"]: float(c["standard_weight"]) for c in scores["categories"]}
    cells: dict[str, dict[str, Any]] = {}
    totals: dict[str, float] = {}
    for party, cats in scores["scores"].items():
        cat_scores = {c: round(float(v["score"]), _ROUND) for c, v in cats.items()}
        totals[party] = _total(cat_scores, weights)
        for c, v in cats.items():
            cells[f"{party}/{c}"] = {
                "score": round(float(v["score"]), _ROUND),
                "flags": sorted(v.get("flags", [])),
            }
    ranking = [p for p, _ in sorted(totals.items(), key=lambda kv: -kv[1])]
    return {"totals": totals, "ranking": ranking, "cells": cells}


def diff_snapshots(old: dict[str, Any], new: dict[str, Any]) -> list[str]:
    """Människoläsbara skillnader mellan två snapshots (ranking, totaler, cellbetyg, flaggor)."""
    out: list[str] = []
    if old.get("ranking") != new.get("ranking"):
        out.append(f"RANKING: {' > '.join(old.get('ranking', []))}  ->  "
                   f"{' > '.join(new.get('ranking', []))}")
    for p, t in new.get("totals", {}).items():
        t0 = old.get("totals", {}).get(p)
        if t0 is not None and abs(t0 - t) >= 0.001:
            out.append(f"TOTAL {p}: {t0:+.3f} -> {t:+.3f} ({t - t0:+.3f})")
    oc, nc = old.get("cells", {}), new.get("cells", {})
    for key in sorted(set(oc) | set(nc)):
        o, n = oc.get(key), nc.get(key)
        if o is None:
            out.append(f"NY CELL {key}: {n['score']}")
        elif n is None:
            out.append(f"BORTTAGEN CELL {key}")
            continue
        else:
            if abs(o["score"] - n["score"]) >= 0.001:
                out.append(f"BETYG {key}: {o['score']} -> {n['score']} ({n['score'] - o['score']:+.3f})")
            if o["flags"] != n["flags"]:
                added = sorted(set(n["flags"]) - set(o["flags"]))
                removed = sorted(set(o["flags"]) - set(n["flags"]))
                parts = []
                if added:
                    parts.append(f"+{added}")
                if removed:
                    parts.append(f"-{removed}")
                out.append(f"FLAGGOR {key}: {' '.join(parts)}")
    return out


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    write = "--write" in sys.argv[1:]
    scores = json.loads((DIST_DIR / "scores.json").read_text(encoding="utf-8"))
    new = summarize(scores)

    if write:
        SNAPSHOT_PATH.write_text(json.dumps(new, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Baslinje uppdaterad: {SNAPSHOT_PATH.name} "
              f"({len(new['totals'])} partier, ranking {' > '.join(new['ranking'])})")
        return

    if not SNAPSHOT_PATH.exists():
        raise SystemExit("Ingen baslinje än — kör `python -m pipeline.tools.score_diff --write`.")
    old = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
    changes = diff_snapshots(old, new)
    if not changes:
        print(f"Inga betygsändringar mot baslinjen (ranking {' > '.join(new['ranking'])}).")
        return
    print(f"== Betygsdrift mot {SNAPSHOT_PATH.name} ({len(changes)} ändringar) ==")
    for c in changes:
        print(f"  {c}")
    print("\nGranska ändringarna; uppdatera baslinjen med --write när de är förväntade.")


if __name__ == "__main__":
    main()


def _read_snapshot(path: Path) -> dict[str, Any]:  # bekvämlighet för tester/återanvändning
    return json.loads(path.read_text(encoding="utf-8"))
