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

# Facit: antal påbörjade GU (FM ÅR), nationell siffra per år. PDF-verifierad 2026-06-08 direkt ur
# FM ÅR (2020 korr. 4917->4915 inkl. HAGS, FM ÅR 2022 bil.1 Tab6; 2024 korr. 7300->7343, FM ÅR 2024
# bil.1 Tab3). Korrigeringarna ändrar inga D-tecken (serien monoton upp utom 2021->2022).
GOLDEN = {
    "2018": 3750, "2019": 4500, "2020": 4915, "2021": 5873,
    "2022": 5475, "2023": 6320, "2024": 7343, "2025": 8136,
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


# --- personalstyrka_kontinuerligt (FM ÅR bilaga Tabell 1, 'Summa kontinuerligt tjänstgörande') ---

# Facit: stående personalvolym per 31 dec, korsverifierad ur FM ÅR-bilagorna 2026-06-12 (2021 = rättat
# +720-värdet ur FM ÅR 2022; 2020/2022 korsbekräftade över två bilagor).
GOLDEN_PERSONALSTYRKA = {
    "2019": 22751, "2020": 24094, "2021": 24353,
    "2022": 25011, "2023": 26195, "2024": 27734,
}


def test_personalstyrka_matchar_pinnade_varden() -> None:
    rows = forsvarsmakten.build_personalstyrka_observations()
    by_year = {r["period"]: int(r["value"]) for r in rows}
    assert by_year == GOLDEN_PERSONALSTYRKA


def test_personalstyrka_strikt_monoton_upp() -> None:
    """Strikt monoton uppåt 2019->2024 -> alla D-tecken +, robust mot sifferosäkerhet."""
    rows = sorted(forsvarsmakten.build_personalstyrka_observations(), key=lambda r: r["period"])
    vals = [r["value"] for r in rows]
    assert all(b > a for a, b in zip(vals, vals[1:], strict=False))


def test_personalstyrka_radform_kanonisk() -> None:
    r = next(r for r in forsvarsmakten.build_personalstyrka_observations() if r["period"] == "2024")
    assert r["indicator"] == "personalstyrka_kontinuerligt"
    assert r["category"] == "forsvar"
    assert r["submeasure"] == "militar_formaga"
    assert r["id"] == "obs:forsvarsmakten:personalstyrka_kontinuerligt:2024"
    assert r["source_ref"] == "forsvarsmakten:personalstyrka_kontinuerligt:2024"
    assert "personalstyrka_kontinuerligt" in forsvarsmakten.INDICATORS


def test_personalstyrka_indikator_kanonisk_riktning_up() -> None:
    forsvar = next(c for c in config.categories()["categories"] if c["id"] == "forsvar")
    ind = next(i for i in forsvar["indicators"] if i["id"] == "personalstyrka_kontinuerligt")
    assert ind["direction"] == "up"
    assert ind["submeasure"] == "militar_formaga"


def test_build_all_omfattar_bada_serierna() -> None:
    """build_all_observations() (build_fas3:s full-replace-källa) bär båda FM-serierna."""
    inds = {r["indicator"] for r in forsvarsmakten.build_all_observations()}
    assert inds == set(forsvarsmakten.INDICATORS)
