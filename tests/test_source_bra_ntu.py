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


def test_fortroende_rattsvasendet_headline_2017_och_framat() -> None:
    """5A:1: förtroende rättsväsendet som helhet fr.o.m. 2017; det asteriskade 2016* uteslutet."""
    series = bra._ntu_headline_series(_wb()["5A.1"], "Samtliga 16-84 år", None, 2017)
    assert series == {2017: 44.06, 2018: 46.80}
    assert 2016 not in series  # NTU 2017-metodbrott (2016* asteriskmärkt) skärs bort av min_year


def test_rows_kanoniska_indikatorer_med_ratt_kategori() -> None:
    """Radbyggaren ger kanoniska indikatorer med rätt form, kategori och source_ref."""
    rows = bra._ntu_rows_from_workbook(_wb())
    inds = {r["indicator"] for r in rows}
    assert inds == {"brottsutsatthet", "upplevd_otrygghet", "fortroende_domstolar_myndigheter"}
    cat_by_ind = {r["indicator"]: r["category"] for r in rows}
    assert cat_by_ind["brottsutsatthet"] == "trygghet"
    assert cat_by_ind["upplevd_otrygghet"] == "trygghet"
    assert cat_by_ind["fortroende_domstolar_myndigheter"] == "demokrati"  # NTU matar demokrati
    fort = [r for r in rows if r["indicator"] == "fortroende_domstolar_myndigheter"]
    assert all(r["submeasure"] == "korruption_tillit" for r in fort)
    assert all(r["geography"] == "Riket" for r in rows)
    assert all(r["indicator"] in bra.INDICATORS for r in rows)
    by_ref = {r["source_ref"] for r in rows}
    assert "bra:ntu_3a:2016" in by_ref
    assert "bra:ntu_4a1:2017" in by_ref
    assert "bra:ntu_5a1:2017" in by_ref


def test_indicator_category_i_synk_med_categories_yaml() -> None:
    """bra.INDICATOR_CATEGORY (som coverage-gaten läser) pekar på rätt kategori i categories.yaml."""
    by_cat = {
        c["id"]: {i["id"] for i in c.get("indicators", [])}
        for c in config.categories()["categories"]
    }
    for ind, cat in bra.INDICATOR_CATEGORY.items():
        assert ind in by_cat[cat], f"{ind} saknas i categories.yaml under {cat}"
    assert "fortroende_domstolar_myndigheter" in by_cat["demokrati"]
