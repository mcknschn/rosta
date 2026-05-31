"""Kopiera deploy-artefakterna dist/*.json -> web/data/ så frontend blir självständig.
Kör efter `python -m pipeline.scorerun`. web/data/ är genererad och behöver inte committas
om man hellre serverar repo-roten (app.js faller tillbaka på ../dist/)."""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
dst = ROOT / "web" / "data"
dst.mkdir(parents=True, exist_ok=True)
for name in ("scores.json", "evidence.json"):
    src = ROOT / "dist" / name
    if not src.exists():
        raise SystemExit(f"saknas: {src} — kör `python -m pipeline.scorerun` först")
    shutil.copy2(src, dst / name)
    print(f"kopierade {name} -> web/data/{name}")
