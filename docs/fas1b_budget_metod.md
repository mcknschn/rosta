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
strukturering av en officiell källa, inte fabrikation. **Version 1 — expertgranskad + mänsklig sign-off 2026-06-05; a1 aktiv i skarp betygsättning.**

## Källor (budgetår 2023–2025)

`budget_ramar.yaml` täcker nu **tre budgetår** (2023, 2024, 2025) ur respektive rambeslut. Varje
år bidrar med en frame-uppsättning; a1 blir ett **snitt över åren** (se grinden nedan), vilket
fångar mandatperioden bredare och dämpar enårsbrus.

| Budgetår | Källa (rambeslut) | Tabell | dok_id |
|----------|-------------------|--------|--------|
| 2025 | bet. 2024/25:FiU1 "Statens budget 2025 – Rambeslutet" | tabell 35 | HC01FiU1 |
| 2024 | bet. 2023/24:FiU1 "Statens budget 2024 – Rambeslutet" | tabell 2.3 | HB01FiU1 |
| 2023 | bet. 2022/23:FiU1 "Statens budget 2023 – Rambeslutet" | tabell 2.3 | HA01FiU1 |

Ur varje tabell tas kolumnen *Regeringens förslag* (absolut, mnkr) plus *Avvikelse från regeringen*
för S, V, C, MP. Varje oppositionspartis absoluta ram = `Regeringens förslag + partiets avvikelse`
(mekanisk normalisering ur samma tabell). UO13/UO20 hade äldre rubriker 2023 (oförändrade UO-koder).

### Attribution (Codex P0-risk)
Ett parti tilldelas regeringens ram endast när en officiell källa stödjer det. Strukturen är
**identisk för alla tre åren** (Tidöregeringen M/KD/L + SD-stöd; S/V/C/MP i opposition):
- **M, KD, L** = regeringspartier (prop. 2024/25:1, 2023/24:1, 2022/23:1) → regeringens ram.
- **SD** = Tidö-stödparti som **röstade Ja till rambeslutet** (votering FiU1 punkt 2, per-ledamot-
  tally M/SD/KD/L = Ja: 2025, 2024 *och* 2023) → regeringens ram, citerat till voteringen.
- **S, V, C, MP** = egen budgetmotion respektive år → egen ram (avvikelse i rambeslutstabellen).

Ett parti utan egen ram **och** utan citerbar uppslutning bakom en gemensam ram skulle utelämnas —
aldrig gissas. För alla tre åren är alla 8 partier täckta (reservationerna på punkt 1 kommer i båda
nya åren *enbart* från S/V/C/MP, dvs. M/KD/L/SD står bakom regeringens ram).

### Verifiering (ingen fabrikation)
Alla tre åren är verifierade med samma flerlagrade kontroll; 2023/2024 transkriberades aldrig för
hand utan **genererades programmatiskt ur den officiella HTML-källan** och korsverifierades fyra vägar:
- **Intern invariant:** för varje parti och år är `Σ(partiets ram) − Σ(regeringens ram)` lika med
  källans egna avvikelse-totaler i raden "Summa utgiftsområden". 2024 + 2025: matchar på kronan för
  alla fyra oppositionspartier. 2023: S/V/MP på kronan; **C +2 mnkr** — källans egen avrundning av
  totalraden (regeringens totalrad avviker likaså −1 mnkr 2023 / −4 mnkr 2024 / −3 mnkr 2025 från
  cellsumman; per-UO-cellerna är troget kopierade och justeras aldrig för att tvinga fram en summa).
- **Oberoende parser** (`pandas.read_html`, helt annan kodväg än regex-extraktionen) — 0 avvikelser
  över 270 celler (2 år × 5 ramar × 27 UO).
- **Oberoende adversariell re-extraktion** (separat Codex-agent, lokaliserade tabellen via innehåll,
  re-deriverade alla celler, bekräftade roll-call) — 0 avvikelser mot configen; flaggade och
  bekräftade både C-2023-avrundningen och en split-span-cell (2023 UO13 MP `3|51`→351, korrekt).
- **Roll-call bekräftad** ur dokumentstatus (förslagspunkt 2, "Rambeslutet"): 2024 M/SD/KD/L = Ja
  (59/63/16/13), 2023 M/SD/KD/L = Ja (60/61/17/12); S = Nej, V/C/MP = Avstår båda åren.

*(Budget 2025 verifierades tidigare separat: intern invariant på kronan — S +30 886, V +132 499,
C +2 821, MP +147 384 — och re-extraktion av alla 135 celler; reg-totalen avviker 3 mnkr p.g.a.
samma avrundning.)*

## Hård grind (a1 får aldrig korrumpera A)

a1 räknas in i A för en `(budgetår, kategori)` **endast** när alla 8 partier har en verifierad ram
som täcker **varje** UO i kategorin, i **alla** inkluderade budgetår (snitt-skärning). Annars faller
A tillbaka på a2 helt för den kategorin (flagga `A_a2_only`; aktiv = `A_a1_active`). En saknad eller
icke-numerisk cell ger **hård fail** (aldrig tyst 0), och a1 rang-normaliseras aldrig över färre än 8
partier. Tom `budget_years` → a1 inaktiv överallt → A = a2 (ingen regression). Testat i
[`tests/test_budget.py`](../tests/test_budget.py) + [`tests/test_fas5.py`](../tests/test_fas5.py).

## Effekt på rangordningen (standardvikter)

a1 är aktiv för alla 7 kategorier. Rangordningen med a1 över **tre budgetår** (2023–2025) jämfört
med tidigare ett år (budget 2025) och ren a2:

| | a2 enbart | a1+a2, 1 år (2025) | a1+a2, 3 år (2023–2025) |
|---|---|---|---|
| Rangordning | S 3,73 · L 3,39 · MP 3,34 · M 3,28 · KD 3,11 · V 2,59 · SD 2,40 · C 2,39 | S 3,54 · L 3,33 · MP 3,31 · M 3,23 · KD 3,10 · V 2,63 · C 2,61 · SD 2,46 | **S 3,73 · L 3,33 · M 3,28 · MP 3,11 · KD 3,05 · C 2,66 · V 2,65 · SD 2,38** |

a1 differentierar A trovärdigt där budgetandelarna är **väl åtskilda**: MP högst på klimat-
budgetandel (8,3 % vs V 6,4 % vs ~5,3 % för övriga), V högst på integration, KD/L/C höga på försvar.
Regeringsblocket (M/KD/L/SD) delar samma ram → identiskt a1-bidrag; deras A skiljer sig då bara via a2.

> **Caveat (rank-normalisering på nära oavgjorda andelar):** för *ekonomi* ligger alla 8 partiers
> a1-andelar inom ~2 procentenheter (22,4–24,6 %), eftersom ekonomi drar från många stora UO som är
> snarlika för alla. Rang-normaliseringen (DATA.md: A/C rankas, känsligt med 8 datapunkter) förstorar
> då skillnader på andra–tredje decimalen till hela rangskiften — MP ligger ~23,4 % varje år men
> dess *rang* pendlar mellan 2:a och 8:a. **Treårssnittet dämpar** detta (medel av tre brusiga
> rangar) jämfört med ettårsmätningen, men grundkänsligheten kvarstår som en modellegenskap (ej en
> A1-defekt). Kandidat för framtida förfining: en dödzon/min–max på a1 för nära-oavgjorda kategorier.

## Begränsningar (version 1)

- **Tre budgetår (2023–2025).** Fler år kan läggas till; grinden kräver fullständig 8-parti-täckning
  per år (snitt-skärning), och varje nytt år ska köras genom samma fyrlagriga verifiering.
- **UO26 (statsskuldsräntor → ekonomi)** och **UO27 (EU-avgift → ingen kategori)** ingår i nämnaren
  (total budget); UO26 är ~lika för alla partier och påverkar den *relativa* a1 marginellt.
- **Slutgranskad** (mänsklig sign-off 2026-06-05) och aktiv i skarp betygsättning, som party_positions.

## Reproduktion / verifiering

```bash
python -m pytest tests/test_budget.py tests/test_fas5.py -q   # a1-matte, grind, blend
python -m pipeline.scorerun                                   # a1 aktiv -> dist/scores.json
```
