# ADR 0001: A mäter prioritering, inte agerande

- Status: accepted
- Datum: 2026-08-17
- Beslutad i: biljett [#7](https://github.com/mcknschn/rosta/issues/7) under karta [#6](https://github.com/mcknschn/rosta/issues/6)

## Kontext

`IDEA.md` definierade A som "vad partiet röstat för, budgeterat, föreslagit och genomfört".
Byggd A är något smalare: `a1` budgetprioritering (vikt 0,6) plus `a2` motionsprioritering
(vikt 0,4). Båda är riktningsneutrala andelar, rang-normaliserade över de åtta partierna
(`pipeline/scorerun.py`, `config/scoring.yaml`). Voteringarna ligger i stället i B, som en av
källorna bakom de 269 partiståndpunkterna i `config/party_positions.yaml`.

Dokumentet och koden sade alltså olika saker om vad A är. Frågan måste avgöras före viktfrågan,
eftersom en vikt satt före det här beslutet är satt om något annat.

## Beslut

1. **A heter Prioritering.** Frågan är: hur stor andel av partiets föreslagna anslag och egna
   motioner går till kategorin? A mäter omfattning, aldrig riktning och aldrig kvalitet.
2. **Voteringarna stannar i B.** En votering visar vilket håll ett parti drar åt. Riktning plus
   evidens är precis vad B mäter.
3. **Gränsen mellan delpoängen går vid frågan, inte vid källan.** A frågar hur mycket, B åt vilket
   håll, C om makten fanns, D hur det gick. Samma dokument får svara på flera av frågorna. Samma
   fråga får aldrig räknas två gånger. Överlappet finns redan: en budgetmotion ger `a1` sina ramar
   per utgiftsområde och ger B en ståndpunkt på ett instrument.
4. **"Genomfört" hör till C och D.** Genomförande är makt plus utfall, inte prioritering.

## Övervägda alternativ

- **A som brett agerande, med röster räknade som volym.** Förkastat. Ett uttömmande
  voteringsregister finns inte byggt: tabellen `actions` i `data/warehouse.duckdb` håller 190 rader
  ur ett prov, alla i kategorin ekonomi, och läses inte av `pipeline/scorerun.py`. Ett röstantal
  skulle dessutom mäta riksdagens dagordning lika mycket som partiets prioritering.
- **A med riktning, alltså om partiet röstat rätt.** Förkastat. Det gör A till en dubblett av B och
  räknar samma votering två gånger av samma skäl.
- **Ett tredje ben i A för propositioner.** Förkastat. Det ger regeringspartier poäng i A för det
  C redan mäter. Regeringskanalen finns dessutom i `a1`: M, KD och L får regeringens ram, och SD
  får den via Tidöavtalet plus Ja i rambeslutsvoteringen (`config/budget_ramar.yaml`).
- **Rollberoende vikt mellan `a1` och `a2` för regeringspartier.** Förkastat. Det skulle låta A
  läsa partiets roll, och rollen är C:s fråga.

## Konsekvenser

- **Ingen kodändring, ingen omkörning.** Beslutet bekräftar den byggda modellen och rättar
  dokumenten. Rankingen är oförändrad.
- `a2` läser en restkanal för regeringspartier, eftersom de driver politik genom proposition och
  budget snarare än genom motioner. Begränsningen accepteras. `a1` väger 0,6 och bär
  regeringskanalen.
- Voteringsprovet i `actions` matar inget betyg och får inte matas in i A. Det är inte en lucka att
  täppa.
- Namnet "Faktiskt agerande" är avfört. `IDEA.md` och ordlistan i
  `docs/done/evidens_trovardighet.md` §4.3 är ändrade i och med det här beslutet. Kvar att ändra i
  en byggslice: kommentaren i `config/scoring.yaml` under `A_agerande`, och strängen "A=agerande" i
  `coverage_technical` som `pipeline/scorerun.py` genererar. Gränssnittet visar ingen etikett för
  delpoängen, så där finns inget att ändra. Konfignyckeln `A_agerande` behålls tills slicen körs.
- Viktfrågan står kvar och blir skarpare: prioritering väger 40 procent, alltså mer än evidensen på
  35 procent. Den avgörs i [#9](https://github.com/mcknschn/rosta/issues/9).
