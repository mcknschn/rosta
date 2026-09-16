# ADR 0018: B:s medelvärde bär inte anspråket om storlek

- Status: accepted
- Datum: 2026-09-14
- Beslutad i: biljett [#45](https://github.com/mcknschn/rosta/issues/45) under karta [#6](https://github.com/mcknschn/rosta/issues/6)
- Bygger på: [ADR 0002](0002-kategoripoangens-ansprak-och-vikter.md), [ADR 0003](0003-skiljbarhet-och-kanslighetsanalys.md), [ADR 0004](0004-vad-delpoang-b-mater.md), [ADR 0006](0006-evidensgrinden-ar-symmetrisk.md), [ADR 0008](0008-cellens-tackning.md) och [ADR 0011](0011-uteslutningen-ar-ett-eget-besked.md)
- Ändrar: [ADR 0004](0004-vad-delpoang-b-mater.md) beslut 1

## Kontext

Biljett #45 frågade om en enhällig post får ligga i samma undermått som differentierande poster. En
enhällig sakpunkt ger alla åtta partier `supports` på samma åtgärdstyp. Metoden som tillåter det
står i `docs/done/evidens_trovardighet.md` §5.2 och har gett fem av repots byggda mått.

Biljetten drog fyra gränser. Den symmetriska evidensgrinden öppnas inte (ADR 0006). Svaret får inte
bli en vikt (ADR 0015 punkt 3). Uteslutning och utskrivning är de byggda formerna (ADR 0011). §5.2
skrivs inte om utan beslut. "Ingen ändring" var en godkänd utgång.

Frågan visade sig vara fel ställd. Enhälligheten är symptomet. Felet sitter i B:s form och gäller
varje svag positiv post, enhällig eller inte.

## Diagnos

Mätt 2026-09-14 mot `config/`, `pipeline/` och en exakt omkörning av `pipeline.scorerun.build()`
mot det befintliga lagret. Se punkt 6 för vad som räknades och varför det var tillåtet.

### 1. Formen är ett medelvärde, och anspråket gäller en storlek

ADR 0004 beslut 1 låser B:s anspråk:

> B svarar på *hur stor förbättring väntas av de åtgärder partiet driver?* Storlek, inte riktning.

ADR 0004 beslut 3 låser formen. `pipeline/effects.py` räknar `net = Σ(q·m) / Σ q` per
(parti, kategori, indikator), där `q` bär kvaliteten och `m` bär storleken med tecken.

En kvot med `Σ q` i nämnaren är ett medelvärde. Ett medelvärde mäter portföljens genomsnittliga
storlek. Anspråket gäller den väntade förbättringens storlek. De två går isär, och isärgåendet
ryms i två rader:

| partiets poster | `net` | betyg |
|---|---|---|
| en post, `q` 0,48 och `m` 0,60 | 0,600 | 4,00 |
| samma post plus `q` 0,48 och `m` 0,30 | 0,450 | 3,63 |

Den andra posten har **belagd positiv effekt**. Att stödja den sänker betyget. Det är ren algebra
och gäller varje gång en posts `m` ligger under partiets dittills vägda medel.

### 2. Breddkanalen räcker inte, och det är mätt

Instrumentet har en kanal som belönar bredd. Täckningskrympningen `B = 2,5 + (rått - 2,5) × täckning`
låter betyget röra sig längre från neutral när partiet har positioner på fler åtgärdstyper. De två
kanalerna drar åt olika håll när en svag positiv post läggs till.

Indikatorn `skolresultat` bär fyra admitterade poster. Tre differentierar. Den fjärde,
`kompetensutveckling_larare`, har alla åtta partier på `supports`, `authority_evaluation`, styrka
`low` och konfidens `medium`. Exakt omkörning med och utan den posten:

| parti | B med | B utan | rörelse | välfärdsbetyg med | utan | rörelse |
|---|---|---|---|---|---|---|
| S | 2,8890 | 2,9500 | -0,0610 | 2,7420 | 2,7730 | -0,0310 |
| M | 3,0390 | 3,1000 | -0,0610 | 2,8480 | 2,8780 | -0,0300 |
| SD | 2,3840 | 2,2000 | **+0,1840** | 2,5450 | 2,4530 | **+0,0920** |
| C | 3,0390 | 3,1000 | -0,0610 | 2,7810 | 2,8110 | -0,0300 |
| V | 2,9060 | 2,9200 | -0,0140 | 2,6660 | 2,6740 | -0,0080 |
| KD | 3,0390 | 3,1000 | -0,0610 | 2,8150 | 2,8450 | -0,0300 |
| L | 2,9060 | 2,9200 | -0,0140 | 2,7600 | 2,7670 | -0,0070 |
| MP | 2,9000 | 2,9200 | -0,0200 | 2,7010 | 2,7110 | -0,0100 |

B-spannet är 0,655 med posten och 0,900 utan.

**Sju av åtta partier får ett lägre välfärdsbetyg därför att en åtgärd med belagd positiv effekt,
som samtliga åtta stödjer, ligger i liggaren.** Breddkanalen tog inte igen fallet i något av de sju
fallen. Under ADR 0004 beslut 1 är det inkoherent.

SD stiger, eftersom SD står `opposes` på de två differentierande posterna och därmed låg under
postens egen storlek. Det är medelvärdets vanliga beteende och inte ett besked om SD.

### 3. En post ensam på sin indikator beter sig precis som §5.2 lovade

Den andra 8/8-posten, `snabbforfarande_lagforing`, är ensam på indikatorn `handlaggningstid`. Exakt
omkörning:

| | rörelse |
|---|---|
| B, alla åtta partier | **+0,3000**, lika för var och en |
| trygghetsbetyget, alla åtta partier | **+0,1500**, lika för var och en |
| B-spann | 0,675 med, 0,675 utan |

Gränsen går alltså vid indikatorn, inte vid undermåttet. Är posten ensam på sin indikator finns
inget medel att dras in i, och lyftet är likformigt in på fjärde decimalen. Delar posten indikator
med andra poster är det inte likformigt.

### 4. §5.2:s andra caveat är falsk sedan ADR 0004

§5.2 lyder ordagrant:

> (2) Det ger **täckning, inte rankning** (likformigt lyft).

Meningen skrevs när B var `tecken(stance) gånger täckning`, alltså före ADR 0004. Under den formen
stämde den. Under medelvärdet stämmer den bara i punkt 3:s fall. §5.2 är levande metod som en
människa eller en agent tillämpar varje gång en post skrivs in, så den felaktiga meningen styr
framtida poster.

§5.2:s tredje caveat varnade för utspädning mellan undermått. Den varnade för rätt sak på fel nivå:
utspädningen sker inom indikatorn, ett steg längre ned.

### 5. Enhällighet är inte klassen, och 8/8 är inte heller klassen

`config/party_positions.yaml` bär 39 åtgärdstyper. Elva har alla åtta partier på `supports`. Grinden
i ADR 0006 tog nio av dem, och två står admitterade.

Räknat på de 33 admitterade posterna har däremot **12** alla sina **kodade** partier på `supports`.
Bara 2 av dem har alla åtta. De övriga tio har 3 till 7 kodade partier.

De två grupperna bär olika mekanik:

- **Fullständigt kodad konsensus**, 2 poster. Alla åtta har en position. Posten är gemensam, och
  dess enda verkan är den medelvärdesdragning punkt 1 beskriver.
- **Partiellt kodad ensidighet**, 10 poster. Bara några partier har en position. Posten drar de
  kodade mot sin egen storlek och lämnar de okodade orörda. Den skiljer alltså partier åt på
  kodningsflit och inte på hållning. Det är `§5.6`:s aktivitetsbias, och den saknar modell: i dag
  betyder en saknad position varken stöd, motstånd eller okänt, den bara uteblir.

Fyra admitterade poster har inga partipositioner alls. De ligger i täckningens `T_s` och sänker
därmed täckningen för alla åtta utan att bidra till någon täljare. Det talet mäter kopplingen
mellan liggaren och positionsfilen, inte partierna.

### 6. Vad som räknades, och varför ADR 0003 punkt 1 inte fälls

ADR 0003 punkt 1 säger att talen räknas först när regeln är låst och nedskriven. Syftet är att ingen
regel ska väljas med kännedom om vem den gynnar.

Räknat: B och kategoribetyg per parti för `valfard` och `trygghet`, med och utan var sin post.
**Inte räknat:** band, totalpoäng eller rangordning under något alternativ.

Diagnosen i punkt 1 är algebra och var känd före varje omkörning. Omkörningen avgjorde bara om
breddkanalen tar igen fallet, alltså en egenskap hos instrumentet. Beslutet nedan följer ur
algebran. Ingen del av det följer ur vem som steg eller föll.

## Beslut

1. **Felet är ett konstruktfel mellan form och anspråk.** Det är varken utspädning eller ett
   spännviddsproblem. B:s medelvärdesform mäter genomsnittlig belagd effektstyrka och kan därför
   inte utan konstruktändring bära anspråket om storleken på den väntade förbättringen.

2. **Spännvidd förkastas som kriterium, uttryckligen.** Att välfärdens B-spann krymper 27 procent
   är ett symptom och aldrig ett skäl. ADR 0003 punkt 1 låste att skiljbarhet är ordningens
   stabilitet. En regel grundad på spannets storlek vore en regel som föredrar stora spann, alltså
   en tumme på vågen. Föreslå den inte igen.

3. **B:s anspråk begränsas tills formen rättas. Detta ändrar ADR 0004 beslut 1.** B svarar från och
   med nu på *hur stark är den belagda effekten i genomsnitt hos de åtgärder partiet driver, justerat
   för täckning?* Anspråket om storleken på den väntade förbättringen är inte längre B:s, förrän
   punkt 7 är byggd. Icke-monotoniciteten skrivs ut som en känd följd: en ytterligare åtgärd med
   belagd positiv effekt kan sänka B.

4. **§5.2 caveat (2) rättas.** Den ersätts av punkt 3:s gräns i klartext: en post som är ensam på
   sin indikator ger ett likformigt lyft, och en post som delar indikator med andra poster gör det
   inte. Metoden i övrigt står kvar oförändrad. Enhällighet får fortsatt vara källa.

5. **Klassen delas i två, och delningen gäller redovisningen.** Fullständigt kodad konsensus och
   partiellt kodad ensidighet är olika saker. En partiellt kodad post får inte beskrivas som
   konsensus någonstans i repot eller i det som når användaren, och en saknad position ska hållas
   uttryckligen okänd. Delningen är i övrigt diagnostisk: den säger var felet syns starkast, inte
   vad som ska göras åt det.

6. **Ingen post utesluts, och ingen placeringsregel införs.** Skälen står var för sig:
   - **Uteslutning** vore fel adress. Båda posterna klarar den symmetriska grinden i ADR 0006 på
     sina egna källor, och felet ligger inte i posterna.
   - **Placeringsregel** vore skör. Utfallet skulle bero på hur indikatorerna råkar vara indelade,
     alltså på en redaktionell gräns och inte på en egenskap hos evidensen.
   - **Vikt** är avvisad sedan ADR 0015 punkt 3. En vikt är inte instrumentet för tvivel.

7. **Rättelsen är en normaliserad summa, och den byggs i en egen biljett.** Nämnaren `Σ q` byts mot
   en förhandsbestämd och versionslåst evidensbudget per indikator, så att fler positiva poster
   aldrig kan sänka talet. Liggarens faktiska radantal får aldrig bestämma nämnaren, annars blir
   antalet poster en dold vikt, och flera poster på samma åtgärdstyp måste dela sin budgetandel.
   Budgetens form är en öppen designfråga och avgörs i sin egen biljett, inte här.

   > **Daterad not 2026-09-16, [ADR 0019](0019-kvoten-anvandes-over-fel-enheter.md) beslut 1.**
   > Frågan var fel ställd. Nämnaren är ingen storhet som ska väljas: kvoten användes över fel
   > enheter. Inom en åtgärdstyp står `Σ q` kvar som poolningsnämnare, eftersom flera
   > utvärderingar av samma ingrepp är upprepade mätningar av en storhet. Över åtgärdstyper
   > summeras bidragen mot `K = R × m_max`. Kravet att poster på samma åtgärdstyp delar sin
   > budgetandel uppfylls exakt: de delar typens plats i summan.

8. **Godkännandetestet för punkt 7, låst i förväg.** Bygget godkänns om **en tillagd post med
   belagd positiv effekt aldrig sänker något partis B**. Aldrig om rangordningen blev bättre, mer
   separerad eller mer stabil. Utfallet redovisas som det blir.

   > **Daterad not 2026-09-16, [ADR 0019](0019-kvoten-anvandes-over-fel-enheter.md) beslut 2
   > och 3.** Testet går inte att uppfylla som det är skrivet, och det beror inte på nämnaren.
   > Krympningen multiplicerar avståndet från neutral, så en positiv post kan sänka publicerat B
   > för ett parti vars `B_rått` ligger under neutral. Sex av 56 celler gör det. Mätt 2026-09-16:
   > en admitterad post med belagd positiv verkan sänker fyra partier utan position på den med
   > 0,075 till 0,150, helt genom täckningskanalen. Testet delas därför i evidensmonotonicitet,
   > med universum fixerat, och universumändring, som är ett versionsärende. Garantin gäller
   > `net` inom indikatorn ovillkorligt, `B_rått` bara vid oförändrat indikatormedlemskap, och
   > publicerat B inte alls.

## Vad beslutet inte rör

- **Den symmetriska evidensgrinden.** ADR 0006 står orörd, och de nio uteslutna posterna står kvar
  uteslutna.
- **`effect_strength`-tabellen 0,3 / 0,6 / 1,0.** ADR 0004 beslut 4 står. Den är dragen parameter i
  känslighetsanalysen och rörs inte av en formändring.
- **B:s vikt.** Kategoribetyget är oförändrat 0,30 A + 0,50 B + 0,20 D.
- **Täckningskrympningen.** Formen `2,5 + (rått - 2,5) × täckning` står orörd. Punkt 7 rör täljarens
  nämnare, inte krympningen.
- **Tomma undermått i täckningsnämnaren.** ADR 0011 punkt 9 äger det valet och prövas inte här.
- **Band, totalpoäng och rangordning.** Inte räknade, och inte del av något skäl ovan.

## Kända invändningar som inte åtgärdas här

Prövade under biljetten och nedskrivna så att de inte går förlorade. Ingen av dem följer av
enhällighet, och ingen avgörs av den här ADR:n.

1. **Poäng och täckning använder olika analysenheter.** Poängen väger evidensposter med `q`, medan
   täckningen räknar åtgärdstyper som mängd. Två poster på samma åtgärdstyp ändrar därför poängen
   men inte täckningen. Punkt 7 måste hantera det, eftersom budgeten delas per åtgärdstyp.
2. **Fyra admitterade poster saknar partipositioner** och sänker allas täckning utan att bidra till
   någon täljare.
3. **`mixed`, `unclear` och `unknown` ger `m = 0` men behåller full nämnarvikt.** Okänt behandlas
   därmed som belägg för exakt nolleffekt. ADR 0004 beslut 3 valde det medvetet för `mixed` och
   `unclear`; för `unknown` är det inte prövat.
4. **Beroende källor räknas som oberoende.** Flera poster om samma effekt kan få oproportionerlig
   vikt genom ren radmultiplicering.

## Följder

- Biljett #45 stängs med den här ADR:n.
- Punkt 7 ligger som biljett [#50](https://github.com/mcknschn/rosta/issues/50) under karta
  [#6](https://github.com/mcknschn/rosta/issues/6). Den avgör nämnarens form.
- Punkt 3 och 5 kräver ändrad text i `pipeline/scorerun.py` metodruta, som i dag säger att B mäter
  väntad storlek. Den ändringen rör dist och ligger i [#50](https://github.com/mcknschn/rosta/issues/50)
  eller en egen byggslice.
- Punkt 4 byggs i den här commiten, eftersom §5.2 är ren metodtext utan kodväg.
