"""Lager 2: rådata (data/raw) -> warehouse-tabeller i data/warehouse.duckdb.

Producerar tre tidy-tabeller (se DATA.md):
  - observations    (objektiva indikatorvärden)
  - actions         (partiagerande: voteringar/motioner/budgetrader)
  - responsibility  (vem hade makt, på vilken nivå, när)

Implementeras i Fas 1-3. Rader valideras mot schemas/{observation,action,responsibility}.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any


def build_warehouse(rows: Iterable[dict[str, Any]]) -> None:  # pragma: no cover - Fas 1+
    raise NotImplementedError("Byggs i Fas 1: normalisera källrader till warehouse-tabeller.")
