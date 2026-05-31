Idén är att göra modellen personlig utan att själva sakgranskningen blir helt subjektiv.

Rösta ska inte fråga användaren vilken ideologisk metod han eller hon föredrar. Användaren anger vilka samhällsområden som är viktigast. Partierna bedöms därefter mot objektiva kategoriindikatorer och evidens för om deras förslag, agerande och ansvar faktiskt pekar mot förbättring i dessa indikatorer.

Exempel: inom ekonomi är det positiva utfallet högre sysselsättning, högre produktivitet, bättre reallöneutveckling, inflation nära målet och hållbara offentliga finanser. Om detta uppnås genom mer höger- eller vänsterorienterad politik är inte poängen i sig. Det centrala är om utfallet är objektivt positivt och om det finns stöd för att partiets politik rimligen leder dit.

# Sammanfattande modell

## Steg 1: Välj huvudkategorier

Jag skulle använda sju kategorier:

| Nr | Kategori | Beskrivning |
|----|----------|-------------|
| 1 | Ekonomi och jobb | Tillväxt, inflation, arbetslöshet, reallöner, statsfinanser |
| 2 | Välfärd | Vård, skola, omsorg, kommuner, regioner |
| 3 | Lag och trygghet | Brott, rättsväsende, trygghet, återfall, utsatthet |
| 4 | Försvar och beredskap | Militärt försvar, Nato, Ukraina, civilförsvar, krisberedskap |
| 5 | Klimat, miljö och energi | Utsläpp, energi, elpriser, biologisk mångfald, omställning |
| 6 | Integration och social sammanhållning | Arbete, språk, skolsegregation, självförsörjning, tillit |
| 7 | Frihet, demokrati och institutioner | Rättsstat, medier, personlig frihet, korruption, myndighetstillit |

Man kan använda fem kategorier om man vill göra det enklare. Då skulle jag slå ihop kategori 6 och 7, och eventuellt lägga klimat/energi som en underkategori.

## Steg 2: Välj dina vikter

Standardförslag:

| Kategori | Standardvikt |
|----------|--------------|
| Ekonomi och jobb | 20 % |
| Välfärd | 20 % |
| Lag och trygghet | 15 % |
| Försvar och beredskap | 15 % |
| Klimat, miljö och energi | 12,5 % |
| Integration och social sammanhållning | 10 % |
| Frihet, demokrati och institutioner | 7,5 % |
| **Totalt** | **100 %** |

Men detta ska väljaren själv kunna ändra.

En väljare som prioriterar ekonomi, trygghet och försvar kan exempelvis vikta:

| Kategori | Vikt |
|----------|------|
| Ekonomi och jobb | 25 % |
| Lag och trygghet | 20 % |
| Försvar och beredskap | 20 % |
| Integration | 15 % |
| Välfärd | 10 % |
| Klimat/energi | 5 % |
| Demokrati/frihet | 5 % |

En väljare som prioriterar välfärd, klimat och sammanhållning kan exempelvis vikta:

| Kategori | Vikt |
|----------|------|
| Välfärd | 25 % |
| Klimat/energi | 20 % |
| Ekonomi och jobb | 15 % |
| Integration/sammanhållning | 15 % |
| Frihet/demokrati | 10 % |
| Lag och trygghet | 8 % |
| Försvar | 7 % |

Poängen är inte att låtsas vara neutral om vilka samhällsområden som är viktigast. Poängen är att göra prioriteringarna synliga, samtidigt som varje kategori bedöms mot samma objektiva mätpunkter för alla partier.

## Steg 3: Scorea varje parti per kategori

Varje parti får 0–5 poäng i varje kategori.

### Bedömningskedja

Varje kategoribetyg ska bygga på en tydlig kedja:

```
Kategoriutfall
  → partiets agerande
  → evidens/träffsäkerhet
  → ansvar/attribution
  → resultat
```

| Led | Fråga |
|-----|-------|
| Kategoriutfall | Vilka objektiva indikatorer visar om kategorin förbättras eller försämras? |
| Partiets agerande | Vad har partiet faktiskt röstat för, budgeterat, föreslagit och genomfört? |
| Evidens/träffsäkerhet | Finns det evidens för att partiets förslag har den effekt partiet påstår, mätt mot kategoriindikatorerna? |
| Ansvar/attribution | Har partiet haft faktisk makt och administrativ möjlighet att påverka utfallet? |
| Resultat | Har indikatorerna förbättrats där partiet haft ansvar, med rimlig tidsförskjutning och osäkerhet? |

Samma reform kan ha positiva effekter på vissa indikatorer och negativa effekter på andra. Den ska därför inte bedömas ideologiskt som "bra" eller "dålig" i sig, utan brytas ned i förväntade indikatorpåverkningar.

### Grundformel

```
Kategoripoäng =
  40 % faktiskt agerande
  35 % evidens/träffsäkerhet
  15 % genomförbarhet/ansvar
  10 % uppmätta resultat
```

### Delpoäng

| Del | Vikt | Fråga | Exempel på källor |
|-----|------|-------|-------------------|
| A. Faktiskt agerande | 40 % | Vad har partiet röstat för, budgeterat, föreslagit och genomfört? | Riksdagsvoteringar, budgetmotioner, propositioner |
| B. Evidens/träffsäkerhet | 35 % | Finns det stöd för att förslagen påverkar kategoriindikatorerna i den positiva riktning partiet påstår? | Myndigheter, forskningsöversikter, utvärderingar |
| C. Genomförbarhet/ansvar | 15 % | Har partiet makt, realistisk finansiering och administrativ möjlighet att genomföra eller påverka förslagen? | Regeringsställning, region/kommunstyren, finansiering |
| D. Resultat | 10 % | Har relevanta indikatorer förbättrats där partiet haft ansvar? | SCB, Brå, Socialstyrelsen, Skolverket, Kolada, Försvarsmakten |

### Claims som mellanlager

För att modellen ska kunna granskas ska poängen inte räknas direkt från rådata till slutbetyg. Mellan rådata och betyg behövs verifierbara claims:

```json
{
  "claim": "Parti X röstade ja till reform Y",
  "category": "ekonomi",
  "indicator": "sysselsattning",
  "expected_direction": "up",
  "effect_confidence": "medium",
  "source": "..."
}
```

Claims ska kunna avse exempelvis:

- faktiskt agerande: partiet röstade ja/nej, föreslog en budgetförändring eller lade en motion.
- påstådd effekt: partiet säger att förslaget ska påverka en viss indikator.
- evidensbedömning: svenska myndigheter eller akademiska källor stödjer, motsäger eller nyanserar den påstådda effekten.
- ansvar: partiet hade eller hade inte möjlighet att påverka utfallet.
- resultat: indikatorn förbättrades eller försämrades under relevant period.

På så sätt kan en användare se vilka påståenden som ligger bakom varje poäng, inte bara slutresultatet.

## Kategorier och mätpunkter

### 1. Ekonomi och jobb

| Undermått | Vikt inom kategorin |
|-----------|---------------------|
| Sysselsättning och arbetslöshet | 25 % |
| BNP per capita och produktivitet | 20 % |
| Reallöner och hushållens ekonomi | 20 % |
| Inflation och prisstabilitet | 15 % |
| Offentliga finanser och långsiktig hållbarhet | 20 % |

**Positiv riktning:**

| Mått | Positivt |
|------|----------|
| Sysselsättning | Upp |
| Arbetslöshet | Ned |
| BNP per capita | Upp |
| Produktivitet | Upp |
| Reallöner | Upp |
| Inflation | Nära målet, inte bara lägst |
| Statsskuld/underskott | Hållbar nivå |

> **Viktig caveat:** Ett parti ska inte få hela äran eller skulden för konjunkturen.

### 2. Välfärd

| Undermått | Vikt inom kategorin |
|-----------|---------------------|
| Vårdens tillgänglighet och kvalitet | 30 % |
| Skolans kunskap och likvärdighet | 30 % |
| Omsorg och personalförsörjning | 20 % |
| Finansiering, styrning och anti-fusk | 20 % |

**Positiv riktning:**

| Mått | Positivt |
|------|----------|
| Vårdköer | Ned |
| Andel som får vård i tid | Upp |
| Överlevnad efter svår sjukdom | Upp |
| Skolresultat | Upp |
| Skillnader mellan skolor | Ned |
| Behöriga lärare | Upp |
| Personalomsättning i omsorg | Ned |
| Välfärdsbrottslighet | Ned |

> **Viktig caveat:** Mer pengar är inte automatiskt bättre, men underfinansiering kan vara direkt skadligt.

### 3. Lag och trygghet

| Undermått | Vikt inom kategorin |
|-----------|---------------------|
| Grov brottslighet och våldsbrott | 30 % |
| Utsatthet och upplevd trygghet | 20 % |
| Rättsväsendets effektivitet | 20 % |
| Förebyggande arbete | 15 % |
| Återfall och kriminalvård | 15 % |

**Positiv riktning:**

| Mått | Positivt |
|------|----------|
| Dödligt våld | Ned |
| Skjutningar/sprängningar | Ned |
| Brottsutsatthet | Ned |
| Upplevd otrygghet | Ned |
| Uppklaringsgrad | Upp |
| Handläggningstid | Ned |
| Återfall i brott | Ned |

> **Viktig caveat:** Anmälda brott är inte alltid samma sak som faktisk brottslighet.

### 4. Försvar och beredskap

| Undermått | Vikt inom kategorin |
|-----------|---------------------|
| Militär förmåga | 35 % |
| Ekonomisk ambitionsnivå och långsiktig finansiering | 25 % |
| Civil beredskap | 20 % |
| Nato, Ukraina och internationell trovärdighet | 15 % |
| Genomförbarhet och leveranstakt | 5 % |

**Positiv riktning:**

| Mått | Positivt |
|------|----------|
| Försvarsanslag som andel av BNP | Upp till beslutad målnivå |
| Personal och värnpliktiga | Upp, om utbildningskapacitet finns |
| Ammunition, luftvärn, logistik, cyberförmåga | Upp |
| Civil beredskap inom vård, energi, mat, transporter | Upp |
| Ukraina-stöd | Upp, givet svensk uthållighet |
| Leveranstid för materiel | Ned |
| Nato-interoperabilitet | Upp |

> **Viktig caveat:** Försvar ska inte mätas bara i pengar. Det centrala är faktisk operativ förmåga.

### 5. Klimat, miljö och energi

| Undermått | Vikt inom kategorin |
|-----------|---------------------|
| Utsläppsminskningar | 30 % |
| Energiförsörjning och elpriser | 25 % |
| Omställningens kostnadseffektivitet | 15 % |
| Biologisk mångfald och natur | 15 % |
| Industriell konkurrenskraft i omställningen | 15 % |

**Positiv riktning:**

| Mått | Positivt |
|------|----------|
| Territoriella utsläpp | Ned |
| Konsumtionsbaserade utsläpp | Ned |
| Fossil energianvändning | Ned |
| Elprisvolatilitet | Ned |
| Effektbrist | Ned |
| Utsläppsminskning per krona | Upp |
| Hotade arter/naturförlust | Ned |

> **Viktig caveat:** Klimatpolitik bör vägas mot försörjningstrygghet, kostnad och industriell konkurrenskraft.

### 6. Integration och social sammanhållning

| Undermått | Vikt inom kategorin |
|-----------|---------------------|
| Arbete och självförsörjning | 30 % |
| Skola, språk och utbildning | 25 % |
| Boendesegregation och trygghet | 20 % |
| Normer, tillit och samhällsgemenskap | 15 % |
| Migrationssystemets hållbarhet | 10 % |

**Positiv riktning:**

| Mått | Positivt |
|------|----------|
| Sysselsättningsgap mellan inrikes/utrikes födda | Ned |
| Självförsörjningsgrad | Upp |
| SFI-resultat/språkkunskaper | Upp |
| Skolresultat i utsatta områden | Upp |
| Trångboddhet | Ned |
| Segregation | Ned |
| Bidragsberoende | Ned |
| Tillit och valdeltagande | Upp |

> **Viktig caveat:** Här finns stor risk för ideologisk bias. Därför måste indikatorerna vara extra tydliga.

### 7. Frihet, demokrati och institutioner

| Undermått | Vikt inom kategorin |
|-----------|---------------------|
| Rättsstat och maktdelning | 25 % |
| Korruption och myndighetstillit | 20 % |
| Yttrandefrihet och medier | 20 % |
| Personlig frihet och integritet | 20 % |
| Transparens och ansvarsutkrävande | 15 % |

**Positiv riktning:**

| Mått | Positivt |
|------|----------|
| Korruption | Ned |
| Förtroende för domstolar/myndigheter | Upp |
| Mediefrihet | Upp |
| Politisk transparens | Upp |
| Otillbörlig politisering av myndigheter | Ned |
| Övervakning utan rättssäkerhet | Ned |

> **Viktig caveat:** Detta är en av de svåraste kategorierna, men också en av de viktigaste. Ett parti kan ha bra sakpolitik men ändå vara riskabelt om det försvagar institutioner.

## Slutberäkning

För varje parti:

```
Totalpoäng =
  Ekonomi × din vikt
  Välfärd × din vikt
  Trygghet × din vikt
  Försvar × din vikt
  Klimat/energi × din vikt
  Integration × din vikt
  Demokrati/frihet × din vikt
```

Exempel:

| Kategori | Din vikt | Parti A poäng | Viktat bidrag |
|----------|----------|---------------|---------------|
| Ekonomi | 20 % | 4,0 | 0,80 |
| Välfärd | 20 % | 3,5 | 0,70 |
| Trygghet | 15 % | 4,2 | 0,63 |
| Försvar | 15 % | 4,5 | 0,68 |
| Klimat/energi | 12,5 % | 2,8 | 0,35 |
| Integration | 10 % | 4,0 | 0,40 |
| Demokrati/frihet | 7,5 % | 3,7 | 0,28 |
| **Total** | **100 %** | | **3,84 / 5** |

### Partipoäng bör visas med osäkerhet

Jag skulle inte bara visa:

> Parti A: 3,84

Utan hellre:

> Parti A: 3,84 / 5, osäkerhetsintervall 3,5–4,1

Det är viktigt eftersom vissa bedömningar är mer säkra än andra.

Exempel på hög säkerhet:

- Partiet röstade ja/nej i riksdagen.
- Partiet föreslog X miljarder i budget.
- Arbetslösheten var X procent.
- Vårdkön var X dagar.

Exempel på lägre säkerhet:

- Förslaget kommer sannolikt minska kriminalitet.
- Politiken kommer sannolikt höja produktiviteten.
- Reformen är mer kostnadseffektiv än alternativet.

## Slutlig modell i kompakt form

### Rösta-modellen

| Komponent | Funktion |
|-----------|----------|
| Väljaren anger vikter | Vad är viktigast för mig? |
| Kategorier har objektiva indikatorer | Vad räknas som förbättring i varje område? |
| Partier scoreas per kategori | Vad gör partierna faktiskt, och pekar det mot bättre indikatorutfall? |
| Källor hämtas | Riksdag, myndigheter, statistik, utvärderingar |
| Claims byggs | Verifierbara påståenden kopplar agerande, evidens, ansvar och resultat till indikatorer |
| Agerande mäts | Röster, budgetar, förslag, regeringsbeslut |
| Evidens mäts | Stöd för förslagens förväntade effekt på indikatorerna |
| Ansvar mäts | Har partiet haft makt att påverka? |
| Resultat mäts försiktigt | Har indikatorer förbättrats där partiet styrt? |
| Osäkerhet redovisas | Poäng visas med caveats och intervall |

### Rekommenderad huvudformel

```
Partiets poäng i kategori =
  0,40 × faktiskt agerande
  0,35 × evidens/träffsäkerhet
  0,15 × genomförbarhet/ansvar
  0,10 × resultat
```

### Rekommenderad totalformel

```
Partiets totalpoäng = summan av alla kategoripoäng × väljarens kategorivikter
```
