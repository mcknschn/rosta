"""Kör hela pipelinen lokalt end-to-end: Fas 1 -> Fas 2 -> Fas 3 -> C3 -> Fas 5.

  python -m pipeline.build_all

Fas 1-3 hämtar live från öppna svenska API:er (Riksdagen, SCB, Kolada, Energimyndigheten)
och fyller data/warehouse.duckdb lokalt. C3 (build_subnational) hämtar region-nivå vårdserier
för den subnationella D-attributionen. Fas 5 skriver dist/scores.json + dist/evidence.json.
Frontend: servera repo-roten (python -m http.server) och öppna /web/.
"""

from __future__ import annotations

from . import build_fas1, build_fas2, build_fas3, build_subnational, scorerun


def main() -> None:
    build_fas1.main()
    print()
    build_fas2.main()
    print()
    build_fas3.main()
    print()
    build_subnational.main()  # C3: region-nivå vård -> subnationell D (måste före scorerun)
    print()
    scorerun.main()


if __name__ == "__main__":
    main()
