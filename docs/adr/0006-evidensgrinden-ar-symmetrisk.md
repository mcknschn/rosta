# ADR 0006: evidensgrinden är symmetrisk och sökningen är riktningsblind

- Status: accepted
- Datum: 2026-08-21
- Beslutad i: biljett [#18](https://github.com/mcknschn/rosta/issues/18) under karta [#6](https://github.com/mcknschn/rosta/issues/6)
- Bygger på: [ADR 0002](0002-kategoripoangens-ansprak-och-vikter.md), [ADR 0003](0003-skiljbarhet-och-kanslighetsanalys.md) och [ADR 0004](0004-vad-delpoang-b-mater.md)

## Kontext

ADR 0004 punkt 4 i diagnosen fann att `config/evidence_ledger.yaml` lutar åt ett håll: 46 poster,
varav 42 `positive`, 3 som ger noll och 1 `negative`. Den ADR:n avgjorde inte lutningen. Den skrev
att rättningen kräver nya liggarposter med källor, alltså ett bygge och inte ett beslut, och lade
frågan i en egen biljett.

Biljett #18 ställde två frågor. Gör lutningen B partisk? Och vad är den neutrala rättningen, givet
att sökandet efter nya poster i sig kan vara en partisk handling?

## Diagnos

Mätt 2026-08-21 mot `config/`, `pipeline/` och `docs/done/fas4c_rubrik.md`.

1. **Lutningen är total, inte nästan total.** De fyra icke-positiva posterna är alla inerta.
   `internationella_materielsamarbeten`, den enda `negative`, har noll partirader och är dessutom
   lyft ur täckningsnämnaren via grunden E1. `jobbskatteavdrag`, `riktat_likvardighetsbidrag` och
   `situationell_prevention_kamerabevakning` har också noll partirader. Alla **282 av 282**
   evidence_effect-claims som matar B kommer därmed ur en `positive`-post. 250 behåller postens
   riktning och 32 vänds av `opposes` via `_FLIP` i `pipeline/positions.py`. Den negativa grenen
   nås bara av motstånd, aldrig av evidens.

2. **Lutningen är en regel vi själva skrev.** `docs/done/fas4c_rubrik.md` §5 håller en
   `direction: negative`-post till `evidence_level ∈ {authority_evaluation, systematic_review}`,
   `confidence ≥ medium` och exakt indikator utan sidoeffekt-proxy. En `positive`-post har ingen
   sådan grind. **13 av 42 positiva poster skulle falla på den grind som gäller negativa.**
   Sökningen som lade dem hette dessutom B-grön-svepet, och mandatet var minst en grön post per
   undermått.

3. **Grindens enda nedskrivna skäl har fallit.** Rubriken motiverar asymmetrin med att "ett
   uteblivet eller för svagt positivt bidrag inte straffar ett parti på samma laddade sätt". Det
   var sant när B var `tecken(stance) x täckning`, för då gav en svag positiv post `+1`, alltså
   5,00. Efter ADR 0004 ger samma post `effect_strength: low`, alltså 0,3 och betyget **3,25**.
   Den drar nu ned. 77 av 228 celler innehåller bara sådana svaga claims, och ingen cell blandar
   svagt med starkt.

4. **Grinden vid dörren är fortfarande den enda skärmen mot svag evidens.** `net = Σ(q·m) / Σ q`,
   så i en cell med ett enda claim tar `q` ut sig och `net = m`. **184 av 228 celler har exakt ett
   claim.** `evidence_level` och `confidence` rör alltså inte poängen i 81 procent av cellerna. De
   når bara säkerhetsetiketten via `scorerun._b_confidence`, som räknas per kategori. Att avskaffa
   grinden och låta formen sköta kvaliteten går därför inte.

5. **Priset för att tillämpa grinden är stort och behövde mätas före beslutet.** Aktivt
   täckningsläge är `weighted_submeasure_depth`, så nämnaren räknas per undermått. Lyfter man ut de
   13 posterna töms **10 av 29 undermått** på varenda kodbar åtgärdstyp: `korruption_tillit`,
   `yttrandefrihet_medier` och `transparens_ansvar` i demokrati, `vard_tillganglighet` och
   `omsorg_personal` i välfärd, `civil_beredskap` och `ekonomisk_ambition` i försvar,
   `forebyggande` i trygghet, `realloner_hushall` i ekonomi samt `biologisk_mangfald` i klimat.
   Demokrati behåller två åtgärdstyper av sju. De 13 posterna **är** B-grön-mandatet.

Svaret på biljettens första fråga är därmed att lutningen är **vår regel och inte världen**. Om
världen också lutar går inte att pröva härifrån, och det står kvar som känd svaghet.

## Beslut

1. **Felet är grinden.** Rättningen riktar sig mot admissionsregeln, inte mot en hypotes om att
   svenska utvärderingar oftare studerar åtgärder någon trodde på. Den hypotesen kan vara sann men
   är inte prövbar med det underlag projektet har, och en rättning som vilar på den vore ett
   antagande förklätt till fynd.

2. **Grinden blir symmetrisk på den nivå som redan var frusen.** Varje liggarpost, oavsett verkan,
   kräver `evidence_level ∈ {authority_evaluation, systematic_review}`, `confidence ≥ medium` och
   evidens som avser exakt den betygsatta indikatorn utan sidoeffekt-proxy.

   Nivån är inte ny. Den sattes 2026-05-30 och frystes före allt det som står i diagnosen. Att
   välja den befintliga nivån i stället för att räkna fram en ny är det enda otaintade valet som
   står till buds, eftersom det nu är känt vilka 13 poster som faller. Skälet är detsamma som gav
   ADR 0004 punkt 4 talen 0,3/0,6/1,0: det otaintade valet är det som gjordes innan någon visste
   vem det träffar. Vi väljer ingen nivå. Vi tillämpar en befintlig åt båda håll.

3. **Sökningen blir källstyrd och riktningsblind, uppräknad per indikator.** En sökning som frågar
   "vilka åtgärder har negativ evidens?" vet vad den vill hitta innan den letar. Den ersätts av en
   sökning som går över **utvärderingar för en given indikator**, där verkan blir vad utvärderingen
   fann. Riktningen finns då inte i sökbegreppet alls och kan därför inte tiltas.

   Indikatorn är enheten, eftersom punkt 2 redan kräver att evidensen avser exakt den betygsatta
   indikatorn. Undermått är för grovt för den grinden.

   **B-grön-mandatet avvecklas.** Kravet på minst en grön post per undermått är samma fel med
   omvänt tecken: ett sökbegrepp som bär en riktning.

4. **Ordningsregel mot att sökaren ser vem posten träffar.** Verkan, effektstyrka och evidensnivå
   låses och skrivs ned **innan** partiraderna för åtgärdstypen slås upp, och svepet loggar att det
   skedde i den ordningen. Regeln biter bara på nya åtgärdstyper. För de 44 som redan står i
   liggaren är partiraderna kända, och den kunskapen går inte att ta tillbaka. Den begränsningen
   skrivs ut i stället för att döljas.

5. **Svepet först, utlyftet av de 13 sedan.** De 13 posterna lyfts inte förrän det källstyrda
   svepet har gett de tömda undermåtten en chans att fyllas med poster som klarar grinden. Skälet
   är inte att skona utfallet utan att lägga bevisbördan rätt: hittar svepet ingen admissibel post
   för `korruption_tillit`, då är tystnaden ett fynd om evidensläget och inte en följd av vår egen
   regel. §6 i rubriken tillåter redan tystnad, men en tystnad som ingen prövat är inte samma sak
   som en tystnad som prövats.

6. **Grunden E1 skrivs om riktningsneutralt.** E1 heter i dag "sidoeffekt-negativ" och är
   formulerad bara för `direction: negative`. Efter punkt 2 är sidoeffekt-proxy ett fel oavsett
   verkan, så grunden blir "sidoeffekt-proxy" och gäller båda håll. Två grunder för samma fel vore
   samma asymmetri en gång till, bara på ett annat ställe.

7. **Godkännandetestet är ett regeltest.** Ändringen godkänns om **varje liggarpost passerar samma
   grind oavsett verkan**, testtvingat. Aldrig på att andelen claims ur positiva poster sjunkit
   under 100 procent. Ett sådant utfallstest vore ett täckningsmål på riktning, och §8 förbjuder
   täckningsmål uttryckligen. Att kräva att svepet ska hitta negativa poster är exakt samma fel som
   att kräva att det ska hitta positiva.

8. **Liggarens `direction` heter Verkan.** Ordlistan §4.3 har låst **Riktning** till
   `indicators[].direction`, alltså upp, ned eller målnivå. Liggarens fält är en annan storhet:
   om åtgärden rör indikatorn åt rätt håll relativt den riktningen. Ett ord för två storheter bryter
   mot ordlistans egen regel. Det kanoniska namnet blir **Verkan**. Confignyckeln `direction` ligger
   kvar tills en byggslice rör filen, på samma sätt som `A_agerande` och `C_ansvar`.

## Övervägda alternativ

- **Sänk den negativa grinden till den positiva nivån i stället.** Förkastat på diagnosen punkt 4:
  i 184 av 228 celler tar `q` ut sig, så evidensnivån når inte poängen. Utan grind vid dörren finns
  ingen skärm alls mot svag evidens i fyra av fem celler.

- **En tredje, lägre gemensam nivå.** Förkastat på ADR 0003 punkt 1. En nivå som räknas fram nu
  räknas fram med kännedom om vilka 13 poster som ligger vid gränsen, alltså går den inte att
  försvara utan att titta på utfallet.

- **Tillämpa grinden direkt och låt de 10 undermåtten tystna.** Tillåtet enligt §6, men förkastat
  som första steg. Utlyftet är stort nog att förtjäna en egen prövning per post, och ordningen i
  punkt 5 ger den utan att principen ändras.

- **Rikta svepet mot de 10 hotade undermåtten för att hinna före utlyftet.** Förkastat. Det är inte
  riktningsstyrt, men det är styrt mot just de undermått där vår egen regel skulle göra skada,
  alltså ett täckningsmål via bakdörren. §8 förbjuder det.

- **Ingen ändring.** Kartans notes tillåter utgången. Förkastad eftersom diagnosen punkt 3 visar att
  asymmetrins enda nedskrivna skäl föll när ADR 0004 byggdes. Att låta en regel stå kvar när dess
  motivering är borta är inte att avstå från en ändring, det är att göra en tyst ändring av vad
  regeln betyder.

## Vad beslutet inte rör

- **Anspråket i ADR 0002 står fast.** B svarar fortfarande på hur stor förbättring som väntas av de
  åtgärder partiet driver.
- **Formen i ADR 0004 rörs inte.** `net = Σ(q·m)/Σq` och talen 0,3/0,6/1,0 står oförändrade.
- **Vikterna 0,30/0,50/0,20 rörs inte.**
- **Ståndpunktssidan rörs inte.** Biljetten gäller liggarens innehåll. Reglerna för `supports` och
  `opposes` i rubriken §1 till §4 står oförändrade, och binär stance består.
- **Täckningskrympningen B5 rörs inte.** Utlyftet ändrar vad nämnaren innehåller, aldrig hur den
  räknas.
- **Världshypotesen avgörs inte.** Att officiella utvärderingar kan luta mot åtgärder någon trodde
  på står kvar som känd svaghet utan åtgärd.

## Följder

- Ingen kod-, config- eller liggarändring i den här ADR:n. Rankingen är oförändrad.
- `docs/done/fas4c_rubrik.md` bumpas till version 2. §5 skrivs om symmetriskt och §7 grund E1 blir
  riktningsneutral. Rubriken är en förregistrering, så ändringen redovisas i filen.
- Ordlistan i `docs/done/evidens_trovardighet.md` §4.3 får **Verkan** som eget begrepp bredvid
  **Riktning**.
- Bygget läggs som **en** slice, inte flera. Skälet är tvingande: testerna kan inte göras
  symmetriska medan de 13 posterna står kvar i liggaren, eftersom de då faller. Svepet, utlyftet,
  E1 och testerna delar därför en enda omkörning, på samma sätt som posterna i #15 gjorde.
