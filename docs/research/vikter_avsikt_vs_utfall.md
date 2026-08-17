# Vikter: avsikt mot uppmätt utfall

**Underlag till issue #8. Ingen rekommendation.**

Beslutet om vikterna fattas i en annan biljett. Det här dokumentet redovisar vad
metodlitteraturen säger. Det tar inte ställning till om 40/35/15/10 ska ändras.

Källorna nedan är **metodlitteratur**, inte datakällor. Projektets källregel om
officiella svenska data gäller data, inte metod. Internationell metodlitteratur
och granskad forskning används här enligt den avgränsningen.

Läsdatum för alla webbsidor: 2026-08-17.

---

## 0. Vad jag läste och hur

Jag skiljer på tre lägen:

| Läge | Betydelse |
|---|---|
| **Full text** | Jag laddade ned dokumentet och läste det aktuella avsnittet i original. |
| **Utdrag** | Jag nådde originalet via hämtverktyg som gav ordagranna stycken, inte hela texten. |
| **Endast sammanfattning** | Jag nådde bara förlagets eller arkivets ordagranna sammanfattning. Full text låg bakom betalvägg. |

Varje källa i avsnitt 5 är märkt med sitt läge.

---

## 1. Delfråga 1: OECD och JRC om viktval, känslighetsanalys och lika vikter

Huvudkällan är OECD och JRC, *Handbook on Constructing Composite Indicators:
Methodology and User Guide* (OECD 2008). Sidhänvisningar avser handbokens tryckta
sidnummer. Jag läste hela handboken i full text.

### 1.1 Vikter är värderingar, inte mätresultat

Handboken är rak på den punkten (s. 31):

> "Regardless of which method is used, weights are essentially value judgements.
> While some analysts might choose weights based only on statistical methods,
> others might reward (or punish) components that are deemed more (or less)
> influential, depending on expert opinion, to better reflect policy priorities
> or theoretical factors."

Den kräver inte en objektiv härledning. Den kräver öppenhet (s. 33):

> "The absence of an 'objective' way to determine weights and aggregation methods
> does not necessarily lead to rejection of the validity of composite indicators,
> as long as the entire process is transparent. The modeller's objectives must be
> clearly stated at the outset, and the chosen model must be tested to see to what
> extent it fulfils the modeller's goal."

Kravlistan efter steg 6 säger vad som ska finnas på plats (s. 34). Vikterna ska
väljas "with reference to the theoretical framework". Alternativa metoder ska ha
övervägts. Valet ska dokumenteras och förklaras.

**Vad det betyder för #8:** handboken kräver ett skäl kopplat till modellens syfte,
plus dokumentation. Den kräver inte att skälet ska vara statistiskt.

### 1.2 Lika vikter: vad handboken faktiskt säger

Handboken rekommenderar inte lika vikter. Den beskriver dem, och den varnar (s. 31):

> "Most composite indicators rely on equal weighting (EW), i.e. all variables are
> given the same weight. This essentially implies that all variables are 'worth'
> the same in the composite, but it could also disguise the absence of a
> statistical or an empirical basis, e.g. when there is insufficient knowledge of
> causal relationships or a lack of consensus on the alternative. In any case,
> equal weighting does not mean 'no weights', but implicitly implies that the
> weights are equal."

Två saker följer. Lika vikter är ett val, inte frånvaro av val. Lika vikter kan
dölja att underlaget saknas.

Handboken pekar också ut en fälla i nästlade strukturer (s. 31). Lika vikt på alla
indikatorer ger ojämn vikt på dimensionerna, eftersom den dimension som samlar
flest indikatorer får störst tyngd. Rösta har den nästlade strukturen: kategori,
undermått, indikator.

**Jag hittade ingen passage i handboken som säger när lika vikter är att föredra
framför satta vikter.** Handboken ställer inte den frågan.

Frågan besvaras däremot i beslutslitteraturen. Robyn Dawes, "The Robust Beauty of
Improper Linear Models in Decision Making", *American Psychologist* 34(7), 1979,
s. 571-582, läst i full text. Sammanfattningen (s. 571):

> "In fact, unit (i.e., equal) weighting is quite robust for making such
> predictions."

Skälet står på s. 577:

> "The solution to the problem of obtaining optimal weights is one that -- in terms
> of von Winterfeldt and Edwards (Note 4) -- has a 'flat maximum.' Weights that are
> near to optimal level produce almost the same output as do optimal beta weights."

Dawes refererar också ett fall där beslutsfattarna inte kunde enas om vikter (s. 577):

> "Since policymakers could not agree about the weights given to the three
> dimensions, Hammond and Adelman suggested that they be weighted equally."

Och slutsatsen som citeras från Dawes och Corrigan 1974, s. 105 (Dawes 1979, s. 577):

> "the whole trick is to decide what variables to look at and then know how to add"

**Två gränser för Dawes.** Resultatet gäller prediktion mot ett känt kriterium.
Rösta har inget sådant kriterium att validera mot. Dawes jämför dessutom lika
vikter mot vikter hämtade ur mänskliga bedömares beteende, inte mot vikter satta
utifrån en teori om vad indexet ska mäta.

### 1.3 I linjär aggregering är vikter utbytesförhållanden, inte betydelsegrader

Det här är handbokens skarpaste punkt för en modell som Röstas. Rösta använder
linjär aggregering: en viktad summa av A, B, C och D.

Handboken (s. 33):

> "In both linear and geometric aggregations, weights express trade-offs between
> indicators. A deficit in one dimension can thus be offset (compensated) by a
> surplus in another. This implies an inconsistency between how weights are
> conceived (usually measuring the importance of the associated variable) and the
> actual meaning when geometric or linear aggregations are used."

Samma sak i avsnittet om AHP (s. 97):

> "Weights represent the trade-off across indicators. They measure willingness to
> forego a given variable in exchange for another. Hence, they are not importance
> coefficients."

Fotnoten till tabell 4 (s. 31) säger det kort: "With both linear and geometric
aggregations weights are trade-offs and not 'importance' coefficients."

**Vad det betyder för #8:** frågan "hur viktigt är uppmätt utfall" är inte den
fråga en vikt i en linjär summa besvarar. Vikten säger hur mycket A som krävs för
att kompensera en förlust i D. Handboken tillägger att en icke-kompenserande
metod krävs om olika mål inte får ersätta varandra (s. 33).

### 1.4 Nominell vikt är inte faktisk påverkan

Det här är den nyare JRC-linjen. Två arbeten bär den.

Paruolo, Saisana och Saltelli, "Ratings and rankings: voodoo or science?",
*Journal of the Royal Statistical Society: Series A* 176(3), 2013, s. 609-634.
Läst i full text. Sammanfattningen:

> "Because socio-economic variables are heteroscedastic and correlated, relative
> nominal weights are hardly ever found to match relative main effects"

De ger ett exempel som ligger nära Röstas fall med fyra delpoäng (s. 613):

> "A hypothetical sustainability index could have environmental, economic, social
> and institutional pillars, and equal weights for these four pillars would flag
> the developers' belief that these dimensions share the same importance. Still one
> of the four pillars with a weighting in principle of 25% could contribute little
> or nothing to the index, e.g. because the variance of the pillar is comparatively
> small and/or the pillar is not correlated to the remaining three."

Slutsatsen (s. 631):

> "practitioners know that weights cannot be used as importance, although they are
> precisely elicited as if they were. Weights are instead measures of
> substitutability in linear aggregation. The error is particularly severe when a
> variable's weight substantially deviates from its relative strength in
> determining the ordering of the units (e.g. countries) being measured."

De prövade också om man kan räkna baklänges från önskad betydelse till nominella
vikter (s. 630-631):

> "Our reverse engineering analysis shows that in most cases it is not possible to
> find nominal weights that would give the desired importance to variables."

Deras tre råd till indexbyggare (s. 631-632), i sammanfattning: sluta likställa
nominell vikt med betydelse och redovisa den faktiska betydelsen i stället; låt bli
att aggregera pelare som står i tydlig målkonflikt; överväg en icke-kompenserande
aggregering.

Becker, Saisana, Paruolo och Vandecasteele, "Weights and importance in composite
indicators: Closing the gap", *Ecological Indicators* 80, 2017, s. 12-22. Läst i
utdrag via öppen version. Inledningen:

> "A possible misconception is that the weight assigned to a variable can be
> directly interpreted as a measure of importance of the variable to the resulting
> value of the composite indicator."

> "However this is rarely the case: different variances and correlations among
> variables, for instance, prevent the weights from corresponding to the
> variables' importance."

**Vad det betyder för #8:** D:s nominella 10 procent säger inte hur mycket D
faktiskt flyttar rankingen. Det måste mätas i data. Om D har liten spridning
mellan partierna, eller korrelerar starkt med A och B, kan D:s faktiska påverkan
ligga långt under 10 procent. Den kan också ligga över.

### 1.5 Osäkerhets- och känslighetsanalys

Handbokens steg 7 heter "Uncertainty and sensitivity analysis". Den är inte
frivillig i handbokens uppställning (s. 117):

> "Composite indicator development involves stages where subjective judgements have
> to be made: the selection of individual indicators, the treatment of missing
> values, the choice of aggregation model, the weights of the indicators, etc. All
> these subjective choices are the bones of the composite indicator"

Handboken listar sju osäkerhetskällor som bör prövas (s. 34). Punkt 5 och punkt 7
rör vikter direkt:

> "5. Using different weighting schemes, e.g. methods from the participatory family
> (budget allocation, analytic hierarchy process) and endogenous weighting (benefit
> of the doubt)."

> "7. Using different plausible values for the weights."

Kravlistan efter steg 7 (s. 35) säger att byggaren ska ha

> "Conducted sensitivity analysis of the inference, e.g. to show what sources of
> uncertainty are more influential in determining the relative ranking of two
> entities."

Handboken visar också hur mycket viktvalet kan flytta en ranking. I dess eget
exempel, Technology Achievement Index med åtta indikatorer, hamnar Korea på plats
2 med AHP-vikter och på plats 5 med lika vikter (tabell 23, s. 100).

Handbokens egen körning av steg 7 ger också en rangordning mellan felkällor
(s. 131):

> "In the current set-up, the uncertainties of higher order are expert selection and
> weighting scheme (second analysis). A fortiori normalisation does not affect
> output when the very aggregation system is uncertain (first analysis). In other
> words, when the weights are uncertain, it is unlikely that normalisation and
> editing will affect the country ranks."

Viktvalet hör alltså till de val som styr rankingen mest. Normalisering och
imputering hör till de val som styr minst.

Handboken varnar samtidigt för att tro att robusthetsprövning räcker (s. 35):

> "Is the assessment of robustness enough for guaranteeing a sensible composite?
> Certainly not. We already claimed that a sound theoretical framework is the
> primary ingredient."

**Vad det betyder för #8:** metoden pekar mot att köra rankingen med flera
viktuppsättningar och redovisa hur mycket den rör sig. Det är en mätning, inte en
rekommendation om vilken vikt som ska väljas.

**Not om projektets blindregel.** Kartans regel säger att vikter fattas blint mot
rankingen. Handbokens steg 7 säger att viktvalets effekt på rankingen ska mätas
och redovisas. De två går att förena i tid: först besluta blint, sedan mäta och
publicera effekten. De går inte att förena om mätningen får styra beslutet. Jag
hittade ingen källa som behandlar den konflikten. Detta är min egen läsning av två
regler, inte ett litteraturfynd.

### 1.6 Handbokens regel om avsiktsmått mot utfallsmått

Handboken tar upp blandningen av input och output redan i steg 1. Det är den
passage som ligger närmast Röstas fråga (s. 22):

> "Too often composite indicators include both input and output measures. For
> example, an Innovation Index could combine R&D expenditures (inputs) and the
> number of new products and services (outputs) in order to measure the scope of
> innovative activity in a given country. However, only the latter set of output
> indicators should be included (or expressed in terms of output per unit of input)
> if the index is intended to measure innovation performance."

Och kort på s. 23:

> "the type of variables selected -- input, output or process indicators -- must
> match the definition of the intended composite indicator."

**Vad det betyder för #8:** handboken villkorar hela frågan. Regeln är inte
"utfall ska väga tungt". Regeln är "typen av mått ska matcha vad indexet påstår
sig mäta". Ett index som säger sig mäta *utfört resultat* ska enligt handboken
bygga på utfallsmått. Ett index som säger sig mäta något annat får bygga på annat.
Rösta måste alltså först fastställa vad kategoripoängen påstår sig mäta. Vikterna
följer av det, inte tvärtom.

### 1.7 Två sidopunkter ur handboken

**Vikt efter datakvalitet.** Handboken nämner tanken och varnar för den (s. 32):

> "Weights may also be chosen to reflect the statistical quality of the data.
> Higher weights could be assigned to statistically reliable data with broad
> coverage. However, this method could be biased towards the readily available
> indicators, penalising the information that is statistically more problematic to
> identify and measure."

**50-procentsregeln.** Handboken skriver (s. 111):

> "In general, it is essential that no indicator weight constitute more than 50% of
> the total weights; otherwise the aggregation procedure would become
> lexicographic in nature, and this individual indicator would become a dictator in
> Arrow's terminology. Following from this, when indicator weights are derived from
> different dimensions, the requirement is that no dimension should weigh more than
> 50% of the total weights (Munda, 2005b)."

Läs den med sammanhanget. Passagen står i kapitlet om icke-kompenserande
flerkriteriemetoder och Condorcet-liknande rangordning. Handboken ställer inte upp
samma regel för linjär aggregering. Röstas A ligger på 40 procent och bryter inte
mot regeln. Om A, B och C betraktas som en dimension, avsikt, hamnar den på 90
procent. Om regeln ska tillämpas på Rösta beror alltså på om A, B och C räknas som
en dimension eller tre. Jag hittade ingen källa som avgör den frågan.

---

## 2. Delfråga 2: valkompassforskningen om sagt mot uppmätt

Kort svar: valkompasser mäter nästan uteslutande vad partier **säger**. Uppmätt
utfall väger inte lågt i dem. Det ingår inte alls.

### 2.1 Den tydligaste utsagan

Wagner och Ruusuvirta, "Matching voters to parties: Voting advice applications and
models of party choice", *Acta Politica* 47(4), 2012, s. 400-422. Jag nådde bara
den ordagranna sammanfattningen i LSE:s arkiv. Full text ligger bakom betalvägg.
Sammanfattningen säger:

> "The voting advice given to users is also inherently limited: VAAs mostly
> disregard accountability, salience, competence and non-policy factors; they treat
> policy positions and not outcomes as paramount; and they can be subject to
> strategic manipulation by political parties."

Studien jämförde partipositioner ur 13 valkompasser i sju länder mot expertsurveyer
och partiprogramskodning. Enligt sammanfattningen visade positionerna

> "strong convergent validity with left-right and economic positions, but compare
> less favourably with immigration and environment measures."

**Detta är litteraturens direkta svar på delfråga 2.** Valkompasser hanterar inte
skillnaden mellan sagt och uppmätt. De bortser från den. Att detta pekas ut som en
brist i en granskad artikel är i sig relevant för #8.

### 2.2 Den iterativa metoden: kalibrering mot dokument, inte mot utfall

Det närmaste fältet kommer en kontroll av partiernas egna uppgifter är den
iterativa metoden. Kieskompas i Nederländerna införde den. EU Profiler och euandi
använder den.

Primärkälla: Michel, Cicchi, Garzia och Ferreira Da Silva, *euandi2019: Project
description and datasets documentation*, RSCAS Working Paper 2019/61, European
University Institute. Läst i full text.

Metoden beskrivs så (s. 6):

> "expert coding and party self-placement of positions take place independently.
> Both experts and parties are required to justify their placement with supporting
> evidence. The respective results are compared, in order to introduce a control
> mechanism. When country experts and the parties themselves disagree on where to
> place precisely a party on an issue, they interact in a so-called 'calibration
> phase', which usually results in an agreement"

Beviskravet på experterna är hårt reglerat (s. 6):

> "Experts had to support their party placement with reliable documentation. The
> sources provided by country experts followed a hierarchical order of preference
> to insure accuracy and reliability: (1) EU Election Manifesto 2019 of national
> party; (2) Party Election Platform; (3) Current/latest national election
> manifesto; (4) EU Election Manifesto of Europarties; (5) Other programmatic and
> official party documentation; (6) Interviews, press releases and social media
> communication by party leader and leading candidates; (7) Older Election
> Manifestos; (8) Other sources."

**Läs listan noga.** Alla åtta nivåer är partidokument eller partiuttalanden. Inga
voteringar. Inga regeringsbeslut. Ingen officiell statistik. Kontrollen i den
iterativa metoden gäller om partiet har skrivit det, inte om partiet har gjort det.

Sista ledet i beslutskedjan (s. 6-7):

> "While the parties themselves were consulted, the final decision on positions
> always lay with the country team, offering the tool a complete impartiality and
> independence."

Samma dokument redovisar varför fältet inte litar på de äldre metoderna (s. 5-6).
Om expertsurveyer:

> "experts position parties in expert survey based on knowledge in the field, but
> they are usually not required to justify their decisions, nor to provide any
> evidence for their choices."

Om partiprogramskodning i Comparative Manifesto Project:

> "It relies on the assumption that position can be inferred through saliency; in
> short, the more a party devotes sections of its manifesto to an issue, the more it
> is considered to support it. Consequently, two parties placing a similar emphasis
> on a given issue are assigned the same positions"

### 2.3 Svenska valkompasser

Två svenska valkompasser med publicerad metodbeskrivning, båda kontrollerade i
original.

**SVT.** Partierna svarar själva. SVT granskar svaren. Metodsidan beskriver
granskningen så, och texten jämför med valen 2010 och 2014:

> "I fallet med riksdagspartierna har dock alla svar denna gång granskats noga av
> våra politiska experter. Detta på grund av att det inte är helt ovanligt att
> partierna av strategiska skäl ibland väljer ett annat svarsalternativ än det som
> motsvarar den politik de faktiskt driver eller har drivit historiskt. I några
> enstaka fall har vi när vi upptäckt detta fört en diskussion med partiet om hur de
> tänker i denna fråga och ifrågasätt deras svar. Vi har då gemensamt kunnat
> diskutera oss fram till ett mer rimligt svar baserat på deras faktiska politik.
> Men överlag så har partiernas svar väl motsvarat den politik som vi tycker att de
> driver i praktiken. Men på lokal nivå har det varit omöjligt att göra denna
> granskning så där är svaren som visas i kompassen alltid de som de lokala
> partierna skickat till oss."

Detta är den enda källa jag hittade där en svensk valkompass säger rakt ut att ett
partis uppgivna ståndpunkt ibland avviker från den politik partiet driver.
Rättelsen sker genom samtal med partiet. Den sker inte mot voteringsdata eller mot
statistik.

SVT anger också ett samarbete kring frågeurval och insamling:

> "Förutom SVT:s egna politiska experter och erfarna valkompasskonstruktörer har vi
> samarbetat med Indikator Opinion både vad gäller frågeurvalet samt insamlingen av
> data från partier och kandidater."

Ingen av SVT:s metodsidor nämner voteringar, regeringsbeslut eller uppmätt
statistik som underlag för partiernas positioner.

**SOM-institutet vid Göteborgs universitet, valkompassen 2026:**

> "En expertgrupp vid SOM-institutet, ledd av Patrik Öhberg, docent i
> statsvetenskap, har ansvarat för att ta fram underlaget till kompassen."

> "Det handlar om att välja ut frågor utifrån var det finns skiljelinjer mellan
> partierna samt att med hjälp av partiprogram och i dialog med partiföreträdare
> fastställa partiernas positioner."

Två källor: partiprogram och dialog med partiföreträdare. Inget uppmätt utfall.

**Jag hittade ingen svensk valkompass som väger in uppmätt utfall.** Jag hittade
heller ingen svensk granskad studie som prövar frågan. Det är en lucka i
underlaget, inte ett svar.

### 2.4 Vad partipositionsforskningen mäter

Manifesto Project (MRG/CMP/MARPOR) är den största datakällan för partipositioner.
Projektets egen kodningshandbok, *Manifesto Coding Instructions* (5:e reviderade
upplagan, maj 2021), läst i full text, definierar underlaget (s. 2):

> "Manifestos are understood to be parties only and presidential candidates' main
> authoritative policy statements and therefore serve as indicators of the parties'
> policy preferences at a given point in time."

Ordet är "preferences". Manifestdata är ett avsiktsmått i sin egen definition. Det
gäller även Chapel Hill Expert Survey, där experter placerar partier efter deras
positioner.

**Kärnan i "avsikt mot utfall" ligger alltså inte i partipositionsforskningen.**
Den forskningen mäter avsikt hela vägen. Den frågar inte vad som blev uppmätt.

### 2.5 Beteendedata har sin egen skevhet

Det finns en frestelse att kalla voteringsdata objektiv. Litteraturen om
voteringsanalys säger emot.

Ainsley, Carrubba, Crisp, Demirkaya, Gabel och Hadzic, "Roll-Call Vote Selection:
Implications for the Study of Legislative Politics", *American Political Science
Review* 114(3), 2020, s. 691-706. Läst i utdrag via förlagets öppna läsversion.

Registrerade omröstningar är ett urval, inte hela populationen av beslut. Urvalet
är inte slumpmässigt, eftersom partiledningar begär omröstning strategiskt:

> "Cohesion scores based on RCV samples will not replicate ones based on unobserved
> votes (and the differences will both be large and in an unpredictable direction)."

**Vad det betyder för #8:** Röstas A-del bygger på riksdagsdata. Den delen är inte
automatiskt mer objektiv än B eller C bara för att den är beteendedata. Den bär
sin egen urvalsskevhet. Jag har inte prövat hur stor den skevheten är i svensk
riksdagsdata. Det ligger utanför den här biljetten.

### 2.6 Håller partier vad de lovar?

Frågan "vad ett parti säger mot vad som faktiskt hände" har en egen litteratur:
vallöftesforskningen. Den är relevant eftersom den mäter hur bra avsikt förutsäger
handling.

Thomson, Royed, Naurin med flera, "The Fulfillment of Parties' Election Pledges: A
Comparative Study on the Impact of Power Sharing", *American Journal of Political
Science* 61(3), 2017, s. 527-542. Läst i full text via författarnas godkända
manusversion.

Huvudresultatet (manus s. 20):

> "The first main finding is that governing parties fulfilled a clear majority of
> pledges at least partially: 59 percent (5,044 of the 8,547 pledges were fulfilled
> at least partially)."

Svenska siffror i samma stycke (manus s. 20):

> "The single-party minority governments in Sweden also fulfilled a remarkably high
> percentage of their constituent parties' pledges at least partially: 87 percent
> (112 of 129 pledges), while the Swedish majority coalition fulfilled a lower
> percentage of its pledges: 68 percent (92 of 135 pledges)."

Och sammanfattningens slutsats:

> "We find high levels of pledge fulfillment for most parties that enter the
> government executive, and substantially lower levels for parties that do not. The
> findings challenge the common view of parties as promise breakers."

**Vad det betyder för #8:** avsiktsmått är inte tomma. För svenska regeringspartier
i studien följdes en stor majoritet av löftena av handling. Studien mäter dock
löfte mot åtgärd, inte löfte mot uppmätt samhällsutfall. Steget från åtgärd till
utfall ligger utanför den studien.

En näraliggande fråga är om partier ljuger i valkompassen. Ilmarinen, Isotalo,
Lönnqvist och von Schoultz, "Do politicians' answers to voting advice applications
reflect their sincere beliefs?", *Electoral Studies* 79, 2022, artikel 102504,
jämförde finländska kandidaters offentliga valkompassvar med konfidentiella svar
efter valet. Enligt sammanfattningen var svaren mycket lika, vilket talar för att
de offentliga svaren är uppriktiga. **Jag nådde bara sammanfattningen.** Full text
låg bakom betalvägg och 403-svar. Resultatet gäller kandidater i ett
personvalssystem, inte partier i Sverige.

---

## 3. Delfråga 3: stöd för eller emot låg vikt på uppmätt utfall vid svag attribution

Här är läget blandat. Jag redovisar båda riktningarna.

### 3.1 Stöd för lägre vikt: precisionsviktning

Den starkaste metodstöd jag hittade för att väga ned ett brusigt mått är
precisionsviktning. Den finns i OECD-handbokens egen verktygslåda och i ett stort
etablerat index.

OECD-handboken, avsnitt 6.4 om unobserved components model (s. 94-95). Vikten är

> "a decreasing function of the variance of indicator q"

Handboken beskriver vad felet i modellen fångar (s. 95):

> "The error term captures two sources of uncertainty. First, the phenomenon can be
> only imperfectly measured or observed in each country (e.g. errors of
> measurement). Second, the relationship between ph(c) and I(c,q) may be imperfect"

Den andra felkällan är svag koppling mellan det man vill mäta och det man mäter.
Attributionsproblemet i Röstas D hör hemma där.

Samma logik står i tabellen över metodernas för- och nackdelar (s. 101). Om UCM:

> "Rewards the absence of outliers, given that weights are a decreasing function of
> the variance of individual indicators."

Det största produktionsindex som gör så är Världsbankens styrningsindikatorer.
Kaufmann, Kraay och Mastruzzi, *The Worldwide Governance Indicators: Methodology
and Analytical Issues*, World Bank Policy Research Working Paper 5430, 2010. Läst i
full text. På s. 10-11:

> "The weights assigned to each source ... are larger the smaller the variance of
> the error term of the source. In other words, sources that provide a more
> informative signal of governance receive higher weight."

Författarna dämpar dock sin egen poäng (s. 16):

> "However, we do not want to overstate the importance of this benefit. We have
> found that precision-weighting reduces the margins of error of our aggregate
> indicators by only about 20 percent relative to unweighted averages. Similarly, we
> find that the choice of weighting scheme has for the most part rather small
> effects on the ranking of countries."

**Räckvidd och gräns.** Detta är stöd för principen "mindre informativ källa får
lägre vikt". Det är inte stöd för någon bestämd siffra. Metoden är dessutom
datadriven: variansen skattas ur data, den sätts inte av byggaren. Röstas D-vikt
är satt, inte skattad. Att åberopa UCM som stöd för en satt siffra vore att låna
auktoritet metoden inte ger.

### 3.2 Emot lägre vikt: handbokens regel om matchning

Se avsnitt 1.6. Om Rösta säger sig mäta utfört resultat, säger handboken att
utfallsmått ska bära indexet. Om Rösta säger sig mäta riktning och avsikt, faller
den invändningen.

Detta är den enda passagen i handboken som direkt behandlar blandningen av
avsiktsmått och utfallsmått. Den formulerar ett villkor, inte en vikt.

### 3.3 Ett etablerat index som gör tvärtom, och motiverar det med eftersläpning

Climate Change Performance Index (CCPI), utgiven av Germanwatch, NewClimate
Institute och Climate Action Network. Metodsidan på ccpi.org, läst i original.

Viktningen:

> "The 'GHG Emissions' category has the highest weight of 40% in a country's
> overall score, as these emissions ultimately affect the climate."

Övriga kategorier: Renewable Energy 20 procent, Energy Use 20 procent, Climate
Policy 20 procent.

Motiveringen till att politik alls får en egen kategori är intressant, för den är
exakt Röstas eftersläpningsargument, fast använt åt andra hållet:

> "The 'Climate Policy' category, weighting 20%, considers the fact that measures
> taken by governments to reduce greenhouse gases often take several years to show
> their effect."

Andelen kvantitativa data:

> "Around 80% of the assessment of a country's performance is based on quantitative
> data from the International Energy Agency (IEA), PRIMAP, the Food and Agriculture
> Organization (FAO), and the national GHG inventories submitted to the UNFCCC."

Climate Policy bedöms av experter via enkät. Det är ett avsiktsmått.

**En viktig nyansering.** Uppdelningen är inte rent 80 mot 20. CCPI skriver:

> "The three quantitative categories GHG Emissions, Renewable Energy, and Energy
> Use are each defined by four indicators: Current Level, Past Trend, Well-Below-2°C
> Compatibility of the Current Level, and Well-Below-2°C Compatibility of the
> Countries' 2030 Target."

En av fyra indikatorer i varje kvantitativ kategori mäter alltså landets **mål för
2030**. Ett mål är en avsikt, inte ett utfall. Andelen ren avsikt i CCPI ligger
därför över 20 procent.

**Vad det betyder för #8:** här finns ett etablerat sammanvägt index som väger
avsikt mot uppmätt utfall, och som landar ungefär omvänt mot Rösta. CCPI:s uttalade
skäl för att ge politiken egen plats är just att utfallet släpar efter. Rösta
använder samma eftersläpning som skäl att väga ned utfallet. Skälet är detsamma.
Slutsatsen är den motsatta. CCPI publicerar inte någon härledning av varför just
20 procent, lika lite som Rösta härleder sina 10.

### 3.4 Attribution och ansvarsutkrävande

**Läs först avgränsningen.** Den här litteraturen mäter om **väljare** klarar att
peka ut vem som bär ansvaret. Den mäter inte om utfallet faktiskt går att härleda
till ett parti. Det är två skilda frågor. Rösta ställer den andra. Litteraturen
svarar mest på den första. Det begränsar hur mycket den kan bära i #8.

#### Regeringens sammanhållning avgör. Flernivåstyret gör det inte.

Hobolt, Tilley och Banducci, "Clarity of responsibility: How government cohesion
conditions performance voting", *European Journal of Political Research* 52(2),
2013, s. 164-187. Läst i full text i förlagets satta version.

Studien delar begreppet i två. Institutionell tydlighet fångar formell
maktdelning, både horisontellt och vertikalt mellan nivåer. Regeringstydlighet
fångar hur sammanhållen den sittande regeringen är. Den vertikala mekanismen
beskrivs så (s. 169):

> "when institutional rules shift power either horizontally between the executive
> and the legislature ... or vertically between different levels of government (as
> in federal systems), it is difficult for voters to assign responsibility for
> policy outcomes because power is dispersed across many political actors"

Det är hypotesen. Resultatet gick åt andra hållet (s. 177):

> "So, overall there appears very weak support for H1 and very strong support for
> H2: the type of clarity of responsibility matters a lot and it is government
> cohesion that matters."

Slutsatsen (s. 180):

> "This suggests that as long as voters face a cohesive incumbent (e.g., a
> single-party government or an ideologically cohesive coalition dominated by one
> large party), they will be able to reward or punish the party in power,
> regardless of whether institutional power is shared with the opposition in
> legislative committees or in upper chambers or in lower levels of government."

Och en observation som rör Röstas välfärdskategori direkt (s. 180):

> "we did not find that this effect was greater for healthcare than the economy,
> even though governments generally have more autonomous control over healthcare
> than the economy."

**Vad det betyder för #8.** Röstas motivering till låg D-vikt räknar upp fyra skäl:
eftersläpning, konjunktur, regionalt ansvar och koalitioner. Hobolt med flera
stöder koalitionsskälet starkt. De ger svagt stöd åt det regionala skälet, i alla
fall på väljarsidan. De prövar inte eftersläpning eller konjunktur.

Studien citerar också Powell och Whitten 1993, som är ursprungskällan till hela
begreppet. **Jag nådde inte den artikeln i original.** Den ligger bakom JSTOR och
förlaget har utelämnat sammanfattningen. Jag citerar den därför bara som den
återges i Hobolt med flera, s. 166:

> "The greater the perceived unified control of policymaking by the incumbent, the
> more likely is the citizen to assign responsibility for economic and policy
> outcomes to the incumbents" (Powell och Whitten 1993: 398)

#### Flernivåstyre: strandet är omtvistat

Två källor pekar åt olika håll. Jag nådde bara deras ordagranna sammanfattningar
via förlagens deponerade metadata. Full text låg bakom betalvägg i båda fallen.

Anderson, "Economic Voting and Multilevel Governance: A Comparative
Individual-Level Analysis", *American Journal of Political Science* 50(2), 2006,
s. 449-463:

> "Results demonstrate that economic voting is weakest in countries where
> multilevel governance is most prominent."

León, "Who is responsible for what? Clarity of responsibilities in multilevel
states: The case of Spain", *European Journal of Political Research* 50(1), 2011,
s. 80-109:

> "Results show that the relationship between decentralisation and clarity of
> responsibility has a u-shape. Responsibility attribution is clearer in regions
> with high and low levels of decentralisation, where one level of government
> clearly predominates over the other, than in regions with a more intertwined
> distribution of powers."

**Vad det betyder för #8.** Antagandet "regionalt ansvar gör attributionen svag" är
inte en etablerad sanning i litteraturen. Anderson stöder det. Hobolt med flera
gör det inte. León säger att sambandet inte är rakt: attributionen är tydlig när
en nivå dominerar och grumlig bara i det blandade mellanläget. Röstas C3-spår
delar ut regionala vårdutfall till regionstyrande parti. León pekar mot att den
frågan måste avgöras per region, inte per princip.

#### Konjunktur och chocker utanför kontroll

Här är stödet starkare, och det pekar mot ett svar som varken är hög eller låg vikt.

Wolfers, *Are Voters Rational? Evidence from Gubernatorial Elections*,
arbetspapper, Wharton School, University of Pennsylvania, utkast 30 januari 2007.
Läst i full text. Normen han utgår från (avsnitt I):

> "If voters efficiently process this information they will reward good economic
> outcomes that reflect the governor's actions, but filter from their assessment
> economic events that reflect influences outside the politician's locus of
> control."

Hans resultat: väljarna gör inte det. Guvernörer i oljestater omväljs när oljepriset
stiger. Slutsatsen (sammanfattningen):

> "this suggests that voters make systematic attribution errors and are best
> characterized as quasi-rational."

**Lägg märke till riktningen.** Wolfers norm är att **filtrera bort** den del av
utfallet som ligger utanför kontrollen. Den är inte att väga ned hela utfallsmåttet.

Achen och Bartels, "Blind Retrospection: Electoral Responses to Drought, Flu, and
Shark Attacks", arbetspapper 2004/199, Juan March-institutet, senare kapitel 5 i
*Democracy for Realists* (2016). Läst i full text. Deras poäng är att väljare
straffar regeringar för torka, översvämningar och hajattacker.

Kayser och Peress ger den konstruktiva versionen. "Benchmarking across Borders:
Electoral Accountability and the Necessity of Comparison", *American Political
Science Review* 106(3), 2012, s. 661-684. **Endast sammanfattningen.**

> "We decompose two key economic aggregates - growth in real gross domestic product
> and unemployment - into their international and domestic components and
> demonstrate that voters hold incumbents more electorally accountable for the
> domestic than for the international component of growth."

**Vad det betyder för #8.** Svaret på konjunkturinvändningen i den här litteraturen
är att dela upp utfallet i en inhemsk och en internationell del, inte att väga ned
det. Rösta har redan en variant av tanken i IDEA.md: "Ett parti ska inte få hela
äran eller skulden för konjunkturen."

#### Eftersläpning

Healy och Lenz, "Substituting the End for the Whole: Why Voters Respond Primarily
to the Election-Year Economy", *American Journal of Political Science* 58(1), 2014,
s. 31-47. Läst i full text, men i författarnas arbetspappersversion daterad
2012-09-15. Sidnumren i den versionen stämmer inte med den publicerade.

Deras resultat (sammanfattningen i arbetspapperet, s. 1):

> "Voters, we find, actually intend to judge presidents on cumulative growth.
> However, since that characteristic is not readily available to them, voters
> inadvertently substitute election-year performance because it is more easily
> accessible."

**Vad det betyder för #8.** Detta är inte stöd för att eftersläpning gör utfallsdata
oanvändbar. Det är motsatsen. Väljarna vill ha hela mandatperiodens utfall och får
det inte. Åtgärden i studien är att tillhandahålla det ackumulerade utfallet. Det
är precis vad ett mätverktyg kan göra.

### 3.5 Vad andra fält gör när attributionen är svag

Två fält har brottats med exakt samma problem. Båda landar i samma svar: justera
måttet, redovisa osäkerheten, tona ned tolkningen. Inget av dem föreslår låg vikt.

**Program- och verksamhetsutvärdering.** Mayne, "Addressing Attribution through
Contribution Analysis: Using Performance Measures Sensibly", *Canadian Journal of
Program Evaluation* 16(1), 2001, s. 1-24. Öppen tillgång. Läst i full text.

Problemet (s. 3):

> "Despite the measurement difficulty, attribution is a problem that cannot be
> ignored when trying to assess the performance of government programs. Without an
> answer to this question, little can be said about the worth of the program"

Vad som görs fel (s. 7):

> "Too often, the measuring and particularly the reporting of performance through
> performance measurement systems completely ignores the attribution problem. The
> performance measured is either directly attributed to the program or attributed by
> implication, through the lack of any discussion or analysis of other factors at
> play."

Vad som ska göras i stället (s. 8):

> "Thus, there is a need to acknowledge that there are other factors at play in
> addition to the program and that it is therefore usually not immediately clear
> what effect the program has had or is having in producing the outcome in
> question. ... For reporting, acknowledging the other factors at play is more
> honest and hence more credible than pretending they do not exist."

Mayne kallar metoden contribution analysis. Den bygger en redovisad orsakskedja
och prövar den mot alternativa förklaringar. Den sätter ingen vikt.

**Skolredovisning.** Här är parallellen skarpast. En skolas resultat påverkas av
elevernas förkunskaper, av bakgrund och av faktorer utanför skolans kontroll. Det
är samma attributionsproblem som Röstas D.

Leckie och Prior, "A Comparison of Value-Added Models for School Accountability",
arXiv 2107.09410. Läst i full text i den öppna versionen. Om det ojusterade måttet:

> "Raw models should not be used to measure school effectiveness as by ignoring
> initial student achievement they fail to separate the value that schools add to
> student learning from pre-existing differences in learning across schools at the
> start of the phase of schooling."

Och i slutsatsen:

> "we agree with the wide held view that the Raw model is inadequate for school
> accountability purposes as it makes no adjustment for initial school differences
> in student achievement"

Fältets svar på svag attribution är alltså att justera bort det som ligger utanför
skolans kontroll. Fältet varnar samtidigt för att justera för mycket:

> "for the purpose of identifying schools which are struggling to boost student
> learning, such adjustments have been argued as overadjustments. For example,
> adjusting for regional differences in student performance will lead the resulting
> school effects to be deviations from regional averages rather than the overall
> average, potentially masking which schools are underperforming nationally"

**Vad det betyder för #8.** Två etablerade fält som mäter prestation under svag
attribution väljer justering, inte nedviktning. Båda varnar också för att justera
för mycket. Ingen av dem prövar nedviktning som alternativ. Det är därför inte
belägg mot nedviktning. Det är frånvaro av belägg för den.

### 3.6 Vad jag inte hittade

Detta är den viktigaste raden i avsnittet.

**Jag hittade ingen metodkälla som säger att ett utfallsmått ska väga lågt när
attributionen är svag.** Inte i OECD- och JRC-handboken. Inte i JRC:s nyare
arbeten om vikter. Inte i valkompasslitteraturen. Inte i litteraturen om
ansvarsutkrävande. Inte i utvärderingslitteraturen.

Det närmaste litteraturen kommer är fyra saker, och ingen av dem är regeln:

1. Precisionsviktning ger lägre vikt åt en källa med större felvarians (avsnitt 3.1).
   Det är en **datadriven skattning**, inte en satt siffra.
2. Handboken varnar för att vikta efter datakvalitet, eftersom det gynnar det som
   råkar vara lättmätt (s. 32).
3. Handboken kräver att måttypen matchar indexets syfte (s. 22-23). Det är ett
   villkor för urvalet, inte en viktregel.
4. Utvärderings- och skolfälten svarar på svag attribution med justering och
   redovisad osäkerhet (avsnitt 3.5).

Det motsatta hittade jag heller inte. **Ingen källa säger att uppmätt utfall måste
väga tungt oavsett attribution.** CCPI väger utfall tungt, men CCPI härleder inte
sina vikter.

En besläktad utsaga finns hos Royal Statistical Societys arbetsgrupp om
prestationsindikatorer. Bird, Cox, Farewell, Goldstein, Holt och Smith,
"Performance Indicators: Good, Bad, and Ugly", *Journal of the Royal Statistical
Society Series A* 168(1), 2005, s. 1-27. **Endast den deponerade sammanfattningen.**
Full text nåddes inte.

> "Procedures for data collection, analysis, presentation of uncertainty and
> adjustment for context, together with dissemination rules, should be explicitly
> defined and reflect good statistical practice. Because of their usually tentative
> nature, PIs should be seen as 'screening devices' and not overinterpreted."

Även här: justering för sammanhang och redovisad osäkerhet, inte låg vikt.

Litteraturen ger alltså inget färdigt svar på delfråga 3. Den ger fyra saker som
går att stödja sig på: kravet på matchning mot syftet, principen att mindre
informativa källor får mindre vikt, det etablerade svaret att justera i stället för
att väga ned, och kravet att mäta och redovisa hur mycket viktvalet flyttar
rankingen.

---

## 4. Sammanfattning per delfråga

**Delfråga 1, OECD och JRC.** Vikter är värderingar. Handboken kräver koppling till
den teoretiska ramen, dokumentation, och känslighetsanalys. Den rekommenderar inte
lika vikter och säger inte när de är att föredra. Den varnar för att lika vikter kan
dölja att underlag saknas. Den understryker att vikter i en linjär summa är
utbytesförhållanden, inte betydelsegrader. JRC:s nyare arbeten visar att nominell
vikt sällan motsvarar faktisk påverkan på rankingen. Stödet för lika vikter kommer
från beslutslitteraturen (Dawes 1979), inte från handboken.

**Delfråga 2, valkompasser.** De hanterar inte skillnaden mellan sagt och uppmätt.
De bortser från den. Wagner och Ruusuvirta pekar ut detta som en inbyggd
begränsning. Den mest utvecklade kvalitetsmetoden i fältet, den iterativa metoden i
euandi och Kieskompas, kontrollerar partiernas självplacering mot en åttagradig
dokumenthierarki som helt saknar beteende- och utfallsdata. Svenska valkompasser
hos SVT och SOM-institutet bygger på partiprogram och dialog med partiföreträdare.
SVT skriver samtidigt att partier ibland av strategiska skäl svarar något annat än
den politik de faktiskt driver, och att SVT rättar det genom samtal med partiet.
Vallöftesforskningen visar samtidigt att avsiktsmått bär information: svenska
enpartiminoritetsregeringar infriade 87 procent av löftena åtminstone delvis.

**Delfråga 3, låg vikt vid svag attribution.** Inget direkt stöd, och inget direkt
motstöd. Precisionsviktning stöder principen, men bara som datadriven skattning.
Handbokens matchningsregel gör frågan beroende av vad Rösta påstår sig mäta. CCPI
är ett etablerat index som använder samma eftersläpningsargument och landar
tvärtom, med ungefär 80 procent utfall.

Attributionslitteraturen stöder **premissen** men inte **åtgärden**. Den stöder
starkt att koalitioner grumlar ansvaret, och att utfall innehåller delar utanför
en regerings kontroll. Den ger svagt och omtvistat stöd åt att regional
ansvarsfördelning gör det, och den ger inget stöd alls åt eftersläpning som skäl
att väga ned utfall. Där litteraturen föreskriver en åtgärd är åtgärden att dela
upp måttet, jämföra mot ett riktmärke, justera för sammanhanget och redovisa
osäkerheten. Inte att sätta en låg vikt.

En sista påminnelse om räckvidd: den här litteraturen mäter främst om väljare
klarar att peka ut ansvarig. Den mäter inte om utfallet faktiskt går att härleda
till ett parti.

---

## 5. Källförteckning

Metodlitteratur. Ingen av källorna nedan är en datakälla för Rösta.

### Sammanvägda index

1. OECD och Joint Research Centre (2008). *Handbook on Constructing Composite
   Indicators: Methodology and User Guide*. OECD Publishing. ISBN 978-92-64-04345-9.
   **Full text.**
   https://www.oecd.org/content/dam/oecd/en/publications/reports/2008/08/handbook-on-constructing-composite-indicators-methodology-and-user-guide_g1gh9301/9789264043466-en.pdf

2. Paruolo, P., Saisana, M. och Saltelli, A. (2013). "Ratings and rankings: voodoo
   or science?" *Journal of the Royal Statistical Society: Series A* 176(3), 609-634.
   DOI 10.1111/j.1467-985X.2012.01059.x. **Full text** via författarens öppna kopia.
   https://www.andreasaltelli.eu/file/repository/rssa_1059.pdf

3. Becker, W., Saisana, M., Paruolo, P. och Vandecasteele, I. (2017). "Weights and
   importance in composite indicators: Closing the gap." *Ecological Indicators* 80,
   12-22. **Utdrag** via öppen version.
   https://pmc.ncbi.nlm.nih.gov/articles/PMC5473177/

4. Kaufmann, D., Kraay, A. och Mastruzzi, M. (2010). *The Worldwide Governance
   Indicators: Methodology and Analytical Issues*. World Bank Policy Research
   Working Paper 5430. **Full text.**
   https://documents1.worldbank.org/curated/en/630421468336563314/pdf/WPS5430.pdf

5. Dawes, R. M. (1979). "The Robust Beauty of Improper Linear Models in Decision
   Making." *American Psychologist* 34(7), 571-582. DOI 10.1037/0003-066X.34.7.571.
   **Full text.**
   https://www.cmu.edu/dietrich/sds/docs/dawes/the-robust-beauty-of-improper-linear-models-in-decision-making.pdf

6. Germanwatch, NewClimate Institute och Climate Action Network. *Climate Change
   Performance Index: Methodology*. **Full text av metodsidan.**
   https://ccpi.org/methodology/

### Valkompasser och partipositioner

7. Wagner, M. och Ruusuvirta, O. (2012). "Matching voters to parties: Voting advice
   applications and models of party choice." *Acta Politica* 47(4), 400-422.
   DOI 10.1057/ap.2011.29. **Endast sammanfattning**, ordagrant ur LSE Research
   Online. Full text bakom betalvägg.
   https://researchonline.lse.ac.uk/id/eprint/46760/

8. Michel, E., Cicchi, L., Garzia, D. och Ferreira Da Silva, F. (2019).
   *euandi2019: Project description and datasets documentation*. RSCAS Working Paper
   2019/61, European University Institute. **Full text.**
   https://cadmus.eui.eu/server/api/core/bitstreams/3465dac5-b0b8-568d-8d72-e445f3f3e011/content

9. Werner, A., Lacewell, O., Volkens, A., Matthieß, T., Zehnter, L. och van Rinsum,
   L. (2021). *Manifesto Project Dataset: Manifesto Coding Instructions* (5:e
   reviderade upplagan). WZB. **Full text.**
   https://manifestoproject.wzb.eu/down/papers/handbook_2021_version_5.pdf

10. Ainsley, C., Carrubba, C. J., Crisp, B. F., Demirkaya, B., Gabel, M. J. och
    Hadzic, D. (2020). "Roll-Call Vote Selection: Implications for the Study of
    Legislative Politics." *American Political Science Review* 114(3), 691-706.
    **Utdrag** via förlagets öppna läsversion.
    https://www.cambridge.org/core/journals/american-political-science-review/article/rollcall-vote-selection-implications-for-the-study-of-legislative-politics/FFAD60FB9CA9BBD54F02DE44A1FF0264/core-reader

11. Thomson, R., Royed, T., Naurin, E. med flera (2017). "The Fulfillment of
    Parties' Election Pledges: A Comparative Study on the Impact of Power Sharing."
    *American Journal of Political Science* 61(3), 527-542. DOI 10.1111/ajps.12313.
    **Full text** via godkänd manusversion i Strathprints.
    https://strathprints.strath.ac.uk/59403/1/Thomson_etal_AJPS_2016_The_fulfillment_of_parties_election_pledges.pdf

12. Ilmarinen, V.-J., Isotalo, V., Lönnqvist, J.-E. och von Schoultz, Å. (2022).
    "Do politicians' answers to voting advice applications reflect their sincere
    beliefs?" *Electoral Studies* 79, 102504. **Endast sammanfattning.** Full text
    otillgänglig (403 och betalvägg).
    https://www.sciencedirect.com/science/article/pii/S0261379422000622

### Svenska valkompasser

13. SVT Nyheter. "Frågor och svar om SVT:s valkompasser." **Full text.**
    https://www.svt.se/nyheter/inrikes/fragor-och-svar-om-svts-valkompasser

14. SVT Nyheter. "Så tog vi fram kompassfrågorna och så beräknas matchningen mot
    partier och kandidater." **Full text.**
    https://www.svt.se/nyheter/inrikes/sa-tog-vi-fram-kompassfragorna-och-sa-beraknas-matchningen-mot-partier-och-kandidater

15. Göteborgs universitet. "Gör valkompassen 2026!" **Full text.**
    https://www.gu.se/nyheter/gor-valkompassen-2026

### Attribution, ansvarsutkrävande och prestationsmätning

16. Hobolt, S. B., Tilley, J. och Banducci, S. (2013). "Clarity of responsibility:
    How government cohesion conditions performance voting." *European Journal of
    Political Research* 52(2), 164-187. DOI 10.1111/j.1475-6765.2012.02072.x.
    **Full text** via författarens kopia av förlagets satta version.
    https://personal.lse.ac.uk/hobolt/Publications/EJPR_CoR.pdf

17. Powell, G. B. och Whitten, G. D. (1993). "A Cross-National Analysis of Economic
    Voting: Taking Account of the Political Context." *American Journal of Political
    Science* 37(2), 391-414. DOI 10.2307/2111378. **Ej nådd.** Bakom JSTOR.
    Förlaget har utelämnat sammanfattningen. Citeras enbart via Hobolt m.fl. 2013.

18. Anderson, C. D. (2006). "Economic Voting and Multilevel Governance: A
    Comparative Individual-Level Analysis." *American Journal of Political Science*
    50(2), 449-463. DOI 10.1111/j.1540-5907.2006.00194.x. **Endast sammanfattning**
    via förlagets deponerade metadata.
    https://api.openalex.org/works/doi:10.1111/j.1540-5907.2006.00194.x

19. León, S. (2011). "Who is responsible for what? Clarity of responsibilities in
    multilevel states: The case of Spain." *European Journal of Political Research*
    50(1), 80-109. DOI 10.1111/j.1475-6765.2010.01921.x. **Endast sammanfattning.**
    https://api.openalex.org/works/doi:10.1111/j.1475-6765.2010.01921.x

20. Wolfers, J. (2007). *Are Voters Rational? Evidence from Gubernatorial
    Elections*. Arbetspapper, The Wharton School, University of Pennsylvania. Utkast
    2007-01-30. **Full text.**
    http://users.nber.org/~jwolfers/Papers/Voterrationality(latest).pdf

21. Achen, C. H. och Bartels, L. M. (2004). *Blind Retrospection: Electoral
    Responses to Drought, Flu, and Shark Attacks*. Estudio/Working Paper 2004/199,
    Juan March-institutet. **Full text.**
    https://ethz.ch/content/dam/ethz/special-interest/gess/cis/international-relations-dam/Teaching/pwgrundlagenopenaccess/Weitere/AchenBartels.pdf

22. Kayser, M. A. och Peress, M. (2012). "Benchmarking across Borders: Electoral
    Accountability and the Necessity of Comparison." *American Political Science
    Review* 106(3), 661-684. DOI 10.1017/S0003055412000275. **Endast sammanfattning.**
    https://api.openalex.org/works/doi:10.1017/s0003055412000275

23. Healy, A. och Lenz, G. S. (2014). "Substituting the End for the Whole: Why
    Voters Respond Primarily to the Election-Year Economy." *American Journal of
    Political Science* 58(1), 31-47. DOI 10.1111/ajps.12053. **Full text av
    arbetspappersversionen** daterad 2012-09-15. Sidnumren i den versionen skiljer
    sig från den publicerade. https://digitalcommons.lmu.edu/econ_fac/15/

24. Mayne, J. (2001). "Addressing Attribution through Contribution Analysis: Using
    Performance Measures Sensibly." *Canadian Journal of Program Evaluation* 16(1),
    1-24. DOI 10.3138/cjpe.016.001. Öppen tillgång. **Full text.**
    https://ces.journals.uvic.ca/index.php/cjpe/article/view/1110

25. Leckie, G. och Prior, L. *A Comparison of Value-Added Models for School
    Accountability*. arXiv 2107.09410 [stat.AP]. **Full text.**
    https://arxiv.org/abs/2107.09410

26. Bird, S. M., Cox, D., Farewell, V. T., Goldstein, H., Holt, T. och Smith, P. C.
    (2005). "Performance Indicators: Good, Bad, and Ugly." *Journal of the Royal
    Statistical Society Series A* 168(1), 1-27.
    DOI 10.1111/j.1467-985X.2004.00333.x. **Endast den deponerade sammanfattningen.**
    https://api.openalex.org/works/doi:10.1111/j.1467-985x.2004.00333.x
