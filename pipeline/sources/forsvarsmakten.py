"""Försvarsmakten — antal värnpliktiga som påbörjade grundutbildning (delpoäng D, kategori forsvar).

Försvarets FÖRSTA D-serie (kategorin var tidigare strukturellt D-tom). Försvarsmaktens
årsredovisning för officiell statistik över hur många värnpliktiga som påbörjade grundutbildning
per kalenderår, men publicerar den ENDAST som FlateDecode-komprimerad PDF (ingen maskinläsbar
tabell, och verktygskedjan kan ej rendera PDF:erna). Årstotalerna är därför troget transkriberade
till config/personal_varnpliktiga.yaml — samma mönster som budget_ramar/skjutningar_sprangningar,
ingen runtime-PDF-parser som kan korrumpera D tyst.

KORSVERIFIERING: varje år stäms av mot Plikt- och prövningsverkets oberoende "inskrivna till
grundutbildning med värnplikt" (annat myndighetsmått, läst direkt ur Pliktverkets pressmeddelanden).
Båda myndigheterna ligger nära varann och visar samma enda nedgång 2021->2022. Reproducerbart via
tools/varnpliktiga_audit.py. Den här modulen läser bara config -> observations (nätverksfri).
"""

from __future__ import annotations

from typing import Any

from .. import config

# Kanoniska indikatorer denna modul levererar (för täcknings-gaten i tests/test_fas3_gate.py).
INDICATORS = ("personal_varnpliktiga", "personalstyrka_kontinuerligt")

# Serie-drift-förväntan (pipeline.expectations). Ankare = stabila publicerade värden (±rel_tol).
EXPECT = {
    # Antal som påbörjade GU per kalenderår 2018-2025 (riktning up).
    "personal_varnpliktiga": {"min_points": 7, "value_range": [3000, 12000],
                              "min_latest_year": 2024, "anchors": {"2018": 3750, "2021": 5873}},
    # Summa kontinuerligt tjänstgörande per 31 dec 2019-2024 (riktning up; FM ÅR bilaga Tabell 1).
    "personalstyrka_kontinuerligt": {"min_points": 5, "value_range": [18000, 35000],
                                     "min_latest_year": 2024, "anchors": {"2019": 22751, "2024": 27734}},
}


def _build_from_config(cfg: dict[str, Any]) -> list[dict[str, Any]]:
    """Transkriberade årsvärden -> observations-rader (Riket). Ren funktion (golden-testbar)."""
    cat, sub, ind, unit = cfg["category"], cfg["submeasure"], cfg["indicator"], cfg["unit"]
    return [
        {
            "id": f"obs:forsvarsmakten:{ind}:{year}",
            "category": cat, "submeasure": sub, "indicator": ind, "period": str(year),
            "value": float(entry["value"]), "unit": unit, "geography": "Riket",
            "source_ref": f"forsvarsmakten:{ind}:{year}",
        }
        for year, entry in sorted(cfg["years"].items())
    ]


def build_personal_varnpliktiga_observations(
    cfg: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Antal påbörjade GU per kalenderår -> observations (militar_formaga)."""
    return _build_from_config(config.personal_varnpliktiga() if cfg is None else cfg)


def build_personalstyrka_observations(
    cfg: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Summa kontinuerligt tjänstgörande per 31 dec -> observations (militar_formaga)."""
    return _build_from_config(config.personalstyrka_forsvarsmakten() if cfg is None else cfg)


def build_all_observations() -> list[dict[str, Any]]:
    """Alla FM-transkriberade serier (för build_fas3:s full-replace av 'forsvarsmakten:%')."""
    return build_personal_varnpliktiga_observations() + build_personalstyrka_observations()
