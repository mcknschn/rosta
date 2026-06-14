# Fas 4c — förregistrerad rubrik för B-differentiering

> **Status: FRYST 2026-05-30.** Denna rubrik är gemensam för Plan B (harmonisering av befintliga
> partiståndpunkter) och Plan A (utökning av evidensliggaren). Den är **förregistrerad**: reglerna
> låses INNAN data bedöms, och får inte ändras under en körning för att passa ett önskat utfall.
> Ändringar av rubriken kräver ny version + motivering här. Designen är fastlagd i samråd (Codex,
> 2026-05-30). Bygger vidare på [fas4b_partistandpunkter_metod.md](fas4b_partistandpunkter_metod.md).

Syftet är att ta bort de två svagheterna i den nuvarande B (version 0): (1) **isolerings-inducerade
verifierar-asymmetrier** (samma slags källa bedömdes olika strängt för olika partier), och (2) **svag
särskiljning** (för få omstridda, evidensbelagda åtgärdstyper). Rubriken får INTE höja B:s
särskiljning på bekostnad av no-fabrication-garantin.

---

## 1. Stance-regeln (instrument-exakt) — oförändrad från metoddoc §4

Sätt `supports`/`opposes` endast om en officiell svensk källa belägger partiets ställningstagande till
**samma policyinstrument** (inte bara samma mål), med ordagrant citat + dokument-id. "Vi vill minska
utsläppen" räcker inte; "vi vill höja koldioxidskatten" räcker. En oberoende granskare utan politisk
tolkning ska kunna peka på text/votering som **direkt** avser instrumentet.

## 2. Bunten-regeln (avgör M/L-asymmetrin)

En motion som buntar flera instrument i samma stycke/yrkande **räknas för det namngivna instrumentet**
om citatet är instrument-exakt enligt §1. Den interna nyansen (att motionen även vill något annat, eller
fasar ut en delvariant) skrivs i `mapping_note` och **används ALDRIG som skäl att förkasta raden**.

> Detta är den direkta rättelsen av det dokumenterade felet där M:s buntade `subventionerade_anstallningar`
> godkändes men L:s analoga buntade ståndpunkt förkastades. Under bunten-regeln bedöms båda lika: instrument-
> exakt citat ⇒ raden gäller, nyansen noteras. (Harmoniseringen kan landa i att båda gäller, eller — om
> citatet vid panelgranskning visar sig icke-instrument-exakt — att båda utelämnas. Se §6.)

## 3. Källhierarki och regeln för enskild motion

Rangordning (från metoddoc §3): **votering** (guldstandard) > parti-/kommitté-/budgetmotion > valmanifest
> partiprogram (endast kontext). Otillåtet för stance: media, intresseorganisationer, internationella index.

**Enskild motion (single-member):** en motion undertecknad av en enskild ledamot (ej kommitté-/partimotion,
ej budgetmotion) får representera partilinjen **endast med `confidence: low`**, och endast om ingen starkare
partikollektiv källa finns. Saknas partikollektiv källa helt och den enskilda motionen är svag → **utelämna
raden** (coverage-lucka, inte stance). Detta beslut låses här och tillämpas symmetriskt över alla partier.

## 4. Tidsregel

`date`/riksmöte krävs. Föredra senaste mandatperioden (2022/23–2025/26). En äldre instrument-exakt källa
får användas om ingen nyare hittas, men `mapping_note` ska ange att den är utanför föredragen period
(symmetriskt: gäller alla partier lika, ingen får strängare tidskrav än en annan).

## 5. Evidens-admission i liggaren (Plan A) — negativ-riktnings-grinden

En evidensliggar-post (`policy_type → indikatoreffekt`) admitteras endast om den citerar en officiell svensk
källa (myndighet/svensk akademi) och avser **exakt den betygsatta indikatorn**.

**Negativ-riktnings-grinden (Codex P0 — den enskilt viktigaste integritetsregeln för Plan A):**
en post med `direction: negative` får bidra till B (dvs. dra ned B för ett parti som stödjer instrumentet,
eller upp för ett som motsätter sig det) **endast om ALLA tre gäller**:

1. `evidence_level ∈ {authority_evaluation, systematic_review}` — aldrig enskild studie, beskrivande
   statistik eller expertutlåtande för en negativ B-effekt.
2. `confidence ≥ medium`.
3. Evidensen avser **exakt den betygsatta indikatorn** — ingen sidoeffekt-proxy. Om evidensen mäter en
   storhet som inte är indikatorn själv (t.ex. IFAU mäter "arbetslöshetstid", indikatorn är `arbetsloshet`),
   ska **indikator-bryggan skrivas ut explicit i `note`**, källbeläggas och granskas. Håller inte bryggan
   → posten admitteras inte (eller kodas `mixed`/`unclear` → inert).

> Varför strängare för negativ riktning: ett negativt B-bidrag är politiskt laddat (det säger "partiets
> drivna åtgärd går enligt evidensen åt FEL håll"). Modellen *ska* våga göra detta (metoddoc §9), men bara
> när evidensen är robust och avser rätt sak — annars riskerar B att se partiskt ut. Positiv riktning har
> kvar den ordinarie admissionen (metoddoc), eftersom ett uteblivet eller för svagt positivt bidrag inte
> straffar ett parti på samma laddade sätt.

## 6. Värdekonflikt utan officiell evidens ⇒ utelämnas (B tiger hellre än gissar)

Instrument där partierna är oense av **värdeskäl** men det saknas riktad officiell evidens på en kategori-
indikator (eller evidensen är `mixed`/`unclear` → `signed_direction = 0`) **kodas inte in i B**. B mäter
*evidens-kodbar instrumentell träffsäkerhet*, inte all viktig politik. Detta **redovisas explicit** (disclosure)
så att tystnaden inte misstas för en mätning. Varje sådant instrument loggas i inert/exkluderad-listan med skäl.

## 7. Generaliserad exkluderingsregel (ersätter ad hoc-undantaget)

En `policy_type` lyfts ur **coverage-nämnaren** (`coverage_exclude`) när — och endast när — den uppfyller en
av dessa principiella grunder, som ska anges som skäl i `config/scoring.yaml: B_evidens.coverage_exclude_reasons`:

- **(E1) Sidoeffekt-negativ:** posten har `direction: negative` men evidensen avser en sidoeffekt, inte
  instrumentets kärnvärde, så att en stance-kodning skulle ge missvisande B-sign. *(Detta är skälet till att
  `internationella_materielsamarbeten` exkluderas: RiR 2011:13 mäter leveranstidsrisk, inte om materielsamarbete
  i sig är sämre försvarspolitik — ett parti som stödjer samarbete ska inte få sämre försvars-B. Faller på §5.3.)*
- **(E2) Inert per konstruktion:** posten är `mixed`/`unclear` (`signed_direction = 0`) och kan aldrig ge
  B-effekt; den hålls utanför nämnaren för att inte blåsa upp den med icke-kodbara rader.

Ingen `policy_type` får exkluderas utan ett skäl ur denna lista. Test (`tests/test_fas4c.py`) tvingar att varje
exkluderad policy_type finns i liggaren och har ett dokumenterat skäl.

## 8. Inget täckningsmål (no target coverage rate)

Varken harmonisering (Plan B) eller utökning (Plan A) får styras mot en önskad andel kodade rader eller en
önskad fördelning supports/opposes. Coverage är ett *utfall* av vilka instrument-exakta källor som faktiskt
finns, aldrig ett *mål*. Att "fylla luckor" för att höja ett partis coverage är förbjudet; en lucka som inte
kan beläggas instrument-exakt förblir en lucka.

## 9. Panel-verifieringsprotokoll (Plan B & A4)

Mot isolerings-asymmetrin (§2) verifieras varje `policy_type` som en **panel**:

1. **Insamling:** för varje av de 8 partierna, sök fram den bästa instrument-exakta kandidatkällan
   (data.riksdagen.se). Spara även **förkastade kandidater med skäl** (rejected-candidate-log).
2. **Första-pass (per rad, mot rubriken §1–§4):** bedöm varje kandidat fristående: instrument-exakt? rätt
   stance-riktning? källa i hierarkin? Detta görs FÖRE jämförelsen för att undvika utjämningstryck/groupthink.
3. **Sida-vid-sida-harmonisering (per policy_type):** lägg alla 8 partiers första-pass-bedömningar bredvid
   varandra och kontrollera att **samma standard** tillämpats (ingen får strängare/lösare krav). Justera bara
   genom att tillämpa rubriken lika — aldrig genom att jämna ut till en önskad fördelning.
4. **"Harmonisera standarden, inte slutsatsen":** om den lika standarden kräver att en rad DROPPAS (snarare än
   att en analog ADDERAS), gör det. Utfallet får vara asymmetriskt om verkligheten är det.
5. **Logg:** varje (parti, policy_type) får ett keep/add/drop/unknown-beslut med skäl i audit-filen.

## 10. Bevarade integritetsregler (oförändrade)

- Ingen ståndpunkt fabriceras; varje rad citerar en officiell svensk källa ordagrant med dok-id.
- Endast officiella svenska källor; akademiska svenska källor när officiell statistik saknas (CLAUDE.md).
- Allt mänskligt omdöme i versionsstyrd config + denna rubrik; inga partibetyg i kod.
- Allt lokalt; inga commits utan begäran.
- Version 0 tills mänsklig slutgranskning gjorts; rubriken ersätter inte den granskningen.
