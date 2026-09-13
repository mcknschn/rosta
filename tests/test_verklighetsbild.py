"""Enhetstester för Verklighetsbildpilotens verktyg (biljett #46, ADR 0016).

Alfavärdena nedan är handräknade ur Krippendorffs definition och står utskrivna i
testernas docstrings, så att en läsare kan följa räkningen utan att lita på minnet.
"""

from __future__ import annotations

import math

import pytest

from pipeline.tools import verklighetsbild as vb

# Populationen per parti, ur ADR 0016 diagnospunkt 2 (mappade + kandidater).
POPULATION = {"S": 72, "M": 300, "SD": 71, "C": 158, "V": 94, "KD": 55, "MP": 37, "L": 109}


# --------------------------------------------------------------------------- korpus


def test_bakatkorpusen_bar_896_utsagor():
    utsagor = vb.las_bakat()
    assert len(utsagor) == 896
    mappade = [u for u in utsagor if u.kalla == "mappning_bakat.md"]
    kandidater = [u for u in utsagor if u.kalla == "kandidater_bakat.md"]
    assert len(mappade) == 230
    assert len(kandidater) == 666


def test_bakatkorpusen_har_adrns_partifordelning():
    fordelning: dict[str, int] = {}
    for u in vb.las_bakat():
        fordelning[u.parti] = fordelning.get(u.parti, 0) + 1
    assert fordelning == POPULATION


def test_alla_utsage_id_ar_unika():
    utsagor = vb.las_bakat() + vb.las_framat()
    ids = [u.id for u in utsagor]
    assert len(ids) == len(set(ids))


def test_mappade_poster_behaller_sitt_egna_id():
    per_id = {u.id: u for u in vb.las_bakat()}
    assert "Sb-017" in per_id
    assert per_id["Sb-017"].parti == "S"
    assert per_id["Sb-017"].kategori == "Ekonomi och jobb"
    assert per_id["Sb-017"].text.startswith("Tidöregeringens passiva jobbpolitik")


def test_kandidater_far_harlett_id_och_sidnummer():
    kandidater = [u for u in vb.las_bakat() if u.kalla == "kandidater_bakat.md"]
    forsta = kandidater[0]
    assert forsta.id == "Sk-001"
    assert forsta.parti == "S"
    assert forsta.sida == 4
    assert all(u.sida is not None for u in kandidater)
    assert all(u.sida is None for u in vb.las_bakat() if u.kalla == "mappning_bakat.md")


def test_framatkorpusen_bar_1073_poster():
    framat = vb.las_framat()
    assert len(framat) == 1073
    assert {u.parti for u in framat} == set(POPULATION)


def test_ingen_utsaga_ar_tom():
    for u in vb.las_bakat() + vb.las_framat():
        assert u.text.strip(), u.id
        assert u.kategori.strip(), u.id


# --------------------------------------------------------------------------- urval


def test_urvalet_tar_25_per_parti():
    urval = vb.dra_urval(vb.las_bakat(), fro=20260913, per_parti=25)
    assert len(urval) == 200
    per_parti: dict[str, int] = {}
    for u in urval:
        per_parti[u.parti] = per_parti.get(u.parti, 0) + 1
    assert per_parti == dict.fromkeys(POPULATION, 25)


def test_urvalet_ar_utan_aterlaggning():
    urval = vb.dra_urval(vb.las_bakat(), fro=20260913, per_parti=25)
    assert len({u.id for u in urval}) == 200


def test_samma_fro_ger_samma_urval():
    korpus = vb.las_bakat()
    a = [u.id for u in vb.dra_urval(korpus, fro=20260913, per_parti=25)]
    b = [u.id for u in vb.dra_urval(korpus, fro=20260913, per_parti=25)]
    assert a == b


def test_annat_fro_ger_ett_annat_urval():
    korpus = vb.las_bakat()
    a = {u.id for u in vb.dra_urval(korpus, fro=20260913, per_parti=25)}
    b = {u.id for u in vb.dra_urval(korpus, fro=1, per_parti=25)}
    assert a != b


def test_urvalet_ryms_i_det_minsta_stratumet():
    """MP bär 37 utsagor. En dragning om 38 ska falla, inte tyst krympa."""
    with pytest.raises(ValueError, match="MP"):
        vb.dra_urval(vb.las_bakat(), fro=1, per_parti=38)


def test_delurvalet_dras_ur_de_200():
    """Prövar de frön piloten faktiskt levererade, inte ett påhittat."""
    urval = vb.dra_urval(vb.las_bakat(), fro=vb.FRO_URVAL, per_parti=vb.PER_PARTI)
    delurval = vb.dra_urval(urval, fro=vb.FRO_DELURVAL, per_parti=vb.PER_PARTI_DELURVAL)
    assert len(delurval) == 40
    assert {u.id for u in delurval} <= {u.id for u in urval}
    assert vb.FRO_DELURVAL != vb.FRO_URVAL, "delurvalet måste ha ett eget frö"


# --------------------------------------------------------------- Krippendorffs alfa


def test_alfa_ar_ett_vid_full_overensstammelse():
    par = {"u1": ["a", "a"], "u2": ["b", "b"], "u3": ["a", "a"]}
    assert vb.krippendorff_alfa(par, skala="nominal") == pytest.approx(1.0)


def test_nominal_alfa_pa_handraknat_fall():
    """Fyra enheter, två kodare, binära värden.

    A: 1 1 0 0
    B: 1 0 0 0

    Sammanträffandematrisen: o_00 = 4, o_11 = 2, o_01 = o_10 = 1, n = 8.
    n_0 = 5, n_1 = 3.
    D_o = o_01 + o_10 = 2.
    D_e = (1/7) * (n_0*n_1 + n_1*n_0) = 30/7.
    alfa = 1 - 2 / (30/7) = 1 - 14/30 = 8/15.
    """
    par = {"u1": ["1", "1"], "u2": ["1", "0"], "u3": ["0", "0"], "u4": ["0", "0"]}
    assert vb.krippendorff_alfa(par, skala="nominal") == pytest.approx(8 / 15)


def test_alfa_blir_negativ_vid_systematisk_oenighet():
    """Två enheter, två kodare, spegelvänt.

    o_01 = o_10 = 2, n = 4, n_0 = n_1 = 2.
    D_o = 4. D_e = (1/3) * (4 + 4) = 8/3. alfa = 1 - 4/(8/3) = -0,5.
    """
    par = {"u1": ["0", "1"], "u2": ["1", "0"]}
    assert vb.krippendorff_alfa(par, skala="nominal") == pytest.approx(-0.5)


def test_ordinal_alfa_pa_handraknat_fall():
    """Tre enheter, två kodare, ordinal skala.

    A: 1 2 3
    B: 1 2 2

    o_11 = 2, o_22 = 2, o_23 = o_32 = 1, n = 6. n_1 = 2, n_2 = 3, n_3 = 1.
    delta^2(1,2) = (2 + 3 - (2+3)/2)^2 = 6,25
    delta^2(2,3) = (3 + 1 - (3+1)/2)^2 = 4
    delta^2(1,3) = (2 + 3 + 1 - (2+1)/2)^2 = 20,25
    D_o = 1*4 + 1*4 = 8
    D_e = (1/5) * 2 * (2*3*6,25 + 2*1*20,25 + 3*1*4) = (1/5) * 180 = 36
    alfa = 1 - 8/36 = 7/9.
    """
    par = {"u1": ["1", "1"], "u2": ["2", "2"], "u3": ["3", "2"]}
    assert vb.krippendorff_alfa(par, skala="ordinal", ordning=["1", "2", "3"]) == pytest.approx(7 / 9)


def test_ordinal_alfa_straffar_langre_avstand_hardare():
    nara = {"u1": ["1", "2"], "u2": ["1", "1"], "u3": ["3", "3"], "u4": ["2", "2"]}
    langt = {"u1": ["1", "3"], "u2": ["1", "1"], "u3": ["3", "3"], "u4": ["2", "2"]}
    ordning = ["1", "2", "3"]
    assert vb.krippendorff_alfa(langt, skala="ordinal", ordning=ordning) < vb.krippendorff_alfa(
        nara, skala="ordinal", ordning=ordning
    )


def test_alfa_hoppar_over_enheter_med_bara_en_kodning():
    """En enhet som bara en kodare rörde bär ingen oenighet och ska inte räknas."""
    utan = {"u1": ["a", "a"], "u2": ["b", "a"]}
    med = {"u1": ["a", "a"], "u2": ["b", "a"], "u3": ["a", None]}
    assert vb.krippendorff_alfa(med, skala="nominal") == pytest.approx(
        vb.krippendorff_alfa(utan, skala="nominal")
    )


def test_alfa_utan_variation_ar_odefinierad():
    """Alla kodare satte samma värde på allt. Det finns ingen skala att mäta emot."""
    assert vb.krippendorff_alfa({"u1": ["a", "a"], "u2": ["a", "a"]}, skala="nominal") is None


def test_forvaxlingsmatris_raknar_bada_hallen():
    par = {"u1": ["a", "b"], "u2": ["a", "a"]}
    matris = vb.forvaxlingsmatris(par)
    assert matris[("a", "b")] == 1
    assert matris[("a", "a")] == 1
    assert ("b", "a") not in matris


# ------------------------------------------------------------------- utbytesskattning


def test_utbytet_ar_designviktat_med_andlighetskorrektion():
    """Två strata. N = [10, 20], n = [5, 5].

    y_A = [1,0,0,0,0], y_B = [2,0,0,0,0].
    Y = (10/5)*1 + (20/5)*2 = 10. X = 30. R = 1/3.
    s_A^2 = 0,2 ; s_B^2 = 0,8.
    Var(R) = (1/900) * [100*0,5*0,2/5 + 400*0,75*0,8/5] = (1/900)*50 = 0,0555...
    """
    skattning = vb.skatta_utbyte(
        relationer_per_utsaga={"A": [1, 0, 0, 0, 0], "B": [2, 0, 0, 0, 0]},
        population={"A": 10, "B": 20},
    )
    assert skattning.utbyte == pytest.approx(1 / 3)
    assert skattning.populationsstorlek == 30
    assert skattning.varians == pytest.approx(50 / 900)
    assert skattning.standardfel == pytest.approx(math.sqrt(50 / 900))
    lo, hi = skattning.intervall
    assert lo == pytest.approx(1 / 3 - 1.96 * math.sqrt(50 / 900))
    assert hi == pytest.approx(1 / 3 + 1.96 * math.sqrt(50 / 900))


def test_full_undersokning_ger_noll_varians():
    """Är hela stratumet kodat är ändlighetskorrektionen 1 - n/N = 0."""
    skattning = vb.skatta_utbyte(
        relationer_per_utsaga={"A": [1, 0, 3]},
        population={"A": 3},
    )
    assert skattning.utbyte == pytest.approx(4 / 3)
    assert skattning.varians == pytest.approx(0.0)


def test_utbytet_kraver_att_varje_stratum_har_en_population():
    with pytest.raises(ValueError, match="B"):
        vb.skatta_utbyte(relationer_per_utsaga={"A": [1], "B": [1]}, population={"A": 10})


def test_utbytet_kraver_att_urvalet_ryms_i_populationen():
    with pytest.raises(ValueError, match="A"):
        vb.skatta_utbyte(relationer_per_utsaga={"A": [1, 1, 1]}, population={"A": 2})


# ------------------------------------------------------------------------ snittalet


def test_snittet_ligger_mellan_de_delade_och_unionen():
    a = {"u1": {"arbetsloshet"}, "u2": {"vardkoer"}, "u3": set()}
    b = {"u1": {"arbetsloshet"}, "u2": set(), "u3": {"realloner"}}
    tal = vb.rakna_relationer(a, b)
    assert tal.delade == 1
    assert tal.union == 3
    assert tal.kodare_a == 2
    assert tal.kodare_b == 2
    assert tal.snitt == pytest.approx(2.0)
    assert tal.delade <= tal.snitt <= tal.union


def test_jaccard_ar_noll_nar_ingen_indikator_delas():
    a = {"u1": {"arbetsloshet"}}
    b = {"u1": {"realloner"}}
    assert vb.rakna_relationer(a, b).jaccard == pytest.approx(0.0)


def test_jaccard_hoppar_over_utsagor_dar_bada_lamnade_tomt():
    a = {"u1": {"arbetsloshet"}, "u2": set()}
    b = {"u1": {"arbetsloshet"}, "u2": set()}
    assert vb.rakna_relationer(a, b).jaccard == pytest.approx(1.0)


# ------------------------------------------------------------------------ citatform


def test_citatet_bevarar_styrtecken_i_stallet_for_att_stada_bort_dem():
    """mappning_framat.md bär ett BEL i S-008. Korpusen ska bära lydelsen, inte en städad version."""
    import yaml

    original = "\x07Inför en arbetarepension"
    assert yaml.safe_load(f"citat: {vb._citat(original)}")["citat"] == original


def test_citatet_skyddar_backslash_och_citattecken():
    import yaml

    original = 'en \\ och ett "citat"'
    assert yaml.safe_load(f"t: {vb._citat(original)}")["t"] == original


# ------------------------------------------------------------------ inlast kodning


def _post(uid, led, bortfall=None):
    return {"utsaga_id": uid, "led": led, "bortfall": bortfall}


def _led(provbar, indikator=None, bortfall=None):
    return {
        "text": "x",
        "provbar": provbar,
        "indikator": indikator,
        "period": {"start": 2022, "slut": 2025} if provbar else None,
        "operationalisering": "x" if provbar else None,
        "bortfall": bortfall,
    }


def test_granskningen_slapper_igenom_en_riktig_post():
    assert vb.granska_kodning(_post("U-1", [_led(True, "arbetsloshet")])).fel == []
    assert vb.granska_kodning(_post("U-2", [_led(False, bortfall="normativ")], "normativ")).fel == []


def test_granskningen_faller_en_utsaga_utan_bade_relation_och_kod():
    fel = vb.granska_kodning(_post("U-3", [_led(False, bortfall="normativ")], None)).fel
    assert any("ingen giltig bortfallskod" in f for f in fel)


def test_granskningen_faller_en_kod_utanfor_den_lasta_listan():
    """skev är förkastat av ADR 0016 beslutspunkt 9 och får inte smyga tillbaka."""
    fel = vb.granska_kodning(_post("U-4", [_led(False, bortfall="skev")], "skev")).fel
    assert any("utanför den låsta listan" in f for f in fel)


def test_granskningen_faller_ett_provbart_led_utan_indikator():
    fel = vb.granska_kodning(_post("U-5", [_led(True, None)])).fel
    assert any("saknar indikator" in f for f in fel)


def test_granskningen_faller_en_relation_som_anda_bar_en_kod():
    fel = vb.granska_kodning(_post("U-7", [_led(True, "arbetsloshet")], "normativ")).fel
    assert any("ändå bortfallskoden" in f for f in fel)


def test_fel_foretradesordning_ar_en_anmarkning_och_inget_fel():
    """normativ står före data_saknas. Fel ordning bryter kodboken, inte godkännandetest 4."""
    post = _post(
        "U-6",
        [_led(False, bortfall="data_saknas"), _led(False, bortfall="normativ")],
        "data_saknas",
    )
    granskning = vb.granska_kodning(post)
    assert granskning.fel == []
    assert any("normativ" in a for a in granskning.anmarkningar)


def test_kodbokens_egen_motsagelse_ger_anmarkning_och_inget_fel():
    """Avsnitt 6.5 vill ha operationaliseringen skriven, avsnitt 10 vill ha fältet tomt."""
    led = _led(False, bortfall="data_saknas")
    led["operationalisering"] = "matchar civil_beredskap_niva, ingen inlast serie"
    granskning = vb.granska_kodning(_post("U-8", [led], "data_saknas"))
    assert granskning.fel == []
    assert any("operationalisering" in a for a in granskning.anmarkningar)


def test_momentparen_tar_bara_utsagor_bada_kodat():
    a = {
        "x": vb.KodadUtsaga("x", 2, ("arbetsloshet",), "arbetsloshet", "relation"),
        "y": vb.KodadUtsaga("y", 1, (), "ingen", "normativ"),
    }
    b = {"x": vb.KodadUtsaga("x", 3, (), "ingen", "normativ")}
    par = vb.momentpar(a, b)
    assert set(par) == {"avgransning", "provbarhet", "indikatorval", "kodvarde"}
    assert list(par["avgransning"]) == ["x"]
    assert par["avgransning"]["x"] == ["2", "3"]
    assert par["provbarhet"]["x"] == ["ja", "nej"]
    assert par["indikatorval"]["x"] == ["arbetsloshet", "ingen"]
    assert par["kodvarde"]["x"] == ["relation", "normativ"]


# ------------------------------------------------------------------ troskelprovning


def _kodad(uid, relationer, antal_led=1):
    rel = tuple(relationer)
    return vb.KodadUtsaga(
        utsaga_id=uid,
        antal_led=antal_led,
        relationer=rel,
        forsta_indikator=rel[0] if rel else "ingen",
        kodvarde="relation" if rel else "normativ",
    )


def test_troskeln_faller_nar_utbytet_ar_for_lagt():
    a = {f"u{i}": _kodad(f"u{i}", []) for i in range(10)}
    b = dict(a)
    provning = vb.prova_trosklarna(a, b, dict.fromkeys(a, "S"), {"S": 100})
    assert provning.utbyte.utbyte == 0.0
    assert not provning.utbyte_klaras
    assert not provning.piloten_klaras


def test_troskeln_klaras_nar_varje_utsaga_ger_en_relation():
    a = {f"u{i}": _kodad(f"u{i}", ["arbetsloshet"]) for i in range(10)}
    b = dict(a)
    provning = vb.prova_trosklarna(a, b, dict.fromkeys(a, "S"), {"S": 100})
    assert provning.utbyte.utbyte == 1.0
    assert provning.utbyte_klaras
    assert provning.snitt_per_parti["S"] == 10
    assert provning.partier_under_fem == {}


def test_ett_parti_under_fem_faller_hela_piloten():
    """Kravet på minst 5 hos SAMTLIGA åtta gör regeln strängare än totalgränsen."""
    a = {f"s{i}": _kodad(f"s{i}", ["arbetsloshet"]) for i in range(10)}
    a |= {f"m{i}": _kodad(f"m{i}", []) for i in range(10)}
    parti = {u: ("S" if u.startswith("s") else "M") for u in a}
    provning = vb.prova_trosklarna(a, dict(a), parti, {"S": 20, "M": 20})
    assert provning.utbyte_klaras
    assert set(provning.partier_under_fem) == {"M"}
    assert not provning.piloten_klaras


def test_enkelsidiga_relationer_raknas_till_halften():
    a = {"u1": _kodad("u1", ["arbetsloshet"]), "u2": _kodad("u2", ["vardkoer"])}
    b = {"u1": _kodad("u1", ["arbetsloshet"]), "u2": _kodad("u2", [])}
    provning = vb.prova_trosklarna(a, b, dict.fromkeys(a, "S"), {"S": 2})
    assert provning.snitt_per_parti["S"] == 1.5


def test_bara_provbarhetens_alfa_faller_piloten():
    """Alfa för indikatorval kan falla utan att piloten gör det (förhandsreg. 4.1)."""
    a = {f"u{i}": _kodad(f"u{i}", ["arbetsloshet"]) for i in range(10)}
    b = {f"u{i}": _kodad(f"u{i}", ["vardkoer"]) for i in range(10)}
    parti = dict.fromkeys(a, "S")
    provning = vb.prova_trosklarna(a, b, parti, {"S": 10})
    assert provning.alfa["indikatorval"] is None or provning.alfa["indikatorval"] < 1.0
    assert provning.provbarheten_haller


def test_alfabeskedet_foljer_krippendorffs_nivaer():
    assert vb.alfabesked(0.81) == "haller"
    assert vb.alfabesked(0.80) == "haller"
    assert vb.alfabesked(0.70) == "tentativt"
    assert vb.alfabesked(0.60) == "haller inte"


def test_odefinierad_alfa_skiljer_full_enighet_fran_tomt_besked():
    """Alfa utan värde betyder två skilda saker. De får inte blandas ihop."""
    assert vb.alfabesked(None, alla_overens=True) == "full enighet"
    assert vb.alfabesked(None, alla_overens=False) == "odefinierad"


def test_full_enighet_kanns_igen():
    assert vb.full_overensstammelse({"u1": ["a", "a"], "u2": ["b", "b"]})
    assert not vb.full_overensstammelse({"u1": ["a", "a"], "u2": ["b", "a"]})
    assert not vb.full_overensstammelse({"u1": ["a", None]})


def test_full_enighet_om_provbarheten_faller_inte_piloten():
    """Båda kodarna sa ja på varje utsaga. Då har tröskeln inget värde att falla under."""
    a = {f"u{i}": _kodad(f"u{i}", ["arbetsloshet"]) for i in range(10)}
    provning = vb.prova_trosklarna(a, dict(a), dict.fromkeys(a, "S"), {"S": 10})
    assert provning.alfa["provbarhet"] is None
    assert provning.full_enighet["provbarhet"]
    assert provning.provbarheten_haller
    assert provning.piloten_klaras


def test_ett_tomt_stratum_stoppar_i_stallet_for_att_krympa_namnaren():
    """Utan stoppet skulle 896 tyst bli 100, och utbytet se större ut än det är."""
    a = {f"u{i}": _kodad(f"u{i}", ["arbetsloshet"]) for i in range(5)}
    parti = dict.fromkeys(a, "S")
    with pytest.raises(ValueError, match="M"):
        vb.prova_trosklarna(a, dict(a), parti, {"S": 100, "M": 100})


def test_kodare_utan_gemensam_utsaga_stoppar():
    a = {"u1": _kodad("u1", [])}
    b = {"u2": _kodad("u2", [])}
    with pytest.raises(ValueError, match="delar ingen utsaga"):
        vb.prova_trosklarna(a, b, {"u1": "S", "u2": "S"}, {"S": 10})


def test_ordinal_skala_sager_ifran_om_ett_varde_ligger_utanfor():
    """Ett led fler än kodbokens tak gav förr ett naket KeyError."""
    par = {"u1": ["7", "1"], "u2": ["1", "1"]}
    with pytest.raises(ValueError, match="utanför den ordinala skalan"):
        vb.krippendorff_alfa(par, "ordinal", ["0", "1", "2", "3", "4", "5", "6"])


def test_perioden_skrivs_ut_och_hamtas_inte_ur_en_repr():
    import yaml

    assert vb._period(None) == "null"
    assert yaml.safe_load(f"p: {vb._period({'start': 2022, 'slut': 2025})}")["p"] == {
        "start": 2022,
        "slut": 2025,
    }
    assert yaml.safe_load(f"p: {vb._period('2022-2025')}")["p"] == "2022-2025"
