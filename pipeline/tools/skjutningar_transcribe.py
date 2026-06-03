"""Reproducerar och AUDITERAR config/skjutningar.yaml mot Polisens per-års-PDF:er.

Polisens bekräftade skjutningar publiceras bara som PDF per polisregion och år. Det här
verktyget laddar ned varje års-PDF, extraherar den nationella årstotalen ur Skjutningar-tabellen
och KORSVERIFIERAR den (summan av polisregionernas årstotaler == PDF:ens nationella Totalt-rad).
Sedan jämförs resultatet mot de pinnade värdena i config/skjutningar.yaml.

Kör manuellt (kräver PyMuPDF/fitz, ej en pipeline-/test-dependens):

    python -m pipeline.tools.skjutningar_transcribe

Exit 0 = config matchar live-PDF:erna; exit 1 = avvikelse (årssiffra ändrad i källan, eller
en PDF-URL som behöver uppdateras). Detta är transkriberingens revisionsspår — ingen
runtime-parser körs i själva pipelinen (den läser bara den pinnade configen).
"""

from __future__ import annotations

import re
import sys

import httpx

from .. import config

_UA = {"User-Agent": "rosta-datapipeline/0.1 (civic-tech; official swedish open data)"}


def national_total(pdf_text: str) -> tuple[int, int]:
    """(nationell Totalt-rad-årstal, summa av regionernas årstotaler) ur Skjutningar-tabellen.

    Första tabellen = allt före 'Avlidna'. Hoppar titel + kolumnrubriker via första 'Totalt'.
    Resten är 7 regionrader (namn + 12 månader + årstotal) + en nationell Totalt-rad (13 tal).
    """
    first = pdf_text.split("Avlidna")[0]
    after = first.split("Totalt", 1)[1]
    ints = [int(x) for x in re.findall(r"-?\d+", after)]
    if len(ints) < 26 or len(ints) % 13 != 0:
        raise ValueError(f"oväntad PDF-struktur: {len(ints)} heltal (förväntade multipel av 13)")
    national = ints[-1]                       # nationella Totalt-radens årstal
    region_annuals = ints[:-13][12::13]       # var 13:e tal i regionblocket = regionens årstotal
    return national, sum(region_annuals)


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    try:
        import fitz  # PyMuPDF — endast detta verktyg, inte pipelinen
    except ImportError:
        raise SystemExit("PyMuPDF (fitz) krävs för transkriberingsverktyget: pip install pymupdf") from None

    cfg = config.skjutningar()
    pinned = {int(y): e["value"] for y, e in cfg["years"].items()}
    sources = {int(y): e["source"] for y, e in cfg["years"].items()}

    print("== Auditerar config/skjutningar.yaml mot Polisens PDF:er ==")
    mismatches = 0
    with httpx.Client(headers=_UA, follow_redirects=True, timeout=90) as c:
        for year in sorted(pinned):
            resp = c.get(sources[year])
            resp.raise_for_status()
            text = fitz.open(stream=resp.content, filetype="pdf")[0].get_text("text")
            nat, region_sum = national_total(text)
            ok_cross = nat == region_sum
            ok_pin = nat == pinned[year]
            flag = "OK" if (ok_cross and ok_pin) else "AVVIKELSE"
            print(f"  {year}: PDF={nat:>4} regionsumma={region_sum:>4} config={pinned[year]:>4}  "
                  f"[{flag}]")
            if not (ok_cross and ok_pin):
                mismatches += 1
    if mismatches:
        raise SystemExit(f"\n{mismatches} avvikelse(r) — uppdatera config/skjutningar.yaml.")
    print(f"\nAlla {len(pinned)} år matchar live-PDF:erna och korsverifieringen.")


if __name__ == "__main__":
    main()
