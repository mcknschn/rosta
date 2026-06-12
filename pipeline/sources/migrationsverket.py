"""Migrationsverket — genomsnittlig handläggningstid för avgjorda asylärenden (delpoäng D, integration).

Öppnar submåttet migrationssystem (tidigare D-tomt). Migrationsverket publicerar "Avgjorda
asylärenden" per år (xlsx); den genomsnittliga handläggningstiden för reguljära förstagångsärenden
(deltabellen "Asyl", EXKL. massflyktsdirektivet/ukrainska medborgare) är troget transkriberad till
config/asyl_handlaggningstid.yaml — samma mönster som ukraina_stod/personal_varnpliktiga (källrad per
värde, ingen runtime-xlsx-parser som kan korrumpera D tyst).

Riktning down (kortare = bättre). Den här modulen läser bara config -> observations (nätverksfri,
golden-testbar). Reproducerbart revisionsspår: pipeline/tools/asyl_handlaggningstid_verify.py
(hämtar de officiella per-års-xlsx och korsverifierar varje årsvärde).
"""

from __future__ import annotations

from typing import Any

from .. import config

# Kanoniska indikatorer denna modul levererar (för täcknings-gaten i tests/test_fas3_gate.py).
INDICATORS = ("asyl_handlaggningstid",)

# Serie-drift-förväntan (pipeline.expectations). Ankare = stabila publicerade värden (±rel_tol).
# Handläggningstid (dagar) per kalenderår 2021-2025, riktning down.
EXPECT = {
    "asyl_handlaggningstid": {"min_points": 5, "value_range": [100, 400],
                              "min_latest_year": 2025, "anchors": {"2021": 257, "2025": 180}},
}


def build_asyl_handlaggningstid_observations(
    cfg: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Transkriberade årsvärden -> observations-rader (Riket); värde = handläggningstid (dagar).

    Ren funktion med injicerbar cfg -> golden-testbar utan fil-IO.
    """
    cfg = config.asyl_handlaggningstid() if cfg is None else cfg
    cat, sub, ind, unit = cfg["category"], cfg["submeasure"], cfg["indicator"], cfg["unit"]
    rows: list[dict[str, Any]] = []
    for year, entry in sorted(cfg["years"].items()):
        rows.append({
            "id": f"obs:migrationsverket:{ind}:{year}",
            "category": cat, "submeasure": sub, "indicator": ind, "period": str(year),
            "value": float(entry["value"]), "unit": unit, "geography": "Riket",
            "source_ref": f"migrationsverket:asyl_handlaggningstid:{year}",
        })
    return rows
