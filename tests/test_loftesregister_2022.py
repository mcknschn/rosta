"""Proven för löftesregistret 2022 (biljett #54).

Två slag av prov ligger här.

**Verktyget.** De rena funktionerna i `pipeline/tools/loftesregister.py`: textstädningen,
avstavningen, läsordningen ur ett spaltsatt uppslag, och de tre differenstalen i beslut 7.
Inget av dem rör en PDF, så de går att köra i CI där PDF:erna inte finns.

**Låsningen.** Beslut 8 kräver ett prov som faller på en ändrad bokstav. Registret bär sin
egen SHA-256, och provet räknar om den. Det prövar också att registret hänger ihop med
underlaget det drogs ur, och att hämtmanifestets PDF-hash står kvar orörd.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from pipeline.tools import loftesregister as lr

ROT = Path(__file__).resolve().parents[1]
KONFIG = ROT / "loften" / "config" / "loftesregister_2022"
REGISTER = KONFIG / "register.yaml"
DIFFERENS = KONFIG / "differens.yaml"


# ------------------------------------------------------------------- textstädningen


def test_ligatur_blir_tva_tecken():
    """Satsen band ihop `fl` till en glyf. Ordet är `inflation` och inte `ination`."""
    assert lr.stada("in\ufb02ation") == "inflation"
    assert lr.stada("di\ufb00erentierade") == "differentierade"


def test_tankstreck_blir_bindestreck():
    assert lr.stada("landet \u2013 och inte") == "landet - och inte"
    assert lr.stada("kris \u2014 och medgang") == "kris - och medgang"


def test_hart_mellanslag_blir_mellanslag():
    assert lr.stada("145\u00a0000") == "145 000"


def test_bel_star_kvar_till_markoren():
    """BEL är en listmarkör i ett symbolteckensnitt, inte ett styrtecken i en mening.

    Det tas bort av `dela_markor` och inte av `stada`, så att raden bär flaggan.
    """
    assert lr.stada("\u0007Infor en arbetarepension") == "\u0007Infor en arbetarepension"
    assert lr.dela_markor("\u0007Infor en arbetarepension") == (True, "Infor en arbetarepension")


def test_markor_av_flera_tecken_skiljs_helt():
    """S satter sin punkt som en Wingdings-glyf, ett tabbsteg, ett mellanslag och ett BEL."""
    assert lr.dela_markor("\t Kraftigt oka antalet poliser") == (
        True,
        "Kraftigt oka antalet poliser",
    )


def test_markor_skiljs_fran_texten():
    assert lr.dela_markor("\u2022 fasa ut fossila subventioner.") == (
        True,
        "fasa ut fossila subventioner.",
    )
    assert lr.dela_markor("fasa ut fossila subventioner.") == (
        False,
        "fasa ut fossila subventioner.",
    )


# ------------------------------------------------------------------- avstavningen


def _foga(*rader: str) -> list[str]:
    return [text for _, text in lr.foga_avstavning([lr.dela_markor(r) for r in rader])]


def test_mjukt_bindestreck_fogas_ihop():
    assert _foga("ge\u00ad", "mensam organisation") == ["gemensam organisation"]


def test_mjukt_bindestreck_mitt_i_raden_tas_bort():
    assert _foga("barnmor\u00adsketeam") == ["barnmorsketeam"]


def test_bindestreck_mot_gemen_fogas_ihop():
    assert _foga("valjarnas for-", "troende for") == ["valjarnas fortroende for"]


def test_elliptisk_sammansattning_star_kvar():
    """`valds- och sexualbrott` bär partiets eget bindestreck. Det fogas aldrig."""
    assert _foga("valds- ", "och sexualbrott") == ["valds-", "och sexualbrott"]


def test_bindestreck_mot_versal_star_kvar():
    assert _foga("El- ", "Och drivmedelspriser") == ["El-", "Och drivmedelspriser"]


def test_markor_bryter_avstavningen():
    """En ny punkt börjar, hur raden före än slutade."""
    assert _foga("skatten sanks-", "\u2022 fasa ut subventioner") == [
        "skatten sanks-",
        "fasa ut subventioner",
    ]


# ------------------------------------------------------------------- lasordningen


def _ruta(x0, y0, x1, y1, text):
    return (x0, y0, x1, y1, text, 0, 0)


def test_spalter_lases_spalt_for_spalt():
    """Två spalter under en rubrik. Rubriken först, sedan hela vänsterspalten."""
    rutor = [
        _ruta(250, 120, 390, 180, "hoger ett"),
        _ruta(50, 120, 190, 180, "vanster ett"),
        _ruta(250, 200, 390, 260, "hoger tva"),
        _ruta(50, 200, 190, 260, "vanster tva"),
        _ruta(50, 30, 390, 90, "rubrik"),
    ]
    assert [r[4] for r in lr.xy_snitt(rutor)] == [
        "rubrik",
        "vanster ett",
        "vanster tva",
        "hoger ett",
        "hoger tva",
    ]


def test_smal_lucka_delar_inte_spalter():
    """Ett radavstand inom en spalt ar ingen ranna. RANNA_MIN skiljer de tva."""
    rutor = [
        _ruta(50, 200, 190, 260, "under"),
        _ruta(50, 120, 190, 180, "over"),
        _ruta(196, 120, 330, 180, "nastan samma spalt"),
    ]
    assert [r[4] for r in lr.xy_snitt(rutor)][0] == "over"


def test_ensam_ruta_star_kvar():
    assert lr.xy_snitt([_ruta(0, 0, 10, 10, "en")]) == [_ruta(0, 0, 10, 10, "en")]


# ------------------------------------------------------------------- radspannen


def test_tolka_spann_bar_flera_delar():
    assert lr.tolka_spann("85-86,89-92") == ((85, 86), (89, 92))
    assert lr.tolka_spann("81") == ((81, 81),)
    assert lr.tolka_spann(" 4-7 , 9 ") == ((4, 7), (9, 9))


def test_tomt_spann_ar_ett_fel():
    with pytest.raises(ValueError):
        lr.tolka_spann("")


def test_skriv_spann_ar_motsatsen():
    for text in ("85-86,89-92", "81", "4-7,9"):
        assert lr.skriv_spann(lr.tolka_spann(text)) == text


def _post(dok: str, spann: str, ident: str = "x") -> lr.Post:
    return lr.Post(id=ident, dokument=dok, spann=lr.tolka_spann(spann))


def _underlag(*texter: str) -> dict[int, lr.Rad]:
    return {
        i: lr.Rad(nr=i, sida=1 + (i - 1) // 5, text=t, block=i, markor=False)
        for i, t in enumerate(texter, start=1)
    }


def test_posten_hoppar_over_sidfoten():
    rader = _underlag("a", "b", "sidnummer", "c", "d")
    post = _post("S", "1-2,4-5")
    assert post.rader == [1, 2, 4, 5]
    assert lr.lydelse(rader, post) == "a b c d"


def test_avstavning_over_sidbrytningen_fogas_i_lydelsen():
    """Ordet bröts over brytningen. Halvorna ligger i skilda block, och fogas anda ihop."""
    rader = _underlag("bland annat for gang-", "6 / 7", "relaterad brottslighet")
    assert lr.lydelse(rader, _post("S", "1,3")) == "bland annat for gangrelaterad brottslighet"


def test_overlappande_poster_ar_ett_fel():
    rader = _underlag("a", "b", "c")
    fel = lr.kontrollera_spann(rader, [_post("S", "1-2", "p1"), _post("S", "2-3", "p2")])
    assert len(fel) == 1
    assert "p1" in fel[0] and "p2" in fel[0]


def test_rad_utanfor_underlaget_ar_ett_fel():
    rader = _underlag("a", "b")
    fel = lr.kontrollera_spann(rader, [_post("S", "1-9", "p1")])
    assert fel and "finns inte i underlaget" in fel[0]


def test_otagna_rader_visar_vad_genomgangen_lamnade():
    rader = _underlag("a", "b", "c", "d")
    assert lr.otagna_rader(rader, [_post("S", "1-2")]) == [3, 4]
    assert lr.otagna_rader(rader, [_post("S", "1-4")]) == []


# ------------------------------------------------------------------- differensen


def test_identiska_genomgangar_ger_noll_i_alla_tre_talen():
    a = [_post("S", "1-3", "a1"), _post("S", "4-6", "a2")]
    b = [_post("S", "1-3", "b1"), _post("S", "4-6", "b2")]
    d = lr.differens(a, b)
    assert d.tal == (0, 0, 0)
    assert d.delade == 2


def test_post_bara_a_har_raknas_for_sig():
    a = [_post("S", "1-3", "a1"), _post("S", "4-6", "a2")]
    b = [_post("S", "1-3", "b1")]
    d = lr.differens(a, b)
    assert d.tal == (1, 0, 0)
    assert [p.id for p in d.bara_a] == ["a2"]


def test_post_bara_b_har_raknas_for_sig():
    d = lr.differens([_post("S", "1-3", "a1")], [_post("S", "1-3", "b1"), _post("S", "9", "b2")])
    assert d.tal == (0, 1, 0)
    assert [p.id for p in d.bara_b] == ["b2"]


def test_samma_post_styckad_olika_ar_inget_bortfall():
    """A drog gransen vid rad 6, B vid rad 5. Det ar en post, inte tva bortfall."""
    d = lr.differens([_post("S", "1-6", "a1")], [_post("S", "1-5", "b1")])
    assert d.tal == (0, 0, 1)
    assert d.styckat_olika[0][0].id == "a1"
    assert d.styckat_olika[0][1].id == "b1"


def test_en_post_i_a_parar_sig_med_hogst_en_i_b():
    """B styckade samma text i tva punkter. Den ena blir paret, den andra `bara B`."""
    d = lr.differens([_post("S", "1-6", "a1")], [_post("S", "1-4", "b1"), _post("S", "5-6", "b2")])
    assert d.tal == (0, 1, 1)
    assert d.styckat_olika[0][1].id == "b1"
    assert [p.id for p in d.bara_b] == ["b2"]


def test_storsta_overlappet_parar_sig_forst():
    d = lr.differens(
        [_post("S", "10-20", "a1")],
        [_post("S", "1-11", "b_liten"), _post("S", "12-19", "b_stor")],
    )
    assert d.styckat_olika[0][1].id == "b_stor"


def test_id_sats_ur_ordningen_och_inte_ur_genomgangen(tmp_path):
    """Tva genomgangar far aldrig skilja sig pa hur de numrerade."""
    fil = tmp_path / "g.yaml"
    fil.write_text("poster:\n  S:\n    - '9-10'\n    - '1-3'\n", encoding="utf-8")
    poster = lr.las_genomgang(fil)["S"]
    assert [p.id for p in poster] == ["S-001", "S-002"]
    assert poster[0].spann == ((1, 3),)


# ------------------------------------------------------------------- facit


def _differens(*fall: dict) -> dict:
    return {"dokument": {"S": {"fall": list(fall)}}}


def _fall(slag: str, a_rader, b_rader, beslut) -> dict:
    return {
        "slag": slag,
        "sida": 1,
        "a_rader": a_rader,
        "b_rader": b_rader,
        "a": None,
        "b": None,
        "beslut": beslut,
    }


def test_facit_bar_det_bada_genomgangarna_ar_eniga_om():
    a = {"S": [_post("S", "1-3", "a1"), _post("S", "4-6", "a2")]}
    b = {"S": [_post("S", "1-3", "b1"), _post("S", "4-6", "b2")]}
    poster = lr.facit(_differens(), a, b)["S"]
    assert [p.spann for p in poster] == [((1, 3),), ((4, 6),)]
    assert [p.id for p in poster] == ["S-001", "S-002"]


def test_ett_oavgjort_fall_stoppar_bygget():
    a = {"S": [_post("S", "1-3", "a1")]}
    b: dict = {"S": []}
    with pytest.raises(SystemExit) as fel:
        lr.facit(_differens(_fall("bara_a", "1-3", None, None)), a, b)
    assert "inte avgjord" in str(fel.value)


def test_beslutet_ingen_lamnar_posten_utanfor():
    a = {"S": [_post("S", "1-3", "a1")]}
    b: dict = {"S": []}
    assert lr.facit(_differens(_fall("bara_a", "1-3", None, "ingen")), a, b)["S"] == []


def test_beslutet_a_tar_a_sin_styckning():
    a = {"S": [_post("S", "1-6", "a1")]}
    b = {"S": [_post("S", "1-4", "b1")]}
    fall = _fall("styckat_olika", "1-6", "1-4", "a")
    assert lr.facit(_differens(fall), a, b)["S"][0].spann == ((1, 6),)


def test_beslutet_b_tar_b_sin_styckning():
    a = {"S": [_post("S", "1-6", "a1")]}
    b = {"S": [_post("S", "1-4", "b1")]}
    fall = _fall("styckat_olika", "1-6", "1-4", "b")
    assert lr.facit(_differens(fall), a, b)["S"][0].spann == ((1, 4),)


def test_projektagaren_far_satta_en_egen_grans():
    a = {"S": [_post("S", "1-6", "a1")]}
    b = {"S": [_post("S", "1-4", "b1")]}
    fall = _fall("styckat_olika", "1-6", "1-4", "1-3,5-6")
    assert lr.facit(_differens(fall), a, b)["S"][0].spann == ((1, 3), (5, 6))


def test_beslutet_a_pa_ett_fall_bara_b_har_ar_ett_fel():
    """Beslutet pekar pa en genomgang som inte har nagon post dar."""
    a: dict = {"S": []}
    b = {"S": [_post("S", "1-3", "b1")]}
    with pytest.raises(SystemExit):
        lr.facit(_differens(_fall("bara_b", None, "1-3", "a")), a, b)


# ------------------------------------------------------------------- lasningen


def _register() -> dict:
    return yaml.safe_load(REGISTER.read_text(encoding="utf-8"))


pytestmark_register = pytest.mark.skipif(
    not REGISTER.is_file(), reason="registret ar inte byggt an"
)


@pytestmark_register
def test_registret_bar_sin_egen_hash():
    """Beslut 8: en andrad bokstav i en lydelse ska falla ett prov."""
    data = _register()
    pinnad = data["innehall_sha256"]
    utan = REGISTER.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
    utan = "\n".join(r for r in utan.split("\n") if not r.startswith("innehall_sha256:"))
    assert lr.sha256_rader(utan) == pinnad


@pytestmark_register
def test_registret_pinnar_samma_pdf_som_hamtmanifestet():
    """Registret ar draget ur ett bestamt dokument, och hashen sager vilket."""
    manifest = {d["id"]: d["sha256"] for d in lr.dokument()}
    for dok, pinnad in _register()["dokument"].items():
        assert pinnad["pdf_sha256"] == manifest[dok]


@pytestmark_register
def test_varje_post_bar_lydelse_sidnummer_och_parti():
    for post in _register()["poster"]:
        assert post["parti"] in {d["id"] for d in lr.dokument()}
        assert isinstance(post["sida"], int) and post["sida"] >= 1
        assert post["lydelse"].strip()


@pytestmark_register
def test_registret_bar_inget_kategorifalt():
    """Beslut 11: extraktionen bar inget kategorifalt alls."""
    for post in _register()["poster"]:
        assert "kategori" not in post


@pytestmark_register
def test_sidnumret_ligger_inom_dokumentet():
    sidor = {d["id"]: d["sidor"] for d in lr.dokument()}
    for post in _register()["poster"]:
        assert 1 <= post["sida"] <= sidor[post["parti"]]


@pytestmark_register
def test_antalet_per_parti_stammer_med_posterna():
    data = _register()
    raknat: dict[str, int] = {}
    for post in data["poster"]:
        raknat[post["parti"]] = raknat.get(post["parti"], 0) + 1
    assert raknat == {d: v["antal"] for d, v in data["dokument"].items()}
    assert sum(raknat.values()) == data["antal"]


@pytestmark_register
def test_differensen_ar_redovisad_per_dokument():
    """Beslut 7: tre tal per dokument, och varje differens avgjord fore lasningen."""
    differens = yaml.safe_load(DIFFERENS.read_text(encoding="utf-8"))
    assert set(differens["dokument"]) == {d["id"] for d in lr.dokument()}
    for tal in differens["dokument"].values():
        for nyckel in ("bara_a", "bara_b", "styckat_olika"):
            assert isinstance(tal[nyckel], int)
    for fall in differens.get("avgjort") or []:
        assert fall["beslut"], "varje differens ska bara ett avgorande"
