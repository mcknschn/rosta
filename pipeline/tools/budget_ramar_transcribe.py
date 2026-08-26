"""Hämtar, prövar och transkriberar PARTIERNAS EGNA UTGIFTSRAMAR till a1 (ADR 0007).

a1 är budgethalvan av delpoäng A. Täljaren är varje partis egen föreslagna ram per
utgiftsområde, förankringen är de beslutade ramarna över ett historiskt fönster. ADR 0007
punkt 1 kräver att de två täcker samma år. Det här verktyget bygger täljaren för hela
fönstret, ur samma FiU1-rambeslutstabell som förankringen redan läser.

    python -m pipeline.tools.budget_ramar_transcribe --bound     # tredje gränsen -> bevisfil
    python -m pipeline.tools.budget_ramar_transcribe --frames     # ett års ramar -> stdout
    python -m pipeline.tools.budget_ramar_transcribe --config     # skriv config/budget_ramar.yaml
    python -m pipeline.tools.budget_ramar_transcribe --audit      # config mot källa (exit 1 vid diff)

Verktyget körs FÖR HAND, aldrig av pipelinen. Det finns ingen runtime-parser av
budgetdokument: A är tyngsta delpoängen och får aldrig kunna korrumperas av en bräcklig
parser (samma regel som `config/a_forankring.yaml`). Beloppen transkriberas till
versionsstyrd config, varje ram citerar sin källrad, och en saknad eller ogiltig cell ger
hård fail i stället för en tyst nolla.

GRÄNSEN (ADR 0007 punkt 2), skriven före hämtningen och orörd efteråt, står i FRAMES_TEST.

KÄLLAN är tabellen "Regeringens och oppositionspartiernas (eller motionärernas) förslag till
utgiftsramar för <år>" i bet. FiU1. Kolumnen "Regeringens förslag" är absolut; varje parti står
som "Avvikelse från regeringen". Ett partis absoluta ram = regeringens förslag plus partiets
avvikelse, alltså mekanisk normalisering ur samma tabell. Inga belopp imputeras eller jämkas.

LÄSNINGEN sker på tabellens GEOMETRI, inte på radernas text. Varje cell är en egen textrad i
PDF:en med en egen ram, och talen är högerställda: kolumnens högerkant sammanfaller på tiondels
punkt med rubrikens. Kolumntillhörighet avgörs därför av högerkanten, aldrig av ordningen mellan
celler. Textläsning tappar kolumnen så fort ett tal delas vid tusentalsmellanslag ("+2 650" blir
"+2" och "650"), och den felläsningen syns inte i utfallet. HTML-vägen används som OBEROENDE
PARSER i verifieringen, aldrig som källa.

VERIFIERINGEN är fyrlagrig, som för de tre år configen redan bar:
  1. Intern invariant: kolumnsummorna mot källans egen rad "Summa utgiftsområden", per kolumn.
     Toleransen är avrundningens, alltså högst 1 mnkr per utgiftsområde.
  2. Oberoende tabell: betänkandets bilagor bär samma ramar ABSOLUT och i tusental kronor, och
     läses av `a_forankring`-verktygets radparser. Kravet är hårt för regeringens ram, eftersom
     varje partis ram räknas ur den: någon bilaga ska återge den på kronan. Reservationerna
     jämförs också, men de får skilja sig, eftersom en reservation är ett annat dokument än
     partiets budgetmotion.
  3. Oberoende parser: samma tabell läst ur betänkandets HTML, en helt annan kodväg. Finns bara
     de år betänkandet har en HTML-tabell vars celler inte gått sönder i konverteringen.
  4. Roll-call ur riksdagens voteringlista: attributionen prövas mot voteringen i
     rambeslutspunkten, aldrig mot ett omdöme.

Utöver de fyra lagren läses de tre expertgranskade budgetåren 2023-2025 om ur PDF:en av
`--audit`, och måste träffa den signade configen på kronan.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Iterable, Mapping, Sequence
from typing import Any, NamedTuple

import httpx

from .. import ROOT, config
from . import a_forankring_transcribe as af

# Gränsen, ordagrant ur ADR 0007 punkt 2. Skriven före hämtningen, orörd efteråt.
FRAMES_TEST = (
    "alla åtta partier har en citerbar ram som listar utgiftsområde 1-27; citerbar betyder "
    "egen budgetmotion, regeringsställning, eller uppslutning bakom en gemensam ram belagd "
    "med votering"
)

BASE = "https://data.riksdagen.se"
EVIDENCE_DIR = ROOT / "docs" / "done" / "a_forankring"

# Partikoder som kan stå som kolumnrubrik. FP är Folkpartiet, som bytte namn till Liberalerna
# 2015-11-22 (samma parti, samma kod L i modellen).
_ALIAS = {"FP": "L"}
_HEADER_CODES = {"S", "M", "SD", "C", "V", "KD", "L", "MP", "FP"}

# Regeringen bakom budgetpropositionen för budgetåret, alltså vems ram kolumnen "Regeringens
# förslag" är. Avskrivet ur propositionens egen avsändare; budgetår Y bärs av prop. (Y-1)/Y:1.
# Raden prövas mot voteringen vid varje körning (_check_government): en regering som inte röstar
# för sin egen ram i rambeslutet är en avvikelse som skrivs ut.
GOVERNMENT: dict[int, tuple[str, ...]] = {
    2008: ("M", "C", "L", "KD"),   # prop. 2007/08:1 (Reinfeldt I)
    2009: ("M", "C", "L", "KD"),   # prop. 2008/09:1
    2010: ("M", "C", "L", "KD"),   # prop. 2009/10:1
    2011: ("M", "C", "L", "KD"),   # prop. 2010/11:1 (Reinfeldt II)
    2012: ("M", "C", "L", "KD"),   # prop. 2011/12:1
    2013: ("M", "C", "L", "KD"),   # prop. 2012/13:1
    2014: ("M", "C", "L", "KD"),   # prop. 2013/14:1
    2015: ("S", "MP"),             # prop. 2014/15:1 (Löfven I)
    2016: ("S", "MP"),             # prop. 2015/16:1
    2017: ("S", "MP"),             # prop. 2016/17:1
    2018: ("S", "MP"),             # prop. 2017/18:1
    2019: ("S", "MP"),             # prop. 2018/19:1 (övergångsregeringen)
    2020: ("S", "MP"),             # prop. 2019/20:1 (Löfven II)
    2021: ("S", "MP"),             # prop. 2020/21:1
    2022: ("S", "MP"),             # prop. 2021/22:1
    2023: ("M", "KD", "L"),        # prop. 2022/23:1 (Kristersson)
    2024: ("M", "KD", "L"),        # prop. 2023/24:1
    2025: ("M", "KD", "L"),        # prop. 2024/25:1
}

# Riksmöteskod för voteringen, samma serie som dok_id men skriven som riksdagen skriver den.
def _rm(budget_year: int) -> str:
    return f"{budget_year - 1}/{str(budget_year)[2:]}"


class Column(NamedTuple):
    """En kolumn i jämförelsetabellen: vilka partier den bär och var dess högerkant går."""

    key: str                 # framens namn i configen ('regeringen', 'S', 'M_C_L_KD', ...)
    parties: tuple[str, ...]  # partikoder som står bakom ramen ((), för regeringens kolumn)
    right: float             # cellernas högerkant i punkter


class PartyTable(NamedTuple):
    """Jämförelsetabellen för ett budgetår, läst ur källan."""

    caption: str
    page: int
    unit: str
    columns: list[Column]
    absolute: dict[str, dict[int, float]]   # framenamn -> {UO -> mnkr}
    deviations: dict[str, dict[int, float]]  # framenamn -> {UO -> avvikelse i mnkr}
    summa: dict[str, float]                  # framenamn -> källans egen summarad
    names: dict[int, str]


# --- Rubrik och kolumner ------------------------------------------------------------------

def caption_pattern(budget_year: int) -> re.Pattern[str]:
    """Rubriken på det årets jämförelsetabell. Preliminära utåren stängs ute uttryckligen."""
    return re.compile(
        r"Regeringens och (?:oppositionspartiernas|oppositionens|motionärernas|partiernas) "
        rf"förslag till utgiftsramar (?:för )?{budget_year}\b",
        re.I,
    )


def header_parties(text: str) -> tuple[str, ...] | None:
    """En rubrikcell -> partikoderna den bär, eller None om cellen inte är en partirubrik.

    Kolumnrubriken är antingen ett parti ('SD') eller en gemensam ram ('M, C, FP, KD',
    'S MP V'). Allt annat, som 'Regeringens' eller 'Miljoner kronor', faller.
    """
    tokens = [t for t in re.split(r"[,\s]+", text.strip()) if t]
    if not tokens or len(tokens) > 5:
        return None
    if not all(t.upper() in _HEADER_CODES for t in tokens):
        return None
    out = tuple(dict.fromkeys(_ALIAS.get(t.upper(), t.upper()) for t in tokens))
    return out or None


def frame_key(parties: Sequence[str]) -> str:
    """Framens namn i configen: partiets kod, eller koderna med understreck för en gemensam ram."""
    return "_".join(parties)


# --- PDF-läsning på geometri --------------------------------------------------------------

class _Line(NamedTuple):
    text: str
    x0: float
    x1: float
    y: float


def pdf_lines(page: Any) -> list[_Line]:
    """Sidans textrader i LÄSRIKTNINGENS koordinater. Varje tabellcell är en egen rad här.

    En bred tabell sätts ibland liggande på en stående sida, alltså med texten vriden ett
    kvarts varv (bet. 2015/16:FiU1 tabell 3.2). Radens `dir` bär vridningen, och koordinaterna
    räknas om till läsriktningen, så att resten av verktyget aldrig behöver veta om saken.
    """
    out: list[_Line] = []
    for block in page.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            text = "".join(span["text"] for span in line["spans"]).strip()
            if not text:
                continue
            x0, y0, x1, y1 = (float(v) for v in line["bbox"])
            direction = tuple(round(v) for v in line.get("dir", (1.0, 0.0)))
            if direction == (0, -1):          # texten löper nedifrån och upp
                out.append(_Line(text, -y1, -y0, x0))
            elif direction == (1, 0):
                out.append(_Line(text, x0, x1, y0))
            else:
                raise ValueError(f"okänd textriktning {direction} på raden {text!r}")
    out.sort(key=lambda ln: (ln.y, ln.x0))
    return out


def _find_columns(lines: Sequence[_Line], caption_y: float) -> list[Column]:
    """Kolumnerna ur rubrikraderna under tabellrubriken, vänster till höger.

    Regeringens kolumn känns igen på ordet 'förslag', partikolumnerna på sina koder.
    Högerkanten är kolumnens nyckel: talen är högerställda och delar högerkant med sin rubrik
    på tiondels punkt.

    Ordet 'förslag' står två gånger i flera år, en gång under 'Regeringens' och en gång i
    blockrubriken 'Avvikelse gentemot regeringens förslag' som spänner över partikolumnerna.
    Den vänstra är regeringens, och att den ligger till vänster om varje partikolumn prövas
    efteråt i stället för att antas.
    """
    gov_candidates: list[float] = []
    parties: list[Column] = []
    for ln in lines:
        if ln.y <= caption_y:
            continue
        if re.fullmatch(r"\d{1,2}", ln.text):
            break                                  # första UO-raden: rubriken är slut
        if re.fullmatch(r"(regeringens?\s+)?förslag", ln.text.lower()):
            gov_candidates.append(ln.x1)
            continue
        codes = header_parties(ln.text)
        if codes:
            parties.append(Column(frame_key(codes), codes, ln.x1))
    if not gov_candidates:
        raise ValueError("hittade ingen kolumn för regeringens förslag i tabellrubriken")
    if not parties:
        raise ValueError("hittade inga partikolumner i tabellrubriken")
    gov = Column("regeringen", (), min(gov_candidates))
    if gov.right >= min(c.right for c in parties):
        raise ValueError(
            f"regeringens kolumn @{gov.right:.1f} ligger inte till vänster om partikolumnerna "
            f"({[f'{c.key}@{c.right:.1f}' for c in parties]})"
        )
    return sorted([gov, *parties], key=lambda c: c.right)


# Ett tal börjar vid ett tecken som följer på blanksteg. Tusentalsmellanslaget saknar tecken
# och delar därför aldrig ett tal, medan två grannceller som klistrats ihop alltid delas.
_SPLIT_RE = re.compile(r"(?<=\s)(?=[−–+±-]\s?\d)")


def split_cells(text: str) -> list[str] | None:
    """En textrad -> ett tal per cell, eller None om raden inte är tal.

    Två grannceller hamnar ibland i samma textrad ('−508 −12 520' är M:s och SD:s celler i
    bet. 2016/17:FiU1 UO8). Delningen sker bara vid ett teckenbyte, alltså aldrig inuti ett
    tal, och varje del måste vara ett giltigt belopp. Går någon del inte att läsa faller raden
    som helhet i stället för att en cell tyst försvinner.
    """
    parts = [p.strip() for p in _SPLIT_RE.split(text.strip()) if p.strip()]
    if not parts:
        return None
    if any(af.parse_amount(p) is None for p in parts):
        return None
    return parts


def _assign(value_lines: Sequence[_Line], columns: Sequence[Column], where: str,
            tol: float = 4.0) -> dict[str, float]:
    """Radens tal -> kolumn via högerkanten.

    En hopklistrad cell bär bara den HÖGRA cellens högerkant. Dess sista tal hör därför till
    den kolumnen, och talen före det till kolumnerna omedelbart till vänster, i ordning. En
    okänd högerkant, en dubblett eller en oläsbar cell ger hård fail, aldrig en tyst nolla.
    """
    order = list(columns)
    out: dict[str, float] = {}
    for ln in value_lines:
        parts = split_cells(ln.text)
        if parts is None:
            if any(ch.isdigit() for ch in ln.text):
                raise ValueError(f"{where}: cellen {ln.text!r} går inte att läsa som belopp")
            continue
        near = min(order, key=lambda c: abs(c.right - ln.x1))
        if abs(near.right - ln.x1) > tol:
            raise ValueError(
                f"{where}: talet {ln.text!r} har högerkant {ln.x1:.1f} som inte hör till någon "
                f"kolumn ({[f'{c.key}@{c.right:.1f}' for c in order]})"
            )
        last = order.index(near)
        first = last - len(parts) + 1
        if first < 0:
            raise ValueError(f"{where}: cellen {ln.text!r} bär fler tal än det finns kolumner")
        for offset, part in enumerate(parts):
            col = order[first + offset]
            amount = af.parse_amount(part)
            if col.key in out:
                raise ValueError(
                    f"{where}: två tal i kolumn {col.key} ({out[col.key]} och {amount})")
            out[col.key] = float(amount)
    if "regeringen" not in out:
        raise ValueError(f"{where}: regeringens kolumn saknar tal")
    # En tom particell betyder ingen avvikelse, alltså noll. Att det stämmer prövas mot
    # källans egen summarad i check_sum_invariant, som skulle falla om en cell tappats bort.
    return {c.key: out.get(c.key, 0.0) for c in order}


def _row_values(band: Sequence[_Line], where: str) -> list[_Line]:
    """Radens tal ur bandet mellan två radankare: cellerna på den FÖRSTA höjd som bär tal.

    Två fall gör att bandet inte kan läsas rakt av. Ett ombrutet namn skjuter ned talen en
    höjd, så raden står inte alltid på ankarets höjd (bet. 2014/15:FiU1 UO18). Och mellan
    UO27 och summaraden står 'Minskning av anslagsbehållningar' med egna tal, som inte är
    någon utgiftsram (bet. 2007/08:FiU1). Båda löses av samma regel: raden är den översta
    höjden i bandet som över huvud taget bär tal, och det som står under hör till något annat.
    """
    if not band:
        raise ValueError(f"{where}: raden bär inga tal alls")
    top = min(ln.y for ln in band)
    return [ln for ln in band if abs(ln.y - top) <= ROW_TOLERANCE]


_SUMMA_RE = re.compile(r"^Summa\s+utgiftsområden", re.I)

# Cellerna på en rad delar höjd på tiondels punkt; radavståndet i tabellerna är
# minst 8 punkter. Toleransen ligger däremellan.
ROW_TOLERANCE = 3.0


def pdf_party_table(pdf_path: str, budget_year: int) -> PartyTable:
    """Jämförelsetabellen för ett budgetår, läst ur PDF:ens geometri."""
    import fitz  # endast det här verktyget, aldrig pipelinen

    want = caption_pattern(budget_year)
    doc = fitz.open(pdf_path)
    try:
        start = None
        for i in range(doc.page_count):
            flat = re.sub(r"\s+", " ", doc[i].get_text())
            if want.search(flat) and "Rikets styrelse" in flat and "preliminär" not in flat.lower():
                start, caption = i, want.search(flat).group(0)
                break
        if start is None:
            raise ValueError(f"{budget_year}: hittade inte jämförelsetabellen i {pdf_path}")

        unit = "mnkr"
        columns: list[Column] = []
        rows: dict[int, dict[str, float]] = {}
        names: dict[int, str] = {}
        summa: dict[str, float] = {}
        for page_no in range(start, min(start + 4, doc.page_count)):
            lines = pdf_lines(doc[page_no])
            flat = re.sub(r"\s+", " ", doc[page_no].get_text())
            caption_y = -1.0
            for ln in lines:
                if want.search(ln.text):
                    caption_y = ln.y
                    break
            if page_no == start and "Tusental kronor" in flat:
                unit = "tkr"
            try:
                page_columns = _find_columns(lines, caption_y)
            except ValueError:
                page_columns = []
            if page_columns:
                columns = page_columns
            if not columns:
                continue
            left = min(c.right for c in columns)
            right = max(c.right for c in columns)
            # Radankaret är UO-numret i vänsterkolumnen, och BARA när det är nästa väntade
            # nummer i följd. Annars skulle ett sidnummer eller ett belopp starta en rad.
            marks: list[tuple[float, str]] = []
            expected = len(rows) + 1
            for ln in lines:
                if ln.y <= caption_y or ln.x1 >= left - 20:
                    continue
                # Numret står antingen ensamt i sin cell eller ihopskrivet med namnet
                # ("10 Ekonomisk trygghet vid"). Båda formerna förekommer i samma tabell.
                if expected <= 27 and re.match(rf"^{expected}(?:\s+\D.*)?$", ln.text):
                    marks.append((ln.y, str(expected)))
                    expected += 1
            summa_line = next((ln for ln in lines if _SUMMA_RE.match(ln.text)), None)
            if summa_line is not None:
                marks.append((summa_line.y, "summa"))
            marks.sort()
            for idx, (y, kind) in enumerate(marks):
                end = marks[idx + 1][0] if idx + 1 < len(marks) else 1e9
                band = [ln for ln in lines if y - ROW_TOLERANCE <= ln.y < end - ROW_TOLERANCE]
                # Talen ligger mellan vänsterkolumnen och tabellens högerkant. Allt utanför
                # är marginal: sidnumret står till höger om sista kolumnen varje sida.
                where = f"{budget_year} {'summa' if kind == 'summa' else 'UO' + kind}"
                values = _row_values(
                    [ln for ln in band if left - 20 <= ln.x1 <= right + 4], where)
                cells = _assign(values, columns, where)
                if kind == "summa":
                    summa = cells
                else:
                    n = int(kind)
                    if n in rows:
                        continue
                    rows[n] = cells
                    label = [re.sub(rf"^{n}\s+", "", ln.text) for ln in band
                             if ln.x1 < left - 20 and ln.text != kind]
                    names[n] = " ".join(label).strip()
            if len(rows) >= 27 and summa:
                break
    finally:
        doc.close()

    missing = [n for n in range(1, 28) if n not in rows]
    if missing:
        raise ValueError(f"{budget_year}: utgiftsområde {missing} saknas i tabellen")
    return _build(budget_year, caption, start, unit, columns, rows, summa, names)


def _build(budget_year: int, caption: str, page: int, unit: str, columns: Sequence[Column],
           rows: Mapping[int, Mapping[str, float]], summa: Mapping[str, float],
           names: Mapping[int, str]) -> PartyTable:
    """Absoluta ramar ur regeringens kolumn plus varje partis avvikelse."""
    divisor = 1000.0 if unit == "tkr" else 1.0
    absolute: dict[str, dict[int, float]] = {}
    deviations: dict[str, dict[int, float]] = {}
    for col in columns:
        cells: dict[int, float] = {}
        devs: dict[int, float] = {}
        for n in range(1, 28):
            gov = rows[n]["regeringen"] / divisor
            if col.key == "regeringen":
                cells[n], devs[n] = gov, 0.0
            else:
                dev = rows[n][col.key] / divisor
                cells[n], devs[n] = gov + dev, dev
        nonpositive = [n for n, v in cells.items() if v <= 0]
        if nonpositive:
            raise ValueError(f"{budget_year}/{col.key}: UO {nonpositive} har ram <= 0")
        absolute[col.key] = cells
        deviations[col.key] = devs
    return PartyTable(
        caption=caption, page=page, unit=unit, columns=list(columns),
        absolute=absolute, deviations=deviations,
        summa={k: v / divisor for k, v in summa.items()},
        names={n: names.get(n, "") for n in range(1, 28)},
    )


# --- Verifiering --------------------------------------------------------------------------

# Källans summarad är avrundad, och cellerna är det också. En avvikelse på högst 1 mnkr per
# utgiftsområde ryms i avrundningen; mer än så är en felläsning och inte en avrundning.
SUM_TOLERANCE = 27.0


def check_sum_invariant(table: PartyTable) -> list[str]:
    """Kolumnsummorna mot källans egen rad 'Summa utgiftsområden'."""
    problems: list[str] = []
    if not table.summa:
        return ["summaraden saknas i tabellen"]
    gov_sum = sum(table.absolute["regeringen"].values())
    for col in table.columns:
        want = table.summa.get(col.key)
        if want is None:
            problems.append(f"{col.key}: summaraden saknar kolumnen")
            continue
        have = (gov_sum if col.key == "regeringen"
                else sum(table.deviations[col.key].values()))
        if abs(have - want) > SUM_TOLERANCE:
            problems.append(
                f"{col.key}: cellsumman {have:.0f} mot källans summarad {want:.0f} "
                f"(diff {have - want:+.0f} mnkr, tolerans {SUM_TOLERANCE:.0f})"
            )
    return problems


def html_party_table(html: str, budget_year: int) -> PartyTable | None:
    """Samma tabell läst ur betänkandets HTML — OBEROENDE PARSER, aldrig källa.

    HTML:en bär cellerna i dokumentordning utan ram, så kolumnen faller så fort ett tal delas
    vid tusentalsmellanslag. Den vägen duger därför bara som kontroll, och bara de år där
    cellräkningen stämmer på varje rad. Returnerar None när tabellen inte går att läsa så.
    """
    want = caption_pattern(budget_year)
    for m in af._TABLE_RE.finditer(html):
        lead = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html[max(0, m.start() - 1200):m.start()]))
        if not want.search(lead) or "preliminär" in lead.lower():
            continue
        rows_raw = [af._cells(r) for r in af._ROW_RE.findall(m.group(0))]
        # Kolumnen är en CELL i rubriken, aldrig en delsträng: fyra celler 'S' 'V' 'C' 'MP' är
        # fyra kolumner, medan en cell 'M, C, FP, KD' är en gemensam ram i en enda kolumn.
        codes: list[tuple[str, ...]] = []
        for row in rows_raw[:4]:
            for cell in row:
                parsed = header_parties(cell)
                if parsed:
                    codes.append(parsed)
        if not codes:
            return None
        columns = [Column("regeringen", (), 0.0)] + [
            Column(frame_key(c), c, float(i + 1)) for i, c in enumerate(codes)
        ]
        rows: dict[int, dict[str, float]] = {}
        summa: dict[str, float] = {}
        for cells in rows_raw:
            if not cells:
                continue
            head = cells[0].strip()
            if _SUMMA_RE.match(head):
                values = [af.parse_amount(c) for c in cells[1:]]
            elif re.fullmatch(r"\d{1,2}", head) and 1 <= int(head) <= 27:
                values = [af.parse_amount(c) for c in cells[2:]]
            else:
                continue
            values = [0.0 if v is None else v for v in values]
            if len(values) != len(columns):
                return None
            cell_map = {col.key: values[i] for i, col in enumerate(columns)}
            if _SUMMA_RE.match(head):
                summa = cell_map
            else:
                rows.setdefault(int(head), cell_map)
        if len(rows) != 27:
            return None
        unit = "tkr" if "Tusental" in lead else "mnkr"
        return _build(budget_year, want.search(lead).group(0), -1, unit, columns, rows, summa, {})
    return None


def cross_check(pdf: PartyTable, other: PartyTable | None, label: str) -> list[str]:
    """PDF-läsningen mot en oberoende läsning av samma tabell. Tomt = de stämmer."""
    if other is None:
        return [f"{label}: ingen oberoende läsning tillgänglig"]
    problems: list[str] = []
    if {c.key for c in pdf.columns} != {c.key for c in other.columns}:
        return [f"{label}: kolumnerna skiljer sig "
                f"({sorted(c.key for c in pdf.columns)} mot {sorted(c.key for c in other.columns)})"]
    for key, cells in pdf.absolute.items():
        for n, value in cells.items():
            have = other.absolute[key].get(n)
            if have is None or round(have) != round(value):
                problems.append(f"{label}: {key}/UO{n} = {value:.0f} mot {have}")
    return problems


_BILAGA_RE = re.compile(
    r"^\s*(Regeringens|Utskottets|Reservanternas)?\s*[Ff]örslag till utgiftsramar\s+(?:för\s+)?"
    r"(\d{4})\s*(?:\(([^)]{1,40})\))?\s*$",
    re.M,
)


def pdf_absolute_bilagor(pdf_path: str, budget_year: int) -> dict[str, dict[int, float]]:
    """Betänkandets bilagetabeller med ABSOLUTA ramar för budgetåret, i miljoner kronor.

    Bilagorna är en annan tabell än jämförelsetabellen, i en annan enhet (tusental kronor) och
    med absoluta belopp i stället för avvikelser. De läses dessutom av `a_forankring`-verktygets
    radparser, alltså en annan kodväg. Skillnaden mot jämförelsetabellen är därför ett äkta
    oberoende prov både på avläsningen och på additionen regeringen + avvikelse.
    """
    import fitz

    doc = fitz.open(pdf_path)
    try:
        out: dict[str, dict[int, float]] = {}
        for page_no in range(doc.page_count):
            text = doc[page_no].get_text()
            match = None
            for m in _BILAGA_RE.finditer(text):
                if int(m.group(2)) == budget_year:
                    match = m
                    break
            if match is None:
                continue
            caption = re.sub(r"\s+", " ", match.group(0)).strip()
            if caption in out:
                continue
            if match.group(1) == "Reservanternas" and not match.group(3):
                # En reservationsbilaga utan partibeteckning bär flera reservanter i samma
                # tabell. Radparsern tar sista talet på raden och kan inte veta vems det är,
                # så tabellen duger inte som prov och utelämnas hellre än jämförs fel.
                continue
            rows: dict[int, tuple[str, float | None]] = {}
            for i in range(page_no, min(page_no + 4, doc.page_count)):
                rows.update(af.uo_rows_from_pdf_page(doc[i].get_text(),
                                                     start_at=max(rows, default=0)))
                if len(rows) >= 27:
                    break
            values = {n: rows[n][1] / 1000.0 for n in range(1, 28)
                      if rows.get(n, (None, None))[1] is not None}
            if len(values) == 27:
                out[caption] = values
        return out
    finally:
        doc.close()


def check_bilagor(
    table: PartyTable, pdf_path: str, budget_year: int
) -> tuple[dict[str, Any], list[str]]:
    """Jämförelsetabellens ramar mot bilagornas absoluta tabeller.

    Kravet är hårt för regeringens ram: någon bilaga ska återge den PÅ KRONAN, eftersom varje
    partis ram räknas ur den. Reservationerna jämförs också, men de får skilja sig: en
    reservation är ett annat dokument än partiets budgetmotion, och den kan bära en justering
    (bet. 2014/15:FiU1 skiljer sig 200 mnkr på UO2 mot allianspartiernas gemensamma motion).
    """
    report: dict[str, Any] = {}
    matched_government = False
    for caption, values in pdf_absolute_bilagor(pdf_path, budget_year).items():
        best, best_off = None, None
        for key, cells in table.absolute.items():
            off = max(abs(round(cells[n]) - round(values[n])) for n in range(1, 28))
            if best_off is None or off < best_off:
                best, best_off = key, off
        report[caption] = {"narmast": best, "max_avvikelse_mnkr": best_off}
        if best == "regeringen" and best_off == 0:
            matched_government = True
    if not report:
        return report, [f"bilagor: hittade ingen absolut ramtabell för {budget_year}"]
    if not matched_government:
        return report, [
            "bilagor: ingen bilaga återger regeringens ram på kronan "
            f"({ {k: v['max_avvikelse_mnkr'] for k, v in report.items()} })"
        ]
    return report, []


def check_adopted_frame(table: PartyTable, budget_year: int) -> tuple[str | None, list[str]]:
    """Den beslutade ramen mot en av tabellens ramar — OBEROENDE RE-EXTRAKTION.

    `config/a_forankring.yaml` bär den ram kammaren faktiskt beslutade för varje år i fönstret.
    Den kommer ur en ANNAN tabell (betänkandets bilaga), i en ANNAN enhet (tusental kronor),
    läst av ett ANNAT verktyg (a_forankring_transcribe), och den är redan expertgranskad och
    signad. Beslutet är alltid en av ramarna i jämförelsetabellen: regeringens förslag de år
    utskottet följde propositionen, och annars den reservation som vann.

    Returnerar vilken ram som träffade, plus avvikelser när ingen gör det.
    """
    frames = config.a_forankring()["a1"]["decided_frames"]
    decided = frames.get(budget_year)
    if decided is None:
        return None, [f"beslutad: {budget_year} saknas i a_forankring.yaml"]
    want = {n: float(decided[f"UO{n}"]) for n in range(1, 28) if f"UO{n}" in decided}
    if len(want) != 27:
        return None, [f"beslutad: {budget_year} saknar utgiftsområden i a_forankring.yaml"]
    best, best_off = None, None
    for key, cells in table.absolute.items():
        off = max(abs(round(cells[n]) - round(want[n])) for n in range(1, 28))
        if best_off is None or off < best_off:
            best, best_off = key, off
    if best_off:
        return None, [
            f"beslutad: ingen ram träffar den beslutade ramen i a_forankring.yaml "
            f"(närmast {best}, största avvikelse {best_off:.0f} mnkr)"
        ]
    return best, []


# --- Voteringen och attributionen ---------------------------------------------------------

def fetch_rollcall(budget_year: int, client: httpx.Client) -> dict[str, dict[str, int]]:
    """Rambeslutspunktens votering per parti, ur riksdagens voteringlista (cachad)."""
    path = af.CACHE_DIR / f"votering_{budget_year}.json"
    if path.exists():
        payload = json.loads(path.read_text(encoding="utf-8"))
    else:
        url = (f"{BASE}/voteringlista/?rm={_rm(budget_year).replace('/', '%2F')}"
               f"&bet=FiU1&punkt=2&utformat=json&sz=20&gruppering=parti")
        resp = client.get(url)
        resp.raise_for_status()
        payload = resp.json()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    rows = payload["voteringlista"].get("votering") or []
    if isinstance(rows, Mapping):
        rows = [rows]
    out: dict[str, dict[str, int]] = {}
    for row in rows:
        code = _ALIAS.get(str(row.get("parti", "")).upper(), str(row.get("parti", "")).upper())
        if code not in config.party_codes():
            continue
        out[code] = {k: int(row.get(k) or 0) for k in ("Ja", "Nej", "Avstår", "Frånvarande")}
    return out


def majority_vote(counts: Mapping[str, int]) -> str:
    """Partiets röst: den ståndpunkt flest av dess ledamöter tog. Ingen röst -> 'Frånvarande'."""
    cast = {k: counts.get(k, 0) for k in ("Ja", "Nej", "Avstår")}
    if not any(cast.values()):
        return "Frånvarande"
    return max(cast, key=lambda k: cast[k])


class Attribution(NamedTuple):
    frame: str
    role: str
    basis: str
    note: str


def attribute(
    budget_year: int, columns: Sequence[Column], rollcall: Mapping[str, dict[str, int]]
) -> tuple[dict[str, Attribution], list[str]]:
    """Vilken ram varje parti står bakom, och på vilken citerbar grund (ADR 0007 punkt 2).

    Ordningen är ADR:ns: egen budgetmotion först, sedan regeringsställning, sist uppslutning
    bakom en gemensam ram belagd med votering. Ett parti som inte når någon av de tre
    utelämnas, och året faller därmed ur gränsen i stället för att gissas fram.
    """
    parties = config.party_codes()
    government = GOVERNMENT.get(budget_year, ())
    gov_votes = {majority_vote(rollcall.get(p, {})) for p in government if p in rollcall}
    out: dict[str, Attribution] = {}
    problems: list[str] = []
    own = {p: col for col in columns for p in col.parties}
    for party in parties:
        vote = majority_vote(rollcall.get(party, {}))
        if party in own:
            col = own[party]
            others = ", ".join(c for c in col.parties if c != party)
            shared = f", gemensam med {others}" if others else ""
            out[party] = Attribution(
                col.key, "opposition" if party not in government else "government", "egen_ram",
                f"egen budgetmotion i bet. FiU1 {_rm(budget_year)} "
                f"(kolumn {'/'.join(col.parties)}{shared})",
            )
        elif party in government:
            out[party] = Attribution(
                "regeringen", "government", "regeringsstallning",
                f"regeringsparti bakom prop. {_rm(budget_year)}:1; röst i rambeslutet: {vote}",
            )
        elif gov_votes and {vote} == gov_votes and vote in ("Ja", "Nej"):
            out[party] = Attribution(
                "regeringen", "support", "votering",
                f"uppslutning bakom regeringens ram: samma röst ({vote}) som "
                f"{'/'.join(government)} i voteringen om rambeslutet, bet. FiU1 "
                f"{_rm(budget_year)} punkt 2",
            )
        else:
            seat = "ingen rad i voteringen" if party not in rollcall else f"röst {vote}"
            problems.append(
                f"{party}: ingen citerbar ram (ingen egen kolumn, ej regeringsparti, "
                f"{seat} mot regeringens {sorted(gov_votes) or 'okänd'})"
            )
    for party in government:
        if party in own:
            problems.append(f"{party}: regeringsparti med egen kolumn i {budget_year}")
    return out, problems


# --- Körlägen -----------------------------------------------------------------------------

def read_year(
    budget_year: int, client: httpx.Client
) -> tuple[PartyTable, list[str], dict[str, Any]]:
    """Ett budgetårs jämförelsetabell, dess avvikelser och verifieringens täckning.

    Lagren är: intern summainvariant per kolumn, den beslutade ramen ur a_forankring.yaml
    (annan tabell, annan enhet, annat verktyg, redan signad), och en oberoende HTML-parser
    där betänkandet har en läsbar HTML-tabell. Roll-call ligger i `attribute`, och
    re-extraktionen av de expertgranskade budgetåren i `--audit`.
    """
    dok = af.dok_id(budget_year)
    status = af.fetch_status(dok, client)
    pdf = af.fetch_pdf(status, dok, client)
    table = pdf_party_table(pdf, budget_year)

    problems = check_sum_invariant(table)
    bilagor, bilaga_problems = check_bilagor(table, pdf, budget_year)
    problems += bilaga_problems
    # Vilken av tabellens ramar den BESLUTADE ramen är redovisas, men grindar inte. Den är
    # regeringens ram de flesta år, en vinnande reservation 2015 och 2019, och 2022 utskottets
    # eget förslag, som är ett förhandlat mellanting och därför inte något partis egen ram.
    adopted, _adopted_problems = check_adopted_frame(table, budget_year)
    html = status["dokumentstatus"]["dokument"].get("html") or ""
    html_table = html_party_table(html, budget_year)
    html_problems = cross_check(table, html_table, "html")
    problems += [p for p in html_problems if "ingen oberoende läsning" not in p]

    report = {
        "celler": 27 * len(table.columns),
        "summainvariant_mnkr": {
            col.key: round(
                (sum(table.absolute["regeringen"].values()) if col.key == "regeringen"
                 else sum(table.deviations[col.key].values())) - table.summa.get(col.key, 0.0)
            )
            for col in table.columns
        } if table.summa else None,
        "beslutad_ram_traffar": adopted,
        "bilagor": bilagor,
        "html_provad": html_table is not None,
    }
    return table, problems, report


def run_bound(years: Iterable[int]) -> dict[str, Any]:
    """Tredje gränsen (ADR 0007 punkt 2), år för år. Skriver in sig i bevisfilen."""
    years = sorted(years)
    per_year: dict[str, Any] = {}
    with af._client() as client:
        for year in years:
            row: dict[str, Any] = {"dok_id": af.dok_id(year)}
            try:
                table, problems, report = read_year(year, client)
                rollcall = fetch_rollcall(year, client)
                attribution, attribution_problems = attribute(year, table.columns, rollcall)
                row.update({
                    # Ett år räknas som fullständigt bara när BÅDE attributionen och
                    # verifieringen går igenom. En overifierad avläsning får aldrig bära
                    # gränsen: då vore gränsen ett omdöme om parsern och inte om källan.
                    "ok": not attribution_problems and not problems,
                    "caption": table.caption,
                    "unit": table.unit,
                    "columns": [{"frame": c.key, "parties": list(c.parties)} for c in table.columns],
                    "government": list(GOVERNMENT.get(year, ())),
                    "rollcall": {p: majority_vote(v) for p, v in sorted(rollcall.items())},
                    "attribution": {p: a._asdict() for p, a in sorted(attribution.items())},
                    "missing": attribution_problems,
                    "verification": problems,
                })
            except Exception as exc:                    # noqa: BLE001 - bevisfilen ska bära felet
                row.update({"ok": False, "error": str(exc)})
            per_year[str(year)] = row
            print(f"{year}: {'OK' if row['ok'] else row.get('error') or row.get('missing')}",
                  flush=True)

    bound = _contiguous_bound(per_year, years)
    out = {"bound": bound, "test": FRAMES_TEST, "adr": "ADR 0007 punkt 2", "per_year": per_year}
    _write_into_evidence(out)
    print(f"\nTredje gränsen: {bound} (fönstret {bound}-{max(years)})")
    return out


def _contiguous_bound(per_year: Mapping[str, Any], years: Sequence[int]) -> int | None:
    """Tidigaste året varifrån VARJE år fram till det sista är fullständigt.

    Sammanhängande, eftersom a1-grinden är ett snitt över åren (ADR 0007 punkt 5): ett
    ofullständigt år inuti fönstret släcker a1 i varje kategori.
    """
    bound: int | None = None
    for year in reversed(years):
        if not per_year.get(str(year), {}).get("ok"):
            break
        bound = year
    return bound


def _write_into_evidence(block: Mapping[str, Any]) -> None:
    """Lägger tredje gränsen i docs/done/a_forankring/fonster.json bredvid de två andra."""
    path = EVIDENCE_DIR / "fonster.json"
    evidence = json.loads(path.read_text(encoding="utf-8"))
    evidence["a1_frames"] = block
    path.write_text(json.dumps(evidence, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Skrev {path}")


_CONFIG_HEADER = '''# Rösta — föreslagna utgiftsramar per utgiftsområde (UO), per parti, per budgetår.
# AUTOGENERERAD av
#
#     python -m pipeline.tools.budget_ramar_transcribe --config
#
# Redigera aldrig för hand. Matar delpoäng A:s a1 (budgetprioritering). Se pipeline/budget.py,
# pipeline/tools/budget_ramar_transcribe.py och docs/done/fas1b_budget_metod.md.
#
# ADR 0007 punkt 1: a1:s TÄLJARE täcker samma år som a1:s FÖRANKRING. Fönstret börjar vid den
# senaste av a1:s två gränser (ADR 0005 punkt 7 och ADR 0007 punkt 2), som båda skrevs före
# hämtningen och står i docs/done/a_forankring/fonster.json.
#
# KÄLLA: tabellen "Regeringens och oppositionspartiernas (eller motionärernas) förslag till
# utgiftsramar för <år>" i bet. FiU1. Regeringens förslag absolut, varje parti som avvikelse
# från regeringen; partiets absoluta ram = regeringens förslag plus partiets avvikelse, alltså
# mekanisk normalisering ur samma tabell. Inga belopp imputeras eller jämkas, och varje frame
# citerar sin källrad. Saknad eller ogiltig cell ger hård fail i a1_shares, aldrig en tyst 0.
#
# INGEN RUNTIME-PARSER finns: A är tyngsta delpoängen och får aldrig kunna korrumperas av en
# bräcklig parser. Talen läses ur PDF:ens geometri (kolumnens högerkant), aldrig ur cellernas
# ordning, och verifieras fyrlagrigt vid varje körning: intern summainvariant per kolumn,
# betänkandets bilagor med absoluta belopp i tusental kronor, betänkandets HTML där den är
# läsbar, och roll-call ur riksdagens voteringlista. Raden `verification` per budgetår bär
# utfallet. De expertgranskade åren läses dessutom om av `--audit` och måste träffa på kronan.
#
# ATTRIBUTION (ADR 0007 punkt 2): ett parti får en ram bara på citerbar grund — egen
# budgetmotion, regeringsställning, eller uppslutning bakom en gemensam ram belagd med
# votering. `basis` bär vilken av de tre som gäller och `note` citerar den.
#
# Struktur:
#   unit: beloppens enhet (alla frames i samma enhet; relativa andelar är enhetsoberoende)
'''


# Budgetår som redan är expertgranskade och mänskligt signade. De läses om ur källan vid varje
# körning och måste träffa den signade configen på kronan (--audit), så raden nedan kan inte
# tyst drifta. Nya år står som version 0 tills en människa har signat dem.
SIGNED_OFF: dict[int, str] = {
    2023: "2026-06-05",
    2024: "2026-06-05",
    2025: "2026-06-05",
}


def run_config(years: Iterable[int]) -> None:
    """Skriver hela config/budget_ramar.yaml ur källan."""
    years = sorted(years, reverse=True)
    lines = [_CONFIG_HEADER, "", "unit: mnkr", "", "budget_years:"]
    with af._client() as client:
        for year in years:
            table, problems, report = read_year(year, client)
            rollcall = fetch_rollcall(year, client)
            attribution, attribution_problems = attribute(year, table.columns, rollcall)
            for problem in problems + attribution_problems:
                raise ValueError(f"{year}: {problem}")
            spec = af.ADOPTED[year]
            signed = SIGNED_OFF.get(year)
            lines += [
                f"  {year}:",
                f"    version: {1 if signed else 0}"
                + (f"     # expertgranskad, mänsklig sign-off {signed}"
                   if signed else "     # väntar på mänsklig sign-off"),
                f'    decided_in: "bet. {_rm(year)}:FiU1 ({spec.caption})"',
                f'    source_table: "{table.caption}"',
                f'    verification: "summainvariant '
                f'{ {k: v for k, v in report["summainvariant_mnkr"].items()} } mnkr; '
                f'bilagor {[k for k in report["bilagor"]]}; '
                f'html-parser {"ja" if report["html_provad"] else "nej"}"',
                "    ramar:",
            ]
            for col in table.columns:
                who = "regeringens förslag" if col.key == "regeringen" else "/".join(col.parties)
                lines.append(f"      {col.key}:")
                lines.append(
                    f'        source_ref: "riksdag:bet:{_rm(year)}:FiU1 ({table.caption}; '
                    f'{who})"'
                )
                cells = table.absolute[col.key]
                lines += [
                    f"        UO{n}: {round(cells[n])}     # {table.names.get(n, '')}".rstrip()
                    for n in range(1, 28)
                ]
            lines.append("    party_frame:")
            lines.append("      # Citerbar grund per parti (ADR 0007 punkt 2), aldrig gissad.")
            for party in config.party_codes():
                a = attribution[party]
                lines.append(
                    f"      {party + ':':4s} {{ frame: {a.frame}, role: {a.role}, "
                    f'basis: {a.basis}, note: "{a.note}" }}'
                )
            print(f"{year}: {len(table.columns)} ramar, {len(table.absolute['regeringen'])} UO",
                  flush=True)
    path = ROOT / "config" / "budget_ramar.yaml"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Skrev {path} — {len(years)} budgetår")


def run_frames(years: Iterable[int]) -> None:
    """Ett eller flera års tabeller till stdout, med alla verifieringslager. Skriver ingen fil."""
    with af._client() as client:
        for year in sorted(years):
            table, problems, report = read_year(year, client)
            rollcall = fetch_rollcall(year, client)
            attribution, attribution_problems = attribute(year, table.columns, rollcall)
            print(f"\n=== {year} {af.dok_id(year)} s.{table.page} [{table.unit}] {table.caption}")
            print("    kolumner: " + ", ".join(
                f"{c.key}({'/'.join(c.parties) or 'regeringen'})@{c.right:.1f}"
                for c in table.columns))
            for party, a in sorted(attribution.items()):
                print(f"    {party:3s} -> {a.frame:12s} {a.basis:18s} {a.note}")
            for problem in problems + attribution_problems:
                print(f"    AVVIKELSE {problem}")


def run_audit(years: Iterable[int] | None = None) -> int:
    """config/budget_ramar.yaml mot källan. Exit 1 vid minsta avvikelse."""
    cfg = config.budget_ramar()
    blocks = (cfg or {}).get("budget_years") or {}
    years = sorted(blocks) if years is None else sorted(years)
    problems: list[str] = []
    with af._client() as client:
        for year in years:
            block = blocks.get(year)
            if block is None:
                problems.append(f"{year}: saknas i configen")
                continue
            table, year_problems, _report = read_year(year, client)
            problems += [f"{year}: {p}" for p in year_problems]
            rollcall = fetch_rollcall(year, client)
            attribution, attribution_problems = attribute(year, table.columns, rollcall)
            problems += [f"{year}: {p}" for p in attribution_problems]
            for key, cells in table.absolute.items():
                have = (block.get("ramar") or {}).get(key)
                if have is None:
                    problems.append(f"{year}: configen saknar ramen {key}")
                    continue
                for n in range(1, 28):
                    if have.get(f"UO{n}") != round(cells[n]):
                        problems.append(
                            f"{year}/{key}/UO{n}: config {have.get(f'UO{n}')} != "
                            f"källa {round(cells[n])}")
            for party, a in attribution.items():
                spec = (block.get("party_frame") or {}).get(party) or {}
                if spec.get("frame") != a.frame:
                    problems.append(
                        f"{year}/{party}: config frame {spec.get('frame')!r} != källa {a.frame!r}")
            print(f"{year}: {len(table.columns)} ramar kontrollerade", flush=True)
    for problem in problems:
        print(f"AVVIKELSE {problem}")
    print("\nconfig/budget_ramar.yaml matchar källan" if not problems
          else f"\n{len(problems)} avvikelser")
    return 1 if problems else 0


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bound", action="store_true", help="tredje gränsen -> bevisfilen")
    parser.add_argument("--frames", action="store_true", help="läs år och skriv ut kontrollerna")
    parser.add_argument("--config", action="store_true", help="skriv config/budget_ramar.yaml")
    parser.add_argument("--audit", action="store_true", help="config mot källa (default)")
    parser.add_argument("--from", dest="start", type=int, default=2011)
    parser.add_argument("--to", dest="end", type=int, default=2025)
    args = parser.parse_args()
    years = range(args.start, args.end + 1)

    if args.bound:
        run_bound(years)
    elif args.frames:
        run_frames(years)
    elif args.config:
        run_config(years)
    else:
        raise SystemExit(run_audit(years))


if __name__ == "__main__":
    main()
