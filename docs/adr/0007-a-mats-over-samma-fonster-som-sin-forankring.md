# ADR 0007: A mäts över samma fönster som sin förankring

- Status: accepted
- Datum: 2026-08-21
- Beslutad i: biljett [#25](https://github.com/mcknschn/rosta/issues/25) under karta [#6](https://github.com/mcknschn/rosta/issues/6)
- Bygger på: [ADR 0002](0002-kategoripoangens-ansprak-och-vikter.md), [ADR 0003](0003-skiljbarhet-och-kanslighetsanalys.md) och [ADR 0005](0005-a-forankras-i-tid-inte-i-faltet.md)

## Kontext

Biljett #25 graderades ur omkörningen i [#21](https://github.com/mcknschn/rosta/issues/21), alltså
bygget av ADR 0005. Efter den slicen ger A ungefär 2,5 till alla åtta partier. A:s viktade spridning
gick från 7,76 till 0,80, alltså från 61,4 till 14,1 procent av separationen.

Biljetten ställde frågan spegelvänt mot ADR 0003 punkt 1, som skrev att "en delpoäng som ger 5,00
till alla åtta partier mäter ingenting". Är tystnaden ett riktigt fynd om världen, alltså att de
åtta faktiskt föreslår nästan samma sak? Eller är den ett artefakt av formen?

## Diagnos

Mätt 2026-08-21 mot `dist/scores.json`, `config/` och `pipeline/`.

1. **Kompressionen är verklig, och A är tunnast av de tre.** Ingen delpoäng använder mycket av
   skalan, men A använder minst.

   | Delpoäng | Realiserat intervall | Andel av skalan per kategori | Viktad spridning |
   | --- | --- | --- | --- |
   | A | 2,17 - 3,07 | 2,4 % till 15,2 % | 0,798 |
   | B | 2,26 - 4,00 | 12,1 % till 34,7 % | 3,544 |
   | D | 2,34 - 3,83 | 9,9 % till 27,4 % | 1,337 |

2. **Biljettens eget prov kan inte falla.** Biljetten föreslog att pröva om A:s spridning följer det
   råa underlagets spridning. A är per konstruktion en monoton funktion av kvoten mellan andelen och
   förankringen. Alltså följer A:s spridning alltid underlagets, i varje tänkbar värld. Provet
   skiljer inte ett fynd från ett artefakt, och det stryks i beslutspunkt 7.

3. **Täljaren och förankringen mäts över olika fönster.** Förankringen ligger på fönstret 2011-2025
   i `config/a_forankring.yaml`. Täljaren gör inte det. a1:s täljare i `config/budget_ramar.yaml`
   har tre budgetår, 2023, 2024 och 2025. a2:s täljare hämtas över 2014-09-01 till 2026-05-29
   (`pipeline/sources/riksdagen.py`, `fetch_motion_counts`), medan a2:s förankring täcker
   2011-01-01 till 2025-12-31. En kvot vars täljare och nämnare täcker olika år bär skillnaden
   mellan åren som om den vore en skillnad mellan partier.

4. **a1 ger fyra partier exakt samma tal, och det följer av fönstret.** I alla tre budgetåren i
   configen står M, KD, L och SD på `frame: regeringen`. a1 väger 0,6 av A. Alltså kan 60 procent
   av A inte skilja halva fältet åt i någon kategori. ADR 0005 skrev ut den begränsningen som ett
   korrekt påstående om verkligheten, och det är den för de tre åren. Den är inte ett korrekt
   påstående om de femton, eftersom de fyra partierna lade egna budgetmotioner under de år de inte
   regerade tillsammans.

5. **ADR 0005 punkt 7 är tvetydig, inte överträdd.** Punkten heter "Ett gemensamt fönster" och
   sätter två gränser, en för a1 och en för a2. "Gemensamt" går att läsa som gemensamt mellan de två
   halvorna, vilket är hur bygget läste det, och lika väl som gemensamt mellan täljare och
   förankring. Samma ADR:s avsnitt "Vad beslutet inte rör" lämnar dessutom uttryckligen
   partiramarna för "de år som betygsätts" orörda. Bygget följde alltså ADR:n troget. Det som
   återstår är ett beslut, inte en rättelse.

6. **Avbildningens växelkurs har aldrig beslutats.** `q = (andel - förankring)/(andel + förankring)`
   följt av `net_support_to_score` är `2,5 x (1 + tanh(ln r / 2))`, där `r` är andelen delad med
   förankringen. Avbildningen är symmetrisk i log: en fördubblad andel ger +0,83 poäng, en halverad
   ger -0,83. Talet 0,83 ärvdes när ADR 0005 lånade B:s avbildning, och det var rätt val då,
   eftersom alternativet var en vald konstant. Realiserat `r` ligger mellan 0,77 och 1,59.

Svaret på biljettens fråga är därmed **båda läsningarna, men inte i lika delar**. De åtta föreslår
verkligen andelar nära den historiska normen, och det ska A rapportera. Men en mätbar del av
tystnaden sitter i fönstret och inte i världen, och den delen går inte att skilja ut förrän
fönstren är lika.

## Beslut

1. **Fönstret styr täljaren, inte bara förankringen.** En kvot mäter en skillnad mellan år om dess
   täljare och nämnare täcker olika år. Det är aritmetik och inte en avvägning. Kravet gäller båda
   halvorna: a1:s täljare täcker samma år som a1:s förankring, och a2:s täljare samma period som
   a2:s förankring.

2. **En tredje gräns, av samma sort som de två i ADR 0005 punkt 7.** Gränsen är: **tidigaste
   budgetår där alla åtta partier har en citerbar ram som listar utgiftsområde 1-27.** Citerbar
   betyder egen budgetmotion, regeringsställning, eller uppslutning bakom en gemensam ram belagd med
   votering. Det är ordagrant den attributionsregel `config/budget_ramar.yaml` redan följer, och den
   prövas på källan och inte på ett omdöme. Gränsen skrivs före hämtningen och rörs inte efteråt.
   a1:s fönster börjar vid den senaste av a1:s gränser och slutar vid senaste färdiga år.

3. **Ett fönster per halva, inte ett för hela A.** ADR 0005 punkt 7 lade halvorna på ett gemensamt
   fönster. Den kopplingen är en bekvämlighet utan aritmetisk kraft: a1 och a2 är skilda kvoter ur
   skilda källor, var och en avbildad på [0, 5] för sig innan de vägs samman 0,6 mot 0,4. Kravet i
   punkt 1 är det som binder. Med ett gemensamt fönster skulle dessutom a1:s tillgänglighet avgöra
   om a2 finns, alltså skulle en lucka i budgetkällan kasta bort motionsår som är fullt giltiga.

4. **Villkorsklausul mot en nollpunkt som tillhör ett block.** **a1 är otillåten om något partis ram
   sammanfaller med den antagna ramen i varje år i fönstret.** Faller klausulen ut, faller a1 ur A
   för alla kategorier, och A blir a2 ensam. Klausulen är ADR 0005:s förkastade alternativ
   "Regeringens ram som nollpunkt" skrivet som ett prov. Utan den kan ett kort a1-fönster återinföra
   det förkastade bakvägen: med enbart 2023-2025 är den antagna ramen regeringens, och M, KD, L och
   SD landar då på exakt 2,5 i varje kategori av konstruktion. I fönstret 2011-2025 klarar a1
   provet, eftersom `adopted` växlar mellan utskottet, reservationen, reservation 5 och utskottets
   eget förslag.

5. **Grinden i `pipeline/budget.py` lämnas orörd.** Grinden är ett snitt över åren: en kategori är
   a1-aktiv bara om alla åtta partier har ram för varje UO i kategorin i varje inkluderat år. Med
   femton år är den skör, eftersom ett ofullständigt år släcker kategorin överallt. Gränsen i punkt
   2 bär kravet i stället, så att varje år i fönstret är fullständigt av konstruktion, och grinden
   står kvar som skyddsnät. Att lossa grinden till per år förkastades: det skulle ge olika
   kategorier olika fönster i samma andetag som punkt 1 beslutas.

6. **Avbildningen lämnas orörd, och dess växelkurs skrivs ut.** Metodrutan säger vad en poäng i A
   betyder, alltså att en fördubblad andel ger 0,83 poäng, och vilket intervall A kan nå. Skälet att
   inte röra avbildningen nu är att en mätbar del av kompressionen sitter i fönstret. Att skala om
   avbildningen före omkörningen vore att laga fel sak, och skalan skulle mätas mot ett underlag som
   är ett enda regeringsår upprepat tre gånger. Reserven, om kompressionen står kvar efteråt, står i
   Övervägda alternativ.

7. **Biljettens eget prov stryks.** Frågan "följer A:s spridning underlagets spridning" ersätts av
   frågan "hur stor omfördelning krävs för att flytta A en poäng". Den senare är prövbar, den tittar
   aldrig på rangordningen, och det är den storhet som faktiskt är obeslutad.

8. **Blindheten deklareras.** Den som beslutade hade sett A:s nuvarande värden, spridningarna i
   diagnosen ovan och den publicerade rangordningen. Vad det här beslutet gör med A:s värden och med
   rangordningen räknades inte ut innan ADR:n skrevs, och går inte att räkna ut, eftersom talen inte
   finns förrän ramtalen är transkriberade. Deklarationen finns för att påståendet "jag höll mig
   objektiv" är oprövbart när talen är kända, precis som ADR 0005 punkt 8 skrev samma sak om sig
   själv.

## Godkännandetest

Ett regeltest, aldrig ett tal om spridning eller rangordning. ADR 0003 punkt 1 förbjuder ökad
separation som mål.

1. **Kodtest:** för varje parti och kategori täcker a1:s täljare exakt a1:s förankringsår, och a2:s
   täljare exakt a2:s förankringsperiod. Annars hård fail.
2. **Klausulen i beslutspunkt 4 som prov**, körd på det fönster som faller ut.
3. **De tre gränserna skrivs före hämtningen**, och de år som faller ut skrivs till en bevisfil, som
   `docs/done/a_forankring/fonster.json` redan gör.
4. **Inget tal om spridning eller rangordning ingår i testet.**

Vid sidan av testet står leveransen ur beslutspunkt 6: metodrutan säger vad en poäng i A betyder.

## Övervägda alternativ

- **Skala `q` mot förankringens egen historiska spridning över fönstret.** Sparad som reserv, inte
  förkastad. Konstanten skulle härledas ur samma fönster och samma källa som förankringen, alltså
  ingen vald konstant, och A skulle bli jämförbar mellan kategorier. Den prövas om kompressionen
  står kvar när fönstren är lika. Att pröva den nu vore att mäta skalan mot ett underlag där fyra
  partier delar ram i varje år.

  **Prövad och förkastad 2026-08-30 av
  [ADR 0012](0012-vaxelkursen-i-a-ar-harledd-ur-kvotens-andar.md) punkt 3** (biljett
  [#28](https://github.com/mcknschn/rosta/issues/28)). Reserven är alltså inte längre sparad. Båda
  leden i skälet ovan föll: konstanten är inte en utan tre, och valet mellan dem flyttar de två
  översta partierna, medan storheten mäter hur mycket budgetpolitiken ändrats över femton år och
  inte hur väl talet är känt.
- **Korta förankringen till täljarens tre år.** Förkastat. Förankringen blir då de tre
  Tidöbudgetarna, alltså M, KD, L och SD:s egen ram, vilket är det alternativ ADR 0005 förkastade
  under rubriken "Regeringens ram som nollpunkt". Beslutspunkt 4 gör förkastandet prövbart.
- **Ett kortare gemensamt fönster av kostnadsskäl.** Förkastat. ADR 0005 punkt 7 skriver att
  gränserna är krav som faller ut, och att ett efterhandsomdöme av typen "kvalitén var för dålig
  före år X" är otillåtet. Att välja fönster efter hur dyr transkriberingen är, är samma sorts
  omdöme.
- **Lossa a1-grinden till per år.** Förkastat, se beslutspunkt 5.
- **Flytta A:s vikt 0,30.** Förkastat på samma grund som i ADR 0005: vikterna är låsta i ADR 0002,
  och att ändra en vikt därför att delpoängen separerar för lite är precis den koppling mellan vikt
  och utfall som prövningsregeln i ADR 0003 punkt 1 förbjuder.
- **Låta A modulera B i stället för att adderas till B.** Utanför rutten. ADR 0002 punkt 3 gav A
  dess vikt med en multiplikativ tanke, alltså att kraften skalar effekten, medan formeln är
  additiv. Att riva den formen kräver att ADR 0002 rivs, alltså en annan karta med en annan
  destination. Ligger som en rad under Out of scope på karta #6.

## Vad beslutet inte rör

- Vikterna 0,30 x A + 0,50 x B + 0,20 x D, C = 0 (ADR 0002).
- Blandningen 0,6 x a1 + 0,4 x a2.
- Avbildningen `net_support_to_score` och den begränsade kvoten (ADR 0005 punkt 4).
- Förankringarnas källor: de beslutade FiU1-ramarna för a1 och kammarens samtliga motioner för a2
  (ADR 0005 punkt 5).
- B, C och D. ADR 0004 och ADR 0006 står oförändrade.
- Rangnormaliseringen av A är fortsatt förbjuden (ADR 0005 punkt 1).

## Följder

- **Bygget är en egen slice.** Den här ADR:n ändrar ingen kod och ingen config. Rangordningen är
  oförändrad tills slicen körs.
- **Ny hämtning krävs på båda halvorna.** a1 behöver partikolumnerna ur samma FiU1-rambeslutstabell
  som förankringen redan läser för varje år 2011-2025, alltså "Regeringens förslag" plus "Avvikelse
  från regeringen" per parti. Dokumentet är uppslaget för alla femton åren, och 2023 och 2024 gick
  programmatiskt ur den officiella HTML-källan enligt `docs/done/fas1b_budget_metod.md`. a2 behöver
  motionsräkningen hämtad om över den nya perioden, ungefär 120 anrop mot data.riksdagen.se.
- **Attributionen per år måste skrivas ut, aldrig gissas.** Varje parti får en `frame` per år med
  sin källrad, enligt regeln i beslutspunkt 2. Ett parti utan egen ram och utan citerbar uppslutning
  bakom en gemensam ram utelämnas, vilket flyttar gränsen framåt. Åren 2020 och 2021 är den kända
  osäkerheten, eftersom C och L stod bakom en budget de inte lade själva.
- **Kända kostnader, alla skrivna i förväg.** Ett långt a1-fönster blandar ett partis regeringsår
  med dess oppositionsår, och för ett regeringsparti är ramen koalitionens och inte partiets egen.
  Halvorna kan hamna på olika fönster, så A kan blanda två tidsavsnitt, och det ska stå i
  metodrutan. Gränsen i beslutspunkt 2 kan falla ut sent, och då faller a1 ur A enligt punkt 4.
- **Domen över kompressionen faller inte här.** Om A är tyst även när fönstren är lika, då är
  tystnaden ett fynd om världen, och reserven i Övervägda alternativ prövas. Frågan ligger som en
  egen biljett, blockerad av bygget.
