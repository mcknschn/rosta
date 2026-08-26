# ADR 0010: Ett reglage är en väg pipen redan kan gå

- Status: accepted
- Datum: 2026-08-26
- Beslutad i: biljett [#24](https://github.com/mcknschn/rosta/issues/24) under karta [#6](https://github.com/mcknschn/rosta/issues/6)
- Bygger på: [ADR 0001](0001-a-mater-prioritering.md), [ADR 0003](0003-skiljbarhet-och-kanslighetsanalys.md), [ADR 0005](0005-a-forankras-i-tid-inte-i-faltet.md) och [ADR 0007](0007-a-mats-over-samma-fonster-som-sin-forankring.md)

## Kontext

Biljett #24 graderades ur kartans dimma när [#21](https://github.com/mcknschn/rosta/issues/21)
byggde ADR 0005. Bygget strök `A_normalization` ur känslighetsanalysen, eftersom A inte
normaliseras längre och posten därmed inte hade något att dra i. Strykningen var riktig och
uttryckligen tillåten av biljetten.

Kvar blev ett hål. Delpoäng A väger 0,30 och hade efter strykningen ingen dragen post som rör
betyget. Den enda kvarvarande posten som nämner A är `default_subscore_certainty.A`, och den är
`band_only`, alltså rör den bandet och aldrig talet.

Biljetten frågade vad, om något, som ska dras i A:s ställe, och gav tre kandidater: fönstret
2011-2025, blandningen 0,6 x a1 + 0,4 x a2, eller ingenting.

Frågan gick inte att svara på utan att först svara på en fråga under den. Vad är det för sorts
lista ADR 0003 punkt 5 för, och vad kvalificerar en post till den? Den här ADR:n avgör den regeln.
Blandningen och fönstret följer sedan ur regeln som två prov.

## Diagnos

### 1. Talen i biljetten var en generation gamla

Biljetten citerade `dist/robustness.json` som filen såg ut efter
[#21](https://github.com/mcknschn/rosta/issues/21). Den kördes om 2026-08-23 i
[#26](https://github.com/mcknschn/rosta/issues/26). Slutsatsen står kvar men talen är andra.
`default_subscore_certainty.A` ligger på 0,093 kategoripoäng och 0,036 totalpoäng. Brusgolvet,
alltså de övriga `band_only`-posterna, ligger på 0,131 till 0,303 kategoripoäng. Monte
Carlo-felet på facken är 1,0 procentenheter (`meta.monte_carlo_error_bins`), så A:s enda post
ligger under mätgränsen. Premissen håller: **A har ingen post som rör betyget.**

### 2. Listan är ett register, inte ett anspråk på fullständig osäkerhet

Två läsningar av ADR 0003 punkt 5 var möjliga. Antingen påstår listan att den täcker all osäkerhet
i betyget, och då är en tom delpoäng med vikt 0,30 ett hål i själva påståendet. Eller så är listan
ett register över modellens byggda variationspunkter, och då är A:s frånvaro ett fynd om A.

Den andra läsningen stämmer med tabellen som den faktiskt ser ut. `D_region_weighting` står i
listan med **exakt ett** alternativ och kan per konstruktion inte flytta något. Noten i
`pipeline/robustness.py` säger varför: posten står kvar "för att frånvaron ska synas". En lista som
gjorde anspråk på att täcka all osäkerhet skulle inte bära en post som inte kan bära någon.

Skillnaden är inte akademisk. Under den andra läsningen är svaret på biljetten inte "något måste
dit", utan "har A en variationspunkt kvar?".

### 3. ADR 0009:s fynd om A svarar på en annan fråga

[ADR 0009](0009-sakerheten-mater-hur-val-talet-ar-kant.md) fann att **ingenting i A skattas**.
a1:s ramar är transkriberade med citerad källrad, och a2:s tunnaste cell bär 84 motioner. Det är
ett riktigt fynd, och det gäller A:s **data**.

Ett reglage rör A:s **metodval**. De två får inte blandas ihop. Ett fullständigt känt underlag kan
matas genom ett metodval som är satt och inte härlett, och då finns det något att dra i även om
ingen siffra är osäker.

### 4. Blandningen 0,6 x a1 + 0,4 x a2 har en riktning men ingen magnitud

Talet kom in i repots första commit (`0945a62`) och har aldrig rörts. ADR 0005 punkt 4 säger att
blandningen står kvar, och ADR 0007 listar den under "Vad beslutet inte rör". Ingen av dem härleder
talet.

Ett skäl finns ändå, och det står i konsekvenserna till ADR 0001:

> `a2` läser en restkanal för regeringspartier, eftersom de driver politik genom proposition och
> budget snarare än genom motioner. Begränsningen accepteras. `a1` väger 0,6 och bär
> regeringskanalen.

Skälet bär riktningen, alltså att a1 väger mer än a2. Det bär inte magnituden: 0,55 och 0,7 skulle
uppfylla det lika väl. Samma ADR förkastade en **rollberoende** blandning, med skälet att A då
skulle läsa partiets roll, och rollen är C:s fråga.

Tre hål i skälet, som alla är skäl att **mäta** blandningen och inget skäl att ändra den:

- **Det är aldrig mätt.** Påståendet gäller kategorifördelningen i ett regeringspartis motioner,
  inte antalet. Lagret bär motionerna som ett enda aggregat över 2014-09-01 till 2026-05-29,
  43 588 stycken utan uppdelning per riksmöte. Data som den ligger kan inte pröva skälet.
- **a1 bär regeringskanalen men kan inte tillskriva den ett parti.** M, KD, L och SD får identiska
  a1-tal i alla sju kategorier, eftersom de delar den antagna ramen. Det är precis vad ADR 0007
  punkt 4:s villkorsklausul finns för.
- **Det finns inget neutralt tal.** 0,6 påstår att en andelsenhet föreslagen ram är värd 1,5
  motionsandelar. 0,5 påstår att den är värd 1. Båda är påståenden om en växelkurs mellan kronor
  och dokument. En vikt är ett utbytesförhållande (OECD/JRC, biljett #8), så jämn delning är inte
  frånvaron av ett påstående.

### 5. Fönstret faller, men inte på biljettens skäl

Biljetten avfärdade fönstret med att spannregeln ger diskreta val deras byggda alternativ, och att
fönstret har exakt ett. Det argumentet håller inte mot `D_region_weighting`, som står i tabellen med
ett enda alternativ.

Det som fäller fönstret är underlaget. `config/a_forankring.yaml` bär a2:s förankring som **ett
enda aggregat** över 2011-01-01 till 2025-12-31, femton utskottssummor utan uppdelning per år.
a1:s förankring räknas däremot år för år. En dragning av `window.start` skulle alltså ändra a1:s
förankring och lämna a2:s orörd. Den skulle inte pröva ett metodval utan producera en
inkonsekvens. Configen kan inte uttrycka ett annat fönster.

Skälet står även efter [#27](https://github.com/mcknschn/rosta/issues/27), eftersom ADR 0007 lämnar
a2:s förankringskälla orörd.

### 6. Gränsen mellan byggt och dokumenterat var oskarp

ADR 0003 punkt 6 säger att diskreta val får sina **byggda** alternativ, varken fler eller färre.
Samtidigt drar `D_attribution_lag_years` värdena 0, 1, 2 och 3, fast repot bara använder 1, med
noten "använt 1, dokumenterat 2".

Motsägelsen är skenbar, och upplösningen är den regel den här ADR:n låser. `attribution_lag_years`
är ett **parametervärde koden redan tar emot**: pipen räknar med vilket heltal som helst utan att
någon skriver ny kod. Att lossa a1-grinden till per år (förkastad i ADR 0007 punkt 5) eller att
skala `q` mot förankringens historiska spridning (reserv i ADR 0007) är däremot **kodvägar som inte
finns**.

### 7. Ordet "källa" är dubbelbokat

I det här repot betyder **källa** en officiell källa till data. Det är CLAUDE.md:s egen rubrik, det
är evidensliggarens ord och det är hela projektets svensk-först-krav. ADR 0003 och
`pipeline/robustness.py` använder samma ord för ett draget metodval.

Ordlistan i `docs/done/evidens_trovardighet.md` §4.3 har regeln ETT namn var, och ASD-STE100
förbjuder ett ord som bär mer än en mening. Biljettens egen mening "A saknar en dragen källa" är
tvetydig mot repots källkrav. Ordet **reglage** används redan informellt för just det här, i ADR
0005 punkt 8 och i rubriken till `tests/test_robustness.py`.

## Beslut

1. **Regeln.** Ett **reglage** är en punkt där pipen kan gå en annan väg **utan att någon skriver
   ny kod**, och där **underlaget kan uttrycka den vägen**. Båda leden krävs. Första ledet skiljer
   ett parametervärde koden redan tar emot från en kodväg som inte finns. Andra ledet skiljer ett
   metodval från en inkonsekvens som configen inte kan bära.

2. **Vad listan påstår.** Listan i ADR 0003 punkt 5 är ett **register över modellens byggda
   variationspunkter**, inte ett anspråk på att täcka all osäkerhet i betyget. Att en delpoäng
   saknar reglage är därför ett fynd om delpoängen, aldrig automatiskt ett fel i listan. Det är den
   läsning tabellen redan följer, eftersom `D_region_weighting` står där utan att kunna flytta
   något.

3. **Ett dokumenterat men obyggt alternativ är inget reglage.** Att en ADR namnger ett alternativ
   under "Övervägda alternativ" ger det ingen plats i listan. Annars blir varje förkastat
   alternativ en post, och listan får ingen övre gräns. Faller ett sådant alternativ in som kod
   senare, blir det ett reglage automatiskt och utan en ny biljett.

4. **Blandningen är ett reglage.** Posten heter `A_component_mix`. Koden läser
   `A_agerande.components` och tar emot vilket par som helst, underlaget är oförändrat, och
   blandningen biter i 56 av 56 celler (`A_a1_active`). A får därmed tillbaka en post som rör
   betyget.

5. **Spannet är a1 i (0,50, 0,80], med a2 som resten.** Båda ändarna är härledda, ingen är vald.
   Nedre änden kommer ur ADR 0001, som härleder att a1 väger mer än a2. Övre änden kommer ur R1
   tillämpad på a2: R1 på 0,4 ger a2 i [0,20, 0,60], alltså a1 högst 0,80. ADR 0005 förkastade
   dessutom uttryckligen att ta bort a2, så a2 får inte gå till noll.

   R1 kan inte tillämpas på a1 direkt. a1 och a2 är ett enda tal med två namn, eftersom de summerar
   till 1, och R1 på 0,6 ger ett spann som bryter R1 för 0,4. Formen följer i stället prejudikatet
   från `subscore_weights`, som enligt ADR 0003 punkt 6 dras ur den mängd härledningen tillåter, så
   att analysen prövar **härledningens slutsats** i stället för en godtycklig omviktning. Här prövar
   den magnituden och lämnar riktningen i fred.

6. **Fönstret är inget reglage.** Det faller på regelns andra led: a2:s förankring är ett aggregat
   utan år, så configen kan inte uttrycka ett annat fönster. Biljettens eget skäl, att alternativen
   är för få, är avfört.

7. **Blandningens tal rörs inte här.** Att dra ett reglage är att mäta hur mycket ett låst val
   betyder, aldrig att förbereda en ändring av det. Att koppla ihop mätningen med ändringen är
   precis vad ADR 0003 punkt 1 förbjuder. Frågan om blandningen har en härledning ur ADR 0002:s
   anspråk är en **egen biljett**, blockerad av [#27](https://github.com/mcknschn/rosta/issues/27).

8. **Ordet.** **Reglage** är det kanoniska namnet på en dragen variationspunkt. *Källa* i den
   betydelsen är avfört och betyder i det här repot en officiell källa till data. Fältnamnet
   `source_influence` i `dist/robustness.json` står kvar tills en schemaändring ändå görs, så att
   ordbytet inte drar med sig ett gränssnittsbrott.

9. **Ett dött reglage stryks med en rad om varför.** Det är vad `A_normalization` fick i #21, och
   praxis skrivs här ut som regel. En post som förlorar sin variationspunkt tas bort ur tabellen,
   och skälet står kvar i noten där posten stod.

10. **Blindheten deklareras.** Den som beslutade hade sett att a2 bär ungefär 78 procent av A:s
    separation på 40 procent av vikten, och att a1 ger fyra av åtta partier identiska tal. Regeln i
    punkt 1 är härledd ur vad koden och configen kan göra, aldrig ur de talen, och den ändrar inget
    betyg. Deklarationen finns för att påståendet "jag höll mig objektiv" är oprövbart när talen är
    kända, precis som ADR 0005 punkt 8 och ADR 0007 punkt 8 skrev samma sak om sig själva.

## Godkännandetest

Ett regeltest, aldrig ett tal om inflytande eller rangordning. ADR 0003 punkt 1 förbjuder ökad
separation som mål, och punkt 3 förbjuder trösklar.

1. **Regeln förklarar hela dagens tabell utan undantag.** Var och en av de tjugo posterna klarar
   båda leden i beslutspunkt 1, `D_region_weighting` inräknad.
2. **`A_component_mix` finns i `robustness.SOURCES`** med spannet ur beslutspunkt 5, och
   mängdtestet i `tests/test_robustness.py` är uppdaterat till tjugoen namn.
3. **Posten är inte `band_only`.** Den rör betyget, och nollkontrollen för `band_only` gäller den
   inte.
4. **Inget tal om inflytande, spridning eller rangordning ingår i testet.**

## Övervägda alternativ

- **Dra fönstret ändå, som en post med ett enda alternativ.** Förkastat på beslutspunkt 6.
  `D_region_weighting` visar att formen är tillåten, men den posten är **konsekvent**: pipen läser
  `equal` och skulle läsa `population` om någon byggde det. En dragen `window.start` är inte
  konsekvent, den ändrar den ena halvans förankring och inte den andras.
- **Byta blandningen till 0,5 / 0,5 i den här ADR:n.** Förkastat, av tre skäl. Det är en ändring av
  betyget och inte av analysen, alltså fel biljett. Det skulle beslutas i samma andetag som talen om
  A:s separation blev kända, alltså inte blint mot rangordningen, vilket kartans Notes förbjuder.
  Och båda halvorna mäter över fel fönster tills #27 är byggd, så växelkursen skulle sättas på ett
  underlag ADR 0007 redan dömt ut.
- **Dra blandningen nu och härleda den om analysen visar att den betyder något.** Förkastat. Den
  ordningen kopplar mätningen till ändringen, och det är just den koppling ADR 0003 punkt 1
  förbjuder. Härledningsfrågan står på egna ben eller inte alls.
- **Låta A stå utan reglage och skriva ut frånvaron.** Förkastat på beslutspunkt 4. Frånvaron var
  ett riktigt besked så länge ingen variationspunkt fanns, men blandningen är en och klarar båda
  leden.
- **Låta ett dokumenterat alternativ räcka.** Förkastat på beslutspunkt 3. Då blir varje rubrik
  "Övervägda alternativ" en reglagefabrik.
- **Lämna ordet "källa" som det är.** Förkastat på beslutspunkt 8. Dubbelbokningen har inte skadat
  något än, men den gör biljettens egen fråga tvetydig, och ordlistans regel är ETT namn var.

## Vad beslutet inte rör

- Blandningens tal 0,6 x a1 + 0,4 x a2. Det står orört. Se beslutspunkt 7.
- Vikterna 0,30 x A + 0,50 x B + 0,20 x D, C = 0 (ADR 0002).
- Avbildningen `net_support_to_score` och den begränsade kvoten (ADR 0005 punkt 3).
- Fönstret, dess gränser och villkorsklausulen (ADR 0005 punkt 7, ADR 0007).
- `max_interval_halfwidth`. ADR 0003 punkt 1 förbjuder att sänka den som åtgärd.
- Skiljbarhetens storhet, de sju scenarierna och tröskelförbudet (ADR 0003 punkt 2, 3 och 8).
- B, C och D. ADR 0004, ADR 0006, ADR 0008 och ADR 0009 står oförändrade.

## Följder

- **Bygget är en egen slice**, blockerad av [#27](https://github.com/mcknschn/rosta/issues/27).
  ADR 0007 punkt 4:s villkorsklausul kan fälla a1 helt, och då har `A_component_mix` ingenting att
  dra i, alltså exakt samma död som `A_normalization` fick. Att bygga före #27 riskerar att skriva
  in en post som stryks i nästa slice.
- **Slicen kräver en omkörning.** 10 000 dragningar, ungefär tolv minuter enligt ADR 0003.
- **ADR 0003 punkt 5 får en not** som pekar hit. Listan är låst där, och en ny post ändrar ADR 0003
  och inte ADR 0005.
- **Mängdtestet i `tests/test_robustness.py` går från tjugo namn till tjugoen.**
- **Ordlistan §4.3 får Reglage**, och *källa* i den betydelsen förs av.
- **Ingen kod och ingen config ändras i det här ärendet.** Rangordningen är oförändrad tills slicen
  körs.
- **En fråga graderas ur beslutet:** har blandningen en härledning ur ADR 0002:s anspråk? Egen
  biljett, blockerad av #27.
- **Ändrat i det här ärendet:** den här ADR:n, en not i ADR 0003 punkt 5, och tre rader i ordlistan
  §4.3.
