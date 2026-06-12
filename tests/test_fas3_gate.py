"""Fas 3 täckningsgate (offline): inget tyst gap, allowlist i synk, ledger-form rimlig.

Bevisar invarianten: varje kanonisk indikator i categories.yaml är ANTINGEN inläst
(build_fas2 SCB/Kolada/Brå) ELLER explicit i config/coverage_allowlist.yaml med skäl.
Kör utan nätverk (läser bara config + modulkonstanter).
"""

from __future__ import annotations

from pipeline import build_fas2, config, derived
from pipeline.sources import (
    bra,
    domstolsverket,
    energimyndigheten,
    fmv,
    forsvarsmakten,
    kriminalvarden,
    medlingsinstitutet,
    migrationsverket,
    mpf,
    polisen,
    regeringen,
    sverigesmiljomal,
    svk,
    vdem,
)


def _all_indicators() -> set[tuple[str, str]]:
    out: set[tuple[str, str]] = set()
    for cat in config.categories()["categories"]:
        for ind in cat.get("indicators", []):
            out.add((cat["id"], ind["id"]))
    return out


def _ingested() -> set[tuple[str, str]]:
    """(kategori, indikator) som build_fas2 faktiskt läser in (SCB + Kolada + Brå)."""
    out: set[tuple[str, str]] = set()
    for s in build_fas2.SCB_SERIES:
        out.add((s["category"], s["indicator"]))
    for k in build_fas2.KOLADA_KPIS:
        out.add((k["category"], k["indicator"]))
    for ind in bra.INDICATORS:
        out.add((bra.INDICATOR_CATEGORY[ind], ind))
    for ind in energimyndigheten.INDICATORS:
        out.add(("klimat", ind))
    for ind in polisen.INDICATORS:
        out.add(("trygghet", ind))
    for ind in domstolsverket.INDICATORS:
        out.add(("trygghet", ind))
    for ind in medlingsinstitutet.INDICATORS:
        out.add(("ekonomi", ind))
    for ind in forsvarsmakten.INDICATORS:
        out.add(("forsvar", ind))
    for ind in fmv.INDICATORS:
        out.add(("forsvar", ind))
    for ind in mpf.INDICATORS:
        out.add(("forsvar", ind))
    for ind in regeringen.INDICATORS:
        out.add(("forsvar", ind))
    for ind in kriminalvarden.INDICATORS:
        out.add(("trygghet", ind))
    for ind in migrationsverket.INDICATORS:
        out.add(("integration", ind))
    for ind in sverigesmiljomal.INDICATORS:
        out.add(("klimat", ind))
    for ind in svk.INDICATORS:
        out.add(("klimat", ind))
    for ind in vdem.INDICATORS:
        out.add(("demokrati", ind))
    for d in derived.DERIVED:
        out.add((d["category"], d["indicator"]))
    return out


def _allowlisted() -> set[tuple[str, str]]:
    return {(e["category"], e["indicator"]) for e in config.coverage_allowlist()["allowlist"]}


def test_no_silent_coverage_gap() -> None:
    """Varje indikator är inläst eller allowlistad — unionen täcker hela modellen."""
    allinds = _all_indicators()
    accounted = _ingested() | _allowlisted()
    missing = allinds - accounted
    assert not missing, f"Indikatorer varken inlästa eller allowlistade (tyst gap): {sorted(missing)}"


def test_allowlist_disjoint_from_ingested() -> None:
    """En indikator får inte vara både inläst OCH allowlistad (allowlisten ska krympa)."""
    overlap = _ingested() & _allowlisted()
    assert not overlap, f"Allowlistade men redan inlästa (ta bort ur allowlist): {sorted(overlap)}"


def test_allowlist_entries_valid_and_motivated() -> None:
    """Varje allowlist-post pekar på en riktig indikator och har ett icke-tomt skäl."""
    allinds = _all_indicators()
    for e in config.coverage_allowlist()["allowlist"]:
        assert (e["category"], e["indicator"]) in allinds, f"Okänd indikator: {e}"
        assert e.get("reason", "").strip(), f"Saknar skäl: {e}"


def test_ingested_indicators_exist_in_model() -> None:
    """Allt build_fas2 läser in pekar på kanoniska indikatorer (inga döda observationer)."""
    allinds = _all_indicators()
    for ci in _ingested():
        assert ci in allinds, f"Inläst indikator saknas i categories.yaml: {ci}"
