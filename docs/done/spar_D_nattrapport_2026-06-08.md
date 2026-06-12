# Spår D — Nattrapport 2026-06-08 (alla försök, lyckade + misslyckade)

> **Uppdrag (din beställning kväll 2026-06-07):** gå igenom D-serien kategori för kategori, nå
> helst **4 mätbara D-indikatorer per kategori** (3 OK; 2 → funderare om vi alls kan hävda "god
> effekt"). Prio 1: dubbelkolla/försök igen på redan identifierade indikatorer (bygg PDF-pipeline om
> det krävs). Prio 2: leta + testa bygga nya. Rapport på ALLA försök, lyckade som misslyckade.
>
> **Källregel (CLAUDE.md):** endast officiella svenska källor; svensk akademi när officiell saknas;
> inga internationella index. Allt nytt = flaggad **v0**, per-indikator `data:`-commit.
>
> Status-legend: ✅ byggd · 🟢 verifierad byggbar (bygger) · 🟡 behöver designbeslut/sign-off ·
> 🔴 vägg (dokumenterat skäl) · ⏳ pågår.

---

## 0. Utgångsläge (per 2026-06-08, ur spar_D_datatackning §2.1)

| Kategori | D-indikatorer byggda | Mot mål 4 |
|----------|:---:|---|
| Ekonomi | 6 | ✅ klar |
| Lag och trygghet | 5 | ✅ klar |
| Integration | 5 | ✅ klar |
| Välfärd | 3 | +1 behövs |
| Klimat | 3 | +1 behövs |
| **Försvar** | **1** | +3 behövs (svårast) |
| **Frihet/demokrati** | **1** | +3 behövs (svårast) |

---

## 1. Verktygsfynd: PDF-pipeline är möjlig (korrigerar tidigare antagande)

Tidigare antagande (i `personal_varnpliktiga.yaml` + `forsvarsmakten.py` + minnet): officiella PDF:er
är FlateDecode → ej maskinläsbara här (saknar pdftoppm; WebFetch binärt). **Detta är inte längre
sant på den här maskinen:**

- `pdfplumber 0.11.9`, `PyMuPDF 1.27.1`, `pypdf 6.9.2` installerade; `pdftotext` finns (mingw64).
- FlateDecode är standard-PDF-komprimering som alla dessa dekomprimerar. PyMuPDF kan dessutom rendera
  sidor → PNG för visuell OCR om en PDF är bildbaserad.

Konsekvens: PDF-only-väggar kan omprövas (`aterfall_i_brott` m.fl.), och `personal_varnpliktiga`
kan lyftas v0→v1 genom direktläsning av FM ÅR.

**Bevis (körning 2026-06-08, `c:\tmp\pdf_probe.py`):** FM ÅR 2025-PDF:en (5,9 MB) laddades ner och
`pdfplumber` extraherade **373 739 tecken** text. Direkta träffar i brödtexten:
- *"Under året påbörjade 8 136 värnpliktiga sin grundutbildning"* → bekräftar 2025 = **8 136** (matchar v0).
- *"Av de 7 343 som påbörjade grundutbildning under 2024"* → exakt 2024-siffra = **7 343** (v0 hade
  avrundat "drygt 7 300" = 7300). Tecknet 6320→7343→8136 är fortsatt entydigt upp, men v1 bör
  bära exakta 7343.

Arkitekturnot: den befintliga designen undviker *medvetet* en runtime-PDF-parser (kan korrumpera D
tyst) och använder transkribering + audit. PDF-upplåsningen ändrar inte det — pdfplumber används som
**läsverktyg för att transkribera/verifiera exakt**, inte som runtime-beroende. Invarianten består.

2018-PDF:ens gamla `siteassets`-URL i `personal_varnpliktiga.yaml` ger nu **404** (FM har flyttat
filerna) — en separat fynd: käll-URL:erna i configen är delvis döda och bör uppdateras vid v1.

---

## 2. Försökslogg (append per försök)

### VÄLFÄRD (3 → mål 4) ✅ MÅL NÅTT

**✅ BYGGD: `overlevnad_svar_sjukdom`** (submått vard_tillganglighet, riktning up) — commit `65a5eda`.
- Källa: Kolada **U70471** "Överlevnad vid tjocktarmscancer, 30 dagar efter akut operation" (Social-
  styrelsen), **verifierad live via repo:ts egen adapter**: 16 konsekutiva år 2010-2025 (91,6→96,0 %).
- Löser den gamla §5.3-frågan: det kvinkenniala 5-årscancermåttet (N79196) var odugligt; U70471 är den
  ÅRLIGA officiella överlevnadsserien för svår sjukdom (matchar riktning up). Diskriminerande (genuina
  nedgångsår 2012/2017/2020/2024). **Välfärd 3 → 4 D-indikatorer.**
- Betygseffekt: endast valfard; nedgångsåren 2017/2020 landar på S-MP + JÖK-stöd → C −0,063 / MP −0,044 /
  L −0,030 valfard; S +0,010 (längre fönster, fler uppår); Tidö marginellt ned. Ranking oförändrad. v0.

**🔴 VÄGG (bekräftad): `skillnader_mellan_skolor`** (skola, down) — ingen maskinläsbar nationell spridnings-
serie i Kolada/SCB; Skolverkets likvärdighetsindex finns bara som PDF/XLS via portal (ej stabil URL).
**`personalomsattning_omsorg`** (down) + **`valfardsbrottslighet`** (down): ingen officiell årsserie
(Kolada saknar KPI; Brå bidragsbrott bara via interaktiv export + revisionsintensitets-störning).

**Nya kandidater (rena Kolada-KPI:er, skulle ge bredd/djup; sign-off för ny kanonisk indikator):**
- `N72837` höftfraktur åldersstd./100k (2001-2024, down) — **öppnar omsorg_personal-submåttet (D-tomt!)**
  = äkta bredd. WHO-erkänt äldreomsorgs-/fallpreventionsutfall, neutralt. **Rekommenderas som sign-off-bygge.**
- `N70845` vårdplatser/1000 (1999-2023, up), `U70425` överbeläggning (2014-2024, down) — vård-djup.
- Alla maskinläsbara via `api.kolada.se`. Verifierbara på samma sätt som U70471.

---

### "DUBBELKOLL" PRIO 1: `personal_varnpliktiga` PDF-verifierad ✅ (commit `23b9215`)

- FM ÅR-PDF:erna ÄR maskinläsbara (pdfplumber) — **det gamla "FlateDecode oläsbart"-antagandet i configen
  + minnet är överspelat på den här maskinen.** Agent läste FM ÅR 2018-2025 direkt.
- 7/8 år direkt verifierade ur FM ÅR (citat/Personalberättelsens tabeller). **Korrigeringar:** 2020
  4917→4915 (FM ÅR 2022 bil.1 Tab6, inkl. HAGS), 2024 "drygt 7 300"→**7343** (FM ÅR 2024 bil.1 Tab3).
  Döda siteassets-URL:er bytta mot fungerande globalassets. 2019 = "drygt 4 500" (enda mjuka punkten;
  bilaga-PDF 404). **Inga D-tecken ändras** (monoton upp utom 2021→2022) → ranking + betyg oförändrade.
- v0 kvarstår tills din sign-off → då **v1** (per configens egen kriterium "transkriberat direkt ur PDF").

---

### FÖRSVAR (1 → mål 4)

**✅ BYGGD: `ukraina_stod`** (submått nato_ukraina, riktning up) — commit `05dc3b3`.
- Källa: Regeringens samlade redovisning av militärt stöd till Ukraina (regeringen.se), per-år-värde.
- Verifierat live mot officiell källa: 2022=6,1 · 2023=17 · 2024=25 · 2025=40 mdr kr. Monoton upp.
- Byggt som transkriberad config (`config/ukraina_stod.yaml`) + ny `regeringen`-sektorsadapter; 2026-2027
  (beslutad framåtram) exkluderas. **Öppnade submåttet nato_ukraina** → försvarets D vilar nu på 2
  submått (militär förmåga + Ukraina), inte 1.
- Betygseffekt: S/forsvar +0,031, L/forsvar +0,019; M/KD/SD oförändrade (redan vid taket via
  varnpliktiga, Ukraina också upp på deras vakt); MP/C/V NA (inget 2022-2025-regeringsansvar). Ranking
  oförändrad. Hela sviten grön.

**🟡 SIGN-OFF: `materiel_formaga`** (submått militar_formaga, up) — proxyfråga.
- Officiella årsserier finns men är **pengar/intentions-proxy**, ej förmåga: FMV leveransindex (2021-25:
  79→98→73→73→53, riktning tvetydig — faller för att beställningarna ökat snabbare än industrin hinner),
  FMV beställningar (19→36→52→68→90 mdr, intention ej utfall), FMV leveranser SEK till FM (2023=8,8 ·
  2024=11,5 · 2025=18 mdr, mest utfallsnära), försvarsanslag UO6 (49→…→148 mdr, 2018-2025).
- Caveat "Försvar ska inte mätas bara i pengar" (categories.yaml) gör detta till ett **designbeslut**:
  bygga FMV-leveranser (mdr levererat materiel) som v0-proxy, eller hålla väggen? **Väntar din sign-off.**

**🔴 VÄGG (bekräftad via PDF-läsning): `civil_beredskap_niva`** (submått civil_beredskap, up).
- Läste MSB ÅR 2022 (450k tecken) + 2025 (320k) direkt med pdfplumber. Civilförsvarsinnehållet är
  **narrativt**; de enda konsekventa årliga TALEN är **pengar/anslag** (ersättning till kommuner/regioner
  för civilt försvar 160/100/100 mnkr; bidrag till frivilliga försvarsorganisationer; övnings-anslag) —
  ej ett neutralt UTFALLSmått. Antal övningar/utbildade/deltagare redovisas i växlande format år för år
  (ingen jämförbar konsekutiv serie). **Bekräftar allowlist-skälet "qualitative: MSB-bedömning, ingen
  kvantitativ årsserie" — nu verifierat genom att faktiskt läsa PDF:erna, inte antaget.** Enda byggbara
  vore en anslags-/pengaserie → samma "ej bara pengar"-caveat som materiel → sign-off.

**🔴 VÄGG (bekräftad): `nato_interoperabilitet`** (ingen öppen svensk mätserie; NATO-bedömningar
hemliga) · **`leveranstid_materiel`** (FMV publicerar ingen snitt-ledtidsserie; leveransindex är närmaste
men sekretess/tvetydig).

**Nya kandidater (skulle kräva ny kanonisk indikator, B-grön-mandatet tillåter v0):** `fm_personalstyrka`
(FM antal anställda, FM ÅR, ~2019-2025, PDF — 2025=30 442), `fm_hemvarnssoldater` (FM ÅR; 2024=22 274,
2025=23 069), `fm_officersutbildade` (FHS/FM ÅR, sign-off). Alla i militar_formaga (djup, ej bredd) →
lägre prio än nato_ukraina/civil_beredskap som ger nya submått.

**Försvar-läge:** 1 → **2 byggda** (varnpliktiga + ukraina_stod, två olika submått). Realistiskt 3 om
civil_beredskap-PDF ger en ren serie; 4 kräver materiel-proxy-sign-off. Detta adresserar direkt din
scenariokritik (Ukraina + civil beredskap är nu separata mätpunkter, inte bara värnpliktsantal).

---

### KLIMAT (3 → mål 4)

**🟡 BYGGBAR men kräver ny adapter + sign-off: `elprisvolatilitet`** (submått energi_elpriser, down).
- Källa: SCB EN0301 (elpriser). En årlig CoV (std/medel av MÅNADSpriser) = volatilitet, finns i SCB:s
  `SSDManadElhandelpris` (månads rörligt pris) 2013-2026. **Löser §5.4 gynnsamt:** SCB EN0301 ÄR en
  officiell svensk serie (SCB är producent), så vi behöver inte Nord Pool direkt.
- **HINDER (verifierat):** repo:ts SCB-adapter talar bara v2beta (TAB-id), och v2beta exponerar bara
  HALVÅRSpriser (TAB4310, 2014H2-2025H2) — 2 punkter/år räcker inte för en meningsfull CoV. Månadspriset
  ligger i SCB:s **klassiska PxWeb (v1)** som adaptern inte talar. → kräver en ny klassisk-PxWeb-adapter +
  en ny derived-op "cov" (mer än ett v0-nattbygge). **Rekommenderas som uppföljning** + din §5.4-sign-off
  (räknas SCB EN0301 som tillräckligt officiell trots Nord Pool-underliggande spotpris?). EJ byggt i natt.
- *(Klimat ligger redan på 3 = "OK" enligt din tröskel, så detta är "helst-4", ej blockerande.)*

**🟡 BYGGBAR men STÖKIG: `effektbrist`** (energi_elpriser, down) — SVK Kraftbalansen.
- Svenska kraftnät publicerar effektbalans (normalvinter) årligen, men i PDF/pressmeddelanden med **glapp**
  (saknar 2019/2021/2023 i pressfynd) och **definitionsbyte** (prognos vs utfall). Glapp bryter konsekutiv-
  års-attributionen. Kan ev. extraheras rent ur SVK ÅR-PDF:erna (PDF-pipelinen funkar) — men lägre prio
  eftersom elprisvolatilitet täcker samma submått rent. Dokumenterad; ej byggd.

**🟡 SIGN-OFF: `hotade_arter_naturforlust`** (submått biologisk_mangfald, riktning **down**) — riktnings-/
neutralitetsfråga.
- Rödlistan (SLU) är **kvinkennial** → oduglig (samma som cancer-överlevnad). Officiella ÅRLIGA alternativ
  finns men har **riktning up** (mismatch mot canonical down) + semantik/neutralitet:
  (a) SCB MI0603 "skyddad natur" %, 2014-2025, **maskinläsbar PxWeb** — men mäter policy-INSATS
  (avsatt areal), ej ekologiskt utfall, och "mer skyddat=bättre" har skogsnärings-trade-off (neutralitet).
  (b) Svensk Fågeltaxering "häckande fåglar"-index (Lund/Naturvårdsverket, Sveriges miljömål-indikator),
  2002-2024 — äkta biodiversitetsutfall, men manuell CSV + riktning up.
- **Öppnar nytt submått (biologisk_mangfald, D-tomt) = hög bredd** men kräver ditt beslut: redefiniera
  hotade_arter:s riktning, eller lägg ny kanonisk indikator (`skyddad_natur` up / `faglar_index` up)?
  Neutralitetskänsligt → **väntar sign-off** (auto-bygger ej en värdeladdad riktning).

**🟡 NEEDS-DESIGN: `utslappsminskning_per_krona`** (kostnadseffektivitet, up) — §5.5 kvarstår.
- Täljaren (SCB MI0107 årlig växthusgasförändring) är maskinläsbar; **nämnaren "klimatutgift" saknar ren
  officiell årsserie** (UO20 blandar klimat/natur/SMHI; ESV har ej UO20-API). Metodiskt omtvistad → sign-off.

**Klimat-läge:** 3 → **4 efter elprisvolatilitet** (byggs). hotade_arter ger bredd (nytt submått) men är
sign-off.

---

### DEMOKRATI (1 → mål 4) — svårast; mestadels vägg eller riktnings-tvetydigt

**🔴 VÄGG (bekräftad): `mediefrihet`** (yttrandefrihet_medier, up).
- RSF förbjudet (internationellt). Ingen officiell svensk ÅRLIG kvantitativ mediefrihetsserie: Medie-
  myndighetens mediestöd mäter subventionsfördelning (ej frihet) + systembrott 2024; JK publicerar ingen
  årstabell över tryckfrihetsmål; Brå spårar ej "hot mot journalister" som egen årlig brottskategori.
  **Kategorins enda kvantitativa mått är förbjudna internationella index.**

**🟡 NEEDS-DESIGN (riktning tvetydig): `korruption`** (korruption_tillit, down).
- Brå SOL "anmälda mutbrott" finns per år (2013-2025) men bara via interaktiv SOL-export (ej API).
  **Riktning inneboende tvetydig:** fler anmälda = mer korruption ELLER bättre upptäckt. Kan byggas v0
  med tydlig ambiguitets-flagga, men det bryter mot D:s teckenlogik (en uppgång är inte entydigt sämre).
  Statskontorets korruptionsrapporter: vart ~10:e år (ej årlig) → vägg.

**🟡 NEEDS-DESIGN (endogent): `politisk_transparens`** (transparens_ansvar, up).
- Riksrevisionen antal granskningsrapporter/år (2018-2025: 35,39,30,31,29,27,25,36) — konsekutiv men
  mäter revisorns egen output, ej regeringens transparens. Bättre kandidat: Riksrevisionens **avvikande
  revisionsberättelser/år** (färre=bättre regelefterlevnad, riktning down) — kräver PDF-extraktion ur
  Riksrevisorns årliga rapport. JO inkomna klagomål/år: tvetydig riktning. Alla sign-off.

**🟡 NEEDS-DESIGN: `overvakning_utan_rattssakerhet`** (personlig_frihet, down) — IMY sanktionsavgifter/år
(2019-2025: 2,10,5,3,9,6,3) konsekutiv men mäter IMY:s tillsynsaktivitet, ej kränkningsnivå; riktning
tvetydig. **`otillborlig_politisering`**: SIN publicerar tillsynsvolym, ej "konstaterade olagligheter/år"
→ vägg.

**Demokrati-läge:** 1 → sannolikt **kvar på 1** byggd (fortroende_domstolar). Honest slutsats (din egen
regel "2 → funderare"): demokratins aspekter saknar i stort sett *neutrala officiella årsserier* — det som
finns är antingen förbjudna internationella index (mediefrihet/korruption-CPI) eller riktnings-tvetydiga
aktivitetsmått (anmälningar/sanktioner/granskningar). Detta är en **genuin mätbarhetsgräns**, inte lättja.
Se §3 för funderaren.

---

## 3. Sammanfattning för morgonen

### Per kategori, före → efter (mot din tröskel 4 helst / 3 OK / 2 = funderare)

| Kategori | Före | Efter | Mot tröskel | Vad hände |
|----------|:---:|:---:|---|---|
| Ekonomi | 6 | 6 | ✅ | (redan klar) |
| **Välfärd** | 3 | **4** | ✅ **mål nått** | byggde `overlevnad_svar_sjukdom` (Kolada U70471) |
| Trygghet | 5 | 5 | ✅ | (redan klar) |
| Integration | 5 | 5 | ✅ | (redan klar) |
| Klimat | 3 | 3 | ✅ OK | `elprisvolatilitet` byggbar men kräver ny adapter + §5.4-sign-off |
| **Försvar** | 1 | **2** | ⚠ funderare→nära OK | byggde `ukraina_stod`; 3:e kräver sign-off |
| **Demokrati** | 1 | 1 | ⚠ funderare | äkta mätbarhetsvägg (se nedan) |

**Byggt + committat i natt (allt v0, flaggat):**
1. `ukraina_stod` (`05dc3b3`) — försvar 1→2, öppnade submåttet nato_ukraina.
2. `personal_varnpliktiga` PDF-verifierad (`23b9215`, `7e1bf58`) — 2 värden korrigerade, exakt PDF-källa,
   inga betygsändringar. v1-redo.
3. `overlevnad_svar_sjukdom` (`65a5eda`) — välfärd 3→4.

Ranking genom hela natten **OFÖRÄNDRAD**: S > L > M > KD > MP > C > SD > V. Hela testsviten grön (185 tester).

### Funderaren du bad om (kategorier som fastnar på ≤2)

**Försvar (2) — egentligen "2 ärliga aspekter", inte "tunt".** De två byggda D-serierna ligger i OLIKA
submått: militär förmåga (`personal_varnpliktiga`) + Nato/Ukraina (`ukraina_stod`). Det adresserar
*direkt* din scenariokritik — Ukraina-stöd är nu en egen mätpunkt. De återstående aspekterna är genuint
icke-mätbara med neutral officiell årsdata (verifierat i natt, ej antaget): **materiel** = sekretess/operativ
förmåga; **civil beredskap** = läste MSB ÅR-PDF:erna, bara pengar/anslag finns (ej utfall); **Nato-
interoperabilitet/leveranstid** = inga öppna serier. Att nå 3-4 kräver antingen **pengaproxyer** (FMV-
leveranser/anslag — bryter mot caveat "Försvar ska inte mätas bara i pengar") eller **att stapla fler
personalmått** i militar_formaga (`fm_hemvarnssoldater`/`fm_personalstyrka` — rena & neutrala, men ger
*ingen ny aspekt-bredd*, bara högre siffra). **Min rekommendation:** håll försvar ärligt på 2 aspekt-
täckande serier och låt `d_coverage_krympning_spec` dämpa överskattningen — hellre det än att padda siffran.

**Demokrati (1) — äkta mätbarhetsvägg.** Kategorins standardmått är *förbjudna* internationella index
(TI CPI, RSF). De officiella svenska alternativen är **riktnings-tvetydiga aktivitetsmått** (anmälda
mutbrott, IMY-sanktioner, Riksrevisionsrapporter, JO-klagomål) där en uppgång lika gärna betyder "bättre
upptäckt/mer engagemang" som "sämre tillstånd" — vilket bryter mot D:s teckenlogik. Den enda rena är den
redan byggda `fortroende_domstolar_myndigheter` (institutionstillit, ett äkta utfall). **Demokrati-D vilar
alltså ärligt på 1 av 5 submått.** Detta är det *starkaste empiriska argumentet för din
`d_coverage_krympning_spec`:** demokratins D bör krympas mot neutral eftersom den bara speglar en femtedel
av kategorin — annars hävdar appen "god demokratieffekt" på tunt underlag (exakt din magstarkt-kritik).

### Öppna sign-off-frågor (inget byggt utan ditt ja)

1. **Försvar 3:e D:** (a) `fm_hemvarnssoldater`/`fm_personalstyrka` (ren FM ÅR-årsserie, men militar_formaga-
   djup) · (b) `materiel_formaga` via FMV-leveranser SEK (pengaproxy, mot caveat) · (c) **behåll 2 + krymp
   (rek.)**. 
2. **Klimat 4:e D:** bygga `elprisvolatilitet` (ny klassisk-PxWeb-adapter + ny "cov"-op) — och godkänner du
   SCB EN0301 som "officiell svensk" trots Nord Pool-underliggande spotpris (§5.4)?
3. **Välfärd bredd:** bygga `N72837 höftfraktur` för att öppna det D-tomma omsorg-submåttet? (ren Kolada, neutral).
4. **`hotade_arter`/biologisk mångfald:** SCB MI0603 skyddad natur (up) eller Svensk Fågeltaxering (up) —
   kräver att hotade_arter:s riktning omdefinieras *eller* ny kanonisk indikator; neutralitet (skogsnäring) (§klimat).
5. **Demokrati:** acceptera 1 + krympning, eller bygga ett riktnings-flaggat v0 (mutbrott/Riksrevisionen) trots tvetydigheten?
6. **`personal_varnpliktiga` v0 → v1?** (nu PDF-exakt; 2019 enda mjuka punkt).

### Sammanfattande slutsats

Den billiga rena-API-vågen var redan skördad; i natt plockades de två kvarvarande *rena* vinsterna
(välfärd-överlevnad + försvars-Ukraina) plus en PDF-verifiering. **4 av 7 kategorier ligger nu på ≥4, en
på 4, en på 3 (OK).** De två som fastnar (försvar 2, demokrati 1) gör det av *äkta* skäl — sekretess och
avsaknad av neutrala officiella årsserier, inte av lättja — vilket i sig validerar att vi behöver
coverage-krympningen i `d_coverage_krympning_spec` snarare än att tvinga fram tunna mått.
