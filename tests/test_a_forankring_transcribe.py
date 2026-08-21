"""Golden-tester för transkriberingsverktygets rena parsers (ADR 0005, biljett #21).

Verktyget läser bet. FiU1 i två format och tre layouter. Fixturerna nedan är avskrivna ur de
faktiska betänkandena, så en layoutändring i källan faller här och inte tyst i configen.
Ingen livedata och ingen fil-IO.
"""

from __future__ import annotations

import pytest

from pipeline.tools import a_forankring_transcribe as t


def test_dok_id_foljer_riksmotesserien() -> None:
    assert t.dok_id(2024) == "HB01FiU1"        # riksmöte 2023/24
    assert t.dok_id(2022) == "H901FiU1"
    assert t.dok_id(2019) == "H601FiU1"
    assert t.dok_id(2013) == "H001FiU1"
    assert t.dok_id(2011) == "GY01FiU1"        # bokstavsgruppen före H


def test_dok_id_utanfor_serien_ar_hard_fail() -> None:
    with pytest.raises(ValueError):
        t.dok_id(1999)


@pytest.mark.parametrize(("raw", "want"), [
    ("19 070 363", 19070363.0),
    ("19 070 363", 19070363.0),      # hårt mellanslag ur HTML
    ("±0", 0.0),
    ("−385", -385.0),                          # U+2212
    ("–395", -395.0),                          # U+2013
    ("+364", 364.0),
    ("Rikets styrelse", None),
    ("", None),
])
def test_parse_amount(raw: str, want: float | None) -> None:
    assert t.parse_amount(raw) == want


def test_caption_key_tal_losa_mellanslag_i_kallan() -> None:
    """Betänkandenas HTML bär "Regeringens f örslag" och "20 20" efter konverteringen."""
    assert t.caption_key("Regeringens f örslag till utgiftsramar 20 20") == \
        t.caption_key("Regeringens förslag till utgiftsramar 2020")


_HTML_TABLE = """
<table>
 <tr><td>Utgiftsområde</td><td>Avvikelse</td><td>Utskottets förslag</td></tr>
 <tr><td>1</td><td>Rikets styrelse</td><td>−30 000</td><td>17 238 338</td></tr>
 <tr><td>2</td><td>Samhällsekonomi och finansförvaltning</td><td>±0</td><td>17 971 183</td></tr>
</table>
"""


def test_html_tabellrad_tar_sista_beloppet() -> None:
    """Tabellen visar först en avvikelse och sedan den absoluta ramen. Den senare gäller."""
    rows = t.uo_rows_from_html_table(_HTML_TABLE)
    assert rows[1] == ("Rikets styrelse", 17238338.0)
    assert rows[2][1] == 17971183.0


def _full_table(caption_inside: str = "") -> str:
    """En tabell med alla 27 utgiftsområdena, valfritt med rubriken som första rad."""
    head = f"<tr><td>{caption_inside}</td></tr>" if caption_inside else ""
    rows = "".join(
        f"<tr><td>{n}</td><td>Utgiftsområde {n}</td><td>±0</td><td>{n} 000 000</td></tr>"
        for n in range(1, 28)
    )
    return f"<table>{head}<tr><td>Utgiftsområde</td><td>Förslag</td></tr>{rows}</table>"


@pytest.mark.parametrize("where", ["fore", "i_tabellen"])
def test_html_rubriken_lases_bade_fore_och_i_tabellen(where: str) -> None:
    """Nyare betänkanden har rubriken före tabellen, äldre som tabellens första rader."""
    caption = "Utskottets förslag till utgiftsramar 2022"
    html = (f"<p>{caption}</p>" + _full_table()) if where == "fore" else _full_table(caption)
    captions = [c for c, _rows in t.html_uo_tables(html)]
    assert captions, "tabellen med 27 utgiftsområden hittades inte"
    assert any(t.caption_key(caption) in t.caption_key(c) for c in captions)


def test_html_tabell_med_farre_an_27_utgiftsomraden_raknas_inte() -> None:
    """En delmängd är inte rambeslutstabellen och får aldrig bli en förankring."""
    assert t.html_uo_tables(_HTML_TABLE) == []


# Numret på egen rad (bet. 2021/22:FiU1, bilaga 4).
_PDF_NUMBER_OWN_LINE = """Utgiftsområde
Avvikelse från
regeringen
Utskottets
förslag
1
Rikets styrelse
−30 000
17 238 338
2
Samhällsekonomi och finansförvaltning
±0
17 971 183
3
Skatt, tull och exekution
100 000
12 829 734
"""

# Numret först på namnraden (bet. 2014/15:FiU1, bilaga 3).
_PDF_NUMBER_ON_NAME_LINE = """Utgiftsområde
Avvikelse från
regeringen
Reservanternas
förslag
1 Rikets styrelse
–214 809
12 198 574
2 Samhällsekonomi och finansförvaltning
209 963
14 799 753
3 Skatt, tull och exekution
–7 195
10 573 781
Summa utgiftsområden
890 900
"""


@pytest.mark.parametrize("page", [_PDF_NUMBER_OWN_LINE, _PDF_NUMBER_ON_NAME_LINE])
def test_pdf_bada_layouterna_lases(page: str) -> None:
    rows = t.uo_rows_from_pdf_page(page)
    assert set(rows) == {1, 2, 3}
    assert rows[1][0] == "Rikets styrelse"
    assert rows[3][0] == "Skatt, tull och exekution"


def test_pdf_summaraden_hamnar_inte_i_sista_utgiftsomradet() -> None:
    """Texten efter beloppen tillhör nästa rad. Annars blev UO3 = 890 900."""
    rows = t.uo_rows_from_pdf_page(_PDF_NUMBER_ON_NAME_LINE)
    assert rows[3][1] == 10573781.0


def test_pdf_ett_belopp_startar_aldrig_ett_utgiftsomrade() -> None:
    """Beloppet "12 198 574" får inte starta utgiftsområde 12 när 11 nyss stängdes."""
    page = "11\nEkonomisk trygghet vid ålderdom\n±0\n12 198 574\n"
    rows = t.uo_rows_from_pdf_page(page, start_at=10)
    assert set(rows) == {11}
    assert rows[11][1] == 12198574.0


def test_pdf_start_at_bar_rakningen_over_en_sidbrytning() -> None:
    page = "22\nKommunikationer\n±0\n48 870 983\n"
    assert set(t.uo_rows_from_pdf_page(page, start_at=21)) == {22}
    assert t.uo_rows_from_pdf_page(page) == {}      # utan start_at börjar räkningen på 1
