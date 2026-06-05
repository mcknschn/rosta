"""Fas 4b' — B-täckningsgate (anti-binär garanti, BACKLOG B4).

Mäter submåttsspridningen i partikopplad B-evidens per kategori (pipeline.tools.
coverage_report.b_submeasure_spread) och vaktar mot att en kategoris B vilar på <=1 submått.
Eftersom score.aggregate_B är submåttsviktat kan en kategori med all aktiv evidens i ETT submått
få sin B-poäng svingad mellan ytterlägen (0/2.5/5) av en enda ståndpunkt — "nära-binär".

Grinden speglar coverage_allowlist-mönstret (test_fas3_gate): varje nära-binär kategori är
ANTINGEN åtgärdad ELLER explicit accepterad i coverage_allowlist.b_near_binary_accepted med skäl,
och listan kan inte bära inaktuella poster. Kör offline (bara config, ingen warehouse).
"""

from __future__ import annotations

from pipeline import config
from pipeline.tools import coverage_report


def _near_binary() -> set[str]:
    rep = coverage_report.b_submeasure_spread()
    return {c["id"] for c in rep["categories"] if c["near_binary"]}


def _accepted() -> set[str]:
    return {e["category"] for e in (config.coverage_allowlist().get("b_near_binary_accepted") or [])}


def test_no_unaccounted_near_binary_category() -> None:
    """Varje nära-binär kategori (<=1 submått med aktiv B-evidens) måste vara explicit accepterad
    i coverage_allowlist.b_near_binary_accepted — annars är det en TYST regression."""
    unaccounted = _near_binary() - _accepted()
    assert not unaccounted, (
        "Nära-binär kategori utan motivering — bredda evidensliggaren (BACKLOG B2) eller "
        f"lägg posten i coverage_allowlist.b_near_binary_accepted med skäl: {sorted(unaccounted)}"
    )


def test_b_near_binary_allowlist_shrinks() -> None:
    """En accepterad post måste fortfarande VARA nära-binär. När B2 breddar en kategori upphör
    den att vara nära-binär och posten ska tas bort — så allowlisten krymper, aldrig växer tyst."""
    stale = _accepted() - _near_binary()
    assert not stale, (
        "Kategori i b_near_binary_accepted är inte längre nära-binär (luckan löst) — ta bort "
        f"posten: {sorted(stale)}"
    )


def test_b_near_binary_allowlist_valid() -> None:
    """Varje post pekar på en kanonisk kategori och har ett icke-tomt skäl."""
    cat_ids = set(config.category_ids())
    for e in config.coverage_allowlist().get("b_near_binary_accepted") or []:
        assert e["category"] in cat_ids, f"Okänd kategori i b_near_binary_accepted: {e}"
        assert e.get("reason", "").strip(), f"Saknar skäl: {e}"


def test_spread_covers_all_categories_and_is_consistent() -> None:
    """Mätaren rapporterar alla 7 kategorier, och täckta + otäckta submått partitionerar helheten."""
    rep = coverage_report.b_submeasure_spread()
    reported = {c["id"] for c in rep["categories"]}
    assert reported == set(config.category_ids())
    for c in rep["categories"]:
        assert c["submeasures_with_evidence"] == len(c["covered_submeasures"])
        assert len(c["covered_submeasures"]) + len(c["uncovered_submeasures"]) == c["submeasures_total"]
        assert c["near_binary"] == (c["submeasures_with_evidence"] <= 1)
