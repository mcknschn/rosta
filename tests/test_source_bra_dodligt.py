"""Offline-regressionstest för Brå:s dödligt-våld-adapter (Tabell 20, blad 'Statistik').

Skyddar parsern mot tysta regressioner: rätt kolumn (per 100 000, inte antal), år-i-rader,
och att SOS:s saknad-data-markör '.' hoppas i stället för att krascha (float('.')).
"""

from __future__ import annotations

from pathlib import Path

import openpyxl

from pipeline.sources import bra

FIXTURE = Path(__file__).parent / "fixtures" / "bra_dodligt_vald_sample.xlsx"


def _wb() -> object:
    return openpyxl.load_workbook(FIXTURE, data_only=True)


def test_dodligt_vald_parser_per_100k_och_hoppar_saknad_data() -> None:
    rows = bra._dodligt_rows_from_workbook(_wb())
    by_year = {r["period"]: r["value"] for r in rows}
    # 2024 har '.' (saknad data) -> ska hoppas; övriga tar per-100 000-kolumnen, inte antalet.
    assert by_year == {"2002": 1.05, "2003": 1.21, "2025": 0.87}
    assert "2024" not in by_year


def test_dodligt_vald_radform_kanonisk() -> None:
    r = bra._dodligt_rows_from_workbook(_wb())[0]
    assert r["indicator"] == "dodligt_vald"
    assert r["category"] == "trygghet"
    assert r["submeasure"] == "grov_brottslighet"
    assert r["unit"] == "per 100 000 inv."
    assert r["geography"] == "Riket"
    assert r["id"] == "obs:bra:dodligt_vald:2002"
    assert r["source_ref"] == "bra:dodligt_vald_tabell20:2002"
    assert "dodligt_vald" in bra.INDICATORS
