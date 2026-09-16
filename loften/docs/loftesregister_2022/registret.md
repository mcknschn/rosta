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
| Två blinda genomgångar per dokument | klart |
| De tre differenstalen räknade per dokument | klart |
| Varje differens avgjord av projektägaren | klart, 21 fall |
| Registret byggt och hashpinnat | klart, **729 poster** |

Registret är låst. `pipeline/tools/loftesregister.py --bygg` vägrar skriva det så länge ett fall
står oavgjort, eftersom en tyst förvald sida vore ett avgörande utan avgörare.

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

## Vad en post är

Posten följer dokumentets egen struktur (beslut 3). Instruktionen som båda genomgångarna fick står
i [`genomgangsinstruktion.md`](genomgangsinstruktion.md) och är lika för A och B.

Dokumenten är byggda på fyra olika sätt, och tabellen visar vilken signal som faktiskt bar posterna
i varje dokument. Talen är räknade på genomgång A.

| Dokument | Posten är | Punktmarkör | Löpnummer | Eget block | Andel av dokumentets tecken |
|---|---|---|---|---|---|
| S | en punkt i listorna som inleds med `Våra viktigaste förslag handlar om att:` | 40 av 40 | 0 | 40 | 54 % |
| M | en punkt i listorna som inleds med `Moderaterna kommer att:` | 253 av 253 | 0 | 204 | 27 % |
| SD | ett förslag i listorna som inleds med `Några av Sverigedemokraternas vallöften:` | 0 | 0 | 42 | 61 % |
| C | en punkt i en `reformagenda` | 94 av 94 | 0 | 94 | 35 % |
| V | **ett stycke i den löpande texten** | 0 | 0 | 68 | 98 % |
| KD | en punkt i listan under kapitlets rubrik | 0 | 0 | 46 | 49 % |
| MP | en punkt i listan efter `Vi vill:` | 114 av 114 | 0 | 2 | 51 % |
| L | ett numrerat löfte, `1.` till `75.` | 0 | 75 av 75 | 74 | 66 % |

**V avviker, och avvikelsen är ett faktum om dokumentet.** Vänsterpartiets valplattform 2022 bär
ingen listmarkör, inget löpnummer och ingen rad som annonserar en uppräkning. Den är löptext under
rubriker. Den finaste nivå dokumentet självt markerar är därför stycket, och V:s poster är stycken
medan M:s är punkter i en lista. V:s poster täcker 98 procent av dokumentets tecken, mot 27 procent
hos M. Talen mäter dokumentens form, inte partiernas vilja.

Sexton poster bärs av **flera radspann**: 9 hos V, 6 hos S och 1 hos C. Punkten bryts där av en
sidbrytning, och sidnumret däremellan hör inte till löftet.

### C kördes om

C sätter sin punktglyf ensam på en rad och texten på nästa. Den första utvinningen tappade
markören där, så C:s underlag bar noll listmarkörer trots 96 punkter i PDF:en, och båda
genomgångarna läste C utan dess starkaste strukturssignal. Felet hittades i kodgranskningen,
lagades, och **båda genomgångarna kördes om för C i nya sammanhang**. Radnumreringen rördes inte.

Utfallet är värt att skriva ned: genomgång A gav exakt samma 94 poster som förut, medan genomgång
B gick från 96 till 94. C:s fyra differenser försvann helt, och dokumentet går nu ihop på varje
post.

### V kördes också om, och av ett tyngre skäl

Instruktionens version 1 gick inte att tillämpa på V. Den sade både att enheten är den finaste nivå
dokumentet självt markerar, vilket för V är stycket, och att löpande brödtext inte är en post,
vilket träffar vart och ett av V:s stycken. De två kan inte gälla samtidigt.

Följden var att båda genomgångarna gjorde något tredje: de tog 50 av 77 brödtextstycken var och
sållade på innehåll utan att skriva ned sållet. De sållade lika i 67 fall och olika i 10. Fem
stycken som **båda** uteslöt beskriver ett problem utan att namnge en åtgärd, vilket är
handlingsprovet i beslut 6 tillämpat ett steg för tidigt. Ett register som låses på ett osagt såll
går inte att göra om.

Instruktionen fick därför ett nytt avsnitt, `Dokument utan liststruktur`, och V kördes om under
version 2. Ändringen står i klartext i
[instruktionens ändringsnot](genomgangsinstruktion.md#ändringar), och den första körningen ligger
kvar i [`arkiv/v_genomgangar_version1.yaml`](../../config/loftesregister_2022/arkiv/v_genomgangar_version1.yaml).
Det är vad spärren i beslut 32 kräver av en omkörning. De sju andra dokumenten bär alla en lista,
så klausulen kan inte falla ut för dem, och de kördes inte om.

Omkörningen gav ett mycket renare utfall. **Båda genomgångarna tog exakt samma 647 av V:s 689
rader**, och de 42 som blev över är identiska i båda: 16 sidhuvuden, 16 sidnummer och 10
kapitelrubriker. Ingen oenighet alls om vad som är text. Kvar stod nio stycken som bryts av en
sidbrytning, där A fogade ihop halvorna och B lät dem stå som två poster. Instruktionens avsnitt
`Sidbrytningen` svarar på det, så alla nio avgjordes till A.

## De två blinda genomgångarna

Beslut 7 kräver två genomgångar i skilda kontexter, med samma instruktion, och att ingen ser den
andras utdata.

- **Genomgång A**: Claude Opus 5, ett eget sammanhang per dokument, åtta i allt.
- **Genomgång B**: Codex (gpt-5.6-sol) via `codex exec`, ett eget anrop per dokument, åtta i allt.

Två leverantörer, precis som Verklighetsbildpilotens kodning. Ingen av dem fick se den andras
svar, och ingen av dem fick se den här filen.

En genomgång pekar ut poster som **radspann i underlaget**, aldrig som avskriven text. Lydelsen
kommer alltså ur PDF:en och inte ur en kodares tangentbord. Det gör också differenstalet till vad
beslut 7 vill mäta, nämligen var två genomgångar drar postens gräns, och inte hur olika de stavar
samma mening.

Båda genomgångarna är maskinellt prövade mot underlaget: varje radnummer finns, inga två poster tar
samma rad, och antalet rader ingen post tog är räknat. Sexton prövningar, noll fel.

## De tre talen

`python -m pipeline.tools.loftesregister --differens`

| Dokument | Poster A | Poster B | Delade | Bara A | Bara B | Styckat olika |
|---|---|---|---|---|---|---|
| S | 40 | 40 | 40 | 0 | 0 | 0 |
| M | 253 | 253 | 253 | 0 | 0 | 0 |
| SD | 42 | 42 | 42 | 0 | 0 | 0 |
| C | 94 | 94 | 94 | 0 | 0 | 0 |
| V | 68 | 77 | 59 | 0 | 9 | 9 |
| KD | 46 | 46 | 46 | 0 | 0 | 0 |
| MP | 114 | 111 | 111 | 3 | 0 | 0 |
| L | 75 | 75 | 75 | 0 | 0 | 0 |
| **Summa** | **732** | **738** | **720** | **3** | **9** | **9** |

Sex av åtta dokument gav noll i alla tre talen, alltså samma svar på varje post. De två som inte
gjorde det gav 21 fall, och alla 21 är av två slag:

- **V, arton fall.** Nio stycken bryts av en sidbrytning. A fogade ihop halvorna till en post med
  två radspann, B lät dem stå som två poster. Varje par ger ett `styckat olika` och ett `bara B`.
  Det är ingen tolkningsfråga: instruktionens avsnitt `Sidbrytningen` säger att posten bärs av
  flera radspann, och varje första halva slutar mitt i en mening.
- **MP, tre fall.** De tre raderna om solidaritet på sidan 3, som den ena genomgången läste som
  punkter och den andra som partiets värdegrund.

## Projektägarens avgöranden

Alla 21 fall är avgjorda, och varje avgörande står med sitt skäl i
[`differens.yaml`](../../config/loftesregister_2022/differens.yaml).

| Fall | Avgörande | Skäl |
|---|---|---|
| V, nio stycken över en sidbrytning | A:s styckning | Instruktionens avsnitt `Sidbrytningen` gäller redan. Samma regel bär de sex hos S och den hos C som båda genomgångarna var eniga om från början. |
| V, nio andra halvor | ingen post | Raderna ligger redan i den hopfogade posten. En egen post skulle ta samma rader två gånger. |
| MP, tre solidaritetsrader | ingen post | Raderna bär MP:s värdegrund och ingen åtgärd. De står som punkter i dokumentet, men innehållet är inte ett löftesled. |

MP-avgörandet är det enda där innehållet fick väga tyngre än strukturen, och det är projektägarens
kall.

Varje fall står i [`differens.yaml`](../../config/loftesregister_2022/differens.yaml) med båda
genomgångarnas lydelse, sidnummer och radspann, och ett tomt `beslut`.

## Antal poster per parti

| Parti | Poster | Sidor i dokumentet |
|---|---|---|
| S | 40 | 17 |
| M | 253 | 40 |
| SD | 42 | 12 |
| C | 94 | 25 |
| V | 68 | 17 |
| KD | 46 | 12 |
| MP | 111 | 12 |
| L | 75 | 19 |
| **Summa** | **729** | |

**Antalet följer dokumentets form, inte partiets vilja.** M får 253 poster och S 40 därför att M
skriver korta punkter genom fyrtio sidor medan S buntar sina förslag i fyrtio längre punkter, inte
därför att M lovar sex gånger mer. V:s 68 är stycken och inte punkter, och är därför inte samma
slags tal som de övriga alls. Partier rangordnas aldrig efter antalet, och den här meningen ska stå
intill talet varje gång det visas (beslut 28).

## Vad registret inte bär

- **Inget kategorifält** (beslut 11). Kategorilistan bestäms i en senare biljett, ur det här
  registret plus den frysta korpusen, och ett fält här skulle forma listan mitt under genomgången.
- **Ingen prövbarhet.** Handlingsprovet i beslut 6 ligger i en egen biljett.
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

Efter låsningen ändras ingen post. Enda öppningen är en **errata-rad** för ett avskrivningsfel som
går att belägga mot PDF:en, med datum och skäl (beslut 8). Fältet `errata` finns i filen och är
tomt.
