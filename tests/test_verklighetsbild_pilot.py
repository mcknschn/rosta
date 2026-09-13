"""De tio godkännandetesterna för Verklighetsbildpiloten.

Ordagrant ur ADR 0016. Ingen regel nämner hur många påståenden som visade sig felaktiga,
och ingen regel nämner ett parti.

  1. Kodboken är låst och versionsmärkt före den första kodade utsagan.
  2. Urvalsdragningen är reproducerbar. Frö och metod står i filen.
  3. Ingen fil i piloten bär en sanningsandel per parti.
  4. Varje kodad utsaga bär antingen minst en relation eller exakt en bortfallskod.
  5. Tröskelvärdena står nedskrivna före kodningen och är oförändrade efteråt.
  6. Två modellkodningar finns, från olika leverantörer, och ingen har sett den andras svar.
  7. Alfa redovisas för alla fyra momenten, med förväxlingsmatris.
  8. Ingen text framställer delurvalet som facit, validering eller riktighet.
  9. Den frysta framåtkorpusen bär dokumenthash, fasta utsage-id och en brytpunkt.
 10. Klaras inte tröskeln finns ett daterat avslagsskäl i repot.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest
import yaml

from pipeline.tools import verklighetsbild as vb

ROT = Path(__file__).resolve().parents[1]
PILOT = ROT / "docs" / "verklighetsbild_pilot"
KONFIG = ROT / "config" / "verklighetsbild"
KODBOK = PILOT / "kodbok_pilot.md"
FORHANDSREG = PILOT / "forhandsregistrering.md"


def _las(fil: Path) -> dict:
    return yaml.safe_load(fil.read_text(encoding="utf-8"))


def _kodningsfiler() -> list[Path]:
    return sorted(KONFIG.glob("kodning_*.yaml"))


def _lades_till_i(fil: Path) -> str | None:
    """Datum för den commit som lade till filen, eller None utanför ett git-träd."""
    try:
        ut = subprocess.run(
            ["git", "log", "--diff-filter=A", "--format=%cI", "--", str(fil.relative_to(ROT))],
            cwd=ROT, capture_output=True, text=True, timeout=30, check=False,
        )
    except (OSError, subprocess.SubprocessError):  # pragma: no cover - beror på miljön
        return None
    rader = [r for r in ut.stdout.splitlines() if r.strip()]
    return rader[-1] if rader else None


# ------------------------------------------------------------------------- regel 1


def test_1_kodboken_ar_last_och_versionsmarkt():
    text = KODBOK.read_text(encoding="utf-8")
    assert "Version: 1" in text
    assert "Status: **låst**" in text
    assert "Låst: 2026-09-13, före den första kodade utsagan" in text


def test_1_kodboken_committades_fore_den_forsta_kodningen():
    """Ordningen ska gå att se på commit-datum, inte bara på en rad i filen."""
    kodboken = _lades_till_i(KODBOK)
    if kodboken is None:
        pytest.skip("inget git-träd att läsa commit-datum ur")
    kodningar = _kodningsfiler()
    if not kodningar:
        pytest.skip("ingen kodning är committad än")
    for fil in kodningar:
        kodningen = _lades_till_i(fil)
        if kodningen is not None:
            assert kodboken < kodningen, f"{fil.name} committades före kodboken"


# ------------------------------------------------------------------------- regel 2


def test_2_urvalet_bar_fro_och_metod():
    urval = _las(KONFIG / "urval_pilot.yaml")
    assert urval["fro"] == vb.FRO_URVAL
    assert urval["per_parti"] == vb.PER_PARTI
    assert "random.Random" in urval["metod"]
    assert "utan återläggning" in (KONFIG / "urval_pilot.yaml").read_text(encoding="utf-8")


def test_2_urvalet_gar_att_dra_om_och_ger_samma_200():
    urval = _las(KONFIG / "urval_pilot.yaml")
    omdraget = vb.dra_urval(vb.las_bakat(), fro=urval["fro"], per_parti=urval["per_parti"])
    assert [u.id for u in omdraget] == [r["id"] for r in urval["urval"]]


def test_2_kallfilernas_hash_matchar_det_som_drogs():
    """Ändras en källfil ändras hashen, och urvalet måste dras om."""
    for post in _las(KONFIG / "urval_pilot.yaml")["korpus"]:
        assert vb.sha256(vb.KALLKATALOG / post["fil"]) == post["sha256"], post["fil"]


# ------------------------------------------------------------------------- regel 3

# De tre sanningskodvärdena hör hemma i produktionskodboken och ingenstans i piloten.
FORBJUDNA_NYCKLAR = re.compile(r"^\s*(sanningsandel|andel_sanna|riktighet|stammer\w*)\s*:", re.M)
FORBJUDNA_VARDEN = re.compile(r":\s*(stammer|stammer_inte|skev)\s*$", re.M)


def test_3_ingen_pilotfil_bar_en_sanningsandel():
    for fil in sorted(KONFIG.glob("*.yaml")) + sorted(PILOT.glob("*.md")):
        text = fil.read_text(encoding="utf-8")
        assert not FORBJUDNA_NYCKLAR.search(text), f"{fil.name} bär ett sanningsfält"
        assert not FORBJUDNA_VARDEN.search(text), f"{fil.name} bär ett sanningskodvärde"


def test_3_kodboken_sager_uttryckligen_att_piloten_inte_kodar_sanning():
    text = KODBOK.read_text(encoding="utf-8")
    assert "Piloten avgör inte om ett påstående är sant" in text


# ------------------------------------------------------------------------- regel 4


def test_4_varje_kodad_utsaga_bar_relation_eller_exakt_en_kod():
    kodningar = _kodningsfiler()
    if not kodningar:
        pytest.skip("ingen kodning är committad än")
    for fil in kodningar:
        dokument = _las(fil)
        for post in dokument["utsagor"]:
            granskning = vb.granska_kodning(post)
            assert granskning.fel == [], f"{fil.name}: {granskning.fel}"


def test_4_bortfallskoderna_ar_adrns_sju_och_inga_andra():
    assert len(vb.BORTFALLSKODER) == 7
    assert set(vb.BORTFALLSKODER) == {
        "framtida_utfall",
        "normativ",
        "otillracklig_kontext",
        "ingen_kompatibel_indikator",
        "flera_operationaliseringar",
        "data_saknas",
        "period_saknas",
    }
    for fil in _kodningsfiler():
        for post in _las(fil)["utsagor"]:
            kod = post.get("bortfall")
            assert kod is None or kod in vb.BORTFALLSKODER, f"{fil.name}: {kod}"


# ------------------------------------------------------------------------- regel 5

TROSKELRADER = (
    "Designviktat totalt utbyte minst 20 procent av de 200 kodade utsagorna",
    "Minst 5 prövbara relationer för vart och ett av de åtta partierna",
    "Ger ett parti 0 till 2 relationer faller per-parti-redovisningen",
    "Ger ett parti 3 eller 4 relationer totalundersöks det partiets material innan beslut",
    "redovisas oavsett utfall",
)


def test_5_alla_fem_troskelvarden_star_nedskrivna():
    text = FORHANDSREG.read_text(encoding="utf-8")
    for rad in TROSKELRADER:
        assert rad in text, rad


def test_5_koden_bar_samma_troskelvarden_som_filen():
    """En tröskel som bara står i prosa kan glida ifrån den som räknar."""
    assert vb.TROSKEL_UTBYTE == 0.20
    assert vb.TROSKEL_RELATIONER_PER_PARTI == 5
    assert vb.ALFA_HALLER == 0.800
    assert vb.ALFA_TENTATIVT == 0.667
    text = FORHANDSREG.read_text(encoding="utf-8")
    assert "`>= 0,800`" in text
    assert "`0,667` till `0,800`" in text


def test_5_forhandsregistreringen_committades_fore_kodningen():
    reg = _lades_till_i(FORHANDSREG)
    if reg is None:
        pytest.skip("inget git-träd att läsa commit-datum ur")
    for fil in _kodningsfiler():
        kodningen = _lades_till_i(fil)
        if kodningen is not None:
            assert reg < kodningen, f"{fil.name} committades före tröskelvärdena"


# ------------------------------------------------------------------------- regel 6


def test_6_tva_kodningar_fran_olika_leverantorer():
    kodningar = [_las(f) for f in _kodningsfiler()]
    fulla = [d for d in kodningar if d["uppdrag"] == "full"]
    if not fulla:
        pytest.skip("ingen full kodning är committad än")
    assert len(fulla) == 2
    assert len({d["kodare"] for d in fulla}) == 2
    assert len({d["leverantor"] for d in fulla}) == 2, "kodarna delar leverantör"


def test_6_ingen_kodare_sag_den_andras_svar():
    for fil in _kodningsfiler():
        assert _las(fil)["sag_andra_kodarens_svar"] is False, fil.name


def test_6_kodarna_fick_bara_kodboken_och_blinda_id():
    """Utsage-id bär partikoden i sitt prefix, så kodaren måste få ett blint id."""
    nyckel = _las(KONFIG / "blindning.yaml")
    assert len(nyckel["full"]) == 200
    assert len(nyckel["delurval"]) == 40
    assert all(re.fullmatch(r"U-\d{3}", b) for b in nyckel["full"])
    assert all(re.fullmatch(r"D-\d{3}", b) for b in nyckel["delurval"])
    assert set(nyckel["delurval"].values()) <= set(nyckel["full"].values())
    for fil in _kodningsfiler():
        for post in _las(fil)["utsagor"]:
            assert re.fullmatch(r"[UD]-\d{3}", post["blint_id"]), post


# ------------------------------------------------------------------------- regel 7

MOMENT = ("avgransning", "provbarhet", "indikatorval", "kodvarde")


def test_7_alfa_redovisas_for_alla_fyra_momenten():
    resultat = KONFIG / "resultat.yaml"
    if not resultat.exists():
        pytest.skip("resultatet är inte räknat än")
    data = _las(resultat)
    for moment in MOMENT:
        assert moment in data["reliabilitet"], moment
        post = data["reliabilitet"][moment]
        assert "alfa" in post
        assert "besked" in post
        assert "forvaxlingsmatris" in post, f"{moment} saknar förväxlingsmatris"


def test_7_kodboken_namnger_samma_fyra_moment():
    text = KODBOK.read_text(encoding="utf-8")
    for ord_ in ("Avgränsning", "Prövbarhet", "Indikatorval", "Kodvärde"):
        assert ord_ in text, ord_


# ------------------------------------------------------------------------- regel 8

ANSPRAKSORD = re.compile(r"\b(facit|validerar|validering|validerad|riktighet)\b", re.I)
NEKANDE = re.compile(r"\b(inte|aldrig|ingen|inget|utan|saknar|avstod)\b", re.I)


def test_8_varje_ansprak_om_delurvalet_star_i_en_nekande_mening():
    """Orden får förekomma, men bara för att avvisas."""
    for fil in sorted(PILOT.glob("*.md")) + sorted(KONFIG.glob("*.yaml")):
        text = fil.read_text(encoding="utf-8")
        for mening in re.split(r"(?<=[.!?])\s+", text.replace("\n", " ")):
            if ANSPRAKSORD.search(mening):
                assert NEKANDE.search(mening), f"{fil.name}: obestritt anspråk: {mening.strip()}"


def test_8_forhandsregistreringen_skriver_ut_att_mansklig_kodare_saknas():
    text = FORHANDSREG.read_text(encoding="utf-8")
    assert "Piloten saknar mänsklig" in text
    assert "gör inget anspråk på mänsklig interkodarreliabilitet" in text


# ------------------------------------------------------------------------- regel 9


def test_9_framatkorpusen_ar_fryst_med_hash_id_och_brytpunkt():
    korpus = _las(KONFIG / "korpus_framat.yaml")
    assert str(korpus["brytpunkt"]) == vb.BRYTPUNKT
    assert korpus["brytpunkt_skal"].strip()
    assert korpus["antal"] == len(korpus["pastaenden"]) == 1073
    ids = [p["id"] for p in korpus["pastaenden"]]
    assert len(set(ids)) == len(ids)
    assert all(p["citat"] for p in korpus["pastaenden"])


def test_9_hamtmanifestet_bar_sha256_for_alla_atta_dokument():
    manifest = _las(KONFIG / "hamtmanifest.yaml")
    assert len(manifest["dokument"]) == 8
    for post in manifest["dokument"]:
        assert re.fullmatch(r"[0-9a-f]{64}", post["sha256"]), post["filnamn"]
        assert post["hamtdatum"]
        assert "url" in post, "URL-fältet ska finnas även när det är tomt"


def test_9_originaltexten_ar_oforandrad_mot_kallan():
    """Frysningen binder lydelsen. Den ska matcha markdownen tecken för tecken."""
    kallan = {u.id: u.text for u in vb.las_framat()}
    for post in _las(KONFIG / "korpus_framat.yaml")["pastaenden"]:
        assert post["citat"] == kallan[post["id"]], post["id"]


def test_9_pdferna_ligger_utanfor_git():
    gitignore = (ROT / ".gitignore").read_text(encoding="utf-8")
    assert "docs/valmanifest_2026/*.pdf" in gitignore


# ------------------------------------------------------------------------ regel 10


def test_10_ett_fallet_troskelvarde_kraver_ett_daterat_avslagsskal():
    resultat = KONFIG / "resultat.yaml"
    if not resultat.exists():
        pytest.skip("resultatet är inte räknat än")
    data = _las(resultat)
    if data["utfall"]["piloten_klaras"]:
        return
    avslag = PILOT / "avslagsskal.md"
    assert avslag.exists(), "tröskeln föll men inget avslagsskäl finns"
    text = avslag.read_text(encoding="utf-8")
    assert re.search(r"\b20\d{2}-\d{2}-\d{2}\b", text), "avslagsskälet saknar datum"


def test_10_ingen_produktionskodbok_finns_nar_troskeln_fallit():
    """Klaras inte tröskeln fortsätter ingen kodning, och produktionskodboken skrivs inte."""
    resultat = KONFIG / "resultat.yaml"
    if not resultat.exists() or _las(resultat)["utfall"]["piloten_klaras"]:
        pytest.skip("tröskeln har inte fallit")
    assert not (PILOT / "kodbok_produktion.md").exists()


# ------------------------------------------------------- kodboken mot modellen


def test_bilaga_a_matchar_categories_yaml():
    """Kodbokens indikatorlista och modellen får inte glida isär."""
    cats = yaml.safe_load((ROT / "config" / "categories.yaml").read_text(encoding="utf-8"))
    allowlist = yaml.safe_load((ROT / "config" / "coverage_allowlist.yaml").read_text(encoding="utf-8"))
    utan_serie = {(e["category"], e["indicator"]) for e in allowlist["allowlist"]}
    vantade = {
        f"| `{i['id']}` | `{i['submeasure']}` | {'nej' if (c['id'], i['id']) in utan_serie else 'ja'} |"
        for c in cats["categories"]
        for i in c["indicators"]
    }
    text = KODBOK.read_text(encoding="utf-8")
    saknade = sorted(rad for rad in vantade if rad not in text)
    assert not saknade, f"bilaga A saknar {len(saknade)} rader, bland dem {saknade[:3]}"


def test_kodarna_valde_bara_indikatorer_som_finns_i_modellen():
    cats = yaml.safe_load((ROT / "config" / "categories.yaml").read_text(encoding="utf-8"))
    kanoniska = {i["id"] for c in cats["categories"] for i in c["indicators"]}
    for fil in _kodningsfiler():
        for post in _las(fil)["utsagor"]:
            for led in post["led"]:
                if led["indikator"]:
                    assert led["indikator"] in kanoniska, f"{fil.name}: {led['indikator']}"


# ------------------------------------------------- piloten ror inte instrumentet


def test_pipen_importerar_aldrig_verklighetsbild():
    """ADR 0016: ingenting i pipen, configen eller gränssnittet ändras av det här.

    Verklighetsbild har vikt 0 och ingår inte i någon poäng. Verktyget ligger i
    pipeline/tools/ och körs för hand. Drar pipen in det har någon flyttat måttet.
    """
    pipen = sorted((ROT / "pipeline").glob("*.py")) + sorted((ROT / "pipeline" / "sources").glob("*.py"))
    assert len(pipen) > 20, "hittade för få pipelinefiler, globben är trasig"
    for fil in pipen:
        text = fil.read_text(encoding="utf-8")
        assert "verklighetsbild" not in text, f"{fil.name} drar in Verklighetsbild i pipen"


def test_verklighetsbild_star_utanfor_kategorimodellen():
    """Måtten i categories.yaml får inte veta att piloten finns."""
    for namn in ("categories.yaml", "scoring.yaml"):
        text = (ROT / "config" / namn).read_text(encoding="utf-8")
        assert "verklighetsbild" not in text.lower(), namn


# ------------------------------------------------- rapporten mot rakningen


def _svenskt(x: float) -> str:
    return f"{x:.3f}".replace(".", ",")


def test_rapportens_tal_matchar_resultatfilen():
    """Prosan får inte glida från räkningen. Varje rubriktal prövas mot resultat.yaml."""
    resultat = KONFIG / "resultat.yaml"
    rapport = PILOT / "resultat.md"
    if not (resultat.exists() and rapport.exists()):
        pytest.skip("resultatet är inte räknat än")
    data = _las(resultat)
    text = rapport.read_text(encoding="utf-8")
    utbyte = data["utbyte"]

    assert _svenskt(utbyte["designviktat"]) in text, "utbytet saknas i rapporten"
    lo, hi = utbyte["intervall_95"]
    assert _svenskt(lo) in text and _svenskt(hi) in text, "intervallet saknas"
    for moment, post in data["reliabilitet"].items():
        assert _svenskt(post["alfa"]) in text, f"alfa for {moment} saknas i rapporten"
    for parti in data["per_parti"]:
        assert parti in text, parti


def test_avslagsskalet_finns_och_namner_bada_troskelvarden():
    resultat = KONFIG / "resultat.yaml"
    if not resultat.exists() or _las(resultat)["utfall"]["piloten_klaras"]:
        pytest.skip("tröskeln har inte fallit")
    text = (PILOT / "avslagsskal.md").read_text(encoding="utf-8")
    data = _las(resultat)
    assert _svenskt(data["utbyte"]["designviktat"]) in text
    assert "0,20" in text
    assert "minst 5" in text.lower()
    assert "igen" in text.lower(), "inga villkor för att ta upp frågan igen"
