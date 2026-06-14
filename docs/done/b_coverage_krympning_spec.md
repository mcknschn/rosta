# Rösta - Spec: B-undermåttsbreddskrympning (BACKLOG B5)

> **Status: ✅ LEVERERAD OCH AKTIVERAD. `coverage_mode: weighted_submeasure_depth` är default
> i config sedan §10.7-sign-offen 2026-06-14; `dist/` omräknad och snapshot rebaselinad
> (ranking S > L > M > MP > KD > C > SD > V). §10.1–10.7 SIGNADE (design, nämnare, KD↔MP-flip,
> tröskel 0,5, flaggformat, B-breddgrind, default-switch — se §11). Legacy `policy_type_count`
> finns kvar via config-override (byte-identisk med sig själv). Arkiverad till done/ — ingen
> öppen fråga kvar.**
>
> Systerspec till den levererade D-specen
> [d_coverage_krympning_spec.md](d_coverage_krympning_spec.md) och speglar dess
> struktur och beslutsmodell. B har redan en runtime-krympning (åtgärdstyps-täckning, Fas 4b'),
> men den krymper efter **antal kodade åtgärdstyper**, inte efter **undermåttsbredd** — en
> kategori vars B-evidens bara når en delmängd av undermåtten gör ändå ett oavkortat
> kategorianspråk. Det är samma renormaliseringsproblem som D hade, fast en nivå upp
> (nämnaren är liggarens innehåll i stället för kategorins anspråk). Kärnrisken som öppnade
> B5 (D-spec §8 / BACKLOG): en extra B-krympning kan **dubbelrabattera** mot den befintliga
> åtgärdstyps-krympningen — den frågan utreds formellt i §3.
>
> ⚠️ Till skillnad från D-ändringen (D väger 10 %) är detta **rankingrelevant**: B väger 35 %
> av kategoribetyget, och den rekommenderade formeln flyttar totaler upp till ±0,06 och
> byter en rankingplats (KD↔MP, se §5 och Bilaga A). Det måste accepteras explicit i §10.
>
> Relaterat: [d_coverage_krympning_spec.md](d_coverage_krympning_spec.md),
> [BACKLOG.md B5/B4](../BACKLOG.md), [evidens_trovardighet.md](evidens_trovardighet.md),
> [../../config/scoring.yaml](../../config/scoring.yaml), [../../pipeline/scorerun.py](../../pipeline/scorerun.py),
> [../../pipeline/score.py](../../pipeline/score.py), [../../pipeline/tools/coverage_report.py](../../pipeline/tools/coverage_report.py).
>
> Begreppsmodell: **Kategori -> Undermått -> Indikator -> Riktning**.

---

## 0. Kärnbeslut

B ska, precis som D, mäta partiets evidensläge för en **kategori**, inte bara för de undermått
där liggaren råkar ha kodbara åtgärdstyper. Därför ska B:s täckningsmått inte längre
renormalisera bort undermått som saknar kodbart instrument, och inte heller vikta undermåtten
efter hur många instrument liggaren råkar innehålla.

**Rekommendation för implementering:**

1. **ERSÄTT** dagens antalsbaserade åtgärdstyps-täckning med ETT enhetligt mått —
   **viktad undermåttsdjuptäckning** `cov_B` (§3.3) — i stället för att komponera två
   rabatter (multiplikativt eller max). Det enhetliga måttet innehåller både bredd
   (vilka undermått) och djup (andel kodade instrument inom undermåttet) exakt en gång,
   så dubbelrabatten (§3.2) uppstår aldrig.
2. Nämnaren = **kategorins icke-target-undermått viktade ur `categories.yaml`** — samma
   nämnare och samma maskinläsbara definition som D (`_d_denominator_submeasures`).
   Undermått utan kodbart instrument (B-väggar) **stannar i nämnaren** med bidrag 0.
3. Numeratorn är **per parti och kategori**: undermåttets vikt × andelen av undermåttets
   kodbara åtgärdstyper partiet har en aktiv ståndpunkt på.
4. Krympformeln är oförändrad i form: `B_just = 2.5 + (B_raw - 2.5) * cov_B`
   (återanvänder `score.coverage_shrink`).
5. Lägg `B_coverage_<covered_weight>/<total_weight>` i `scores.json` (ersätter dagens
   antalsflagga `B_coverage_<num>/<den>` i den nya moden); `B_thin_coverage` behålls
   med tröskel 0,5 på det nya måttet.
6. Gate:a bakom `B_evidens.coverage_mode` (`policy_type_count` = legacy, byte-identisk
   baseline; `weighted_submeasure_depth` = ny) — samma utrullningsmönster som D:s
   `coverage_shrink`.
7. Behåll B4-grinden (`b_submeasure_spread`) som offline-regressionsgrind; utöka
   `coverage_report` med en viktad B-breddssektion (spegel av `d_submeasure_breadth`).
8. Rör inte D, inte `aggregate_B`:s inre rollup, och inte stance-kodningen.

Varför ersätta i stället för att lägga till: dagens mått och ett breddmått överlappar — ett
parti utan ståndpunkt i ett otäckt undermått förlorar täljarmassa i **båda** (§3.2). Att
multiplicera dem kvadrerar i praktiken breddrabatten (empiriskt: MP/försvar 0,25 → 0,0625
utan att någon ny information tillkommit, §3.2). Det enhetliga måttet är dessutom det som
D-specen redan valde bort antalsräkning till förmån för: en täckt 30-procentsdel ska inte
räknas som lika stor som en täckt 10-procentsdel — och i dag viktas undermåtten implicit
efter liggarens instrumentantal, vilket är en källartefakt, inte en modellvikt.

---

## 1. Problemet i dagens kod

B-vägen i [pipeline/scorerun.py](../../pipeline/scorerun.py) bygger täckningen på
ÅTGÄRDSTYPS-nivå (Fas 4b'):

```python
cov_den: dict[str, set[str]] = {}  # kategori -> kodbara åtgärdstyper (signed != 0, ej exkluderade)
for e in ledger_entries:
    if signed.get(e["direction"], 0) != 0 and e["policy_type"] not in b_exclude:
        cov_den.setdefault(e["category"], set()).add(e["policy_type"])
cov_num: dict[tuple[str, str], set[str]] = {}  # (parti, kategori) -> kodade åtgärdstyper
```

och krymper sedan:

```python
b_raw = score.aggregate_B(b_inputs, b_weights, missing_all_score=b_missing)
b_val = 2.5 + (b_raw - 2.5) * coverage  # krymp mot neutral efter täckning
```

`aggregate_B` i [pipeline/score.py](../../pipeline/score.py) renormaliserar samtidigt B-värdet
över de indikatorer som har effekt:

```python
present = {k: v for k, v in indicator_net_support.items() if v is not None}
wsum = sum(indicator_weights.get(k, 0.0) for k in present)
...
return clamp(sum(net_support_to_score(present[k]) * indicator_weights.get(k, 0.0) for k in present) / wsum)
```

Det ger två principfel, båda av samma art som D:s gamla renormalisering:

1. **Undermått utan kodbart instrument försvinner ur nämnaren.** `cov_den` byggs ur
   liggaren — ett undermått där ingen åtgärdstyp kodats (B-vägg eller obyggt) bidrar med
   noll typer och är därmed osynligt. Integration har i dag kodbara instrument i bara
   3 av 5 undermått (65 % av kategorivikten, §2), men C och KD når ändå `coverage = 5/5
   = 1.0` och gör ett **oavkortat kategorianspråk B = 5,00** — trots att 35 % av
   kategorins anspråk (boendesegregation + normer_tillit) saknar all B-evidens.
   `aggregate_B`:s renormalisering över indikatorer med effekt sluter cirkeln: värdet
   låtsas tala för hela kategorin.
2. **Undermåtten viktas implicit efter liggarens instrumentantal, inte efter
   `categories.yaml`.** I demokrati har korruption_tillit 3 av kategorins 7 kodbara typer
   (43 % av täckningsmåttet) men modellvikt 20 %. Ett parti som saknar 2 av 3
   korruptionstyper (M/V/KD) straffas i dag som om 29 % av kategorin saknades, fast alla
   5 undermått är evidenstäckta. Det är exakt den antalsräkning D-specen förkastade.

`b_submeasure_spread`-grinden (B4) ser nära-binär bredd offline, men ändrar inget betyg:
den är en varningslampa, inte en krympning (§3.5).

---

## 2. Aktuellt täckningsläge

Verifierat 2026-06-12 med `python -m pipeline.tools.coverage_report` (B-spridningssektionen)
plus en read-only-härledning av kodbara typer per undermått ur config. OBS: B4-tabellen i
BACKLOG är delvis inaktuell (skriven 2026-06-05/06) — siffrorna nedan är dagens.

**Undermått med AKTIV partikopplad B-evidens (B4-spridningen, kategori-global):**

| Kategori | Undermått m. aktiv evidens | Kodbara åtgärdstyper (`cov_den`) | Otäckta undermått |
|---|---:|---:|---|
| ekonomi | 4/6 | 5 | inflation_prisstabilitet, offentliga_finanser (target-only) |
| valfard | 4/4 | 6 | — |
| trygghet | 5/5 | 6 | — |
| forsvar | 4/5 | 4 | genomforbarhet_leverans (B-vägg) |
| klimat | 4/5 | 4 | industriell_konkurrenskraft (saknar indikator) |
| integration | 3/5 | 5 | boendesegregation, normer_tillit (B-väggar) |
| demokrati | 5/5 | 7 | — |

**Viktat B-breddstak per kategori** (om ALLA kodbara typer kodas; nämnare = icke-target-vikt
ur `categories.yaml`, samma som D):

| Kategori | Tak (vikt) | Kvot | Kommentar |
|---|---:|---:|---|
| ekonomi | 73/73 | 1.00 | target-only-undermåtten (12+15) ur nämnaren, som i D |
| valfard | 100/100 | 1.00 | |
| trygghet | 100/100 | 1.00 | |
| forsvar | 95/100 | 0.95 | genomforbarhet_leverans (5) saknar kodbar typ |
| klimat | 85/100 | 0.85 | industriell_konkurrenskraft (15) saknar indikator/typ |
| integration | 65/100 | 0.65 | boendesegregation (20) + normer_tillit (15) = B-väggar |
| demokrati | 100/100 | 1.00 | |

Två lägesnoteringar:

- **Inga nära-binära kategorier** finns kvar (B4-grindens `b_near_binary_accepted` är tom).
  Problemet är inte längre 1/5-bredd utan att 2/5–4/6-bredd inte syns i betyget alls.
- En åtgärdstyp kan mata **flera undermått**: `koldioxidskatt` ligger i både
  utslappsminskningar och kostnadseffektivitet (två liggarposter, samma typ). Dagens
  antalsmått räknar den en gång i `cov_den`; undermåttsdekompositionen är alltså ingen
  partition — formellt hanterat i §3.1.

---

## 3. Formell modell

### 3.1 Definitioner

För kategori `c` och parti `p`:

- `S_den(c)` = kategorins **icke-target-undermått** enligt exakt samma definition som D
  (`_d_denominator_submeasures`): target-only ⇔ undermåttet har ≥1 indikator och alla har
  `direction: target`; undermått **utan** indikatorer ingår i nämnaren.
- `w_s` = undermåttets vikt i `categories.yaml`; `W(c) = Σ_{s∈S_den} w_s`.
- `T_s(c)` = kodbara åtgärdstyper vars liggarpost pekar på en indikator i `s`
  (signed_direction ≠ 0, ej `coverage_exclude`). En typ kan ligga i flera `T_s`
  (koldioxidskatt) — då bidrar en ståndpunkt på den med djup i varje undermått dess
  evidens faktiskt matar. Det är avsiktligt: ståndpunkten informerar båda anspråken.
- `K_s(p,c) = T_s ∩ {partiets kodade åtgärdstyper}`.
- `djup_s(p,c) = |K_s| / |T_s|` om `T_s ≠ ∅`, annars `0` (B-vägg ⇒ noll kunskap).

Dagens mått (för jämförelse): `cov_pt(p,c) = |∪K_s| / |∪T_s|` (antal distinkta typer,
oviktat, nämnaren = bara liggarens innehåll).

Ett rent breddmått (för jämförelse): `cov_bredd(p,c) = Σ_{s: K_s≠∅} w_s / W`.

### 3.2 Dubbelrabatten — kvantifierad, och varför komposition förkastas

Saknar partiet ståndpunkt på alla typer i undermåttet `s` förlorar det täljarmassa i
**båda** måtten samtidigt: `|T_s|/|∪T_s|` av `cov_pt` **och** `w_s/W` av `cov_bredd`.
De två måtten skiljer sig bara genom (a) viktning (antal vs `categories.yaml`-vikt) och
(b) att `cov_pt` även rabatterar delvis kodade undermått. I det vanligaste fallet —
**ett kodbart instrument per undermått** (`|T_s| = 1` för alla `s`, vilket gäller hela
försvar och nästan hela trygghet/valfard) — mäter de **exakt samma sak** med olika vikter.

Faktiskt exempel ur configen (försvar, 4 kodbara typer i 4 undermått à 35/25/20/15;
genomforbarhet_leverans 5 saknar typ):

| Parti | `cov_pt` (idag) | `cov_bredd` | (b) multiplikativt | (c) max-rabatt = min(cov) |
|---|---:|---:|---:|---:|
| MP (1 typ kodad) | 0.25 | 0.25 | **0.0625** | 0.25 |
| C/KD (3 typer) | 0.75 | 0.75 | **0.5625** | 0.75 |
| S/M/SD/V/L (4 typer) | 1.00 | 0.95 | 0.95 | 0.95 |

- **(b) multiplikativ komposition förkastas.** När måtten sammanfaller kvadreras rabatten:
  MP:s försvars-B skulle gå 3,12 → 2,66 utan att någon ny information tillkommit — samma
  saknade ståndpunkt straffas två gånger. Totaleffekten är systematiskt ensidig (alla
  partier −0,04…−0,13, §5) eftersom de två faktorerna är starkt korrelerade per
  konstruktion, inte ortogonala.
- **(c) max av rabatterna (= min av täckningarna) förkastas.** Den undviker dubbelräkning
  men är ad hoc: den ärver antalsmåttets liggarviktning så fort `cov_pt < cov_bredd`
  (demokrati M: min = 0,714 styrt av 5/7 typer trots full 5/5-bredd) och kastar bort
  djupinformation åt andra hållet. Den saknar dessutom D-parallellens semantik (fast
  nämnare med neutralt bidrag).
- **(a) ERSÄTT med ett enhetligt mått rekommenderas** (§3.3): bredd och djup ingår exakt
  en gång, viktade ur `categories.yaml`, över en fast nämnare.

### 3.3 Det enhetliga måttet: viktad undermåttsdjuptäckning

```text
cov_B(p,c) = Σ_{s ∈ S_den(c)} w_s * djup_s(p,c)  /  W(c)

B_just(p,c) = 2.5 + (B_raw(p,c) - 2.5) * cov_B(p,c)
```

`cov_B` faktoriseras exakt som `bredd × djup-givet-bredd`:

```text
cov_B = [Σ_{s:K_s≠∅} w_s / W] * [Σ_{s:K_s≠∅} w_s*djup_s / Σ_{s:K_s≠∅} w_s]
```

dvs. den ÄR den multiplikativa kompositionen av bredd och **betingat** djup — det enda sätt
på vilket de två dimensionerna kan komponeras utan överlapp. Specialfall som visar att
måttet är en konservativ generalisering: om alla `|T_s| = 1` och vikterna är lika är
`cov_B = cov_pt = cov_bredd` (försvar i tabellen ovan: 0,25/0,75/0,95 ≈ dagens värden).

Varför `B_raw × cov_B` och inte D:s direkta neutral-missing-rollup
(`weighted_mean_with_neutral_missing`): D:s numerator per undermått är ett **värde**
(medelnet av serier — finns eller finns inte), medan B:s numerator har en äkta
**djupdimension** (2 av 3 instrument kodade är varken 0 eller 1). En neutral-missing-
rollup på undermåttsnivå skulle räkna ett 1/3-kodat undermått som fullt täckt.
Krympfaktor-formen behåller djupet; matematiken är ändå D-ekvivalent i breddledet
eftersom `net_support_to_score` och krympningen är linjära (jfr D-spec §3.3).

### 3.4 Nämnaren: varför D:s icke-target-definition — och varför inte alternativen

Frågan "vilka undermått är B-bara?" måste avgöras maskinellt. Kandidater:

1. **Icke-target-undermått ur `categories.yaml` (= D:s nämnare). REKOMMENDERAS.**
   Maskinläsbar, redan implementerad (`_d_denominator_submeasures`), och ger B och D
   **samma kategorianspråk**: target-only-undermått (inflation, offentliga_finanser) tar
   inget riktat B-bidrag (B4-fyndet 2026-06-05 — target-indikatorer har ingen B-bar
   riktning) och lyfts ur nämnaren på samma dokumenterade grund som i D. Undermått utan
   indikatorer (industriell_konkurrenskraft) ingår, som i D: de är en del av anspråket.
   Konsekvensen att B-väggar (boendesegregation, normer_tillit, genomforbarhet_leverans)
   permanent sänker taket (integration max 0,65) är **avsikten**, inte en bugg: B vet
   faktiskt ingenting om de delarna, och krympning mot neutral är **symmetrisk kring
   2,5** — den gynnar inget håll på betygsskalan. Men den är **inte lika-delta**:
   partier med högt `|B_raw − 2,5|` i en berörd kategori förlorar mer i absoluta
   betygspoäng än partier nära neutral (C/KD:s oavkortade integration-5,00:or tappar
   mest; V, under neutral, vinner). Den effektbilden är skriptat verifierad och
   redovisas öppet i **Bilaga A** — den ska accepteras vid sign-off, inte gömmas
   bakom ordet "neutral" (jfr B-grön-mandatet: väggarna ska byggas bort, inte
   definieras bort).
2. **"Undermått med ≥1 kodbar åtgärdstyp i liggaren". FÖRKASTAS.** Självrefererande:
   liggaren är täljarens källa — låter man den också definiera nämnaren återuppstår
   renormaliseringsproblemet en nivå upp (ett okodat undermått lämnar tyst anspråket),
   med det perversa incitamentet att aldrig koda svåra undermått. Det är exakt dagens
   `cov_den`-fel.
3. **Explicit config-lista med grind (à la `coverage_exclude`/E1-E2). FÖRKASTAS som
   nämnardefinition, hålls som framtida ventil.** Dokumenterade "EJ B-bart"-verdikt är
   i praktiken **indikator-/instrumentnivå**, inte undermåttsnivå — kronexemplet är
   `realloner_hushall`: reallöneindikatorn är EJ B-bar (parterna sätter lön), men
   undermåttet öppnades senare via systerindikatorn `hushallens_reala_disponibla_inkomst`.
   En undermåttsexkludering 2026-06-05 hade varit fel i efterhand. Om ett framtida,
   genuint strukturellt omöjligt undermått uppstår kan en principgrundad
   `b_breadth_exclude` med skälsregister läggas till (spegel av E1/E2) — **startvärde:
   ingen lista alls**.

### 3.5 Interaktion med B4-grinden (`b_submeasure_spread`)

Krympningen gör nära-binär bredd **ekonomiskt verkningslös att gama**: en kategori vars
B-evidens vilar på ett enda undermått får `cov_B ≤ max(w_s)/W ≤ 0,35`, dvs. B kan som mest
nå `2,5 ± 0,875` i stället för dagens `2,5 ± 2,5` vid fullkodat enda undermått. En enda
ståndpunkt kan inte längre svinga kategorin mellan ytterlägen.

Blir B4-grinden redundant? **Nej — den behålls, med omformulerad roll** (samma beslut som
D-specen tog när D-breddgrinden behölls trots runtime-krympning):

- Grinden är **offline/config-nivå** (fångar liggarregression i test, före scoring);
  krympningen är **runtime/betygs-nivå** (epistemisk ärlighet i utdata). Ortogonala lager.
- Grinden bär **allowlist-semantiken** (`b_near_binary_accepted` = människosignerad
  acceptans av tunn bredd) — krympningen har ingen sign-off-kanal.
- Grindens tröskel (≤1 undermått) och krympningens flagga (`cov_B < 0,5`) överlappar men
  sammanfaller inte: ett 2/5-täckt undermåttspar kan passera grinden men flaggas tunt.

`coverage_report`-texten för B4-sektionen uppdateras så den hänvisar till krympningen i
stället för till "coverage-krympningen ... löser inte detta" (det stycket blir delvis
överspelat när B5 levereras).

### 3.6 Gate och fallback

Oförändrade: `b_inputs` tomt eller täckning 0 → `missing_all_score` 2,5 +
`B_no_party_evidence` + `missing_all_confidence`. Kantfall som ska testas: en kodad typ
vars indikator ligger i ett target-only-undermått skulle ge `b_inputs ≠ ∅` men bidrar inte
till `cov_B`-täljaren (utanför nämnaren); gaten ska då använda `cov_B > 0`, inte
`cov_pt > 0` (i dag finns ingen sådan post i liggaren, men grinden ska inte bero på det).

---

## 4. Confidence och flaggor

Nya/ändrade konfignycklar i `config/scoring.yaml` under `B_evidens`:

```yaml
coverage_mode: policy_type_count   # legacy (byte-identisk baseline); ny: weighted_submeasure_depth
coverage_denominator: non_target_submeasure_weight   # dokumenterar nämnarens semantik (samma som D)
thin_coverage_threshold: 0.5       # oförändrad nivå, mäts på cov_B i nya moden
```

Confidence-logik (oförändrad i form): B = `medium` när evidens finns; `cov_B <
thin_coverage_threshold` → sänk till `low` + flagga `B_thin_coverage`.

Flaggor i `scores.json` (nya moden):

- `B_coverage_<covered_weight>/<total_weight>` där `covered_weight = Σ w_s*djup_s` och
  `total_weight = W(c)`. **Formatet är LÅST och deterministiskt:** `covered_weight`
  kan bli icke-heltal pga `|K_s|/|T_s|`-bråken (demokrati M: 86,666…) och skrivs som
  `f"{round(covered_weight, 1):g}"` — avrundas till 1 decimal, heltal skrivs utan
  decimal (M/demokrati ⇒ exakt `B_coverage_86.7/100`; full täckning ekonomi ⇒
  `B_coverage_73/73`). `total_weight` är alltid heltal ur `categories.yaml` och
  skrivs `:g`. Ersätter antalsflaggan `B_coverage_<num>/<den>` — antalsbilden finns
  kvar i `coverage_report`.
- `B_thin_coverage` om `cov_B < 0,5`.
- `B_no_party_evidence` oförändrad.

Med tröskel 0,5 flaggas i dagens dataläge ungefär: MP/integration (0,20), MP/försvar
(0,25), S/integration (0,30), C/klimat (0,30), SD/V/integration (0,45), M/C/trygghet
(0,425) — fler än i dag (i dag bara `cov_pt < 0,5`), vilket är avsikten: tunn bredd ska
synas. En höjning till 0,6 skulle även fånga C/KD/integration (0,65 ligger strax över) —
se §10.

---

## 5. Förväntad effekt

B väger **35 %** av kategoribetyget — tio gånger D-ändringens hävstång. Räknat på dagens
config (`b_raw` via `positions`/`effects`/`aggregate_B`, vikter ur `categories.yaml`,
read-only 2026-06-12):

**Integration** (nämnare 100; B-väggarna boendesegregation 20 + normer_tillit 15 i nämnaren):

| Parti | `cov_pt` idag | B idag | `cov_B` | B förslag (a) | Δ B |
|---|---:|---:|---:|---:|---:|
| C | 1.000 | 5.00 | 0.650 | 4.12 | −0.88 |
| KD | 1.000 | 5.00 | 0.650 | 4.12 | −0.88 |
| M | 0.800 | 4.50 | 0.550 | 3.88 | −0.62 |
| L | 0.800 | 4.50 | 0.550 | 3.88 | −0.62 |
| SD | 0.600 | 4.00 | 0.450 | 3.62 | −0.38 |
| S | 0.600 | 3.57 | 0.300 | 3.04 | −0.53 |
| MP | 0.400 | 3.00 | 0.200 | 2.75 | −0.25 |
| V | 0.600 | 2.41 | 0.450 | 2.43 | +0.02 |

C/KD är flaggskepps-exemplet på dagens hål: full åtgärdstyps-täckning (5/5) → oavkortat
B = 5,00 trots att 35 % av kategorivikten saknar all B-evidens.

**Demokrati** (nämnare 100; full bredd 5/5, men antalsmåttet liggarviktar korruption 3/7):

| Parti | `cov_pt` idag | B idag | `cov_B` | B förslag (a) | Δ B |
|---|---:|---:|---:|---:|---:|
| M | 0.714 | 3.57 | 0.867 | 3.80 | +0.23 |
| V | 0.714 | 4.29 | 0.867 | 4.67 | +0.38 |
| KD | 0.714 | 3.57 | 0.867 | 3.80 | +0.23 |
| SD | 0.714 | 3.33 | 0.683 | 3.30 | −0.03 |
| MP | 0.857 | 4.64 | 0.933 | 4.83 | +0.19 |
| S/C/L | 1.000 | of. | 1.000 | of. | 0 |

Här **lossar** förslaget: full undermåttsbredd med partiellt instrumentdjup straffas
mildare än i dag — antalsmåttets implicita 43-procentsviktning av korruption_tillit
ersätts av modellens 20.

**Total- och rankingeffekt** (Δ applicerad på dagens `dist/scores.json`-totaler,
standardvikter):

| Parti | Total idag | (a) ersätt `cov_B` | (b) multiplikativt |
|---|---:|---:|---:|
| S | 3.683 | 3.637 (−0.045) | 3.560 (−0.123) |
| L | 3.389 | 3.356 (−0.033) | 3.293 (−0.096) |
| M | 3.321 | 3.278 (−0.043) | 3.231 (−0.090) |
| KD | 3.152 | 3.111 (−0.041) | 3.050 (−0.102) |
| MP | 3.112 | 3.126 (+0.013) | 3.041 (−0.072) |
| C | 3.077 | 3.015 (−0.062) | 2.946 (−0.131) |
| SD | 2.727 | 2.713 (−0.013) | 2.656 (−0.071) |
| V | 2.621 | 2.644 (+0.023) | 2.583 (−0.039) |

- **(a) byter EN rankingplats: KD↔MP** (KD 3,111 vs MP 3,126; ny marginal 0,014 mot
  dagens +0,040 — långt inom osäkerhetsintervallen, men en faktisk platsväxling).
  Drivare: KD tappar integrationens oavkortade 5,00:a; MP vinner netto på
  demokrati-/valfards-/trygghetslossningen. Mönstret följer dagens täcknings- och
  viktläge, inte en partisk regel — men krympningen är symmetrisk mot 2,5, **inte
  lika-delta**: partier med högt B_raw i berörda kategorier förlorar mer. I dagens
  dataläge betyder det att regeringspartierna M/KD/L tappar −0,03…−0,04, C mest
  (−0,062), S −0,045, medan MP/V gör små vinster (+0,013/+0,023). Det ska redovisas
  öppet före sign-off, inte avfärdas som "straffar alla lika" — fullständig verifierad
  effektbild i **Bilaga A**.
- **(b) sänker alla** (−0,04…−0,13) — den ensidiga signaturen av dubbelrabatt; ranking
  råkar bevaras men kompressionen mot neutral är dubbelt så stor utan informationsgrund.
- Per-cell-effekterna är större än D-ändringens (största |Δkategori| ≈ 0,88 × 0,35 ≈ 0,31
  mot D:s ≈ 0,15 × 0,10 ≈ 0,015 i totalled).

---

## 6. Teknisk design

### 6.1 `pipeline/score.py`

`coverage_shrink` finns redan och återanvänds oförändrad. Ny ren, golden-testbar helper:

```python
def weighted_depth_coverage(
    coded: Mapping[str, AbstractSet[str]],     # undermått -> partiets kodade typer i undermåttet
    codable: Mapping[str, AbstractSet[str]],   # undermått -> kodbara typer (T_s)
    weights: Mapping[str, float],
    denominator_keys: Iterable[str],
) -> tuple[float, float]:
    """(covered_weight, total_weight): Σ w_s*|K_s|/|T_s| över fast nämnare; T_s=∅ -> 0."""
```

`weighted_mean_with_neutral_missing` lämnas orörd (D:s väg); `aggregate_B` lämnas orörd
(§8).

### 6.2 `pipeline/scorerun.py`

- Bryt ut nämnarhelpern: `_d_denominator_submeasures()` döps om/aliasas till en delad
  `_non_target_submeasures()` (samma beteende; D-anropen oförändrade) — B och D ska
  bevisligen dela definition, inte duplicera den.
- Ny helper `_b_codable_types_by_submeasure()`: kategori -> undermått -> set kodbara
  åtgärdstyper (ur liggaren: signed ≠ 0, ej `coverage_exclude`, indikatorns undermått).
  Ersätter/kompletterar dagens platta `cov_den`.
- `cov_num` per (parti, kategori) behålls men struktureras per undermått
  (`(p, c) -> {undermått -> kodade typer}`).
- Huvudloopen:

```python
if coverage_mode == "weighted_submeasure_depth":
    covered_w, total_w = score.weighted_depth_coverage(
        k_by_sub, t_by_sub, sub_w.get(c, {}), nontarget[c]
    )
    cov = covered_w / total_w if total_w else 0.0
    b_val = score.coverage_shrink(b_raw, cov)
    b_flags.append(f"B_coverage_{round(covered_w, 1):g}/{total_w:g}")  # låst format, §4
else:  # policy_type_count — legacy, byte-identisk
    ...dagens block oförändrat...
```

Gaten (`b_inputs and cov > 0`) använder den aktiva modens täckning (§3.6).

### 6.3 `coverage_report`

Ny sektion `b_submeasure_breadth()` — spegel av `d_submeasure_breadth` (offline, endast
config): viktat **tak** per kategori (alla kodbara typer kodade) + per-undermått
otäckt-lista. Förväntad utskrift i dagens läge:

```text
== B-undermåttsbredd (coverage_mode: …, tröskel 0.5) ==
  ekonomi       73/73   1.00
  valfard      100/100  1.00
  trygghet     100/100  1.00
  forsvar       95/100  0.95
  klimat        85/100  0.85
  integration   65/100  0.65
        otäckta: boendesegregation, normer_tillit
  demokrati    100/100  1.00
```

(Notera ekonomi `73/73`, inte `100/100` — heltalsvikter, target-only ur nämnaren; samma
konvention som D-sektionen.) `b_submeasure_spread` (B4) behålls; dess docstring/utskrift
uppdateras per §3.5. Taket är kategori-globalt; scoringens `cov_B` är per parti/kategori.

### 6.4 Eventuell B-breddgrind

Spegla D:s `d_thin_breadth_accepted`: kategori vars **tak** < 0,75 måste stå i
`coverage_allowlist.b_thin_breadth_accepted` med skäl (i dag: integration 65/100), annars
testfel. Gör B-väggarnas kostnad människosignerad i stället för tyst. (Sign-off §10.)

---

## 7. Tester och acceptanskriterier

- `weighted_depth_coverage`: full täckning → `(W, W)`; tom → `(0, W)`; `T_s = ∅` ger 0 i
  täljaren men `w_s` kvar i nämnaren; delvis kodat undermått ger proportionellt bidrag;
  typ i flera undermått bidrar i varje; monotoni i antal kodade typer.
- `coverage_mode: policy_type_count` ger **byte-identiskt** `dist/scores.json` mot före
  ändringen.
- `cov_B = 1` ⇒ `B_just = B_raw`; `cov_B = 0` ⇒ neutral 2,5.
- Target-only-undermått ingår inte i nämnaren; undermått utan indikatorer ingår
  (delad helper med D — ett test låser att B och D använder SAMMA nämnarfunktion).
- Kodad typ mot target-only-undermått bidrar inte till täljaren; gaten använder `cov_B`
  (§3.6-kantfallet, fixturtest).
- Krympningen bevarar partiordning inom kategori vid lika täckning; olika täckning kan
  ändra ordning (dokumenterat förväntat — integration C/KD vs V).
- `scores.json` innehåller `B_coverage_<covered>/<total>` i det LÅSTA formatet (§4) i
  nya moden; `B_thin_coverage` triggar på `cov_B < 0,5`; `B_no_party_evidence`-celler
  får ingen `B_coverage_*`.
- `coverage_report` visar B-breddstak per kategori; B4-sektionen kvar och grön.
- Ev. B-breddgrind: integration utan allowlist-post ⇒ rött; med post ⇒ grönt.

**Anti-gaming-acceptanstester för `|K_s|/|T_s|` (P1, Codex-granskningen):**

- **Dedup inom undermått:** dubblerad `policy_type` i samma undermått (två liggarposter,
  samma typ, samma undermått) dedupliceras — `T_s` och `K_s` är mängder, `|T_s|` ökar
  inte och `djup_s` påverkas inte (set-semantik, fixturtest).
- **En gång PER undermått:** samma `policy_type` i flera undermått (koldioxidskatt-fallet,
  §2/§3.1) bidrar exakt en gång per undermått dess evidens matar — kodad ståndpunkt höjer
  `djup_s` i varje berört undermått, men aldrig dubbelt inom samma undermått (fixturtest).
- **Triviala/duplikativa åtgärdstillägg** som enbart skulle blåsa upp `cov_B` blockeras
  av Fas 4c-reglerna: inget täckningsmål får styra liggarens innehåll (§8 — liggaren
  röres inte av täckningsskäl) och exkludering är principgrindad (`coverage_exclude`
  med skälsregister). **Uttryckligt acceptanskriterium:** varje liggarändring ska
  åtföljas av en `coverage_report`-diff som granskas (cov_B-/breddförändring per
  kategori redovisad i ändringen) — täckningsdrift får aldrig passera tyst.

**Config- och formattester (P2, Codex-granskningen):**

- Ogiltigt `B_evidens.coverage_mode`-värde (annat än `policy_type_count` /
  `weighted_submeasure_depth`) ⇒ **hard fail** i `config.validate` — ingen tyst
  fallback till legacy.
- Flaggformatet är deterministiskt enligt det låsta formatet (§4): fixturtest
  M/demokrati (86,666… → exakt `B_coverage_86.7/100`) och heltalsfall
  (ekonomi full täckning → `B_coverage_73/73`, ingen `73.0`).
- `pytest -q` grönt; `ruff` rent.
- `python -m pipeline.scorerun` körs med nya moden och **score-diff per cell, kategori
  och total redovisas TILLSAMMANS med en CI-överlapp-/rankingnot** (KD↔MP-bytet
  förväntat, §5/Bilaga A) innan `dist/` rebaselinas.

---

## 8. Scope-avgränsning: vad som INTE ändras

- **D röres inte** — D:s krympning är levererad och mätt; denna spec är B-sidan.
- **`aggregate_B`:s inre rollup röres inte.** Känd kvarvarande egenhet: två indikatorer i
  samma undermått får var sin full undermåttsvikt i indikatorsnittet (ingen
  inom-undermåtts-medelvärdesbildning som D:s `by_sub`). Ortogonal fråga; om den ska
  åtgärdas är det en egen spec — att fixa den samtidigt skulle förorena diffen.
- **Stance-kodningen röres inte** — binär stance ligger fast (viktad stance utvärderad
  och FÖRKASTAD 2026-06-07; återföreslås inte).
- **B4-grindens allowlist-semantik** (`b_near_binary_accepted`) behålls oförändrad (§3.5).
- **Liggarens innehåll** röres inte — specen ändrar hur täckning mäts, inte vad som är
  kodbart. B-väggarna (boendesegregation, normer_tillit, genomforbarhet_leverans,
  industriell_konkurrenskraft) byggs bort i Spår B/B2, inte här.

---

## 9. Implementeringsordning

1. Lägg in confignycklar med `coverage_mode: policy_type_count` (legacy) — byte-identisk
   golden-baseline.
2. Ny ren helper + tester i `score.py` (`weighted_depth_coverage`).
3. Delad nämnarhelper i `scorerun.py` (`_non_target_submeasures`, D-anrop oförändrade)
   + `_b_codable_types_by_submeasure` + per-undermått `cov_num`.
4. Mode-växeln i huvudloopen; flaggor/confidence följer med.
5. Utöka `coverage_report` (`b_submeasure_breadth`) + ev. B-breddgrind (§6.4, efter §10).
6. Kör testsvit (legacy-mode byte-identisk verifierad).
7. Kör scorerun i nya moden; redovisa score-diff per cell/kategori/total + CI-överlapp-/
   rankingnot (KD↔MP förväntat, Bilaga A) för granskning.
8. Efter sign-off: slå om till `weighted_submeasure_depth` och rebaselina `dist/` + snapshot.

---

## 10. Öppna sign-off-frågor

1. **Kompositionsbeslutet (§3.2-3.3):** godkänns **(a) ERSÄTT** antalsmåttet med enhetlig
   viktad undermåttsdjuptäckning `cov_B` (rekommenderas), eller ska (b) multiplikativ /
   (c) max-rabatt väljas trots invändningarna?
2. **Nämnaren (§3.4):** godkänns D:s icke-target-definition som B:s nämnare, med
   B-väggarna kvar i nämnaren (integrationstak 0,65) och **ingen** `b_breadth_exclude`-
   lista vid start?
3. **Rankingeffekten (§5/Bilaga A):** accepteras att ändringen byter KD↔MP i totalranking
   (ny marginal 0,014, dagens +0,040) — dvs. att detta uttryckligen är en betygsrelevant
   modelländring, inte bara en flagg-/ärlighetsändring? Notera: marginalen är långt inom
   osäkerhetsintervallen — väljaren ser CI-överlapp mellan KD och MP — men flippen ska
   ändå redovisas explicit, inte döljas bakom CI:t.
4. **`thin_coverage_threshold`:** behålls 0,5 på det nya måttet (rekommenderas), eller
   höjs till 0,6 så även 0,65-taket (integration C/KD) flaggas?
5. **Flaggformat:** ersätts `B_coverage_<num>/<den>` (antal) av viktflaggan i det LÅSTA
   formatet (§4: `round(covered_weight, 1)` skrivet `:g`, `total_weight` heltal `:g`),
   med antalsbilden kvar enbart i `coverage_report` (rekommenderas)? Eller ska båda
   flaggorna skrivas?
6. **B-breddgrind (§6.4):** ska `b_thin_breadth_accepted`-grinden byggas (spegel av D:s),
   med integration som första människosignerade post (rekommenderas)?
7. **Utrullning:** börja i `policy_type_count` för byte-identisk baseline, slå om +
   rebaselina efter diff-granskning (rekommenderas, samma mönster som D)? **Krav före
   default-switch:** diff-granskningen ska omfatta score-diff per cell, kategori och
   total SAMT en CI-överlapp-/rankingnot (KD↔MP-marginalen 0,014 vs osäkerhets-
   intervallen, Bilaga A) — båda människosignerade.

---

## 11. Granskningslogg

- 2026-06-12: v1-utkast skrivet (Claude) som systerspec till
  [d_coverage_krympning_spec.md](d_coverage_krympning_spec.md). §2 verifierat
  mot körd `coverage_report` (B4-tabellen i BACKLOG konstaterad delvis inaktuell:
  integration 3/5, valfard 4/4, forsvar 4/5, trygghet 5/5, demokrati 5/5); §3.2- och
  §5-siffrorna reproducerade read-only ur config + `dist/scores.json` (cov_pt/cov_bredd/
  cov_B per cell; totaldelta per parti; KD↔MP-bytet under (a); ensidig −0,04…−0,13 under
  (b)). Väntar Codex-granskning + mänsklig sign-off av §10.
- 2026-06-12: Codex-granskning **APPROVE-WITH-CHANGES** → v2 (Claude). P1: (1)
  neutralitetsformuleringen i §3.4/§5 var överdriven ("straffar alla partier lika") —
  omformulerad till symmetrisk-mot-2,5-men-inte-lika-delta, med verifierad total- och
  rankingbild öppet redovisad i ny **Bilaga A**; (2) anti-gaming-acceptanstester för
  `|K_s|/|T_s|` tillagda i §7 (dedup-set inom undermått, bidrag en gång per undermått,
  Fas 4c-grindar + krav på coverage-diff-granskning vid varje liggarändring). P2: (3)
  configvalidering (ogiltig `coverage_mode` hard-failar) + deterministiskt flaggformat
  låst i §4/§6.2/§7; (4) sign-off-kravet i §10 utökat: score-diff per cell/kategori/total
  + CI-överlapp-/rankingnot före default-switch. Orkestratorns skriptade omräkning mot
  committad `dist/scores.json` + config bekräftade Codex manuella aritmetik exakt
  (Bilaga A); KD↔MP-marginalen preciserad 0,015 → 0,014.
- 2026-06-12: IMPLEMENTERAD (Claude) enligt §9 steg 1–4 + 6 bakom
  `B_evidens.coverage_mode: policy_type_count` (legacy default). Levererat:
  `score.weighted_depth_coverage` (§6.1), delad nämnarhelper
  `scorerun._non_target_submeasures` (alias `_d_denominator_submeasures`, D-anrop
  oförändrade) + `_b_codable_types_by_submeasure` + `_b_coverage_flag` (låst format §4),
  mode-växel i huvudloopen med cov_B-gate (§3.6), configvalidering (ogiltigt läge
  hard-failar i `config.validate` OCH i `scorerun.build`), 18 tester i
  `tests/test_b_coverage_mode.py` (formel/B-vägg/multi-undermått/dedup/monotoni,
  delad nämnarfunktion-identitet, flaggformat 86.7/100 + 73/73, formelekvivalens per
  cell mot oberoende cov_B-omräkning, §3.6-kantfallet legacy-vs-ny, default=legacy
  byte-identisk). Verifierat: `pytest` 282 grönt, `dist/` byte-identisk i legacy-läget
  (git diff tom + score_diff ren). §9 steg 5 (`coverage_report.b_submeasure_breadth` +
  ev. B-breddgrind §6.4) och steg 7–8 (diff-redovisning + default-switch + rebaselina)
  väntar §10-sign-off. Lägesnot: §5/Bilaga A-siffrorna är från före B3-leveransen
  (1571031); i dagens config ger nya läget t.ex. S/integration cov 42,5/100 och
  KD/integration 52,5/100 (B3-posterna breddade täckningen), KD↔MP-flippen kvarstår
  (MP 3,148 > KD 3,119 i lokal testkörning) — effektbilden ska räknas om vid
  §10-granskningen.
- 2026-06-12: **§10.1–10.6 SIGNADE** (mänsklig sign-off): (1) ERSÄTT med enhetlig `cov_B`
  godkänd; (2) D:s icke-target-nämnare godkänd, ingen `b_breadth_exclude` vid start;
  (3) KD↔MP-flippen accepterad i princip (faktisk diff granskas i §10.7); (4)
  `thin_coverage_threshold` behålls 0,5 (verifierad i config); (5) viktflaggan ersätter
  antalsflaggan; (6) bygg B-breddgrinden. **§9 steg 5 LEVERERAT** (Claude) per §10.6:
  `coverage_report.b_submeasure_breadth` (viktat cov_B-TAK per kategori; delar
  `_non_target_submeasures` + T_s-reglerna via `_b_codable_types_by_submeasure` — ingen
  duplicerad definition) + rapportsektion i `main()` (spegel av D-sektionen); grind
  `tests/test_b_breadth_gate.py` (spegel av `test_d_breadth_gate`: no-unaccounted/
  shrinks/valid/partition-bounds) mot `coverage_allowlist.b_thin_breadth_accepted`,
  grindtröskel 0,75 (§6.4); `b_submeasure_spread`-docstring uppdaterad per §3.5.
  Första människosignerade posten: **integration 65/100** (B-väggarna boendesegregation +
  normer_tillit = loggade mandat-undantag H4/H3 med triggrar, beslutsunderlag_hold_
  2026-06-12); forsvar 95/100 och klimat 85/100 ligger ÖVER grindtröskeln (H6 gällde
  D-sidan; B-väggen genomforbarhet_leverans väger bara 5). Verifierat: pytest 292 grönt,
  `dist/` fortsatt byte-identisk i legacy-läget (git diff tom + score_diff ren).
  KVAR: endast §10.7 — default-switch + rebaselina efter människogranskad switch-diff
  (per cell/kategori/total + CI-överlapp-/rankingnot).
- 2026-06-14: **§10.7 SIGNAD — DEFAULT-SWITCH AKTIVERAD** (mänsklig sign-off på
  människogranskad switch-diff, GO). `config/scoring.yaml` `coverage_mode`
  `policy_type_count` → `weighted_submeasure_depth`. `python -m pipeline.scorerun` skrev om
  `dist/` och `score_diff --write` rebaselinade `scores.snapshot.json`. Den granskade
  switch-diffen (mot committad snapshot): **106 ändringar, allt B-drivet** (D/A/C orörda).
  Totaler/ranking: S 3,704→3,660; L 3,405→3,370; M 3,330→3,284; **MP 3,118→3,127**;
  **KD 3,162→3,119**; C 3,103→3,034; SD 2,735→2,720; V 2,576→2,600 — ranking
  S > L > M > **KD > MP** > C > SD > V → S > L > M > **MP > KD** > C > SD > V (KD↔MP-flippen
  verkställd; ny marginal 0,0085 inom det öppet redovisade 80 % CI-överlappet). Största
  kategori-Δ: C/integration −0,306, KD/integration −0,270, S/integration −0,167,
  S+C/klimat −0,175; lossningen demokrati V +0,134 / M+KD +0,080 (antalsviktning av
  korruption_tillit ersatt av modellvikt). 8 tunnhetsflaggor (mot 1 i legacy). Två tester
  i `test_b_coverage_mode.py` som pinnade default==legacy uppdaterade till default==weighted
  (legacy-garantierna kvar via explicit override). Verifierat: **pytest 292 grönt** (4
  skip), ruff rent, `score_diff` ren mot ny baslinje. Specen arkiverad till done/.

---

## Bilaga A. Neutralitets- och rankingbild (skriptat verifierad)

Verifierad 2026-06-12 av orkestratorn med skriptad omräkning mot committad
`dist/scores.json` + config (read-only); bekräftar Codex-granskningens manuella
aritmetik exakt.

**Totaler, dagens läge → med `cov_B` (ersätt-varianten (a), standardvikter):**

| Parti | Total idag | Med `cov_B` | Δ |
|---|---:|---:|---:|
| C | 3.077 | 3.015 | −0.062 |
| KD | 3.152 | 3.111 | −0.041 |
| L | 3.389 | 3.356 | −0.033 |
| M | 3.321 | 3.278 | −0.043 |
| MP | 3.112 | 3.126 | +0.013 |
| S | 3.683 | 3.637 | −0.045 |
| SD | 2.727 | 2.713 | −0.013 |
| V | 2.621 | 2.644 | +0.023 |

**Ranking:** S > L > M > KD > MP > C > SD > V → S > L > M > **MP > KD** > C > SD > V.
En platsväxling (KD↔MP); ny marginal 0,014 (MP 3,126 mot KD 3,111) att jämföra med
dagens +0,040 åt andra hållet. Marginalen är långt inom osäkerhetsintervallen —
väljaren ser CI-överlapp mellan KD och MP — men flippen ska ändå redovisas explicit
vid sign-off (§10 fråga 3 och 7).

**Neutralitetsläsning.** Krympningen är **symmetrisk mot 2,5 men inte lika-delta**:
partier med högt `|B_raw − 2,5|` i en berörd kategori förlorar mer i absoluta
betygspoäng än partier nära eller under neutral. I dagens täcknings- och viktläge ger
det: regeringspartierna M/KD/L −0,03…−0,04; C störst tapp (−0,062, drivet av
integrationens oavkortade 5,00 mot tak 0,65); S −0,045; MP/V små vinster
(+0,013/+0,023 — B_raw nära/under neutral i berörda kategorier plus
demokrati-lossningen, §5). Mönstret följer alltså dagens täcknings-/viktläge — det är
ingen partisk regel, och det vänder om evidensläget vänder — men det ska redovisas
öppet före sign-off, inte sammanfattas som att krympningen "straffar alla lika".
