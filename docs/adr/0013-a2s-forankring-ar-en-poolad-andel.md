# ADR 0013: a2:s förankring är en poolad andel, och fönstret faller på spannet

- Status: accepted
- Datum: 2026-08-30
- Beslutad i: biljett [#36](https://github.com/mcknschn/rosta/issues/36) under karta [#6](https://github.com/mcknschn/rosta/issues/6)
- Bygger på: [ADR 0005](0005-a-forankras-i-tid-inte-i-faltet.md), [ADR 0007](0007-a-mats-over-samma-fonster-som-sin-forankring.md), [ADR 0009](0009-sakerheten-mater-hur-val-talet-ar-kant.md), [ADR 0010](0010-ett-reglage-ar-en-vag-pipen-redan-kan-ga.md) och [ADR 0012](0012-vaxelkursen-i-a-ar-harledd-ur-kvotens-andar.md)

## Kontext

Biljett #36 graderades ur [#28](https://github.com/mcknschn/rosta/issues/28) när ADR 0012 förkastade
reserven ur ADR 0007. Reserven gick bara att räkna på a1, och skälet var underlaget: a2:s förankring
saknar år.

Samma underlag hade redan fällt en andra sak. ADR 0010 punkt 6 fällde fönstret som reglage med
skälet att `config/a_forankring.yaml` bär a2:s förankring som ett enda aggregat över 2011-2025. En
dragning av `window.start` skulle ändra a1:s förankring och lämna a2:s orörd, alltså producera en
inkonsekvens i stället för att pröva ett metodval.

Två beslut hade alltså fallit på samma lagringsdetalj. Biljetten frågar om detaljen ska förbli.

Frågan visade sig bära två frågor. Den ena gäller **lagringens kornighet**: står kammarens tal per
år i configen? Den andra gäller **aggregationsformen**: är förankringen medlet av årsandelarna eller
andelen av summan? Diagnosen nedan visar att de går isär, så beslutet svarar på dem var för sig.

## Diagnos

Talen är räknade 2026-08-30 ur `config/a_forankring.yaml`, `config/budget_ramar.yaml`,
`config/mappings.yaml` och `docs/done/a_forankring/fonster.json`, alltså underlaget efter
[#27](https://github.com/mcknschn/rosta/issues/27), [#32](https://github.com/mcknschn/rosta/issues/32)
och [#35](https://github.com/mcknschn/rosta/issues/35).

### 1. Båda halvorna är konsekventa i dag, men på var sin form

Biljetten beskrev asymmetrin som att a1 har år och a2 saknar dem. Koden säger något mer exakt.
Ingen halva är internt inkonsekvent. Varje halva använder **samma form i täljaren och i
förankringen**, och de två halvorna använder olika form.

| halva | täljare | förankring | form |
| --- | --- | --- | --- |
| a1 | `budget.py:164` | `anchor.py:110` | medlet av årsandelarna |
| a2 | `scorerun.py:791-798` | `anchor.py:135` | andelen av summan över åren |

Skillnaden går att säga i en mening. a1 väger varje år lika. a2 väger varje år efter dess egen
motionsvolym.

### 2. Formen rör förankringen nästan inte alls

Kammarens årsvisa tal finns inte lokalt, så förankringen mäts på 8-partipoolen, som spårar
kammarens fördelning inom 0,0008 i varje kategori. Skillnaden mellan de två formerna:

| kategori | andel av summan | medel av årsandelar | skillnad |
| --- | --- | --- | --- |
| välfärd | 0,20931 | 0,21000 | +0,00069 |
| trygghet | 0,08659 | 0,08592 | -0,00067 |
| klimat | 0,09503 | 0,09538 | +0,00035 |
| försvar | 0,06644 | 0,06630 | -0,00014 |
| integration | 0,12137 | 0,12128 | -0,00010 |
| ekonomi | 0,31774 | 0,31766 | -0,00008 |
| demokrati | 0,10351 | 0,10346 | -0,00005 |

Kammarens kategorisammansättning är stabil över åren, så volymviktningen betyder ingenting för
förankringen. Formvalet är på den sidan nära nog verkningslöst.

### 3. Formen rör täljaren mycket mer, och den rör den där den är sämst

Samma formbyte på täljaren flyttar a2 med upp till **0,139 poäng** och byter inbördes ordning mellan
grannar i 4 av 7 kategorier (demokrati, ekonomi, klimat, välfärd). De största utslagen:

| kategori | parti | a2 poolad | a2 medel-av-år | skillnad |
| --- | --- | --- | --- | --- |
| klimat | L | 1,8443 | 1,9833 | +0,1390 |
| försvar | MP | 2,9150 | 2,7849 | -0,1301 |
| demokrati | MP | 2,4443 | 2,5562 | +0,1120 |
| försvar | L | 2,8420 | 2,7385 | -0,1035 |
| integration | L | 2,5361 | 2,4513 | -0,0849 |

De två partier formen flyttar mest, L och MP, är exakt de två med störst volymsvängning över åren
(L 6,5 gånger mellan högsta och lägsta år, MP 4,4). Utslaget är alltså en egenskap hos formen, inte
ett fynd om partierna.

### 4. Motionsvolymen följer regeringsställningen

| parti | lägsta år | högsta år | kvot |
| --- | --- | --- | --- |
| L | 54 (2024) | 350 (2017) | 6,48 |
| MP | 80 (2020) | 355 (2013) | 4,44 |
| M | 548 (2022) | 1854 (2021) | 3,38 |
| SD | 294 (2011) | 876 (2021) | 2,98 |
| C | 177 (2011) | 465 (2021) | 2,63 |
| S | 543 (2018) | 1320 (2013) | 2,43 |
| V | 93 (2018) | 202 (2011) | 2,17 |
| KD | 178 (2023) | 352 (2021) | 1,98 |

Mönstret är inte brus. S skrev 1115-1320 motioner per år i opposition 2011-2013 och 543-853 i
regering. M skrev 766 år 2011 i regering och 1854 år 2021 i opposition. Det stämmer med ADR 0001,
som skriver att a2 läser en restkanal för regeringspartier.

Ett medel av årsandelar ger alltså regeringsåret samma vikt som oppositionsåret, fast
regeringsåret bär fem till sex gånger färre motioner.

### 5. Den tunnaste cellen går från 84 motioner till 1

Poolad bär a2:s tunnaste cell 84 motioner. Det är precis det tal ADR 0009 punkt 5 lutade sig mot när
A behöll `high` i 56 av 56 celler: ingenting i A skattas.

År för år bär den tunnaste cellen **1 motion** (L i försvar, 2024). Tunnaste cellen per år ligger
mellan 1 och 8 motioner i vartenda år i fönstret.

### 6. Lagringen och formen är två skilda saker

Att lagra kammarens tal per år och ändå summera över fönstrets år ger **samma tal av konstruktion**,
eftersom summan av delarna är helheten. Ett sådant bygge tar bort exakt det hinder ADR 0010 punkt 6
namngav, utan att röra formen och utan att flytta ett enda betyg.

Biljetten buntade ihop de två. Buntade måste de svaras ihop, och då drar formens problem med sig
lagringen i fall utan att ha prövats.

### 7. Ett draget fönster kräver årsvisa tal i båda ändar

`party_activity` har `period` i primärnyckeln, så årsrader passar schemat utan schemaändring.
`_require_a2_period` (`scorerun.py:729`) prövar i dag en enda period och skulle behöva pröva en
mängd år. Kostnaden: kammaren per år är 15 utskott gånger 15 år, alltså 225 anrop. Partitäljaren per
år är 120 anrop per år, och de är redan körda en gång, eftersom `fonster.json` bär dem för 2008-2025.

### 8. ADR 0005 punkt 7 låser redan fönstrets början

Punkten säger att fönstret börjar vid den senare av de två gränserna och slutar vid senaste färdiga
år. Den förbjuder uttryckligen efterhandsomdömen av typen "kvalitén var för dålig före år X", med
skälet att ingen kan pröva dem och att de går att fatta med kännedom om effekten.

Ett reglage för fönstret kräver ett spann för `start`. ADR 0010 punkt 5 kräver att **båda** ändarna
är härledda. Nedre änden finns: 2011, ur gränserna. Övre änden finns inte. Varje kandidat (2015,
2018, 2022) är exakt det omdöme ADR 0005 punkt 7 redan förbjudit.

### 9. Den enda kandidat som ser härledd ut går mot stupet

"Fönstret är senaste mandatperiod" vore testbart och skrivet i förväg, alltså inget efterhandsomdöme.
Villkorsklausulen (ADR 0007 punkt 4) körd för varje möjlig fönsterstart:

| start | antal budgetår | klausulen |
| --- | --- | --- |
| 2011 till 2022 | 15 till 4 | håller |
| 2023 | 3 | **faller: KD, L, M, SD** |

Ett fyraårsfönster lägger förankringen på en enda regerings ramar. Det är ADR 0005 punkt 5:s
förkastade "regeringens ram som nollpunkt" via bakvägen, och det är precis det klausulen skrevs för
att stoppa. Klausulen fyrar ett år efter kandidaten, inte tio.

### 10. a2:s gräns prövas på en annan nivå än den betyget använder

a1 prövar sitt aktivitetstest i **varje** budgetår och skär snittet (`budget.py:158`). a2 prövar sitt
test bara i gränsåret.

På utskottsnivå faller a2:s test i 8 av de 15 åren (2013, 2015, 2019, 2020, 2022, 2023 och 2024, med
en eller två nollceller vardera). På **kategorinivå**, som är den nivå betyget räknar på, finns noll
nollceller i något år, och testet håller från 2010. SD är skälet: partiet kom in i riksdagen 2010,
och 2008-2009 saknar SD motioner i varje kategori.

Gränsen 2011 är alltså ett år konservativ. Nivåskillnaden är verklig men effekten är nära noll
(fynd 2), och a1 kan ändå inte gå till 2010, eftersom `a1_frames_bound` är 2011.

## Beslut

1. **a2:s förankring förblir en poolad andel.** Andelen av kammarens samtliga motioner i fönstret,
   alltså varje år vägt efter sitt eget underlag. Skälet är inte tröghet. Formen mäter partiets
   faktiska motionsandel i fönstret, och att väga varje år efter dess eget underlag är estimatorns
   rätta beteende. Symmetri i **form** med a1 är inte samma sak som symmetri i **frågan**: a1 har ett
   tal per år och inget naturligt antal att poola, medan a2 har ett antal. Att poola kronor över år
   skulle väga senare år tyngre, eftersom budgeten växer. a1:s medelform är därför en följd av dess
   underlag, inte ett val a2 ska härma.

2. **Täljaren följer förankringen, alltså poolad i båda ändar.** ADR 0007 punkt 1 kräver att täljare
   och förankring täcker samma år. Punkten skärps här: de ska också ha **samma form**. En kvot vars
   ändar väger åren olika bär viktskillnaden som om den vore en skillnad mellan partier, vilket är
   samma fel punkt 1 redan förbjuder i tid.

3. **Lagringen förblir ett aggregat. Kostnaden skrivs ned.** Med punkt 5 nedan köper årsvis lagring
   ingenting som överlever, så bygget faller på att det inte har någon konsument. Kostnaden den dag
   frågan blir skarp: 225 anrop för kammaren och 1800 för partihalvan, båda körda en gång tidigare.
   Det som skulle låsa upp frågan är en biljett som river ADR 0005 punkt 7:s fönsterregel.

4. **Formvalet får ett lås.** Ett kodtest ska hålla a2:s förankring vid den poolade andelen och
   skilja den från medlet av årsandelarna på en fixtur där årsvolymen varierar. Testet faller åt
   båda hållen, precis som `test_a1_forankring_ar_medel_over_fonstrets_ar` redan gör för a1. Utan
   låset är punkt 1 oskyddad, eftersom ingenting i dag hindrar ett formbyte.

5. **Fönstret är inget reglage, och skälet är ett annat än ADR 0010 punkt 6:s.** Det faller på
   **spannet**, inte på underlaget: spannets övre ände har ingen härledning (fynd 8), och den enda
   kandidat som ser härledd ut leder rakt mot villkorsklausulen (fynd 9). Skälet står oavsett hur
   talen lagras.

   ADR 0010 punkt 6:s skäl var sant men ytligt. Det hängde på ett lagringsval vem som helst kan bygga
   bort för 225 anrop, och då hade punkten fallit utan att något metodmässigt hade ändrats. Punkten
   skrivs om till en not om att den var det svagare av två skäl. Reglagelistan står orörd.

6. **A behåller `high`, och villkoret skrivs ut.** ADR 0012 punkt 7 lämnade öppet om ett partis egen
   årsvariation i a2-emfas rör ADR 0009:s beslut. Svaret är nej. Med poolad form mäter a2
   femtonårsandelen, och den är räknad och fullständig. Årsvariationen är en egenskap hos världen,
   inte en osäkerhet i talet, alltså samma artskillnad ADR 0009 gjorde när den förkastade `|q|`.

   Villkoret: svaret hänger på formen. Den som en gång byter till medel av årsandelar måste pröva
   `high` på nytt, eftersom tunnaste cellen då bär 1 motion i stället för 84 (fynd 5). Då skattas
   något i A, och ADR 0009:s fynd faller.

7. **a2:s gräns står kvar vid 2011.** Fynd 10 är verkligt men rör ingenting: effekten är mätt till
   nära noll, och a1 kan inte gå till 2010. Att öppna gränsen hör till ADR 0007, inte hit. Fyndet
   står nedskrivet så att frågan går att hitta om ADR 0007 ändå öppnas.

8. **Orden.** **Poolad andel** och **Årsmedel** införs i ordlistan §4.3. Biljetten uppstod ur att
   asymmetrin saknade namn: ADR 0010 punkt 6 kunde bara säga "ett aggregat utan år", vilket beskriver
   lagringen och inte formen, och därför pekade skälet på fel sak.

9. **Blindheten deklareras.** Den som beslutade hade sett vad formbytet gör med a2 per parti och
   kategori, inklusive att det byter inbördes ordning mellan grannar i 4 av 7 kategorier (fynd 3).
   Talen räknades fram för att pröva om formvalet betyder något, eftersom biljetten inte gick att
   avgöra utan det. Beslutet är härlett ur vad storheten mäter och ur volymens koppling till
   regeringsställningen (fynd 4), inte ur vilka partier ordningsbytena gynnar. Talen om totalbetyg
   och totalranking räknades aldrig.

## Godkännandetest

Ett regeltest, aldrig ett tal om spridning eller rangordning. ADR 0003 punkt 1 förbjuder ökad
separation som mål, och det här beslutet ändrar ingenting i talen.

1. **Nytt lås:** a2:s förankring är andelen av summan, och den skiljer sig från medlet av
   årsandelarna på en fixtur där årsvolymen varierar mellan åren. Faller åt båda hållen.
2. **Befintligt lås står kvar:** `test_alla_kallor_i_adr_0003_punkt_5_dras` håller reglagelistan mot
   en exakt mängd, så ett insmuget fönsterreglage faller rött.
3. **Befintligt lås står kvar:** `test_a1_forankring_ar_medel_over_fonstrets_ar` låser a1:s form.
4. **Betyg, band och ranking står exakt still.** Beslutet rör ingen kod som räknar tal.
5. **Inget tal om spridning eller rangordning ingår i testet.**

## Övervägda alternativ

- **Medel av årsandelar i båda halvorna, för symmetri med a1.** Förkastat på punkt 1. Symmetrin är
  formens, inte frågans. Formen rör dessutom förankringen med högst 0,00069 (fynd 2) men täljaren med
  upp till 0,139 poäng (fynd 3), och den rör den där underlaget är tunnast: utslaget är störst för de
  två partier vars motionsvolym svänger mest.

- **Årsvis lagring med bibehållen poolad form.** Verkligt övervägt, och det enda alternativ som är
  rankingneutralt av konstruktion (fynd 6). Förkastat på punkt 3 och 5: med fönstret fällt på
  spannet har bygget ingen konsument, och kod utan konsument står oanvänd tills någon river ADR 0005
  punkt 7. Kostnaden är nedskriven så att bygget går att beställa den dagen.

- **Fönstret som reglage med spannet start i [2011, 2022].** Förkastat på punkt 5. Övre änden 2022 är
  en vald konstant, och ADR 0010 punkt 5 kräver två härledda ändar. Att spannet råkar hålla
  villkorsklausulen till och med 2022 gör inte 2022 härlett.

- **Fönstret som senaste mandatperiod.** Förkastat på fynd 9. Regeln vore testbar och skriven i
  förväg, men den lägger förankringen på en enda regerings ramar, och villkorsklausulen faller ett år
  senare.

- **a2:s gräns flyttad till 2010, prövad på kategorinivå.** Förkastat på punkt 7. Effekten är nära
  noll och a1 kan inte följa med.

## Vad beslutet inte rör

- Avbildningen `net_support_to_score`, den begränsade kvoten och växelkursen (ADR 0005 punkt 4, ADR
  0012 punkt 2). Låsta.
- Blandningen 0,6 x a1 + 0,4 x a2. Egen biljett, [#33](https://github.com/mcknschn/rosta/issues/33).
- Reserven ur ADR 0007. Förkastad av ADR 0012 punkt 3, och prövas inte om här.
- Fönstrets ändar 2011 och 2025. Satta av ADR 0005 punkt 7 och ADR 0007 punkt 2.
- Reglagelistan i `robustness.SOURCES`. Oförändrad, se punkt 5.

## Följder

- Ingen kod- eller configändring i räknande kod. Ranking oförändrad.
- Bygget bär två poster: det nya låset ur punkt 4, och kommentaren i `robustness.py` som i dag anger
  ADR 0010 punkt 6:s skäl för att fönstret inte är ett reglage.
- ADR 0010 punkt 6 får en not ur punkt 5. ADR 0012 punkt 7 får en not ur punkt 6.
- Ordlistan §4.3 får **Poolad andel** och **Årsmedel** ur punkt 8.
