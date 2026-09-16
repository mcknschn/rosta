# Pilotkodbok för Verklighetsbild

- Version: 1
- Status: **låst**
- Låst: 2026-09-13, före den första kodade utsagan
- Beslutad av: [ADR 0016](../adr/0016-verklighetsbild-avgors-av-en-pilot.md) beslutspunkt 6
- Byggs i: biljett [#46](https://github.com/mcknschn/rosta/issues/46), steg 1

Kodboken är enda gemensamma indata till de två modellkodningarna. Den ändras inte efter att den
första utsagan är kodad. Ändras den ändå, faller hela piloten och måste dras om.

## 1. Vad piloten mäter

Piloten mäter två tal och inget annat:

- **Utbytet.** Hur många prövbara relationer bär materialet per hundra kodade utsagor.
- **Reliabiliteten.** Hur väl två kodare som läser samma kodbok kommer fram till samma sak.

**Piloten avgör inte om ett påstående är sant.** Inget kodvärde i denna kodbok säger stämmer,
stämmer inte eller skev. De kodvärdena skrivs i produktionskodboken, och bara om tröskeln klaras
(ADR 0016 beslutspunkt 9). En kodare som ändå fäller ett omdöme om sanning har brutit mot
kodboken.

Kodaren jämför alltså aldrig ett påstående mot en siffra. Kodaren avgör bara om en sådan jämförelse
**skulle gå att göra**, och skriver ned mot vilken indikator, för vilken period och under vilken
operationalisering.

## 2. Analysenheten

Analysenheten är relationen

> `utsaga x indikator x tidsperiod x operationalisering`

En utsaga kan ge noll, en eller flera relationer (ADR 0016 beslutspunkt 1).

**Utsagan** är en rad i `docs/valmanifest_2026/mappning_bakat.md` eller
`docs/valmanifest_2026/kandidater_bakat.md`, med partiets egen lydelse. Utsagan är given och
kodaren ändrar den aldrig.

**Ledet** är den minsta del av utsagan som bär ett eget påstående. Atomiseringen i avsnitt 3 delar
utsagan i led.

**Relationen** uppstår när ett led klarar alla fyra proven i avsnitt 4 till 7.

## 3. Atomisering

Kodaren delar utsagan i led. Ett led är ett självständigt påstående om hur något är eller har
blivit.

### 3.1 Regler

1. **En storhet, ett led.** Bär meningen två storheter som kan röra sig åt olika håll, blir det två
   led. `Matpriser och hyror har stigit` ger två led: matpriser, hyror.
2. **En uppräkning som delar predikat delas.** `Långa köer och brist på nya bostäder` ger två led.
3. **Ett led delas aldrig i en storhet och ett värdeomdöme.** `För många elever lämnar skolan utan
   fullständiga kunskaper` är ett led. Värdeomdömet `för många` avgörs i avsnitt 4.
4. **En bisats som bara motiverar huvudsatsen är inget eget led.** `Fattigdomen har brett ut sig,
   vilket är oacceptabelt` ger ett led.
5. **Två meningar i samma utsaga ger minst två led**, om båda bär ett eget påstående.
6. **Ett led som upprepar ett tidigare led i samma utsaga räknas en gång.**
7. **Övre gräns: sex led per utsaga.** Bär utsagan fler, kodar kodaren de sex första i
   dokumentordning och skriver `fler_an_sex_led` i utsagans anteckningsfält. Gränsen finns för att
   avgränsningsmåttet ska ha en ändlig skala.

### 3.2 Vad avgränsningen mäter

Kodaren skriver ut varje led ordagrant som en sammanhängande del av utsagan. Antalet led per
utsaga är det som jämförs mellan kodarna (avsnitt 9, moment 1).

## 4. Prövbarhet

Ett led är **prövbart** när alla fyra svaren är ja:

1. **Påstår ledet något om utfallet i Sverige?** Ett förslag, en avsikt eller ett tidlöst
   värdepåstående är inte ett utfall.
2. **Bär ledet en storhet som går att mäta?** Priser, antal, andelar, väntetider, utsläpp och
   förtroende är storheter. `Sverige är på väg åt fel håll` är ingen storhet.
3. **Bär ledet en riktning eller en nivå?** `Har ökat`, `har minskat`, `är fortsatt långa`,
   `730 000 personer`. Ett led utan riktning och utan nivå är inte prövbart.
4. **Går ledet att läsa utan sin föregångare?** `Det gör oss sårbara` går inte.

### 4.1 Normativa led

Ett led där värdeomdömet **är** påståendet är inte prövbart. `Skatten är för hög` säger ingenting
om nivån, bara om talarens tycke om nivån.

Ett led där värdeomdömet sitter **på** ett mätbart påstående är prövbart, och kodaren prövar då
bara den mätbara kärnan. `För många elever lämnar skolan utan fullständiga kunskaper` prövas som
`andelen elever utan fullständiga kunskaper`, aldrig som `för många`.

Normativa led märks separat och sanningskodas aldrig mot statistik (ADR 0016 beslutspunkt 1).

### 4.2 Regeringsgärningar

`Vi har gjort det straffbart att inte avslöja tvångsäktenskap` är sant per definition. Ett led som
bara påstår att ett beslut fattats är **inte prövbart** i Verklighetsbild. Skälet är att beslutet
står i författningssamlingen och inte i en indikatorserie. Bortfallskoden är `normativ`.

Ett led som påstår ett **utfall** av beslutet är prövbart. `Vi har infört reformer så att en
barnfamilj får behålla 5 000 kr mer i månaden jämfört med 2022` påstår ett utfall.

### 4.3 Riktningsblindhet

Kodaren behandlar regeringspartier och oppositionspartier lika (ADR 0006). Ett led som svartmålar
någon annans period prövas med samma regler som ett led som skönmålar den egna. Partikoden är en
strataetikett och får aldrig påverka bedömningen av prövbarhet.

## 5. Tidsperiod

### 5.1 När texten anger perioden

Kodaren tar perioden ur texten. `Sedan 2022`, `de senaste åren`, `under mandatperioden`,
`jämfört med 2021`.

`De senaste åren` läses som **2022 till slutåret** enligt 5.2. Skälet är att alla åtta manifest
skrevs inför valet 2026 och att den period läsaren har i huvudet är mandatperioden.

### 5.2 När texten inte anger perioden

Bär ledet ingen period gäller **förvalsperioden**:

- **Referensår: 2022.** Regeringen Kristersson tillträdde 2022-10-18
  (`config/mappings.yaml`, `government_periods`).
- **Slutår: det sista år indikatorns serie bär en observation, dock högst 2025.**

Detta gäller även presensformer av typen `vårdköerna är fortsatt långa` och `arbetslösheten biter
sig fast`. Sådana led påstår att nivån vid slutåret skiljer sig från nivån vid referensåret.

### 5.3 När perioden inte går ihop

Namnger ledet en period som serien inte täcker, faller ledet på `period_saknas`. Detta gäller också
när ledet namnger en period som slutar efter slutåret i 5.2.

### 5.4 Framtida utfall

Ett led som gör anspråk på en period som ännu inte är slut faller på `framtida_utfall`. Detta gäller
oavsett hur väl ledet i övrigt passar en indikator.

## 6. Indikatormatchning

### 6.1 Var indikatorerna står

De 68 kanoniska indikatorerna listas i bilaga A och är hämtade ur `config/categories.yaml`. Kodaren
väljer bara ur den listan. En indikator som kodaren tycker borde finnas men inte gör det är ett
bortfall, inte en frihet att uppfinna en.

### 6.2 Vad som krävs för en matchning

Indikatorn matchar ledet när **båda** är sanna:

1. Indikatorn mäter samma storhet som ledet påstår något om.
2. Indikatorns population är ledets population, eller vidare på ett sätt kodaren kan skriva ut.

**Semantisk likhet räcker inte** (ADR 0016 beslutspunkt 3). Att ledet och indikatorn handlar om
skola gör dem inte till samma storhet.

### 6.3 Uteslutna indikatorer får matchas

Tre indikatorer bär ett `exclusion` i stället för en riktning (ADR 0011). De får ändå matchas i
Verklighetsbild. Skälet är att uteslutningsskälen gäller **betyget**, inte sanningen:

- **Gränsfel** säger att frågan redan ägs av en annan delpoäng. Det säger ingenting om huruvida
  påståendet stämmer. Detta gäller `forsvarsanslag_andel_bnp`.
- **Giltighetsfel** säger att utfallet inte kan tillskrivas ett parti. Verklighetsbild tillskriver
  ingenting, alltså biter skälet inte. Detta besvarar `inflation`.
- **Neutralitetsfel** säger att det bättre hållet inte går att ange utan att ta ett partis parti.
  Verklighetsbild behöver ingen riktning, bara en storhet och en period. Detta besvarar
  `statsskuld_underskott`.

Detta är svaret på biljett [#42](https://github.com/mcknschn/rosta/issues/42) punkt 5: **ja, både
`inflation` och `statsskuld_underskott` får prövas.** En utsaga om statsskuldens storlek faller
alltså inte på uteslutningen. Den faller däremot på `data_saknas`, eftersom ingen av de två har en
inläst serie.

Ett undermått kan också bära ett `exclusion`, och då bär det inga indikatorer alls. Så är det med
`klimat/industriell_konkurrenskraft`. Ett led om industrins konkurrenskraft har alltså ingen
indikator att matchas mot och faller på `ingen_kompatibel_indikator`, inte på uteslutningen.

### 6.4 Flera indikatorer passar

Passar två eller flera indikatorer **lika bra** och kodboken ger ingen skiljeregel, faller ledet på
`flera_operationaliseringar`.

Passar en indikator bättre än de andra, väljer kodaren den och skriver skälet i
operationaliseringsfältet. `Bättre` betyder närmare storhet och närmare population, aldrig närmare
partiets egen formulering.

### 6.5 Serien är inläst eller inte

Bilaga A anger per indikator om serien är inläst. Ett led som matchar en indikator utan inläst
serie faller på `data_saknas`. Matchningen skrivs ändå ut i operationaliseringsfältet, eftersom
hålet ska synas (ADR 0008 punkt 7, ADR 0011 punkt 9).

## 7. Operationalisering

Operationaliseringen är kodarens skrivna svar på frågan: **hur skulle detta led prövas mot denna
indikator?**

Den innehåller tre saker, i en mening vardera:

1. **Storheten.** Vad indikatorn räknar.
2. **Jämförelsen.** Referensår mot slutår, eller nivå vid slutåret.
3. **Populationen.** Vilka som ingår, och om ledet gäller en smalare grupp.

### 7.1 Oförenliga storheter

Är partiets storhet oförenlig med indikatorns finns ingen relation (ADR 0016 beslutspunkt 10).

Exempel ur ADR:ns egen diagnos: M skriver att vårdköerna minskat 40 procent och för talet
`antal som väntat över 90 dagar`. Projektets indikator `vardkoer` är **medianväntetid i dagar**.
Det är två storheter, inte två mätningar av samma storhet. Ledet faller på
`ingen_kompatibel_indikator`.

**Regeln är inte att projektets serie vinner över partiets.** Regeln är att det inte finns någon
relation att pröva.

### 7.2 När ledet är smalare än indikatorn

Gäller ledet en delmängd av indikatorns population och serien inte bryts ned på den delmängden,
faller ledet på `ingen_kompatibel_indikator`. `Arbetslösheten bland unga har ökat` mot
`arbetsloshet`, som är en totalserie, är ett sådant fall.

## 8. Bortfallskoderna

De sju koderna är låsta av ADR 0016 beslutspunkt 2. Ett led som inte ger en relation bär **exakt
en** av dem.

| Kod | Betyder |
|---|---|
| `framtida_utfall` | Ledet gör anspråk på en period som ännu inte är slut |
| `normativ` | Ledet bär inget prövbart utfallspåstående, eller är sant per definition |
| `otillracklig_kontext` | Ledet går inte att läsa utan sin föregångare |
| `ingen_kompatibel_indikator` | Ingen av de 68 mäter ledets storhet för ledets population |
| `flera_operationaliseringar` | Två eller flera indikatorer passar lika bra |
| `data_saknas` | Indikatorn matchar men serien är inte inläst |
| `period_saknas` | Serien täcker inte den period ledet gör anspråk på |

### 8.1 Företrädesordning

Passar flera koder, gäller den som står **först** i listan ovan. Ordningen är en tratt: först
frågar kodaren om ledet över huvud taget påstår ett avslutat utfall, sedan om det går att läsa,
sedan om det finns en indikator, sedan om den är entydig, sedan om den bär data, och sist om
perioden går ihop.

### 8.2 Från led till utsaga

Godkännandetest 4 i ADR 0016 kräver att **varje kodad utsaga** bär antingen minst en relation eller
exakt en bortfallskod.

- Ger minst ett led en relation, bär utsagan ingen bortfallskod.
- Ger inget led en relation, bär utsagan den kod som står först i företrädesordningen bland ledens
  koder.

## 9. De fyra momenten

Reliabiliteten räknas på fyra moment, alla med utsagan som enhet (ADR 0016 beslutspunkt 5).

| Moment | Värde per utsaga | Skala |
|---|---|---|
| 1. Avgränsning | Antal led | ordinal, 1 till 6 |
| 2. Prövbarhet | Ger utsagan minst en relation | nominal, ja eller nej |
| 3. Indikatorval | Utsagans **första** indikator i dokumentordning, annars `ingen` | nominal, 69 värden |
| 4. Kodvärde | Utsagans bortfallskod, annars `relation` | nominal, 8 värden |

Moment 3 räknas på den första indikatorn och inte på hela mängden. Skälet är att en
förväxlingsmatris över mängder inte går att läsa. Överensstämmelsen över hela mängden redovisas
separat som Jaccardlikhet, och den är ett beskrivande tal och ingen alfa.

**Kodvärdet i piloten är bortfallskoden.** Sanningskodvärdena stämmer, stämmer inte och skev ingår
inte i piloten, eftersom `skev` är förkastat i sin nuvarande form och de tre inte går att göra
ömsesidigt uteslutande innan utbytet är mätt (ADR 0016 beslutspunkt 9).

## 10. Vad kodaren lämnar ifrån sig

Ett YAML-dokument per kodare, med en post per utsaga i urvalets ordning:

```yaml
kodare: <id>
kodboksversion: 1
kodningsdatum: <ÅÅÅÅ-MM-DD>
utsagor:
  - utsaga_id: Sb-003
    anteckning: null
    led:
      - text: "Omkring 100 000 fler svenskar är arbetslösa idag än när tidöregeringen tillträdde"
        provbar: true
        indikator: arbetsloshet
        period: { start: 2022, slut: 2025 }
        operationalisering: "Antal arbetslösa enligt AKU. Nivå 2025 mot nivå 2022. Hela befolkningen 15-74 år."
        bortfall: null
    bortfall: null
  - utsaga_id: Cb-003
    anteckning: null
    led:
      - text: "Den ekonomiska tryggheten har minskat för alldeles för många svenska hushåll"
        provbar: false
        indikator: null
        period: null
        operationalisering: null
        bortfall: normativ
    bortfall: normativ
```

Fältregler:

- `provbar: true` kräver `indikator`, `period` och `operationalisering` ifyllda och `bortfall: null`.
- `provbar: false` kräver `bortfall` ifyllt och de tre andra `null`.
- `utsaga_id` skrivs av ur urvalet och ändras aldrig.
- `text` är en sammanhängande del av utsagans lydelse, ordagrant.
- `anteckning` är fritext eller `null`, och läses aldrig av någon räkning.

## 11. Vad kodaren aldrig gör

1. **Avgör aldrig om ett påstående är sant.** Piloten mäter utbyte och reliabilitet.
2. **Läser aldrig den andra kodarens svar.**
3. **Uppfinner aldrig en indikator** som inte står i bilaga A.
4. **Väger aldrig in vilket parti utsagan kommer från.**
5. **Ändrar aldrig partiets lydelse.**
6. **Lämnar aldrig en utsaga utan både led och kod.**

## Bilaga A: de 68 indikatorerna

Hämtad ur `config/categories.yaml` 2026-09-13. Kolumnen `Serie inläst` är `nej` för de 25
indikatorer som står i `config/coverage_allowlist.yaml`. Tabellen prövas mot configen i
`tests/test_verklighetsbild_pilot.py`, så att kodboken och modellen inte kan glida isär.

**Ekonomi och jobb** (`ekonomi`)

| Indikator | Undermått | Serie inläst |
|---|---|---|
| `sysselsattning` | `sysselsattning_arbetsloshet` | ja |
| `arbetsloshet` | `sysselsattning_arbetsloshet` | ja |
| `bnp_per_capita` | `bnp_produktivitet` | ja |
| `produktivitet` | `bnp_produktivitet` | ja |
| `realloner` | `realloner_hushall` | ja |
| `hushallens_reala_disponibla_inkomst` | `realloner_hushall` | ja |
| `naringslivets_investeringar` | `foretagande_investeringar` | ja |
| `inflation` | `inflation_prisstabilitet` | nej |
| `statsskuld_underskott` | `offentliga_finanser` | nej |

**Välfärd** (`valfard`)

| Indikator | Undermått | Serie inläst |
|---|---|---|
| `vardkoer` | `vard_tillganglighet` | ja |
| `vard_i_tid` | `vard_tillganglighet` | nej |
| `overlevnad_svar_sjukdom` | `vard_tillganglighet` | ja |
| `skolresultat` | `skola_kunskap` | ja |
| `skillnader_mellan_skolor` | `skola_kunskap` | nej |
| `behoriga_larare` | `skola_kunskap` | ja |
| `personalomsattning_omsorg` | `omsorg_personal` | nej |
| `kontinuitet_i_omsorgen` | `omsorg_personal` | nej |
| `brukarnojdhet_hemtjanst` | `omsorg_personal` | ja |
| `valfardsbrottslighet` | `finansiering_styrning` | nej |

**Lag och trygghet** (`trygghet`)

| Indikator | Undermått | Serie inläst |
|---|---|---|
| `dodligt_vald` | `grov_brottslighet` | ja |
| `skjutningar_sprangningar` | `grov_brottslighet` | ja |
| `brottsutsatthet` | `utsatthet_trygghet` | ja |
| `upplevd_otrygghet` | `utsatthet_trygghet` | ja |
| `uppklaringsgrad` | `rattsvasendets_effektivitet` | ja |
| `handlaggningstid` | `rattsvasendets_effektivitet` | ja |
| `aterfall_i_brott` | `aterfall_kriminalvard` | ja |
| `kommunalt_brottsforebyggande_arbete` | `forebyggande` | nej |

**Försvar och beredskap** (`forsvar`)

| Indikator | Undermått | Serie inläst |
|---|---|---|
| `forsvarsanslag_andel_bnp` | `ekonomisk_ambition` | nej |
| `forsvarsfinansiering_upptrappning_mot_mal` | `ekonomisk_ambition` | nej |
| `personal_varnpliktiga` | `militar_formaga` | ja |
| `personalstyrka_kontinuerligt` | `militar_formaga` | ja |
| `materiel_formaga` | `militar_formaga` | nej |
| `civil_beredskap_niva` | `civil_beredskap` | nej |
| `forsvarsvilja` | `civil_beredskap` | ja |
| `ukraina_stod` | `nato_ukraina` | ja |
| `materielleveransutfall` | `genomforbarhet_leverans` | ja |
| `leveranstid_materiel` | `genomforbarhet_leverans` | nej |
| `nato_interoperabilitet` | `nato_ukraina` | nej |

**Klimat, miljö och energi** (`klimat`)

| Indikator | Undermått | Serie inläst |
|---|---|---|
| `territoriella_utslapp` | `utslappsminskningar` | ja |
| `konsumtionsbaserade_utslapp` | `utslappsminskningar` | ja |
| `fossil_energianvandning` | `energi_elpriser` | ja |
| `elprisvolatilitet` | `energi_elpriser` | ja |
| `effektbrist` | `energi_elpriser` | ja |
| `utslappsminskning_per_krona` | `kostnadseffektivitet` | nej |
| `utslappsintensitet` | `kostnadseffektivitet` | ja |
| `hotade_arter_naturforlust` | `biologisk_mangfald` | nej |
| `hackande_faglar_skog` | `biologisk_mangfald` | ja |

**Integration och social sammanhållning** (`integration`)

| Indikator | Undermått | Serie inläst |
|---|---|---|
| `sysselsattningsgap_inrikes_utrikes` | `arbete_sjalvforsorjning` | ja |
| `sjalvforsorjningsgrad` | `arbete_sjalvforsorjning` | ja |
| `bidragsberoende` | `arbete_sjalvforsorjning` | ja |
| `sfi_sprakkunskaper` | `skola_sprak` | ja |
| `skolresultat_utsatta_omraden` | `skola_sprak` | nej |
| `trangboddhet` | `boendesegregation` | ja |
| `segregation` | `boendesegregation` | nej |
| `tillit_valdeltagande` | `normer_tillit` | nej |
| `mellanmansklig_tillit` | `normer_tillit` | ja |
| `atervandande_effektivitet` | `migrationssystem` | nej |
| `asyl_handlaggningstid` | `migrationssystem` | ja |

**Frihet, demokrati och institutioner** (`demokrati`)

| Indikator | Undermått | Serie inläst |
|---|---|---|
| `korruption` | `korruption_tillit` | nej |
| `fortroende_domstolar_myndigheter` | `korruption_tillit` | ja |
| `mediefrihet` | `yttrandefrihet_medier` | nej |
| `politisk_transparens` | `transparens_ansvar` | nej |
| `otillborlig_politisering` | `rattsstat_maktdelning` | nej |
| `overvakning_utan_rattssakerhet` | `personlig_frihet` | nej |
| `rattsstatsindex` | `rattsstat_maktdelning` | ja |
| `yttrandefrihetsindex` | `yttrandefrihet_medier` | ja |
| `privata_friheter` | `personlig_frihet` | ja |
| `horisontellt_ansvarsutkravande` | `transparens_ansvar` | ja |
