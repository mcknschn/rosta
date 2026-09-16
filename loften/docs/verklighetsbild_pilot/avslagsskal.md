# Avslagsskäl: Verklighetsbild byggs inte

- Datum: **2026-09-13**
- Beslutad av: [ADR 0016](../adr/0016-verklighetsbild-avgors-av-en-pilot.md) beslutspunkt 11
- Grundat på: [`resultat.md`](resultat.md) och
  [`config/verklighetsbild/resultat.yaml`](../../config/verklighetsbild/resultat.yaml)
- Biljett: [#46](https://github.com/mcknschn/rosta/issues/46)

Piloten klarade inte den förhandsregistrerade tröskeln. Arbetet med Verklighetsbild läggs ned.
Materialet ligger kvar.

Detta är en godkänd utgång. Den viktade stansen prövades och förkastades på samma sätt 2026-06-07.

## Skälet

Tröskeln krävde två saker. Båda föll.

1. **Designviktat utbyte minst 0,20 prövbara relationer per utsaga.** Utfallet blev **0,054**, med
   det 95-procentiga intervallet 0,017 till 0,091. Intervallets övre gräns ligger under halva
   tröskelvärdet.

2. **Minst 5 prövbara relationer hos vart och ett av de åtta partierna.** Ett parti nådde dit. Fyra
   partier bar noll relationer i sina 25 kodade utsagor.

Skattat till hela bakåtmaterialet bär de 896 utsagorna omkring 48 prövbara relationer. Tröskeln
förutsatte omkring 180.

## Vad som inte var skälet

**Kodarna var överens.** Krippendorffs alfa för prövbarhet blev 0,850, alltså långt över
tröskelvärdet 0,667. Avgränsningen låg på 0,884 och indikatorvalet på 0,853. Bara kodvärdet, 0,677,
stannade på tentativ nivå.

Instrumentet fungerade alltså. Det var materialet som inte bar.

Det spelar roll för hur beskedet ska läsas. Ett lågt utbyte med låg reliabilitet hade betytt att
kodboken var för svag och att en bättre kodbok kunde ge ett annat svar. Ett lågt utbyte med hög
reliabilitet betyder att två kodare som läser samma regler ser samma tomhet.

## Vad materialet faktiskt bär

188 av 200 kodade utsagor bedömde båda kodarna som **inte prövbara**. Bortfallet fördelar sig så
här, med kodare A:s koder:

| Kod | Utsagor |
|---|---|
| `normativ` | 112 |
| `ingen_kompatibel_indikator` | 52 |
| `otillracklig_kontext` | 12 |
| `data_saknas` | 7 |
| `framtida_utfall` | 4 |
| `flera_operationaliseringar` | 1 |

Mer än hälften av materialet är alltså värdepåståenden utan mätbar kärna. Ytterligare en fjärdedel
bär en mätbar kärna som ingen av modellens 68 indikatorer mäter.

Detta bekräftar ADR 0016 diagnospunkt 3, som handklassade 40 kandidater och fann 20 procent rena
faktapåståenden. Piloten mätte samma sak på 200 utsagor med två kodare och en låst kodbok, och fick
ett lägre tal.

## Vad beslutet inte rör

- **Betygen.** Verklighetsbild hade vikt 0 och ingick aldrig i någon poäng, något band eller någon
  rangordning. Inga betyg rör sig. `dist/` är orört.
- **Materialet.** `docs/valmanifest_2026/` ligger kvar, och korpusen i
  `config/verklighetsbild/` likaså. Framåtkorpusen är fryst med brytpunkten 2030-09-08 och rörs
  inte förrän dess.
- **De 68 indikatorerna.** Piloten prövade inte modellen. Den prövade om partiernas egna
  beskrivningar går att hålla mot den.

## Vad som faller bort

- **Produktionskodboken skrivs inte.** Den skulle bara skrivas om tröskeln klarades
  (ADR 0016 beslutspunkt 6 och 9). Kodvärdet `skev` förblir förkastat, och ingen ersättande regel
  behövs.
- **En egen karta graderas inte.** Den skulle bara graderas om piloten klarades.
- **Biljett #42 punkt 9 faller.** Frågan om nya källor ska höja täckningen förutsatte ett utbyte
  som är värt att höja. Utbytet är 0,054.

## Vad som lever vidare

Tre fynd är värda att bära med sig, oberoende av att måttet lades ned.

1. **Kodboken motsäger sig själv** i avsnitt 6.5 mot avsnitt 10. Tre kodare hittade det oberoende
   av varandra. Skrivs ett liknande instrument någon gång, är den motsägelsen först att laga.
2. **Framåtkorpusen bär rubriker, inte full text.** Två av 1 073 poster bär både en storhet och en
   period, och båda faller på att partiets storhet är ett antal medan indikatorns är en andel.
   Ska framåthalvan någonsin prövas måste posterna bära den fulla lydelsen ur PDF:en.
3. **Hämtmanifestets URL-fält är tomma.** Adresserna skrevs aldrig ned. Nästa gång dokument hämtas
   utifrån förs adressen in samtidigt som filen.

## Villkor för att ta upp frågan igen

Frågan tas upp igen om, och bara om, något av detta inträffar. Villkoren skrivs så att de går att
pröva.

- **Materialet byts.** Prövas ett annat underlag än valmanifest, till exempel partiernas
  budgetmotioner eller riksdagsanföranden, gäller inte detta utbytestal. Det mättes på manifesten.
- **Indikatorlistan växer kraftigt.** 52 av 200 utsagor föll på `ingen_kompatibel_indikator`.
  Fördubblas antalet inlästa indikatorer, från dagens 43, är utbytet värt att mäta om.
- **Analysenheten byts.** Detta utbyte gäller relationen `utsaga x indikator x tidsperiod x
  operationalisering`. En annan enhet ger ett annat tal, och då krävs en ny förhandsregistrering.

Ingen av de tre är på väg att inträffa. Frågan är stängd tills vidare.
