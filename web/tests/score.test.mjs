// Enhetstester för de rena frontend-modulerna (format.js + score.js).
// Kör: node --test web/tests/   (eller npm run test:unit)
import { test } from "node:test";
import assert from "node:assert/strict";
import { fmtNum, fmtScoreWithCI, fmtCoverage, visibleFlags, hasLowConfidence, pct, metaLine } from "../format.js";
import { normalizeWeights, partyTotals, pairStability } from "../score.js";

test("fmtNum: svensk decimalkomma + avrundning", () => {
  assert.equal(fmtNum(3.842), "3,84");
  assert.equal(fmtNum(3.842, 1), "3,8");
  assert.equal(fmtNum(20, 0), "20");
  assert.equal(fmtNum(undefined), "-");
});

test("fmtScoreWithCI: '3,84 av 5 (3,5-4,1)'", () => {
  assert.equal(fmtScoreWithCI(3.842, [3.5, 4.1]), "3,84 av 5 (3,5-4,1)");
  assert.equal(fmtScoreWithCI(2.5, null), "2,50 av 5");
});

test("pct: klampar till skalan 0 till 5", () => {
  assert.equal(pct(2.5), "50%");
  assert.equal(pct(6), "100%");
  assert.equal(pct(-1), "0%");
});

test("normalizeWeights summerar till 1 (eller 0 om alla 0, ingen NaN)", () => {
  const n = normalizeWeights({ a: 20, b: 20, c: 10 }, ["a", "b", "c"]);
  assert.ok(Math.abs(n.a + n.b + n.c - 1) < 1e-9);
  assert.ok(Math.abs(n.a - 0.4) < 1e-9);
  const z = normalizeWeights({ a: 0, b: 0 }, ["a", "b"]);
  assert.equal(z.a, 0); assert.equal(z.b, 0);
  assert.ok(!Number.isNaN(z.a));
});

test("partyTotals: viktad summa, fallande, alfabetisk tie-break", () => {
  const scores = {
    X: { a: { score: 4, ci: [3, 5] }, b: { score: 2, ci: [1, 3] } },
    Y: { a: { score: 2, ci: [1, 3] }, b: { score: 4, ci: [3, 5] } },
    Z: { a: { score: 3, ci: [2, 4] }, b: { score: 3, ci: [2, 4] } },
  };
  // lika vikt -> alla snitt 3; tie-break alfabetisk X,Y,Z
  const eq = partyTotals(scores, { a: 1, b: 1 }, ["a", "b"]);
  assert.deepEqual(eq.map((r) => r.party), ["X", "Y", "Z"]);
  eq.forEach((r) => assert.ok(Math.abs(r.total - 3) < 1e-9));
  // vikta a tungt -> X (4) > Z (3) > Y (2)
  const wa = partyTotals(scores, { a: 1, b: 0 }, ["a", "b"]);
  assert.deepEqual(wa.map((r) => r.party), ["X", "Z", "Y"]);
  assert.ok(Math.abs(wa[0].total - 4) < 1e-9);
  assert.ok(Math.abs(wa[0].lo - 3) < 1e-9 && Math.abs(wa[0].hi - 5) < 1e-9);
});

// Issue #3: foten skiljer underlagets slut (data_as_of) från fönstrets slut (window_end).
const META = {
  generated: "2026-08-17", window: "2014-2026", window_end: "2026-09-13",
  window_open: true, data_as_of: "2025-12-31", model_version: 1,
};

test("metaLine: underlagets slut och fönstrets slut står som skilda datum", () => {
  const line = metaLine(META);
  assert.match(line, /Uppdaterad 2026-08-17\./);
  assert.match(line, /Data till och med 2025-12-31\./);
  assert.match(line, /Mätfönstret är 2014 till 2026\./);
  assert.match(line, /Mandatperioden pågår till 2026-09-13, så betygen för den är preliminära\./);
  assert.match(line, /Modellversion 1\./);
});

test("metaLine: avslutad mandatperiod ger ingen preliminär-mening", () => {
  const line = metaLine({ ...META, window_open: false });
  assert.ok(!line.includes("preliminära"));
  assert.match(line, /Data till och med 2025-12-31\./);
});

test("metaLine: fält som saknas hoppas över, inget 'undefined' i foten", () => {
  const line = metaLine({ generated: "2026-08-17", window: "2014-2026", model_version: 1 });
  assert.ok(!line.includes("undefined"));
  assert.ok(!line.includes("Data till och med"));
  assert.ok(!line.includes("preliminära"));
  assert.equal(metaLine(null), "");
  assert.equal(metaLine({}), "");
});

// --- pairStability (ADR 0003): andelen metodvarianter där ett parti ligger före ett annat ---

// Två partier, två kategorier, fyra dragningar. Betygen är skalade med 100.
// dragning 0: S (4,0 / 1,0)  M (3,0 / 2,0)
// dragning 1: S (1,0 / 1,0)  M (4,0 / 4,0)
// dragning 2: S (3,0 / 3,0)  M (3,0 / 3,0)   -> oavgjort i båda kategorierna
// dragning 3: S (5,0 / 5,0)  M (1,0 / 1,0)
const DRAWS = {
  parties: ["S", "M"],
  categories: ["a", "b"],
  scale: 100,
  values: [
    400, 100, 300, 200,
    100, 100, 400, 400,
    300, 300, 300, 300,
    500, 500, 100, 100,
  ],
};

test("pairStability: andelen räknas per dragning ur användarens vikter", () => {
  // lika vikt -> S-totaler: 2,5 · 1,0 · 3,0 · 5,0   M-totaler: 2,5 · 4,0 · 3,0 · 1,0
  const eq = pairStability(DRAWS, { a: 1, b: 1 }, ["a", "b"]);
  assert.equal(eq.S.M, 0.25);   // bara dragning 3
  assert.equal(eq.M.S, 0.25);   // bara dragning 1
  // Vikta kategori a tungt: S 4,0 · 1,0 · 3,0 · 5,0   M 3,0 · 4,0 · 3,0 · 1,0
  const wa = pairStability(DRAWS, { a: 1, b: 0 }, ["a", "b"]);
  assert.equal(wa.S.M, 0.5);
  assert.equal(wa.M.S, 0.25);
});

test("pairStability: oavgjort räknas inte som 'före' åt något håll", () => {
  const eq = pairStability(DRAWS, { a: 1, b: 1 }, ["a", "b"]);
  assert.ok(eq.S.M + eq.M.S < 1);   // dragning 0 och 2 är oavgjorda
  assert.ok(!("S" in eq.S));        // inget parti jämförs med sig självt
});

test("pairStability: en bortvald kategori väger noll", () => {
  const onlyB = pairStability(DRAWS, { a: 1, b: 1 }, ["b"]);
  // S i kategori b: 1,0 · 1,0 · 3,0 · 5,0   M: 2,0 · 4,0 · 3,0 · 1,0
  assert.equal(onlyB.S.M, 0.25);
  assert.equal(onlyB.M.S, 0.5);
});

test("pairStability: tom eller trasig indata ger tomt resultat, aldrig NaN", () => {
  assert.deepEqual(pairStability(null, { a: 1 }, ["a"]), {});
  assert.deepEqual(pairStability({ parties: [], categories: [], values: [] }, {}, []), {});
  assert.deepEqual(pairStability(DRAWS, { a: 0, b: 0 }, ["a", "b"]), {});
  const vals = Object.values(pairStability(DRAWS, { a: 1, b: 1 }, ["a", "b"]).S);
  assert.ok(vals.every((v) => Number.isFinite(v)));
});

test("pairStability: en kategori som saknas i dragningarna ger tomt, aldrig ett halvt svar", () => {
  // robustness.json är från en äldre modell och känner inte kategorin "c". Ett tal räknat på
  // a och b skulle svara på en annan fråga än den listan ställer.
  assert.deepEqual(pairStability(DRAWS, { a: 1, b: 1, c: 1 }, ["a", "b", "c"]), {});
  // Extra kategorier i dragningarna som användaren inte väger är däremot ofarliga.
  const extra = { ...DRAWS, categories: ["a", "b"] };
  assert.notDeepEqual(pairStability(extra, { a: 1, b: 1 }, ["a", "b"]), {});
});

test("score.js bär inget skiljbarhetspåstående längre", async () => {
  const mod = await import("../score.js");
  assert.equal(mod.ciOverlap, undefined);
});

// --- Täckning (ADR 0008) -------------------------------------------------------

test("fmtCoverage: talet visas i procent, utan tröskel och utan omdöme", () => {
  assert.equal(fmtCoverage(0.8), "80 %");
  assert.equal(fmtCoverage(1), "100 %");
  assert.equal(fmtCoverage(0), "0 %");
  assert.equal(fmtCoverage(undefined), "-");
  assert.equal(fmtCoverage(null), "-");
});

test("visibleFlags: de tre täckningsflaggorna utgår ur flaggkolumnen", () => {
  // Talet i täckningskolumnen säger samma sak som de här flaggorna, fast bättre.
  const kvar = visibleFlags([
    "A_a1_active", "A_a2_only", "B_coverage_86.7/100", "D_coverage_73/100",
  ]);
  assert.deepEqual(kvar, []);
});

test("visibleFlags: allt som inte är täckning står orört", () => {
  // Tröskelflaggorna stannar kvar trots att de går att härleda ur talet: de markerar en
  // ÅTGÄRD i modellen, inte bara ett faktum (ADR 0008 punkt 9).
  const flaggor = [
    "B_coverage_86.7/100", "B_thin_coverage", "A_a1_active", "D_coverage_73/100",
    "D_thin_coverage", "D_thin_basis", "D_not_applicable", "B_no_party_evidence",
    "C_national_only_by_design", "D_subnational_region_0.81",
  ];
  assert.deepEqual(visibleFlags(flaggor), [
    "B_thin_coverage", "D_thin_coverage", "D_thin_basis", "D_not_applicable",
    "B_no_party_evidence", "C_national_only_by_design", "D_subnational_region_0.81",
  ]);
});

test("visibleFlags: tom eller saknad lista ger tom lista, aldrig undefined", () => {
  assert.deepEqual(visibleFlags([]), []);
  assert.deepEqual(visibleFlags(undefined), []);
  assert.deepEqual(visibleFlags(null), []);
});

// --- Säkerhet (ADR 0009) -------------------------------------------------------

test("hasLowConfidence: C på low fäller inte cellen, C väger 0", () => {
  assert.equal(hasLowConfidence({ A: "high", B: "medium", C: "low", D: "high" }), false);
});

test("hasLowConfidence: A, B eller D på low fäller cellen, alla tre väger", () => {
  assert.equal(hasLowConfidence({ A: "low", B: "high", C: "high", D: "high" }), true);
  assert.equal(hasLowConfidence({ A: "high", B: "low", C: "high", D: "high" }), true);
  assert.equal(hasLowConfidence({ A: "high", B: "high", C: "high", D: "low" }), true);
});

test("hasLowConfidence: tomt eller saknat objekt ger false, aldrig ett kast", () => {
  assert.equal(hasLowConfidence({}), false);
  assert.equal(hasLowConfidence(undefined), false);
  assert.equal(hasLowConfidence(null), false);
});
