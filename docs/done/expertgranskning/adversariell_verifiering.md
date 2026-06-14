# Adversariell omverifiering — högrisk-delmängd (B)

> Oberoende skeptisk granskning (2026-05-31) av den högsta-risk-delmängden i
> `config/party_positions.yaml`: de **propositionsavslags-opposes** och **`ny_karnkraft`**-rader
> som DATA.md/BACKLOG flaggar. Varje rad hämtades live mot riksdagens fulltext (`data.riksdagen.se`)
> och bedömdes på tre frågor: (a) är citatet ordagrant? (b) ÄR den avslagna propositionen
> verkligen den kodade åtgärdstypen? (c) följer `stance`?
>
> Tre oberoende granskare default:ade till SUSPECT vid minsta tvivel. **Ingen config ändrades** —
> fynden nedan är beslutsunderlag för den mänskliga slutgranskningen.

## Sammanfattning

| Verdikt | Antal | Rader |
|---------|-------|-------|
| ✅ CONFIRMED | 7 | V/MP `ny_karnkraft` opposes (prop 2025/26:160); V `aktiveringskrav` opposes (prop 2025/26:207); SD `tidiga_insatser` opposes (prop 2017/18:195); SD/KD/L `ny_karnkraft` supports |
| ⚠️ SUSPECT | 4 | S `ny_karnkraft` supports · V `kontroller_valfardsbrott` opposes · C `tidiga_insatser` opposes · M `ny_karnkraft` supports (källtyp) |

**Det viktigaste resultatet:** de evidens-*vändande* opposes-rader där ett fel gör mest skada
(V/MP mot ny kärnkraft, V mot aktivitetskrav, SD mot läsa-skriva-räkna-garantin) är alla
**bekräftade ordagrant och rätt riktade**. Den allvarligaste felklassen är alltså utesluten.
De fyra SUSPECT-fynden rör *övertolkad stance* och *felaktig partitillskrivning*, inte fabrikat.

---

## ⚠️ SUSPECT 1 — S `ny_karnkraft` = supports (doc_id HD023594)

**Fynd:** Citatet är ordagrant, men S kvalificerar uttryckligen: *"För Socialdemokraterna är det
fortsatt inte aktuellt att bygga ny kärnkraft på andra platser än de befintliga."* S accepterar
finansieringsramen för all fossilfri el men **avvisar ny kärnkraft på nya platser** — vilket är
själva kärnan i prop 2025/26:160. Att koda detta som rent `supports` på `ny_karnkraft` övertolkar.

**Rekommendation (expertbeslut):** omkoda till villkorat/neutralt, eller ta bort raden (frånvaro =
coverage-lucka, inte motstånd). Påverkar S:s B i klimat (höjer den i dag via `effektbrist`-effekten).

## ⚠️ SUSPECT 2 — V `kontroller_och_informationsutbyte_mot_valfardsbrott` = opposes (doc_id HC023445)

**Fynd:** Citatet ("Riksdagen avslår proposition 2024/25:180") är ordagrant. Men **prop 2024/25:180
är bredare än åtgärdstypen**: titeln är "Ökat informationsutbyte mellan myndigheter – en ny
sekretessbrytande bestämmelse" och täcker brottsbekämpning generellt, inte bara välfärdsbrott. V:s
yrkande 2 begär dessutom ett *"mer begränsat, proportionellt och rättssäkert förslag"* — V är alltså
inte emot informationsutbyte mot välfärdsbrott i sak, utan mot den breda lagens utformning.

**Rekommendation:** stance=opposes mot just `...mot_valfardsbrott` är inte ordagrant belagd. Omkoda
till "stödjer med förbehåll/snävare" eller knyt till en bredare åtgärdstyp. Sänker i dag V:s B i
välfärd felaktigt.

## ⚠️ SUSPECT 3 — C `tidiga_insatser_lagstadiet` = opposes (doc_id H5023910)

**Fynd:** Citatet ("Riksdagen avslår regeringens proposition 2017/18:18 …") är ordagrant och rör rätt
sakområde (läsa-skriva-räkna). **Två problem:** (1) dokumentet är en **gemensam allians-kommittémotion
(L, M, C, KD)** med Christer Nylander (L) som förstanamn — att tillskriva enbart C är missvisande;
(2) den riktar sig mot prop 2017/18:**18** (tidig, ej antagen variant), inte den antagna **195**. På
det antagna instrumentet ville alliansen justera ikraftträdandet, inte avslå.

**Rekommendation:** granska partitillskrivningen (är detta C:s linje, eller alliansens?) och om
opposes ska gälla det antagna instrumentet. Speglas: SD-raden (H501UbU10) är mot rätt proposition (195)
och är CONFIRMED — C-raden är den svaga.

## ⚠️ SUSPECT 4 — M/SD/KD/L `ny_karnkraft` = supports (källtyps-asymmetri)

**Fynd:** Alla fyra citat är ordagranna och hållningen (pro ny/utbyggd kärnkraft) är entydig. Men
medan opposes-raderna (V/MP) är äkta **följdmotioner till prop 2025/26:160**, är supports-raderna
**generella partimotioner från andra riksmöten** (M 2021/22, SD 2024/25, KD 2021/22, L 2020/21).

**Bedömning:** Detta är metodologiskt *försvarbart* om åtgärdstypen `ny_karnkraft` avser partiets
**generella hållning** (vilket evidensliggarens `ny_karnkraft → effektbrist` antyder), inte en röst om
just prop 160. Lägre prioritet än SUSPECT 1–3, men bör dokumenteras så jämförelsen "för/emot ny
kärnkraft" inte tolkas som "för/emot prop 160".

---

## ✅ CONFIRMED (verbatim + rätt proposition + rätt riktning)

| Parti | Åtgärdstyp | Stance | doc_id | Proposition / källa |
|-------|-----------|--------|--------|---------------------|
| V | ny_karnkraft | opposes | HD023961 | följdmotion mot prop 2025/26:160 "Ny kärnkraft i Sverige – fler möjliga platser vid kusten" |
| MP | ny_karnkraft | opposes | HD023984 | följdmotion mot prop 2025/26:160 |
| V | aktiveringskrav_ekonomiskt_bistand | opposes | HD024027 | avslag prop 2025/26:207 "Aktivitetskrav för mottagare av försörjningsstöd" |
| SD | tidiga_insatser_lagstadiet | opposes | H501UbU10 | reservation 1 (SD), avslår prop 2017/18:195 (den antagna garantin) |
| SD | ny_karnkraft | supports | HC021464 | "successivt bygga ut och vidareutveckla kärnkraften" |
| KD | ny_karnkraft | supports | H9024195 | "återuppta planeringen av nya kärnkraftsreaktorer" |
| L | ny_karnkraft | supports | H8023242 | statlig utredare för små/alternativa reaktorer |

Prop-identiteterna 2025/26:160, 2025/26:207, 2017/18:195 och 2017/18:18 är samtliga oberoende
bekräftade mot riksdagen.se/regeringen.se.
