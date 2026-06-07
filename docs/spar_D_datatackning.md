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

**21/56 indikatorer inlästa** (annuell, D-duglig) i **5/7 kategorier** (efter Tier 1, §7). Försvar +
demokrati = 0 D. *(Var 19/56 innan Tier 1; +2 ekonomi 2026-06-07.)*

| Kategori | D-täckta submått | Inlästa D-serier |
|----------|:---:|---|
| ekonomi | **4 / 4 D-bara¹** | sysselsattning, arbetsloshet, bnp_per_capita, produktivitet, **naringslivets_investeringar**, **hushallens_reala_disponibla_inkomst** |
| valfard | 2 / 4 | vardkoer, skolresultat, behoriga_larare |
| trygghet | 3 / 5 | dodligt_vald, skjutningar_sprangningar, brottsutsatthet, upplevd_otrygghet, uppklaringsgrad |
| forsvar | **0 / 5** | — (strukturell lucka) |
| klimat | 2 / 5 | territoriella_utslapp, konsumtionsbaserade_utslapp, fossil_energianvandning |
| integration | 2 / 5 | sysselsattningsgap_inrikes_utrikes, sjalvforsorjningsgrad, bidragsberoende, trangboddhet |
| demokrati | **0 / 5** | — (strukturell lucka) |

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

### Tier 2 — ny adapter, källa finns (M) ⚪

| ☐ | Indikator | Kategori → submått | Källa/metod | Effort | Not |
|---|-----------|--------------------|-------------|:---:|-----|
| ☐ | `sfi_sprakkunskaper` | integration → skola_sprak | Skolverkets statistikportal (Komvux i sfi) | M | Öppnar D-löst submått. Semantikval: godkäntandel vs progression (§5.2). |
| ☐ | `overlevnad_svar_sjukdom` | valfard → vard_tillganglighet | Socialstyrelsen/Kolada — **annuell** överlevnadsserie | M | Submått redan täckt (djup, ej bredd). Cancer-KPI N79196 = kvinkennial/inkompatibel; **annuellt alternativ behöver sonderas** (t.ex. 28-dygnsöverlevnad AMI/stroke) (§5.3). |
| ☐ | `realloner` | ekonomi → realloner_hushall | Medlingsinstitutets konjunkturlönestatistik | M | Samma submått som Tier 1-posten täcker billigare → låg prio. |

### Tier 3 — härledd, kräver ny föräldraadapter (M+S) ⚪🟣

| ☐ | Indikator | Kategori → submått | Metod | Effort | Not |
|---|-----------|--------------------|-------|:---:|-----|
| ☐ | *(Svk-källadapter)* | förkrav klimat-energi | Svenska kraftnät öppna data (spotpris/effektbalans) | M | Förkrav för nästa två. **Gränsfall mot officiell-källa-regeln** (Nord Pool-pris) → §5.4. |
| ☐ | `elprisvolatilitet` | klimat → energi_elpriser | härled ur Svk spotpris (`derived.py`) | S | Submått redan täckt (djup). |
| ☐ | `effektbrist` | klimat → energi_elpriser | härled ur Svk effektbalans | S | Submått redan täckt (djup). |
| ☐ | `utslappsminskning_per_krona` | klimat → kostnadseffektivitet | utsläpp ÷ klimatutgift | L | Öppnar D-löst submått, men "klimatutgift" är metodiskt omtvistad (vilket UO?) → §5.5. |

### Tier 4 — transkribering med källrad, fyller strukturella nollor (L) 🟣

Samma trogna transkriberingsmönster som `budget_ramar.yaml` / SKR / `skjutningar_sprangningar.yaml`
(källrad per värde, korsverifiering, auditverktyg). **Högsta strategiska värde** — ger de två
D-blanka kategorierna sin första utfallsserie — men störst arbete och integritetskrav.

| ☐ | Indikator | Kategori → submått | Källa/metod | Effort | Not |
|---|-----------|--------------------|-------------|:---:|-----|
| ☐ | `personal_varnpliktiga` | **forsvar** → militar_formaga | Försvarsmaktens ÅR / Plikt- och prövningsverket | L | **Ger försvar sin första D.** Transkribering, ej API. |
| ☐ | `fortroende_domstolar_myndigheter` | **demokrati** → korruption_tillit | SOM-institutet (akademisk, tillåten) | L | **Ger demokrati sin första D.** Ej maskinläsbar → transkribering m. dokumenterad metod. |
| ☐ | `tillit_valdeltagande` | integration → normer_tillit | SOM-institutet (akademisk) | L | Öppnar D-löst submått. Valdeltagande bara valår (glest). |

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

1. **Tier 1** (om §5.1-beslutet blir bygg) — billigaste reella D-breddning; tar ekonomi till full
   D-täckning av sina D-bara submått. Validerar trackern med en liten, säker leverans.
2. **Tier 2 `sfi_sprakkunskaper`** — öppnar integration/skola_sprak (D-löst submått) via ny men
   välavgränsad Skolverket-adapter.
3. **Tier 4 strukturella nollor** (`personal_varnpliktiga`, SOM) — högst strategiskt värde (försvar +
   demokrati får sin första D), men störst arbete; tas när billigare bredd är uttömd.
4. **Tier 3 Svk-derived** — mest djup (energi-submåttet är redan täckt); lägst prioritet, gränsfall
   mot källregeln.

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

### 5.2 `sfi_sprakkunskaper`: vilken semantik?
Godkäntandel (nivå) vs progression/genomströmning. Måste väljas innan adaptern byggs; påverkar
riktningstolkning. Officiell statistikansvarig: Skolverket (producent SCB).

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
2. Båda strukturella nollorna (försvar, demokrati) har **antingen** sin första D-serie **eller** ett
   uttryckligt accepterat "redovisas som låg täckning med hög osäkerhet"-beslut (sign-off).
3. `coverage_allowlist.yaml` innehåller bara poster i klasserna `target`/`international`/`qualitative`/
   `blocked`/`no_api` (= genuint ej byggbara) — inga `future`-poster kvar utan beslut.
4. `docs/fas3_coverage.md` + `scorerun.py:coverage`-strängen speglar slutläget; testsviten grön.

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
