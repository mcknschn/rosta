"""Sveriges miljömål-portalen (sverigesmiljomal.se) — häckande fåglar i skogen (delpoäng D, klimat).

Öppnar submåttet biologisk_mangfald med dess FÖRSTA D-serie. Indikatorn hackande_faglar_skog
(riktning up) = det samlade populationsindexet för 16 skogsfågelarter (basår 2002 = 100), producerat
av Svensk Fågeltaxering (Lunds universitet) och publicerat som officiell miljömålsindikator för
"Levande skogar". Tidsserien ligger maskinläsbart som Highcharts-JSON i portalsidans HTML, men
värdena är ändå troget transkriberade till config/hackande_faglar_skog.yaml (samma mönster som
övriga D-serier — ingen runtime-HTML-parser som kan korrumpera D tyst). Reproducerbar avläsning/
audit: pipeline/tools/faglar_transcribe.py. Den här modulen läser bara config -> observations.
"""

from __future__ import annotations

from typing import Any

from .. import config

# Kanoniska indikatorer denna modul levererar (för täcknings-gaten i tests/test_fas3_gate.py).
INDICATORS = ("hackande_faglar_skog",)

# Serie-drift-förväntan (pipeline.expectations). Indexvärden (basår 2002 = 100), riktning up.
EXPECT = {
    "hackande_faglar_skog": {"min_points": 23, "value_range": [50, 170], "min_latest_year": 2024,
                             "anchors": {"2002": 100.0, "2024": 109.07}},
}


def build_faglar_observations(cfg: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    """Transkriberade indexvärden -> observations-rader (Riket); värde = skogsfågelindex (2002=100).

    Ren funktion med injicerbar cfg -> golden-testbar utan fil-IO.
    """
    cfg = config.hackande_faglar_skog() if cfg is None else cfg
    cat, sub, ind, unit = cfg["category"], cfg["submeasure"], cfg["indicator"], cfg["unit"]
    rows: list[dict[str, Any]] = []
    for year, value in sorted(cfg["years"].items()):
        rows.append({
            "id": f"obs:sverigesmiljomal:{ind}:{year}",
            "category": cat, "submeasure": sub, "indicator": ind, "period": str(year),
            "value": float(value), "unit": unit, "geography": "Riket",
            "source_ref": f"sverigesmiljomal:{ind}:{year}",
        })
    return rows
