"""Reproducerar och AUDITERAR config/hackande_faglar_skog.yaml mot sverigesmiljomal.se.

Sveriges miljömåls-portal bäddar in tidsserien för "Häckande fåglar i skogen" (Svensk
Fågeltaxering, Lunds universitet) som ett Highcharts-JSON-objekt direkt i sidans HTML. Det här
verktyget är "HTML-avläsaren": det hämtar sid-HTML:en, extraherar den SAMLADE skogsfågelserien
(serienamn "Häckande fåglar i skogen" — inte habitat-delindexen lövskog/gammal skog/död ved) och
korsverifierar varje årsvärde mot den pinnade configen.

Kör manuellt (ej en pipeline-/test-dependens):

    python -m pipeline.tools.faglar_transcribe

Exit 0 = configen matchar live-sidan; exit 1 = avvikelse (värde ändrat i källan, ny datapunkt, eller
URL som behöver uppdateras). Detta är transkriberingens revisionsspår — ingen runtime-HTML-parser
körs i själva pipelinen (sverigesmiljomal.py läser bara den pinnade configen).
"""

from __future__ import annotations

import json
import re
import sys

import httpx

from .. import config

_UA = {"User-Agent": "rosta-datapipeline/0.1 (civic-tech; official swedish open data)"}
# Det SAMLADE indexet. Måste matchas EXAKT så vi inte tyst plockar ett habitat-delindex (vars
# namn alla börjar med "Häckande fåglar -").
_SERIES_NAME = "Häckande fåglar i skogen"
_TOL = 0.05  # tillåten absolut avvikelse i indexenheter (källan kan revideras marginellt)


def extract_series(html: str, series_name: str) -> dict[str, float]:
    """Plockar {år -> värde} för en namngiven Highcharts-serie ur portalsidans HTML."""
    for m in re.finditer(r'"name"\s*:\s*"([^"]+)"\s*,\s*"data"\s*:\s*(\[\[.*?\]\])', html, re.S):
        if m.group(1) == series_name:
            return {int(y): float(v) for y, v in json.loads(m.group(2))}
    raise ValueError(f"Hittar ingen Highcharts-serie {series_name!r} i sid-HTML:en (sidan ändrad?)")


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    cfg = config.hackande_faglar_skog()
    url = cfg["source"]
    print(f"== Auditerar config/hackande_faglar_skog.yaml mot {url} ==")
    with httpx.Client(headers=_UA, follow_redirects=True, timeout=60) as c:
        resp = c.get(url)
        resp.raise_for_status()
        live = extract_series(resp.text, cfg.get("series_name", _SERIES_NAME))

    cfg_years = {int(y): float(v) for y, v in cfg["years"].items()}
    mismatches = 0
    for year in sorted(set(cfg_years) | set(live)):
        cv = cfg_years.get(year)
        lv = live.get(year)
        ok = cv is not None and lv is not None and abs(cv - lv) <= _TOL
        flag = "OK" if ok else "AVVIKELSE"
        print(f"  {year}: cfg={cv}  live={lv}   [{flag}]")
        if not ok:
            mismatches += 1
    if mismatches:
        raise SystemExit(f"\n{mismatches} avvikelse(r) — uppdatera config/hackande_faglar_skog.yaml.")
    print(f"\nAlla {len(cfg_years)} år matchar live-serien (±{_TOL} indexenheter).")


if __name__ == "__main__":
    main()
