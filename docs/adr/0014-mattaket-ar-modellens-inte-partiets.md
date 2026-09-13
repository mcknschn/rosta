# ADR 0014: Mättaket är modellens, inte partiets

- Status: accepted
- Datum: 2026-09-13
- Beslutad i: biljett [#39](https://github.com/mcknschn/rosta/issues/39) under karta [#6](https://github.com/mcknschn/rosta/issues/6)
- Bygger på: [ADR 0002](0002-kategoripoangens-ansprak-och-vikter.md), [ADR 0003](0003-skiljbarhet-och-kanslighetsanalys.md), [ADR 0004](0004-vad-delpoang-b-mater.md), [ADR 0006](0006-evidensgrinden-ar-symmetrisk.md), [ADR 0008](0008-cellens-tackning.md), [ADR 0009](0009-sakerheten-mater-hur-val-talet-ar-kant.md) och [ADR 0011](0011-uteslutningen-ar-ett-eget-besked.md)

## Kontext

Biljett #39 kom ur en mätning gjord 2026-08-30. B väger 0,50 och bär 60,6 procent av
separationen. Reglaget `B_coverage_shrink` är modellens största: 6,15 kategoripoäng mot ett
brusgolv på 1,0. B:s täckning per cell har medianen 0,50, och ingen av de 56 cellerna når 1,00.

Biljetten frågade om halva täckningen är ett fel eller ett fynd. Om det är ett fel frågade den
vidare vad som får bli en post i evidensliggaren som inte får bli det i dag. ADR 0006 avgjorde
grindens **riktning** i biljett [#18](https://github.com/mcknschn/rosta/issues/18). Den här
biljetten frågade om grindens **nivå**.

Nivån visade sig inte vara det som binder. Under frågan låg en annan: vad påstår krympningen, och
om vem.

## Diagnos

Mätt 2026-09-13 mot `config/`, `pipeline/`, `dist/`, `web/` och git-historiken.

### 1. Biljettens eget underlag bar fyra fel

| Biljetten säger | Mätt | Följd |
|---|---|---|
| försvarstaket 0,55 | **0,50** | försvar har inget utrymme kvar |
| klimats högsta uppmätta 0,40 | **0,625** | klimats utrymme är 0,075, inte 0,30 |
| 31 kodbara åtgärdstyper | **28** | 31 är antalet antagna poster före `coverage_exclude` och före `mixed`/`unclear` |
| 18 celler under 0,50 | **22** | elva till ligger exakt på 0,50 |

Rättelsen gör biljettens diagnos starkare och inte svagare. Minst ett parti ligger exakt på taket i
**6 av 7 kategorier**, inte 5 av 7. Bara klimat har utrymme kvar på ståndpunktssidan.

### 2. Krympningen bär två skilda besked i ett tal

Ett undermått utan en enda namngiven åtgärdstyp bidrar 0 till täljaren och full vikt till nämnaren.
Det är **vår** tystnad. Ett undermått där liggaren har namngivit typer men partiet saknar ståndpunkt
är **partiets** tystnad.

Medel över alla 56 celler: krympningen är 0,480, varav **0,371 vår tystnad (77,2 procent)** och
**0,109 partiets (22,8 procent)**.

Vår tystnad är en **kategorikonstant**. Den är samma tal för alla åtta partier i en kategori. I
ekonomi ligger alla åtta på exakt 0,753, alltså är krympningen där helt och hållet vår.

### 3. Vår tystnad är 14 tomma undermått, och tio tömdes av ADR 0006

| kategori | tomma undermått | vikt |
|---|---|---|
| demokrati | korruption_tillit, yttrandefrihet_medier, transparens_ansvar | 55 |
| välfärd | vard_tillganglighet, omsorg_personal | 50 |
| försvar | ekonomisk_ambition, civil_beredskap, genomforbarhet_leverans | 50 |
| integration | boendesegregation, normer_tillit | 35 |
| klimat | industriell_konkurrenskraft, biologisk_mangfald | 30 |
| ekonomi | realloner_hushall | 18 |
| trygghet | forebyggande | 15 |

Tio av de 14 tömdes 2026-08-23 av utlyftet i [#26](https://github.com/mcknschn/rosta/issues/26),
exakt som ADR 0006 diagnos punkt 5 förutsåg. Tre är kända HOLD-väggar med färdiga
återöppningstriggar. En, `industriell_konkurrenskraft`, bär 15 av klimats 100 och har **noll
indikatorer**.

Medeltaket föll från **0,921 till 0,629** när utlyftet tillämpades.

### 4. Krympningen var störst redan före utlyftet, och utlyftet gjorde den mindre

Ur git-historiken för `dist/robustness.json`:

| körning | datum | `B_coverage_shrink` | näst största reglage |
|---|---|---|---|
| #21, före utlyftet | 2026-08-21 | **8,263** | D_attribution_lag_years 4,23 |
| #26, efter utlyftet | 2026-08-23 | **6,822** | D_attribution_lag_years 5,30 |
| #32, senaste | 2026-08-27 | **6,154** | D_attribution_lag_years 5,56 |

Det är signaturen punkt 2 förutsäger. En kategorikonstant kan aldrig vända ordningen mellan två
partier inne i kategorin. När dess andel steg föll reglagets uppmätta inflytande.

### 5. Den utlyfta postklassen kan inte skilja något parti

De 14 utlyfta posterna bär 79 partirader. **Alla 79 är `supports`. Noll `opposes`.** Nio av de 14
har alla åtta partierna, alltså är de konsensusmått. Två har noll partirader alls, så att släppa in
dem skulle **sänka** täckningen för alla åtta.

Svepet i #26, kört under den symmetriska grinden, gav dessutom en enda ny post. Grinden fäller
alltså inga kandidater, eftersom det inte finns några.

### 6. Redovisningen finns, men är tröskelstyrd och delvis fel

`config/coverage_allowlist.yaml` bär nyckeln `b_thin_breadth_accepted`, och
`tests/test_b_breadth_gate.py` tvingar fram en post med skäl för varje kategori under
grindtröskeln. Fem kategorier står där. Ekonomi och trygghet gör det inte, fast båda har ett tomt
undermått. ADR 0003 punkt 3 och ADR 0008 punkt 6 avgjorde båda att en redovisad storhet inte får
ha en tröskel.

Två vikter i registret stämmer inte. Demokrati står som 25 + 15 + 15, configen säger 20 + 20 + 15.
Försvar står som 20 + 15 + 15, configen säger 20 + 25 + 5. Summorna är rätt, delarna fel.

### 7. Flaggan användaren ser är inte den vi trodde

`web/format.js:19` filtrerar bort `B_coverage_*` ur flaggkolumnen, enligt ADR 0008 punkt 9.
Användaren ser den aldrig. Den flagga användaren ser är `B_thin_coverage`, som ADR 0008 punkt 9
medvetet lät stå kvar.

I demokrati fyrar den för alla åtta, eftersom taket 0,45 ligger under tröskeln 0,50. I trygghet
fyrar den bara för partier som faktiskt tigit. Samma flagga, två skilda orsaker, och användaren ser
bara namnet.

### 8. Det finns två tak, inte ett

ADR 0011 gav Täckning en egen nämnare. Därmed finns ett tak på Täckningens skala och ett på
krympningens. I ekonomi är B-taket 0,550 på den ena och 0,753 på den andra.

Blandas Täckningens tak enligt ADR 0008 punkt 5:s vikter fås `0,30 x 1 + 0,50 x B-tak + 0,20 x
D-tak`. Prövat mot körningen: **sex av sju kategorier har ett parti som ligger exakt på det talet.**
Klimat är den sjunde och avviker med 0,038, vilket är exakt dess kvarvarande utrymme.

### 9. D har fyra strukturella tak, inget under sin tröskel

| kategori | D-tak | B-tak (krympningens skala) |
|---|---|---|
| försvar | **0,750** | 0,500 |
| välfärd | 0,800 | 0,500 |
| trygghet | 0,850 | 0,850 |
| klimat | 0,850 | 0,700 |

D:s tröskel är 0,75 och villkoret är strikt mindre än. Inget av taken ligger under. Försvarets
ligger på **exakt** tröskeln.

### 10. Diffen läser inte täckning

`pipeline/tools/score_diff.py` summerar per cell bara `score` och `flags`. En ändring som rör
enbart täckning passerar tyst.

Svaret på biljettens fråga följer ur punkt 2 och punkt 4. Halva täckningen är varken ett fel i
grinden eller ett fynd om partierna. Den är ett fynd om oss, och krympningen räknar den rätt.

## Beslut

1. **Nivån står.** Biljettens fråga 2 besvaras "nivån ligger rätt". Skälet är inte att nivån är
   bevisat rätt, utan att den inte är det som binder. Diagnosen punkt 5 visar att en sänkt nivå
   köper täckning och aldrig mätning: hela den utlyfta klassen är `supports` rakt igenom och kan
   inte skilja ett enda parti. Att sänka nivån skulle flytta betyg genom att minska krympningen,
   utan att tillföra en enda mätning. Det faller på ADR 0003 punkt 1.

2. **Krympningen står, och vår tystnad räknas kvar i dess nämnare.** B svarar enligt ADR 0002 på
   hur mycket kategorin väntas förbättras. Finns ingen antagen evidens för 55 procent av demokrati
   är 2,5 det ärliga svaret för den delen, och det gäller alla åtta lika. Krympningen räknar
   alltså 45 procent känt plus 55 procent neutralt, vilket är rätt väntevärde under okunskap.

   Skillnaden mot ADR 0011 punkt 9 är avgörande och skrivs ut. Där togs ett **uteslutet** undermått
   ur nämnaren med skälet att vi vägrar poängsätta det. Här vägrar vi ingenting. Vi vet inte.

   Att i stället flytta ut vår tystnad skulle låta demokratibetyget göra ett helt kategorianspråk
   på 45 procent av kategorin. Det är exakt vad `d_coverage_krympning_spec.md` en gång slutade
   göra, och ADR 0008 punkt 4 skrev ned skälet.

3. **Felet ligger i redovisningen.** Ingenting säger att 0,45 är ett tak och inte en egenskap hos
   partiet. Användaren ser Täckning per cell. C visar 45 av 100 i demokrati och 35 av 100 i
   trygghet. Utan taket ser C ut att vara bättre täckt i demokrati. Med taket vänder bilden: i
   demokrati ligger C på taket, i trygghet på 35 av möjliga 85.

   Betyget bär samma osynlighet. Demokratis B kan aldrig bli högre än 3,63, hur bra demokratipolitik
   ett parti än driver. Trygghets B kan nå 4,63.

4. **Taket får namnet Mättak och blir en kanonisk storhet.** Mättak är det högsta tal Täckning kan
   anta i en kategori, blandat enligt ADR 0008 punkt 5:s vikter. Talet står på `categories[]` i
   `scores.json`, ett per kategori och inte 56 kopior av sju tal. Krympningens tak förblir internt
   och namnlöst, eftersom bara flaggan i punkt 7 jämför det mot en tröskel. Två publika namn för
   samma idé vore precis den tvetydighet ADR 0010 punkt 8 och ADR 0011 punkt 11 tog bort.

5. **Ett undermått bär minst en indikator eller ett Uteslutningsskäl.** Det är ADR 0011 punkt 4:s
   form ett steg upp. Regeln i ADR 0011 punkt 2 prövar undermåttet i samma tre steg och i samma
   ordning, och varje uteslutet undermått bär ett återöppningsvillkor. Ett uteslutet undermått ryker
   ur krympningens nämnare och räknas 0 täckt i Täckning, precis som ADR 0011 punkt 9 redan säger.

   Ett undermått vars indikatorer alla är uteslutna bär **inget** eget skäl. Det bär en indikator
   och passerar regeln, och ADR 0011 fäller det ett steg ned. Två skäl för samma fall vore ADR 0011
   punkt 11:s egen varning en gång till. I dag gäller det ekonomis `inflation_prisstabilitet` och
   `offentliga_finanser`.

6. **`industriell_konkurrenskraft` faller på `neutralitetsfel`.** Den väger 15 av klimats 100 och
   har noll indikatorer. Dubbelväggen i `docs/done/evidens_trovardighet.md` §8.7 har en halva i
   varje ände. Dubbelräkningshalvan är ett skäl mot **en kandidatindikator** och inte mot
   undermåttet, och ADR 0011 punkt 2 steg 1 frågar uttryckligen om en annan **delpoäng** äger
   frågan. Klimat mot klimat är inte det. Kvar står att inget neutralt ankare finns, alltså steg 3.

   Återöppningsvillkoret tas ur §8.7 och skärps till uteslutningens nivå: villkoret ska säga vad som
   gör att en **indikator** kan namnges neutralt. Att formulera ett nytt villkor nu vore att kasta
   en diagnos gjord 2026-06-07, alltså innan någon visste vad den här biljetten skulle hitta.

7. **`B_thin_coverage` delas i två flaggor.** Den ena säger att kategorins Mättak ligger under
   tröskeln. Den andra säger att partiet gör det. Skillnaden är maskinellt avgörbar och uppfyller
   ADR 0008 punkt 10. Båda sänker säkerheten ett steg, precis som den gamla gjorde, så bandet står
   still i varje cell.

   **D delas inte.** Diagnosen punkt 9 visar att inget D-tak ligger under D:s tröskel, alltså skulle
   kategoriflaggan ha noll medlemmar. ADR 0011 punkt 1 avvisade en mekanism med noll medlemmar, och
   ADR 0010 punkt 3 sade samma sak om obyggda alternativ. Att kontrollen gjordes skrivs ned, så
   asymmetrin mellan B och D är nedskriven och inte tyst. Försvarets tak ligger på exakt tröskeln,
   och godkännandetestet fäller om något D-tak sjunker under den.

8. **De interna flaggorna `B_coverage_*` och `D_coverage_*` byter namn.** Efter ADR 0011 bär de ett
   tal som inte är Täckning, alltså ljuger ordet. D tas med, eftersom ordet är delat och inte
   räkningen. Att rätta B och låta D bära samma fel vore ADR 0006 punkt 6:s misstag en gång till.

9. **Pipen äger talet, registret äger skälet.** `b_thin_breadth_accepted` slutar bära tak och
   vikter och bär bara orsaken och återöppningstriggern. Pipen räknar Mättaket och
   undermåttsvikterna. Skälet är ADR 0004:s egen byggnot om `confidence_numeric`: två kopior av ett
   tal bör ha en källa och inte två. Diagnosen punkt 6 visar vad den andra kopian redan kostat.

   Registret listar **exakt de kategorier som har minst ett tomt undermått**, och ett test läser det
   villkoret. Tröskeln utgår. Ett fast tal ruttnar tyst den dag en vägg byggs bort, vilket är samma
   fel som tröskeln, bara med en annan konstant.

10. **Spärren gäller åt båda håll.** ADR 0006 punkt 4 låser att verkan skrivs ned innan
    partiraderna slås upp. Hit läggs följdregeln: **"det skulle höja täckningen" får aldrig vara ett
    skäl för att släppa in en post.** Rubriken §8 förbjuder i dag att fylla luckor "för att höja ett
    partis coverage". De nio konsensusmåtten bland de utlyfta höjer alla åttas täckning samtidigt,
    alltså inget enskilt partis, och den formuleringen täcker inte fallet.

11. **Blindheten deklareras.** Under biljetten räknades täckningstal fram, aldrig betyg, band eller
    rangordning. Att beslutet i punkt 5 flyttar klimats B **och** D var känt innan regeln låstes,
    eftersom det följer ur aritmetiken: klimats krympningsnämnare faller från 100 till 85, täckningen
    stiger för alla åtta, och krympningen minskar. Riktningen gick inte att inte veta. Storleken
    räknades inte, och deklarationen finns för att påståendet "jag höll mig objektiv" är oprövbart
    när talen är kända. Samma form som ADR 0005 punkt 8, ADR 0007 punkt 8, ADR 0010 punkt 10 och
    ADR 0011 punkt 12.

12. **Ordningen.** Den här ADR:n ändrar ingen kod och ingen config. Bygget är **en** slice med
    **en** omkörning. Byter flaggan namn utan att pipen räknar Mättaket säger schemat och testerna
    emot varandra, och klimats betyg rör sig två gånger i stället för en. Känsligheten körs om med
    orört frö och orörda spann. Diffen visas innan något publiceras.

    **Diffens storlek avgör bara om vi publicerar nu, aldrig om regeln står.** Ser diffen fel ut är
    det ett byggfel att leta rätt på. En omprövning av punkt 2 kräver en egen biljett som motiverar
    sig utan de talen, enligt ADR 0003 punkt 1.

## Godkännandetest

Tio regler, alla regeltester. Inget tal om täckningens nivå, spridning eller rangordning ingår,
eftersom ADR 0006 punkt 7 och ADR 0011:s godkännandetest punkt 6 förbjuder det.

1. Varje undermått bär minst en indikator eller ett Uteslutningsskäl med återöppningsvillkor.
2. Ett **uteslutet** undermått ligger utanför krympningens nämnare och räknas 0 täckt i Täckning.
3. Mättaket räknas i pipen och står i registret för varje kategori med minst ett tomt undermått,
   utan tröskel.
4. Uppmätt Täckning överstiger aldrig Mättaket i någon cell.
5. Betyg, band och rangordning står still **utom i klimat**.
6. Båda de nya B-flaggorna sänker säkerheten ett steg, så bandet står still i varje cell.
7. Ingen kod och inget test läser de gamla flaggnamnen efter slicen.
8. Inget D-tak ligger under `D_resultat.thin_coverage_threshold`.
9. Ett **tomt men ej uteslutet** undermått ligger kvar i krympningens nämnare. Demokrati bär testet,
   eftersom tre av dess fem undermått är i det läget.
10. Mättaket står på `categories[]`, `categories/items` bär `additionalProperties: false`, och ingen
    cell bär talet.

Regel 9 är den viktigaste. Den låser det beslut biljetten kom för att fatta, och utan den kan en
senare omskrivning flytta 77 procent av krympningen utan att ett enda test faller.

## Övervägda alternativ

- **Sänk grindens nivå så att en postklass släpps in.** Förkastat på beslutspunkt 1. Hela den
  utlyfta klassen är `supports` rakt igenom, nio av 14 med alla åtta partier. En sådan post flyttar
  bara krympningen, alltså är den ett rent separationsreglage förklätt till en evidensfråga.

- **Flytta vår tystnad ur krympningens nämnare, in i Täckning.** Förkastat på beslutspunkt 2, och
  det var den slutsats biljetten och den första analysen båda lutade åt. Räkningen är rätt som den
  står. Alternativet skulle dessutom låta en cell göra ett helt kategorianspråk på en delmängd,
  vilket ADR 0008 punkt 4 redan avvisat en gång.

- **Räkna ett tomt undermått som täckt i stället för 0.** Förkastat. Formen är additiv i stället för
  proportionell och påstår att det tomma undermåttet är **mätt**, vilket är falskt.

- **Ge B ett giltighetsbesked när Mättaket är lågt, som D:s ej tillämplig.** Förkastat på ADR 0009.
  Ett giltighetsfel gäller när delpoängen mäter **fel storhet**. B mäter rätt storhet dåligt, och
  det är osäkerhet. Ett brett band är rätt svar och krympningen är rätt räkning.

- **Dela också D:s tröskelflagga.** Förkastat på beslutspunkt 7. Noll medlemmar i dag.

- **Ett fjärde Uteslutningsskäl för undermåttsnivån.** Förkastat på ADR 0011 punkt 5. Namnen ska
  peka på regeln som fäller, och ingen ny regel fäller här.

- **Lägga Mättaket på cellen, som Täckning.** Förkastat på beslutspunkt 4. Talet är en
  kategorikonstant, och 56 kopior av sju tal är sju tal för mycket.

- **Ingen ändring.** Kartans notes tillåter utgången, och biljettens godkännandetest namngav den.
  Halvt förkastad: nivån står och krympningen står, alltså är utgången "ingen ändring" på de två
  frågor biljetten faktiskt ställde. Redovisningen ändras, eftersom diagnosen punkt 3 och punkt 7
  visar att sajten i dag låter läsaren tro att locket sitter på partiet.

## Vad beslutet inte rör

- **Vikterna 0,30 x A + 0,50 x B + 0,20 x D, C = 0** (ADR 0002).
- **Evidensgrindens symmetri** (ADR 0006). Frågan var nivån, aldrig riktningen.
- **Formen i ADR 0004.** `net = Σ(q·m)/Σq` och talen 0,3/0,6/1,0 står oförändrade.
- **Bandet, säkerhetsnivåerna och `band_only`** (ADR 0009).
- **De 14 utlyfta posterna.** De står kvar utanför med sina källspår och sina återöppningstriggar.
- **Ståndpunktssidan.** Binär stance består.
- **Genomgången av samtliga indikatorer.** Den ligger i
  [#4](https://github.com/mcknschn/rosta/issues/4) och utvidgas **inte** till 35 undermått. Regeln
  har en enda medlem i dag, och slicen tar den. En kommentar i #4 pekar på regeln.
- **Kortets framsida.** Den ligger i [#11](https://github.com/mcknschn/rosta/issues/11).
  Flaggkolumnen i detaljtabellen är inte framsidan, och ADR 0008 punkt 9 ändrade den redan en gång.

## Följder

- **Bygget är en egen slice**, en omkörning. Den rör `config/categories.yaml`,
  `config/coverage_allowlist.yaml`, `pipeline/config.py`, `pipeline/scorerun.py`,
  `pipeline/tools/score_diff.py`, `pipeline/tools/coverage_report.py`, metodrutan och
  `meta.coverage`/`meta.coverage_technical` i pipen, `schemas/scores.schema.json`,
  `web/format.js`, `web/app.js` samt testerna.
- **Klimats B och D rör sig, en gång.** Storleken räknas i slicen och redovisas i dess Följder.
- **Klimats Täckning står exakt still medan klimats betyg rör sig.** Täckningens nämnare är den
  fulla kategorivikten och rörs inte, och täljaren var noll i det uteslutna undermåttet ändå. De
  två talen svarar på skilda frågor, och detta är första gången det syns. ADR 0011 skrev samma sorts
  mening när ekonomis täckning föll utan att betyget rörde sig. Då gick det åt andra hållet.
- **Redovisningen rättas på fyra ställen:** metodrutan i `web/app.js`, `meta.coverage`,
  `meta.coverage_technical` och ordlistan. `meta.coverage` säger i dag "Där underlaget är tunt drar
  vi betyget mot mitten i stället för att gissa" utan att säga vems underlag.
- **Känslighetsanalysen körs om** med orört frö 20260821 och orörda spann. `B_coverage_shrink`
  redovisas som en mätning i slicens Följder. Talet får inte kallas en förbättring, eftersom
  ADR 0003 punkt 1 förbjuder att en ändring försvaras med vad den gjorde med separationen.
- **Publicering sker på uttryckligt klartecken**, efter att diffen visats. Samma ordning som
  [#15](https://github.com/mcknschn/rosta/issues/15).
- **`docs/done/fas4c_rubrik.md` bumpas till version 3.** §8 får en mening om att förbudet gäller
  också när höjningen träffar alla åtta lika. Rubriken är en förregistrering, så ändringen redovisas
  i filen.
- **`docs/done/b_coverage_krympning_spec.md` får en daterad not** om den ändrade nämnaren, samma
  form som ADR 0011 gav ADR 0008 punkt 5.
- **Ordlistan `docs/done/evidens_trovardighet.md` §4.3 får Mättak** som kanoniskt namn bredvid
  Täckning, med `B_coverage` som retirerad synonym.
- **ADR 0006 och ADR 0011 får daterade noter**, skrivna i det här ärendet.
- **Ändrat i det här ärendet:** den här ADR:n samt noterna i ADR 0006 och ADR 0011. Ingen kod, ingen
  config, inget betyg.
