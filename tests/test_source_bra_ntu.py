"""Offline-test för Brå NTU-adaptern (xlsx-tabellsamling -> utsatthet/otrygghet-serier).

Facit mot en beskuren NTU-fixtur (verkliga värden ur Tabellsamling NTU 2007-2025, blad 3A
och 4A:1). Ingen nätverkstrafik — parsern och radbyggaren testas direkt mot fixturen.
Verifierar: års-header med asterisk, exkluderade CI-kolumner, min_year-skärning vid
metodbrytet, en-dash-normalisering i radetiketten, och hård fail när raden saknas.
"""

from __future__ import annotations

from pathlib import Path

import openpyxl
import pytest

from pipeline import config
from pipeline.sources import bra

FIXTURE = Path(__file__).parent / "fixtures" / "bra_ntu_sample.xlsx"


def _wb() -> object:
    return openpyxl.load_workbook(FIXTURE, data_only=True)


def test_brottsutsatthet_headline_2016_och_framat() -> None:
    """3A: 'Brott mot enskild person/Samtliga' fr.o.m. 2016; '..' och CI-kolumner uteslutna."""
    series = bra._ntu_headline_series(_wb()["3A"], "Brott mot enskild person", "Samtliga", 2016)
    assert series == {2016: 20.76, 2017: 22.44, 2018: 23.07}


def test_otrygghet_exkluderar_asteriskade_metodar_och_ci() -> None:
    """4A:1: nuvarande metod fr.o.m. 2017; det omräknade 2016* och CI-kolumner uteslutna.

    Radetiketten i källan har en-dash ('Samtliga 16–84 år') — locatorn matchar via dash-norm."""
    series = bra._ntu_headline_series(_wb()["4A.1"], "Samtliga 16-84 år", None, 2017)
    assert series == {2017: 27.72, 2018: 27.89}
    assert 2016 not in series  # det asteriskade gamla-metoden-året skärs bort av min_year


def test_radlocator_valjer_inte_undergrupp_eller_brottstyp() -> None:
    """Decoy-rader (undergrupp 'Män', brottstypen 'Misshandel') får inte plockas som headline."""
    series = bra._ntu_headline_series(_wb()["3A"], "Brott mot enskild person", "Samtliga", 2016)
    # Misshandel-raden ligger ~3 %; headline brott mot enskild person ~20 % -> rätt rad vald.
    assert min(series.values()) > 10


def test_saknad_rad_ger_hard_fail() -> None:
    """En etikett som inte finns ska faila högt (aldrig tyst tom serie / fel rad)."""
    with pytest.raises(ValueError, match="exakt 1 rad"):
        bra._ntu_headline_series(_wb()["3A"], "Obefintlig kategori", None, 2016)


def test_for_fa_arsvarden_ger_hard_fail() -> None:
    """Om en serie ger <2 numeriska årsvärden (struktur ändrad) ska parsern faila högt."""
    with pytest.raises(ValueError, match="<2 numeriska"):
        bra._ntu_headline_series(_wb()["4A.1"], "Samtliga 16-84 år", None, 2099)


def test_rows_kanoniska_indikatorer_i_trygghet() -> None:
    """Radbyggaren ger kanoniska trygghet-indikatorer med rätt form och source_ref."""
    rows = bra._ntu_rows_from_workbook(_wb())
    inds = {r["indicator"] for r in rows}
    assert inds == {"brottsutsatthet", "upplevd_otrygghet"}
    assert all(r["category"] == "trygghet" for r in rows)
    assert all(r["submeasure"] == "utsatthet_trygghet" for r in rows)
    assert all(r["geography"] == "Riket" for r in rows)
    assert all(r["indicator"] in bra.INDICATORS for r in rows)
    by_ind = {r["source_ref"] for r in rows}
    assert "bra:ntu_3a:2016" in by_ind
    assert "bra:ntu_4a1:2017" in by_ind


def test_ntu_indikatorer_ar_kanoniska_trygghetsindikatorer() -> None:
    """INDICATORS pekar bara på indikatorer som finns i categories.yaml under trygghet."""
    trygghet = next(c for c in config.categories()["categories"] if c["id"] == "trygghet")
    inds = {i["id"] for i in trygghet["indicators"]}
    assert {"brottsutsatthet", "upplevd_otrygghet"} <= inds
