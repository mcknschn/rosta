"""Förankringen för delpoäng A (ADR 0005): nollpunkten ligger i tid, inte tvärs partier.

A frågar hur stor andel av sin kraft ett parti lägger på en kategori. Före ADR 0005 mättes den
andelen mot de sju andra partierna, alltså mot fältet, och betyget kunde bara säga "mest av de
åtta". Efter ADR 0005 mäts den mot hur stor andel kategorin normalt fått under ett historiskt
fönster:

  a1  kategorins andel av de BESLUTADE utgiftsramarna i bet. FiU1, som medel över fönstret
  a2  kategorins andel av kammarens samtliga motioner under fönstret

Talen står i `config/a_forankring.yaml`, transkriberade ur officiella källor av
`pipeline/tools/a_forankring_transcribe.py`. Det finns INGEN runtime-parser: A är tyngsta
delpoängen och får aldrig kunna korrumperas av en bräcklig parser (samma regel som budget.py).

Saknat underlag ger HÅRD FAIL, aldrig en tyst nolla. En tyst nolla i en förankring blir en kvot
på +1, alltså toppbetyg åt alla, och det skulle vara det värsta tänkbara felet i A.

Rena funktioner med injicerbara fixturer -> golden-testbara utan livedata.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from . import budget, config


def _require_positive(shares: Mapping[str, float], half: str) -> None:
    """En förankring på noll finns inte, den saknas.

    Kvoten mot en nolla blir +1, alltså 5,00 till alla åtta partier, och en kategori utan
    underlag skulle då se ut som en kategori alla prioriterar maximalt. Det är det värsta
    tänkbara felet i A, så en saknad förankring hard-failar i stället.
    """
    empty = sorted(cat for cat, value in shares.items() if value <= 0)
    if empty:
        raise ValueError(f"a_forankring: {half} saknar förankring för {', '.join(empty)}")


def window(cfg: Mapping[str, Any] | None = None) -> tuple[int, int]:
    """(första året, sista året) i förankringsfönstret. Båda ändarna räknas med."""
    cfg = config.a_forankring() if cfg is None else cfg
    w = cfg["window"]
    return int(w["start"]), int(w["end"])


def a1_years(cfg: Mapping[str, Any] | None = None) -> list[int]:
    """Budgetåren a1 mäter, alltså a1:s eget fönster (ADR 0007 punkt 2 och 3).

    Fönstret börjar vid den SENASTE av a1:s två gränser och slutar vid senaste färdiga år.
    Den första gränsen bär förankringen (FiU1 listar utgiftsområde 1-27), den andra täljaren
    (alla åtta partier har en citerbar ram). Halvorna har egna fönster: a2 ska inte falla bara
    för att budgetkällan har en lucka (ADR 0007 punkt 3).
    """
    cfg = config.a_forankring() if cfg is None else cfg
    w = cfg["window"]
    bounds = [int(w["a1_bound"]), int(w["a1_frames_bound"]), int(w["start"])]
    return list(range(max(bounds), int(w["end"]) + 1))


def a2_period(cfg: Mapping[str, Any] | None = None) -> tuple[str, str]:
    """(från, till) som ISO-datum för a2:s fönster, läst ur förankringens egen period.

    Täljaren hämtas över exakt den här perioden (ADR 0007 punkt 1). Den är skild från
    `mappings.window`, som D och `responsibility` fortsätter använda oförändrad.
    """
    cfg = config.a_forankring() if cfg is None else cfg
    period = str(cfg["a2"]["chamber_motions"]["period"])
    frm, _, tom = period.partition("/")
    if not frm or not tom:
        raise ValueError(f"a_forankring: a2-perioden {period!r} går inte att läsa")
    return frm, tom


def a1_anchor_shares(
    category_ids: list[str],
    years: list[int] | None = None,
    cfg: Mapping[str, Any] | None = None,
    uo_map: Mapping[str, Any] | None = None,
) -> dict[str, float]:
    """kategori -> andel av de beslutade utgiftsramarna, som medel över a1:s budgetår.

    Samma andelsräkning som partiernas egna ramar (budget.category_shares_for_party), så andel
    och förankring är samma storhet mätt på två underlag. Nämnaren är hela ramen, alltså även de
    utgiftsområden som inte hör till någon kategori.

    `years` är de år TÄLJAREN täcker. ADR 0007 punkt 1 kräver att förankringen läggs på exakt
    dem: en kvot vars täljare och nämnare täcker olika år bär skillnaden mellan åren som om den
    vore en skillnad mellan partier. Utelämnas `years` används a1:s eget fönster.
    """
    cfg = config.a_forankring() if cfg is None else cfg
    umap = config.mappings()["expenditure_areas"] if uo_map is None else uo_map
    cat_uo_w = budget.category_uo_weights(umap)
    frames = cfg["a1"]["decided_frames"]
    years = a1_years(cfg) if years is None else sorted(years)
    if not years:
        raise ValueError("a_forankring: a1 saknar budgetår att förankra mot")

    per_year: list[dict[str, float]] = []
    for year in years:
        frame = frames.get(year)
        if frame is None:
            raise ValueError(f"a_forankring: budgetår {year} saknar beslutad ram")
        cells = {uo: float(frame[uo]) for uo in umap if uo in frame}
        missing = sorted(set(umap) - set(cells))
        if missing:
            raise ValueError(f"a_forankring {year}: saknar {', '.join(missing)}")
        per_year.append(budget.category_shares_for_party(cells, cat_uo_w))

    out = {cat: sum(y.get(cat, 0.0) for y in per_year) / len(per_year) for cat in category_ids}
    _require_positive(out, "a1")
    return out


def a2_anchor_shares(
    category_ids: list[str],
    cfg: Mapping[str, Any] | None = None,
    committee_map: Mapping[str, str] | None = None,
) -> dict[str, float]:
    """kategori -> andel av kammarens samtliga motioner i fönstret.

    Kammarens fördelning, inte de åtta partiernas poolade. Partipoolen är ett fältmått viktat
    efter hur många motioner varje parti skriver, alltså samma fel som ADR 0005 punkt 2 avvisar.
    """
    cfg = config.a_forankring() if cfg is None else cfg
    cmap = config.mappings()["committee_to_category"] if committee_map is None else committee_map
    counts = cfg["a2"]["chamber_motions"]["committees"]
    missing = sorted(set(cmap) - set(counts))
    if missing:
        raise ValueError(f"a_forankring: kammarsiffror saknas för {', '.join(missing)}")

    total = sum(float(counts[org]) for org in cmap)
    if total <= 0:
        raise ValueError(f"a_forankring: kammaren har {total} motioner i fönstret")
    per_cat = {cat: 0.0 for cat in category_ids}
    for org, cat in cmap.items():
        if cat in per_cat:
            per_cat[cat] += float(counts[org])
    out = {cat: n / total for cat, n in per_cat.items()}
    _require_positive(out, "a2")
    return out


def validate(cfg: Mapping[str, Any] | None = None) -> None:
    """Strukturinvarianter i a_forankring.yaml (höjer ValueError).

    Prövar formen, aldrig talen. Att talen matchar källan prövas av
    `python -m pipeline.tools.a_forankring_transcribe --audit`, som går mot riksdagen live.
    """
    cfg = config.a_forankring() if cfg is None else cfg
    for key in ("window", "a1", "a2"):
        if key not in cfg:
            raise ValueError(f"a_forankring.yaml saknar '{key}'")
    start, end = window(cfg)
    if start > end:
        raise ValueError(f"a_forankring: fönstret {start}-{end} går baklänges")
    for bound in ("a1_bound", "a1_frames_bound", "a2_bound"):
        if not isinstance((cfg["window"] or {}).get(bound), int):
            raise ValueError(f"a_forankring: gränsen '{bound}' saknas eller är inget år")
    if not a1_years(cfg):
        raise ValueError("a_forankring: a1:s fönster är tomt")
    a2_period(cfg)

    frames = (cfg["a1"] or {}).get("decided_frames") or {}
    for year in range(start, end + 1):
        frame = frames.get(year)
        if frame is None:
            raise ValueError(f"a_forankring: budgetår {year} saknas i fönstret")
        if not str(frame.get("source_ref", "")).strip():
            raise ValueError(f"a_forankring {year}: saknar source_ref")
        for uo, amount in frame.items():
            if uo.startswith("UO") and not isinstance(amount, (int, float)):
                raise ValueError(f"a_forankring {year}/{uo}: belopp ej numeriskt: {amount!r}")

    chamber = (cfg["a2"] or {}).get("chamber_motions") or {}
    if not str(chamber.get("source_ref", "")).strip():
        raise ValueError("a_forankring: kammarmotionerna saknar source_ref")
    for org, n in (chamber.get("committees") or {}).items():
        if not isinstance(n, int) or n < 0:
            raise ValueError(f"a_forankring: kammaren/{org} = {n!r} är inget antal")
