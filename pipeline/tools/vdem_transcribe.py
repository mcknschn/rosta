"""Reproducerar och AUDITERAR config/vdem_demokrati.yaml mot V-Dems officiella dataset.

V-Dem (Göteborgs universitet) publicerar hela datasetet fritt; R-paketet vdemdata speglar det som
vdem.RData på GitHub. Det här verktyget laddar ned datasetet, filtrerar Sverige och korsverifierar
varje årsvärde i configen mot den auktoritativa källan (per V-Dem-variabelkod, t.ex. v2x_rule).

Kör manuellt (kräver pyreadr — endast detta verktyg, ej pipelinen/testerna):

    python -m pipeline.tools.vdem_transcribe

Exit 0 = configen matchar V-Dem-datasetet; exit 1 = avvikelse (värde reviderat i ny V-Dem-version,
ny variabelkod, eller årsspann som behöver uppdateras). Detta är transkriberingens revisionsspår —
ingen runtime-parser körs i själva pipelinen (sources/vdem.py läser bara den pinnade configen).
"""

from __future__ import annotations

import sys

import httpx

from .. import config

_DATA_URL = "https://raw.githubusercontent.com/vdeminstitute/vdemdata/master/data/vdem.RData"
_TOL = 0.001  # V-Dem publicerar 3 decimaler; tål avrundning men fångar fel serie/version.


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    try:
        import pyreadr  # endast detta verktyg, inte pipelinen
    except ImportError:
        raise SystemExit("pyreadr krävs för V-Dem-transkriberingsverktyget: pip install pyreadr") from None

    cfg = config.vdem_demokrati()
    country = cfg.get("country", "Sweden")
    print(f"== Auditerar config/vdem_demokrati.yaml mot V-Dem ({cfg['dataset']}), land={country} ==")

    resp = httpx.get(_DATA_URL, follow_redirects=True, timeout=300)
    resp.raise_for_status()
    tmp = "vdem_audit.RData"
    with open(tmp, "wb") as fh:
        fh.write(resp.content)
    df = pyreadr.read_r(tmp)
    df = df[next(iter(df))]
    swe = df[df["country_name"] == country].set_index("year")

    mismatches = 0
    for ind, spec in cfg["indicators"].items():
        var = spec["vdem_code"]
        print(f"\n-- {ind}  ({var}) --")
        for year, cv in sorted(spec["years"].items()):
            live = swe.loc[float(year), var] if float(year) in swe.index else None
            ok = live is not None and abs(float(cv) - float(live)) <= _TOL
            if not ok:
                lv = round(float(live), 3) if live is not None else None
                print(f"  {year}: cfg={cv}  vdem={lv}   [AVVIKELSE]")
                mismatches += 1
        if mismatches == 0:
            print(f"  alla {len(spec['years'])} år OK (±{_TOL})")
    if mismatches:
        raise SystemExit(f"\n{mismatches} avvikelse(r) — uppdatera config/vdem_demokrati.yaml.")
    print("\nAlla indikatorer och år matchar V-Dem-datasetet.")


if __name__ == "__main__":
    main()
