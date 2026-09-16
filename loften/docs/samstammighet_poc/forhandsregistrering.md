# Förhandsregistrering av POC:en Samstämmighet

- Version: 1
- Status: **låst**
- Låst: 2026-09-14, före den första räkningen
- Beslutad av: biljett [#47](https://github.com/mcknschn/rosta/issues/47) steg 1
- Körs i: biljett #47 steg 2 till 5
- Räknas av: `python -m pipeline.tools.samstammighet --resultat`

Talen i denna fil står skrivna innan något räknades. De ändras aldrig efteråt. Ändras de ändå,
faller POC:en och måste köras om. Ordningen går att se på commit-datum, och
`tests/test_samstammighet_poc.py` läser den ur git i stället för att lita på en rad i filen.

Förebilden är [Verklighetsbildpilotens förhandsregistrering](../verklighetsbild_pilot/forhandsregistrering.md),
som låstes 2026-09-13 på samma sätt.

## 0. Vad POC:en avgör

POC:en bygger inte måttet. Den avgör om måttet är värt att grilla. Den svarar på tre frågor och
inga andra:

1. Skiljer måttet partierna?
2. Mäter det dokumentlängd?
3. Är det neutralt mellan regering och opposition?

**Måttet väger 0.** Det ingår inte i någon poäng, något band eller någon rangordning, av samma
skäl som gav Verklighetsbild vikt 0. Ett osammanhängande valmanifest är inte i sig dåligt för
Sverige. `dist/` är orört och ingen befintlig config ändras.

## 1. Enheten

Enheten är **(parti, kategori)**, alltså 8 partier gånger 7 kategorier, 56 celler. Partikoderna
och kategori-id:na läses ur `config/categories.yaml`.

Ingen sammanvägning till ett betyg sker. Se avsnitt 5 för hur tröskelstatistiken skiljer sig från
ett betyg.

## 2. Retoriksidan

**R(p, c) = kategorins andel av partiets manifestposter.**

### 2.1 Vilket material som räknas

**Unionen av de två korpusarna avgör.** Bakåtkorpusen bär 896 poster av typen `detta är ett
problem`, framåtkorpusen 1 073 poster av typen `detta ska vi göra`. Unionen bär 1 969.

Skälet är belöningslogikens egen formulering. Kedjan säger `något tas upp i valmanifestet`, och
`tas upp` skiljer inte på tempus. Unionen är dessutom det tal biljettens egen längdfråga vilar
på: 525 poster för M och 107 för MP är unionens tal.

Bakåt och framåt räknas **var för sig och redovisas alltid**, men de avgör ingenting. Skillnaden
mellan de två halvorna är underlag till grillningens öppna fråga 4.

### 2.2 Frysningen tillåter att framåtkorpusen läses

Framåtkorpusen är fryst till brytpunkten 2030-09-08
([ADR 0016](../adr/0016-verklighetsbild-avgors-av-en-pilot.md) beslutspunkt 4). POC:en läser den
ändå, och skälet står här.

Frysningen förbjuder tre saker: att en post ändras, att en post läggs till och att en post tas
bort. POC:en gör ingen av dem. Den läser filen och räknar kategorietiketten.

Frysningens syfte är att hindra efterhandsval av formulering, indikator och tröskel när perioden
väl är slut. Att räkna kategorietiketten på samtliga 1 073 poster väljer ingenting. Varje post
räknas, och ingen post får ett indikatorval.

**Gränsen skrivs ut:** ingen framåtpost prövas mot något utfall här, och ingen framåtpost får en
indikator. Gör någon det före 2030-09-08 är frysningen bruten, och det är inte den här POC:ens
sak att göra.

### 2.3 Nämnaren

Nämnaren är partiets poster **i de sju kategorierna**.

Båda korpusarna bär en åttonde etikett, `Utanför de sju kategorierna`. De posterna räknas bort ur
både täljare och nämnare. Skälet är att handlingssidan bara är definierad på de sju. En post
utanför dem har ingen handlingssida att jämföras med. Antalet borträknade poster redovisas per
parti.

Andelarna summerar därför till 1 över de sju kategorierna, för varje parti.

**En kategori partiet aldrig nämner får andelen 0.** Nämnaren är alltså alltid alla sju, aldrig
bara de kategorier partiet nämner. Grillningens öppna fråga 2 gäller måttets form och inte
POC:ens räkning.

### 2.4 Kategorinamnen

Korpusarna bär kategorins **namn** och `config/categories.yaml` bär dess **id**. Ett namn skiljer
sig: korpusarna skriver `Integration och sammanhållning` där configen skriver `Integration och
social sammanhållning`. Bryggan står i koden som en uttrycklig tabell.

**Ett okänt kategorinamn faller hårt.** En post får aldrig falla bort tyst, eftersom ett tyst
bortfall skulle krympa nämnaren utan att synas.

## 3. Handlingssidan

**H(p, c) = kategorins andel av partiets kraft.**

### 3.1 Den primära kanalen avgör

**Delpoäng A ur `dist/scores.json`, normerad inom partiet över de sju kategorierna:**

```
H(p, c) = A(p, c) / summa_c A(p, c)
```

Tre skäl. A är projektets eget mått på hur mycket kraft ett parti lägger på en kategori
([ADR 0001](../adr/0001-a-mater-prioritering.md)). A täcker alla 56 celler utan grind. A ligger i
repot, så räkningen är reproducerbar utan ny hämtning.

### 3.2 Begränsningen i den primära kanalen

**A är ingen andel av kraft.** A är en graderad poäng 0 till 5, avbildad ur kvoten mellan partiets
andel och en historisk förankring
([ADR 0005](../adr/0005-a-forankras-i-tid-inte-i-faltet.md)). Normeringen i 3.1 är därför en
**omräkning till profil** och ingen mätning av andel. Den gör tre saker som måste stå skrivna:

1. **Den flyttar nollpunkten.** En kategori där partiet ligger under förankringen får ändå en
   positiv andel, eftersom A är bunden nedåt av 0 och i praktiken ligger långt över.
2. **Den komprimerar.** A är bunden i [0, 5], så profilen kan aldrig bli lika spetsig som
   retorikprofilen kan bli.
3. **Den är inte invariant mot A:s skala.** En annan avbildning av kvoten till poäng ger en annan
   profil, även om rangordningen inom partiet står still.

Biljetten kallar normeringen en gissning. Den bedömningen står kvar. Punkt 1 och 2 gör att glappet
i avsnitt 4 systematiskt mäter **hur mycket spetsigare retoriken är än handlingen**, och det är en
egenskap hos normeringen och inte hos partierna. Därför finns den sekundära kanalen.

### 3.3 Den sekundära kanalen redovisas alltid

**a1 rå, alltså kategorins andel av partiets egna föreslagna utgiftsramar**, som medel över
budgetåren 2011 till 2025, renormerad över de sju kategorierna.

Den är en äkta andel av kraft, mätt i pengar, och den ligger i repot
(`config/budget_ramar.yaml`). Hela tröskelprövningen körs om på den, och utfallet redovisas.

**Den avgör ingenting**, av två skäl. Ett regeringsår bärs av en delad ram, så koalitionspartier
får identiska tal de åren
([ADR 0017](../adr/0017-a1-laser-forfattarskap-inte-uppslutning.md)). Och a1 är grindad i
modellen, så den bär inte hela A.

Renormeringen behövs eftersom a1:s nämnare är hela ramen, alltså även de utgiftsområden som inte
hör till någon kategori. Utan renormering skulle de två sidorna ligga på olika skalor, och glappet
bli systematiskt positivt av ren konstruktion.

### 3.4 a2 används inte, och biljetten bär ett fel på den punkten

Biljettens steg 3 pekar ut `config/a_forankring.yaml` som råkanalernas plats. **Det stämmer
inte.** Den filen bär **förankringen**, alltså de beslutade utgiftsramarna och kammarens samtliga
motioner. Partiets egen täljare ligger någon annanstans: a1:s i `config/budget_ramar.yaml` och
a2:s i lagret `data/warehouse.duckdb`.

Lagret är gitignorerat. Godkännandetest 2 kräver att räkningen är reproducerbar ur repot, så
**a2 faller ur POC:en**. Följden skrivs ut: POC:en ser bara pengakanalen och aldrig
motionskanalen på rå nivå. Motionskanalen finns ändå med inbakad i den primära kanalen, eftersom
A blandar a1 och a2 med vikterna i `config/scoring.yaml`
([ADR 0015](../adr/0015-as-tva-kanaler-vager-lika.md)).

## 4. Glappet

```
G(p, c) = R(p, c) - H(p, c)
```

Positivt glapp betyder att partiet säljer in kategorin mer än det lägger kraft där. Negativt glapp
betyder tvärtom.

**Ett glapp är ett glapp.** Ingen text i POC:en kallar ett glapp ohederlighet, inkonsekvens eller
löftesbrott. Ett parti kan vara inkonsekvent och ändå ha den bästa politiken.

Riktningen på handlingen ingår inte. Biljettens tillstånd 3, alltså partiet som nämner något och
arbetar emot det, behandlas som tillstånd 2. Öppen fråga 1 avgörs i grillningen och inte här.

## 5. Tröskelstatistiken per parti

Tröskel 1 talar om `minst fem skilda värden över de åtta partierna` och om `spannet mellan högsta
och lägsta`. Det är en ordnad mängd om åtta tal, alltså ett tal per parti. Den statistiken
definieras här.

### 5.1 Profilavståndet avgör

```
TV(p) = 0,5 * summa_c |G(p, c)|
```

Båda profilerna summerar till 1 över de sju kategorierna, så TV ligger i [0, 1]. Talet läser rakt
av: **den andel av partiets betoning som skulle behöva flytta för att de två profilerna skulle
sammanfalla.**

Det är totalvariationsavståndet mellan två fördelningar, alltså ett vedertaget avstånd och ingen
konstruktion för det här ändamålet.

### 5.2 Varför ett avstånd inte är ett betyg

Godkännandetest 3 förbjuder ett sammanvägt betyg. Profilavståndet är inget betyg, och skillnaden
står här:

- Det **inverteras aldrig** till ett samstämmighetstal.
- Det **rangordnas aldrig** som bättre eller sämre.
- Det bär **inga kategorivikter**. Alla sju räknas lika, vilket följer av avståndets definition
  och inte av ett omdöme om vilken kategori som är viktigast.
- Det är **ingen delpoäng** och väger 0.

Att alla sju räknas lika är ändå ett val, och det skrivs här. Kategorierna bär olika
standardvikter i modellen, från 20 för ekonomi till 7,5 för demokrati. Avståndet bryr sig inte om
dem, eftersom det mäter avståndet mellan två profiler och inte kategoriernas betydelse för
Sverige.

### 5.3 Det andra talet redovisas alltid

**Största positiva glapp per parti**, alltså `max_c G(p, c)`, plus kategorin som bär det. Det är
talet biljettens egen handräkning använde. Trösklarna körs om på det och utfallet redovisas, men
profilavståndet avgör.

## 6. Trösklarna

Ordagrant ur biljetten, med räkningen skriven ut.

### 6.1 Skiljbarhet

> Måttet ger minst fem skilda värden över de åtta partierna, och spannet mellan högsta och lägsta
> är minst 0,10.

Prövas på profilavståndet. Två värden räknas som skilda när de skiljer sig efter avrundning till
**tre decimaler**. Spannet är högsta minus lägsta.

Prövningen körs **dessutom per kategori**, på glappets åtta värden i den kategorin. Det utfallet
**redovisas alltid men avgör inte**. Skälet är att en kategori där alla åtta partier ligger lika
nära sin handling inte är ett fel hos måttet, och biljettens tröskel talar om en ordnad mängd om
åtta tal och inte om sju sådana mängder.

### 6.2 Längdkonfunden

> Korrelationen mellan måttet och partiets antal manifestposter håller sig under 0,7 i
> absolutbelopp.

Pearsons r mellan profilavståndet och partiets antal manifestposter i de sju kategorierna, räknat
på unionen. Åtta observationer. Måttet faller om `|r| >= 0,7`.

Spearmans rangkorrelation redovisas bredvid, men avgör inte. Skälet är att biljetten skriver
`korrelationen` utan kvalifikation, och Pearson är den läsning som ligger närmast en linjär
konfund.

**Begränsningen skrivs ut:** åtta observationer ger en mycket bred osäkerhet i r. Talet 0,7 är en
gräns för när konfunden är stor nog att diskvalificera måttet, och ingen statistisk prövning.

### 6.3 Neutralitet

> Skillnaden mellan regeringssidan och oppositionssidan redovisas alltid. Överstiger den
> spridningen inom blocken faller måttet, om det inte går att skriva ned en mekanism som förklarar
> skillnaden utan att ta ett partis parti.

**Sidorna läses ur `config/mappings.yaml`**, `government_periods`, den sittande regeringen
Kristersson från 2022-10-18:

| Sida | Partier | Skäl |
|---|---|---|
| Regeringssidan | M, KD, L, SD | `parties` plus `support_parties` |
| Oppositionen | S, V, C, MP | resten |

SD räknas på regeringssidan. Skälet är att modellen redan bär stödpartiet som ansvarigt i sina
`responsibility`-claims, och att Tidöavtalet gav SD del i regeringens program. **Varianten där SD
står utanför båda blocken redovisas alltid** som känslighetsprov.

Räkningen:

```
mellan = |medelvärde(regeringssidan) - medelvärde(oppositionen)|
inom   = roten ur ((s_reg^2 + s_opp^2) / 2)      s = stickprovets standardavvikelse, ddof=1
```

Måttet faller om `mellan > inom`. Talet `mellan / inom` är Cohens d med lika stora grupper, och
regeln säger alltså `|d| <= 1`.

Klausulen om en mekanism står kvar. Faller måttet på den här tröskeln skrivs antingen en mekanism
ned, eller ett avslagsskäl. Mekanismen måste gå att pröva och får inte ta ett partis parti.

### 6.4 Redovisningen

> Punktskattningar och spridning redovisas oavsett utfall.

Se avsnitt 7.

## 7. Spridningen

### 7.1 Vad osäkerheten är

Retoriksidan bär en urvalsosäkerhet. Partiets poster är de poster manifestet råkade bära, och
intervallet läser som **hade partiet skrivit ett annat manifest av samma längd**.

Handlingssidan bär ingen urvalsosäkerhet. A är räknad över hela förankringsfönstret och inte ur
ett stickprov.

### 7.2 Hur den räknas

**Bootstrap på retoriksidan.** Partiets poster dras om med återläggning, lika många som partiet
bär, 10 000 gånger. Handlingssidan hålls fast. För varje omdragning räknas profilavståndet och
glappet om.

- Frö: **20260914**
- Omdragningar: **10 000**
- Intervall: percentil 2,5 till 97,5
- Generator: `random.Random(frö)`, ett eget frö per parti, härlett som `frö + partiets index i
  config/categories.yaml`

Fröet och antalet omdragningar är låsta. Ändras de, faller POC:en.

### 7.3 Begränsningen

Bootstrappen mäter **bara retoriksidans urvalsosäkerhet**. Tre osäkerheter ligger utanför:

1. Osäkerheten i kategoriseringen av en post. Etiketten är satt en gång och prövas inte här.
2. Osäkerheten i A. A:s eget osäkerhetsintervall ligger i `dist/scores.json` och går inte att föra
   in i en normerad profil utan att anta hur felen samvarierar mellan kategorier.
3. Osäkerheten i normeringen. Se avsnitt 3.2.

Intervallet är därför indikativt och aldrig exakt.

## 8. Vad som händer när trösklarna faller

**Att måttet faller är en godkänd utgång.** Klaras inte trösklarna skrivs ett **daterat
avslagsskäl** i `docs/samstammighet_poc/`, med villkor för att ta upp frågan igen, och arbetet
läggs ned.

Förebilden är
[`docs/verklighetsbild_pilot/avslagsskal.md`](../verklighetsbild_pilot/avslagsskal.md) och
mönstret med `reopen_if` ur [ADR 0011](../adr/0011-uteslutningen-ar-ett-eget-besked.md).

Klaras trösklarna graderas en grillning som avgör måttets form. POC:en bygger aldrig måttet.

## 9. Vad POC:en aldrig publicerar

- **Inget sammanvägt betyg.** Se avsnitt 5.2.
- **Ingen rangordning av partier.** Profilavståndet sorteras i tabell, men ingen text kallar ett
  högt avstånd sämre än ett lågt.
- **Ingen riktning.** Se avsnitt 4.
- **Ingen text som kallar ett glapp ohederlighet.**
- **Ingen ändring i `dist/`, i pipen, i configen eller i gränssnittet.** Verktyget ligger i
  `pipeline/tools/` och körs för hand, precis som Verklighetsbildpilotens verktyg.

## 10. De öppna frågorna POC:en inte avgör

Biljettens sju öppna frågor grillas inte här. Fyra av dem har ändå ett **provisoriskt val** i den
här filen, satt för att räkningen ska gå att göra, och valet binder inte grillningen:

| Fråga | Provisoriskt val | Står i |
|---|---|---|
| 2. Nämnaren | alla sju kategorier | 2.3 |
| 3. Får framåtkorpusen läsas | ja, utan att någon post prövas mot ett utfall | 2.2 |
| 4. Vad `tas upp` är | unionen av bakåt och framåt | 2.1 |
| 5. Regeringsställning | vägs inte in, men redovisas som blockskillnad | 6.3 |

Fråga 1 om tillstånd 3, fråga 6 om kategorins upplösning och fråga 7 om vikt 0 rör POC:en inte
alls.
