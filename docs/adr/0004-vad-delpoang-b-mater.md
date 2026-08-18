# ADR 0004: B mäter väntad storlek, inte bara riktning

- Status: accepted
- Datum: 2026-08-18
- Beslutad i: biljett [#16](https://github.com/mcknschn/rosta/issues/16) under karta [#6](https://github.com/mcknschn/rosta/issues/6)
- Bygger på: [ADR 0002](0002-kategoripoangens-ansprak-och-vikter.md) och [ADR 0003](0003-skiljbarhet-och-kanslighetsanalys.md)

## Kontext

ADR 0003 punkt 2 i diagnosen fann att B är mättad vid taket. Räknar man bort
täckningskrympningen ligger `B_raw` på 5,00 i 32 av 56 celler, och i trygghet har alla åtta
partier samma tal. Biljett #16 ställde följdfrågan: är taket ett riktigt fynd om partierna,
eller en form på `net_support` som mättar så snart ett partis kodade ståndpunkter pekar åt rätt
håll? B väger 50 procent och är det enda ledet som bär riktning, så frågan avgör om halva
modellen mäter något.

## Diagnos

Mätt 2026-08-18 mot `config/`, `pipeline/` och `dist/scores.json`. Taket på 32 av 56 celler
reproducerades exakt.

1. **Normaliseraren gör om varje enhällig cell till ett rent tecken.**
   `pipeline/effects.py` räknar `net = num_sum / abs_sum`. Vikterna är alltid icke-negativa,
   så för en grupp där alla claims pekar åt samma håll blir kvoten exakt `±1` oavsett hur stora
   vikterna är. 282 evidence_effect-claims blir 228 indikatorceller. **184 av 228 har exakt ett
   claim**, och för dem är `±1` algebraiskt tvunget. 220 av 228 är enhälliga. Bara 8 celler
   hamnar strikt inuti skalan. 200 ligger på `+1`, 20 på `-1`.

2. **Evidensgraderingen når aldrig betyget.** Sätter man om varje claim till svagast tänkbara
   evidens, alltså `expert_opinion` gånger `low` styrka gånger `low` säkerhet, ändras
   **4 av 228 celler**. `evidence_level`, `effect_strength` och `confidence` tar ut varandra i
   normaliseraren i 224 av 228 fall.

3. **Det aggregerade `confidence` läses aldrig.** `aggregate_effects` räknar ut ett
   `confidence` per cell. `pipeline/scorerun.py` läser bara `net_support` och slänger resten.
   B:s säkerhet sätts i stället enbart av täckningen. Etiketten följer `B_thin_coverage` i
   **56 av 56 celler**, och ingen B-cell når någonsin `high`. `config/scoring.yaml` påstår
   samtidigt att "B:s confidence per kategori härleds ur indicator_effects-aggregatets
   confidence". Koden gör inte det. Configen dokumenterar ett beteende som inte finns, och
   `min_claims_for_high_confidence` i `config/claims.yaml` används av ingenting.

4. **Liggaren är enkelriktad.** `config/evidence_ledger.yaml` har 46 poster: 42 `positive`,
   3 som ger noll (`unclear` och `mixed`) och 1 `negative`. Det finns alltså precis en åtgärdstyp
   där det kostar att stödja den. Samtidigt är 239 av 269 partiståndpunkter `supports`.

5. **Följden.** B är i praktiken `tecken(stance) gånger täckning`. Tre av sex ingångar är döda.
   I trygghet är spridningen i `B_raw` exakt 0,000 över åtta partier medan spridningen i det
   utlevererade B är 0,459, alltså kommer all separation där ur hur många åtgärdstyper vi hunnit
   koda. I integration och klimat drar krympningen tvärtom ihop spridningen, 0,86 till 0,52
   respektive 0,81 till 0,49.

Svaret på biljettens fråga är därmed att taket är en **form, inte ett fynd**. Configen säger att
B mäter "Evidens/träffsäkerhet. Har förslagen källstöd för påstådd indikatoreffekt?". Det B
faktiskt räknar är andelen av partiets kodade ståndpunkter som backar liggarens åtgärder.

## Beslut

1. **Anspråket för B.** B svarar på *hur stor förbättring väntas av de åtgärder partiet driver?*
   Storlek, inte riktning. Det följer ur det låsta anspråket i ADR 0002: ett kategoribetyg svarar
   på hur mycket kategorin väntas förbättras. Ett rent tecken kan inte svara på "hur mycket".

2. **Storlek och säkerhet skiljs åt.** `effect_strength` bär storleken och går in i poängen.
   `evidence_level` och `confidence` bär säkerheten och går till säkerhetsetiketten och därmed
   till bandet. Storleken är punktskattningen, säkerheten är osäkerheten kring den. Det är samma
   uppdelning som underlaget i biljett [#8](https://github.com/mcknschn/rosta/issues/8) fann att
   etablerad praxis kräver: justering och redovisad osäkerhet, inte en rabatt på själva talet.

3. **Formen.** `net_support` per (parti, kategori, indikator) räknas som ett kvalitetsviktat
   medel av storlekar med tecken:

   ```
   q   = evidence_level x confidence           # kvalitet: vems storlek man tror på
   m   = effect_strength x tecken(riktning)    # storlek med tecken, i [-1, 1]
   net = Σ(q · m) / Σ q
   ```

   Ett ensamt claim ger `net = m`, alltså exakt sin egen effektstyrka med tecken. Flera claims
   ger ett medel där den bäst belagda källans storlek väger tyngst. Formen kan aldrig kollapsa
   till tecknet, eftersom storleksskalan står i täljaren men inte i nämnaren. `mixed` och
   `unclear` ger `m = 0` men behåller sitt `q`, alltså drar en källa som säger "oklart" cellen
   mot neutral, vilket är vad den säger.

4. **Talen 0,3 / 0,6 / 1,0 behålls oförändrade.** `numeric.effect_strength` i
   `config/claims.yaml` blir nu B:s skala rakt av: `low` ger 3,25, `medium` 4,00, `high` 5,00.
   Tabellen är ärvd och aldrig härledd. Den behålls ändå, och skälet är prövningsregeln i
   ADR 0003 punkt 1. Under arbetet med den här biljetten blev det känt att de enda två
   `high`-posterna i liggaren är **ny kärnkraft** och **Nato-medlemskap**. Att välja ett nytt tak
   efter den kunskapen vore ett val taget med kännedom om vilka partier det gynnar. Tabellen
   sattes innan någon tittade på ranking och är därmed det enda otaintade valet som står till
   buds. Att `high` når 1,0 och därmed återskapar ett tak för enskilda celler skrivs ned som en
   känd svaghet, och `numeric.effect_strength` läggs in som dragen parameter i
   känslighetsanalysen enligt ADR 0003 punkt 5.

5. **Säkerheten börjar läsa evidensen.** B:s grundnivå hämtas ur det aggregerade
   evidens-`confidence` med `min_claims_for_high_confidence: 3`, alltså regeln som redan står i
   `config/claims.yaml` men aldrig körts. Nivån sänks sedan ett steg vid tunn täckning, med
   samma `_step_down_confidence` som C och D använder. Evidenssäkerhet och täckningssäkerhet är
   båda osäkerhet och ska förstärka varandra, inte ersätta varandra. B kan för första gången nå
   `high`. Configtexten i `config/scoring.yaml` blir sann i stället för rättad.

6. **Godkännandetestet.** Ändringen godkänns om **B slutar ge samma tal till alla åtta partier**.
   Aldrig om rankingen blev bättre eller mer separerad. Formeln och talen låses i den här ADR:n
   före omkörningen, och utfallet redovisas som det blir. Rättningen byggs även om taket sitter
   kvar, eftersom den är motiverad i sig: tre döda fält blir levande och en config som säger emot
   sin egen kod blir sann.

## Vad beslutet inte rör

- **Täckningskrympningen (B5) står oförändrad.** Den är inte orsaken till taket, den är det som
  gör symptomet synligt. Att röra ett signat beslut för att dölja ett fel längre upp i kedjan går
  inte att försvara utan att titta på rankingen och faller på ADR 0003 punkt 1.
- **Viktad stance förblir övergiven.** Det beslutet (2026-06-07) stängde partisidan, alltså hur
  mycket av en åtgärd ett parti vill ha, med slutsatsen att appen kodar instrument och att binär
  stance därför är rätt passform. Den här ADR:n rör evidenssidan, alltså hur stor effekt
  utvärderingen fann. Binär stance består.
- **Anspråket i ADR 0002 står fast.** Rättningen tjänar det anspråket i stället för att bryta det.
- **Vikterna 0,30 / 0,50 / 0,20 och `max_interval_halfwidth` rörs inte.**
- **Liggarens enkelriktning avgörs inte här.** Diagnosen punkt 4 är en av tre orsaker till taket,
  men rättningen kräver nya liggarposter med källor, alltså ett bygge och inte ett beslut. Egen
  biljett.

## Följder

- Bygge: `pipeline/effects.py` (formen), `pipeline/scorerun.py` (säkerheten), `config/claims.yaml`
  och `config/scoring.yaml` (regeltexten), samt metodrutan i `web/app.js`. En slice med en
  omkörning, i samma form som #15.
- Byggnot: `numeric.confidence` i `config/claims.yaml` och `uncertainty.confidence_numeric` i
  `config/scoring.yaml` är två kopior av samma tal (0,85 / 0,60 / 0,30). När evidenssäkerheten
  nu går hela vägen till bandet bör de ha en källa, inte två.
- Metodrutans mening "Officiell statistik och forskning får avgöra om det partiet driver flyttar
  siffrorna åt rätt håll" blir sann först efter bygget. I dag avgör graderingen ingenting.
- Följdändringar: `IDEA.md` §Delpoäng och ordlistan `docs/done/evidens_trovardighet.md` §4.3
  beskriver båda B som ett rent riktningsmått.
