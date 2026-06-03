"""Offline-test för Brå:s personuppklaring-adapter (Handlagda brott 10La).

Facit mot en beskuren fixtur (riktiga 10La-värden, blad 'Statistik personuppklaringsproc').
Ingen nätverkstrafik. Verifierar: rätt headline-rad (SAMTLIGA BROTT, ej en brottstyp-decoy),
kanonisk radform, och att uppklaringsgrad är en kanonisk trygghetsindikator med riktning up.
"""

from __future__ import annotations

from pathlib import Path

import openpyxl

from pipeline import config
from pipeline.sources import bra

FIXTURE = Path(__file__).parent / "fixtures" / "bra_personuppklaring_sample.xlsx"


def _wb() -> object:
    return openpyxl.load_workbook(FIXTURE, data_only=True)


def test_personuppklaring_headline_serie() -> None:
    """Headline-raden SAMTLIGA BROTT -> personuppklaringsprocent per år (avrundat 2 dec)."""
    rows = bra._personuppklaring_rows_from_workbook(_wb())
    by_year = {r["period"]: r["value"] for r in rows}
    assert by_year == {"2016": 13.23, "2017": 13.34, "2018": 13.56, "2019": 13.52, "2020": 13.87}


def test_valjer_inte_brottstyp_decoy() -> None:
    """En specifik brottstyp (~8 %) får inte plockas i stället för headline (~13 %)."""
    rows = bra._personuppklaring_rows_from_workbook(_wb())
    assert min(r["value"] for r in rows) > 10


def test_radform_kanonisk() -> None:
    r = bra._personuppklaring_rows_from_workbook(_wb())[0]
    assert r["indicator"] == "uppklaringsgrad"
    assert r["category"] == "trygghet"
    assert r["submeasure"] == "rattsvasendets_effektivitet"
    assert r["unit"] == "% (personuppklaringsprocent, samtliga brott)"
    assert r["geography"] == "Riket"
    assert r["id"] == "obs:bra:uppklaringsgrad:2016"
    assert r["source_ref"] == "bra:personuppklaring_10la:2016"
    assert "uppklaringsgrad" in bra.INDICATORS


def test_uppklaringsgrad_kanonisk_trygghetsindikator_riktning_up() -> None:
    """INDICATORS-posten pekar på en categories.yaml-indikator med riktning up (högre = bättre)."""
    trygghet = next(c for c in config.categories()["categories"] if c["id"] == "trygghet")
    ind = next(i for i in trygghet["indicators"] if i["id"] == "uppklaringsgrad")
    assert ind["direction"] == "up"
    assert ind["submeasure"] == "rattsvasendets_effektivitet"
