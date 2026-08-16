"""D-undermåttsbredd (docs/done/d_coverage_krympning_spec.md): nämnare, krympning, flaggor och grind.

Grinden speglar fas4b-mönstret (test_fas4b_coverage): varje kategori under
thin_coverage_threshold är ANTINGEN åtgärdad ELLER explicit accepterad i
coverage_allowlist.d_thin_breadth_accepted med skäl, och listan kan inte bära inaktuella
poster. Mätaren (coverage_report.d_submeasure_breadth) är offline: ett undermått räknas
täckt om det har en up/down-indikator som inte är coverage-allowlistad — Fas 3-gatens
invariant (test_fas3_gate: inläst ELLER allowlistad, aldrig båda) garanterar att en sådan
indikator faktiskt är inläst. End-to-end-testerna kör scorerun.build mot ett seedat
in-memory-warehouse med coverage_shrink påslagen via config-override.
"""

from __future__ import annotations

import copy

import pytest

from pipeline import config, scorerun, warehouse
from pipeline.sources import government
from pipeline.tools import coverage_report

# --- nämnaren: target-only exkluderas, indikatorlösa undermått ingår -----------------


def test_d_denominator_excludes_target_only() -> None:
    den = scorerun._d_denominator_submeasures()
    # ekonomi: inflation/offentliga finanser har ENBART target-indikatorer -> utanför nämnaren
    assert "inflation_prisstabilitet" not in den["ekonomi"]
    assert "offentliga_finanser" not in den["ekonomi"]
    # blandat undermått (target + up) är INTE target-only -> ingår i nämnaren
    assert "ekonomisk_ambition" in den["forsvar"]


def test_d_denominator_keeps_indicatorless_submeasure() -> None:
    # undermått utan indikatorer är inte target-only per automatik — det är en del av
    # kategorianspråket och ska dra mot neutral tills en indikator byggs
    assert "industriell_konkurrenskraft" in scorerun._d_denominator_submeasures()["klimat"]


# --- grind: tunn D-bredd passerar aldrig tyst (allowlist-mönstret) --------------------


def _thin() -> set[str]:
    rep = coverage_report.d_submeasure_breadth()
    return {c["id"] for c in rep["categories"] if c["thin"]}


def _accepted() -> set[str]:
    return {e["category"] for e in (config.coverage_allowlist().get("d_thin_breadth_accepted") or [])}


def test_no_unaccounted_thin_d_breadth() -> None:
    """Varje kategori med viktad D-bredd under tröskeln måste vara explicit accepterad i
    coverage_allowlist.d_thin_breadth_accepted — annars är det en TYST regression."""
    unaccounted = _thin() - _accepted()
    assert not unaccounted, (
        "Tunn D-bredd utan motivering — bredda D-täckningen (Spår D) eller lägg posten i "
        f"coverage_allowlist.d_thin_breadth_accepted med skäl: {sorted(unaccounted)}"
    )


def test_d_thin_allowlist_shrinks() -> None:
    """En accepterad post måste fortfarande VARA under tröskeln. När D-täckningen breddas
    ska posten tas bort — listan krymper, växer aldrig tyst."""
    stale = _accepted() - _thin()
    assert not stale, (
        "Kategori i d_thin_breadth_accepted är inte längre under tröskeln (luckan löst) — "
        f"ta bort posten: {sorted(stale)}"
    )


def test_d_thin_allowlist_valid() -> None:
    cat_ids = set(config.category_ids())
    for e in config.coverage_allowlist().get("d_thin_breadth_accepted") or []:
        assert e["category"] in cat_ids, f"Okänd kategori i d_thin_breadth_accepted: {e}"
        assert e.get("reason", "").strip(), f"Saknar skäl: {e}"


def test_d_breadth_partitions_and_bounds() -> None:
    """Mätaren rapporterar alla 7 kategorier; täckta + otäckta partitionerar nämnaren och
    kvoten ligger i [0,1]."""
    rep = coverage_report.d_submeasure_breadth()
    den = scorerun._d_denominator_submeasures()
    assert {c["id"] for c in rep["categories"]} == set(config.category_ids())
    for c in rep["categories"]:
        assert set(c["covered_submeasures"]) | set(c["uncovered_submeasures"]) == den[c["id"]]
        assert not set(c["covered_submeasures"]) & set(c["uncovered_submeasures"])
        assert 0.0 <= c["ratio"] <= 1.0
        assert c["covered_weight"] <= c["total_weight"]
        assert c["thin"] == (c["ratio"] < rep["threshold"])


# --- end-to-end: krympning, flaggor, per parti/kategori-numerator ----------------------


def _seed_con():
    con = warehouse.connect(":memory:")
    warehouse.upsert(con, "responsibility", government.build_national_responsibility())
    return con


def _obs(indicator: str, submeasure: str, vals: dict[int, float], unit: str = "%") -> list[dict]:
    return [
        {"id": f"obs:test:{indicator}:{y}", "category": "ekonomi", "submeasure": submeasure,
         "indicator": indicator, "period": str(y), "value": v, "unit": unit,
         "geography": "Riket", "source_ref": f"test:{y}"}
        for y, v in vals.items()
    ]


# arbetslöshet (down=bättre) faller stadigt under S/MP-regeringen 2014-2021
ARBETSLOSHET = {2014: 8.0, 2015: 7.5, 2016: 7.0, 2017: 6.7, 2018: 6.5, 2019: 6.4, 2020: 6.2, 2021: 6.0}
# bnp_per_capita (up=bättre) stiger 2021-2025 -> attribuerar både S/MP- och M-ledda år
BNP = {2021: 100.0, 2022: 102.0, 2023: 104.0, 2024: 106.0, 2025: 108.0}


def _set_shrink(monkeypatch: pytest.MonkeyPatch, on: bool) -> None:
    sc = copy.deepcopy(config.scoring())
    sc["D_resultat"]["coverage_shrink"] = on
    monkeypatch.setattr(config, "scoring", lambda: sc)


def _shrink_on(monkeypatch: pytest.MonkeyPatch) -> None:
    _set_shrink(monkeypatch, True)


def test_coverage_shrink_krymper_d_och_flaggar(monkeypatch: pytest.MonkeyPatch) -> None:
    con = _seed_con()
    warehouse.upsert(con, "observations", _obs("arbetsloshet", "sysselsattning_arbetsloshet", ARBETSLOSHET))
    _set_shrink(monkeypatch, False)  # legacy-gren oavsett config-default
    base = scorerun.build(con)["scores"]["scores"]["S"]["ekonomi"]
    # legacy-grenen (shrink av, default) sätter inga D-breddflaggor
    assert not [f for f in base["flags"] if f.startswith("D_coverage") or f == "D_thin_coverage"]
    assert base["confidence"]["D"] == "medium"

    _shrink_on(monkeypatch)
    shrunk = scorerun.build(con)["scores"]["scores"]["S"]["ekonomi"]
    # ekonomi-nämnare = 73 (22+18+18+15; target-only exkluderade), täckt = 22
    assert "D_coverage_22/73" in shrunk["flags"]
    assert "D_thin_coverage" in shrunk["flags"]      # 22/73 ≈ 0.30 < 0.75
    assert "D_thin_basis" not in shrunk["flags"]     # ansvarsunderlaget (7 helår) är inte tunt
    assert shrunk["confidence"]["D"] == "low"        # medium -1 steg (endast thin_coverage)
    d0, d1 = base["components"]["D"], shrunk["components"]["D"]
    # spec §3.3-ekvivalensen (komponenter avrundas till 3 decimaler i scores.json)
    assert d1 == pytest.approx(2.5 + (d0 - 2.5) * 22 / 73, abs=1e-3)
    assert d0 > d1 > 2.5                             # förbättringen kvar, men ödmjukare
    con.close()


def test_na_celler_far_ingen_coverage_flagga(monkeypatch: pytest.MonkeyPatch) -> None:
    _shrink_on(monkeypatch)
    con = _seed_con()
    warehouse.upsert(con, "observations", _obs("arbetsloshet", "sysselsattning_arbetsloshet", ARBETSLOSHET))
    v_eco = scorerun.build(con)["scores"]["scores"]["V"]["ekonomi"]
    assert "D_not_applicable" in v_eco["flags"]
    assert v_eco["components"]["D"] == 2.5
    assert not [f for f in v_eco["flags"] if f.startswith("D_coverage") or f == "D_thin_coverage"]
    con.close()


def test_coverage_ar_per_parti(monkeypatch: pytest.MonkeyPatch) -> None:
    """Numeratorn är per (parti, kategori): S attribueras båda serierna, M bara bnp-serien
    (arbetslöshetsserien slutar 2021, före M-ledda år)."""
    _shrink_on(monkeypatch)
    con = _seed_con()
    warehouse.upsert(con, "observations",
                     _obs("arbetsloshet", "sysselsattning_arbetsloshet", ARBETSLOSHET)
                     + _obs("bnp_per_capita", "bnp_produktivitet", BNP, unit="index"))
    sc = scorerun.build(con)["scores"]["scores"]
    assert "D_coverage_40/73" in sc["S"]["ekonomi"]["flags"]   # 22 + 18 täckta
    assert "D_coverage_18/73" in sc["M"]["ekonomi"]["flags"]   # bara bnp_produktivitet
    con.close()


def test_thin_basis_och_thin_coverage_triggar_oberoende(monkeypatch: pytest.MonkeyPatch) -> None:
    """Kort serie där M bara attribueras en delårsviktad förändring -> tunt ansvarsunderlag
    OCH tunn bredd samtidigt; säkerheten sänks kumulativt men klampas till low."""
    _shrink_on(monkeypatch)
    con = _seed_con()
    warehouse.upsert(con, "observations",
                     _obs("bnp_per_capita", "bnp_produktivitet",
                          {2021: 100.0, 2022: 102.0, 2023: 104.0}, unit="index"))
    m_eco = scorerun.build(con)["scores"]["scores"]["M"]["ekonomi"]
    assert "D_thin_basis" in m_eco["flags"]       # basis = M:s del av 2022 (< 1.0)
    assert "D_thin_coverage" in m_eco["flags"]    # 18/73 < 0.75
    assert m_eco["confidence"]["D"] == "low"      # medium -2 steg, klampat i botten
    con.close()
