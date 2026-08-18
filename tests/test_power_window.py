"""Issue #14: maktandelen får inte tillgodoräkna en regering dagar den ännu inte suttit.

WINDOW_END är mandatperiodens FORMELLA slut (valdagen) och ligger i framtiden under hela
mandatperioden. Maktandelen (C, `government_fractions`) räknade förut både täljare och nämnare
dit, så den sittande regeringen fick maktdagar den inte suttit och alla fraktioner späddes av en
framtida nämnare. Gränsen går nu vid POWER_WINDOW_END, sista dagen i sista avslutade
observationsåret.

Den NATIONELLA maktandelens rangordning är identisk under båda gränserna. Betygen står däremot
INTE still: components.C är inte den nationella fraktionen utan en per-kategori-blandning av
nationell och subnationell makt (`category_c`), och i trygghet korsar SD och C när den nationella
termen rör sig olika mycket per parti. C väger dessutom fortfarande 0,15 i `config/scoring.yaml`
— ADR 0002:s viktslice har inte körts — så korsningen når kategoribetyget:
C/trygghet 3,036 -> 3,143 och SD/trygghet 3,296 -> 3,189. Totalrankingen och trygghets interna
ordning står still. Testerna nedan pinnar gränsen, den nationella rangstabiliteten och att
konstanten inte hamnar på efterkälken när lagret får ett nytt avslutat år.
"""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from pipeline import config, scorerun, warehouse


def test_power_window_end_ligger_i_det_forflutna_och_fore_window_end() -> None:
    """Invarianten buggen bröt. WINDOW_END får vara framtida, maktandelens gräns aldrig."""
    assert scorerun.POWER_WINDOW_END == date(2025, 12, 31)
    assert scorerun.POWER_WINDOW_END < scorerun.WINDOW_END
    assert scorerun.POWER_WINDOW_END <= date.today()


def test_maktandelens_namnare_slutar_vid_power_window_end() -> None:
    """Nämnaren är fönstret 2014-10-03 -> POWER_WINDOW_END, inte -> valdagen."""
    starts = [scorerun._as_date(gp["start"]) for gp in config.mappings()["government_periods"]]
    win_start = min(starts)
    stop = scorerun.POWER_WINDOW_END + timedelta(days=1)   # halvöppen gräns, sista dagen räknas
    total = (stop - win_start).days
    frac = scorerun.government_fractions()
    # S satt hela 2014-10-03 -> 2022-10-18 (de tre första perioderna), utan avbrott.
    s_days = (date(2022, 10, 18) - win_start).days
    assert abs(frac["S"] - s_days / total) < 1e-12
    # Den sittande regeringen räknas till och med POWER_WINDOW_END, inte längre.
    m_days = (stop - date(2022, 10, 18)).days
    assert abs(frac["M"] - m_days / total) < 1e-12
    assert all(0.0 <= v <= 1.0 for v in frac.values())


def test_ingen_regering_tillgodoraknas_dagar_efter_sista_avslutade_aret() -> None:
    """Summan av alla maktdagar får aldrig överstiga fönstret. Buggen sprängde den gränsen."""
    frac = scorerun.government_fractions()
    # M och KD sitter bara i den nuvarande regeringen, så deras andel ÄR fönstrets svans.
    # (L räknas högre: L var stödparti 2019-2021 och bär ett halvvägt påslag därifrån.)
    assert frac["M"] == frac["KD"]
    assert frac["L"] > frac["M"]
    stop = scorerun.POWER_WINDOW_END + timedelta(days=1)
    win_start = min(scorerun._as_date(gp["start"])
                    for gp in config.mappings()["government_periods"])
    # Gränsen är flyttad bakåt: både svansen och nämnaren är kortare än med valdagen som slut.
    assert frac["M"] == (stop - date(2022, 10, 18)).days / (stop - win_start).days
    bugged = ((scorerun.WINDOW_END - date(2022, 10, 18)).days
              / (scorerun.WINDOW_END - win_start).days)
    assert frac["M"] < bugged           # buggen gav M för många maktdagar
    assert frac["S"] + frac["M"] <= 1.0 + 1e-12


def test_maktvikten_stannar_vid_sista_avslutade_aret() -> None:
    """year_power_fractions ger ingen makt år 2026: inget avslutat observationsår når dit."""
    yp = scorerun.year_power_fractions()
    assert yp[2025]["M"] == 1.0
    assert yp.get(2026, {}) == {}
    # D läser aldrig 2026 ändå (lag 1), så tomheten är ofarlig - men den ska vara tom.
    assert max(y for y, f in yp.items() if f) == 2025


def test_rangordningen_ar_identisk_under_bada_granserna() -> None:
    """Härledningen bakom 'rättningen syns inte i utdatan': C rangnormaliseras.

    En tidigare gräns tar dagar från de fyra som sitter nu och krymper nämnaren för alla, så
    grupperna glider isär men vänder aldrig. Går den här sönder är härledningen fel.
    """
    now_frac = scorerun.government_fractions()
    orig = scorerun.POWER_WINDOW_END
    try:
        scorerun.POWER_WINDOW_END = scorerun.WINDOW_END  # den gamla, buggiga gränsen
        before_frac = scorerun.government_fractions()
    finally:
        scorerun.POWER_WINDOW_END = orig
    # Grinden mot ett tomt test: gränsen MASTE påverka fraktionerna, annars jämför vi ett värde
    # med sig självt och testet kan aldrig falla.
    assert before_frac != now_frac
    assert before_frac["M"] > now_frac["M"]      # buggen gav sittande regering fler maktdagar
    order = lambda d: sorted(d, key=lambda p: (-d[p], p))  # noqa: E731
    assert order(now_frac) == order(before_frac)


def test_konstanten_hanger_med_nar_lagret_far_ett_nytt_avslutat_ar() -> None:
    """Grinden mot en handsatt konstant som glöms bort.

    POWER_WINDOW_END är satt för hand med flit: `data_freshness()` avgör "avslutat år" mot
    today.year och skulle göra maktandelen beroende av körtidpunkten. Priset är att konstanten
    kan hamna på efterkälken. Höjs den inte när 2026 stängs får sittande regering inget
    ansvarsår för 2026, och förändringen 2026 -> 2027 hoppas över i attribute_series. Testet
    är den enda automatiska påminnelsen. Faller det: höj POWER_WINDOW_END till fresh.as_of.
    """
    # Enda testet i sviten som läser det RIKTIGA lagret. Filen är gitignorerad (*.duckdb), så
    # CI har inget lager och grinden kan bara gå lokalt, där konstanten faktiskt underhålls.
    if not warehouse.WAREHOUSE_PATH.exists():
        pytest.skip("inget byggt lager (CI kör utan data/warehouse.duckdb)")
    con = warehouse.connect(read_only=True)
    fresh = scorerun.data_freshness(con, today=date.today())
    con.close()
    if fresh.as_of is None:
        pytest.skip("tomt lager, inget avslutat observationsår att jämföra mot")
    assert scorerun.POWER_WINDOW_END.isoformat() == fresh.as_of, (
        f"lagret når {fresh.as_of} men POWER_WINDOW_END står på "
        f"{scorerun.POWER_WINDOW_END.isoformat()} — höj konstanten (biljett #14)"
    )


def test_meta_exponerar_maktandelens_fonsterslut() -> None:
    """Den enda observerbara följden av hela rättningen."""
    con = warehouse.connect(":memory:")
    warehouse.upsert(con, "observations", [{
        "id": "obs:test:arbetsloshet:2025", "category": "ekonomi",
        "submeasure": "sysselsattning_arbetsloshet", "indicator": "arbetsloshet",
        "period": "2025", "value": 6.0, "unit": "%", "geography": "Riket",
        "source_ref": "scb:test:2025",
    }])
    meta = scorerun.build(con)["scores"]["meta"]
    con.close()
    assert meta["power_window_end"] == "2025-12-31"
    assert meta["power_window_end"] != meta["window_end"]
    assert meta["window"] == "2014-2026"  # fönstersträngen står kvar oförändrad
