# ADR 0002: Kategoripoängens anspråk och vikter

- Status: accepted
- Datum: 2026-08-18
- Beslutad i: biljett [#9](https://github.com/mcknschn/rosta/issues/9) under karta [#6](https://github.com/mcknschn/rosta/issues/6)
- Bygger på: [ADR 0001](0001-a-mater-prioritering.md) och underlaget i biljett [#8](https://github.com/mcknschn/rosta/issues/8)

## Kontext

`IDEA.md` §Grundformel satte 40 procent prioritering, 35 procent evidens, 15 procent ansvar och
10 procent resultat. Talen var asserterade utan härledning. Invändningen i
[#1](https://github.com/mcknschn/rosta/issues/1) punkt 2 är att A därmed väger tyngst trots att A
mäter prioritering, inte om politiken fungerar. ADR 0001 skärpte invändningen: A är
riktningsneutral, så det tyngsta ledet i betyget kan inte skilja förbättring från försämring.

Underlaget i #8 gav ingen vikt. Det gav en villkorsregel. Metodlitteraturen härleder inte vikter
statistiskt: vikter är värderingar som ska kopplas till syftet, dokumenteras och prövas med
känslighetsanalys. Den skarpaste regeln för oss står i OECD/JRC:s handbok, steg 1, s. 22-23:
måttypen ska matcha vad indexet påstår sig mäta. Anspråket avgörs alltså före vikten. Handboken
understryker också att vikter i en linjär summa är utbytesförhållanden, inte betydelsegrader.

Kartans regel gäller: vikten motiveras och låses innan pipen körs om, aldrig tvärtom. Ingenting i
det här beslutet är taget med kännedom om hur rankingen påverkas.

## Beslut

1. **Anspråket.** Ett kategoribetyg svarar på en enda fråga: *hur mycket väntas kategorin förbättras
   om partiets politik genomförs?* Anspråket gäller politiken, inte partiets chans att få makt.
   Betyget bär dessutom ett kontrolled som kan säga emot anspråket, se punkt 4.
2. **Formeln.**

   ```
   Kategoripoäng = 0,30 x A + 0,50 x B + 0,20 x D
   ```

   C väger 0.
3. **B väger mer än A, i förhållandet 5:3.** B är det enda ledet som bär riktning. A bär omfattning.
   Ett parti som lägger all sin kraft på fel åtgärd förbättrar ingenting, medan ett parti som lägger
   lite kraft på rätt åtgärd förbättrar något. Den asymmetrin är inte liten, och talet är det inte
   heller. Ett tal som påstår sig mäta väntad förbättring får inte låta omfattning väga upp riktning.
4. **D väger 20 procent, härlett ur kontrolledets uppgift.** D ska kunna vända ett jämnt läge men
   aldrig ett tydligt försprång. Ett tydligt försprång är 1,0 poäng, en femtedel av 0-5-skalan. Den
   största möjliga skillnaden i D mellan två partier är hela skalan, alltså 5, och 0,20 x 5 = 1,0.
   Vikten är därmed precis så stor att en maximal motsägelse i utfallet når gränsen men inte förbi
   den.
5. **C är inte längre en delpoäng.** Den heter **ansvarsunderlag** och bär attributionen för D, vilket
   är den roll koden redan ger den (`min_responsibility` i `config/scoring.yaml`). Storheten räknas
   ut som förut och redovisas som upplysning om vem som haft makten, men den ger inga poäng.
6. **Vikterna är globala och låsta.** Samma fyra tal i alla sju kategorier, och användaren kan inte
   flytta dem. Användaren väger kategorier, aldrig metod.
7. **Osäkerheten kompenseras inte.** Halvbredden vägs med delpoängvikterna, så bredare spann är den
   korrekta följden av beslutet, se Konsekvenser.

## Övervägda alternativ

- **Behåll 40/35/15/10 och skriv motiveringen i efterhand.** Förkastat. Det är precis den form
  invändningen i #1 punkt 2 riktar sig mot, och att göra om den svarar inte på något.
- **Lika vikter, 25 procent var.** Förkastat. OECD rekommenderar inte lika vikter och varnar för att
  de döljer att grunden saknas. De är dessutom lika mycket ett värderingsval som vilket annat tal.
- **Vikter per kategori, satta efter hur väl varje del är mätt där.** Förkastat. Det byter ett
  värderingsval mot sju, och att sänka en delpoängs vikt där dess data är tunn är just den koppling
  mellan vikt och utfall som blindhetsregeln finns för att stoppa. Tunn täckning möts med krympning
  mot neutral och breda spann, och båda finns redan byggda.
- **Bakåtsyftande anspråk, alltså "hur väl har partiet levererat", med D som huvudmått.** Förkastat.
  `IDEA.md` och `CLAUDE.md` säger båda förväntad effekt. CCPI väger uppmätt utfall runt 80 procent
  och är motexemplet i #8, men den modellen bedömer sittande regeringar, inte partier i ett val.
- **D ut ur summan, redovisad bredvid som kontroll.** Förkastat. Det tar bort det enda ledet som kan
  falsifiera modellen ur det tal användaren faktiskt rangordnar på. #8 fann dessutom att etablerad
  praxis vid svag attribution är justering och redovisad osäkerhet, inte att lyfta ut måttet.
- **C kvar med vikt som proxy för realiserbarhet.** Förkastat. Anspråket villkorar redan på att
  politiken genomförs, så innehavd makt svarar på en fråga betyget inte ställer. C som byggd är
  dessutom `c1` ensam, alltså andel av innehavd makt (`pipeline/scorerun.py`, `category_c`), vilket
  ger ett inkumbensbidrag på 15 procent i varje kategori oavsett vad makten användes till. Det enda
  innehåll i C som skulle pröva anspråkets premiss är `c2`, finansiering, och `c2` är uppskjuten
  med motiveringen att den inte går att bygga neutralt ur svensk officiell data.
- **A minst lika tungt som B, med skälet att A är robust mätt medan B är krympt mot mitten.**
  Förkastat, av samma skäl som kategorivikter: det låter datatillgången bestämma vad modellen
  påstår sig mäta.
- **Minsta skiljande marginal mellan B och A, alltså 42,5 mot 37,5.** Förkastat. En marginal vald
  för att precis vända ett tecken är svår att försvara som härledd ur anspråket.

## Konsekvenser

- **Rankingrelevant.** Femton procent lämnar C och fördelas om, och B går om A. `config/scoring.yaml`
  och `config/categories.yaml` ändras i en byggslice, och pipen körs om först på uttrycklig order.
  Ingen ranking har konsulterats före låsningen.
- **Osäkerhetsspannen blir bredare.** Halvbredden är `max_halfwidth x Σ vikt x (1 - säkerhet)`
  (`pipeline/score.py`, `category_uncertainty_halfwidth`). Med standardsäkerheterna ger de gamla
  vikterna 0,44 och de nya 0,58, alltså ungefär en tredjedel bredare. C:s höga säkerhet drog
  tidigare ned spannet med sina 15 procent och gör det inte längre. `max_interval_halfwidth`
  justeras inte som kompensation. Fler partipar kommer att ha spann som går omlott, och att de inte
  går att skilja åt är då ett riktigt besked, inte ett fel.
- **Konfignyckeln C behålls.** `pipeline/config.py` kräver att `subscore_weights` har alla fyra
  nycklarna A, B, C och D och att de summerar till 1,0. C sätts därför till 0 och stryks inte. Det
  är bara i delpoängstabellen C försvinner.
- **Kompenserbarheten kvarstår som egenskap.** Formen är fortfarande en linjär summa, så delpoängen
  kan väga upp varandra. Med B på 50 mot A på 30 kan omfattning inte längre väga upp riktning, och
  det var invändningen i #1 punkt 2. En multiplikativ form prövades därför inte.
- **Kvar till byggslice:** vikterna i `config/scoring.yaml` och `config/categories.yaml`, kommentaren
  om formeln överst i `config/scoring.yaml`, metodrutan i `web/app.js` (som dessutom beskriver A som
  enbart motioner och saknar `a1`), och `coverage_technical`-strängen som `pipeline/scorerun.py`
  genererar.
- **Ändrat i det här ärendet:** den här ADR:n, `IDEA.md` §Bedömningskedja, §Grundformel och
  §Delpoäng, samt delpoängsordlistan i `docs/done/evidens_trovardighet.md` §4.3.
- **Avblockerar** [#5](https://github.com/mcknschn/rosta/issues/5), kartan för D:s kausala
  försiktighet. Frågan om D:s täckning håller vid 20 procent i stället för 10 hör hemma där.

## Rättelse 2026-08-18

Beslutad i biljett [#14](https://github.com/mcknschn/rosta/issues/14). Punkt 5 står kvar oredigerad,
eftersom ADR:n är accepterad. Två saker i den är fel.

1. **C bär inte attributionen för D.** Punkt 5 skriver att C "bär attributionen för D, vilket är den
   roll koden redan ger den (`min_responsibility` i `config/scoring.yaml`)". Koden gör inte det.
   `min_responsibility` grindar på D:s egen storhet `basis` i `category_d`, alltså Σ maktvikt över de
   år partiet faktiskt attribueras, per kategori. Den räknas ur `year_power_fractions()`. C räknas ur
   `government_fractions()`, som är andel av hela fönstret. Olika funktioner, olika nämnare. De två
   storheterna rör aldrig varandra. C:s roll är upplysning om vem som haft makten, och ingenting mer.
2. **C heter maktandel, inte ansvarsunderlag.** Ordet *ansvarsunderlag* var upptaget: det är namnet på
   D:s grindstorhet ovan, och den användningen är äldre och sitter i confignycklar och i flaggan
   `D_thin_basis`. Ett ord, en betydelse. C:s namn bytte därför, inte D:s. Konfignyckeln `C_ansvar`
   behålls, precis som `A_agerande` behålls tills ADR 0001:s byggslice körs.

Rättelsen rör inga vikter. Den rör däremot två betyg, tvärtemot vad biljett #14 antog.
Maktandelens fönsterslut flyttades i samma ärende från valdagen till 2025-12-31, och `components.C`
är inte den nationella maktandelen utan en per-kategori-blandning av nationell och subnationell makt
(`category_c`). Den nationella rangordningen är stabil under båda gränserna, men blandningen är det
inte: i trygghet korsar SD och C. Eftersom vikterna i den här ADR:n ännu inte är byggda -
`config/scoring.yaml` och `config/categories.yaml` har kvar `C: 0,15` - når korsningen kategoribetyget:
C/trygghet 3,036 -> 3,143 och SD/trygghet 3,296 -> 3,189, med spannen. Totalrankingen och trygghets
interna ordning står still. När viktslicen körs faller den här effekten bort av sig själv, eftersom C
då väger 0.
