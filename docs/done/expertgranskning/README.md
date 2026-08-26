# Expertgranskningspaket — B/A-config (granskning genomförd)

> **✅ Status 2026-06-14: granskningen är GENOMFÖRD och alla tre configfiler är signerade.**
> `budget_ramar.yaml` → version 1 (budgetåren 2023-2025 sign-off 2026-06-05; de tolv år ADR 0007
> lade till, 2011-2022, sign-off 2026-08-26, se
> [A_budgetramar_verifiering_2011_2022.md](A_budgetramar_verifiering_2011_2022.md));
> `party_positions.yaml` + `evidence_ledger.yaml`
> → version 2 / `expert_reviewed` (v1 2026-06-05, §8.8-sign-off 2026-06-07 → v2). Skarp betygsättning
> är aktiverad. Paketet bevaras som **granskningshistorik och beslutsunderlag**; siffrorna nedan är
> ögonblicksvärden från när paketet skapades (2026-06-03/06) och speglar inte senare B2-/B3-tillägg
> (aktuellt: **269 ståndpunkter / 46 evidensposter**).

När paketet skapades var Rösta-pipelinen komplett (Fas 0–6 + b-faser) men tre configfiler var
**AI-utkast (version 0)** som projektets disciplin flaggade som *"kräver mänsklig slutgranskning innan
skarp betygsättning"*. Eftersom hela appens värde är **objektivitet** var granskningen av dessa filer
den faktiska grinden mellan fungerande prototyp och trovärdig produkt. Det här paketet gjorde
granskningen spårbar och fokuserade den på de rader som faktiskt rör betygen.

| Fil | Driver delpoäng | Vikt | Granskningsdok |
|-----|-----------------|------|----------------|
| `config/party_positions.yaml` (130 ståndpunkter) | **B** | 35 % | [B_partistandpunkter.md](B_partistandpunkter.md) |
| `config/evidence_ledger.yaml` (30 poster) | **B** | 35 % | [B_evidensliggare.md](B_evidensliggare.md) |
| `config/budget_ramar.yaml` (a1) | **A** | 40 % (a1 = 0,6·A) | [A_budgetramar.md](A_budgetramar.md) |

Allt under `docs/expertgranskning/` (utom denna README + [adversariell_verifiering.md](adversariell_verifiering.md))
är **autogenererat** av `pipeline/tools/review_packet.py`. Regenerera efter varje configändring:

```bash
python -m pipeline.tools.review_packet
```

> **Historisk statusnotis (2026-06-03, vid paketets skapande):** Datatäckningen och driftrobustheten
> hade byggts ut sedan paketet skapades (nya D-serier: trygghet uppklaringsgrad + skjutningar/sprängningar;
> serie-drift-skydd, snapshot-diff och live-smoke-test — se [BACKLOG.md](../../BACKLOG.md)). De tre
> configfilerna var då oförändrade v0 och utgjorde granskningsgrinden. **Den grinden är sedan passerad**
> (se status-bannern överst — sign-off 2026-06-05/06-07).

## Vad granskningen redan vet (deterministiskt härlett)

- **Alla 130 ståndpunkter är "aktiva"** — var och en har en `policy_type` som finns i
  evidensliggaren, så alla rör B (inga inerta rader att avfärda). De ger 157 evidence_effect-claims.
- Pipelinen joinar **bara** på `party + policy_type + stance`. `supports` behåller evidensens
  riktning; **`opposes` vänder den** (störst skaderisk). Övriga fält är spårbarhet.
- Stance-fördelning: 113 supports / 17 opposes. Konfidens: 71 high / 28 medium / 17 low / 14 utan
  fält (klimat-raderna ur votering bet. 2023/24:MJU5).

## Granskningsordning (rekommenderad)

1. **[adversariell_verifiering.md](adversariell_verifiering.md)** — börja här. En oberoende skeptisk
   omverifiering av högrisk-delmängden (propositionsavslags-opposes + `ny_karnkraft`) mot riksdagens
   fulltext är redan gjord. De evidens-*vändande* opposes som spelar störst roll är **bekräftade**;
   fyra rader var SUSPECT (S kärnkraft, V välfärdsbrott, C tidiga insatser, M kärnkraft-källtyp) —
   **alla avgjorda i sign-offen 2026-06-05** (V `kontroller_mot_valfardsbrott` → supports/förbehåll,
   C `tidiga_insatser` → supports/omattribuerad, S/M m.fl. `ny_karnkraft` behållna med dokumenterad
   källtyps-asymmetri; se beslutsloggen i [done/evidens_trovardighet.md §9](../evidens_trovardighet.md) + BACKLOG B1).
2. **[B_partistandpunkter.md](B_partistandpunkter.md) → "⚑ Prioriterad granskning"** — 79 rader där
   fel gör störst skada (opposes, prop_avslag, ny_karnkraft, low_confidence, single_member, äldre
   källa). Sätt verdikt (✅/✏️/❌) i OK?-kolumnen.
3. **Panelvyn** i samma fil — granska varje åtgärdstyp som en panel (alla partier sida vid sida) så
   asymmetrier syns. Kärnkontroll: är `stance` rätt på det **namngivna instrumentet**?
4. **[B_evidensliggare.md](B_evidensliggare.md)** — 30 poster. Varje post sätter riktningen för ALLA
   partier som driver åtgärdstypen (blast-radius anges), så källkvaliteten väger tungt. Var extra
   skeptisk mot `expert_opinion`-nivå och `unclear/mixed/negative`-riktningar.
5. **[A_budgetramar.md](A_budgetramar.md)** — jämför de transkriberade UO-beloppen cell för cell mot
   bet. 2024/25:FiU1 tabell 35 (källrad anges per frame). Feltranskribering korrumperar A.

## Sign-off-protokoll (genomfört 2026-06-05 → §8.8 2026-06-07)

Detta protokoll FÖLJDES vid sign-offen och bevaras som referens. När en fil var granskad och eventuella rättelser införda:

1. Inför rättelser **i `config/*.yaml`** (inte i granskningsdoken — de regenereras).
2. Höj filens `version: 0 → 1` och uppdatera `status:`
   (`party_positions.yaml`: `harmonized_alla_kategorier_unreviewed → expert_reviewed`;
   `evidence_ledger.yaml`: `seed_requires_curation → expert_reviewed`).
3. Kör `python -m pipeline.build_all` och granska att rankingen i `dist/scores.json` rör sig som
   väntat; uppdatera `meta.coverage`-strängen (ta bort "version 0 – kräver mänsklig slutgranskning").
4. Kör `python -m pytest` (ska vara grönt) och `python -m pipeline.tools.review_packet` (regenererar
   paketet mot den granskade configen).
5. Notera granskningsbeslutet i [BACKLOG.md](../../BACKLOG.md) under **Spår B (B1)** — ROADMAP.md är
   fryst historik och uppdateras inte längre.

> **Princip:** detta paket *ändrade ingen config* — det var beslutsunderlag. De fyra SUSPECT-fynden
> i adversariell_verifiering.md lämnades medvetet orättade i koden tills expertbeslutet; **de avgjordes
> sedan i sign-offen 2026-06-05** (se ovan + beslutsloggen).
