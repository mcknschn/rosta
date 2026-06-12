"""B5 — B-undermåttsbreddskrympning (docs/b_coverage_krympning_spec.md): formel, nämnare,
flaggformat, gate och mode-växel.

Mönstret speglar tests/test_d_breadth_gate.py (monkeypatch-deepcopy för mode-override,
seedat in-memory-warehouse för end-to-end). Default-läget är `policy_type_count` (legacy,
byte-identisk baseline — verifieras även mot dist/ i leveransen); `weighted_submeasure_depth`
aktiveras endast via config-override här. Ekvivalenstesterna räknar cov_B oberoende per cell
och låser att krympningen är exakt `2.5 + (B_raw - 2.5) * cov_B` (spec §3.3) med D:s
icke-target-nämnare (spec §3.4). Anti-gaming-testerna låser set-semantiken för |K_s|/|T_s|
(dedup inom undermått, bidrag en gång PER undermått — koldioxidskatt-fallet, spec §7).
"""

from __future__ import annotations

import copy
import re

import pytest

from pipeline import config, score, scorerun, warehouse
from pipeline.sources import government

# --- syntetisk fixtur för score.weighted_depth_coverage (spec §3.1/§3.3) --------------

W = {"a": 40.0, "b": 30.0, "c": 20.0, "d": 10.0, "t": 15.0}  # t = target-only (utanför nämnaren)
DEN = ("a", "b", "c", "d")  # fast nämnare, totalvikt 100
CODABLE = {"a": {"x1", "x2", "x3"}, "b": {"y"}, "c": {"z"}, "d": set()}  # d = B-vägg (T_s tom)


def test_wdc_full_och_tom_tackning() -> None:
    full = {"a": {"x1", "x2", "x3"}, "b": {"y"}, "c": {"z"}}
    codable = {"a": {"x1", "x2", "x3"}, "b": {"y"}, "c": {"z"}, "d": {"w"}}
    assert score.weighted_depth_coverage(codable, codable, W, DEN) == (100.0, 100.0)
    assert score.weighted_depth_coverage({}, codable, W, DEN) == (0.0, 100.0)
    # delmängd: d okodad -> w_d faller ur täljaren men inte nämnaren
    assert score.weighted_depth_coverage(full, codable, W, DEN) == (90.0, 100.0)


def test_wdc_b_vagg_bidrar_noll_men_behaller_vikt() -> None:
    # d har ingen kodbar typ (B-vägg) -> bidrag 0, men vikten 10 stannar i nämnaren
    coded = {"a": {"x1", "x2", "x3"}, "b": {"y"}, "c": {"z"}, "d": {"smuggad_typ"}}
    covered, total = score.weighted_depth_coverage(coded, CODABLE, W, DEN)
    assert (covered, total) == (90.0, 100.0)


def test_wdc_delvis_kodat_undermatt_ger_proportionellt_bidrag() -> None:
    covered, total = score.weighted_depth_coverage({"a": {"x1"}}, CODABLE, W, DEN)
    assert covered == pytest.approx(40.0 / 3)
    assert total == 100.0
    covered2, _ = score.weighted_depth_coverage({"a": {"x1", "x2"}}, CODABLE, W, DEN)
    assert covered2 == pytest.approx(80.0 / 3)


def test_wdc_typ_i_flera_undermatt_bidrar_i_varje() -> None:
    # koldioxidskatt-fallet (spec §3.1): samma typ kodbar i a OCH b -> en kodad ståndpunkt
    # höjer djupet i båda, men aldrig dubbelt inom samma undermått
    codable = {"a": {"x"}, "b": {"x"}, "c": {"z"}, "d": set()}
    coded = {"a": {"x"}, "b": {"x"}}
    covered, total = score.weighted_depth_coverage(coded, codable, W, DEN)
    assert (covered, total) == (70.0, 100.0)  # 40 + 30, inte 40 eller 140


def test_wdc_kodad_typ_utanfor_kodbar_mangd_eller_namnare_bidrar_inte() -> None:
    # typ utanför T_s ignoreras (K_s = K ∩ T_s) ...
    assert score.weighted_depth_coverage({"a": {"q"}}, CODABLE, W, DEN) == (0.0, 100.0)
    # ... och ett fullkodat undermått UTANFÖR nämnaren (target-only, spec §3.6) räknas inte
    codable = dict(CODABLE, t={"tt"})
    assert score.weighted_depth_coverage({"t": {"tt"}}, codable, W, DEN) == (0.0, 100.0)


def test_wdc_monotoni_i_antal_kodade_typer() -> None:
    prev = -1.0
    for coded_a in (set(), {"x1"}, {"x1", "x2"}, {"x1", "x2", "x3"}):
        covered, _ = score.weighted_depth_coverage({"a": coded_a, "b": {"y"}}, CODABLE, W, DEN)
        assert covered > prev
        prev = covered


# --- nämnaren: B och D delar definition (spec §3.4/§6.2) -------------------------------


def test_b_och_d_delar_namnarfunktion() -> None:
    """B:s nämnare ÄR D:s — samma funktionsobjekt, ingen duplicerad definition."""
    assert scorerun._d_denominator_submeasures is scorerun._non_target_submeasures


# --- T_s ur liggaren: per undermått, dedup, multi-undermått (spec §3.1, anti-gaming §7) --


def test_b_codable_typ_i_flera_undermatt_koldioxidskatt() -> None:
    t = scorerun._b_codable_types_by_submeasure()["klimat"]
    assert "koldioxidskatt" in t["utslappsminskningar"]      # via territoriella_utslapp
    assert "koldioxidskatt" in t["kostnadseffektivitet"]     # via utslappsminskning_per_krona


def test_b_codable_dedup_av_dubblerad_post_inom_undermatt(monkeypatch: pytest.MonkeyPatch) -> None:
    """Dubblerad policy_type i samma undermått (två liggarposter, samma typ+indikator)
    ändrar varken T_s eller djupet — set-semantik (spec §7)."""
    before = scorerun._b_codable_types_by_submeasure()
    led = copy.deepcopy(config.evidence_ledger())
    dup = copy.deepcopy(next(
        e for e in led["entries"]
        if e["policy_type"] == "koldioxidskatt" and e["indicator"] == "territoriella_utslapp"
    ))
    led["entries"].append(dup)
    monkeypatch.setattr(config, "evidence_ledger", lambda: led)
    assert scorerun._b_codable_types_by_submeasure() == before


def test_b_codable_respekterar_kodbarhetsreglerna() -> None:
    """Samma kodbarhetsregler som legacy-nämnaren cov_den: coverage_exclude och inerta
    (signed_direction 0) typer ingår aldrig i något T_s."""
    excluded = set(config.scoring()["B_evidens"].get("coverage_exclude", []))
    assert excluded, "fixturen förutsätter minst en coverage_exclude-post"
    all_types = {
        t for subs in scorerun._b_codable_types_by_submeasure().values()
        for ts in subs.values() for t in ts
    }
    assert not (all_types & excluded)


# --- flaggformatet är LÅST och deterministiskt (spec §4) -------------------------------


def test_flaggformat_last_och_deterministiskt() -> None:
    assert scorerun._b_coverage_flag(86.66666666666667, 100.0) == "B_coverage_86.7/100"
    assert scorerun._b_coverage_flag(73.0, 73.0) == "B_coverage_73/73"  # aldrig '73.0'
    assert scorerun._b_coverage_flag(42.5, 100.0) == "B_coverage_42.5/100"
    assert scorerun._b_coverage_flag(0.0, 100.0) == "B_coverage_0/100"


# --- config-validering: ogiltigt läge hard-failar (spec §7) ----------------------------


def _set_mode(monkeypatch: pytest.MonkeyPatch, mode: str) -> None:
    sc = copy.deepcopy(config.scoring())
    sc["B_evidens"]["coverage_mode"] = mode
    monkeypatch.setattr(config, "scoring", lambda: sc)


def test_ogiltig_coverage_mode_hard_failar_i_validate(monkeypatch: pytest.MonkeyPatch) -> None:
    _set_mode(monkeypatch, "submeasure_weighted_depth")  # felstavning -> ALDRIG tyst legacy
    with pytest.raises(config.ConfigError, match="coverage_mode"):
        config.validate()


def test_giltiga_coverage_modes_validerar(monkeypatch: pytest.MonkeyPatch) -> None:
    for mode in ("policy_type_count", "weighted_submeasure_depth"):
        _set_mode(monkeypatch, mode)
        config.validate()


def test_ogiltig_coverage_mode_hard_failar_i_build(monkeypatch: pytest.MonkeyPatch) -> None:
    _set_mode(monkeypatch, "antal")
    con = _seed_con()
    with pytest.raises(config.ConfigError, match="coverage_mode"):
        scorerun.build(con)
    con.close()


# --- end-to-end: legacy byte-identisk, nya modens värden, formelekvivalens -------------


def _seed_con():
    con = warehouse.connect(":memory:")
    warehouse.upsert(con, "responsibility", government.build_national_responsibility())
    return con


def _b_cells(scores: dict) -> dict[tuple[str, str], dict]:
    return {(p, c): scores[p][c] for p in scores for c in scores[p]}


def test_default_ar_legacy_och_byte_identisk_med_explicit_mode(monkeypatch: pytest.MonkeyPatch) -> None:
    """Committad config (coverage_mode: policy_type_count) ger EXAKT samma utdata som
    explicit legacy-override, och legacy-flaggan förblir antalsbaserad (heltal/heltal)."""
    assert config.scoring()["B_evidens"]["coverage_mode"] == "policy_type_count"
    con = _seed_con()
    base = scorerun.build(con)["scores"]["scores"]
    _set_mode(monkeypatch, "policy_type_count")
    explicit = scorerun.build(con)["scores"]["scores"]
    assert explicit == base
    cov_flags = [
        f for cell in _b_cells(base).values()
        for f in cell["flags"] if f.startswith("B_coverage_")
    ]
    assert cov_flags
    assert all(re.fullmatch(r"B_coverage_\d+/\d+", f) for f in cov_flags)
    con.close()


def test_ny_mode_ger_viktad_djuptackning_handraknat(monkeypatch: pytest.MonkeyPatch) -> None:
    """Handräknade celler ur dagens config (spec §2/§5; uppdateras vid liggardrift —
    täckningsdrift ska aldrig passera tyst, spec §7)."""
    _set_mode(monkeypatch, "weighted_submeasure_depth")
    con = _seed_con()
    sc = scorerun.build(con)["scores"]["scores"]
    # C/integration — flaggskeppsfallet: B_raw = 5.00 men B-väggarna boendesegregation (20)
    # + normer_tillit (15) stannar i nämnaren -> cov_B = 0.65, B = 2.5 + 2.5*0.65 = 4.125
    c_int = sc["C"]["integration"]
    assert "B_coverage_65/100" in c_int["flags"]
    assert c_int["components"]["B"] == pytest.approx(4.125, abs=1e-3)
    # M/demokrati: 86,666... skrivs deterministiskt '86.7' (LÅST format, spec §4)
    assert "B_coverage_86.7/100" in sc["M"]["demokrati"]["flags"]
    # ekonomi: target-only (12+15) ur nämnaren -> full täckning '73/73', aldrig '73.0'
    s_eco = sc["S"]["ekonomi"]
    assert "B_coverage_73/73" in s_eco["flags"]
    assert not any("73.0" in f for f in s_eco["flags"])
    # MP/forsvar: ekonomisk_ambition fullt kodad (25) + nato_ukraina 1/2 kodbara typer
    # (dca_avtal_usa kodad opposes, nato_medlemskap=none -> 15 * 1/2 = 7.5; B3
    # dca_avtal_usa 2026-06-12) -> cov_B = 0.325 < 0.5 -> tunn täckning, säkerhet låg
    mp_for = sc["MP"]["forsvar"]
    assert "B_coverage_32.5/100" in mp_for["flags"]
    assert "B_thin_coverage" in mp_for["flags"]
    assert mp_for["confidence"]["B"] == "low"
    con.close()


def _independent_cov_b(party: str, cat: str) -> tuple[float, float]:
    """Oberoende cov_B-omräkning per cell (testets egen kodade-mängd ur config)."""
    signed = config.claims()["aggregation"]["signed_direction"]
    b_ex = set(config.scoring()["B_evidens"].get("coverage_exclude", []))
    codable_flat = {
        e["policy_type"] for e in config.evidence_ledger()["entries"]
        if e["category"] == cat and signed.get(e["direction"], 0) != 0
        and e["policy_type"] not in b_ex
    }
    coded = {
        pos["policy_type"] for pos in config.party_positions()["entries"]
        if pos["party"] == party and pos["policy_type"] in codable_flat
    }
    t_by_sub = scorerun._b_codable_types_by_submeasure().get(cat, {})
    weights = scorerun._submeasure_weights()[cat]
    return score.weighted_depth_coverage(
        {s: ts & coded for s, ts in t_by_sub.items()},
        t_by_sub, weights, scorerun._non_target_submeasures()[cat],
    )


def test_formelekvivalens_mellan_moderna(monkeypatch: pytest.MonkeyPatch) -> None:
    """Samma B_raw i båda moderna -> B_ny = 2.5 + (B_legacy - 2.5) * cov_B / cov_pt för
    varje cell med täckning i båda (spec §3.3: endast krympfaktorn byts). cov_B räknas
    oberoende; cov_pt läses ur legacy-flaggan. Låser också att cov_B = 1 <=> B_just = B_raw
    och att flaggan matchar den oberoende omräkningen."""
    con = _seed_con()
    legacy = scorerun.build(con)["scores"]["scores"]
    _set_mode(monkeypatch, "weighted_submeasure_depth")
    new = scorerun.build(con)["scores"]["scores"]
    checked = 0
    for (p, c), leg_cell in _b_cells(legacy).items():
        leg_flag = next((f for f in leg_cell["flags"] if f.startswith("B_coverage_")), None)
        if leg_flag is None:
            continue  # B_no_party_evidence i legacy -> ingen jämförbar krympning
        num, den = (int(x) for x in leg_flag.removeprefix("B_coverage_").split("/"))
        covered_w, total_w = _independent_cov_b(p, c)
        cov_b = covered_w / total_w
        new_cell = new[p][c]
        if cov_b == 0:
            assert "B_no_party_evidence" in new_cell["flags"]
            continue
        assert scorerun._b_coverage_flag(covered_w, total_w) in new_cell["flags"]
        b_leg, b_new = leg_cell["components"]["B"], new_cell["components"]["B"]
        assert b_new == pytest.approx(2.5 + (b_leg - 2.5) * cov_b / (num / den), abs=5e-3)
        # tunn täckning mäts på cov_B i nya moden
        thr = float(config.scoring()["B_evidens"]["thin_coverage_threshold"])
        assert ("B_thin_coverage" in new_cell["flags"]) == (cov_b < thr)
        checked += 1
    assert checked >= 40  # 8 partier x 7 kategorier, nästan alla celler har B-evidens
    con.close()


def test_kodad_typ_mot_target_only_undermatt_gatear_pa_cov_b(monkeypatch: pytest.MonkeyPatch) -> None:
    """Spec §3.6-kantfallet: en kodad typ vars indikator ligger i ett target-only-undermått
    ger b_inputs != tomt men cov_B = 0 -> nya modens gate faller till neutral
    B_no_party_evidence (legacy hade gett betyg, eftersom cov_den är undermåttsblind)."""
    led = copy.deepcopy(config.evidence_ledger())
    led["entries"].append({
        "category": "ekonomi", "indicator": "inflation",  # target-only-undermåttet
        "policy_type": "test_targetonly_typ", "direction": "positive",
        "evidence_level": "authority_evaluation", "effect_strength": "medium",
        "confidence": "medium", "source": "test",
    })
    pos = copy.deepcopy(config.party_positions())
    pos["entries"] = [{"party": "S", "policy_type": "test_targetonly_typ",
                       "stance": "supports", "source": "test"}]
    monkeypatch.setattr(config, "evidence_ledger", lambda: led)
    monkeypatch.setattr(config, "party_positions", lambda: pos)

    con = _seed_con()
    _set_mode(monkeypatch, "policy_type_count")
    leg = scorerun.build(con)["scores"]["scores"]["S"]["ekonomi"]
    assert any(f.startswith("B_coverage_") for f in leg["flags"])  # legacy: typen "täcker"

    _set_mode(monkeypatch, "weighted_submeasure_depth")
    new = scorerun.build(con)["scores"]["scores"]["S"]["ekonomi"]
    assert "B_no_party_evidence" in new["flags"]
    assert new["components"]["B"] == 2.5
    assert not any(f.startswith("B_coverage_") for f in new["flags"])
    assert new["confidence"]["B"] == "low"
    con.close()
