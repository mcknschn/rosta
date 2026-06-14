# B3 — kandidatregister (omstridda ∧ evidensbelagda åtgärdstyper, 2026-06-12)

> **✅ UPPDATERING 2026-06-14:** de tre byggda posterna (C1 `nedtrappad_ersattningsprofil_akassa`,
> C2 `dca_avtal_usa`, C3 `uppsokande_forskoleerbjudande_nyanlandas_barn`) är **slutgranskade v0→v1
> och avflaggade**; C4 (`rattssakerhetsgarantier_preventiva_tvangsmedel`, beslutsfråga B2) = **HOLD/vänta**.
> Statustexterna nedan ("flaggad v0" / "Väntar sign-off") är historik från 2026-06-12.
>
> **Status:** research genomförd **2026-06-12** med 7 parallella kategoriagenter (läs-bara; alla
> voteringar API-verifierade live mot data.riksdagen.se — dokumentlista → dokumentstatus →
> votering/voteringlista, partifördelningar hämtade per ledamot aggregerat). Därefter
> **Codex-triage 2026-06-12** av de fyra STRONG-kandidaterna med utfall:
>
> | # | Kandidat | Codex-verdikt | Utfall |
> |---|----------|---------------|--------|
> | C1 | `nedtrappad_ersattningsprofil_akassa` (ekonomi) | **BUILD-WITH-CHANGES** | **Byggd i kväll**, flaggad v0 |
> | C2 | `dca_avtal_usa` (forsvar) | **HOLD** | **BYGGD 2026-06-12** efter användar-sign-off (beslutsfråga B1 = **JA**, med Codex-villkoren: anti-stacknings-not + p1-källkonstruktion via beslutsnotis/följdvoteringar + stance-confidence max medium), flaggad v0. Se §9.1. |
> | C3 | `uppsokande_forskoleerbjudande_nyanlandas_barn` (integration) | **BUILD-WITH-CHANGES** | **Byggd i kväll**, flaggad v0; **SD/KD = none** per aktualitetsprejudikatet (MP/Nato) |
> | C4 | `rattssakerhetsgarantier_preventiva_tvangsmedel` (demokrati) | **HOLD** | Väntar sign-off — S-kodningen kräver instrumentlåsning + panel; andra rättssäkerhetsposten i `personlig_frihet` = stackning. Se beslutsfråga B2 nedan. |
>
> Detta dokument bevarar **hela** researchen (inkl. WEAK/REJECT och rejected-candidate-loggarna)
> som granskningsbart register, efter samma mönster som
> [done/fas4c_planA_kandidatregister.md](fas4c_planA_kandidatregister.md): inget fynd får gå
> förlorat, och en människa ska kunna granska, ompröva eller återuppta varje spår. Voterings-id:n,
> betänkandenummer, partifördelningar och källcitat är bevarade exakt som agenterna levererade dem.

Legend för **verdikt (research)**: `STRONG` = uppfyller omstridd ∧ evidensbelagd ∧ neutral → till
Codex-triage · `WEAK` = nära men fäller på en grind, dokumenteras för bevakning · `REJECT` =
granskad och förkastad med skäl (kvar i loggen för återöppning).

---

## 1. Sammanfattningstabell

| Kandidat | Kategori → indikator | Verdikt (research) | Codex-verdikt | Status |
|---|---|---|---|---|
| `nedtrappad_ersattningsprofil_akassa` | ekonomi → `arbetsloshet` | STRONG | BUILD-WITH-CHANGES | **Byggd 2026-06-12, v0→v1 avflaggad 2026-06-14** |
| `dca_avtal_usa` | forsvar → `nato_interoperabilitet` | STRONG | HOLD | **Sign-off 2026-06-12: BYGG med Codex-villkoren — BYGGD 2026-06-12, v0→v1 avflaggad 2026-06-14 (se §9.1; commit `data: B3 — dca_avtal_usa …`)** |
| `uppsokande_forskoleerbjudande_nyanlandas_barn` | integration → `skolresultat_utsatta_omraden` | STRONG | BUILD-WITH-CHANGES | **Byggd 2026-06-12, v0→v1 avflaggad 2026-06-14; SD/KD = none** |
| `rattssakerhetsgarantier_preventiva_tvangsmedel` | demokrati → `overvakning_utan_rattssakerhet` | STRONG | HOLD | **Sign-off 2026-06-12: HOLD bekräftad — vänta (kandidaten kvar färdigberedd)** |
| `likvardiga_urvalsgrunder_skolval` | valfard → `skillnader_mellan_skolor` | WEAK | — | Bevakning (Tidö-utredningen, IFAU-remiss 2025-11-28) |
| `karriarsteg_forstelarare` | valfard → `skolresultat` | WEAK | — | Bevakning (uppgraderas till trolig STRONG om V:s avskaffa-yrkande voteras) |
| `sakerhetszoner_visitationszoner` | trygghet → `skjutningar_sprangningar` | REJECT | — | Återöppningstrigger: lagstadgad utvärdering ~2027 |
| `anonyma_vittnen` | trygghet → `uppklaringsgrad` | REJECT | — | Återöppningstrigger: framtida Brå-/myndighetsutvärdering |
| `drivmedelsskatt_energiskatt_bensin_diesel` | klimat → `territoriella_utslapp` | REJECT | — | Stängd (dubbelräkning + blockspegling) |
| `slopad_flygskatt` | klimat → `konsumtionsbaserade_utslapp` | REJECT | — | Stängd (budgetspegling + proxy-evidens) |

**Kategorier utan kandidat:** trygghet och klimat levererade 0 STRONG — i båda fallen ett legitimt
utfall per rubriken §8 (inget täckningsmål; B tiger hellre än gissar). Valfärds slutsats: de två
starkaste fallerar på varsin spegelvänd grind (skolval: stark votering/tunn evidens + tilt;
karriärsteg: stark IFAU-evidens/ingen votering) → bygg inget nu.

---

## 2. Ekonomi

### 2.1 `nedtrappad_ersattningsprofil_akassa` → `arbetsloshet` (sysselsattning_arbetsloshet) — **STRONG** → byggd v0

- **Contested (steg 2):** bet. 2023/24:AU9 punkt 1 "Regeringens lagförslag" (anta prop. 2023/24:128
  "En arbetslöshetsförsäkring baserad på inkomster"), kammaren 2024-06-18, votering-id
  `20D6BDDC-B9AC-47E8-B286-48CF613D7276` (verifierad via data.riksdagen.se/votering): **283 Ja / 20 Nej**.
  Per parti: S 93 Ja, M 60 Ja, SD 63 Ja, C 21 Ja, KD 16 Ja, L 13 Ja, MP 15 Ja — **V 20 Nej**
  (kommittémotion 2023/24:2881 yrk. 1 = avslag på propositionen; V:s reservation kräver i stället
  "höja ersättningsnivån till 80 procent för hela ersättningsperioden" = instrument-exakt opposition
  mot nedtrappningen). INTE regeringsläges-artefakt: S, MP och C röstade MED regeringen på p1;
  splittringen speglar instrumentet. Kompletterande differentiering finns i p2 "Arbetslöshetsförsäkringens
  framtida utformning" (votering `B74D499B-48C6-4AEF-BF4F-8E3FDB965234`: S Nej 93, C/V/MP avstår,
  M/SD/KD/L Ja) — användbar för mapping_note-nyans (S/MP accepterade lagen men vill höja nivåer framåt).
  7-1-mönstret har prejudikat i liggaren: `fou_avdrag_skatteincitament` (bet. 2022/23:SfU19, 7 supports / V opposes).
- **Effektevidens (steg 1):** IFAU (officiellt svenskt forskningsinstitut under
  Arbetsmarknadsdepartementet), forskningssammanfattning "Om a-kassa och löner"
  (https://www.ifau.se/Press/Forskningssammanfattningar/Om-a-kassa-och-loner-/, live-verifierad
  2026-06-12), som syntetiserar flera IFAU-rapporter: (1) Fredriksson & Söderström R 2008:12 — höjd
  ersättningsnivå 80→85 % "medförde att arbetslösheten steg förhållandevis mycket, med 1,5 procentenheter"
  = EXAKT indikatorn `arbetsloshet` (nivå, ej bara arbetslöshetstid — ingen §5.3-proxybrygga behövs,
  men IFAU-beräkningen är kontrafaktisk simulering på skattade samband, ska noteras);
  (2) Uusitalo & Verho WP 2007:21 — högre ersättning första 150 dagarna minskade
  anställningssannolikheten ~20 % och "effekten försvann efter 150 dagar då den högre ersättningen
  togs bort" = direkt mekanismbelägg för just NEDTRAPPNINGSPROFILEN; (3) Bennmarker m.fl. R 2013:10 —
  "en mindre generös a-kassa håller tillbaks löneökningarna vilket i sin tur förmodligen påverkar
  sysselsättningen positivt"; (4) Bennmarker m.fl. R 2005:16 — höjd ersättning 2001–02 gav längre
  arbetslöshetstider för män (men EJ kvinnor — heterogenitet, motiverar confidence medium). Rubrik på
  sidan: "A-kassan påverkar lönebildningen och arbetslösheten". Förslag:
  evidence_level=authority_evaluation (IFAU-syntes av flera egna kausalstudier; ej formell systematic
  review), effect_strength=medium, confidence=medium (heterogenitet kön/grupper; magnitud delvis
  simuleringsbaserad; nedtrappningskomponenten belagd via finsk kvasiexperimentell variation + svensk
  nivåvariation, ej en utvärdering av 2025 års lag i sig).
- **Riktning:** positiv — instrumentet (nedtrappad ersättningsprofil/arbetslinje-utformning) rör
  `arbetsloshet` (down-indikator) åt rätt håll enligt IFAU-evidensen; negativ-riktnings-grinden (§5)
  är därmed inte direkt tillämplig på posten. OBS: V:s opposes vänds via _FLIP till negativt
  B-bidrag — samma konstruktion som `ny_karnkraft` (prejudikat: flaggad för mänsklig granskning) och
  `fou_avdrag` (V opposes). Skulle posten i stället formuleras som "höjd a-kassa → negative på
  arbetsloshet" måste §5-grinden prövas: authority_evaluation JA, confidence medium JA, exakt
  indikator JA (R 2008:12 mäter arbetslöshetsNIVÅN, inte bara tid) — den klarar grinden, men
  positiv-formuleringen är att föredra (mindre laddad, samma information).
- **Neutralitet (risker, ärligt redovisade):** (1) Vänster-höger-tilt: "mindre generös försäkring →
  lägre arbetslöshet" belönar arbetslinjen — MEN tilten mildras kraftigt av att S och MP röstade JA
  på lagen (V ensamt opposes; splittringen är inte blockaxeln), av att IFAU-sammanfattningen själv
  balanserar (a-kassans försäkringsvärde och matchningsnytta redovisas i samma text — instrumentet är
  PROFILEN nedtrappning, inte "lägre ersättning alltid bättre"), och av att liggaren redan har
  spegelposter åt andra hållet (`inkomststarkande_hushallspolitik` kodar höjda transfereringar
  positivt). (2) Dubbelräkning: INGEN — indikatorn `arbetsloshet` har idag noll liggarposter;
  undermåttets befintliga poster (arbetsmarknadsutbildning, subventionerade_anstallningar →
  sysselsattning) är andra instrumentfamiljer (program vs försäkringsdesign); jobbskatteavdrag är
  separat instrument och inert (unclear). (3) Sidoeffekt-proxy: NEJ — R 2008:12 avser
  arbetslöshetsnivån direkt; tid-/lönekanalerna är stödjande mekanismer, inte bärande brygga.
  (4) Acklamation: NEJ — rösträknad votering med verklig splittring. (5) Instrument-exakthet
  stance-sidan: V-citatet ("80 procent för hela ersättningsperioden") är direkt mot
  nedtrappningsprofilen; 7 Ja-partier band sig till lagen som innehåller den — mapping_note bör
  notera att S/MP/C samtidigt vill höja nivåer/tak framåt (p2-reservationer) utan att det ändrar
  stance på instrumentet (bunten-regeln §2).
- **Partifördelning (preliminär):** supports = S, M, SD, C, KD, L, MP (Ja på AU9 p1, lag med
  nedtrappning); opposes = V (Nej + avslagsreservation med citat mot nedtrappningen). Nyans för
  mapping_note: S (p2-reservation, vill höja tak/ersättningsgrad framåt), MP (Ja p1 men egen
  reservationssvit p2–p4), C (Ja p1, egen p2-reservation om framtida utformning) — alla förenliga
  med supports på instrumentet enligt bunten-regeln.

### 2.2 Rejected-candidate-logg (ekonomi)

Sökstrategi: ekonomins B-bara indikatorer kartlagda mot befintliga liggarposter — tunnast var
`arbetsloshet` (noll poster) och differentieringen i `realloner_hushall`
(`inkomststarkande_hushallspolitik` = alla 8 supports). Allt verifierat live, inget gissat:

1. **RUT-avdrag → sysselsattning:** RiR 2020:2 "Rutavdraget – konsekvenser av reformen" är BLANDAD
   på aggregatnivå ("svagt empiriskt stöd" för självfinansiering; effekter endast för vissa grupper;
   RiR rekommenderar att "se över ... långsiktiga effekter på sysselsättningen") → skulle kodas
   mixed/unclear = inert; dessutom togs rut/rot-punkten (p4) i bet. 2024/25:SkU9 i ACKLAMATION
   (verifierat via dokumentstatus) → faller på omstridd-grinden.
2. **ROT-avdrag** (tillfälligt höjt tak, bet. 2023/24:SkU24; RiR-rapporten "Svart på vitt –
   rotavdragets kostnader och effekter", bet. 2023/24:SkU28): RiR:s slutsats är svaga effekter/hög
   kostnad → unclear/inert på sysselsattning; kostnadseffektivitet är ingen ekonomi-indikator.
3. **Sänkta arbetsgivaravgifter för unga → sysselsattning:** IFAU-forskningssammanfattning finns
   ("om sänkta arbetsgivaravgifter för ungdomar", Egebark & Kaunitz: små effekter, hög kostnad per
   jobb) men senaste instrument-exakta voteringen är avskaffandet 2014/15 (utanför föredragen
   mandatperiod) och dagens partiläge på instrumentet är inaktuellt/odifferentierat → WEAK, ej levererad.
4. **Specifika skattesänkningar → hushallens_reala_disponibla_inkomst:** dubbelräknar per
   konstruktion familjeposten `inkomststarkande_hushallspolitik` i samma undermått → REJECT by design.
5. **Jobbskatteavdrag:** finns redan i liggaren som unclear/inert (IFAU: ej utvärderingsbart) — ny
   votering ändrar inte evidensläget.
6. **Regelförenkling → produktivitet** (Produktivitetskommissionen SOU 2025:96): instrumentvagt
   ("förenkla" stöds retoriskt av alla), NU-betänkandenas voteringar är regeringsläges-artefakter → REJECT.
7. **Infrastrukturinvesteringar → produktivitet:** projektspecifikt, samhällsekonomisk lönsamhet ≠
   produktivitetsindikatorn (proxy) → REJECT.
8. **Aktivitetskrav försörjningsstöd** (bet. 2025/26:SoU29): instrumentet finns redan som
   `aktiveringskrav_ekonomiskt_bistand` i integration — att räkna samma IFAU-Stockholmsutvärdering
   igen i ekonomi vore dubbelräkning av samma evidens.

Leverans: 1 STRONG i stället för 3 WEAK, per uppdragsinstruktionen och §8 (inget täckningsmål).
STRONG-kandidatens alla voteringsuppgifter är API-verifierade (dokumentlista → dokumentstatus →
votering, per ledamot aggregerat); IFAU-citaten är hämtade ur sidkällan 2026-06-12.

---

## 3. Välfärd

### 3.1 `likvardiga_urvalsgrunder_skolval` → `skillnader_mellan_skolor` (skola_kunskap) — **WEAK**

- **Contested (steg 2):** bet. 2021/22:UbU33 "Ett mer likvärdigt skolval" (prop. 2021/22:158),
  punkt 2 "Lagförslaget i övrigt" (= avslag på regeringens urvalsgrunds-/skolvalsförslag), VOTERING
  2022-06-09, votering_id `5CEAB1C8-AA59-4A2A-8CC3-CF43C1471346` (verifierad live mot
  data.riksdagen.se/voteringlista): Ja (bifall utskottets AVSLAG) M 57, SD 51, C 26, KD 17, L 16 = 167;
  Nej (ville anta lagförslaget) S 84, V 22, MP 11 = 118. Även punkt 3 (tillkännagivande om ett nytt
  "utvecklat skolval") röstades 169-118 med samma mönster. Punkt 1 (resursskolor) togs däremot i
  acklamation och antogs — den delen är konsensus och ingår INTE i instrumentet. Splittringen är
  instrument-äkta i sak (för/emot reglerade urvalsgrunder i skolvalet är en bestående konfliktlinje,
  C stod utanför regeringssamarbetet) MEN är block-formad (S-regering vs M/SD/C/KD/L våren 2022) och
  ligger strax FÖRE föredragen mandatperiod (2021/22, ej 2022/23–2025/26).
- **Effektevidens (steg 1):** kedja i tre led, alla officiella: (1) SOU 2020:28 "En mer likvärdig
  skola – minskad skolsegregation och förbättrad resurstilldelning" (Åstrand-utredningen) —
  designevidens: kötid som urvalsgrund gynnar resursstarka; föreslagna urvalsgrunder (syskonförtur,
  geografi, kvot, lika möjligheter; kötid otillåten) + skyldighet att verka för allsidig social
  sammansättning syftar till minskad skolsegregation. (2) IFAU remissvar dnr 111/2020: IFAU bedömer
  utredningen "väl genomförd", slutsatserna väl underbyggda, och TILLSTYRKER de nya urvalsgrunderna
  samt kravet på allsidig social sammansättning (myndighets-endorsement av instrumentet).
  (3) IFAU Rapport 2015:5 "Skolsegregation och skolval" (Böhlmark/Holmlund/Lindahl): mer skolval ↔
  ökad skolsegregation utöver boendesegregation — men boendesegregationen är den klart största
  faktorn. Indikator-BRYGGA krävs: evidensen avser SKOLSEGREGATION (elevsammansättning), inte den
  betygsatta indikatorn `skillnader_mellan_skolor` (resultatskillnader) — bryggan (Skolverket 2018,
  sortering driver mellanskolvariation) är beskrivande, ej kausal för instrumentet. Förslag:
  evidence_level authority_evaluation, confidence LOW (designnivå, aldrig implementerat → ingen
  ex-post; magnitud liten enligt IFAU 2015:5).
- **Riktning:** positiv (instrumentet driver `skillnader_mellan_skolor` NEDÅT = rätt håll) —
  negativ-riktnings-grinden (§5) är formellt ej tillämplig. MEN: via stance-flip skulle M/SD/C/KD/L
  (5 partier) få NEGATIVT B-bidrag på 30 % av kategorivikten, på enbart design-/mekanismevidens med
  osäker indikator-brygga — det är i praktiken den laddade situation grinden finns för, och kedjan
  klarar INTE grindens anda (confidence låg + brygga håller ej kausalt).
- **Neutralitet:** BETYDANDE RISK. (1) Vänster-höger-tilt: instrumentfamiljen "reglera skolvalets
  urvalsgrunder" är vänsterblockets metod; opposes-sidans motiv är valfrihet/förutsebarhet
  (värdekonflikt) — med tunn riktad evidens på själva RESULTAT-indikatorn hamnar detta i
  §6-territorium (B tiger hellre än gissar). (2) Magnituden: IFAU 2015:5 visar att boendesegregation
  dominerar → instrumentets effekt på resultatskillnader sannolikt liten → "mixed/low" → inert-risk.
  (3) Ingen dubbelräkning: `skillnader_mellan_skolor` är B-tom; `riktat_likvardighetsbidrag`
  (unclear/inert) avser resurstilldelning, ej urval — distinkt. (4) Ej sidoeffekt-proxy i strikt
  mening, men brygga sammansättning→resultatskillnader är obelagd för instrumentet. (5) Pågående
  rörelse: Tidö-utredningen "Verktyg för en mer likvärdig resursfördelning till skolan" (IFAU-remiss
  2025-11-28) kan ge ett nytt, mindre block-format ankare framöver — bevakningsvärde.
- **Partifördelning (preliminär):** supports: S, V, MP (röstade Nej till avslaget = för
  instrumentet); opposes: M, SD, C, KD, L (röstade Ja till avslag). 5-3 block-split.

### 3.2 `karriarsteg_forstelarare` → `skolresultat` (skola_kunskap) — **WEAK**

- **Contested (steg 2):** FALLERAR voterings-grinden — detta är kandidatens enda men avgörande
  brist. Verifierat mot data.riksdagen.se/dokumentstatus: kärninstrumentets punkt
  (bet. 2012/13:UbU15 punkt 1 "Karriärvägar för lärare i skolväsendet m.m.", prop. 2012/13:136)
  togs i ACKLAMATION redan 2013; de fyra röstningarna i UbU15 gällde detaljer (ansökningsprocess p3,
  lektorer p6/p7, förskollärare p10). Ingen karriärstegs-votering finns i senare betänkanden
  (kontrollerat: 2022/23:UbU7, 2022/23:UbU13, 2023/24:UbU11 — beslutspunktlista verifierad, ingen
  karriärtjänstpunkt; 2025/26:UbU9 — 0 träffar på karriärsteg/förstelärare). V:s motstånd är dock
  AKTUELLT och instrument-exakt, men bara som särskilt yttrande i bet. 2022/23:UbU13
  (Lorena Delgado Varas, V, ordagrant verifierat ur betänkandetexten): "Jag har varit emot
  förstelärarspåret i karriärstegsreformen sedan dag ett" ... "måste förstelärarsystemet avskaffas
  till förmån för professionsprogrammet." → max 7-1-differentiering via motion/yttrande-stance
  (fou_avdrag-prejudikatet hade till skillnad från detta en riktig votering).
- **Effektevidens (steg 1):** STARKAST TILLGÄNGLIGA i kategorin: IFAU Rapport 2020:3 "Minskar
  lärarrörligheten och förbättras studieresultaten av karriärstegsreformen?" (Grönqvist, Hensvik,
  Thoresson) — kausalt upplagd myndighetsutvärdering av exakt instrumentet (statsbidrag för
  karriärstegen förstelärare/lektor): "deltagande skolor förbättrar sina resultat på nationella
  proven i årskurs 3 och 6 i viss utsträckning" samt lägre personalomsättning ("lägre sannolikhet
  att lärarna byter arbetsplats och ... lämnar läraryrket"); "karriärstegsreformen kan vara ett
  viktigt verktyg för att höja kvaliteten i den svenska skolan". Nationella prov åk 3/6 = exakt
  indikatorn `skolresultat`. Stödkälla: Skolverket Rapport 2023:11 (utvärdering av det samlade
  statsbidraget; bidraget når skolor med svåra förutsättningar). Motkälla att notera: RiR 2017:18
  "Karriärstegsreformen och Lärarlönelyftet – högre lön men sämre sammanhållning" — avser
  sammanhållning/lön, INTE skolresultat (ej riktningsvändande, men nämns för ärlighet). Förslag:
  evidence_level authority_evaluation, effect_strength low-medium ("i viss utsträckning"),
  confidence medium.
- **Riktning:** positiv (karriärsteg driver `skolresultat` UPP) — negativ-grinden ej tillämplig.
  Flip-effekten träffar endast V (opposes) → litet, avgränsat negativt bidrag; samma mönster som
  `fou_avdrag_skatteincitament` (7-1, V).
- **Neutralitet:** instrumentet är metodneutralt (statsbidrag för karriärsteg, infört av Alliansen,
  behållet och utbyggt av S-regeringar — ingen vänster-höger-metodpreferens). Ingen dubbelräkning:
  `kompetensutveckling_larare` (fortbildning) och minskad_klasstorlek/tidiga_insatser är distinkta
  instrument; tre liggarposter på `skolresultat` finns redan som prejudikat. ACKLAMATIONS-RISK är
  huvudproblemet: utan votering vilar omstriddheten helt på V:s yttrande/motioner — om stance kodas
  blir det 7-1 där bara V straffas; det kräver att V:s opposes-källa uppgraderas (kommittémotion med
  avskaffa-yrkande behöver sökas fram för stance-kodning; yttrandet bevisar hållningen men är
  svagare i källhierarkin). MP:s hållning okänd → trolig coverage-lucka.
- **Partifördelning (preliminär):** supports (via prop/förvaltning/motioner): S, M, SD, KD, L,
  troligen C; opposes: V (särskilt yttrande UbU13 2023 + historik sedan 2013); MP: okänd/lucka.

### 3.3 Rejected-candidate-logg (valfard)

SÖKT: alla 4 undermått systematiskt. RESPEKTERADE BEFINTLIGA HOLD (ej om-prövade, per
djupsvep-loggen i docs/done/evidens_trovardighet.md §6/§8.7): vårdgaranti/kömiljard/SVF
(RiR 2023:12 mixed/negativ → riktningsgrind faller), nationell_vardformedling (outvärderad),
vårdplatser (RiR 2026:3 villkor konsumerat), cancerscreening (steg-2-tilt). Nya förkastade denna
körning:

1. **Vinsttak/vinstbegränsning i välfärden** — utmärkt votering finns (bet. 2017/18:FiU44,
   S/V/MP vs M/SD/C/KD/L) men ingen officiell svensk evidens kopplar instrumentet till någon
   kanonisk indikator med riktning (SOU 2016:78 är förslag, remisskritiken massiv, effekt på
   kvalitet/resultat obelagd) → faller på evidensgrinden.
2. **Utbetalningsmyndigheten/transaktionskontroll → valfardsbrottslighet** — dubbelräknar
   `kontroller_och_informationsutbyte_mot_valfardsbrott` (samma mekanism, samma undermått) +
   i praktiken konsensus → REJECT.
3. **Lovskola/extra studietid** (prop. 2021/22:111) — Skolverkets uppföljningar visar små/blandade
   effekter → mixed/inert.
4. **Legitimations-/behörighetskrav → behoriga_larare** — ingen kausal myndighetsutvärdering hittad.
5. **Språkkrav i äldreomsorgen** — kontested men ingen officiell evidens mot
   kontinuitet/kvalitetsindikator.
6. **Fast läkarkontakt primärvård** — ingen kanonisk indikator i kategorin (`kontinuitet_i_omsorgen`
   är hemtjänst-specifik; dubbelräkningsrisk mot fast_omsorgskontakt).
7. **Statligt huvudmannaskap, tioårig grundskola, mobilförbud, tvålärarsystem** —
   design-/utredningsnivå utan instrument-exakt effektevidens eller utan splittring.

VERIFIERINGSARBETE: UbU33-voteringen punkt-för-punkt med partifördelning (votering_id 5CEAB1C8...),
UbU15 2012/13 beslutstyper per punkt (kärnpunkt = acklamation!), UbU13-yttrandet ordagrant ur
betänkande-HTML, UbU11/UbU9 punktlistor (ingen karriärstegspunkt), IFAU 2020:3 huvudresultat,
IFAU remissvar dnr 111/2020.

**Slutsats:** ingen kandidat uppfyller omstridd ∧ evidensbelagd ∧ neutral utan tveksamhet — de två
starkaste fallerar på varsin spegelvänd grind (skolval: stark votering/tunn evidens+tilt;
karriärsteg: stark IFAU-evidens/ingen votering). Per rubriken §8 är luckan ett legitimt utfall;
rekommendation = bygg inget nu. **BEVAKNING:** (a) Tidö-utredningen "Verktyg för en mer likvärdig
resursfördelning till skolan" (IFAU-remiss 2025-11-28) kan ge ett nytt mindre block-format
skolvals-/skolpengsankare; (b) om V:s avskaffa-förstelärare-yrkande går till votering i ett kommande
UbU-betänkande uppgraderas `karriarsteg_forstelarare` till trolig STRONG (evidensen är redan på plats).

---

## 4. Trygghet

### 4.1 `sakerhetszoner_visitationszoner` → `skjutningar_sprangningar` (grov_brottslighet) — **REJECT**

- **Contested (steg 2):** PERFEKT steg 2, API-verifierad: bet. 2023/24:JuU13 punkt 1
  (prop. 2023/24:84 Säkerhetszoner), votering 2024-04-10
  (votering_id `21b819e2-3778-4bf2-ac22-8de4782d7823`, data.riksdagen.se): Ja = M(59) SD(63) KD(14)
  L(14); Nej = S(92) V(21) C(21) MP(13). Äkta 4-4-split som INTE är ren regeringsläges-artefakt:
  alla fyra nej-partier lade egna sakmotioner (S 2023/24:2831, V 2829, MP 2832, C 2833) med
  instrument-specifika invändningar; 8 reservationer i betänkandet.
- **Effektevidens (steg 1):** SAKNAS — detta fäller kandidaten. Lagens egen utvärdering (effekt-,
  likabehandlings- och integritetsperspektiv) inleds först ca 3 år efter ikraftträdande (~2027, per
  prop. 2023/24:84 + Strömmers svar på skriftlig fråga 2024/25:222). Polisens interna utvärdering av
  zonen i Norrköping (region Öst) är inte publicerad som citerbar myndighetsprodukt — endast
  medierapporterad (DN: "mycket begränsad påverkan på kriminaliteten"). Brås kritiska remissvar är
  ett remissvar, inte en utvärdering. Ingen admissibel svensk authority_evaluation/systematic_review
  finns i NÅGON riktning på `skjutningar_sprangningar` eller `brottsutsatthet`.
- **Riktning:** okodbar idag — en negativ post (instrumentet verkningslöst/kontraproduktivt) klarar
  INTE negativ-riktnings-grinden (fas4c_rubrik §5: kräver authority_evaluation/systematic_review +
  confidence>=medium + exakt indikator; medieläckt intern polisrapport och remissvar kvalar inte).
  En positiv post saknar källa helt.
- **Neutralitet:** ingen dubbelräkning (distinkt från situationell_prevention_kamerabevakning/
  belysning). Ingen metodpreferens-tilt i sig, men att koda utan riktad evidens vore exakt §6-fallet
  (värdekonflikt utan officiell evidens => B tiger). OBS även latent krock med demokrati-kategorins
  `overvakning_utan_rattssakerhet` om den byggs ensidigt som trygghet-positiv.
  **ÅTERÖPPNINGSTRIGGER:** den lagstadgade utvärderingen ~2027 (utredning eller myndighetsuppdrag) —
  om den ger riktat effektutfall på skjutningar/brottsutsatthet är detta trygghets i särklass bästa
  B3-kandidat (steg 2 redan löst och verifierad).
- **Partifördelning (preliminär):** supports: M, SD, KD, L; opposes: S, V, C, MP (4-4,
  rankningsdrivande åt båda håll — ovanligt välbalanserad split).

### 4.2 `anonyma_vittnen` → `uppklaringsgrad` (rattsvasendets_effektivitet) — **REJECT**

- **Contested (steg 2):** API-verifierad: bet. 2024/25:JuU6 punkt 1 (prop. 2024/25:20 Anonyma
  vittnen), votering 2024-11-21 (votering_id `be21f895-223b-4c1f-9432-f398a8bfa2c3`): Ja = S(92)
  M(59) SD(63) KD(15) L(15); Nej = V(21) C(21) MP(14). Genuint ICKE-block-split (S röstade med
  regeringssidan) => splittringen speglar instrumentet, inte regeringsläget.
- **Effektevidens (steg 1):** FINNS men pekar mot NOLL: SOU 2023:67 "Anonyma vittnen" (officiell
  svensk källa, utredningens egen bedömning) — ett system med anonyma vittnen skulle "endast i
  mycket begränsad utsträckning" bidra till utredning och lagföring av brott; Lagrådet och
  remissmajoriteten avstyrkte. Det officiella underlaget belägger alltså att instrumentets effekt på
  uppklaringsgrad är försumbar => signed_direction = 0 (mixed/unclear) => inert per fas4c_rubrik
  §6/E2. Ingen myndighetsutvärdering med riktad effekt existerar (lagen ikraft 2025-01-01, oprövad).
- **Riktning:** unclear/inert — kan inte kodas positiv (officiella källan säger "mycket begränsad"
  nytta) och en negativ kodning avser rättssäkerhets-sidoeffekter (försvarets möjligheter,
  bevisvärde) = sidoeffekt-proxy utanför trygghets indikatorer, fäller på §5.3/E1.
- **Neutralitet:** splitten är äkta och icke-block, men §6 är entydig: värdekonflikt utan riktad
  officiell evidens kodas inte in i B. Att ändå bygga posten som positiv skulle premiera
  M/SD/KD/L/S på en åtgärd vars eget officiella beslutsunderlag säger nära-noll-effekt — ren
  tilt-risk. Ingen dubbelräkning mot befintliga poster. **ÅTERÖPPNINGSTRIGGER:** framtida
  Brå-/myndighetsutvärdering av lagen (övervaka; ingen aviserad ännu).
- **Partifördelning (preliminär):** supports: S, M, SD, KD, L; opposes: V, C, MP — men inert
  (direction 0) => ingen B-effekt oavsett.

### 4.3 Rejected-candidate-logg (trygghet)

SLUTSATS: 0 STRONG. Intersektionen omstridd ∧ evidensbelagd är idag TOM i trygghet utöver
befintlig liggare — de omstridda instrumenten är för nya för svensk effektutvärdering, och de
utvärderade instrumenten är konsensus eller redan kodade. Detta speglar D-svepets fynd: blockeraren
är attribution/evidens, inte uppslag. Fullständig logg (utöver de 2 dokumenterade kandidaterna):

1. **Preventiva tvångsmedel** (prop. 2022/23:126): votering API-verifierad bet. 2022/23:JuU31 p1
   2023-09-07 (votering `ccd60a0b`) — endast V Nej(19), alla övriga inkl. MP/C Ja => 7-1 ≈ noll
   differentiering (samma skäl som fällde kamera-vägen); enda "evidensen" är
   Åklagarmyndighetens/regeringens årliga nytto-redovisning (skr./bet. JuU25) = statens
   självvärdering av eget verktyg, ej oberoende utvärdering; krockar dessutom med
   demokrati/`overvakning_utan_rattssakerhet` (§8.7-varningen). Preventivlagen tidsbegränsad 5 år =>
   oberoende utvärdering väntas ~2028 = återöppningstrigger.
2. **Fotboja/elektronisk övervakning:** bäst evidens i hela kategorin (Brå 2005 "Effekter av
   utslussning med elektronisk fotboja": 26 % återfall vs 38 % matchad kontroll; Brå 2007:19;
   Brå 2010 "Utökad frigång och återfall") => skulle klara steg 1 som medium — MEN steg 2 faller:
   bet. 2025/26:JuU7 p1 (utökade möjligheter verkställa fängelsestraff med elektronisk övervakning,
   2025-10-22) togs i ACKLAMATION, 0 reservationer (API-verifierat) => konsensus, ej omstridd;
   möjlig framtida §5.2-konsensuspost för `aterfall_i_brott` men det är B2-spår, inte B3, och
   `aterfall_i_brott` har redan 2 liggarposter (dubbelräknings-/mättnadsrisk).
3. **10 000 fler polisanställda:** Brå-utvärdering 2026-03-25 finns (uppklaring grova brott EJ ökat;
   uppklaring ingripandebrott 52→39 %) men instrumentet är konsensus + utfallet no-effect => inert;
   negativ kodning fäller på kompositionsförklaringen (mer narkotikaingripanden) = ej ren
   indikatorbrygga.
4. **Ordningsvakter** (lag 2023:421): evidensen är kommunala utvärderingar i Brås erfarenhetsbank
   med blandat utfall (Stockholms mobila ordningsvakter: ingen mätbar effekt på anmälda brott eller
   generell trygghet) => mixed/inert + ej riksnivå-källa.
5. **Kronvittnen:** redan loggad 🟡 i evidens_trovardighet.md §6 (JuU35 2021/22 utanför tidsfönster,
   fel indikator) — Brå-utvärdering ännu ej publicerad; ej återprövad i sak.
6. **Straffskärpning grovt vapenbrott / skärpta straff kriminella nätverk / slopad ungdomsreduktion
   / skärpt villkorlig frigivning:** inga svenska authority_evaluations med riktad effekt på
   dodligt_vald/skjutningar/aterfall; negativ-kodning (Brå-forskningens "begränsad allmänpreventiv
   effekt") är generellt expertutlåtande, klarar ej §5-grindens krav på exakt indikator +
   utvärderingsnivå.
7. **Vistelseförbud, säkerhetszoner för barn, ansiktsigenkänning/biometri** (SOU 2023:32): oprövade
   instrument utan effektutvärdering; biometri krockar dessutom med befintlig demokrati-post
   `begransa_biometrisk_realtidsovervakning_rattssakerhet`.
8. **Avhopparverksamhet/SIG/MST:** SBU/Socialstyrelsen = otillräckligt vetenskapligt underlag eller
   nolleffekt i svensk RCT => inert; dessutom konsensus.
9. **Trygghetsvärdar:** Brå-erfarenhetsbank-utvärdering 2025 positiv men kommunal nivå — ingen
   riksdagsvotering => steg 2 saknas strukturellt.

**BEVAKNINGSLISTA** (bästa framtida B3-vägar i trygghet, i ordning): säkerhetszons-utvärderingen
~2027 (steg 2 redan löst, 4-4), preventivlagens utvärdering ~2028, Brås kommande
kronvittnes-utvärdering, ev. Brå-utvärdering av anonyma vittnen. Inga filer ändrade (läs-bara
research). Källor: data.riksdagen.se (dokumentstatus + votering-API, alla partifördelningar hämtade
live), bra.se, regeringen.se, riksdagen.se, SOU 2023:67.

---

## 5. Försvar

### 5.1 `dca_avtal_usa` → `nato_interoperabilitet` (nato_ukraina) — **STRONG** → Codex HOLD (beslutsfråga B1)

- **Contested (steg 2):** bet. 2023/24:UFöU1 (sammansatta utrikes- och försvarsutskottet), beslut
  2024-06-18. PUNKT 1 = godkännande av DCA-avtalet + lagändringar (prop. 2023/24:141), kvalificerad
  majoritet (3/4): **266 Ja / 37 Nej / 0 Avstår** — Ja: S 93, SD 63, M 60, C 21, KD 16, L 13;
  Nej: V 20, MP 15 (+2 utan partibeteckning). Partifördelning per riksdagens officiella beslutsnotis
  2024-06-18 (riksdagen.se "Ja till avtal om försvarssamarbete med USA"); **punkt 1-voteringen
  exponeras INTE i voteringlista-API:t** (verifierat @antal=0 för punkt=1), men dokumentstatus
  HB01UFöU1 anger beslutstyp=röstning för p1, och de fyra API-verifierade följdvoteringarna i samma
  bet. bekräftar exakt samma mönster: punkt 5 "Nedrustning" votering
  `A1C914E0-4544-4389-A757-A5BEDDACBFD9` = 266 Ja / 37 Nej (V 20 Nej, MP 15 Nej); punkt 3
  "Kärnvapen" votering `A52E4273-06BE-4869-9C8D-078E3607B40F` = V 20 Nej, MP 15 Avstår; punkt 4
  "Permanenta baser" votering `2F1B8869` = 281–21 (V Nej); punkt 6 "Domsrätt" votering `B7FC3608`
  = 267–20. REGERINGSLÄGES-TEST: blocköverskridande — S (opposition) röstade Ja med regeringssidan;
  V:s och MP:s Nej är instrumentspecifikt, belagt av deras egna avvikande meningar om just DCA i
  Ds 2024:6 bilaga 4 (V: "Vänsterpartiet är motståndare till det så kallade DCA-avtalet";
  MP: "Miljöpartiet kommer att rösta nej till avtalet").
- **Effektevidens (steg 1):** Försvarsberedningen, Ds 2024:6 "Stärkt försvarsförmåga – Sverige som
  allierad" (april 2024, blocköverskridande beredningsorgan — samma neutrala ankare som befintliga
  `nato_medlemskap`-posten). Instrument-exakta utsagor (verbatim-kollade mot HCB46.html): "Avtalet
  utgör en förutsättning för ett mer kontinuerligt operativt försvarssamarbete genom att lägga fast
  förutsättningarna för amerikanska styrkor i Sverige"; "DCA skapar förutsättningar för amerikanskt
  militärt stöd om säkerhetsläget så kräver och är således av stor betydelse för Sveriges säkerhet
  ... DCA-avtalet är stabiliserande, höjer tröskeln för angrepp mot Sverige och blir viktigt för
  försvaret i norra Europa"; avtalet "förbättrar därmed förutsättningarna för amerikanskt stöd till
  Sverige". Kopplingen avser exakt `nato_interoperabilitet` (förmåga att operativt agera gemensamt
  med allierade: tillträde till anläggningar, förhandslagring, kontinuerligt operativt samarbete med
  USA — Sveriges viktigaste allierade i Nato). Förslag: evidence_level=authority_evaluation,
  effect_strength=medium (förutsättnings-/mekanismutsaga från beredningsorgan, ingen
  ex-post-utvärdering — lägre än nato_medlemskaps "nära definitionella" high), confidence=high
  (entydig riktning, blocköverskridande organ, upprepad i flera avsnitt).
- **Riktning:** positiv — ordinarie admission gäller (negativ-riktnings-grinden §5 ej tillämplig).
  Partier som motsätter sig instrumentet (V, MP) vänds till negativt B via _FLIP, samma mönster som
  `nato_medlemskap` och klimat-reduktionsplikt.
- **Neutralitet:** ingen vänster-höger-metodpreferens (S+SD+M+C+KD+L på samma sida; splittringen är
  säkerhetspolitisk linje, inte block). Inga befintliga DCA-referenser i config (grep=0).
  **RISK 1 (flagga för sign-off):** samma indikator som `nato_medlemskap` i samma undermått
  (nato_ukraina) → V får TVÅ opposes-poster på `nato_interoperabilitet`. Distinkt instrument
  (bilateralt basavtal med USA: rättslig status, anläggningstillträde, förhandslagring — vs
  multilateralt alliansmedlemskap) och prejudikat finns (`territoriella_utslapp` bär både
  reduktionsplikt och koldioxidskatt), men stackningen för V bör vägas medvetet vid sign-off.
  MERVÄRDE: MP differentieras NYTT — MP=none på nato_medlemskap (reverserad position) men opposes på
  DCA är AKTUELL (votering juni 2024 + avvikande mening Ds 2024:6). **RISK 2:** MP:s nej är villkorat
  (vill ha kärnvapenförbudslagstiftning för att kunna stödja) — voteringen Nej på godkännandepunkten
  är ändå instrument-exakt per stance-regeln §1; nyansen skrivs i mapping_note per bunten-regeln §2,
  aldrig som skäl att förkasta. **RISK 3 (citation):** punkt 1-partifördelningen vilar på riksdagens
  beslutsnotis (officiell) eftersom API:t saknar p1-raden — implementeraren bör citera notisen +
  dokumentstatus + p3–p6-voteringarna som korroboration. Ej sidoeffekt-proxy, ej acklamation, ej
  budgetmagnitud (ingen A-dubbelräkning).
- **Partifördelning (preliminär):** supports: S, M, SD, C, KD, L (Ja på godkännandet). opposes:
  V (Nej, "motståndare till DCA-avtalet"), MP (Nej, aktuell position, villkorad på
  kärnvapenförbudslag — mapping_note). Differentierar V OCH MP mot övriga sex — starkare
  särskiljning än nato_medlemskap (som bara differentierar V).

### 5.2 Rejected-candidate-logg (forsvar)

1. **TPNW/kärnvapenförbudskonventionen → nato_interoperabilitet NEGATIV för tillträde:** omstridd
   (V-motioner, reservationer; även punkt 3 "Kärnvapen" i UFöU1 voterades V Nej/MP Avstår) men
   FALLER på negativ-riktnings-grinden §5.1 — enda riktade officiella källan är enmansutredningen
   (Lundin 2019), närmare expertutlåtande än authority_evaluation, dessutom pre-Nato-medlemskap
   (bryggan till dagens indikator håller inte utan tolkning) + skulle ge V en TREDJE negativ post på
   samma indikator (stacknings-/neutralitetsrisk).
2. **Beredskapslager/försörjningsberedskap → civil_beredskap_niva:** voteringarna är
   tillkännagivande-punkter med opposition-vs-Tidö-mönster = regeringsläges-artefakt;
   SOU 2023:50/RiR belägger BEHOV och organisationsmodell, inte instrument→indikator-effekt; delvis
   redan täckt av `tydlig_statlig_styrning_civilt_forsvar` (dubbelräkningsrisk).
3. **genomforbarhet_leverans:** dokumenterad äkta steg-1-vägg (djupsvep §5.8, 7 instrument, HOLD) —
   ej om-svept per metodminne.
4. **Utökad värnpliktsvolym:** dubbelräknar `ateraktiverad_utokad_varnplikt`
   (personal_varnpliktiga) och är i praktiken konsensus.
5. **Ukraina-ramverk/militärt stöd → ukraina_stod:** enhällighet i kammaren, ej omstridd (skulle
   bara bli konsensus-mått, B3 söker differentiering).
6. **UFöU1 punkt 4 "Permanenta baser med utländsk trupp"** (281–21, V Nej): subsumeras i
   DCA-instrumentet — separat kodning vore dubbelräkning i samma undermått.

Verifieringsläge: alla voteringssiffror hämtade live från data.riksdagen.se (voteringlista +
votering/{id}/json + dokumentstatus HB01UFöU1); punkt 1-fördelningen från riksdagens officiella
beslutsnotis 2024-06-18 (API-luckan för p1 dokumenterad i kandidaten); Ds 2024:6-citat
verbatim-kollade mot data.riksdagen.se/dokument/HCB46.html (10 DCA-omnämnanden).

---

## 6. Klimat

### 6.1 `drivmedelsskatt_energiskatt_bensin_diesel` → `territoriella_utslapp` (utslappsminskningar) — **REJECT**

- **Contested (steg 2):** VERIFIERAT mot data.riksdagen.se men FALLER på "verklig splittring".
  (a) bet. 2021/22:SkU19 (sänkt energiskatt på bensin/diesel, prop. 2021/22:84 p.1-2, riksmöte
  2021/22): "I betänkandet finns en reservation (MP) och fem särskilda yttranden (M, SD, C, V, L)"
  — dvs ENDA oppositionsreservationen var MP (vill INTE sänka, klimatskäl); alla övriga gav
  särskilda yttranden eller stödde. Drevs av M/SD/KD-budgeten. (b) bet. 2023/24:SkU7
  (prop. 2023/24:24, riksmöte 2023/24) punkt 1: deltagarlistan markerar S, V, C, MP-ledamöterna
  "* Avstår från ställningstagande under punkt 1, se särskilda yttranden"; reservation 1-2
  (endast C) gäller punkt 2-3 (landsbygds-/jordbruksavdrag), INTE skattesänkningen. Källa:
  data.riksdagen.se/dokumentstatus/h901sku19.html och .../hb01sku7.html. => Ingen ren
  för/emot-votering på själva instrumentet; mönstret är budget-/blockstyrt med opposition som avstår
  + en grön-axel-reservation (MP/C). Regeringsläges-artefakt, ej instrument-splittring.
- **Effektevidens (steg 1):** Naturvårdsverket, "Sveriges klimatutsläpp ökade med 7 procent under
  2024" (pressmeddelande/preliminär territoriell statistik, juni 2025). MEN källan tillskriver
  ökningen "framför allt ... ökad användning av fossil diesel inom vägtrafiken och arbetsmaskiner"
  p.g.a. att "reduktionsplikten minskats i januari 2024" — INGEN instrument-exakt attribution till
  energiskatte-/drivmedelsskattesänkningen. Riktningsmekanismen för en bränsleskatt på
  `territoriella_utslapp` är ekonomiskt rimlig men SAKNAR officiell svensk källa som kopplar JUST
  detta instrument till indikatorn. evidence_level vore i bästa fall authority_evaluation men
  bryggan instrument→indikator är icke belagd för skatten specifikt (RiR 2012:1 belägger
  koldioxidskatt, inte energiskatt på drivmedel). confidence: low.
- **Riktning:** positiv (höjd/bibehållen skatt → lägre territoriella_utslapp); cut-supportrar
  skulle få negativt B via flip → negativ-riktnings-grinden (§5) AKTIVERAS och FALLER: §5.3 kräver
  att evidensen avser exakt indikatorn för JUST detta instrument — Naturvårdsverket attribuerar till
  reduktionsplikt, inte skatten.
- **Neutralitet:** DUBBELRÄKNING + blockspegling. Drivmedelsskattesänkningen och
  reduktionspliktssänkningen ingick i SAMMA Tidö-paket (sänka pumppriset) och röstas av samma
  block → ett parti som ogillar "dyrare fossilbränsle" straffas redan via `reduktionsplikt_drivmedel`
  (befintlig liggarpost, samma undermått utslappsminskningar, samma indikator territoriella_utslapp).
  Att addera skatten räknar samma stance två gånger; splittringen speglar blockläget, inte
  instrumentet. Tydlig vänster-höger-metodtilt (pumppris vs utsläpp).
- **Partifördelning (preliminär):** Block: M/SD/KD/L (regering+stöd) för sänkning; MP emot
  (reservation, klimatskäl); S/V/C avstår eller särskilt yttrande. Speglar block, ej instrument.

### 6.2 `slopad_flygskatt` → `konsumtionsbaserade_utslapp` (utslappsminskningar) — **REJECT**

- **Contested (steg 2):** omstridd i sak (M/SD vill avskaffa: motion 2021/22:855 Riedl (M), motion
  2023/24:70 Gholam Ali Pour (SD); MP/C vill behålla). MEN det faktiska slopandet (1 juli 2024)
  genomfördes via regeringens BUDGET/ändringsbudget-ram, inte en fristående namnvotering om
  instrumentet. Agenten hittade INGEN ren stand-alone för/emot-namnvotering på data.riksdagen.se som
  speglar instrumentet snarare än budgetblocket (motionerna avslås rutinmässigt i budgetsamordnade
  betänkanden). Gissar INTE partifördelning. => omstridd i princip men voteringen är
  budget-/blockspeglande, inte instrument-ren.
- **Effektevidens (steg 1):** SVAG. Flygskatten är distansbaserad (ej utsläppsbaserad), och svenskt
  flygs utsläpp ligger till stor del UTANFÖR de territoriella nationalräkenskaperna (internationell
  bunkring). Flygskatteutredningen (SOU 2016:83) och Trafikanalys uppskattade en LITEN
  utsläppseffekt. Ingen officiell svensk källa fastställer en robust instrument-exakt effekt på vare
  sig `territoriella_utslapp` eller `konsumtionsbaserade_utslapp`. evidence_level: svagt/blandat.
  confidence: low.
- **Riktning:** positiv (flygskatt → lägre flygutsläpp) skulle göra slopande negativt;
  negativ-grinden (§5) faller eftersom evidensen är svag/blandad och inte avser exakt en kanonisk
  indikator (utsläppen mestadels utanför territoriella konton).
- **Neutralitet:** risk för grön-axel-tilt (flygskatt = klassisk vänster-höger-symbolfråga) +
  budget-/blockspegling. Ingen ren instrument-splittring; sidoeffekt-/proxyproblem (distansskatt
  mäter ej utsläpp). Ej byggbar neutralt.
- **Partifördelning (preliminär):** M/SD-driven slopning; MP/C för bibehållande. Genomfört via
  budget → blockspegling, ej verifierad fristående votering.

### 6.3 Notes och landskap (klimat)

SÖKT: nya OMSTRIDDA ∧ EVIDENSBELAGDA ∧ NEUTRALA policy_types för klimat, med fokus på tunna/svagt
differentierande undermått. UTFALL: ingen STRONG, ingen försvarbar WEAK → legitim lucka per §8
(inget täckningsmål).

**Landskap (verifierat mot config):** klimat har 5 undermått, varav 4/5 redan B-täckta. Befintliga
liggarposter: reduktionsplikt_drivmedel→territoriella_utslapp (Naturvårdsverket, votering MJU5),
koldioxidskatt→territoriella_utslapp + →utslappsminskning_per_krona (RiR 2012:1),
ny_karnkraft→effektbrist (Svk Kraftbalansen 2025, votering/motioner),
atgarder_mot_invasiva_frammande_arter→hotade_arter_naturforlust (Naturvårdsverket, enhällig MJU13
p1, FLAGGAD v0). 5:e undermåttet industriell_konkurrenskraft har INGEN kanonisk indikator i
categories.yaml → omöjligt att adressera utan modellutvidgning (utanför mandatet "effekten måste
avse EXAKT en indikator").

**Otäckta kanoniska indikatorer + varför ingen kandidat håller:**
- `konsumtionsbaserade_utslapp` (utslappsminskningar): ingen officiell svensk källa kopplar ett
  OMSTRITT riksdagsinstrument instrument-exakt till konsumtionsbaserade utsläpp (Naturvårdsverket
  rapporterar nivån men attribuerar inte till en kontroversiell votering). Lucka.
- `fossil_energianvandning` (energi_elpriser): se EXTENSION nedan — enda instrument-exakta
  evidensen är reduktionsplikt, men det är ingen NY policy_type och dubbelräknar.
- `elprisvolatilitet` (energi_elpriser): instrument (marknadsdesign, mer planerbar kraft,
  nätutbyggnad) saknar omstridd namnvotering med instrument-exakt officiell evidens; mestadels
  konsensus/Svk-teknik. D-härledd serie redan planerad (BACKLOG Våg 3, Svk spotpris). Lucka.

**EXTENSION-OPTION (EJ ny policy_type, dokumenteras för användarens bedömning):**
`reduktionsplikt_drivmedel` → `fossil_energianvandning` (down). Naturvårdsverkets 2024-statistik
säger ORDAGRANT att reduktionspliktssänkningen gav "ökad användning av fossil diesel inom
vägtrafiken och arbetsmaskiner" → instrument-exakt för fossil_energianvandning (idag B-tomt). MEN:
(1) det är ingen NY åtgärdstyp; (2) partipositionerna skulle vara BYTE-IDENTISKA med befintliga
territoriella_utslapp-raden (samma MJU5-votering) → NOLL ny differentiering, bara förstärkning av
ETT partistance tvärs två undermått; (3) det vore ren coverage-padding som §8 uttryckligen förbjuder
("att fylla luckor för att höja coverage är förbjudet"). Bedömning: REJECT som rankningsdrivande
mått; kan ev. läggas som icke-rankningsdrivande dokumentation om användaren vill belägga
fossil_energianvandning-mekanismen, men då med uttrycklig dubbelräknings-flagga.

**Genomgående vägg** (bekräftar tidigare svep, MEMORY rosta-b-sweep + rosta-d-sweep): klimatens
omstridda namnvoteringar är antingen (a) budget-/blockstyrda (drivmedelsskatt, flygskatt) eller
(b) "avslå mer-ambition" = grön-axel-tilt, eller (c) opposition avstår på själva lagändringen. De
två rena instrument-splittringarna som FINNS (reduktionsplikt MJU5, ny_karnkraft) är redan byggda.
Inget nytt neutralt+evidensbelagt instrument återstår. Rekommendation: lämna klimat som lucka;
lägg ev. krut på elprisvolatilitet/fossil via D-sidan (Svk-adapter) i stället för B.

---

## 7. Integration

### 7.1 `uppsokande_forskoleerbjudande_nyanlandas_barn` → `skolresultat_utsatta_omraden` (skola_sprak) — **STRONG** → byggd v0

- **Contested (steg 2):** votering bet. 2021/22:UbU24 "Förskola för fler barn" (prop. 2021/22:132),
  punkt 1 "Avslag på propositionen", 2022-06-01, votering_id `13F52F92-6597-473E-B912-4C7BB0EEE42F`
  (data.riksdagen.se, partifördelning verifierad ur dokvotering): JA till lagförslaget 228 = S 89,
  M 62, C 26, V 21, L 15, MP 14 (+1 obunden); NEJ (avslag) 70 = SD 50, KD 20. ÄKTA INSTRUMENT-SPLIT,
  inte regeringsläges-artefakt: M, C, L (opposition) röstade MED S-regeringen; SD+KD:s reservation 1
  motiverar avslaget med instrumentet självt, ordagrant: "Vi värnar valfriheten", förslaget är
  "resurskrävande och integritetskränkande" och "allt för ingripande gentemot vårdnadshavarna" —
  samtidigt som de uttryckligen DELAR målet ("Propositionen lyfter ... att förskolan ska bidra till
  en bättre språkutveckling. Vi delar i grunden denna uppfattning men ser att det kan och bör ske på
  annat vis"). Tidsnot (§4): riksmöte 2021/22, en session före föredragen period — mapping_note
  krävs; ingen nyare votering om samma instrument finns (utredning U 2024:04 om obligatorisk
  språkförskola redovisas först dec 2025, ej lagstiftad).
- **Effektevidens (steg 1):** SOU 2020:67 "Förskola för alla barn – för bättre språkutveckling i
  svenska" (nov 2020) — utredningen som föreslog EXAKT detta instrument (uppsökande verksamhet +
  obligatoriskt/direkt erbjudande av förskoleplats från 3 år för barn till nyanlända, skollagen
  8 kap. 12a–12c §§). Citerad i bet. UbU24: "Barn som har gått i förskolan har bättre språkliga och
  kognitiva förutsättningar och når högre kunskapsresultat i grundskolan", med störst effekt "för
  barn med svag socioekonomisk bakgrund". Kausalkedjan är instrumentets KÄRNVÄRDE (inte sidoeffekt):
  uppsökande+obligatoriskt erbjudande → ökat förskoledeltagande bland nyanländas barn → bättre
  språkutveckling/kunskapsresultat. evidence_level-förslag: authority_evaluation (SOU; samma nivå
  som SOU 2023:12-prejudikatet i demokrati). confidence-förslag: medium (design-/mekanismevidens;
  deltagande→resultat är belagt, men ingen svensk ex-post-utvärdering av själva direktinskrivningen
  ännu — lagen trädde i kraft 2023-07-01). effect_strength-förslag: medium. INDIKATOR-BRYGGA
  (skrivs ut i note): evidensen avser barn med utländsk bakgrund/svag socioekonomisk bakgrund;
  indikatorn är `skolresultat_utsatta_omraden` — samma brygga som befintliga raden
  `riktade_insatser_nyanlanda_elever` redan använder ("störst för utrikes födda" → utsatta områden).
- **Riktning:** positiv — negativ-riktnings-grinden (fas4c_rubrik §5) ej tillämplig; ordinarie
  admission gäller. Partier som röstade avslag (SD, KD) skulle få negativt B via _FLIP, samma
  mekanik som ny_karnkraft/reduktionsplikt — flaggas för mänsklig granskning som där.
- **Neutralitet:** ingen vänster-höger-metodpreferens: splitten är blocköverskridande (M, C, L med
  S/V/MP; SD+KD emot) och speglar instrumentet, inte blockläget. Ingen dubbelräkning: skola_sprak
  har idag bara `riktade_insatser_nyanlanda_elever` (statliga insatser i GRUNDSKOLAN,
  IFAU-utvärderad) — förskoledeltagande är ett distinkt instrument med distinkt evidenskälla;
  arbete_sjalvforsorjning berörs ej. Inte sidoeffekt-proxy: språkutveckling/kunskapsresultat är
  instrumentets uttalade kärnvärde. TRE RISKER att hantera vid panelbygge: **(1) AKTUALITET SD/KD** —
  Tidö-regeringens dir. 2024:113 (obligatorisk språkförskola för 5-åringar med påtagliga
  språkbrister) visar att SD/KD idag stödjer ett SNÄVARE obligatoriskt språkförskole-instrument;
  deras 2022-nej gällde prop 132:s bredare design (alla nyanländas barn från 3 år + uppsökande
  verksamhet riktad mot pedagogisk-omsorg-familjer). Panelen måste hålla policy_type
  instrument-exakt till prop 132-designen och pröva opposes vs none för SD/KD
  (MP/Nato-prejudikatet: föråldrad position ska inte ge negativt B). **(2)** Värdekonflikt-komponent
  (valfrihet) finns, men §6 utesluter bara när riktad officiell evidens SAKNAS — här finns
  SOU 2020:67 → kodbar instrumentell träffsäkerhet, samma logik som ny_karnkraft.
  **(3)** Indikator-bryggan utländsk bakgrund→utsatta områden ska källbeläggas i note (prejudikat
  finns i liggaren). Ej acklamation: 228–70 med rollupprop.
- **Partifördelning (preliminär):** supports: S, M, C, V, L, MP (alla Ja punkt 1). opposes: SD, KD
  (Nej + reservation 1 med instrument-exakt motivering) — med aktualitetsflagg: SD/KD kan landa som
  none om panelen bedömer dir. 2024:113 som positionsskifte för instrumentfamiljen.
  **Codex-triagens utfall:** SD/KD = **none** per aktualitetsprejudikatet — så byggdes posten.

### 7.2 Rejected-candidate-logg (integration)

Sökt brett över de tre icke-HOLD-undermåtten (arbete_sjalvforsorjning, skola_sprak,
migrationssystem); boendesegregation + normer_tillit EJ omsvepta (HOLD per djupsvep 2026-06-06/07 +
memory-mandat, väggdokumentation finns i categories.yaml-notes).

1. **Aktivitetskrav för försörjningsstöd** — bet. 2025/26:SoU29 punkt 6, votering 2026-05-20
   (S/M/SD/KD/L Ja 281; C Nej 24; V/MP Avstår 41; verifierad mot data.riksdagen.se, votering_id
   `0D7ED001-415B-4804-AAF6-488D84AE35EA`): DUBBLERAR befintlig policy_type
   `aktiveringskrav_ekonomiskt_bistand` → förkastad som NY åtgärdstyp, men **BIFYND till
   A2/stance-arbetet:** färsk, omstridd votering (C=nej!, V/MP=avstår) som kan uppdatera
   partiståndpunkterna för den befintliga raden. Se §8.3 nedan.
2. **Utbildningsplikt för nyanlända** — Statskontoret: "effekterna ... hittills små" →
   unclear/inert; som negativ post faller den på §5-grinden.
3. **Begränsad föräldrapenning för nyanlända (2017)** — IFAU 2024:14: ökat förskole-/sfi-deltagande
   "verkar inte bero på" begränsningen → null/unclear → inert.
4. **Sfi-bonus** — IFAU: effekt endast i Stockholm, ingen nationell effekt → mixed → inert
   (avskaffades dessutom 2014).
5. **Intensivåret** — samma instrumentfamilj som befintliga `sfi_kombinerat_med_praktik`
   (Dahlberg-Göteborgs-RCT:n är intensivårets förlaga; liggaren har uttrycklig
   dubbelräknings-spärr) + Af-uppföljning endast beskrivande → dubbelräkning i
   arbete_sjalvforsorjning.
6. **Nystartsjobb → sysselsattningsgap** — tvärkategori-dubblett av
   ekonomi/`subventionerade_anstallningar` (samma instrumentfamilj, samma IFAU 2018:14-evidens).
7. **Fler förvarsplatser → atervandande_effektivitet** — skulle åter-konsumera RiR 2020:7 som redan
   bär `se_over_ansvarsfordelning_atervandande` i samma undermått + frihetsberövande-värdekonflikt.
8. **Modersmålsundervisning** (SD-avskaffande-split finns) — endast korrelativ/selektionskänslig
   evidens, ej instrument-kausal → ej evidensbelagd.
9. **Språkkrav för medborgarskap/PUT** — omstridd men ingen svensk officiell effektevidens på
   `sfi_sprakkunskaper` → §6-utelämning.

`asyl_handlaggningstid` är D-only per design (categories.yaml-note: atervandande_effektivitet bär
B-spåret) → inget B-bygge sökt där. Utfall: 1 STRONG kandidat; luckan i övriga undermått är ett
legitimt utfall (§8, inget täckningsmål).

---

## 8. Demokrati

### 8.1 `rattssakerhetsgarantier_preventiva_tvangsmedel` → `overvakning_utan_rattssakerhet` (personlig_frihet) — **STRONG** → Codex HOLD (beslutsfråga B2)

- **Contested (steg 2):** bet. 2023/24:JuU24 "Preventiva tvångsmedel för att förebygga och
  förhindra allvarliga brott" (prop. 2023/24:117), 4 voteringar 2024-06-18 (verifierade via
  data.riksdagen.se/voteringlista, gruppering=parti): **PUNKT 1** (avslag på propositionen, res. 1 V):
  V Nej 20 — yrkade avslå hela utvidgningen; S 93/M 60/SD 63/C 21/KD 16/L 13/MP 15 Ja. **PUNKT 2**
  (anta lagförslagen, res. 2 C/res. 3 MP): MP Nej 15, C Avstår 21, V Avstår 20; S/M/SD/KD/L Ja.
  **PUNKT 4** (beslut i ärenden enligt inhämtningslagen = domstolsprövning, res. 5 C/res. 6 MP —
  exakt den garanti Lagrådet förordar): C Nej 21 (biföll sin reservation), MP Avstår 14, V Avstår
  20; S/M/SD/KD/L Ja (avslog domstolsprövning). **PUNKT 7** (översyn och utvärdering,
  res. 9 S+V+C+MP): S 93/V 20/C 21/MP 15 Nej mot M 60/SD 63/KD 16/L 13 Ja — äkta 4-4. INTE
  regeringsläges-artefakt: S röstade MED regeringen om själva utvidgningen (p1/p2/p4) men MOT om
  utvärdering (p7); C avstod p2 men röstade aktivt Nej p4; splittringen följer instrumentets
  rättssäkerhetsdimension, inte blockläget. Votering_id p7: `49FB1796-44FA-4818-8406-2D11E0F44CED`.
- **Effektevidens (steg 1):** Lagrådets granskningsyttrande över prop. 2023/24:117, återgivet i
  utskottets överväganden i bet. 2023/24:JuU24 (data.riksdagen.se/dokument/HB01JuU24.html) — samma
  neutrala officiella ankare och samma konstruktion som den redan admitterade posten
  `begransa_biometrisk_realtidsovervakning_rattssakerhet` (JuU28). Lagrådet fastslår: (1) beslut
  enligt inhämtningslagen bör fattas av allmän domstol eftersom realtidsinhämtning med egen teknik
  gör att "nivån på potentiella integritetsintrång blir en helt annan och mer ingripande" — dvs. en
  saknad rättssäkerhetsgaranti pekas ut; (2) det "ter sig svårbedömt huruvida utformningen av
  förslagen kan förhindra godtycke" (JO framför liknande: risk att tillämpningen "uppfattas som ett
  utslag av trakasseri eller otillbörlig kontroll från statens sida"); (3) det är "starkt påkallat"
  med samlad översyn av all preventiv tvångsmedelsreglering för att bedöma om
  integritetsinskränkningarna "kan anses godtagbara i ett demokratiskt samhälle"; (4) Lagrådet
  avstyrkte föreslaget ikraftträdande. Instrumentet = BEGRÄNSA/VILLKORA preventiva tvångsmedel med
  rättssäkerhetsgarantier (domstolsprövning i inhämtningslagen, oberoende utvärdering/översyn) →
  driver `overvakning_utan_rattssakerhet` NER. Förslag: evidence_level=authority_evaluation,
  confidence=medium, effect_strength=medium — identisk kalibrering som JuU28-posten.
  Kompletterande kontext: IMY:s rapport "Integritet och ny teknik 2020–2024" (IMY-2024-2570,
  överlämnad via skr. 2025/26:208, bet. 2025/26:KU36).
- **Riktning:** positiv (begränsning/villkorande driver indikatorn, som har riktning down, NEDÅT)
  med _FLIP för partier som röstade för utvidgning utan garantierna — samma mönster som
  `begransa_biometrisk_realtidsovervakning_rattssakerhet`. Klarar dessutom negativ-riktnings-grinden
  om panelen hellre kodar den negativt: authority_evaluation (Lagrådet, officiellt granskningsorgan)
  + confidence medium + exakt den betygsatta indikatorn (rättssäkerhetsgarantier vid hemlig
  övervakning är indikatorns kärnvärde, ingen sidoeffekt-proxy).
- **Neutralitet:** VÄNSTER-HÖGER-TILT: låg på instrumentnivå — ankaret är Lagrådet (inte
  partiretorik) och splittringen är blocköverskridande (S med M/SD/KD/L om utvidgningen; C aktivt
  Nej på domstolsprövning; p7 4-4). **DUBBELRÄKNING (viktigaste flaggan, måste till panel):** samma
  indikator/undermått (personlig_frihet) som befintliga
  `begransa_biometrisk_realtidsovervakning_rattssakerhet` — men DISTINKT instrument
  (preventivlagen/inhämtningslagen/hemlig dataavläsning-utvidgningen 2024 vs AI-ansiktsigenkänning i
  realtid 2025/26), distinkt Lagrådsyttrande, distinkt votering, och delvis ANNAN partifördelning
  (C: avslag-helt i JuU28 vs domstolsprövnings-reservation här; S: opposes garantier där vs stödde
  utvidgningen men drev utvärderingskravet här). Kumulativ effekt: två poster i samma undermått som
  båda gynnar övervakningsskeptiska partier — undermåttsviktningen (20 %) cappar dock totalpåverkan,
  och prejudikatet (flera instrument per indikator finns redan för korruption) tillåter det.
  SIDOEFFEKT-PROXY: nej — rättssäkerhetsgarantier vid hemlig övervakning ÄR indikatorns
  kärnkonstrukt. ACKLAMATION: nej — fyra rösträkningar. **S-KODNINGEN är panelens svåraste beslut:**
  S röstade för utvidgningen utan domstolsprövning (p1/p2/p4 Ja) men för utvärdering (p7 Nej) →
  beroende på exakt instrumentdefinition blir S opposes (om instrumentet = garantierna
  domstolsprövning m.m.) eller mixed/none; får INTE definieras post hoc för önskat utfall — förslag
  att instrumentet låses till Lagrådets två huvudgarantier (domstolsprövning + oberoende
  utvärdering/översyn) INNAN panelen kodar.
- **Partifördelning (preliminär):** supports (drev rättssäkerhetsgarantier/avslag): V (avslag,
  res. 1), MP (Nej p2, res. 3 + res. 6 beslutsordning), C (Nej p4 = domstolsprövning, res. 5 +
  res. 8 tillsynsresurser). opposes (röstade för utvidgning OCH avslog både domstolsprövning p4 och
  utvärdering p7): M, SD, KD, L. S: gränsfall — för utvidgningen (p1/p2/p4 Ja) men för
  utvärdering/översyn (p7 Nej, res. 9) → opposes eller none beroende på låst instrumentdefinition.

### 8.2 Rejected-candidate-logg (demokrati)

Sökstrategi: demokratis befintliga B är nästan helt konsensus (lagstadgat_oberoende_public_service,
insyn_partifinansiering, grundlagsskydd_domstolarnas_oberoende = alla 8 supports) eller
expert_opinion low/low (3 korruptionsposter) — enda omstridda posten är
`begransa_biometrisk_realtidsovervakning_rattssakerhet`. Letade därför kontesterade instrument per
indikator. Alla voteringar verifierade mot data.riksdagen.se:

1. **Mediestöd** (prop. 2022/23:133, bet. 2023/24:KU3 p1: M/SD/C/KD/L Ja 169, S Nej 94, V+MP
   avstår 33) → FÖRKASTAD som omstridd-artefakt: S/V/MP-reservationerna är EGNA alternativa
   lagförslag om mediestödets UTFORMNING (bilaga 3 "Reservanternas lagförslag" + gemensamt särskilt
   yttrande S,V,MP); inget parti motsätter sig instrumentet mediestöd → splittringen speglar
   design/regeringsläge, inte instrumentet; att koda S=opposes mediestöd vore vilseledande.
2. **Visselblåsarlagen** (bet. 2021/22:AU3, voteringar 288-18 och 281-26) → FÖRKASTAD: nära
   enhällig, inte omstridd; evidenskopplingen till korruption dessutom svag (Statskontoret 2023:13
   är redan expert_opinion-ankare för annan post).
3. **Utlandsspioneri som tryckfrihetsbrott** (grundlagsändringen 2022, äkta blocköverskridande Nej
   från V/MP/L) → FÖRKASTAD på negativ-riktnings-grinden: ingen svensk authority_evaluation kopplar
   instrumentet till mediefrihet (kritiken kom från medieorganisationer = otillåtna källor;
   V-Dem-nedgången 2023 är beskrivande statistik, fel evidence_level för negativ riktning).
4. **Säkerhetszoner** (bet. 2023/24:JuU13) → FÖRKASTAD: konstrukt-mismatch (kroppsvisitation är
   inte övervakning; indikator-bryggan till overvakning_utan_rattssakerhet håller inte) + skulle
   tredubbla samma övervakningsdimension.
5. **Offentlighetsprincip i friskolor** (SOU 2015:82) → FÖRKASTAD: dubbelräkning mot
   `starkt_oberoende_granskning_och_insyn` (MP redan ankrad på offentlighetsprincipen där) +
   tveksam brygga till politisk_transparens.
6. **Anonyma vittnen** (Lagrådet avstyrkte) → FÖRKASTAD: ingen kanonisk demokrati-indikator matchar
   (domstolsprocessens rättssäkerhet ≠ övervakning/politisering).

**BEVAKNING (ej kandidat i dag):** insynsregister för politiska beslutsprocesser (lobbyregister,
prop. 2025/26:258, bet. 2025/26:KU39) — potentiellt bästa transparens_ansvar-kandidaten med
SOU 2025:52 som authority-ankare, men kammarbeslutet är planerat 2026-06-15 (om 3 dagar) →
voteringen kan inte verifieras ännu; redan flaggad i BACKLOG B4-tabellen som "stark återöppning",
följ upp efter 06-15 (jfr KU39-notisen i beslutsunderlag_hold_2026-06-12.md).

**Luckor som förblir luckor (§8):** korruption_tillit (ingen omstridd ∧ evidensbelagd åtgärdstyp
funnen; fortroende_domstolar_myndigheter helt utan instrumentkandidat) och rattsstat_maktdelning
(författningsdomstol m.m. finns bara som motioner utan myndighetsevidens). Den levererade
kandidaten återanvänder exakt JuU28-mönstret (Lagrådet-ankare, positiv riktning + _FLIP,
authority_evaluation/medium) — viktigaste panelfrågan är S-kodningen och den kumulativa
två-poster-i-personlig_frihet-flaggan, båda utskrivna i neutrality_assessment.

---

## 9. Vad som återstår

§ 9.1 och 9.2 är beslutsfrågor i samma stil som
[beslutsunderlag_hold_2026-06-12.md](beslutsunderlag_hold_2026-06-12.md) — svara JA/NEJ.

### 9.1 Beslutsfråga B1 — forsvar / `dca_avtal_usa` (Codex HOLD)

> **✅ AVGJORD 2026-06-12: JA (alternativ A) — BYGGD samma dag, flaggad v0** (commit
> `data: B3 — dca_avtal_usa …`, samma commit som denna statusrad; hash i git-loggen).
> Verkställd med alla tre Codex-villkoren: (1) anti-stacknings-not i liggarposten (DCA =
> bilateralt basavtal vs nato_medlemskap = multilateralt alliansmedlemskap; prejudikat
> territoriella_utslapp; V:s andra opposes-post = sign-off:ad avvägning, differentieringsvinsten
> MP vägde tyngre); (2) p1-källkonstruktion (beslutsnotis 'Kammaren biföll utskottets förslag' +
> dokumentstatus HB01UFöU1 [punkt 1: beslutstyp 'röstning', vinnare 'utskottet', tomt votering_id —
> API-luckan omverifierad @antal=0] + följdvoteringarna p5 'Nedrustning' A1C914E0 [266/37: V 20 +
> MP 15 Nej] och p3 'Kärnvapen' A52E4273 [V 20 Nej, MP 15 Avstår], båda OMVERIFIERADE LIVE via
> data.riksdagen.se/voteringlista gruppering=parti 2026-06-12); (3) stance-confidence medium på
> alla 8 rader. Citaten (3 Ds-utsagor + V:s och MP:s avvikande meningar) ordagrant omverifierade
> mot HCB46-fulltexten. Resultat: 6 supports S/M/SD/C/KD/L, V + MP opposes; ranking oförändrad
> (C/KD forsvar +0,04 via coverage 3/4→4/5, MP forsvar −0,13, övriga mättade ±1).

- **Läge:** research-STRONG med komplett steg 1 (Ds 2024:6, Försvarsberedningen — samma neutrala
  ankare som nato_medlemskap) och steg 2 (UFöU1 p1 266–37, blocköverskridande, V/MP Nej belagt i
  egna avvikande meningar). Codex-triagen satte **HOLD** på två grunder: (i) **NATO-stackningsrisk** —
  posten ligger på samma indikator (`nato_interoperabilitet`) och samma undermått (nato_ukraina) som
  befintliga `nato_medlemskap`; V skulle få sin ANDRA opposes-post på samma indikator (kumulativ
  nedviktning av ett parti via två poster på en indikator bör vara ett medvetet människobeslut, inte
  ett agentbeslut); (ii) **p1-roll-call saknas i voterings-API:t** (@antal=0 för punkt=1) —
  partifördelningen vilar på riksdagens officiella beslutsnotis + dokumentstatus + fyra
  API-verifierade följdvoteringar med samma mönster, vilket är gott men en grad svagare än
  liggar-normen rå API-roll-call.
- **Alternativ:**
  - **A:** Bygg posten flaggad v0 med stacknings-flaggan i ledger-noten och trippelcitering
    (beslutsnotis + dokumentstatus HB01UFöU1 + p3–p6-voteringarna) för p1-fördelningen. Mervärde:
    MP differentieras NYTT (opposes aktuell, vs none på nato_medlemskap); prejudikat för
    två-instrument-per-indikator finns (territoriella_utslapp).
  - **B (Codex rek):** Behåll HOLD/BEVAKA. Trigger för återöppning: antingen (i) beslut att
    stackning på nato_interoperabilitet accepteras medvetet, eller (ii) p1-roll-call dyker upp i
    API:t/annan maskinläsbar officiell form.
- **Betygskonsekvens:** A: V får andra negativa B-posten på samma indikator (cappas av
  undermåttsviktning), MP får ny opposes; försvar-B breddas. B: ingen.
- **Beslutsfråga:** **JA/NEJ** — accepterar du NATO-stackningen på `nato_interoperabilitet`
  (V två opposes-poster på samma indikator) och beslutsnotis-citeringen för p1, så att
  `dca_avtal_usa` byggs som flaggad v0? (NEJ = kvarstår som HOLD/BEVAKA med triggrarna ovan.)

### 9.2 Beslutsfråga B2 — demokrati / `rattssakerhetsgarantier_preventiva_tvangsmedel` (Codex HOLD)

- **Läge:** research-STRONG med Lagrådet-ankare (exakt JuU28-mönstret) och fyra API-verifierade
  voteringar (JuU24 p1/p2/p4/p7) med genuint blocköverskridande mönster. Codex-triagen satte
  **HOLD** på två grunder: (i) **S-kodningen kräver instrumentlåsning + panel** — S röstade för
  utvidgningen utan domstolsprövning (p1/p2/p4 Ja) men för utvärdering/översyn (p7 Nej, res. 9);
  S blir opposes eller none beroende på hur instrumentet definieras, och definitionen får INTE
  sättas post hoc för önskat utfall → instrumentet måste låsas till Lagrådets två huvudgarantier
  (domstolsprövning + oberoende utvärdering/översyn) INNAN en panel kodar ståndpunkterna;
  (ii) **stackning** — detta vore den ANDRA rättssäkerhetsposten i undermåttet personlig_frihet
  (bredvid begransa_biometrisk_realtidsovervakning_rattssakerhet); båda gynnar
  övervakningsskeptiska partier, kumulativt.
- **Alternativ:**
  - **A:** Ge mandat: lås instrumentdefinitionen till Lagrådets två huvudgarantier, kör
    panel-kodning av S (och övriga), bygg flaggad v0 med stacknings-flaggan i ledger-noten.
  - **B (Codex rek):** Behåll HOLD tills användaren själv tagit ställning till
    (i) instrumentlåsningen och (ii) om två poster i personlig_frihet accepteras. Allt underlag
    (voterings-id:n, Lagrådscitat, reservationsnummer) är bevarat här för direkt återupptag.
- **Betygskonsekvens:** A: M/SD/KD/L får opposes (avslog både p4 och p7), V/MP/C supports,
  S beror på låsningen; personlig_frihet får andra posten åt samma håll (cappas av
  undermåttsvikten 20 %). B: ingen.
- **Beslutsfråga:** **JA/NEJ** — godkänner du (i) instrumentlåsningen till Lagrådets två
  huvudgarantier och (ii) den andra posten i personlig_frihet, så att panel-kodningen (inkl.
  S-gränsfallet) körs och posten byggs som flaggad v0? (NEJ = kvarstår som HOLD med underlaget
  bevarat här.)

### 9.3 Bifynd — A2/stance-underhåll: aktivitetskrav-voteringen 2026-05-20

Integration-researchens rejected-logg (post 1, §7.2) fann en **färsk omstridd votering på en
BEFINTLIG liggarpost:** bet. 2025/26:SoU29 punkt 6 (aktivitetskrav för försörjningsstöd), votering
2026-05-20, votering_id `0D7ED001-415B-4804-AAF6-488D84AE35EA` (API-verifierad):
**S/M/SD/KD/L Ja 281; C Nej 24; V/MP Avstår 41.** Instrumentet dubblerar befintliga
`aktiveringskrav_ekonomiskt_bistand` → ingen ny åtgärdstyp, men voteringen kan **uppdatera de
befintliga partiståndpunkterna** (notera särskilt C = Nej och V/MP = avstår — färskare och mer
differentierande källäge än postens nuvarande stance-underlag). Detta är A2-/stance-underhåll, inte
B3: hämta postens nuvarande ståndpunkter i party_positions.yaml, jämför mot voteringen och
uppdatera citat/mapping_notes vid avvikelse.

### 9.4 Övriga bevaknings-/återöppningstriggrar (samlade ur loggarna)

| Trigger | Kandidat som återöppnas | När |
|---|---|---|
| KU39-voteringen (lobbyregister, prop. 2025/26:258) | transparens_ansvar-bygge (redan instruerad i beslutsunderlag_hold_2026-06-12.md) | **2026-06-15** |
| V:s avskaffa-förstelärare-yrkande går till votering i UbU | `karriarsteg_forstelarare` → trolig STRONG | löpande |
| Tidö-utredningen likvärdig resursfördelning (IFAU-remiss 2025-11-28) | nytt skolvals-/skolpengsankare (valfard) | löpande |
| Lagstadgad säkerhetszons-utvärdering | `sakerhetszoner_visitationszoner` (steg 2 redan löst, 4-4) | ~2027 |
| Preventivlagens oberoende utvärdering (tidsbegränsad 5 år) | trygghet-spåret preventiva tvångsmedel | ~2028 |
| Brå-utvärdering kronvittnen resp. anonyma vittnen | kronvittnen / `anonyma_vittnen` | ej aviserad |
| Utredning U 2024:04 (obligatorisk språkförskola, redovisad dec 2025) → ev. lagstiftning | nyare votering för förskole-instrumentfamiljen | löpande |
