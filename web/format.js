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

// Foten: när betygen räknades, hur långt underlaget når, och vilket fönster som mäts.
// data_as_of och window_end är SKILDA datum (issue #3). window_end är mandatperiodens formella
// slut och ligger i framtiden tills valet hållits; data_as_of är sista dagen serierna faktiskt
// når. Ett fält som saknas hoppas över, så en äldre scores.json fortfarande renderar.
export function metaLine(meta) {
  if (!meta || !meta.generated) return "";
  const parts = [`Uppdaterad ${meta.generated}.`];
  if (meta.data_as_of) parts.push(`Data till och med ${meta.data_as_of}.`);
  if (meta.window) parts.push(`Mätfönstret är ${String(meta.window).replace("-", " till ")}.`);
  if (meta.window_open && meta.window_end) {
    parts.push(`Mandatperioden pågår till ${meta.window_end}, så betygen för den är preliminära.`);
  }
  if (meta.model_version !== null && meta.model_version !== undefined) {
    parts.push(`Modellversion ${meta.model_version}.`);
  }
  return parts.join(" ");
}

// Skalan 0 till 5 till procent för stapelbredd.
export function pct(x) {
  const v = Math.max(0, Math.min(5, Number(x) || 0));
  return `${(v / 5) * 100}%`;
}
