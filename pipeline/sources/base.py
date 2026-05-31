"""Gemensamt gränssnitt för källmoduler + reproducerbar cache med manifest.

Varje källmodul ärver Source och implementerar fetch()/normalize(). Råsvar cachas
under data/raw/<source>/<dataset>/<retrieved_at>.json och loggas i ett manifest
(käll-URL, dataset-id, fråga, hämtdatum, licens) så körningar blir reproducerbara.

Endast lokalt: inget av detta deployas.
"""

from __future__ import annotations

import json
import os
import re
from abc import ABC, abstractmethod
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .. import DATA_DIR

RAW_DIR = DATA_DIR / "raw"


def _safe(segment: str) -> str:
    """Saneras till en säker sökvägskomponent (inga separatorer eller '..')."""
    return re.sub(r"[^A-Za-z0-9._-]", "_", str(segment))


@dataclass(frozen=True, slots=True)
class Manifest:
    """Härkomst för en cachad hämtning."""

    source: str
    dataset_id: str
    url: str
    query: str
    retrieved_at: str  # ISO-datum, skickas in (Date är inte tillgängligt i scripten ovanför)
    license: str
    row_count: int | None = None


class Source(ABC):
    """Basklass för en officiell källa.

    Underklasser sätter `name` och `license` och implementerar fetch()/normalize().
    """

    name: str
    license: str

    def cache_path(self, dataset_id: str, retrieved_at: str) -> Path:
        # Sanera mot path traversal — käll-id:n får aldrig skriva utanför cache-trädet.
        return RAW_DIR / _safe(self.name) / _safe(dataset_id) / f"{_safe(retrieved_at)}.json"

    def write_cache(self, payload: Any, manifest: Manifest) -> Path:
        path = self.cache_path(manifest.dataset_id, manifest.retrieved_at)
        path.parent.mkdir(parents=True, exist_ok=True)
        # Atomiskt: skriv till temp och byt namn, så avbrott aldrig lämnar trunkerad JSON.
        tmp = path.with_name(path.name + ".tmp")
        with tmp.open("w", encoding="utf-8") as fh:
            json.dump({"manifest": asdict(manifest), "payload": payload}, fh, ensure_ascii=False)
        os.replace(tmp, path)
        return path

    @abstractmethod
    def fetch(self, retrieved_at: str) -> Iterable[Manifest]:
        """Hämtar råsvar från källan och cachar dem. Yieldar ett manifest per dataset."""

    @abstractmethod
    def normalize(self) -> Iterable[dict[str, Any]]:
        """Omvandlar cachat råsvar till observations/actions/responsibility-rader."""
