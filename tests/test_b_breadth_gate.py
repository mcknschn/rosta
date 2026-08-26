"""B-undermåttsbredd (docs/done/b_coverage_krympning_spec.md §6.4): cov_B-takets grind.

Grinden speglar tests/test_d_breadth_gate.py (allowlist-mönstret): varje kategori vars
viktade cov_B-TAK ligger under grindtröskeln är ANTINGEN åtgärdad (B-väggen byggd bort,
Spår B/B2) ELLER explicit accepterad i coverage_allowlist.b_thin_breadth_accepted med skäl,
och listan kan inte bära inaktuella poster. Mätaren (coverage_report.b_submeasure_breadth)
är offline (endast config): ett icke-target-undermått räknas B-täckbart om det har minst en
kodbar åtgärdstyp — T_s-reglerna och nämnaren DELAS med scoringen (scorerun._b_codable_
types_by_submeasure resp. _non_excluded_submeasures), så grinden mäter exakt det tak som
per-parti-cov_B aldrig kan överstiga. Taket är coverage_mode-oberoende: i legacy-läget är
grinden en ren varningslampa, i weighted_submeasure_depth är det krympningens hårda tak.
Formel-/flagg-/mode-testerna ligger i tests/test_b_coverage_mode.py.
"""

from __future__ import annotations

from pipeline import config, scorerun
from pipeline.tools import coverage_report


def _thin() -> set[str]:
    rep = coverage_report.b_submeasure_breadth()
    return {c["id"] for c in rep["categories"] if c["thin"]}


def _accepted() -> set[str]:
    return {e["category"] for e in (config.coverage_allowlist().get("b_thin_breadth_accepted") or [])}


def test_no_unaccounted_thin_b_breadth() -> None:
    """Varje kategori med cov_B-tak under grindtröskeln måste vara explicit accepterad i
    coverage_allowlist.b_thin_breadth_accepted — annars är det en TYST regression."""
    unaccounted = _thin() - _accepted()
    assert not unaccounted, (
        "Tunt B-breddstak utan motivering — bygg bort B-väggen (Spår B/B2) eller lägg posten i "
        f"coverage_allowlist.b_thin_breadth_accepted med skäl: {sorted(unaccounted)}"
    )


def test_b_thin_allowlist_shrinks() -> None:
    """En accepterad post måste fortfarande VARA under tröskeln. När B-väggen byggs bort
    ska posten tas bort — listan krymper, växer aldrig tyst."""
    stale = _accepted() - _thin()
    assert not stale, (
        "Kategori i b_thin_breadth_accepted är inte längre under grindtröskeln (väggen borta) — "
        f"ta bort posten: {sorted(stale)}"
    )


def test_b_thin_allowlist_valid() -> None:
    cat_ids = set(config.category_ids())
    for e in config.coverage_allowlist().get("b_thin_breadth_accepted") or []:
        assert e["category"] in cat_ids, f"Okänd kategori i b_thin_breadth_accepted: {e}"
        assert e.get("reason", "").strip(), f"Saknar skäl: {e}"


def test_b_breadth_partitions_and_bounds() -> None:
    """Mätaren rapporterar alla 7 kategorier; täckta + otäckta partitionerar den delade
    icke-target-nämnaren och kvoten ligger i [0,1]."""
    rep = coverage_report.b_submeasure_breadth()
    den = scorerun._non_excluded_submeasures()
    assert rep["threshold"] == coverage_report.B_BREADTH_GATE_THRESHOLD
    assert {c["id"] for c in rep["categories"]} == set(config.category_ids())
    for c in rep["categories"]:
        assert set(c["covered_submeasures"]) | set(c["uncovered_submeasures"]) == den[c["id"]]
        assert not set(c["covered_submeasures"]) & set(c["uncovered_submeasures"])
        assert 0.0 <= c["ratio"] <= 1.0
        assert c["covered_weight"] <= c["total_weight"]
        assert c["thin"] == (c["ratio"] < rep["threshold"])
