# Kandidater till bakåtblickande påståenden, valmanifest 2026

> Råmaterial för **Verklighetsbild**, se [#42](https://github.com/mcknschn/rosta/issues/42).
> Detta är **inte** en färdig mappning. Varje rad är en kandidat som väntar på ett avgörande
> om vad som räknas som en post. Se `Vad som återstår` nedan.

## Varför filen finns

[`mappning_bakat.md`](mappning_bakat.md) räknade 230 bakåtblickande påståenden i de åtta
manifesten. Den siffran var för låg. Sveptet bakom den letade efter dåtidsformer som
`har ökat`, `de senaste åren` och `sedan 2022`, men de flesta partier beskriver mandatperioden
i presens: `vårdköerna är fortsatt långa`, `tåg är försenade`, `arbetslösheten biter sig fast`.
Svepet var blint för hela den formen.

En andra genomgång 2026-09-13 läste om alla åtta manifest sida för sida med samma
inkluderande regel för alla. Den gav **666 kandidater** utöver de 230 redan mappade.

## Så är materialet framställt

Varje manifest extraherades till text med PyMuPDF, med sidmarkörer bevarade. Texten lästes
sedan i bitar om högst 24 sidor, nitton läsningar totalt. Regeln som gällde vid läsningen:

- **Med:** varje mening som påstår något om hur det är eller har blivit i Sverige, i presens
  eller dåtid, även när meningen bär ett värdeomdöme som `för många` eller `för dåligt`.
- **Utan:** rena förslag (`vi vill sänka skatten`) och tidlösa värdepåståenden
  (`alla människor har lika värde`).
- **Lydelsen är partiets egen.** Ingen omskrivning, ingen hopfogning av meningar som inte
  står intill varandra.

## Så är materialet kontrollerat

Varje rad slogs mot partiets egen PDF med exakt strängmatchning efter normalisering.
**657 av 666 rader står ordagrant i källdokumentet på den angivna sidan.**

De 9 undantagen är märkta i listan nedan:

- `avviker` betyder att raden inte matchar min extraktion ord för ord. Åtta sådana finns.
  **Tre är fel i min extraktion, inte i citatet.** Alla tre är M:s. M:s tvåspaltiga sidor
  flätar in punktlistor mitt i löptexten, så den linjära extraktionen kastar om orden.
  Läsningen av sidan var riktig.
  **Fem är äkta fel i citatet.** Tre fogar ihop två meningar som har en tredje mening emellan
  (`C` sidorna 78 och 91, `L` sidan 15). Två är omskrivningar i stället för citat
  (`C` sidorna 56 och 62), och den på sidan 56 är dessutom hämtad inifrån ett framåtriktat
  förslag och hör inte hemma i bakåthalvan alls.
- `sidbrott` betyder att meningen börjar på den angivna sidan och fortsätter på nästa.
  Citatet är riktigt.

## Vad som återstår

Regeln som användes är avsiktligt vid, och den drar in tre slag som troligen inte hör hemma
i ett mått som prövas mot statistik:

1. **Normativa hybrider.** `För många elever lämnar skolan utan fullständiga kunskaper`.
   Kärnan går att mäta, `för många` gör det inte.
2. **Satser som kräver sin föregångare.** `Det gör oss sårbara både ekonomiskt och
   säkerhetspolitiskt`.
3. **Regeringsgärningar formulerade som påståenden.** `Vi har gjort det straffbart att inte
   avslöja tvångsäktenskap`. Sant per definition, och därför meningslöst att kontrollera.

Triagen är inte gjord. Den hänger på punkt 2 och 3 i [#42](https://github.com/mcknschn/rosta/issues/42).

## Fördelning

| Kategori | S | M | SD | C | V | KD | MP | L | Summa |
|---|---|---|---|---|---|---|---|---|---|
| Ekonomi och jobb | 12 | 47 | 12 | 40 | 35 | 14 | 5 | 20 | **185** |
| Välfärd | 13 | 44 | 8 | 34 | 32 | 10 | 4 | 34 | **179** |
| Lag och trygghet | 4 | 32 | 7 | 23 | 0 | 1 | 2 | 8 | **77** |
| Försvar och beredskap | 8 | 16 | 1 | 6 | 0 | 0 | 3 | 1 | **35** |
| Klimat, miljö och energi | 5 | 18 | 6 | 6 | 0 | 2 | 7 | 1 | **45** |
| Integration och sammanhållning | 6 | 11 | 9 | 4 | 0 | 0 | 0 | 6 | **36** |
| Frihet, demokrati och institutioner | 4 | 5 | 10 | 14 | 0 | 4 | 2 | 12 | **51** |
| Utanför de sju kategorierna | 2 | 14 | 3 | 14 | 7 | 14 | 1 | 3 | **58** |
| **Summa** | **54** | **187** | **56** | **141** | **74** | **45** | **24** | **85** | **666** |

## Kandidaterna


### S (54)

**Ekonomi och jobb** (12)

- s4 De senaste åren har varit tuffa för hårt arbetande familjer.
- s5 De med mycket stora förmögenheter och de med högst inkomster har också fått mest.
- s5 Men dagens pensionssystem levererar inte som det var utlovat.
- s5 Men under de senaste åren har politiken varit missriktad.
- s5 Sverige är ett i grunden rikt land med stora möjligheter.
- s6 Omfattande förseningar i järnvägen är ett betydande problem för resenärerna.
- s7 Små- och medelstora företag är helt avgörande för svensk ekonomi.
- s7 Sverige är hem för ett framgångsrikt näringsliv och en stark industri.
- s7 Vi har en välutbildad arbetskraft, ett välfungerande samarbete mellan stat, näringsliv, fackföreningsrörelse och akademi och en vilja att blicka framåt mot det nya.
- s8 Inspiration finns tex i den svenska framgången med Hem-pc reformen.
- s8 När fler vill plugga vidare så har regeringen i stället minskat antalet utbildningsplatser på högskolor och universitet. Det är skadligt för Sverige.
- s9 Sverigedemokraterna och regeringen lovade att vända utvecklingen. I stället har de prioriterat skattesänkningar för de allra rikaste.

**Välfärd** (13)

- s4 När vi byggde vårt välfärdssamhälle så var det med bra jobb, en växande ekonomi och ett välstånd som kom alla till del.
- s12 Obehöriga lärare är tyvärr vardag i svensk skola, särskilt i vinstdrivande skolor men också i utanförskapsområden och på landsbygden.
- s12 Stora klasser och stök leder idag till sämre skolresultat och dålig arbetsmiljö för skolpersonalen.
- s14 Alltför många får vänta - ibland i ovisshet- på sin operation.
- s14 Det ska vara enkelt att komma i kontakt med vårdcentralen, man ska inte behöva vänta onödigt länge på en nödvändig operation och personalen ska ha tid för dig. Men så är det långtifrån alltid idag.
- s14 Det är ofta svårt att få en läkartid på vårdcentralen när man behöver det.
- s14 Men sjukvården dras också med stora problem.
- s14 Personalen tvingas jäkta från patient till patient.
- s14 Samtidigt brister stödet och samordningen kring patienter med kroniska sjukdomar och långtidssjukskrivna får inte det stödet de behöver.
- s14 Svensk sjukvård håller världsklass.
- s14 Vi har världens bästa läkare, sjuksköterskor, undersköterskor och vårdpersonal.
- s15 Behovet av personal inom äldreomsorgen är redan idag stort och kommer att öka framöver.
- s15 De omfattande problemen med bristande geografisk tillgång till tandvård behöver få en lösning.

**Lag och trygghet** (4)

- s16 Att politiken inte har klarat av att vända utvecklingen har skadat Sverige och tilltron mellan människor.
- s16 Bakom ungdomsgängen finns en växande organiserad brottslighet som blivit mer etablerad och förgrenat sig in i samhällsviktiga institutioner.
- s16 Den här utvecklingen skiljer sig från övrig brottslighet i samhället som inte ökat utan har legat still eller minskat.
- s17 Den pågående massnedläggningen av skyddade boenden behöver stoppas.

**Försvar och beredskap** (8)

- s18 Kina flyttar fram sina positioner såväl ekonomiskt som säkerhetspolitiskt.
- s18 Ryssland fortsätter hota stabiliteten på hela vår kontinent.
- s18 Samtidigt förändras Europas relation med USA.
- s18 USA riktar i ökad utsträckning sitt fokus mot andra delar av världen.
- s19 Den svenska försvarsindustrin är en vital del av Sveriges försvarsförmåga.
- s19 Det svenska stödet till Ukraina ligger fast så länge som det krävs.
- s19 Natomedlemskapet gör Sverige säkrare och Nato starkare.
- s20 FN och den regelbaserade världsordningen är under attack.

**Klimat, miljö och energi** (5)

- s10 I många år var Sverige ledande i klimatomställningen. Det resulterade inte bara i sänkta klimatutsläpp, utan också i fler jobb, tillväxt, minskat oljeberoende och stärkt konkurrenskraft.
- s10 Investeringar och jobb har uteblivit.
- s11 Den biologiska mångfalden hotas när arter trängs undan och hela ekosystem utarmas.
- s11 Sillen, strömmingen, torsken och andra svaga bestånd riskerar att slås ut när det storskaliga industrifisket fångar fisk i en snabbare takt än bestånden hinner återhämta sig och miljögifter sprids i våra hav.
- s11 Vi har unika resurser, kunskapen och ett näringsliv i framkant.

**Integration och sammanhållning** (6)

- s18 Den svenska samhällsgemenskapen bygger på plikt och rätt, svenska språket som samhällets gemensamma och att alla är med och bidrar.
- s18 Fattigdomen har förstärkts av ett språkligt utanförskap som försvagar delaktighet och inträde på arbetsmarknaden.
- s18 Framväxten av utsatta områden ger näring åt kriminalitet, religiös extremism och hedersförtryck.
- s18 För sextio år sedan byggdes miljonprogrammet med visionen att alla svenskar, oavsett inkomst, skulle ha ett gott hem till rimlig kostnad.
- s18 Konsekvenserna är tydliga: eftersatt underhåll, otrygghet, organiserad kriminalitet, slumvärdar, social dumping, växande arbetslöshet och förlorad framtidstro.
- s18 Under de många decennier som följt har samhället dragit sig tillbaka, segregationen fördjupats och invandringen varit större än vår förmåga att integrera.

**Frihet, demokrati och institutioner** (4)

- s17 De senaste åren har varit dåliga år för svensk kultur och idrottsliv.
- s17 Inte minst landsbygden har drabbats hårt när replokaler och folkhögskolor tvingats stänga. Eller när kursen i italienska eller artificiell intelligens har ställts in på grund av tidöpartiernas omfattande nedskärningar i folkbildningen.
- s17 Stundtals har kulturkriget slagit hårt mot alla eldsjälar och kulturskapare.
- s19 De högerradikala partiernas frammarsch är ett hot mot våra demokratiska värderingar och måste med kraft motarbetas.

**Utanför de sju kategorierna** (2)

- s3 Vi lever i en orolig tid. Med kriser och krig i vårt närområde som får direkt påverkan på vår vardag. Med starka krafter i rörelse som vill splittra oss. Världen förändras just nu mitt framför våra ögon. Samtidigt som Sverige glider isär och försvagas.
- s9 På många platser har samhället dragit sig tillbaka. På landsbygden märks det särskilt tydligt. När polisstationer, vårdcentraler och servicekontor läggs ned blir det svårare att få livet att fungera.


### M (187)

**Ekonomi och jobb** (47)

- s2 Det som många trodde var omöjligt inom en mandatperiod har visat sig fullt möjligt, med rätt politik, rätt prioriteringar och rätt vilja.
- s2 För det är fortfarande alltför många strävsamma människor som jobbar, bidrar, sliter med vardagspusslet och tar ansvar för sig och sin familj, men som trots det får för lite tillbaka för allt de ger.
- s2 Många menade att det skulle ta decennier att vända en sådan utveckling, om det ens gick.
- s2 Sverige är på rätt väg - men vi är inte framme.
- s4 Strävsamma människor som jobbar, bidrar, sliter med vardagspusslet och tar ansvar känner att de inte får tillräckligt tillbaka.
- s5 Sverige har vunnit över inflationen
- s6 Det har underlättat under ekonomiskt svåra tider till följd av hög inflation, ökande kostnader och lågkonjunktur.
- s6 I regeringen har Moderaterna stärkt arbetslinjen, bland annat genom sänkt skatt på låga och medelhöga inkomster.
- s7 Att det funnits en broms i pensionssystemet i dåliga ekonomiska tider men ingen gas i goda tider har varit orättvist.
- s7 Därför har vi sett till att en gas införs i pensionssystemet så att överskott som byggs upp kommer pensionärerna till del.
- s8 Det leder till att människor riskerar att falla mellan stolarna i stället för att få rätt stöd.
- s8 I dag gör Arbetsförmedlingen, Försäkringskassan och socialtjänsten ofta olika bedömningar av samma persons arbetsförmåga.
- s8 Moderaterna har i regering påbörjat en omläggning av bidragspolitiken.
- s9 Förutom att vi är det starkaste innovationslandet i EU har vi flest unicorns per capita i Europa, det vill säga startupbolag värderade till över en miljard amerikanska dollar.
- s9 I dag konkurrerar vi inte bara med våra grannländer utan med hela världen om investeringar, kompetens och framtidens jobb - där inte minst USA och Kina tävlar om produktion och företagsetableringar.
- s9 I regering har vi därför kraftigt ökat de offentliga investeringarna.
- s9 När viktiga investeringar i energi, industri, bostäder och infrastruktur fastnar i långa tillstånds- och miljöprövningar förlorar Sverige jobb, tillväxt och konkurrenskraft.
- s9 Och människor som vill bygga, utveckla eller investera möts av osäkerhet i stället för tydliga besked.
- s9 Sverige har goda förutsättningar.
- s10 Det är ofta här nya jobb skapas.
- s10 Matkravet för att få servera alkohol är avskaffat, likaså danstillståndet och hotelltillståndet.
- s10 Sveriges alla småföretag utgör ryggraden för ekonomin.
- s10 Vi har inrättat ett Förenklingsråd och driver på för enklare regler på EU-nivå - ett arbete som börjar ge resultat.
- s11 De höga marginalskatterna i Sverige hämmar drivkrafterna till utbildning, ansträngning och innovation, något som både Produktivitetskommissionen och OECD påtalat.
- s11 Från kullagret, separatorn och tändstickan till världsledande telekomteknik, digitala betallösningar och avancerad medicinteknik har svenska ingenjörer gång på gång förändrat världen.
- s11 I dag rankas Sverige som det mest innovativa landet i EU.
- s11 Men samtidigt utbildas för få ingenjörer för att möta framtidens behov.
- s11 Regeringen har beslutat om en STEM-strategi för Sverige som sträcker sig från förskola till forskarutbildning.
- s11 Regeringen har samtidigt genomfört den största satsningen på forskning och innovation någonsin.
- s11 Sverige blev rikt genom att uppfinna, utveckla och bygga.
- s11 Sverige investerar i dag mer i forskning och utveckling än något annat EU-land.
- s42 Det slopade matkravet bedöms leda till en kostnadsbesparing för berörda företag motsvarande cirka 3,9 miljarder kronor årligen i form av minskad administrationsbörda, lägre personalkostnader och minskat matsvinn.
- s45 De kulturella och kreativa branscherna utgör en ny svensk basindustri som omsätter 640 miljarder kronor per år.
- s46 Den låga offentliga skuldsättningen gör också att Sverige har bland de lägsta räntekostnaderna i hela EU.  `avviker`
- s46 Det finanspolitiska ramverket och den breda parlamentariska uppslutning som råder kring ramverket är centralt i detta sammanhang.
- s46 Detta gör den svenska ekonomin motståndskraftig.
- s46 Nyligen bekräftades att Sverige är ett av endast nio länder i världen som har högsta kreditbetyg hos de större kreditinstituten.
- s46 Sverige har en låg offentlig skuldsättning med offentliga finanser i världsklass.
- s46 Sveriges offentliga skuldsättning är i dag lägre än när Magdalena Andersson fick igenom sin sista budget och klart lägre än snittet i EU.
- s46 Tack vare starka statsfinanser har Sverige handlingsutrymme för att stå emot såväl säkerhetspolitiska som ekonomiska störningar vilket skapar en ekonomisk trygghet för alla svenskar.
- s47 Bara en procent i ökad tillväxt skulle innebära cirka 30 miljarder kronor i ökat reformutrymme.
- s47 Därutöver har Moderaterna tillsatt en Slöserikommission vars uppdrag är att se över utgifterna för den statliga förvaltningen och ge förslag på hur utgifterna kan minska.
- s47 För att värna styrkan i de offentliga finanserna, samtidigt som Sverige behåller en hög nivå på de offentliga investeringarna, är vi överens med de blågula partierna om att nya större reformer i huvudsak bör vara finansierade under nästa mandatperiod.
- s47 Hittills under mandatperioden har vi omprioriterat omkring 50 miljarder kronor av statens utgifter, vilket inneburit att de permanenta skattelättnader som regeringen har genomfört till betydande del varit finansierade.
- s47 Moderaterna har därför utvecklat principer för hur finansiering ska gå till och tagit fram förslag på finansiering.
- s47 Regeringens reformer - framförallt den stramare migrationspolitiken, att det blivit mer lönsamt att arbeta, bidragsreformen samt reformen av a-kassan - gör att såväl Regeringskansliet som Konjunkturinstitutet bedömer att den strukturella arbetslösheten kommer att minska trendmässigt framöver för första gången på 20 år.
- s48 Sverige har, även efter att enprocentmålet avskaffats, ett av världens mest generösa bistånd.

**Välfärd** (44)

- s16 En helt ny socialtjänstlag med fokus på förebyggande arbete har införts, Lex Lilla Hjärtat har stärkt barns rättigheter, socialtjänsten får möjlighet att ge insatser även när samtycke från föräldrar saknas och sekretesshinder har rivits.
- s21 De upplever i större utsträckning att det är lättare att få kontakt, att personalen har kännedom om deras sjukdomshistoria och mediciner samt att vården är anpassad efter deras behov och önskemål.
- s21 För att korta köerna långsiktigt pågår även arbetet med att bygga upp en nationell vårdförmedling.
- s21 I dag lägger läkare uppemot hälften av arbetstiden på administration i stället för på vård.
- s21 Men långa väntetider har länge varit ett problem inom svensk hälso- och sjukvård och skillnaderna är stora mellan olika regioner.
- s21 Moderaterna har drivit på för ökad statlig styrning för att korta vårdköerna.
- s21 Personer med en fast läkare har generellt sett mer positiva erfarenheter av sjukvården.
- s21 Samtidigt vittnar patienter om att de tvingas upprepa sin sjukdomshistoria och genomgå samma undersökningar flera gånger därför att information inte följer med genom vårdkedjan.
- s21 Trots detta har endast tre av tio en fast läkarkontakt i Sverige.
- s22 Allt för länge har kvinnors hälsa åsidosatts.
- s22 Forskning visar också att vården inte är jämlik för sjukdomar som drabbar både kvinnor och män.
- s22 I regering har vi genomfört ett antal åtgärder för att förbättra kvinnosjukvården.
- s22 Kvinnor behöver ofta visa mer smärta för att få samma behandling som män och får i många fall mindre resurser och en lägre vårdkvalitet.
- s22 Kvinnor får senare diagnos, har sämre tillgång till nya läkemedel och får vänta längre på behandling.
- s22 Sammantaget bidrar detta till att kvinnor är mer sjukskrivna än män, vilket inte bara innebär svårigheter och inkomstförluster för den enskilda kvinnan utan även stora kostnader för samhället.
- s22 Tyvärr har kvinnors hälsa och sjukdomar länge varit eftersatta både inom forskning och kliniskt arbete.
- s22 Vi har också tagit viktiga steg för att stärka aborträtten och möjligheterna till att genomföra medicinsk abort i hemmet.
- s23 Fler pappor är föräldralediga, barnet får knyta an till båda föräldrarna och det har visat sig vara positivt för mammors hälsa.
- s23 Flera tusen kvinnor drabbas årligen av allvarliga bristningsskador.
- s23 Många kvinnor lever med komplikationer som skulle kunna ha åtgärdats i ett tidigare skede.
- s23 Tack vare framsteg inom fertilitetsbehandlingar kan allt fler kvinnor i dag bli gravida vid en högre ålder.
- s23 Vi har sett positiva effekter för jämställdheten av att regeringen 2024 dubblade dubbeldagarna.  `avviker`
- s23 Vården vid graviditet och förlossning håller överlag hög kvalitet och är säker. Men trots en hög standard finns det tydlig förbättringspotential, särskilt gällande eftervård.
- s24 Detta gäller inte minst barn- och ungdomspsykiatrin, där många barn och unga inte får hjälp i tid trots ökande behov.
- s24 Efter de brister i äldreomsorgen som uppdagades efter pandemin har Moderaternas arbete i regering gått ut på att höja kvaliteten i äldreomsorgen.
- s24 I regering har vi påbörjat arbetet med att vända utvecklingen.
- s24 Psykisk ohälsa är i dag den främsta orsaken till sjukskrivning, samtidigt som psykiatrin är hårt pressad med långa väntetider.
- s24 Samtidigt brister samordningen mellan psykiatri, primärvård, elevhälsa och socialtjänst, vilket gör att personer med komplexa behov riskerar att falla mellan stolarna och i praktiken tvingas samordna sin egen vård.
- s24 Vi har beslutat om en nationell strategi, ökade resurser och riktade satsningar på BUP och barns och ungas psykiska hälsa, men mer behöver göras för att säkerställa en tillgänglig och sammanhållen vård i hela landet.
- s25 Det är både ovärdigt och farligt då näringsrik mat är viktigt för såväl livsglädje och som för att undvika undernäring.
- s25 Men på senare tid har rapporter kommit om att kommuner i stället dragit ner på uppskattade och näringsrika maträtter som lax och kött på äldreboenden.
- s25 Sverige är ett föregångsland när det gäller vaccinationsgraden bland barn, med en täckning på cirka 95 procent inom det nationella vaccinationsprogrammet.
- s25 Trots dessa goda erfarenheter saknas ett motsvarande nationellt program för äldre.
- s27 Barn och ungdomar i Sverige har i dag mycket god tillgång till olika digitala verktyg i hemmet och på sin fritid.
- s27 Fram till 1991 fanns det en statlig granskning av läromedel.
- s27 Samtidigt har träning av handstil under lågstadiet visat sig ha en viktig betydelse för hjärnans kognitiva utveckling och en elevs inlärning.
- s27 Sedan dess har läromedelsmarknaden släppts fri och det finns ingen som ansvarar för att säkerställa att läroböckerna i matematik, svenska och andra ämnen håller måttet.
- s28 Bland annat har vi gjort skoldagen mobilfri samt möjliggjort längre avstängningar och särskilda akutskolor för elever med ett allvarligt störande, hotfullt eller våldsamt beteende.
- s28 Det är en ohållbar situation som sviker både de barn som har svårt att sitta still och de elever som aldrig får arbeta i lugn och ro.
- s28 En stor del av kränkningarna sker i dag via mobiltelefoner, vilket gör att mobbarna dessutom följer med hem.
- s28 Moderaterna har i regeringen tagit flera viktiga steg för att skapa en tryggare skola.
- s28 Sverige sticker ut i Europa med att ha den sämsta klassrumsdisciplinen, enligt Pisa-mätningen.
- s48 Den moderatledda regeringen har sett till att resurserna till välfärden är på en historiskt hög nivå och vi vill se till att resurserna till sjukvården, skolan och omsorgen ökar varje år.
- s48 Det finns samtidigt stora ekonomiska behov i Sverige som ställer krav på att skattebetalarnas pengar prioriteras på bästa sätt.

**Lag och trygghet** (32)

- s2 En skenande kriminalitet fick många familjer att dra sig för att släppa ut barnen på gården.
- s2 För fyra år sedan fanns det medborgare som hade börjat fråga sig om Sveriges stora samhällsproblem överhuvudtaget kunde lösas.
- s13 Riksdagen har godkänt den moderatledda regeringens förslag om att slopa dagens mängdrabatt.
- s13 Rådet mot kvinnofrid inrättades i januari 2026 med en nollvision för det dödliga våldet mot kvinnor.
- s13 Vi har stärkt kontaktförbuden, skärpt straffen för allvarliga sexualbrott och infört en ny brottsrubricering för psykiskt våld.
- s15 Allt yngre barn dras in i grov brottslighet.
- s15 Dagens system lyckas varken skydda medborgarna från livsfarligt våld, ge brottsoffer upprättelse eller bryta de destruktiva mönster som finns runt de här barnen.
- s15 De intäkterna finansierar våldet, rekryteringen och infiltrationen av vårt samhälle.
- s15 De kriminella nätverken omsätter hundratals miljarder kronor varje år genom bedrägerier, välfärdsbrott, narkotikahandel och annan organiserad brottslighet.
- s15 Fler grova våldsbrott förhindras, fler gärningsmän lagförs och fler kriminella grips utomlands.
- s15 Gängen har flyttat sin rekrytering från skolgården till mobiltelefonen och använder barn som utförare av våldsbrott och annan kriminalitet.
- s15 Sverige är tryggare i dag än för några år sedan.
- s15 Under denna mandatperiod har regeringen tagit fram förslag som gör det straffbart att vara med i ett kriminellt gäng och som innebär att gängtoppar med dubbla medborgarskap kan bli av med sitt svenska medborgarskap.
- s15 Utvecklingen är ett uttryck för flera saker - en organiserad brottslighet som under alldeles för lång tid möttes med otillräckliga insatser och ett rättspolitiskt system som byggts för en annan tid och verklighet.
- s16 I regeringsställning har vi genomfört den största omläggningen av politiken någonsin för att öka barns trygghet och sätta in insatser tidigt.
- s16 Systemet har inte varit byggt för den verklighet där barn används som soldater i kriminella nätverk.
- s16 Vi river sekretesshinder, stärker socialtjänstens möjligheter att agera tidigt och skärper straffen för dem som utnyttjar barn i kriminella syften.
- s17 Alltför många upplever otrygghet i sina bostadsområden.
- s17 Den pågående utbyggnaden av bevakningskameror till minst 5 000 vid utgången av 2027 kommer att ge polisen ännu bättre förutsättningar att både förebygga och utreda brott på otrygga platser.
- s17 Moderaterna har redan tagit bort tillståndsplikten för kamerabevakning för kommuner, regioner och statliga myndigheter.
- s18 Alltför ofta är det gärningsmannen som står i fokus för samhällets reaktioner, medan brottsoffret lämnas att själv kämpa för upprättelse och kompensation. Det är djupt orättvist och naggar samhällskontraktet i kanterna.
- s18 Det gäller även de brott som brukar benämnas mängdbrott, där en liten grupp står för flertalet brott som drabbar människor i vardagen.
- s18 I dag hamnar pengar från förverkad brottslig egendom i den allmänna statskassan.
- s18 När dessa brott inte lagförs skapas en ond spiral, där benägenheten att anmäla sådana brott minskar.
- s18 Regeringen har lagt fram ett sådant förslag, men ikraftträdandet kan riskeras med en annan regering efter nästa val.
- s19 Av de som anmält uppger få att brottet klarades upp.
- s19 Bangladesh, Ecuador, Chile, Costa Rica, Peru och Sverige. I dessa länder oroar sig företagen mest för att drabbas av brott, visar en rapport från World Economic Forum.
- s19 En av de främsta anledningarna till att inte anmäla är bristande tilltro till polisens förmåga att lösa brott.
- s19 Moderaterna har genomfört en lång rad reformer för att skydda barnen och straffa förövarna.
- s19 Näringslivets kostnader för brottsligheten uppskattas nu uppgå till över 100 miljarder kronor per år.
- s19 Omkring hälften av de företagare som utsatts för brott har avstått från att polisanmäla.
- s19 Vi ser också till så att den som tror sig ha kontakt med ett barn i syfte att begå sexuella övergrepp kan dömas för detta även om en polis tagit över chattkonversationen.

**Försvar och beredskap** (16)

- s30 EU är Sveriges viktigaste utrikespolitiska plattform och vår bästa möjlighet att tillsammans värna demokrati, frihet och internationell rätt.
- s30 Erfarenheterna från Ukraina visar att luftvärn, drönare, långräckviddig bekämpning och försvarsinnovation kommer att vara avgörande för framtidens försvarsförmåga.
- s30 I en tid då Ryssland fortsätter sitt anfallskrig mot Ukraina och utvecklar sin militära förmåga behöver Europas norra flank bli starkare.
- s30 Inte bara Norden, utan även Baltikum och länderna kring Östersjön, står i dag inför liknande hotbild och har ett gemensamt intresse av att försvara vår frihet, säkerhet och självständighet.
- s30 På slagfälten i Ukraina, genom det ukrainska samhällets motståndskraft och befolkningens mod, avgörs om Europa även i framtiden ska bestå av suveräna stater.
- s30 Stödet till Ukraina är Sveriges främsta utrikespolitiska uppgift och en nödvändig investering i Europas - och därmed vår egen - säkerhet, självständighet och framtid.
- s30 Sveriges och Finlands medlemskap i Nato har skapat helt nya möjligheter att stärka säkerheten i vårt närområde.
- s31 En ny nationell cybersäkerhetsstrategi har antagits och Sveriges operativa cyberförmåga har stärkts.
- s31 Erfarenheterna från Ukraina visar också att Ryssland medvetet attackerar civilbefolkningen och kritisk infrastruktur.
- s31 Moderaterna har i regering inrättat ett stärkt nationellt cybersäkerhetscenter (NCSC) under ledning av FRA.
- s32 Den tekniska utvecklingen i världen påverkar utrikes- och säkerhetspolitiken både positivt och negativt.
- s32 Ny teknik som artificiell intelligens, miniatyriserade satelliter och kvantteknik får en större roll.
- s32 Regeringens målmedvetna arbete för svensk försvarsindustri har bidragit till det.
- s32 Sverige har och ska fortsatt ha en försvarsindustri i världsklass med kapacitet att både producera högteknologiska system och mer mängdproducerat och kostnadseffektivt materiel.
- s32 Under den nuvarande mandatperioden har Sveriges försvarsindustri gjort unikt många mångmiljardaffärer.
- s48 Riksdagens åtta partier är överens om att permanent finansiering ska komma på plats senast 2035 och regeringen ska i varje budgetproposition från och med 2027 redovisa hur arbetet med finansieringen fortgår.

**Klimat, miljö och energi** (18)

- s2 Ett elsystem i kris hotade både industrins konkurrenskraft och den enskilda familjens ekonomi.
- s2 Vi har börjat arbetet med att få ordning på elsystemet och sett till att människor får behålla mer pengar i plånboken.
- s9 Energiförsörjningen byggs ut långsammare.
- s9 Klimatomställningen försenas.
- s10 Men dagens system sätter för stor tyngdpunkt vid miljöskydd och leder till att viktiga projekt försenas eller stoppas.
- s39 För att omställningen inte ska straffa den som i dag är beroende av sin bensin- eller dieseldrivna bil är det bråttom att få på plats tillräcklig laddinfrastruktur för elbilar i hela Sverige.
- s39 Förnybar energi, såsom vind-, vatten- bio- och solenergi, är också en viktig del av energimixen.
- s39 I regering har vi tagit fram en finansieringsmodell för att stötta de första projekten för ny kärnkraft.
- s39 Moderaterna vill byta ut transportmålet som innebär att dieselpriset på kort tid behöver höjas med upp till 10 kronor per liter, mot ett elektrifieringsmål som innebär fler elfordon på svenska vägar.
- s39 Omkring en tredjedel av Sveriges nationella utsläpp kommer från inrikes transporter, framför allt från bilar och lastbilar.
- s39 Snåriga beslutsprocesser gör det exempelvis svårt och dyrt att bygga vindkraft.
- s40 Antalet hagar och betesmarker har blivit färre över tid, inte minst för att enskilda bönder upplevt att det inte är möjligt eller rimligt att lägga ner den tid, kraft och pengar som krävs för att hålla markerna betade med djur.
- s40 Artskyddsförordningen, som bygger på EU-beslut, är en del av den miljölagstiftning som orsakar stora problem för skogsbrukare.
- s40 Den ger staten en rätt att kräva att den som äger skog helt eller delvis avstår från att bruka sin mark, exempelvis på grund av att en relativt vanlig fågelart finns där.
- s40 I regeringsställning har vi gjort flera satsningar för att stärka hela livsmedelskedjan och främja svensk livsmedelsproduktion.
- s41 Det innebär att bestånd av fisk, särskilt i kustnära vatten, håller på att försvinna helt.
- s41 Säl och skarv fångar och äter numer minst lika mycket fisk som vi människor fiskar upp.
- s41 Trots vår långa kustlinje och våra stora fiskevatten importerar vi i dag mer fisk och skaldjur för konsumtion än vi producerar själva.

**Integration och sammanhållning** (11)

- s2 Vi har fått kontroll på invandringen, stärkt barns rättigheter och prioriterat välfärdens kärna.
- s8 Den som har invandrat till Sverige behöver numera kvalificera sig genom att arbeta och bidra innan den får tillgång till hela välfärden.  `avviker`
- s8 Nu ställs tydliga krav på den som får försörjningsstöd att ta steg mot arbete.
- s34 Den obegränsade rätten till offentligt finansierad tolk har inneburit att många saknat tillräckliga drivkrafter att lära sig svenska.
- s34 Därför har vi också höga förväntningar på att den som kommer hit snabbt lär sig tillräckligt bra svenska, blir självförsörjande och en del av den svenska gemenskapen, precis som så många redan har blivit.
- s36 Men hundratusentals unga i Sverige lever under hedersförtryck och berövas sina grundläggande fri- och rättigheter.
- s36 Nyligen förbjöds även kusinäktenskap, och att utsätta någon för psykiskt våld eller tvång har kriminaliserats.
- s36 Vi har gjort det straffbart att inte avslöja eller förhindra tvångs- eller barnäktenskap.
- s37 75 % färre asylsökande
- s37 Under åren 2000-2020 tog Sverige varje år emot i genomsnitt 4 gånger så många asylsökande per capita som genomsnittet i EU.
- s37 Vi är övertygade om att integrationsproblemen går att lösa, men vi ser också att de är mycket stora.

**Frihet, demokrati och institutioner** (5)

- s44 Trots att Sverige befinner sig i det allvarligaste säkerhetsläget sedan andra världskriget står sig den svenska demokratiska rättsstaten fortsatt stark och är väl förankrad i våra grundlagar.
- s45 I regering har Moderaterna fattat beslut om en ny public service-lag som både är teknikneutral och slår fast tydliga krav på neutralitet och saklighet oavsett distributionsform.
- s45 Men teknikutvecklingen, inte minst med AI, innebär utmaningar för befintliga affärsmodeller, upphovsrätt och verifiering som kräver en fortsatt hög reformtakt.
- s45 Public service-bolagen har fått en garanterad finansiering för åtta år, men kommer i likhet med privata bolag att löpande behöva effektivisera sin verksamhet.
- s45 Vi har även infört ett nytt mediestöd med fokus på kvalitativ lokaljournalistik.

**Utanför de sju kategorierna** (14)

- s7 Den trenden sammanfaller med att barnafödandet i Sverige är historiskt lågt.
- s7 I regering har Moderaterna redan lättat på strandskyddet, förenklat byggregler och gjort det lättare att spara ihop till kontantinsatsen till en egen bostad, men mer behöver göras.
- s7 Men för många känns husdrömmen i dag avlägsen. Det är för dyrt, inte minst för unga och barnfamiljer.
- s7 När två helt vanliga löner inte längre räcker för att köpa ett hus riskerar något viktigt att gå förlorat: tron på att nästa generation kan få det bättre än den förra.
- s7 Sju av tio svenskar vill någon gång bo i hus.
- s41 Länge har fisk varit basföda för våra svenska kustsamhällen och både kust och skärgård är i dag viktiga resmål för besöksnäringen.
- s41 Med ett skyddsområde som sträcker sig 100 meter från strandlinjen innebär det att strandskyddet sammanlagt omfattar ett område ungefär lika stort som Danmark.
- s41 Många vittnar om att strandskyddsreglerna i dag utgör ett hinder, inte minst mot landsbygdens utveckling.
- s41 Om man räknar in alla kuster, öar, vattendrag och insjöar utgör den sammanlagda strandlinjen i Sverige över 400 000 km, vilket motsvarar nästan 11 varv runt jorden.
- s42 Förr flyttade människor till jobben.
- s42 Numera flyttar tvärtom företag och jobb dit människor vill leva och verka.
- s45 En stor kulturbyråkrati konkurrerar också om resurser.
- s45 För att stötta branschen har vi bland annat sett till att den orättvisa dansbands- och nattklubbsmomsen har sänkts, liksom momsen på konstverk.
- s45 Vi vill göra det mer gynnsamt för företag att sponsra kultur och har utrett utökad avdragsrätt för privatpersoner att ge, liksom införandet av ett matchningssystem.


### SD (56)

**Ekonomi och jobb** (12)

- s8 Elskatten gör vardagen dyrare för både hushåll och företag.
- s8 I takt med att djursjukvården blir dyrare så blir även försäkringspremierna dyrare, något som påverkar många djurägares ekonomi.
- s8 Staten ställer många krav på svenska bönder som går utöver EU’s minimikrav vilket missgynnar svenska bönder på den inre marknaden, här tycker vi att staten ska ersätta lantbruket för de nationella särkrav vi har.
- s9 Den tillfälliga sänkningen av matmomsen har visat sig vara ett effektivt verktyg för att få ner matpriserna.
- s9 Matkostnader utgör en stor del av hushållens utgifter, särskilt för barnfamiljer.
- s9 Under mandatperioden har Sverigedemokraterna varit starkt pådrivande för att sänka priset på drivmedel.
- s18 Eftersom BNP nu växer, växer också den samlade ekonomin och därmed reformutrymmet.
- s18 I relation till det finanspolitiska ramverket, där skuldankaret ska vara 35 procent, +/- 5 procent, är detta inom marginalen.
- s18 Konjunkturinstitutet presenterade i sin uppdatering den elfte augusti 2026 en bedömning som pekar på ett årligt reformutrymme på omkring 23 miljarder kronor.
- s18 Konjunkturinstitutet räknar med att skuldsättningen landar på 36 procent.
- s18 Samtidigt ligger skuldsättningen fortfarande inom ramverket för andelen av BNP.
- s18 Totalt för mandatperioden 2027-2030 beräknas utrymmet till cirka 95 miljarder kronor.

**Välfärd** (8)

- s4 Från och med den 1 januari 2026 betalar äldre endast 10 procent av referenspriset för nödvändiga behandlingar som lagningar, rotfyllningar och reparationer.
- s4 Staten tar resten.
- s8 Det gör att många djur antingen avlivas eller inte får den vård som de behöver.
- s8 Många har inte råd att ha en försäkring som täcker kostnaderna när något händer.
- s8 Ungefär en tredjedel av hushållen har ett eller flera husdjur, de senaste åren har priserna på djursjukvård skenat långt över prisökningen på andra tjänster och på många håll är tillgången starkt begränsad, inte minst under kvällar och helger.
- s9 För ungdomar på landsbygden är kollektivtrafiken sällan ett fungerande alternativ efter skoltid.
- s10 Dagens system med många kommunala huvudmän har bidragit till stora skillnader mellan skolor i olika delar av landet.
- s10 Skolan är en viktig knytpunkt i många byar och när den stängs dör en del av bygden.

**Lag och trygghet** (7)

- s5 Den som har blivit utsatt för grova brott riskerar att aldrig bli fri från de djupa sår som detta skapat.
- s5 I Socialdemokraternas Sverige har brottsofferperspektivet glömts bort.
- s5 I decennier har kriminalpolitiken i Sverige haft ett helt felaktigt fokus.
- s5 Idag kostar en anstaltsplats nästan dubbelt så mycket.
- s15 Både rödgröna och borgerliga regeringar har under lång tid blundat för kriminaliteten på svenska byggarbetsplatser.
- s15 Resultatet ser vi i form av illegal arbetskraft som arbetar under slavliknande villkor och vars förekomst bidrar till lönedumpning och undanträngningseffekter för svenska löntagare.
- s16 Det öppna tiggeriet har alldeles för länge bidragit till otrygghet och oreda i samhället.

**Försvar och beredskap** (1)

- s7 Under mandatperioden har Sverigedemokraterna stått på Ukrainas sida i kampen mot Ryssland.

**Klimat, miljö och energi** (6)

- s8 I Sverige har vi fantastisk åkermark, tyvärr försvinner den i rask takt när kommuner väljer att exploatera denna med bostäder och industrier, det vill vi stoppa, åkermark ska odlas, inte bebyggas.
- s11 På senare år har många skogsägare hamnat i kläm när de försökt bruka sin skog, helt orimligt tycker vi.  `sidbrott`
- s11 Skogen är en oerhört viktig resurs i Sverige, både som exportvara och för alla de arbetstillfällen den genererar på landsbygden.
- s12 Att sänka utsläppen ytterligare i Sverige är mycket dyrt, den globala klimateffekten av sänkta utsläpp i Sverige är försumbar men kostnaden för hushåll och företag blir enorm.
- s12 Avverkningar under 2 ha ska kunna göras utan avverkningsanmälan och för att överklaga en avverkning vill vi införa en kostnad, det är helt orimligt som det är idag när personer helt utan anknytning kan överklaga avverkningsbeslut när detta får enorma ekonomiska konsekvenser för markägaren.
- s12 Sist men inte minst är skogsråvaran vi producerar viktig för att kunna fasa ut fossila produkter, vi vill stärka och öka svensk skogsproduktion, det är det bästa för Sverige, landsbygden, ekonomin, skogsägaren och klimatet.

**Integration och sammanhållning** (9)

- s13 Dels handlar det om engelskans inflytande, där vi både kan läsa och höra hur allt fler anglicismer letar sig in i såväl talad som skriven svenska.
- s13 Det handlar även om påverkan från språkgrupper som kommit till Sverige, såsom arabiska.
- s13 Det svenska språkets särart hotas idag från flera håll.
- s13 Detta bidrar till att sociolekter växer fram och därmed även till den kulturella splittringen.
- s13 Idag ser vi allt för ofta hur barn inte får de förutsättningar de behöver för att bli en del av den svenska samhällsgemenskapen.
- s14 Den nya anvisningslagen är bättre än den äldre, men den löser inte problemet.
- s14 Idag har kommunerna inga reella möjligheter att tacka nej till att ta emot asylinvandrare, det vill vi ändra på.
- s15 Det finns många röda, gröna och i vissa fall blåa kommuner i Sverige som fortfarande är av uppfattningen att invandringen berikar vårt land.
- s16 Dagens regler innebär ännu inte ett krav på att en person måste ha klarat ett individuellt språktest på B2-nivå för att kunna anställas.

**Frihet, demokrati och institutioner** (10)

- s4 Socialdemokraterna har tillsammans med oppositionen röstat nej till detta.
- s15 Dessa företag och organisationer är ofta verksamma på marknader som ligger nära exempelvis kommunernas verksamhet, vilka i sin tur kan använda politisk makt för att gynna dessa.
- s15 Detta är en ordning som bäddar för politisk korruption, urholkar förtroendet för politiken och existerar heller inte i något annat land i Europa.
- s15 Politisk islam är ett hot mot vårt demokratiska samhälle, även när den inte leder till våld eller terrorism.
- s15 Under lång tid har det varit möjligt för politiska partier i Sverige att tillskansa sig makt och ekonomiska värden via tätt knutna företag och organisationer.
- s16 Det har förekommit allvarliga systembrister med fusk och bidragsmissbruk där skattemedel inte använts på avsett sätt.
- s16 I en Tidö-utredning presenterades förslag i syfte att göra det möjligt att återkalla svenskt medborgarskap från den som har förvärvat medborgarskapet på felaktiga grunder eller som har begått vissa allvarliga brott, till exempel viss allvarlig systemhotande brottslighet som begås inom ramen för kriminella nätverk.
- s17 I nära tusen år har monarkin varit en naturlig del av vårt land.
- s17 Idag kan den som dömts till utvisning rösta i svenska val.
- s17 Socialdemokraterna och vänsterpartierna avskyr Sveriges kungahus på ideologisk grund.

**Utanför de sju kategorierna** (3)

- s14 Alltför mycket av samtidskulturen, från enskilda kulturskapare till kulturinstitutioner, är beroende av offentliga medel.
- s14 Sverige har en enorm kulturarvsskuld, och i dagsläget saknas en samlad bild av hur omfattande den faktiskt är.
- s14 Sverige sticker ut i ett europeiskt perspektiv genom att vi saknar tillräckligt utvecklade system och metoder för att öka den privata eller alternativa finansieringen.


### C (141)

**Ekonomi och jobb** (40)

- s4 Samtidigt har vi företag som vill skapa jobb, men som motarbetas.
- s4 Sverige har människor som vill arbeta, men som inte ges den möjligheten.
- s4 Vid köksbord i hela Sverige går familjer igenom sin ekonomi med en växande insikt om att marginalerna blivit mindre, trots att ansträngningen är densamma.
- s5 När många lantbrukare går på knäna är det inte bara ett problem för den enskilde företagaren, det är ett problem för hela Sveriges förmåga att försörja sig självt.
- s5 Svenskt jordbruk pressas från flera håll samtidigt av ökade kostnader och av osäkra villkor och regelverk som gör det svårare att få verksamheten att gå runt.
- s12 Krångel, höga kostnader och osäkra politiska villkor gör att många inte vågar anställa.
- s12 Samtidigt motarbetas företag som skapar jobb.
- s12 Samtidigt som företag skriker efter personal stänger regeringen dörren för talang genom absurda kompetensutvisningar.
- s12 Sverige har fastnat i hög arbetslöshet, svag tillväxt och låg produktivitet.
- s12 Utbildningar som inte möter företagens och välfärdens behov fördjupar arbetslösheten och utanförskapet.
- s14 Arbetslösheten breddas nu till nya grupper, inklusive akademiker.
- s14 Dagens arbetsmarknadspolitik misslyckas med att skapa riktiga vägar till arbete.
- s14 Sverige befinner sig i en arbetslöshetskris där allt för många människor står utan jobb, samtidigt som företagen inte hittar rätt kompetens.
- s14 Sverige har bland världens högsta skatter på att anställa personer med låga inkomster där över en tredjedel av de så kallade arbetsgivaravgifterna är en ren skatt på anställningen utan att finansiera förmåner som sjukledighet eller pension.
- s15 Arbetslösheten är hög på många håll men lägre på andra, där företagen istället inte hittar nya medarbetare som kan ta de jobb som finns.
- s15 Bara varannan person med funktionsnedsättning arbetar idag, det är ett underbetyg till samhället.
- s15 Idag försvinner stora delar av inkomstökningen i minskade bidrag, och människor som vill arbeta fastnar i trösklar bort från bidragen.
- s16 Det gör att många företag tvekar inför att anställa och expandera.
- s16 Företagare i Sverige möter en snårskog av krångliga regler, höga kostnader och en osäkerhet som gör det svårt att starta, driva och utveckla verksamheter.
- s16 Sverige ligger i botten i EU sett till andelen företagande kvinnor.
- s17 Barn till ensamförsörjande föräldrar löper högre risk att drabbas av barnfattigdom.
- s17 Ett gemensamt problem är icke-fungerande marknader där enskilda aktörer har för stor dominans.
- s17 Många avgifter och kostnader har på kort tid rusat i höjden.
- s18 Det höga lönegolvet för arbetskraftsinvandrare är skadligt för svensk tillväxt då företag blir av med anställda som utvisas och får svårare att rekrytera nya medarbetare.
- s18 Just nu förändras arbetsmarknaden dessutom snabbt genom AI, digitalisering och den gröna omställningen.
- s18 Problemet är att utbildning och arbetsliv inte hänger ihop tillräckligt bra.
- s18 Sverige har en arbetsmarknad där många arbetsgivare inte hittar rätt kompetens, samtidigt som många, särskilt unga och studenter, har svårt att få sina första jobb.
- s19 Bostadsbristen begränsar människors frihet och håller tillbaka Sveriges utveckling.
- s19 Boverket uppskattar att minst en halv miljon bostäder behöver byggas till 2034, men byggandet är inte nära att nå dit.
- s19 Sverige lider av allvarlig bostadsbrist, som bara väntas förvärras.
- s20 Den teknologiska utvecklingen går snabbt och artificiell intelligens omformar just nu både arbetsmarknaden och ekonomin i grunden.
- s20 Tyvärr bromsar politiska hinder tillväxten, kompetensförsörjningen brister och vägen in på arbetsmarknaden blir längre för många, inte minst för unga och nyutexaminerade.
- s50 Här produceras maten, råvarorna och energin som får landet att fungera.
- s54 Låga marknadsvärden idag gör det svårt att få lån.
- s54 Men idag möter företag regelkrångel, sämre tillgång till kompetens och en service som steg för steg försvinner.
- s54 Nedlagda butiker, mackar och annan kommersiell service som nedmonteras påverkar även hela lokalsamhället negativt.
- s55 Kostnaderna för svenska lantbruk är för höga.
- s55 Samtidigt pressas lantbrukare av ökade kostnader, hård konkurrens och regelverk som inte bara försvårar utveckling utan leder till många nedläggningar.
- s55 Summerat ser vi hur det i praktiken finns en gårdsskatt.
- s93 Det höga lönegolvet för arbetskraftsinvandrare är skadligt för svensk tillväxt.

**Välfärd** (34)

- s4 Samtidigt upplever de som arbetar i välfärden att tiden inte räcker till.
- s4 Vi har en ung generation som inte mår bra, där den psykiska ohälsan breder ut sig och där alltför många inte får stöd i tid.
- s7 För många unga mår dåligt i Sverige.
- s34 I storstäderna är trycket istället högt, med långa köer, hög belastning och stora skillnader i livschanser mellan områden som ligger nära varandra.
- s34 Lager efter lager av krav, system och kontroller har byggts upp och på bara ett decennium har antalet administratörer och chefer utan bakgrund i välfärdens professioner ökat med nästan femtio procent.
- s34 Många i välfärdsyrken känner samvetsstress, för att de inte hann trösta det ena barnet medan det andra behövde gå på toaletten.
- s34 Personal inom vård, skola och omsorg vittnar om en arbetsvardag där tiden inte räcker till och där administration och detaljstyrning tar över på bekostnad av kärnuppdraget.
- s34 På landsbygderna och i mindre orter försvinner vårdcentraler, skolor och annan samhällsservice. Avstånden ökar och det blir svårare att få vård eller utbildning nära sitt hem.
- s34 Skolan sviker också: alltför många elever lämnar grundskolan utan fullständiga betyg, ordningen i klassrummen brister och elever som behöver stöd får det inte i tid.
- s34 Vårdköerna är fortsatt långa. För många får vänta för länge på behandling. Barn och unga med psykisk ohälsa fastnar i köer istället för att få hjälp i tid.
- s35 För mycket resurser i välfärden går till administration istället för till människor.
- s35 För många barn och unga mår dåligt och fastnar i köer där hjälpen kommer för sent.
- s35 För många elever lämnar skolan utan att ha fått rätt stöd.
- s36 Samtidigt räcker inte personalen till och vården är för dåligt organiserad. Resultatet blir att människor inte får hjälp i tid.
- s37 Alltför många barn och unga mår psykiskt dåligt idag utan att få hjälp, ibland utan att någon ser dem.
- s37 Det finns ett generationsglapp i den psykiska hälsan idag. Unga vuxna svenskar mår allt sämre och känner mindre livstillfredsställelse, mindre mening i livet och sämre ekonomisk trygghet än äldre åldersgrupper.
- s38 För många får vänta för länge, får fel stöd eller faller mellan stolarna när vårdkedjan inte hänger ihop.
- s38 Psykisk ohälsa är en av folkhälsans största utmaningar, men vården räcker inte till.
- s39 För många elever lämnar idag skolan utan fullständiga kunskaper.
- s40 Detaljstyrning och politiska pekpinnar begränsar professionens utrymme, trots att det är lärarna, rektorerna och skolorna som bäst vet vad som fungerar för eleverna.
- s40 Många lärare pressas idag av stora klasser, hög arbetsbelastning och en växande administration.
- s41 För många elever, särskilt de med neuropsykiatriska funktionsnedsättningar, blir skolan en kamp istället för en möjlighet.
- s41 Föräldrar tvingas slåss för stöd som borde vara självklart, och barns skolgång avgörs ibland av familjens resurser snarare än elevens behov.
- s42 Idag söker sig för få till vård, skola och omsorg, samtidigt som arbetsvillkoren ofta är för tuffa och möjligheterna att utvecklas för små.
- s43 Fler lever allt längre liv, men många äldre möter en vardag där deras valmöjligheter är begränsade, tillgången till vård varierar och stödet inte alltid utgår från individens behov.
- s44 För mycket av tiden i välfärden går till administration istället för till människor.
- s44 Krångliga statsbidrag, återrapportering och onödig byråkrati stjäl resurser från vård, skola och omsorg.
- s46 Kvinnors hälsa har länge varit nedprioriterad i vården. Kunskapen om kvinnorelaterade sjukdomar är för dålig, tillgången till vård varierar och många får vänta för länge på diagnos och behandling.
- s50 Vägar förfaller, vården blir svårare att nå och skolor hotas av nedläggning.
- s52 Det leder till otrygghet och bidrar till att människor i landsbygder i högre grad drabbas av sjukdomar som hade kunnat behandlas i tid.
- s53 Ett byråkratiskt tungt regelverk byggt för stora skolor gör det svårare att driva landsbygdsskolor.
- s53 På många håll i landsbygderna är det svårare att rekrytera behöriga lärare, resultaten är lägre och hotet om nedläggning ständigt närvarande.
- s68 Men vi vet att efterfrågan på sjukvården för dessa ingrepp består.
- s77 Idag ser vi hur allt fler behöver medicinsk hjälp för att få barn, samtidigt som tillgången till behandling varierar och möjligheterna begränsas av system som inte hängt med i människors verklighet.

**Lag och trygghet** (23)

- s5 I grova brott och organiserad kriminalitet som biter sig fast och påverkar en generation av barn och unga.
- s51 Stärk polisens närvaro i de delar av landet där den idag är alldeles för svag.
- s57 Idag är polisens närvaro svagare i många landsbygdsområden samtidigt som brott mot individer, företag och lantbruk fortsätter, med exempelvis inbrott, bedrägerier och stölder av diesel och andra råvaror.
- s57 När staten drar sig tillbaka växer otryggheten och tilliten minskar.
- s60 Företag utnyttjas, välfärdssystemen plundras och parallella strukturer etableras.
- s60 Kvinnors frihet begränsas, äldre känner oro och företagare utsätts för brott som sällan leder till konsekvenser.
- s60 Många människor upplever oro i sin vardag - i bostadsområden, i sina hem, på arbetsplatser och i det offentliga rummet.
- s60 Skjutningar, sprängningar och systematisk brottslighet har tagit över vardagen på platser där människor tidigare levde i trygghet.
- s60 Sverige har varit ett sådant land.
- s62 För många upplever idag att polisen inte hinner fram, att brott inte utreds och att konsekvenser uteblir.
- s62 Många mängdbrott som inbrott, cykelstölder och dieselstölder från jordbrukare anmäls sällan ens när människor inte litar på att det leder till något.  `avviker`
- s64 För många barn och unga rekryteras in i våld, utnyttjas för brott och växer upp med en normalisering av gängens kriminella värld.
- s64 Samhällets insatser kommer ofta för sent, hänger inte ihop och är för svaga för att bryta utvecklingen.
- s66 Bara i Sverige kan kriminella identifiera sina brottsoffer genom publika hemsidor.
- s66 Brott mot företagare är ett stort problem, likaså när företag används som brottsverktyg.
- s66 Den grova organiserade brottsligheten och dess ekonomi grundar sig fortfarande i stor utsträckning på handel med narkotika.
- s66 Idag kan kriminella tjäna miljardbelopp på bedrägerier, arbetslivskriminalitet och ekonomisk brottslighet, samtidigt som seriösa företag konkurreras ut och skattepengar missbrukas.
- s66 Skjutningar är ofta kopplade till konflikter om kontrollen över försäljning av narkotika i specifika områden.
- s67 Kopplingen mellan barn som utsätts för, eller upplever våld, under sin uppväxt och de som ansluter sig till gängkriminalitet är dessutom mycket stark.
- s68 Den farligaste platsen för en kvinna är hennes eget hem och den farligaste perioden är när hon vågar ta steget och bryta upp.
- s68 Varje år blir 13 kvinnor mördade av en man hon har eller har haft en nära relation med.
- s69 Den nya lagstiftningen har fört med sig att kvinnojourer i hela landet tvingats stänga eller minska sina öppettider.
- s79 Hot och hat måste tas på större allvar, inte minst gentemot transpersoner som idag lever i en mycket utsatt position.

**Försvar och beredskap** (6)

- s5 Samtidigt växer auktoritära krafter globalt och utmanar den regelbaserade världsordning som Sverige byggt sin säkerhet, sin handel och sin frihet på.
- s24 Det gör oss sårbara både ekonomiskt och säkerhetspolitiskt.
- s24 Vårens blockad av Hormuzsundet har visat hur snabbt ett sådant fossilberoende kan slå hårt mot svenskarnas vardag.
- s89 Under lång tid har investeringar varit otillräckliga och förmågan att hantera väpnade angrepp begränsad.
- s90 Idag finns brister i beredskap, samordning och förmåga att hantera störningar. Det gör Sverige mer sårbart vid krig, kriser och hybridhot.
- s91 Sverige är idag beroende av globala leveranskedjor för viktiga varor som livsmedel, läkemedel och energi. Samtidigt är beredskapen och lagren vi idag har otillräckliga för sådana större avbrott.  `avviker`

**Klimat, miljö och energi** (6)

- s24 Det har gjort klimatomställningen dyrare och krångligare än nödvändigt för både hushåll och företag, när alternativen till det fossila egentligen är långsiktigt billigare och säkrare än importerad olja.
- s24 Sverige är idag fortfarande onödigt och skadligt beroende av fossila bränslen i transporter, industri och jordbruket.
- s26 Sverige är världsledande i den gröna industrin.
- s27 Fossilberoendet gör Sverige sårbart, samtidigt som alternativen inte alltid är tillräckligt tillgängliga eller är för dyra.
- s28 Idag bromsas utbyggnaden av osäkra marknadsvillkor, otydliga spelregler, bromsande politik och höga risker.
- s29 Effekterna märks redan i översvämningar, torka, värmeböljor och hot mot dricksvatten.

**Integration och sammanhållning** (4)

- s14 Utrikes födda fastnar i ineffektiva system, långtidsarbetslösa möter stängda dörrar och personer med funktionsnedsättning lämnas utanför arbetsmarknaden.
- s21 Entreprenörer möts av flera års handläggningstider som skrämmer bort dem från att etablera sig i Sverige.
- s72 Rasismen, med angrepp på minoriteter, vardagsrasism och diskriminering, begränsar människors frihet.
- s93 Sveriges migrations- och integrationspolitik fungerar för dåligt. Processer är långsamma, incitamenten svaga och systemen motverkar dem som vill arbeta och bidra.

**Frihet, demokrati och institutioner** (14)

- s5 När också äganderätten steg för steg inskränks, och människor blir osäkra på vad de får göra med sin mark och sina investeringar, minskar viljan att satsa, utveckla och ta ansvar.
- s47 Erfarenheterna ifrån när Barnrättskonventionen blev lag är över lag positiva eftersom det ökat fokus på barnens rättigheter.
- s47 Funktionsrättskonventionen är ratificerad av Sverige, men inte implementerad som lag.
- s50 Centraliserad byråkrati och regelkrångel har byggts upp under lång tid samtidigt som statens närvaro i hela landet nu nedmonteras ännu snabbare när regeringen lägger ner servicekontor.
- s54 Regeringen har stängt servicekontor på många orter och centraliserad byråkrati har byggts upp under lång tid.
- s65 Tilliten till socialtjänsten brister på många håll.
- s72 Även i Sverige ser vi ökad polarisering och misstro, samt förslag som riskerar att försvaga rättssäkerheten och individens skydd mot staten.
- s74 De globala digitala plattformarna har stort inflytande över demokratin i Sverige. De kan styra hur information sprids och förvärra splittringar i samhället, och de är sårbara för desinformation och påverkansoperationer.
- s74 Men i Sverige är den ordningen sårbar eftersom oppositionens inflytande till stor del hänger på praxis.
- s75 Trollfabriker och anonym kommunikation från politiska partier skadar demokratin och det offentliga samtalet.
- s75 Trots att svenskarna är samhällsengagerade är färre med i ett politiskt parti än förut, och en ännu mindre skara vill axla ansvaret som folkvald.
- s76 Men trots det är staten skadeståndsskyldig i alldeles för få fall och skadestånden är alldeles för låga.
- s76 Trots det finns minst 494 exempel i svenska lagar och förordningar som står i strid med rätten till domstolsprövning, där individen inte har rätt att få sin sak prövad i domstol.
- s78 Att kvinnor i många fall tar ett större ansvar för familjen gör det svårare för dem att påverka samhället som fritidspolitiker.

**Utanför de sju kategorierna** (14)

- s4 Det märks när avståndet till vård, jobb eller service ökar lite mer för varje år
- s4 I vissa delar växer möjligheterna, i andra krymper de.
- s4 Sverige blir också alltmer ojämlikt beroende på var du bor.
- s50 Servicen försvinner, skyltfönster släcks ner och välfärden flyttar längre bort.
- s50 Skillnaderna i hälsa ökar, företag möter större hinder och allt fler känner sig bortprioriterade.
- s50 Vi vet också att långt fler, särskilt unga, skulle vilja bo på våra landsbygder, men inte ser att de har möjligheten eftersom samhället drar sig undan.
- s56 Efterfrågan från pendling, godstrafik och klimatsmarta transporter växer snabbt.  `avviker`
- s56 Idag fungerar inte infrastrukturen som den ska.
- s56 Tåg är försenade, vägar förfaller och resor blir dyrare och mer osäkra.
- s72 Samtidigt upplever många människor att friheten i deras vardag hålls tillbaka, av krångliga regler, ekonomisk otrygghet och ett samhälle som inte alltid fungerar.
- s78 Jämställdheten i Sverige har tagit stora steg framåt, men kvinnors frihet begränsas fortfarande i praktiken. Idag ser vi hur löneskillnader består, hur kvinnor tar ett större ansvar för familjen och hur våld och kontroll fortsatt inskränker deras livsutrymme.  `avviker`
- s81 Särskilda insatser krävs för att riva de ekonomiska och strukturella hinder som idag utestänger många paraidrottare.
- s82 Det är bra att det gamla danstillståndet försvunnit men det är inte rimligt att man fortfarande behöver skicka in en anmälan på förhand.
- s82 Efter år av debatt och utredningar levererade regeringen till slut en tillkrånglad gårdsförsäljningsreform.


### V (74)

**Ekonomi och jobb** (35)

- s3 Du som läser det här står inför ett vägval. Efter fyra år med en högerregering som har prioriterat skattesänkningar för de rikaste på vanliga människors bekostnad behöver Sverige en ny politisk inriktning.
- s3 Samtidigt har de som redan hade mest fått ännu mer.
- s5 Det finns idag stora och omotiverade skatteskillnader mellan kommuner och regioner som måste minska.
- s5 I dag ser det inte ut så.
- s10 730 000 svenskar lever i materiell och social fattigdom, en fördubbling jämfört med 2021. Av dessa lever t 400 000 personer i allvarlig materiell och social fattigdom.
- s10 Den ökande fattigdomen beror framför allt på försämringar inom trygghetssystemen och prisökningar.
- s10 Hushållen har drabbats hårt under den gånga mandatperioden.
- s10 Istället har de sänkt skatterna för de som redan har så det räcker.
- s10 Regeringen har inte gjort någonting för de hushåll som har det sämst ställt.
- s11 Bostadsbidraget är ett mycket träffsäkert instrument för att höja inkomsterna för dem som har det sämst ställt.
- s11 Efter år av höga matpriser, stigande hyror och urholkade bidrag har pressen på hushållen ökat kraftigt. Och allra hårdast slår det mot ensamstående barnfamiljerna.
- s11 Studenter har en utsatt ekonomisk situation och har drabbats hårt av prisökningarna
- s12 Bidragstaket slår mot de fattigaste i samhället.
- s12 Den allmänna pensionen är för låg och ger lång under de utlovade 60 procenten av slutlönen.
- s12 Miljardärer betalar ofta lägre andel av sin inkomst i skatt än resten av befolkningen.
- s13 Att två aktörer dominerar marknaden är ett marknadsmisslyckande.
- s13 Bristen på konkurrens på bankmarknaden beror delvis på att det är svårt för kunder att jämföra priser, avgifter och villkor.
- s13 Den svenska dagligvaruhandeln domineras av vertikalt integrerade aktörer där grossister i praktiken kontrollerar sina egna butiker, vilket hindrar butiker från att fritt välja mellan grossister. Detta eliminerar pris- och konkurrenstryck i grossistledet och gör det i praktiken omöjligt att driva en fristående fullsortimentsbutik i Sverige, vilket skadar både konkurrensen och konsumenterna.
- s13 Detta utnyttjas av privata hyresvärdar, som taktiskt använder höga krav för att nå större hyreshöjningar än i förhandling.
- s13 Hushållen får höga bolån, dyra avgifter och nästintill ingen ränta på insatta pengar.
- s13 Idag domineras den svenska bankmarknaden av de fyra storbankerna.
- s13 Sedan 2022 kan tvister gå till skiljeman.
- s14 De många oligopolmarknaderna i Sverige visar att dagens konkurrenslagstiftning bör skärpas.
- s15 I stället för att skapa jobb väljer Tidöregeringen att straffa människor för att de blivit arbetslösa, genom sänkt a-kassa och sänkta bidrag.
- s15 Många kommuner kämpar med bristande service, eftersatt infrastruktur och utflyttning trots att de står för de naturresurser som är avgörande för landets välstånd. Det gäller inte minst de norra delarna av landet som förser Sverige med skog, vattenkraft och malm.
- s15 Problemet är inte att det byggs för mycket, utan att det byggs för dyrt.
- s15 Resultatet är kraftigt minskat bostadsbyggande, trångboddhet och höga hyror som gör att många inte har råd att flytta hemifrån.
- s15 Sverige har i decennier förlitat sig på att marknaden ska lösa bostadsförsörjningen.
- s16 Bara hälften av alla kvinnor med ett arbetaryrke har en fast heltidsanställning.
- s16 Hälften av alla de som arbetar heltid skulle vilja gå upp i tid och jobba heltid.
- s16 Sveriges kommuner och regioner står inför stora investeringsbehov.
- s16 Sveriges kommuner och regioner står inför stora investeringsbehov.
- s18 Alla ska kunna vara säkra på att den lägenhet man hyr och det hus den ligger i tas om hand och underhålls enligt konstens alla regler. Så ser de inte ut idag.
- s18 I stället tjänar riskkapitalbolag och slumvärdar stora pengar på att låta fastigheter förfalla utan åtgärder från det offentliga.
- s20 Men trots att det är Norrland som producerar den energi som genererar störst skatteintäkter kommer inte resurserna kommunerna lokalt till del.

**Välfärd** (32)

- s4 Den svenska välfärden har monterats ned under årtionden.
- s4 Kommuner och regioner tvingas idag lägga en stor del av sina resurser på att kontrollera privata aktörer och stoppa fusk.
- s4 Regeringens svar har varit otillräckligt, närmast obefintligt.
- s4 Under senare år har dessutom kriminella aktörer klivit in i välfärden. De stjäl våra gemensamma resurser som skulle ha gått till vård och omsorg och använder dessa pengar i sin brottsliga verksamhet samtidigt som de rekryterar barn till kriminalitet.
- s4 Underfinansiering har i kombination med privata aktörers intåg och expansion inom välfärden lett till minskade resurser, sämre arbetsvillkor och färre kollegor.
- s5 Kvinnor som arbetar i vår gemensamma välfärd halkar efter allt mer i löneutvecklingen.
- s5 Trots höga krav, stort ansvar och avgörande samhällsinsatser tjänar kvinnor i kvinnodominerade välfärdsyrken fortfarande tusentals kronor mindre i månaden än män i likvärdiga yrken.
- s6 I stället ser vi allt fler exempel runt om i landet där klassernas storlek ökar för att i kommunerna spara pengar eller i friskolorna för att kunna ta ut mer vinst.
- s6 Många patienter möter i dag långa väntetider, bristande kontinuitet och för få behandlingsalternativ.
- s6 Många unga vuxna slutar att besöka tandvården i förebyggande syfte när de inte längre har tillgång till avgiftsfri tandvård.
- s6 När hyror, mat och andra nödvändiga utgifter blivit dyrare har regeringen gjort det ännu dyrare att vara sjuk.
- s6 Psykiatrin fungerar inte i Sverige.
- s7 I dag saknas dock riktmärken för hur stora grupper som är rimliga och hur mycket personal som bör finnas.
- s7 Många barn börjar och slutar sin dag på fritidshemmet.
- s7 Skolans uppdrag försvåras av den ökade ojämlikheten.
- s8 Dagens system gör det möjligt för företag att etablera sig i den region som har högst ersättningsnivåer och sedan ta lika mycket betalt i hela landet.
- s8 Den sätter käppar i hjulen när kommuner och regioner vill prioritera och planera sin verksamhet och släpper lös hemtjänstaktörer och vårdcentraler utan kostnadskontroll.
- s8 En tydlig majoritet av svenskarna säger nej till vinstutdelning i skattefinansierad vård, skola och omsorg.
- s8 Lagen om valfrihet i vården bidrar till att skapa markandskaos och överetablering.
- s8 Nätläkarbolag och andra privata vårdföretag har kunnat växa i ett system som saknar tillräcklig kontroll och där stora summor skattemedel varje år går till vinster och överetableringar.
- s8 Nätläkare i sin nuvarande form urholkar vården och minskar resurserna för de patienter som behöver vården mest.
- s8 Personal på äldreboenden går på knäna, äldre får inte alltid den omsorg de behöver och samtidigt försvinner miljarder skattekronor till privata vinster. Detsamma gäller inom skolan om sjukvården.
- s8 Privata sjukvårdsförsäkringar skapar en ojämlik vård där betalningsförmåga går före medicinskt behov.
- s8 Svensk välfärd befinner sig i kris.
- s8 Vänsterpartiet menar att resurser som i dag försvinner till vinster och marknadsstyrning i stället behövs för att stärka välfärden.
- s9 Experimentet med vinstdrivande fristående skolor har tillåtits pågå alltför länge, på bekostnad av tusentals elevers skolgång och framtid.
- s9 Idag ger Skolinspektionen tillstånd till skoletableringar och kommuner är remissinstanser.
- s9 Regeringens reform för värdeöverföringar är otillräcklig.
- s9 Skolinspektionen tar i praktiken inte hänsyn till behovet av nya skolplatser.
- s9 Vänsterpartiet anser att dagens system för skolpeng är djupt orättvist eftersom kommunala skolor har ett lagstadgat och mer omfattande ansvar.
- s12 Flera av förslagen som då utreddes genomfördes aldrig.
- s12 Sjukförsäkringen förstärktes under mandatperioden 2018-2022.

**Utanför de sju kategorierna** (7)

- s15 Det har bidragit till förseningar och tågkaos.
- s15 Järnvägssystemet i Sverige är idag uppsplittrat mellan en mängd aktörer utan helhetsansvar.
- s16 Många offentliga byggnader har liksom vatten- och avloppsledningar runtom i landet nått slutet på sin tekniska livslängd.
- s18 Ansvaret för järnvägen är idag uppdelat på flera myndigheter och privata aktörer.
- s18 Det gör att helhetsansvaret går förlorat och kortsiktiga vinstintressen går före en fungerande tågtrafik.
- s18 Många järnvägssträckor är redan idag överbelastade och underhållsskulden är enorm.
- s18 Sveriges kommuner och regioner har stora behov av att rusta upp gammal infrastruktur som vatten- och avloppssystem, vägar och byggnader.


### KD (45)

**Ekonomi och jobb** (14)

- s2 Alltför många har svårt att få ekonomin att gå ihop.
- s3 Boendet är för många satt under ekonomisk press.
- s3 Kostnaden för ett bygglov varierar stort mellan landets kommuner, vilket är helt orimligt.
- s3 Reavinstskatten är i praktiken en flyttskatt som gör att människor bor kvar i för stora eller felanpassade bostäder då flytten utlöser en skattesmäll.
- s3 Staten har alltid varit frestad att använda boendet som stabil skattebas.
- s6 Sverige hålls tillbaka av överregleringar.
- s6 Trots att vi under de senaste åren gjort flera förenklingar och investeringar, dras vi fortfarande med problem som orsakats av en bristande politisk vilja att prioritera innovation och entreprenörskap, infrastruktur och etableringar.
- s7 Att företag får goda förutsättningar betyder alltså också att ge förutsättningar för ett gott samhälle, välfärd och växande ekonomi.
- s7 Det är här basen byggs för människors privatekonomi och för finansieringen av vår gemensamma välfärd.
- s7 Det är i de små och växande företagen som de nya jobben skapas.
- s7 För många är drömmen om ett eget företag också drömmen om frihet och att förverkliga sig själv eller sin idé.
- s7 Företagare skapar service, tar ofta socialt ansvar och skapar mötesplatser och livskraft i lokalsamhällen.
- s7 Här formas nästa exportsuccé och här föds innovationer.
- s7 Här får många unga chansen att få sitt första jobb.

**Välfärd** (10)

- s2 Alltför många människor väntar med oro på vård.
- s2 Alltför många unga mår dåligt och tappar hoppet.
- s2 Men vi ser också allt som fortfarande brister.
- s4 1862. Det var året då svensk sjukvård senast reformerades.
- s4 När den är som sämst präglas vården av köer och av ojämlikhet.
- s4 När vården är som bäst är den i världsklass.
- s4 Sveriges hälso- och sjukvård står inför stora utmaningar.
- s4 Vårdgarantin i barn- och ungdomspsykiatrin blir nu lag och väntetiderna måste vara korta.
- s5 En stark svensk värdering är att alla ska kunna känna sig trygga med att vården, skolan och omsorgen fungerar och inte är en fråga om pengar, kontakter eller social status.
- s5 Svensk välfärd består av många delar.

**Lag och trygghet** (1)

- s9 Samhällsgemenskapen utmanas och försvagas.

**Klimat, miljö och energi** (2)

- s7 Svensk mat är dessutom producerad med ett stort ansvarstagande för både djur och natur.
- s7 Sverige har en fantastisk natur som ger förutsättningar för livskraftigt jordbruk, skogsbruk, fiske och jakt.

**Frihet, demokrati och institutioner** (4)

- s6 Återkommande kriser och en ökad politisk polarisering tycks ha resulterat i passivitet och brist på ambitioner för det gemensamma bästa.
- s8 De utmanas ständigt.
- s8 Svenska makthavare och opinionsbildare har alltför länge förminskat och ibland förnekat det som är Sveriges värdegrund.
- s9 En allt större fara mot goda värderingar är också sociala medier och andra sammanhang på nätet som nyttjas för att såväl polarisera, sprida desinformation som att mata barn och unga med värderingar som skadar deras självkänsla och möjlighet till hälsa och utveckling.

**Utanför de sju kategorierna** (14)

- s3 De senaste decennierna har det rullats ut bostadsmattor, men vi behöver bygga mer genomtänkta stadsdelar.
- s3 Detta har Sverige förutsättningarna till.
- s3 Då var tanken - som fortfarande håller i sina grunder - att bygga villor och radhus i ett större område, tillsammans med låga flerfamiljshus, vilket ger underlag för ett lokalsamhälle med skola, torg, parker, samlingslokaler, idrottsytor och mindre affärsverksamheter.
- s3 Endast tre procent av Sveriges yta är bebyggd mark.
- s3 Här finns utrymme för nytänkande och modernitet, men förebilden finns i de trädgårdsstäder som byggdes för runt 100 år sedan på flera platser runt om i Sverige.
- s3 Undersökningar visar att de flesta svenskar vill bo i villa eller radhus.
- s6 Arbetet med att bygga Sverige starkt går för långsamt.
- s6 I dag kan en enskild fågel eller en liten planta sätta stopp för viktiga investeringar.
- s6 Sverige står inför en period där vi behöver rusta samhället starkare.
- s7 Det finns delar av Sverige som ofta glöms bort, inte bara i debatten utan även i de politiska beslut som fattas.
- s7 På samma sätt som stadens villaförort och utanförskapsområden skiljer sig från varandra, finns det flera olika landsbygder och glesbygder.
- s7 Svenska bönder är ett föredöme i världen.
- s7 Sverige ser olika ut på olika platser.
- s7 Ändå talas det ofta om landsbygd på ett förenklat sätt som förminskar vårt lands mångfald och människorna som bor på landsbygden.


### MP (24)

**Ekonomi och jobb** (5)

- s3 Sverige är ett land med långa avstånd och en fungerande infrastruktur är helt avgörande för att det ska gå att arbeta och bo i hela landet.
- s3 Utbyggnaden och underhållet av järnvägen har misskötts under lång tid. Det har lett till dyrare biljetter, fler inställda avgångar, stora förseningar och överfyllda tåg.
- s4 Miljardärerna blir rikare medan andra har svårt att få hushållsekonomin att gå ihop.
- s4 Många har idag svårt att klara vardagen.
- s5 Idag står många utan jobb samtidigt som andra jobbar så mycket att de inte orkar ett helt arbetsliv.

**Välfärd** (4)

- s4 Misslyckade marknadslösningar leder till att pengar hamnar hos aktieägare istället för att gå till barn, sjuka och äldre.
- s4 Sverige har alla förutsättningar för att vara ett bra land för alla - oavsett varifrån du kommer eller hur mycket pengar du har. Men idag är verkligheten en annan.
- s5 Hälsoskillnaderna är stora.
- s5 I Sverige ska du kunna lita på att få bra vård, omsorg och assistans - oavsett var du bor och hur mycket du tjänar. Så ser det inte ut idag.

**Lag och trygghet** (2)

- s7 Geopolitiska spänningar, demokratisk tillbakagång, organiserad brottslighet och våldsbejakande extremism påverkar vår trygghet och säkerhet.
- s8 När hat, våld och kriminalitet ökar hotas människors frihet och tilliten i samhället.

**Försvar och beredskap** (3)

- s7 Sverige och Europa befinner sig i ett allvarligt säkerhetspolitiskt läge.
- s7 Vi lever i en orolig tid och en osäker omvärld.
- s9 Krig, klimatkris och konflikter påverkar inte bara människor långt bort, det märks också här, i vår vardag, genom högre priser och ökad osäkerhet över framtiden.

**Klimat, miljö och energi** (7)

- s2 De som tjänar på vårt fossilberoende är stater som Ryssland, Saudiarabien och Iran.
- s2 Efter fyra år med Tidöregeringen är resultaten förödande.
- s2 Läget är akut och fönstret för att agera är nu.
- s6 Idag hotas den biologiska mångfalden både av hur vi människor använder naturen och av klimatförändringarna.
- s6 När skyddet monteras ner märks det i vår vardag: i det vi äter, det vi dricker och den natur vi har omkring oss.
- s6 Trots det töms våra hav på fisk, enorma kalhyggen breder ut sig och vår mat och vårt dricksvatten förgiftas av miljögifter.
- s6 Även i våra stadsmiljöer finns stor potential att odla mer lokalt.

**Frihet, demokrati och institutioner** (2)

- s8 När kvinnors och HBTQI-personers rättigheter attackeras, rasism och extremism ökar och civilsamhället pressas tillbaka försvagas vårt öppna samhälle.
- s8 Runt om i världen och i Sverige utmanas demokratin från flera håll.

**Utanför de sju kategorierna** (1)

- s2 Sverige har allt som krävs för att vara ett bra land att leva i.


### L (85)

**Ekonomi och jobb** (20)

- s5 Samtidigt har föräldrar med de lägsta inkomsterna svårt att få pengarna att räcka till allt det där som barnen behöver: terminsavgiften för fotbollsträningen, nya gympaskor eller vinterkläder i lagom storlek.
- s15 Företag hindras från att växa när de inte hittar rätt personal.
- s15 Händelser i en orolig omvärld märks nu direkt i svenskarnas hushållskassor.
- s15 Jobbskapare hindras av byråkrati.
- s15 Samtidigt är många människor arbetslösa och fastnar i passivitet.
- s15 Skatten på arbete är fortfarande för hög.
- s15 Sverige är ett rikt land tack vare alla människor som jobbar, driver företag och tänker nytt. Men det finns flera hot mot vårt välstånd.  `avviker`
- s15 Under snart fyra år i regering har vi sänkt skatterna på lönen, pensionen, sparandet, maten och elen.
- s16 Det är framgångsrika företagare som gjort Sverige rikt.
- s16 Euron gör att handeln blir enklare och att svenska företag slipper risken med den skakiga kronan, samtidigt som Sverige sitter med vid bordet när viktiga beslut fattas.
- s16 I dag går alldeles för mycket arbetstid till rapportering och interna processer som ger liten nytta.
- s16 I dag står många arbetslösa medan företagen ropar efter yrkeskunnig personal.
- s16 I en orolig omvärld växer eurons betydelse som stabil världsvaluta, och nu är det hög tid för Sverige att införa den gemensamma valutan.
- s19 Många barnfamiljer pressas av att pengarna ska räcka till.
- s19 Och när bostadsmarknaden är stängd för den som är ung eller ska flytta till ett nytt jobb är det svårt att få framtidsplanerna att gå i lås.
- s19 Under snart fyra år i regering har vi sänkt skatten för dig som jobbar, så att du kan bestämma över en större del av din inkomst.
- s20 Det byggs för lite och det är för svårt att komma in på den svenska bostadsmarknaden.
- s20 Krångliga byggregler och dålig konkurrens gör att det ofta är dyrt och svårt att bygga där människor vill bo.
- s31 Frihandel, mänskliga kontakter och nyfikenhet på omvärlden är en del av det som gör vårt land rikt.
- s31 Sverige är byggt på öppenhet mot världen.

**Välfärd** (34)

- s5 Förskolor där barngrupperna är för stora.
- s5 Kriser för förlossningsvården i både storstad och glesbygd.
- s5 Många barn växer upp i en tillvaro där skärmarna tränger undan allt annat som är viktigt. Resultatet blir att allt fler unga fastnar i en värld fylld av likes och scrollande.
- s5 Och unga som inte får det stöd de behöver, trots tydliga risksignaler.
- s5 Sverige är ett bra land att växa upp i. Men samtidigt finns det brister som drabbar barn och unga.
- s6 Allt fler unga, både tjejer och killar, mår psykiskt dåligt men får inte den hjälp de behöver.
- s6 De orimliga väntetiderna till BUP måste kortas och varje barn som besöker BUP ska ha rätt till en personlig vårdkontakt.
- s6 I dag växer många barn upp i en oreglerad digital värld där få vuxna har insyn och där unkna värderingar sprids, samtidigt som sömn, lek och kompisliv trängs undan.
- s9 Alldeles för många lämnar skolan utan att kunna läsa och skriva tillräckligt bra.
- s9 I stället för fokus på kunskap har vi fått ett system där elevernas behov alldeles för ofta prioriteras bort av kommuner eller aktiebolag.
- s9 Mycket är bra i svensk skola, men mycket måste bli bättre.
- s9 Och när AI är vardag blir det ännu viktigare att varje ung människa får med sig de kunskaper som behövs för att vara källkritisk.
- s9 Stora klasser, stökiga klassrum och skärmar har trängt undan den lärarledda undervisningen.
- s10 I dag drabbas hela klasser ofta av stökiga miljöer, samtidigt som elever som behöver extra stöd blir utan hjälp.
- s10 Så kan Sverige gå från sämst klassrumsdisciplin i Europa till bäst i Norden.
- s10 Överfulla klasser gör det svårt att skapa arbetsro och ge stöd i tid.
- s11 I dag finns det för många kurser i gymnasiet, vilket gör att elever ofta väljer det som lätt ger höga betyg i stället för att läsa mer krävande ämnen.
- s11 I dag känner vissa föräldrar knappt till möjligheten att välja skola till sina barn.
- s11 I dag sitter många barn framför skärmar i stället för att springa, klättra och cykla.
- s19 Att kombinera föräldraskap och jobb ställer krav som ofta gör vardagen till en balansakt.
- s19 I flera större städer har partierna till vänster försämrat kollektivtrafik och vård, och klarar inte ens av att få snöskottningen att fungera.
- s19 Vardagslivet kan vara fantastiskt. Men det kan vara svårt att få vardagen att gå ihop när tiden är för knapp och marginalerna för små.
- s20 Nästan var femte vuxen, oftast en kvinna, vårdar eller stöttar en närstående. Men den som jobbar kläms mellan omöjliga krav, och den som behöver avlastning blir ofta utan.
- s24 Men i dag ser samhällets stöd olika ut beroende på var i landet du bor
- s27 Den som behöver stöttning på äldre dagar möts ständigt av nya ansikten i hemtjänsten.
- s27 Låga ambitioner i äldreomsorgen gör att många inte kommer ut i friska luften eller ens kan besöka sin partners grav när de vill.
- s27 Men det finns också stora luckor.
- s27 När och hur du får vård beror alltför ofta på ditt postnummer.
- s27 Och den som lider av psykisk ohälsa får stå i kö i stället för att få hjälp när den behövs.
- s27 Samtidigt har många som använder LSS under lång tid mött försämringar och indraget stöd.
- s27 Visst har Sverige ett socialt skyddsnät att vara stolt över.
- s27 Vårdcentraler dras in och ätstörningsvård monteras ner samtidigt som vårdens personal drunknar i administration.
- s28 Ingen ska behöva avstå från tandläkarbesöket av ekonomiska skäl, men i dag kan en behandling gräva djupa hål i plånboken.
- s28 Liberalerna drev igenom assistansreformen på 90-talet, och nu är det hög tid för en ny LSS-reform som reparerar hålen efter många års försämringar.

**Lag och trygghet** (8)

- s23 Alldeles för länge gjordes alldeles för lite för att bekämpa brotten och dess orsaker.
- s23 Gängbrott, skjutningar och sprängningar, och bedrägerier mot äldre har gjort att människor tvingas anpassa sig och krympa sin frihet.
- s23 Tryggheten måste också öka där många av dagens övergrepp sker: i hemmet och på nätet.
- s23 Under många år har brottsligheten fått bita sig fast.
- s24 Sverige ska inte tillbaka till en naiv politik där de kriminellas rättigheter gått före brottsoffrets rätt till upprättelse.
- s24 Vi vill utrota gängbrottsligheten: inom fem år ska vi ha gjort upp med det Sverige som präglats av att det skjuts och sprängs.
- s25 Alltför många kvinnor utsätts för sexuella trakasserier, övergrepp och våld utan att samhället reagerar.
- s25 Bedrägerier mot äldre ökar snabbt och kan tömma ett helt livs besparingar, och därför behöver vi skärpa kraven på bankerna att förebygga brott och ta ansvar när kunder drabbas.

**Försvar och beredskap** (1)

- s32 Sveriges och Europas stora beroende av digital teknik från andra delar av världen gör oss sårbara för cyberhot och påtryckningar.

**Klimat, miljö och energi** (1)

- s15 Energisystemet har tagit stryk av tidigare regeringars experimenterande.

**Integration och sammanhållning** (6)

- s5 Barn som aldrig får en ordentlig möjlighet att lära sig det svenska språket.
- s15 Samtidigt tänker vi sätta stopp för den exploatering av människor som har brett ut sig när skuggsamhället har tillåtits växa.
- s24 Nära en kvarts miljon unga i Sverige lever under kontroll, hot och tvång som begränsar deras liv.
- s35 Det sker efter en lång tid med hög invandring och en integration som inte fungerat tillräckligt väl.
- s35 Hundratusentals barn växer upp i områden där utanförskap, parallellsamhällen och hedersförtryck begränsar deras frihet.
- s36 I dag begränsar islamism, klanstrukturer och hedersförtryck människors frihet på många håll i Sverige.

**Frihet, demokrati och institutioner** (12)

- s3 Länge styrdes Sverige av politiker som lät stora samhällsproblem växa. Men för fyra år sedan fick vi väljarnas förtroende att göra något åt detta. Sedan dess tar vi ansvar.
- s3 Sverige står nu inför ett viktigt val: mer liberalism, eller en sväng mot vänster.
- s3 Under de senaste åren har vi klarat av att kombinera att föra politik mot stora hot som Ryssland och ekonomisk oro med liberala hjärtefrågor som att sätta skolan först, stärka arbetet mot hedersrelaterat förtryck och se till att fler har råd att spara för framtiden. Allt detta samtidigt som vi visat att vi klarar av att göra ekonomiska prioriteringar och stärka arbetslinjen.
- s3 Äntligen grundlagsskyddas aborträtten och äntligen kan homosexuella män donera blod.
- s35 Attityderna mot hbtqi-personer hårdnar bland unga, antisemitism uttrycks alltmer öppet och kulturinstiutioner tvekar att visa sådant som kan uppfattas som kontroversiellt.
- s35 Frihet, demokrati och jämställdhet är självklarheter för de flesta i vårt land. Men inte för alla.
- s35 När algoritmer styr nyhetsflödet och desinformation sprids ökar polariseringen.
- s35 Samtidigt ser vi hur intoleransen ökar.
- s36 Men rasism och antisemitism fortsätter att drabba människor, och särskilt för judar har situationen förvärrats.
- s36 Och även om vår svenska demokrati står stark behöver vi stärka rättsstaten så att dina rättigheter alltid försvaras.
- s36 Regimer som Eritrea, Ryssland, Iran och Kina använder föreningar, propaganda och hot för att övervaka, kontrollera och kräva pengar av människor som bor i vårt land.
- s36 Våra folkbibliotek fungerar som hubbar för kunskap och bildning i hela landet, men samtidigt sparar många kommuner in på biblioteken.

**Utanför de sju kategorierna** (3)

- s3 Äntligen har det blivit lättare att bygga på en strandtomt och äntligen avskaffas matkravet på krogen.
- s19 På landsbygden är igenbommad service, potthål och nedsläckt vägbelysning alldeles för ofta en del av vardagen.
- s19 Samtidigt ska vi städa bland onödiga regler som har tillåtits växa under tidigare regeringar.
