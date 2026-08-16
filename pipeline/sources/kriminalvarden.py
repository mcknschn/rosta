"""Kriminalvården — återfall i brott inom tre år (delpoäng D, trygghet).

Öppnar submåttet aterfall_kriminalvard (tidigare D-tomt; tidigare allowlistat "blocked: PDF").
Kriminalvården redovisar i KOS 2025 Tabell 6.1 antalet klienter med starthändelse och antalet av
dem som återföll inom 3 år per ingångsår 1994–2022. Råtalen är troget transkriberade till
config/aterfall_i_brott.yaml — samma mönster som ukraina_stod/personal_varnpliktiga/
skjutningar_sprangningar (källa per serie, ingen runtime-PDF-parser som kan korrumpera D tyst).

Loadern beräknar andelen = aterfall / klienter * 100 (2 dec) ur råtalen (se config-headern för
varför råtal i stället för den heltalsavrundade publicerade andelen — sign-only D + dödzon).
`andel_publicerad` korsverifieras: avviker den beräknade andelen >0,6 pp från Kriminalvårdens egen
avrundade andel hard-failar bygget (transkriptionsfel i täljare/nämnare). Nätverksfri, golden-testbar.
"""

from __future__ import annotations

from typing import Any

from .. import config

# Kanoniska indikatorer denna modul levererar (för täcknings-gaten i tests/test_fas3_gate.py).
INDICATORS = ("aterfall_i_brott",)

# Serie-drift-förväntan (pipeline.expectations). Ankare = beräknade andelar ur Tabell 6.1 (down).
EXPECT = {
    "aterfall_i_brott": {"min_points": 29, "value_range": [25, 45], "min_latest_year": 2022,
                         "anchors": {"1999": 41.70, "2012": 29.27, "2022": 31.11}},
}

# Max avvikelse (procentenheter) mellan beräknad andel och Kriminalvårdens publicerade heltalsandel.
# Heltalsavrundning ger ±0,5 pp; 0,6 pp ger marginal men fångar ett transkriberat täljar-/nämnarfel.
_ANDEL_TOL_PP = 0.6


def build_aterfall_observations(cfg: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    """Transkriberade råtal -> observations-rader (Riket); värde = andel återfall inom 3 år (%).

    Ren funktion med injicerbar cfg -> golden-testbar utan fil-IO. Beräknar andelen ur råtalen och
    korsverifierar mot den publicerade heltalsandelen (hård fail vid >0,6 pp avvikelse).
    """
    cfg = config.aterfall_i_brott() if cfg is None else cfg
    cat, sub, ind, unit = cfg["category"], cfg["submeasure"], cfg["indicator"], cfg["unit"]
    rows: list[dict[str, Any]] = []
    for year, entry in sorted(cfg["years"].items()):
        klienter = int(entry["klienter"])
        aterfall = int(entry["aterfall"])
        if klienter <= 0 or not (0 <= aterfall <= klienter):
            raise ValueError(f"aterfall_i_brott {year}: orimliga råtal "
                             f"klienter={klienter} aterfall={aterfall}")
        andel = round(aterfall / klienter * 100, 2)
        pub = entry.get("andel_publicerad")
        if pub is not None and abs(andel - float(pub)) > _ANDEL_TOL_PP:
            raise ValueError(
                f"aterfall_i_brott {year}: beräknad andel {andel} avviker >{_ANDEL_TOL_PP} pp "
                f"från publicerad {pub} (transkriptionsfel i täljare/nämnare?)"
            )
        rows.append({
            "id": f"obs:kriminalvarden:{ind}:{year}",
            "category": cat, "submeasure": sub, "indicator": ind, "period": str(year),
            "value": andel, "unit": unit, "geography": "Riket",
            "source_ref": f"kriminalvarden:{ind}:{year}",
        })
    return rows
