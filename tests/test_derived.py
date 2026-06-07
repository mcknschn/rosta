"""Offline-test för härledda indikatorer (pipeline.derived) — ren gap/ratio-beräkning, ingen nätverk.

Facit med påhittade men realistiska värden. Verifierar: rätt differens/kvot, ingen imputation
(bara år med BÅDA föräldrarna), hård fail vid <2 år, rimlighetsgrind på nivån (fångar enhetsbyte),
kanoniska indikatorer/kategorier, och source_ref-/id-form med dubbel provenans.
"""

from __future__ import annotations

import pytest

from pipeline import config, derived

# Spec-uppslag (ordningsoberoende) så testerna inte beror på positionen i DERIVED.
_GAP = next(d for d in derived.DERIVED if d["indicator"] == "sysselsattningsgap_inrikes_utrikes")
_PROD = next(d for d in derived.DERIVED if d["indicator"] == "produktivitet")
_INC = next(
    d for d in derived.DERIVED if d["indicator"] == "hushallens_reala_disponibla_inkomst"
)


def test_compute_gap_subtraherar_och_skar_ojamna_ar() -> None:
    """gap = a−b, avrundat 2 dec; år som saknar någon förälder utelämnas (ingen imputation)."""
    inrikes = {"2022": 82.5, "2023": 83.0, "2024": 82.857}
    utrikes = {"2022": 67.1, "2023": 68.4}  # saknar 2024
    assert derived.compute_gap(inrikes, utrikes) == {"2022": 15.4, "2023": 14.6}


def test_compute_ratio_dividerar_skalar_och_hoppar_noll() -> None:
    """ratio = a/b·scale, avrundat 2 dec; delar bara gemensamma år och hoppar b==0 (ingen div0)."""
    bnp = {"2022": 5341042.0, "2023": 5330143.0, "2024": 5436222.0}
    timmar = {"2022": 855459.0, "2023": 864486.0, "2025": 0.0}  # 2024 saknas, 2025 är 0
    assert derived.compute_ratio(bnp, timmar, 100.0) == {"2022": 624.35, "2023": 616.57}


def test_rows_for_gap_bygger_kanoniska_rader_med_dubbel_provenans() -> None:
    rows = derived._rows_for(_GAP, {"2022": 82.5, "2023": 83.0}, {"2022": 67.1, "2023": 68.4})
    assert [r["indicator"] for r in rows] == [_GAP["indicator"], _GAP["indicator"]]
    assert all(r["category"] == "integration" for r in rows)
    assert all(r["geography"] == "Riket" for r in rows)
    r0 = rows[0]
    assert r0["id"] == "obs:derived:sysselsattningsgap_inrikes_utrikes:2022"
    assert r0["source_ref"] == "derived:scb:TAB6529:SYSP(13-23):2022"
    assert r0["value"] == 15.4


def test_rows_for_produktivitet_kvot_kanonisk_och_dubbel_provenans() -> None:
    """Produktivitet = BNP/timmar·100; rader är kanoniska (ekonomi) och citerar BÅDA tabellerna."""
    rows = derived._rows_for(_PROD, {"2022": 5341042.0, "2023": 5330143.0},
                             {"2022": 855459.0, "2023": 864486.0})
    assert all(r["category"] == "ekonomi" and r["submeasure"] == "bnp_produktivitet" for r in rows)
    r0 = rows[0]
    assert r0["id"] == "obs:derived:produktivitet:2022"
    assert r0["source_ref"] == "derived:scb:TAB3610(BNPM,fast2020)/TAB5622(hela_ekonomin,timmar):2022"
    assert r0["value"] == 624.35  # kr/timme, fasta 2020-priser


def test_compute_index_kumulerar_tillvaxttakt_och_bevarar_tecken() -> None:
    """index[y] = index[y-1]·(1+g[y]/100), nivå före första året = base; tecknet på
    årsförändringen = tecknet på tillväxttakten (det enda D använder)."""
    growth = {"2021": 4.3, "2022": 1.7, "2023": -1.1}
    idx = derived.compute_index(growth, 100.0)
    assert idx == {"2021": 104.3, "2022": 106.07, "2023": 104.91}
    # 2023 hade NEGATIV real tillväxt -> indexet ska FALLA (real-inkomstfall), tecknet bevaras
    assert idx["2023"] < idx["2022"]
    assert idx["2022"] > idx["2021"]


def test_rows_for_index_kanonisk_enkel_operand_dubbel_provenans() -> None:
    """index-op tar EN operand (b=None); rader är kanoniska (ekonomi/realloner_hushall) + citerar källan."""
    rows = derived._rows_for(_INC, {"2021": 4.3, "2022": 1.7})
    assert all(r["category"] == "ekonomi" and r["submeasure"] == "realloner_hushall" for r in rows)
    r0 = rows[0]
    assert r0["id"] == "obs:derived:hushallens_reala_disponibla_inkomst:2021"
    assert r0["source_ref"] == "derived:scb:TAB4592(B6nRealGrowth,S14,kumul.index):2021"
    assert r0["value"] == 104.3


def test_gap_op_kraver_tva_operander() -> None:
    """gap/ratio utan andra operanden (b=None) ska faila högt — inte tyst ge fel serie."""
    with pytest.raises(ValueError, match="kräver två operander"):
        derived._series_for(_GAP, {"2022": 82.5}, None)


def test_for_fa_gemensamma_ar_ger_hard_fail() -> None:
    """Om bara ett gemensamt år finns ska byggaren faila högt (serien ej meningsfull)."""
    with pytest.raises(ValueError, match="<2 år"):
        derived._rows_for(_GAP, {"2024": 82.0}, {"2024": 67.0})


def test_rimlighetsgrind_failar_vid_enhetsbyte() -> None:
    """Om nivån hamnar utanför spec:ens rimliga band (t.ex. SCB byter timenhet 100x) -> hård fail.

    Här är nämnaren 100x för stor -> ~6 kr/timme, långt under produktivitetsbandet [100, 5000]."""
    with pytest.raises(ValueError, match="rimligt band"):
        derived._rows_for(_PROD, {"2022": 5341042.0, "2023": 5330143.0},
                          {"2022": 85545900.0, "2023": 86448600.0})


def test_indicators_ar_kanoniska() -> None:
    """derived.INDICATORS pekar bara på kanoniska indikatorer i categories.yaml."""
    allinds = {
        (cat["id"], ind["id"])
        for cat in config.categories()["categories"]
        for ind in cat.get("indicators", [])
    }
    for d in derived.DERIVED:
        assert (d["category"], d["indicator"]) in allinds
