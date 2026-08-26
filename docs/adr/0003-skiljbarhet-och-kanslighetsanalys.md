# ADR 0003: Skiljbarhet mäts som ordningens stabilitet, inte som bandöverlapp

- Status: accepted
- Datum: 2026-08-18
- Beslutad i: biljett [#10](https://github.com/mcknschn/rosta/issues/10) under karta [#6](https://github.com/mcknschn/rosta/issues/6)
- Bygger på: [ADR 0002](0002-kategoripoangens-ansprak-och-vikter.md) och underlaget i biljett [#8](https://github.com/mcknschn/rosta/issues/8)

## Kontext

[#1](https://github.com/mcknschn/rosta/issues/1) punkt 4 begär två saker. Känslighetsanalysen ska
bli förstklassig utdata, och frontend ska kunna visa vilka partipar som är robust skilda. Biljetten
ställde därför två frågor: vilka scenarier ska köras, och vad räknas som en robust skillnad.

Efter viktbytet i [#15](https://github.com/mcknschn/rosta/issues/15) går 28 av 28 partipar omlott i
totalen. Sajten visar en rangordnad lista och säger samtidigt i metodrutan att omlottgående spann
inte går att skilja åt. Läst bokstavligt påstår produkten alltså att den inte kan rangordna
någonting, samtidigt som den visar ett parti högst upp.

### Diagnos

Mätt 2026-08-18 mot `dist/scores.json` och standardvikterna i `config/categories.yaml`.

1. **Bandet är ingen skattning ur data.** Halvbredden är
   `max_halfwidth x Σ vikt x (1 - säkerhet)` (`pipeline/score.py`,
   `category_uncertainty_halfwidth`). 39 av 56 celler ligger på 0,488. Bandet varierar bara med
   deklarerad säkerhetsnivå, aldrig med spridningen i underlaget. `max_interval_halfwidth = 1,5`
   saknar härledning i repot. Talet står i `config/scoring.yaml` och i `docs/done/ROADMAP.md` utan
   motivering.
2. **B är mättad vid taket.** Räknar man bort coverage-krympningen
   (`B_raw = 2,5 + (B - 2,5) / cov`) ligger B_raw på 5,00 i 32 av 56 celler. I trygghet har alla
   åtta partier B_raw = 5,00, så det enda som skiljer dem i B är täckningen, alltså hur många
   åtgärdstyper som hunnit kodas. B väger 50 procent och är den enda delpoäng som bär riktning.
3. **A bär separationen.** Viktad spridning summerad över de sju kategorierna: A 7,76, B 6,24,
   D 1,34. A är rangnormaliserad och spänner 0 till 5 per konstruktion. ADR 0001 låste A som
   riktningsneutral. Modellen skiljer alltså partierna åt främst med den delpoäng som inte påstår
   att politiken är bra.
4. **Utjämningen mellan kategorier äter 75 procent.** Snittspridningen inom en kategori är 1,25. I
   totalen blir den 0,31 vid lika vikt. Partierna leder olika kategorier.
5. **Separationen kommer inte tillbaka med andra reglage.** Av 2000 slumpade viktuppsättningar gav
   1 procent något skiljbart par alls.

Bandöverlappet jämför alltså en signal på 0,43 mot ett valt tal som är 0,98 brett. Testet mäter
modellparametern, inte partierna.

### Metodstöd

OECD/JRC:s handbok, steg 7 (s. 34-35), kräver att analysen visar *"what sources of uncertainty are
more influential in determining the relative ranking of two entities"*. Handboken rangordnar också
felkällorna: viktvalet styr rankingen mest, normalisering och imputering minst (s. 131). Underlaget
ligger i `docs/research/vikter_avsikt_vs_utfall.md` §1.5, på branchen
`research/vikter-avsikt-vs-utfall`.

Kartans blindhetsregel gäller. Kriteriet och spannen låses här, före första körningen. Talen i
diagnosen är dock redan kända, vilket är en känd svaghet i den här ADR:n. Prövningsregeln i punkt 1
finns för att hantera det.

## Beslut

1. **Prövningsregel.** Ökad separation är aldrig ett mål. En metodändring är tillåten om den går att
   försvara utan att titta på rankingen. En delpoäng som ger 5,00 till alla åtta partier mäter
   ingenting, och det argumentet står oavsett vad en rättning gör med ordningen. En sänkt
   `max_interval_halfwidth` klarar inte samma test och är därför förbjuden som åtgärd.
2. **Storhet.** Skiljbarhet mellan två partier mäts som **andelen metodvarianter där deras inbördes
   ordning håller**. Bandöverlappet upphör att vara skiljbarhetstest. Bandet står kvar som
   redovisad osäkerhet i kategoribetyget, och `max_interval_halfwidth` behåller värdet 1,5.
3. **Ingen tröskel.** Andelen redovisas som den är. Sajten säger "S ligger före L i 68 procent av
   metodvarianterna", aldrig "robust skilda" eller "oskiljbara". Ett tröskeltal skulle flytta
   gränsen mellan rangordnat och vet ej utan att något i underlaget ändras, och faller på punkt 1.
4. **Form.** Monte Carlo bär statistiken. Alla osäkra val dras samtidigt. Sju namngivna scenarier
   bär kommunikationen och körs var för sig. Bara samtidig dragning svarar på vilken källa som
   dominerar, vilket är den del av steg 7 som är ett krav.
5. **Källor.** Med i dragningen: delpoängvikterna A, B och D; `max_interval_halfwidth`;
   `confidence_numeric`; `default_subscore_certainty`; A:s normalisering; B:s `coverage_mode`; B:s
   krympning på eller av; `thin_coverage_threshold`; D:s `attribution_lag_years`,
   `change_dead_zone`, `min_responsibility`, `thin_basis_threshold` och `coverage_shrink`; D:s
   subnationella läge och `region_weighting`. **C ingår inte**, den väger 0. **Kategorivikterna
   ingår inte i pipekörningen**, eftersom användaren äger dem i webbläsaren.

   > **Utvidgad av [ADR 0010](0010-ett-reglage-ar-en-vag-pipen-redan-kan-ga.md), 2026-08-26.**
   > Punkten räknar upp posterna men säger inte vad som kvalificerar en post till listan. ADR 0010
   > punkt 1 avgör regeln: ett **reglage** är en punkt där pipen kan gå en annan väg utan att någon
   > skriver ny kod, och där underlaget kan uttrycka den vägen. ADR 0010 punkt 2 avgör att listan
   > är ett register över byggda variationspunkter, inte ett anspråk på all osäkerhet. Två
   > följdändringar: **A:s normalisering** står kvar i texten ovan men är struken ur tabellen sedan
   > [#21](https://github.com/mcknschn/rosta/issues/21), och **`A_component_mix`** läggs till med
   > spannet a1 i (0,50, 0,80]. Ordet **reglage** ersätter *källa* för den dragna storheten
   > (ADR 0010 punkt 8). Texten nedan står oförändrad.
6. **Spann.** En regel, inte en tabell med valda tal. Diskreta val får sina **byggda** alternativ,
   varken fler eller färre. Kontinuerliga parametrar får ett spann som täcker varje värde repot
   faktiskt använt eller dokumenterat som alternativ, plus en symmetrisk marginal. Vikterna dras ur
   den mängd som ADR 0002:s härledning tillåter, alltså B störst, A näst, D minst och C noll. Då
   prövar analysen härledningens slutsats i stället för en godtycklig omviktning.
   `max_interval_halfwidth` får ett brett spann, just för att 1,5 saknar härledning.
7. **Nivå.** Både kategori och total. Pipen kan inte förberäkna totalen, eftersom användarens vikter
   sätts i webbläsaren. Pipen skriver därför kategoribetygen per dragning, och webbläsaren räknar
   andelen för användarens egna vikter. Det avskaffar samtidigt dagens antagande om full korrelation
   mellan kategorier, som uppstår när `web/score.js` adderar kategoribanden.
8. **De sju namngivna scenarierna.** 1. Gamla vikterna 0,40 A + 0,35 B + 0,15 C + 0,10 D. 2. A
   halveras. 3. B utan coverage-krympning. 4. B:s säkerhet ett steg ned. 5. D-lagg 2 år i stället
   för 1. 6. Bara kategorier med hög D-täckning. 7. Bara partier med nationellt ansvar.
9. **Filter redovisas skilt.** Scenario 6 och 7 byter vad indexet mäter, inte hur osäkert det är.
   De hör därför inte hemma i Monte Carlo-statistiken och redovisas i en egen tabell.
10. **Avgränsning.** Den här ADR:n avgör kriteriet och vad sajten ska säga. Utformningen i frontend
    ligger i [#11](https://github.com/mcknschn/rosta/issues/11). Tillförlitlighetsgraden per cell
    ligger i [#12](https://github.com/mcknschn/rosta/issues/12). D:s inerthet ligger i
    [#5](https://github.com/mcknschn/rosta/issues/5). B:s mättnad får en egen biljett.

## Övervägda alternativ

- **Sänk `max_interval_halfwidth`.** Förkastat. Det byter tal och inte storhet, och faller rakt på
  prövningsregeln i punkt 1. Ett smalare band skulle producera skiljbara par utan att något i
  underlaget blivit säkrare.
- **Behåll bandöverlappet som skiljbarhetstest.** Förkastat. Bandet är nästan konstant över
  cellerna, så att två band överlappar säger ingenting om just det paret.
- **Tröskel, till exempel 95 procent.** Förkastat. Se punkt 3.
- **Bara namngivna scenarier, utan Monte Carlo.** Förkastat. En lista körd en variant i taget svarar
  inte på vilken källa som dominerar, och det är kravet i handbokens steg 7.
- **Blockera biljetten på B:s mättnad.** Förkastat. Scenariobeslutet står oavsett vad B landar i,
  och analysen är själva instrumentet som mäter om en B-rättning gör skillnad.
- **Skiljbarhet bara på totalen.** Förkastat. Kategorinivån är där modellen faktiskt separerar
  partierna, och den nivån går att förberäkna i pipen.

## Konsekvenser

- **Inte rankingrelevant.** Inga betyg ändras. Utdatan får ett nytt fält och sajten en ny
  formulering. Ordningen är oförändrad.
- **Metodrutan i `web/app.js` måste skrivas om.** Meningen "Går två partiers spann omlott kan vi
  inte säga vilket av dem som ligger bäst till" blir fel när bandet inte längre är
  skiljbarhetstest.
- **`ciOverlap` i `web/score.js` slutar bära skiljbarhetspåståendet.** Funktionen och märkningen
  "Skillnaden mot nr N är osäker" ersätts av andelen.
- **Kostnaden är låg.** `scorerun.build()` mot den lokala warehouse:n tar 0,07 sekunder varm. Tio
  tusen dragningar landar på ungefär tolv minuter.
- **Utjämningen är ett fynd, inte ett fel.** Partierna leder olika kategorier, och därför tar
  skillnaderna ut varandra i totalen. Det är ett riktigt besked om svensk politik. Modellen ska
  redovisa det, inte kompensera för det.
- **A:s faktiska påverkan är öppen.** A väger 0,30 men bär mest av separationen. Det är JRC:s poäng
  om att nominell vikt inte är faktisk påverkan. Frågan är inte skarp nog för en egen biljett förrän
  B:s mättnad är avgjord, och ligger därför i kartans dimma.
- **Avblockerar ingenting.** Ingen kant mot B-biljetten, åt något håll.
- **Ändrat i det här ärendet:** den här ADR:n. Ingen kod och ingen config.

## Byggspec

Egen slice för `/workflow`. Ingenting av detta byggs i biljetten.

### Pipeline

Nytt verktyg `pipeline/robustness.py`, byggt som `pipeline/tools/c3_sensitivity.py`: kopiera
`config.scoring()`, ändra i minnet, monkeypatcha `config.scoring` och kör `scorerun.build(con)`.

Skriver `dist/robustness.json`:

- `meta`: `n_draws`, `n_draws_shipped`, `seed`, `generated`, `sources` (namn till spann eller
  alternativlista), `monte_carlo_error` i procentenheter.
- `draws`: `parties` och `categories` som ordningslistor, plus en flat heltalsvektor med
  kategoribetygen skalade med 100. Formatet håller filen liten nog att skickas till webbläsaren.
- `category_stability`: per kategori och partipar, andelen dragningar där ordningen håller.
- `source_influence`: per källa, hur mycket den ensam flyttar andelen. Detta är handbokens
  steg 7-krav.
- `scenarios`: de sju namngivna, var och en med hela 8 x 7-matrisen och den ordning den ger under
  standardvikterna. Scenario 6 och 7 märks som filter.

`seed` är fast, så körningen är reproducerbar. `n_draws` default 10 000, `n_draws_shipped` default
2000. Monte Carlo-felet redovisas i utdatan och göms aldrig.

### Frontend

`web/score.js` får `pairStability(draws, weights, catIds)`, som returnerar andelen per partipar för
användarens egna vikter. Ren funktion, testbar i Node, ingen A/B/C/D-logik.

`web/app.js` byter märkningen mot andelen och skriver om metodrutans stycke om spann. Formen
avgörs i [#11](https://github.com/mcknschn/rosta/issues/11), inte här.

### Tester

Lås att andelen aldrig presenteras som ett binärt omdöme. Lås `seed` och `n_draws`, så att en
oavsiktlig ändring av spannen syns som en diff. Testerna kör mot `:memory:`, aldrig mot
`data/warehouse.duckdb`.
