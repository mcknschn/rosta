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
| Varje differens avgjord av projektägaren | **öppet, 17 fall** |
| Registret byggt och hashpinnat | väntar på avgörandet |

Bygget stannar med flit vid avgörandet. `pipeline/tools/loftesregister.py --bygg` vägrar skriva
registret så länge ett fall står oavgjort, eftersom en tyst förvald sida vore ett avgörande utan
avgörare.

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
| C | en punkt i en `reformagenda` | 0 | 0 | 94 | 35 % |
| V | **ett stycke löptext** | 0 | 0 | 42 | 66 % |
| KD | en punkt i listan under kapitlets rubrik | 0 | 0 | 46 | 49 % |
| MP | en punkt i listan efter `Vi vill:` | 114 av 114 | 0 | 2 | 51 % |
| L | ett numrerat löfte, `1.` till `75.` | 0 | 75 av 75 | 74 | 66 % |

**V avviker, och avvikelsen är ett faktum om dokumentet.** Vänsterpartiets valplattform 2022 bär
ingen listmarkör, inget löpnummer och ingen rad som annonserar en uppräkning. Den är löptext under
rubriker. Den finaste nivå dokumentet självt markerar är därför stycket, och V:s poster är stycken
medan M:s är punkter i en lista. Det är också där de två genomgångarna gick isär mest.

Fjorton poster bärs av **flera radspann**: 7 hos V, 6 hos S och 1 hos C. Punkten bryts där av en
sidbrytning, och sidnumret däremellan hör inte till löftet.

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
| C | 94 | 96 | 92 | 0 | 2 | 2 |
| V | 43 | 43 | 38 | 5 | 5 | 0 |
| KD | 46 | 46 | 46 | 0 | 0 | 0 |
| MP | 114 | 111 | 111 | 3 | 0 | 0 |
| L | 75 | 75 | 75 | 0 | 0 | 0 |
| **Summa** | **707** | **706** | **697** | **8** | **7** | **2** |

Fem av åtta dokument gav noll i alla tre talen. De tre som inte gjorde det är de tre där
dokumentets egen struktur är svagast:

- **V** står för tio av de sjutton fallen. Dokumentet bär ingen lista alls, så gränsen mellan ett
  förslag och ett resonemang vilar helt på ett omdöme.
- **C** har fyra fall, som är två oenigheter räknade från båda hållen: en punkt som bär två
  meningar, där genomgång B läste den andra meningen som en egen punkt.
- **MP** har tre fall, alla samma sak: de tre raderna om solidaritet på sidan 3, som den ena
  genomgången läste som punkter och den andra som partiets värdegrund.

Varje fall står i [`differens.yaml`](../../config/loftesregister_2022/differens.yaml) med båda
genomgångarnas lydelse, sidnummer och radspann, och ett tomt `beslut`.

## Antal poster per parti

Talen nedan är vad de två genomgångarna redan är eniga om, alltså registret utan de sjutton
oavgjorda fallen. Det slutliga antalet sätts när differensen är avgjord.

| Parti | Poster (eniga) | Sidor i dokumentet |
|---|---|---|
| S | 40 | 17 |
| M | 253 | 40 |
| SD | 42 | 12 |
| C | 92 | 25 |
| V | 38 | 17 |
| KD | 46 | 12 |
| MP | 111 | 12 |
| L | 75 | 19 |
| **Summa** | **697** | |

**Antalet följer dokumentets form, inte partiets vilja.** M får 253 poster och S 40 därför att M
skriver korta punkter genom fyrtio sidor medan S buntar sina förslag i fyrtio längre punkter, inte
därför att M lovar sex gånger mer. V:s 38 är stycken och inte punkter, och är därför inte samma
slags tal som de övriga. Partier rangordnas aldrig efter antalet, och den här meningen ska stå
intill talet varje gång det visas (beslut 28).

## Vad registret inte bär

- **Inget kategorifält** (beslut 11). Kategorilistan bestäms i en senare biljett, ur det här
  registret plus den frysta korpusen, och ett fält här skulle forma listan mitt under genomgången.
- **Ingen prövbarhet.** Handlingsprovet i beslut 6 ligger i en egen biljett.
- **Inget om instrument, uppfyllelse eller tumme.** Det är handlingssidan, och den kommer senare.
- **Ingen atomisering.** Lagret i beslut 4 läggs ovanpå extraktionen, inte i den.

## Låsningen

När differensen är avgjord byggs registret med

```
python -m pipeline.tools.loftesregister --bygg <datum>
```

Filen bär då sin egen SHA-256, räknad över filen utan just den raden, och varje dokuments PDF-hash
ur hämtmanifestet. `tests/test_loftesregister_2022.py` räknar om hashen och faller på en ändrad
bokstav.

Efter låsningen ändras ingen post. Enda öppningen är en **errata-rad** för ett avskrivningsfel som
går att belägga mot PDF:en, med datum och skäl (beslut 8). Fältet `errata` finns i filen och är
tomt.
