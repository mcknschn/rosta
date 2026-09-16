# Arkivet

Här ligger de låsta registren från tidigare versioner av genomgångsinstruktionen,
med sina genomgångar och sin differens. **Filerna ändras aldrig.** Var och en bär
sin egen `innehall_sha256`, räknad på filens innehåll, och en ändrad bokstav faller
i `tests/test_loftesregister_2022.py`.

## Vilken instruktion varje register kördes under

De arkiverade registren pinnar instruktionen med en **sökväg**, inte med en hash.
Sökvägen pekar på den levande filen, som sedan skrevs om. Raden
`instruktion: '../../docs/loftesregister_2022/genomgangsinstruktion.md'` i ett
arkiverat register säger alltså ingenting om vilken regel som gällde när det byggdes.

Den här tabellen säger det i stället. Instruktionsfilerna ligger här bredvid, tagna
ur git-historiken.

| Register | Poster | Instruktion | `sha256_text` |
| --- | --- | --- | --- |
| `register_version2.yaml` | 729 | [`genomgangsinstruktion_version2.md`](genomgangsinstruktion_version2.md) | `518050de163cd054b218453c2eb8db54affcaf74246c71173876d376fde720ee` |
| `register_version3.yaml` | 1120 | [`genomgangsinstruktion_version3.md`](genomgangsinstruktion_version3.md) | `468a8afa73cc21d64cfb5bf120342882223848492c0a54fb26852029ed14936f` |

`v_genomgangar_version1.yaml` är V:s första två genomgångar, körda under version 1.
Den versionen gick inte att tillämpa på V och finns beskriven i instruktionens
ändringsnot för version 2.

Hashen är räknad med `sha256_text`, alltså med radsluten normaliserade, precis som
för PDF:erna och underlagen. Det talet är detsamma på Windows och Linux.

## Varför luckan uppstod, och hur den är tilltäppt

Version 4 av instruktionen kom ur en kodgranskning som fann just det här: ett register
som hänvisar till en regel det inte kördes under. Från och med version 4 bär registret
två nya fält, `instruktion_version` och `instruktion_sha256`, och ett register kan
därför aldrig mer tappa bort sin egen regel.

De arkiverade registren får inga sådana fält i efterhand. Att lägga till en rad i en
arkiverad fil skulle bryta dess `innehall_sha256`, och då vore låsningen ingen låsning.
Den här filen är svaret i stället.
