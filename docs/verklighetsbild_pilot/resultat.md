# Resultatet av Verklighetsbildpiloten

- Datum: 2026-09-13
- Kodbok: [`kodbok_pilot.md`](kodbok_pilot.md) version 1, låst i commit `36c3907`
- Förhandsregistrering: [`forhandsregistrering.md`](forhandsregistrering.md) version 1
- Räknat av: `python -m pipeline.tools.verklighetsbild --resultat`
- Talen i maskinläsbar form: [`config/verklighetsbild/resultat.yaml`](../../config/verklighetsbild/resultat.yaml)

**Piloten klarar inte tröskeln.** Avslagsskälet står i [`avslagsskal.md`](avslagsskal.md).

Piloten mätte två tal och inget annat: utbytet och reliabiliteten. Den kodade ingen sanning, och
ingenting nedan säger om ett parti har rätt.

## 1. Utbytet

| Tal | Värde |
|---|---|
| Designviktat utbyte | **0,054** prövbara relationer per utsaga |
| Tröskel | 0,20 |
| 95-procentigt intervall | 0,017 till 0,091 |
| Standardfel | 0,019 |
| Skattat antal relationer i hela bakåtmaterialet | 48 av 896 utsagor |

Tröskeln faller med bred marginal. Hela intervallets övre gräns, 0,091, ligger under halva
tröskelvärdet. Detta är ingen knapp miss som fler kodade utsagor skulle rätta till.

### 1.1 De fem talen

| Tal | Relationer |
|---|---|
| Kodare A | 14 |
| Kodare B | 10 |
| Delade | 10 |
| Unionen | 14 |
| **Snittet** | **12,0** |

Jaccardlikheten över indikatormängderna är 0,72.

Snittet avgör tröskeln, låst i förhandsregistreringen avsnitt 3. Varje relation kodare B fann var
en relation kodare A också fann. Oenigheten är alltså ensidig: A fann fyra relationer B inte såg,
och B fann ingen A missade.

### 1.2 Per parti

Snittet prövas mot kravet på minst 5 relationer hos samtliga åtta.

| Parti | Snitt | A | B | Delade | Utsagor med relation | Kategorier |
|---|---|---|---|---|---|---|
| S | 2,5 | 3 | 2 | 2 | 3 | 2 |
| M | 0 | 0 | 0 | 0 | 0 | 0 |
| SD | 2,0 | 2 | 2 | 2 | 2 | 2 |
| C | **5,0** | 6 | 4 | 4 | 4 | 2 |
| V | 0 | 0 | 0 | 0 | 0 | 0 |
| KD | 0 | 0 | 0 | 0 | 0 | 0 |
| MP | 2,5 | 3 | 2 | 2 | 3 | 3 |
| L | 0 | 0 | 0 | 0 | 0 | 0 |

**Ett parti av åtta når 5.** Fyra partier bär noll relationer i sina 25 kodade utsagor.

Kategorispridningen i sista kolumnen är diagnostisk och aldrig en stoppregel
(ADR 0016 beslutspunkt 8). Den skrivs ut utan omdöme.

Tröskelregel 5 kräver osäkerhetsintervall oavsett utfall. Andelen utsagor som gav minst en
relation, med ändlighetskorrektion enligt förhandsregistreringen avsnitt 2:

| Parti | Andel | Standardfel | 95-procentigt intervall | n / N |
|---|---|---|---|---|
| S | 0,120 | 0,054 | 0,015 till 0,225 | 25 / 72 |
| M | 0,000 | 0,000 | 0,000 till 0,000 | 25 / 300 |
| SD | 0,080 | 0,045 | 0,000 till 0,167 | 25 / 71 |
| C | 0,160 | 0,069 | 0,025 till 0,295 | 25 / 158 |
| V | 0,000 | 0,000 | 0,000 till 0,000 | 25 / 94 |
| KD | 0,000 | 0,000 | 0,000 till 0,000 | 25 / 55 |
| MP | 0,120 | 0,038 | 0,046 till 0,194 | 25 / 37 |
| L | 0,000 | 0,000 | 0,000 till 0,000 | 25 / 109 |

Ändlighetskorrektionen syns i talen. S och MP har samma andel, men MP:s intervall är smalare,
eftersom två tredjedelar av MP:s hela material är kodat mot en tredjedel av S:s.

**Begränsningen skrivs ut:** vid andelen 0 kollapsar det normala intervallet till en punkt och
säger ingenting. Fyra partier ligger där. Intervallet redovisas ändå, eftersom
förhandsregistreringen utfäste det, men `0,000 till 0,000` ska inte läsas som att saken är
avgjord för de fyra.

### 1.3 En lucka i tröskelreglerna

Tröskelregel 3 gäller 0 till 2 relationer och regel 4 gäller 3 eller 4. Snittet kan bli ett
halvtal, och S och MP landar på 2,5, alltså mellan de två banden. Förhandsregistreringen förutsåg
inte det fallet.

Luckan ändrar ingenting här. Regel 2 kräver minst 5, och varken S eller MP är i närheten oavsett
vilket band de hamnar i. Ingen totalundersökning enligt regel 4 utlöses, eftersom inget partis
snitt ligger på 3 eller 4. Luckan skrivs ned för att den ska vara lagad innan någon räknar om
detta.

### 1.4 Var relationerna fanns

De tio delade relationerna fördelar sig på fyra kategorier: ekonomi 5, välfärd 3, integration 1 och
försvar 1. Nio indikatorer bär dem, och `arbetsloshet` ensam bär fyra.

Tre av de sju kategorierna, alltså trygghet, klimat och demokrati, gav ingen enda delad relation.

## 2. Reliabiliteten

Krippendorffs alfa mellan kodare A och kodare B, över alla 200 utsagor.

| Moment | Skala | Alfa | Besked |
|---|---|---|---|
| Avgränsning | ordinal | 0,884 | håller |
| Prövbarhet | nominal | 0,850 | håller |
| Indikatorval | nominal | 0,853 | håller |
| Kodvärde | nominal | 0,677 | tentativt |

**Detta är resultatets viktigaste rad.** Prövbarhetens alfa är 0,850, alltså långt över
tröskelvärdet 0,667. Utbytestalet vilar därför inte på brus. Piloten faller på materialet och inte
på att kodarna var oense.

### 2.1 Förväxlingsmatrisen för prövbarhet

| A \ B | ja | nej |
|---|---|---|
| **ja** | 9 | 3 |
| **nej** | 0 | 188 |

188 av 200 utsagor bedömde båda kodarna som icke prövbara.

### 2.2 Förväxlingsmatrisen för kodvärdet

De vanligaste rutorna, av 16 förekommande par:

| A | B | Antal |
|---|---|---|
| `normativ` | `normativ` | 88 |
| `ingen_kompatibel_indikator` | `ingen_kompatibel_indikator` | 42 |
| `normativ` | `ingen_kompatibel_indikator` | 12 |
| `otillracklig_kontext` | `otillracklig_kontext` | 9 |
| `relation` | `relation` | 9 |
| `ingen_kompatibel_indikator` | `otillracklig_kontext` | 7 |
| `data_saknas` | `data_saknas` | 6 |
| `normativ` | `framtida_utfall` | 6 |
| `normativ` | `otillracklig_kontext` | 6 |

Kodvärdet är det enda moment som inte når 0,800. Oenigheten ligger nästan helt i gränsen mellan
`normativ` och `ingen_kompatibel_indikator`, alltså i frågan om ett led saknar mätbar kärna eller
bär en mätbar kärna som modellen råkar sakna indikator för. Den gränsen måste skärpas i
produktionskodboken.

### 2.3 Avgränsningen

109 av 200 utsagor gav ett enda led hos båda kodarna, och 44 gav två hos båda. Oenighet om
ledantalet är ovanlig och nästan alltid ett steg.

## 3. Delurvalet

Fyrtio utsagor kodades om blindat. Måtten nedan är parvis överensstämmelse på prövbarhet.

| Par | Leverantörer | Alfa |
|---|---|---|
| A mot A-prim | samma | 0,789 |
| B mot B-prim | samma | 1,000 |
| A-prim mot B-prim | olika | 0,789 |

**Detta är inget facit.** Det validerar ingenting och är ingen riktighet
(ADR 0016 godkännandetest 8). Måtten säger hur stabilt samma kodbok styr en kodare två gånger, och
ingenting om huruvida kodningen är riktig.

**Piloten saknar mänsklig kodare helt.** ADR 0016 beslutspunkt 5 lät projektägaren koda delurvalet.
Projektägaren avstod 2026-09-13, och avvikelsen är skriven i förhandsregistreringen avsnitt 5.1.
Instrumentet gör därför inget anspråk på mänsklig interkodarreliabilitet, och systematiska fel som
alla fyra kodningarna delar syns inte alls.

## 4. Vad som gick fel i kodboken

### 4.1 Kodboken motsäger sig själv

Avsnitt 6.5 säger att en matchning mot en indikator utan inläst serie ändå skrivs ut i
operationaliseringsfältet. Avsnitt 10 kräver att fältet är `null` när ledet inte är prövbart. En
kodare kan följa den ena regeln eller den andra, aldrig båda.

Tre kodare hittade motsägelsen oberoende av varandra och löste den åt olika håll. Åtta led i de
fyra kodningarna bär spåret.

Kodboken är låst och rättas inte i efterhand (godkännandetest 1). Motsägelsen redovisas i stället,
och den binder produktionskodboken om en sådan någonsin skrivs.

### 4.2 Kodvärdets gräns är för lös

Se avsnitt 2.2. Gränsen mellan `normativ` och `ingen_kompatibel_indikator` bär nästan hela
oenigheten i det moment som ligger lägst.

## 5. Godkännandetesterna

Alla tio reglerna i ADR 0016 är prövade i `tests/test_verklighetsbild_pilot.py` och passerar.

Ordningen mellan kodboken, tröskelvärdena och kodningen går att se på commit-datum, och testet
läser dem ur git i stället för att lita på en rad i filen.

## 6. Framåtkorpusens förhandsregistrering

Två av de 1 073 framåtposterna bär både en storhet och en period, alltså villkoret i ADR 0016
beslutspunkt 4. Båda är M:s, och båda säger att `fler brott utreds` under `nästa mandatperiod`.

Båda är bedömda 2026-09-13, före periodens slut, och bedömningen binder den som prövar dem efter
brytpunkten. Ingen av dem gav ett registrerat indikatorval:

| Post | Storhet | Prövade indikatorer | Utfall |
|---|---|---|---|
| `M-108` | antal brott som utreds | `uppklaringsgrad`, `handlaggningstid` | `ingen_kompatibel_indikator` |
| `M-117` | antal brott som utreds och leder till lagföring | `uppklaringsgrad`, `handlaggningstid` | `ingen_kompatibel_indikator` |

Skälet står i korpusfilen: utsagan räknar **antalet** utredda brott, medan `uppklaringsgrad` mäter
**andelen** uppklarade. Antalet kan stiga medan andelen faller, om anmälda brott stiger snabbare.
Kodbokens avsnitt 7.1 ger då ingen relation.

Att bara två poster klarar filtret är ett fynd om korpusens **form** och inte om partiernas löften.
Posten är rubriken, inte den fulla texten ur PDF:en. Noll poster bär ett årtal, och 22 bär över
huvud taget en siffra.

**En rättelse.** Filtrets storhetsprov krävde först ett tal eller ett storhetsord, och gav då noll
poster. Det provet var snävare än kodbokens eget, som i avsnitt 4 punkt 3 godtar `en riktning eller
en nivå`. Provet är rättat och följer nu kodboken. Det första talet var en artefakt av filtret.

## 7. Vad som inte gick att göra

- **Hämtmanifestets URL-fält är tomma.** Adresserna till de åtta PDF:erna skrevs aldrig ned vid
  hämtningen och står varken i mappningsfilerna, i biljett #42 eller i PDF-metadatan. De gissas
  inte. Hashen styrker vilket dokument som lästes men återskapar det inte.
- **Sidnumret saknas i 1 303 av 1 969 poster.** ADR 0016 beslutspunkt 3 kräver sida per post.
  Fältet är ifyllt för de 666 kandidaterna, som bär en sidmarkör i källfilen, men tomt för de 230
  mappade bakåtposterna och för alla 1 073 framåtposter. Källfilerna bär inget sidnummer för dem,
  så fältet går inte att fylla utan att läsa om PDF:erna. Det gissas inte.
- **Godkännandetest 6 kan inte belägga vem som kodade.** Testet prövar att två skilda kodningar
  finns, och de skiljer sig på 115 av 200 utsagor, alltså är de inte kopior av varandra. Vilken
  leverantör som skrev vilken vilar däremot på uppgiften i `leverantor`-fältet och på
  körningsspåret i `spar`. Codexkörningarna ligger som tio sessionsfiler under `CODEX_HOME`, på
  samma villkor som valmanifestens PDF:er: de går att peka på men inte att versionshantera här.

## 8. Två avsteg från specen, båda medvetna

1. **Blindningen gäller alla fyra kodarna, inte bara delurvalet.** ADR 0016 krävde blindning bara i
   steg 5. Utsage-id bär partikoden i sitt prefix, så kodbokens regel 11.4 om att aldrig väga in
   partiet vore annars ett löfte och ingen regel. Avsteget är strängare än specen, aldrig lösare.
2. **Avslagsskälet bär villkor för att ta upp frågan igen.** Biljetten krävde bara ett daterat
   skäl. Villkoren följer projektets eget mönster: ADR 0011 gav varje utesluten indikator ett
   `reopen_if` skrivet så att det går att pröva.
