# Fas 4b — kureringsmetod för partiståndpunkter (delpoäng B)

> Status: **version 2 — expertgranskad och aktiv**. Metoden lades fast i samråd (andra-åsikt via Codex,
> 2026-05-30); `party_positions.yaml` slutgranskades och signades (v1 2026-06-05, §8.8-sign-off → v2
> 2026-06-07) och B används nu för skarp betygsättning. Avsnitten nedan beskriver kureringsprincipen.

## 1. Vad B är och varför ståndpunkter behövs

Delpoäng B (väger 0,35 av varje kategoripoäng) mäter om ett partis **faktiskt drivna åtgärder** rör
kategorins indikatorer åt rätt håll *enligt officiell svensk evidens*. Maskineriet
([pipeline/positions.py](../pipeline/positions.py)) joinar:

```
config/party_positions.yaml   (parti -> åtgärdstyp, stance, KÄLLA)
        ⋈ on policy_type
config/evidence_ledger.yaml    (åtgärdstyp -> indikatoreffekt enligt officiell utvärdering)
        => evidence_effect-claims => indicator_effects => B
```

- `stance: supports` behåller evidensens riktning; `stance: opposes` vänder den (`_FLIP`).
- B kan **bara** byggas för de ~25 `policy_type` som finns i evidensliggaren. En rad med okänd
  `policy_type` ger noll claims (ofarlig no-op).
- Saknas rader för (parti, kategori) faller B tillbaka på **neutral 2,5 / låg säkerhet / flagga
  `B_no_party_evidence`** ([config/scoring.yaml](../config/scoring.yaml)).

## 2. Bärande integritetsprincip

Inga partiståndpunkter fabriceras. En `supports`/`opposes` får sättas **endast** om den kan beläggas
med en officiell svensk källa till partiets **faktiska** ställningstagande, med ordagrant citat och
dokument-id. Detta är skillnaden mellan att *läsa av* vad ett parti gjort (tillåtet) och att *gissa*
vad det "nog tycker" (förbjudet).

## 3. Källhierarki (rangordnad)

1. **Riksdagsdata (primär)** — voteringar, betänkanden/reservationer, budgetmotioner, kommittémotioner,
   propositioner. Officiellt, tidsstämplat, dokument-id-citerbart, konkret nog för smala åtgärdstyper.
   En **votering** är guldstandard: partiets röst står i protokollet, ingen tolkning behövs.
2. **Valmanifest (sekundär)** — partiets eget, tidsbundet och policykonkret, men ofta bredare än en
   enskild åtgärdstyp.
3. **Partiprogram (endast kontext)** — ideologiskt och högnivå; får **aldrig ensamt** sätta en stance.

Otillåtet för stance: media, intresseorganisationer, internationella index. (Myndighetsmaterial får
bara ge *kontext*, inte en partistance.)

## 4. Instrument-regeln (avgörande mot mål-vs-instrument-glidning)

> Sätt stance endast om källan stödjer/motsätter sig **samma instrument**, inte bara samma mål.

| Räcker INTE | Räcker |
|---|---|
| "Vi vill minska utsläppen" | "Vi vill höja koldioxidskatten" |
| "Vi vill stärka arbetslinjen" | "Vi bygger ut subventionerade anställningar/nystartsjobb" |
| "Sänkt skatt på drivmedel" (≈ energiskatt) | "Sänkt **koldioxidskatt**" / röst om reduktionspliktens nivå |

En oberoende granskare utan politisk tolkning ska kunna peka på text/votering som **direkt** avser
policyinstrumentet (eller en fördefinierad synonym till det). Annars: utelämna raden (→ `unknown`).

## 5. Attribuering vid regeringsbeslut (proposition/budget)

Regeringspartier "äger" propositioner/budget kollektivt. Regel (per Codex):

- Sätt stance per parti endast om partiet är **formell avsändare**, **röstat för/emot**, står bakom
  budget/proposition **genom regeringsunderlag**, eller har **egen motion/reservation**.
- För regeringspartier (t.ex. M/KD/L): regeringsproposition/budget räcker som kollektiv stance **när
  instrumentet är explicit** i beslutet.
- För stödparti (t.ex. SD): attribuera via **explicit votering/utskottsställning/överenskommelse/motion**
  — **inte** automatiskt som "regeringsparti". `mapping_note` ska säga exakt varför (t.ex. "röstade Ja
  till budgetbeslutet som sänkte reduktionsplikten").

## 6. Saknad ståndpunkt = unknown, inte mitten

Om ett parti saknar citerbar stance på en åtgärdstyp → **ingen rad** → ingen claim. Det betyder
*"vi vet inte"*, inte *"partiet ligger i mitten"*.

**Coverage-viktning (byggd i `scorerun`):** för att frånvaro inte ska misstas för en uppmätt position
krymps B mot neutral efter täckning:

```
coverage = kodade åtgärdstyper / kategorins kodbara åtgärdstyper (signed_direction ≠ 0, ej exkluderade)
B = 2.5 + (B_raw − 2.5) × coverage
```

Tunn täckning drar alltså B mot neutral (varken belönar eller straffar luckor), och ett ensamt
`supports`-claim ger inte längre maxbetyg. `coverage` redovisas i `scores.json` som flaggan
`B_coverage_{num}/{den}`; `coverage < thin_coverage_threshold` (0,5) ger låg säkerhet + `B_thin_coverage`.
Detta var nödvändigt: utan viktning mättade B vid 5,0 för nästan alla, eftersom liggarens åtgärdstyper
mestadels är brett stödda (se §10).

## 7. Rad-schema i `party_positions.yaml`

Pipeline joinar bara på `party` + `policy_type` + `stance`; övriga fält är **spårbarhet** (ignoreras av
maskineriet men krävs för granskning):

| Fält | Krav |
|---|---|
| `party` | partikod S/M/SD/C/V/KD/L/MP |
| `policy_type` | måste finnas i `evidence_ledger.yaml` |
| `stance` | `supports` \| `opposes` |
| `source` | officiell källa (kort beteckning) |
| `source_type` | votering \| betankande \| reservation \| budgetmotion \| kommittemotion \| proposition \| valmanifest |
| `source_url` | data.riksdagen.se / regeringen.se-URL |
| `doc_id` | riksdagens dok-id (t.ex. HB01MJU5) eller votering_id |
| `quote` | ordagrant utdrag som belägger stance |
| `date` | datum/riksmöte |
| `mapping_note` | varför detta avser *instrumentet* (ej bara målet) |

## 8. Verifieringsprotokoll (två-kodare / adversariellt)

Varje rad granskas av en **oberoende** part som hämtar den citerade källan och prövar STRÄNGT:

1. **quote_found** — finns citatet ordagrant/nära i dokumentet?
2. **instrument_precise** — avser det rätt instrument (ej närliggande mål)?
3. **confirmed** — stödjer källan den påstådda riktningen (supports/opposes)?

`confirmed=true` endast om alla tre. Vid tvivel → `false` och raden utelämnas; oenighet loggas. Default
är skepsis. (I piloten görs detta av en separat verifieringsagent per rad; voteringsförankrade rader
återhämtas och kontrolleras mot protokollet.)

## 9. Kända bias-risker och mitigering

| Risk | Mitigering |
|---|---|
| **Aktivitetsbias** (partier som motionerar mer får fler claims) | coverage redovisas; B normeras inte mot antal rader |
| **Regerings-/oppositionsasymmetri** (prop vs motion) | tillåt båda källtyper, märk `source_type` |
| **Tidsbias** (gammal ståndpunkt lever kvar) | `date`/riksmöte krävs; föredra senaste mandatperioden |
| **Instrumentförväxling** | instrument-regeln §4 + verifiering §8 |
| **Negativ evidens är politiskt känslig** | systemet *ska* våga ge negativt B-bidrag när ett parti driver en åtgärd som enligt liggaren har fel riktning |
| **Coverage-bias** (få rader ser skenbart säkra ut) | coverage-markör + låg säkerhet/`B_no_party_evidence` |

## 10. Utrullning 2026-05-30 — alla 7 kategorier

**Klimat** (handkurerad pilot): `reduktionsplikt_drivmedel` förankrad i **votering bet. 2023/24:MJU5**
(prop. 2023/24:28), punkt 1 — röst Nej till sänkningen = `supports` (S, C, V, MP), Ja = `opposes`
(M, SD, KD, L); `koldioxidskatt` via instrument-exakta motioner (6/8, S/C unknown).

**Övriga 6 kategorier** togs fram av en research+verifierings-workflow (en agent per (åtgärdstyp, parti)
sökte data.riksdagen.se; en oberoende granskare hämtade källans fulltext `.text` och bekräftade citat
+ riktning deterministiskt). **Endast `confirmed=true` togs med** — verifieringen fångade och förkastade
fabricerade/oprecisa citat. Resultat: **111 rader** totalt (99 supports / 12 opposes). *(Detta var den
initiala utrullningen; ståndpunkterna panel-harmoniserades och utökades senare (B2/B3 t.o.m. 2026-06-14) till **269 rader** — se §11.)*

**Inerta åtgärdstyper kodades inte** (mixed/unclear-riktning → `signed_direction = 0` → ingen B-effekt):
`kamerabevakning`, `jobbskatteavdrag`, `riktat_likvardighetsbidrag`. **Exkluderad:**
`internationella_materielsamarbeten` (negativ riktning → ett parti som stödjer samarbete skulle få sämre
försvars-B, missvisande). Beslut bekräftade med andra-åsikt (Codex).

**Viktig observation:** utanför ekonomi (jobb) och klimat (reduktionsplikt) är de flesta åtgärdstyper
**nära-konsensus** (alla partier stödjer kompetensutveckling lärare, värnplikt, civilt försvar,
behandlingsprogram …). De 12 opposes (de särskiljande signalerna) ligger i ekonomi (5: SD/C mot
subv. anställningar + C/KD/L mot arbetsmarknadsutbildning), klimat (5), välfärd (1: SD mot minskad
klasstorlek) och integration (1: V mot aktiveringskrav). Detta + coverage-viktningen (§6) gör att B
särskiljer måttligt; **evidensliggaren kan behöva fler omstridda åtgärdstyper** för att B ska bli en
starkare differentiator. Flaggat för granskning.

Status: `party_positions.yaml` **version 2, expertgranskad** (källkontroll + bias slutförda; sign-off
2026-06-05 v1, §8.8 2026-06-07 v2). Skarp betygsättning aktiverad.

## 11. Fas 4c — harmonisering + differentiering (2026-05-30)

Efter utrullningen identifierades två svagheter (se [ROADMAP Fas 4c](done/ROADMAP.md)): (1) isolerings-inducerade
verifierar-asymmetrier (samma slags källa bedömdes olika strängt för olika partier, t.ex. M/L på
`subventionerade_anstallningar`), och (2) svag särskiljning. Åtgärder, under den frysta rubriken
[fas4c_rubrik.md](fas4c_rubrik.md):

- **Plan B — panel-harmonisering:** varje åtgärdstyp re-verifierades med alla 8 partier bedömda SIDA VID SIDA
  under en gemensam standard (bunten-regeln: en buntad motion räknas för det namngivna instrumentet, intern
  nyans förkastar ej raden). 109 non-klimat-rader admitterades (panel keep/add ∧ verifierad confirmed).
  Audit + rejected-log: [fas4c_planB_audit.md](done/fas4c_planB_audit.md). `status: harmonized_alla_kategorier_unreviewed`.
- **Plan A — omstridda åtgärdstyper:** 8 instrument systematiskt evidens-skannades; **bara `ny_karnkraft`
  → effektbrist** (Svenska kraftnät, Kraftbalansen 2025) passerade evidens-/negativ-grinden. 7 lämnades
  **inerta** (blandad officiell evidens — a-kassa, vårdval/LOV, bonus-malus, bidragstak m.fl.), inkl. den
  enda negativa kandidaten (a-kassa) som korrekt stoppades av negativ-grinden. [kandidatregister + A3/A5](done/fas4c_planA_kandidatregister.md).
- **Negativ-riktnings-grind (§5 i rubriken):** ett negativt B-bidrag kräver authority_evaluation/systematic_review
  + confidence ≥ medium + exakt indikator. Modellen har **0 admitterade negativ-riktnings-poster** som bidrar
  till B; negativa bidrag uppstår bara när `opposes` vänder en *positiv* evidenspost.

**Centralt fynd:** de flesta värde-omstridda instrument saknar robust riktad officiell evidens på exakt
kategori-indikatorn — då tiger B (rubrik §6). B mäter *evidens-kodbar instrumentell träffsäkerhet*, inte all
viktig politik. Totalt 269 ståndpunkter (version 2, expertgranskad — sign-off 2026-06-05 v1, §8.8 2026-06-07 v2).
