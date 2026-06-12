"""Offline-test för Medlingsinstitutet-adaptern (MI:s PxWeb v1, json-stat2 -> årsserie).

Facit mot den verkliga (beskurna) Realloner_arsdata-fixturen: reala löner i hela ekonomin,
Reallön (KPI) som Index(1995=100). Ingen nätverkstrafik — parsern och observations-byggaren
testas direkt mot fixturen.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from pipeline.sources import medlingsinstitutet as mi

FIXTURE = Path(__file__).parent / "fixtures" / "medlingsinstitutet_realloner_arsdata.json"


def _fixture() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_annual_series_ger_publicerade_indexvarden() -> None:
    """Serien pinnas mot publicerade värden (1960: 59.3, basåret 1995: 100, 2024: 155.5, 2025: 160.1)."""
    series = mi.annual_series(_fixture())
    assert series == {
        "1960": pytest.approx(59.3),
        "1995": pytest.approx(100.0),
        "2024": pytest.approx(155.5),
        "2025": pytest.approx(160.1),
    }


def test_periods_ar_artal_inte_pxweb_koder() -> None:
    """Tidsnycklarna ska vara årtal (labels), inte interna PxWeb-index ('0','35','64','65')."""
    series = mi.annual_series(_fixture())
    assert set(series) == {"1960", "1995", "2024", "2025"}


def test_icke_eliminerad_extra_dimension_ger_hard_fail() -> None:
    """Om en icke-tidsdimension inte är fixerad (storlek 1) ska parsern faila högt —
    annars skulle pos=0 tyst plocka en delserie (fel variabel, eller %-serien i stället
    för indexserien)."""
    j = _fixture()
    j["size"] = [5, 1, 4]  # Variabel låtsas ofiltrerad (alla 5: nominell, KPI, KPIF, reallön x2)
    with pytest.raises(ValueError, match="icke-eliminerad"):
        mi.annual_series(j)


def test_build_observations_radform_och_id_monster() -> None:
    """Observations-raderna bär kanonisk kategori/submått/indikator + id-/source_ref-mönster."""
    rows = mi.build_observations(mi.annual_series(_fixture()))
    assert [r["period"] for r in rows] == ["1960", "1995", "2024", "2025"]
    r = rows[2]
    assert r["id"] == "obs:medlingsinstitutet:realloner:2024"
    assert r["category"] == "ekonomi"
    assert r["submeasure"] == "realloner_hushall"
    assert r["indicator"] == "realloner"
    assert r["value"] == pytest.approx(155.5)
    assert r["unit"] == "index (1995=100)"
    assert r["geography"] == "Riket"
    assert r["source_ref"] == "medlingsinstitutet:Realloner_arsdata:2024"


def test_realloner_finns_i_modellens_ekonomikategori() -> None:
    """INDICATORS pekar på en kanonisk ekonomiindikator med riktning up (annars faller gaten)."""
    from pipeline import config

    ekonomi = next(c for c in config.categories()["categories"] if c["id"] == "ekonomi")
    inds = {i["id"]: i for i in ekonomi["indicators"]}
    assert set(mi.INDICATORS) <= set(inds)
    assert inds["realloner"]["direction"] == "up"
    assert inds["realloner"]["submeasure"] == "realloner_hushall"
