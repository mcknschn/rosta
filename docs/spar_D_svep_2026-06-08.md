# Spår D — Djupsvep: 5 kandidater per D-tomt undermått (90 tester)

> **Uppdrag (din beställning 2026-06-08):** för VARJE undermått utan en fungerande D-serie, testa 5
> potentiella indikatorer **hela vägen** — faktiskt hämta datat och försöka mäta/bygga, inte avfärda
> på resonemang. Syfte: lära hur datat publiceras + hitta tidigare missade byggbara mått (som i
> B-svepet). **Beslut:** bygg rena (neutrala/officiella/riktningsklara) som flaggad v0 direkt; pausa
> riktnings-tvetydiga/värdeladdade/pengaproxyer för sign-off. Target-submått ingår (testa proxyer).
>
> 18 D-tomma undermått × 5 = **90 kandidater**. Källregel: endast officiella svenska källor; ingen
> internationell index. Konsekutiv årsserie, riktning up/down.

Legend: ✅ byggd v0 · 🟢 BUILDABLE (verifierad, ej byggd än) · 🟡 SIGN-OFF (byggbar men tvetydig/
värdeladdad/pengaproxy) · 🔴 WALL (testad mot källan, ingen användbar serie) · ⏳ pågår.

---

## Status per kategori

| Kategori | D-tomma undermått | Agent | Status |
|---|---|---|---|
| Ekonomi | inflation_prisstabilitet, offentliga_finanser | E | ✅ klar (alla data finns, men neutralitet/attribution → sign-off) |
| Välfärd | omsorg_personal, finansiering_styrning | V | ✅ klar (1 ren bygge: U21468) |
| Trygghet | forebyggande, aterfall_kriminalvard | T | ✅ klar (0 rena; KOS=pending tabellbilaga, forebyggande sign-off) |
| Försvar | ekonomisk_ambition, civil_beredskap, genomforbarhet_leverans | F | ✅ klar (0 rena; civil=vägg, övr money-proxy sign-off) |
| Klimat | kostnadseffektivitet, biologisk_mangfald, industriell_konkurrenskraft | K | ✅ klar (1 rent bygge: utslappsintensitet) |
| Integration | normer_tillit, migrationssystem | I | ✅ klar (data finns men neutralitet → sign-off) |
| Demokrati | rattsstat_maktdelning, yttrandefrihet_medier, personlig_frihet, transparens_ansvar | D | ✅ klar (0 rena — äkta vägg, all data tvetydig/endogen) |

**Genomgående lärdom hittills:** Kolada v2-API är nedlagt (410 Gone) → använd **v3** (repo-adaptern funkar dock).
Många "väggar" visade sig ha *data som faktiskt finns* — blockeraren är oftast **riktning/neutralitet/
attribution**, inte tillgänglighet. Det är i sig ett starkt argument för coverage-krympning + target-design.

---

## Testlogg (alla 90 kandidater)

### EKONOMI — alla data FINNS, men target-design håller (neutralitet/attribution) → sign-off

**inflation_prisstabilitet** (target). Alla 5 maskinläsbara (SCB):
- C1 KPIF |avvikelse från 2%|, SCB TAB6590, **26 år 2000-2025**, down → 🟡 SIGN-OFF.
- C4 KPIF-XE |avvikelse från 2%|, SCB TAB6593, **26 år**, down → 🟡 (starkast; Riksbankens målmått).
- C2 andel månader i band 1-3% (UP), C3 KPIF-volatilitet (down): byggbara men ej oberoende → 🟡.
- C5 inflationsförväntan hushåll (KI), 24 år → 🟡 (systematiskt biased).
- **Slutsats:** data finns rikligt. MEN inflation styrs av *oberoende Riksbanken*, ej regering → D-attribution
  till partier är metodiskt svag; och target (symmetrisk runt 2%) är mer neutralt än up/down. **Behåll target.**

**offentliga_finanser** (target). Alla 5 maskinläsbara (SCB, ren ratio-op):
- C1 finansiellt sparande % BNP, TAB3573, **30 år 1996-2025**, up → 🟡.
- C2 Maastrichtskuld % BNP, TAB5050/TAB3573, **30 år**, down → 🟡 (EU-måttet).
- C4 ränteutgifter % BNP, **30 år**, down → 🟡. C5 finansiell nettoförmögenhet % BNP, TAB4350, **29 år**, up → 🟡.
- C3 strukturellt sparande → 🔴 WALL (bara KI-PDF, ingen API).
- **Slutsats:** rikligt med rena 30-årsserier (byggbara via befintlig ratio-op!). MEN "sparande up/skuld down =
  bättre" kodar finanskonservatism (Keynes vs austerity) — ej neutralt; den officiella hållningen är *ankaret*
  (target ~35% skuld), inte extremvärde. **Behåll target** (eller bygg symmetrisk "avstånd från skuldankaret").

### VÄLFÄRD

**omsorg_personal** (D-tomt). 5 testade:
- ✅ **U21468 brukarbedömning hemtjänst helhet (Kolada, 2013-2025, up)** — VERIFIERAD via adaptern, ren/neutral
  → **BYGGS** (öppnar omsorg_personal via ny kanonisk indikator).
- N00090 sjukfrånvaro kommunanställda (17 år, down) → 🟡 (scope = alla kommunanställda, ej omsorgsspecifik).
- U21401 personalkontinuitet (down): bara OU-nivå, inget nationellt → 🔴. Fast omsorgskontakt N21497: 2 år → 🔴.
  Omsorgspersonal-utbildning: OU-nivå/2 år → 🔴.

**finansiering_styrning** (D-tomt). 5 testade — INGEN ren:
- N03002 soliditet inkl pension (14 år, up) → 🟡 (drivs delvis av pensionsbokföring; soliditet *exkl* pension
  faller → riktning artefakt).
- Brå bidragsbrott (10 år, down) → 🟡 (enforcement-brus, +93% 2020-spik).
- Felaktiga utbetalningar (ESV) → 🔴 (bara PDF). Årets resultat/nettokostnadsavvikelse → 🔴 (volatilt/odefinierat nationellt).

### TRYGGHET (redan 5 D; dessa ger bredd till D-tomma submått)

**aterfall_kriminalvard** (D-tomt). 5 testade:
- 🟡 **KOS 3-årsåterfall till Kriminalvård (down)** — INTEGRITETSFYND vid egen PDF-läsning: de exakta
  årsvärdena ligger i en **FIGUR** (figur 6.2, axeletiketter bara vart 4:e år 1994/1998/.../2022) + prosa,
  INTE i en extraherbar tabell i huvud-PDF:en. Prosan bekräftar formen (42 %→29 % 1999-2012, sen platt
  ~30-31 %, 2022=31 %) men i den platta zonen 2013-2022 avgörs D:s årstecken av ±1 pp — **diagram-avläsning
  är ej säkert för sign-only D**. → kräver KOS **tabellbilaga (Excel)** för exakta årsvärden. **Byggbar men
  ej från huvud-PDF:en**; rekommenderas som greenlight-bygge när tabellbilagan hämtats. (Gamla allowlist-
  skälet "blocked: PDF" var alltså delvis korrekt — figuren, ej tabellen.)
- Brå 1-årsåterfall (2014-2023, down) → 🟡 (bara diagram i PDF, ej tabell). Behandlingsprogram fullföljt (3 år,
  metodbrott) → 🔴. Återfall frivård/anstalt (10 år) → 🟡 (platt, ≤3 pp). Beläggningsgrad → 🔴 (metodbrott + fel riktning).

**forebyggande** (D-tomt). 5 testade — bäst men sign-off:
- Brå lagförda unga 15-20 (2016-2025, down) → 🟡 (kräver SCB-befolkningsnämnare = rate; semantik: ungdomsbrott ≠
  kommunal förebyggande kapacitet). Misstänkta 15-20 likadant 🟡. Skadegörelse (16 år) → 🟡 (V-format, tvetydig trend).
- Kommuner m. lägesbild/åtgärdsplan (lag 2023:196) → 🔴 (2 år, för nytt). Medborgarlöften → 🔴 (ingen nationell aggregat).

### DEMOKRATI — 0 rena (äkta mätbarhetsvägg; all data finns men är tvetydig/endogen/värdeladdad)

**rattsstat_maktdelning** (D-tomt): Domstolsverket ändringsfrekvens kammarrätt (23 år) 🟡 riktnings-tvetydig ·
JO-kritik (10 år) 🟡 tvetydig+bred · Riksrevisionen modifierade revberättelser (22 år) 🟡 endogen · Lagrådet
invändningar 🔴 ingen årstabell · myndighetsbeslut upphävda 🔴 ingen serie.
**yttrandefrihet_medier** (D-tomt): JK yttrandefrihetsmål (20 år) 🟡 tvetydig · mediestödda titlar (20 år) 🟡
"subvention ≠ frihet" · hot mot journalister 🔴 ingen officiell serie · vita fläckar 🔴 ej årlig · PTU 🔴 vartannat år.
**personlig_frihet** (D-tomt): hemliga tvångsmedel-tillstånd (2016-2024, 12 år) 🟡 — men mäter *lagliga* (court-
approved) tvångsmedel, ej "utan rättssäkerhet" → semantisk miss + "mer övervakning=sämre" är värdeladdat (law-and-
order vs civilliberty). SIN-brister 🔴 ingen aggregat/för få (n≈28). IMY-sanktioner mot myndigheter 🔴 för få (0-7/år).
Kamerabevakning 🔴 lag slopad apr 2025.
**transparens_ansvar** (D-tomt): Riksrevisionen effektivitetsgranskningar (22 år) 🟡 endogen · DIGG öppna data 🔴
bara 5 år · utlämnandemål-ändring 🔴 ej särredovisat · JO-handläggningstid 🔴 · partifinansiering-compliance 🔴 ingen aggregat.
**→ Demokrati-slutsats:** rikligt med officiella årsserier EXISTERAR, men varenda en är riktnings-tvetydig (fler
anmälningar/granskningar/sanktioner = bättre upptäckt ELLER sämre tillstånd?), endogen (myndighetens egen output)
eller värdeladdad. Ingen kan byggas neutralt. **Starkaste empiriska stödet för coverage-krympning av demokrati-D.**

### INTEGRATION

**normer_tillit** (D-tomt). 5 testade — ingen ren med fit:
- SCB "avstått gå ut pga otrygghet" (LE0101 T374, 2020-2025, 6 år, down) → 🟡 (byggbar, men mäter otrygghet ≈
  trygghet-kategorins upplevd_otrygghet, svag fit mot *tillit*).
- Mellanmänsklig tillit (Kolada U01413, Folkhälsomynd HLV): 2007-2016 konsekutiv men glapp 2017/2019/2023 → 🔴 recent.
- SCB Medborgarundersökning tillit/förtroende (N00665): bara 2021-2025 (5 år) → 🟡 borderline (6:e år 2026).
- Föreningsdeltagande (SCB ULF) → 🔴 gles (4 punkter). Valdeltagande → 🔴 (bara valår, Kolada fyller syntetiskt).

**migrationssystem** (D-tomt). 5 testade — data finns men SIGN-OFF (neutralitet i bias-riskkategori):
- 🟡 Öppna återvändandeärenden (Migrationsverket ÅR, down). Egen PDF-läsning: värdena ligger i **Figur 11.3**
  (ej tabell), MEN prosan bekräftar monoton nedgång (2023: −27 % vs 2022; 2024: −30 % vs 2023) → tecknen är
  SÄKRA (alla ned) trots figur. Källa: MV ÅR 2023 (Dnr 1.3.2-2024-2238) + ÅR 2024. **Riktningskonflikt:**
  integration-kategorins egen caveat = "stor risk för ideologisk bias; indikatorerna måste vara extra
  tydliga". "Färre öppna återvändandeärenden = bättre" förutsätter en effektiv-återvändande-ram som är
  politiskt omtvistad → **SIGN-OFF, ej autobygge**. (Skulle bara kreditera Tidö 2022-2025; mekaniskt korrekt
  men värdeladdat.) 2021 har dessutom definitionsfotnot (exkl. utresta/avvikna).
- 🟡 Asyl-handläggningstid (Migrationsverket xlsx, 2021-2025, down): maskinläsbar, 257→166→194→162→178 dgr.
  Byggbar men kräver ny MV xlsx-adapter; 5 år; snabbare handläggning rimligare neutral än återvändande → om
  något bygg DENNA hellre (sign-off).
- Verkställda återvändanden (up): 🟡 definitionsbyte + värdeladdat. Självmant-andel/avgjorda: 🟡 nämnare/throughput-tvetydig.
- **Slutsats:** data finns (figur+xlsx), tecknen säkra, men migrationssystem är den mest neutralitetskänsliga
  D-luckan (kategori-caveat) → all autobygge pausad för din riktnings-/neutralitets-sign-off.

### KLIMAT

**kostnadseffektivitet** (D-tomt). 5 testade:
- ✅ **utslappsintensitet (territoriella utsläpp SCB TAB4698 ÷ BNP TAB3610, 1990-2024, down)** — VERIFIERAD
  (1990=25,5 → 2024=8,7 ton/mnkr), ren härledd ratio → **BYGGD** (öppnar kostnadseffektivitet).
- Utsläpp/capita (35 år, down) → 🟡 kollinjär med territoriella_utslapp. Energiintensitet (35 år, down) → 🟡
  (energisystem-eff, ej klimat-kostnad). Utsläpp/TWh → 🔴 kollinjär m. fossil. Utsläpp ÷ klimatutgift(UO20) →
  🔴 (COFOG05 fel proxy; ESV UO20-utfall ingen API; §5.5 kvarstår).

**biologisk_mangfald** (D-tomt). 5 testade — 2 byggbara men sign-off:
- 🟡 Skyddad natur % av landareal (SCB MI0603D, 2014-2025, up, **maskinläsbar**) → policy-INSATS ej ekologiskt
  utfall + neutralitet (skogsnärings-trade-off "mer skyddat=bättre").
- 🟡 Häckande fåglar i skogen (Svensk Fågeltaxering via sverigesmiljomal.se, 2002-2024, up) → äkta biologiskt
  UTFALL, neutralare, men kräver HTML-scrape-adapter (Highcharts) + akademisk producent (Lund, officiell portal).
- Död ved (2005-2021, stale) 🔴 · ängs-/betesmark (glapp 2015-17) 🔴.

**industriell_konkurrenskraft** (D-tomt, saknar helt indikator). 5 testade:
- 🟡 Industrins GHG/förädlingsvärde (SCB MI1301B ÷ NR T09RK, 2008-2024, down, **maskinläsbar, ren SNI-match**)
  → byggbar men semantik: mäter utsläpps-EFFEKTIVITET, ej "konkurrenskraft"; kräver ny kanonisk indikator → sign-off.
- Fossilfri el % (35 år, up) 🟡 (riktning DOWN över 1990-2024, up först sen 2011). Nettoexport el 🟡 (1990-2010 brusig).
  Total elprod TWh 🔴 (väderdominerad, hydroår).

### FÖRSVAR — 0 rena (ukraina_stod redan byggd i natt; resten money-proxy/vägg)

**ekonomisk_ambition** (target+B-only submått; money ÄR poängen här). 5 testade:
- 🟡 Försvarsutgifter % BNP (statskontoret UO6-utfall ÷ SCB BNP, 2015-2025, up: 1,1%→2,2%) — ren officiell data,
  on-topic (submåttet ÄR ekonomisk ambition) MEN money-proxy + forsvarsanslag är medvetet *target* + skulle
  attachas mot upptrappnings-åtagandet (commitment vs utfall) → **SIGN-OFF (toppkandidat för försvarets 3:e D)**.
- Materielanslag-andel av UO6 (11 år, up) 🟡. Per-capita/absolut UO6 🟡 (överlapp). Genomförandegrad UO6 🔴 (platt ~100%).

**civil_beredskap** (D-tomt). 5 testade — 🔴 VÄGG bekräftad djupare:
- Civilpliktiga: bara 2024 (1 år, civilplikt återaktiverad jan 2024) 🔴. Värnplikt-inskrivna (5 år, up) → DUBBLERAR
  personal_varnpliktiga (militar_formaga) 🔴 ej för civil. Beredskapslager (Socialstyrelsen) 🔴 ej publik årsserie.
  FFO-medlemmar 🔴 ej aggregerad. Räddningstjänst responstid (Kolada U07442, 4 år) 🔴 PLATT (11,2-11,4 min, inget tecken).
  RSA-kommuner 🔴 ej maskinläsbar. → Bekräftar: civil beredskap har ingen neutral officiell utfallsårsserie (bara pengar/anslag).

**genomforbarhet_leverans** (D-tomt). 5 testade — 🟡 sign-off:
- FMV leveranser SEK till FM (FMV ÅR, 2023-2025: 8,7→11,4→18 mdr, up) → 🟡 money-proxy (men on-topic leverans).
- FMV leveransindex (2021-2025: 79/97/72/73/53) → 🟡 VOLATIL + FMV säger nedgången beror på industrikapacitet/
  överplanering, ej politik → attribution-problem. Genomförandegrad/antal system/försenade-andel 🔴 ej standardiserat.

---

## 4. Sammanfattning & rekommendationer (morgon)

### Vad djupsvepet gav (90 kandidater fullt testade)

| | Antal | Vilka |
|---|---|---|
| ✅ **Byggda rena v0 (i svepet)** | **2** | `brukarnojdhet_hemtjanst` (omsorg_personal), `utslappsintensitet` (kostnadseffektivitet) |
| 🟡 **Buildable-pending (1 steg kvar)** | 3 | KOS-3årsåterfall (kräver Excel-tabellbilaga, figur ej säker), FMV leveranser SEK (extrahera 2021-22), migration handläggningstid (ny MV xlsx-adapter) |
| 🟡 **Sign-off (data finns, men riktning/neutralitet/attribution/semantik)** | ~14 | ekonomi inflation+offentliga_finanser-proxyer, försvar % BNP + leveransindex, klimat skyddad natur/fågelindex/industri-GHG, migration öppna-ärenden, forebyggande ungdomsbrott, demokrati (Domstolsverk/JK/Riksrevision/hemliga tvångsmedel) |
| 🔴 **Genuin vägg (testat mot källan)** | resten | civil_beredskap, mediefrihet, personalomsattning, valfardsbrottslighet, m.fl. |

### De stora lärdomarna (poängen med övningen)
1. **"Saknad data" ≠ sant i de flesta fall.** För target-submåtten (inflation, offentliga finanser) finns rena
   26-30-årsserier; för demokrati finns 20+ officiella årsserier. Blockeraren är nästan aldrig *tillgänglighet*
   utan **riktning/neutralitet/attribution**. → validerar target-design + coverage-krympning starkt.
2. **Figurer ≠ tabeller.** KOS-återfall och Migrationsverkets öppna-ärenden ligger i diagram; exakta årsvärden
   ej extraherbara ur huvud-PDF. För platta serier (KOS) gör det sign-only D osäkert → kräver tabellbilaga.
3. **Demokrati är en äkta mätbarhetsvägg** (alla 20 kandidater tvetydiga/endogena/värdeladdade/förbjudet-index).
4. **Neutralitet är den vanligaste blockeraren** — flest kandidater faller på att riktningen kodar en
   politisk preferens (skuld ned, mer övervakning, färre återvändandeärenden, mer skyddad natur, mer försvarspengar).
5. Infra: Kolada **v2 nedlagt (410) → v3**; repo-adaptern fungerar. PDF-pipelinen (pdfplumber) fungerar för text
   men inte för diagram-inbäddade värden.

### Rekommenderade nästa byggen (kräver din sign-off — riktning/neutralitet)
- **Försvar 3:e D:** `forsvarsutgifter_andel_bnp_upptrappning` (% BNP, statskontoret÷SCB) — money-proxy men on-topic
  för ekonomisk_ambition; öppnar ett 3:e försvarssubmått (adresserar din scenariokritik om finansieringsambition).
- **Klimat bredd:** häckande-fåglar-index (biologiskt utfall, neutralast) ELLER skyddad natur (maskinläsbar) → biologisk_mangfald.
- **Välfärd/Trygghet:** KOS-3årsåterfall via tabellbilaga → aterfall_kriminalvard.
- **Avstå (mot neutralitet):** ekonomi target-proxyer, demokrati-aktivitetsmått, migration-återvändande → behåll
  target/krymp hellre än tvinga fram värdeladdade D.

---

## 5. BESLUT (din sign-off 2026-06-09) — byggkö för FÄRSK SESSION

> Diskussionen avslutad här (kontext slut). Bygg ej nu — exekvera i ny session.

**🔑 Bärande princip du formulerade (gäller all D framåt):** *D ska mäta VERKLIGA EFFEKTER, inte aktivitet/
insats.* Din liknelse: "Fler avlyssningstillstånd säger inget om vad avlyssningen bidrar med — som att räkna
hammare för att veta om huset är byggt." → rena insats-/aktivitetsmått diskvalificeras som D.

### ✅ BYGG (i färsk session)
1. **Försvarsutgifter (% av BNP) → ekonomisk_ambition** (försvarets 3:e D). JA (Hög 1): "tycker jag försvaret
   är viktigt är en högre försvarsbudget bra." Källa: statskontoret UO6-utfall ÷ SCB BNP, 2015–2025.
   ⚠️ **LÖS FÖRST (spänning mot din egen hammare-princip):** försvarsbudget är en INSATS/pengar, och delpoäng
   **A mäter redan budgetprioritering** → risk för dubbelräkning + krock med "effekt, ej aktivitet". Dubbelkolla
   i färsk session om detta hör hemma i D eller egentligen är A. Om vi behåller i D: motivera explicit som
   "utfall av finansieringsambition", ej A-dubblett. (Du sa ja; jag flaggar metodspänningen ärligt.)
2. **Återfall i brott → aterfall_kriminalvard** (trygghet). JA (Hög 4): hämta Kriminalvårdens **Excel-
   tabellbilaga** (KOS) för exakta årsvärden (huvud-PDF har bara diagram), bygg sign-only D. Äkta effekt.
3. **Häckande fåglar-index → biologisk_mangfald** (klimat). JA (Hög 4): bygg HTML-scrape-adapter för
   sverigesmiljomal.se (Svensk Fågeltaxering). Äkta naturUTFALL (ej "skyddad mark" = insats/hammare).

### 🚫 AVSTÅ (behåll neutralt/target)
- **Statsskuld/överskott** (ekonomi): NEJ (Hög 1) — ekonomi har redan god täckning, chansa inte. Behåll target.
- **Migration (återvändande) · övervakning (avlyssningstillstånd) · naturskydd (skyddad mark)**: NEJ (Hög 2) —
  INSATS/aktivitet, ej effekt. (Notera: detta är samma princip som gör att naturskydd-arealen ratas men
  fågelindexet byggs.)
- **Demokrati-aktivitetssiffror** (mutbrott-anmälningar, granskningar, klagomål): NEJ som svenska aktivitetsmått.

### ❓ ÖPPEN DESIGNFRÅGA (eget beslut nästa session) — Hög 3: demokrati via EXTERN utvärderare
Din poäng: demokrati är till stor del en *självutvärdering ur statsapparatens perspektiv* → en **extern,
oberoende** bedömare är metodiskt LÄMPLIGARE än att staten betygsätter sig själv. Att utreda:
- **Stark öppning:** **V-Dem-institutet drivs från Göteborgs universitet** → kan räknas som *svensk akademisk*
  källa, vilket CLAUDE.md redan tillåter "när officiell statistik saknas" → kanske INGEN regeländring behövs!
  (Till skillnad från TI CPI / RSF / Freedom House som är utländska.)
- Frågor att lösa: vilka V-Dem-index? är de neutrala nog (egna metoddebatter)? bara demokrati-kategorin? hur
  väga extern bedömning mot resten (svensk officiell data)? bryter det "hammare"-principen (V-Dem ÄR en
  effekt-/tillståndsbedömning, ej aktivitetsräkning → passar principen bra).
→ Kärnregel-/designbeslut → eget sign-off, ej autobygge. **Högt värde:** skulle kunna lösa demokrati-väggen.
