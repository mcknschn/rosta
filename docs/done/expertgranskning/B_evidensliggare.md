# Granskning B — evidensliggare (`config/evidence_ledger.yaml`)

> AUTOGENERERAD av `pipeline/tools/review_packet.py` — ändra inte för hand.

**47 poster** (åtgärdstyp → indikatoreffekt), varav **33 matar B** och **14 är UTLYFTA**. Generell policy-evidens, medvetet **inte** partikopplad. Varje post som matar B sätter riktningen för ALLA partier som driver åtgärdstypen — granska källan noga (blast-radius anges per post).

En **utlyft** post föll på den symmetriska evidensgrinden (rubriken §5, [ADR 0006](../../adr/0006-evidensgrinden-ar-symmetrisk.md)): evidence_level i {authority_evaluation, systematic_review}, confidence minst medium, evidens som avser exakt indikatorn. Grinden gäller **oavsett verkan**. Posten är inte raderad — källa och skäl står kvar — men den ger inga claims och ligger utanför täckningsnämnaren. Granska den som ett arkiverat spår, inte som underlag för dagens betyg.

## Så granskar du

1. Öppna `source_url` och bekräfta att den svenska utvärderingen/akademiska källan faktiskt stöder `direction` på `indicator` (`positive` = rör indikatorn åt RÄTT håll).
2. Bedöm om `evidence_level`/`effect_strength`/`confidence` är rimliga (ej översålda).
3. Särskilt: `unclear`/`mixed` ger ≈neutral B (rätt om evidensen är svag); `negative` **vänder** semantiken; `expert_opinion` är svagast (ej uppmätt kausalitet).

---

## demokrati

### 🚫 `systematiskt_antikorruptionsarbete_kommuner_regioner` → korruption

- **Riktning:** positive · **evidensnivå:** expert_opinion · **styrka:** low · **konfidens:** low
- **Källa:** Statskontoret 2023:13, Nya utmaningar och gamla problem – om korruption i kommuner och regioner
- **URL:** https://www.statskontoret.se/uppdrag-och-rapporter/rapporter/2023/nya-utmaningar-och-gamla-problem--om-korruption-i-kommuner-och-regioner/lasrapporten
- **Not:** Rekommenderar systematiskt riskbaserat antikorruptionsarbete; inget uppmätt kausalsamband (expertbedömning).
- **Utlyft, skäl:** UTLYFT 2026-08-23 (#26, ADR 0006 punkt 2 och 5): faller på den symmetriska evidensgrinden, rubriken §5. Posten raderas INTE - källspåret står kvar - men hålls utanför claims och täckningsnämnaren. Faller på §5.1 OCH §5.2: evidence_level är expert_opinion och confidence är low. Postens egen not säger 'inget uppmätt kausalsamband (expertbedömning)'. Nio av de 13 utlyfta posterna kom ur B-grön-svepet, vars mandat var minst en post med positiv verkan per undermått. Mandatet är avvecklat (ADR 0006 punkt 3). Återöppningstrigger: en officiell utvärdering som mäter instrumentets verkan på exakt indikatorn och som bär confidence minst medium.
- **Skulle ha påverkat partier:** C(+), L(+), S(+), SD(+)
- 🚫 UTLYFT — matar inte B · ⚠ expert_opinion (ej uppmätt kausalitet) · ⚠ låg konfidens
- **OK?** ⬜ (✅/✏️/❌): 

### 🚫 `atgarder_mot_otillaten_paverkan_offentlig_sektor` → korruption

- **Riktning:** positive · **evidensnivå:** expert_opinion · **styrka:** low · **konfidens:** low
- **Källa:** Brå, kunskaps-/vägledningsmaterial om otillåten påverkan mot offentlig sektor
- **URL:** https://bra.se/amnen/otillaten-paverkan
- **Not:** Rekommenderar systematiskt förebyggande arbete; kvantifierar inte riskminskningen (expertbedömning).
- **Utlyft, skäl:** UTLYFT 2026-08-23 (#26, ADR 0006 punkt 2 och 5): faller på den symmetriska evidensgrinden, rubriken §5. Posten raderas INTE - källspåret står kvar - men hålls utanför claims och täckningsnämnaren. Faller på §5.1 OCH §5.2: expert_opinion och confidence low. Källan är vägledningsmaterial som rekommenderar förebyggande arbete och kvantifierar inte riskminskningen.
- **Skulle ha påverkat partier:** C(+), L(+), MP(+), S(+)
- 🚫 UTLYFT — matar inte B · ⚠ expert_opinion (ej uppmätt kausalitet) · ⚠ låg konfidens
- **OK?** ⬜ (✅/✏️/❌): 

### 🚫 `starkt_oberoende_granskning_och_insyn` → korruption

- **Riktning:** positive · **evidensnivå:** expert_opinion · **styrka:** low · **konfidens:** low
- **Källa:** ESO 2013:2, Allmän nytta eller egen vinning? (Bergh, Erlingsson, Sjölin, Öhrvall)
- **URL:** https://eso.expertgrupp.se/rapporter/20132-allman-nytta-eller-egen-vinning/
- **Not:** Brister i granskning av kommuner/bolag = korruptionssårbarhet -> stärkt insyn motverkar; ej effektutvärdering.
- **Utlyft, skäl:** UTLYFT 2026-08-23 (#26, ADR 0006 punkt 2 och 5): faller på den symmetriska evidensgrinden, rubriken §5. Posten raderas INTE - källspåret står kvar - men hålls utanför claims och täckningsnämnaren. Faller på §5.1 OCH §5.2: expert_opinion och confidence low. ESO 2013:2 är en analys av korruptionssårbarhet, inte en effektutvärdering av stärkt insyn. Nio av de 13 utlyfta posterna kom ur B-grön-svepet, vars mandat var minst en post med positiv verkan per undermått. Mandatet är avvecklat (ADR 0006 punkt 3). Återöppningstrigger: en officiell utvärdering som mäter instrumentets verkan på exakt indikatorn och som bär confidence minst medium.
- **Skulle ha påverkat partier:** C(+), KD(+), L(+), M(+), MP(+), S(+), SD(+), V(+)
- 🚫 UTLYFT — matar inte B · ⚠ expert_opinion (ej uppmätt kausalitet) · ⚠ låg konfidens
- **OK?** ⬜ (✅/✏️/❌): 

### `grundlagsskydd_domstolarnas_oberoende` → otillborlig_politisering

- **Riktning:** positive · **evidensnivå:** authority_evaluation · **styrka:** medium · **konfidens:** medium
- **Källa:** Prop. 2024/25:165 'Stärkt skydd för demokratin och domstolarnas oberoende' (bygger på SOU 2023:12, 2020 års grundlagskommitté), bet. 2025/26:KU2. Internationell bekräftelse: EU-kommissionens rättsstatsrapport 2024, Sverige-kapitlet.
- **URL:** https://data.riksdagen.se/dokument/HD01KU2.html
- **Not:** Förslaget tydliggör i regeringsformen att 'rättskipande verksamhet utövas av oberoende domstolar' och syftar till att 'minska risken för politisk styrning av den centrala domstolsadministrationen' (domstolsadministrationen leds av styrelse med domarmajoritet; regeringsmyndigheter får ej längre utöva tillsyn över domstolarnas rättskipande verksamhet) -> driver otillborlig_politisering NER. Institutionellt/normativt designargument (prop+SOU+EU-bedömning), ingen uppmätt kausaleffekt -> effect_strength/confidence medium. INTERNATIONELL KÄLLA endast som BEKRÄFTELSE (EU:s rättsstatsrapport), ej primärkälla, ej index — per DATA.md-undantag 2026-06-05.
- **Påverkar partier:** C(+), KD(+), L(+), M(+), MP(+), S(+), V(+)
- **OK?** ⬜ (✅/✏️/❌): 

### `begransa_biometrisk_realtidsovervakning_rattssakerhet` → overvakning_utan_rattssakerhet

- **Riktning:** positive · **evidensnivå:** authority_evaluation · **styrka:** medium · **konfidens:** medium
- **Källa:** Lagrådets yttrande över prop. 2025/26:150 (Polisens användning av AI för ansiktsigenkänning i realtid), återgivet ordagrant i bet. 2025/26:JuU28. Officiellt svenskt granskningsorgan.
- **URL:** https://data.riksdagen.se/dokument/HD01JuU28.html
- **Not:** NEUTRALT ANKARE = Lagrådet (officiellt svenskt granskningsorgan), EJ partiretorik: Lagrådet fann att förslaget 'går avsevärt längre än nödvändigt' och 'står därmed i strid med grundlag', att beslut flyttas från riksdag till åklagare/domstol och att det 'saknas reella överklagandemöjligheter' samt kraftigt begränsad tillsyn. Åtgärdstypen = att BEGRÄNSA eller VILLKORA biometrisk realtidsövervakning med rättssäkerhetsgarantier (domstolsprövning, proportionalitet, oberoende tillsyn, överklagande) -> driver overvakning_utan_rattssakerhet NER (positiv riktning; partier som motsätter sig vänds till negativt B via _FLIP, som klimat-reduktionsplikt). Institutionellt/normativt (Lagrådets proportionalitetsbedömning), ingen uppmätt kausaleffekt -> effect_strength/confidence medium.
- **Påverkar partier:** C(+), KD(−), L(−), M(−), MP(+), S(−), SD(−), V(+)
- **OK?** ⬜ (✅/✏️/❌): 

### 🚫 `lagstadgat_oberoende_public_service` → mediefrihet

- **Riktning:** positive · **evidensnivå:** authority_evaluation · **styrka:** low · **konfidens:** low
- **Källa:** Prop. 2024/25:166 'En lag om public service och riktlinjer för verksamheten 2026–2033' (bygger på 2023 års parlamentariska public service-kommitté, betänkandet SOU 2024:34 'Ansvar och oberoende – public service i oroliga tider'). Partiståndpunkter via enhälligt betänkande 2025/26:KrU2 punkt 1, acklamation.
- **URL:** https://data.riksdagen.se/dokument/HC03166.html
- **Not:** TILLAGD 2026-06-06 (B2, enhällighet-som-källa). INSTRUMENT: för första gången regleras public service-uppdraget I LAG (ny lag om public service) med LAGSTADGAT OBEROENDE, i stället för enbart i regeringsbeslutat sändningstillstånd -> mediefrihet UPP (positiv riktning) via institutionellt skyddat oberoende. SNÄV FORMULERING (codex-krav 2026-06-06): claimet avser lagstadgat oberoende -> mediefrihet/fri åsiktsbildning, INTE generellt 'public service-lag -> demokrati'. INSTRUMENT-MEKANISM (ordagrant ur prop. 2024/25:166 avsnitt 5.2.1, Regeringens förslag): 'Public service-uppdraget ska bedrivas självständigt i förhållande till såväl staten som olika ekonomiska, politiska och andra intressen och maktsfärer i samhället och verksamheten ska präglas av oberoende och stark integritet.' Provenans = bred politisk enighet (prop. avsnitt 4): 'I Sverige råder sedan länge en bred politisk enighet om att en väl fungerande mediemarknad bygger på en kombination av ansvarstagande kommersiella medier och ett starkt och oberoende public service med högt förtroende hos allmänheten'; mediepolitikens syfte är 'att skapa goda förutsättningar för en mångfald av självständiga medieaktörer som bidrar till att stärka en fri åsiktsbildning, ett fritt utbyte av idéer liksom en aktiv granskning av samhällets makthavare'. KAVEAT (effect_strength/confidence=LOW, codex-kalibrerat): MEKANISM-/DESIGNBASERAD evidens (parlamentarisk kommitté SOU 2024:34 + proposition), INGEN ex-post-effektutvärdering av att lagen MÄTT ökat mediefriheten -> låg styrka/förtroende; får ej formuleras som uppmätt indikatorförbättring. KONSENSUS-MÅTT (icke-rankningsdrivande): positioneras via enhälligt bet. 2025/26:KrU2 punkt 1 (acklamation, votering-API tomt @antal=0, 'Det har inte väckts någon motion som går emot att riksdagen antar regeringens lagförslag'); samtliga 15 reservationer gäller punkt 2-14 (innehållsuppdrag/ekonomi/uppföljning, S/V/C/MP) och tolkas INTE som opposition mot punkt 1 -> alla 8 partier supports på instrumentet att anta lagen. FRAMTIDA UPPGRADERING: om SOU/utvärdering belägger starkare varför lagFORMEN (ej bara oberoende i sak) stärker institutionellt oberoende. Demokrati yttrandefrihet_medier tidigare B-tomt -> demokrati 3/5 -> 4/5.
- **Utlyft, skäl:** UTLYFT 2026-08-23 (#26, ADR 0006 punkt 2 och 5): faller på den symmetriska evidensgrinden, rubriken §5. Posten raderas INTE - källspåret står kvar - men hålls utanför claims och täckningsnämnaren. Faller på §5.2: confidence är low. Institutionell designevidens ur prop. 2024/25:166 om vad lagen ska åstadkomma, ingen uppmätt effekt på mediefrihet. Nio av de 13 utlyfta posterna kom ur B-grön-svepet, vars mandat var minst en post med positiv verkan per undermått. Mandatet är avvecklat (ADR 0006 punkt 3). Återöppningstrigger: en officiell utvärdering som mäter instrumentets verkan på exakt indikatorn och som bär confidence minst medium.
- **Skulle ha påverkat partier:** C(+), KD(+), L(+), M(+), MP(+), S(+), SD(+), V(+)
- 🚫 UTLYFT — matar inte B · ⚠ låg konfidens
- **OK?** ⬜ (✅/✏️/❌): 

### 🚫 `insyn_partifinansiering` → politisk_transparens

- **Riktning:** positive · **evidensnivå:** authority_evaluation · **styrka:** low · **konfidens:** low
- **Källa:** Lagen (2018:90) om insyn i finansiering av partier (1 §), antagen via prop. 2017/18:55 'Ökad insyn i partiers finansiering – ett utbyggt regelverk', bet. 2017/18:KU19 punkt 1, acklamation. Syftesbekräftelse: dir. 2023:88 / SOU 2025:52 (insyn 'förebygger korruption och ökar legitimitet').
- **URL:** https://data.riksdagen.se/dokument/H501KU19.html
- **Not:** TILLAGD 2026-06-07 (B-grön-svepet, enhällighet-som-källa §5.2, FLAGGAD low/low). INSTRUMENT: lagstadgad öppen redovisning av partiers/ledamöters intäkter och bidrag (utbyggt 2018 till regional/lokal nivå + sidoorganisationer) -> politisk_transparens UPP. INSTRUMENT-MEKANISM (lagens 1 §, ordagrant): 'Syftet med lagen är att trygga allmänhetens insyn i hur partier ... finansierar sin verksamhet.' KAVEAT (effect_strength/confidence=LOW): institutionell/designevidens (lagens syftesparagraf + dir/SOU), INGEN uppmätt kausaleffekt på en transparensindikator. KONSENSUS-MÅTT (icke-rankningsdrivande): bet. 2017/18:KU19 punkt 1 (kärnlagen) togs i ACKLAMATION (verifierat: dokumentstatus p1 = acklamation), ingen reservation mot p1 -> alla 8 supports. Avser ENBART den breda insynslagen (p1); EXKLUDERAR den tiltade p4 'förbud mot partistöd från arbetsmarknadens parter' (röstning, M/C/KD-reservation). DUBBELRÄKNING ÅTGÄRDAD 2026-06-07 (sign-off, codex-flagga stängd): C:s och MP:s rader i bunten starkt_oberoende_granskning_och_insyn (-> korruption) omankrade från partifinansierings-citat till lobbyregister (C, HD023583 yrk. 17) resp. offentlighetsprincipen (MP, HA02181 yrk. 9); partifinansierings-instrumentet krediteras nu ENDAST här (transparens_ansvar). Övriga 6 partier i bunten är offentlighetsprincip/riksrevision (ingen överlapp). Poäng oförändrad (stance kvar supports).
- **Utlyft, skäl:** UTLYFT 2026-08-23 (#26, ADR 0006 punkt 2 och 5): faller på den symmetriska evidensgrinden, rubriken §5. Posten raderas INTE - källspåret står kvar - men hålls utanför claims och täckningsnämnaren. Faller på §5.2: confidence är low. Postens egen kaveat säger 'institutionell/designevidens (lagens syftesparagraf + dir/SOU), INGEN uppmätt kausaleffekt på en transparensindikator'. Nio av de 13 utlyfta posterna kom ur B-grön-svepet, vars mandat var minst en post med positiv verkan per undermått. Mandatet är avvecklat (ADR 0006 punkt 3). Återöppningstrigger: en officiell utvärdering som mäter instrumentets verkan på exakt indikatorn och som bär confidence minst medium.
- **Skulle ha påverkat partier:** C(+), KD(+), L(+), M(+), MP(+), S(+), SD(+), V(+)
- 🚫 UTLYFT — matar inte B · ⚠ låg konfidens
- **OK?** ⬜ (✅/✏️/❌): 

## ekonomi

### `subventionerade_anstallningar` → sysselsattning

- **Riktning:** positive · **evidensnivå:** systematic_review · **styrka:** medium · **konfidens:** medium
- **Källa:** IFAU Rapport 2018:14, Subventionerade anställningar – avvägningar och empirisk evidens (Forslund)
- **URL:** https://www.ifau.se/Press/Meddelanden/subventionerade-anstallningar--avvagningar-och-empirisk-evidens/
- **Not:** Högre sysselsättning för deltagare, men betydande undanträngning dämpar nettoeffekten.
- **Påverkar partier:** C(−), KD(+), L(+), M(+), MP(+), S(+), SD(−), V(+)
- **OK?** ⬜ (✅/✏️/❌): 

### `arbetsmarknadsutbildning` → sysselsattning

- **Riktning:** positive · **evidensnivå:** authority_evaluation · **styrka:** medium · **konfidens:** high
- **Källa:** IFAU Rapport 2017:17, Långsiktiga effekter av arbetsmarknadsutbildning (Vikström & van den Berg)
- **URL:** https://www.ifau.se/Forskning/Publikationer/Rapporter/2017/langsiktiga-effekter-av-arbetsmarknadsutbildning/
- **Not:** Högre arbetsinkomst och sysselsättning för deltagare, effekt kvarstår länge.
- **Påverkar partier:** C(−), KD(−), L(−), M(+), MP(+), S(+), SD(+), V(+)
- **OK?** ⬜ (✅/✏️/❌): 

### 🚫 `jobbskatteavdrag` → sysselsattning

- **Riktning:** unclear · **evidensnivå:** authority_evaluation · **styrka:** unknown · **konfidens:** low
- **Källa:** IFAU, forskningssammanfattning Jobbskatteavdrag
- **URL:** https://www.ifau.se/Press/Forskningssammanfattningar/Jobbskatteavdrag/
- **Not:** Effekten svår att utvärdera (kontrollgrupp saknas); inga säkra slutsatser.
- **Utlyft, skäl:** UTLYFT 2026-08-23 (#26, ADR 0006 punkt 2): faller på den symmetriska evidensgrinden, rubriken §5. Posten raderas INTE - källspåret står kvar - men hålls utanför claims och täckningsnämnaren. Faller på §5.2: confidence är low. IFAU anger själv att effekten är svår att utvärdera eftersom kontrollgrupp saknas. INTE en av de 13 som biljett #26 räknar upp, eftersom de 13 är de positiva posterna. Grinden gäller efter ADR 0006 lika oavsett verkan, så en post med verkan unclear prövas mot samma nivå. Posten var redan inert (signed_direction 0) och har noll partirader, så utlyftet flyttar inga betyg. Att låta den stå kvar hade krävt ett undantag för verkan, alltså exakt den asymmetri ADR 0006 tar bort.
- **Skulle ha påverkat partier:** —(ingen ståndpunkt)
- 🚫 UTLYFT — matar inte B · ⚠ unclear → ≈neutral B · ⚠ låg konfidens
- **OK?** ⬜ (✅/✏️/❌): 

### `fou_avdrag_skatteincitament` → produktivitet

- **Riktning:** positive · **evidensnivå:** authority_evaluation · **styrka:** medium · **konfidens:** medium
- **Källa:** Produktivitetskommissionen, slutbetänkande SOU 2025:96 'Fler möjligheter till ökat välstånd' + SOU 2025:3 'Skatteincitament för forskning och utveckling'
- **URL:** https://www.regeringen.se/rattsliga-dokument/statens-offentliga-utredningar/2025/10/sou-202596/
- **Not:** TILLAGD 2026-06-05 (BACKLOG B2, anti-binär): ger ekonomi B-evidens i submåttet bnp_produktivitet (1/5 -> 2/5, ej längre nära-binär). Produktivitetskommissionen lyfter FoU som produktivitetslever ('Kommissionen bedömer att företagsfrämjande åtgärder bör förbättras och FoU-avdraget förenklas'); SOU 2025:3 ser över FoU-avdraget för att öka företagens FoU-investeringar; utskottet (bet. 2022/23:SfU19) konstaterar att FoU 'bidrar till högre produktivitet och tillväxt'. KAVEAT (därför effect_strength/confidence=medium, ej high): riktningen FoU->produktivitet är väletablerad (kommission + ekonomisk forskning), men själva avdragets marginaleffekt är ALDRIG kausalutvärderad — exakt skälet bakom SOU 2025:3 och V:s avslagsmotivering. Riktning säker, magnitud osäker. Partiståndpunkter: party_positions fou_avdrag_skatteincitament (votering bet. 2022/23:SfU19, 7 supports / V opposes).
- **Påverkar partier:** C(+), KD(+), L(+), M(+), MP(+), S(+), SD(+), V(−)
- **OK?** ⬜ (✅/✏️/❌): 

### `konkurrenskraftig_foretags_och_agarbeskattning` → naringslivets_investeringar

- **Riktning:** positive · **evidensnivå:** authority_evaluation · **styrka:** medium · **konfidens:** medium
- **Källa:** Företagsskattekommittén, SOU 2014:40 'Neutral bolagsskatt – för ökad effektivitet och stabilitet'
- **URL:** https://www.regeringen.se/rattsliga-dokument/statens-offentliga-utredningar/2014/06/sou-201440/
- **Not:** TILLAGD 2026-06-05 (BACKLOG B2): nytt submått foretagande_investeringar (ekonomi 2/6 -> 3/6 täckta). BRED ram: konkurrenskraftig/lägre beskattning av företag OCH ägare/kapital -> högre avkastning efter skatt -> mer investeringar (positive på naringslivets_investeringar). Företagsskattekommitténs uppdrag var att utforma företagsbeskattningen så att 'investeringar som är lönsamma före skatt också ska vara lönsamma efter skatt' och främja investeringar/företagande. KAVEAT (effect_strength/confidence=medium, ej high): (1) investeringars elasticitet mot skatt är empiriskt omtvistad i magnitud; (2) bred ram -> supports-sidan belägger främst SÄNKT BOLAGSSKATT (direkt koppling till företagsinvestering) medan opposes-sidan belägger HÖJD KAPITAL-/ÄGARSKATT (mer indirekt koppling). Riktning rimlig, magnitud osäker. Partiståndpunkter: party_positions konkurrenskraftig_foretags_och_agarbeskattning (5 supports M/SD/C/KD/L, 3 opposes S/V/MP).
- **Påverkar partier:** C(+), KD(+), L(+), M(+), MP(−), S(−), SD(+), V(−)
- **OK?** ⬜ (✅/✏️/❌): 

### 🚫 `inkomststarkande_hushallspolitik` → hushallens_reala_disponibla_inkomst

- **Riktning:** positive · **evidensnivå:** descriptive_statistic · **styrka:** medium · **konfidens:** high
- **Källa:** Fördelningspolitisk redogörelse april 2025 (bilaga till 2025 års ekonomiska vårproposition, Finansdepartementet)
- **URL:** https://www.regeringen.se/informationsmaterial/2025/04/fordelningspolitisk-redogorelse-april-2025/
- **Not:** TILLAGD 2026-06-05 (BACKLOG B2): gör submåttet 'Reallöner och hushållens ekonomi' B-bart (ekonomi 3/6 -> 4/6) via den ARBETANDE indikatorn hushallens_reala_disponibla_inkomst (realloner förblir vilande kontext, ej partistyrbar). VÄRDENEUTRAL åtgärdstyp-FAMILJ: skatte- OCH/ELLER transfereringsreformer som höjer hushållens disponibla inkomst. Fördelningspolitiska redogörelsen definierar disponibel inkomst (arbets-/kapital-/näringsinkomst + transfereringar − direkta skatter) och analyserar hur skatte- och transfereringsreformer påverkar den -> både SÄNKT SKATT (höger) och HÖJDA TRANSFERERINGAR (vänster) höjer disponibel inkomst. Därför kodas BÅDA blocken som supports via sitt instrument = ingen höger-/vänstertilt (till skillnad från skatt/reglering där bara 'mindre stat' räknas). evidence_level descriptive_statistic (accounting/beskrivande, ej kausal välfärdsutvärdering) -> modest vikt; riktning definitionsmässigt säker -> confidence high. Partiståndpunkter: inkomststarkande_hushallspolitik (8 supports, instrument per parti i mapping_note).
- **Utlyft, skäl:** UTLYFT 2026-08-23 (#26, ADR 0006 punkt 2 och 5): faller på den symmetriska evidensgrinden, rubriken §5. Posten raderas INTE - källspåret står kvar - men hålls utanför claims och täckningsnämnaren. Faller på §5.1: evidence_level är descriptive_statistic. Fördelningspolitiska redogörelsen är officiell beskrivande statistik över hur inkomster fördelas, inte en utvärdering av att åtgärdstypen orsakar högre real disponibel inkomst.
- **Skulle ha påverkat partier:** C(+), KD(+), L(+), M(+), MP(+), S(+), SD(+), V(+)
- 🚫 UTLYFT — matar inte B
- **OK?** ⬜ (✅/✏️/❌): 

### `nedtrappad_ersattningsprofil_akassa` → arbetsloshet

- **Riktning:** positive · **evidensnivå:** authority_evaluation · **styrka:** medium · **konfidens:** medium
- **Källa:** IFAU, forskningssammanfattning 'Om a-kassa och löner' (syntetiserar Fredriksson & Söderström R 2008:12, Uusitalo & Verho WP 2007:21, Bennmarker m.fl. R 2013:10 och R 2005:16). Partiståndpunkter via votering bet. 2023/24:AU9 punkt 1 (prop. 2023/24:128).
- **URL:** https://www.ifau.se/Press/Forskningssammanfattningar/Om-a-kassa-och-loner-/
- **Not:** TILLAGD 2026-06-12 (B3 differentiering, v0→v1 AVFLAGGAD 2026-06-14 efter mänsklig slutgranskning, behåll oförändrad; codex BUILD-WITH-CHANGES). INSTRUMENTLÅSNING (codex-krav): posten avser inkomstbaserad a-kassa med NEDTRAPPAD ERSÄTTNINGSPROFIL (prop. 2023/24:128-designen: 80 % de första 100 ersättningsdagarna, därefter nedtrappning med 10 procentenheter efter 100 dagar och ytterligare 5 procentenheter efter 200 dagar, bet. AU9) — INTE generisk 'lägre/sämre a-kassa'. INDIKATOR-BRYGGA (explicit, §5.3-mönstret): evidensen avser arbetslöshetsNIVÅN — exakt indikatorn arbetsloshet — inte bara arbetslöshetstid. IFAU om R 2008:12 (Fredriksson & Söderström), ordagrant: när ersättningsnivån höjdes 'från 80 till 85 procent av tidigare lön' steg arbetslösheten 'förhållandevis mycket, med 1,5 procentenheter' -> ersättningsprofilens generositet driver arbetslöshetsnivån UPP, dvs. nedtrappad profil rör arbetsloshet (riktning down) ÅT RÄTT HÅLL = direction positive. MEKANISM FÖR JUST TIDSPROFILEN/NEDTRAPPNINGEN (Uusitalo & Verho WP 2007:21, finsk reform 2003): höjd ersättning de första 150 dagarna minskade sannolikheten att anställas med 20 procent och 'Effekten försvann efter 150 dagar då den högre ersättningen togs bort' -> ersättningens TIDSPROFIL (inte bara genomsnittsnivån) styr utfallet, direkt stöd för nedtrappningsprofilens verkningsmekanism. KAVEAT 1 (könsheterogenitet -> confidence medium): Bennmarker m.fl. R 2005:16 fann att 2001/02 års höjning 'påverkade männen, men inte kvinnorna' (kvinnorna fick tvärtom kortare arbetslöshetstider); R 2013:10 verkar via lönebildningen ('en mindre generös a-kassa håller tillbaks löneökningarna vilket i sin tur förmodligen påverkar sysselsättningen positivt' — notera 'förmodligen'). KAVEAT 2 (magnitud delvis simuleringsbaserad -> effect_strength medium): R 2008:12:s +1,5 procentenheter bygger på 'två hypotetiska förändringar av a-kassereglerna' (simulering/kontrafaktisk beräkning på svenska data), och ingen svensk ex-post-utvärdering av prop. 2023/24:128-designen finns ännu (lagen träder i kraft 2025-10-01). Riktning robust över flera IFAU-studier, magnitud osäker. SPEGELPOST/METODNEUTRALITET (codex-krav): liggaren kodar samtidigt inkomststarkande_hushallspolitik positivt på hushallens_reala_disponibla_inkomst (där HÖJDA transfereringar är rätt håll för den indikatorn) — B mäter instrumentell träffsäkerhet PER indikator, inte ideologisk metodpreferens; båda blocken kan få plus via sina respektive instrument. Partiståndpunkter: nedtrappad_ersattningsprofil_akassa (votering bet. 2023/24:AU9 punkt 1, 283 Ja / 20 Nej: 7 supports S/M/SD/C/KD/L/MP, V opposes).
- **Påverkar partier:** C(+), KD(+), L(+), M(+), MP(+), S(+), SD(+), V(−)
- **OK?** ⬜ (✅/✏️/❌): 

## forsvar

### `ateraktiverad_utokad_varnplikt` → personal_varnpliktiga

- **Riktning:** positive · **evidensnivå:** authority_evaluation · **styrka:** medium · **konfidens:** high
- **Källa:** Riksrevisionen RiR 2022:19, Expansion utan prioritet – personalförsörjningen
- **URL:** https://www.riksrevisionen.se/granskningar/granskningsrapporter/2022/expansion-utan-prioritet---personalforsorjningen-av-kontinuerligt-tjanstgorande-gruppbefal-soldater-och-sjoman.html
- **Not:** Återinförd värnplikt vidgade rekryteringsbasen och ökade antalet grundutbildade.
- **Påverkar partier:** C(+), KD(+), L(+), M(+), S(+), SD(+), V(+)
- **OK?** ⬜ (✅/✏️/❌): 

### `internationella_materielsamarbeten` → leveranstid_materiel

- **Riktning:** negative · **evidensnivå:** authority_evaluation · **styrka:** medium · **konfidens:** medium
- **Källa:** Riksrevisionen RiR 2011:13, Leverans på utsatt tid? Försvarets internationella materielsamarbeten
- **URL:** https://www.riksrevisionen.se/granskningar/granskningsrapporter/2011/leverans-pa-utsatt-tid-en-granskning-av-forsvarets-internationella-materielsamarbeten.html
- **Not:** Materielsamarbeten leder inte tillförlitligt till leverans på utsatt tid (förseningar vanliga).
- **Påverkar partier:** —(ingen ståndpunkt)
- ⚠ negativ riktning (vänder semantiken)
- **OK?** ⬜ (✅/✏️/❌): 

### 🚫 `tydlig_statlig_styrning_civilt_forsvar` → civil_beredskap_niva

- **Riktning:** positive · **evidensnivå:** authority_evaluation · **styrka:** low · **konfidens:** low
- **Källa:** Riksrevisionen RiR 2025:4, Den statliga styrningen av det civila försvarets uppbyggnad
- **URL:** https://www.riksrevisionen.se/granskningar/granskningsrapporter/2025/den-statliga-styrningen-av-det-civila-forsvarets-uppbyggnad.html
- **Not:** Otydliga mandat och svag finansiering bromsade uppbyggnaden -> tydligare styrning behövs.
- **Utlyft, skäl:** UTLYFT 2026-08-23 (#26, ADR 0006 punkt 2 och 5): faller på den symmetriska evidensgrinden, rubriken §5. Posten raderas INTE - källspåret står kvar - men hålls utanför claims och täckningsnämnaren. Faller på §5.2: confidence är low. RiR 2025:4 är en styrningsgranskning, och 'tydligare styrning behövs' är en rekommendation, inte en uppmätt verkan på civil_beredskap_niva.
- **Skulle ha påverkat partier:** L(+), M(+), S(+), SD(+), V(+)
- 🚫 UTLYFT — matar inte B · ⚠ låg konfidens
- **OK?** ⬜ (✅/✏️/❌): 

### `nato_medlemskap` → nato_interoperabilitet

- **Riktning:** positive · **evidensnivå:** authority_evaluation · **styrka:** high · **konfidens:** high
- **Källa:** Försvarsberedningen, Ds 2024:6 'Stärkt försvarsförmåga – Sverige som allierad'. Partiståndpunkter via votering bet. 2022/23:UU16 punkt 1 (godkänner Sveriges anslutning till Nato, prop. 2022/23:74).
- **URL:** https://data.riksdagen.se/dokument/HCB46.html
- **Not:** NEUTRALT ANKARE = Försvarsberedningen (blocköverskridande beredningsorgan): Nato-medlemskap 'ökar säkerheten för Sverige och stärker Nato som helhet'; 'det kollektiva försvarsåtagandet i Nato utgör nu en central del i den svenska säkerhets- och försvarspolitiken' och ger 'interoperabilitet och förmåga att operativt agera gemensamt med andra'. Medlemskapet är det grundläggande instrumentet för nato_interoperabilitet (UPP) -> direction positive (nära definitionellt) -> effect_strength/confidence high. MP-NOT (codex-granskat 2026-06-06): MP röstade Nej 2022 men har sedan svängt till Nato-stöd -> MP kodas none (ej opposes), då ett negativt B från en föråldrad position vore vilseledande för en app som guidar dagens röst. V (fortsatt Nato-kritiskt = aktuellt) kodas opposes.
- **Påverkar partier:** C(+), KD(+), L(+), M(+), S(+), SD(+), V(−)
- **OK?** ⬜ (✅/✏️/❌): 

### 🚫 `upptrappning_forsvarsanslag_mot_mal` → forsvarsfinansiering_upptrappning_mot_mal

- **Riktning:** positive · **evidensnivå:** authority_evaluation · **styrka:** low · **konfidens:** low
- **Källa:** Försvarsberedningen Ds 2024:6 'Stärkt försvarsförmåga – Sverige som allierad' + prop. 2024/25:34 'Totalförsvaret 2025–2030'. Partiståndpunkter via enhälligt bet. 2024/25:FöU2 punkt 1 (Mål för totalförsvaret) + punkt 5 (Framtida ekonomisk inriktning), båda acklamation.
- **URL:** https://data.riksdagen.se/dokument/HC01FöU2.html
- **Not:** TILLAGD 2026-06-07 (B-grön-svepet, enhällighet-som-källa §5.2, FLAGGAD low/low; codex BUILD-WITH-CHANGES). INSTRUMENT (snävt, codex-krav): ÅTAGANDE att fullfölja den BESLUTADE totalförsvars-finansieringsbanan UPP MOT den beslutade målnivån (Försvarsberedningens planeringsram som 'syftar till att nå 2 procent av BNP fr.o.m. budgetåret 2028') -> ekonomisk ambitionsnivå/långsiktig finansiering UPP. EJ 'mer pengar alltid bättre', EJ budgetmagnitud (delpoäng A/a1-dubbelräkning), EJ materiel/personal (militar_formaga). INSTRUMENT-MEKANISM (FöU2, ur Ds 2024:6): 'det krävs betydande tillskott till anslagen för det militära försvaret under perioden 2025–2030 för att nå planeringsramen som syftar till att nå 2 procent av BNP fr.o.m. budgetåret 2028'. KAVEAT (LOW/LOW): design-/mekanismevidens (beredningsorgan + proposition), ingen ex-post-utvärdering av att åtagandet mätt höjt förmågan. KONSENSUS-MÅTT (icke-rankningsdrivande): bet. 2024/25:FöU2 p1 + p5 båda ACKLAMATION (verifierat dokumentstatus); benchmark är en BESLUTAD målnivå (ej öppen utgiftspreferens); MP:s enda p5-reservation vill MER (uppåt), inget parti reserverar MOT att nå målnivån -> alla 8 supports. Target-indikatorn forsvarsanslag_andel_bnp behålls som kontext.
- **Utlyft, skäl:** UTLYFT 2026-08-23 (#26, ADR 0006 punkt 2 och 5): faller på den symmetriska evidensgrinden, rubriken §5. Posten raderas INTE - källspåret står kvar - men hålls utanför claims och täckningsnämnaren. Faller på §5.2: confidence är low. Källan är ett åtagande om en beslutad finansieringsbana, inte en utvärdering av vad banan gör med indikatorn. Nio av de 13 utlyfta posterna kom ur B-grön-svepet, vars mandat var minst en post med positiv verkan per undermått. Mandatet är avvecklat (ADR 0006 punkt 3). Återöppningstrigger: en officiell utvärdering som mäter instrumentets verkan på exakt indikatorn och som bär confidence minst medium.
- **Skulle ha påverkat partier:** C(+), KD(+), L(+), M(+), MP(+), S(+), SD(+), V(+)
- 🚫 UTLYFT — matar inte B · ⚠ låg konfidens
- **OK?** ⬜ (✅/✏️/❌): 

### `dca_avtal_usa` → nato_interoperabilitet

- **Riktning:** positive · **evidensnivå:** authority_evaluation · **styrka:** medium · **konfidens:** high
- **Källa:** Försvarsberedningen, Ds 2024:6 'Stärkt försvarsförmåga – Sverige som allierad' (april 2024). Partiståndpunkter via riksdagens godkännande av DCA-avtalet, bet. 2023/24:UFöU1 punkt 1 (prop. 2023/24:141), beslut 2024-06-18, korroborerat via följdvoteringarna punkt 5 och punkt 3 (samma betänkande) samt V:s och MP:s avvikande meningar i Ds 2024:6 bilaga 4.
- **URL:** https://data.riksdagen.se/dokument/HCB46.html
- **Not:** TILLAGD 2026-06-12 (B3 differentiering, beslutsunderlag B1, v0→v1 AVFLAGGAD 2026-06-14 efter mänsklig slutgranskning — tre Codex-villkoren verifierade uppfyllda; byggd på användar-sign-off med Codex-villkoren). NEUTRALT ANKARE = Försvarsberedningen (blocköverskridande beredningsorgan), samma källa som nato_medlemskap. INSTRUMENT-EXAKTA UTSAGOR (Ds 2024:6, ordagrant omverifierade mot fulltexten 2026-06-12): 'Avtalet utgör en förutsättning för ett mer kontinuerligt operativt försvarssamarbete genom att lägga fast förutsättningarna för amerikanska styrkor i Sverige'; 'DCA skapar förutsättningar för amerikanskt militärt stöd om säkerhetsläget så kräver och är således av stor betydelse för Sveriges säkerhet och säkerheten i Sveriges närområde'; 'DCA-avtalet är stabiliserande, höjer tröskeln för angrepp mot Sverige och blir viktigt för försvaret i norra Europa'; avtalets innehåll: 'Avtalet reglerar bland annat den rättsliga statusen för amerikansk militär personal vid närvaro i Sverige, tillträde till svenska militära anläggningar, förhandslagring av materiel och frågor om tullar och skatter.' -> kontinuerligt operativt samarbete med allierad stormakt + förhandslagring + rättsliga förutsättningar driver nato_interoperabilitet UPP -> direction positive. ANTI-STACKNINGS-NOT (Codex-villkor 1): dca_avtal_usa och nato_medlemskap är TVÅ DISTINKTA INSTRUMENT på samma indikator — DCA är ett BILATERALT försvarssamarbets-/basavtal med USA (rättslig status för amerikansk personal, tillträde till 17 överenskomna anläggningar och områden enligt avtalsbilagan i prop. 2023/24:141, förhandslagring av materiel, förutsättningar för kontinuerligt operativt samarbete), medan nato_medlemskap är ett MULTILATERALT alliansmedlemskap (kollektivt försvarsåtagande, art. 5). Ett parti kan logiskt stödja det ena och motsätta sig det andra (MP gör exakt detta: stödjer i dag Nato-medlemskapet men röstade nej till DCA). Prejudikat för flera instrument per indikator: territoriella_utslapp (reduktionsplikt + koldioxidskatt). V får härmed sin ANDRA opposes-post på indikatorn — sign-off:ad avvägning 2026-06-12 (differentieringsvinsten att MP:s första aktuella position på indikatorn kodas vägde tyngre än V-stackningsrisken; V:s båda nej är dessutom sakligt distinkta ställningstaganden till två olika instrument). GRADERING: effect_strength medium (EJ high som nato_medlemskap): DCA är ett förutsättningsskapande KOMPLEMENT till medlemskapet ('utgör en förutsättning för', 'skapar förutsättningar för'), inte det grundläggande instrumentet för interoperabilitet; confidence high: Försvarsberedningens bedömning är entydig i riktning och blocköverskridande. KÄLLHÄNVISNINGSKONSTRUKTION FÖR HUVUDVOTERINGEN p1 (Codex-villkor 2): huvudvoteringen (bet. 2023/24:UFöU1 punkt 1, 2024-06-18, 266 Ja / 37 Nej, kvalificerad majoritet enligt 10 kap. 6 § andra stycket RF — betänkandet ordagrant: beslutet 'ska fattas med minst tre fjärdedels majoritet av de röstande, och mer än hälften av riksdagens ledamöter måste rösta för förslaget') finns INTE i voteringlista-API:t — verifierat live 2026-06-12: voteringlista rm=2023/24 bet=UFöU1 punkt=1 ger @antal=0, och dokumentstatus HB01UFöU1 visar för punkt 1 beslutstyp 'röstning' och vinnare 'utskottet' men TOMT votering_id (API-lucka, ej acklamation). Källhänvisning därför via riksdagens officiella beslutsnotis/dokumentstatus HB01UFöU1 ('Kammaren biföll utskottets förslag'; förslag till riksdagsbeslut p1: 'Riksdagen godkänner avtalet om försvarssamarbete mellan Konungariket Sveriges regering och Amerikas förenta staters regering (DCA-avtalet) och antar regeringens lagförslag.') + korroboration från följdvoteringarna i SAMMA betänkande, båda OMVERIFIERADE LIVE via data.riksdagen.se/voteringlista (gruppering parti) 2026-06-12: punkt 5 'Nedrustning' (votering A1C914E0-4544-4389-A757-A5BEDDACBFD9, 2024-06-18): 266 Ja (S 93, M 60, SD 63, C 21, KD 16, L 13) / 37 Nej (V 20, MP 15, 2 partilösa) — exakt samma 266/37-konstellation som huvudvoteringen; punkt 3 'Kärnvapen' (votering A52E4273-06BE-4869-9C8D-078E3607B40F): V 20 Nej, MP 15 Avstår. STANCE-CONFIDENCE (Codex-villkor 3): max medium på alla p1-härledda partirader (huvudvoteringens partifördelning är härledd via beslutsnotis + följdvoteringskorroboration, ej direkt ur roll-call-API). Partiståndpunkter: dca_avtal_usa (bet. 2023/24:UFöU1 punkt 1: 6 supports S/M/SD/C/KD/L; V opposes — avvikande mening Ds 2024:6 bilaga 4 'Vänsterpartiet är motståndare till det så kallade DCA-avtalet' + nej-röst; MP opposes — avvikande mening bilaga 4 'Miljöpartiet kommer att rösta nej till avtalet' + nej-röst; villkorat nej, se mapping_note).
- **Påverkar partier:** C(+), KD(+), L(+), M(+), MP(−), S(+), SD(+), V(−)
- **OK?** ⬜ (✅/✏️/❌): 

## integration

### `sfi_kombinerat_med_praktik` → sysselsattningsgap_inrikes_utrikes

- **Riktning:** positive · **evidensnivå:** authority_evaluation · **styrka:** medium · **konfidens:** high
- **Källa:** IFAU, forskningssammanfattning 'Utrikes föddas etablering på arbetsmarknaden' (refererar Dahlberg m.fl. 2020); BEKRÄFTAD av IFAU R 2023:19 'Etablering av nyanlända flyktingar' (Dahlberg/Egebark/Vikman, RCT-uppföljning 4 år av samma Göteborgs-försök)
- **URL:** https://www.ifau.se/Press/Forskningssammanfattningar/Utrikes-foddas-eta-pa-arbetsmarknaden-/
- **Not:** EXPERTUPPGRADERING 2026-06-05 (ersätter generisk seed-källa): IFAU sammanfattar att 'Genom intensiv språkutbildning, arbetspraktik samt sök- och matchningshjälp dubblerades sysselsättningen bland lågutbildade nyanlända' (Dahlberg m.fl. 2020) -> kombinerad sfi + praktik höjer sysselsättningen för utrikes födda (minskar gapet). UPPGRADERAD 2026-06-07 (användarbeslut, version ej bumpad -> sign-off) confidence medium->high: IFAU R 2023:19 (RCT i Göteborg, 140 lottade) är 4-årsuppföljningen av SAMMA försök och visar att effekten BESTÅR — behandlingsgruppen har '10-20 procentenheter högre sysselsättning under flera år efter att insatsen avslutats' och jämförelsegruppen kommer ifatt först >3 år senare (kortsiktigt ~+15 p.e. = fördubbling). Inte längre 'bara en pilot' -> RCT med varaktig effekt -> confidence high (effect_strength kvar medium: ett försöksområde/pilotskala, ej nationell utrullning). PDF: https://www.ifau.se/globalassets/pdf/se/2023/r2023-19-etablering-av-nyanlanda-flyktingar.pdf . DUBBELRÄKNINGS-SPÄRR: R 2023:19 konsumeras HÄR som bekräftande källa — den får ALDRIG byggas som eget B-instrument (det vore samma Dahlberg-Göteborgs-RCT räknad två gånger).
- **Påverkar partier:** C(+), KD(+), L(+), M(+), S(+)
- **OK?** ⬜ (✅/✏️/❌): 

### `aktiveringskrav_ekonomiskt_bistand` → bidragsberoende

- **Riktning:** positive · **evidensnivå:** authority_evaluation · **styrka:** medium · **konfidens:** high
- **Källa:** IFAU, utvärdering av aktiveringskrav för socialbidragstagare (Stockholms stadsdelar)
- **URL:** https://www.ifau.se/Press/Pressmeddelanden/Krav-pa-aktivering-av-socialbidragstagare-ger-fler-sysselsatta/
- **Not:** Aktiveringskrav minskade bidragstagande ~5,6 % och ökade sysselsättning, starkast för utomvästligt födda.
- **Påverkar partier:** C(+), KD(+), L(+), M(+), S(+), SD(+), V(−)
- **OK?** ⬜ (✅/✏️/❌): 

### `aktiveringskrav_ekonomiskt_bistand` → sysselsattningsgap_inrikes_utrikes

- **Riktning:** positive · **evidensnivå:** authority_evaluation · **styrka:** medium · **konfidens:** medium
- **Källa:** IFAU, utvärdering av aktiveringskrav för socialbidragstagare
- **URL:** https://www.ifau.se/Press/Pressmeddelanden/Krav-pa-aktivering-av-socialbidragstagare-ger-fler-sysselsatta/
- **Not:** Störst sysselsättningseffekt för utomvästligt födda -> talar för minskat gap för utrikes födda.
- **Påverkar partier:** C(+), KD(+), L(+), M(+), S(+), SD(+), V(−)
- **OK?** ⬜ (✅/✏️/❌): 

### `sprakpraktik_kombinerad_sprakutbildning_och_arbetspraktik` → sysselsattningsgap_inrikes_utrikes

- **Riktning:** positive · **evidensnivå:** authority_evaluation · **styrka:** medium · **konfidens:** medium
- **Källa:** IFAU, utvärdering av språkpraktik med modersmålsstöd
- **URL:** https://www.ifau.se/Press/Pressmeddelanden/sprakpraktik-med-stod-pa-modersmal-gav-fler-kvinnor-jobb/
- **Not:** Språkpraktik höjde sysselsättning för utrikes födda, tydligt för kvinnor, ingen mätbar effekt för män.
- **Påverkar partier:** C(+), KD(+), MP(+), V(+)
- **OK?** ⬜ (✅/✏️/❌): 

### `riktade_insatser_nyanlanda_elever` → skolresultat_utsatta_omraden

- **Riktning:** positive · **evidensnivå:** authority_evaluation · **styrka:** medium · **konfidens:** high
- **Källa:** Skolverket (2026), referat av IFAU-utvärdering av riktade insatser 2016–2019
- **URL:** https://www.skolverket.se/om-skolverket/nyheter-och-pressmeddelanden/nyheter/nyheter/2026-01-30-riktade-insatser-forbattrade-utrikesfodda-elevers-kunskapsresultat
- **Not:** Riktade insatser i kommuner med många nyanlända gav bestående bättre provresultat, störst för utrikes födda.
- **Påverkar partier:** C(+), KD(+), L(+), M(+), SD(+), V(+)
- **OK?** ⬜ (✅/✏️/❌): 

### `se_over_ansvarsfordelning_atervandande` → atervandande_effektivitet

- **Riktning:** positive · **evidensnivå:** authority_evaluation · **styrka:** medium · **konfidens:** medium
- **Källa:** Riksrevisionen RiR 2020:7 'Återvändandeverksamheten – resultat, kostnader och effektivitet' (riksdagens spegel dok H8B57). Partiståndpunkter via bet. 2020/21:SfU6 punkt 2 (votering C7DEF4C6-4668-4D8E-AF06-7A820A666C39).
- **URL:** https://www.riksrevisionen.se/granskningar/granskningsrapporter/2020/atervandandeverksamheten---resultat-kostnader-och-effektivitet.html
- **Not:** TILLAGD 2026-06-07 (integration-svepet, NY INDIKATOR §5.7, FLAGGAD; codex KEEP-WITH-CHANGES). INSTRUMENT (snävt, codex-krav): att SE ÖVER/reformera ansvarsfördelningen för återvändandeverksamheten (Migrationsverket/Polis/Kriminalvården) -> atervandande_effektivitet UPP. EJ den starkare 'samla allt ansvar'-tesen (som RiR inte slår fast) -> policy_type bytt till se_over_ansvarsfordelning_atervandande. SYSTEMFUNKTION, EJ VOLYM: mäter kostnad/effektivitet PER verkställt beslut (att lagakraftvunna beslut verkställs effektivt) — ALDRIG antal utvisningar/'fler = bra'. INSTRUMENT-MEKANISM (RiR 2020:7, ordagrant): kostnaden per verkställd person har 'ökat från cirka 48 000 kronor 2016 till knappt 97 000 kronor 2018'; styrningen beskrivs som 'svag, otydlig och splittrad'. INSTRUMENT-GRIND: RiR REKOMMENDERAR uttryckligen att 'se över myndigheternas uppdrag och ansvarsfördelning, samt överväga förändring av myndighetsorganisationen på området' — claimet hålls vid DENNA nivå (se över/överväga). direction positive (ej en §10-negativ-post; framställs ej som negativ-evidens-vinkel). KAVEAT (effect_strength/confidence=MEDIUM, ej high): RiR belägger problemet starkt + rekommenderar översynen, men ingen ex-post-utvärdering bevisar att omorganisation RÄCKER (S/MP-reservation 3 invänder just detta). TIDSNOT (§10.5): primärkällan är 2020/21 -> partiernas NUVARANDE hållning är EJ bevisad här; flaggas för tidskontroll vid sign-off (M/KD/L/SD-riktningen är förenlig med Tidöavtalet 2022). EJ enhällighet: tvåsidig split. NEUTRALITET (verifierat mot SfU6 votering C7DEF4C6 + betänkandetext 2026-06-07): tillkännagivandet 'tillsätta en utredning som ser över ansvarsfördelningen' vanns MOT sittande S/MP-regering; C+L (då i Januari-samarbete med S) röstade JA med oppositionen -> ej rent regering-vs-opp; V avstod (ej med S/MP) -> ej ren vänster-höger-axel. Röster p2: S 1ja/15nej, M 11, SD 10, C 5, V 4avst, KD 3, L 3, MP 3nej.
- **Påverkar partier:** C(+), KD(+), L(+), M(+), MP(−), S(−), SD(+)
- **OK?** ⬜ (✅/✏️/❌): 

### `uppsokande_forskoleerbjudande_nyanlandas_barn` → skolresultat_utsatta_omraden

- **Riktning:** positive · **evidensnivå:** authority_evaluation · **styrka:** medium · **konfidens:** medium
- **Källa:** SOU 2020:67 'Förskola för alla barn – för bättre språkutveckling i svenska'. Instrument/lag: prop. 2021/22:132 'Förskola för fler barn' (skollagen 8 kap. 12 a–12 c §§), bet. 2021/22:UbU24. Partiståndpunkter via votering bet. 2021/22:UbU24 punkt 1.
- **URL:** https://www.regeringen.se/rattsliga-dokument/statens-offentliga-utredningar/2020/11/sou-202067/
- **Not:** TILLAGD 2026-06-12 (B3 differentiering, v0→v1 AVFLAGGAD 2026-06-14 efter mänsklig slutgranskning, behåll oförändrad; codex BUILD-WITH-CHANGES). INSTRUMENT (prop. 2021/22:132-designen, ur SOU 2020:67 avsnitt 7.4/7.5/8): (1) UPPSÖKANDE VERKSAMHET — hemkommunen skyldig att 'genom uppsökande verksamhet ta kontakt med vårdnadshavare till de barn som inte har en plats i förskolan och informera om förskolans syfte och barnets rätt till förskola' från hösten det år barnet fyller 3 år (skollagen 8 kap. 12 a §); (2) DIREKT/OBLIGATORISKT FÖRSKOLEERBJUDANDE för nyanländas barn — 'obligatoriskt för hemkommunen att erbjuda förskola till barn som har bott i Sverige kort tid eller som har vårdnadshavare som har bott i Sverige kort tid', med 'en reserverad förskoleplats även utan att vårdnadshavarna har anmält önskemål om det' från 3 års ålder (12 b–12 c §§). Citaten ordagrant ur bet. UbU24/propositionen (omverifierade 2026-06-12). INDIKATOR-BRYGGA (källbelagd; SAMMA brygga som befintliga riktade_insatser_nyanlanda_elever, vars evidens om utrikes födda/nyanlända elever kodas på skolresultat_utsatta_omraden): propositionen/utskottet ordagrant — deltagande i förskolan 'kan vara avgörande för språkutvecklingen i svenska. Detta framhålls särskilt gälla utrikes födda barn, barn med annat modersmål än svenska och barn med en svag socioekonomisk bakgrund'; 'det finns en bred samsyn inom forskningen att förskolan har störst betydelse för barn med svag socioekonomisk bakgrund (se t.ex. källor i betänkande SOU 2020:67)'; 'Bland de barn som inte går i förskolan är barn med svag socioekonomisk bakgrund och barn med utländsk bakgrund överrepresenterade' -> instrumentet riktar förskoledeltagande mot exakt de grupper (nyanländas/utrikes föddas barn, svag socioekonomisk bakgrund) som bär indikatorn skolresultat_utsatta_omraden. KAVEAT (effect_strength/confidence=medium): design-/mekanismevidens (statlig utredning + bred forskningssamsyn om förskolans betydelse för målgruppen), INGEN svensk ex-post-utvärdering av själva lagändringen ännu — lagen i kraft 2022-07-01, tillämpas första gången på utbildning som påbörjas efter 2023-07-01. REJECTED-CANDIDATE-NOTE (SD/KD kodas INTE — ej opposes; codex-krav, MP/Nato-prejudikatet): SD+KD röstade Nej på UbU24 punkt 1 2022 (avslagsreservation mot prop-132-designen), men Tidö-regeringens dir. 2024:113 (utredning U 2024:04 om bl.a. obligatorisk språkförskola för 5-åringar) visar att SD/KD i dag stödjer ett SNÄVARE instrument i samma familj (obligatoriskt förskoledeltagande för språksvaga/nyanländas barn) -> 2022-nejet är sannolikt föråldrat som mått på dagens hållning, men dir. 2024:113 är inte instrument-exakt för 12 a–12 c §§ -> SD/KD utelämnas (none = 'vet ej', ingen rad) tills en instrument-exakt aktuell källa finns. En föråldrad position ska inte ge negativt B (prejudikat: MP/nato_medlemskap). TIDSREGEL (§4): votering rm 2021/22 = en session före föredragen period (2022/23–2025/26); ingen nyare votering om samma instrument finns (U 2024:04 redovisas dec 2025, ej lagstiftad) — symmetriskt dokumenterat, gäller alla 6 kodade partier lika. Partiståndpunkter: uppsokande_forskoleerbjudande_nyanlandas_barn (votering bet. 2021/22:UbU24 punkt 1, 228 Ja / 70 Nej: 6 supports S/M/C/V/L/MP; SD/KD ej kodade).
- **Påverkar partier:** C(+), L(+), M(+), MP(+), S(+), V(+)
- **OK?** ⬜ (✅/✏️/❌): 

## klimat

### `reduktionsplikt_drivmedel` → territoriella_utslapp

- **Riktning:** positive · **evidensnivå:** authority_evaluation · **styrka:** medium · **konfidens:** medium
- **Källa:** Naturvårdsverket, officiell klimatstatistik / pressmeddelande om 2024 års utsläpp (2025)
- **URL:** https://www.naturvardsverket.se/om-oss/aktuellt/nyheter-och-pressmeddelanden/2025/juni/sveriges-klimatutslapp-okade-med-7-procent-under-2024/
- **Not:** Naturvårdsverket tillskriver 2024 års utsläppsökning (~7 %) sänkt reduktionsplikt -> högre plikt sänker transportutsläpp.
- **Påverkar partier:** C(+), KD(−), L(−), M(−), MP(+), S(+), SD(−), V(+)
- **OK?** ⬜ (✅/✏️/❌): 

### `koldioxidskatt` → territoriella_utslapp

- **Riktning:** positive · **evidensnivå:** authority_evaluation · **styrka:** medium · **konfidens:** medium
- **Källa:** Riksrevisionen RiR 2012:1, Klimatrelaterade skatter – Vem betalar?
- **URL:** https://www.riksdagen.se/sv/dokument-och-lagar/dokument/riksrevisionens-granskningsrapport/klimatrelaterade-skatter-vem-betalar_h0b51/html/
- **Not:** Koldioxidskatt centralt styrmedel; prissättning av utsläpp minskar utsläpp i icke-handlande sektorn.
- **Påverkar partier:** KD(+), L(+), M(+), MP(+), SD(−), V(+)
- **OK?** ⬜ (✅/✏️/❌): 

### `koldioxidskatt` → utslappsminskning_per_krona

- **Riktning:** positive · **evidensnivå:** authority_evaluation · **styrka:** medium · **konfidens:** medium
- **Källa:** Riksrevisionen RiR 2012:1, Klimatrelaterade skatter – Vem betalar?
- **URL:** https://www.riksdagen.se/sv/dokument-och-lagar/dokument/riksrevisionens-granskningsrapport/klimatrelaterade-skatter-vem-betalar_h0b51/html/
- **Not:** Enhetlig koldioxidskatt kostnadseffektiv (utsläppsminskning till lägre samhällskostnad); ojämn tillämpning sänker effektiviteten.
- **Påverkar partier:** KD(+), L(+), M(+), MP(+), SD(−), V(+)
- **OK?** ⬜ (✅/✏️/❌): 

### `klimatinvesteringsstod_klimatklivet` → utslappsminskning_per_krona

- **Riktning:** negative · **evidensnivå:** authority_evaluation · **styrka:** medium · **konfidens:** medium
- **Källa:** Riksrevisionen RiR 2019:1, Klimatklivet – stöd till lokala klimatinvesteringar (beslutad 2019-01-09)
- **URL:** https://www.riksdagen.se/sv/dokument-och-lagar/dokument/riksrevisionens-granskningsrapport/klimatklivet-stod-till-lokala_h7b51/html/
- **Not:** INDIKATOR-BRYGGA (§5.3): ingen brygga behövs. Indikatorn är utsläppsminskning per krona (riktning up); Riksrevisionen mäter marginalkostnad i kronor per kilo koldioxid, alltså samma storhet inverterad. FYND: 'Klimatklivet [är] inte en del av en kostnadseffektiv styrmedelskombination för att nå det svenska klimatmålet till 2030'; marginalkostnaden blir ca 6,6 kr/kg CO2 för biogaskedjan och drygt 8,5 kr/kg för laddstationer när dubbelräkning, bristande additionalitet och samverkan med andra styrmedel räknas in, mot Naturvårdsverkets egna 1-4 kr/kg; 'klimatmålet skulle kunna uppnås till lägre marginalkostnad'. NYANS som håller styrka och confidence på medium i stället för högre: Riksrevisionen 2025 (Statens insatser för jordbrukets klimatomställning) finner att Klimatklivet bidrar till minskade jordbruksutsläpp till en kostnad under eller i nivå med koldioxidskatten — ett smalare utsnitt än RiR 2019:1, som bedömer stödet som helhet.
- **Påverkar partier:** —(ingen ståndpunkt)
- ⚠ negativ riktning (vänder semantiken)
- **OK?** ⬜ (✅/✏️/❌): 

### `ny_karnkraft` → effektbrist

- **Riktning:** positive · **evidensnivå:** authority_evaluation · **styrka:** high · **konfidens:** high
- **Källa:** Svenska kraftnät, Kraftbalansen på den svenska elmarknaden – rapport 2025 (lagstadgad rapport till regeringen, 3 § förordn. 2007:1119)
- **URL:** https://www.svk.se/49bb53/siteassets/om-oss/rapporter/2025/kraftbalansen-pa-den-svenska-elmarknaden-rapport-2025.pdf
- **Not:** Exakt på indikatorn effektbrist (effektbalans vid topplasttimmen). Planerbar baskraft har tillgänglighetsfaktor ~90 % vid topplast (vindkraft 9 %, solkraft 0 %, Tabell 13 s.45), så ny/utbyggd planerbar kärnkraft ökar tillgänglig effekt vid topplast och drar effektbrist-risken nedåt. POSITIV riktning (negativ-grinden ej tillämplig). Källan fastställer riktningsmekanismen via tillgänglighetsfaktorer, ej nybyggnadskostnad/ledtid; ett parti som motsätter sig instrumentet (opposes) får negativt B-bidrag på effektbrist — flaggat för mänsklig granskning. KÄLLTYPS-ASYMMETRI (expertgranskning 2026-06-05, SUSPECT 4): ny_karnkraft kodar partiets GENERELLA hållning till ny/utbyggd kärnkraft. supports-raderna (M/SD/KD/L) är generella partimotioner från olika riksmöten (2020/21–2024/25); opposes-raderna (V/MP) är följdmotioner mot prop 2025/26:160. Jämförelsen avser alltså för/emot ny kärnkraft generellt — inte en röst om just prop 160. Bekräftat ordagrant + rätt riktade i adversariell omverifiering.
- **Påverkar partier:** KD(+), L(+), M(+), MP(−), S(+), SD(+), V(−)
- **OK?** ⬜ (✅/✏️/❌): 

### 🚫 `atgarder_mot_invasiva_frammande_arter` → hotade_arter_naturforlust

- **Riktning:** positive · **evidensnivå:** authority_evaluation · **styrka:** low · **konfidens:** low
- **Källa:** Naturvårdsverket, ämnesområde 'Invasiva främmande arter' (myndighetsbedömning). Instrument/beslut: prop. 2025/26:41, bet. 2025/26:MJU13 punkt 1 (skärpt regelverk: miljöbalken + inregränslagen).
- **URL:** https://www.naturvardsverket.se/amnesomraden/invasiva-frammande-arter/
- **Not:** TILLAGD 2026-06-06 (B2, enhällighet-som-källa). Åtgärder mot invasiva främmande arter (EU-förordn. 1143/2014 + nationellt regelverk: nationell förteckning, straffansvar för otillåten hantering, anmälningsskyldighet + Tullverkets kontroll vid inre gräns, tidig upptäckt) -> hotade_arter_naturforlust NER (positiv riktning). INSTRUMENT-MEKANISM (svar på codex instrument-precisions-invändning 2026-06-06): Naturvårdsverket anger att förteckningen är 'ett verktyg i arbetet med att förebygga och begränsa spridningen av arter som kan orsaka skador på natur, biologisk mångfald och ekosystem', och prop. 2025/26:41 (i MJU13) att 'det mest kostnadseffektiva sättet att förhindra introduktion av invasiva främmande arter är att de upptäcks i ett tidigt skede' -> instrumentet driver indikatorn via mekanismen förhindra spridning/introduktion. Naturvårdsverkets rubrikbedömning: 'Invasiva främmande arter är ett av de största hoten mot biologisk mångfald i Sverige och globalt.' KAVEAT (effect_strength/confidence=LOW, codex-kalibrerat 2026-06-06): riktningen är myndighetsbelagd på MEKANISM-nivå men det finns INGEN kvantifierad svensk kausalutvärdering av åtgärdernas faktiska utfall på hotade arter -> låg styrka/förtroende. KONSENSUS-MÅTT: positioneras via enhälligt bet. 2025/26:MJU13 punkt 1 (acklamation, 'inte väckts någon motion som går emot regeringens lagförslag') -> alla 8 partier supports; tiltade avslagspunkten (p2) utesluten. SIGN-OFF 2026-06-12 (beslutsunderlag H5, VAL A): BEHÅLL + AVFLAGGAD, version 0 -> 1 — konsensus-mått (alla 8 supports) kan inte tilta; low/low kvarstår tills kvantifierad svensk kausalutvärdering finns.
- **Utlyft, skäl:** UTLYFT 2026-08-23 (#26, ADR 0006 punkt 2 och 5): faller på den symmetriska evidensgrinden, rubriken §5. Posten raderas INTE - källspåret står kvar - men hålls utanför claims och täckningsnämnaren. Faller på §5.2: confidence är low. Källan beskriver regelverkets syfte (Naturvårdsverket plus prop. 2025/26:41), inte en uppmätt effekt på hotade_arter_naturforlust. Nio av de 13 utlyfta posterna kom ur B-grön-svepet, vars mandat var minst en post med positiv verkan per undermått. Mandatet är avvecklat (ADR 0006 punkt 3). Återöppningstrigger: en officiell utvärdering som mäter instrumentets verkan på exakt indikatorn och som bär confidence minst medium.
- **Skulle ha påverkat partier:** C(+), KD(+), L(+), M(+), MP(+), S(+), SD(+), V(+)
- 🚫 UTLYFT — matar inte B · ⚠ låg konfidens
- **OK?** ⬜ (✅/✏️/❌): 

## trygghet

### `behandlingsprogram_kriminalvard` → aterfall_i_brott

- **Riktning:** positive · **evidensnivå:** authority_evaluation · **styrka:** medium · **konfidens:** medium
- **Källa:** Kriminalvården, Behandling inom Kriminalvården (ackrediterade behandlingsprogram, KBT-baserade)
- **URL:** https://www.kriminalvarden.se/kriminalvard/behandling-inom-kriminalvarden/
- **Not:** EXPERTUPPGRADERING 2026-06-05 (ersätter generisk seed-källa): Kriminalvården anger att behandling är 'en viktig del i Kriminalvårdens arbete med att minska risken för återfall i brott' och att programmen är ackrediterade via vetenskaplig prövning med forskningsstöd för att de 'kan minska risken för återfall'. NYANS (program-nivå blandad): ETS ~9 % och Brotts-Brytet ~8 % riskminskning ej statistiskt säkerställda, medan PRISM gav signifikant lägre återfall -> riktning positive säker, effect_strength/confidence medium.
- **Påverkar partier:** C(+), KD(+), L(+), M(+), MP(+), S(+), V(+)
- **OK?** ⬜ (✅/✏️/❌): 

### `fokuserad_avskrackning_gvi` → skjutningar_sprangningar

- **Riktning:** positive · **evidensnivå:** systematic_review · **styrka:** medium · **konfidens:** medium
- **Källa:** SBU Rapport 369 (2023), Psykosociala insatser mot gängkriminalitet
- **URL:** https://www.sbu.se/369
- **Not:** Fokuserad avskräckning (GVI) minskar skjutvapenvåld ~26 % (IRR 0,74), måttlig tillförlitlighet.
- **Påverkar partier:** MP(+), S(+), V(+)
- **OK?** ⬜ (✅/✏️/❌): 

### 🚫 `psykosociala_insatser_frivard` → aterfall_i_brott

- **Riktning:** positive · **evidensnivå:** systematic_review · **styrka:** low · **konfidens:** low
- **Källa:** SBU Rapport 369 (2023), Psykosociala insatser mot gängkriminalitet
- **URL:** https://www.sbu.se/369
- **Not:** Psykosociala insatser i frivård kan minska återfall ~1 år (OR 0,56), låg tillförlitlighet.
- **Utlyft, skäl:** UTLYFT 2026-08-23 (#26, ADR 0006 punkt 2 och 5): faller på den symmetriska evidensgrinden, rubriken §5. Posten raderas INTE - källspåret står kvar - men hålls utanför claims och täckningsnämnaren. Faller på §5.2: confidence är low. Nivån räcker (SBU 369 är en systematisk översikt), men SBU anger själv låg tillförlitlighet i underlaget bakom OR 0,56.
- **Skulle ha påverkat partier:** —(ingen ståndpunkt)
- 🚫 UTLYFT — matar inte B · ⚠ låg konfidens
- **OK?** ⬜ (✅/✏️/❌): 

### `situationell_prevention_utomhusbelysning` → brottsutsatthet

- **Riktning:** positive · **evidensnivå:** systematic_review · **styrka:** low · **konfidens:** medium
- **Källa:** Brå Rapport 2007:28, Förbättrad utomhusbelysning och brottsprevention (Welsh & Farrington)
- **URL:** https://bra.se/rapporter/arkiv/2023-02-28-gar-det-att-forebygga-brott-genom-att-forandra-utomhusbelysningen
- **Not:** Bättre belysning minskar brott ~14 % (främst egendomsbrott); ingen säkerställd effekt på våldsbrott.
- **Påverkar partier:** KD(+), L(+), MP(+), SD(+), V(+)
- **OK?** ⬜ (✅/✏️/❌): 

### `situationell_prevention_kamerabevakning` → brottsutsatthet

- **Riktning:** mixed · **evidensnivå:** systematic_review · **styrka:** low · **konfidens:** medium
- **Källa:** Brå, kunskapssammanställning Kamerabevakning och belysning (Welsh & Farrington-meta)
- **URL:** https://bra.se/amnen/kamerabevakning-och-belysning
- **Not:** Effektiv mot planerade egendomsbrott, ingen påtaglig effekt mot våldsbrott (platsspecifikt).
- **Påverkar partier:** —(ingen ståndpunkt)
- ⚠ mixed → ≈neutral B
- **OK?** ⬜ (✅/✏️/❌): 

### `snabbforfarande_lagforing` → handlaggningstid

- **Riktning:** positive · **evidensnivå:** authority_evaluation · **styrka:** medium · **konfidens:** medium
- **Källa:** Brå Rapport 2020:3 'Snabbare lagföring – Utvärdering av en försöksverksamhet i norra Stockholm'. Partiståndpunkter via enhälligt betänkande 2022/23:JuU2 punkt 1 (prop. 2021/22:279), acklamation.
- **URL:** https://bra.se/rapporter/arkiv/2020-04-01-snabbare-lagforing
- **Not:** TILLAGD 2026-06-06 (B2, enhällighet-som-källa). Snabbförfarande/snabbare lagföring KORTAR handläggningstiden i rättskedjan -> handlaggningstid NER (positiv riktning). Brå (kvasiexperiment mot kontrollområde) ordagrant: 'Den totala handläggningstiden från registrerad misstanke till avslut har mer än halverats'; tingsrätt -34 dagar efter justering för tidstrender = 'en minskning med cirka 40 procent' (median från >50 till ~20 dagar). Brås slutsats: 'goda skäl att fortsätta med, och utvidga verksamheten'. KAVEAT (effect_strength/confidence=medium, ej high): ETT försöksområde (norra Stockholm), icke-parallella förtrender flaggade av Brå själv, 'bör inte förvänta sig samma resultat överallt'. Riktning entydig. KONSENSUS-MÅTT (codex 2026-06-06): positioneras via enhälligt bet. 2022/23:JuU2 punkt 1 (acklamation, ingen reservation mot sakinnehållet; enda reservationen V/C/MP gäller punkt 2/påföljd) -> alla 8 partier supports = icke-rankningsdrivande, höjer trygghet-coverage (submåttet rattsvasendets_effektivitet, tidigare B-tomt).
- **Påverkar partier:** C(+), KD(+), L(+), M(+), MP(+), S(+), SD(+), V(+)
- **OK?** ⬜ (✅/✏️/❌): 

### 🚫 `lagstadgat_kommunalt_brottsforebyggande_ansvar` → kommunalt_brottsforebyggande_arbete

- **Riktning:** positive · **evidensnivå:** authority_evaluation · **styrka:** low · **konfidens:** low
- **Källa:** Lagen (2023:196) om kommuners ansvar för brottsförebyggande arbete (ikraft 2023-07-01), prop. 2022/23:43; Brå, 'Kommunens ansvar'. Partiståndpunkter via enhälligt bet. 2022/23:JuU9 punkt 1, acklamation.
- **URL:** https://data.riksdagen.se/dokument/HA01JuU9.html
- **Not:** TILLAGD 2026-06-07 (B-grön-svepet, §5.7 ny indikator + §5.2 enhällighet; codex BUILD). NY INDIKATOR kommunalt_brottsforebyggande_arbete (up) i forebyggande (tidigare utan indikator, §4.2-vägg). INSTRUMENT: lagstadgat krav att varje kommun bedriver kunskapsbaserat, samordnat brottsförebyggande arbete (lägesbild + åtgärdsplan + samordningsfunktion). RIKTNING (ordagrant, prop. 2022/23:43): 'För att säkerställa att kommunerna arbetar med dessa frågor på ett effektivt och kunskapsbaserat sätt föreslår regeringen att kommunernas ansvar för brottsförebyggande arbete regleras i lag.' Brå: 'Syftet med lagen är att stärka kommunernas systematiska brottsförebyggande arbete.' KAVEAT (LOW/LOW): design-/mekanismevidens (lagens syfte), ingen ex-post-effektutvärdering (lagen ny 2023). Mäter förebyggande KAPACITET, ej uppklaring/återfall (ingen dubbelräkning mot rattsvasendets_effektivitet/aterfall_kriminalvard). KONSENSUS-MÅTT (icke-rankningsdrivande): bet. 2022/23:JuU9 p1 ACKLAMATION (verifierat dokumentstatus; enpunkts-betänkande), 'Propositionen har inte lett till några motionsyrkanden eller andra invändningar under utskottsbehandlingen' -> alla 8 supports.
- **Utlyft, skäl:** UTLYFT 2026-08-23 (#26, ADR 0006 punkt 2 och 5): faller på den symmetriska evidensgrinden, rubriken §5. Posten raderas INTE - källspåret står kvar - men hålls utanför claims och täckningsnämnaren. Faller på §5.2: confidence är low. Design- och mekanismevidens ur prop. 2022/23:43 och Brå om lagens syfte; lagen trädde i kraft 2023 och är ännu inte effektutvärderad. Nio av de 13 utlyfta posterna kom ur B-grön-svepet, vars mandat var minst en post med positiv verkan per undermått. Mandatet är avvecklat (ADR 0006 punkt 3). Återöppningstrigger: en officiell utvärdering som mäter instrumentets verkan på exakt indikatorn och som bär confidence minst medium.
- **Skulle ha påverkat partier:** C(+), KD(+), L(+), M(+), MP(+), S(+), SD(+), V(+)
- 🚫 UTLYFT — matar inte B · ⚠ låg konfidens
- **OK?** ⬜ (✅/✏️/❌): 

## valfard

### `tidiga_insatser_lagstadiet` → skolresultat

- **Riktning:** positive · **evidensnivå:** systematic_review · **styrka:** medium · **konfidens:** medium
- **Källa:** Skolforskningsinstitutet, systematisk forskningssammanställning 'Läsförståelse och undervisning om lässtrategier' (2019)
- **URL:** https://www.skolfi.se/forskningssammanstallningar/systematiska-forskningssammanstallningar/lasforstaelse-och-undervisning-om-lasstrategier/
- **Not:** EXPERTUPPGRADERING 2026-06-05 (ersätter generisk seed-källa): systematisk översikt finner POSITIV effekt — 'det är möjligt att förbättra elevers läsförståelse med explicit strategiundervisning', och effekten är STÖRST för svaga läsare (= målgruppen för tidiga stödinsatser). Mekanism-nivå (strukturerad tidig läsundervisning förbättrar resultat); en direkt kausalutvärdering av själva läsa-skriva-räkna-garantin saknas ännu -> confidence medium.
- **Påverkar partier:** C(+), KD(+), M(+), MP(+), S(+), SD(−)
- **OK?** ⬜ (✅/✏️/❌): 

### `minskad_klasstorlek` → skolresultat

- **Riktning:** positive · **evidensnivå:** authority_evaluation · **styrka:** medium · **konfidens:** high
- **Källa:** IFAU Rapport 2012:5, Långsiktiga effekter av mindre klasser (Fredriksson, Oosterbeek, Öckert)
- **URL:** https://www.ifau.se/Forskning/Publikationer/Rapporter/2012/Langsiktiga-effekter-av-mindre-klasser/
- **Not:** Mindre klasser åk 4-6 förbättrade provresultat och långsiktiga utfall (linje med STAR).
- **Påverkar partier:** C(+), KD(+), L(+), M(+), S(+), SD(−), V(+)
- **OK?** ⬜ (✅/✏️/❌): 

### `kompetensutveckling_larare` → skolresultat

- **Riktning:** positive · **evidensnivå:** authority_evaluation · **styrka:** low · **konfidens:** medium
- **Källa:** IFAU Rapport 2015:23, Satsningar på lärare i skolor med låga elevresultat (Hall, Lundin, Sibbmark)
- **URL:** https://www.ifau.se/globalassets/pdf/se/2015/r-2015-23-erfarenheter-och-effekter-av-satsningar-pa-larare-i-skolor-med-laga-elevresultat.pdf
- **Not:** Förbättrade betyg i eng/sva åk 9, men svårt att isolera enskild komponent.
- **Påverkar partier:** C(+), KD(+), L(+), M(+), MP(+), S(+), SD(+), V(+)
- **OK?** ⬜ (✅/✏️/❌): 

### `riktat_likvardighetsbidrag` → skolresultat

- **Riktning:** unclear · **evidensnivå:** authority_evaluation · **styrka:** low · **konfidens:** medium
- **Källa:** IFAU Rapport 2025:17, Effekter av kompensatorisk resursfördelning i grundskolan (Rosenqvist, Sauermann)
- **URL:** https://www.ifau.se/Press/Pressmeddelanden/kunskapsbidraget-gav-fler-larare-men-inte-battre-resultat-pa-nationella-proven/
- **Not:** Ökade lärartätheten men förbättrade i snitt INTE nationella provresultat (nollresultat).
- **Påverkar partier:** —(ingen ståndpunkt)
- ⚠ unclear → ≈neutral B
- **OK?** ⬜ (✅/✏️/❌): 

### `kontroller_och_informationsutbyte_mot_valfardsbrott` → valfardsbrottslighet

- **Riktning:** positive · **evidensnivå:** authority_evaluation · **styrka:** low · **konfidens:** medium
- **Källa:** Brå Rapport 2022:1, Välfärdsbrott mot kommuner och regioner
- **URL:** https://bra.se/rapporter/arkiv/2022-03-25-valfardsbrott-mot-kommuner-och-regioner
- **Not:** Tillståndsplikt, kontroll och informationsutbyte bedöms verksamt; nuvarande system missar mycket.
- **Påverkar partier:** C(+), KD(+), L(+), M(+), MP(+), SD(+), V(+)
- **OK?** ⬜ (✅/✏️/❌): 

### 🚫 `koncentration_nationell_hogspecialiserad_vard` → overlevnad_svar_sjukdom

- **Riktning:** positive · **evidensnivå:** authority_evaluation · **styrka:** low · **konfidens:** low
- **Källa:** SOU 2015:98 'Träning ger färdighet – Koncentrera vården för patientens bästa' (kap. 8, volym–utfall, SBU-upplysningstjänst). Instrument/lag: prop. 2017/18:40 'En ny beslutsprocess för den högspecialiserade vården', bet. 2017/18:SoU18 punkt 1, acklamation.
- **URL:** https://data.riksdagen.se/dokument/H501SoU18.html
- **Not:** TILLAGD 2026-06-07 (B-grön-svepet, enhällighet-som-källa §5.2, FLAGGAD low/low; codex BUILD-WITH-CHANGES). INSTRUMENT (snävt, codex-krav): statligt beslutad nivåstrukturering som KONCENTRERAR nationell högspecialiserad vård (NHV) till färre enheter -> bättre resultat/ÖVERLEVNAD vid svår sjukdom DÄR volym–utfall-evidens finns -> overlevnad_svar_sjukdom UPP. EJ 'bättre vård generellt' (ej vard_tillganglighet/vårdköer). RIKTNING (SOU 2015:98, ordagrant): 'hundratals liv kan räddas varje år om den högspecialiserade vården koncentreras'; kap. 8 (SBU): volym–utfall-samband (dos-respons 5-årsöverlevnad). KAVEAT (LOW/LOW): design-/syntesevidens (utredning + SBU volym–utfall), INGEN kvantifierad ex-post kausalutvärdering av själva NHV-reformen. NEUTRAL (≠ cancerscreening, som faller på steg-2-tilt): SoU18 p1 ACKLAMATION (verifierat dokumentstatus), utskottet 'välkomnar de lagändringar som regeringen föreslår och ställer sig bakom propositionen' -> alla 8 supports. TIDSNOT (§10): bet. 2017/18, men instrumentet är fortlöpande aktivt — Socialstyrelsen fattar löpande NHV-beslut t.o.m. 2026 under samma lag (HSL 2 kap. 7 §).
- **Utlyft, skäl:** UTLYFT 2026-08-23 (#26, ADR 0006 punkt 2 och 5): faller på den symmetriska evidensgrinden, rubriken §5. Posten raderas INTE - källspåret står kvar - men hålls utanför claims och täckningsnämnaren. Faller på §5.2: confidence är low. Postens egen kaveat säger 'design-/syntesevidens (utredning + SBU volym-utfall), INGEN kvantifierad ex-post-utvärdering'. Nio av de 13 utlyfta posterna kom ur B-grön-svepet, vars mandat var minst en post med positiv verkan per undermått. Mandatet är avvecklat (ADR 0006 punkt 3). Återöppningstrigger: en officiell utvärdering som mäter instrumentets verkan på exakt indikatorn och som bär confidence minst medium.
- **Skulle ha påverkat partier:** C(+), KD(+), L(+), M(+), MP(+), S(+), SD(+), V(+)
- 🚫 UTLYFT — matar inte B · ⚠ låg konfidens
- **OK?** ⬜ (✅/✏️/❌): 

### 🚫 `fast_omsorgskontakt` → kontinuitet_i_omsorgen

- **Riktning:** positive · **evidensnivå:** authority_evaluation · **styrka:** low · **konfidens:** low
- **Källa:** Prop. 2021/22:116 'En fast omsorgskontakt i hemtjänsten' (3 kap. 3 c § SoL); Socialstyrelsen 'Vård och omsorg för äldre – Lägesrapport 2025' (kap. 'Fast omsorgskontakt – en viktig faktor för kontinuitet'). Partiståndpunkter via bet. 2021/22:SoU24 punkt 2 'Lagförslaget i övrigt', acklamation.
- **URL:** https://data.riksdagen.se/dokument/H901SoU24.html
- **Not:** TILLAGD 2026-06-07 (B-grön-svepet, §5.7 ny indikator + §5.2 enhällighet; codex BUILD-WITH-CHANGES). NY INDIKATOR kontinuitet_i_omsorgen (up) i omsorg_personal. KONSTRUKT-KORRIGERING (codex-krav): fast omsorgskontakt är konstrukt-exakt för KONTINUITET (relationskontinuitet för omsorgstagaren), INTE för personalomsattning_omsorg (🔴-väggen, data nedlagd) som behålls SEPARAT/orörd — fast_omsorgskontakt får ALDRIG beskrivas som belägg för lägre personalomsättning. INSTRUMENT-MEKANISM (prop. 2021/22:116, ordagrant): den fasta omsorgskontakten ska 'tillgodose den enskildes behov av trygghet, kontinuitet, individanpassad omsorg och samordning'; Socialstyrelsen (Lägesrapport 2025): 'Hemtjänsttagare som ofta träffar sin fasta omsorgskontakt upplever i högre grad att de får trygg och individanpassad omsorg.' KAVEAT (LOW/LOW): observations-/mekanismevidens (association + lagens syfte), ingen kausal ex-post-effekt; tillgången varierar 0–71 % mellan utförare; Socialstyrelsens formella effektutvärdering klar dec 2026/okt 2027. KONSENSUS-MÅTT (icke-rankningsdrivande): bet. 2021/22:SoU24 punkt 2 'Lagförslaget i övrigt' (3 c §) ACKLAMATION (verifierat dokumentstatus) -> alla 8 supports. EXKLUDERAR p1 (3 d §, undersköterske-KOMPETENSkravet, röstning M=Nej; M ville BREDDA behörigheten, ej avskaffa -> fel konstrukt + tilt).
- **Utlyft, skäl:** UTLYFT 2026-08-23 (#26, ADR 0006 punkt 2 och 5): faller på den symmetriska evidensgrinden, rubriken §5. Posten raderas INTE - källspåret står kvar - men hålls utanför claims och täckningsnämnaren. Faller på §5.2: confidence är low. Designevidens ur prop. 2021/22:116 och Socialstyrelsens lägesrapport om vad den fasta omsorgskontakten ska tillgodose, ingen uppmätt effekt på kontinuitet_i_omsorgen. Nio av de 13 utlyfta posterna kom ur B-grön-svepet, vars mandat var minst en post med positiv verkan per undermått. Mandatet är avvecklat (ADR 0006 punkt 3). Återöppningstrigger: en officiell utvärdering som mäter instrumentets verkan på exakt indikatorn och som bär confidence minst medium.
- **Skulle ha påverkat partier:** C(+), KD(+), L(+), M(+), MP(+), S(+), SD(+), V(+)
- 🚫 UTLYFT — matar inte B · ⚠ låg konfidens
- **OK?** ⬜ (✅/✏️/❌): 
