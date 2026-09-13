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
    urval = vb.dra_urval(vb.las_bakat(), fro=20260913, per_parti=25)
    delurval = vb.dra_urval(urval, fro=460513, per_parti=5)
    assert len(delurval) == 40
    assert {u.id for u in delurval} <= {u.id for u in urval}


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
