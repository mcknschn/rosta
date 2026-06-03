"""Energimyndighetens statistikdatabas (PxWeb v1) -> observations (delpoäng D, klimat).

Levererar `fossil_energianvandning` (riktning down, lägre = bättre): summan av den
SLUTLIGA energianvändningen för de fossila energivarorna (kol och koks, petroleum-
produkter, natur- och stadsgas) ur tabell EN0202_8 "Slutlig energianvändning per
energivara fr.o.m. 1970, TWh" (Officiell energistatistik, årlig energibalans).

Varför slutlig användning och inte tillförsel: indikatorn mäter fossil ENERGIANVÄNDNING;
slutlig energianvändning per energivara (EN0202_8) är den officiella serie som svarar mot
"användning" (exkl. omvandlingsförluster/energisektorns egenanvändning). De tre fossila
energivarorna summeras per år -> en total fossil-serie.

PxWeb v1 skiljer sig från SCB:s v2 (scb.py): data hämtas via POST med en json-query, och
tidsdimensionen heter "År" (kategorikoderna är interna index, så ÅRET läses ur category.label,
inte ur koden). Allt råsvar cachas i data/raw/energimyndigheten/ med manifest. Inget deployas.
Tabellväg + fossila energivaror verifierade live 2026-05-30 (json-stat2, HTTP 200).
"""

from __future__ import annotations

import json
from dataclasses import asdict
from typing import Any

import httpx

from .base import RAW_DIR, Manifest, _safe

BASE = "https://pxexternal.energimyndigheten.se/api/v1/sv/Energimyndighetens_statistikdatabas"
TABLE_PATH = "Officiell_energistatistik/Arlig_energibalans/Total_slutlig_energianvandning/EN0202_8.px"
TABLE_URL = f"{BASE}/{TABLE_PATH}"
LICENSE = "Sveriges officiella statistik – fri vidareutnyttjning med källangivelse (källa: Energimyndigheten)"
_UA = {"User-Agent": "rosta-datapipeline/0.1 (civic-tech; official swedish open data)"}

CARRIER_DIM = "Energivara"
# Fossila energivaror i EN0202_8. Matchas på namn (valueText) och slås upp till PxWeb-koder
# live, så en omnumrering av koderna inte tyst byter serie. Saknas något namn -> hård fail.
FOSSIL_CARRIERS = ("Kol och koks", "Petroleumprodukter", "Natur- och stadsgas")

# Kanoniska indikatorer denna modul levererar (för täcknings-gaten i tests/test_fas3_gate.py).
INDICATORS = ("fossil_energianvandning",)

# Serie-drift-förväntan (pipeline.expectations). Slutlig fossil energianvändning, TWh.
EXPECT = {
    "fossil_energianvandning": {"min_points": 30, "value_range": [50, 350], "min_latest_year": 2022,
                                "anchors": {"2020": 95.21}},
}


def _client() -> httpx.Client:
    return httpx.Client(timeout=90, headers=_UA, follow_redirects=True)


def _cache(dataset_id: str, retrieved_at: str, url: str, payload: Any, rows: int) -> None:
    path = RAW_DIR / "energimyndigheten" / _safe(dataset_id) / f"{_safe(retrieved_at)}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    man = Manifest(
        source="energimyndigheten", dataset_id=dataset_id, url=url,
        query="POST json-stat2 (Energivara=fossila)", retrieved_at=retrieved_at,
        license=LICENSE, row_count=rows,
    )
    tmp = path.with_name(path.name + ".tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        json.dump({"manifest": asdict(man), "payload": payload}, fh, ensure_ascii=False)
    tmp.replace(path)


def _time_dim(j: dict[str, Any]) -> str:
    """Tidsdimensionens kod ur json-stat2 (role.time, annars känt kodnamn)."""
    role_time = (j.get("role") or {}).get("time") or []
    if role_time:
        return role_time[0]
    for d in j["id"]:
        if d in ("Tid", "År", "Ar", "ar"):
            return d
    raise ValueError(f"Hittar ingen tidsdimension i json-stat2 (id={j['id']})")


def annual_sum_over(j: dict[str, Any], sum_dim: str) -> dict[str, float]:
    """Summerar json-stat2-värden över `sum_dim` per tidsperiod -> {år -> summa}.

    Året tas ur tidsdimensionens category.label (PxWeb-koderna är interna index, inte år).
    Övriga dimensioner måste vara eliminerade (storlek 1) — annars hård fail (annars skulle
    pos=0 tyst plocka en delserie). None-celler hoppas över; ett år utan något värde utelämnas.
    """
    ids: list[str] = j["id"]
    size: list[int] = j["size"]
    value: list[Any] = j["value"]
    dims: dict[str, Any] = j["dimension"]
    time_code = _time_dim(j)
    for k, did in enumerate(ids):
        if did not in (time_code, sum_dim) and size[k] != 1:
            raise ValueError(f"Oväntad icke-eliminerad dimension {did!r} (storlek {size[k]}) i {ids}")
    strides = [1] * len(ids)
    for i in range(len(ids) - 2, -1, -1):
        strides[i] = strides[i + 1] * size[i + 1]
    tcat = dims[time_code]["category"]
    tlabel = tcat.get("label", {})
    scat = dims[sum_dim]["category"]
    out: dict[str, float] = {}
    for tcode, tpos in tcat["index"].items():
        total: float | None = None
        for spos in scat["index"].values():
            lin = 0
            for k, did in enumerate(ids):
                pos = tpos if did == time_code else (spos if did == sum_dim else 0)
                lin += pos * strides[k]
            v = value[lin] if lin < len(value) else None
            if v is None:
                continue
            total = (total or 0.0) + float(v)
        if total is not None:
            out[str(tlabel.get(tcode, tcode))] = total
    return out


def fetch_fossil_energy(retrieved_at: str) -> list[dict[str, Any]]:
    """EN0202_8: slutlig fossil energianvändning (kol+petroleum+gas) -> observations (Riket)."""
    with _client() as c:
        meta = c.get(TABLE_URL)
        meta.raise_for_status()
        carrier = next(v for v in meta.json()["variables"] if v["code"] == CARRIER_DIM)
        name2code = dict(zip(carrier["valueTexts"], carrier["values"], strict=False))
        missing = [n for n in FOSSIL_CARRIERS if n not in name2code]
        if missing:
            raise ValueError(f"EN0202_8 saknar förväntade fossila energivaror: {missing}")
        query = {
            "query": [{
                "code": CARRIER_DIM,
                "selection": {"filter": "item", "values": [name2code[n] for n in FOSSIL_CARRIERS]},
            }],
            "response": {"format": "json-stat2"},
        }
        resp = c.post(TABLE_URL, json=query)
        resp.raise_for_status()
        j = resp.json()

    series = annual_sum_over(j, CARRIER_DIM)
    rows: list[dict[str, Any]] = []
    for year, val in sorted(series.items()):
        rows.append({
            "id": f"obs:energimyndigheten:fossil_energianvandning:{year}",
            "category": "klimat", "submeasure": "energi_elpriser",
            "indicator": "fossil_energianvandning", "period": str(year),
            "value": round(float(val), 3), "unit": "TWh (slutlig energianvändning)",
            "geography": "Riket", "source_ref": f"energimyndigheten:EN0202_8:{year}",
        })
    _cache("EN0202_8_fossil", retrieved_at, TABLE_URL, {"series_len": len(series)}, len(rows))
    return rows
