"""Delpoäng A, a1 (budgetprioritering): andel av partiets föreslagna anslag per kategori.

Läser config/budget_ramar.yaml — officiella, källbelagda utgiftsramar per utgiftsområde (UO)
per parti per budgetår — och beräknar a1-andelar deterministiskt. INGA belopp hittas på här;
config är en kurerings-gated seed (version 0, kräver mänsklig slutgranskning, precis som
party_positions.yaml). Det finns ingen runtime-parser av budgetdokument: beloppen är manuellt
transkriberade ur officiella källor (FiU1 rambeslut + partiernas budgetmotioner) och varje frame
citerar sin källa, så a1 kan aldrig korrumperas av en bräcklig parser (A är tyngsta delpoängen).

HÅRD GRIND (Codex-konsensus): a1 aktiveras för en (budgetår, kategori) ENDAST när alla 8 partier
har en verifierad ram som täcker VARJE UO i kategorin, i ALLA inkluderade budgetår. Annars faller
A tillbaka på a2 för den kategorin. En saknad/ogiltig cell ger HÅRD FAIL (aldrig tyst 0).

Andelen som räknas här är RÅ. Vad den sedan jämförs med avgörs i pipeline/anchor.py: sedan
ADR 0005 mäts den mot de beslutade utgiftsramarnas andel över ett historiskt fönster, inte mot
de sju andra partierna.

Rena funktioner med injicerbara fixturer -> golden-testbara utan livedata.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any

from . import config

_UO_RE = re.compile(r"^UO\d+$")


def category_uo_weights(uo_map: Mapping[str, Any]) -> dict[str, dict[str, float]]:
    """kategori -> {UO -> vikt} ur mappings.expenditure_areas (ett UO kan dela på flera kat.)."""
    out: dict[str, dict[str, float]] = {}
    for uo, spec in uo_map.items():
        for cat, w in (spec.get("map") or {}).items():
            out.setdefault(cat, {})[uo] = float(w)
    return out


def resolve_frames(year_block: Mapping[str, Any]) -> dict[str, dict[str, float]]:
    """parti -> {UO -> belopp} för ett budgetår via namngivna ramar + party_frame-mappning.

    Endast UO-nycklar (UO1..UO27) plockas ur en frame; metadata (source_ref m.m.) ignoreras.
    Okänd frame-referens, icke-numeriskt belopp eller saknad party_frame -> hård fail.
    """
    ramar = year_block.get("ramar") or {}
    party_frame = year_block.get("party_frame") or {}
    out: dict[str, dict[str, float]] = {}
    for party, pf in party_frame.items():
        fname = pf.get("frame") if isinstance(pf, Mapping) else None
        if fname not in ramar:
            raise ValueError(f"party_frame[{party}] pekar på okänd frame {fname!r}")
        frame = ramar[fname]
        cells: dict[str, float] = {}
        for k, v in frame.items():
            if not _UO_RE.match(str(k)):
                continue
            if not isinstance(v, (int, float)):
                raise ValueError(f"Icke-numeriskt belopp {frame.get('__name__', fname)}/{k}={v!r}")
            cells[k] = float(v)
        out[party] = cells
    return out


def category_shares_for_party(
    frame: Mapping[str, float], cat_uo_w: Mapping[str, Mapping[str, float]]
) -> dict[str, float]:
    """kategori -> andel av partiets TOTALA anslag (Σ alla UO) som går till kategorins UO.

    Relativ prioritering (som a2), inte om mer pengar är rätt. Total <= 0 -> hård fail.
    """
    total = sum(frame.values())
    if total <= 0:
        raise ValueError(f"Partiets totala ram måste vara > 0, fick {total}")
    out: dict[str, float] = {}
    for cat, uow in cat_uo_w.items():
        out[cat] = sum(frame.get(uo, 0.0) * w for uo, w in uow.items()) / total
    return out


def _year_active_categories(
    frames: Mapping[str, dict[str, float]],
    cat_uo_w: Mapping[str, Mapping[str, float]],
    parties: list[str],
    category_ids: list[str],
) -> set[str]:
    """Kategorier där ALLA partier har ram för VARJE UO i kategorin (annars a2-fallback)."""
    if not all(p in frames for p in parties):
        return set()
    active: set[str] = set()
    for cat in category_ids:
        uos = list(cat_uo_w.get(cat, {}))
        if not uos:
            continue  # kategori utan UO-koppling kan aldrig få a1 (t.ex. om map saknas)
        if all(all(uo in frames[p] for uo in uos) for p in parties):
            active.add(cat)
    return active


def shared_frame_years(ramar_cfg: Mapping[str, Any] | None = None) -> list[tuple[str, int]]:
    """(parti, antal år) där partiets ram bärs av mer än ett parti, störst först.

    Ett regeringsår mäts på koalitionens ram och ett år med gemensam budgetmotion på
    undertecknarnas, så a1 kan inte skilja de partierna åt de åren. Talet hör hemma i
    metodrutan: ADR 0007 Följder nämner förhållandet, men läsaren ska se hur stort det är.
    Tom config -> [] så metodrutan kan tiga i stället för att påstå noll.
    """
    cfg = config.budget_ramar() if ramar_cfg is None else ramar_cfg
    years = (cfg or {}).get("budget_years") or {}
    if not years:
        return []
    counts = {p: 0 for p in config.party_codes()}
    for block in years.values():
        frames = [pf.get("frame") for pf in (block.get("party_frame") or {}).values()]
        for party, pf in (block.get("party_frame") or {}).items():
            if party in counts and frames.count(pf.get("frame")) > 1:
                counts[party] += 1
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))


def a1_shares(
    category_ids: list[str],
    parties: list[str],
    ramar_cfg: Mapping[str, Any] | None = None,
    uo_map: Mapping[str, Any] | None = None,
) -> tuple[dict[tuple[str, str], float], set[str], list[int]]:
    """((parti,kategori) -> a1-andel, aktiva kategorier, budgetåren täljaren täcker).

    Andelen är medel över de inkluderade budgetåren. a1 är aktiv för en kategori endast om den
    var aktiv (alla 8 partier × alla kategori-UO) i VARJE budgetår (snitt-skärning). Tom config
    -> ({}, set(), []) så A faller på a2 (ingen regression).

    Åren returneras därför att förankringen ska läggas på exakt dem (ADR 0007 punkt 1). Den
    som räknar kvoten ska inte behöva lista ut vilka år täljaren råkade täcka.
    """
    cfg = config.budget_ramar() if ramar_cfg is None else ramar_cfg
    umap = config.mappings()["expenditure_areas"] if uo_map is None else uo_map
    cat_uo_w = category_uo_weights(umap)
    years = (cfg or {}).get("budget_years") or {}
    if not years:
        return {}, set(), []

    per_year_shares: dict[Any, dict[tuple[str, str], float]] = {}
    per_year_active: list[set[str]] = []
    for y, block in years.items():
        frames = resolve_frames(block)
        per_year_active.append(_year_active_categories(frames, cat_uo_w, parties, category_ids))
        sh: dict[tuple[str, str], float] = {}
        for p in parties:
            if p not in frames:
                continue
            pcs = category_shares_for_party(frames[p], cat_uo_w)
            for cat in category_ids:
                sh[(p, cat)] = pcs.get(cat, 0.0)
        per_year_shares[y] = sh

    active = set.intersection(*per_year_active) if per_year_active else set()
    shares: dict[tuple[str, str], float] = {}
    for p in parties:
        for cat in category_ids:
            vals = [per_year_shares[y][(p, cat)] for y in years if (p, cat) in per_year_shares[y]]
            if vals:
                shares[(p, cat)] = sum(vals) / len(vals)
    return shares, active, sorted(int(y) for y in years)


def parties_matching_adopted(
    parties: list[str],
    decided_frames: Mapping[int, Mapping[str, Any]],
    ramar_cfg: Mapping[str, Any] | None = None,
) -> list[str]:
    """Partier vars ram sammanfaller med den ANTAGNA ramen i VARJE budgetår i fönstret.

    Underlaget till villkorsklausulen i ADR 0007 punkt 4. Ett parti vars ram är den antagna i
    varje år har ingen egen nollpunkt: kvoten mot förankringen blir densamma som förankringens
    egen kvot mot sig själv, och partiet landar mitt på skalan i varje kategori av konstruktion.
    Klausulen är ADR 0005:s förkastade alternativ "Regeringens ram som nollpunkt", skrivet som
    ett prov, så att ett kort fönster inte kan återinföra det bakvägen.
    """
    cfg = config.budget_ramar() if ramar_cfg is None else ramar_cfg
    years = (cfg or {}).get("budget_years") or {}
    if not years:
        return []
    out: list[str] = []
    for party in parties:
        matches = True
        for year, block in years.items():
            decided = decided_frames.get(int(year))
            frame_name = ((block.get("party_frame") or {}).get(party) or {}).get("frame")
            frame = (block.get("ramar") or {}).get(frame_name)
            if decided is None or frame is None:
                matches = False
                break
            uos = [k for k in frame if _UO_RE.match(str(k))]
            if not uos or any(float(frame[uo]) != float(decided.get(uo, float("nan")))
                              for uo in uos):
                matches = False
                break
        if matches:
            out.append(party)
    return out


def a1_admissible(
    parties: list[str],
    decided_frames: Mapping[int, Mapping[str, Any]],
    ramar_cfg: Mapping[str, Any] | None = None,
) -> tuple[bool, list[str]]:
    """Villkorsklausulen (ADR 0007 punkt 4): (får a1 räknas, partierna som fällde den).

    a1 är otillåten om NÅGOT partis ram sammanfaller med den antagna ramen i varje år i
    fönstret. Faller klausulen ut, faller a1 ur A för alla kategorier, och A blir a2 ensam.
    """
    offenders = parties_matching_adopted(parties, decided_frames, ramar_cfg)
    return not offenders, offenders


def validate(cfg: Mapping[str, Any] | None = None, parties: list[str] | None = None) -> None:
    """Strukturinvarianter för budget_ramar.yaml (höjer ValueError). Tom config är giltig.

    Per budgetår: varje party_frame-parti (måste vara exakt de 8) pekar på en namngiven ram;
    varje ram har source_ref; alla UO-belopp numeriska; varje frame täcker samma UO-mängd.
    """
    cfg = config.budget_ramar() if cfg is None else cfg
    parties = config.party_codes() if parties is None else parties
    years = (cfg or {}).get("budget_years") or {}
    for y, block in years.items():
        ramar = block.get("ramar") or {}
        pf = block.get("party_frame") or {}
        if set(pf) != set(parties):
            raise ValueError(f"budget_ramar {y}: party_frame måste täcka exakt {sorted(parties)}, "
                             f"har {sorted(pf)}")
        for fname, frame in ramar.items():
            if not str(frame.get("source_ref", "")).strip():
                raise ValueError(f"budget_ramar {y}: frame {fname!r} saknar source_ref")
            for k, v in frame.items():
                if _UO_RE.match(str(k)) and not isinstance(v, (int, float)):
                    raise ValueError(f"budget_ramar {y}/{fname}/{k}: belopp ej numeriskt: {v!r}")
        uo_sets = {
            fname: frozenset(k for k in frame if _UO_RE.match(str(k)))
            for fname, frame in ramar.items()
        }
        if len(set(uo_sets.values())) > 1:
            raise ValueError(f"budget_ramar {y}: ramar täcker olika UO-mängder: "
                             f"{ {f: sorted(s) for f, s in uo_sets.items()} }")
        for party, spec in pf.items():
            if spec.get("frame") not in ramar:
                raise ValueError(f"budget_ramar {y}: party_frame[{party}] -> okänd frame "
                                 f"{spec.get('frame')!r}")
