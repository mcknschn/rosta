# Förhandsregistrering av Verklighetsbildpiloten

- Version: 1
- Status: **låst**
- Låst: 2026-09-13, före urvalsdragningen och före den första kodade utsagan
- Beslutad av: [ADR 0016](../adr/0016-verklighetsbild-avgors-av-en-pilot.md) beslutspunkt 5, 6 och 7
- Byggs i: biljett [#46](https://github.com/mcknschn/rosta/issues/46), steg 2
- Kodbok: [`kodbok_pilot.md`](kodbok_pilot.md) version 1, låst i commit `36c3907`

Talen i denna fil står skrivna innan något kodades. De ändras aldrig efteråt. Ändras de ändå,
faller piloten och måste dras om.

## 1. Utbyteströsklarna

Ordagrant ur ADR 0016 beslutspunkt 7.

1. **Designviktat totalt utbyte minst 20 procent av de 200 kodade utsagorna.**
2. **Minst 5 prövbara relationer för vart och ett av de åtta partierna.**
3. Ger ett parti 0 till 2 relationer faller per-parti-redovisningen.
4. Ger ett parti 3 eller 4 relationer totalundersöks det partiets material innan beslut. Kravet på
   minst 5 står kvar efter utökningen.
5. Punktskattningar, partiresultat och osäkerhetsintervall redovisas oavsett utfall.

Talet 20 procent är en miniminivå för användbarhet och inte ett statistiskt belagt
populationsvärde. Kravet på minst 5 relationer hos **samtliga** åtta partier gör den samlade
regeln strängare än totalgränsen ensam.

Kategorispridningen redovisas men är **aldrig** en stoppregel (ADR 0016 beslutspunkt 8).

## 2. Vad utbytet är för tal

**Utbytet är antalet prövbara relationer per kodad utsaga**, skattat till hela bakåtmaterialet om
896 utsagor.

Urvalet är stratifierat på parti med `n_h = 25` ur stratum `h`. Populationen per stratum, `N_h`,
är känd. Skattningen är därför ett designviktat medelvärde och ingen kvotskattning:

```
Y = summa_h (N_h / n_h) * summa_i y_hi        skattat totalt antal relationer
X = summa_h N_h = 896                          känd populationsstorlek
R = Y / X                                      utbytet
```

`y_hi` är antalet prövbara relationer utsaga `i` i stratum `h` gav.

Varianten med ändlighetskorrektion:

```
Var(R) = (1 / X^2) * summa_h N_h^2 * (1 - n_h / N_h) * s_h^2 / n_h
```

`s_h^2` är stickprovsvariansen för `y_hi` inom stratum `h`. Faktorn `(1 - n_h / N_h)` är
ändlighetskorrektionen. Den biter hårdast på MP, där `25 / 37 = 0,676`, och på KD, där
`25 / 55 = 0,455`.

Osäkerhetsintervallet är `R +/- 1,96 * roten ur Var(R)`. **Begränsningen skrivs ut:** intervallet
är en normalapproximation på 25 observationer per stratum, och `y_hi` är ett litet heltal med
tung vänsterpunkt i noll. Intervallet är därför indikativt och inte exakt.

Per parti redovisas dessutom andelen utsagor som gav minst en relation, med samma
ändlighetskorrektion.

## 3. Vilken kodares tal tröskeln prövas mot

Två modeller kodar var för sig och deras svar jämkas aldrig samman (avsnitt 5). Utbytet finns
alltså i flera versioner. **Tröskeln i avsnitt 1 prövas mot snittet.**

En relation räknas som **delad** när båda kodarna gett samma `utsaga_id` samma `indikator`. Period
och operationalisering är fritext och ingår inte i nyckeln.

| Tal | Definition | Roll |
|---|---|---|
| Snittet | Delade relationer plus halva antalet enkelsidiga | **Avgör tröskeln** |
| Kodare A | Alla relationer kodare A fann | Redovisas |
| Kodare B | Alla relationer kodare B fann | Redovisas |
| Delade | Relationer båda fann | Redovisas, undre gräns |
| Unionen | Relationer minst en fann | Redovisas, övre gräns |

Skälet till att snittet avgör: de delade relationerna ensamma straffar materialet för kodbokens
brister, och unionen ensam belönar den kodare som gissar oftast. Snittet ligger mellan och rör sig
inte med antalet kodare.

Trösklarna 2, 3 och 4 i avsnitt 1 räknas på samma sätt, alltså på snittet per parti.

## 4. Reliabilitetströskeln

ADR 0016 beslutspunkt 5 kräver att tröskel och förfarande vid oenighet bestäms före kodningen.

Krippendorffs alfa räknas för de fyra momenten i kodbokens avsnitt 9. Skalorna är ordinal för
avgränsning och nominal för de tre andra.

| Alfa | Läsning |
|---|---|
| `>= 0,800` | Momentet håller |
| `0,667` till `0,800` | Momentet håller bara för tentativa slutsatser |
| `< 0,667` | Momentet håller inte |

Gränserna är Krippendorffs egna konventionella nivåer och inte projektets uppfinning.

### 4.1 Vilket moment som fäller piloten

**Bara prövbarheten fäller.** Faller alfa för prövbarhet under 0,667 saknar utbytestalet mening,
eftersom utbytet just är antalet led två kodare är överens om att kunna pröva. Piloten faller då
oavsett hur många relationer som räknades.

Avgränsning, indikatorval och kodvärde **redovisas och binder produktionskodboken**, men fäller
inte piloten ensamma. Skälet är att låg överensstämmelse där är ett fel i kodbokens regler och
inte ett besked om hur mycket materialet bär. Klaras utbyteströskeln men inte ett av de tre, är
beskedet att instrumentet kan byggas först sedan just den regeln skärpts.

### 4.2 Förfarandet vid oenighet

**Ingen sammanjämkning.** De två kodningarna står som de är. Ingen tredje part avgör tvister, och
ingen kodare får ändra sitt svar efter att ha sett den andras.

Skälet är att sammanjämkning förstör själva mätningen. Ett sammanjämkat protokoll har per
konstruktion alfa 1,0 och säger ingenting om hur väl kodboken styr en kodare som läser den ensam.

## 5. Kodarna

| Roll | Kodare | Leverantör | Uppgift |
|---|---|---|---|
| A | Claude Opus 5 | Anthropic | Alla 200 utsagor |
| B | Codex, GPT-5-serien | OpenAI | Alla 200 utsagor |
| A-prim | Claude Opus 5, färsk kontext | Anthropic | Delurvalet om 40 |
| B-prim | Codex, GPT-5-serien, ny körning | OpenAI | Delurvalet om 40 |

Ingen kodare ser någon annan kodares svar. Den låsta kodboken är enda gemensamma indata.

### 5.1 Avvikelse från ADR 0016 beslutspunkt 5

ADR:n skrev att delurvalet skulle kodas **av projektägaren**, alltså av en människa, och redovisas
som ett parvist överensstämmelsemått mot vardera modellen.

**Projektägaren avstod 2026-09-13** och lät i stället en färsk modellkontext och en andra
Codexkörning göra det. Avvikelsen är beslutad av projektägaren och skriven här samma dag, före
kodningen.

Följden är att **piloten inte innehåller någon mänsklig kodare alls**. Vad delurvalet mäter ändras
därmed:

- A mot A-prim och B mot B-prim mäter **stabilitet inom samma leverantör**, alltså om samma modell
  med samma kodbok kommer fram till samma sak två gånger.
- A-prim mot B-prim är ett **andra par över leverantörsgränsen** på ett mindre urval.
- Ingenting i piloten mäter längre människa mot modell.

### 5.2 Begränsningen

Skrivs i metodrutan, ordagrant:

> Instrumentet gör inget anspråk på mänsklig interkodarreliabilitet. Piloten saknar mänsklig
> kodare helt. Systematiska fel som två modeller delar går inte att upptäcka med denna
> uppställning, och ett fel som alla fyra kodningarna delar syns inte alls.

Delurvalet är **inte** ett facit. Det validerar ingenting och beskrivs aldrig som riktighet
(ADR 0016 godkännandetest 8).

## 6. Delurvalet

- **Storlek: 40 av 200.** Fem per parti.
- **Dragning:** slumpmässigt utan återläggning ur de 200, stratifierat på parti, eget frö.
- **Blindning:** A-prim och B-prim får utsagorna i ny slumpordning, utan partikod och utan
  kodningarna från A och B.

Storleken är satt till en femtedel. Ett mindre urval ger ett intervall som är för brett för att
säga något, och ett större kostar körtid utan att flytta beskedet. Fem per parti är det minsta tal
som gör ett partivist mönster synligt utan att bli ett partivist påstående.

## 7. Vad som händer när trösklarna faller

Klaras inte utbyteströsklarna i avsnitt 1, eller faller alfa för prövbarhet under 0,667, skrivs ett
**daterat avslagsskäl** i `docs/verklighetsbild_pilot/`, och ingen kodning fortsätter
(ADR 0016 beslutspunkt 11). Materialet ligger kvar.

Det är en godkänd utgång. Den viktade stansen prövades och förkastades på samma sätt 2026-06-07.

## 8. Vad piloten aldrig publicerar

- **Ingen sanningsandel.** Piloten kodar ingen sanning alls (kodbokens avsnitt 1).
- **Ingen andel per parti som handlar om riktighet.** Andelen utsagor som gav en relation är ett
  mått på materialets prövbarhet, aldrig på partiets vederhäftighet, och texten säger det.
- **Ingen kategorispridning som omdöme.** Talet skrivs ut utan tröskel (ADR 0016 beslutspunkt 8).
