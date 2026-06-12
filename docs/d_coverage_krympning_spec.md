# Rösta - Spec: D-täckningskrympning via viktad undermåttsbredd

> **Status: IMPLEMENTERAD 2026-06-12 bakom `coverage_shrink: false` — väntar diff-granskning
> innan flaggan slås på och `dist/` rebaselinas (§10-besluten signade, se §11).**
>
> v2 ersätter den äldre 1/5-bilden för försvar/demokrati. Dagens täckningsläge är bredare
> (verifierat med `python -m pipeline.tools.coverage_report`, 2026-06-12), men kodens principiella
> problem kvarstår: delpoäng **D** renormaliserar över observerade undermått och låter därmed
> saknade delar av en kategori försvinna ur nämnaren. Den här specen gör D mer epistemiskt ärligt
> genom att saknade icke-target-undermått bidrar neutralt i stället för att renormaliseras bort.
>
> Relaterat: [spar_D_datatackning.md](spar_D_datatackning.md), [done/evidens_trovardighet.md](done/evidens_trovardighet.md),
> [../config/scoring.yaml](../config/scoring.yaml), [../pipeline/scorerun.py](../pipeline/scorerun.py),
> [../pipeline/score.py](../pipeline/score.py).
>
> Begreppsmodell: **Kategori -> Undermått -> Indikator -> Riktning**.

---

## 0. Kärnbeslut

D ska fortsatt mäta utfallet i en **kategori**, inte bara utfallet i de undermått där vi råkar ha en
årsserie. Därför ska D inte längre renormalisera bort saknade icke-target-undermått.

**Rekommendation för implementering:**

1. Inför runtime-krympning för D.
2. Använd **viktad undermåttstäckning**, inte antal undermått.
3. Låt täckningen vara **per parti och kategori**, eftersom vissa serier kan sakna attribuerade år för
   ett visst parti.
4. Behandla saknade icke-target-undermått som **neutral net = 0** i D-rollupen.
5. Lägg till `D_thin_coverage` och `D_coverage_<covered_weight>/<total_weight>` i `scores.json`.
6. Lägg till en D-breddgrind/test så framtida tunn D-bredd inte passerar tyst.
7. Lämna B orört i denna iteration.

Det här är bättre än den tidigare v1-formeln `D = 2.5 + (D_raw - 2.5) * antalstäckning`, eftersom
`categories.yaml` redan innehåller vikten för varje undermått. En täckt 35-procentsdel ska inte räknas
som lika stor som en täckt 5-procentsdel.

---

## 1. Problemet i dagens kod

`category_d` i [pipeline/scorerun.py](../pipeline/scorerun.py) gör i dag:

```python
sub_nets = {sub: sum(v) / len(v) for sub, v in by_sub.items()}
cat_net = score.submeasure_weighted_mean(sub_nets, sub_w.get(c, {}))
```

`submeasure_weighted_mean` i [pipeline/score.py](../pipeline/score.py) summerar vikten bara över
**närvarande** undermått. Saknade undermått är varken täljare eller nämnare.

Det är rätt beteende för vissa generiska rolluper, men fel semantik för D som kategoriutfall:

- Om D bara har sett en del av kategorin ska punktskattningen vara mer neutral.
- Om D har sett hela den icke-target-del som kategorin faktiskt betygssätter ska den vara oförändrad.
- `D_thin_basis` räcker inte, eftersom den mäter ansvarsunderlag, inte kategoribredd.

Problemet är alltså inte längre främst att försvar/demokrati är 1/5. Det var ett äldre dataläge.
Problemet är att kodvägen fortfarande gör ett oavkortat kategorianspråk utifrån en delmängd.

---

## 2. Aktuellt täckningsläge

Verifierat 2026-06-12 med `python -m pipeline.tools.coverage_report`:

| Kategori | D-täckta undermått | Icke-target-undermått | Kommentar |
|---|---:|---:|---|
| ekonomi | 4 | 4 | full D-bredd; target-only inflation/offentliga finanser exkluderas |
| valfard | 3 | 4 | finansiering/styrning saknar D |
| trygghet | 4 | 5 | förebyggande saknar D |
| forsvar | 3 | 5 | militär förmåga, civil beredskap, Nato/Ukraina täckta |
| klimat | 4 | 5 | industriell konkurrenskraft saknar indikator/D |
| integration | 5 | 5 | full D-bredd |
| demokrati | 5 | 5 | full D-bredd |

Viktig korrigering från v1: **demokrati ska inte krympas på bredd i nuvarande dataläge** om alla fem
icke-target-undermått har D-attribuerbar serie. Försvar ska krympas, men måttligt, inte som 1/5.

---

## 3. Formell modell

### 3.1 Denominator: viktade icke-target-undermått

För en kategori `c`, definiera `D_den(c)` som alla undermått i `categories.yaml` som inte är target-only.

Ett undermått är **target-only** endast om:

- undermåttet har minst en indikator, och
- alla indikatorer i undermåttet har `direction: target`.

Konsekvenser:

- Ekonomins `inflation_prisstabilitet` och `offentliga_finanser` exkluderas från D-denominatorn.
- Ett undermått utan indikatorer är **inte** target-only per automatik. Det ingår i denominatorn om det
  är en del av kategorianspråket. Detta fångar t.ex. klimatets `industriell_konkurrenskraft`.
- Target-indikatorer i ett annars icke-target-undermått ger inte D-serier, men undermåttet kan ändå
  täckas av en systerindikator med `up`/`down`.

### 3.2 Numerator: faktiskt attribuerade undermått per parti och kategori

För varje `(parti p, kategori c)` räknas ett undermått som D-täckt om `category_d` faktiskt fick minst
en attribuerbar D-serie i det undermåttet för partiet. Praktiskt är detta `by_sub.keys()` efter att
`score.attribute_series(...)` har returnerat `net is not None`.

Det gör täckningen parti/kategori-specifik. Det är mer korrekt än kategori-global täckning eftersom
korta serier, glapp och `min_responsibility` kan göra att ett parti saknar verkligt underlag i en serie
som andra partier kan attribueras.

### 3.3 Rollup med neutral för saknad bredd

Låt:

- `w_s` = undermåttets vikt i `categories.yaml`
- `net_s` = medelnet för D-serier i undermåttet, i `[-1, 1]`
- saknat `net_s` = `0.0` (neutral)
- `S_den` = alla icke-target-undermått i kategorin
- `S_obs(p,c)` = undermått med faktiskt D-underlag för partiet i kategorin

Ny D-rollup:

```text
cat_net_just(p,c) =
    sum(w_s * net_s for s in S_obs(p,c)) / sum(w_s for s in S_den)
```

Det är ekvivalent med:

```text
D_raw_present = renormaliserat D över observerade undermått, dagens beteende
weighted_d_cov = sum(w_s for s in S_obs) / sum(w_s for s in S_den)
D_just = 2.5 + (D_raw_present - 2.5) * weighted_d_cov
```

Men implementeringen bör helst beräkna `cat_net_just` direkt, eftersom den gör neutral-pseudoobservationen
explicit och undviker avrundnings-/renormaliseringsförvirring.

### 3.4 Gate och NA

`min_responsibility` ska vara oförändrad:

- Om `cat_net_present is None` eller `basis < min_responsibility`: D är `not_applicable`, score `2.5`,
  flagga `D_not_applicable`, confidence `low`.
- Om D är measured: använd `cat_net_just` för komponentvärdet.

`D_thin_basis` fortsätter mäta ansvarsunderlag. `D_thin_coverage` mäter bredd. De är ortogonala.

---

## 4. Confidence och flaggor

Nya konfigvärden i `config/scoring.yaml` under `D_resultat`:

```yaml
coverage_shrink: true
coverage_denominator: non_target_submeasure_weight
thin_coverage_threshold: 0.75
```

Rekommenderad confidence-logik:

- measured D börjar på `measured_confidence` (`medium` i dag).
- Om `basis < thin_basis_threshold`: sänk ett steg och flagga `D_thin_basis`.
- Om `weighted_d_cov < thin_coverage_threshold`: sänk ett steg och flagga `D_thin_coverage`.
- Steg sänks kumulativt men klampas till `low`.

Med `thin_coverage_threshold: 0.75` kommer måttligt ofullständig D-bredd att synas. Med `0.5` skulle
nästan allt aktuellt dataläge passera utan coverage-flagga, vilket gör flaggan mindre användbar.

Flaggor i `scores.json`:

- `D_coverage_<covered_weight>/<total_weight>` där vikterna är heltal från `categories.yaml`.
- `D_thin_coverage` om viktad täckning understiger tröskeln.
- `D_thin_basis` oförändrad.
- `D_not_applicable` oförändrad.

Exempel:

```text
D_coverage_70/100
D_thin_coverage
```

för försvar om täckta undermått är `militar_formaga` 35, `civil_beredskap` 20 och `nato_ukraina` 15.

---

## 5. Förväntad effekt med v2

Eftersom D väger 10 procent av kategoribetyget blir totalpåverkan begränsad. Det här ändrar främst
översäkerheten i D-komponenten.

Förväntad per-kategori-bild:

| Kategori | Viktad D-täckning, ungefär | Effekt |
|---|---:|---|
| ekonomi | 1.00 | oförändrad |
| integration | 1.00 | oförändrad |
| demokrati | 1.00 | oförändrad |
| klimat | ca 0.85 | liten krympning, ingen thin om tröskel 0.75 |
| trygghet | ca 0.85 | liten krympning, ingen thin om tröskel 0.75 |
| valfard | ca 0.80 | liten/måttlig krympning, ingen thin om tröskel 0.75 |
| forsvar | ca 0.70 | måttlig krympning + `D_thin_coverage` vid tröskel 0.75 |

Exempel försvar:

- Dagens täckta försvarsundermått: `militar_formaga` 35, `civil_beredskap` 20, `nato_ukraina` 15.
- Denominator: 100, eftersom `ekonomisk_ambition` inte är target-only (har även en `up`-indikator) och
  `genomforbarhet_leverans` är ett icke-target-undermått.
- Viktad täckning: `70/100 = 0.70`.
- Ett försvars-D på `4.03` krymper ungefär till `2.5 + (4.03 - 2.5) * 0.70 = 3.57`.

Det är en helt annan och rimligare effekt än v1:s gamla 1/5-exempel.

---

## 6. Teknisk design

### 6.1 `pipeline/score.py`

Lägg till rena hjälpfunktioner:

```python
def coverage_shrink(raw: float, coverage: float, neutral: float = 2.5) -> float:
    return neutral + (raw - neutral) * coverage
```

och helst även en net-baserad helper:

```python
def weighted_mean_with_neutral_missing(
    values: Mapping[str, float],
    weights: Mapping[str, float],
    denominator_keys: Iterable[str],
    neutral: float = 0.0,
) -> float | None:
    ...
```

Den senare bör:

- summera över `denominator_keys`
- använda `neutral` för saknade keys
- returnera `None` om denominatorn saknar total vikt
- inte ändra `submeasure_weighted_mean`, eftersom den används för annan renormaliserande semantik.

### 6.2 `pipeline/scorerun.py`

Lägg till helpers:

- `_submeasure_indicator_directions()`: kategori -> undermått -> lista riktningar
- `_d_denominator_submeasures()`: kategori -> list/set icke-target-undermått
- eventuellt `_weighted_coverage(covered, denominator, weights)`

Uppdatera `category_d` att returnera mer data:

```python
(score, measured, thin_basis, coverage, covered_weight, total_weight, thin_coverage)
```

eller en liten dataclass om repo-stilen tillåter. Om tuple används, dokumentera ordningen tydligt.

Rollup:

1. Bygg `by_sub` som i dag.
2. Bygg `sub_nets` som i dag för observerade undermått.
3. Beräkna `cat_net_present` med dagens `submeasure_weighted_mean` bara för measured-gate.
4. Om measured: beräkna `cat_net_just` över D-denominator med saknade undermått som neutral net `0`.
5. Konvertera `cat_net_just` till score med `net_support_to_score`.

Varför behålla `cat_net_present` för gaten? För att `None` fortsatt betyder "ingen observerad D alls";
saknade undermått ska inte göra en helt tom kategori measured.

### 6.3 `coverage_report`

Utöka rapporten med D-bredd per kategori:

```text
== D-undermåttsbredd ==
  ekonomi       73/73   1.00
  valfard       80/100  0.80
  trygghet      85/100  0.85
  forsvar       70/100  0.70  THIN om threshold=0.75
  klimat        85/100  0.85
  integration  100/100  1.00
  demokrati    100/100  1.00
```

Observera att ekonomi blir `73/73` (inte `100/100`): nämnaren är heltalsvikterna ur
`categories.yaml` och ekonomins icke-target-vikter summerar till 73 (22+18+18+15) eftersom
target-only-undermåtten (12+15) lyfts ur nämnaren. Kvoten är ändå 1.00.

Denna rapport kan vara kategori-global, eftersom den är en översikt. Själva scoringens numerator ska
fortfarande vara per parti/kategori.

---

## 7. Tester och acceptanskriterier

- `coverage_shrink(raw, cov)` testas för `cov=1`, `cov=0`, monotoni och symmetri runt 2.5.
- Ny helper för neutral-missing-rollup testas med viktade undermått.
- Target-only-undermått exkluderas från D-denominator.
- Undermått utan indikatorer blir inte felaktigt target-only.
- `coverage_shrink: false` ger byte-identiskt `dist/scores.json` mot före ändringen.
- `weighted_d_cov=1` ger oförändrad D.
- D-krympning bevarar partiordning inom en kategori när alla partier har samma coverage.
- Parti/kategori-specifik coverage kan skilja sig när attribution saknas i korta serier.
- `D_thin_basis` och `D_thin_coverage` kan trigga oberoende.
- `scores.json` innehåller `D_coverage_<covered>/<total>` för measured D.
- `D_not_applicable`-celler förblir neutral 2.5 och får inte `D_coverage_*`.
- `coverage_report` visar D-bredd per kategori.
- `pytest -q` grönt.
- `python -m pipeline.scorerun` körs och ranking-/score-diff redovisas innan `dist/` rebaselinas.

---

## 8. B ska inte ändras nu

B har redan:

- runtime-krympning mot neutral efter partiets kodade åtgärdstypstäckning
- `B_thin_coverage`
- `b_submeasure_spread`-grind mot nära-binär kategoribredd

Det finns ett verkligt parallellt B-breddsproblem, men en extra B-undermåttskrympning riskerar
dubbelrabatt och bör specas separat efter att D-ändringen är mätt. Denna spec gäller endast D.

---

## 9. Implementeringsordning

1. Lägg in config-nycklar med `coverage_shrink: false` som första commit/patch om en golden-baseline behövs.
2. Lägg till rena helpers och tester i `score.py`.
3. Lägg till D-denominator-helpers i `scorerun.py`.
4. Ändra `category_d` och huvudloopen så flags/confidence följer med.
5. Utöka `coverage_report`.
6. Kör testsvit.
7. Kör scorerun och redovisa score-diff/ranking-diff.
8. Efter sign-off: slå på `coverage_shrink: true` och rebaselina `dist/`.

---

## 10. Sign-off-frågor — AVGJORDA 2026-06-12

1. `thin_coverage_threshold` = **0.75** (rekommendationen). Följdfråga besvarad: när ett nytt
   D-mått byggs för t.ex. försvar bumpas täckningen **automatiskt** vid nästa scorerun —
   numeratorn beräknas i runtime ur attribuerade serier och nämnaren ur `categories.yaml`,
   ingen kodändring krävs. (En ny serie i ett redan täckt undermått ändrar dock inte bredden;
   det är undermåttsbredd som mäts, inte antal indikatorer.)
2. **Bara heltalsflagga** `D_coverage_<covered>/<total>` + kvot i rapporten (rekommendationen).
3. **Börja `false`** för byte-identisk baseline; slå på + rebaselina efter diff-granskning
   (rekommendationen).
4. **Ja** — försvar krymps måttligt (`70/100`) enligt kategorins egna vikter (rekommendationen).
   Accepterat i `coverage_allowlist.d_thin_breadth_accepted` (grind: tests/test_d_breadth_gate.py).

---

## 11. Codex-granskningslogg

- 2026-06-12: v2 omarbetad efter Codex-granskning. Huvudändringar: rebasat mot aktuell D-täckning,
  ersatt antalbaserad krympning med viktad icke-target-undermåttsrollup, gjort numerator per
  parti/kategori, behållit B utanför scope.
- 2026-06-12: spec verifierad av Claude mot kod/config (alla §2/§5-anspråk reproducerade;
  §3.3-ekvivalensen bekräftad linjär; §6.3-exemplet rättat till `73/73` för ekonomi) och
  IMPLEMENTERAD enligt §9 steg 1-7 med `coverage_shrink: false`. Tillägg utöver spec:
  D-breddgrind som allowlist-mönster (`coverage_allowlist.d_thin_breadth_accepted`, spegel av
  B4-grinden) med offline-mätare `coverage_report.d_submeasure_breadth`. Verifierat:
  `pytest -q` grönt, `dist/` byte-identiskt med flaggan av, score-/rankingdiff med flaggan på
  redovisad (81 ändringar, ingen rankingändring, totaler -0.008..-0.017). Steg 8 (slå på +
  rebaselina) väntar diff-granskning.
