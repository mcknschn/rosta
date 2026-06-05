# Granskning B — evidensliggare (`config/evidence_ledger.yaml`)

> AUTOGENERERAD av `pipeline/tools/review_packet.py` — ändra inte för hand.

**33 poster** (åtgärdstyp → indikatoreffekt). Generell policy-evidens, medvetet **inte** partikopplad. Varje post sätter riktningen för ALLA partier som driver åtgärdstypen — granska källan noga (blast-radius anges per post).

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
