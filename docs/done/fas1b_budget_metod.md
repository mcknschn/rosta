# Fas 1b — a1 budgetprioritering (delpoäng A)

Metod för **a1**, budgetdelen av delpoäng A (faktiskt agerande). A väger 0,40 — den tyngsta
delpoängen — och `A = 0,6·a1 + 0,4·a2` (vikter i [`config/scoring.yaml`](../../config/scoring.yaml)
`A_agerande.components`). a2 (motionsprioritering) byggdes i Fas 1; a1 var **medvetet uppskjuten**
tills den kunde byggas utan att en bräcklig parser korrumperar A. Detta dokument beskriver hur a1
nu byggts robust och gated.

## Vad a1 mäter

`a1(parti, kategori)` = **andelen av partiets föreslagna anslag som går till kategorins
utgiftsområden (UO)**, mätt mot samma andel i de BESLUTADE utgiftsramarna över fönstret. Det är
ett *prioriteringsmått* (som a2), inte ett mått på om mer pengar är rätt — rättheten fångas av B
och D.

```
andel(parti, kat) = Σ_UO ( ram(parti, UO) · UO→kat-vikt ) / Σ_UO ram(parti, UO)
förankring(kat)   = samma räkning på de beslutade ramarna, som medel över fönstrets år
a1(kat)           = net_support_to_score( (andel - förankring) / (andel + förankring) )
```

> **Uppdaterad 2026-08-26 (ADR 0007, biljett #27).** Två saker i det här dokumentet gällde det
> gamla treåriga fönstret och är nu ersatta. Rang-normaliseringen över de åtta partierna föll
> med **ADR 0005** (biljett #21): a1 är absolut och mäts mot en historisk förankring, inte mot
> fältet. Fönstret gick från tre budgetår till **2011-2025** med **ADR 0007** (biljett #27):
> täljaren täcker samma år som förankringen. Avsnitten nedan om källor, verifiering och
> begränsningar är uppdaterade; effekttabellen längre ned är fryst historik från 2026-06-05.

UO→kategori-vikterna ligger i [`config/mappings.yaml`](../../config/mappings.yaml) `expenditure_areas`
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
([`config/budget_ramar.yaml`](../../config/budget_ramar.yaml)), där varje frame **citerar sin källrad**,
och deterministisk kod ([`pipeline/budget.py`](../../pipeline/budget.py)) konsumerar configen. Detta är
en **trogen kopia** av officiella tal — inga belopp imputeras, jämkas eller gissas. Det är
strukturering av en officiell källa, inte fabrikation. **Version 1 — expertgranskad + mänsklig sign-off 2026-06-05; a1 aktiv i skarp betygsättning.**

## Källor (budgetår 2011-2025)

`budget_ramar.yaml` täcker **femton budgetår**, 2011 till 2025, ur respektive rambeslut. Varje år
bidrar med en frame-uppsättning; a1 blir ett **snitt över åren** (se grinden nedan). Fönstret
faller ut ur tre gränser som skrevs före hämtningen och står i
[`docs/done/a_forankring/fonster.json`](a_forankring/fonster.json). Den bindande gränsen är ADR
0007 punkt 2, "alla åtta partier har en citerbar ram": före budgetår 2011 saknade SD mandat i
kammaren och kan därför inte ha någon ram.

Källan är samma tabell varje år, "Regeringens och oppositionspartiernas (eller motionärernas)
förslag till utgiftsramar för `<år>`" i bet. FiU1. Ur den tas kolumnen *Regeringens förslag*
(absolut, mnkr) plus *Avvikelse från regeringen* per parti. Varje partis absoluta ram =
`Regeringens förslag + partiets avvikelse`, alltså mekanisk normalisering ur samma tabell.
Dokument-id per år ges av `pipeline.tools.a_forankring_transcribe.dok_id`, och tabellens rubrik
skrivs ut i configens `source_table` per budgetår.

Antalet ramar varierar mellan åren, eftersom antalet partier med egen budgetmotion gör det: 2011
lade S, MP och V en gemensam motion, 2015 lade M, C, FP och KD en gemensam, och de år ett parti
varken regerade eller lade en egen motion står det på den ram det röstade för.

**Avläsningen sker på tabellens geometri**, alltså kolumnens högerkant, aldrig på cellernas
ordning. Betänkandenas text delar ett tal vid tusentalsmellanslaget så fort två celler är trånga
("+2 650" blir "+2" och "650"), och en textläsning tappar då kolumnen utan att det syns i
utfallet. Två tabeller är dessutom satta liggande på stående sida (bet. 2015/16:FiU1), vilket
läsningen räknar om till läsriktningen. Verktyget är
[`pipeline/tools/budget_ramar_transcribe.py`](../../pipeline/tools/budget_ramar_transcribe.py).

### Attribution (ADR 0007 punkt 2)
Ett parti tilldelas en ram endast på **citerbar grund**, aldrig på ett omdöme. De tre grunderna
prövas i den ordningen, och `basis` i configen bär vilken som gällde:

1. **egen_ram** - partiet har en egen kolumn i rambeslutstabellen, alltså en egen eller gemensamt
   inlämnad budgetmotion.
2. **regeringsstallning** - partiet står bakom budgetpropositionen för året, alltså är kolumnen
   "Regeringens förslag" dess egen ram.
3. **votering** - partiet röstade som regeringspartierna i voteringen om rambeslutet (FiU1
   punkt 2), alltså slöt det upp bakom regeringens ram.

Ett parti som inte når någon av de tre **utelämnas aldrig tyst**: året faller ur fönstret, och
gränsen flyttas framåt. Det är precis vad som händer 2008-2010, där SD saknar både kolumn och rad
i voteringen. Voteringen läses ur riksdagens `voteringlista` per parti, aldrig ur en tolkning.

### Verifiering (ingen fabrikation)
Varje budgetår verifieras fyrlagrigt vid varje körning av verktyget, och utfallet per år skrivs
in i configens rad `verification`:

- **Intern summainvariant per kolumn:** cellsumman mot källans egen rad "Summa utgiftsområden".
  Över de femton åren ligger varje avvikelse inom **4 mnkr**, alltså inom källans egen avrundning
  (toleransen är 27 mnkr, en per utgiftsområde). Per-UO-cellerna är troget kopierade och justeras
  aldrig för att tvinga fram en summa.
- **Oberoende tabell:** betänkandets bilagor bär samma ramar ABSOLUT och i tusental kronor, läst
  av `a_forankring`-verktygets radparser, alltså en annan tabell, en annan enhet och en annan
  kodväg. **Regeringens ram träffar bilagan på kronan i alla femton åren.** Reservationerna
  träffar också, inom en miljon kronor som är avrundningen, med ett undantag: allianspartiernas
  reservation 2015 skiljer sig 200 mnkr på UO2 och 112 mnkr på UO25 från deras gemensamma
  budgetmotion. Det är två olika dokument, och skillnaden är ett fynd om året.
- **Oberoende parser:** samma tabell läst ur betänkandets HTML, en helt annan kodväg. Finns för
  fem av åren; de övriga betänkandenas HTML har celler som gått sönder i konverteringen.
- **Roll-call** ur riksdagens voteringlista, per parti, för varje års rambeslutspunkt.

Utöver de fyra lagren läser `--audit` om de tre expertgranskade budgetåren 2023-2025 ur PDF:en.
**405 celler, noll avvikelser** mot den signade configen. Det är ett prov på hela kedjan: samma
tal som en tidigare, oberoende transkribering kom fram till.

**Version per budgetår.** 2023-2025 står som `version: 1` (expertgranskade, mänsklig sign-off
2026-06-05). De tolv nya åren står som `version: 0` och väntar på mänsklig sign-off.

## Hård grind (a1 får aldrig korrumpera A)

a1 räknas in i A för en `(budgetår, kategori)` **endast** när alla 8 partier har en verifierad ram
som täcker **varje** UO i kategorin, i **alla** inkluderade budgetår (snitt-skärning). Annars faller
A tillbaka på a2 helt för den kategorin (flagga `A_a2_only`; aktiv = `A_a1_active`). En saknad eller
icke-numerisk cell ger **hård fail** (aldrig tyst 0), och a1 rang-normaliseras aldrig över färre än 8
partier. Tom `budget_years` → a1 inaktiv överallt → A = a2 (ingen regression). Testat i
[`tests/test_budget.py`](../../tests/test_budget.py) + [`tests/test_fas5.py`](../../tests/test_fas5.py).

## Effekt på rangordningen (standardvikter)

> **FRYST HISTORIK från 2026-06-05.** Tabellen nedan gällde det treåriga fönstret och den
> dåvarande rang-normaliseringen. Både fönstret och avbildningen har bytts sedan dess, av
> ADR 0005 respektive ADR 0007, så talen går inte att jämföra med dagens. Aktuell ranking
> står i `dist/scores.json`, och driften mellan körningar i `dist/scores.snapshot.json`.

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

## Begränsningar

- **Fönstret börjar 2011.** Gränsen är källans, inte ett omdöme: SD saknade mandat i kammaren före
  valet 2010 och kan därför inte ha någon citerbar ram för budgetår 2008-2010.
- **Ett långt fönster blandar regeringsår med oppositionsår.** För ett regeringsparti är ramen
  koalitionens och inte partiets egen. Kostnaden är skriven i förväg i ADR 0007 Följder och står i
  metodrutan på sajten. Attributionen per år är citerbar, så det går att se vilka år som är vilka.
- **En gemensam budgetmotion ger flera partier samma ram.** Det gäller S, MP och V 2011 och M, C,
  FP och KD 2015. Det är en riktig likhet i källan och jämnas aldrig ut.
- **UO26 (statsskuldsräntor → ekonomi)** och **UO27 (EU-avgift → ingen kategori)** ingår i nämnaren
  (total budget); UO26 är ~lika för alla partier och påverkar den *relativa* a1 marginellt.
- **Sign-off per år.** 2023-2025 är slutgranskade (mänsklig sign-off 2026-06-05). De tolv nya åren
  står som version 0 och väntar på sin.

## Reproduktion / verifiering

```bash
python -m pytest tests/test_budget.py tests/test_fas5.py -q   # a1-matte, grind, blend
python -m pytest tests/test_a_fonster.py -q                   # fönstret, villkorsklausulen (ADR 0007)
python -m pipeline.tools.budget_ramar_transcribe --audit      # configen mot källan, exit 1 vid diff
python -m pipeline.scorerun                                   # a1 aktiv -> dist/scores.json
```
