"""ADR 0007: A mäts över samma fönster som sin förankring. Godkännandetest till biljett #27.

Provet är ett REGELTEST. Det säger ingenting om spridning eller rangordning, eftersom ADR 0003
punkt 1 förbjuder ökad separation som mål och ADR 0007 punkt 8 deklarerar att utfallet inte var
känt när beslutet fattades.

Allt kör mot `:memory:`, aldrig mot data/warehouse.duckdb: CI har inget lager, och ett test som
läser disklagret passerar lokalt och fäller CI.
"""

from __future__ import annotations

import copy

import pytest

from pipeline import anchor, budget, config, scorerun, warehouse
from pipeline.tools import budget_ramar_transcribe
from pipeline.sources import government

_A2_PERIOD = "/".join(anchor.a2_period())


def _seed(period: str = _A2_PERIOD) -> object:
    con = warehouse.connect(":memory:")
    warehouse.upsert(con, "responsibility", government.build_national_responsibility())
    warehouse.upsert(con, "party_activity", [
        {"party": "S", "category": "ekonomi", "committee": "FiU",
         "kind": "motion", "period": period, "count": 100, "source_ref": "u"},
    ], validate=False)
    return con


# --- 1. Täljare och förankring täcker samma år, i båda halvorna ---------------------------

def test_a1_taljaren_tacker_exakt_forankringens_ar() -> None:
    """Kravet i ADR 0007 punkt 1, prövat för varje parti och kategori genom kvotens år."""
    cats, parties = config.category_ids(), config.party_codes()
    shares, active, years = budget.a1_shares(cats, parties)
    assert years == anchor.a1_years()
    assert years, "a1 saknar budgetår"
    # Andelen finns för varje parti och kategori, alltså är varje kvot räknad på samma år.
    for party in parties:
        for category in cats:
            assert (party, category) in shares, f"{party}/{category} saknar a1-andel"
    assert active == set(cats), f"grinden släckte {sorted(set(cats) - active)}"


def test_a1_forankringen_laggs_pa_taljarens_ar_och_ingenting_annat() -> None:
    """Ett år utanför täljaren får inte väga in i förankringen."""
    cats = config.category_ids()
    _shares, _active, years = budget.a1_shares(cats, config.party_codes())
    full = anchor.a1_anchor_shares(cats, years=years)
    kortare = anchor.a1_anchor_shares(cats, years=years[1:])
    assert full != kortare, "förankringen ändras inte när ett år tas bort - läser den åren alls?"


def test_a1_taljare_pa_andra_ar_an_forankringen_ar_hard_fail() -> None:
    """Faller täljaren bort ett år ska körningen stanna, aldrig räkna en skev kvot."""
    cfg = copy.deepcopy(config.budget_ramar())
    cfg["budget_years"].pop(max(cfg["budget_years"]))
    con = _seed()
    with pytest.raises(ValueError, match="ADR 0007 punkt 1"):
        scorerun.build(con, budget_cfg=cfg)
    con.close()


def test_a2_perioden_ar_forankringens_egen() -> None:
    """a2:s täljare hämtas över förankringens period, inte över mappings.window."""
    assert "/".join(anchor.a2_period()) == \
        config.a_forankring()["a2"]["chamber_motions"]["period"]
    window = config.mappings()["window"]
    assert anchor.a2_period()[0][:4] != str(window["start"]), \
        "a2 delar fönster med mappings.window - då är det inte A:s eget"


def test_a2_taljare_pa_fel_period_ar_hard_fail() -> None:
    """party_activity nycklas på perioden, så en omhämtning LÄGGER TILL rader.

    Utan den här grinden skulle motionerna summeras två gånger, och felet skulle inte synas
    i något betyg. Provet är därför att en främmande period stannar körningen.
    """
    con = _seed(period="2014-09-01/2026-05-29")
    with pytest.raises(ValueError, match="ADR 0007 punkt 1"):
        scorerun.build(con)
    con.close()


def test_a2_ratt_period_gar_igenom() -> None:
    con = _seed()
    assert scorerun.build(con)["scores"]["scores"]
    con.close()


# --- 2. Villkorsklausulen (ADR 0007 punkt 4) ----------------------------------------------

def test_villkorsklausulen_faller_inte_ut_pa_det_beslutade_fonstret() -> None:
    """Inget partis ram sammanfaller med den antagna ramen i VARJE år 2011-2025.

    Provet läser configen som den står. Det säger ingenting om hur stor skillnaden är, bara
    att nollpunkten inte tillhör ett block.
    """
    decided = config.a_forankring()["a1"]["decided_frames"]
    ok, offenders = budget.a1_admissible(config.party_codes(), decided)
    assert ok, f"a1 otillåten: {offenders} har den antagna ramen varje år"


def test_villkorsklausulen_faller_ut_pa_ett_kort_fonster() -> None:
    """Klausulen är inte tom: med bara Tidöåren är den antagna ramen regeringens.

    Det är precis det ADR 0005 förkastade under rubriken "Regeringens ram som nollpunkt", och
    klausulen finns för att ett kort fönster inte ska kunna återinföra det bakvägen.
    """
    decided = config.a_forankring()["a1"]["decided_frames"]
    cfg = copy.deepcopy(config.budget_ramar())
    cfg["budget_years"] = {y: b for y, b in cfg["budget_years"].items() if y >= 2023}
    ok, offenders = budget.a1_admissible(config.party_codes(), decided, ramar_cfg=cfg)
    assert not ok
    assert set(offenders) == {"M", "KD", "L", "SD"}, offenders


def test_villkorsklausulen_tar_bort_a1_ur_A_nar_den_faller_ut() -> None:
    """Faller klausulen ut vilar A på a2 ensam, alltså grindens vanliga tillstånd.

    Täckningen följer med av sig själv (ADR 0008 punkt 3), och skälet står som en egen flagga
    så att det inte förväxlas med en lucka i underlaget.
    """
    short = copy.deepcopy(config.budget_ramar())
    short["budget_years"] = {y: b for y, b in short["budget_years"].items() if y >= 2023}
    con = _seed()
    med_a1 = scorerun.build(con)["scores"]["scores"]
    # Fönsterprovet i punkt 1 gäller täljarens år; här prövas punkt 4, så åren tillåts matcha.
    original = anchor.a1_years
    anchor.a1_years = lambda cfg=None: [2023, 2024, 2025]        # noqa: ARG005
    try:
        utan_a1 = scorerun.build(con, budget_cfg=short)["scores"]["scores"]
    finally:
        anchor.a1_years = original
    con.close()

    # Täckningens A-halva faller från 0,30 till 0,30 x 0,4, alltså 0,18 i varje cell
    # (ADR 0008 punkt 3). Talet härleds ur configen och skrivs inte av.
    vikter = config.scoring()
    tapp = (float(vikter["subscore_weights"]["A"])
            * float(vikter["A_agerande"]["components"]["a1_budgetprioritering"]))
    for party, cats in utan_a1.items():
        for category, cell in cats.items():
            assert "A_a2_only" in cell["flags"], f"{party}/{category}"
            # Flaggan namnger partierna som fällde klausulen, inte bara att den föll.
            assert "A_a1_inadmissible:KD,L,M,SD" in cell["flags"], f"{party}/{category}"
            assert "A_a1_active" in med_a1[party][category]["flags"]
            # Den publicerade täckningen är avrundad till tre decimaler, så skillnaden mellan
            # två avrundade tal kan missa med en tusendel åt vardera hållet.
            tappet = med_a1[party][category]["coverage"] - cell["coverage"]
            assert tappet == pytest.approx(tapp, abs=0.0011), f"{party}/{category}: {tappet}"


# --- 3. Grinden i pipeline/budget.py lämnas orörd (ADR 0007 punkt 5) ----------------------

def test_grinden_star_kvar_och_passerar() -> None:
    """Snittet över åren: alla åtta partier har ram för varje UO i varje kategori, varje år."""
    cats, parties = config.category_ids(), config.party_codes()
    _shares, active, years = budget.a1_shares(cats, parties)
    assert active == set(cats)
    assert len(years) == 15, years


def test_grinden_slacker_kategorin_nar_ett_ar_ar_ofullstandigt() -> None:
    """Ett ofullständigt år ska släcka a1, inte tyst utelämnas. Grinden är oförändrad."""
    cfg = copy.deepcopy(config.budget_ramar())
    year = max(cfg["budget_years"])
    frame = cfg["budget_years"][year]["party_frame"]["S"]["frame"]
    cfg["budget_years"][year]["ramar"][frame].pop("UO4")     # trygghet tappar sitt UO
    _shares, active, _years = budget.a1_shares(
        config.category_ids(), config.party_codes(), ramar_cfg=cfg
    )
    assert "trygghet" not in active


# --- 4. Voteringsgrunden kräver röstdata för HELA regeringen -----------------------------
# Sign-off 2b, 2026-08-26: grunden behålls, men luckan stängs. `gov_votes` hoppade över
# regeringspartier som saknades i voteringlistan, så ett ensamt kvarvarande regeringsparti
# kunde definiera regeringens röst och därmed ge ett stödparti regeringens ram på halva
# underlaget. Ingen av de femton åren träffar luckan; den stängs innan den hinner göra det.

def _kolumner_utan(*partier: str) -> list[budget_ramar_transcribe.Column]:
    """Jämförelsetabellens kolumner där `partier` saknar egen ram."""
    return [budget_ramar_transcribe.Column("regeringen", (), 0.0)] + [
        budget_ramar_transcribe.Column(p, (p,), 0.0)
        for p in config.party_codes() if p not in partier
    ]


def _rostlangd(rost: dict[str, str]) -> dict[str, dict[str, int]]:
    """Voteringlistan som `attribute` läser den: parti -> röster per ståndpunkt."""
    return {p: {v: 10} for p, v in rost.items()}


def test_voteringsgrunden_slar_till_nar_hela_regeringen_har_rostat() -> None:
    """Utgångsläget: SD utan egen ram röstar som en fulltalig regering, alltså uppslutning."""
    regering = budget_ramar_transcribe.GOVERNMENT[2023]        # M, KD, L
    rost = {p: "Ja" for p in regering} | {"SD": "Ja"}
    rost |= {p: "Nej" for p in config.party_codes() if p not in rost}
    fick, problem = budget_ramar_transcribe.attribute(
        2023, _kolumner_utan("SD", *regering), _rostlangd(rost)
    )
    assert fick["SD"].basis == "votering"
    assert problem == []


def test_voteringsgrunden_slar_inte_till_nar_ett_regeringsparti_saknar_rost() -> None:
    """Codex granskning 2026-08-26: halva regeringen får inte definiera regeringens röst."""
    regering = budget_ramar_transcribe.GOVERNMENT[2023]        # M, KD, L
    rost = {p: "Ja" for p in regering} | {"SD": "Ja"}
    rost |= {p: "Nej" for p in config.party_codes() if p not in rost}
    del rost[regering[-1]]                                     # L saknas i voteringlistan
    fick, problem = budget_ramar_transcribe.attribute(
        2023, _kolumner_utan("SD", *regering), _rostlangd(rost)
    )
    assert "SD" not in fick, "uppslutning tillskriven på en ofullständig regeringsröst"
    assert any(p.startswith("SD:") for p in problem), problem


# --- 5. Delad ram per parti står i klartext (ADR 0007 Följder, sign-off 2e) ---------------
# Ett regeringsår mäts på koalitionens ram, inte partiets egen, så partier med lång
# regeringstid går sämre att skilja åt i a1. Metodrutan nämnde förhållandet men gav inga tal,
# och läsaren kunde därför inte se hur stor asymmetrin är. Sign-off 2e 2026-08-26.

def test_delad_ram_raknas_per_parti_over_hela_fonstret() -> None:
    """Talet är antal år av fönstrets, per parti, där ramen bärs av mer än ett parti."""
    delad = dict(budget.shared_frame_years())
    _shares, _active, years = budget.a1_shares(config.category_ids(), config.party_codes())
    assert set(delad) == set(config.party_codes())
    for party, n in delad.items():
        assert 0 <= n <= len(years), f"{party}: {n} av {len(years)}"
    # Ytterkanterna, som underlaget till sign-offen redovisar dem.
    assert delad["L"] == 10, delad
    assert delad["SD"] == 3, delad


def test_delad_ram_ar_tom_utan_budgetkalla() -> None:
    """Utan budgetconfig finns inga år att räkna, och metodrutan ska inte påstå något."""
    assert budget.shared_frame_years({}) == []


def test_metodrutan_ger_talen_for_delad_ram() -> None:
    """Sajten ska bära siffran, inte bara förhållandet."""
    con = _seed()
    out = scorerun.build(con)
    text = out["scores"]["meta"]["coverage_technical"]
    assert "delar ram med minst ett annat parti" in text, text
    assert "L 10" in text and "SD 3" in text, text


def test_metodrutan_tiger_om_luckan_nar_alla_ar_ar_signade() -> None:
    """Svansen redovisar en lucka. Noll kvar ska ge en mening utan svans, inte "0 står i ...".."""
    con = _seed()
    text = scorerun.build(con)["scores"]["meta"]["coverage_technical"]
    signade = sum(1 for b in config.budget_ramar()["budget_years"].values()
                  if int(b.get("version", 0)) >= 1)
    _shares, _active, years = budget.a1_shares(config.category_ids(), config.party_codes())
    if signade >= len(years):
        assert "alla expertgranskade med mänsklig sign-off" in text
        assert "står i version 0" not in text, text
    else:
        assert f"{len(years) - signade} står i version 0" in text, text
