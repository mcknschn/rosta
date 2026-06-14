"""Subnationellt ansvar (responsibility, level=regional/municipal) ur versionsstyrd config.

Deterministiskt — kräver ingen hämtning. Styresdatan (regioner i config/mappings.yaml,
kommuner i config/subnational_municipalities.yaml) är troget transkriberad ur SKR:s officiella
öppna data ("Styren i regioner 1994-2022" + "Styren i kommuner 1994-2022"); se
docs/done/fas1c_subnational_metod.md. Ingen handsatt poäng: en rad per (parti, geografi, mandatperiod)
där partiet ingår i det ledande styret.

strength = 1 / antal ledande riksdagspartier (1.0 vid enpartistyre) — lokala partier (ÖP)
räknas inte med i nämnaren, modellen bedömer bara de 8 riksdagspartierna.

Matar delpoäng C (subnationell makt) i Fas 5 via scorerun.regional_fractions()/municipal_fractions()
— som läser SAMMA config — och skrivs till warehouse (responsibility) för spårbarhet/claims/evidence.
"""

from __future__ import annotations

from typing import Any

from .. import config

REGION_SOURCE_PREFIX = "skr:styren_regioner"
MUNICIPAL_SOURCE_PREFIX = "skr:styren_kommuner"
TERMS = ("2014-2018", "2018-2022", "2022-2026")


def build_regional_responsibility() -> list[dict[str, Any]]:
    """En responsibility-rad per (parti, region, mandatperiod). level=regional.

    Höjer ValueError vid okänd partikod (aldrig tyst skip) så transkriberingsfel fångas.
    """
    sg = config.mappings().get("subnational_governance", {})
    regions = sg.get("regions") or {}
    term_source = sg.get("term_source", {})
    all_sources = sorted(sg.get("sources", {}))
    valid_parties = set(config.party_codes())
    rows: list[dict[str, Any]] = []
    for code in sorted(regions):
        for term, styre in regions[code].get("terms", {}).items():
            leading = styre.get("leading_parties", [])
            if not leading:
                continue
            strength = 1.0 / len(leading)
            src_keys = term_source.get(term) or all_sources
            src = "+".join(src_keys) if src_keys else "skr_styren_regioner"
            for party in leading:
                if party not in valid_parties:
                    raise ValueError(
                        f"Okänd partikod '{party}' i subnational_governance ({code} {term})"
                    )
                rows.append({
                    "id": f"resp:{party}:regional:{code}:{term}",
                    "party": party, "level": "regional", "geography": code,
                    "period": term, "role": "government", "strength": strength,
                    "source_ref": f"{REGION_SOURCE_PREFIX}:{term}:{code}:{src}",
                })
    return rows


def build_municipal_responsibility() -> list[dict[str, Any]]:
    """En responsibility-rad per (parti, kommun, mandatperiod). level=municipal.

    Läser config/subnational_municipalities.yaml (terms = [t2014-2018, t2018-2022, t2022-2026]).
    Höjer ValueError vid okänd partikod.
    """
    data = config.subnational_municipalities().get("municipalities") or {}
    valid_parties = set(config.party_codes())
    rows: list[dict[str, Any]] = []
    for code in sorted(data):
        terms = data[code].get("terms", [])
        for term, leading in zip(TERMS, terms, strict=False):
            if not leading:
                continue
            strength = 1.0 / len(leading)
            for party in leading:
                if party not in valid_parties:
                    raise ValueError(
                        f"Okänd partikod '{party}' i subnational_municipalities ({code} {term})"
                    )
                rows.append({
                    "id": f"resp:{party}:municipal:{code}:{term}",
                    "party": party, "level": "municipal", "geography": code,
                    "period": term, "role": "government", "strength": strength,
                    "source_ref": f"{MUNICIPAL_SOURCE_PREFIX}:{term}:{code}",
                })
    return rows


def build_subnational_responsibility() -> list[dict[str, Any]]:
    """Regionalt + kommunalt ansvar (för Fas 1-bygget till warehouse)."""
    return build_regional_responsibility() + build_municipal_responsibility()
