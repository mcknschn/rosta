# Löftesregistret 2022

> Registret över vad de åtta riksdagspartierna lovade inför valet 2022, draget ur deras egna
> valmanifest med full lydelse och sidnummer. Biljett
> [#54](https://github.com/mcknschn/rosta/issues/54), steg 1 i byggordningen (beslut 34 i
> [beslutsdokumentet](../beslut/2026-09-16-sparets-form.md)).

**Registret mäter inte om ett löfte är bra för Sverige.** Det säger vad partiet lovade, och
ingenting annat. Om åtgärden var klok avgörs av delpoäng B och D i modellen, aldrig här.

## Läget

| Steg | Läge |
|---|---|
| Underlaget draget ur alla åtta PDF:er, med blockens textgrad | klart |
| Tre blinda genomgångar per dokument, under instruktionens version 4 | klart |
| De tre differenstalen räknade per dokument | klart |
| Varje differens avgjord av projektägaren | klart, 32 fall i 3 frågor |
| Registret byggt och hashpinnat | klart, **1147 poster** |

Registret är låst. `pipeline/tools/loftesregister.py --bygg` vägrar skriva det så länge ett fall
står oavgjort, eftersom en tyst förvald sida vore ett avgörande utan avgörare.

Registret bar 729 poster i sin första låsning och 1120 i sin andra, båda samma dag. Varför det
gjordes om två gånger står under [Varför registret gjordes om](#varför-registret-gjordes-om).

## Underlaget

Registret dras inte ur PDF:en för hand. `pipeline/tools/loftesregister.py --underlag` läser varje
PDF och skriver ett radnumrerat textunderlag, ett per dokument, under
`loften/underlag/valmanifest_2022/`. Samma PDF ger samma underlag, tecken för tecken.

Underlaget ligger **utanför git**, av samma skäl som PDF:erna: det är hela det
upphovsrättsskyddade verket, ord för ord. Registret bär i stället de citerade löftena, och
`underlag_sha256` i `register.yaml` binder registret till det underlag det drogs ur.

Varje rad bär radnummer, sidnummer, en markör för om raden inleds med en listmarkör i PDF:en, och
texten. Blockgränser och sidbrytningar står som egna rader. Ett block är PDF:ens egen styckning,
alltså dokumentets egen form.

### Läsordningen

S, M och KD är spaltsatta. De fem andra är ensspaltiga. Läsordningen tas fram med ett rekursivt
XY-snitt: snittet läggs vid den bredaste luckan, och en lodrät lucka provas före en vågrät. En
rubrik som går över båda spalterna hindrar den lodräta delningen, så bandet med rubriken skiljs av
först och spalterna delas därefter. Sorterar man i stället på höjd flätas spalterna ihop rad för
rad.

**Två trösklar styr snittet, och båda är mätta och inte valda.**

| Tröskel | Värde | Vad den skiljer |
|---|---|---|
| `RANNA_MIN` | 8,5 punkter | Spaltrännan från radavståndet inom en spalt |
| `BAND_MIN` | 0,1 punkter | Ett band från nästa band, vågrätt |

Textspaltrännan är 11,09 till 19,33 punkter hos M, 85 hos S och 21 hos KD. Med den första
låsningens `RANNA_MIN` på 14,0 vägrades den lodräta delningen för M överallt, och läsordningen blev
en annan på **26 av M:s 40 sidor**. Utfallet är identiskt för varje tröskel mellan 6,2 och 10,1.
Platåns övre kant sätts inte av spalterna utan av en rad ikoner på M:s sida 29, där luckan mellan
två ikoner är 10,15 punkter. 8,5 ligger inne på platån med marginal åt båda hållen.

Den vågräta delningen bevarar alltid ordningen, eftersom den skiljer band uppifrån och ned. Den
behöver därför ingen bred lucka för att vara säker. KD sätter luckan under rubriken
`REDO FÖR EN NY REGERING`, som korsar rännan, till 0,2 punkter. Med den första låsningens
`BAND_MIN` på 3,0 gick varken den lodräta eller den vågräta delningen, och sidan föll igenom till
en sortering på höjd. Utfallet är identiskt för varje tröskel mellan 0 och 0,21, och KD:s sida 2 är
det enda ställe i hela korpusen där sänkningen ändrar något.

Måttet på om läsordningen stämmer är språkligt och inte typografiskt: **ett block som börjar mitt
i en mening ska föregås av ett block som slutar mitt i en mening.** M hade sex sådana brott och KD
ett. Efter rättelsen har alla åtta dokument noll.

### Vad som skiljer underlaget från PDF:en

Fyra saker, och bara de fyra. De följer 2026 års mappning, så att årgångarna går att jämföra.

- **Avstavning över radbrott, spaltbrott och sidbrytning är hopfogad**, så att `för-` och
  `troende` blir `förtroende`. Bindestreck i sammansättningar står kvar, som i
  `vålds- och sexualbrott`, och regeln som skiljer de två är att nästa rad börjar med `och`,
  `eller` eller `samt`, eller med versal.
- **Ligaturer är upplösta**, så att `inﬂation` blir `inflation`.
- **Tankstreck är ersatta med bindestreck**, och hårt mellanslag med mellanslag.
- **Listmarkören är skild från texten.** S sätter sin punkt som en Wingdings-glyf, ett tabbsteg,
  ett mellanslag och ett BEL innan första bokstaven. Ingen del av det är partiets mening, men var
  det står är ett faktum om dokumentets form, så markören bärs vidare som en flagga på raden.

Partiernas egna stavfel står kvar. Ett **löpnummer som partiet självt satte** står också kvar i
lydelsen, som i L:s `75. Handel och bistånd för demokrati.` Skillnaden mot punktglyfen är att
numret är text partiet skrev, medan glyfen är typografi satsen lade till.

## Varför registret gjordes om

Den första låsningen gav 729 poster och byggde på instruktionens version 2. Den versionen band
styckeregeln till hela dokumentet: bar dokumentet en lista någonstans gällde listsignalerna
överallt, också i kapitel utan lista.

En mätning på det låsta registret visade vad klausulen kostade. Mätningen kördes i två pass, ett av
mig och ett av Codex i eget sammanhang med samma definition, och de gav **exakt samma tal** på alla
åtta dokument och alla tre prövade storleksgränser. Med gränsen 120 tecken: 63 listlösa sträckor om
minst två stycken, tillsammans 319 stycken och 104 677 tecken. Räknar man varje otäckt stycke för
sig, utan kravet på en sträcka, blir det 379.

De styckena låg inte där man först kunde tro, alltså i inledningar före en lista. För C och M var
det kapiteltexten själv, skriven i prosa och med uttryckliga förslag i sig:

> C, s12: `Vi ska dessutom leda Sverige till större ekonomisk jämställdhet. Vi vill uppvärdera
> statusen på kvinnodominerade yrken...`
>
> M, s24: `Invandringen till Sverige behöver minska för att integrationen ska fungera bättre.`

S:s slutkapitel `En stark global röst` bar hela partiets utrikespolitik i åtta stycken utan en
enda punkt, och låg utanför registret i sin helhet.

**Följden var att registret mätte typografi och inte löften.** Andelen av dokumentets brödtext som
kom med berodde på hur partiet råkade sätta sin text. Talet är tecken i tagna rader genom alla
tecken i underlaget, räknat likadant för båda versionerna.

| Dokument | Version 2 | Version 3 |
|---|---|---|
| S | 54,8 % | 93,4 % |
| SD | 61,7 % | 98,1 % |
| C | 35,4 % | 93,4 % |
| V | 98,4 % | 98,4 % |
| MP | 51,0 % | 94,4 % |
| L | 66,1 % | 98,9 % |
| M | ingen jämförelse | 87,8 % |
| KD | ingen jämförelse | 93,2 % |

M och KD saknar version 2-tal därför att deras underlag drogs om när läsordningen rättades. Deras
gamla radspann pekar på andra rader i det nya underlaget, så ett tal räknat på dem vore inte det
det ser ut att vara. De sex övriga dokumentens underlag är byte för byte oförändrade.

För de sex jämförbara gick spannet från **35 till 98 procent** till **93 till 99**. Med M och KD
inräknade är version 3-spannet 88 till 99.

V, som bara skriver löpande text, fick hela sitt dokument i registret redan under version 2. C, som
skriver både lista och löpande text, fick bara listan. Spannet var en egenskap hos satsen och inte
hos partierna.

Version 3 flyttar klausulen från dokument till avsnitt: **en följd av block som ingen listsignal
rör har stycket som enhet.** Det är samma regel som redan gällde V, tillämpad där den biter.

### Och varför det gjordes om en gång till

Version 3 gav 1120 poster, men en kodgranskning och en korsläsning fällde regeln som sådan.

Version 3 hade **två regimer**: fyra listsignaler där avsnittet bar en lista, och en styckeregel
där det inte gjorde det. Vilken regim som gällde berodde på var listan slutade, och var listan
slutade berodde på regimen. Signal 3 pekade ut block som inte bar någon signal, så gränsen gick
inte att läsa ur underlaget. Cirkeln gick inte att laga med en gränsregel.

Version 4 tar bort gränsen i stället för att dra den. En regel, två led, ingen regim. Mätningen som
motiverar det: **fyra av de åtta dokumenten bär inte en enda listmarkör**, så för dem var de fyra
signalerna redan verkningslösa.

Tre fel till rättades, alla funna i granskningen av version 3:

- **Princip 3 var inte tillämpbar.** Den säger att typografin och inte innehållet avgör
  rubrikfrågan, men underlaget bar ingen textgrad. Därför uteslöt två genomgångar av tre
  `Framtiden är grön.` som ett slagord. Blocket bär nu sin grad, mätt i PDF:en.
- **En post var avhuggen.** S-066 slutade `för att trygga vår` medan orden `fred och frihet.` stod
  på nästa rad, tillsammans med listannonseringen. Alla tre genomgångarna uteslöt hela raden.
- **Registret pinnade instruktionen med en sökväg.** Filen skrevs sedan om, så det låsta registret
  hänvisade till en regel det aldrig kördes under.

Täckningen rörde sig knappt, från 88-99 procent till 88-99. Det säger vad version 4 var till för:
inte att fånga mer text, utan att göra regeln tillämpbar lika av tre oberoende genomgångar.

De två tidigare låsningarna ligger kvar i
[`arkiv/`](../../config/loftesregister_2022/arkiv/) tillsammans med sina genomgångar, sin differens
och den instruktionsversion var och en kördes under, se
[`arkiv/LASMIG.md`](../../config/loftesregister_2022/arkiv/LASMIG.md). De ändras aldrig. Varje
ändring står i klartext i [instruktionens ändringsnot](genomgangsinstruktion.md#ändringar).

## Vad en post är

Posten följer dokumentets egen struktur (beslut 3). Instruktionen som alla genomgångar fick står i
[`genomgangsinstruktion.md`](genomgangsinstruktion.md) och är lika för A, B och C.

Version 4 har **en regel med två led**. Bär blocket listsignaler är varje punkt en post. Bär det
inga är hela blocket en post. En listsignal är listmarkören `*` eller ett inledande löpnummer.

| Dokument | Poster | Varav listpunkt | Varav löpnummer | Flera radspann | Täckning |
|---|---|---|---|---|---|
| S | 82 | 40 | 0 | 6 | 93,4 % |
| M | 376 | 253 | 0 | 7 | 87,6 % |
| SD | 65 | 0 | 0 | 0 | 97,9 % |
| C | 235 | 94 | 0 | 4 | 95,3 % |
| V | 68 | 0 | 0 | 9 | 98,4 % |
| KD | 63 | 0 | 0 | 1 | 95,0 % |
| MP | 138 | 114 | 0 | 0 | 95,5 % |
| L | 120 | 0 | 75 | 0 | 98,9 % |
| **Summa** | **1147** | **501** | **75** | **27** | |

Resten är hela block. Täckningen är tecken i tagna rader genom alla tecken i underlaget.

**Fyra av de åtta dokumenten, SD, V, KD och L, bär inte en enda listmarkör.** För dem gäller bara
andra ledet: varje block är en post. Det är den ojämnheten regeln finns till för. L är undantaget
bland de fyra och numrerar sina 75 förslag i löptext.

M ligger lägst på 87,6 procent, och det som saknas är diagram. Tolv procent av M:s text är
axeletiketter, bildtexter, sifferetiketter och källrader, som alla faller i steg 1.

## De tre blinda genomgångarna

Beslut 7 kräver två genomgångar i skilda kontexter, med samma instruktion, och att ingen ser den
andras utdata. Projektägaren beställde ett tredje pass som extra prov på hur stabil regeln är.

- **Genomgång A**: Claude Opus 5, ett eget sammanhang per dokument.
- **Genomgång B**: Codex (gpt-5.6-sol) via `codex exec`, ett eget anrop per dokument.
- **Genomgång C**: Claude Opus 5 igen, nya sammanhang, som inte såg vare sig A eller B.

Två leverantörer, precis som Verklighetsbildpilotens kodning. Differensen och facit räknas på A mot
B enligt beslut 7. Pass C avgör ingenting, utan mäter.

En genomgång pekar ut poster som **radspann i underlaget**, aldrig som avskriven text. Lydelsen
kommer alltså ur PDF:en och inte ur en kodares tangentbord. Det gör också differenstalet till vad
beslut 7 vill mäta, nämligen var två genomgångar drar postens gräns, och inte hur olika de stavar
samma mening.

Alla tre genomgångarna är maskinellt prövade mot underlaget: varje radnummer finns, inga två poster
tar samma rad, och antalet rader ingen post tog är räknat. Tjugofyra prövningar, noll fel.

## De tre talen

`python -m pipeline.tools.loftesregister --differens`

| Dokument | Poster A | Poster B | Delade | Bara A | Bara B | Styckat olika |
|---|---|---|---|---|---|---|
| S | 82 | 80 | 79 | 2 | 0 | 1 |
| M | 376 | 376 | 376 | 0 | 0 | 0 |
| SD | 65 | 65 | 65 | 0 | 0 | 0 |
| C | 214 | 235 | 214 | 0 | 21 | 0 |
| V | 68 | 68 | 68 | 0 | 0 | 0 |
| KD | 63 | 55 | 55 | 8 | 0 | 0 |
| MP | 138 | 138 | 138 | 0 | 0 | 0 |
| L | 120 | 120 | 120 | 0 | 0 | 0 |
| **Summa** | **1126** | **1137** | **1115** | **10** | **21** | **1** |

Fem av åtta dokument gav noll i alla tre talen, alltså samma svar på varje post. Under version 3
gällde det också fem dokument, men M var inte ett av dem. Nu är M identiskt i alla tre passen,
alla 376 posterna.

### Vad det tredje passet visade

| Dokument | A | B | C | Alla tre eniga |
|---|---|---|---|---|
| S | 82 | 80 | 82 | 79 |
| M | 376 | 376 | 376 | 376 |
| SD | 65 | 65 | 65 | 65 |
| C | 214 | 235 | 214 | 214 |
| V | 68 | 68 | 68 | 68 |
| KD | 63 | 55 | 56 | 54 |
| MP | 138 | 138 | 138 | 138 |
| L | 120 | 120 | 120 | 120 |
| **Summa** | **1126** | **1137** | **1119** | **1114** |

**1114 poster drogs exakt lika av tre oberoende genomgångar.** Pass A och C är två oberoende
körningar av samma modell och är **identiska i sju av åtta dokument**, KD undantaget. Oenigheten
går alltså nästan helt mellan leverantörerna och inte mellan körningarna.

Alla 24 genomgångarna är maskinellt prövade mot underlaget: varje radnummer finns, inga två poster
tar samma rad, och ingen post slutar mitt i en mening. Noll fel i alla tre talen.

## Projektägarens avgöranden

De 32 fallen faller i tre frågor, och varje avgörande står med sitt skäl i
[`differens.yaml`](../../config/loftesregister_2022/differens.yaml).

### Fråga 1: S, tre fall. Avgjord till A

Rad 165 slutar `...gå till jobbet.` med punkt och rad 168 på nästa sida börjar `Fler insatser
krävs` med versal. Det språkliga provet i princip 1 ger då två poster, inte en över sidbrytningen.
Pass B fogade ihop dem ändå. Det tredje fallet är rad 588-590, tre rader löpande prosa i 12,0
punkter mot sidans 9,5, som A och C tog och B uteslöt. Pass C stöder A på alla tre.

### Fråga 2: C, 21 fall. Avgjord till B, mot pass A och C

Det här är det mest upplysande avgörandet i hela omkörningen, eftersom **instruktionen gav Codex
rätt mot båda mina egna pass.**

C sätter 21 mellanrubriker i sidans brödtextgrad 9,7, till exempel `Fördubbla produktionen av
utsläppsfri el och förnybara bränslen` på rad 244, var och en över en punktlista. Pass A och C
uteslöt dem som mellanrubriker. Pass B tog dem som poster.

Instruktionen säger att graden bara kan visa att ett block **inte** är en rubrik. Står blocket i
brödtextgrad är det alltså ingen rubrik, och då är det en post. Det är exakt samma läge som
`Framtiden är grön.` på rad 190, som version 3 redan avgjorde åt det hållet. Pass A och C
tillämpade det omdöme princip 3 förbjuder, och de gjorde det likadant båda två.

Att två pass av samma modell kan gå fel åt samma håll är skälet till att ett tredje pass av en
annan leverantör behövs. Här gjorde det sitt jobb.

### Fråga 3: KD sida 12, åtta fall. Avgjord till A

Raderna 288-299 är sju block i grad 10,9 med versala fraser, `FLER JOBB FLER FÖRETAG`, `BÄTTRE
OMSORG FÖR UTSATTA` och så vidare. Pass A gjorde sju poster, pass B uteslöt dem som grafik, och
pass C slog ihop 286-299 till en enda post. Tre olika svar på samma textställe, det enda i hela
korpusen.

Pass C läste versalraderna som objekt till meningen som slutar `Förslag för` på rad 287, vilket är
den bästa läsningen språkligt. Men det språkliga provet kräver gemen begynnelsebokstav, och
versalraderna har versal. Huvudregelns andra led ger då sju block, alltså sju poster.

Rad 300-301, `VI ÄR REDO` och `Din röst behövs för förändring`, står i 12,2 punkter, samma grad som
blocken 80 och 81 på samma sida. 12,2 är alltså sidans egen brödtextgrad, och uteslutningen av
slagord gäller bara block utanför brödtextgraden.

## Formberoendet som stängdes

Version 3 lät en inledning i ett block som bar en lista falla bort, medan samma inledning i ett
eget block blev en post. I hela korpusen slog det igenom på **ett ställe**: MP:s sida 3, raderna
6-7, 259 tecken. Blocket bär både brödtexten och de tre solidaritetspunkterna.

Version 4 gör raderna före blockets första listsignal till en post för sig. MP:s rad 6-7 är nu
posten `Vi strävar efter en värld där alla kan leva goda liv utan att försämra villkoren för
kommande generationer...`, och C:s motsvarande inledning i eget block behandlas likadant.

Kvar är formberoendet mellan ett långt och ett kort dokument, se
[Antal poster per parti](#antal-poster-per-parti). Det är en egenskap hos dokumenten och inget ett
register kan räkna bort.

## Antal poster per parti

| Parti | Poster | Sidor i dokumentet |
|---|---|---|
| S | 82 | 17 |
| M | 376 | 40 |
| SD | 65 | 12 |
| C | 235 | 25 |
| V | 68 | 17 |
| KD | 63 | 12 |
| MP | 138 | 12 |
| L | 120 | 19 |
| **Summa** | **1147** | |

**Antalet följer dokumentets form, inte partiets vilja.** M får 376 poster och KD 63 därför att M
skriver korta punkter genom fyrtio sidor medan KD skriver tolv, inte därför att M lovar sju gånger
mer. Partier rangordnas aldrig efter antalet, och den här meningen ska stå intill talet varje gång
det visas (beslut 28).

Version 3 och 4 tog bort skevheten mellan lista och löptext, men inte den mellan ett långt och ett
kort dokument. Den senare är en egenskap hos dokumenten och inget ett register kan
räkna bort.

## En iakttagelse som inte ändrades

Instruktionens korta uteslutningslista för listlösa avsnitt nämner rubriker, bildtexter,
diagramrubriker, sidnummer, sidhuvuden, innehållsförteckning, tryckortsuppgifter och
namnunderskrifter. Den nämner inte webbadresser eller konton i sociala medier.

Följden syns på två ställen. KD:s `Facebook: fb.me/buschebba Insta: @buschebba` står i blocket
direkt efter namnunderskriften och föll bort som en del av den. SD:s
`Läs valplattformen: sd.se/dokument` står fritt i ett listlöst avsnitt och är därför en post, och
alla tre genomgångarna tog den.

De två är åtskiljbara, och registret är följdriktigt. Men luckan är värd att täppa till nästa gång
instruktionen ändå ändras. Att ändra den nu vore att flytta regeln efter att genomgångarna kört
under den.

## Vad registret inte bär

- **Inget kategorifält** (beslut 11). Kategorilistan bestäms i en senare biljett, ur det här
  registret plus den frysta korpusen, och ett fält här skulle forma listan mitt under genomgången.
- **Ingen prövbarhet.** Handlingsprovet i beslut 6 ligger i en egen biljett. Att ett stycke bara
  beskriver ett problem gör det inte till en icke-post här.
- **Inget om instrument, uppfyllelse eller tumme.** Det är handlingssidan, och den kommer senare.
- **Ingen atomisering.** Lagret i beslut 4 läggs ovanpå extraktionen, inte i den.

## Låsningen

Registret är byggt och låst 2026-09-16 med

```
python -m pipeline.tools.loftesregister --bygg 2026-09-16
```

Filen bär sin egen SHA-256, räknad över filen utan just den raden, och varje dokuments PDF-hash ur
hämtmanifestet plus underlagets hash. `tests/test_loftesregister_2022.py` räknar om hashen. Provet
är kört mot en ändrad bokstav i en lydelse och föll, och passerade igen när bokstaven lades
tillbaka.

Fyra prov till bär låsningen.

**Ingen otagen radföljd på 200 tecken eller mer får ligga utanför registret.** En rubrik, en
bildtext, ett sidnummer eller en tryckortsrad är aldrig så lång, så en lång radföljd utanför
registret är ett stycke som en genomgång tappade. Provet mäter radföljder och inte block, eftersom
ett block kan bära både tagen och otagen text.

**Registret pinnar det underlag det drogs ur.** Registret bär bara radspann, så en lydelse är sann
bara relativt ett bestämt underlag. Ändras utvinningen glider radnumren, och då pekar spannen på
annan text utan att `innehall_sha256` reagerar. `underlag_sha256` är spärren.

**Registret pinnar den instruktion genomgångarna kördes under.** Version 3:s register pinnade
instruktionen med en sökväg, och filen skrevs sedan om. `instruktion_sha256` och
`instruktion_version` är spärren. Provet är kört mot en tillagd rad i instruktionen och föll, och
passerade igen när raden togs bort.

**Ingen post slutar mitt i en mening.** Provet är det språkliga: en posts sista rad slutar utan
avslutande skiljetecken och nästa rad i samma block börjar med gemen, utan att någon annan post tog
den. Mot version 3:s register gav det exakt en träff, nämligen S-066. Mot version 4:s ger det noll.
Provet är den enda spärren mot ett fel som alla tre genomgångarna gör likadant, för då ger
differensen ingen signal.

Efter låsningen ändras ingen post. Enda öppningen är en **errata-rad** för ett avskrivningsfel som
går att belägga mot PDF:en, med datum och skäl (beslut 8). Fältet `errata` finns i filen och är
tomt.
