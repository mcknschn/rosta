"""Riksdagens öppna data (data.riksdagen.se) — delpoäng A (faktiskt agerande).

Två signaler:
  1. Motionsaktivitet (a2): antal motioner per (parti, utskott) för hela fönstret,
     via dokumentlistans @traffar. Utskott -> kategori via mappings.committee_to_category.
     Full täckning, billigt (en request per parti×utskott). -> party_activity-tabellen.
  2. Voteringar (avgränsat prov): per-ledamot-röster aggregeras till partinivå per votering,
     kategori via beteckningens utskottsprefix. -> actions-tabellen (kind=votering).

Allt råsvar cachas i data/raw/riksdagen/ med manifest (idempotent, reproducerbart).
API:t verifierat live 2026-05-29 (HTTP 200, JSON). Inget deployas.
"""

from __future__ import annotations

import json
import re
import time
from collections import Counter
from dataclasses import asdict
from typing import Any

import httpx

from .. import config
from .base import RAW_DIR, Manifest, _safe

BASE = "https://data.riksdagen.se"
LICENSE = "Fri vidarespridning med källangivelse (källa: Sveriges riksdag)"
_UA = {"User-Agent": "rosta-datapipeline/0.1 (civic-tech; official swedish open data)"}
_BETECKNING_PREFIX = re.compile(r"^([A-Za-zÅÄÖåäö]+)")
_ROST_MAP = {"Ja": "ja", "Nej": "nej", "Avstår": "avstar", "Frånvarande": "franvarande"}


def _client() -> httpx.Client:
    return httpx.Client(timeout=60, headers=_UA, follow_redirects=True)


def _cache(dataset_id: str, retrieved_at: str, url: str, query: str, payload: Any, rows: int) -> None:
    path = RAW_DIR / "riksdagen" / _safe(dataset_id) / f"{_safe(retrieved_at)}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    man = Manifest(
        source="riksdagen", dataset_id=dataset_id, url=url, query=query,
        retrieved_at=retrieved_at, license=LICENSE, row_count=rows,
    )
    tmp = path.with_name(path.name + ".tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        json.dump({"manifest": asdict(man), "payload": payload}, fh, ensure_ascii=False)
    tmp.replace(path)


def committee_from_beteckning(beteckning: str) -> str:
    m = _BETECKNING_PREFIX.match(beteckning or "")
    return m.group(1).upper() if m else ""


def fetch_motion_counts(
    retrieved_at: str, frm: str | None = None, tom: str | None = None, delay: float = 0.3
) -> list[dict[str, Any]]:
    """party_activity-rader: antal motioner per (parti, utskott) i a2:s fönster.

    Fönstret är A:s EGET och kommer ur förankringens period (`anchor.a2_period`), inte ur
    `mappings.window`. ADR 0007 punkt 1 kräver att a2:s täljare täcker samma period som a2:s
    förankring; `mappings.window` står oförändrad och används fortsatt av D och responsibility.
    """
    from .. import anchor  # sent, så sources kan importeras utan att dra in scoringkedjan

    if frm is None or tom is None:
        default_frm, default_tom = anchor.a2_period()
        frm, tom = frm or default_frm, tom or default_tom
    cmap: dict[str, str] = config.mappings()["committee_to_category"]
    parties = config.party_codes()
    period = f"{frm}/{tom}"
    rows: list[dict[str, Any]] = []
    raw: dict[str, Any] = {}
    with _client() as c:
        for party in parties:
            for org, category in cmap.items():
                q = f"doktyp=mot&parti={party}&org={org}&from={frm}&tom={tom}&utformat=json&sz=1"
                url = f"{BASE}/dokumentlista/?{q}"
                resp = c.get(url)
                resp.raise_for_status()
                traffar = int(resp.json()["dokumentlista"]["@traffar"])
                rows.append({
                    "party": party, "category": category, "committee": org,
                    "kind": "motion", "period": period, "count": traffar,
                    "source_ref": url,
                })
                raw[f"{party}:{org}"] = traffar
                time.sleep(delay)
    _cache(
        "motion_counts", retrieved_at, f"{BASE}/dokumentlista/",
        "doktyp=mot per parti×org", raw, len(rows),
    )
    return rows


def fetch_votes_sample(
    retrieved_at: str, rm: str = "2024/25", max_pages: int = 6, sz: int = 500, delay: float = 0.4
) -> list[dict[str, Any]]:
    """actions-rader (kind=votering): per (parti, votering) majoritetsröst, kategori via beteckning.

    Avgränsat prov (max_pages) för att bevisa per-action-vägen — täckning loggas av anroparen.
    """
    cmap: dict[str, str] = config.mappings()["committee_to_category"]
    cmap_upper = {k.upper(): v for k, v in cmap.items()}  # beteckningsprefix matchas skiftlägesokänsligt
    valid = set(config.party_codes())
    # (votering_id, parti) -> Counter(rost);  votering_id -> (beteckning, dok_id)
    tally: dict[tuple[str, str], Counter] = {}
    meta: dict[str, tuple[str, str]] = {}
    rm_enc = rm.replace("/", "%2F")
    total_rows = 0
    with _client() as c:
        for p in range(1, max_pages + 1):
            url = f"{BASE}/voteringlista/?rm={rm_enc}&utformat=json&sz={sz}&p={p}"
            resp = c.get(url)
            resp.raise_for_status()
            votes = resp.json().get("voteringlista", {}).get("votering", [])
            if not votes:
                break
            for v in votes:
                party = (v.get("parti") or "").upper()
                if party not in valid:
                    continue
                vid = v.get("votering_id", "")
                tally.setdefault((vid, party), Counter())[v.get("rost", "")] += 1
                meta[vid] = (v.get("beteckning", ""), v.get("dok_id", ""))
                total_rows += 1
            time.sleep(delay)

    rows: list[dict[str, Any]] = []
    for (vid, party), counter in tally.items():
        beteckning, dok_id = meta.get(vid, ("", ""))
        committee = committee_from_beteckning(beteckning)
        category = cmap_upper.get(committee)
        if category is None:
            continue  # utskott utan kategorimappning hoppas över (loggas i count-diffen)
        majority = counter.most_common(1)[0][0]
        row: dict[str, Any] = {
            "id": f"action:{party}:votering:{vid}",
            "party": party, "kind": "votering", "category": category,
            "period": rm, "outcome": "unknown", "document_ref": dok_id,
            "source_ref": f"{BASE}/voteringlista/?rm={rm_enc}",
        }
        vote = _ROST_MAP.get(majority)
        if vote:
            row["vote"] = vote
        rows.append(row)
    _cache(f"votes_{rm.replace('/', '_')}", retrieved_at, f"{BASE}/voteringlista/?rm={rm_enc}",
           f"rm={rm} max_pages={max_pages}", {"ledamot_rows": total_rows, "voteringar": len(meta)}, len(rows))
    return rows
