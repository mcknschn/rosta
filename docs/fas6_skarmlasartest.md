# Fas 6 — manuellt skärmläsartest (backlogg F2)

> Sista öppna punkten i WCAG 2.2 AA-genomgången. Automatiken i
> [done/fas6_wcag.md](done/fas6_wcag.md) täcker DOM- och ARIA-kontraktet samt fokusbeteendet.
> Den kan inte höra vad som faktiskt läses upp. Det här protokollet gör den delen.
>
> **Utförare:** en människa med skärmläsare. Räkna med 20 minuter.
> **Status:** ⬜ ej utförd

## Förberedelse

```powershell
cd <repo>
python -m http.server 8000
# öppna http://localhost:8000/web/
```

Använd **NVDA på Windows** (gratis, nvaccess.org) med Firefox eller Chrome. VoiceOver på macOS med
Safari fungerar likvärdigt. Slå på skärmläsaren innan sidan laddas.

Kortkommandon i NVDA: `NVDA+ned` läser vidare, `H` hoppar rubrik, `D` hoppar landmärke,
`Tabb` flyttar fokus, `NVDA+mellanslag` växlar mellan bläddrings- och fokusläge.

## Testfall

Fyll i utfall och skriv vad du faktiskt hörde. "Verkar ok" räcker inte, skriv uppläsningen.

### 1. Skip-länken

1. Ladda om sidan. Tryck `Tabb` en gång utan att röra musen.

- [ ] Första fokus är "Hoppa till innehållet"
- [ ] Enter flyttar fokus till huvudinnehållet, och nästa uppläsning kommer därifrån

Hörde: `___`

### 2. Rubrikhierarki

1. Tryck `H` upprepade gånger från sidans topp.

- [ ] Ordningen är logisk: Rösta (h1), sedan Dina vikter, Rangordning, Så funkar det
- [ ] Inget hopp från h1 till h3, inga tomma rubriker

Hörde: `___`

### 3. Förbehållsbannern

1. Läs sidans början med `NVDA+ned`.

- [ ] Bannern läses upp före rangordningen, inte efter
- [ ] Texten "Demonstration, inte färdigt röstråd" uppfattas som en anmärkning, inte som brödtext
- [ ] Coverage-texten under den är begriplig som uppläst löptext, inte en ordsallad

Hörde: `___`

> Coverage-texten är lång och tekniskt tät. Om den är obegriplig uppläst, notera det. Det är i så
> fall ett verkligt fynd som bör leda till en kortare sammanfattning i gränssnittet.

### 4. Sliders (viktreglagen)

1. Tabba till första reglaget. Ändra värdet med piltangenterna.

- [ ] Reglaget presenteras med kategorinamn, aktuellt värde och att det är ett reglage
- [ ] Varje piltryck läser upp det **nya** värdet
- [ ] Namnet upprepas inte irriterande vid varje litet steg

Hörde: `___`

### 5. Live-status vid omräkning (4.1.3)

Detta är det viktigaste fallet. `#status` är `role="status"`, `aria-atomic`, med 350 ms debounce.

1. Dra ett reglage snabbt fram och tillbaka i ett par sekunder.

- [ ] Skärmläsaren läser **inte** upp alla åtta partikort vid varje litet steg
- [ ] När du släpper kommer en kort sammanfattning, ungefär "Rangordning uppdaterad. Etta: …"
- [ ] Sammanfattningen avbryter inte det du håller på att läsa på ett störande sätt

Hörde: `___`

### 6. Expanderbart bevisspår

1. Tabba till ett partikort och expandera det med Enter, sedan med Mellanslag.

- [ ] Elementet presenteras med roll knapp och tillstånd hopfällt eller expanderat
- [ ] Tillståndet läses om när du växlar
- [ ] Det expanderade innehållet går att nå med fortsatt läsning, fokus tappas inte

Hörde: `___`

### 7. Fokus överlever omräkning

Detta var det blockerande felet som åtgärdades i juni. Kontrollera att det håller.

1. Expandera ett partikort. Låt fokus ligga kvar i det. Ändra en vikt så att rankingen ändras.

- [ ] Fokus ligger kvar på samma element, hoppar inte till sidans topp
- [ ] Kortet är fortfarande expanderat

Hörde: `___`

### 8. Betygstabellen A/B/C/D

1. Navigera in i ett expanderat korts tabell.

- [ ] Kolumnrubrikerna kopplas till cellerna vid uppläsning
- [ ] Bokstäverna A, B, C och D får sin betydelse uppläst, antingen ur rubriken eller ur
      förklaringsraden under tabellen

Hörde: `___`

### 9. Felläget

1. Stäng servern och ladda om sidan.

- [ ] Felmeddelandet läses upp automatiskt, det är `role="alert"`
- [ ] Texten är på svenska och säger vad användaren ska göra

Hörde: `___`

## Utfall

| Fall | Resultat | Anteckning |
|---|---|---|
| 1 Skip-länk | ⬜ | |
| 2 Rubriker | ⬜ | |
| 3 Banner | ⬜ | |
| 4 Sliders | ⬜ | |
| 5 Live-status | ⬜ | |
| 6 Expandering | ⬜ | |
| 7 Fokus | ⬜ | |
| 8 Tabell | ⬜ | |
| 9 Fel | ⬜ | |

**Skärmläsare och version:** `___`
**Webbläsare:** `___`
**Datum:** `___`

## Efter testet

Rapportera utfallet. Fynd i fall 5, 6 eller 7 är blockerande för AA-anspråket och åtgärdas direkt.
Fynd i fall 3 eller 8 är förbättringar som förs in i backloggen. När protokollet är ifyllt och
eventuella blockerare är åtgärdade: uppdatera "TODO (manuell)" i
[done/fas6_wcag.md §5](done/fas6_wcag.md) och bocka av F2 i [BACKLOG.md](BACKLOG.md).
