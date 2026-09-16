# Löftesspåret

Allt under `loften/` hör till detta spår. Projektets rot-CLAUDE.md gäller fortfarande för
språk, källor och skrivregler. Denna fil säger var spåret **avviker**.

## Frågan spåret ställer

**Vad lovar ett parti sina väljare inför ett val, och har partiet sedan arbetat med det löftet?**

Två leveranser:

1. **Kartan.** Vad partierna lovar. Ett läsbart löftesregister.
2. **Uppfyllelsen.** Har partiet lagt fram förslag och budgetar i linje med löftet.

Biljett: [#52](https://github.com/mcknschn/rosta/issues/52).

## Anspråket

Spåret mäter **löfte mot handling**. Aldrig löfte mot samhällsutfall.

Följden ska stå skriven i varje text spåret producerar:

> Ett parti som lovat något och sedan arbetat för det får en tumme upp, även om saken vore dålig
> för Sverige.

Om åtgärden var klok avgörs av delpoäng B och D i modellen, aldrig här.

En tumme ned betyder att partiet inte arbetat med löftet. Den betyder **aldrig** ohederlighet,
löftesbrott eller dålig politik.

## Fyra regler som binder

### 1. Framlagt räknas, genomröstat räknas inte

Ett parti som lagt fram sitt förslag och blivit nedröstat har arbetat med löftet. Det straffas
inte. Spåret läser vad partiet lade fram, aldrig vad som gick igenom.

### 2. Instrumentet följer positionen

Ett regeringsparti skriver ingen budgetmotion. Det lägger en budgetproposition. Mäts bara egna
motioner får de partier som styrde landet noll, vilket är bakvänt.

Därför gäller:

| Partiets läge | Vad som räknas som framläggande |
|---|---|
| Opposition | Partiets egna motioner och egen budgetmotion |
| Regering | Regeringens propositioner och budgetpropositionen, tillskrivna regeringspartierna |

Detta är **ingen maktkorrigering i efterhand**. Båda lägena mäts med sitt eget instrument, så
ingen justering behövs efteråt.

Två fall är olösta och ska avgöras innan något byggs. En koalitionsproposition bärs av flera
partier. Ett stödparti är varken regering eller ren opposition.

### 3. Spåret väger 0 och rör aldrig rangordningen

Ingenting här påverkar modellens betyg, band eller rangordning. Vikterna 0,30 A + 0,50 B + 0,20 D,
C = 0 står orörda (ADR 0002). `dist/` skrivs aldrig av detta spår.

### 4. Utfall hör inte hit

Varje text som antyder att ett uppfyllt löfte är bra för Sverige är ett fel i spåret.

## Förhållandet till projektets ADR:er

Projektets ADR:er binder **modellens delpoäng**. De binder inte detta spår. Spåret får sätta egna
regler, och motsägelser mot en ADR är tillåtna här.

Gränsen går vid skillnaden mellan beslut och faktum:

- Ett **beslut** i en ADR får spåret avvika från. ADR 0017 låste a1 till författarskap. Spåret
  behöver inte följa det.
- Ett **faktum om data** går inte att besluta bort. Att koalitionsår bärs av en delad ram är ett
  faktum. Spåret får välja hur det hanteras, aldrig att det inte gäller.

Avviker spåret från en ADR ska avvikelsen skrivas ned här, med skälet.

## Två lärdomar som binder

Båda kommer ur nedlagda mått i projektet och gäller här.

1. **Förhandsregistrera, och pröva talens ursprung.** Samstämmighet klarade alla tre trösklarna
   och mätte ändå fel sak. Profilavståndet korrelerade 0,998 med retorikens egen koncentration.
   Trösklar som bara prövar hur talen fördelar sig kan inte se var talen kommer ifrån. Varje
   förhandsregistrering i detta spår ska bära minst ett prov som pekar på ursprunget.
   Se [`docs/samstammighet_poc/nedlaggning.md`](docs/samstammighet_poc/nedlaggning.md).
2. **Korsläs kodboken innan den låses.** Pilotkodbokens avsnitt 6.5 stred mot avsnitt 10. Tre
   kodare hittade motsägelsen oberoende av varandra och löste den åt olika håll.
   Se [`docs/verklighetsbild_pilot/avslagsskal.md`](docs/verklighetsbild_pilot/avslagsskal.md).

## Mappen

Allt som rör spåret flyttades hit 2026-09-16, inklusive de två förkastade måtten.

```
loften/
  CLAUDE.md                        denna fil
  docs/valmanifest_2026/           källdokumenten. PDF:erna ligger utanför git.
  docs/verklighetsbild_pilot/      FÖRKASTAT mått, nedlagt 2026-09-13
  docs/samstammighet_poc/          FÖRKASTAT mått, nedlagt 2026-09-16
  config/verklighetsbild/          korpusarna, urvalet och pilotens resultat
  config/samstammighet_poc/        POC:ens resultat
```

Koden ligger kvar i `pipeline/tools/` och proven i `tests/`, eftersom de är paket och inte
dokument.

### De två förkastade måtten är arkiv

Dokumenten under `docs/verklighetsbild_pilot/` och `docs/samstammighet_poc/` **ändras aldrig**.
Två av dem är dessutom hashpinnade i sitt eget resultat, så en ändrad bokstav fäller ett prov.

Följden: deras relativa länkar skrevs före flytten. Står det `](../adr/...)` i en arkivfil menas
`docs/adr/...` i repots rot, inte en katalog under `loften/`. Länken lagas inte. Filen står som
den signerades.

Nya filer i spåret skriver förstås rätt länkar.

### Skillnaden mellan avslagsskäl och nedläggning

- **`avslagsskal.md`** betyder att måttet **föll på sin förhandsregistrerade tröskel**.
  Verklighetsbild gjorde det.
- **`nedlaggning.md`** betyder att måttet lades ned **av något annat skäl**. Samstämmighet klarade
  alla tre trösklarna, och lades ned därför att frågan byttes.

Ett prov i `tests/test_samstammighet_poc.py` vaktar skillnaden: ett mått som klarade sina
trösklar får inte bära ett avslagsskäl.

## Material

**Ligger i repot**

- `loften/config/verklighetsbild/korpus_framat.yaml`: 1 073 poster ur valmanifesten 2026, typen
  `detta ska vi göra`. Bär **rubriker och inte full text**. Noll poster bär ett årtal.
- `loften/config/verklighetsbild/korpus_bakat.yaml`: 896 poster, typen `detta är ett problem`.
- `config/budget_ramar.yaml`: partiernas egna föreslagna utgiftsramar, budgetåren 2011 till 2025.

**Saknas**

- Valmanifesten 2022.
- Budgetåret 2026, ur bet. 2025/26:FiU1.
- Full lydelse och sidnummer i korpusen.
- Regeringens propositioner, som regel 2 kräver.

## Frysningen

Framåtkorpusen är fryst till brytpunkten **2030-09-08** (ADR 0016 beslutspunkt 4). Ingen post får
ändras, läggas till eller tas bort. Ingen post prövas mot ett utfall före brytpunkten.

Att läsa filen är tillåtet. Att välja formulering, indikator eller tröskel i efterhand är det
frysningen hindrar.

## Hämtning av dokument

**Skriv ned URL och hämtdatum samtidigt som filen sparas.** Adresserna till valmanifesten 2026
skrevs aldrig ned och går inte att återskapa. Den luckan upprepas inte.

## Nedläggning är en godkänd utgång

Två mått i projektet har lagts ned med daterade avslagsskäl, och båda nedläggningarna var rätt
beslut. Faller detta spår skrivs ett avslagsskäl med prövbara återöppningsvillkor, i denna mapp.
