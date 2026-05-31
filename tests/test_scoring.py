"""Golden tests för den deterministiska betygsmatten."""

from __future__ import annotations

import pytest

from pipeline import score

WEIGHTS = {"A": 0.40, "B": 0.35, "C": 0.15, "D": 0.10}


def test_weighted_category_score_uniform() -> None:
    assert score.weighted_category_score({"A": 4, "B": 4, "C": 4, "D": 4}, WEIGHTS) == pytest.approx(4.0)


def test_weighted_category_score_only_a() -> None:
    assert score.weighted_category_score({"A": 5, "B": 0, "C": 0, "D": 0}, WEIGHTS) == pytest.approx(2.0)


def test_weighted_category_score_missing_component() -> None:
    with pytest.raises(ValueError):
        score.weighted_category_score({"A": 5, "B": 0, "C": 0}, WEIGHTS)


def test_weighted_category_score_missing_weight_raises_valueerror() -> None:
    # Tidigare läckte detta ett bart KeyError; nu en tydlig ValueError.
    with pytest.raises(ValueError):
        score.weighted_category_score({"A": 5, "B": 0, "C": 0, "D": 0}, {"A": 1, "B": 0, "C": 0})


def test_minmax_normalize_spreads_to_full_scale() -> None:
    out = score.minmax_normalize({"S": 10, "M": 20, "V": 30})
    assert out["S"] == pytest.approx(0.0)
    assert out["M"] == pytest.approx(2.5)
    assert out["V"] == pytest.approx(5.0)


def test_minmax_normalize_zero_spread_is_neutral() -> None:
    assert score.minmax_normalize({"S": 3, "M": 3}, neutral=2.5) == {"S": 2.5, "M": 2.5}


def test_rank_normalize_orders_and_handles_ties() -> None:
    out = score.rank_normalize({"S": 100, "M": 1, "V": 50, "C": 1})
    # M och C delar lägsta värdet (medelrang) -> samma poäng, lägst
    assert out["M"] == out["C"] < out["V"] < out["S"]
    assert out["S"] == pytest.approx(5.0)
    # outlier (S=100) komprimerar inte de övriga som minmax skulle
    assert out["V"] == pytest.approx(5.0 * 2 / 3)


def test_rank_normalize_zero_spread_is_neutral() -> None:
    assert score.rank_normalize({"S": 7, "M": 7, "V": 7}) == {"S": 2.5, "M": 2.5, "V": 2.5}


def test_net_support_endpoints() -> None:
    assert score.net_support_to_score(-1) == pytest.approx(0.0)
    assert score.net_support_to_score(0) == pytest.approx(2.5)
    assert score.net_support_to_score(1) == pytest.approx(5.0)


def test_aggregate_b_submeasure_weighted() -> None:
    # net_support 1.0 -> 5, -1.0 -> 0; viktat (5*30 + 0*10)/40 = 3.75
    out = score.aggregate_B({"i1": 1.0, "i2": -1.0}, {"i1": 30, "i2": 10})
    assert out == pytest.approx(3.75)


def test_aggregate_b_missing_indicator_skipped() -> None:
    out = score.aggregate_B({"i1": 1.0, "i2": None}, {"i1": 30, "i2": 10})
    assert out == pytest.approx(5.0)  # endast i1 räknas


def test_aggregate_b_all_missing_is_neutral() -> None:
    assert score.aggregate_B({"i1": None}, {"i1": 30}, missing_all_score=2.5) == pytest.approx(2.5)


def test_submeasure_weighted_mean_skips_none() -> None:
    assert score.submeasure_weighted_mean({"a": 1.0, "b": None}, {"a": 30, "b": 10}) == pytest.approx(1.0)
    assert score.submeasure_weighted_mean({"a": None}, {"a": 30}) is None
    # (1.0*30 + -1.0*10)/40 = 0.5
    assert score.submeasure_weighted_mean({"a": 1.0, "b": -1.0}, {"a": 30, "b": 10}) == pytest.approx(0.5)


# --- D-attribution -------------------------------------------------------------

def test_period_to_year_handles_formats() -> None:
    assert score.period_to_year("2024") == 2024
    assert score.period_to_year("2021-2021") == 2021    # enkelårs-etikett -> det året
    assert score.period_to_year("2018-2019") is None    # äkta dubbelår -> inget enskilt år
    assert score.period_to_year("2024M03") is None      # månad -> ingen årsupplösning
    assert score.period_to_year("2024K1") is None       # kvartal
    assert score.period_to_year("skräp") is None


def test_direction_adjusted_change_respects_direction() -> None:
    assert score.direction_adjusted_change(100, 110, "up") == pytest.approx(0.1)
    assert score.direction_adjusted_change(100, 90, "down") == pytest.approx(0.1)    # förbättring
    assert score.direction_adjusted_change(100, 110, "down") == pytest.approx(-0.1)  # försämring
    assert score.direction_adjusted_change(100, 110, "target") is None              # ingen målnivå
    assert score.direction_adjusted_change(0, 5, "up") is None                       # v_prev=0


def test_change_sign_dead_zone() -> None:
    assert score.change_sign(0.02, 0.005) == 1
    assert score.change_sign(-0.02, 0.005) == -1
    assert score.change_sign(0.003, 0.005) == 0   # inom dödzon -> oförändrat


def test_attribute_series_weights_by_power_and_sign() -> None:
    series = {2020: 100.0, 2021: 110.0, 2022: 99.0}
    yp = {2020: {"A": 1.0}, 2021: {"A": 1.0}}
    # 2020->2021 förbättring (+1, vikt yp[2020]); 2021->2022 försämring (-1, vikt yp[2021])
    net, basis = score.attribute_series(series, "up", yp, "A", lag=1, dead_zone=0.005)
    assert net == pytest.approx(0.0)
    assert basis == pytest.approx(2.0)


def test_attribute_series_only_counts_responsible_years() -> None:
    series = {2020: 100.0, 2021: 110.0, 2022: 99.0}
    yp = {2020: {"A": 1.0}}  # A tillskrivs bara förbättringsåret (2020->2021)
    net, basis = score.attribute_series(series, "up", yp, "A", lag=1, dead_zone=0.005)
    assert net == pytest.approx(1.0)
    assert basis == pytest.approx(1.0)


def test_attribute_series_none_without_basis_or_gaps() -> None:
    assert score.attribute_series({2020: 1.0, 2021: 2.0}, "up", {}, "A", 1, 0.005) == (None, 0.0)
    # glapp i serien -> inga konsekutiva år -> inget underlag
    gappy = score.attribute_series({2018: 1.0, 2021: 2.0}, "up", {2017: {"A": 1.0}}, "A", 1, 0.005)
    assert gappy == (None, 0.0)


def test_confidence_interval_clamped() -> None:
    assert score.confidence_interval(4.8, 1.5) == [pytest.approx(3.3), pytest.approx(5.0)]
    assert score.confidence_interval(0.2, 1.5) == [pytest.approx(0.0), pytest.approx(1.7)]


def test_total_score_matches_idea_example() -> None:
    # IDEA.md "Slutberäkning"-exemplet för Parti A.
    cat_scores = {
        "ekonomi": 4.0, "valfard": 3.5, "trygghet": 4.2, "forsvar": 4.5,
        "klimat": 2.8, "integration": 4.0, "demokrati": 3.7,
    }
    weights = {
        "ekonomi": 20, "valfard": 20, "trygghet": 15, "forsvar": 15,
        "klimat": 12.5, "integration": 10, "demokrati": 7.5,
    }
    assert score.total_score(cat_scores, weights) == pytest.approx(3.8325)


def test_total_score_rejects_negative_weight() -> None:
    with pytest.raises(ValueError):
        score.total_score({"a": 4.0, "b": 3.0}, {"a": 3.0, "b": -1.0})


def test_total_score_rejects_nonpositive_sum() -> None:
    with pytest.raises(ValueError):
        score.total_score({"a": 4.0}, {"a": 0.0})


def test_category_score_from_components_pins_ci() -> None:
    out = score.category_score_from_components({"A": 4.0, "B": 4.0, "C": 4.0, "D": 4.0})
    assert out["score"] == pytest.approx(4.0)
    # Default halvbredd = 1.5*(0.40*0.15+0.35*0.40+0.15*0.15+0.10*0.70) = 0.43875
    assert out["ci"] == [pytest.approx(3.561), pytest.approx(4.439)]
    assert out["confidence"] == {"A": "high", "B": "medium", "C": "high", "D": "low"}


def test_uncertainty_is_data_driven() -> None:
    # Mittbetyg så intervallet inte klipps; bredd = 2*halvbredd.
    mid = {"A": 2.5, "B": 2.5, "C": 2.5, "D": 2.5}
    default = score.category_score_from_components(mid)
    b_low = score.category_score_from_components(mid, confidence_overrides={"B": "low"})
    all_high = score.category_score_from_components(
        mid, confidence_overrides={"A": "high", "B": "high", "C": "high", "D": "high"}
    )

    def width(r: dict) -> float:
        return r["ci"][1] - r["ci"][0]

    # Lägre confidence på B -> bredare intervall än default; allt högt -> smalare.
    assert width(b_low) > width(default) > width(all_high)


def test_not_applicable_flag_and_confidence() -> None:
    out = score.category_score_from_components(
        {"A": 3.0, "B": 3.0, "C": 3.0, "D": 2.5},
        confidence_overrides={"D": "low"},
        flags=["D_not_applicable"],
    )
    assert out["flags"] == ["D_not_applicable"]
    assert out["confidence"]["D"] == "low"


def test_category_score_rejects_out_of_range_component() -> None:
    with pytest.raises(ValueError):
        score.category_score_from_components({"A": 9.0, "B": 3.0, "C": 3.0, "D": 3.0})
