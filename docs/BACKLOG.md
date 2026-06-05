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
  **distinkta submått** som har AKTIV partikopplad B-evidens per kategori (åtgärdstyp med
  signed_direction≠0, ej coverage_exclude, **och** minst en partiståndpunkt → indikator → submått) och
  flaggar **nära-binär** kategori (≤1 submått). Speglar att `score.aggregate_B` är submåttsviktat:
  vilar all aktiv evidens på ett submått kan en enda ståndpunkt svinga b_raw mellan ytterlägen.
  Reproducerar BACKLOG-tabellen exakt (ekonomi 1/5, demokrati 1/5, valfard 2/4, forsvar 2/5,
  integration 2/5, trygghet 3/5, klimat 3/5). Grinden följer coverage_allowlist-mönstret: varje
  nära-binär kategori måste stå i nya `coverage_allowlist.b_near_binary_accepted` med skäl (annars tyst
  regression), och listan kan inte bära inaktuella poster (krymper när B2 levererar). **Fynd:** ekonomis
  realistiska B-mål är `bnp_produktivitet` + `realloner_hushall` (up-indikatorer) — inte
  inflation/offentliga finanser, som är **target-indikatorer utan B-bär riktning** (samma skäl som de
  uteslöts ur D). Hela sviten grön (167 passed). Återstår (=B2): faktiskt bredda liggaren.
- ✅ **B2 (första leveransen) — ekonomi/produktivitet via FoU-avdraget** ([evidence_ledger](../config/evidence_ledger.yaml)
  + [party_positions](../config/party_positions.yaml)): ny åtgärdstyp `fou_avdrag_skatteincitament` → indikator
  `produktivitet` (submått bnp_produktivitet). Evidens: **Produktivitetskommissionen SOU 2025:96** + **SOU 2025:3**
  (authority_evaluation, medium/medium — riktningen FoU→produktivitet säker, men avdragets marginaleffekt ej
  kausalutvärderad). **8 partiståndpunkter votering-belagda** (bet. 2022/23:SfU19, prop. 2022/23:79 "höjt tak för
  FoU-avdraget" 600 000→1,5 mkr/mån, kammaren 2023-05-31): 7 Ja = **supports**, **V Nej = opposes** (reservation +
  kommittémotion 2022/23:2365). **Ekonomi 1/5 → 2/5 submått med B-evidens — ej längre nära-binär** (ekonomi borttagen
  ur `b_near_binary_accepted`; B4-grinden tvingade fram det). Betygseffekt (förklarbar): V faller på ekonomi
  3,31→2,54 (dess tidigare topplacering var en nära-binär artefakt — ekonomi vilade på jobb-submåttet där V var max),
  C stiger 1,26→2,04 (jobbsubventions-skeptisk men FoU-positiv). **Ny ranking: S > L > M > MP > KD > C > V > SD.**
  dist omräknat, snapshot re-baselinad, paket regenererat (priority 79), 167 tester gröna. Forskning→förslag→mänsklig
  sign-off 2026-06-05.
- ✅ **B2 (andra leveransen) — nytt ekonomi-submått "Företagande och investeringar"** (modellutvidgning:
  [categories.yaml](../config/categories.yaml) + [IDEA.md](../IDEA.md) + [evidence_ledger](../config/evidence_ledger.yaml)
  + [party_positions](../config/party_positions.yaml) + [coverage_allowlist](../config/coverage_allowlist.yaml)):
  reallöner visade sig **ej B-bart** (Medlingsinstitutet: reallön sätts av parterna via Industriavtalet, drivs av
  produktivitet + Riksbankens inflationsmål → inget partistyrt icke-dubbelräknande instrument). I stället tillagt ett
  **6:e submått** `foretagande_investeringar` (vikt 15; ekonomi-vikterna omfördelade 22/18/18/15/12/15) med indikator
  `naringslivets_investeringar` (up, SCB; allowlistad för D — konjunkturkänslig). Åtgärdstyp
  `konkurrenskraftig_foretags_och_agarbeskattning` → investeringar, evidens **Företagsskattekommittén SOU 2014:40**
  (authority_evaluation, medium/medium — investeringars skatteelasticitet empiriskt omtvistad). **BRED ram** (efter att
  smal bolagsskatts-ram visade sig gles, 4/1/3): 8 partiståndpunkter, ordagrant källbelagda via 8+3 parallella
  researchagenter mot fulltext — **5 supports** (M/SD/C/KD/L: lägre bolags-/ägarskatt) / **3 opposes** (S/V/MP: höja
  kapital-/företagsvinstskatt). **Ekonomi 2/6 → 3/6 täckta submått** (av 4 B-möjliga: jobb, produktivitet, investeringar
  täckta; reallöner ej B-bart, inflation/offentliga finanser target). Betygseffekt: vänstern ner på ekonomi (S/MP
  −0,48, V −0,27), högern upp (C +0,27, KD/L +0,15). **Ny ranking: S > L > M > KD > MP > C > SD > V.** dist/snapshot/paket
  (priority 84) + 167 tester gröna. Forskning→förslag→mänsklig sign-off 2026-06-05.
- ✅ **B2 (tredje leveransen) — 4:e ekonomi-måttet: hushållens disponibla inkomst (värdeneutralt)** ([categories.yaml](../config/categories.yaml)
  + [evidence_ledger](../config/evidence_ledger.yaml) + [party_positions](../config/party_positions.yaml)): submåttet **"Reallöner och
  hushållens ekonomi"** gjordes B-bart genom en ny ARBETANDE indikator `hushallens_reala_disponibla_inkomst` (up, SCB; `realloner`
  förblir vilande kontext/framtida D). **Ingen ny hink, ingen omviktning** — bara en indikator i befintligt submått. Värdeneutral
  familj-åtgärdstyp `inkomststarkande_hushallspolitik` (skatte- och/eller transfereringsreformer som höjer disponibel inkomst),
  evidens **Fördelningspolitisk redogörelse april 2025** (descriptive_statistic/medium/high). **8 partiståndpunkter, alla supports**
  via sitt block-instrument (höger M/SD/C/KD/L: sänkt skatt på arbete; vänster S/V/MP: höjda transfereringar) — ordagrant källbelagda
  via 8 parallella agenter mot fulltext. **Löser tilt-problemet:** eftersom båda blocken kodas supports (en åtgärдstyp, coverage 4/4→5/5,
  ingen straff) får alla ett positivt köpkraftsbidrag, **störst lyft för dem investeringar-submåttet tryckte ner** (V +0,26, C +0,17,
  MP/S +0,12) → späder ut högertilten. **Ekonomi 3/6 → 4/6 täckta submått = "4 bra mått" nått, värdeneutralt.** Ny ranking:
  **S > L > M > KD > MP > C > V > SD.** dist/snapshot/paket (priority 87) + 167 tester gröna. Forskning→förslag→mänsklig sign-off 2026-06-05.
  *(Sparande/sparkvot avfärdat: target-likt + svag attribuering; reallöner kvar som vilande kontext.)*
- ✅ **B2 (fjärde leveransen) — demokrati: rättsstat/domstolarnas oberoende** ([evidence_ledger](../config/evidence_ledger.yaml)
  + [party_positions](../config/party_positions.yaml) + [coverage_allowlist](../config/coverage_allowlist.yaml) + [DATA.md](../DATA.md)):
  submåttet **rattsstat_maktdelning** gjordes B-bart via åtgärdstyp `grundlagsskydd_domstolarnas_oberoende` → indikator
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
  + [party_positions](../config/party_positions.yaml)): submåttet **personlig_frihet** gjordes B-bart via åtgärdstyp `begransa_biometrisk_realtidsovervakning_rattssakerhet` → indikator
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
- ✅ **O4 — reproducerbar dist** ([pipeline/scorerun.py](../pipeline/scorerun.py)): `dist/scores.json`
  + `dist/evidence.json` var **icke-deterministiska mellan körningar** — claims byggdes i hash-
  randomiserad ordning, så `claim_refs` (provenanspekare) bytte ordning *och* `obs_by_cat[:3]`-urvalet
  pekade på olika 3 observationsclaims per process. Betygen var alltid deterministiska; bara
  provenansen drev. Fixat genom att sortera claims på id + `sort_keys` på JSON-utskriften → dist är nu
  **byte-identisk över processer** (verifierat med olika `PYTHONHASHSEED`). Upptäckt under A1-omräkningen;
  stärker O2-snapshot/diff (ingen falsk drift av ordningsbrus).

### Status per spår efter nattkörning 2026-06-04 (A-raden uppdaterad 2026-06-05)

| Spår | Status |
|------|--------|
| **D** (datatäckning) | uppklaringsgrad + skjutningar/sprängningar **levererade**. Återstående D-källor **uttömda/blockerade** (se [coverage_allowlist](../config/coverage_allowlist.yaml) med precisa skäl): återfall (PDF prel/slutlig + metodbrott), handläggning (interaktiv DB), overlevnad (Kolada N79196 finns men **kvinkennial** → inkompatibel med D:s konsekutiva-år-krav), reallöner/sfi (portal/ej ren serie), Svk-derived klimat (operativ/timdata + Nord Pool-pris = gränsfall mot officiell-källa-regeln, lågt mervärde då klimat har 3 D-serier), demokrati (internationella index förbjudna), försvar (sekretess/kvalitativt). **De rena SCB/Kolada-årsserierna skördades i Fas 2–3; den hårda taljen kräver expertbedömd transkribering, modellutvidgning, eller är otillåten.** |
| **B** (evidens) | ✅ **B1 expertgranskad + sign-off 2026-06-05 → `version 1`** (se B1 nedan): party_positions (4 SUSPECT + 79-raders screening) och evidence_ledger (30 poster triade, 6 fixar) genomgångna; skarp betygsättning aktiverad. **B4-verktyg/grind ✅** + **B2 ekonomi ✅** (4/6) + **B2 demokrati ✅** (rättsstat: grundlagsskydd domstolarnas oberoende, votering KU2; personlig frihet: begränsa biometrisk realtidsövervakning, votering JuU28/Lagrådet, codex-granskat) levererade 2026-06-05 → demokrati **1/5 → 3/5**, **inga nära-binära kategorier kvar** (`b_near_binary_accepted` tom). Återstår otäckta (ej blockerare): transparens_ansvar (offentlighetsprincip = dubbelräkning, skippat) + yttrandefrihet_medier (acklamation/regeringslägesartefakt) — inget värdeneutralt mått funnet utan tilt/dubbelräkning. |
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

Störst hävstång på trovärdighet. B väger 35 % och vilar på **33 evidensposter + 169 ståndpunkter,
expertgranskade och bumpade till `version 1` (mänsklig sign-off 2026-06-05); B2 samma dag: FoU-avdrag, submåttet
företagande/investeringar samt hushållens disponibla inkomst → ekonomi 4/6 täckta submått**.

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
      undviker dubbelvikt av jobbeffekten i samma submått), `tidiga_insatser`/`behandlingsprogram_kriminalvard`/
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
  kategoriers B vilar på för få submått (se B4). **Ekonomi är värst: 1/5 submått (25 % av kat-vikten), bara
  2 aktiva åtgärdstyper som båda matar `sysselsattning`** → B blir nästan binär (5,0 / ~2,5 / 0,0 efter två
  jobbpolitiska ställningstaganden; BNP/produktivitet + reallöner + inflation + offentliga finanser = 75 % har
  **noll** B-evidens). Demokrati lika illa (1/5, 20 %, dessutom enbart `expert_opinion`). Åtgärd: källbelagda
  åtgärdstyper för de otäckta submåtten — **ekonomi först**, och då **produktivitet** (`bnp_produktivitet`)
  och **reallöner** (`realloner_hushall`) — de enda up-indikatorerna. (Inflation + offentliga finanser är
  target-indikatorer → tar inget riktat B-bidrag; B4-grinden bekräftar detta.) Fler åtgärdstyper/kategori
  → fler täckta submått → mindre binäritet (och högre `coverage` → mindre B-krympning).
- **B3 — Fler omstridda/differentierande åtgärdstyper** ⚪ — återanvänd Plan A-mönstret
  (Fas 4c): kandidatregister → endast intersektionen *omstridd ∧ evidensbelagd* → negativ-grind.
- **B4 — Kategori-täckningsaudit (anti-binär garanti)** ⚪ *(ny 2026-06-05)* — säkerställ att **ingen
  kategoris B vilar på ett enda submått**. Täckningsaudit 2026-06-05 (aktiva åtgärdstyper × submått de matar):

  | Kategori | Submått m. B-evidens | Andel kat-vikt | Status |
  |---|---|---|---|
  | ekonomi | ~~1/5~~ **4/6** | ~~25 %~~ **73 %** | ✅ åtgärdad 2026-06-05 (FoU→produktivitet + företagande/investeringar + hushållens disponibla inkomst). 4 av 4 B-möjliga täckta; inflation/off.finanser = target (vilande) |
  | demokrati | ~~1/5~~ **3/5** | ~~20 %~~ **60 %** | ✅ åtgärdad 2026-06-05: (1) grundlagsskydd domstolarnas oberoende → otillborlig_politisering (votering KU2, neutralt/odifferentierande), (2) begränsa biometrisk realtidsövervakning m. rättssäkerhet → overvakning_utan_rattssakerhet (votering JuU28, **blocköverskridande/differentierande**, Lagrådet-ankrat, codex-granskat). Kvar otäckta: transparens_ansvar (offentlighetsprincip = dubbelräkning mot bunt, skippat) + yttrandefrihet_medier (acklamation/regeringslägesartefakt) — inget värdeneutralt mått funnet |
  | valfard | 2/4 | 50 % | tunn |
  | forsvar | 2/5 | 55 % | tunn (mest sekretess/kvalitativt) |
  | integration | 2/5 | 55 % | tunn |
  | trygghet | 3/5 | 65 % | ok |
  | klimat | 3/5 | 70 % | bäst |

  Mål: ≥2–3 submått med evidens per kategori; ingen kategori där en enda åtgärdstyp (eller ett submått) kan
  svänga betyget mellan ytterlägen. **Verktyg/grind ✅ levererad 2026-06-05** (se B4-verktyg under Levererat):
  [coverage_report.py](../pipeline/tools/coverage_report.py) `b_submeasure_spread()` flaggar nära-binär
  kategori (≤1 submått) och [test_fas4b_coverage.py](../tests/test_fas4b_coverage.py) + nya
  `coverage_allowlist.b_near_binary_accepted` gör regressionen synlig. **Kvar (=B2):** faktiskt höja
  spridningen till ≥2 submått för ekonomi och demokrati. **VIKTIGT fynd från grinden:** inflation och
  offentliga finanser (ekonomi) är target-indikatorer → kan inte få riktat B-bidrag; ekonomis enda
  realistiska B-mål är produktivitet och reallöner (up-indikatorer). Knyter an till B2 (ekonomi/demokrati först).
  - **Demokrati är trippel-svag** (fynd vid 79-screeningen 2026-06-05): (1) nära-binär (1/5 submått), (2) liggaren
    är enbart `expert_opinion` (rekommendationer, ej uppmätt effekt), och (3) partiståndpunkterna bygger till stor del
    på **enskilda ledamotsmotioner** (4 av `starkt_oberoende_granskning`-raderna M/SD/KD/L + flera antikorruptionsrader
    är `enskild_motion`). Riktningen är låg-risk (alla stödjer antikorruption), men demokrati-B vilar på den svagaste
    provenansen i hela modellen → bör antingen få bredare/bättre källor eller redovisas med uttryckligt lågt förtroende.

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
| **2** | Våg 2: Medlingsinstitutet (reallöner) + Skolverket (sfi) + Svk-adapter | B2: bredda liggaren | ~~A1: fler budgetår~~ ✅ klar |
| **3** | Våg 3: härledda klimat (elpris/effekt) + demokrati/försvar-design | B3: omstridda åtgärdstyper | A2 votering · C2/C3 · F1/F2 |

> Varje levererat steg: flytta indikatorn ur `coverage_allowlist.yaml`, uppdatera täckningssiffran
> i `scorerun.py:coverage`-strängen, och bocka av posten här (✅ → kort rad i ROADMAP.md).
