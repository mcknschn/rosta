"""Offline-test för Domstolsverket-adaptern (DOMstat PxWeb v1, json-stat2 -> årsserie).

Facit mot den verkliga (beskurna) 01_Verksamhetsmal_TR-fixturen: handläggningstid vid
tingsrätt, 75-percentil i månader, brottmål exkl. förtursmål, alla tingsrätter.
Ingen nätverkstrafik — parsern och observations-byggaren testas direkt mot fixturen.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from pipeline.sources import domstolsverket as dv

FIXTURE = Path(__file__).parent / "fixtures" / "domstolsverket_01_verksamhetsmal_tr.json"


def _fixture() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_annual_series_ger_publicerade_75_percentiler() -> None:
    """Serien pinnas mot publicerade värden (2007: 5.3, 2023: 3.5, 2024: 3.1 månader)."""
    series = dv.annual_series(_fixture())
    assert series == {
        "2007": pytest.approx(5.3),
        "2023": pytest.approx(3.5),
        "2024": pytest.approx(3.1),
    }


def test_periods_ar_artal_inte_pxweb_koder() -> None:
    """Tidsnycklarna ska vara årtal (labels), inte interna PxWeb-index ('0','16','17')."""
    series = dv.annual_series(_fixture())
    assert set(series) == {"2007", "2023", "2024"}


def test_icke_eliminerad_extra_dimension_ger_hard_fail() -> None:
    """Om en icke-tidsdimension inte är fixerad (storlek 1) ska parsern faila högt —
    annars skulle pos=0 tyst plocka en delserie (fel domstol/fel målkategori)."""
    j = _fixture()
    j["size"] = [1, 49, 1, 3]  # Domstol låtsas ofiltrerad (alla 49 tingsrätter)
    with pytest.raises(ValueError, match="icke-eliminerad"):
        dv.annual_series(j)


def test_build_observations_radform_och_id_monster() -> None:
    """Observations-raderna bär kanonisk kategori/submått/indikator + id-/source_ref-mönster."""
    rows = dv.build_observations(dv.annual_series(_fixture()))
    assert [r["period"] for r in rows] == ["2007", "2023", "2024"]
    r = rows[-1]
    assert r["id"] == "obs:domstolsverket:handlaggningstid:2024"
    assert r["category"] == "trygghet"
    assert r["submeasure"] == "rattsvasendets_effektivitet"
    assert r["indicator"] == "handlaggningstid"
    assert r["value"] == pytest.approx(3.1)
    assert r["unit"] == "månader"
    assert r["geography"] == "Riket"
    assert r["source_ref"] == "domstolsverket:01_Verksamhetsmal_TR:2024"


def test_handlaggningstid_finns_i_modellens_trygghetskategori() -> None:
    """INDICATORS pekar på en kanonisk trygghetsindikator med riktning down (annars faller gaten)."""
    from pipeline import config

    trygghet = next(c for c in config.categories()["categories"] if c["id"] == "trygghet")
    inds = {i["id"]: i for i in trygghet["indicators"]}
    assert set(dv.INDICATORS) <= set(inds)
    assert inds["handlaggningstid"]["direction"] == "down"
    assert inds["handlaggningstid"]["submeasure"] == "rattsvasendets_effektivitet"
