"""Transkriberingsaid: SKR-CSV (Styren i kommuner 1994-2022) -> config/subnational_municipalities.yaml.

ENGÅNGSVERKTYG, inte en del av scoring-pipelinen. Läser SKR:s officiella öppna-data-CSV och
SKRIVER config-filen direkt (290 kommuner × 3 mandatperioder är för många för handtranskribering;
maskinell generering ur den officiella källan är dessutom felfri och fullt reproducerbar). Den
genererade filen är versionsstyrd config (källan till sanning); ingen runtime-parser av CSV:n.

Hämta källfilen (gitignorad, stannar lokalt i data/raw/):
  Dataset: SKR "Styren i kommuner 1994-2022", catalog.skl.se (öppna data)
  CSV:     https://catalog.skl.se/store/1/resource/127
  curl -sL "https://catalog.skl.se/store/1/resource/127" -o data/raw/skr/kommuner_1994_2022.csv

Kör:  python -m pipeline.tools.skr_municipalities_transcribe
Endast de 8 riksdagspartierna tas med (L/FP->L); lokala partier (ÖP) räknas inte.
Skriver kontrollsummor (antal kommuner med partiet i styret per valår) som matchar SKR:s
halvtidsuppföljnings-PDF inom ±2 (mindre ögonblicksvariation mellan två SKR-produkter).
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

CSV_PATH = Path("data/raw/skr/kommuner_1994_2022.csv")
OUT_PATH = Path("config/subnational_municipalities.yaml")
YEARS = ("2014", "2018", "2022")
TERMS = ("2014-2018", "2018-2022", "2022-2026")
PARTY_COLS = ["M", "C", "L/FP", "KD", "S", "V", "MP", "SD"]
NORM = {"L/FP": "L"}
CANON_ORDER = ["S", "M", "SD", "C", "V", "KD", "L", "MP"]


def _col(rows: list[dict], needle: str) -> str:
    return next(c for c in rows[0] if needle in c.replace("﻿", ""))


def parse(csv_path: Path = CSV_PATH) -> tuple[dict, dict]:
    """-> ({kod -> {name, terms:[parties_per_term]}}, {valår -> {parti -> antal kommuner}})."""
    if not csv_path.exists():
        raise SystemExit(f"Saknar källfil {csv_path} — se modulens docstring för curl-kommando.")
    rows = list(csv.DictReader(csv_path.open(encoding="utf-8-sig"), delimiter=";"))
    year_col = _col(rows, "Valår")
    code_col = _col(rows, "Kod")
    name_col = _col(rows, "Kommun")
    by_code: dict[str, dict] = {}
    tally: dict[str, dict[str, int]] = {y: {p: 0 for p in CANON_ORDER} for y in YEARS}
    for r in rows:
        yr = (r.get(year_col) or "").strip()
        if yr not in YEARS:
            continue
        code = (r.get(code_col) or "").strip().zfill(4)
        name = (r.get(name_col) or "").strip().removesuffix(" kommun").strip()
        present = {NORM.get(c, c) for c in PARTY_COLS if (r.get(c) or "").strip()}
        parties = [p for p in CANON_ORDER if p in present]
        for p in parties:
            tally[yr][p] += 1
        d = by_code.setdefault(code, {"name": name, "terms": {}})
        d["terms"][yr] = parties
    return by_code, tally


def render(by_code: dict, tally: dict) -> str:
    out = [
        "# Rösta — kommunala styren per mandatperiod (delpoäng C, subnationell makt).",
        "#",
        "# GENERERAD config ur SKR:s officiella öppna data \"Styren i kommuner 1994-2022\"",
        "# (catalog.skl.se, CSV resource/127) via pipeline/tools/skr_municipalities_transcribe.py.",
        "# Källan till sanning; ingen runtime-parser. Endast de 8 riksdagspartierna; lokala partier",
        "# (ÖP) räknas ej. terms = [2014-2018, 2018-2022, 2022-2026] (post-val-styre per period).",
        "# kod = SCB:s 4-siffriga kommunkod (Kolada-format). Se docs/done/fas1c_subnational_metod.md.",
        "#",
        "# Kontrollsummor (antal kommuner med partiet i styret per valår; ±2 mot SKR:s",
        "# halvtidsuppföljnings-PDF \"efter valet 2022\" pga ögonblicksvariation mellan SKR-produkter):",
    ]
    for yr in YEARS:
        out.append(f"#   {yr}: " + "  ".join(f"{p}={tally[yr][p]}" for p in CANON_ORDER))
    out.append("version: 1")
    out.append('source: "SKR – Styren i kommuner 1994-2022 (öppna data, catalog.skl.se resource/127)"')
    out.append('source_url: "https://catalog.skl.se/store/1/resource/127"')
    out.append("retrieved: 2026-05-31")
    out.append("municipalities:")
    for code in sorted(by_code):
        d = by_code[code]
        terms = d["terms"]
        if set(terms) != set(YEARS):
            raise SystemExit(f"Kommun {code} saknar valår: {set(YEARS) - set(terms)}")
        lists = ", ".join("[" + ", ".join(terms[y]) + "]" for y in YEARS)
        name = d["name"].replace('"', "'")
        out.append(f'  "{code}": {{ name: "{name}", terms: [{lists}] }}')
    return "\n".join(out) + "\n"


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    by_code, tally = parse()
    OUT_PATH.write_text(render(by_code, tally), encoding="utf-8")
    print(f"Skrev {OUT_PATH} ({len(by_code)} kommuner).")
    for yr in YEARS:
        print(f"  {yr}: " + "  ".join(f"{p}={tally[yr][p]}" for p in CANON_ORDER))


if __name__ == "__main__":
    main()
