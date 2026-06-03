"""Fas 3-bygge: sektorsmyndigheter -> observations (delpoäng D, återstående indikatorer).

Kör: python -m pipeline.build_fas3
REAL ingest från live-verifierade öppna svenska API:er. Allt lagras lokalt i data/.

Idag: Energimyndigheten (PxWeb v1) -> klimat/fossil_energianvandning (slutlig fossil
energianvändning, TWh). Indikator-id är kanoniskt (categories.yaml) och annuellt, så det
matar D-attributionen i Fas 5b automatiskt. Källor utanför build_fas2:s _purge-scope
(scb:/kolada:) — egna source_ref-prefix, idempotent via INSERT OR REPLACE på id.
"""

from __future__ import annotations

import sys
from datetime import date

from . import derived, expectations, warehouse
from .sources import energimyndigheten


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ra = date.today().isoformat()
    con = warehouse.connect()
    print("== Fas 3 (sektorsadaptrar) ==")

    rows = energimyndigheten.fetch_fossil_energy(ra)
    # Håll energimyndigheten.INDICATORS (som coverage-gaten läser) i synk med vad som skrivs.
    unlisted = {r["indicator"] for r in rows} - set(energimyndigheten.INDICATORS)
    if unlisted:
        raise ValueError(f"Energimyndigheten emitterar indikatorer utanför INDICATORS: {sorted(unlisted)}")
    for ind in energimyndigheten.INDICATORS:
        expectations.check_series(
            [r for r in rows if r["indicator"] == ind], energimyndigheten.EXPECT.get(ind),
            f"Energimyndigheten {ind}",
        )
    n = warehouse.upsert(con, "observations", rows)
    span = f"{rows[0]['period']}..{rows[-1]['period']}" if rows else "-"
    print(f"Energimyndigheten EN0202_8 -> klimat       fossil_energianvandning: {n:4} obs ({span})")

    # Härledda indikatorer (gap/kvot ur verifierade serier) — source_ref 'derived:' ligger utanför
    # build_fas2:s scb/kolada-purge-scope, så raderna rensas aldrig av SCB/Kolada-bygget.
    drows = derived.fetch_derived(ra)
    unlisted = {r["indicator"] for r in drows} - set(derived.INDICATORS)
    if unlisted:
        raise ValueError(f"Härledda emitterar indikatorer utanför derived.INDICATORS: {sorted(unlisted)}")
    for spec in derived.DERIVED:
        expectations.check_series(
            [r for r in drows if r["indicator"] == spec["indicator"]], spec.get("expect"),
            f"Härledd {spec['indicator']}",
        )
    n = warehouse.upsert(con, "observations", drows)
    for spec in derived.DERIVED:
        sub = [r for r in drows if r["indicator"] == spec["indicator"]]
        span = f"{sub[0]['period']}..{sub[-1]['period']}" if sub else "-"
        print(f"Härledd (SCB)  -> {spec['category']:11} {spec['indicator']:30}: {len(sub):4} obs ({span})")

    print("\n-- täckning (klimat, observations) --")
    for cat, ind, n, lo, hi in con.execute(
        "SELECT category, indicator, count(*), min(period), max(period) "
        "FROM observations WHERE category='klimat' GROUP BY category, indicator ORDER BY 2"
    ).fetchall():
        print(f"   {cat:12} {ind:24} {n:4}  {lo}..{hi}")

    print("\n-- kända luckor (loggas, ej tysta; se docs/fas3_coverage.md) --")
    print("   klimat: elprisvolatilitet/effektbrist (Svk, härledda) återstår.")
    print("   forsvar/demokrati: kvalitativa/internationella indikatorer -> ingen officiell")
    print("       svensk årsserie matar D (allowlistade).")
    con.close()


if __name__ == "__main__":
    main()
