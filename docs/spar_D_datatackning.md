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
A (aktivitet) + C (makt). D är `not_applicable` i **21 av 56 celler**. Modellen mäter alltså mer
*vad partierna prioriterar och har styrt* än *om utfallet blev bättre* — tvärtemot grundidén. Att
bredda D flyttar tyngdpunkten mot faktiskt utfall.

---

## 2. Nuläge (verifierat via `python -m pipeline.tools.coverage_report`, 2026-06-07)

**24/56 indikatorer inlästa** (annuell, D-duglig) i **ALLA 7 kategorier** (efter Tier 4, §7). **Ingen
kategori är längre D-tom — båda strukturella nollorna (försvar + demokrati) fyllda.** *(Var 19/56 innan
Tier 1; +2 ekonomi + 1 integration + 1 försvar + 1 demokrati 2026-06-07.)*

| Kategori | D-täckta submått | Inlästa D-serier |
|----------|:---:|---|
| ekonomi | **4 / 4 D-bara¹** | sysselsattning, arbetsloshet, bnp_per_capita, produktivitet, **naringslivets_investeringar**, **hushallens_reala_disponibla_inkomst** |
| valfard | 2 / 4 | vardkoer, skolresultat, behoriga_larare |
| trygghet | 3 / 5 | dodligt_vald, skjutningar_sprangningar, brottsutsatthet, upplevd_otrygghet, uppklaringsgrad |
| forsvar | **1 / 5** | **personal_varnpliktiga** (första D — Tier 4; militar_formaga öppnat) |
| klimat | 2 / 5 | territoriella_utslapp, konsumtionsbaserade_utslapp, fossil_energianvandning |
| integration | 3 / 5 | sysselsattningsgap_inrikes_utrikes, sjalvforsorjningsgrad, bidragsberoende, trangboddhet, **sfi_sprakkunskaper** |
| demokrati | **1 / 5** | **fortroende_domstolar_myndigheter** (första D — Tier 4; Brå NTU 5A:1, korruption_tillit öppnat) |

¹ ekonomi har 6 submått men 2 är `target`-only (inflation, offentliga finanser) → ej D-bara.

**Strukturellt (ej en databredd-fråga, lämnas som är):** `V` får `D_not_applicable` i alla
kategorier — Vänsterpartiet har inte suttit i nationell regering i fönstret 2014–2026, så det finns
inget ansvar att attribuera. Det är **korrekt och rättvist**, inte ett gap.

---

## 3. Arbetskö — D-lösa submått med byggbarhet

Status: 🔵 nästa · ⚪ planerad · 🟣 designbeslut krävs · 🔴 blockerad/stängd · ✅ klar.
Effort: `S` återanvänder befintlig adapter · `M` ny adapter · `L` transkribering/research/design.

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
| ☐ | `realloner` | ekonomi → realloner_hushall | Medlingsinstitutets konjunkturlönestatistik | M | Samma submått som Tier 1-posten täcker billigare → låg prio. |

¹ Visade sig vara **S, inte M**: SCB (producenten) exponerar sfi-statistiken som en ren PxWeb-v2-
tabell (TAB1814), så den befintliga `scb.py`-adaptern räckte — ingen egen Skolverket-portaladapter
behövdes. Allowlistens "ej ren PxWeb"-antagande (Skolverkets portal) var överspelat. Metodbrott 2022
hanteras genom att hela serien behålls (sign-only D är robust mot magnitudskiftet); se §7 + `build_fas2`-not.

### Tier 3 — härledd, kräver ny föräldraadapter (M+S) ⚪🟣

| ☐ | Indikator | Kategori → submått | Metod | Effort | Not |
|---|-----------|--------------------|-------|:---:|-----|
| ☐ | *(Svk-källadapter)* | förkrav klimat-energi | Svenska kraftnät öppna data (spotpris/effektbalans) | M | Förkrav för nästa två. **Gränsfall mot officiell-källa-regeln** (Nord Pool-pris) → §5.4. |
| ☐ | `elprisvolatilitet` | klimat → energi_elpriser | härled ur Svk spotpris (`derived.py`) | S | Submått redan täckt (djup). |
| ☐ | `effektbrist` | klimat → energi_elpriser | härled ur Svk effektbalans | S | Submått redan täckt (djup). |
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
- **`international`** (otillåtet, CLAUDE.md): `korruption` (TI CPI), `mediefrihet` (RSF).
- **`qualitative`/sekretess** (försvar/demokrati): `materiel_formaga`, `civil_beredskap_niva`,
  `ukraina_stod`, `nato_interoperabilitet`, `leveranstid_materiel`, `otillborlig_politisering`,
  `overvakning_utan_rattssakerhet`, `politisk_transparens`.
- **`no_api`** (ingen maskinläsbar årsserie): `skillnader_mellan_skolor`, `personalomsattning_omsorg`,
  `valfardsbrottslighet`, `hotade_arter_naturforlust`, `skolresultat_utsatta_omraden`, `segregation`.
- **`blocked`** (PDF prel/slutlig + metodbrott): `aterfall_i_brott`.
- **`future`/interaktiv DB** (ingen ren årsserie funnen): `handlaggningstid`.
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
4. **Tier 3 Svk-derived** — mest djup (energi-submåttet är redan täckt); lägst prioritet, gränsfall
   mot källregeln. **← nästa om mer D-bredd önskas** (men öppnar inget D-löst submått).
5. **Tier 2-rest** (`overlevnad_svar_sjukdom` §5.3, `realloner`) — kvar i Tier 2 men kräver sondering/
   är låg prio (samma submått billigare täckt).

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

### 5.3 `overlevnad_svar_sjukdom`: finns en annuell serie?
Cancer-5-årsöverlevnad (Kolada N79196) är kvinkennial → inkompatibel med D:s konsekutiva-år-krav.
Behöver sonderas om Socialstyrelsen/Kolada har en **annuell** överlevnadsindikator (t.ex.
28-/30-dygnsöverlevnad efter hjärtinfarkt/stroke) som matchar submåttet utan modellutvidgning.

### 5.4 Svk-adapter: håller den källregeln?
Spotpris (Nord Pool) + operativ effekt-/timdata är gränsfall mot "officiell svensk källa". Lågt
mervärde (klimat-energi redan täckt). Avgör om det är värt det innan adaptern byggs.

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
   några `future`-poster — overlevnad_svar_sjukdom, realloner, Svk-derived — kräver sondering/beslut.)*
4. `docs/fas3_coverage.md` + `scorerun.py:coverage`-strängen speglar slutläget; testsviten grön. ✅

---

## 7. Leveranslogg (append per leverans)

> Format: datum · indikator · kategori→submått · källa · verifiering · betygseffekt · flagga/version.

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
