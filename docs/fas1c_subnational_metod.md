# Fas 1c — Subnationell styresdata (regioner + kommuner) → delpoäng C

> **Status: ✅ C komplett vad gäller makt (c1): nationell + regional + kommunal.**
> Fyller den största strukturella luckan i C: tidigare var C en **platt per-parti-konstant**
> identisk över alla 7 kategorier (enbart nationell regeringsmakt). Nu blandas nationell makt
> med **subnationell makt** (alla 21 regioner + 290 kommuner × 3 mandatperioder) via en
> per-kategori region/kommun-split, så C bär en kategorisignal och vilar på full officiell
> täckning. **c2 (finansiering) är uppskjutet** — se §c2. Metodval i samråd med Codex.

## 1. Vad som byggts

| Del | Innehåll |
|-----|----------|
| **Regiondata** | 21 regioner × 3 mandatperioder, `config/mappings.yaml:subnational_governance`. |
| **Kommundata** | 290 kommuner × 3 mandatperioder, `config/subnational_municipalities.yaml`. |
| **Adapter** | `pipeline/sources/skr.py`: `build_regional_responsibility()` + `build_municipal_responsibility()` → `responsibility` (level=regional/municipal), idempotent i warehouse via `build_fas1.py`. |
| **Scoring** | `pipeline/scorerun.py`: `regional_fractions()` + `municipal_fractions()` + `category_c()` — per-kategori region/kommun-split, blandning med nationell makt, rank-normaliserad. |
| **Provenance** | `pipeline/claims.py` — aggregerad ansvars-claim per (parti, nivå, period) i `evidence.json` (spårbar till SKR). |
| **Transkribering** | `pipeline/tools/skr_regions_transcribe.py` + `pipeline/tools/skr_municipalities_transcribe.py` (engångsverktyg, ej runtime). |

## 2. Källor (endast officiella)

- **Regioner:** SKR, *"Styren i regioner 1994-2022"*, öppna data,
  [catalog.skl.se dataset 80](https://catalog.skl.se/catalog/1/datasets/80) (CSV `resource/123`).
  Korsverifierad mot *"Styren i regioner efter valet 2022"* (xlsx) — **exakt match för alla 21**;
  kontrollsummorna matchar SKR:s *halvtidsuppföljning 2024-11-30* (PDF) "efter valet"-tal exakt.
- **Kommuner:** SKR, *"Styren i kommuner 1994-2022"*, öppna data (CSV `resource/127`). 2022-talen
  ligger inom **±2** av halvtidsuppföljnings-PDF:ns "efter valet"-tal (M=175, C=149, V=58 exakt;
  S/KD/L −1, MP +1, SD +2 — ögonblicksvariation mellan två SKR-produkter; den per-kommun-granulära
  CSV:n är den auktoritativa källan). Hämtade 2026-05-31.

Rådatafilerna stannar lokalt i `data/raw/skr/` (gitignorad). Config (mappings.yaml + subnational_
municipalities.yaml) är källan till sanning; **ingen runtime-parser** (samma princip som Fas 1b).
Kommunfilen (290 poster) genereras maskinellt ur den officiella CSV:n — felfritt och fullt
reproducerbart; golden-tally i `tests/test_source_skr.py` pinnar datan mot SKR.

## 3. Transkriberingsregler

- **leading_parties** = de av de 8 riksdagspartierna (S, M, SD, C, V, KD, L, MP) som ingår i
  styret. SKR:s historiska kod `L/FP` → `L` (samma som `party_code_map` fp→L).
- **Lokala partier** (ÖP/"Övrigt parti") noteras (regioner) eller utelämnas (kommuner) men
  **poängsätts aldrig** — modellen bedömer bara de 8 partierna; de räknas inte i koalitionsnämnaren.
- **Post-val-styre per mandatperiod.** Mandatperiod-skiften mitt i perioden modelleras inte
  (SKR:s primära sammanställning är post-val; jfr nationella `government_periods`).
- **geography** = SCB:s region-/kommunkod (regioner 2-siffrig läns-kod `01`…`25`; kommuner
  4-siffrig kod, Kolada-format). Spårbarhet; inga subnationella observationer joinas ännu.

## 4. Hur makt blir delpoäng C (c1)

`scoring.yaml:C_ansvar.level_weights` viktar **nationell** vs **regional_municipal** makt per
kategori: välfard `{0.4, 0.6}`, trygghet `{0.8, 0.2}`, forsvar `{1.0, 0.0}`, default `{0.7, 0.3}`.

1. `national_frac[p]` = andel av fönstret 2014–2026 i nationell regering (stöd vägs 0.5).
2. `regional_frac[p]` / `municipal_frac[p]` = medel över alla (geografi × mandatperiod)-celler av
   partiets styresandel, där makten i en cell delas **jämnt** mellan de ledande riksdagspartierna
   (1/antal). Alla fraktioner i [0,1] ("andel av tillgänglig makt").
3. **Per-kategori region/kommun-split** (`scoring.yaml:subnational_split`) av den kombinerade
   `regional_municipal`-bucketen, satt efter **lagstadgad ansvarsfördelning** (vem som driver
   verksamheten), inte ideologi:

   | Kategori | region | kommun | Motiv |
   |----------|:------:|:------:|-------|
   | valfard | 0.45 | 0.55 | region=hälso/sjukvård; kommun=skola, äldreomsorg, IFO |
   | trygghet | 0.0 | 1.0 | regioner saknar lagstadgat trygghetsansvar (polis=nat, brottsförebyggande/socialtjänst=kommun) |
   | integration | 0.0 | 1.0 | mottagande/SFI/ekonomiskt bistånd = kommunalt |
   | klimat | 0.4 | 0.6 | region=kollektivtrafik; kommun=fysisk planering/energi/avfall |
   | ekonomi, demokrati | 0.30 | 0.70 | default (region: regional utveckling/kultur; kommun: mark/näringsliv/lokal demokrati) |
   | forsvar | – | – | `regional_municipal`-vikt 0 → nationellt per design |

   `subnat_frac[p] = region·regional_frac[p] + kommun·municipal_frac[p]`.
4. `blended[p] = w_nat·national_frac[p] + w_reg·subnat_frac[p]`, sedan **rank-normaliseras en gång**
   över de 8 partierna → c1. **C = c1** (c2 uppskjutet, ingen 0.7-multiplikation).

**Säkerhet:** subnationell makt har nu **full täckning** (båda nivåerna) → C:s default-säkerhet
**hög** för alla kategorier (den tidigare sänkningen för saknad subnational utgår). forsvar = hög
(nationellt per design, flagga `C_national_only_by_design`). En guard (`C_missing_subnational`,
sänkt säkerhet) triggas bara om en datafil mot förmodan saknas.

## 5. Metodval (Codex-granskat)

Den **regionala** halvan granskades oberoende av Codex, som rekommenderade (och vi följde):
blanda råa fraktioner och rank-normalisera en gång (A); jämn termvikt för subnationella perioder
(B, mandatperioderna är jämnstora); och — i regioner-only-läget — aktivera regiondata bara där
regionen var dominerande aktör. När **kommundata** tillkom blev den sista punkten överflödig:
hela `regional_municipal`-bucketen täcks nu och delas per kategori efter statutärt ansvar (§4).
En andra Codex-körning för region+kommun-kombinationen avbröts av en pollnings-bugg innan
slutomdömet skrevs; designen vilar därför på den första granskningen + den dokumenterade
statutära ansvarsfördelningen.

**Resultat:** C bär nu en kategorisignal — trygghet (kommun-only subnational + hög nationell vikt)
och forsvar (rent nationellt) skiljer sig från övriga, och hela C vilar på officiell styresdata
med hög säkerhet. Att flera kategorier ändå rank-normaliserar lika beror på att samma partier
tenderar att styra på alla nivåer (region- och kommunmakt är starkt korrelerade) — en sann
egenskap hos svensk politik, inte ett fel. Rank-normalisering (ej min–max) behålls per
`scoring.yaml` (8 datapunkter, outlier-robust).

## c2 — Finansiering: UPPSKJUTET (beslut Fas 1c)

Modellen avser C = `0.7·c1_makt + 0.3·c2_finansiering`. **c2 byggs inte** — C = c1. Skäl:

- **Likformigt:** alla 8 partiers budgetmotioner är formellt fullt finansierade (rambesluts-
  modellen + budgetlagen kräver komplett, balanserad ram) → ett "är budgeten finansierad?"-mått
  ger alla samma betyg = ingen signal.
- **Subjektivt eller riktningsladdat:** det som faktiskt skiljer (realismen i antagandena) saknar
  en ren officiell per-parti-källa; och ett saldo-/ramverksavviknings-mått skulle systematiskt
  gynna en finanspolitisk riktning (åtstramning) → bryter mot modellens riktningsneutralitet
  (CLAUDE.md: bedöm efter indikatoreffekt, inte ideologisk metodpreferens).
- **Omformuleringar prövade:** "driver de politiken de lovar?" (budget vs partiprogram; budget vs
  motionsfokus a1↔a2; röstning vs program) — alla kräver antingen subjektiv programtolkning, eller
  återanvänder signaler som redan finns i A (prioritering), B (källbelagda ståndpunkter ur
  voteringar/motioner) och D (resultat under makt). En statsbudget är dessutom till ~90 %
  strukturellt låst, så "matchar budget rhetoriken" blir en grumlig signal.
- **Inte en lucka:** "löftesuppfyllelse" fångas redan **distribuerat** av A + B + D. c2 skulle mest
  skiva om samma objektiva signaler eller kräva subjektivitet.

Komponentvikterna (0.7/0.3) behålls i `scoring.yaml` som dokumenterad avsikt om en neutral,
objektiv, oberoende finansieringskälla skulle uppstå. Tills dess: **C = c1, redovisat ärligt.**

## 6. Verifiering

```powershell
# Återskapa config ur officiella CSV:er (kräver lokala data/raw/skr/-filer):
python -m pipeline.tools.skr_regions_transcribe        # regioner -> klistras in i mappings.yaml
python -m pipeline.tools.skr_municipalities_transcribe # kommuner -> skriver subnational_municipalities.yaml

# Tester (golden-tally pinnar region- och kommundata mot SKR; C-wiring + schema):
python -m pytest tests/test_source_skr.py -q
python -m pytest -m "not network" -q                   # hela sviten

# Bygg subnationell responsibility + regenerera deploy-artefakten:
python -m pipeline.build_fas1     # national + regional + municipal responsibility -> warehouse
python -m pipeline.scorerun       # -> dist/scores.json + dist/evidence.json
```

## 7. Kvar (loggat)

- **c2 finansiering** — uppskjutet (se §c2). C = c1 tills en neutral objektiv källa finns.
- **Mandatperiod-skiften mitt i perioden** modelleras ej (post-val-styre per term).
- **Subnationella observationer** (regional/kommunal D-resultatdata) ej inlästa — geography-fältet
  ligger redo (SCB/Kolada-koder) för en framtida regional/kommunal D-attribution.
