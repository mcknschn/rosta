"""Härledda D-indikatorer (gap/kvot) ur redan verifierade officiella serier.

Vissa kanoniska indikatorer (categories.yaml) är inte EN publicerad serie utan en DIFFERENS
eller KVOT mellan två officiella serier. Loadern (pipeline.sources.scb) hämtar en serie i taget;
den här modulen kombinerar två sådana serier (vardera helt specificerad av tabell + fixerade
dimensionskoder) till en härledd årsserie som matar delpoäng D precis som vilken annan
observations-serie som helst.

Implementerat:
  * sysselsattningsgap_inrikes_utrikes (integration, riktning down): skillnaden i
    sysselsättningsgrad (SCB AKU TAB6529, SYSP) mellan INRIKES (InrikesUtrikes=13) och UTRIKES
    (=23) födda, procentenheter. Mindre gap = bättre arbetsmarknadsintegration.
  * produktivitet (ekonomi, riktning up): arbetsproduktivitet i hela ekonomin = BNP till
    marknadspris i FASTA priser (SCB nationalräkenskaper TAB3610, Anvandningstyp=BNPM,
    ContentsCode=000000RN, mnkr) DELAT med faktiskt arbetade timmar i hela ekonomin (TAB5622
    Arbetskraftsinsats, SNI2007=0002, ContentsCode=000004C1, 10 000-tal timmar), skalat till
    kr per arbetad timme. Reell produktivitet (fasta priser separerar volym från pris).

Provenans: en härledd observation citerar BÅDA föräldraserierna i source_ref
("derived:{ref_tag}:{år}") och beräkningen är ren/deterministisk -> golden-testbar. Inget
mänskligt omdöme; ingen imputation (ett år tas bara med om BÅDA föräldrarna har värde).

Robusthet: en serie med en angiven enhet (t.ex. kr/timme) får en rimlighetsgrind ('plausible')
på nivån. SCB bytte t.ex. TAB5622:s timenhet från "1 000 000-tal" till "10 000-tal" 2026-05-29;
ett framtida enhetsbyte skulle annars tyst ge en 100x fel nivå. Grinden failar då högt i stället.
"""

from __future__ import annotations

from typing import Any

from .sources import scb

# Härledda indikatorer. Varje post specificerar två operander (a, b) — vardera en SCB-serie
# (tabell + fixerade dimensionskoder) — samt en operation ('gap' = a−b, 'ratio' = a/b·scale).
DERIVED = (
    {
        "indicator": "sysselsattningsgap_inrikes_utrikes",
        "category": "integration", "submeasure": "arbete_sjalvforsorjning",
        "unit": "procentenheter (sysselsättningsgrad inrikes − utrikes födda)",
        "op": "gap",
        "a": {"table": "TAB6529", "fixed": {"Arbetskraftstillh": "SYSP", "TypData": "O_DATA",
              "Kon": "1+2", "Alder": "tot15-74", "ContentsCode": "000007VG",
              "InrikesUtrikes": "13"}},  # inrikes födda
        "b": {"table": "TAB6529", "fixed": {"Arbetskraftstillh": "SYSP", "TypData": "O_DATA",
              "Kon": "1+2", "Alder": "tot15-74", "ContentsCode": "000007VG",
              "InrikesUtrikes": "23"}},  # utrikes födda
        "ref_tag": "scb:TAB6529:SYSP(13-23)",
    },
    {
        "indicator": "produktivitet",
        "category": "ekonomi", "submeasure": "bnp_produktivitet",
        "unit": "kr per arbetad timme (BNP, fasta priser ref. 2020)",
        "op": "ratio", "scale": 100.0,
        # mnkr (1e6 kr) / (10 000-tal timmar = 1e4 timmar) · 100 = kr/timme. Tecknet på
        # årsförändringen (det D bryr sig om) är oberoende av skalfaktorn.
        "plausible": (100.0, 5000.0),  # kr/timme; fångar ett ev. SCB-enhetsbyte (100x-fel) högt
        "a": {"table": "TAB3610", "fixed": {"Anvandningstyp": "BNPM", "ContentsCode": "000000RN"}},
        "b": {"table": "TAB5622", "fixed": {"SNI2007": "0002", "ContentsCode": "000004C1"}},
        "ref_tag": "scb:TAB3610(BNPM,fast2020)/TAB5622(hela_ekonomin,timmar)",
    },
)

# Kanoniska indikatorer denna modul levererar (för täcknings-gaten i tests/test_fas3_gate.py).
INDICATORS = tuple(d["indicator"] for d in DERIVED)


def compute_gap(a: dict[str, float], b: dict[str, float]) -> dict[str, float]:
    """{år -> a−b} för de år BÅDA serierna har värde (avrundat 2 dec). Ingen imputation."""
    return {year: round(a[year] - b[year], 2) for year in sorted(set(a) & set(b))}


def compute_ratio(a: dict[str, float], b: dict[str, float], scale: float) -> dict[str, float]:
    """{år -> a/b·scale} för de år BÅDA serierna har värde (avrundat 2 dec). Hoppar b==0."""
    return {
        year: round(a[year] / b[year] * scale, 2)
        for year in sorted(set(a) & set(b))
        if b[year] != 0
    }


def _series_for(spec: dict[str, Any], a: dict[str, float], b: dict[str, float]) -> dict[str, float]:
    """Tillämpar spec:ens operation på de två föräldraserierna."""
    if spec["op"] == "gap":
        return compute_gap(a, b)
    if spec["op"] == "ratio":
        return compute_ratio(a, b, spec["scale"])
    raise ValueError(f"Okänd operation {spec['op']!r} för {spec['indicator']!r}")


def _rows_for(spec: dict[str, Any], a: dict[str, float], b: dict[str, float]) -> list[dict[str, Any]]:
    """Bygger observations-rader ur två (redan hämtade) föräldraserier. Nätverksfri -> testbar."""
    series = _series_for(spec, a, b)
    if len(series) < 2:
        raise ValueError(
            f"Härledd {spec['indicator']!r}: <2 år med båda föräldraserierna (ej beräkningsbart)"
        )
    lo, hi = spec.get("plausible", (None, None))
    if lo is not None:
        bad = {y: v for y, v in series.items() if not (lo <= v <= hi)}
        if bad:
            raise ValueError(
                f"Härledd {spec['indicator']!r}: värden utanför rimligt band [{lo}, {hi}] "
                f"(enhetsbyte i källan?): {dict(sorted(bad.items())[:3])}"
            )
    rows: list[dict[str, Any]] = []
    for year, val in series.items():
        rows.append({
            "id": f"obs:derived:{spec['indicator']}:{year}",
            "category": spec["category"], "submeasure": spec["submeasure"],
            "indicator": spec["indicator"], "period": str(year),
            "value": val, "unit": spec["unit"], "geography": "Riket",
            "source_ref": f"derived:{spec['ref_tag']}:{year}",
        })
    return rows


def fetch_derived(retrieved_at: str) -> list[dict[str, Any]]:
    """Hämtar föräldraserierna ur SCB och returnerar härledda observations-rader."""
    rows: list[dict[str, Any]] = []
    for spec in DERIVED:
        a = scb.fetch_series_map(
            spec["a"]["table"], spec["a"]["fixed"], retrieved_at,
            dataset_id=f"{spec['indicator']}_a",
        )
        b = scb.fetch_series_map(
            spec["b"]["table"], spec["b"]["fixed"], retrieved_at,
            dataset_id=f"{spec['indicator']}_b",
        )
        rows.extend(_rows_for(spec, a, b))
    return rows
