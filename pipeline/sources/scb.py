"""SCB PxWeb v2 (api.scb.se) -> observations (delpoäng D, nationella indikatorer).

Hämtar hela tidsserier via json-stat2 (GET med valueCodes[dim]=* för alla obligatoriska
variabler). En serie extraheras genom att fixera alla icke-Tid-dimensioner till ett valt
(eller första) kodvärde. Licens: CC0 (SCB). Verifierat live 2026-05-29.
"""

from __future__ import annotations

import json
import time
from dataclasses import asdict
from typing import Any
from urllib.parse import quote

import httpx

from .base import RAW_DIR, Manifest, _safe

BASE = "https://api.scb.se/OV0104/v2beta/api/v2"
LICENSE = "CC0 1.0 (källa: SCB)"
_UA = {"User-Agent": "rosta-datapipeline/0.1 (civic-tech; official swedish open data)"}


def _client() -> httpx.Client:
    return httpx.Client(timeout=90, headers=_UA, follow_redirects=True)


def _cache(dataset_id: str, retrieved_at: str, url: str, payload: Any, rows: int) -> None:
    path = RAW_DIR / "scb" / _safe(dataset_id) / f"{_safe(retrieved_at)}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    man = Manifest(
        source="scb", dataset_id=dataset_id, url=url, query="valueCodes[*]=*",
        retrieved_at=retrieved_at, license=LICENSE, row_count=rows,
    )
    tmp = path.with_name(path.name + ".tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        json.dump({"manifest": asdict(man), "payload": payload}, fh, ensure_ascii=False)
    tmp.replace(path)


def _series_from_jsonstat(j: dict[str, Any], fixed: dict[str, str]) -> list[tuple[str, float | None]]:
    """Extraherar (Tid-kod, värde) för en serie med icke-Tid-dimensioner fixerade."""
    ids: list[str] = j["id"]
    size: list[int] = j["size"]
    value: list[Any] = j["value"]
    dims: dict[str, Any] = j["dimension"]
    strides = [1] * len(ids)
    for i in range(len(ids) - 2, -1, -1):
        strides[i] = strides[i + 1] * size[i + 1]
    tid_index: dict[str, int] = dims["Tid"]["category"]["index"]
    out: list[tuple[str, float | None]] = []
    for code, tpos in sorted(tid_index.items(), key=lambda kv: kv[1]):
        lin = 0
        for k, did in enumerate(ids):
            if did == "Tid":
                pos = tpos
            else:
                idxmap = dims[did]["category"]["index"]
                sel = fixed.get(did)
                pos = idxmap[sel] if sel in idxmap else min(idxmap.values())
            lin += pos * strides[k]
        out.append((code, value[lin] if lin < len(value) else None))
    return out


def _fetch_raw(
    table: str, fixed: dict[str, str], retrieved_at: str, dataset_id: str, delay: float
) -> list[tuple[str, float | None]]:
    """GET json-stat2 för en serie (icke-Tid-dims fixerade), cacha råsvaret, returnera (period, val)."""
    with _client() as c:
        meta = c.get(f"{BASE}/tables/{table}/data?lang=sv&outputFormat=json-stat2")
        meta.raise_for_status()
        dim_ids = list(meta.json()["id"])
        # Default-/data-vyn utelämnar ELIMINERBARA dimensioner; lägg till dem som finns i 'fixed'
        # så att deras kod faktiskt begärs (annars summerar SCB tyst till totalen = fel serie).
        for d in fixed:
            if d not in dim_ids:
                dim_ids.append(d)
        # Fixerade dims begärs som EN kod (URL-kodad, '+' -> %2B); övriga som '*' (alla värden).
        sel = "&".join(
            f"valueCodes[{d}]={quote(str(fixed[d]), safe='')}" if d in fixed else f"valueCodes[{d}]=*"
            for d in dim_ids
        )
        url = f"{BASE}/tables/{table}/data?lang=sv&outputFormat=json-stat2&{sel}"
        time.sleep(delay)
        resp = c.get(url)
        resp.raise_for_status()
        j = resp.json()
    series = _series_from_jsonstat(j, fixed)
    kept = sum(1 for _, v in series if v is not None)
    _cache(dataset_id, retrieved_at, url, {"series_len": len(series), "kept": kept}, kept)
    return series


def fetch_series(
    table: str,
    indicator: str,
    category: str,
    submeasure: str,
    retrieved_at: str,
    fixed: dict[str, str] | None = None,
    unit: str = "",
    delay: float = 0.5,
) -> list[dict[str, Any]]:
    """Hämtar en SCB-tabellserie -> observations-rader (geography=Riket)."""
    fixed = fixed or {}
    series = _fetch_raw(table, fixed, retrieved_at, table, delay)
    rows: list[dict[str, Any]] = []
    for period, val in series:
        if val is None:
            continue
        rows.append({
            "id": f"obs:scb:{indicator}:{period}",
            "category": category, "submeasure": submeasure, "indicator": indicator,
            "period": str(period), "value": float(val), "unit": unit,
            "geography": "Riket", "source_ref": f"scb:{table}:{period}",
        })
    return rows


def fetch_series_map(
    table: str,
    fixed: dict[str, str],
    retrieved_at: str,
    dataset_id: str | None = None,
    delay: float = 0.5,
) -> dict[str, float]:
    """Hämtar EN SCB-serie som {period -> värde} (för härledda indikatorer i pipeline.derived).

    Cachar råsvaret under `dataset_id` (default = tabellnamnet) så att två serier ur SAMMA tabell
    (t.ex. inrikes vs utrikes födda) inte skriver över varandras råcache.
    """
    series = _fetch_raw(table, fixed, retrieved_at, dataset_id or table, delay)
    return {str(p): float(v) for p, v in series if v is not None}
