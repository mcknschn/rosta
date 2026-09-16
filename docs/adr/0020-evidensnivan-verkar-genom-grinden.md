# ADR 0020: Evidensnivån verkar genom grinden, inte genom bandet

- Status: accepted
- Datum: 2026-09-16
- Beslutad i: biljett [#53](https://github.com/mcknschn/rosta/issues/53) under karta [#6](https://github.com/mcknschn/rosta/issues/6)
- Bygger på: [ADR 0003](0003-skiljbarhet-och-kanslighetsanalys.md), [ADR 0004](0004-vad-delpoang-b-mater.md), [ADR 0006](0006-evidensgrinden-ar-symmetrisk.md), [ADR 0008](0008-cellens-tackning.md), [ADR 0009](0009-sakerheten-mater-hur-val-talet-ar-kant.md), [ADR 0011](0011-uteslutningen-ar-ett-eget-besked.md), [ADR 0018](0018-bs-medelvarde-bar-inte-anspraket.md) och [ADR 0019](0019-kvoten-anvandes-over-fel-enheter.md)
- Preciserar: [ADR 0004](0004-vad-delpoang-b-mater.md) beslut 2 och [ADR 0009](0009-sakerheten-mater-hur-val-talet-ar-kant.md)
- Ändrar: [ADR 0019](0019-kvoten-anvandes-over-fel-enheter.md) beslut 12, som märkte bandet preliminärt

## Kontext

ADR 0019 rättade B:s form och bröt uttryckligen ut säkerhetsmodellen. Tre fel lämnades orörda,
eftersom de inte blockerade formrättelsen: att `evidence_level` aldrig når bandet, att
upprullningen påstods bära samma konstruktfel en nivå upp, och att bandets bredd var satt för en
skala som sedan byttes.

Biljett #53 skulle avgöra alla tre plus tio odeklarerade punkter. Två av dem visade sig vara fel
ställda. Ett tredje fel, som ingen letade efter, visade sig vara det allvarligaste.

## Diagnos

Mätt 2026-09-16 mot `config/`, `pipeline/`, `dist/scores.json` och elva omkörningar av den
faktiska pipen i minnet. Baslinjen i minnet stämde cell för cell mot den publicerade, noll
avvikelser på alla 56 celler och alla fyra delpoäng.

### 1. Evidensnivån når aldrig bandet, och kan inte nå det under dagens grind

Säkerhetsetiketten räknas ur enbart `confidence`. Fältets enda väg in i något tal går genom `q`,
där det förkortas bort för en ensam post. **112 av 151 celler bär exakt ett claim**, alltså 74
procent av materialet.

Rättelsen tycktes enkel: låt säkerheten bli `min(klass(evidence_level), klass(confidence))`.
Mätningen fäller den. Inträdesgrinden släpper bara in två evidensnivåer:

| evidence_level | påståenden |
|---|---|
| `authority_evaluation` | 175 |
| `systematic_review` | 22 |

Och per cell:

| | av 56 |
|---|---|
| celler där all evidens är `systematic_review` | **0** |
| celler där all evidens är `authority_evaluation` | 36 |
| celler med båda nivåerna | 20 |

Det ger två möjliga avbildningar, och båda misslyckas. Med `systematic_review` som hög och
`authority_evaluation` som medel blir **samtliga 56 celler medel**, och hög blir strukturellt
onåbar. Med båda som hög gäller `min(hög, confidence) = confidence`, alltså gör `evidence_level`
ingenting. Ordningen spelar ingen roll: `min` per påstående och `min` efter aggregering ger
samma utfall i båda avbildningarna.

Slutsatsen är inte att regeln är dålig. Slutsatsen är att grinden redan har gjort arbetet.

### 2. Bandet är 152 procent av spridningen

Halvbredden är `1,5 × Σ vikt × (1 − säkerhet)`. Konstanten 1,5 saknar härledning, vilket ADR 0003
punkt 6 redan skriver ut.

| | mätt |
|---|---|
| bandets fulla bredd, median | 0,975 |
| hela fältets spridning i kategoribetyg | 0,643 |
| bandet i andel av spridningen | **152 procent** |
| samma tal före ADR 0019 | 114 procent |

ADR 0019 tryckte ihop betygen. Bredden stod still. Bandet växte alltså i förhållande till det det
omsluter, utan att någon fattade ett beslut.

### 3. Säkerhetsskalan har nästan inga medlemmar

Dagens utfall för B: **7 höga, 27 medel, 22 låga**. Samtliga 22 låga kommer ur nedgraderingen vid
tunn täckning. Aggregatet självt kan bara ge hög eller medel, eftersom `conf_cat` alltid ligger i
[0,60, 0,85] under grinden. **Låg är en död gren i aggregatet.**

De 7 höga ligger alla i försvar. Var och en bär 3 råa rader men bara **2 distinkta
evaluationer**, eftersom `nato_medlemskap` och `dca_avtal_usa` är kodade ur samma
riksdagsdokument. Liggaren bär 29 distinkta `evaluation_id` över 32 poängberättigade poster.

### 4. Upprullningen är inte samma konstruktfel

Påståendet löd att en ny post på en tidigare tom indikator sänker `B_rått` i 42 av 56 celler.
Mätningen visar att riktningen avgörs av en brytpunkt. En ensam post ger ett fast indikatorbetyg
som bara beror på storleksklassen, och `B_rått` sjunker exakt när det betyget ligger under
cellens nivå:

| `effect_strength` | indikatorbetyg | `B_rått` sjunker | stiger | står still |
|---|---|---|---|---|
| unknown | 2,500 | 50 | 6 | 0 |
| low | 2,750 | **42** | 14 | 0 |
| medium | 3,000 | 20 | 28 | 8 |
| high | 3,333 | 5 | 51 | 0 |

Påståendets 42 av 56 motsvarar raden `low`, inte posten i allmänhet. Vilken storleksklass den
gamla mätningen använde är inte prövat, så ingen koppling hävdas.

Det publicerade talet går dessutom ofta åt andra hållet. I ett prövat fall sjönk `B_rått` i 7
celler medan publicerat B **steg** i 8, eftersom posten också höjde täckningen. Att mäta `B_rått`
ensamt ger fel tecken på det tal appen visar.

Rangordningen mellan partier stod still i samtliga elva prövade fall. Största partirörelse var
+0,0101, och avståndet M till KD i baslinjen är 0,0089. En enskild post kan alltså i princip
flytta ordningen. Ingen av de prövade gjorde det.

### 5. De två täckningsbegreppen går isär, och det är det verkliga felet

Krympningen vore likvärdig med att låta en omätt indikator bidra med neutralt betyg bara om
täckningen vore `Σ närvarande indikatorvikt / Σ all indikatorvikt`. Den räknar något annat:
viktat undermåttsdjup över kodade åtgärdstyper.

| | median | spann |
|---|---|---|
| krympningens tal | **0,500** | 0,075 till 0,850 |
| indikatorviktstäckning | **0,260** | 0,071 till 0,588 |
| differens | **+0,225** | −0,088 till +0,465 |

I **55 av 56 celler** krymper modellen mindre än en neutral imputering skulle kräva. Publicerat B
ligger genomgående längre från neutral än indikatortäckningen bär. Felet lutar mot överdriven
säkerhet, aldrig mot försiktighet.

Det här felet stod inte i biljetten. Det ersätter det som stod där.

## Beslut

1. **Evidensnivån verkar genom grinden, inte genom bandet.** Säkerheten bestäms **sekventiellt**:
   `evidence_level` avgör genom inträdesgrinden vilka påståenden som får bidra alls, därefter
   sätter `confidence` etiketten, därefter kan tunn täckning ge ett steg ned. `evidence_level`
   ingår **inte** som en separat numerisk komponent i bandaggregatet.

   Formuleringen i ADR 0004 beslut 2, att `evidence_level` och `confidence` tillsammans bär
   säkerheten, avser **den här kedjan** och inte två sammanslagna tal. Detta är dagens
   operationalisering, och den skrivs ut: **efter inträdet skiljer `evidence_level` inte mellan
   band.**

2. **Kombinationen är sekventiell och ordinal.** Den är varken additiv, multiplikativ, maxstyrd
   eller tabellerad. En kombinationstabell avvisas, eftersom den kräver ett omdöme per ruta som
   sedan medelvärdesbildas, alltså samma dolda kardinalisering en nivå upp som ADR 0019 tog bort
   en nivå ned.

3. **Bandet är heuristiskt, aldrig kalibrerat.** Bredden trimmas **inte** efter den observerade
   spridningen. Att välja bredden efter utfallet vore samma fel som ADR 0003 punkt 1 förbjuder.
   Bandet kallas hädanefter ett **heuristiskt osäkerhetsband** och aldrig ett kalibrerat
   intervall.

   ADR 0019 beslut 12 märkte bandet **preliminärt**. Den märkningen **ersätts** och lyfts inte:
   ett preliminärt tillstånd väntar på en rättelse, medan detta är en bestående egenskap. Fältet
   blir maskinläst och permanent.

4. **Att bandet är bredare än spridningen är inget fel, men det är inte heller ett bevis.** Att
   medianbandet är bredare än totalspridningen räcker **inte** för att säga att inga partier kan
   skiljas åt. Det kräver parvisa band och deras beroenden. Det räcker däremot för beskedet att
   instrumentets särskiljningsförmåga överlag är låg, och det beskedet ska stå i klartext och
   inte bara ritas som ett streck.

5. **Hög säkerhet kräver minst tre väsentligen oberoende evaluationer.** Grinden räknade råa
   kodade rader. En rad är inte en studie. Tre estimand ur samma studie är **en** studie.

   **Följden är mätt och godtagen före låsningen: hög säkerhet går från 7 celler till 0.**
   Onåbarheten är **empirisk och inte strukturell**. En enda ytterligare oberoende evaluation
   återställer nivån, och regeln stänger ingen dörr. Att sänka tröskeln till två är **uteslutet**,
   eftersom tröskeln då väljs efter att utfallet setts.

6. **Tre saker redovisas i klartext**, eftersom skalan annars ser ut att mäta mer än den gör:
   att hög kräver tre oberoende evaluationer och har **noll medlemmar i dag**, att låg bara
   uppstår genom täckningsnedgradering, och att aggregatet före nedgradering därför bara ger
   mellanläget.

7. **Väsentligen oberoende evaluation, operativ definition.** `evaluation_id` enligt ADR 0019
   beslut 10 är det **mekaniska golvet**: samma källa räknas en gång, oavsett hur många rader
   någon råkar skriva om den.

   Utöver det får en liggarpost bära ett fält som pekar ut **känt delat analysunderlag**. En
   pekare utan mottagare ger **hård fail**. **Saknas deklaration antas oberoende**, och det
   antagandet skrivs ut som en känd begränsning i stället för att döljas.

   Motsatsen, att anta beroende när inget sägs, avvisas: den gör hög säkerhet onåbar för alltid
   och byter en empirisk lucka mot en strukturell.

8. **Upprullningen bär inte samma konstruktfel, och punkten läggs ned.** Flera åtgärdstyper är
   skilda ingrepp vars effekter adderas i verkligheten, så summan var rätt en nivå ned. Flera
   indikatorer inom en kategori är **inte** ingrepp utan **aspekter som mäts** av samma storhet.
   Att mäta en aspekt till kan inte göra förbättringen större. Medelvärdet är rätt form.

   Att en post som säger att en åtgärd har liten effekt sänker betyget är **avsett lärande** och
   inget monotonicitetsbrott, precis som ADR 0019 beslut 2 redan skriver ut.

   Nedläggningen döljer ingenting: den renormerade nämnarens känslighet för smal
   indikatortäckning **kvarstår som känd modellrisk** och ägs av beslut 9. Att rangordningen stod
   still i elva prövade fall är stöd för empirisk robusthet, **aldrig bevis för
   konstruktvaliditet**.

9. **De två täckningsbegreppen ska valideras, inte tyst byggas om.** Krympningen räknar kodade
   åtgärdstyper. Medlet räknar indikatorer med värde. De går isär med median 0,225, ensidigt.

   Felet är i första hand att vi **tolkar** krympningen som något den inte gör. Tolkningen skrivs
   rätt först: krympningen mäter **evidensdjup**, aldrig neutral imputering av saknade
   indikatorer. Om måtten ska föras samman är det en **skaländring med omkörning**, på samma
   villkor som en ändring av `R`.

10. **En post utan känd storlek står utanför `B_rått`.** Okänd effektstorlek är **frånvaro av en
    skattning**, aldrig en skattning om exakt neutral verkan. En sådan post får räknas mot en
    separat dokumentationstäckning, men aldrig som belägg för neutral verkan.

    **Mätt: 0 av 197 påståenden bär `m = 0` i dag**, och den enda `unknown`-posten i liggaren är
    inte poängberättigad. Regeln skrivs ändå nu, före medlemmar, eftersom ADR 0003 punkt 1 kräver
    att regeln står nedskriven före talet.

11. **Evidensklass och säkerhetsetikett hålls isär i datamodellen.** Evidensklassen finns kvar och
    används i grinden. Den ska därför hållas begreppsligt och datamässigt skild från etiketten,
    **även om den inte ingår i etikettkedjan**. Att slå ihop dem vore att låta en regel om
    inträde se ut som en regel om säkerhet.

12. **Evidenskvaliteten är teckenoberoende.** Den får inte skilja mellan positivt och negativt
    bidrag. Evidens verkar bara genom grinden, och grinden är symmetrisk sedan ADR 0006.

13. **Ordningen mellan klippning och viktning skrivs ut som rådande.** Klippning sker per
    indikator, därefter viktning, därefter en yttre klampning. Ordningen ändras inte här.

14. **Tunn mot tillräcklig skrivs ut som rådande.** Viktat undermåttsdjup under 0,50 ger ett steg
    ned i säkerhetsnivån. Definitionen **ärver den öppna valideringen i beslut 9**, eftersom den
    läser samma storhet.

15. **Varningsfärgen utlöses bara av uttryckligt låg.** Saknade och ej tillämpliga värden utlöser
    ingenting. `conf-low` läser aldrig C, vilket ADR 0009 redan låser.

16. **Saknad kvalitetsklass följer redan av ADR 0019 beslut 10 och biljett #50 D3.** Hård fail
    vid null, tomt, okänt, icke mappningsbart eller utanför domän, validerat före eller samtidigt
    med inträdet. Ingen ny regel införs.

17. **Medianvarianten läggs ned.** Ingen viktad median finns någonstans i poängkedjan, och den
    valda vägen inför ingen. Deklarationen saknar medlemmar.

## Vad som måste deklareras innan bygget räknar ett tal

ADR 0003 punkt 1 kräver att regeln står nedskriven innan talet räknas. Följande är låst av den
här ADR:n och får inte prövas om under bygget:

- Tröskeln **tre** oberoende evaluationer (beslut 5). Den valdes inte efter utfallet.
- Att `evaluation_id` är det mekaniska golvet och att frånvaro av deklaration betyder oberoende
  (beslut 7).
- Att bandets konstant **inte** rörs (beslut 3).
- Att upprullningens form **inte** rörs (beslut 8).
- Att de två täckningsbegreppen **inte** förs samman i det här bygget (beslut 9).

## Vad beslutet inte rör

- **Formen i ADR 0019 beslut 1.** Poolning inom åtgärdstyp, summa över typer, `K = R × m_max`.
- **`q` som relativ poolningsvikt**, aldrig amplitudfaktor.
- **Vikterna.** Att vikt inte är instrumentet för tvivel står i ADR 0015 punkt 3.
- **Inträdesgrindens bredd.** En vidare grind skulle göra en `min`-regel meningsfull, men det är
  en ändring av evidenspopulation, modell och skala. Den kräver eget beslut, ny kodning och
  omkörning, och behandlas aldrig som en rättelse inom det här arbetet.

## Kända invändningar som inte åtgärdas här

1. **Säkerhetsskalan har i praktiken ett värde.** Efter beslut 5 producerar aggregatet bara
   mellanläget, och de två ytterlägena nås bara utifrån: låg genom täckningsnedgradering, hög
   inte alls på dagens underlag. Skalan fungerar som en **prospektiv regel**. Den mäter dåligt i
   dag.

2. **Konstanten 1,5 saknar fortfarande härledning.** Beslut 3 säger bara att den inte trimmas
   efter utfallet. Kalibreringen ska prövas senare, oberoende av dagens spridning.

3. **Den renormerade nämnaren är en känd modellrisk.** Beslut 8 lägger ned påståendet om ett
   konstruktfel, aldrig risken. Beslut 9 äger den.

4. **Claim-id:t är inte unikt per liggarpost.** Nyckeln
   `claim:evidence_effect:{parti}:{typ}:{kategori}:{indikator}` gör att två poster på samma typ
   och indikator kollapsar till en rad i `evidence.json`. Betygen rörs inte, eftersom poolningen
   sker före nyckeln, men **provenansen visar bara den ena posten**. Det är ett spårbarhetsfel och
   läggs som egen biljett.

5. **`config/claims.yaml` beskriver fortfarande den gamla formen.** Raderna om
   `net_support = clamp(Σ(q·m)/Σq, -1, 1)` och `normalizer: sum_of_quality_weights` är inaktuella
   sedan ADR 0019. Rättas i bygget.

## Följder

- Bygget läggs som en egen biljett, på samma sätt som #50 byggde ADR 0019.
- Biljett [#53](https://github.com/mcknschn/rosta/issues/53) stängs av den här ADR:n.
- Betygen väntas **inte** röra sig. Besluten rör säkerhetsetiketten, bandets benämning och en
  grind som sänker sju celler ett steg. Vad som faktiskt händer mäts i bygget och redovisas som
  det blir.
- Underlaget är en grillning i fyra rundor, prövad mot en extern granskare i varje runda.
  Grillningen fällde bland annat: att `min(evidence_level, confidence)` kunde få in evidensnivån i
  bandet, att täckningskrympningen redan ägde den renormerade nämnaren, att upprullningen bar
  samma konstruktfel en nivå upp, att klass och etikett kunde slås ihop, och att ett band bredare
  än spridningen bevisar att partier inte kan skiljas åt.
