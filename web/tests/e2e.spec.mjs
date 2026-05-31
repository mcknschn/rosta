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
  expect(texts[0]).toMatch(/\d,\d{2} \/ 5 \(\d,\d–\d,\d\)/); // "3,72 / 5 (3,3–4,2)"

  const nums = texts.map((t) => parseFloat(t.match(/([\d,]+) \/ 5/)[1].replace(",", ".")));
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
  await expect(err).toContainText(/Datakontraktsfel|Osäkerhet/);
  await expect(page.locator("#parties > li.party")).toHaveCount(0);
});

test("ingen horisontell sidoscroll vid 320px (reflow 1.4.10)", async ({ page }) => {
  await page.setViewportSize({ width: 320, height: 800 });
  await page.goto(PAGE);
  await page.locator("#parties > li.party .party-head").first().click(); // rendera den breda tabellen
  const overflow = await page.evaluate(
    () => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  expect(overflow).toBeLessThanOrEqual(1); // tabellen scrollar i egen container, inte sidan
});
