"""Golden-test för O2 (pipeline.tools.score_diff): snapshot-summering + diff.

Rena funktioner mot syntetiska scores-strukturer — ingen fil-IO, inget dist/.
"""

from __future__ import annotations

from pipeline.tools.score_diff import diff_snapshots, summarize


def _scores(s_score: float = 4.0, s_flags: list[str] | None = None) -> dict[str, object]:
    """Minimal scores.json: 2 kategorier (vikt 60/40), 2 partier."""
    return {
        "categories": [
            {"id": "ekonomi", "standard_weight": 60},
            {"id": "valfard", "standard_weight": 40},
        ],
        "scores": {
            "S": {
                "ekonomi": {"score": s_score, "flags": s_flags or ["A_a1_active"]},
                "valfard": {"score": 3.0, "flags": []},
            },
            "M": {
                "ekonomi": {"score": 2.0, "flags": []},
                "valfard": {"score": 2.0, "flags": []},
            },
        },
    }


def test_summarize_totals_ranking_cells() -> None:
    snap = summarize(_scores())
    # S total = (4.0*60 + 3.0*40)/100 = 3.6 ; M = (2*60+2*40)/100 = 2.0
    assert snap["totals"] == {"S": 3.6, "M": 2.0}
    assert snap["ranking"] == ["S", "M"]
    assert snap["cells"]["S/ekonomi"] == {"score": 4.0, "flags": ["A_a1_active"]}


def test_diff_identiska_ger_inga_andringar() -> None:
    a = summarize(_scores())
    assert diff_snapshots(a, a) == []


def test_diff_fangar_betyg_total_och_ranking() -> None:
    old = summarize(_scores(s_score=4.0))
    new = summarize(_scores(s_score=1.0))  # S ekonomi 4.0 -> 1.0 ; S total 3.6 -> 1.8 (< M:s 2.0)
    changes = "\n".join(diff_snapshots(old, new))
    assert "RANKING" in changes  # S faller under M
    assert "BETYG S/ekonomi" in changes
    assert "TOTAL S" in changes


def test_diff_fangar_flaggandring() -> None:
    old = summarize(_scores(s_flags=["A_a1_active"]))
    new = summarize(_scores(s_flags=["A_a2_only", "B_thin_coverage"]))
    changes = "\n".join(diff_snapshots(old, new))
    assert "FLAGGOR S/ekonomi" in changes
    assert "A_a2_only" in changes  # tillagd
    assert "A_a1_active" in changes  # borttagen


def test_diff_fangar_ny_och_borttagen_cell() -> None:
    old = summarize(_scores())
    new = summarize(_scores())
    del new["cells"]["M/valfard"]
    new["cells"]["X/forsvar"] = {"score": 2.5, "flags": []}
    changes = "\n".join(diff_snapshots(old, new))
    assert "BORTTAGEN CELL M/valfard" in changes
    assert "NY CELL X/forsvar" in changes
