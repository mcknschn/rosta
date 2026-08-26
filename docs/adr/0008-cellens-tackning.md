# ADR 0008: Cellens täckning är hur stor del av betyget som är mätt

- Status: accepted, punkt 5 ändrad 2026-08-26 av [ADR 0011](0011-uteslutningen-ar-ett-eget-besked.md)
- Datum: 2026-08-23
- Beslutad i: biljett [#12](https://github.com/mcknschn/rosta/issues/12) under karta [#6](https://github.com/mcknschn/rosta/issues/6)
- Bygger på: [ADR 0002](0002-kategoripoangens-ansprak-och-vikter.md), [ADR 0003](0003-skiljbarhet-och-kanslighetsanalys.md) och [ADR 0004](0004-vad-delpoang-b-mater.md)

## Kontext

Biljett #12 kommer ur punkt 7 i issue [#1](https://github.com/mcknschn/rosta/issues/1). Varje cell
bär i dag fyra säkerhetsnivåer och en flagglista. Det saknas en sammanfattande grad per cell, och
biljetten frågade vilken regel som väger ihop signalerna till en sådan grad.

Biljetten ställde två följdfrågor. Ska graden härledas ur befintliga flaggor, eller får den ta in
nytt? Och vad händer visuellt vid låg grad, eftersom en grad som göms bland flaggorna gör ingen
nytta?

## Diagnos

Mätt 2026-08-23 mot `dist/scores.json`, `config/`, `pipeline/`, `web/` och `schemas/`.

1. **Cellen har redan en sammanvägd grad, och det är bandet.** Halvbredden räknas som
   `1,5 x Σ(vikt x (1 - säkerhet))` (`pipeline/score.py:386`). Bandet är alltså precis den
   hopvägning av de fyra säkerhetsnivåerna som biljetten efterfrågar.

2. **Två av de fyra nivåerna är konstanter.** A står på `high` i 56 av 56 celler och C likaså.
   `overrides` i `pipeline/scorerun.py:813` sätter bara B, C och D, och A överskrids aldrig utan tar
   alltid defaulten. C:s override är `high` utom när en datafil saknas.

3. **De två övriga når aldrig taket.** B står på `low` i 35 celler och `medium` i 21, aldrig `high`.
   D står på `low` i 12 och `medium` i 44, aldrig `high`. Fyra tillstånd av nio förekommer.

4. **Alltså rör bara B och D bandet.** C väger 0 sedan ADR 0002, så dess säkerhet räknas bort ur
   summan, och A är konstant. Bandet är en uppslagning med fyra utfall:

   | B | D | Halvbredd | Celler |
   | --- | --- | --- | --- |
   | medium | medium | 0,975 | 18 |
   | medium | low | 1,155 | 3 |
   | low | medium | 1,425 | 26 |
   | low | low | 1,605 | 9 |

5. **Täckningen finns i utdatan, men bara som strängar.** B och D delar nämnare per kategori, alltså
   kategorins samlade undermåttsvikt: 73 för ekonomi och 100 för de sex övriga. Alla 56 celler har
   en `B_coverage_*`-flagga. Sex saknar `D_coverage_*`, och det är exakt V:s sex
   `D_not_applicable`-celler. Talen löper brett, från `B_coverage_30/100` till `B_coverage_100/100`.

6. **Två av biljettens kandidatindata finns inte som fält.** Ordet proxy står bara i fritext i
   `note:`-strängar i `config/categories.yaml`. Om en källa är handkodad eller maskinellt hämtad
   finns inte alls som data, bara i verktygsnamn och kommentarer.

7. **Den visuella behandlingen är nästan osynlig.** `conf-low` färgar flaggkolumnen i detaljtabellen
   med `--warn` (`web/app.js:294`, `web/style.css:69`). Den fyras när någon av de fyra nivåerna är
   `low`, alltså i varje cell, eftersom D är `low` i 12 och B i 35. Kolumnen dumpar upp till fyra
   strängar per rad, och tre av dem är rena täckningsfakta.

Svaret på biljettens fråga följer ur punkt 1 och punkt 5. Säkerheten är redan sammanvägd, och
bandet är den sammanvägningen. Täckningen är inte sammanvägd alls. Det som saknas är alltså inte en
grad över alla signaler, utan en grad över den signal som ännu står oläst.

## Beslut

1. **Storheten heter Täckning, och den mäter hur stor del av cellens betyg som vilar på mätt
   underlag.** Den säger inget om hur säkert det mätta är. En fullt täckt cell kan vila på svag
   evidens, och då är det bandet som bär beskedet. De två storheterna svarar på skilda frågor och
   hålls isär.

2. **Täckningen räknar A, B och D. C räknas aldrig.** C väger 0 och har ingen täckningsstorhet.
   Anspråket i punkt 1 gäller cellens betyg, och C ingår inte i betyget.

3. **A:s täckning är 100 när `A_a1_active` står och 40 när `A_a2_only` står.** Grinden i
   `pipeline/budget.py` släpper in a1 bara när alla åtta partier har verifierad ram för varje
   utgiftsområde i kategorin. Faller a1 ur vilar A på a2 ensam, och a2 väger 0,4 av A. Talet är
   konstant 100 i dag, och just därför skrivs regeln nu: den ska vara rätt den dag grinden stänger.

4. **En ej tillämplig D räknas som 0 täckt, aldrig bort ur nämnaren.** Precedensen är
   `docs/done/d_coverage_krympning_spec.md`, som slutade renormalisera bort saknade undermått för
   att en cell inte ska göra ett helt kategorianspråk på en delmängd. Samma aritmetik gäller ett steg
   upp. Faller D ur nämnaren får en cell utan utfallsdata samma täckning som en fullt mätt cell, och
   då mäter storheten ingenting. Skälet följer med som etikett: ej tillämpligt är inte samma sak som
   saknat, och V straffas inte i betyget, precis som förut.

5. **Vikterna är ADR 0002:s delpoängvikter.** Täckningen är `0,30 x a + 0,50 x b + 0,20 x d`, där
   `a`, `b` och `d` är per-delpoängstäckningen på kategorins egen nämnare. De tre summerar redan
   till 1,00 eftersom C väger 0, så ingen omnormalisering behövs. Ingen konstant väljs här. Ett
   ovägt medel skulle påstå att A:s täckning betyder lika mycket som B:s, fast A väger 0,30 och B
   0,50, och det motsäger anspråket i punkt 1.

   > **Ändrad 2026-08-26 av [ADR 0011](0011-uteslutningen-ar-ett-eget-besked.md) punkt 9.**
   > "Kategorins egen nämnare" var samma tal som B och D krymper mot neutral med, alltså 73 för
   > ekonomi och 100 för de sex övriga, och `B_coverage`-flaggan bar det. Nu är det två tal.
   > Täckningen räknas över kategorins **fulla** undermåttsvikt, alltså 100 för var och en av de
   > sju, och ett uteslutet undermått räknas 0 täckt i stället för att strykas ur nämnaren.
   > Krympningens nämnare står orörd, så inget betyg rör sig. Vikterna, formeln och allt annat i
   > den här punkten står kvar. Regeln är punkt 4:s egen, tillämpad på ett hål till: en ej
   > tillämplig D räknas likaså 0 täckt och faller aldrig ur nämnaren. Byggd i biljett
   > [#34](https://github.com/mcknschn/rosta/issues/34).

6. **Täckningen redovisas som ett tal, utan tröskel.** ADR 0003 punkt 3 avgjorde samma sak för
   andelen metodvarianter: andelen står som den är, så listan och brasklappen slutar säga emot
   varandra. Sajtens andra redovisade storhet av samma slag följer samma regel. Tre nivåer skulle
   kräva två gränser, och bara en finns (`thin_coverage_threshold` 0,75). Den andra vore vald, och
   ADR 0005 och ADR 0007 vägrade båda välja konstanter.

7. **Täckningen har ingen verkan på betyget.** Den ändrar inte poäng, band eller rangordning. Tunn
   täckning verkar redan på modellen genom `thin_coverage`, som sänker säkerheten ett steg och
   därmed breddar bandet. Låter vi täckningen verka en gång till räknas samma fråga två gånger, och
   ordlistan §4.3 förbjuder det uttryckligen.

8. **Täckningen räknas i pipen, som ett nytt fält på cellen i `scores.json`.** `web/score.js:2`
   säger att frontend endast får vikta och summera förberäknade kategoribetyg, och att ingen
   A/B/C/D-logik får ligga där. Täckningen är A/B/D-logik. `categoryScore` i
   `schemas/scores.schema.json` har `additionalProperties: false`, så fältet blir en uttrycklig och
   testbar schemaändring i stället för ett underförstått tillägg.

9. **Talet får en egen kolumn i detaljtabellen och suger upp de tre täckningsflaggorna.**
   `A_a1_active`, `A_a2_only`, `B_coverage_*` och `D_coverage_*` utgår ur flaggkolumnen, eftersom
   kolumnen då säger samma sak som talet fast sämre. Kvar i flaggkolumnen står det som inte är
   täckning: `D_not_applicable`, `D_thin_basis`, `B_no_party_evidence`,
   `C_national_only_by_design` och `D_subnational_region_*`. Tröskelflaggorna `B_thin_coverage` och
   `D_thin_coverage` stannar också kvar, trots att de går att härleda ur talet, eftersom de markerar
   en åtgärd i modellen och inte bara ett faktum.

10. **Nya fält tillåts, men bara maskinellt avgörbara.** Ett fält som kräver ett omdöme per
    indikator förkastas. Skälet är repots hårdaste regel: inget partibetyg sätts för hand. En
    handsatt markör är inget betyg, men den skulle flytta ett tal som visas för användaren, och det
    ligger nära nog för att kräva sitt eget skäl. Hämtningsmarkören ur diagnosens punkt 6 klarar
    ribban, eftersom den följer av vilken källmodul som körde. Proxymarkören gör det inte och
    förkastas.

11. **Fyndet i diagnosens punkt 2 namnges här men rättas inte här.** Att A och C står på `high` i
    varje cell är samma sorts fel som ADR 0004 fann i B och ADR 0005 i A, alltså en form och inte
    ett fynd. A väger 0,30 av bandet och bidrar med samma tal överallt. Rättningen kräver att två
    delpoängs osäkerhet härleds om, och det är en annan fråga än den här biljettens. Den ligger som
    [#30](https://github.com/mcknschn/rosta/issues/30).

12. **Regeln låstes innan talen räknades.** Vad regeln ger för täckning per cell räknades inte ut
    innan ADR:n skrevs. Kartans regel gäller: motivera och lås först, kör om sedan. Beslutet rör
    visserligen ingen rangordning enligt punkt 7, men samma disciplin gäller, eftersom påståendet
    "jag höll mig objektiv" är oprövbart när talen är kända.

## Godkännandetest

Ett regeltest, aldrig ett tal om hur hög täckningen blev.

1. **Betyg, band och rangordning står exakt still.** `score`, `ci` och `components` är byte-identiska
   för alla 56 celler före och efter slicen.
2. **Täckningen räknas som beslutspunkt 5 säger**, med per-delpoängstäckningen tagen på kategorins
   egen nämnare.
3. **V:s sex ej tillämpliga celler får `d = 0`**, och nämnaren är oförändrad. Ett test som klarar
   sig genom att utelämna D ur nämnaren ska falla.
4. **Schemat avvisar en cell utan fältet.**
5. **De tre täckningsflaggorna finns inte kvar i frontend-utdatan**, och de övriga flaggorna står
   orörda.
6. **Inget tal om hur hög täckningen blev ingår i testet.**

## Övervägda alternativ

- **Tre nivåer, hög, medel och låg.** Det var biljettens egen formulering. Förkastad, se
  beslutspunkt 6. En gräns finns redan och skulle ärvas, men den andra vore vald, och en vald
  konstant på ett visat tal är precis vad ADR 0003 punkt 3 tog bort.
- **Låta en ej tillämplig D falla ur nämnaren.** Förkastat, se beslutspunkt 4. Det vore samma fel
  som D-krympningen tog bort 2026-06-12.
- **Ovägt medel över de tre delpoängen.** Förkastat, se beslutspunkt 5.
- **Egna vikter för täckningen.** Förkastat. De skulle vara valda tal, och ADR 0002:s vikter finns
  redan och betyder just det som behövs här.
- **En proxymarkör per indikator.** Förkastad, se beslutspunkt 10.
- **Låta låg täckning sänka betyget eller bredda bandet.** Förkastat, se beslutspunkt 7.
- **Ingen storhet alls.** Övervägt på allvar. Bandet finns, och ADR 0003:s andel metodvarianter
  finns. Förkastat eftersom ingen av dem svarar på hur stor del av cellen som är mätt, och den
  frågan går i dag bara att besvara genom att tolka strängar.
- **En täckning för totalen på kortets framsida.** Inte förkastad, utan lämnad till
  [#11](https://github.com/mcknschn/rosta/issues/11), som äger den ytan. Den vore tekniskt tillåten,
  eftersom ett viktat medel av förberäknade tal är sådant frontend får räkna.

## Vad beslutet inte rör

- Vikterna 0,30 x A + 0,50 x B + 0,20 x D, C = 0 (ADR 0002).
- Säkerhetsnivåerna per delpoäng och talen 0,85, 0,60 och 0,30 i `config/scoring.yaml`.
- `thin_coverage_threshold` 0,75 och dess verkan på säkerheten.
- B:s och D:s egna täckningsberäkningar och deras nämnare.
- ADR 0003:s andel metodvarianter.
- Kortets framsida, som ägs av #11.
- A:s och C:s konstanta säkerhetsnivåer, som ligger som [#30](https://github.com/mcknschn/rosta/issues/30)
  enligt beslutspunkt 11.

## Följder

- **Bygget är en egen slice**, [#29](https://github.com/mcknschn/rosta/issues/29). Den här ADR:n
  ändrar ingen kod och ingen config. Rangordningen är oförändrad, och den ska förbli det även efter
  slicen enligt godkännandetestet.
- **Schemat måste ändras.** `categoryScore` har `additionalProperties: false`, så fältet läggs till
  uttryckligen i `schemas/scores.schema.json`.
- **A:s tal 40 ärver blandningen 0,6 x a1 + 0,4 x a2.** Biljett
  [#24](https://github.com/mcknschn/rosta/issues/24) kallar den blandningen A:s enda kvarvarande tal
  som är satt och inte uppmätt. Täckningens A-halva vilar alltså på en konstant som en annan biljett
  kan komma att röra. Ändras blandningen följer täckningen med av sig själv, så ingen låsning
  behövs här.
- **`B_no_party_evidence` ger B-täckningen 0.** Flaggan fyras aldrig i dagens utdata, men regeln
  säger vad som gäller om den gör det.
- **Ordet tillförlitlighet avförs som namn på storheten.** Det lovar att cellen är pålitlig, medan
  storheten mäter hur stor del som är mätt. Ordlistan §4.3 bär raden, på samma sätt som den bär
  varför "träffsäkerhet" och "faktiskt agerande" avfördes.
