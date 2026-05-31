# Fas 6 — WCAG 2.2-genomgång (tillgänglighet)

Genomgång av frontenden i [`web/`](../web/) mot **WCAG 2.2 nivå AA**. Målnivån i ROADMAP
(task 6.6) är AA. Genomgången är gjord på källkoden + automatiserad mätning (kontrast och
reflow via Playwright/Chromium). Punkter markerade **TODO (manuell)** kräver test med riktig
skärmläsare och täcks inte automatiskt.

Status: **AA uppfyllt för de granskade kriterierna nedan.** Det enda blockerande felet som
hittades (fokus-/expanderingsförlust vid omräkning) är åtgärdat och regressionstestat.

---

## 1. Kontrast (1.4.3 Contrast Minimum, AA)

Uträknade kontrastkvoter (WCAG-formeln, sRGB) för faktiska text-/färgpar. AA kräver **4,5:1**
för normal text, **3:1** för stor text och UI-komponenter (1.4.11).

| Par | Kvot | Krav | Status |
|-----|------|------|--------|
| Brödtext `--ink` #e8eaed / bg #0f1115 | 15,7 | 4,5 | ✅ |
| Dämpad `--muted` #9aa3b2 / bg | 7,4 | 4,5 | ✅ |
| Dämpad / panel #181c24 | 6,7 | 4,5 | ✅ |
| Accent (länk/knapp) #4f8cff / bg | 5,9 | 4,5 | ✅ |
| Accent / panel | 5,3 | 4,5 | ✅ |
| Varningsbanner-text #f0d9a8 / banner-bg | 10,0 | 4,5 | ✅ |
| Felbanner-text #f3c0c0 / banner-bg | 9,2 | 4,5 | ✅ |
| Överlapp-notis `--warn` #e0a23a / panel | 7,6 | 4,5 | ✅ |
| Flagg-tag #9aa3b2 / #223333 | 5,2 | 4,5 | ✅ |
| Fokusram (accent) / bg (UI) | 5,9 | 3,0 | ✅ |

**Slutsats:** all text klarar AA. Mätningen reproduceras med skriptet i metodloggen (samma
WCAG-relativ-luminans-formel). Ingen färg behövde ändras.

### 1.4.11 Non-text Contrast (AA)
Kortkanter (`--line` #2a3140 vs bg = 1,45:1) och panel-vs-bg (1,11:1) ligger under 3:1, men
kanterna är **dekorativa** (struktur uppfattas även utan dem; poäng/CI finns som text) och
omfattas inte av 1.4.11. Stapeln/CI-bandet är `aria-hidden` och kompletterar en synlig
sifferpoäng → färg är supplementär. **Pass.** (Möjlig framtida finputs: höj `--line` något.)

---

## 2. Tangentbord & fokus

| Kriterium | Bedömning |
|-----------|-----------|
| **2.1.1 Keyboard (A)** | Hela flödet nås med tangentbord: skip-link, reglage (native `range`), Återställ/Dela (native `button`), partikort (`role="button"`, `tabindex="0"`, Enter/Space med `preventDefault`), `<details>` för metod + bevisspår, källänkar. ✅ |
| **2.1.2 No Keyboard Trap (A)** | Inga fokusfällor; inga modaler. ✅ |
| **2.4.1 Bypass Blocks (A)** | Skip-link "Hoppa till innehållet" → `#main-content` (`tabindex="-1"`). ✅ |
| **2.4.3 Focus Order (A)** | DOM-ordning = visuell ordning. Omordning sker genom att flytta befintliga element (inte CSS `order`), så tabbordningen följer rankningen. Se blocker-fix nedan. ✅ |
| **2.4.7 Focus Visible (AA)** | Global `:focus-visible { outline: 2px solid accent; offset 2px }`. Gäller div-knappen, reglage, summary och länkar. ✅ |
| **2.5.8 Target Size Minimum (AA, 2.2)** | Kort-huvud ~44px höjd, knappar ~34px, summary/reglage ≥24px. ✅ |

### BLOCKER (åtgärdad): fokus- och expanderingsförlust vid omräkning
Tidigare nollades `ol.innerHTML` vid **varje** reglage-`input`, vilket återskapade alla 8 kort
→ ett expanderat kort kollapsade och tangentbordsfokus föll till `<body>`
(**3.2.2 On Input**, **2.4.3 Focus Order**). Detta var den enda blockerande bristen
(flaggad av Codex second opinion).

**Fix:** korten byggs **en gång** (`buildCards()`); `render()` uppdaterar bara
föränderliga fält (plats, totalpoäng, stapel, överlapp, `aria-label`) och **omordnar befintliga
element**. Eftersom en flyttad `<li>` tillfälligt kopplar bort sitt fokuserade huvud fångas och
återställs fokus över omordningen (`focus({preventScroll:true})`). Det expanderade tillståndet
bor på elementet och följer med. **Regressionstest:** `e2e.spec.mjs` →
"expanderat kort + fokus bevaras vid viktändring".

---

## 3. Struktur, namn, roller, status

| Kriterium | Bedömning |
|-----------|-----------|
| **1.3.1 Info & Relationships (A)** | En `<h1>`, sektioner med `<h2>`, `<ol>` för rangordning, riktig `<table>` med `<caption class="sr-only">`, `<th>`-rubriker. Reglage har `<label for>`. ✅ |
| **3.1.1 Language (A)** | `<html lang="sv">`. ✅ |
| **2.4.2 Page Titled (A)** | `<title>Rösta — väljarkompass</title>`. ✅ |
| **4.1.2 Name/Role/Value (A)** | Kort-huvud: `role="button"` + `aria-expanded` + `aria-controls="detail_<parti>"` → stabil id-koppling till panelen. Reglage namnges via `aria-label="Vikt för <kategori>"`; native-värdet (0–40) annonseras. ✅ |
| **4.1.3 Status Messages (AA)** | Dedikerad `#status` `role="status"` (sr-only) skrivs vid varje render med en **kort** sammanfattning ("Rangordning uppdaterad. Etta: …"). `aria-live` togs bort från hela `<ol>` (annars lästes alla 8 kort upp vid varje tick). Statustexten **debounce:as 350 ms** så drag inte spammar skärmläsaren. ✅ |
| **3.2.2 On Input (A)** | Reglage räknar om i samma vy utan kontextbyte/omladdning; fokus bevaras (se blocker-fix). ✅ |
| **3.3.1 Error Identification (A)** | Datafel → `#error` `role="alert"` med svensk text ("Datakontraktsfel: …"); appen kraschar inte. Regressionstestat. ✅ |

---

## 4. Anpassningsbar layout

| Kriterium | Bedömning |
|-----------|-----------|
| **1.4.10 Reflow (AA, 320px)** | Två-kolumnsgriden kollapsar till en kolumn ≤760px. `min-width:0` på grid-items (sektioner) hindrar att tabellens `min-width` (i ett expanderat kort) tvingar spalten bredare → ingen horisontell **sid**scroll vid 320px. Den 8-kolumns A/B/C/D-**tabellen** ligger i en `overflow-x:auto`-container och scrollar i sig själv (tabeller är undantagna 1.4.10). Vid ≤420px faller poängsträngen till egen rad så partinamnet inte kläms. **Verifierat i e2e** ("ingen horisontell sidoscroll vid 320px"). ✅ |
| **1.4.4 Resize Text (AA)** | Relativa enheter (`rem`/`em`), inga absoluta px-lås på text. ✅ |
| **1.4.1 Use of Color (A)** | Överlapp signaleras med **text** ("≈ osäker skillnad mot #n"), inte enbart färg; flaggor är text. ✅ |

---

## 5. Kvarstående / medvetna val

- **`role="button"`-div i stället för native `<button>`** — uppfyller 4.1.2 (namn/roll/tillstånd,
  fokus, Enter+Space). Codex bedömde native `<button>` som *marginellt* bättre men div:en som
  godtagbar. Behållen för att minimera ändringsyta; **nice-to-have** för framtiden.
- **`title`-tooltip på A/B/C/D-rubriker** (1.4.13/2.1.1) — informationen finns även som synlig
  text i förklaringsraden under tabellen, så tooltip är supplementär. **Pass**, men kan ersättas
  med synliga rubriknamn senare.
- **TODO (manuell):** verifiering med riktig skärmläsare (NVDA/VoiceOver) av live-status,
  expandering och tabellnavigering. Automatiken täcker DOM/ARIA-kontrakt och fokusbeteende, inte
  uppläsningsupplevelsen.

---

## 6. Verifiering

```bash
# I web/ :
npm run test:e2e     # Playwright: bl.a. fokus/expand bevaras, reflow 320px, felkort, ?w=, bevisspår
npm run test:unit    # rena moduler (format/score)
```

Kontrast- och reflow-siffrorna ovan är mätta (inte uppskattade): kontrast med WCAG-relativ
luminans, reflow genom att räkna `documentElement.scrollWidth − clientWidth` vid 320px i Chromium.
