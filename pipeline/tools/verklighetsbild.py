"""Verktyg för Verklighetsbildpiloten (ADR 0016, biljett #46).

Modulen körs FÖR HAND och aldrig av pipelinen. Verklighetsbild har vikt 0, ingår inte i
någon poäng och rör varken `dist/`, `config/categories.yaml` eller gränssnittet
(ADR 0016, sista följdpunkten). Därför ligger den i `pipeline/tools/` och importeras
inte av `pipeline/build_all.py`.

Stegen körs i biljettens ordning, och varje steg committas innan nästa börjar:

    python -m pipeline.tools.verklighetsbild --urval               # steg 3: dra 200 + 40
    python -m pipeline.tools.verklighetsbild --uppdrag KATALOG     # steg 4: blindat underlag
    python -m pipeline.tools.verklighetsbild --kodning A KATALOG   # steg 4: råsvar -> config
    python -m pipeline.tools.verklighetsbild --resultat            # steg 6: utbyte och alfa
    python -m pipeline.tools.verklighetsbild --manifest            # steg 8: SHA-256 per PDF
    python -m pipeline.tools.verklighetsbild --skriv-korpus        # steg 7 och 8: korpus
    python -m pipeline.tools.verklighetsbild --korpus              # räkna korpusen, skriv inget

Räkningarna, alla prövade i `tests/test_verklighetsbild.py`:

  las_bakat / las_framat   läser de tre markdownfilerna i docs/valmanifest_2026/ och ger
                           utsagor med stabila id. Mappade poster behåller sitt eget id.
                           Kandidater får ett härlett id av formen `<PARTI>k-<nnn>`, satt
                           av ordningen i filen.
  dra_urval                stratifierad dragning utan återläggning, 25 per parti, med frö.
  blinda                   ger varje utsaga ett blint id, så kodaren aldrig ser partikoden.
  granska_kodning          prövar en kodad utsaga mot ADR 0016 godkännandetest 4.
  krippendorff_alfa        alfa för nominal och ordinal skala, med förväxlingsmatris.
  skatta_utbyte            designviktat medelvärde med ändlighetskorrektion per stratum.
  prova_trosklarna         de två trösklarna i förhandsregistreringen.

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

import yaml

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

# Kodboken avsnitt 3.1 regel 7 sätter taket till sex led per utsaga. Skalan för
# avgränsningens ordinala alfa följer det taket.
LEDORDNING = [str(n) for n in range(0, 7)]


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
    utanfor = sorted(v for v in marginal if v not in index)
    if utanfor:
        raise ValueError(f"värden utanför den ordinala skalan: {', '.join(utanfor)}")

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
    """Skriver kodningsunderlaget, ett blindat parti utsagor per batchfil.

    Skriver också nyckeln till `config/verklighetsbild/blindning.yaml`, alltså UTANFÖR
    `ut`. De två hör ihop: utan nyckeln går kodarens svar inte att översätta tillbaka.
    Batchfilerna går till `ut`, som ligger utanför repot, eftersom de bär kodboken plus
    utdragen och är helt härledbara ur nyckeln och korpusen.
    """
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


# ------------------------------------------------------------------ inläst kodning


@dataclass(frozen=True)
class KodadUtsaga:
    """En utsaga som en kodare lämnat ifrån sig, reducerad till de fyra momenten."""

    utsaga_id: str
    antal_led: int
    relationer: tuple[str, ...]
    forsta_indikator: str
    kodvarde: str

    @property
    def provbar(self) -> bool:
        return bool(self.relationer)


@dataclass(frozen=True)
class Granskning:
    """Utfallet av att pröva en kodad utsaga mot reglerna.

    `fel` är brott mot ADR 0016 godkännandetest 4, alltså den regel piloten står och
    faller med. `anmarkningar` är avvikelser från kodbokens egna fältregler i avsnitt 10.
    De skiljs åt därför att kodboken motsäger sig själv på en punkt, se `granska_kodning`.
    """

    fel: list[str]
    anmarkningar: list[str]


def granska_kodning(post: dict) -> Granskning:
    """Prövar en kodad utsaga mot godkännandetest 4 och mot kodbokens fältregler.

    HÅRD REGEL, ADR 0016 godkännandetest 4: varje kodad utsaga bär antingen minst en
    relation eller exakt en bortfallskod ur den låsta listan om sju.

    MJUK REGEL, kodbokens avsnitt 10: fältreglerna per led. De är anmärkningar och inga
    fel, eftersom den låsta kodboken motsäger sig själv: avsnitt 6.5 säger att en
    matchning mot en indikator utan inläst serie ändå skrivs i operationaliseringsfältet,
    medan avsnitt 10 kräver att fältet är null när ledet inte är prövbart. En kodare kan
    följa den ena regeln eller den andra, men inte båda. Kodboken är låst och rättas inte
    i efterhand (godkännandetest 1). Motsägelsen redovisas i stället och binder
    produktionskodboken.
    """
    fel: list[str] = []
    anmarkningar: list[str] = []
    uid = post.get("utsaga_id", "?")
    led = post.get("led") or []
    if not led:
        fel.append(f"{uid}: bär inga led")

    bortfall_i_led: list[str] = []
    for nr, ett_led in enumerate(led, start=1):
        plats = f"{uid} led {nr}"
        if ett_led.get("provbar"):
            saknade = [f for f in ("indikator", "period", "operationalisering") if not ett_led.get(f)]
            if saknade:
                fel.append(f"{plats}: prövbart led saknar {', '.join(saknade)}")
            if ett_led.get("bortfall") is not None:
                anmarkningar.append(f"{plats}: prövbart led bär ändå en bortfallskod")
        else:
            kod = ett_led.get("bortfall")
            if kod not in BORTFALLSKODER:
                fel.append(f"{plats}: bortfallskoden {kod!r} står utanför den låsta listan")
            else:
                bortfall_i_led.append(kod)
            satta = [f for f in ("indikator", "period", "operationalisering") if ett_led.get(f)]
            if satta:
                anmarkningar.append(f"{plats}: ej prövbart led bär ändå {', '.join(satta)}")

    har_relation = any(
        ett_led.get("provbar") and ett_led.get("indikator") for ett_led in led
    )
    utsagans_kod = post.get("bortfall")
    if har_relation:
        if utsagans_kod is not None:
            fel.append(f"{uid}: bär en relation men ändå bortfallskoden {utsagans_kod!r}")
    elif utsagans_kod not in BORTFALLSKODER:
        fel.append(f"{uid}: saknar relation och bär ingen giltig bortfallskod")
    elif bortfall_i_led:
        vantad = min(bortfall_i_led, key=BORTFALLSKODER.index)
        if utsagans_kod != vantad:
            anmarkningar.append(
                f"{uid}: utsagans kod är {utsagans_kod!r}, men företrädesordningen ger {vantad!r}"
            )
    return Granskning(fel=fel, anmarkningar=anmarkningar)


def las_kodning(filer: list[Path], nyckel: dict[str, str] | None = None) -> dict[str, KodadUtsaga]:
    """Läser en kodares YAML och reducerar varje utsaga till de fyra momenten.

    `nyckel` översätter blinda id till utsage-id och behövs för kodarens råsvar. De
    normaliserade configfilerna bär redan utsage-id, och då lämnas nyckeln utanför.
    """
    kodade: dict[str, KodadUtsaga] = {}
    for fil in sorted(filer):
        dokument = yaml.safe_load(fil.read_text(encoding="utf-8"))
        for post in dokument["utsagor"]:
            uid = post["utsaga_id"]
            if nyckel is not None:
                if uid not in nyckel:
                    raise ValueError(f"{fil.name}: okänt blint id {uid!r}")
                uid = nyckel[uid]
            if uid in kodade:
                raise ValueError(f"{uid} kodad två gånger ({fil.name})")
            led = post.get("led") or []
            relationer = tuple(
                ett_led["indikator"] for ett_led in led if ett_led.get("provbar") and ett_led.get("indikator")
            )
            kodade[uid] = KodadUtsaga(
                utsaga_id=uid,
                antal_led=len(led),
                relationer=relationer,
                forsta_indikator=relationer[0] if relationer else "ingen",
                kodvarde="relation" if relationer else (post.get("bortfall") or "saknas"),
            )
    return kodade


def momentpar(a: dict[str, KodadUtsaga], b: dict[str, KodadUtsaga]) -> dict[str, Par]:
    """De fyra momenten i kodbokens avsnitt 9, som par redo för alfa."""
    gemensamma = sorted(set(a) & set(b))

    def ja_nej(k: KodadUtsaga) -> str:
        return "ja" if k.provbar else "nej"

    return {
        "avgransning": {u: [str(a[u].antal_led), str(b[u].antal_led)] for u in gemensamma},
        "provbarhet": {u: [ja_nej(a[u]), ja_nej(b[u])] for u in gemensamma},
        "indikatorval": {u: [a[u].forsta_indikator, b[u].forsta_indikator] for u in gemensamma},
        "kodvarde": {u: [a[u].kodvarde, b[u].kodvarde] for u in gemensamma},
    }


# Kodarna och deras körningsspår. `spar` pekar på var körningen går att belägga utanför
# repot. Codexkörningarna ligger som sessionsfiler under CODEX_HOME, på samma villkor som
# valmanifestens PDF:er: de går att peka på men inte att versionshantera här.
# BEGRÄNSNINGEN i klartext: inget av spåren ligger i git. Godkännandetest 6 prövar att två
# SKILDA kodningar finns, och att varje kodning pekar ut sitt spår. Att spåret finns går
# att kontrollera på maskinen som körde, men inte ur repot. Anthropicsidan bär inga
# sessions-id alls, eftersom subagentkörningarna inte ger några.
KODARE = {
    "A": {
        "leverantor": "Anthropic",
        "modell": "Claude Opus 5",
        "uppdrag": "full",
        "spar": "Claude Code-subagenter, 8 batchar om 25, 2026-09-13",
    },
    "B": {
        "leverantor": "OpenAI",
        "modell": "Codex, gpt-5.6-sol",
        "uppdrag": "full",
        "spar": "codex exec, 8 sessioner 2026-09-13 21:52-22:03, se sessioner nedan",
        "sessioner": [
            "01a09c53-b691-76b2-8b3b-c7a473c814fa",
            "01a09c55-4071-7c42-a20d-feb4e0521c6f",
            "01a09c56-8673-7dc3-8d08-92251fe4633a",
            "01a09c58-3e9e-77e1-b614-836945b9a6a1",
            "01a09c59-8f5d-7a42-bf24-ad1113f4cd14",
            "01a09c5b-2de7-7003-829c-8c9422d7469e",
            "01a09c5c-ce53-7d52-8372-d22cc0b1404f",
            "01a09c5e-4c20-7300-83d9-c835effd08c0",
        ],
    },
    "A-prim": {
        "leverantor": "Anthropic",
        "modell": "Claude Opus 5",
        "uppdrag": "delurval",
        "spar": "Claude Code-subagenter, 2 batchar, 2026-09-13",
    },
    "B-prim": {
        "leverantor": "OpenAI",
        "modell": "Codex, gpt-5.6-sol",
        "uppdrag": "delurval",
        "spar": "codex exec, 2 sessioner 2026-09-13 22:05-22:07, se sessioner nedan",
        "sessioner": [
            "01a09c60-1c42-7f12-b3a1-c64f524ec2e5",
            "01a09c62-0056-7a51-acf2-bcf921c85482",
        ],
    },
}


def _period(period: object) -> str:
    """Perioden som YAML-flödesmappning, skriven ut i stället för tagen ur en repr.

    Kodarens svar är fritt YAML, så perioden kan komma i mer än en form. Att lita på
    Pythons repr skulle skriva en sträng som råkar se ut som YAML, och den räddningen
    håller inte för ett värde ingen förutsåg.
    """
    if not period:
        return "null"
    if isinstance(period, dict):
        delar = ", ".join(f"{nyckel}: {varde}" for nyckel, varde in period.items())
        return "{ " + delar + " }"
    return _citat(str(period))


def _kodningsfil(kodare: str) -> str:
    return f"kodning_{kodare.lower().replace('-', '_')}.yaml"


def skriv_kodning(kallfiler: list[Path], kodare: str, ut: Path) -> tuple[Path, list[str], list[str]]:
    """Översätter en kodares råsvar till configformat och prövar dem mot reglerna."""
    if kodare not in KODARE:
        raise ValueError(f"okänd kodare {kodare!r}")
    fakta = KODARE[kodare]
    nyckelfil = yaml.safe_load((UTKATALOG / "blindning.yaml").read_text(encoding="utf-8"))
    nyckel = nyckelfil["full" if fakta["uppdrag"] == "full" else "delurval"]
    parti_per_utsaga = {u.id: u.parti for u in las_bakat()}

    fel: list[str] = []
    anmarkningar: list[str] = []
    rader = [
        f"# Rösta - kodning {kodare} i Verklighetsbildpiloten (biljett #46 steg 4 och 5).",
        "#",
        "# Råsvaren är översatta från blinda id till utsage-id via blindning.yaml. Ingenting",
        "# annat är ändrat: leden, koderna och operationaliseringarna står som kodaren skrev",
        "# dem. Ingen sammanjämkning har skett (förhandsregistreringen avsnitt 4.2).",
        "",
        "version: 1",
        f"kodare: {kodare}",
        f"leverantor: {fakta['leverantor']}",
        f"modell: '{fakta['modell']}'",
        f"uppdrag: {fakta['uppdrag']}",
        f"spar: {_citat(fakta['spar'])}",
        *(
            ["sessioner:"] + [f"  - {s}" for s in fakta["sessioner"]]
            if fakta.get("sessioner")
            else ["sessioner: []"]
        ),
        "kodboksversion: 1",
        "kodningsdatum: 2026-09-13",
        "sag_andra_kodarens_svar: false",
        "utsagor:",
    ]
    antal = 0
    for fil in sorted(kallfiler):
        text = fil.read_text(encoding="utf-8")
        dokument = yaml.safe_load(text)
        for post in dokument["utsagor"]:
            blint = post["utsaga_id"]
            if blint not in nyckel:
                raise ValueError(f"{fil.name}: okänt blint id {blint!r}")
            granskning = granska_kodning(post)
            fel += granskning.fel
            anmarkningar += granskning.anmarkningar
            uid = nyckel[blint]
            antal += 1
            rader += [
                f"  - utsaga_id: {uid}",
                f"    parti: {parti_per_utsaga[uid]}",
                f"    blint_id: {blint}",
                f"    bortfall: {post.get('bortfall') or 'null'}",
                "    led:",
            ]
            for ett_led in post.get("led") or []:
                operationalisering = ett_led.get("operationalisering")
                rader += [
                    f"      - text: {_citat(str(ett_led.get('text') or ''))}",
                    f"        provbar: {'true' if ett_led.get('provbar') else 'false'}",
                    f"        indikator: {ett_led.get('indikator') or 'null'}",
                    f"        period: {_period(ett_led.get('period'))}",
                    "        operationalisering: "
                    + (_citat(str(operationalisering)) if operationalisering else "null"),
                    f"        bortfall: {ett_led.get('bortfall') or 'null'}",
                ]
            if post.get("anteckning"):
                rader.append(f"    anteckning: {_citat(str(post['anteckning']))}")
    rader.insert(rader.index("utsagor:"), f"antal: {antal}")
    ut.parent.mkdir(parents=True, exist_ok=True)
    ut.write_text("\n".join(rader) + "\n", encoding="utf-8")
    return ut, fel, anmarkningar


# ------------------------------------------------------------------ tröskelprövning

# Krippendorffs konventionella nivåer, låsta i förhandsregistreringen avsnitt 4.
ALFA_HALLER = 0.800
ALFA_TENTATIVT = 0.667

# Utbyteströsklarna, låsta i förhandsregistreringen avsnitt 1.
TROSKEL_UTBYTE = 0.20
TROSKEL_RELATIONER_PER_PARTI = 5


def full_overensstammelse(par: Par) -> bool:
    """Sant när ingen enhet bär någon oenighet alls."""
    satta = [[v for v in varden if v is not None] for varden in par.values()]
    jamforbara = [v for v in satta if len(v) >= 2]
    return bool(jamforbara) and all(len(set(v)) == 1 for v in jamforbara)


def alfabesked(alfa: float | None, alla_overens: bool = False) -> str:
    """Krippendorffs nivåer, plus en läsning av det odefinierade fallet.

    Alfa är odefinierad när materialet saknar variation. Det kan betyda två skilda
    saker, och de får inte blandas ihop:

      - Kodarna satte SAMMA värde på varje enhet. Då finns ingen oenighet att mäta, och
        att kalla det `håller inte` vore en felläsning. Beskedet blir `full enighet`.
      - Alla värden är lika av något annat skäl, till exempel för få enheter. Då säger
        materialet ingenting, och beskedet blir `odefinierad`.
    """
    if alfa is None:
        return "full enighet" if alla_overens else "odefinierad"
    if alfa >= ALFA_HALLER:
        return "haller"
    if alfa >= ALFA_TENTATIVT:
        return "tentativt"
    return "haller inte"


@dataclass(frozen=True)
class Troskelprovning:
    """Utfallet av de två trösklarna i förhandsregistreringen."""

    utbyte: Utbyte
    snitt_per_parti: dict[str, float]
    alfa: dict[str, float | None]
    full_enighet: dict[str, bool]

    @property
    def utbyte_klaras(self) -> bool:
        return self.utbyte.utbyte >= TROSKEL_UTBYTE

    @property
    def partier_under_fem(self) -> dict[str, float]:
        return {p: v for p, v in self.snitt_per_parti.items() if v < TROSKEL_RELATIONER_PER_PARTI}

    @property
    def provbarheten_haller(self) -> bool:
        """Bara prövbarhetens alfa fäller piloten (förhandsregistreringen avsnitt 4.1).

        Är alfa odefinierad därför att kodarna var överens om varje utsaga, har tröskeln
        inte fallit. Den har inget värde att falla under. Är den odefinierad av något
        annat skäl säger materialet ingenting, och då håller momentet inte.
        """
        alfa = self.alfa.get("provbarhet")
        if alfa is None:
            return self.full_enighet.get("provbarhet", False)
        return alfa >= ALFA_TENTATIVT

    @property
    def piloten_klaras(self) -> bool:
        return self.utbyte_klaras and not self.partier_under_fem and self.provbarheten_haller


def prova_trosklarna(
    a: dict[str, KodadUtsaga],
    b: dict[str, KodadUtsaga],
    parti_per_utsaga: dict[str, str],
    population: dict[str, int],
) -> Troskelprovning:
    """Räknar utbytet på snittet av de två kodningarna, och alfa för de fyra momenten.

    Snittet är delade relationer plus halva antalet enkelsidiga, låst i
    förhandsregistreringen avsnitt 3. En relation räknas som delad när båda kodarna gett
    samma utsaga samma indikator.
    """
    gemensamma = sorted(set(a) & set(b))
    if not gemensamma:
        raise ValueError("kodarna delar ingen utsaga")
    per_stratum: dict[str, list[float]] = {p: [] for p in population}
    snitt_per_parti: dict[str, float] = dict.fromkeys(population, 0.0)
    for u in gemensamma:
        mangd_a, mangd_b = set(a[u].relationer), set(b[u].relationer)
        delade = len(mangd_a & mangd_b)
        snitt = delade + (len(mangd_a | mangd_b) - delade) / 2
        parti = parti_per_utsaga[u]
        per_stratum[parti].append(snitt)
        snitt_per_parti[parti] += snitt

    par = momentpar(a, b)
    alfa = {
        "avgransning": krippendorff_alfa(par["avgransning"], "ordinal", LEDORDNING),
        "provbarhet": krippendorff_alfa(par["provbarhet"], "nominal"),
        "indikatorval": krippendorff_alfa(par["indikatorval"], "nominal"),
        "kodvarde": krippendorff_alfa(par["kodvarde"], "nominal"),
    }
    tomma = sorted(p for p, v in per_stratum.items() if not v)
    if tomma:
        # Ett tomt stratum skulle tyst krympa nämnaren från 896, och utbytet skulle
        # se större ut än det är. Hellre stopp än ett för högt tal.
        raise ValueError(f"inget kodat i stratum: {', '.join(tomma)}")
    return Troskelprovning(
        utbyte=skatta_utbyte(per_stratum, dict(population)),
        snitt_per_parti=snitt_per_parti,
        alfa=alfa,
        full_enighet={moment: full_overensstammelse(par[moment]) for moment in alfa},
    )


# ----------------------------------------------------------------------- resultatet


def _andel_med_fpc(traffar: int, n: int, stor_n: int) -> tuple[float, float, list[float]]:
    """Andel med ändlighetskorrektion, som förhandsregistreringen avsnitt 2 utfäster.

        Var(p) = (1 - n/N) * p*(1-p) / (n-1)

    BEGRÄNSNINGEN: vid p = 0 eller p = 1 kollapsar det normala intervallet till en punkt
    och säger ingenting. Fyra partier ligger på 0. Intervallet redovisas ändå, eftersom
    förhandsregistreringen utfäste det, och kollapsen skrivs ut i resultatet.
    """
    p = traffar / n
    varians = (1 - n / stor_n) * p * (1 - p) / (n - 1) if n > 1 else 0.0
    halva = 1.96 * math.sqrt(varians)
    return round(p, 4), round(math.sqrt(varians), 4), [
        round(max(0.0, p - halva), 4),
        round(min(1.0, p + halva), 4),
    ]


def _avrundad(par: Par) -> float | None:
    """Nominal alfa avrundad, utan besked och utan matris."""
    alfa = krippendorff_alfa(par, "nominal")
    return None if alfa is None else round(alfa, 4)


def _alfapost(par: Par, skala: str, ordning: list[str] | None = None) -> dict:
    alfa = krippendorff_alfa(par, skala, ordning)
    overens = full_overensstammelse(par)
    matris = forvaxlingsmatris(par)
    return {
        "skala": skala,
        "enheter": len(par),
        "alfa": None if alfa is None else round(alfa, 4),
        "besked": alfabesked(alfa, overens),
        "forvaxlingsmatris": {f"{c} | {k}": n for (c, k), n in sorted(matris.items())},
    }


def rakna_resultat(
    a: dict[str, KodadUtsaga],
    b: dict[str, KodadUtsaga],
    delurval: dict[str, dict[str, KodadUtsaga]],
) -> dict:
    """Sammanställer utbytet, reliabiliteten och tröskelprövningen."""
    korpus = las_bakat()
    utsagor = {u.id: u for u in korpus}
    okanda = sorted((set(a) | set(b)) - set(utsagor))
    if okanda:
        raise ValueError(f"kodade utsagor som inte finns i korpusen: {', '.join(okanda[:5])}")
    parti_per_utsaga = {uid: utsagor[uid].parti for uid in set(a) | set(b)}
    population = Counter(u.parti for u in korpus)

    provning = prova_trosklarna(a, b, parti_per_utsaga, dict(population))
    par = momentpar(a, b)

    per_parti: dict[str, dict] = {}
    for parti in PARTIER:
        ids = [uid for uid in sorted(set(a) & set(b)) if parti_per_utsaga[uid] == parti]
        mangder_a = {uid: set(a[uid].relationer) for uid in ids}
        mangder_b = {uid: set(b[uid].relationer) for uid in ids}
        tal = rakna_relationer(mangder_a, mangder_b)
        kategorier = {
            utsagor[uid].kategori for uid in ids if mangder_a[uid] or mangder_b[uid]
        }
        med_relation = sum(1 for uid in ids if mangder_a[uid] or mangder_b[uid])
        andel, standardfel, intervall = _andel_med_fpc(med_relation, len(ids), population[parti])
        per_parti[parti] = {
            "kodade_utsagor": len(ids),
            "population": population[parti],
            "urvalsandel": round(len(ids) / population[parti], 3),
            "andel_med_relation": andel,
            "andel_standardfel": standardfel,
            "andel_intervall_95": intervall,
            "kodare_a": tal.kodare_a,
            "kodare_b": tal.kodare_b,
            "delade": tal.delade,
            "union": tal.union,
            "snitt": tal.snitt,
            "utsagor_med_relation": med_relation,
            "representerade_kategorier": len(kategorier),
        }

    del_resultat: dict[str, dict] = {}
    for namn, (x, y) in {
        "a_mot_a_prim": ("A", "A-prim"),
        "b_mot_b_prim": ("B", "B-prim"),
        "a_prim_mot_b_prim": ("A-prim", "B-prim"),
    }.items():
        forsta = {"A": a, "B": b}.get(x) or delurval.get(x)
        andra = {"A": a, "B": b}.get(y) or delurval.get(y)
        if not forsta or not andra:
            continue
        gemensamma = sorted(set(forsta) & set(andra))
        if not gemensamma:
            continue
        delpar = momentpar(
            {u: forsta[u] for u in gemensamma}, {u: andra[u] for u in gemensamma}
        )
        del_resultat[namn] = {
            "kodare": [x, y],
            "samma_leverantor": KODARE[x]["leverantor"] == KODARE[y]["leverantor"],
            "enheter": len(gemensamma),
            "provbarhet_alfa": _avrundad(delpar["provbarhet"]),
            "kodvarde_alfa": _avrundad(delpar["kodvarde"]),
            "indikatorval_alfa": _avrundad(delpar["indikatorval"]),
        }

    hela = rakna_relationer(
        {uid: set(a[uid].relationer) for uid in a}, {uid: set(b[uid].relationer) for uid in b}
    )
    return {
        "version": 1,
        "kodboksversion": 1,
        "kodningsdatum": "2026-09-13",
        "kodade_utsagor": len(set(a) & set(b)),
        "utbyte": {
            "definition": "prövbara relationer per kodad utsaga, skattat till hela bakåtmaterialet",
            "designviktat": round(provning.utbyte.utbyte, 4),
            "skattat_antal_relationer": round(provning.utbyte.skattat_antal_relationer, 1),
            "populationsstorlek": provning.utbyte.populationsstorlek,
            "standardfel": round(provning.utbyte.standardfel, 4),
            "intervall_95": [round(v, 4) for v in provning.utbyte.intervall],
            "troskel": TROSKEL_UTBYTE,
            "kodare_a_relationer": hela.kodare_a,
            "kodare_b_relationer": hela.kodare_b,
            "delade_relationer": hela.delade,
            "union_relationer": hela.union,
            "snitt_relationer": hela.snitt,
            "jaccard": round(hela.jaccard, 4),
        },
        "per_parti": per_parti,
        "reliabilitet": {
            "avgransning": _alfapost(par["avgransning"], "ordinal", LEDORDNING),
            "provbarhet": _alfapost(par["provbarhet"], "nominal"),
            "indikatorval": _alfapost(par["indikatorval"], "nominal"),
            "kodvarde": _alfapost(par["kodvarde"], "nominal"),
        },
        "delurval": del_resultat,
        "utfall": {
            "utbyte_klaras": provning.utbyte_klaras,
            "partier_under_fem": sorted(provning.partier_under_fem),
            "provbarheten_haller": provning.provbarheten_haller,
            "piloten_klaras": provning.piloten_klaras,
        },
    }


# ------------------------------------------------------ hämtmanifest och konfigkorpus

# Brytpunkten för framåtkorpusen. Ordinarie val hålls andra söndagen i september
# (vallagen 1 kap. 3 §). Regeln ger 2014-09-14, 2018-09-09, 2022-09-11 och 2026-09-13,
# alltså exakt de fyra valdagar `config/mappings.yaml` redan bär. Nästa blir 2030-09-08.
BRYTPUNKT = "2030-09-08"

# En framåtutsaga får ett förhandsregistrerat indikatorval bara om den bär BÅDE en storhet
# och en period (ADR 0016 beslutspunkt 4). Filtret är grovt med flit: det ska hellre släppa
# igenom för mycket än sålla bort en utsaga som bär båda.
#
# Storhetsprovet följer kodbokens avsnitt 4 punkt 3, som godtar `en riktning ELLER en nivå`.
# Ett tal krävs alltså inte: `fler brott utreds` bär storheten antal utredda brott och en
# riktning. Ett snävare prov, som bara letat tal och storhetsord, hade sållat bort dem och
# gjort utfallet till en artefakt av filtret i stället för ett besked om korpusen.
STORHET = re.compile(
    r"\d|procent|procentenhet|kronor|miljard|miljon|andel|antal|dubbl|halver|fördubbl|tredubbl"
    r"|\bfler\b|\bfärre\b|\bökad|\bökar\b|\bminskad|\bminskar\b|\bhögre\b|\blägre\b"
    r"|\bstarkare\b|\bkortare\b|\blängre\b|\bsnabbare\b",
    re.IGNORECASE,
)
PERIOD = re.compile(
    r"(19|20)\d{2}|senast|inom \w+ år|mandatperiod|per år|årlig|året|fram till|till och med",
    re.IGNORECASE,
)


def forhandsregistrerbara(utsagor: list[Utsaga]) -> list[Utsaga]:
    """De framåtutsagor som bär både en storhet och en period."""
    return [u for u in utsagor if STORHET.search(u.text) and PERIOD.search(u.text)]


# Förhandsregistreringen av indikatorval för de utsagor som klarar filtret ovan
# (ADR 0016 beslutspunkt 4). Bedömningen är gjord 2026-09-13, alltså före periodens slut,
# och den binder den som prövar posterna efter brytpunkten. Den är inte gjord av pilotens
# blindade kodare, eftersom framåthalvan lämnade instrumentet i beslutspunkt 4.
FORHANDSREGISTRERING = {
    "M-108": {
        "storhet": "antal brott som utreds",
        "period": "nästa mandatperiod, 2026-10 till 2030-09",
        "provade_indikatorer": ["uppklaringsgrad", "handlaggningstid"],
        "utfall": "ingen_kompatibel_indikator",
        "skal": (
            "Utsagan räknar ANTAL utredda brott. uppklaringsgrad mäter ANDELEN uppklarade "
            "brott, och de två är skilda storheter: antalet kan stiga medan andelen faller, "
            "om anmälda brott stiger snabbare. Kodboken avsnitt 7.1 ger då ingen relation. "
            "Ledet om att livsstilskriminella sitter inne längre rör strafftid, och ingen "
            "av de 68 indikatorerna mäter den."
        ),
    },
    "M-117": {
        "storhet": "antal brott som utreds och leder till lagföring",
        "period": "nästa mandatperiod, 2026-10 till 2030-09",
        "provade_indikatorer": ["uppklaringsgrad", "handlaggningstid"],
        "utfall": "ingen_kompatibel_indikator",
        "skal": (
            "Samma skäl som M-108. Lagföringsledet ligger nära uppklaringsgradens "
            "personuppklaring, men utsagans storhet är antalet och indikatorns är andelen."
        ),
    },
}


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
                "# både en storhet och en period. Storhetsprovet följer kodbokens avsnitt 4 punkt",
                "# 3, som godtar en riktning utan tal. Filtret ligger i",
                "# pipeline/tools/verklighetsbild.py:forhandsregistrerbara och går att köra om.",
                "#",
                f"# {len(kandidater)} av de 1 073 posterna klarar filtret. Båda bedömdes 2026-09-13,",
                "# alltså före periodens slut, och bedömningen binder den som prövar dem efter",
                "# brytpunkten. Ingen av dem gav ett registrerat indikatorval: båda faller på att",
                "# utsagans storhet är ett ANTAL och indikatorns en ANDEL (kodboken avsnitt 7.1).",
                "#",
                "# Att så få klarar filtret är ett fynd om korpusens FORM och inte om partiernas",
                "# löften. Posten är rubriken, inte den fulla texten ur PDF:en. Noll poster bär ett",
                "# årtal och 22 bär över huvud taget en siffra. Ska framåthalvan någonsin prövas",
                "# måste posterna bära den fulla lydelsen.",
                "forhandsregistrering:",]
    + [
        rad
        for u in kandidater
        for rad in (
            f"  - utsaga_id: {u.id}",
            f"    storhet: {_citat(FORHANDSREGISTRERING[u.id]['storhet'])}",
            f"    period: {_citat(FORHANDSREGISTRERING[u.id]['period'])}",
            "    provade_indikatorer: ["
            + ", ".join(FORHANDSREGISTRERING[u.id]["provade_indikatorer"])
            + "]",
            f"    utfall: {FORHANDSREGISTRERING[u.id]['utfall']}",
            f"    skal: {_citat(FORHANDSREGISTRERING[u.id]['skal'])}",
        )
    ]
    + [
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
    p.add_argument("--kodning", nargs=2, metavar=("KODARE", "KATALOG"), help="normalisera råsvaren")
    p.add_argument("--resultat", action="store_true", help="räkna utbyte, alfa och tröskelprövning")
    args = p.parse_args(argv)
    if args.kodning:
        kodare, katalog = args.kodning
        kallfiler = sorted(Path(katalog).glob("raw_*"))
        if not kallfiler:
            raise SystemExit(f"inga råsvar i {katalog}")
        ut, fel, anmarkningar = skriv_kodning(kallfiler, kodare, UTKATALOG / _kodningsfil(kodare))
        print(f"skrev {ut}")
        print(f"fel: {len(fel)}, anmärkningar: {len(anmarkningar)}")
        for rad in fel:
            print(f"  FEL {rad}")
        for rad in anmarkningar:
            print(f"  anm {rad}")
    if args.resultat:
        kodningar: dict[str, dict[str, KodadUtsaga]] = {}
        for kodare in KODARE:
            fil = UTKATALOG / _kodningsfil(kodare)
            if fil.exists():
                kodningar[kodare] = las_kodning([fil])
        saknade = {"A", "B"} - set(kodningar)
        if saknade:
            raise SystemExit(f"kodning saknas: {', '.join(sorted(saknade))}")
        resultat = rakna_resultat(
            kodningar["A"],
            kodningar["B"],
            {k: v for k, v in kodningar.items() if k.endswith("-prim")},
        )
        ut = UTKATALOG / "resultat.yaml"
        ut.write_text(
            "# Rösta - Verklighetsbildpilotens resultat (biljett #46 steg 6).\n"
            "#\n"
            "# Räkningen ligger i pipeline/tools/verklighetsbild.py och går att köra om.\n"
            "# Ingen sammanjämkning har skett: de två kodningarna står som de är.\n"
            "# Inget tal här inne är en sanningsandel. Piloten kodar ingen sanning alls.\n\n"
            + yaml.safe_dump(resultat, allow_unicode=True, sort_keys=False, default_flow_style=False),
            encoding="utf-8",
        )
        print(f"skrev {ut}")
        print(json.dumps(resultat["utfall"], ensure_ascii=False))
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
