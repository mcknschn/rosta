# Rösta — Backlog (framåtblickande arbete)

> Levande planeringsdokument för arbetet **efter** faser 0–6. Organiserat efter
> **arbetsspår** (inte faser) eftersom fasmodellen är levererad. Bärande princip
> oförändrad: inget partibetyg eller mänskligt omdöme i kod — bara i versionsstyrd
> config; all data spårbar till en officiell svensk källa (CLAUDE.md).

**Status-legend:** 🔵 nästa · ⚪ planerad · 🟣 designfråga (ej byggbar än) · ✅ klar (flyttas till ROADMAP).
**Effort:** `S` = återanvänder befintligt mönster · `M` = ny adapter · `L` = kräver research/design.

---

## Hur filerna hänger ihop

| Fil | Roll |
|-----|------|
| [ROADMAP.md](done/ROADMAP.md) | **Fryst historik** (arkiverad i `done/`) — hur faser 0–6 + b-faser byggdes och verifierades. Ändras inte. |
| [leveranslogg.md](done/leveranslogg.md) | **Fryst leveranshistorik** (arkiverad i `done/`) — daterad logg över vad som byggts/verifierats 2026-06-03…06-12 + gammal status-ögonblicksbild, utbruten ur denna fil 2026-06-14. |
| [../config/coverage_allowlist.yaml](../config/coverage_allowlist.yaml) | **Maskinläsbar sanningskälla** för vilka D-indikatorer som ännu saknas, med skäl-tag. Coverage-gaten (`tests/test_fas3_gate.py`) tvingar varje indikator att vara *inläst* ELLER *allowlistad*. |
| **BACKLOG.md** (denna) | **Prioritering & plan** — vågordning per arbetsspår. Duplicerar inte allowlisten; pekar på den. När en indikator byggs: flytta ut den ur allowlisten och bocka av här. |
| [evidens_trovardighet.md](done/evidens_trovardighet.md) | **B-spårets arbetslogg & metodutveckling** — bärande: **tvåstegsmodellen** (måttet ≠ positioneringen). Skiljer äkta steg-1-väggar (måttet saknas) från steg-2-källval (acklamation slår bara ut voteringskällan). Metodregister för positionering (källstege, enhällighet, budget-/kommittémotion, bana över tid), statustavla + kandidat-pipeline per kategori, öppna designfrågor, beslutslogg. Uppdateras per B-leverans. **§4.3 = kanonisk begreppsmodell (Kategori→Undermått→Indikator→Riktning) + mätbarhetskarta för samtliga 52 indikatorer.** |

---

## Varför den här prioriteringen

Rankingen drevs vid backloggens start mest av **A (aktivitet) + C (makt)**, eftersom **B krymps
mot neutralt** vid tunn täckning och D då var "ej tillämplig" i 21 av 56 celler. *(Uppdaterat
2026-06-12: D matas nu i **alla 7 kategorier** — 43/68 indikatorer, 29/35 undermått — och krymps
sedan 2026-06-12 efter **viktad undermåttsbredd** i stället för att renormalisera bort saknad
bredd, se [done/d_coverage_krympning_spec.md](done/d_coverage_krympning_spec.md). B är utrullad
med ≥2 undermått per kategori. Obalansen är alltså i stort åtgärdad; kvarvarande tyngdpunkt är
trovärdighets-/breddarbete, inte strukturella nollor.)*

**Mål med backloggen:** flytta tyngdpunkten mot **B (evidens/träffsäkerhet)** och
**D (resultat)** så att betygen speglar utfall, inte bara emfas. Vald strategi: **balans** —
billig D-bredd (återanvänder API-mönster) *parallellt* med att höja B:s trovärdighet
(expertgranskning + bredare evidensliggare). De två hänger ihop: bredare evidensliggare →
högre coverage → mindre B-krympning → B får faktiskt genomslag.

> **📄 Leveranshistorik utbruten 2026-06-14:** vad som byggts och verifierats 2026-06-03 … 06-12
> (de gamla "Levererat"-loggarna + "Status per spår"-ögonblicksbilden) finns nu i
> [done/leveranslogg.md](done/leveranslogg.md). Den här filen är därför ren framåtblickande arbetskö.

---

## Spår D — Datatäckning (utfall, delpoäng D)

> **📍 Aktiv tracker:** [spar_D_datatackning.md](done/spar_D_datatackning.md) — utbruten arbets-/
> trackinglogg för Spår D (verifierat nuläge, byggbarhetsverdikt per indikator, öppna beslut,
> exit-kriterier). Vågtabellerna nedan behålls som översikt; trackern är sanningskällan för status.
>
> **Aktuell D-täckning** genereras alltid live med `python -m pipeline.tools.coverage_report`; luckor
> med skäl i `config/coverage_allowlist.yaml` (maskinläsbar sanningskälla, grindad av
> `tests/test_fas3_gate.py`). Den gamla narrativa matrisen är fryst i [done/fas3_coverage.md](done/fas3_coverage.md).

> **Status 2026-06-14: aktivt D-byggande är uttömt.** Våg 1–3 levererade (43/68 indikatorer, alla
> 7 kategorier). Kvarvarande luckor i `coverage_allowlist.yaml` är antingen permanenta (target,
> international, design_closed, low_value) eller hårda väggar (qualitative/sekretess, no_api) eller
> BEVAKA-bevakningar — inget direkt byggbart D-item återstår (jfr djupsvepet: blockeraren för D är
> neutralitet/attribution, inte datatillgång). Återupptas bara om en BEVAKA-trigger faller ut eller
> via C3 (subnationell D-data, eget spår nedan).

Mål: fler kanoniska årsserier som matar D-attributionen, så fler kategorier/undermått mäts på
faktiskt utfall. Alla nya serier ska vara kanoniska (finnas i `categories.yaml` med rätt
riktning) och annuella, så de matar `category_d` automatiskt.

### Våg 1 — billig bredd (återanvänder befintliga mönster) ✅ AVSLUTAD 2026-06-09

| Indikator | Kategori → undermått | Utfall |
|-----------|--------------------|--------|
| ~~`uppklaringsgrad`~~ ✅ | trygghet → rättsväsendets effektivitet | inläst 2026-06-03 (Brå 10La) |
| ~~`handlaggningstid`~~ ✅ | trygghet → rättsväsendets effektivitet | inläst 2026-06-12 (Domstolsverket DOMstat 01_Verksamhetsmal_TR, PxWeb v1 — 2026-06-03-väggen gällde Brå/ÅM, domstolsledet var förbisett) |
| ~~`aterfall_i_brott`~~ ✅ | trygghet → återfall/kriminalvård | inläst 2026-06-09 (Kriminalvården KOS Tabell 6.1, transkriberade råtal) |
| ~~`skjutningar_sprangningar`~~ ✅ | trygghet → grov brottslighet | inläst 2026-06-03 (Polisen, transkriberad) |
| ~~`overlevnad_svar_sjukdom`~~ ✅ | välfärd → vård tillgänglighet | inläst 2026-06-08 (Kolada U70471, 30-dagarsöverlevnad) |
| `vard_i_tid` ⛔ | välfärd → vård tillgänglighet | stängd som `low_value` (Kolada U79142 avslutad 2023 + dubblerar vardkoer) |

Trygghet gick därmed till 4/5 D-täckta undermått (förebyggande saknar indikator); välfärd 3/4.
Detaljer + verifiering i [spar_D_datatackning.md](done/spar_D_datatackning.md).

### Våg 2 — nya adaptrar (källa finns men ej rent öppet API) ✅ AVSLUTAD 2026-06-12

| Indikator | Kategori → undermått | Källa & metod | Effort | Tag |
|-----------|--------------------|---------------|--------|-----|
| ~~`realloner`~~ ✅ | ekonomi → reallöner/hushåll | Medlingsinstitutets **egen PxWeb** (Realloner_arsdata, Reallön (KPI) Index 1995=100, 1960–2025) — SCB-API-väggen gällde fel instans | M | ✅ **inläst 2026-06-12 (Spår D kväll, v0); KPI-valet dokumenterat** |
| ~~`sfi_sprakkunskaper`~~ ✅ | integration → skola/språk | SCB **TAB1814** `AA0003EB` (andel godkända i sfi %) — ej Skolverket-portal, SCB-PxWeb räckte | **S** | ✅ **inläst 2026-06-07 (Tier 2, v0); §5.2 avgjord (godkäntandel)** |
| ~~*(Svk-källadapter)*~~ ✅ | ~~klimat (förkrav för Våg 3-resten, effektbrist)~~ | ✅ **FÖRKRAVET STÄNGT 2026-06-12 (Spår D kväll):** effektbrist byggdes via Svk:s KRAFTBALANSRAPPORT (transkriberad config + tunn reader `svk.py`), ej tim-/effektdata — ingen Mimer/eSett-adapter behövdes, källregel-gränsfallet (§5.4-resten) upplöst utan att öppnas | — | ✅ stängt |

### Våg 3 — härledda + design­krävande ✅ AVSLUTAD 2026-06-12 (utom 1 design-stängd)

| Indikator | Kategori → undermått | Metod | Effort | Tag |
|-----------|--------------------|-------|--------|-----|
| ~~`elprisvolatilitet`~~ ✅ | klimat → energi/elpriser | **Energimyndigheten Energiindikatorer 12.5 EN_IND12-5A** (spotpris månadsmedel SE1–SE4 → årlig CV i adaptern) — Svk-/Nord Pool-väggen var överspelad, §5.4 upplöst | S (utökad bef. adapter) | ✅ **inläst 2026-06-12 (Spår D kväll, v0); CV-valet (ddof=0, likaviktning) dokumenterat** |
| ~~`effektbrist`~~ ✅ | klimat → energi/elpriser | **Svk "Kraftbalansen på den svenska elmarknaden"** (lagstadgad regeringsrapport): nettoimport vid vinterns topplasttimme, vinterår → slutår, 7 obs 2020–2026, transkriberad config (maskinverifierad PyMuPDF) — "härled ur effektdata"-antagandet var överspelat, rapporten publicerar årsvärdet färdigt | ~~S (efter Svk-adapter)~~ → L (transkr.) | ✅ **inläst 2026-06-12 (Spår D kväll, v0); måttval (lastfrånkoppling aldrig inträffad → nettoimport-bäraren, down direkt) + väder-caveat dokumenterade** |
| ~~`utslappsminskning_per_krona`~~ ⛔ | klimat → kostnadseffektivitet | **STÄNGD som designbeslut 2026-06-12 (D1):** kvoten premierar skattetung instrumentmix = ideologisk metodpreferens (CLAUDE.md-brott); kostnadseffektivitet är ändå D-täckt via `utslappsintensitet`. Allowlist-skäl `design_closed` | — | design_closed |
| ~~`personal_varnpliktiga`~~ ✅ | försvar → militär förmåga | **Försvarsmaktens ÅR** (antal påbörjade GU/år 2018–2025), korsverif. mot Pliktverkets inskrivna — transkribering m. källrad (PDF:er ej maskinläsbara) | L | ✅ **inläst 2026-06-07 (Tier 4, v0); FÖRSVARETS FÖRSTA D** |
| ~~`fortroende_domstolar_myndigheter`~~ ✅ / `tillit_valdeltagande` | demokrati | **Brå NTU 5A:1** (förtroende rättsväsendet, officiell — ej SOM) / SOM (tillit_valdeltagande, 🔴 BEVAKA/B-only) | L→**S** | ✅ **fortroende inläst 2026-06-07 (Tier 4, v0); DEMOKRATINS FÖRSTA D** |

### Medvetet **inte** för D (stäng som designbeslut)

- **`target`-indikatorer** (`inflation`, `statsskuld_underskott`, `forsvarsanslag_andel_bnp`):
  har ingen up/down-riktning (nära mål ≠ "uppåt bra") → ej D-dugliga. Behålls för B/visning.
- **`international`** (`korruption`/TI CPI, `mediefrihet`/RSF): förbjudna enligt CLAUDE.md
  (ej officiell svensk källa). Demokrati måste lösas via svenska akademiska källor (SOM) eller
  redovisas som låg täckning med hög osäkerhet — bygg **aldrig** internationella index för D.
- **`qualitative`/sekretess** (försvars materiel/operativ förmåga, civil beredskap, Ukraina-stöd,
  Nato-interoperabilitet): ingen öppen mätserie → acceptera gap, redovisa via osäkerhet.

---

## Spår B — Evidens & trovärdighet (delpoäng B)

Störst hävstång på trovärdighet. B väger 35 % och vilar på **46 evidensposter + 269 ståndpunkter,
expertgranskade (`version 2`; sign-off 2026-06-05 v1 → §8.8-sign-off 2026-06-07 v2); B2 samma dag: FoU-avdrag, undermåttet
företagande/investeringar samt hushållens disponibla inkomst → ekonomi 4/6 täckta undermått. 2026-06-06: nato
(försvar) + snabbförfarande (trygghet 4/5) + invasiva arter (klimat 4/5, avflaggad v1) via enhällighet-som-källa**.

- **B1 — Expertgranska version-0-config** ✅ *(mänsklig sign-off 2026-06-05 — `version 0 → 1`)* —
  gransknings­paketet i [expertgranskning/](done/expertgranskning/) genomgånget; `party_positions.yaml` +
  `evidence_ledger.yaml` är nu `version: 2` (denna B1-sign-off gav v1; §8.8-sign-offen 2026-06-07 → v2),
  `budget_ramar.yaml` `version: 1`; alla `status: expert_reviewed`, coverage-
  strängen uppdaterad (version-0-varningen borttagen), `dist/` ombyggt, snapshot re-baselinad, testsviten
  grön. **Skarp betygsättning aktiverad.** Granskningsbesluten (vad som ändrades och varför) nedan:
  - **Granskningssession 2026-06-05 (beslut införda i config, version kvar 0):**
    - *party_positions — 4 SUSPECT-fynd avgjorda:* V `kontroller_..._mot_valfardsbrott` opposes→**supports/förbehåll**
      (ankrad till yrkande 2: stöd för åtgärder mot välfärdsbrott med rättssäkerhetsförbehåll); C `tidiga_insatser`
      opposes→**supports** (omattribuerad — H5023910 är en L-ledd allians­motion mot *tillbakadragna* prop 2017/18:18;
      kodas nu som M/KD via H5024117 mot antagna 195); S `ny_karnkraft` **behållen supports** (noten dokumenterar
      villkoret); M/SD/KD/L `ny_karnkraft` **behållna + källtyps-asymmetri dokumenterad** i liggaren.
    - *evidence_ledger — alla 30 poster triade (blast-radius-mätt), 6 åtgärder införda:* koldioxidskatt→territoriella_utslapp-
      **dubblett borttagen** (löste bekräftad double-count), **redundant** subventionerade→arbetslöshet borttagen (D4;
      undviker dubbelvikt av jobbeffekten i samma undermått), `tidiga_insatser`/`behandlingsprogram_kriminalvard`/
      `sfi_kombinerat_med_praktik` **uppgraderade** från generiska seed-källor till URL-verifierade officiella källor
      (Skolforskningsinst. 2019 / Kriminalvården / IFAU Dahlberg m.fl. 2020), `reduktionsplikt_drivmedel` effect_strength
      **HIGH→medium** (vilade på en-års-attribution i pressmeddelande). 5 inerta poster identifierade (unclear/mixed/
      0 ståndpunkter → ingen B-effekt). De 3 demokrati-posterna (expert_opinion) **behållna** (bästa tillgängliga). Liggaren nu **28 poster**.
    - *party_positions — 79-raders panelscreening klar 2026-06-05:* **inga fabrikat**. De 11 kvarvarande
      `opposes` granskade — 7 sunda (4 voteringsbelagda reduktionsplikt + SD subventionerade + SD minskad_klasstorlek
      [äldre 2015/16] + redan klara), 5 av typen "motsätter sig *expansion/höjning*" (C/KD/L arbetsmarknadsutbildning,
      C subventionerade, SD koldioxidskatt) **behållna som opposes** per expertbeslut: riktningsregeln hålls objektiv
      (observerbar handling, ingen avsiktstolkning); magnituden adresseras via täckning (B2/B4), inte omkodning.
      12 enskild-motion-rader + 17 lågkonfidens-supports identifierade (riktningsbevarande, svag provenans, koncentrerade
      till demokrati — se B4).
    - *✅ Sign-off + version-bump 0→1 genomförd 2026-06-05.* Screeningdjup (det sign-offen vilar på): högrisk-
      klasserna (alla opposes, enskild-motion, lågkonfidens) är genomgångna; övriga supports-rader är riktnings-
      bevarande och instrument-exakta enligt sina mapping_notes men har inte var för sig återhämtats mot källa.
      *Kvarstående B-arbete flyttat till B2/B4 (täckning) — ej en blockerare för v1.*
- **B2 — Bredda evidensliggaren (anti-binär)** ✅ **i allt väsentligt LEVERERAD** *(status 2026-06-14)* —
  målet (ingen kategoris B vilar på för få undermått) är uppnått. Live `b_submeasure_breadth`: ekonomi
  73/73, valfard/trygghet/demokrati **100/100**, forsvar 95/100, klimat 85/100 — **inga nära-binära
  kategorier**. Ekonomi (1/5→4/6) och demokrati (1/5→5/5), de två "värsta" 2026-06-05, är nu fullt täckta.
  **Enda kvarvarande sub-tröskel: integration 65/100** (B-väggarna boendesegregation + normer_tillit) —
  ett **signat, accepterat undantag** (H3/H4, `b_thin_breadth_accepted`) med trigger ~2027 (bosättningslag),
  inte aktivt byggarbete. Per-kategori-detaljer i B4-tabellen nedan.
- **B3 — Fler omstridda/differentierande åtgärdstyper** ✅ **aktuell omgång LEVERERAD** *(2026-06-14)* —
  återanvänd Plan A-mönstret (Fas 4c): kandidatregister → endast intersektionen *omstridd ∧ evidensbelagd*
  → negativ-grind. Recurring: nya kandidater återöppnas via triggrar (b3_kandidatregister §9.4).
  **3 poster levererade 2026-06-12** (alla slutgranskade v0→v1 2026-06-14, avflaggade; codex BUILD-WITH-CHANGES ×2,
  voteringar + citat omverifierade mot data.riksdagen.se): **(1) `nedtrappad_ersattningsprofil_akassa`**
  (ekonomi → arbetsloshet; IFAU 'Om a-kassa och löner' som syntes av R 2008:12/WP 2007:21/R 2013:10/R 2005:16;
  votering bet. 2023/24:AU9 p1: 7 supports / V opposes — instrument-exakt via motion 2023/24:2881; spegelpost-
  notering mot `inkomststarkande_hushallspolitik` = metodneutralitet) och **(2) `uppsokande_forskoleerbjudande_nyanlandas_barn`**
  (integration → skolresultat_utsatta_omraden; SOU 2020:67; votering bet. 2021/22:UbU24 p1: 6 supports
  S/M/C/V/L/MP; **SD/KD ej kodade** per MP/Nato-prejudikatet — 2022-nej + Tidö-dir. 2024:113 visar nuvarande
  stöd för snävare instrument i samma familj → none tills instrument-exakt aktuell källa). Scoreeffekt
  (förklarbar, ranking OFÖRÄNDRAD S>L>M>KD>MP>C>SD>V): ekonomi-B rör alla 8 (V −0,22 via opposes-flip);
  integration: KD −0,15 / SD −0,09 (coverage-nämnare 5→6 utan ny rad = modellkonsekvent 'vet ej'-krympning
  mot neutral), MP +0,13 (thin-coverage-flaggan släckt). **(3) `dca_avtal_usa`** (forsvar →
  nato_interoperabilitet; Försvarsberedningen Ds 2024:6, medium/high) **byggd 2026-06-12 efter
  användar-sign-off av beslutsfråga B1** med Codex-villkoren (anti-stacknings-not: DCA bilateralt
  basavtal ≠ nato_medlemskap multilateralt alliansmedlemskap, prejudikat territoriella_utslapp;
  p1-källkonstruktion: huvudvoteringen bet. 2023/24:UFöU1 p1 [266–37, 3/4-majoritet] saknas i
  voteringlista-API:t → beslutsnotis HB01UFöU1 + följdvoteringarna p5/p3 live-omverifierade;
  stance-confidence max medium): 6 supports S/M/SD/C/KD/L, **V + MP opposes** (avvikande meningar
  Ds 2024:6 bilaga 4, citat ordagrant verifierade; MP:s villkorade nej = bunten-regeln §2, MP:s
  FÖRSTA aktuella position på indikatorn). Scoreeffekt (förklarbar, ranking OFÖRÄNDRAD): C/KD
  forsvar +0,04 (coverage 3/4→4/5), MP forsvar −0,13 (ny opposes + 1/4→2/5), S/M/SD/L/V oförändrade
  (indikatorcell redan mättad ±1, coverage-kvot 1,0). **`rattssakerhetsgarantier_preventiva_tvangsmedel`
  ⏸️ HOLD MED TRIGGER (beslut 2026-06-14: behåll HOLD)** — stacknings-tilt (andra rättssäkerhetsposten i
  personlig_frihet) + S-kodningens neutralitetsfälla i en bias-känslig kategori; Codex förordade HOLD.
  Inte aktivt arbete; underlaget bevarat för direkt återupptag (voterings-id:n, Lagrådscitat). **Återöppnas**
  vid preventivlagens lagstadgade oberoende utvärdering (~2028). Se
  [beslutsunderlag_hold_2026-06-12.md](done/beslutsunderlag_hold_2026-06-12.md) +
  [b3_kandidatregister_2026-06-12.md §9.2](done/b3_kandidatregister_2026-06-12.md).
- **B4 — Kategori-täckningsaudit (anti-binär garanti)** ✅ **LEVERERAD** *(grind 2026-06-05; audit aktuell)* —
  garantin "ingen kategoris B vilar på ett enda undermått" är aktiv: `b_submeasure_spread()`-grinden flaggar
  nära-binär kategori offline, och live-auditen visar **inga nära-binära**. Täckningsaudit (aktiva åtgärdstyper × undermått de matar):

  *(Tabellen avstämd mot live `b_submeasure_spread` 2026-06-12 kväll: integration 3/5, ekonomi 4/6,
  valfard 4/4, forsvar 4/5, klimat 4/5, trygghet 5/5, demokrati 5/5 — inga nära-binära. Kvarvarande
  otäckta: integrations boendesegregation+normer_tillit (HOLD H3/H4), försvarets genomforbarhet_leverans
  (HOLD H6 på B-sidan — D-sidan LÖST 2026-06-12 via materielleveransutfall, se Levererat),
  klimats industriell_konkurrenskraft + trygghets/valfards target-/indikatorlösa — se
  [beslutsunderlag_hold_2026-06-12.md](done/beslutsunderlag_hold_2026-06-12.md).)*

  | Kategori | Undermått m. B-evidens | Andel kat-vikt | Status |
  |---|---|---|---|
  | ekonomi | ~~1/5~~ **4/6** | ~~25 %~~ **73 %** | ✅ åtgärdad 2026-06-05 (FoU→produktivitet + företagande/investeringar + hushållens disponibla inkomst). 4 av 4 B-möjliga täckta; inflation/off.finanser = target (vilande) |
  | demokrati | ~~1/5 → 4/5~~ **5/5** *(transparens_ansvar täckt via insyn_partifinansiering — låg/2018; **KU39-uppgraderingen prövad och FÄLLD 2026-08-16**, buntad omnibus → HOLD, se not under tabellen)* | **100 %** | ✅ åtgärdad 2026-06-05/06: (1) grundlagsskydd domstolarnas oberoende → otillborlig_politisering (votering KU2), (2) begränsa biometrisk realtidsövervakning m. rättssäkerhet → overvakning_utan_rattssakerhet (votering JuU28, **blocköverskridande**, Lagrådet-ankrat), **(3) lagstadgat oberoende public service → mediefrihet (enhälligt bet. 2025/26:KrU2 p1, prop. 2024/25:166 ur parlamentarisk kommitté SOU 2024:34 → alla 8 supports; codex BUILD-WITH-CHANGES, mekanism-/designevidens low/low; demokrati 3/5 → 4/5)**. transparens_ansvar täckt (insyn_partifinansiering). **KU39-återöppningen prövad och fälld 2026-08-16:** bet. 2025/26:KU39 hade en enda punkt som buntar lobbyregister + fackbidragslagen + 2018:90-ändringen; följdmotionerna (S 4151, C 4184) yrkade avslag ENBART på fackbidragsdelen, den bygginstruktionen förbjuder. Neutralitetsgrind punkt 4 (buntad omnibus förkastas) → **HOLD**, underlaget bevarat. Ny trigger: instrument-exakt källa för enbart lobbyregistret |
  | valfard | ~~2/4~~ **4/4** *(2026-06-12: live-mätaren — kontinuitet/NHV-byggena 2026-06-07 täckte resten)* | **100 %** | tunn — vard_tillganglighet + omsorg_personal HOLD 2026-06-06, **djupsvep §5.8 (11 instrument) bekräftar**: vårdplats-slutrapport 2026:3 föll *nedåt* (villkor konsumerat), cancerscreening klarar steg 1 men faller på neutralitet (avslag/opp-reservationer); omsorg_personal = fel konstrukt (kompetens/heltid/kontinuitet ≠ omsättning). HOLD:arna STÄNGDA som BEVAKA med triggrar (sign-off 2026-06-12, beslutsunderlag H1+H2: cancerstrategi-enighet resp. Socialstyrelse-omsättningsmått) |
  | forsvar | ~~2/5 → 3/5~~ **4/5** *(2026-06-12: +ekonomisk_ambition via forsvarsfinansiering-posten 2026-06-07)* | **95 %** | ✅ nato_ukraina tillagt 2026-06-06 (nato_medlemskap, votering UU16, Försvarsberedningen-källa, codex-granskat: V=opposes, MP=none pga reversering). Kvar: ekonomisk_ambition=target (ej B-bar), genomforbarhet_leverans (HOLD, **djupsvep §5.8/7 instrument bekräftar äkta steg-1-vägg**: ingen svensk källa kopplar instrument → kortad *leveranstid*, bara kapacitet/kostnad; sign-off 2026-06-12 (H6, A+B): BEVAKA utvärderings-triggern + FMV-leveransindex-sondering BEVILJAD → **sonderingen LEVERERADE på D-sidan 2026-06-12 sen kväll: materielleveransutfall (FMV leveransindex ap. 1:3.1, NY kanonisk D-only-indikator, v0) öppnade genomforbarhet_leverans i D — försvar ur `d_thin_breadth_accepted` (70→75/100). B-sidan kvarstår BEVAKA** (FöU3-utvärderingstriggern; tabellens 4/5 avser B-evidens, oförändrat)) |
  | integration | ~~2/5~~ **3/5** *(2026-06-12: +skola_sprak via uppsokande_forskoleerbjudande, B3)* | **65 %** | tunn — normer_tillit + boendesegregation HOLD 2026-06-06, **djupsvep §5.8 (11 instrument) bekräftar**: boendesegr. = äkta steg-1-vägg (allt beskrivande/mixed), normer_tillit/KU4-tillgänglighet = perfekt steg 2 men fel konstrukt (förmåga att rösta ≠ uppmätt valdeltagande). Högsta bias-risk; HOLD/BEVAKA bekräftad med loggade mandat-undantag (sign-off 2026-06-12, beslutsunderlag H3+H4; triggrar: enig GOTV/UbU-behandling resp. bosättningslag-betänkandet ~2027) |
  | trygghet | ~~3/5 → 4/5~~ **5/5** *(2026-06-12: +forebyggande via kommunalt_brottsforebyggande 2026-06-07)* | **100 %** | ✅ snabbforfarande_lagforing 2026-06-06 (handlaggningstid, Brå 2020:3, enhälligt bet. JuU2 p1 → alla 8 supports, codex BUILD-WITH-CHANGES). Kvar: forebyggande (saknar indikator) |
  | klimat | ~~3/5~~ **4/5** | ~~70 %~~ **85 %** | ✅ atgarder_mot_invasiva_frammande_arter 2026-06-06 (hotade_arter_naturforlust, Naturvårdsverket, enhälligt bet. MJU13 p1 → alla 8 supports). **SIGN-OFF 2026-06-12 (H5, VAL A): BEHÅLL + AVFLAGGAD, v0→v1** (konsensus-mått, low/low kvarstår). Kvar: industriell_konkurrenskraft (saknar indikator) |

  Mål: ≥2–3 undermått med evidens per kategori; ingen kategori där en enda åtgärdstyp (eller ett undermått) kan
  svänga betyget mellan ytterlägen. **Verktyg/grind ✅ levererad 2026-06-05** (se B4-verktyg under Levererat):
  [coverage_report.py](../pipeline/tools/coverage_report.py) `b_submeasure_spread()` flaggar nära-binär
  kategori (≤1 undermått) och [test_fas4b_coverage.py](../tests/test_fas4b_coverage.py) + nya
  `coverage_allowlist.b_near_binary_accepted` gör regressionen synlig. **Kvar (=B2):** faktiskt höja
  spridningen till ≥2 undermått för ekonomi och demokrati. **VIKTIGT fynd från grinden:** inflation och
  offentliga finanser (ekonomi) är target-indikatorer → kan inte få riktat B-bidrag; ekonomis enda
  realistiska B-mål är produktivitet och reallöner (up-indikatorer). Knyter an till B2 (ekonomi/demokrati först).
  - **Demokrati är trippel-svag** (fynd vid 79-screeningen 2026-06-05): (1) nära-binär (1/5 undermått), (2) liggaren
    är enbart `expert_opinion` (rekommendationer, ej uppmätt effekt), och (3) partiståndpunkterna bygger till stor del
    på **enskilda ledamotsmotioner** (4 av `starkt_oberoende_granskning`-raderna M/SD/KD/L + flera antikorruptionsrader
    är `enskild_motion`). Riktningen är låg-risk (alla stödjer antikorruption), men demokrati-B vilar på den svagaste
    provenansen i hela modellen → bör antingen få bredare/bättre källor eller redovisas med uttryckligt lågt förtroende.

- **B5 — B-undermåttsbreddskrympning (parallellen till D:s coverage_shrink)** ✅ *(öppnad 2026-06-12
  ur [done/d_coverage_krympning_spec.md §8](done/d_coverage_krympning_spec.md); spec
  [done/b_coverage_krympning_spec.md](done/b_coverage_krympning_spec.md) v2 Codex-granskad
  APPROVE-WITH-CHANGES)* — **LEVERERAD OCH AKTIVERAD 2026-06-14** (§10.7-sign-off): enhetlig viktad
  undermåttsdjuptäckning `cov_B` (spec §3.3 — ERSÄTTER antalsmåttet så dubbelrabatten aldrig
  uppstår) är nu default `B_evidens.coverage_mode: weighted_submeasure_depth`; delar D:s
  icke-target-nämnare (`_non_target_submeasures`), testat i
  [test_b_coverage_mode.py](../tests/test_b_coverage_mode.py). `dist/` omräknad + snapshot
  rebaselinad — den signade switch-diffen verkställde **KD↔MP-flippen** i totalranking
  (S > L > M > MP > KD > C > SD > V; ny marginal 0,0085 inom 80 % CI-överlapp), 106 B-drivna
  ändringar, 8 tunnhetsflaggor. Legacy `policy_type_count` kvar via config-override.
  Spec arkiverad till done/.

---

## Spår A — Agerande (delpoäng A)

- **A1 — Fler budgetår** ✅ *(levererad 2026-06-05)* — `budget_ramar.yaml` täcker nu **budget
  2023 + 2024 + 2025** (samma trogna transkriberingsmönster, källrad per frame). a1 är ett snitt
  över åren i stället för en enda mätpunkt. Fyrlagrigt verifierad (invariant + pandas + Codex +
  roll-call); se Levererat ovan + [metod](done/fas1b_budget_metod.md).
- **A2 — Aktivera voteringsprovet** ⏸️ **PARKERAD (designbeslut 2026-06-14)** — designfrågan är
  utredd och löser sig mot park på princip (samma klass som C1/D1): det finns ingen neutral,
  icke-redundant signal att väga in i A. (a) Röst*riktningen* (ja/nej) är **stance**, och stance
  fångas redan fullständigt av **B** (party_positions.yaml är byggd ur exakt dessa voteringar, 802
  källrader) — A är dessutom medvetet `Direktionsneutralt` ("rättheten fångas av B och D",
  scoring.yaml). Att poängsätta röstriktning i A vore att dubbelräkna B och bryta A/B-separationen.
  (b) Röst*volym/deltagande* per kategori är agendadrivet (alla partier röstar på samma ärenden)
  → odifferentierande och redundant med a2 (motionsandel). Voteringsprovet behålls som **källa**
  (matar B/provenans), inte som egen A-komponent. Återöppnas bara om ett neutralt emfas-mått ur
  röstdata identifieras som a2 inte redan fångar. A = 0,6·a1 + 0,4·a2 (oförändrat).

---

## Spår C — Ansvar (delpoäng C)

- **C1 — c2 (finansiering)** ⏸️ **PARKERAD (designbeslut 2026-06-14)** — inget objektivt,
  riktningsneutralt finansieringsmått går att bygga ur officiell svensk data: alla partibudgetar är
  formellt fullt finansierade (rambeslutsmodellen) → likformigt, och ett saldo-/ramverksmått skulle
  gynna åtstramning → bryter neutraliteten (CLAUDE.md). C = c1 (makt) tills vidare; komponentvikten
  0.7/0.3 behålls som dokumenterad avsikt. **Inte aktivt arbete** — återöppnas endast om en neutral
  officiell källa uppstår (samma klass som D1: stängd på princip, inte på datatillgång). Detalj:
  [fas1c_subnational_metod.md §c2](done/fas1c_subnational_metod.md).
- **C2 — Mandatperiodskiften mitt i period** ⏸️ **I ALLT VÄSENTLIGT LÖST / data-begränsad rest
  (2026-06-14)** — premissen var stale för det NATIONELLA: regeringsbyten mitt i år är redan
  finhanterade via dagviktning (`year_power_fractions`/`government_fractions`), t.ex. 2022 = S 0,795
  (Andersson) + M/KD/L 0,205 (Kristersson) + SD 0,103 (stöd). Den enda kvarvarande grovheten är
  *subnationella* mid-term-styrbyten (en regional/kommunal koalition som spricker mitt i perioden) —
  och det är en **datakälla-begränsning**: SKR:s officiella öppna data är post-val-snapshots per
  mandatperiod, det finns ingen ren officiell mid-term-serie. Lågt mervärde (sällsynt). Återöppnas
  bara om SKR (eller motsv.) publicerar en maskinläsbar mid-term-styresserie.
- ~~**C3 — Subnationell D-resultatdata**~~ ✅ **LEVERERAD + AKTIVERAD 2026-06-14** — D blandar nu
  in region-nivå vårdutfall (Kolada U70471 överlevnad + N79242 vårdköer, alla 21 regioner) och
  attribuerar dem till det parti som styrde regionen (speglar hur C blandar nationell + subnationell
  makt). v0 = region-nivå välfärd (`vard_tillganglighet`); submåtts-blandning national 0,4 / region
  0,6; år-ekvivalent ansvarsgrind + soundness-grind (`region_basis ≥ min_responsibility`).
  Rättvisefix: V blir measured för välfärd via regional vård-makt; SD (styr ~inga regioner) gated
  bort. Neutralitetsauditerad (`pipeline/tools/c3_sensitivity.py`); endast välfärds-D rör sig,
  totalranking oförändrad. Gated på `scoring.D_resultat.subnational.enabled`.
  [Metod](done/c3_subnational_d_metod.md). **Utvidgningsväg:** kommun-nivå (skola/bistånd) i
  framtida våg, samma maskineri.

---

## Spår F — Frontend & publicering

- ~~**F1 — Faktisk publicering**~~ ✅ **LEVERERAD 2026-08-16** — repot pushat till
  [mcknschn/rosta](https://github.com/mcknschn/rosta) (publikt) och sajten ligger på
  **<https://mcknschn.github.io/rosta/>**. GitHub Pages med källa GitHub Actions;
  [pages.yml](../.github/workflows/pages.yml) laddar upp `web/` som sajtrot vid varje push till
  `main`. Ingen byggkedja: frontenden är byggfri statisk och läser `web/data/`, synkat från
  `dist/` med `scripts/sync_dist.py`. Rådata och warehouse stannar lokalt per design.
  Befintlig [ci.yml](../.github/workflows/ci.yml) kör nu skarpt (ruff + pytest, py3.11/3.12) —
  den hade aldrig körts tidigare eftersom repot saknade remote, vilket dolde 11 ruff-brott och
  två fallerande e2e-test tills 2026-08-16.
- **F2 — Manuell skärmläsartest** 🔵 **redo att köras** — protokoll skrivet:
  [fas6_skarmlasartest.md](fas6_skarmlasartest.md), 9 testfall (skip-länk, rubriker, banner,
  sliders, live-status, expandering, fokus, tabell, felläge). Kräver NVDA/VoiceOver + människa;
  ca 20 min. Sista WCAG 2.2 AA-punkten.

---

## Spår O — Drift, robusthet & ops ✅ KOMPLETT (O1–O4, 2026-06-03/05)

- ~~**O1 — Serie-drift-skydd**~~ ✅ — [pipeline/expectations.py](../pipeline/expectations.py),
  förväntansassertion per inläst serie (se Levererat 2026-06-03).
- ~~**O2 — Snapshot/diff**~~ ✅ — [score_diff.py](../pipeline/tools/score_diff.py) mot
  `dist/scores.snapshot.json` (se Levererat 2026-06-03).
- ~~**O3 — Live-fetch smoke test**~~ ✅ — [test_sources_live.py](../tests/test_sources_live.py),
  opt-in `ROSTA_LIVE=1` (se Levererat 2026-06-03). *(O4 reproducerbar dist ✅ 2026-06-05.)*

---

## Föreslagen ordning (vågor)

| Sprint | Data (D) | Evidens (B) | Övrigt |
|--------|----------|-------------|--------|
| **1** | ~~Våg 1: Brå (uppklaring/handläggning/återfall) + Socialstyrelsen (överlevnad)~~ ✅ avslutad 2026-06-09 | ~~**B1: starta expertgranskning**~~ ✅ sign-off 2026-06-05 | ~~**O1: drift-skydd**~~ ✅ |
| **2** | ~~Våg 2: Medlingsinstitutet (reallöner)~~ ✅ (MI:s egen PxWeb, 2026-06-12) + ~~Skolverket (sfi)~~ ✅ (SCB TAB1814, Tier 2) + ~~Svk-adapter (gränsfall källregel)~~ ✅ stängt 2026-06-12 (Kraftbalansrapporten, ej adapter) | ~~B2: bredda liggaren~~ ✅ *(valfard/integration HOLD-beslut avgjorda 2026-06-12 (H1-H4); **transparens_ansvar-bygget prövat och fällt 2026-08-16** — KU39 = buntad omnibus → HOLD)* | ~~A1: fler budgetår~~ ✅ klar |
| **3** | Våg 3: härledda klimat — ~~elpris~~ ✅ + ~~effekt~~ ✅ (båda 2026-06-12 kväll); ~~utsläpp-per-krona~~ ✅ stängt 2026-06-12 (D1, design_closed) → **Spår D klart** | ~~B3: omstridda åtgärdstyper~~ ✅ (3 byggen avflaggade v1 2026-06-14; kvar endast B2 HOLD) · ~~B5: B-breddskrympning~~ ✅ aktiverad 2026-06-14 | A2 votering · C2/C3 · F1/F2 |

> Varje levererat steg: flytta indikatorn ur `coverage_allowlist.yaml`, uppdatera täckningssiffran
> i `scorerun.py:coverage`-strängen, och bocka av posten här (✅ → kort rad i ROADMAP.md).
