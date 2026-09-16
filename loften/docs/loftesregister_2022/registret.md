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
| Underlaget draget ur alla åtta PDF:er | klart |
| Tre blinda genomgångar per dokument | klart |
| De tre differenstalen räknade per dokument | klart |
| Varje differens avgjord av projektägaren | klart, 15 fall |
| Registret byggt och hashpinnat | klart, **1120 poster** |

Registret är låst. `pipeline/tools/loftesregister.py --bygg` vägrar skriva det så länge ett fall
står oavgjort, eftersom en tyst förvald sida vore ett avgörande utan avgörare.

Registret bar 729 poster i sin första låsning samma dag. Varför det gjordes om står under
[Varför registret gjordes om](#varför-registret-gjordes-om).

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

Alla åtta dokument är spaltsatta. Läsordningen tas fram med ett rekursivt XY-snitt: snittet läggs
vid den bredaste luckan, och en lodrät lucka provas före en vågrät. En rubrik som går över båda
spalterna hindrar den lodräta delningen, så bandet med rubriken skiljs av först och spalterna
delas därefter. Sorterar man i stället på höjd flätas spalterna ihop rad för rad.

**Två trösklar styr snittet, och båda är mätta och inte valda.**

| Tröskel | Värde | Vad den skiljer |
|---|---|---|
| `RANNA_MIN` | 8,5 punkter | Spaltrännan från radavståndet inom en spalt |
| `BAND_MIN` | 0,1 punkter | Ett band från nästa band, vågrätt |

M sätter sina spalter med 8,9 till 12,2 punkters ränna, medan S har 85 punkter och KD 50. Med den
första låsningens tröskel på 14,0 vägrades den lodräta delningen för M på 28 av 40 sidor, och
spalterna flätades ihop. Utfallet är identiskt för varje tröskel mellan 7,0 och 10,0, och 8,5
ligger mitt på den platån.

Den vågräta delningen bevarar alltid ordningen, eftersom den skiljer band uppifrån och ned. Den
behöver därför ingen bred lucka för att vara säker. KD sätter luckan under rubriken
`REDO FÖR EN NY REGERING`, som korsar rännan, till 0,2 punkter. Med den första låsningens tröskel
på 3,0 gick varken den lodräta eller den vågräta delningen, och sidan föll igenom till en
sortering på höjd. Utfallet är identiskt för varje tröskel mellan 0,01 och 0,2.

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

En mätning på det låsta registret visade vad klausulen kostade. Mätningen kördes i två pass som
gav **exakt samma tal** på alla åtta dokument och alla tre prövade storleksgränser: 63 listlösa
sträckor, 379 brödtextstycken utanför registret, tillsammans 104 677 tecken.

De styckena låg inte där man först kunde tro, alltså i inledningar före en lista. För C och M var
det kapiteltexten själv, skriven i prosa och med uttryckliga förslag i sig:

> C, s12: `Vi ska dessutom leda Sverige till större ekonomisk jämställdhet. Vi vill uppvärdera
> statusen på kvinnodominerade yrken...`
>
> M, s24: `Invandringen till Sverige behöver minska för att integrationen ska fungera bättre.`

S:s slutkapitel `En stark global röst` bar hela partiets utrikespolitik i åtta stycken utan en
enda punkt, och låg utanför registret i sin helhet.

**Följden var att registret mätte typografi och inte löften.** Andelen av dokumentets brödtext som
kom med berodde på hur partiet råkade sätta sin text:

| Dokument | Andel av dokumentets tecken, version 2 | Andel, version 3 |
|---|---|---|
| S | 54 % | 95 % |
| M | 27 % | 89 % |
| SD | 61 % | 99 % |
| C | 35 % | 94 % |
| V | 98 % | 99 % |
| KD | 49 % | 95 % |
| MP | 51 % | 95 % |
| L | 66 % | 100 % |

V, som bara skriver löpande text, fick hela sitt dokument i registret. C, som skriver både lista
och löpande text, fick bara listan. Spannet gick från 27 till 98 procent, och det spannet var en
egenskap hos satsen och inte hos partierna.

Version 3 flyttar klausulen från dokument till avsnitt: **en följd av block som ingen listsignal
rör har stycket som enhet.** Det är samma regel som redan gällde V, tillämpad där den biter.
Spannet är nu 89 till 100 procent.

Den första låsningen ligger kvar i
[`arkiv/register_version2.yaml`](../../config/loftesregister_2022/arkiv/register_version2.yaml)
tillsammans med sina genomgångar och sin differens, och ändras aldrig. Ändringen står i klartext i
[instruktionens ändringsnot](genomgangsinstruktion.md#ändringar).

## Vad en post är

Posten följer dokumentets egen struktur (beslut 3). Instruktionen som alla genomgångar fick står i
[`genomgangsinstruktion.md`](genomgangsinstruktion.md) och är lika för A, B och C.

| Dokument | Poster | Varav listpunkt | Varav löpnummer | Poster med flera radspann |
|---|---|---|---|---|
| S | 81 | 40 | 0 | 8 |
| M | 377 | 253 | 0 | 7 |
| SD | 66 | 0 | 0 | 0 |
| C | 214 | 94 | 0 | 4 |
| V | 68 | 0 | 0 | 9 |
| KD | 56 | 0 | 0 | 1 |
| MP | 138 | 114 | 0 | 0 |
| L | 120 | 0 | 75 | 0 |

Resten är stycken i listlösa avsnitt. En post med flera radspann är ett stycke som satsen brutit
över en sidbrytning eller ett spaltbyte, och raderna däremellan, alltså sidnummer, sidhuvud eller
en bildtext, hör inte till löftet.

SD, V, KD och L bär ingen listmarkör alls. SD annonserar sina listor med raden
`Några av Sverigedemokraternas vallöften:`, KD sätter ett eget block per förslag, L numrerar 1 till
75, och V bär ingen lista alls och är i sin helhet ett listlöst avsnitt.

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
| S | 81 | 81 | 81 | 0 | 0 | 0 |
| M | 377 | 375 | 372 | 2 | 0 | 3 |
| SD | 66 | 66 | 66 | 0 | 0 | 0 |
| C | 214 | 211 | 211 | 3 | 0 | 0 |
| V | 68 | 68 | 68 | 0 | 0 | 0 |
| KD | 56 | 52 | 50 | 5 | 1 | 1 |
| MP | 138 | 138 | 138 | 0 | 0 | 0 |
| L | 120 | 120 | 120 | 0 | 0 | 0 |
| **Summa** | **1120** | **1111** | **1106** | **10** | **1** | **4** |

Fem av åtta dokument gav noll i alla tre talen, alltså samma svar på varje post.

### Vad det tredje passet visade

| Dokument | A | B | C | Alla tre eniga |
|---|---|---|---|---|
| S | 81 | 81 | 81 | 81 |
| M | 377 | 375 | 377 | 372 |
| SD | 66 | 66 | 66 | 66 |
| C | 214 | 211 | 214 | 211 |
| V | 68 | 68 | 68 | 68 |
| KD | 56 | 52 | 58 | 50 |
| MP | 138 | 138 | 138 | 138 |
| L | 120 | 120 | 120 | 120 |
| **Summa** | **1120** | **1111** | **1128** | **1106** |

**1106 av 1120 poster drogs exakt lika av tre oberoende genomgångar.**

Det mest upplysande är inte talet utan var oenigheten ligger. A och C är två oberoende körningar av
samma modell, och de är **identiska i sju av åtta dokument**. Bara KD skiljer dem åt, och där på
två ställen. Oenigheten går alltså nästan helt mellan leverantörerna och inte mellan körningarna,
vilket är ett starkare besked om regelns stabilitet än differenstalet i sig.

## Projektägarens avgöranden

Alla 15 fall är avgjorda, och varje avgörande står med sitt skäl i
[`differens.yaml`](../../config/loftesregister_2022/differens.yaml). Projektägaren godkände tre
principer, och varje fall hör till en av dem.

| Princip | Fall | Avgörande |
|---|---|---|
| **1. Ett stycke är ett stycke.** Har satsen brutit ett stycke över en sidbrytning eller ett spaltbyte är det en post. Står två stycken efter varandra är det två. | M-01 till M-04, KD-02, KD-05, KD-06 | sju |
| **2. Satsens egna delar är inte löften.** | M-05 | ett |
| **3. Innehållet avgör aldrig.** Är texten satt i brödtextgrad är den ett stycke. | C-01 till C-03, KD-01, KD-03, KD-04, KD-07 | sju |

Fjorton fall avgjordes till A och ett till `ingen`. I varje fall utom ett står två av tre
genomgångar bakom avgörandet. Undantaget är KD-02, där A och C har samma rader men drar gränsen
olika, och där A:s hopfogning följer instruktionens avsnitt `Sidbrytningen`.

Princip 3 är den som bär registrets omfång, och den är hela poängen med version 3. Att
`Framtiden är grön.` är satt i 9,7 punkter, exakt sidans brödtextgrad, är ett faktum om satsen.
Att meningen låter som ett slagord är ett faktum om innehållet, och innehållet avgör aldrig.

## Antal poster per parti

| Parti | Poster | Sidor i dokumentet |
|---|---|---|
| S | 81 | 17 |
| M | 377 | 40 |
| SD | 66 | 12 |
| C | 214 | 25 |
| V | 68 | 17 |
| KD | 56 | 12 |
| MP | 138 | 12 |
| L | 120 | 19 |
| **Summa** | **1120** | |

**Antalet följer dokumentets form, inte partiets vilja.** M får 377 poster och KD 56 därför att M
skriver korta punkter genom fyrtio sidor medan KD skriver tolv, inte därför att M lovar sju gånger
mer. Partier rangordnas aldrig efter antalet, och den här meningen ska stå intill talet varje gång
det visas (beslut 28).

Version 3 tog bort den grövsta skevheten, den mellan lista och löptext, men inte den mellan ett
långt och ett kort dokument. Den senare är en egenskap hos dokumenten och inget ett register kan
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

Ett prov till bär version 3: **inget block på 200 tecken eller mer får ligga utanför registret.**
En rubrik, en bildtext, ett sidnummer eller en tryckortsrad är aldrig så lång, så ett långt block
utanför registret är ett stycke som en genomgång tappade. Provet har ett enda namngivet undantag,
de 27 landsnamnen under stapelaxeln i diagrammet på M:s sida 5.

Efter låsningen ändras ingen post. Enda öppningen är en **errata-rad** för ett avskrivningsfel som
går att belägga mot PDF:en, med datum och skäl (beslut 8). Fältet `errata` finns i filen och är
tomt.
