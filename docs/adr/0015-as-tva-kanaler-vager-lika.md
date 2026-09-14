# ADR 0015: A:s två kanaler väger lika

- Status: accepted
- Datum: 2026-09-13
- Beslutad i: biljett [#33](https://github.com/mcknschn/rosta/issues/33) under karta [#6](https://github.com/mcknschn/rosta/issues/6)
- Bygger på: [ADR 0001](0001-a-mater-prioritering.md), [ADR 0002](0002-kategoripoangens-ansprak-och-vikter.md), [ADR 0003](0003-skiljbarhet-och-kanslighetsanalys.md), [ADR 0005](0005-a-forankras-i-tid-inte-i-faltet.md), [ADR 0007](0007-a-mats-over-samma-fonster-som-sin-forankring.md), [ADR 0009](0009-sakerheten-mater-hur-val-talet-ar-kant.md), [ADR 0010](0010-ett-reglage-ar-en-vag-pipen-redan-kan-ga.md) och [ADR 0012](0012-vaxelkursen-i-a-ar-harledd-ur-kvotens-andar.md)

## Kontext

Delpoäng A mäter prioritering. Den mäts i två kanaler. `a1` är andelen av partiets föreslagna
utgiftsramar. `a2` är andelen av partiets egna motioner. Blandningen `a1 = 0,6` kom in i repots
första commit (`0945a62`) och har aldrig rörts.

ADR 0005 punkt 4 lät blandningen stå. ADR 0007 listade den under "Vad beslutet inte rör".
ADR 0010 gjorde den till ett reglage och graderade härledningsfrågan till den här biljetten.
Ingen av dem härledde talet.

A väger 0,30 och blandningen biter i 56 av 56 celler. Frågan är alltså rankingrelevant. Kartans
regel gäller därför fullt ut: motivera och lås en vikt först, kör om pipen sedan.

## Diagnos

Mätt 2026-09-13 mot `config/`, `pipeline/`, `dist/` och `docs/done/a_forankring/fonster.json`.

### 1. Biljetten beskrev fel tal

Biljetten skrev att 0,6 påstår att en andelsenhet föreslagen ram är värd 1,5 motionsandelar.
Koden viktar inte andelar. Den viktar två poäng som redan är avbildade
(`pipeline/scorerun.py:958`). Båda kanalerna mäts mot sin egen förankring med samma avbildning,
alltså `q = (andel - förankring) / (andel + förankring)` följt av `net_support_to_score`.

Det 0,6 säger är något annat och något smalare. En lika stor relativ avvikelse från kanalens eget
normalläge räknas 1,5 gånger i budgetkanalen. Förankringen är just det som gör kanalerna
jämförbara, så biljettens invändning om kronor och dokument faller.

### 2. Kanalerna är substituerbara, alltså mäter de samma storhet

Faller `a1` ur sin grind bär `a2` hela A ensam (`pipeline/scorerun.py:962`). Modellen byter alltså
redan i dag ut den ena kanalen mot den andra utan att räkna om skalan. Det går bara om de mäter
samma storhet. Beslutet är låst sedan Fas 1b och prövas inte om här.

### 3. ADR 0001:s skäl bär en riktning men ingen magnitud

Skälet står i konsekvenserna till ADR 0001. `a2` läser en restkanal för regeringspartier, alltså
väger `a1` mer. Biljetten fann tre hål i skälet. Hål 1 var att skälet aldrig mätts, eftersom
lagret bar motionerna som ett enda aggregat.

Hålet är stängt. `docs/done/a_forankring/fonster.json` bär motioner per parti, utskott och
kalenderår för 2008-2025. Filen hämtades när fönstrets gränser prövades i #27.

### 4. Restkanalen finns i volymen, och volymen mäter A inte

| parti | volymkvot opposition/regering | fördelningsskifte (TVD) | skifte utan epokeffekt |
|---|---|---|---|
| S | 1,63 | 0,027 | 0,060 |
| M | 1,57 | 0,066 | 0,082 |
| C | 1,82 | 0,047 | 0,106 |
| KD | 0,99 | 0,092 | 0,146 |
| L | 1,37 | 0,065 | 0,164 |
| MP | 1,90 | 0,079 | 0,193 |

Fem av sex partier skriver färre motioner i regeringsställning. KD gör det inte. Men `a2` mäter
andel och inte volym, vilket `config/scoring.yaml` skriver ut. Volymfallet är alltså redan
neutraliserat av konstruktionen.

SD och V går inte att pröva. De har suttit i opposition i hela fönstret.

### 5. Fördelningsskiftet är litet, och det pekar inte åt samma håll

Regeringsåren och oppositionsåren ligger i olika epoker. M regerade 2011-2014 och 2023-2025 men
satt i opposition 2015-2022. Trygghetsfrågan växte för alla efter 2015. Rollen och epoken måste
därför skiljas åt.

Med epoken bortrensad har bara två av sju kategorier samstämmigt tecken över de sex prövbara
partierna. Demokrati är positiv i 6 av 6 med medel +0,009. Trygghet är positiv i 1 av 6 med medel
-0,018. De övriga fem delar sig.

Rollskiftet är dessutom litet mot det som skiljer partierna åt. Kvoten går från 0,07 i klimat till
0,39 i välfärd.

### 6. `a1` kan inte fylla luckan, eftersom den delar ram

Varje parti ligger på en delad ram i 3 till 9 av 15 år: L 9, S 8, MP 8, M 7, KD 7, C 6, V 5, SD 3.
Något enskilt år finns bara 3 till 7 distinkta ramar bland åtta partier.

> **Daterad not 2026-09-13, skriven i biljett [#44](https://github.com/mcknschn/rosta/issues/44)
> under [ADR 0017](0017-a1-laser-forfattarskap-inte-uppslutning.md).** Vektorn ovan är antalet år
> partiet står på ramen `regeringen`, inte antalet år det delar ram. Rätt vektor är
> **L 10, MP 9, S 9, KD 8, M 8, C 7, V 6, SD 3**, alltså spannet 3 till 10. Skillnaden är sju
> parti-år på gemensam oppositionsmotion: ramen `S_MP_V` 2011 och ramen `M_C_L_KD` 2015.
> Slutsatsen i avsnittet överlever, eftersom delningen är STÖRRE än den sade. Efter ADR 0017
> räknas talet dessutom på partiets giltiga år, och metodrutan bär båda kolumnerna.

Därför är `a1`:s partispann 1,02 till 1,30, medan `a2`:s är 1,35 till 2,95. Ett regeringsparti får
regeringens ram, delad med koalitionspartner och stödparti. De två kanalerna tunnas alltså ut i
samma år, för samma partier, av samma orsak. Skälet i ADR 0001 förutsatte att de tunnas ut
komplementärt.

### 7. Förankringarna skiljer sig kraftigt, och det är avsiktligt

Välfärd är 42,6 procent av de beslutade ramarna men 21,0 procent av kammarens motioner. Demokrati
är 4,8 mot 10,3. Ekonomi är 25,4 mot 31,9.

Kanalerna säger alltså olika saker om var kraften ligger. Det är precis vad förankringen tar bort.
Efter förankringen mäter båda samma sak: hur mycket mer än kanalens normalläge partiet lägger på
kategorin.

### 8. Reglagets nedre ände vilar på det fällda skälet, och den ligger publicerad

`A_component_mix` har spannet `a1` i (0,50, 0,80]. Den nedre änden kommer ur ADR 0001:s påstående
att `a1` väger mer (`pipeline/robustness.py:166`). ADR 0010 punkt 5 kräver två härledda ändar.

Meningen "Nedre änden ur ADR 0001, som härleder att a1 väger mer än a2" ligger ordagrant i
`dist/robustness.json` och i `web/data/robustness.json`. Den är alltså publicerad.

### 9. A:s nåbara tak flyttar lite

Taket per kategori följer förankringarnas storlek och blandningen (`pipeline/scorerun.py:474`).
Vid jämn blandning går det från 3,757-4,702 till 3,820-4,686, alltså -0,029 till +0,063 per
kategori. Spannet mellan kategorierna krymper något. Taket är en egenskap hos förankringarna och
säger ingenting om något parti.

## Beslut

1. **Blandningen blir 0,5 x a1 + 0,5 x a2.** Talet är härlett och inte valt. Kedjan är:
   kanalerna mäter en storhet (punkt 2); båda mäts mot sin egen förankring med samma avbildning,
   så en poäng betyder samma sak i båda (punkt 1); det enda nedskrivna skälet till asymmetrin
   faller (punkt 3 till 6); och inget tillåtet skäl återstår (beslutspunkt 3). Då är 1:1 det enda
   tal som inte inför en konstant utöver vad storheten kräver. Formen är densamma som
   ADR 0012 använde när den härledde avbildningen.

2. **ADR 0001:s skäl är fällt som härledning.** Restkanalen finns i volymen, och `a2` mäter inte
   volym. I fördelningen är effekten liten och osystematisk. `a1` kan inte fylla luckan.
   Skälet står kvar i ADR 0001 som historik och får en daterad not.

3. **En vikt är inte instrumentet för tvivel.** ADR 0009 låste att osäkerhet bärs av Säkerheten
   och att ett giltighetsfel möts med uteslutning. Att väga ned en kanal för att den är brusig
   uttrycker samma osäkerhet två gånger, en gång i bandet och en gång i betyget. Det är samma
   dubbelräkning som ADR 0008 avvisade när Täckningen fick noll verkan på betyget. Regeln gäller
   åt båda håll och binder också beslutspunkt 7.

4. **Kanal blir kanoniskt ord.** En Kanal är en av de två vägar delpoäng A mäter prioritering
   genom, var och en mätt mot sin egen förankring. Ordet förs in i ordlistan i
   `docs/done/evidens_trovardighet.md` § 4.3. Utan ordet måste texten säga "halva" om något som
   mäter hela storheten.

5. **Reglagets spann härleds om.** Spannet blir R1 på det beslutade värdet, alltså `a1` i
   [0,25, 0,75]. ADR 0010 punkt 5 noterade att R1 inte kunde tillämpas på `a1` direkt, eftersom
   R1 på 0,6 ger ett spann som bryter R1 för 0,4. Vid jämn blandning upphör den invändningen av
   sig själv. Det är en följd av beslutet och aldrig ett skäl för det. Att välja ett betygstal för
   att analysen blir prydligare är den koppling ADR 0010 förkastade.

6. **A:s täckning i grindfallet blir 50.** Talet ärver blandningen ur configen och ändras därför
   av sig självt. ADR 0008 punkt 3 låser det normativt till 40 och får en daterad not. Ändringen
   är vilande, eftersom `a1` står i alla 56 celler i dag.

7. **Ramdelningen är en utskriven kostnad, inte en vikt.** Fyndet i diagnosens punkt 6 möts inte
   med en sänkt vikt för `a1`, av skälet i beslutspunkt 3. ADR 0007 punkt 4:s villkorsklausul
   prövar bara ytterfallet, alltså delad ram i varje år, och den fyrar inte. Frågan om `a1` hör
   hemma i delade år graderas som egen biljett.

8. **Blindheten deklareras i tre nivåer.** Mätt och tillåtet: restkanalsprovet och ramdelningen,
   båda egenskaper hos instrumentet och båda beordrade av biljetten. Känt sedan tidigare och
   otillåtet som skäl: att `a2` bär den större delen av A:s separation, och att `A_component_mix`
   ligger på 0,68 kategoripoäng, alltså under brusgolvet 1,0. Aldrig räknat: kategoribetyg, band
   och rangordning under något alternativ. Talen räknas först när regeln är låst och nedskriven.

## Godkännandetest

Sju regler, alla regeltester. Ingen regel nämner ett betyg, ett band eller en rangordning.

1. Configen bär 0,5 och 0,5.
2. Ett mutationstest prövar minst **två** viktpar och kräver att A följer värdena.
3. Mutationstestet kör **båda** grindlägena, alltså både aktiv `a1` och `A_a2_only`.
4. Mutationstestet läser configen på produktionens väg, eftersom `config.scoring()` är cachad.
5. Täckningen i grindfallet följer blandningen i samma mutationstest.
6. Reglagets spann är R1 på det beslutade värdet.
7. Inget test hävdar en ordning mellan kanalerna.

Regel 2 till 4 hör ihop och är de viktigaste. Ett enda mutationsvärde räcker inte: en hårdkodad
fallback på 0,75 passerar mutationen 0,25/0,75 men är fel vid standardvärdet. En fixtur som bara
kör med aktiv grind missar vägen där A blir `a2` och täckningen sätts ur `w_a2`. Repot har blivit
bitet av just den klassen av fel förut, i #37, där båda sidor av ett prov kom ur samma config.

Regel 7 är det gamla testet vänt rätt. `tests/test_robustness.py:235` hävdar i dag att `a1` väger
mer. Efter slicen ska inget test påstå en ordning alls.

## Övervägda alternativ

- **Låta 0,6 stå som ett deklarerat, oderiverat val.** Förkastat. Beslutspunkt 1 ger en
  härledning, så valet behöver inte längre deklareras som obeslutat. Att behålla 0,6 **för att**
  vi vet vad en ändring skulle göra med separationen är dessutom samma överträdelse av
  ADR 0003 punkt 1 som att ändra för samma skäl, bara spegelvänd.

- **Vikta kanalerna efter precision.** Förkastat på beslutspunkt 3. Kanalerna mäter samma storhet,
  så inversvarians vore den vanliga formen. Men precision är tvivel, och tvivel bärs av Säkerheten
  i den här modellen.

- **Låta blandningen variera per kategori.** Förkastat. Välfärd drivs mest genom pengar och
  demokrati mest genom lag, vilket diagnosens punkt 7 visar. Att bygga in det kräver sju valda
  konstanter, alltså samma skäl som ADR 0012 punkt 7 använde när den vägrade jämna ut A:s tak.
  Det låter också A läsa kategorins institutionella form i stället för partiets prioritering,
  alltså ADR 0001:s invändning mot en rollberoende blandning ett steg upp. Förankringen gör
  dessutom redan jobbet.

- **Väga ned `a1` för att den delar ram.** Förkastat på beslutspunkt 3 och 7. Att en kanal mäter
  fel storhet för ett parti är ett giltighetsfel enligt ADR 0009, och giltighetsfel möts med
  uteslutning eller med att skrivas ut.

- **Ompröva ADR 0001:s förkastande av en rollberoende blandning.** Inte prövat här. ADR 0001
  förkastade den med skälet att A då skulle läsa partiets roll, och rollen är C:s fråga. Det
  förkastandet står kvar.

## Vad beslutet inte rör

- **Vikterna 0,30 x A + 0,50 x B + 0,20 x D, C = 0** (ADR 0002).
- **A:s form, avbildning och växelkurs** (ADR 0005 och ADR 0012). En fördubblad andel ger
  fortfarande 0,83 poäng i den kanal som mäts.
- **Fönstret 2011-2025 och båda förankringarna** (ADR 0007 och ADR 0013).
- **`a1`:s grind** (`pipeline/budget.py`). Villkoret för när `a1` vägs in är orört.
- **ADR 0007 punkt 4:s villkorsklausul.** Den prövar delad ram i varje år och fyrar inte.
- **Att `a2` mäter andel och inte volym.** Diagnosens punkt 4 vilar på det, och det är låst sedan
  Fas 1a.

## Följder

- **Bygget är en egen slice**, en omkörning som flyttar 56 av 56 celler. Den rör
  `config/scoring.yaml`, `pipeline/robustness.py`, `tests/test_robustness.py`,
  `tests/test_a_taket.py`, metodrutan i `web/app.js`, `DATA.md` rad 175, 292 och 362,
  `README.md` rad 85, `docs/BACKLOG.md` rad 263, `docs/done/a_forankring_metod.md` rad 19,
  `docs/done/fas1b_budget_metod.md` rad 4, `docs/done/ROADMAP.md` rad 75 och
  `docs/done/expertgranskning/README.md` rad 23.
- **Daterade noter läggs i ADR 0001, ADR 0008 punkt 3 och ADR 0010 punkt 5.** Ingen ADR skrivs om.
  `docs/done/expertgranskning/A_budgetramar_verifiering_2011_2022.md` får också en daterad not, av
  samma skäl: den är en signerad granskning av ett läge som gällde då.
- **Känslighetsanalysen körs om** med orört frö 20260821. `A_component_mix` får sitt nya spann.
  Omkörningen krävs, eftersom artefakten bär det fällda skälet i klartext och ligger publicerad.
  Den är 10 000 dragningar och startar på uttryckligt klartecken.
- **Metodrutan får en mening.** Budgeten och motionerna väger lika, eftersom båda mäts mot sitt
  eget normalläge och ingen skillnad mellan dem ger ett sakligt skäl att väga den ena högre.
  Meningen säger inte att kanalerna är lika. Den säger att ingen skillnad mellan dem bär en vikt.
- **A:s nåbara tak per kategori skrivs redan ut av koden** och följer med av sig självt.
- **Ordningen efter omkörningen är låst i sex steg.** Kör om. Validera och kör hela
  godkännandetestet. Diffgranska mot `dist/scores.snapshot.json`. Visa diffen. Skriv ny snapshot
  med `--write`. Synka och committa allt tillsammans. Testerna går före diffen, annars godkänns en
  diff från ett ogiltigt bygge.
- **Resultatet publiceras som det blir**, även om rangordningen byter plats. ADR 0003 punkt 1
  förbjuder att en ändring försvaras med vad den gjorde med separationen. Samma regel förbjuder
  att den dras tillbaka av samma skäl. Godkännandet gäller att regeln följts.
- **En biljett graderas** om `a1` hör hemma i år där partiet delar ram med andra.
