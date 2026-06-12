"""Medlingsinstitutets PxWeb-instans -> observations (delpoäng D, ekonomi).

Levererar `realloner` (riktning up, högre = bättre): reala löner i hela ekonomin som
INDEX (1995=100), nominell lön deflaterad med KPI, ur tabell Realloner_arsdata.px
"Löner, konsumentpriser och reala löner i hela ekonomin, årsdata" (Medlingsinstitutet —
statlig myndighet, statistikansvarig för den officiella lönestatistiken/konjunktur-
lönestatistiken; underlag: MI/SCB/Konjunkturinstitutet). 66 konsekutiva år 1960-2025.
version 0 (FLAGGAD — kräver mänsklig granskning).

MÅTTVAL (dokumenterat, v0):
- REALLÖN (KPI), inte (KPIF): KPI-deflaterad reallön är MI:s HUVUDSERIE i analyserna av
  reallöneutvecklingen. Valet är inte neutralt i magnitud — KPI inkluderar hushållens
  räntekostnader, så räntehöjningsåren 2022-23 ger djupare fall med KPI än KPIF
  (2023: -4,9 % mot -2,3 %) — men D tar bara TECKNET på årsförändringen, och tecknet är
  detsamma (fall 2022-23, återhämtning 2024-25) för båda deflatorerna. Explicit val, ej tyst.
- INDEX (1995=100), inte årlig %: D-attributionen bildar själv år-för-år-förändringar ur
  nivåserien (score.direction_adjusted_change); en %-serie vore en redan deriverad storhet
  med annan semantik (förändring av förändringen).
- 2025 ÄR PRELIMINÄR tills konjunkturlönestatistiken är definitiv (lönerevisioner släpar
  ~12 mån); historiska år är definitiva.
- Submåttet realloner_hushall har redan D via hushallens_reala_disponibla_inkomst (SCB NR,
  derived) — serierna är korrelerade (löner är största inkomstkällan): detta är en MEDVETEN
  dubbelbreddning inom undermåttet (djup, inte bredd), noterad i allowlist-kommentaren.

PxWeb v1-dialekt identisk med domstolsverket.py/energimyndigheten.py: data hämtas via POST
med en json-query (json-stat2); tidsdimensionen heter "Period" och kategorikoderna är interna
index ("0".."65"), så ÅRET läses ur category.label, inte ur koden. Dimensionsvärden slås upp
via valueText (svenska namn) så en omkodning i källan inte tyst byter serie. EGENHETER:
URL:en bär URL-encodade svenska tecken (Konjunkturl%C3%B6nestatistik/Reall%C3%B6neutveckling)
och MI:s server har observerats svara med UTF-8-BOM -> svaren avkodas med utf-8-sig
(BOM-tolerant, ofarligt utan BOM). Dimensionskoden "Typ av data" innehåller mellanslag.
Allt råsvar cachas i data/raw/medlingsinstitutet/ med manifest. Inget deployas.
Tabellväg + serie live-verifierad 2026-06-12 (json-stat2, HTTP 200; ankarvärden 1995=100,
2020=168,9, 2022=161,0, 2023=153,7, 2024=155,5, 2025=160,1 matchar publicerade värden).
"""

from __future__ import annotations

import json
from dataclasses import asdict
from typing import Any

import httpx

from .base import RAW_DIR, Manifest, _safe

# OBS: URL-encodade svenska tecken (ö/Ö) i databas-/tabellvägen — behåll exakt denna form.
TABLE_URL = (
    "https://www.mi.se/PXWeb/api/v1/sv/"
    "Konjunkturl%C3%B6nestatistik/Reall%C3%B6neutveckling/Realloner_arsdata.px"
)
LICENSE = "Medlingsinstitutet (statistikansvarig myndighet, officiell lönestatistik) – fri vidareutnyttjning med källangivelse"
_UA = {"User-Agent": "rosta-datapipeline/0.1 (civic-tech; official swedish open data)"}

VARIABLE_DIM = "Variabel"
DATATYPE_DIM = "Typ av data"  # dimensionskod med mellanslag — giltig PxWeb-kod, citeras i query
# Önskade dimensionsvärden, matchade på namn (valueText) och uppslagna till PxWeb-koder live,
# så en omkodning (koderna är idag indexsträngar "0".."4") inte tyst byter serie. Saknas -> hård fail.
VARIABLE_REAL_WAGE_KPI = "Reallön (KPI)"
DATATYPE_INDEX = "Index(1995=100)"

# Kanoniska indikatorer denna modul levererar (för täcknings-gaten i tests/test_fas3_gate.py).
INDICATORS = ("realloner",)

# Serie-drift-förväntan (pipeline.expectations). Reallön (KPI) som index, 1995=100.
# Ankare 2024=155.5 + basåret 1995=100.0 är publicerade värden (MI Realloner_arsdata).
EXPECT = {
    "realloner": {"min_points": 60, "value_range": [20, 250], "min_latest_year": 2025,
                  "anchors": {"1995": 100.0, "2024": 155.5}},
}


def _client() -> httpx.Client:
    return httpx.Client(timeout=90, headers=_UA, follow_redirects=True)


def _json(resp: httpx.Response) -> Any:
    """JSON ur ett MI-svar. utf-8-sig tål serverns observerade UTF-8-BOM (no-op utan BOM)."""
    return json.loads(resp.content.decode("utf-8-sig"))


def _cache(dataset_id: str, retrieved_at: str, url: str, payload: Any, rows: int) -> None:
    path = RAW_DIR / "medlingsinstitutet" / _safe(dataset_id) / f"{_safe(retrieved_at)}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    man = Manifest(
        source="medlingsinstitutet", dataset_id=dataset_id, url=url,
        query="POST json-stat2 (Variabel=Reallön (KPI), Typ av data=Index(1995=100))",
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
        if d in ("Tid", "År", "Ar", "ar", "Period"):
            return d
    raise ValueError(f"Hittar ingen tidsdimension i json-stat2 (id={j['id']})")


def annual_series(j: dict[str, Any]) -> dict[str, float]:
    """En enda årsserie ur json-stat2 -> {år -> värde}.

    Året tas ur tidsdimensionens category.label (PxWeb-koderna är interna index, inte år).
    ALLA icke-tidsdimensioner måste vara eliminerade/fixerade (storlek 1) — annars hård fail
    (annars skulle pos=0 tyst plocka en delserie, t.ex. fel variabel eller fel datatyp:
    %-förändring i stället för index). None-celler (år utan värde) utelämnas.
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
    """{år -> reallöneindex (KPI), 1995=100} -> observations-rader (Riket). Ren funktion, golden-testbar."""
    rows: list[dict[str, Any]] = []
    for year, val in sorted(series.items()):
        rows.append({
            "id": f"obs:medlingsinstitutet:realloner:{year}",
            "category": "ekonomi", "submeasure": "realloner_hushall",
            "indicator": "realloner", "period": str(year),
            "value": round(float(val), 3), "unit": "index (1995=100)",
            "geography": "Riket",
            "source_ref": f"medlingsinstitutet:Realloner_arsdata:{year}",
        })
    return rows


def fetch_realloner(retrieved_at: str) -> list[dict[str, Any]]:
    """Realloner_arsdata: Reallön (KPI) som Index(1995=100), hela ekonomin -> observations."""
    with _client() as c:
        meta = c.get(TABLE_URL)
        meta.raise_for_status()
        variables = {v["code"]: v for v in _json(meta)["variables"]}
        wanted = {VARIABLE_DIM: VARIABLE_REAL_WAGE_KPI, DATATYPE_DIM: DATATYPE_INDEX}
        codes: dict[str, str] = {}
        for dim, name in wanted.items():
            var = variables.get(dim)
            if var is None:
                raise ValueError(f"Realloner_arsdata saknar förväntad dimension {dim!r}")
            name2code = dict(zip(var["valueTexts"], var["values"], strict=False))
            if name not in name2code:
                raise ValueError(f"Realloner_arsdata saknar förväntat värde {name!r} i {dim!r}")
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
        j = _json(resp)

    series = annual_series(j)
    rows = build_observations(series)
    _cache("Realloner_arsdata_reallon_kpi_index", retrieved_at, TABLE_URL,
           {"series_len": len(series)}, len(rows))
    return rows
