"""Försvarsmakten — antal värnpliktiga som påbörjade grundutbildning (delpoäng D, kategori forsvar).

Försvarets FÖRSTA D-serie (kategorin var tidigare strukturellt D-tom). Försvarsmaktens
årsredovisning för officiell statistik över hur många värnpliktiga som påbörjade grundutbildning
per kalenderår, men publicerar den ENDAST som FlateDecode-komprimerad PDF (ingen maskinläsbar
tabell, och verktygskedjan kan ej rendera PDF:erna). Årstotalerna är därför troget transkriberade
till config/personal_varnpliktiga.yaml — samma mönster som budget_ramar/skjutningar_sprangningar,
ingen runtime-PDF-parser som kan korrumpera D tyst.

KORSVERIFIERING: varje år stäms av mot Plikt- och prövningsverkets oberoende "inskrivna till
grundutbildning med värnplikt" (annat myndighetsmått, läst direkt ur Pliktverkets pressmeddelanden).
Båda myndigheterna ligger nära varann och visar samma enda nedgång 2021->2022. Reproducerbart via
tools/varnpliktiga_audit.py. Den här modulen läser bara config -> observations (nätverksfri).
"""

from __future__ import annotations

from typing import Any

from .. import config

# Kanoniska indikatorer denna modul levererar (för täcknings-gaten i tests/test_fas3_gate.py).
INDICATORS = ("personal_varnpliktiga",)

# Serie-drift-förväntan (pipeline.expectations). Ankare = stabila publicerade värden (±rel_tol).
# Antal som påbörjade GU per kalenderår 2018-2025 (riktning up).
EXPECT = {
    "personal_varnpliktiga": {"min_points": 7, "value_range": [3000, 12000],
                              "min_latest_year": 2024, "anchors": {"2018": 3750, "2021": 5873}},
}


def build_personal_varnpliktiga_observations(
    cfg: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Transkriberade årstotaler -> observations-rader (Riket); värde = antal påbörjade GU.

    Ren funktion med injicerbar cfg -> golden-testbar utan fil-IO.
    """
    cfg = config.personal_varnpliktiga() if cfg is None else cfg
    cat, sub, ind, unit = cfg["category"], cfg["submeasure"], cfg["indicator"], cfg["unit"]
    rows: list[dict[str, Any]] = []
    for year, entry in sorted(cfg["years"].items()):
        rows.append({
            "id": f"obs:forsvarsmakten:{ind}:{year}",
            "category": cat, "submeasure": sub, "indicator": ind, "period": str(year),
            "value": float(entry["value"]), "unit": unit, "geography": "Riket",
            "source_ref": f"forsvarsmakten:personal_varnpliktiga:{year}",
        })
    return rows
