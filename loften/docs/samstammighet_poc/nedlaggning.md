# Nedläggning: Samstämmighet byggs inte

**Detta är inget avslagsskäl.** Måttet klarade alla tre trösklarna. Filen heter därför inte
`avslagsskal.md`, som i projektet betyder att ett mått föll på sin förhandsregistrerade
tröskel. Samstämmighet lades ned därför att frågan byttes.

- Datum: **2026-09-16**
- Beslutad av: projektägaren i biljett
  [#49](https://github.com/mcknschn/rosta/issues/49)
- Grundat på: [`besked.md`](besked.md) och [`resultat.md`](resultat.md)
- Föregångare: [Verklighetsbildpiloten](../verklighetsbild_pilot/avslagsskal.md), nedlagd 2026-09-13

Grillningen i #49 avgjorde aldrig sin fråga 0. Frågan togs i stället bort. Arbetet med
Samstämmighet läggs ned och materialet ligger kvar.

Detta är en godkänd utgång. Verklighetsbild lades ned på samma sätt 2026-09-13 och den viktade
stansen 2026-06-07.

## Skälet

Måttet skulle svara på om det finns ett glapp mellan två profiler: hur partiet fördelar sin
retorik över de sju kategorierna, och hur det fördelar sin kraft.

Projektägaren avgjorde 2026-09-16 att det inte är den fråga projektet vill ställa. Frågan är i
stället smalare: **vad lovar ett parti inför ett val, och har det sedan arbetat med det löftet?**

Samstämmighet kan inte svara på den frågan. Fyra hinder står i vägen, och inget av dem går att
lyfta genom att svara på fråga 0.

1. **Tidsaxeln går åt fel håll.** Korpusen är valmanifesten från 2026, alltså löften inför den
   kommande perioden. Handlingssidan är a1 med budgetåren 2011 till 2025, och A är förankrad mot
   samma fönster ([ADR 0005](../../../docs/adr/0005-a-forankras-i-tid-inte-i-faltet.md)). Måttet håller
   alltså ett löfte mot arbete som utfördes innan löftet gavs.
2. **Enheten är kategorin och inte löftet.** Ett parti kan lova en sak inom en kategori, arbeta
   med en annan sak inom samma kategori, och profilerna sammanfaller ändå.
3. **Riktningen saknas.** Öppen fråga 1 behandlar partiet som nämner något och arbetar emot det
   likadant som partiet som arbetar för det. Utan riktning går ingen uppfyllelse att avgöra.
4. **Ett omdöme är förbjudet.** Godkännandetest 3 förbjuder ett sammanvägt betyg, avståndet
   inverteras aldrig och rangordnas aldrig. Den nya frågan kräver just ett omdöme per löfte.

## Vad som inte var skälet

**Måttet föll inte på sina trösklar.** Det klarade alla tre, i den primära uppställningen och i
var och en av de fem varianterna. Skiljbarheten låg på 0,491 mot kravet 0,10, längdkonfunden på
-0,354 mot kravet 0,7, och blockskillnaden på 0,084 mot spridningen 0,167.

**Fråga 0 är obesvarad.** Villkoret i `besked.md` avsnitt 5 krävde att ingen kanal på
handlingssidan bär mer spridning än A:s normerade profil. Det provet kördes aldrig på a1 rå.
Måttet är alltså avfört och inte motbevisat.

Det spelar roll för hur beskedet ska läsas. Ett mått som faller på sin tröskel är prövat. Detta
mått är avfört därför att frågan byttes.

## Vad POC:en ändå slog fast

Tre fynd bär vidare, oberoende av att måttet lades ned.

1. **Trösklar som prövar hur talen fördelar sig kan inte upptäcka var talen kommer ifrån.**
   Profilavståndet korrelerade 0,998 med retorikens egen koncentration och 0,065 med handlingens.
   Alla tre trösklarna klarades ändå. Nästa förhandsregistrering i projektet ska bära minst ett
   prov som pekar på talens ursprung och inte bara på deras spridning.
2. **A:s normerade profil är nästan jämn.** Varje cell ligger mellan 0,123 och 0,165, alltså tätt
   runt 1/7. Det är en egenskap hos A som mått på prioritering mot en historisk förankring
   ([ADR 0005](../../../docs/adr/0005-a-forankras-i-tid-inte-i-faltet.md)) och ingen brist. A duger däremot
   inte som andel av kraft i ett annat mått. Förhandsregistreringen 3.2 skrev det före körningen,
   och utfallet höll.
3. **Kanalvalet avgör utfallet.** Byts handlingssidan från A till a1 rå korrelerar de två
   uppsättningarna -0,141, och SD går från lägst till högst. Ett mått vars rangordning vänder med
   kanalvalet kräver att kanalen motiveras före körningen.

## Vad beslutet inte rör

- **Betygen.** Samstämmighet hade vikt 0 och ingick aldrig i någon poäng, något band eller någon
  rangordning. Vikterna 0,30 A + 0,50 B + 0,20 D, C = 0 står kvar
  ([ADR 0002](../../../docs/adr/0002-kategoripoangens-ansprak-och-vikter.md)). `dist/` är orört.
- **Trösklarna i POC:en.** De var låsta före körningen och klarades. De skrivs inte om i
  efterhand.
- **Talen i `resultat.md`.** De får citeras som skiljbarhet och aldrig som samstämmighet, precis
  som `besked.md` punkt 4 slog fast.
- **Korpusen.** `config/verklighetsbild/` ligger kvar. Framåtkorpusen är fryst med brytpunkten
  2030-09-08 och rörs inte förrän dess.
- **Verklighetsbild.** De tre återöppningsvillkoren i
  [`../verklighetsbild_pilot/avslagsskal.md`](../verklighetsbild_pilot/avslagsskal.md) är orörda.

## Villkor för att ta upp frågan igen

Frågan tas upp igen om, och bara om, något av detta inträffar.

- **Löftesspåret behöver en kategoriprofil.** Visar det nya spåret att uppfyllelse per löfte inte
  går att mäta, och att en profil över kategorier är det enda som bär, då är fråga 0 åter levande.
  Då krävs en ny förhandsregistrering, och ett prov på talens ursprung enligt fynd 1 ovan.
- **En handlingssida med egen spridning skrivs.** Finns en kanal som bär spridning i samma
  storleksordning som retoriken, alltså tiofalt mer än A:s normerade profil, då är glappet värt
  att mäta om.

Ingen av de två är på väg att inträffa. Frågan är stängd tills vidare.
