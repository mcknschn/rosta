// Rösta — Playwright-e2e (Fas 6, task 6.7). Kör mot den statiska frontenden serverad
// från repo-roten (se playwright.config.mjs). Täcker: 8 kort fallande, live-omräkning,
// bevisspår, ?w=-round-trip, trasig fixtur → felkort, samt WCAG-regressioner
// (fokus/expanderat bevaras vid viktändring; ingen sidoscroll vid 320px).
import { test, expect } from "@playwright/test";

const PAGE = "index.html";   // löses mot baseURL .../web/

const score = (li) => li.locator(".score");

// Sätt EN reglagevikt och trigga appens 'input'-lyssnare (drag fungerar dåligt på range i headless).
async function setSlider(page, selector, value) {
  await page.locator(selector).first().evaluate((el, v) => {
    el.value = String(v);
    el.dispatchEvent(new Event("input", { bubbles: true }));
  }, value);
}

test("8 partikort rankas fallande i svensk poängformat", async ({ page }) => {
  await page.goto(PAGE);
  const cards = page.locator("#parties > li.party");
  await expect(cards).toHaveCount(8);

  const texts = await score(cards).allTextContents();
  expect(texts).toHaveLength(8);
  expect(texts[0]).toMatch(/\d,\d{2} av 5 \(\d,\d-\d,\d\)/); // "3,72 av 5 (3,3-4,2)"

  const nums = texts.map((t) => parseFloat(t.match(/([\d,]+) av 5/)[1].replace(",", ".")));
  for (let i = 1; i < nums.length; i++) {
    expect(nums[i]).toBeLessThanOrEqual(nums[i - 1] + 1e-9); // fallande
  }
});

test("viktändring räknar om live utan omladdning (0 → tom, åter → 8 kort)", async ({ page }) => {
  await page.goto(PAGE);
  await expect(page.locator("#parties > li.party")).toHaveCount(8);

  // Nolla alla vikter → deterministiskt tomtillstånd.
  await page.evaluate(() => {
    document.querySelectorAll('input[type="range"]').forEach((el) => {
      el.value = "0";
      el.dispatchEvent(new Event("input", { bubbles: true }));
    });
  });
  await expect(page.locator("#parties .empty")).toBeVisible();
  await expect(page.locator("#parties > li.party")).toHaveCount(0);

  // Dra upp en kategori → korten kommer tillbaka, ingen omladdning.
  await setSlider(page, 'input[type="range"]', 40);
  await expect(page.locator("#parties > li.party")).toHaveCount(8);
});

test("expanderat kort + fokus bevaras vid viktändring (WCAG 3.2.2 / 2.4.3)", async ({ page }) => {
  await page.goto(PAGE);
  const firstHead = page.locator("#parties > li.party .party-head").first();
  await firstHead.focus();
  await page.keyboard.press("Enter"); // expandera via tangentbord
  await expect(firstHead).toHaveAttribute("aria-expanded", "true");

  const focusedParty = await page.evaluate(
    () => document.activeElement.closest("li.party")?.dataset.party);
  expect(focusedParty).toBeTruthy();

  // Ändra en vikt → render() omordnar listan in-place.
  await setSlider(page, 'input[type="range"]', 35);

  // Samma parti ska fortfarande vara både fokuserat OCH expanderat.
  const stillFocused = await page.evaluate(
    () => document.activeElement.closest("li.party")?.dataset.party);
  expect(stillFocused).toBe(focusedParty);
  await expect(
    page.locator(`#parties > li.party[data-party="${focusedParty}"] .party-head`),
  ).toHaveAttribute("aria-expanded", "true");
});

test("expandering visar A/B/C/D-tabell och bevisspår", async ({ page }) => {
  await page.goto(PAGE);
  // Första kortet som faktiskt har ett bevisspår (alla har inte nödvändigtvis källrefs).
  const card = page.locator("#parties > li.party")
    .filter({ has: page.locator("details.evidence") }).first();
  const head = card.locator(".party-head");
  await expect(head).toBeVisible();

  await head.click();
  await expect(head).toHaveAttribute("aria-expanded", "true");
  const detail = card.locator(".detail");
  await expect(detail).toBeVisible();
  await expect(detail.locator("table")).toBeVisible();

  const ev = detail.locator("details.evidence");
  await ev.locator("summary").click();
  await expect(ev.locator("li").first()).toBeVisible();
});

test("täckningskolumnen ersätter täckningsflaggorna i detaljtabellen (ADR 0008)", async ({ page }) => {
  await page.goto(PAGE);
  const head = page.locator("#parties > li.party .party-head").first();
  await head.click();
  const detail = page.locator("#parties > li.party .detail").first();
  await expect(detail.locator("th", { hasText: "Täckning" })).toBeVisible();

  // Talet står i procent på varje rad, ingen cell är tom.
  const täckning = detail.locator("tbody tr td:nth-last-child(2)");
  for (const text of await täckning.allTextContents()) {
    expect(text).toMatch(/^\d+ %$/);
  }

  // De tre täckningsflaggorna är borta ur flaggkolumnen, resten står kvar.
  const flaggor = (await detail.locator("tbody .tag").allTextContents());
  for (const f of flaggor) {
    expect(f).not.toMatch(/^A_a1_active$|^A_a2_only$|^B_coverage_|^D_coverage_/);
  }
});

test("vikter round-trippar via ?w= i URL:en", async ({ page }) => {
  await page.goto(PAGE);
  const first = page.locator('input[type="range"]').first();
  const id = await first.getAttribute("id"); // w_<kategori>

  await setSlider(page, 'input[type="range"]', 7);
  await expect(page).toHaveURL(/[?&]w=/);

  const url = page.url();
  await page.goto(url);                      // ladda om med vikterna i URL:en
  await expect(page.locator(`#${id}`)).toHaveValue("7");
});

test("Dela-knappen ger feedback (klipper/faller tillbaka)", async ({ page }) => {
  await page.goto(PAGE);
  await page.locator("#share").click();
  await expect(page.locator("#share")).toHaveText(/Länk kopierad|Kopiera adressfältet/);
});

test("trasig datafil ger svenskt felkort, ingen krasch", async ({ page }) => {
  // Cache-buster ?t=... gör att globben måste matcha querystring → regex är säkrast.
  await page.route(/scores\.json/, async (route) => {
    const broken = {
      meta: { coverage: "x", generated: "2026-01-01", window: "", parties: [], model_version: "v0" },
      categories: [{ id: "ekonomi", name: "Ekonomi", standard_weight: 10 }],
      // ci0 (4) > score (3) → validate() ska avvisa.
      scores: { S: { ekonomi: { score: 3, ci: [4, 5], components: {}, confidence: {}, flags: [] } } },
    };
    await route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(broken) });
  });
  await page.goto(PAGE);

  const err = page.locator("#error");
  await expect(err).toBeVisible();
  await expect(err).toContainText(/Data ser trasig ut|kunde inte hämta data/);
  await expect(page.locator("#parties > li.party")).toHaveCount(0);
});

test("foten säger hur långt underlaget når, och aldrig ett framtida datum (issue #3)", async ({ page }) => {
  await page.goto(PAGE);
  const foot = page.locator("#generated");
  await expect(foot).toContainText(/Data till och med \d{4}-\d{2}-\d{2}\./);
  await expect(foot).toContainText(/Mandatperioden pågår till \d{4}-\d{2}-\d{2}, så betygen för den är preliminära\./);

  // Kärnan i buggen: underlagets slut fick inte vara valdagen, som ligger i framtiden.
  const meta = await page.evaluate(async () => (await (await fetch("./data/scores.json")).json()).meta);
  expect(meta.data_as_of).not.toBe(meta.window_end);
  expect(new Date(meta.data_as_of).getTime()).toBeLessThanOrEqual(Date.now());
});

test("andelen metodvarianter står vid varje kort utom det översta (ADR 0003)", async ({ page }) => {
  await page.goto(PAGE);
  // Samma två vägar som app.js provar, annars kan testet hoppa över i ett läge där sajten
  // faktiskt visar andelen.
  const hasRobustness = await page.evaluate(async () => {
    for (const path of ["./data/robustness.json", "../dist/robustness.json"]) {
      try { if ((await fetch(path)).ok) return true; } catch { /* nästa väg */ }
    }
    return false;
  });
  test.skip(!hasRobustness, "robustness.json saknas — kör python -m pipeline.robustness");

  const cards = page.locator("#parties > li.party");
  await expect(cards.first().locator(".stability")).toBeHidden();   // nr 1 har inget kort ovanför
  const second = cards.nth(1).locator(".stability");
  await expect(second).toBeVisible();
  await expect(second).toHaveText(/^[A-ZÅÄÖ]+ ligger före [A-ZÅÄÖ]+ i \d+ procent av metodvarianterna$/);
  // Ingen tröskel och inget binärt omdöme någonstans i listan (ADR 0003 punkt 3).
  await expect(page.locator("#parties")).not.toContainText(/robust skil|oskiljbar|är osäker/i);
});

test("utan robustness.json lovar metodrutan ingen andel", async ({ page }) => {
  await page.route(/robustness\.json/, (route) => route.fulfill({ status: 404, body: "" }));
  await page.goto(PAGE);
  await expect(page.locator("#parties > li.party")).toHaveCount(8);
  await expect(page.locator("#parties .stability")).toHaveCount(8);
  await expect(page.locator("#parties .stability:visible")).toHaveCount(0);
  await expect(page.locator("#method-body")).toContainText("Den körningen saknas i den här versionen");
  await expect(page.locator("#method-body")).not.toContainText("procent av metodvarianterna");
});

test("en robustness.json med andra kategorier ger ingen andel alls", async ({ page }) => {
  await page.route(/robustness\.json/, async (route) => {
    const body = JSON.stringify({
      meta: { n_draws: 10, n_draws_shipped: 1 },
      draws: { parties: ["S"], categories: ["gammal_kategori"], scale: 100, values: [300] },
    });
    await route.fulfill({ status: 200, contentType: "application/json", body });
  });
  await page.goto(PAGE);
  await expect(page.locator("#parties > li.party")).toHaveCount(8);
  await expect(page.locator("#parties .stability:visible")).toHaveCount(0);
});

test("conf-low läser A, B och D men aldrig C (ADR 0009 punkt 6)", async ({ page }) => {
  // En cell per delpoäng, var och en ensam på low. C väger 0 och får inte fälla sin cell.
  const cell = (conf) => ({
    score: 3, ci: [2, 4], components: {}, coverage: 1, flags: [],
    confidence: { A: "high", B: "high", C: "high", D: "high", ...conf },
  });
  await page.route(/scores\.json/, async (route) => {
    const fixture = {
      meta: { coverage: "", generated: "2026-01-01", window: "2014-2026", parties: [], model_version: "v0" },
      categories: [
        { id: "lag_a", name: "Låg A", standard_weight: 10 },
        { id: "lag_b", name: "Låg B", standard_weight: 10 },
        { id: "lag_c", name: "Låg C", standard_weight: 10 },
        { id: "lag_d", name: "Låg D", standard_weight: 10 },
      ],
      scores: { S: {
        lag_a: cell({ A: "low" }), lag_b: cell({ B: "low" }),
        lag_c: cell({ C: "low" }), lag_d: cell({ D: "low" }),
      } },
    };
    await route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(fixture) });
  });
  await page.goto(PAGE);
  await page.locator("#parties > li.party .party-head").first().click();
  const detail = page.locator("#parties > li.party .detail").first();

  const flaggkolumn = (namn) =>
    detail.locator("tbody tr").filter({ hasText: namn }).locator("td:last-child");
  await expect(flaggkolumn("Låg A")).toHaveClass(/conf-low/);
  await expect(flaggkolumn("Låg B")).toHaveClass(/conf-low/);
  await expect(flaggkolumn("Låg D")).toHaveClass(/conf-low/);
  await expect(flaggkolumn("Låg C")).not.toHaveClass(/conf-low/);
});

test("ingen horisontell sidoscroll vid 320px (reflow 1.4.10)", async ({ page }) => {
  await page.setViewportSize({ width: 320, height: 800 });
  await page.goto(PAGE);
  await page.locator("#parties > li.party .party-head").first().click(); // rendera den breda tabellen
  const overflow = await page.evaluate(
    () => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  expect(overflow).toBeLessThanOrEqual(1); // tabellen scrollar i egen container, inte sidan
});
