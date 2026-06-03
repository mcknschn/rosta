"""Golden tests för serie-drift-skyddet (pipeline.expectations, O1).

Två delar:
  1. check_series logik (varje grind + no-op) mot syntetiska rader — helt nätverksfritt.
  2. Invariant på REPO:ts faktiska expect-specar: varje ankare ligger inom sitt value_range,
     value_range är ordnat, min_points ≥ 1. Fångar ett spec-typo (t.ex. ankare utanför bandet)
     utan att behöva köra livehämtning eller ha ett warehouse.
"""

from __future__ import annotations

import pytest

from pipeline import build_fas2
from pipeline.derived import DERIVED
from pipeline.derived import INDICATORS as DERIVED_INDICATORS
from pipeline.expectations import SeriesDriftError, _end_year, check_series
from pipeline.sources import bra, energimyndigheten, polisen


def _rows(pairs: list[tuple[str, float]]) -> list[dict[str, object]]:
    return [{"period": p, "value": v} for p, v in pairs]


_GOOD = _rows([("2018", 10.0), ("2019", 11.0), ("2020", 12.0), ("2021", 13.0)])


def test_valid_series_passes() -> None:
    spec = {"min_points": 3, "value_range": [0, 20], "min_latest_year": 2021,
            "anchors": {"2020": 12.0}}
    check_series(_GOOD, spec, "ok")  # ingen exception


def test_none_and_empty_spec_are_noop() -> None:
    check_series(_GOOD, None, "noop")
    check_series([], {}, "noop")  # tom spec på tom serie -> inget krav


def test_min_points_violation_raises() -> None:
    with pytest.raises(SeriesDriftError, match="min_points"):
        check_series(_GOOD, {"min_points": 10}, "fewpoints")


def test_value_range_violation_raises() -> None:
    with pytest.raises(SeriesDriftError, match="utanför"):
        check_series(_GOOD, {"value_range": [0, 11]}, "outofrange")


def test_min_latest_year_violation_raises() -> None:
    with pytest.raises(SeriesDriftError, match="stale"):
        check_series(_GOOD, {"min_latest_year": 2025}, "stale")


def test_anchor_mismatch_raises() -> None:
    with pytest.raises(SeriesDriftError, match="fel serie"):
        check_series(_GOOD, {"anchors": {"2020": 99.0}}, "wrongseries")


def test_anchor_missing_period_raises() -> None:
    with pytest.raises(SeriesDriftError, match="saknas"):
        check_series(_GOOD, {"anchors": {"1999": 12.0}}, "missingyear")


def test_anchor_within_rel_tol_passes() -> None:
    # 12.3 mot förväntat 12.0 ligger inom default 5 %.
    check_series(_GOOD, {"anchors": {"2020": 12.3}}, "tol")


def test_anchor_zero_expected_uses_absolute_band() -> None:
    rows = _rows([("2020", 0.02), ("2021", 0.03)])
    check_series(rows, {"anchors": {"2020": 0.0}}, "zero")  # |0.02| <= 0.05
    with pytest.raises(SeriesDriftError):
        check_series(_rows([("2020", 0.2)]), {"anchors": {"2020": 0.0}}, "zerobad")


def test_end_year_parses_period_formats() -> None:
    assert _end_year("2024") == 2024
    assert _end_year("2018-2019") == 2019  # äkta flerårsspann -> slutåret
    assert _end_year("2024-2024") == 2024
    assert _end_year("2024M03") == 2024
    assert _end_year("inget") is None


# --- Invariant på repo:ts faktiska specar ---------------------------------------

def _repo_specs() -> list[tuple[str, dict[str, object]]]:
    out: list[tuple[str, dict[str, object]]] = []
    for s in build_fas2.SCB_SERIES:
        out.append((f"SCB {s['table']}", s["expect"]))
    for k in build_fas2.KOLADA_KPIS:
        out.append((f"Kolada {k['kpi']}", k["expect"]))
    for ind, spec in {**bra.EXPECT, **energimyndigheten.EXPECT, **polisen.EXPECT}.items():
        out.append((ind, spec))
    for d in DERIVED:
        out.append((d["indicator"], d["expect"]))
    return out


def _ingested_indicators() -> set[str]:
    """Alla indikatorer som build_fas2/fas3 faktiskt läser in (samma källor som coverage-gaten)."""
    inds = {s["indicator"] for s in build_fas2.SCB_SERIES}
    inds |= {k["indicator"] for k in build_fas2.KOLADA_KPIS}
    inds |= set(bra.INDICATORS) | set(energimyndigheten.INDICATORS) | set(DERIVED_INDICATORS)
    inds |= set(polisen.INDICATORS)
    return inds


def _indicators_with_expect() -> set[str]:
    inds = {s["indicator"] for s in build_fas2.SCB_SERIES if s.get("expect")}
    inds |= {k["indicator"] for k in build_fas2.KOLADA_KPIS if k.get("expect")}
    inds |= set(bra.EXPECT) | set(energimyndigheten.EXPECT) | set(polisen.EXPECT)
    inds |= {d["indicator"] for d in DERIVED if d.get("expect")}
    return inds


def test_every_ingested_series_has_drift_guard() -> None:
    """Robust invariant: varje inläst serie har en drift-förväntan (auto-skalar med nya serier)."""
    missing = _ingested_indicators() - _indicators_with_expect()
    assert not missing, f"inlästa serier utan serie-drift-förväntan (lägg till 'expect'): {sorted(missing)}"


def test_repo_specs_internally_consistent() -> None:
    """Varje deklarerad expect-spec är intern­konsistent (ankare inom band, band ordnat)."""
    specs = _repo_specs()
    for label, spec in specs:
        vr = spec.get("value_range")
        if vr is not None:
            assert vr[0] < vr[1], f"{label}: value_range ej ordnat: {vr}"
        mp = spec.get("min_points")
        if mp is not None:
            assert mp >= 1, f"{label}: min_points måste vara ≥ 1"
        for period, val in (spec.get("anchors") or {}).items():
            if vr is not None:
                assert vr[0] <= val <= vr[1], f"{label}: ankare {period}={val} utanför {vr}"


def test_repo_specs_pass_their_own_anchors() -> None:
    """En syntetisk serie byggd ur en specs ankare passerar samma spec (ingen självmotsägelse)."""
    for label, spec in _repo_specs():
        anchors = spec.get("anchors") or {}
        if not anchors:
            continue
        rows = _rows([(p, float(v)) for p, v in anchors.items()])
        # Bara ankar-grinden ska köras isolerat (min_points/latest_year kräver full serie).
        check_series(rows, {"anchors": anchors, "rel_tol": spec.get("rel_tol", 0.05)}, label)
