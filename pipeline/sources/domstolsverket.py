"""Domstolsverkets statistikdatabas DOMstat (PxWeb v1) -> observations (delpoäng D, trygghet).

Levererar `handlaggningstid` (riktning down, kortare = bättre): handläggningstid vid tingsrätt
i månader, 75:e percentilen, för BROTTMÅL EXKL. FÖRTURSMÅL, alla tingsrätter, ur tabell
01_Verksamhetsmal_TR.px "Verksamhetsmål vid tingsrätt" (Officiell domstolsstatistik, SOS).
Tiden mäts från inkommandedag (för brottmål i första hand stämningsansökans datum) till
avgjortdag, per avgörandeår. version 0 (FLAGGAD — kräver mänsklig granskning).

MÅTTVAL (dokumenterat, v0):
- 75-PERCENTIL: Domstolsverkets/regeringens eget verksamhetsmålsmått (mål: 5 månader) —
  robust mot extremmål och känsligare för den breda ärendemassan än ett medelvärde.
- EXKL. FÖRTURSMÅL (häktade/15-17-åringar, hanteras skyndsamt): att snabbspårsreformer flyttar
  mål TILL förturshantering biasar det kvarvarande måttet UPPÅT (de snabbaste målen lämnar
  serien) — alltså en icke-smickrande bias, inte en som belönar sittande regering.
- DOMSTOLSLEDET: serien mäter tingsrätternas genomströmning; uppströms polis-/åklagartid
  fångas delvis av syskonindikatorn uppklaringsgrad i samma submått (rattsvasendets_effektivitet).

PxWeb v1-dialekt identisk med energimyndigheten.py: data hämtas via POST med en json-query
(json-stat2); tidsdimensionen heter "År" och kategorikoderna är interna index, så ÅRET läses ur
category.label, inte ur koden. Dimensionsvärden slås upp via valueText (svenska namn) så en
omkodning i källan inte tyst byter serie. Allt råsvar cachas i data/raw/domstolsverket/ med
manifest. Inget deployas. Tabellväg + serie live-verifierad 2026-06-12 (json-stat2, HTTP 200;
alla 19 år 2007-2025 matchar publicerade värden).
"""

from __future__ import annotations

import json
from dataclasses import asdict
from typing import Any

import httpx

from .base import RAW_DIR, Manifest, _safe

BASE = "https://pxweb.etjanst.domstol.se/PxWeb/api/v1/sv/DOMstat"
TABLE_PATH = "Verksamhetsmal/01_Verksamhetsmal_TR.px"
TABLE_URL = f"{BASE}/{TABLE_PATH}"
LICENSE = "Sveriges officiella statistik – fri vidareutnyttjning med källangivelse (källa: Domstolsverket)"
_UA = {"User-Agent": "rosta-datapipeline/0.1 (civic-tech; official swedish open data)"}

COURT_DIM = "Domstol"
GOAL_DIM = "Verksamhetsmålskategori"
# Önskade dimensionsvärden, matchade på namn (valueText) och uppslagna till PxWeb-koder live,
# så en omkodning (koderna är idag engelska strängar) inte tyst byter serie. Saknas -> hård fail.
COURT_ALL = "Alla tingsrätter"
GOAL_CRIMINAL = "Brottmål exkl. förtursmål"

# Kanoniska indikatorer denna modul levererar (för täcknings-gaten i tests/test_fas3_gate.py).
INDICATORS = ("handlaggningstid",)

# Serie-drift-förväntan (pipeline.expectations). Handläggningstid 75-percentil, månader.
# Ankare 2024=3.1 är publicerat värde (Domstolsverkets officiella domstolsstatistik).
EXPECT = {
    "handlaggningstid": {"min_points": 19, "value_range": [2, 8], "min_latest_year": 2025,
                         "anchors": {"2024": 3.1}},
}


def _client() -> httpx.Client:
    return httpx.Client(timeout=90, headers=_UA, follow_redirects=True)


def _cache(dataset_id: str, retrieved_at: str, url: str, payload: Any, rows: int) -> None:
    path = RAW_DIR / "domstolsverket" / _safe(dataset_id) / f"{_safe(retrieved_at)}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    man = Manifest(
        source="domstolsverket", dataset_id=dataset_id, url=url,
        query="POST json-stat2 (Domstol=Alla tingsrätter, brottmål exkl. förtursmål)",
        retrieved_at=retrieved_at, license=LICENSE, row_count=rows,
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


def annual_series(j: dict[str, Any]) -> dict[str, float]:
    """En enda årsserie ur json-stat2 -> {år -> värde}.

    Året tas ur tidsdimensionens category.label (PxWeb-koderna är interna index, inte år).
    ALLA icke-tidsdimensioner måste vara eliminerade/fixerade (storlek 1) — annars hård fail
    (annars skulle pos=0 tyst plocka en delserie, t.ex. fel domstol eller fel målkategori).
    None-celler (år utan värde) utelämnas.
    """
    ids: list[str] = j["id"]
    size: list[int] = j["size"]
    value: list[Any] = j["value"]
    time_code = _time_dim(j)
    for k, did in enumerate(ids):
        if did != time_code and size[k] != 1:
            raise ValueError(f"Oväntad icke-eliminerad dimension {did!r} (storlek {size[k]}) i {ids}")
    strides = [1] * len(ids)
    for i in range(len(ids) - 2, -1, -1):
        strides[i] = strides[i + 1] * size[i + 1]
    tstride = strides[ids.index(time_code)]
    tcat = j["dimension"][time_code]["category"]
    tlabel = tcat.get("label", {})
    out: dict[str, float] = {}
    for tcode, tpos in tcat["index"].items():
        v = value[tpos * tstride] if tpos * tstride < len(value) else None
        if v is None:
            continue
        out[str(tlabel.get(tcode, tcode))] = float(v)
    return out


def build_observations(series: dict[str, float]) -> list[dict[str, Any]]:
    """{år -> 75-percentil i månader} -> observations-rader (Riket). Ren funktion, golden-testbar."""
    rows: list[dict[str, Any]] = []
    for year, val in sorted(series.items()):
        rows.append({
            "id": f"obs:domstolsverket:handlaggningstid:{year}",
            "category": "trygghet", "submeasure": "rattsvasendets_effektivitet",
            "indicator": "handlaggningstid", "period": str(year),
            "value": round(float(val), 3), "unit": "månader",
            "geography": "Riket",
            "source_ref": f"domstolsverket:01_Verksamhetsmal_TR:{year}",
        })
    return rows


def fetch_handlaggningstid(retrieved_at: str) -> list[dict[str, Any]]:
    """01_Verksamhetsmal_TR: handläggningstid 75-percentil brottmål exkl. förtursmål -> observations."""
    with _client() as c:
        meta = c.get(TABLE_URL)
        meta.raise_for_status()
        variables = {v["code"]: v for v in meta.json()["variables"]}
        wanted = {COURT_DIM: COURT_ALL, GOAL_DIM: GOAL_CRIMINAL}
        codes: dict[str, str] = {}
        for dim, name in wanted.items():
            var = variables.get(dim)
            if var is None:
                raise ValueError(f"01_Verksamhetsmal_TR saknar förväntad dimension {dim!r}")
            name2code = dict(zip(var["valueTexts"], var["values"], strict=False))
            if name not in name2code:
                raise ValueError(f"01_Verksamhetsmal_TR saknar förväntat värde {name!r} i {dim!r}")
            codes[dim] = name2code[name]
        query = {
            "query": [
                {"code": dim, "selection": {"filter": "item", "values": [code]}}
                for dim, code in codes.items()
            ],
            "response": {"format": "json-stat2"},
        }
        resp = c.post(TABLE_URL, json=query)
        resp.raise_for_status()
        j = resp.json()

    series = annual_series(j)
    rows = build_observations(series)
    _cache("01_Verksamhetsmal_TR_brottmal", retrieved_at, TABLE_URL, {"series_len": len(series)}, len(rows))
    return rows
