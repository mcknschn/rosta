# Beskedet efter POC:en Samstämmighet

- Datum: 2026-09-14
- Biljett: [#47](https://github.com/mcknschn/rosta/issues/47) steg 5
- Underlag: [`resultat.md`](resultat.md) och
  [`config/samstammighet_poc/resultat.yaml`](../../config/samstammighet_poc/resultat.yaml)
- Trösklarna: [`forhandsregistrering.md`](forhandsregistrering.md) version 1, låst före räkningen

## 1. Utfallet

**Måttet klarar alla tre trösklarna.** Det gör det i den primära uppställningen och i var och en
av de fem varianterna.

| Tröskel | Krav | Utfall |
|---|---|---|
| Skiljbarhet | 5 skilda värden, spann 0,10 | 8 skilda, spann 0,491 |
| Längdkonfunden | \|r\| under 0,7 | -0,355 |
| Neutralitet | mellan högst inom | 0,084 mot 0,167 |

Enligt biljetten graderas då en grillning som avgör måttets form. **Den graderas.**

## 2. Grillningen ärver ett fynd som väger tyngre än trösklarna

POC:ens efterhandsprov visar att skiljbarheten kommer från en enda av de två sidorna.

- Profilavståndet korrelerar **0,998** med hur koncentrerad partiets retorikprofil är.
- Det korrelerar **0,163** med handlingssidans egen koncentration.
- Byts handlingssidan från A till a1 rå korrelerar de två uppsättningarna **-0,129** med varandra.

Den primära uppställningen mäter alltså i praktiken hur koncentrerat valmanifestet är, och knappt
alls ett glapp mellan två sidor. Byts kanalen på handlingssidan byter partierna plats.

**Trösklarna prövade fel sak.** De tre frågorna biljetten ställde var rimliga, och måttet klarar
dem alla tre. Ett mått kan ändå skilja partierna brett, vara oberoende av dokumentlängd och vara
neutralt mellan blocken, och samtidigt inte mäta det som var avsikten. Ingen av de tre trösklarna
kunde upptäcka det, eftersom alla tre prövar hur talen fördelar sig och ingen prövar var talen
kommer ifrån.

Det är ett fynd om trösklarna och inte om partierna.

## 3. Beskedet

1. **Grillningen graderas.** Måttet är värt att grilla.
2. **Grillningens första fråga är handlingssidan.** Ingen annan fråga går att avgöra före den,
   eftersom måttets utfall per parti hänger på vilken kanal handlingssidan läser.
3. **Måttet byggs inte före grillningen.** Vikten står kvar på 0.
4. **Talen i `resultat.md` får citeras som skiljbarhet och aldrig som samstämmighet.** Ett glapp
   är ett glapp, och ingen siffra i POC:en säger att ett parti är inkonsekvent eller att en
   inkonsekvens vore dålig för Sverige.

## 4. Vad grillningen måste avgöra

Biljettens sju öppna frågor står kvar. POC:en lägger till en åttonde, och flyttar upp den först.

| # | Fråga | Vad POC:en tillför |
|---|---|---|
| **0** | **Vad är handlingssidan?** | A normerad bär nästan ingen spridning (0,022 till 0,036 inom ett parti). a1 rå bär mer men grindas och delas mellan koalitionspartier. a2 rå ligger utanför repot. Frågan är olöst och blockerar resten. |
| 1 | Tillstånd 3, alltså nämner och arbetar emot | Orört. POC:en behandlar tillstånd 3 som tillstånd 2. |
| 2 | Nämnaren, sju kategorier eller bara de nämnda | POC:en körde på alla sju. V nämner tre och får därför det största avståndet, 0,663. Valet är alltså inte oskyldigt. |
| 3 | Får framåtkorpusen läsas | POC:en läste den utan att pröva någon post mot ett utfall. Utfallet ändras inte nämnvärt av valet: bakåt ger spann 0,547 och framåt 0,456. |
| 4 | Vad `tas upp` är | Skillnaden mellan halvorna är under 0,09 för sex partier av åtta. S och SD skiljer sig mer. |
| 5 | Regeringsställning | Blockskillnaden är 0,084 mot en spridning på 0,167, alltså liten. |
| 6 | Kategorins upplösning | Demokrati faller på skiljbarhet per kategori, spann 0,096 mot kravet 0,10. |
| 7 | Vikt 0 för alltid | Orört. Att ge måttet vikt kräver att ADR 0002 skrivs om först. |

## 5. Villkor för att lägga ned frågan

POC:en föll inte, så inget avslagsskäl skrivs. Nedläggningen kan ändå komma ur grillningen, och
villkoren skrivs här så att de går att pröva:

- **Faller fråga 0**, alltså finns ingen kanal på handlingssidan som bär mer spridning än A:s
  normerade profil, då mäter måttet retorikens koncentration och inget glapp. Då läggs det ned
  med ett daterat avslagsskäl, och den fil som skriver det hör hemma i den här katalogen.
- **Faller fråga 1**, alltså går riktningen inte att få tag i till ett rimligt pris, då bär måttet
  ett hål det aldrig kan täppa. Grillningen får avgöra om ett mått med det hålet är värt att
  bygga.

## 6. Vad detta besked inte gör

- **Det bygger ingenting.** POC:en ändrade ingen config, ingen pipeline och inget gränssnitt, och
  `dist/` är orört.
- **Det ger måttet ingen vikt.** Vikterna 0,30 A + 0,50 B + 0,20 D, C = 0 står kvar (ADR 0002).
- **Det rangordnar inga partier.** Profilavståndet är ett avstånd mellan två profiler.
- **Det återupptar inte Verklighetsbild.** De tre återöppningsvillkoren i
  [`../verklighetsbild_pilot/avslagsskal.md`](../verklighetsbild_pilot/avslagsskal.md) är orörda,
  och POC:en prövade ingen sanning.
