# Genomgångsinstruktion: strukturmappning av ett dokument

> Detta är instruktionen för **båda** de blinda genomgångarna i biljett
> [#54](https://github.com/mcknschn/rosta/issues/54). Den är låst och lika för A och B.
> Beslut 7 i [beslutsdokumentet](../beslut/2026-09-16-sparets-form.md) kräver att de två
> genomgångarna får samma instruktion och arbetar i skilda kontexter.
>
> **Version 3, 2026-09-16.** Ändringarna mot tidigare versioner står längst ned.

## Uppgiften

Uppgiften är **avskrift och strukturmappning**: att peka ut var dokumentets egna
listpunkter börjar och slutar i ett radnumrerat textunderlag.

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
- `# ---- block ----` är ett nytt textblock, alltså dokumentets egen styckning.

## Vad en post är

En **post** är en punkt i dokumentets egen lista över vad partiet vill göra.

Enheten är den **finaste nivå dokumentet självt markerar**. Markerar dokumentet varje
åtgärd som en egen punkt är varje punkt en post. Buntar dokumentet flera åtgärder i en
punkt är den punkten en post. Punkterna slås aldrig ihop och styckas aldrig upp av
genomgången.

Fyra signaler pekar ut en post. De gäller i denna ordning:

1. **Markören `*`.** Raden börjar en ny post. Posten löper till raden före nästa `*`,
   eller till slutet av blocket.
2. **Ett löpnummer.** En rad som börjar med `1.`, `2.`, `12.` och så vidare i en
   uppräkning börjar en ny post.
3. **En inledande rad som annonserar en lista.** Står det en rad som slutar med kolon och
   annonserar en uppräkning, är varje textblock därefter i uppräkningen en post.
4. **Ett eget block per förslag.** Sätter dokumentet varje förslag som ett eget block,
   med en inledande mening som säger vad som ska göras, är blocket en post.

Posten bär **hela punkten**: den inledande meningen och den förklaring som hör till den.
Den förkortas aldrig.

Bär en del av dokumentet ingen av de fyra signalerna, läs avsnittet
`Avsnitt utan liststruktur` nedan. Det avsnittet gäller då i stället.

## Vad som inte är en post

- Rubriker, kapitelrubriker och mellanrubriker.
- Löpande brödtext, inledningar och resonemang som inte står som en punkt i en lista.
  **Denna punkt gäller bara inom ett avsnitt som bär en lista.** Se
  `Avsnitt utan liststruktur` nedan.
- Den rad som annonserar listan, alltså raden som slutar med kolon.
- Innehållsförteckning, sidnummer, sidhuvud och sidfot.
- Tryckortsuppgifter, ISBN, upplaga, grafisk form, webbadresser och konton i sociala
  medier.
- Bildtexter, diagramrubriker, axeltal och sifferetiketter i figurer.
- Partiledarens förord och namnunderskrift.
- Slagord och uppmaningar att rösta.

En punkt är en post även när innehållet ligger utanför de sju kategorier Rösta mäter
(beslut 9). Ingen punkt sorteras bort på ämne.

## Avsnitt utan liststruktur

Ett dokument, eller en del av ett dokument, kan sakna lista helt: ingen listmarkör, inget
löpnummer, och ingen rad som annonserar en uppräkning. Då är den finaste nivå dokumentet
självt markerar **stycket**, och **varje stycke i den löpande texten är en post**.

Ett **listlöst avsnitt** är en följd av block som ingen av de fyra signalerna rör. Det
börjar där föregående posts sista rad slutar, eller vid dokumentets början, och det slutar
på raden före nästa listsignal, eller vid dokumentets slut. Bär dokumentet ingen lista alls
är hela dokumentet ett enda listlöst avsnitt.

Fyra saker binder när regeln gäller:

1. **Regeln gäller avsnitt för avsnitt.** Ett dokument kan bära listor i några kapitel och
   löpande text i andra. Då gäller de fyra signalerna där listan står, och styckeregeln där
   den inte står. Att dokumentet bär en lista någon annanstans befriar inget avsnitt.
2. **Innehållet avgör aldrig.** Ett stycke som bara beskriver ett problem är en post lika
   mycket som ett stycke som namnger en åtgärd. Var stycket står i dokumentet avgör inte
   heller: ett stycke i inledningen och ett i slutkapitlet är poster på samma villkor som ett
   stycke mitt i ett sakkapitel.
3. **Bara satsens egna delar faller bort.** Listan under `Vad som inte är en post` ersätts
   här av en kortare: rubriker, bildtexter, diagramrubriker, sidnummer, sidhuvuden,
   innehållsförteckning, tryckortsuppgifter och namnunderskrifter. Ingenting annat utesluts.
   Ett stycke som slutar med en uppmaning att rösta är alltså en post, medan en rubrik som
   lyder `Rösta på partiet!` inte är det.
4. **Stycket är blocket.** Underlagets `# ---- block ----` är dokumentets egen styckning,
   och den avgör var ett stycke börjar och slutar. Två block slås aldrig ihop till en post,
   utom när sidbrytningen delat ett och samma stycke, se `Sidbrytningen` nedan.

Skälet till punkt 2: prövbarheten avgörs av handlingsprovet i beslut 6, i en senare biljett.
Sållar genomgången på innehåll redan här görs det provet två gånger, en gång utan nedskriven
regel. Ett stycke som utesluts här kan dessutom aldrig komma tillbaka, eftersom låsningen i
beslut 8 bara öppnar för avskrivningsfel.

## Sidbrytningen

En punkt kan börja på en sida och sluta på nästa. Däremellan ligger sidnummer och
sidhuvud i underlaget, och de hör inte till punkten. Posten hoppar då över dem, och bärs
av **flera radspann**: `85-86,89-92`.

Samma sak gäller en punkt som bryts av ett spaltbyte.

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

## Ändringar

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
