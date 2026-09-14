"""Delpoäng A, a1 (budgetprioritering): andel av partiets föreslagna anslag per kategori.

Läser config/budget_ramar.yaml — officiella, källbelagda utgiftsramar per utgiftsområde (UO)
per parti per budgetår — och beräknar a1-andelar deterministiskt. INGA belopp hittas på här;
config är en kurerings-gated seed (version 0, kräver mänsklig slutgranskning, precis som
party_positions.yaml). Det finns ingen runtime-parser av budgetdokument: beloppen är manuellt
transkriberade ur officiella källor (FiU1 rambeslut + partiernas budgetmotioner) och varje frame
citerar sin källa, så a1 kan aldrig korrumperas av en bräcklig parser (A är tyngsta delpoängen).

HÅRD GRIND (Codex-konsensus): a1 aktiveras för en (budgetår, kategori) ENDAST när varje parti har
en verifierad ram som täcker VARJE UO i kategorin, i varje budgetår PARTIET SJÄLVT mäts på. Annars
faller A tillbaka på a2 för den kategorin. En saknad/ogiltig cell ger HÅRD FAIL (aldrig tyst 0).

ADR 0017 lossade grindens räckvidd från alla partier per år till partiet självt (punkt 5), och
höll fönstret orört: varje kategori mäter samma år, och varje parti samma årsmängd i alla sju
kategorier. Uteslutningen som gjorde lossningen nödvändig är en KLASSREGEL i config/scoring.yaml
(A_agerande.a1_exclusions): ett parti-år vars enda citerbara grund är en röst i rambeslutet bär
inget besked om partiets egen fördelning över de 27 utgiftsområdena, alltså ett giltighetsfel
(ADR 0011 punkt 2 steg 2). `basis` i budgetconfigen bokför källan och står orört.

Andelen som räknas här är RÅ. Vad den sedan jämförs med avgörs i pipeline/anchor.py: sedan
ADR 0005 mäts den mot de beslutade utgiftsramarnas andel över ett historiskt fönster, inte mot
de sju andra partierna.

Rena funktioner med injicerbara fixturer -> golden-testbara utan livedata.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any, NamedTuple

from . import config

_UO_RE = re.compile(r"^UO\d+$")
# Källraden för en voteringsgrund citerar voteringen. Provet går på NOTEN och aldrig på `role`:
# de tre fälten delar i dag exakt samma 120 parti-år, så bara källraden visar vad regeln vilar
# på (ADR 0017 diagnos 4). Rollen är C:s fråga (ADR 0001).
_VOTERING_RE = re.compile(r"votering", re.IGNORECASE)


def note_cites_votering(note: str) -> bool:
    """Citerar källraden en votering? Enda källan till vad "citerar en votering" betyder."""
    return bool(_VOTERING_RE.search(note or ""))


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


def _covered_categories(
    frame: Mapping[str, float],
    cat_uo_w: Mapping[str, Mapping[str, float]],
    category_ids: list[str],
) -> set[str]:
    """Kategorier där partiets ram täcker VARJE UO i kategorin (annars a2-fallback).

    Grindens fråga är oförändrad efter ADR 0017. Bara dess räckvidd flyttade: den ställs nu
    per parti och år, och en kategori är a1-aktiv först när svaret är ja för varje parti i
    varje år partiet självt mäts på (se a1_shares).
    """
    active: set[str] = set()
    for cat in category_ids:
        uos = list(cat_uo_w.get(cat, {}))
        if not uos:
            continue  # kategori utan UO-koppling kan aldrig få a1 (t.ex. om map saknas)
        if all(uo in frame for uo in uos):
            active.add(cat)
    return active


def excluded_party_years(
    ramar_cfg: Mapping[str, Any] | None = None,
    exclusions: list[dict[str, Any]] | None = None,
) -> dict[str, set[int]]:
    """parti -> budgetår som en KLASSREGEL håller utanför a1 (ADR 0017 punkt 1 och 3).

    Regeln selekterar på `basis`, alltså på vad källan belägger, och aldrig på rollen. Den
    lever i config/scoring.yaml: budgetconfigen är autogenererad och bokför källan, medan
    uteslutningen är modellens dom (ADR 0011 punkt 3).

    Varje parti i configen får en nyckel, också när mängden är tom, så en anropare aldrig
    behöver skilja "inget uteslutet" från "partiet finns inte".
    """
    cfg = config.budget_ramar() if ramar_cfg is None else ramar_cfg
    regler = config.a1_exclusions() if exclusions is None else exclusions
    years = (cfg or {}).get("budget_years") or {}
    out: dict[str, set[int]] = {}
    for y, block in years.items():
        for party, spec in (block.get("party_frame") or {}).items():
            out.setdefault(party, set())
            if any(spec.get("basis") == regel["basis"] for regel in regler):
                out[party].add(int(y))
    return out


def valid_party_years(
    ramar_cfg: Mapping[str, Any] | None = None,
    exclusions: list[dict[str, Any]] | None = None,
    parties: list[str] | None = None,
) -> dict[str, list[int]]:
    """parti -> budgetåren a1 mäter partiet på, alltså åren med ram minus klassreglernas.

    Enda källan till årsmängden. Både täljaren (a1_shares), förankringen (ADR 0007 punkt 1),
    villkorsklausulen (ADR 0017 punkt 8) och metodrutans delningstal räknar på den, så de
    aldrig kan hamna på olika årsmängder.
    """
    cfg = config.budget_ramar() if ramar_cfg is None else ramar_cfg
    parties = config.party_codes() if parties is None else parties
    years = (cfg or {}).get("budget_years") or {}
    excluded = excluded_party_years(cfg, exclusions)
    out: dict[str, list[int]] = {p: [] for p in parties}
    for y, block in years.items():
        pf = block.get("party_frame") or {}
        for party in parties:
            if party in pf and int(y) not in excluded.get(party, set()):
                out[party].append(int(y))
    return {p: sorted(ar) for p, ar in out.items()}


class SharedFrames(NamedTuple):
    """Delningstalet per parti, redovisat per grund (ADR 0017 godkännandetest regel 9)."""

    party: str
    shared: int      # år där partiets ram bärs av mer än ett parti, av de giltiga åren
    valid: int       # partiets giltiga år, alltså nämnaren talet ska läsas mot
    excluded: int    # parti-år som en klassregel håller utanför a1


def shared_frame_years(
    ramar_cfg: Mapping[str, Any] | None = None,
    exclusions: list[dict[str, Any]] | None = None,
) -> list[SharedFrames]:
    """Delningen per parti, störst först, räknad på de år a1 faktiskt mäter partiet.

    Ett regeringsår mäts på koalitionens ram och ett år med gemensam budgetmotion på
    undertecknarnas, så a1 kan inte skilja de partierna åt de åren. Talet hör hemma i
    metodrutan: ADR 0007 Följder nämner förhållandet, men läsaren ska se hur stort det är.

    Efter ADR 0017 bär raden TVÅ tal: delningen räknas på partiets giltiga år, och de
    uteslutna parti-åren står i en egen kolumn. Att bara byta ut den ena vektorn mot den
    andra vore att byta ett missvisande tal mot ett annat.

    Tom config -> [] så metodrutan kan tiga i stället för att påstå noll.
    """
    cfg = config.budget_ramar() if ramar_cfg is None else ramar_cfg
    years = (cfg or {}).get("budget_years") or {}
    if not years:
        return []
    giltiga = valid_party_years(cfg, exclusions)
    utesluten = excluded_party_years(cfg, exclusions)
    counts = {p: 0 for p in config.party_codes()}
    for y, block in years.items():
        pf = block.get("party_frame") or {}
        frames = [spec.get("frame") for spec in pf.values()]
        for party, spec in pf.items():
            if (party in counts and int(y) in giltiga.get(party, [])
                    and frames.count(spec.get("frame")) > 1):
                counts[party] += 1
    return sorted(
        (SharedFrames(p, n, len(giltiga.get(p, [])), len(utesluten.get(p, set())))
         for p, n in counts.items()),
        key=lambda r: (-r.shared, r.party),
    )


def a1_shares(
    category_ids: list[str],
    parties: list[str],
    ramar_cfg: Mapping[str, Any] | None = None,
    uo_map: Mapping[str, Any] | None = None,
    exclusions: list[dict[str, Any]] | None = None,
) -> tuple[dict[tuple[str, str], float], set[str], dict[str, list[int]]]:
    """((parti,kategori) -> a1-andel, aktiva kategorier, parti -> budgetåren täljaren täcker).

    Andelen är medel över PARTIETS giltiga budgetår. a1 är aktiv för en kategori endast om
    varje parti har ram för varje kategori-UO i varje år partiet självt mäts på. Tom config
    -> ({}, set(), {}) så A faller på a2 (ingen regression).

    Åren returneras PER PARTI därför att förankringen ska läggas på exakt dem (ADR 0007
    punkt 1, ADR 0017 punkt 6). Den som räknar kvoten ska inte behöva lista ut vilka år
    täljaren råkade täcka, och en enda årslista för alla åtta lät en avvikelse per parti
    passera osedd (ADR 0017 diagnos 6).

    HÅRD FAIL när ett parti tappar ett år som ingen klassregel förklarar. Ett tyst medel över
    "de år partiet råkar finnas i" är precis det hålet regeln stänger.
    """
    cfg = config.budget_ramar() if ramar_cfg is None else ramar_cfg
    umap = config.mappings()["expenditure_areas"] if uo_map is None else uo_map
    cat_uo_w = category_uo_weights(umap)
    years = (cfg or {}).get("budget_years") or {}
    if not years:
        return {}, set(), {}

    giltiga = valid_party_years(cfg, exclusions, parties)
    utesluten = excluded_party_years(cfg, exclusions)
    alla_ar = {int(y) for y in years}
    for p in parties:
        oforklarade = alla_ar - set(giltiga[p]) - utesluten.get(p, set())
        if oforklarade:
            raise ValueError(
                f"budget_ramar: {p} saknar ram {sorted(oforklarade)} utan en klassregel som "
                "förklarar luckan (ADR 0017 godkännandetest 3)"
            )
        if not giltiga[p]:
            # Utan giltiga år finns ingen fråga att ställa till grinden för partiet, och att
            # då låta de sju andra avgöra den vore en tyst grind av precis det slag ADR 0017
            # diagnos 6 tog fram i ljuset. a1 kan inte mätas för partiet, och det ska sägas.
            raise ValueError(
                f"budget_ramar: {p} har inga giltiga budgetår kvar, så a1 kan inte mätas för "
                "partiet (ADR 0017 punkt 5)"
            )

    per_year_shares: dict[int, dict[str, dict[str, float]]] = {}
    per_year_cover: dict[int, dict[str, set[str]]] = {}
    for y, block in years.items():
        frames = resolve_frames(block)
        per_year_shares[int(y)] = {
            p: category_shares_for_party(frames[p], cat_uo_w) for p in parties if p in frames
        }
        per_year_cover[int(y)] = {
            p: _covered_categories(frames[p], cat_uo_w, category_ids)
            for p in parties if p in frames
        }

    active = set(category_ids)
    shares: dict[tuple[str, str], float] = {}
    for p in parties:
        for y in giltiga[p]:
            active &= per_year_cover[y].get(p, set())
        vals = [per_year_shares[y][p] for y in giltiga[p]]
        for cat in category_ids:
            if vals:
                shares[(p, cat)] = sum(v.get(cat, 0.0) for v in vals) / len(vals)
    return shares, active, giltiga


def parties_matching_adopted(
    parties: list[str],
    decided_frames: Mapping[int, Mapping[str, Any]],
    ramar_cfg: Mapping[str, Any] | None = None,
    years_by_party: Mapping[str, list[int]] | None = None,
) -> list[str]:
    """Partier vars ram sammanfaller med den ANTAGNA ramen i VARJE av partiets giltiga år.

    Underlaget till villkorsklausulen i ADR 0007 punkt 4. Ett parti vars ram är den antagna i
    varje år har ingen egen nollpunkt: kvoten mot förankringen blir densamma som förankringens
    egen kvot mot sig själv, och partiet landar mitt på skalan i varje kategori av konstruktion.
    Klausulen är ADR 0005:s förkastade alternativ "Regeringens ram som nollpunkt", skrivet som
    ett prov, så att ett kort fönster inte kan återinföra det bakvägen.

    `years_by_party` är partiets giltiga årsmängd (ADR 0017 punkt 8). Frågan går bara att
    ställa på de år partiet faktiskt mäts på: ett år som inte matar a1 kan varken ge eller ta
    ifrån partiet en egen nollpunkt. Utelämnas den prövas alla år i configen.

    Ett parti utan PRÖVADE år matchar aldrig. Tomt underlag är ingen träff: en vakuös träff
    skulle fälla a1 globalt utan att ett enda år jämförts, och klausulen finns för att fånga
    ett parti som SAKNAR egen nollpunkt, aldrig ett som saknar underlag.
    """
    cfg = config.budget_ramar() if ramar_cfg is None else ramar_cfg
    years = (cfg or {}).get("budget_years") or {}
    if not years:
        return []
    out: list[str] = []
    for party in parties:
        provade = (None if years_by_party is None
                   else {int(y) for y in years_by_party.get(party, [])})
        if provade is not None and not provade:
            continue
        matches, antal_provade = True, 0
        for year, block in years.items():
            if provade is not None and int(year) not in provade:
                continue
            antal_provade += 1
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
        if matches and antal_provade:
            out.append(party)
    return out


def a1_admissible(
    parties: list[str],
    decided_frames: Mapping[int, Mapping[str, Any]],
    ramar_cfg: Mapping[str, Any] | None = None,
    years_by_party: Mapping[str, list[int]] | None = None,
) -> tuple[bool, list[str]]:
    """Villkorsklausulen (ADR 0007 punkt 4): (får a1 räknas, partierna som fällde den).

    a1 är otillåten om NÅGOT partis ram sammanfaller med den antagna ramen i varje av partiets
    giltiga år. Rättsverkan är global (ADR 0017 punkt 8): faller klausulen ut faller a1 ur A
    för alla kategorier och alla partier, och A blir a2 ensam.
    """
    offenders = parties_matching_adopted(parties, decided_frames, ramar_cfg, years_by_party)
    return not offenders, offenders


def validate(cfg: Mapping[str, Any] | None = None, parties: list[str] | None = None) -> None:
    """Strukturinvarianter för budget_ramar.yaml (höjer ValueError). Tom config är giltig.

    Per budgetår: varje party_frame-parti (måste vara exakt de 8) pekar på en namngiven ram;
    varje ram har source_ref; alla UO-belopp numeriska; varje frame täcker samma UO-mängd.

    Per party_frame-rad dessutom (ADR 0017 godkännandetest 2 och 4): `basis` ligger i den
    slutna mängden config.VALID_FRAME_BASES, `note` finns, och NOTEN stämmer med grunden. En
    voteringsgrund citerar en votering, och de två författarskapsgrunderna gör det inte.
    Provet går på källraden och aldrig på `role`: fälten delar i dag exakt samma parti-år, så
    det är det enda som visar att klassregeln vilar på vad källan belägger (ADR 0017 diagnos 4).
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
            basis = spec.get("basis")
            if basis not in config.VALID_FRAME_BASES:
                raise ValueError(
                    f"budget_ramar {y}: party_frame[{party}] har basis={basis!r} "
                    f"(tillåtna: {', '.join(sorted(config.VALID_FRAME_BASES))})"
                )
            note = str(spec.get("note", "")).strip()
            if not note:
                raise ValueError(
                    f"budget_ramar {y}: party_frame[{party}] saknar note, alltså källraden "
                    f"som belägger grunden {basis!r}"
                )
            citerar = note_cites_votering(note)
            if basis == "votering" and not citerar:
                raise ValueError(
                    f"budget_ramar {y}: party_frame[{party}] har basis votering men noten "
                    f"citerar ingen votering: {note!r}"
                )
            if basis != "votering" and citerar:
                raise ValueError(
                    f"budget_ramar {y}: party_frame[{party}] har basis {basis!r} men noten "
                    f"citerar en votering: {note!r}"
                )
