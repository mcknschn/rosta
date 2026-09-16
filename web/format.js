// Rösta: formatering (ren, testbar i både webbläsare och Node).
// Svensk konvention: decimalkomma. Intervall skrivs med vanligt bindestreck.

export function fmtNum(x, decimals = 2) {
  if (x === null || x === undefined || Number.isNaN(x)) return "-";
  return Number(x).toFixed(decimals).replace(".", ",");
}

// Täckningen: hur stor del av cellens betyg som vilar på mätt underlag (ADR 0008). Talet
// räknas i pipen och står som det är, utan tröskel och utan omdöme (ADR 0008 punkt 6).
// Samma formatering bär kategorins MÄTTAK (ADR 0014), alltså det högsta tal täckningen kan
// nå där. De två står på samma skala och ska därför se likadana ut.
export function fmtCoverage(x) {
  if (x === null || x === undefined || Number.isNaN(Number(x))) return "-";
  return `${Math.round(Number(x) * 100)} %`;
}

// Flaggkolumnen visar bara det som INTE är täckning (ADR 0008 punkt 9). A_a1_active,
// A_a2_only, B_shrink_* och D_shrink_* säger samma sak som täckningskolumnen, fast sämre.
// De två sista bar ordet coverage i namnet fram till ADR 0014, fast de bär KRYMPNINGENS
// täljare och nämnare, som efter ADR 0011 är ett annat tal än täckningen.
// Kvar står flaggorna som markerar något annat: en ej tillämplig del, ett tunt underlag,
// en åtgärd i modellen eller en subnationell attribution.
const COVERAGE_FLAGS = [/^A_a1_active$/, /^A_a2_only$/, /^B_shrink_/, /^B_terms_/, /^D_shrink_/];

export function visibleFlags(flags) {
  return (flags || []).filter((f) => !COVERAGE_FLAGS.some((re) => re.test(f)));
}

// conf-low läser bara de delpoäng som väger (ADR 0009 punkt 6). C väger 0, så en låg C
// säger ingenting om cellen och ska inte fälla den. Listan speglar subscore_weights i
// config/scoring.yaml; ändras vikterna där måste den här raden följa med.
const WEIGHTED_SUBSCORES = ["A", "B", "D"];

export function hasLowConfidence(confidence) {
  const c = confidence || {};
  return WEIGHTED_SUBSCORES.some((s) => c[s] === "low");
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
