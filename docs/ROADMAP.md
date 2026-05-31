# Rösta — Exekverings-roadmap (Fas 0–6)

> Sammanslagen, körbar roadmap för det svenska civic-tech-projektet **Rösta**: en automatisk, källbackad och granskningsbar partibetygsmotor som omvandlar officiell svensk statistik och riksdagsdata till kategoribetyg (0–5) per parti, med användarstyrd viktning i en statisk frontend.
>
> **Bärande princip:** Inget mänskligt omdöme och inga partibetyg får finnas i kod — endast i versionsstyrd config (`config/*.yaml`). All data är spårbar till en officiell källa via `source_refs` och manifest. Endast `dist/scores.json` + `dist/evidence.json` + metodbeskrivning deployas; rådata och warehouse stannar lokalt.

---

## 1. Översikt och beroendegraf

### 1.1 Lagermodell (DATA.md)

| Lager | Innehåll | Format | Deployas? |
|-------|----------|--------|-----------|
| Lager 1 (raw) | Rådatasvar + manifest per hämtning | JSON under `data/raw/<källa>/<dataset>/<datum>.json` | Nej (gitignore) |
| Lager 2 (warehouse) | Normaliserade `observations`/`actions`/`responsibility` | Parquet + `data/warehouse.duckdb` | Nej |
| Lager 3 (claims/effects) | `claims` + `indicator_effects` | Parquet + DuckDB-tabeller | Nej |
| Deploy | `scores.json` + `evidence.json` + metod | JSON (schemavaliderat) | **Ja** |

### 1.2 Pipeline-flöde

```
config/*.yaml  ──┐
                 ▼
 Fas 1-3: källadaptrar → Lager 1 (raw+manifest) → Lager 2 (observations/actions/responsibility)
                 │                                          + Lager 3-evidensliggare (config)
                 ▼
 Fas 4: claims-engine → claims → indicator_effects (Lager 3)
                 ▼
 Fas 5: scoring-engine → A/B/C/D → kategoribetyg 0-5 + CI → dist/scores.json + dist/evidence.json
                 ▼
 Fas 6: statisk frontend → läser dist/*.json → client-side viktning → rankad partilista + bevisspår
```

### 1.3 Beroendegraf mellan faser

```
Fas 0 (skelett, config, scheman, tooling, golden-test-stomme)
  │
  ├──> Fas 1 (Riksdagen/Valmynd/SKR → actions/responsibility)   [ej i indata; antas leverera _client/cache/models/transform-stomme]
  │
  ├──> Fas 2 (SCB + Brå/NTU + Kolada → observations)            beror på Fas 0; F2-T0 fyller Fas 1-luckor vid behov
  │       │
  │       └──> Fas 3 (sektorsmyndigheter + evidensliggare)      beror på Fas 2 (täckningsgap) + Fas 0/1-stomme
  │               │
  │               ▼
  └──────────────> Fas 4 (claims/effects engine)               konsumerar Lager 2 (Fas 1-3) + evidensliggare (Fas 3)
                          │                                      kan färdigställas mot mini_warehouse-fixtur oberoende
                          ▼
                   Fas 5 (scoring engine → dist/*.json)          konsumerar Fas 4:s indicator_effects/claims
                          │                                      kan köras mot syntetisk fixtur oberoende
                          ▼
                   Fas 6 (frontend)                              konsumerar dist/-kontraktet (scheman delas med Fas 5)
```

**Kritiska blockeringar:**

- **Fas 0 blockerar allt** — den lägger config-scheman, Pydantic/JSON-Schema-bron, golden-test-stommen och tooling (uv/ruff/mypy/pytest/CI).
- **Fas 2 → Fas 3** via täckningsgap: Fas 3 ska bara fylla submått Fas 1–2 inte redan täckt (coverage_report körs först).
- **Fas 4, 5, 6 är "fixtur-frikopplade"**: var och en kan slutföras och bevisas mot syntetiska fixturer **innan** uppströmsdata finns. Riktig data kopplas in när Lager 2/3 är fyllt.
- **Schema-delning Fas 0/5/6**: `scores.schema.json` + `evidence.schema.json` är ETT kontrakt. Fas 5 genererar dem ur Pydantic; Fas 6 konsumerar dem. `gen_schemas`-drift-check i CI hindrar isärglidning.

> **Repo-status (verifierad 2026-05-29):** Repot innehåller redan `config/{categories,claims,mappings,scoring}.yaml`, ett antal `schemas/*.schema.json` (action, claim, evidence, indicator_effect, observation, responsibility, scores — notera enkelnamn `observation.schema.json`), samt tomma `docs/`, `pipeline/`, `tests/`, `web/`, en `.gitignore`, `README.md` och en `pyproject.toml`. **Konsekvens:** flera Fas 0-/Fas 5-deliverabler ska *kompletteras additivt*, inte skapas från noll. Avstäm filnamn (`observation` vs `observations`) tidigt — golden-testet i Fas 0 ska låsa det faktiska namnet.

> **Levererat 2026-05-30 (b-faser, ovanpå Fas 0–6):**
> - **Fas 2b ✅** — 8 kanoniska årsserier verifierade live mot officiella källor och inlästa i warehouse (182 obs, 4 kategorier): SCB `arbetsloshet`/TAB2891, `sysselsattning`/TAB6514, `bnp_per_capita`/TAB6728, `territoriella_utslapp`/TAB4698, `trangboddhet`/TAB6439; Kolada `skolresultat`/N15507, `behoriga_larare`/N15813, `bidragsberoende`/N31825. Rätt enskild nationell serie isoleras via `fixed`-dimensionskoder. Fixade `kolada.kpi_title`-bugg (v3 `/kpi?id=` → `/kpi/{id}`).
> - **Fas 5b ✅** — D-resultatattribution (`score.attribute_series` + `scorerun.category_d`): tecken på riktningsjusterad årsförändring, attribution till sittande regering med 1 års lag, makt-/koalitionsvikt, `min_responsibility`-gate, `D_thin_basis`-flagga. D mäts nu i ekonomi/välfärd/klimat/integration.
> - **Fas 4b ✅** — B-maskineri (`pipeline/positions.py`: `party_positions × evidence_ledger → indicator_effects → B`). **Kurerings-gated** — inga ståndpunkter fabriceras; B aktiveras automatiskt när källbelagda ståndpunkter fylls i.
> - **Fas 4b — B utrullad för ALLA 7 kategorier ✅ (version 0, kräver mänsklig slutgranskning)** — `config/party_positions.yaml` fylld med **130 källbelagda, adversariellt verifierade + panel-harmoniserade** partiståndpunkter (113 supports / 17 opposes; harmoniserade i Fas 4c). Klimat handkurerat (reduktionsplikt via VOTERING bet. 2023/24:MJU5 + koldioxidskatt); övriga 6 kategorier via research+verifierings-workflow (en agent per (åtgärdstyp, parti); oberoende granskare bekräftade citat mot fulltext `.text` — fångade fabrikat). Inerta åtgärdstyper (mixed/unclear → 0 B-effekt) ej kodade; `internationella_materielsamarbeten` (negativ riktning) exkluderad. **B coverage-viktad** (`B = 2.5 + (B_raw−2.5)·coverage`, `B_thin_coverage`-flagga) — annars mättade B vid 5.0 för nästan alla (de flesta åtgärdstyper är konsensus). Metod + Codex-konsensus i [docs/fas4b_partistandpunkter_metod.md](fas4b_partistandpunkter_metod.md). Preliminär ranking efter Fas 4c: **S 3.72 · L 3.39 · MP 3.34 · M 3.30 · KD 3.12 · V 2.59 · SD 2.41 · C 2.39**. **Fas 4c klar** (panel-harmonisering + omstridda åtgärdstyper, Codex-gated) — se Fas 4c nedan. Återstår: mänsklig expertgranskning (särskilt de flaggade propositionsavslags-opposes + ny_karnkraft).
> - **Fas 1b ✅** — `a1` budgetprioritering **byggd och aktiv (gated)**: partiernas föreslagna utgiftsramar per UO (budget 2025) ur **bet. 2024/25:FiU1 tabell 35**, troget transkriberade till `config/budget_ramar.yaml` (version 0, källrad per frame). **Ingen runtime-parser** — empiriskt bekräftat att ingen strukturerad API-väg till anslag per UO finns (förslagspunkts-endpointen saknar belopp-fält); en bräcklig parser fick inte korrumpera A (tyngsta delpoängen). `A = 0,6·a1 + 0,4·a2`; **hård grind** (`pipeline/budget.py`): a1 vägs in för en (budgetår, kategori) endast när alla 8 partier har verifierad ram för varje kategori-UO, annars `A=a2` (flagga `A_a2_only`); saknad cell → hård fail, aldrig tyst 0. Attribution: M/KD/L=regering, SD=Tidö-stöd (röstade Ja, votering FiU1 punkt 2), S/V/C/MP=egen motion. Oberoende adversariellt verifierad (135 celler + roll-call); intern invariant matchar källans avvikelse-totaler på kronan. Design i samråd (Codex-konsensus Option D). [Metod](fas1b_budget_metod.md). Voteringsprov utökat till hela fönstret (12 riksmöten, sampelt; matar ännu inget betyg).
> - **Fas 3 (delvis) ✅/🟡** — täckningsverktyg `pipeline/tools/coverage_report.py` (T3.0) + coverage-gate `tests/test_fas3_gate.py` (inget tyst gap: varje indikator inläst ELLER allowlistad i `config/coverage_allowlist.yaml`, [docs/fas3_coverage.md](docs/fas3_coverage.md)). **7 nya D-serier**: vårdköer, konsumtionsbaserade utsläpp, självförsörjningsgrad utrikes födda, dödligt våld via Brå, **fossil energianvändning via Energimyndigheten EN0202_8 (ny PxWeb-v1-adapter `pipeline/build_fas3.py`)**, samt **brottsutsatthet + upplevd otrygghet via Brå NTU Tabellsamling (blad 3A + 4A:1, `bra.fetch_ntu`)** → D i **5 kategorier** (klimat och **trygghet** har nu 3 D-serier vardera). NTU-metodbrytet hanteras källtroget: utsatthetsaggregatet finns bara 2016+, otryggheten 2007–2016 är omräknad med annan metod → endast nuvarande-metod-fönstret tas med (Codex-konsensus + oberoende re-extraktion av alla 18 årsvärden, VERDICT CONFIRMED). **Härledda indikatorer** (`pipeline/derived.py`): deterministisk gap/kvot-beräkning ur två verifierade serier (två-tabells-operander + rimlighetsgrind på nivån). Inlästa: `sysselsattningsgap_inrikes_utrikes` (SCB TAB6529, sysselsättningsgrad inrikes − utrikes födda; internt korsverifierad mot den redan inlästa självförsörjningsgraden) och `produktivitet` (SCB TAB3610 BNP marknadspris fasta priser ÷ TAB5622 arbetade timmar i hela ekonomin → kr/timme; Codex-konsensus + oberoende adversariell verifiering CONFIRMED, reproducerar finanskris-svackan 2008–2009 och produktivitetsfallet 2022–2023). **17 D-dugliga indikatorer / 386 obs**. Fixade SCB-loaderbugg (eliminerbara dimensioner gav tyst fel serie). Evidensliggaren utbyggd till 30 källverifierade poster (T3.9, AI-utkast, expertgranskning återstår). Återstår: fler sektorsadaptrar (Socialstyrelsen, Skolverket, Medlingsinstitutet för realloner, Brås uppklarings-/återfallstabeller) + fler härledda (utslappsminskning_per_krona, elprisvolatilitet). `realloner` kräver Medlingsinstitutets konjunkturlönestatistik — SCB:s API saknar en ren helekonomi-löneserie (sonderat 2026-05-31). Partiståndpunkter för B är nu kompletta för alla 7 kategorier och panel-harmoniserade (Fas 4c).
>
> **Levererat 2026-05-31 (Fas 1c — subnationell styresdata → C, F1-T7):**
> - **Regioner kompletta ✅** — alla **21 regioner × 3 mandatperioder** (post-val-styre efter valen 2014/2018/2022) troget transkriberade i `config/mappings.yaml:subnational_governance` ur SKR:s officiella öppna data **"Styren i regioner 1994-2022"** ([catalog.skl.se dataset 80](https://catalog.skl.se/catalog/1/datasets/80)). **Korsverifierad** mot SKR:s separata "Styren i regioner efter valet 2022" (matchar 21/21 exakt) och kontrollsummorna matchar SKR:s halvtidsuppföljnings-PDF (2024-11-30) "efter valet"-tal exakt. Endast de 8 riksdagspartierna i `leading_parties`; lokala partier (ÖP) noteras men poängsätts ej. Ingen runtime-parser — reproducerbar via `pipeline/tools/skr_regions_transcribe.py`. Golden-tally pinnar datan i `tests/test_source_skr.py`.
> - **Kommuner kompletta ✅** — alla **290 kommuner × 3 mandatperioder** ur SKR:s öppna data **"Styren i kommuner 1994-2022"** (resource/127), maskinellt transkriberade till `config/subnational_municipalities.yaml` via `pipeline/tools/skr_municipalities_transcribe.py` (290 poster; egen fil för läsbarhet). 2022-talen inom ±2 av halvtidsuppföljnings-PDF (ögonblicksvariation mellan SKR-produkter). Golden-tally pinnar datan.
> - **`pipeline/sources/skr.py`** — `build_regional_responsibility()` + `build_municipal_responsibility()` → `responsibility` (regional 219 + municipal 2706 rader) i warehouse via `build_fas1.py` (idempotent, schema-validerad, source_ref `skr:`).
> - **C-wiring ✅ (fixar den platta per-parti-C-konstanten över alla kategorier)** — `scorerun.regional_fractions()` + `municipal_fractions()` + `category_c()`: nationell + subnationell makt blandas **per kategori** enligt `level_weights`, där den kombinerade regional_municipal-bucketen delas efter en **region/kommun-split satt av lagstadgat ansvar** (`scoring.yaml:subnational_split`: valfard 0.45/0.55, trygghet & integration 0/1 = kommun-only, klimat 0.4/0.6, default 0.3/0.7), rank-normaliserat. Full subnationell täckning → C-säkerhet **hög**; forsvar nationellt per design (`C_national_only_by_design`); guard `C_missing_subnational` bara om datafil saknas. **Codex-granskad regionaldesign** (blanda-sedan-rank, jämn termvikt). C bär nu kategorisignal (trygghet/forsvar skiljer sig; övriga rank-lika pga korrelerad region/kommun-makt — sann egenskap, ej fel).
> - **c2 (finansiering) UPPSKJUTET (beslut Fas 1c, användarsamråd)** — C = c1 (makt). Inget objektivt, riktningsneutralt och differentierande finansieringsmått går att bygga ur officiell svensk data (alla partibudgetar formellt finansierade → likformigt; saldo-/ramverksmått gynnar åtstramning → bryter neutraliteten; "driver de det de lovar" fångas redan av A+B+D, alternativen kräver subjektiv programtolkning eller återanvänder A:s data). Komponentvikter (0.7/0.3) behålls som avsikt. [Metod §c2](fas1c_subnational_metod.md). **Återstår (ej blockerande):** mandatperiod-skiften mitt i period; subnationell D-resultatdata.

---

## Fas 0 — Repo-skelett, config-komplettering, JSON-scheman, Python-tooling, CI, golden-test-stomme

> **✅ Status: KLAR och verifierad (2026-05-29)** — `36 passed`, `ruff: All checks passed!`, CI tillagd, på Python 3.14.2.
>
> **Den faktiska implementationen avviker medvetet från utkastet nedan** (utkastet skrevs av en designagent som inte såg den färdiga koden):
> - **Layout:** flat `pipeline/`-paket, inte `src/rosta/`. Enklare och tillräckligt för en applikation.
> - **Schemanamn:** singular (`observation.schema.json` …), låst av golden-testet.
> - **Tooling:** pip + `ruff` + `pytest` (inte `uv`/`mypy`). CI kör ruff + pytest på Python 3.12.
> - **Config-scheman för YAML-filerna:** ej skapade — invarianterna verifieras i stället direkt i `pipeline/config.validate()` + `tests/test_config.py`.
> - **Verifierat:** 7 kategorier / standardvikt 100 / 34 submått / 50 indikatorer; A/B/C/D = 40/35/15/10; IDEA.md:s totalpoängexempel (3,8325); schemafixturer + sabotagetest.
> - **Valfri kvarvarande härdning:** `uv`-lockfil, `mypy`, config-scheman, ADR-0001.
>
> Task-tabellen nedan är den ursprungliga designen och behålls som referens/checklista.

### Mål
Lägg den reproducerbara grunden som Fas 1–6 hänger på: komplett repo-skelett (src-layout `src/rosta/`), de fem versionsstyrda `config/*.yaml` (komplettera de saknade `sources.yaml` + `mappings.yaml`), JSON Schema Draft 2020-12 för samtliga artefakter och config-filer, `pyproject.toml` + uv-lockfil med ruff/pytest/mypy, `.gitignore` som håller data lokalt, CI-workflow och en körbar golden-test-stomme som **bevisar** att varje config-fil är internt konsistent och validerar mot sitt schema. Inga partibetyg eller mänskligt omdöme i kod.

**Exit-villkor (DoD):** `uv run pytest` grönt, `uv run ruff check` + `ruff format --check` + `mypy src` rent, alla scheman laddar i `Draft202012Validator`, befintliga config-filer (categories/scoring/claims) oförändrade i sak.

### Task-tabell

| id | Task | Deliverable | Acceptanskriterium |
|----|------|-------------|--------------------|
| T0.1 | Git, `.gitignore`, src-layout | `.gitignore`, `src/rosta/__init__.py` (`__version__='0.0.0'`), `src/rosta/sources/__init__.py`, stubbar `{transform,claims,effects,score,schema}.py`, `.gitkeep` i `data/raw/`,`dist/`,`tests/fixtures/`, `docs/ADR-0001-repo-layout.md`, git-repo (main) | `git status` fungerar; `git check-ignore data/raw/x.json` träffar; `git check-ignore uv.lock` tomt; `import rosta` → `0.0.0`; inga betyg i .py |
| T0.2 | `pyproject.toml` + uv-miljö + ruff/pytest/mypy | `pyproject.toml`, `uv.lock` (eller dokumenterad pip-fallback) | `uv run python -c "import yaml,pydantic,jsonschema,duckdb,httpx,pandas;print('ok')"`; `ruff check`/`format --check` exit 0; `pytest -q` startar; `uv.lock` committad |
| T0.3 | `config/sources.yaml` (NY) — källregister | `config/sources.yaml` | YAML parsar; minst riksdagen/scb_pxweb/kolada med `license` satt och `dataset_ids:{}` tomt; Kolada `/v3` + 410-gotcha; SCB rate_limit 30/10s + 150000 celler; varje källa har `auth`+`license` |
| T0.4 | JSON Schema Draft 2020-12 för alla artefakter + config | `schemas/{observations,actions,responsibility,claims,indicator_effects,scores,evidence}.schema.json` + `{categories,sources,mappings,scoring,claims.config}.schema.json` + `schemas/README.md` | Alla 12 scheman: `Draft202012Validator.check_schema` utan fel; claims-enums = `claims.yaml`; party-enum = `[S,M,SD,C,V,KD,L,MP]`; scores kräver `score`,`ci[2]`,`components{A,B,C,D}`; unika `$id` |
| T0.5 | `config/mappings.yaml` (NY) | `config/mappings.yaml` | YAML validerar mot `mappings.schema.json`; `expenditure_area_to_category` täcker alla 7 kategorier; `government_periods` täcker 2014–2026 utan glapp, varje rad har `source`; ingen vikt-duplicering; `regional_municipal_governance` draft-block |
| T0.6 | `src/rosta/schema.py` — bro config↔pydantic↔JSON Schema | `src/rosta/schema.py` | `PARTIES`(8)/`CATEGORY_IDS`(7); `get_validator('scores')` OK; `validate_config(...)` tomt för alla fem; `mypy` exit 0; Pydantic avvisar fel enum |
| T0.7 | Golden-test-stomme | `tests/test_config.py`, `tests/test_schemas.py`, `tests/fixtures/{scores,evidence}.min.json` | `pytest -q` grönt ≥20 fall, 0 fel/skip; medvetet sabotage (submått-vikt≠100) failar exakt ett test; `scores.min.json` validerar grönt, `score=6` rött |
| T0.8 | CI-workflow | `.github/workflows/ci.yml`, `README.md` | YAML giltig, refererar uv→ruff→format→mypy→pytest i ordning; pythonpath=src i CI; README dokar `uv sync`+`uv run pytest` |
| T0.9 | Verifiering, ADR, commit | `docs/ADR-0001-repo-layout.md`, `docs/PHASE-0-DONE.md`, branch `phase-0-skeleton` (1 commit) | Hela verifieringslistan grön i ren shell; ADR motiverar src-layout/uv/schema-dubbelspår; PHASE-0-DONE listar draft-platshållare; commit på branch, ej pushat |

### Filer
`.gitignore`, `pyproject.toml`, `uv.lock`, `config/sources.yaml` (NY), `config/mappings.yaml` (NY), `config/{categories,scoring,claims}.yaml` (finns, rörs ej i sak), `schemas/*.schema.json` (12 st), `schemas/README.md`, `src/rosta/{__init__,schema}.py`, `src/rosta/sources/__init__.py`, `src/rosta/{transform,claims,effects,score}.py` (stubbar), `tests/test_config.py`, `tests/test_schemas.py`, `tests/fixtures/{scores,evidence}.min.json`, `.github/workflows/ci.yml`, `README.md`, `docs/ADR-0001-repo-layout.md`, `docs/PHASE-0-DONE.md`, `.gitkeep`-filer.

### Verifiering (körbara steg)
```bash
cd "c:/Users/marcu/Documents/GitHub/Rösta"
uv sync --all-extras --dev                       # fallback: python -m pip install -e .[dev]
uv run python -c "import yaml,pydantic,jsonschema,duckdb,httpx,pandas;print('deps ok')"
uv run ruff check . && uv run ruff format --check .
uv run mypy src
uv run python -c "import json,glob; from jsonschema import Draft202012Validator as V; [V.check_schema(json.load(open(p,encoding='utf-8'))) for p in glob.glob('schemas/*.schema.json')]; print('schemas ok')"
uv run python -c "from rosta.schema import validate_config; assert all(validate_config(c)==[] for c in ['categories','sources','mappings','scoring','claims']); print('config valid')"
uv run python -c "import yaml;d=yaml.safe_load(open('config/categories.yaml',encoding='utf-8'));c=d['categories'];print(len(c), sum(x['standard_weight'] for x in c), sum(len(x['submeasures']) for x in c), sum(len(x['indicators']) for x in c))"   # → 7 100 34 50
uv run pytest -q
git check-ignore data/raw/x.json   # träff
git check-ignore uv.lock           # tomt
```

### Risker (urval)
- **uv ej installerat** + **pyyaml saknas globalt**: installera uv i T0.2 eller kör pip-fallback; pyyaml är hård dependency (inte bara dev). Alla verifieringskommandon ska ha `uv run`-form **och** venv-fallbackform.
- **Python 3.14 lokalt vs CI-golv 3.12/3.13**: `requires-python='>=3.12'`, undvik 3.14-only-syntax.
- **Befintliga config-filer av hög kvalitet**: T0.3/T0.5 skapar BARA de saknade; golden-test låser invarianter; `git diff` granskas i T0.9.
- **Dubbelunderhåll enums config↔schema**: golden-test asserterar enum-paritet.
- **Icke-ASCII rotnamn (Rösta) + cwd-nollställning mellan bash-anrop**: läs allt med `encoding='utf-8'`; `repo_root()` letar uppåt efter `pyproject.toml`, hårdkoda aldrig sökväg.

### Exit-kriterium (DoD)
Git-repo med `.gitignore` som bevisat håller `data/` lokalt men committar `uv.lock`; alla fem `config/*.yaml` finns och validerar mot sitt schema (tre befintliga oförändrade i sak); alla 12 scheman är Draft 2020-12 och passerar `check_schema`; `src/rosta/` importerar; `pytest` grönt med invariant-låsta golden tests (7/100/34/50, A/B/C/D=40/35/15/10, level-vikter=1.0, enum-/cross-konsistens) + deploy-fixturer validerade och sabotage bevisat failande; ruff/format/mypy rena; CI kör samma kedja; ADR-0001 + PHASE-0-DONE dokumenterar draft-platshållare (`sources.dataset_ids`, `government_periods`-källor, `regional_municipal_governance`). Allt committat på branch `phase-0-skeleton`, ej pushat.

---

## Fas 1 — Riksdagen (actions/A) + Valmyndigheten/Regeringskansliet/SKR (responsibility/C)

### Mål
Bygg pipeline-stommen och de tre politiska källadaptrarna som definierar partiernas AGERANDE (delpoäng A) och ANSVAR (delpoäng C) för hela fönstret 2014–2026, ladda dem deterministiskt till DuckDB-tabellerna `actions` och `responsibility`, och pinna alla `dataset_ids`/licenser/styren i versionsstyrd config. Konkret: (1) `pipeline/sources/riksdagen.py` hämtar motioner/propositioner/betänkanden (→ `actions` av kind motion/proposition/betankande) och voteringar (per-ledamot → aggregerat till partinivå, kind votering), (2) `pipeline/sources/valmyndigheten.py` + government_periods kodar nationell regeringssammansättning → `responsibility` (level national), (3) `pipeline/sources/skr.py` strukturerar region/kommun-styren manuellt i `mappings.yaml` → `responsibility` (level regional/municipal). Allt rådata cachas i `data/raw/` med manifest (idempotent), endast warehouse-tabeller produceras lokalt — inget deployas i Fas 1. Designen är medvetet anpassad till den FAKTISKA repo-strukturen (flat `pipeline/`-paket, singulara schemanamn, befintlig `pipeline/sources/base.py` med `Source`/`Manifest`, `pipeline/config.py`, pip+ruff+pytest, Python 3.12 i CI / 3.14 lokalt) — INTE till `src/rosta/`-utkastet i ROADMAP.md som Fas 0 medvetet frångick.

### Task-tabell

| id | Task | Deliverable | Acceptanskriterium |
|----|------|-------------|--------------------|
| F1-T1 | Härda fetch/cache/manifest-stommen + httpx-klient (additivt ovanpå befintlig base.py) | pipeline/sources/base.py (utökad: Manifest med content_hash/http_status/content_type/source_url/params/api_version/record_count; make_client(); cache_key(); normalize_url(); idempotent fetch-grind; throttle)<br>tests/test_source_base.py (manifest-fält, sha256-stabilitet, normalize_url http→https och //→https, cache_key-determinism, idempotensgrind ger 0 nätverksanrop andra körningen) | Manifest innehåller alla DATA.md 3.2-fält; två serialiseringar av samma payload ger identisk content_hash (sha256 hex, 64 tecken)<br>normalize_url('//data.riksdagen.se/x')=='https://data.riksdagen.se/x' och normalize_url('http://data.riksdagen.se/x')=='https://data.riksdagen.se/x'<br>Andra fetch-körningen med oförändrad payload utför 0 nätverksanrop (verifierat med monkeypatchad transport som räknar anrop)<br>ruff check pipeline tests rent; befintliga test_config/test_schemas/test_scoring fortsatt gröna |
| F1-T2 | Pydantic v2-modeller Action/Responsibility som speglar de FAKTISKA schemana _(beror på F1-T1)_ | pipeline/models.py (Action, Responsibility — frozen, extra=forbid, Literal-enums)<br>tests/test_models.py (giltig Action/Responsibility OK; action utan source_ref avvisas; ogiltig party 'x' avvisas; ogiltig kind avvisas; strength>1 avvisas; .model_dump() validerar mot JSON Schema via pipeline.schema.validate) | Action(**giltig).model_dump(exclude_none=True) validerar grönt mot 'action'-schemat; Responsibility likadant mot 'responsibility'<br>party-Literal i modellerna == pipeline.config.party_codes() (test asserterar paritet, så de inte glider isär)<br>Pydantic avvisar fel enum (kind='lag', vote='kanske', level='eu', strength=1.5) med ValidationError<br>mypy/ruff rent (mypy valfritt enligt Fas 0-beslut men import måste lyckas på 3.12 och 3.14) |
| F1-T3 | Party-kodnormalisering + government_periods-källor i mappings.yaml | config/mappings.yaml (NYTT block party_code_map; government_periods kompletterat med source per rad + sluten sista period)<br>tests/test_mappings.py (party_code_map täcker alla 8 kanon-koder och innehåller fp→L; government_periods utan glapp/overlap mellan 2014-10-03 och 2026-09-13; varje period har source och giltiga partikoder) | set(party_code_map.values()) == {S,M,SD,C,V,KD,L,MP}; party_code_map['fp']=='L'; ingen råkod saknas för de 7 koder som voteringlista returnerar (s,m,c,v,kd,fp,mp) plus sd<br>government_periods sorterade: varje periods start == föregående periods end (ingen lucka), första start<=2014-10-03, sista end>=2026-05-29; varje rad har icke-tom source<br>Alla partier i parties[] (categories.yaml) som satt i regering 2014–2026 förekommer i minst en periods parties/support_parties<br>yaml.safe_load på mappings.yaml lyckas; befintligt subnational_governance-block orört av denna task |
| F1-T4 | Riksdagen-adapter: dokumentlista → actions (motion/proposition/betankande) _(beror på F1-T1, F1-T2)_ | pipeline/sources/riksdagen.py (fetch_dokument + normalize_dokument; @nasta_sida-paginering; @-attribut/sträng-tal-hantering; årschunkning vid @varning)<br>tests/fixtures/riksdagen_dokumentlista_prop_p1.json (beskuren verklig fixtur, 2 dokument + @nasta_sida)<br>tests/fixtures/riksdagen_dokumentlista_prop_p2.json (sista sidan, inget @nasta_sida)<br>tests/test_source_riksdagen.py (offline: paginering följer @nasta_sida över 2 sidor och stannar; @traffar parsas till int; normalize ger Action med kind=proposition, document_ref=dok_id, source_ref-prefix 'riksdag:'; alla rader validerar mot 'action'-schemat) | Offline-fixturtest: två sidor unioneras utan dubbletter, paginering stoppar när @nasta_sida saknas, total == @traffar<br>Varje normaliserad rad validerar mot schemas/action.schema.json; kind ∈ {motion,proposition,betankande}; source_ref börjar på 'riksdag:'<br>@-prefix och sträng-tal hanteras (int('277')); protokoll-relativa/http-URL:er normaliseras till https före nästa anrop<br>@pytest.mark.network live-smoke (manuell): dokumentlista doktyp=prop&sz=1&from=2014-01-01&tom=2014-12-31 → HTTP 200 och @traffar=='277' (verifierat 2026-05-29) |
| F1-T5 | Riksdagen-adapter: voteringlista → actions (kind=votering, per-ledamot aggregerat till partinivå) _(beror på F1-T1, F1-T2, F1-T3, F1-T4)_ | pipeline/sources/riksdagen.py (fetch_voteringar + normalize_voteringar med per-parti-majoritetsaggregering och party_code_map-översättning)<br>tests/fixtures/riksdagen_voteringlista_sample.json (beskuren verklig votering, ~30 ledamotrader täckande flera partier inkl. fp och Frånvarande)<br>tests/test_source_riksdagen.py (utökad: 349-radig fixtur → 7–8 partinivå-actions; fp→L översatt; majoritet Ja→vote=ja; ren-frånvaro→franvarande; alla validerar mot 'action'-schemat; source_ref unikt per (votering_id,party)) | Fixturtest: en votering med per-ledamot-rader aggregeras till exakt en Action per parti; partikod fp normaliseras till L, s→S osv.; vote == majoritet bland icke-frånvarande<br>Action.kind=='votering', document_ref==dok_id, period==rm, source_ref=='riksdag:votering:<id>:<PARTY>'; validerar mot schemas/action.schema.json<br>Frånvarande exkluderas från majoritetsberäkning; parti där alla ledamöter frånvarande → vote=='franvarande'<br>@pytest.mark.network live-smoke (manuell): voteringlista rm=2024%2F25&sz=400 → HTTP 200, en votering har 349 rader, parti-fält i {s,m,sd,c,v,kd,fp,mp} (verifierat 2026-05-29: 349 rader, fp förekommer) |
| F1-T6 | Valmyndigheten + Regeringskansliet → responsibility (level=national) _(beror på F1-T1, F1-T2, F1-T3)_ | pipeline/sources/valmyndigheten.py (fetch ZIP/CSV semikolon+svensk decimal; build_national_responsibility() ur government_periods)<br>config/sources.yaml (valmyndigheten.datasets kompletterad med faktiska val.se/historik.val.se nedladdnings-URL:er per val 2014/2018/2022 + verified-flagga)<br>tests/fixtures/valmyndigheten_riksdag_2022_sample.csv (beskuren semikolon-CSV, några partirader, svensk decimal)<br>tests/test_source_valmyndigheten.py (offline: semikolon+decimal-',' parsas rätt; build_national_responsibility ur en government_periods-fixtur ger en Responsibility per parti×period med level=national, role=government/support, strength∈(0,1]; validerar mot 'responsibility'-schemat) | CSV-parsning: semikolonavgränsare och decimalkomma ger korrekta numeriska partivärden (golden-test mot beskuren fixtur, ingen mojibake i åäö)<br>build_national_responsibility ger Responsibility med id ^resp:, level=='national', geography=='riket', role∈{government,support}, strength∈(0,1], source_ref börjar 'regeringskansliet:'; alla validerar mot schemas/responsibility.schema.json<br>Summan av regeringsperiodernas strength per parti är konsistent med andel av fönstret 2014-2026 partiet satt i regering (S högst, t.ex. >0.5; M/KD/L lägre)<br>@pytest.mark.network live-smoke (manuell): nedladdnings-URL för minst ett val ger HTTP 200 och en ZIP/CSV (URL:er pinnade, inte gissade); 2014/2018 dokumenterat på historik.val.se |
| F1-T7 | SKR region/kommun-styren → responsibility (level=regional/municipal), manuellt strukturerat i mappings.yaml _(beror på F1-T1, F1-T2, F1-T3)_ | config/mappings.yaml (subnational_governance ifyllt: alla 21 regioner × 3 mandatperioder med leading_parties + source; kommuner = urval eller dokumenterat pending med metod; status uppdaterad från pending_fas1)<br>pipeline/sources/skr.py (build_subnational_responsibility() läser mappings → Responsibility-rader)<br>tests/test_source_skr.py (offline: subnational_governance-fixtur → Responsibility med level∈{regional,municipal}, giltiga kanon-partikoder, strength∈(0,1], source_ref 'skr:'; varje styre har source; alla validerar mot 'responsibility'-schemat) | Alla 21 regioner har styre för var och en av perioderna 2014-2018, 2018-2022, 2022-2026, varje rad med icke-tom source och leading_parties ur kanon-koderna<br>build_subnational_responsibility ger Responsibility med level∈{regional,municipal}, geography matchar Kolada municipality-id-format (4-siffrig kommun / region-id), strength∈(0,1], source_ref börjar 'skr:'; validerar mot schemas/responsibility.schema.json<br>Inga handsatta partibetyg/omdömen i skr.py (grep: inga numeriska poäng eller party→score); all styre-data ligger i config/mappings.yaml<br>Om kommuner lämnas som urval: docs/fas1.md dokumenterar exakt vilka kommuner som täcks och varför (befolkning/representativitet), och subnational_governance.municipalities.status anger 'partial' med metod |
| F1-T8 | Transform: actions + responsibility → DuckDB-warehouse (idempotent via Parquet) _(beror på F1-T5, F1-T6, F1-T7)_ | pipeline/transform.py (build_warehouse: schema-validering per rad, Parquet-skrivning partitionerad per source, DuckDB CREATE OR REPLACE via read_parquet)<br>pipeline/fetch_fas1.py (orkestrering: --source riksdagen\|valmyndigheten\|skr, --offline, --force)<br>tests/test_transform.py (offline: blandade action+responsibility-rader laddas; count(*) FROM actions > 0 och FROM responsibility > 0; ogiltig rad → ValidationError, ingen tyst skip; andra körning = oförändrat radantal) | Efter en körning: DuckDB har tabellerna actions och responsibility; SELECT count(*) FROM actions > 0; SELECT DISTINCT source/kind visar kind∈{votering,motion,proposition,betankande} och level∈{national,regional,municipal}<br>Varje rad validerar mot sitt schema före skrivning; en injicerad ogiltig rad (party='x' eller kind='lag') gör hela laddningen hård fail med tydligt fel<br>Idempotens: andra körningen utan --force ger identiskt radantal och identisk Parquet-content_hash (test räknar)<br>git status visar inga spårade ändringar under data/ (warehouse + raw gitignorade); git check-ignore data/warehouse.duckdb träffar |
| F1-T9 | Pinna sources.yaml (dataset_ids, licenser, verified-flaggor) + network-markör + testkonvention _(beror på F1-T1, F1-T4, F1-T5, F1-T6, F1-T7)_ | config/sources.yaml (riksdagen: bekräftade query-mallar + 349-rader/fp=L-gotcha; valmyndigheten: pinnade URL:er + verified=true; skr_styren: manuell-strukturering-note + verified)<br>pyproject.toml ([tool.pytest.ini_options] markers=['network: ...'])<br>tests/conftest.py (network-markör + ev. --offline-hjälpfixtur)<br>tests/test_config.py (utökad: riksdagen/valmyndigheten har icke-tomma datasets med id; ingen källa med feeds A eller C saknar license) | yaml.safe_load(sources.yaml) OK; riksdagen och valmyndigheten har datasets[] med konkreta id/query och verified=true; ingen license-sträng tom för A/C-källor<br>Befintligt test_sources_feeds_reference_valid_categories fortsatt grönt; nytt test asserterar A/C-källors license icke-tom och dataset_ids icke-tomma efter Fas 1<br>pytest -m 'not network' samlar in och kör utan internet; pytest -m network är opt-in (markör registrerad, inga okända-markör-varningar)<br>Inga gissade licenser eller dataset-id (varje pinnat id spårbart till en verifierad endpoint i research.json eller live-anrop) |
| F1-T10 | End-to-end-verifiering, metoddok (docs/fas1.md) och fasgrindstest _(beror på F1-T8, F1-T9)_ | docs/fas1.md (verifierade endpoints + radantal, pagineringsstrategi, A/C-koppling, kända luckor, bakåtspårningskedja)<br>tests/test_fas1_gate.py (coverage/party/idempotens/source-gates)<br>körd warehouse (lokalt, gitignorad) som bevisar att Fas 1 fyller actions+responsibility för fönstret | fetch_fas1.py fyller warehouse; SELECT DISTINCT kind FROM actions ⊇ {votering,motion,proposition}; SELECT DISTINCT level FROM responsibility ⊇ {national,regional}<br>Alla 8 partier (S,M,SD,C,V,KD,L,MP) förekommer i actions; alla regeringsbärande partier i government_periods förekommer i responsibility level=national<br>test_fas1_gate.py grönt; idempotens-gate bevisar andra körning 0 nätverksanrop; source-gate bevisar 0 rader utan source_ref<br>docs/fas1.md listar de live-verifierade radantalen och pagineringsstrategin; ruff check pipeline tests + pytest -m 'not network' grönt |

### Task-detaljer

- **F1-T1 — Härda fetch/cache/manifest-stommen + httpx-klient (additivt ovanpå befintlig base.py)**: Befintliga pipeline/sources/base.py har redan Source (ABC) + Manifest (frozen dataclass) + write_cache/cache_path mot data/raw/<source>/<dataset>/<retrieved_at>.json. Komplettera UTAN att bryta gränssnittet: (1) lägg content_hash (sha256 av serialiserad payload), http_status, content_type, source_url, params och api_version till Manifest så manifestfälten matchar DATA.md sektion 3.2 (source_url, dataset_id, params, fetched_at, http_status, content_type, content_hash, license, api_version, record_count). retrieved_at behålls (ISO 8601 UTC). (2) Lägg en httpx-klientfabrik make_client(base_url) i base.py: httpx.Client(base_url=..., timeout=30, headers={'User-Agent': defaults.user_agent ur sources.yaml}, follow_redirects=True). (3) Lägg cache_key(url, params)=sha256(url+json.dumps(params,sort_keys=True)) och en idempotensgrind: om manifest med samma content_hash finns och force=False → returnera cachat utan nätverksanrop. (4) Lägg normalize_url() som tvingar // och http:// → https:// (Riksdagens @nasta_sida är http://). (5) Lägg en politeness-throttle (defaults.politeness_delay_seconds) mellan nätverksanrop. Inga partibetyg eller omdömen — endast infrastruktur.
- **F1-T2 — Pydantic v2-modeller Action/Responsibility som speglar de FAKTISKA schemana**: Lägg pipeline/models.py med frozen Pydantic v2-modeller (model_config = ConfigDict(frozen=True, extra='forbid')) Action och Responsibility som exakt speglar schemas/action.schema.json och schemas/responsibility.schema.json (singular, redan i repot). Action: id (pattern ^action:), party (Literal över de 8 versala koderna S/M/SD/C/V/KD/L/MP), kind (Literal votering\|motion\|proposition\|betankande\|budgetrad\|regeringsbeslut), category, submeasure?, period, expenditure_area?, amount_sek?, vote? (Literal ja\|nej\|avstar\|franvarande), outcome? (Literal bifall\|avslag\|unknown), document_ref?, source_ref. Responsibility: id (^resp:), party (Literal 8), level (Literal national\|regional\|municipal), geography?, period, role? (Literal government\|support\|opposition), strength (float 0–1), source_ref. Validera party-Literal mot pipeline.config.party_codes() i en test. Lägg också en EvidenceManifestRow vid behov INTE — håll Fas 1 till Action/Responsibility. Modellerna är källan som pipeline/schema.py JSON-validerar mot (dubbelspår: Pydantic internt, JSON Schema som kontrakt).
- **F1-T3 — Party-kodnormalisering + government_periods-källor i mappings.yaml**: LIVE-VERIFIERAT KRITISKT FYND (2026-05-29): Riksdagens voteringlista levererar partikoder i GEMENER och använder 'fp' för Liberalerna (Folkpartiets gamla kod ligger kvar i hela serien 2014/15–2024/25; SD förekom ej i stickprovet men finns). Modellens kanon är versala koder S/M/SD/C/V/KD/L/MP (categories.yaml). Lägg därför ett party_code_map-block i config/mappings.yaml: {s: S, m: M, sd: SD, c: C, v: V, kd: KD, fp: L, l: L, mp: MP} med kommentar om att fp==L är en historisk datakod, inte ett omdöme. Detta är en data-mappning (tillåten i config), inte ett partibetyg. Komplettera samtidigt government_periods (finns redan, fyra perioder Löfven I/II/Andersson/Kristersson 2014-10-03→null): lägg ett source-fält per rad med URL till Regeringskansliet/regeringen.se regeringsförteckning, och sätt sista periodens end till 2026-09-13 (valdatum, fönstrets slut) i stället för null så fönstret 2014–2026 är heltäckande utan glapp. Verifiera att perioderna inte överlappar och täcker hela fönstret.
- **F1-T4 — Riksdagen-adapter: dokumentlista → actions (motion/proposition/betankande)**: pipeline/sources/riksdagen.py: klass Riksdagen(Source) med name='riksdagen', license ur sources.yaml. fetch_dokument(doktyp, from_, tom): hämtar dokumentlistan (utformat=json, sz=500), pagineras via @nasta_sida (normaliserad till https) tills den saknas — INTE via gissat p+sz. Hantera @-prefixade attribut och sträng-tal (@traffar='277' → int). Vid @varning (stora träffmängder utan lista) → chunka på from/tom (år för år) och larma. Cacha varje sida som eget rådatasvar med manifest (dataset_id='dokumentlista_'+doktyp, source_url=exakt URL, record_count). normalize(): mappa varje dokument → Action: kind=motion\|proposition\|betankande (ur doktyp), party = för motioner partiet i dok-metadata (motioner har parti; propositioner=regeringen → party utelämnas/sätts via regeringssammansättning i Fas 4, INTE här), period = riksmöte eller år ur dok-datum, document_ref=dok_id, source_ref='riksdag:dok:'+dok_id. category/submeasure lämnas TOMMA i Fas 1 (taggning UO/kategori sker i Fas 4 via mappings — Fas 1 levererar råa actions med document_ref). Doktyp-koder exakt: mot/prop/bet. Endast actions, ingen scoringlogik.
- **F1-T5 — Riksdagen-adapter: voteringlista → actions (kind=votering, per-ledamot aggregerat till partinivå)**: Utöka pipeline/sources/riksdagen.py: fetch_voteringar(rm) hämtar voteringlista per riksmöte (rm URL-kodat 2024%2F25, utformat=json, sz=500, gruppering=votering). LIVE-VERIFIERAT: svaret är 1 rad PER LEDAMOT (349 rader/votering), med fält parti (gemen, fp=L), rost (Ja/Nej/Avstår/Frånvarande), votering_id, dok_id (via beteckning/punkt), avser. Pagineras (sz + p eller @nasta_sida). normalize_voteringar(): (1) gruppera rader på (votering_id, parti); (2) översätt parti via party_code_map (F1-T3) till kanon; (3) bestäm partiets röst = majoritetsröst bland icke-frånvarande ledamöter (Frånvarande räknas inte mot majoriteten, men om alla frånvarande → vote=franvarande); (4) producera EN Action per (votering_id, parti) med kind=votering, party=kanon, vote=ja\|nej\|avstar\|franvarande, document_ref=dok_id, period=rm, source_ref='riksdag:votering:'+votering_id+':'+party. outcome (bifall/avslag) hämtas ENDAST vid behov via /votering/{votering_id}/json (cachas separat) — i Fas 1 kan outcome sättas 'unknown' om enskild-votering-anropet skippas, dokumentera valet. Iterera rm över fönstrets riksmöten (2013/14–2025/26). VARNING i risker: ~15 600 voteringssidor totalt → throttle + cache, ingen aggressiv async-fan-out.
- **F1-T6 — Valmyndigheten + Regeringskansliet → responsibility (level=national)**: pipeline/sources/valmyndigheten.py: klass Valmyndigheten(Source). RESEARCH-FYND: Valmyndigheten har INGET API — endast ZIP/CSV/XLSX (semikolonseparerad, svensk decimal), och 2014/2018 ligger på historik.val.se, inte huvudsidans rådatasida (2006–2022 ZIP). fetch(): ladda ned riksdagsvalets resultat-ZIP för 2014/2018/2022 (URL:er pinnas i sources.yaml under valmyndigheten.datasets), packa upp, läs semikolon-CSV med decimal=','. normalize_valresultat(): mandatfördelning per parti och val (för transparens/evidence, validerar EJ mot action/responsibility — det är råobservation; i Fas 1 räcker att cacha + producera ett enkelt valresultat-record, det konsumeras inte av betyget direkt). HUVUDLEVERANS för C: bygg national-responsibility ur government_periods (mappings.yaml, F1-T3), INTE ur valresultatet: build_national_responsibility() läser government_periods och producerar en Responsibility per (parti, period) med level=national, geography='riket', role=government för parties resp. support för support_parties, strength = andel av fönstret perioden täcker × roll-vikt (government 1.0, support per scoring.yaml C-logik — men Fas 1 sätter bara strength=fraktion av fönster i regering; finansieringsdelen c2 är Fas 5). source_ref='regeringskansliet:'+period.name. Valresultatet är komplement/spårbarhet; regeringssammansättningen är den C-bärande responsibility-källan.
- **F1-T7 — SKR region/kommun-styren → responsibility (level=regional/municipal), manuellt strukturerat i mappings.yaml**: RESEARCH-FYND: region/kommun-styren saknar EN ren officiell maskinläsbar dataset; SKR:s sammanställning 'Styren i kommuner och regioner' efter varje val är källan men kräver MANUELL strukturering. Fyll subnational_governance-blocket i config/mappings.yaml (idag status: pending_fas1, regions:{}, municipalities:{}). Strategi för 12 års fönster utan att handsätta betyg: (a) strukturera ALLA 21 regioner per mandatperiod (2014–2018, 2018–2022, 2022–2026) med leading_parties + källhänvisning per styre (regionerna är hanterbart få och bär välfärd/vård tungt → störst betydelse för level_weights valfard:0.6 regionalt); (b) för kommuner: i Fas 1 strukturera ett representativt/befolkningstungt urval (de största kommunerna) ELLER markera municipalities som 'pending med dokumenterad metod' om full 290-kommunstäckning inte hinns — men regions SKA vara kompletta. Lägg per styre: {term, leading_parties:[kanon-koder], source:'SKR Styren ...'+år}. pipeline/sources/skr.py: klass SKR(Source) med build_subnational_responsibility() som läser subnational_governance och producerar Responsibility per (parti, geografi, term) med level=regional\|municipal, geography=region/kommunkod (Kolada/SCB-koder, t.ex. region 0001, kommun 0180), role=government, strength = andel av styret (delat jämnt mellan leading_parties eller 1.0 för enpartistyre), source_ref='skr:'+term+':'+geografi. Detta är strukturering av officiell källa i config, inte omdöme.
- **F1-T8 — Transform: actions + responsibility → DuckDB-warehouse (idempotent via Parquet)**: Implementera pipeline/transform.py (idag stub som höjer NotImplementedError). build_warehouse(rows) ska: (1) ta normaliserade dict-rader från riksdagen/valmyndigheten/skr-adaptrarna, (2) validera VARJE rad mot rätt schema (action eller responsibility) via pipeline.schema.validate INNAN skrivning — okänd/ogiltig rad = hård fail, inte tyst skip, (3) skriva Parquet under data/warehouse/<table>/ (partitionerat per source) och (4) skapa/uppdatera DuckDB-vyer/tabeller i data/warehouse.duckdb via read_parquet (CREATE OR REPLACE TABLE actions AS SELECT * FROM read_parquet(...)). Tabeller: actions (Riksdagen) och responsibility (Valmyndigheten/Regeringskansliet national + SKR regional/municipal). Idempotens: en andra körning på oförändrat rådata ger oförändrat radantal och byte-identiska Parquet-content_hash. Warehouse är gitignorad (/data/ + *.duckdb redan i .gitignore — verifierat). Lägg pipeline/fetch_fas1.py som orkestrerar fetch→normalize→build_warehouse för de tre källorna (med --source-flagga för att köra en i taget och --offline för fixtur).
- **F1-T9 — Pinna sources.yaml (dataset_ids, licenser, verified-flaggor) + network-markör + testkonvention**: Uppdatera config/sources.yaml efter live-verifiering: riksdagen.verified redan true — lägg konkreta dataset-query-mallar som är BEKRÄFTADE (dokumentlista doktyp=mot\|prop\|bet med from/tom/sz/p, voteringlista rm + gruppering, votering/{id}/json) och en gotcha-rad om att voteringlista returnerar 349 rader/votering med GEMENA partikoder (fp=L) — koppla till party_code_map. Sätt valmyndigheten.verified=true med pinnade nedladdnings-URL:er (huvudsida 2006–2022 + historik.val.se för 2014/2018) och licenssträng 'Fri med källangivelse (Valmyndigheten)'. skr_styren: lägg note att styren struktureras manuellt i mappings.yaml:subnational_governance med källa per styre; verified=true om SKR-sammanställningarna lokaliserats. Licenssträngar får ALDRIG gissas — Riksdagen='Fri vidarespridning med källangivelse (källa: Sveriges riksdag), inget SPDX' (redan i config, behåll). Lägg i pyproject.toml [tool.pytest.ini_options] markers = ['network: kräver internet'] och addopts behåll -q; dokumentera att 'pytest -m "not network"' körs offline i CI och 'pytest -m network' körs manuellt. Lägg tests/conftest.py med network-markörregistrering om markers-config inte räcker.
- **F1-T10 — End-to-end-verifiering, metoddok (docs/fas1.md) och fasgrindstest**: Knyt ihop Fas 1: kör pipeline/fetch_fas1.py mot riktig data (throttlad, cachad) och fyll warehouse. Skriv docs/fas1.md (samma djup/stil som ROADMAP.md övriga faser): verifierade endpoints med faktiska radantal (prop 2014=277, votering=349 rader, party_code_map fp=L), pagineringsstrategin (@nasta_sida, ~15600 voteringssidor → throttle+cache), de tre källornas roll (Riksdagen→A via actions, regeringssammansättning→C national, SKR→C regional/municipal), kända luckor (kommun-styren urval/pending, propositioners party tilldelas i Fas 4, outcome bifall/avslag valfritt i Fas 1), och bakåtspårning action/responsibility→source_ref→manifest. Lägg tests/test_fas1_gate.py: (1) coverage-gate — actions har minst kind votering+motion+proposition, responsibility har både national och regional rader; (2) party-gate — alla 8 kanon-partier förekommer i actions (via voteringar) och de regeringsbärande i responsibility; (3) idempotens-gate — andra körningen 0 nätverksanrop + oförändrat radantal; (4) source-gate — varje action/responsibility-rad har source_ref och spårar till ett manifest.

### Filer

- `c:/Users/marcu/Documents/GitHub/Rösta/pipeline/sources/base.py` — BEFINTLIG — utökas additivt (F1-T1): Manifest får content_hash/http_status/content_type/source_url/params/api_version/record_count; ny make_client()/cache_key()/normalize_url()/throttle + idempotent fetch-grind. Source/Manifest-gränssnittet behålls.
- `c:/Users/marcu/Documents/GitHub/Rösta/pipeline/models.py` — NY (F1-T2): frozen Pydantic v2 Action + Responsibility med Literal-enums som speglar schemas/action.schema.json + responsibility.schema.json (singular). party-Literal == config.party_codes().
- `c:/Users/marcu/Documents/GitHub/Rösta/pipeline/sources/riksdagen.py` — NY (F1-T4, F1-T5): dokumentlista (mot/prop/bet → actions) + voteringlista (per-ledamot 349 rader → partinivå-aggregering, fp→L via party_code_map). @nasta_sida-paginering, @-attribut/sträng-tal, https-normalisering, throttle.
- `c:/Users/marcu/Documents/GitHub/Rösta/pipeline/sources/valmyndigheten.py` — NY (F1-T6): ZIP/CSV semikolon+svensk decimal (inget API; 2014/2018 på historik.val.se); build_national_responsibility() ur government_periods → Responsibility level=national.
- `c:/Users/marcu/Documents/GitHub/Rösta/pipeline/sources/skr.py` — NY (F1-T7): build_subnational_responsibility() läser manuellt strukturerat subnational_governance i mappings.yaml → Responsibility level=regional/municipal. Ingen scoringlogik.
- `c:/Users/marcu/Documents/GitHub/Rösta/pipeline/transform.py` — BEFINTLIG stub → implementeras (F1-T8): build_warehouse validerar varje rad mot schema, skriver Parquet partitionerat per source, laddar idempotent till data/warehouse.duckdb (actions + responsibility) via read_parquet.
- `c:/Users/marcu/Documents/GitHub/Rösta/pipeline/fetch_fas1.py` — NY (F1-T8): orkestrering fetch→normalize→build_warehouse för riksdagen/valmyndigheten/skr; flaggor --source/--offline/--force.
- `c:/Users/marcu/Documents/GitHub/Rösta/config/mappings.yaml` — BEFINTLIG — utökas (F1-T3, F1-T7): nytt party_code_map (fp→L m.fl.), government_periods får source per rad + sluten sista period (2026-09-13), subnational_governance fylls med 21 regioner × 3 perioder + kommun-urval, källa per styre.
- `c:/Users/marcu/Documents/GitHub/Rösta/config/sources.yaml` — BEFINTLIG — pinnas (F1-T9): riksdagen bekräftade query-mallar + 349/fp-gotcha; valmyndigheten pinnade URL:er + verified=true; skr_styren manuell-strukturering-note. Inga gissade licenser/id.
- `c:/Users/marcu/Documents/GitHub/Rösta/pyproject.toml` — BEFINTLIG — additivt (F1-T9): [tool.pytest.ini_options] markers=['network: kräver internet'].
- `c:/Users/marcu/Documents/GitHub/Rösta/tests/conftest.py` — NY (F1-T9): registrerar network-markör + ev. offline-fixturhjälp.
- `c:/Users/marcu/Documents/GitHub/Rösta/tests/test_source_base.py` — NY (F1-T1): manifest-fält, sha256-stabilitet, normalize_url, cache_key-determinism, idempotensgrind.
- `c:/Users/marcu/Documents/GitHub/Rösta/tests/test_models.py` — NY (F1-T2): Action/Responsibility validering + JSON Schema-paritet + party-Literal == config.party_codes().
- `c:/Users/marcu/Documents/GitHub/Rösta/tests/test_mappings.py` — NY (F1-T3): party_code_map täckning (fp→L), government_periods utan glapp/overlap, source per rad.
- `c:/Users/marcu/Documents/GitHub/Rösta/tests/test_source_riksdagen.py` — NY (F1-T4, F1-T5): paginering, @-attribut, 349-rad→partinivå-aggregering, fp→L, schema-validering; network-smoke.
- `c:/Users/marcu/Documents/GitHub/Rösta/tests/test_source_valmyndigheten.py` — NY (F1-T6): semikolon+decimalkomma-CSV, build_national_responsibility, schema-validering.
- `c:/Users/marcu/Documents/GitHub/Rösta/tests/test_source_skr.py` — NY (F1-T7): subnational_governance → Responsibility regional/municipal, source per styre, schema-validering.
- `c:/Users/marcu/Documents/GitHub/Rösta/tests/test_transform.py` — NY (F1-T8): warehouse-laddning, schema-validering per rad, hård fail på ogiltig rad, idempotens.
- `c:/Users/marcu/Documents/GitHub/Rösta/tests/test_fas1_gate.py` — NY (F1-T10): coverage/party/idempotens/source-gates som fasgrind.
- `c:/Users/marcu/Documents/GitHub/Rösta/tests/fixtures/riksdagen_dokumentlista_prop_p1.json` — NY (F1-T4): beskuren dokumentlista, sida 1 med @nasta_sida.
- `c:/Users/marcu/Documents/GitHub/Rösta/tests/fixtures/riksdagen_dokumentlista_prop_p2.json` — NY (F1-T4): sista sidan utan @nasta_sida.
- `c:/Users/marcu/Documents/GitHub/Rösta/tests/fixtures/riksdagen_voteringlista_sample.json` — NY (F1-T5): beskuren votering med per-ledamot-rader (inkl. fp och Frånvarande).
- `c:/Users/marcu/Documents/GitHub/Rösta/tests/fixtures/valmyndigheten_riksdag_2022_sample.csv` — NY (F1-T6): beskuren semikolon-CSV med svensk decimal.
- `c:/Users/marcu/Documents/GitHub/Rösta/docs/fas1.md` — NY (F1-T10): metoddok — verifierade endpoints/radantal, pagineringsstrategi, A/C-koppling, kända luckor, bakåtspårning.

### Verifiering (körbara steg)

- Miljö (verifierat live 2026-05-29): python --version → 3.14.2 lokalt (CI-golv 3.12); python -c "import httpx,pydantic,duckdb,pandas,jsonschema,yaml" → deps ok. requires-python>=3.11, undvik 3.14-only-syntax.
- Riksdagen prop (verifierat HTTP 200): python -c "import httpx;d=httpx.get('https://data.riksdagen.se/dokumentlista/?doktyp=prop&utformat=json&sz=1&from=2014-01-01&tom=2014-12-31',timeout=30).json()['dokumentlista'];print(d['@traffar'])" → 277. @nasta_sida returneras som http:// (måste normaliseras till https).
- Riksdagen votering (verifierat HTTP 200): voteringlista rm=2024%2F25&sz=400&gruppering=votering → en votering = 349 rader; partikoder GEMENA, Liberalerna='fp'; rost∈{Ja,Nej,Avstår,Frånvarande}. Samma fp-kod i rm=2014/15. → party_code_map obligatorisk.
- Enskild votering (verifierat HTTP 200): /votering/{votering_id}/json → {"votering": {...}} application/json (för outcome bifall/avslag vid behov).
- Offline-svit: pytest -m 'not network' grönt utan internet (fixturbaserade tester för riksdagen/valmyndigheten/skr/transform/models/base/mappings).
- Live-smoke (opt-in, manuell, throttlad): pytest -m network kör endast de fyra verifierade anropen ovan; ingen aggressiv fan-out (politeness_delay + cache).
- Warehouse-bevis: python -m pipeline.fetch_fas1 (eller --offline mot fixtur) → DuckDB SELECT DISTINCT kind FROM actions ⊇ {votering,motion,proposition}; SELECT DISTINCT level FROM responsibility ⊇ {national,regional}; count(*)>0 i båda.
- Idempotens: andra körningen utan --force → 0 nätverksanrop + byte-identisk Parquet-content_hash (test räknar transport-anrop).
- Schema-paritet: varje normaliserad rad validerar mot schemas/action.schema.json resp. responsibility.schema.json via pipeline.schema.validate; ogiltig rad → ValidationError, ingen tyst skip.
- Deploy-disciplin: git check-ignore data/warehouse.duckdb och data/raw/x.json träffar; git status visar inga spårade ändringar under data/ (Fas 1 deployar inget).
- Kvalitetsgrindar: ruff check pipeline tests rent; befintliga test_config/test_schemas/test_scoring fortsatt gröna (additiva ändringar).

### Risker

- Paginering av 15 000+ sidor: voteringlistan har ~15 600 sidor i fönstret. Mitigering: paginera via @nasta_sida (aldrig gissa p+sz-tak), throttla med defaults.politeness_delay_seconds, cacha varje sida med content_hash-manifest (andra körning = 0 anrop), och hämta rm för rm (riksmöte) i stället för en enda gigantisk fråga. Ingen aggressiv async-fan-out mot riksdagen.
- @-prefixad XML-konverterad JSON: alla attribut prefixas '@' (@traffar, @nasta_sida) och tal levereras som STRÄNGAR ('277'). Mitigering: explicit attributläsning + int()-konvertering i normalize; golden-fixturtest mot beskuren verklig payload.
- Partikod-mismatch (KRITISKT, live-upptäckt): voteringlista använder gemena koder och 'fp' för Liberalerna i HELA serien 2014-2026. Mitigering: obligatorisk party_code_map i mappings.yaml (fp→L, gemen→versal), testad för fullständighet; dokumenterat som historisk datakod, inte omdöme.
- Valmyndigheten saknar API: endast ZIP/CSV/XLSX semikolon+svensk decimal, och 2014/2018 ligger på historik.val.se (inte huvudsidans 2006-2022-rådata). Mitigering: pinna nedladdnings-URL:er per val i sources.yaml, läs med decimal=',' och sep=';', golden-test på beskuren CSV (åäö ej mojibake). C-bärande responsibility byggs primärt ur government_periods, valresultatet är spårbarhetskomplement.
- SKR region/kommun-styren saknar ren maskinläsbar dataset: kräver MANUELL strukturering. Mitigering: strukturera alla 21 regioner × 3 mandatperioder komplett (regioner bär välfärd tungt och är få), kommuner som dokumenterat befolkningstungt urval om full 290-täckning inte hinns; källa per styre obligatorisk; subnational_governance.status='partial' med metod i docs/fas1.md. Detta är det enskilt mest arbetskrävande och felkänsliga momentet.
- Brå/Valmyndigheten saknar API (research-fynd): inget Brå-beroende i Fas 1 (Brå är Fas 2), men Valmyndighetens fil-beroende kräver robust nedladdning + hård fail vid 404 (inte tyst tom), och URL-uppdateringsrutin i docs.
- Propositioner saknar parti i dokumentmetadata: en proposition kommer från regeringen, inte ett enskilt parti. Mitigering: Fas 1 levererar prop-actions med document_ref men utan party; parti tillskrivs via regeringssammansättning (government_periods) först i Fas 4. Dokumenteras explicit i docs/fas1.md så det inte ser ut som en bugg.
- Layout-/namndrift mot ROADMAP-utkastet: ROADMAP Fas 1 beskriver src/rosta/ och plural-scheman, men det FAKTISKA repot är flat pipeline/ med singulara scheman och befintlig pipeline/sources/base.py (Source/Manifest). Mitigering: hela designen är skriven mot det faktiska repot; base.py utökas additivt, inte ersätts; modeller speglar singular-schemana.
- outcome (bifall/avslag) kräver extra anrop per votering: /votering/{id}/json. Mitigering: outcome får sättas 'unknown' i Fas 1 om enskild-votering-anropet skippas (dokumenterat val); kan berikas senare utan att bryta schemat (outcome är optional).
- Python 3.14 lokalt vs 3.12 i CI: undvik 3.14-only-syntax; kör ruff/pytest mot requires-python>=3.11; verifiera att Pydantic/httpx/duckdb-versionerna i pyproject fungerar på båda.

### Exit-kriterium (DoD)
Fas 1 är klar när: (1) actions (Riksdagen — voteringar aggregerade till partinivå med korrekt party_code_map fp→L, samt motioner/propositioner/betänkanden) och responsibility (regeringssammansättning level=national ur government_periods + SKR region/kommun-styren level=regional/municipal ur manuellt strukturerat subnational_governance) är laddade i data/warehouse.duckdb och varje rad validerar mot schemas/action.schema.json resp. responsibility.schema.json; (2) alla dataset_ids, query-mallar och licenssträngar är pinnade och verified i config/sources.yaml utan gissningar, och party_code_map + government_periods (med source per rad, sluten 2014-10-03→2026-09-13) + subnational_governance (21 regioner × 3 perioder med källa per styre; kommuner komplett eller dokumenterat partial) är ifyllda i config/mappings.yaml; (3) fetch/cache/manifest-stommen i pipeline/sources/base.py är härdad (content_hash, alla DATA.md 3.2-manifestfält, https-normalisering, idempotensgrind) så Fas 2 inte behöver dubbla den; (4) pytest -m 'not network' är grönt offline med golden-fixturer för paginering, @-attribut, 349-rad-aggregering och semikolon-CSV, idempotens-gate bevisar 0 nätverksanrop vid omkörning, source-gate bevisar 0 rader utan source_ref, och ruff check är rent; (5) docs/fas1.md dokumenterar de live-verifierade endpoints/radantalen, pagineringsstrategin, A/C-kopplingen och kända luckor (kommun-urval, prop-parti i Fas 4, outcome valfritt); (6) deploy-splitten är intakt — inget rådata/warehouse spåras i git (data/ + *.duckdb gitignorade). Allt på en branch, ej pushat utan begäran.

---

## Fas 2 — SCB + Brå (inkl. NTU) + Kolada → observations (bredaste resultatkällorna)

### Mål
Tre källadaptrar (SCB PxWeb v2, Kolada v3, Brå/NTU fil+SOL) hämtar rådata till Lager 1 (raw+manifest), normaliserar till tidy `observations` som validerar mot `observation(s).schema.json`, och laddas idempotent i `data/warehouse.duckdb`. Fyller objektiva D-resultatindikatorer (+ behovsbild för B) för **ekonomi, välfärd, trygghet, integration** och delar av **demokrati**. Ingen A/B/C/D-scoringlogik (Fas 4–5).

### Task-tabell

| id | Task | Deliverable | Acceptanskriterium |
|----|------|-------------|--------------------|
| F2-T0 | Förankra kontrakt + stäng Fas 0/1-luckor | `_client.py`/`cache.py`/`models.py` om de saknas; `pyproject.toml`/`.gitignore` om saknas | `import pipeline, pipeline.sources` OK; ruff/mypy 0 fel; `Observation.model_json_schema()` = required i schema; `git check-ignore data/raw` träffar, `dist/scores.json` ej |
| F2-T1 | Pinna SCB/Kolada/Brå i `sources.yaml` (live-verifierat) | tre källblock + `datasets[]` | YAML parsar; varje `datasets[].indicator` finns i `categories.yaml`; SCB `license=='CC0-1.0'`+`'Källa: SCB'`; Kolada `/v3`; Brå `source_type!='rest_api'`; ingen gissad licens |
| F2-T2 | SCB-adapter (PxWeb v2: metadata→POST→json-stat2) | `sources/scb.py` | KPI/KPIF-fixtur → `indicator=='inflation'`, rätt period; live KPI-TAB HTTP 200 + 64-hex content_hash; alla obs validerar; ≤30 anrop/10s |
| F2-T3 | Kolada-adapter (v3, kommun/region) | `sources/kolada.py` | N00003 Stockholm 2020–2022 → 3 obs, geography `0180`; `next_url`-paginering union utan dubblett; `isdeleted` exkluderas; gender `T`; `/v3` |
| F2-T4 | Brå/NTU-adapter (fil + SOL, ISO-8859-1) | `sources/bra.py` | Excel/CSV-fixtur → `dodligt_vald` rätt period; SOL-HTML dekodas ISO-8859-1 (åäö ej mojibake); 404 = hård fail, ej tyst tom |
| F2-T5 | Ladda till warehouse (DuckDB via Parquet) | `transform.py` | `count(*) FROM observations > 0`; `DISTINCT source`={scb,kolada,bra}; omkörning oförändrat radantal; inga NULL/okänd indicator; warehouse gitignorad |
| F2-T6 | Offline-fixturer + `network`-markör | `tests/fixtures/*`, `tests/conftest.py` | `pytest -m 'not network'` grönt utan internet; SOL-fixtur verifierat ISO-8859-1 |
| F2-T7 | Indikator↔dataset-mappning i config | mappningsfält i `sources.yaml` el. `mappings.yaml:indicator_sources` | grep efter `'arbetsloshet'` i `sources/*.py` → 0 träffar utanför kommentar; varje (kategori,submått,indikator) finns i `categories.yaml` |
| F2-T8 | Testsvit (schema, config, normalisering, idempotens) | `tests/test_*.py` | `pytest -m 'not network'` grönt, coverage ≥80%; schema-kontraktstest failar vid brott |
| F2-T9 | End-to-end + metodnotering | `pipeline/fetch_fas2.py`, `docs/fas2.md` | körning fyller warehouse; docs listar ≥1 täckt indikator i ekonomi/valfard/trygghet/integration; SCB+Kolada täcker 2014–2026 för pinnade indikatorer |

### Filer
`config/sources.yaml`, `config/mappings.yaml`, `pipeline/sources/{scb,kolada,bra}.py`, `pipeline/{_client,cache,models,transform,fetch_fas2}.py`, `tests/fixtures/{scb_kpi_jsonstat2.json,kolada_n00003.json,kolada_paginated_p1.json,kolada_paginated_p2.json,bra_dodligt_vald.csv,bra_sol_sample.html}`, `tests/conftest.py`, `tests/test_*.py`, `docs/fas2.md`.

### Verifiering
```bash
uv run python -c "import pipeline, pipeline.sources"
uv run ruff check pipeline tests && uv run mypy pipeline
uv run pytest -m "not network" --cov=pipeline           # ≥80% på scb/kolada/bra + transform
uv run pytest -m network                                # live: SCB /config CC0, Kolada N00003, Brå SOL ISO-8859-1
python -m pipeline.fetch_fas2
# DuckDB: SELECT source, count(*) FROM observations GROUP BY source  → scb/kolada/bra
```

### Risker
- SCB v2 ligger under `v2beta`-path → pinna både v2beta och v1-fallback; larma om `/config` inte svarar.
- SCB full-text-sök matchar löst → pinna exakta TAB-id via `/metadata`, sök aldrig vid körning.
- SCB rate-limit 30/10s + 150000 celler/IP → sekventiell throttle + Tid-chunking + cache, inte parallell fan-out.
- Kolada saknar formell SPDX → dokumentera attribution-required (Kolada/RKA + SCB), gissa aldrig CC0.
- Brå har inget API → filberoende, hård fail vid 404, explicit kolumnmappning (inte heuristik), manuell URL-uppdateringsrutin i docs.
- Brå SOL = ISO-8859-1 → explicit dekodning + golden-test.
- json-stat2-parsning icke-trivial → metadata-driven kodlösning, golden-test på beskuren verklig fixtur.
- Indikator↔dataset bär implicit omdöme → all mappning i config + cross-check-test, proxyval dokumenteras.

### Exit-kriterium (DoD)
`sources.yaml` pinnar SCB (v2, CC0, exakta TAB-id), Kolada (v3, attribution), Brå/NTU (file_download/SOL, ISO-8859-1), datasets mappade, inga gissade licenser; tre adaptrar hämtar→cachar→normaliserar till `observations` som alla validerar; inga hårdkodade indicator-namn; `transform.py` laddar idempotent till warehouse; `pytest -m "not network"` grönt ≥80% coverage; live end-to-end fyller warehouse för ekonomi/valfard/trygghet/integration 2014–2026, dokumenterat i `docs/fas2.md` med verifierade endpoints och kända luckor (Brå-filberoende, återstående submått → Fas 3).

---

## Fas 3 — Sektorsmyndigheter + evidensliggare: återstående D-indikatorer + B-evidens

### Mål
Källmoduler för sektorsmyndigheterna (Socialstyrelsen, Skolverket, Naturvårdsverket via SCB MI0107, Energimyndigheten, Svenska kraftnät/eSett, Försvar via UO6+ÅR-proxy, Statskontoret/Riksrevisionen/SOM) **samt** evidens-/utvärderingskällorna (IFAU, SBU, Vårdanalys, Skolforskningsinstitutet, FOI, Klimatpolitiska rådet m.fl.). Resultat: (1) varje Fas-3-ägt submått får ≥1 observationsserie i warehouse, och (2) `config/evidence_ledger.yaml` fylls med ≥3 källbackade `evidence_effect`-poster per kategori (≥21 totalt). Inga claims/effects/betyg (Fas 4/5).

### Task-tabell

| id | Task | Deliverable | Acceptanskriterium |
|----|------|-------------|--------------------|
| T3.0 | Gap-matris + pinna prerequisites | `pipeline/tools/coverage_report.py`, `sources.yaml` Fas-3-block, `docs/fas3_coverage.md` | coverage_report listar (kategori,submått,indikator,har_observation); varje källa har base_url/datasets/license(verifierad)/api_version/rate_limit; svaga submått flaggade proxy |
| T3.1 | Återanvändbar PxWeb-klient + json-stat2-parser | `sources/_pxweb.py`, `sources/_jsonstat.py`, test | auto-chunk >150000 celler i flera POST; parse på MI0107-fixtur ger rätt radantal; ingen nätverkstrafik i CI (mockad transport) |
| T3.2 | Socialstyrelsen → valfard D | `sources/socialstyrelsen.py`, `mappings.yaml:indicator_sources`, fixtur, test | ≥3 valfard-submått har obs; manifest med content_hash + verifierad license; idempotent (0 nätverksanrop omkörning) |
| T3.3 | Skolverket (api + SiRiS-fallback) → valfard & integration | `sources/skolverket.py`, mappings, fixturer, test | obs för skolresultat+behoriga_larare+sfi_sprakkunskaper; CSV semikolon+svensk decimal; saknad pToken → WARN+skip, ej krasch |
| T3.4 | Naturvårdsverket via SCB MI0107 → klimat | `sources/naturvardsverket.py`, mappings, fixtur, test | territoriell utsläppsserie 2014→senaste år (`kalla='naturvardsverket'`); chunkar; senaste år i manifest; konsumtionsbaserade ifyllt el. flaggat svagt |
| T3.5 | Energimyndigheten (PxWeb) → klimat | `sources/energimyndigheten.py`, mappings, fixtur, test | fossil_energianvandning-serie; tabellväg via `navigate()` pinnad (ej gissad); json-stat2 + celltak + throttle |
| T3.6 | El: Svk Mimer + eSett (datumdelad) → klimat | `sources/el.py`, mappings (`cutover_date`), fixturer, test | stitchad serie kontinuerlig över 2025-03-18 utan dubbel/lucka; eSett-paths "verifierad via Swagger <datum>"; degraderar+WARN om en källa nere |
| T3.7 | Försvar (UO6/BNP + ÅR-proxy) → forsvar | `sources/forsvar.py`, `mappings.yaml:forsvar_proxies`, test | andel-av-BNP korrekt mot syntetiskt facit; varje proxy `is_proxy=true`+source_ref; sekretessbegränsade submått flaggade svaga; `level_weights national:1.0` respekteras |
| T3.8 | Institutioner (SOM + Statskontoret) → demokrati & integration | `sources/institutioner.py`, mappings, fixtur, test | fortroende + tillit_valdeltagande har serier; SOM-obs `confidence_hint='low'` + tabellref; svaga demokrati-indikatorer flaggade |
| T3.9 | **Evidensliggaren (B)** — seed + maskineri (Fas 4b). Utbyggd 2026-05-30 till **30 källverifierade poster, ≥3/kategori (alla 7)** (29 + `ny_karnkraft` via Fas 4c) via research-workflow (URL-bekräftade officiella källor; stickprov manuellt). Version 0, AI-utkast → expertgranskning återstår före B aktiveras | validerar (`tests/test_fas4.py`): kanonisk indikator + källa + giltiga etiketter; ≥3/kategori; endast allowlist-org |
| T3.10 | Transform-integration + warehouse | `models.py` (Observation/EvidenceEffect), `transform.py`, `run_fas3.py`, test | `run_fas3.py --only socialstyrelsen` laddar utan fel; okänd kategori/indikator avvisas; alla Fas-3-källor i `GROUP BY kalla`; Parquet partitionerat |
| T3.11 | Fasgrindstest | `tests/test_fas3_gate.py`, `docs/fas3_coverage.md` (allowlist) | coverage-gate + evidence-gate + idempotens-gate gröna; varje Fas-3-submått är `har_observation` ELLER i allowlist; andra körningen 0 nätverksanrop |

### Filer
`config/{sources,mappings,evidence_ledger}.yaml`, `schemas/evidence_ledger.schema.json`, `pipeline/sources/{_pxweb,_jsonstat,socialstyrelsen,skolverket,naturvardsverket,energimyndigheten,el,forsvar,institutioner}.py`, `pipeline/{evidence,models,transform,run_fas3}.py`, `pipeline/tools/coverage_report.py`, `docs/fas3_coverage.md`, `tests/fixtures/*`, `tests/test_*.py`.

### Verifiering
```bash
python pipeline/tools/coverage_report.py                     # gap-matris före/efter
uv run pytest tests/test_source_*.py tests/test_pxweb_client.py -q   # offline
uv run pytest tests/test_source_el.py -q                     # skarv 2025-03-18 utan lucka/dubbel
uv run pytest tests/test_evidence_ledger.py -q             # ≥3/kategori, source_ref, allowlist
python pipeline/run_fas3.py                                  # SELECT kalla, COUNT(*) FROM observations GROUP BY kalla
uv run pytest tests/test_fas3_gate.py -q
uv run ruff check && uv run mypy pipeline && uv run pytest -q
git status                                                   # inga ändringar under data/ eller dist/
```

### Risker
- Sekretess på försvarets operativa förmåga → endast proxy (anslag/personal/ÅR), `is_proxy=true`, låg confidence, allowlist; modellen redovisar luckan.
- El-källans datumdelning (Mimer ≤2025-03-18, eSett efter) → dedikerat skarvtest, pinnad cutover, dedup, degradering+WARN.
- SiRiS långsam (~30s) + pToken expirerar → föredra `api.skolverket.se`, cache+throttle, token-skip utan krasch.
- Demokrati svagast täckt → SOM (akademisk, tillåten enligt CLAUDE.md) med `confidence_hint='low'`, svaga gap allowlistas.
- MI0107 uppdateras nov/dec → sista helår kan vara 2024; gate kräver "senaste tillgängliga", inte 2026.
- Licenssträngar får ej gissas → verifiera live, skriv i sources.yaml + manifest; test kräver icke-tom license.
- Evidensliggaren kan smuggla in omdöme → source_ref-krav, org-allowlist, schema, versionsstyrt i git.
- Risk att dubblera Fas 2 (Kolada↔välfärd) → T3.0 coverage_report kör först; `personalomsattning_omsorg` dokumenteras Socialstyrelsen **eller** Kolada-komplement, inte båda blint.

### Exit-kriterium (DoD)
Varje Fas-3-ägt submått (valfard vård/skola/omsorg, klimat utsläpp/energi/el, forsvar anslag/personal-proxy, integration sfi/skolresultat, demokrati förtroende/medier) har ≥1 observationsserie 2014→senaste år **eller** är explicit i allowlistan (hotade_arter, delar av militär förmåga) — inget tyst gap, bevisat av coverage-gate; `evidence_ledger.yaml` har ≥3 evidence_effect/kategori (≥21), alla med source_ref, validerade; varje källa har fetch/normalize + manifest (verifierad license) + idempotent cache, laddat via transform; ruff/mypy/pytest gröna, offline kräver inget nät; inget rådata/warehouse deployas (`data/` gitignorad).

---

## Fas 4 — Claims/effects engine: gör B granskningsbar (Lager 3)

### Mål
Deterministiskt mellanlager: omvandla warehouse-tabellerna (`observations`, `actions`, `responsibility`) + evidensregistret till (1) normaliserade källbackade **claims** och (2) aggregerade **indicator_effects** per (parti, kategori, indikator). Alla tolkningsregler i `config/claims.yaml` + `config/mappings.yaml`; ingen kod innehåller handsatt omdöme. Output stannar lokalt (`data/claims/*.parquet` + DuckDB); endast bantad indexering lyfts i Fas 5/6.

### Task-tabell

| id | Task | Deliverable | Acceptanskriterium |
|----|------|-------------|--------------------|
| F4-T1 | Pydantic v2 `Claim`/`IndicatorEffect` (frozen, extra=forbid) | `pipeline/models.py` | giltigt claim valideras, claim utan `source_refs` avvisas; enums = `claims.yaml`; frozen |
| F4-T2 | `interpretation_rules` i `claims.yaml` (action→claim, votering→direction, target, evidens→evidence_effect) | utökad `claims.yaml` | varje regel unikt `rule_id`; inga partikoder i regler; befintliga sektioner oförändrade; `target_resolution` definierad |
| F4-T3 | Fas-4-nycklar i `mappings.yaml` (UO→kategori, `action_magnitude_bands`, `target_levels`) | utökad `mappings.yaml` | laddas utan fel; `target_levels` täcker alla `direction=target`-indikatorer; varje target_level har `source` |
| F4-T4 | Config-loader + korsvalidering | `pipeline/config_loader.py` | loaders OK mot incheckad config; brutet test-config → `ConfigError` som namnger saknad indikator |
| F4-T5 | `claims.py` byggare (5 claim-typer) | `pipeline/claims.py` | fixtur → exakt förväntad ClaimSet (golden); varje claim har source_ref+rule_id; källlös rad → inget claim; deterministisk claim-id |
| F4-T6 | `effects.py` aggregering | `pipeline/effects.py` | golden net_support/confidence inom 1e-6; `net_support∈[-1,1]`,`confidence∈[0,1]`; `expected_direction`=`categories.yaml`; <3 claims sänker confidence |
| F4-T7 | JSON Schema (härledda ur Pydantic) + validering | `schemas/{claim,indicator_effect}.schema.json`, `pipeline/{gen_schemas,schema}.py` | `gen_schemas.py` → `git diff` tom; korrupt claim avvisas; `check_schema` passerar |
| F4-T8 | Persistens (Parquet+DuckDB+manifest) | `pipeline/{persist_claims,claims_engine}.py` | engine skapar `claims.parquet`/`indicator_effects.parquet`/`_manifest.json`; två körningar = identisk content_hash; `count(*) FROM claims`=manifest |
| F4-T9 | Testsvit (golden/property/config/schema/idempotens) | `tests/fixtures/mini_warehouse/`, `tests/test_*.py` | `pytest` grönt; sex testfiler samlas in; byte-stabilt över två körningar |
| F4-T10 | `pyproject.toml`+uv+ruff/mypy (additivt) | `pyproject.toml`, `uv.lock` | `uv sync` OK; ruff/format/mypy rena |
| F4-T11 | Metoddok (granskningsbarhet B) | `docs/fas4_claims_effects.md` | genomräknat net_support-exempel = golden-test; varje regelfamilj med rule_id; bakåtspårning score→effect→claim→source_ref→manifest |

### Filer
`pipeline/{models,config_loader,claims,effects,gen_schemas,schema,persist_claims,claims_engine}.py`, `config/{claims,mappings}.yaml` (additivt), `schemas/{claim,indicator_effect}.schema.json`, `tests/fixtures/mini_warehouse/`, `tests/test_{config_claims,claims_builder,effects,schema_contract,idempotens}.py`, `pyproject.toml`, `uv.lock`, `docs/fas4_claims_effects.md`.

### Aggregeringsmatte (från `claims.yaml`)
```
raw = Σ_supporting (evidence_level_weight · effect_strength_num · confidence_num · signed_direction)
    − Σ_contradicting (samma)
net_support = clamp(raw / Σ|weights|, -1, 1)
confidence  = viktat medel av confidence_num, nedjusterat om n_claims < min_claims_for_high_confidence (=3)
expected_direction = från categories.yaml  (net_support>0 ⇒ mot kategorins positiva riktning)
target-indikatorer: net_support via target_resolution (mot målnivå, icke-monotont)
```

### Verifiering
```bash
uv run python -c "import pipeline.models, pipeline.claims, pipeline.effects, pipeline.config_loader"
uv run python -c "from pipeline.config_loader import load_claims_config, load_mappings, load_categories; load_claims_config(); load_mappings(); load_categories(); print('config OK')"
uv run python pipeline/gen_schemas.py && git diff --exit-code schemas/      # 0 drift
uv run pytest -q
uv run python -m pipeline.claims_engine --warehouse tests/fixtures/mini_warehouse   # claims.parquet + indicator_effects.parquet + _manifest.json
# kör två ggr → identisk content_hash i data/claims/_manifest.json
uv run ruff check pipeline tests && uv run mypy pipeline
git status                                                                   # inga spårade filer under data/
```

### Risker
- Beror på warehouse-scheman + evidensregister (Fas 1–3) → driv allt mot `mini_warehouse`-fixtur; byt bara fixturkälla när riktiga tabeller finns.
- Tolkningsreglerna bär all subjektivitet → partineutrala (test: inga partikoder), rule_id, källhänvisade target_levels, inga magiska tal.
- `direction=target` passar inte monotona matten → explicit `target_resolution` + golden-test som täcker en target-indikator.
- Flyttalsobestämdhet → fast avrundningsprecision, stabil sortering före hash, ren Python-aritmetik, idempotens-test.
- Tunn B (få evidence_effect per parti×kategori) är korrekt (Fas 5 → 2.5) men ser ut som bugg → engine loggar coverage i `_manifest.json`.
- Scope-glidning mot Fas 5/dist → Fas 4 stannar vid indicator_effects i warehouse/Parquet.
- Delat ägarskap `mappings.yaml` Fas 1↔4 → Fas 4 lägger endast avgränsade kommenterade block.

### Exit-kriterium (DoD)
Engine bygger deterministiskt claims + indicator_effects ur Lager 2 + evidensregister med exakt `claims.yaml`-matten och `expected_direction` ur `categories.yaml`; varje claim har ≥1 source_ref + rule_id mot versionsstyrd regel (inga källlösa omdömen i kod, testat); output validerar mot Pydantic-härledda JSON Schema (gen_schemas==incheckat); `pytest` grönt inkl. golden (för hand räknat), property, config-konsistens och idempotens (byte-identisk content_hash); ruff/format/mypy rena; Lager 3-output endast lokalt (ej spårat i git); `docs/fas4_claims_effects.md` dokumenterar bakåtspårningskedjan.

---

## Fas 4c — B-differentiering: verifierar-harmonisering (Plan B) + omstridda åtgärdstyper (Plan A)

> **Status: Steg 0 ✅ · Plan B ✅ · Plan A ✅ — 2026-05-30, design i samråd (Codex-konsensus). KRÄVER mänsklig slutgranskning.**
> Steg 0: rubrik fryst ([fas4c_rubrik.md](fas4c_rubrik.md)), negativ-grind + generaliserad exkludering testtvingade ([tests/test_fas4c.py](../tests/test_fas4c.py)). Plan B: 19 åtgärdstyper × 8 partier panel-harmoniserade (289 agenter), 109 non-klimat-rader admitterade + 14 klimat bevarade; audit + rejected-log i [fas4c_planB_audit.md](fas4c_planB_audit.md); M/L-asymmetrin rättad. Plan A: 8 omstridda instrument systematiskt evidens-skannade ([fas4c_planA_kandidatregister.md](fas4c_planA_kandidatregister.md)) — **bara 1 passerade grindarna** (`ny_karnkraft` → effektbrist, Svenska kraftnät; 7 inerta pga blandad evidens, inkl. a-kassa stoppad av negativ-grinden). 7 partirader för ny_karnkraft → **130 rader totalt**. Ranking (med kärnkraft): **S 3.72 · L 3.39 · MP 3.34 · M 3.30 · KD 3.12 · V 2.59 · SD 2.41 · C 2.39**; känslighetsanalys ±0.08 (måttlig); 0 admitterade negativ-riktnings-poster; determinism verifierad. Flaggat för granskning: 4 propositionsavslags-opposes (Plan B) + ny_karnkraft (laddad energifråga).
>
> Bakgrund: delpoäng B (vikt 0,35) särskiljer i dag partierna svagt — endast 12 av 111 ståndpunkter är `opposes`, resten konsensus, koncentrerat till ekonomi (5) och klimat (5). B kan bara väga åtgärdstyper som (a) finns i evidensliggaren och (b) har riktad officiell evidens; de kodbara åtgärdstyperna per kategori är få (ekonomi 2, valfard 4, trygghet 4, klimat 2, integration 4, forsvar 2, demokrati 3). Två spår höjer B:s kvalitet **utan att bryta no-fabrication-garantin**.
>
> **Ordning (Codex-gated): Steg 0 rubrik → Plan B (harmonisera befintliga) → Plan A (utöka liggaren).** Att utöka FÖRE harmonisering skulle baka in befintliga verifierar-asymmetrier i en större coverage-nämnare. *(OBS: "Plan A/B" = användarens förslagslista, INTE delpoäng A/B.)*

### Steg 0 — Frys rubriken (gemensam för båda spåren)
**Deliverable:** `docs/fas4c_rubrik.md` — en FÖRREGISTRERAD, oföränderlig-under-körning rubrik som kodifierar:
- **Instrument-/stance-regeln** (instrument-exakt, metoddoc §4) + **bunten-regeln**: en motion som buntar flera instrument räknas för det namngivna instrumentet om citatet är instrument-exakt; intern nyans → `mapping_note`, används ALDRIG för att förkasta raden.
- **Källhierarki** + regel för **enskild motion** (single-member): får representera partilinje endast som `confidence: low`, annars utelämnas. Beslut låses här.
- **Negativ-riktnings-grinden (Codex P0):** en `direction: negative`-liggarpost får bidra till B endast om `evidence_level ∈ {authority_evaluation, systematic_review}`, `confidence ≥ medium`, OCH evidensen avser **exakt den betygsatta indikatorn** (ingen sidoeffekt-proxy). Varje indikator-brygga (t.ex. IFAU "arbetslöshetstid" → indikator `arbetsloshet`) måste skrivas ut, källbeläggas och granskas explicit.
- **Generaliserad exkluderingsregel**: ersätt ad hoc-undantaget `internationella_materielsamarbeten` med en principiell regel för när en policy_type lyfts ur coverage-nämnaren.
- **Inget täckningsmål** (no target coverage rate) — harmonisering/utökning får aldrig styras mot en önskad andel kodade rader.

**Acceptans:** `tests/test_fas4c.py` asserterar att varje `direction: negative`-post i liggaren passerar negativ-grinden och att exkluderingsregeln är generell (ingen hårdkodad policy_type-lista i koden utan motsvarande regel-skäl).

### Plan B — Panel-harmonisering av de 111 befintliga raderna
**Mål:** ta bort isolerings-inducerade asymmetrier (det dokumenterade M/L-fallet på `subventionerade_anstallningar`). Re-verifiera **per policy_type som en panel** — alla 8 partiers kandidatkällor bedöms SIDA VID SIDA under Steg 0-rubriken — i stället för rad-för-rad i isolering.

| id | Task | Acceptanskriterium |
|----|------|--------------------|
| B1 | Per kodbar policy_type: samla varje partis bästa instrument-exakta kandidatkälla (återanvänd research-workflow mot data.riksdagen.se). Behåll **förkastade kandidater med skäl** (de gamla verdikten finns ej kvar på disk → byggs om). | rejected-candidate-log finns per policy_type |
| B2 | Två-stegs bedömning mot groupthink/utjämningstryck: (1) första-pass mot rubriken per rad, (2) sida-vid-sida-harmonisering per policy_type. | varje keep/add/drop loggas per (parti, policy_type) |
| B3 | Tillämpa "harmonisera STANDARDEN, inte slutsatsen": om rubriken kräver att en rad DROPPAS i stället för att en analog adderas, gör det. Inget täckningsmål. | audit visar symmetrisk regeltillämpning |
| B4 | Skriv harmoniserad `party_positions.yaml` + `docs/fas4c_planB_audit.md`. Bump status. | no-fabrication-gate (test_fas4) grönt |
| B5 | Bygg om pipeline; jämför ranking före/efter; dokumentera. | `scorerun` reproducerar; diff redovisad |

### Plan A — Utöka liggaren med omstridda, evidens-belagda åtgärdstyper
**Mål:** höj B:s särskiljningsförmåga. **Kandidat-register FÖRST** (systematisk skanning per kategori), SEDAN filter — aldrig börja från de politiska striderna och leta evidens i efterhand (Codex P0 mot cherry-picking).

| id | Task | Acceptanskriterium |
|----|------|--------------------|
| A1 | `docs/fas4c_planA_kandidatregister.md`: per kategori systematisk lista över instrument partierna driver, oavsett om de särskiljer. Märk: contested? officiell riktad evidens på kategori-indikator? | varje kategori skannad; källor noterade |
| A2 | Filtrera till intersektionen **contested ∧ officiellt-evidensbelagd**. Värdekonflikter utan riktad officiell evidens (eller mixed/unclear → inert) **utelämnas**; loggas i inert/exkluderad-liggaren med skäl + disclosure att B mäter "evidens-kodbar instrumentell träffsäkerhet", inte all viktig politik. | inert/exkluderad-lista publicerad |
| A3 | Per kvalificerad kandidat: lägg evidensliggar-post (officiell svensk källa, URL-bekräftad, exakt-indikator); negativ riktning → passera negativ-grinden. **Verifiera varje evidensfynd** (Codex verifierade INTE de svenska fynden). | varje post källbelagd + grind-godkänd |
| A4 | Koda partiståndpunkter för de nya policy_types under SAMMA panel-rubrik (Plan B-metod). | adversariellt verifierade, confirmed=true |
| A5 | Bygg om; **känslighetsanalys**: ranking (i) med/utan nya omstridda instrument, (ii) med negativ-riktnings-instrument borttagna. | robusthet redovisad |

**Kandidat-skiss** (villkorad på att evidensen håller vid A3-verifiering): ekonomi a-kassenivå/-varaktighet (IFAU; negativ på `arbetsloshet` — kräver brygg-kodifiering), klimat ny kärnkraft (Energimyndigheten/Svk; `fossil_energianvandning`/`effektbrist`), valfard vårdval/LOV (Vårdanalys/Riksrevisionen; dela tillgänglighet vs likvärdighet), trygghet visitationszoner/skärpta straff (Brå; trolig svag/mixed → sannolikt inert), integration bidragstak/kvalificeringstid (IFAU/ESO; tight instrument-matchning).

### Filer
`docs/fas4c_rubrik.md` (NY), `docs/fas4c_planB_audit.md` (NY), `docs/fas4c_planA_kandidatregister.md` (NY), `config/party_positions.yaml` (harmoniseras + nya rader), `config/evidence_ledger.yaml` (nya poster + generaliserad exkludering), `config/scoring.yaml` (exkluderingsregel generaliseras), `docs/fas4b_partistandpunkter_metod.md` (uppdateras: rubrik + negativ-grind), `tests/test_fas4c.py` (NY), `tests/test_fas4.py` (uppdateras).

### Risker (Codex-identifierade)
- **Cherry-picking** omstridda instrument för att de särskiljer → kandidat-register FÖRST, filter sedan.
- **Negativ evidens mappad till fel/närliggande indikator** → exakt-indikator-grind; brygga skrivs ut + granskas.
- **Ad hoc-exkludering** av negativa instrument → generaliserad regel.
- **Enskild motion som partilinje** → låst regel (low confidence eller utelämna).
- **Coverage-inflation** via svaga buntade rader → samma standard, inget täckningsmål, rejected-log.
- **Panel-groupthink / utjämningstryck** → första-pass mot rubrik FÖRE sida-vid-sida; alla beslut loggas.

### Exit-kriterium (DoD)
Steg 0-rubriken fryst och testtvingad (negativ-grind); de befintliga icke-klimat-ståndpunkterna panel-harmoniserade (109 admitterade, 14 klimat bevarade) med per-(parti,policy_type) add/drop/keep-audit och bevarad rejected-log (Plan B); inert/exkluderad-liggare publicerad med skäl; Plan A-kandidatregister byggt FÖRE scoring, endast intersektionen contested∧evidensbelagd admitterad, varje ny liggar-post officiellt källbelagd och (vid negativ riktning) godkänd av negativ-grinden; alla nya partirader kodade under samma panel-rubrik; pipeline reproducerar med känslighetsanalys (med/utan nya instrument; med/utan negativa); pytest + no-fabrication-gate grönt; allt version-bumpat och dokumenterat. **Mänsklig slutgranskning kvarstår** innan skarp betygsättning.

---

## Fas 5 — Scoring engine: A/B/C/D, kategoribetyg 0–5 med osäkerhet, dist-artefakter, golden tests

> **Implementeringsnotis (A):** A = *relativ prioritering* — andel av partiets egna motioner som rör kategorin (rank-normaliserad), inte rå motionsvolym. Det hindrar stora partier från att bli höga i varje kategori. Se [DATA.md §4](../DATA.md) och `config/scoring.yaml`.

### Mål
Deterministisk scoringmotor: omvandla Fas 4:s claims + indicator_effects (+ observations/actions/responsibility) och config (`scoring.yaml`, `categories.yaml`, `claims.yaml`, `mappings.yaml`) till per-parti×kategori-betyg 0–5 med A/B/C/D-komponenter och osäkerhetsintervall, och skriv de **två** deploy-artefakterna `dist/scores.json` + `dist/evidence.json` — schemavaliderade (Draft 2020-12) och låsta av golden tests. Ingen logik eller tröskel utanför config.

### Task-tabell

| id | Task | Deliverable | Acceptanskriterium |
|----|------|-------------|--------------------|
| 5.0 | **Frys scoringkontraktet** + två mattbeslut | `docs/scoring-method.md` (utkast), kommentar i `scoring.yaml`, INTERFACE-sektion i `score.py` | input-kontrakt definierat; **A/C = cross-party minmax, B/D = absolut** låst; degenererat fall → neutral 2.5; inga nya trösklar |
| 5.1 | Körbart skelett (additivt om Fas 0 finns) | `pyproject.toml`, `pipeline/__init__.py`, `tests/__init__.py`, `.gitignore` (dist/ ignoreras men `dist/.gitkeep` behålls) | venv/uv-install OK; `pytest -q` körs; ruff/mypy konfig OK; git status fungerar |
| 5.2 | Config-loader + Pydantic-modeller (fail-fast) | `pipeline/config.py`, `pipeline/models.py` | `load_config()` utan ValidationError; submåttsvikt≠100 → ValidationError; mypy strict; 7 kat/8 partier; indikator→submått valideras |
| 5.3 | Delpoäng A/B/C/D (ren funktionell kärna) | `pipeline/subscores.py`, `pipeline/normalize.py` | varje compute ger value∈[0,5]+confidence; B vänder tecken rätt; C(regering hela fönstret)>C(aldrig styrt); D<min_responsibility=0.15 → 2.5/low; target-närhet; inga magiska tal |
| 5.4 | Kategoribetyg + osäkerhetsintervall | `pipeline/aggregate.py` | betyg = 0.40A+0.35B+0.15C+0.10D; ci_low≤score≤ci_high∈[0,5]; alla high → halvbredd 0.225; alla low → 1.05; aldrig >max 1.5 |
| 5.5 | Orkestrering → `dist/scores.json`+`dist/evidence.json` | `pipeline/{score,io}.py`, `dist/.gitkeep` | körning skapar bägge filer; två körningar (fast stämpel) byte-identiska; 8×7 celler, varje med score/ci[2]/components/refs; refintegritet; evidence bantat |
| 5.6 | JSON Schema (Draft 2020-12) + validering | `schemas/{scores,evidence}.schema.json`, `pipeline/schema.py`, `scripts/gen_schemas.py` | `check_schema` OK; dist-filer validerar; score=6/ci0>ci1/okänt parti → fail; gen_schemas 0 drift |
| 5.7 | Golden tests + fixtures + e2e + schema | `tests/fixtures/mini_warehouse/`, `tests/golden/{scores,evidence}.golden.json`, `tests/test_*.py` | `pytest` grönt; mutation 0.40→0.41 → test_aggregate failar; determinism byte-identisk; coverage ≥90% |
| 5.8 | Metoddok + build-kedja + CI-stub | `docs/scoring-method.md`, `docs/build.md`, `[project.scripts] rosta-score`, `.github/workflows/ci.yml` | metod täcker A/B/C/D+osäkerhet+begränsningar (endast config-värden); `rosta-score` fungerar; build.md reproducerar dist/*.json |

### Osäkerhetsformel (`scoring.yaml`)
```
confidence_numeric: high=0.85, medium=0.60, low=0.30
halvbredd = max_interval_halfwidth(1.5) · Σ_k subscore_weight_k · (1 − confidence_numeric_k)
ci = [clamp(score − halvbredd, 0, 5), clamp(score + halvbredd, 0, 5)]
```

### Verifiering
```bash
python -m venv .venv; .venv/Scripts/python -m pip install -e .[dev]   # eller uv sync
uv run ruff check pipeline tests && uv run mypy pipeline
uv run python -c "from pipeline.config import load_config; load_config()"
uv run python -m pipeline.score --input tests/fixtures/mini_warehouse --out dist
uv run python pipeline/gen_schemas.py    # 0 drift
uv run pytest -q                          # golden + mutation + determinism + schema
uv run pytest --cov=pipeline --cov-report=term-missing    # ≥90%
# kör score.py två ggr med fast generated-stämpel → fc/diff identiska
```

### Risker
- **Normaliseringsordning tvetydig** i `scoring.yaml` → låst i 5.0 (B/D absolut, A/C cross-party minmax), dokumenterat i scoring-method.md.
- Upstream-beroende (Fas 4 effects/claims) → kör mot syntetisk fixtur; input-kontrakt fryst i 5.0; ev. adapter om Fas 4-schema avviker.
- Repot ej körbart Python från start → 5.1 etablerar skelett idempotent/minimalt (överlappar Fas 0, gör additivt).
- Determinism skör (float/dict-ordning/stämpel/pydantic) → `io.py` sort_keys + fast float-format + reproducerbar stämpel; `test_determinism` vakt; pinna avrundning, lita ej på repr.
- `subnational_governance` pending → hantera tomt graciöst (faller på national), lägre confidence, dokumenterad begränsning.
- D inneboende brusig → D-vikt låg (10%), bred osäkerhet vid låg ansvarsgrad.
- Kategori 7 + target-indikatorer icke-monotona → dedikerade normalize-tester + lägre confidence.
- "Inga magiska tal" → grep/lint-regel flaggar numeriska literaler i subscores/aggregate.

### Exit-kriterium (DoD)
`python -m pipeline.score --out dist` (eller `rosta-score`) producerar deterministiskt `dist/scores.json` + `dist/evidence.json` i DATA.md-format för 8×7 med A/B/C/D + osäkerhet; bägge validerar mot scheman och refintegriteten håller; hela matten låst av golden tests som failar vid mutation; två körningar byte-identiska; all logik/tröskel ur config (verifierat); ruff/mypy(strict)/pytest grönt med ≥90% coverage; `docs/scoring-method.md` är publik granskningsbar metod. Körbar på syntetiska fixturer oberoende av Fas 1–4.

---

## Fas 6 — Frontend: client-side viktning, rankad partilista, osäkerhet och bevisspår

> **Status: v1 byggd ✅ (2026-05-30).** Statisk frontend i [web/](../web/): laddar `scores.json`+`evidence.json`
> (self-contained via `web/data/`, fallback `../dist/`), client-side viktning med reglage, rankad partilista
> med osäkerhetsband + "≈ osäker skillnad"-notis vid CI-överlapp, expanderbart **bevisspår** (löser `claim_refs`
> mot evidence.json), URL-delning (`?w=`), svensk talformatering (`3,72 / 5 (3,3–4,2)`), prominent **version-0-varning**
> och metod-sektion, dynamisk källattribution. Rena testbara moduler ([web/format.js](../web/format.js),
> [web/score.js](../web/score.js)) — frontend gör ENDAST viktning/summering, ingen betygslogik. Tester:
> `node --test web/tests/` (6 gröna) + `tests/test_dist_schema.py` (deploy-kontrakt + negativtest) +
> **Playwright-e2e (8 gröna, task 6.7)**. Verifierat: `web/score.js` reproducerar pipelinens ranking exakt.
>
> **Uppdatering 2026-05-30 (task 6.6 + 6.7 klara):** Playwright-e2e ([web/tests/e2e.spec.mjs](../web/tests/e2e.spec.mjs),
> `npm run test:e2e`) täcker 8 kort fallande, live-omräkning, bevisspår, `?w=`-round-trip, trasig fixtur → felkort,
> samt WCAG-regressioner (fokus/expandering bevaras vid omräkning, ingen sidoscroll vid 320px). **Full
> WCAG 2.2 AA-genomgång** i [docs/fas6_wcag.md](fas6_wcag.md): alla textkontraster mätta ≥4,5:1, tangentbordsflöde,
> skip-link, `aria-controls`, dedikerad `role="status"`-livesammanfattning (debounce:ad), 320px-reflow. Den enda
> **blockerande** bristen (fokus-/expanderingsförlust när `ol.innerHTML` nollades vid varje reglagedrag — 3.2.2/2.4.3,
> flaggad av Codex) är åtgärdad: korten byggs en gång och omordnas in-place med fokusåterställning.
> **Återstår (ej blockerande):** manuell skärmläsartest (NVDA/VoiceOver), ev. moduluppdelning enligt task-tabellen.
> Kör: `python -m http.server 8000` → `/web/`.

### Mål
Statisk, byggfri webb-frontend i `web/` som (1) laddar `dist/scores.json` + `dist/evidence.json`, (2) validerar mot delat JSON Schema, (3) låter användaren vikta de 7 kategorierna (IDEA.md-standardvikter default), (4) räknar total + osäkerhet **helt client-side** (`Total = Σ kategoribetyg × normaliserad vikt`), (5) visar partier rankade fallande med poäng + intervall (`3,84 / 5 (3,5–4,1)`), och (6) gör varje betyg granskningsbart via expandering till claims/källor. Ingen betygslogik uppfinns i frontend. All text svensk.

### Task-tabell

| id | Task | Deliverable | Acceptanskriterium |
|----|------|-------------|--------------------|
| 6.0 | **Frys datakontraktet** + fixtures | `schemas/{scores,evidence}.schema.json`, `schemas/README.md`, `tests/fixtures/{scores,evidence}.sample.json` | sample-filer validerar (Draft202012); ingen dinglande ref; alla score/components∈[0,5], ci0≤score≤ci1; 7 kategori-id + standard_weight summerar 100 |
| 6.1 | Frontend-skelett + inladdning + klientvalidering | `web/index.html`, `web/css/styles.css`, `web/js/{data,validate,config}.js`, `web/data/{scores,evidence}.json`, `package.json` (endast dev) | root serveras utan konsolfel; refs upplöses; kontraktsbrott → svenskt felmeddelande, ej krasch; inga runtime-npm-deps |
| 6.2 | Ren scoringmodul (Node+browser) | `web/js/score.js` | `normalizeWeights` summerar 1.0±1e-9; totalScore=Σ w·score (handräknat); ciLo≤total≤ciHi; rankParties fallande + alfabetisk tie-break; vikter alla 0 → ingen NaN |
| 6.3 | Viktpanel + URL-delning | `web/js/{weights,format}.js`, uppdaterad HTML/CSS | reglage räknar om live; standardvikter summerar 100%; URL round-trip; ogiltig kategori ignoreras; `formatScoreWithCI(3.84,[3.5,4.1])==='3,84 / 5 (3,5–4,1)'` |
| 6.4 | Rankad resultatlista + partikort | `web/js/results.js`, HTML/CSS | 8 kort fallande; total+CI-stapel inom 0–5; expander 7 kategorier + A/B/C/D; "osäker skillnad"-notis vid CI-överlapp; re-sortering utan omladdning |
| 6.5 | Bevis-/källspår (transparenskrav) | `web/js/evidence.js`, Metod-sektion i HTML, CSS | expander listar summary/källa/dataset-id/datum/nyckelvärde/licens/URL; URL ny flik rel=noopener, https-normaliserad; saknad ref → "källa saknas"-notis; metod anger A/B/C/D-vikter |
| 6.6 | Tillgänglighet + mobil + attribution + degradering | HTML/CSS, `web/js/ui.js` | hela flödet tangentbordsstyrt; aria-live på resultat; footer attribution ur evidence.json (SCB CC0, Riksdagen, Kolada/RKA); 360px användbar; trasig fil → felkort; generated-stämpel |
| 6.7 | Tester (unit + schema + e2e) | `web/tests/{score,format}.test.js`, `tests/test_dist_schema.py`, `web/tests/e2e.spec.js`, `web/README.md`, npm-scripts | `test:unit` grönt; schemavalidering grönt; Playwright: 8 kort, live-omräkning, bevisspår, `?w=`-round-trip; trasig fixtur (ci0>score) failar |
| 6.8 | Deploy-koppling + .gitignore-disciplin | `web/README.md`, `docs/frontend.md`, `scripts/sync-dist.mjs`, `.gitignore` | dok beskriver de två filerna som hela kontraktet; sync kopierar dist→web/data; `data/`+`*.duckdb` ignoreras, fixturer+dist committas; statisk serve utan extra nätverksanrop |

### Filer
`schemas/{scores,evidence}.schema.json`, `schemas/README.md`, `tests/fixtures/{scores,evidence}.sample.json`, `web/index.html`, `web/css/styles.css`, `web/js/{config,data,validate,score,format,weights,results,evidence,ui}.js`, `web/data/{scores,evidence}.json`, `package.json`, `web/tests/{score.test,format.test,e2e.spec}.js`, `tests/test_dist_schema.py`, `web/README.md`, `docs/frontend.md`, `scripts/sync-dist.mjs`, `.gitignore`.

### CI-propagering (beslut)
```
total-lo = Σ_k w_k · lo_k ;  total-hi = Σ_k w_k · hi_k     (linjär gränspropagering, konservativ)
```
Konsekvent med `scoring.yaml`:s deterministiska halvbreddsmodell. Ingen sannolikhetsmodell uppfinns i frontend; valet dokumenteras i kod-kommentar och metodtext.

### Verifiering
```bash
uv run pytest -q tests/test_dist_schema.py     # fixtures + web/data validerar; negativtest ci0>score failar
npm run test:unit                              # score.js + format.js
npm run test:e2e                               # Playwright: 8 kort, viktändring, bevisspår, URL round-trip
# manuell: tangentbord-only flöde, aria-live, 360px viewport
# deploy-disciplin: serva web/ + två JSON statiskt → inga extra nätverksanrop
```

### Risker
- **Kontraktsdrift** Fas 5↔6 → samma scheman valideras i bägge teststackar; `meta.schema_version` bevakar brott.
- CI-propageringens semantik → håll linjär gränspropagering, dokumentera, uppfinn ingen sannolikhetsmodell.
- Frontend frestas räkna om betyg → `score.js` får ENDAST vikta/summera; kodgranskning + test att components kommer oförändrade.
- Lokaliseringsfällor (komma/tankstreck) → all formatering i `format.js` med test; URL i maskinformat separerat från visning.
- Dinglande evidens-refs → defensiv rendering + kontraktstest att alla refs upplöses.
- `file://` blockerar fetch/ESM → dev-server i README/e2e, deploy via statisk host.
- Tom viktinmatning (alla 0) → definierat beteende + test mot NaN.
- Tillgänglighet underprioriteras → eget task (6.6) med tangentbordsgenomgång + aria-live som acceptanskriterium.

### Exit-kriterium (DoD)
Scheman formaliserar DATA.md sektion 5 och fixtures + `web/data/*.json` validerar grönt (med bevisat negativt test); statisk frontend laddar de två filerna, viktar 7 kategorier (default IDEA.md-vikter), räknar total + osäkerhet client-side via ren `score.js` (ingen A/B/C/D-logik i frontend); partier rankade fallande i svensk format, varje betyg expanderbart till A/B/C/D → claims-/källspår; viktval delbart via URL och round-trippar; unit + schema + Playwright-e2e gröna; tillgänglighet (tangentbord, aria-live, AA) + 360px verifierade; deploy-split intakt: artefakt = `web/` + endast `dist/scores.json` + `dist/evidence.json`, `.gitignore` upprätthåller det.

---

## 3. Tvärgående kapitel

### 3.1 Datalicenser och attribution per källa

> **Hård regel (CLAUDE.md/DATA.md):** Licenssträngar och `dataset_id` får **aldrig** gissas. Verifiera vid första hämtning, skriv exakt sträng i `config/sources.yaml` + i varje manifest. Endast officiella svenska myndigheter/etablerade akademiska källor.

| Källa | Myndighet | Licens (verifierad) | Attribution | Auth | Rate-limit |
|-------|-----------|---------------------|-------------|------|-----------|
| Riksdagens öppna data | Sveriges riksdag | Attribution-required (inget formellt SPDX) | "Källa: Sveriges riksdag" | none | Ingen publicerad — var hövlig |
| SCB PxWeb v2 | SCB | **CC0-1.0** (verbatim i `/config`) | "Källa: SCB" | none | 30 anrop/10s/IP, max 150000 celler/fråga |
| Kolada v3 | RKA/SKR | Öppen/kostnadsfri, inget SPDX → **attribution-required** | "Kolada/RKA + ursprungskälla (ofta SCB)" | none | Ingen publicerad; `next_url`-paginering |
| Brå / NTU | Brå | Fri med källangivelse (inget API) | "Brå" | n/a (fildownload/SOL) | n/a; SOL = ISO-8859-1 |
| Valmyndigheten | Valmyndigheten | Fri med citering (inget API) | "Valmyndigheten" | n/a (ZIP/CSV) | n/a |
| Socialstyrelsen | Socialstyrelsen | Öppen officiell statistik (verifiera live) | "Socialstyrelsen" | none | per_sida/sida >5000 rader |
| Skolverket | Skolverket | Öppen (verifiera live) | "Skolverket" | none | SiRiS långsam (~30s), pToken expirerar |
| Naturvårdsverket (via SCB MI0107) | Naturvårdsverket/SCB | CC0 (SCB) | "Källa: SCB (Naturvårdsverket)" | none | SCB-gränser |
| Energimyndigheten | Energimyndigheten | Öppen (verifiera live) | "Energimyndigheten" | none | PxWeb-celltak |
| Svenska kraftnät (Mimer) / eSett | Svk / eSett | Öppen (verifiera) | "Svenska kraftnät" / "eSett" | none | odokumenterat → konservativt |
| SOM-institutet | Göteborgs universitet (akademisk) | Akademisk, tabellref | "SOM-institutet, Göteborgs universitet" | n/a | — |
| Evidensorgan (IFAU, SBU, Vårdanalys, FOI, Klimatpolitiska rådet m.fl.) | Resp. myndighet/råd | Per rapport (source_ref) | Rapport-URL/diarienr | n/a | — |

Licensfältet är **obligatoriskt** per källa (test kräver icke-tomt). Frontend genererar footer-attribution dynamiskt ur `evidence.json:license/source_name` så attributionen alltid speglar faktiskt använda källor.

### 3.2 Reproducerbarhet och caching av API-svar (manifest)

Per hämtning skrivs rådatasvaret + ett manifest till Lager 1:
```
data/raw/<källa>/<dataset>/<fetched_date>.json        (rådata, gitignorad)
data/raw/<källa>/<dataset>/<fetched_date>.manifest.json
```
**Manifest-fält** (`manifest_fields` i `sources.yaml`):
```
source_url        # exakt anropad URL inkl. query
dataset_id        # pinnad i sources.yaml (gissas aldrig)
params            # POST-body / query-parametrar
fetched_at        # ISO 8601 UTC
http_status
content_type
content_hash      # sha256 av kroppen (idempotens/diff)
license           # verifierad sträng
api_version
record_count
```
- **Cache-nyckel** = `sha256(url + params)`. Finns manifest med samma hash och `--force` ej satt → ingen omhämtning (idempotens-bevis: andra körningen = 0 nätverksanrop).
- **Lagring:** Lager 1 = JSON; Lager 2/3 = Parquet (partitionerat per källa/dataset/datum) som DuckDB frågar direkt via `read_parquet`. `uv.lock` committas för exakt miljö.
- **Reproducerbar stämpel:** scoring/output använder SOURCE_DATE_EPOCH-mönster (`generated` via env/flagga) så golden-output inte bryts av klockan.
- **Determinism:** sorterade nycklar, fast float-avrundning, stabil parti/kategori-ordning ur config → två körningar byte-identiska.

### 3.3 Teststrategi (golden tests + schema-validering)

| Nivå | Vad | Var |
|------|-----|-----|
| Config-invarianter | 7/100/34/50, A/B/C/D=40/35/15/10, level-vikter=1.0, enum-/cross-konsistens | Fas 0 `test_config.py` |
| Schema check | Alla scheman `Draft202012Validator.check_schema` | Fas 0 `test_schemas.py` |
| Schema-kontrakt | Pydantic `model_json_schema()` == incheckat JSON Schema (gen_schemas-drift) | Fas 4/5 |
| Normaliserings-golden | json-stat2/ISO-8859-1/paginering på fixturer | Fas 2/3 |
| Claims-golden | fixtur → exakt ClaimSet; source_ref+rule_id; källlös → inget claim | Fas 4 |
| Effects-golden | net_support/confidence inom 1e-6, för hand räknat | Fas 4 |
| Scoring-golden + mutation | A/B/C/D + betyg + osäkerhet; 0.40→0.41 → test failar | Fas 5 |
| Idempotens/determinism | byte-identisk content_hash/output över två körningar | Fas 2/4/5 |
| Frontend-unit | normalisering/total/CI/rankning/format | Fas 6 |
| E2e (Playwright) | 8 kort, live-omräkning, bevisspår, URL round-trip | Fas 6 |
| Deploy-kontrakt + negativtest | dist/fixtures validerar; trasig (score=6/ci0>score) failar | Fas 5/6 |

**Sabotage-/mutationsprincip:** varje låsande test ska bevisligen RÖTT-faila vid ett medvetet brott (vikt≠100, vikt 0.40→0.41, ci0>score) — annars biter testet inte. Offline-tester (`-m "not network"`) kräver inget internet; live-smoke är `@pytest.mark.network`, körs manuellt.

### 3.4 CI (GitHub Actions)

`.github/workflows/ci.yml` (push + PR mot main), matris Python 3.12/3.13, cache uv:
```
checkout
astral-sh/setup-uv@v3            (fallback: setup-python + pip install uv)
uv sync --all-extras --dev
uv run ruff check .
uv run ruff format --check .
uv run mypy src                   (Fas 4/5: pipeline)
uv run python pipeline/gen_schemas.py && git diff --exit-code schemas/   # schema-drift-check
uv run pytest -q --cov=rosta --cov-report=term-missing
```
Frontend (Fas 6) lägger `npm run test:unit` + Playwright-e2e + `pytest tests/test_dist_schema.py`. CI bevisar grön grund på ren maskin; offline-tester kräver inget nät.

### 3.5 Hur osäkerhet propageras genom kedjan

```
Källa → observation        confidence_hint='low' för enkät/proxy-data (SOM, försvar ÅR)
   │                       is_proxy=true bärs vidare
   ▼
Claim                      confidence ∈ {low,medium,high}; evidence_level styr källstyrka
   │
   ▼
IndicatorEffect (Fas 4)    confidence ∈ [0,1] = viktat medel av claim-confidence;
   │                       nedjusterat om n_claims < 3 (min_claims_for_high_confidence)
   ▼
Delpoäng A/B/C/D (Fas 5)   confidence_level per delpoäng (high/med/low);
   │                       missing_effects → B=2.5/low; D<min_responsibility → 2.5/low;
   │                       subnational pending → lägre confidence
   ▼
Kategoribetyg + CI (Fas 5) halvbredd = 1.5 · Σ_k w_k·(1−confidence_numeric_k)
   │                       ci = [clamp(score−hw,0,5), clamp(score+hw,0,5)]
   ▼
Total + CI (Fas 6)         total-lo = Σ w_k·lo_k ; total-hi = Σ w_k·hi_k (linjär)
                           "osäker skillnad"-notis när partiers CI-band överlappar
```
Osäkerheten degraderar **graciöst** snarare än döljs: svaga gap allowlistas och redovisas, låg confidence breddar intervallet, och frontend visar intervall + överlapp explicit (IDEA.md-krav).

---

## 4. Fas 0 snabbstart — checklista med konkreta filer

> Kör i `c:/Users/marcu/Documents/GitHub/Rösta`. Repot har redan partiell scaffolding — **komplettera additivt**, skriv inte över config i sak.

**1. Git + ignorerar (T0.1)**
- [ ] `git init` (om ej redan repo), default branch `main`, branch `phase-0-skeleton`
- [ ] `.gitignore`: `data/`, `.venv/`, `__pycache__/`, `*.pyc`, `.pytest_cache/`, `.ruff_cache/`, `.mypy_cache/`, `*.duckdb`, `*.parquet`, `.DS_Store` — **INTE** `uv.lock`; behåll `dist/.gitkeep`
- [ ] `src/rosta/__init__.py` (`__version__='0.0.0'`), `src/rosta/sources/__init__.py`
- [ ] Stubbar (endast moduldocstring): `src/rosta/{transform,claims,effects,score,schema}.py`
- [ ] `.gitkeep` i `data/raw/`, `dist/`, `tests/fixtures/`
- [ ] `docs/ADR-0001-repo-layout.md` (välj `src/rosta/` som kanon; befintliga top-level `pipeline/` migreras eller hålls tomt)

**2. Tooling (T0.2)**
- [ ] `pyproject.toml`: `requires-python='>=3.12'`, deps `pydantic>=2.10, jsonschema>=4.23, pyyaml>=6.0, httpx>=0.27, duckdb>=1.1, pandas>=2.2`; dev `pytest>=8, pytest-cov, ruff>=0.6, mypy>=1.11, types-PyYAML`
- [ ] `[tool.ruff]` line-length 100, target py312, lint `['E','F','I','UP','B','SIM']`
- [ ] `[tool.pytest.ini_options]` `addopts=['--import-mode=importlib']`, `testpaths=['tests']`, `pythonpath=['src']`
- [ ] `[tool.mypy]` py312, `packages=['rosta']`, `plugins=['pydantic.mypy']`
- [ ] `[build-system]` hatchling, `[tool.hatch.build.targets.wheel] packages=['src/rosta']`
- [ ] `pip install uv` → `uv sync` → committa `uv.lock` (eller dokumentera pip-fallback i ADR)

**3. Saknade config-filer (T0.3, T0.5)**
- [ ] `config/sources.yaml` (NY) — källregister; `dataset_ids:{}` tomma; SCB CC0/30-10s/150000, Kolada `/v3`+410-gotcha, Riksdagen attribution; manifest_fields + `raw_path_template`
- [ ] `config/mappings.yaml` (NY/komplettera) — `expenditure_area_to_category` (UO1–27→7 kategorier), `government_periods` 2014–2026 med `source`, `regional_municipal_governance` draft

**4. Scheman (T0.4)** — avstäm faktiska filnamn mot repot (`observation` vs `observations`); fyll/komplettera till 12 st:
- [ ] Artefakter: `observations`, `actions`, `responsibility`, `claims`, `indicator_effects`, `scores`, `evidence`
- [ ] Config: `categories`, `sources`, `mappings`, `scoring`, `claims.config`
- [ ] `schemas/README.md` ($id + bunden artefakt/config + produktionsfas)

**5. Bro config↔pydantic↔JSON Schema (T0.6)**
- [ ] `src/rosta/schema.py`: Pydantic-modeller (Observation/Action/Responsibility/Claim/IndicatorEffect med Literal-enums), `load_yaml/load_schema/get_validator/validate_config`, `repo_root()` (letar uppåt efter pyproject.toml), `PARTIES`(8)/`CATEGORY_IDS`(7 ur categories.yaml)

**6. Golden-test-stomme (T0.7)**
- [ ] `tests/test_config.py` (schema_loads, config_validates, categories/scoring/claims-invarianter, cross_consistency, deploy_artifacts_smoke)
- [ ] `tests/test_schemas.py` (12 scheman check_schema + fixtur grönt/trasig rött)
- [ ] `tests/fixtures/{scores,evidence}.min.json`

**7. CI + README (T0.8)**
- [ ] `.github/workflows/ci.yml` (uv→ruff→format→mypy→pytest, matris 3.12/3.13)
- [ ] `README.md` (en mening + `uv sync && uv run pytest`, länkar IDEA.md/DATA.md/CLAUDE.md)

**8. Verifiera + dokumentera (T0.9)**
- [ ] Hela verifieringslistan grön i ren shell
- [ ] `docs/ADR-0001-repo-layout.md` + `docs/PHASE-0-DONE.md` (draft-platshållare Fas 1 ärver)
- [ ] EN sammanhållen commit på `phase-0-skeleton` (pusha ej utan begäran)

**Snabbverifiering:**
```bash
uv run ruff check . && uv run ruff format --check . && uv run mypy src && uv run pytest -q
uv run python -c "from rosta.schema import PARTIES, CATEGORY_IDS; print(len(PARTIES), len(CATEGORY_IDS))"   # 8 7
uv run python -c "import yaml;d=yaml.safe_load(open('config/categories.yaml',encoding='utf-8'));c=d['categories'];print(len(c), sum(x['standard_weight'] for x in c), sum(len(x['submeasures']) for x in c), sum(len(x['indicators']) for x in c))"   # 7 100 34 50
git check-ignore data/raw/x.json && (git check-ignore uv.lock || echo "uv.lock spåras korrekt")
```