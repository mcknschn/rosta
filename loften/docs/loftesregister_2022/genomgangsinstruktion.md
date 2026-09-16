# Genomgångsinstruktion: strukturmappning av ett dokument

> Detta är instruktionen för **båda** de blinda genomgångarna i biljett
> [#54](https://github.com/mcknschn/rosta/issues/54). Den är låst och lika för A och B.
> Beslut 7 i [beslutsdokumentet](../beslut/2026-09-16-sparets-form.md) kräver att de två
> genomgångarna får samma instruktion och arbetar i skilda kontexter.

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

## Vad som inte är en post

- Rubriker, kapitelrubriker och mellanrubriker.
- Löpande brödtext, inledningar och resonemang som inte står som en punkt i en lista.
- Den rad som annonserar listan, alltså raden som slutar med kolon.
- Innehållsförteckning, sidnummer, sidhuvud och sidfot.
- Tryckortsuppgifter, ISBN, upplaga, grafisk form, webbadresser och konton i sociala
  medier.
- Bildtexter, diagramrubriker, axeltal och sifferetiketter i figurer.
- Partiledarens förord och namnunderskrift.
- Slagord och uppmaningar att rösta.

En punkt är en post även när innehållet ligger utanför de sju kategorier Rösta mäter
(beslut 9). Ingen punkt sorteras bort på ämne.

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
