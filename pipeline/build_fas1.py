"""Fas 1-bygge: responsibility (nationellt) + Riksdagen actions/aktivitet -> warehouse.

Kör: python -m pipeline.build_fas1
Hämtar live från data.riksdagen.se (öppna data). Allt lagras lokalt i data/.
Skriver en täckningsrapport och flaggar kända luckor (a1 budget, voteringsprov).
"""

from __future__ import annotations

import sys
from datetime import date

from . import anchor, warehouse
from .sources import government, riksdagen, skr

# Riksmöten i fönstret (3 mandatperioder). Voteringsprovet spänner hela fönstret (Fas 1b),
# sampelt per riksmöte (max_pages) eftersom full per-ledamot-votering är ~miljonskala.
RIKSMOTEN = [
    "2014/15", "2015/16", "2016/17", "2017/18", "2018/19", "2019/20",
    "2020/21", "2021/22", "2022/23", "2023/24", "2024/25", "2025/26",
]


def main(votes_pages: int = 2) -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    retrieved_at = date.today().isoformat()
    con = warehouse.connect()

    print("== Fas 1 ==")

    # 1. Nationellt ansvar (deterministiskt ur government_periods).
    resp_rows = government.build_national_responsibility()
    n_resp = warehouse.upsert(con, "responsibility", resp_rows)
    print(f"responsibility (national): {n_resp} rader")

    # 1b. Subnationellt ansvar (deterministiskt ur SKR-styren): regioner + kommuner.
    reg_rows = skr.build_regional_responsibility()
    n_reg = warehouse.upsert(con, "responsibility", reg_rows)
    print(f"responsibility (regional): {n_reg} rader ({len({r['geography'] for r in reg_rows})} regioner)")
    mun_rows = skr.build_municipal_responsibility()
    n_mun = warehouse.upsert(con, "responsibility", mun_rows)
    print(f"responsibility (municipal): {n_mun} rader ({len({r['geography'] for r in mun_rows})} kommuner)")

    # 2. Motionsaktivitet per (parti, utskott) över a2:s fönster -> party_activity.
    # Fönstret är A:s eget (ADR 0007 punkt 1 och 3), alltså förankringens period och inte
    # mappings.window. Tabellens nyckel bär perioden, så en omhämtning över en ny period
    # LÄGGER TILL rader. De gamla raderna tas bort först, annars räknas motionerna dubbelt.
    frm, tom = anchor.a2_period()
    print(f"hämtar motionsräkning per parti×utskott ({frm}..{tom}, ~120 anrop) ...")
    removed = con.execute(
        "DELETE FROM party_activity WHERE kind = 'motion' AND period != ?", [f"{frm}/{tom}"]
    ).fetchall()
    act_rows = riksdagen.fetch_motion_counts(retrieved_at, frm=frm, tom=tom)
    n_act = warehouse.upsert(con, "party_activity", act_rows, validate=False)
    print(f"party_activity: {n_act} rader (rader på andra perioder borttagna: {removed})")

    # 3. Voteringar -> actions, prov per riksmöte över HELA fönstret (Fas 1b).
    print(f"hämtar voteringsprov per riksmöte ({len(RIKSMOTEN)} rm × {votes_pages} sidor) ...")
    n_votes = 0
    for rm in RIKSMOTEN:
        vote_rows = riksdagen.fetch_votes_sample(retrieved_at, rm=rm, max_pages=votes_pages)
        n_votes += warehouse.upsert(con, "actions", vote_rows)
    print(f"actions (votering, prov hela fönstret): {n_votes} rader över {len(RIKSMOTEN)} riksmöten")

    # --- Täckningsrapport ---
    print("\n-- täckning --")
    print("party_activity: motioner per kategori (summa över partier, hela fönstret):")
    for cat, total in con.execute(
        "SELECT category, sum(count) FROM party_activity GROUP BY category ORDER BY 2 DESC"
    ).fetchall():
        print(f"   {cat:12} {int(total)}")
    print("party_activity: per parti (summa motioner):")
    for party, total in con.execute(
        "SELECT party, sum(count) FROM party_activity GROUP BY party ORDER BY 2 DESC"
    ).fetchall():
        print(f"   {party:4} {int(total)}")
    print("actions (votering-prov): per kategori:")
    for cat, n in con.execute(
        "SELECT category, count(*) FROM actions GROUP BY category ORDER BY 2 DESC"
    ).fetchall():
        print(f"   {cat:12} {n}")
    print("responsibility: per parti×roll:")
    for party, role, n in con.execute(
        "SELECT party, role, count(*) FROM responsibility GROUP BY party, role ORDER BY party"
    ).fetchall():
        print(f"   {party:4} {role:11} {n}")

    print("\n-- kända luckor (loggas, ej tysta) --")
    print("   a1 budgetprioritering: kräver robust parsning av budgetmotioners anslag per UO.")
    print("       Medvetet uppskjuten — A:s tyngsta vikt; en bräcklig parser får inte korrumpera A.")
    print("   actions(votering): prov per riksmöte (max_pages), ej uttömmande; matar ännu inget betyg.")
    print("   responsibility subnationell: 21 regioner + 290 kommuner × 3 mandatperioder (SKR-styren) -> C.")
    con.close()


if __name__ == "__main__":
    pages = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    main(votes_pages=pages)
