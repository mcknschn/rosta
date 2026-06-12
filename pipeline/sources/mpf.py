"""Myndigheten för psykologiskt försvar (MPF) — försvarsvilja (delpoäng D, kategori forsvar).

Öppnar submåttet civil_beredskap (tidigare D-tomt). MPF:s (tidigare MSB:s) Opinioner-undersökning
mäter årligen försvarsviljan — andel som anser att Sverige bör göra väpnat motstånd vid ett angrepp
även om utgången är oviss. Årsvärdena (andel JA = "Ja, absolut" + "Ja, kanske") är troget
transkriberade till config/forsvarsvilja.yaml ur Opinioner-rapportens tidsserietabell — samma mönster
som ukraina_stod/personal_varnpliktiga (källrad, ingen runtime-PDF-parser).

Försvarsvilja är ett resiliens-/tillståndsmått (psykologiskt försvar = del av totalförsvaret), inte
anslag/aktivitet → klarar hammare-principen (jfr V-Dem för demokrati). Den här modulen läser bara
config -> observations (nätverksfri, golden-testbar). Luckan 2019 (ingen mätning) hanteras genom att
året saknas i configen; D beräknar bara konsekutiva årsövergångar.
"""

from __future__ import annotations

from typing import Any

from .. import config

# Kanoniska indikatorer denna modul levererar (för täcknings-gaten i tests/test_fas3_gate.py).
INDICATORS = ("forsvarsvilja",)

# Serie-drift-förväntan (pipeline.expectations). Ankare = stabila publicerade värden (±rel_tol).
# Andel JA till väpnat motstånd per mätår 2014-2025 (riktning up; lucka 2019).
EXPECT = {
    "forsvarsvilja": {"min_points": 10, "value_range": [60, 90],
                      "min_latest_year": 2025, "anchors": {"2014": 75, "2024": 79}},
}


def build_forsvarsvilja_observations(
    cfg: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Transkriberade årsvärden -> observations-rader (Riket); värde = andel JA (procent).

    Ren funktion med injicerbar cfg -> golden-testbar utan fil-IO.
    """
    cfg = config.forsvarsvilja() if cfg is None else cfg
    cat, sub, ind, unit = cfg["category"], cfg["submeasure"], cfg["indicator"], cfg["unit"]
    rows: list[dict[str, Any]] = []
    for year, entry in sorted(cfg["years"].items()):
        rows.append({
            "id": f"obs:mpf:{ind}:{year}",
            "category": cat, "submeasure": sub, "indicator": ind, "period": str(year),
            "value": float(entry["value"]), "unit": unit, "geography": "Riket",
            "source_ref": f"mpf:forsvarsvilja:{year}",
        })
    return rows
