"""C3 — subnationell D (docs/done/c3_subnational_d_metod.md): region-attribution, region-år-makt,
submåtts-blandning, byte-identisk när avstängd, rättvisa (regional-only -> measured) + config-grind.

Mönstret speglar tests/test_fas5.py (seedat in-memory-warehouse) och test_b_coverage_mode.py
(monkeypatch-deepcopy för config-override). region_year_power_fractions läser den RIKTIGA
subnational_governance-configen (inte seedad), så testerna pinnar den faktiska region/term-datan.
"""

from __future__ import annotations

import copy

import pytest

from pipeline import config, score, scorerun, warehouse
from pipeline.sources import government

# --- 1. Ren matte: attribute_subnational_indicator (score.py) -----------------------------

# lag=1: en förändring år y tillskrivs makten år (y-1). ryp täcker 2014-2016 -> förändringarna
# 2015/2016/2017 attribueras 2014/2015/2016. Region R1 styrs av X, R2 av Y (full makt).
_RYP = {
    "R1": {2014: {"X": 1.0}, 2015: {"X": 1.0}, 2016: {"X": 1.0}},
    "R2": {2014: {"Y": 1.0}, 2015: {"Y": 1.0}, 2016: {"Y": 1.0}},
}


def test_attribute_subnational_pools_over_regions_equal_weight() -> None:
    # up-indikator som STIGER i båda regionerna -> +1 varje konsekutiv förändring.
    series = {
        "R1": {2014: 10, 2015: 11, 2016: 12, 2017: 13},
        "R2": {2014: 10, 2015: 11, 2016: 12, 2017: 13},
    }
    # X styr bara R1 (3 attribuerade förändringar, alla +1) -> net 1.0, den_raw 3, n_regions 2.
    assert score.attribute_subnational_indicator(series, "up", _RYP, "X", 1, 0.0) == (1.0, 3.0, 2)
    # Y styr bara R2 -> samma. Ett parti utan makt -> (None, 0, 2) men n_regions räknar ändå datan.
    assert score.attribute_subnational_indicator(series, "up", _RYP, "Y", 1, 0.0) == (1.0, 3.0, 2)
    assert score.attribute_subnational_indicator(series, "up", _RYP, "Z", 1, 0.0) == (None, 0.0, 2)


def test_attribute_subnational_direction_and_sign() -> None:
    # R1 stiger (bra för up), R2 faller (dåligt). X styr R1 -> +1; Y styr R2 -> -1.
    series = {
        "R1": {2014: 10, 2015: 11, 2016: 12, 2017: 13},
        "R2": {2014: 13, 2015: 12, 2016: 11, 2017: 10},
    }
    net_x, _, _ = score.attribute_subnational_indicator(series, "up", _RYP, "X", 1, 0.0)
    net_y, _, _ = score.attribute_subnational_indicator(series, "up", _RYP, "Y", 1, 0.0)
    assert net_x == 1.0 and net_y == -1.0
    # down-riktning vänder tecknet: R1 som stiger blir nu en försämring för X.
    net_x_down, _, _ = score.attribute_subnational_indicator(series, "down", _RYP, "X", 1, 0.0)
    assert net_x_down == -1.0


def test_attribute_subnational_skips_year_gaps_and_counts_regions() -> None:
    # R3 har ENBART ett glapp (2014->2016) -> ingen konsekutiv förändring -> räknas ej i n_regions.
    series = {"R1": {2014: 10, 2015: 11, 2016: 12, 2017: 13}, "R3": {2014: 10, 2016: 12}}
    ryp = {**_RYP, "R3": {2014: {"X": 1.0}, 2015: {"X": 1.0}}}
    net, den, n = score.attribute_subnational_indicator(series, "up", ryp, "X", 1, 0.0)
    assert (net, den, n) == (1.0, 3.0, 1)  # bara R1 har konsekutiv data


def test_attribute_subnational_dead_zone() -> None:
    # förändring under dödzonen -> tecken 0 (oförändrat), räknas i den men inte num.
    series = {"R1": {2015: 100.0, 2016: 100.2, 2017: 100.4}}  # ~0.2 % förändring < 1 %
    ryp = {"R1": {2015: {"X": 1.0}, 2016: {"X": 1.0}}}
    net, den, n = score.attribute_subnational_indicator(series, "up", ryp, "X", 1, 0.01)
    assert net == 0.0 and den == 2.0 and n == 1


# --- 2. region_year_power_fractions (riktig config) ---------------------------------------

def test_region_year_power_keys_are_kolada_codes_and_coalition_split() -> None:
    ryp = scorerun.region_year_power_fractions()
    assert ryp, "subnational_governance saknas i config"
    assert "0001" in ryp and "01" not in ryp  # 4-siffrig Kolada-kod, inte config-nyckeln
    # Region Stockholm 2022-2026 styrs av [S, C, MP] (mappings.yaml). 2024 ligger helt inom
    # mandatperioden -> varje parti får 1/3 (jämn koalitionsdelning, dagviktat = hela året).
    y2024 = ryp["0001"][2024]
    assert set(y2024) == {"S", "C", "MP"}
    for p in ("S", "C", "MP"):
        assert y2024[p] == pytest.approx(1 / 3)
    assert sum(y2024.values()) == pytest.approx(1.0)


def test_region_year_power_only_riksdag_parties_and_bounded() -> None:
    ryp = scorerun.region_year_power_fractions()
    valid = set(config.party_codes())
    for region, years in ryp.items():
        assert len(region) == 4
        for year, frac in years.items():
            assert set(frac) <= valid                  # lokala partier räknas aldrig
            assert sum(frac.values()) <= 1.0 + 1e-9     # dagviktad andel, aldrig > 1


# --- 3. Integration: blend, byte-identisk när av, rättvisa --------------------------------

def _seed() -> object:
    con = warehouse.connect(":memory:")
    warehouse.upsert(con, "responsibility", government.build_national_responsibility())
    warehouse.upsert(con, "party_activity", [
        {"party": "S", "category": "valfard", "committee": "SoU",
         "kind": "motion", "period": "w", "count": 50, "source_ref": "u"},
    ], validate=False)
    return con


def _region_overlevnad_obs() -> list[dict]:
    """overlevnad_svar_sjukdom (up) per region; INGEN nationell välfärdsserie -> välfärd-D kan
    bara bli measured via den subnationella attributionen (renodlar rättvise-effekten)."""
    series = {
        "0001": {2019: 90, 2020: 91, 2021: 92, 2022: 93, 2023: 94},  # Stockholm: stiger
        "0012": {2019: 94, 2020: 93, 2021: 92, 2022: 91, 2023: 90},  # Skåne: faller
        "0014": {2019: 90, 2020: 91, 2021: 92, 2022: 93, 2023: 94},  # VGR: stiger
    }
    rows = []
    for geo, vals in series.items():
        for y, v in vals.items():
            rows.append({
                "id": f"obs:kolada:U70471:{geo}:{y}", "category": "valfard",
                "submeasure": "vard_tillganglighet", "indicator": "overlevnad_svar_sjukdom",
                "period": str(y), "value": float(v), "unit": "%", "geography": geo,
                "source_ref": f"kolada:U70471:{geo}:{y}",
            })
    return rows


def _set_subnational_enabled(monkeypatch: pytest.MonkeyPatch, enabled: bool) -> None:
    sc = copy.deepcopy(config.scoring())
    sc["D_resultat"]["subnational"]["enabled"] = enabled
    monkeypatch.setattr(config, "scoring", lambda: sc)


def test_subnational_blends_into_valfard_and_flags(monkeypatch: pytest.MonkeyPatch) -> None:
    _set_subnational_enabled(monkeypatch, True)
    con = _seed()
    warehouse.upsert(con, "observations", _region_overlevnad_obs())
    sc = scorerun.build(con)["scores"]["scores"]
    # Minst ett parti blir measured för välfärd ENBART via regional attribution (D_not_applicable
    # borttagen) och bär D_subnational_region-flaggan.
    measured = [p for p in sc if "D_not_applicable" not in sc[p]["valfard"]["flags"]]
    assert measured, "ingen blev measured för välfärd via regional attribution"
    for p in measured:
        assert any(f.startswith("D_subnational_region_") for f in sc[p]["valfard"]["flags"])
    con.close()


def test_disabled_is_byte_identical_to_no_region_data(monkeypatch: pytest.MonkeyPatch) -> None:
    # Med subnational AV ska region-observationerna ignoreras helt -> identiskt med att de inte fanns.
    _set_subnational_enabled(monkeypatch, False)
    con_with = _seed()
    warehouse.upsert(con_with, "observations", _region_overlevnad_obs())
    with_region = scorerun.build(con_with)["scores"]["scores"]
    con_without = _seed()
    without_region = scorerun.build(con_without)["scores"]["scores"]
    assert with_region == without_region  # exakt lika -> legacy-garantin
    # och inget D_subnational_region-spår någonstans
    assert not any(
        f.startswith("D_subnational_region_")
        for p in with_region for c in with_region[p] for f in with_region[p][c]["flags"]
    )
    con_with.close()
    con_without.close()


def test_only_valfard_changes_other_categories_byte_identical(monkeypatch: pytest.MonkeyPatch) -> None:
    # Samma seedade con; ENDA skillnaden är subnational på/av. Bara välfärd får röra sig.
    con = _seed()
    warehouse.upsert(con, "observations", _region_overlevnad_obs())
    _set_subnational_enabled(monkeypatch, False)
    off = scorerun.build(con)["scores"]["scores"]
    _set_subnational_enabled(monkeypatch, True)
    on = scorerun.build(con)["scores"]["scores"]
    for p in on:
        for c in on[p]:
            if c == "valfard":
                continue
            assert on[p][c]["components"]["D"] == off[p][c]["components"]["D"], (p, c)
            assert on[p][c]["flags"] == off[p][c]["flags"], (p, c)
    con.close()


# --- 4. Config-grind (config.validate) ----------------------------------------------------

def _validate_with(monkeypatch: pytest.MonkeyPatch, mutate) -> None:
    sc = copy.deepcopy(config.scoring())
    mutate(sc["D_resultat"]["subnational"])
    monkeypatch.setattr(config, "scoring", lambda: sc)
    config.validate()


def test_subnational_config_valid_passes(monkeypatch: pytest.MonkeyPatch) -> None:
    _validate_with(monkeypatch, lambda s: None)  # orörd config validerar


def test_subnational_weights_must_sum_to_one(monkeypatch: pytest.MonkeyPatch) -> None:
    with pytest.raises(config.ConfigError):
        _validate_with(monkeypatch, lambda s: s["submeasure_level_weights"]["vard_tillganglighet"]
                       .update({"national": 0.4, "region": 0.5}))


def test_subnational_unknown_submeasure_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    with pytest.raises(config.ConfigError):
        _validate_with(monkeypatch, lambda s: s["submeasure_level_weights"]
                       .update({"inte_ett_submatt": {"national": 0.4, "region": 0.6}}))


def test_subnational_bad_region_weighting_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    with pytest.raises(config.ConfigError):
        _validate_with(monkeypatch, lambda s: s.update({"region_weighting": "befolkning"}))


def test_subnational_enabled_must_be_bool(monkeypatch: pytest.MonkeyPatch) -> None:
    with pytest.raises(config.ConfigError):
        _validate_with(monkeypatch, lambda s: s.update({"enabled": "ja"}))
