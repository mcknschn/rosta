"""Offline golden-test för Försvarsmakten-serien (personal_varnpliktiga, transkriberad config).

Indikatorn personal_varnpliktiga = antal värnpliktiga som påbörjade grundutbildning per kalenderår
(config/personal_varnpliktiga.yaml, ur Försvarsmaktens årsredovisning, korsverifierad mot
Pliktverkets inskrivna). Försvarets FÖRSTA D-serie. Pinnar årstotalerna + kontrollerar radform,
kanonisk indikator och att audit-invarianterna håller (tools/varnpliktiga_audit). Ingen nätverkstrafik.
"""

from __future__ import annotations

from pipeline import config
from pipeline.sources import forsvarsmakten
from pipeline.tools import varnpliktiga_audit

# Facit: antal påbörjade GU (FM ÅR), nationell siffra per år, transkriberade 2026-06-07.
GOLDEN = {
    "2018": 3750, "2019": 4500, "2020": 4917, "2021": 5873,
    "2022": 5475, "2023": 6320, "2024": 7300, "2025": 8136,
}


def test_serie_matchar_pinnade_varden() -> None:
    rows = forsvarsmakten.build_personal_varnpliktiga_observations()
    by_year = {r["period"]: int(r["value"]) for r in rows}
    assert by_year == GOLDEN


def test_borjar_2018_ej_tidigare() -> None:
    """Serien börjar 2018 (värnplikten återaktiverad); inga värden före (måttet existerar ej)."""
    rows = forsvarsmakten.build_personal_varnpliktiga_observations()
    assert min(r["period"] for r in rows) == "2018"


def test_radform_kanonisk() -> None:
    r = next(r for r in forsvarsmakten.build_personal_varnpliktiga_observations() if r["period"] == "2024")
    assert r["indicator"] == "personal_varnpliktiga"
    assert r["category"] == "forsvar"
    assert r["submeasure"] == "militar_formaga"
    assert r["geography"] == "Riket"
    assert r["id"] == "obs:forsvarsmakten:personal_varnpliktiga:2024"
    assert r["source_ref"] == "forsvarsmakten:personal_varnpliktiga:2024"
    assert "personal_varnpliktiga" in forsvarsmakten.INDICATORS


def test_builder_ren_funktion_injicerad_cfg() -> None:
    """Ren funktion: värdet = entry['value'] för en injicerad cfg (ingen fil-IO)."""
    cfg = {
        "indicator": "personal_varnpliktiga", "category": "forsvar",
        "submeasure": "militar_formaga", "unit": "antal",
        "years": {
            2018: {"value": 3750, "source": "a"},
            2019: {"value": 4500, "source": "b"},
        },
    }
    rows = forsvarsmakten.build_personal_varnpliktiga_observations(cfg)
    assert [(r["period"], r["value"]) for r in rows] == [("2018", 3750.0), ("2019", 4500.0)]


def test_indikator_kanonisk_forsvar_riktning_up() -> None:
    forsvar = next(c for c in config.categories()["categories"] if c["id"] == "forsvar")
    ind = next(i for i in forsvar["indicators"] if i["id"] == "personal_varnpliktiga")
    assert ind["direction"] == "up"
    assert ind["submeasure"] == "militar_formaga"


def test_config_har_kalla_per_ar() -> None:
    """Varje år har ett heltalsvärde och en FM-källa (ingen tyst siffra)."""
    cfg = config.personal_varnpliktiga()
    assert cfg["indicator"] == "personal_varnpliktiga"
    for year, e in cfg["years"].items():
        assert isinstance(e["value"], int), f"{year}: värde ej heltal"
        assert str(e["source"]).startswith("https://"), f"{year}: saknar källa"


def test_audit_invarianter_haller() -> None:
    """Integritets-audit (konsekutiva år, enda dubbelbekräftade nedgången 2021->2022,
    Pliktverket-korsverifiering inom tolerans) ska passera utan avvikelser."""
    assert varnpliktiga_audit.audit() == []


def test_audit_fangar_ovantad_nedgang() -> None:
    """En andra, odokumenterad nedgång (som kan flippa ett D-tecken) ska flaggas av auditen."""
    bad = {
        "indicator": "personal_varnpliktiga", "category": "forsvar",
        "submeasure": "militar_formaga", "unit": "antal",
        "years": {
            2018: {"value": 3750, "source": "a"},
            2019: {"value": 3000, "source": "b"},  # odokumenterad nedgång
            2020: {"value": 4917, "source": "c"},
            2021: {"value": 5873, "source": "d"},
            2022: {"value": 5475, "source": "e"},
        },
    }
    assert varnpliktiga_audit.audit(bad)  # icke-tom -> avvikelse upptäckt
