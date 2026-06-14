"""C3 — subnationell D: region-nivå vårdserier -> observations (geography = Kolada-regionkod).

Hämtar samma kanoniska välfärds-vårdindikatorer som build_fas2 men på REGIONNIVÅ (de 21
regionerna; Kolada 4-siffrig regionkod 0001=Region Stockholm ... 0025=Norrbotten), så scorerun
kan attribuera regionalt utfall till det parti som styrde regionen (docs/done/c3_subnational_d_metod.md).
Regionen är sjukvårdshuvudman => vård är den rena, neutrala ansvarskopplingen (kortare köer /
högre överlevnad är icke-ideologiska mål). De NATIONELLA serierna (geography 0000) rörs inte —
subnationell D blandas in på submåttsnivå parallellt med den nationella attributionen.

Idempotent (obs-id innehåller region + period -> INSERT OR REPLACE). Kör:
  python -m pipeline.build_subnational

REAL ingest från Kolada v3 (öppen och kostnadsfri, RKA). Live-verifierat 2026-06-14:
U70471 2010-2025/region (16 år), N79242 2021-2025/region (5 år).
"""

from __future__ import annotations

import sys
from datetime import date

from . import config, warehouse
from .sources import kolada

# Region-nivå KPI:er. Samma kanoniska indikator-id / kategori / submått / riktning som de
# nationella (build_fas2 KOLADA_KPIS) — bara geografin skiljer. Endast vard_tillganglighet:
# regionen är lagstadgad sjukvårdshuvudman, så vård är den enda submåttsnivå där en region-
# attribution är en ren, neutral ansvarskoppling (skola/omsorg är kommunala -> framtida våg).
REGION_KPIS = [
    {"kpi": "N79242", "indicator": "vardkoer", "category": "valfard",
     "submeasure": "vard_tillganglighet", "unit": "antal dagar (median, region)",
     "value_range": (0, 400)},
    {"kpi": "U70471", "indicator": "overlevnad_svar_sjukdom", "category": "valfard",
     "submeasure": "vard_tillganglighet",
     "unit": "% (30-dagarsöverlevnad akut tjocktarmscancerkir., region)",
     "value_range": (60, 100)},
]


def region_kolada_code(config_key: str) -> str:
    """Config-regionnyckel ('01') -> Kolada 4-siffrig regionkod ('0001')."""
    return f"{int(config_key):04d}"


def managed_region_codes() -> list[str]:
    """Kolada-koder för de regioner C3 attribuerar (alla i subnational_governance.regions)."""
    regions = config.mappings()["subnational_governance"]["regions"]
    return [region_kolada_code(k) for k in regions]


def _purge_stale(con: object, region_codes: list[str], managed_indicators: set[str]) -> int:
    """Tar bort region-geo Kolada-obs för indikatorer som inte längre hämtas här (idempotent).

    Scopas hårt till (kolada-källa) ∩ (våra regionkoder) ∩ (indikator EJ längre managerad), så
    nationella rader (geography 0000) och ev. framtida kommunrader aldrig rörs av misstag.
    """
    if not managed_indicators:
        return 0
    geo_ph = ", ".join("?" for _ in region_codes)
    ind_ph = ", ".join("?" for _ in managed_indicators)
    where = (
        f"source_ref LIKE 'kolada:%' AND geography IN ({geo_ph}) "
        f"AND indicator NOT IN ({ind_ph})"
    )
    params = [*region_codes, *sorted(managed_indicators)]
    n = con.execute(f"SELECT count(*) FROM observations WHERE {where}", params).fetchone()[0]
    if n:
        con.execute(f"DELETE FROM observations WHERE {where}", params)
    return n


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ra = date.today().isoformat()
    con = warehouse.connect()
    print("== C3: subnationell D (region-nivå vård) ==")

    region_keys = list(config.mappings()["subnational_governance"]["regions"].keys())
    region_codes = [region_kolada_code(k) for k in region_keys]
    managed = {k["indicator"] for k in REGION_KPIS}

    purged = _purge_stale(con, region_codes, managed)
    if purged:
        print(f"rensade {purged} föråldrade region-observationer (borttagna/omdöpta serier)")

    total = 0
    for k in REGION_KPIS:
        lo, hi = k["value_range"]
        kpi_rows: list[dict[str, object]] = []
        covered = 0
        for key in region_keys:
            code = region_kolada_code(key)
            rows = kolada.fetch_kpi_series(
                k["kpi"], k["indicator"], k["category"], k["submeasure"], ra,
                municipality=code, unit=k["unit"],
            )
            rows = [r for r in rows if r["value"] is not None]
            if rows:
                covered += 1
            kpi_rows.extend(rows)
        # Sanity (grov, med flit): minst hälften av regionerna har serie OCH alla värden rimliga
        # (fångar fel KPI/geo-format eller en trasig enhetsskala — inte exakta tal).
        if covered < len(region_keys) // 2:
            raise ValueError(
                f"Kolada {k['kpi']} {k['indicator']}: bara {covered}/{len(region_keys)} regioner "
                "har data — fel KPI eller regionkodformat?"
            )
        bad = [(r["geography"], r["period"], r["value"]) for r in kpi_rows if not (lo <= r["value"] <= hi)]
        if bad:
            raise ValueError(
                f"Kolada {k['kpi']} {k['indicator']}: {len(bad)} värden utanför "
                f"[{lo},{hi}], ex {bad[:3]}"
            )
        n = warehouse.upsert(con, "observations", kpi_rows)
        total += n
        periods = sorted({r["period"] for r in kpi_rows})
        span = f"{periods[0]}..{periods[-1]}" if periods else "-"
        print(
            f"Kolada {k['kpi']:7} -> {k['category']:8} {k['indicator']:24}: "
            f"{n:4} obs, {covered:2}/{len(region_keys)} regioner ({span})"
        )

    print(f"\nTotalt {total} region-observationer i warehouse (geography = Kolada-regionkod).")
    print("Subnationell D matas nu in via scorerun.category_d (D_resultat.subnational.enabled).")
    con.close()


if __name__ == "__main__":
    main()
