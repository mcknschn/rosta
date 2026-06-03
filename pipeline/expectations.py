"""Serie-drift-skydd (O1): deklarativa förväntansassertioner per inläst årsserie.

Pipelinen isolerar varje officiell serie via hårdkodade tabell-/dimensionskoder (scb.py:s
`fixed`, energimyndigheten.py:s energivaror, Brås bladetiketter). Om en källa byter
tabell-id, dimensionskod eller omdefinierar en serie kan loadern tyst hämta FEL serie —
och eftersom betyg D byggs på dessa serier skulle felet propagera tyst. En ren förväntansgrind
körd DIREKT efter fetch (före warehouse-skrivning) hard-failar då i stället för att korrumpera D.

De befintliga per-modul-grindarna (derived.py:s `plausible`, energimyndigheten.py:s
dimensionskontroll, bra.py:s "exakt 1 rad") fångar tom/avkortad/strukturändrad data. Den HÄR
grinden lägger till det de inte fångar: en **fel-men-rimlig** serie (rätt storleksordning, fel
dimension — t.ex. fel åldersgrupp i AKU) via förankrade publicerade värden.

En förväntan (spec) är medvetet GROV — den ska fånga "fel serie / tom / stale", inte återskapa
källans exakta tal (det gör golden-testerna). Fält (alla valfria):
  min_points       minsta antal observationer i serien
  value_range      [lo, hi]; alla värden måste ligga inom (grov enhets-/storleksrimlighet)
  min_latest_year  serien måste nå minst detta år (annars död/stale källa)
  anchors          {period-sträng -> publicerat värde}; pinnar seriens IDENTITET (±rel_tol)
  rel_tol          relativ tolerans för anchors (default 0.05 — tål källrevisioner, fångar fel serie)

Specarna bor bredvid seriedefinitionen (build_fas2/build_fas3, bra/energimyndigheten/derived).
Ren funktion utan nätverk -> golden-testbar.
"""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from typing import Any

_YEAR_RE = re.compile(r"(?<!\d)(\d{4})(?!\d)")


class SeriesDriftError(ValueError):
    """En inläst serie matchar inte sin förväntan -> trolig käll-/dimensionsdrift."""


def _end_year(period: object) -> int | None:
    """Sista 4-siffriga året i en periodsträng ('2024', '2018-2019', '2024-2024') -> int.

    Tar SISTA året så ett äkta flerårsspann ('2018-2019') bedöms på sitt slutår för
    stale-kontrollen. Perioder utan 4-siffrigt år (kvartal/månad utan år) -> None.
    """
    years = _YEAR_RE.findall(str(period))
    return int(years[-1]) if years else None


def check_series(rows: Sequence[Mapping[str, Any]], spec: Mapping[str, Any] | None, label: str) -> None:
    """Validerar en inläst serie mot sin förväntan. Höjer SeriesDriftError vid avvikelse.

    rows: observations-rader (varje med 'period' + numeriskt 'value'). spec=None -> ingen kontroll
    (serien har ingen deklarerad förväntan än). label: människoläsbar serie-etikett för felmeddelandet.
    """
    if not spec:
        return
    values = [float(r["value"]) for r in rows if r.get("value") is not None]

    min_points = spec.get("min_points")
    if min_points is not None and len(rows) < int(min_points):
        raise SeriesDriftError(
            f"{label}: {len(rows)} punkter < min_points {min_points} (tom/avkortad serie — fel tabell?)"
        )

    vr = spec.get("value_range")
    if vr is not None and values:
        lo, hi = float(vr[0]), float(vr[1])
        bad = [v for v in values if v < lo or v > hi]
        if bad:
            raise SeriesDriftError(
                f"{label}: {len(bad)} värde(n) utanför [{lo}, {hi}], t.ex. {bad[:5]} "
                "(fel serie/enhet?)"
            )

    mly = spec.get("min_latest_year")
    if mly is not None:
        years = [y for y in (_end_year(r.get("period")) for r in rows) if y is not None]
        latest = max(years) if years else None
        if latest is None or latest < int(mly):
            raise SeriesDriftError(
                f"{label}: senaste år {latest} < min_latest_year {mly} (stale/död källa?)"
            )

    anchors = spec.get("anchors") or {}
    if anchors:
        by_period = {str(r["period"]): float(r["value"]) for r in rows if r.get("value") is not None}
        rel_tol = float(spec.get("rel_tol", 0.05))
        for period, expected in anchors.items():
            key = str(period)
            if key not in by_period:
                raise SeriesDriftError(
                    f"{label}: ankarperiod {key!r} saknas i serien (förskjuten/fel serie?)"
                )
            got = by_period[key]
            exp = float(expected)
            ok = abs(got) <= rel_tol if exp == 0 else abs(got - exp) <= rel_tol * abs(exp)
            if not ok:
                raise SeriesDriftError(
                    f"{label}: ankare {key}={got} ≠ förväntat {exp} (±{rel_tol:.0%}) -> fel serie"
                )
