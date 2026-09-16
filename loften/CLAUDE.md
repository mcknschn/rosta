# Löftesspåret

Allt under `loften/` hör till detta spår. Projektets rot-CLAUDE.md gäller fortfarande för
språk, källor och skrivregler. Denna fil säger var spåret **avviker**.

Spårets form avgjordes 2026-09-16 i [#52](https://github.com/mcknschn/rosta/issues/52). De 34
besluten står med sina skäl i
[beslutsdokumentet](docs/beslut/2026-09-16-sparets-form.md). Denna fil bär reglerna i kort form.

## Frågan spåret ställer

**Vad lovar ett parti sina väljare inför ett val, och har partiet sedan arbetat med det löftet?**

Två leveranser:

1. **Kartan.** Vad partierna lovar. Ett läsbart löftesregister.
2. **Uppfyllelsen.** Har partiet lagt fram förslag och budgetar i linje med löftet.

Biljett: [#52](https://github.com/mcknschn/rosta/issues/52).

## Anspråket

Spåret mäter **löfte mot handling**. Aldrig löfte mot samhällsutfall.

Följden ska stå skriven i varje text spåret producerar:

> Ett parti som lovat något och sedan arbetat för det får en tumme upp, även om saken vore dålig
> för Sverige.

Om åtgärden var klok avgörs av delpoäng B och D i modellen, aldrig här.

En tumme ned betyder att partiet inte arbetat med löftet. Den betyder **aldrig** ohederlighet,
löftesbrott eller dålig politik.

## Fyra regler som binder

### 1. Framlagt räknas, genomröstat räknas inte

Ett parti som lagt fram sitt förslag och blivit nedröstat har arbetat med löftet. Det straffas
inte. Spåret läser vad partiet lade fram, aldrig vad som gick igenom.

### 2. Instrumentet följer positionen

Ett regeringsparti skriver ingen budgetmotion. Det lägger en budgetproposition. Mäts bara egna
motioner får de partier som styrde landet noll, vilket är bakvänt.

Därför gäller:

| Partiets läge | Vad som räknas som framläggande |
|---|---|
| Opposition | Partiets **partimotioner och kommittémotioner**, och egen budgetmotion |
| Regering | Regeringens propositioner och budgetpropositionen, **kollektivt på alla regeringspartier** |
| Stödparti | Samma som opposition. Den saknade budgetkanalen är en **lucka, aldrig en nolla** |

Detta är **ingen maktkorrigering i efterhand**. Båda lägena mäts med sitt eget instrument, så
ingen justering behövs efteråt.

**Enskild motion räknas aldrig.** Den är en ledamots papper och inte partiets. Fältet `subtyp` i
riksdagens dokumentlista bär skillnaden. Riksmötet 2023/24 lade M 612 enskilda motioner av 613,
och V 1 av 124. Detta avviker från hur `a2` räknar i modellen, där alla motioner ingår.
Avvikelsen är avsiktlig. Om `a2` bär samma fel är en egen fråga för en egen biljett.

**Budgeten läses som text**, aldrig som ramtal. Budgetmotionen och budgetpropositionen är dokument
som alla andra. Att pröva ett löfte mot en ram kräver en magnitud, och magnituden avvisas.

De två fall som stod olösta är avgjorda 2026-09-16: en koalitionsproposition bärs kollektivt
(RF 7 kap. 3 §), och ett stödparti mäts som opposition. Skälen står i beslut 15 och 17 i
[beslutsdokumentet](docs/beslut/2026-09-16-sparets-form.md).

### 3. Spåret väger 0 och rör aldrig rangordningen

Ingenting här påverkar modellens betyg, band eller rangordning. Vikterna 0,30 A + 0,50 B + 0,20 D,
C = 0 står orörda (ADR 0002). `dist/` skrivs aldrig av detta spår.

### 4. Utfall hör inte hit

Varje text som antyder att ett uppfyllt löfte är bra för Sverige är ett fel i spåret.

## Formen i korthet

Reglerna nedan binder lika hårt som de fyra ovan. Skälen står i
[beslutsdokumentet](docs/beslut/2026-09-16-sparets-form.md), med beslutsnumret inom parentes.

**Löftessidan**

- Posten följer dokumentets egen struktur, samma regel för båda årgångarna (3).
- Ovanpå ligger ett **atomiseringslager**: en post som bär flera skilda åtgärder styckas, med
  provet "kan det här bli två skilda motioner?", och ursprungspostens id står kvar (4).
- Registret dras om ur PDF:erna med full lydelse och sidnummer. Korpusen står orörd och blir en
  tredje oberoende genomgång (5).
- **Prövbart löfte** avgörs av handlingsprovet: posten namnger en åtgärd som går att lägga på
  papper. Bortfallet redovisas per parti (6).
- Kompletthet beläggs med **två blinda genomgångar**, tre differenstal per dokument, och
  projektägaren avgör varje differens innan låsning (7).
- Registret låses hårt och hashpinnat. Enda öppningen är en errata-rad för ett avskrivningsfel (8).
- Alla löften räknas, också de utanför de sju kategorierna (9).
- Spåret får en **egen, längre kategorilista**, men innehållet bestäms först när 2022 är mappat.
  Extraktionen bär inget kategorifält. En ärlig rest är tillåten (10, 11, 12).
- Båda årgångarna visas. 2026 utan kolumn för uppfyllelse, inte ens en tom (13).

**Handlingssidan**

- Perioden är hela mandatperioden 2022 till 2026 (21).
- Löften som inget riksdagspapper kan bära räknas bort ur nämnaren, och antalet redovisas per
  parti. Gränsen är snäv: kommun, region och EU ligger **innanför** (22).
- Pappret hittas genom sökning från löftet, plus ett omvänt stickprov som mäter vad sökningen
  missar (23).
- **Tummen är binär**, och kopplingen bär dokumentets id (24).
- Uppfyllelsen kodas i två blinda genomgångar (25).

**Redovisning**

- Talen räknas per parti och kategori, i **absoluta tal**. En cell utan löften skriver
  "inget löfte" (26).
- Maktläget står som etikett per parti och år, och regeringsår poolas aldrig med oppositionsår (27).
- Antalet konkreta förslag publiceras per parti som upplysning om nämnaren, aldrig som omdöme (28).
- Två filer per årgång, register och utfall. Celltalen räknas fram i kod till spårets egen utfil,
  aldrig till `dist/` (29).

**Kvalitet**

- Tre förhandsregistrerade prov: kodaröverensstämmelse, missgrad och **korsprovet**, alltså samma
  sökning mot ett annat partis papper (31).
- Faller ett prov läggs spåret **inte** ned. Talet publiceras inte, metoden lagas och körs om under
  ny förhandsregistrering med eget datum, och den fällda körningen ligger kvar i arkivet (32).
- Trösklarnas siffror sätts i förhandsregistreringen, innan en enda kodning görs (33).

**Bygget**

1. Mappa alla åtta valmanifest 2022. Hela registret, ingen pilot.
2. Kategorilistan, och flödestestet på **KD** från löfte till tumme (34).

## Förhållandet till projektets ADR:er

Projektets ADR:er binder **modellens delpoäng**. De binder inte detta spår. Spåret får sätta egna
regler, och motsägelser mot en ADR är tillåtna här.

Gränsen går vid skillnaden mellan beslut och faktum:

- Ett **beslut** i en ADR får spåret avvika från. ADR 0017 låste a1 till författarskap. Spåret
  behöver inte följa det.
- Ett **faktum om data** går inte att besluta bort. Att koalitionsår bärs av en delad ram är ett
  faktum. Spåret får välja hur det hanteras, aldrig att det inte gäller.

Avviker spåret från en ADR ska avvikelsen skrivas ned här, med skälet.

## Två lärdomar som binder

Båda kommer ur nedlagda mått i projektet och gäller här.

1. **Förhandsregistrera, och pröva talens ursprung.** Samstämmighet klarade alla tre trösklarna
   och mätte ändå fel sak. Profilavståndet korrelerade 0,998 med retorikens egen koncentration.
   Trösklar som bara prövar hur talen fördelar sig kan inte se var talen kommer ifrån. Varje
   förhandsregistrering i detta spår ska bära minst ett prov som pekar på ursprunget.
   Se [`docs/samstammighet_poc/nedlaggning.md`](docs/samstammighet_poc/nedlaggning.md).
2. **Korsläs kodboken innan den låses.** Pilotkodbokens avsnitt 6.5 stred mot avsnitt 10. Tre
   kodare hittade motsägelsen oberoende av varandra och löste den åt olika håll.
   Se [`docs/verklighetsbild_pilot/avslagsskal.md`](docs/verklighetsbild_pilot/avslagsskal.md).

## Mappen

Allt som rör spåret flyttades hit 2026-09-16, inklusive de två förkastade måtten.

```
loften/
  CLAUDE.md                        denna fil
  docs/beslut/                     spårets bärande beslut
  docs/loftesregister_2022/        instruktionen till genomgångarna, och rapporten
  docs/valmanifest_2022/           källdokumenten 2022. PDF:erna ligger utanför git.
  docs/valmanifest_2026/           källdokumenten 2026. PDF:erna ligger utanför git.
  docs/verklighetsbild_pilot/      FÖRKASTAT mått, nedlagt 2026-09-13
  docs/samstammighet_poc/          FÖRKASTAT mått, nedlagt 2026-09-16
  config/loftesregister_2022/      genomgångarna, differensen och det låsta registret
  config/verklighetsbild/          korpusarna, urvalet och pilotens resultat
  config/samstammighet_poc/        POC:ens resultat
  underlag/valmanifest_2022/       textunderlaget. Ligger utanför git.
```

Koden ligger kvar i `pipeline/tools/` och proven i `tests/`, eftersom de är paket och inte
dokument.

### De två förkastade måtten är arkiv

Dokumenten under `docs/verklighetsbild_pilot/` och `docs/samstammighet_poc/` **ändras aldrig**.
Två av dem är dessutom hashpinnade i sitt eget resultat, så en ändrad bokstav fäller ett prov.

Följden: deras relativa länkar skrevs före flytten. Står det `](../adr/...)` i en arkivfil menas
`docs/adr/...` i repots rot, inte en katalog under `loften/`. Länken lagas inte. Filen står som
den signerades.

Nya filer i spåret skriver förstås rätt länkar.

### Skillnaden mellan avslagsskäl och nedläggning

- **`avslagsskal.md`** betyder att måttet **föll på sin förhandsregistrerade tröskel**.
  Verklighetsbild gjorde det.
- **`nedlaggning.md`** betyder att måttet lades ned **av något annat skäl**. Samstämmighet klarade
  alla tre trösklarna, och lades ned därför att frågan byttes.

Ett prov i `tests/test_samstammighet_poc.py` vaktar skillnaden: ett mått som klarade sina
trösklar får inte bära ett avslagsskäl.

## Material

**Ligger i repot**

- `loften/config/verklighetsbild/korpus_framat.yaml`: 1 073 poster ur valmanifesten 2026, typen
  `detta ska vi göra`. Bär **rubriker och inte full text**. Noll poster bär ett årtal.
- `loften/config/verklighetsbild/korpus_bakat.yaml`: 896 poster, typen `detta är ett problem`.
- `config/budget_ramar.yaml`: partiernas egna föreslagna utgiftsramar, budgetåren 2011 till 2025.
- `loften/docs/valmanifest_2022/`: de åtta dokumenten inför valet 2022, inlagda 2026-09-16.
  **Alla åtta adresser är belagda** i `hamtmanifest.yaml`: varje URL hämtades om och den
  hämtade filens SHA-256 jämfördes byte för byte. V:s dokument heter `valplattform`, vilket
  är partiets eget ord för samma slags dokument.
- `loften/config/loftesregister_2022/register.yaml`: **löftesregistret 2022, 1120 poster**, låst
  och hashpinnat 2026-09-16 (#54). En rad per löfte med full lydelse, sidnummer och parti. Inget
  kategorifält (beslut 11). Bredvid ligger de **tre** blinda genomgångarna, differensen med
  projektägarens 15 avgöranden, och arkivet över den första låsningen på 729 poster. Den första
  låsningen band styckeregeln till hela dokumentet, vilket lät registret mäta typografi: andelen
  av dokumentets text som kom med gick från 27 procent hos M till 98 hos V. Version 3 av
  instruktionen flyttar regeln till avsnittsnivå, och spannet är nu 89 till 100 procent.
  Läsanvisningen står i
  [`docs/loftesregister_2022/registret.md`](docs/loftesregister_2022/registret.md).

**Saknas**

- Regeringens propositioner, som regel 2 kräver. Ingen kod i projektet hämtar dem i dag.

**Utanför git**

- `loften/underlag/valmanifest_2022/`: textunderlaget som registret dras ur. Det är hela det
  upphovsrättsskyddade verket, ord för ord, av samma skäl som PDF:erna. Bygg om det med
  `python -m pipeline.tools.loftesregister --underlag`.

Budgetåret 2026 ur bet. 2025/26:FiU1 stod här tidigare. Det **behövs inte** av spåret, eftersom
budgeten läses som text. Modellens `a1` behöver det fortfarande, men det är en annan biljett.

## Frysningen

Framåtkorpusen är fryst till brytpunkten **2030-09-08** (ADR 0016 beslutspunkt 4). Ingen post får
ändras, läggas till eller tas bort. Ingen post prövas mot ett utfall före brytpunkten.

Att läsa filen är tillåtet. Att välja formulering, indikator eller tröskel i efterhand är det
frysningen hindrar.

## Hämtning av dokument

**Skriv ned URL och hämtdatum samtidigt som filen sparas.** Adresserna till valmanifesten 2026
skrevs aldrig ned vid hämtningen. Den luckan upprepas inte.

Går en adress ändå förlorad finns en väg tillbaka: leta upp dokumentet, hämta det på nytt och
jämför SHA-256 byte för byte mot filen på disk. Stämmer hashen är adressen **belagd** och inte
gissad. Stämmer den inte skrivs ingen URL.

Den vägen användes 2026-09-16 för båda årgångarna. **Alla sexton adresser är belagda**, och
båda hämtmanifesten bär dem. Ingen hash rördes, eftersom en flytt av adress inte är en ändring
av innehåll.

Pilotens rapport säger fortfarande att fälten är tomma. Den står kvar oförändrad, eftersom den
beskriver vad som gällde 2026-09-13. Arkivet rättas inte i efterhand.

## Nedläggning är en godkänd utgång

Två mått i projektet har lagts ned med daterade avslagsskäl, och båda nedläggningarna var rätt
beslut. Faller detta spår skrivs ett avslagsskäl med prövbara återöppningsvillkor, i denna mapp.
