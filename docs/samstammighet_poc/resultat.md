# Resultatet av POC:en Samstämmighet

- Datum: 2026-09-14
- Förhandsregistrering: [`forhandsregistrering.md`](forhandsregistrering.md) version 1, låst
  2026-09-14 före den första räkningen
- Räknat av: `python -m pipeline.tools.samstammighet --resultat`
- Talen i maskinläsbar form:
  [`config/samstammighet_poc/resultat.yaml`](../../config/samstammighet_poc/resultat.yaml)

**POC:en klarar alla tre trösklarna.** Beskedet står i [`besked.md`](besked.md).

POC:en mätte skiljbarhet och inget annat. Den bygger inte måttet, den väger 0, och ingenting nedan
säger om ett parti för en bra politik. Ett glapp är ett glapp.

## 1. Utfallet mot trösklarna

| Tröskel | Krav | Utfall | Besked |
|---|---|---|---|
| 1. Skiljbarhet | minst 5 skilda värden, spann minst 0,10 | 8 skilda, spann **0,491** | klaras |
| 2. Längdkonfunden | Pearsons \|r\| under 0,7 | r = **-0,355** | klaras |
| 3. Neutralitet | mellan högst inom | mellan 0,084 mot inom 0,167 | klaras |

Ingen tröskel ligger nära sin gräns. Spannet är nästan fem gånger kravet, längdkonfunden hälften
av sin gräns, och blockskillnaden halva spridningen inom blocken.

## 2. Profilavståndet per parti

Avståndet är den andel av partiets betoning som skulle behöva flytta för att retorikprofilen och
handlingsprofilen skulle sammanfalla. Det är ett avstånd mellan två profiler och inget omdöme.
Ett högt avstånd är inte sämre än ett lågt.

Intervallet är bootstrappens percentil 2,5 till 97,5 över 10 000 omdragningar av partiets egna
manifestposter, med frö 20260914.

| Parti | Avstånd | 95-procentigt intervall | Poster i de sju | Poster utanför |
|---|---|---|---|---|
| V | **0,663** | 0,625 till 0,694 | 159 | 16 |
| KD | **0,463** | 0,395 till 0,531 | 147 | 20 |
| L | **0,364** | 0,304 till 0,430 | 197 | 11 |
| MP | **0,333** | 0,253 till 0,413 | 100 | 7 |
| C | **0,279** | 0,236 till 0,323 | 434 | 52 |
| S | **0,254** | 0,198 till 0,336 | 147 | 15 |
| M | **0,192** | 0,152 till 0,235 | 498 | 27 |
| SD | **0,172** | 0,120 till 0,262 | 127 | 12 |

Intervallen är breda och flera överlappar. V ligger ensamt utanför de andra sju. M och SD går inte
att skilja åt, och inte heller C och S.

160 av de 1 969 posterna bär etiketten `Utanför de sju kategorierna` och räknas bort ur både
täljare och nämnare enligt förhandsregistreringen 2.3. C bär flest, 52 stycken.

## 3. Glappet per cell

Retorikens andel minus handlingens andel. Ett positivt tal betyder att partiet tar upp kategorin
oftare än det lägger kraft där, mätt så som avsnitt 3 i förhandsregistreringen definierar kraft.

| Parti | ekonomi | välfärd | trygghet | försvar | klimat | integration | demokrati |
|---|---|---|---|---|---|---|---|
| S | +0,170 | +0,084 | -0,047 | -0,029 | -0,001 | -0,070 | -0,107 |
| M | +0,053 | +0,086 | +0,054 | -0,038 | -0,018 | -0,042 | -0,095 |
| SD | +0,044 | +0,065 | +0,005 | -0,101 | -0,027 | +0,058 | -0,044 |
| C | +0,099 | +0,141 | +0,040 | -0,055 | -0,058 | -0,114 | -0,052 |
| V | +0,435 | +0,228 | -0,144 | -0,159 | -0,066 | -0,153 | -0,141 |
| KD | +0,240 | +0,223 | -0,057 | -0,152 | -0,079 | -0,069 | -0,107 |
| L | +0,087 | +0,278 | -0,024 | -0,118 | -0,089 | -0,078 | -0,056 |
| MP | +0,051 | +0,051 | -0,053 | -0,103 | +0,231 | -0,106 | -0,071 |

Glappet summerar till noll inom varje parti, eftersom båda profilerna summerar till 1.

### 3.1 Det största positiva glappet

| Parti | Kategori | Glapp | Biljettens handräkning |
|---|---|---|---|
| V | ekonomi | +0,435 | +0,43 |
| L | välfärd | +0,278 | +0,28 |
| KD | ekonomi | +0,240 | +0,24 |
| MP | klimat | +0,231 | +0,23 |
| S | ekonomi | +0,170 | +0,17 |
| C | välfärd | +0,141 | +0,14 |
| M | välfärd | +0,086 | +0,09 |
| SD | välfärd | +0,065 | +0,06 |

**Räkningen reproducerar biljettens handräkning cell för cell.** Handräkningen gjordes 2026-09-13
på tio minuter och kallades uttryckligen varken metod eller resultat. Att den ändå träffar rätt
säger att den normalisering biljetten kallade en gissning är den normalisering som nu är
nedskriven, och ingenting mer.

## 4. Det viktigaste fyndet ligger utanför trösklarna

Trösklarna klaras. Ett efterhandsprov, alltså ett prov som **inte** är förhandsregistrerat och som
inte får ändra något besked ovan, visar var skiljbarheten kommer ifrån.

| Prov | Pearsons r |
|---|---|
| Avståndet mot **retorikens** avstånd till en jämn profil | **0,998** |
| Avståndet mot **handlingens** avstånd till en jämn profil | 0,163 |
| Avståndet med A mot avståndet med a1 rå | **-0,129** |

Talet 0,998 betyder att profilavståndet, på tre decimaler, är samma tal som hur spetsig partiets
retorikprofil är. Handlingssidan flyttar det knappt.

Skälet syns direkt i profilerna:

| Sida | Minsta spridning inom ett parti | Största |
|---|---|---|
| Retoriken | 0,157 (SD) | 0,572 (V) |
| Handlingen, A normerad | 0,022 (L) | 0,036 (MP) |

**A:s normerade profil är nästan jämn för alla åtta partier.** Varje cell ligger mellan 0,123 och
0,165, alltså tätt runt 1/7 = 0,143. Det var förutsagt i förhandsregistreringen 3.2 punkt 1 och 2:
A är en graderad poäng bunden i [0, 5] och mätt mot en historisk förankring, så alla åtta partier
landar nära mitten i alla sju kategorier, och normeringen kan inte skapa en spets som inte finns.

Följden är att den primära uppställningen i praktiken mäter **hur koncentrerat valmanifestet är**,
och inte glappet mellan två sidor. Det är inte samma sak som biljettens fråga.

Raden `-0,129` är den andra halvan av samma fynd. Byts handlingssidan från A till a1 rå, alltså
till en äkta andel av pengar, blir per-parti-talen i stort sett obesläktade med den primära
uppställningens. Måttets utfall hänger alltså på vilken kanal handlingssidan läser, och den frågan
är inte avgjord.

## 5. Varianterna

Alla räknas om hela vägen och prövas mot samma trösklar. Ingen av dem avgör något.

| Variant | Skilda | Spann | Pearson mot längd | mellan / inom | Klarar |
|---|---|---|---|---|---|
| Primär: union mot A | 8 | 0,491 | -0,355 | 0,084 / 0,167 | ja |
| a1 rå som handlingssida | 8 | 0,250 | -0,192 | 0,040 / 0,096 | ja |
| Bara bakåtkorpusen | 8 | 0,547 | -0,238 | 0,114 / 0,171 | ja |
| Bara framåtkorpusen | 8 | 0,456 | -0,507 | 0,074 / 0,153 | ja |
| Största positiva glappet | 8 | 0,370 | -0,418 | 0,077 / 0,121 | ja |
| SD utanför båda blocken | bara neutralitet | - | - | 0,042 / 0,165 | ja |

Varje variant klarar alla tre trösklarna. Det gör utfallet robust mot de val
förhandsregistreringen fick göra, med ett undantag: **rangordningen mellan partierna är det inte.**

| Parti | Avstånd med A | Avstånd med a1 rå |
|---|---|---|
| V | 0,663 | 0,315 |
| KD | 0,463 | 0,176 |
| L | 0,364 | 0,124 |
| MP | 0,333 | 0,373 |
| C | 0,279 | 0,212 |
| S | 0,254 | 0,220 |
| M | 0,192 | 0,285 |
| SD | 0,172 | 0,375 |

SD ligger lägst i den ena kolumnen och högst i den andra. L ligger tredje högst i den ena och
lägst i den andra. Det är samma sak som `r = -0,129` säger, uttryckt i tal läsaren kan följa.

### 5.1 Bakåt mot framåt

Skillnaden mellan de två korpushalvorna är liten för sex partier och tydlig för två. S ligger på
0,235 bakåt och 0,331 framåt, SD på 0,132 bakåt och 0,236 framåt. De övriga sex rör sig mindre än
0,09 mellan halvorna.

Det är underlag till grillningens öppna fråga 4 och inget besked i den.

## 6. Skiljbarheten per kategori

Redovisas enligt förhandsregistreringen 6.1. Utfallet avgör ingenting.

| Kategori | Skilda värden | Spann | Klarar |
|---|---|---|---|
| ekonomi | 8 | 0,390 | ja |
| klimat | 8 | 0,320 | ja |
| välfärd | 8 | 0,227 | ja |
| integration | 8 | 0,211 | ja |
| trygghet | 8 | 0,197 | ja |
| försvar | 8 | 0,131 | ja |
| demokrati | 7 | **0,096** | nej |

Sex av sju kategorier klarar provet. Demokrati faller på spannet, med 0,096 mot kravet 0,10.
Kategorin bär minst retorik hos alla åtta partier, mellan 0,034 och 0,110 av posterna, så det
finns lite att skilja åt där.

## 7. Neutraliteten mellan blocken

| Tal | Värde |
|---|---|
| Regeringssidan (M, KD, L, SD), medel | 0,298 |
| Oppositionen (S, V, C, MP), medel | 0,382 |
| Skillnaden mellan blocken | 0,084 |
| Spridningen inom blocken | 0,167 |
| Kvoten, alltså Cohens d | 0,506 |

Oppositionen ligger högre, men skillnaden är halva spridningen inom blocken. Tröskeln kräver att
skillnaden inte överstiger spridningen, och den gör den inte.

Känslighetsprovet där SD står utanför båda blocken ger en ännu mindre skillnad, 0,042 mot en
spridning på 0,165, alltså d = 0,256.

**Begränsningen skrivs ut:** fyra partier per block ger en mycket osäker skattning av både
skillnad och spridning. Talet säger att måttet inte slår grovt åt ett håll, och ingenting mer.

## 8. Vad räkningen vilar på

| Källa | Vad den bär | Rader |
|---|---|---|
| `config/verklighetsbild/korpus_bakat.yaml` | 896 bakåtposter med kategori | retoriksidan |
| `config/verklighetsbild/korpus_framat.yaml` | 1 073 framåtposter med kategori | retoriksidan |
| `dist/scores.json` | delpoäng A per parti och kategori | handlingssidan, primär |
| `config/budget_ramar.yaml` | partiernas egna utgiftsramar 2011-2025 | handlingssidan, sekundär |
| `config/mappings.yaml` | den sittande regeringens partier och stödparti | blocken |

Ingen ny hämtning skedde. Ingen fil ändrades av räkningen, och `dist/` är orört.

**Framåtkorpusen lästes trots frysningen**, på de villkor förhandsregistreringen 2.2 skrev ned:
ingen post ändrades, ingen post fick ett indikatorval, och ingen post prövades mot ett utfall.
Bara kategorietiketten räknades.

### 8.1 Talen är pinnade till sitt underlag

`resultat.yaml` bär en SHA-256 per källfil under nyckeln `kallhashar`. Radsluten normaliseras
före hashningen, så en utcheckning på Windows ger samma tal som en på Linux.

Skälet är att `dist/scores.json` är en **byggd artefakt**. Den rör sig varje gång pipen körs om,
och en ändring på tredje decimalen i A flyttar varje tal i den här filen. Utan pinnet skulle
resultatet kunna bära tal ingen längre kan återskapa, och ingenting skulle säga det.

Rör sig en källa faller `test_2_kallorna_ar_desamma_som_vid_korningen`, och rättelsen är att köra
om POC:en. Att lossa provet är inte rättelsen. Körningen tar under två sekunder.

**Detta är ett tillägg till specen.** Biljetten krävde bara att räkningen är reproducerbar ur
repot. Pinnet är strängare, aldrig lösare: det prövar påståendet i stället för att utfästa det.

### 8.2 Körningen skedde i ett rent träd

Talen är räknade i en `git worktree` på den committade HEAD, och inte i ett arbetsträd med
oincheckade ändringar. Skälet är att a1 rå läser `pipeline/budget.py`, alltså kod och inte bara
data. Räknas POC:en i ett träd där den koden är under ombyggnad bär resultatet tal som ingen kan
återskapa ur ett klonat repo, och pinnet i 8.1 skulle inte fånga det: hasharna täcker källfilerna
och inte koden som läser dem.

Den som kör om POC:en ska därför göra det i ett rent träd.

## 9. Begränsningarna

1. **Handlingssidan bär knappt någon signal.** Se avsnitt 4. Detta är POC:ens tyngsta
   begränsning, och den låg utanför de tre frågor biljetten ställde.
2. **a2 ingår inte på rå nivå.** Partiets egna motionsantal ligger i det gitignorerade lagret, så
   räkningen skulle inte gå att göra om ur repot. Motionskanalen finns ändå med inbakad i A.
3. **Riktningen saknas.** Ett parti som tar upp något och arbetar emot det behandlas här som ett
   parti som inte arbetar alls. Det är biljettens tillstånd 3, och det är olöst.
4. **Bootstrappen mäter en enda osäkerhet.** Den mäter hur mycket avståndet skulle röra sig om
   partiet skrivit ett annat manifest av samma längd. Osäkerheten i kategorietiketten, i A och i
   normeringen ligger utanför.
5. **Kategorin är grov.** Sju kategorier är en trubbig brygga mellan en mening i ett valmanifest
   och en utgiftspost i en budgetram.
6. **Posten är rubriken.** Korpusposterna bär rubriken ur valmanifestet och inte den fulla
   lydelsen ur PDF:en, precis som Verklighetsbildpiloten fann. Ett parti som skriver långa
   brödtexter under få rubriker räknas därför lägre än ett som punktar upp samma innehåll.

## 10. En rättelse av biljetten

Biljettens steg 3 pekar ut `config/a_forankring.yaml` som platsen för A:s två råkanaler. Den filen
bär **förankringen**, alltså de beslutade utgiftsramarna och kammarens samtliga motioner, och inte
partiets egen täljare. Täljaren ligger i `config/budget_ramar.yaml` för a1 och i lagret för a2.

Rättelsen står också i förhandsregistreringen 3.4, skriven före räkningen.

## 11. Godkännandetesterna

Biljettens åtta regler är prövade i `tests/test_samstammighet_poc.py` och passerar.

Ordningen mellan tröskelvärdena och räkningen går att se på commit-datum, och testet läser den ur
git i stället för att lita på en rad i filen. Ett test kör hela räkningen igen och jämför den mot
den committade filen, så påståendet om reproducerbarhet är prövat och inte bara skrivet.
