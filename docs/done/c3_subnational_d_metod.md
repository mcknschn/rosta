# C3 — Subnationell D (region-nivå vårdutfall) — metod & sign-off

> ✅ **LEVERERAD OCH AKTIVERAD 2026-06-14.** Kopplar subnationell makt till subnationellt utfall i
> delpoäng D: ett regionalt vårdutfall attribueras till det parti som styrde DEN regionen det året,
> parallellt med den nationella attributionen. Gated på `scoring.D_resultat.subnational.enabled`
> (true). `enabled:false` -> byte-identisk med ren nationell D (legacy-garanti, testtvingad).

## 1. Problemet C3 löser

D mätte tidigare bara **nationella** årsserier och attribuerade förändringar till **nationell**
regering. Men C (ansvar) blandar redan in subnationell makt per kategori via `level_weights`
(välfärd national 0.4 / regional_municipal 0.6) — regionerna är lagstadgade sjukvårdshuvudmän.
D var alltså asymmetriskt: ett parti som aldrig satt i regeringen men styr regioner (t.ex. V) fick
`D_not_applicable` för välfärd trots faktiskt vårdansvar. C3 gör D symmetriskt med C: subnationellt
utfall attribueras till subnationell makt.

## 2. Scope v0 (medvetet smalt, arkitekturen generell)

**Region-nivå välfärd, submåttet `vard_tillganglighet`.** Två kanoniska indikatorer som redan finns
nationellt, nu även per region (Kolada, live-verifierat 2026-06-14):

| Indikator | KPI | Riktning | Region-serie |
|-----------|-----|----------|--------------|
| `overlevnad_svar_sjukdom` (30-dagarsöverlevnad akut tjocktarmscancerkir.) | U70471 | up | 2010–2025, 21/21 regioner |
| `vardkoer` (väntetider, median) | N79242 | down | 2021–2025, 21/21 regioner |

Varför just detta: regionen är **sjukvårdshuvudman** → vård är den enda submåttsnivå där en region-
attribution är en ren, **neutral** ansvarskoppling (kortare köer / högre överlevnad är icke-
ideologiska mål). Kommunstyrda utfall (skolresultat, ekonomiskt bistånd) skjuts till en framtida våg
(290 enheter, demografiskt confounderade → brusigare; se §7). 6 av 7 kategorier är byte-identiska;
endast välfärds-D rör sig.

## 3. Maskineri

- **Data:** `pipeline/build_subnational.py` hämtar region-serierna (config-regionnyckel `01` →
  Kolada 4-siffrig `0001`) till `observations` med `geography` = regionkod (samexisterar med de
  nationella `Riket`/`0000`-raderna; lästs separat). Region-observationer blir **inte** egna
  `observed_result`-claims i det deployade evidensindexet (skulle bli oskiljbara dubbletter och
  svälla indexet) — de är intern scoring-input; per-region-värdena ligger i den lokala warehouse:n
  (deploy-split, DATA.md §1). Regionspåret syns i stället via flaggan `D_subnational_region_<basis>`.
- **Region-år-makt** (`scorerun.region_year_power_fractions`): `{regionkod → {år → {parti → maktvikt}}}`.
  Mandatperioderna (`subnational_governance.terms`, tillträde 15 okt valåret) **dagviktas** per
  kalenderår precis som den nationella `year_power_fractions`; inom ett styre delas makten **jämnt**
  mellan de ledande riksdagspartierna (1/antal, jfr `regional_fractions`/`skr.py`). Inget stödparti-
  begrepp subnationellt. Lokala partier räknas aldrig.
- **Attribution** (`score.attribute_subnational_indicator`): som den nationella men poolat över
  regioner med **lika per-region-vikt** (ej befolkningsviktat — neutralt; se §6). Varje regions
  konsekutiva årsförändring tar bara sitt **tecken** (förbättring +1 / försämring −1 / oförändrat 0
  i dödzon) och tillskrivs det parti som styrde regionen år (y − lag). Tecken-bara håller måttet
  robust mot magnitud/konjunktur (IDEA.md-brasklappen), precis som nationellt.
- **Blandning** (submåttsnivå, `scorerun.category_d`): för submått i
  `subnational.submeasure_level_weights` blandas det nationella submåtts-nätet med det region-poolade
  enligt `{national, region}`-vikten och renormaliseras över närvarande sidor. För `vard_tillganglighet`
  är vikten **{national 0.4, region 0.6}** — hela `regional_municipal`-vikten (0.6) går till region
  eftersom vård ÄR regionstyrd; vi återanvänder medvetet **inte** C:s `subnational_split` (region 0.45),
  som är ett kategorisnitt med kommunstyrd skola/omsorg inblandad. Övriga välfärdssubmått förblir
  nationella.

## 4. Grindar (rättvisa + soundness)

- **År-ekvivalent ansvarsunderlag:** rått regionalt underlag (Σ maktvikt över region-år) normaliseras
  till `region_basis = Σ power / antal regioner med serie`, så det ligger på **samma skala som det
  nationella** (år-ekvivalenter av full makt). Annars hade 21 regioner × år sprängt
  `min_responsibility`/`thin_basis_threshold`.
- **Kombinerad measured-grind:** `combined_basis = nationellt + regionalt (år-ekv.)`. Ett parti med
  ENBART regional vård-makt blir därmed measured för välfärd (rättvisefixen — V, se §5).
- **Soundness-grind (`region_basis ≥ min_responsibility = 0.15`):** den regionala signalen blandas in
  ENDAST om det regionala ansvaret är meningsfullt. Annars dominerar ett brusigt teckenmedel ur ett
  pyttigt region-år-urval submåttet via 0.6-vikten. **Detta var nödvändigt** — auditen (§6) visade att
  SD (region_basis 0.02, styr nästan inga regioner) annars svängde sin välfärds-D −0.58 på ~1–2
  region-år. Med grinden judge­ras SD bara nationellt (0.02 < 0.15) → välfärds-D oförändrad.
- **Tunt underlag:** `combined_basis < thin_basis_threshold (1.0)` → `D_thin_basis` + säkerhet sänks.
  Detta fångar de instabila nära-noll-fallen (V 0.58, KD 0.74; se §6).

## 5. Faktisk effekt (mot baslinjen, score_diff 2026-06-14)

Endast välfärd rör sig; **totalrankingen oförändrad** (S > L > M > MP > KD > C > SD > V):

```
välfärds-D (komponent), nationell-only -> blandad:
  S  2.555 -> 2.558   M  3.065 -> 2.872   C 2.999 -> 2.833   KD 3.065 -> 2.838
  L  2.975 -> 2.775   MP 2.843 -> 2.570   V 2.500 -> 2.451   SD 3.065 -> 3.065 (gated)
```

- **Rättvisa:** V/välfärd `D_not_applicable` → **measured** (region_basis 0.58, flaggat
  `D_thin_basis`/`D_thin_coverage`, låg säkerhet). V styr regioner → får nu vårdansvar.
- **Soundness:** SD oförändrad (gated bort, styr ~inga regioner → attribueras inte regionalt).
- Regerings-/regionstyrande partier (M/KD/C/L/MP) sjunker något — regionala vårdköer steg 2021–2025
  (ärlig negativ signal), 0.6-viktat in i vård-submåttet.

## 6. Neutralitetsaudit (Codex-krav före sign-off) — `pipeline/tools/c3_sensitivity.py`

Region-attribution riskerar att bli en förtäckt geografi-/blockproxy. Tecken-bara dämpar magnitud
men inte regionalt urval/demografi/finansiering. Auditen kör vård-signalen under flera varianter:

- **Lika vs befolkningsviktat (Kolada N01951):** **extremerna robusta** (S bäst, SD sämst i båda),
  men mitten (M/C/L/KD/MP) kastas om — de har små net (0.05–0.13). Lika viktning är det principiella,
  neutrala valet (matchar `regional_fractions`; befolkningsvikt skulle luta mot storstadsstyre).
- **Per indikator:** köer och överlevnad ger olika ordningar (de mäter olika vårddimensioner; S
  robust positiv, SD robust negativ i båda) — den kombinerade signalen medlar, vilket är ärligt.
- **Leave-one-region-out:** S/M/C/L/MP/SD tecken­stabila; **V och KD teckenflippar** (net nära noll).
  Dessa fångas redan av `D_thin_basis` (basis < 1.0) → säkerhet nedgraderad.

**Verdikt:** instabiliteten är begränsad till (a) små mittenmagnituder och (b) nära-noll-partier som
redan flaggas thin/låg säkerhet. SD-bruset är gated bort. Totalrankingen är oförändrad. Detta möter
"ship with confidence downgrade"-tröskeln (ej "keep behind a flag"). C3 levereras **aktiverad** med
ärlig säkerhetsflaggning. Trivialt reversibelt via `subnational.enabled: false`.

## 7. Caveats & utvidgningsväg (v0)

- **Confounders:** sign-only neutraliserar inte demografi/case-mix/finansiering/baslinjetrend mellan
  regioner. Mildras av tecken-bara + lika viktning + makt-/ansvarsviktning + 10 %-D-vikt.
- **Mid-term-skiften:** SKR-datan är post-val; styrbyten mitt i mandatperiod modelleras ej (jfr C2).
- **Korta serier:** `vardkoer` 2021–2025 (5 år) → få förändringar; `overlevnad` 2010–2025 bär tyngden.
- **Utvidgning:** arkitekturen är generell. Nästa våg = kommun-nivå (skola → `skola_kunskap`,
  ekonomiskt bistånd → integration) med samma maskineri men egna neutralitets-/confounder-prövningar,
  samt fler region-submått om rena serier finns. Lägg då till i `submeasure_level_weights` + en
  kommun-variant av region-år-makten.

## 8. Filer

- Config: `config/scoring.yaml` (`D_resultat.subnational`), validering `pipeline/config.py`.
- Data: `pipeline/build_subnational.py` (region-serier), inkopplad i `pipeline/build_all.py`.
- Math: `pipeline/score.py:attribute_subnational_indicator`.
- Scoring: `pipeline/scorerun.py` (`region_year_power_fractions`, `_subnational_annual_series`,
  `category_d`-blandning + grindar).
- Claims: `pipeline/claims.py` (observed_result scopas till nationell geografi).
- Audit: `pipeline/tools/c3_sensitivity.py`. Tester: `tests/test_c3_subnational_d.py`.
