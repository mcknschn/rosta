# ADR 0016: Verklighetsbild avgörs av en förhandsregistrerad pilot

- Status: accepted
- Datum: 2026-09-13
- Beslutad i: biljett [#42](https://github.com/mcknschn/rosta/issues/42), medvetet utanför karta [#6](https://github.com/mcknschn/rosta/issues/6)
- Bygger på: [ADR 0002](0002-kategoripoangens-ansprak-och-vikter.md), [ADR 0003](0003-skiljbarhet-och-kanslighetsanalys.md), [ADR 0006](0006-evidensgrinden-ar-symmetrisk.md), [ADR 0008](0008-cellens-tackning.md) och [ADR 0011](0011-uteslutningen-ar-ett-eget-besked.md)

## Kontext

**Verklighetsbild** är arbetsnamnet på ett föreslaget mått som håller partiets egen beskrivning av
mandatperioden mot officiell statistik. Biljetten föreslog tre utfall per påstående: stämmer,
stämmer inte, skev.

Måttet föreslogs med vikt 0. Skälet står i biljetten och prövas inte om här: ett parti kan gå till
val på något skadligt, genomföra det perfekt och därmed förtjäna full poäng i ett mått som bara
frågar om beskrivningen var riktig. Ett välhållet skadligt löfte får aldrig höja en poäng som
påstår att kategorin förbättras (ADR 0002 punkt 1).

Underlaget ligger i `docs/valmanifest_2026/`, framställt 2026-09-13 ur de åtta partiernas
valmanifest: 230 mappade bakåtblickande poster, 666 bakåtblickande kandidater och 1 073
framåtblickande poster. De åtta PDF:erna ligger i samma katalog men utanför git.

Biljetten krävde att punkt 2, 3, 4 och 7 skulle avgöras i grillningen, eftersom de fyra bestämmer
vad som faktiskt mäts. Den skrev också att "vi bygger det inte" är en godkänd utgång.

Rekommendationen är framgrillad i tre turer mot en andra modell, som granskade metoden separat.
Den granskningen ändrade förslaget på två punkter, se beslutspunkt 2 och beslutspunkt 8.

## Diagnos

Mätt 2026-09-13 mot `docs/valmanifest_2026/`, `config/`, `pipeline/` och `web/`.

### 1. Ingen post bär en indikator, och täckningstalet i biljetten har inget spår

Alla tre filerna är punktlistor med parti, kategori och citat. Ett fält för indikator finns inte i
schemat. Det är alltså inte tomt, det saknas.

Biljettens punkt 9 skrev att ungefär en tredjedel av bakåtpåståendena namnger en indikator vi
redan hämtar, och kallade det ett stickprov ur de 230. Den handprövningen finns inte nedskriven
någonstans i repot. Talet går varken att granska eller räkna om. Överlappet mot de 43 inlästa
indikatorerna är därmed **okänt**, inte lågt.

### 2. Åtta procent av bakåtposterna bär ett tal

74 av 896. Mappade 15,7 procent, kandidater 5,7 procent. Per parti: MP 0 av 37, S 2 av 72,
KD 3 av 55, C 4 av 158, L 4 av 109, SD 11 av 71, V 11 av 94, M 39 av 300.

Ett tal krävs inte för att pröva ett påstående. `Klimatutsläppen har ökat` går att pröva. Men
fördelningen visar att materialet nästan alltid prövas på riktning och nästan aldrig på storlek,
och att två partier saknar kvantifierade påståenden helt eller nästan helt.

### 3. En femtedel av kandidaterna är rena faktapåståenden

Handklassning av 40 slumpdragna kandidater, 5 per parti, frö 20260913: 20 procent rena
faktapåståenden, 45 procent normativa hybrider av typen `för många elever lämnar skolan utan
fullständiga kunskaper`, 30 procent satser som kräver sin föregångare av typen `det gör oss
sårbara`, 5 procent regeringsgärningar av typen `vi har gjort det straffbart att`.

Maskinell kontroll mot alla 666 stöder storleksordningen. Biljettens punkt 2 rör alltså minst en
fjärdedel av materialet och inte en handfull specialfall.

### 4. Syskonjämförelsen saknar syskon i två tredjedelar av modellen

Bara 12 av 35 undermått har två eller fler **inlästa** indikatorer. 43 av 68 indikatorer läses in,
25 är allowlistade utan data. Hela kategorin demokrati har noll undermått med två inlästa
indikatorer.

Kodvärdet skev, som biljettens punkt 4 definierar som en syskonrörelse i samma undermått, är
därmed omöjligt att sätta i 23 av 35 undermått.

### 5. Kodvärdet skev blandar utfall med mätfel

Stämmer och stämmer inte avser överensstämmelse med en observation. Skev kan i biljettens lydelse
avse överdrift, fel indikator, selektiv tidsperiod, ofullständig kontext eller normativ inramning.
Det är fem olika saker under en etikett, och tre av dem är egenskaper hos mätningen och inte hos
påståendet.

### 6. Kodningen är gjord en gång, av en kodare, utan reliabilitetsmått

Korpusen är framställd i ett svep av en språkmodell. Det finns ingen andra kodare, inget
dubbelkodat urval och inget överensstämmelsemått. Ingen av biljettens tio punkter ställer den
frågan.

### 7. Serievalet är ett operationaliseringsfel och inte en tolkningstvist

M skriver att vårdköerna minskat 40 procent, och för talet 140 000 som väntat över 90 dagar 2022
mot 40 000 år 2025. Projektets indikator `vardkoer` är Kolada N79242, alltså **medianväntetid i
dagar**, 2021-2024, som går 65,0 till 64,0.

Det är två storheter och inte två mätningar av samma storhet. Biljettens punkt 6 föreslog regeln
att vi alltid läser projektets serie. Den regeln ger ett svar där det inte finns någon fråga.

### 8. Åttioåtta framåtposter faller utanför alla sju kategorier

8,2 procent av de framåtblickande. Innehållet är kultur, alkoholregler, civilsamhälle, idrott,
jakt, transport, landsbygdsservice, utrikespolitik och bistånd. Det är ett fynd om kategorimodellen
och inte om manifesten.

### 9. Tystnaden är belagd, men biljettens tal är fel

Biljetten skrev att V har noll poster i fem av sju kategorier. Det är **fyra** av sju. V har fyra
klimatposter, bland dem `Vb-004`, som biljetten själv citerar i stycket om utsläppskollisionen.
Trygghet, försvar, integration och demokrati står på noll.

Ordkontrollen mot källdokumentet står kvar: polis, Nato, migration, asyl och demokrati förekommer
noll gånger i V:s manifest. KD ligger på 0,9 procent i både försvar och demokrati bland sina
framåtposter.

### 10. Nollvikt har en fungerande förebild i produkten

Maktandelen väger 0 sedan ADR 0002 och visas ändå på fem ställen i `web/app.js`, varje gång med
texten att den inte ger poäng. En nollviktad sidoredovisning är alltså inte en teoretisk form i
det här repot.

## Beslut

1. **Analysenheten är relationen `utsaga x indikator x tidsperiod x operationalisering`.** En
   utsaga kan ge noll, en eller flera prövbara relationer. Detta ersätter biljettens punkt 2 och
   punkt 3. Varken meningen eller indikatorn duger ensam som enhet. Normativa led märks separat
   och sanningskodas aldrig mot statistik.

2. **Täckning och sanning är två redovisningar och blandas aldrig.** Matrisen parti x indikator
   redovisar täckning och tystnad. Tystnad är aldrig ett belägg för stämmer, stämmer inte eller
   skev, utan en egen kod. Bortfallskoderna är sju: ej prövbar normativ utsaga, otillräcklig
   kontext, ingen kompatibel indikator, data saknas, period saknas eller matchar inte, flera
   möjliga operationaliseringar, framtida utfall. De ligger utanför sanningens nämnare men kvar i
   täckningen.

   **Inga publicerade andelar i v0.** Antal per status plus hela bortfallsprofilen. Ska en andel
   någon gång publiceras måste både täljare och nämnare visas och en miniminivå för publicering
   vara satt i förväg. Skälet är att en andel med antalet skrivna meningar i nämnaren mäter
   dokumentlängd, och en andel med indikatorlistan i nämnaren mäter uppmärksamhet. Ingen av dem
   mäter riktighet.

3. **Källan bärs av ett hämtmanifest, inte av ett arkiv.** Korpusen blir en configfil med samma
   disciplin som projektets övriga transkriberade källor. Varje post bär stabilt utsage-id,
   dokument-id, ordagrant citat med bevarad kontext, sida, parti, kodningsdatum, kodboksversion
   och kodare. Per källdokument förs URL, hämtdatum, ursprungligt filnamn och SHA-256.

   PDF:erna stannar utanför git. Repot är publikt och dokumenten är upphovsrättsskyddade verk, och
   instrumentet behöver för sin prövning bara de citerade meningarna. **Begränsningen skrivs ut i
   klartext:** hashen styrker vilket dokument som lästes men återskapar det inte om URL:en dör. En
   arkivadress hos oberoende tredje part får läggas som frivilligt fält.

   Påstående, observation och indikator lagras som **tre skilda objekt**. Påståendet är textens
   utsaga, indikatorn är den på förhand definierade mätvariabeln, observationen är ett
   indikatorvärde för en viss period och population. Semantisk likhet räcker inte som koppling.
   Publicerade bedömningar är append-only.

4. **Framåthalvan lämnar instrumentet och fryses som egen prospektiv korpus.** De 1 073
   framåtblickande utsagorna går inte att pröva förrän perioden är slut. Ett rent uteslutande
   räcker inte, eftersom det öppnar för efterhandsval av formulering, indikator och tröskel.
   Materialet fryses därför nu med dokumenthashar, fasta utsage-id, oföränderlig originaltext och
   en nedskriven brytpunkt. Indikatorval förhandsregistreras bara där utsagan bär en storhet och
   en period. Originalregistret anpassas aldrig när utfallet blivit känt.

5. **Instrumentet är modellkodat och säger det om sig självt.** Två språkmodeller från olika
   leverantörer kodar var för sig, med den låsta kodboken som enda gemensamma indata och utan
   tillgång till varandras svar. Krippendorffs alfa redovisas separat för avgränsning, prövbarhet,
   indikatorval och kodvärde, med förväxlingsmatris. Tröskel och förfarande vid oenighet bestäms
   före kodningen.

   Ett slumpmässigt och blindat delurval kodas dessutom av projektägaren och redovisas som ett
   eget parvist överensstämmelsemått mot vardera modellen. Det är inte ett facit, det validerar
   ingenting och får inte beskrivas som riktighet. **Begränsningen skrivs i metodrutan:**
   instrumentet gör inget anspråk på mänsklig interkodarreliabilitet, eftersom projektet saknar en
   andra mänsklig kodare, och systematiska fel som två modeller delar går inte att upptäcka med
   denna uppställning.

6. **Beslutet nu gäller en förhandsregistrerad pilot, inte ett bygge.** Ingen har mätt hur många
   prövbara relationer materialet bär, och det talet avgör hela frågan. Piloten omfattar 200
   utsagor, 25 per parti, dragna utan återläggning ur bakåtmaterialet. Redovisning per parti.
   Totalskattning med designvikter. Ändlighetskorrektion där urvalsandelen är stor, vilket den
   blir för MP och KD.

   **Pilotkodboken låses före kodningen** och innehåller regler för atomisering, prövbarhet,
   bortfallskoder, tidsperiod, indikatormatchning och operationalisering. Den kan inte begränsas
   till prövbarhet och bortfall, eftersom tröskeln gäller relationer och inte utsagor. Slutliga
   kodvärden och produktionskodboken skrivs först om tröskeln klaras.

7. **Tröskeln sätts före kodningen och ändras inte efteråt.**

   1. Designviktat totalt utbyte minst 20 procent av de 200 kodade utsagorna.
   2. Minst 5 prövbara relationer för vart och ett av de åtta partierna.
   3. Ger ett parti 0 till 2 relationer faller per-parti-redovisningen.
   4. Ger ett parti 3 eller 4 relationer totalundersöks det partiets material innan beslut. Kravet
      på minst 5 står kvar efter utökningen.
   5. Punktskattningar, partiresultat och osäkerhetsintervall redovisas oavsett om tröskeln nås.

   Talet 20 procent är en miniminivå för användbarhet och inte ett statistiskt belagt
   populationsvärde. Det är härlett ur diagnosens punkt 3. Kravet på minst 5 relationer hos
   **samtliga** åtta partier gör den samlade regeln strängare än totalgränsen ensam.

8. **Kategorispridningen är diagnostisk, aldrig en stoppregel.** Antalet representerade kategorier
   per parti skrivs ut, utan tröskel och utan omdöme. Skälet är projektets eget prejudikat:
   ADR 0008 punkt 7 gav Täckningen noll verkan på betyget, och ADR 0011 punkt 9 lät ett uteslutet
   undermått ligga kvar i täckningens nämnare och räknas noll täckt, för att hålet skulle synas.
   Att stoppa en smal men sann redovisning vore att dölja hålet. Samma regel binder ADR 0003
   punkt 3 och ADR 0008 punkt 6.

9. **Kodvärdet skev är förkastat i sin nuvarande form.** Diagnosens punkt 5 visar att etiketten
   blandar utfall med mätfel, och punkt 4 att jämförelsen är omöjlig i 23 av 35 undermått. En
   ersättande regel, som gör de tre kodvärdena ömsesidigt uteslutande och reproducerbara, skrivs i
   produktionskodboken och alltså bara om piloten klaras.

   Biljetten krävde att punkt 4 skulle avgöras i grillningen. Det gick inte. Skälet är att en
   beslutsregel för tre kodvärden inte går att skriva innan utbytet är mätt, och att den
   syskonstruktur regeln förutsätter saknas i två tredjedelar av modellen.

10. **Operationaliseringen avgör, inte vems serie som vinner.** Biljettens punkt 6 är besvarad
    genom beslutspunkt 1. Är partiets storhet oförenlig med indikatorns finns ingen relation, och
    utfallet blir bortfallskoden ingen kompatibel indikator eller flera möjliga operationaliseringar.
    Vårdköfallet i diagnosens punkt 7 är alltså inte ett fall där vår serie vinner över partiets.
    Det är ett fall utan prövbar relation.

11. **Faller tröskeln avslutas arbetet med ett skrivet avslagsskäl.** Materialet ligger kvar.
    Det är en godkänd utgång, på samma sätt som den viktade stansen prövades och förkastades
    2026-06-07.

## Godkännandetest

Tio regler, alla regeltester. Ingen regel nämner hur många påståenden som visade sig felaktiga,
och ingen regel nämner ett parti.

1. Kodboken är låst och versionsmärkt före den första kodade utsagan. Ordningen går att se på
   commit-datum.
2. Urvalsdragningen är reproducerbar. Frö och metod står i filen.
3. Ingen fil i piloten bär en sanningsandel per parti.
4. Varje kodad utsaga bär antingen minst en relation eller exakt en bortfallskod ur den låsta
   listan om sju.
5. Tröskelvärdena i beslutspunkt 7 står nedskrivna före kodningen och är oförändrade efteråt.
6. Två modellkodningar finns, från olika leverantörer, och ingen av dem har sett den andras svar.
7. Alfa redovisas för alla fyra momenten, med förväxlingsmatris.
8. Ingen text och inget test framställer projektägarens delurval som facit, validering eller
   riktighet.
9. Den frysta framåtkorpusen bär dokumenthash, fasta utsage-id och en nedskriven brytpunkt.
10. Klaras inte tröskeln finns ett daterat avslagsskäl i repot, och ingen kodning fortsätter.

## Övervägda alternativ

- **Nämnaren är partiets egna påståenden.** Förkastat. Nämnaren ligger då utanför instrumentets
  kontroll. Dokumenten skiljer sig med faktor 8,4 i längd, och två partier har noll eller nästan
  noll kvantifierade påståenden. En andel räknad på 0 till 4 observationer är brus, och ett
  brustal bredvid ett betyg är värre än inget tal.

- **Nämnaren är de 43 inlästa indikatorerna.** Förkastat som sanningsnämnare. Den matrisen mäter
  täckning och uppmärksamhet, inte andelen riktiga påståenden. Den behålls för just det, se
  beslutspunkt 2. Detta var förslaget i grillningens första runda, och den andra modellens
  invändning fällde det.

- **PDF:erna in i versionshanteringen.** Förkastat. Repot är publikt, och att lägga hela
  dokumenten där är en spridningshandling och inte en citathandling. Storleken, 18,4 MB, är ett
  underordnat skäl.

- **Kräva en återskapbar arkivkopia innan instrumentet får byggas.** Förkastat. Projektet har
  varken rätt eller praktisk möjlighet att långtidsarkivera fullständiga källdokument. Den
  begränsningen skrivs ut i stället, se beslutspunkt 3.

- **Bygga framåthalvan och låta den ligga oanvänd.** Förkastat. Varje designfråga skulle då
  besvaras två gånger, och den andra halvans svar kan ingen pröva förrän perioden är slut.

- **En minimal pilotkodbok som bara definierar prövbarhet och bortfall.** Förkastat. Den kan
  skatta antalet kandidatutsagor men inte utbytet av relationer, och det är relationerna tröskeln
  gäller. Detta var också ett förslag som den andra modellens invändning fällde.

- **Kategorispridningen som stoppregel.** Förkastat på prejudikatet i beslutspunkt 8.

- **Projektägarens kodning som facit.** Förkastat. En människa som kodar två gånger mäter
  intrakodarreliabilitet, och en människa mot två modeller är ingen validering. Måttet redovisas,
  men anspråket får inte ställas.

- **Delpoäng E med vikt.** Inte prövat här. Biljettens avgränsning håller: vikterna är låsta av
  ADR 0002, och att ge måttet vikt kräver att anspråket i ADR 0002 skrivs om först.

## Vad beslutet inte rör

- **Vikterna 0,30 x A + 0,50 x B + 0,20 x D, C = 0** (ADR 0002). Verklighetsbild har vikt 0 och
  ingår inte i någon poäng, något band eller någon rangordning.
- **Riktningsblindheten** (ADR 0006). Måttet ska träffa den som skönmålar sin egen period och den
  som svartmålar någon annans lika hårt.
- **Uteslutningarna** (ADR 0011). Biljettens punkt 5 är inte prövad, se Följder.
- **Partiprogram.** Avfört i biljetten. Endast valmanifest.
- **Partiernas innehåll.** Spaltbrytningar är lagade, egna stavfel står kvar. Dokumentet som det
  publicerades är dokumentet.
- **De 68 indikatorerna och deras riktning.** Frågan om målintervall ligger i biljett
  [#4](https://github.com/mcknschn/rosta/issues/4).

## Följder

- **Biljett [#42](https://github.com/mcknschn/rosta/issues/42) stängs med detta beslut.** En
  pilotbiljett graderas. Den bär kodboken, urvalet, de två modellkodningarna, delurvalet och
  tröskelprövningen.
- **En egen karta graderas bara om piloten klaras.** Verklighetsbild är ingen delpoäng och ligger
  utanför karta #6, på samma sätt som biljett [#5](https://github.com/mcknschn/rosta/issues/5)
  föreslår en egen karta för D:s kausala försiktighet.
- **`.gitignore` får en rad** som håller `docs/valmanifest_2026/*.pdf` utanför
  versionshanteringen. Beslutspunkt 3 blir annars beroende av att ingen råkar committa dem.
- **Biljettens punkt 5 står öppen.** Frågan är om påståenden om `inflation` och
  `statsskuld_underskott` får prövas, givet att Verklighetsbild inte tillskriver något och att
  neutralitetsfelet gäller riktning och inte sanning. Den prövas i pilotbiljetten, eftersom
  kodboken måste svara på den innan en utsaga om de två indikatorerna kan kodas.
- **Biljettens punkt 9 avgörs delvis av piloten.** Utbytet visar hur stort hålet är, och först
  därefter är ett beslut om nya källor meningsfullt. En ny indikator med data kräver alltid en
  kodändring, minst en rad i `pipeline/build_fas2.py`.
- **Biljettens punkt 10 faller av sig själv.** De 88 posterna utanför kategorierna har ingen
  indikator och ger därför ingen relation. De syns i bortfallet.
- **Biljettens punkt 8 faller bort.** Skillnaden mellan att styra och att vara i opposition gällde
  bara framåthalvan, och den lämnar instrumentet i beslutspunkt 4.
- **En rättelse förs in i biljetten.** V har noll poster i fyra kategorier, inte fem. Se
  diagnosens punkt 9.
- **Ingenting i pipen, configen eller gränssnittet ändras av detta beslut.** Inga betyg rör sig,
  och `dist/` är orört.
