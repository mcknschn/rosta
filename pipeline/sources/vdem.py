"""V-Dem (Göteborgs universitet) — Sveriges demokrati-/institutionsindex (delpoäng D, demokrati).

Öppnar fyra tidigare D-tomma demokrati-submått med var sin V-Dem-årsserie för Sverige (riktning
up). V-Dem-institutet är värdat vid Göteborgs universitet → svensk akademisk källa (CLAUDE.md).
Värdena är troget transkriberade till config/vdem_demokrati.yaml ur V-Dems officiella dataset (v16),
samma mönster som övriga D-serier — ingen runtime-parser i pipelinen. Reproducerbar avläsning/audit:
pipeline/tools/vdem_transcribe.py (de tre OWID-tillgängliga indexen korsverifierades dessutom exakt
mot Our World in Data). Se config-headern för källregel-motivering + expert-kodnings-caveat (v0).

Den här modulen läser bara config -> observations (nätverksfri, golden-testbar).
"""

from __future__ import annotations

from typing import Any

from .. import config

# Kanoniska indikatorer denna modul levererar (för täcknings-gaten i tests/test_fas3_gate.py).
# Ett V-Dem-index per tidigare D-tomt demokrati-submått.
INDICATORS = (
    "rattsstatsindex",
    "yttrandefrihetsindex",
    "privata_friheter",
    "horisontellt_ansvarsutkravande",
)

# Serie-drift-förväntan (pipeline.expectations). Sverige ligger nära skalans tak (0,94-0,995);
# ankare = stabila publicerade V-Dem v16-värden (±rel_tol). Alla 0-1-skala, riktning up.
EXPECT = {
    "rattsstatsindex": {"min_points": 26, "value_range": [0.9, 1.0], "min_latest_year": 2025,
                        "anchors": {"2014": 0.995, "2024": 0.99}},
    "yttrandefrihetsindex": {"min_points": 26, "value_range": [0.9, 1.0], "min_latest_year": 2025,
                             "anchors": {"2014": 0.974, "2024": 0.946}},
    "privata_friheter": {"min_points": 26, "value_range": [0.9, 1.0], "min_latest_year": 2025,
                         "anchors": {"2014": 0.968, "2024": 0.948}},
    "horisontellt_ansvarsutkravande": {"min_points": 26, "value_range": [0.9, 1.0],
                                       "min_latest_year": 2025, "anchors": {"2014": 0.98, "2024": 0.989}},
}


def build_vdem_observations(cfg: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    """Transkriberade V-Dem-årsserier -> observations-rader (Riket); värde = index (0-1).

    Ren funktion med injicerbar cfg -> golden-testbar utan fil-IO. Emitterar alla indikatorer i
    cfg['indicators']; varje måste finnas i INDICATORS (annars hård fail i build_fas3).
    """
    cfg = config.vdem_demokrati() if cfg is None else cfg
    cat = cfg["category"]
    rows: list[dict[str, Any]] = []
    for ind, spec in cfg["indicators"].items():
        sub, unit = spec["submeasure"], spec["unit"]
        for year, value in sorted(spec["years"].items()):
            rows.append({
                "id": f"obs:vdem:{ind}:{year}",
                "category": cat, "submeasure": sub, "indicator": ind, "period": str(year),
                "value": float(value), "unit": unit, "geography": "Riket",
                "source_ref": f"vdem:{ind}:{year}",
            })
    return rows
