# Datainsamling och betygsmodell

Plan för hur Rösta samlar in data, beräknar partibetyg och deployar resultatet.
Bygger på [IDEA.md](IDEA.md) (modellen) och [CLAUDE.md](CLAUDE.md) (mål + källregel).

## Beslut som styr planen

| Fråga | Val | Konsekvens |
|-------|-----|------------|
| Betygssättning | **Helt automatisk via claims** | Alla delpoäng (A/B/C/D) beräknas deterministiskt från observationer, claims och regler. Mänskligt omdöme får bara finnas i *konfiguration*, aldrig i handsatta partibetyg. |
| Källor | **Myndigheter + svensk akademi** | Statliga myndigheter + etablerade svenska forskningskällor (SOM-institutet, universitet) där myndighetsdata saknas. Inga internationella index. **Undantag (2026-06-05, demokrati):** mellanstatliga Sverige-utvärderingar där Sverige är medlem (EU:s rättsstatsrapport, GRECO, OECD) får användas som *bekräftelse* av en svensk primärkälla — aldrig som primärkälla, aldrig som index. |
| Styrnivå | **Nationellt + region/kommun** | Ansvarskoppling sker både via regering (nationellt) och Kolada/SKR (region/kommun). |
| Teknik | **Python-pipeline + webb-frontend** | DuckDB/pandas lokalt, kompakt `scores.json` + `evidence.json` till frontend. |

### Antaganden (rätta mig om något är fel)
- **Partier:** de 8 riksdagspartierna — S, M, SD, C, V, KD, L, MP.
- **Tidsfönster:** 3 senaste mandatperioderna, valen **2014, 2018, 2022** → fönstret **2014–2026** (~12 år).
- **Deploy:** statisk frontend som läser förberäknade betyg. Inget rådata i extern deploy.

## 1. Arkitektur: observationer, claims, betyg + deploy-split

Din teori — rådata lokalt, endast betyg i deploy — är grunden. Konkret:

```
Lager 1  RÅ INSAMLING (endast lokalt)
  Officiella API:er  ->  data/raw/<källa>/<dataset>/<hämtdatum>.json  +  manifest
                         (käll-URL, dataset-id, fråga, hämtdatum, licens)

Lager 2  TRANSFORM / OBSERVATIONER (endast lokalt)
  Rådata  ->  data/warehouse.duckdb
              tidy-tabeller:
              - observations: indikator, kategori, undermått, år/period, värde, enhet, geografi, källa
              - actions: parti, datum/period, dokument/votering/budgetrad, kategori, källa
              - responsibility: parti, nivå, geografi, period, styrkegrad, källa

Lager 3  CLAIMS / INDIKATOREFFEKTER (endast lokalt, bantat index deployas)
  Observationer + regler -> claims
                         -> indicator_effects
                            (parti, förslag/agerande, indikator, förväntad riktning,
                             stöd/motsägelse, effektstyrka, osäkerhet, källor)

Lager 4  BETYG (det som deployas)
  Claims + indikatorer + regler  ->  dist/scores.json     (per parti × kategori: 0-5 + osäkerhet)
                                    dist/evidence.json    (bantad claims-/bevisindex)
```

**Deploy-artefakt = endast `dist/scores.json` + `dist/evidence.json` + metodbeskrivning.**
`data/raw/` och `data/warehouse.duckdb` är `.gitignore`:ade och stannar lokalt.

Frontend gör i webbläsaren: `totalpoäng = Σ (kategoribetyg × användarens vikt)`.
Kategorivikterna bakas alltså **inte** in i betygen — de sätts av användaren vid körning (precis som IDEA.md kräver).

### Varför `evidence.json` också skickas med
"Objektivt utifrån faktiskt data" måste vara verifierbart. `evidence.json` innehåller per betyg: källhänvisningar, relevanta claims och de nyckelvärden betyget vilar på — men **inte** hela rådatadumpen. Spåret följer med, tyngden stannar lokalt.

Ett claim är ett litet granskningsbart påstående, till exempel:

- "Parti X röstade ja till reform Y."
- "Parti X föreslog +N kronor till utgiftsområde Z."
- "Förslaget kopplas till indikatorn sysselsättning med förväntad positiv riktning."
- "Källa A stödjer att åtgärdstypen brukar öka sysselsättning, med medelhög säkerhet."
- "Partiet hade regeringsansvar under perioden där indikatorn senare förändrades."

## 2. Repo-struktur

```
rosta/
  config/
    categories.yaml      # 7 kategorier, undermått, standardvikter, positiv riktning  (från IDEA.md)
    sources.yaml         # endpoints, dataset-id, licens per källa
    mappings.yaml        # utgiftsområde<->kategori, indikator<->undermått,
                         # partiernas regeringsperioder, region/kommun-styren
    scoring.yaml         # delpoängvikter (30/50/0/20), normaliserings- och osäkerhetsregler
    claims.yaml          # claim-typer, tillåtna effektetiketter, evidensnivåer
  pipeline/
    sources/             # en modul per källa: fetch -> cache -> normalize
      riksdagen.py  scb.py  bra.py  kolada.py  skolverket.py  ...
    transform.py         # rådata -> warehouse-tabeller
    claims.py            # observations/actions/responsibility -> claims
    effects.py           # claims -> indicator_effects
    score.py             # indicator_effects + config -> dist/scores.json, dist/evidence.json
    schema.py            # validering av output
  data/                  # .gitignore  (raw/ + warehouse.duckdb)
  dist/                  # scores.json, evidence.json  (det enda som deployas)
  web/                   # frontend (läser dist/)
  tests/                 # golden tests på scoringmatte + schema-validering
```

## 3. Källregister

Genomgående källor (försörjer A och C för alla kategorier):

| Källa | Vad | Försörjer |
|-------|-----|-----------|
| Riksdagens öppna data (data.riksdagen.se) | Voteringar, motioner, propositioner, betänkanden, ledamöter | A (agerande) |
| Statsbudget / utgiftsområden (ESV, regeringen, finansutskottet) | Anslag per UO, partiernas budgetmotioner, saldo | A (prioritering), C (finansiering) |
| Valmyndigheten + Regeringskansliet | Valresultat, regeringssammansättning per period | C (nationellt ansvar) |
| SKR "Styren i kommuner och regioner" | Vilket parti/koalition styrde var | C (regionalt/kommunalt ansvar) |

Per kategori (försörjer objektiva kategoriutfall och D resultat, samt behovsbilden för B). Riktning enligt IDEA.md:

| # | Kategori | Huvudkällor | Exempelindikatorer |
|---|----------|-------------|--------------------|
| 1 | Ekonomi och jobb | SCB, Riksbanken, ESV, Konjunkturinstitutet | Arbetslöshet (AKU), BNP per capita, produktivitet, KPIF, reallöner, statsskuld/saldo |
| 2 | Välfärd | Socialstyrelsen, Skolverket (SiRiS), Kolada, SKR Vården i siffror, Brå | Vårdköer, vård i tid, skolresultat, behöriga lärare, personalomsättning omsorg, välfärdsbrott |
| 3 | Lag och trygghet | Brå (inkl. NTU), Domstolsverket, Åklagarmyndigheten, Kriminalvården | Dödligt våld, skjutningar, brottsutsatthet, otrygghet, uppklaring, handläggningstid, återfall |
| 4 | Försvar och beredskap | Statsbudget UO 6, Försvarsmakten, MSB, FOI, Regeringskansliet | Försvarsanslag % BNP, personal/värnpliktiga, materielbeslut, civil beredskap, Ukrainastöd |
| 5 | Klimat, miljö, energi | Naturvårdsverket, SCB, Energimyndigheten, Svenska kraftnät, SLU Artdatabanken | Territoriella + konsumtionsbaserade utsläpp, fossilandel, elprisvolatilitet, effektbalans, hotade arter |
| 6 | Integration och sammanhållning | SCB, Skolverket, Boverket, SOM-institutet | Sysselsättningsgap in-/utrikes födda, självförsörjning, SFI-resultat, trångboddhet, segregation, valdeltagande |
| 7 | Frihet, demokrati, institutioner | Statskontoret, Riksrevisionen, SOM-institutet, MPRT/Nordicom, JO/JK | Myndighetstillit, mediemångfald, förvaltningsstyrning, rättssäkerhet, ansvarsutkrävande |

Evidens-/utvärderingskällor (försörjer **B** — `evidence_effect`-claims om huruvida en åtgärdstyp rimligen påverkar indikatorerna). Dessa svenska utvärderingsorgan utgör den citerade evidensliggaren; inga internationella index (undantag: mellanstatliga Sverige-utvärderingar som *bekräftelse*, se beslutstabellen ovan):

| Källa | Vad den utvärderar | Försörjer B i kategori |
|-------|--------------------|------------------------|
| IFAU | Arbetsmarknads- och utbildningspolitikens effekter | 1, 2, 6 |
| Vårdanalys (Myndigheten för vård- och omsorgsanalys) | Vård- och omsorgsreformers effekter | 2 |
| SBU | Medicinsk och social metodutvärdering | 2 |
| Skolforskningsinstitutet | Skolinsatsers effekt | 2 |
| Brå (utvärderingsdelen) | Kriminalpolitiska åtgärders effekt | 3 |
| FOI | Försvars- och säkerhetspolitisk analys | 4 |
| Klimatpolitiska rådet | Om klimatpolitiken når beslutade mål | 5 |
| Tillväxtanalys | Närings- och tillväxtpolitik | 1, 5 |
| Finanspolitiska rådet | Finanspolitikens hållbarhet och effekt | 1 |
| Konjunkturinstitutet | Makro- och miljöekonomisk analys | 1, 5 |
| ESO (Expertgruppen för studier i offentlig ekonomi) | Studier i offentlig ekonomi (brett) | tvärgående |
| Riksrevisionen | Statliga insatsers effektivitet och måluppfyllelse | tvärgående (särskilt 4, 7) |
| Statskontoret | Förvaltnings- och styrningsutvärdering | 7, tvärgående |
| Vetenskapsrådet / svenska forskningsöversikter | Akademiskt kunskapsläge | tvärgående |
| Mellanstatliga Sverige-utvärderingar (EU:s rättsstatsrapport, GRECO, OECD) — endast som *bekräftelse* | Landsspecifika utvärderingar av Sverige (ej index) | 7 (demokrati), undantag 2026-06-05 |

**Exakta endpoints/dataset-id pinnas i `config/sources.yaml` vid första hämtningen (Fas 1)** — de verifieras live, inte gissas.

## 4. Automatisk betygsmodell

Per parti och kategori (delpoängvikter från IDEA.md):

```
Kategoribetyg = 0,40·A + 0,35·B + 0,15·C + 0,10·D        (A,B,C,D ∈ [0,5])
```

Allt nedan är deterministiskt. Normalisering till 0–5 sker per kategori över de 8 partierna (min–max eller rang, satt i `scoring.yaml`).

Bedömningskedjan är:

```
objektiva kategoriindikatorer
  -> partiets agerande
  -> claims om förväntad indikatoreffekt
  -> ansvar/attribution
  -> uppmätta resultat
  -> kategoribetyg
```

Väljaren viktar kategorier, inte ideologiska metoder. Scoringen ska därför inte fråga om en åtgärd är "höger" eller "vänster", utan om den enligt källorna rimligen påverkar indikatorerna i positiv eller negativ riktning.

### Två nivåer: vad varje delpoäng sitter på

De fyra delpoängen lever på **två olika nivåer** i begreppsmodellen (Kategori → Undermått → Indikator → Riktning). Det är avsiktligt — inte en lucka att linjera bort:

| Delpoäng | Mäter | Nivå | Sitter på indikatorer? |
|---|---|---|:---:|
| **A** | prioritering (budgetandel + motionsandel) | **Kategori** | nej |
| **B** | evidens för ståndpunkt (instrument → indikatoreffekt) | **Indikator/undermått** | **ja** |
| **C** | makt/ansvar | **Kategori** | nej |
| **D** | utfall (årsserie förbättrades under ansvar) | **Indikator/undermått** | **ja** |

- **A och C är kategorinivå** och har inga indikatorer: prioritering (budget-UO + motionsandel) och makt är egenskaper hos (parti × kategori), inte hos en enskild indikator. De har alltid ett värde för varje kategori — ingen undermåttslucka kan göra dem "tunna" — och utgör tillsammans 55 % av kategoripoängen. Att efterfråga "samma indikatorer" för A/C är därför ett kategorifel.
- **B och D är indikator-/undermåttsnivå** och sitter på *samma* indikator-id. Idealet är därför **B+D på samma undermått** (framåtblickande evidens + bakåtblickande utfall = fullständig bild). Var detta uppnås spåras i mastertabellerna ([done/evidens_trovardighet.md §4.3](docs/done/evidens_trovardighet.md) för B/D-status, [spar_D_datatackning.md §2.1](docs/done/spar_D_datatackning.md) för D-täckning).
- **Mål: maximal union av B och D — inte tvingad identitet.** B når indikatorer D aldrig kan (mediefrihet/korruption = D förbjuden; kvalitativt/sekretess = materiel, civil beredskap), och D når rena makroutfall där inget rent instrument finns att koda B mot. Att tvinga samma indikatormängd vore att krympa till snittmängden och kasta täckning. Tunnhet i en kategoris B/D-bredd hanteras därför genom att *bredda unionen* och krympa D efter bredd ([docs/done/d_coverage_krympning_spec.md](docs/done/d_coverage_krympning_spec.md)) — inte genom att linjera de fyra linserna. (Skild men parallell strukturaxel: skalsemantiken nedan, relativ A/C vs absolut B/D.)

**A — Faktiskt agerande** (vad partiet prioriterat, *relativt* — inte i absolut volym): `A = 0,6·a1 + 0,4·a2`.
- `a1` budgetprioritering **(byggd, Fas 1b):** andel av partiets föreslagna utgiftsramar (Σ kategorins UO / Σ alla 27 UO), rank-normaliserad över de 8 partierna. Ramtalen transkriberas troget ur officiella källor (FiU1 rambeslut + budgetmotioner) till `config/budget_ramar.yaml` med källrad per frame — **ingen runtime-parser** (det finns ingen strukturerad API-väg till anslag per UO; en bräcklig parser fick inte korrumpera A, tyngsta delpoängen). **Hård grind:** a1 vägs in för en (budgetår, kategori) endast när alla 8 partier har verifierad ram för varje kategori-UO; annars `A = a2` (flagga `A_a2_only`). Saknad cell → hård fail, aldrig tyst 0. a1 är ett snitt över **tre budgetår (2023–2025)** ur respektive FiU1-rambeslut; version 1, expertgranskad (mänsklig sign-off 2026-06-05). [Metod](docs/done/fas1b_budget_metod.md).
- `a2` lagstiftningsprioritering: **andel av partiets egna motioner** som rör kategorin (= motioner i kategorins utskott / partiets totala motioner), rank-normaliserad över de 8 partierna.
- **Varför andel och inte antal:** rå volym belönar stora partier — de skriver mer om *allt* och blir då höga i varje kategori. Andelen mäter prioritering oberoende av partistorlek, så en kategori tillfaller de partier som faktiskt lägger en stor del av sitt arbete (eller sina pengar) där. *(Brasklapp: ett mycket litet enfråge-parti kan se 100 % fokuserat ut; därför rank-normaliseras värdet efteråt.)*
- Mäter *emfas/prioritering*, inte om politiken är rätt — det fångas av B och D.

**B — Evidens/träffsäkerhet** (har förslagen stöd för påstådd effekt):
- Varje relevant förslag/agerande kopplas till ett eller flera `indicator_effects`.
- Ett `indicator_effect` anger indikator, förväntad riktning, effektstyrka, källstöd, eventuell motsägande evidens och osäkerhet.
- `B` blir hög när partiets förslag har starkt källstöd för positiv påverkan på kategorins indikatorer.
- `B` blir lägre när källor saknas, effekten är oklar, effekten går emot den positiva indikatorriktningen, eller förslaget har tydliga negativa sidoeffekter inom samma kategori.
- Detta motverkar A:s "mer aktivitet eller mer pengar = bättre"-problem. A mäter vad partiet gör; B mäter om det partiet gör sannolikt hjälper mot de objektiva indikatorerna.
- **Maskineri (Fas 4b, byggt):** `config/party_positions.yaml` (källbelagda partiståndpunkter per åtgärdstyp) joinas mot `config/evidence_ledger.yaml` (åtgärdstyp → indikatoreffekt) → `indicator_effects` → B (`pipeline/positions.py` + `pipeline/effects.py`). Stödjer partiet åtgärdstypen behålls evidensens riktning; motsätter det sig vänds den. Ståndpunktsfilen innehåller **269 källbelagda ståndpunkter** (192 t.o.m. B2 2026-06-05/06, varav 130 panel-harmoniserade Fas 4c + 8 FoU-avdrag + 8 företags-/ägarbeskattning + 8 hushållens disponibla inkomst + 7 grundlagsskydd domstolarnas oberoende + 8 begränsa biometrisk realtidsövervakning + 7 Nato-medlemskap + 8 snabbförfarande/lagföring + 8 åtgärder mot invasiva arter; + senare D-/B3-poster t.o.m. 2026-06-14; version 2, expertgranskad; de enhällighetsbyggda via **enhällighet-som-källa** = enhälligt betänkande → alla 8 partier supports, se docs/done/evidens_trovardighet.md); saknas rad för (parti, kategori) är B coverage-viktad mot neutral (flaggor `B_thin_coverage`/`B_no_party_evidence`). Inga ståndpunkter fabriceras.

**C — Genomförbarhet/ansvar** (makt + realistisk finansiering):
- `c1` makt **(byggd, nationell + regional + kommunal, Fas 1c):** per kategori blandas andel av 2014–2026 partiet satt i nationell regering (stöd vägs 0,5) med subnationell makt (SKR-styren: 21 regioner + 290 kommuner × 3 mandatperioder), via en per-kategori region/kommun-split efter lagstadgat ansvar och rank-normaliserat (`level_weights` + `subnational_split`). Full subnationell täckning → C:s säkerhet hög; forsvar nationellt per design ([metod](docs/done/fas1c_subnational_metod.md)).
- `c2` finansiering: **uppskjutet (beslut Fas 1c)** → C = c1. Ett objektivt, riktningsneutralt och differentierande finansieringsmått går inte att bygga ur officiell data (alla partibudgetar är formellt finansierade → likformigt; ett saldomått gynnar åtstramning → bryter neutraliteten). "Löftesuppfyllelse" fångas redan av A+B+D. Komponentvikterna behålls som avsikt.

**D — Resultat** (förbättrades indikatorerna där partiet hade ansvar):
- För perioder/områden där partiet styrde (från C): förändring i kategorins indikatorer mot positiv riktning, **tidsförskjuten** och attributionsviktad.
- **Implementerat (Fas 5b):** för varje nationell årsindikator (`up`/`down`; `target` hoppas över, saknar målnivå) tas *tecknet* på den riktningsjusterade årsförändringen (förbättring +1 / försämring −1 / oförändrat 0 inom en relativ dödzon). Varje årsförändring (år y−1 → y) tillskrivs regeringen som satt år y−1 (`attribution_lag_years = 1`), viktad med maktvikt (regering 1,0, stöd 0,5) — koalitionspartier delar därför samma resultat. Per kategori: undermåttsviktat medel → `net ∈ [−1,1]` → betyg via samma 0→2,5-skala som B. *Tecken, inte magnitud*, håller måttet robust och ödmjukt (IDEA.md:s konjunktur-caveat). Täckning (per 2026-06-12): D matas i **ALLA 7 kategorier** — 38 kanoniska årsserier över 28 av 35 undermått. Försvar och demokrati fick sina första D-serier 2026-06-07 (Försvarsmaktens ÅR resp. Brå NTU) och har breddats sedan (försvar 3/5, demokrati 5/5, integration 5/5 undermått). **Aktuell status per indikator/undermått: [docs/spar_D_datatackning.md §2.1](docs/done/spar_D_datatackning.md) (sanningskälla).** Kvarvarande D-luckor (materiel/civil-beredskapsnivå/leverans = sekretess/pengar; internationella demokrati-index = otillåtna) är allowlistade i `config/coverage_allowlist.yaml`.
- **Rättvisa:** partier med litet/inget ansvar (ansvarsunderlag < `min_responsibility`) får D ≈ neutral (2,5) med **bred osäkerhet** och flaggan `D_not_applicable` — de straffas inte för utfall de inte rådde över. Tunt ansvarsunderlag flaggas `D_thin_basis`.
- **D-bredd (sedan 2026-06-12, `coverage_shrink`):** D renormaliserar inte längre bort saknade icke-target-undermått — de bidrar neutralt (net 0) i en fast nämnare av undermåttsvikt, så D gör inget oavkortat kategorianspråk på en delmängd av kategorin. Numeratorn är per (parti, kategori); varje uppmätt cell flaggas `D_coverage_<täckt>/<total>` och viktad täckning < 0,75 ger `D_thin_coverage` + sänkt säkerhet. Tunn bredd grindas via `coverage_allowlist.d_thin_breadth_accepted` (i dag endast försvar 70/100). [Spec](docs/done/d_coverage_krympning_spec.md).
- **Subnationell D (C3, sedan 2026-06-14, `subnational.enabled`):** för submått där utfallet är region-/kommunstyrt blandas det nationella submåtts-nätet med ett **region-poolat** net — ett regionalt utfall (vårdköer/överlevnad) attribueras till det parti som styrde DEN regionen det året (`score.attribute_subnational_indicator`; dagviktad region-år-makt, lika per-region-vikt, bara tecken). Speglar hur C blandar nationell + subnationell makt (`level_weights`). v0 = region-nivå välfärd (`vard_tillganglighet`, national 0,4 / region 0,6 — regionen är sjukvårdshuvudman). Regionalt ansvarsunderlag normaliseras till år-ekvivalent och adderas i grinden (ett parti med **enbart** regional vård-makt blir measured — rättvisefix, t.ex. V); en soundness-grind (`region_basis ≥ min_responsibility`) hindrar att brus ur ett pyttigt region-år-urval dominerar (t.ex. SD). Neutralitetsauditerad (`pipeline/tools/c3_sensitivity.py`); `enabled:false` = byte-identisk ren nationell D. Endast välfärds-D rör sig, totalrankingen oförändrad. [Metod](docs/done/c3_subnational_d_metod.md).

### Claims-modell

Claims är intern, normaliserad bevisdata. De byggs från rådata, dokument, voteringar, budgetposter, indikatorserier och evidenskällor.

Minsta claim-format:

```json
{
  "id": "claim:...",
  "type": "action|claimed_effect|evidence_effect|responsibility|observed_result",
  "party": "M",
  "category": "ekonomi",
  "submeasure": "sysselsattning",
  "indicator": "arbetsloshet",
  "period": "2022-2026",
  "statement": "Partiet föreslog reform X med påstådd effekt Y.",
  "direction": "positive|negative|mixed|unclear",
  "effect_strength": "low|medium|high|unknown",
  "confidence": "low|medium|high",
  "source_refs": ["riksdag:...", "scb:...", "rapport:..."]
}
```

Claims får inte vara fristående omdömen utan källstöd. Om ett claim bygger på en tolkningsregel ska regeln finnas i `config/claims.yaml` eller `config/scoring.yaml`.

`indicator_effects` aggregerar flera claims till en maskinläsbar effektbedömning:

```json
{
  "party": "M",
  "category": "ekonomi",
  "indicator": "arbetsloshet",
  "expected_direction": "down",
  "net_support": 0.72,
  "confidence": 0.61,
  "supporting_claims": ["claim:1", "claim:2"],
  "contradicting_claims": ["claim:3"]
}
```

### Osäkerhet (IDEA.md kräver intervall)
Varje delpoäng har en **default-säkerhetsnivå** (A hög, B medel, C hög, D låg) som **datan kan överskrida per (parti, kategori)** — så intervallet blir datadrivet, inte konstant:
- **B** får sin säkerhet från `indicator_effects`-aggregatets confidence; saknas effekter helt → `low` (brett).
- **D** är `low` (bred) när ansvaret är för litet → not_applicable (markeras med flaggan `D_not_applicable`), annars `measured` (smalare).
- **C** sänks ett steg när subnationell styresdata saknas (omviktas då till 100 % nationellt).

Intervallets halvbredd per kategori = `max_halfwidth × Σ(delpoängvikt × (1 − säkerhet))`. Frontend propagerar kategoriintervallen till totalpoängens intervall vid körning. Visas som `3,84 / 5 (3,5–4,1)` precis som i IDEA.md.

**Skalsemantik:** A och C är *relativa* (rangordnas över de 8 partierna; A=5 = "mest av alla", inte "absolut bra"), medan B och D är *absoluta* (net_support=0 → 2,5 oberoende av andra partier). A och C-makt rank-normaliseras (inte min–max) eftersom de bara har 8 datapunkter och är känsliga för en enda outlier.

## 5. Output-scheman

`dist/scores.json` (deployas):
```json
{
  "meta": { "generated": "2026-…", "window": "2014-2026",
            "window_end": "2026-09-13", "window_open": true,
            "data_as_of": "2025-12-31", "latest_observation_year": 2026,
            "parties": ["S","M","SD","C","V","KD","L","MP"] },
  "categories": [{ "id": "ekonomi", "submeasures": ["sysselsattning", "..."] }],
  "scores": {
    "M": {
      "ekonomi": {
        "score": 4.0, "ci": [3.6, 4.3],
        "components": { "A": 4.1, "B": 3.8, "C": 4.2, "D": 3.9 },
        "claim_refs": ["claim:ekonomi:M:..."],
        "evidence_refs": ["scb:AKU:2025", "riksdag:votering:2023:UO24:..."]
      }
    }
  }
}
```

**Fönstrets slut mot underlagets slut:** `window_end` är mandatperiodens formella slut, alltså nästa valdag. Det datumet ligger i framtiden tills valet hållits. `window_open` säger att perioden pågår, alltså att betygen för den är preliminära. `data_as_of` är något annat: sista dagen underlaget faktiskt når. Serierna är årsserier, så ett år som fortfarande pågår flyttar inte fram datumet. Det året syns i stället som `latest_observation_year`. De två datumen får aldrig blandas ihop (issue #3).

`dist/evidence.json` (deployas): per `claim_ref` och `evidence_ref` → claim-sammanfattning, källnamn, dataset-id, hämtdatum, nyckelvärde, käll-URL. Bara bantade claims och nyckelvärden deployas, inte hela rådatat eller alla interna arbetsfält.

## 6. Insamlingsordning (roadmap)

Detaljerad, körbar exekveringsplan per fas (mål, tasks, filer, verifiering, exit-kriterier):
**[docs/ROADMAP.md](docs/done/ROADMAP.md)** (fryst historik, faser 0–6).
Framåtblickande arbete (ny datatäckning, evidenskvalitet, drift) ligger i
**[docs/BACKLOG.md](docs/BACKLOG.md)**, organiserat efter arbetsspår.

Status nedan: ✅ byggd & verifierad · 🟡 byggd, avgränsad täckning (loggas). Hela
pipelinen körs lokalt med `python -m pipeline.build_all`.

| Fas | Status | Innehåll | Varför först |
|-----|--------|----------|--------------|
| 0 | ✅ | Repo-skelett, `config/*.yaml`, claim-typer, källregister, scheman, scoringmatte, golden tests, CI | Grund |
| 1 | ✅ | Riksdagen (live): `responsibility` 11 rader + `party_activity` 120 rader (motioner/parti×utskott, hela fönstret) + voteringsprov 190 rader (12 riksmöten) | Definierar A, C och parti/period-ställningen allt annat hänger på |
| 2 | 🟡 | SCB + Kolada + Brå (live): **386 obs, 17 kanoniska årsindikatorer** (15 direkta + 2 härledda) i 5 kategorier (ekonomi, välfärd, klimat, integration, trygghet) | Bredaste resultatkällorna; täcker flera kategorier |
| 3 | 🟡 | Täckningsverktyg (`coverage_report`) + allowlist (`coverage_allowlist.yaml`) + coverage-gate (inget tyst gap); evidensliggaren 46 källverifierade poster (≥3/kat, expertgranskad v2 2026-06-07); fler D-sektorsadaptrar kvarstår | Fyller återstående undermått, gör luckor explicita |
| 4 | ✅ | Claims/effects/positions engine (`pipeline/{claims,effects,positions}.py`), aggregering testad; B partikopplas via ståndpunkter | Gör evidens/träffsäkerhet granskningsbar |
| 5 | ✅ | Scoring engine + **D-resultatattribution** → `dist/scores.json` (8×7) + `dist/evidence.json` (604 claims), golden tests | Producerar deploy-artefakten |
| 6 | ✅ | Frontend (`web/`): client-side viktning, rankad partilista, osäkerhetsintervall, bevisspår — lokalt verifierad | Användarupplevelse och transparens |

### Uppföljning (b-faser)

✅ levererad & verifierad · 🟡 avgränsad/uppskjuten (loggas). Förfiningar ovanpå fas 0–6.

| b-fas | Status | Innehåll |
|-------|--------|----------|
| 2b | ✅ | 8 kanoniska årsserier verifierade live mot officiella källor: SCB (arbetslöshet TAB2891, sysselsättning TAB6514, BNP/capita TAB6728, växthusgaser TAB4698, trångboddhet TAB6439), Kolada (meritvärde åk 9 N15507, behöriga lärare N15813, ekonomiskt bistånd N31825). Rätt enskild nationell serie isoleras via `fixed`. Fixade `kolada.kpi_title`-bugg. |
| 5b | ✅ | D-resultatattribution: tecken på riktningsjusterad årsförändring, lag-attribution till sittande regering, makt-/koalitionsvikt, `min_responsibility`-gate, `D_thin_basis`-flagga. |
| 4b | ✅ | B-maskineri (`party_positions × evidence_ledger → indicator_effects → B`) byggt och testat. **B utrullad för ALLA 7 kategorier (version 0):** klimat handkurerat (votering bet. 2023/24:MJU5 + koldioxidskatt), övriga via research+verifierings-workflow mot riksdagens fulltext (fångade fabrikat). **Coverage-viktad B** (`2.5 + (B_raw−2.5)·coverage`, `B_thin_coverage`-flagga) — annars mättade B vid 5.0. [Metod](docs/done/fas4b_partistandpunkter_metod.md). Ingen fabrikation. |
| 4c | ✅ | **B-differentiering (byggd version 0, sedan expertgranskad → version 2):** rubrik fryst + negativ-grind testtvingad; alla ståndpunkter **panel-harmoniserade** (19 åtgärdstyper × 8 partier sida vid sida, M/L-asymmetri rättad); liggaren utökad med enda omstridda åtgärdstyp som passerade evidens-/negativ-grinden av 8 (`ny_karnkraft`→effektbrist, Svenska kraftnät; 7 inerta). **130 ståndpunkter** (109 harmoniserade non-klimat + 14 klimat + 7 kärnkraft). Känslighetsanalys ±0.08; 0 admitterade negativ-riktnings-poster. [ROADMAP Fas 4c](docs/done/ROADMAP.md) · [audit](docs/done/fas4c_planB_audit.md) · [kandidatregister](docs/done/fas4c_planA_kandidatregister.md). |
| 1b | ✅ | `a1` budgetprioritering **byggd och aktiv** (gated): partiernas föreslagna utgiftsramar per UO **över tre budgetår (2023–2025)** ur bet. 2022/23:FiU1, 2023/24:FiU1 (tabell 2.3) + 2024/25:FiU1 (tabell 35), troget transkriberade till `config/budget_ramar.yaml` (ingen runtime-parser; version 1, expertgranskad 2026-06-05). a1 = snitt över åren (snitt-skärning av aktiva kategorier). A = 0,6·a1 + 0,4·a2; hård grind kräver alla 8 partier per kategori-UO annars `A=a2`. Adversariellt verifierad: intern invariant per år + oberoende parser (pandas) + Codex re-extraktion (0 avvikelser, 270 celler) + roll-call. [Metod](docs/done/fas1b_budget_metod.md). Voteringsprov utökat till hela fönstret (12 riksmöten, sampelt; matar ännu inget betyg). |
| 1c | ✅ | **Subnationell styresdata (regioner + kommuner) → C.** Alla **21 regioner + 290 kommuner × 3 mandatperioder** (post-val-styre 2014/2018/2022) ur SKR:s öppna data "Styren i regioner/kommuner 1994-2022" ([dataset 80](https://catalog.skl.se/catalog/1/datasets/80) + resource/127), region-2022 korsverifierad exakt (21/21), kommun-2022 inom ±2 av halvtidsuppföljnings-PDF. `pipeline/sources/skr.py` → `responsibility` (regional 219 + municipal 2706 rader); `scorerun.regional_fractions()`/`municipal_fractions()` + `category_c()` blandar nationell + subnationell makt per kategori via en **region/kommun-split efter lagstadgat ansvar** (`level_weights` + `subnational_split`), rank-normaliserat. Full subnationell täckning → C-säkerhet **hög**; forsvar nationellt per design. Fixar den tidigare **platta per-parti-C-konstanten**. Golden-tally pinnar datan mot SKR; Codex-granskad regionaldesign. **c2 (finansiering) uppskjutet** (ej neutralt/objektivt byggbart → C = c1). [Metod](docs/done/fas1c_subnational_metod.md). |
| 3 (T3.0/3.x) | ✅ | Täckningsverktyg `pipeline/tools/coverage_report.py` + coverage-gate (`tests/test_fas3_gate.py`): varje indikator är inläst ELLER allowlistad (`config/coverage_allowlist.yaml`, [docs/done/fas3_coverage.md](docs/done/fas3_coverage.md)) — inget tyst gap. 7 nya D-serier: vårdköer (Kolada N79242), konsumtionsbaserade utsläpp (SCB TAB5637), självförsörjningsgrad utrikes födda (SCB TAB6529), dödligt våld (Brå Tabell 20), **fossil energianvändning (Energimyndigheten EN0202_8, PxWeb v1 — ny adapter `pipeline/build_fas3.py`)**, **brottsutsatthet + upplevd otrygghet (Brå NTU Tabellsamling, blad 3A + 4A:1, `bra.fetch_ntu`)**. Fixade SCB-loaderbugg (eliminerbara dimensioner). D mäts nu i **5 kategorier**; klimat har 3 D-serier och **trygghet 3** (dödligt våld + NTU-utsatthet + NTU-otrygghet). **Härledda indikatorer** (`pipeline/derived.py`, deterministisk gap/kvot ur två verifierade serier, två-tabells-operander + rimlighetsgrind): `sysselsattningsgap_inrikes_utrikes` (SCB TAB6529, sysselsättningsgrad inrikes − utrikes födda) och `produktivitet` (SCB TAB3610 BNP fasta priser ÷ TAB5622 arbetade timmar, kr/timme; Codex- + adversariellt verifierad mot finanskris- och 2022–2023-svackorna). **17 D-dugliga indikatorer / 386 obs.** |
| 3 (T3.9) | ✅ | Evidensliggaren (B): **46 källverifierade poster, ≥3/kategori (alla 7)** (ursprungligen 29 + `ny_karnkraft`→effektbrist via Svenska kraftnät, Fas 4c; utökad via B2/B3). Källor URL-bekräftade (stickprov manuellt: IFAU 2025:17, SBU 369, Svk Kraftbalansen 2025), version 2 — expertgranskad (sign-off 2026-06-07), skarp betygsättning aktiv. Påverkar betyg för **alla 7 kategorier** (partiståndpunkter kurerade + panel-harmoniserade, se 4b/4c). |
| 6 | ✅ v1 | **Frontend byggd** ([web/](web/)): statisk, byggfri; client-side viktning, rankad partilista med osäkerhetsband + CI-överlapp-notis, expanderbart bevisspår (`claim_refs`→evidence.json), URL-delning, svensk formatering, version-0-varning + metod. Rena moduler `web/{format,score}.js` (frontend viktar bara, ingen betygslogik). Tester: `node --test web/tests/` + `tests/test_dist_schema.py` + **Playwright-e2e (8 fall: kort, live-omräkning, bevisspår, ?w=, felkort, fokus/reflow)**. `web/score.js` reproducerar pipelinens ranking exakt. **Task 6.6/6.7 klara:** WCAG 2.2 AA-genomgång ([docs/done/fas6_wcag.md](docs/done/fas6_wcag.md), alla textkontraster ≥4,5:1, blocker fokus-/expanderingsförlust åtgärdad). Återstår (ej blockerande): manuell skärmläsartest. |

## 7. Risker och öppna frågor

- **A som magnitud** kan belöna stora utgifter eller hög aktivitet. A (0,40) är den största *enskilda* delpoängen, men B+D (0,45 tillsammans) väger tyngre och korrigerar magnituden; A rank-normaliseras dessutom för att dämpa extremvärden. A *dominerar* alltså inte, men kan inte heller ensam överröstas av en enskild annan delpoäng.
- **Claims kan gömma subjektivitet** om reglerna är otydliga. Därför måste claim-typer, effektetiketter och tolkningsregler vara konfigurerade, versionsstyrda och testade.
- **Attribution i D** är inneboende brusig (regeringar ärver utfall, koalitioner delar ansvar). Hanteras med tidsförskjutning, attributionsvikt från C och breda osäkerhetsintervall.
- **Försvars operativa förmåga** är till stor del sekretessbelagd → proxy via anslag, personal, materielbeslut. Bör noteras i metoden.
- **Region/kommun-styren historiskt** saknar en enda ren officiell dataset; SKR:s sammanställningar efter varje val är källan. **Nu inlästa (Fas 1c):** alla **21 regioner + 290 kommuner × 3 mandatperioder** ur SKR:s öppna data "Styren i regioner/kommuner 1994-2022" (korsverifierade mot "efter valet 2022" + halvtidsuppföljnings-PDF), i `mappings.yaml:subnational_governance` + `config/subnational_municipalities.yaml` ([metod](docs/done/fas1c_subnational_metod.md)). Subnationell makt blandas in i C per kategori via en **region/kommun-split efter lagstadgat ansvar**; full täckning → C:s säkerhet hög; forsvar nationellt per design (`C_national_only_by_design`). En guard (`C_missing_subnational`, sänkt säkerhet) triggas bara om en datafil saknas. **c2 (finansiering) är uppskjutet** — inget objektivt, riktningsneutralt finansieringsmått går att bygga ur officiell data, så C = c1 (makt); se [metod §c2](docs/done/fas1c_subnational_metod.md).
- **Kategori 7** har svagast datatäckning och lutar mot akademiska enkäter (SOM) → större osäkerhet, vilket modellen redovisar.
- **Indelning S→nuvarande partistruktur** över 12 år: partier byter namn/ledning men de 8 är stabila i fönstret; inga sammanslagningar behöver hanteras.
