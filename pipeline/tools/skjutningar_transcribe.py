"""Reproducerar och AUDITERAR config/skjutningar_sprangningar.yaml mot Polisens per-års-PDF:er.

Polisens bekräftade skjutningar OCH sprängningar publiceras bara som PDF per polisregion och år.
Det här verktyget laddar ned varje års-PDF (båda serierna), extraherar den nationella årstotalen
ur den första tabellen och KORSVERIFIERAR den (summan av polisregionernas årstotaler == PDF:ens
nationella Totalt-rad). Sedan jämförs varje komponent mot de pinnade värdena i configen.

Kör manuellt (kräver PyMuPDF/fitz, ej en pipeline-/test-dependens):

    python -m pipeline.tools.skjutningar_transcribe

Exit 0 = configen matchar live-PDF:erna; exit 1 = avvikelse (årssiffra ändrad i källan, eller en
PDF-URL som behöver uppdateras). Detta är transkriberingens revisionsspår — ingen runtime-parser
körs i själva pipelinen (den läser bara den pinnade configen).
"""

from __future__ import annotations

import re
import sys

import httpx

from .. import config

_UA = {"User-Agent": "rosta-datapipeline/0.1 (civic-tech; official swedish open data)"}


def national_total(pdf_text: str) -> tuple[int, int]:
    """(nationell Totalt-rad-årstal, summa av regionernas årstotaler) ur PDF:ens FÖRSTA tabell.

    Etikett-agnostisk (funkar för både Skjutningar- och Detonationer-tabeller): splittar på 'Totalt'.
    parts[1] = regionraderna (namn + 12 månader + årstotal), parts[2] inleds med Totalt-radens
    13 tal (12 månader + årstal). Trailing sektioner (Avlidna/Skadade) påverkar inte.
    """
    parts = pdf_text.split("Totalt")
    if len(parts) < 3:
        raise ValueError("oväntad PDF-struktur: < 2 Totalt-sektioner")
    region = [int(x) for x in re.findall(r"-?\d+", parts[1])]
    totalt_row = [int(x) for x in re.findall(r"-?\d+", parts[2])][:13]
    if len(region) % 13 != 0 or len(totalt_row) < 13:
        raise ValueError(f"oväntad struktur: region={len(region)} totalt={len(totalt_row)}")
    return totalt_row[12], sum(region[12::13])


def _verify(client: httpx.Client, fitz: object, url: str, expected: int) -> tuple[int, bool, bool]:
    resp = client.get(url)
    resp.raise_for_status()
    text = fitz.open(stream=resp.content, filetype="pdf")[0].get_text("text")
    nat, region_sum = national_total(text)
    return nat, nat == region_sum, nat == expected


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    try:
        import fitz  # PyMuPDF — endast detta verktyg, inte pipelinen
    except ImportError:
        raise SystemExit("PyMuPDF (fitz) krävs för transkriberingsverktyget: pip install pymupdf") from None

    cfg = config.skjutningar_sprangningar()
    print("== Auditerar config/skjutningar_sprangningar.yaml mot Polisens PDF:er ==")
    mismatches = 0
    with httpx.Client(headers=_UA, follow_redirects=True, timeout=90) as c:
        for year in sorted(cfg["years"]):
            e = cfg["years"][year]
            sk, sk_x, sk_p = _verify(c, fitz, e["skjutningar_source"], e["skjutningar"])
            sp, sp_x, sp_p = _verify(c, fitz, e["sprangningar_source"], e["sprangningar"])
            ok = sk_x and sk_p and sp_x and sp_p
            print(f"  {year}: skjut={sk:>4}(cfg {e['skjutningar']:>4}) spräng={sp:>4}"
                  f"(cfg {e['sprangningar']:>4}) summa={sk + sp:>4}  [{'OK' if ok else 'AVVIKELSE'}]")
            if not ok:
                mismatches += 1
    if mismatches:
        raise SystemExit(f"\n{mismatches} avvikelse(r) — uppdatera config/skjutningar_sprangningar.yaml.")
    print(f"\nAlla {len(cfg['years'])} år matchar live-PDF:erna och korsverifieringen "
          "(båda komponenterna).")


if __name__ == "__main__":
    main()
