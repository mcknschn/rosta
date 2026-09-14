"""POC:en Samstämmighet (biljett #47): räkningens seams och biljettens åtta godkännandetester.

Måttet väger 0, ingår inte i någon poäng och rör varken `dist/`, pipen eller gränssnittet.
Testerna delar sig i två halvor:

  1. Seams. Rena funktioner med injicerade fixturer, så räkningen går att pröva utan repots data.
  2. Godkännandetesterna. Biljettens åtta regler, ordagrant.

Ingen regel nämner ett parti, och inget test läser ett glapp som ett omdöme.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import subprocess
from pathlib import Path

import pytest
import yaml

from pipeline.tools import samstammighet as sam

ROT = Path(__file__).resolve().parents[1]
POC = ROT / "docs" / "samstammighet_poc"
KONFIG = ROT / "config" / "samstammighet_poc"
FORHANDSREG = POC / "forhandsregistrering.md"
RESULTAT_YAML = KONFIG / "resultat.yaml"

KATEGORIER = ["ekonomi", "valfard", "trygghet", "forsvar", "klimat", "integration", "demokrati"]
PARTIER = ["S", "M", "SD", "C", "V", "KD", "MP", "L"]

# Kategorinamnen som korpusarna faktiskt bär, plus avvikelsen i 2.4.
NAMN = {
    "Ekonomi och jobb": "ekonomi",
    "Välfärd": "valfard",
    "Lag och trygghet": "trygghet",
    "Försvar och beredskap": "forsvar",
    "Klimat, miljö och energi": "klimat",
    "Integration och sammanhållning": "integration",
    "Frihet, demokrati och institutioner": "demokrati",
}


def _poster(parti: str, namn_och_antal: dict[str, int]) -> list[sam.Post]:
    ut = []
    for namn, antal in namn_och_antal.items():
        for i in range(antal):
            ut.append(sam.Post(id=f"{parti}-{namn[:3]}-{i}", parti=parti, kategorinamn=namn))
    return ut


def _las(fil: Path) -> dict:
    return yaml.safe_load(fil.read_text(encoding="utf-8"))


def _dist_hashar() -> dict[str, str]:
    return {
        f.name: hashlib.sha256(f.read_bytes()).hexdigest()
        for f in sorted((ROT / "dist").glob("*.json"))
    }


def _git(*argument: str) -> str | None:
    """Utdata från ett git-anrop, eller None utanför ett git-träd."""
    try:
        ut = subprocess.run(
            ["git", *argument], cwd=ROT, capture_output=True, text=True, timeout=30, check=False,
        )
    except (OSError, subprocess.SubprocessError):  # pragma: no cover - beror på miljön
        return None
    return ut.stdout if ut.returncode == 0 else None


def _ytligt_trad() -> bool:
    """Är historien avhuggen? En grund klon bär bara en commit.

    `actions/checkout` klonar grunt som standard, och då bär VARJE fil samma commit-datum.
    Ordningen går alltså inte att se, och ett prov på den skulle avgöras av en slump.
    Provet hoppas över i stället, och CI hämtar hela historien (`fetch-depth: 0`).
    """
    return (_git("rev-parse", "--is-shallow-repository") or "").strip() == "true"


def _lades_till_i(fil: Path) -> str | None:
    """Datum för den commit som lade till filen, eller None när ordningen inte går att läsa."""
    if _ytligt_trad():
        return None
    ut = _git("log", "--diff-filter=A", "--format=%cI", "--", str(fil.relative_to(ROT)))
    if ut is None:
        return None
    rader = [r for r in ut.splitlines() if r.strip()]
    return rader[-1] if rader else None


# ----------------------------------------------------------------- seam: retoriksidan (2.1-2.4)


def test_retorikandelarna_summerar_till_ett_over_de_sju():
    poster = _poster("S", {"Ekonomi och jobb": 3, "Välfärd": 1})
    andelar, antal = sam.retorikandelar(poster, ["S"], KATEGORIER, NAMN)
    assert sum(andelar[("S", c)] for c in KATEGORIER) == pytest.approx(1.0)
    assert andelar[("S", "ekonomi")] == pytest.approx(0.75)
    assert andelar[("S", "valfard")] == pytest.approx(0.25)
    assert antal["S"]["i_kategori"] == 4


def test_en_kategori_partiet_aldrig_namner_far_andelen_noll():
    poster = _poster("V", {"Ekonomi och jobb": 5})
    andelar, _ = sam.retorikandelar(poster, ["V"], KATEGORIER, NAMN)
    assert andelar[("V", "klimat")] == 0.0
    assert set(andelar) == {("V", c) for c in KATEGORIER}


def test_posterna_utanfor_de_sju_raknas_bort_ur_bade_taljare_och_namnare():
    """2.3: en post utanför de sju har ingen handlingssida att jämföras med."""
    poster = _poster("M", {"Ekonomi och jobb": 2, sam.UTANFOR: 8})
    andelar, antal = sam.retorikandelar(poster, ["M"], KATEGORIER, NAMN)
    assert andelar[("M", "ekonomi")] == pytest.approx(1.0)
    assert antal["M"] == {"i_kategori": 2, "utanfor": 8, "totalt": 10}


def test_avvikande_kategorinamn_bryggas_till_sitt_id():
    """2.4: korpusarna skriver 'Integration och sammanhållning', configen 'och social'."""
    poster = _poster("C", {"Integration och sammanhållning": 4})
    andelar, _ = sam.retorikandelar(poster, ["C"], KATEGORIER, NAMN)
    assert andelar[("C", "integration")] == pytest.approx(1.0)


def test_okant_kategorinamn_faller_hart():
    """2.4: ett tyst bortfall skulle krympa nämnaren utan att synas."""
    poster = _poster("L", {"Bostadspolitik": 3})
    with pytest.raises(ValueError, match="Bostadspolitik"):
        sam.retorikandelar(poster, ["L"], KATEGORIER, NAMN)


def test_parti_utan_en_enda_post_i_de_sju_faller_hart():
    """En tom nämnare ger ingen profil, och en tyst nolla vore ett värre fel."""
    poster = _poster("MP", {sam.UTANFOR: 3})
    with pytest.raises(ValueError, match="MP"):
        sam.retorikandelar(poster, ["MP"], KATEGORIER, NAMN)


# ----------------------------------------------------------------- seam: handlingssidan (3.1)


def test_handlingsandelarna_normeras_inom_partiet():
    a = {("S", c): v for c, v in zip(KATEGORIER, [3.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0], strict=True)}
    andelar = sam.handlingsandelar(a, ["S"], KATEGORIER)
    assert sum(andelar[("S", c)] for c in KATEGORIER) == pytest.approx(1.0)
    assert andelar[("S", "ekonomi")] == pytest.approx(3.0 / 10.0)
    assert andelar[("S", "demokrati")] == pytest.approx(2.0 / 10.0)


def test_handlingssidan_faller_nar_partiets_summa_ar_noll():
    a = {("S", c): 0.0 for c in KATEGORIER}
    with pytest.raises(ValueError, match="S"):
        sam.handlingsandelar(a, ["S"], KATEGORIER)


def test_handlingssidan_faller_nar_en_cell_saknas():
    a = {("S", c): 1.0 for c in KATEGORIER[:-1]}
    with pytest.raises(ValueError, match="demokrati"):
        sam.handlingsandelar(a, ["S"], KATEGORIER)


# ----------------------------------------------------------------- seam: glappet (4, 5.1, 5.3)


def test_glappet_ar_retorik_minus_handling():
    r = {("S", "ekonomi"): 0.6, ("S", "valfard"): 0.4}
    h = {("S", "ekonomi"): 0.5, ("S", "valfard"): 0.5}
    g = sam.glapp(r, h, ["S"], ["ekonomi", "valfard"])
    assert g[("S", "ekonomi")] == pytest.approx(0.1)
    assert g[("S", "valfard")] == pytest.approx(-0.1)


def test_profilavstandet_ar_noll_nar_profilerna_sammanfaller():
    g = {("S", c): 0.0 for c in KATEGORIER}
    assert sam.profilavstand(g, "S", KATEGORIER) == pytest.approx(0.0)


def test_profilavstandet_ar_ett_nar_profilerna_ar_disjunkta():
    """All betoning skulle behöva flytta, alltså avståndet 1."""
    g = {("S", c): 0.0 for c in KATEGORIER}
    g[("S", "ekonomi")] = 1.0
    g[("S", "klimat")] = -1.0
    assert sam.profilavstand(g, "S", KATEGORIER) == pytest.approx(1.0)


def test_storsta_positiva_glappet_namner_sin_kategori():
    g = {("S", c): 0.0 for c in KATEGORIER}
    g[("S", "valfard")] = 0.21
    g[("S", "klimat")] = -0.30
    kategori, varde = sam.storsta_positiva_glapp(g, "S", KATEGORIER)
    assert (kategori, varde) == ("valfard", pytest.approx(0.21))


# ----------------------------------------------------------------- seam: trösklarna (6.1-6.3)


def test_skiljbarheten_raknar_skilda_varden_pa_tre_decimaler():
    """6.1: två värden som bara skiljer sig i fjärde decimalen är ett värde."""
    varden = {"S": 0.1000, "M": 0.10004, "SD": 0.2, "C": 0.3, "V": 0.4, "KD": 0.5, "MP": 0.6, "L": 0.7}
    ut = sam.skiljbarhet(varden)
    assert ut["skilda"] == 7
    assert ut["spann"] == pytest.approx(0.6)
    assert ut["klarar"] is True


def test_skiljbarheten_faller_pa_for_litet_spann():
    varden = {p: 0.10 + i * 0.01 for i, p in enumerate(PARTIER)}
    ut = sam.skiljbarhet(varden)
    assert ut["skilda"] == 8
    assert ut["spann"] == pytest.approx(0.07)
    assert ut["klarar"] is False
    assert "spann" in ut["skal"]


def test_skiljbarheten_faller_pa_for_fa_skilda_varden():
    varden = {p: (0.0 if i < 5 else 0.5) for i, p in enumerate(PARTIER)}
    ut = sam.skiljbarhet(varden)
    assert ut["skilda"] == 2
    assert ut["klarar"] is False
    assert "skilda" in ut["skal"]


def test_pearson_ger_ett_vid_perfekt_linjart_samband():
    assert sam.pearson([1, 2, 3, 4], [2, 4, 6, 8]) == pytest.approx(1.0)
    assert sam.pearson([1, 2, 3, 4], [8, 6, 4, 2]) == pytest.approx(-1.0)


def test_pearson_ar_noll_utan_samband():
    assert sam.pearson([1, 2, 3, 4], [1, -1, -1, 1]) == pytest.approx(0.0, abs=1e-12)


def test_pearson_faller_pa_en_konstant_serie():
    with pytest.raises(ValueError, match="konstant"):
        sam.pearson([1, 2, 3, 4], [7, 7, 7, 7])


def test_spearman_ser_ett_monotont_men_icke_linjart_samband():
    xs = [1, 2, 3, 4]
    ys = [1, 4, 9, 1000]
    assert sam.spearman(xs, ys) == pytest.approx(1.0)
    assert sam.pearson(xs, ys) < 0.95


def test_langdkonfunden_faller_vid_absolutbelopp_over_grasen():
    kort = {p: float(i) for i, p in enumerate(PARTIER)}
    langd = {p: float(i) for i, p in enumerate(PARTIER)}
    ut = sam.langdkonfund(kort, langd)
    assert ut["pearson"] == pytest.approx(1.0)
    assert ut["klarar"] is False


def test_langdkonfunden_klarar_sig_utan_samband():
    varden = dict(zip(PARTIER, [0.1, 0.5, 0.2, 0.4, 0.3, 0.45, 0.15, 0.35], strict=True))
    langd = dict(zip(PARTIER, [100, 100, 100, 100, 500, 500, 500, 500], strict=True))
    ut = sam.langdkonfund(varden, langd)
    assert abs(ut["pearson"]) < sam.TROSKEL_KORRELATION
    assert ut["klarar"] is True


def test_blockskillnaden_ar_cohens_d_och_klarar_sig_nar_den_ar_hogst_ett():
    varden = {"M": 0.5, "KD": 0.3, "L": 0.5, "SD": 0.3, "S": 0.4, "V": 0.2, "C": 0.4, "MP": 0.2}
    ut = sam.blockskillnad(varden, ["M", "KD", "L", "SD"], ["S", "V", "C", "MP"])
    assert ut["mellan"] == pytest.approx(0.1)
    assert ut["inom"] == pytest.approx(0.11547, abs=1e-4)
    assert ut["d"] == pytest.approx(ut["mellan"] / ut["inom"])
    assert ut["klarar"] is True


def test_blockskillnaden_faller_nar_mellan_overstiger_inom():
    varden = {"M": 0.80, "KD": 0.81, "L": 0.79, "SD": 0.80, "S": 0.20, "V": 0.21, "C": 0.19, "MP": 0.20}
    ut = sam.blockskillnad(varden, ["M", "KD", "L", "SD"], ["S", "V", "C", "MP"])
    assert ut["mellan"] > ut["inom"]
    assert ut["klarar"] is False


# ----------------------------------------------------------------- seam: bootstrappen (7.2)


# Retoriken tyngre i ekonomi, handlingen jämnare: profilerna korsar varandra, så avståndet
# rör sig åt båda hållen när posterna dras om. En fixtur där de aldrig korsas ger ett
# konstant avstånd, och då prövar bootstraptesterna ingenting.
_BOOT_TYNGD = {
    "Ekonomi och jobb": 30, "Välfärd": 25, "Lag och trygghet": 15, "Försvar och beredskap": 10,
    "Klimat, miljö och energi": 10, "Integration och sammanhållning": 5,
    "Frihet, demokrati och institutioner": 5,
}
_BOOT_HANDLING = {
    ("S", c): v for c, v in zip(KATEGORIER, [0.20, 0.20, 0.20, 0.15, 0.10, 0.10, 0.05], strict=True)
}


def _boot_poster(faktor: int = 1) -> list[sam.Post]:
    return _poster("S", {namn: antal * faktor for namn, antal in _BOOT_TYNGD.items()})


def test_bootstrappen_ger_samma_intervall_med_samma_fro():
    argument = (_boot_poster(), _BOOT_HANDLING, ["S"], KATEGORIER, NAMN)
    ett = sam.bootstrap(*argument, fro=123, omdragningar=200)
    tva = sam.bootstrap(*argument, fro=123, omdragningar=200)
    assert ett == tva
    assert ett["S"][0] < ett["S"][1], "fixturen ger ett konstant avstånd och prövar ingenting"


def test_bootstrappen_ror_sig_med_frot():
    argument = (_boot_poster(), _BOOT_HANDLING, ["S"], KATEGORIER, NAMN)
    ett = sam.bootstrap(*argument, fro=123, omdragningar=200)
    tva = sam.bootstrap(*argument, fro=124, omdragningar=200)
    assert ett["S"] != tva["S"]


def test_bootstrappens_intervall_omsluter_punktskattningen():
    poster = _boot_poster()
    r, _ = sam.retorikandelar(poster, ["S"], KATEGORIER, NAMN)
    punkt = sam.profilavstand(sam.glapp(r, _BOOT_HANDLING, ["S"], KATEGORIER), "S", KATEGORIER)
    lo, hi = sam.bootstrap(
        poster, _BOOT_HANDLING, ["S"], KATEGORIER, NAMN, fro=sam.FRO, omdragningar=500
    )["S"]
    assert lo <= punkt <= hi


def test_bootstrappen_blir_smalare_av_fler_poster():
    """Fler poster ger mindre urvalsosäkerhet, alltså ett smalare intervall."""
    lo_s, hi_s = sam.bootstrap(
        _boot_poster(10), _BOOT_HANDLING, ["S"], KATEGORIER, NAMN, fro=sam.FRO, omdragningar=400
    )["S"]
    lo_b, hi_b = sam.bootstrap(
        _boot_poster(1), _BOOT_HANDLING, ["S"], KATEGORIER, NAMN, fro=sam.FRO, omdragningar=400
    )["S"]
    assert (hi_s - lo_s) < (hi_b - lo_b)


# ----------------------------------------------------------------- seam: diagnostiken


def test_koncentrationen_ar_noll_for_en_jamn_profil():
    jamn = {("S", c): 1.0 / len(KATEGORIER) for c in KATEGORIER}
    assert sam.koncentration(jamn, ["S"], KATEGORIER)["S"] == pytest.approx(0.0)


def test_koncentrationen_ar_hogst_for_en_profil_i_en_enda_kategori():
    spets = {("S", c): 0.0 for c in KATEGORIER}
    spets[("S", "ekonomi")] = 1.0
    vantat = 1.0 - 1.0 / len(KATEGORIER)
    assert sam.koncentration(spets, ["S"], KATEGORIER)["S"] == pytest.approx(vantat)


def test_diagnostiken_ser_nar_hela_variationen_ligger_pa_retoriksidan():
    """Är handlingssidan jämn för alla partier blir avståndet retorikens koncentration."""
    namn = {v: k for k, v in NAMN.items()}
    poster: list[sam.Post] = []
    for i, p in enumerate(PARTIER):
        tyngd = {c: 10 + 8 * ((i + j) % 5) for j, c in enumerate(KATEGORIER)}
        poster += _poster(p, {namn[c]: n for c, n in tyngd.items()})
    r, _ = sam.retorikandelar(poster, PARTIER, KATEGORIER, NAMN)
    jamn = {(p, c): 1.0 / len(KATEGORIER) for p in PARTIER for c in KATEGORIER}
    ut = sam.diagnostik(r, jamn, jamn, PARTIER, KATEGORIER)
    assert ut["r_avstand_mot_retorikens_koncentration"] == pytest.approx(1.0)
    assert max(ut["handlingens_koncentration"].values()) == pytest.approx(0.0)


# ----------------------------------------------------------------- seam: hela räkningen


def _fixtur() -> dict:
    """Ett litet men fullständigt underlag: 8 partier, 7 kategorier, skilda profiler."""
    namn = {v: k for k, v in NAMN.items()}
    poster: list[sam.Post] = []
    for i, p in enumerate(PARTIER):
        tyngd = {c: 10 + (5 * ((i + j) % 4)) for j, c in enumerate(KATEGORIER)}
        poster += _poster(p, {namn[c]: n for c, n in tyngd.items()})
    a = {(p, c): 1.0 + ((i + j) % 3) for i, p in enumerate(PARTIER) for j, c in enumerate(KATEGORIER)}
    return {"poster": poster, "a": a}


def test_rakningen_ger_ett_glapp_per_cell_och_ett_avstand_per_parti():
    f = _fixtur()
    ut = sam.rakna_resultat(
        bakat=f["poster"], framat=[], a_celler=f["a"], a1_celler=f["a"],
        partier=PARTIER, kategorier=KATEGORIER, namn_till_id=NAMN,
        regeringssidan=["M", "KD", "L", "SD"], oppositionen=["S", "V", "C", "MP"],
        omdragningar=100,
    )
    assert len(ut["glapp"]["primar"]) == len(PARTIER)
    for p in PARTIER:
        assert set(ut["glapp"]["primar"][p]) == set(KATEGORIER)
    assert set(ut["profilavstand"]["primar"]) == set(PARTIER)


def test_rakningen_ar_reproducerbar():
    f = _fixtur()
    argument = dict(
        bakat=f["poster"], framat=[], a_celler=f["a"], a1_celler=f["a"],
        partier=PARTIER, kategorier=KATEGORIER, namn_till_id=NAMN,
        regeringssidan=["M", "KD", "L", "SD"], oppositionen=["S", "V", "C", "MP"],
        omdragningar=100,
    )
    assert sam.rakna_resultat(**argument) == sam.rakna_resultat(**argument)


def test_rakningen_bar_inget_sammanvagt_betyg():
    """Godkännandetest 3: POC:en mäter skiljbarhet, inte samstämmighet."""
    f = _fixtur()
    ut = sam.rakna_resultat(
        bakat=f["poster"], framat=[], a_celler=f["a"], a1_celler=f["a"],
        partier=PARTIER, kategorier=KATEGORIER, namn_till_id=NAMN,
        regeringssidan=["M", "KD", "L", "SD"], oppositionen=["S", "V", "C", "MP"],
        omdragningar=100,
    )
    text = json.dumps(ut, ensure_ascii=False).lower()
    for ord_ in ("betyg", "poäng", "rangordning", "samstämmighetstal"):
        assert ord_ not in text, f"räkningen bär ordet {ord_!r}"


# ----------------------------------------------------------------- godkännandetest 1


def test_1_trosklarna_star_nedskrivna_och_lasta():
    text = FORHANDSREG.read_text(encoding="utf-8")
    assert "Version: 1" in text
    assert "Status: **låst**" in text
    assert "Låst: 2026-09-14, före den första räkningen" in text


def test_1_trosklarna_committades_fore_den_forsta_korningen():
    """Ordningen ska gå att se på commit-datum, inte bara på en rad i filen."""
    reg = _lades_till_i(FORHANDSREG)
    if reg is None:
        pytest.skip("inget git-träd att läsa commit-datum ur")
    if not RESULTAT_YAML.exists():
        pytest.skip("ingen körning är committad än")
    resultat = _lades_till_i(RESULTAT_YAML)
    if resultat is None:
        pytest.skip("resultatet är inte committat än")
    assert reg < resultat, "resultatet committades före tröskelvärdena"


def test_1_de_lasta_talen_star_kvar_i_koden():
    """Ändras ett låst tal faller POC:en. Koden och filen ska säga samma sak."""
    text = FORHANDSREG.read_text(encoding="utf-8")
    assert f"**{sam.FRO}**" in text
    assert f"{sam.OMDRAGNINGAR:,}".replace(",", " ") in text
    assert str(sam.TROSKEL_SPANN).replace(".", ",") in text
    assert str(sam.TROSKEL_KORRELATION).replace(".", ",") in text
    assert sam.TROSKEL_SKILDA == 5 and "minst fem skilda värden" in text
    assert sam.DECIMALER == 3 and "**tre decimaler**" in text


# ----------------------------------------------------------------- godkännandetest 2


@pytest.mark.skipif(not RESULTAT_YAML.exists(), reason="ingen körning är committad än")
def test_2_kallorna_ar_desamma_som_vid_korningen():
    """Talen är PINNADE till sitt underlag, och delpoäng A rör sig varje gang pipen byggs om.

    Faller det här testet är POC:ens tal gamla. Rättelsen är att köra om den, inte att lossa
    provet: en tyst gammal siffra är ett värre fel än ett rött test.
    """
    pinnat = _las(RESULTAT_YAML)["kallhashar"]
    aktuella = sam.kallhashar()
    rorda = sorted(k for k in aktuella if aktuella[k] != pinnat.get(k))
    assert not rorda, (
        "underlaget har ändrats sedan körningen: " + ", ".join(rorda)
        + ". Kör om: python -m pipeline.tools.samstammighet --resultat"
    )


@pytest.mark.skipif(not RESULTAT_YAML.exists(), reason="ingen körning är committad än")
def test_2_rakningen_ar_reproducerbar_ur_repot():
    """Samma indata ur repot ger samma tal, utan ny hämtning."""
    committat = _las(RESULTAT_YAML)
    if sam.kallhashar() != committat["kallhashar"]:
        pytest.skip("underlaget har ändrats; se test_2_kallorna_ar_desamma_som_vid_korningen")
    farskt = sam.kor()
    for nyckel in ("retorik", "handling", "glapp", "profilavstand", "trosklar", "utfall"):
        assert farskt[nyckel] == committat[nyckel], f"{nyckel} skiljer sig från det committade"


@pytest.mark.skipif(not RESULTAT_YAML.exists(), reason="ingen körning är committad än")
def test_2_ingen_kalla_ligger_utanfor_repot():
    kallor = _las(RESULTAT_YAML)["kallor"]
    for _namn, sokvag in kallor.items():
        assert (ROT / sokvag).exists(), f"{sokvag} saknas i repot"
        assert "warehouse" not in sokvag, "lagret är gitignorerat och får inte vara en källa"


# ----------------------------------------------------------------- godkännandetest 3


@pytest.mark.skipif(not RESULTAT_YAML.exists(), reason="ingen körning är committad än")
def test_3_ingen_fil_bar_ett_sammanvagt_betyg():
    for fil in sorted(POC.glob("*.md")) + sorted(KONFIG.glob("*.yaml")):
        text = fil.read_text(encoding="utf-8").lower()
        for ord_ in ("samstämmighetsbetyg", "samstämmighetspoäng", "samstämmighetsindex"):
            assert ord_ not in text, f"{fil.name} bär {ord_!r}"


@pytest.mark.skipif(not RESULTAT_YAML.exists(), reason="ingen körning är committad än")
def test_3_profilavstandet_inverteras_aldrig():
    """5.2: avståndet blir ett betyg i samma stund det vänds till ett samstämmighetstal."""
    for fil in sorted(POC.glob("*.md")):
        text = fil.read_text(encoding="utf-8")
        assert "1 - TV" not in text and "1 minus avståndet" not in text


# ----------------------------------------------------------------- godkännandetest 4 och 5


@pytest.mark.skipif(not RESULTAT_YAML.exists(), reason="ingen körning är committad än")
def test_4_langdkonfunden_ar_redovisad_som_ett_tal():
    langd = _las(RESULTAT_YAML)["trosklar"]["primar"]["langd"]
    assert isinstance(langd["pearson"], float)
    assert isinstance(langd["spearman"], float)
    assert -1.0 <= langd["pearson"] <= 1.0


@pytest.mark.skipif(not RESULTAT_YAML.exists(), reason="ingen körning är committad än")
def test_5_blockskillnaden_ar_redovisad():
    res = _las(RESULTAT_YAML)
    neutralitet = res["trosklar"]["primar"]["neutralitet"]
    for nyckel in ("mellan", "inom", "d", "regeringssidan", "oppositionen"):
        assert nyckel in neutralitet
    assert set(neutralitet["regeringssidan"]) == {"M", "KD", "L", "SD"}

    sd_ut = res["trosklar"]["varianter"].get("sd_utanfor")
    assert sd_ut, "känslighetsprovet i 6.3 saknas"
    assert "SD" not in sd_ut["neutralitet"]["regeringssidan"]
    assert "SD" not in sd_ut["neutralitet"]["oppositionen"]
    # Provet gäller BARA neutraliteten. Skiljbarhet och längd räknas på samma per-parti-värden
    # som den primära, så de skulle bara upprepa primärens tal under en missvisande etikett.
    assert set(sd_ut) == {"galler", "neutralitet", "klarar", "fallna"}


@pytest.mark.skipif(not RESULTAT_YAML.exists(), reason="ingen körning är committad än")
def test_4_spridningen_ar_redovisad_for_varje_parti():
    """Tröskelregel 4: punktskattningar och spridning redovisas oavsett utfall."""
    res = _las(RESULTAT_YAML)
    for parti in res["partier"]:
        lo, hi = res["profilavstand"]["intervall"][parti]
        punkt = res["profilavstand"]["primar"][parti]
        assert lo <= punkt <= hi, f"{parti}: punktskattningen ligger utanför sitt intervall"


# ----------------------------------------------------------------- godkännandetest 6


# Anklagande ord, med böjning: 'svek', 'sveket', 'ohederligt', 'lögner'.
_OHEDERLIGT = (r"ohederlig\w*", r"lögn\w*", r"bluff\w*", r"svek\w*", r"löftesbrott\w*",
               r"vilseled\w*", r"falsk\w*")
# Nekande ord, UTAN fri böjning. 'inte\w*' skulle matcha 'integration', och då nekar varje
# mening om integration sig själv och provet slutar bita.
_NEKANDE = (r"aldrig", r"ingen\w*", r"inget", r"inte", r"varken")


def _bar(stycke: str, monster: tuple[str, ...]) -> bool:
    """Ordgränsat prov mot en mängd mönster."""
    return any(re.search(rf"\b{m}\b", stycke, re.IGNORECASE) for m in monster)


def _ohederliga_stycken(stycken: list[str]) -> list[str]:
    """Stycken som använder ett anklagande ord utan att neka det."""
    return [st for st in stycken if _bar(st, _OHEDERLIGT) and not _bar(st, _NEKANDE)]


def _stycken(fil: Path) -> list[str]:
    """Meningar ur en markdownfil, rader ur en yamlfil.

    Markdown radbryts för hand, så en rad där är ingen enhet. Yaml skrivs av verktyget och
    radbryts aldrig mitt i en mening, och dess enda fritext är huvudkommentaren. Att flata ut
    yamlfilen till meningar ger i stället sju stycken på upp till 15 000 tecken, och då räcker
    ett enda nekande ord någonstans i filen för att släppa igenom allt.
    """
    text = fil.read_text(encoding="utf-8")
    if fil.suffix == ".yaml":
        return [r for r in text.splitlines() if r.strip()]
    return re.split(r"(?<=[.!?]) ", re.sub(r"\s+", " ", text))


def test_ohederlighetsprovet_biter_pa_en_dold_anklagelse():
    """Provet som vaktar godkännandetest 6 måste självt vara provätt."""
    assert _ohederliga_stycken(["Glappet i integration visar ett svek mot väljarna."])
    assert _ohederliga_stycken(["Partiets intervall döljer en lögn."])
    assert not _ohederliga_stycken(["Ingen text kallar ett glapp ohederlighet."])
    assert not _ohederliga_stycken(["Ett glapp är aldrig ett löftesbrott."])
    assert not _ohederliga_stycken(["Integration och intervall nämns i samma mening."])


@pytest.mark.skipif(not RESULTAT_YAML.exists(), reason="ingen körning är committad än")
def test_6_ingen_text_framstaller_ett_glapp_som_ohederlighet():
    """En mening som SLÅR FAST regeln får nämna orden. En mening som använder dem får inte."""
    traffar = []
    for fil in sorted(POC.glob("*.md")) + sorted(KONFIG.glob("*.yaml")):
        traffar += [f"{fil.name}: {st.strip()}" for st in _ohederliga_stycken(_stycken(fil))]
    assert not traffar, "texten läser ett glapp som ohederlighet: " + "; ".join(traffar)


# ----------------------------------------------------------------- godkännandetest 7


def test_7_pipen_importerar_aldrig_poc_en():
    """Måttet väger 0. Drar pipen in det har någon flyttat måttet."""
    pipen = sorted((ROT / "pipeline").glob("*.py")) + sorted((ROT / "pipeline" / "sources").glob("*.py"))
    assert len(pipen) > 20, "hittade för få pipelinefiler, globben är trasig"
    for fil in pipen:
        assert "samstammighet" not in fil.read_text(encoding="utf-8"), f"{fil.name} drar in POC:en"


def test_7_kategorimodellen_vet_inte_att_poc_en_finns():
    for namn in ("categories.yaml", "scoring.yaml"):
        text = (ROT / "config" / namn).read_text(encoding="utf-8").lower()
        assert "samstammighet" not in text and "samstämmighet" not in text, namn


def test_7_granssnittet_vet_inte_att_poc_en_finns():
    for fil in sorted((ROT / "web").glob("*.js")) + sorted((ROT / "web").glob("*.html")):
        text = fil.read_text(encoding="utf-8").lower()
        assert "samstammighet" not in text and "samstämmighet" not in text, fil.name


_SKRIVANDE = (
    r"\.write_text\(", r"\.write_bytes\(", r"\.mkdir\(", r"\.touch\(", r"\.unlink\(",
    r"\bopen\([^)]*[\"']\s*[wax]", r"\bjson\.dump\(", r"\byaml\.(safe_)?dump_all\(",
    r"\bshutil\.", r"\bos\.(remove|replace|rename|makedirs)\(",
)


def test_7_verktyget_skriver_bara_i_sin_egen_utkatalog():
    """Varje skrivande rad i verktyget måste utgå från UTKATALOG, och den ligger inte i dist/."""
    assert sam.UTKATALOG == ROT / "config" / "samstammighet_poc"
    assert sam.UTKATALOG.relative_to(ROT).parts[0] == "config"
    kallan = (ROT / "pipeline" / "tools" / "samstammighet.py").read_text(encoding="utf-8")
    skrivrader = [
        r.strip() for r in kallan.splitlines()
        if any(re.search(rx, r) for rx in _SKRIVANDE) and not r.strip().startswith(("#", "r\""))
    ]
    assert skrivrader, "hittade ingen skrivning alls, testet prövar ingenting"
    for rad in skrivrader:
        assert rad.startswith(("UTKATALOG.mkdir", "fil.write_text")), f"okänd skrivning: {rad}"
    kropp = kallan[kallan.index("def skriv_resultat"):]
    assert 'fil = UTKATALOG / "resultat.yaml"' in kropp, "utfilen byggs inte ur UTKATALOG"


def test_7_en_korning_lamnar_dist_orort():
    """Godkännandetest 7: dist/ är orört. A läses, aldrig skrivs."""
    fore = _dist_hashar()
    sam.kor(omdragningar=20)
    assert _dist_hashar() == fore


# ----------------------------------------------------------------- godkännandetest 8


@pytest.mark.skipif(not RESULTAT_YAML.exists(), reason="ingen körning är committad än")
def test_8_ett_fallet_matt_bar_ett_daterat_avslagsskal():
    utfall = _las(RESULTAT_YAML)["utfall"]
    avslag = POC / "avslagsskal.md"
    if utfall["klarar"]:
        assert not avslag.exists(), "måttet klarade trösklarna men ett avslagsskäl ligger kvar"
        return
    assert avslag.exists(), "måttet föll men inget avslagsskäl finns"
    text = avslag.read_text(encoding="utf-8")
    assert "Datum: 2026-09-14" in text
    assert "reopen_if" in text or "Villkor för att ta upp frågan igen" in text


# ----------------------------------------------------------------- rapporten mot räkningen


def _svenskt(x: float) -> str:
    return f"{x:.3f}".replace(".", ",")


@pytest.mark.skipif(
    not (RESULTAT_YAML.exists() and (POC / "resultat.md").exists()),
    reason="ingen körning eller ingen rapport är committad än",
)
def test_rapporten_citerar_rakningens_egna_tal():
    res = _las(RESULTAT_YAML)
    rapport = (POC / "resultat.md").read_text(encoding="utf-8")
    for parti in res["partier"]:
        tal = _svenskt(res["profilavstand"]["primar"][parti])
        assert tal in rapport, f"{parti}: profilavståndet {tal} saknas i rapporten"


@pytest.mark.skipif(not RESULTAT_YAML.exists(), reason="ingen körning är committad än")
def test_retorikandelarna_i_resultatet_summerar_till_ett():
    res = _las(RESULTAT_YAML)
    for parti, rad in res["retorik"]["union"].items():
        assert sum(rad.values()) == pytest.approx(1.0), parti


@pytest.mark.skipif(not RESULTAT_YAML.exists(), reason="ingen körning är committad än")
def test_glappet_summerar_till_noll_inom_partiet():
    """Två profiler som båda summerar till 1 ger ett glapp som summerar till 0."""
    res = _las(RESULTAT_YAML)
    for parti, rad in res["glapp"]["primar"].items():
        assert sum(rad.values()) == pytest.approx(0.0, abs=1e-8), parti


@pytest.mark.skipif(not RESULTAT_YAML.exists(), reason="ingen körning är committad än")
def test_profilavstandet_i_resultatet_ar_halva_absolutsumman():
    res = _las(RESULTAT_YAML)
    for parti, rad in res["glapp"]["primar"].items():
        vantat = 0.5 * sum(abs(v) for v in rad.values())
        assert res["profilavstand"]["primar"][parti] == pytest.approx(vantat)


@pytest.mark.skipif(not RESULTAT_YAML.exists(), reason="ingen körning är committad än")
def test_antalet_poster_stammer_med_biljettens_egna_tal():
    """Biljetten skriver 525 poster för M och 107 för MP. Unionen ska ge samma tal."""
    antal = _las(RESULTAT_YAML)["poster"]["union"]
    assert antal["M"]["totalt"] == 525
    assert antal["MP"]["totalt"] == 107
    assert sum(rad["totalt"] for rad in antal.values()) == 896 + 1073


def test_matematiken_bakom_profilavstandet_ar_ett_avstand():
    """Symmetri och triangelolikhet, alltså att talet verkligen är ett avstånd."""
    a = dict(zip(KATEGORIER, [0.4, 0.3, 0.1, 0.1, 0.05, 0.03, 0.02], strict=True))
    b = dict(zip(KATEGORIER, [0.1, 0.1, 0.3, 0.2, 0.2, 0.05, 0.05], strict=True))
    c = dict(zip(KATEGORIER, [0.2, 0.2, 0.2, 0.2, 0.1, 0.05, 0.05], strict=True))

    def tv(x, y):
        g = {("P", k): x[k] - y[k] for k in KATEGORIER}
        return sam.profilavstand(g, "P", KATEGORIER)

    assert tv(a, b) == pytest.approx(tv(b, a))
    assert tv(a, b) <= tv(a, c) + tv(c, b) + 1e-12
    assert math.isclose(tv(a, a), 0.0, abs_tol=1e-12)
