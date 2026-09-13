"""B-undermåttsbredd (docs/done/b_coverage_krympning_spec.md §6.4): registret över tomma undermått.

Grinden speglar tests/test_d_breadth_gate.py (allowlist-mönstret): varje kategori med minst ett
TOMT undermått är ANTINGEN åtgärdad (B-väggen byggd bort, Spår B/B2) ELLER explicit accepterad i
coverage_allowlist.b_thin_breadth_accepted med skäl, och listan kan inte bära inaktuella poster.
Mätaren (coverage_report.b_submeasure_breadth) är offline (endast config): ett icke-uteslutet
undermått räknas B-täckbart om det har minst en kodbar åtgärdstyp. T_s-reglerna och nämnaren
DELAS med scoringen (scorerun._b_covered_submeasures resp. _non_excluded_submeasures), så grinden
mäter exakt de väggar som sänker det tak per-parti-cov_B aldrig kan överstiga.

TRÖSKELN UTGICK 2026-09-13 (ADR 0014 punkt 9). Villkoret var "tak under 0,75", och det dolde
ekonomi och trygghet: båda bär ett tomt undermått men låg över talet. En redovisad storhet får
inte ha en tröskel (ADR 0003 punkt 3, ADR 0008 punkt 6), och ett fast tal ruttnar dessutom tyst
den dag en vägg byggs bort. Talen bor numera i pipen och skältexterna bär bara orsaken.

Formel-/flagg-/mode-testerna ligger i tests/test_b_coverage_mode.py, Mättaket i tests/test_mattak.py.
"""

from __future__ import annotations

from pipeline import config, scorerun
from pipeline.tools import coverage_report


def _med_tomt_undermatt() -> set[str]:
    rep = coverage_report.b_submeasure_breadth()
    return {c["id"] for c in rep["categories"] if c["uncovered_submeasures"]}


def _accepted() -> set[str]:
    return {e["category"] for e in (config.coverage_allowlist().get("b_thin_breadth_accepted") or [])}


def test_no_unaccounted_empty_b_submeasure() -> None:
    """Varje kategori med ett tomt undermått måste vara explicit accepterad i
    coverage_allowlist.b_thin_breadth_accepted — annars är det en TYST regression."""
    unaccounted = _med_tomt_undermatt() - _accepted()
    assert not unaccounted, (
        "Tomt B-undermått utan motivering. Bygg bort B-väggen (Spår B/B2) eller lägg posten i "
        f"coverage_allowlist.b_thin_breadth_accepted med skäl: {sorted(unaccounted)}"
    )


def test_b_thin_allowlist_shrinks() -> None:
    """En accepterad post måste fortfarande HA ett tomt undermått. När B-väggen byggs bort
    ska posten tas bort — listan krymper, växer aldrig tyst."""
    stale = _accepted() - _med_tomt_undermatt()
    assert not stale, (
        "Kategori i b_thin_breadth_accepted har inga tomma undermått kvar (väggen borta), "
        f"ta bort posten: {sorted(stale)}"
    )


def test_b_thin_allowlist_valid() -> None:
    cat_ids = set(config.category_ids())
    for e in config.coverage_allowlist().get("b_thin_breadth_accepted") or []:
        assert e["category"] in cat_ids, f"Okänd kategori i b_thin_breadth_accepted: {e}"
        assert e.get("reason", "").strip(), f"Saknar skäl: {e}"


def test_registret_bar_skalet_och_aldrig_talet() -> None:
    """ADR 0014 punkt 9: pipen äger talet, registret äger skälet.

    Två kopior av ett tal bör ha en källa och inte två. Den andra kopian hade redan kostat:
    två av skältexterna bar undermåttsvikter som inte stämde mot configen. Ett skäl får
    namnge undermåtten och källorna, men aldrig bära tak eller vikter.
    """
    vikter = {
        str(int(w)) for vikt in scorerun._submeasure_weights().values() for w in vikt.values()
    }
    for e in config.coverage_allowlist().get("b_thin_breadth_accepted") or []:
        reason = e["reason"]
        assert "cov_B-tak" not in reason, f"{e['category']}: taket står i skälet"
        for vikt in vikter:
            assert f"({vikt})" not in reason, (
                f"{e['category']}: undermåttsvikten {vikt} står i skälet, pipen äger talet"
            )


def test_b_breadth_partitions_and_bounds() -> None:
    """Mätaren rapporterar alla 7 kategorier; täckta + otäckta partitionerar den delade
    icke-uteslutna nämnaren och kvoten ligger i [0,1]."""
    rep = coverage_report.b_submeasure_breadth()
    den = scorerun._non_excluded_submeasures()
    assert "threshold" not in rep, "B-breddsgrinden har fått en tröskel igen (ADR 0014 punkt 9)"
    assert {c["id"] for c in rep["categories"]} == set(config.category_ids())
    for c in rep["categories"]:
        assert set(c["covered_submeasures"]) | set(c["uncovered_submeasures"]) == den[c["id"]]
        assert not set(c["covered_submeasures"]) & set(c["uncovered_submeasures"])
        assert 0.0 <= c["ratio"] <= 1.0
        assert c["covered_weight"] <= c["total_weight"]
