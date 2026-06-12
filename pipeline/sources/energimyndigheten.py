"""Energimyndighetens statistikdatabas (PxWeb v1) -> observations (delpoäng D, klimat).

Levererar TVÅ klimatindikatorer ur samma PxWeb-instans (olika db-vägar, samma host/dialekt):

1. `fossil_energianvandning` (riktning down, lägre = bättre): summan av den
   SLUTLIGA energianvändningen för de fossila energivarorna (kol och koks, petroleum-
   produkter, natur- och stadsgas) ur tabell EN0202_8 "Slutlig energianvändning per
   energivara fr.o.m. 1970, TWh" (Officiell energistatistik, årlig energibalans).

   Varför slutlig användning och inte tillförsel: indikatorn mäter fossil ENERGIANVÄNDNING;
   slutlig energianvändning per energivara (EN0202_8) är den officiella serie som svarar mot
   "användning" (exkl. omvandlingsförluster/energisektorns egenanvändning). De tre fossila
   energivarorna summeras per år -> en total fossil-serie.

2. `elprisvolatilitet` (riktning down, lägre = bättre): årlig variationskoefficient för
   elspotpriset ur tabell EN_IND12-5A "Elspotpris Sverige (från november 2011), månads-
   medelvärden, kr/MWh" (Energiindikatorer 12.5), per elområde SE1-SE4. Datakällan är
   Energimyndighetens OFFICIELLA statistikdatabas (statlig myndighet) — inte Nord Pool
   direkt — vilket UPPLÖSER källregelfrågan i docs/spar_D_datatackning.md §5.4.

   MÅTTVAL (v0, dokumenterat och LÅST):
   - Årlig volatilitet = CV = stdev/medel över årets 12 månadsmedel, per elområde,
     LIKAVIKTAT medel över SE1-SE4, i procent. CV är skalfri: den straffar inte hög
     prisNIVÅ eller inflation, bara INSTABILITET — indikatorn heter volatilitet.
     Standardmått, riktningsneutralt utan ideologiskt val. FÖRKASTADE alternativ:
     rå stdev (nivå-/inflationskänslig), max-min (outlierkänslig).
   - POPULATIONS-stdev (ddof=0, statistics.pstdev) — valt och låst här + i golden-testet.
     (Sonderingens referensvärden var beräknade med sample-stdev ddof=1; våra värden är
     exakt referens x sqrt(11/12) ~ 4 % lägre — t.ex. 2022: 62,6 mot 65,3 — dokumenterad,
     förväntad avvikelse, samma serieform/tecken.)
   - Endast år med 12/12 månader per elområde räknas (serien är lucka-fri 2011M11-2025M12
     -> 14 kompletta år 2012-2025; 2011 har bara nov-dec och utesluts av regeln).
   - LIKAVIKTNING SE1-SE4 (inte konsumtionsviktning): enklare + neutralt, inget val av
     viktkälla. Caveat: SE3/SE4 har flest kunder; likaviktningen ger norra elområdena
     samma röst.
   - Beräkningen sker I ADAPTERN: månadsobservationer skrivs INTE till warehouse
     (period_to_year ger None för YYYYMmm -> döda rader); endast årsvärden emittas.
     Prejudikat: kriminalvarden.py beräknar andel ur råtal.
   v0-CAVEATS: månadsupplösning underskattar tim-/dygnsvolatilitet (negativa timpriser/
   spotspikar syns ej — måttet fångar säsongs-/strukturell instabilitet; effektproblematik
   täcks av syskonindikatorn effektbrist när den byggs); volatiliteten drivs starkt av
   europeiska gaspriser/överföringsläge (2022) — sedvanlig D-konjunktur-caveat (tecken-ej-
   magnitud + 10 %-vikt + ansvarsviktning).

PxWeb v1 skiljer sig från SCB:s v2 (scb.py): data hämtas via POST med en json-query, och
tidsdimensionen heter "År" resp. "År/Månad" (kategorikoderna är interna index, så PERIODEN
läses ur category.label, inte ur koden; EN_IND12-5A saknar role.time -> namnfallback).
Allt råsvar cachas i data/raw/energimyndigheten/ med manifest. Inget deployas.
Tabellväg + fossila energivaror verifierade live 2026-05-30; EN_IND12-5A verifierad live
2026-06-12 (json-stat2, HTTP 200; ankarvärden SE3 kr/MWh: 2021M01=491, 2022M08=2230,
2022M12=2690, 2023M06=531, 2025M12=517 matchar publicerade värden).
"""

from __future__ import annotations

import json
import re
import statistics
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

# Elspotpris (Energiindikatorer 12.5): annan db-väg i samma statistikdatabas/host.
SPOT_TABLE_PATH = "Energiindikatorer/12/12.5/EN_IND12-5A.px"
SPOT_TABLE_URL = f"{BASE}/{SPOT_TABLE_PATH}"
AREA_DIM = "Elområde"
# Elområden i EN_IND12-5A. Matchas på namn (valueText), slås upp till koder live (samma
# anti-omnumreringsskydd som FOSSIL_CARRIERS). Saknas något -> hård fail.
SPOT_AREAS = ("SE1", "SE2", "SE3", "SE4")
_MONTH_RE = re.compile(r"^(\d{4})M(\d{2})$")  # periodformat i EN_IND12-5A, t.ex. 2022M08

# Kanoniska indikatorer denna modul levererar (för täcknings-gaten i tests/test_fas3_gate.py).
INDICATORS = ("fossil_energianvandning", "elprisvolatilitet")

# Serie-drift-förväntan (pipeline.expectations). Slutlig fossil energianvändning, TWh;
# elprisvolatilitet = årlig CV i % (ddof=0, likaviktat SE1-SE4) — ankare 2022=62.56 är
# vårt beräknade värde ur live-datat 2026-06-12 (rel_tol 0.05 default tål källrevision).
EXPECT = {
    "fossil_energianvandning": {"min_points": 30, "value_range": [50, 350], "min_latest_year": 2022,
                                "anchors": {"2020": 95.21}},
    "elprisvolatilitet": {"min_points": 12, "value_range": [2, 120], "min_latest_year": 2025,
                          "anchors": {"2022": 62.56}},
}


def _client() -> httpx.Client:
    return httpx.Client(timeout=90, headers=_UA, follow_redirects=True)


def _cache(dataset_id: str, retrieved_at: str, url: str, payload: Any, rows: int,
           query: str = "POST json-stat2 (Energivara=fossila)") -> None:
    path = RAW_DIR / "energimyndigheten" / _safe(dataset_id) / f"{_safe(retrieved_at)}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    man = Manifest(
        source="energimyndigheten", dataset_id=dataset_id, url=url,
        query=query, retrieved_at=retrieved_at,
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
        if d in ("Tid", "År", "Ar", "ar", "År/Månad"):  # EN_IND12-5A saknar role.time
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


def monthly_by_area(j: dict[str, Any]) -> dict[str, dict[str, float]]:
    """json-stat2 (EN_IND12-5A) -> {elområde -> {YYYYMmm -> spotpris kr/MWh}}.

    Område/månad tas ur respektive dimensions category.label (PxWeb-koderna är interna
    index). Övriga dimensioner (ContentsCode) måste vara eliminerade (storlek 1) — annars
    hård fail (annars skulle pos=0 tyst plocka en delserie). Månadsetiketter som inte
    matchar YYYYMmm -> hård fail (formatdrift i källan ska inte tyst ge tomma årsgrupper).
    None-celler (månad utan värde) utelämnas — 12/12-regeln i annual_cv hanterar dem.
    """
    ids: list[str] = j["id"]
    size: list[int] = j["size"]
    value: list[Any] = j["value"]
    dims: dict[str, Any] = j["dimension"]
    time_code = _time_dim(j)
    for k, did in enumerate(ids):
        if did not in (time_code, AREA_DIM) and size[k] != 1:
            raise ValueError(f"Oväntad icke-eliminerad dimension {did!r} (storlek {size[k]}) i {ids}")
    strides = [1] * len(ids)
    for i in range(len(ids) - 2, -1, -1):
        strides[i] = strides[i + 1] * size[i + 1]
    acat = dims[AREA_DIM]["category"]
    alabel = acat.get("label", {})
    tcat = dims[time_code]["category"]
    tlabel = tcat.get("label", {})
    out: dict[str, dict[str, float]] = {}
    for acode, apos in acat["index"].items():
        area = str(alabel.get(acode, acode))
        for tcode, tpos in tcat["index"].items():
            month = str(tlabel.get(tcode, tcode))
            if not _MONTH_RE.match(month):
                raise ValueError(f"Oväntat periodformat {month!r} i {time_code!r} (väntade YYYYMmm)")
            lin = 0
            for k, did in enumerate(ids):
                pos = tpos if did == time_code else (apos if did == AREA_DIM else 0)
                lin += pos * strides[k]
            v = value[lin] if lin < len(value) else None
            if v is None:
                continue
            out.setdefault(area, {})[month] = float(v)
    return out


def annual_cv(monthly: dict[str, dict[str, float]]) -> dict[str, float]:
    """{elområde -> {YYYYMmm -> pris}} -> {år -> CV i %} (ren funktion, golden-testbar).

    Årlig volatilitet = variationskoefficient CV = POPULATIONS-stdev (ddof=0,
    statistics.pstdev) / medel över årets 12 månadsmedel, per elområde, sedan LIKAVIKTAT
    medel över elområdena. Endast år där VARJE elområde har exakt 12/12 månader räknas
    (2011 har bara nov-dec -> utesluts; en framtida lucka i något område fäller hela året
    i stället för att tyst snedvikta). Måttvalsmotivering: se modulens docstring.
    """
    per_year_cv: dict[str, dict[str, float]] = {}
    for area, months in monthly.items():
        by_year: dict[str, list[float]] = {}
        for month, v in months.items():
            by_year.setdefault(month[:4], []).append(v)
        for year, vals in by_year.items():
            if len(vals) != 12:
                continue  # 12/12-regeln: ofullständigt år räknas inte
            mean = sum(vals) / 12.0
            per_year_cv.setdefault(year, {})[area] = 100.0 * statistics.pstdev(vals) / mean
    n_areas = len(monthly)
    return {
        year: sum(cvs.values()) / n_areas
        for year, cvs in per_year_cv.items()
        if len(cvs) == n_areas  # alla elområden kompletta, annars utesluts året
    }


def build_volatility_observations(series: dict[str, float]) -> list[dict[str, Any]]:
    """{år -> CV %} -> observations-rader (Riket). Ren funktion, golden-testbar."""
    rows: list[dict[str, Any]] = []
    for year, val in sorted(series.items()):
        rows.append({
            "id": f"obs:energimyndigheten:elprisvolatilitet:{year}",
            "category": "klimat", "submeasure": "energi_elpriser",
            "indicator": "elprisvolatilitet", "period": str(year),
            "value": round(float(val), 3), "unit": "CV % (månadsmedel, likaviktat SE1-SE4)",
            "geography": "Riket", "source_ref": f"energimyndigheten:EN_IND12-5A:{year}",
        })
    return rows


def fetch_elprisvolatilitet(retrieved_at: str) -> list[dict[str, Any]]:
    """EN_IND12-5A: elspotpris månadsmedel SE1-SE4 -> årlig CV (%) -> observations (Riket)."""
    with _client() as c:
        meta = c.get(SPOT_TABLE_URL)
        meta.raise_for_status()
        area = next(v for v in meta.json()["variables"] if v["code"] == AREA_DIM)
        name2code = dict(zip(area["valueTexts"], area["values"], strict=False))
        missing = [n for n in SPOT_AREAS if n not in name2code]
        if missing:
            raise ValueError(f"EN_IND12-5A saknar förväntade elområden: {missing}")
        query = {
            "query": [{
                "code": AREA_DIM,
                "selection": {"filter": "item", "values": [name2code[n] for n in SPOT_AREAS]},
            }],
            "response": {"format": "json-stat2"},
        }
        resp = c.post(SPOT_TABLE_URL, json=query)
        resp.raise_for_status()
        j = resp.json()

    monthly = monthly_by_area(j)
    series = annual_cv(monthly)
    rows = build_volatility_observations(series)
    _cache("EN_IND12-5A_elprisvolatilitet", retrieved_at, SPOT_TABLE_URL,
           {"areas": sorted(monthly), "months_per_area": {a: len(m) for a, m in monthly.items()},
            "series_len": len(series)}, len(rows),
           query="POST json-stat2 (Elområde=SE1-SE4) -> årlig CV (ddof=0, likaviktat)")
    return rows
