# ADR 0009: Säkerheten mäter hur väl talet är känt, inte vad talet säger

- Status: accepted
- Datum: 2026-08-26
- Beslutad i: biljett [#30](https://github.com/mcknschn/rosta/issues/30) under karta [#6](https://github.com/mcknschn/rosta/issues/6)
- Bygger på: [ADR 0002](0002-kategoripoangens-ansprak-och-vikter.md), [ADR 0003](0003-skiljbarhet-och-kanslighetsanalys.md) och [ADR 0008](0008-cellens-tackning.md)

## Kontext

Biljett #30 graderades ur [ADR 0008](0008-cellens-tackning.md) punkt 11, som fann konstanterna men
avstod från att rätta dem. `A` står på `high` i 56 av 56 celler och `C` likaså. Ingen cell avviker.

ADR 0008 delade cellens redovisning i två storheter. Täckning säger hur stor del av betyget som
vilar på mätt underlag, och den byggdes i [#29](https://github.com/mcknschn/rosta/issues/29).
Säkerhet säger hur säkert det mätta är, och den bärs av bandet. Den här ADR:n rör bara Säkerhet.

Biljetten ställde två frågor, en per delpoäng. Vad ska A:s säkerhet dras på? Och ska C ha en
säkerhet alls, när C väger 0 och inte kan flytta ett betyg?

## Diagnos

Mätt 2026-08-26 mot `dist/scores.json` vid `e13270e`, `config/scoring.yaml`,
`config/budget_ramar.yaml`, `pipeline/` och `web/app.js`.

1. **Premissen håller.** A står på `high` i 56 av 56 celler och C likaså. Talen är oförändrade
   genom tre omkörningar: `526c0a7` (#21), `ff2b2be` (#26) och `e13270e` (#29).

2. **ADR 0008:s tabell gäller före #26 och bär fel kolumnrubrik.** Den säger att B står på `low` i
   35 celler och `medium` i 21, aldrig `high`, och att bandet har fyra utfall. Sedan den
   symmetriska evidensgrinden (ADR 0006) står B på `low` i 22, `medium` i 27 och **`high` i 7**.
   Bandet har alltså sex utfall, inte fyra. Talen i tabellens kolumn "Halvbredd" är dessutom hela
   bredder: de uppmätta halvbredderna är 0,3000 · 0,3900 · 0,4875 · 0,5775 · 0,7125 · 0,8025,
   och ADR 0008:s 0,975 · 1,155 · 1,425 · 1,605 är exakt två gånger fyra av dem.

3. **A och C skiljer sig i art, inte i grad.** Halvbredden är `1,5 x Σ(vikt x (1 - säkerhet))`
   (`pipeline/score.py:385`). A väger 0,30 och bidrar därför med konstanta **0,0675** till varje
   halvbredd. `medium` skulle lägga till 0,1125 och `low` 0,2475, mot halvbredder som i dag löper
   0,30 till 0,8025. C väger 0, så dess term är **exakt 0,0000** oavsett nivå. A:s konstant är en
   term som inte varierar. C:s är ingen term alls.

4. **Beslutet kan inte flytta rangordningen, och det är prövat.**
   `default_subscore_certainty.A` är märkt `band_only` i `pipeline/robustness.py:146`, och
   `build_matrix` läser bara `score`. Två test låser paret:
   `test_band_only_kallor_ror_aldrig_betyget` prövar att källan aldrig flyttar ett betyg, och
   `test_band_only_kallor_nar_bandet` att den faktiskt rör bandet. Det skiljer den här frågan från
   ADR 0004 och ADR 0005, som båda fann konstanter i **betyget**.

5. **Configens skäl för A är halvt inaktuellt.** `config/scoring.yaml:242` säger
   `A: high # voteringar, budgetbelopp`. [ADR 0001](0001-a-mater-prioritering.md) flyttade
   voteringarna till B. Halva det nedskrivna skälet namnger ett underlag A inte längre har.

6. **A:s underlag är räknat, inte skattat.** a1:s ramar är transkriberade ur officiella källor och
   adversariellt verifierade, och varje ram citerar sin källrad (`config/budget_ramar.yaml`).
   a2 räknar motioner: den tunnaste cellen bär 84, medianen 509 och den största 4718. Ingen cell
   är tunn, och ingenting imputeras.

7. **A:s underlag är däremot inte likformigt i vad det mäter.** a1:s täljare täcker tre budgetår
   (2023-2025) mot en förankring på femton. I alla tre åren bär KD, L, M och SD
   `frame: regeringen`. **28 av 56 celler vilar alltså på partiets egen ram och 28 på den
   antagna.** För de fyra partierna mäter a1 inte partiets eget förslag.

8. **Biljettens tre kandidater håller olika bra.** `A_a1_active` står i 56 av 56, och a1-grinden
   släpper igenom alla sju kategorier, så den kandidaten byter en konstant mot en annan. Antalet
   år som bär ram är tre av femton i varje cell, alltså också en konstant. Bara `|q|` varierar:
   för a1 ligger 31 celler under 0,05, 16 mellan 0,05 och 0,15 och 9 mellan 0,15 och 0,30.

9. **C:s override finns men fyrar aldrig.** `category_c` sänker C ett steg bara när subnationell
   data saknas, med flaggan `C_missing_subnational`. Data finns för varje kategori, så C tar
   alltid defaulten. Flaggan förekommer 0 gånger i utdatan.

10. **C:s nivå är osynlig.** Den enda konsumenten av `confidence` utanför bandet är
    `web/app.js:294`, som sätter klassen `conf-low` när **någon** av de fyra nivåerna är `low`.
    C är aldrig `low`, så C:s nivå påverkar inte ens den. Klassen fyrar i 28 av 56 celler, och
    orsaken är alltid B eller D.

Svaret på biljettens båda frågor följer ur punkt 3, 6 och 7. A:s tal är väl känt i varje cell, och
det som skiljer cellerna åt är inte hur väl talet är känt utan vad talet mäter. C:s nivå är inte
en konstant som borde variera, utan en storhet som inte finns.

## Beslut

1. **Säkerheten mäter hur väl talet är känt, aldrig vad talet säger.** Det är regeln som avgör
   resten. En delpoäng vars underlag är räknat och fullständigt är väl känd även när talet den ger
   är nära mitten. Att ett parti ligger nära den historiska normen är ett fynd om världen, inte ett
   tecken på att vi vet talet sämre.

2. **A behåller `high` i varje cell. Konstanten är ett fynd, inte en form.** Skälet står i
   diagnosens punkt 6: ingenting i A skattas. a1 är transkriberat och citerar sin källrad, a2
   räknar motioner och den tunnaste cellen bär 84. En delpoäng där varje tal är räknat ur ett
   officiellt dokument **är** lika väl känd i varje cell, och då ska nivån säga det.

3. **`|q|` förkastas som säkerhetsstorhet.** Avståndet till nollpunkten mäter hur mycket A säger,
   inte hur väl A är känd. Att göra det till säkerhet vore en artförväxling enligt punkt 1, och den
   skulle dessutom bredda bandet mest för de partier som ligger närmast normen, alltså påstå att vi
   vet minst om det vi vet bäst.

4. **Fyndet i diagnosens punkt 7 är ett giltighetsfel, inte ett osäkerhetsfel, och det rättas inte
   här.** Att a1 för KD, L, M och SD är den antagna ramen betyder att A mäter fel storhet för dem,
   inte att den mäter rätt storhet sämre. Att möta det med ett bredare band vore att tapetsera över
   ett giltighetsfel med en osäkerhetsmarkering. Frågan ägs redan av
   [ADR 0007](0007-a-mats-over-samma-fonster-som-sin-forankring.md), vars villkorsklausul gör
   precis det här fallet prövbart, och bygget ligger som
   [#27](https://github.com/mcknschn/rosta/issues/27).

5. **C behåller sin nivå i utdatan, men den är overksam och det skrivs ut.** C är inte en delpoäng
   utan maktandel (ADR 0002), och en maktandel har en källa men ingen säkerhet som verkar. Fältet
   står kvar därför att en läsare som jämför de fyra delpoängen annars tappar en rad, och därför
   att `C_missing_subnational` fortfarande beskriver ett verkligt datatillstånd. Ordlistan §4.3 bär
   raden, på samma sätt som den bär att C inte ger poäng.

6. **`conf-low` slutar läsa C.** Följer direkt ur punkt 5: säger vi att C:s nivå är overksam ska
   den vara overksam överallt, inte bara i bandet. I dag är ändringen osynlig, eftersom C aldrig är
   `low`, men koden som skulle sänka C finns. A stannar kvar i läsningen, eftersom A väger 0,30.

7. **Skälet i configen skrivs om.** `A: high # voteringar, budgetbelopp` byts mot ett skäl som
   namnger det underlag A faktiskt har: transkriberade utgiftsramar och räknade motioner. Ett
   nedskrivet skäl som pekar på fel underlag är sämre än inget, eftersom det ser prövat ut.

8. **Ingen ny grind.** De tre lås beslutet vilar på finns redan, och en fjärde skulle kräva ett
   golv, till exempel ett minsta antal motioner per cell. Ett golv är en vald konstant, och ADR
   0005 och ADR 0007 vägrade båda välja konstanter. En ADR som inte ändrar något ska inte smyga in
   en konstant genom sitt test.

9. **ADR 0008:s tabell skrivs inte om, men båda felen står i diagnosen ovan.** En ADR är ett
   beslutsprotokoll och rättas inte i efterhand. Rättelsen står daterad här i stället, så att en
   läsare som möter tabellen hittar den.

## Godkännandetest

Beslutet ändrar ingen betygslogik, så testet är att de befintliga låsen står kvar. Alla tre finns
redan och namnges här så att de inte kan tas bort utan att någon möter den här raden.

1. `tests/test_robustness.py::test_band_only_kallor_ror_aldrig_betyget` med
   `default_subscore_certainty.A` som parameter: A:s nivå flyttar aldrig ett betyg.
2. `tests/test_robustness.py::test_band_only_kallor_nar_bandet` med samma parameter: A:s nivå rör
   faktiskt bandet, alltså är den ingen död knapp.
3. `tests/test_cell_coverage.py::test_c_raknas_aldrig`: C väger 0, vilket är det som gör C:s
   säkerhet overksam.

Efter byggslicen tillkommer ett test på punkt 6: en cell med `C` på `low` får inte ge
flaggkolumnen klassen `conf-low`, medan en cell med `A` på `low` ska ge den.

## Övervägda alternativ

- **Låta A:s säkerhet följa `A_a1_active`.** Förkastad. Flaggan står i 56 av 56 celler, så
  kandidaten byter en konstant mot en annan. Biljetten sade det själv.
- **Låta A:s säkerhet följa antalet år som bär ram.** Förkastad av samma skäl: talet är tre av
  femton i varje cell. Det skulle dessutom vila på ett fönster som ADR 0007 är på väg att flytta.
- **Låta A:s säkerhet följa `|q|`.** Förkastad, se beslutspunkt 3. Den enda kandidaten som
  faktiskt varierar, och den mäter fel sak.
- **Låta A:s säkerhet följa om cellen vilar på egen eller antagen ram.** Förkastad, se
  beslutspunkt 4. Den varierar (28 mot 28) och pekar på ett verkligt problem, men problemet är
  giltighet och inte osäkerhet.
- **Ta bort `C` ur `confidence`-objektet.** Förkastad, se beslutspunkt 5. Renast i modellen, men
  det är en schemaändring som kostar en läsare en rad utan att ge något tillbaka.
- **Grinda skälet med ett golv på A:s underlag.** Förkastad, se beslutspunkt 8.
- **Ingen ADR, bara en slutkommentar.** Förkastad. Beslutet är lätt att riva, men nästa läsare som
  ser `high` i 56 av 56 kommer att undra precis som den här biljetten gjorde, och då ska svaret gå
  att hitta i stället för att öppnas igen.
- **Sänka A ett steg rakt av, så att bandet inte påstår hög säkerhet överallt.** Förkastad. Det
  vore en vald konstant utan mätt skäl, och det bryter mot punkt 1: A:s underlag är räknat, så en
  lägre nivå skulle påstå något som inte stämmer.

## Vad beslutet inte rör

- Talen 0,85, 0,60 och 0,30 i `confidence_numeric`, låsta av ADR 0004.
- `max_interval_halfwidth` 1,5 och halvbreddens form, som hör till ADR 0003.
- B:s och D:s säkerhet, som härleds per cell och står orörda.
- Delpoängvikterna, låsta av ADR 0002.
- C:s skala och normalisering, som ägs av [#22](https://github.com/mcknschn/rosta/issues/22).
- Vad känslighetsanalysen drar i A:s ställe, som ägs av
  [#24](https://github.com/mcknschn/rosta/issues/24).
- Hur mycket A säger, alltså kompressionen, som ägs av
  [#28](https://github.com/mcknschn/rosta/issues/28).
- Täckningen, låst av ADR 0008.

## Följder

- **Byggslicen är liten och rör ingen betygslogik**: skälet i `config/scoring.yaml` skrivs om
  (beslutspunkt 7) och `conf-low` slutar läsa C (beslutspunkt 6). Ingen omkörning behövs, eftersom
  varken kommentaren eller klassen rör ett tal.
- **Ordlistan §4.3 bär raden om C:s overksamma säkerhet**, i avsnittet om cellens två redovisade
  storheter.
- **En koppling som ingen biljett skrivit ut**: fyrar ADR 0007:s villkorsklausul och a1 tas bort,
  faller A tillbaka på a2 ensam. Då ger ADR 0008 punkt 3 varje cell `a = 0,40` i stället för 1,00,
  och den visade täckningen sjunker i alla 56 celler. Raden läggs på #27, som är den biljett som
  kan utlösa det.
- **B når `high` sedan #26.** Kartans anteckning från #17, att ingen cell når B-säkerhet `high`,
  gäller inte längre. Det är den väntade följden av att den symmetriska grinden kräver `confidence`
  minst `medium` vid dörren, och den kräver inget eget beslut.
