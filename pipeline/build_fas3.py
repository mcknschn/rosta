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
from .sources import energimyndigheten, forsvarsmakten, kriminalvarden, polisen, regeringen


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

    # Polisen: bekräftade skjutningar + sprängningar (trygghet, delpoäng D) — transkriberad config,
    # ingen runtime-PDF-parser (config/skjutningar_sprangningar.yaml; reproducerbar via
    # tools/skjutningar_transcribe). source_ref 'polisen:' ligger utanför scb/kolada-purge-scope.
    prows = polisen.build_skjutningar_sprangningar_observations()
    unlisted = {r["indicator"] for r in prows} - set(polisen.INDICATORS)
    if unlisted:
        raise ValueError(f"Polisen emitterar indikatorer utanför polisen.INDICATORS: {sorted(unlisted)}")
    for ind in polisen.INDICATORS:
        expectations.check_series(
            [r for r in prows if r["indicator"] == ind], polisen.EXPECT.get(ind), f"Polisen {ind}"
        )
    # Full-replace av polisen-rader (transkriberad, komplett serie): tar bort ev. föråldrade rader
    # om årsuppsättning/source_ref ändrats (t.ex. när sprängningar slogs in och 2017 utgick).
    con.execute("DELETE FROM observations WHERE source_ref LIKE 'polisen:%'")
    n = warehouse.upsert(con, "observations", prows)
    span = f"{prows[0]['period']}..{prows[-1]['period']}" if prows else "-"
    print(f"Polisen (transkr.) -> trygghet    skjutningar_sprangningar: {n:4} obs ({span})")

    # Försvarsmakten: antal värnpliktiga som påbörjade grundutbildning (forsvar, delpoäng D) —
    # transkriberad config (config/personal_varnpliktiga.yaml; reproducerbar via
    # tools/varnpliktiga_audit), korsverifierad mot Pliktverkets inskrivna. source_ref
    # 'forsvarsmakten:' ligger utanför scb/kolada-purge-scope. Försvarets FÖRSTA D-serie.
    frows = forsvarsmakten.build_personal_varnpliktiga_observations()
    unlisted = {r["indicator"] for r in frows} - set(forsvarsmakten.INDICATORS)
    if unlisted:
        raise ValueError(f"Försvarsmakten emitterar indikatorer utanför INDICATORS: {sorted(unlisted)}")
    for ind in forsvarsmakten.INDICATORS:
        expectations.check_series(
            [r for r in frows if r["indicator"] == ind], forsvarsmakten.EXPECT.get(ind),
            f"Försvarsmakten {ind}",
        )
    # Full-replace av forsvarsmakten-rader (transkriberad, komplett serie): tar bort ev.
    # föråldrade rader om årsuppsättning/source_ref ändrats.
    con.execute("DELETE FROM observations WHERE source_ref LIKE 'forsvarsmakten:%'")
    n = warehouse.upsert(con, "observations", frows)
    span = f"{frows[0]['period']}..{frows[-1]['period']}" if frows else "-"
    print(f"Försvarsmakten (transkr.) -> forsvar  personal_varnpliktiga: {n:4} obs ({span})")

    # Regeringen/Försvarsdepartementet: Sveriges militära stöd till Ukraina per år (forsvar,
    # delpoäng D) — transkriberad config (config/ukraina_stod.yaml). Öppnar submåttet nato_ukraina.
    # source_ref 'regeringen:' ligger utanför scb/kolada-purge-scope.
    rrows = regeringen.build_ukraina_stod_observations()
    unlisted = {r["indicator"] for r in rrows} - set(regeringen.INDICATORS)
    if unlisted:
        raise ValueError(f"Regeringen emitterar indikatorer utanför INDICATORS: {sorted(unlisted)}")
    for ind in regeringen.INDICATORS:
        expectations.check_series(
            [r for r in rrows if r["indicator"] == ind], regeringen.EXPECT.get(ind),
            f"Regeringen {ind}",
        )
    # Full-replace av regeringen-rader (transkriberad, komplett serie).
    con.execute("DELETE FROM observations WHERE source_ref LIKE 'regeringen:%'")
    n = warehouse.upsert(con, "observations", rrows)
    span = f"{rrows[0]['period']}..{rrows[-1]['period']}" if rrows else "-"
    print(f"Regeringen (transkr.) -> forsvar       ukraina_stod: {n:4} obs ({span})")

    # Kriminalvården: återfall i brott inom 3 år (trygghet, delpoäng D) — transkriberade råtal
    # (config/aterfall_i_brott.yaml, KOS 2025 Tabell 6.1; loadern beräknar andel + korsverifierar).
    # Öppnar submåttet aterfall_kriminalvard. source_ref 'kriminalvarden:' utanför scb/kolada-purge.
    krows = kriminalvarden.build_aterfall_observations()
    unlisted = {r["indicator"] for r in krows} - set(kriminalvarden.INDICATORS)
    if unlisted:
        raise ValueError(f"Kriminalvården emitterar indikatorer utanför INDICATORS: {sorted(unlisted)}")
    for ind in kriminalvarden.INDICATORS:
        expectations.check_series(
            [r for r in krows if r["indicator"] == ind], kriminalvarden.EXPECT.get(ind),
            f"Kriminalvården {ind}",
        )
    # Full-replace av kriminalvarden-rader (transkriberad, komplett serie).
    con.execute("DELETE FROM observations WHERE source_ref LIKE 'kriminalvarden:%'")
    n = warehouse.upsert(con, "observations", krows)
    span = f"{krows[0]['period']}..{krows[-1]['period']}" if krows else "-"
    print(f"Kriminalvården (transkr.) -> trygghet   aterfall_i_brott: {n:4} obs ({span})")

    print("\n-- täckning (klimat, observations) --")
    for cat, ind, n, lo, hi in con.execute(
        "SELECT category, indicator, count(*), min(period), max(period) "
        "FROM observations WHERE category='klimat' GROUP BY category, indicator ORDER BY 2"
    ).fetchall():
        print(f"   {cat:12} {ind:24} {n:4}  {lo}..{hi}")

    print("\n-- kända luckor (loggas, ej tysta; se docs/fas3_coverage.md) --")
    print("   klimat: elprisvolatilitet/effektbrist (Svk, härledda) återstår.")
    print("   forsvar: personal_varnpliktiga (FM ÅR) matar nu D — övriga försvarsindikatorer")
    print("       kvalitativa/sekretess (allowlistade). demokrati: ingen officiell D-serie ännu.")
    con.close()


if __name__ == "__main__":
    main()
