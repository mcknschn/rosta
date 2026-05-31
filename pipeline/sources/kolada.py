"""Kolada v3 (api.kolada.se) -> observations (delpoäng D, kommun/region/riket).

v3 är obligatoriskt (v2 ger HTTP 410). Tidsserier per KPI; värden per kön (T=totalt).
Riket har municipality-kod 0000. Öppen och kostnadsfri (RKA). Verifierat live 2026-05-29.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from typing import Any

import httpx

from .base import RAW_DIR, Manifest, _safe

BASE = "https://api.kolada.se/v3"
LICENSE = "Öppen och kostnadsfri (RKA / Kolada)"
_UA = {"User-Agent": "rosta-datapipeline/0.1 (civic-tech; official swedish open data)"}


def _client() -> httpx.Client:
    return httpx.Client(timeout=60, headers=_UA, follow_redirects=True)


def _cache(dataset_id: str, retrieved_at: str, url: str, payload: Any, rows: int) -> None:
    path = RAW_DIR / "kolada" / _safe(dataset_id) / f"{_safe(retrieved_at)}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    man = Manifest(
        source="kolada", dataset_id=dataset_id, url=url, query="data/kpi",
        retrieved_at=retrieved_at, license=LICENSE, row_count=rows,
    )
    tmp = path.with_name(path.name + ".tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        json.dump({"manifest": asdict(man), "payload": payload}, fh, ensure_ascii=False)
    tmp.replace(path)


def kpi_title(kpi_id: str) -> str:
    # v3 /kpi?id=<id> ignorerar id-filtret och returnerar hela katalogen (fel titel).
    # Path-formen /kpi/<id> returnerar rätt enskild KPI (count=1).
    with _client() as c:
        r = c.get(f"{BASE}/kpi/{kpi_id}")
        if r.status_code == 200:
            vals = r.json().get("values", [])
            if vals:
                return vals[0].get("title", "")
    return ""


def fetch_kpi_series(
    kpi_id: str,
    indicator: str,
    category: str,
    submeasure: str,
    retrieved_at: str,
    municipality: str = "0000",
    gender: str = "T",
    unit: str = "",
) -> list[dict[str, Any]]:
    """En KPI-tidsserie för en kommun/region (0000 = Riket) -> observations-rader."""
    url = f"{BASE}/data/kpi/{kpi_id}/municipality/{municipality}"
    with _client() as c:
        r = c.get(url)
        r.raise_for_status()
        records = r.json().get("values", [])

    rows: list[dict[str, Any]] = []
    for rec in records:
        period = rec.get("period")
        cell = next((v for v in rec.get("values", []) if v.get("gender") == gender), None)
        if cell is None or cell.get("value") is None:
            continue
        rows.append({
            "id": f"obs:kolada:{kpi_id}:{municipality}:{period}",
            "category": category, "submeasure": submeasure, "indicator": indicator,
            "period": str(period), "value": float(cell["value"]), "unit": unit,
            "geography": municipality, "source_ref": f"kolada:{kpi_id}:{municipality}:{period}",
        })
    _cache(
        f"{kpi_id}_{municipality}", retrieved_at, url,
        {"records": len(records), "kept": len(rows)}, len(rows),
    )
    return rows
