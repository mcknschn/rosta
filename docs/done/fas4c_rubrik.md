# Fas 4c — förregistrerad rubrik för B-differentiering

> **Status: version 2, fryst 2026-08-21.** Denna rubrik är gemensam för Plan B (harmonisering av
> befintliga partiståndpunkter) och Plan A (utökning av evidensliggaren). Den är **förregistrerad**:
> reglerna låses INNAN data bedöms, och får inte ändras under en körning för att passa ett önskat
> utfall. Ändringar av rubriken kräver ny version + motivering här. Designen är fastlagd i samråd
> (Codex, 2026-05-30). Bygger vidare på
> [fas4b_partistandpunkter_metod.md](fas4b_partistandpunkter_metod.md).
>
> **Versionshistorik**
>
> - **version 1, fryst 2026-05-30.** Ursprunglig förregistrering.
> - **version 2, 2026-08-21** ([ADR 0006](../adr/0006-evidensgrinden-ar-symmetrisk.md), biljett
>   [#18](https://github.com/mcknschn/rosta/issues/18)). §5 skrevs om symmetriskt och §7 grund E1
>   blev riktningsneutral. Skälet: §5:s asymmetri hade ett enda nedskrivet skäl, att ett svagt
>   positivt bidrag inte straffar ett parti, och det skälet föll när
>   [ADR 0004](../adr/0004-vad-delpoang-b-mater.md) byggdes. En svag positiv post ger sedan dess
>   3,25 i stället för 5,00 och drar alltså ned. Nivån i §5 är oförändrad från version 1. Den
>   tillämpas nu åt båda håll i stället för åt ett.

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

## 5. Evidens-admission i liggaren (Plan A) — den symmetriska evidensgrinden

> **Omskriven i version 2** ([ADR 0006](../adr/0006-evidensgrinden-ar-symmetrisk.md)). Hette tidigare
> "negativ-riktnings-grinden" och gällde bara `direction: negative`. Nivån är oförändrad. Den
> gäller nu åt båda håll.

En evidensliggar-post (`policy_type → indikatoreffekt`) admitteras endast om den citerar en officiell svensk
källa (myndighet/svensk akademi) och avser **exakt den betygsatta indikatorn**.

**Den symmetriska evidensgrinden:** en liggarpost får bidra till B **oavsett verkan** endast om ALLA tre
gäller:

1. `evidence_level ∈ {authority_evaluation, systematic_review}` — aldrig enskild studie, beskrivande
   statistik eller expertutlåtande.
2. `confidence ≥ medium`.
3. Evidensen avser **exakt den betygsatta indikatorn** — ingen sidoeffekt-proxy. Om evidensen mäter en
   storhet som inte är indikatorn själv (t.ex. IFAU mäter "arbetslöshetstid", indikatorn är `arbetsloshet`),
   ska **indikator-bryggan skrivas ut explicit i `note`**, källbeläggas och granskas. Håller inte bryggan
   → posten admitteras inte (eller kodas `mixed`/`unclear` → inert).

> Varför grinden är symmetrisk: version 1 höll bara negativ verkan till nivån ovan, med skälet att ett
> uteblivet eller för svagt positivt bidrag inte straffar ett parti på samma laddade sätt. Det var sant när
> B var `tecken(stance) x täckning`, för då gav en svag positiv post `+1`, alltså 5,00. Efter
> [ADR 0004](../adr/0004-vad-delpoang-b-mater.md) ger samma post `effect_strength: low`, alltså betyget
> 3,25, och drar därmed ned. Asymmetrins enda skäl har alltså fallit. Grinden vid dörren är dessutom den
> enda skärmen mot svag evidens i poängen: `net = Σ(q·m)/Σ q`, så i en cell med ett enda claim tar `q` ut
> sig och `net = m`. 184 av 228 celler har exakt ett claim.

**Verkan (`direction` i liggaren) är inte samma sak som Riktning.** Riktning är indikatorns egen
riktning, alltså upp, ned eller målnivå (`indicators[].direction`). Verkan säger om åtgärden rör
indikatorn åt rätt håll relativt den riktningen. Se ordlistan i
[evidens_trovardighet.md §4.3](evidens_trovardighet.md).

### 5b. Sökregeln: källstyrd och riktningsblind

Nya liggarposter söks genom att räkna upp **officiella utvärderingar per indikator**, och verkan blir
vad utvärderingen fann. Riktningen får aldrig stå i sökbegreppet. En sökning som frågar "vilka åtgärder
har negativ evidens?" vet vad den vill hitta innan den letar, och det gör sökandet i sig till en partisk
handling. Samma sak gäller omvänt: **B-grön-mandatet är avvecklat**, alltså kravet att varje undermått
ska ha minst en post med positiv verkan.

**Ordningsregel:** verkan, `effect_strength` och `evidence_level` låses och skrivs ned INNAN
partiraderna för åtgärdstypen slås upp i `config/party_positions.yaml`, och svepet loggar att det skedde
i den ordningen. Regeln biter bara på nya åtgärdstyper. För de åtgärdstyper som redan står i liggaren är
partiraderna kända, och den kunskapen går inte att ta tillbaka.

## 6. Värdekonflikt utan officiell evidens ⇒ utelämnas (B tiger hellre än gissar)

Instrument där partierna är oense av **värdeskäl** men det saknas riktad officiell evidens på en kategori-
indikator (eller evidensen är `mixed`/`unclear` → `signed_direction = 0`) **kodas inte in i B**. B mäter
*evidens-kodbar instrumentell träffsäkerhet*, inte all viktig politik. Detta **redovisas explicit** (disclosure)
så att tystnaden inte misstas för en mätning. Varje sådant instrument loggas i inert/exkluderad-listan med skäl.

## 7. Generaliserad exkluderingsregel (ersätter ad hoc-undantaget)

En `policy_type` lyfts ur **coverage-nämnaren** (`coverage_exclude`) när — och endast när — den uppfyller en
av dessa principiella grunder, som ska anges som skäl i `config/scoring.yaml: B_evidens.coverage_exclude_reasons`:

- **(E1) Sidoeffekt-proxy:** evidensen avser en sidoeffekt, inte instrumentets kärnvärde, så att en
  stance-kodning skulle ge missvisande B-sign. Grunden gäller **oavsett verkan** (omskriven i version 2,
  [ADR 0006](../adr/0006-evidensgrinden-ar-symmetrisk.md); hette tidigare "sidoeffekt-negativ" och var
  formulerad bara för `direction: negative`). *(Detta är skälet till att `internationella_materielsamarbeten`
  exkluderas: RiR 2011:13 mäter leveranstidsrisk, inte om materielsamarbete i sig är sämre försvarspolitik —
  ett parti som stödjer samarbete ska inte få sämre försvars-B. Faller på §5.3.)*
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
