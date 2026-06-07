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

from . import expectations, warehouse
from .sources import bra, kolada, scb

# SCB PxWeb-tabeller. 'fixed' fixerar varje icke-Tid-dimension till rätt kodvärde
# (annars väljer loadern dimensionens första index, vilket ofta är fel serie).
# 'expect' = serie-drift-förväntan (pipeline.expectations), grov med flit: fångar fel/tom/stale
# serie, inte exakta tal. Ankare = stabila publicerade värden (slutår, ±rel_tol) som pinnar seriens
# identitet — fångar en fel-men-rimlig dimension som value_range ensamt släpper igenom.
SCB_SERIES = [
    {"table": "TAB2891", "indicator": "arbetsloshet", "category": "ekonomi",
     "submeasure": "sysselsattning_arbetsloshet", "unit": "%",
     "fixed": {"Arbetskraftstillh": "ALÖS", "Kon": "1+2", "Alder": "tot15-74",
               "ContentsCode": "AM04011Q"},
     "expect": {"min_points": 15, "value_range": [3, 15], "min_latest_year": 2024,
                "anchors": {"2020": 8.5}}},
    {"table": "TAB6514", "indicator": "sysselsattning", "category": "ekonomi",
     "submeasure": "sysselsattning_arbetsloshet", "unit": "%",
     "fixed": {"Arbetskraftstillh": "SYSP", "TypData": "O_DATA"},
     "expect": {"min_points": 15, "value_range": [55, 80], "min_latest_year": 2024,
                "anchors": {"2020": 66.8}}},
    {"table": "TAB6728", "indicator": "bnp_per_capita", "category": "ekonomi",
     "submeasure": "bnp_produktivitet", "unit": "kr (fasta priser, ref 2020)",
     "fixed": {"ContentsCode": "000008DW"},
     "expect": {"min_points": 20, "value_range": [200000, 700000], "min_latest_year": 2023,
                "anchors": {"2020": 484000}}},
    {"table": "TAB4698", "indicator": "territoriella_utslapp", "category": "klimat",
     "submeasure": "utslappsminskningar", "unit": "kt CO2-ekv.",
     "fixed": {"Vaxthusgaser": "CO2-ekv.", "Sektor": "0.1", "ContentsCode": "0000018Q"},
     "expect": {"min_points": 20, "value_range": [20000, 100000], "min_latest_year": 2022,
                "anchors": {"2020": 45968.6}}},
    {"table": "TAB6439", "indicator": "trangboddhet", "category": "integration",
     "submeasure": "boendesegregation", "unit": "%",
     "fixed": {"Indikator": "B035", "Alder": "16+", "Kon": "00", "ContentsCode": "000007OV"},
     "expect": {"min_points": 8, "value_range": [1, 12], "min_latest_year": 2023}},
    {"table": "TAB5637", "indicator": "konsumtionsbaserade_utslapp", "category": "klimat",
     "submeasure": "utslappsminskningar", "unit": "ton CO2-ekv.",
     "fixed": {"AmneMiljo": "GHG", "Anvandningstyp": "999"},
     "expect": {"min_points": 10, "value_range": [50000000, 150000000], "min_latest_year": 2021,
                "anchors": {"2018": 95274815}}},
    {"table": "TAB6529", "indicator": "sjalvforsorjningsgrad", "category": "integration",
     "submeasure": "arbete_sjalvforsorjning", "unit": "%",
     "fixed": {"Arbetskraftstillh": "SYSP", "InrikesUtrikes": "23", "TypData": "O_DATA",
               "Kon": "1+2", "Alder": "tot15-74", "ContentsCode": "000007VG"},
     "expect": {"min_points": 12, "value_range": [40, 80], "min_latest_year": 2024,
                "anchors": {"2020": 59.2}}},
    # naringslivets_investeringar (ekonomi -> foretagande_investeringar, riktning up): näringslivets
    # FASTA bruttoinvesteringar i FASTA priser (volym, ref 2020) ur BNP-användningssidan (TAB3610,
    # samma tabellfamilj som produktivitetens BNP-täljare). Anvandningstyp=BNAR ("näringslivets fasta
    # bruttoinv"); fasta priser separerar volym från pris så D:s årstecken mäter reell investering,
    # inte inflation. D-aktiverad 2026-06-07 (Spår D Tier 1, v0); konjunkturkänslig -> D tar bara
    # TECKEN (ej magnitud), makt-/ansvarsviktas och väger 10 % (jfr ekonomi-caveat, IDEA.md).
    {"table": "TAB3610", "indicator": "naringslivets_investeringar", "category": "ekonomi",
     "submeasure": "foretagande_investeringar", "unit": "mnkr (fasta priser, ref 2020)",
     "fixed": {"Anvandningstyp": "BNAR", "ContentsCode": "000000RN"},
     "expect": {"min_points": 20, "value_range": [200000, 1300000], "min_latest_year": 2023,
                "anchors": {"2020": 972986}}},
    # sfi_sprakkunskaper (integration -> skola_sprak, riktning up): andel personer GODKÄNDA i
    # svenska för invandrare (procent), SCB:s officiella sfi-statistik TAB1814 (Skolverket är
    # statistikansvarig, SCB producent). ContentsCode AA0003EB = "Andel godkända i sfi, procent".
    # SEMANTIKVAL (§5.2) avgjort av datan: tabellen har två mått — godkäntandel (AA0003EB, up) och
    # vistelsetid-median (AA0003EC, down). Bara godkäntandel matchar indikatorns kanoniska riktning
    # (up) -> det är det enda direktionskonsistenta valet utan att omdefiniera indikatorn.
    # METODBROTT 2022 (SCB-not: kursbetyg G/I/– + sista kursdag 1 jan fr.o.m. 2022): SCB publicerar
    # ändå EN obruten serie 1997–2023, och de två brott-närliggande övergångarna (2021->2022 = −,
    # 2022->2023 = +) är teckenkonsistenta med den genuina nedgång-/stabiliseringstrenden. Eftersom D
    # bara tar TECKEN (ej magnitud) ändrar metodbrottet magnituden men inte tecknet -> hela serien
    # behålls (till skillnad från NTU, där SCB delade serien och nivåerna var ojämförbara). v0, flaggad.
    {"table": "TAB1814", "indicator": "sfi_sprakkunskaper", "category": "integration",
     "submeasure": "skola_sprak", "unit": "% godkända i sfi",
     "fixed": {"Region": "00", "Kon": "1+2", "Bakgrund": "000", "ContentsCode": "AA0003EB"},
     "expect": {"min_points": 20, "value_range": [25, 55], "min_latest_year": 2023,
                "anchors": {"2020": 32.3, "2004": 46.4}}},
]

# Kolada-KPI:er (Riket = kommun 0000, kön T = totalt via fetch_kpi_series-defaults).
KOLADA_KPIS = [
    {"kpi": "N15507", "indicator": "skolresultat", "category": "valfard",
     "submeasure": "skola_kunskap", "unit": "meritvärdespoäng",
     "expect": {"min_points": 8, "value_range": [200, 250], "min_latest_year": 2024,
                "anchors": {"2018": 230.0}}},
    {"kpi": "N15813", "indicator": "behoriga_larare", "category": "valfard",
     "submeasure": "skola_kunskap", "unit": "%",
     "expect": {"min_points": 8, "value_range": [60, 85], "min_latest_year": 2024,
                "anchors": {"2018": 70.54}}},
    {"kpi": "N31825", "indicator": "bidragsberoende", "category": "integration",
     "submeasure": "arbete_sjalvforsorjning", "unit": "%",
     "expect": {"min_points": 10, "value_range": [1, 6], "min_latest_year": 2023}},
    {"kpi": "N79242", "indicator": "vardkoer", "category": "valfard",
     "submeasure": "vard_tillganglighet", "unit": "antal dagar (median)",
     "expect": {"min_points": 3, "value_range": [20, 200], "min_latest_year": 2023,
                "anchors": {"2022": 65.0}}},
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
        expectations.check_series(rows, s.get("expect"), f"SCB {s['table']} {s['indicator']}")
        n = warehouse.upsert(con, "observations", rows)
        span = f"{rows[0]['period']}..{rows[-1]['period']}" if rows else "-"
        print(f"SCB {s['table']:8} -> {s['category']:11} {s['indicator']:22}: {n:4} obs ({span})")

    for k in KOLADA_KPIS:
        title = kolada.kpi_title(k["kpi"])
        rows = kolada.fetch_kpi_series(
            k["kpi"], k["indicator"], k["category"], k["submeasure"], ra, municipality="0000",
            unit=k["unit"],
        )
        expectations.check_series(rows, k.get("expect"), f"Kolada {k['kpi']} {k['indicator']}")
        n = warehouse.upsert(con, "observations", rows)
        print(f"Kolada {k['kpi']:7} -> {k['category']:11} {k['indicator']:22}: {n:4} obs  ('{title}')")

    # Brå (trygghet, delpoäng D) — Excel, inget API. source_ref 'bra:' ligger utanför
    # _purge_unmanaged-scopet (scb:/kolada:), så raderna rensas aldrig av SCB/Kolada-bygget.
    # Dödligt våld (Tabell 20) + NTU (utsatthet 3A, otrygghet 4A:1) + personuppklaring (10La).
    bra_rows = bra.fetch_dodligt_vald(ra) + bra.fetch_ntu(ra) + bra.fetch_personuppklaring(ra)
    # Håll bra.INDICATORS (som coverage-gaten läser) i synk med vad som faktiskt skrivs:
    # en framtida Brå-fetch som emitterar en oannonserad indikator ska falla högt här.
    unlisted = {r["indicator"] for r in bra_rows} - set(bra.INDICATORS)
    if unlisted:
        raise ValueError(f"Brå emitterar indikatorer utanför bra.INDICATORS: {sorted(unlisted)}")
    for ind in bra.INDICATORS:
        expectations.check_series(
            [r for r in bra_rows if r["indicator"] == ind], bra.EXPECT.get(ind), f"Brå {ind}"
        )
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
    print("   trygghet: dödligt våld (Tabell 20) + NTU utsatthet/otrygghet + personuppklaring "
          "(10La) inlästa (Brå).")
    print("       Handläggningstid/genomströmning och återfall återstår (separata Brå-tabeller).")
    print("   forsvar/demokrati: till stor del kvalitativa/internationella indikatorer")
    print("       -> ingen officiell svensk årsserie matar D (D = ej tillämplig, allowlistad).")
    con.close()


if __name__ == "__main__":
    main()
