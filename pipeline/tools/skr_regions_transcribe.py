"""Transkriberingsaid: SKR-CSV (Styren i regioner 1994-2022) -> mappings.yaml-block.

ENGÅNGSVERKTYG, inte en del av scoring-pipelinen. Läser SKR:s officiella öppna-data-CSV
och skriver ett färdigt subnational_governance.regions-block (kanoniska partikoder,
kontrollsummor per valår). Resultatet klistras in som STATISK config i config/mappings.yaml
(källan till sanning) — ingen runtime-parser, jfr config/budget_ramar.yaml. Verktyget finns
versionsstyrt så transkriberingen är reproducerbar/granskningsbar av vem som helst som
hämtar samma officiella fil.

Hämta källfilen (gitignorad, stannar lokalt i data/raw/):
  Dataset: SKR "Styren i regioner 1994-2022", catalog.skl.se dataset 80
  CSV:     https://catalog.skl.se/store/1/resource/123
  curl -sL "https://catalog.skl.se/store/1/resource/123" -o data/raw/skr/regioner_1994_2022.csv

Kör:  python -m pipeline.tools.skr_regions_transcribe
2022-perioden korsverifieras separat mot "Styren i regioner efter valet 2022" (xlsx),
som matchar 1994-2022-filen exakt (21/21 regioner). Endast de 8 riksdagspartierna tas med
i leading_parties; lokala partier (ÖP/"Övrigt parti") noteras i local_parties men poängsätts ej.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

CSV_PATH = Path("data/raw/skr/regioner_1994_2022.csv")
YEARS = ("2014", "2018", "2022")
TERM = {"2014": "2014-2018", "2018": "2018-2022", "2022": "2022-2026"}
PARTY_COLS = ["M", "C", "L/FP", "KD", "S", "V", "MP", "SD"]
NORM = {"L/FP": "L"}                                   # SKR:s historiska kod -> kanon (fp->L)
CANON_ORDER = ["S", "M", "SD", "C", "V", "KD", "L", "MP"]  # categories.yaml-ordning

# Unik nyckel i regionnamnet -> (SCB läns-/regionkod, kanoniskt namn). Namnen växlar mellan
# åren (landsting -> region); nyckeln är ett unikt substräng som finns i alla varianter.
KEY_TO_REGION = [
    ("Stockholm", "01", "Region Stockholm"),
    ("Uppsala", "03", "Region Uppsala"),
    ("Sörmland", "04", "Region Sörmland"),
    ("Söderman", "04", "Region Sörmland"),
    ("Östergötland", "05", "Region Östergötland"),
    ("Jönköping", "06", "Region Jönköpings län"),
    ("Kronoberg", "07", "Region Kronoberg"),
    ("Kalmar", "08", "Region Kalmar län"),
    ("Gotland", "09", "Region Gotland"),
    ("Blekinge", "10", "Region Blekinge"),
    ("Skåne", "12", "Region Skåne"),
    ("Halland", "13", "Region Halland"),
    ("Västra Göta", "14", "Västra Götalandsregionen"),
    ("Värmland", "17", "Region Värmland"),
    ("Örebro", "18", "Region Örebro län"),
    ("Västmanland", "19", "Region Västmanland"),
    ("Dalarna", "20", "Region Dalarna"),
    ("Gävleborg", "21", "Region Gävleborg"),
    ("Västernorrland", "22", "Region Västernorrland"),
    ("Jämtland", "23", "Region Jämtland Härjedalen"),
    ("Västerbotten", "24", "Region Västerbotten"),
    ("Norrbotten", "25", "Region Norrbotten"),
]


def _region_of(name: str) -> tuple[str, str]:
    for key, code, canon in KEY_TO_REGION:
        if key in name:
            return code, canon
    raise SystemExit(f"Okänd region i CSV: {name!r}")


def transcribe(csv_path: Path = CSV_PATH) -> str:
    """Returnerar config-blocket (subnational_governance.regions) som sträng."""
    if not csv_path.exists():
        raise SystemExit(f"Saknar källfil {csv_path} — se modulens docstring för curl-kommando.")
    rows = list(csv.DictReader(csv_path.open(encoding="utf-8-sig"), delimiter=";"))
    ov_col = next(c for c in rows[0] if c.startswith("Övrigt parti"))
    data: dict[str, dict] = {}
    for r in rows:
        if r["År"] not in YEARS:
            continue
        code, canon = _region_of(r["Region"])
        present = {NORM.get(c, c) for c in PARTY_COLS if (r.get(c) or "").strip()}
        parties = [p for p in CANON_ORDER if p in present]      # kanonisk ordning
        local = (r.get(ov_col) or "").strip()
        d = data.setdefault(code, {"name": canon, "terms": {}})
        d["terms"][TERM[r["År"]]] = {"parties": parties, "local": local}

    out: list[str] = ["  regions:"]
    for code in sorted(data):
        d = data[code]
        out.append(f'    "{code}":')
        out.append(f'      name: "{d["name"]}"')
        out.append("      terms:")
        for term in ("2014-2018", "2018-2022", "2022-2026"):
            t = d["terms"][term]
            line = f'        "{term}": {{ leading_parties: [{", ".join(t["parties"])}]'
            if t["local"]:
                line += f', local_parties: "{t["local"]}"'
            out.append(line + " }")
    out.append("  # kontrollsummor (antal regioner med partiet i styret per valår):")
    for yr in YEARS:
        tally: dict[str, int] = {}
        for d in data.values():
            for p in d["terms"][TERM[yr]]["parties"]:
                tally[p] = tally.get(p, 0) + 1
        out.append(f"  #   {yr}: " + "  ".join(f"{p}={tally.get(p, 0)}" for p in CANON_ORDER))
    return "\n".join(out)


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(transcribe())


if __name__ == "__main__":
    main()
