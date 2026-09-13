# ADR 0017: a1 läser författarskap, inte uppslutning

- Status: accepted
- Datum: 2026-09-13
- Beslutad i: biljett [#44](https://github.com/mcknschn/rosta/issues/44) under karta [#6](https://github.com/mcknschn/rosta/issues/6)
- Bygger på: [ADR 0001](0001-a-mater-prioritering.md), [ADR 0003](0003-skiljbarhet-och-kanslighetsanalys.md), [ADR 0005](0005-a-forankras-i-tid-inte-i-faltet.md), [ADR 0007](0007-a-mats-over-samma-fonster-som-sin-forankring.md), [ADR 0008](0008-cellens-tackning.md), [ADR 0009](0009-sakerheten-mater-hur-val-talet-ar-kant.md), [ADR 0011](0011-uteslutningen-ar-ett-eget-besked.md), [ADR 0014](0014-mattaket-ar-modellens-inte-partiets.md) och [ADR 0015](0015-as-tva-kanaler-vager-lika.md)

## Kontext

`a1` mäter andelen av partiets föreslagna utgiftsramar. Många år föreslår partiet ingen egen ram.
Det ställer sig bakom någon annans. Frågan är om `a1` mäter partiets prioritering de åren.

Biljetten graderades ur [#33](https://github.com/mcknschn/rosta/issues/33) när ADR 0015 punkt 7 lade
fyndet utanför sitt eget beslut. Tre gränser följde med: blandningen är låst till 0,5 / 0,5
(ADR 0015 punkt 1), svaret får inte bli en sänkt vikt för `a1` (ADR 0015 punkt 3), och talen om A:s
separation är kända och får inte styra svaret (ADR 0003 punkt 1). "Ingen ändring" var en godkänd
utgång.

## Diagnos

Mätt 2026-09-13 mot `config/budget_ramar.yaml`, `config/a_forankring.yaml` och `pipeline/`.

### 1. Biljettens tabell räknar fel sak

Biljetten och ADR 0015 rad 83 bär vektorn L 9, S 8, MP 8, M 7, KD 7, C 6, V 5, SD 3 och spannet 3
till 9. De talen är antalet år partiet står på ramen **`regeringen`**. Antalet år partiet delar ram
med minst ett annat parti är ett annat tal, och `budget.shared_frame_years()` producerar det redan:
**L 10, MP 9, S 9, KD 8, M 8, C 7, V 6, SD 3**, alltså spannet 3 till 10.

Skillnaden är sju parti-år på gemensam oppositionsmotion: ramen `S_MP_V` 2011 och ramen `M_C_L_KD`
2015. Slutsatsen i ADR 0015 överlever, eftersom delningen är större än den sade.

### 2. Delad ram är tre företeelser, inte en

`basis` i `config/budget_ramar.yaml` bär tre värden, och de fördelar sig på 120 parti-år så här:

| `basis` | parti-år | vad källan belägger |
|---|---|---|
| `egen_ram` | 67 | partiet skrev och undertecknade ramen; 7 av dem är gemensam motion |
| `regeringsstallning` | 41 | koalitionen skrev ramen, och partiet är en av författarna |
| `votering` | 12 | partiet röstade ja i voteringen om rambeslutet |

De tolv är V 2015 till 2019, C och L 2020 till 2021, samt SD 2023 till 2025.

### 3. Bara den tredje bär ett giltighetsfel

ADR 0011 punkt 2 steg 2 frågar om utfallet kan tillskrivas ett parti. För `votering` är svaret nej.
Det partiet sade var ja till en ram. Det `a1` läser ur beskedet är en fördelning över 27
utgiftsområden. Ingenting i källan bär den fördelningen. Talet är härlett ur ett binärt ja.

För de två andra håller tillskrivningen. En gemensam motion är undertecknad av varje parti den
namnger. En regeringsram är skriven av den koalition som lägger fram den. Båda är författarskap, och
författarskap är ett besked om prioritering. Uppslutning bakom en summa är det inte.

### 4. Regeln kan inte gå på rollen, och fälten går i dag inte att skilja åt

De tre fälten `role`, `basis` och källraden delar i dag **exakt** samma 120 parti-år:

| `role` | `basis` | parti-år |
|---|---|---|
| `government` | `regeringsstallning` | 41 |
| `opposition` | `egen_ram` | 67 |
| `support` | `votering` | 12 |

En regel skriven på `basis` väljer alltså samma tolv rader som en regel skriven på `role`, och
skillnaden mellan dem syns inte i data. Men "partiet regerade" är C:s fråga (ADR 0001), och `basis`
är en redaktionell klassificering. Regeln måste därför vila på vad `note` citerar, och bygget måste
pröva `basis` mot källraden och aldrig mot rollen. Det är inte en formalitet: den dag ett stödparti
lägger en egen ram skiljer sig fälten åt, och då avgör provet vilket av dem som hade rätt.

### 5. ADR 0009 punkt 4 namngav redan ett giltighetsfel i `a1`, och det är ett annat

ADR 0009 punkt 4 skrev att `a1` för KD, L, M och SD är den antagna ramen, kallade det ett
giltighetsfel och lämnade frågan till ADR 0007 punkt 4:s villkorsklausul. De två felen ser lika ut i
data och är olika frågor:

- **ADR 0009:s fel.** Partiets ram **är** förankringen, alltså blir kvoten noll av konstruktion.
  Felet sitter i nollpunkten, det biter oavsett vem som skrev ramen, och klausulen äger det.
- **Det här felet.** Ingen källa tillskriver partiet fördelningen. Felet sitter i attributionen, det
  biter oavsett om ramen råkar bli antagen, och ADR 0011 punkt 2 steg 2 äger det.

De överlappar: **10 av de 12** uteslutna parti-åren är år där partiets ram också är den antagna. De
två återstående är V 2015 och V 2019, alltså år där den antagna ramen var oppositionens. Överlappet
är stort, men det gör inte frågorna till en.

Över hela fönstret är partiets ram den antagna i **45 av 120** parti-år. Efter uteslutningen är den
det i 35 av 108.

### 6. Att stryka de tolv posterna rakt av dödar `a1` helt, och tyst

`_year_active_categories` i `pipeline/budget.py:89-90` börjar med

    if not all(p in frames for p in parties):
        return set()

och `a1_shares` skär sedan årens mängder mot varandra på rad 158. Tas de tolv posterna bort går
`active` från 7 kategorier till 0. Mätt. Grinden är alltså inte bara hård mot en saknad cell, som
docstringen lovar. Den är hård mot ett saknat **parti**, och då säger den ingenting alls.

`a1_shares` har dessutom ett tyst medel på rad 160-165. Den räknar per parti över de år partiet
råkar finnas i, men returnerar **en** årslista för alla åtta. En avvikelse per parti passerar därför
utan att någon ser den.

### 7. Inget kort fönster räddar `a1`

Åren utan någon voteringspost är 2011, 2012, 2013, 2014 och 2022. Det enda sammanhängande intervall
som är längre än ett år är 2011 till 2014, och där fäller villkorsklausulen M, C, KD och L.

De fem åren tillsammans klarar klausulen. Men de är inte ett fönster. ADR 0007 punkt 2 lade fönstrets
början vid den senaste av tre gränser som skrevs före hämtningen. En handplockad årsmängd med ett hål
i mitten är precis den valda konstant ADR 0005 och ADR 0007 båda vägrade välja.

### 8. Villkorsklausulens vila är inte robust

Klausulen fäller ett parti vars ram är den antagna i **varje** år. Två saker bär vilan: att
regeringsmakten skiftar, och att den antagna ramen i tre år **inte** är regeringens. De tre är 2015
(reservationen), 2019 (reservation 5) och 2022 (utskottets eget förslag i bilaga 4). Ingen ADR har
noterat det.

Matchande år per parti av kvarvarande, efter uteslutningen: C 4/13, KD 7/15, L 7/13, M 7/15, MP 5/15,
S 5/15, SD 0/12, V 0/10. Klausulen fyrar inte. För SD och V var varje matchande år ett voteringsår,
så de går från 3/15 till noll.

### 9. Vad de tolv posterna gör med andelarna

Största andelsförskjutning över de sju kategorierna, i procentenheter, om posterna faller: V 0,868,
SD 0,752, C 0,176, L 0,162, och noll för S, M, KD och MP. De fyra sista har inga voteringsposter, så
deras noll är konstruktion och inte fynd.

### 10. `a1` har ett kanalbegrepp men ingen kanalgrind

ADR 0011 prövar en **indikator**. ADR 0014 punkt 5 lyfte samma regel ett steg upp, till ett
**undermått**. Ingen av dem når ett parti-år inne i en kanal. Formen finns alltså, men den saknar det
steg det här fallet behöver.

### 11. `a_cov_by_cat` gör dubbel tjänst

Variabeln sätts i `pipeline/scorerun.py:949-964` och läses på två ställen: `scorerun.py:1170` som
cellens A-täckning, och `scorerun.py:1041` som A:s del av Mättaket. `_coverage_ceilings` skriver
själv ut varför det inte får fortsätta: "Talet står en gång per kategori och aldrig på cellen: det är
samma tal för alla åtta partier."

## Beslut

1. **En röst är inte ett prioriteringsbesked.** De tolv parti-år vars enda citerbara grund är
   `basis: votering` utesluts ur `a1`. Uteslutningsskälet är **`giltighetsfel`** (ADR 0011 punkt 2
   steg 2). Övriga delade ramar står kvar: en gemensam motion är undertecknad, och en regeringsram är
   koalitionsskriven. Skillnaden är författarskap, aldrig roll och aldrig hur många partier som står
   på ramen.

2. **ADR 0011:s regel utvidgas till en kanalobservation.** Samma tre prov, samma ordning, samma krav
   på ett återöppningsvillkor. Objektet är ett (parti, budgetår) inne i `a1`. Formen är den
   ADR 0014 punkt 5 använde när den lyfte regeln från indikator till undermått.

3. **Uteslutningen skrivs som en klassregel, aldrig som tolv fält.** `config/budget_ramar.yaml` är
   autogenererad och får inte handredigeras, alltså kan en modellregel inte bo där. Regeln ligger i
   `config/scoring.yaml` under `A_agerande`, selekterar på `basis: votering` och bär `exclusion` och
   `reopen_if`. `basis` står orört: det bokför källan, och uteslutningen är modellens dom. Det är
   ADR 0011 punkt 3:s delning, alltså ett fält och ett besked.

   `votering` är klassvillkoret och aldrig skälets namn. Skälet heter `giltighetsfel`, eftersom namnet
   ska peka på regeln som fäller och inte på symtomet (ADR 0011 punkt 5).

4. **Återöppningsvillkoret.** Uteslutningen hävs för ett parti-år om en citerbar **officiell svensk**
   källa belägger att partiet **författat eller undertecknat** den aktuella ramen, inte bara röstat
   för den. Partidokument duger inte under CLAUDE.md:s källregel. Källraden måste knyta partiet till
   just den ramen, annars smyger rollslutledningen tillbaka genom villkoret.

5. **Grinden lossas per parti.** ADR 0007 punkt 5 förkastade att lossa grinden **till per år**, med
   skälet att kategorier då får olika fönster. Per parti träffas inte av det skälet: varje kategori
   behåller samma fönster, och varje parti behåller samma årsmängd i alla sju kategorier. Utan
   lossningen tar uteslutningen `a1` från 7 kategorier till 0, tyst (diagnos 6).

6. **Förankringen följer partiets egna år.** ADR 0007 punkt 1 kräver att täljare och förankring täcker
   samma år. Med olika giltiga årsmängder betyder det en förankring per distinkt årsmängd, alltså
   fyra i dag. Förankringen är ingen partistorhet: den är de antagna ramarnas andel, alltså en
   egenskap hos **året**. `anchor.a1_anchor_shares` tar redan `years`. En delmängd av åren bryter inte
   ADR 0005, som förkastade förankring i **fältet**.

7. **Citerbar ram delas i två roller.** ADR 0007 punkt 2:s gräns, alltså tidigaste år där alla åtta har
   en citerbar ram, sätter fortfarande fönstret. Den prövar en dokumenterad **ramanknytning**. Att
   mata `a1`:s täljare kräver mer, nämligen ett giltigt besked om partiets egen prioritering. Fönstret
   2011 till 2025 står därför kvar, och uteslutningen verkar inne i det.

8. **Villkorsklausulen prövas på partiets egen giltiga årsmängd. Rättsverkan förblir global.**
   Klausulen frågar om ett parti har en egen nollpunkt, och den frågan går bara att ställa på de år
   partiet faktiskt mäts på. Verkan står kvar som ADR 0007 punkt 4 skrev den: fyrar den för något
   parti faller `a1` ur A för alla kategorier.

9. **Faran skrivs ut i stället för att lappas.** Diagnos 8 visar att klausulens vila hänger på tre år.
   Beslutspunkt 8 gör dessutom provet lättare att uppfylla, eftersom en mindre årsmängd är lättare att
   matcha helt. Det är rätt riktning: ju mindre underlag ett parti har kvar, desto närmare ligger det
   att `a1` inte mäter något eget för det partiet, och klausulen är just den vakt som ska fånga det.
   Talen i diagnos 8 skrivs in här så att nästa biljett ser var marginalen ligger.

10. **Täckningen blir proportionell.** `a1`:s bidrag till A:s delpoängstäckning är
    `w_a1 x (partiets giltiga år / fönstrets år)`. Med fullt täckt `a2` ger det A:s delpoängstäckning
    V 0,833, SD 0,900, C och L 0,933, och 1,000 för S, M, KD och MP. Precedensen är ADR 0008 punkt 4:
    det som fattas räknas delvis täckt på **full** nämnare, aldrig bort ur den. Täckningen rör inte
    betyget (ADR 0008 punkt 7).

11. **Det är ingen säkerhetsfråga.** Färre år breddar inte bandet. ADR 0009 punkt 2 låste att A är väl
    känd i varje cell, eftersom ingenting i A skattas: `a1` är transkriberat och citerar sin källrad.
    ADR 0013 punkt 6 sade samma sak om a2:s årsvariation. De uteslutna åren är inte osäkra, de är
    ogiltiga, och ADR 0009 punkt 4 skrev själv att ett giltighetsfel inte möts med ett bredare band.

12. **`a_cov_by_cat` delas i två.** Mättaket behåller A som **kategorikonstant** 1,00 när `a1` står,
    eftersom ADR 0014 punkt 4:s bärande egenskap är att talet är samma för alla åtta partier. Cellens
    A-täckning blir **per parti**. Utan delningen får Mättaket åtta värden per kategori, och då mäter
    det partiet i stället för modellen, alltså precis det ADR 0014 hette efter.

13. **Två daterade noter läggs, och ingen ADR skrivs om.** ADR 0008 punkt 3 får sin andra not, efter
    ADR 0015:s: A:s täckning är inte längre 100 när `A_a1_active` står, utan
    `w_a1 x (giltiga år / fönstrets år) + w_a2`. ADR 0015 rad 83 får en not om räknefelet i diagnos 1.
    Formen är repots egen, se ADR 0008 rad 76 och ADR 0001 rad 52.

14. **Blindheten deklareras.** Känt före beslutet: `a1`:s partispann 1,02 till 1,30 mot `a2`:s 1,35
    till 2,95 (mätt i [#28](https://github.com/mcknschn/rosta/issues/28), bekräftat i #33), den
    publicerade rangordningen, och andelsförskjutningen i diagnos 9. Inget av dem är skälet. Skälet är
    attributionen. Vad beslutet gör med betyg, band och rangordning räknades inte ut innan ADR:n
    skrevs. Deklarationen finns för att påståendet "jag höll mig objektiv" är oprövbart när talen är
    kända, precis som ADR 0005 punkt 8, ADR 0007 punkt 8, ADR 0010 punkt 10 och ADR 0011 punkt 12
    skrev samma sak om sig själva.

## Godkännandetest

Regeltester. Ingen regel nämner ett betyg, ett band eller en rangordning.

1. **Klassregeln väljer exakt de parti-år vars `basis` är `votering`**, och den bär ett
   Uteslutningsskäl ur ADR 0011:s tre värden plus ett återöppningsvillkor. En regel utan endera faller
   i config-valideringen.
2. **Varje `votering`-not citerar en votering, och ingen `egen_ram`- eller `regeringsstallning`-not
   gör det.** Provet går på källraden och aldrig på `role` (diagnos 4).
3. **`a1_shares` hårdfailar** när två partier kommer ut med olika antal år utan att en uteslutning
   förklarar skillnaden. Det tysta medlet i diagnos 6 är felet regeln stänger.
4. **`validate` låser `basis` till en sluten mängd och kräver `note`** på varje party_frame-rad.
5. **För varje parti täcker `a1`:s täljare exakt de år partiets förankring täcker.** Det är ADR 0007
   godkännandetest 1 ett steg ned, från kategori till parti.
6. **Villkorsklausulen prövas på partiets egen giltiga årsmängd, och rättsverkan är global.** Ett
   parti som matchar den antagna ramen i varje år det har kvar fäller `a1` för alla åtta.
7. **Mättaket är samma tal för alla åtta partier i varje kategori. Cellens A-täckning är det inte.**
   De två prövas i samma test, annars kan delningen i beslutspunkt 12 göras åt fel håll utan att något
   faller.
8. **A:s delpoängstäckning är `w_a1 x (giltiga år / fönstrets år) + w_a2`** och ärver blandningen ur
   configen, så en ändrad blandning följer med. Provet kör **båda** grindlägena, av skälet
   ADR 0015 godkännandetest 3 ger.
9. **Hela åttavektorn från `shared_frame_years` är låst i test**, inte bara L och SD, och
   delningstalet redovisas per grund. `tests/test_a_fonster.py:229-252` låser i dag två av åtta tal
   fast alla åtta publiceras.
10. **Inget test påstår något om `a1`:s spann, om separationen eller om rangordningen.**

Regel 2, 3 och 4 byggs oavsett utgången av beslutspunkt 1. De stänger hål som finns i dag.

## Övervägda alternativ

- **Ingen ändring, kostnaden skrivs bara ut.** Förkastat. Utgången var godkänd, och ADR 0015 skrev
  redan ut kostnaden. Men att skriva ut är svaret på en kanal som mäter rätt storhet sämre. Här mäter
  en av tre företeelser fel storhet: fördelningen över 27 utgiftsområden har ingen källa i ett ja.
  ADR 0009 kallar det ett giltighetsfel, och ADR 0011 punkt 1 låste att en uteslutning är ett eget
  besked och inte en fotnot.

- **Utesluta varje delad ram.** Förkastat. Det vore 108 av 120 parti-år, och regeln skulle vila på hur
  många partier som står på ramen i stället för på vad källan belägger. En gemensam motion är
  undertecknad av var och en den namnger. Att i stället gå på rollen är ADR 0001:s gräns: rollen är
  C:s fråga.

- **Väga ned `a1`.** Förkastat på ADR 0015 punkt 3 och på biljettens egen avgränsning. En vikt är
  aldrig instrumentet för tvivel.

- **Krympa fönstret till de voteringsfria åren.** Förkastat på diagnos 7. Det vore att stryka 10 av 15
  år för alla åtta partier för att laga 12 parti-år, och den återstående mängden är handplockad och
  har ett hål i mitten.

- **Skriva uteslutningen som tolv fält i `config/budget_ramar.yaml`.** Förkastat på beslutspunkt 3.
  Filen är autogenererad, och en modelldom inskriven i en källtranskription blandar ihop de två besked
  ADR 0011 punkt 3 höll isär.

- **Möta färre år med ett bredare band.** Förkastat på beslutspunkt 11. ADR 0009 punkt 4 avvisade
  redan att tapetsera över ett giltighetsfel med en osäkerhetsmarkering.

- **Lossa grinden till per år.** Inte prövat här. ADR 0007 punkt 5 förkastade den, och beslutspunkt 5
  rör inte det förkastandet.

## Vad beslutet inte rör

- **Blandningen 0,5 x a1 + 0,5 x a2** (ADR 0015 punkt 1).
- **A:s form, avbildning och växelkurs** (ADR 0005 och ADR 0012).
- **Fönstret 2011 till 2025 och de tre gränser det faller ut ur** (ADR 0007 punkt 2).
- **`a2` och dess poolade förankring** (ADR 0013).
- **`basis`, `role` och `note` i `config/budget_ramar.yaml`.** Bokföringen står orörd. Regeln läser
  den.
- **Grindens fråga.** Den frågar fortfarande om partiet har en verifierad ram för varje UO i
  kategorin. Bara dess räckvidd flyttar, från alla partier per år till partiet självt.
- **Villkorsklausulens rättsverkan** (ADR 0007 punkt 4). Bara underlaget den prövas på flyttar.
- **Täckningens noll verkan på betyget** (ADR 0008 punkt 7).

## Följder

- **Bygget är en egen slice.** Den rör `pipeline/budget.py`, `pipeline/scorerun.py`,
  `pipeline/config.py`, `config/scoring.yaml`, `tests/test_budget.py`, `tests/test_a_fonster.py`,
  `tests/test_a_kanalerna.py`, `tests/test_cell_coverage.py`, `tests/test_mattak.py`, `DATA.md` rad
  176 och 292, metodrutan i `pipeline/scorerun.py`, `docs/done/fas1b_budget_metod.md` och
  `docs/done/expertgranskning/A_budgetramar.md`.
- **Omkörningen flyttar fyra partier.** V, SD, C och L får nya `a1`-andelar och en egen förankring,
  alltså 28 av 56 celler. S, M, KD och MP står still av konstruktion, eftersom de inte har någon
  voteringspost. Resultatet publiceras som det blir (ADR 0003 punkt 1).
- **Känslighetsanalysen körs om.** `A_component_mix` drar `a1` i varje dragning, och `a1` är ett annat
  tal efter slicen. Körningen är 10 000 dragningar med orört frö 20260821 och startar på uttryckligt
  klartecken.
- **Metodrutan får två ändringar.** Delningstalet delas upp per grund, så läsaren ser att `L 10` inte
  är samma sak som `L 9`. Och rutan namnger att tolv parti-år är uteslutna ur `a1` och varför, av
  samma skäl som ADR 0011 punkt 10 gav: ett sjunkande täckningstal utan förklaring inbjuder till fel
  slutsats.
- **Ordningen efter omkörningen är låst i sex steg**, som ADR 0015 skrev dem. Kör om. Validera och kör
  hela godkännandetestet. Diffgranska mot `dist/scores.snapshot.json`. Visa diffen. Skriv ny snapshot
  med `--write`. Synka och committa allt tillsammans. Testerna går före diffen.
- **En fråga graderas inte.** Klausulens marginal i diagnos 8 är utskriven och inte åtgärdad. Den blir
  en biljett först den dag ett partis giltiga årsmängd krymper vidare.
