# ADR 0005: A förankras i tid, inte i fältet

- Status: accepted
- Datum: 2026-08-21
- Beslutad i: biljett [#19](https://github.com/mcknschn/rosta/issues/19) under karta [#6](https://github.com/mcknschn/rosta/issues/6)
- Bygger på: [ADR 0001](0001-a-mater-prioritering.md), [ADR 0002](0002-kategoripoangens-ansprak-och-vikter.md), [ADR 0003](0003-skiljbarhet-och-kanslighetsanalys.md) och [ADR 0004](0004-vad-delpoang-b-mater.md)

## Kontext

Biljett #19 graderades ur kartans dimma när #16 avgjorde att B:s mättnad var ett fel och inte ett
fynd. ADR 0003 punkt 3 i diagnosen hade mätt den viktade spridningen över de sju kategorierna:
A 7,76, B 6,24, D 1,34. A väger 0,30 men bar mest av separationen, och ADR 0001 låste A som
riktningsneutral. Biljetten kunde inte ställas förrän B-rättningen var körd, eftersom en rättad B
ändrar A:s relativa påverkan. Bygget levererades i [#17](https://github.com/mcknschn/rosta/issues/17)
den 2026-08-21.

## Diagnos

Mätt 2026-08-21 mot `dist/scores.json` efter #17, mot `config/` och mot `data/warehouse.duckdb`.
ADR 0003:s storhet reproducerades först exakt mot den gamla artefakten (commit `fa3ca36`), vilket
fastställer definitionen: vikt gånger (max minus min) över de åtta partierna, summerad över de sju
kategorierna.

1. **A bär mer av separationen nu än före.** A 7,76, B 3,54, D 1,34. Andelarna är 61,4, 28,0 och
   10,6 procent, mot 50,6, 40,7 och 8,7 procent före. A står exakt stilla kategori för kategori,
   eftersom ADR 0004 inte rörde A. Snittspridningen i kategoribetyget gick 1,248 till 1,112.

2. **A:s spridning beror inte på underlaget.** `A = 0,6 x rang(a1) + 0,4 x rang(a2)`
   (`pipeline/scorerun.py`). `rank_normalize` lägger alltid lägsta partiet på 0 och högsta på 5
   (`pipeline/score.py`). Talet 7,76 blir därför detsamma oavsett vad partierna föreslår. Under
   `minmax` blir det 8,18, alltså högre. Båda byggda metoderna är fältrelativa.

3. **Underlaget är nästan identiskt.** Kvoten mellan högsta och lägsta råa budgetandel per
   kategori: demokrati 1,04, ekonomi 1,05, välfärd 1,05, försvar 1,06, trygghet 1,09,
   integration 1,16, klimat 1,56. I demokrati skiljer 0,17 procentenheter de åtta partierna åt.

4. **a1 kan inte skilja fyra av åtta partier åt.** `config/budget_ramar.yaml` bygger varje ram som
   regeringens ram plus partiets avvikelse. M, KD och L pekar på `frame: regeringen`, och SD gör
   det också. a1 har därför fem unika värden av åtta i alla sju kategorier, med M, KD, L och SD
   permanent lika. I klimat skiljer 8,73e-06 S från blocket, och rangnormaliseringen gör om det
   till a1 = 0,00 mot 1,79, alltså 0,32 poäng av det färdiga kategoribetyget.

5. **a2 har samma defekt, en tiopotens mildare.** a2 ger åtta skilda värden i alla sju kategorier.
   Men minsta grannavstånd i klimat är 0,012 procentenheter och största 2,807. Rangen ger båda
   exakt 0,714 poäng.

6. **Normaliseringen är modellens största reglage.** Monte Carlo-körningen i
   [#20](https://github.com/mcknschn/rosta/issues/20) mäter varje källas ensamma påverkan på
   totalordningens stabilitet, med allt annat utmedelvärdat. `A_normalization` flyttar 10,13
   punkter, mest av samtliga 21 källor. `subscore_weights` flyttar 5,32. Modellens största reglage
   är alltså ett val mellan två lika oförankrade sträckningar av nästan lika tal.

## Beslut

1. **A är absolut, inte fältrelativt.** Beslutet är härlett ur ADR 0002 punkt 3, som ger A dess vikt
   med orden *"ett parti som lägger lite kraft på rätt åtgärd förbättrar något"*. "Lite kraft" är
   ett absolut påstående. Ett rangmått kan bara säga "minst kraft av de åtta". Härledningen som ger
   A dess vikt förutsätter alltså ett absolut A, och den byggda A:n är inte det. `scale_semantics` i
   `config/scoring.yaml` flyttar A från `relative` till `absolute`.

2. **Nollpunkten ligger i tid, inte tvärs partier.** Både a1 och a2 mäts mot hur stor andel
   kategorin normalt har fått under ett historiskt fönster. En nollpunkt räknad ur de åtta
   partiernas egna förslag förkastas, eftersom den behåller fältet som måttstock. Då förblir
   "alla åtta lägger lite kraft" osynligt, vilket är precis det anspråket i ADR 0002 punkt 1 kräver
   att betyget ska kunna säga.

3. **Formen är en begränsad kvot.** För varje parti och kategori gäller
   `q = (andel - förankring) / (andel + förankring)`. `q` ligger i [-1, 1] av konstruktion och är 0
   vid jämnhöjd. Betyget blir `score.net_support_to_score(q)`, alltså samma linjära avbildning som B
   redan använder. Ingen konstant väljs. Formen är hämtad ur koden, inte satt av den som beslutade.

4. **Blandningen står kvar.** a1 väger 0,6 och a2 0,4, oförändrat. Båda halvorna får samma form.
   Att blanda ett rangmått med ett kvotmått i en viktad summa vore ett formfel i sig, så en rättning
   av bara a1 lämnar A trasig på ett nytt sätt.

5. **a1:s förankring är den beslutade ramen.** Kategorins andel av de beslutade utgiftsramarna i
   bet. FiU1, som medel över fönstret. Regeringens förslag förkastas som förankring, eftersom det är
   ett blocks förslag varje enskilt år. Utfallet enligt årsredovisningen förkastas också: A frågar
   hur mycket kraft ett parti lägger och D frågar hur det gick, och gränsen mellan delpoängen går
   vid frågan (ADR 0001).

6. **a2:s förankring är kammarens fördelning.** Andelen av kammarens samtliga motioner som rör
   kategorin, hämtad ur samma endpoint som i dag men över fönstret. Kammarens fördelning över den
   period som redan ligger i lagret förkastas: den poolade kammaren är de åtta partierna, viktad
   efter hur många motioner var och en skriver, alltså samma fel som punkt 2 avvisar.

7. **Ett gemensamt fönster, satt av testbara gränser som skrivs före hämtningen.**
   - a1:s gräns: tidigaste budgetår vars FiU1-rambeslutstabell listar **samma 27 utgiftsområden med
     samma namn** som `mappings.expenditure_areas`.
   - a2:s gräns: tidigaste år där **alla åtta nuvarande partier** har motioner i varje utskott som
     mappningen använder.
   - Fönstret börjar vid den senare av de två gränserna och slutar vid senaste färdiga år.

   Båda gränserna är krav som faller ut, inte omdömen efter hämtningen. Ett efterhandsomdöme av
   typen "kvalitén var för dålig före år X" är otillåtet: ingen kan pröva det, och det går att fatta
   med kännedom om effekten.

   > **Förtydligad av [ADR 0007](0007-a-mats-over-samma-fonster-som-sin-forankring.md), 2026-08-21.**
   > Punkten säger inte om fönstret styr täljaren eller bara förankringen, och bygget i
   > [#21](https://github.com/mcknschn/rosta/issues/21) lade det på förankringen. ADR 0007 punkt 1
   > avgör att fönstret styr båda. ADR 0007 punkt 3 lägger dessutom a1 och a2 på var sitt fönster i
   > stället för ett gemensamt, och punkt 2 lägger till en tredje gräns för a1:s täljare. Texten
   > ovan står oförändrad.

8. **Blindheten deklareras.** Den som beslutade hade sett `source_influence` i
   `dist/robustness.json`, alltså att `rank` ger 89,04 i ordningsstabilitet och `minmax` 83,57.
   Punkt 3 väljer ingen av dem. Vad beslutet gör med A:s värden och med rangordningen räknades inte
   ut innan den här ADR:n skrevs. Deklarationen finns för att påståendet "jag höll mig objektiv" är
   oprövbart när talen är kända, precis som ADR 0003 skrev ut samma svaghet om sin egen diagnos.

## Övervägda alternativ

- **Flytta vikten 0,30.** Förkastat. Vikterna är låsta i ADR 0002, och att sänka A:s vikt därför att
  A separerar för mycket är precis den koppling mellan vikt och utfall som prövningsregeln i
  ADR 0003 punkt 1 förbjuder.
- **Byt `rank` mot `minmax`.** Förkastat. Båda är fältrelativa, och A:s viktade spridning blir 8,18
  under `minmax`, alltså högre. Bytet flyttar formen inom samma spann utan att röra felet.
- **Regeringens ram som nollpunkt.** Förkastat. Samma block styrde 2023, 2024 och 2025, så M, KD, L
  och SD skulle landa exakt på nollpunkten i varje kategori och varje år. Det bygger in en politisk
  nollpunkt i en riktningsneutral delpoäng.
- **De åtta partiernas medelandel som nollpunkt.** Förkastat på punkt 2.
- **Lika delning, en sjundedel, som nollpunkt för a2.** Förkastat. Kammarens egen fördelning går
  från 6,7 procent i försvar till 31,6 procent i ekonomi, alltså en faktor 4,7. Jämn delning
  beskriver ingenting.
- **Ta bort a2 och behålla a1.** Förkastat. a1 kan inte skilja M, KD, L och SD åt i någon kategori,
  så A skulle förlora förmågan att skilja fyra partier åt helt.
- **Linjärt i kvoten med tak vid 2,0, eller logaritmiskt.** Båda förkastade. Var och en kräver att
  den som beslutar sätter ett tal, och ett sådant tal går inte att motivera utan att se vad det gör.

## Vad beslutet inte rör

- Vikterna 0,30 x A + 0,50 x B + 0,20 x D, C = 0 (ADR 0002).
- a1-grinden i `pipeline/budget.py`. Den gäller partiramarna för de år som betygsätts, och de
  ligger redan i configen.
- B och D. ADR 0004 står oförändrad.
- `max_interval_halfwidth`. ADR 0003 punkt 1 förbjuder att sänka den som åtgärd.
- C:s rangnormalisering. Samma argument gäller ordagrant för C, men C väger 0 och saknar en naturlig
  medelmakt att förankra mot. Frågan får en egen biljett.
- **a1:s koalitionsdelade ram.** M, KD, L och SD föreslog faktiskt samma ram, och att de har samma
  budgetprioritering är ett korrekt påstående om verkligheten. Beslutet lämnar det orört. Felet
  uppstod först när normaliseraren blåste upp de mikroskopiska stegen mellan blocken till hela
  skalan. Begränsningen skrivs ut, den åtgärdas inte.

## Följder

- **Bygget är en egen slice**, som #17 var för ADR 0004. Den här ADR:n ändrar ingen kod och ingen
  config. Rangordningen är oförändrad tills slicen körs.
- **Ny hämtning krävs, men mindre än den ser ut.** a1 behöver en ram per historiskt år, den
  beslutade, inte åtta partiramar. a2 behöver poolade kategorisummor per period. Per-parti-data
  behövs en enda gång, för att avgöra fönstrets start enligt punkt 7. Dokument-id:na följer en
  obruten serie: `H601FiU1` (2018/19), `H901FiU1` (2021/22), `HA01FiU1` (2022/23),
  `HB01FiU1` (2023/24).
- **`scale_semantics` skrivs om** så att A står under `absolute`.
- **Kända kostnader, alla tre skrivna i förväg.** Den begränsade kvoten mättar mjukt, så ett parti
  som lägger tre gånger normen och ett som lägger fem gånger hamnar nära varandra. En historisk
  förankring bär strukturell drift, så alla åtta partier får högt A i försvar efter 2022. Det
  gemensamma fönstret i punkt 7 kastar sannolikt bort giltiga a1-år.
- **Om slicen inte hinner före valet** går sajten till val på formeln som ligger i config, enligt
  kartans stående regel. Nedsidan är att rättningen uteblir, aldrig att A blir halvbyggd.
