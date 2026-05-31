"""Nationellt ansvar (responsibility, level=national) ur config/mappings.yaml.

Deterministiskt — kräver ingen hämtning. Regeringspartier får role=government (strength 1.0),
stödpartier role=support (strength 0.5). Matar delpoäng C (makt) i Fas 5.

Regionalt/kommunalt ansvar (SKR-styren) byggs när subnational_governance fyllts (se skr.py).
"""

from __future__ import annotations

from typing import Any

from .. import config

SOURCE_REF_PREFIX = "regeringskansliet:government_periods"


def _period_label(start: Any, end: Any) -> str:
    return f"{start}/{end if end else 'pagaende'}"


def build_national_responsibility() -> list[dict[str, Any]]:
    """En responsibility-rad per (parti, regeringsperiod). Idempotent id per rad."""
    periods = config.mappings().get("government_periods", [])
    valid_parties = set(config.party_codes())
    rows: list[dict[str, Any]] = []
    for gp in periods:
        label = _period_label(gp.get("start"), gp.get("end"))
        name = gp.get("name", label)
        for party in gp.get("parties", []):
            if party not in valid_parties:
                raise ValueError(f"Okänd partikod '{party}' i government_periods ({name})")
            rows.append({
                "id": f"resp:{party}:national:{gp.get('start')}",
                "party": party, "level": "national", "geography": "Riket",
                "period": label, "role": "government", "strength": 1.0,
                "source_ref": f"{SOURCE_REF_PREFIX}:{name}",
            })
        for party in gp.get("support_parties", []):
            if party not in valid_parties:
                raise ValueError(f"Okänd stödpartikod '{party}' i government_periods ({name})")
            rows.append({
                "id": f"resp:{party}:national:{gp.get('start')}:support",
                "party": party, "level": "national", "geography": "Riket",
                "period": label, "role": "support", "strength": 0.5,
                "source_ref": f"{SOURCE_REF_PREFIX}:{name}",
            })
    return rows
