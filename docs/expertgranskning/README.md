# Expertgranskningspaket — version-0-config

Rösta-pipelinen är komplett (Fas 0–6 + b-faser), men tre configfiler är **AI-utkast (version 0)**
som projektets disciplin flaggar som *"kräver mänsklig slutgranskning innan skarp betygsättning"*.
Eftersom hela appens värde är **objektivitet**, är granskningen av dessa filer den faktiska grinden
mellan fungerande prototyp och trovärdig produkt. Det här paketet gör granskningen spårbar och
fokuserar den på de rader som faktiskt rör betygen.

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

> **Status (2026-06-03):** Datatäckningen och driftrobustheten har byggts ut sedan paketet skapades
> (nya D-serier: trygghet uppklaringsgrad + skjutningar/sprängningar; serie-drift-skydd, snapshot-diff
> och live-smoke-test — se [BACKLOG.md](../BACKLOG.md)). **De tre version-0-configfilerna nedan är
> oförändrade** av det arbetet och är fortfarande den faktiska granskningsgrinden. Paketet är
> regenererat mot aktuell config (inga ändringar i de granskade raderna).

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
   **fyra rader är SUSPECT** och väntar på ditt beslut (S kärnkraft, V välfärdsbrott, C tidiga insatser,
   M kärnkraft-källtyp).
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

## Sign-off-protokoll

När en fil är granskad och eventuella rättelser införda:

1. Inför rättelser **i `config/*.yaml`** (inte i granskningsdoken — de regenereras).
2. Höj filens `version: 0 → 1` och uppdatera `status:`
   (`party_positions.yaml`: `harmonized_alla_kategorier_unreviewed → expert_reviewed`;
   `evidence_ledger.yaml`: `seed_requires_curation → expert_reviewed`).
3. Kör `python -m pipeline.build_all` och granska att rankingen i `dist/scores.json` rör sig som
   väntat; uppdatera `meta.coverage`-strängen (ta bort "version 0 – kräver mänsklig slutgranskning").
4. Kör `python -m pytest` (ska vara grönt) och `python -m pipeline.tools.review_packet` (regenererar
   paketet mot den granskade configen).
5. Notera granskningsbeslutet i [BACKLOG.md](../BACKLOG.md) under **Spår B (B1)** — ROADMAP.md är
   fryst historik och uppdateras inte längre.

> **Princip:** detta paket *ändrar ingen config* — det är beslutsunderlag. De fyra SUSPECT-fynden
> i adversariell_verifiering.md är medvetet INTE rättade i koden; det är expertens beslut om de ska
> omkodas, kvalificeras eller tas bort.
