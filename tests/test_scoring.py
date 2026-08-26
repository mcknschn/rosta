"""Golden tests för den deterministiska betygsmatten."""

from __future__ import annotations

import pytest

from pipeline import score

# Godtyckliga vikter för att pröva weighted_category_score som ren funktion.
# Modellens egna vikter står i config/scoring.yaml och prövas i tests/test_config.py.
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


def test_coverage_shrink_endpoints() -> None:
    assert score.coverage_shrink(4.0, 1.0) == pytest.approx(4.0)   # full täckning -> oförändrat
    assert score.coverage_shrink(4.0, 0.0) == pytest.approx(2.5)   # ingen täckning -> neutral
    assert score.coverage_shrink(1.0, 0.5) == pytest.approx(1.75)


def test_coverage_shrink_monoton_och_symmetrisk_runt_neutral() -> None:
    # mer täckning -> närmare råvärdet, från båda håll
    assert score.coverage_shrink(4.5, 0.3) < score.coverage_shrink(4.5, 0.7) < 4.5
    assert score.coverage_shrink(0.5, 0.3) > score.coverage_shrink(0.5, 0.7) > 0.5
    # symmetri: lika stort avstånd över/under 2.5 krymper lika mycket
    over = score.coverage_shrink(3.5, 0.4) - 2.5
    under = 2.5 - score.coverage_shrink(1.5, 0.4)
    assert over == pytest.approx(under)


def test_weighted_mean_with_neutral_missing() -> None:
    # saknad key i nämnaren bidrar neutralt 0: (1.0*30 + 0*10)/40 = 0.75
    out = score.weighted_mean_with_neutral_missing({"a": 1.0}, {"a": 30, "b": 10}, ["a", "b"])
    assert out == pytest.approx(0.75)
    # full täckning -> vanligt viktat medel: (1.0*30 - 1.0*10)/40 = 0.5
    out = score.weighted_mean_with_neutral_missing(
        {"a": 1.0, "b": -1.0}, {"a": 30, "b": 10}, ["a", "b"]
    )
    assert out == pytest.approx(0.5)
    # tom nämnarvikt -> None; värden utanför nämnaren ignoreras
    assert score.weighted_mean_with_neutral_missing({"a": 1.0}, {}, ["a"]) is None
    out = score.weighted_mean_with_neutral_missing({"a": 1.0, "x": -1.0}, {"a": 30, "x": 99}, ["a"])
    assert out == pytest.approx(1.0)


def test_neutral_missing_rollup_ekvivalent_med_coverage_shrink() -> None:
    # spec §3.3: direkt neutral-missing-rollup == krympning av det renormaliserade betyget,
    # eftersom net_support_to_score är linjär.
    vals = {"a": 0.8, "b": -0.2}
    w = {"a": 35, "b": 20, "c": 30, "d": 15}
    den = ["a", "b", "c", "d"]
    just = score.net_support_to_score(score.weighted_mean_with_neutral_missing(vals, w, den))
    raw = score.net_support_to_score(score.submeasure_weighted_mean(vals, w))
    assert just == pytest.approx(score.coverage_shrink(raw, (35 + 20) / 100))


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
    assert score.direction_adjusted_change(0, 5, "up") is None                       # v_prev=0
    # Riktningen håller bara upp och ned (ADR 0011 punkt 3). Ett tredje värde är ett fel i
    # configen och hard-failar hellre än att tyst ge None, som 'target' en gång gjorde.
    with pytest.raises(ValueError, match="Okänd riktning"):
        score.direction_adjusted_change(100, 110, "target")


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
    # Default halvbredd = 1.5*(0.30*0.15+0.50*0.40+0.00*0.15+0.20*0.70) = 0.5775
    # ADR 0002: spannet blir bredare eftersom C:s höga säkerhet inte längre drar ned det.
    assert out["ci"] == [pytest.approx(3.422), pytest.approx(4.577)]
    assert out["confidence"] == {"A": "high", "B": "medium", "C": "high", "D": "low"}


def test_c_contributes_nothing_to_the_category_score() -> None:
    # ADR 0002 punkt 5: C är maktandel, inte delpoäng. Den väger noll och får därför
    # aldrig flytta vare sig betyget eller spannet, hur stor den än är.
    low_c = score.category_score_from_components({"A": 4.0, "B": 3.0, "C": 0.0, "D": 2.0})
    high_c = score.category_score_from_components({"A": 4.0, "B": 3.0, "C": 5.0, "D": 2.0})
    assert low_c["score"] == high_c["score"]
    assert low_c["ci"] == high_c["ci"]


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


# --- Begränsad kvot: A:s form efter ADR 0005 ------------------------------------

def test_bounded_quotient_ar_noll_vid_jamnhojd() -> None:
    assert score.bounded_quotient(0.12, 0.12) == pytest.approx(0.0)


def test_bounded_quotient_ligger_i_intervallet() -> None:
    """q ligger i [-1, 1] av konstruktion, hur extrem andelen än är (ADR 0005 punkt 3)."""
    for andel in (0.0, 1e-9, 0.001, 0.5, 1.0, 1000.0):
        for forankring in (1e-9, 0.001, 0.5, 1.0, 1000.0):
            assert -1.0 <= score.bounded_quotient(andel, forankring) <= 1.0


def test_bounded_quotient_mattar_mjukt() -> None:
    """Tre gånger och fem gånger förankringen hamnar nära varandra (deklarerad kostnad)."""
    q3 = score.bounded_quotient(0.30, 0.10)
    q5 = score.bounded_quotient(0.50, 0.10)
    assert q3 == pytest.approx(0.5)
    assert q5 == pytest.approx(2 / 3)
    assert q5 - q3 < 0.2


def test_bounded_quotient_nastan_lika_andelar_ger_nastan_lika_kvot() -> None:
    """Godkännandetest: 8,73e-06 skillnad i andel får inte bli ett helt betygssteg."""
    a = score.bounded_quotient(0.0413, 0.0500)
    b = score.bounded_quotient(0.0413 + 8.73e-06, 0.0500)
    assert abs(score.net_support_to_score(a) - score.net_support_to_score(b)) < 0.001


def test_bounded_quotient_utan_underlag_ar_noll() -> None:
    """andel = förankring = 0 saknar kvot. Den blir 0, alltså jämnhöjd, aldrig NaN."""
    assert score.bounded_quotient(0.0, 0.0) == 0.0


def test_bounded_quotient_negativt_underlag_ar_hard_fail() -> None:
    """Andelar och förankringar är per konstruktion icke-negativa. Ett negativt tal är ett fel."""
    with pytest.raises(ValueError):
        score.bounded_quotient(-0.1, 0.2)
    with pytest.raises(ValueError):
        score.bounded_quotient(0.1, -0.2)


def test_a_spridningen_beror_pa_underlaget_till_skillnad_fran_rang() -> None:
    """Godkännandetest ur biljett #21: A slutar spendera hela sitt utrymme oavsett underlag.

    Samma åtta andelar mot två olika förankringar. Rangnormaliseringen ger samma spridning i
    båda fallen, eftersom den alltid lägger lägsta partiet på 0 och högsta på 5. Den begränsade
    kvoten ger olika, eftersom den mäter hur långt ifrån förankringen andelarna faktiskt ligger.
    """
    shares = {"S": 0.052, "M": 0.050, "SD": 0.050, "C": 0.051, "V": 0.049,
              "KD": 0.050, "L": 0.050, "MP": 0.053}

    def spread(anchor: float) -> float:
        vals = [score.net_support_to_score(score.bounded_quotient(v, anchor))
                for v in shares.values()]
        return max(vals) - min(vals)

    rank = score.rank_normalize(shares)
    assert max(rank.values()) - min(rank.values()) == pytest.approx(5.0)
    assert spread(0.050) != pytest.approx(spread(0.020))
    assert spread(0.050) < 1.0        # nästan lika andelar ger nästan lika betyg
