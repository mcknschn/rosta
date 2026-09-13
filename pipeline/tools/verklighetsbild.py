"""Verktyg för Verklighetsbildpiloten (ADR 0016, biljett #46).

Modulen körs FÖR HAND och aldrig av pipelinen. Verklighetsbild har vikt 0, ingår inte i
någon poäng och rör varken `dist/`, `config/categories.yaml` eller gränssnittet
(ADR 0016, sista följdpunkten). Därför ligger den i `pipeline/tools/` och importeras
inte av `pipeline/build_all.py`.

    python -m pipeline.tools.verklighetsbild --manifest   # hämtmanifest med SHA-256
    python -m pipeline.tools.verklighetsbild --korpus     # bakåt- och framåtkorpus -> config
    python -m pipeline.tools.verklighetsbild --urval      # dra pilotens 200 + delurvalets 40
    python -m pipeline.tools.verklighetsbild --uppdrag    # kodningsunderlag per kodare
    python -m pipeline.tools.verklighetsbild --resultat   # utbyte, alfa och tröskelprövning

Modulen innehåller fyra räkningar, alla prövade i `tests/test_verklighetsbild.py`:

  las_bakat / las_framat   läser de tre markdownfilerna i docs/valmanifest_2026/ och ger
                           utsagor med stabila id. Mappade poster behåller sitt eget id.
                           Kandidater får ett härlett id av formen `<PARTI>k-<nnn>`, satt
                           av ordningen i filen.
  dra_urval                stratifierad dragning utan återläggning, 25 per parti, med frö.
  krippendorff_alfa        alfa för nominal och ordinal skala, med förväxlingsmatris.
  skatta_utbyte            designviktat medelvärde med ändlighetskorrektion per stratum.

Ingen av dem avgör om ett påstående är sant. Piloten mäter utbyte och reliabilitet
(se `docs/verklighetsbild_pilot/kodbok_pilot.md` avsnitt 1).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

ROT = Path(__file__).resolve().parents[2]
KALLKATALOG = ROT / "docs" / "valmanifest_2026"
UTKATALOG = ROT / "config" / "verklighetsbild"
PILOTKATALOG = ROT / "docs" / "verklighetsbild_pilot"

# Partikoderna i `config/categories.yaml`-ordning. Ordningen är en del av dragningens
# metod: byts den, byts urvalet.
PARTIER = ("S", "M", "SD", "C", "V", "KD", "MP", "L")

# Partiernas källdokument, ur tabellen `Källfiler` i båda mappningsfilerna.
KALLDOKUMENT = {
    "S": "S-Valprogram-2026.pdf",
    "M": "M-Valmanifest-2026.pdf",
    "SD": "sd-valmanifest-2026.pdf",
    "C": "C-Valmanifest-2026.pdf",
    "V": "V-Valmanifest-2026.pdf",
    "KD": "kd-Valmanifest-2026.pdf",
    "MP": "mp-valmanifest-2026.pdf",
    "L": "L-valmanifest-2026.pdf",
}

# Bortfallskoderna i ADR 0016 beslutspunkt 2, i kodbokens företrädesordning (avsnitt 8.1).
BORTFALLSKODER = (
    "framtida_utfall",
    "normativ",
    "otillracklig_kontext",
    "ingen_kompatibel_indikator",
    "flera_operationaliseringar",
    "data_saknas",
    "period_saknas",
)

FRO_URVAL = 20260913
FRO_DELURVAL = 20260946
FRO_BLINDNING = 20264601
FRO_BLINDNING_DELURVAL = 20264602
PER_PARTI = 25
PER_PARTI_DELURVAL = 5
UTSAGOR_PER_BATCH = 25


@dataclass(frozen=True)
class Utsaga:
    """En rad i bakåt- eller framåtkorpusen, med partiets egen lydelse."""

    id: str
    parti: str
    kategori: str
    text: str
    kalla: str
    sida: int | None = None
    anmarkning: str | None = None


# --------------------------------------------------------------------------- korpus


def _brodtext(fil: Path, rubrik: str) -> list[str]:
    rader = fil.read_text(encoding="utf-8").split("\n")
    for i, rad in enumerate(rader):
        if rad.strip() == rubrik:
            return rader[i + 1 :]
    raise ValueError(f"{fil.name} saknar rubriken {rubrik!r}")


def _las_mappning(filnamn: str, rot: Path) -> list[Utsaga]:
    """Kategori som h3, parti som fetstil, poster med eget id i bakåtcitat."""
    fil = rot / filnamn
    utsagor: list[Utsaga] = []
    kategori = parti = ""
    for rad in _brodtext(fil, "## Posterna"):
        if rad.startswith("### "):
            kategori = re.sub(r"\s*\(\d+\)\s*$", "", rad[4:]).strip()
        elif (m := re.match(r"^\*\*([A-Za-z]+)\*\* \(\d+\)\s*$", rad)) is not None:
            parti = m.group(1)
        elif (m := re.match(r"^- `([A-Za-z0-9\-]+)` (.+)$", rad)) is not None:
            utsagor.append(
                Utsaga(id=m.group(1), parti=parti, kategori=kategori, text=m.group(2).strip(), kalla=filnamn)
            )
    return utsagor


def _las_kandidater(rot: Path) -> list[Utsaga]:
    """Parti som h3, kategori som fetstil, poster med sidmarkör och utan id."""
    filnamn = "kandidater_bakat.md"
    fil = rot / filnamn
    utsagor: list[Utsaga] = []
    kategori = parti = ""
    lopnummer: Counter[str] = Counter()
    for rad in _brodtext(fil, "## Kandidaterna"):
        if rad.startswith("### "):
            parti = re.sub(r"\s*\(\d+\)\s*$", "", rad[4:]).strip()
        elif (m := re.match(r"^\*\*(.+?)\*\* \(\d+\)\s*$", rad)) is not None:
            kategori = m.group(1).strip()
        elif (m := re.match(r"^- s(\d+) (.+)$", rad)) is not None:
            text = m.group(2).strip()
            anmarkning = None
            if (märkt := re.search(r"\s+`(avviker|sidbrott)`\s*$", text)) is not None:
                anmarkning = märkt.group(1)
                text = text[: märkt.start()].strip()
            lopnummer[parti] += 1
            utsagor.append(
                Utsaga(
                    id=f"{parti}k-{lopnummer[parti]:03d}",
                    parti=parti,
                    kategori=kategori,
                    text=text,
                    kalla=filnamn,
                    sida=int(m.group(1)),
                    anmarkning=anmarkning,
                )
            )
    return utsagor


def las_bakat(rot: Path = KALLKATALOG) -> list[Utsaga]:
    """De 896 bakåtblickande utsagorna: 230 mappade plus 666 kandidater."""
    return _las_mappning("mappning_bakat.md", rot) + _las_kandidater(rot)


def las_framat(rot: Path = KALLKATALOG) -> list[Utsaga]:
    """De 1 073 framåtblickande posterna."""
    return _las_mappning("mappning_framat.md", rot)


# --------------------------------------------------------------------------- urval


def dra_urval(utsagor: list[Utsaga], fro: int, per_parti: int) -> list[Utsaga]:
    """Stratifierad dragning utan återläggning, `per_parti` ur varje parti.

    Metoden är låst och står i `config/verklighetsbild/urval_pilot.yaml`: ett
    `random.Random(fro)` sås en gång, och partierna dras i PARTIER-ordning ur varje
    partis utsagor i korpusordning. Samma frö och samma korpus ger samma urval.
    """
    per_parti_lista: dict[str, list[Utsaga]] = {p: [] for p in PARTIER}
    for u in utsagor:
        if u.parti not in per_parti_lista:
            raise ValueError(f"okänd partikod {u.parti!r} på {u.id}")
        per_parti_lista[u.parti].append(u)

    for parti, lista in per_parti_lista.items():
        if len(lista) < per_parti:
            raise ValueError(f"{parti} bär {len(lista)} utsagor, färre än de {per_parti} som ska dras")

    rng = random.Random(fro)
    urval: list[Utsaga] = []
    for parti in PARTIER:
        urval.extend(rng.sample(per_parti_lista[parti], per_parti))
    return urval


# --------------------------------------------------------------- Krippendorffs alfa

Par = dict[str, list[str | None]]


def _sammantraffanden(par: Par) -> tuple[dict[tuple[str, str], float], Counter[str], float]:
    """Sammanträffandematrisen o_ck, marginalerna n_c och totalen n."""
    o: dict[tuple[str, str], float] = {}
    for varden in par.values():
        satta = [v for v in varden if v is not None]
        if len(satta) < 2:
            continue
        vikt = 1.0 / (len(satta) - 1)
        for i, c in enumerate(satta):
            for j, k in enumerate(satta):
                if i != j:
                    o[(c, k)] = o.get((c, k), 0.0) + vikt
    marginal: Counter[str] = Counter()
    for (c, _k), antal in o.items():
        marginal[c] += antal
    return o, marginal, sum(marginal.values())


def _delta_kvadrat(skala: str, ordning: list[str] | None, marginal: Counter[str]):
    if skala == "nominal":
        return lambda c, k: 0.0 if c == k else 1.0
    if skala != "ordinal":
        raise ValueError(f"okänd skala {skala!r}")
    if ordning is None:
        raise ValueError("ordinal skala kräver en ordning")
    index = {v: i for i, v in enumerate(ordning)}

    def delta(c: str, k: str) -> float:
        if c == k:
            return 0.0
        lo, hi = sorted((index[c], index[k]))
        summa = sum(marginal[ordning[g]] for g in range(lo, hi + 1))
        return (summa - (marginal[c] + marginal[k]) / 2) ** 2

    return delta


def krippendorff_alfa(par: Par, skala: str = "nominal", ordning: list[str] | None = None) -> float | None:
    """Krippendorffs alfa. Ger None när materialet saknar variation att mäta emot.

    `par` är en avbildning enhet -> kodarnas värden i fast kodarordning. `None` betyder
    att kodaren inte satte något värde på enheten. Enheter med färre än två satta värden
    bär ingen oenighet och hoppas över.
    """
    o, marginal, n = _sammantraffanden(par)
    if n < 2 or len(marginal) < 2:
        return None
    delta = _delta_kvadrat(skala, ordning, marginal)

    observerad = sum(antal * delta(c, k) for (c, k), antal in o.items())
    vardelista = list(marginal)
    forvantad = sum(
        marginal[c] * marginal[k] * delta(c, k) for c in vardelista for k in vardelista if c != k
    ) / (n - 1)
    if forvantad == 0:
        return None
    return 1.0 - observerad / forvantad


def forvaxlingsmatris(par: Par) -> dict[tuple[str, str], int]:
    """Antal enheter per värdepar, i kodarordningen (kodare 1, kodare 2)."""
    matris: Counter[tuple[str, str]] = Counter()
    for varden in par.values():
        if len(varden) != 2 or any(v is None for v in varden):
            continue
        matris[(varden[0], varden[1])] += 1  # type: ignore[index]
    return dict(matris)


# ------------------------------------------------------------------- utbytesskattning


@dataclass(frozen=True)
class Utbyte:
    """Designviktat utbyte med ändlighetskorrektion (förhandsregistreringen avsnitt 2)."""

    utbyte: float
    populationsstorlek: int
    skattat_antal_relationer: float
    varians: float

    @property
    def standardfel(self) -> float:
        return math.sqrt(self.varians)

    @property
    def intervall(self) -> tuple[float, float]:
        halva = 1.96 * self.standardfel
        return (self.utbyte - halva, self.utbyte + halva)


def skatta_utbyte(relationer_per_utsaga: dict[str, list[float]], population: dict[str, int]) -> Utbyte:
    """Skatta antalet prövbara relationer per utsaga i hela bakåtmaterialet.

        Y = summa_h (N_h / n_h) * summa_i y_hi
        R = Y / summa_h N_h
        Var(R) = (1 / X^2) * summa_h N_h^2 * (1 - n_h/N_h) * s_h^2 / n_h
    """
    saknade = sorted(set(relationer_per_utsaga) - set(population))
    if saknade:
        raise ValueError(f"stratum utan population: {', '.join(saknade)}")

    skattat = 0.0
    varians_summa = 0.0
    for stratum, varden in relationer_per_utsaga.items():
        stor_n = population[stratum]
        liten_n = len(varden)
        if liten_n > stor_n:
            raise ValueError(f"{stratum} har {liten_n} kodade utsagor men bara {stor_n} i populationen")
        skattat += (stor_n / liten_n) * sum(varden)
        if liten_n > 1:
            medel = sum(varden) / liten_n
            s2 = sum((v - medel) ** 2 for v in varden) / (liten_n - 1)
            varians_summa += stor_n**2 * (1 - liten_n / stor_n) * s2 / liten_n

    stor_x = sum(population[s] for s in relationer_per_utsaga)
    return Utbyte(
        utbyte=skattat / stor_x,
        populationsstorlek=stor_x,
        skattat_antal_relationer=skattat,
        varians=varians_summa / stor_x**2,
    )


# ------------------------------------------------------------------------ snittalet


@dataclass(frozen=True)
class Relationstal:
    """De fem talen i förhandsregistreringen avsnitt 3."""

    kodare_a: int
    kodare_b: int
    delade: int
    union: int
    jaccard: float

    @property
    def snitt(self) -> float:
        """Delade relationer plus halva antalet enkelsidiga."""
        return self.delade + (self.union - self.delade) / 2


def rakna_relationer(a: dict[str, set[str]], b: dict[str, set[str]]) -> Relationstal:
    """Jämför två kodningar på nyckeln utsaga x indikator."""
    utsagor = set(a) | set(b)
    delade = union = antal_a = antal_b = 0
    jaccard_summa = 0.0
    jaccard_enheter = 0
    for u in utsagor:
        mangd_a, mangd_b = a.get(u, set()), b.get(u, set())
        antal_a += len(mangd_a)
        antal_b += len(mangd_b)
        delade += len(mangd_a & mangd_b)
        union += len(mangd_a | mangd_b)
        if mangd_a or mangd_b:
            jaccard_summa += len(mangd_a & mangd_b) / len(mangd_a | mangd_b)
            jaccard_enheter += 1
    return Relationstal(
        kodare_a=antal_a,
        kodare_b=antal_b,
        delade=delade,
        union=union,
        jaccard=jaccard_summa / jaccard_enheter if jaccard_enheter else 1.0,
    )


# ------------------------------------------------------------------------ hämtmanifest


def sha256(fil: Path) -> str:
    digest = hashlib.sha256()
    with fil.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _citat(text: str) -> str:
    """YAML-sträng i dubbla citattecken, med lydelsen bevarad tecken för tecken.

    Styrtecken skyddas som `\\xNN` i stället för att tas bort. `mappning_framat.md` bär ett
    sådant, ett BEL i början av `S-008`, som följt med ur PDF-extraktionen. Korpusen ska
    bära dokumentets lydelse och inte en städad version av den, så tecknet stannar.
    """
    ut = []
    for tecken in text:
        if tecken == "\\":
            ut.append("\\\\")
        elif tecken == '"':
            ut.append('\\"')
        elif ord(tecken) < 0x20 or ord(tecken) == 0x7F:
            ut.append(f"\\x{ord(tecken):02x}")
        else:
            ut.append(tecken)
    return '"' + "".join(ut) + '"'


def skriv_urval(ut: Path = UTKATALOG / "urval_pilot.yaml") -> Path:
    """Dra pilotens 200 utsagor och delurvalets 40, och skriv dem med frö och metod."""
    bakat = las_bakat()
    urval = dra_urval(bakat, fro=FRO_URVAL, per_parti=PER_PARTI)
    delurval = {u.id for u in dra_urval(urval, fro=FRO_DELURVAL, per_parti=PER_PARTI_DELURVAL)}
    population = Counter(u.parti for u in bakat)

    rader = [
        "# Rösta - Verklighetsbildpilotens urval (ADR 0016 beslutspunkt 6, biljett #46 steg 3)",
        "#",
        "# Dragningen är reproducerbar. Fröet och metoden står nedan, och hasharna binder",
        "# dragningen till de två källfilerna. Ändras en källfil ändras hashen, och urvalet",
        "# måste dras om. Filen skrivs av `python -m pipeline.tools.verklighetsbild --urval`.",
        "#",
        "# Urvalet är stratifierat på parti, 25 per parti, utan återläggning. Partierna är",
        "# strata och ingenting annat: kodaren får aldrig se partikoden (kodboken avsnitt 11).",
        "",
        "version: 1",
        "beslutad_av: 'ADR 0016 beslutspunkt 6'",
        "kodbok: 'docs/verklighetsbild_pilot/kodbok_pilot.md version 1'",
        "forhandsregistrering: 'docs/verklighetsbild_pilot/forhandsregistrering.md version 1'",
        "",
        "metod: |",
        "  1. Läs mappning_bakat.md och kandidater_bakat.md i den ordning posterna står.",
        "     Mappade poster behåller sitt eget id. Kandidater får id `<PARTI>k-<nnn>`, satt av",
        "     ordningen i filen.",
        "  2. Så ett random.Random(fro) en gång.",
        "  3. Dra per parti i ordningen S, M, SD, C, V, KD, MP, L med random.sample, 25 per parti.",
        "  4. Dra delurvalet ur de 200 på samma sätt, med eget frö och 5 per parti.",
        "  Metoden ligger i pipeline/tools/verklighetsbild.py:dra_urval och prövas i",
        "  tests/test_verklighetsbild.py.",
        "",
        f"fro: {FRO_URVAL}",
        f"per_parti: {PER_PARTI}",
        f"fro_delurval: {FRO_DELURVAL}",
        f"per_parti_delurval: {PER_PARTI_DELURVAL}",
        "",
        "# SHA-256 över källfilerna som dragningen läste.",
        "korpus:",
    ]
    for filnamn in ("mappning_bakat.md", "kandidater_bakat.md"):
        antal = sum(1 for u in bakat if u.kalla == filnamn)
        rader.append(
            f"  - {{ fil: {filnamn}, poster: {antal}, sha256: {sha256(KALLKATALOG / filnamn)} }}"
        )
    rader += [
        "",
        "# N_h per stratum. Urvalsandelen n_h/N_h bär ändlighetskorrektionen i",
        "# förhandsregistreringen avsnitt 2. Den biter hårdast på MP och KD.",
        "population:",
    ]
    for parti in PARTIER:
        andel = PER_PARTI / population[parti]
        nyckel = f"{parti}:"
        rader.append(f"  {nyckel:<4}{{ N: {population[parti]:>3}, urvalsandel: {andel:.3f} }}")
    rader += [
        f"summa_population: {sum(population.values())}",
        "",
        "# De 200 dragna utsagorna, i dragningsordning. `delurval: true` märker de 40 som",
        "# A-prim och B-prim kodar blindat (förhandsregistreringen avsnitt 6).",
        "urval:",
    ]
    for u in urval:
        märke = "true " if u.id in delurval else "false"
        rader.append(
            f"  - {{ id: {u.id + ',':<10} parti: {u.parti + ',':<4}"
            f" kalla: {u.kalla + ',':<21} delurval: {märke} }}"
        )
    ut.parent.mkdir(parents=True, exist_ok=True)
    ut.write_text("\n".join(rader) + "\n", encoding="utf-8")
    return ut


# ------------------------------------------------------------------- kodningsuppdrag


def las_urval(fil: Path = UTKATALOG / "urval_pilot.yaml") -> list[dict]:
    """Läser den dragna urvalsfilen utan att dra om den."""
    import yaml

    return yaml.safe_load(fil.read_text(encoding="utf-8"))["urval"]


def blinda(utsage_id: list[str], fro: int, prefix: str) -> dict[str, str]:
    """Ger varje utsaga ett blint id i ny slumpordning.

    Utsage-id:t bär partikoden i sitt prefix. Ett blint id är det enda sättet att hålla
    kodbokens regel 11.4, alltså att kodaren aldrig väger in vilket parti utsagan kom
    från. Nyckeln ligger i `config/verklighetsbild/blindning.yaml` och når aldrig en kodare.
    """
    blandad = list(utsage_id)
    random.Random(fro).shuffle(blandad)
    return {f"{prefix}-{i:03d}": u for i, u in enumerate(blandad, start=1)}


UPPDRAGSRAM = """\
Du granskar ett mätinstrument. Uppgiften är ren kodning mot en låst kodbok.

Du ska INTE avgöra om något påstående är sant. Du ska INTE bedöma något politiskt parti.
Texterna nedan är avidentifierade utdrag ur svenska offentliga dokument, och de bär
varken avsändare eller partikod. Din uppgift är att avgöra om varje utdrag skulle gå att
pröva mot en på förhand definierad statistisk indikator, och i så fall vilken.

Följ kodboken ordagrant. Där kodboken ger en regel gäller regeln och inte ditt omdöme.
Svara med ett enda YAML-dokument och ingenting annat: ingen inledning, ingen
sammanfattning, inga kodstaket.
"""


def skriv_uppdrag(ut: Path, batchstorlek: int = UTSAGOR_PER_BATCH) -> list[Path]:
    """Skriver kodningsunderlaget, ett blindat parti utsagor per batchfil."""
    import yaml

    kodbok = (PILOTKATALOG / "kodbok_pilot.md").read_text(encoding="utf-8")
    text_per_id = {u.id: u.text for u in las_bakat()}
    urval = las_urval()

    nyckel_full = blinda([r["id"] for r in urval], FRO_BLINDNING, "U")
    nyckel_del = blinda(
        [r["id"] for r in urval if r["delurval"]], FRO_BLINDNING_DELURVAL, "D"
    )

    nyckelfil = UTKATALOG / "blindning.yaml"
    nyckelfil.write_text(
        "# Rösta - blindningsnyckeln för Verklighetsbildpiloten (biljett #46 steg 4 och 5).\n"
        "#\n"
        "# Utsage-id bär partikoden i sitt prefix. Kodarna får därför blinda id, och den här\n"
        "# filen är kopplingen tillbaka. Den når ALDRIG en kodare. Fröna står i\n"
        "# pipeline/tools/verklighetsbild.py, så nyckeln går att göra om.\n"
        "#\n"
        "# `full` gäller kodare A och B, `delurval` gäller A-prim och B-prim. De två har\n"
        "# skilda fron och skild ordning, så en kodare inte kan känna igen en utsaga.\n\n"
        + yaml.safe_dump(
            {"version": 1, "fro_full": FRO_BLINDNING, "fro_delurval": FRO_BLINDNING_DELURVAL,
             "full": nyckel_full, "delurval": nyckel_del},
            allow_unicode=True, sort_keys=False, default_flow_style=False,
        ),
        encoding="utf-8",
    )

    ut.mkdir(parents=True, exist_ok=True)
    skrivna: list[Path] = []
    for märke, nyckel in (("full", nyckel_full), ("delurval", nyckel_del)):
        poster = sorted(nyckel.items())
        for nr in range(0, len(poster), batchstorlek):
            batch = poster[nr : nr + batchstorlek]
            fil = ut / f"uppdrag_{märke}_{nr // batchstorlek + 1:02d}.md"
            rader = [
                UPPDRAGSRAM,
                "\n---\n\n# Kodboken\n\n",
                kodbok,
                "\n---\n\n# Utdragen\n\n",
                "Koda vart och ett av utdragen nedan. Använd det id som står först på raden.\n\n",
            ]
            for blint, riktigt in batch:
                rader.append(f"- `{blint}` {text_per_id[riktigt]}\n")
            rader.append(
                f"\n---\n\n# Svaret\n\nEtt YAML-dokument med exakt {len(batch)} poster under "
                "`utsagor`, i samma ordning som utdragen ovan, enligt kodbokens avsnitt 10. "
                "Sätt `kodare` till det namn du fått, `kodboksversion: 1` och `kodningsdatum` "
                "till dagens datum.\n"
            )
            fil.write_text("".join(rader), encoding="utf-8")
            skrivna.append(fil)
    return skrivna


# ------------------------------------------------------ hämtmanifest och konfigkorpus

# Brytpunkten för framåtkorpusen. Ordinarie val hålls andra söndagen i september
# (vallagen 1 kap. 3 §). Regeln ger 2014-09-14, 2018-09-09, 2022-09-11 och 2026-09-13,
# alltså exakt de fyra valdagar `config/mappings.yaml` redan bär. Nästa blir 2030-09-08.
BRYTPUNKT = "2030-09-08"

# En framåtutsaga får ett förhandsregistrerat indikatorval bara om den bär BÅDE en storhet
# och en period (ADR 0016 beslutspunkt 4). Filtret är grovt med flit: det ska hellre släppa
# igenom för mycket än sålla bort en utsaga som bär båda.
STORHET = re.compile(
    r"\d|procent|procentenhet|kronor|miljard|miljon|andel|antal|dubbl|halver|fördubbl|tredubbl",
    re.IGNORECASE,
)
PERIOD = re.compile(
    r"(19|20)\d{2}|senast|inom \w+ år|mandatperiod|per år|årlig|året|fram till|till och med",
    re.IGNORECASE,
)


def forhandsregistrerbara(utsagor: list[Utsaga]) -> list[Utsaga]:
    """De framåtutsagor som bär både en storhet och en period."""
    return [u for u in utsagor if STORHET.search(u.text) and PERIOD.search(u.text)]


def skriv_hamtmanifest(ut: Path = UTKATALOG / "hamtmanifest.yaml") -> Path:
    """Ett hämtmanifest per källdokument: filnamn, hämtdatum, storlek och SHA-256."""
    rader = [
        "# Rösta - hämtmanifest för valmanifesten 2026 (ADR 0016 beslutspunkt 3, biljett #46).",
        "#",
        "# PDF:erna ligger UTANFÖR git. Repot är publikt och dokumenten är upphovsrättsskyddade",
        "# verk, och instrumentet behöver för sin prövning bara de citerade meningarna.",
        "# `.gitignore` håller dem utanför sedan d82100d.",
        "#",
        "# BEGRÄNSNINGEN, i klartext: hashen styrker VILKET dokument som lästes, men den",
        "# återskapar det inte. Dör partiets URL finns ingen väg tillbaka till dokumentet.",
        "#",
        "# `url` är TOM för alla åtta. Adresserna skrevs inte ned vid hämtningen 2026-09-13 och",
        "# står varken i mappningsfilerna, i biljett #42 eller i PDF:ernas metadata. De gissas",
        "# inte här. Fältet fylls av den som kan belägga adressen, och `arkivadress` är ett",
        "# frivilligt fält för en kopia hos oberoende tredje part.",
        "#",
        "# `hamtdatum` vilar på två ben: mappningsfilerna säger själva att materialet är",
        "# framställt 2026-09-13 ur dessa filer, och filernas tidsstämplar ligger samma dag.",
        "",
        "version: 1",
        "hamtdatum_kalla: 'mappningsfilernas egen ingress plus filernas tidsstämpel'",
        "dokument:",
    ]
    for parti in PARTIER:
        filnamn = KALLDOKUMENT[parti]
        fil = KALLKATALOG / filnamn
        if not fil.exists():
            raise FileNotFoundError(f"{filnamn} saknas i {KALLKATALOG}")
        rader += [
            f"  - id: {parti}",
            f"    filnamn: {filnamn}",
            "    hamtdatum: 2026-09-13",
            "    url: null",
            "    arkivadress: null",
            f"    byte: {fil.stat().st_size}",
            f"    sha256: {sha256(fil)}",
        ]
    ut.parent.mkdir(parents=True, exist_ok=True)
    ut.write_text("\n".join(rader) + "\n", encoding="utf-8")
    return ut


def _korpusrader(utsagor: list[Utsaga]) -> list[str]:
    rader = []
    for u in utsagor:
        rader += [
            f"  - id: {u.id}",
            f"    dokument: {u.parti}",
            f"    kategori: {_citat(u.kategori)}",
            f"    sida: {u.sida if u.sida is not None else 'null'}",
            f"    kalla: {u.kalla}",
        ]
        if u.anmarkning:
            rader.append(f"    anmarkning: {u.anmarkning}")
        rader.append(f"    citat: {_citat(u.text)}")
    return rader


def skriv_korpus(ut: Path = UTKATALOG) -> list[Path]:
    """Skriver bakåt- och framåtkorpusen i configformat (ADR 0016 beslutspunkt 3 och 4)."""
    huvud = [
        "# Påstående, observation och indikator är TRE SKILDA OBJEKT (ADR 0016 beslutspunkt 3).",
        "#",
        "#   pastaenden   textens egen utsaga, med bevarad lydelse. Ligger nedan.",
        "#   indikatorer  modellens på förhand definierade mätvariabler. Ligger i",
        "#                config/categories.yaml och dubbleras ALDRIG hit.",
        "#   observationer  ett indikatorvärde för en viss period och population. Tom i v0:",
        "#                piloten kodar ingen sanning (kodboken avsnitt 1).",
        "#",
        "# Semantisk likhet räcker inte som koppling mellan de tre. Publicerade bedömningar",
        "# är append-only: en post ändras aldrig, den läggs till.",
        "",
        "version: 1",
        "hamtmanifest: hamtmanifest.yaml",
        "indikatorregister: '../categories.yaml'",
        "observationer: []",
    ]

    bakat = las_bakat()
    bakatfil = ut / "korpus_bakat.yaml"
    bakatfil.write_text(
        "\n".join(
            [
                "# Rösta - bakåtkorpusen för Verklighetsbild (biljett #46 steg 8).",
                "#",
                "# 896 bakåtblickande utsagor ur de åtta valmanifesten: 230 mappade och 666",
                "# kandidater. Lydelsen är partiets egen. Kandidaternas id är härledda av",
                "# ordningen i kandidater_bakat.md och är därefter fasta.",
                "",
                *huvud,
                "",
                f"antal: {len(bakat)}",
                "pastaenden:",
                *_korpusrader(bakat),
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    framat = las_framat()
    kandidater = forhandsregistrerbara(framat)
    framatfil = ut / "korpus_framat.yaml"
    framatfil.write_text(
        "\n".join(
            [
                "# Rösta - den FRYSTA framåtkorpusen för Verklighetsbild (biljett #46 steg 7).",
                "#",
                "# 1 073 framåtblickande poster. Framåthalvan lämnade instrumentet i ADR 0016",
                "# beslutspunkt 4 och fryses här. Ett rent uteslutande räckte inte, eftersom det",
                "# öppnar för efterhandsval av formulering, indikator och tröskel när perioden",
                "# väl är slut.",
                "#",
                "# FRYSNINGEN BINDER: originaltexten ändras aldrig, id är fasta, dokumenthashen",
                "# ligger i hamtmanifest.yaml, och ingen post får läggas till eller tas bort.",
                "",
                *huvud,
                "",
                f"brytpunkt: {BRYTPUNKT}",
                "brytpunkt_skal: |",
                "  Ordinarie val hålls andra söndagen i september. Regeln ger 2014-09-14,",
                "  2018-09-09, 2022-09-11 och 2026-09-13, alltså exakt de fyra valdagar",
                "  config/mappings.yaml redan bär, och därefter 2030-09-08. Före den dagen är",
                "  perioden inte slut och ingen framåtpost går att pröva.",
                "",
                "# ADR 0016 beslutspunkt 4: indikatorval förhandsregistreras BARA där utsagan bär",
                "# både en storhet och en period. Villkoret uppfylls av NOLL av de 1 073 posterna.",
                "#",
                "# Skälet står i mappning_framat.md: posten är rubriken eller punkten, och den",
                "# fulla texten står i PDF:en. Rubriker bär sällan tal och aldrig en period. Noll",
                "# poster bär ett årtal, och 22 bär över huvud taget en siffra.",
                "#",
                "# Detta är ett fynd om korpusens FORM och inte om partiernas löften. Ska",
                "# förhandsregistrering bli möjlig måste posterna bära den fulla lydelsen ur",
                "# PDF:en, inte rubriken. Filtret ligger i",
                "# pipeline/tools/verklighetsbild.py:forhandsregistrerbara och går att köra om.",
                f"forhandsregistrerade_indikatorval: []   # {len(kandidater)} poster klarade filtret",
                "",
                f"antal: {len(framat)}",
                "pastaenden:",
                *_korpusrader(framat),
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return [bakatfil, framatfil]


def _main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--korpus", action="store_true", help="räkna korpusen och skriv en sammanfattning")
    p.add_argument("--urval", action="store_true", help="dra de 200 och delurvalets 40 -> config")
    p.add_argument("--uppdrag", metavar="KATALOG", help="skriv blindat kodningsunderlag dit")
    p.add_argument("--manifest", action="store_true", help="skriv hämtmanifestet med SHA-256")
    p.add_argument("--skriv-korpus", action="store_true", help="skriv bakåt- och framåtkorpus -> config")
    args = p.parse_args(argv)
    if args.manifest:
        print(f"skrev {skriv_hamtmanifest()}")
    if args.skriv_korpus:
        for fil in skriv_korpus():
            print(f"skrev {fil}")
    if args.korpus:
        bakat, framat = las_bakat(), las_framat()
        print(json.dumps({"bakat": len(bakat), "framat": len(framat)}, ensure_ascii=False))
    if args.urval:
        print(f"skrev {skriv_urval()}")
    if args.uppdrag:
        for fil in skriv_uppdrag(Path(args.uppdrag)):
            print(f"skrev {fil}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
