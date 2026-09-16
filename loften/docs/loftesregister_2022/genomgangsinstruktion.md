# Genomgångsinstruktion: strukturmappning av ett dokument

> Detta är instruktionen för **alla** de blinda genomgångarna i biljett
> [#54](https://github.com/mcknschn/rosta/issues/54). Den är låst och lika för varje
> genomgång. Beslut 7 i [beslutsdokumentet](../beslut/2026-09-16-sparets-form.md) kräver att
> genomgångarna får samma instruktion och arbetar i skilda kontexter.
>
> **Version 4, 2026-09-16.** Ändringarna mot tidigare versioner står längst ned.

## Uppgiften

Uppgiften är **avskrift och strukturmappning**: att peka ut var dokumentets egna
listpunkter och stycken börjar och slutar i ett radnumrerat textunderlag.

Uppgiften är **inte** att bedöma, rangordna, sammanfatta eller kommentera innehållet.
Ingen post ska värderas. Ingen post ska formuleras om. Ingen text ska skrivas av för
hand. Utdata är radnummer, ingenting annat.

## Underlaget

Underlaget ligger i `loften/underlag/valmanifest_2022/<parti>.txt`. Det är utvunnet ur
dokumentets PDF med `pipeline/tools/loftesregister.py` och är deterministiskt.

Varje textrad har formen

```
radnummer|sidnummer|markör|text
```

Markören är `*` när raden inleds med en listmarkör i PDF:en, annars `.`.

Rader som börjar med `#` är satsens form och inte dokumentets text:

- `# ---- sida N ----` är en sidbrytning i PDF:en.
- `# ---- block grad G ----` är ett nytt textblock, alltså dokumentets egen styckning.
  `G` är blockets dominerande textgrad i punkter, mätt i PDF:en.

### Graden, och vad den inte kan

Graden säger hur stort blocket är satt. Talet är ett faktum om satsen och inget omdöme om
texten.

Graden avgör **en enda fråga, och bara åt ett håll**: den kan visa att ett block INTE är
en rubrik. Den kan aldrig visa att ett block ÄR en rubrik.

```
# ---- block grad 15.5 ----
189|6|.|KLIMATET KRÄVER VÅR HANDLINGSKRAFT

# ---- block grad 9.7 ----
190|6|.|Framtiden är grön.

# ---- block grad 9.7 ----
191|6|.|Centerpartiet sätter klimatet först, för att framtiden måste vara grön.
```

Rad 190 står i samma grad som stycket under. Den är alltså ingen rubrik, hur mycket den än
låter som ett slagord.

**Graden gör inte mer än så.** Ett block satt större än texten omkring kan vara en rubrik,
men det kan lika gärna vara en bildtext eller en ingress. Det finns ingen gräns i punkter
över vilken ett block blir en rubrik, och instruktionen sätter ingen.

Mätt på hela korpusen står mellan 0 och 96 procent av det som ska uteslutas på
brödtextgrad: C:s innehållsförteckning, M:s bildtexter, MP:s numrerade kapitelrubriker.
Graden utesluter ett fel. Den ersätter ingen läsning.

**Jämför alltid med blocken närmast omkring, aldrig med ett tal ur ett annat dokument.**
De åtta dokumenten sätter olika grader, och ett och samma dokument kan sätta två
brödtextgrader. KD sätter till exempel sin löpande text i 11,0 punkter och sina listpunkter
i 10,0. Båda är brödtext.

Skulle ett block sakna grad står det `# ---- block grad ? ----`. Avgör då på de övriga
reglerna. I 2022 års korpus har varje block en grad.

## Ordningen

Reglerna gäller i tre steg, och ett tidigare steg går före ett senare.

1. **Rensa bort satsens egna delar.** Se `Vad som inte är en post`, steg 1. Ett block som
   faller där är aldrig en post, och det avgörs utan att något annat prövas först.
2. **Peka ut posterna bland det som är kvar.** Se `Vad en post är`. Bär blocket markörer
   eller löpnummer är varje punkt en post. Bär det inga är hela blocket en post. Här, och
   först här, faller också annonseringsraden bort, se `Vad som inte är en post`, steg 2.
3. **Foga ihop det satsen brutit isär.** Se princip 1 och `När en post bärs av flera spann`.

De tre principerna avgör tveksamma fall inom steget de hör till. De upphäver aldrig ett
tidigare steg.

## Vad som inte är en post

Listan har två delar, och de hör till olika steg i `Ordningen`.

### Steg 1: satsens egna delar

Dessa faller bort överallt, och det avgörs utan att något annat prövas först. Om avsnittet
bär en lista eller inte spelar ingen roll.

- Rubriker, kapitelrubriker och mellanrubriker.
- Innehållsförteckning, sidnummer, sidhuvud och sidfot.
- Tryckortsuppgifter, ISBN, upplaga, grafisk form, webbadresser och konton i sociala
  medier.
- Bildtexter, diagramrubriker, axeltal, sifferetiketter i figurer och källrader.
- Partiledarens namnunderskrift.
- Slagord och uppmaningar att rösta som står i ett eget block och inte i sidans
  brödtextgrad.

### Steg 2: annonseringsraden

Bara en sak faller bort här, och den avgörs när blockets poster är utpekade.

- Den rad som annonserar en lista, alltså raden som slutar med kolon och säger att en
  uppräkning följer.
  **Undantag:** bär raden både slutet på en sats som redan är en post och annonseringen,
  hör raden till satsen och tas med. Raden är den minsta enhet ett spann kan peka på, och
  en avhuggen mening är ett större fel än en annonsering för mycket.

En punkt är en post även när innehållet ligger utanför de sju kategorier Rösta mäter
(beslut 9). Ingen punkt sorteras bort på ämne.

### Att känna igen satsens egna delar kräver att blocket läses

Ett sidnummer, ett axeltal, en källrad och en innehållsförteckning känns igen på vad de
är. Det kräver att blocket läses, och det är tillåtet. Det är något annat än att låta
innehållet avgöra om ett stycke är för vagt eller för retoriskt för att vara ett löfte.
Se princip 3.

M:s sida 16 bär ett diagram. Blocken `jan feb mar apr maj`, `0`, `50`, `100`,
`Elpris öre/kWh, södra Sverige` och `Källa: Vattenfall` hör till diagrammet. Två av dem
står i sidans brödtextgrad. Graden hjälper inte, läsningen gör det.

**Här finns ingen mekanisk regel, och instruktionen låtsas inte om att det gör det.**
Underlaget säger inte vilka block som hör till en figur. PDF:ens egna ritobjekt täcker bara
diagramfältet, inte bildtexten över eller källraden under, så inget mått i satsen pekar ut
dem heller. Igenkänningen är genomgångens egen.

Det är just därför genomgångarna körs blint och flera gånger. Skiljer de sig åt på ett
sådant block faller det ut som en differens och avgörs av projektägaren, med båda
lydelserna framför sig. Kontrollen ligger i förfarandet och inte i regeln.

## Vad en post är

En **post** är ett stycke eller en listpunkt i dokumentets egen text.

Enheten är den **finaste nivå dokumentet självt markerar**, och underlaget visar två
nivåer. Blocket är dokumentets egen styckning. Markören och löpnumret är dokumentets egen
listindelning inom ett block.

Regeln har därför bara två led:

1. **Bär blocket listsignaler, är varje punkt en post.** En listsignal är markören `*`
   eller ett inledande löpnummer, alltså `1.`, `2.`, `12.` och så vidare. Signalen börjar en
   ny post, och posten löper till raden före nästa listsignal, eller till blockets slut.
2. **Bär blocket inga listsignaler, är hela blocket en post.**

Posten bär **hela punkten**: den inledande meningen och den förklaring som står i samma
block. Den förkortas aldrig. Punkterna slås aldrig ihop och styckas aldrig upp av
genomgången.

Det finns ingen tredje regim, och inget avsnitt behöver klassas som listbärande eller
listlöst. Ett dokument som bara skriver löpande text och ett som skriver rena listor
behandlas av samma två led.

### Raderna före blockets första listsignal

**Listsignal** betyder här markören `*` eller ett inledande löpnummer. De två behandlas
lika överallt i instruktionen.

Ett block kan bära både löpande text och listpunkter. MP:s block 3 gör det: raderna 6 och 7
är löpande text, och raderna 8 till 10 bär var sin markör.

**Bär ett block listsignaler, och finns det rader före blockets första listsignal, är de
raderna en post för sig.** De faller inte bort. Det enda som faller bort är annonseringen,
se `Vad som inte är en post`, och bär raden både en sats slut och annonseringen tas hela
raden med.

Regeln rör bara raderna före den första listsignalen. Raderna därefter är redan fördelade
på poster av huvudregelns första led, och tas aldrig en gång till.

Skälet är version 3:s eget skäl. Ett stycke ska inte falla ur registret för att partiet
råkade sätta det i samma block som sin lista. C sätter sin inledning i ett eget block och
får den med. MP sätter sin i samma block som listan. Samma text ska behandlas lika.

### Fyra av de åtta dokumenten bär inga markörer alls

SD, V, KD och L sätter ingen listmarkör och inget löpnummer i hela dokumentet. För dem
gäller alltså bara led 2: varje block är en post. S, M, C och MP bär markörer i 40, 253, 95
respektive 23 block av sina 161, 792, 310 och 50.

Det är den ojämnheten hela regeln finns till för. Talet i registret ska mäta partiets
löften och inte partiets typografi.

## De tre principerna

De tre principerna avgör tveksamma fall. De avgjorde alla femton differenser mellan den
förra körningens genomgångar, och de står här för att genomgången ska kunna tillämpa dem i
stället för att skilja sig åt och få dem tillämpade efteråt. Ingen princip upphäver ett
tidigare steg i `Ordningen`.

Fallen under varje princip är exempel som visar hur principen faller ut. De är inte egna
regler, och ett annat dokument kan se annorlunda ut.

### Princip 1: ett stycke är ett stycke

Blockgränsen avgör var ett stycke börjar och slutar. Två block som båda är poster är två
poster, hur nära varandra de än står.

Undantaget är **en mening som satsen brutit mellan två block**. Den hör ihop, och de två
delarna bärs av samma post. Provet är språkligt och inte typografiskt:

> Det första blocket slutar utan avslutande skiljetecken, och nästa block börjar med
> gemen bokstav.

Slutar det första blocket med punkt är det ett eget stycke.

**Provet gäller aldrig när nästa block bär en listsignal.** Börjar nästa block med en
listsignal är det en ny post, vad det första blocket än slutade med. En listsignal går
alltid före det språkliga provet.

**Förklaringen hör till punkten bara när den står i samma block.** `Vad en post är` säger
att posten bär hela punkten, alltså den inledande meningen och förklaringen. Det gäller
inom blocket. Står förklaringen i ett eget block är den ett eget stycke, och alltså en egen
post, om inte meningen brutits mellan de två.

Exempel: M:s rad 904-910 slutar `...för energiförsörjningens skull.` och rad 911 börjar
`Vi ska som land ta fullt ansvar...`. Två stycken, alltså två poster.

### Princip 2: satsens egna delar är inte löften

En figur bär bildtext, axeltal, sifferetiketter, källrad och sin egen rubrik. De hör till
figuren, inte till partiets löften, och de är inte poster. Det gäller även när de står i
ett eget block, även när de står i brödtextgrad, och även när orden låter som ett förslag.

Den här principen hör till steg 1 i `Ordningen` och går därför före princip 1 och 3.

Exempel: M sätter `Regeringens stängning av Ringhals 1 och 2 leder till att utsläppen i EU
ökar med 8 miljoner ton` i samma block som talen `8`, `miljoner` och `flygresor`. Det är
infografikens bildtext.

### Princip 3: innehållet avgör aldrig om ett stycke är för svagt för att vara ett löfte

Det som förbjuds är att utesluta ett stycke för att det låter för vagt, för retoriskt eller
för litet. Det provet görs senare, av handlingsprovet i beslut 6, och att göra det här är
att göra det två gånger, en gång utan nedskriven regel.

Det som är tillåtet, och nödvändigt, är att läsa ett block för att se **vad satsen lade
dit**: ett sidnummer, ett axeltal, en källrad, en innehållsförteckningsrad.

Graden hjälper åt ett håll och bara ett. Står blocket i samma grad som texten omkring är
det ingen rubrik, och då faller det inte bort som rubrik. Står det större säger graden
ingenting: det kan vara en rubrik, en bildtext eller en ingress, och vilket av dem avgörs
av läsningen enligt princip 2.

Exempel: C sätter `Framtiden är grön.` i 9,7 punkter, alltså sidans brödtextgrad, med
rubriken `KLIMATET KRÄVER VÅR HANDLINGSKRAFT` i 15,5 punkter över. `Framtiden är grön.` är
inget rubrikblock, alltså ett stycke, alltså en post.

## När en post bärs av flera spann

Satsen kan lägga något mitt i en post. Det som satsen lade dit hör inte till posten, och
posten hoppar över det. Posten bärs då av **flera radspann**: `85-86,89-92`.

Det gäller allt satsen lägger emellan, inte bara sidbrytningen:

- sidnummer och sidhuvud, när punkten börjar på en sida och slutar på nästa
- en bildtext eller en diagramrubrik som bryter spalten
- sifferetiketter som hör till en figur

**Ett spaltbyte syns aldrig i underlaget, och behöver inte synas.** Läsordningen är redan
utredd när underlaget skrivs, så ett spaltbyte kommer ut som en vanlig blockgräns. Ligger
inget uteslutet block emellan är en punkt som bryts av ett spaltbyte ett enda spann.

**Två skilda frågor, i denna ordning.** Först: hör blocket däremellan till posten? Det
avgörs av steg 1, alltså av `Vad som inte är en post`, och aldrig av det språkliga provet.
Sedan: är de två delarna en post eller två? Det avgörs av det språkliga provet i princip 1.

Faller blocket däremellan inte bort i steg 1, är det en egen post och de två delarna är två
poster.

Exempel: M:s sida 16. Rad 915 är bildtexten `Nya elprisrekord varje månad` och faller bort i
steg 1. Rad 914 slutar `och innovativa tekniker som minskar eller tar` och rad 916 börjar
`bort utsläppen.`, så de två delarna är en post. Den skrivs `911-914,916-918`. Alla tre
raderna står på samma sida, och ingen sidbrytning är inblandad.

## Utdata

En YAML-fil med två nycklar. Inget annat.

```yaml
dokument: XX
poster:
  - "81-84"
  - "85-86,89-92"
  - "93-97"
```

- `dokument` är partiets kod, alltså filnamnet utan ändelse och med versaler.
- `poster` är en lista av radspann, i den ordning de står i dokumentet.
- Ett spann skrivs `start-slut`. En post som hoppar över rader skrivs som flera spann
  åtskilda av komma, utan mellanslag.
- Posterna numreras inte. Numret sätts senare, ur postens plats i dokumentet.

## Kraven på genomgången

1. **Hela dokumentet läses.** Genomgången slutar inte vid en viss sida eller ett visst
   antal poster.
2. **Ingen rad tas av två poster.** Spannen överlappar aldrig varandra.
3. **Varje rad i ett spann finns i underlaget.** Radnumren skrivs av, aldrig av minnet.
4. **Inga poster utelämnas för att de liknar varandra.** Står samma förslag två gånger i
   dokumentet blir det två poster.
5. **Ingen post slutar mitt i en mening.** Slutar en posts sista spann utan avslutande
   skiljetecken, och fortsätter meningen på nästa rad, är posten avhuggen. Läs princip 1
   och `När en post bärs av flera spann`.
   **Undantag:** bär nästa rad en listsignal är posten slut ändå, och nästa rad börjar en
   ny post. En listsignal går före det språkliga provet.

## Ändringar

### Version 4, 2026-09-16: en regel i stället för två regimer, och graden i underlaget

Version 3 gav 1120 poster i tre genomgångar, varav 1106 var eniga. De femton skiljaktiga
fallen avgjordes efter tre principer som inte stod i instruktionen. En kodgranskning fann
tre fel, och en korsläsning i tre rundor av en andra modell i eget sammanhang fann
ytterligare femton. Det är den korsläsning instruktionens egen lärdom från version 2 kräver
och som varken version 2 eller version 3 fick.

**1. Två regimer har blivit en.** Version 3 hade fyra listsignaler för avsnitt med lista
och en styckeregel för avsnitt utan. Vilken regim som gällde avgjordes av om avsnittet bar
en lista, och vad som hörde till listan avgjordes av regimen. Korsläsningen visade att
cirkeln inte går att laga med en gränsregel: signal 3 pekar ut block som inte bär någon
signal, så gränsen kan inte läsas ur underlaget.

Regeln har nu två led och ingen regim. Bär blocket markörer eller löpnummer är varje punkt
en post. Bär det inga är hela blocket en post.

Mätningen säger varför det duger: **fyra av de åtta dokumenten, SD, V, KD och L, bär inte en
enda listmarkör.** För dem var de fyra signalerna redan verkningslösa, och styckeregeln var
det enda som gällde. De fyra andra bär markörer i 40, 253, 95 och 23 block. Den enda regel
som behövs är den som säger vad en markör gör inom ett block.

**2. Graden ligger nu i underlaget.** Princip 3 säger att typografin och inte innehållet
avgör rubrikfrågan, men underlaget bar bara radnummer, sida, markör och text. Ingen
genomgång kunde se en textgrad. Principen var inte tillämpbar, och `Framtiden är grön.`
uteslöts av två genomgångar av tre, som läste den som ett slagord.

Blocket bär nu sin dominerande textgrad, mätt i PDF:en. Ändringen flyttar ingen textrad:
alla åtta underlag är byte för byte oförändrade på varje rad som bär partiets text, och
bara annoteringsraderna är nya. Varje block i alla åtta dokument fick en grad.

**Graden räcker inte, och instruktionen säger det.** Mätt på hela korpusen står mellan 0 och
96 procent av det som ska uteslutas på brödtextgrad. Ett första utkast påstod att ett större
block är en rubrik. Korsläsningen fällde det: M:s bildtext på sida 16 är satt i 14 punkter
mot brödtextens 11. Graden kan nu visa att ett block INTE är en rubrik, aldrig att det är.

**3. Ordningen står utskriven.** Tre steg, där ett tidigare går före ett senare: rensa bort
satsens egna delar, peka ut posterna bland det som är kvar, foga ihop det satsen brutit
isär. Uteslutningslistan är delad efter steg, eftersom en del av den gällde överallt och en
del berodde på avsnittet. Den kortare listan för listlösa avsnitt är borta, och med den den
lucka som lät förordets stycken hamna mellan två listor.

**4. De tre principerna står nedskrivna**, med sina fall märkta som exempel. De avgjorde
femton differenser av femton och hörde hemma i instruktionen innan genomgångarna kördes.

**5. En rad som bär både en sats slut och annonseringen tas med.** Posten S-066 slutade
`för att trygga vår`. Orden `fred och frihet.` stod på nästa rad, som i sin helhet lyder
`fred och frihet. Därför vill vi att:`. Alla tre genomgångarna uteslöt hela raden för att bli
av med annonseringen, och tappade meningens slut med den. En mätning på hela registret gav
**ett enda sådant fall av 1120 poster**. Kravlistan bär nu provet, och verktygets
`kontroll`-kommando räknar avhuggna poster.

**6. Flerspannsregeln gällde bara sidbrytningen.** Texten sade att två block aldrig slås ihop
`utom när sidbrytningen delat ett och samma stycke`. Två av de femton avgörandena bryter mot
den texten, och båda med rätta: M:s sida 16 fogar ihop två block över en bildtext utan någon
sidbrytning. Regeln är nu skriven som den tillämpades, som två skilda frågor i given ordning.

Spaltbytet är samtidigt struket ur listan över vad en genomgång måste känna igen.
Läsordningen är utredd innan underlaget skrivs, så ett spaltbyte kommer ut som en vanlig
blockgräns. Av registrets 29 flerspannsposter är ingen ett rent spaltbyte: i luckorna ligger
sidnummer, sidhuvuden, källrader, axeltal och bildtexter.

**7. Raderna före blockets första listsignal är en post.** Version 3 lät dem falla som
inledning. Det slog bara till på ett ställe i korpusen, MP:s block 3, där 259 tecken löpande
text stod i samma block som tre listpunkter. C sätter sin inledning i ett eget block och fick
den med. Samma text ska behandlas lika, och det var version 3:s eget skäl.

**8. Fyra luckor till kom ur korsläsningen.** En listsignal går före det språkliga provet, så
ett block som börjar med `*` alltid är en ny post, och kravlistan bär samma undantag.
Förklaringen hör till punkten bara när den står i samma block. Löpnumrets post slutar vid
nästa löpnummer eller vid blockets slut. Och princip 3 sade fortfarande att graden avgör
rubrikfrågan, vilket motsade avsnittet om graden.

**9. Ett fynd står kvar och rättas inte.** Underlaget säger inte vilka block som hör till en
figur. PDF:ens ritobjekt täcker bara diagramfältet, inte bildtexten över eller källraden
under, så inget mått i satsen pekar ut dem. Där finns ingen mekanisk regel. Instruktionen
säger det rent ut och pekar på var kontrollen ligger i stället: genomgångarna körs blint och
flera gånger, och skillnaderna avgörs av projektägaren.

**Följden:** alla åtta dokument körs om, alla genomgångar, under version 4.

Registret från version 3 ligger kvar i
[`arkiv/register_version3.yaml`](../../config/loftesregister_2022/arkiv/register_version3.yaml)
tillsammans med sina genomgångar och sin differens, och ändras aldrig. Instruktionens
version 2 och 3 ligger som filer i samma katalog, se
[`arkiv/LASMIG.md`](../../config/loftesregister_2022/arkiv/LASMIG.md).

### Version 3, 2026-09-16: klausulen flyttad från dokument till avsnitt

Version 2 band styckeregeln till hela dokumentet: bar dokumentet en lista någonstans gällde
de fyra signalerna överallt, också i kapitel utan lista. Den klausulen gjorde registret
osymmetriskt mellan dokumenten.

En mätning på det låsta registret, gjord i två pass som gav samma tal, visade följden. Av
dokumentens brödtext låg 379 stycken utanför registret, tillsammans 104 677 tecken. De låg
inte där jag först antog, alltså i inledningar före en lista. För C och M var det
kapiteltexten själv, skriven i prosa och med uttryckliga förslag i sig. S:s slutkapitel
`En stark global röst` bar hela partiets utrikespolitik i åtta stycken utan en enda punkt.

Andelen av brödtexten som föll utanför:

| Dokument | Andel utanför |
| --- | --- |
| C | 62 % |
| M | 61 % |
| S | 38 % |
| SD | 36 % |
| KD | 34 % |
| L | 33 % |
| MP | 20 % |
| V | 0 % |

V, som bara skriver löpande text, fick hela sitt dokument i registret. C, som skriver både
lista och löpande text, fick bara listan. Talet mäter då dokumentets typografi och inte
partiets löften, och det går åt olika håll för olika partier.

Att V:s egna poster redan bär problembeskrivningar utan åtgärd, vilket version 2 slog fast
med avsikt, gör saken tyngre. Registret blandar redan. Att låta samma regel gälla listlösa
avsnitt i de andra dokumenten gör dem mer lika V, inte mindre.

**Följden:** alla åtta dokument körs om, båda genomgångarna, under version 3. V är
kontrollfallet: V bär ingen lista, så V:s avsnitt är hela dokumentet, och V:s resultat ska
stå stilla. Gör det inte det är regeln inte den jag tror att den är.

Det låsta registret från version 2 ligger kvar i
[`arkiv/register_version2.yaml`](../../config/loftesregister_2022/arkiv/register_version2.yaml)
och ändras aldrig.

### Version 2, 2026-09-16: avsnittet `Dokument utan liststruktur` tillagt

Version 1 gick inte att tillämpa på V:s valplattform, som saknar lista helt. Den sade två
saker som inte kan gälla samtidigt för ett sådant dokument:

- enheten är den finaste nivå dokumentet självt markerar, vilket för V är stycket, och
- löpande brödtext är inte en post, vilket träffar vart och ett av V:s stycken.

Följer man den första regeln har V 77 poster. Följer man den andra har V noll. Båda
genomgångarna gjorde i stället något tredje: de tog 50 brödtextstycken var och sållade på
innehåll utan att skriva ned sållet. De sållade lika i 67 fall och olika i 10. Fem stycken
som **båda** uteslöt beskriver ett problem utan att namnge en åtgärd, vilket är
handlingsprovet i beslut 6 tillämpat ett steg för tidigt.

Motsägelsen är av samma slag som den i pilotkodboken, där avsnitt 6.5 stred mot avsnitt 10
och tre kodare löste den åt olika håll. Spårets andra lärdom säger att kodboken ska korsläsas
innan den låses. Version 1 blev inte korsläst.

**Följden:** V körs om, båda genomgångarna, under version 2. Den första körningen ligger kvar
i [`arkiv/v_genomgangar_version1.yaml`](../../config/loftesregister_2022/arkiv/v_genomgangar_version1.yaml)
och ändras aldrig.

**De sju andra dokumenten körs inte om.** Alla sju bär en lista, så klausulen kan inte falla
ut för dem, och ingen annan rad i instruktionen är ändrad. Deras två genomgångar gav samma
svar på 661 poster av 661.
