"""Regeringen/Försvarsdepartementet — Sveriges militära stöd till Ukraina (delpoäng D, forsvar).

Öppnar submåttet nato_ukraina (tidigare D-tomt). Regeringen redovisar det militära stödet till
Ukraina per år på sin samlade stöd-sida; värdet per kalenderår är troget transkriberat till
config/ukraina_stod.yaml — samma mönster som personal_varnpliktiga/skjutningar_sprangningar
(källrad per värde, ingen runtime-HTML/PDF-parser som kan korrumpera D tyst).

Endast MILITÄRT stöd (matchar försvarskategorin); 2026-2027 (beslutad framåtram) exkluderas i
configen. Den här modulen läser bara config -> observations (nätverksfri, golden-testbar).
"""

from __future__ import annotations

from typing import Any

from .. import config

# Kanoniska indikatorer denna modul levererar (för täcknings-gaten i tests/test_fas3_gate.py).
INDICATORS = ("ukraina_stod",)

# Serie-drift-förväntan (pipeline.expectations). Ankare = stabila publicerade värden (±rel_tol).
# Militärt stöd per kalenderår 2022-2025 (mdr kr, riktning up).
EXPECT = {
    "ukraina_stod": {"min_points": 4, "value_range": [1, 60],
                     "min_latest_year": 2025, "anchors": {"2022": 6.1, "2025": 40.0}},
}


def build_ukraina_stod_observations(
    cfg: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Transkriberade årsvärden -> observations-rader (Riket); värde = militärt stöd (mdr kr).

    Ren funktion med injicerbar cfg -> golden-testbar utan fil-IO.
    """
    cfg = config.ukraina_stod() if cfg is None else cfg
    cat, sub, ind, unit = cfg["category"], cfg["submeasure"], cfg["indicator"], cfg["unit"]
    rows: list[dict[str, Any]] = []
    for year, entry in sorted(cfg["years"].items()):
        rows.append({
            "id": f"obs:regeringen:{ind}:{year}",
            "category": cat, "submeasure": sub, "indicator": ind, "period": str(year),
            "value": float(entry["value"]), "unit": unit, "geography": "Riket",
            "source_ref": f"regeringen:ukraina_stod:{year}",
        })
    return rows
