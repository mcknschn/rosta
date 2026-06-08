# Rösta — Spec: D-täckningskrympning (undermåttsbredd i delpoäng D) 🟡 UTKAST v1

> **Status: 🟡 UTKAST — väntar Codex-granskning + användarens sign-off.** Adresserar en verifierad
> asymmetri: delpoäng **D** låter ett enda täckt Undermått tala för hela Kategorins utfall, oavkortat
> och med oförtjänt confidence. Ingen kod ändrad ännu; detta är designen för diskussion.
>
> Relaterat: [spar_D_datatackning.md](spar_D_datatackning.md) (D-trackern + §2.1 mastertabellen),
> [done/viktad_stance_spec.md](done/viktad_stance_spec.md) (parallell scoring-spec, mall för detta dok),
> [done/evidens_trovardighet.md §4.3](done/evidens_trovardighet.md) (B/D-mastertabell, begreppsmodell),
> [../config/scoring.yaml](../config/scoring.yaml), [../pipeline/scorerun.py](../pipeline/scorerun.py),
> [../pipeline/score.py](../pipeline/score.py), [../IDEA.md](../../IDEA.md), [../DATA.md](../../DATA.md).
>
> Begreppsmodell (kanonisk, §4.3): **Kategori → Undermått → Indikator → Riktning.**

---

## 0. Kärnbeslutet (läs först)

D påstår sig mäta **Kategorins** utfall ("förbättrades de objektiva indikatorerna där partiet hade
ansvar?"). Men D beräknas som ett renormaliserat medel över **bara de Undermått som har en serie** —
utan någon rabatt för hur stor andel av Kategorin det faktiskt är. Försvar har D i **1 av 5** Undermått
(`militar_formaga` via `personal_varnpliktiga`); de övriga fyra (materiel, civil beredskap, Nato/Ukraina,
leverans) är osynliga för D. Ändå presenteras försvars-D med `measured_confidence: medium` och utan en
enda flagga om att det är en femtedel.

**Konsekvens (verifierad, §1):** ett parti som driver upp värnpliktssiffran men samtidigt försvårar
materielinköp, drar ner Ukrainastöd och skär i civilförsvaret får ändå **hög försvars-D** — och appen
"hävdar att utfallet blev bra".

**Det enda beslut som avgör allt annat i denna spec:** ska D krympas mot neutral efter
**undermåttsbredd**, och i så fall med vilken **nämnare**? (§4 är crux.) Rekommendation: **ja — krymp +
sänkt confidence, nämnare = icke-target Undermått (N_b, §4).** Det ger försvar/demokrati den ödmjukhet
de ska ha utan att röra väl täckta Kategorier (ekonomi oförändrad).

---

## 1. Problemet — verifierad mekanik

### 1.1 D renormaliserar bort, men rabatterar aldrig

[`category_d`](../pipeline/scorerun.py#L215-L222):

```python
sub_nets = {sub: sum(v) / len(v) for sub, v in by_sub.items()}     # bara Undermått med serie
cat_net  = score.submeasure_weighted_mean(sub_nets, sub_w.get(c, {}))  # renormaliserar över NÄRVARANDE
measured = cat_net is not None and basis >= min_resp
out[(p, c)] = (score.net_support_to_score(cat_net), True, basis < thin)
```

[`submeasure_weighted_mean`](../pipeline/score.py#L120-L124) summerar vikten **bara över närvarande**
Undermått (`wsum = Σ present`). Ett saknat Undermått försvinner spårlöst — varken täljare eller nämnare.
Så `cat_net` är medlet av *de täckta* Undermåtten, skalat 1:1 till [0,5]. **Ingen term beror på hur många
Undermått Kategorin egentligen har.**

### 1.2 Asymmetri mot B — och B:s eget bredd-hål

B *har* en coverage-krympning ([scorerun.py:416](../pipeline/scorerun.py#L416)):
`b_val = 2.5 + (b_raw - 2.5) * coverage`. Men nämnaren är **partiets kodbara åtgärdstyper**
([scorerun.py:373-381](../pipeline/scorerun.py#L373-L381)) — den mäter *"hur många av de instrument vi
kodat har partiet en ståndpunkt på"*, **inte** *"hur stor andel av Kategorins Undermått mäter vi"*.

Det betyder att **B har samma bredd-hål som D**: om en Kategori bara har liggar-poster under 1 Undermått
blir `cov_den` litet, ett välpositionerat parti får `coverage ≈ 1`, och det enda Undermåttet talar för
hela B oavkortat. B:s skydd mot detta är inte runtime utan en **grind** — `b_submeasure_spread` +
allowlisten [`b_near_binary_accepted`](../config/coverage_allowlist.yaml#L83-L95) (test
`tests/test_fas4b_coverage.py`), som tvingar mänsklig uppmärksamhet när en Kategori vilar på ≤1 Undermått.

**D har varken runtime-rabatt ELLER bredd-grind.** Det är helt oskyddat. Det är hålet denna spec stänger.

### 1.3 `D_thin_basis` mäter fel sak

Flaggan ([scorerun.py:220-222](../pipeline/scorerun.py#L220-L222), `basis < thin`) mäter **ansvars­underlag**
= Σ maktvikt över de år partiet attribueras. Det är en *attributions*-storhet (styrde partiet länge nog?),
**inte** en *bredd*-storhet (mäter vi nog av Kategorin?). De är oberoende: ett parti kan ha starkt
ansvarsunderlag på `militar_formaga` (ingen `D_thin_basis`) och ändå representera 1/5 av försvaret. Vi
behöver en **ny, ortogonal** flagga för bredd, inte en omdefiniering av basis.

### 1.4 Arbetat exempel — försvar idag (Tier 4-leveransloggen)

| Parti | D_raw idag | net | Kommentar |
|---|---:|---:|---|
| M / KD / SD | **5,00** | +1,00 | Tidö-eran, värnplikt upp varje år |
| L | 4,37 | +0,75 | JÖK-stöd + Tidö |
| S | 3,96 | +0,58 | bär 2018–2021-rampen + 2022-dippen |
| MP | 3,83 | +0,53 | |
| C | 3,40 | +0,36 | |
| V | 2,50 | NA | aldrig regering (korrekt) |

Spridning 3,40–5,00 på en **enda** värnpliktsserie, presenterad som uppmätt försvarsutfall. Det är det
magstarka påståendet.

---

## 2. Mål & icke-mål

**Mål:** D ska vara **ödmjukt i proportion till hur stor andel av Kategorin det faktiskt observerat.**
När D bara sett en femtedel ska det (a) regrediera mot neutral 2,5 och (b) bära bredare osäkerhet — så
att en ensam serie inte kan hävda ett helt Kategoriutfall.

**Icke-mål:**
- Inte att "laga" döda Undermått (de är ofarliga; se [spar_D_datatackning.md §2.1](spar_D_datatackning.md)).
- Inte att straffa partier — krympningen är **partineutral** (kategori-egenskap, rör inte inbördes ordning,
  bara spridningen) och drar mot **neutral**, inte nedåt.
- Inte att fabricera bredd. En Kategori som genuint bara kan mätas tunt (försvar, demokrati — mestadels
  kvalitativt/sekretess) **ska** ha ett permanent ödmjukt D. Det är korrekt, inte en brist.
- Inte att röra B i denna iteration (men §8 öppnar frågan — användaren bad uttryckligen om den).

---

## 3. Designval — fyra alternativ

| # | Ansats | Rör punktskattningen? | Rör confidence/CI? | Mönster i repo |
|---|---|:---:|:---:|---|
| **A** | **Confidence-only** — behåll D_raw, sänk confidence + flagga vid tunn bredd | nej | ja | — |
| **B** | **Krympning** — `D = 2.5 + (D_raw−2.5)·d_cov` + sänkt confidence + flagga | ja | ja | speglar B [scorerun.py:416](../pipeline/scorerun.py#L416) |
| **C** | **Omviktning** — under bredd-tröskel: dra D:s 0,10-vikt, fördela på A/B/C + flagga | binärt (på/av) | indirekt | speglar C `missing_subnational` [scoring.yaml:109-111](../config/scoring.yaml#L109-L111) |
| **D** | **Grind-only** — ingen runtime-ändring; nytt test som tvingar allowlist vid ≤1 D-Undermått | nej | nej | speglar `b_submeasure_spread` |

**Avvägning:**
- **Alt A** är minst ingripande och löser *falsk confidence*, men inte användarens *substantiella*
  invändning: D=5,0 syns fortfarande som rubrik (bara med bred CI). Användaren ifrågasätter magnituden,
  inte bara säkerheten.
- **Alt B** löser båda och är epistemiskt symmetriskt med B ("frånvaro av observation → vet ej → mot
  neutral"). Risk: inför en avsiktlig bias mot 2,5 på en serie som *genuint* förbättrades — men det är
  rätt: vi vet inte om de övriga 4/5 förbättrades, så Kategori-skattningen *ska* regrediera.
- **Alt C** undviker att injicera en 2,5-pseudoobservation, men är trubbig (allt-eller-inget) och gör D:s
  vikt Kategori-beroende, vilket komplicerar totalpoängens tolkning.
- **Alt D** är billigast och mest konservativt men ändrar inget betyg — det gör bara hålet *synligt*. Bra
  som komplement, otillräckligt ensamt (användaren vill att betyget blir ärligt, inte bara flaggat).

**Rekommendation: Alt B + Alt D.** Krymp punktskattningen och sänk confidence (B), OCH lägg en bredd-grind
(D) så att en framtida tunt täckt Kategori inte tyst slinker förbi. Alt A är fallback om Codex/användaren
inte vill röra punktskattningen.

---

## 4. Nämnaren i `d_cov` — specens crux ⭐

`d_cov ∈ [0,1]` = täckta Undermått / **(nämnare)**. Allt hänger på nämnaren:

| Nämnare | Definition | Försvar | Effekt |
|---|---|:---:|---|
| **N_a** | Undermått som **kan** ha en serie (D-bara) | **1/1 = 1,00** | ingen krympning — **löser inte problemet** (övriga försvars-Undermått är kvalitativa/target → exkluderas → 100 %) |
| **N_b** | **Icke-target** Undermått (alla som "betyder något") | **1/5 = 0,20** | kraftig, ärlig krympning — **rekommenderad** |
| **N_d** | Undermått med **B eller D** (allt modellen fångar alls) | **1/4 = 0,25** | mellanläge; exkluderar helt ofångade Undermått |

**Varför N_b (icke-target):** D:s semantiska anspråk är *Kategorins* utfall. Kategorin **definieras** av
sina icke-target Undermått (target = "kontext, betygssätts ej", korrekt exkluderad). Att försvar inte
*kan* mäta materiel med en officiell serie gör inte materiel mindre till en del av vad "försvarsutfall"
betyder — så D ska vara ödmjukt om det det inte ser, även när blindheten är oundviklig. Konsekvensen
(försvar/demokrati får ett permanent capat D) är **korrekt**: utfallsdata ser bara en flik av dessa
Kategorier, och D väger ändå bara 10 % — Kategorin bärs av A/B/C.

**Motargument (för N_a / N_d), som Codex bör pröva:** B:s coverage-nämnare är "kodbara åtgärdstyper" =
*det vi byggt*, vilket liknar N_a/N_d (det modellen fångar), inte N_b (allt som betyder något). En strikt
*symmetri-med-B*-läsning pekar mot N_d. Men N_a/N_d återinför delvis problemet (de exkluderar just de
ofångade Undermåtten som gör att appen överskattar försvar). **Avgör medvetet, dokumentera valet.**

**`d_cov` per Kategori under N_b** (täckta från [spar_D §2.1](spar_D_datatackning.md), icke-target nämnare):

| Kategori | Täckta D-Undermått | Icke-target Undermått | d_cov (N_b) | Krympning? |
|---|:---:|:---:|:---:|---|
| ekonomi | 4 | 4 | **1,00** | nej (oförändrad) |
| integration | 3 | 5 | 0,60 | måttlig |
| trygghet | 3 | 5 | 0,60 | måttlig |
| valfard | 2 | 4 | 0,50 | måttlig |
| klimat | 2 | 5 | 0,40 | tydlig |
| **forsvar** | 1 | 5 | **0,20** | kraftig |
| **demokrati** | 1 | 5 | **0,20** | kraftig |

Notera: ekonomi rörs inte (full bredd), exakt som önskat. Krympningen träffar precis de Kategorier
användaren pekade på.

**Per-parti vs per-Kategori:** `d_cov` är en **Kategori-egenskap** (vilka Undermått som har serie är samma
för alla partier). Partispecifik attribution hanteras redan av `min_responsibility`/`basis`. Så krympningen
komprimerar alla partiers D i Kategorin likformigt mot 2,5 → bevarar inbördes ordning, minskar spridningen.
(Öppen fråga §10: ska numeratorn vara partispecifik — bara Undermått där *partiet* har attribution?)

---

## 5. Formell definition (rekommendation: Alt B + Alt D)

För varje (parti `p`, Kategori `c`) där D är `measured` (befintlig grind oförändrad):

```
d_cov(c)   = |{Undermått i c med ≥1 attribuerad D-serie}| / |{icke-target Undermått i c}|     # N_b
D_just     = 2.5 + (D_raw - 2.5) * d_cov(c)
```

- **Stege på bredd** (parallellt med basis-stegen): `d_cov < d_thin_coverage_threshold` (förslag **0,5**)
  → flagga `D_thin_coverage` + sänk D-confidence ett steg (`measured`→`low` via `_step_down_confidence`,
  [scorerun.py:231-234](../pipeline/scorerun.py#L231-L234)). `d_cov ≥ tröskel` → behåll `measured_confidence`.
- **Ortogonal mot basis:** `D_thin_basis` (attributionsunderlag) och `D_thin_coverage` (bredd) kan flagga
  oberoende; båda får stega ner confidence (de mäter olika osäkerheter → ej dubbelräkning).
- `not_applicable` (D ej uppmätt) är oförändrat — `d_cov` appliceras bara när `measured=True`.
- **Invariant:** Kategori med `d_cov = 1` (ekonomi) → `D_just = D_raw`, dvs. byte-identiskt utfall.

### Arbetat exempel — försvar med N_b (d_cov = 0,20)

| Parti | D_raw | D_just = 2,5+(D_raw−2,5)·0,20 | Δ försvarskat. (D-vikt 0,10) |
|---|---:|---:|---:|
| M / KD / SD | 5,00 | **3,00** | −0,20 |
| L | 4,37 | 2,87 | −0,15 |
| S | 3,96 | 2,79 | −0,12 |
| MP | 3,83 | 2,77 | −0,11 |
| C | 3,40 | 2,68 | −0,07 |
| V | 2,50 | 2,50 | 0 |

D-spridningen kollapsar 3,40–5,00 → 2,68–3,00: D slutar vara en stor differentiator i en Kategori den
knappt mäter, exakt som avsett. Rankingeffekten måste mätas (§9) — D väger 10 %, men flera Kategorier
rörs samtidigt.

---

## 6. Teknisk design

- **`config/scoring.yaml` → `D_resultat`:** nya nycklar
  `coverage_shrink: true`, `coverage_denominator: non_target_submeasures` (enum: `non_target_submeasures` |
  `d_eligible_submeasures` | `b_or_d_submeasures`, motsvarar N_b/N_a/N_d), `thin_coverage_threshold: 0.5`.
  Dokumentera valet i en kommentar precis som B:s `coverage_exclude_reasons`.
- **`pipeline/scorerun.py` → `category_d`:** beräkna `non_target_submeasures` per Kategori ur
  `categories.yaml` (ett Undermått är target endast om *alla* dess Indikatorer har `direction: target`);
  räkna täckta Undermått ur `by_sub.keys()`; returnera även `d_cov` och `thin_coverage`-boolean i tupeln.
  Applicera `D_just` + flaggor i huvudloopen ([scorerun.py:427-439](../pipeline/scorerun.py#L427-L439)).
- **`pipeline/score.py`:** ren hjälpfunktion `coverage_shrink(raw, cov, neutral=2.5)` (golden-testbar);
  `weighted_category_score`/`category_score_from_components` oförändrade.
- **Utdata:** `D_thin_coverage` + `D_coverage_k/n` i `scores.json`-flaggorna (provenans, jfr `B_coverage_n/m`).
- **`coverage_report`:** visa `d_cov` per Kategori så bredd-tunnheten blir synlig i trackern.

**Invarianter (test):** (1) `coverage_shrink: false` ⇒ `dist/` byte-identiskt. (2) `d_cov=1` ⇒ D oförändrat.
(3) `d_cov=0` omöjligt när `measured` (minst ett täckt Undermått ⇒ täljare ≥1). (4) krympning bevarar
inbördes partiordning på D inom Kategorin. (5) target-Undermått aldrig i nämnaren.

---

## 7. Bakåtkompatibilitet & förväntad betygseffekt

- Default-flagga gör beteendet **opt-in**; `false` ⇒ exakt dagens betyg (golden-grind).
- Förväntat med N_b: **ekonomi oförändrad**; försvar/demokrati D komprimeras kraftigt mot neutral;
  valfard/klimat/integration/trygghet måttligt. Eftersom V redan är NA i allt påverkas inte V.
- **Ranking:** måste köras och granskas (`score_diff` + `coverage_report`) före sign-off. Hypotes: topp
  rörs lite (D är 10 %, krympningen drar mot neutral snarare än åt ett håll), men det är en empirisk fråga,
  inte ett antagande — re-baselina `dist/` först efter granskning (jfr B-grön-svepets re-baselining).

---

## 8. Ska samma bredd-rabatt gälla B? (användarens uttryckliga fråga)

B har **två** mekanismer redan: positions-coverage-krympning (runtime, [scorerun.py:416](../pipeline/scorerun.py#L416))
+ `b_submeasure_spread`-grinden (test). En **tredje**, undermåttsbredd-krympning på B, skulle:
- **+** stänga B:s bredd-hål på samma runtime-sätt som D, konsekvent modell;
- **−** riskera **dubbelräkning** mot den befintliga positions-coverage-krympningen (båda drar mot neutral;
  produkten `coverage · d_cov` kan överstraffa), och interagera oklart med grinden.

**Rekommendation:** **scope:a denna spec till D** (som är helt oskyddat) och behandla "utvidga bredd-rabatt
till B" som en **separat, senare** fråga — först efter att D-varianten verifierats och vi sett om
interaktionen med B:s två mekanismer går att hålla ren. Markerad som öppen fråga, inte avfärdad.

---

## 9. Acceptanskriterier & verifiering

- [ ] `coverage_shrink: false` ⇒ `dist/scores.json` **byte-identisk** (golden-test).
- [ ] `coverage_shrink(raw, cov)` golden-testad: `cov=1`→raw; `cov=0`→2,5; symmetri kring 2,5
      (supports och opposes krymper lika mycket); monotoni i `cov`.
- [ ] `category_d`: target-Undermått aldrig i nämnaren; täljare = distinkta täckta Undermått; tupeln bär
      `d_cov`+`thin_coverage`.
- [ ] Flaggor `D_thin_coverage` + `D_coverage_k/n` i `scores.json`; `D_thin_basis` oförändrad och oberoende.
- [ ] Confidence stegas ner vid `d_cov < tröskel`; CI breddas (golden på `category_score_from_components`).
- [ ] **Arbetat exempel (försvar)** reproducerat: M/KD/SD D 5,00→3,00 vid N_b; ekonomi oförändrad.
- [ ] `score_diff` + `coverage_report` granskade per Kategori; **ranking-effekt redovisad** före re-baseline.
- [ ] `pytest -q` grönt, `ruff` rent, cyrillisk-koll 0, codex BUILD/KEEP, `dist/` re-baselinad efter granskning.
- [ ] `spar_D_datatackning.md` + `scoring.yaml`-kommentar uppdaterade; v0→v1-status noterad.

---

## 10. Öppna frågor för sign-off

1. **Ansats:** Alt B + Alt D (rek.), eller bara Alt A (confidence-only, rör ej punktskattningen)?
2. **Nämnare (§4, crux):** N_b (icke-target, rek.), N_d (B-eller-D-täckta), eller N_a (D-bara)?
3. **`thin_coverage_threshold`:** 0,5 (förslag) eller annat?
4. **Numerator partispecifik?** Bara Undermått där *partiet* har attribution, eller Kategori-globalt (rek.)?
5. **B (§8):** lämna B orört nu (rek.), eller speca bredd-rabatt på B parallellt?
6. **Permanent capat försvars-/demokrati-D** under N_b är *avsett* — accepteras det som korrekt ödmjukhet?

---

## 11. Codex-granskningslogg

- *(väntar v1-granskning)*

## 12. Relaterat

- [spar_D_datatackning.md](spar_D_datatackning.md) — D-tracker, §2.1 mastertabell (täckningsläget)
- [done/evidens_trovardighet.md](done/evidens_trovardighet.md) — B-spårets logg, §4.3 begreppsmodell/mastertabell
- [done/viktad_stance_spec.md](done/viktad_stance_spec.md) — parallell scoring-spec (mall, abandon-utfall)
- [../config/scoring.yaml](../config/scoring.yaml) · [../pipeline/scorerun.py](../pipeline/scorerun.py) · [../pipeline/score.py](../pipeline/score.py)
