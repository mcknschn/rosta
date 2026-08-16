"""Härledda D-indikatorer (gap/kvot/index) ur redan verifierade officiella serier.

Vissa kanoniska indikatorer (categories.yaml) är inte EN publicerad serie utan en DIFFERENS,
KVOT eller ett kumulerat INDEX byggt ur officiella serier. Loadern (pipeline.sources.scb) hämtar
en serie i taget; den här modulen kombinerar en eller två sådana serier (vardera helt
specificerad av tabell + fixerade dimensionskoder) till en härledd årsserie som matar delpoäng D
precis som vilken annan observations-serie som helst.

Implementerat:
  * sysselsattningsgap_inrikes_utrikes (integration, riktning down): skillnaden i
    sysselsättningsgrad (SCB AKU TAB6529, SYSP) mellan INRIKES (InrikesUtrikes=13) och UTRIKES
    (=23) födda, procentenheter. Mindre gap = bättre arbetsmarknadsintegration.
  * produktivitet (ekonomi, riktning up): arbetsproduktivitet i hela ekonomin = BNP till
    marknadspris i FASTA priser (SCB nationalräkenskaper TAB3610, Anvandningstyp=BNPM,
    ContentsCode=000000RN, mnkr) DELAT med faktiskt arbetade timmar i hela ekonomin (TAB5622
    Arbetskraftsinsats, SNI2007=0002, ContentsCode=000004C1, 10 000-tal timmar), skalat till
    kr per arbetad timme. Reell produktivitet (fasta priser separerar volym från pris).
  * hushallens_reala_disponibla_inkomst (ekonomi, riktning up): kumulativt REALINDEX (basår-1 =
    100) ur SCB:s officiella reala tillväxttakt för hushållens disponibla inkomst, netto (NR
    TAB4592, NRindikator=B6nRealGrowth, Sektor=S14). idx[y] = idx[y-1]·(1 + g[y]/100). SCB har
    redan deflaterat (real tillväxt), så indexet kräver inget eget deflatorval. Måttet finns bara
    publicerat som tillväxttakt; D behöver en NIVÅ (tecknet på årsförändringen). Tecknet på
    indexets årsförändring = tecknet på den officiella reala tillväxttakten — vilket är allt D
    använder (sign, ej magnitud). Drift-skyddet sitter därför på FÖRÄLDRA-tillväxtserien
    (input_expect), inte på det konstruerade indexet (som saknar publicerat ankarvärde).

Provenans: en härledd observation citerar föräldraserie(rna) i source_ref
("derived:{ref_tag}:{år}") och beräkningen är ren/deterministisk -> golden-testbar. Inget
mänskligt omdöme; ingen imputation (gap/kvot: ett år tas bara med om BÅDA föräldrarna har värde).

Robusthet: en serie med en angiven enhet (t.ex. kr/timme) får en rimlighetsgrind ('plausible')
på nivån. SCB bytte t.ex. TAB5622:s timenhet från "1 000 000-tal" till "10 000-tal" 2026-05-29;
ett framtida enhetsbyte skulle annars tyst ge en 100x fel nivå. Grinden failar då högt i stället.
"""

from __future__ import annotations

from typing import Any

from . import expectations
from .sources import scb

# Härledda indikatorer. Varje post specificerar en (a) eller två (a, b) operander — vardera en
# SCB-serie (tabell + fixerade dimensionskoder) — samt en operation ('gap' = a−b, 'ratio' =
# a/b·scale, 'index' = kumulativt index av en tillväxttakt a).
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
        "expect": {"min_points": 12, "value_range": [0, 20], "min_latest_year": 2024,
                   "anchors": {"2020": 9.9}},
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
        "expect": {"min_points": 20, "value_range": [200, 800], "min_latest_year": 2022,
                   "anchors": {"2020": 619.94}},
    },
    {
        "indicator": "utslappsintensitet",
        "category": "klimat", "submeasure": "kostnadseffektivitet",
        "unit": "ton CO2-ekv. per mnkr BNP (fasta priser ref. 2020)",
        "op": "ratio", "scale": 1000.0,
        # kt (1000 ton) / mnkr · 1000 = ton/mnkr. Tecknet på årsförändringen (det D bryr sig om) är
        # oberoende av skalfaktorn. Ekonomins koldioxidintensitet (frikoppling utsläpp/BNP).
        "plausible": (1.0, 40.0),  # ton/mnkr; fångar ett ev. SCB-enhetsbyte högt
        "a": {"table": "TAB4698", "fixed": {"Vaxthusgaser": "CO2-ekv.", "Sektor": "0.1",
              "ContentsCode": "0000018Q"}},  # territoriella växthusgasutsläpp, kt
        # BNP mnkr
        "b": {"table": "TAB3610", "fixed": {"Anvandningstyp": "BNPM", "ContentsCode": "000000RN"}},
        "ref_tag": "scb:TAB4698(CO2ekv,tot)/TAB3610(BNPM,fast2020)",
        "expect": {"min_points": 20, "value_range": [1, 40], "min_latest_year": 2023,
                   "anchors": {"2020": 9.17}},
    },
    {
        "indicator": "hushallens_reala_disponibla_inkomst",
        "category": "ekonomi", "submeasure": "realloner_hushall",
        "unit": "index (realt, basår-1 = 100; SCB NR hushållens reala disp. inkomst, netto)",
        "op": "index", "base": 100.0,
        "a": {"table": "TAB4592", "fixed": {"NRindikator": "B6nRealGrowth", "Sektor": "S14"}},
        "ref_tag": "scb:TAB4592(B6nRealGrowth,S14,kumul.index)",
        # Drift-skyddet sitter på FÖRÄLDRA-tillväxtserien (indexet är konstruerat -> inget publicerat
        # ankarvärde). value_range [-15,15] tål reala fall (skiljer från nominell tillväxt, som
        # alltid > 0 i fönstret); ankare 2023≈-1.1 (real, NEGATIVT) pinnar real vs nominell/annan
        # sektor med rel_tol 0.3 (NR revideras). rel_tol-bandet [-1.43,-0.77] utesluter nominell.
        "input_expect": {"min_points": 60, "value_range": [-15, 15], "min_latest_year": 2024,
                         "anchors": {"2023": -1.1, "2021": 4.3}, "rel_tol": 0.3},
        # expect på det HÄRLEDDA indexet: bara form/aktualitet (nivån är arbiträr, sign-only D).
        "expect": {"min_points": 60, "min_latest_year": 2024},
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


def compute_index(growth: dict[str, float], base: float) -> dict[str, float]:
    """{år -> kumulativt index} ur en tillväxttakt i PROCENT (avrundat 2 dec).

    idx[y] = idx[y-1]·(1 + g[y]/100); nivån FÖRE första året = base. Eftersom idx alltid är > 0
    har idx:s årsförändring samma TECKEN som g[y] — vilket är allt delpoäng D använder (sign, ej
    magnitud). Ingen imputation: bara år som finns i tillväxtserien emitteras.
    """
    out: dict[str, float] = {}
    level = base
    for year in sorted(growth, key=int):
        level *= 1.0 + growth[year] / 100.0
        out[year] = round(level, 2)
    return out


def _series_for(
    spec: dict[str, Any], a: dict[str, float], b: dict[str, float] | None
) -> dict[str, float]:
    """Tillämpar spec:ens operation på föräldraserien/-serierna."""
    if spec["op"] == "index":
        return compute_index(a, spec.get("base", 100.0))
    if b is None:
        raise ValueError(f"Operation {spec['op']!r} kräver två operander (a, b) — {spec['indicator']!r}")
    if spec["op"] == "gap":
        return compute_gap(a, b)
    if spec["op"] == "ratio":
        return compute_ratio(a, b, spec["scale"])
    raise ValueError(f"Okänd operation {spec['op']!r} för {spec['indicator']!r}")


def _rows_for(
    spec: dict[str, Any], a: dict[str, float], b: dict[str, float] | None = None
) -> list[dict[str, Any]]:
    """Bygger observations-rader ur (redan hämtade) föräldraserier. Nätverksfri -> testbar."""
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
    """Hämtar föräldraserien/-serierna ur SCB och returnerar härledda observations-rader."""
    rows: list[dict[str, Any]] = []
    for spec in DERIVED:
        a = scb.fetch_series_map(
            spec["a"]["table"], spec["a"]["fixed"], retrieved_at,
            dataset_id=f"{spec['indicator']}_a",
        )
        # Drift-skydd på FÖRÄLDRA-serien (för index-op, där det härledda värdet saknar publicerat
        # ankare) — hard-failar på fel dimension/sektor INNAN den kumuleras in i D.
        ie = spec.get("input_expect")
        if ie:
            expectations.check_series(
                [{"period": y, "value": v} for y, v in a.items()], ie,
                f"Härledd {spec['indicator']} (föräldraserie {spec['ref_tag']})",
            )
        b = None
        if "b" in spec:
            b = scb.fetch_series_map(
                spec["b"]["table"], spec["b"]["fixed"], retrieved_at,
                dataset_id=f"{spec['indicator']}_b",
            )
        rows.extend(_rows_for(spec, a, b))
    return rows
