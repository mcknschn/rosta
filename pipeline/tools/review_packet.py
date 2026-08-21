"""Genererar expertgranskningspaketet för de tre version-0-configfilerna.

party_positions.yaml (B), evidence_ledger.yaml (B) och budget_ramar.yaml (A:a1) är alla
AI-utkast (version 0) som projektets disciplin flaggar som "kräver mänsklig slutgranskning
innan skarp betygsättning". Det här verktyget läser dem deterministiskt och skriver ett
granskningspaket till docs/done/expertgranskning/ som fokuserar mänsklig granskning på de rader
som faktiskt rör betygen och på den högrisk-delmängd (opposes/laddade/lågkonfidens) där fel
gör störst skada.

Genererar inga omdömen och ändrar ingen config — ren härledning ur befintlig config + det
faktiska join-maskineriet (pipeline.positions, pipeline.budget). Kör:

    python -m pipeline.tools.review_packet
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from typing import Any

from pipeline import budget, config
from pipeline.positions import _FLIP, build_evidence_effect_claims

DOCS_DIR = config.CONFIG_DIR.parent / "docs" / "done" / "expertgranskning"

# Föredragen källperiod (senaste mandatperioden+). Äldre källor flaggas för tidskontroll.
_PREFERRED_FROM_YEAR = 2022

# Flaggor som lyfter en ståndpunkt till prioriterad granskning (högst betygspåverkan/risk).
_PRIORITY_FLAGS = {"opposes", "prop_avslag", "ny_karnkraft", "low_confidence", "single_member"}


def _year(date: Any) -> int | None:
    m = re.search(r"(19|20)\d{2}", str(date))
    return int(m.group(0)) if m else None


def _indicator_maps() -> tuple[dict[str, str], dict[str, str]]:
    """indikator -> kategori, indikator -> riktning (up/down/target) ur categories.yaml."""
    ind_cat: dict[str, str] = {}
    ind_dir: dict[str, str] = {}
    for c in config.categories()["categories"]:
        for ind in c.get("indicators", []):
            ind_cat[ind["id"]] = c["id"]
            ind_dir[ind["id"]] = ind["direction"]
    return ind_cat, ind_dir


def _b_arrow(direction: str) -> str:
    """Evidensens effektiva riktning -> läsbar B-konsekvens."""
    return {
        "positive": "↑ mot bättre (höjer B)",
        "negative": "↓ mot sämre (sänker B)",
        "mixed": "↔ blandad (≈neutral B)",
        "unclear": "? oklar (≈neutral B)",
    }.get(direction, direction)


def _is_single_member(pos: dict[str, Any]) -> bool:
    st = str(pos.get("source_type", "")).lower()
    note = str(pos.get("mapping_note", "")).lower()
    if "enskild motion" in st:
        return True
    # mapping_note säger uttryckligen single-member -> low
    return "single-member" in note and "is_single_member=false" not in note


def analyse() -> dict[str, Any]:
    """Härleder all granskningsdata deterministiskt ur config + join-maskineriet."""
    positions = config.party_positions()["entries"]
    ledger = config.evidence_ledger()["entries"]
    ind_cat, _ind_dir = _indicator_maps()

    by_policy: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for e in ledger:
        by_policy[e["policy_type"]].append(e)

    # Vilka indikatoreffekter varje ståndpunkt faktiskt ger (supports=behåll, opposes=vänd).
    enriched: list[dict[str, Any]] = []
    for p in positions:
        matches = by_policy.get(p["policy_type"], [])
        effects = []
        for e in matches:
            eff_dir = e["direction"] if p["stance"] == "supports" else _FLIP.get(e["direction"], "unclear")
            effects.append({
                "category": e["category"],
                "indicator": e["indicator"],
                "ledger_direction": e["direction"],
                "effective_direction": eff_dir,
                "evidence_level": e["evidence_level"],
                "effect_strength": e["effect_strength"],
                "ledger_confidence": e["confidence"],
            })
        yr = _year(p.get("date"))
        flags = []
        if p["stance"] == "opposes":
            flags.append("opposes")
        if re.search(r"avsl[åa]r\s+(regeringens\s+)?prop", str(p.get("quote", "")), re.I):
            flags.append("prop_avslag")
        if p["policy_type"] == "ny_karnkraft":
            flags.append("ny_karnkraft")
        if p.get("confidence") == "low":
            flags.append("low_confidence")
        if p.get("confidence") is None:
            flags.append("no_confidence_field")
        if _is_single_member(p):
            flags.append("single_member")
        if yr is not None and yr < _PREFERRED_FROM_YEAR:
            flags.append(f"old_source_{yr}")
        if any(eff["ledger_direction"] in ("unclear", "mixed") for eff in effects):
            flags.append("ledger_unclear_or_mixed")
        if any(eff["ledger_direction"] == "negative" for eff in effects):
            flags.append("ledger_negative_direction")
        enriched.append({**p, "_effects": effects, "_year": yr, "_flags": flags})

    priority = [e for e in enriched if _PRIORITY_FLAGS & set(e["_flags"]) or any(
        f.startswith("old_source_") for f in e["_flags"])]

    return {
        "positions": enriched,
        "ledger": ledger,
        "by_policy": by_policy,
        "ind_cat": ind_cat,
        "priority": priority,
        "counts": {
            "positions_total": len(positions),
            "ledger_entries": len(ledger),
            "claims_produced": len(build_evidence_effect_claims(positions, ledger)),
            "stance": dict(Counter(p["stance"] for p in positions)),
            "confidence": dict(Counter(str(p.get("confidence")) for p in positions)),
            "priority_count": len(priority),
        },
    }


def _esc(s: Any) -> str:
    return str(s).replace("|", "\\|").replace("\n", " ").strip()


def write_positions_doc(a: dict[str, Any]) -> None:
    pos = a["positions"]
    by_cat_policy: dict[str, dict[str, list[dict[str, Any]]]] = defaultdict(lambda: defaultdict(list))
    for p in pos:
        # kategori via första effekten (alla effekter på en policy delar sällan kategori men
        # första räcker för gruppering); fall tillbaka på "?".
        cat = p["_effects"][0]["category"] if p["_effects"] else "?"
        by_cat_policy[cat][p["policy_type"]].append(p)

    lines: list[str] = []
    lines.append("# Granskning B — partiståndpunkter (`config/party_positions.yaml`)")
    lines.append("")
    lines.append("> AUTOGENERERAD av `pipeline/tools/review_packet.py` — ändra inte för hand.")
    lines.append("> Källa för betygskonsekvensen är det faktiska join-maskineriet i `pipeline/positions.py`.")
    lines.append("")
    c = a["counts"]
    lines.append(f"**{c['positions_total']} ståndpunkter** → {c['claims_produced']} evidence_effect-claims. "
                 f"Stance: {c['stance']}. Konfidens: {c['confidence']}.")
    lines.append("")
    lines.append("Pipelinen joinar **bara** på `party + policy_type + stance`. `supports` behåller "
                 "evidensens riktning; `opposes` **vänder** den. Övriga fält är spårbarhet.")
    lines.append("")
    lines.append("## Så granskar du")
    lines.append("")
    lines.append("1. Öppna `source_url`, läs `quote` i sitt sammanhang (`.text`-endpoint för riksdagsdok).")
    lines.append("2. Bekräfta att (a) citatet är ordagrant, (b) `stance` stämmer med partiets faktiska "
                 "linje på det **namngivna instrumentet**, (c) `policy_type` är rätt åtgärdstyp.")
    lines.append("3. Sätt verdikt i kolumnen **OK?** (✅/✏️/❌) och notera ev. rättelse.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## ⚑ Prioriterad granskning (högst betygspåverkan/risk)")
    lines.append("")
    lines.append(f"{c['priority_count']} rader där fel gör störst skada: **opposes** (vänder evidensen), "
                 "**prop_avslag** (måste verifiera att propositionen ÄR instrumentet), **ny_karnkraft** "
                 "(laddad fråga), **low_confidence**, **single_member**, **äldre källa**.")
    lines.append("")
    lines.append("| OK? | Parti | Åtgärdstyp | Stance | B-konsekvens | Konf. | doc_id | Datum | Flaggor |")
    lines.append("|-----|-------|-----------|--------|--------------|-------|--------|-------|---------|")
    for p in sorted(a["priority"], key=lambda x: (x["policy_type"], x["party"])):
        arrows = "; ".join(sorted({_b_arrow(e["effective_direction"]) for e in p["_effects"]})) or "—"
        flags = ", ".join(f for f in p["_flags"] if f not in ("no_confidence_field",))
        cf = p.get("confidence") or "—"
        lines.append(f"|  | {p['party']} | {_esc(p['policy_type'])} | **{p['stance']}** | "
                     f"{arrows} | {cf} | {_esc(p.get('doc_id'))} | {_esc(p.get('date'))} | {_esc(flags)} |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Alla ståndpunkter per kategori (panelvy)")
    lines.append("")
    lines.append("Granska varje åtgärdstyp som en panel — alla partier sida vid sida, så asymmetrier syns.")
    lines.append("")
    for cat in sorted(by_cat_policy):
        lines.append(f"### {cat}")
        lines.append("")
        for policy in sorted(by_cat_policy[cat]):
            rows = sorted(by_cat_policy[cat][policy], key=lambda x: x["party"])
            led = a["by_policy"].get(policy, [])
            led_desc = "; ".join(f"{e['indicator']}={e['direction']} ({e['confidence']})" for e in led)
            lines.append(f"#### `{policy}`")
            lines.append("")
            lines.append(f"Liggarens effekt: {_esc(led_desc) or '—'}")
            lines.append("")
            lines.append("| OK? | Parti | Stance | B-konsekvens | Konf. | doc_id | Datum |")
            lines.append("|-----|-------|--------|--------------|-------|--------|-------|")
            for p in rows:
                arrows = "; ".join(sorted({_b_arrow(e["effective_direction"]) for e in p["_effects"]})) or "—"
                star = " ⚑" if (set(p["_flags"]) & _PRIORITY_FLAGS) else ""
                cf = p.get("confidence") or "—"
                lines.append(f"|  | {p['party']}{star} | {p['stance']} | {arrows} | "
                             f"{cf} | {_esc(p.get('doc_id'))} | {_esc(p.get('date'))} |")
            lines.append("")
    (DOCS_DIR / "B_partistandpunkter.md").write_text("\n".join(lines), encoding="utf-8")


def write_ledger_doc(a: dict[str, Any]) -> None:
    ledger = a["ledger"]
    # Blast-radius: vilka partier driver/motsätter sig varje policy_type.
    parties_by_policy: dict[str, list[str]] = defaultdict(list)
    for p in a["positions"]:
        parties_by_policy[p["policy_type"]].append(f"{p['party']}({'+' if p['stance']=='supports' else '−'})")

    by_cat: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for e in ledger:
        by_cat[e["category"]].append(e)

    lines: list[str] = []
    lines.append("# Granskning B — evidensliggare (`config/evidence_ledger.yaml`)")
    lines.append("")
    lines.append("> AUTOGENERERAD av `pipeline/tools/review_packet.py` — ändra inte för hand.")
    lines.append("")
    lines.append(f"**{len(ledger)} poster** (åtgärdstyp → indikatoreffekt). Generell policy-evidens, "
                 "medvetet **inte** partikopplad. Varje post sätter riktningen för ALLA partier som "
                 "driver åtgärdstypen — granska källan noga (blast-radius anges per post).")
    lines.append("")
    lines.append("## Så granskar du")
    lines.append("")
    lines.append("1. Öppna `source_url` och bekräfta att den svenska utvärderingen/akademiska källan "
                 "faktiskt stöder `direction` på `indicator` (`positive` = rör indikatorn åt RÄTT håll).")
    lines.append("2. Bedöm om `evidence_level`/`effect_strength`/`confidence` är rimliga (ej översålda).")
    lines.append("3. Särskilt: `unclear`/`mixed` ger ≈neutral B (rätt om evidensen är svag); `negative` "
                 "**vänder** semantiken; `expert_opinion` är svagast (ej uppmätt kausalitet).")
    lines.append("")
    lines.append("---")
    lines.append("")
    for cat in sorted(by_cat):
        lines.append(f"## {cat}")
        lines.append("")
        for e in by_cat[cat]:
            blast = ", ".join(sorted(parties_by_policy.get(e["policy_type"], []))) or "—(ingen ståndpunkt)"
            warn = []
            if e["direction"] in ("unclear", "mixed"):
                warn.append(f"⚠ {e['direction']} → ≈neutral B")
            if e["direction"] == "negative":
                warn.append("⚠ negativ riktning (vänder semantiken)")
            if e["evidence_level"] == "expert_opinion":
                warn.append("⚠ expert_opinion (ej uppmätt kausalitet)")
            if e["confidence"] == "low":
                warn.append("⚠ låg konfidens")
            lines.append(f"### `{e['policy_type']}` → {e['indicator']}")
            lines.append("")
            lines.append(f"- **Riktning:** {e['direction']} · **evidensnivå:** {e['evidence_level']} · "
                         f"**styrka:** {e['effect_strength']} · **konfidens:** {e['confidence']}")
            lines.append(f"- **Källa:** {_esc(e['source'])}")
            if e.get("source_url"):
                lines.append(f"- **URL:** {e['source_url']}")
            if e.get("note"):
                lines.append(f"- **Not:** {_esc(e['note'])}")
            lines.append(f"- **Påverkar partier:** {_esc(blast)}")
            if warn:
                lines.append(f"- {' · '.join(warn)}")
            lines.append("- **OK?** ⬜ (✅/✏️/❌): ")
            lines.append("")
    (DOCS_DIR / "B_evidensliggare.md").write_text("\n".join(lines), encoding="utf-8")


def write_budget_doc() -> None:
    cfg = config.budget_ramar()
    cats = config.category_ids()
    parties = config.party_codes()
    shares, active = budget.a1_shares(cats, parties)

    lines: list[str] = []
    lines.append("# Granskning A:a1 — budgetramar (`config/budget_ramar.yaml`)")
    lines.append("")
    lines.append("> AUTOGENERERAD av `pipeline/tools/review_packet.py` — ändra inte för hand.")
    lines.append("")
    lines.append("a1 = andel av partiets föreslagna utgiftsramar (Σ kategorins UO / Σ alla UO), "
                 "mätt mot de BESLUTADE utgiftsramarnas andel över ett historiskt fönster "
                 "(ADR 0005, `config/a_forankring.yaml`) — inte rangordnad över de åtta partierna. "
                 "Manuellt transkriberade ur officiella källor (ingen runtime-parser). "
                 "**Granska transkriberingen mot källraden.** Fel här korrumperar A (30 %).")
    lines.append("")
    lines.append(f"**a1-aktiva kategorier** (alla 8 partier har ram för varje kategori-UO): "
                 f"{', '.join(sorted(active)) or '—'}. Övriga faller på a2 (`A_a2_only`).")
    lines.append("")
    for y, block in (cfg.get("budget_years") or {}).items():
        lines.append(f"## Budgetår {y}")
        lines.append("")
        lines.append(f"Beslutat i: {_esc(block.get('decided_in'))}")
        lines.append("")
        ramar = block.get("ramar") or {}
        pf = block.get("party_frame") or {}
        lines.append("### Frame-tilldelning (parti → ram)")
        lines.append("")
        lines.append("| Parti | Frame | Roll | Not |")
        lines.append("|-------|-------|------|-----|")
        for party in parties:
            spec = pf.get(party, {})
            fr, ro, nt = _esc(spec.get("frame")), _esc(spec.get("role")), _esc(spec.get("note"))
            lines.append(f"| {party} | {fr} | {ro} | {nt} |")
        lines.append("")
        lines.append("### Källrad per frame (granska transkriberingen mot denna)")
        lines.append("")
        for fname, frame in ramar.items():
            lines.append(f"- **{fname}** — {_esc(frame.get('source_ref'))}")
        lines.append("")
        lines.append("### Transkriberade ramar (miljoner kr) — jämför cell för cell mot källan")
        lines.append("")
        frame_names = list(ramar)
        header = "| UO | " + " | ".join(frame_names) + " | OK? |"
        lines.append(header)
        lines.append("|" + "----|" * (len(frame_names) + 2))
        uo_keys = sorted((k for k in next(iter(ramar.values())) if k.startswith("UO")),
                         key=lambda k: int(k[2:]))
        for uo in uo_keys:
            row = f"| {uo} | " + " | ".join(str(ramar[f].get(uo, "—")) for f in frame_names) + " |  |"
            lines.append(row)
        lines.append("")
    lines.append("## Resulterande a1-andelar per parti × kategori (betygskonsekvens)")
    lines.append("")
    lines.append("| Kategori | " + " | ".join(parties) + " |")
    lines.append("|" + "----|" * (len(parties) + 1))
    for cat in cats:
        cells = " | ".join(f"{shares.get((p, cat), float('nan')):.3f}" if (p, cat) in shares else "—"
                           for p in parties)
        marker = " ✓a1" if cat in active else " (a2)"
        lines.append(f"| {cat}{marker} | {cells} |")
    lines.append("")
    (DOCS_DIR / "A_budgetramar.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    a = analyse()
    write_positions_doc(a)
    write_ledger_doc(a)
    write_budget_doc()
    index = {
        "counts": a["counts"],
        "priority_doc_ids": sorted({p.get("doc_id") for p in a["priority"]} - {None}),
        "files": ["B_partistandpunkter.md", "B_evidensliggare.md", "A_budgetramar.md"],
    }
    (DOCS_DIR / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(a["counts"], ensure_ascii=False, indent=2))
    print(f"Skrev granskningspaket till {DOCS_DIR}")


if __name__ == "__main__":
    main()
