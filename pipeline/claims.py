"""Lager 3a: warehouse -> claims (källbackade, granskningsbara påståenden).

Bygger provenance-claims (action/responsibility/observed_result) ur warehouse-tabellerna.
Dessa matar evidence.json (spårbarhet). evidence_effect-claims kommer separat ur
config/evidence_ledger.yaml (delpoäng B) när partikoppling finns (Fas 4b).
Tolkningsregler bor i config — inga fristående omdömen.
"""

from __future__ import annotations

from typing import Any

import duckdb


def build_claims(con: duckdb.DuckDBPyConnection) -> list[dict[str, Any]]:
    """Provenance-claims ur warehouse. Varje claim har minst en source_ref."""
    claims: list[dict[str, Any]] = []

    # Ansvar (C): en claim per (parti, nivå, period, roll). Regionala rader aggregeras
    # (en rad per region × period) till en summerande claim med regionantal — annars
    # kolliderar id:n och evidensindexet sväller. national: "Riket"; regional: antal regioner.
    for party, level, period, role, n, src in con.execute(
        "SELECT party, level, period, role, count(*), max(source_ref) FROM responsibility "
        "GROUP BY party, level, period, role"
    ).fetchall():
        if level == "national":
            statement = f"{party} hade {role} (nationellt) under {period}."
        else:
            unit = "region" if n == 1 else "regioner"
            statement = f"{party} ingick i det ledande styret i {n} {unit} ({level}) under {period}."
        claims.append({
            "id": f"claim:responsibility:{party}:{level}:{period}:{role}",
            "type": "responsibility", "party": party, "period": period,
            "statement": statement,
            "source_refs": [src],
        })

    # Agerande (A): en claim per (parti, kategori) aktivitetssumma.
    for party, category, total, src in con.execute(
        "SELECT party, category, sum(count), max(source_ref) FROM party_activity "
        "GROUP BY party, category"
    ).fetchall():
        claims.append({
            "id": f"claim:action:{party}:{category}:motioner",
            "type": "action", "party": party, "category": category,
            "statement": f"{party} lämnade {int(total)} motioner i utskott kopplade till {category}.",
            "source_refs": [src],
        })

    # Resultat (D): en claim per observation.
    for oid, category, indicator, period, value, src in con.execute(
        "SELECT id, category, indicator, period, value, source_ref FROM observations"
    ).fetchall():
        claims.append({
            "id": f"claim:observed_result:{oid}",
            "type": "observed_result", "category": category, "indicator": indicator,
            "period": str(period),
            "statement": f"{indicator} = {value} ({category}, {period}).",
            "source_refs": [src],
        })

    return claims
