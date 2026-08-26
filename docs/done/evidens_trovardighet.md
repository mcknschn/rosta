# Rösta — Evidens & trovärdighet (B-spåret): arbetslogg & metodutveckling

> ✅ **B-SPÅRET SIGNERAT / SLUTFÖRT 2026-06-07** — arkiverat i `docs/done/`. Hela §8.8-sign-off-ytan avgjord
> (se §8.8 + beslutslogg §9): 6 B-mått godkända, version 1→2, snapshot re-baselinad, dubbelräkning åtgärdad,
> migration omverifierad, döda indikatorer→BEVAKA. **§4.3 förblir den LEVANDE kanoniska ordlistan**
> (Kategori→Undermått→Indikator→Riktning) som IDEA/DATA/BACKLOG pekar på. Dokumentet återupptas vid framtida
> B-leverans (HOLD-triggrar faller in) eller om **viktad stance** ändrar B-modellen → flyttas då tillbaka till `docs/`.

> **Levande arbetsdokument.** Spårar arbetet med att höja **B** (delpoäng evidens/träffsäkerhet,
> 0,35 av varje kategoripoäng) — både *täckning* (fler undermått med partikopplad evidens) och
> *trovärdighet* (källkvalitet, neutralitet, verifierbarhet).
> Skapad 2026-06-06 efter att natten gav **1 byggt mått** trots research i fem kategorier.
> Bärande omtag (2026-06-06): **måttet och positioneringen är två skilda steg** (§2). Mycket av
> det vi kallade "väggen" var i själva verket ett källval i steg 2, inte ett fel i måttet.
>
> Relaterat: metoden i [fas4b_partistandpunkter_metod.md](fas4b_partistandpunkter_metod.md)
> (källhierarki, instrument-regeln, verifiering), planen i [BACKLOG.md](../BACKLOG.md) (Spår B),
> grundprincipen i [../IDEA.md](../../IDEA.md), datamodellen i [../DATA.md](../../DATA.md).

---

## 0. Varför denna fil finns

Natten 2026-06-06 var uppdraget "nå 4 undermått i välfärd, försvar, integration, trygghet och
klimat". Resultatet blev **1 mått** (försvar/nato_medlemskap) — inte av brist på letande (varje
röstsiffra verifierades mot data.riksdagen.se) utan för att metoden vi körde, **ren votering + krav
på differentiering**, blandade ihop två frågor som borde hållas isär (§2). Filen finns för att:

1. hålla **tvåstegsmodellen** (§2) levande så vi inte återfaller i votering-fixeringen,
2. skilja **äkta hinder** (steg-1: måttet saknas) från **källval** (steg-2: var positioneringen bor) (§4),
3. samla ett **metodregister för positionering** (§5) — fler officiella källor, samma stränghet,
4. hålla **statustavla** (§6), **kandidat-pipeline** (§7) och **beslutslogg** (§9) uppdaterade,
   så att versionsstyrd config alltid kan spåras till ett resonemang.

Bärande princip oförändrad (CLAUDE.md): inget partibetyg eller mänskligt omdöme i kod — bara i
versionsstyrd config; all data spårbar till en officiell svensk källa; värdeneutralitet är kärnan.

---

## 1. Mål & spelregler

**Mål:** varje kategori ska ha **≥4 undermått med aktiv partikopplad B-evidens** *där det är möjligt*
(vissa undermått saknar indikator, vissa indikatorer är `target` utan riktning — se §4). Fler täckta
undermått → mindre coverage-krympning mot neutral 2,5 → B får faktiskt genomslag och vilar inte på en
enda rad.

**Spelregler (beslutade med användaren, gäller tills annat sägs):**

| Regel | Innebörd |
|---|---|
| **Neutralitet före 4** | Bygg hellre färre mått än ett som tiltar vänster/höger eller regering-vs-opposition. Ett tiltat mått skadar trovärdigheten mer än ett saknat mått. Gäller hur vi *positionerar* — inte ett krav på att ett mått ska särskilja (§2). |
| **Svensk-först** | Riktningsbelägget (evidensliggaren) ska vara officiell svensk källa; akademisk svensk när officiell statistik saknas. Mellanstatliga Sverige-utvärderingar (EU:s rättsstatsrapport, GRECO, OECD) **endast som bekräftelse** — aldrig primär, aldrig index (DATA.md, beslut 2026-06-05). Internationella **index** (RSF/CPI/Freedom House/V-Dem) är förbjudna. |
| **Bygg rena, håll tveksamma** | Endast mått som passerar alla grindar (§10) byggs nu. Tveksamma kandidater hålls i §7 för diskussion, byggs inte autonomt. |
| **Versionen bumpar bara användaren** | Config byggs i `version 0`/förslag; människan signerar och bumpar. |

---

## 2. Tvåstegsmodellen: måttet vs positioneringen ⭐

Den bärande insikten (2026-06-06): **ett mått, och hur vi positionerar partier på det, är två skilda
steg.** Vi behandlade dem länge som ett — "finns en ren votering?" fick avgöra både om måttet dög
*och* hur partierna placerades. Det var fel.

- **Steg 1 — Måttet.** Ett undermått + en indikator (med riktning) + ett policyinstrument + **officiell
  svensk evidens att instrumentet flyttar indikatorn** åt det håll partiet påstår. Det här avgör om
  måttet *finns* och är trovärdigt. Oberoende av vilka partier som råkar stödja det.
- **Steg 2 — Positioneringen.** *Var* visar sig varje partis hållning på instrumentet? Votering,
  betänkande, reservation, kommittémotion, budgetmotion, valmanifest — en hel stege (§5.1).
  Acklamation slår bara ut *votering*-källan; den säger ingenting om de andra.

**Följder:**

1. **Ett bra mått kan inte underkännas för att voteringen är acklamation.** Det är ett steg-2-problem
   (källval), inte ett steg-1-problem (måttkvalitet). Måttet kan vara utmärkt — vi hämtar
   positioneringen någon annanstans.
2. **Differentiering är ett *utfall*, inte ett inträdeskrav.** Skiljer sig partierna faktiskt syns det
   i positioneringssteget; gör de inte det är måttet ändå korrekt (bidrar till täckning/trovärdighet,
   bara inte till rankning). Differentiering spelar roll för *rankningsnytta*, aldrig för *korrekthet* —
   och är aldrig värt en tilt.
3. **"Icke-differentierande" var en felbenämning.** Det jag tidigare kallade så var att *voteringen*
   inte särskiljer — vilket inte säger något om budget/motioner. Rätt term: **voterings-konsensus**,
   som inte utesluter budget-/motionsdifferentiering.

**Men steg 2 måste fortfarande gå att mäta vettigt** (gränserna i §5.6). Två fallgropar att hålla emot:

- **Mål vs instrument.** Manifest uttrycker oftast *mål* ("korta vårdköerna"), inte instrument.
  Positionerar vi löst på målspråk blir alla = `supports` på allt → B mättar mot 5 för alla → *mindre*
  sant än voteringar. Instrument-grinden (§10) måste följa med till *alla* källor.
- **Gradskillnad ryms inte i dagens modell.** `party_positions` kodar binärt `supports`/`opposes` —
  ingen magnitud. Att "alla stödjer men S satsar mer än M" går att *se* i budgetar men **inte att
  koda** utan modellutvidgning. Tills dess fångar steg 2 *riktning* (finansierar/avvecklar
  instrumentet), inte *grad*.

---

## 3. Var vi står (uppdateras per leverans)

Aktiv partikopplad B-evidens per kategori (källa: `python -m pipeline.tools.coverage_report`,
B4-grind `b_submeasure_spread`). **Senast uppdaterad 2026-06-07 — ✅ SIGN-OFF GENOMFÖRD (B-grön- + integration-svepen godkända; version 1→2; snapshot re-baselinad). Se §8.8/§9.**

| Kategori | Undermått m. B-evidens | Status |
|---|---|---|
| demokrati | **5/5** | ✅ **FULLT** — transparens_ansvar byggt 2026-06-07 (insyn partifinansiering, lagen 2018:90/KU19 p1) |
| trygghet | **5/5** | ✅ **FULLT** — forebyggande byggt 2026-06-07 (lagen 2023:196/JuU9 p1; tidigare utan indikator) |
| valfard | **4/4** | ✅ **FULLT** — vard_tillganglighet (NHV→överlevnad) + omsorg_personal (kontinuitet) byggt 2026-06-07 |
| ekonomi | **4/6** | ✅ alla 4 B-möjliga täckta; **offentliga_finanser HOLD-kontext** (codex: åtstramnings-tilt), inflation = target |
| forsvar | **4/5** | ✅ ekonomisk_ambition byggt 2026-06-07 (upptrappning mot mål, FöU2 p1+p5); **genomforbarhet_leverans HOLD** (steg-2-tilt) |
| klimat | **4/5** | **industriell_konkurrenskraft HOLD** (dubbelvägg: RiR 2024:17 + MJU15-tilt) |
| integration | **3/5** | migrationssystem byggt 2026-06-07 (atervandande_effektivitet, RiR 2020:7, tvåsidig split); **boendesegr./normer_tillit HOLD** (genuina väggar, högsta bias-risk) |

**B-grön-svepet 2026-06-07 (användarmandat "varje undermått ≥1 B-grön"):** 11 parallella researchagenter +
codex adversariell granskning → **5 byggda** (alla enhällighet-som-källa §5.2, alla 8 supports,
icke-rankningsdrivande, v0/low/low, FLAGGADE för sign-off), **5 HOLD** (genuina väggar, sign-off-kandidater
i §6/§8.7) + **offentliga_finanser HOLD-kontext** (codex). 3 kategorier nådde FULLT (demokrati/trygghet/valfard),
forsvar 3/5→4/5.

**Integration-svepet 2026-06-07 (forts.):** **migrationssystem byggt** (atervandande_effektivitet via RiR 2020:7,
negativ-evidens-vinkeln; **genuin tvåsidig split** — appens första differentierande integration-B-mått, ej
enhällighet) → **integration 2/5→3/5**. **boendesegregation** (kamera-väg byggd → reverterad av codex: trygghet-
relabel + dubbelräkning) och **normer_tillit** (steg 1 löst/Delmi 2025:5, steg 2 saknas) förblir HOLD.

¹ Undermått vars indikator har en riktning (≠ `target`) **och** kan kopplas till en åtgärdstyp med
  evidensbelagd riktning.

**Sammanlagt:** 43 evidensposter / 247 ståndpunkter (2026-06-07: B-grön-svepet +5 poster/+40 ståndpunkter; integration-
svepet +1 post/+7 ståndpunkter [migration, V utelämnat]). `dist/`-snapshot **re-baselinad vid sign-off 2026-06-07** (drift nollställd; den ackumulerade svep-effekten inlåst — vid baslinjebytet flippade SD>V längst ner, topp 6 oförändrad). **B-grön-svepets ISOLERADE
effekt** (current dist vs git HEAD): **ranking OFÖRÄNDRAD** (S > L > M > KD > MP > C > SD > V), alla 8 partier +0,018…+0,109
total (alla cellförändringar positiva — inget parti straffas, omöjligt att tilta då alla supports); störst lyft
till tidigare under-täckta (SD +0,109 via valfard, MP +0,053 via forsvar) = täckningsifyllnad, ej bias.

---

## 4. Vad som verkligen blockerar — steg-1-väggar vs steg-2-källval

Med tvåstegsmodellen faller det mesta av "väggen" jag beskrev natten. Den var till stor del ett
**steg-2-artefakt**: vi använde nästan bara voteringar för positionering, och acklamation slår ut just
den källan. Sorterat på vad som *verkligen* hindrar:

### 4.1 Inte äkta väggar — bara steg-2-källval (lösbara genom att byta källa)
- **Acklamation på sakpunkten** (snabbförfarande, invasiva arter, materielpunkter, hedersvåld, EMFA) →
  voteringen är noll, men ett enhälligt betänkande eller en kommittémotion belägger ändå hållningen
  (§5.2–5.3).
- **Buntad omnibus** (FöU3 buntad med Israel-export; KU12 buntad med SD:s grundlagsreservation) →
  voteringens innebörd är tvetydig, men en instrument-specifik kommittémotion är entydig.
- **Avslags-tilt** → den enda voteringen är tiltad, men andra källor kan ge neutral positionering —
  eller så speglar tilten genuin *nuvarande* differentiering, vilket är ok om värdeneutralt belagt.

### 4.2 Äkta väggar — steg-1, måttet självt saknas
Ingen källa i världen hjälper; måttet existerar inte förrän en indikator med svensk auktoritetsbelagd
riktning läggs till (§5.7).

| Kategori | Undermått | Steg-1-hinder |
|---|---|---|
| trygghet | `forebyggande` | saknar indikator |
| klimat | `industriell_konkurrenskraft` | saknar indikator |
| integration | `migrationssystem` | saknar indikator |
| försvar | `ekonomisk_ambition` | indikator = `forsvarsanslag_andel_bnp` (`target`, ingen upp/ned) |
| ekonomi | inflation, offentliga finanser | `target` (nära mål ≠ "uppåt bra") |

→ Kräver **modellutvidgning**; tas upp som designfrågor, byggs inte autonomt.

---

## 4.3 Begreppsmodell + mätbarhetskarta per indikator (samtliga mått) ⭐

> Tillagd 2026-06-06 på användarens begäran: (a) en **stringent begreppsmodell** — samma namn i alla
> dokument, och (b) en **mätbarhetskarta** — kan varje indikator faktiskt mätas? Detta avsnitt är den
> **auktoritativa ordlistan** för hela projektet; IDEA.md, DATA.md, BACKLOG.md och ROADMAP.md använder
> samma termer (terminologin normaliserades 2026-06-06: "submått" → **Undermått**).

### Begreppsmodell (ordlista) — fyra nivåer, ETT namn var

| Nivå | Kanoniskt namn | Kod-nyckel (sanningskälla) | Exempel |
|---|---|---|---|
| 1 | **Kategori** | `categories[].id` | Försvar och beredskap (`forsvar`) |
| 2 | **Undermått** | `submeasures[].id` | Militär förmåga (`militar_formaga`) |
| 3 | **Indikator** | `indicators[].id` | Försvarsanslag som andel av BNP (`forsvarsanslag_andel_bnp`) |
| 3b | **Riktning** | `indicators[].direction` | upp · ned |
| 3c | **Verkan** | `evidence_ledger.entries[].direction` | åtgärden rör indikatorn åt rätt håll (`positive`) · åt fel håll (`negative`) · oklart/blandat (`unclear`/`mixed`) |
| 3d | **Uteslutningsskäl** | `indicators[].exclusion` | gränsfel (`gransfel`) · giltighetsfel (`giltighetsfel`) · neutralitetsfel (`neutralitetsfel`) |

**Regel mot begreppsförvirring:** `config/categories.yaml` är sanningskälla; **id:t** (t.ex. `nato_ukraina`) är
det som aldrig får glida mellan dokument. De svenska visningsnamnen ovan är kanoniska — använd dem i all prosa.
*Retirerade synonymer:* "submått" → **Undermått** (kod-nyckeln heter fortfarande `submeasures`/`submeasure`,
engelska — det är samma begrepp); "mätpunkt"/"mått" → **Indikator**. Varje indikator har EN riktning:
`up` → upp, `down` → ned. Värdet `target` (målnivå) är avfört 2026-08-26 av
[ADR 0011](../adr/0011-uteslutningen-ar-ett-eget-besked.md); se raden om Uteslutningsskäl nedan.

**Riktning och Verkan är två storheter, inte en.** Riktning tillhör indikatorn och säger vilket håll som
är bättre. Verkan tillhör evidensliggarens post och säger om åtgärden rör indikatorn åt det hållet.
Båda fälten heter `direction` i config, vilket bryter mot regeln ovan om ett namn per begrepp. I prosa
används alltid **Riktning** respektive **Verkan**. Confignycklarna byts först när en byggslice rör filerna,
på samma sätt som `A_agerande` och `C_ansvar`. Låst 2026-08-21 av
[ADR 0006](../adr/0006-evidensgrinden-ar-symmetrisk.md) (biljett #18 under karta #6).

**Riktning och Uteslutningsskäl utesluter varandra.** Riktning är ett besked om indikatorn, alltså vilket
håll som är bättre. **Uteslutningsskäl** är ett besked om modellen, alltså varför indikatorn inte poängsätts.
En indikator bär det ena eller det andra, aldrig båda och aldrig ingetdera. Fältet `exclusion` är sitt eget
skäl: finns det är indikatorn utesluten, och värdet namnger felet. De tre värdena pekar var och ett på en
beslutad regel: `gransfel` på [ADR 0001](../adr/0001-a-mater-prioritering.md) (frågan ägs av en annan
delpoäng), `giltighetsfel` på [ADR 0009](../adr/0009-sakerheten-mater-hur-val-talet-ar-kant.md) (utfallet
kan inte tillskrivas ett parti) och `neutralitetsfel` på CLAUDE.md:s neutralitetskrav (det bättre hållet
går inte att ange utan att ta ett partis parti). *Kollision att hålla isär:* `coverage_exclude` i
`config/scoring.yaml` utesluter **åtgärdstyper** ur B:s nämnare, alltså ett annat objekt och en annan
mekanism. Liggarens `admitted` bär ADR 0006:s evidensgrind och används aldrig om indikatorer. Låst
2026-08-26 av [ADR 0011](../adr/0011-uteslutningen-ar-ett-eget-besked.md) (biljett #13 under karta #6). (Visningsnamnen för Kategori/Undermått hämtas ur `categories.yaml`
`name`-fältet — fyra trunkerade namn rättades 2026-06-06: Nato/Skola/Normer/Finansiering hade kapats av
oquoterade kommatecken.)

### Delpoäng (ordlista) — fyra delar, ETT namn var

Låst 2026-08-17 av [ADR 0001](../adr/0001-a-mater-prioritering.md) (biljett #7 under karta #6).
Vikterna låsta 2026-08-18 av [ADR 0002](../adr/0002-kategoripoangens-ansprak-och-vikter.md)
(biljett #9 under samma karta).

**Anspråket:** ett kategoribetyg svarar på frågan hur mycket kategorin väntas förbättras om partiets
politik genomförs. D är ett kontrolled som kan säga emot anspråket.

| Del | Kanoniskt namn | Vikt | Frågan delen ställer | Kod-nyckel |
|---|---|---|---|---|
| A | **Prioritering** | 0,30 | Hur stor andel av partiets föreslagna anslag och egna motioner går till kategorin? | `A_agerande` |
| B | **Evidens** | 0,50 | Hur stor förbättring väntas av de åtgärder partiet driver? Storlek ur `effect_strength`, säkerhet ur `evidence_level` och `confidence` ([ADR 0004](../adr/0004-vad-delpoang-b-mater.md)). | `B_evidens` |
| C | **Maktandel** | 0 | Har partiet haft makt att påverka, och hur mycket? Upplysning, ej attribution. | `C_ansvar` |
| D | **Resultat** | 0,20 | Har indikatorerna förbättrats där partiet haft ansvar? | `D_resultat` |

**Regel mot dubbelräkning:** gränsen mellan delpoängen går vid **frågan**, inte vid källan. Samma dokument
får svara på flera av frågorna. Samma fråga får aldrig räknas två gånger. En budgetmotion ger därför både
A sina ramar per utgiftsområde och B en ståndpunkt på ett instrument, utan att något räknas dubbelt.

*Retirerad synonym:* "Faktiskt agerande" → **Prioritering**. A mäter omfattning, aldrig riktning och aldrig
kvalitet. Riktningen bor i B. Konfignyckeln heter fortfarande `A_agerande` tills en byggslice byter den.
Voteringar är en källa till **ståndpunkt** och hör därmed till B, inte till A.

*Retirerade synonymer:* "Genomförbarhet/ansvar" och "Ansvarsunderlag" → **Maktandel**. Ordet
*ansvarsunderlag* är upptaget av D:s grindstorhet, alltså Σ maktvikt över de år partiet faktiskt
attribueras (`config/scoring.yaml:141`). Det är en annan storhet med en annan nämnare, och den
användningen är äldre och sitter i confignycklar. C är inte längre en delpoäng och ger
inga poäng. Storheten räknas ut som förut och redovisas som upplysning om vem som haft makten, och
ingenting mer. Den bär INTE attributionen för D: den grinden (`min_responsibility`) läser D:s eget
`basis` i `category_d`, aldrig `government_fractions()`. Se ADR 0002 § Rättelse 2026-08-18. Skälet
att C inte ger poäng: anspråket villkorar redan på att politiken genomförs, så innehavd makt svarar
på en fråga betyget inte ställer. Konfignyckeln `C_ansvar` behålls med vikten 0, eftersom `pipeline/config.py` kräver alla fyra
nycklarna.

*Retirerad synonym:* "Evidens/träffsäkerhet" → **Evidens**. Ordet *träffsäkerhet* svarar på om ett
förslag träffar rätt, alltså en ja/nej-fråga om riktning, och det är precis det anspråk
[ADR 0004](../adr/0004-vad-delpoang-b-mater.md) drog tillbaka. B svarar på hur STOR förbättring som
väntas: `effect_strength` bär storleken och går in i talet, `evidence_level` och `confidence` bär
säkerheten och går till etiketten och därmed till bandet. Konfignyckeln `B_evidens` är oförändrad.
Ordet retirerades ur `IDEA.md`, `DATA.md`, `README.md`, `docs/BACKLOG.md` och `config/scoring.yaml`
i byggslicen [#17](https://github.com/mcknschn/rosta/issues/17).

### Cellens två redovisade storheter: Täckning och Säkerhet

Låst 2026-08-23 av [ADR 0008](../adr/0008-cellens-tackning.md) (biljett #12 under karta #6).

| Storhet | Frågan den ställer | Var den bor |
|---|---|---|
| **Täckning** | Hur stor del av cellens betyg vilar på mätt underlag? | Ett tal per (parti, kategori) i `scores.json`, vägt `0,30 x A + 0,50 x B + 0,20 x D` |
| **Säkerhet** | Hur säkert är det som är mätt? | En nivå per delpoäng (`high`/`medium`/`low`), hopvägd till bandets halvbredd |

**Täckning och Säkerhet är två storheter, inte en.** En fullt täckt cell kan vila på svag evidens,
och då är det bandet som bär beskedet. Täckningen ändrar aldrig poäng, band eller rangordning: tunn
täckning verkar redan på modellen genom `thin_coverage`, som sänker Säkerheten ett steg, och att
låta den verka igen vore dubbelräkning. Ordet **täckning** användes redan om B och D var för sig;
ADR 0008 gör det till kategorinivåns hopvägning av samma sak.

*Retirerad synonym:* "Tillförlitlighet" → **Täckning**. Ordet *tillförlitlighet* lovar att cellen är
pålitlig, medan storheten mäter hur stor del som är mätt. Det är två skilda påståenden, och att
blanda dem vore samma fel som *träffsäkerhet* gjorde för B. Bygge:
[#29](https://github.com/mcknschn/rosta/issues/29).

**Säkerheten mäter hur väl talet är känt, aldrig vad talet säger.** Låst 2026-08-26 av
[ADR 0009](../adr/0009-sakerheten-mater-hur-val-talet-ar-kant.md) (biljett #30). En delpoäng vars
underlag är räknat och fullständigt är väl känd även när talet den ger ligger nära mitten. Att ett
parti ligger nära normen är ett fynd om världen, inte ett tecken på att vi vet talet sämre. Regeln
avgör vad som får bli en säkerhetsnivå: hur nära nollpunkten ett tal ligger får det inte, och
inte heller att en delpoäng mäter fel storhet för ett parti. Det senare är ett **giltighetsfel**,
och att möta det med ett bredare band vore att tapetsera över det.

**A:s `high` i 56 av 56 celler är ett fynd, inte en form** (ADR 0009 punkt 2). Ingenting i A
skattas: a1:s ramar är transkriberade och citerar sin källrad, a2 räknar motioner och den tunnaste
cellen bär 84. Konstanten skiljer sig därmed från de konstanter ADR 0004 och ADR 0005 fann, som
båda satt i **betyget**. A:s nivå är `band_only` och kan bevisligen inte flytta en rangordning.

**C:s säkerhetsnivå är overksam** (ADR 0009 punkt 5). C väger 0, så dess term i halvbredden är
exakt 0. Nivån står kvar i `scores.json` som upplysning om datatillståndet
(`C_missing_subnational`), men den verkar ingenstans, och `conf-low` i frontend slutar läsa den.
En maktandel har en källa men ingen säkerhet som verkar.

### Känslighetsanalysens storhet: Reglage

Låst 2026-08-26 av [ADR 0010](../adr/0010-ett-reglage-ar-en-vag-pipen-redan-kan-ga.md) (biljett #24
under karta #6).

**Reglage:** en punkt där pipen kan gå en annan väg utan att någon skriver ny kod, och där
underlaget kan uttrycka den vägen. Båda leden krävs. Reglagen står i `robustness.SOURCES` och dras
samtidigt i varje Monte Carlo-dragning (ADR 0003 punkt 4). Listan är ett **register** över byggda
variationspunkter, aldrig ett anspråk på att täcka all osäkerhet i betyget. Att en delpoäng saknar
reglage är därför ett fynd om delpoängen.

*Retirerad synonym:* "Källa" (i betydelsen dragen osäkerhetskälla) → **Reglage**. Ordet *källa*
betyder i det här repot en officiell källa till data, och ett ord får bära en mening. Fältnamnet
`source_influence` i `dist/robustness.json` står kvar tills en schemaändring ändå görs.

**Ett dokumenterat men obyggt alternativ är inget reglage** (ADR 0010 punkt 3). Att en ADR namnger
ett alternativ under "Övervägda alternativ" ger det ingen plats i listan, annars får listan ingen
övre gräns. Faller alternativet in som kod senare blir det ett reglage automatiskt. **Ett dött
reglage stryks med en rad om varför** (punkt 9), som `A_normalization` fick i
[#21](https://github.com/mcknschn/rosta/issues/21).

### Mätbarhet — kan varje indikator mätas?
En indikator bidrar till betyget om den har **B** (partikopplad evidens att ett instrument flyttar den) **eller**
**D** (officiell svensk årsserie). B och D är två vägar — en stängd D dödar inte indikatorn om B bär den (t.ex.
mediefrihet/korruption: D förbjuden/sekretess men B byggd).
**Mätstatus:** ✅ **mäts** (B och/eller D, bidrar nu) · 🟡 **mätbar, ej byggd** (väg finns, jobb kvarstår) ·
🔴 **ej mätbar** (indikator finns men B-vägg + ingen D) · 🔴 **saknar indikator** (inget definierat att mäta —
kräver ny indikator, §5.7) · ⚪ **target** (kontext, ingen riktning, betygssätts ej, renormaliseras bort).

### Mastertabell — samtliga 35 undermått / 55 indikatorer (uppdaterad 2026-06-07, B-grön-svepet)
> ⚠️ **D-kolumnen ("mäts (D)") är INAKTUELL** efter Spår D (Tier 1–4 + djupsvep + V-Dem + integration +
> försvar, t.o.m. 2026-06-12). Denna tabell behålls som **B-/begreppsmodell-vy och historik**; den
> **auktoritativa, aktuella D-täckningsvyn** (38 serier / 28 av 35 undermått, alla 7 kategorier) är
> [spar_D_datatackning.md §2.1](spar_D_datatackning.md). Läs D-status därifrån, ej härifrån.
*B-grön-svepet 2026-06-07 lade till 3 nya indikatorer (forsvarsfinansiering_upptrappning_mot_mal,
kommunalt_brottsforebyggande_arbete, kontinuitet_i_omsorgen) och grönmarkerade 5 undermått (de 5 raderna
markerade "byggt 2026-06-07"). Kvar utan B-grön: 2 undermått som **saknar indikator** (Industriell
konkurrenskraft, Migrationssystemets hållbarhet — steg-1-väggar §4.2) + 4 HOLD-undermått (se §6/§8.7).
Förebyggande arbete har nu en indikator (var tidigare en "saknar indikator"-vägg).*
| Kategori | Undermått | Indikator | Riktning | Mätstatus |
|---|---|---|---|---|
| Ekonomi och jobb | Sysselsättning och arbetslöshet `sysselsattning_arbetsloshet` | Sysselsättning `sysselsattning` | upp | ✅ mäts (B+D) |
| Ekonomi och jobb | Sysselsättning och arbetslöshet `sysselsattning_arbetsloshet` | Arbetslöshet `arbetsloshet` | ned | ✅ mäts (D) |
| Ekonomi och jobb | BNP per capita och produktivitet `bnp_produktivitet` | BNP per capita `bnp_per_capita` | upp | ✅ mäts (D) |
| Ekonomi och jobb | BNP per capita och produktivitet `bnp_produktivitet` | Produktivitet `produktivitet` | upp | ✅ mäts (B+D) |
| Ekonomi och jobb | Reallöner och hushållens ekonomi `realloner_hushall` | Reallöner `realloner` | upp | 🟡 mätbar, ej byggd |
| Ekonomi och jobb | Reallöner och hushållens ekonomi `realloner_hushall` | Hushållens reala disponibla inkomst `hushallens_reala_disponibla_inkomst` | upp | ✅ mäts (B) |
| Ekonomi och jobb | Företagande och investeringar `foretagande_investeringar` | Näringslivets investeringar `naringslivets_investeringar` | upp | ✅ mäts (B) |
| Ekonomi och jobb | Inflation och prisstabilitet `inflation_prisstabilitet` | Inflation (nära mål) `inflation` | målnivå | ⚪ target (kontext) |
| Ekonomi och jobb | Offentliga finanser och långsiktig hållbarhet `offentliga_finanser` | Statsskuld/underskott (hållbar nivå) `statsskuld_underskott` | målnivå | ⚪ target (kontext) |
| Välfärd | Vårdens tillgänglighet och kvalitet `vard_tillganglighet` | Vårdköer `vardkoer` | ned | ✅ mäts (D) |
| Välfärd | Vårdens tillgänglighet och kvalitet `vard_tillganglighet` | Andel som får vård i tid `vard_i_tid` | upp | 🟡 mätbar, ej byggd |
| Välfärd | Vårdens tillgänglighet och kvalitet `vard_tillganglighet` | Överlevnad efter svår sjukdom `overlevnad_svar_sjukdom` | upp | ✅ mäts (B) — byggt 2026-06-07: koncentration_nationell_hogspecialiserad_vard (SOU 2015:98 + SoU18 p1, alla 8) |
| Välfärd | Skolans kunskap och likvärdighet `skola_kunskap` | Skolresultat `skolresultat` | upp | ✅ mäts (B+D) |
| Välfärd | Skolans kunskap och likvärdighet `skola_kunskap` | Skillnader mellan skolor `skillnader_mellan_skolor` | ned | 🟡 mätbar, ej byggd |
| Välfärd | Skolans kunskap och likvärdighet `skola_kunskap` | Behöriga lärare `behoriga_larare` | upp | ✅ mäts (D) |
| Välfärd | Omsorg och personalförsörjning `omsorg_personal` | Personalomsättning i omsorgen `personalomsattning_omsorg` | ned | 🔴 ej mätbar (vägg; behålls separat) |
| Välfärd | Omsorg och personalförsörjning `omsorg_personal` | Kontinuitet i omsorgen `kontinuitet_i_omsorgen` | upp | ✅ mäts (B) — byggt 2026-06-07: fast_omsorgskontakt (prop. 2021/22:116 + SoU24 p2, alla 8); NY indikator (konstrukt = kontinuitet, ej personalomsättning) |
| Välfärd | Finansiering, styrning och anti-fusk `finansiering_styrning` | Välfärdsbrottslighet `valfardsbrottslighet` | ned | ✅ mäts (B) |
| Lag och trygghet | Grov brottslighet och våldsbrott `grov_brottslighet` | Dödligt våld `dodligt_vald` | ned | ✅ mäts (D) |
| Lag och trygghet | Grov brottslighet och våldsbrott `grov_brottslighet` | Skjutningar och sprängningar `skjutningar_sprangningar` | ned | ✅ mäts (B+D) |
| Lag och trygghet | Utsatthet och upplevd trygghet `utsatthet_trygghet` | Brottsutsatthet `brottsutsatthet` | ned | ✅ mäts (B+D) |
| Lag och trygghet | Utsatthet och upplevd trygghet `utsatthet_trygghet` | Upplevd otrygghet `upplevd_otrygghet` | ned | ✅ mäts (D) |
| Lag och trygghet | Rättsväsendets effektivitet `rattsvasendets_effektivitet` | Uppklaringsgrad `uppklaringsgrad` | upp | ✅ mäts (D) |
| Lag och trygghet | Rättsväsendets effektivitet `rattsvasendets_effektivitet` | Handläggningstid `handlaggningstid` | ned | ✅ mäts (B) |
| Lag och trygghet | Förebyggande arbete `forebyggande` | Kommunalt brottsförebyggande arbete `kommunalt_brottsforebyggande_arbete` | upp | ✅ mäts (B) — byggt 2026-06-07: lagstadgat_kommunalt_brottsforebyggande_ansvar (lagen 2023:196, JuU9 p1, alla 8); NY indikator (tidigare saknade undermåttet indikator) |
| Lag och trygghet | Återfall och kriminalvård `aterfall_kriminalvard` | Återfall i brott `aterfall_i_brott` | ned | ✅ mäts (B) |
| Försvar och beredskap | Militär förmåga `militar_formaga` | Personal och värnpliktiga `personal_varnpliktiga` | upp | ✅ mäts (B) |
| Försvar och beredskap | Militär förmåga `militar_formaga` | Ammunition, luftvärn, logistik, cyberförmåga `materiel_formaga` | upp | 🟡 mätbar, ej byggd |
| Försvar och beredskap | Ekonomisk ambitionsnivå och långsiktig finansiering `ekonomisk_ambition` | Försvarsanslag som andel av BNP `forsvarsanslag_andel_bnp` | målnivå | ⚪ target (kontext) |
| Försvar och beredskap | Ekonomisk ambitionsnivå och långsiktig finansiering `ekonomisk_ambition` | Finansieringsupptrappning mot mål `forsvarsfinansiering_upptrappning_mot_mal` | upp | ✅ mäts (B) — byggt 2026-06-07: upptrappning_forsvarsanslag_mot_mal (FöU2 p1+p5, alla 8); NY indikator |
| Försvar och beredskap | Civil beredskap `civil_beredskap` | Civil beredskap (vård, energi, mat, transporter) `civil_beredskap_niva` | upp | ✅ mäts (B) |
| Försvar och beredskap | Nato, Ukraina och internationell trovärdighet `nato_ukraina` | Ukraina-stöd `ukraina_stod` | upp | 🟡 mätbar, ej byggd |
| Försvar och beredskap | Nato, Ukraina och internationell trovärdighet `nato_ukraina` | Nato-interoperabilitet `nato_interoperabilitet` | upp | ✅ mäts (B) |
| Försvar och beredskap | Genomförbarhet och leveranstakt `genomforbarhet_leverans` | Leveranstid för materiel `leveranstid_materiel` | ned | 🔴 ej mätbar (vägg) |
| Klimat, miljö och energi | Utsläppsminskningar `utslappsminskningar` | Territoriella utsläpp `territoriella_utslapp` | ned | ✅ mäts (B+D) |
| Klimat, miljö och energi | Utsläppsminskningar `utslappsminskningar` | Konsumtionsbaserade utsläpp `konsumtionsbaserade_utslapp` | ned | ✅ mäts (D) |
| Klimat, miljö och energi | Energiförsörjning och elpriser `energi_elpriser` | Fossil energianvändning `fossil_energianvandning` | ned | ✅ mäts (D) |
| Klimat, miljö och energi | Energiförsörjning och elpriser `energi_elpriser` | Elprisvolatilitet `elprisvolatilitet` | ned | 🟡 mätbar, ej byggd |
| Klimat, miljö och energi | Energiförsörjning och elpriser `energi_elpriser` | Effektbrist `effektbrist` | ned | ✅ mäts (B) |
| Klimat, miljö och energi | Omställningens kostnadseffektivitet `kostnadseffektivitet` | Utsläppsminskning per krona `utslappsminskning_per_krona` | upp | ✅ mäts (B) |
| Klimat, miljö och energi | Biologisk mångfald och natur `biologisk_mangfald` | Hotade arter / naturförlust `hotade_arter_naturforlust` | ned | ✅ mäts (B) |
| Klimat, miljö och energi | Industriell konkurrenskraft i omställningen `industriell_konkurrenskraft` | _(ingen indikator definierad)_ | — | 🔴 saknar indikator |
| Integration och social sammanhållning | Arbete och självförsörjning `arbete_sjalvforsorjning` | Sysselsättningsgap inrikes/utrikes födda `sysselsattningsgap_inrikes_utrikes` | ned | ✅ mäts (B+D) |
| Integration och social sammanhållning | Arbete och självförsörjning `arbete_sjalvforsorjning` | Självförsörjningsgrad `sjalvforsorjningsgrad` | upp | ✅ mäts (D) |
| Integration och social sammanhållning | Arbete och självförsörjning `arbete_sjalvforsorjning` | Bidragsberoende `bidragsberoende` | ned | ✅ mäts (B+D) |
| Integration och social sammanhållning | Skola, språk och utbildning `skola_sprak` | SFI-resultat/språkkunskaper `sfi_sprakkunskaper` | upp | 🟡 mätbar, ej byggd |
| Integration och social sammanhållning | Skola, språk och utbildning `skola_sprak` | Skolresultat i utsatta områden `skolresultat_utsatta_omraden` | upp | ✅ mäts (B) |
| Integration och social sammanhållning | Boendesegregation och trygghet `boendesegregation` | Trångboddhet `trangboddhet` | ned | ✅ mäts (D) |
| Integration och social sammanhållning | Boendesegregation och trygghet `boendesegregation` | Segregation `segregation` | ned | 🔴 ej mätbar (vägg) |
| Integration och social sammanhållning | Normer, tillit och samhällsgemenskap `normer_tillit` | Tillit och valdeltagande `tillit_valdeltagande` | upp | 🔴 ej mätbar (vägg) |
| Integration och social sammanhållning | Migrationssystemets hållbarhet `migrationssystem` | _(ingen indikator definierad)_ | — | 🔴 saknar indikator |
| Frihet, demokrati och institutioner | Rättsstat och maktdelning `rattsstat_maktdelning` | Otillbörlig politisering av myndigheter `otillborlig_politisering` | ned | ✅ mäts (B) |
| Frihet, demokrati och institutioner | Korruption och myndighetstillit `korruption_tillit` | Korruption `korruption` | ned | ✅ mäts (B) |
| Frihet, demokrati och institutioner | Korruption och myndighetstillit `korruption_tillit` | Förtroende för domstolar/myndigheter `fortroende_domstolar_myndigheter` | upp | 🟡 mätbar, ej byggd |
| Frihet, demokrati och institutioner | Yttrandefrihet och medier `yttrandefrihet_medier` | Mediefrihet `mediefrihet` | upp | ✅ mäts (B) |
| Frihet, demokrati och institutioner | Personlig frihet och integritet `personlig_frihet` | Övervakning utan rättssäkerhet `overvakning_utan_rattssakerhet` | ned | ✅ mäts (B) |
| Frihet, demokrati och institutioner | Transparens och ansvarsutkrävande `transparens_ansvar` | Politisk transparens `politisk_transparens` | upp | ✅ mäts (B) — byggt 2026-06-07: insyn_partifinansiering (lagen 2018:90, KU19 p1, alla 8) |

### Vad kartan säger — efter B-grön-svepet + integration-svepet 2026-06-07
**Status per undermått (35 totalt):** **29 har nu en B-grön indikator** (23 sedan tidigare + 5 i B-grön-svepet
+ 1 i integration-svepet: migrationssystem). **6 saknar B-grön:** 4 HOLD-undermått (genuina väggar) + 2 target-/
kontext-undermått (medvetet).
1. **✅ Mäts via B (bidrar nu)** — 29 undermått. Värdeneutralt skydd: indikatorer utan D bärs ändå av **B**
   (nato_interoperabilitet, mediefrihet, korruption, + de 6 nya). 5 nya är enhällighet-konsensus (alla 8
   supports, icke-rankningsdrivande); det 6:e (migrationssystem via RiR 2020:7) är en **genuin tvåsidig split**
   (5 supports/2 opposes/V none) med värdeneutralt auktoritetsankare. Alla v0, FLAGGADE för sign-off.
2. **🟡 Mätbar, ej byggd (8 st kvar)** — bonus-indikatorer på undermått som REDAN har en B-grön (ej krav för
   målet): realloner, vard_i_tid, skillnader_mellan_skolor, materiel_formaga, ukraina_stod, elprisvolatilitet,
   sfi_sprakkunskaper, fortroende_domstolar_myndigheter. Mest D-adaptrar (Spår D) + enstaka B-vägar. Nästa steg, ej brådskande.
3. **🔴 HOLD-undermått utan B-grön (4):** `genomforbarhet_leverans` (forsvar — steg-2-tilt; ny indikator
   `forsorjningstrygghet_materiel` föreslagen), `industriell_konkurrenskraft` (klimat — dubbelvägg;
   `industrins_utslappsintensitet` föreslagen), `boendesegregation` + `normer_tillit`
   (integration — genuina väggar/högsta bias-risk; se §8.7). *(`migrationssystem` LÖST 2026-06-07 via RiR 2020:7,
   se §8.7.) (De döda indikatorerna `personalomsattning_omsorg`, `leveranstid_materiel`, `segregation`,
   `tillit_valdeltagande` omklassade till **🔴 BEVAKA / utvidgningskandidat** 2026-06-07 — behålls med
   återöppningsvillkor i `categories.yaml`-noter, renormaliseras bort tills dess; Beslut 8.)*
4. **⚪ Target/kontext (utan B-grön, medvetet):** `inflation_prisstabilitet` (Riksbanksstyrt) +
   `offentliga_finanser` (codex HOLD-kontext 2026-06-07: åtstramnings-tilt + dubbelräkning mot A/c2 — directional
   konvertering avvisad). `forsvarsanslag_andel_bnp` förblir target men undermåttet ekonomisk_ambition nåddes via
   den nya syster-indikatorn forsvarsfinansiering_upptrappning_mot_mal.

**Slutsats:** B-grön-målet är nått så långt **neutralitet före 4** tillåter — 5 rena enhällighet-mått + 1
differentierande integration-mått (migrationssystem) byggda; de **6 återstående** (4 HOLD + 2 target/kontext)
är antingen genuina väggar (där bygge skulle kräva tilt/fabrikat → sign-off-kandidater §8.7) eller medvetna
target/kontext. De 8 gula är frivilliga bonus-indikatorer på redan täckta undermått.

## 5. Steg 2 — metodregister för positionering

Alla källor lyder under samma grindar (§10): instrument-exakthet, ordagrant citat + dok-id,
neutralitet. `source_type`-enumet i [fas4b §7](fas4b_partistandpunkter_metod.md) tillåter redan hela
stegen — vi har bara underutnyttjat allt utom votering.

### 5.1 Källstegen och vad varje källa är bra på
| Källa (stark→svag provenans) | source_type | confidence-tak | Bäst för |
|---|---|---|---|
| Skarp votering på sakpunkten | `votering` | high | binär riktning, ingen tolkning — men **noll vid acklamation** |
| Enhälligt betänkande | `betankande` | medium–high | baslinje-täckning (alla supports) när voteringen är acklamation |
| Reservation som anger nivå | `reservation` | medium | *mer/mindre* inom konsensus (differentiering) |
| Kommittémotion (partiofficiell) | `kommittemotion` | medium | instrument-specifik hållning, finns även vid acklamation |
| Budgetmotion | `budgetmotion` | medium | *riktning* (finansierar/avvecklar); **grad** kräver modellutv. (§5.6) |
| Valmanifest | `valmanifest` | low–medium | endast om instrument-konkret (annars mål → ej kodbart) |
| Partiprogram | — | — | endast kontext, aldrig ensam stance |

Confidence speglar var på stegen raden sitter; coverage-krympning + flagga bär osäkerheten ärligt.
`enskild_motion` = svag provenans, flaggas särskilt.

### 5.2 Enhällighet som källa — baslinje-täckning
**Vad:** När en sakpunkt tas med acklamation *därför att utskottet var enhälligt* (ingen reservation
*mot* punkten) är det belägg för att alla 8 partier står bakom. Koda samtliga `supports`,
`source_type: betankande`, `quote` = meningen som visar enhällighet/utskottets förslag.

**Varför tillåtet:** [fas4b §5](fas4b_partistandpunkter_metod.md) säger redan att stance får sättas när
partiet är formell avsändare, röstat för, eller står bakom via utskott. Ett enhälligt betänkande är de
facto kollektiv stance — och den **renaste neutraliteten**: alla kodas lika, inget straffas.

**Caveat:** (1) Acklamation ≠ alltid enhällighet — hämta fulltexten och bekräfta att *just den punkten*
saknar reservation mot sakinnehållet. (2) Det ger **täckning, inte rankning** (likformigt lyft). (3)
Lägger man ett konsensus-undermått bredvid ett differentierande i samma kategori späds differentieringen
(undermåttsviktat medel) — gör ett undermått i taget, inte en flod.

### 5.3 Budget- och kommittémotion — där differentieringen oftast bor
**Vad:** En budget- eller kommittémotion visar ett partis hållning på det *specifika instrumentet* även
när voteringen är acklamation. Budgeten är instrument-konkret (anslag/UO) och avslöjar **riktning** —
finansierar partiet instrumentet eller vill det avveckla/skära det?

**Varför viktigt:** det är här konsensus-reformer faktiskt skiljer partier åt. Acklamation i kammaren
döljer att budgetmotionerna pekar olika håll. Detta är primärvägen att hämta tillbaka differentiering
*utan tilt och utan votering*.

**Caveat:** (1) **Dubbelräkning mot A** — a1 mäter redan budget*prioritering* (andel till kategori). B
får bara mäta *om det finansierade instrumentet är evidensbelagt åt rätt håll*, inte prioriteringen
igen; håll frågorna åtskilda i `mapping_note`. (2) **Grad ryms inte** — se §5.6.

### 5.4 Reservations-mining — differentiering *inom* konsensus
**Vad:** Även när huvudpunkten är konsensus filar partier reservationer som vill ha **mer/mindre** av
samma instrument. Mer av positiv-riktad åtgärd → `supports`; avveckla/minska → `opposes` (negativ-grind
§10). Bara "annan utformning" utan riktningsinnebörd → ingen rad.
**Caveat:** högst tilt-risk (reservationer är ofta opposition-mot-regering) → codex/2nd-opinion per mått.

### 5.5 Positionsmönster över mandatperioden (bana, inte ögonblicksbild)
**Vad:** Etablera hållning ur **mönstret av flera källor/voteringar över mandatperioden**, inte en
enskild punkt. Konsekvent riktning är starkare belägg och kan avslöja en hållning en enskild
acklamation döljer (jfr nato: ögonblicket 2026 säger "alla för", banan skiljer V från MP).
**Caveat:** bara samma instrument (instrument-regeln). **Varaktiga, genuina omsvängningar kodas efter
nuläget** (nato/MP → `none`) — banan är en prediktor tyngd mot det senaste, inte en evig skuld; annars
bygger vi en "straffa-konvertiterna"-maskin som belönar stelhet. Föregående mandatperiod = kontext i
`mapping_note`, inte poäng.

### 5.6 Gränserna för steg 2 — när positionering *inte* går att mäta vettigt
- **Magnitud/grad** — binärmodellen (`supports`/`opposes`) kan inte säga "alla stödjer men olika
  mycket". Kräver modellutvidgning (viktad stance, eller instrument uppdelat på ambitionsnivå). Öppen
  designfråga (§8), byggs inte autonomt.
- **Målspråk utan instrument** — om enda belägget är ett mål ("bättre vård") → ingen rad (`unknown`).
- **Aktivitetsbias** — partier som motionerar mer får fler rader. Coverage normeras inte mot antal
  rader; redovisas som flagga (fas4b §9).

### 5.7 Nya indikatorer för steg-1-väggar (modellutvidgning, gräv djupare)
**Vad:** För undermått i §4.2 utan indikator: lägg en **ny indikator med svensk auktoritetsbelagd
riktning** i `categories.yaml`, sedan en åtgärdstyp i evidensliggaren. Öppnar ett annars ouppnåeligt
undermått. Ex: trygghet/`forebyggande` via lag (2023) om kommuners brottsförebyggande ansvar + Brå.
**"L"-arbete** (design + sign-off), inte autonomt.

### 5.8 Sökdjup, eskalering och zoom-ut — när ett delområde/kategori får kallas "uttömt"
> Standard fastlagd 2026-06-06 (skärpt efter diskussion). Första svepet prövade ~1 instrument per otäckt
> undermått i en enda runda och stannade vid "HOLD". Det räcker inte. **Att inte hitta ett instrument är
> INTE en slutpunkt — det är signalen att eskalera.**

**Eskaleringstrappa — deklarera inte "fast" förrän ALLA steg är uttömda:**

1. **Instrument till befintligt undermått (bredd + djup).** Pröva **5–7 genuint olika instrument** per otäckt
   undermått, i **flera rundor** tills två i rad ger noll nytt ("leta tills det är torrt"). Inte ett primärt
   plus närliggande varianter.
2. **Hittar du inget rent instrument → STANNA INTE. Eskalera till nytt undermått.** Kör INTE
   instrument-för-instrument i blindo. Ta ett steg tillbaka:
   - **a.** Läs om kategorin i [../IDEA.md](../../IDEA.md) — vad den *ska* fånga + dess caveat.
   - **b.** Bred analys uppifrån-och-ned: vad påverkar *generellt* kategorin positivt enligt officiell svensk
     kunskap (myndigheter, SOU, forskningsöversikter)?
   - **c.** Borra ner till ett **NYTT undermått** (med ny indikator, jfr §5.2/§5.7) som (i) genuint hör hemma i
     kategorin enligt IDEA.md, och (ii) har både evidens (steg 1) och neutral positionering (steg 2).
3. **"Fast"/"uttömt" får sättas FÖRST när både (1) och (2) är uttömda** — och ska då redovisa *vilka*
   instrument **och** *vilka* undermått-vinklar som prövades. "HOLD" ≠ "uttömt": HOLD = ingen ren kandidat i
   *denna* runda på *detta* spår, inte att kategorin är omöjlig.

**Två spärrar som alltid gäller på steg 2:**
- **Fuska inte:** lägg inte ett nytt undermått bara för att slippa ett svårt — det måste genuint höra hemma i
  kategorin (IDEA.md), inte vara en genväg till en lätt fyra.
- **Struktur kräver sign-off:** nytt undermått/indikator ändrar `categories.yaml` + viktbalansen → *föreslås*
  för människan (instrument i befintligt undermått byggs autonomt som v0). Default tills annat sägs.

---

## 6. Statustavla per kategori

Legend: ✅ byggt · 🟡 kandidat (research klar, väntar beslut) · ❌ förkastat (med skäl) · 🟣 steg-1-vägg (modellutvidgning).

> **Leveranser 2026-06-07 — ✅ SIGN-OFF GENOMFÖRD (§8.8/§9):** se **§8.7** (B-grön-svepet: 5 mått + integration-svepet:
> migration + alternativ-undermått-analys) och **§8.8 sign-off-checklista** (nu avgjord). Totalt **6 byggda B-mått, godkända
> v2** (5 enhällighet + 1 differentierande migration) + 1 kalibrering (sfi confidence→high). Dubbelräkning (C/MP transparens)
> åtgärdad, migration omverifierad, 4 döda indikatorer → BEVAKA, version 1→2, snapshot re-baselinad. **4 HOLD-väggar**
> (boendesegregation, normer_tillit, genomforbarhet_leverans, industriell_konkurrenskraft — med skärpta diagnoser + triggrar,
> lämnas/bevakas) + inflation/offentliga_finanser = target/kontext. Rubrikerna nedan uppdaterade till nya undermåttsräkningen.

### Trygghet — **5/5** ✅ FULLT (forebyggande byggt 2026-06-07; snabbförfarande 2026-06-06)
- ✅ `snabbforfarande_lagforing` → `handlaggningstid` (Brå 2020:3: handläggningstid i tingsrätt ca −40 %,
  total "mer än halverats"). Enhälligt bet. 2022/23:JuU2 p1 (acklamation; reservation V/C/MP gäller p2,
  de "välkomnar" snabbförfarandet) → **alla 8 supports** (§5.2). authority_evaluation/medium/medium.
  Codex: BUILD-WITH-CHANGES. Icke-rankningsdrivande, lyfter alla i trygghet (+0,04…+0,13).
- 🟡 `kronvittnen` (JuU35 2021/22, 7 Ja/V Nej). ❌-risk: utanför tidsfönster + bara prop-källa + fel
  indikator (grov brottslighet, ej generell uppklaring).
- 🟣 `forebyggande`: saknar indikator → §5.7.

### Klimat — **4/5** (invasiva arter byggt 2026-06-06, FLAGGAD; industriell_konkurrenskraft HOLD 2026-06-07 — se §8.7)
- ✅ `atgarder_mot_invasiva_frammande_arter` → `hotade_arter_naturforlust` (Naturvårdsverket: förteckningen
  är "ett verktyg i arbetet med att förebygga och begränsa spridningen av arter som kan orsaka skador på ...
  biologisk mångfald"). Enhälligt bet. 2025/26:MJU13 p1 (acklamation, "inte väckts någon motion som går
  emot"; tiltade p2 utesluten) → **alla 8 supports** (§5.2). **⚠️ Codex förordade HOLD** (rubrikcitatet
  bevisar hotet, ej instrumenteffekten); byggt som version 0 med **konservativ kalibrering low/low** +
  instrument-mekanismcitat. **FLAGGAD för din sign-off** (§8/§9).
- ❌ bottentrålning / naturvård / levande hav: utformningsstrid eller avslagspunkter (tilt).
- ❌ `industriell_konkurrenskraft` HOLD (saknar indikator → §5.7; dubbelvägg: RiR 2024:17 "oklart vilka effekter" + MJU15 p1 avslag V+MP).
  - **Kandidatnedstigning 2026-06-07 (dedikerad agent, 4 kandidater):** HOLD bekräftat, diagnos skärpt. (#1) `industrins_utslappsintensitet`
    (down, utsläpp/förädlingsvärde) — **D-serie FINNS** (SCB miljöräkenskaper, genuint skild från nivå-utsläppen, överlever relabel-testet)
    men **B faller**: instrumenten som sänker täljaren (koldioxidskatt/reduktionsplikt) ligger redan i `utslappsminskningar` → dubbelräkning;
    förädlingsvärde-/teknikskifteskanalen saknar kausal svensk källa. (#2) miljöprövningsreform **MJU4** = blocktilt (M/KD/SD/L vs S/V/MP/C).
    (#3) **elnät/elektrifiering — närmast genombrott: steg 2 LÖST** (bet. 2023/24:**NU15 p1**, snabbare elnätsprövning, **ACKLAMATION**, ingen
    reservation mot p1 → alla 8 supports via §5.2) MEN **steg 1 faller** — riktningen är genuint tvåsidig: Tillväxtanalys (kategorins egen
    B-källa) drar att elektrifiering → högre elpriser → "förlorad konkurrenskraft", medan Energimyndigheten ser den som nödvändig → ingen ren
    positiv riktning, ej heller §10-belagd negativ. (#4) negativ-rutt RiR 2024:17 = "oklart" ≠ belagd negativ → klarar ej §10-grinden.
    **Diagnos: BÅDA komponenterna fattas samtidigt på samma instrument** (till skillnad från demokrati/trygghet där §5.2 löste steg 2 + steg 1 fanns):
    den renaste reform-axeln (miljöprövning) är blocktiltad; det enda neutrala ankaret (elnät NU15) saknar rent steg-1-belägg.
    **Återöppna (#3, närmast):** svensk auktoritetskälla som ger ett RENT positivt konkurrenskraftsbelägg för snabbare elnätsutbyggnad (utan
    elpris-motverkan), eller KI/Tillväxtanalys-nettoutvärdering → då byggs §5.2-mått på NU15-ankaret. Bevaka NU10 (2025/26) + prop. 2025/26:238.

### Försvar — 4/5 (nato 2026-06-06 + ekonomisk_ambition/upptrappning 2026-06-07 byggt; genomforbarhet_leverans HOLD — se §8.7)
- ✅ `nato_medlemskap` → `nato_interoperabilitet` (votering UU16 2022/23 p1; Försvarsberedningen Ds 2024:6;
  supports S/M/SD/C/KD/L, **opposes V**, **MP=none** [reversering, codex-granskad]). *Flaggat: straffar V.*
- ❌ `genomforbarhet_leverans` HOLD (2026-06-06): inget instrument klarar steg 1 + steg 2 samtidigt. Ren
  positionering finns (FiU39 förenklad upphandling, acklamation) men saknar leveranstid-belägg; SOU 2022:24:s
  lagerhållning/inhemsk kapacitet belägger *försörjningstrygghet*, ej leveranstid, och FöU3 är genomgående
  tiltat (S/C/V/MP-reservationer). Väger 5/100 → tvinga inte. **Återöppna:** prop-fulltext om förenklad
  upphandling ordagrant kopplar till kortare leveranstid, eller RiR/FMV-granskning.
  - **Djupsvep §5.8 (2026-06-06, 7 instrument):** HOLD **bekräftat och härdat** — äkta steg-1-vägg av
    *indikator*-typ. Prövade: ASAP-fakta-pm (EU-källa, "korta leveransledtider" = Kommissionens mål, ingen
    riksdagsbehandling), LUFS-ändring SFS 2023:253 (rör krigsmaterielundantag, ej leveranstid), prop. 2024/25:34
    Totalförsvaret (fulltext grep: 0 träffar instrument→kortad ledtid; "nya materielsystem behöver levereras
    fortare" = uttalat behov, ej instrumenteffekt; gemensam upphandling kopplas till *kostnad/försörjningstrygghet*,
    uttryckligen ej leveranstid), RiR (enda leveranstid-granskningen RiR 2011:13 fann motsatsen — int. samarbeten
    ger *ej* leverans i tid; ingen 2020–2025-granskning), EDIRPA (EU-källa), ökade beställningsbemyndiganden
    (tidigarelägger *order*, ej ledtid; budget→A-dubbelräkning), beredskapslagstiftning (försörjningskapacitet).
    Officiella svenska källor behandlar genomgående lång leveranstid som *exogent marknadsproblem* och
    positionerar instrument mot kapacitet/kostnad — aldrig ordagrant mot kortad ledtid. **Flagga (sign-off):**
    enda B-vägen kan vara att byta/komplettera indikatorn (t.ex. FMV leveransindex som D-serie) → designbeslut.
  - **Kandidatnedstigning 2026-06-07 (dedikerad agent):** HOLD bekräftat — men **väggen krympt: STEG 2 numera LÖST.**
    Konstrukt-bytet `forsorjningstrygghet_materiel` (up, ersätter leveranstid) har nu ett **rent neutralt §5.2-ankare**:
    bet. 2025/26:**FöU3 p1** "En försvarsindustristrategi" togs i **ACKLAMATION, 0 reservationer mot p1** (alla 13 res. på
    p2–p10; beslut 2025-10-14) → alla 8 supports. Kvarvarande vägg = **ENBART steg-1/instrument-effekt**: ingen svensk
    kausalkälla belägger att strategin/inhemsk kapacitet HÖJER försörjningstrygghet *som distinkt leveransutfall* utan att
    (a) reduceras till målformulering (skr. 2024/25:193 = bara mål) eller (b) dubbelräkna `materiel_formaga`/`militar_formaga`
    (operativ förmåga/avskräckning). FOI-R--4366 (2016) = rekommendationer, ej ex-post, + avvisar "mer lagerhållning→bättre".
    Negativ-rutt: ingen RiR-granskning 2020–2026 om materielleverans (RiR 2011:13 = utanför fönster). **Återöppna (skärpt):
    EN** kommande effektutvärdering (regeringens utlovade årliga strategiredovisning, eller FOI/RiR) som belägger
    försörjningstrygghet-effekten → då BUILD v0 på FöU3-ankaret (low/low). D-spår: FMV:s leveransplaneutfall (% försenat)
    kan vara D-serie. Vikt 5/100 → tvinga inget.
- 🟣 `ekonomisk_ambition`: `target`-indikator → steg-1-vägg.

### Välfärd — 4/4 ✅ FULLT (vard_tillganglighet/NHV + omsorg_personal/kontinuitet byggt 2026-06-07 — se §8.7; tidigare HOLD överstigna med nya instrument)
- ❌ `vard_tillganglighet` HOLD (2026-06-06): **riktningsgrinden faller**. RiR 2023:12 finner vårdgaranti/
  kömiljard/SVF "på många sätt inte effektiva" + undanträngning (mixed/negativ); nationell vårdförmedling är
  *outvärderad* (E-hälsomyndighetens uppdrag 2023, system under uppbyggnad) → vore fabrikat; vårdval (RiR
  2014:22) mixed + neutralitetsbrytande. **Återöppna:** Vård- och omsorgsanalys vårdplats-slutrapport (apr
  2026) eller framtida effektutvärdering av vårdförmedlingen.
  - **Djupsvep §5.8 (2026-06-06, 6 instrument):** HOLD bekräftat. **Återöppningsvillkoret konsumerat negativt** —
    vårdplats-slutrapporten finns nu (Vård- och omsorgsanalys **2026:3 "Brist på plats", 29 apr 2026**) och föll
    *nedåt*: "Hittills ser satsningen inte ut att ha bidragit till att öka antalet vårdplatser på nationell nivå".
    Nära vård ("Omtag för omställning", 31 mars 2025): "inte haft några synliga effekter för befolkningen".
    Vårdförmedling fortsatt outvärderad. **NYTT fynd — cancerscreening är enda vard-instrumentet som passerar
    riktningsgrinden** (Socialstyrelsen: tjock-/ändtarmscancer-screening "sänker dödligheten … med 15 procent",
    mammografi −16/−20 %; konstrukt-exakt mot `overlevnad_svar_sjukdom`) men **faller på neutralitet** — varje
    riksdagskälla 2022–2026 är ett avslag med oppositionsreservationer (SoU16 p2, SoU17 p3); enda enhälliga
    (SoU36 2020/21) utanför fönstret + screening beslutas regionalt. **Bevaka:** enhälligt SoU-betänkande om
    nationella cancerstrategin 2.0 där alla 8 står bakom screening utan tilt → då ren BUILD via §5.2.
- ❌ `omsorg_personal` HOLD (2026-06-06): `fast_omsorgskontakt` har **perfekt steg 2** (lag bet.
  2021/22:SoU24 p2, acklamation, alla 8) men **fel konstrukt i steg 1** — instrumentet rör relationskontinuitet
  *för omsorgstagaren*, inte personalomsättning. Socialstyrelsen fick mars 2026 i uppdrag att utveckla ett
  personalkontinuitetsmått (del 2026-12-16, slut 2027-10-01). **Återöppna:** när det måttet + utvärdering finns.
  - **Djupsvep §5.8 (2026-06-06, 5 instrument):** HOLD bekräftat. Inget instrument har en *färdig officiell
    utvärdering som belägger sänkt personalomsättning*: Äldreomsorgslyftet (mäter kompetens/utbildning, ej
    omsättning), skyddad yrkestitel undersköterska (outvärderad), Heltidsresan (SKR/Kommunal = ej myndighet;
    mäter heltidsandel, ej omsättning), bemanning/arbetsvillkor (endast facklig källa). Socialstyrelsens nya mått
    visar sig vara **samma felkonstrukt** (personalkontinuitet ≠ omsättning) + finns ej förrän dec 2026/okt 2027;
    SKR la dessutom ned kontinuitetsstatistiken 2024 → även dataunderlaget borta. Strukturell vägg (en enda
    indikator, inget partistyrbart instrument flyttar den bevisat nedåt).

### Integration — 3/5 (migrationssystem BYGGT 2026-06-07 via RiR 2020:7; boendesegr./normer_tillit HOLD — högsta bias-risk; kamera-vägen för boendesegr. förkastad av codex; sign-off-kandidater §8.7)
- ✅ `migrationssystem` BYGGT 2026-06-07 (integration-svepet, FLAGGAT v0). NY indikator `atervandande_effektivitet`
  (up, systemfunktion EJ volym), instrument `se_over_ansvarsfordelning_atervandande` (RiR 2020:7: splittrad
  återvändandestruktur kostar/ineffektiv, RiR rekommenderar att se över ansvarsfördelningen). **Genuin tvåsidig
  split** (bet. 2020/21:SfU6 p2, votering verifierad): supports M/KD/SD/C/L, opposes S/MP, V none (avstod).
  NEUTRALT: vanns mot sittande S/MP-regering, C+L röstade med oppositionen, V ej med S/MP. Detta är den
  **negativ-evidens-vinkel** användaren efterlyste (RiR:s negativa fynd om splittringen krediterar reformsidan).
  Codex KEEP-WITH-CHANGES (snävade policy_type från "samla" → "se över ansvarsfördelning"; tidsnot 2020/21).
- ❌ `normer_tillit` HOLD (2026-06-06): samhällsorientering belägger "kunskap om samhället/etablering", **inte
  tillit/valdeltagande** (instrument-grind faller); AU8 p3 ej enhällig (S-reservation) + är ett *avslag*.
  - **Djupsvep §5.8 (2026-06-06, 6 instrument):** HOLD bekräftat. **Renaste near-miss:** tillgänglighet vid val
    (prop. 2024/25:181, bet. **2025/26:KU4 p1**) har **perfekt steg 2** (acklamation, ingen reservation mot p1,
    SD-reservationer gäller p2/p3 → alla 8 supports) men **fel konstrukt i steg 1** — källan belägger "likvärdig
    möjlighet att utöva rösträtten", inte *uppmätt höjt valdeltagande* (samma samhällsorientering-fälla).
    Övriga: demokratisatsningar (RFR15: "impossible to determine" kausalitet), förtidsröstnings-tillgänglighet
    (akademisk, effekt svag/oklar), föreningsstöd (SOM: korrelation, orsak går institutionstillit→tillit; +
    A-dubbelräkning), hedersförtryck (fel konstrukt). **Återöppna:** svensk källa som kopplar KU4-tillgänglighets-
    åtgärden till *uppmätt högre valdeltagande* → då vänds instrument-grinden och måttet byggs via §5.2.
  - **Kandidatnedstigning 2026-06-07 (integration-svepet):** HOLD kvarstår. **Steg 1 äntligen löst** för GOTV:
    Delmi 2025:5 (systematisk genomgång, randomiserade fältexperiment) kopplar *kausalt* lokal röstmobilisering →
    uppmätt valdeltagande. MEN **steg 2 saknar neutralt ankare**: varje riksdagsbehandling av "öka valdeltagandet"
    2022–2026 (KU23/KU13/KU27) är ett *avslag* med enpartisreservation (MP, sedan S) = tilt; enda positiva anslaget
    (UO1 GOTV inför EU-val 2024) togs i acklamation bara för att S/V/MP/C **avstod** → kan ej kodas supports.
    Nedstigning #2 (politisk representation) + #3 (psykologiskt försvar/MPF) + egna vinklar (föräldrastöd, bibliotek,
    medborgarceremoni, folkbildning) + negativ-evidens-rutten — **alla wall på steg-1 instrument-grind** (fel
    konstrukt / icke-svensk kausalitet / korrelation / A-dubbelräkning). Status: **steg 1 löst, steg 2 saknas.**
    **Återöppna (GOTV):** ett enhälligt/acklamerat anslagsbeslut för icke-partisk röstmobilisering där oppositionen
    EJ avstår — då byggs måttet via §5.2.
  - **Extra runda 2026-06-07 (5 nya spår):** HOLD bekräftat, men en genuint ny near-miss. **IFAU 2017:12** (treåriga
    yrkesprogram → valdeltagande +3 p.e. för resurssvaga unga) är en **NY steg-1-vinst med ett PARTISTYRBART instrument**
    (det GOTV saknade) — men steg 2 faller: bet. 2021/22:UbU22 p1-spliten är **SD+L-avslag på utbildningskvalitets-grund
    (kunskapsurholkning), ej valdeltagande** → koda dem `opposes` vore konstrukt-missmatch + tilt på fel värdeaxel. Övriga:
    IFAU 2018:3 (tidig rösträtt utländska medborgare = kausal NOLLeffekt), Brå hedersförtryck 2026 (beskrivande, ej
    utfallseffekt), RiR 2026 etnisk diskriminering (processgranskning), RiR 2023 tillit/kontroll civilsamhälle
    (administrativ kontroll, ej tillitseffekt) — alla wall. **Skärpt återöppning:** acklamerad UbU-behandling av treåriga
    yrkesprogram UTAN avslagsreservation → §5.2 löser steg 2 mot IFAU 2017:12.
- ❌ `boendesegregation` HOLD (2026-06-06): ingen kausal svensk *instrument*-utvärdering (Boverket beskrivande);
  CU18 p12 är ett **avslag** med S/V/C-reservationer, underliggande CU6 är regering-vs-vänster-split → tilt.
  *(RÄTTAT 2026-06-07: steg-1-evidens finns numera — RiR 2021:29, se nedstigningen längre ned; väggen är STEG 2/neutralitet.)*
  - **Djupsvep §5.8 (2026-06-06, 5 instrument):** HOLD bekräftat — **äkta steg-1-vägg (§4.2)**. Ingen svensk
    auktoritetskälla visar att ett *instrument* mäter trångboddhet/segregation NEDÅT: blandade upplåtelseformer
    (mixed), områdesinsatser (förbättrar individer men området oförändrat — folk flyttar + stigma), Boverket
    2023:26 (beskrivande verktygslåda), bostadsförsörjning CU37 p1 (acklamation men rör hyresavtals-säkerhet, ej
    trångboddhet), Delmi 2025:3 (kunskapsöversikt, icke-kvantifierade samband). En reform mot trångboddhet hade
    "rather the opposite effect" (Boverket). **Återöppna:** framtida IFAU/Boverket *instrument*-effektutvärdering.
- 🟡→❌ `boendesegregation` KAMERA-VÄGEN FÖRKASTAD 2026-06-07 (codex KILL): byggd och sedan reverterad. Förslaget
  var `trygghet_utsatta_omraden` via utökad kamerabevakning (JuU27, Brå-metastudie) + symmetrisk IMY-negativ-post
  i demokrati. Codex-skäl (korrekta): (1) det är **trygghet-evidens ometiketterad** som integration — Brå-effekten
  avser ej utsatta områden; (2) **dubbelräknar** befintliga `situationell_prevention_kamerabevakning`→trygghet;
  (3) exakt den varning §8.7 redan givit ("kamera... dubbelräknar trygghet + krockar med demokrati-övervakning");
  (4) 7 supports/1 opposes → ~noll differentiering. boendesegregation kvarstår HOLD.
  - **Kandidatnedstigning 2026-06-07 (efter codex-killen, dedikerad agent):** HOLD bekräftat — men **diagnosen skärpt
    och en logg-faktarättelse:** väggen är **STEG 2 (neutralitet), inte steg 1 (evidens)**. (i) **#2 bosättningslagen
    (2016:38)/kommunanvisning PASSERAR instrument-grinden** — **RiR 2021:29** "Bosättningslagen – har reformen levt upp
    till intentionerna?" ÄR en kausal segments-instrumentutvärdering (statlig kommunanvisning → jämnare kommunspridning;
    det tidigare ojämna mottagandet "ökade segregationen") → motsäger den tidigare logg-raden "ingen kausal svensk
    instrument-utvärdering". MEN faller på neutralitetsgrinden: SD vill AVSKAFFA lagen på *kommunalt-självstyre*-grund,
    M vill behålla → genuin självstyre/centralism-VÄRDEKONFLIKT (Dir 2024:22 ramar in den så) = tilt. (ii) **#3
    vräkningsförebyggande:** ingen kausal effektutvärdering (Socialstyrelsen/Länsstyrelsen beskrivande) + ankare S/V-
    ensidiga (SoU16 p10 avslag, vänstertilt) → faller båda grindar. (iii) **#4 EBO/områdesbegränsning:** negativ-evidens
    DELVIS belagd (Ds 2018:18/SfU11: EBO-koncentration → "segregation, trångboddhet…") men bara utrednings-MOTIVERING
    (ej ex-post-effektmätning) + migrations-värdeaxel-tilt (V avslår hela, M/SD/KD vill strängare) → bygg ej. (iv) **#5
    områdesinsatser/Delmi 2025:3/Statskontoret 2023:** beskrivande/mixed (oförändrat). **Återöppna #2:** om den nya
    bosättningslagen (ur Dir 2024:22, ikraft ~2027) tas i enhälligt SfU/AU-betänkande utan självstyre-reservation mot
    huvudpunkten → RiR 2021:29 blir steg 1 och §5.2 löser steg 2. (Bevaka SfU 2026/27.)
  - **Extra runda 2026-06-07 (5 nya spår):** HOLD bekräftat, inga nya öppningar. Avförda spår: DO-bostadsdiskriminering
    (instrument = förslag, ej infört; värdeaxel), hemlöshet/Bostad först (regeringsbeslut → inget riksdagsankare;
    CU13-motioner avslagna; mäter kvarboende ej segregation), bostadsbidrag **RiR 2024:15** (belägger trångboddhet
    ÖKAT men ingen kausal instrumenteffekt + transfererings-värdeaxel), bostadspolitik **bet. 2024/25:CU13** (acklamation
    = avslag på ~160 oppositionsmotioner, §5.2 ej tillämpbar), färska kunskapskällor (Delmi 2025:3/Boverket
    2023:23/2023:26 beskrivande). Dir 2024:22-triggern fortfarande ouppfylld (utredningsstadiet, självstyre-inramad).
- ✅ `migrationssystem` byggt (se kategorihuvudet ovan) — den enda av integrations tre HOLD-väggar som föll
  2026-06-07. normer_tillit + boendesegregation kvarstår HOLD.
- ⚠️ Kategorins egen IDEA.md-caveat ("stor risk för ideologisk bias") **bekräftad i praktiken** → HOLD rätt.

### Demokrati — **5/5** ✅ FULLT (transparens_ansvar/insyn partifinansiering byggt 2026-06-07; public service 2026-06-06)
- ✅ `lagstadgat_oberoende_public_service` → `mediefrihet` (undermått yttrandefrihet_medier, tidigare B-tomt
  3/5 → **4/5**). Instrument: för första gången regleras public service-uppdraget I LAG (prop. 2024/25:166,
  ur 2023 års **parlamentariska** public service-kommitté SOU 2024:34 "Ansvar och oberoende") med lagstadgat
  oberoende → mediefrihet UPP. Instrument-mekanism (prop. 5.2.1): public service "ska bedrivas självständigt i
  förhållande till såväl staten som olika ekonomiska, politiska och andra intressen … oberoende och stark
  integritet". Enhälligt bet. 2025/26:KrU2 punkt 1 (acklamation, votering-API tomt; "inte väckts någon motion
  som går emot att riksdagen antar regeringens lagförslag"; alla 15 reservationer gäller punkt 2–14, ej p1) →
  **alla 8 supports**. **Codex: BUILD-WITH-CHANGES** (mekanism-/designflagga; snäv formulering lagstadgat
  oberoende → mediefrihet, ej "public service-lag → demokrati"; behåll authority_evaluation/low/low). Icke-
  rankningsdrivande. **Framtida uppgradering:** SOU/utvärdering som belägger varför lagFORMEN (ej bara oberoende
  i sak) stärker institutionellt oberoende.
- 🟡 `transparens_ansvar`: **återöppningen PRÖVAD OCH FÄLLD 2026-08-16 — buntad omnibus, HOLD med trigger.**
  Steg 1 höll (riktning belagd, dir. 2023:88: insyn "förebygger korruption och ökar … legitimitet"; ingen
  dubbelräkning mot offentlighetsprincipen). **Steg 2 faller på neutralitetsgrind punkt 4.** Verifierat live mot
  data.riksdagen.se: bet. 2025/26:KU39 hade **en enda punkt** (p1, huvudvotering i sakfrågan, votering_id
  `DCA347C0-D1CA-40A9-9748-2797405C09CB`, beslut 2026-06-16, 174 Ja / 172 Nej / 3 frånv.; Ja = M/SD/KD/L,
  Nej = S/C/V/MP), och den punkten **buntar tre lagar**: (1) lobbyregister, (2) arbetsmarknadsorganisationers
  bidrag för partipolitiska ändamål, (3) ändring i lagen 2018:90. Lag 2 är exakt den del bygginstruktionen
  förbjuder att koda (S-tilt) — och den går inte att lyfta ut, eftersom det bara fanns en omröstning.
  **Avgörande:** båda följdmotionerna yrkade avslag ENBART på lag 2 — 2025/26:4151 (S, Jennie Nilsson m.fl.)
  och 2025/26:4184 (C, Malin Björk m.fl.), ordagrant "Riksdagen avslår regeringens förslag till lag med
  bestämmelser om arbetsmarknadsorganisationers bidrag för partipolitiska ändamål". Varken lobbyregistret
  eller 2018:90-skärpningarna möttes av invändning. Att koda Nej-sidan som `opposes` på politisk transparens
  vore alltså ett fabrikat som handlingarna motsäger; att koda enbart Ja-sidan vore ensidigt B-tillskott till
  ett block i den mest bias-känsliga kategorin. **Kostnaden för HOLD är låg:** transparens_ansvar är redan
  täckt via `insyn_partifinansiering` och demokrati ligger 5/5 i B-bredd — KU39 var en uppgradering av ett
  svagt mått, inte en lagning av en lucka. **Återöppnas** via §4.1-vägen (steg-2-källbyte): en instrument-exakt
  källa för *enbart* lobbyregistret per parti, t.ex. en framtida separat votering eller kommittémotioner som
  bara avser registret. Obs dubbelräkningsrisk: C:s lobbyregistermotion (HD023583 yrk. 17) är redan ankare i
  `starkt_oberoende_granskning_och_insyn` — principen "en post bär en fråga" gäller.
  Visselblåsarlagen/öppna data-lagen förkastade sedan tidigare (tid resp. fel konstrukt).
- ❌ `yttrandefrihet_medier` övriga instrument HOLD: straffskärpning brott mot journalister (V-reservation = krim-
  pol. tilt, ej anti-pressfrihet), nytt mediestöd (förordning → ingen votering; dubbelräkning mot A), massmedie-
  betänkanden KU18 (regering-vs-opp-tilt).

### Ekonomi — 4/6 ✅ (offentliga_finanser HOLD-som-kontext 2026-06-07, codex avvisade directional konvertering — se §8.7; inflation = target)
- Färdigställt 2026-06-05; se [BACKLOG.md](../BACKLOG.md). Alla 4 B-möjliga undermått täckta; inflation/off.finanser
  = target (vilande).

---

## 7. Kandidat-pipeline — utfall 2026-06-06

Sju kandidater researchades med tvåstegsmetoden (steg 1 svensk auktoritetskälla, steg 2 positionering;
varje röstsiffra curl-verifierad mot data.riksdagen.se; codex-2nd-opinion på byggena). **Resultat: 2 byggda,
5 HOLD** — dubblade nattens leverans (1 → 2 nya) och tog trygghet + klimat till 4 undermått.

| # | Kategori → undermått | Åtgärdstyp | Metod | Utfall |
|---|---|---|---|---|
| 1 | trygghet → rättsv.effektivitet | `snabbforfarande_lagforing` | §5.2 enhällighet | ✅ **BYGGT** (Brå 2020:3; JuU2 p1) |
| 2 | klimat → biologisk_mangfald | `atgarder_mot_invasiva_frammande_arter` | §5.2 enhällighet | ✅ **BYGGT** (low/low, FLAGGAD; MJU13 p1) |
| 3 | välfärd → vard_tillganglighet | `nationell_vardformedling` m.fl. | §5.2/§5.3 | ❌ HOLD — riktningsgrind faller (RiR 2023:12 mixed; vårdförmedling outvärderad) |
| 4 | välfärd → omsorg_personal | `fast_omsorgskontakt` | §5.2 | ❌ HOLD — steg 2 perfekt, steg 1 fel konstrukt (kontinuitet ≠ omsättning) |
| 5 | integration → normer_tillit | `samhallsorientering` | §5.2 | ❌ HOLD — belägger kunskap, ej tillit; AU8 ej enhällig |
| 6 | integration → boendesegregation | (CU18 p12) | §5.2/§5.3 | ❌ HOLD — ingen kausal källa; avslag + tilt |
| 7 | försvar → genomforbarhet_leverans | (upphandling/lagerhållning) | §5.2/§5.3 | ❌ HOLD — steg 1 + steg 2 ej uppfyllbara samtidigt |

Återöppningsvillkor per HOLD står i §6. Centralt fynd: **enhällighet-som-källa fungerar** (#1, #2 var
"väggade" under den gamla votering-först-metoden), men den dissolverar bara *steg-2*-väggen — där *steg 1*
(riktningsevidensen) saknas eller är mixed (#3–#7) hjälper ingen positioneringsmetod. Det är gränsen mellan
"källval" och "äkta vägg" (§4), nu empiriskt bekräftad. Förkastningsskäl + dok-id även i [BACKLOG.md](../BACKLOG.md).

> **OBS — detta var ett FÖRSTA svep (en runda, ~1 instrument per delområde), inte en uttömmande genomgång.**
> De 5 HOLD och de 4 kategorier under 4 undermått (välfärd 2, integration 2, försvar 3, demokrati 3) ska
> genomgås på nytt enligt **§5.8** (5–7 instrument per delområde, flera rundor, zoom-ut via IDEA.md) innan
> någon kategori avförs som uttömd. "HOLD" här = ingen ren kandidat i runda 1, inte "omöjligt".
>
> **✅ ANDRA SVEPET UTFÖRT 2026-06-06 (§5.8 djupsvep, 4 parallella researchagenter, 7+11+11 instrument):**
> **demokrati löst → 4/5** (public service-lagen, KrU2 p1 enhällighet; se §6). **forsvar/valfard/integration:
> HOLD ×5 bekräftat** efter genuint 5–7+ instrument per delområde — äkta steg-1-väggar (leveranstid,
> boendesegregation), fel konstrukt (omsorg_personal, normer_tillit) eller steg-2-tilt (cancerscreening).
> Skärpta återöppningsvillkor + near-miss-fynd (cancerscreening, KU4-tillgänglighet, KU39-insyn) i §6. Dessa
> tre kategoriers väg till 4 undermått kräver nu **modellutvidgning** (ny indikator/undermått eller nytt
> steg-2-läge) → **sign-off-frågor**, ej autonomt byggbart (§5.8 spärr 2 + §8).

---

## 8. Öppna designfrågor (för dig)

| # | Fråga | Läge / rekommendation |
|---|---|---|
| 1 | **Räkna värdeneutrala konsensus-mått mot 4-undermått-målet?** (steg-1-bra mått, positionerat via enhällighet/§5.2 → alla supports) | Rekommendation: **ja, med disciplin** — ett undermått i taget, enhällighet verifierad, flaggat som icke-rankningsdrivande. Det är BACKLOG-målet "höj B:s trovärdighet". |
| 2 | **Modellutvidgning för grad/magnitud?** (§5.6 — fånga "alla stödjer men olika mycket" ur budgetar) | ❌ **AVGJORT 2026-06-07: ÖVERGIVEN** (Beslut 12). Spec skriven ([done/viktad_stance_spec.md](viktad_stance_spec.md)), Codex v1→HOLD, v2→DATAPILOT-FIRST; **datapilot: ~3/43 instrument (≈7 %)** har kvantifierad ambitionsnivå, klustrade i forsvar+klimat, mest budgetnära → kill-kriterier föll in. Strukturell orsak: instrumentbaserad modell ⇒ instrument är diskreta reformer; grad bor i budgetnivåer (= delpoäng A). **Binär stance är rätt passform — bygg ej.** |
| 3 | **Hur långt bak väger banan?** (§5.5) | ✅ **BESLUTAT 2026-06-07** (Beslut 13): mandatperioden, recency-viktat; varaktiga omsvängningar kodas efter nuläget (nato-regeln). **Framtida:** väga in flera mandatperioder — kräver eget designbeslut (hur tyngs historik utan "straffa-konvertiter"-effekt). |
| 4 | **Acceptera nato-byggets V-straff?** (V −0,375 i försvar) | ✅ **BESLUTAT 2026-06-06: OK** (objektivt belagt, V genuint Nato-kritiskt). |
| 5 | **Behåll invasiva-arter-måttet (klimat)?** | ✅ **BESLUTAT 2026-06-06: BEHÅLL** ("kan fylla på i framtiden"). Byggt v0 med instrument-mekanismcitat + konservativ low/low + alla 8 supports. |
| 6 | **Ta bort / åtgärda de röda undermåtten?** Efter B-grön-svepet 2026-06-07 är bilden ändrad: `forebyggande` har nu en indikator (byggd); `omsorg_personal` nås via nya `kontinuitet_i_omsorgen` (döda `personalomsattning_omsorg` behålls separat). Kvar: (a) döda indikatorer `leveranstid_materiel`/`segregation`/`tillit_valdeltagande` (deras undermått är HOLD eller D-täckta); (b) 2 undermått som *saknar indikator* (`industriell_konkurrenskraft`, `migrationssystem`). | ✅ **BESLUTAT 2026-06-07** (Beslut 8): de 4 döda indikatorerna (`personalomsattning_omsorg`, `leveranstid_materiel`, `segregation`, `tillit_valdeltagande`) omklassade till **🔴 BEVAKA / utvidgningskandidat** med återöppningsvillkor i `categories.yaml`-noter — ej strukna, kan återupplivas vid ny indikator/evidens. De 2 indikatorlösa undermåtten: `migrationssystem` LÖST (RiR 2020:7), `industriell_konkurrenskraft` kvar som HOLD-vägg (§8.7). Poängneutralt (renormaliseras bort). |

### 8.7 B-grön-svepet 2026-06-07 — vad som byggdes + sign-off-kandidater ⭐

> Användarmandat (2026-06-07): **varje undermått ska ha minst en B-grön indikator** (D-grön räcker inte; om ett
> undermått bara har D-grön måste en B-grön hittas). Scope vidgat: nya indikatorer får byggas autonomt som
> **version 0**. Regel 1 (neutralitet före 4) gäller fortfarande — tiltade mått byggs aldrig.

**BYGGT (5 mått, version 0, FLAGGADE för din sign-off — alla enhällighet-som-källa §5.2, alla 8 supports,
icke-rankningsdrivande, low/low):** 11 parallella researchagenter + codex adversariell granskning (codex:
4× BUILD-WITH-CHANGES, 1× BUILD; ändringar införda). Acklamation per punkt verifierad mot data.riksdagen.se
dokumentstatus; citat verbatim-kollade.

| Undermått (kategori) | Indikator | Åtgärdstyp / källa | Codex |
|---|---|---|---|
| transparens_ansvar (demokrati) | politisk_transparens | `insyn_partifinansiering` — lagen 2018:90, bet. 2017/18:KU19 p1 | BUILD-WC (dubbelräknings-flagga, se nedan) |
| ekonomisk_ambition (forsvar) | **NY** forsvarsfinansiering_upptrappning_mot_mal | `upptrappning_forsvarsanslag_mot_mal` — Ds 2024:6 + prop. 2024/25:34, FöU2 p1+p5 | BUILD-WC (snäv "åtagande mot beslutad nivå") |
| forebyggande (trygghet) | **NY** kommunalt_brottsforebyggande_arbete | `lagstadgat_kommunalt_brottsforebyggande_ansvar` — lagen 2023:196, JuU9 p1 | BUILD |
| vard_tillganglighet (valfard) | overlevnad_svar_sjukdom | `koncentration_nationell_hogspecialiserad_vard` — SOU 2015:98 + prop. 2017/18:40, SoU18 p1 | BUILD-WC (snäv "koncentration→överlevnad") |
| omsorg_personal (valfard) | **NY** kontinuitet_i_omsorgen | `fast_omsorgskontakt` — prop. 2021/22:116 + Socialstyrelsen, SoU24 p2 | BUILD-WC (ny indikator ≠ personalomsättning) |

**Sign-off-frågor på de byggda:**
- **Dubbelräkning (transparens) — ✅ ÅTGÄRDAD (sign-off 2026-06-07, Beslut 3):** C och MP var i bunten
  `starkt_oberoende_granskning_och_insyn` (→ korruption) ankrade på partifinansierings-citat → dubbelkrediterade under två
  demokrati-undermått. **Lösning:** raderna omankrade till andra yrkanden i *samma* motioner — C → **lobbyregister**
  (HD023583 yrk. 17), MP → **offentlighetsprincipen** (HA02181 yrk. 9), båda verifierade ordagrant mot `.text`.
  Partifinansiering krediteras nu ENDAST i `insyn_partifinansiering`. Poängneutralt (stance kvar supports). Övriga 6 partier överlappade ej.
- **Strukturändring:** 3 nya indikatorer i `categories.yaml` (forsvar/trygghet/valfard) — normalt §5.8-spärr-2-sign-off;
  byggt som v0 per mandatet. Inga undermåttsvikter ändrade (nya indikatorer i befintliga undermått).
- **Behåll/kasta:** alla 5 är low/low mekanism-/designevidens (ingen ex-post-effektutvärdering) — samma kalibrering
  som invasiva arter/public service. Din sign-off avgör.

**HOLD (5 undermått — bygge skulle kräva tilt/fabrikat; konkreta kandidat-indikatorer för din sign-off):**

| Undermått (kategori) | Varför HOLD | Föreslagen indikator (sign-off) | Återöppningsvillkor |
|---|---|---|---|
| genomforbarhet_leverans (forsvar) | **[UPPDATERAT 2026-06-07 (nedstigning): STEG 2 LÖST — bet. 2025/26:FöU3 p1 "försvarsindustristrategi" ACKLAMATION, 0 res. mot p1, alla 8 supports. Kvarvarande vägg = ENBART steg-1/instrument-effekt + dubbelräkningsrisk mot materiel_formaga]** ~~leveranstid = äkta steg-1-vägg~~ | `forsorjningstrygghet_materiel` (up) — ankare FöU3 p1; SOU 2022:24/FOI 4366 = ej ex-post-effekt | **EN** effektutvärdering (regeringens årliga strategiredovisning, FOI/RiR) som belägger försörjningstrygghet-effekten → BUILD v0 |
| industriell_konkurrenskraft (klimat) | **[UPPDATERAT 2026-06-07 (nedstigning, 4 kand.): BÅDA komponenterna fattas samtidigt. Renaste reform-axeln (miljöprövning MJU4) blocktiltad; enda neutrala ankaret (elnät NU15 p1, ACKLAMATION) saknar rent steg-1-belägg (Tillväxtanalys: elektrifiering→"förlorad konkurrenskraft" = tvåsidig); RiR 2024:17 "oklart"≠belagd negativ; #1 utsläppsintensitet=dubbelräkning]** | `industrins_utslappsintensitet` (down, SCB miljöräkenskaper) — **D-serie finns** (≠ B); elnäts-ankare NU15 p1 | RENT positivt konkurrenskraftsbelägg för elnätsutbyggnad (utan elpris-motverkan), eller KI/Tillväxtanalys-nettoutvärdering → §5.2 på NU15. Bevaka NU10 (2025/26) + prop. 2025/26:238 |
| boendesegregation (integration) | **[UPPDATERAT 2026-06-07, se Integration-svepet nedan: kamera-väg byggd→reverterad (codex KILL); diagnos rättad — steg-1-evidens FINNS (RiR 2021:29 kommunanvisning→spridning), väggen är STEG 2/neutralitet (bosättningslag/EBO = självstyre-/migrations-värdekonflikt)]** ~~äkta steg-1-vägg (Boverket beskrivande)~~ | — | enhälligt SfU/AU-betänkande om nya bosättningslagen (Dir 2024:22, ~2027) utan självstyre-reservation → RiR 2021:29 blir steg 1 |
| normer_tillit (integration) | **[UPPDATERAT 2026-06-07, se nedan: steg 1 LÖST (Delmi 2025:5 GOTV-kausalitet); väggen är STEG 2 — inget neutralt ankare]** ~~inget neutralt partistyrbart instrument med svensk kausalkälla~~ | (öppen) `valdeltagande_utsatta_omraden` om enhälligt GOTV-ankare hittas | enhälligt/acklamerat GOTV-anslag där oppositionen EJ avstår |
| migrationssystem (integration) | **[LÖST 2026-06-07, se Integration-svepet nedan: byggt via negativ-evidens-vinkeln — RiR 2020:7/`se_over_ansvarsfordelning_atervandande`, tvåsidig split SfU6 p2]** ~~steg-1 faller hårt~~ | ✅ `atervandande_effektivitet` (up) BYGGT v0 | (byggt) |

**KONTEXT (ej B-grön, medvetet):** `offentliga_finanser` — codex HOLD-kontext (åtstramnings-tilt: "framework
compliance" privilegierar finanspolitisk återhållsamhet; dubbelräkning mot A/c2; smugglar target-konstrukt in i
directional B). Lämnas som ⚪ target/kontext likt `inflation`. *(Kandidat fanns: `langsiktig_finanspolitisk_hallbarhet`
via efterlevnad finanspolitiska ramverket, FiU14 acklamation — avvisad av codex på neutralitet. Din override möjlig.)*

#### Integration-svepet 2026-06-07 (forts.) — de tre integrations-väggarna återangripna ⭐

Användaren bad att specifikt fylla integrations otäckta undermått, med metodpoängen att **negativ evidens är
lika giltig som positiv** (en auktoritetsbelagd skadlig instrumenteffekt → den som vill avveckla instrumentet
får bra B). 3 forskningsagenter (5 förslag/undermått) + per-parti-verifiering + codex adversariell granskning.

| Undermått | Utfall | Vad |
|---|---|---|
| `migrationssystem` | ✅ **BYGGT v0 (FLAGGAT)** | NY ind. `atervandande_effektivitet` (up, systemfunktion) / instrument `se_over_ansvarsfordelning_atervandande` / RiR 2020:7 (negativ-evidens-vinkeln: splittrad struktur kostar). Genuin tvåsidig split bet. 2020/21:SfU6 p2 (votering verifierad): supports M/KD/SD/C/L, opposes S/MP, V none. Codex **KEEP-WITH-CHANGES** (snävade policy_type "samla"→"se över ansvarsfördelning"; tidsnot 2020/21 = partiernas nuläge ej bevisat → sign-off). Effekt: integration 2/5→**3/5**, ranking oförändrad, endast integration rörd (S −0.063, MP −0.044, M/SD/L +0.04…0.09). |
| `boendesegregation` | ❌ **HOLD** (kamera reverterad; nedstigning #2–#5 gjord) | Kamera-vägen byggd→reverterad (codex KILL: trygghet-relabel + dubbelräknar `situationell_prevention_kamerabevakning` + §8.7-varningen + 7-1≈noll diff). **Dedikerad nedstigning 2026-06-07:** #2 bosättningslagen/kommunanvisning **passerar instrument-grinden** (RiR 2021:29 = kausal: kommunanvisning→jämnare spridning, gamla systemet "ökade segregationen") men **faller på neutralitet** (SD vill avskaffa på självstyre-grund, M behålla = värdekonflikt); #3 vräkning (ingen kausal eval + S/V-tilt); #4 EBO (negativ-evidens bara utredningsmotivering + migrations-värdeaxel-tilt); #5 områdesinsatser (beskrivande/mixed). **Diagnos rättad: väggen är STEG 2/neutralitet, EJ steg 1** (RiR 2021:29 finns). |
| `normer_tillit` | ❌ **HOLD** (steg 1 löst, steg 2 saknas) | GOTV: Delmi 2025:5 löser steg 1 (kausal) men inget neutralt steg-2-ankare (avslag+enpartisreservation, eller acklamation där oppositionen avstår). Nedstigning #2/#3 + egna vinklar + negativ-rutt: alla wall på instrument-grind. Se §6. |

**Sign-off på det byggda (migration) — ✅ AVGJORD (2026-06-07, Beslut 2):** (1) `atervandande_effektivitet` **BEHÅLLS**
(v0→v2, RiR 2020:7, MEDIUM/MEDIUM — starkare kalibrering än enhällighetsmåttens low/low eftersom RiR är auktoritetsutvärdering).
(2) **Tidsgrind — OMVERIFIERAD (Beslut 2a, val A):** bred sökning i innevarande mandatperiod (SfU-motioner, plattformar, prop.
2025/26:263 + S/MP/C:s följdmotioner hd024152/hd024173/hd024159) gav INGEN nyare instrument-exakt källa om ansvarsfördelningen
för återvändande → kodningen vilar fortsatt på SfU6 2020/21, **symmetriskt skärpt föråldrad-flagga** på S/MP/C-raderna. Att
städa bort de overifierbara raderna skulle lämna enbart Tidöblocket → blocktilt; den tvåsidiga RiR-spliten bär neutraliteten.
(3) **BEKRÄFTAD** som appens första *differentierande* integration-B-mått (Beslut 2b): den tvåsidiga splitten (RiR-ankrad,
vunnen mot S/MP-regeringen, C+L korsade) är värdeneutral nog för den mest bias-känsliga kategorin.

#### Integration extra runda + alternativ-undermått-analys 2026-06-07 (§5.8 steg 2) ⭐

Användaren bad om en runda till med fler indikatorer för de två kvarvarande väggarna (boendesegregation, normer_tillit),
och om inget vettigt hittas — en §5.8-steg-2-analys av ALTERNATIVA undermått. Båda gjorda (3 agenter).

**Indikatorvändan:** båda väggarna bekräftade (se §6 "Extra runda"). Enda nya near-miss: normer_tillit IFAU 2017:12
(treåriga yrkesprogram → valdeltagande, partistyrbart instrument) — men UbU22-spliten är på fel värdeaxel (utbildnings-
kvalitet) → tilt. boendesegregation: 5 nya spår, alla wall (instrument-grind eller värdeaxel).

**Alternativ-undermått-analys (zoom-ut via IDEA.md "Arbete, språk, skolsegregation, självförsörjning, tillit"):**
**Inget alternativt undermått är en ren ersättare.** Prövade: (a) diskriminering arbets-/bostadsmarknad (D = bara
DO-anmälningar, icke-neutralt; varje instrument-ankare tiltat — AU10-avslag), (b) hälsogap inrikes/utrikes (= VÄLFÄRD-
överlapp), (c) utrikes kvinnors sysselsättning (= delmängd `arbete_sjalvforsorjning`, samma SCB TAB6529), (d)
medborgarskap/naturalisering (IFAU: effekten är SELEKTION ej kausal + värdeladdat), (e) barns skolnärvaro (= `skola_sprak`),
(g) barnfattigdom utrikes födda (= arbete/ekonomi-överlapp). Alla **dubbelräknar** ett befintligt undermått/annan kategori
eller faller på **samma neutralitetsvägg**. Att byta in en lättare fyra = exakt §5.8-spärren ("fuska inte").

**Enda starka fyndet — ett B-INSTRUMENT (ej nytt undermått):** **etableringseffektivitet** via **IFAU R 2023:19** (intensiv/
tidig etableringsinsats → ~+15 p.e. sysselsättning år 1; uppmätt KAUSAL effekt, medium/medium-värdig — starkaste steg-1 i
hela integrationssvepet). Men den **dubbelräknar `arbete_sjalvforsorjning`** (= ny instrument-väg in i ett REDAN B-grönt
undermått, inte ett nytt). Höjer inte 3/5→4/5, men skulle stärka integrationens B-robusthet (coverage). Steg-2-ankare
(AU-betänkande om etablerings-/intensitetsreform) **ej verifierat ännu** → kräver verifiering + codex om det byggs.

**Slutsats/rekommendation:** integration stannar på **3/5 B-grön** — det neutrala taket. boendesegregation + normer_tillit
redovisas som genuina HOLD-väggar (uttömda över flera rundor, med skärpta steg-1-vs-steg-2-diagnoser + konkreta
återöppningstriggrar). **Ersätt INTE** ett walls-undermått med ett alternativ (alla dubbelräknar/tiltar).
**ANVÄNDARBESLUT 2026-06-07: ACCEPTERA 3/5** — båda väggarna kvar som HOLD (återöppningstriggrar loggade), ingen
omstrukturering. Neutralitet före 4.

**EFTERSPEL 2026-06-07 — försök att stärka arbete_sjalvforsorjning med fler instrument (användarbegäran "flera mått"):**
RÄTTELSE: etablerings-"bonusen" (IFAU R 2023:19) är **ingen användbar reserv — den är en DUBBELRÄKNING.** R 2023:19 är
4-årsuppföljningen av SAMMA Göteborgs-RCT (Dahlberg) som redan ankrar `sfi_kombinerat_med_praktik`; att bygga den som
nytt instrument vore att blåsa upp arbete-B artificiellt → bygg ej. **Fresh sökning efter ett GENUINT DISTINKT instrument
(2026-06-07): inget byggbart.** yrkesvux/komvux (IFAU 2019:17) har neutrala partiankare men effekten för utrikes födda
*utanför Europa* är ~0 (snittet drivs av inrikes/vård) → `positive` vore tilt; validering (enda källa SNS Analys 72 =
före/efter, ingen kontroll → korrelation); KROM/Rusta-och-matcha (IFAU 2024:9 noll effekt + privatiserings-värdeaxel);
snabbspår (implementeringsuppföljning); subv. anställningar (redan i liggaren/undanträngning). **`sjalvforsorjningsgrad`
förblir B-tomt** (operationaliserat som SCB TAB6529 = utrikes föddas sysselsättningsgrad → kräver konstrukt-exakt
sysselsättnings-effekt för målgruppen). **Watch-lead:** kommande IFAU-effektutvärdering av regionalt yrkesvux/
kombinationsutbildningar med sysselsättningsutfall PER FÖDELSELAND (SOU 2024:16 "Växla yrke som vuxen") → då blir
yrkesvux byggbart (verifierade particitat finns redan: S/M/C/V/KD/L/MP, SD-lucka). **GJORT 2026-06-07 (användarbeslut):**
R 2023:19 lagd som bekräftande 4-års-RCT-källa till BEFINTLIGA `sfi_kombinerat_med_praktik` + confidence medium→high
(effekten består 10–20 p.e. i flera år, ej längre "bara en pilot"). **VIKTIGT — INGEN score-effekt:** dist byte-identisk.
B normaliserar `net_support` per riktning (num_sum/abs_sum), så confidence-vikten cancelar när ett partis claims pekar åt
samma håll; även CI oförändrad efter avrundning. Ändringen är alltså ren proveniens/kalibrering (korrekt confidence-värde,
forward-korrekt om modellen senare använder confidence för CI), version ej bumpad → sign-off.

---

### 8.8 Sign-off-checklista — ✅ GENOMFÖRD 2026-06-07 ⭐

> **SIGN-OFF GENOMFÖRD 2026-06-07 (användarbeslut, hela ytan nedan avgjord).** `version`-fälten bumpade 1→2
> (categories/evidence_ledger/party_positions) och `dist/scores.snapshot.json` re-baselinad (drift nollställd).
> Inget partibetyg/omdöme finns i kod — bara i versionsstyrd config (CLAUDE.md). Den ursprungliga checklistan
> bevaras nedan; utfallet per punkt:

**Utfall per punkt (beslut 2026-06-07):**
- **A. Alla 6 byggda B-mått BEHÅLLS** (Beslut 1: de 5 enhällighetsmåtten; Beslut 2: migration). Inget kastat.
- **B. sfi-kalibreringen BEKRÄFTAD** (Beslut 5).
- **C1. Migration tidsgrind — OMVERIFIERAD** (Beslut 2a): bred sökning i innevarande mandatperiod gav ingen nyare
  instrument-exakt källa för S/MP/C → kodningen behålls (vilar på SfU6 2020/21), **symmetriskt skärpt föråldrad-flagga**
  på S/MP/C-raderna. Valet: behåll alla rader (den tvåsidiga RiR-spliten bär neutraliteten; att städa bort skapar blocktilt).
  Migration bekräftad som appens första *differentierande* integration-B-mått (Beslut 2b).
- **C2. Transparens-dubbelräkning — ÅTGÄRDAD** (Beslut 3): C:s och MP:s rader i bunten
  `starkt_oberoende_granskning_och_insyn` omankrade från partifinansierings-citat till **lobbyregister** (C, HD023583 yrk. 17)
  resp. **offentlighetsprincipen** (MP, HA02181 yrk. 9), verifierade ordagrant mot `.text`. Partifinansiering krediteras nu
  ENDAST i `insyn_partifinansiering`. Poängneutralt (stance kvar supports).
- **C3. 3 nya indikatorer i `categories.yaml` — GODKÄNDA** (Beslut 9). Inga undermåttsvikter ändrade.
- **C4. Kalibreringen BEKRÄFTAD** (Beslut 4): mått 1–5 low/low, mått 6 medium/medium — ingen justering.
- **C5. `offentliga_finanser` LÄMNAS ⚪ kontext** (Beslut 6), ingen override.
- **C6. Snapshot RE-BASELINAD** (Beslut 10).
- **C7. `version`-fälten BUMPADE 1→2** (Beslut 11) + test_fas4.py uppdaterat.
- **D. HOLD-väggarna LÄMNAS, bevakas** (Beslut 7). De 4 döda indikatorerna omklassade till **🔴 BEVAKA** /
  utvidgningskandidat (Beslut 8). inflation/offentliga_finanser = medvetet target/kontext.
- **Beslut 12 (viktad stance):** ❌ ÖVERGIVEN samma dag efter utvärdering — spec + Codex (HOLD→DATAPILOT-FIRST) + datapilot (~7 % instrument viktbara, klustrade/budgetnära). Binär stance behålls. Se §8 fråga 2 + [done/viktad_stance_spec.md](viktad_stance_spec.md).
- **Beslut 13 (banan):** mandatperioden recency-viktat bekräftad nu; flera mandatperioder = framtida designfråga (se §8 fråga 3).

> **Ursprunglig checklista (bevarad — allt nedan nu avgjort ovan):**

**A. Byggda B-mått att behålla/kasta (6 st, alla v0):**
| # | Mått (kategori) | Källa/typ | Codex | Score-effekt |
|---|---|---|---|---|
| 1 | transparens_ansvar / `insyn_partifinansiering` (demokrati) | enhällighet KU19 p1, low/low | BUILD-WC | icke-rankningsdrivande |
| 2 | ekonomisk_ambition / NY `forsvarsfinansiering_upptrappning_mot_mal` (forsvar) | enhällighet FöU2, low/low | BUILD-WC | icke-rankningsdrivande |
| 3 | forebyggande / NY `kommunalt_brottsforebyggande_arbete` (trygghet) | enhällighet JuU9, low/low | BUILD | icke-rankningsdrivande |
| 4 | vard_tillganglighet / `koncentration_nationell_hogspecialiserad_vard` (valfard) | enhällighet SoU18, low/low | BUILD-WC | icke-rankningsdrivande |
| 5 | omsorg_personal / NY `kontinuitet_i_omsorgen` (valfard) | enhällighet SoU24, low/low | BUILD-WC | icke-rankningsdrivande |
| 6 | migrationssystem / NY `atervandande_effektivitet` (integration) | **genuin split** RiR 2020:7/SfU6 p2, medium/medium | KEEP-WC | **differentierande** (S −0,06, MP −0,04, M/SD/L +0,04…0,09) |

**B. Kalibrering att bekräfta (1 st):** `sfi_kombinerat_med_praktik` confidence medium→high + R 2023:19-källa (ingen score-effekt; ren proveniens).

**C. Specifika sign-off-frågor:**
1. **Mått 6 (migration) — TIDSGRIND:** stansen vilar på 2020/21 (SfU6); M/KD/L/SD bekräftas av Tidöavtalet 2022, men S/MP/C:s *nuvarande* hållning är ej omverifierad. Acceptera, eller kräv omverifiering mot innevarande mandatperiod? Och: godkänn att det är appens första *differentierande* integration-B-mått.
2. **Mått 1 (transparens) — DUBBELRÄKNING:** C/MP är även i bunten `starkt_oberoende_granskning_och_insyn` (→ korruption) ankrade på partifinansierings-citat. Omankra C/MP där, eller acceptera överlappet (båda icke-rankningsdrivande)?
3. **3 NYA indikatorer i `categories.yaml`** (forsvarsfinansiering_upptrappning_mot_mal, kommunalt_brottsforebyggande_arbete, kontinuitet_i_omsorgen) + 1 (atervandande_effektivitet) = strukturändring; normalt §5.8-spärr-2-sign-off, byggt v0 per mandatet. Inga undermåttsvikter ändrade.
4. **Kalibrering:** mått 1–5 är low/low (mekanism-/designevidens); mått 6 är medium/medium (RiR-auktoritetsutvärdering). Bekräfta kalibreringen.
5. **offentliga_finanser** lämnad ⚪ HOLD-kontext (codex: åtstramnings-tilt). Override möjlig (`langsiktig_finanspolitisk_hallbarhet` via FiU14-acklamation).
6. **Re-baselina `dist/scores.snapshot.json`?** Görs vid sign-off så drift nollställs.
7. **Bumpa `version`-fälten** i categories.yaml/evidence_ledger.yaml/party_positions.yaml (1→2) vid godkännande.

**D. HOLD-väggar (ingen åtgärd nu, bevaka triggrarna):** boendesegregation (steg-2/neutralitet; trigger: enhälligt bosättningslag-betänkande ~2027 + RiR 2021:29), normer_tillit (steg-2; trigger: enhälligt GOTV-anslag, el. acklamerat yrkesprogram + IFAU 2017:12), genomforbarhet_leverans (steg-1/instrument-effekt; trigger: FöU3-strategins effektredovisning), industriell_konkurrenskraft (steg-1 tvåsidig; trigger: ren positiv konkurrenskraftskälla för elnät NU15). + inflation/offentliga_finanser = medvetet target/kontext.

---

## 9. Beslutslogg

| Datum | Beslut | Skäl |
|---|---|---|
| 2026-06-05 | Mellanstatliga Sverige-utvärderingar tillåtna som **bekräftelse** (ej primär/index) | demokrati saknade officiell svensk effektutvärdering; dokumenterat i DATA.md |
| 2026-06-05 | "Neutralitet före 4" | tiltat mått skadar trovärdighet mer än saknat mått |
| 2026-06-06 | nato_medlemskap byggt (V=opposes, MP=none) | enda rena differentierande försvarsmåttet; codex-granskat. *(Öppen §8.4: V-straffet)* |
| 2026-06-06 | **Tvåstegsmodellen** antagen (§2): måttet ≠ positioneringen; differentiering är utfall, inte krav | natten gav 1 mått för att de två frågorna blandades; "väggen" var till stor del steg-2-källval |
| 2026-06-06 | **snabbforfarande_lagforing byggt** (trygghet 3→4, alla 8 supports) | enhällighet-som-källa, codex BUILD-WITH-CHANGES; första rena tillämpningen av §5.2 |
| 2026-06-06 | **atgarder_mot_invasiva_frammande_arter byggt** (klimat 3→4, alla 8 supports), **men FLAGGAD** | codex förordade HOLD (instrument-precision på rubrikcitatet); byggt v0 med instrument-mekanismcitat + konservativ kalibrering low/low — **din sign-off avgör om det behålls** (§8.5) |
| 2026-06-06 | **5 kandidater HOLD** (vård, omsorg, normer_tillit, boendesegregation, försvar-leverans) | steg 1 saknas/mixed eller fel konstrukt; "neutralitet före 4" + riktningsgrind står över täckningsmålet |
| 2026-06-06 | ✅ nato-byggets V-straff **OK** (användarbeslut) | objektivt belagt; V genuint Nato-kritiskt |
| 2026-06-06 | ✅ invasiva-arter-måttet **behålls** (användarbeslut) | "kan fylla på i framtiden"; värdeneutralt (alla supports), konservativt kalibrerat |
| 2026-06-06 | **Sökdjups-standard antagen** (§5.8): 5–7 instrument/delområde, flera rundor, zoom-ut via IDEA.md innan "uttömt" | första svepet var för grunt (~1 instrument/delområde, en runda); HOLD ≠ uttömt |
| 2026-06-06 | Dagens arbete **committat** (data:-prefix) | användarbeslut; fortsätter i fräsch session med §5.8 som spelbok |
| 2026-06-06 | **public service-lagen byggt** (demokrati 3/5→4/5, alla 8 supports) | enhällighet-som-källa (bet. 2025/26:KrU2 p1, acklamation), codex BUILD-WITH-CHANGES; instrument lagstadgat oberoende (prop. 2024/25:166 ur parlamentarisk kommitté SOU 2024:34) → mediefrihet; mekanism-/designevidens → konservativ kalibrering low/low; icke-rankningsdrivande |
| 2026-06-06 | **Djupsvep §5.8 på forsvar + valfard + integration** → HOLD ×5 bekräftat | 7+11+11 genuint olika instrument prövade (4 parallella researchagenter); äkta steg-1-väggar (leveranstid, boendesegregation) / fel konstrukt (omsorg_personal, normer_tillit) / steg-2-tilt (cancerscreening); återöppningsvillkor skärpta i §6. "Neutralitet före 4" + riktningsgrind står över täckningsmålet |
| 2026-06-07 | **B-grön-mandatet** antaget (användare): varje undermått ≥1 **B-grön** (D-grön räcker ej); nya indikatorer får byggas autonomt som v0 | vidgar scope förbi §5.8-spärr-2 FÖR DETTA SYFTE; regel 1 (neutralitet före 4) kvar överst |
| 2026-06-07 | **B-grön-svepet: 5 mått byggda v0** (transparens_ansvar, ekonomisk_ambition [NY ind.], forebyggande [NY ind.], vard_tillganglighet, omsorg_personal [NY ind.]) | 11 researchagenter + codex (4 BUILD-WC, 1 BUILD); alla enhällighet §5.2, alla 8 supports, low/low, FLAGGADE; demokrati/trygghet/valfard → FULLT, forsvar 3/5→4/5; ranking oförändrad, inget parti straffat |
| 2026-06-07 | **5 undermått HOLD** (genomforbarhet_leverans, industriell_konkurrenskraft, boendesegregation, normer_tillit, migrationssystem) | bygge skulle kräva tilt/fabrikat; konkreta kandidat-indikatorer för sign-off i §8.7; "neutralitet före 4" |
| 2026-06-07 | **offentliga_finanser HOLD-som-kontext** (directional konvertering avvisad) | codex: efterlevnad-av-ramverket privilegierar åtstramning + dubbelräkning A/c2 + target-konstrukt i directional B; lämnas ⚪ likt inflation. Q2-beslut "konvertera där meningsfullt" → ej här |
| 2026-06-07 | **Snapshot ej re-baselinad** | kumulativ drift syns; re-baseline är sign-off-åtgärd |
| 2026-06-07 | **Negativ evidens bekräftad som giltig B-väg** (användarens metodpoäng) | redan i modellen: evidensliggarens `direction: negative` + `_FLIP` + §10-grind 1 (authority_evaluation/systematic_review + conf≥medium). Att avveckla ett bevisat skadligt instrument → bra B, symmetriskt med positiv evidens. Villkor: mät systemfunktion, ej nivå/värdeval |
| 2026-06-07 | **Integration-svepet: migrationssystem BYGGT v0** (`atervandande_effektivitet` / `se_over_ansvarsfordelning_atervandande`, RiR 2020:7) | negativ-evidens-vinkeln; genuin tvåsidig split (SfU6 p2, votering verifierad mot data.riksdagen.se); codex KEEP-WITH-CHANGES; integration 2/5→3/5; ranking oförändrad |
| 2026-06-07 | **boendesegregation kamera-väg byggd → REVERTERAD** (codex KILL) | trygghet-evidens ometiketterad som integration + dubbelräknar `situationell_prevention_kamerabevakning` + exakt §8.7-varningen + 7-1≈noll differentiering; "neutralitet före 4" → äkta steg-1-vägg kvarstår |
| 2026-06-07 | **normer_tillit förblir HOLD** efter kandidatnedstigning (#1 GOTV → #2/#3/egna) | steg 1 löst (Delmi 2025:5) men inget neutralt steg-2-ankare; övriga kandidater wall på instrument-grind; "neutralitet före 4" + riktningsgrind |
| 2026-06-07 | **boendesegregation: full nedstigning #2–#5** → HOLD; **logg-rättelse** | #2 bosättningslag passerar steg 1 (RiR 2021:29) men faller på steg-2-värdekonflikt (självstyre); #3/#4/#5 wall. Diagnos: STEG 2/neutralitet, EJ steg 1 (gamla loggen fel) |
| 2026-06-07 | **genomforbarhet_leverans + industriell_konkurrenskraft: nedstigning** → båda HOLD, men **väggarna krympta** | genomforbarhet: STEG 2 LÖST (FöU3 p1 acklamation), kvar enbart steg-1/instrument-effekt → en effektutvärdering räcker för BUILD. industriell_konkurrenskraft: neutralt ankare finns (elnät NU15 p1 acklamation) men steg 1 tvåsidigt (Tillväxtanalys: elektrifiering→"förlorad konkurrenskraft"); D-serie (utsläpp/förädlingsvärde) finns men ≠ B. Inget byggt — "neutralitet före 4" |
| 2026-06-07 | **Integration extra indikatorvända + alternativ-undermått-analys** (för att nå 4/5) → integration stannar på **3/5** | nya indikatorspår (boendesegr: DO/Bostad först/RiR 2024:15/CU13; normer: IFAU 2017:12/2018:3/heders/diskriminering) alla wall; alternativ-undermått-analys: inget rent byte (alla dubbelräknar befintligt undermått/annan kategori eller tiltar) → §5.8-spärr "fuska inte" → behåll HOLD, ersätt ej. Etablerings-instrument (IFAU R 2023:19) starkt men dubbelräknar arbete_sjalvforsorjning (öppet sign-off-val) |
| 2026-06-07 | **Integration ACCEPTERAS på 3/5** (användarbeslut) | inget neutralt 4:e undermått finns (båda väggar äkta, alla alternativ dubbelräknar/tiltar); omstrukturering avvisad; "neutralitet före 4". Etablerings-bonusen ej byggd. Väggarnas återöppningstriggrar bevakas |
| 2026-06-07 | **arbete_sjalvforsorjning: inget nytt distinkt instrument byggt** (användarbegäran "flera mått") | etablering IFAU R 2023:19 = DUBBELRÄKNING (samma Göteborgs-RCT som sfi_kombinerat_med_praktik); fresh sökning (yrkesvux/validering/KROM/snabbspår/subv.) wallar på evidens-grind (~0 effekt för utrikes födda / korrelation / noll effekt) el. neutralitet; bygg ej (att koda yrkesvux positive vore tilt). sjalvforsorjningsgrad förblir B-tomt; watch-lead IFAU yrkesvux per födelseland (SOU 2024:16). Öppet sign-off: stärk sfi_kombinerat_med_praktik m. R 2023:19 (4-års-RCT, ev. conf medium→high) |
| 2026-06-07 | **sfi_kombinerat_med_praktik stärkt** (användarbeslut): R 2023:19 som bekräftande 4-års-RCT-källa + confidence medium→high | RCT-uppföljning visar att effekten består (10–20 p.e. flera år) → ej längre "bara en pilot". **INGEN score-effekt** (dist byte-identisk: B normaliserar net_support per riktning → confidence cancelar för samriktade claims; CI oförändrad). Ren proveniens/kalibrering; version ej bumpad → sign-off |
| 2026-06-07 | ✅ **SIGN-OFF GENOMFÖRD** (hela §8.8-ytan, användarbeslut): alla **6 byggda B-mått behålls** (Beslut 1+2); kalibreringen (1–5 low/low, 6 medium/medium) + sfi medium→high **bekräftade** (Beslut 4+5); `offentliga_finanser` lämnas **⚪ kontext** ingen override (Beslut 6); HOLD-väggarna **lämnas/bevakas** (Beslut 7); 3 nya indikatorer i categories.yaml **godkända** (Beslut 9). | flaggade v0-mått mognade till godkänd config; "neutralitet före 4" upprätthållen genom hela bygget |
| 2026-06-07 | **version-fälten bumpade 1→2** (categories/evidence_ledger/party_positions) + test_fas4.py; **dist/scores.snapshot.json re-baselinad** (drift nollställd) (Beslut 10+11) | sign-off-åtgärder; ackumulerad drift från B-grön- + integration-svepen inlåst. **Bottenflip SD>V** (var V>SD vid förra baslinjen) = följd av att SD:s täckningsluckor fyllts med konsensusmått (SD störst lyft +0,133, mest välfärd); ej bias (alla nya mått alla-8-supports), ej från dagens edits (byte-identisk dist). Topp 6 oförändrad |
| 2026-06-07 | **Transparens-dubbelräkning ÅTGÄRDAD** (Beslut 3): C/MP:s rader i bunten `starkt_oberoende_granskning_och_insyn` omankrade från partifinansiering → **lobbyregister** (C, HD023583 yrk. 17) resp. **offentlighetsprincipen** (MP, HA02181 yrk. 9) | codex-dubbelräkningsflaggan stängd; partifinansiering krediteras nu ENDAST i `insyn_partifinansiering`. Citat verifierade ordagrant mot `.text`; poängneutralt (stance kvar supports). Princip: en post bär en fråga |
| 2026-06-07 | **Migration tidsgrind OMVERIFIERAD → behåll alla rader, skärp föråldrad-flagga** (Beslut 2a, val A) | bred sökning innevarande mandatperiod (SfU-motioner, plattformar, prop. 2025/26:263 + följdmotioner) gav INGEN nyare instrument-exakt S/MP/C-källa om ansvarsfördelningen för återvändande → kodningen vilar fortsatt på SfU6 2020/21, symmetriskt flaggad föråldrad. Att städa bort de overifierbara raderna skulle lämna enbart Tidöblocket → blocktilt; den tvåsidiga RiR-spliten bär neutraliteten. Bekräftad som appens första differentierande integration-B-mått (Beslut 2b) |
| 2026-06-07 | **4 döda indikatorer omklassade → 🔴 BEVAKA / utvidgningskandidat** (Beslut 8): personalomsattning_omsorg, leveranstid_materiel, segregation, tillit_valdeltagande | poängneutralt (renormaliseras redan bort, score.py aggregate_B); behålls med återöppningsvillkor istället för att strykas — kan bli kandidater när ny indikator/evidens dyker upp. §8 fråga 6 löst |
| 2026-06-07 | **Viktad stance ÖVERGIVEN** (Beslut 12 — antagen som idé, men avgjord NEJ samma dag efter utvärdering) | spec [done/viktad_stance_spec.md](viktad_stance_spec.md) skriven; Codex v1→HOLD, v2 (10 punkter åtgärdade)→DATAPILOT-FIRST; **datapilot: ~3/43 instrument (≈7 %)** har kvantifierad ambitionsnivå, klustrade i forsvar+klimat, mest budgetnära → alla kill-kriterier föll in (lägre än Codex 10–25 %-prior). Strukturell orsak: instrumentbaserad modell ⇒ instrument är diskreta reformer; grad bor i budgetnivåer (= A). Binär stance behålls som rätt passform. "Neutralitet före 4" (kategori-asymmetri-risk K1) |
| 2026-06-07 | **Banan: mandatperioden recency-viktat BEKRÄFTAD** (Beslut 13) nu; **flera mandatperioder = framtida designfråga** | nato-regeln står (varaktiga omsvängningar kodas efter nuläget). Att väga in flera mandatperioder kräver designbeslut om hur historik ska tyngas utan att bli "straffa-konvertiter"-maskin (§5.5). §8 fråga 3 |
| 2026-06-12 | **B3: 2 omstridda poster byggda v0 FLAGGADE** — (1) `nedtrappad_ersattningsprofil_akassa` (ekonomi → arbetsloshet; IFAU 'Om a-kassa och löner'; votering bet. 2023/24:AU9 p1: 7 supports / V opposes via motion 2023/24:2881) + (2) `uppsokande_forskoleerbjudande_nyanlandas_barn` (integration → skolresultat_utsatta_omraden; SOU 2020:67; votering bet. 2021/22:UbU24 p1: 6 supports, **SD/KD ej kodade**) | codex BUILD-WITH-CHANGES ×2; voteringar + alla citat omverifierade ordagrant mot data.riksdagen.se (votering-API + .text). Instrumentlåsning a-kassa: NEDTRAPPAD PROFIL (prop. 2023/24:128-designen), ej generisk 'lägre a-kassa'; indikator-brygga nivå (R 2008:12 +1,5 pe), nedtrappningsmekanism (WP 2007:21), heterogenitet/simulering → medium/medium; spegelpost-notering mot `inkomststarkande_hushallspolitik` (metodneutralitet). SD/KD-utelämning per MP/Nato-prejudikatet (2022-nej + Tidö-dir. 2024:113 = snävare instrument i samma familj → none). Scoreeffekt förklarbar, **ranking oförändrad** (S>L>M>KD>MP>C>SD>V): V ekonomi −0,22 (opposes-flip), KD −0,15/SD −0,09 integration (coverage-nämnare 5→6 = 'vet ej'-krympning), MP +0,13 (thin-coverage släckt). C2 DCA + C4 preventiva = HOLD för sign-off |
| 2026-06-12 | **B3 beslutsfråga B1 = JA → `dca_avtal_usa` byggt v0 FLAGGAD** (forsvar → nato_interoperabilitet; Försvarsberedningen Ds 2024:6, medium/high; bet. 2023/24:UFöU1 p1 266–37, kvalificerad 3/4-majoritet: 6 supports S/M/SD/C/KD/L, **V + MP opposes** via avvikande meningar i Ds 2024:6 bilaga 4). **B2 (preventiva tvångsmedel) kvarstår HOLD** | användar-sign-off med Codex-villkoren, alla tre uppfyllda: (1) anti-stacknings-not i liggarposten (DCA = bilateralt basavtal vs nato_medlemskap = multilateralt alliansmedlemskap; prejudikat territoriella_utslapp; V:s ANDRA opposes-post på indikatorn = sign-off:ad avvägning — differentieringsvinsten MP vägde tyngre); (2) p1-källkonstruktion dokumenterad (huvudvoteringen saknas i voteringlista-API:t, verifierat @antal=0 + tomt votering_id i dokumentstatus HB01UFöU1 → beslutsnotis 'Kammaren biföll utskottets förslag' + följdvoteringarna p5 'Nedrustning' A1C914E0 266/37 V+MP Nej och p3 'Kärnvapen' A52E4273 V Nej/MP Avstår, båda OMVERIFIERADE LIVE 2026-06-12); (3) stance-confidence medium på alla 8 p1-härledda rader. Alla citat (3 Ds-utsagor + V + MP) ordagrant omverifierade mot fulltexten. MP:s villkorade nej (kärnvapenförbudslag) = bunten-regeln §2, nyans ändrar ej stance; MP:s FÖRSTA aktuella position på indikatorn. Scoreeffekt förklarbar, **ranking oförändrad** (S>L>M>KD>MP>C>SD>V): C/KD forsvar +0,04 (coverage 3/4→4/5), MP forsvar −0,13 (ny opposes + coverage 1/4→2/5), S/M/SD/L/V forsvar oförändrade (indikatorcellen redan mättad ±1; coverage 4/4→5/5 = kvot 1,0). Drift-vakt-testet test_b_coverage_mode (handräknat MP/forsvar 25→32,5/100 i weighted-läget) uppdaterat per sin egen täckningsdrift-regel |
| 2026-08-16 | **KU39/transparens_ansvar PRÖVAD OCH FÄLLD → HOLD med trigger** (inget bygge; §6 demokrati uppdaterad) | Voteringen ägde rum (p1, `DCA347C0-D1CA-40A9-9748-2797405C09CB`, beslut 2026-06-16, 174/172, Ja = M/SD/KD/L) men punkten **buntar tre lagar**, varav lag 2 (arbetsmarknadsorganisationers partipolitiska bidrag) är den bygginstruktionen förbjuder att koda (S-tilt). Enda punkten i betänkandet → delen går inte att lyfta ut. Båda följdmotionerna (S 2025/26:4151, C 2025/26:4184) yrkade avslag ENBART på lag 2; ingen invände mot lobbyregistret eller 2018:90-skärpningarna. `opposes` på Nej-sidan vore därmed ett fabrikat, enbart Ja-sidan vore ensidigt blocktillskott i den mest bias-känsliga kategorin. **Neutralitetsgrind punkt 4** ("buntade omnibuspunkter förkastas") är avgörande. Låg kostnad: undermåttet redan täckt via `insyn_partifinansiering`, demokrati 5/5. Återöppning = steg-2-källbyte (§4.1) på enbart lobbyregistret; obs dubbelräkningsrisk mot C:s HD023583 yrk. 17 i `starkt_oberoende_granskning_och_insyn` |

---

## 10. Verifierings- & provenansstandard (grindar varje mått måste passera)

Sammanfattar grindarna — fullständigt i [fas4b §4, §8](fas4b_partistandpunkter_metod.md) och
[fas4c_rubrik.md](fas4c_rubrik.md).

1. **Riktningsgrind (steg 1)** — instrumentets effekt på indikatorn belagd av officiell svensk källa
   (akademisk svensk om officiell saknas). Negativt B-bidrag kräver `authority_evaluation`/
   `systematic_review` + `confidence ≥ medium` + exakt indikator.
2. **Instrument-grind** — källan avser *samma instrument*, inte bara samma mål (gäller *alla* källor på
   stegen §5.1, inte bara voteringar).
3. **Stance-grind (steg 2)** — ordagrant citat + dok-id; confidence enligt källstegen; `enskild_motion`
   flaggas svag.
4. **Neutralitetsgrind** — inget systematiskt vänster/höger- eller regering-vs-opposition-tilt; buntade
   omnibuspunkter förkastas; vid tvekan codex/2nd-opinion.
5. **Tidsgrind** — föredra innevarande mandatperiod; dokumentera om en hållning kan vara föråldrad
   (jfr MP/nato-reverseringen → `none`, §5.5).
6. **Verifiering** — oberoende kodare hämtar fulltext (`.text`) och prövar quote_found ∧
   instrument_precise ∧ confirmed; default skepsis.

Efter bygge: `python -m pytest -q` (grön), `python -m ruff check pipeline tests` (rent), cyrillisk-koll
`[Ѐ-ӿ]` (0), `pipeline.scorerun` (bygg om dist), `coverage_report` (B4-spridning), `score_diff` (effekt
mot snapshot), `review_packet` (granskningspaket). Snapshot re-baselineas **bara** vid sign-off.

---

## 11. Ändringslogg (denna fil)

| Datum | Ändring |
|---|---|
| 2026-06-06 | Skapad efter natt-resultatet 1 mått: väggen, metodregister (kärna enhällighet-som-källa), designfråga, statustavla, kandidat-pipeline. |
| 2026-06-06 | **Omstrukturerad kring tvåstegsmodellen** (§2): måttet skilt från positioneringen; "väggen" omklassad till steg-1-väggar (äkta) vs steg-2-källval (lösbart, §4); metodregistret blev "steg 2 — positionering" (§5) med källstege + budget-/kommittémotion (§5.3) + banan (§5.5) + uttryckliga gränser inkl. grad/magnitud-begränsningen (§5.6); differentiering omdefinierad som utfall, inte krav; öppna designfrågor samlade (§8). |
| 2026-06-06 | **Första leveransen på metoden:** 7 kandidater researchade (codex-2nd-opinion), **2 byggda** (snabbforfarande → trygghet 4/5; invasiva arter → klimat 4/5, FLAGGAD) **+ 5 HOLD**. §3/§6/§7/§8/§9 uppdaterade med utfall; 36 evidensposter / 192 ståndpunkter; 167 tester gröna, ruff rent, inga nära-binära. Enhällighet-som-källa empiriskt bekräftad (löste steg-2-väggen för #1/#2). |
| 2026-06-06 | **§5.8 sökdjup + zoom-ut tillagt** (5–7 instrument/delområde, flera rundor, läs IDEA.md + bred analys när du kör fast, leta nya undermått). §7 markerat som "första svep, ej uttömt". §8.4/§8.5 markerade BESLUTADE (nato OK, invasiva behålls). Dagens arbete committat; fortsättning i fräsch session. |
| 2026-06-06 | **§5.8 skärpt till eskaleringstrappa:** "inget instrument hittat" är inte slutstation — eskalera då till **nytt undermått** (zoom-ut via IDEA.md). "Fast/uttömt" får sättas först när BÅDE instrument- OCH undermått-spåret är uttömda. Spärrar kvar: fuska inte med undermått, struktur kräver sign-off. |
| 2026-06-06 | **§4.3 mätbarhetskarta tillagd** (på användarfråga): varje indikator klassad B/D → ✅ mäts / 🟡 mätbart-ej-byggt (10) / 🔴 ej mätbart (4) / ⚪ target (3). De 4 röda = exakt de 4 HOLD-undermåtten → designfråga §8.6 (borttagning/omklassning, sign-off). De 10 gula ska byggas, ej strykas. |
| 2026-06-06 | **Andra svepet (§5.8 tillämpat):** demokrati **3/5 → 4/5** via public service-lagen (KrU2 p1 enhällighet, codex BUILD-WITH-CHANGES, low/low). forsvar/valfard/integration djupsvepta (7+11+11 instrument, 4 parallella researchagenter, alla röstsiffror verifierade mot data.riksdagen.se) → **HOLD ×5 bekräftat** med skärpta återöppningsvillkor (§6). Nya fynd: vårdplats-slutrapport 2026:3 föll *nedåt* (villkor konsumerat); **cancerscreening** (valfard) + **KU4-tillgänglighet** (integration) = near-miss som faller på steg-2-tilt resp. fel konstrukt; **KU39 insyn i politiska processer** = stark demokrati-återöppning (beslut 2026-06-15). 37 evidensposter / 200 ståndpunkter; 167 tester gröna, ruff rent, 0 cyrilliska. §3/§6/§9 uppdaterade. |
| 2026-06-06 | **Begreppsmodell stringentad (på användarfråga):** kanonisk vokabulär **Kategori → Undermått → Indikator → Riktning** låst i §4.3-ordlista; "submått" → **Undermått** normaliserat i alla 5 dok (IDEA/DATA/BACKLOG/ROADMAP/evidens_trovardighet, 116 förekomster); IDEA.md + BACKLOG.md pekar nu på §4.3 som sanningskälla. **Config-bugg fixad:** 4 undermåttsnamn (Nato/Skola/Normer/Finansiering) var trunkerade av oquoterade kommatecken i `categories.yaml` flow-YAML → citerade. **§4.3 fick mastertabell** över samtliga **35 undermått / 52 indikatorer** (Kategori/Undermått/Indikator/Riktning/Mätstatus, genererad ur config; de 3 undermått som *saknar indikator* — forebyggande/industriell_konkurrenskraft/migrationssystem — listas som egna rader). dist byte-identisk (namn påverkar ej betyg); 167 tester gröna. |
| 2026-06-07 | **sfi_kombinerat_med_praktik stärkt + §8.8 sign-off-checklista + doc-konsistensgenomgång:** R 2023:19 (4-års-RCT) lagd som bekräftande källa + confidence medium→high (användarbeslut) — ingen score-effekt (dist byte-identisk, B normaliserar net_support per riktning). Ny **§8.8 = samlad sign-off-yta** (6 byggda v0 + 1 kalibrering + 7 sign-off-frågor + 4 HOLD-väggar) inför kommande sign-off-session. §3-timestamp + §6-banner uppdaterade; counts verifierade (43 poster / 247 ståndpunkter / 29 av 35 B-grön). |
| 2026-06-07 | **arbete_sjalvforsorjning fler-mått-försök (användarbegäran "bygg arbete_sjalvforsorjning, flera mått"):** 2 agenter. Etablering IFAU R 2023:19 = **DUBBELRÄKNING** (4-årsuppföljning av samma Göteborgs-RCT som redan ankrar sfi_kombinerat_med_praktik) → bygg ej. Fresh sökning efter GENUINT DISTINKT instrument: **inget byggbart** — yrkesvux/komvux (IFAU 2019:17 effekt ~0 för utrikes födda utanför Europa → positive vore tilt), validering (SNS 72 = före/efter/korrelation), KROM (IFAU 2024:9 noll effekt + privatiserings-axel), snabbspår/subv. anställningar (uppföljning/dubbelräkning). sjalvforsorjningsgrad förblir B-tomt; watch-lead IFAU yrkesvux per födelseland (SOU 2024:16). **Inget byggt, ingen config-ändring** — "neutralitet före 4" (koda ej en effekt källan inte bär). Öppet sign-off: stärk befintliga sfi_kombinerat_med_praktik m. R 2023:19 (4-års-RCT). §8.7/§9. |
| 2026-06-07 | **INTEGRATION EXTRA RUNDA + ALTERNATIV-UNDERMÅTT (användarbegäran: en vända till för att nå 4/5, annars byt undermått):** 3 agenter (fresh indikatorvända boendesegr + normer_tillit, samt §5.8-steg-2 strukturanalys). **Båda väggarna bekräftade på GENUINT NYA spår** (ej omprövning): boendesegr — DO-diskriminering, hemlöshet/Bostad först, bostadsbidrag RiR 2024:15, CU13-acklamation, alla wall; normer_tillit — **ny near-miss IFAU 2017:12** (yrkesprogram→valdeltagande, partistyrbart) men UbU22-split på fel värdeaxel = tilt, + IFAU 2018:3/heders/diskriminering wall. **Alternativ-undermått: inget rent byte** — diskriminering/hälsogap/utrikes kvinnor/medborgarskap/skolnärvaro/barnfattigdom dubbelräknar alla befintligt undermått/annan kategori eller tiltar (§5.8-spärr). Enda starka fynd = **etablerings-B-instrument** (IFAU R 2023:19, uppmätt kausal) men dubbelräknar arbete_sjalvforsorjning (öppet sign-off-val). **integration stannar 3/5**; inget byggt; "neutralitet före 4". §6/§8.7/§9 uppdaterade, ingen config-ändring. |
| 2026-06-07 | **HOLD-VÄGG-NEDSTIGNINGAR (användarbegäran "gå igenom dem med"):** dedikerade kandidatnedstigningar för de återstående HOLD-väggarna. **boendesegregation:** #2–#5 prövade → HOLD, men logg-rättelse (RiR 2021:29 ÄR kausal kommunanvisning-utvärdering; väggen är STEG 2/neutralitet, ej steg 1) + skärpta återöppningsvillkor. **genomforbarhet_leverans (forsvar):** STEG 2 LÖST (bet. 2025/26:FöU3 p1 acklamation, alla 8) → väggen krympt till enbart steg-1/instrument-effekt; en effektutvärdering räcker nu för BUILD. **industriell_konkurrenskraft (klimat):** neutralt ankare finns (elnät bet. 2023/24:NU15 p1 acklamation) men steg 1 tvåsidigt (Tillväxtanalys: elektrifiering→"förlorad konkurrenskraft"); RiR 2024:17 "oklart"≠belagd negativ; D-serie utsläpp/förädlingsvärde finns (≠ B). **Inget byggt** (inget passerar båda grindar) — "neutralitet före 4". §6/§8.7/§9 uppdaterade; ingen config-ändring. |
| 2026-06-07 | **INTEGRATION-SVEPET (användarfokus: fyll integrations otäckta undermått; metodpoäng: negativ evidens lika giltig som positiv):** 3 researchagenter (5 förslag/undermått) + per-parti-verifiering mot data.riksdagen.se + codex adversariell granskning. **migrationssystem BYGGT v0** (NY ind. `atervandande_effektivitet` / `se_over_ansvarsfordelning_atervandande` / RiR 2020:7; genuin tvåsidig split SfU6 p2: supports M/KD/SD/C/L, opposes S/MP, V none; codex KEEP-WITH-CHANGES — policy_type snävad "samla"→"se över", tidsnot 2020/21). **boendesegregation: kamera-väg byggd → REVERTERAD** (codex KILL: trygghet-relabel + dubbelräkning + §8.7-varningen + 7-1≈noll diff). **normer_tillit: HOLD** (Delmi 2025:5 löser steg 1; inget neutralt steg-2-ankare; nedstigning #2/#3/egna wall på instrument-grind). **Integration 2/5→3/5**; isolerad effekt: **ranking OFÖRÄNDRAD** (S>L>M>KD>MP>C>SD>V), endast integration rörd (S −0.063, MP −0.044, M/SD/L +0.04…0.09); 43 evidensposter / 247 ståndpunkter; 167 tester gröna, ruff rent, 0 cyrilliska, config valid. §4.3/§6/§8.7/§9/§11 uppdaterade. snapshot ej re-baselinad. Väntar sign-off. |
| 2026-06-07 | **B-GRÖN-SVEPET (användarmandat: varje undermått ≥1 B-grön):** 11 parallella researchagenter + codex adversariell granskning → **5 mått byggda v0** (insyn_partifinansiering→transparens; NY forsvarsfinansiering_upptrappning_mot_mal→ekonomisk_ambition; NY kommunalt_brottsforebyggande_arbete→forebyggande; koncentration NHV→överlevnad; NY kontinuitet_i_omsorgen→omsorg_personal). Alla enhällighet-som-källa §5.2 (alla 8 supports, acklamation verifierad mot data.riksdagen.se dokumentstatus, citat verbatim-kollade), low/low, FLAGGADE. **Demokrati 4/5→5/5, trygghet 4/5→5/5, valfard 2/4→4/4 (alla FULLT), forsvar 3/5→4/5.** **5 HOLD** (genomforbarhet_leverans, industriell_konkurrenskraft, boendesegregation, normer_tillit, migrationssystem — genuina väggar, kandidat-indikatorer §8.7) + **offentliga_finanser HOLD-kontext** (codex: åtstramnings-tilt). 42 evidensposter / 240 ståndpunkter; **isolerad effekt: ranking OFÖRÄNDRAD** (S>L>M>KD>MP>C>SD>V), alla cellförändringar positiva (inget parti straffat); ruff rent, 167 tester gröna, config valid, B4 inga nära-binära. §3/§4.3/§6/§8.6/§8.7(ny)/§9 uppdaterade. snapshot ej re-baselinad. Väntar mänsklig sign-off. |
| 2026-06-07 | ✅ **SIGN-OFF-SESSION GENOMFÖRD (§8.8-ytan stängd):** Användaren gick igenom alla öppna frågor och avgjorde. **Verkställt i config:** (3) transparens-dubbelräkning åtgärdad — C omankrad till lobbyregister (HD023583 yrk. 17), MP till offentlighetsprincipen (HA02181 yrk. 9), båda verifierade ordagrant mot `.text` av researchagent; (2a) migration S/MP/C omverifierade mot innevarande mandatperiod (ingen nyare källa → behåll, skärpt föråldrad-flagga); (8) 4 döda indikatorer → 🔴 BEVAKA-noter; (11) version 1→2 i tre config-filer + test; (10) snapshot re-baselinad (drift nollställd). **Allt poängneutralt** (`git diff dist/scores.json` tom; bara svepens ackumulerade drift inlåst → bottenflip SD>V, topp 6 oförändrad). 167 tester gröna, ruff rent, 0 cyrilliska, B4 inga nära-binära, ranking S>L>M>KD>MP>C>SD>V. **Beslut 12 (viktad stance) antagen** som kommande förbättring (sekvensering vs D under beslut); **Beslut 13 (banan)** mandatperioden bekräftad, flerperiod framtida designfråga. §3/§4.3/§6/§8/§8.7/§8.8/§9/§11 uppdaterade. |
| 2026-06-07 | ❌ **VIKTAD STANCE UTVÄRDERAD → ÖVERGIVEN (Beslut 12):** spec [done/viktad_stance_spec.md](viktad_stance_spec.md) skriven (grad/magnitud i B). Codex adversariell granskning v1 → HOLD (för svaga spärrar); v2 åtgärdade 10 punkter (G6 instrumenturval, G7 ankartaxonomi, m_min-band, A-dubbelräkningstest) → Codex DATAPILOT-FIRST. **Datapilot** (icke-scoring kartläggning av alla 43 instrument): bara ~3/43 (≈7 %) har kvantifierad ambitionsnivå, klustrade i forsvar+klimat, mest budgetnära → alla kill-kriterier föll in. **Användarbeslut: ÖVERGE.** Strukturell slutsats: instrumentbaserad modell ⇒ binär stance är rätt passform (grad bor i budgetnivåer = A). Spec + denna fil flyttade till `docs/done/`. Ingen config-/kodändring; binär modell oförändrad. §8 fråga 2 + §8.8 + §9 uppdaterade. |
| 2026-08-17 | **A OMDÖPT TILL PRIORITERING (ADR 0001, biljett #7 under karta #6):** `IDEA.md` definierade A som "röstat, budgeterat, föreslagit, genomfört", men byggd A är a1 budgetandel + a2 motionsandel, riktningsneutralt. Beslut: A heter **Prioritering** och mäter omfattning; voteringarna stannar i B; "genomfört" hör till C och D. **Ny regel mot dubbelräkning:** gränsen mellan delpoängen går vid frågan, inte vid källan (en budgetmotion bär både A:s ramar och B:s ståndpunkt). §4.3 fick delpoängsordlista. Ingen kod-/configändring, ranking oförändrad; kvar till byggslice: kommentaren under `A_agerande` + etiketten i gränssnittet. Viktfrågan skickad vidare till #9, skärpt: prioritering väger 40 % mot evidensens 35 %. |
| 2026-08-18 | **VIKTERNA HÄRLEDDA OCH LÅSTA (ADR 0002, biljett #9 under karta #6):** 40/35/15/10 var asserterat utan härledning. Kedjan: anspråket avgörs före vikten (OECD/JRC steg 1, underlag #8) → **anspråket = hur mycket kategorin väntas förbättras om partiets politik genomförs**. Ur det följer **B > A** (endast B bär riktning, förhållandet 5:3), **C = 0** (anspråket villkorar redan på genomförande, så innehavd makt svarar på en fråga betyget inte ställer; C blir **ansvarsunderlag** och bär attributionen för D) och **D = 20 %** (kontrolledet ska nå 1,0 poäng vid maximal motsägelse, alltså vända ett jämnt läge men inte ett tydligt försprång). **Ny formel: 0,30 A + 0,50 B + 0,20 D.** Halvbredden går 0,44 → 0,58 med standardsäkerheterna och kompenseras inte. Beslutet är **rankingrelevant** men taget blint mot rankingen enligt kartans regel. Ändrat nu: ADR 0002, `IDEA.md` §Bedömningskedja/§Grundformel/§Delpoäng, §4.3. Kvar till byggslice: `scoring.yaml`, `categories.yaml`, metodrutan i `web/app.js`, `coverage_technical`; pipen körs om först på uttrycklig order. |
| 2026-08-18 | **MAKTANDELENS FÖNSTER RÄTTAT + C OMDÖPT (biljett #14 under karta #6):** `government_fractions()` satte den sittande regeringens periodslut till `WINDOW_END` (valdagen 2026-09-13) och lät nämnaren gå dit, så regeringen Kristersson tillgodoräknades maktdagar den inte suttit och alla fraktioner späddes av en framtida nämnare. Ny handsatt konstant `POWER_WINDOW_END` = 2025-12-31 (sista dagen i sista avslutade observationsåret) på `scorerun.py:66,69,187`; `WINDOW_END` står kvar på sina tre rätta jobb. **C bytte namn `Ansvarsunderlag` → `Maktandel`**, eftersom *ansvarsunderlag* redan är D:s grindstorhet (Σ maktvikt över de attribuerade åren) och den användningen är äldre. **ADR 0002 punkt 5 rättad** (§ Rättelse 2026-08-18): C bär INTE attributionen för D, `min_responsibility` grindar på D:s eget `basis`. **Biljettens antagande att rättningen är osynlig i utdatan höll inte:** `components.C` är en per-kategori-blandning av nationell och subnationell makt, och i trygghet korsar SD och C. Med C fortfarande på vikt 0,15 (ADR 0002:s viktslice ej körd) rör det kategoribetyget: C/trygghet 3,036 → 3,143, SD/trygghet 3,296 → 3,189. Totalrankingen och trygghets interna ordning oförändrade. Byggt på uttrycklig order efter att grinden fällts. |
