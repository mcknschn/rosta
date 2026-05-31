"""Rösta datapipeline.

Lager (se DATA.md):
  1. sources/   – rå insamling från officiella svenska källor (endast lokalt)
  2. transform  – rådata -> warehouse-tabeller (observations/actions/responsibility)
  3. claims     – observations/actions/responsibility -> claims
     effects     – claims -> indicator_effects
  4. score      – indicator_effects + indikatorer + regler -> dist/scores.json + evidence.json

Endast dist/ deployas. data/ stannar lokalt.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT / "config"
SCHEMA_DIR = ROOT / "schemas"
DATA_DIR = ROOT / "data"
DIST_DIR = ROOT / "dist"

__all__ = ["ROOT", "CONFIG_DIR", "SCHEMA_DIR", "DATA_DIR", "DIST_DIR"]
