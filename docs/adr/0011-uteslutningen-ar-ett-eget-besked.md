# ADR 0011: Uteslutningen är ett eget besked, inte en riktning

- Status: accepted
- Datum: 2026-08-26
- Beslutad i: biljett [#13](https://github.com/mcknschn/rosta/issues/13) under karta [#6](https://github.com/mcknschn/rosta/issues/6)
- Bygger på: [ADR 0001](0001-a-mater-prioritering.md), [ADR 0002](0002-kategoripoangens-ansprak-och-vikter.md), [ADR 0006](0006-evidensgrinden-ar-symmetrisk.md), [ADR 0008](0008-cellens-tackning.md) och [ADR 0009](0009-sakerheten-mater-hur-val-talet-ar-kant.md)

## Kontext

Biljett #13 kom ur [#1](https://github.com/mcknschn/rosta/issues/1) punkt 8. Den sade att varje
indikator i dag har en riktning, `up` eller `down`, och att modellen därmed antar att mer eller
mindre alltid är bättre. För en del mått håller det inte. Låg arbetslöshet är objektivt bra.
Inflation har en officiell målnivå på 2 procent, alltså är varken högre eller lägre alltid bättre.
Biljetten frågade om modellen behöver målintervall som komplement till monoton riktning, och vilken
regel som avgör när en indikator får ett.

Premissen höll inte. `config/categories.yaml` bär redan ett tredje värde, och `pipeline/config.py`
godkänner det. Värdet heter `target`, och ordlistan §4.3 rad 3b kallar det "målnivå". Ingen målnivå
är däremot nedskriven någonstans i repot.

Frågan gick alltså inte att svara på som den stod. Under den låg en annan fråga: vad betyder det
tredje värdet i dag, och vad borde det betyda? Den här ADR:n avgör den regeln. Målintervallen
följer sedan ur regeln, eller följer inte alls.

## Diagnos

### 1. Det tredje värdet finns, men betyder inte målnivå

`pipeline/config.py:198` godkänner `{"up", "down", "target"}`. Av 68 indikatorer står 38 på `up`,
27 på `down` och 3 på `target`. De tre är `inflation`, `statsskuld_underskott` och
`forsvarsanslag_andel_bnp`, alltså exakt biljettens tre exempel.

Vad `target` gör står i klartext i koden. `pipeline/score.py:274` säger
`return None  # target: ingen mållnivå -> ej poängsättbar i D`, och `DATA.md` upprepar det.
Ordet betyder alltså **hoppas över**, inte **har en målnivå**. Ingen av de tre bär ett tal.

### 2. De tre är helt overksamma

Lagrets tabell `observations` har noll rader för alla tre. Evidensliggaren har noll poster för alla
tre. De matar därför varken B eller D. De syns ingenstans i `dist/scores.json` utom som
undermåttsnamn i kategorilistan, och `web/app.js` läser aldrig undermått. För användaren finns de
alltså inte.

### 3. Etiketten kostar kategorivikt, och hålet syns inte

`pipeline/scorerun.py:319` tar bort target-only-undermått ur den nämnare B och D delar. Ett
undermått är target-only när det har minst en indikator och alla dess indikatorer står på `target`.
I ekonomi gäller det `inflation_prisstabilitet` (vikt 12) och `offentliga_finanser` (vikt 15),
alltså **27 av 100**. Ekonomins nämnare är 73.

Ekonomi är den enda kategorin med target-only-undermått. Försvarets `ekonomisk_ambition` överlever
bara för att syskonindikatorn `forsvarsfinansiering_upptrappning_mot_mal` bär riktning `up`.

Efter [ADR 0008](0008-cellens-tackning.md) räknas Täckning över samma nämnare. Ett bortstruket
undermått sänker därför inget täckningstal. Ekonomi visar 0,877 i täckning för sju partier och
0,677 för V, samtidigt som 27 procent av kategorianspråket inte är med. Ekonomi är därmed
kategorin med **högst** redovisad täckning.

### 4. De tre står där av tre olika fel

`docs/done/evidens_trovardighet.md` §4.3 har redan skrivit skälen, ett per indikator, och inget av
dem är "vi saknar en målnivå":

- `inflation`: "Riksbanksstyrt".
- `offentliga_finanser`: "åtstramnings-tilt + dubbelräkning mot A/c2 - directional konvertering
  avvisad".
- `forsvarsanslag_andel_bnp`: liggarens FöU2-not säger "EJ budgetmagnitud (delpoäng
  A/a1-dubbelräkning)" och "behålls som kontext".

Det är tre olika fel. Att indikatorn inte är partistyrbar är ett **giltighetsfel** i ADR 0009:s
mening. Att frågan redan ägs av en annan delpoäng är ett brott mot ADR 0001:s regel att gränsen
mellan delpoängen går vid frågan. Bara det mellersta felet handlar om riktning.

Ett ord som bär tre fel läses som ett fel. Det är därför biljetten bad om målintervall när ingen av
de tre saknade en nivå.

### 5. Inflation klarar en målnivå-prövning och utesluts ändå

Provet har två steg. *Är preferensen enkeltoppig?* Ja för alla tre. Deflation är inte bättre än 2
procent. *Finns en beslutad nivå ur officiell källa som inte i sig är en partiståndpunkt?*

- `inflation`: **ja**. Riksbankens 2 procent, satt under eget lagmandat, och inget riksdagsparti
  driver en annan nivå.
- `statsskuld_underskott`: **nej**. Skuldankaret och överskottsmålet är precis vad partierna tvistar
  om.
- `forsvarsanslag_andel_bnp`: **nej**. Den beslutade nivån är ett golv, och ambitionen ovanför är
  omtvistad.

Inflation är alltså den enda av de tre som en målnivå faktiskt skulle lösa, och den utesluts ändå,
på ett skäl som inte har med riktning att göra. Det är beviset för att målintervallen aldrig var
frågan.

Halva den gamla invändningen mot `offentliga_finanser` har dessutom fallit av sig själv.
"Dubbelräkning mot A/c2" pekade på C:s finansieringskomponent c2, som är uppskjuten sedan Fas 1c,
och C väger 0 sedan ADR 0002. Kvar står bara neutralitetsdelen.

### 6. Ett hål i B som ett syskon råkar täppa

`config/claims.yaml:20` definierar Verkan "relativt indikatorns positiva riktning". En indikator
utan positiv riktning gör fältet odefinierat. Spärren finns ändå bara för target-only-undermått: en
post mot `inflation` ignoreras av B5-spec §3.6, men `forsvarsanslag_andel_bnp` ligger i ett
undermått med en `up`-syskonindikator, så undermåttet ligger innanför nämnaren. En post där skulle
gå rakt in i B. `pipeline/score.py:118` filtrerar inte på riktning, och `pipeline/scorerun.py:798`
delar ut undermåttsvikten utan att fråga.

I dag pekar noll poster dit, så hålet är otrampat. De två utfallen, tyst ignorerad respektive tyst
poängsatt, beror alltså på om ett syskon råkar bära riktning. Det är en form och inte ett beslut.

### 7. Täckningens nämnare är också krympningens nämnare

`pipeline/scorerun.py:804` krymper B mot neutral med variabeln `coverage`, och rad 818 rapporterar
**samma** variabel som B:s täckning. D har samma koppling på rad 509. Att flytta den delade
nämnaren från 73 till 100 skulle därför flytta betygen, inte bara redovisningen.

Ett undantag finns redan i koden. `pipeline/scorerun.py:853` räknar D:s täckta vikt på kategorins
egen nämnare även när D är ej tillämplig, med noten att nämnaren aldrig krymper och att talet
"rör inte betyget". Täckning redovisar alltså redan ett hål som betyget inte känner.

## Beslut

1. **Nej, modellen behöver inga målintervall i dag.** Frågan har noll medlemmar: den enda
   indikator som klarar målnivå-provet utesluts på ett annat fel (diagnos 5). Ingen mekanism för
   avstånd till en nivå byggs, av samma skäl som [ADR 0010](0010-ett-reglage-ar-en-vag-pipen-redan-kan-ga.md)
   punkt 3 ger: ett dokumenterat men obyggt alternativ är inget alternativ. Regeln i punkt 2 säger
   när frågan ska ställas igen.

2. **Regeln.** Varje indikator prövas i tre steg, i den här ordningen. Det första steg som fäller
   indikatorn ger dess Uteslutningsskäl.

   1. **Gränsprovet** (ADR 0001). Svarar indikatorn på en fråga som en annan delpoäng redan äger?
      Ja → `gransfel`.
   2. **Giltighetsprovet** (ADR 0009). Kan utfallet tillskrivas ett parti? Nej → `giltighetsfel`.
   3. **Riktningsprovet.** Kan det bättre hållet anges ur officiell källa utan att ta ett partis
      parti? Nej → `neutralitetsfel`. Ja och preferensen är monoton → `up` eller `down`. Ja och
      preferensen är enkeltoppig med en beslutad nivå som inget parti driver bort ifrån →
      indikatorn är godtagbar i princip, men mekanismen är inte byggd, och att bygga den är ett
      eget beslut.

   Ordningen är inte godtycklig. Ett gränsfel gör de två senare proven meningslösa, eftersom
   indikatorn inte hör hemma i delpoängen alls. Ett giltighetsfel gör riktningsprovet meningslöst,
   eftersom en riktning ingen kan tillskrivas ett parti inte hjälper någon.

3. **Riktningen håller bara `up` och `down`.** Värdet `target` förs av. Riktning är ett besked om
   indikatorn, alltså vilket håll som är bättre. Uteslutningen är ett besked om modellen, alltså
   varför indikatorn inte poängsätts. Ett fält kan inte bära båda utan att det ena döljer det
   andra, vilket diagnos 4 visar att det gjorde.

4. **Uteslutningen får ett eget fält som är sitt eget skäl.** Fältet heter `exclusion` och den
   kanoniska storheten heter **Uteslutningsskäl**. Finns fältet är indikatorn utesluten, och värdet
   namnger felet. Saknas fältet krävs `direction`. Formen gör "utesluten utan skäl" omöjlig att
   skriva, vilket är precis det tillstånd de tre indikatorerna befinner sig i i dag. En flagga plus
   en fritextnot förkastas, eftersom den formen tillåter det tillståndet.

5. **Tre värden, vart och ett förankrat i en beslutad regel.** `gransfel` (ADR 0001),
   `giltighetsfel` (ADR 0009) och `neutralitetsfel` (CLAUDE.md:s neutralitetskrav). Namnen pekar
   på regeln och inte på symtomet i det enskilda fallet, så de går att återanvända på nästa
   indikator. Klarspråksförklaringen, till exempel "dubbelräkning mot A", står i notraden.

6. **De tre proven.** Regeln körs på de tre indikatorer som bär `target` i dag. De faller på tre
   olika steg, i ordning, vilket är vad som gör regeln prövad.

   | Indikator | Faller på | Skäl |
   |---|---|---|
   | `forsvarsanslag_andel_bnp` | steg 1 | Talet är anslagets storlek. Hur mycket kraft ett parti lägger på försvar är A:s fråga, mätt som andel av föreslagna anslag. Liggarens FöU2-not sade redan detta. |
   | `inflation` | steg 2 | Penningpolitiken är Riksbankens under eget lagmandat. Utfallet kan inte tillskrivas ett riksdagsparti. Indikatorn klarar steg 3, vilket är utan verkan här. |
   | `statsskuld_underskott` | steg 3 | Preferensen är enkeltoppig, och den bättre nivån är skuldankaret. Nivån är i sig en partiståndpunkt, så en riktning skulle privilegiera åtstramning. |

   `neutralitetsfel` får därmed **en enda medlem av 68**. Det är inte ett argument mot regeln. En
   regel som släpper igenom en indikator har mätt något. En regel som släpper igenom tre för tre
   olika skäl har inte det.

7. **En utesluten indikator får inte bära en evidenspost.** Pipen ska säga ifrån i
   config-valideringen, inte tyst räkna och inte tyst ignorera. Grinden går på uteslutningsfältet
   och aldrig på om ett syskon råkar bära riktning, vilket är hålet i diagnos 6.

8. **Varje utesluten indikator bär ett återöppningsvillkor.** Villkoret säger vad som måste ändras
   för att felet ska vara borta, och det ska gå att pröva. Repot gör redan så för HOLD-väggarna
   `segregation`, `normer_tillit` och `leveranstid_materiel`. De tre målnivå-indikatorerna står i
   dag som "behålls som kontext", utan slut. Ett villkor som i praktiken aldrig kan fyras är ändå
   bättre än inget, eftersom det namnger vad som skulle behöva ändras.

9. **Täckning får en egen nämnare. Krympningen står kvar.** Täckning räknas över kategorins **fulla**
   undermåttsvikt, och ett uteslutet undermått räknas 0 täckt i stället för att strykas ur nämnaren.
   B:s och D:s krympning mot neutral behåller den nämnare de har i dag.

   Regeln är ADR 0008 punkt 4:s egen, tillämpad på ett hål till: ej tillämplig D räknas som 0 täckt,
   "aldrig bort ur nämnaren". Precedensen står i koden, i `pipeline/scorerun.py:853`.

   Sakskälet mot att i stället flytta den delade nämnaren: B krymper mot neutral därför att en
   saknad ståndpunkt betyder "vet ej". För statsskulden saknar vi ingen ståndpunkt. Vi vägrar
   poängsätta den. Att krympa alla åtta partiers B för vår egen modellgräns säger ingenting om
   något parti, och det skulle flytta betygen (se punkt 12).

   **ADR 0008 punkt 5 ändras.** Den låser att B:s täckning är samma tal som `B_coverage`-flaggan
   bär. Den identiteten skrevs när det bara fanns en nämnare, och upphör här.

10. **Metodrutan namnger de uteslutna indikatorerna och skälet för var och en.** Ekonomins Täckning
    sjunker synligt av punkt 9, och ett sjunkande tal utan förklaring inbjuder till fel slutsats,
    nämligen att ekonomidata blivit sämre. Ett samlingsord räcker inte, eftersom hela beslutet är
    att de tre felen är olika. Kortets framsida rörs inte och ägs av
    [#11](https://github.com/mcknschn/rosta/issues/11).

11. **Ordlistan.** **Uteslutningsskäl** blir kanoniskt namn med sina tre värden. Riktningens rad
    3b tappar "målnivå (`target`)" och håller upp och ned. En kollision skrivs ut: `coverage_exclude`
    i `config/scoring.yaml` utesluter **åtgärdstyper** ur B:s nämnare, alltså ett annat objekt och
    en annan mekanism. Liggarens `admitted` återanvänds inte, eftersom det ordet bär ADR 0006:s
    symmetriska evidensgrind och en andra betydelse skulle göra frågan "varför är den inte
    admitted" tvetydig. Det är ADR 0010:s lärdom om ordet *källa*.

12. **Blindheten deklareras.** Under biljetten mättes vad det förkastade alternativet i punkt 9
    skulle kosta: ekonomibetygen rör sig -0,151 (MP) till +0,065 (V), sju partier ned och V upp,
    med inbördes ordning inom ekonomi oförändrad i den körningen. Talen räknades fram för att rätta
    ett faktafel i biljettens eget underlag, alltså påståendet att ändringen vore rankingneutral.
    Regeln i punkt 2 och valet i punkt 9 är härledda ur ADR 0008 punkt 4 och ur vad krympningen
    betyder, aldrig ur de talen. Deklarationen finns för att påståendet "jag höll mig objektiv" är
    oprövbart när talen är kända, precis som ADR 0005 punkt 8, ADR 0007 punkt 8 och ADR 0010
    punkt 10 skrev samma sak om sig själva.

## Godkännandetest

Ett regeltest, aldrig ett tal om hur hög täckningen blev. Ett tal om täckningen vore ett
täckningsmål, och det förbjuder ADR 0006:s godkännandetest av samma skäl.

1. **`direction` godkänner bara `up` och `down`.** Ett tredje värde faller i config-valideringen.
2. **Varje indikator bär antingen en Riktning eller ett Uteslutningsskäl, aldrig båda och aldrig
   ingetdera.**
3. **Varje Uteslutningsskäl är ett av de tre värdena**, och varje utesluten indikator bär ett
   återöppningsvillkor.
4. **En liggarpost mot en utesluten indikator hard-failar**, oavsett vad dess syskonindikatorer bär.
5. **Betyg, band och rangordning står exakt still.** Bara Täckning rör sig, och bara i ekonomi,
   eftersom ekonomi är den enda kategorin där alla indikatorer i ett undermått är uteslutna.
6. **Inget tal om täckningens nivå, spridning eller rangordning ingår i testet.**

## Övervägda alternativ

- **Bygga poängsättning mot en målnivå.** Förkastat på beslutspunkt 1. Frågan har noll medlemmar,
  och en mekanism utan medlem är den sorts obyggda alternativ ADR 0010 punkt 3 avvisar. Regeln
  namnger tröskeln för när frågan ska ställas igen, och [#4](https://github.com/mcknschn/rosta/issues/4)
  kommer att pröva den mot 68 indikatorer.
- **Behålla `target` som tredje riktningsvärde och bara lägga till ett skälfält.** Förkastat på
  beslutspunkt 3. Då bär fältet fortfarande två besked, och riktningsfrågan står kvar i configen
  även när ingen indikator faller på den.
- **Flytta den delade nämnaren till 100, så att B och D krymper mot neutral för uteslutna
  undermått.** Förkastat på beslutspunkt 9. Krympningen betyder "vet ej", och ett uteslutet
  undermått är inte "vet ej" utan "går inte att fråga". Alternativet flyttar dessutom betygen, och
  en redovisningsfråga får inte flytta betyget.
- **Låta allt stå och skriva skälet bara i metodrutan.** Förkastat på beslutspunkt 9. Täckning är
  det enda tal appen visar per cell, och där syns hålet inte alls.
- **Återanvända liggarens `admitted: false` plus `admission_note`.** Förkastat på beslutspunkt 4
  och 11. Formen tillåter en flagga utan skäl, och ordet är upptaget av ADR 0006:s grind.
- **Ta bort de tre indikatorerna ur `categories.yaml`.** Förkastat. De dokumenterar vad
  kategorianspråket omfattar. Att stryka dem skulle dölja hålet helt, alltså motsatsen till
  beslutspunkt 9 och 10.
- **Namnge felen efter symtomet, till exempel `omtvistad_målnivå` och `ej_partistyrbar`.**
  Förkastat på beslutspunkt 5. Symtomnamn är svåra att återanvända på nästa indikator, och de
  pekar inte på den regel som fäller.

## Vad beslutet inte rör

- Vikterna 0,30 x A + 0,50 x B + 0,20 x D, C = 0 (ADR 0002).
- B:s och D:s krympning mot neutral och deras nämnare. De står orörda (beslutspunkt 9).
- Bandet, säkerhetsnivåerna och `band_only` (ADR 0009).
- Evidensgrinden och `admitted` (ADR 0006).
- Reglagelistan och känslighetsanalysen (ADR 0003, ADR 0010).
- Genomgången av samtliga indikatorer. Den är ett bygge och ligger i
  [#4](https://github.com/mcknschn/rosta/issues/4).
- Kortets framsida. Den ligger i [#11](https://github.com/mcknschn/rosta/issues/11).

## Följder

- **Bygget är en egen slice. BYGGD 2026-08-26** i biljett
  [#34](https://github.com/mcknschn/rosta/issues/34). Den rörde `config/categories.yaml`,
  `pipeline/config.py`, `pipeline/scorerun.py`, `pipeline/score.py`, metodrutan i
  `pipeline/scorerun.py` samt testerna. Uteslutningsskälet står i fältet `exclusion` och
  återöppningsvillkoret i `reopen_if`. `dist/scores.json` ändrades i exakt ett fält: ekonomins
  `coverage`, 0,877 till 0,721 för sju partier och 0,677 till 0,575 för V. `score`, `ci`,
  `components`, `confidence` och `flags` stod still i alla 56 celler, och rangordningen med dem.
  Ingen omkörning av känslighetsanalysen krävdes, eftersom betygen står still.
- **ADR 0008 punkt 5 ändras** enligt beslutspunkt 9. Ändringen skrivs in när slicen byggs.
- **Ordlistan §4.3 får Uteslutningsskäl** med tre värden, och rad 3b tappar `target`.
- **`DATA.md` och `IDEA.md` ändras.** `DATA.md` beskriver i dag `target` som "hoppas över, saknar
  målnivå", och `IDEA.md` har både en not om att target-undermått renormaliseras bort och en
  tabellrad "Upp till beslutad målnivå".
- **[#4](https://github.com/mcknschn/rosta/issues/4) är avblockerad.** Regeln är låst, och
  genomgången kan börja. En upplysning till den biljetten: den säger 52 indikatorer, men configen
  har 68. Mastertabellen i §4.3 är från 2026-06-06 och har inte följt med D-svepen.
- **Ingen kod och ingen config ändrades i BESLUTSärendet (#13).** Rangordningen var oförändrad
  tills slicen kördes, och den stod still också då.
- **Ändrat i det här ärendet:** den här ADR:n, ordlistan §4.3, `DATA.md` och `IDEA.md`.
