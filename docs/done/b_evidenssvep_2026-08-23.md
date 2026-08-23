# B — källstyrt evidenssvep per indikator (2026-08-23)

> **Status:** klart 2026-08-23. Registret skrevs medan svepet kördes, inte efteråt.
> Byggslice [#26](https://github.com/mcknschn/rosta/issues/26) under
> [ADR 0006](../adr/0006-evidensgrinden-ar-symmetrisk.md), regel i
> [fas4c_rubrik.md §5b](fas4c_rubrik.md) (version 2).
>
> Registret bevarar **hela** svepet, efter samma mönster som
> [b3_kandidatregister_2026-06-12.md](b3_kandidatregister_2026-06-12.md): inget fynd får gå
> förlorat, och även förkastade kandidater loggas med skäl så att en människa kan ompröva dem.

---

## 1. Protokoll (förregistrerat innan första sökningen)

**Enhet:** indikatorn, inte undermåttet. Rubriken §5.3 kräver att evidensen avser exakt den
betygsatta indikatorn, så undermått är för grovt för grinden (ADR 0006 punkt 3).

**Uppräkning:** samtliga 68 indikatorer i `config/categories.yaml`, i filens ordning. Ingen
indikator hoppas över, och ingen får djupare sökning än en annan. Skälet är ADR 0006:s förkastade
alternativ 4: att styra svepet mot de undermått där vår egen regel gör skada vore ett täckningsmål
via bakdörren, och §8 förbjuder det.

**Sökdjup (S1-S2):**

- **S1** sökningar som parar indikatorns sakord med `utvärdering effekt` och med de officiella
  utvärderingsorganen (Riksrevisionen, IFAU, Brå, SBU, Statskontoret, Vårdanalys, Socialstyrelsen,
  Skolforskningsinstitutet, Konjunkturinstitutet, ESV, Naturvårdsverket, Energimyndigheten, MSB,
  FOI, ISF, Delmi, Tillväxtanalys, IVO).
- **S2** varje träff som ser ut som en officiell utvärdering av ett **policyinstrument** mot exakt
  indikatorn hämtas och läses. Träffar som bara beskriver indikatorns nivå är statistik, inte
  utvärdering, och räknas inte.

> **Avvikelse, utskriven i stället för dold.** Protokollet skrevs först som två sökningar PER
> indikator, alltså 136 stycken. Körningen gjorde i stället 41 sökningar i kluster per undermått,
> där flera indikatorer delar sökning. Varje indikator ligger i minst ett kluster, men djupet per
> indikator blev alltså lägre än den ursprungliga texten lovade. Det som bär neutraliteten är att
> djupet är LIKFORMIGT, inte att det är stort: inget kluster fick fler sökningar för att dess
> undermått var hotat. Ett tunnare svep hittar färre poster i alla riktningar samtidigt, och den
> begränsningen gäller lika för de tio hotade undermåtten som för de nitton andra.

**Riktningsblindhet:** sökbegreppen innehåller aldrig `positiv`, `negativ`, `fungerar`, `misslyckad`
eller motsvarande. Verkan blir vad utvärderingen fann. B-grön-mandatet är avvecklat (ADR 0006
punkt 3), så svepet söker varken efter positiv eller negativ verkan.

**Ordningsregel (S3 före S4), ADR 0006 punkt 4:**

- **S3** verkan, `effect_strength` och `evidence_level` skrivs ned **i det här dokumentet** direkt
  efter läsningen.
- **S4** först därefter slås åtgärdstypens partirader upp i `config/party_positions.yaml`.

Regeln biter bara på **nya** åtgärdstyper. För de 44 som redan står i liggaren är partiraderna
kända sedan tidigare, och den kunskapen går inte att ta tillbaka. Begränsningen skrivs ut i stället
för att döljas.

**Grinden (rubriken §5, symmetrisk):** en ny post admitteras endast om alla tre gäller:
`evidence_level ∈ {authority_evaluation, systematic_review}`, `confidence ≥ medium`, och evidensen
avser exakt den betygsatta indikatorn utan sidoeffekt-proxy.

**Regel mot fynd på befintliga åtgärdstyper (skriven innan kandidaterna bedömdes).** Svepet stötte tidigt på
officiella utvärderingar som rör åtgärdstyper vars partirader redan är kända, däribland några av de
13 poster som faller på grinden. Att lägga en ny källa på en sådan post nu, när det är känt vilka 13
som faller och vem de träffar, är samma taintade drag som ADR 0006 punkt 2 förkastar när den vägrar
räkna fram en ny grindnivå. Regeln blir därför:

- Ett fynd som rör en **befintlig** åtgärdstyp byggs inte i den här slicen, oavsett åt vilket håll
  det pekar. Det gäller lika för en källa som skulle lyfta en post över grinden och för en källa som
  skulle lägga en ny indikatorrad på en känd åtgärdstyp. Fyndet loggas som **FÖRKASTAD** med källa
  och skäl och blir en återöppningstrigger för en senare slice, där kodningen kan göras innan någon
  vet vem den träffar.
- En **ny** åtgärdstyp grindas normalt. Där biter ordningsregeln, eftersom partiraderna inte är
  uppslagna.

Regeln är strängare än ADR 0006 kräver. ADR:n nöjer sig med att skriva ut begränsningen för de 44
befintliga åtgärdstyperna. Svepet väljer ett enda likformigt förbud i stället, eftersom en regel som
tillämpas från fall till fall inte går att skilja från ett urval gjort med utfallet i sikte.

**Inget täckningsmål (§8):** att svepet inte hittar något för en indikator är ett tillåtet utfall och
redovisas som tystnad, inte som lucka att fylla.

**Verdikt-legend:** `BYGG` = passerar grinden, ny liggarpost · `FÖRKASTAD` = granskad och fälld,
skälet står kvar · `TYST` = ingen officiell utvärdering av ett instrument mot exakt indikatorn hittad.

---

## 2. Fynd per indikator

### 2.0 Faktiskt sökdjup

Svepet kördes 2026-08-23 med **41 sökningar** och **6 hämtade källdokument**. Sökningarna gjordes i
kluster per undermått, inte en per indikator (se avvikelsen i §1), men varje indikator i
`config/categories.yaml` ligger i minst ett kluster och ingen indikator lämnades utan sökning.
Varje träff som såg ut som en kvantifierad myndighetsutvärdering av ett policyinstrument mot en
indikator hämtades och lästes.

**Djupet hölls likformigt med avsikt.** De 10 hotade undermåtten fick INTE fler sökningar än de
övriga 19, trots att tystnaden kostar mest just där. ADR 0006 förkastar uttryckligen att rikta
svepet mot dem: det är ett täckningsmål via bakdörren och §8 förbjuder det. Det betyder att en
tystnad här är prövad på samma djup som överallt annars, varken mer eller mindre.

### 2.1 Utfall i sammandrag

Raderna räknar INDIKATORER, inte kandidater: flera kandidater kan falla på samma indikator
(`vardkoer` fällde tre). Kandidatantalet står i egen kolumn så de två talen inte blandas ihop.

| Kategori | Indikatorer | BYGG | FÖRKASTAD | TYST | Kandidater granskade |
|---|---|---|---|---|---|
| ekonomi | 9 | 0 | 2 | 7 | 2 |
| valfard | 10 | 0 | 2 | 8 | 4 |
| trygghet | 8 | 0 | 1 | 7 | 1 |
| forsvar | 11 | 0 | 2 | 9 | 2 |
| klimat | 9 | **1** | 0 | 8 | 2 |
| integration | 11 | 0 | 0 | 11 | 0 |
| demokrati | 10 | 0 | 1 | 9 | 2 |
| **Summa** | **68** | **1** | **8** | **59** | **13** |

Ett fynd passerade grinden. Att det blev ett och inte tio är utfallet, inte ett misslyckande: §8
förbjuder täckningsmål, och ADR 0006 punkt 7 säger uttryckligen att ett krav på att svepet ska
hitta något är samma fel som ett krav på att det ska hitta positiv verkan.

---

## 3. BYGG - poster som passerar den symmetriska grinden

### 3.1 `klimatinvesteringsstod_klimatklivet` -> klimat / `utslappsminskning_per_krona`

**S3, låst 2026-08-23 innan `config/party_positions.yaml` slogs upp:**

| Fält | Värde |
|---|---|
| verkan (`direction`) | `negative` |
| `effect_strength` | `medium` |
| `evidence_level` | `authority_evaluation` |
| `confidence` | `medium` |

**Källa:** Riksrevisionen, granskningsrapport **RiR 2019:1** *Klimatklivet - stöd till lokala
klimatinvesteringar*, beslutad 2019-01-09.

**Vad utvärderingen fann.** Riksrevisionen bedömer att "Klimatklivet inte är en del av en
kostnadseffektiv styrmedelskombination för att nå det svenska klimatmålet till 2030".
Naturvårdsverkets egen statistik ger 1-4 kronor per kilo koldioxid, men när Riksrevisionen räknar
med dubbelräkning, bristande additionalitet och samverkan med andra styrmedel blir marginal-
kostnaden cirka 6,6 kronor per kilo för biogaskedjan och drygt 8,5 kronor per kilo för
laddstationer. Rapporten skriver att "klimatmålet skulle kunna uppnås till lägre marginalkostnad".

**Indikator-brygga (§5.3).** Ingen brygga behövs. Indikatorn `utslappsminskning_per_krona` har
riktning `up`, alltså är mer utsläppsminskning per krona bättre. Riksrevisionen mäter kronor per
kilo koldioxid, alltså exakt samma storhet inverterad. Hög marginalkostnad är låg utsläppsminskning
per krona. Verkan blir därför `negative` relativt indikatorns riktning.

**Nyans som skrivs in i posten.** Riksrevisionen 2025 (*Statens insatser för jordbrukets
klimatomställning*) finner att Klimatklivet bidrar till minskade utsläpp från jordbruket till en
kostnad under eller i nivå med koldioxidskatten. Det är ett smalare utsnitt än RiR 2019:1, som
bedömer stödet som helhet. Nyansen står i postens `note` och håller `effect_strength` på `medium`
och `confidence` på `medium` i stället för högre.

**Ordningsregeln (ADR 0006 punkt 4).** Åtgärdstypen är ny. Den fanns inte i liggaren, och
`tests/test_fas4.py` tvingar att varje partiståndpunkt pekar på en åtgärdstyp som finns i liggaren,
så `config/party_positions.yaml` har noll rader för den av konstruktion. Raderna slogs inte upp före
kodningen ovan. **Utskriven begränsning:** det mekaniska skyddet håller, men Klimatklivet är ett
välkänt instrument och svepet kan inte påstå att det saknade all förhandsuppfattning om vilken sida
instrumentet förknippas med. Samma slags begränsning som ADR 0006 skriver ut för de 44 befintliga
åtgärdstyperna gäller alltså i svagare form även här.

**Följd som redovisas i förväg.** Posten lägger en kodbar åtgärdstyp i undermåttet
`kostnadseffektivitet`, som förut hade en enda (`koldioxidskatt`). Varje parti som har en
koldioxidskatt-ståndpunkt går därmed från 1/1 till 1/2 i det undermåttets djuptäckning, och klimats
B krymps mot neutralt för alla åtta lika. Att avstå från att bygga posten **för att** den sänker
täckningen vore ett täckningsmål och är förbjudet enligt §8. Ståndpunktssidan rörs inte i den här
slicen, så posten går in utan partirader.

---

## 4. FÖRKASTAD - granskade och fällda, med skäl

Skälen står kvar så att en människa kan ompröva eller återuppta varje spår.

### 4.1 Fällda på indikator-bryggan (§5.3)

| Kandidat | Indikator | Källa | Skäl |
|---|---|---|---|
| `standardiserade_vardforlopp_cancer` | valfard / `vardkoer` | RiR 2023:12 *I väntan på vård* (2023-06-15) | Riksrevisionen mäter kortare väntetider för flera cancerdiagnoser (21 dagar prostata, 5-6 dagar övriga) men varnar samtidigt för "undanträngning av patienter med större vårdbehov" och **rekommenderar att nettot utreds kvantitativt**. Bryggan cancerväntetid till vårdköer som helhet håller därför inte. §5.3 ger då `mixed`/`unclear`, alltså inert. Bygger inte. **Återöppningstrigger:** den nettostudie RiR rekommenderar. |
| `vardgaranti_lagreglerad` | valfard / `vardkoer` | RiR 2023:12 | Slutsatsen är en styrningsbedömning ("inte effektiv") utan kontrafaktisk effektskattning. Att väntetiderna försämrats sedan 2010 är en trend, inte en uppmätt verkan av instrumentet. |
| `komiljard_prestationsbaserad_ersattning` | valfard / `vardkoer` | RiR 2023:12 | Effekten "avtog" enligt rapporten, alltså ingen bestående riktad verkan. Posten vore inert och skulle lyftas av grund E2. |

### 4.2 Fällda på att åtgärdstypen redan finns i liggaren

För dessa är partiraderna kända sedan tidigare, så ordningsregeln kan inte uppfyllas. Att lägga en
ny källa på dem nu, när det är känt vilka 13 poster som faller och vem de träffar, är samma taintade
drag som ADR 0006 punkt 2 förkastar. Regeln tillämpas likformigt och blint för vem den gynnar.

| Fynd | Rör åtgärdstyp | Källa | Återöppningstrigger |
|---|---|---|---|
| Statens styrning av civilt försvar har inte varit tillräckligt effektiv 2015-2024 | `tydlig_statlig_styrning_civilt_forsvar` (en av de 13) | RiR 2025:4 | Slice där kodningen kan göras innan utfallet är känt |
| Värnpliktens återinförande höjde inte antalet som tar anställning efter grundutbildning | `ateraktiverad_utokad_varnplikt` | RiR 2022:19 *Expansion utan prioritet* (2022-09-06) | Samma |
| Svepet återfann Brå:s utvärdering av snabbare lagföring i norra Stockholm | `snabbforfarande_lagforing` | Brå rapport 2020:3, samma källa som liggarens befintliga post redan citerar | Inget nytt fynd. Raden står här för att svepet ska vara komplett, inte för att något ändras |
| Statliga myndigheters skydd mot korruption är otillräckligt | `systematiskt_antikorruptionsarbete_kommuner_regioner` och `starkt_oberoende_granskning_och_insyn` (två av de 13) | RiR 2013:2 | Samma |
| Klimatklivet bidrar i jordbruket till en kostnad under koldioxidskattens nivå | `koldioxidskatt` som jämförelsenorm | RiR 2025, jordbrukets klimatomställning | Konsumeras som nyans i 3.1, byggs inte separat |

### 4.3 Fällda på nollresultat (verkan inte riktad, alltså inert)

| Kandidat | Indikator | Källa | Skäl |
|---|---|---|---|
| `selektiva_foretagsstod_innovationsbidrag` | ekonomi / `produktivitet` | Tillväxtanalys PM 2014:16 (Vinnova Vinn Nu, Forska och Väx) | Inga signifikanta effekter mot kontrollgrupp. Verkan blir `unclear`, `signed_direction` 0, posten kan aldrig ge B-effekt och skulle lyftas av grund E2. |
| Motstående fynd om arbetsmarknadsutbildning | ekonomi / `sysselsattning` | IFAU R 2011:7 | Översikten finner ingen eller negativ effekt för studier från 1989 och framåt, medan liggarens befintliga post vilar på IFAU R 2017:17. Befintlig åtgärdstyp, alltså 4.2. |

### 4.4 Fällda på att utvärderingen inte finns ännu

| Kandidat | Indikator | Läge |
|---|---|---|
| `karriarsteg_forstelarare` och lärarlönelyftet | valfard / `behoriga_larare` | Riksrevisionen påbörjade granskningen 2026-02-13 och skriver att "inga utvärderingar gjorts av reformernas långsiktiga effekter". Rapport planerad oktober 2026. **Återöppningstrigger:** den rapporten. Kandidaten stod redan som WEAK i [b3-registret](b3_kandidatregister_2026-06-12.md). |
| Myndigheters arbete mot oegentligheter vid inköp | demokrati / `korruption` | Riksrevisionens granskning publiceras oktober 2026. |

---

## 5. TYST - indikatorer utan officiell instrumentutvärdering

För 59 av 68 indikatorer hittade svepet ingen officiell svensk utvärdering som mäter ett
policyinstruments verkan på exakt den indikatorn. Tystnaden är tätast i två slag av indikatorer:

1. **Sammanvägda index.** De fyra V-Dem-indikatorerna (`rattsstatsindex`, `yttrandefrihetsindex`,
   `privata_friheter`, `horisontellt_ansvarsutkravande`) mäter Sveriges position i ett
   internationellt expertkodat index. Svenska myndigheter utvärderar instrument, inte sin plats i
   ett index, så ingen myndighetsutvärdering knyter ett instrument till ett indexutfall.
   Detsamma gäller i praktiken de enkätbaserade attitydmåtten `mediefrihet`, `upplevd_otrygghet`,
   `mellanmansklig_tillit` och `brukarnojdhet_hemtjanst`: myndigheterna mäter nivån återkommande
   men utvärderar inte ett instruments verkan på den.
2. **Målnivå-indikatorer** (`inflation`, `statsskuld_underskott`, `forsvarsanslag_andel_bnp`). De
   ligger dessutom utanför B:s och D:s gemensamma nämnare, som räknar icke-target-undermått.

**De tio hotade undermåtten.** Svepet fann ingen admissibel post för `korruption_tillit`,
`yttrandefrihet_medier`, `transparens_ansvar`, `vard_tillganglighet`, `omsorg_personal`,
`civil_beredskap`, `ekonomisk_ambition`, `forebyggande`, `realloner_hushall` eller
`biologisk_mangfald`. `vard_tillganglighet` kom närmast och föll på indikator-bryggan (4.1).

Det är svaret ADR 0006 punkt 5 bad om. Tystnaden i de tio undermåtten är nu **prövad** och inte bara
antagen, och den är ett fynd om evidensläget snarare än en följd av vår egen regel. Bevisbördan
ligger därmed rätt när de 13 posterna lyfts ut.

---

## 6. Vad svepet inte gjorde

- **Ståndpunktssidan rörs inte.** Inga partirader lades, ändrades eller togs bort. Den nya posten i
  3.1 har noll partirader.
- **Ingen befintlig post ändrades.** Varken verkan, styrka, evidensnivå eller confidence rördes på
  någon av de 44 åtgärdstyper som redan stod i liggaren.
- **Världshypotesen prövades inte.** Att officiella svenska utvärderingar oftare studerar åtgärder
  någon trodde på står kvar som känd svaghet utan åtgärd, precis som ADR 0006 skriver.
