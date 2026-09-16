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


def test_markor_pa_egen_rad_bars_till_nasta_rad():
    """C satter glyfen ensam pa en rad och texten pa nasta. Flaggan far inte falla bort."""
    assert lr.markerade_rader(["• ", "Sverige ska bli Europas grona batteri", "och rusta"]) == [
        (True, "Sverige ska bli Europas grona batteri"),
        (False, "och rusta"),
    ]


def test_tom_rad_utan_markor_bar_ingen_flagga_vidare():
    assert lr.markerade_rader(["   ", "vanlig text"]) == [(False, "vanlig text")]


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


def test_smal_ranna_delar_anda_spalterna():
    """M sätter sina textspalter med elva punkters ränna, och tröskeln måste ligga under den.

    Ligger tröskeln över rännan vägras den lodräta delningen, och snittet faller tillbaka
    på vågräta band. Då läses sidan vänster, höger, vänster, höger, och ett stycke som
    löper från vänsterspaltens fot till högerspaltens hjässa får sin andra halva före sin
    första.

    Måtten är de fyra brödtextblockens verkliga rutor på M:s sida 3, där rännan är 11,1
    punkter. Korpusens smalaste textspaltränna är 11,09 och ligger på M:s sida 32, alltså
    en hårsmån under. Provet skyddar därför hela korpusen mot en för hög tröskel.
    """
    rutor = [
        _ruta(304.7, 206.8, 527.6, 264.6, "hoger ett"),
        _ruta(63.8, 205.9, 293.6, 294.5, "vanster ett"),
        _ruta(304.7, 281.8, 526.6, 354.6, "hoger tva"),
        _ruta(63.8, 311.7, 289.1, 369.5, "vanster tva"),
    ]
    assert [r[4] for r in lr.xy_snitt(rutor)] == [
        "vanster ett",
        "vanster tva",
        "hoger ett",
        "hoger tva",
    ]


def test_rubrik_over_bada_spalterna_delas_av_en_harfin_lucka():
    """KD:s sida 2: rubriken korsar rännan, och luckan under den är 0,2 punkter.

    Rubriken hindrar den lodräta delningen, eftersom den täcker båda spalterna. Då måste
    den vågräta delningen skilja av rubrikbandet, annars faller snittet igenom till en
    sortering på y som läser vänster, höger, höger, vänster. Måtten är hämtade ur KD:s
    sida 2.
    """
    rutor = [
        _ruta(24.2, 4.1, 418.3, 190.1, "rubrik"),
        _ruta(26.9, 190.3, 205.2, 429.1, "vanster ett"),
        _ruta(227.5, 190.3, 405.4, 389.5, "hoger ett"),
        _ruta(227.5, 396.8, 402.6, 569.6, "hoger tva"),
        _ruta(26.9, 436.4, 206.3, 569.6, "vanster tva"),
    ]
    assert [r[4] for r in lr.xy_snitt(rutor)] == [
        "rubrik",
        "vanster ett",
        "vanster tva",
        "hoger ett",
        "hoger tva",
    ]


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


def test_post_som_tar_samma_rad_tva_ganger_ar_ett_fel():
    """`1-5,3-7` skulle annars ge en lydelse med tre dubblerade ord."""
    rader = _underlag("a", "b", "c", "d", "e", "f", "g")
    fel = lr.kontrollera_spann(rader, [_post("S", "1-5,3-7", "p1")])
    assert fel and "egna spann" in fel[0]


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


def test_ett_beslut_som_varken_ar_ord_eller_spann_namnger_fallet():
    a = {"S": [_post("S", "1-3", "a1")]}
    b: dict = {"S": []}
    with pytest.raises(SystemExit) as fel:
        lr.facit(_differens(_fall("bara_a", "1-3", None, "ja")), a, b)
    assert "varken" in str(fel.value) and "S sida 1" in str(fel.value)


def test_citat_skyddar_osynliga_tecken_over_ff_med_fyra_siffror():
    """`\\x200b` laser YAML tillbaka som blanksteg plus nolla. Lydelsen ska overleva."""
    assert yaml.safe_load("t: " + lr._citat("ett​ord")) == {"t": "ett​ord"}
    assert yaml.safe_load("t: " + lr._citat("punkt")) == {"t": "punkt"}


def test_beslutet_a_pa_ett_fall_bara_b_har_ar_ett_fel():
    """Beslutet pekar pa en genomgang som inte har nagon post dar."""
    a: dict = {"S": []}
    b = {"S": [_post("S", "1-3", "b1")]}
    with pytest.raises(SystemExit):
        lr.facit(_differens(_fall("bara_b", None, "1-3", "a")), a, b)


# ------------------------------------------------------------------- lasningen


def _register() -> dict:
    return yaml.safe_load(REGISTER.read_text(encoding="utf-8"))


def _underlag_finns() -> bool:
    return all(lr.underlagsfil(d["id"]).is_file() for d in lr.dokument())


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


@pytest.mark.skipif(
    not REGISTER.is_file() or not _underlag_finns(),
    reason="underlaget ligger utanfor git, och provet kan inte koras utan det",
)
def test_registret_pinnar_det_underlag_det_drogs_ur():
    """Bindningen mellan register och underlag ar det som gor registret reproducerbart.

    Registret bar bara radspann, sa en lydelse ar sann bara relativt ett bestamt underlag.
    Andras utvinningen glider radnumren, och da pekar spannen pa annan text utan att
    `innehall_sha256` reagerar, eftersom den bara hashar registerfilen. `underlag_sha256`
    ar spärren, och utan det har provet var den obevakad.
    """
    for dok, pinnad in _register()["dokument"].items():
        assert pinnad["underlag_sha256"] == lr.sha256_text(lr.underlagsfil(dok)), (
            f"{dok}: underlaget pa disk ar inte det registret drogs ur"
        )


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


def _pdf_finns() -> bool:
    return all(lr.pdf_stammer(d) for d in lr.dokument())


@pytest.mark.skipif(
    not REGISTER.is_file() or not _pdf_finns(),
    reason="PDF:erna ligger utanfor git, och provet kan inte koras utan dem",
)
def test_varje_post_gar_att_sla_upp_i_pdfen_pa_sitt_sidnummer():
    """Biljettens tredje krav, provat mot kallan och inte mot underlaget.

    Underlaget bar ocksa sidnumret, men det ar utvunnet av samma kod som skrev registret.
    Detta prov gar runt underlaget: det oppnar PDF:en pa den sida registret namner och
    letar efter postens lydelse dar. Glider sidnumreringen isar fran kallan sager provet det.
    """
    fitz = pytest.importorskip("fitz", reason="PyMuPDF behovs for att lasa PDF:en")

    def nyckel(text: str) -> str:
        return "".join(t for t in lr.stada(text).lower() if t.isalnum())

    sidor = {}
    for post in lr.dokument():
        with fitz.open(lr.PDF_KATALOG / post["filnamn"]) as doc:
            sidor[post["id"]] = [nyckel(sida.get_text()) for sida in doc]

    saknas = [
        f"{p['id']} sida {p['sida']}"
        for p in _register()["poster"]
        if nyckel(p["lydelse"])[:60] not in sidor[p["parti"]][p["sida"] - 1]
    ]
    assert not saknas, f"posterna gar inte att hitta pa sin sida: {saknas[:10]}"


def test_differensen_ar_redovisad_per_dokument():
    """Beslut 7: tre tal per dokument. Galler aven fore lasningen."""
    differens = yaml.safe_load(DIFFERENS.read_text(encoding="utf-8"))
    assert set(differens["dokument"]) == {d["id"] for d in lr.dokument()}
    for tal in differens["dokument"].values():
        for nyckel in ("poster_a", "poster_b", "delade", "bara_a", "bara_b", "styckat_olika"):
            assert isinstance(tal[nyckel], int)
        assert len(tal["fall"]) == tal["bara_a"] + tal["bara_b"] + tal["styckat_olika"]


@pytestmark_register
def test_varje_differens_ar_avgjord_fore_lasningen():
    """Beslut 7: projektagaren avgor varje differens INNAN registret las."""
    differens = yaml.safe_load(DIFFERENS.read_text(encoding="utf-8"))
    oavgjort = [
        f"{dok} sida {fall['sida']}"
        for dok, tal in differens["dokument"].items()
        for fall in tal["fall"]
        if fall.get("beslut") in (None, "")
    ]
    assert not oavgjort, f"registret ar last men dessa fall star oavgjorda: {oavgjort}"


# ------------------------------------------------------------------- tackningen

# Block som instruktionens version 3 lamnar utanfor med avsikt, trots sin langd.
# Var rad ar ett dokument och ett blocknummer, med skalet. Listan ar avsiktligt kort:
# den bar bara satsens egna delar, aldrig ett stycke av partiets text.
TILLATNA_LANGA_LUCKOR: dict[str, dict[int, str]] = {
    # Diagrammet `Sa har arbetslosheten forandrats i EU sedan 2014` pa M:s sida 5.
    # Blocket ar de 27 landernas namn under stapelaxeln, ett namn per rad. Det raknas
    # som langt bara for att namnen fogas ihop till en strang, inte for att det bar
    # lopande text. Blocket fore ar diagramrubriken och blocken efter ar axeltalen.
    "M": {51: "axeletiketterna i diagrammet pa sida 5, 27 landsnamn"},
    # MP:s sida 3. Blocket bar bade brodtext (rad 6-7) och tre listpunkter (rad 8-10).
    # Raderna 6-7 ar inledningen, och rad 7 slutar `Allt vi gor bygger pa solidaritet i
    # ord och handling:`, alltsa den rad som annonserar listan. Blocket bar en lista, sa
    # de fyra signalerna galler dar och inte styckeregeln, och instruktionens langa lista
    # utesluter bade inledningar och den annonserande raden. Alla tre genomgangarna
    # uteslot dem.
    #
    # Detta ar den kvarvarande formberoendet i version 3: en inledning fore en lista ar
    # ingen post, medan ett stycke i ett listlost avsnitt ar det. Undantaget ar ett och
    # bara ett i hela korpusen, och det star nedskrivet i registret.md.
    "MP": {3: "inledningen som annonserar solidaritetslistan pa sida 3"},
}

# En rubrik, en bildtext, ett sidnummer, ett sidhuvud eller en tryckortsrad ar aldrig
# 200 tecken lopande text. Ett otackt block over den langden ar darfor ett stycke som
# genomgangen tappade, inte satsens form.
LANGT_BLOCK = 200



@pytest.mark.skipif(
    not REGISTER.is_file() or not _underlag_finns(),
    reason="underlaget ligger utanfor git, och provet kan inte koras utan det",
)
def test_ingen_lang_radfoljd_ligger_utanfor_registret():
    """Version 3 av instruktionen: ett listlost avsnitt har stycket som enhet.

    Foljden ska vara att inget stycke av partiets text hamnar utanfor registret. Provet
    mater otagna RADFOLJDER och inte otagna block. Skillnaden ar inte akademisk: MP:s
    block 3 bar 259 tecken lopande text pa raderna 6-7 och tre tagna listpunkter pa
    raderna 8-10. Ett prov som hoppar over blocket sa fort en rad ar tagen ar tyst om de
    259 tecknen, och skulle ocksa vara tyst om en genomgang tog forsta punkten i ett
    block och tappade resten.
    """
    tagna: dict[str, set[int]] = {}
    for post in _register()["poster"]:
        for lo, hi in lr.tolka_spann(post["rader"]):
            tagna.setdefault(post["parti"], set()).update(range(lo, hi + 1))

    luckor = []
    for dok in lr.dokument():
        kod = dok["id"]
        block: dict[int, list] = {}
        for rad in lr.las_underlag(lr.underlagsfil(kod)):
            block.setdefault(rad.block, []).append(rad)
        tillatna = TILLATNA_LANGA_LUCKOR.get(kod, {})
        for nr, rader in block.items():
            if nr in tillatna:
                continue
            foljd: list = []
            for rad in [*rader, None]:
                if rad is not None and rad.nr not in tagna.get(kod, set()):
                    foljd.append(rad)
                    continue
                text = " ".join(r.text for r in foljd)
                if len(text) >= LANGT_BLOCK:
                    luckor.append(f"{kod} block {nr} (rad {foljd[0].nr}): {text[:70]}")
                foljd = []

    assert not luckor, f"{len(luckor)} langa radfoljder ligger utanfor registret: {luckor[:8]}"
