"""Fas 1-tester (deterministiska, utan nätverk)."""

from __future__ import annotations

from pipeline import build_fas2, config, schema, warehouse
from pipeline.sources import government, riksdagen


def test_national_responsibility_valid_and_complete() -> None:
    rows = government.build_national_responsibility()
    assert rows
    for r in rows:
        schema.validate("responsibility", r)  # höjer vid fel
    pr = {(r["party"], r["role"]) for r in rows}
    # Kristersson-regeringen + stödparti
    assert {("M", "government"), ("KD", "government"), ("L", "government")} <= pr
    assert ("SD", "support") in pr
    # S har regeringsansvar i flera perioder (Löfven I/II, Andersson)
    s_gov = [r for r in rows if r["party"] == "S" and r["role"] == "government"]
    assert len(s_gov) >= 3
    # ids är unika
    ids = [r["id"] for r in rows]
    assert len(ids) == len(set(ids))


def test_committee_map_targets_valid_categories() -> None:
    cats = set(config.category_ids())
    cmap = config.mappings()["committee_to_category"]
    assert cmap
    for org, cat in cmap.items():
        assert cat in cats, f"{org} -> {cat}"


def test_committee_from_beteckning() -> None:
    assert riksdagen.committee_from_beteckning("AU10") == "AU"
    assert riksdagen.committee_from_beteckning("FiU1") == "FIU"
    assert riksdagen.committee_from_beteckning("") == ""


def test_warehouse_roundtrip_is_idempotent() -> None:
    con = warehouse.connect(":memory:")
    rows = government.build_national_responsibility()
    n = warehouse.upsert(con, "responsibility", rows)
    assert warehouse.count(con, "responsibility") == n
    warehouse.upsert(con, "responsibility", rows)  # samma id:n -> ingen tillväxt
    assert warehouse.count(con, "responsibility") == n
    warehouse.upsert(con, "party_activity", [{
        "party": "S", "category": "ekonomi", "committee": "FiU",
        "kind": "motion", "period": "x", "count": 5, "source_ref": "u",
    }], validate=False)
    assert warehouse.count(con, "party_activity") == 1
    con.close()


def test_purge_unmanaged_spares_foreign_source_rows() -> None:
    # Regression (review): purge får bara röra SCB/Kolada-rader, inte andra modulers data.
    con = warehouse.connect(":memory:")
    managed_ind = next(iter(build_fas2.SCB_SERIES))["indicator"]
    warehouse.upsert(con, "observations", [
        # En egen (scb) rad med en EJ hanterad indikator -> ska rensas.
        {"id": "obs:scb:gammal:2020", "category": "ekonomi", "indicator": "gammal_borttagen",
         "period": "2020", "value": 1.0, "geography": "Riket", "source_ref": "scb:TABX:2020"},
        # En Brå-rad (annan modul) -> ska ÖVERLEVA även om indikatorn inte är hanterad här.
        {"id": "obs:bra:dodligt_vald:2020", "category": "trygghet", "indicator": "dodligt_vald",
         "period": "2020", "value": 1.0, "geography": "Riket", "source_ref": "bra:ntu:2020"},
        # En hanterad scb-rad -> ska behållas.
        {"id": "obs:scb:keep:2020", "category": "ekonomi", "indicator": managed_ind,
         "period": "2020", "value": 1.0, "geography": "Riket", "source_ref": "scb:TABY:2020"},
    ])
    removed = build_fas2._purge_unmanaged(con)
    assert removed == 1  # bara den egna ej-hanterade scb-raden
    surviving = {r[0] for r in con.execute("SELECT id FROM observations").fetchall()}
    assert surviving == {"obs:bra:dodligt_vald:2020", "obs:scb:keep:2020"}
    con.close()
