# Rösta

En app som så objektivt som möjligt hjälper väljaren att förstå vilket svenskt
riksdagsparti som bäst matchar hens prioriteringar. Väljaren viktar kategorier av
sakfrågor; appen rangordnar partierna utifrån faktiskt data från officiella svenska källor.

**Live: <https://mcknschn.github.io/rosta/>** — publiceras automatiskt från `main`
([pages.yml](.github/workflows/pages.yml)); `web/` är sajtens rot.

- **Modellen:** [IDEA.md](IDEA.md)
- **Datainsamling & arkitektur:** [DATA.md](DATA.md)
- **Exekveringsplan (faser 0–6, fryst historik):** [docs/ROADMAP.md](docs/done/ROADMAP.md)
- **Framåtblickande backlog (data, evidens, drift):** [docs/BACKLOG.md](docs/BACKLOG.md)
- **Grundregler:** [CLAUDE.md](CLAUDE.md) — endast officiella svenska källor.

## Princip: rådata lokalt, betyg i deploy

```
Officiella API:er ─▶ data/raw/ (lokalt) ─▶ data/warehouse.duckdb (lokalt)
                                          ─▶ claims + indicator_effects (lokalt)
                                          ─▶ dist/scores.json + dist/evidence.json  ◀── deployas
```

Frontenden räknar `totalpoäng = Σ(kategoribetyg × väljarens vikt)` i webbläsaren.
Allt rådata och hela warehouse stannar lokalt (se [.gitignore](.gitignore)); endast de
förberäknade betygen och en bantad bevisindex deployas.

## Betygsmodell (helt automatisk)

Per parti och kategori: `betyg = 0.40·A + 0.35·B + 0.15·C + 0.10·D` (0–5, med osäkerhetsintervall).

| Delpoäng | Mäter | Källor |
|----------|-------|--------|
| A – Faktiskt agerande | Budgetprioritering + lagstiftningsaktivitet | Riksdagen, statsbudget |
| B – Evidens/träffsäkerhet | Källstöd för förslagens indikatoreffekt | IFAU, SBU, Vårdanalys, Brå, ESO, Riksrevisionen … |
| C – Genomförbarhet/ansvar | Makt (regering/region/kommun) + finansiering | Valmyndigheten, Regeringskansliet, SKR, Kolada |
| D – Resultat | Indikatorförändring där partiet hade ansvar | SCB, Brå, Socialstyrelsen, Skolverket … |

Inga partibetyg sätts för hand. Allt mänskligt omdöme ligger i versionsstyrd config
([config/](config/)) och i den citerade evidensliggaren.

## Struktur

```
config/     modellen som config (categories, sources, mappings, scoring, claims,
            evidence_ledger, party_positions, coverage_allowlist)
schemas/    JSON-scheman för observations/actions/responsibility/claims/effects/scores/evidence
pipeline/   datapipelinen (sources, claims, effects, positions, score, tools/coverage_report)
tests/      golden tests + schemavalidering
dist/       scores.json + evidence.json (deploy-artefakt, genereras)
web/        frontend (Fas 6)
```

## Kom igång

```powershell
pip install httpx pyyaml pydantic jsonschema duckdb pandas openpyxl pytest ruff
python -m pytest                     # golden tests + schemavalidering (alla faser)
ruff check .                         # lint

# Bygg hela pipelinen lokalt (hämtar live från Riksdagen/SCB/Kolada -> data/ + dist/)
python -m pipeline.build_all

# Frontend: servera repo-roten och öppna /web/
python -m http.server 8000          # -> http://localhost:8000/web/
```

Enskilda steg: `python -m pipeline.build_fas1` (Riksdagen → actions/responsibility),
`python -m pipeline.build_fas2` (SCB/Kolada → observations), `python -m pipeline.scorerun`
(→ `dist/`).

## Status

Hela pipelinen kör lokalt end-to-end (Fas 0–6 + b-faser). Datatäckningen är medvetet **avgränsad
och loggad**: **A = 0,6·a1 + 0,4·a2** — a2 (motionsprioritering, andel av egna motioner) har full
täckning, och **a1 (budgetprioritering) är nu byggd och gated**: partiernas föreslagna utgiftsramar
per UO ur officiella källor (budget 2025, bet. 2024/25:FiU1; troget transkriberade, ingen runtime-
parser; [metod](docs/done/fas1b_budget_metod.md)) — a1 vägs in bara när alla 8 partier har verifierad ram
för kategorins UO, annars faller A på a2. **C (ansvar/makt) blandar nu nationell regeringsmakt med
subnationell makt** (SKR-styren: 21 regioner + 290 kommuner × 3 mandatperioder, Fas 1c) per kategori
via en region/kommun-split efter lagstadgat ansvar — full täckning, hög säkerhet (c2 finansiering
uppskjutet, ej neutralt byggbart → C = c1; [metod](docs/done/fas1c_subnational_metod.md)); **D (resultat)
attribueras** från officiella årsserier i **alla 7 kategorier** (43/68 indikatorer, 29/35 undermått —
försvar och demokrati fick D-data 2026-06-09/12; [docs/done/fas3_coverage.md](docs/done/fas3_coverage.md)) där partiet
haft nationell makt, sedan 2026-06-12 krympt mot neutral efter viktad undermåttsbredd. **B (evidens)
är aktiverad för alla 7 kategorier** via 269 källbelagda partiståndpunkter (riksdagsvotering/motion),
coverage-viktade så tunn täckning drar mot neutral (expertgranskad, `version 2`;
[metod](docs/done/fas4b_partistandpunkter_metod.md)). Ståndpunkterna är **panel-harmoniserade** (Fas 4c, alla
8 partier per åtgärdstyp bedömda mot en gemensam frusen rubrik) och liggaren utökad med den enda omstridda
åtgärdstyp som passerade evidens-/negativ-grinden av 8 skannade (`ny_karnkraft` → effektbrist; 7 hade för
blandad officiell evidens och lämnades inerta – [Fas 4c](docs/done/ROADMAP.md)). **Inga ståndpunkter fabriceras**
— varje rad citerar en riksdagskälla och är adversariellt verifierad mot fulltext. **Frontenden (Fas 6) är byggd** — en statisk, byggfri väljarkompass i [web/](web/) som viktar kategorierna
client-side, rangordnar partierna med osäkerhetsband och expanderbart bevisspår, delar vikter via URL och
visar en tydlig förbehållsbanner. Den är **Playwright-e2e-testad** (8 fall).
**Frontenden uppfyller WCAG 2.2 nivå AA för de maskinellt granskade kriterierna** (kontrast ≥4,5:1,
reflow vid 320 px, fokushantering och ARIA-kontrakt; det enda blockerande felet — fokus-/expanderings-
förlust vid omräkning — är åtgärdat och regressionstestat). Granskningen är gjord på källkod och
automatiserad mätning. **Uppläsningsupplevelsen med skärmläsare är inte granskad**, och något sådant
test är inte planerat (avfört som designbeslut 2026-08-16); anspråket ovan sträcker sig därför inte
längre än till det maskinellt prövbara. Detaljerad audit arkiverad i
[docs/done/fas6_wcag.md](docs/done/fas6_wcag.md). Kör `python -m http.server 8000` och
öppna `/web/`. Per-fas status:
[DATA.md §6](DATA.md). Full exekveringsplan: [docs/ROADMAP.md](docs/done/ROADMAP.md).

> `dist/scores.json` är en **pipeline-demonstration på riktig data**, inte ett färdigt röstråd —
> rankingen drivs tills vidare främst av aktivitet + makt (+ resultat där makt funnits), vilket
> framgår av låg säkerhet och flaggor i utdata.
