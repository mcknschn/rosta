# Spår D — Datatäckning (delpoäng D, resultat)

> **Roll:** Aktiv arbets- och trackinglogg för Spår D (utfall/resultat). Bryter ut Spår D ur
> [BACKLOG.md](BACKLOG.md) så arbetet kan trackas per indikator och **flyttas till `docs/done/`**
> när exit-kriterierna nedan är uppfyllda. Samma livscykel som B-spårets logg
> ([done/evidens_trovardighet.md](done/evidens_trovardighet.md)).
>
> **Sanningskälla för vad som saknas:** [`config/coverage_allowlist.yaml`](../config/coverage_allowlist.yaml)
> (maskinläsbar, grindad av `tests/test_fas3_gate.py`). Detta dokument **duplicerar inte** skälen
> där — det är *planen och trackern*. När en indikator byggs: ta bort den ur allowlisten, uppdatera
> `scorerun.py:coverage`-strängen + `docs/fas3_coverage.md`, bocka av här, och skriv en kort rad i
> [done/ROADMAP.md](done/ROADMAP.md).
>
> **Bärande princip (CLAUDE.md):** endast officiella svenska källor; svensk akademi när officiell
> statistik saknas. Inga internationella index. All data spårbar till källrad. Ingen tyst lucka.

---

## 1. Vad delpoäng D är, och varför spåret finns

D = **resultat**: förbättrades kategorins objektiva indikatorer där partiet hade ansvar?
Mekaniken (Fas 5b, `pipeline/score.py:attribute_series` + `scorerun.py:category_d`):

- För varje **nationell årsserie** (`up`/`down`; `target` hoppas över) tas *tecknet* på den
  riktningsjusterade årsförändringen (förbättring +1 / försämring −1 / 0 i dödzon).
- Varje förändring (år y−1 → y) tillskrivs regeringen som satt år y−1 (`attribution_lag_years = 1`),
  viktad med maktandel (regering 1,0, stöd 0,5). Per kategori: submåttsviktat medel → `net ∈ [−1,1]`
  → betyg via 0→2,5-skalan. *Tecken, inte magnitud* (robust mot konjunktur-caveat, IDEA.md).
- Maktandel < `min_responsibility` → D ≈ neutral (2,5), flagga `D_not_applicable`, **bred osäkerhet**
  (partiet straffas inte för utfall det inte rådde över). Tunt underlag → `D_thin_basis`.

**En ny D-serie behöver bara:** vara *kanonisk* (finnas i `categories.yaml` med rätt `direction`)
och *annuell* (konsekutiva år). Då matar den `category_d` **automatiskt** — ingen scoringändring.
Registrering = en post i `pipeline/build_fas2.py:SCB_SERIES`/`KOLADA_KPIS` (eller en sektorsadapter)
med verifierade dimensionskoder + en `expect`-ankare (drift-skydd).

**Varför spåret är viktigt (BACKLOG "Varför den här prioriteringen"):** rankingen drivs i dag mest av
A (aktivitet) + C (makt). D var `not_applicable` i **21 av 56 celler** — efter Spår D-breddningen (alla
7 kategorier har nu minst en D-serie) är det nere i **7 av 56 celler** (= enbart `V`, som aldrig haft
nationell regeringsmakt i fönstret → strukturellt korrekt, ej ett gap). Modellen mäter därmed
*om utfallet blev bättre där partiet styrde* i betydligt fler celler — närmare grundidén.

---

## 2. Nuläge (verifierat via `python -m pipeline.tools.coverage_report`, 2026-06-12)

**42 D-serier inlästa** (annuell, D-duglig) i **ALLA 7 kategorier** *(56 ursprungliga kanoniska + 11 nya
kanoniska indikatorer)*. *(24 efter Tier 4; +`overlevnad_svar_sjukdom` +`ukraina_stod` natt 2026-06-08;
+`brukarnojdhet_hemtjanst` +`utslappsintensitet` djupsvep 2026-06-09; **+6 färsk session 2026-06-09:**
+`aterfall_i_brott` (trygghet) +`hackande_faglar_skog` (klimat) + 4 V-Dem-index (demokrati);
**+2 integration 2026-06-12:** +`mellanmansklig_tillit` (SCB medborgarunders. N00666) +`asyl_handlaggningstid`
(Migrationsverket) → **integration 3/5 → 5/5 undermått med D**; **+2 försvar 2026-06-12:**
+`forsvarsvilja` (MPF Opinioner → civil_beredskap) +`personalstyrka_kontinuerligt` (FM ÅR) →
**försvar 2/5 → 3/5 undermått med D**; **+1 trygghet 2026-06-12 (kväll):** +`handlaggningstid`
(Domstolsverket DOMstat — 2:a serien i rattsvasendets_effektivitet); **+1 ekonomi 2026-06-12 (kväll):**
+`realloner` (Medlingsinstitutets egen PxWeb — 2:a serien i realloner_hushall); **+1 klimat 2026-06-12
(kväll):** +`elprisvolatilitet` (Energimyndigheten EN_IND12-5A, spotpris → årlig CV — 2:a serien i
energi_elpriser, §5.4 upplöst); **+1 klimat 2026-06-12 (kväll, effektbrist):** +`effektbrist`
(Svk Kraftbalansen, nettoimport vid vinterns topplasttimme — 3:e serien i energi_elpriser,
§5.4-RESTEN avgjord: rapporten, ej timdata).)* Full logg:
[spar_D_svep_2026-06-08.md §5](done/spar_D_svep_2026-06-08.md) (byggkö exekverad) + [nattrapport](done/spar_D_nattrapport_2026-06-08.md).
**aterfall_kriminalvard + biologisk_mangfald + alla 4 D-tomma demokrati-submått + normer_tillit + migrationssystem öppnade → ingen kategori D-tom på submåttsnivå utom enstaka.**

| Kategori | D-täckta submått | Inlästa D-serier |
|----------|:---:|---|
| ekonomi | **4 / 4 D-bara¹** | sysselsattning, arbetsloshet, bnp_per_capita, produktivitet, **naringslivets_investeringar**, **hushallens_reala_disponibla_inkomst**, **realloner** (MI:s egen PxWeb, 2:a serien i realloner_hushall — ekonomi 2026-06-12 kväll) |
| valfard | **3 / 4** | vardkoer, overlevnad_svar_sjukdom, skolresultat, behoriga_larare, **brukarnojdhet_hemtjanst** (omsorg_personal öppnat, djupsvep) |
| trygghet | **4 / 5** | dodligt_vald, skjutningar_sprangningar, brottsutsatthet, upplevd_otrygghet, uppklaringsgrad, **handlaggningstid** (Domstolsverket DOMstat, 2:a serien i rattsvasendets_effektivitet — trygghet 2026-06-12), **aterfall_i_brott** (aterfall_kriminalvard öppnat, KOS, färsk session) |
| forsvar | **3 / 5** | personal_varnpliktiga, ukraina_stod (nato_ukraina), **personalstyrka_kontinuerligt** (FM ÅR, 2:a militar_formaga-serien), **forsvarsvilja** (civil_beredskap öppnat, MPF Opinioner — försvar 2026-06-12) |
| klimat | **4 / 5** | territoriella_utslapp, konsumtionsbaserade_utslapp, fossil_energianvandning, **elprisvolatilitet** (Energimyndigheten EN_IND12-5A spotpris → årlig CV, 2:a serien i energi_elpriser — klimat 2026-06-12 kväll), **effektbrist** (Svk Kraftbalansen, nettoimport vid topplasttimmen — 3:e serien i energi_elpriser, klimat 2026-06-12 kväll), **utslappsintensitet** (kostnadseff., djupsvep), **hackande_faglar_skog** (biologisk_mangfald öppnat, Svensk Fågeltaxering, färsk session) |
| integration | **5 / 5** | sysselsattningsgap_inrikes_utrikes, sjalvforsorjningsgrad, bidragsberoende, trangboddhet, sfi_sprakkunskaper, **mellanmansklig_tillit** (normer_tillit öppnat, SCB medborgarunders. N00666), **asyl_handlaggningstid** (migrationssystem öppnat, Migrationsverket — integration 2026-06-12) |
| demokrati | **5 / 5** | fortroende_domstolar_myndigheter (Brå NTU), **rattsstatsindex, yttrandefrihetsindex, privata_friheter, horisontellt_ansvarsutkravande** (V-Dem/Göteborgs univ., 4 D-tomma submått öppnade, färsk session — demokrati-väggen löst på D-sidan) |

¹ ekonomi har 6 submått men 2 är `target`-only (inflation, offentliga finanser) → ej D-bara.

**Strukturellt (ej en databredd-fråga, lämnas som är):** `V` får `D_not_applicable` i alla
kategorier — Vänsterpartiet har inte suttit i nationell regering i fönstret 2014–2026, så det finns
inget ansvar att attribuera. Det är **korrekt och rättvist**, inte ett gap.

---

## 2.1 Mastertabell — D-täckning per indikator (samtliga 67) ⭐

> **Parallell till B-spårets mastertabell** ([done/evidens_trovardighet.md §4.3](done/evidens_trovardighet.md)),
> fast för **D** (resultat/utfall). Sanningskälla: `python -m pipeline.tools.coverage_report` +
> [`config/coverage_allowlist.yaml`](../config/coverage_allowlist.yaml). **Verifierad 2026-06-12.**
> OBS: D-dimensionen i §4.3-tabellen (kolumnen "mäts (D)") är **inaktuell** efter Spår D Tier 1/2/4 +
> djupsvep + färsk session + integration 2026-06-12 —
> *denna* tabell är den auktoritativa D-vyn. Kanoniska visningsnamn för Kategori/Undermått: §4.3.
>
> **D-status:** ✅ **byggd** (officiell svensk annuell up/down-serie inläst, matar `category_d`) ·
> 🟡 **byggbar / öppet beslut** (väg finns — härledning/sondering/adapter — men ej byggd; väntar
> designbeslut §5) · 🔴 **ej byggbar** (ingen maskinläsbar officiell årsserie: `no_api`/`qualitative`/
> `blocked`/`low_value`/`B-only`, eller otillåten `international`-källa) · ⚪ **target** (ingen
> riktning → ej D-duglig per konstruktion).

### Sammanfattning (hur stor täckning vi har)

- **42 / 67 indikatorer** har en D-serie (annuell up/down som matar `category_d`). *(+2 natt 2026-06-08,
  +2 djupsvep, +6 färsk session 2026-06-09: aterfall_i_brott, hackande_faglar_skog, 4 V-Dem-index;
  **+2 integration 2026-06-12: mellanmansklig_tillit (SCB medborgarunders. N00666) + asyl_handlaggningstid
  (Migrationsverket); +2 försvar 2026-06-12: forsvarsvilja (MPF Opinioner) + personalstyrka_kontinuerligt
  (FM ÅR); +1 trygghet 2026-06-12 (kväll): handlaggningstid (Domstolsverket DOMstat); +1 ekonomi
  2026-06-12 (kväll): realloner (Medlingsinstitutets egen PxWeb); +1 klimat 2026-06-12 (kväll):
  elprisvolatilitet (Energimyndigheten EN_IND12-5A — §5.4 upplöst); +1 klimat 2026-06-12 (kväll,
  effektbrist): effektbrist (Svk Kraftbalansen, nettoimport vid topplasttimmen — §5.4-resten avgjord).**)*
- **+1 byggbar/öppen** (🟡; utslappsminskning_per_krona) →
  **realistiskt tak ≈ 43/67**; resten är **3 target** (⚪) + **21 genuina väggar** (🔴) + 1 undermått utan
  indikator (`industriell_konkurrenskraft`). *(Internationella försvarskällor testade 2026-06-12: SIPRI
  vapenimport-TIV källan tillåten men årssignal-brus → vägg; SIPRI/NATO milex = pengar → vägg.)*
- **28 / 35 undermått** har minst en D-serie. *(+10 sedan 2026-06-07: nato_ukraina, omsorg_personal,
  kostnadseffektivitet, aterfall_kriminalvard, biologisk_mangfald, + alla 4 D-tomma demokrati-submått
  via V-Dem → **demokrati-väggen löst på D-sidan**; **+normer_tillit +migrationssystem 2026-06-12 →
  integration 5/5; +civil_beredskap 2026-06-12 (MPF försvarsvilja) → försvar 2/5 → 3/5**.)*

| Kategori | ✅ byggd | 🟡 öppen | 🔴 vägg | ⚪ target | Indikatorer | Undermått m. D |
|----------|:---:|:---:|:---:|:---:|:---:|:---:|
| Ekonomi och jobb | **7** | 0 | 0 | 2 | 9 | 4/6 (4/4 D-bara) |
| Välfärd | **5** | 0 | 5 | 0 | 10 | **3/4** |
| Lag och trygghet | **7** | 0 | **1** | 0 | 8 | **4/5** |
| Försvar och beredskap | **4** | 0 | 5 | 1 | 10 | **3/5** |
| Klimat, miljö och energi | **7** | 1 | 1 | 0 | 9 | **4/5** |
| Integration och social sammanhållning | **7** | 0 | 4 | 0 | **11** | **5/5** |
| Frihet, demokrati och institutioner | **5** | 0 | **5** | 0 | 10 | **5/5** |
| **SUMMA** | **42** | **1** | **21** | **3** | **67** | **28/35** |

¹ klimat har 5 undermått men `industriell_konkurrenskraft` saknar indikator (ingen rad i de 63);
  `biologisk_mangfald` är öppnat 2026-06-09 → klimat 4/5 undermått med D.

### Full mastertabell — alla 56 indikatorer

| Kategori | Undermått | Indikator | Riktn. | D-status | Serie / skäl |
|----------|-----------|-----------|:---:|:---:|--------------|
| Ekonomi och jobb | Sysselsättning och arbetslöshet | `sysselsattning` | upp | ✅ byggd | 25 obs · 2001–2025 |
| Ekonomi och jobb | Sysselsättning och arbetslöshet | `arbetsloshet` | ned | ✅ byggd | 25 obs · 2001–2025 |
| Ekonomi och jobb | BNP per capita och produktivitet | `bnp_per_capita` | upp | ✅ byggd | 45 obs · 1980–2024 |
| Ekonomi och jobb | BNP per capita och produktivitet | `produktivitet` | upp | ✅ byggd | 45 obs · 1980–2024 |
| Ekonomi och jobb | Reallöner och hushållens ekonomi | `hushallens_reala_disponibla_inkomst` | upp | ✅ byggd | 75 obs · 1951–2025 (härlett realindex, Tier 1) |
| Ekonomi och jobb | Reallöner och hushållens ekonomi | `realloner` | upp | ✅ byggd | Medlingsinstitutets EGEN PxWeb, Realloner_arsdata (Reallön (KPI), Index 1995=100), 66 obs 1960–2025 (ekonomi 2026-06-12 kväll — SCB-API-väggen gällde fel instans; KPI = MI:s huvudserie, dokumenterat val; medveten dubbelbreddning i realloner_hushall) |
| Ekonomi och jobb | Företagande och investeringar | `naringslivets_investeringar` | upp | ✅ byggd | 45 obs · 1980–2024 (Tier 1) |
| Ekonomi och jobb | Inflation och prisstabilitet | `inflation` | mål | ⚪ target | nära mål, ingen up/down |
| Ekonomi och jobb | Offentliga finanser och hållbarhet | `statsskuld_underskott` | mål | ⚪ target | hållbar nivå, ingen up/down |
| Välfärd | Vårdens tillgänglighet och kvalitet | `vardkoer` | ned | ✅ byggd | 4 obs · 2021–2024 |
| Välfärd | Vårdens tillgänglighet och kvalitet | `overlevnad_svar_sjukdom` | upp | ✅ byggd | Kolada U70471 30-dagarsöverlevnad tjocktarmscancer, 16 obs 2010-2025 (natt 2026-06-08; §5.3 löst) |
| Välfärd | Vårdens tillgänglighet och kvalitet | `vard_i_tid` | upp | 🔴 vägg | `low_value`: Kolada U79142 avslutad 2023 + dubblerar vardkoer |
| Välfärd | Skolans kunskap och likvärdighet | `skolresultat` | upp | ✅ byggd | 11 obs · 2015–2025 |
| Välfärd | Skolans kunskap och likvärdighet | `behoriga_larare` | upp | ✅ byggd | 11 obs · 2015–2025 |
| Välfärd | Skolans kunskap och likvärdighet | `skillnader_mellan_skolor` | ned | 🔴 vägg | `no_api`: ingen nationell likvärdighetsserie |
| Välfärd | Omsorg och personalförsörjning | `personalomsattning_omsorg` | ned | 🔴 vägg | `no_api`: ingen omsorgsspecifik serie |
| Välfärd | Omsorg och personalförsörjning | `kontinuitet_i_omsorgen` | upp | 🔴 vägg | `B-only`: utfallsserie saknas (bidrar bara till B) |
| Välfärd | Omsorg och personalförsörjning | `brukarnojdhet_hemtjanst` | upp | ✅ byggd | Kolada U21468 brukarnöjdhet hemtjänst, 12 obs 2013–2025 (djupsvep — **öppnade omsorg_personal**) |
| Välfärd | Finansiering, styrning och anti-fusk | `valfardsbrottslighet` | ned | 🔴 vägg | `no_api`: ingen ren årsserie |
| Lag och trygghet | Grov brottslighet och våldsbrott | `dodligt_vald` | ned | ✅ byggd | 24 obs · 2002–2025 |
| Lag och trygghet | Grov brottslighet och våldsbrott | `skjutningar_sprangningar` | ned | ✅ byggd | 8 obs · 2018–2025 (transkriberad) |
| Lag och trygghet | Utsatthet och upplevd trygghet | `brottsutsatthet` | ned | ✅ byggd | 9 obs · 2016–2024 (Brå NTU) |
| Lag och trygghet | Utsatthet och upplevd trygghet | `upplevd_otrygghet` | ned | ✅ byggd | 9 obs · 2017–2025 (Brå NTU) |
| Lag och trygghet | Rättsväsendets effektivitet | `uppklaringsgrad` | upp | ✅ byggd | 10 obs · 2016–2025 |
| Lag och trygghet | Rättsväsendets effektivitet | `handlaggningstid` | ned | ✅ byggd | Domstolsverket DOMstat 01_Verksamhetsmal_TR (PxWeb v1), 75-percentil brottmål exkl. förtursmål vid tingsrätt, 19 obs 2007–2025 = 5,3→3,0 mån (trygghet 2026-06-12 kväll — förra väggen gällde Brå/ÅM, domstolsledet var förbisett; exkl.-förtursmål-bias icke-smickrande) |
| Lag och trygghet | Förebyggande arbete | `kommunalt_brottsforebyggande_arbete` | upp | 🔴 vägg | `B-only`: ingen nationell KPI för kommunal kapacitet |
| Lag och trygghet | Återfall och kriminalvård | `aterfall_i_brott` | ned | ✅ byggd | Kriminalvården KOS 2025 Tabell 6.1 (råtal→andel), 29 obs 1994–2022 (färsk session — **öppnade aterfall_kriminalvard**; KOS-tabellen gav råtalen, ingen Excel-bilaga behövdes) |
| Försvar och beredskap | Militär förmåga | `personal_varnpliktiga` | upp | ✅ byggd | 8 obs · 2018–2025 (FM ÅR, transkriberad — Tier 4) |
| Försvar och beredskap | Militär förmåga | `personalstyrka_kontinuerligt` | upp | ✅ byggd | FM ÅR bilaga Tabell 1 (Summa kontinuerligt tjänstgörande), 6 obs 2019–2024 = 22751→27734 (försvar 2026-06-12 — 2:a militar_formaga-serien; strikt monoton; bemannad numerär ≠ pengar) |
| Försvar och beredskap | Militär förmåga | `materiel_formaga` | upp | 🔴 vägg | `qualitative`: sekretess/operativ förmåga (SIPRI vapenimport-TIV testad 2026-06-12: källan tillåten men årssignal-brus → vägg) |
| Försvar och beredskap | Ekonomisk ambitionsnivå | `forsvarsanslag_andel_bnp` | mål | ⚪ target | upp till beslutad målnivå |
| Försvar och beredskap | Ekonomisk ambitionsnivå | `forsvarsfinansiering_upptrappning_mot_mal` | upp | 🔴 vägg | `B-only`: åtagande-/inriktningsmått, ej utfallsårsserie |
| Försvar och beredskap | Civil beredskap | `civil_beredskap_niva` | upp | 🔴 vägg | `qualitative`: MSB-bedömning, ingen årsserie (submåttet D-täckt via `forsvarsvilja` nedan) |
| Försvar och beredskap | Civil beredskap | `forsvarsvilja` | upp | ✅ byggd | MPF/MSB Opinioner (väpnat motstånd även om utgången oviss), 11 obs 2014–2025 (lucka 2019) (försvar 2026-06-12 — **öppnade civil_beredskap**; psykologiskt försvar/resiliensutfall; caveat 2022-toppen invasionsdriven) |
| Försvar och beredskap | Nato, Ukraina, trovärdighet | `ukraina_stod` | upp | ✅ byggd | Regeringens militära stöd/år, 4 obs 2022-2025 (natt 2026-06-08) |
| Försvar och beredskap | Nato, Ukraina, trovärdighet | `nato_interoperabilitet` | upp | 🔴 vägg | `qualitative`: ingen öppen mätserie |
| Försvar och beredskap | Genomförbarhet och leveranstakt | `leveranstid_materiel` | ned | 🔴 vägg | `qualitative`: sekretess |
| Klimat, miljö och energi | Utsläppsminskningar | `territoriella_utslapp` | ned | ✅ byggd | 35 obs · 1990–2024 |
| Klimat, miljö och energi | Utsläppsminskningar | `konsumtionsbaserade_utslapp` | ned | ✅ byggd | 16 obs · 2008–2023 |
| Klimat, miljö och energi | Energiförsörjning och elpriser | `fossil_energianvandning` | ned | ✅ byggd | 55 obs · 1970–2024 (Energimynd.) |
| Klimat, miljö och energi | Energiförsörjning och elpriser | `elprisvolatilitet` | ned | ✅ byggd | Energimyndigheten Energiindikatorer 12.5 **EN_IND12-5A** (spotpris månadsmedel SE1–SE4 → årlig CV i adaptern, ddof=0, likaviktat), 14 obs 2012–2025 (klimat 2026-06-12 kväll — **§5.4 upplöst**: officiell myndighetskälla, inte Nord Pool; 2:a serien i energi_elpriser) |
| Klimat, miljö och energi | Energiförsörjning och elpriser | `effektbrist` | ned | ✅ byggd | Svk **Kraftbalansen** (lagstadgad regeringsrapport, 3 § förordning 2007:1119): nettoimport vid vinterns topplasttimme MWh/h, vinterår → slutår, 7 obs 2020–2026 = −1700/+500/+1600/+3290/+2430/−2690/+200 (klimat 2026-06-12 kväll — **§5.4-resten avgjord**: rapportens årsvärden, ej timdata; lastfrånkoppling aldrig inträffad → nettoimport = närliggande bärare, down direkt; ⚠ väderdriven, normalvinter-prognos som robusthetsreferens) |
| Klimat, miljö och energi | Omställningens kostnadseffektivitet | `utslappsminskning_per_krona` | upp | 🟡 öppen | `derived`: utsläpp/kostnad — **def. "klimatutgift" §5.5** |
| Klimat, miljö och energi | Omställningens kostnadseffektivitet | `utslappsintensitet` | ned | ✅ byggd | härledd ratio territoriella utsläpp (TAB4698) ÷ BNP (TAB3610 BNPM), 35 obs 1990–2024 (djupsvep — **öppnade kostnadseffektivitet**) |
| Klimat, miljö och energi | Biologisk mångfald och natur | `hotade_arter_naturforlust` | ned | 🔴 vägg | `no_api`: SLU rödlistan, ingen årlig maskinläsbar serie |
| Klimat, miljö och energi | Biologisk mångfald och natur | `hackande_faglar_skog` | upp | ✅ byggd | Svensk Fågeltaxering/Lund (sverigesmiljomal.se Highcharts), 23 obs 2002–2024 (färsk session — **öppnade biologisk_mangfald**; ⚠ brusig/trendlös → D≈neutral) |
| Klimat, miljö och energi | Industriell konkurrenskraft | _(ingen indikator)_ | — | 🔴 vägg | saknar indikator (steg-1-vägg, §4.2 i B-trackern) |
| Integration och social sammanhållning | Arbete och självförsörjning | `sysselsattningsgap_inrikes_utrikes` | ned | ✅ byggd | 21 obs · 2005–2025 (härlett) |
| Integration och social sammanhållning | Arbete och självförsörjning | `sjalvforsorjningsgrad` | upp | ✅ byggd | 21 obs · 2005–2025 |
| Integration och social sammanhållning | Arbete och självförsörjning | `bidragsberoende` | ned | ✅ byggd | 15 obs · 2010–2024 |
| Integration och social sammanhållning | Skola, språk och utbildning | `sfi_sprakkunskaper` | upp | ✅ byggd | 27 obs · 1997–2023 (Tier 2) |
| Integration och social sammanhållning | Skola, språk och utbildning | `skolresultat_utsatta_omraden` | upp | 🔴 vägg | `no_api`: ingen ren nationell årsserie |
| Integration och social sammanhållning | Boendesegregation och trygghet | `trangboddhet` | ned | ✅ byggd | 15 obs · 1988–2025 |
| Integration och social sammanhållning | Boendesegregation och trygghet | `segregation` | ned | 🔴 vägg | `no_api`: ingen ren officiell segregationsårsserie |
| Integration och social sammanhållning | Normer, tillit och samhällsgemenskap | `tillit_valdeltagande` | upp | 🔴 vägg | `no_api/sparse`: valdeltagande bara valår; SOM-tillit ej API (submåttet D-täckt via `mellanmansklig_tillit` nedan) |
| Integration och social sammanhållning | Normer, tillit och samhällsgemenskap | `mellanmansklig_tillit` | upp | ✅ byggd | SCB:s medborgarundersökning "kan generellt lita på människor" (Kolada N00666), 5 obs 2021–2025 (integration 2026-06-12 — **öppnade normer_tillit**; rätt konstrukt vs N00665 politikerförtroende; nära platt 61–63 % → D≈neutral) |
| Integration och social sammanhållning | Migrationssystemets hållbarhet | `atervandande_effektivitet` | upp | 🔴 vägg | `B-only`: ingen publik årsserie för kostnad/effektivitet (submåttet D-täckt via `asyl_handlaggningstid` nedan) |
| Integration och social sammanhållning | Migrationssystemets hållbarhet | `asyl_handlaggningstid` | ned | ✅ byggd | Migrationsverket "Avgjorda asylärenden" (förstagångs-Asyl, exkl. massflykt), 5 obs 2021–2025 = 257/166/198/187/180 dgr (integration 2026-06-12 — **öppnade migrationssystem**; genuin teckenväxling; neutralt vs återvändande, kvalitet-vs-hastighet-caveat) |
| Frihet, demokrati och institutioner | Rättsstat och maktdelning | `otillborlig_politisering` | ned | 🔴 vägg | `qualitative`: ingen objektiv mätserie (submåttet D-täckt via V-Dem nedan) |
| Frihet, demokrati och institutioner | Rättsstat och maktdelning | `rattsstatsindex` | upp | ✅ byggd | V-Dem `v2x_rule`, 26 obs 2000–2025 (färsk session — **öppnade rattsstat_maktdelning**; nära platt → D≈neutral) |
| Frihet, demokrati och institutioner | Korruption och myndighetstillit | `fortroende_domstolar_myndigheter` | upp | ✅ byggd | 9 obs · 2017–2025 (Brå NTU 5A:1 — Tier 4) |
| Frihet, demokrati och institutioner | Korruption och myndighetstillit | `korruption` | ned | 🔴 vägg | `international`: TI CPI ej officiell svensk källa |
| Frihet, demokrati och institutioner | Yttrandefrihet och medier | `mediefrihet` | upp | 🔴 vägg | `international`: RSF-index ej officiell svensk källa (submåttet D-täckt via V-Dem nedan) |
| Frihet, demokrati och institutioner | Yttrandefrihet och medier | `yttrandefrihetsindex` | upp | ✅ byggd | V-Dem `v2x_freexp_altinf`, 26 obs 2000–2025 (färsk session — **öppnade yttrandefrihet_medier**; nedgång 2018+2023) |
| Frihet, demokrati och institutioner | Personlig frihet och integritet | `overvakning_utan_rattssakerhet` | ned | 🔴 vägg | `qualitative`: ingen objektiv mätserie (submåttet D-täckt via V-Dem nedan) |
| Frihet, demokrati och institutioner | Personlig frihet och integritet | `privata_friheter` | upp | ✅ byggd | V-Dem `v2x_clpriv`, 26 obs 2000–2025 (färsk session — **öppnade personlig_frihet**) |
| Frihet, demokrati och institutioner | Transparens och ansvarsutkrävande | `politisk_transparens` | upp | 🔴 vägg | `qualitative`: ingen kvantitativ officiell årsserie (submåttet D-täckt via V-Dem nedan) |
| Frihet, demokrati och institutioner | Transparens och ansvarsutkrävande | `horisontellt_ansvarsutkravande` | upp | ✅ byggd | V-Dem `v2x_horacc_osp`, 26 obs 2000–2025 (färsk session — **öppnade transparens_ansvar**; horacc, ej diagacc, för att ej dubbelräkna media) |

**Partiaxeln (orthogonal mot tabellen ovan):** `V` får `D_not_applicable` i *alla* kategorier
(aldrig nationell regering 2014–2026) — det är en attributions-egenskap, inte en täckningslucka, och
påverkar inte raderna ovan. Se §2.

---

## 3. Arbetskö — D-lösa submått med byggbarhet

Status: 🔵 nästa · ⚪ planerad · 🟣 designbeslut krävs · 🔴 blockerad/stängd · ✅ klar.
Effort: `S` återanvänder befintlig adapter · `M` ny adapter · `L` transkribering/research/design.

> **✅ Djupsvepets sign-off-byggkö EXEKVERAD 2026-06-09 (färsk session, utöver Tier 1–4 nedan):**
> `aterfall_i_brott` (Kriminalvården KOS → aterfall_kriminalvard), `hackande_faglar_skog` (Svensk
> Fågeltaxering → biologisk_mangfald) och 4 V-Dem-index (Göteborgs univ. → de 4 D-tomma demokrati-
> submåtten). **Försvarsutgifter % BNP HÅLLS** (luktar A/dubbelräkning, ej D). Full logg: §7.

### Tier 1 — billigast: återanvänder SCB-adaptern (S) ✅ LEVERERAD 2026-06-07

Indikatorerna fanns redan i `categories.yaml` (tillagda för B), men hölls **B-only**. §5.1-beslutet
(häv B-only, bygg som v0) togs 2026-06-07. **Ekonomi 2 → 4 D-täckta submått (alla 4 D-bara täckta).**

| ☑ | Indikator | Kategori → submått | Källa/metod | Effort | Not |
|---|-----------|--------------------|-------------|:---:|-----|
| ☑ | `naringslivets_investeringar` | ekonomi → foretagande_investeringar | SCB NR **TAB3610** Anvandningstyp=`BNAR` (näringslivets fasta bruttoinv, **fasta priser** ref 2020), `build_fas2` | S | ✅ inläst 1980–2024, ur allowlisten. v0, sign-only D. |
| ☑ | `hushallens_reala_disponibla_inkomst` | ekonomi → realloner_hushall | SCB NR **TAB4592** `B6nRealGrowth`/`S14` → kumulerat **realindex** (`derived.py` op `index`) | S→M¹ | ✅ inläst 1951–2025, ur allowlisten. v0, sign-only D. |

¹ Visade sig kräva en härledning: real disp. inkomst publiceras bara som *tillväxttakt*, så D-nivån
byggs som ett kumulativt realindex (tecken på indexförändring = tecken på officiell real tillväxt).
Drift-skyddet sitter på föräldra-tillväxtserien. Något mer än ren "reuse adapter", men deterministiskt
och golden-testat (`tests/test_derived.py`).

### Tier 2 — ny adapter, källa finns (M) ⚪ (sfi LEVERERAD 2026-06-07)

| ☑ | Indikator | Kategori → submått | Källa/metod | Effort | Not |
|---|-----------|--------------------|-------------|:---:|-----|
| ☑ | `sfi_sprakkunskaper` | integration → skola_sprak | SCB **TAB1814** `AA0003EB` (andel godkända i sfi %, `build_fas2`) | **S**¹ | ✅ inläst 1997–2023, ur allowlisten. **Öppnade skola_sprak (D-löst submått).** §5.2 avgjort av datan (godkäntandel = enda direktionskonsistenta måttet). v0, sign-only D. |
| ☐ | `overlevnad_svar_sjukdom` | valfard → vard_tillganglighet | Socialstyrelsen/Kolada — **annuell** överlevnadsserie | M | Submått redan täckt (djup, ej bredd). Cancer-KPI N79196 = kvinkennial/inkompatibel; **annuellt alternativ behöver sonderas** (t.ex. 28-dygnsöverlevnad AMI/stroke) (§5.3). |
| ☑ | `realloner` | ekonomi → realloner_hushall | Medlingsinstitutets **egen PxWeb** (Realloner_arsdata, Reallön (KPI) Index 1995=100) | M→S² | ✅ inläst 1960–2025, ur allowlisten (2026-06-12 kväll). v0, sign-only D. |

¹ Visade sig vara **S, inte M**: SCB (producenten) exponerar sfi-statistiken som en ren PxWeb-v2-
tabell (TAB1814), så den befintliga `scb.py`-adaptern räckte — ingen egen Skolverket-portaladapter
behövdes. Allowlistens "ej ren PxWeb"-antagande (Skolverkets portal) var överspelat. Metodbrott 2022
hanteras genom att hela serien behålls (sign-only D är robust mot magnitudskiftet); se §7 + `build_fas2`-not.

² Samma mönster som ¹: väggen ("SCB:s API saknar ren helekonomi-löneserie", sonderat 2026-05-31) var
sann men gällde FEL INSTANS — Medlingsinstitutet har en EGEN PxWeb (v1, samma dialekt som Domstols-
verket/Energimyndigheten) med Realloner_arsdata som ren årsserie 1960–2025. Adapterkostnaden blev S
(kopia av domstolsverket-mönstret). KPI-valet (MI:s huvudserie, ej KPIF) dokumenterat i adaptern; se §7.

### Tier 3 — härledd, kräver ny föräldraadapter (M+S) ⚪🟣

| ☐ | Indikator | Kategori → submått | Metod | Effort | Not |
|---|-----------|--------------------|-------|:---:|-----|
| ☑ | *(Svk-källadapter)* | ~~förkrav klimat-energi~~ | ~~Svenska kraftnät öppna data (effektbalans)~~ | ~~M~~ | ✅ FÖRKRAVET STÄNGT 2026-06-12 (kväll): effektbrist byggdes via Svk:s KRAFTBALANSRAPPORT (transkriberad config + tunn reader `pipeline/sources/svk.py`) — ingen tim-/effektdata-adapter (Mimer/eSett) behövdes, §5.4-gränsfallet upplöst utan att öppnas. |
| ☑ | `elprisvolatilitet` | klimat → energi_elpriser | ~~härled ur Svk spotpris~~ → **Energimyndigheten EN_IND12-5A** (årlig CV i adaptern, befintlig PxWeb-v1-adapter utökad) | M+S→**S** | ✅ inläst 2012–2025, ur allowlisten (2026-06-12 kväll). Svk-förkravet föll bort — myndighetskällan täcker spotpriset (§5.4). Submått redan täckt (djup). v0, sign-only D. |
| ☑ | `effektbrist` | klimat → energi_elpriser | ~~härled ur Svk effektbalans~~ → **Svk Kraftbalansen-rapporten** (nettoimport vid vinterns topplasttimme, transkriberad config) | S→**L** | ✅ inläst 2020–2026 (vintrar 2019/20–2025/26), ur allowlisten (2026-06-12 kväll). Ingen härledning behövdes — rapporten publicerar årsvärdet färdigt. Submått redan täckt (djup — 3:e serien). Tier 3 därmed tömd sånär som på utslappsminskning_per_krona (§5.5). v0, sign-only D. |
| ☐ | `utslappsminskning_per_krona` | klimat → kostnadseffektivitet | utsläpp ÷ klimatutgift | L | Öppnar D-löst submått, men "klimatutgift" är metodiskt omtvistad (vilket UO?) → §5.5. |

### Tier 4 — transkribering med källrad, fyller strukturella nollor (L) 🟣 (varnpliktiga LEVERERAD 2026-06-07)

Samma trogna transkriberingsmönster som `budget_ramar.yaml` / SKR / `skjutningar_sprangningar.yaml`
(källrad per värde, korsverifiering, auditverktyg). **Högsta strategiska värde** — ger de två
D-blanka kategorierna sin första utfallsserie — men störst arbete och integritetskrav.

| ☑ | Indikator | Kategori → submått | Källa/metod | Effort | Not |
|---|-----------|--------------------|-------------|:---:|-----|
| ☑ | `personal_varnpliktiga` | **forsvar** → militar_formaga | **Försvarsmaktens ÅR** (antal påbörjade GU/år 2018–2025), korsverif. mot Pliktverkets inskrivna | L | ✅ inläst, ur allowlisten. **GAV FÖRSVAR DESS FÖRSTA D.** "varför inte båda" löst: FM = värde, Pliktverket = oberoende korsverifiering; båda visar samma enda nedgång 2021→2022. v0. |
| ☑ | `fortroende_domstolar_myndigheter` | **demokrati** → korruption_tillit | **Brå NTU 5A:1** (förtroende rättsväsendet som helhet, andel ganska/mycket stort förtroende), `bra.fetch_ntu` | L→**S**¹ | ✅ inläst 2017–2025, ur allowlisten. **GAV DEMOKRATI DESS FÖRSTA D.** Officiell källa (Brå/SOS) krävs framför SOM (akademiskt). v0. |
| ☐ | `tillit_valdeltagande` | integration → normer_tillit | SOM-institutet (akademisk) | L | 🔴 BEVAKA: B-only/utvidgningskandidat, ej D-byggas (categories.yaml-not). Öppnar D-löst submått först om neutralt ankare dyker upp. |

¹ Visade sig vara **S, inte L** (samma mönster som sfi): Brå NTU — en *officiell* källa — mäter förtroende
för rättsväsendet (5A:1) som en ren xlsx-tabell via den befintliga `bra.fetch_ntu`-adaptern, så ingen
SOM-transkribering behövdes. CLAUDE.md *kräver* dessutom officiell källa när sådan finns (akademiskt bara
"när officiell statistik saknas") → SOM hade varit otillåtet här. Allowlistens "no_api: SOM"-antagande överspelat.

### Tier 5 — blockerade / stängda som designbeslut 🔴 (bygg **inte**)

Listade här för fullständighet så de inte återöppnas oavsiktligt. Skäl i allowlisten.

- **`target`-indikatorer** (ingen up/down): `inflation`, `statsskuld_underskott`, `forsvarsanslag_andel_bnp`.
- **`international`** (otillåtet som primärkälla, CLAUDE.md): `korruption` (TI CPI), `mediefrihet` (RSF).
  *(OBS: deras SUBMÅTT är nu D-täckta via V-Dem-syskonindikatorer — yttrandefrihet_medier→`yttrandefrihetsindex`;
  korruption_tillit har `fortroende_domstolar_myndigheter`. Dessa specifika TI/RSF-index förblir stängda.)*
- **`qualitative`/sekretess** (försvar/demokrati): `materiel_formaga`, `civil_beredskap_niva`,
  `nato_interoperabilitet`, `leveranstid_materiel`, `otillborlig_politisering`,
  `overvakning_utan_rattssakerhet`, `politisk_transparens`. *(OBS: de fyra demokrati-submåtten är nu
  D-täckta via V-Dem (`rattsstatsindex`/`yttrandefrihetsindex`/`privata_friheter`/`horisontellt_ansvarsutkravande`);
  dessa gamla kvalitativa indikatorer förblir stängda som B-/visningsindikatorer.)*
- **`no_api`** (ingen maskinläsbar årsserie): `skillnader_mellan_skolor`, `personalomsattning_omsorg`,
  `valfardsbrottslighet`, `hotade_arter_naturforlust`, `skolresultat_utsatta_omraden`, `segregation`.
- ~~**`future`/interaktiv DB**: `handlaggningstid`~~ — ✅ ÅTERÖPPNAD OCH BYGGD 2026-06-12 (kväll):
  väggen gällde Brå/ÅM-ledet; Domstolsverkets DOMstat (SOS) bär en ren PxWeb-årsserie för
  domstolsledet (se §2.1 + §7).
- **`low_value`/inkompatibel**: `vard_i_tid` (dubblerar vardkoer, avslutad 2023);
  `overlevnad`-cancer-KPI N79196 (kvinkennial → kräver annuellt alternativ, se Tier 2).
- **B-only-indikatorer** (utfallsserie saknas, bidrar bara till B): `kommunalt_brottsforebyggande_arbete`,
  `kontinuitet_i_omsorgen`, `forsvarsfinansiering_upptrappning_mot_mal`, `atervandande_effektivitet`.

---

## 4. Rekommenderad ordning

1. ~~**Tier 1**~~ ✅ — ekonomi till full D-täckning av sina D-bara submått (2026-06-07, §7).
2. ~~**Tier 2 `sfi_sprakkunskaper`**~~ ✅ — öppnade integration/skola_sprak (D-löst submått); visade sig
   vara **S, inte M** (SCB exponerar TAB1814 som ren PxWeb v2 → befintlig adapter räckte) (2026-06-07, §7).
3. ~~**Tier 4 strukturella nollor**~~ ✅ — BÅDA fyllda 2026-06-07 (§7): `personal_varnpliktiga` (FM ÅR)
   gav **försvar** sin första D; `fortroende_domstolar_myndigheter` (Brå NTU 5A:1 — officiell, ej SOM)
   gav **demokrati** sin första D. **Alla 7 kategorier har nu D.** Båda strukturella nollorna ur
   exit-kriterium §6.2 är därmed uppfyllda.
4. ~~**Tier 3 Svk-derived**~~ ✅ — *(Uppdaterat 2026-06-12 kväll: `elprisvolatilitet` ✅ byggd UTAN Svk —
   Energimyndigheten EN_IND12-5A täckte spotpriset, §5.4 upplöst för pris-delen. `effektbrist` ✅ byggd
   samma kväll via Svk:s KRAFTBALANSRAPPORT (transkriberad config, ej timdata) — §5.4-resten avgjord
   utan att Mimer/eSett-gränsfallet behövde öppnas. Kvar i Tier 3: endast `utslappsminskning_per_krona`
   (§5.5, designfråga).)*
5. ~~**Tier 2-rest** (`overlevnad_svar_sjukdom` §5.3, `realloner`)~~ ✅ — båda byggda
   (overlevnad 2026-06-08 via Kolada U70471; realloner 2026-06-12 kväll via MI:s egen PxWeb).
   Tier 2 är därmed tömd.

> **Ärlig brasklapp:** den billiga rena-API-vågen är i allt väsentligt redan skördad (Fas 2–3). Det
> som återstår är antingen ett **uppskjutet designbeslut** (Tier 1), **nya adaptrar** (Tier 2–3),
> eller **transkribering** (Tier 4). Det finns ingen mer "gratis" SCB/Kolada-serie att plocka.

---

## 5. Öppna beslut (kräver din sign-off innan bygge)

### 5.1 Tier 1: häva "B-only" för de två SCB-NR-serierna? ✅ AVGJORT 2026-06-07 (bygg, v0)
Båda hölls B-only med skäl *konjunkturkänslig → D-attribution brusig*. Men D är redan byggt för
konjunkturkänsliga serier (`bnp_per_capita`, `produktivitet`) med *tecken-ej-magnitud* + 10 %-vikt +
makt-/ansvarsviktning + flaggor. **Beslut (din sign-off 2026-06-07): bygg båda som v0.** Levererat
(§7); ekonomi-effekt liten + förklarbar, ranking oförändrad.

### 5.2 `sfi_sprakkunskaper`: vilken semantik? ✅ AVGJORT 2026-06-07 (av datan — godkäntandel)
Godkäntandel (nivå) vs progression/genomströmning. **Datan avgjorde:** SCB:s TAB1814 har båda måtten
som var sin ContentsCode — godkäntandel (`AA0003EB`, riktning **up**) och vistelsetid-median för
godkända (`AA0003EC`, riktning **down**, dvs. progressionsmåttet). Bara godkäntandel matchar
indikatorns kanoniska riktning (`up` i categories.yaml); progression skulle kräva att riktningen
flippas, dvs. en omdefiniering av indikatorn — inte "bygg Tier 2". **Beslut: godkäntandel (AA0003EB).**
Levererat (§7). Metodbrott 2022 hanterades genom att behålla hela serien (sign-only D robust).

### 5.3 `overlevnad_svar_sjukdom`: finns en annuell serie? ✅ AVGJORT 2026-06-08 (natt — Kolada U70471)
Cancer-5-årsöverlevnad (Kolada N79196) är kvinkennial → inkompatibel med D:s konsekutiva-år-krav.
**Löst:** Kolada **U70471** (30-dagarsöverlevnad efter akut tjocktarmscancerkirurgi) är den annuella
officiella serien (16 obs 2010–2025), inläst i natt-bygget (§7). Ingen modellutvidgning behövdes.

### 5.4 Svk-adapter: håller den källregeln? ✅ AVGJORT 2026-06-12 (av sonderingen — officiell svensk källa funnen, jfr §5.3-mönstret); §5.4-RESTEN ✅ AVGJORT 2026-06-12 (kväll)
Spotpris (Nord Pool) + operativ effekt-/timdata var gränsfall mot "officiell svensk källa".
**UPPLÖST för spotpris-delen:** Energimyndighetens statistikdatabas (statlig myndighet) publicerar
elspotpriset som officiell månadsserie — **Energiindikatorer 12.5, tabell EN_IND12-5A** (SE1–SE4,
2011M11–) — så `elprisvolatilitet` byggdes 2026-06-12 (kväll) direkt mot myndighetskällan, helt utan
Nord Pool/Svk (§7). Samma mönster som §5.3: sonderingen fann en officiell väg som gjorde gränsfallet
irrelevant. **§5.4-RESTEN ✅ AVGJORT samma kväll:** `effektbrist` löstes via **Svk:s lagstadgade
KRAFTBALANSRAPPORT** ("Kraftbalansen på den svenska elmarknaden", 3 § förordning 2007:1119) — UTFALLS-
kapitlet "Vinterns topplasttimme" publicerar nettoimporten som färdigt årsvärde, så ingen tim-/
effektdata behövdes (data.svk.se saknar ännu ett förbruknings-/effektbalansdataset; Mimer/eSett-
gränsfallet blev aldrig aktuellt — Svk själv, ett statligt affärsverk, är källan rakt av).
Transkriberad config + tunn reader (§7). §5.4 är därmed HELT stängd.

### 5.5 `utslappsminskning_per_krona`: hur definieras "klimatutgift"?
Kräver en officiell, riktningsneutral nämnare (vilka UO/anslag räknas som klimatutgift?). Metodiskt
omtvistat → designfråga, inte ren databredd.

---

## 6. Exit-kriterier (när flyttas dokumentet till `docs/done/`?)

Spår D anses **färdigt för arkivering** när:

1. Varje icke-blockerad D-lös submått (Tier 1–4) är **antingen byggd** (serie inläst, ur allowlisten,
   golden-testad) **eller** har ett dokumenterat HOLD/stängt-beslut med skäl i allowlisten.
   *(Status 2026-06-07: Tier 1+2+4 byggda. Kvar: Tier 3 Svk-derived (öppnar inget D-löst submått) +
   Tier 2-rest overlevnad/realloner — alla har dokumenterat skäl/HOLD, inget tyst gap.)*
2. ✅ **UPPFYLLT 2026-06-07:** båda strukturella nollorna har sin första D-serie — **försvar**
   (`personal_varnpliktiga`, FM ÅR) och **demokrati** (`fortroende_domstolar_myndigheter`, Brå NTU 5A:1).
   Alla 7 kategorier har nu D.
3. `coverage_allowlist.yaml` innehåller bara poster i klasserna `target`/`international`/`qualitative`/
   `blocked`/`no_api` (= genuint ej byggbara) — inga `future`-poster kvar utan beslut. *(Kvar att städa:
   endast utslappsminskning_per_krona (§5.5, designfråga); overlevnad_svar_sjukdom byggd 2026-06-08,
   realloner byggd 2026-06-12 kväll, elprisvolatilitet byggd 2026-06-12 kväll (§5.4 upplöst),
   effektbrist byggd 2026-06-12 kväll (§5.4-resten avgjord — Svk Kraftbalansen, ej timdata).)*
4. `docs/fas3_coverage.md` + `scorerun.py:coverage`-strängen speglar slutläget; testsviten grön. ✅

---

## 7. Leveranslogg (append per leverans)

> Format: datum · indikator · kategori→submått · källa · verifiering · betygseffekt · flagga/version.

### ✅ 2026-06-12 (kväll) — Spår D klimat: `effektbrist` byggd via Svk Kraftbalansen, §5.4-resten avgjord (v0, FLAGGAD)

**1 bygge, 1 ny D-serie; coverage 41/67 → 42/67 inlästa; undermått oförändrat 28/35** (energi_elpriser
hade redan fossil_energianvandning + elprisvolatilitet — detta är djup, inte bredd: 3:e serien; Tier 3
därmed tömd sånär som på utslappsminskning_per_krona, och Svk-adapter-förkravet stängt).

1. **`effektbrist`** (klimat → energi_elpriser, ned): **nettoimport vid vinterns topplasttimme**
   (MWh/h; positivt = nettoimport, negativt = nettoexport) — **Svenska kraftnät** (statligt
   affärsverk = officiell svensk källa), **"Kraftbalansen på den svenska elmarknaden"**, årlig
   LAGSTADGAD regeringsrapport (3 § förordning 2007:1119), UTFALLS-kapitlet "Vinterns topplasttimme".
   7 obs, vintrarna 2019/20–2025/26 etiketterade på SLUTÅRET: 2020: −1700 · 2021: +500 · 2022: +1600 ·
   2023: +3290 · 2024: +2430 · 2025: −2690 · 2026: +200. **MÅTTVAL (sonderat och avgjort):** faktisk
   effektbrist (lastfrånkoppling) har ALDRIG inträffat — Svk rapport 2025 s.30 explicit ("Svenska
   kraftnät har därför aldrig behövt koppla bort elförbrukning på grund av effektbrist") → konstant 0
   bär inget D-tecken; nettoimporten under årets mest ansträngda timme = trogen närliggande bärare
   (högre importberoende = mindre inhemsk effektmarginal = närmare effektbrist), och riktningen
   **down matchar DIREKT** (lägre nettoimport/mer export = bättre), ingen teckenmappning.
   **Korrigering av tidigare antagande:** allowlist-posten (`derived`, "härleds ur Svk effektdata,
   ingen färdig årsserie") och Tier 3-Svk-adapter-förkravet var överspelade — rapporten publicerar
   årsvärdet FÄRDIGT, ingen härledning ur tim-/effektdata (Mimer/eSett-gränsfallet blev aldrig
   aktuellt; data.svk.se saknar ännu förbrukningsdataset) → **§5.4 HELT stängd**. Transkriberad
   config (`config/effektbrist.yaml`, källrad + rapportutgåva per värde) + tunn reader
   (`pipeline/sources/svk.py`, config → observations, nätverksfri) — samma mönster som
   personal_varnpliktiga/ukraina_stod/skjutningar_sprangningar.

**Verifiering:** ALLA 7 årsvärden MASKINVERIFIERADE 2026-06-12 ur Svk:s original-PDF:er (PyMuPDF):
2024/2025/vår-2026 ur live-PDF:erna på svk.se; 2020–2023 ur web.archive.org-snapshots AV SVK-
ORIGINALEN (utgåvorna 404 på svk.se; wayback-URL = hämtväg i configen, källan förblir rapporttitel
+ år). Varje övergång dessutom korsbekräftad av påföljande års rapport ("förra vintern var det ...")
→ alla 6 D-tecken dubbelkällade inom rapportserien. SEKUNDÄRSERIE (robusthetsreferens, matar EJ D):
Svk:s vädernormerade prognos för nationell effektbalans normalvinter, även den maskinverifierad
(2021: −1700 · 2022: −1600 · 2023: −1400 · 2024: −1400 · 2025: −1300 · 2026: +600) — samma
underliggande förlopp utan väderbrus, dokumenterad som kommentarsblock i configen. Ankarreferens:
Svk:s HTML-tabell över topplasttimmen (datum/topplast per vinter 2002/03–2024/25; decemberundantagen
2019/20 + 2021/22 noterade). Drift-skydd: min_points 7, range [−6000, 8000], min_latest_year 2026,
ankare 2023=3290. Oberoende attributionssanity (lag 1 år, ned-indikator, handräknad): 2024→2025
+2430→−2690 stort fall (förbättring) → år 2024 = M/KD/L+SD ✓; 2020→2021 −1700→+500 försämring →
år 2020 = S/MP ✓; 2025→2026 −2690→+200 försämring → år 2025 = M/KD/L+SD ✓ — bekräftade mot
scorerun-utfallet (Tidö netto upp: 2 förbättringar + 1 försämring; S/MP/C netto ned). Golden-test
(`tests/test_source_svk.py`: pinnade årsvärden, teckenbevarande för nettoexport-åren, 7 konsekutiva
slutår, radform/id-mönster, prognosserie-läckagegrind, kanonisk riktning down, källrad per år +
wayback-krav för 404-årgångarna); registrerad i `test_fas3_gate._ingested()` (svk.INDICATORS →
klimat); hela offline-sviten grön (264 passed, 4 skipped); coverage-gaten håller (`coverage_report`:
effektbrist ✓A, 7 obs 2020..2026, SUMMA 42/67).

**Betygseffekt (score_diff):** endast **klimat**-celler rör sig, och serien DIFFERENTIERAR (S bär
försämringarna 2020→21/2021→22/2022→23, Tidö krediteras förbättringarna 2023→24/2024→25 men bär
försämringen 2025→26): S −0,027 · MP −0,026 · C −0,020 · KD +0,013 · SD +0,013 · M +0,012 ·
L +0,002 (Tidö-vinsterna nettas mot stödåren 2019–2021) · V ±0 (D_not_applicable). Totaler:
S −0,004 · MP −0,003 · C −0,002 · KD/M/SD +0,002 · L/V ±0. **Ranking OFÖRÄNDRAD**
(S>L>M>KD>MP>C>SD>V). `dist/` omräknat + snapshot re-baselinad.

**Flaggor/version:** v0 (FLAGGAD — kräver mänsklig granskning; caveats: VÄDERDRIVEN serie — kall
vinter ⇒ högre topplast/import oavsett politik (mild-2025-outliern: mild + blåsig, vind 62 % av
installerad effekt → ovanlig nettoexport); delvis prisdriven import (Svk: oftast billigare el, inte
uttömda inhemska resurser); kort serie (6 förändringar) → sign-only D + 10 %-vikt + makt-/ansvars-
viktning mildrar; normalvinter-prognosserien som vädernormerad robusthetsreferens i configen).
v0 → v1 vid expertgranskning.

### ✅ 2026-06-12 (kväll) — Spår D klimat: `elprisvolatilitet` byggd, §5.4-källregelfrågan upplöst (v0, FLAGGAD)

**1 bygge, 1 ny D-serie; coverage 40/67 → 41/67 inlästa; undermått oförändrat 28/35** (energi_elpriser
hade redan fossil_energianvandning — detta är djup, inte bredd: 2:a serien + 14 kompletta år).

1. **`elprisvolatilitet`** (klimat → energi_elpriser, ned): årlig **variationskoefficient CV =
   populations-stdev (ddof=0) / medel över årets 12 månadsmedel** av elspotpriset (kr/MWh), per
   elområde, **likaviktat medel SE1–SE4**, i % — **Energimyndighetens statistikdatabas** (statlig
   myndighet), **Energiindikatorer 12.5, tabell `EN_IND12-5A.px`** ("Elspotpris Sverige (från
   november 2011), månadsmedelvärden"), PxWeb v1 (samma host/dialekt som EN0202_8 — den BEFINTLIGA
   energimyndigheten-adaptern UTÖKADES, ingen ny modul). 14 obs 2012–2025 (26,7 → 9,3 → … → 43,3 →
   41,8 → **62,6 (2022-toppen)** → 40,2 → 53,9 → 36,1). **Korrigering av tidigare antagande:**
   allowlist-posten (`derived`, "härleds ur Svk/spotpriser") och Tier 3-förkravet Svk-adapter var
   överspelade — **§5.4-källregelfrågan UPPLÖST**: datakällan är Energimyndighetens officiella
   statistikdatabas, inte Nord Pool (samma mönster som §5.3: officiell väg funnen av sonderingen).
   **MÅTTVAL (dokumenterat i adaptern):** (a) **CV är skalfri** — straffar instabilitet, inte
   prisNIVÅ/inflation (indikatorn heter volatilitet); standard, riktningsneutralt; förkastade: rå
   stdev (nivå-/inflationskänslig), max–min (outlierkänslig); (b) **ddof=0 låst** i docstring +
   golden-test (sonderingens referens med ddof=1 = våra värden × √(12/11), t.ex. 2022: 65,3 mot
   62,6 — dokumenterad avvikelse, identisk serieform/tecken); (c) endast 12/12-kompletta år per
   elområde (2011 = nov–dec → utesluts; framtida lucka fäller hela året i stället för tyst
   snedviktning); (d) **likaviktning SE1–SE4** (enklare + neutralt, inget viktkälleval); (e) CV
   beräknas **I ADAPTERN** — månadsobservationer skrivs aldrig till warehouse (period_to_year ger
   None för YYYYMmm → döda rader; prejudikat kriminalvarden.py).

**Verifiering:** live-extraktion 2026-06-12 matchar publicerade månadsvärden exakt (SE3 kr/MWh:
2021M01=491, 2022M08=2230, 2022M12=2690, 2023M06=531, 2025M12=517); serien är lucka-fri 2011M11–
2025M12 (170 månader × 4 elområden, inga None). Årsvärden (CV %, likaviktat): 2012: 26,7 · 2013: 9,3
· 2014: 9,6 · 2015: 26,9 · 2016: 23,1 · 2017: 6,8 · 2018: 16,7 · 2019: 16,2 · 2020: 43,3 · 2021: 41,8
· 2022: 62,6 · 2023: 40,2 · 2024: 53,9 · 2025: 36,1. Drift-skydd: ankare 2022=62,56, min_points 12,
range [2,120], min_latest_year 2025. Oberoende attributionssanity (lag 1 år, ned-indikator):
2021→2022 41,8→62,6 stegring (dåligt) → år 2021 = S (+C/L-stöd, MP t.o.m. nov) ✓; 2023→2024
40,2→53,9 stegring → år 2023 = Tidö ✓; 2024→2025 53,9→36,1 fall (bra) → år 2024 = Tidö ✓ — alla
tre tecken bekräftade mot scorerun-utfallet. Golden-test (utökat `tests/test_source_energimyndigheten.py`
+ äkta beskuren json-stat2-fixtur: 2011M11–M12 + hela 2021 + hela 2022 × SE1–SE4; pinnar CV-värdena,
12/12-regeln, ddof=0 via handräknat facit 100/300-alternering → CV exakt 50,0 %, hård-fail-grindar
för icke-eliminerad dimension + periodformatdrift, radform); INDICATORS-registreringen täcks av
befintlig `test_fas3_gate._ingested()`-rad (energimyndigheten → klimat); hela offline-sviten grön
(256 passed, 4 skipped); coverage-gaten håller (`coverage_report`: elprisvolatilitet ✓A, 14 obs
2012..2025, SUMMA 41/67).

**Betygseffekt (score_diff):** endast **klimat**-celler rör sig, och serien DIFFERENTIERAR
(2022-toppen attribueras år 2021 = S+stöd; 2022→2023- och 2024→2025-fallen krediterar Tidö, som
dock även bär 2023→2024-stegringen): M +0,029 · KD +0,029 · SD +0,029 · L +0,005 · S −0,007 ·
MP −0,011 · C −0,019 · V ±0 (D_not_applicable). Totaler: SD +0,004, KD/M +0,003, C −0,003,
MP −0,001, S/L ±0. **Ranking OFÖRÄNDRAD** (S>L>M>KD>MP>C>SD>V). `dist/` omräknat + snapshot
re-baselinad.

**Flaggor/version:** v0 (FLAGGAD — kräver mänsklig granskning; måttvals-caveats: månadsupplösning
underskattar tim-/dygnsvolatilitet — negativa timpriser/spotspikar syns ej, måttet fångar säsongs-/
strukturell instabilitet, effektproblematik täcks av syskonet `effektbrist` när den byggs;
volatiliteten drivs starkt av europeiska gaspriser/överföringsläge (2022) — sedvanlig D-konjunktur-
caveat (tecken-ej-magnitud + 10 %-vikt + ansvarsviktning); likaviktning SE1–SE4 vs konsumtions-
viktning — likaviktat valt). v0 → v1 vid expertgranskning.

### ✅ 2026-06-12 (kväll) — Spår D ekonomi: `realloner` byggd, SCB-väggen gällde fel instans (v0, FLAGGAD)

**1 bygge, 1 ny D-serie; coverage 39/67 → 40/67 inlästa; undermått oförändrat 28/35** (realloner_hushall
hade redan hushallens_reala_disponibla_inkomst — detta är djup, inte bredd: 2:a serien + 66 konsekutiva år).

1. **`realloner`** (ekonomi → realloner_hushall, upp): reala löner i hela ekonomin som **index
   (1995=100)**, nominell lön deflaterad med **KPI** — **Medlingsinstitutet** (statlig myndighet,
   statistikansvarig för den officiella lönestatistiken; tabellunderlag MI/SCB/KI), **MI:s EGEN
   PxWeb-instans**, tabell `Konjunkturlönestatistik/Reallöneutveckling/Realloner_arsdata.px`
   (PxWeb v1, samma dialekt som Domstolsverket/Energimyndigheten: POST json-query → json-stat2,
   årtal ur tidsdimensionens category.label; URL-encodade svenska tecken i tabellvägen, BOM-tolerant
   avkodning utf-8-sig). 66 obs 1960–2025 (1960: 59,3 → 1995: 100 → 2021: 169,7 → 2023: 153,7 →
   2025: 160,1; 2025 preliminär tills KLS definitiv). **Korrigering av tidigare antagande:**
   allowlist-väggen (`future`, sonderat 2026-05-31) gällde **SCB:s API** (ingen ren helekonomi-
   löneserie där — sant) — **MI:s egen PxWeb var förbisedd**. **MÅTTVAL (dokumenterat i adaptern):**
   (a) **Reallön (KPI)** = MI:s huvudserie; KPI inkluderar räntekostnader → djupare 2022–23-fall än
   KPIF (2023: −4,9 % mot −2,3 %) men D tar bara TECKNET, som är identiskt för båda deflatorerna —
   explicit motiverat val, inte tyst; (b) indexserien (inte %-serien) eftersom D själv bildar
   år-för-år-tecken ur nivån; (c) **medveten dubbelbreddning**: submåttet hade redan D via
   hushallens_reala_disponibla_inkomst och serierna är korrelerade (löner = största inkomstkällan) —
   djup, inte bredd. Ny `medlingsinstitutet`-adapter (`pipeline/sources/medlingsinstitutet.py`) +
   källpost i sources.yaml.

**Verifiering:** live-extraktion 2026-06-12 matchar publicerade värden exakt (index: 2020=168,9,
2021=169,7, 2022=161,0, 2023=153,7, 2024=155,5, 2025=160,1; årlig % KPI: 2022=−5,6, 2023=−4,9,
2024=+1,2, 2025=+2,9). Drift-skydd: ankare 1995=100,0 + 2024=155,5, min_points 60, range [20,250],
min_latest_year 2025. Serien börjar 1960 — `period_to_year`/årsserielogiken hanterar det (samma
mönster som hushallens 1951-start); D-attributionen använder ändå bara fönstret med maktdata.
Oberoende attributionssanity (lag 1 år): 2021→2022 169,7→161,0 fall → år 2021 = S/MP (+C/L stöd
0,5 t.o.m. nov) ✓; 2022→2023 161,0→153,7 fall → år 2022 = S-majoritet + M/KD/L+SD-del (Tidö fr.
18 okt) ✓; 2024→2025 155,5→160,1 ökning → år 2024 = M/KD/L + SD ✓ — alla tre tecken bekräftade mot
scorerun-utfallet. Golden-test (`tests/test_source_medlingsinstitutet.py`, pinnade indexvärden +
årtal-ej-koder + hård-fail-dimensionsgrind + radform); registrerad i `test_fas3_gate._ingested()`;
hela offline-sviten grön (249 passed, 4 skipped); coverage-gaten håller (`coverage_report`:
realloner ✓A, 66 obs 1960..2025, SUMMA 40/67).

**Betygseffekt (score_diff):** endast **ekonomi**-celler rör sig, och serien DIFFERENTIERAR
(reallönefallet 2022–23 attribueras åren 2021–2022 = S-styre+stöd; uppgången 2024–25 = Tidö):
C −0,010 · MP −0,008 · S −0,007 · L −0,004 · M ±0,000 · KD ±0,000 · SD ±0,000 · V ±0,000
(Tidö-parternas 2022-delfall nettas av 2023/2024-uppgångarna; L bär dessutom stödåren 2019–2021;
V orörd, D_not_applicable). Totaler: C −0,002 · MP −0,002 · S −0,001, övriga ±0. **Ranking
OFÖRÄNDRAD** (S>L>M>KD>MP>C>SD>V). `dist/` omräknat + snapshot re-baselinad.

**Flaggor/version:** v0 (FLAGGAD — kräver mänsklig granskning; måttvals-caveats ovan: KPI-vs-KPIF-
deflatorval, preliminärt 2025, korrelerad dubbelbreddning inom undermåttet). v0 → v1 vid expertgranskning.

### ✅ 2026-06-12 (kväll) — Spår D trygghet: `handlaggningstid` byggd, trygghet-väggen var fel led (v0, FLAGGAD)

**1 bygge, 1 ny D-serie; coverage 38/67 → 39/67 inlästa; undermått oförändrat 28/35** (rattsvasendets_
effektivitet hade redan uppklaringsgrad — detta är djup, inte bredd: 2:a serien + 19 konsekutiva år).

1. **`handlaggningstid`** (trygghet → rattsvasendets_effektivitet, ned): handläggningstid vid tingsrätt,
   **75:e percentilen i månader**, **brottmål exkl. förtursmål**, alla tingsrätter — **Domstolsverket,
   Officiell domstolsstatistik (SOS), statistikdatabasen DOMstat**, tabell `01_Verksamhetsmal_TR.px`
   (PxWeb v1, samma dialekt som Energimyndigheten: POST json-query → json-stat2, årtal ur tids-
   dimensionens category.label). 19 obs 2007–2025 = 5,3/5,0/4,9/4,7/4,9/4,6/4,6/4,5/4,3/4,1/4,0/4,0/
   3,9/4,0/4,2/3,9/3,5/3,1/3,0. **Korrigering av tidigare antagande:** allowlist-väggen (`future`,
   sonderat 2026-06-03) gällde **Brå/Åklagarmyndighetens** genomströmningstider (interaktiv DB/PDF) —
   **domstolsledet var förbisett**; Domstolsverkets DOMstat bär en ren maskinläsbar SOS-årsserie.
   **MÅTTVAL (dokumenterat i adaptern):** (a) 75-percentilen = regeringens/Domstolsverkets eget
   verksamhetsmålsmått (mål 5 mån), robust mot extremmål; (b) exkl. förtursmål (häktade/15–17-åringar)
   → snabbspårsreformer som flyttar mål till förtur biasar det KVARVARANDE måttet UPPÅT — en icke-
   smickrande bias, inte en som belönar sittande regering; (c) serien mäter DOMSTOLSLEDET — uppströms
   polis-/åklagartid fångas delvis av syskonindikatorn uppklaringsgrad i samma submått. Ny
   `domstolsverket`-adapter (`pipeline/sources/domstolsverket.py`) + källpost i sources.yaml.

**Verifiering:** live-extraktion 2026-06-12 matchar publicerade värden exakt för alla 19 år (ankare
2024=3,1 i drift-skyddet, expectations min_points 19 / range [2,8] / min_latest_year 2025). Oberoende
attributionssanity (lag 1 år): 2021→2022 4,2→3,9 förbättring → år 2021 = S ≈1,0/MP ≈0,92/C+L ≈0,46 ✓;
2023→2024 3,5→3,1 förbättring → år 2023 = M/KD/L 1,0 + SD 0,5 (Tidö) ✓; 2019→2020 3,9→4,0 försämring →
år 2019 = S/MP (+C/L stöd) ✓. Serien föll mest under BÅDA regeringstyperna. Golden-test
(`tests/test_source_domstolsverket.py`, pinnade percentiler + årtal-ej-koder + hård-fail-dimensionsgrind
+ radform); modulen registrerad i `test_fas3_gate._ingested()`; hela offline-sviten grön (244 passed,
4 skipped); coverage-gaten håller (`coverage_report`: handlaggningstid ✓A, 19 obs 2007..2025).

**Betygseffekt (score_diff):** endast **trygghet**-celler rör sig, alla svagt UPP (förbättringsåren
dominerar för båda blocken): S +0,009 · SD +0,005 · KD +0,004 · M +0,004 · L +0,003 · MP +0,003 ·
C ±0,000 (stödåren 2019–2021 nettar ~0). Totaler ≤0,001 (endast S +0,001). **Ranking OFÖRÄNDRAD**
(S>L>M>KD>MP>C>SD>V). V orörd (D_not_applicable). `dist/` omräknat + snapshot re-baselinad.

**Flaggor/version:** v0 (FLAGGAD — kräver mänsklig granskning; måttvals-caveats ovan: percentilval,
förtursmåls-exklusion, domstolsledet). v0 → v1 vid expertgranskning.

### ✅ 2026-06-12 — Spår D försvar: +2 D-serier → försvar 3/5 undermått, 4 D-indikatorer (v0, FLAGGADE)

Din beställning: brett källsvep (inkl. internationella källor) efter fler försvars-D; "1 till bra, 2 till
fantastiskt, även tunna/osäkra OK". Fyra parallella källsondrings-agenter (FM ÅR / MSB-MPF / internationellt /
lateralt Kolada-SCB-FMV). **2 byggen, 2 nya D-serier; coverage 36/65 → 38/67 inlästa; 27/35 → 28/35 undermått;
försvar 2/5 → 3/5 undermått, 2 → 4 D-indikatorer.**

1. **`forsvarsvilja`** (försvar → civil_beredskap, upp): andel som anser att Sverige bör göra väpnat motstånd
   även om utgången är oviss, **MPF/MSB Opinioner** (psykologiskt försvar = del av totalförsvaret). **Öppnade
   civil_beredskap** (var allowlistat `qualitative`). 2014–2025 (lucka 2019, ingen mätning): 75/75/72/71/72/–/
   70/70/78/79/79/75 %. **Utanför-boxen-vinsten:** den gamla väggen kom av att man läste MSB:s *årsredovisning*
   (pengar/anslag); utfallsserien finns i stället i *Opinioner*-undersökningen. Verifierad direkt ur MPF
   Opinioner 2025 s.87 (andel JA = ja_absolut+ja_kanske). Hammare-test: befolkningens faktiska vilja
   (tillstånd/resiliens), ej anslag. ⚠ CAVEAT (v0): hoppet 2021→2022 invasionsdrivet → D tar bara tecknet.
   Ny `mpf`-adapter + config/forsvarsvilja.yaml. Samma tillstånds-logik som löste demokrati-väggen med V-Dem.
2. **`personalstyrka_kontinuerligt`** (försvar → militar_formaga, upp): antal kontinuerligt tjänstgörande i FM
   (yrkesoff. + GSS/K + civila), **FM ÅR bilaga Tabell 1**. Andra D-serien i militar_formaga (utöver
   värnpliktiga). 2019–2024 = 22751/24094/24353/25011/26195/27734 (**strikt monoton**, alla tecken +).
   Verifierad ur FM ÅR 2021+2022+2024 bilagor (korsbekräftad; 2021 = rättat +720-värde). Hammare-test:
   bemannad numerär (förmågeutfall), ej pengar. Transkriberad config + utökad `forsvarsmakten`-adapter.

**Internationellt svep (testat, blev väggar — ärliga nej):** SIPRI vapenimport-TIV (materiel_formaga) — källan
**tillåten** (Stockholm/V-Dem-logiken, kringgår sekretess) men **årssignalen är brus** (enstaka storleveranser,
net −3 under upprustningsåren) → vägg. SIPRI milex %BNP + NATO utrustningsandel = **pengar** → hammare/A-dubbel-
räkning, bekräftar ert HOLD. Lateralt: Kolada/FMV = pengar/platt; Pliktverket inskrivna = policy/regleringsbrev
(insats). **Blockeraren är måttens natur (sekretess/pengar/brus), ej datatillgång.** Kvar D-tomma: ekonomisk_
ambition + genomforbarhet_leverans (pengar-väggar).

**Verifiering:** försvarsvilja direkt ur MPF Opinioner 2025-PDF (s.87); personalstyrka ur FM ÅR-bilagornas
Tabell 1 (pdfplumber, korsbekräftad över bilagor). Golden-test för mpf-adaptern + personalstyrka (pinnade
värden, monotoni, lucka-2019, radform); hela offline-sviten grön (228 passed, 4 skipped); coverage-gaten håller.

**Betygseffekt (score_diff):** endast **försvar** rörd (≤0,10/kategori), totaler ≤0,015. Försvars-D rebalanserades
från uppblåst (bara stigande militar_formaga+ukraina) till ärlig blandbild: den invasionsdrivna försvarsvilje-
toppen 2021→2022 landar på S (regering 2021); Tidö (M/KD/SD −0,10) får den flacka/sjunkande senaste försvarsvilje-
trenden men behåller stigande personalstyrka. **Ranking OFÖRÄNDRAD** (S>L>M>KD>MP>C>SD>V). V orörd
(D_not_applicable). `dist/` omräknat + snapshot re-baselinad.

**Flaggor/version:** båda v0 (försvarsvilja survey + invasions-caveat; personalstyrka monoton men militar_formaga-
djup). v0 → v1 vid expertgranskning.

### ✅ 2026-06-12 — Spår D integration: +2 D-serier → integration 5/5 undermått (v0, FLAGGADE)

Din beställning: bygg BÅDE asyl-handläggningstid och SCB:s medborgarundersökning (tunt 1-av-5-mått OK).
**2 byggen, 2 nya D-serier; coverage 34/63 → 36/65 inlästa; 25/35 → 27/35 undermått med D; integration
3/5 → 5/5 undermått (alla undermått D-täckta).**

1. **`mellanmansklig_tillit`** (integration → normer_tillit, upp): andel som svarar att man i allmänhet
   kan lita på människor, **SCB:s medborgarundersökning** via **Kolada N00666**, 2021–2025 (5 obs,
   62,9/62,6/61,2/62,9/62,8 %). **Öppnade normer_tillit** (var allowlistat `no_api/sparse`). **Korrigering
   av antagande:** den uppenbara kandidaten N00665 visade sig vara "förtroende för riksdagens politiker"
   (fel konstrukt + överlappar demokratis institutionstillit) — N00666 är den *mellanmänskliga* tillits-
   frågan (rätt fit för social sammanhållning). Ren Kolada-väg (`build_fas2`). ⚠ Nästan platt → D≈neutral;
   tunt 5-årsunderlag (sign-off). Ny kanonisk indikator (D-only; `tillit_valdeltagande` bär B-spåret).
2. **`asyl_handlaggningstid`** (integration → migrationssystem, ned): genomsnittlig handläggningstid (dagar)
   för avgjorda **förstagångsärenden om asyl**, **Migrationsverket "Avgjorda asylärenden"** (deltabellen
   **Asyl**, EXKL. massflyktsdirektivet/ukrainska medborgare — near-automatisk EU-process, ej svensk
   handläggningseffektivitet). 2021–2025 = **257/166/198/187/180** dgr. **Öppnade migrationssystem** (var
   allowlistat `B-only`). **Korrigering:** svepets 257/166/**194/162/178** var fel cut — verifierade tal
   hämtade direkt ur per-årsfilernas xlsx (`tools/asyl_handlaggningstid_verify.py` korsverifierar Asyl-
   tabellens Totalt-rad). Transkriberad config (källrad/år) + ny `migrationsverket`-adapter. Genuin
   teckenväxling (förbättring 2021→22, försämring 2022→23, förbättringar 2023→25). v0.

**Neutralitet (din fråga om asyl):** kortare asylhandläggning är ett av få migrationsmått där båda poler
är överens (sökande slipper limbo + lägre systemkostnad) — till skillnad från återvändandeärenden
(värdeladdat, avstått). Kvarvarande caveat (v0): kvalitet-vs-hastighet + inflödesvolym-beroende → D tar
bara TECKEN, väger 10 %.

**Verifiering:** N00666 live via Kolada-adaptern; asyl direkt ur Migrationsverkets per-års-xlsx (openpyxl,
Asyl-deltabellens Totalt-rad, massflykt exkluderad). Golden-test för migrationsverket-adaptern (pinnade
årsvärden + teckenväxling + radform); hela offline-sviten grön (217 passed, 4 skipped); coverage-gaten håller.

**Betygseffekt (score_diff):** endast **integration** rörd (≤0,026/kategori), totaler ≤0,003. S/integration
−0,013 (höll regeringen 2021 när tilliten började falla; får kredit för asyl-förbättringen 2021→22);
MP/C/L +0,02–0,03 (JÖK-eran, 2021-asylförbättringen); Tidö marginellt upp. **Ranking OFÖRÄNDRAD**
(S>L>M>KD>MP>C>SD>V). V orörd (D_not_applicable). `dist/` omräknat + snapshot re-baselinad.

**Flaggor/version:** båda v0 (tillit nästan platt + tunt; asyl kvalitet-vs-hastighet). v0 → v1 vid expert-
granskning. Reproducerbart revisionsspår: `tools/asyl_handlaggningstid_verify.py`.

### ✅ 2026-06-09 — Spår D byggkö (färsk session): +6 D-serier, demokrati-väggen löst (v0, FLAGGADE)

Djupsvepets sign-off-byggkö exekverad (medskick: försvar % BNP nedgraderat till HOLD, V-Dem uppgraderat
till aktiv). **3 byggen, 6 nya D-serier; coverage 28/58 → 34/63 inlästa; 25/35 undermått har D.**
Commits `69eda42` (återfall) · `014146c` (fåglar) · `30f2edb` (V-Dem) · `e0408b7` (dist) · `8c05477` (docs).

1. **`aterfall_i_brott`** (trygghet → aterfall_kriminalvard, ned): andel klienter som återfaller i brott
   inom 3 år, **Kriminalvården KOS 2025 Tabell 6.1** (ingångsår 1994–2022, 29 obs). **Öppnade
   aterfall_kriminalvard** (var allowlistat `blocked:PDF`). **Korrigering av tidigare antagande:** ingen
   separat Excel-tabellbilaga behövdes — Tabell 6.1 i huvud-PDF:en bär RÅTALEN (antal klienter + återfall),
   extraherbara med pdfplumber. Lagrar råtal → loadern beräknar andelen (decimal), eftersom den publicerade
   heltalsandelen annars gör varje 1 pp-avrundningssteg till ett falskt tecken i platån 2012–2022 (dödzon
   0,5 %). Loadern korsverifierar mot publicerad andel (hård fail >0,6 pp). Verifierad direkt mot KOS-PDF:en.
2. **`hackande_faglar_skog`** (klimat → biologisk_mangfald, upp): samlat skogsfågelindex (16 arter, basår
   2002=100), **Svensk Fågeltaxering, Lunds universitet** (akademisk svensk källa), officiell miljömåls-
   indikator via sverigesmiljomal.se. **NY kanonisk indikator → öppnade biologisk_mangfald** (hotade_arter
   förblir no_api). Highcharts-JSON i sid-HTML:en → ny HTML-avläsare `pipeline/tools/faglar_transcribe.py`
   (verifierade alla 23 år mot live-sidan); pipelinen läser transkriberad config. ⚠ **BRUS-CAVEAT:** trendlös/
   brusig serie → D (tecken, 10 %, makt-/ansvarsviktat) bidrar netto ≈ neutralt. Skogsindexet (neutralt) valt
   framför jordbruksindexet (CAP-laddat).
3. **V-Dem ×4** (demokrati, alla upp): fyra index ur **V-Dem v16** (Sverige 2000–2025, 26 obs/index) →
   **öppnade ALLA 4 kvarvarande D-tomma demokrati-submått → demokrati-väggen löst på D-sidan (1/5 → 5/5).**
   `rattsstatsindex` (`v2x_rule`, nära platt → D≈neutral) · `yttrandefrihetsindex` (`v2x_freexp_altinf`,
   nedgång 2018+2023) · `privata_friheter` (`v2x_clpriv`) · `horisontellt_ansvarsutkravande` (`v2x_horacc_osp`
   — valt framför diagonal accountability för att ej dubbelräkna medie-signalen). Avstod `v2x_corr` (ingen
   varians för Sverige; korruption_tillit har redan Brå-NTU-D).

**Källregel — V-Dem (din sign-off 2026-06-09, fält "Svensk akademisk D-källa"):** V-Dem-institutet är värdat
vid **Göteborgs universitet → svensk akademisk källa** (CLAUDE.md tillåter när officiell statistik saknas) +
ny intl-neutralitetsklausul (commit 7fa9337: extern bedömare neutralare än statens självvärdering). V-Dem är
ett TILLSTÅNDS-mått → klarar din hammare-princip (effekt, ej aktivitet). ⚠ **Största caveat (v0):** V-Dem är
EXPERT-KODAT (subjektiva bedömningar, Bayesiansk IRT), ej hård räkning → mildras av tecken-only + 10 % vikt +
takeffekt (Sverige 0,94–0,995 → bara trend meningsfull).

**Verifiering:** KOS direkt mot PDF; fåglar mot live-Highcharts (tools/faglar_transcribe); V-Dem läst direkt
ur officiella v16-datasetet (pyreadr) + korsverifierat mot OWID (3 av 4 index) + auditerat via
tools/vdem_transcribe (alla 4×26 år). Hela offline-sviten grön; coverage-gaten håller.

**Betygseffekt (score_diff):** alla totaler rör sig ≤0,018, **ranking OFÖRÄNDRAD** (S>L>M>KD>MP>C>SD>V).
Demokrati-D rebalanserades från uppblåst (~3,9–4,5, en enda stigande indikator) till ärlig blandbild
(~2,6–2,9; yttrandefrihet/privata friheter sjönk 2015–2024). Klimat-fågelbruset drog mot neutralt som väntat;
återfalls-platån mest i dödzonen. `V` orörd (D_not_applicable — styrde aldrig nationellt). `dist/` omräknat +
snapshot re-baselinad.

**Flaggor/version:** alla v0 (KOS platå-signalsvaghet; fågel-brus; V-Dem expert-kodning). v0 → v1 vid expert-
granskning. Reproducerbara avläsar-/auditverktyg: `faglar_transcribe.py`, `vdem_transcribe.py`,
`kriminalvarden` korsverifiering i loadern.

### ✅ 2026-06-09 — Spår D djupsvep: 90 kandidater testade, +2 D-serier (v0, FLAGGADE)

Fullt djuptest av **5 kandidater per D-tomt undermått (18 × 5 = 90)**, varje kandidat hämtad mot källan.
Full logg: [spar_D_svep_2026-06-08.md](done/spar_D_svep_2026-06-08.md). Byggt (rena/neutrala/officiella/riktningsklara):

1. **`brukarnojdhet_hemtjanst`** (välfärd → omsorg_personal, up): Kolada U21468 brukarbedömning hemtjänst
   helhet, 2013-2025. **Öppnar omsorg_personal (D-tomt).** Ny kanonisk indikator (D-only). Commit `1cd6f56`.
2. **`utslappsintensitet`** (klimat → kostnadseffektivitet, down): härledd ratio territoriella utsläpp
   (TAB4698) ÷ BNP (TAB3610 BNPM), 1990-2024. **Öppnar kostnadseffektivitet (D-tomt).** Commit `1cd6f56`.

**Lärdom:** "saknad data" var sällan sant — för target-submått + demokrati FINNS rena 20-30-årsserier; blockeraren
är **riktning/neutralitet/attribution**, ej tillgänglighet (validerar target-design + coverage-krympning). Två
"byggbara" visade sig figur-låsta (KOS-återfall, migration öppna-ärenden — diagram ej tabell). Demokrati = äkta
vägg (20/20 tvetydiga). **Öppna sign-off-byggen** (data verifierad, väntar riktnings-/neutralitetsbeslut): försvar
% BNP (ekonomisk_ambition), klimat fågelindex/skyddad natur (biologisk_mangfald), KOS-återfall via tabellbilaga,
m.fl. — se svep-rapporten §4.

### ✅ 2026-06-08 — Spår D natt: +2 D-serier + PDF-verifiering (v0, FLAGGADE)

Full försökslogg (alla försök, lyckade + misslyckade, 5 parallella källsondering-agenter):
[spar_D_nattrapport_2026-06-08.md](done/spar_D_nattrapport_2026-06-08.md). Sammanfattning:

1. **`overlevnad_svar_sjukdom`** (välfärd → vard_tillganglighet, up): Kolada **U70471** 30-dagarsöverlevnad
   tjocktarmscancer, 16 obs 2010-2025. **Välfärd 3→4 D-indikatorer.** Löser §5.3 (kvinkennial-problemet).
   Betygseffekt: endast valfard, ranking oförändrad. Commit `65a5eda`.
2. **`ukraina_stod`** (försvar → nato_ukraina, up): Regeringens militära stöd/år, 4 obs 2022-2025 (6,1→40
   mdr). **Öppnade nato_ukraina → försvar 1→2 D, två olika submått.** Ny `regeringen`-adapter. Commit `05dc3b3`.
3. **`personal_varnpliktiga` PDF-verifierad** → v1-redo: FM ÅR-PDF:erna nu maskinläsbara (pdfplumber); 2020
   4917→4915, 2024 →7343; inga D-tecken ändrade. Commits `23b9215`, `7e1bf58`.

**Verktygsfynd:** "officiell PDF = oläsbar" var överspelat (pdfplumber/PyMuPDF/pdftotext finns) → FM ÅR + MSB
ÅR lästa direkt. **Omprövade väggar:** civil_beredskap (MSB ÅR PDF-läst = bara pengar/anslag → vägg
bekräftad); demokrati (mediefrihet vägg, korruption/transparens riktnings-tvetydiga → funderare);
elprisvolatilitet (byggbar via SCB EN0301 men kräver ny klassisk-PxWeb-adapter + §5.4-sign-off).
**Öppna sign-off-frågor:** se nattrapporten §3 (försvar 3:e D, klimat 4:e, höftfraktur/omsorg, demokrati, v1-bump).

### ✅ 2026-06-07 — Tier 1: ekonomi-D till full submåttstäckning (v0, FLAGGAD, väntar sign-off)

**Två D-serier byggda → ekonomi 2 → 4 D-täckta submått (alla 4 D-bara täckta):**

1. **`naringslivets_investeringar`** (ekonomi → foretagande_investeringar, riktning up): näringslivets
   FASTA bruttoinvesteringar i FASTA priser (volym), SCB NR **TAB3610** Anvandningstyp=`BNAR`,
   ContentsCode=`000000RN`. Samma tabellfamilj som produktivitetens BNP-täljare → ren `SCB_SERIES`-post
   (`build_fas2`). Inläst 1980–2024 (45 obs). `expect`-ankare 2020=972 986 mnkr (live-verifierad).
2. **`hushallens_reala_disponibla_inkomst`** (ekonomi → realloner_hushall, riktning up): kumulativt
   **realindex** ur SCB:s officiella reala tillväxttakt (NR **TAB4592** `B6nRealGrowth`/`S14`), ny
   `derived.py`-op `index`. Inläst 1951–2025 (75 obs). Drift-skydd på föräldra-tillväxtserien
   (ankare real 2023≈−1,1 / 2021=4,3, rel_tol 0,3 → skiljer real från nominell).

**Verifiering:** live-hämtade dimensionskoder (ej gissade); `expect`-grindar passerade i bygget;
golden-test för `compute_index` + enkel-operand-vägen (`tests/test_derived.py`); **adversariell
teckenkontroll** av attributionen — investeringsnedgången 2023–2024 bärs av Tidö-partierna
(M/SD/KD net −1,00), JÖK-erans tillväxt av C (+1,00)/S/MP; real-inkomstfallet 2023 fördelas
principiellt (M får delår-2022-vikt 0,21 + full 2024–2025-återhämtning = +0,81). Hela testsviten
grön, ruff rent, 0 främmande tecken.

**Betygseffekt (score_diff):** endast **ekonomi** rörd; alla 7 ansvarspartier +0,007…+0,074;
V/ekonomi oförändrad (NA, korrekt). **Ranking OFÖRÄNDRAD:** S > L > M > KD > MP > C > SD > V.

**Flaggor/version:** v0 (konjunkturkänsliga serier; D tar bara tecken, väger 10 %). `dist/` omräknat +
coverage-strängen rättad (trygghet felaktigt listad som D-tom → nu korrekt 5 kategorier). **`dist/`-
snapshot re-baselinad + committad 2026-06-07** (`data:`-commit). v0 kvarstår tills en formell
granskning bumpar v0→v1 (jfr B1-expertgranskningen).

### ✅ 2026-06-07 — Tier 2: `sfi_sprakkunskaper` → integration får sin första skola_sprak-D (v0, FLAGGAD)

**En D-serie byggd → integration 2 → 3 D-täckta submått (skola_sprak öppnat):**

1. **`sfi_sprakkunskaper`** (integration → skola_sprak, riktning up): andel personer **godkända i sfi**
   (procent), SCB:s officiella sfi-statistik **TAB1814**, ContentsCode `AA0003EB` (Skolverket
   statistikansvarig, SCB producent). Inläst **1997–2023** (27 obs). Visade sig vara **S, inte M**:
   SCB exponerar serien som ren PxWeb v2 → befintliga `scb.py`-adaptern räckte, ingen Skolverket-
   portaladapter. `expect`-ankare 2020=32,3 / 2004=46,4 (live-verifierade). Ur allowlisten.

**Semantik (§5.2 avgjord av datan):** TAB1814 har båda §5.2-måtten som var sin ContentsCode —
godkäntandel (`AA0003EB`, up) och vistelsetid-median för godkända (`AA0003EC`, down = progressionen).
Bara godkäntandel matchar indikatorns kanoniska riktning (up) → enda direktionskonsistenta valet utan
att omdefiniera indikatorn.

**Metodbrott 2022** (SCB-not: kursbetyg G/I/– + sista kursdag 1 jan fr.o.m. 2022): hela serien
behålls. Skäl: de två brott-närliggande övergångarna (2021→2022 = −, 2022→2023 = +) är teckenkonsistenta
med den genuina nedgång-/stabiliseringstrenden, och D tar bara **tecken** (ej magnitud) → brottet
ändrar magnituden men inte tecknet. Till skillnad från NTU (där SCB delade serien, ojämförbara nivåer →
fönstrades) publicerar SCB här EN obruten serie 1997–2023.

**Verifiering:** live-hämtade dimensionskoder (Region/Kon/Bakgrund/ContentsCode fixerade, ej gissade);
`expect`-grind passerad i bygget; **adversariell teckenkontroll** av attributionen — sfi-godkäntandelen
föll stadigt 2015→2020 (39,7→32,3) under S+MP-regeringarna (post-2015 immigrationsvåg) → S net −0,49 /
MP −0,65 (genuint negativt integrationsutfall på deras vakt); JÖK-stödpartierna C −0,30 / L −0,14 delar
sent-nedgångsfönstret; Tidö-partierna M/KD net +1,0 men **tunt** underlag (basis 0,10–0,21, bara
2022→2023-återhämtningen via delår-2022) → ej överkrediterade; V = NA (aldrig regering). Brottövergången
flippar ingen partis tecken. Hela testsviten grön (≈170 passed, 4 skipped).

**Betygseffekt (score_diff):** endast **integration** rörd. S/integration −0,060, MP −0,079, C −0,052,
L −0,032 (sfi-nedgången sänker JÖK-erans integration-D); M/KD/SD +0,067 (liten, tunn återhämtningskredit);
V oförändrad (NA). TOTAL-rörelser ±0,004…0,008. **Ranking OFÖRÄNDRAD:** S > L > M > KD > MP > C > SD > V.

**Flaggor/version:** v0 (sign-only D, väger 10 %; metodbrott 2022 dokumenterat). `dist/` omräknat. v0
kvarstår tills en formell granskning bumpar v0→v1.

### ✅ 2026-06-07 — Tier 4: `personal_varnpliktiga` → FÖRSVARET FÅR SIN FÖRSTA D (v0, FLAGGAD)

**En D-serie byggd → forsvar 0 → 1 D-täckt submått (militar_formaga öppnat); kategorin var tidigare
strukturellt D-tom. 6/7 kategorier har nu D (bara demokrati kvar).**

1. **`personal_varnpliktiga`** (forsvar → militar_formaga, riktning up): antal värnpliktiga som
   **påbörjade grundutbildning** per kalenderår, **Försvarsmaktens årsredovisning**. Inläst **2018–2025**
   (8 obs, 3 750→8 136). Transkriberad config (`config/personal_varnpliktiga.yaml`) — FM:s/Pliktverkets
   ÅR-PDF:er är FlateDecode och ej maskinläsbara av verktygskedjan, så samma trogna transkriberings-
   mönster som skjutningar/budget_ramar; auditerbar via `pipeline/tools/varnpliktiga_audit.py`. Ny
   sektorsadapter `pipeline/sources/forsvarsmakten.py`, wirad i `build_fas3` (full-replace,
   `forsvarsmakten:`-source_ref utanför scb/kolada-purge-scope). Ur allowlisten.

**Designbeslut "varför inte båda" (din sign-off 2026-06-07):** två officiella myndighetsmått fanns —
FM "påbörjade GU" (kalenderårsrent) och Plikt- och prövningsverkets "inskrivna till GU" (utbildningsårs-
etiketterat, mappar EJ entydigt mot kalenderår). Till skillnad från sfi (§5.2, där datan eliminerade
valet) divergerar de inte i sak — de **korsverifierar samma uppbyggnad**. Lösning: **FM = värdebärande
serie** (förmågemyndighet, kalenderårsrent), **Pliktverket = oberoende korsverifiering** varje år
(≤~3 % skillnad de år båda finns). Avgörande: BÅDA visar samma **enda nedgång 2021→2022** — den enda
teckenkänsliga D-övergången är dubbelbekräftad.

**Attribution (matchar oberoende handberäkning exakt):** värnpliktsuppbyggnaden 2018→2025 (3 750→8 136)
skedde under både S-ledda och Tidö-regeringar → alla ansvarspartier får POSITIV försvars-D (genuint
positivt utfall på allas vakt). S net +0,58 (D 3,96, basis 4,79 stark) / MP +0,53 (3,83) — bär 2018–2021-
rampen, dinged av 2022-dippen som landar på dem; L +0,75 (4,37, JÖK-stöd + Tidö-regering); M/KD/SD
net +1,0 (D 5,0, Tidö-eran 2022→2025 alla upp); C +0,36 (3,40, JÖK-stöd). **V = NA** (aldrig regering i
fönstret — korrekt, ingen försvars-D att attribuera). Inga D_thin_basis-flaggor (alla basis > 1,0).

**Källgräns (v0, transparent):** 2018 + 2025 direkt bekräftade ur FM ÅR (ordagranna meningar);
2019/2021/2022/2024 korsverifierade mot Pliktverkets direkt-lästa pressmeddelanden; 2020 + 2023 (inre
monotona punkter — påverkar inget D-tecken) lokaliserade via Wikipedias FM-ÅR-citerade tabell "Volymer
inryckta". v0 kvarstår tills exakta siffror transkriberats direkt ur FM-ÅR-PDF:erna (→v1).

**Verifiering:** integritets-audit grön (konsekutiva 2018–2025, monoton upp utom dubbelbekräftad
2021→2022-dipp, Pliktverket-korsverifiering inom tolerans); golden-test (`tests/test_source_forsvarsmakten.py`,
8 nya) inkl. att auditen fångar en odokumenterad nedgång; fas3-gaten håller; hela sviten grön.

**Betygseffekt (score_diff):** endast **forsvar** rörd. Alla 7 ansvarspartier: forsvar D
not_applicable→uppmätt, kategori +0,090…+0,250 (KD/M/SD +0,250, L +0,187, S +0,146, MP +0,133, C +0,090);
V oförändrad (NA). TOTAL +0,014…+0,038. **Ranking OFÖRÄNDRAD:** S > L > M > KD > MP > C > SD > V. `dist/`
omräknat + snapshot re-baselinad. v0 kvarstår tills formell granskning bumpar v0→v1.

### ✅ 2026-06-07 — Tier 4: `fortroende_domstolar_myndigheter` → DEMOKRATIN FÅR SIN FÖRSTA D (v0, FLAGGAD)

**En D-serie byggd → demokrati 0 → 1 D-täckt submått (korruption_tillit öppnat). ALLA 7 kategorier har
nu D — den sista strukturella nollan fylld; exit-kriterium §6.2 uppfyllt.**

1. **`fortroende_domstolar_myndigheter`** (demokrati → korruption_tillit, riktning up): andel med
   **ganska/mycket stort förtroende för rättsväsendet som helhet** (domstolar + polis/åklagare/
   kriminalvård), **Brå NTU blad 5A:1** "Samtliga 16-84 år". Inläst **2017–2025** (9 obs, 44,1→54,0 %).

**Källval — S, inte L (samma mönster som sfi):** trackern antog SOM-institutet (akademiskt → L-
transkribering). Men **Brå NTU — en officiell källa (SOS)** — mäter förtroende för rättsväsendet som
en ren xlsx-tabell, läst av den BEFINTLIGA `bra.fetch_ntu`-adaptern (samma som brottsutsatthet/
upplevd_otrygghet). Dessutom: CLAUDE.md tillåter akademiska källor **bara när officiell statistik
saknas** — vilket den inte gör här → SOM hade varit otillåtet. Adaptern generaliserades så NTU-serier
bär egen kategori/submått (`bra.INDICATOR_CATEGORY`; de flesta är trygghet, denna demokrati).

**Scope-val (5A:1 rättsväsendet som helhet):** indikatornamnet "domstolar_*myndigheter*" → den trognaste
matchningen är aggregatet rättsväsendet som helhet (domstolar + rättsvårdande myndigheter), inte en
enskild institution. **Icke-konsekvent val:** blad 5D:1 (domstolarna specifikt) ger samma kvalitativa
D (stigande utom dipp 2022→2023), så valet 5A:1 vs 5D:1 ändrar inte attributionen — 5D:1 dokumenteras
som korsverifiering ("varför inte båda"-andan).

**2017-fönster (NTU-metodbrott):** åren 2007*–2016* är asteriskmärkta (NTU 2017-omläggning), exakt
samma metodbrott som upplevd_otrygghet redan hanterar → `min_year=2017` (nuvarande metod, 9 år).

**Verifiering (attribution matchar oberoende handberäkning exakt):** förtroendet för rättsväsendet steg
44→54 % 2017→2025 under både S-ledda och Tidö-regeringar → alla ansvarspartier positiv demokrati-D.
MP +0,80 (D 4,49 — högst; regering 2017–2021-uppgången, lämnade före 2022→2023-dippen); SD/M/KD +0,81
(4,53, Tidö-eran); L +0,76 (4,39); C +0,67 (4,17); S +0,55 (3,88, bär längsta fönstret + 2022→2023-
dippen via 0,79-vikt). **V = NA** (aldrig regering). Inga D_thin_basis (alla basis > 1,0). Generaliserad
adapter golden-testad (NTU-fixtur fick blad 5A:1; ny kategori-mappnings-test); fas3-gaten håller; sviten grön.

**Betygseffekt (score_diff):** endast **demokrati** rörd. Alla 7 ansvarspartier: demokrati D
not_applicable→uppmätt, kategori +0,139…+0,203; V oförändrad (NA). TOTAL +0,010…+0,015. **Ranking
OFÖRÄNDRAD:** S > L > M > KD > MP > C > SD > V. `dist/` omräknat + snapshot re-baselinad. v0 (survey-mått,
sign-only D, väger 10 %). coverage-strängen: D nu aktiv i ALLA 7 kategorier.
