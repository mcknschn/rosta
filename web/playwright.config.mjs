// Playwright-e2e för Rösta-frontenden (Fas 6, task 6.7).
// Serverar repo-roten statiskt (python http.server --directory ..) så att både
// /web/ och ../dist/ nås precis som i deploy; ingen runtime-npm-dep i appen.
import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./tests",
  // Kör ENDAST e2e-specen här. node:test-enhetsfilen (score.test.mjs) körs via `npm run test:unit`.
  testMatch: /e2e\.spec\.mjs$/,
  timeout: 30_000,
  expect: { timeout: 5_000 },
  fullyParallel: true,
  retries: 1,
  reporter: [["list"]],
  use: {
    baseURL: "http://localhost:8000/web/",
    trace: "on-first-retry",
    // Clipboard för "Dela mina vikter"; testet tål även avsaknad (fallback-text).
    permissions: ["clipboard-read", "clipboard-write"],
  },
  projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"] } }],
  webServer: {
    command: "python -m http.server 8000 --directory ..",
    url: "http://localhost:8000/web/index.html",
    reuseExistingServer: true,
    timeout: 30_000,
  },
});
