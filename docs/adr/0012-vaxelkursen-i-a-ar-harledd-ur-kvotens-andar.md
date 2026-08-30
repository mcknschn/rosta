# ADR 0012: Växelkursen i A är härledd ur kvotens ändar

- Status: accepted
- Datum: 2026-08-30
- Beslutad i: biljett [#28](https://github.com/mcknschn/rosta/issues/28) under karta [#6](https://github.com/mcknschn/rosta/issues/6)
- Bygger på: [ADR 0003](0003-skiljbarhet-och-kanslighetsanalys.md), [ADR 0005](0005-a-forankras-i-tid-inte-i-faltet.md), [ADR 0007](0007-a-mats-over-samma-fonster-som-sin-forankring.md), [ADR 0009](0009-sakerheten-mater-hur-val-talet-ar-kant.md) och [ADR 0010](0010-ett-reglage-ar-en-vag-pipen-redan-kan-ga.md)

## Kontext

Biljett #28 graderades ur [#25](https://github.com/mcknschn/rosta/issues/25), som fann att A:s
tystnad har två orsaker och bara avgjorde den ena. En mätbar del satt i fönstret: a1:s täljare hade
tre budgetår mot en förankring på femton, och i alla tre stod M, KD, L och SD på samma ram. ADR 0007
rättade det, och [#27](https://github.com/mcknschn/rosta/issues/27) byggde rättningen 2026-08-26.

Kvar stod frågan som blir när rättningen är körd. **Är A fortfarande tyst när fönstren är lika?**

ADR 0007 punkt 7 strök biljettens eget prov, eftersom A per konstruktion är monoton i kvoten mellan
andelen och förankringen, så det provet aldrig kan falla. Frågan som ersatte det: hur stor
omfördelning krävs för att flytta A en poäng? I dag är svaret att en fördubblad andel ger 0,83
poäng. Talet ärvdes när ADR 0005 lånade B:s avbildning, och ingen hade beslutat att det är rätt
växelkurs.

ADR 0007 sparade dessutom ett alternativ utan att förkasta det: skala `q` mot förankringens egen
historiska spridning över fönstret. Reserven skulle prövas när fönstren blev lika, och den prövas
här.

## Diagnos

Talen är räknade 2026-08-30 ur `config/a_forankring.yaml`, `config/budget_ramar.yaml`, lagrets
`party_activity` och `dist/scores.json`, alltså underlaget efter #27 och
[#32](https://github.com/mcknschn/rosta/issues/32).

### 1. Kompressionen står kvar när fönstren är lika

Bygget i #27 mätte det redan: A:s realiserade intervall smalnade från 2,17-3,07 till 2,23-2,83, och
den viktade spridningen gick från 0,358 till 0,344. Rättningen gjorde alltså A **tystare**, inte
högre.

Mätt per cell ligger A mellan 2,229 och 2,831 över de 56 cellerna, med sd 0,131. Spannet per
kategori går från 0,120 (ekonomi) till 0,543 (klimat).

### 2. Halvorna lever på olika skalor

Medel av absolutbeloppet av `q` är **0,011 i a1** och **0,100 i a2**, alltså nio gånger. Största
enskilda avvikelse är SD i integration (a1, `q` = -0,113) och KD i försvar (a2, `q` = +0,329).

### 3. Partierna skiljer sig verkligt åt i a2, knappt alls i a1

Kvoten mellan det parti som betonar mest och det som betonar minst, uttryckt som andelen mot
förankringen:

| kategori | a1 | a2 |
| --- | --- | --- |
| ekonomi | 1,04 | 1,35 |
| välfärd | 1,02 | 1,63 |
| trygghet | 1,10 | 2,12 |
| försvar | 1,06 | **2,95** |
| klimat | 1,18 | 2,43 |
| integration | **1,30** | 1,55 |
| demokrati | 1,08 | 1,86 |

a1:s tystnad är alltså ett fynd om världen. De åtta föreslår ramar som ligger inom 30 procent av
varandra i den kategori där de skiljer sig mest, och inom 4 procent i ekonomi. a2 bär däremot
skillnader upp till nästan tre gånger.

### 4. Växelkursen i dag

För att flytta A **en poäng** krävs att andelen mot förankringen mångdubblas 2,33 gånger i båda
halvorna. Via a1 ensam krävs 5,0 gånger. Via a2 ensam går det inte alls, eftersom halvan väger 0,4
och `q` är mindre än 1 av konstruktion. Störst faktisk avvikelse, KD i försvar, ger A ett påslag på
0,33 poäng.

### 5. a1:s signal ligger under förankringens egen årsrörelse i varje kategori

Förankringens sd av `q` per år, mot medel av absolutbeloppet av `q` i a1:

| kategori | sd(`q` per år) | medel, a1 |
| --- | --- | --- |
| ekonomi | 0,033 | 0,005 |
| välfärd | 0,010 | 0,002 |
| trygghet | 0,045 | 0,012 |
| försvar | 0,084 | 0,008 |
| klimat | 0,051 | 0,018 |
| integration | 0,136 | 0,022 |
| demokrati | 0,030 | 0,008 |

Partiernas avstånd till förankringen är alltså mindre än förankringens avstånd till sig själv
mellan två år. Det gäller alla sju kategorier.

### 6. Förankringens spridning är till största delen trend, inte brus

Andelen av den beslutade ramen per år, i procent:

| kategori | 2011 | 2017 | 2021 | 2025 | restspridning efter borttagen trend |
| --- | --- | --- | --- | --- | --- |
| ekonomi | 28,09 | 25,41 | 23,93 | 23,22 | 0,016 |
| välfärd | 42,49 | 41,44 | 44,29 | 41,42 | 0,019 |
| trygghet | 4,53 | 4,37 | 4,84 | 6,02 | 0,056 |
| försvar | 7,72 | 7,17 | 8,28 | **13,47** | 0,127 |
| klimat | 4,29 | 4,49 | 5,48 | 5,12 | 0,048 |
| integration | 4,28 | **9,40** | 4,42 | 3,32 | 0,281 |
| demokrati | 4,82 | 4,66 | 4,90 | 4,11 | 0,058 |

Försvarets andel går upp 3,4 procent per år över fönstret och integrationens ned 2,7 procent per år
med en topp 2017. Storheten mäter alltså hur mycket budgetpolitiken faktiskt har ändrats, inte hur
väl ett tal är känt.

### 7. Reserven är i dag byggbar bara för a1, och statistikvalet avgör utfallet

a2:s förankring är ett enda aggregat över hela fönstret, femton utskottssummor utan uppdelning per
år. Det är samma underlagsfel som fällde fönstret som reglage i ADR 0010 punkt 6. Reserven går
alltså bara att räkna på a1, alltså på den halva som bär minst signal.

Räknad på a1 ensam, med tre lika rimliga mått på historisk spridning:

| skala | A-spann per kategori | klampade celler | rangordning |
| --- | --- | --- | --- |
| i dag | 0,120-0,543 | 0 | M > KD > L > C > S > MP > SD > V |
| sd(`q` per år) | 0,610-2,057 | 2 av 56 | oförändrad |
| medel per år | 0,657-2,097 | 2 av 56 | **KD > M**, resten oförändrad |
| max per år | 0,543-1,821 | 0 | oförändrad |

Skalan är alltså inte ett tal utan tre, och valet mellan dem flyttar de två översta partierna.

### 8. En årsserie för a2 är billigare än den ser ut

Täljaren per år finns redan på disk. `docs/done/a_forankring/fonster.json` bär motioner per parti,
utskott och år för 2008-2025, hämtade av `party_committee_counts` när fönstrets gränser prövades.
Bara kammarens årsvisa tal saknas, och `chamber_motions` i
`pipeline/tools/a_forankring_transcribe.py` gör redan slagningen per utskott över ett intervall.

En proxy räknad på de åtta partiernas poolade fördelning ger sd av `q` per år på 0,014 till 0,062,
alltså under a2:s partiavvikelser (0,044 till 0,179 i medel) i varje kategori. Reserven skulle
därför förstärka a2 och dämpa a1, om den byggdes symmetriskt.

Samma fil visar en andra sak. Ett partis **egen** årsvariation i a2-emfas ligger på 5 till 48
procent av dess eget medel, alltså i nivå med eller större än dess avstånd till kammaren. Det är en
egenskap hos världen och inte en osäkerhet om talet: A mäter femtonårsmedlet, och det talet är
räknat och fullständigt.

### 9. Skalans nåbara tak varierar mellan kategorier

`q` når +1 bara om förankringen är noll, så taket ligger på `(1 - förankring)/(1 + förankring)`.
Golvet 0,00 är däremot nåbart överallt: ett parti som inte skriver något alls i kategorin hamnar
där.

| kategori | a1-förankring | a2-förankring | nåbart A-tak |
| --- | --- | --- | --- |
| välfärd | 0,426 | 0,210 | **3,76** |
| ekonomi | 0,254 | 0,319 | 3,91 |
| försvar | 0,086 | 0,066 | 4,64 |
| integration | 0,052 | 0,121 | 4,64 |
| demokrati | 0,048 | 0,103 | 4,68 |
| klimat | 0,048 | 0,096 | 4,69 |
| trygghet | 0,049 | 0,086 | **4,70** |

Metodrutan säger redan att 5,00 aldrig nås. Den säger inte att taket skiljer sig mellan kategorier.
Ett parti som la hela sin kraft på välfärd skulle få 3,76, medan samma handling i trygghet ger 4,70.

## Beslut

1. **Domen: tystnaden är två olika saker, och ingen av dem är ett fel i formen.** I a1 är den ett
   fynd om världen, eftersom de åtta föreslår nästan samma fördelning (diagnos 3 och 5). I a2 är
   partierna verkligt olika, upp till nästan tre gånger, och avbildningen rapporterar den
   skillnaden som högst 0,53 poäng. Det smala intervallet följer av att ändpunkterna är absoluta,
   inte av att modellen tystar något.

2. **Växelkursen är avgjord och låst, och härledningen skrivs ned.** `q` ligger i [-1, 1] av
   konstruktion. Den linjära avbildningen på [0, 5] är den enda som lägger jämnhöjd i mitten utan
   att införa en konstant, och golvet betyder något verkligt: partiet lägger ingenting alls i
   kategorin. Avbildningen **sammanfaller** med B:s i stället för att vara lånad ur den. Meningen
   att talet 0,83 ärvdes utan att beslutas är därmed avförd ur #25 och #28.

3. **Reserven förkastas.** Tre skäl, vart och ett tillräckligt. Skalan är inte ett tal utan tre, och
   valet mellan dem flyttar rangordningen (diagnos 7). Yardsticken mäter hur mycket budgetpolitiken
   ändrats över femton år, inte hur väl talet är känt, så en avvikelse skulle räknas som mindre värd
   just i de kategorier där politiken rört sig mest (diagnos 6). Och den finns i dag bara för den
   halva som bär minst signal, så blandningen skulle addera ett skalat tal till en ren kvot
   (diagnos 7). Reserven är alltså **förkastad**, inte längre sparad.

4. **Takets snedhet är en deklarerad kostnad.** Det nåbara taket följer förankringens storlek och
   går 3,76 till 4,70 mellan kategorierna, medan golvet 0,00 är nåbart överallt. Kostnaden
   redovisas på samma sätt som ADR 0005 redovisade mättnaden, alltså att tre gånger förankringen
   ger 0,50. Den rättas inte, eftersom varje utjämning kräver en vald konstant per kategori.

5. **Metodrutan får en mening om taket.** Den säger i dag att 5,00 aldrig nås och lämnar läsaren med
   att skalan i övrigt är densamma överallt. Talet ska räknas ur förankringen i configen, aldrig
   skrivas in som konstant. Bygget är en egen slice.

6. **a2:s årsförankring är en egen fråga.** Diagnos 8 visar att den saknade årsserien är billig att
   bygga, men att bygga den byter ut det aggregat ADR 0005 valde som nollpunkt. Det är ett beslut
   och inte ett bygge, och det ligger som en egen biljett.

7. **Årsvariationen rör inte ADR 0009.** Att ett partis emfas svänger mellan år är ett besked om
   världen, inte om hur väl talet är känt. A behåller `high`, precis som ADR 0009 beslutade, och
   frågan ställs på nytt först om förankringen blir årsvis.

   > **Frågan stängd av [ADR 0013](0013-a2s-forankring-ar-en-poolad-andel.md) punkt 6, 2026-08-30**
   > (biljett [#36](https://github.com/mcknschn/rosta/issues/36)). Förankringen förblir en poolad
   > andel, så A behåller `high` och punkten ovan står. Villkoret är utskrivet i ADR 0013: svaret
   > hänger på formen, inte på lagringen. Byter någon till medlet av årsandelarna bär a2:s tunnaste
   > cell 1 motion i stället för 84, och då skattas något i A, så ADR 0009 punkt 5 måste prövas om.

8. **Blindheten deklareras.** Biljetten beordrade att reservens verkan skulle mätas före beslutet,
   som ADR 0006 mätte priset för utlyftet. Den som beslutade hade därför sett att en av tre
   skalvarianter sätter KD före M, och att alla tre vidgar A:s spann. Beslutet i punkt 3 är härlett
   ur vad storheten mäter och ur att skalan inte är unik, aldrig ur de talen. Deklarationen finns
   för att påståendet att jag höll mig objektiv är oprövbart när talen är kända, precis som ADR 0005
   punkt 8, ADR 0007 punkt 8 och ADR 0010 punkt 10 skrev samma sak om sig själva.

## Godkännandetest

Ett regeltest, aldrig ett tal om spridning eller rangordning. ADR 0003 punkt 1 förbjuder ökad
separation som mål.

1. **Kodtest:** metodrutans tak räknas ur förankringen som `(1 - förankring)/(1 + förankring)`
   avbildad med `net_support_to_score`, och ingen konstant skrivs in i texten. Ändras förankringen
   följer talet med.
2. **Betyg, band och rangordning står exakt still.** Slicen rör metatext och ingenting annat.
3. **Inget tal om spridning eller rangordning ingår i testet.**

## Övervägda alternativ

- **Skala `q` mot förankringens egen historiska spridning (reserven ur ADR 0007).** Förkastad på
  beslutspunkt 3. ADR 0007 skrev att konstanten skulle härledas ur samma fönster och samma källa som
  förankringen, alltså ingen vald konstant, och att A skulle bli jämförbar mellan kategorier. Båda
  leden faller. Konstanten är inte en utan tre, och A är redan enhetslös, så det reserven skulle
  tillföra är kalibrering mot hur mycket kategorin normalt rör sig.
- **Skala mot restspridningen efter borttagen trend.** Förkastad. Den möter invändningen i diagnos 6
  men gör konstanten mer vald och inte mindre: i ekonomi går skalan från 0,065 till 0,016, alltså
  fyra gånger, beroende på om en rät linje dras bort först.
- **Utjämna det nåbara taket mellan kategorier.** Förkastad på beslutspunkt 4. Varje utjämning
  kräver en vald konstant per kategori, och den enda vinsten är ett bredare spann, vilket ADR 0003
  punkt 1 förbjuder som mål.
- **Byta den begränsade kvoten mot en skillnad i procentenheter.** Förkastad. Formen är låst av
  ADR 0005 punkt 3, och att riva den kräver en annan karta med en annan destination. Måttet skulle
  dessutom göra välfärd och ekonomi till de enda kategorier som kan röra A alls, eftersom deras
  andelar är tio gånger de andras.
- **Flytta vikt från a1 till a2, eftersom a2 bär signalen.** Förkastad. Det är blandningens fråga
  och ligger i [#33](https://github.com/mcknschn/rosta/issues/33). Att avgöra den här skulle
  dessutom ske med talen i diagnos 2 och 3 kända, alltså inte blint mot rangordningen.
- **Hålla biljetten öppen tills a2 har en årsserie.** Förkastad. Växelkursen står på egna ben:
  härledningen i beslutspunkt 2 gäller oavsett hur förankringen är byggd, och en årsvis förankring
  ändrar vilka tal som matas in, inte vad en poäng betyder.

## Vad beslutet inte rör

- Blandningen 0,6 x a1 + 0,4 x a2. Den är [#33](https://github.com/mcknschn/rosta/issues/33):s
  fråga och rörs inte här.
- Vikterna 0,30 x A + 0,50 x B + 0,20 x D, C = 0 (ADR 0002).
- Den begränsade kvotens form (ADR 0005 punkt 3) och fönstren (ADR 0007).
- Grinden i `pipeline/budget.py` och villkorsklausulen (ADR 0007 punkt 4 och 5).
- A:s säkerhetsnivå (ADR 0009). Se beslutspunkt 7.
- `A_component_mix` och reglagens regel (ADR 0010).
- B, C och D. ADR 0004, ADR 0006, ADR 0008 och ADR 0011 står oförändrade.

## Följder

- **Bygget är en egen slice:** meningen i metodrutan ur beslutspunkt 5. Den kräver en omkörning av
  `scorerun`, eftersom metatexten ligger i `dist/scores.json`, men ingen omkörning av
  känslighetsanalysen, eftersom ingen delpoäng ändras.
- **Ordlistan §4.3 får Växelkurs**, i samma form som Reglage och Täckning fick.
- **Reserven är avförd ur ADR 0007:s Övervägda alternativ.** Den stod som sparad och prövas här.
  ADR 0007 får en not som pekar hit.
- **En biljett graderas ur beslutet:** ska a2:s förankring vara en årsserie?
- **En not till [#33](https://github.com/mcknschn/rosta/issues/33):** biljettens hål 1 håller inte
  längre. Påståendet att lagret inte kan pröva ADR 0001:s skäl gällde `party_activity`, som bär ett
  enda aggregat. `docs/done/a_forankring/fonster.json` bär motionerna per parti, utskott och år för
  2008-2025, så jämförelsen mellan ett partis regeringsår och dess oppositionsår går att köra på
  befintlig data.
- **Ingen kod och ingen config ändras i det här ärendet.** Rangordningen är oförändrad.
- **Ändrat i det här ärendet:** den här ADR:n, en not i ADR 0007 under Övervägda alternativ, och en
  rad i ordlistan §4.3.
