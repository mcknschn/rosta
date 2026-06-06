# Rösta — Evidens & trovärdighet (B-spåret): arbetslogg & metodutveckling

> **Levande arbetsdokument.** Spårar arbetet med att höja **B** (delpoäng evidens/träffsäkerhet,
> 0,35 av varje kategoripoäng) — både *täckning* (fler undermått med partikopplad evidens) och
> *trovärdighet* (källkvalitet, neutralitet, verifierbarhet).
> Skapad 2026-06-06 efter att natten gav **1 byggt mått** trots research i fem kategorier.
> Bärande omtag (2026-06-06): **måttet och positioneringen är två skilda steg** (§2). Mycket av
> det vi kallade "väggen" var i själva verket ett källval i steg 2, inte ett fel i måttet.
>
> Relaterat: metoden i [fas4b_partistandpunkter_metod.md](fas4b_partistandpunkter_metod.md)
> (källhierarki, instrument-regeln, verifiering), planen i [BACKLOG.md](BACKLOG.md) (Spår B),
> grundprincipen i [../IDEA.md](../IDEA.md), datamodellen i [../DATA.md](../DATA.md).

---

## 0. Varför denna fil finns

Natten 2026-06-06 var uppdraget "nå 4 undermått i välfärd, försvar, integration, trygghet och
klimat". Resultatet blev **1 mått** (försvar/nato_medlemskap) — inte av brist på letande (varje
röstsiffra verifierades mot data.riksdagen.se) utan för att metoden vi körde, **ren votering + krav
på differentiering**, blandade ihop två frågor som borde hållas isär (§2). Filen finns för att:

1. hålla **tvåstegsmodellen** (§2) levande så vi inte återfaller i votering-fixeringen,
2. skilja **äkta hinder** (steg-1: måttet saknas) från **källval** (steg-2: var positioneringen bor) (§4),
3. samla ett **metodregister för positionering** (§5) — fler officiella källor, samma stränghet,
4. hålla **statustavla** (§6), **kandidat-pipeline** (§7) och **beslutslogg** (§9) uppdaterade,
   så att versionsstyrd config alltid kan spåras till ett resonemang.

Bärande princip oförändrad (CLAUDE.md): inget partibetyg eller mänskligt omdöme i kod — bara i
versionsstyrd config; all data spårbar till en officiell svensk källa; värdeneutralitet är kärnan.

---

## 1. Mål & spelregler

**Mål:** varje kategori ska ha **≥4 undermått med aktiv partikopplad B-evidens** *där det är möjligt*
(vissa undermått saknar indikator, vissa indikatorer är `target` utan riktning — se §4). Fler täckta
undermått → mindre coverage-krympning mot neutral 2,5 → B får faktiskt genomslag och vilar inte på en
enda rad.

**Spelregler (beslutade med användaren, gäller tills annat sägs):**

| Regel | Innebörd |
|---|---|
| **Neutralitet före 4** | Bygg hellre färre mått än ett som tiltar vänster/höger eller regering-vs-opposition. Ett tiltat mått skadar trovärdigheten mer än ett saknat mått. Gäller hur vi *positionerar* — inte ett krav på att ett mått ska särskilja (§2). |
| **Svensk-först** | Riktningsbelägget (evidensliggaren) ska vara officiell svensk källa; akademisk svensk när officiell statistik saknas. Mellanstatliga Sverige-utvärderingar (EU:s rättsstatsrapport, GRECO, OECD) **endast som bekräftelse** — aldrig primär, aldrig index (DATA.md, beslut 2026-06-05). Internationella **index** (RSF/CPI/Freedom House/V-Dem) är förbjudna. |
| **Bygg rena, håll tveksamma** | Endast mått som passerar alla grindar (§10) byggs nu. Tveksamma kandidater hålls i §7 för diskussion, byggs inte autonomt. |
| **Versionen bumpar bara användaren** | Config byggs i `version 0`/förslag; människan signerar och bumpar. |

---

## 2. Tvåstegsmodellen: måttet vs positioneringen ⭐

Den bärande insikten (2026-06-06): **ett mått, och hur vi positionerar partier på det, är två skilda
steg.** Vi behandlade dem länge som ett — "finns en ren votering?" fick avgöra både om måttet dög
*och* hur partierna placerades. Det var fel.

- **Steg 1 — Måttet.** Ett undermått + en indikator (med riktning) + ett policyinstrument + **officiell
  svensk evidens att instrumentet flyttar indikatorn** åt det håll partiet påstår. Det här avgör om
  måttet *finns* och är trovärdigt. Oberoende av vilka partier som råkar stödja det.
- **Steg 2 — Positioneringen.** *Var* visar sig varje partis hållning på instrumentet? Votering,
  betänkande, reservation, kommittémotion, budgetmotion, valmanifest — en hel stege (§5.1).
  Acklamation slår bara ut *votering*-källan; den säger ingenting om de andra.

**Följder:**

1. **Ett bra mått kan inte underkännas för att voteringen är acklamation.** Det är ett steg-2-problem
   (källval), inte ett steg-1-problem (måttkvalitet). Måttet kan vara utmärkt — vi hämtar
   positioneringen någon annanstans.
2. **Differentiering är ett *utfall*, inte ett inträdeskrav.** Skiljer sig partierna faktiskt syns det
   i positioneringssteget; gör de inte det är måttet ändå korrekt (bidrar till täckning/trovärdighet,
   bara inte till rankning). Differentiering spelar roll för *rankningsnytta*, aldrig för *korrekthet* —
   och är aldrig värt en tilt.
3. **"Icke-differentierande" var en felbenämning.** Det jag tidigare kallade så var att *voteringen*
   inte särskiljer — vilket inte säger något om budget/motioner. Rätt term: **voterings-konsensus**,
   som inte utesluter budget-/motionsdifferentiering.

**Men steg 2 måste fortfarande gå att mäta vettigt** (gränserna i §5.6). Två fallgropar att hålla emot:

- **Mål vs instrument.** Manifest uttrycker oftast *mål* ("korta vårdköerna"), inte instrument.
  Positionerar vi löst på målspråk blir alla = `supports` på allt → B mättar mot 5 för alla → *mindre*
  sant än voteringar. Instrument-grinden (§10) måste följa med till *alla* källor.
- **Gradskillnad ryms inte i dagens modell.** `party_positions` kodar binärt `supports`/`opposes` —
  ingen magnitud. Att "alla stödjer men S satsar mer än M" går att *se* i budgetar men **inte att
  koda** utan modellutvidgning. Tills dess fångar steg 2 *riktning* (finansierar/avvecklar
  instrumentet), inte *grad*.

---

## 3. Var vi står (uppdateras per leverans)

Aktiv partikopplad B-evidens per kategori (källa: `python -m pipeline.tools.coverage_report`,
B4-grind `b_submeasure_spread`). **Senast uppdaterad 2026-06-06.**

| Kategori | Undermått m. B-evidens | B-möjliga undermått¹ | Status |
|---|---|---|---|
| ekonomi | **4/6** | 4 | ✅ alla B-möjliga täckta (inflation/off.finanser = target) |
| trygghet | **4/5** | ~4 | ✅ snabbförfarande byggt 2026-06-06 (enhällighet) → **4 nått** |
| klimat | **4/5** | ~4 | ✅ invasiva arter byggt 2026-06-06 (enhällighet; low/low, FLAGGAD) → **4 nått** |
| demokrati | **4/5** | 4–5² | ✅ public service-lagen byggt 2026-06-06 (enhällighet, KrU2 p1, alla 8 supports) → **4 nått** |
| forsvar | **3/5** | 3³ | nato byggt; leverans HOLD **bekräftat djupsvep §5.8** (7 instrument; äkta steg-1-vägg — leveranstid ej svenskt belagt), ambition = target |
| integration | 2/5 | 3–4⁴ | HOLD ×2 **bekräftat djupsvep §5.8** (11 instrument; boendesegr. steg-1-vägg, normer_tillit/KU4 fel konstrukt) |
| valfard | 2/4 | 3⁵ | HOLD ×2 **bekräftat djupsvep §5.8** (11 instrument; vårdplats-slutrapport 2026:3 föll nedåt, cancerscreening = steg-2-tilt) |

¹ Undermått vars indikator har en riktning (≠ `target`) **och** kan kopplas till en åtgärdstyp med
  evidensbelagd riktning. ² demokrati har undermått där neutralt mått ännu inte hittats utan dubbelräkning.
  ³ försvar: `ekonomisk_ambition` = `forsvarsanslag_andel_bnp` är `target`. ⁴ integration:
  `migrationssystem` saknar indikator. ⁵ välfärd: `vard_tillganglighet` + `omsorg_personal` otäckta.

**Sammanlagt:** 37 evidensposter / 200 ståndpunkter (2026-06-06: +3 poster, +24 ståndpunkter via de tre
enhällighet-måtten snabbförfarande + invasiva arter + public service). `dist/`-snapshot medvetet ej
re-baselinad så kumulativ effekt syns (`score_diff` visar demokrati+nato+dagens leverans tillsammans).
Public service-måttets **isolerade** effekt: icke-rankningsdrivande (ranking oförändrad), demokrati +0,0…+0,20
per parti (alla supports), total +0,0…+0,015.

---

## 4. Vad som verkligen blockerar — steg-1-väggar vs steg-2-källval

Med tvåstegsmodellen faller det mesta av "väggen" jag beskrev natten. Den var till stor del ett
**steg-2-artefakt**: vi använde nästan bara voteringar för positionering, och acklamation slår ut just
den källan. Sorterat på vad som *verkligen* hindrar:

### 4.1 Inte äkta väggar — bara steg-2-källval (lösbara genom att byta källa)
- **Acklamation på sakpunkten** (snabbförfarande, invasiva arter, materielpunkter, hedersvåld, EMFA) →
  voteringen är noll, men ett enhälligt betänkande eller en kommittémotion belägger ändå hållningen
  (§5.2–5.3).
- **Buntad omnibus** (FöU3 buntad med Israel-export; KU12 buntad med SD:s grundlagsreservation) →
  voteringens innebörd är tvetydig, men en instrument-specifik kommittémotion är entydig.
- **Avslags-tilt** → den enda voteringen är tiltad, men andra källor kan ge neutral positionering —
  eller så speglar tilten genuin *nuvarande* differentiering, vilket är ok om värdeneutralt belagt.

### 4.2 Äkta väggar — steg-1, måttet självt saknas
Ingen källa i världen hjälper; måttet existerar inte förrän en indikator med svensk auktoritetsbelagd
riktning läggs till (§5.7).

| Kategori | Undermått | Steg-1-hinder |
|---|---|---|
| trygghet | `forebyggande` | saknar indikator |
| klimat | `industriell_konkurrenskraft` | saknar indikator |
| integration | `migrationssystem` | saknar indikator |
| försvar | `ekonomisk_ambition` | indikator = `forsvarsanslag_andel_bnp` (`target`, ingen upp/ned) |
| ekonomi | inflation, offentliga finanser | `target` (nära mål ≠ "uppåt bra") |

→ Kräver **modellutvidgning**; tas upp som designfrågor, byggs inte autonomt.

---

## 4.3 Begreppsmodell + mätbarhetskarta per indikator (samtliga mått) ⭐

> Tillagd 2026-06-06 på användarens begäran: (a) en **stringent begreppsmodell** — samma namn i alla
> dokument, och (b) en **mätbarhetskarta** — kan varje indikator faktiskt mätas? Detta avsnitt är den
> **auktoritativa ordlistan** för hela projektet; IDEA.md, DATA.md, BACKLOG.md och ROADMAP.md använder
> samma termer (terminologin normaliserades 2026-06-06: "submått" → **Undermått**).

### Begreppsmodell (ordlista) — fyra nivåer, ETT namn var

| Nivå | Kanoniskt namn | Kod-nyckel (sanningskälla) | Exempel |
|---|---|---|---|
| 1 | **Kategori** | `categories[].id` | Försvar och beredskap (`forsvar`) |
| 2 | **Undermått** | `submeasures[].id` | Militär förmåga (`militar_formaga`) |
| 3 | **Indikator** | `indicators[].id` | Försvarsanslag som andel av BNP (`forsvarsanslag_andel_bnp`) |
| 3b | **Riktning** | `indicators[].direction` | upp · ned · målnivå (`target`) |

**Regel mot begreppsförvirring:** `config/categories.yaml` är sanningskälla; **id:t** (t.ex. `nato_ukraina`) är
det som aldrig får glida mellan dokument. De svenska visningsnamnen ovan är kanoniska — använd dem i all prosa.
*Retirerade synonymer:* "submått" → **Undermått** (kod-nyckeln heter fortfarande `submeasures`/`submeasure`,
engelska — det är samma begrepp); "mätpunkt"/"mått" → **Indikator**. Varje indikator har EN riktning:
`up` → upp, `down` → ned, `target` → målnivå. (Visningsnamnen för Kategori/Undermått hämtas ur `categories.yaml`
`name`-fältet — fyra trunkerade namn rättades 2026-06-06: Nato/Skola/Normer/Finansiering hade kapats av
oquoterade kommatecken.)

### Mätbarhet — kan varje indikator mätas?
En indikator bidrar till betyget om den har **B** (partikopplad evidens att ett instrument flyttar den) **eller**
**D** (officiell svensk årsserie). B och D är två vägar — en stängd D dödar inte indikatorn om B bär den (t.ex.
mediefrihet/korruption: D förbjuden/sekretess men B byggd).
**Mätstatus:** ✅ **mäts** (B och/eller D, bidrar nu) · 🟡 **mätbar, ej byggd** (väg finns, jobb kvarstår) ·
🔴 **ej mätbar** (indikator finns men B-vägg + ingen D) · 🔴 **saknar indikator** (inget definierat att mäta —
kräver ny indikator, §5.7) · ⚪ **target** (kontext, ingen riktning, betygssätts ej, renormaliseras bort).

### Mastertabell — samtliga 35 undermått / 52 indikatorer (genererad ur config 2026-06-06)
*De 3 undermått som **saknar indikator** (Förebyggande arbete, Industriell konkurrenskraft, Migrationssystemets
hållbarhet) listas som egna rader — de är steg-1-väggar (§4.2): det finns inget definierat att mäta.*
| Kategori | Undermått | Indikator | Riktning | Mätstatus |
|---|---|---|---|---|
| Ekonomi och jobb | Sysselsättning och arbetslöshet `sysselsattning_arbetsloshet` | Sysselsättning `sysselsattning` | upp | ✅ mäts (B+D) |
| Ekonomi och jobb | Sysselsättning och arbetslöshet `sysselsattning_arbetsloshet` | Arbetslöshet `arbetsloshet` | ned | ✅ mäts (D) |
| Ekonomi och jobb | BNP per capita och produktivitet `bnp_produktivitet` | BNP per capita `bnp_per_capita` | upp | ✅ mäts (D) |
| Ekonomi och jobb | BNP per capita och produktivitet `bnp_produktivitet` | Produktivitet `produktivitet` | upp | ✅ mäts (B+D) |
| Ekonomi och jobb | Reallöner och hushållens ekonomi `realloner_hushall` | Reallöner `realloner` | upp | 🟡 mätbar, ej byggd |
| Ekonomi och jobb | Reallöner och hushållens ekonomi `realloner_hushall` | Hushållens reala disponibla inkomst `hushallens_reala_disponibla_inkomst` | upp | ✅ mäts (B) |
| Ekonomi och jobb | Företagande och investeringar `foretagande_investeringar` | Näringslivets investeringar `naringslivets_investeringar` | upp | ✅ mäts (B) |
| Ekonomi och jobb | Inflation och prisstabilitet `inflation_prisstabilitet` | Inflation (nära mål) `inflation` | målnivå | ⚪ target (kontext) |
| Ekonomi och jobb | Offentliga finanser och långsiktig hållbarhet `offentliga_finanser` | Statsskuld/underskott (hållbar nivå) `statsskuld_underskott` | målnivå | ⚪ target (kontext) |
| Välfärd | Vårdens tillgänglighet och kvalitet `vard_tillganglighet` | Vårdköer `vardkoer` | ned | ✅ mäts (D) |
| Välfärd | Vårdens tillgänglighet och kvalitet `vard_tillganglighet` | Andel som får vård i tid `vard_i_tid` | upp | 🟡 mätbar, ej byggd |
| Välfärd | Vårdens tillgänglighet och kvalitet `vard_tillganglighet` | Överlevnad efter svår sjukdom `overlevnad_svar_sjukdom` | upp | 🟡 mätbar, ej byggd |
| Välfärd | Skolans kunskap och likvärdighet `skola_kunskap` | Skolresultat `skolresultat` | upp | ✅ mäts (B+D) |
| Välfärd | Skolans kunskap och likvärdighet `skola_kunskap` | Skillnader mellan skolor `skillnader_mellan_skolor` | ned | 🟡 mätbar, ej byggd |
| Välfärd | Skolans kunskap och likvärdighet `skola_kunskap` | Behöriga lärare `behoriga_larare` | upp | ✅ mäts (D) |
| Välfärd | Omsorg och personalförsörjning `omsorg_personal` | Personalomsättning i omsorgen `personalomsattning_omsorg` | ned | 🔴 ej mätbar (vägg) |
| Välfärd | Finansiering, styrning och anti-fusk `finansiering_styrning` | Välfärdsbrottslighet `valfardsbrottslighet` | ned | ✅ mäts (B) |
| Lag och trygghet | Grov brottslighet och våldsbrott `grov_brottslighet` | Dödligt våld `dodligt_vald` | ned | ✅ mäts (D) |
| Lag och trygghet | Grov brottslighet och våldsbrott `grov_brottslighet` | Skjutningar och sprängningar `skjutningar_sprangningar` | ned | ✅ mäts (B+D) |
| Lag och trygghet | Utsatthet och upplevd trygghet `utsatthet_trygghet` | Brottsutsatthet `brottsutsatthet` | ned | ✅ mäts (B+D) |
| Lag och trygghet | Utsatthet och upplevd trygghet `utsatthet_trygghet` | Upplevd otrygghet `upplevd_otrygghet` | ned | ✅ mäts (D) |
| Lag och trygghet | Rättsväsendets effektivitet `rattsvasendets_effektivitet` | Uppklaringsgrad `uppklaringsgrad` | upp | ✅ mäts (D) |
| Lag och trygghet | Rättsväsendets effektivitet `rattsvasendets_effektivitet` | Handläggningstid `handlaggningstid` | ned | ✅ mäts (B) |
| Lag och trygghet | Förebyggande arbete `forebyggande` | _(ingen indikator definierad)_ | — | 🔴 saknar indikator |
| Lag och trygghet | Återfall och kriminalvård `aterfall_kriminalvard` | Återfall i brott `aterfall_i_brott` | ned | ✅ mäts (B) |
| Försvar och beredskap | Militär förmåga `militar_formaga` | Personal och värnpliktiga `personal_varnpliktiga` | upp | ✅ mäts (B) |
| Försvar och beredskap | Militär förmåga `militar_formaga` | Ammunition, luftvärn, logistik, cyberförmåga `materiel_formaga` | upp | 🟡 mätbar, ej byggd |
| Försvar och beredskap | Ekonomisk ambitionsnivå och långsiktig finansiering `ekonomisk_ambition` | Försvarsanslag som andel av BNP `forsvarsanslag_andel_bnp` | målnivå | ⚪ target (kontext) |
| Försvar och beredskap | Civil beredskap `civil_beredskap` | Civil beredskap (vård, energi, mat, transporter) `civil_beredskap_niva` | upp | ✅ mäts (B) |
| Försvar och beredskap | Nato, Ukraina och internationell trovärdighet `nato_ukraina` | Ukraina-stöd `ukraina_stod` | upp | 🟡 mätbar, ej byggd |
| Försvar och beredskap | Nato, Ukraina och internationell trovärdighet `nato_ukraina` | Nato-interoperabilitet `nato_interoperabilitet` | upp | ✅ mäts (B) |
| Försvar och beredskap | Genomförbarhet och leveranstakt `genomforbarhet_leverans` | Leveranstid för materiel `leveranstid_materiel` | ned | 🔴 ej mätbar (vägg) |
| Klimat, miljö och energi | Utsläppsminskningar `utslappsminskningar` | Territoriella utsläpp `territoriella_utslapp` | ned | ✅ mäts (B+D) |
| Klimat, miljö och energi | Utsläppsminskningar `utslappsminskningar` | Konsumtionsbaserade utsläpp `konsumtionsbaserade_utslapp` | ned | ✅ mäts (D) |
| Klimat, miljö och energi | Energiförsörjning och elpriser `energi_elpriser` | Fossil energianvändning `fossil_energianvandning` | ned | ✅ mäts (D) |
| Klimat, miljö och energi | Energiförsörjning och elpriser `energi_elpriser` | Elprisvolatilitet `elprisvolatilitet` | ned | 🟡 mätbar, ej byggd |
| Klimat, miljö och energi | Energiförsörjning och elpriser `energi_elpriser` | Effektbrist `effektbrist` | ned | ✅ mäts (B) |
| Klimat, miljö och energi | Omställningens kostnadseffektivitet `kostnadseffektivitet` | Utsläppsminskning per krona `utslappsminskning_per_krona` | upp | ✅ mäts (B) |
| Klimat, miljö och energi | Biologisk mångfald och natur `biologisk_mangfald` | Hotade arter / naturförlust `hotade_arter_naturforlust` | ned | ✅ mäts (B) |
| Klimat, miljö och energi | Industriell konkurrenskraft i omställningen `industriell_konkurrenskraft` | _(ingen indikator definierad)_ | — | 🔴 saknar indikator |
| Integration och social sammanhållning | Arbete och självförsörjning `arbete_sjalvforsorjning` | Sysselsättningsgap inrikes/utrikes födda `sysselsattningsgap_inrikes_utrikes` | ned | ✅ mäts (B+D) |
| Integration och social sammanhållning | Arbete och självförsörjning `arbete_sjalvforsorjning` | Självförsörjningsgrad `sjalvforsorjningsgrad` | upp | ✅ mäts (D) |
| Integration och social sammanhållning | Arbete och självförsörjning `arbete_sjalvforsorjning` | Bidragsberoende `bidragsberoende` | ned | ✅ mäts (B+D) |
| Integration och social sammanhållning | Skola, språk och utbildning `skola_sprak` | SFI-resultat/språkkunskaper `sfi_sprakkunskaper` | upp | 🟡 mätbar, ej byggd |
| Integration och social sammanhållning | Skola, språk och utbildning `skola_sprak` | Skolresultat i utsatta områden `skolresultat_utsatta_omraden` | upp | ✅ mäts (B) |
| Integration och social sammanhållning | Boendesegregation och trygghet `boendesegregation` | Trångboddhet `trangboddhet` | ned | ✅ mäts (D) |
| Integration och social sammanhållning | Boendesegregation och trygghet `boendesegregation` | Segregation `segregation` | ned | 🔴 ej mätbar (vägg) |
| Integration och social sammanhållning | Normer, tillit och samhällsgemenskap `normer_tillit` | Tillit och valdeltagande `tillit_valdeltagande` | upp | 🔴 ej mätbar (vägg) |
| Integration och social sammanhållning | Migrationssystemets hållbarhet `migrationssystem` | _(ingen indikator definierad)_ | — | 🔴 saknar indikator |
| Frihet, demokrati och institutioner | Rättsstat och maktdelning `rattsstat_maktdelning` | Otillbörlig politisering av myndigheter `otillborlig_politisering` | ned | ✅ mäts (B) |
| Frihet, demokrati och institutioner | Korruption och myndighetstillit `korruption_tillit` | Korruption `korruption` | ned | ✅ mäts (B) |
| Frihet, demokrati och institutioner | Korruption och myndighetstillit `korruption_tillit` | Förtroende för domstolar/myndigheter `fortroende_domstolar_myndigheter` | upp | 🟡 mätbar, ej byggd |
| Frihet, demokrati och institutioner | Yttrandefrihet och medier `yttrandefrihet_medier` | Mediefrihet `mediefrihet` | upp | ✅ mäts (B) |
| Frihet, demokrati och institutioner | Personlig frihet och integritet `personlig_frihet` | Övervakning utan rättssäkerhet `overvakning_utan_rattssakerhet` | ned | ✅ mäts (B) |
| Frihet, demokrati och institutioner | Transparens och ansvarsutkrävande `transparens_ansvar` | Politisk transparens `politisk_transparens` | upp | 🟡 mätbar, ej byggd |

### Vad kartan säger — fyra slags otäckthet
1. **✅ Mäts (bidrar nu)** — majoriteten. Värdeneutralt skydd: indikatorer utan D mäts ofta ändå via **B**
   (nato_interoperabilitet, mediefrihet, korruption — D sekretess/förbjuden men B bär dem).
2. **🟡 Mätbar, ej byggd (10 st)** — jobb kvarstår, inte väggar: D-serien finns men adaptern är obyggd
   (realloner, sfi, elprisvolatilitet…) **eller** en B-väg finns men är ogjord (materiel, Ukraina-stöd,
   politisk_transparens via KU39, domstolsförtroende, overlevnad via cancerstrategi). **Dessa byggs, ej stryks.**
3. **🔴 Ej mätbar (7 undermått totalt):**
   - **Indikator finns men är en äkta vägg (4):** `personalomsattning_omsorg`, `leveranstid_materiel`,
     `segregation`, `tillit_valdeltagande` — varken byggbar B eller åtkomlig D. **Exakt dessa blockerar fyra av
     HOLD-undermåtten.** Kandidater för **borttagning/omklassning** (§8.6).
   - **Saknar indikator helt (3):** `forebyggande` (trygghet), `industriell_konkurrenskraft` (klimat),
     `migrationssystem` (integration) — inget är ens definierat att mäta. Kräver en **ny indikator** (§5.7,
     modellutvidgning) eller borttagning. Båda är sign-off.
4. **⚪ Target (3 st):** inflation, statsskuld, försvarsanslag — saknar riktning (nära mål = bäst), betygssätts
   aldrig, renormaliseras bort. Behålls medvetet för *visning/kontext*.

**Slutsats för "kan vi inte mäta — ska vi ha kvar?":** principen håller för de **7 röda** (4 ej mätbara + 3 utan
indikator = precis de undermått vi inte når) → ta bort, omklassa till kontext, eller (för de 3) lägg ny indikator.
De **10 gula** är mätbara och bör byggas, inte strykas. Beslutsdiskussion: §8.6.

## 5. Steg 2 — metodregister för positionering

Alla källor lyder under samma grindar (§10): instrument-exakthet, ordagrant citat + dok-id,
neutralitet. `source_type`-enumet i [fas4b §7](fas4b_partistandpunkter_metod.md) tillåter redan hela
stegen — vi har bara underutnyttjat allt utom votering.

### 5.1 Källstegen och vad varje källa är bra på
| Källa (stark→svag provenans) | source_type | confidence-tak | Bäst för |
|---|---|---|---|
| Skarp votering på sakpunkten | `votering` | high | binär riktning, ingen tolkning — men **noll vid acklamation** |
| Enhälligt betänkande | `betankande` | medium–high | baslinje-täckning (alla supports) när voteringen är acklamation |
| Reservation som anger nivå | `reservation` | medium | *mer/mindre* inom konsensus (differentiering) |
| Kommittémotion (partiofficiell) | `kommittemotion` | medium | instrument-specifik hållning, finns även vid acklamation |
| Budgetmotion | `budgetmotion` | medium | *riktning* (finansierar/avvecklar); **grad** kräver modellutv. (§5.6) |
| Valmanifest | `valmanifest` | low–medium | endast om instrument-konkret (annars mål → ej kodbart) |
| Partiprogram | — | — | endast kontext, aldrig ensam stance |

Confidence speglar var på stegen raden sitter; coverage-krympning + flagga bär osäkerheten ärligt.
`enskild_motion` = svag provenans, flaggas särskilt.

### 5.2 Enhällighet som källa — baslinje-täckning
**Vad:** När en sakpunkt tas med acklamation *därför att utskottet var enhälligt* (ingen reservation
*mot* punkten) är det belägg för att alla 8 partier står bakom. Koda samtliga `supports`,
`source_type: betankande`, `quote` = meningen som visar enhällighet/utskottets förslag.

**Varför tillåtet:** [fas4b §5](fas4b_partistandpunkter_metod.md) säger redan att stance får sättas när
partiet är formell avsändare, röstat för, eller står bakom via utskott. Ett enhälligt betänkande är de
facto kollektiv stance — och den **renaste neutraliteten**: alla kodas lika, inget straffas.

**Caveat:** (1) Acklamation ≠ alltid enhällighet — hämta fulltexten och bekräfta att *just den punkten*
saknar reservation mot sakinnehållet. (2) Det ger **täckning, inte rankning** (likformigt lyft). (3)
Lägger man ett konsensus-undermått bredvid ett differentierande i samma kategori späds differentieringen
(undermåttsviktat medel) — gör ett undermått i taget, inte en flod.

### 5.3 Budget- och kommittémotion — där differentieringen oftast bor
**Vad:** En budget- eller kommittémotion visar ett partis hållning på det *specifika instrumentet* även
när voteringen är acklamation. Budgeten är instrument-konkret (anslag/UO) och avslöjar **riktning** —
finansierar partiet instrumentet eller vill det avveckla/skära det?

**Varför viktigt:** det är här konsensus-reformer faktiskt skiljer partier åt. Acklamation i kammaren
döljer att budgetmotionerna pekar olika håll. Detta är primärvägen att hämta tillbaka differentiering
*utan tilt och utan votering*.

**Caveat:** (1) **Dubbelräkning mot A** — a1 mäter redan budget*prioritering* (andel till kategori). B
får bara mäta *om det finansierade instrumentet är evidensbelagt åt rätt håll*, inte prioriteringen
igen; håll frågorna åtskilda i `mapping_note`. (2) **Grad ryms inte** — se §5.6.

### 5.4 Reservations-mining — differentiering *inom* konsensus
**Vad:** Även när huvudpunkten är konsensus filar partier reservationer som vill ha **mer/mindre** av
samma instrument. Mer av positiv-riktad åtgärd → `supports`; avveckla/minska → `opposes` (negativ-grind
§10). Bara "annan utformning" utan riktningsinnebörd → ingen rad.
**Caveat:** högst tilt-risk (reservationer är ofta opposition-mot-regering) → codex/2nd-opinion per mått.

### 5.5 Positionsmönster över mandatperioden (bana, inte ögonblicksbild)
**Vad:** Etablera hållning ur **mönstret av flera källor/voteringar över mandatperioden**, inte en
enskild punkt. Konsekvent riktning är starkare belägg och kan avslöja en hållning en enskild
acklamation döljer (jfr nato: ögonblicket 2026 säger "alla för", banan skiljer V från MP).
**Caveat:** bara samma instrument (instrument-regeln). **Varaktiga, genuina omsvängningar kodas efter
nuläget** (nato/MP → `none`) — banan är en prediktor tyngd mot det senaste, inte en evig skuld; annars
bygger vi en "straffa-konvertiterna"-maskin som belönar stelhet. Föregående mandatperiod = kontext i
`mapping_note`, inte poäng.

### 5.6 Gränserna för steg 2 — när positionering *inte* går att mäta vettigt
- **Magnitud/grad** — binärmodellen (`supports`/`opposes`) kan inte säga "alla stödjer men olika
  mycket". Kräver modellutvidgning (viktad stance, eller instrument uppdelat på ambitionsnivå). Öppen
  designfråga (§8), byggs inte autonomt.
- **Målspråk utan instrument** — om enda belägget är ett mål ("bättre vård") → ingen rad (`unknown`).
- **Aktivitetsbias** — partier som motionerar mer får fler rader. Coverage normeras inte mot antal
  rader; redovisas som flagga (fas4b §9).

### 5.7 Nya indikatorer för steg-1-väggar (modellutvidgning, gräv djupare)
**Vad:** För undermått i §4.2 utan indikator: lägg en **ny indikator med svensk auktoritetsbelagd
riktning** i `categories.yaml`, sedan en åtgärdstyp i evidensliggaren. Öppnar ett annars ouppnåeligt
undermått. Ex: trygghet/`forebyggande` via lag (2023) om kommuners brottsförebyggande ansvar + Brå.
**"L"-arbete** (design + sign-off), inte autonomt.

### 5.8 Sökdjup, eskalering och zoom-ut — när ett delområde/kategori får kallas "uttömt"
> Standard fastlagd 2026-06-06 (skärpt efter diskussion). Första svepet prövade ~1 instrument per otäckt
> undermått i en enda runda och stannade vid "HOLD". Det räcker inte. **Att inte hitta ett instrument är
> INTE en slutpunkt — det är signalen att eskalera.**

**Eskaleringstrappa — deklarera inte "fast" förrän ALLA steg är uttömda:**

1. **Instrument till befintligt undermått (bredd + djup).** Pröva **5–7 genuint olika instrument** per otäckt
   undermått, i **flera rundor** tills två i rad ger noll nytt ("leta tills det är torrt"). Inte ett primärt
   plus närliggande varianter.
2. **Hittar du inget rent instrument → STANNA INTE. Eskalera till nytt undermått.** Kör INTE
   instrument-för-instrument i blindo. Ta ett steg tillbaka:
   - **a.** Läs om kategorin i [../IDEA.md](../IDEA.md) — vad den *ska* fånga + dess caveat.
   - **b.** Bred analys uppifrån-och-ned: vad påverkar *generellt* kategorin positivt enligt officiell svensk
     kunskap (myndigheter, SOU, forskningsöversikter)?
   - **c.** Borra ner till ett **NYTT undermått** (med ny indikator, jfr §5.2/§5.7) som (i) genuint hör hemma i
     kategorin enligt IDEA.md, och (ii) har både evidens (steg 1) och neutral positionering (steg 2).
3. **"Fast"/"uttömt" får sättas FÖRST när både (1) och (2) är uttömda** — och ska då redovisa *vilka*
   instrument **och** *vilka* undermått-vinklar som prövades. "HOLD" ≠ "uttömt": HOLD = ingen ren kandidat i
   *denna* runda på *detta* spår, inte att kategorin är omöjlig.

**Två spärrar som alltid gäller på steg 2:**
- **Fuska inte:** lägg inte ett nytt undermått bara för att slippa ett svårt — det måste genuint höra hemma i
  kategorin (IDEA.md), inte vara en genväg till en lätt fyra.
- **Struktur kräver sign-off:** nytt undermått/indikator ändrar `categories.yaml` + viktbalansen → *föreslås*
  för människan (instrument i befintligt undermått byggs autonomt som v0). Default tills annat sägs.

---

## 6. Statustavla per kategori

Legend: ✅ byggt · 🟡 kandidat (research klar, väntar beslut) · ❌ förkastat (med skäl) · 🟣 steg-1-vägg (modellutvidgning).

### Trygghet — **4/5** ✅ (snabbförfarande byggt 2026-06-06)
- ✅ `snabbforfarande_lagforing` → `handlaggningstid` (Brå 2020:3: handläggningstid i tingsrätt ca −40 %,
  total "mer än halverats"). Enhälligt bet. 2022/23:JuU2 p1 (acklamation; reservation V/C/MP gäller p2,
  de "välkomnar" snabbförfarandet) → **alla 8 supports** (§5.2). authority_evaluation/medium/medium.
  Codex: BUILD-WITH-CHANGES. Icke-rankningsdrivande, lyfter alla i trygghet (+0,04…+0,13).
- 🟡 `kronvittnen` (JuU35 2021/22, 7 Ja/V Nej). ❌-risk: utanför tidsfönster + bara prop-källa + fel
  indikator (grov brottslighet, ej generell uppklaring).
- 🟣 `forebyggande`: saknar indikator → §5.7.

### Klimat — **4/5** ✅ (invasiva arter byggt 2026-06-06; FLAGGAD)
- ✅ `atgarder_mot_invasiva_frammande_arter` → `hotade_arter_naturforlust` (Naturvårdsverket: förteckningen
  är "ett verktyg i arbetet med att förebygga och begränsa spridningen av arter som kan orsaka skador på ...
  biologisk mångfald"). Enhälligt bet. 2025/26:MJU13 p1 (acklamation, "inte väckts någon motion som går
  emot"; tiltade p2 utesluten) → **alla 8 supports** (§5.2). **⚠️ Codex förordade HOLD** (rubrikcitatet
  bevisar hotet, ej instrumenteffekten); byggt som version 0 med **konservativ kalibrering low/low** +
  instrument-mekanismcitat. **FLAGGAD för din sign-off** (§8/§9).
- ❌ bottentrålning / naturvård / levande hav: utformningsstrid eller avslagspunkter (tilt).
- 🟣 `industriell_konkurrenskraft`: saknar indikator → §5.7.

### Försvar — 3/5 (nato byggt; leverans HOLD)
- ✅ `nato_medlemskap` → `nato_interoperabilitet` (votering UU16 2022/23 p1; Försvarsberedningen Ds 2024:6;
  supports S/M/SD/C/KD/L, **opposes V**, **MP=none** [reversering, codex-granskad]). *Flaggat: straffar V.*
- ❌ `genomforbarhet_leverans` HOLD (2026-06-06): inget instrument klarar steg 1 + steg 2 samtidigt. Ren
  positionering finns (FiU39 förenklad upphandling, acklamation) men saknar leveranstid-belägg; SOU 2022:24:s
  lagerhållning/inhemsk kapacitet belägger *försörjningstrygghet*, ej leveranstid, och FöU3 är genomgående
  tiltat (S/C/V/MP-reservationer). Väger 5/100 → tvinga inte. **Återöppna:** prop-fulltext om förenklad
  upphandling ordagrant kopplar till kortare leveranstid, eller RiR/FMV-granskning.
  - **Djupsvep §5.8 (2026-06-06, 7 instrument):** HOLD **bekräftat och härdat** — äkta steg-1-vägg av
    *indikator*-typ. Prövade: ASAP-fakta-pm (EU-källa, "korta leveransledtider" = Kommissionens mål, ingen
    riksdagsbehandling), LUFS-ändring SFS 2023:253 (rör krigsmaterielundantag, ej leveranstid), prop. 2024/25:34
    Totalförsvaret (fulltext grep: 0 träffar instrument→kortad ledtid; "nya materielsystem behöver levereras
    fortare" = uttalat behov, ej instrumenteffekt; gemensam upphandling kopplas till *kostnad/försörjningstrygghet*,
    uttryckligen ej leveranstid), RiR (enda leveranstid-granskningen RiR 2011:13 fann motsatsen — int. samarbeten
    ger *ej* leverans i tid; ingen 2020–2025-granskning), EDIRPA (EU-källa), ökade beställningsbemyndiganden
    (tidigarelägger *order*, ej ledtid; budget→A-dubbelräkning), beredskapslagstiftning (försörjningskapacitet).
    Officiella svenska källor behandlar genomgående lång leveranstid som *exogent marknadsproblem* och
    positionerar instrument mot kapacitet/kostnad — aldrig ordagrant mot kortad ledtid. **Flagga (sign-off):**
    enda B-vägen kan vara att byta/komplettera indikatorn (t.ex. FMV leveransindex som D-serie) → designbeslut.
- 🟣 `ekonomisk_ambition`: `target`-indikator → steg-1-vägg.

### Välfärd — 2/4 (vård + omsorg HOLD)
- ❌ `vard_tillganglighet` HOLD (2026-06-06): **riktningsgrinden faller**. RiR 2023:12 finner vårdgaranti/
  kömiljard/SVF "på många sätt inte effektiva" + undanträngning (mixed/negativ); nationell vårdförmedling är
  *outvärderad* (E-hälsomyndighetens uppdrag 2023, system under uppbyggnad) → vore fabrikat; vårdval (RiR
  2014:22) mixed + neutralitetsbrytande. **Återöppna:** Vård- och omsorgsanalys vårdplats-slutrapport (apr
  2026) eller framtida effektutvärdering av vårdförmedlingen.
  - **Djupsvep §5.8 (2026-06-06, 6 instrument):** HOLD bekräftat. **Återöppningsvillkoret konsumerat negativt** —
    vårdplats-slutrapporten finns nu (Vård- och omsorgsanalys **2026:3 "Brist på plats", 29 apr 2026**) och föll
    *nedåt*: "Hittills ser satsningen inte ut att ha bidragit till att öka antalet vårdplatser på nationell nivå".
    Nära vård ("Omtag för omställning", 31 mars 2025): "inte haft några synliga effekter för befolkningen".
    Vårdförmedling fortsatt outvärderad. **NYTT fynd — cancerscreening är enda vard-instrumentet som passerar
    riktningsgrinden** (Socialstyrelsen: tjock-/ändtarmscancer-screening "sänker dödligheten … med 15 procent",
    mammografi −16/−20 %; konstrukt-exakt mot `overlevnad_svar_sjukdom`) men **faller på neutralitet** — varje
    riksdagskälla 2022–2026 är ett avslag med oppositionsreservationer (SoU16 p2, SoU17 p3); enda enhälliga
    (SoU36 2020/21) utanför fönstret + screening beslutas regionalt. **Bevaka:** enhälligt SoU-betänkande om
    nationella cancerstrategin 2.0 där alla 8 står bakom screening utan tilt → då ren BUILD via §5.2.
- ❌ `omsorg_personal` HOLD (2026-06-06): `fast_omsorgskontakt` har **perfekt steg 2** (lag bet.
  2021/22:SoU24 p2, acklamation, alla 8) men **fel konstrukt i steg 1** — instrumentet rör relationskontinuitet
  *för omsorgstagaren*, inte personalomsättning. Socialstyrelsen fick mars 2026 i uppdrag att utveckla ett
  personalkontinuitetsmått (del 2026-12-16, slut 2027-10-01). **Återöppna:** när det måttet + utvärdering finns.
  - **Djupsvep §5.8 (2026-06-06, 5 instrument):** HOLD bekräftat. Inget instrument har en *färdig officiell
    utvärdering som belägger sänkt personalomsättning*: Äldreomsorgslyftet (mäter kompetens/utbildning, ej
    omsättning), skyddad yrkestitel undersköterska (outvärderad), Heltidsresan (SKR/Kommunal = ej myndighet;
    mäter heltidsandel, ej omsättning), bemanning/arbetsvillkor (endast facklig källa). Socialstyrelsens nya mått
    visar sig vara **samma felkonstrukt** (personalkontinuitet ≠ omsättning) + finns ej förrän dec 2026/okt 2027;
    SKR la dessutom ned kontinuitetsstatistiken 2024 → även dataunderlaget borta. Strukturell vägg (en enda
    indikator, inget partistyrbart instrument flyttar den bevisat nedåt).

### Integration — 2/5 (båda HOLD; högsta bias-risk bekräftad)
- ❌ `normer_tillit` HOLD (2026-06-06): samhällsorientering belägger "kunskap om samhället/etablering", **inte
  tillit/valdeltagande** (instrument-grind faller); AU8 p3 ej enhällig (S-reservation) + är ett *avslag*.
  - **Djupsvep §5.8 (2026-06-06, 6 instrument):** HOLD bekräftat. **Renaste near-miss:** tillgänglighet vid val
    (prop. 2024/25:181, bet. **2025/26:KU4 p1**) har **perfekt steg 2** (acklamation, ingen reservation mot p1,
    SD-reservationer gäller p2/p3 → alla 8 supports) men **fel konstrukt i steg 1** — källan belägger "likvärdig
    möjlighet att utöva rösträtten", inte *uppmätt höjt valdeltagande* (samma samhällsorientering-fälla).
    Övriga: demokratisatsningar (RFR15: "impossible to determine" kausalitet), förtidsröstnings-tillgänglighet
    (akademisk, effekt svag/oklar), föreningsstöd (SOM: korrelation, orsak går institutionstillit→tillit; +
    A-dubbelräkning), hedersförtryck (fel konstrukt). **Återöppna:** svensk källa som kopplar KU4-tillgänglighets-
    åtgärden till *uppmätt högre valdeltagande* → då vänds instrument-grinden och måttet byggs via §5.2.
- ❌ `boendesegregation` HOLD (2026-06-06): ingen kausal svensk *instrument*-utvärdering (Boverket beskrivande);
  CU18 p12 är ett **avslag** med S/V/C-reservationer, underliggande CU6 är regering-vs-vänster-split → tilt.
  - **Djupsvep §5.8 (2026-06-06, 5 instrument):** HOLD bekräftat — **äkta steg-1-vägg (§4.2)**. Ingen svensk
    auktoritetskälla visar att ett *instrument* mäter trångboddhet/segregation NEDÅT: blandade upplåtelseformer
    (mixed), områdesinsatser (förbättrar individer men området oförändrat — folk flyttar + stigma), Boverket
    2023:26 (beskrivande verktygslåda), bostadsförsörjning CU37 p1 (acklamation men rör hyresavtals-säkerhet, ej
    trångboddhet), Delmi 2025:3 (kunskapsöversikt, icke-kvantifierade samband). En reform mot trångboddhet hade
    "rather the opposite effect" (Boverket). **Återöppna:** framtida IFAU/Boverket *instrument*-effektutvärdering.
- 🟣 `migrationssystem`: saknar indikator → §5.7.
- ⚠️ Kategorins egen IDEA.md-caveat ("stor risk för ideologisk bias") **bekräftad i praktiken** → HOLD rätt.

### Demokrati — **4/5** ✅ (public service-lagen byggt 2026-06-06)
- ✅ `lagstadgat_oberoende_public_service` → `mediefrihet` (undermått yttrandefrihet_medier, tidigare B-tomt
  3/5 → **4/5**). Instrument: för första gången regleras public service-uppdraget I LAG (prop. 2024/25:166,
  ur 2023 års **parlamentariska** public service-kommitté SOU 2024:34 "Ansvar och oberoende") med lagstadgat
  oberoende → mediefrihet UPP. Instrument-mekanism (prop. 5.2.1): public service "ska bedrivas självständigt i
  förhållande till såväl staten som olika ekonomiska, politiska och andra intressen … oberoende och stark
  integritet". Enhälligt bet. 2025/26:KrU2 punkt 1 (acklamation, votering-API tomt; "inte väckts någon motion
  som går emot att riksdagen antar regeringens lagförslag"; alla 15 reservationer gäller punkt 2–14, ej p1) →
  **alla 8 supports**. **Codex: BUILD-WITH-CHANGES** (mekanism-/designflagga; snäv formulering lagstadgat
  oberoende → mediefrihet, ej "public service-lag → demokrati"; behåll authority_evaluation/low/low). Icke-
  rankningsdrivande. **Framtida uppgradering:** SOU/utvärdering som belägger varför lagFORMEN (ej bara oberoende
  i sak) stärker institutionellt oberoende.
- 🟡 `transparens_ansvar` (otäckt): **stark återöppning** — prop. 2025/26:258 "Ökad insyn i politiska processer"
  (lobbyregister + förbud mot anonyma/utländska partibidrag), riktning belagd (dir. 2023:88: insyn "förebygger
  korruption och ökar … legitimitet"), ingen dubbelräkning mot offentlighetsprincipen. Steg 2 **ej avgjort än**:
  bet. 2025/26:KU39, beslut **2026-06-15**. Bygg när KU39 är voterat (lobbyregister/anonymförbud brett; **koda EJ**
  del 2 om fackbidrag = S-tilt). Visselblåsarlagen/öppna data-lagen förkastade (tid resp. fel konstrukt).
- ❌ `yttrandefrihet_medier` övriga instrument HOLD: straffskärpning brott mot journalister (V-reservation = krim-
  pol. tilt, ej anti-pressfrihet), nytt mediestöd (förordning → ingen votering; dubbelräkning mot A), massmedie-
  betänkanden KU18 (regering-vs-opp-tilt).

### Ekonomi — 4/6 ✅
- Färdigställt 2026-06-05; se [BACKLOG.md](BACKLOG.md). Alla 4 B-möjliga undermått täckta; inflation/off.finanser
  = target (vilande).

---

## 7. Kandidat-pipeline — utfall 2026-06-06

Sju kandidater researchades med tvåstegsmetoden (steg 1 svensk auktoritetskälla, steg 2 positionering;
varje röstsiffra curl-verifierad mot data.riksdagen.se; codex-2nd-opinion på byggena). **Resultat: 2 byggda,
5 HOLD** — dubblade nattens leverans (1 → 2 nya) och tog trygghet + klimat till 4 undermått.

| # | Kategori → undermått | Åtgärdstyp | Metod | Utfall |
|---|---|---|---|---|
| 1 | trygghet → rättsv.effektivitet | `snabbforfarande_lagforing` | §5.2 enhällighet | ✅ **BYGGT** (Brå 2020:3; JuU2 p1) |
| 2 | klimat → biologisk_mangfald | `atgarder_mot_invasiva_frammande_arter` | §5.2 enhällighet | ✅ **BYGGT** (low/low, FLAGGAD; MJU13 p1) |
| 3 | välfärd → vard_tillganglighet | `nationell_vardformedling` m.fl. | §5.2/§5.3 | ❌ HOLD — riktningsgrind faller (RiR 2023:12 mixed; vårdförmedling outvärderad) |
| 4 | välfärd → omsorg_personal | `fast_omsorgskontakt` | §5.2 | ❌ HOLD — steg 2 perfekt, steg 1 fel konstrukt (kontinuitet ≠ omsättning) |
| 5 | integration → normer_tillit | `samhallsorientering` | §5.2 | ❌ HOLD — belägger kunskap, ej tillit; AU8 ej enhällig |
| 6 | integration → boendesegregation | (CU18 p12) | §5.2/§5.3 | ❌ HOLD — ingen kausal källa; avslag + tilt |
| 7 | försvar → genomforbarhet_leverans | (upphandling/lagerhållning) | §5.2/§5.3 | ❌ HOLD — steg 1 + steg 2 ej uppfyllbara samtidigt |

Återöppningsvillkor per HOLD står i §6. Centralt fynd: **enhällighet-som-källa fungerar** (#1, #2 var
"väggade" under den gamla votering-först-metoden), men den dissolverar bara *steg-2*-väggen — där *steg 1*
(riktningsevidensen) saknas eller är mixed (#3–#7) hjälper ingen positioneringsmetod. Det är gränsen mellan
"källval" och "äkta vägg" (§4), nu empiriskt bekräftad. Förkastningsskäl + dok-id även i [BACKLOG.md](BACKLOG.md).

> **OBS — detta var ett FÖRSTA svep (en runda, ~1 instrument per delområde), inte en uttömmande genomgång.**
> De 5 HOLD och de 4 kategorier under 4 undermått (välfärd 2, integration 2, försvar 3, demokrati 3) ska
> genomgås på nytt enligt **§5.8** (5–7 instrument per delområde, flera rundor, zoom-ut via IDEA.md) innan
> någon kategori avförs som uttömd. "HOLD" här = ingen ren kandidat i runda 1, inte "omöjligt".
>
> **✅ ANDRA SVEPET UTFÖRT 2026-06-06 (§5.8 djupsvep, 4 parallella researchagenter, 7+11+11 instrument):**
> **demokrati löst → 4/5** (public service-lagen, KrU2 p1 enhällighet; se §6). **forsvar/valfard/integration:
> HOLD ×5 bekräftat** efter genuint 5–7+ instrument per delområde — äkta steg-1-väggar (leveranstid,
> boendesegregation), fel konstrukt (omsorg_personal, normer_tillit) eller steg-2-tilt (cancerscreening).
> Skärpta återöppningsvillkor + near-miss-fynd (cancerscreening, KU4-tillgänglighet, KU39-insyn) i §6. Dessa
> tre kategoriers väg till 4 undermått kräver nu **modellutvidgning** (ny indikator/undermått eller nytt
> steg-2-läge) → **sign-off-frågor**, ej autonomt byggbart (§5.8 spärr 2 + §8).

---

## 8. Öppna designfrågor (för dig)

| # | Fråga | Läge / rekommendation |
|---|---|---|
| 1 | **Räkna värdeneutrala konsensus-mått mot 4-undermått-målet?** (steg-1-bra mått, positionerat via enhällighet/§5.2 → alla supports) | Rekommendation: **ja, med disciplin** — ett undermått i taget, enhällighet verifierad, flaggat som icke-rankningsdrivande. Det är BACKLOG-målet "höj B:s trovärdighet". |
| 2 | **Modellutvidgning för grad/magnitud?** (§5.6 — fånga "alla stödjer men olika mycket" ur budgetar) | Större ingrepp (viktad stance / ambitionsnivåer). Inte börjat; kräver designbeslut. Avgör hur mycket budgetdifferentiering vi kan kapitalisera. |
| 3 | **Hur långt bak väger banan?** (§5.5) | Rekommendation: mandatperioden, recency-viktat; varaktiga omsvängningar kodas efter nuläget (nato-regeln). |
| 4 | **Acceptera nato-byggets V-straff?** (V −0,375 i försvar) | ✅ **BESLUTAT 2026-06-06: OK** (objektivt belagt, V genuint Nato-kritiskt). |
| 5 | **Behåll invasiva-arter-måttet (klimat)?** | ✅ **BESLUTAT 2026-06-06: BEHÅLL** ("kan fylla på i framtiden"). Byggt v0 med instrument-mekanismcitat + konservativ low/low + alla 8 supports. |
| 6 | **Ta bort / åtgärda de 7 röda undermåtten?** (a) 4 ej-mätbara *indikatorer* (`personalomsattning_omsorg`, `leveranstid_materiel`, `segregation`, `tillit_valdeltagande` — varken byggbar B eller åtkomlig D); (b) 3 undermått som *saknar indikator helt* (`forebyggande`, `industriell_konkurrenskraft`, `migrationssystem`). Se mätbarhetskartan §4.3. | **ÖPPEN — användarfråga 2026-06-06.** Rekommendation: för (a) ta bort eller omklassa till "kontext, ej betygssatt"; för (b) antingen lägg en **ny indikator** (§5.7, om värdeneutral svensk mätpunkt finns) eller ta bort undermåttet. Behåll de **10 gula** (mätbara, ej byggda — bygg dem). Allt detta ändrar undermåttsvikterna → **sign-off**; rör ej autonomt. (Modellen renormaliserar redan bort tomma undermått, så betygen är oförändrade tills beslut.) |

---

## 9. Beslutslogg

| Datum | Beslut | Skäl |
|---|---|---|
| 2026-06-05 | Mellanstatliga Sverige-utvärderingar tillåtna som **bekräftelse** (ej primär/index) | demokrati saknade officiell svensk effektutvärdering; dokumenterat i DATA.md |
| 2026-06-05 | "Neutralitet före 4" | tiltat mått skadar trovärdighet mer än saknat mått |
| 2026-06-06 | nato_medlemskap byggt (V=opposes, MP=none) | enda rena differentierande försvarsmåttet; codex-granskat. *(Öppen §8.4: V-straffet)* |
| 2026-06-06 | **Tvåstegsmodellen** antagen (§2): måttet ≠ positioneringen; differentiering är utfall, inte krav | natten gav 1 mått för att de två frågorna blandades; "väggen" var till stor del steg-2-källval |
| 2026-06-06 | **snabbforfarande_lagforing byggt** (trygghet 3→4, alla 8 supports) | enhällighet-som-källa, codex BUILD-WITH-CHANGES; första rena tillämpningen av §5.2 |
| 2026-06-06 | **atgarder_mot_invasiva_frammande_arter byggt** (klimat 3→4, alla 8 supports), **men FLAGGAD** | codex förordade HOLD (instrument-precision på rubrikcitatet); byggt v0 med instrument-mekanismcitat + konservativ kalibrering low/low — **din sign-off avgör om det behålls** (§8.5) |
| 2026-06-06 | **5 kandidater HOLD** (vård, omsorg, normer_tillit, boendesegregation, försvar-leverans) | steg 1 saknas/mixed eller fel konstrukt; "neutralitet före 4" + riktningsgrind står över täckningsmålet |
| 2026-06-06 | ✅ nato-byggets V-straff **OK** (användarbeslut) | objektivt belagt; V genuint Nato-kritiskt |
| 2026-06-06 | ✅ invasiva-arter-måttet **behålls** (användarbeslut) | "kan fylla på i framtiden"; värdeneutralt (alla supports), konservativt kalibrerat |
| 2026-06-06 | **Sökdjups-standard antagen** (§5.8): 5–7 instrument/delområde, flera rundor, zoom-ut via IDEA.md innan "uttömt" | första svepet var för grunt (~1 instrument/delområde, en runda); HOLD ≠ uttömt |
| 2026-06-06 | Dagens arbete **committat** (data:-prefix) | användarbeslut; fortsätter i fräsch session med §5.8 som spelbok |
| 2026-06-06 | **public service-lagen byggt** (demokrati 3/5→4/5, alla 8 supports) | enhällighet-som-källa (bet. 2025/26:KrU2 p1, acklamation), codex BUILD-WITH-CHANGES; instrument lagstadgat oberoende (prop. 2024/25:166 ur parlamentarisk kommitté SOU 2024:34) → mediefrihet; mekanism-/designevidens → konservativ kalibrering low/low; icke-rankningsdrivande |
| 2026-06-06 | **Djupsvep §5.8 på forsvar + valfard + integration** → HOLD ×5 bekräftat | 7+11+11 genuint olika instrument prövade (4 parallella researchagenter); äkta steg-1-väggar (leveranstid, boendesegregation) / fel konstrukt (omsorg_personal, normer_tillit) / steg-2-tilt (cancerscreening); återöppningsvillkor skärpta i §6. "Neutralitet före 4" + riktningsgrind står över täckningsmålet |

---

## 10. Verifierings- & provenansstandard (grindar varje mått måste passera)

Sammanfattar grindarna — fullständigt i [fas4b §4, §8](fas4b_partistandpunkter_metod.md) och
[fas4c_rubrik.md](fas4c_rubrik.md).

1. **Riktningsgrind (steg 1)** — instrumentets effekt på indikatorn belagd av officiell svensk källa
   (akademisk svensk om officiell saknas). Negativt B-bidrag kräver `authority_evaluation`/
   `systematic_review` + `confidence ≥ medium` + exakt indikator.
2. **Instrument-grind** — källan avser *samma instrument*, inte bara samma mål (gäller *alla* källor på
   stegen §5.1, inte bara voteringar).
3. **Stance-grind (steg 2)** — ordagrant citat + dok-id; confidence enligt källstegen; `enskild_motion`
   flaggas svag.
4. **Neutralitetsgrind** — inget systematiskt vänster/höger- eller regering-vs-opposition-tilt; buntade
   omnibuspunkter förkastas; vid tvekan codex/2nd-opinion.
5. **Tidsgrind** — föredra innevarande mandatperiod; dokumentera om en hållning kan vara föråldrad
   (jfr MP/nato-reverseringen → `none`, §5.5).
6. **Verifiering** — oberoende kodare hämtar fulltext (`.text`) och prövar quote_found ∧
   instrument_precise ∧ confirmed; default skepsis.

Efter bygge: `python -m pytest -q` (grön), `python -m ruff check pipeline tests` (rent), cyrillisk-koll
`[Ѐ-ӿ]` (0), `pipeline.scorerun` (bygg om dist), `coverage_report` (B4-spridning), `score_diff` (effekt
mot snapshot), `review_packet` (granskningspaket). Snapshot re-baselineas **bara** vid sign-off.

---

## 11. Ändringslogg (denna fil)

| Datum | Ändring |
|---|---|
| 2026-06-06 | Skapad efter natt-resultatet 1 mått: väggen, metodregister (kärna enhällighet-som-källa), designfråga, statustavla, kandidat-pipeline. |
| 2026-06-06 | **Omstrukturerad kring tvåstegsmodellen** (§2): måttet skilt från positioneringen; "väggen" omklassad till steg-1-väggar (äkta) vs steg-2-källval (lösbart, §4); metodregistret blev "steg 2 — positionering" (§5) med källstege + budget-/kommittémotion (§5.3) + banan (§5.5) + uttryckliga gränser inkl. grad/magnitud-begränsningen (§5.6); differentiering omdefinierad som utfall, inte krav; öppna designfrågor samlade (§8). |
| 2026-06-06 | **Första leveransen på metoden:** 7 kandidater researchade (codex-2nd-opinion), **2 byggda** (snabbforfarande → trygghet 4/5; invasiva arter → klimat 4/5, FLAGGAD) **+ 5 HOLD**. §3/§6/§7/§8/§9 uppdaterade med utfall; 36 evidensposter / 192 ståndpunkter; 167 tester gröna, ruff rent, inga nära-binära. Enhällighet-som-källa empiriskt bekräftad (löste steg-2-väggen för #1/#2). |
| 2026-06-06 | **§5.8 sökdjup + zoom-ut tillagt** (5–7 instrument/delområde, flera rundor, läs IDEA.md + bred analys när du kör fast, leta nya undermått). §7 markerat som "första svep, ej uttömt". §8.4/§8.5 markerade BESLUTADE (nato OK, invasiva behålls). Dagens arbete committat; fortsättning i fräsch session. |
| 2026-06-06 | **§5.8 skärpt till eskaleringstrappa:** "inget instrument hittat" är inte slutstation — eskalera då till **nytt undermått** (zoom-ut via IDEA.md). "Fast/uttömt" får sättas först när BÅDE instrument- OCH undermått-spåret är uttömda. Spärrar kvar: fuska inte med undermått, struktur kräver sign-off. |
| 2026-06-06 | **§4.3 mätbarhetskarta tillagd** (på användarfråga): varje indikator klassad B/D → ✅ mäts / 🟡 mätbart-ej-byggt (10) / 🔴 ej mätbart (4) / ⚪ target (3). De 4 röda = exakt de 4 HOLD-undermåtten → designfråga §8.6 (borttagning/omklassning, sign-off). De 10 gula ska byggas, ej strykas. |
| 2026-06-06 | **Andra svepet (§5.8 tillämpat):** demokrati **3/5 → 4/5** via public service-lagen (KrU2 p1 enhällighet, codex BUILD-WITH-CHANGES, low/low). forsvar/valfard/integration djupsvepta (7+11+11 instrument, 4 parallella researchagenter, alla röstsiffror verifierade mot data.riksdagen.se) → **HOLD ×5 bekräftat** med skärpta återöppningsvillkor (§6). Nya fynd: vårdplats-slutrapport 2026:3 föll *nedåt* (villkor konsumerat); **cancerscreening** (valfard) + **KU4-tillgänglighet** (integration) = near-miss som faller på steg-2-tilt resp. fel konstrukt; **KU39 insyn i politiska processer** = stark demokrati-återöppning (beslut 2026-06-15). 37 evidensposter / 200 ståndpunkter; 167 tester gröna, ruff rent, 0 cyrilliska. §3/§6/§9 uppdaterade. |
| 2026-06-06 | **Begreppsmodell stringentad (på användarfråga):** kanonisk vokabulär **Kategori → Undermått → Indikator → Riktning** låst i §4.3-ordlista; "submått" → **Undermått** normaliserat i alla 5 dok (IDEA/DATA/BACKLOG/ROADMAP/evidens_trovardighet, 116 förekomster); IDEA.md + BACKLOG.md pekar nu på §4.3 som sanningskälla. **Config-bugg fixad:** 4 undermåttsnamn (Nato/Skola/Normer/Finansiering) var trunkerade av oquoterade kommatecken i `categories.yaml` flow-YAML → citerade. **§4.3 fick mastertabell** över samtliga **35 undermått / 52 indikatorer** (Kategori/Undermått/Indikator/Riktning/Mätstatus, genererad ur config; de 3 undermått som *saknar indikator* — forebyggande/industriell_konkurrenskraft/migrationssystem — listas som egna rader). dist byte-identisk (namn påverkar ej betyg); 167 tester gröna. |
