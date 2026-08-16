// Rösta: formatering (ren, testbar i både webbläsare och Node).
// Svensk konvention: decimalkomma. Intervall skrivs med vanligt bindestreck.

export function fmtNum(x, decimals = 2) {
  if (x === null || x === undefined || Number.isNaN(x)) return "-";
  return Number(x).toFixed(decimals).replace(".", ",");
}

// "3,84 av 5 (3,5-4,1)"
export function fmtScoreWithCI(score, ci) {
  const s = fmtNum(score, 2);
  if (!Array.isArray(ci) || ci.length !== 2) return `${s} av 5`;
  return `${s} av 5 (${fmtNum(ci[0], 1)}-${fmtNum(ci[1], 1)})`;
}

// Skalan 0 till 5 till procent för stapelbredd.
export function pct(x) {
  const v = Math.max(0, Math.min(5, Number(x) || 0));
  return `${(v / 5) * 100}%`;
}
