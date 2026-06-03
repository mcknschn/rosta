# Rösta — Backlog (framåtblickande arbete)

> Levande planeringsdokument för arbetet **efter** faser 0–6. Organiserat efter
> **arbetsspår** (inte faser) eftersom fasmodellen är levererad. Bärande princip
> oförändrad: inget partibetyg eller mänskligt omdöme i kod — bara i versionsstyrd
> config; all data spårbar till en officiell svensk källa (CLAUDE.md).

**Status-legend:** 🔵 nästa · ⚪ planerad · 🟣 designfråga (ej byggbar än) · ✅ klar (flyttas till ROADMAP).
**Effort:** `S` = återanvänder befintligt mönster · `M` = ny adapter · `L` = kräver research/design.

---

## Hur filerna hänger ihop

| Fil | Roll |
|-----|------|
| [ROADMAP.md](ROADMAP.md) | **Fryst historik** — hur faser 0–6 + b-faser byggdes och verifierades. Ändras inte. |
| [../config/coverage_allowlist.yaml](../config/coverage_allowlist.yaml) | **Maskinläsbar sanningskälla** för vilka D-indikatorer som ännu saknas, med skäl-tag. Coverage-gaten (`tests/test_fas3_gate.py`) tvingar varje indikator att vara *inläst* ELLER *allowlistad*. |
| **BACKLOG.md** (denna) | **Prioritering & plan** — vågordning per arbetsspår. Duplicerar inte allowlisten; pekar på den. När en indikator byggs: flytta ut den ur allowlisten och bocka av här. |

---

## Varför den här prioriteringen

Rankingen drivs i dag mest av **A (aktivitet) + C (makt)**, eftersom **B krymps mot
neutralt** vid tunn täckning och **D är "ej tillämplig" i 21 av 56 celler**. Modellen mäter
alltså än så länge mer *vad partierna prioriterar och har styrt* än *om utfallet blivit
bättre* — tvärtemot grundidén (objektivt utfall, IDEA.md).

**Mål med backloggen:** flytta tyngdpunkten mot **B (evidens/träffsäkerhet)** och
**D (resultat)** så att betygen speglar utfall, inte bara emfas. Vald strategi: **balans** —
billig D-bredd (återanvänder API-mönster) *parallellt* med att höja B:s trovärdighet
(expertgranskning + bredare evidensliggare). De två hänger ihop: bredare evidensliggare →
högre coverage → mindre B-krympning → B får faktiskt genomslag.

### Levererat (2026-06-03)

- ✅ **O1 — serie-drift-skydd** ([pipeline/expectations.py](../pipeline/expectations.py)): deklarativa
  förväntansassertioner (min_points / value_range / min_latest_year / förankrade publicerade värden)
  per inläst serie, wired i build_fas2/fas3 så en tyst fel-serie-hämtning hard-failar. Alla 17
  befintliga serier har en förväntan (testtvingat); 0 falsklarm mot verklig data.
- ✅ **D-bredd: `uppklaringsgrad`** (trygghet → rättsväsendets effektivitet, riktning up): Brås
  **personuppklaringsprocent** (samtliga brott, tidsserie 10La), 2016–2025. Live-hämtad +
  driftgrindad + golden-testad ([test_source_bra_uppklaring](../tests/test_source_bra_uppklaring.py)),
  ur allowlisten, omräknad i `dist/`. Trygghets-D nu uppmätt och differentierat. *(Codex-granskning
  av måttvalet pågår.)*

---

## Spår D — Datatäckning (utfall, delpoäng D)

Mål: fler kanoniska årsserier som matar D-attributionen, så fler kategorier/submått mäts på
faktiskt utfall. Alla nya serier ska vara kanoniska (finnas i `categories.yaml` med rätt
riktning) och annuella, så de matar `category_d` automatiskt.

### Våg 1 — billig bredd (återanvänder befintliga mönster) 🔵

| Indikator | Kategori → submått | Källa & metod | Återanvänder | Tag |
|-----------|--------------------|---------------|--------------|-----|
| `uppklaringsgrad` | trygghet → rättsväsendets effektivitet | Brå, handlagda brott (Excel) | `bra.fetch_*`-mönster | future |
| `handlaggningstid` | trygghet → rättsväsendets effektivitet | Brå / Åklagarmyndigheten (Excel) | `bra.fetch_*` | future |
| `aterfall_i_brott` | trygghet → återfall/kriminalvård | Brå / Kriminalvården, återfallsstatistik (Excel) | `bra.fetch_*` | future |
| `skjutningar_sprangningar` | trygghet → grov brottslighet | Polisens statistik (CSV/Excel) | liten ny adapter | future |
| `overlevnad_svar_sjukdom` | välfärd → vård tillgänglighet/kvalitet | Socialstyrelsens statistikdatabas (PxWeb-likt) | SCB-likt PxWeb-mönster | future |
| `vard_i_tid` | välfärd → vård tillgänglighet | Kolada-KPI (kräver val av up-polaritets-KPI) | `kolada.fetch_kpi_series` | future |

**Varför först:** trygghet har i dag 3 D-serier men bara på *utsatthet/grovt våld* — de fyra
första lyfter rättsväsende + förebyggande + återfall, så **trygghets-D går från ~halv till
nästan full submåttstäckning**. Det är en kategori vars betyg i dag drivs av A/C. Allt utom
Polisen/Socialstyrelsen återanvänder Brå-Excel-mönstret som redan finns.

### Våg 2 — nya adaptrar (källa finns men ej rent öppet API) ⚪

| Indikator | Kategori → submått | Källa & metod | Effort | Tag |
|-----------|--------------------|---------------|--------|-----|
| `realloner` | ekonomi → reallöner/hushåll | Medlingsinstitutets konjunkturlönestatistik (helekonomi-löneindex; SCB:s API saknar ren serie) | M | future |
| `sfi_sprakkunskaper` | integration → skola/språk | Skolverkets statistikportal (kräver semantikval: godkäntandel vs progression) | M | future |
| *(Svk-källadapter)* | klimat (förkrav för Våg 3-härledda) | Svenska kraftnät, öppna data (spotpris/effektbalans) | M | derived-förkrav |

### Våg 3 — härledda + design­krävande ⚪🟣

| Indikator | Kategori → submått | Metod | Effort | Tag |
|-----------|--------------------|-------|--------|-----|
| `elprisvolatilitet` | klimat → energi/elpriser | härled ur Svk spotpris (`derived.py`-mönster) | S (efter Svk-adapter) | derived |
| `effektbrist` | klimat → energi/elpriser | härled ur Svk effektbalans | S (efter Svk-adapter) | derived |
| `utslappsminskning_per_krona` | klimat → kostnadseffektivitet | utsläpp ÷ klimatutgift (flera serier) | M | derived |
| `personal_varnpliktiga` | försvar → militär förmåga | Försvarsmaktens ÅR / Plikt- och prövningsverket — sannolikt transkribering med källrad (jfr budget/SKR) | L | no_api |
| `fortroende_domstolar_myndigheter` / `tillit_valdeltagande` | demokrati | SOM-institutet (akademisk, **tillåten**) — ej maskinläsbar → transkribering med dokumenterad metod | L | no_api |

### Medvetet **inte** för D (stäng som designbeslut)

- **`target`-indikatorer** (`inflation`, `statsskuld_underskott`, `forsvarsanslag_andel_bnp`):
  har ingen up/down-riktning (nära mål ≠ "uppåt bra") → ej D-dugliga. Behålls för B/visning.
- **`international`** (`korruption`/TI CPI, `mediefrihet`/RSF): förbjudna enligt CLAUDE.md
  (ej officiell svensk källa). Demokrati måste lösas via svenska akademiska källor (SOM) eller
  redovisas som låg täckning med hög osäkerhet — bygg **aldrig** internationella index för D.
- **`qualitative`/sekretess** (försvars materiel/operativ förmåga, civil beredskap, Ukraina-stöd,
  Nato-interoperabilitet): ingen öppen mätserie → acceptera gap, redovisa via osäkerhet.

---

## Spår B — Evidens & trovärdighet (delpoäng B)

Störst hävstång på trovärdighet. B väger 35 % men vilar i dag på **30 evidensposter + 130
ståndpunkter, alla "version 0, AI-utkast"**.

- **B1 — Expertgranska version-0-config** 🔵 — kör igenom granskningspaketet i
  [expertgranskning/](expertgranskning/) (evidensliggare + partiståndpunkter + budgetramar).
  Output: signerad granskning → bumpa `version: 0 → 1` i `evidence_ledger.yaml` /
  `party_positions.yaml`. **Detta är förutsättningen för "skarp" betygsättning.**
- **B2 — Bredda evidensliggaren** ⚪ — i dag ≥3 åtgärdstyper/kategori. Fler källbelagda
  åtgärdstyper per kategori → högre `coverage` → mindre B-krympning mot neutral. Det är den
  enskilt största åtgärden för att B faktiskt ska differentiera partier.
- **B3 — Fler omstridda/differentierande åtgärdstyper** ⚪ — återanvänd Plan A-mönstret
  (Fas 4c): kandidatregister → endast intersektionen *omstridd ∧ evidensbelagd* → negativ-grind.

---

## Spår A — Agerande (delpoäng A)

- **A1 — Fler budgetår** ⚪ — `budget_ramar.yaml` har i dag **bara budget 2025**. Lägg 2023 + 2024
  (samma trogna transkriberingsmönster, källrad per frame) → a1 blir ett snitt över år i stället
  för en enda mätpunkt, och fångar mandatperiodskiftet.
- **A2 — Aktivera voteringsprovet** 🟣 — röster hämtas redan (12 riksmöten) men matar inget
  betyg. Designfråga: hur väga faktiskt röstbeteende per kategori in i A utan att dubbelräkna a2.

---

## Spår C — Ansvar (delpoäng C)

- **C1 — c2 (finansiering)** 🟣 — uppskjutet: inget objektivt, riktningsneutralt mått går att
  bygga ur officiell data (se [fas1c_subnational_metod.md](fas1c_subnational_metod.md) §c2).
  Hålls öppen tills en neutral källa uppstår; komponentvikt 0.7/0.3 behålls som avsikt.
- **C2 — Mandatperiodskiften mitt i period** ⚪ — regeringsbyte mitt i ett år hanteras grovt i dag.
- **C3 — Subnationell D-resultatdata** ⚪ — D attribueras i dag bara på nationell makt; region/
  kommun-utfall (Kolada finns) skulle koppla subnationell makt till subnationellt resultat.

---

## Spår F — Frontend & publicering

- **F1 — Faktisk publicering** ⚪ — `web/` är byggfri statisk men hostas ingenstans. Sätt upp
  statisk hosting + CI som bygger om `dist/` och deployar (rådata stannar lokalt per design).
- **F2 — Manuell skärmläsartest** ⚪ — sista WCAG 2.2 AA-punkten (NVDA/VoiceOver); allt övrigt klart.

---

## Spår O — Drift, robusthet & ops

- **O1 — Serie-drift-skydd** 🔵 — SCB-serier isoleras via hårdkodade dimensionskoder (`fixed`).
  Om SCB byter tabell-/dimensionskod kan pipelinen tyst hämta *fel* serie. Lägg en
  rimlighets-/förväntansassertion per serie (ungefär som `derived.py`:s nivå-grind). Billigt,
  skyddar allt annat datalager.
- **O2 — Schemalagd ominhämtning + dist-versionering** ⚪ — diff mellan körningar så
  utfallsändringar syns; undviker tyst regression.
- **O3 — Live-fetch smoke test** ⚪ — opt-in `network`-markör finns redan; lägg ett cron-/manuellt
  jobb som bekräftar att källornas endpoints fortfarande svarar med förväntad form.

---

## Föreslagen ordning (vågor)

| Sprint | Data (D) | Evidens (B) | Övrigt |
|--------|----------|-------------|--------|
| **1** | Våg 1: Brå (uppklaring/handläggning/återfall) + Socialstyrelsen (överlevnad) | **B1: starta expertgranskning** | **O1: drift-skydd** |
| **2** | Våg 2: Medlingsinstitutet (reallöner) + Skolverket (sfi) + Svk-adapter | B2: bredda liggaren | A1: fler budgetår |
| **3** | Våg 3: härledda klimat (elpris/effekt) + demokrati/försvar-design | B3: omstridda åtgärdstyper | A2 votering · C2/C3 · F1/F2 |

> Varje levererat steg: flytta indikatorn ur `coverage_allowlist.yaml`, uppdatera täckningssiffran
> i `scorerun.py:coverage`-strängen, och bocka av posten här (✅ → kort rad i ROADMAP.md).
