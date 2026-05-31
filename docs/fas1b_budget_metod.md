# Fas 1b — a1 budgetprioritering (delpoäng A)

Metod för **a1**, budgetdelen av delpoäng A (faktiskt agerande). A väger 0,40 — den tyngsta
delpoängen — och `A = 0,6·a1 + 0,4·a2` (vikter i [`config/scoring.yaml`](../config/scoring.yaml)
`A_agerande.components`). a2 (motionsprioritering) byggdes i Fas 1; a1 var **medvetet uppskjuten**
tills den kunde byggas utan att en bräcklig parser korrumperar A. Detta dokument beskriver hur a1
nu byggts robust och gated.

## Vad a1 mäter

`a1(parti, kategori)` = **andelen av partiets föreslagna anslag som går till kategorins
utgiftsområden (UO)**, rang-normaliserad över de 8 partierna. Det är ett *relativt
prioriteringsmått* (som a2), inte ett mått på om mer pengar är rätt — rättheten fångas av B och D.

```
andel(parti, kat) = Σ_UO ( ram(parti, UO) · UO→kat-vikt ) / Σ_UO ram(parti, UO)
a1(kat) = rank_normalize_över_8_partier( andel(·, kat) )
```

UO→kategori-vikterna ligger i [`config/mappings.yaml`](../config/mappings.yaml) `expenditure_areas`
(ett UO kan delas mellan flera kategorier). Nämnaren är partiets **totala** föreslagna ram (Σ alla
27 UO), så måttet är storleksoberoende: ett stort parti blir inte högt i varje kategori.

## Varför ingen runtime-parser (och varför detta inte är fabrikation)

Empirisk kontroll 2026-05-30 mot data.riksdagen.se: **det finns ingen strukturerad API-väg till
partiernas anslag per UO.** `/dokument/{id}.json` och `dokutskottsforslag`/förslagspunkts-endpointen
exponerar beslutsstruktur men **inget ram-/belopp-fält** (inga av `ram/anslag/belopp/kronor/miljard`
förekommer). Beloppen finns bara i dokumentens fulltext (FiU1-betänkandets tabeller + budgetmotioner).
En runtime-HTML-parser av en 2 MB-fil med 60 tabeller vore exakt den bräckliga parser projektet
medvetet undvek för A.

Lösningen följer projektets etablerade mönster (`party_positions.yaml`, `subnational_governance`):
de officiella, publicerade ramtalen **transkriberas till versionsstyrd config**
([`config/budget_ramar.yaml`](../config/budget_ramar.yaml)), där varje frame **citerar sin källrad**,
och deterministisk kod ([`pipeline/budget.py`](../pipeline/budget.py)) konsumerar configen. Detta är
en **trogen kopia** av officiella tal — inga belopp imputeras, jämkas eller gissas. Det är
strukturering av en officiell källa, inte fabrikation. **Version 0 — kräver mänsklig slutgranskning.**

## Källa (budgetår 2025)

Allt kommer ur **bet. 2024/25:FiU1 "Statens budget 2025 – Rambeslutet"** (dok_id HC01FiU1),
tabell 35 "Utgiftsram per utgiftsområde": kolumnen *Regeringens förslag* (absolut, mnkr) plus
*Avvikelse från regeringen* för S, V, C, MP. Varje oppositionspartis absoluta ram =
`Regeringens förslag + partiets avvikelse` (mekanisk normalisering ur samma tabell).

### Attribution (Codex P0-risk)
Ett parti tilldelas regeringens ram endast när en officiell källa stödjer det:
- **M, KD, L** = regeringspartier (prop. 2024/25:1) → regeringens ram.
- **SD** = Tidö-stödparti som **röstade Ja till rambeslutet** (votering bet. 2024/25:FiU1 punkt 2;
  per-ledamot-tally: M/SD/KD/L = Ja) → regeringens ram, citerat till voteringen.
- **S, V, C, MP** = egen budgetmotion 2024/25 → egen ram (avvikelse i tabell 35).

Ett parti utan egen ram **och** utan citerbar uppslutning bakom en gemensam ram skulle utelämnas —
aldrig gissas. För 2025 är alla 8 partier täckta.

### Verifiering (ingen fabrikation)
- **Intern invariant:** för varje parti är `Σ(partiets ram) − Σ(regeringens ram)` lika med källans
  egna avvikelse-totaler i raden "Summa utgiftsområden" (S +30 886, V +132 499, C +2 821,
  MP +147 384 mnkr) — matchar på kronan.
- **Oberoende adversariell re-extraktion** (separat agent, lokaliserade tabellen via innehåll,
  re-deriverade alla 135 celler, jämförde mot configen, bekräftade roll-call) — se changelog nedan.
- Källans "Summa utgiftsområden" reg-total (1 441 596) avviker 3 mnkr från cellsumman (1 441 593);
  det är källans egen avrundning av totalraden, inte ett transkriberingsfel (cellerna är troget kopierade).

## Hård grind (a1 får aldrig korrumpera A)

a1 räknas in i A för en `(budgetår, kategori)` **endast** när alla 8 partier har en verifierad ram
som täcker **varje** UO i kategorin, i **alla** inkluderade budgetår (snitt-skärning). Annars faller
A tillbaka på a2 helt för den kategorin (flagga `A_a2_only`; aktiv = `A_a1_active`). En saknad eller
icke-numerisk cell ger **hård fail** (aldrig tyst 0), och a1 rang-normaliseras aldrig över färre än 8
partier. Tom `budget_years` → a1 inaktiv överallt → A = a2 (ingen regression). Testat i
[`tests/test_budget.py`](../tests/test_budget.py) + [`tests/test_fas5.py`](../tests/test_fas5.py).

## Effekt på rangordningen (standardvikter)

Med a1 aktiv för alla 7 kategorier (budget 2025) jämfört med ren a2:

| | a2 enbart (innan) | a1+a2 (nu) |
|---|---|---|
| Rangordning | S 3,73 · L 3,39 · MP 3,34 · M 3,28 · KD 3,11 · V 2,59 · SD 2,40 · C 2,39 | **S 3,54 · L 3,33 · MP 3,31 · M 3,23 · KD 3,10 · V 2,63 · C 2,61 · SD 2,46** |

a1 differentierar A trovärdigt: MP högst på klimat-budgetandel, V högst på integration, S högst på
välfärd, KD/L/C höga på försvar, M högst på trygghet. Regeringsblocket (M/KD/L/SD) delar samma ram
→ identiskt a1-bidrag; deras A skiljer sig då bara via a2.

## Begränsningar (version 0)

- **Ett budgetår (2025).** Fler år kan läggas till; grinden kräver fullständig 8-parti-täckning per år.
- **UO26 (statsskuldsräntor → ekonomi)** och **UO27 (EU-avgift → ingen kategori)** ingår i nämnaren
  (total budget); UO26 är ~lika för alla partier och påverkar den *relativa* a1 marginellt.
- **Kräver mänsklig slutgranskning** innan skarp betygsättning (som party_positions).

## Reproduktion / verifiering

```bash
python -m pytest tests/test_budget.py tests/test_fas5.py -q   # a1-matte, grind, blend
python -m pipeline.scorerun                                   # a1 aktiv -> dist/scores.json
```
