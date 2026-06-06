# Granskning B — evidensliggare (`config/evidence_ledger.yaml`)

> AUTOGENERERAD av `pipeline/tools/review_packet.py` — ändra inte för hand.

**37 poster** (åtgärdstyp → indikatoreffekt). Generell policy-evidens, medvetet **inte** partikopplad. Varje post sätter riktningen för ALLA partier som driver åtgärdstypen — granska källan noga (blast-radius anges per post).

## Så granskar du

1. Öppna `source_url` och bekräfta att den svenska utvärderingen/akademiska källan faktiskt stöder `direction` på `indicator` (`positive` = rör indikatorn åt RÄTT håll).
2. Bedöm om `evidence_level`/`effect_strength`/`confidence` är rimliga (ej översålda).
3. Särskilt: `unclear`/`mixed` ger ≈neutral B (rätt om evidensen är svag); `negative` **vänder** semantiken; `expert_opinion` är svagast (ej uppmätt kausalitet).

---

## demokrati

### `systematiskt_antikorruptionsarbete_kommuner_regioner` → korruption

- **Riktning:** positive · **evidensnivå:** expert_opinion · **styrka:** low · **konfidens:** low
- **Källa:** Statskontoret 2023:13, Nya utmaningar och gamla problem – om korruption i kommuner och regioner
- **URL:** https://www.statskontoret.se/uppdrag-och-rapporter/rapporter/2023/nya-utmaningar-och-gamla-problem--om-korruption-i-kommuner-och-regioner/lasrapporten
- **Not:** Rekommenderar systematiskt riskbaserat antikorruptionsarbete; inget uppmätt kausalsamband (expertbedömning).
- **Påverkar partier:** C(+), L(+), S(+), SD(+)
- ⚠ expert_opinion (ej uppmätt kausalitet) · ⚠ låg konfidens
- **OK?** ⬜ (✅/✏️/❌): 

### `atgarder_mot_otillaten_paverkan_offentlig_sektor` → korruption

- **Riktning:** positive · **evidensnivå:** expert_opinion · **styrka:** low · **konfidens:** low
- **Källa:** Brå, kunskaps-/vägledningsmaterial om otillåten påverkan mot offentlig sektor
- **URL:** https://bra.se/amnen/otillaten-paverkan
- **Not:** Rekommenderar systematiskt förebyggande arbete; kvantifierar inte riskminskningen (expertbedömning).
- **Påverkar partier:** C(+), L(+), MP(+), S(+)
- ⚠ expert_opinion (ej uppmätt kausalitet) · ⚠ låg konfidens
- **OK?** ⬜ (✅/✏️/❌): 

### `starkt_oberoende_granskning_och_insyn` → korruption

- **Riktning:** positive · **evidensnivå:** expert_opinion · **styrka:** low · **konfidens:** low
- **Källa:** ESO 2013:2, Allmän nytta eller egen vinning? (Bergh, Erlingsson, Sjölin, Öhrvall)
- **URL:** https://eso.expertgrupp.se/rapporter/20132-allman-nytta-eller-egen-vinning/
- **Not:** Brister i granskning av kommuner/bolag = korruptionssårbarhet -> stärkt insyn motverkar; ej effektutvärdering.
- **Påverkar partier:** C(+), KD(+), L(+), M(+), MP(+), S(+), SD(+), V(+)
- ⚠ expert_opinion (ej uppmätt kausalitet) · ⚠ låg konfidens
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

### `lagstadgat_oberoende_public_service` → mediefrihet

- **Riktning:** positive · **evidensnivå:** authority_evaluation · **styrka:** low · **konfidens:** low
- **Källa:** Prop. 2024/25:166 'En lag om public service och riktlinjer för verksamheten 2026–2033' (bygger på 2023 års parlamentariska public service-kommitté, betänkandet SOU 2024:34 'Ansvar och oberoende – public service i oroliga tider'). Partiståndpunkter via enhälligt betänkande 2025/26:KrU2 punkt 1, acklamation.
- **URL:** https://data.riksdagen.se/dokument/HC03166.html
- **Not:** TILLAGD 2026-06-06 (B2, enhällighet-som-källa). INSTRUMENT: för första gången regleras public service-uppdraget I LAG (ny lag om public service) med LAGSTADGAT OBEROENDE, i stället för enbart i regeringsbeslutat sändningstillstånd -> mediefrihet UPP (positiv riktning) via institutionellt skyddat oberoende. SNÄV FORMULERING (codex-krav 2026-06-06): claimet avser lagstadgat oberoende -> mediefrihet/fri åsiktsbildning, INTE generellt 'public service-lag -> demokrati'. INSTRUMENT-MEKANISM (ordagrant ur prop. 2024/25:166 avsnitt 5.2.1, Regeringens förslag): 'Public service-uppdraget ska bedrivas självständigt i förhållande till såväl staten som olika ekonomiska, politiska och andra intressen och maktsfärer i samhället och verksamheten ska präglas av oberoende och stark integritet.' Provenans = bred politisk enighet (prop. avsnitt 4): 'I Sverige råder sedan länge en bred politisk enighet om att en väl fungerande mediemarknad bygger på en kombination av ansvarstagande kommersiella medier och ett starkt och oberoende public service med högt förtroende hos allmänheten'; mediepolitikens syfte är 'att skapa goda förutsättningar för en mångfald av självständiga medieaktörer som bidrar till att stärka en fri åsiktsbildning, ett fritt utbyte av idéer liksom en aktiv granskning av samhällets makthavare'. KAVEAT (effect_strength/confidence=LOW, codex-kalibrerat): MEKANISM-/DESIGNBASERAD evidens (parlamentarisk kommitté SOU 2024:34 + proposition), INGEN ex-post-effektutvärdering av att lagen MÄTT ökat mediefriheten -> låg styrka/förtroende; får ej formuleras som uppmätt indikatorförbättring. KONSENSUS-MÅTT (icke-rankningsdrivande): positioneras via enhälligt bet. 2025/26:KrU2 punkt 1 (acklamation, votering-API tomt @antal=0, 'Det har inte väckts någon motion som går emot att riksdagen antar regeringens lagförslag'); samtliga 15 reservationer gäller punkt 2-14 (innehållsuppdrag/ekonomi/uppföljning, S/V/C/MP) och tolkas INTE som opposition mot punkt 1 -> alla 8 partier supports på instrumentet att anta lagen. FRAMTIDA UPPGRADERING: om SOU/utvärdering belägger starkare varför lagFORMEN (ej bara oberoende i sak) stärker institutionellt oberoende. Demokrati yttrandefrihet_medier tidigare B-tomt -> demokrati 3/5 -> 4/5.
- **Påverkar partier:** C(+), KD(+), L(+), M(+), MP(+), S(+), SD(+), V(+)
- ⚠ låg konfidens
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

### `jobbskatteavdrag` → sysselsattning

- **Riktning:** unclear · **evidensnivå:** authority_evaluation · **styrka:** unknown · **konfidens:** low
- **Källa:** IFAU, forskningssammanfattning Jobbskatteavdrag
- **URL:** https://www.ifau.se/Press/Forskningssammanfattningar/Jobbskatteavdrag/
- **Not:** Effekten svår att utvärdera (kontrollgrupp saknas); inga säkra slutsatser.
- **Påverkar partier:** —(ingen ståndpunkt)
- ⚠ unclear → ≈neutral B · ⚠ låg konfidens
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

### `inkomststarkande_hushallspolitik` → hushallens_reala_disponibla_inkomst

- **Riktning:** positive · **evidensnivå:** descriptive_statistic · **styrka:** medium · **konfidens:** high
- **Källa:** Fördelningspolitisk redogörelse april 2025 (bilaga till 2025 års ekonomiska vårproposition, Finansdepartementet)
- **URL:** https://www.regeringen.se/informationsmaterial/2025/04/fordelningspolitisk-redogorelse-april-2025/
- **Not:** TILLAGD 2026-06-05 (BACKLOG B2): gör submåttet 'Reallöner och hushållens ekonomi' B-bart (ekonomi 3/6 -> 4/6) via den ARBETANDE indikatorn hushallens_reala_disponibla_inkomst (realloner förblir vilande kontext, ej partistyrbar). VÄRDENEUTRAL åtgärdstyp-FAMILJ: skatte- OCH/ELLER transfereringsreformer som höjer hushållens disponibla inkomst. Fördelningspolitiska redogörelsen definierar disponibel inkomst (arbets-/kapital-/näringsinkomst + transfereringar − direkta skatter) och analyserar hur skatte- och transfereringsreformer påverkar den -> både SÄNKT SKATT (höger) och HÖJDA TRANSFERERINGAR (vänster) höjer disponibel inkomst. Därför kodas BÅDA blocken som supports via sitt instrument = ingen höger-/vänstertilt (till skillnad från skatt/reglering där bara 'mindre stat' räknas). evidence_level descriptive_statistic (accounting/beskrivande, ej kausal välfärdsutvärdering) -> modest vikt; riktning definitionsmässigt säker -> confidence high. Partiståndpunkter: inkomststarkande_hushallspolitik (8 supports, instrument per parti i mapping_note).
- **Påverkar partier:** C(+), KD(+), L(+), M(+), MP(+), S(+), SD(+), V(+)
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

### `tydlig_statlig_styrning_civilt_forsvar` → civil_beredskap_niva

- **Riktning:** positive · **evidensnivå:** authority_evaluation · **styrka:** low · **konfidens:** low
- **Källa:** Riksrevisionen RiR 2025:4, Den statliga styrningen av det civila försvarets uppbyggnad
- **URL:** https://www.riksrevisionen.se/granskningar/granskningsrapporter/2025/den-statliga-styrningen-av-det-civila-forsvarets-uppbyggnad.html
- **Not:** Otydliga mandat och svag finansiering bromsade uppbyggnaden -> tydligare styrning behövs.
- **Påverkar partier:** L(+), M(+), S(+), SD(+), V(+)
- ⚠ låg konfidens
- **OK?** ⬜ (✅/✏️/❌): 

### `nato_medlemskap` → nato_interoperabilitet

- **Riktning:** positive · **evidensnivå:** authority_evaluation · **styrka:** high · **konfidens:** high
- **Källa:** Försvarsberedningen, Ds 2024:6 'Stärkt försvarsförmåga – Sverige som allierad'. Partiståndpunkter via votering bet. 2022/23:UU16 punkt 1 (godkänner Sveriges anslutning till Nato, prop. 2022/23:74).
- **URL:** https://data.riksdagen.se/dokument/HCB46.html
- **Not:** NEUTRALT ANKARE = Försvarsberedningen (blocköverskridande beredningsorgan): Nato-medlemskap 'ökar säkerheten för Sverige och stärker Nato som helhet'; 'det kollektiva försvarsåtagandet i Nato utgör nu en central del i den svenska säkerhets- och försvarspolitiken' och ger 'interoperabilitet och förmåga att operativt agera gemensamt med andra'. Medlemskapet är det grundläggande instrumentet för nato_interoperabilitet (UPP) -> direction positive (nära definitionellt) -> effect_strength/confidence high. MP-NOT (codex-granskat 2026-06-06): MP röstade Nej 2022 men har sedan svängt till Nato-stöd -> MP kodas none (ej opposes), då ett negativt B från en föråldrad position vore vilseledande för en app som guidar dagens röst. V (fortsatt Nato-kritiskt = aktuellt) kodas opposes.
- **Påverkar partier:** C(+), KD(+), L(+), M(+), S(+), SD(+), V(−)
- **OK?** ⬜ (✅/✏️/❌): 

## integration

### `sfi_kombinerat_med_praktik` → sysselsattningsgap_inrikes_utrikes

- **Riktning:** positive · **evidensnivå:** authority_evaluation · **styrka:** medium · **konfidens:** medium
- **Källa:** IFAU, forskningssammanfattning 'Utrikes föddas etablering på arbetsmarknaden' (refererar Dahlberg m.fl. 2020)
- **URL:** https://www.ifau.se/Press/Forskningssammanfattningar/Utrikes-foddas-eta-pa-arbetsmarknaden-/
- **Not:** EXPERTUPPGRADERING 2026-06-05 (ersätter generisk seed-källa): IFAU sammanfattar att 'Genom intensiv språkutbildning, arbetspraktik samt sök- och matchningshjälp dubblerades sysselsättningen bland lågutbildade nyanlända' (Dahlberg m.fl. 2020) -> kombinerad sfi + praktik höjer sysselsättningen för utrikes födda (minskar gapet). confidence höjd low->medium (konkret kvantifierad effekt, men vilar på en pilot i Göteborg).
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

### `ny_karnkraft` → effektbrist

- **Riktning:** positive · **evidensnivå:** authority_evaluation · **styrka:** high · **konfidens:** high
- **Källa:** Svenska kraftnät, Kraftbalansen på den svenska elmarknaden – rapport 2025 (lagstadgad rapport till regeringen, 3 § förordn. 2007:1119)
- **URL:** https://www.svk.se/49bb53/siteassets/om-oss/rapporter/2025/kraftbalansen-pa-den-svenska-elmarknaden-rapport-2025.pdf
- **Not:** Exakt på indikatorn effektbrist (effektbalans vid topplasttimmen). Planerbar baskraft har tillgänglighetsfaktor ~90 % vid topplast (vindkraft 9 %, solkraft 0 %, Tabell 13 s.45), så ny/utbyggd planerbar kärnkraft ökar tillgänglig effekt vid topplast och drar effektbrist-risken nedåt. POSITIV riktning (negativ-grinden ej tillämplig). Källan fastställer riktningsmekanismen via tillgänglighetsfaktorer, ej nybyggnadskostnad/ledtid; ett parti som motsätter sig instrumentet (opposes) får negativt B-bidrag på effektbrist — flaggat för mänsklig granskning. KÄLLTYPS-ASYMMETRI (expertgranskning 2026-06-05, SUSPECT 4): ny_karnkraft kodar partiets GENERELLA hållning till ny/utbyggd kärnkraft. supports-raderna (M/SD/KD/L) är generella partimotioner från olika riksmöten (2020/21–2024/25); opposes-raderna (V/MP) är följdmotioner mot prop 2025/26:160. Jämförelsen avser alltså för/emot ny kärnkraft generellt — inte en röst om just prop 160. Bekräftat ordagrant + rätt riktade i adversariell omverifiering.
- **Påverkar partier:** KD(+), L(+), M(+), MP(−), S(+), SD(+), V(−)
- **OK?** ⬜ (✅/✏️/❌): 

### `atgarder_mot_invasiva_frammande_arter` → hotade_arter_naturforlust

- **Riktning:** positive · **evidensnivå:** authority_evaluation · **styrka:** low · **konfidens:** low
- **Källa:** Naturvårdsverket, ämnesområde 'Invasiva främmande arter' (myndighetsbedömning). Instrument/beslut: prop. 2025/26:41, bet. 2025/26:MJU13 punkt 1 (skärpt regelverk: miljöbalken + inregränslagen).
- **URL:** https://www.naturvardsverket.se/amnesomraden/invasiva-frammande-arter/
- **Not:** TILLAGD 2026-06-06 (B2, enhällighet-som-källa). Åtgärder mot invasiva främmande arter (EU-förordn. 1143/2014 + nationellt regelverk: nationell förteckning, straffansvar för otillåten hantering, anmälningsskyldighet + Tullverkets kontroll vid inre gräns, tidig upptäckt) -> hotade_arter_naturforlust NER (positiv riktning). INSTRUMENT-MEKANISM (svar på codex instrument-precisions-invändning 2026-06-06): Naturvårdsverket anger att förteckningen är 'ett verktyg i arbetet med att förebygga och begränsa spridningen av arter som kan orsaka skador på natur, biologisk mångfald och ekosystem', och prop. 2025/26:41 (i MJU13) att 'det mest kostnadseffektiva sättet att förhindra introduktion av invasiva främmande arter är att de upptäcks i ett tidigt skede' -> instrumentet driver indikatorn via mekanismen förhindra spridning/introduktion. Naturvårdsverkets rubrikbedömning: 'Invasiva främmande arter är ett av de största hoten mot biologisk mångfald i Sverige och globalt.' KAVEAT (effect_strength/confidence=LOW, codex-kalibrerat 2026-06-06): riktningen är myndighetsbelagd på MEKANISM-nivå men det finns INGEN kvantifierad svensk kausalutvärdering av åtgärdernas faktiska utfall på hotade arter -> låg styrka/förtroende. KONSENSUS-MÅTT: positioneras via enhälligt bet. 2025/26:MJU13 punkt 1 (acklamation, 'inte väckts någon motion som går emot regeringens lagförslag') -> alla 8 partier supports; tiltade avslagspunkten (p2) utesluten. FLAGGAD för mänsklig sign-off — codex förordade HOLD; byggd som version 0 med konservativ kalibrering för din bedömning.
- **Påverkar partier:** C(+), KD(+), L(+), M(+), MP(+), S(+), SD(+), V(+)
- ⚠ låg konfidens
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

### `psykosociala_insatser_frivard` → aterfall_i_brott

- **Riktning:** positive · **evidensnivå:** systematic_review · **styrka:** low · **konfidens:** low
- **Källa:** SBU Rapport 369 (2023), Psykosociala insatser mot gängkriminalitet
- **URL:** https://www.sbu.se/369
- **Not:** Psykosociala insatser i frivård kan minska återfall ~1 år (OR 0,56), låg tillförlitlighet.
- **Påverkar partier:** —(ingen ståndpunkt)
- ⚠ låg konfidens
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
