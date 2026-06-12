# Fas 3 — täckning (coverage)

Status per kanonisk indikator (`config/categories.yaml`): **inläst** = officiell svensk årsserie
matar delpoäng D, eller **allowlistad** = explicit gap med skäl (`config/coverage_allowlist.yaml`).
Invarianten "inget tyst gap" hävdas av `tests/test_fas3_gate.py`. Generera aktuell matris med:

```bash
python -m pipeline.tools.coverage_report
```

Per 2026-06-12: **36 / 65 indikatorer inlästa** (D-dugliga, annuell up/down) i **alla 7 kategorier**
(ekonomi, välfärd, klimat, integration, trygghet, försvar, demokrati). **Ingen kategori är längre D-tom.**
*(17 per 2026-05-31; +2 trygghet 2026-06-03 — uppklaringsgrad + skjutningar/sprängningar; +2 ekonomi
2026-06-07 — naringslivets_investeringar + hushallens_reala_disponibla_inkomst, Spår D Tier 1;
+1 integration 2026-06-07 — sfi_sprakkunskaper, Spår D Tier 2; +1 försvar 2026-06-07 —
personal_varnpliktiga (försvarets första D); +1 demokrati 2026-06-07 — fortroende_domstolar_myndigheter
(demokratis första D, Brå NTU 5A:1), Spår D Tier 4; +1 välfärd + 1 klimat 2026-06-08/09 (Spår D
djupsvep); **+6 färsk session 2026-06-09 (Spår D byggkö):** aterfall_i_brott (trygghet, Kriminalvården
KOS), hackande_faglar_skog (klimat, biologisk_mangfald — Svensk Fågeltaxering), och 4 V-Dem-index
(demokrati — rattsstatsindex/yttrandefrihetsindex/privata_friheter/horisontellt_ansvarsutkravande,
öppnar alla 4 kvarvarande D-tomma demokrati-submått). **Inget demokrati-submått är längre D-tomt.**
**+2 integration 2026-06-12:** mellanmansklig_tillit (normer_tillit — SCB medborgarunders. N00666) +
asyl_handlaggningstid (migrationssystem — Migrationsverket). **Integration nu 5/5 undermått med D.**)*

## Inlästa indikatorer (matar D)

| Kategori | Indikator | Källa | Tabell/KPI | Riktning | Span |
|----------|-----------|-------|-----------|----------|------|
| ekonomi | arbetsloshet | SCB AKU | TAB2891 | down | 2001–2025 |
| ekonomi | sysselsattning | SCB AKU | TAB6514 | up | 2001–2025 |
| ekonomi | bnp_per_capita | SCB NR | TAB6728 | up | 1980–2024 |
| ekonomi | produktivitet | SCB NR (härledd) | TAB3610 ÷ TAB5622 | up | 1980–2024⁵ |
| ekonomi | naringslivets_investeringar | SCB NR | TAB3610 (BNAR, fasta priser) | up | 1980–2024 |
| ekonomi | hushallens_reala_disponibla_inkomst | SCB NR (härledd index) | TAB4592 (B6nRealGrowth, S14)⁶ | up | 1951–2025 |
| valfard | skolresultat | Kolada | N15507 | up | 2015–2025 |
| valfard | behoriga_larare | Kolada | N15813 | up | 2015–2025 |
| valfard | vardkoer | Kolada | N79242 | down | 2021–2024 |
| trygghet | dodligt_vald | Brå (Tabell 20) | per 100 000 | down | 2002–2025 |
| trygghet | skjutningar_sprangningar | Polisen (transkr.) | config-yaml | down | 2018–2025 |
| trygghet | brottsutsatthet | Brå NTU | Tabell 3A | down | 2016–2024² |
| trygghet | upplevd_otrygghet | Brå NTU | Tabell 4A:1 | down | 2017–2025³ |
| trygghet | uppklaringsgrad | Brå (Handlagda 10La) | personuppkl.% | up | 2016–2025 |
| trygghet | aterfall_i_brott | Kriminalvården KOS (transkr.) | Tabell 6.1 (råtal→andel) | down | 1994–2022¹⁰ |
| klimat | territoriella_utslapp | SCB (Naturvårdsverket) | TAB4698 | down | 1990–2024 |
| klimat | konsumtionsbaserade_utslapp | SCB Miljöräkenskaper | TAB5637 | down | 2008–2023 |
| klimat | fossil_energianvandning | Energimyndigheten (PxWeb v1) | EN0202_8 | down | 1970–2024 |
| klimat | hackande_faglar_skog | Svensk Fågeltaxering / Lund (transkr.) | sverigesmiljomal.se Highcharts | up | 2002–2024¹¹ |
| integration | bidragsberoende | Kolada | N31825 | down | 2010–2024 |
| integration | trangboddhet | SCB ULF | TAB6439 | down | 2020–2025¹ |
| integration | sjalvforsorjningsgrad | SCB AKU (utrikes födda) | TAB6529 | up | 2005–2025 |
| integration | sysselsattningsgap_inrikes_utrikes | SCB AKU (härledd) | TAB6529 SYSP 13−23 | down | 2005–2025⁴ |
| integration | sfi_sprakkunskaper | SCB (Skolverket) | TAB1814 (AA0003EB) | up | 1997–2023⁷ |
| integration | mellanmansklig_tillit | SCB medborgarunders. (Kolada) | N00666 | up | 2021–2025¹³ |
| integration | asyl_handlaggningstid | Migrationsverket (transkr.) | Avgjorda asylärenden (Asyl) | down | 2021–2025¹⁴ |
| forsvar | personal_varnpliktiga | Försvarsmakten (ÅR) | transkr. config-yaml | up | 2018–2025⁸ |
| demokrati | fortroende_domstolar_myndigheter | Brå NTU | blad 5A:1 | up | 2017–2025⁹ |
| demokrati | rattsstatsindex | V-Dem / Göteborgs univ. (transkr.) | v2x_rule | up | 2000–2025¹² |
| demokrati | yttrandefrihetsindex | V-Dem / Göteborgs univ. (transkr.) | v2x_freexp_altinf | up | 2000–2025¹² |
| demokrati | privata_friheter | V-Dem / Göteborgs univ. (transkr.) | v2x_clpriv | up | 2000–2025¹² |
| demokrati | horisontellt_ansvarsutkravande | V-Dem / Göteborgs univ. (transkr.) | v2x_horacc_osp | up | 2000–2025¹² |

¹ TAB6439 har dubbelår före 2020 som medvetet utesluts från D (multiårsspann ≠ enskild årspunkt).
² Aggregatet "brott mot enskild person" (Samtliga 16–84 år) finns i NTU enbart fr.o.m. 2016
  (NTU 2017 lade till brottstyper → ej jämförbart bakåt, Brå:s källfotnot). Tidigare år utesluts.
³ NTU:s otrygghetsserie 2007–2016 är omräknad med en ANNAN metod (källflaggad med asterisk);
  endast nuvarande metod (2017–2025) tas med, så metodbrytet inte ger en falsk D-årsförändring.
⁴ Härledd serie (`pipeline/derived.py`): sysselsättningsgrad (SYSP) inrikes födda − utrikes
  födda, procentenheter. Båda delserierna ur samma verifierade tabell (TAB6529); deterministisk
  differens, ingen imputation (år tas bara med när båda föräldraserierna har värde).
⁵ Härledd serie (`pipeline/derived.py`): arbetsproduktivitet i hela ekonomin = BNP till
  marknadspris i fasta priser (TAB3610, ref. 2020, mnkr) ÷ faktiskt arbetade timmar i hela
  ekonomin (TAB5622, 10 000-tal), skalat till kr/timme. Deterministisk kvot, ingen imputation.
  Reproducerar finanskris-svackan 2008–2009 och produktivitetsfallet 2022–2023 (Codex- och
  adversariellt verifierad). Ettårstecken är konjunkturkänsligt/revideras — D väger bara 10 %,
  makt-/ansvarsviktat och flaggat.
⁶ Härlett kumulativt REALINDEX (`pipeline/derived.py`, op `index`): hushållens reala disponibla
  inkomst finns bara publicerad som tillväxttakt (SCB NR TAB4592, NRindikator=B6nRealGrowth,
  Sektor=S14). Indexet idx[y]=idx[y−1]·(1+g[y]/100) ger den NIVÅ D behöver; tecknet på indexets
  årsförändring = tecknet på den officiella reala tillväxttakten (sign-only, vilket är allt D
  använder). SCB har redan deflaterat → inget eget deflatorval. Drift-skyddet sitter på
  föräldra-tillväxtserien (fångar real 2023 ≈ −1,1 %). Konjunktur-/räntekänslig → D 10 %, flaggat.
⁷ Andel personer GODKÄNDA i sfi (procent), SCB:s officiella sfi-statistik TAB1814, ContentsCode
  AA0003EB (Skolverket statistikansvarig, SCB producent). Semantikval (Spår D §5.2) avgjort av
  datan: tabellen har två mått — godkäntandel (AA0003EB, riktning up) och vistelsetid-median
  (AA0003EC, down). Bara godkäntandel matchar indikatorns kanoniska riktning. METODBROTT 2022
  (SCB-not: kursbetyg G/I/– + sista kursdag 1 jan fr.o.m. 2022): SCB publicerar ändå EN obruten
  serie 1997–2023, och de brott-närliggande övergångarna (2021→2022 −, 2022→2023 +) är
  teckenkonsistenta med den genuina nedgång-/stabiliseringstrenden — eftersom D bara tar TECKEN
  (ej magnitud) ändrar brottet magnituden men inte tecknet, så hela serien behålls (jfr NTU², där
  SCB delade serien och nivåerna var ojämförbara → fönstrades). v0, flaggad.
⁸ Antal värnpliktiga som PÅBÖRJADE grundutbildning per kalenderår, **Försvarsmaktens årsredovisning**
  (förmågemyndigheten; FM:s ÅR-mått är kalenderårsrent, till skillnad från Pliktverkets utbildningsårs-
  etiketterade "inskrivna"). **Försvarets första D-serie** (kategorin var tidigare strukturellt D-tom).
  Värdet (3 750→8 136, 2018–2025) korsverifieras varje år mot Plikt- och prövningsverkets OBEROENDE
  "inskrivna till GU" (≤~3 % skillnad de år båda finns); avgörande är att BÅDA myndigheterna visar
  samma enda nedgång 2021→2022, den enda teckenkänsliga D-övergången. Eftersom D bara tar TECKEN är
  attributionen robust mot sifferosäkerhet. Transkriberad config (FM:s/Pliktverkets ÅR-PDF:er är ej
  maskinläsbara), auditerbar via `pipeline/tools/varnpliktiga_audit.py`. KÄLLGRÄNS: 2018 + 2025 direkt
  bekräftade ur FM ÅR; 2019/2021/2022/2024 korsverifierade mot Pliktverket; 2020 + 2023 (inre monotona
  punkter, påverkar inget tecken) lokaliserade via Wikipedias FM-ÅR-citerade tabell. v0 tills exakta
  PDF-siffror transkriberats direkt (→v1).
⁹ Förtroende för **rättsväsendet som helhet** (domstolar + polis/åklagare/kriminalvård), andel med
  ganska/mycket stort förtroende, **Brå NTU blad 5A:1** ("Samtliga 16-84 år"). **Demokratis första
  D-serie.** Officiell källa (Brå/SOS) → krävs framför SOM-institutet (akademiskt; CLAUDE.md tillåter
  akademiskt bara NÄR officiell statistik saknas — vilket den inte gör här). Samma adapter som
  brottsutsatthet/upplevd_otrygghet (`bra.fetch_ntu`), så "no_api/SOM"-antagandet var överspelat.
  **2017-fönstret:** åren 2007*–2016* är asteriskmärkta (NTU 2017-omläggning, samma metodbrott som
  upplevd_otrygghet³) → nuvarande metod fr.o.m. 2017 (2017–2025, 9 år). Blad 5D:1 (domstolarna
  specifikt) korsverifierar med samma teckenförlopp (stigande utom dipp 2022→2023).
¹⁰ Andel av klienter med starthändelse (avslutad fängelse-/påbörjad frivårdsverkställighet) som
  återfaller i brott inom 3 år, **Kriminalvården KOS 2025 Tabell 6.1** (ingångsår 1994–2022, källa
  KVR/KUM). Öppnar submåttet aterfall_kriminalvard (tidigare allowlistat blocked:PDF). KOS publicerar
  råtalen (antal klienter + antal återfall) + en heltalsavrundad andel; vi lagrar RÅTALEN och beräknar
  andelen (config/aterfall_i_brott.yaml + loader), eftersom dödzonen (0,5 %) annars gör varje 1 pp-
  avrundningssteg till ett falskt tecken i platån 2012–2022. Verifierat direkt mot KOS-PDF:en;
  loadern korsverifierar mot publicerad andel (hård fail >0,6 pp). v0 (platå-signalsvaghet, ej dataproblem).
¹¹ Samlat populationsindex för 16 skogsfågelarter (basår 2002=100), **Svensk Fågeltaxering, Lunds
  universitet** (akademisk svensk källa), officiell miljömålsindikator "Levande skogar" via
  sverigesmiljomal.se. Öppnar biologisk_mangfald (NY indikator; hotade_arter_naturforlust förblir
  no_api-allowlistad). Tidsserien ligger maskinläsbart som Highcharts-JSON i sid-HTML:en; verifierad
  exakt via `pipeline/tools/faglar_transcribe.py` (alla 23 år). Äkta biologiskt UTFALL, ej policy-insats.
  v0 ⚠ BRUS-CAVEAT: trendlös/brusig serie → D (tecken, 10 %, makt-/ansvarsviktat) bidrar netto ≈ neutralt.
¹² **V-Dem** (Varieties of Democracy), Sverige 2000–2025, fyra 0-1-index (ett per tidigare D-tomt
  demokrati-submått). **V-Dem-institutet är värdat vid Göteborgs universitet → svensk akademisk källa**
  (CLAUDE.md tillåter när officiell statistik saknas) + ny intl-neutralitetsklausul (extern bedömare >
  statens självvärdering); TILLSTÅNDS-mått → klarar hammare-principen. ⚠ CAVEAT (största neutralitets-
  reservationen, v0): EXPERT-KODAT (subjektiva bedömningar, Bayesiansk IRT), ej hård räkning → mildras
  av tecken-only + 10 % vikt + takeffekt (Sverige 0,94–0,995 → bara trend meningsfull; rattsstatsindex
  i praktiken platt). Transkriberad ur V-Dem v16; verifierad mot V-Dem-datasetet (tools/vdem_transcribe)
  + OWID (3 av 4 index). Sign-off 2026-06-09. Indexval undviker dubbelräkning (horacc ej diagacc).

¹³ Andel som svarar att man i allmänhet kan lita på människor ("Till stor del"/"Helt och hållet"),
  **SCB:s medborgarundersökning** via Kolada **N00666**, 2021–2025 (ny enkätmetodik fr.o.m. 2021 → 5 år).
  Öppnar normer_tillit (integration 2026-06-12). KONSTRUKTVAL: N00666 mäter MELLANMÄNSKLIG (social) tillit
  = rätt fit, till skillnad från N00665 (förtroende för riksdagspolitiker → fel konstrukt, överlappar
  demokratis institutionstillit). ⚠ Nära platt (61,2–62,9 %) → D≈neutral; tunt 5-årsunderlag (sign-off).
  D tar bara TECKEN, väger 10 %. D-only (tillit_valdeltagande bär B-spåret).

¹⁴ Genomsnittlig handläggningstid (dagar) för avgjorda FÖRSTAGÅNGSÄRENDEN om asyl, **Migrationsverkets**
  "Avgjorda asylärenden" (bladet "Totalt, förstagångsärenden", deltabellen **Asyl**, raden Totalt). 2021–2025
  = 257/166/198/187/180. EXKL. massflyktsdirektivet/ukrainska medborgare (near-automatisk EU-process ~20–30 d,
  ej svensk handläggningseffektivitet; gör serien ojämförbar och dränker signalen). Öppnar migrationssystem
  (integration 2026-06-12). NEUTRALITET: kortare = bättre är ett av få migrationsmått där båda poler är
  överens (vs återvändande, värdeladdat); kvarvarande caveat: kvalitet-vs-hastighet + inflödesberoende → D
  tar bara TECKEN. Transkriberad config (källrad/år); revisionsspår `tools/asyl_handlaggningstid_verify.py`.

## Allowlistade gap (skäl i `config/coverage_allowlist.yaml`)

29 indikatorer saknar ännu en officiell svensk årsserie. Sammanfattning per skältyp:

- **target** (ej up/down, ej D-duglig): inflation, statsskuld_underskott, forsvarsanslag_andel_bnp.
- **derived** (kräver flera serier/beräkning): elprisvolatilitet, effektbrist,
  utslappsminskning_per_krona. (produktivitet, sysselsattningsgap_inrikes_utrikes och
  hushallens_reala_disponibla_inkomst är nu härledda, se ovan.)
- **no_api** (officiell/akademisk källa utan maskinläsbar årsserie): skillnader_mellan_skolor,
  personalomsattning_omsorg, valfardsbrottslighet, hotade_arter_naturforlust, skolresultat_utsatta_omraden,
  segregation. (fortroende_domstolar_myndigheter inläst 2026-06-07 via Brå NTU 5A:1 — officiell källa,
  ej SOM; demokratis första D-serie, Spår D Tier 4.)
- **future** (källa finns, adapter ej byggd): vard_i_tid,
  realloner (kräver Medlingsinstitutets konjunkturlönestatistik — SCB:s API saknar en ren helekonomi-
  löneserie, sonderat 2026-05-31), och Brås handläggningstabell (handlaggningstid). (uppklaringsgrad
  + skjutningar_sprangningar inlästa 2026-06-03; **aterfall_i_brott inläst 2026-06-09 via Kriminalvården
  KOS Tabell 6.1** — Brås PDF-väg behövdes ej, KOS ger råtalen;
  naringslivets_investeringar + hushallens_reala_disponibla_inkomst inlästa 2026-06-07;
  sfi_sprakkunskaper inläst 2026-06-07 via SCB TAB1814 — Spår D Tier 2;
  overlevnad_svar_sjukdom inläst 2026-06-08 via Kolada U70471 (30-dagarsöverlevnad tjocktarmscancer) — Spår D natt.)
- **international** (ej officiell svensk källa, otillåtet enligt CLAUDE.md): korruption (TI), mediefrihet (RSF).
  (OBS: dessa indikatorers SUBMÅTT får ändå D fr.o.m. 2026-06-09 via NYA V-Dem-indikatorer —
  yttrandefrihet_medier→yttrandefrihetsindex; de gamla TI/RSF-indikatorerna förblir allowlistade.)
- **qualitative** (ingen kvantitativ officiell mätserie): merparten av försvars- och demokratiindikatorerna
  (materiel_formaga, civil_beredskap_niva, nato_interoperabilitet, leveranstid_materiel,
  politisk_transparens, otillborlig_politisering, overvakning_utan_rattssakerhet). (OBS: de fyra
  demokrati-submåtten rattsstat_maktdelning/yttrandefrihet_medier/personlig_frihet/transparens_ansvar
  får alla D fr.o.m. 2026-06-09 via nya V-Dem-indikatorer (se ¹²); dessa gamla kvalitativa indikatorer
  förblir allowlistade som B-/visningsindikatorer.) (personal_varnpliktiga
  inläst 2026-06-07 via Försvarsmaktens ÅR — Spår D Tier 4, försvarets första D-serie; ukraina_stod inläst
  2026-06-08 via Regeringens militära stöd/år — Spår D natt, öppnade submåttet nato_ukraina. civil_beredskap_niva
  bekräftad vägg via MSB ÅR-PDF-läsning 2026-06-08: bara pengar/anslag, inget neutralt utfallsmått.)

## Nästa steg för att krympa allowlisten

1. ~~**Energimyndigheten** (fossil_energianvandning)~~ — **klar** (PxWeb-v1-adapter `pipeline/build_fas3.py`, EN0202_8, fossila energivaror summerade).
2. ~~**Brå NTU** (brottsutsatthet, upplevd_otrygghet)~~ — **klar** (`bra.fetch_ntu`, Tabellsamling NTU 2007–2025, blad 3A + 4A:1, "Samtliga 16–84 år", nuvarande-metod-fönster). Trygghet har nu 3 D-serier.
3. ~~**Socialstyrelsen** (overlevnad_svar_sjukdom)~~ **klar 2026-06-08 via Kolada U70471** (ej egen Socialstyrelse-adapter behövdes) + ~~**Skolverket** (sfi_sprakkunskaper)~~ **klar** (SCB TAB1814) + **Medlingsinstitutet** (realloner) — kvarstår, låg prio.
4. ~~**Loader-stöd för härledda indikatorer** (gap/kvot)~~ — **klar** (`pipeline/derived.py`, ren gap/kvot-beräkning ur verifierade serier, två-tabells-operander + rimlighetsgrind). Inlästa: sysselsattningsgap_inrikes_utrikes (SCB TAB6529 SYSP 13−23) och produktivitet (SCB TAB3610 BNP fast ÷ TAB5622 arbetade timmar). Återstår att härleda: utslappsminskning_per_krona, elprisvolatilitet (kräver nya föräldraserier).
5. ~~**SOM-institutet** (fortroende_domstolar_myndigheter)~~ — **klar 2026-06-07 via Brå NTU 5A:1** (officiell
   källa, ej SOM; demokratis första D). Återstår ev. SOM för `tillit_valdeltagande` (integration), men den är
   🔴 BEVAKA/B-only (categories.yaml) — bygg ej som D utan separat sign-off.
