# Förankringen för delpoäng A — metod

Bygger [ADR 0005](../adr/0005-a-forankras-i-tid-inte-i-faltet.md) i biljett
[#21](https://github.com/mcknschn/rosta/issues/21). Kod: `pipeline/anchor.py`,
`score.bounded_quotient`, `config/a_forankring.yaml`,
`pipeline/tools/a_forankring_transcribe.py`.

## 1. Vad som ändrades

A mätte förut varje partis andel mot de sju andra partierna. Rangnormaliseringen lade alltid det
lägsta partiet på 0,00 och det högsta på 5,00, så A:s spridning blev densamma oavsett vad
partierna föreslog. Efter den här slicen mäts andelen mot hur stor andel kategorin normalt fått
under ett historiskt fönster. För varje parti och kategori gäller

    q = (andel - förankring) / (andel + förankring)
    delpoäng = score.net_support_to_score(q)

`q` ligger i [-1, 1] av konstruktion och är 0 vid jämnhöjd. Ingen konstant väljs, och båda
halvorna får samma form. Blandningen 0,6 x a1 + 0,4 x a2 står orörd.

### 1.1 Golvet är nåbart, taket är det inte

Byggt 2026-08-30 i biljett [#35](https://github.com/mcknschn/rosta/issues/35) ur
[ADR 0012](../adr/0012-vaxelkursen-i-a-ar-harledd-ur-kvotens-andar.md) punkt 5. Kod:
`score.max_reachable_score`, `scorerun._a_ceilings` och `scorerun._a_ceiling_sentence`.

Andelen är högst 1, alltså hela partiets kraft i en enda kategori, så `q` når bara
`(1 - förankring) / (1 + förankring)`. Taket följer därför förankringens storlek och skiljer sig
mellan kategorier, medan golvet 0,00 nås överallt. Metodrutan i `dist/scores.json` bär talet per
kategori, räknat vid körningen ur förankringen i `config/a_forankring.yaml`, blandningen i
`config/scoring.yaml` och a1-grinden. En ändrad förankring följer med utan att någon rör texten,
och en inskriven konstant fäller `tests/test_a_taket.py`.

Snedheten jämnas inte ut. Varje utjämning kräver en vald konstant per kategori, och den enda
vinsten vore ett bredare spann, vilket ADR 0003 punkt 1 förbjuder som mål.

## 2. Förankringarna

| Halva | Förankring | Källa |
| --- | --- | --- |
| a1 | kategorins andel av de **beslutade** utgiftsramarna, medel över fönstret | bet. FiU1 per budgetår |
| a2 | kategorins andel av **kammarens samtliga** motioner i fönstret | `data.riksdagen.se/dokumentlista` |

Regeringens förslag förkastades som a1-förankring: det är ett blocks förslag varje enskilt år.
Den poolade partikammaren förkastades som a2-förankring: den är de åtta partierna viktade efter
hur mycket var och en skriver, alltså samma fältmått som beslutet avvisar.

Talen per kategori i det byggda fönstret:

| Kategori | a1-förankring | a2-förankring |
| --- | --- | --- |
| ekonomi | 25,4 % | 31,9 % |
| valfard | 42,6 % | 21,0 % |
| trygghet | 4,9 % | 8,6 % |
| forsvar | 8,6 % | 6,6 % |
| klimat | 4,8 % | 9,6 % |
| integration | 5,2 % | 12,1 % |
| demokrati | 4,8 % | 10,3 % |

## 3. Fönstret

Fönstret blev **2011-2025**. Båda gränserna skrevs före hämtningen och rördes inte efteråt.
Utfallet år för år ligger i [a_forankring/fonster.md](a_forankring/fonster.md), skrivet av

    python -m pipeline.tools.a_forankring_transcribe --window

- **a2-gränsen ger 2011.** Det är det tidigaste kalenderåret där alla åtta nuvarande partier har
  minst en motion i varje utskott som mappningen använder. 2010 faller på SD i civilutskottet
  (SD tillträdde i oktober 2010) och 2009 och 2008 faller på SD i samtliga femton utskott.
- **a1-gränsen ger 2008**, alltså det tidigaste år som prövades. Indelningen i utgiftsområde 1-27
  står oförändrad hela vägen, så gränsen binder inte.
- Fönstret börjar vid den senare av de två och slutar vid det sista färdiga året.

### 3.1 a1-gränsen prövas på indelningen, inte på namnen

ADR 0005 punkt 7 skrev gränsen som "samma 27 utgiftsområden med **samma namn** som
`mappings.expenditure_areas`". Den formuleringen går inte att pröva, och den prövningen fälldes
före bygget:

- `mappings.expenditure_areas` bär förkortningar som aldrig varit något års officiella namn.
  UO10 står som "Ekonomisk trygghet vid sjukdom", medan det officiella namnet är "Ekonomisk
  trygghet vid sjukdom och funktionsnedsättning" i vartenda granskat år. UO18 saknar på samma
  sätt "samt konsumentpolitik".
- Listan blandar dessutom två vintages. UO19 står med det nya namnet ("Regional utveckling",
  gäller från budget 2023) medan UO13 och UO20 står med de gamla ("Jämställdhet och nyanlända
  invandrares etablering", "Allmän miljö- och naturvård", gäller till och med budget 2023).

En bokstavlig namnlikhet ger därför noll år, alltså ett tomt fönster. Varje annat namntest
landar på budgetår 2024, eftersom UO13 och UO20 bytte namn då, vilket ger ett treårigt fönster
som krockar med ADR:ns egen kostnadslista ("alla åtta partier får högt A i försvar efter 2022"
förutsätter att fönstret når före 2022). Gränsen prövar därför **indelningen**: att
rambeslutstabellen listar utgiftsområde 1-27. Namnen hämtas och skrivs i bevisfilen så att en
omdöpning syns i efterhand, men de grindar inte. Beslutet togs av människa 2026-08-21, före
hämtningen av ramtalen.

### 3.2 Fönstret har hål i a2-gränsen som inte kortar det

Sju år inne i fönstret faller a2-gränsen på en enda cell: L i försvarsutskottet 2013, 2023 och
2024, V i skatteutskottet 2015, MP i finansutskottet 2019 och 2020, L i kulturutskottet 2022 och
L i arbetsmarknadsutskottet 2024. Det är regeringspartier som skriver få motioner (L skrev 54
motioner under hela 2024 mot S 834), inte en indelning som saknas. Gränsen är skriven som
"tidigaste år där ...", alltså ett tidigaste år och inte ett krav på varje år, och fönstret
kortas därför inte. Hålen står i bevisfilen.

Läsningen låstes i koden (`min` över godkända år) innan mätningen kördes, alltså före talen. En
sammanhängande läsning, där varje år i fönstret måste klara gränsen, skulle ge 2016-2025. Att
byta till den läsningen nu vore ett efterhandsomdöme av precis den sort punkt 7 förbjuder.

## 4. Den beslutade ramen per budgetår

"Beslutad" avgörs aldrig av gissning. Verktyget läser beslutspunktens `vinnare` och meningen om
utgiftsramarna ur betänkandet självt, och `_check_adopted` faller om något av dem drivit ifrån
det som står i koden. Tre år i fönstret avgjordes inte på regeringens förslag:

| Budgetår | Vinnare | Beslutad tabell |
| --- | --- | --- |
| 2015 | reservationen | Reservanternas förslag till utgiftsramar för 2015 (M, C, FP, KD) |
| 2019 | reservation 5 | Reservanternas förslag till utgiftsramar 2019 (M, KD) |
| 2022 | utskottet | Utskottets förslag till utgiftsramar 2022 (bilaga 4) |

Elva år transkriberades ur betänkandets HTML och fyra ur dess PDF (2015, 2016, 2021 och 2022,
där ingen HTML-tabell finns). Ingen runtime-parser finns: talen ligger i configen och
`--audit` kör dem mot riksdagen igen.

### 4.1 Korsverifiering

Budgetåren 2023, 2024 och 2025 finns redan i `config/budget_ramar.yaml` som `regeringen`-ramen,
transkriberad för hand och expertgranskad 2026-06-05. Verktygets extraktion matchar den
utgiftsområde för utgiftsområde i alla tre åren, alltså 81 av 81 tal.

## 5. Utfallet

Talen räknades ut EFTER att mekanismen låstes, enligt ADR 0005 punkt 8.

- **A:s viktade spridning gick 7,76 till 0,80.** Storheten är vikt gånger (max minus min) över de
  åtta partierna, summerad över de sju kategorierna, alltså samma mått som ADR 0003 diagnos
  punkt 3. A bar 61,4 procent av separationen före och bär 14,1 procent nu. B gick 28,0 till 62,4
  och D 10,6 till 23,5. Talet beror nu på underlaget: A:s spridning är 0,12 i ekonomi och 0,76 i
  klimat, i stället för samma tal överallt.
- **Nästan lika andelar ger nästan lika betyg.** I klimat skiljer 8,73e-06 S från M-blocket i a1.
  Före gav det 0,00 mot 1,79. Nu ger det 2,624 mot 2,624.
- **M, KD, L och SD får fortfarande samma a1** i alla sju kategorier. De föreslog samma ram, och
  likheten jämnas inte ut.
- **Den deklarerade kostnaden syns.** Försvarets andel av de beslutade ramarna gick från 5,6
  procent 2011 till 11,8 procent 2025, så alla åtta partier ligger över förankringen i försvar.
- **Rangordningen ändrades** från S > M > C > L > KD > SD > V > MP till
  M > KD > L > S > C > MP > SD > V. Det redovisas som det blev. Ökad eller minskad separation var
  aldrig ett mål (ADR 0003 punkt 1).
- **Flytten kommer av att A tystnar, inte av ett bättre A.** B och D står exakt stilla i den här
  slicen, så hela rangordningsflytten kommer ur att A slutade spänna ut nästan lika andelar över
  hela skalan. A väger fortfarande 0,30 men bär nu 14,1 procent av separationen. Det är beslutets
  avsedda verkan (ADR 0005 punkt 1), inte en bieffekt, men det ska sägas rakt ut.

## 6. Följdändringar

- `scale_semantics` i `config/scoring.yaml`: A flyttad från `relative` till `absolute`.
- `normalization.per_subscore.A` borttagen. `pipeline/config.py` faller om nyckeln läggs
  tillbaka, eller om A åter står under `relative`.
- `A_normalization` struken ur `pipeline/robustness.py`. Källan var mest inflytelserik av
  samtliga 21 i biljett #20 och har nu inget att dra i, eftersom A inte normaliseras. **A saknar
  därmed en dragen källa i känslighetsanalysen.** Närmaste kandidat är fönstret i ADR 0005
  punkt 7, men källistan är låst av ADR 0003 punkt 5 och en ny källa kräver en egen biljett.

  > **Rättad av [ADR 0010](../adr/0010-ett-reglage-ar-en-vag-pipen-redan-kan-ga.md),
  > 2026-08-27 (biljett #32).** A har åter en dragen post: blandningen `A_component_mix`,
  > med a1 i (0,50, 0,80]. Fönstret föll som kandidat, eftersom a2:s förankring är ett
  > aggregat utan år (punkt 6). Ordet för en dragen variationspunkt är numera **reglage**
  > (punkt 8). Texten ovan står som den skrevs.

## 7. Kör om

```bash
python -m pipeline.tools.a_forankring_transcribe --window   # gränserna -> bevisfil
python -m pipeline.tools.a_forankring_transcribe --config   # skriv om configen ur källan
python -m pipeline.tools.a_forankring_transcribe --audit    # config mot källa, exit 1 vid diff
python -m pipeline.scorerun                                 # bygg om dist/
python -m pipeline.robustness                               # 10 000 dragningar (lång)
```
