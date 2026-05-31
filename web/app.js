// Rösta-frontend. Läser de förberäknade betygen (scores.json) + bevisindex (evidence.json)
// och gör viktningen client-side. Inget rådata finns här. All betygslogik ligger i pipelinen;
// frontend får ENDAST vikta/summera (se score.js) och visa.

import { fmtNum, fmtScoreWithCI, pct } from "./format.js";
import { partyTotals, ciOverlap } from "./score.js";

const PARTY_NAMES = {
  S: "Socialdemokraterna", M: "Moderaterna", SD: "Sverigedemokraterna",
  C: "Centerpartiet", V: "Vänsterpartiet", KD: "Kristdemokraterna",
  L: "Liberalerna", MP: "Miljöpartiet",
};

let DATA = null;        // scores.json
let EVID = {};          // evidence.json (claim_ref -> {statement, source_name, source_url?})
let CAT_IDS = [];
const weights = {};

const $ = (id) => document.getElementById(id);

// ---- inladdning (self-contained ./data/, fallback ../dist/) -------------------
async function fetchJson(paths) {
  let lastErr;
  for (const p of paths) {
    try {
      const r = await fetch(`${p}?t=${Date.now()}`, { cache: "no-store" });
      if (r.ok) return await r.json();
      lastErr = new Error(`HTTP ${r.status} för ${p}`);
    } catch (e) { lastErr = e; }
  }
  throw lastErr;
}

function validate(data) {
  if (!data || typeof data !== "object") return "scores.json saknas eller är tom.";
  if (!data.meta || !Array.isArray(data.categories) || !data.scores) return "scores.json har fel format (meta/categories/scores saknas).";
  for (const [party, cats] of Object.entries(data.scores)) {
    for (const [cid, cs] of Object.entries(cats)) {
      if (typeof cs.score !== "number" || !Array.isArray(cs.ci) || cs.ci.length !== 2) return `Trasig cell ${party}/${cid}.`;
      if (cs.ci[0] > cs.score || cs.score > cs.ci[1]) return `Osäkerhetsintervall fel i ${party}/${cid} (ci0≤score≤ci1 bröts).`;
    }
  }
  return null;
}

async function load() {
  try {
    DATA = await fetchJson(["./data/scores.json", "../dist/scores.json"]);
    EVID = await fetchJson(["./data/evidence.json", "../dist/evidence.json"]).catch(() => ({}));
  } catch {
    $("error").hidden = false;
    $("error").textContent =
      "Kunde inte ladda data. Servera repo-roten med t.ex. `python -m http.server 8000` och öppna /web/.";
    return;
  }
  const bad = validate(DATA);
  if (bad) { $("error").hidden = false; $("error").textContent = `Datakontraktsfel: ${bad}`; return; }

  CAT_IDS = DATA.categories.map((c) => c.id);
  $("coverage").textContent = (DATA.meta && DATA.meta.coverage) || "";
  $("generated").textContent = DATA.meta?.generated ? `Data genererad ${DATA.meta.generated} · fönster ${DATA.meta.window} · modellversion ${DATA.meta.model_version}` : "";

  initWeights();
  buildSliders();
  buildCards();
  buildMethod();
  buildAttribution();
  render();

  $("reset").addEventListener("click", () => {
    DATA.categories.forEach((c) => (weights[c.id] = c.standard_weight ?? 10));
    syncUrl(); buildSliders(); render();
  });
  $("share").addEventListener("click", async () => {
    syncUrl();
    try { await navigator.clipboard.writeText(location.href); $("share").textContent = "Länk kopierad ✓"; }
    catch { $("share").textContent = "Kopiera adressfältet"; }
    setTimeout(() => ($("share").textContent = "Dela mina vikter"), 2500);
  });
}

// ---- vikter + URL -------------------------------------------------------------
function initWeights() {
  const fromUrl = parseWeightsFromUrl();
  DATA.categories.forEach((c) => {
    weights[c.id] = (fromUrl && c.id in fromUrl) ? fromUrl[c.id] : (c.standard_weight ?? 10);
  });
}

function parseWeightsFromUrl() {
  const w = new URLSearchParams(location.search).get("w");
  if (!w) return null;
  const out = {};
  for (const part of w.split(",")) {
    const [id, val] = part.split(":");
    const n = parseFloat(val);
    if (id && !Number.isNaN(n) && n >= 0) out[id] = n;
  }
  return Object.keys(out).length ? out : null;
}

function syncUrl() {
  const w = CAT_IDS.map((c) => `${c}:${(weights[c] ?? 0)}`).join(",");
  const url = new URL(location.href);
  url.searchParams.set("w", w);
  history.replaceState(null, "", url);
}

function buildSliders() {
  const root = $("sliders");
  root.innerHTML = "";
  DATA.categories.forEach((c) => {
    const wrap = document.createElement("div");
    wrap.className = "slider";
    wrap.innerHTML =
      `<label for="w_${c.id}">${c.name} <b id="v_${c.id}">${fmtNum(weights[c.id], 0)}</b></label>` +
      `<input type="range" id="w_${c.id}" min="0" max="40" step="0.5" value="${weights[c.id]}" aria-label="Vikt för ${c.name}">`;
    root.appendChild(wrap);
    wrap.querySelector("input").addEventListener("input", (ev) => {
      weights[c.id] = parseFloat(ev.target.value);
      $(`v_${c.id}`).textContent = fmtNum(weights[c.id], 0);
      syncUrl(); render();
    });
  });
}

// ---- rendering ----------------------------------------------------------------
// Korten byggs EN gång och uppdateras/omordnas in-place. Att nolla ol.innerHTML vid
// varje reglagedrag skulle förstöra fokus + expanderat tillstånd (WCAG 3.2.2 On Input,
// 2.4.3 Focus Order). Kategoribetygen (A/B/C/D) är viktoberoende → detaljen byggs en gång;
// bara totalpoäng, plats, stapel och överlapp ändras med vikterna.
let cardEls = {};   // party -> <li>

function buildCards() {
  cardEls = {};
  Object.keys(DATA.scores).forEach((party) => {
    const name = PARTY_NAMES[party] || party;
    const detId = `detail_${party}`;
    const li = document.createElement("li");
    li.className = "party";
    li.dataset.party = party;
    li.innerHTML =
      `<div class="party-head" role="button" tabindex="0" aria-expanded="false" aria-controls="${detId}">
         <span class="rank"></span>
         <span class="pname"><b>${party}</b> ${name}</span>
         <span class="score"></span>
         <div class="barwrap" aria-hidden="true">
           <div class="ci"></div>
           <div class="barfill"></div>
         </div>
         <span class="overlap" hidden></span>
       </div>
       <div class="detail" id="${detId}" hidden>${detailHTML({ party, catScores: DATA.scores[party] })}</div>`;
    const head = li.querySelector(".party-head");
    const det = li.querySelector(".detail");
    const toggle = () => {
      const open = det.hasAttribute("hidden");
      if (open) det.removeAttribute("hidden"); else det.setAttribute("hidden", "");
      head.setAttribute("aria-expanded", String(open));
    };
    head.addEventListener("click", toggle);
    head.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); toggle(); }
    });
    cardEls[party] = li;
  });
}

function updateCard(li, row, i, overlapAbove) {
  const name = PARTY_NAMES[row.party] || row.party;
  li.querySelector(".rank").textContent = String(i + 1);
  li.querySelector(".score").textContent = fmtScoreWithCI(row.total, [row.lo, row.hi]);
  li.querySelector(".ci").style.cssText = `left:${pct(row.lo)};width:${pct(row.hi - row.lo)}`;
  li.querySelector(".barfill").style.width = pct(row.total);
  const ov = li.querySelector(".overlap");
  if (overlapAbove) {
    ov.hidden = false;
    ov.title = "Osäkerhetsintervallen överlappar — skillnaden är inte statistiskt säker";
    ov.textContent = `≈ osäker skillnad mot #${i}`;
  } else {
    ov.hidden = true; ov.textContent = "";
  }
  li.querySelector(".party-head").setAttribute(
    "aria-label", `${name}, plats ${i + 1}, betyg ${fmtNum(row.total)}. Expandera för detaljer.`);
}

function render() {
  const ol = $("parties");
  const allZero = CAT_IDS.every((c) => (weights[c] || 0) === 0);
  if (allZero) {
    const empty = document.createElement("li");
    empty.className = "empty";
    empty.textContent = "Alla vikter är 0 — dra upp minst en kategori för att få en rangordning.";
    ol.replaceChildren(empty);   // korten detachas; deras expanderade tillstånd lever kvar i elementen
    setStatus("Alla vikter är 0 – ingen rangordning visas.");
    return;
  }
  ol.querySelector(".empty")?.remove();
  // Att flytta en <li> kopplar tillfälligt bort dess fokuserade huvud → webbläsaren nollar
  // fokus till <body>. Fånga och återställ fokus över omordningen (WCAG 2.4.3 Focus Order).
  // (Det expanderade tillståndet bor på elementet och följer med flytten av sig självt.)
  const active = document.activeElement;
  const refocus = active?.classList?.contains("party-head")
    ? active.closest("li.party")?.dataset.party : null;
  const rows = partyTotals(DATA.scores, weights, CAT_IDS);
  rows.forEach((row, i) => {
    const li = cardEls[row.party];
    updateCard(li, row, i, i > 0 && ciOverlap(rows[i - 1], row));
    ol.appendChild(li);   // flyttar BEFINTLIGT element (behåller expanderat tillstånd)
  });
  if (refocus) cardEls[refocus]?.querySelector(".party-head")?.focus({ preventScroll: true });
  const top = rows[0];
  setStatus(`Rangordning uppdaterad. Etta: ${PARTY_NAMES[top.party] || top.party} med ${fmtNum(top.total)} av 5.`);
}

// 'input' triggar kontinuerligt vid drag → debounca livesammanfattningen så skärmläsare
// inte spammas (WCAG 4.1.3 Status Messages). Visuell rendering sker direkt (ovan).
let statusTimer = null;
function setStatus(msg) {
  const el = $("status");
  if (!el) return;
  if (statusTimer) clearTimeout(statusTimer);
  statusTimer = setTimeout(() => { el.textContent = msg; }, 350);
}

function detailHTML(row) {
  const catRows = DATA.categories.map((c) => {
    const cs = row.catScores[c.id]; if (!cs) return "";
    const comp = cs.components || {};
    const flags = (cs.flags || []).map((f) => `<span class="tag">${f}</span>`).join(" ");
    const lowConf = Object.values(cs.confidence || {}).includes("low") ? ' class="conf-low"' : "";
    return `<tr>
      <td>${c.name}</td>
      <td class="num">${fmtNum(cs.score)}</td>
      <td class="num">${fmtNum(cs.ci[0], 1)}–${fmtNum(cs.ci[1], 1)}</td>
      <td class="num">${fmtNum(comp.A, 1)}</td><td class="num">${fmtNum(comp.B, 1)}</td>
      <td class="num">${fmtNum(comp.C, 1)}</td><td class="num">${fmtNum(comp.D, 1)}</td>
      <td${lowConf}>${flags || "—"}</td>
    </tr>`;
  }).join("");
  return `<div class="tablewrap"><table>
      <caption class="sr-only">Kategoribetyg och delpoäng för ${row.party}</caption>
      <thead><tr><th>Kategori</th><th class="num">Betyg</th><th class="num">Osäkerhet</th>
        <th class="num" title="Agerande">A</th><th class="num" title="Evidens">B</th>
        <th class="num" title="Ansvar">C</th><th class="num" title="Resultat">D</th><th>Flaggor</th></tr></thead>
      <tbody>${catRows}</tbody>
    </table></div>
    <p class="hint">A = agerande (prioritering) · B = evidens (träffsäkerhet) · C = ansvar (makt) · D = resultat. Flaggor visar var data är tunn eller saknas.</p>
    ${evidenceHTML(row)}`;
}

// ---- bevis-/källspår: lös claim_refs mot evidence.json ------------------------
function evidenceHTML(row) {
  const refs = new Set();
  DATA.categories.forEach((c) => {
    const cs = row.catScores[c.id]; if (!cs) return;
    (cs.claim_refs || []).forEach((r) => refs.add(r));
    (cs.evidence_refs || []).forEach((r) => refs.add(r));
  });
  if (!refs.size) return "";
  const items = [...refs].map((ref) => {
    const e = EVID[ref];
    if (!e) return `<li class="missing"><code>${ref}</code> — källa saknas i bevisindex</li>`;
    const url = e.url ? ` <a href="${e.url}" target="_blank" rel="noopener noreferrer">källa ↗</a>` : "";
    const src = e.source_name ? ` <span class="src">${e.source_name}</span>` : "";
    const val = (e.value !== undefined && e.value !== null && e.value !== "") ? ` <span class="src">(${e.value})</span>` : "";
    return `<li>${e.statement || ref}${src}${val}${url}</li>`;
  }).join("");
  return `<details class="evidence"><summary>Bevisspår (${refs.size} källbelägg)</summary><ul>${items}</ul></details>`;
}

function buildMethod() {
  $("method-body").innerHTML =
    `<p>Varje parti får ett betyg <b>0–5</b> per kategori, sammanvägt av fyra delpoäng:</p>
     <ul>
       <li><b>A – Agerande (40 %):</b> hur mycket partiet faktiskt prioriterar kategorin (andel av egna motioner).</li>
       <li><b>B – Evidens (35 %):</b> om partiets drivna åtgärder enligt officiell svensk evidens rör indikatorerna åt rätt håll.</li>
       <li><b>C – Ansvar (15 %):</b> om partiet haft makt (regering/region) att genomföra.</li>
       <li><b>D – Resultat (10 %):</b> om indikatorerna förbättrades där partiet hade ansvar.</li>
     </ul>
     <p>Du viktar de 7 kategorierna; <b>totalpoängen räknas i din webbläsare</b> som Σ (din vikt × kategoribetyg).
     Osäkerhetsintervall visas — överlappar två partiers band kan de inte säkert särskiljas.</p>
     <p class="warn"><b>Version 0:</b> betygen är en pipeline-demonstration på riktig officiell data, inte ett färdigt
     röstråd. Rankingen drivs ännu främst av aktivitet + makt (+ resultat där makt funnits), och partiståndpunkterna
     (delpoäng B) är källbelagda men ännu inte expertgranskade. Tolka med försiktighet.</p>`;
}

function buildAttribution() {
  const names = new Set();
  for (const e of Object.values(EVID)) if (e && e.source_name) names.add(e.source_name);
  const list = [...names].sort((a, b) => a.localeCompare(b, "sv"));
  $("attribution").textContent = list.length
    ? `Källor: ${list.join(" · ")}.`
    : "Källor: officiell svensk myndighets- och riksdagsdata.";
}

load();
