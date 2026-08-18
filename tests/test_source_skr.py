"""Fas 1c-tester: SKR-regionstyren -> responsibility (regional) + subnationell C.

Deterministiska, utan nätverk. Golden-tallyn nedan pinnar regiondatan i config/mappings.yaml
mot SKR:s officiella sammanställning (Styren i regioner 1994-2022 + efter valet 2022); ändras
datan av misstag failar testet. 2022-talen matchar SKR:s halvtidsuppföljnings-PDF exakt.
"""

from __future__ import annotations

from pipeline import config, schema, score, scorerun, warehouse
from pipeline.sources import skr

CANON = ["S", "M", "SD", "C", "V", "KD", "L", "MP"]

# Antal regioner med partiet i det ledande styret per valår (SKR, officiellt).
GOLDEN_TALLY = {
    "2014-2018": {"S": 16, "M": 5, "SD": 0, "C": 8, "V": 13, "KD": 5, "L": 7, "MP": 19},
    "2018-2022": {"S": 9, "M": 13, "SD": 0, "C": 19, "V": 2, "KD": 13, "L": 16, "MP": 10},
    "2022-2026": {"S": 13, "M": 11, "SD": 1, "C": 12, "V": 6, "KD": 12, "L": 6, "MP": 3},
}
TERMS = ("2014-2018", "2018-2022", "2022-2026")


def test_subnational_responsibility_valid_and_complete() -> None:
    rows = skr.build_regional_responsibility()
    assert rows
    valid = set(config.party_codes())
    for r in rows:
        schema.validate("responsibility", r)  # höjer vid fel
        assert r["level"] == "regional"
        assert r["role"] == "government"
        assert r["party"] in valid
        assert r["geography"]                       # icke-tom regionkod
        assert 0.0 < r["strength"] <= 1.0
        assert r["source_ref"].startswith("skr:")   # spårar till SKR
        assert r["period"] in TERMS
    # 21 regioner, var och en med alla tre mandatperioder.
    geos = {r["geography"] for r in rows}
    assert len(geos) == 21
    for geo in geos:
        periods = {r["period"] for r in rows if r["geography"] == geo}
        assert periods == set(TERMS), f"{geo} saknar period: {set(TERMS) - periods}"
    # ids unika.
    ids = [r["id"] for r in rows]
    assert len(ids) == len(set(ids))


def test_strength_is_equal_coalition_share() -> None:
    rows = skr.build_regional_responsibility()
    # Per (region, period) ska strength summera till <=1 (lokala partier räknas ej med).
    by_cell: dict[tuple[str, str], list[float]] = {}
    for r in rows:
        by_cell.setdefault((r["geography"], r["period"]), []).append(r["strength"])
    for (geo, period), strengths in by_cell.items():
        n = len(strengths)
        assert all(abs(s - 1.0 / n) < 1e-9 for s in strengths), f"{geo} {period}"
        assert abs(sum(strengths) - 1.0) < 1e-9


def test_golden_tally_matches_skr() -> None:
    """Antal regioner per parti och mandatperiod = SKR:s officiella siffror (regressionsgrind)."""
    rows = skr.build_regional_responsibility()
    for period, expected in GOLDEN_TALLY.items():
        got = {p: 0 for p in CANON}
        for r in rows:
            if r["period"] == period:
                got[r["party"]] += 1
        assert got == expected, f"{period}: {got} != {expected}"


# Antal KOMMUNER med partiet i styret per valår (SKR open data, per-kommun CSV). Inom ±2 av
# SKR:s halvtidsuppföljnings-PDF "efter valet 2022" (ögonblicksvariation mellan SKR-produkter).
MUNICIPAL_GOLDEN = {
    "2014-2018": {"S": 194, "M": 113, "SD": 0, "C": 144, "V": 102, "KD": 100, "L": 110, "MP": 124},
    "2018-2022": {"S": 147, "M": 161, "SD": 4, "C": 201, "V": 60, "KD": 153, "L": 148, "MP": 69},
    "2022-2026": {"S": 162, "M": 175, "SD": 39, "C": 149, "V": 58, "KD": 138, "L": 107, "MP": 48},
}


def test_municipal_responsibility_valid_and_complete() -> None:
    rows = skr.build_municipal_responsibility()
    assert rows
    valid = set(config.party_codes())
    for r in rows:
        schema.validate("responsibility", r)
        assert r["level"] == "municipal"
        assert r["role"] == "government"
        assert r["party"] in valid
        assert len(r["geography"]) == 4 and r["geography"].isdigit()   # SCB 4-siffrig kommunkod
        assert 0.0 < r["strength"] <= 1.0
        assert r["source_ref"].startswith("skr:")
        assert r["period"] in TERMS
    assert len({r["geography"] for r in rows}) == 290                  # alla 290 kommuner
    ids = [r["id"] for r in rows]
    assert len(ids) == len(set(ids))


def test_municipal_golden_tally_matches_skr() -> None:
    rows = skr.build_municipal_responsibility()
    for period, expected in MUNICIPAL_GOLDEN.items():
        got = {p: 0 for p in CANON}
        for r in rows:
            if r["period"] == period:
                got[r["party"]] += 1
        assert got == expected, f"{period}: {got} != {expected}"


def test_municipalities_config_invariants() -> None:
    data = config.subnational_municipalities()["municipalities"]
    assert len(data) == 290
    valid = set(config.party_codes())
    for code, entry in data.items():
        assert len(code) == 4 and code.isdigit(), code
        assert entry.get("name")
        terms = entry["terms"]
        assert len(terms) == 3, code
        for leading in terms:
            assert set(leading) <= valid, f"{code}: {leading}"
            assert len(leading) == len(set(leading)), code


def test_municipal_fractions_in_unit_range() -> None:
    muni = scorerun.municipal_fractions()
    assert set(muni) == set(config.party_codes())
    assert all(0.0 <= v <= 1.0 for v in muni.values())
    assert 0.0 < sum(muni.values()) <= 1.0


def test_each_region_term_resolves_a_source() -> None:
    sg = config.mappings()["subnational_governance"]
    sources = sg["sources"]
    term_source = sg["term_source"]
    for code, region in sg["regions"].items():
        for term in region["terms"]:
            keys = term_source.get(term)
            assert keys, f"{code} {term} saknar term_source"
            for k in keys:
                assert k in sources and sources[k].get("url"), f"källa {k} saknar url"


def test_mappings_regions_invariants() -> None:
    sg = config.mappings()["subnational_governance"]
    assert sg["status"] == "regions_complete"
    assert sg["municipalities"]["status"] == "complete"     # kommuner nu inlästa (egen fil)
    valid = set(config.party_codes())
    assert len(sg["regions"]) == 21
    for code, region in sg["regions"].items():
        assert region.get("name")
        assert set(region["terms"]) == set(TERMS), code
        for term, styre in region["terms"].items():
            leading = styre["leading_parties"]
            assert leading, f"{code} {term} tomt styre"
            assert set(leading) <= valid, f"{code} {term} ogiltig partikod"
            assert len(leading) == len(set(leading)), f"{code} {term} dubblett"


def test_regional_fractions_in_unit_range() -> None:
    reg = scorerun.regional_fractions()
    assert set(reg) == set(config.party_codes())
    assert all(0.0 <= v <= 1.0 for v in reg.values())
    # summan = andel icke-tomma celler = 1.0 (alla 63 region-perioder har ett styre).
    assert abs(sum(reg.values()) - 1.0) < 1e-9


def test_category_c_blends_region_and_municipal() -> None:
    parties = config.party_codes()
    cats = config.category_ids()
    nat = scorerun.government_fractions()
    reg = scorerun.regional_fractions()
    mun = scorerun.municipal_fractions()
    by_cat, conf, flags = scorerun.category_c(nat, reg, mun, parties, cats)
    for c in cats:
        for p in parties:
            assert 0.0 <= by_cat[c][p] <= 5.0
    # Full subnationell täckning (regioner+kommuner) -> hög säkerhet, ingen caveat-flagga.
    assert conf["valfard"] == "high"
    assert flags["valfard"] == []
    # forsvar: subnationell vikt 0 per design -> ren nationell makt (= rank-norm av nat_frac).
    assert flags["forsvar"] == ["C_national_only_by_design"]
    assert conf["forsvar"] == "high"
    nat_only = score.rank_normalize(nat)
    assert all(abs(by_cat["forsvar"][p] - nat_only[p]) < 1e-9 for p in parties)
    # C bär en kategorisignal (ej platt konstant): kategorier som blandar in subnationell makt
    # skiljer sig från det rent nationella forsvar.
    assert any(by_cat["ekonomi"][p] != by_cat["forsvar"][p] for p in parties)
    # Signalen är EN bit bred, inte mer: forsvar mot resten. Blandningsvikterna skiljer sig mellan
    # de sex blandande kategorierna (national 0,4-0,8, split region/kommun 0-0,45), men efter
    # rangnormaliseringen ger de samma ordning, så samma vektor. Före issue #14 låg trygghet som en
    # tredje vektor - SD och C stod olika där - och maktandelens gräns flyttade den korsningen.
    # Testet pinnar det som gäller nu; blir det tre vektorer igen är det en riktig ändring i C.
    vectors = {tuple(round(by_cat[c][p], 9) for p in parties) for c in cats}
    assert len(vectors) == 2
    # Guard: utan subnationell data faller C på nationell fallback (flaggad, sänkt säkerhet).
    g_by, g_conf, g_flags = scorerun.category_c(nat, {}, {}, parties, cats)
    assert g_flags["valfard"] == ["C_missing_subnational"]
    assert g_conf["valfard"] == "medium"


def test_regional_responsibility_warehouse_idempotent() -> None:
    con = warehouse.connect(":memory:")
    rows = skr.build_subnational_responsibility()
    n = warehouse.upsert(con, "responsibility", rows)
    assert warehouse.count(con, "responsibility") == n
    warehouse.upsert(con, "responsibility", rows)   # samma id:n -> ingen tillväxt
    assert warehouse.count(con, "responsibility") == n
    con.close()
