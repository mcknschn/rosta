"""Fas 2/2b-bygge: SCB + Kolada -> observations (delpoäng D). Brå = explicit lucka.

Kör: python -m pipeline.build_fas2
REAL ingest från två live-verifierade öppna API:er. Allt lagras lokalt.

Alla indikator-id är KANONISKA (finns i config/categories.yaml med rätt riktning), så att
serierna faktiskt matar D-attributionen i Fas 5b. SCB-serierna isolerar rätt enskild
nationell serie via 'fixed' (dimensions-koder verifierade mot tabellernas metadata).
Tabeller/KPI:er verifierade live 2026-05-30.
"""

from __future__ import annotations

import sys
from datetime import date

from . import warehouse
from .sources import bra, kolada, scb

# SCB PxWeb-tabeller. 'fixed' fixerar varje icke-Tid-dimension till rätt kodvärde
# (annars väljer loadern dimensionens första index, vilket ofta är fel serie).
SCB_SERIES = [
    {"table": "TAB2891", "indicator": "arbetsloshet", "category": "ekonomi",
     "submeasure": "sysselsattning_arbetsloshet", "unit": "%",
     "fixed": {"Arbetskraftstillh": "ALÖS", "Kon": "1+2", "Alder": "tot15-74",
               "ContentsCode": "AM04011Q"}},
    {"table": "TAB6514", "indicator": "sysselsattning", "category": "ekonomi",
     "submeasure": "sysselsattning_arbetsloshet", "unit": "%",
     "fixed": {"Arbetskraftstillh": "SYSP", "TypData": "O_DATA"}},
    {"table": "TAB6728", "indicator": "bnp_per_capita", "category": "ekonomi",
     "submeasure": "bnp_produktivitet", "unit": "kr (fasta priser, ref 2020)",
     "fixed": {"ContentsCode": "000008DW"}},
    {"table": "TAB4698", "indicator": "territoriella_utslapp", "category": "klimat",
     "submeasure": "utslappsminskningar", "unit": "kt CO2-ekv.",
     "fixed": {"Vaxthusgaser": "CO2-ekv.", "Sektor": "0.1", "ContentsCode": "0000018Q"}},
    {"table": "TAB6439", "indicator": "trangboddhet", "category": "integration",
     "submeasure": "boendesegregation", "unit": "%",
     "fixed": {"Indikator": "B035", "Alder": "16+", "Kon": "00", "ContentsCode": "000007OV"}},
    {"table": "TAB5637", "indicator": "konsumtionsbaserade_utslapp", "category": "klimat",
     "submeasure": "utslappsminskningar", "unit": "ton CO2-ekv.",
     "fixed": {"AmneMiljo": "GHG", "Anvandningstyp": "999"}},
    {"table": "TAB6529", "indicator": "sjalvforsorjningsgrad", "category": "integration",
     "submeasure": "arbete_sjalvforsorjning", "unit": "%",
     "fixed": {"Arbetskraftstillh": "SYSP", "InrikesUtrikes": "23", "TypData": "O_DATA",
               "Kon": "1+2", "Alder": "tot15-74", "ContentsCode": "000007VG"}},
]

# Kolada-KPI:er (Riket = kommun 0000, kön T = totalt via fetch_kpi_series-defaults).
KOLADA_KPIS = [
    {"kpi": "N15507", "indicator": "skolresultat", "category": "valfard",
     "submeasure": "skola_kunskap", "unit": "meritvärdespoäng"},
    {"kpi": "N15813", "indicator": "behoriga_larare", "category": "valfard",
     "submeasure": "skola_kunskap", "unit": "%"},
    {"kpi": "N31825", "indicator": "bidragsberoende", "category": "integration",
     "submeasure": "arbete_sjalvforsorjning", "unit": "%"},
    {"kpi": "N79242", "indicator": "vardkoer", "category": "valfard",
     "submeasure": "vard_tillganglighet", "unit": "antal dagar (median)"},
]


def _purge_unmanaged(con: object) -> int:
    """Tar bort SCB/Kolada-observationer för indikatorer som inte längre hämtas (idempotent).

    Scopas till denna builders EGNA källor (source_ref scb:/kolada:) så att rader från andra
    moduler — t.ex. Brå:s trygghetsdata i Fas 2b — aldrig raderas av misstag.
    """
    managed = sorted({s["indicator"] for s in SCB_SERIES} | {k["indicator"] for k in KOLADA_KPIS})
    if not managed:
        return 0  # tom managed-mängd får aldrig bli "NOT IN ()" (skulle radera allt eget)
    placeholders = ", ".join("?" for _ in managed)
    where = (
        "(source_ref LIKE 'scb:%' OR source_ref LIKE 'kolada:%') "
        f"AND indicator NOT IN ({placeholders})"
    )
    n = con.execute(f"SELECT count(*) FROM observations WHERE {where}", managed).fetchone()[0]
    if n:
        con.execute(f"DELETE FROM observations WHERE {where}", managed)
    return n


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ra = date.today().isoformat()
    con = warehouse.connect()
    print("== Fas 2 ==")

    purged = _purge_unmanaged(con)
    if purged:
        print(f"rensade {purged} föråldrade observationsrader (borttagna/omdöpta serier)")

    for s in SCB_SERIES:
        rows = scb.fetch_series(
            s["table"], s["indicator"], s["category"], s["submeasure"], ra,
            fixed=s["fixed"], unit=s["unit"],
        )
        n = warehouse.upsert(con, "observations", rows)
        span = f"{rows[0]['period']}..{rows[-1]['period']}" if rows else "-"
        print(f"SCB {s['table']:8} -> {s['category']:11} {s['indicator']:22}: {n:4} obs ({span})")

    for k in KOLADA_KPIS:
        title = kolada.kpi_title(k["kpi"])
        rows = kolada.fetch_kpi_series(
            k["kpi"], k["indicator"], k["category"], k["submeasure"], ra, municipality="0000",
            unit=k["unit"],
        )
        n = warehouse.upsert(con, "observations", rows)
        print(f"Kolada {k['kpi']:7} -> {k['category']:11} {k['indicator']:22}: {n:4} obs  ('{title}')")

    # Brå (trygghet, delpoäng D) — Excel, inget API. source_ref 'bra:' ligger utanför
    # _purge_unmanaged-scopet (scb:/kolada:), så raderna rensas aldrig av SCB/Kolada-bygget.
    # Dödligt våld (Tabell 20) + NTU (utsatthet 3A, otrygghet 4A:1).
    bra_rows = bra.fetch_dodligt_vald(ra) + bra.fetch_ntu(ra)
    # Håll bra.INDICATORS (som coverage-gaten läser) i synk med vad som faktiskt skrivs:
    # en framtida Brå-fetch som emitterar en oannonserad indikator ska falla högt här.
    unlisted = {r["indicator"] for r in bra_rows} - set(bra.INDICATORS)
    if unlisted:
        raise ValueError(f"Brå emitterar indikatorer utanför bra.INDICATORS: {sorted(unlisted)}")
    n = warehouse.upsert(con, "observations", bra_rows)
    for ind in bra.INDICATORS:
        sub = [r for r in bra_rows if r["indicator"] == ind]
        span = f"{sub[0]['period']}..{sub[-1]['period']}" if sub else "-"
        print(f"Brå     NTU/SOS   -> trygghet     {ind:22}: {len(sub):4} obs ({span})")

    print("\n-- täckning (observations) --")
    for cat, ind, n, lo, hi in con.execute(
        "SELECT category, indicator, count(*), min(period), max(period) "
        "FROM observations GROUP BY category, indicator ORDER BY 1,2"
    ).fetchall():
        print(f"   {cat:12} {ind:22} {n:4}  {lo}..{hi}")

    print("\n-- kända luckor (loggas, ej tysta; se docs/fas3_coverage.md) --")
    print("   trygghet: dödligt våld (Tabell 20) + NTU utsatthet/otrygghet inlästa (Brå).")
    print("       Uppklaring/handläggning och återfall återstår (separata Brå-tabeller).")
    print("   forsvar/demokrati: till stor del kvalitativa/internationella indikatorer")
    print("       -> ingen officiell svensk årsserie matar D (D = ej tillämplig, allowlistad).")
    con.close()


if __name__ == "__main__":
    main()
