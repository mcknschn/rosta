"""Polisen — bekräftade skjutningar + sprängningar (delpoäng D, kategori trygghet).

Polisen för officiell statistik över bekräftade skjutningar (regeringsuppdrag nov 2016) och
sprängningar/detonationer (fr.o.m. 2018), men publicerar dem ENDAST som PDF per polisregion och
år (ingen maskinläsbar tabell). De nationella årstotalerna är därför troget transkriberade till
config/skjutningar_sprangningar.yaml — samma mönster som budget_ramar/SKR-styren, ingen runtime-
PDF-parser som kan korrumpera D tyst. Varje komponent och år korsverifierades vid transkribering
(regionsumma == PDF:ens nationella Totalt-rad), reproducerbart via tools/skjutningar_transcribe.py.

Indikatorn skjutningar_sprangningar (riktning down) = SUMMAN skjutningar + sprängningar per år,
så datan matchar indikatornamnet. Serien börjar 2018 (då båda komponenterna finns). Den här
modulen läser bara config -> observations (nätverksfri).
"""

from __future__ import annotations

from typing import Any

from .. import config

# Kanoniska indikatorer denna modul levererar (för täcknings-gaten i tests/test_fas3_gate.py).
INDICATORS = ("skjutningar_sprangningar",)

# Serie-drift-förväntan (pipeline.expectations). Ankare = stabila publicerade värden (±rel_tol).
# Kombinerade årstotaler (skjutningar + sprängningar) 2018-2025.
EXPECT = {
    "skjutningar_sprangningar": {"min_points": 7, "value_range": [200, 800],
                                 "min_latest_year": 2024, "anchors": {"2020": 486, "2023": 527}},
}


def build_skjutningar_sprangningar_observations(
    cfg: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Transkriberade årstotaler -> observations-rader (Riket); värde = skjutningar + sprängningar.

    Ren funktion med injicerbar cfg -> golden-testbar utan fil-IO.
    """
    cfg = config.skjutningar_sprangningar() if cfg is None else cfg
    cat, sub, ind, unit = cfg["category"], cfg["submeasure"], cfg["indicator"], cfg["unit"]
    rows: list[dict[str, Any]] = []
    for year, entry in sorted(cfg["years"].items()):
        total = float(entry["skjutningar"]) + float(entry["sprangningar"])
        rows.append({
            "id": f"obs:polisen:{ind}:{year}",
            "category": cat, "submeasure": sub, "indicator": ind, "period": str(year),
            "value": total, "unit": unit, "geography": "Riket",
            "source_ref": f"polisen:skjutningar_sprangningar:{year}",
        })
    return rows
