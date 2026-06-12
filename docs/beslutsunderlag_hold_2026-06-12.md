# Beslutsunderlag — HOLD-beslut som väntar sign-off

**Status:** väntar användarens sign-off · **Datum:** 2026-06-12 · **Varifrån:** djupsvepet §5.8 +
kandidat-pipeline §7 (2026-06-06) samt nedstigningarna/svepen 2026-06-07, alla dokumenterade i
[done/evidens_trovardighet.md](done/evidens_trovardighet.md) (§6 statustavla, §8.7, §9 beslutslogg)
och [BACKLOG.md B4-tabellen](BACKLOG.md). §8.8-sign-offen 2026-06-07 stängde de **byggda** måtten
(6 st → v2); det här dokumentet samlar det som **inte** stängdes: kvarvarande HOLD-väggar samt den
fortfarande FLAGGADE invasiva-arter-posten. Varje paket avslutas med en fråga att svara
**JA/NEJ/VAL** på.

| # | Beslut | Rekommendation | Brådska |
|---|--------|----------------|---------|
| H1 | valfard / vard_tillganglighet (bredd) | A — stäng HOLD som BEVAKA (cancerscreening-trigger) | Låg |
| H2 | valfard / omsorg_personal | A — bekräfta BEVAKA (Socialstyrelse-måttet dec 2026) | Låg |
| H3 | integration / normer_tillit | A — HOLD/BEVAKA + dokumenterat undantag från B-grön-mandatet | Medel |
| H4 | integration / boendesegregation | A — HOLD/BEVAKA + dokumenterat undantag (bosättningslag ~2027) | Medel |
| H5 | klimat / invasiva främmande arter | A — BEHÅLL, avflagga, bumpa v0→v1 | Låg (snabbast att avgöra) |
| H6 | forsvar / genomforbarhet_leverans | A nu + sonderingsmandat för FMV-leveransindex (D-spår) | Låg (vikt 5/100) |
| D1 | klimat / utslappsminskning_per_krona | A — stäng som designbeslut (sondering avråder; sista exit-spärren för D-trackern) | Medel (låser arkivering) |
| B1 | forsvar / dca_avtal_usa (B3) | Sign-off: bygg/HOLD — se b3_kandidatregister | Medel |
| B2 | demokrati / rättssäkerhetsgarantier preventiva tvångsmedel (B3) | Sign-off: instrumentlåsning + bygg/HOLD — se b3_kandidatregister | Medel |
| — | KU39 / transparens_ansvar | Inget HOLD-beslut — hantera direkt efter riksdagsbeslutet | **2026-06-15** |

---

### H1. valfard / vard_tillganglighet — breddinstrumenten föll; undermåttet är ändå redan B-grönt
- **Läge:** HOLD 2026-06-06. Djupsvep §5.8 (11 instrument, dokumenterat i evidens_trovardighet.md §6):
  vårdplats-slutrapporten (Vård- och omsorgsanalys 2026:3) **föll nedåt** — "Hittills ser satsningen inte
  ut att ha bidragit till att öka antalet vårdplatser på nationell nivå" (återöppningsvillkoret konsumerat
  negativt). **Cancerscreening** är enda instrumentet som passerar riktningsgrinden (Socialstyrelsen:
  −15 %/−16–20 % dödlighet) men **faller på neutralitet** (SoU16 p2/SoU17 p3 = avslag med
  oppositionsreservationer; screening beslutas dessutom regionalt). B4-tabellen: "Väg till 4 kräver
  modellutvidgning → sign-off." **OBS:** undermåttet fick sedan sin B-gröna indikator 2026-06-07 via
  `koncentration_nationell_hogspecialiserad_vard` → `overlevnad_svar_sjukdom` (SoU18 p1, godkänd i
  §8.8-sign-offen) — B-grön-mandatet är alltså redan uppfyllt här; frågan gäller enbart ytterligare *bredd*.
- **Alternativ:**
  - **A (rek):** Stäng HOLD som **BEVAKA** med trigger: enhälligt SoU-betänkande om nationella
    cancerstrategin 2.0 där alla 8 står bakom screening utan tilt → ren BUILD via §5.2. Ingen modelländring.
  - **B:** Bygg cancerscreening på dagens källäge → bryter neutralitetsgrinden (avslag + opp-reservationer
    = tilt mot oppositionssidan). Avråds.
  - **C:** Modellutvidgning nu (ny screening-indikator i categories.yaml) → strukturändring utan neutralt
    steg-2-ankare; löser inget B inte redan löst.
- **Betygskonsekvens:** A: ingen. B/C: skulle lyfta reservationssidan (S/V/MP) på välfärd → systematisk tilt.
- **Rekommendation:** A — "neutralitet före 4" + undermåttet bidrar redan; bevaka triggern.
- **Beslutsfråga:** **JA/NEJ** — stänger vi vard_tillganglighet-bredden som BEVAKA med
  cancerstrategi-triggern (inget bygge, ingen modelländring)?

### H2. valfard / omsorg_personal — fel konstrukt (omsättning); löst via kontinuitet, väggen kvar att stänga
- **Läge:** HOLD 2026-06-06 (samma §5.8-djupsvep, 5 instrument): `fast_omsorgskontakt` har **perfekt
  steg 2** (SoU24 p2, acklamation, alla 8) men **fel konstrukt i steg 1** — kompetens (Äldreomsorgslyftet),
  heltid (Heltidsresan) och kontinuitet ≠ *personalomsättning*; ingen källa belägger sänkt omsättning.
  Socialstyrelsens kommande mått är **samma felkonstrukt** (personalkontinuitet, del 2026-12-16, slut
  2027-10-01) och SKR lade ned kontinuitetsstatistiken 2024 → även D-underlaget borta (allowlist:
  `no_api`). Löst i praktiken 2026-06-07: NY indikator `kontinuitet_i_omsorgen` byggd och godkänd
  (Beslut 9), `personalomsattning_omsorg` omklassad 🔴 BEVAKA (Beslut 8).
- **Alternativ:**
  - **A (rek):** Bekräfta BEVAKA-statusen formellt med trigger: Socialstyrelsens mått + en
    effektutvärdering som faktiskt avser *omsättning* → då återupplivas indikatorn.
  - **B:** Stryk `personalomsattning_omsorg` ur categories.yaml → onödigt (renormaliseras redan bort,
    poängneutral) och förstör återöppningsvägen.
  - **C:** Ny instrumentjakt nu → uttömd enligt §5.8 (strukturell vägg: inget partistyrbart instrument
    flyttar måttet bevisat nedåt).
- **Betygskonsekvens:** Ingen i något alternativ (indikatorn är död/poängneutral; undermåttet bärs av
  kontinuitet-indikatorn).
- **Rekommendation:** A — detta formaliserar bara Beslut 7+8 från 2026-06-07.
- **Beslutsfråga:** **JA/NEJ** — bekräftar du BEVAKA med omsättnings-triggern (ingen åtgärd förrän
  Socialstyrelse-måttet + utvärdering finns)?

### H3. integration / normer_tillit — steg 1 löst (Delmi 2025:5), steg 2 saknar neutralt ankare
- **Läge:** HOLD 2026-06-06, bekräftad i tre rundor (§5.8-djupsvep 6 instrument + nedstigning +
  extra runda 2026-06-07). Renaste near-miss **KU4-tillgänglighet**: perfekt steg 2 (KU4 p1 acklamation,
  alla 8) men **fel konstrukt** — källan belägger "likvärdig möjlighet att utöva rösträtten", inte *uppmätt
  valdeltagande*. GOTV: **Delmi 2025:5 löser steg 1 kausalt**, men varje riksdagsbehandling 2022–2026 är
  avslag med enpartisreservation eller acklamation där oppositionen *avstod* → inget neutralt steg-2-ankare.
  IFAU 2017:12 (yrkesprogram → valdeltagande): partistyrbart men UbU22-spliten ligger på fel värdeaxel.
  **D-täckt sedan 2026-06-12** via syskonindikatorn `mellanmansklig_tillit` (SCB N00666) — men
  B-grön-mandatet (2026-06-06) säger ≥1 B-grön per undermått, **D-only räcker inte**; och mandatets
  v0-väg ("neutral-men-svag, aldrig tiltad") är stängd: kandidaterna är tiltade, inte svaga.
- **Alternativ:**
  - **A (rek):** HOLD/BEVAKA med dubbla triggrar: (i) enhälligt/acklamerat GOTV-anslag där oppositionen
    EJ avstår → §5.2 på Delmi 2025:5; (ii) acklamerad UbU-behandling av treåriga yrkesprogram utan
    avslagsreservation → §5.2 på IFAU 2017:12. **Dokumenterat undantag från B-grön-mandatet.**
  - **B:** Bygg på UbU22-spliten nu → kodar SD+L `opposes` på utbildningskvalitets-grund som
    anti-valdeltagande = konstrukt-missmatch + tilt. Avråds skarpt (högsta bias-risk-kategorin).
- **Betygskonsekvens:** A: ingen. B: SD/L straffas på en värdeaxel källan inte bär → trovärdighetsskada.
- **Rekommendation:** A — konsekvent med användarbeslutet 2026-06-07 ("ACCEPTERA 3/5", neutralitet före 4).
- **Beslutsfråga:** **JA/NEJ** — accepterar du att normer_tillit står utan B-grön tills en trigger faller
  ut (formellt loggat undantag från B-grön-mandatet)?

### H4. integration / boendesegregation — väggen är steg 2/neutralitet; ingen neutral-men-svag kandidat finns
- **Läge:** HOLD 2026-06-06 (§5.8-djupsvep, 5 instrument: "äkta steg-1-vägg, allt beskrivande/mixed").
  **Diagnosen rättad 2026-06-07** (nedstigning, loggrättelse §9): steg-1-evidens FINNS — **RiR 2021:29**
  (bosättningslagen/kommunanvisning → jämnare kommunspridning; gamla systemet "ökade segregationen") —
  väggen är **STEG 2/neutralitet**: SD vill avskaffa lagen på *kommunalt-självstyre*-grund, M behålla →
  genuin värdekonflikt (Dir 2024:22) = tilt. Kamera-vägen byggdes → **reverterades** (codex KILL:
  trygghet-relabel + dubbelräkning). Alternativ-undermått-analysen 2026-06-07: inget rent byte (§5.8
  "fuska inte"). **Ditt stående mandat (2026-06-06):** ≥1 B-grön per undermått — D-only (`trangboddhet`
  är D-inläst) räcker inte; men mandatets "bygg flaggad v0 för neutral-men-svag" är inte tillämpbart:
  varje kandidat faller på **tilt**, inte på svaghet — och tiltad byggs ALDRIG.
- **Alternativ:**
  - **A (rek):** HOLD/BEVAKA med trigger: nya bosättningslagen (ur Dir 2024:22, ikraft ~2027) tas i
    enhälligt SfU/AU-betänkande utan självstyre-reservation mot huvudpunkten → RiR 2021:29 blir steg 1
    och §5.2 löser steg 2. **Dokumenterat undantag från B-grön-mandatet.** Bevaka SfU 2026/27.
  - **B:** Bygg bosättningslag-måttet nu → kodar SD `opposes` för en självstyre-position = tilt på fel
    värdeaxel i den mest bias-känsliga kategorin. Avråds skarpt.
  - **C:** Byt undermått → redan prövat och avvisat 2026-06-07 (alla alternativ dubbelräknar eller tiltar).
- **Betygskonsekvens:** A: ingen. B: SD straffas på integration utan konstrukt-exakt belägg.
- **Rekommendation:** A — samma logik som H3; väggen har den konkretaste triggern av alla (lagförslag på väg).
- **Beslutsfråga:** **JA/NEJ** — accepterar du boendesegregation utan B-grön tills
  bosättningslag-betänkandet (~2027), som formellt loggat mandat-undantag?

### H5. klimat / atgarder_mot_invasiva_frammande_arter — byggd v0 mot codex HOLD; behåll, justera eller riv
- **Läge:** Byggd 2026-06-06 (enhällighet §5.2: bet. 2025/26:MJU13 p1 acklamation, "inte väckts någon
  motion som går emot" → **alla 8 supports**; tiltade p2 utesluten) → `hotade_arter_naturforlust`,
  klimat/biologisk_mangfald 3/5→4/5. **Codex förordade HOLD** (rubrikcitatet bevisar hotet, ej
  instrumenteffekten); byggdes ändå med instrument-mekanismcitat (Naturvårdsverket: förteckningen är
  "ett verktyg i arbetet med att förebygga och begränsa spridningen av arter…" + prop. 2025/26:41 om
  tidig upptäckt) och **konservativ kalibrering authority_evaluation/low/low**. Ledger-noten slutar:
  "FLAGGAD för mänsklig sign-off — codex förordade HOLD". §8 fråga 5 noterar visserligen "BESLUTAT
  2026-06-06: BEHÅLL", men posten är fortfarande markerad FLAGGAD/v0 i evidence_ledger.yaml och
  B4-tabellen ("sign-off avgör") → formell stängning saknas. 8 ståndpunkter i party_positions.yaml,
  citat per parti (S/C/MP via särskilt yttrande resp. reservation som enbart gäller p2).
- **Alternativ:**
  - **A (rek):** **BEHÅLL** + ta bort FLAGGAD-markeringen (ledger-not + B4-rad) och bumpa posten v0→v1.
    Konsensus-mått (alla 8 supports) → kan inte tilta; low/low håller anspråket nere tills kvantifierad
    utvärdering finns.
  - **B:** **JUSTERA** — behåll men skriv in explicit uppgraderingsvillkor (kvantifierad svensk
    kausalutvärdering → low→medium). Marginellt mer arbete, ingen betygsskillnad i dag.
  - **C:** **RIV** — klimat 4/5→3/5, biologisk_mangfald förlorar sin enda B-gröna indikator → bryter
    B-grön-mandatet och sänker alla partiers klimat-B likformigt (−0,07…−0,20).
- **Betygskonsekvens:** A/B: ingen (likformigt lyft redan inräknat, icke-rankningsdrivande). C: se ovan.
- **Rekommendation:** A — konsekvent med public service-måttet (samma low/low-mekanismklass, godkänt).
- **Beslutsfråga:** **VAL A/B/C** — behåll och avflagga (A), behåll med uppgraderingsvillkor (B),
  eller riv posten (C)?

### H6. forsvar / genomforbarhet_leverans — steg 2 numera löst, steg 1 saknas; indikatorbyte kräver modellbeslut
- **Läge:** HOLD 2026-06-06; djupsvep §5.8 (7 instrument) bekräftade **äkta steg-1-vägg av
  indikator-typ**: officiella källor behandlar lång leveranstid som *exogent marknadsproblem* och kopplar
  instrumenten till kapacitet/kostnad — aldrig ordagrant till kortad ledtid (prop. 2024/25:34 fulltext-grep:
  0 träffar; RiR 2011:13 fann motsatsen). **Nedstigning 2026-06-07 krympte väggen: STEG 2 LÖST** —
  bet. 2025/26:FöU3 p1 "En försvarsindustristrategi" i acklamation, 0 reservationer mot p1 → alla 8
  supports på konstrukt-bytet `forsorjningstrygghet_materiel`; kvar ENBART steg-1/instrumenteffekt
  (+ dubbelräkningsrisk mot `materiel_formaga`). **Öppen idé:** indikatorbyte/komplettering till
  **FMV leveransindex** (leveransplaneutfall, % försenat — D-serie) — ändrar categories.yaml
  (`leveranstid_materiel` är i dag 🔴 BEVAKA, allowlistad "qualitative: sekretess") → sign-off.
  Undermåttet väger **5/100** i försvar → minst rankingkänsliga beslutet i listan.
- **Alternativ:**
  - **A (rek):** HOLD/BEVAKA, trigger: **EN** effektutvärdering (regeringens årliga strategiredovisning,
    FOI eller RiR) som belägger försörjningstrygghet-effekten → BUILD v0 på FöU3-ankaret (low/low).
  - **B:** Ge **sonderingsmandat** för indikatorbytet: verifiera först om FMV publicerar leveransutfall
    maskinläsbart/officiellt (sondera källan innan modelländring beslutas — sekretess-antagandet kan vara
    för pessimistiskt); faller sonderingen väl ut → konkret categories.yaml-förslag för separat sign-off.
  - **C:** Sänk/nolla undermåttets vikt → avråds (strukturen ska spegla IDEA.md, inte mätbarheten).
- **Betygskonsekvens:** A: ingen. B: ingen nu; en framtida FMV-D-serie skulle ge försvar D-bredd
  (försvar är i dag enda kategorin i `d_thin_breadth_accepted`, 70/100).
- **Rekommendation:** A **och** B parallellt — bevaka triggern och sondera FMV-källan; båda är gratis nu.
- **Beslutsfråga:** **VAL** — (A) bara bevaka, eller (A+B) bevaka **och** ge sonderingsmandat för
  FMV-leveransindex som framtida D-serie/indikatorkomplettering?

---

## D1. klimat / utslappsminskning_per_krona — sista öppna D-posten; sondering avråder bygge (tillagd kvällen 2026-06-12)

- **Läge:** enda kvarvarande icke-vägg-posten i `coverage_allowlist` (klass `derived`). Djupsonderad
  2026-06-12 med alla nämnarvägar nedladdade + parsade — full genomgång i
  [spar_D_datatackning.md §5.5](spar_D_datatackning.md). Kärnfyndet: ingen officiell källa definierar
  "klimatutgift" heltäckande, och kvoten Δutsläpp/utgift premierar strukturellt skattetung
  instrumentmix (CO2-skatt ≈ 0 kr på utgiftssidan) → ideologisk metodpreferens inbyggd i måttet,
  i strid med IDEA.md. Undermåttet kostnadseffektivitet är dessutom redan D-täckt via
  `utslappsintensitet` (CO2/BNP).
- **Alternativ:** **A (rekommenderad):** stäng som designbeslut — allowlist-skälet uppdateras till
  `design_closed` med §5.5-referens; Spår D-trackern arkiveras till `done/` (sista exit-kriteriet).
  **B:** bygg ändå minst-dåliga konstruktionen (3-års Δutsläpp ÷ SCB MI1301H, 2016–2025, flaggad v0)
  — avrådes av neutralitetsskäl.
- **Betygskonsekvens:** A = ingen. B = ny klimat-D-cell med hög neutralitetsrisk.
- **Rekommendation:** A — neutralitetsbrottet är strukturellt, inte datatekniskt; ingen nämnare löser det.
- **Beslutsfråga:** **JA/NEJ** — stänger vi `utslappsminskning_per_krona` som designbeslut (A) så att
  Spår D-trackern kan arkiveras?

---

## Notis 2 (B3-beslut, tillagda kvällen 2026-06-12): DCA-avtalet + preventiva tvångsmedel

Kvällens B3-research (7 kategorier, allt API-verifierat) gav 4 STRONG-kandidater. Två byggdes efter
Codex-triage (a-kassenedtrappningen → ekonomi/arbetsloshet; uppsökande förskoleerbjudande →
integration, SD/KD=none) — flaggade v0, din slutgranskning kvarstår. Två är **HOLD för din sign-off**,
fullt beredda med beslutsfrågor i [b3_kandidatregister_2026-06-12.md](b3_kandidatregister_2026-06-12.md):
- **B1: `dca_avtal_usa`** (forsvar → nato_interoperabilitet) — Codex HOLD pga NATO-stackning (V skulle
  få andra opposes-posten på samma indikator) + p1-roll-call utanför voterings-API:t.
- **B2: `rattssakerhetsgarantier_preventiva_tvangsmedel`** (demokrati → overvakning_utan_rattssakerhet)
  — Codex HOLD pga S-kodningen (kräver instrumentlåsning före kodning) + andra rättssäkerhetsposten
  i personlig_frihet.

---

## Notis (ej HOLD-beslut): KU39 / transparens_ansvar — riksdagsbeslut 2026-06-15

Prop. 2025/26:258 "Ökad insyn i politiska processer" (lobbyregister + förbud mot anonyma/utländska
partibidrag) avgörs i kammaren **2026-06-15** (bet. 2025/26:KU39). Detta är ingen HOLD-vägg — riktningen
är redan belagd (dir. 2023:88: insyn "förebygger korruption och ökar … legitimitet", ingen dubbelräkning
mot offentlighetsprincipen) och bygginstruktionen är klar sedan tidigare (evidens_trovardighet.md §6):
**bygg när KU39 är voterat; koda EJ del 2 om fackbidrag (S-tilt).** Det skulle ge transparens_ansvar —
i dag demokratis svagaste undermått (enbart enhällighets-måttet insyn partifinansiering 2018, low/low) —
ett aktuellt mått och därmed demokrati **5/5 med full B-bredd**. Bör hanteras direkt efter beslutet:
hämta voteringen/dokumentstatus per parti mot data.riksdagen.se och bygg enligt källstegen §5.1.
