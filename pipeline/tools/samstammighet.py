"""Verktyg för POC:en Samstämmighet (biljett #47).

Modulen körs FÖR HAND och aldrig av pipelinen. Måttet väger 0, ingår inte i någon poäng och rör
varken `dist/`, `config/categories.yaml` eller gränssnittet. Därför ligger den i `pipeline/tools/`
och importeras inte av `pipeline/build_all.py`.

POC:en bygger inte måttet. Den avgör om måttet är värt att grilla, och svarar på tre frågor:
skiljer måttet partierna, mäter det dokumentlängd, och är det neutralt mellan regering och
opposition. Trösklarna är låsta i `docs/samstammighet_poc/forhandsregistrering.md` och ändras
aldrig efteråt.

    python -m pipeline.tools.samstammighet --resultat   # steg 2 till 4: räkna och skriv
    python -m pipeline.tools.samstammighet --korpus     # räkna korpusen, skriv inget

Räkningarna, alla prövade i `tests/test_samstammighet_poc.py`:

  retorikandelar        kategorins andel av partiets manifestposter (förhandsreg. 2)
  handlingsandelar      kategorins andel av partiets kraft, normerad inom partiet (3)
  glapp                 retorik minus handling, per cell (4)
  profilavstand         totalvariationsavståndet mellan de två profilerna (5.1)
  skiljbarhet           tröskel 1 (6.1)
  langdkonfund          tröskel 2, Pearson och Spearman (6.2)
  blockskillnad         tröskel 3, mellan delat med inom (6.3)
  bootstrap             tröskel 4, spridningen på retoriksidan (7.2)

Ett glapp är ett glapp. Ingen funktion här läser det som ohederlighet, och inget tal här inne är
ett betyg.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from pipeline import budget, config

ROT = Path(__file__).resolve().parents[2]
KORPUSKATALOG = ROT / "config" / "verklighetsbild"
UTKATALOG = ROT / "config" / "samstammighet_poc"
POCKATALOG = ROT / "docs" / "samstammighet_poc"

# --- de låsta talen (förhandsregistreringen 6 och 7.2). Ändras ett av dem faller POC:en. -----
FRO = 20260914
OMDRAGNINGAR = 10_000
PERCENTILER = (2.5, 97.5)
TROSKEL_SKILDA = 5
TROSKEL_SPANN = 0.10
TROSKEL_KORRELATION = 0.7
DECIMALER = 3

# Korpusarnas åttonde etikett. Posterna räknas bort ur både täljare och nämnare (2.3).
UTANFOR = "Utanför de sju kategorierna"

# Korpusarna bär kategorins NAMN, configen dess id. Ett namn skiljer sig (2.4).
NAMNAVVIKELSER = {"Integration och sammanhållning": "integration"}

# Alla tal i utdata rundas hit. Nio decimaler ligger långt under varje tröskel och gör ändå
# filen jämförbar tecken för tecken mellan två körningar.
UTDECIMALER = 9


@dataclass(frozen=True)
class Post:
    """En manifestpost: partiets egen utsaga med sin kategorietikett."""

    id: str
    parti: str
    kategorinamn: str


def _rund(x: float) -> float:
    return round(float(x), UTDECIMALER)


# --------------------------------------------------------------------------- inläsning


def kategorinamn_till_id(kategorier_cfg: dict[str, Any] | None = None) -> dict[str, str]:
    """Kategorinamn -> id, byggd ur configen plus den uttryckliga avvikelsetabellen (2.4)."""
    cfg = config.categories() if kategorier_cfg is None else kategorier_cfg
    ut = {c["name"]: c["id"] for c in cfg["categories"]}
    ut.update(NAMNAVVIKELSER)
    return ut


def las_korpus(fil: Path) -> list[Post]:
    """Läser en korpusfil till poster. Filen ändras aldrig, bara läses."""
    data = yaml.safe_load(fil.read_text(encoding="utf-8"))
    poster = [
        Post(id=str(p["id"]), parti=str(p["dokument"]), kategorinamn=str(p["kategori"]))
        for p in data["pastaenden"]
    ]
    if len(poster) != int(data["antal"]):
        raise ValueError(f"{fil.name}: antal säger {data['antal']} men filen bär {len(poster)}")
    return poster


def las_a(sokvag: Path | None = None) -> dict[tuple[str, str], float]:
    """(parti, kategori) -> delpoäng A ur dist/scores.json. Filen läses, aldrig skrivs."""
    sokvag = (ROT / "dist" / "scores.json") if sokvag is None else sokvag
    data = json.loads(sokvag.read_text(encoding="utf-8"))
    return {
        (parti, kategori): float(cell["components"]["A"])
        for parti, rad in data["scores"].items()
        for kategori, cell in rad.items()
    }


def las_a1() -> dict[tuple[str, str], float]:
    """(parti, kategori) -> a1 rå, alltså kategorins andel av partiets egna utgiftsramar (3.3).

    Andelen är medel över budgetåren. Nämnaren är hela ramen, alltså även de utgiftsområden som
    inte hör till någon kategori, så talet renormeras i handlingsandelar.
    """
    andelar, _aktiva, ar = budget.a1_shares(config.category_ids(), config.party_codes())
    if not ar:
        raise ValueError("a1 saknar budgetår; config/budget_ramar.yaml är tom")
    return dict(andelar)


def las_blocken() -> tuple[list[str], list[str]]:
    """(regeringssidan, oppositionen) ur den SITTANDE regeringen i config/mappings.yaml (6.3).

    Regeringssidan är `parties` plus `support_parties`. Den sittande perioden är den vars `end`
    är tom. Finns ingen sådan period faller räkningen hårt: blocken får aldrig gissas.
    """
    perioder = config.mappings()["government_periods"]
    sittande = [p for p in perioder if p.get("end") in (None, "")]
    if len(sittande) != 1:
        raise ValueError(f"mappings: {len(sittande)} sittande regeringsperioder, väntade 1")
    regering = list(sittande[0].get("parties") or []) + list(sittande[0].get("support_parties") or [])
    partier = config.party_codes()
    okanda = sorted(set(regering) - set(partier))
    if okanda:
        raise ValueError(f"mappings: okänt parti i regeringsperioden: {', '.join(okanda)}")
    return sorted(regering), sorted(set(partier) - set(regering))


# --------------------------------------------------------------------------- retoriksidan


def retorikandelar(
    poster: list[Post],
    partier: list[str],
    kategorier: list[str],
    namn_till_id: dict[str, str],
) -> tuple[dict[tuple[str, str], float], dict[str, dict[str, int]]]:
    """((parti, kategori) -> andel, parti -> antal poster).

    Nämnaren är partiets poster i de sju kategorierna (2.3). Posterna utanför dem räknas bort ur
    både täljare och nämnare, och antalet redovisas. Ett okänt kategorinamn faller hårt (2.4):
    ett tyst bortfall skulle krympa nämnaren utan att synas.
    """
    rakning = {p: Counter() for p in partier}
    utanfor = {p: 0 for p in partier}
    for post in poster:
        if post.parti not in rakning:
            raise ValueError(f"{post.id}: okänt parti {post.parti!r}")
        if post.kategorinamn == UTANFOR:
            utanfor[post.parti] += 1
            continue
        kid = namn_till_id.get(post.kategorinamn)
        if kid is None:
            raise ValueError(f"{post.id}: okänd kategori {post.kategorinamn!r}")
        if kid not in kategorier:
            raise ValueError(f"{post.id}: kategori {kid!r} står utanför modellens sju")
        rakning[post.parti][kid] += 1

    andelar: dict[tuple[str, str], float] = {}
    antal: dict[str, dict[str, int]] = {}
    for p in partier:
        i_kategori = sum(rakning[p].values())
        if i_kategori == 0:
            raise ValueError(f"{p}: ingen post i de sju kategorierna, ingen profil går att räkna")
        for c in kategorier:
            andelar[(p, c)] = rakning[p][c] / i_kategori
        antal[p] = {
            "i_kategori": i_kategori,
            "utanfor": utanfor[p],
            "totalt": i_kategori + utanfor[p],
        }
    return andelar, antal


# --------------------------------------------------------------------------- handlingssidan


def handlingsandelar(
    celler: dict[tuple[str, str], float],
    partier: list[str],
    kategorier: list[str],
) -> dict[tuple[str, str], float]:
    """((parti, kategori) -> andel av partiets kraft), normerad inom partiet (3.1).

    Saknad eller negativ cell faller hårt. En tyst nolla skulle se ut som en kategori partiet
    inte lägger någon kraft på, vilket är ett helt annat besked än att talet saknas.
    """
    ut: dict[tuple[str, str], float] = {}
    for p in partier:
        rad = {}
        for c in kategorier:
            if (p, c) not in celler:
                raise ValueError(f"{p}/{c}: cellen saknas på handlingssidan")
            v = float(celler[(p, c)])
            if v < 0:
                raise ValueError(f"{p}/{c}: {v} är negativt, kraft kan inte vara mindre än noll")
            rad[c] = v
        summa = sum(rad.values())
        if summa <= 0:
            raise ValueError(f"{p}: summan över de sju kategorierna är {summa}, ingen profil finns")
        for c in kategorier:
            ut[(p, c)] = rad[c] / summa
    return ut


# --------------------------------------------------------------------------- glappet


def glapp(
    retorik: dict[tuple[str, str], float],
    handling: dict[tuple[str, str], float],
    partier: list[str],
    kategorier: list[str],
) -> dict[tuple[str, str], float]:
    """(parti, kategori) -> retorik minus handling (4). Ett glapp är ett glapp."""
    return {(p, c): retorik[(p, c)] - handling[(p, c)] for p in partier for c in kategorier}


def profilavstand(g: dict[tuple[str, str], float], parti: str, kategorier: list[str]) -> float:
    """Totalvariationsavståndet mellan partiets två profiler (5.1).

    Talet läser som den andel av partiets betoning som skulle behöva flytta för att profilerna
    skulle sammanfalla. Det är ett avstånd och aldrig ett betyg (5.2).
    """
    return 0.5 * sum(abs(g[(parti, c)]) for c in kategorier)


def storsta_positiva_glapp(
    g: dict[tuple[str, str], float], parti: str, kategorier: list[str]
) -> tuple[str, float]:
    """(kategorin partiet säljer in mest relativt handlingen, glappet) (5.3)."""
    kategori = max(kategorier, key=lambda c: (g[(parti, c)], c))
    return kategori, g[(parti, kategori)]


# --------------------------------------------------------------------------- trösklarna


def skiljbarhet(
    varden: dict[str, float],
    decimaler: int = DECIMALER,
    min_skilda: int = TROSKEL_SKILDA,
    min_spann: float = TROSKEL_SPANN,
) -> dict[str, Any]:
    """Tröskel 1 (6.1): minst fem skilda värden och ett spann på minst 0,10."""
    tal = list(varden.values())
    skilda = len({round(v, decimaler) for v in tal})
    spann = max(tal) - min(tal)
    brister = []
    if skilda < min_skilda:
        brister.append(f"{skilda} skilda värden, kräver {min_skilda}")
    if spann < min_spann:
        brister.append(f"spann {spann:.3f}, kräver {min_spann}")
    return {
        "skilda": skilda,
        "spann": _rund(spann),
        "hogsta": _rund(max(tal)),
        "lagsta": _rund(min(tal)),
        "klarar": not brister,
        "skal": "; ".join(brister),
    }


def pearson(xs: list[float], ys: list[float]) -> float:
    """Pearsons r. Konstant serie faller hårt: en korrelation mot en konstant finns inte."""
    n = len(xs)
    if n != len(ys) or n < 3:
        raise ValueError(f"pearson: {n} mot {len(ys)} observationer")
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys, strict=True))
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    if sxx <= 0 or syy <= 0:
        raise ValueError("pearson: en av serierna är konstant")
    return sxy / (sxx * syy) ** 0.5


def _rangordna(vs: list[float]) -> list[float]:
    """Medelrang vid lika värden, alltså standardrangordning för Spearman."""
    ordnade = sorted(range(len(vs)), key=lambda i: vs[i])
    rang = [0.0] * len(vs)
    i = 0
    while i < len(ordnade):
        j = i
        while j + 1 < len(ordnade) and vs[ordnade[j + 1]] == vs[ordnade[i]]:
            j += 1
        medel = (i + j) / 2 + 1
        for k in range(i, j + 1):
            rang[ordnade[k]] = medel
        i = j + 1
    return rang


def spearman(xs: list[float], ys: list[float]) -> float:
    """Spearmans rangkorrelation, alltså Pearson på rangerna."""
    return pearson(_rangordna(list(xs)), _rangordna(list(ys)))


def langdkonfund(
    varden: dict[str, float],
    langder: dict[str, float],
    grans: float = TROSKEL_KORRELATION,
) -> dict[str, Any]:
    """Tröskel 2 (6.2): mäter måttet dokumentlängd? Pearson avgör, Spearman redovisas."""
    partier = sorted(varden)
    xs = [float(varden[p]) for p in partier]
    ys = [float(langder[p]) for p in partier]
    r = pearson(xs, ys)
    return {
        "pearson": _rund(r),
        "spearman": _rund(spearman(xs, ys)),
        "n": len(partier),
        "grans": grans,
        "klarar": abs(r) < grans,
        "skal": "" if abs(r) < grans else f"|r| = {abs(r):.3f}, kräver under {grans}",
    }


def _medel(vs: list[float]) -> float:
    return sum(vs) / len(vs)


def _stickprovsvarians(vs: list[float]) -> float:
    if len(vs) < 2:
        raise ValueError("varians: minst två observationer krävs")
    m = _medel(vs)
    return sum((v - m) ** 2 for v in vs) / (len(vs) - 1)


def blockskillnad(
    varden: dict[str, float],
    regeringssidan: list[str],
    oppositionen: list[str],
) -> dict[str, Any]:
    """Tröskel 3 (6.3): skillnaden mellan blocken mot spridningen inom dem.

    `mellan` är skillnaden mellan blockens medelvärden och `inom` den poolade
    standardavvikelsen. Kvoten är Cohens d vid lika stora grupper, och regeln säger |d| <= 1.
    """
    reg = [float(varden[p]) for p in regeringssidan]
    opp = [float(varden[p]) for p in oppositionen]
    mellan = abs(_medel(reg) - _medel(opp))
    inom = ((_stickprovsvarians(reg) + _stickprovsvarians(opp)) / 2) ** 0.5
    if inom <= 0:
        raise ValueError("blockskillnad: spridningen inom blocken är noll")
    return {
        "regeringssidan": list(regeringssidan),
        "oppositionen": list(oppositionen),
        "medel_regeringssidan": _rund(_medel(reg)),
        "medel_oppositionen": _rund(_medel(opp)),
        "mellan": _rund(mellan),
        "inom": _rund(inom),
        "d": _rund(mellan / inom),
        "klarar": mellan <= inom,
        "skal": "" if mellan <= inom else f"mellan {mellan:.3f} över inom {inom:.3f}",
    }


# --------------------------------------------------------------------------- spridningen


def _percentil(ordnade: list[float], q: float) -> float:
    """Linjärt interpolerad percentil ur en redan sorterad lista."""
    if not ordnade:
        raise ValueError("percentil: tom lista")
    pos = (len(ordnade) - 1) * (q / 100.0)
    lag = int(pos)
    hog = min(lag + 1, len(ordnade) - 1)
    return ordnade[lag] + (ordnade[hog] - ordnade[lag]) * (pos - lag)


def bootstrap(
    poster: list[Post],
    handling: dict[tuple[str, str], float],
    partier: list[str],
    kategorier: list[str],
    namn_till_id: dict[str, str],
    fro: int = FRO,
    omdragningar: int = OMDRAGNINGAR,
    percentiler: tuple[float, float] = PERCENTILER,
) -> dict[str, list[float]]:
    """parti -> [undre, övre] för profilavståndet (7.2).

    Partiets poster dras om med återläggning, lika många som partiet bär. Handlingssidan hålls
    fast: den är räknad över hela förankringsfönstret och bär ingen urvalsosäkerhet.

    Fröet är eget per parti, härlett som `fro + partiets index`, så ett parti aldrig ärver en
    annans dragning.
    """
    etiketter: dict[str, list[str]] = {p: [] for p in partier}
    for post in poster:
        if post.kategorinamn == UTANFOR:
            continue
        kid = namn_till_id.get(post.kategorinamn)
        if kid is None:
            raise ValueError(f"{post.id}: okänd kategori {post.kategorinamn!r}")
        etiketter[post.parti].append(kid)

    ut: dict[str, list[float]] = {}
    for index, p in enumerate(partier):
        egna = etiketter[p]
        if not egna:
            raise ValueError(f"{p}: ingen post att dra om")
        rng = random.Random(fro + index)
        n = len(egna)
        avstand = []
        for _ in range(omdragningar):
            rakning = Counter(rng.choices(egna, k=n))
            avstand.append(
                0.5 * sum(abs(rakning[c] / n - handling[(p, c)]) for c in kategorier)
            )
        avstand.sort()
        ut[p] = [_rund(_percentil(avstand, percentiler[0])), _rund(_percentil(avstand, percentiler[1]))]
    return ut


# --------------------------------------------------------------------------- diagnostiken


def koncentration(
    profil: dict[tuple[str, str], float], partier: list[str], kategorier: list[str]
) -> dict[str, float]:
    """parti -> profilens avstånd till en jämn fördelning över kategorierna.

    Samma avstånd som i 5.1, mätt mot den jämna profilen i stället för mot den andra sidan.
    Talet säger hur spetsig profilen är, och ingenting om vad partiet betonar.
    """
    lik = 1.0 / len(kategorier)
    return {p: 0.5 * sum(abs(profil[(p, c)] - lik) for c in kategorier) for p in partier}


def _r_eller_none(xs: list[float], ys: list[float]) -> float | None:
    """Pearson, eller None när en av serierna är konstant. En konstant serie är ett svar."""
    try:
        return _rund(pearson(xs, ys))
    except ValueError:
        return None


def diagnostik(
    retorik: dict[tuple[str, str], float],
    handling: dict[tuple[str, str], float],
    handling_a1: dict[tuple[str, str], float],
    partier: list[str],
    kategorier: list[str],
) -> dict[str, Any]:
    """EFTERHANDSPROV: vilken av de två sidorna bär variationen mellan partierna?

    Provet är INTE förhandsregistrerat och avgör ingenting. Det lades till efter den första
    körningen, när talen visade att handlingssidans profil låg nära den jämna. Frågan det
    svarar på är om avståndet i 5.1 mäter ett glapp mellan två sidor, eller bara hur spetsig
    den ena sidan är.

    Ligger `r_avstand_mot_retorikens_koncentration` nära 1 mäter avståndet i praktiken
    retorikens koncentration, och handlingssidan bidrar inte.
    """
    tv = {p: profilavstand(glapp(retorik, handling, partier, kategorier), p, kategorier) for p in partier}
    tv_a1 = {
        p: profilavstand(glapp(retorik, handling_a1, partier, kategorier), p, kategorier)
        for p in partier
    }
    ret_k = koncentration(retorik, partier, kategorier)
    han_k = koncentration(handling, partier, kategorier)
    xs = [tv[p] for p in partier]
    spridning = {
        "retorik": {p: _rund(max(retorik[(p, c)] for c in kategorier)
                             - min(retorik[(p, c)] for c in kategorier)) for p in partier},
        "handling": {p: _rund(max(handling[(p, c)] for c in kategorier)
                              - min(handling[(p, c)] for c in kategorier)) for p in partier},
    }
    return {
        "efterhandsprov": True,
        "retorikens_koncentration": {p: _rund(v) for p, v in ret_k.items()},
        "handlingens_koncentration": {p: _rund(v) for p, v in han_k.items()},
        "r_avstand_mot_retorikens_koncentration": _r_eller_none(xs, [ret_k[p] for p in partier]),
        "r_avstand_mot_handlingens_koncentration": _r_eller_none(xs, [han_k[p] for p in partier]),
        "r_primar_mot_a1": _r_eller_none(xs, [tv_a1[p] for p in partier]),
        "spridning_i_profilen": spridning,
    }


# --------------------------------------------------------------------------- hela räkningen


def _profil(g: dict[tuple[str, str], float], partier: list[str], kategorier: list[str]) -> dict[str, float]:
    return {p: _rund(profilavstand(g, p, kategorier)) for p in partier}


def _tabell(
    celler: dict[tuple[str, str], float], partier: list[str], kategorier: list[str]
) -> dict[str, dict[str, float]]:
    return {p: {c: _rund(celler[(p, c)]) for c in kategorier} for p in partier}


def _provning(
    varden: dict[str, float],
    langder: dict[str, float],
    regeringssidan: list[str],
    oppositionen: list[str],
) -> dict[str, Any]:
    """De tre trösklarna på en och samma uppsättning per-parti-värden."""
    ut = {
        "skiljbarhet": skiljbarhet(varden),
        "langd": langdkonfund(varden, langder),
        "neutralitet": blockskillnad(varden, regeringssidan, oppositionen),
    }
    fallna = [namn for namn, rad in ut.items() if not rad["klarar"]]
    ut["klarar"] = not fallna
    ut["fallna"] = fallna
    return ut


def rakna_resultat(
    bakat: list[Post],
    framat: list[Post],
    a_celler: dict[tuple[str, str], float],
    a1_celler: dict[tuple[str, str], float],
    partier: list[str],
    kategorier: list[str],
    namn_till_id: dict[str, str],
    regeringssidan: list[str],
    oppositionen: list[str],
    fro: int = FRO,
    omdragningar: int = OMDRAGNINGAR,
) -> dict[str, Any]:
    """Hela räkningen: två profiler, glappet, de tre trösklarna och spridningen.

    Den primära uppställningen är unionen av korpusarna mot normerad A. Varianterna räknas på
    samma sätt och redovisas alltid, men de avgör ingenting (förhandsregistreringen 2.1 och 3.3).
    """
    union = list(bakat) + list(framat)
    r_union, antal_union = retorikandelar(union, partier, kategorier, namn_till_id)
    r_bakat, antal_bakat = retorikandelar(bakat, partier, kategorier, namn_till_id)
    r_framat, antal_framat = (
        retorikandelar(framat, partier, kategorier, namn_till_id) if framat else ({}, {})
    )

    h_a = handlingsandelar(a_celler, partier, kategorier)
    h_a1 = handlingsandelar(a1_celler, partier, kategorier)

    g_primar = glapp(r_union, h_a, partier, kategorier)
    g_a1 = glapp(r_union, h_a1, partier, kategorier)
    g_bakat = glapp(r_bakat, h_a, partier, kategorier)
    g_framat = glapp(r_framat, h_a, partier, kategorier) if framat else {}

    langder = {p: float(antal_union[p]["i_kategori"]) for p in partier}
    tv_primar = _profil(g_primar, partier, kategorier)
    storsta = {
        p: dict(zip(("kategori", "glapp"), storsta_positiva_glapp(g_primar, p, kategorier), strict=True))
        for p in partier
    }
    for rad in storsta.values():
        rad["glapp"] = _rund(rad["glapp"])

    varianter: dict[str, Any] = {
        "a1_ra": _provning(_profil(g_a1, partier, kategorier), langder, regeringssidan, oppositionen),
        "bakat": _provning(_profil(g_bakat, partier, kategorier), langder, regeringssidan, oppositionen),
        "storsta_glapp": _provning(
            {p: storsta[p]["glapp"] for p in partier}, langder, regeringssidan, oppositionen
        ),
        "sd_utanfor": _provning(
            tv_primar,
            langder,
            [p for p in regeringssidan if p != "SD"],
            [p for p in oppositionen if p != "SD"],
        ),
    }
    if framat:
        varianter["framat"] = _provning(
            _profil(g_framat, partier, kategorier), langder, regeringssidan, oppositionen
        )

    # Skiljbarheten per kategori (6.1). Redovisas alltid, avgör aldrig.
    per_kategori = {
        c: skiljbarhet({p: g_primar[(p, c)] for p in partier}) for c in kategorier
    }

    primar = _provning(tv_primar, langder, regeringssidan, oppositionen)
    ut: dict[str, Any] = {
        "partier": list(partier),
        "kategorier": list(kategorier),
        "fro": fro,
        "omdragningar": omdragningar,
        "poster": {
            "union": antal_union,
            "bakat": antal_bakat,
            "framat": antal_framat,
        },
        "retorik": {
            "union": _tabell(r_union, partier, kategorier),
            "bakat": _tabell(r_bakat, partier, kategorier),
            "framat": _tabell(r_framat, partier, kategorier) if framat else {},
        },
        "handling": {
            "a_normerad": _tabell(h_a, partier, kategorier),
            "a1_ra": _tabell(h_a1, partier, kategorier),
        },
        "glapp": {
            "primar": _tabell(g_primar, partier, kategorier),
            "a1_ra": _tabell(g_a1, partier, kategorier),
        },
        "profilavstand": {
            "primar": tv_primar,
            "intervall": bootstrap(
                union, h_a, partier, kategorier, namn_till_id,
                fro=fro, omdragningar=omdragningar,
            ),
        },
        "storsta_positiva_glapp": storsta,
        "skiljbarhet_per_kategori": per_kategori,
        "trosklar": {"primar": primar, "varianter": varianter},
        "diagnostik": diagnostik(r_union, h_a, h_a1, partier, kategorier),
    }
    ut["utfall"] = {
        "klarar": primar["klarar"],
        "fallna_trosklar": primar["fallna"],
    }
    return ut


KALLOR = {
    "korpus_bakat": "config/verklighetsbild/korpus_bakat.yaml",
    "korpus_framat": "config/verklighetsbild/korpus_framat.yaml",
    "delpoang_a": "dist/scores.json",
    "a1_ra": "config/budget_ramar.yaml",
    "blocken": "config/mappings.yaml",
    "forhandsregistrering": "docs/samstammighet_poc/forhandsregistrering.md",
}


def kallhashar(a_sokvag: Path | None = None) -> dict[str, str]:
    """namn -> SHA-256 av källfilen, som den ligger just nu.

    Talen i POC:en är PINNADE till sitt underlag. Delpoäng A är en byggd artefakt som rör sig
    varje gång pipen körs om, så utan en hash kan resultatfilen bära tal ingen längre kan
    återskapa. Rör sig en källa faller `tests/test_samstammighet_poc.py` och säger att POC:en
    ska köras om. En tyst gammal siffra är ett värre fel än ett rött test.

    Radsluten normaliseras före hashningen. Alla fem källorna är textfiler, och en utcheckning
    på Windows ger dem CRLF där git bär LF. Utan normaliseringen skulle hashen säga att
    underlaget ändrats så fort någon checkat ut repot på ett annat operativsystem.
    """
    ut = {}
    for namn, rel in KALLOR.items():
        fil = a_sokvag if (namn == "delpoang_a" and a_sokvag is not None) else ROT / rel
        text = fil.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
        ut[namn] = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return ut


def kor(
    omdragningar: int = OMDRAGNINGAR,
    fro: int = FRO,
    a_sokvag: Path | None = None,
) -> dict[str, Any]:
    """Räkningen på repots eget underlag. Läser fem filer och skriver ingen."""
    namn_till_id = kategorinamn_till_id()
    regeringssidan, oppositionen = las_blocken()
    ut = rakna_resultat(
        bakat=las_korpus(KORPUSKATALOG / "korpus_bakat.yaml"),
        framat=las_korpus(KORPUSKATALOG / "korpus_framat.yaml"),
        a_celler=las_a(a_sokvag),
        a1_celler=las_a1(),
        partier=config.party_codes(),
        kategorier=config.category_ids(),
        namn_till_id=namn_till_id,
        regeringssidan=regeringssidan,
        oppositionen=oppositionen,
        fro=fro,
        omdragningar=omdragningar,
    )
    ut["kallor"] = dict(KALLOR)
    ut["kallhashar"] = kallhashar(a_sokvag)
    return ut


def skriv_resultat(resultat: dict[str, Any]) -> Path:
    """Skriver den maskinläsbara räkningen. Enda utkatalogen är config/samstammighet_poc/."""
    UTKATALOG.mkdir(parents=True, exist_ok=True)
    fil = UTKATALOG / "resultat.yaml"
    fil.write_text(
        "# Rösta - POC:en Samstämmighets räkning (biljett #47 steg 2 till 4).\n"
        "#\n"
        "# AUTOGENERERAD av pipeline/tools/samstammighet.py, redigera aldrig för hand:\n"
        "#\n"
        "#     python -m pipeline.tools.samstammighet --resultat\n"
        "#\n"
        "# Trösklarna är låsta i docs/samstammighet_poc/forhandsregistrering.md, skriven innan\n"
        "# något räknades. Inget tal här inne är ett betyg: POC:en mäter skiljbarhet och inte\n"
        "# samstämmighet. Ett glapp är ett glapp, och ingen rad läser det som ohederlighet.\n"
        "#\n"
        "# Måttet väger 0. Det ingår inte i någon poäng, och dist/ är orört.\n\n"
        + yaml.safe_dump(resultat, allow_unicode=True, sort_keys=False, default_flow_style=False),
        encoding="utf-8",
    )
    return fil


def _main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("--resultat", action="store_true", help="räkna glappet och pröva trösklarna")
    p.add_argument("--korpus", action="store_true", help="räkna korpusen, skriv ingen fil")
    p.add_argument("--kallhashar", action="store_true", help="skriv ut källornas SHA-256")
    args = p.parse_args(argv)
    if args.korpus:
        bakat = las_korpus(KORPUSKATALOG / "korpus_bakat.yaml")
        framat = las_korpus(KORPUSKATALOG / "korpus_framat.yaml")
        print(json.dumps({"bakat": len(bakat), "framat": len(framat)}, ensure_ascii=False))
    if args.kallhashar:
        print(json.dumps(kallhashar(), ensure_ascii=False, indent=1))
    if args.resultat:
        resultat = kor()
        print(f"skrev {skriv_resultat(resultat)}")
        print(json.dumps(resultat["utfall"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
