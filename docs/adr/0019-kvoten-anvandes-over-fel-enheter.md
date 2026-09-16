# ADR 0019: Kvoten användes över fel enheter

- Status: accepted
- Datum: 2026-09-16
- Beslutad i: biljett [#50](https://github.com/mcknschn/rosta/issues/50) under karta [#6](https://github.com/mcknschn/rosta/issues/6)
- Bygger på: [ADR 0002](0002-kategoripoangens-ansprak-och-vikter.md), [ADR 0003](0003-skiljbarhet-och-kanslighetsanalys.md), [ADR 0004](0004-vad-delpoang-b-mater.md), [ADR 0006](0006-evidensgrinden-ar-symmetrisk.md), [ADR 0008](0008-cellens-tackning.md), [ADR 0009](0009-sakerheten-mater-hur-val-talet-ar-kant.md), [ADR 0011](0011-uteslutningen-ar-ett-eget-besked.md) och [ADR 0018](0018-bs-medelvarde-bar-inte-anspraket.md)
- Ändrar: [ADR 0004](0004-vad-delpoang-b-mater.md) beslut 3, och preciserar [ADR 0018](0018-bs-medelvarde-bar-inte-anspraket.md) punkt 7 och 8

## Kontext

ADR 0018 fastställde att B:s medelvärdesform inte bär anspråket om storlek, och låste rättelsen
till en normaliserad summa med en förhandsbestämd nämnare. Punkt 7 lämnade nämnarens form öppen.
Biljett #50 skulle avgöra den.

Frågan visade sig vara fel ställd på samma sätt som #45:s var det. Nämnaren är inte en storhet
som ska väljas. Kvoten var aldrig fel i sig. Den användes över fel enheter.

## Diagnos

Mätt 2026-09-16 mot `config/`, `pipeline/`, `dist/scores.json` och exakta omkörningar mot lagret.
Punkt 9 säger vad som räknades och varför ADR 0003 punkt 1 inte fälls.

### 1. En cell blandar två olika slags poster

Ett `net` per (parti, kategori, indikator) byggs i dag av poster som är två väsensskilda saker:

- **Flera utvärderingar av samma åtgärdstyp** är upprepade mätningar av **en storhet**. Att väga
  samman dem med kvalitetsvikt är poolning. Där är kvoten riktig: en andra studie som finner en
  mindre effekt **ska** sänka skattningen av den åtgärdens effekt. Det är att lära av data.
- **Flera åtgärdstyper på samma indikator** är **skilda ingrepp**, var och ett med sin egen
  effekt. Deras bidrag ska **adderas**. En ytterligare åtgärd som bevisligen fungerar ska höja
  den väntade förbättringen.

`pipeline/effects.py` använder **en enda form för båda**. Det är konstruktfelet. ADR 0018
namngav dess ena halva.

### 2. Kvoten är det som hittills har hållit isär storlek och säkerhet

ADR 0004 beslut 2 lyder att `effect_strength` bär storleken och går in i poängen, medan
`evidence_level` och `confidence` bär säkerheten. Under kvoten **förkortas `q` bort** för en
ensam post: `net = q·m / q = m`. Kört 2026-09-16:

| post | `net` |
|---|---|
| `authority_evaluation` / medium confidence / medium styrka | 0,600 |
| `systematic_review` / high confidence / medium styrka | 0,600 |

Identiska. 112 av 151 celler bär exakt ett claim, så för tre fjärdedelar av materialet saknar
`q` verkan. Hade `Σ q` tagits ur nämnaren rakt av hade `q` multiplicerat amplituden direkt, och
ADR 0004 beslut 2 hade fallit utan att någon beslutat det. Den form som beslutas nedan undviker
det: `q` stannar som **relativ poolningsvikt** och blir aldrig amplitudfaktor.

### 3. Varje nämnare som läser liggaren bär samma fel

Låt nämnaren följa antalet åtgärdstyper på indikatorn. En ny åtgärdstyp höjer då nämnaren för
alla, medan täljaren står still för den som saknar position. Talet faller. Det är ren algebra.
Nämnaren måste därför hämtas ur den versionslåsta instrumentdesignen, aldrig ur de poster som
råkar finnas i körningen.

### 4. Monotoniciteten går inte att utlova för publicerat B

Krympningen multiplicerar **avståndet från neutral**. Stiger täckningen förstärks det tecken
cellen redan har. Ligger `B_rått` under neutral drar en höjd täckning betyget nedåt, så en
positiv post kan sänka publicerat B utan att universum ändrats. **Sex av 56 celler** ligger
under neutral i `B_rått`: MP i försvar, SD i demokrati, klimat och välfärd, V i ekonomi och
integration. I den lägsta, `B_rått` 1,858 med täckning 0,753, räcker det att en positiv post
höjer `B_rått` med mindre än 0,040 medan täckningen stiger 0,05.

Ovanför neutral gäller spegelbilden: en negativ post kan höja publicerat B.

### 5. Samma konstruktfel finns en nivå upp, och det rättas inte här

`score.aggregate_B` är ett viktat medel över de indikatorer som **har ett värde**. Indikatorer
utan claims utelämnas och nämnaren renormeras. Tillkommer indikator `j` gäller

```
B_rått' - B_rått = w_j · (s_j - B_rått) / (Σ_närvarande w + w_j)
```

Tecknet avgörs av om den nya indikatorns betyg ligger över eller under det gamla medelvärdet,
aldrig av om posten är positiv. **22 av 68 indikatorer bär liggarposter, 46 bär inga**, så en ny
post landar normalt på en tom indikator. En ensam ny post av den vanligaste sorten, `q = 0,48`
och `m = 0,6`, ger ett indikatorbetyg på högst 3,22 för varje `K ≥ 1`, och **42 av 56 celler**
ligger över 3,22.

Felet överlever alltså den här rättelsen. Punkt 11 säger var det avgörs.

### 6. Produkten `q` bär ett epistemiskt omdöme som ingen har fattat

Grinden släpper in fyra kombinationer. Tre förekommer: `authority_evaluation` + high (9 poster),
`authority_evaluation` + medium (19), `systematic_review` + medium (5). `systematic_review` +
high finns inte. Produkten ger dem 0,68, 0,48 och 0,60, och rangordnar därmed **9 myndighets-
utvärderingar med hög tilltro över 5 systematiska översikter med medelhög tilltro**. Ingen har
fattat det beslutet. Det ligger i en multiplikation.

### 7. Grindens tak är en sammanträffning

`entry_admitted` läser bara det booleska fältet `admitted`. Grindens kriterier står i prosa. Att
tabellens globala maximum också är admissibelt är sant av en sammanträffning:
`systematic_review` är både tabellens topp och grindgodkänd, och `high confidence` likaså. En
skala får inte vila på det.

### 8. Bandet är redan bredare än hela spannet

Bandets halvbredd är `1,5 × Σ vikt × (1 - säkerhet)` och läser **bara säkerhetsetiketterna**,
aldrig betyget. Vid B = medium är bredden 1,155. Hela spannet av kategoribetyg över åtta partier
och sju kategorier är 1,01. **Bandet är alltså redan 114 procent av spannet.** Dess uppgift är
inte att skilja partier åt utan att säga att talet är mjukt.

### 9. Vad som räknades, och varför ADR 0003 punkt 1 inte fälls

Räknat: instrumentets egenskaper, alltså fördelningar över liggaren, antal claims per cell,
`q`- och `m`-värden, samt exakta omkörningar med och utan **befintliga** poster. Beslutet nedan
följer ur algebran i punkt 1 till 3 och ur formens egenskaper, aldrig ur vem som steg eller föll.

**Inte räknat:** band, totalpoäng eller rangordning under någon kandidatnämnare. Inga tal under
någon kandidatkonstant. `R = 3` i punkt 4 är skrivet **före** varje sådan körning.

## Beslut

1. **Formen är poolning inom åtgärdstyp och summa över åtgärdstyper.**

   ```
   inom åtgärdstypen:   x_t = Σ_e (q_e · m_e) / Σ_e q_e
   över åtgärdstyper:   net = clip( Σ_t x_t / K , -1, 1 )
   ```

   `x_t` ligger i [-1, 1] av konstruktion, eftersom det är ett viktat medel av `m`-värden. Något
   typtak `c_t` behövs därför inte och införs inte. `q` är enbart relativ poolningsvikt och blir
   aldrig amplitudfaktor, så **ADR 0004 beslut 2 står orört**. Detta ändrar ADR 0004 beslut 3 och
   uppfyller ADR 0018 punkt 7, inklusive kravet att poster på samma åtgärdstyp delar sin
   budgetandel: de delar typens plats i summan.

2. **Monotoniciteten gäller i tre led, och inte fler.** Detta preciserar ADR 0018 punkt 8, vars
   ordalydelse inte går att uppfylla.

   - **`net` inom indikatorn:** ovillkorlig garanti. En ny åtgärdstyp med `q·m > 0` höjer alltid
     eller lämnar talet orört. En post med `q·m < 0` sänker alltid eller lämnar det orört. Efter
     klippning får talet stå still, aldrig vända.
   - **`B_rått`:** garanti endast vid **oförändrat indikatormedlemskap**, av skälet i diagnos 5.
   - **Publicerat `B`:** ingen garanti, av skälet i diagnos 4.

   En ny utvärdering **inom** en åtgärdstyp får sänka `x_t`. Det är poolning och inget
   monotonicitetsbrott.

   Krympningens beteende skrivs som **förstärkning av avvikelsen från neutral när täckningen
   ökar**, aldrig som förbättring eller försämring.

3. **Godkännandetestet delas i två.**
   - **Evidensmonotonicitet:** med indikatorer, åtgärdstyper och täckningsnämnare fixerade
     gäller punkt 2:s första led.
   - **Universumändring:** när en ny åtgärdstyp införs får B röra sig genom täckningen. Det
     prövas som ett versions- och jämförbarhetsärende, aldrig som ett monotonicitetsprov.

   Konflikten med ADR 0018 punkt 8:s ordalydelse står här som konflikt och läses inte bort.

4. **`R = 3`, låst i modellversionen.** Ordagrann lydelse:

   > Positiv respektive negativ full skala nås när tre skilda åtgärdstyper var och en bidrar med
   > maximal belagd effekt i samma riktning. Summor med större absolut magnitud klipps vid
   > skalans ändpunkt. Modellen skiljer därefter inte mellan tillräcklig och större sammanlagd
   > effekt.

   `K = R × m_max`. Talet är **normativt och inte härlett**. `min_claims_for_high_confidence`
   avvisas uttryckligen som ankare: den deklarerades för säkerhetsetiketten, och att återanvända
   den för storleksskalan gör en säkerhetsparameter till en dold breddparameter. Ett nytt `R` är
   en ny modellversion. Klippningen redovisas som **informationsförlust**: modellen avstår från
   att skilja på allt ovanför budgeten.

5. **Nämnaren hämtas ur instrumentdesignen, aldrig ur körningen.** Den inre poolningsnämnaren
   `Σ q` är undantagen: den normerar bara relativa vikter inom en skattning, tilldelar ingen
   budget, och gör inte en typs bidrag större för att den bär fler utvärderingar.

6. **Åtgärdstyperna är ett versionerat, slutet register** med stabilt id, operativ avgränsning
   och versionshistorik. Enbart etiketter räcker inte, eftersom en typs innehåll annars kan
   ändras utan formell delning. **Att dela eller slå ihop en typ är en skaländring** och går genom
   samma versionsmaskineri som en ändring av `R`. En genuint ny typ är en universumändring enligt
   punkt 3. En post eller position på en typ utanför registret faller hårt.

7. **Additiviteten är ett skrivet modellantagande.** Typbidrag är **additivt summerbara utan
   interaktions- eller överlappskorrigering**. Det är inte ett antagande om statistiskt oberoende.
   Ingen överlappsregel byggs, eftersom den kräver ett omdöme per par. Klippningen begränsar bara
   utslagets numeriska storlek: den motverkar inte dubbelräkning under mättnadspunkten, kan föra
   en cell till ±1 på felaktiga grunder, och döljer hur stort det oklippta överskottet var.
   **Den oklippta summan redovisas därför diagnostiskt.** Visar sig två typer vara samma ingrepp
   slås de ihop, vilket är en skaländring enligt punkt 6.

8. **Poolningsregeln.** `Σ q = 0` ger **hård fail**, aldrig en tyst nolla, även om tillståndet är
   onåbart under dagens grind. Utvärderingar inom en typ som är **oense om tecknet** bär en
   **rent deskriptiv flagga** utan automatisk verkan. En automatisk nedgradering av
   säkerhetsetiketten avvisas som ospecificerad: den lämnar öppet hur svag en motröst får vara,
   hur `m = 0` behandlas, om `+0,01` mot `−0,01` är samma konflikt som `+1` mot `−1`, och på
   vilken nivå sänkningen sker. En viktad heterogenitetsregel får förhandsregistreras senare.

9. **Grinden blir maskinläst.** Den mekaniserbara halvan kodas i configen som en lista över
   tillåtna `evidence_level` och en lägsta `confidence`. **Skalans faktorer räknas som maxima över
   den admissibla domänen**, aldrig över hela tabellerna, så sambandet blir konstruktivt i stället
   för en testad sammanträffning. Configen vägrar laddas om den admissibla mängden är tom eller
   inkonsistent. Det booleska fältet står kvar för omdömeshalvan, alltså att evidensen avser exakt
   indikatorn, och det måste bära **granskningsbar proveniens**. En grindändring är en
   **modell- och skaländring**, inte datavalidering. Mätt: alla 33 admitterade poster klarar redan
   kriterierna, så kodningen ändrar ingenting i dagens material.

10. **Analysenheten är estimandet, bundet till exakt en åtgärdstyp.** Två identifierare krävs:
    `evaluation_id` för studien och `estimand_id` för det kodade resultatet.

    - Ett estimand bidrar **en gång**, på sin enda åtgärdstyp. Att dela ett estimand över två
      typer för att dubbla dess vikt är därmed stängt.
    - En utvärdering får bära **flera** estimand när de avser skilda åtgärdstyper. Att tvinga en
      utvärdering till ett bidrag per indikator vore fel: det gör utfallet beroende av hur
      studiernas programomfång råkar vara paketerat.
    - Dedupliceringsnoden är `evaluation_id × indikator × åtgärdstyp`. Flera estimand i samma nod
      förs först samman och lämnar sedan **ett** bidrag.
    - Samma utvärdering får räknas på **flera indikatorer**. Det levande fallet, RiR 2012:1 på två
      klimatindikatorer via `koldioxidskatt`, är tillåtet.
    - Ett estimand som avser ett **odelbart paket** av flera åtgärdstyper får inte fördelas
      godtyckligt. Det kräver en fördefinierad kombinationstyp, annars kan det inte ingå alls.

    Hård fail gäller vid samma `evaluation_id` och `estimand_id` med olika `m`, och vid saknat
    `estimand_id` när flera resultat finns. Inom-utvärderingssammanvägning är **aldrig automatiskt
    ett medel**: först utvärderingens eget syntetiska huvudmått, annars ett estimand valt före
    modellberäkningen med skäl i liggaren, annars en deklarerad konservativ sammanvägning, och i
    varje fall redovisad känslighet. Ett författardefinierat huvudmått får bara användas om dess
    riktning och innehåll motsvarar indikatorn.

    Mätt: noll kollisioner inom en indikator i dag, så reglerna ändrar ingenting i nuvarande
    material.

11. **Säkerhetsmodellen avgörs i en egen biljett, och den här ADR:n löser den inte.** Skälet är
    att `evidence_level` aldrig når bandet, vilket är ett **befintligt** fel mot ADR 0004 beslut 2
    som den här rättelsen varken skapar eller förvärrar. Under formen i punkt 1 gör `q` verkligt
    arbete i poolningen, så argumentet att kvaliteten måste flytta till bandet faller.

    Upprullningsfelet i diagnos 5 hör till samma biljett, eftersom varje rättelse av det rör
    krympningen, som ADR 0018 frös.

    **Denna ADR får inte beskrivas som en lösning på evidensmonotonicitet end to end.** Talet
    42 av 56 i diagnos 5 är ett mätresultat för en bestämd dataversion, posttyp och konstant, och
    får aldrig läsas som en generell egenskap.

12. **Bandet märks preliminärt, maskinläst.** Formen i punkt 1 ändrar vad `net` är, medan bandets
    bredd bara läser säkerhetsetiketterna. Ett gammalt band runt ett nytt tal är därför
    **okalibrerat**. Felet lutar åt det försiktiga hållet: betygen komprimeras mot neutral medan
    bredden står still, så bandet överdriver osäkerheten snarare än tvärtom.

    Bandet döljs därför **inte**. Att ta bort ett band som överdriver osäkerheten gör sidan mer
    tvärsäker, inte ärligare, och det motsäger diagnos 8. I stället:

    - `scores.json` bär ett maskinläst fält som säger att säkerhetsmodellen är preliminär.
    - Den mening i metodpanelen som **definierar** bandet skrivs om. En fotnot räcker inte när
      definitionen säger något annat.

13. **Spårbarheten delas.** Den här biljetten bär hela vägen från claims till `q`, till
    typpoolen, till typbidraget, till `net`, plus vilka säkerhetsindata som lämnats vidare. Tre
    maskinella invariansprov låses: duplicering av samma estimand ändrar ingenting, uppdelning av
    samma estimand i flera redaktionella poster ändrar ingenting, och byte av dokumentrepresentation
    för samma utvärdering ändrar ingenting. Spårbarheten från säkerhetsindata till band, grindar,
    varningar och etikett hör till biljetten i punkt 11.

## Vad som måste deklareras innan bygget räknar ett tal

ADR 0003 punkt 1 kräver att regeln är låst och nedskriven först. Följande står ännu öppet och
avgörs i byggspecen, inte här:

1. Vad som räknas som **skilda åtgärdstyper**, alltså registrets avgränsningsregel enligt punkt 6.
2. Om `q` i poolningen ska följa en deklarerad klassordning i stället för produkten, givet
   diagnos 6. Produkten och en kombinationstabell kan annars rangordna samma två kombinationer
   olika inom samma modell.
3. Hur en **saknad kvalitetsklass** behandlas, eftersom den avgör om och hur `q` får användas.
4. Om kvaliteten får **skilja mellan positivt och negativt bidrag**, eftersom det kan ändra `net`.
5. Känslighetsanalysens körbara plan: `R` över 2 till 5 som grid eller svep, vilka fullständiga
   ordningar som körs, en faktor i taget **och** full korsprodukt, vilket alternativestimand som
   används per post, och vad som redovisas. Konstantens verkan redovisas som **nivå- och
   klippningsdiagnostik**, aldrig som rangordningsstabilitet, eftersom ADR 0003:s mått strukturellt
   saknar känslighet för en gemensam positiv skalning före klippning.

## Vad beslutet inte rör

- **Täckningskrympningen.** Formen `2,5 + (rått - 2,5) × täckning` står orörd (ADR 0018).
- **Den symmetriska evidensgrinden.** ADR 0006 står, och de uteslutna posterna står kvar uteslutna.
- **`effect_strength`-tabellen 0,3 / 0,6 / 1,0.** ADR 0004 beslut 4 står.
- **B:s vikt.** Kategoribetyget är oförändrat 0,30 A + 0,50 B + 0,20 D.
- **ADR 0004 beslut 2.** Storlek och säkerhet hålls isär, och punkt 1 är vald just för att bevara
  det.
- **Band, totalpoäng och rangordning.** Inte räknade, och inte del av något skäl ovan.

## Kända invändningar som inte åtgärdas här

1. **Upprullningen är samma konstruktfel en nivå upp** (diagnos 5). Hör till biljetten i punkt 11.
2. **`evidence_level` når aldrig bandet**, vilket är ett befintligt fel mot ADR 0004 beslut 2.
   Samma biljett.
3. **Viktförhållandet 5:3 kan vara upphävt i praktiken.** Nominella vikter styr inflytandet bara
   om delskalorna är jämförbart kalibrerade. Komprimeras B men inte A har utbytesrelationen
   ändrats trots att koefficienterna står kvar. Rätt ordning är skalor först, vikter därefter, och
   uppfyller 5:3 inte sitt uttalade syfte på den färdiga skalan måste ADR 0002 öppnas. Det är
   intern konsistenskontroll och ingen utfallstrimning.
4. **Versionsjämförbarheten.** Med fast nämnare blir varje ändring av register, `q`-tabell, grind
   eller delningsregel en skaländring. Det finns ingen publicerad tidsserie att bryta, så kostnaden
   landar i versionshistorien. Baslinjen skrivs om, men först efter en arkiverad engångsdiff
   gammal mot ny som migrationsbevis, märkt icke-longitudinell.
5. **Mättnadens marginaleffektsasymmetri.** Tillskott ovanför klippet är osynliga, och
   borttagningar är osynliga tills summan åter passerar `K`. Det är informationsförlust, inte
   historikberoende: allt räknas om från liggaren vid varje körning.

## Följder

- Biljett [#50](https://github.com/mcknschn/rosta/issues/50) byter namn och räckvidd till formen.
  Uttryckligt icke-mål: säkerhetsbandets semantik och kalibrering.
- Säkerhetsmodellen läggs som en egen biljett under ADR 0009.
- Underlaget är en grillning i tretton rundor, prövad mot en extern granskare. Grillningen fällde
  bland annat: att nämnaren kunde vara en kapacitet med krediteringstak, att den starkaste posten
  per typ kunde krediteras, att avtagande marginalkreditering var förenlig med monotonicitet och
  kommutativitet, att `min_claims_for_high_confidence` kunde förankra skalan, och att villkoret om
  flera poster per åtgärdstyp saknade medlemmar och därför inte behövde byggas.
