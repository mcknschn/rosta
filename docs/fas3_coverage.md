# Fas 3 — täckning (coverage)

Status per kanonisk indikator (`config/categories.yaml`): **inläst** = officiell svensk årsserie
matar delpoäng D, eller **allowlistad** = explicit gap med skäl (`config/coverage_allowlist.yaml`).
Invarianten "inget tyst gap" hävdas av `tests/test_fas3_gate.py`. Generera aktuell matris med:

```bash
python -m pipeline.tools.coverage_report
```

Per 2026-05-31: **17 / 50 indikatorer inlästa** (D-dugliga, annuell up/down) i **5 av 7 kategorier**
(ekonomi, välfärd, klimat, integration, trygghet). Försvar och demokrati saknar D-data (allowlistade).

## Inlästa indikatorer (matar D)

| Kategori | Indikator | Källa | Tabell/KPI | Riktning | Span |
|----------|-----------|-------|-----------|----------|------|
| ekonomi | arbetsloshet | SCB AKU | TAB2891 | down | 2001–2025 |
| ekonomi | sysselsattning | SCB AKU | TAB6514 | up | 2001–2025 |
| ekonomi | bnp_per_capita | SCB NR | TAB6728 | up | 1980–2024 |
| ekonomi | produktivitet | SCB NR (härledd) | TAB3610 ÷ TAB5622 | up | 1980–2024⁵ |
| valfard | skolresultat | Kolada | N15507 | up | 2015–2025 |
| valfard | behoriga_larare | Kolada | N15813 | up | 2015–2025 |
| valfard | vardkoer | Kolada | N79242 | down | 2021–2024 |
| trygghet | dodligt_vald | Brå (Tabell 20) | per 100 000 | down | 2002–2025 |
| trygghet | brottsutsatthet | Brå NTU | Tabell 3A | down | 2016–2024² |
| trygghet | upplevd_otrygghet | Brå NTU | Tabell 4A:1 | down | 2017–2025³ |
| klimat | territoriella_utslapp | SCB (Naturvårdsverket) | TAB4698 | down | 1990–2024 |
| klimat | konsumtionsbaserade_utslapp | SCB Miljöräkenskaper | TAB5637 | down | 2008–2023 |
| klimat | fossil_energianvandning | Energimyndigheten (PxWeb v1) | EN0202_8 | down | 1970–2024 |
| integration | bidragsberoende | Kolada | N31825 | down | 2010–2024 |
| integration | trangboddhet | SCB ULF | TAB6439 | down | 2020–2025¹ |
| integration | sjalvforsorjningsgrad | SCB AKU (utrikes födda) | TAB6529 | up | 2005–2025 |
| integration | sysselsattningsgap_inrikes_utrikes | SCB AKU (härledd) | TAB6529 SYSP 13−23 | down | 2005–2025⁴ |

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

## Allowlistade gap (skäl i `config/coverage_allowlist.yaml`)

34 indikatorer saknar ännu en officiell svensk årsserie. Sammanfattning per skältyp:

- **target** (ej up/down, ej D-duglig): inflation, statsskuld_underskott, forsvarsanslag_andel_bnp.
- **derived** (kräver flera serier/beräkning): elprisvolatilitet, effektbrist,
  utslappsminskning_per_krona. (produktivitet och sysselsattningsgap_inrikes_utrikes är nu härledda, se ovan.)
- **no_api** (officiell/akademisk källa utan maskinläsbar årsserie): skillnader_mellan_skolor,
  personalomsattning_omsorg, valfardsbrottslighet, hotade_arter_naturforlust, skolresultat_utsatta_omraden,
  segregation, fortroende_domstolar_myndigheter (SOM).
- **future** (källa finns, adapter ej byggd): vard_i_tid, overlevnad_svar_sjukdom, sfi_sprakkunskaper,
  realloner (kräver Medlingsinstitutets konjunkturlönestatistik — SCB:s API saknar en ren helekonomi-
  löneserie, sonderat 2026-05-31), och Brås uppklarings-/återfallstabeller (uppklaringsgrad,
  handlaggningstid, aterfall_i_brott), skjutningar_sprangningar (Polisen). NTU-utsatthet/otrygghet inlästa.
- **international** (ej officiell svensk källa, otillåtet enligt CLAUDE.md): korruption (TI), mediefrihet (RSF).
- **qualitative** (ingen kvantitativ officiell mätserie): merparten av försvars- och demokratiindikatorerna
  (materiel_formaga, civil_beredskap_niva, ukraina_stod, nato_interoperabilitet, leveranstid_materiel,
  personal_varnpliktiga, politisk_transparens, otillborlig_politisering, overvakning_utan_rattssakerhet).

## Nästa steg för att krympa allowlisten

1. ~~**Energimyndigheten** (fossil_energianvandning)~~ — **klar** (PxWeb-v1-adapter `pipeline/build_fas3.py`, EN0202_8, fossila energivaror summerade).
2. ~~**Brå NTU** (brottsutsatthet, upplevd_otrygghet)~~ — **klar** (`bra.fetch_ntu`, Tabellsamling NTU 2007–2025, blad 3A + 4A:1, "Samtliga 16–84 år", nuvarande-metod-fönster). Trygghet har nu 3 D-serier.
3. **Socialstyrelsen** (overlevnad_svar_sjukdom) + **Skolverket** (sfi_sprakkunskaper) + **Medlingsinstitutet** (realloner) — egna adaptrar.
4. ~~**Loader-stöd för härledda indikatorer** (gap/kvot)~~ — **klar** (`pipeline/derived.py`, ren gap/kvot-beräkning ur verifierade serier, två-tabells-operander + rimlighetsgrind). Inlästa: sysselsattningsgap_inrikes_utrikes (SCB TAB6529 SYSP 13−23) och produktivitet (SCB TAB3610 BNP fast ÷ TAB5622 arbetade timmar). Återstår att härleda: utslappsminskning_per_krona, elprisvolatilitet (kräver nya föräldraserier).
5. **SOM-institutet** (fortroende_domstolar_myndigheter, tillit) — tabellinläsning (akademisk källa, tillåten).
