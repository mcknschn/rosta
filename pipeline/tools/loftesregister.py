"""Löftesregistret: underlaget, differensen och låsningen (biljett #54).

Spåret drar om registret ur valmanifestens PDF:er, med full lydelse och sidnummer
(beslut 5 i `loften/docs/beslut/2026-09-16-sparets-form.md`). Posten följer dokumentets
egen struktur (beslut 3), och kompletthet beläggs med två blinda genomgångar (beslut 7).

Verktyget gör fyra saker, och bara de fyra:

1. **Underlaget.** Läser en PDF och skriver ett radnumrerat textunderlag, en rad per
   textrad i dokumentet, med sidnummer, blockgräns och listmarkör. Utvinningen är
   deterministisk: samma PDF ger samma underlag, tecken för tecken. Underlaget är det
   de två genomgångarna läser.
2. **Kontrollen.** Prövar en genomgång mot underlaget: att varje radspann finns, att
   inga spann överlappar, och vilka rader ingen post tog.
3. **Differensen.** Jämför två genomgångar och räknar de tre tal beslut 7 kräver:
   poster bara A har, poster bara B har, och poster båda har men styckat olika.
4. **Registret.** Bygger den låsta filen ur underlaget och det avgjorda facit, och
   hashar den med normaliserade radslut.

En genomgång pekar ut poster som **radspann i underlaget**, aldrig som avskriven text.
Skälet är att lydelsen då inte kan glida: den kommer ur PDF:en och inte ur en kodares
tangentbord. Det gör också differenstalet till vad beslut 7 vill mäta, alltså var två
genomgångar drar postens gräns, och inte hur olika de stavar samma mening.

Kör manuellt (kräver PyMuPDF, ingen pipeline-dependens):

    python -m pipeline.tools.loftesregister --underlag
    python -m pipeline.tools.loftesregister --kontroll
    python -m pipeline.tools.loftesregister --differens
    python -m pipeline.tools.loftesregister --bygg
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
import unicodedata
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path

import yaml

ROT = Path(__file__).resolve().parents[2]
PDF_KATALOG = ROT / "loften" / "docs" / "valmanifest_2022"
HAMTMANIFEST = PDF_KATALOG / "hamtmanifest.yaml"
UNDERLAG = ROT / "loften" / "underlag" / "valmanifest_2022"
KONFIG = ROT / "loften" / "config" / "loftesregister_2022"

# Kolumnrännan i ett valmanifest är smal. Radavståndet inom en spalt är smalare.
# Tröskeln skiljer de två, och en lodrät delning provas före en vågrät, så att en
# tillfällig lucka mellan två punkter i samma spalt aldrig fogar ihop två spalter.
#
# Talet är mätt och inte valt. M sätter sina spalter med 8,9 till 12,2 punkters ränna,
# och de sju andra dokumenten sätts i en spalt eller med en ränna på 50 punkter och mer.
# Utfallet är identiskt för varje tröskel mellan 7,0 och 10,0, och 8,5 ligger mitt på den
# platån. Vid 12,0 och uppåt flätas M:s spalter ihop: sidan läses vänster, höger, vänster,
# och ett stycke som löper över spaltbytet får sin andra halva före sin första.
RANNA_MIN = 8.5
# Den vågräta delningen bevarar alltid ordningen, eftersom den skiljer band uppifrån och
# ned. Den behöver därför ingen bred lucka för att vara säker, och tröskeln är låg med
# flit. Dess uppgift är att skilja av ett band som korsar rännan, typiskt en rubrik över
# båda spalterna, så att spalterna därunder kan delas lodrätt. KD sätter luckan under en
# sådan rubrik till 0,2 punkter. Utfallet är identiskt för varje tröskel mellan 0,01 och
# 0,2, och vid 0,3 och uppåt faller KD:s sida 2 igenom till en sortering på y som läser
# vänster, höger, höger, vänster.
BAND_MIN = 0.1


# ------------------------------------------------------------------------ hämtmanifest


def hamtmanifest() -> dict:
    return yaml.safe_load(HAMTMANIFEST.read_text(encoding="utf-8"))


def dokument() -> list[dict]:
    return hamtmanifest()["dokument"]


def sha256_fil(fil: Path) -> str:
    digest = hashlib.sha256()
    with fil.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256_rader(text: str) -> str:
    """SHA-256 med normaliserade radslut.

    Samma skäl som i `pipeline/tools/samstammighet.py`: en utcheckning på Windows ger
    CRLF där git bär LF, och utan normaliseringen skulle hashen säga att filen ändrats
    så fort någon checkat ut repot på ett annat operativsystem.
    """
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_text(fil: Path) -> str:
    return sha256_rader(fil.read_text(encoding="utf-8"))


def pdf_stammer(post: dict) -> bool:
    """Är PDF:en på disk den som hämtmanifestet pinnar?"""
    fil = PDF_KATALOG / post["filnamn"]
    return fil.is_file() and sha256_fil(fil) == post["sha256"]


# ------------------------------------------------------------------------ textstädning

LIGATURER = {
    "ﬀ": "ff",
    "ﬁ": "fi",
    "ﬂ": "fl",
    "ﬃ": "ffi",
    "ﬄ": "ffl",
    "ﬅ": "st",
    "ﬆ": "st",
}

# Elliptiska sammansättningar: `vålds- och sexualbrott`. Bindestrecket är partiets,
# inte satsens, och raden ska aldrig fogas ihop med nästa.
ELLIPS = {"och", "eller", "samt"}

# Listmarkören som PDF-satsen sätter framför en punkt. Tecknet är ingen del av partiets
# mening, men VAR det står är ett faktum om dokumentets egen styckning, och beslut 3
# säger att posten ska följa den. Därför skiljs markören från texten och bärs vidare som
# en egen flagga i stället för att tas bort.
#
# Markören kan vara flera tecken med mellanrum emellan. S sätter sin punkt som en
# Wingdings-glyf (U+F0B7), ett tabbsteg, ett mellanslag och ett BEL innan första
# bokstaven. Samma BEL följde med i 2026 års korpus, där det står kvar mitt i en lydelse.
PUNKTGLYF = re.compile("^(?:[\\s]*[•●▪■‣⁃·])+[\\s]*")

# Hårt mellanslag är ett mellanslag. Inget annat tecken tas bort ur partiets text.
SKRAP = {" ": " "}


def stada(text: str) -> str:
    """Tecken som PDF-satsen lade till, bort. Partiets stavning, kvar."""
    for tecken, ersattning in LIGATURER.items():
        text = text.replace(tecken, ersattning)
    for tecken, ersattning in SKRAP.items():
        text = text.replace(tecken, ersattning)
    text = text.replace("–", "-").replace("—", "-")
    text = text.replace("’", "'").replace("‘", "'")
    return "".join(t for t in text if unicodedata.category(t) != "Cc" or t in "\n")


def dela_markor(rad: str) -> tuple[bool, str]:
    """(bär raden en listmarkör, raden utan den)."""
    utan = PUNKTGLYF.sub("", rad)
    return utan != rad, utan


def markerade_rader(rader: Iterable[str]) -> list[tuple[bool, str]]:
    """Textraderna med sin listmarkör, där en markör på egen rad bärs vidare.

    C sätter sina punkter så att glyfen står ensam på en rad och texten börjar på nästa.
    Raden blir tom när markören skilts av, och utan det här steget föll flaggan bort med
    den. C har 96 sådana punkter, alltså hela dokumentets liststruktur.
    """
    ut: list[tuple[bool, str]] = []
    hangande = False
    for rad in rader:
        markor, text = dela_markor(rad)
        if not platta(text):
            hangande = hangande or markor
            continue
        ut.append((markor or hangande, text))
        hangande = False
    return ut


def foga_avstavning(rader: Sequence[tuple[bool, str]]) -> list[tuple[bool, str]]:
    """Fogar ihop ord som satsen bröt över ett radslut.

    Två fall fogas: ett mjukt bindestreck (U+00AD), som satsen själv satte dit, och ett
    vanligt bindestreck följt av en rad som börjar med gemen. Det andra fallet undantar
    `och`, `eller` och `samt`, eftersom `vålds- och sexualbrott` bär partiets eget
    bindestreck och inte satsens.

    En rad med listmarkör fogas aldrig in i raden före. Markören säger att en ny punkt
    börjar, och den gränsen väger tyngre än ett bindestreck i slutet av raden före.
    """
    resultat: list[tuple[bool, str]] = []
    i = 0
    while i < len(rader):
        markor, rad = rader[i]
        rad = rad.rstrip()
        while i + 1 < len(rader):
            nasta_markor, nasta = rader[i + 1]
            nasta = nasta.strip()
            if not nasta or nasta_markor:
                break
            if rad.endswith("­"):
                rad = rad[:-1] + nasta
            elif rad.endswith("-") and nasta[:1].islower() and nasta.split()[0] not in ELLIPS:
                rad = rad[:-1] + nasta
            else:
                break
            i += 1
        resultat.append((markor, rad.replace("­", "")))
        i += 1
    return resultat


def platta(text: str) -> str:
    """En rad med enkla mellanslag. Det är formen en post bär i registret."""
    return re.sub(r"\s+", " ", text).strip()


# ------------------------------------------------------------------------ sidutvinning


@dataclass(frozen=True)
class Rad:
    nr: int
    sida: int
    text: str
    block: int
    markor: bool


def _snitt(rutor: Sequence[tuple], lo: int, hi: int, minsta: float) -> tuple[list, list] | None:
    """Delar rutorna i två vid den bredaste luckan, om den är bred nog."""
    tackning: list[list[float]] = []
    for r in sorted(rutor, key=lambda r: r[lo]):
        if tackning and r[lo] <= tackning[-1][1]:
            tackning[-1][1] = max(tackning[-1][1], r[hi])
        else:
            tackning.append([r[lo], r[hi]])
    if len(tackning) < 2:
        return None
    bredd, kant = max((b[0] - a[1], a[1]) for a, b in zip(tackning, tackning[1:], strict=False))
    if bredd < minsta:
        return None
    return [r for r in rutor if r[lo] <= kant], [r for r in rutor if r[lo] > kant]


def xy_snitt(rutor: Sequence[tuple]) -> list[tuple]:
    """Läsordning ur ett spaltsatt uppslag, med rekursivt XY-snitt.

    Snittet läggs vid den **bredaste** luckan, och en lodrät lucka provas före en vågrät.
    Det är skillnaden mot att sortera på y. En rubrik över båda spalterna hindrar den
    lodräta delningen, så bandet med rubriken skiljs av först och spalterna delas
    därefter. Sorterar man bara på y flätas spalterna ihop, rad för rad.

    Bara ett snitt läggs per varv. Delas alla luckor på en gång kan två punkter i olika
    spalter som råkar ligga i höjd med varandra dela sidan på tvären, och då flätas
    spalterna ihop igen.
    """
    if len(rutor) <= 1:
        return list(rutor)
    for axel, minsta in ((0, RANNA_MIN), (1, BAND_MIN)):
        delar = _snitt(rutor, axel, axel + 2, minsta)
        if delar and all(delar):
            return xy_snitt(delar[0]) + xy_snitt(delar[1])
    return sorted(rutor, key=lambda r: (r[1], r[0]))


def sidrader(pdf: Path) -> list[Rad]:
    """Dokumentets textrader i läsordning, numrerade löpande över hela dokumentet."""
    import fitz  # lokal import: PyMuPDF är inget pipeline-beroende

    rader: list[Rad] = []
    nr = 0
    blocknr = 0
    with fitz.open(pdf) as doc:
        for sidnr, sida in enumerate(doc, start=1):
            block = [b for b in sida.get_text("blocks") if b[6] == 0 and b[4].strip()]
            for ruta in xy_snitt(block):
                blocknr += 1
                rena = markerade_rader(stada(ruta[4]).split("\n"))
                for markor, text in foga_avstavning(rena):
                    text = platta(text)
                    if not text:
                        continue
                    nr += 1
                    rader.append(
                        Rad(nr=nr, sida=sidnr, text=text, block=blocknr, markor=markor)
                    )
    return rader


HUVUD = """\
# Underlag för löftesregistret 2022 (biljett #54). Utvunnet ur PDF:en med
# pipeline/tools/loftesregister.py, aldrig skrivet för hand.
#
# Format per textrad: radnummer | sidnummer | markör | text
#   markör `*`  raden inleds med en listmarkör i PDF:en, alltså en ny punkt
#   markör `.`  raden gör det inte
#
# En rad som börjar med # är satsens form och inte partiets text:
#   ---- sida N ----   sidbrytning i PDF:en
#   ---- block ----    nytt textblock i PDF:en, alltså dokumentets egen styckning
#
# Avstavning över radslut är hopfogad. Bindestreck i sammansättningar står kvar.
# Tankstreck är ersatta med bindestreck. Partiets egna stavfel står kvar.
"""


def underlagstext(rader: Iterable[Rad]) -> str:
    ut = HUVUD.rstrip("\n").split("\n") + [""]
    forra_sida = None
    forra_block = None
    for rad in rader:
        if rad.sida != forra_sida:
            ut.append(f"# ---- sida {rad.sida} ----")
            forra_sida, forra_block = rad.sida, None
        if rad.block != forra_block:
            if forra_block is not None:
                ut.append("")
            ut.append("# ---- block ----")
            forra_block = rad.block
        ut.append(f"{rad.nr}|{rad.sida}|{'*' if rad.markor else '.'}|{rad.text}")
    return "\n".join(ut) + "\n"


def las_underlag(fil: Path) -> list[Rad]:
    rader = []
    blocknr = 0
    for rad in fil.read_text(encoding="utf-8").splitlines():
        if rad.startswith("# ---- block ----"):
            blocknr += 1
            continue
        if not rad or rad.startswith("#"):
            continue
        nr, sida, markor, text = rad.split("|", 3)
        rader.append(
            Rad(nr=int(nr), sida=int(sida), text=text, block=blocknr, markor=markor == "*")
        )
    return rader


def underlagsfil(dok_id: str) -> Path:
    return UNDERLAG / f"{dok_id.lower()}.txt"


def alla_underlag() -> dict[str, dict[int, Rad]]:
    return {
        post["id"]: {r.nr: r for r in las_underlag(underlagsfil(post["id"]))}
        for post in dokument()
    }


def skriv_underlag() -> list[tuple[str, int, int]]:
    """Skriver ett underlag per dokument. Returnerar (id, antal rader, antal sidor)."""
    UNDERLAG.mkdir(parents=True, exist_ok=True)
    ut = []
    for post in dokument():
        if not pdf_stammer(post):
            raise SystemExit(f"{post['filnamn']}: saknas eller stämmer inte mot hämtmanifestet")
        rader = sidrader(PDF_KATALOG / post["filnamn"])
        underlagsfil(post["id"]).write_text(
            underlagstext(rader), encoding="utf-8", newline="\n"
        )
        ut.append((post["id"], len(rader), rader[-1].sida if rader else 0))
    return ut


# ------------------------------------------------------------------------ genomgångar


@dataclass(frozen=True)
class Post:
    id: str
    dokument: str
    spann: tuple[tuple[int, int], ...]

    @property
    def rad_start(self) -> int:
        return self.spann[0][0]

    @property
    def rad_slut(self) -> int:
        return self.spann[-1][1]

    @property
    def rader(self) -> list[int]:
        """Raderna posten tar, i ordning.

        En post kan bestå av flera spann. Skälet är sidbrytningen: en punkt som börjar
        på sidan 4 och slutar på sidan 5 avbryts i underlaget av sidnumret och sidhuvudet,
        och de raderna är inte partiets löfte. Posten hoppar då över dem.
        """
        return [n for lo, hi in self.spann for n in range(lo, hi + 1)]


def tolka_spann(text: str) -> tuple[tuple[int, int], ...]:
    """`85-86,89-92` blir ((85, 86), (89, 92)). Ett ensamt tal blir ett spann om en rad."""
    spann = []
    for del_ in str(text).split(","):
        del_ = del_.strip()
        if not del_:
            continue
        if "-" in del_:
            lo, hi = del_.split("-", 1)
            spann.append((int(lo), int(hi)))
        else:
            spann.append((int(del_), int(del_)))
    if not spann:
        raise ValueError(f"tomt radspann: {text!r}")
    return tuple(spann)


def skriv_spann(spann: Sequence[tuple[int, int]]) -> str:
    return ",".join(f"{lo}-{hi}" if lo != hi else str(lo) for lo, hi in spann)


def las_genomgang(fil: Path) -> dict[str, list[Post]]:
    """Genomgången per dokument. Varje post är ett eller flera radspann i underlaget.

    Genomgången numrerar inga poster. Id:t sätts här, ur postens plats i dokumentet, så
    att två genomgångar aldrig kan skilja sig på hur de räknade.
    """
    data = yaml.safe_load(fil.read_text(encoding="utf-8"))
    ut: dict[str, list[Post]] = {}
    for dok, poster in (data.get("poster") or {}).items():
        ordnade = sorted((tolka_spann(p) for p in poster), key=lambda s: s[0])
        ut[dok] = [
            Post(id=f"{dok}-{i:03d}", dokument=dok, spann=s)
            for i, s in enumerate(ordnade, start=1)
        ]
    return ut


def lydelse(rader: dict[int, Rad], post: Post) -> str:
    """Postens fulla lydelse, hopfogad ur underlagets rader.

    Avstavningen fogas också HÄR, och inte bara inom ett block. En punkt som bryts av en
    sidbrytning har sin första halva i ett block och sin andra i ett annat, och ordet som
    bröts över brytningen skulle annars stå kvar som `gäng- relaterad`.
    """
    bitar = [(rader[n].markor, rader[n].text) for n in post.rader if n in rader]
    return platta(" ".join(text for _, text in foga_avstavning(bitar)))


def sidnummer(rader: dict[int, Rad], post: Post) -> int:
    return rader[post.rad_start].sida


def kontrollera_spann(rader: dict[int, Rad], poster: Sequence[Post]) -> list[str]:
    """Fel som gör en genomgång obrukbar.

    Tre slag: ett spann som pekar utanför underlaget, ett spann som vänder på sig, och
    två poster som tar samma rad. Det sista är det som gör talen i beslut 7 odefinierade,
    eftersom en rad då hör till två poster på en gång.
    """
    fel = []
    tagna: dict[int, str] = {}
    for post in poster:
        for lo, hi in post.spann:
            if hi < lo:
                fel.append(f"{post.id}: spannet {lo}-{hi} vänder på sig")
        if len(set(post.rader)) != len(post.rader):
            fel.append(f"{post.id}: postens egna spann överlappar varandra")
            continue
        krock = False
        for n in post.rader:
            if n not in rader:
                fel.append(f"{post.id}: rad {n} finns inte i underlaget")
                krock = True
                break
            if n in tagna:
                fel.append(f"{post.id}: rad {n} är redan tagen av {tagna[n]}")
                krock = True
                break
        if not krock:
            for n in post.rader:
                tagna[n] = post.id
    return fel


def otagna_rader(rader: dict[int, Rad], poster: Sequence[Post]) -> list[int]:
    """Rader som ingen post tog. Talet fångar en genomgång som slutade halvvägs."""
    tagna = {n for post in poster for n in post.rader}
    return sorted(n for n in rader if n not in tagna)


# ------------------------------------------------------------------------ differensen


@dataclass(frozen=True)
class Differens:
    bara_a: list[Post]
    bara_b: list[Post]
    styckat_olika: list[tuple[Post, Post]]
    delade: int

    @property
    def tal(self) -> tuple[int, int, int]:
        return len(self.bara_a), len(self.bara_b), len(self.styckat_olika)


def differens(a: Sequence[Post], b: Sequence[Post]) -> Differens:
    """De tre tal beslut 7 kräver, räknade på radspann.

    Ordningen är bestämd. Först parar identiska spann ihop sig, och de är `delade`.
    Sedan paras de som överlappar men inte stämmer, störst överlapp först, och de är
    `styckat olika`. Ett spann i A får som mest en partner i B, och det som blir kvar är
    `bara A` eller `bara B`.
    """
    kvar_a = {p.id: p for p in a}
    kvar_b = {p.id: p for p in b}
    delade = 0
    nyckel_b: dict[tuple[tuple[int, int], ...], list[str]] = {}
    for p in b:
        nyckel_b.setdefault(p.spann, []).append(p.id)
    for pa in sorted(a, key=lambda p: p.rad_start):
        koen = nyckel_b.get(pa.spann)
        if koen:
            kvar_b.pop(koen.pop(0), None)
            kvar_a.pop(pa.id, None)
            delade += 1
    par: list[tuple[int, Post, Post]] = []
    for pa in kvar_a.values():
        for pb in kvar_b.values():
            gemensam = len(set(pa.rader) & set(pb.rader))
            if gemensam:
                par.append((gemensam, pa, pb))
    olika: list[tuple[Post, Post]] = []
    for _, pa, pb in sorted(par, key=lambda t: (-t[0], t[1].rad_start)):
        if pa.id in kvar_a and pb.id in kvar_b:
            olika.append((pa, pb))
            kvar_a.pop(pa.id)
            kvar_b.pop(pb.id)
    return Differens(
        bara_a=sorted(kvar_a.values(), key=lambda p: p.rad_start),
        bara_b=sorted(kvar_b.values(), key=lambda p: p.rad_start),
        styckat_olika=sorted(olika, key=lambda t: t[0].rad_start),
        delade=delade,
    )


def differensrapport(
    genomgang_a: dict[str, list[Post]],
    genomgang_b: dict[str, list[Post]],
    underlag: dict[str, dict[int, Rad]],
) -> dict:
    """Differensen per dokument, i den form `differens.yaml` bär den."""
    ut: dict = {"dokument": {}, "summa": {"bara_a": 0, "bara_b": 0, "styckat_olika": 0}}
    ordning = [d["id"] for d in dokument()]
    for dok in sorted(set(genomgang_a) | set(genomgang_b), key=ordning.index):
        rader = underlag[dok]
        d = differens(genomgang_a.get(dok, []), genomgang_b.get(dok, []))
        bara_a, bara_b, olika = d.tal
        fall = [
            {
                "slag": "bara_a",
                "sida": sidnummer(rader, p),
                "a_rader": skriv_spann(p.spann),
                "b_rader": None,
                "a": lydelse(rader, p),
                "b": None,
            }
            for p in d.bara_a
        ]
        fall += [
            {
                "slag": "bara_b",
                "sida": sidnummer(rader, p),
                "a_rader": None,
                "b_rader": skriv_spann(p.spann),
                "a": None,
                "b": lydelse(rader, p),
            }
            for p in d.bara_b
        ]
        fall += [
            {
                "slag": "styckat_olika",
                "sida": sidnummer(rader, pa),
                "a_rader": skriv_spann(pa.spann),
                "b_rader": skriv_spann(pb.spann),
                "a": lydelse(rader, pa),
                "b": lydelse(rader, pb),
            }
            for pa, pb in d.styckat_olika
        ]
        ut["dokument"][dok] = {
            "poster_a": len(genomgang_a.get(dok, [])),
            "poster_b": len(genomgang_b.get(dok, [])),
            "delade": d.delade,
            "bara_a": bara_a,
            "bara_b": bara_b,
            "styckat_olika": olika,
            "fall": sorted(
                fall, key=lambda f: tolka_spann(f["a_rader"] or f["b_rader"])[0]
            ),
        }
        ut["summa"]["bara_a"] += bara_a
        ut["summa"]["bara_b"] += bara_b
        ut["summa"]["styckat_olika"] += olika
    return ut


# ------------------------------------------------------------------------ registret


def _citat(text: str) -> str:
    """YAML-sträng i dubbla citattecken, med lydelsen bevarad tecken för tecken.

    Styrtecken skyddas som `\\xNN` i stället för att tas bort, av samma skäl som i
    `pipeline/tools/verklighetsbild.py`: registret ska bära dokumentets lydelse och inte
    en städad version av den.
    """
    ut = []
    for tecken in text:
        if tecken == "\\":
            ut.append("\\\\")
        elif tecken == '"':
            ut.append('\\"')
        elif unicodedata.category(tecken) in ("Cc", "Cf"):
            # YAML:s `\xNN` bär bara två siffror. Ett osynligt tecken över U+00FF måste
            # skrivas `\uNNNN`, annars läses `\x200b` tillbaka som ett blanksteg och en
            # nolla, och lydelsen är tyst förvanskad.
            ut.append(f"\\x{ord(tecken):02x}" if ord(tecken) <= 0xFF else f"\\u{ord(tecken):04x}")
        else:
            ut.append(tecken)
    return '"' + "".join(ut) + '"'


# Vad projektägaren kan svara på en differens.
#   a      A:s styckning gäller
#   b      B:s styckning gäller
#   ingen  fallet är ingen post, och faller ur registret
# Vilket annat värde som helst läses som ett radspann, alltså projektägarens egen
# gräns: `93-99`, eller `93-95,98-99` över en sidbrytning.
BESLUT = ("a", "b", "ingen")


def facit(
    differens: dict, a: dict[str, list[Post]], b: dict[str, list[Post]]
) -> dict[str, list[Post]]:
    """Posterna som registret ska bära, efter projektägarens avgörande.

    Utgångspunkten är det de två genomgångarna redan är eniga om. Varje differens
    avgörs av ett `beslut` i `differens.yaml`, och ett oavgjort fall stoppar bygget.
    Beslut 7 kräver att varje differens är avgjord innan låsningen, och en tyst förvald
    sida vore ett avgörande utan avgörare.
    """
    valda = {
        dok: sorted({p.spann for p in a.get(dok, [])} & {p.spann for p in b.get(dok, [])})
        for dok in sorted(set(a) | set(b))
    }
    oavgjort = []
    for dok, tal in differens["dokument"].items():
        for fall in tal["fall"]:
            beslut = fall.get("beslut")
            plats = f"{dok} sida {fall['sida']} ({fall['slag']})"
            if beslut in (None, ""):
                oavgjort.append(plats)
            elif beslut == "ingen":
                continue
            elif beslut in ("a", "b"):
                spann = fall[f"{beslut}_rader"]
                if spann is None:
                    oavgjort.append(f"{plats}: genomgång {beslut.upper()} har ingen post här")
                else:
                    valda[dok].append(tolka_spann(spann))
            else:
                try:
                    valda[dok].append(tolka_spann(str(beslut)))
                except ValueError:
                    oavgjort.append(
                        f"{plats}: `{beslut}` är varken {', '.join(BESLUT)} eller ett radspann"
                    )
    if oavgjort:
        raise SystemExit(
            "differensen är inte avgjord, och registret låses inte förrän den är det:\n  "
            + "\n  ".join(oavgjort)
        )
    return {
        dok: [
            Post(id=f"{dok}-{i:03d}", dokument=dok, spann=s)
            for i, s in enumerate(sorted(set(spann)), start=1)
        ]
        for dok, spann in valda.items()
    }


def registertext(poster: dict[str, list[Post]], underlag: dict[str, dict[int, Rad]], datum: str) -> str:
    """Registret som YAML, skrivet rad för rad så att lydelsen aldrig formas om."""
    manifest = {d["id"]: d for d in dokument()}
    antal = sum(len(p) for p in poster.values())
    rader = [
        "# Rösta - LÖFTESREGISTRET 2022 (biljett #54, beslut 5, 7 och 8).",
        "#",
        "# En rad per löfte, med full lydelse och sidnummer, draget ur partiets egen PDF.",
        "# Posten följer dokumentets egen struktur (beslut 3). Registret bär INGET",
        "# kategorifält (beslut 11), och fälten för prövbarhet och instrument fylls i av",
        "# senare biljetter.",
        "#",
        "# LÅSNINGEN BINDER (beslut 8). Lydelsen ändras aldrig. Enda öppningen är en",
        "# errata-rad för ett avskrivningsfel som går att belägga mot PDF:en. `innehall_sha256`",
        "# är filens egen hash, räknad utan just den raden, och tests/test_loftesregister_2022.py",
        "# faller på en ändrad bokstav.",
        "#",
        "# `rader` pekar in i underlaget under loften/underlag/valmanifest_2022/, som är",
        "# deterministiskt utvunnet ur PDF:en. Flera spann betyder att punkten bröts av en",
        "# sidbrytning, och att sidnumret däremellan inte hör till löftet.",
        "",
        "version: 1",
        f"byggt: {datum}",
        "hamtmanifest: '../../docs/valmanifest_2022/hamtmanifest.yaml'",
        "instruktion: '../../docs/loftesregister_2022/genomgangsinstruktion.md'",
        f"antal: {antal}",
        "",
        "dokument:",
    ]
    for dok in sorted(poster, key=lambda d: [x["id"] for x in dokument()].index(d)):
        fil = underlagsfil(dok)
        rader += [
            f"  {dok}:",
            f"    antal: {len(poster[dok])}",
            f"    sidor: {manifest[dok]['sidor']}",
            f"    pdf_sha256: {manifest[dok]['sha256']}",
            f"    underlag_sha256: {sha256_text(fil)}",
        ]
    rader += ["", "poster:"]
    for dok in sorted(poster, key=lambda d: [x["id"] for x in dokument()].index(d)):
        for post in poster[dok]:
            rader += [
                f"  - id: {post.id}",
                f"    parti: {dok}",
                f"    sida: {sidnummer(underlag[dok], post)}",
                f"    rader: '{skriv_spann(post.spann)}'",
                f"    lydelse: {_citat(lydelse(underlag[dok], post))}",
            ]
    rader += ["", "errata: []", ""]
    text = "\n".join(rader)
    return text + f"innehall_sha256: {sha256_rader(text)}\n"


# ------------------------------------------------------------------------ CLI


def _las_genomgangar() -> tuple[dict[str, list[Post]], dict[str, list[Post]]]:
    return (
        las_genomgang(KONFIG / "genomgang_a.yaml"),
        las_genomgang(KONFIG / "genomgang_b.yaml"),
    )


def _kommando_underlag() -> int:
    for dok_id, antal, sidor in skriv_underlag():
        print(f"{dok_id:3s} {antal:5d} rader {sidor:3d} sidor")
    return 0


def _kommando_kontroll() -> int:
    underlag = alla_underlag()
    trasigt = 0
    for namn, genomgang in zip("AB", _las_genomgangar(), strict=True):
        for dok, poster in sorted(genomgang.items()):
            rader = underlag[dok]
            fel = kontrollera_spann(rader, poster)
            otagna = otagna_rader(rader, poster)
            trasigt += len(fel)
            print(
                f"{namn} {dok:3s} poster={len(poster):4d} fel={len(fel):3d} "
                f"otagna rader={len(otagna):5d} av {len(rader)}"
            )
            for rad in fel[:10]:
                print(f"      {rad}")
    return 1 if trasigt else 0


def _kommando_differens(skriv: bool) -> int:
    a, b = _las_genomgangar()
    rapport = differensrapport(a, b, alla_underlag())
    for dok, tal in rapport["dokument"].items():
        print(
            f"{dok:3s} A={tal['poster_a']:4d} B={tal['poster_b']:4d} "
            f"delade={tal['delade']:4d} baraA={tal['bara_a']:3d} "
            f"baraB={tal['bara_b']:3d} styckat={tal['styckat_olika']:3d}"
        )
    print("summa:", rapport["summa"])
    if skriv:
        fil = KONFIG / "differens.yaml"
        # Projektägarens avgöranden överlever en omräkning. Både beslutet och skälet
        # bärs över, eftersom skälet är spåret av avgörandet och inte en anteckning.
        tidigare = {}
        if fil.is_file():
            gammal = yaml.safe_load(fil.read_text(encoding="utf-8")) or {}
            for dok, tal in (gammal.get("dokument") or {}).items():
                for fall in tal.get("fall") or []:
                    nyckel = (dok, fall["slag"], fall["a_rader"], fall["b_rader"])
                    tidigare[nyckel] = (fall.get("beslut"), fall.get("skal"))
        for dok, tal in rapport["dokument"].items():
            for fall in tal["fall"]:
                nyckel = (dok, fall["slag"], fall["a_rader"], fall["b_rader"])
                fall["beslut"], fall["skal"] = tidigare.get(nyckel, (None, None))
        fil.write_text(differenstext(rapport), encoding="utf-8", newline="\n")
        print(f"skrev {fil.relative_to(ROT)}")
    return 0


def differenstext(rapport: dict) -> str:
    rader = [
        "# Rösta - DIFFERENSEN mellan de två blinda genomgångarna (biljett #54, beslut 7).",
        "#",
        "# Tre tal per dokument: poster bara A har, poster bara B har, och poster båda har",
        "# men styckat olika. Talen är räknade av pipeline/tools/loftesregister.py på",
        "# radspann i underlaget, aldrig på avskriven text.",
        "#",
        "# PROJEKTÄGAREN AVGÖR VARJE FALL INNAN LÅSNINGEN. Fältet `beslut` tar:",
        "#   a       A:s styckning gäller",
        "#   b       B:s styckning gäller",
        "#   ingen   fallet är ingen post och faller ur registret",
        "#   <spann> projektägarens egen gräns, till exempel 93-99 eller 93-95,98-99",
        "# `skal` är frivilligt och står kvar i filen som spår av avgörandet.",
        "#",
        "# Ett oavgjort fall stoppar bygget. Det är avsiktligt: en tyst förvald sida vore",
        "# ett avgörande utan avgörare.",
        "",
        "version: 1",
        "",
        "summa:",
    ]
    for nyckel, tal in rapport["summa"].items():
        rader.append(f"  {nyckel}: {tal}")
    rader += ["", "dokument:"]
    for dok, tal in rapport["dokument"].items():
        rader += [
            f"  {dok}:",
            f"    poster_a: {tal['poster_a']}",
            f"    poster_b: {tal['poster_b']}",
            f"    delade: {tal['delade']}",
            f"    bara_a: {tal['bara_a']}",
            f"    bara_b: {tal['bara_b']}",
            f"    styckat_olika: {tal['styckat_olika']}",
        ]
        if not tal["fall"]:
            rader.append("    fall: []")
            continue
        rader.append("    fall:")
        for fall in tal["fall"]:
            rader += [
                f"      - slag: {fall['slag']}",
                f"        sida: {fall['sida']}",
                f"        a_rader: {fall['a_rader'] and repr(fall['a_rader']) or 'null'}",
                f"        b_rader: {fall['b_rader'] and repr(fall['b_rader']) or 'null'}",
                f"        a: {_citat(fall['a']) if fall['a'] else 'null'}",
                f"        b: {_citat(fall['b']) if fall['b'] else 'null'}",
                f"        beslut: {fall.get('beslut') and repr(fall['beslut']) or 'null'}",
                f"        skal: {fall.get('skal') and _citat(fall['skal']) or 'null'}",
            ]
    return "\n".join(rader) + "\n"


def _kommando_bygg(datum: str) -> int:
    a, b = _las_genomgangar()
    underlag = alla_underlag()
    differens_data = yaml.safe_load((KONFIG / "differens.yaml").read_text(encoding="utf-8"))
    poster = facit(differens_data, a, b)
    for dok, lista in poster.items():
        fel = kontrollera_spann(underlag[dok], lista)
        if fel:
            raise SystemExit(f"{dok}: facit håller inte ihop\n  " + "\n  ".join(fel))
    fil = KONFIG / "register.yaml"
    fil.write_text(registertext(poster, underlag, datum), encoding="utf-8", newline="\n")
    for dok, lista in poster.items():
        print(f"{dok:3s} {len(lista):4d} poster")
    print(f"summa {sum(len(p) for p in poster.values())}, skrev {fil.relative_to(ROT)}")
    return 0


def _kommando_samla(katalog: Path, mal: Path) -> int:
    """Slår ihop en genomgångs filer per dokument till en fil.

    En genomgång körs ett dokument i taget, i skilda kontexter. Den här funktionen gör
    ingenting annat än att lägga delarna i en fil, i hämtmanifestets ordning.
    """
    rader = [
        "# Genomgång, en post = ett radspann i loften/underlag/valmanifest_2022/.",
        "# Poster numreras inte här. Numret sätts ur postens plats i dokumentet.",
        "",
        "version: 1",
        "poster:",
    ]
    for post in dokument():
        fil = katalog / f"{post['id']}.yaml"
        if not fil.is_file():
            raise SystemExit(f"saknas: {fil}")
        data = yaml.safe_load(fil.read_text(encoding="utf-8"))
        if data.get("dokument") != post["id"]:
            raise SystemExit(f"{fil}: dokumentkoden är {data.get('dokument')!r}")
        rader.append(f"  {post['id']}:")
        for spann in data["poster"]:
            rader.append(f"    - '{skriv_spann(tolka_spann(spann))}'")
    mal.write_text("\n".join(rader) + "\n", encoding="utf-8", newline="\n")
    print(f"skrev {mal}")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--underlag", action="store_true", help="skriv om textunderlaget ur PDF:erna")
    p.add_argument("--samla", nargs=2, metavar=("KATALOG", "MAL"), help="slå ihop en genomgång")
    p.add_argument("--kontroll", action="store_true", help="pröva genomgångarna mot underlaget")
    p.add_argument("--differens", action="store_true", help="räkna de tre talen per dokument")
    p.add_argument("--skriv", action="store_true", help="skriv differens.yaml, behåll besluten")
    p.add_argument("--bygg", metavar="DATUM", help="bygg och lås registret")
    argument = p.parse_args(argv)
    if argument.underlag:
        return _kommando_underlag()
    if argument.samla:
        return _kommando_samla(Path(argument.samla[0]), Path(argument.samla[1]))
    if argument.kontroll:
        return _kommando_kontroll()
    if argument.differens:
        return _kommando_differens(argument.skriv)
    if argument.bygg:
        return _kommando_bygg(argument.bygg)
    p.print_help()
    return 1


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
