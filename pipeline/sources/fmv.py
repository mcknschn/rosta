"""FMV — leveransindex ap. 1:3.1 (delpoäng D, kategori forsvar).

Indikatorn materielleveransutfall (genomforbarhet_leverans, riktning up) bärs av FMV:s
leveransindex för anslagspost 1:3.1: andel av årets planerade materielleveranser till
Försvarsmakten som levererats i enlighet med årets leveransplan, värdeviktat (kan överstiga 100
när tidigarelagda leveranser överträffar planen). Serien börjar 2021 — FMV intygar själv
jämförbarhet fr.o.m. ÅR 2021 och att 2020 och tidigare år är OJÄMFÖRBARA (annan indikator,
andra principer/indata; kedjecitat i configen). Värdena är troget transkriberade till
config/materielleveransutfall.yaml — samma mönster som effektbrist/personal_varnpliktiga
(källrad per värde, maskinverifierade ur original-PDF:erna med PyMuPDF, ingen runtime-PDF-parser
som kan korrumpera D tyst). v0-caveats (självreferentiell måttstock/FMV-överplanering 2025,
kalenderårskänslighet, viktningsbas-skifte 2022->2023, endast ap. 1:3.1 — Ukraina-donationer
ingår ej) dokumenterade i configen; öppnar försvarets sista D-tomma icke-target-undermått.
Den här modulen läser bara config -> observations (nätverksfri, golden-testbar).
"""

from __future__ import annotations

from typing import Any

from .. import config

# Kanoniska indikatorer denna modul levererar (för täcknings-gaten i tests/test_fas3_gate.py).
INDICATORS = ("materielleveransutfall",)

# Serie-drift-förväntan (pipeline.expectations). Ankare = stabila publicerade värden (±rel_tol).
# Leveransindex ap. 1:3.1, 2021-2025 (riktning up; värdeviktat, kan överstiga 100).
EXPECT = {
    "materielleveransutfall": {"min_points": 5, "value_range": [10, 150],
                               "min_latest_year": 2025, "anchors": {"2022": 97}},
}


def build_materielleveransutfall_observations(
    cfg: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Transkriberade årsvärden -> observations-rader (Riket).

    Värdet = FMV:s leveransindex ap. 1:3.1 för kalenderåret (index, andel av leveransplan i %).
    Ren funktion med injicerbar cfg -> golden-testbar utan fil-IO.
    """
    cfg = config.materielleveransutfall() if cfg is None else cfg
    cat, sub, ind, unit = cfg["category"], cfg["submeasure"], cfg["indicator"], cfg["unit"]
    return [
        {
            "id": f"obs:fmv:{ind}:{year}",
            "category": cat, "submeasure": sub, "indicator": ind, "period": str(year),
            "value": float(entry["value"]), "unit": unit, "geography": "Riket",
            "source_ref": f"fmv:{ind}:{year}",
        }
        for year, entry in sorted(cfg["years"].items())
    ]
