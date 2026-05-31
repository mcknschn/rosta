"""Lager 2: lokal analytisk warehouse i DuckDB.

Tre tidy-tabeller (se DATA.md): observations, actions, responsibility.
Rader valideras mot motsvarande JSON-schema innan de skrivs (integritetskrav).
Endast lokalt — data/warehouse.duckdb deployas aldrig.
"""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path
from typing import Any

import duckdb

from . import DATA_DIR, schema

WAREHOUSE_PATH = DATA_DIR / "warehouse.duckdb"

# Kolumner per tabell (ordning spelar roll för INSERT). Matchar schemas/*.schema.json.
COLUMNS: dict[str, list[str]] = {
    "observations": [
        "id", "category", "submeasure", "indicator", "period",
        "value", "unit", "geography", "source_ref",
    ],
    "actions": [
        "id", "party", "kind", "category", "submeasure", "period",
        "expenditure_area", "amount_sek", "vote", "outcome", "document_ref", "source_ref",
    ],
    "responsibility": [
        "id", "party", "level", "geography", "period", "role", "strength", "source_ref",
    ],
    # Derivad aggregatsignal (delpoäng A, lagstiftningsaktivitet). Inget JSON-schema.
    "party_activity": [
        "party", "category", "committee", "kind", "period", "count", "source_ref",
    ],
}

_DDL: dict[str, str] = {
    "observations": """CREATE TABLE IF NOT EXISTS observations(
        id TEXT PRIMARY KEY, category TEXT, submeasure TEXT, indicator TEXT, period TEXT,
        value DOUBLE, unit TEXT, geography TEXT, source_ref TEXT)""",
    "actions": """CREATE TABLE IF NOT EXISTS actions(
        id TEXT PRIMARY KEY, party TEXT, kind TEXT, category TEXT, submeasure TEXT, period TEXT,
        expenditure_area TEXT, amount_sek DOUBLE, vote TEXT, outcome TEXT,
        document_ref TEXT, source_ref TEXT)""",
    "responsibility": """CREATE TABLE IF NOT EXISTS responsibility(
        id TEXT PRIMARY KEY, party TEXT, level TEXT, geography TEXT, period TEXT,
        role TEXT, strength DOUBLE, source_ref TEXT)""",
    "party_activity": """CREATE TABLE IF NOT EXISTS party_activity(
        party TEXT, category TEXT, committee TEXT, kind TEXT, period TEXT,
        count BIGINT, source_ref TEXT,
        PRIMARY KEY (party, committee, kind, period))""",
}

# Tabellnamn -> schemanamn för radvalidering.
_SCHEMA = {"observations": "observation", "actions": "action", "responsibility": "responsibility"}


def connect(path: Path | str = WAREHOUSE_PATH, read_only: bool = False) -> duckdb.DuckDBPyConnection:
    """Öppnar (eller skapar) warehouse och säkerställer att tabellerna finns.

    Använd ':memory:' som path i tester.
    """
    if path != ":memory:":
        Path(path).parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(path), read_only=read_only)
    if not read_only:  # DDL kan inte köras i read-only-läge
        for ddl in _DDL.values():
            con.execute(ddl)
    return con


def upsert(
    con: duckdb.DuckDBPyConnection,
    table: str,
    rows: Iterable[dict[str, Any]],
    validate: bool = True,
) -> int:
    """Skriver rader med INSERT OR REPLACE (idempotent på id). Returnerar antal rader."""
    if table not in COLUMNS:
        raise ValueError(f"Okänd tabell: {table}")
    cols = COLUMNS[table]
    schema_name = _SCHEMA.get(table)  # aggregat (party_activity) saknar JSON-schema
    placeholders = ", ".join("?" for _ in cols)
    sql = f"INSERT OR REPLACE INTO {table} ({', '.join(cols)}) VALUES ({placeholders})"
    n = 0
    for row in rows:
        if validate and schema_name:
            schema.validate(schema_name, row)
        con.execute(sql, [row.get(c) for c in cols])
        n += 1
    return n


def count(con: duckdb.DuckDBPyConnection, table: str) -> int:
    return con.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
