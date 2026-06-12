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
| [ROADMAP.md](done/ROADMAP.md) | **Fryst historik** (arkiverad i `done/`) — hur faser 0–6 + b-faser byggdes och verifierades. Ändras inte. |
| [../config/coverage_allowlist.yaml](../config/coverage_allowlist.yaml) | **Maskinläsbar sanningskälla** för vilka D-indikatorer som ännu saknas, med skäl-tag. Coverage-gaten (`tests/test_fas3_gate.py`) tvingar varje indikator att vara *inläst* ELLER *allowlistad*. |
| **BACKLOG.md** (denna) | **Prioritering & plan** — vågordning per arbetsspår. Duplicerar inte allowlisten; pekar på den. När en indikator byggs: flytta ut den ur allowlisten och bocka av här. |
| [evidens_trovardighet.md](done/evidens_trovardighet.md) | **B-spårets arbetslogg & metodutveckling** — bärande: **tvåstegsmodellen** (måttet ≠ positioneringen). Skiljer äkta steg-1-väggar (måttet saknas) från steg-2-källval (acklamation slår bara ut voteringskällan). Metodregister för positionering (källstege, enhällighet, budget-/kommittémotion, bana över tid), statustavla + kandidat-pipeline per kategori, öppna designfrågor, beslutslogg. Uppdateras per B-leverans. **§4.3 = kanonisk begreppsmodell (Kategori→Undermått→Indikator→Riktning) + mätbarhetskarta för samtliga 52 indikatorer.** |

---

## Varför den här prioriteringen

Rankingen drevs vid backloggens start mest av **A (aktivitet) + C (makt)**, eftersom **B krymps
mot neutralt** vid tunn täckning och D då var "ej tillämplig" i 21 av 56 celler. *(Uppdaterat
2026-06-12: D matas nu i **alla 7 kategorier** — 38/67 indikatorer, 28/35 undermått — och krymps
sedan 2026-06-12 efter **viktad undermåttsbredd** i stället för att renormalisera bort saknad
bredd, se [done/d_coverage_krympning_spec.md](done/d_coverage_krympning_spec.md). B är utrullad
med ≥2 undermått per kategori. Obalansen är alltså i stort åtgärdad; kvarvarande tyngdpunkt är
trovärdighets-/breddarbete, inte strukturella nollor.)*

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
- ✅ **D-bredd: `skjutningar_sprangningar`** (trygghet → grov brottslighet, riktning down): Polisens
  bekräftade skjutningar **+ sprängningar** (summan), nationell årstotal **2018–2025**. Polisen
  publicerar bara PDF per polisregion/år, så båda komponenterna är **transkriberade**
  ([config/skjutningar_sprangningar.yaml](../config/skjutningar_sprangningar.yaml)) enligt
  budget/SKR-mönstret — varje komponent/år korsverifierat (regionsumma == PDF:ens Totalt-rad) och
  auditerbart via [skjutningar_transcribe.py](../pipeline/tools/skjutningar_transcribe.py) (alla 8 år,
  båda serierna). Reader [polisen.py](../pipeline/sources/polisen.py) + golden-test + ur allowlisten.
  Preliminär (Polisens källnotis). Trygghets-D mäts nu även via grov brottslighet.
- ✅ **O2 — dist-snapshot/diff** ([score_diff.py](../pipeline/tools/score_diff.py)): reducerar
  scores.json till en kompakt baslinje (`dist/scores.snapshot.json`) och diffar ranking/betyg/flaggor
  mot den, så tysta betygsändringar mellan datauppdateringar syns. Golden-testat.
- ✅ **O3 — live smoke-test** ([test_sources_live.py](../tests/test_sources_live.py)): kontrollerar att
  SCB/Kolada/Energimyndigheten/Brå-endpoints svarar med förväntad form (fångar käll-/hash-drift).
  Opt-in (`ROSTA_LIVE=1`); CI kör plain pytest → skippas, förblir grön. **Spår O komplett (O1–O3).**

### Levererat (2026-06-05)

- ✅ **A1 — fler budgetår (2023 + 2024)** ([config/budget_ramar.yaml](../config/budget_ramar.yaml)):
  `a1` budgetprioritering går från **en mätpunkt (budget 2025) till ett snitt över tre budgetår
  (2023–2025)**, vilket fångar mandatperioden bredare och dämpar enårsbrus. Ramtalen för budget 2024
  (bet. 2023/24:FiU1 tabell 2.3) och 2023 (bet. 2022/23:FiU1 tabell 2.3) hämtades ur den officiella
  HTML-källan och **genererades programmatiskt** (aldrig handknappat) enligt samma transkriberings-/
  attributionsmönster som 2025. Attributionen är identisk struktur (Tidöregeringen M/KD/L + SD-stöd
  röstade Ja till rambeslutet, votering FiU1 punkt 2 båda åren; S/V/C/MP egna budgetmotioner) och
  roll-call-bekräftad. **Fyrlagrig adversariell verifiering** (den deferral-blockerande korruptions-
  risken i A löst): intern invariant per år (7/8 avvikelsetotaler på kronan; C-2023 +2 = källans egen
  totalrads-avrundning, jfr reg-totalens −1/−4/−3), oberoende parser (pandas, 0 avvikelser/270 celler),
  **Codex oberoende re-extraktion** (0 avvikelser, bekräftade roll-call + split-span-cell), samt
  reservationsstrukturen i källan. a1 aktiv för **7/7 kategorier** (snitt-skärning håller). Hela
  testsviten grön; `dist/` omräknat + snapshot-baslinjen uppdaterad (`score_diff --write`). Version 0
  (kräver fortfarande mänsklig slutgranskning som 2025). [Metod uppdaterad](fas1b_budget_metod.md).
  *Ny ranking (standardvikter): S 3,73 · L 3,33 · M 3,28 · MP 3,11 · KD 3,05 · C 2,66 · V 2,65 · SD 2,38.*
  *Caveat: ekonomi-a1 är nära oavgjort (alla ~23 %) → rang-noise; treårssnittet dämpar men löser ej
  modellegenskapen (se metoddok).*
- ✅ **B4-verktyg — anti-binär täckningsgrind** ([coverage_report.py](../pipeline/tools/coverage_report.py)
  `b_submeasure_spread()` + [test_fas4b_coverage.py](../tests/test_fas4b_coverage.py)): mäter hur många
  **distinkta undermått** som har AKTIV partikopplad B-evidens per kategori (åtgärdstyp med
  signed_direction≠0, ej coverage_exclude, **och** minst en partiståndpunkt → indikator → undermått) och
  flaggar **nära-binär** kategori (≤1 undermått). Speglar att `score.aggregate_B` är undermåttsviktat:
  vilar all aktiv evidens på ett undermått kan en enda ståndpunkt svinga b_raw mellan ytterlägen.
  Reproducerar BACKLOG-tabellen exakt (ekonomi 1/5, demokrati 1/5, valfard 2/4, forsvar 2/5,
  integration 2/5, trygghet 3/5, klimat 3/5). Grinden följer coverage_allowlist-mönstret: varje
  nära-binär kategori måste stå i nya `coverage_allowlist.b_near_binary_accepted` med skäl (annars tyst
  regression), och listan kan inte bära inaktuella poster (krymper när B2 levererar). **Fynd:** ekonomis
  realistiska B-mål är `bnp_produktivitet` + `realloner_hushall` (up-indikatorer) — inte
  inflation/offentliga finanser, som är **target-indikatorer utan B-bär riktning** (samma skäl som de
  uteslöts ur D). Hela sviten grön (167 passed). Återstår (=B2): faktiskt bredda liggaren.
- ✅ **B2 (första leveransen) — ekonomi/produktivitet via FoU-avdraget** ([evidence_ledger](../config/evidence_ledger.yaml)
  + [party_positions](../config/party_positions.yaml)): ny åtgärdstyp `fou_avdrag_skatteincitament` → indikator
  `produktivitet` (undermått bnp_produktivitet). Evidens: **Produktivitetskommissionen SOU 2025:96** + **SOU 2025:3**
  (authority_evaluation, medium/medium — riktningen FoU→produktivitet säker, men avdragets marginaleffekt ej
  kausalutvärderad). **8 partiståndpunkter votering-belagda** (bet. 2022/23:SfU19, prop. 2022/23:79 "höjt tak för
  FoU-avdraget" 600 000→1,5 mkr/mån, kammaren 2023-05-31): 7 Ja = **supports**, **V Nej = opposes** (reservation +
  kommittémotion 2022/23:2365). **Ekonomi 1/5 → 2/5 undermått med B-evidens — ej längre nära-binär** (ekonomi borttagen
  ur `b_near_binary_accepted`; B4-grinden tvingade fram det). Betygseffekt (förklarbar): V faller på ekonomi
  3,31→2,54 (dess tidigare topplacering var en nära-binär artefakt — ekonomi vilade på jobb-undermåttet där V var max),
  C stiger 1,26→2,04 (jobbsubventions-skeptisk men FoU-positiv). **Ny ranking: S > L > M > MP > KD > C > V > SD.**
  dist omräknat, snapshot re-baselinad, paket regenererat (priority 79), 167 tester gröna. Forskning→förslag→mänsklig
  sign-off 2026-06-05.
- ✅ **B2 (andra leveransen) — nytt ekonomi-undermått "Företagande och investeringar"** (modellutvidgning:
  [categories.yaml](../config/categories.yaml) + [IDEA.md](../IDEA.md) + [evidence_ledger](../config/evidence_ledger.yaml)
  + [party_positions](../config/party_positions.yaml) + [coverage_allowlist](../config/coverage_allowlist.yaml)):
  reallöner visade sig **ej B-bart** (Medlingsinstitutet: reallön sätts av parterna via Industriavtalet, drivs av
  produktivitet + Riksbankens inflationsmål → inget partistyrt icke-dubbelräknande instrument). I stället tillagt ett
  **6:e undermått** `foretagande_investeringar` (vikt 15; ekonomi-vikterna omfördelade 22/18/18/15/12/15) med indikator
  `naringslivets_investeringar` (up, SCB; allowlistad för D — konjunkturkänslig). Åtgärdstyp
  `konkurrenskraftig_foretags_och_agarbeskattning` → investeringar, evidens **Företagsskattekommittén SOU 2014:40**
  (authority_evaluation, medium/medium — investeringars skatteelasticitet empiriskt omtvistad). **BRED ram** (efter att
  smal bolagsskatts-ram visade sig gles, 4/1/3): 8 partiståndpunkter, ordagrant källbelagda via 8+3 parallella
  researchagenter mot fulltext — **5 supports** (M/SD/C/KD/L: lägre bolags-/ägarskatt) / **3 opposes** (S/V/MP: höja
  kapital-/företagsvinstskatt). **Ekonomi 2/6 → 3/6 täckta undermått** (av 4 B-möjliga: jobb, produktivitet, investeringar
  täckta; reallöner ej B-bart, inflation/offentliga finanser target). Betygseffekt: vänstern ner på ekonomi (S/MP
  −0,48, V −0,27), högern upp (C +0,27, KD/L +0,15). **Ny ranking: S > L > M > KD > MP > C > SD > V.** dist/snapshot/paket
  (priority 84) + 167 tester gröna. Forskning→förslag→mänsklig sign-off 2026-06-05.
- ✅ **B2 (tredje leveransen) — 4:e ekonomi-måttet: hushållens disponibla inkomst (värdeneutralt)** ([categories.yaml](../config/categories.yaml)
  + [evidence_ledger](../config/evidence_ledger.yaml) + [party_positions](../config/party_positions.yaml)): undermåttet **"Reallöner och
  hushållens ekonomi"** gjordes B-bart genom en ny ARBETANDE indikator `hushallens_reala_disponibla_inkomst` (up, SCB; `realloner`
  förblir vilande kontext/framtida D). **Ingen ny hink, ingen omviktning** — bara en indikator i befintligt undermått. Värdeneutral
  familj-åtgärdstyp `inkomststarkande_hushallspolitik` (skatte- och/eller transfereringsreformer som höjer disponibel inkomst),
  evidens **Fördelningspolitisk redogörelse april 2025** (descriptive_statistic/medium/high). **8 partiståndpunkter, alla supports**
  via sitt block-instrument (höger M/SD/C/KD/L: sänkt skatt på arbete; vänster S/V/MP: höjda transfereringar) — ordagrant källbelagda
  via 8 parallella agenter mot fulltext. **Löser tilt-problemet:** eftersom båda blocken kodas supports (en åtgärdstyp, coverage 4/4→5/5,
  ingen straff) får alla ett positivt köpkraftsbidrag, **störst lyft för dem investeringar-undermåttet tryckte ner** (V +0,26, C +0,17,
  MP/S +0,12) → späder ut högertilten. **Ekonomi 3/6 → 4/6 täckta undermått = "4 bra mått" nått, värdeneutralt.** Ny ranking:
  **S > L > M > KD > MP > C > V > SD.** dist/snapshot/paket (priority 87) + 167 tester gröna. Forskning→förslag→mänsklig sign-off 2026-06-05.
  *(Sparande/sparkvot avfärdat: target-likt + svag attribuering; reallöner kvar som vilande kontext.)*
- ✅ **B2 (fjärde leveransen) — demokrati: rättsstat/domstolarnas oberoende** ([evidence_ledger](../config/evidence_ledger.yaml)
  + [party_positions](../config/party_positions.yaml) + [coverage_allowlist](../config/coverage_allowlist.yaml) + [DATA.md](../DATA.md)):
  undermåttet **rattsstat_maktdelning** gjordes B-bart via åtgärdstyp `grundlagsskydd_domstolarnas_oberoende` → indikator
  `otillborlig_politisering` (down). Svensk primärkälla **prop. 2024/25:165 / SOU 2023:12 / bet. 2025/26:KU2**
  (authority_evaluation, medium/medium); **EU:s rättsstatsrapport 2024 endast som BEKRÄFTELSE** — dokumenterat
  KÄLLUNDANTAG i DATA.md (mellanstatliga Sverige-utvärderingar tillåtna som bekräftelse, ej primär, ej index; beslut 2026-06-05).
  **7 partiståndpunkter votering-belagda** (KU2 punkt 1, votering 3C8070DF, verifierat per parti mot data.riksdagen.se:
  S/M/C/V/KD/L/MP Ja = supports). **SD = none, EJ opposes** (SD:s Nej gällde enbart grundlagsändrings-PROCEDUREN
  RF 8 kap. 14/17/18 §§; reservationen avslår "i de delar den avser formerna för ändringar i grundlagarna" och antar
  domstolsoberoendet "som vilande … i övrigt"). **Demokrati 1/5 → 2/5 — ej längre nära-binär** (demokrati borttagen ur
  `b_near_binary_accepted`; listan nu tom). Betygseffekt: KD/M/V **+0,146**, MP +0,073 på demokrati; **SD −0,146** (ensam
  utanför → täckningsutspädning 2/3→2/4). Totalt KD/M +0,011, V +0,010, SD −0,011. **Ranking oförändrad: S > L > M > KD > MP > C > V > SD.**
  167 tester gröna, ruff rent. Forskning→verifiering→sign-off 2026-06-05.
  *(medier UNDERKÄNT: EMFA-medielagen togs med acklamation, enda voteringen (KU12 p2) gällde SD:s grundlagsreservation om
  TF/YGL-företräde — ej mediefrihet → ej differentierbart. transparens + personlig frihet HÅLLS: vänster-tilt resp. hög
  tilt; jakt på fler värdeneutrala demokrati-mått pågår, se B2 nedan.)*
- ✅ **B2 (femte leveransen) — demokrati: personlig frihet (blocköverskridande, Lagrådet-ankrat, codex-granskat)** ([evidence_ledger](../config/evidence_ledger.yaml)
  + [party_positions](../config/party_positions.yaml)): undermåttet **personlig_frihet** gjordes B-bart via åtgärdstyp `begransa_biometrisk_realtidsovervakning_rattssakerhet` → indikator
  `overvakning_utan_rattssakerhet` (down). Källa: **Lagrådets yttrande över prop. 2025/26:150** (Polisens AI-ansiktsigenkänning i realtid),
  ordagrant i bet. 2025/26:JuU28 — Lagrådet: förslaget "går avsevärt längre än nödvändigt" och "står därmed i strid med grundlag"
  (helsvensk källa, inget int. undantag behövs). **8 partiståndpunkter votering-belagda** (JuU28, verifierat per parti): **supports = C**
  (avslog hela lagen, punkt 1), **V + MP** (krävde rättssäkerhetsgarantier, punkt 2/3); **opposes = S, M, SD, KD, L** (röstade för lagen
  + mot garantierna → `_FLIP` → negativt B). **BLOCKÖVERSKRIDANDE split** (S ligger med högern → ej vänster-höger, ej regering-vs-opposition;
  den frihetliga dissidenten är mittenpartiet C). **Detta är det första DIFFERENTIERANDE demokrati-måttet.** Förkastade alternativ:
  transparens/offentlighetsprincip (codex: dubbelräkning mot befintlig `starkt_oberoende_granskning_och_insyn`-bunt), medier (acklamation/
  regeringslägesartefakt). Betygseffekt (demokrati): C/V/MP upp (V +0,23, MP +0,12), S/M/SD/KD/L ner (S/L/SD −0,5…−0,6). **Totalt ±0,04,
  ranking oförändrad: S > L > M > KD > MP > C > V > SD.** Demokrati **2/5 → 3/5**. 167 tester gröna, ruff rent. codex-rescue-granskad ("BYGG
  med ändring": bred policyfamilj, Lagrådet som huvudankare, C egen mapping_note, confidence=medium). Forskning→codex→sign-off pågår 2026-06-05.
- ✅ **B2 (sjätte leveransen) — försvar: Nato-medlemskap** ([evidence_ledger](../config/evidence_ledger.yaml)
  + [party_positions](../config/party_positions.yaml)): undermåttet **nato_ukraina** (tidigare 0 B-täckning) gjordes B-bart via
  åtgärdstyp `nato_medlemskap` → indikator `nato_interoperabilitet` (up). Källa: **Försvarsberedningen Ds 2024:6**
  (authority_evaluation, high/high; "Nato-medlemskap ökar säkerheten … ger interoperabilitet och förmåga att operativt agera
  gemensamt"). **Votering bet. 2022/23:UU16 p1** (Sveriges Nato-anslutning), verifierat per parti: **supports S/M/SD/C/KD/L**,
  **opposes V** (fortsatt Nato-kritiskt). **MP = none** (codex-granskat: MP röstade Nej 2022 men har svängt till Nato-stöd →
  opposes vore föråldrat/vilseledande). Blocköverskridande (S på Ja-sidan med högern). Effekt: C/KD +0,146 i försvar; V −0,375
  (flippad); MP oförändrat; **ranking oförändrad: S > L > M > KD > MP > C > V > SD**. Försvar **2/5 → 3/5**. 167 tester gröna, ruff rent.
- 🟡 **B2-natt 2026-06-06 — välfärd/trygghet/klimat/integration: 0 byggda, kandidatlistor för diskussion.** Systematisk research
  (alla röstsiffror verifierade mot data.riksdagen.se) av de B-bara otäckta undermåtten gav **inget värdeneutralt votering-mått** i
  fyra kategorier. **Genomgående vägg:** den faktiska sakreformen tas med **acklamation** (brett stöd → ingen namnvotering att
  partikoppla), medan de namnvoteringar som finns gäller "avslå oppositionens mer-krav" → **regering-vs-opposition eller
  vänster-höger-tilt**. Per regeln *neutralitet före 4* byggdes inget. Kandidatlistor (källkollade, med exakt skäl till förkastande)
  per undermått finns i nattens forskningsanteckningar — kondenserat:
  - **välfärd/vard_tillganglighet:** `nationell_vardformedling` (alla för, men votering fångar bara C:s utformningsnyans; byggbar bara via 8 motioner = all-supports/låg differentiering). Övriga (vårdplatser, SVF, vårdgaranti) = omnibus-tilt eller mixed svensk evidens (RiR 2023:12).
  - **välfärd/omsorg_personal:** riktnings-ankare klart (Socialstyrelsen), men instrumenten (Äldreomsorgslyftet, kompetensplan) splittrar rakt vänster-höger; konsensuspunkter = acklamation. (D-not: SKR lade ned kontinuitetsstatistiken; nytt mått 2027.)
  - **trygghet/rattsvasendets_effektivitet:** `snabbforfarande_lagforing` = bäst evidens (Brå 2020:3) men acklamation; `kronvittnen` (JuU35) = bäst votering (7 Ja/V Nej, blocköverskridande) men utanför tidsfönstret + bara prop-källa + fel indikator. (forebyggande-undermåttet saknar indikator → ev. modellutvidgning.)
  - **klimat/biologisk_mangfald:** skyddsåtgärder = acklamation; namnvoteringar = "avslå mer-ambition" = grön-axel-tilt. `invasiva_frammande_arter` möjlig motion-baserad all-supports (riktning hårt belagd, Naturvårdsverket) men bunten-problem.
  - **integration/boendesegregation + normer_tillit:** kategorins egen caveat ("stor risk för ideologisk bias") bekräftad i praktiken — värdeneutrala åtgärder (hedersvåld, samhällsorientering, segregationsåtgärder) tas i acklamation; namnvoteringar = bostads-/hyrespolitik eller S-/C-ensam = tilt.
  - **försvar/genomforbarhet_leverans:** riktning klar (SOU 2022:24), men materielpunkter = acklamation; namnvoteringar buntade (Israel-vapenexport, Saab-ägande) eller budgettiltade.
- ✅ **O4 — reproducerbar dist** ([pipeline/scorerun.py](../pipeline/scorerun.py)): `dist/scores.json`
  + `dist/evidence.json` var **icke-deterministiska mellan körningar** — claims byggdes i hash-
  randomiserad ordning, så `claim_refs` (provenanspekare) bytte ordning *och* `obs_by_cat[:3]`-urvalet
  pekade på olika 3 observationsclaims per process. Betygen var alltid deterministiska; bara
  provenansen drev. Fixat genom att sortera claims på id + `sort_keys` på JSON-utskriften → dist är nu
  **byte-identisk över processer** (verifierat med olika `PYTHONHASHSEED`). Upptäckt under A1-omräkningen;
  stärker O2-snapshot/diff (ingen falsk drift av ordningsbrus).
- ✅ **B2 (sjunde+åttonde leveransen) — enhällighet-som-källa: trygghet + klimat → 4/5** ([evidens_trovardighet.md](done/evidens_trovardighet.md)
  + [evidence_ledger](../config/evidence_ledger.yaml) + [party_positions](../config/party_positions.yaml)): den nya **tvåstegsmetoden**
  (måttet ≠ positioneringen; acklamation slår bara ut *voteringskällan*, ett **enhälligt betänkande** belägger att alla 8 partier står bakom)
  byggde de två mått som var "väggade" under natten. **(7) `snabbforfarande_lagforing` → `handlaggningstid`** (trygghet, undermått
  rattsvasendets_effektivitet 3/5 → **4/5**): Brå 2020:3 (handläggningstid i tingsrätt ca −40 %, total "mer än halverats"); enhälligt
  bet. 2022/23:JuU2 punkt 1 (acklamation; enda reservationen V/C/MP gäller punkt 2/påföljd och "välkomnar" snabbförfarandet) → **alla 8 supports**;
  authority_evaluation/medium/medium; **codex BUILD-WITH-CHANGES**. **(8) `atgarder_mot_invasiva_frammande_arter` → `hotade_arter_naturforlust`**
  (klimat, undermått biologisk_mangfald 3/5 → **4/5**): Naturvårdsverket (förteckningen "ett verktyg i arbetet med att förebygga och begränsa
  spridningen av arter som kan orsaka skador på ... biologisk mångfald"); enhälligt bet. 2025/26:MJU13 punkt 1 (acklamation, "inte väckts någon
  motion som går emot"; tiltade p2 utesluten) → **alla 8 supports**. **⚠️ FLAGGAD:** codex förordade HOLD (instrument-precision på rubrikcitatet) →
  byggt som **version 0 med konservativ kalibrering authority_evaluation/low/low** + instrument-mekanismcitat; **din sign-off avgör om det behålls**.
  Båda är **icke-rankningsdrivande konsensus-mått** (alla supports → likformigt lyft, inget parti straffas): trygghet +0,04…+0,13, klimat +0,07…+0,20.
  **5 andra kandidater HOLD** (vård, omsorg, normer_tillit, boendesegregation, försvar-leverans — steg-1-evidens saknas/mixed eller fel konstrukt; se
  evidens_trovardighet.md §6–§7). 36 evidensposter / 192 ståndpunkter; scorerun + B4 (inga nära-binära) + 167 tester gröna + ruff rent; granskningspaket
  priority 93; **snapshot ej re-baselinad** (kumulativ drift syns). Forskning (4+3 agenter) → codex → bygge 2026-06-06; väntar mänsklig sign-off.
- ✅ **B2 (nionde leveransen) — demokrati: lagstadgat oberoende public service (enhällighet, codex-granskat)** ([evidence_ledger](../config/evidence_ledger.yaml)
  + [party_positions](../config/party_positions.yaml) + [evidens_trovardighet.md](done/evidens_trovardighet.md)): undermåttet **yttrandefrihet_medier** (tidigare B-tomt)
  gjordes B-bart via åtgärdstyp `lagstadgat_oberoende_public_service` → indikator `mediefrihet` (up). Instrument: för första gången regleras
  public service-uppdraget I LAG (ny lag om public service) med lagstadgat oberoende. Källa **prop. 2024/25:166** (ur 2023 års **parlamentariska**
  public service-kommitté, **SOU 2024:34** "Ansvar och oberoende") — instrument-mekanism (prop. 5.2.1): public service "ska bedrivas självständigt i
  förhållande till såväl staten som olika ekonomiska, politiska och andra intressen … oberoende och stark integritet". **8 partiståndpunkter via
  enhälligt bet. 2025/26:KrU2 punkt 1** (acklamation, votering-API tomt @antal=0, "inte väckts någon motion som går emot att riksdagen antar regeringens
  lagförslag"; samtliga 15 reservationer gäller punkt 2–14 → ingen mot p1) → **alla 8 supports** (S/M/SD/C/V/KD/L/MP). **Codex: BUILD-WITH-CHANGES**
  (mekanism-/designflagga; snäv formulering lagstadgat oberoende → mediefrihet; behåll authority_evaluation/**low/low** — ingen ex-post-effektutvärdering).
  **Demokrati 3/5 → 4/5.** Icke-rankningsdrivande konsensus-mått: isolerad effekt demokrati +0,0…+0,20/parti (alla supports), total +0,0…+0,015,
  **ranking oförändrad**. 37 evidensposter / 200 ståndpunkter; scorerun + B4 (inga nära-binära) + 167 tester gröna + ruff rent + 0 cyrilliska; paket
  regenererat. **snapshot ej re-baselinad.** Samma dag: **djupsvep §5.8** på forsvar/valfard/integration (7+11+11 instrument, 4 parallella agenter) →
  **HOLD ×5 bekräftat** med skärpta återöppningsvillkor (se evidens_trovardighet.md §6); väg till 4 undermått där kräver modellutvidgning → sign-off.
- ✅ **B-GRÖN-SVEPET 2026-06-07 (användarmandat: varje undermått ≥1 B-grön; nya indikatorer autonomt som v0)** — 11 parallella
  researchagenter + codex adversariell granskning → **5 mått byggda v0** (alla enhällighet-som-källa §5.2, alla 8 supports,
  acklamation verifierad mot data.riksdagen.se dokumentstatus, citat verbatim, low/low, FLAGGADE för sign-off):
  **(1)** `insyn_partifinansiering` → politisk_transparens (demokrati, lagen 2018:90/KU19 p1) → **demokrati 5/5 FULLT**;
  **(2)** NY indikator `forsvarsfinansiering_upptrappning_mot_mal` ← `upptrappning_forsvarsanslag_mot_mal` (forsvar, FöU2 p1+p5) → **forsvar 4/5**;
  **(3)** NY indikator `kommunalt_brottsforebyggande_arbete` ← `lagstadgat_kommunalt_brottsforebyggande_ansvar` (trygghet, lagen 2023:196/JuU9 p1) → **trygghet 5/5 FULLT**;
  **(4)** `koncentration_nationell_hogspecialiserad_vard` → overlevnad_svar_sjukdom (valfard, SOU 2015:98/SoU18 p1);
  **(5)** NY indikator `kontinuitet_i_omsorgen` ← `fast_omsorgskontakt` (valfard, prop. 2021/22:116/SoU24 p2) → **valfard 4/4 FULLT**.
  **5 HOLD** (genomforbarhet_leverans, industriell_konkurrenskraft, boendesegregation, normer_tillit, migrationssystem — genuina
  väggar; konkreta kandidat-indikatorer för sign-off) + **offentliga_finanser HOLD-kontext** (codex: åtstramnings-tilt). Inflation kontext.
  42 evidensposter / 240 ståndpunkter; **isolerad effekt: ranking OFÖRÄNDRAD** (S>L>M>KD>MP>C>SD>V), alla cellförändringar positiva (inget
  parti straffat — omöjligt att tilta då alla supports); ruff rent, 167 tester gröna, B4 inga nära-binära, 0 cyrilliska i config.
  snapshot ej re-baselinad. **Fullständig leverans + sign-off-frågor: [evidens_trovardighet.md §8.7](done/evidens_trovardighet.md).** Väntar mänsklig sign-off.

- ✅ **INTEGRATION-SVEPET 2026-06-07 (användarfokus: fyll integrations otäckta undermått; metodpoäng: negativ evidens lika giltig som positiv)**
  — 3 researchagenter (5 förslag/undermått) + per-parti-verifiering mot data.riksdagen.se + codex adversariell granskning.
  **1 byggt v0 (FLAGGAT):** NY indikator `atervandande_effektivitet` ← `se_over_ansvarsfordelning_atervandande` (migrationssystem, RiR 2020:7 —
  splittrad återvändandestruktur kostar/ineffektiv; **negativ-evidens-vinkeln**). **Genuin tvåsidig split** (appens första differentierande
  integration-B-mått, ej enhällighet): bet. 2020/21:SfU6 p2, votering verifierad → supports M/KD/SD/C/L, opposes S/MP, V none. Codex
  **KEEP-WITH-CHANGES** (snävade policy_type "samla"→"se över ansvarsfördelning"; tidsnot 2020/21). → **integration 2/5 → 3/5.**
  **2 HOLD:** `boendesegregation` (kamera-väg byggd → REVERTERAD, codex KILL: trygghet-relabel + dubbelräknar situationell_prevention_kamerabevakning +
  exakt §8.7-varningen + 7-1≈noll diff) + `normer_tillit` (Delmi 2025:5 löser steg 1, inget neutralt steg-2-ankare; nedstigning #2/#3/egna wall).
  43 evidensposter / 247 ståndpunkter; **isolerad effekt: ranking OFÖRÄNDRAD** (S>L>M>KD>MP>C>SD>V), endast integration rörd (S −0,063, MP −0,044,
  M/SD/L +0,04…0,09 — korrekt riktningsmönster för systemeffektivitet); 167 tester gröna, ruff rent, 0 cyrilliska. snapshot ej re-baselinad.
  **Sign-off-frågor: [evidens_trovardighet.md §8.7](done/evidens_trovardighet.md).** Väntar mänsklig sign-off.

- ✅ **SPÅR D — Tier 1: ekonomi-D till full submåttstäckning 2026-06-07 (v0, FLAGGAD; tracker [spar_D_datatackning.md](spar_D_datatackning.md))** —
  två SCB-NR-serier byggda (§5.1 B-only-beslutet hävt, din sign-off): **(1)** `naringslivets_investeringar` (ekonomi → foretagande_investeringar, up)
  ur SCB NR **TAB3610** Anvandningstyp=`BNAR` (näringslivets fasta bruttoinv, **fasta priser** ref 2020), ren `SCB_SERIES`-post, 1980–2024;
  **(2)** `hushallens_reala_disponibla_inkomst` (ekonomi → realloner_hushall, up) som kumulativt **realindex** ur SCB:s officiella reala tillväxttakt
  (NR **TAB4592** `B6nRealGrowth`/`S14`), ny `derived.py`-op `index` med drift-skydd på föräldra-tillväxtserien, 1951–2025. **Ekonomi 2 → 4 D-täckta
  submått (alla 4 D-bara täckta);** total D-täckning **19 → 21/56**. Dimensionskoder **live-verifierade** (ej gissade); `expect`-grindar passerade;
  golden-test för `compute_index`; **adversariell teckenkontroll** (Tidö-partierna bär investeringsnedgången 2023–2024, JÖK-eran tillväxten;
  real-inkomstfallet 2023 principiellt fördelat). **Isolerad effekt: endast ekonomi rörd, +0,007…+0,074/parti, ranking OFÖRÄNDRAD** (S>L>M>KD>MP>C>SD>V);
  V/ekonomi NA korrekt. 170 tester gröna (+3 nya derived-tester), ruff rent, 0 främmande tecken. Coverage-strängen rättad (trygghet var felaktigt listad D-tom). snapshot
  re-baselinad + committad 2026-06-07 (`data:`-commit). v0 kvarstår tills formell granskning bumpar v0→v1.

- ✅ **SPÅR D — Tier 2: `sfi_sprakkunskaper` → integration får sin första skola_sprak-D 2026-06-07 (v0, FLAGGAD; tracker [spar_D_datatackning.md](spar_D_datatackning.md))** —
  andel personer **godkända i sfi** (%, riktning up) ur SCB:s officiella sfi-statistik **TAB1814** ContentsCode `AA0003EB`, 1997–2023 (27 obs). Visade sig vara
  **S, inte M:** SCB (producenten) exponerar serien som ren PxWeb v2 → befintliga `scb.py`-adaptern räckte, ingen Skolverket-portaladapter behövdes (allowlistens
  "ej ren PxWeb"-antagande överspelat). **§5.2-semantiken avgjord av datan:** TAB1814 har båda §5.2-måtten som var sin ContentsCode — godkäntandel (`AA0003EB`, up) och
  vistelsetid-median (`AA0003EC`, down = progressionen); bara godkäntandel matchar indikatorns kanoniska riktning. **Metodbrott 2022** (G/I/– + cutoff 1 jan) hanterat
  genom att behålla hela serien (sign-only D robust mot magnitudskiftet; brott-övergångarna teckenkonsistenta med trenden). **Integration 2 → 3 D-täckta submått
  (skola_sprak öppnat);** total D-täckning **21 → 22/56**. **Adversariell teckenkontroll:** sfi-godkäntandelen föll 2015→2020 under S+MP → S net −0,49 / MP −0,65
  (genuint negativt integrationsutfall på deras vakt); Tidö-partierna +1,0 men tunt underlag (ej överkrediterade); V = NA. **Isolerad effekt: endast integration rörd**
  (S −0,060, MP −0,079, M/KD/SD +0,067), TOTAL ±0,004…0,008, **ranking OFÖRÄNDRAD** (S>L>M>KD>MP>C>SD>V). ≈170 tester gröna, fas3-gate-invarianten håller. v0.
- ✅ **SPÅR D — Tier 4: `personal_varnpliktiga` → FÖRSVARET FÅR SIN FÖRSTA D 2026-06-07 (v0, FLAGGAD; tracker [spar_D_datatackning.md](spar_D_datatackning.md))** —
  antal värnpliktiga som **påbörjade grundutbildning** per kalenderår (riktning up) ur **Försvarsmaktens årsredovisning**, 2018–2025 (8 obs, 3 750→8 136). **Fyllde den
  strukturella nollan forsvar (0 → 1 D-täckt submått, militar_formaga); 6/7 kategorier har nu D (bara demokrati kvar). Total D-täckning 22 → 23/56.** **Designbeslut
  "varför inte båda" (sign-off):** FM (kalenderårsrent förmågemått) = värdebärande serie, **Plikt- och prövningsverkets inskrivna = oberoende korsverifiering** varje år
  (≤~3 %); avgörande att BÅDA myndigheterna visar samma enda nedgång 2021→2022 (den enda teckenkänsliga D-övergången). Transkriberad config (FM:s/Pliktverkets ÅR-PDF:er ej
  maskinläsbara) + ny adapter `pipeline/sources/forsvarsmakten.py` + auditverktyg `tools/varnpliktiga_audit.py`. **Adversariell teckenkontroll (matchar handberäkning
  exakt):** uppbyggnaden skedde under både S-ledda och Tidö-regeringar → alla ansvarspartier positiv försvars-D (S +0,58/MP +0,53 bär 2018–2021-rampen + 2022-dippen;
  M/KD/SD +1,0 Tidö-eran; L +0,75; C +0,36); **V = NA** (aldrig regering). **Isolerad effekt: endast forsvar rörd** (kategori +0,09…+0,25, TOTAL +0,014…+0,038),
  **ranking OFÖRÄNDRAD** (S>L>M>KD>MP>C>SD>V). Hela testsviten grön (8 nya golden + fas3-gate). **Källgräns v0:** 2018+2025 direkt ur FM ÅR, 2019/2021/2022/2024 korsverif.
  Pliktverket, 2020+2023 (inre monotona punkter) via Wikipedias FM-ÅR-citerade tabell → v1 vid direkt PDF-transkribering.
- ✅ **SPÅR D — Tier 4: `fortroende_domstolar_myndigheter` → DEMOKRATIN FÅR SIN FÖRSTA D 2026-06-07 (v0, FLAGGAD; tracker [spar_D_datatackning.md](spar_D_datatackning.md))** —
  andel med ganska/mycket stort **förtroende för rättsväsendet som helhet** (domstolar + polis/åklagare/kriminalvård, riktning up) ur **Brå NTU blad 5A:1**, 2017–2025
  (9 obs, 44→54 %). **Fyllde den sista strukturella nollan demokrati (0 → 1 D-täckt submått, korruption_tillit); ALLA 7 kategorier har nu D — exit-kriterium §6.2 uppfyllt.
  Total D-täckning 23 → 24/56.** **Källval S inte L (samma mönster som sfi):** trackern antog SOM (akademiskt, L-transkribering), men Brå NTU — *officiell* källa — har
  serien som ren xlsx via den BEFINTLIGA `bra.fetch_ntu`-adaptern; dessutom kräver CLAUDE.md officiell källa när sådan finns (akademiskt bara "när officiell saknas") →
  SOM otillåtet här. Adaptern generaliserades så NTU-serier bär egen kategori (`bra.INDICATOR_CATEGORY`). **Scope 5A:1 (rättsväsendet helhet) = trognaste matchning för
  "domstolar_myndigheter"; icke-konsekvent val** (5D:1 domstolarna ger samma kvalitativa D → korsverifiering). **2017-fönster** (NTU 2017-metodbrott, samma som otrygghet).
  **Adversariell teckenkontroll (matchar handberäkning exakt):** förtroendet steg under båda block → alla ansvarspartier positiv demokrati-D (MP +0,80 högst, lämnade före
  2022→2023-dippen; SD/M/KD +0,81 Tidö; L +0,76; C +0,67; S +0,55 bär längsta fönstret + dippen); **V = NA**. **Isolerad effekt: endast demokrati rörd** (+0,139…+0,203,
  TOTAL +0,010…+0,015), **ranking OFÖRÄNDRAD** (S>L>M>KD>MP>C>SD>V). Generaliserad adapter golden-testad (NTU-fixtur fick 5A:1), hela sviten grön, ruff rent.

### Levererat (2026-06-07 … 2026-06-12) — sammanfattning, detaljer i trackern

- ✅ **Spår D-expansionen** (tracker: [spar_D_datatackning.md](spar_D_datatackning.md), svep/natt-
  rapporter arkiverade i [done/](done/)): 24/56 → **38/67 inlästa indikatorer, 28/35 undermått,
  alla 7 kategorier** — bl.a. försvar 1/5 → 3/5 (forsvarsvilja, personalstyrka, ukraina_stod),
  demokrati 1/5 → 5/5 (V-Dem-index ×4), integration 5/5, aterfall_i_brott, overlevnad_svar_sjukdom,
  hackande_faglar_skog. Allt v0, per-indikator `data:`-commits.
- ✅ **D-täckningskrympning (2026-06-12)** ([done/d_coverage_krympning_spec.md](done/d_coverage_krympning_spec.md)):
  D krymps mot neutral efter **viktad icke-target-undermåttsbredd** per (parti, kategori) i stället
  för att renormalisera bort saknad bredd. `D_coverage_<täckt>/<total>` + `D_thin_coverage`-flagga
  (tröskel 0,75) + säkerhetssteg; **D-breddgrind** enligt allowlist-mönstret
  (`coverage_allowlist.d_thin_breadth_accepted`, i dag endast försvar 70/100;
  [test_d_breadth_gate](../tests/test_d_breadth_gate.py)); `coverage_report` visar D-bredd per
  kategori. Diff granskad + godkänd: ingen rankingändring, totaler −0,008…−0,017. **Sidospår öppnat:**
  det parallella B-breddsproblemet (spec §8) — en extra B-undermåttskrympning riskerar dubbelrabatt
  och ska specas separat nu när D-ändringen är mätt (se Spår B nedan).

### Status per spår — ögonblicksbild 2026-06-04/05 (D- och B-raderna delvis överspelade; aktuellt D-läge i [spar_D_datatackning.md](spar_D_datatackning.md))

| Spår | Status |
|------|--------|
| **D** (datatäckning) | **Egen tracker: [spar_D_datatackning.md](spar_D_datatackning.md).** uppklaringsgrad + skjutningar/sprängningar (2026-06-03) + **Tier 1 ekonomi: naringslivets_investeringar + hushallens_reala_disponibla_inkomst (2026-06-07, v0)** + **Tier 2: sfi_sprakkunskaper (SCB TAB1814, integration→skola_sprak, 2026-06-07, v0)** + **Tier 4: personal_varnpliktiga (Försvarsmaktens ÅR, forsvar→militar_formaga) + fortroende_domstolar_myndigheter (Brå NTU 5A:1, demokrati→korruption_tillit), 2026-06-07, v0 — FÖRSVARETS + DEMOKRATINS FÖRSTA D** levererade → **24/56 D-serier i ALLA 7 kategorier (ingen längre D-tom; båda strukturella nollorna fyllda, exit-§6.2 ✅); ekonomi 4/4 D-bara, integration 3/5, försvar 1/5, demokrati 1/5 submått**. *(sfi: §5.2 avgjord av datan. varnpliktiga: "varför inte båda" = FM + Pliktverket korsverif. domstolsförtroende: S inte L — Brå NTU officiell krävs framför SOM akademisk.)* Återstående D-källor **uttömda/blockerade eller kräver M/L-bygge** (se [coverage_allowlist](../config/coverage_allowlist.yaml) + tracker Tier 3): overlevnad annuell (Socialstyrelsen, M, §5.3), realloner (Medlingsinstitutet, M, låg prio), Svk-derived klimat (gränsfall källregel, öppnar inget D-löst submått), samt blockerade (återfall PDF, handläggning interaktiv DB, demokrati int. index förbjudna, försvar sekretess). **De rena SCB/Kolada-årsserierna skördades i Fas 2–3; resten kräver ny adapter, transkribering, eller är otillåten.** |
| **B** (evidens) | ✅ **B1 expertgranskad + sign-off 2026-06-05 → `version 1`** (se B1 nedan): party_positions (4 SUSPECT + 79-raders screening) och evidence_ledger (30 poster triade, 6 fixar) genomgångna; skarp betygsättning aktiverad. **B4-verktyg/grind ✅** + **B2 ekonomi ✅** (4/6) + **B2 demokrati ✅** (rättsstat: grundlagsskydd domstolarnas oberoende, votering KU2; personlig frihet: begränsa biometrisk realtidsövervakning, votering JuU28/Lagrådet, codex-granskat) levererade 2026-06-05 → demokrati **1/5 → 3/5**, **inga nära-binära kategorier kvar** (`b_near_binary_accepted` tom). Återstår otäckta (ej blockerare): transparens_ansvar (offentlighetsprincip = dubbelräkning, skippat) + yttrandefrihet_medier (acklamation/regeringslägesartefakt) — inget värdeneutralt mått funnet utan tilt/dubbelräkning. **Natt 2026-06-06:** B2 utvidgad till de 5 övriga kategorierna — **1 byggt** (forsvar/nato_medlemskap → försvar 3/5); välfärd (2/4), trygghet (3/5), klimat (3/5), integration (2/5) gav **0 rena mått** (alla föll på "sakreform=acklamation / namnupprop=vänster-höger-tilt"); kandidatlistor för morgondiskussion (se B2-natt-blocket nedan). **Dag 2026-06-06 (enhällighet-som-källa, [evidens_trovardighet.md](done/evidens_trovardighet.md)):** den nya tvåstegsmetoden (måttet ≠ positioneringen; acklamation slår bara ut *voteringskällan*, enhälligt betänkande = alla 8 supports) byggde **2 till** — **snabbforfarande → trygghet 4/5** och **invasiva arter → klimat 4/5** (FLAGGAD, codex förordade HOLD). 5 andra kandidater HOLD (steg-1-evidens saknas/mixed). 36 evidensposter / 192 ståndpunkter; 167 tester gröna. |
| **A** (agerande) | **A1 (fler budgetår) ✅ LEVERERAD 2026-06-05** — budget 2023 + 2024 tillagda (snitt över 3 år), fyrlagrigt adversariellt verifierat (invariant + pandas + Codex + roll-call); se Levererat ovan. Korruptionsrisken som blockerade solo-körningen löstes via den oberoende cell-för-cell-kontrollen. A2 (votering→A) är en designfråga (viktning utan dubbelräkning av a2) → kräver beslut, deferrad. |
| **C** (ansvar) | c2 finansiering uppskjutet (designbeslut, ej neutralt byggbart). C2 (mandatperiodskiften) + C3 (subnationell D) är modellutvidgningar utanför ren databredd → deferrade. |
| **F** (frontend) | F1 (extern hosting) **blockerad** — kräver dina credentials/hosting-beslut (utåtriktad publicering gör jag inte autonomt). F2 (manuell skärmläsartest) kan bara göras av människa. |
| **O** (drift/ops) | ✅ **Komplett** (O1 drift-skydd, O2 snapshot-diff, O3 live-smoke-test, **O4 reproducerbar dist** — 2026-06-05). |

**A1-plan — ✅ UTFÖRD 2026-06-05.** Partiernas utgiftsramar per UO för budget **2024** (bet. 2023/24:FiU1
tabell 2.3) och **2023** (bet. 2022/23:FiU1 tabell 2.3) lades till, samma tabell-/källrads­mönster som
budget 2025. Den **interna invarianten** (partiernas avvikelser summerar till källans totaler på kronan)
verifierades per år (7/8 på kronan; C-2023 +2 = källans totalrads-avrundning), tillsammans med en oberoende
parser (pandas) och en oberoende adversariell cell-för-cell-kontroll via **Codex** (0 avvikelser) **innan**
det matade A. a1 är nu ett snitt över 3 budgetår i stället för en mätpunkt. *Den ursprungliga deferralen
("görs inte solo övernatten p.g.a. korruptionsrisken i A") upphävdes eftersom den oberoende verifieringen
nu utfördes — det var precis det villkoret planen ställde.*

---

## Spår D — Datatäckning (utfall, delpoäng D)

> **📍 Aktiv tracker:** [spar_D_datatackning.md](spar_D_datatackning.md) — utbruten arbets-/
> trackinglogg för Spår D (verifierat nuläge, byggbarhetsverdikt per indikator, öppna beslut,
> exit-kriterier). Flyttas till `docs/done/` när spåret är klart. Vågtabellerna nedan behålls
> som översikt; trackern är sanningskällan för status.

Mål: fler kanoniska årsserier som matar D-attributionen, så fler kategorier/undermått mäts på
faktiskt utfall. Alla nya serier ska vara kanoniska (finnas i `categories.yaml` med rätt
riktning) och annuella, så de matar `category_d` automatiskt.

### Våg 1 — billig bredd (återanvänder befintliga mönster) ✅ AVSLUTAD 2026-06-09

| Indikator | Kategori → undermått | Utfall |
|-----------|--------------------|--------|
| ~~`uppklaringsgrad`~~ ✅ | trygghet → rättsväsendets effektivitet | inläst 2026-06-03 (Brå 10La) |
| `handlaggningstid` 🔴 | trygghet → rättsväsendets effektivitet | vägg (sonderat 2026-06-03: interaktiv DB/PDF, ingen maskinläsbar serie) — allowlistad `future` |
| ~~`aterfall_i_brott`~~ ✅ | trygghet → återfall/kriminalvård | inläst 2026-06-09 (Kriminalvården KOS Tabell 6.1, transkriberade råtal) |
| ~~`skjutningar_sprangningar`~~ ✅ | trygghet → grov brottslighet | inläst 2026-06-03 (Polisen, transkriberad) |
| ~~`overlevnad_svar_sjukdom`~~ ✅ | välfärd → vård tillgänglighet | inläst 2026-06-08 (Kolada U70471, 30-dagarsöverlevnad) |
| `vard_i_tid` ⛔ | välfärd → vård tillgänglighet | stängd som `low_value` (Kolada U79142 avslutad 2023 + dubblerar vardkoer) |

Trygghet gick därmed till 4/5 D-täckta undermått (förebyggande saknar indikator); välfärd 3/4.
Detaljer + verifiering i [spar_D_datatackning.md](spar_D_datatackning.md).

### Våg 2 — nya adaptrar (källa finns men ej rent öppet API) ⚪

| Indikator | Kategori → undermått | Källa & metod | Effort | Tag |
|-----------|--------------------|---------------|--------|-----|
| `realloner` | ekonomi → reallöner/hushåll | Medlingsinstitutets konjunkturlönestatistik (helekonomi-löneindex; SCB:s API saknar ren serie) | M | future |
| ~~`sfi_sprakkunskaper`~~ ✅ | integration → skola/språk | SCB **TAB1814** `AA0003EB` (andel godkända i sfi %) — ej Skolverket-portal, SCB-PxWeb räckte | **S** | ✅ **inläst 2026-06-07 (Tier 2, v0); §5.2 avgjord (godkäntandel)** |
| *(Svk-källadapter)* | klimat (förkrav för Våg 3-härledda) | Svenska kraftnät, öppna data (spotpris/effektbalans) | M | derived-förkrav |

### Våg 3 — härledda + design­krävande ⚪🟣

| Indikator | Kategori → undermått | Metod | Effort | Tag |
|-----------|--------------------|-------|--------|-----|
| `elprisvolatilitet` | klimat → energi/elpriser | härled ur Svk spotpris (`derived.py`-mönster) | S (efter Svk-adapter) | derived |
| `effektbrist` | klimat → energi/elpriser | härled ur Svk effektbalans | S (efter Svk-adapter) | derived |
| `utslappsminskning_per_krona` | klimat → kostnadseffektivitet | utsläpp ÷ klimatutgift (flera serier) | M | derived |
| ~~`personal_varnpliktiga`~~ ✅ | försvar → militär förmåga | **Försvarsmaktens ÅR** (antal påbörjade GU/år 2018–2025), korsverif. mot Pliktverkets inskrivna — transkribering m. källrad (PDF:er ej maskinläsbara) | L | ✅ **inläst 2026-06-07 (Tier 4, v0); FÖRSVARETS FÖRSTA D** |
| ~~`fortroende_domstolar_myndigheter`~~ ✅ / `tillit_valdeltagande` | demokrati | **Brå NTU 5A:1** (förtroende rättsväsendet, officiell — ej SOM) / SOM (tillit_valdeltagande, 🔴 BEVAKA/B-only) | L→**S** | ✅ **fortroende inläst 2026-06-07 (Tier 4, v0); DEMOKRATINS FÖRSTA D** |

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

Störst hävstång på trovärdighet. B väger 35 % och vilar på **36 evidensposter + 192 ståndpunkter,
expertgranskade och bumpade till `version 1` (mänsklig sign-off 2026-06-05); B2 samma dag: FoU-avdrag, undermåttet
företagande/investeringar samt hushållens disponibla inkomst → ekonomi 4/6 täckta undermått. 2026-06-06: nato
(försvar) + snabbförfarande (trygghet 4/5) + invasiva arter (klimat 4/5, FLAGGAD) via enhällighet-som-källa**.

- **B1 — Expertgranska version-0-config** ✅ *(mänsklig sign-off 2026-06-05 — `version 0 → 1`)* —
  gransknings­paketet i [expertgranskning/](expertgranskning/) genomgånget; `party_positions.yaml`,
  `evidence_ledger.yaml` (+ `budget_ramar.yaml`) är nu `version: 1` / `status: expert_reviewed`, coverage-
  strängen uppdaterad (version-0-varningen borttagen), `dist/` ombyggt, snapshot re-baselinad, testsviten
  grön. **Skarp betygsättning aktiverad.** Granskningsbesluten (vad som ändrades och varför) nedan:
  - **Granskningssession 2026-06-05 (beslut införda i config, version kvar 0):**
    - *party_positions — 4 SUSPECT-fynd avgjorda:* V `kontroller_..._mot_valfardsbrott` opposes→**supports/förbehåll**
      (ankrad till yrkande 2: stöd för åtgärder mot välfärdsbrott med rättssäkerhetsförbehåll); C `tidiga_insatser`
      opposes→**supports** (omattribuerad — H5023910 är en L-ledd allians­motion mot *tillbakadragna* prop 2017/18:18;
      kodas nu som M/KD via H5024117 mot antagna 195); S `ny_karnkraft` **behållen supports** (noten dokumenterar
      villkoret); M/SD/KD/L `ny_karnkraft` **behållna + källtyps-asymmetri dokumenterad** i liggaren.
    - *evidence_ledger — alla 30 poster triade (blast-radius-mätt), 6 åtgärder införda:* koldioxidskatt→territoriella_utslapp-
      **dubblett borttagen** (löste bekräftad double-count), **redundant** subventionerade→arbetslöshet borttagen (D4;
      undviker dubbelvikt av jobbeffekten i samma undermått), `tidiga_insatser`/`behandlingsprogram_kriminalvard`/
      `sfi_kombinerat_med_praktik` **uppgraderade** från generiska seed-källor till URL-verifierade officiella källor
      (Skolforskningsinst. 2019 / Kriminalvården / IFAU Dahlberg m.fl. 2020), `reduktionsplikt_drivmedel` effect_strength
      **HIGH→medium** (vilade på en-års-attribution i pressmeddelande). 5 inerta poster identifierade (unclear/mixed/
      0 ståndpunkter → ingen B-effekt). De 3 demokrati-posterna (expert_opinion) **behållna** (bästa tillgängliga). Liggaren nu **28 poster**.
    - *party_positions — 79-raders panelscreening klar 2026-06-05:* **inga fabrikat**. De 11 kvarvarande
      `opposes` granskade — 7 sunda (4 voteringsbelagda reduktionsplikt + SD subventionerade + SD minskad_klasstorlek
      [äldre 2015/16] + redan klara), 5 av typen "motsätter sig *expansion/höjning*" (C/KD/L arbetsmarknadsutbildning,
      C subventionerade, SD koldioxidskatt) **behållna som opposes** per expertbeslut: riktningsregeln hålls objektiv
      (observerbar handling, ingen avsiktstolkning); magnituden adresseras via täckning (B2/B4), inte omkodning.
      12 enskild-motion-rader + 17 lågkonfidens-supports identifierade (riktningsbevarande, svag provenans, koncentrerade
      till demokrati — se B4).
    - *✅ Sign-off + version-bump 0→1 genomförd 2026-06-05.* Screeningdjup (det sign-offen vilar på): högrisk-
      klasserna (alla opposes, enskild-motion, lågkonfidens) är genomgångna; övriga supports-rader är riktnings-
      bevarande och instrument-exakta enligt sina mapping_notes men har inte var för sig återhämtats mot källa.
      *Kvarstående B-arbete flyttat till B2/B4 (täckning) — ej en blockerare för v1.*
- **B2 — Bredda evidensliggaren (anti-binär)** 🟡 *(ekonomi ✅ 4/6 täckta = alla 4 B-möjliga, 2026-06-05: FoU→produktivitet + företagande/investeringar + hushållens disponibla inkomst; kvar: demokrati)* — flera
  kategoriers B vilar på för få undermått (se B4). **Ekonomi är värst: 1/5 undermått (25 % av kat-vikten), bara
  2 aktiva åtgärdstyper som båda matar `sysselsattning`** → B blir nästan binär (5,0 / ~2,5 / 0,0 efter två
  jobbpolitiska ställningstaganden; BNP/produktivitet + reallöner + inflation + offentliga finanser = 75 % har
  **noll** B-evidens). Demokrati lika illa (1/5, 20 %, dessutom enbart `expert_opinion`). Åtgärd: källbelagda
  åtgärdstyper för de otäckta undermåtten — **ekonomi först**, och då **produktivitet** (`bnp_produktivitet`)
  och **reallöner** (`realloner_hushall`) — de enda up-indikatorerna. (Inflation + offentliga finanser är
  target-indikatorer → tar inget riktat B-bidrag; B4-grinden bekräftar detta.) Fler åtgärdstyper/kategori
  → fler täckta undermått → mindre binäritet (och högre `coverage` → mindre B-krympning).
- **B3 — Fler omstridda/differentierande åtgärdstyper** ⚪ — återanvänd Plan A-mönstret
  (Fas 4c): kandidatregister → endast intersektionen *omstridd ∧ evidensbelagd* → negativ-grind.
- **B4 — Kategori-täckningsaudit (anti-binär garanti)** ⚪ *(ny 2026-06-05)* — säkerställ att **ingen
  kategoris B vilar på ett enda undermått**. Täckningsaudit 2026-06-05 (aktiva åtgärdstyper × undermått de matar):

  | Kategori | Undermått m. B-evidens | Andel kat-vikt | Status |
  |---|---|---|---|
  | ekonomi | ~~1/5~~ **4/6** | ~~25 %~~ **73 %** | ✅ åtgärdad 2026-06-05 (FoU→produktivitet + företagande/investeringar + hushållens disponibla inkomst). 4 av 4 B-möjliga täckta; inflation/off.finanser = target (vilande) |
  | demokrati | ~~1/5~~ **4/5** | ~~20 %~~ **80 %** | ✅ åtgärdad 2026-06-05/06: (1) grundlagsskydd domstolarnas oberoende → otillborlig_politisering (votering KU2), (2) begränsa biometrisk realtidsövervakning m. rättssäkerhet → overvakning_utan_rattssakerhet (votering JuU28, **blocköverskridande**, Lagrådet-ankrat), **(3) lagstadgat oberoende public service → mediefrihet (enhälligt bet. 2025/26:KrU2 p1, prop. 2024/25:166 ur parlamentarisk kommitté SOU 2024:34 → alla 8 supports; codex BUILD-WITH-CHANGES, mekanism-/designevidens low/low; demokrati 3/5 → 4/5)**. Kvar otäckt: transparens_ansvar (**stark återöppning: prop. 2025/26:258 insyn i politiska processer, bet. KU39, beslut 2026-06-15**) |
  | valfard | 2/4 | 50 % | tunn — vard_tillganglighet + omsorg_personal HOLD 2026-06-06, **djupsvep §5.8 (11 instrument) bekräftar**: vårdplats-slutrapport 2026:3 föll *nedåt* (villkor konsumerat), cancerscreening klarar steg 1 men faller på neutralitet (avslag/opp-reservationer); omsorg_personal = fel konstrukt (kompetens/heltid/kontinuitet ≠ omsättning). Väg till 4 kräver modellutvidgning → sign-off |
  | forsvar | ~~2/5~~ **3/5** | ~~55 %~~ **60 %** | ✅ nato_ukraina tillagt 2026-06-06 (nato_medlemskap, votering UU16, Försvarsberedningen-källa, codex-granskat: V=opposes, MP=none pga reversering). Kvar: ekonomisk_ambition=target (ej B-bar), genomforbarhet_leverans (HOLD, **djupsvep §5.8/7 instrument bekräftar äkta steg-1-vägg**: ingen svensk källa kopplar instrument → kortad *leveranstid*, bara kapacitet/kostnad; ev. indikatorbyte FMV leveransindex → sign-off) |
  | integration | 2/5 | 55 % | tunn — normer_tillit + boendesegregation HOLD 2026-06-06, **djupsvep §5.8 (11 instrument) bekräftar**: boendesegr. = äkta steg-1-vägg (allt beskrivande/mixed), normer_tillit/KU4-tillgänglighet = perfekt steg 2 men fel konstrukt (förmåga att rösta ≠ uppmätt valdeltagande). Högsta bias-risk; väg till 4 kräver modellutvidgning → sign-off |
  | trygghet | ~~3/5~~ **4/5** | ~~65 %~~ **85 %** | ✅ snabbforfarande_lagforing 2026-06-06 (handlaggningstid, Brå 2020:3, enhälligt bet. JuU2 p1 → alla 8 supports, codex BUILD-WITH-CHANGES). Kvar: forebyggande (saknar indikator) |
  | klimat | ~~3/5~~ **4/5** | ~~70 %~~ **85 %** | ✅ atgarder_mot_invasiva_frammande_arter 2026-06-06 (hotade_arter_naturforlust, Naturvårdsverket, enhälligt bet. MJU13 p1 → alla 8 supports). **FLAGGAD: codex förordade HOLD; byggt v0 low/low — sign-off avgör.** Kvar: industriell_konkurrenskraft (saknar indikator) |

  Mål: ≥2–3 undermått med evidens per kategori; ingen kategori där en enda åtgärdstyp (eller ett undermått) kan
  svänga betyget mellan ytterlägen. **Verktyg/grind ✅ levererad 2026-06-05** (se B4-verktyg under Levererat):
  [coverage_report.py](../pipeline/tools/coverage_report.py) `b_submeasure_spread()` flaggar nära-binär
  kategori (≤1 undermått) och [test_fas4b_coverage.py](../tests/test_fas4b_coverage.py) + nya
  `coverage_allowlist.b_near_binary_accepted` gör regressionen synlig. **Kvar (=B2):** faktiskt höja
  spridningen till ≥2 undermått för ekonomi och demokrati. **VIKTIGT fynd från grinden:** inflation och
  offentliga finanser (ekonomi) är target-indikatorer → kan inte få riktat B-bidrag; ekonomis enda
  realistiska B-mål är produktivitet och reallöner (up-indikatorer). Knyter an till B2 (ekonomi/demokrati först).
  - **Demokrati är trippel-svag** (fynd vid 79-screeningen 2026-06-05): (1) nära-binär (1/5 undermått), (2) liggaren
    är enbart `expert_opinion` (rekommendationer, ej uppmätt effekt), och (3) partiståndpunkterna bygger till stor del
    på **enskilda ledamotsmotioner** (4 av `starkt_oberoende_granskning`-raderna M/SD/KD/L + flera antikorruptionsrader
    är `enskild_motion`). Riktningen är låg-risk (alla stödjer antikorruption), men demokrati-B vilar på den svagaste
    provenansen i hela modellen → bör antingen få bredare/bättre källor eller redovisas med uttryckligt lågt förtroende.

- **B5 — B-undermåttsbreddskrympning (parallellen till D:s coverage_shrink)** 🟣 *(öppnad 2026-06-12
  ur [done/d_coverage_krympning_spec.md §8](done/d_coverage_krympning_spec.md))* — B har redan
  åtgärdstyps-coverage-krympning + `b_submeasure_spread`-grind, men ingen krympning efter
  **undermåttsbredd** (en kategori med B-evidens i 2/5 undermått gör ändå oavkortat kategorianspråk).
  En extra B-krympning riskerar **dubbelrabatt** mot den befintliga åtgärdstyps-krympningen → kräver
  egen spec med samma metodik (viktad icke-target-bredd, per parti/kategori) nu när D-ändringen är
  mätt och kan jämföras. Designfråga, ej byggbar utan spec + sign-off.

---

## Spår A — Agerande (delpoäng A)

- **A1 — Fler budgetår** ✅ *(levererad 2026-06-05)* — `budget_ramar.yaml` täcker nu **budget
  2023 + 2024 + 2025** (samma trogna transkriberingsmönster, källrad per frame). a1 är ett snitt
  över åren i stället för en enda mätpunkt. Fyrlagrigt verifierad (invariant + pandas + Codex +
  roll-call); se Levererat ovan + [metod](fas1b_budget_metod.md).
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

## Spår O — Drift, robusthet & ops ✅ KOMPLETT (O1–O4, 2026-06-03/05)

- ~~**O1 — Serie-drift-skydd**~~ ✅ — [pipeline/expectations.py](../pipeline/expectations.py),
  förväntansassertion per inläst serie (se Levererat 2026-06-03).
- ~~**O2 — Snapshot/diff**~~ ✅ — [score_diff.py](../pipeline/tools/score_diff.py) mot
  `dist/scores.snapshot.json` (se Levererat 2026-06-03).
- ~~**O3 — Live-fetch smoke test**~~ ✅ — [test_sources_live.py](../tests/test_sources_live.py),
  opt-in `ROSTA_LIVE=1` (se Levererat 2026-06-03). *(O4 reproducerbar dist ✅ 2026-06-05.)*

---

## Föreslagen ordning (vågor)

| Sprint | Data (D) | Evidens (B) | Övrigt |
|--------|----------|-------------|--------|
| **1** | ~~Våg 1: Brå (uppklaring/handläggning/återfall) + Socialstyrelsen (överlevnad)~~ ✅ avslutad 2026-06-09 | ~~**B1: starta expertgranskning**~~ ✅ sign-off 2026-06-05 | ~~**O1: drift-skydd**~~ ✅ |
| **2** | Våg 2: Medlingsinstitutet (reallöner, låg prio) + ~~Skolverket (sfi)~~ ✅ (SCB TAB1814, Tier 2) + Svk-adapter (gränsfall källregel) | B2: bredda liggaren *(kvar: valfard/integration HOLD-beslut, transparens_ansvar-bevakning KU39 2026-06-15)* | ~~A1: fler budgetår~~ ✅ klar |
| **3** | Våg 3: härledda klimat (elpris/effekt/utsläpp-per-krona) — enda öppna D-byggen | B3: omstridda åtgärdstyper · B5: B-breddskrympning (spec) | A2 votering · C2/C3 · F1/F2 |

> Varje levererat steg: flytta indikatorn ur `coverage_allowlist.yaml`, uppdatera täckningssiffran
> i `scorerun.py:coverage`-strängen, och bocka av posten här (✅ → kort rad i ROADMAP.md).
