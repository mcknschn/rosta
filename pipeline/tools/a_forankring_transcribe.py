"""Hämtar, prövar och transkriberar FÖRANKRINGEN för delpoäng A (ADR 0005).

A är absolut efter ADR 0005: varje andel mäts mot hur stor andel kategorin normalt fått under
ett historiskt fönster. Det här verktyget bygger underlaget till `config/a_forankring.yaml` och
skriver bevisfilen för fönstrets två gränser. Det körs för hand, aldrig av pipelinen — samma
transkribera-in-i-config-mönster som `config/budget_ramar.yaml`. Ingen runtime-parser finns, så
en bräcklig parser kan aldrig korrumpera A.

    python -m pipeline.tools.a_forankring_transcribe --window    # gränserna -> docs/done/a_forankring/
    python -m pipeline.tools.a_forankring_transcribe --frames    # a1: beslutade ramar -> YAML
    python -m pipeline.tools.a_forankring_transcribe --chamber   # a2: kammarens motioner -> YAML
    python -m pipeline.tools.a_forankring_transcribe --config    # skriv config/a_forankring.yaml
    python -m pipeline.tools.a_forankring_transcribe --audit     # config mot källa (exit 1 vid diff)

Fönstrets TRE gränser är krav som faller ut, inte omdömen efter hämtningen. De två första
står i ADR 0005 punkt 7, den tredje i ADR 0007 punkt 2:

  a1  FiU1:s rambeslutstabell listar utgiftsområde 1-27, alltså samma indelning som
      `mappings.expenditure_areas` bygger på. NAMNEN hämtas och skrivs i bevisfilen men grindar
      inte, eftersom configens namnlista är en förkortning som aldrig varit något års officiella
      lista (UO10 heter "Ekonomisk trygghet vid sjukdom och funktionsnedsättning" i varje
      granskat år) och dessutom blandar två vintages (UO19 nytt namn, UO13 och UO20 gamla).
      En bokstavlig namnlikhet ger noll år och kan alltså inte pröva någonting.
  a1  (den tredje gränsen, ADR 0007 punkt 2) Alla åtta partier har en CITERBAR RAM som listar
      utgiftsområde 1-27. Citerbar betyder egen budgetmotion, regeringsställning, eller
      uppslutning bakom en gemensam ram belagd med votering. Gränsen bär a1:s TÄLJARE, alltså
      partiernas egna ramar, medan den första gränsen bär a1:s förankring. Provet ligger i
      `pipeline/tools/budget_ramar_transcribe.py`, som läser samma FiU1-tabell.
  a2  Alla åtta nuvarande partier har minst en motion i varje utskott som mappningen använder,
      under kalenderåret.

Gränserna skrivs FÖRE hämtningen och rörs inte efteråt. Den tredje gränsens ordalydelse är
avskriven ur ADR 0007 punkt 2 och står i `budget_ramar_transcribe.FRAMES_TEST`.

Den beslutade ramen per budgetår läses aldrig av gissning: dokumentets egen `vinnare` och
meningen om utgiftsramarna avgör vilken tabell som gäller, och båda skrivs i bevisfilen.
"""

from __future__ import annotations

import argparse
import html as htmlmod
import json
import re
import sys
import time
from collections.abc import Iterable, Mapping
from typing import Any, NamedTuple

import httpx

from .. import ROOT, config
from ..sources.base import RAW_DIR

BASE = "https://data.riksdagen.se"
_UA = {"User-Agent": "rosta-datapipeline/0.1 (civic-tech; official swedish open data)"}
EVIDENCE_DIR = ROOT / "docs" / "done" / "a_forankring"
CACHE_DIR = RAW_DIR / "riksdagen" / "fiu1"

# Riksmöteskoden i dokument-id:t. Budgetår Y beslutas i riksmöte (Y-1)/Y. Serien är obruten:
# H0 = 2012/13 och räknas upp ett steg per riksmöte, med bokstäver efter nio (ADR 0005 följder).
# G-åren står som en uttrycklig tabell, eftersom bokstavsserien byter bokstavsgrupp där.
_RM_LETTERS = "0123456789ABCDEFGHIJ"
_RM_BEFORE_H = {2008: "GV", 2009: "GW", 2010: "GX", 2011: "GY", 2012: "GZ"}


def dok_id(budget_year: int) -> str:
    """Dokument-id för bet. FiU1 som beslutar budgetåret (t.ex. 2024 -> HB01FiU1)."""
    if budget_year in _RM_BEFORE_H:
        return f"{_RM_BEFORE_H[budget_year]}01FiU1"
    idx = budget_year - 2013
    if not 0 <= idx < len(_RM_LETTERS):
        raise ValueError(f"Budgetår {budget_year} ligger utanför den kända riksmötesserien")
    return f"H{_RM_LETTERS[idx]}01FiU1"


class Adopted(NamedTuple):
    """Vilken ramtabell kammaren faktiskt beslutade, läst ur dokumentet självt."""

    winner: str          # dokumentets 'vinnare': 'utskottet' | 'reservationen' | 'reservation N'
    sentence: str        # meningen om utgiftsramarna i beslutspunkten
    caption: str         # rubriken på den tabell meningen (plus vinnaren) pekar ut
    source: str          # 'html' | 'pdf'
    unit: str            # 'tkr' | 'mnkr' — tabellens egen enhet


# Per budgetår: vilken tabell som beslutades, och var den finns. Rubriken är avskriven ur
# dokumentet och vinnaren kontrolleras mot dokumentets egen 'vinnare' vid varje körning
# (_check_adopted), så raden nedan kan aldrig tyst drifta ifrån källan.
ADOPTED: dict[int, Adopted] = {
    # 2011-2013 har inget partinamn i bilagerubriken; utskottets förslag ÄR den beslutade ramen.
    2011: Adopted("utskottet", "i enlighet med vad regeringen föreslår",
                  "Förslag till utgiftsramar 2011", "html", "tkr"),
    2012: Adopted("utskottet", "enligt utskottets förslag i bilaga 3",
                  "Förslag till utgiftsramar 2012", "html", "tkr"),
    2013: Adopted("utskottet", "i enlighet med utskottets förslag i bilaga 3",
                  "Förslag till utgiftsramar 2013", "html", "tkr"),
    2014: Adopted("utskottet", "i enlighet med utskottets förslag i bilaga 2",
                  "Utskottets förslag till utgiftsramar 2014", "html", "tkr"),
    # Reservationen vann: SD röstade på allianspartiernas ram (M, C, FP, KD).
    2015: Adopted("reservationen", "i enlighet med utskottets förslag i bilaga 2",
                  "Reservanternas förslag till utgiftsramar för 2015 (M, C, FP, KD)", "pdf", "tkr"),
    2016: Adopted("utskottet", "i enlighet med utskottets förslag i bilaga x",
                  "Utskottets förslag till utgiftsramar 2016", "pdf", "tkr"),
    2017: Adopted("utskottet", "i enlighet med utskottets förslag i bilaga 2",
                  "Utskottets förslag till utgiftsramar 2017", "html", "tkr"),
    2018: Adopted("utskottet", "enligt utskottets förslag i bilaga 2",
                  "Utskottets förslag till utgiftsramar 2018", "html", "tkr"),
    # Reservation 5 (M, KD) vann över utskottets förslag, som var regeringens ram.
    2019: Adopted("reservation 5", "enligt regeringens förslag",
                  "Reservanternas förslag till utgiftsramar 2019 (M, KD)", "html", "tkr"),
    2020: Adopted("utskottet", "enligt regeringens förslag",
                  "Regeringens förslag till utgiftsramar 2020", "html", "tkr"),
    2021: Adopted("utskottet", "enligt regeringens förslag",
                  "Regeringens förslag till utgiftsramar 2021", "pdf", "tkr"),
    2022: Adopted("utskottet", "enligt utskottets förslag i bilaga 4",
                  "Utskottets förslag till utgiftsramar 2022", "pdf", "tkr"),
    2023: Adopted("utskottet", "enligt regeringens förslag",
                  "Regeringens förslag till utgiftsramar 2023", "html", "tkr"),
    2024: Adopted("utskottet", "enligt regeringens förslag",
                  "Regeringens förslag till utgiftsramar 2024", "html", "tkr"),
    2025: Adopted("utskottet", "enligt regeringens förslag",
                  "Regeringens förslag till utgiftsramar 2025", "html", "tkr"),
}


# --- Rena parsers (golden-testbara utan livedata) --------------------------------------

_CELL_RE = re.compile(r"<t[dh]\b.*?>(.*?)</t[dh]>", re.S | re.I)
_ROW_RE = re.compile(r"<tr\b.*?</tr>", re.S | re.I)
_TABLE_RE = re.compile(r"<table\b.*?</table>", re.S | re.I)
_AMOUNT_RE = re.compile(r"^[−–\-+±]?[\d\s ]+$")


def _text(fragment: str) -> str:
    return re.sub(r"\s+", " ", htmlmod.unescape(re.sub(r"<[^>]+>", " ", fragment))
                  .replace(" ", " ")).strip()


def caption_key(text: str) -> str:
    """Rubrik -> jämförbar nyckel: gemener, bara bokstäver och siffror.

    Betänkandenas HTML och PDF bär lösa mellanslag inuti ord ("Regeringens f örslag", "20 20")
    efter konverteringen från sättningsformatet. En exakt strängjämförelse missar då rubriken
    fast den står där. Nyckeln tar bort allt utom tecknen själva.
    """
    return re.sub(r"[^0-9a-zåäöéü]", "", text.lower())


def _cells(row: str) -> list[str]:
    return [_text(m.group(1)) for m in _CELL_RE.finditer(row)]


def parse_amount(raw: str) -> float | None:
    """'19 070 363' -> 19070363.0. '±0' -> 0.0. Icke-belopp -> None."""
    s = raw.replace(" ", " ").replace("−", "-").replace("–", "-").strip()
    if not s or not _AMOUNT_RE.match(s):
        return None
    s = s.replace("±", "").replace("+", "").replace(" ", "")
    if s in ("", "-"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def uo_rows_from_html_table(table: str) -> dict[int, tuple[str, float | None]]:
    """En HTML-tabell -> {UO-nummer: (namn, sista beloppet på raden)}.

    Raden känns igen på att första cellen är ett tal 1-27 och andra cellen är text. Beloppet är
    SISTA numeriska cellen, alltså den absoluta ramen i tabeller som först visar en avvikelse.
    """
    out: dict[int, tuple[str, float | None]] = {}
    for row in _ROW_RE.findall(table):
        cs = _cells(row)
        if len(cs) < 2 or not re.fullmatch(r"\d{1,2}", cs[0]):
            continue
        n = int(cs[0])
        if not 1 <= n <= 27 or n in out:
            continue
        name = cs[1]
        if not name or parse_amount(name) is not None:
            continue
        amounts = [a for a in (parse_amount(c) for c in cs[2:]) if a is not None]
        out[n] = (name, amounts[-1] if amounts else None)
    return out


def html_uo_tables(html: str) -> list[tuple[str, dict[int, tuple[str, float | None]]]]:
    """Alla tabeller med hela UO-indelningen, som (rubrik, rader).

    Rubriken står före tabellen i nyare betänkanden och som tabellens egna första rader i de
    äldre (t.ex. bet. 2013/14:FiU1 bilaga 2). Båda ställena läses, så samma sökning träffar
    hela serien.
    """
    found: list[tuple[str, dict[int, tuple[str, float | None]]]] = []
    for m in _TABLE_RE.finditer(html):
        rows = uo_rows_from_html_table(m.group(0))
        if len(rows) < 27:
            continue
        lead = [line for line in htmlmod.unescape(
            re.sub(r"<[^>]+>", "\n", html[max(0, m.start() - 1500):m.start()])
        ).split("\n") if line.strip()]
        head = [" ".join(c for c in _cells(row) if c) for row in _ROW_RE.findall(m.group(0))[:6]]
        caption = " / ".join(
            [re.sub(r"\s+", " ", line).strip() for line in lead[-4:]] + head
        )
        found.append((caption, rows))
    return found


def uo_rows_from_pdf_page(
    page_text: str, start_at: int = 0
) -> dict[int, tuple[str, float | None]]:
    """En PDF-sidas text -> {UO-nummer: (namn, sista beloppet)}.

    Två layouter förekommer i serien: numret på egen rad (bet. 2021/22:FiU1) och numret först på
    namnraden (bet. 2014/15:FiU1). Båda läses. Ett UO börjar BARA där raden bär exakt nästa
    väntade nummer, och där resten av raden är text och inte fler siffror. Annars skulle ett
    belopp som "12 198 574" starta utgiftsområde 12. start_at bär räkningen över en sidbrytning.
    """
    out: dict[int, tuple[str, float | None]] = {}
    current: int | None = None
    name_parts: list[str] = []
    amounts: list[float] = []
    done = False

    def close() -> None:
        if current is not None:
            out[current] = (" ".join(name_parts).strip(), amounts[-1] if amounts else None)

    def marker(line: str, expected: int) -> str | None:
        """Radens text efter numret om raden startar `expected`, annars None."""
        if expected > 27:
            return None
        m = re.match(rf"^{expected}(?:\s+(\D.*))?$", line)
        return (m.group(1) or "") if m else None

    for raw_line in page_text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        rest = marker(line, (current if current is not None else start_at) + 1)
        if rest is not None:
            close()
            current = (current if current is not None else start_at) + 1
            name_parts, amounts, done = ([rest] if rest else []), [], False
            continue
        if current is None or done:
            continue
        amount = parse_amount(line)
        if amount is None:
            if amounts:
                done = True                     # texten efter beloppen tillhör nästa rad
            else:
                name_parts.append(line)         # namnet står före beloppen
        else:
            amounts.append(amount)
    close()
    return out


def pdf_uo_table(pdf_path: str, caption: str) -> dict[int, tuple[str, float | None]]:
    """Tabellen under en given rubrik i en PDF, sammanfogad över sidbrytningar."""
    import fitz  # endast det här verktyget, aldrig pipelinen

    doc = fitz.open(pdf_path)
    try:
        want = caption_key(caption)
        pages = [i for i in range(doc.page_count) if want in caption_key(doc[i].get_text())]
        if not pages:
            raise ValueError(f"Hittade inte rubriken {caption!r} i {pdf_path}")
        rows: dict[int, tuple[str, float | None]] = {}
        for i in range(pages[0], min(pages[0] + 4, doc.page_count)):
            rows.update(uo_rows_from_pdf_page(doc[i].get_text(), start_at=max(rows, default=0)))
            if len(rows) >= 27:
                break
        return rows
    finally:
        doc.close()


# --- Hämtning ---------------------------------------------------------------------------

def _client() -> httpx.Client:
    return httpx.Client(timeout=120, headers=_UA, follow_redirects=True)


def fetch_status(dok: str, client: httpx.Client) -> dict[str, Any]:
    """dokumentstatus-JSON, cachad under data/raw/ (idempotent, stannar lokalt)."""
    path = CACHE_DIR / f"{dok}.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    resp = client.get(f"{BASE}/dokumentstatus/{dok}.json")
    resp.raise_for_status()
    payload = resp.json()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return payload


def fetch_pdf(status: dict[str, Any], dok: str, client: httpx.Client) -> str:
    path = CACHE_DIR / f"{dok}.pdf"
    if path.exists():
        return str(path)
    bilagor = (status["dokumentstatus"].get("dokbilaga") or {}).get("bilaga") or []
    if isinstance(bilagor, Mapping):
        bilagor = [bilagor]
    if not bilagor:
        raise ValueError(f"{dok} saknar bilaga att hämta")
    path.parent.mkdir(parents=True, exist_ok=True)
    with client.stream("GET", bilagor[0]["fil_url"]) as resp:
        resp.raise_for_status()
        with path.open("wb") as fh:
            for chunk in resp.iter_bytes(1 << 20):
                fh.write(chunk)
    return str(path)


def rambeslut_punkt(status: dict[str, Any], budget_year: int) -> tuple[str, str]:
    """(vinnare, meningen om utgiftsramarna) ur beslutspunkten. Hård fail om den saknas."""
    items = (status["dokumentstatus"].get("dokutskottsforslag") or {}).get("utskottsforslag") or []
    if isinstance(items, Mapping):
        items = [items]
    pattern = re.compile(
        r"(?:beslutar om|fastställer)[^.]{0,200}utgiftsområden?a?[^.]{0,160}\.", re.I
    )
    for item in items:
        body = _text(item.get("forslag") or "")
        for match in pattern.finditer(body):
            if str(budget_year) in match.group(0):
                return str(item.get("vinnare") or ""), match.group(0)
    raise ValueError(f"Hittade ingen ram-mening för {budget_year}")


def _check_adopted(budget_year: int, status: dict[str, Any]) -> list[str]:
    """Dokumentets egen vinnare och ram-mening mot ADOPTED-raden. Tomt = de stämmer."""
    spec = ADOPTED[budget_year]
    winner, sentence = rambeslut_punkt(status, budget_year)
    problems = []
    if winner != spec.winner:
        problems.append(f"{budget_year}: vinnare {winner!r} != {spec.winner!r}")
    if spec.sentence not in sentence:
        problems.append(f"{budget_year}: ram-meningen {sentence!r} saknar {spec.sentence!r}")
    return problems


def decided_frame(
    budget_year: int, client: httpx.Client
) -> tuple[dict[int, float], dict[int, str], list[str]]:
    """({UO -> belopp i mnkr}, {UO -> namn}, avvikelser mot ADOPTED) för ett budgetår."""
    spec = ADOPTED[budget_year]
    dok = dok_id(budget_year)
    status = fetch_status(dok, client)
    problems = _check_adopted(budget_year, status)
    if spec.source == "html":
        html = status["dokumentstatus"]["dokument"].get("html") or ""
        want = caption_key(spec.caption)
        hits = [rows for caption, rows in html_uo_tables(html) if want in caption_key(caption)]
        if not hits:
            raise ValueError(f"{budget_year}: hittade inte tabellen {spec.caption!r} i {dok}")
        rows = hits[0]
    else:
        rows = pdf_uo_table(fetch_pdf(status, dok, client), spec.caption)
    missing = [n for n in range(1, 28) if rows.get(n, (None, None))[1] is None]
    if missing:
        raise ValueError(f"{budget_year}: belopp saknas för UO {missing}")
    # "Sista numeriska cellen" är ramen i bilagornas layout (avvikelse, sedan förslag). Skulle en
    # tabell lägga kolumnerna tvärtom fångar parsern en AVVIKELSE i stället, och avvikelser är
    # negativa eller noll i flera utgiftsområden varje år. En beslutad ram är däremot positiv i
    # varje utgiftsområde, så grinden nedan skiljer de två fallen utan att sätta något tal.
    nonpositive = [n for n in range(1, 28) if rows[n][1] <= 0]
    if nonpositive:
        raise ValueError(
            f"{budget_year}: UO {nonpositive} har belopp <= 0 — läste parsern en avvikelsekolumn?"
        )
    divisor = 1000.0 if spec.unit == "tkr" else 1.0
    amounts = {n: round(rows[n][1] / divisor) for n in range(1, 28)}
    names = {n: rows[n][0] for n in range(1, 28)}
    return amounts, names, problems


def uo_structure(budget_year: int, client: httpx.Client) -> dict[int, str]:
    """{UO-nummer -> namn} ur budgetårets FiU1. a1-gränsen mäts på den här.

    Gränsen frågar efter INDELNINGEN, inte efter vilken tabell som beslutades, så vilken som
    helst av betänkandets rambeslutstabeller duger. Den första fullständiga tas.
    """
    status = fetch_status(dok_id(budget_year), client)
    tables = html_uo_tables(status["dokumentstatus"]["dokument"].get("html") or "")
    if tables:
        return {n: name for n, (name, _amount) in tables[0][1].items()}
    spec = ADOPTED.get(budget_year)
    if spec is None:
        raise ValueError(f"{budget_year}: ingen HTML-tabell och ingen känd PDF-rubrik")
    rows = pdf_uo_table(fetch_pdf(status, dok_id(budget_year), client), spec.caption)
    return {n: name for n, (name, _amount) in rows.items()}


def chamber_motions(start: int, end: int, client: httpx.Client, delay: float = 0.15) -> dict[str, int]:
    """Kammarens SAMTLIGA motioner per utskott i fönstret (ingen partifiltrering)."""
    out: dict[str, int] = {}
    for org in config.mappings()["committee_to_category"]:
        query = f"doktyp=mot&org={org}&from={start}-01-01&tom={end}-12-31&utformat=json&sz=1"
        resp = client.get(f"{BASE}/dokumentlista/?{query}")
        resp.raise_for_status()
        out[org] = int(resp.json()["dokumentlista"]["@traffar"])
        time.sleep(delay)
    return out


def party_committee_counts(year: int, client: httpx.Client, delay: float = 0.1) -> dict[str, int]:
    """{'parti:utskott' -> antal motioner} för ETT kalenderår. Grinden a2 mäts på den här."""
    out: dict[str, int] = {}
    for party in config.party_codes():
        for org in config.mappings()["committee_to_category"]:
            query = (f"doktyp=mot&parti={party}&org={org}"
                     f"&from={year}-01-01&tom={year}-12-31&utformat=json&sz=1")
            resp = client.get(f"{BASE}/dokumentlista/?{query}")
            resp.raise_for_status()
            out[f"{party}:{org}"] = int(resp.json()["dokumentlista"]["@traffar"])
            time.sleep(delay)
    return out


# --- Körlägen ---------------------------------------------------------------------------

def run_window(years: Iterable[int]) -> dict[str, Any]:
    """Båda gränserna, år för år, plus fönstret de ger. Skriver bevisfilen."""
    years = list(years)
    a1: dict[str, Any] = {}
    a2: dict[str, Any] = {}
    with _client() as client:
        for year in years:
            try:
                names = uo_structure(year, client)
                row: dict[str, Any] = {
                    "dok_id": dok_id(year), "uo_count": len(names), "ok": len(names) == 27,
                    "names": {str(n): names[n] for n in sorted(names)},
                }
                if year in ADOPTED:
                    winner, sentence = rambeslut_punkt(fetch_status(dok_id(year), client), year)
                    row["adopted"] = {"vinnare": winner, "mening": sentence,
                                      "tabell": ADOPTED[year].caption,
                                      "avvikelser": _check_adopted(year, fetch_status(dok_id(year), client))}
                a1[str(year)] = row
            except Exception as exc:                      # noqa: BLE001 - bevisfilen ska bära felet
                a1[str(year)] = {"ok": False, "error": str(exc)}
            print(f"a1 {year}: {'OK' if a1[str(year)]['ok'] else a1[str(year)].get('error', 'FEL')}",
                  flush=True)
        for year in years:
            counts = party_committee_counts(year, client)
            zeros = sorted(k for k, v in counts.items() if v == 0)
            a2[str(year)] = {"ok": not zeros, "zeros": zeros, "counts": counts}
            print(f"a2 {year}: {'OK' if not zeros else 'nollor: ' + ', '.join(zeros)}", flush=True)

    a1_bound = min((int(y) for y, r in a1.items() if r["ok"]), default=None)
    a2_bound = min((int(y) for y, r in a2.items() if r["ok"]), default=None)
    start = max(b for b in (a1_bound, a2_bound) if b is not None)
    out = {
        "tested_years": years,
        "a1": {"bound": a1_bound, "test": "FiU1:s rambeslutstabell listar utgiftsområde 1-27",
               "per_year": a1},
        "a2": {"bound": a2_bound,
               "test": "alla åtta partier har minst en motion i varje utskott mappningen använder",
               "per_year": a2},
        "window": {"start": start, "end": max(years)},
    }
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    (EVIDENCE_DIR / "fonster.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    print(f"\nFönster: {start}-{max(years)}  (a1-gräns {a1_bound}, a2-gräns {a2_bound})")
    return out


def run_frames(years: Iterable[int]) -> None:
    """Beslutade ramar per budgetår som ett YAML-block att klistra in i configen."""
    with _client() as client:
        print("  decided_frames:")
        for year in years:
            amounts, names, problems = decided_frame(year, client)
            spec = ADOPTED[year]
            for problem in problems:
                print(f"# AVVIKELSE {problem}", file=sys.stderr)
            print(f"    {year}:")
            print(f'      source_ref: "riksdag:bet:{dok_id(year)} ({spec.caption})"')
            print(f'      adopted: "{spec.winner}"')
            for n in range(1, 28):
                print(f"      UO{n}: {amounts[n]}     # {names[n]}")


def run_chamber(start: int, end: int) -> None:
    """Kammarens motionsfördelning över fönstret som ett YAML-block."""
    with _client() as client:
        counts = chamber_motions(start, end, client)
    print("  chamber_motions:")
    print(f'    source_ref: "riksdag:dokumentlista:doktyp=mot per org, '
          f'{start}-01-01/{end}-12-31 (kammarens samtliga motioner)"')
    print(f'    period: "{start}-01-01/{end}-12-31"')
    print("    committees:")
    for org, n in counts.items():
        print(f"      {org}: {n}")


_CONFIG_HEADER = '''# Rösta — FÖRANKRINGEN för delpoäng A (ADR 0005). AUTOGENERERAD, redigera aldrig för hand.
#
#     python -m pipeline.tools.a_forankring_transcribe --config
#
# A frågar hur stor andel av sin kraft ett parti lägger på en kategori. Efter ADR 0005 mäts den
# andelen mot hur stor andel kategorin normalt fått under ett historiskt fönster, inte mot de sju
# andra partierna. Nollpunkten ligger alltså i tid och inte tvärs partier.
#
#   a1  kategorins andel av de BESLUTADE utgiftsramarna i bet. FiU1, som medel över fönstret.
#       Regeringens förslag förkastas som förankring: det är ett blocks förslag varje enskilt år.
#   a2  kategorins andel av kammarens SAMTLIGA motioner under fönstret. Den poolade
#       partikammaren förkastas: den är de åtta partierna viktade efter hur mycket var och en
#       skriver, alltså samma fältmått som ADR 0005 punkt 2 avvisar.
#
# Beloppen är transkriberade ur officiella källor, aldrig imputerade eller jämkade, och varje år
# citerar sin tabell. Det finns INGEN runtime-parser: A är tyngsta delpoängen och får aldrig
# kunna korrumperas av en bräcklig parser (samma regel som config/budget_ramar.yaml).
# `--audit` kör configen mot riksdagen igen och faller på minsta avvikelse.
#
# Vilken tabell som är den beslutade läses ur betänkandet självt: beslutspunktens `vinnare` och
# meningen om utgiftsramarna. Tre år i fönstret avgjordes inte på regeringens förslag:
# 2015 på allianspartiernas reservation, 2019 på reservation 5 (M, KD) och 2022 på utskottets
# eget förslag i bilaga 4. `adopted` bär vinnaren per år.
'''


def write_window_report() -> None:
    """Renderar docs/done/a_forankring/fonster.md ur bevisfilen. Rör inte nätet."""
    ev = json.loads((EVIDENCE_DIR / "fonster.json").read_text(encoding="utf-8"))
    years = ev["tested_years"]
    rows = ["# Förankringsfönstret för delpoäng A (ADR 0005 punkt 7)", "",
            "> AUTOGENERERAD av `python -m pipeline.tools.a_forankring_transcribe --window`.",
            "> Redigera aldrig för hand. Talen är utfallet av två gränser som skrevs FÖRE",
            "> hämtningen, och de har inte rörts efteråt.", "",
            f"Fönstret blev **{ev['window']['start']}-{ev['window']['end']}**: "
            f"a1-gränsen ger {ev['a1']['bound']}, a2-gränsen ger {ev['a2']['bound']}, "
            "och fönstret börjar vid den senare av dem.", "",
            "## Gränserna", "",
            f"- **a1**: {ev['a1']['test']}.",
            f"- **a2**: {ev['a2']['test']}.", "",
            "## År för år", "",
            "| År | a1 | a2 | a2:s nollor |", "| --- | --- | --- | --- |"]
    for year in years:
        a1 = ev["a1"]["per_year"].get(str(year), {})
        a2 = ev["a2"]["per_year"].get(str(year), {})
        a1_cell = "ja" if a1.get("ok") else f"nej ({a1.get('error', 'okänt')})"
        zeros = ", ".join(a2.get("zeros", [])) or "-"
        rows.append(f"| {year} | {a1_cell} | {'ja' if a2.get('ok') else 'nej'} | {zeros} |")

    rows += ["", "## Utgiftsområdenas namn per år", "",
             "Namnen grindar inte (se verktygets modulkommentar). De står här för att en",
             "omdöpning ska synas i efterhand.", "", "| UO | " +
             " | ".join(str(y) for y in years if ev["a1"]["per_year"].get(str(y), {}).get("ok")) +
             " |", "| --- |" + " --- |" * sum(
                 1 for y in years if ev["a1"]["per_year"].get(str(y), {}).get("ok"))]
    ok_years = [y for y in years if ev["a1"]["per_year"].get(str(y), {}).get("ok")]
    for n in range(1, 28):
        cells = [ev["a1"]["per_year"][str(y)]["names"].get(str(n), "") for y in ok_years]
        rows.append(f"| {n} | " + " | ".join(cells) + " |")

    rows += ["", "## Den beslutade ramen per budgetår", "",
             "Vilken tabell som gäller läses ur betänkandet självt, aldrig av gissning.", "",
             "| År | Vinnare | Tabell |", "| --- | --- | --- |"]
    for year in ok_years:
        adopted = ev["a1"]["per_year"][str(year)].get("adopted")
        if adopted:
            rows.append(f"| {year} | {adopted['vinnare']} | {adopted['tabell']} |")
    (EVIDENCE_DIR / "fonster.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"Skrev {EVIDENCE_DIR / 'fonster.md'}")


def run_config() -> None:
    """Skriver hela config/a_forankring.yaml ur källan. Fönstret läses ur bevisfilen."""
    evidence = json.loads((EVIDENCE_DIR / "fonster.json").read_text(encoding="utf-8"))
    start, end = int(evidence["window"]["start"]), int(evidence["window"]["end"])
    lines = [_CONFIG_HEADER, "version: 1", "", "window:",
             f"  start: {start}", f"  end: {end}",
             f'  a1_bound: {evidence["a1"]["bound"]}      # {evidence["a1"]["test"]}',
             f'  a2_bound: {evidence["a2"]["bound"]}      # {evidence["a2"]["test"]}',
             '  evidence: "docs/done/a_forankring/fonster.json"', "", "a1:",
             "  unit: mnkr", "  decided_frames:"]
    with _client() as client:
        for year in range(start, end + 1):
            amounts, names, problems = decided_frame(year, client)
            for problem in problems:
                raise ValueError(f"avvikelse mot källan: {problem}")
            spec = ADOPTED[year]
            lines += [f"    {year}:",
                      f'      source_ref: "riksdag:bet:{dok_id(year)} ({spec.caption})"',
                      f'      adopted: "{spec.winner}"']
            lines += [f"      UO{n}: {amounts[n]}     # {names[n]}" for n in range(1, 28)]
        counts = chamber_motions(start, end, client)
    lines += ["", "a2:", "  chamber_motions:",
              f'      source_ref: "riksdag:dokumentlista:doktyp=mot per org, '
              f'{start}-01-01/{end}-12-31 (kammarens samtliga motioner)"'.replace("      ", "    ", 1),
              f'    period: "{start}-01-01/{end}-12-31"', "    committees:"]
    lines += [f"      {org}: {n}" for org, n in counts.items()]
    path = ROOT / "config" / "a_forankring.yaml"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Skrev {path} — fönster {start}-{end}, {end - start + 1} budgetår")


def run_audit() -> int:
    """config/a_forankring.yaml mot källan. Exit 1 vid minsta avvikelse."""
    cfg = config.a_forankring()
    window = cfg["window"]
    start, end = int(window["start"]), int(window["end"])
    frames = cfg["a1"]["decided_frames"]
    problems: list[str] = []
    with _client() as client:
        for year in range(start, end + 1):
            if year not in frames:
                problems.append(f"{year}: saknas i configen")
                continue
            amounts, _names, spec_problems = decided_frame(year, client)
            problems.extend(spec_problems)
            for n in range(1, 28):
                have = frames[year].get(f"UO{n}")
                if have != amounts[n]:
                    problems.append(f"{year}/UO{n}: config {have} != källa {amounts[n]}")
            print(f"{year}: {len(amounts)} UO kontrollerade", flush=True)
        counts = chamber_motions(start, end, client)
    for org, n in counts.items():
        have = cfg["a2"]["chamber_motions"]["committees"].get(org)
        if have != n:
            problems.append(f"kammaren/{org}: config {have} != källa {n}")
    for problem in problems:
        print(f"AVVIKELSE {problem}")
    print("\nconfig/a_forankring.yaml matchar källan" if not problems
          else f"\n{len(problems)} avvikelser")
    return 1 if problems else 0


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--window", action="store_true", help="kör fönstrets två gränser")
    parser.add_argument("--frames", action="store_true", help="beslutade ramar -> YAML")
    parser.add_argument("--chamber", action="store_true", help="kammarens motioner -> YAML")
    parser.add_argument("--config", action="store_true", help="skriv config/a_forankring.yaml")
    parser.add_argument("--report", action="store_true", help="rendera bevisfilens .md på nytt")
    parser.add_argument("--audit", action="store_true", help="config mot källa (default)")
    parser.add_argument("--from", dest="start", type=int, default=2008)
    parser.add_argument("--to", dest="end", type=int, default=2025)
    args = parser.parse_args()

    if args.window:
        run_window(range(args.start, args.end + 1))
    elif args.frames:
        run_frames(range(args.start, args.end + 1))
    elif args.chamber:
        run_chamber(args.start, args.end)
    elif args.config:
        run_config()
    elif args.report:
        write_window_report()
    else:
        raise SystemExit(run_audit())


if __name__ == "__main__":
    main()
