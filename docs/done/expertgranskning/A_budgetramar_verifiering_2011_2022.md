# Beslutsunderlag: sign-off av budgetåren 2011-2022 (a1)

> Handskrivet underlag, som [adversariell_verifiering.md](adversariell_verifiering.md). Resten av
> paketet är autogenererat av `pipeline/tools/review_packet.py`.
>
> **Status: väntar på mänsklig sign-off.** De tolv åren står som `version: 0` i
> `config/budget_ramar.yaml` och matar redan publicerade betyg, efter uttryckligt klartecken
> 2026-08-26.

ADR 0007 ([#27](https://github.com/mcknschn/rosta/issues/27)) utvidgade a1 från tre budgetår till
femton. Tolv nya år ska signas: 2011 till 2022. Åren 2023-2025 är signade sedan 2026-06-05 och
rörs inte.

Sign-off-protokollet i [README.md](README.md) steg 5 säger "jämför de transkriberade UO-beloppen
cell för cell mot bet. FiU1". De tolv åren bär 1647 nya celler, så en fullständig manuell
jämförelse är inte görbar. Det här dokumentet delar därför granskningen i två: vad maskinen redan
har bevisat, och vad som återstår som mänskligt omdöme.

## 1. Vad maskinen har bevisat

Verifieringen körs vid varje körning av verktyget och utfallet per år står i configens rad
`verification`. Den är starkare än den som fanns 2026-06-05, eftersom den nu har en oberoende
**absolut** tabell att gå emot.

| Lager | Vad det prövar | Utfall över alla 15 åren |
| --- | --- | --- |
| Summainvariant per kolumn | cellsumman mot källans egen rad "Summa utgiftsområden" | högst **4 mnkr** avvikelse, alltså inom avrundningen (toleransen är 27, en per utgiftsområde) |
| Bilagornas absoluta tabeller | annan tabell, annan enhet (tusental kronor), annan parser | regeringens ram träffar **på kronan i 15 av 15 år** |
| Reservationsbilagorna, där de finns | partiets absoluta ram mot dess avvikelsekolumn | **±1 mnkr**, alltså avrundningen, med ett undantag (se punkt 2d) |
| Betänkandets HTML | helt annan kodväg genom en annan filtyp | 5 år har läsbar HTML, alla utan avvikelse |
| Roll-call | attributionen mot voteringen i rambeslutspunkten | prövad varje år |
| Re-extraktion av de signade åren | hela kedjan mot ett tidigare, oberoende arbete | **405 celler, noll avvikelser** mot configen som signades 2026-06-05 |

Det sista lagret är det starkaste argumentet för de tolv nya åren. Samma kod, samma tabelltyp och
samma aritmetik träffar den redan expertgranskade transkriberingen exakt, cell för cell.

`python -m pipeline.tools.budget_ramar_transcribe --audit` kördes mot källan live 2026-08-26 och
svarade `config/budget_ramar.yaml matchar källan`.

**Avläsningen sker på tabellens geometri**, alltså kolumnens högerkant, och aldrig på cellernas
ordning. Det spelar roll: betänkandenas text delar ett tal vid tusentalsmellanslaget så fort två
celler är trånga, och kolumnen går då förlorad utan att felet syns i utfallet. Två tabeller är
dessutom satta liggande på stående sida.

## 2. Vad som återstår som mänskligt omdöme

Fem punkter. Maskinen kan inte avgöra någon av dem.

### 2a. Regeringstabellen

Det här är den **enda handskrivna faktauppgiften** i hela kedjan. Den avgör vems ram kolumnen
"Regeringens förslag" är, alltså vilka partier som tilldelas den på grunden `regeringsstallning`.
Raderna står i `pipeline/tools/budget_ramar_transcribe.py` under `GOVERNMENT` och är avskrivna ur
propositionernas avsändare. Budgetår Y bärs av prop. (Y-1)/Y:1.

| Budgetår | Regering | Proposition |
| --- | --- | --- |
| 2011-2014 | M, C, L (FP), KD | prop. 2010/11:1 till 2013/14:1 (Reinfeldt II) |
| 2015-2018 | S, MP | prop. 2014/15:1 till 2017/18:1 (Löfven I) |
| 2019 | S, MP | prop. 2018/19:1 (övergångsregeringen) |
| 2020-2022 | S, MP | prop. 2019/20:1 till 2021/22:1 (Löfven II) |
| 2023-2025 | M, KD, L | prop. 2022/23:1 till 2024/25:1 (Kristersson) |

Två rader förtjänar en blick. **2019** bars av en övergångsregering, vars proposition är en
framskrivning och inte ett politiskt program. **2022** beslutades i november 2021, medan MP lämnade
regeringen den 30 november 2021; propositionen 2021/22:1 är Löfven II:s, alltså S och MP:s, och
tabellen följer propositionen och inte kalendern.

Folkpartiet bytte namn till Liberalerna 2015-11-22. Koden `L` bär båda, och `FP` i källans
kolumnrubriker översätts till `L`.

### 2b. Den tredje attributionsgrunden

ADR 0007 punkt 2 säger att en ram är citerbar genom "egen budgetmotion, regeringsställning, eller
**uppslutning bakom en gemensam ram belagd med votering**". Den tredje grenen är operationaliserad
som: partiet röstade som regeringspartierna i voteringen om rambeslutet.

Den grenen bär tolv partiår:

| År | Parti | Sammanhang |
| --- | --- | --- |
| 2015-2019 | V | V var regeringens budgetpartner och lade ingen egen budgetmotion |
| 2020-2021 | C, L | Januariavtalet |
| 2023-2025 | SD | Tidöavtalet (redan signat 2026-06-05) |

Frågan att svara på: räcker "röstade som regeringen i rambeslutet" som belägg för uppslutning?
Alternativet vore att kräva ett skriftligt åtagande, vilket skulle fälla åren och korta fönstret.

### 2c. Gemensamma ramar

Två år bär en gemensam budgetmotion, så flera partier får identisk ram det året:

- **2011:** S, MP och V lade en gemensam motion (de rödgröna).
- **2015:** M, C, FP och KD lade en gemensam motion (allianspartierna).

Det är en riktig likhet i källan, och den jämnas aldrig ut. Frågan att svara på: ska en gemensam
motion räknas som "egen budgetmotion" för var och en av undertecknarna? Configen säger ja.

### 2d. Motionen, inte reservationen

Källan är jämförelsetabellen, alltså partiets **egen budgetmotion**. Betänkandenas bilagor bär
ibland en **reservation** i stället, som är ett förhandlat mellanting. De två skiljer sig:

| År | Reservation | Skillnad mot motionen |
| --- | --- | --- |
| 2015 | M, C, FP, KD gemensamt | 200 mnkr på UO2, 112 mnkr på UO25 |
| 2019 | M, KD gemensamt | upp till 2205 mnkr |
| 2022 | utskottets eget förslag (M, SD, KD) | upp till 3797 mnkr |

Configen använder motionen, eftersom a1 mäter partiets **egen** prioritering. Frågan att svara på:
är det rätt val, eller ska det parti som fick sin reservation antagen mätas på reservationen?

### 2e. Kostnaden för ett långt fönster

Ett långt fönster blandar ett partis regeringsår med dess oppositionsår, och för ett regeringsår är
ramen koalitionens och inte partiets egen. Kostnaden är skriven i förväg i ADR 0007 Följder. Så
här stor är den:

| Parti | Egen ram | Regeringens ram | varav regeringsställning | varav votering |
| --- | --- | --- | --- | --- |
| SD | 12 | 3 | 0 | 3 |
| V | 10 | 5 | 0 | 5 |
| C | 9 | 6 | 4 | 2 |
| M | 8 | 7 | 7 | 0 |
| KD | 8 | 7 | 7 | 0 |
| S | 7 | 8 | 8 | 0 |
| MP | 7 | 8 | 8 | 0 |
| L | 6 | 9 | 7 | 2 |

L mäts på regeringens ram i 9 av 15 år och SD i 3. Det är ingen defekt: det är vad det betyder att
mäta femton år av svensk budgetpolitik. Men det är asymmetriskt mellan partier, och asymmetrin
följer av hur ofta ett parti har regerat.

## 3. Stickprov mot källan

Två celler per nytt år, valda deterministiskt ur årtalet så att urvalet inte kan ha valts efter
utfallet. Kolumnerna visar hela härledningen: regeringens förslag plus partiets avvikelse ska bli
det tal configen bär. Slå upp betänkandet på `data.riksdagen.se/dokument/<dok_id>` och gå till den
angivna sidan i PDF:en.

| År | Betänkande | PDF-sida | Ram | UO | Regeringens förslag | Avvikelse | Summa | Configen |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2011 | GY01FiU1 | 83 | S_MP_V | UO5 | 2002 | ±0 | 2002 | 2002 |
| 2011 | GY01FiU1 | 83 | S_MP_V | UO23 | 17867 | +10 | 17877 | 17877 |
| 2012 | GZ01FiU1 | 102 | V | UO6 | 45578 | -1905 | 43673 | 43673 |
| 2012 | GZ01FiU1 | 102 | V | UO24 | 6012 | +2556 | 8568 | 8568 |
| 2013 | H001FiU1 | 111 | V | UO7 | 31192 | +3224 | 34416 | 34416 |
| 2013 | H001FiU1 | 111 | V | UO25 | 88906 | +1277 | 90183 | 90183 |
| 2014 | H101FiU1 | 105 | V | UO8 | 9919 | +640 | 10559 | 10559 |
| 2014 | H101FiU1 | 105 | V | UO26 | 22084 | ±0 | 22084 | 22084 |
| 2015 | H201FiU1 | 71 | SD | UO9 | 64441 | +3187 | 67628 | 67628 |
| 2015 | H201FiU1 | 71 | SD | UO14 | 71846 | +722 | 72568 | 72568 |
| 2016 | H301FiU1 | 98 | SD | UO1 | 12717 | -587 | 12130 | 12130 |
| 2016 | H301FiU1 | 98 | SD | UO15 | 21708 | +401 | 22109 | 22109 |
| 2017 | H401FiU1 | 106 | SD | UO2 | 15259 | +192 | 15451 | 15451 |
| 2017 | H401FiU1 | 106 | SD | UO16 | 72381 | -1347 | 71034 | 71034 |
| 2018 | H501FiU1 | 105 | SD | UO3 | 11399 | +354 | 11753 | 11753 |
| 2018 | H501FiU1 | 105 | SD | UO17 | 15880 | -530 | 15350 | 15350 |
| 2019 | H601FiU1 | 60 | SD | UO4 | 46343 | +4769 | 51112 | 51112 |
| 2019 | H601FiU1 | 60 | SD | UO18 | 6972 | -1029 | 5943 | 5943 |
| 2020 | H701FiU1 | 60 | V | UO5 | 2028 | ±0 | 2028 | 2028 |
| 2020 | H701FiU1 | 60 | V | UO19 | 3673 | +30 | 3703 | 3703 |
| 2021 | H801FiU1 | 67 | V | UO6 | 71153 | -1441 | 69712 | 69712 |
| 2021 | H801FiU1 | 67 | V | UO20 | 16202 | +1450 | 17652 | 17652 |
| 2022 | H901FiU1 | 94 | V | UO7 | 51940 | +500 | 52440 | 52440 |
| 2022 | H901FiU1 | 94 | V | UO21 | 4455 | +3005 | 7460 | 7460 |

Aritmetiken stämmer i alla 24 raderna. Det som återstår att kontrollera för hand är att de två
källtalen står som här i betänkandet.

Attributionen per parti och år står i [A_budgetramar.md](A_budgetramar.md), med citerad grund per
rad, och i `docs/done/a_forankring/fonster.json`.

## 4. Sign-off

När punkterna 2a till 2e är avgjorda och stickprovet är kontrollerat:

1. Inför eventuella rättelser i verktyget, aldrig i configen för hand. Configen är autogenererad.
2. Lägg de tolv åren i `SIGNED_OFF` i `pipeline/tools/budget_ramar_transcribe.py`, med datum.
3. Kör `python -m pipeline.tools.budget_ramar_transcribe --config`. Bara `version`-raderna ska
   ändras, och `git diff` ska visa noll ändrade tal.
4. Kör `python -m pytest`, `python -m pipeline.scorerun` och
   `python -m pipeline.tools.score_diff`. Betygen ska stå still: sign-off ändrar ingen siffra.
5. Kör `python -m pipeline.tools.review_packet` och publicera.
