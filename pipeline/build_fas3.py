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
from .sources import (
    domstolsverket,
    energimyndigheten,
    fmv,
    forsvarsmakten,
    kriminalvarden,
    medlingsinstitutet,
    migrationsverket,
    mpf,
    polisen,
    regeringen,
    sverigesmiljomal,
    svk,
    vdem,
)


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ra = date.today().isoformat()
    con = warehouse.connect()
    print("== Fas 3 (sektorsadaptrar) ==")

    # Energimyndigheten (PxWeb v1): två klimatserier ur samma statistikdatabas —
    # fossil_energianvandning (EN0202_8) + elprisvolatilitet (EN_IND12-5A, Energiindikatorer
    # 12.5: spotpris månadsmedel SE1-SE4 -> årlig CV beräknad I ADAPTERN, månadsraderna skrivs
    # aldrig till warehouse). Måttval (CV ddof=0, likaviktning, 12/12-regeln) + v0-caveats
    # dokumenterade i modulen. §5.4-källregelfrågan UPPLÖST: officiell svensk myndighetskälla,
    # inte Nord Pool. v0, FLAGGAD.
    rows = energimyndigheten.fetch_fossil_energy(ra) + energimyndigheten.fetch_elprisvolatilitet(ra)
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
    for ind, table in (("fossil_energianvandning", "EN0202_8"), ("elprisvolatilitet", "EN_IND12-5A")):
        sub = [r for r in rows if r["indicator"] == ind]
        span = f"{sub[0]['period']}..{sub[-1]['period']}" if sub else "-"
        print(f"Energimyndigheten {table:11} -> klimat       {ind}: {len(sub):4} obs ({span})")

    # Domstolsverket DOMstat (PxWeb v1, samma dialekt som Energimyndigheten): handläggningstid vid
    # tingsrätt, 75-percentil i månader, brottmål exkl. förtursmål, alla tingsrätter (trygghet,
    # delpoäng D — submåttet rattsvasendets_effektivitet). Måttval dokumenterat i modulen
    # (75-percentil; exkl.-förtursmål-biasen är icke-smickrande; domstolsledet — uppströms
    # polis-/åklagartid fångas delvis av uppklaringsgrad). v0, FLAGGAD. source_ref
    # 'domstolsverket:' ligger utanför scb/kolada-purge-scope.
    dvrows = domstolsverket.fetch_handlaggningstid(ra)
    unlisted = {r["indicator"] for r in dvrows} - set(domstolsverket.INDICATORS)
    if unlisted:
        raise ValueError(f"Domstolsverket emitterar indikatorer utanför INDICATORS: {sorted(unlisted)}")
    for ind in domstolsverket.INDICATORS:
        expectations.check_series(
            [r for r in dvrows if r["indicator"] == ind], domstolsverket.EXPECT.get(ind),
            f"Domstolsverket {ind}",
        )
    n = warehouse.upsert(con, "observations", dvrows)
    span = f"{dvrows[0]['period']}..{dvrows[-1]['period']}" if dvrows else "-"
    print(f"Domstolsverket 01_Verksamhetsmal_TR -> trygghet  handlaggningstid: {n:4} obs ({span})")

    # Medlingsinstitutet (egen PxWeb-instans, v1, samma dialekt som Domstolsverket/Energimyndig-
    # heten): reala löner i hela ekonomin, Reallön (KPI) som Index(1995=100), 1960-2025 (ekonomi,
    # delpoäng D — submåttet realloner_hushall). Måttval dokumenterat i modulen (KPI = MI:s huvud-
    # serie, tecknet identiskt med KPIF; indexserien, inte %-serien; 2025 preliminär; medveten
    # dubbelbreddning — submåttet har redan D via hushallens_reala_disponibla_inkomst). v0,
    # FLAGGAD. source_ref 'medlingsinstitutet:' ligger utanför scb/kolada-purge-scope.
    mirows = medlingsinstitutet.fetch_realloner(ra)
    unlisted = {r["indicator"] for r in mirows} - set(medlingsinstitutet.INDICATORS)
    if unlisted:
        raise ValueError(f"Medlingsinstitutet emitterar indikatorer utanför INDICATORS: {sorted(unlisted)}")
    for ind in medlingsinstitutet.INDICATORS:
        expectations.check_series(
            [r for r in mirows if r["indicator"] == ind], medlingsinstitutet.EXPECT.get(ind),
            f"Medlingsinstitutet {ind}",
        )
    n = warehouse.upsert(con, "observations", mirows)
    span = f"{mirows[0]['period']}..{mirows[-1]['period']}" if mirows else "-"
    print(f"Medlingsinstitutet Realloner_arsdata -> ekonomi  realloner: {n:4} obs ({span})")

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

    # Försvarsmakten (forsvar, delpoäng D) — transkriberade configar (källrad per värde, ingen
    # runtime-PDF-parser). TVÅ serier i militar_formaga: personal_varnpliktiga (antal som påbörjade GU,
    # korsverifierad mot Pliktverket; reproducerbar via tools/varnpliktiga_audit) och
    # personalstyrka_kontinuerligt (stående personalvolym, FM ÅR bilaga Tabell 1). source_ref
    # 'forsvarsmakten:' ligger utanför scb/kolada-purge-scope.
    frows = forsvarsmakten.build_all_observations()
    unlisted = {r["indicator"] for r in frows} - set(forsvarsmakten.INDICATORS)
    if unlisted:
        raise ValueError(f"Försvarsmakten emitterar indikatorer utanför INDICATORS: {sorted(unlisted)}")
    for ind in forsvarsmakten.INDICATORS:
        expectations.check_series(
            [r for r in frows if r["indicator"] == ind], forsvarsmakten.EXPECT.get(ind),
            f"Försvarsmakten {ind}",
        )
    # Full-replace av forsvarsmakten-rader (transkriberade, kompletta serier): tar bort ev.
    # föråldrade rader om årsuppsättning/source_ref ändrats.
    con.execute("DELETE FROM observations WHERE source_ref LIKE 'forsvarsmakten:%'")
    n = warehouse.upsert(con, "observations", frows)
    for ind in forsvarsmakten.INDICATORS:
        sub = [r for r in frows if r["indicator"] == ind]
        span = f"{sub[0]['period']}..{sub[-1]['period']}" if sub else "-"
        print(f"Försvarsmakten (transkr.) -> forsvar  {ind:28}: {len(sub):4} obs ({span})")

    # MPF (Myndigheten för psykologiskt försvar): försvarsvilja (forsvar, delpoäng D) — transkriberad
    # config (config/forsvarsvilja.yaml, MPF Opinioner-tabellen). Öppnar submåttet civil_beredskap
    # (resiliens-/attitydutfall; psykologiskt försvar = del av totalförsvaret). source_ref 'mpf:'
    # ligger utanför scb/kolada-purge-scope.
    morows = mpf.build_forsvarsvilja_observations()
    unlisted = {r["indicator"] for r in morows} - set(mpf.INDICATORS)
    if unlisted:
        raise ValueError(f"MPF emitterar indikatorer utanför INDICATORS: {sorted(unlisted)}")
    for ind in mpf.INDICATORS:
        expectations.check_series(
            [r for r in morows if r["indicator"] == ind], mpf.EXPECT.get(ind), f"MPF {ind}"
        )
    # Full-replace av mpf-rader (transkriberad, komplett serie).
    con.execute("DELETE FROM observations WHERE source_ref LIKE 'mpf:%'")
    n = warehouse.upsert(con, "observations", morows)
    span = f"{morows[0]['period']}..{morows[-1]['period']}" if morows else "-"
    print(f"MPF (transkr.) -> forsvar  forsvarsvilja: {n:4} obs ({span})")

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

    # FMV: leveransindex ap. 1:3.1 (forsvar, delpoäng D) — transkriberad config
    # (config/materielleveransutfall.yaml, FMV ÅR 2021-2025, maskinverifierad PyMuPDF). Öppnar
    # submåttet genomforbarhet_leverans (försvarets sista D-tomma icke-uteslutna undermått ->
    # D-bredd 70->75/100, forsvar ur d_thin_breadth_accepted). Serien börjar 2021 (FMV: 2020-
    # explicit ojämförbara). v0-caveats (FMV:s egen leveransplan som måttstock/överplanering
    # 2025, kalenderårskänslighet, viktningsbas-skifte, endast ap. 1:3.1) i configen. v0,
    # FLAGGAD. source_ref 'fmv:' ligger utanför scb/kolada-purge-scope.
    fmvrows = fmv.build_materielleveransutfall_observations()
    unlisted = {r["indicator"] for r in fmvrows} - set(fmv.INDICATORS)
    if unlisted:
        raise ValueError(f"FMV emitterar indikatorer utanför INDICATORS: {sorted(unlisted)}")
    for ind in fmv.INDICATORS:
        expectations.check_series(
            [r for r in fmvrows if r["indicator"] == ind], fmv.EXPECT.get(ind), f"FMV {ind}"
        )
    # Full-replace av fmv-rader (transkriberad, komplett serie).
    con.execute("DELETE FROM observations WHERE source_ref LIKE 'fmv:%'")
    n = warehouse.upsert(con, "observations", fmvrows)
    span = f"{fmvrows[0]['period']}..{fmvrows[-1]['period']}" if fmvrows else "-"
    print(f"FMV (transkr.) -> forsvar  materielleveransutfall: {n:4} obs ({span})")

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

    # Sveriges miljömål / Svensk Fågeltaxering (Lunds universitet): häckande fåglar i skogen
    # (klimat, delpoäng D) — transkriberat indexvärde ur portalens Highcharts-serie
    # (config/hackande_faglar_skog.yaml; reproducerbart via tools/faglar_transcribe.py). Öppnar
    # submåttet biologisk_mangfald. source_ref 'sverigesmiljomal:' utanför scb/kolada-purge-scope.
    brows = sverigesmiljomal.build_faglar_observations()
    unlisted = {r["indicator"] for r in brows} - set(sverigesmiljomal.INDICATORS)
    if unlisted:
        raise ValueError(f"Sverigesmiljomal emitterar indikatorer utanför INDICATORS: {sorted(unlisted)}")
    for ind in sverigesmiljomal.INDICATORS:
        expectations.check_series(
            [r for r in brows if r["indicator"] == ind], sverigesmiljomal.EXPECT.get(ind),
            f"Sverigesmiljomal {ind}",
        )
    # Full-replace av sverigesmiljomal-rader (transkriberad, komplett serie).
    con.execute("DELETE FROM observations WHERE source_ref LIKE 'sverigesmiljomal:%'")
    n = warehouse.upsert(con, "observations", brows)
    span = f"{brows[0]['period']}..{brows[-1]['period']}" if brows else "-"
    print(f"Sverigesmiljomal (transkr.) -> klimat   hackande_faglar_skog: {n:4} obs ({span})")

    # Svenska kraftnät: nettoimport vid vinterns topplasttimme (klimat, delpoäng D) — transkriberad
    # config (config/effektbrist.yaml, ur lagstadgade Kraftbalansen-rapportens utfallskapitel;
    # maskinverifierad PyMuPDF, vinterår -> slutår). Effektbrist-bäraren: lastfrånkoppling har aldrig
    # inträffat -> nettoimport vid topplast = närliggande bärare, riktning down direkt. Väder-caveat
    # + normalvinter-prognos som robusthetsreferens i configen. source_ref 'svk:' utanför
    # scb/kolada-purge-scope. v0, FLAGGAD.
    srows = svk.build_effektbrist_observations()
    unlisted = {r["indicator"] for r in srows} - set(svk.INDICATORS)
    if unlisted:
        raise ValueError(f"Svk emitterar indikatorer utanför INDICATORS: {sorted(unlisted)}")
    for ind in svk.INDICATORS:
        expectations.check_series(
            [r for r in srows if r["indicator"] == ind], svk.EXPECT.get(ind), f"Svk {ind}"
        )
    # Full-replace av svk-rader (transkriberad, komplett serie).
    con.execute("DELETE FROM observations WHERE source_ref LIKE 'svk:%'")
    n = warehouse.upsert(con, "observations", srows)
    span = f"{srows[0]['period']}..{srows[-1]['period']}" if srows else "-"
    print(f"Svenska kraftnät (transkr.) -> klimat   effektbrist: {n:4} obs ({span})")

    # Migrationsverket: genomsnittlig handläggningstid för avgjorda förstagångsärenden om asyl
    # (integration, delpoäng D) — transkriberad config (config/asyl_handlaggningstid.yaml, deltabellen
    # Asyl exkl. massflykt; reproducerbar via tools/asyl_handlaggningstid_verify). Öppnar submåttet
    # migrationssystem. source_ref 'migrationsverket:' ligger utanför scb/kolada-purge-scope.
    mrows = migrationsverket.build_asyl_handlaggningstid_observations()
    unlisted = {r["indicator"] for r in mrows} - set(migrationsverket.INDICATORS)
    if unlisted:
        raise ValueError(f"Migrationsverket emitterar indikatorer utanför INDICATORS: {sorted(unlisted)}")
    for ind in migrationsverket.INDICATORS:
        expectations.check_series(
            [r for r in mrows if r["indicator"] == ind], migrationsverket.EXPECT.get(ind),
            f"Migrationsverket {ind}",
        )
    # Full-replace av migrationsverket-rader (transkriberad, komplett serie).
    con.execute("DELETE FROM observations WHERE source_ref LIKE 'migrationsverket:%'")
    n = warehouse.upsert(con, "observations", mrows)
    span = f"{mrows[0]['period']}..{mrows[-1]['period']}" if mrows else "-"
    print(f"Migrationsverket (transkr.) -> integration asyl_handlaggningstid: {n:4} obs ({span})")

    # V-Dem (Göteborgs universitet): Sveriges demokrati-/institutionsindex (demokrati, delpoäng D)
    # — fyra index ur V-Dem v16 (config/vdem_demokrati.yaml; reproducerbart via tools/vdem_transcribe).
    # Öppnar fyra D-tomma demokrati-submått. Svensk akademisk källa (se config-headern; sign-off
    # 2026-06-09). source_ref 'vdem:' utanför scb/kolada-purge-scope.
    vrows = vdem.build_vdem_observations()
    unlisted = {r["indicator"] for r in vrows} - set(vdem.INDICATORS)
    if unlisted:
        raise ValueError(f"V-Dem emitterar indikatorer utanför INDICATORS: {sorted(unlisted)}")
    for ind in vdem.INDICATORS:
        expectations.check_series(
            [r for r in vrows if r["indicator"] == ind], vdem.EXPECT.get(ind), f"V-Dem {ind}"
        )
    # Full-replace av vdem-rader (transkriberad, komplett serie).
    con.execute("DELETE FROM observations WHERE source_ref LIKE 'vdem:%'")
    n = warehouse.upsert(con, "observations", vrows)
    span = f"{vrows[0]['period']}..{vrows[-1]['period']}" if vrows else "-"
    print(f"V-Dem (transkr.) -> demokrati  {len(vdem.INDICATORS)} index: {n:4} obs ({span})")

    print("\n-- täckning (klimat, observations) --")
    for cat, ind, n, lo, hi in con.execute(
        "SELECT category, indicator, count(*), min(period), max(period) "
        "FROM observations WHERE category='klimat' GROUP BY category, indicator ORDER BY 2"
    ).fetchall():
        print(f"   {cat:12} {ind:24} {n:4}  {lo}..{hi}")

    print("\n-- kända luckor (loggas, ej tysta; se docs/done/fas3_coverage.md) --")
    print("   klimat: elprisvolatilitet (Energimyndigheten EN_IND12-5A, årlig CV) matar nu D;")
    print("       effektbrist (Svk Kraftbalansen, nettoimport vid topplasttimmen) matar nu D.")
    print("   ekonomi: realloner (MI Realloner_arsdata, Reallön KPI index 1995=100) matar nu D —")
    print("       realloner_hushall har 2 serier (medveten dubbelbreddning, se modulen).")
    print("   forsvar: personal_varnpliktiga + personalstyrka_kontinuerligt (FM ÅR) + ukraina_stod")
    print("       + forsvarsvilja (MPF Opinioner -> civil_beredskap) + materielleveransutfall")
    print("       (FMV leveransindex -> genomforbarhet_leverans) matar D; materiel_formaga m.fl.")
    print("       kvalitativa/sekretess (allowlistade). 4/5 submått med D (ekon_ambition utesluten/B-only).")
    print("   trygghet: aterfall_i_brott (Kriminalvården KOS) + handlaggningstid (Domstolsverket")
    print("       DOMstat 01_Verksamhetsmal_TR) matar nu D.")
    print("   klimat: hackande_faglar_skog (Svensk Fågeltaxering) matar nu biologisk_mangfald-D.")
    print("   demokrati: rattsstat/yttrandefrihet/personlig frihet/transparens matas nu av V-Dem")
    print("       (4 index, Göteborgs univ.) + förtroende (Brå NTU); korruption-D allowlistad (intl).")
    print("   integration: normer_tillit (SCB medborgarunders. N00666, fas 2) + migrationssystem")
    print("       (asyl_handlaggningstid, Migrationsverket) matar nu D; segregation/utsatta allowlistade.")
    con.close()


if __name__ == "__main__":
    main()
