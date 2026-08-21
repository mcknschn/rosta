// Rösta: client-side viktning (ren, testbar i både webbläsare och Node).
// Frontend FÅR ENDAST vikta/summera de förberäknade kategoribetygen. Ingen A/B/C/D-logik här.
// Total = Σ (normaliserad vikt × kategoribetyg). CI propageras linjärt (konservativt).

export function normalizeWeights(weights, catIds) {
  const sum = catIds.reduce((a, c) => a + (Number(weights[c]) || 0), 0);
  const out = {};
  for (const c of catIds) out[c] = sum > 0 ? (Number(weights[c]) || 0) / sum : 0;
  return out;
}

// scores: { party: { cat: { score, ci:[lo,hi], components, ... } } }
// -> [{ party, total, lo, hi, catScores }] sorterat fallande, alfabetisk tie-break.
export function partyTotals(scores, weights, catIds) {
  const frac = normalizeWeights(weights, catIds);
  const rows = Object.entries(scores).map(([party, catScores]) => {
    let total = 0, lo = 0, hi = 0;
    for (const c of catIds) {
      const cs = catScores[c];
      if (!cs) continue;
      total += (cs.score || 0) * frac[c];
      lo += (cs.ci ? cs.ci[0] : cs.score || 0) * frac[c];
      hi += (cs.ci ? cs.ci[1] : cs.score || 0) * frac[c];
    }
    return { party, total, lo, hi, catScores };
  });
  rows.sort((a, b) => (b.total - a.total) || a.party.localeCompare(b.party, "sv"));
  return rows;
}

// Andelen metodvarianter där ett parti ligger före ett annat, för ANVÄNDARENS vikter
// (ADR 0003 punkt 2 och 7). Pipen kan inte förberäkna totalen, eftersom vikterna sätts här.
//
// draws: { parties, categories, scale, values } ur robustness.json. values är en flat
// heltalsvektor med kategoribetygen skalade med `scale`; betyget för dragning d, parti p och
// kategori c ligger på ((d * P) + p) * C + c.
//
// Returnerar { a: { b: andel } } för varje riktat partipar. Oavgjort räknas inte som "före"
// åt något håll, så andel[a][b] + andel[b][a] kan vara under 1. Ingen tröskel och inget
// omdöme: talet redovisas som det är.
//
// Att räkna paren HÄR, ur varje dragnings hela kategorirad, avskaffar samtidigt antagandet om
// full korrelation mellan kategorier som uppstod när banden adderades.
export function pairStability(draws, weights, catIds) {
  if (!draws || !Array.isArray(draws.values) || !draws.values.length) return {};
  const parties = draws.parties || [];
  const cats = draws.categories || [];
  const P = parties.length, C = cats.length;
  if (!P || !C) return {};
  const nDraws = Math.floor(draws.values.length / (P * C));
  if (!nDraws) return {};

  // Varje kategori användaren väger måste finnas i dragningarna. Saknas en är dragningarna ett
  // ANNAT index än listan ovanför, och andelen skulle svara på en annan fråga än den ställda.
  // Då lämnas talet hellre osagt (en inaktuell robustness.json får aldrig se aktuell ut).
  if (catIds.some((c) => !cats.includes(c))) return {};

  const frac = normalizeWeights(weights, catIds);
  // Vikt per kolumn i draws.categories. Kategorier utanför catIds väger 0.
  const colWeight = cats.map((c) => (catIds.includes(c) ? frac[c] || 0 : 0));
  if (!colWeight.some((w) => w > 0)) return {};

  const out = {};
  for (const a of parties) out[a] = {};
  const wins = new Float64Array(P * P);
  const totals = new Float64Array(P);
  const scale = draws.scale || 100;
  for (let d = 0; d < nDraws; d++) {
    const base = d * P * C;
    for (let p = 0; p < P; p++) {
      let t = 0;
      const row = base + p * C;
      for (let c = 0; c < C; c++) t += (draws.values[row + c] / scale) * colWeight[c];
      totals[p] = t;
    }
    for (let i = 0; i < P; i++) {
      for (let j = 0; j < P; j++) {
        if (i !== j && totals[i] > totals[j]) wins[i * P + j]++;
      }
    }
  }
  for (let i = 0; i < P; i++) {
    for (let j = 0; j < P; j++) {
      if (i !== j) out[parties[i]][parties[j]] = wins[i * P + j] / nDraws;
    }
  }
  return out;
}
