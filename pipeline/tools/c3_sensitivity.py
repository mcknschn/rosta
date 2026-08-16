"""C3 — neutralitets-/robusthetsaudit för den subnationella välfärds-D (vård).

Codex-kravet före sign-off: subnationell region-attribution riskerar att bli en förtäckt
GEOGRAFI-/blockproxy snarare än ett mått på partistyrt utfall. Tecken-bara dämpar magnitud-
outliers men INTE regionalt urval, demografi, finansiering eller serielängd. Den här auditen
kör därför den per-parti subnationella vård-signalen under flera varianter och rapporterar om
PARTIORDNINGEN är stabil:

  1. lika-per-region   vs  befolkningsviktat   (Kolada N01951)   -> geografi-/storleksberoende?
  2. vardkoer-only     vs  overlevnad-only     vs kombinerat     -> driver en enda serie tecknet?
  3. leave-one-region-out (21 körningar)                         -> driver ett fåtal regioner tecknet?
  4. nationell-only    vs  blandad             (faktisk välfärds-D-ranking, två scorerun-byggen)

Om ordningen bara flippar under viktning eller drivs av få regioner -> nedgradera säkerheten /
behåll bakom flaggan. Kör: python -m pipeline.tools.c3_sensitivity
Ej i testsviten (hämtar befolkning live). Läser den lokala warehouse:n (region-obs från
build_subnational måste ha körts).
"""

from __future__ import annotations

import sys

import httpx

from .. import config, score, scorerun, warehouse

_BASE = "https://api.kolada.se/v3"
_UA = {"User-Agent": "rosta-datapipeline/0.1 (civic-tech; official swedish open data)"}
_POP_KPI = "N01951"  # folkmängd (Kolada/SCB)


def _region_populations(codes: list[str]) -> dict[str, float]:
    """Senaste årets folkmängd per Kolada-regionkod (audit-input, ej deployad)."""
    pops: dict[str, float] = {}
    with httpx.Client(timeout=60, headers=_UA, follow_redirects=True) as c:
        for code in codes:
            r = c.get(f"{_BASE}/data/kpi/{_POP_KPI}/municipality/{code}")
            r.raise_for_status()
            pts = []
            for rec in r.json().get("values", []):
                cell = next((v for v in rec.get("values", []) if v.get("gender") == "T"), None)
                if cell and cell.get("value") is not None:
                    pts.append((rec["period"], float(cell["value"])))
            if pts:
                pops[code] = max(pts)[1]  # senaste året
    return pops


def _subnat_vard_net(
    sub_series: dict, ryp: dict, meta: dict, party: str, lag: int, dead: float,
    region_weights: dict[str, float] | None = None,
    indicators: set[str] | None = None,
    exclude_region: str | None = None,
) -> float | None:
    """Region-poolat vård-submåttsnet per parti under en variant (vikt/indikator/exkluderad region)."""
    nets: list[float] = []
    for (cat, ind), by_region in sub_series.items():
        if cat != "valfard" or (indicators is not None and ind not in indicators):
            continue
        direction = meta[(cat, ind)][1]
        num = den = 0.0
        for code, series in by_region.items():
            if code == exclude_region:
                continue
            rw = 1.0 if region_weights is None else region_weights.get(code, 0.0)
            years = sorted(series)
            for i in range(1, len(years)):
                y_prev, y = years[i - 1], years[i]
                if y - y_prev != 1:
                    continue
                adj = score.direction_adjusted_change(series[y_prev], series[y], direction)
                if adj is None:
                    continue
                w = ryp.get(code, {}).get(y - lag, {}).get(party, 0.0)
                if w <= 0:
                    continue
                num += rw * w * score.change_sign(adj, dead)
                den += rw * w
        if den > 0:
            nets.append(num / den)
    return sum(nets) / len(nets) if nets else None


def _order(net_by_party: dict[str, float | None]) -> list[str]:
    present = {p: v for p, v in net_by_party.items() if v is not None}
    return [p for p, _ in sorted(present.items(), key=lambda kv: -kv[1])]


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    cfg = config.scoring()["D_resultat"]
    lag, dead = int(cfg["attribution_lag_years"]), float(cfg["change_dead_zone"])
    parties = config.party_codes()

    con = warehouse.connect()
    sub_series = scorerun._subnational_annual_series(con)
    ryp = scorerun.region_year_power_fractions()
    meta = scorerun._indicator_meta()
    codes = sorted({code for by_region in sub_series.values() for code in by_region})
    if not sub_series:
        print("Inga region-observationer i warehouse — kör 'python -m pipeline.build_subnational' först.")
        return

    print(f"== C3 sensitivitetsaudit (välfärd/vård, {len(codes)} regioner) ==\n")

    pops = _region_populations(codes)
    psum = sum(pops.values())
    pop_w = {c: pops.get(c, 0.0) / psum * len(codes) for c in codes}  # medel 1.0 -> jämförbar med lika

    def nets(**kw) -> dict[str, float | None]:
        return {p: _subnat_vard_net(sub_series, ryp, meta, p, lag, dead, **kw) for p in parties}

    equal = nets()
    weighted = nets(region_weights=pop_w)
    only_vk = nets(indicators={"vardkoer"})
    only_ov = nets(indicators={"overlevnad_svar_sjukdom"})

    print("Subnationellt vård-net per parti (sign-medel i [-1,1]):")
    print(f"  {'parti':5} {'lika':>7} {'pop-vikt':>9} {'köer':>7} {'överlevn':>9}")
    for p in parties:
        def f(v): return f"{v:+.3f}" if v is not None else "   –  "
        print(f"  {p:5} {f(equal[p]):>7} {f(weighted[p]):>9} {f(only_vk[p]):>7} {f(only_ov[p]):>9}")

    print("\nOrdning (subnationellt vård-net, högst först):")
    print(f"  lika      : {' > '.join(_order(equal))}")
    print(f"  pop-vikt  : {' > '.join(_order(weighted))}")
    print(f"  köer-only : {' > '.join(_order(only_vk))}")
    print(f"  överlev.  : {' > '.join(_order(only_ov))}")

    # Leave-one-region-out: per parti, spann av vård-net + ev. teckenflipp.
    print("\nLeave-one-region-out (lika vikt): spann av vård-net + teckenstabilitet:")
    flips = []
    for p in parties:
        if equal[p] is None:
            continue
        loo = [_subnat_vard_net(sub_series, ryp, meta, p, lag, dead, exclude_region=c) for c in codes]
        loo = [v for v in loo if v is not None]
        lo, hi = min(loo), max(loo)
        sign_flip = (lo < 0 < hi) or (lo < 0 <= equal[p]) or (hi > 0 >= equal[p])
        mark = "  ⚠ TECKENFLIPP" if sign_flip else ""
        print(f"  {p:5} full={equal[p]:+.3f}  LOO-spann [{lo:+.3f}, {hi:+.3f}]{mark}")
        if sign_flip:
            flips.append(p)

    # Faktisk välfärds-D-ranking: nationell-only vs blandad (två byggen mot live-warehouse).
    import copy as _copy
    sc_off = _copy.deepcopy(config.scoring())
    sc_off["D_resultat"]["subnational"]["enabled"] = False
    sc_on = _copy.deepcopy(config.scoring())
    sc_on["D_resultat"]["subnational"]["enabled"] = True
    orig = config.scoring
    try:
        config.scoring = lambda: sc_off  # type: ignore[assignment]
        off = scorerun.build(con)["scores"]["scores"]
        config.scoring = lambda: sc_on   # type: ignore[assignment]
        on = scorerun.build(con)["scores"]["scores"]
    finally:
        config.scoring = orig  # type: ignore[assignment]
    d_off = {p: off[p]["valfard"]["components"]["D"] for p in parties}
    d_on = {p: on[p]["valfard"]["components"]["D"] for p in parties}
    print("\nFaktisk välfärds-D (komponent) nationell-only -> blandad:")
    for p in parties:
        print(f"  {p:5} {d_off[p]:.3f} -> {d_on[p]:.3f}  ({d_on[p] - d_off[p]:+.3f})")
    print(f"  ordning nat-only : {' > '.join([p for p,_ in sorted(d_off.items(), key=lambda kv:-kv[1])])}")
    print(f"  ordning blandad  : {' > '.join([p for p,_ in sorted(d_on.items(), key=lambda kv:-kv[1])])}")

    # Verdikt
    print("\n== VERDIKT ==")
    eq_ord, pw_ord = _order(equal), _order(weighted)
    print(f"  lika vs pop-vikt ordning {'IDENTISK' if eq_ord == pw_ord else 'SKILJER'}")
    print(f"  teckenflipp under LOO: {flips or 'inga'}")
    print("  (Flippar ordningen bara under viktning, eller driver få regioner tecknet -> "
          "nedgradera säkerhet / flagga. Annars är region-signalen robust.)")
    con.close()


if __name__ == "__main__":
    main()
