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

// Överlappar två osäkerhetsband? Då kan partierna inte säkert särskiljas.
export function ciOverlap(a, b) {
  return a.lo <= b.hi && b.lo <= a.hi;
}
