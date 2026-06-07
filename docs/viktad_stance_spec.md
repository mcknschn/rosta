# Rösta — Spec: Viktad stance (grad/magnitud i B) 🟡 UTKAST v2

> **Status: UTKAST v2 — ej implementerad.** v1 granskad adversariellt av Codex 2026-06-07 → **verdikt HOLD**
> (rätt riskområden, men spärrarna för svaga; centrala val flyttades till "officiell referensnivå",
> "ambitionssteg" och manuell neutralitetskoll utan hård definition — där låg tilt-vektorn). v2 nedan
> adresserar Codex 10 punkter (granskningslogg §12). **Kräver förnyad Codex-granskning + mänsklig sign-off
> innan bygge.** Bärande regel oförändrad: **neutralitet före 4** — en grad-modell som inte kan hållas
> värdeneutral byggs INTE.
>
> Relaterat: [done/evidens_trovardighet.md §5.6](done/evidens_trovardighet.md) (gränserna för steg 2),
> [done/evidens_trovardighet.md §2](done/evidens_trovardighet.md) (tvåstegsmodellen),
> [fas4b_partistandpunkter_metod.md](fas4b_partistandpunkter_metod.md) (källhierarki/grindar),
> [../DATA.md](../DATA.md), [../IDEA.md](../IDEA.md).

---

## 0. Huvudrisk & ärlig go/no-go (läs först)

Codex centrala invändning: **de flesta kvantifierbara "instrumentmål" är budgetproxy i annan form** (försvar
% av BNP, antal poliser, ersättnings-/lärartäthets-/vårdplatsnivåer, biståndsandel). Då gäller:
- **strikt G4** (ingen A-dubbelräkning) ⇒ binär fallback *nästan alltid* ⇒ specen löser inte problemet brett, eller
- **mjuk G4** ⇒ A-dubbelräkning smyger tillbaka via instrumentnivån.

Därför är **pilotens FÖRSTA uppgift en go/no-go**: finns det ÖVERHUVUDTAGET instrument med en *neutral,
icke-A-dubbelräknande* kvantifierad ambition? Om svaret är "knappt några" är den ärliga slutsatsen att viktad
stance ska byggas **smalt eller inte alls** — inte att tvinga fram den. Detta är inte ett misslyckande; det är
"neutralitet före 4" tillämpat på modellnivå.

---

## 1. Problemet & målet

**Idag är B sign-baserad.** Per (parti, indikator) ([effects.py](../pipeline/effects.py)):

```
num_sum = Σ  w_c · s_c        # w_c = confidence-vikt, s_c = tecken(±1)
abs_sum = Σ |w_c|
net     = clamp(num_sum / abs_sum, -1, 1)        # → net_support_to_score → [0,5], 0 → 2,5
```

`abs_sum` använder `|w_c|` ⇒ **confidence cancelar för samriktade claims** ⇒ "supports" ger `net=+1` oavsett
styrka. Modellen ser *riktning* men inte *grad*, så konsensusmått kollapsar till enhällighet (alla 8 supports,
icke-rankningsdrivande) trots verklig ambitionsskillnad ([done/evidens_trovardighet.md §5.6](done/evidens_trovardighet.md)).

**Mål:** låta B fånga grad **endast där graden kan beläggas värdeneutralt**. B är 35 % av kategoripoängen —
störst hävstång. **Icke-mål:** tvinga fram differentiering; binär fallback är ett fullgott utfall.

---

## 2. Neutralitetsgrindar (G1–G7)

> G6 och G7 är NYA (Codex p.1): de skyddar mot de tilt-vektorer G1–G5 missade — **instrumenturval** och **ankarval**.

- **G1 — Grad endast ur kvantifierad officiell källa.** Magnitud får bara sättas ur en siffra partiet självt
  officiellt anger (budget-/kommittémotion, manifest med konkret målnivå) eller en officiell svensk mätning av
  partiets förslag. Aldrig redaktionellt omdöme. Ingen siffra → binär fallback.
- **G2 — Allt-eller-inget per instrument.** Antingen får *alla* partier med stance på instrumentet en
  kvantifierad magnitud, eller *ingen* (binär fallback för hela instrumentet). Framtvingas i config-validering.
  *(Skyddar mot asymmetrisk datatäckning — men EJ mot urval/ankare; se G6/G7.)*
- **G3 — Symmetri supports/opposes.** Magnitud definieras likadant åt båda håll på samma skala (se §3 formell skala).
- **G4 — Ingen dubbelräkning mot A** (skärpt, se §3). A mäter budget*prioritering* (motionsandel); B-grad mäter
  *instrumentets ambitionsnivå*. **Budgetnära nivåer kräver ett uttryckligt dubbelräkningstest mot A** (§3/§10).
- **G5 — Codex/2nd-opinion per viktat mått.** *Process, ej invariant* — hindrar inte ensamt blocktilt; därför G6/G7 + testbara kriterier (§10).
- **G7 — Hård ankartaxonomi** (NY, Codex p.1). `X_ankare` får INTE väljas fritt. Prioritetsordning:
  1. **Riksdagsbeslutad målnivå** (demokratiskt satt referens; t.ex. 2 % av BNP-beslutet).
  2. **Svensk myndighets behovs-/rekommenderad nivå** (Försvarsberedningen, Socialstyrelsen, Brå …).
  3. Finns ingen av 1–2 → **ingen grad** (binär fallback).
  - **Förbjudna ankare:** högsta partiet (ytterkant sätter skalan); internationellt mål som *primärt* ankare
    (endast bekräftelse, jfr DATA.md); historisk status-quo-nivå (gynnar bevarande-partier); sittande
    regerings budgetpropositionsnivå (gynnar regeringen). Ankarkonkurrenter dokumenteras i ledger (§10 p.10).
- **G6 — Instrumenturvals-neutralitet** (NY, Codex p.2). Viktade instrument får inte plockas opportunistiskt.
  Vid pilot/utrullning **redovisas ALLA kandidatinstrument i kategorin** + varför vart och ett viktades eller
  föll till binärt. Selektivt urval som råkar gynna ett block = tilt, även om varje enskilt mått är neutralt.

---

## 3. Källregel, A-gränsen & den formella skalan

**Grad hämtas ur instrumentets egen kvantifierade ambition, ej budgetens kategori-andel.** Klassificera varje
kandidat-magnitudkälla (Codex p.6):

| Klass | Exempel | A-dubbelräkningsrisk | Regel |
|---|---|---|---|
| **Utfalls-/effektnivå** | RiR/IFAU/SCB-kvantifierad effekt av partiets förslag | låg | Tillåten utan extra test |
| **Icke-budgetär kvantitet** | målnivå i %/antal som ej är ren utgift (svårt — ofta finns inte) | medel | Tillåten, A-test om tveksam |
| **Budgetnära nivå** | försvar % BNP, antal poliser, ersättnings-/täthetsnivåer | **hög** | **Kräver A-dubbelräkningstest (§10); annars binär fallback** |

**A-dubbelräkningstest (budgetnära):** A = motionsandel till kategorin (uppmärksamhet/aktivitet). B-grad = angiven
målnivå. De är konceptuellt skilda (ett parti kan motionera mycket men vilja modest nivå, eller tvärtom). Testet:
visa att B-grad *inte är kollinjär* med A över partierna för instrumentet (känslighets-/korrelationskoll). Är de
~redundanta → binär fallback. **Erkänd huvudrisk (§0):** budgetnära är det vanligaste fallet → fallback blir ofta utfallet.

**Den formella skalan (per instrument, Codex p.5):** varje viktat instrument MÅSTE definiera, i evidensliggaren:
nollpunkt, ankare (G7), riktning, cap-regel (vid värde > ankare), hantering av **målintervall/target**-indikatorer
(där "bättre" = närmare mål, ej "mer"), och hur **opposes** mäts symmetriskt (t.ex. "avveckla helt" = full
motsatt magnitud). Saknas någon del → instrumentet kan inte viktas.

---

## 4. Magnitud-semantik — skilj svagt stöd från neutralt (Codex p.3/p.4)

Problemet i v1: `num_sum += w·s·m` med `m∈(0,1]` drog lågt `m` mot `net=0` (=2,5), oskiljbart från neutral/oklar
stance; och `clamp(...,0,1)` tillät smyg-`m=0`.

**v2-regel — magnitud moduleras INOM den committade riktningens band, korsar aldrig neutralt:**
- `m ∈ [m_min, 1]`, **`m_min` är en sign-off-parameter** (förslag 0,5). `m=0` är **förbjudet** när stance finns
  (det är inte "svagt stöd" — det är ingen stance ⇒ ingen rad).
- supports ⇒ `net ∈ [m_min, 1]` ⇒ score ∈ [`2,5+2,5·m_min`, 5]. Med m_min=0,5: svagast stöd → 3,75; starkast → 5,0.
- opposes ⇒ `net ∈ [-1, -m_min]` ⇒ score ∈ [0, `2,5−2,5·m_min`].
- **Neutral/oklar/ingen rad förblir 2,5** och kan därmed alltid skiljas från "svagt men reellt stöd".
- Grad differentierar alltså *inom* stöd-/motståndsbandet, inte mellan stöd och neutralitet.

Detta bevarar absolut-B (ingen rad → net=0 → 2,5) och löser glidningen + `m=0`-inkonsekvensen.

---

## 5. Två modellalternativ

### Alt A — kontinuerlig magnitud (rekommenderad slutform)
`m_c = clamp(m_min + (1−m_min)·X_parti/X_ankare, m_min, 1)` (linjär i ambition, golvad vid `m_min`, capad vid 1).
Scoring: `num_sum += w·s·m_c`, `abs_sum` oförändrad.
- **+**: minimal kodändring; bevarar absolut-B; en knapp.
- **−**: kräver G7-ankare + §3-skala per instrument.

### Alt B — ambitionsnivå-split
Codex p.7: **Alt B är INTE noll modellrisk och får inte vara scoring-pilot rakt av.** Diskreta steg (2,0/2,5/3,0 %)
är inte neutrala bara för att de är binära, och nested steg **dubbelräknar inom B** (stöd för 2,5 % implicerar
2,0 %) om vikter ej renormaliseras. → Alt B tillåts **endast som icke-scoring datapilot** (kartlägg om neutrala
nivå-källor finns) ELLER med explicit vikt-renormalisering så att samma riktning ej multipliceras.

### Rekommendation
**Fas 1 = icke-scoring datapilot** (Alt B-stil): kartlägg, per kategori, vilka instrument som ens HAR en
G7-konform, icke-A-dubbelräknande kvantifierad nivå (go/no-go §0). **Fas 2 = Alt A** på de instrument som
överlever, med m_min-bandet (§4). Bygg aldrig scoring innan go/no-go är besvarad.

---

## 6. Teknisk design (om/när Alt A byggs)
- `config/party_positions.yaml`: valfritt `magnitude` (float) + obligatorisk `magnitude_source` (kvantifierat
  citat + dok-id) när satt. `stance` oförändrad enum {supports, opposes} (bryter ej `tests/test_fas4.py`).
- `config/evidence_ledger.yaml`: per viktad policy_type ett **`magnitude_scale`-block** (nollpunkt, `magnitude_anchor`
  + ankartyp/källa per G7, riktning, cap, target-hantering, opposes-symmetri).
- `pipeline/positions.py`: propagera `magnitude` (default 1,0).
- `pipeline/effects.py`: `num_sum += w·s·m`; `abs_sum` oförändrad; **clamp `m` till `[m_min,1]`**, hård fel vid `m=0` med stance.
- `pipeline/score.py`: oförändrad.

**Invarianter (framtvingade i test):** (1) `magnitude` saknas överallt ⇒ dist **byte-identisk**. (2) absolut-B
`net=0→2,5`. (3) G2 allt-eller-inget per instrument. (4) `m∈[m_min,1]`, `m=0` förbjudet med stance.
(5) G7: ankartyp ur tillåten lista, annars fel.

---

## 7. Bakåtkompatibilitet
Allt binärt förblir oförändrat i betyg (default `magnitude=1,0`). Viktning är opt-in per instrument; instrument
utan neutral nivå-källa stannar binärt utan kostnad.

---

## 8. Risker
| Risk | Mildring |
|---|---|
| **G4 kollaps (HUVUDRISK §0)** — instrumentmål är budgetproxy | A-dubbelräkningstest (§3/§10); go/no-go-pilot innan bygge; ärligt "smalt eller inte alls" |
| **Instrumenturvals-tilt** | G6: redovisa alla kandidater + bortfallsskäl |
| **Ankar-tilt** | G7 hård taxonomi + förbjudna ankare + ankarkonkurrenter i ledger |
| **Svagt stöd ≈ neutralt** | m_min-band (§4); neutral förblir 2,5 |
| **`m=0`-inkonsekvens** | förbjudet med stance; clamp [m_min,1] |
| **Alt B dubbelräknar inom B** | datapilot eller explicit renormalisering |
| **Komplexitet/överbygge** | default 1,0 + opt-in; go/no-go först |

---

## 9. Fasning
1. **Spike (denna spec + Codex v2-pass):** lås G1–G7, m_min, ankartaxonomi, A-test.
2. **Go/no-go-datapilot (icke-scoring):** per kategori, lista alla kandidatinstrument (G6) + om de har G7-ankare
   utan A-dubbelräkning. Resultat avgör om viktad stance är värd att bygga och hur smalt.
3. **Alt A-bygge** på överlevande instrument med invarianterna §6, codex per mått (G5).
4. **Utvärdering:** neutralitetstester §10 gröna? annars återgå.

---

## 10. Acceptanskriterier & verifiering
- [ ] `magnitude` frånvarande ⇒ `dist/scores.json` **byte-identisk** (golden-test).
- [ ] **Golden-tests edge cases** (Codex p.9): alla `m=1`; alla små `m` (= m_min); blandade riktningar; saknad
  magnitud; `m=0` ⇒ fel; värde > ankare ⇒ capad vid 1; (Alt B) nested thresholds ⇒ renormaliserade.
- [ ] absolut-B (net=0→2,5) golden-testad; m_min-bandet testat (supports aldrig < 2,5+2,5·m_min).
- [ ] G2-validering: blandad täckning på ett instrument ⇒ test failar.
- [ ] G7-validering: ankartyp utanför tillåten lista ⇒ test failar.
- [ ] **Testbar neutralitetskoll** (Codex p.8) — ersätter "manuell granskning": definierad **blocklista**,
  **max tillåten total-förändring relativt binär baseline** (tröskel = sign-off-parameter), **känslighetsanalys**
  för ankare/m_min/trösklar, och **fail-regel** (överskrids tröskeln eller flippar ranking på blocknivå ⇒ HOLD).
- [ ] **A-dubbelräkningstest** per budgetnära instrument: kollinjäritet B-grad vs A under tröskel.
- [ ] **Per-instrument adversariellt protokoll** (Codex p.10): dold tilt-vektor, A-risk, ankarkonkurrenter, och
  *varför binär fallback inte vore mer neutral* — dokumenterat per viktat mått.
- [ ] `pytest -q` grönt, `ruff` rent, cyrillisk-koll 0, `coverage_report`/`score_diff` granskade, codex BUILD/KEEP.

---

## 11. Öppna frågor för sign-off
1. **Go/no-go först:** kör fas-2-datapiloten (icke-scoring) innan något scoring-beslut — OK?
2. **m_min-värde:** 0,5 (förslag) eller annat?
3. **Ankartaxonomi (G7):** godkänn prioritetsordningen + förbudslistan?
4. **Neutralitetströskel:** max tillåten total-förändring relativt binär baseline?
5. **Sekvensering vs D-spåret:** denna spec före D (B = större hävstång) eller D först (lägre risk)? (Beslut 12, öppen.)
6. **Räckvidd:** bara konsensus-mått, eller alla?

---

## 12. Codex-granskningslogg
- **2026-06-07 (v1 → HOLD):** Codex adversariell granskning. Verdikt HOLD: riskområden rätt men spärrar för svaga;
  centrala val (referensnivå/ambitionssteg/manuell neutralitetskoll) odefinierade = tilt-vektor. 10 ändringsförslag.
  **v2 åtgärdar:** G6 instrumenturval (p.2) + G7 ankartaxonomi (p.1); m_min-band skiljer svagt stöd från neutralt +
  förbjuder m=0 (p.3/p.4); §3 3-klass-källtaxonomi + A-dubbelräkningstest, G4-kollaps erkänd som HUVUDRISK §0 (p.6);
  Alt B nedgraderad till datapilot/renormalisering (p.7); formell per-instrument-skala (p.5); testbar neutralitetskoll
  + golden edge cases + per-instrument adversariellt protokoll (p.8/p.9/p.10). **Väntar v2-pass.**

## 13. Relaterat
- [done/evidens_trovardighet.md](done/evidens_trovardighet.md) — B-spårets arbetslogg (§5.6, §8 fråga 2, §9 Beslut 12)
- [fas4b_partistandpunkter_metod.md](fas4b_partistandpunkter_metod.md) — källhierarki, instrument-regeln, grindar
- [../IDEA.md](../IDEA.md), [../DATA.md](../DATA.md) — grundprincip & datamodell
- [../config/scoring.yaml](../config/scoring.yaml), [../pipeline/effects.py](../pipeline/effects.py), [../pipeline/score.py](../pipeline/score.py)
