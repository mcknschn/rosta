# Fas 4c Plan A — kandidatregister (systematisk skanning per kategori)

> **Status: A1-utkast (2026-05-30).** Detta är den **systematiska skanningen FÖRE filter** (rubrik §6–§8,
> Codex P0 mot cherry-picking): vi listar de instrument partierna faktiskt driver i varje kategori — både
> konsensus och omstridda — och noterar två attribut: (1) **contested?** (splittrar partierna supports/opposes)
> och (2) **officiell riktad evidens?** på en kategori-indikator. Admission till B kräver intersektionen
> contested ∧ evidensbelagd, OCH att evidensen passerar admission/negativ-grinden i A3.
>
> **VIKTIGT:** evidens-kolumnen nedan är en **hypotes om var evidens kan finnas** — ingen källa här är
> verifierad ännu. A3 hämtar och bekräftar varje fynd live (officiell svensk källa, exakt indikator). Faller
> en hypotes vid A3 → instrumentet blir inert/utelämnas, inte kodat. Vi börjar alltså INTE från striden och
> letar evidens i efterhand; vi kräver att evidensen håller självständigt.

Legend för **verdikt**: `KANDIDAT` = går vidare till A3-evidensverifiering · `KONSENSUS` = ej omstridd, ger
ingen särskiljning (skippas) · `VÄRDE-INERT` = omstridd men sannolikt ingen riktad officiell evidens / mixed
→ utelämnas (B tiger) · `FINNS` = redan i liggaren.

---

## Ekonomi (indikatorer: sysselsattning↑, arbetsloshet↓, bnp_per_capita↑, produktivitet↑, realloner↑, inflation~mål, statsskuld~mål)

| Instrument | contested? | officiell riktad evidens (hypotes) | verdikt |
|---|---|---|---|
| subventionerade anställningar | ja | IFAU (FINNS) | FINNS |
| arbetsmarknadsutbildning | ja | IFAU (FINNS) | FINNS |
| a-kassa: ersättningsnivå/varaktighet | **ja** (V/S/MP höjer, M/SD/KD/L stramar) | IFAU: högre/längre ersättning → längre arbetslöshetstid (sök-teori). **Negativ på `arbetsloshet`** | **KANDIDAT** (negativ-grind + brygg-kodifiering krävs) |
| jobbskatteavdrag | ja | IFAU: svår att utvärdera, unclear (FINNS som inert) | VÄRDE-INERT |
| RUT/ROT-avdrag | ja | IFAU/Skatteverket: sysselsättningseffekt liten/mixed | VÄRDE-INERT (mixed → ev. A3-check) |
| sänkt arbetsgivaravgift unga | delvis (historiskt) | IFAU 2013: dyr, svag effekt → unclear/low | VÄRDE-INERT |
| höjt/sänkt bolagsskatt | ja | ingen ren svensk indikator-kausalstudie | VÄRDE-INERT |
| yrkesvux-expansion | mest konsensus | Skolverket/IFAU: positiv på sysselsättning | KONSENSUS (kolla split i A1+) |

## Välfärd (vardkoer↓, vard_i_tid↑, overlevnad↑, skolresultat↑, skillnader_skolor↓, behoriga_larare↑, personalomsattning↓, valfardsbrottslighet↓)

| Instrument | contested? | officiell riktad evidens (hypotes) | verdikt |
|---|---|---|---|
| kompetensutveckling lärare, minskad klasstorlek, tidiga insatser, kontroller välfärdsbrott | — | IFAU/Brå (FINNS) | FINNS |
| vårdval/LOV i primärvården | **ja** (M/KD/L/C pro, V/S/MP skeptiska) | Vårdanalys/Riksrevisionen: ökad tillgänglighet/etableringar; likvärdighet mixed | **KANDIDAT** (dela: tillgänglighet vs likvärdighet; A3 avgör riktning) |
| vinst i välfärden / vinstbegränsning | ja | Officiell evidens på skolresultat/kvalitet genuint mixed | VÄRDE-INERT |
| marknadsskola / fristående skolor / fritt skolval | ja | IFAU/Skolverket friskolereform: skolresultat mixed/likvärdighet negativ? | VÄRDE-INERT (möjlig A3-check på `skillnader_mellan_skolor`) |
| betygssystem / tidigare betyg | ja | evidens tunn | VÄRDE-INERT |
| karensavdrag/karensdag | ja | ingen ren indikator-evidens i kategorin | VÄRDE-INERT |

## Trygghet (dodligt_vald↓, skjutningar↓, brottsutsatthet↓, upplevd_otrygghet↓, uppklaringsgrad↑, handlaggningstid↓, aterfall↓)

| Instrument | contested? | officiell riktad evidens (hypotes) | verdikt |
|---|---|---|---|
| behandlingsprogram, GVI, utomhusbelysning | — | SBU/Brå (FINNS) | FINNS |
| visitationszoner (stopp-och-visitera) | **ja** (M/SD/KD pro, V/MP/C/S-nyans con) | Brå/forskning: svag/osäker effekt på brott | **KANDIDAT→trolig VÄRDE-INERT** (om Brå mixed/unclear → signed 0; A3 avgör) |
| skärpta straff / längre fängelsestraff | **ja** (höger pro, vänster skeptisk) | Brå: avskräckningseffekt av strafflängd svag/osäker; inkapacitering separat | **KANDIDAT→trolig VÄRDE-INERT** (A3: finns riktad Brå-evidens på `aterfall`/`brott`?) |
| fler poliser / polistäthet | mest konsensus nu | Brå/forskning: effekt på brott osäker | KONSENSUS/VÄRDE-INERT |
| avhopparverksamhet | mest konsensus | viss positiv evidens | KONSENSUS |
| kameraövervakning | ja | Brå: mixed (FINNS som inert) | VÄRDE-INERT |

## Klimat (territoriella_utslapp↓, konsumtionsbaserade↓, fossil_energianvandning↓, elprisvolatilitet↓, effektbrist↓, utslappsminskning_per_krona↑, hotade_arter↓)

| Instrument | contested? | officiell riktad evidens (hypotes) | verdikt |
|---|---|---|---|
| koldioxidskatt, reduktionsplikt | ja | RiR/Naturvårdsverket (FINNS) | FINNS |
| ny kärnkraft / utbyggd kärnkraft | **ja** (M/SD/KD/L pro, MP/V/(C) con) | Energimyndigheten/Svk: fossilfri baskraft → lägre `fossil_energianvandning`/`effektbrist`; kostnad per kWh omstridd | **KANDIDAT** (positiv på effektbrist/fossil; kostnadseffektivitet trolig mixed→inert) |
| elbilsbonus / bonus-malus | **ja** (avskaffat av nuv. regering) | Trafikanalys/officiell: effekt på transportutsläpp | **KANDIDAT** (A3: riktad evidens på `territoriella_utslapp`?) |
| havsbaserad vindkraft | ja | Energimyndigheten/Svk: effekt på fossil/effekt | KANDIDAT→A3-check |
| sänkt drivmedelsskatt (energiskatt) | ja | jfr reduktionsplikt; ej dubbelkoda | VÄRDE-INERT (överlappar reduktionsplikt) |

## Integration (sysselsattningsgap↓, sjalvforsorjningsgrad↑, bidragsberoende↓, sfi↑, skolresultat_utsatta↑, trangboddhet↓, segregation↓, tillit↑)

| Instrument | contested? | officiell riktad evidens (hypotes) | verdikt |
|---|---|---|---|
| aktiveringskrav, sfi+praktik, språkpraktik, riktade insatser nyanlända | ja/nej | IFAU/Skolverket (FINNS) | FINNS |
| bidragstak / kvalificeringstid till bidrag | **ja** (höger pro, vänster con) | IFAU/ESO: incitamentseffekter på självförsörjning/bidragsberoende | **KANDIDAT** (A3: tight instrument-matchning krävs, ej generisk "incitament") |
| etableringsersättning villkor | ja | IFAU etableringsreformen | KANDIDAT→A3-check |
| arbetskraftsinvandring / lönekrav | ja | evidens tunn på kategori-indikatorer | VÄRDE-INERT |
| medborgarskaps-/språkkrav | ja | evidens tunn | VÄRDE-INERT |

## Försvar (forsvarsanslag~mål, personal_varnpliktiga↑, materiel↑, civil_beredskap↑, ukraina_stod↑, leveranstid↓, nato_interop↑)

| Instrument | contested? | officiell riktad evidens (hypotes) | verdikt |
|---|---|---|---|
| värnplikt, civilt försvar | — | RiR (FINNS) | FINNS |
| NATO-medlemskap | ej längre contested | — | KONSENSUS |
| höjda försvarsanslag (mot mål) | mest konsensus | — | KONSENSUS |
| internationella materielsamarbeten | (negativ) | RiR 2011:13 sidoeffekt (FINNS, exkluderad) | EXKLUDERAD (E1) |
| *Försvar är i praktiken konsensus-tungt → liten särskiljningspotential i B.* | | | |

## Demokrati (korruption↓, fortroende↑, mediefrihet↑, politisk_transparens↑, otillborlig_politisering↓, overvakning_utan_rattssakerhet↓)

| Instrument | contested? | officiell riktad evidens (hypotes) | verdikt |
|---|---|---|---|
| antikorruption, granskning/insyn, otillåten påverkan | mest konsensus | Statskontoret/ESO/Brå expert (FINNS, expert_opinion/low) | FINNS |
| utökad övervakning (datalagring, hemlig dataavläsning, kamera) | **ja** (höger/SD pro, V/MP/(C/L) integritetscon) | trolig expert-nivå; indikator `overvakning_utan_rattssakerhet`↓ → negativ riktning | **KANDIDAT→trolig VÄRDE-INERT** (negativ-grind kräver authority_evaluation+; expert_opinion räcker EJ) |
| anonyma vittnen | ja | evidens tunn | VÄRDE-INERT |

---

## Sammanfattning — A3-kandidater (måste passera evidensverifiering + grindarna)

1. **a-kassa nivå/varaktighet** (ekonomi → `arbetsloshet`, NEGATIV; kräver brygg-kodifiering arbetslöshetstid→arbetsloshet + negativ-grind).
2. **ny kärnkraft** (klimat → `fossil_energianvandning`/`effektbrist`, POSITIV; kostnadseffektivitet trolig inert).
3. **vårdval/LOV** (välfärd → `vard_i_tid` tillgänglighet POSITIV; likvärdighet trolig mixed→inert).
4. **elbilsbonus/bonus-malus** (klimat → `territoriella_utslapp`).
5. **bidragstak/kvalificeringstid** (integration → `sjalvforsorjningsgrad`/`bidragsberoende`).
6. (svaga, trolig inert efter A3: visitationszoner, skärpta straff, utökad övervakning — behålls i loggen som granskade-men-ej-admitterade om Brå/expert-evidensen är mixed/unclear eller bara expert_opinion.)

**Disclosure (rubrik §6):** B mäter *evidens-kodbar instrumentell träffsäkerhet*, inte all viktig politik. Flera
av de mest värdeladdade striderna (vinst i välfärden, marknadsskola, arbetskraftsinvandring, anonyma vittnen)
saknar riktad officiell evidens på kategori-indikatorerna och förblir därför **medvetet okodade** i B. Det är en
egenskap, inte en lucka: där evidensen tiger ska B tiga.


---

## A3-utfall — evidensverifiering (2026-05-30, workflow w7vm2q3hn)

Systematisk evidens-research + adversariell verifiering av 8 kandidat-instrument mot officiella
svenska källor (WebFetch). **Endast 1 av 8 passerade** admission/negativ-grinden. Detta är det
centrala fyndet: de flesta värde-omstridda instrument saknar *robust riktad* officiell evidens på
exakt kategori-indikatorn — där evidensen är blandad kodas instrumentet **inert** (B tiger, rubrik §6).

### ✅ Admitterad (1)
- **ny_karnkraft_effektbrist** → indikator `effektbrist` (klimat), riktning **positive**, authority_evaluation/high. Källa: Svenska kraftnät, Kraftbalansen på den svenska elmarknaden, rapport 2025 (lagstadgad rapport till regeringen enligt 3 § förordning 2007:1119) ([källa](https://www.svk.se/49bb53/siteassets/om-oss/rapporter/2025/kraftbalansen-pa-den-svenska-elmarknaden-rapport-2025.pdf)). Kodad som policy_type `ny_karnkraft` i evidensliggaren.

### ⛔ Inerta / ej admitterade (7) — verklig officiell källa men blandad/svag/fel-indikator-evidens
| kandidat | indikator | källa (officiell) | varför inert |
|---|---|---|---|
| `hojd_a_kassa` | `arbetsloshet` | [IFAU, IFAU Rapport 2005:16 (Bennmarker, Carling, Holmlund) — "Lede](https://www.ifau.se/Forskning/Publikationer/Rapporter/2005/Leder-hojd-a-kassa-till-langre-arbetsloshetstider-En-studie-av-de-svenska-forandringarna-2001-2002/) | IFAU 2005:16: effekter 'inte statistiskt säkerställda', motsatt tecken för kvinnor; bryggan arbetslöshetstid→arbetslöshetsnivå håller ej → mixed (negativ-grind ej passerad). |
| `ny_karnkraft_fossil` | `fossil_energianvandning` | [Energimyndigheten, Långsiktiga scenarier över Sveriges energisystem 2023 (ER 20](https://www.energimyndigheten.se/49428c/globalassets/statistik/prognoser-och-scenarier/langsiktiga-scenarier/langsiktiga-scenarier-over-sveriges-energisystem-2023.pdf) | Energimyndigheten ER 2023:07 (scenarier): blandad/scenariebroende effekt på fossil energianvändning → mixed. |
| `vardval_lov` | `vard_i_tid` | [Riksrevisionen, RiR 2014:22 (Primärvårdens styrning – efter behov eller efte](https://www.riksrevisionen.se/granskningar/granskningsrapporter/2014/primarvardens-styrning---efter-behov-eller-efterfragan.html) | Riksrevisionen RiR 2014:22: ökad tillgänglighet men styrning 'efter efterfrågan snarare än behov' → blandad riktning på vård i tid → mixed. |
| `bonus_malus` | `territoriella_utslapp` | [Naturvårdsverket; Riksrevisionen; Konjunkturinstitutet, Naturvårdsverket Rapport 7194 (ISBN 978-91-620-7194-3); Riks](https://www.naturvardsverket.se/publikationer/7100/978-91-620-7194-3/) | Naturvårdsverket R7194 / RiR 2020:1: utsläppseffekt vs kostnadseffektivitet blandad/kritiserad → mixed. |
| `bidragstak` | `bidragsberoende` | [IFAU, IFAU remissvar (dnr 2025): "Kvalificering till socialförsäkr](https://www.ifau.se/Om-IFAU/Remissvar/kvalificering-till-socialforsakring-och-ekonomiskt-bistand-for-vissa-grupper/) | IFAU remissvar SOU 2025:53: starkare incitament men osäkra/blandade nettoeffekter; ej tight instrument-evidens → mixed. |
| `visitationszoner` | `brottsutsatthet` | [Polismyndigheten (analys av säkerhetszon i Eskilstuna 2024); jfr Ds 2023:31, Polismyndighetens interna analys av säkerhetszonen i Eskilst](https://www.svt.se/nyheter/lokalt/ost/polisens-analys-sakerhetszonen-hade-ingen-matbar-paverkan) | Polismyndighetens utvärdering (Hageby/Eskilstuna 2024): 'ingen mätbar påverkan', endast enskild studie/låg → mixed/svag. |
| `skarpta_straff` | `aterfall_i_brott` | [Brottsförebyggande rådet (Brå), Brå Rapport 2024:1 (urn:nbn:se:bra-1158)](https://bra.se/download/18.403f39de192bd4311313edc/1730191258452/2023_1-Forskning-om-alder-och-brott.pdf) | Brå 2024:1: avskräckningseffekt av strafflängd oklar → unclear. |

**Slutsats Plan A:** B fick **en** ny särskiljande åtgärdstyp (`ny_karnkraft` → effektbrist). Att 7 av 8
kandidater stannade inerta är inte ett misslyckande utan en bekräftelse på modellens objektivitet: B
vägrar koda en riktning som officiell svensk evidens inte robust stödjer. De inerta hålls i denna logg
(granskade-men-ej-admitterade) så att en människa kan ompröva om/när starkare evidens publiceras.


---

## A5 — känslighetsanalys (2026-05-30)

Plan A admitterade **1** ny åtgärdstyp: `ny_karnkraft` → indikator `effektbrist` (positiv). Kodad för 7/8
partier (S/M/SD/KD/L supports, V/MP opposes; C = lucka, verifieraren underkände C:s permissiva citat).
Totalt 130 partiståndpunkter (123 + 7).

**Ranking utan vs med `ny_karnkraft`** (standardvikter):

| Parti | Utan (post-Plan B) | Med | Δ |
|---|---|---|---|
| S  | 3.71 | 3.72 | +0.01 |
| L  | 3.37 | 3.39 | +0.02 |
| MP | 3.41 | 3.34 | -0.07 (faller under L) |
| M  | 3.28 | 3.30 | +0.02 |
| KD | 3.10 | 3.12 | +0.02 |
| V  | 2.67 | 2.59 | -0.08 |
| SD | 2.33 | 2.41 | +0.08 (över C) |
| C  | 2.40 | 2.39 | -0.01 |

Effekten är **måttlig och proportionerlig** (max ±0.08): MP/V (motsätter sig ny kärnkraft) får ett
negativt B-bidrag på `effektbrist` (klimat), SD/M/KD/L/S ett positivt. MP byter plats med L; SD passerar C.
Klimat väger 12,5 %, B 35 % av kategorin, och bidraget är coverage-viktat — därför blir utslaget begränsat.

**Känslighet för negativ evidens:** modellen har **noll admitterade negativ-riktnings-poster** som bidrar
till B (den enda, `internationella_materielsamarbeten`, är exkluderad enligt E1). V/MP:s negativa
klimat-bidrag kommer från att `opposes` VÄNDER en *positiv* evidenspost (de motsätter sig ett instrument som
officiell evidens säger hjälper indikatorn) — inte från någon admitterad negativ evidens. "Ranking med
negativa instrument borttagna" är därför identisk med nuvarande modell. Detta är den avsedda semantiken och
det starkaste skyddet mot partiskhet: B drar bara ned ett parti när partiet aktivt motsätter sig ett
robust evidensbelagt instrument, aldrig på grund av en svag eller sidoeffekts-baserad negativ evidenspost.

**Flaggat för mänsklig granskning:** `ny_karnkraft` är en laddad energifråga. Att MP/V får lägre klimat-B för
att motsätta sig ny kärnkraft vilar på Svenska kraftnäts robusta fynd om planerbar baskrafts roll för
effekttillräcklighet — men en människa bör bekräfta att detta är en rimlig kodning av partiernas faktiska
energilinjer (båda förespråkar andra effektlösningar; evidensen visar dock att intermittent kraft bidrar
marginellt vid topplast).
