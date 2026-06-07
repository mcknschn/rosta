# Fas 4c Plan B — harmoniserings-audit
> Genererad 2026-05-30 ur panel-harmoniserings-workflowen (19 åtgärdstyper × 8 partier, 289 agenter)
> under den frysta rubriken [fas4c_rubrik.md](../fas4c_rubrik.md). Klimat (koldioxidskatt,
> reduktionsplikt_drivmedel) ingick EJ — votering-förankrat, ingen isolerings-asymmetri.

## Sammanfattning
- Admitterade non-klimat-rader: **109** (panel keep/add OCH verifierare confirmed=true).
- Klimat-rader bevarade oförändrat: **14**. Totalt i config: **123**.
- Avvisade/luckor loggade nedan: **43**.
- Panel-protokoll: första-pass per rad mot rubriken, sedan SIDA-VID-SIDA-harmonisering per
  åtgärdstyp (samma standard för alla 8 partier), därefter oberoende verifiering mot .text.
- **Inget täckningsmål**; utfallen är medvetet asymmetriska där verkligheten är det.

## Ranking-effekt (standardvikter, version 0)

| Parti | Före harmonisering | Efter | Δ |
|---|---|---|---|
| S | 3.67 | 3.71 | ↑ |
| MP | 3.41 | 3.41 | – |
| L | 3.20 | 3.37 | ↑ (återvunna luckor) |
| M | 3.12 | 3.28 | ↑ (M↔KD byter plats) |
| KD | 3.14 | 3.10 | ↓ |
| V | 2.68 | 2.67 | – |
| C | 2.49 | 2.40 | ↓ (fler opposes / droppad svag rad) |
| SD | 2.28 | 2.33 | ↑ |

Rankingen är stabil — harmoniseringen gav nyanser (återvunna luckor lyfte L/M, återvunna/behållna
opposes sänkte C), inga stora kast. evidence.json: 445 → 458 claims.

## ⚠️ Flaggat för mänsklig granskning (instrument-vs-proposition + recency)
Vissa `opposes` vilar på *avslag av en specifik proposition* snarare än ett uttryckligt motstånd
mot åtgärdstypen som sådan. Att avslå en regerings *lagförslag* kan vara motstånd mot instrumentet
ELLER mot just den utformningen. En människa bör avgöra om dessa ska stå kvar:
- **V kontroller_och_informationsutbyte_mot_valfardsbrott** [HC023445, 2025-06-17]: "Riksdagen avslår proposition 2024/25:180."
- **SD tidiga_insatser_lagstadiet** [H501UbU10, 2018-05-30]: "Vi anser att förslaget till riksdagsbeslut under punkt 1 borde ha följande lydelse: Riksdagen avslår regeringens förslag. Därmed bifaller ri"
- **C tidiga_insatser_lagstadiet** [H5023910, 2017-10-12]: "Riksdagen avslår regeringens proposition 2017/18:18 Läsa, skriva, räkna – en åtgärdsgaranti."
- **V aktiveringskrav_ekonomiskt_bistand** [HD024027, 2026-04-01]: "Riksdagen avslår proposition 2025/26:207. ... I denna proposition lämnar regeringen lagförslag om ett aktivitetskrav som villkor för rätt ti"

## Per åtgärdstyp — panelbeslut + verifiering

### ekonomi / `subventionerade_anstallningar`
| parti | panelbeslut | verifierare | utfall |
|---|---|---|---|
| S | keep | confirmed | ADMITTED (supports) |
| M | keep | confirmed | ADMITTED (supports) |
| SD | keep | confirmed | ADMITTED (opposes) |
| C | keep | confirmed | ADMITTED (opposes) |
| V | keep | confirmed | ADMITTED (supports) |
| KD | keep | confirmed | ADMITTED (supports) |
| L | keep | confirmed | ADMITTED (supports) |
| MP | keep | confirmed | ADMITTED (supports) |

*Gemensam standard:* Gemensam standard tillämpad sida vid sida för alla 8 partier: (1) INSTRUMENT-REGEL — stance endast vid källa som rör samma policyinstrument (subventionerade anställningar) eller en av dess namngivna delformer (nystartsjobb, introduktionsjobb, extratjänster, lönebidrag); inga allmänna mål godtogs. (2) BUNTEN-REGEL — alla källor här är buntade UO14/arbetsmarknadsmotioner; ingen rad förkastades p.g.a. intern nyans när citatet var instrument-exakt. (3) Alla 8 källor är partikollektiva (kommitté-/budgetmotioner), ingen enskild ledamot => ingen confidence-begränsning till low; samtliga fick high. (4) Alla 8 citat verifierades ORDAGRANT mot data.riksdagen.se .text (L:s citat finns i .text inbäddat i HTML-span-taggar och är verbatim efter avkodning; S/V hade HTML-/soft-hyphen-artefakter som rensats utan att ändra ordalydelsen). Beslut: 8 keep, 0 drop, 0 unknown. Utfallet är medvetet asymmetriskt (6 supports, 2 opposes) och INTET täckningsmål eller fördelnings-utjämning tillämpades. HARMONISERINGAR där tidigare olika-bedömda partier nu behandlas LIKA: (a) S, M, KD, L har alla buntade motioner där EN namngiven delform stärks medan en ANNAN delform skärs ned/fasas ut — alla fyra = supports (M:s utfasning av extratjänster+introduktionsjobb behandlas exakt som L/KD:s utfasning av extratjänster och som S:s kontrollskärpning av nystartsjobb: intern nyans, ej rejection). (b) SD och C har båda buntade motioner med instrument-exakt umbrella-citat som pekar mot nedskärning/motstånd MEN är samtidigt positiva till delformen lönebidrag — båda = opposes, med lönebidrag-nyansen i mapping_note (symmetrisk behandling). (c) MP saknar umbrella-termen men belägger stance via namngiven delform (lönebidrag) — behandlas LIKA med M och L som belägger stance via namngiven delform (nystartsjobb), dvs delform-belägg är giltigt instrument-exakt belägg oavsett vilken delform.

### ekonomi / `arbetsmarknadsutbildning`
| parti | panelbeslut | verifierare | utfall |
|---|---|---|---|
| S | keep | confirmed | ADMITTED (supports) |
| M | keep | confirmed | ADMITTED (supports) |
| SD | keep | confirmed | ADMITTED (supports) |
| C | keep | confirmed | ADMITTED (opposes) |
| V | keep | confirmed | ADMITTED (supports) |
| KD | keep | confirmed | ADMITTED (opposes) |
| L | keep | confirmed | ADMITTED (opposes) |
| MP | keep | confirmed | ADMITTED (supports) |

*Gemensam standard:* Gemensam standard tillämpad sida-vid-sida på instrumentet "arbetsmarknadsutbildning (AUB via Arbetsförmedlingen)" enligt frusen rubrik (docs/fas4c_rubrik.md, FRYST 2026-05-30). Alla 8 citat verifierades ORDAGRANT mot hämtad .text från data.riksdagen.se (entitetsnormalisering: mjukt bindestreck &#xad; och icke-brytande mellanslag &#xa0; återställdes — C:s 'före-slagna', M:s 'arbetsmarknad-sutbildningar' och V:s '2 000' var endast brutna av dessa entiteter i råtexten, inte fabricerade).

INSTRUMENT-REGEL (§1): Varje rad namnger ordet 'arbetsmarknadsutbildning(ar/en)' explicit — ingen rad vilar på ett allmänt mål ('fler i arbete'). Samtliga 8 klarar instrument-exakthet.

BUNTEN-REGEL (§2) — tillämpad LIKA: S, C, V, KD, L och MP buntar alla flera arbetsmarknadsinstrument i samma motion/yrkande; i samtliga fall är AUB-citatet instrument-exakt, så raden räknas och intern nyans noteras i mapping_note utan att förkasta raden. Detta är direkt den M/L-symmetri rubriken skrevs för att rätta: M:s buntade supports-ståndpunkt och L:s analoga buntade opposes-ståndpunkt behandlas nu på exakt samma villkor — bägge gäller. Inget parti fick lösare/strängare buntkrav.

KÄLLHIERARKI & ENSKILD MOTION (§3): Alla 8 källor är partikollektiva (parti-/kommitté-/budgetmotion); ingen enskild motion behövde åberopas, så ingen rad tvingades till confidence=low på den grunden. För M valdes medvetet den partikollektiva kommittémotionen (H6022931) framför en nyare enskild M-motion (HD022316, 2025/26) enligt §3.

TIDSREGEL (§4) — tillämpad SYMMETRISKT: S, SD, V, MP har källor i föredragen period (2024/25-2025/26) => confidence=high. M (2018/19), C (2021/22), KD (2020/21) och L (2021/22) ligger utanför föredragen period eftersom ingen nyare partikollektiv instrument-exakt källa finns (motiverat per parti i mapping_note) => confidence=medium. Tidsleniens gavs lika till alla fyra äldre-period-partier; inget parti fick strängare tidskrav, och stance-riktningen påverkade inte konfidensgraderingen (graderad enbart på period + källtyp).

INGET TÄCKNINGSMÅL / INGEN UTJÄMNING (§8): Utfallet blev 5 supports (S, M, SD, V, MP) och 3 opposes (C, KD, L). Denna asymmetri lämnades orörd — den speglar de faktiskt funna källorna. Inga luckor fylldes och fördelningen jämnades inte ut.

BESLUT: Alla 8 rader KEEP (instrument-exakt, rätt riktning, citat verbatim). Inga drop, inga unknown. rejected[] är tom eftersom varje parti hade en hållbar instrument-exakt partikollektiv källa.

### valfard / `kompetensutveckling_larare`
| parti | panelbeslut | verifierare | utfall |
|---|---|---|---|
| S | keep | confirmed | ADMITTED (supports) |
| M | keep | confirmed | ADMITTED (supports) |
| SD | keep | confirmed | ADMITTED (supports) |
| C | keep | confirmed | ADMITTED (supports) |
| V | keep | confirmed | ADMITTED (supports) |
| KD | keep | confirmed | ADMITTED (supports) |
| L | keep | confirmed | ADMITTED (supports) |
| MP | keep | confirmed | ADMITTED (supports) |

*Gemensam standard:* Gemensam standard tillämpad lika på alla 8 partier för instrumentet kompetensutveckling/fortbildning för lärare (kompetensutveckling_larare, valfard). (1) INSTRUMENT-REGEL (§1): stance endast om citatet rör SAMMA policyinstrument — här lärarfortbildning/kompetensutveckling. Alla 8 citat namnger lärar(/skolledar/rektors-)fortbildning eller anslag 1:10 'Fortbildning av lärare och förskolepersonal' explicit; inget vilar på enbart ett gemensamt mål ('bättre skola'). (2) BUNTEN-REGEL (§2): där en motion buntar flera instrument eller innehåller en utformningsnyans (M: 'övertagande' till högskolor; SD: egen modell synk:ad med karriärsystem; C: avgränsat till digitala verktyg/AI; L: lärarna styr själva; KD: bredare skolpaket; MP: flera skolyrkanden) räknas raden för det namngivna instrumentet och nyansen läggs i mapping_note — den används ALDRIG som skäl att förkasta. Detta är den uttryckliga rättelsen av det historiska M/L-fallet: M:s och L:s analoga buntade/nyanserade ståndpunkter behandlas nu LIKA (båda keep, båda supports), inte olika strängt. (3) BUDGET-/ANSLAGSBELÄGG behandlas lika: KD (prosa + anslag 1:10), L (prosa + tabell anslag 1:10) och V (tabell anslag 1:10 med positiv avvikelse) räknas alla som instrument-exakta budgetbelägg för samma anslag. (4) KÄLLHIERARKI (§3): alla 8 är partikollektiva (kommitté-/parti-/budgetmotion) — ingen enskild ledamotsmotion, så ingen confidence=low-sänkning på den grunden. (5) NO-FABRICATION (§10): jag verifierade varje citat mot data.riksdagen.se .text. Sju citat är ordagrant sammanhängande och bekräftade (S, M, SD, C, KD, L, MP). V:s research-citat var en REKONSTRUERAD KOMPOSIT (tabellrubrik + ellips + radetikett) som INTE förekommer sammanhängande i .text (rubriken 'Avvikelser gentemot regeringen för utgiftsområde 16 ...' splittras av span-taggar och &#xa0;-entiteter). Per §10 ersatte jag V:s citat med den enda sammanhängande verbatim-strängen, anslagsetiketten 'Fortbildning av lärare och förskolepersonal', och sänkte V:s confidence till medium eftersom riktningen (+) vilar på tabellstrukturen snarare än sammanhängande prosa. Detta är en standard-harmonisering, inte en slutsats-justering: V:s stance (supports) håller på samma grund som KD/L. (6) TIDSREGEL (§4) tillämpad symmetriskt: fyra källor (M, SD, KD, L) är från 2021/22, strax före föredragen period (2022/23-2025/26), vilket noterats i varje mapping_note; ingen fick strängare tidskrav än annan. S är 2023/24, C och MP är 2025/26. (7) INGET TÄCKNINGSMÅL (§8): utfallet är 8/8 supports — detta är inte utjämning utan en spegling av verkligheten: kontinuerlig lärarfortbildning stöds brett tvärs över blocken; partierna skiljer sig i UTFORMNING (statligt styrt vs lärarstyrt vs systembyggande vs anslagsnivå), vilket per bunten-regeln är mapping_note-material, inte stance. Inget opposes hittades eftersom ingen instrument-exakt källa belägger att något parti vill avskaffa/skära ned lärarfortbildning. Inga rader droppades och inga luckor fylldes utan instrument-exakt verbatim-källa.

### valfard / `minskad_klasstorlek`
| parti | panelbeslut | verifierare | utfall |
|---|---|---|---|
| S | keep | confirmed | ADMITTED (supports) |
| M | keep | confirmed | ADMITTED (supports) |
| SD | keep | confirmed | ADMITTED (opposes) |
| C | keep | confirmed | ADMITTED (supports) |
| V | keep | confirmed | ADMITTED (supports) |
| KD | keep | confirmed | ADMITTED (supports) |
| L | keep | confirmed | ADMITTED (supports) |
| MP | keep | rejected | REJECTED-BY-VERIFIER (panel sa keep) |

*Gemensam standard:* GEMENSAM STANDARD (frusen rubrik, tillämpad lika på alla 8 partier): (1) INSTRUMENT-regeln — stance endast om källan rör SAMMA instrument (minskad klasstorlek / fler lärare per elev). Alla 8 rader bygger på citat som namnger klasstorlek/klasser/lärartäthet explicit; inget allmänt skolmål godtogs. (2) BUNTEN-regeln tillämpad IDENTISKT: S, M, C, V, KD, L och MP har alla buntade källor (instrumentet sitter i en lista/avsnitt med andra skolåtgärder). Eftersom citatet i varje fall är instrument-exakt förkastades INGEN bunt; intern nyans (begränsat till lågstadiet för M/KD/L; villkorad formulering för MP) skrevs i mapping_note och användes ALDRIG som skäl att förkasta. (3) Källhierarki/recency: ingen votering hittades för instrumentet hos något parti; alla rader vilar på parti-/kommittémotion (nivå 2). Föredragen mandatperiod (2025/26) finns för S, C, V, MP; äldre 2014/15-källa (H2023002) behålls för M, KD, L eftersom ingen nyare instrument-exakt källa existerar — recency-regeln tillämpad lika.\n\nVIKTIGASTE HARMONISERINGEN — H2023002 (delas av M, KD, L): Detta är ETT dokument med EN instrument-exakt passage. Research-resultaten citerade det inkonsekvent: M och L återgav .text-endpointens rå-span-artefakter (\"min skad klasstorlek\", \"satsn ingar\"), medan KD återgav den rena lydelsen. Jag hämtade och HTML-avkodade .text och fastställde att den faktiskt SERVERADE/renderade texten är ren: \"Vi föreslår satsningar på fler utbildade lärare, satsningar på fler karriärtjänster i skolan–särskilda satsningar görs i utanförskapsområden, satsningar på fler speciallärare, minskad klasstorlek i lågstadiet, satsningar på ett fortsatt mattelyft\". Jag normaliserade därför M:s och L:s citat till EXAKT samma renderade lydelse som KD, så att tre partier med IDENTISK källa nu får identiskt verbatim-citat och identisk confidence (medium). Detta är ren standardharmonisering (rubrik §9: harmonisera standarden, inte slutsatsen) — slutsatsen (supports) var redan likadan; det var citatåtergivningen som skilde sig.\n\nCONFIDENCE-likabehandling: partikollektiva källor i senaste mandatperioden (S, C, V) => high. Partikollektiva men 2014/15 (M, KD, L) => medium (gammal men instrument-exakt, ingen nyare). MP => low p.g.a. villkorad/exemplifierande formulering utan skarpt yrkande (instrument-exakt men svagt) — sänkt confidence, ej drop, eftersom citatet ändå är instrument-exakt. Ingen rad vilar på enskild motion, så ingen tvingades till low/unknown av is_single_member.\n\nASYMMETRI BEVARAD (inget täckningsmål): SD står ensamt som opposes — en dedikerad, instrument-exakt SD-passage (avsnitt 6.6.2) som uttryckligen avvisar att minska klasserna. Detta jämnades INTE ut mot de sju supports; verkligheten är asymmetrisk och rubriken förbjuder utjämning. Alla 8 rader = keep; inga drop, inga unknown — varje parti hade en instrument-exakt, verifierbar källa på data.riksdagen.se. Samtliga citat verifierade ordagrant mot hämtad .text (S, SD, C, V, MP via direkt grep/fetch; M/KD/L via HTML-avkodad .text).

### valfard / `tidiga_insatser_lagstadiet`
| parti | panelbeslut | verifierare | utfall |
|---|---|---|---|
| S | keep | confirmed | ADMITTED (supports) |
| M | keep | confirmed | ADMITTED (supports) |
| SD | keep | confirmed | ADMITTED (opposes) |
| C | keep | confirmed | ADMITTED (opposes) |
| V | unknown | — | UNKNOWN |
| KD | keep | confirmed | ADMITTED (supports) |
| L | unknown | — | UNKNOWN |
| MP | add | confirmed | ADMITTED (supports) |

*Gemensam standard:* Gemensam standard (FRYST RUBRIK fas4c_rubrik.md §1–§4, §6, §8–§10) tillämpad SIDA VID SIDA på alla 8 partier för instrumentet 'tidiga stödinsatser i lågstadiet (läsa-skriva-räkna-garantin)'. (A) INSTRUMENT-EXAKTHET (§1): stance endast om källan direkt avser garantin/åtgärdsgarantin för tidiga stödinsatser i förskoleklass/lågstadiet, ej allmänna mål. Detta uteslöt V (förskola-sektion = annat instrument) och MP:s gamla rad HD024048 (neutral beskrivning + allmänt mål 'tidigt stöd'). (B) BUNTEN-REGELN (§2) tillämpad SYMMETRISKT: S (budgetmotion som buntar flera instrument) och M/KD/C (allianskommittémotioner med interna nyanser om tioårig grundskola/dubbelreglering) behandlas LIKA — instrument-exakt citat => raden gäller, intern nyans noteras endast i mapping_note, aldrig som skäl att förkasta. Ingen buntad rad förkastades på nyans. (C) HARMONISERING AV M/KD/C/L (rubrikens uttalade kärnfall): alla fyra delar samma alliansens kommittémotionsunderlag. Standarden: parti kodas av RIKTNINGEN i den/de instrument-exakta källor som utgör dess record. H5024117 (re prop. 2017/18:195) = acceptans utan avslag => supports (M, KD). H5023910 (re prop. 2017/18:18 åtgärdsgarantin) = rent avslagsyrkande => opposes (C). L är det enda parti vars record omfattar BÅDA motstridiga källorna utan tiebreaker => unknown. Detta är 'harmonisera standarden, inte slutsatsen' (§9.4): samma regel ger asymmetriska utfall därför att underlaget skiljer sig, inte därför att stränghet skiljer sig. (D) KÄLLHIERARKI (§3): SD belagt via votering+reservation (guldstandard, höjer enskild följdmotion till partilinje => is_single_member=false). Inga enskilda motioner användes som ensamt belägg. (E) TIDSREGEL (§4) symmetriskt: M/SD/C/KD/L:s källor är 2017/18 (utanför föredragen period 2022/23–2025/26) och detta noteras lika för alla; S och MP har källor inom perioden. Ingen fick strängare tidskrav. (F) INGET TÄCKNINGSMÅL (§8): V:s och L:s luckor fylldes EJ; utfallet (4 supports: S/M/KD/MP, 2 opposes: SD/C, 2 unknown: V/L) är ett rent utfall av befintliga instrument-exakta källor, ej en utjämnad fördelning. (G) NO-FABRICATION (§10): samtliga citerade quotes verifierade ordagrant mot hämtad .text — S (curl+grep på 561 KB-fil, WebFetch truncerade), M/KD (WebFetch), C (WebFetch), SD-reservation (WebFetch), MP (WebFetch). VERIFIERINGSNOT: S-budgetmotionen krävde direkt nedladdning (curl) eftersom WebFetch endast returnerade innehållsförteckningen; citatet och motionens explicita referens till 'läsa, skriva och räkna – garantin' samt 'Skolinspektionens granskning av läsa, skriva och räkna – garantin' bekräftades ordagrant.

### valfard / `kontroller_och_informationsutbyte_mot_valfardsbrott`
| parti | panelbeslut | verifierare | utfall |
|---|---|---|---|
| S | keep | rejected | REJECTED-BY-VERIFIER (panel sa keep) |
| M | keep | confirmed | ADMITTED (supports) |
| SD | keep | confirmed | ADMITTED (supports) |
| C | keep | confirmed | ADMITTED (supports) |
| V | keep | confirmed | ADMITTED (opposes) |
| KD | keep | confirmed | ADMITTED (supports) |
| L | keep | confirmed | ADMITTED (supports) |
| MP | keep | confirmed | ADMITTED (supports) |

*Gemensam standard:* Gemensam standard (fas4c_rubrik.md, FRYST 2026-05-30) tillämpad sida-vid-sida på alla 8 partier för instrumentet kontroller_och_informationsutbyte_mot_valfardsbrott (kategori valfard). Alla 8 citat verifierades ORDAGRANT mot data.riksdagen.se/dokument/<dok_id>.text (WebFetch + rå curl/Python där summeringsmodellen var osäker). VIKTIGT: L:s och MP:s citat 'försvann' vid naiv grep p.g.a. mjukbindestreck (&#xad;) och span-taggar i .text-HTML; efter tag-/entitet-strippning matchade båda citaten exakt — inga rader förkastades p.g.a. detta artefaktfel. BUNTEN-REGELN (§2) tillämpad SYMMETRISKT på alla buntade källor (S, SD, C, KD, L, MP): varje rad behölls eftersom citatet är instrument-exakt, och intern nyans skrevs i mapping_note utan att förkasta raden. Detta harmoniserar det tidigare dokumenterade M/L-felet: M:s och L:s analoga buntade ståndpunkter behandlas nu lika (båda gäller). C-fallet är det skarpaste nyans-testet: C yrkar avslag på en SPECIFIK kontrollvariant (FK-åtkomst till arbetsgivardeklaration) men förespråkar instrumentet (myndigheter delar data mot felaktiga utbetalningar) i samma motion — per §2 noteras avslaget som nyans och förkastar inte raden; C kodas supports (medium) likt övriga datadelnings-förespråkare. ENSKILD MOTION-regeln (§3) tillämpad: M (HC023146) är panelens enda enskilda motion (Josefin Malmqvist ensam undertecknare) => confidence sänkt till low; ingen starkare partikollektiv M-källa med instrument-exakt yrkande i senaste mandatperioden fanns, men eftersom källan ändå är instrument-exakt behölls raden på low (ej unknown). TIDSREGELN (§4) tillämpad symmetriskt: KD (2021/22) och L (2021/22) är utanför föredragen senaste mandatperiod — noterat lika för båda, godtaget då ingen nyare instrument-exakt partikollektiv källa krävdes; inget strängare tidskrav lades på något parti. INGEN UTJÄMNING (§8): utfallet 7 supports / 1 opposes (V) är asymmetriskt och bevaras avsiktligt — V:s avslag på prop. 2024/25:180 (sekretessbrytande bestämmelse för utökat informationsutbyte mot felaktiga utbetalningar/välfärdsbrott) är instrument-exakt opposes och jämnades INTE ut mot någon önskad fördelning. Inga rader hamnade i rejected: alla 8 kandidatkällor var instrument-exakta, rätt-riktade och verbatim-verifierade.

### trygghet / `behandlingsprogram_kriminalvard`
| parti | panelbeslut | verifierare | utfall |
|---|---|---|---|
| S | keep | confirmed | ADMITTED (supports) |
| M | keep | confirmed | ADMITTED (supports) |
| SD | unknown | — | UNKNOWN |
| C | keep | confirmed | ADMITTED (supports) |
| V | keep | confirmed | ADMITTED (supports) |
| KD | keep | confirmed | ADMITTED (supports) |
| L | keep | confirmed | ADMITTED (supports) |
| MP | keep | confirmed | ADMITTED (supports) |

*Gemensam standard:* GEMENSAM STANDARD TILLÄMPAD SIDA VID SIDA (fas4c_rubrik.md, fryst 2026-05-30) för instrumentet 'Kriminalvårdens behandlingsprogram (återfallsförebyggande)':

§1 INSTRUMENT-EXAKT: stance endast om källan rör samma policyinstrument, ordagrant citat. Verifierade samtliga 8 citat mot data.riksdagen.se .text (direkt råtext-hämtning där WebFetch-sammanfattaren var osäker). S, M, C, V, L namnger 'behandlingsprogram' explicit och kopplas till kriminalvård/återfall => alla supports. KD likaså men enskild motion. MP använder umbrella-termen 'behandlingsverksamhet' kopplad till återfall — bedöms som samma instrument (se nedan). SD saknar instrument-exakt källa => unknown.

§2 BUNTEN-REGEL tillämpad symmetriskt och avgörande: alla godkända rader (S svar på Riksrevisionen, M 'effektiv kriminalvård', C prop.-svar, V kapitelmotion, L 'Liberal rättspolitik', MP Riksrevisionssvar) är buntade motioner. Ingen rad förkastades på grund av intern nyans (M: 'under häktestiden'; V: reservation mot koppling till villkorlig frigivning; MP: obligatorisk behandling för vissa brottstyper; L: bunt med yrkesutbildning). Nyanserna noterade i mapping_note, aldrig som förkastningsskäl. Detta är den direkta rättelsen av den tidigare dokumenterade M/L-asymmetrin: M:s och L:s analoga buntade ståndpunkter behandlas nu LIKA — båda gäller.

§3 KÄLLHIERARKI + ENSKILD MOTION tillämpad symmetriskt: M uppgraderades från enskild motion (HD023389) till partikollektiv kommittémotion (H9023779) per hierarkin. KD är det enda partiet vars enda instrument-exakta belägg är en ENSKILD motion (1 undertecknare verifierad) => confidence=low (ej unknown, eftersom belägget är instrument-exakt och verifierat, och ingen starkare partikollektiv källa finns). Ingen starkare källa fabricerades.

§4 TIDSREGEL tillämpad symmetriskt: M (2021/22), C (2018/19), V (2021/22), L (2021/22) ligger utanför föredragen period; alla fyra accepteras på samma grund (ingen nyare instrument-exakt partikollektiv källa) och noteras lika i mapping_note. Inget parti hölls till strängare tidskrav. S (2024/25), MP (2024/25), KD (2025/26) ligger i föredragen period.

HARMONISERINGSBESLUT MP vs S (centralt): S och MP svarar på SAMMA Riksrevisionsrapport (skr. 2024/25:29 om Kriminalvårdens behandlingsverksamhet). S:s citat säger 'behandlingsprogram', MP:s säger 'behandlingsverksamhet ... den dömdes risk för återfall ska minimeras'. För att inte hålla MP till en strängare instrument-strikthet än S (vilket annars vore en isolerings-inducerad asymmetri som rubriken §9 ska eliminera) bedöms MP:s umbrella-term som samma instrument, men confidence sätts en notch lägre (medium) än parterna som namnger programmet explicit (high) — defensibel gradering inom samma standard, inte drop.

§8 INGET TÄCKNINGSMÅL: SD-luckan fylldes INTE. Utfallet är medvetet asymmetriskt — 7 supports, 0 opposes, 1 unknown — eftersom det är vad de instrument-exakta källorna faktiskt visar. Ingen utjämning mot en önskad fördelning. Konfidensspridning (5 high, 1 medium MP, 1 low KD) speglar källstyrkan, inte en kvot."}

### trygghet / `fokuserad_avskrackning_gvi`
| parti | panelbeslut | verifierare | utfall |
|---|---|---|---|
| S | keep | confirmed | ADMITTED (supports) |
| M | unknown | — | UNKNOWN |
| SD | unknown | — | UNKNOWN |
| C | unknown | — | UNKNOWN |
| V | keep | confirmed | ADMITTED (supports) |
| KD | unknown | — | UNKNOWN |
| L | unknown | — | UNKNOWN |
| MP | keep | confirmed | ADMITTED (supports) |

*Gemensam standard:* Gemensam standard tillämpad sida-vid-sida enligt rubrikens panel-protokoll (§9). (1) INSTRUMENT-REGEL (§1): stance krävde källa om SAMMA policyinstrument. 'Sluta skjut' godtogs som instrument-exakt eftersom det är det etablerade svenska namnet på fokuserad avskräckning/GVI (gruppvåldsintervention) — detta bekräftades direkt i V- och MP-texterna ('gruppvåldsintervention (GVI)', 'metoden GVI, Group Violence Intervention'). Allmänna trygghetsmål godtogs ALDRIG. (2) Alla tre supports-citat verifierades ORDAGRANT mot rå .text från data.riksdagen.se (inte enbart konverterad markdown — den lilla fetch-modellen rapporterade felaktigt att V:s GVI-omnämnande/quote saknades, men rå-texten visade att V:s mapping_note var korrekt och citatet verbatim). (3) BUNTEN-REGELN (§2) tillämpades LIKA: S och MP buntar båda 'Sluta skjut' med andra instrument (avhopparverksamhet m.m.); i båda fallen godtogs raden eftersom det namngivna instrumentet citeras exakt, och bunt-nyansen noterades endast i mapping_note — aldrig som förkastningsskäl. (4) KÄLLHIERARKI + ENSKILD-MOTION-REGEL (§3) tillämpades symmetriskt: S och V är partikollektiva kommittémotioner från senaste mandatperioden => keep/high. MP:s källa klassas av riksdagen som 'Enskild motion' (två namngivna ledamöter, ej m.fl./kommitté/parti/budget); per §3 hålls den men nedgraderas till confidence=low då ingen starkare partikollektiv MP-källa finns. Detta är harmonisering av STANDARDEN (svagare källklass => lägre confidence), inte av slutsatsen. (5) FÖRKASTADE KANDIDATER behandlades med samma instrument-tröskel oavsett parti: M:s statistik-fr, SD:s Nato-'avskräckning', C:s jakt-'skjut'/2003-interpellation och L:s försvars-/straffrätts-'avskräckning' förkastades alla på §1 (fel instrument / ej instrument-ståndpunkt / utanför hierarkin). (6) INGET TÄCKNINGSMÅL (§8): de fem luckorna (M, SD, C, KD, L) lämnades som unknown — fördelningen (3 supports, 0 opposes, 5 unknown) speglar att instrumentet i riksdagskorpusen drivs av V/S/MP och inte beläggs instrument-exakt av Tidö-/M-blocket; asymmetrin lämnades orörd."

### trygghet / `situationell_prevention_utomhusbelysning`
| parti | panelbeslut | verifierare | utfall |
|---|---|---|---|
| S | keep | rejected | REJECTED-BY-VERIFIER (panel sa keep) |
| M | unknown | — | UNKNOWN |
| SD | keep | confirmed | ADMITTED (supports) |
| C | keep | rejected | REJECTED-BY-VERIFIER (panel sa keep) |
| V | add | confirmed | ADMITTED (supports) |
| KD | keep | confirmed | ADMITTED (supports) |
| L | keep | confirmed | ADMITTED (supports) |
| MP | keep | confirmed | ADMITTED (supports) |

*Gemensam standard:* Gemensam standard tillämpad sida-vid-sida (rubrik §1-§4, §9). (1) INSTRUMENT-REGELN (§1): stance endast vid källa om SAMMA policyinstrument (utomhusbelysning som brottsförebyggande/trygghetsåtgärd), ej blott målet trygghet. Detta fällde M (vägbelysning = trafiksäkerhet, samma mål ej instrument => unknown). (2) BUNTEN-REGELN (§2): alla buntade källor (S, C, KD, L, MP, V) namnger belysning instrument-exakt inom ett paket av fysiska åtgärder; bunten förkastades ALDRIG, intern nyans ('vill även annat', 'bara ett exempel', 'inte bländar') noterades i mapping_note men användes aldrig som skäl att fälla. (3) ENSKILD MOTION (§3): S (Backeskog) och SD (Westmont) är enskilda motioner => confidence=low, symmetriskt; ingen av dem nedgraderades hårdare än den andra trots att SD:s citat är textuellt starkast. Kommittémotion (C/HB022738) och partimotion (L, MP, V) räknas som partikollektiva enligt §3 även när en namngiven person står som undertecknare => medium. (4) TIDSREGELN (§4): KD (2015/16) och L (2021/22) ligger utanför föredragen period 2022/23-2025/26; äldre källa tillåts symmetriskt och noteras, ingen fick strängare tidskrav. PIVOT/HARMONISERING (§9.4 'harmonisera standarden, inte slutsatsen'): Researchen hade behandlat V STRÄNGARE än L/C/MP — V:s 'Väl upplysta gångstråk och gångtunnlar ... ökar tryggheten' (motivtext i partimotion HA021217) sattes unknown med skälet 'beskrivande exempel, ej yrkande', medan L:s 'God belysning ... ökar tryggheten' och C:s 'belysning och liknande åtgärder' (också motivtext utan dedikerat belysnings-yrkande) godkändes som supports. Det är exakt den isolerings-inducerade verifierar-asymmetri rubriken finns för att rätta (jfr det dokumenterade M/L-felet i §2). Jag harmoniserade UPPÅT: V adderas som supports (medium) under samma standard som L/C/MP/KD. Ingen utjämning av supports/opposes-fördelning (§8) styrde detta — V:s källa är genuint instrument-exakt och partikollektiv; M lämnades som unknown trots att det ger asymmetriskt utfall (7 supports / 1 unknown), eftersom verkligheten är asymmetrisk och ingen lucka får fyllas utan instrument-exakt källa (§8). Alla sju keep/add-citat verifierades ORDAGRANT mot dokumentens .text på data.riksdagen.se (§10).

### trygghet / `psykosociala_insatser_frivard`
| parti | panelbeslut | verifierare | utfall |
|---|---|---|---|
| S | unknown | — | UNKNOWN |
| M | unknown | — | UNKNOWN |
| SD | unknown | — | UNKNOWN |
| C | unknown | — | UNKNOWN |
| V | drop | — | DROP |
| KD | unknown | — | UNKNOWN |
| L | unknown | — | UNKNOWN |
| MP | unknown | — | UNKNOWN |

*Gemensam standard:* Gemensam standard tillämpad sida-vid-sida enligt fas4c_rubrik.md §1, §2, §9. KÄRNPRINCIP: instrumentet 'psykosociala insatser i frivården' kräver att källan namnger just psykosociala insatser LEVERERADE VIA frivården (§1 instrument-exakt). Generella 'behandlingsprogram inom Kriminalvården', 'frivårdsinsatser', 'sociala insatser', anstaltsbaserad behandling, återfallsförebyggande HoS, eller 'psykosocial' i annan kontext (Sis/psykiatri/arbetsmiljö) är samma MÅL/OMRÅDE men ett ANNAT instrument och räknas aldrig.

HARMONISERINGSPUNKT (§9.3-9.4): Alla 8 partier har en strukturellt identisk närmiss — ett brett behandlings-/frivårdsförslag som inte namnger det specifika instrumentet. Samtliga behandlas LIKA: ingen får ett strängare och ingen ett lösare krav. Detta gäller särskilt V, som var det enda parti vars research hade en proposed_quote (HD022788). Jag behandlade V exakt som övriga: eftersom citatet refererar 'sociala insatser'/'behandlingsprogram' och dokumentet helt saknar ordet 'psykosocial' (verifierat mot data.riksdagen.se/dokument/HD022788.text), är det inte instrument-exakt. V droppas därför till unknown — INTE för att jämna ut fördelningen, utan för att den lika standarden kräver det.

BUNTEN-REGELN (§2): Tillämpades men aktiverades för inget parti. Bunten-regeln räddar en rad endast när det BUNTADE citatet i sig är instrument-exakt och den enda invändningen är intern nyans. Här är problemet inte intern nyans utan att inget citat över huvud taget namnger instrumentet; därför finns ingen bunt att rädda.

INGET TÄCKNINGSMÅL (§8): Utfallet är fullständigt tomt (8/8 unknown). Detta är en äkta coverage-lucka (§6): instrumentet är reellt men ingen partikollektiv riksdagskälla namnger det specifikt. Asymmetri/tomhet är tillåtet utfall; luckan fylls inte och fördelningen jämnas inte ut. Konfidens 'low' anges för unknown-raderna då bedömningen vilar på frånvaro av träff snarare än positiv beläggning.

### integration / `aktiveringskrav_ekonomiskt_bistand`
| parti | panelbeslut | verifierare | utfall |
|---|---|---|---|
| S | keep | confirmed | ADMITTED (supports) |
| M | keep | confirmed | ADMITTED (supports) |
| SD | keep | confirmed | ADMITTED (supports) |
| C | keep | confirmed | ADMITTED (supports) |
| V | keep | confirmed | ADMITTED (opposes) |
| KD | keep | confirmed | ADMITTED (supports) |
| L | keep | confirmed | ADMITTED (supports) |
| MP | keep | rejected | REJECTED-BY-VERIFIER (panel sa keep) |

*Gemensam standard:* GEMENSAM STANDARD (FRYST RUBRIK docs/fas4c_rubrik.md), tillämpad sida vid sida för alla 8 partier på instrumentet 'aktiveringskrav för ekonomiskt bistånd/socialbidrag'. UTFALL: 8 keep, 0 drop, 0 unknown. Fördelning: 7 supports (S, M, SD, C, KD, L, MP), 1 opposes (V).

1) INSTRUMENT-EXAKTHET (§1): Alla åtta källor rör SAMMA policyinstrument — aktivitetskrav/aktivitetsplikt/motprestation som villkor för försörjningsstöd (= ekonomiskt bistånd/socialbidrag) — inte bara det allmänna målet 'fler i arbete'. Sökordet 'aktiveringskrav' saknas i samtliga källor; instrumentet uttrycks konsekvent med synonymerna 'aktivitetskrav'/'aktivitetsplikt'/'krav på aktivitet'/'motprestation' + 'försörjningsstöd' (alla i sökordslistans instrumentfamilj). Denna synonymtolkning tillämpades LIKA för alla — ingen fick strängare ordkrav.

2) BUNTEN-REGELN (§2) HARMONISERAD — den centrala likabehandlingen: S, C och MP är alla 'med anledning av prop. 2025/26:207'-källor som stödjer instrumentet men buntar in reservationer/nyanser om dess UTFORMNING (S: organiserad brottslighet/barnomsorg/tillsynsmyndighet; C: nystartsår/uppföljning/proportionerlig tillsyn; MP: res. 2/4/5/7 om omfattning, tillsyn, uppföljning). Per §2 förkastas raden ALDRIG för intern nyans när citatet är instrument-exakt — alla tre kodas supports. Likaså M, SD, L, KD: breda motioner (integration, hel socialtjänst, budgetmotion) där det citerade stycket är instrument-exakt => raden räknas, bredden noteras endast. Ingen bunt förkastades för någon part.

3) KÄLLHIERARKI + ENSKILD MOTION (§3): Symmetriskt tillämpad. För M och KD fanns instrument-exakta ENSKILDA motioner (M: HD021533 2025/26; KD: H9022978) som per §3 endast får ge confidence=low och bara om ingen starkare partikollektiv källa finns. För BÅDA fanns en starkare partikollektiv källa (M: partimotion H9024033; KD: kommittémotion H9024212), så raderna kodades mot dessa med confidence=high. Samma logik (uppgradera till starkaste partikollektiva källa) tillämpades lika. V:s källtyp korrigerades till kommittemotion (var 'motion' i research). MP:s rad pekar på den hierarkiskt högsta källan (votering HD19SoU29p1), styrkt av särskilt yttrande.

4) TIDSREGELN (§4) HARMONISERAD: M (2021/22), KD (2021/22) och L (2021/22) vilar alla på källor utanför föredragen mandatperiod (2022/23-2025/26). Per §4 är äldre instrument-exakt källa tillåten om ingen nyare partikollektiv finns — detta noterades symmetriskt i alla tre mapping_notes. Inget parti fick strängare tidskrav. S, C, V, MP vilar på 2025/26-källor (prop. 207-cykeln).

5) ASYMMETRI BEVARAD (§8, inget täckningsmål): V:s opposes (instrument-exakt avslagsyrkande 'Riksdagen avslår proposition 2025/26:207') jämnades INTE ut mot supports. Den 7-1-fördelningen återspeglar verkligheten — sju partier stödjer instrumentet, V motsätter sig det av värdeskäl men på exakt samma instrument, så raden kodas (ej §6-tystnad, eftersom instrument-exakt källa finns).

6) VERIFIERING (no-fabrication, §10): Samtliga åtta citat verifierades ordagrant mot data.riksdagen.se/.text. För M (H9024033) och L (H9024181) returnerade den lättviktiga WebFetch-modellen 'hittas ej' p.g.a. mjuka bindestreck (U+00AD) och dokumentstorlek/trunkering; direkt rå-hämtning bekräftade dock att proposed_quote finns EXAKT i texten. MP:s votering bekräftades via dokumentstatus (MP Ja=18, Nej=0 på förslagspunkt 1) och yttrandecitatet verbatim i HD01SoU29.text. Mjuka-bindestreck-normalisering (borttagning av U+00AD) tillämpades lika för alla citat.

### integration / `riktade_insatser_nyanlanda_elever`
| parti | panelbeslut | verifierare | utfall |
|---|---|---|---|
| S | unknown | — | UNKNOWN |
| M | keep | confirmed | ADMITTED (supports) |
| SD | keep | confirmed | ADMITTED (supports) |
| C | keep | confirmed | ADMITTED (supports) |
| V | add | confirmed | ADMITTED (supports) |
| KD | keep | confirmed | ADMITTED (supports) |
| L | keep | confirmed | ADMITTED (supports) |
| MP | unknown | — | UNKNOWN |

*Gemensam standard:* Tillämpad gemensam standard (FRYST rubrik docs/fas4c_rubrik.md, §1–§9), lika för alla 8 partier. Utfall: 6 supports (M, SD, C, V, KD, L) + 2 unknown (S, MP). 0 opposes. Asymmetrin är ett UTFALL av vilka instrument-exakta källor som faktiskt finns, inte ett mål (rubrik §8).

STANDARDEN:
1) INSTRUMENT-EXAKTHET (§1): stance endast när citatet direkt avser riktade åtgärder i skolan SPECIFIKT för nyanlända elever (förberedelseskola, lovskola+sommarkollo, prioriterad timplan, halverat sommarlov, extra svensklektioner, studiehandledning på modersmål för nyanlända, utredd särskild skolform). Allmänt stödmål eller generell modersmålspolitik räcker ALDRIG — detta fällde S (folkhögskola som anordnare = annat instrument) och MP ('tidigt stöd'/'alla elevers rätt').
2) BUNTEN-REGEL (§2) tillämpad LIKA på M, SD, C, V, KD, L — alla sex vilar på buntade integrations-/skolmotioner. Var och en behålls eftersom det citerade yrkandet/meningen är instrument-exakt; den interna nyansen (t.ex. SD:s parallella önskan att begränsa antalet nyanlända; V:s breda språkpolitik) noteras i mapping_note och används ALDRIG som skäl att förkasta. M/L-symmetrin från rubrikens motivexempel är explicit upprätthållen: M (H9024033) och L (H9024002) är samma slags buntade partimotion och båda behålls.
3) ENSKILD MOTION (§3): ingen keep/add-rad vilar på en enskild ledamotsmotion. Alla sex stödrader är partikollektiva (partimotion/kommittémotion/budgetmotion). S:s Folkhögskolespår (flerledamots) föll på instrument, inte på undertecknarantal.
4) TIDSREGEL (§4) symmetriskt: M, KD, L vilar alla på 2021/22 (en period äldre än föredraget) och behålls var och en med samma motivering — inget nyare partikollektivt instrument-exakt belägg finns. Inget parti fick strängare tidskrav än ett annat. SD (2024/25), C (2022/23), V (2024/25) ligger inom föredragen period.
5) VERBATIM (§10 + INSTRUKTION): varje kvarvarande citat verifierat ordagrant mot rådata-.text via fixed-string-match (M, SD, C, KD, L) eller, för V, efter att inline-HTML-span/soft-hyphen avlägsnats (innehållsorden i exakt ordning). Två summerar-fel upptäcktes och korrigerades vid rådata-verifiering: (a) KD — summerare läste 'sent anlända', men rådatat har 'nyanlända elever' verbatim; (b) M — summerare missade avsnittet pga soft-hyphen i 'kom­binerar', men rådatat har både avsnittsrubriken 'insatser för nyanlända elever' och citatet verbatim. Ingen rad behölls på ett icke-verifierat citat.

LIKABEHANDLING AV TIDIGARE OLIKA-BEDÖMDA PARTIER: V uppgraderades (drop av gammal icke-instrument-exakt 2014/15-rad + add av instrument-exakt 2024/25-rad) så att V nu beläggs på exakt samma kvalitetsnivå som M/SD/C/KD/L i stället för på en svagare/äldre procedurell uppföljningsmotion — harmonisering av STANDARDEN, inte av slutsatsen (§9 punkt 4). C:s belägg (riktad språkutbildning/modersmål för nyanlända, utan ordet 'riktade') behandlades LIKA med V:s studiehandlednings-belägg: sakligt instrument-belägg godtas även när termen 'riktade insatser' inte förekommer ordagrant. Inga luckor (S, MP) fylldes och fördelningen jämnades aldrig ut (§8).

### integration / `sfi_kombinerat_med_praktik`
| parti | panelbeslut | verifierare | utfall |
|---|---|---|---|
| S | keep | confirmed | ADMITTED (supports) |
| M | keep | confirmed | ADMITTED (supports) |
| SD | unknown | — | UNKNOWN |
| C | keep | confirmed | ADMITTED (supports) |
| V | unknown | — | UNKNOWN |
| KD | keep | confirmed | ADMITTED (supports) |
| L | keep | confirmed | ADMITTED (supports) |
| MP | keep | rejected | REJECTED-BY-VERIFIER (panel sa keep) |

*Gemensam standard:* Gemensam standard tillämpad sida vid sida enligt rubrik §9. INSTRUMENT-REGEL (§1): supports endast vid instrument-exakt belägg för SFI kombinerat med praktik/yrkesutbildning (yrkes-sfi/kombinationsutbildning) — allmänt integrationsmål räckte aldrig. Detta fällde SD (bortre tidsgräns + skärpta krav) och V (rätt till sfi, lärarförsörjning, huvudmannaskap, Svenska-från-dag-ett) lika: båda samma mål men fel/annat instrument => unknown, inga rader fabricerade (§8, inget täckningsmål — utfallet 6 supports / 0 opposes / 2 unknown tilläts vara asymmetriskt eftersom de instrument-exakta källorna faktiskt pekar ensidigt åt UTÖKA). BUNTEN-REGEL (§2) tillämpad symmetriskt på L och MP (och S): avsnitt/motioner som buntar flera sfi-förslag förkastades ALDRIG när citatet var instrument-exakt; intern nyans noterades bara i mapping_note. ENSKILD-MOTION-REGEL (§3) tillämpad lika: C (Martina Johansson, enskild) gavs confidence=low och behölls eftersom ingen starkare partikollektiv C-källa var instrument-exakt; KD däremot byttes från enskild motion (HD021563) till starkare partikollektiv kommittémotion (H9024198) per källhierarkin — samma regel, olika utfall pga olika källtillgång. TIDSREGEL (§4) tillämpad symmetriskt: M (2016/17), KD (2021/22) och L (2021/22) ligger utanför föredragen mandatperiod; alla tre fick samma notering och confidence=low enbart pga ålder, medan S (2025/26) och MP (2023/24) fick high. Ingen part fick strängare tidskrav än annan. NO-FABRICATION (§10): jag faktagranskade alla sex supports-citat mot data.riksdagen.se .text. Fem var ordagranna. För L upptäcktes att research-citatet \"Yrkes- sfi\" innehöll ett mellanslag som är en HTML-tagg-artefakt (Yrkes-</span><span>sfi), ej i den faktiska prosan; jag rättade citatet till verbatim \"Yrkes-sfi...\" snarare än att behålla en icke-ordagrann sträng. Tidigare olika-behandling som nu harmoniserats: KD och C behandlades båda under enskild-motion-regeln men utföll olika ENDAST därför att KD hade en starkare partikollektiv källa tillgänglig och C inte — regeln, inte slutsatsen, är gemensam.

### integration / `sprakpraktik_kombinerad_sprakutbildning_och_arbetspraktik`
| parti | panelbeslut | verifierare | utfall |
|---|---|---|---|
| S | unknown | — | UNKNOWN |
| M | unknown | — | UNKNOWN |
| SD | unknown | — | UNKNOWN |
| C | keep | confirmed | ADMITTED (supports) |
| V | keep | confirmed | ADMITTED (supports) |
| KD | keep | confirmed | ADMITTED (supports) |
| L | drop | — | DROP |
| MP | keep | confirmed | ADMITTED (supports) |

*Gemensam standard:* Tillampad gemensam standard for instrumentet 'sprakpraktik (sprakutbildning + arbetspraktik)', sida vid sida over alla 8 partier enligt fas4c-rubriken.

KARNTEST (bunten-regeln, rubrik 2): C, V och MP har alla en partikollektiv kalla som buntar 'sprak/sprakutbildning + praktik' i ett namngivet program (C: intensivaret 'kombinerar insatser for sprak och praktik'; V: 'matchning fran dag 1' med 'sprakutbildning, praktik'; MP: 'sfi-undervisning som kombineras med praktik' / 'forena studierna med arbetspraktik'). Alla tre citat ar instrument-exakta for sprak+praktik-delen. Enligt rubrik 2 raknas raden for det namngivna instrumentet och bunt-nyansen (att programmet aven innehaller jobb/mentorskap/kartlaggning/subventionerade anstallningar) skrivs i mapping_note men anvands ALDRIG som skal att forkasta. Darfor: alla tre = keep/supports. Detta ar den direkta tillampningen av den i rubriken dokumenterade M/L-asymmetri-rattelsen: analoga buntade kollektiva kallor bedoms lika.

ENSKILD-MOTION-REGELN (rubrik 3): KD:s instrument-exakta kalla (HD021563, 'sprakundervisning kombineras med ... yrkespraktik') ar lika instrument-exakt som C/V/MP, MEN ar en enskild motion (enda intressent). Den skiljs INTE pa instrument-exakthet utan enbart pa kalltyp: enligt rubrik 3 far enskild motion representera partilinjen endast med confidence=low och endast nar ingen starkare kollektiv kalla finns (bekraftat). Darfor keep/supports men confidence=low - symmetriskt med hur alla partiers enskilda motioner ska behandlas.

DROP SOM HARMONISERING (rubrik 9.4): L:s tidigare kodade supports-rad (H9023965) droppas eftersom re-verifiering visar att citatet (a) inte ar instrument-exakt (komponenttermerna saknas i .text) och (b) pekar at fel riktning (kritik mot langdragna sfi/praktik-varvningar => begransa). Detta ar 'harmonisera standarden, inte slutsatsen': nar den lika standarden kraver att en rad droppas snarare an att en analog adderas, droppas den. L far darfor unknown - INTE for att jamna ut, utan for att L:s faktiska citat saknar det positiva, instrument-exakta innehall som C/V/MP/KD har.

TIDSREGEL (rubrik 4): MP:s kalla ar fran 2002/03, langt utanfor foredragen mandatperiod och hela 2014-2026-fonstret. Tidsregeln tillats symmetriskt: aldre instrument-exakt kalla far anvandas nar ingen nyare finns (bekraftat: 'sprakpraktik' parti=MP=0; nyare MP-motioner ror endast separat sfi-ratt). Aldern noteras och confidence sanks till medium - men inget strangare tidskrav lades pa MP an pa ovriga.

AKTA LUCKOR (rubrik 8, inget tackningsmal): S, M, SD har ingen instrument-exakt kalla (S:s starkaste kollektiva kalla anvander arbetsmarknadsutbildning+arbetspraktik, ej sprakutbildning; M/SD saknar komponenttermerna i sina integrationsdokument). Allmanna integrationsmal racker aldrig (rubrik 1). Dessa forblir unknown - luckorna fylls inte.

UTFALL (asymmetriskt och tillatet): keep/supports C (high), V (high), MP (medium), KD (low); drop->unknown L; unknown S, M, SD. Fordelningen ar ett utfall av vilka instrument-exakta kallor som faktiskt finns, inte ett mal. Endast data.riksdagen.se anvant; inga citat fabricerade (samtliga citat kopierade ordagrant ur research proposed_quote).

### forsvar / `ateraktiverad_utokad_varnplikt`
| parti | panelbeslut | verifierare | utfall |
|---|---|---|---|
| S | keep | confirmed | ADMITTED (supports) |
| M | keep | confirmed | ADMITTED (supports) |
| SD | keep | confirmed | ADMITTED (supports) |
| C | keep | confirmed | ADMITTED (supports) |
| V | keep | confirmed | ADMITTED (supports) |
| KD | keep | confirmed | ADMITTED (supports) |
| L | keep | confirmed | ADMITTED (supports) |
| MP | unknown | — | UNKNOWN |

*Gemensam standard:* Gemensam standard tillämpad sida vid sida på alla 8 partier per den frysta rubriken (docs/fas4c_rubrik.md §1-§4, §8-§10). (1) STANCE = endast vid instrument-exakt belägg som namnger instrumentet 'återaktiverad/utökad värnplikt' (mönstring/grundutbildning/värnpliktsvolymer/återaktivering) med riktning — allmänna mål om 'starkt försvar/totalförsvar' räcker aldrig. (2) BUNTEN-REGELN (§2) tillämpades LIKA på S, M, V och KD: deras citat buntar värnplikten med andra instrument (regementen/hemvärn, GSS/K-T, HR-villkor, reservofficerare) men eftersom det namngivna instrumentet citeras instrument-exakt räknas raderna; den interna nyansen noterades i mapping_note och förkastade ALDRIG någon rad. Detta är exakt det fel som §2 rättar (M:s buntade godkändes en gång men L:s analoga förkastades) — här bedöms alla buntade declarativa partilinjer symmetriskt: instrument-exakt citat => raden gäller. (3) Alla sju keep-källor är partikollektiva kommittémotioner (ej single-member, §3) — ingen tvingades till confidence=low; votering saknades för alla, så kommittémotion (näst i hierarkin) användes genomgående. (4) TIDSREGELN (§4) tillämpades symmetriskt: S/C/V senaste mandatperioden (high), medan M (2021/22), KD (2021/22) och L (2015/16) är utanför föredragen period — detta noterades för alla tre och sänkte confidence till medium (ingen fick strängare tidskrav än annan). (5) MP avvisades som äkta lucka (unknown): dess enda värnplikts-mening är beskrivande bakgrundsprosa utan instrument-exakt proposition, och dess yrkanden rör dagersättning (ersättning) och civilplikt (annat instrument). Detta är INTE en strängare måttstock än keep-partiernas — skillnaden är att MP:s text aldrig gör en instrument-exakt proposition om själva instrumentet, så bunten-regeln har inget instrument-exakt citat att rädda. (6) NO FABRICATION (§10): samtliga sju citat verifierades ordagrant mot råtexten på data.riksdagen.se (Grep/curl mot .text). Särskilt S- och V-citaten innehåller &#xa0;-tokens (non-breaking space) i sifferparen 10/12/20 000 i råmarkupen; efter HTML-strip och nbsp->vanligt mellanslag matchar citaten exakt — WebFetch-summeringsmodellen missade S-meningen eftersom den spänner över <span>-taggar, men direkt Grep mot råtexten bekräftade den. (7) INGET TÄCKNINGSMÅL (§8): utfallet är medvetet asymmetriskt (7 supports, 0 opposes, 1 unknown) eftersom det speglar de faktiskt funna instrument-exakta källorna; ingen lucka fylldes utan belägg och fördelningen jämnades aldrig ut.

### forsvar / `tydlig_statlig_styrning_civilt_forsvar`
| parti | panelbeslut | verifierare | utfall |
|---|---|---|---|
| S | keep | confirmed | ADMITTED (supports) |
| M | keep | confirmed | ADMITTED (supports) |
| SD | keep | confirmed | ADMITTED (supports) |
| C | keep | rejected | REJECTED-BY-VERIFIER (panel sa keep) |
| V | keep | confirmed | ADMITTED (supports) |
| KD | drop | — | DROP |
| L | keep | confirmed | ADMITTED (supports) |
| MP | unknown | — | UNKNOWN |

*Gemensam standard:* Gemensam standard tillämpad sida-vid-sida (rubrik §9). KÄRNTEST: instrumentet tydlig_statlig_styrning_civilt_forsvar kräver att källans citat rör en STYRNINGS-/GOVERNANCE-MEKANISM riktad mot staten/regeringen för civilt försvar (myndighetsuppdrag/-struktur, central kravställning+uppföljning, ledningsstruktur, lednings-/samordningsansvar, reglering/styrning av beredskapen) — inte enbart det allmänna målet att 'stärka/bygga upp/intensifiera civilt försvar' (§1). Den exakta frasen 'statlig styrning' krävs INTE ordagrant; den prövas via funktionell governance-text. Denna standard tillämpades LIKA: keep+supports för S (MSB-uppdrag + nya statliga myndighetsstrukturer), M (tydliga krav/riktlinjer/resultatmål + uppföljning + MSB övergripande ansvar), SD (tydlig ledning och styrning + sanktioner), C (eget avsnitt 'Tydligare styrning av svensk beredskap' + revidering av principerna), V (offentlig styrning av samhällsviktig verksamhet + ansvars-/ledningsförhållanden), L (krisledningsansvar hos statsministern via statsrådsberedningen + nationellt säkerhetsråd, under rubrik 'Civilt försvar'>'Tydlig ledningsstruktur'). BUNTEN-REGELN (§2) tillämpades symmetriskt på alla sex: samtliga är bredd-/buntmotioner, men eftersom citatet i varje fall är instrument-exakt förkastas ingen rad p.g.a. intern nyans (noteras i mapping_note). HARMONISERA STANDARDEN, INTE SLUTSATSEN (§9.4): KD och MP föll på SAMMA test — deras citat/yrkanden är endast det allmänna målet ('intensifieras och påskyndas', 'att stärka det civila försvaret') utan någon styrnings-/ledningsmekanism. KD droppades alltså från en tidigare supports (H9023908) till unknown, och MP förblir unknown — inte p.g.a. strängare krav utan p.g.a. att den lika standarden kräver instrument-exakt governance-text som dessa två källor saknar. INGET TÄCKNINGSMÅL (§8): luckorna for KD/MP fylldes inte. Utfallet är medvetet asymmetriskt (6 supports, 2 unknown) eftersom källäget är det. Alla sex behållna citat verifierades ORDAGRANT mot data.riksdagen.se .text (S yrk. 81, M yrk. 5, SD kontinuerlig mening med soft-hyphens borttagna, C inkl. inledande 'Det är rimligt ändamålsenligheten' + rubrik, V hela meningen, L kontinuerlig passage); inget citat fabricerat. Tidsregel (§4) symmetrisk: M (2021/22) och L (2020/21) ligger utanför föredragen senaste period men tillåts då ingen instrument-exakt nyare partikollektiv källa hittades — noterat i båda mapping_note. Källhierarki (§3): samtliga behållna är partikollektiva (kommitté-/flerpersonsmotioner), ingen enskild motion åberopad; voteringar saknades på exakt instrument. C source_type korrigerad från 'motion' till 'kommittemotion'; V confidence satt till medium (motion utan voteringsstöd + 'offentlig' snarare än enbart 'statlig' styrning), övriga keep high utom S/SD/M/C/L high.

### demokrati / `atgarder_mot_otillaten_paverkan_offentlig_sektor`
| parti | panelbeslut | verifierare | utfall |
|---|---|---|---|
| S | keep | confirmed | ADMITTED (supports) |
| M | unknown | — | UNKNOWN |
| SD | add | rejected | REJECTED-BY-VERIFIER (panel sa add) |
| C | add | confirmed | ADMITTED (supports) |
| V | add | rejected | REJECTED-BY-VERIFIER (panel sa add) |
| KD | unknown | — | UNKNOWN |
| L | add | confirmed | ADMITTED (supports) |
| MP | keep | confirmed | ADMITTED (supports) |

*Gemensam standard:* Gemensam standard (FRYST rubrik docs/fas4c_rubrik.md §1-§4, §8-§9) tillämpad sida vid sida på alla 8 partier.

INSTRUMENT-REGEL (§1): stance endast vid samma policyinstrument (åtgärder mot otillåten/otillbörlig påverkan, korruption, infiltration, hot/våld mot offentlig sektor — kommuner, regioner, statliga myndigheter, tjänstemän), inte vid delat mål. Term-match krävs INTE — synonyma konkreta instrument (bakgrundskontroller mot infiltration, antikorruptionsmyndighet, stödfunktion mot otillbörlig påverkan, straffskydd för offentliganställda) räknas om de avser samma instrument.

BUNTEN-REGEL (§2) tillämpad LIKA på de tre partikollektiva buntade källorna S (HD023586), C (HD023581) och MP (HB022669): alla tre buntar flera instrument men har instrument-exakt namngivet yrkande => alla tre behålls (keep/add, supports), intern nyans noteras endast i mapping_note. Ingen bunt förkastas. Detta är den centrala harmoniseringen: tidigare risk var att en buntad källa godkändes för ett parti men förkastades för ett annat — här bedöms S, C, MP identiskt.

ENSKILD MOTION-REGEL (§3) tillämpad LIKA på SD (HD02247) och L (HD022663): båda enskilda motioner med instrument-exakta yrkanden => båda supports men confidence=low (ej droppade, ingen starkare partikollektiv källa fanns). Identisk behandling.

ASYMMETRIN harmoniserad korrekt (§9.4 \"harmonisera standarden, inte slutsatsen\"): M:s rad (HB02767) DROPPAS trots att den också är en enskild motion som SD/L — men skälet är INTE strängare källtypskrav utan att M:s yrkanden (anonymisering) inte är instrument-exakta medan motiveringens \"otillåten påverkan\" bara är problembeskrivning. SD och L har instrument-exakta yrkanden, M har det inte. Standarden är alltså identisk; utfallet skiljer sig för att verkligheten skiljer sig.

KÄLLHIERARKI (§3): V belagt via votering (guldstandard, JuU29/prop. 2024/25:141, V röstade Ja 17-0-1-6). S/C/MP via partikollektiva (kommitté-/parti)motioner => high. SD/L via enskilda motioner => low.

INGET TÄCKNINGSMÅL (§8): KD förblir unknown (äkta lucka, ingen instrument-exakt källa i någon period); luckan fylls inte. M:s lucka fylls inte heller. Fördelningen jämnas inte ut.

VERIFIERING: samtliga keep/add-citat hämtades och kontrollerades ordagrant mot data.riksdagen.se .text/votering (S yrkande 50, SD yrkande, C yrkande 33 + bakgrund, V voteringsutfall, L yrkande, MP mening + Riksrevisionen-yrkande) — alla matchar.

UTFALL: 6 supports (S high, C high, V high, MP high, SD low, L low), 2 unknown (M, KD). Asymmetriskt utfall (inga opposes) återspeglar att samtliga belagda partilinjer vill INFÖRA/UTÖKA åtgärder mot otillåten påverkan mot offentlig sektor; ingen instrument-exakt opposes-källa fanns.

### demokrati / `starkt_oberoende_granskning_och_insyn`
| parti | panelbeslut | verifierare | utfall |
|---|---|---|---|
| S | keep | confirmed | ADMITTED (supports) |
| M | add | confirmed | ADMITTED (supports) |
| SD | keep | confirmed | ADMITTED (supports) |
| C | keep | confirmed | ADMITTED (supports) |
| V | keep | confirmed | ADMITTED (supports) |
| KD | add | confirmed | ADMITTED (supports) |
| L | add | confirmed | ADMITTED (supports) |
| MP | keep | confirmed | ADMITTED (supports) |

*Gemensam standard:* Gemensam standard tillämpad sida vid sida (rubrik docs/fas4c_rubrik.md, fryst 2026-05-30) over alla 8 partier. Alla 8 citat verifierade ordagrant mot hämtad .text pa data.riksdagen.se innan beslut.

(1) INSTRUMENT-REGELN (§1): stance endast vid SAMMA policyinstrument. Tva befintliga rader droppades for att de bara delade ett allmänt mål: KD H9024186 (abstrakt normprövning + anslag; offentlighetsprincip endast i allmän principtext) och L H8024091 (visselblåsardirektiv = arbetsrättsligt skydd). Samma 'allmänt mål räcker aldrig'-tröskel tillämpades pa båda — den symmetriska rättelsen mot tidigare risk att bedöma dem olika strängt.

(2) BUNTEN-REGELN (§2): C (HD023583), MP (HA02181), S (HD024024) och V (HD023996) ar buntade motioner med flera yrkanden. For samtliga: instrument-exakt citat => raden gäller, intern nyans skrivs i mapping_note och anvands ALDRIG som skäl att förkasta. C och MP — bägge buntade insyn/transparens-motioner — behandlades nu IDENTISKT (keep/supports/high).

(3) ENSKILD-MOTION-REGELN (§3): symmetriskt confidence=low for alla single-member-källor. Viktigaste harmoniserade fallet: M (HD021743) vs L (HD023766) — bägge av riksdagen klassade som subtyp 'Enskild motion' MEN med flera partiundertecknare ('m.fl.' / 3 namn). Bägge behandlades lika: instrument-exakt citat => raden gäller pa low, varken upphöjd till partikollektiv eller förkastad. SD (HD021701) och KD (HD021556) ar äkta en-undertecknar-motioner => också low. Ingen starkare partikollektiv kalla fanns for nagon av dessa fyra; var och en hade en verifierbar instrument-exakt enskild kalla, sa ingen utelämnades.

(4) TIDSREGELN (§4): sju partier har källor fran senaste mandatperioden (de flesta 2025/26). MP:s enda instrument-exakta partikollektiva kalla ar rm 2022/23; per §4 far äldre kalla anvandas nar ingen nyare finns och detta noteras explicit i MP:s mapping_note — inget strängare tidskrav pa MP.

(5) INGET TÄCKNINGSMÅL (§8): fördelningen jämnades INTE ut. Utfallet blev 8/8 supports — ett äkta asymmetriskt utfall: varje instrument-exakt kalla som faktiskt hittades pekar mot att UTÖKA/STÄRKA insyn och oberoende granskning (offentlighetsprincip, Riksrevisionens uppdrag, transparens i partifinansiering). Inga opposes-källor fabricerades eller söktes for balans; inga luckor fylldes utan instrument-exakt belägg. De tva droppade raderna ersattes endast for att äkta instrument-exakta (om än enskilda, low) källor fanns; annars hade KD/L blivit unknown.

(6) KÄLLHIERARKI (§3): votering > parti-/kommitté-/budgetmotion > valmanifest, endast data.riksdagen.se. Inga voteringar hittades; bästa tillgängliga ar partikollektiva motioner (S, C, V, MP) respektive enskilda motioner (M, SD, KD, L). Confidence speglar hierarkin konsekvent (partikollektiv high, enskild low)."

### demokrati / `systematiskt_antikorruptionsarbete_kommuner_regioner`
| parti | panelbeslut | verifierare | utfall |
|---|---|---|---|
| S | keep | confirmed | ADMITTED (supports) |
| M | unknown | — | UNKNOWN |
| SD | keep | confirmed | ADMITTED (supports) |
| C | keep | confirmed | ADMITTED (supports) |
| V | unknown | — | UNKNOWN |
| KD | unknown | — | UNKNOWN |
| L | keep | confirmed | ADMITTED (supports) |
| MP | unknown | — | UNKNOWN |

*Gemensam standard:* Gemensam standard tillämpad sida vid sida enligt fryst rubrik fas4c_rubrik.md (§1 instrument-exakt, §2 bunten-regel, §3 källhierarki + enskild-motion-regel, §9 panel-protokoll, §8 inget täckningsmål).

VERIFIERING: Jag hämtade .text för alla fyra supports-källor (HC02445, HD02247, HD023581, HD022663) och bekräftade att citaten är ORDAGRANNA samt antal undertecknare. Resultat: S/SD/L = 1 undertecknare (enskilda motioner) => confidence=low; C = kommittémotion (Ulrika Liljeberg m.fl., JuU) => partikollektiv, confidence=medium. Jag hämtade även M:s HD021760 och bekräftade att den är 'Avpolitisering av den kommunala revisionen' (revisionsreform) som nämner korruption endast som mål.

SYMMETRI / HARMONISERA STANDARDEN INTE SLUTSATSEN (§9.4): Två par behandlades uttryckligen lika där de tidigare riskerat olik bedömning. (1) M och MP: båda har som enda kommun-nära källa en motion om reform av den kommunala REVISIONEN (M: HD021760; MP: H5021712), där korruption endast är mål. Per §1 (samma mål räcker aldrig) förkastas BÅDA till unknown — ingen av dem fick en lösare tolkning än den andra. (2) De tre enskilda supports-motionerna S, SD och L bedöms identiskt: instrument-exakt citat + 1 undertecknare => stance=supports men confidence=low (§3). Ingen av dem höjdes över de andra; C ligger högre (medium) ENBART för att källan är en partikollektiv kommittémotion (§3 källhierarki), inte för att jämna ut.

BUNTEN-REGELN (§2) tillämpad lika för S, SD, C och L: alla fyra citat sitter i breda motioner som buntar flera instrument; eftersom det citerade stycket är instrument-exakt gäller raden, och den interna nyansen (t.ex. L:s 'utreda'-yrkande, SD:s nepotism/utbildningsdelar) noteras i mapping_note men förkastar aldrig raden.

INGET TÄCKNINGSMÅL (§8): Utfallet är medvetet asymmetriskt — 4 supports (S, SD, C, L), 4 unknown (M, V, KD, MP), 0 opposes. Detta speglar vilka instrument-exakta källor som faktiskt finns; inga luckor fylldes och fördelningen jämnades inte ut. V och KD är äkta luckor (deras antikorruptionsmaterial avser nationell nivå resp. bistånd/straffrätt). Inga voteringar fanns för någon part, så källhierarkin landade på motion-nivå genomgående.

## Rejected-candidate-log (luckor, drops, verifierar-underkända)
| parti | åtgärdstyp | panelbeslut | skäl |
|---|---|---|---|
| MP | minskad_klasstorlek | keep | verifierare underkände (confirmed=false): Citatet återfinns ordagrant i fulltexten (HD023364) — quote_found=true. Instrumentet "mindre klasser" namnges explicit i citatet, så det är instrument-exakt (avser minskad klasstorlek, inte enbart ett |
| V | tidiga_insatser_lagstadiet | unknown | UNKNOWN/lucka: ingen instrument-exakt källa. Närmaste sektion (HD022791 m.fl., 3.4 'Tidiga insatser för barn i behov av särskilt stöd') avser uttryckligen FÖRSKOLAN ('redan i förskolan hjälpa och stödja barn i behov av särskilt stöd ... utredning som undersöker om förskolebarn med behov av särskilt  |
| L | tidiga_insatser_lagstadiet | unknown | UNKNOWN: två instrument-exakta men motstridiga kommittémotioner (H5023910 avslag på åtgärdsgarantin 2017/18:18 => opposes-signal; H5024117 acceptans-med-reservation av den reviderade garantin 2017/18:195 => ej opposes, ej rent supports). Ingen källa från innevarande mandatperiod och ingen votering s |
| S | kontroller_och_informationsutbyte_mot_valfardsbrott | keep | verifierare underkände (confirmed=false): Källan är kommittémotion 2025/26:3588 av Ida Karkiainen m.fl. (S), SfU, dok HD023588 — partitillskrivningen till S stämmer. quote_found=true: citatet (Yrkande 13) finns ordagrant i fulltexten. MEN ins |
| SD | behandlingsprogram_kriminalvard | unknown | UNKNOWN (äkta coverage-lucka, §8 — fyll aldrig utan instrument-exakt källa). Ingen instrument-exakt SD-källa för Kriminalvårdens behandlingsprogram (återfallsförebyggande) hittades på data.riksdagen.se. Verifierat direkt: SD:s partimotion 'Kriminalvårdsfrågor' HC022892 (2024/25) har 0 träffar på 'be |
| M | fokuserad_avskrackning_gvi | unknown | H911333 + H911420 (Johan Forssell, M, skriftliga frågor 2021/22): nämner 'GVI (Sluta skjut)' men endast för att granska S-regeringens avhoppsstatistik i Malmö — statistikkritik mot minister, ingen ståndpunkt för/emot instrumentet; dessutom enskild ledamot och doktyp utanför stance-hierarkin. Förkast |
| SD | fokuserad_avskrackning_gvi | unknown | HC021434 'Sveriges Natopolitik' (enda literala 'fokuserad avskräckning'-träffen för SD): avser militär avskräckning/Nato — fel instrument och fel kategori (försvar, ej trygghet/brottsprevention). Förkastas på §1. GVI/Sluta skjut hos SD förekommer endast i interpellationer (utanför hierarkin §3). |
| C | fokuserad_avskrackning_gvi | unknown | HD022833 'Jord, skog, jakt' och GR1021 (interpellation 2003/04): de två enda 'Sluta skjut'-träffarna för C, båda falska positiva ('skjut' i jaktkontext / orelaterad interpellation). Förkastas på §1; den exakta frasen finns ej som instrument i C:s rättspolitik-/UO4-/budgetmotioner. |
| KD | fokuserad_avskrackning_gvi | unknown | Inget KD-dokument nämner instrumentet i någon doktyp (0 träffar på alla fyra sökord, parti=KD). Korpusens 'gruppvåldsintervention'-träffar är samtliga V-motioner. Ingen kandidatkälla att bedöma => äkta lucka per §8. |
| L | fokuserad_avskrackning_gvi | unknown | Inget L-dokument är instrument-exakt (0 träffar på 'Sluta skjut'/'fokuserad avskräckning'/'gruppvåldsintervention'/'GVI', parti=L). L:s 'avskräckning'-träffar avser cyberdoktrin/kärnvapen/försvar samt allmän straffrättslig avskräckning — fel instrument (§1). Äkta lucka per §8. |
| S | situationell_prevention_utomhusbelysning | keep | verifierare underkände (confirmed=false): Citatet återfinns ordagrant i fulltexten (HD021326), så quote_found=true. Riktningen är förenlig med 'supports' (åtgärder i den fysiska miljön för att minska risken för våld). MEN instrument_precise=f |
| M | situationell_prevention_utomhusbelysning | unknown | UNKNOWN (äkta lucka). Ingen instrument-exakt M-källa för situationell prevention via förbättrad utomhusbelysning på data.riksdagen.se. De enda instrument-exakta 'Trygghetsbelysning'-motionerna (HD02256/HC02310/HB0284/HA0263) är skrivna av Martin Westmont (SD), inte M. M:s belysningsmotioner ('Vägbel |
| C | situationell_prevention_utomhusbelysning | keep | verifierare underkände (confirmed=false): Citatet återfinns nära ordagrant i fulltexten för HB022738 (quote_found=true), under rubriken "Trygga boendemiljöer". Riktningen motsägs inte: texten är positiv till enkla insatser för ökad upplevd tr |
| S | psykosociala_insatser_frivard | unknown | HD023586 (UO4 2025/26), HC023264 (skr. Riksrevisionen 2024/25), HC023111 (UO4 2024/25): 'frivård' endast generisk ansvarsbeskrivning; faktiska instrument är anstaltsbaserade behandlingsprogram + återfallsförebyggande HoS, inte psykosociala insatser i frivården. 'psykosocial' = 0 träffar. Annat instr |
| M | psykosociala_insatser_frivard | unknown | H9023779 (frivård = verkställighetstid/närvaro/säkerhet), H9023765 (frivård = missbruks-/kontraktsvård; 'psykosocial' = regioners psykiatrivård), H5023681 ('psykosocial' = arbetsmiljö). Termerna förekommer aldrig som det namngivna instrumentet => unknown. |
| SD | psykosociala_insatser_frivard | unknown | HD022412/HD022411/H8023795 (frivård = påföljd/ordning/säkerhet, ingen behandling/'psykosocial'), 43 'psykosociala'-dok i hälso-/psykiatrikontext utan koppling till frivården. Annat instrument => unknown. |
| C | psykosociala_insatser_frivard | unknown | H5023188 (frivårdsinsatser för unga gängkriminella), H3022648 (kartläggning av befintliga behandlingsprogram), H5023685/H4023287 (radikalisering), ip HD10288 ('effektiv rehabilitering' generellt, ip lägre i hierarki). 'psykosocial' saknas helt i C-motioner. Samma mål/område, ej instrumentet => unkno |
| V | psykosociala_insatser_frivard | drop | HD022788 (kommittémotion Rättsväsendet 2025/26): verifierat att 'psykosocial' = 0 träffar och proposed_quote ej verbatim-bekräftad; texten avser 'sociala insatser'/'behandlingsprogram'/frivårdsreform, ett bredare/annat instrument. Droppad till unknown (behandlas lika med övrigas generella behandling |
| KD | psykosociala_insatser_frivard | unknown | H9024194 (2021/22): frivård brett (frivårdsinsatser, visitationsrätt, säkerhetsutrustning, frivårdsreform kring påföljdsval, allmänna åtgärdsprogram), namnger aldrig 'psykosociala insatser'. GP02So622 (2001/02): frivård endast drogstatistikkälla. Allmän rehabilitering, ej instrumentet => unknown. |
| L | psykosociala_insatser_frivard | unknown | H9023974/H8023272/H7023076/H7022016/H5023188/H3022648 (frivård = säkerhet/kostnadsanalys/unga gängkriminella, inget 'psykosocial'); H9023975/H8023271 ('psykosocial' = Sis-vården; frivård = generella 'frivårdsinsatser för unga lagöverträdare'). Brett instrument, ej psykosociala insatser i frivården = |
| MP | psykosociala_insatser_frivard | unknown | HD023544 ('psykosocial' utan 'frivård'); HB022669 (frivårdskontor/behandlingsprogram generellt + anhörigstöd); HD023841 (villkorlig frigivning). Inget dokument namnger psykosociala insatser i frivården => unknown. |
| MP | aktiveringskrav_ekonomiskt_bistand | keep | verifierare underkände (confirmed=false): Källan HD19SoU29p1 är ett VOTERINGSPROTOKOLL (omröstning/RIM-vot) för betänkande 2025/26:SoU29 'Aktivitetskrav för mottagare av försörjningsstöd', förslagspunkt 1. Fulltexten innehåller ENDAST rösttab |
| S | riktade_insatser_nyanlanda_elever | unknown | Ingen instrument-exakt partikollektiv källa. Närmast: H502744 'Folkhögskolespår' (2017/18, 5 S-ledamöter) — folkhögskola som alternativ anordnare av språkintroduktion på gymnasienivå. Samma målgrupp (nyanlända) men annat policyinstrument (anordnar-/organisationsfråga) och utanför föredragen mandatpe |
| MP | riktade_insatser_nyanlanda_elever | unknown | Ingen instrument-exakt källa. HD023364 (2025/26) och HC023217 (2024/25) nämner nyanlända endast i generell 'tidigt stöd'-mening eller i 'alla elevers rätt' till studiehandledning på modersmål (generell modersmålspolitik). Budgetmotioner (HD023770, HC023220, HB022691, HB022680) saknar skolinstrument  |
| SD | sfi_kombinerat_med_praktik | unknown | Ingen instrument-exakt källa. Närmaste kandidat HB02368 (SD-kommittémotion 2023/24, "En gymnasieskola och vuxenutbildning i världsklass") gäller bortre tidsgräns på två år för sfi + skärpta krav/anställningsbarhet, ej SFI kombinerat med yrkespraktik. Övriga granskade (HC021765, H8023403, H5023890, H |
| V | sfi_kombinerat_med_praktik | unknown | Ingen instrument-exakt källa. Granskade V-dokument 2022/23–2025/26 (HD022798, HC021930, HC021932 §8, HC02468, HD022791, budget-/arbetsmarknadsmotioner) rör endast andra instrument: rätt till sfi för asylsökande, lärarförsörjning, statligt huvudmannaskap, samt "Svenska från dag ett" (språk+samhällsvä |
| MP | sfi_kombinerat_med_praktik | keep | verifierare underkände (confirmed=false): Dokumentet är bekräftat: Motion 2023/24:2691 av Märta Stenevi m.fl. (MP), rätt parti. Citatet återfinns ordagrant i fulltexten (quote_found=true), och riktningen är tydligt stödjande: texten kallar ko |
| S | sprakpraktik_kombinerad_sprakutbildning_och_arbetspraktik | unknown | Ingen instrument-exakt kalla. HD023590 (kommittemotion UO14 2025/26) anvander arbetsmarknadsutbildning + arbetspraktik (ej sprakutbildning) => annat instrument. H302814 (enskild motion 2015/16, Kalmarmodellen) kombinerar sprak+praktik men ar for svag (enskild, utanfor fonstret, regional sjukvardsmod |
| M | sprakpraktik_kombinerad_sprakutbildning_och_arbetspraktik | unknown | Ingen instrument-exakt kalla. 'sprakpraktik' parti=M doktyp=mot=0; 'arbetspraktik'-traffar pre-2010/off-instrument. Aktuella integrationsmotioner (H9024033, H9023987, H9024176) namner endast allman praktik i arbetsmarknadspolitik/nystartsjobb och sfi+akademisk specialisering - andra instrument, ej s |
| SD | sprakpraktik_kombinerad_sprakutbildning_och_arbetspraktik | unknown | Ingen instrument-exakt kalla. 'sprakpraktik' parti=SD = 0 traffar (mot + alla doktyper); 'arbetspraktik' = 1 ej relevant (skatteutgifter); centrala integrations-/etableringsmotioner (H9023704, H9023895, H8023403, HD02162, HC02158) saknar samtliga komponenttermer. Endast 'i praktiken' o.dyl., ej som  |
| L | sprakpraktik_kombinerad_sprakutbildning_och_arbetspraktik | drop | H9023965 (partimotion 2021/22) droppas: icke-instrument-exakt (sprakpraktik/arbetspraktik/sprakutbildning saknas i .text) och enda 'praktik'-traffen ar kritisk ('sfi, praktikplatser ... varvas i araten' => vill begransa, fel riktning). Aldre kandidat H4021068 (2016/17) ar maliniva, namner inte det d |
| MP | ateraktiverad_utokad_varnplikt | unknown | UNKNOWN (äkta coverage-lucka, §1 + §8). Ingen instrument-exakt MP-källa för 'återaktiverad/utökad militär värnplikt' i någon hämtad försvarsmotion. Den enda meningen som nämner att 'fler kallas också till värnplikt' (HC023038, rm 2024/25) är — verifierat mot råtexten — en BESKRIVANDE bakgrundsmening |
| C | tydlig_statlig_styrning_civilt_forsvar | keep | verifierare underkände (confirmed=false): Citatet återfinns ordagrant i HD022822 (Centerpartiets motion). MEN instrumentet är "tydlig STATLIG styrning av CIVILT FÖRSVAR". Citatet efterfrågar i själva verket tydligare styrning av "samhällets K |
| KD | tydlig_statlig_styrning_civilt_forsvar | drop | Källa H9023908 (kommittémotion 2021/22:3908) förkastad for instrumentet tydlig_statlig_styrning_civilt_forsvar. Citatet 'Den återupptagna planeringen för det civila försvaret går för långsamt och behöver intensifieras och påskyndas' är endast det allmänna målet (§1, instrument-regeln avvisar samma m |
| MP | tydlig_statlig_styrning_civilt_forsvar | unknown | Ingen MP-källa instrument-exakt. Närmaste, HD023405 (2025/26, kommittémotion, Emma Berginger m.fl.), har endast det allmänna målet 'att stärka det civila försvaret och krisberedskapen' (§1 avvisar) plus andra delinstrument (FOI-forskning, nordiskt samarbete, civilplikt, civilsamhälle). Direkt textsö |
| M | atgarder_mot_otillaten_paverkan_offentlig_sektor | unknown | DROP av befintlig rad HB02767 (tidigare supports). Enskild motion (Caroline Högström, M, "Skydd av anställda inom vård och socialtjänst", 2023/24). Frasen "otillåten påverkan" förekommer ENDAST i motiveringen som problembeskrivning ("...där otillåten påverkan och hot riskerar hota rättssäkerheten i  |
| SD | atgarder_mot_otillaten_paverkan_offentlig_sektor | add | verifierare underkände (confirmed=false): Citatet hittades ordagrant i fulltexten (HD02247, motion 2025/26:247 av Johnny Svedin, SD) som Yrkande 1 under Förslag till riksdagsbeslut. Stance-riktningen 'supports' stämmer i sak: motionen vill ak |
| V | atgarder_mot_otillaten_paverkan_offentlig_sektor | add | verifierare underkände (confirmed=false): Dokumentet HC19JuU29p1 är ett voteringsprotokoll för betänkande 2024/25:JuU29 "Ett starkare skydd för offentliganställda mot våld, hot och trakasserier m.m.". Citatets voteringssiffror återfinns ORDAG |
| KD | atgarder_mot_otillaten_paverkan_offentlig_sektor | unknown | UNKNOWN — äkta coverage-lucka. Ingen instrument-exakt KD-källa på data.riksdagen.se. Exakt frasen "otillåten påverkan" i KD-motioner: endast 2 äldre träffar (H4023236 2016/17; H002Ju355 2012/13), 0 i innevarande mandatperiod. I H4023236 är frasen ren bakgrundsbeskrivning om grov organiserad brottsli |
| M | systematiskt_antikorruptionsarbete_kommuner_regioner | unknown | unknown / codeable=false. Bästa domännära M-källan, HD021760 'Avpolitisering av den kommunala revisionen' (Boriana Åberg, 1 undertecknare — verifierat i .text), föreslår ett ANNAT instrument: reform/avpolitisering av den kommunala revisionen. Korruption nämns endast som mål ('En väl fungerande kommu |
| V | systematiskt_antikorruptionsarbete_kommuner_regioner | unknown | unknown / codeable=false. V:s demokrati-/konstitutionsmotioner (HB02440, HC021934, HD022790, avsnitt 'Transparens och antikorruption') rör uteslutande NATIONELL nivå: partifinansiering/insynslagen, lobbyregister, statsråds aktieaffärer/karens, Greco-rekommendationer om statliga tjänstemän. 'Kommuner |
| KD | systematiskt_antikorruptionsarbete_kommuner_regioner | unknown | unknown / codeable=false. Efter uttömmande sökning saknas instrument-exakt KD-källa: 'antikorruption'/'korruption'-träffar gäller internationellt bistånd/utrikespolitik, eller nationell straffrätt (HC021172 'Införandet av tjänstemannaansvaret' — annat instrument). Inga visselblåsar-/antikorruptionsp |
| MP | systematiskt_antikorruptionsarbete_kommuner_regioner | unknown | unknown / codeable=false. MP:s antikorruptionsförslag (kommittémotion HB022669, HA02181) rör nationell nivå: transparens-/lobbyregister, skärpta regler för anonyma/utländska partibidrag, meddelarskydd. Den enda kommun-nära källan, enskild motion H5021712 'Revision i kommunsektorn' (Jan Lindholm, 1 u |
