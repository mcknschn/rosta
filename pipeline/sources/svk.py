"""Svenska kraftnät — nettoimport vid vinterns topplasttimme (delpoäng D, kategori klimat).

Indikatorn effektbrist (energi_elpriser, riktning down) bärs av NETTOIMPORTEN vid vinterns
topplasttimme (MWh/h; positivt = nettoimport, negativt = nettoexport) ur Svk:s lagstadgade
regeringsrapport "Kraftbalansen på den svenska elmarknaden" (3 § förordning 2007:1119),
UTFALLS-kapitlet "Vinterns topplasttimme". Faktisk effektbrist (lastfrånkoppling) har ALDRIG
inträffat (Svk rapport 2025 s.30) — konstant 0 bär inget D-tecken; högre importberoende under
årets mest ansträngda timme = mindre inhemsk effektmarginal = närmare effektbrist, så riktningen
down matchar direkt. Värdena är troget transkriberade till config/effektbrist.yaml — samma
mönster som personal_varnpliktiga/ukraina_stod/skjutningar_sprangningar (källrad per värde,
maskinverifierade ur original-PDF:erna med PyMuPDF, ingen runtime-PDF-parser som kan korrumpera
D tyst). Vinterår etiketteras på SLUTÅRET (vintern 2024/2025 -> 2025); måttvals-, väder- och
robusthetscaveats (prognos_normalvinter-sekundärserien) dokumenterade i configen.
Den här modulen läser bara config -> observations (nätverksfri, golden-testbar).
"""

from __future__ import annotations

from typing import Any

from .. import config

# Kanoniska indikatorer denna modul levererar (för täcknings-gaten i tests/test_fas3_gate.py).
INDICATORS = ("effektbrist",)

# Serie-drift-förväntan (pipeline.expectations). Ankare = stabila publicerade värden (±rel_tol).
# Nettoimport vid vinterns topplasttimme, vintrarna 2019/20-2025/26 (MWh/h, riktning down).
EXPECT = {
    "effektbrist": {"min_points": 7, "value_range": [-6000, 8000],
                    "min_latest_year": 2026, "anchors": {"2023": 3290}},
}


def build_effektbrist_observations(
    cfg: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Transkriberade vinterårsvärden -> observations-rader (Riket).

    Värdet = nettoimport vid vinterns topplasttimme (MWh/h), etiketterat på vinterns slutår;
    negativa värden (nettoexport) bevaras med tecken. Ren funktion med injicerbar cfg ->
    golden-testbar utan fil-IO. Sekundärserien prognos_normalvinter läses INTE (prognos, ej utfall).
    """
    cfg = config.effektbrist() if cfg is None else cfg
    cat, sub, ind, unit = cfg["category"], cfg["submeasure"], cfg["indicator"], cfg["unit"]
    return [
        {
            "id": f"obs:svk:{ind}:{year}",
            "category": cat, "submeasure": sub, "indicator": ind, "period": str(year),
            "value": float(entry["value"]), "unit": unit, "geography": "Riket",
            "source_ref": f"svk:{ind}:{year}",
        }
        for year, entry in sorted(cfg["years"].items())
    ]
