"""Polisen — bekräftade skjutningar (delpoäng D, kategori trygghet).

Polisen för på regeringens uppdrag (sedan nov 2016) officiell statistik över bekräftade
skjutningar, men publicerar den ENDAST som PDF per polisregion och år (ingen maskinläsbar
tabell). Den nationella årstotalen är därför troget transkriberad till config/skjutningar.yaml
— samma mönster som budget_ramar/SKR-styren, ingen runtime-PDF-parser som kan korrumpera D tyst.
Varje årsvärde korsverifierades vid transkribering (regionsumma == PDF:ens nationella Totalt-rad),
reproducerbart via pipeline/tools/skjutningar_transcribe.py.

Den här modulen läser bara config -> observations-rader (nätverksfri). Indikatorn är
skjutningar_sprangningar (riktning down); endast skjutningar transkriberas (etablerad jämförbar
serie fr.o.m. 2017) — se config-headern för måttvalet.
"""

from __future__ import annotations

from typing import Any

from .. import config

# Kanoniska indikatorer denna modul levererar (för täcknings-gaten i tests/test_fas3_gate.py).
INDICATORS = ("skjutningar_sprangningar",)

# Serie-drift-förväntan (pipeline.expectations). Ankare = stabila publicerade värden (±rel_tol).
EXPECT = {
    "skjutningar_sprangningar": {"min_points": 7, "value_range": [50, 600],
                                 "min_latest_year": 2024, "anchors": {"2020": 379, "2022": 391}},
}


def build_skjutningar_observations(cfg: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    """Transkriberade årstotaler (config/skjutningar.yaml) -> observations-rader (Riket).

    Ren funktion med injicerbar cfg -> golden-testbar utan fil-IO.
    """
    cfg = config.skjutningar() if cfg is None else cfg
    cat, sub, ind, unit = cfg["category"], cfg["submeasure"], cfg["indicator"], cfg["unit"]
    rows: list[dict[str, Any]] = []
    for year, entry in sorted(cfg["years"].items()):
        rows.append({
            "id": f"obs:polisen:{ind}:{year}",
            "category": cat, "submeasure": sub, "indicator": ind, "period": str(year),
            "value": float(entry["value"]), "unit": unit, "geography": "Riket",
            "source_ref": f"polisen:skjutningar:{year}",
        })
    return rows
