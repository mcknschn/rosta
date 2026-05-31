"""Kör hela pipelinen lokalt end-to-end: Fas 1 -> Fas 2 -> Fas 3 -> Fas 5.

  python -m pipeline.build_all

Fas 1-3 hämtar live från öppna svenska API:er (Riksdagen, SCB, Kolada, Energimyndigheten)
och fyller data/warehouse.duckdb lokalt. Fas 5 skriver dist/scores.json + dist/evidence.json.
Frontend: servera repo-roten (python -m http.server) och öppna /web/.
"""

from __future__ import annotations

from . import build_fas1, build_fas2, build_fas3, scorerun


def main() -> None:
    build_fas1.main()
    print()
    build_fas2.main()
    print()
    build_fas3.main()
    print()
    scorerun.main()


if __name__ == "__main__":
    main()
