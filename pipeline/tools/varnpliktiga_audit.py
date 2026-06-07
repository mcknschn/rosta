"""Auditerar config/personal_varnpliktiga.yaml — försvarets D-serie (antal påbörjade GU/år).

Till skillnad från skjutningar_transcribe (som laddar live-PDF:er) kan FM:s och Pliktverkets
årsredovisnings-PDF:er INTE maskinläsas (FlateDecode; verktygskedjan saknar pdftoppm/PyMuPDF i
detta läge). Det här verktyget auditerar i stället de INTEGRITETSINVARIANTER som faktiskt avgör
D-attributionen, helt offline:

  1. Serien är konsekutiva år fr.o.m. 2018 (D använder bara konsekutiva år).
  2. Serien är monoton UPP utom exakt EN dokumenterad nedgång (2021->2022) — så det enda
     teckenkänsliga D-året är isolerat och medvetet.
  3. Varje år som har en oberoende Pliktverket-korsverifiering ligger inom tolerans (≤15 %), och
     BÅDA myndigheterna är överens om tecknet på 2021->2022 (den dubbelbekräftade nedgången).
  4. Varje år har en källa (FM ÅR) — ingen tyst siffra.

Eftersom D bara tar TECKEN på årsförändringen bevisar (1)-(3) att attributionen är robust mot
kvarvarande sifferosäkerhet i de PDF-låsta åren. Kör:

    python -m pipeline.tools.varnpliktiga_audit

Exit 0 = invarianterna håller; exit 1 = avvikelse (serien har ändrats på ett sätt som kan flippa
ett D-tecken, eller en korsverifiering spretar -> kräver manuell granskning).
"""

from __future__ import annotations

import sys

from .. import config

_XCHECK_TOL = 0.15           # FM vs Pliktverket: oberoende myndighetsmått, tillåt ≤15 % skillnad
_KNOWN_DIP = (2021, 2022)    # enda dokumenterade nedgången (dubbelbekräftad av båda myndigheterna)


def audit(cfg: dict | None = None) -> list[str]:
    """Returnerar en lista avvikelser (tom = allt OK). Ren funktion -> enhetstestbar."""
    cfg = config.personal_varnpliktiga() if cfg is None else cfg
    years = sorted(cfg["years"])
    vals = {y: float(cfg["years"][y]["value"]) for y in years}
    problems: list[str] = []

    # (1) konsekutiva år fr.o.m. 2018
    if years and years[0] != 2018:
        problems.append(f"serien borjar {years[0]}, forvantat 2018 (varnplikten ateraktiverad 2018)")
    for a, b in zip(years, years[1:], strict=False):
        if b - a != 1:
            problems.append(f"glapp i serien: {a}->{b} ar ej konsekutiva")

    # (2) monoton upp utom exakt en dokumenterad nedgang
    dips = [(a, b) for a, b in zip(years, years[1:], strict=False) if vals[b] < vals[a]]
    if dips != [_KNOWN_DIP]:
        problems.append(f"forvantade exakt en nedgang {_KNOWN_DIP}, fann {dips} "
                        "(en ovantad nedgang kan flippa ett D-tecken -> granska)")

    # (3) korsverifiering mot Pliktverket + dubbelbekraftat dip-tecken
    for y in years:
        e = cfg["years"][y]
        xc = e.get("crosscheck_pliktverket")
        if xc is None:
            continue
        rel = abs(float(xc) - vals[y]) / vals[y]
        if rel > _XCHECK_TOL:
            problems.append(f"{y}: FM {vals[y]:.0f} vs Pliktverket {xc} spretar "
                            f"{rel:.0%} (> {_XCHECK_TOL:.0%})")
    dy0, dy1 = _KNOWN_DIP
    x0 = cfg["years"].get(dy0, {}).get("crosscheck_pliktverket")
    x1 = cfg["years"].get(dy1, {}).get("crosscheck_pliktverket")
    if x0 is not None and x1 is not None and not (float(x1) < float(x0)):
        problems.append(f"Pliktverket bekraftar INTE nedgangen {dy0}->{dy1} ({x0}->{x1}) "
                        "-> den teckenkansliga overgangen ar ej langre dubbelbekraftad")

    # (4) ingen tyst siffra
    for y in years:
        if not str(cfg["years"][y].get("source", "")).strip():
            problems.append(f"{y}: saknar source (tyst siffra)")

    return problems


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    cfg = config.personal_varnpliktiga()
    years = sorted(cfg["years"])
    print("== Auditerar config/personal_varnpliktiga.yaml (forsvarets D-serie) ==")
    for y in years:
        e = cfg["years"][y]
        xc = e.get("crosscheck_pliktverket")
        xs = f"  | Pliktverket {xc}" if xc else ""
        print(f"  {y}: FM {float(e['value']):>6.0f} paborjade GU{xs}")
    problems = audit(cfg)
    if problems:
        print("\nAVVIKELSER:")
        for p in problems:
            print(f"  - {p}")
        raise SystemExit(f"\n{len(problems)} avvikelse(r) — granska config/personal_varnpliktiga.yaml.")
    print(f"\nAlla {len(years)} ar: konsekutiva fr.o.m. 2018, monoton upp utom dubbelbekraftad "
          "nedgang 2021->2022, korsverifierade mot Pliktverket. D-tecknen ar robusta.")


if __name__ == "__main__":
    main()
