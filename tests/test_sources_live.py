"""O3: live smoke-test mot de officiella API-källorna — fångar käll-/endpoint-drift proaktivt.

Kompletterar O1 (pipeline.expectations, som kontrollerar VÄRDEN efter hämtning) genom att
kontrollera att varje källas ENDPOINT fortfarande svarar med förväntad form — innan en hel
build körs. Läser tabell-/KPI-listorna direkt ur modulerna, så nya serier täcks automatiskt.

OPT-IN (CI kör plain `pytest` och ska INTE nå nätet): tester skippas om inte ROSTA_LIVE=1 är satt.

    ROSTA_LIVE=1 python -m pytest tests/test_sources_live.py -m network

Polisens skjutnings-/sprängnings-PDF:er (hash-URL:er) täcks av pipeline/tools/skjutningar_transcribe
(full live-audit av alla värden), så de dupliceras inte här.
"""

from __future__ import annotations

import os

import httpx
import pytest

from pipeline import build_fas2
from pipeline.sources import bra, energimyndigheten, kolada, scb

pytestmark = [
    pytest.mark.network,
    pytest.mark.skipif(
        os.environ.get("ROSTA_LIVE") != "1",
        reason="live smoke-test mot officiella API:er; sätt ROSTA_LIVE=1 för att köra",
    ),
]

_UA = {"User-Agent": "rosta-datapipeline/0.1 (civic-tech; official swedish open data)"}


def _client() -> httpx.Client:
    return httpx.Client(timeout=60, headers=_UA, follow_redirects=True)


def test_scb_tabeller_svarar() -> None:
    """Varje SCB-tabell i build_fas2.SCB_SERIES svarar 200 med json-stat2 (har 'id')."""
    with _client() as c:
        for s in build_fas2.SCB_SERIES:
            url = f"{scb.BASE}/tables/{s['table']}/data?lang=sv&outputFormat=json-stat2"
            r = c.get(url)
            assert r.status_code == 200, f"SCB {s['table']}: HTTP {r.status_code}"
            assert "id" in r.json(), f"SCB {s['table']}: oväntat svar (struktur ändrad?)"


def test_kolada_kpier_svarar() -> None:
    """Varje Kolada-KPI i build_fas2.KOLADA_KPIS svarar 200 och finns kvar (values)."""
    with _client() as c:
        for k in build_fas2.KOLADA_KPIS:
            r = c.get(f"{kolada.BASE}/kpi/{k['kpi']}")
            assert r.status_code == 200, f"Kolada {k['kpi']}: HTTP {r.status_code}"
            assert r.json().get("values"), f"Kolada {k['kpi']}: tom KPI (borttagen?)"


def test_energimyndigheten_tabell_svarar() -> None:
    with _client() as c:
        r = c.get(energimyndigheten.TABLE_URL)
        assert r.status_code == 200, f"Energimyndigheten: HTTP {r.status_code}"
        assert "variables" in r.json(), "Energimyndigheten: oväntad PxWeb-metastruktur"


def test_bra_filer_svarar() -> None:
    """Brås xlsx-download-URL:er lever (hash-id ändras vid ny publicering -> 404 fångas här)."""
    urls = {
        "dödligt våld (Tabell 20)": bra.DODLIGT_VALD_URL,
        "NTU-tabellsamling": bra.NTU_URL,
        "personuppklaring (10La)": bra.PERSONUPPKL_URL,
    }
    with _client() as c:
        for name, url in urls.items():
            r = c.get(url)
            assert r.status_code == 200, f"Brå {name}: HTTP {r.status_code} (download-id ändrat?)"
            assert len(r.content) > 5000, f"Brå {name}: misstänkt liten fil ({len(r.content)} B)"
