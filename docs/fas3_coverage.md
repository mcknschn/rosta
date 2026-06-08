# Fas 3 — täckning (coverage)

Status per kanonisk indikator (`config/categories.yaml`): **inläst** = officiell svensk årsserie
matar delpoäng D, eller **allowlistad** = explicit gap med skäl (`config/coverage_allowlist.yaml`).
Invarianten "inget tyst gap" hävdas av `tests/test_fas3_gate.py`. Generera aktuell matris med:

```bash
python -m pipeline.tools.coverage_report
```

Per 2026-06-07: **24 / 56 indikatorer inlästa** (D-dugliga, annuell up/down) i **alla 7 kategorier**
(ekonomi, välfärd, klimat, integration, trygghet, försvar, demokrati). **Ingen kategori är längre D-tom.**
*(17 per 2026-05-31; +2 trygghet 2026-06-03 — uppklaringsgrad + skjutningar/sprängningar; +2 ekonomi
2026-06-07 — naringslivets_investeringar + hushallens_reala_disponibla_inkomst, Spår D Tier 1;
+1 integration 2026-06-07 — sfi_sprakkunskaper, Spår D Tier 2; +1 försvar 2026-06-07 —
personal_varnpliktiga (försvarets första D); +1 demokrati 2026-06-07 — fortroende_domstolar_myndigheter
(demokratis första D, Brå NTU 5A:1), Spår D Tier 4.)*

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
| klimat | territoriella_utslapp | SCB (Naturvårdsverket) | TAB4698 | down | 1990–2024 |
| klimat | konsumtionsbaserade_utslapp | SCB Miljöräkenskaper | TAB5637 | down | 2008–2023 |
| klimat | fossil_energianvandning | Energimyndigheten (PxWeb v1) | EN0202_8 | down | 1970–2024 |
| integration | bidragsberoende | Kolada | N31825 | down | 2010–2024 |
| integration | trangboddhet | SCB ULF | TAB6439 | down | 2020–2025¹ |
| integration | sjalvforsorjningsgrad | SCB AKU (utrikes födda) | TAB6529 | up | 2005–2025 |
| integration | sysselsattningsgap_inrikes_utrikes | SCB AKU (härledd) | TAB6529 SYSP 13−23 | down | 2005–2025⁴ |
| integration | sfi_sprakkunskaper | SCB (Skolverket) | TAB1814 (AA0003EB) | up | 1997–2023⁷ |
| forsvar | personal_varnpliktiga | Försvarsmakten (ÅR) | transkr. config-yaml | up | 2018–2025⁸ |
| demokrati | fortroende_domstolar_myndigheter | Brå NTU | blad 5A:1 | up | 2017–2025⁹ |

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

## Allowlistade gap (skäl i `config/coverage_allowlist.yaml`)

30 indikatorer saknar ännu en officiell svensk årsserie. Sammanfattning per skältyp:

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
  löneserie, sonderat 2026-05-31), och Brås handläggnings-/återfallstabeller (handlaggningstid,
  aterfall_i_brott). (uppklaringsgrad + skjutningar_sprangningar inlästa 2026-06-03;
  naringslivets_investeringar + hushallens_reala_disponibla_inkomst inlästa 2026-06-07;
  sfi_sprakkunskaper inläst 2026-06-07 via SCB TAB1814 — Spår D Tier 2;
  overlevnad_svar_sjukdom inläst 2026-06-08 via Kolada U70471 (30-dagarsöverlevnad tjocktarmscancer) — Spår D natt.)
- **international** (ej officiell svensk källa, otillåtet enligt CLAUDE.md): korruption (TI), mediefrihet (RSF).
- **qualitative** (ingen kvantitativ officiell mätserie): merparten av försvars- och demokratiindikatorerna
  (materiel_formaga, civil_beredskap_niva, nato_interoperabilitet, leveranstid_materiel,
  politisk_transparens, otillborlig_politisering, overvakning_utan_rattssakerhet). (personal_varnpliktiga
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
