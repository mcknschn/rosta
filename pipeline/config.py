"""Laddning och validering av config/*.yaml.

Configen är modellens auktoritativa specifikation (helt automatisk betygssättning,
inget mänskligt omdöme utanför config). Invarianterna nedan testas i tests/test_config.py.
"""

from __future__ import annotations

from functools import cache
from typing import Any

import yaml

from . import CONFIG_DIR


def _load(name: str) -> dict[str, Any]:
    path = CONFIG_DIR / name
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


@cache
def categories() -> dict[str, Any]:
    return _load("categories.yaml")


@cache
def scoring() -> dict[str, Any]:
    return _load("scoring.yaml")


@cache
def claims() -> dict[str, Any]:
    return _load("claims.yaml")


@cache
def mappings() -> dict[str, Any]:
    return _load("mappings.yaml")


@cache
def subnational_municipalities() -> dict[str, Any]:
    return _load("subnational_municipalities.yaml")


@cache
def sources() -> dict[str, Any]:
    return _load("sources.yaml")


@cache
def evidence_ledger() -> dict[str, Any]:
    return _load("evidence_ledger.yaml")


def entry_admitted(entry: Any) -> bool:
    """Får liggarposten bidra till B? Den symmetriska evidensgrinden (rubriken §5).

    Grinden gäller OAVSETT VERKAN (ADR 0006): evidence_level i {authority_evaluation,
    systematic_review}, confidence >= medium, och evidens som avser exakt den betygsatta
    indikatorn utan sidoeffekt-proxy. Det tredje villkoret är ett mänskligt omdöme och kan
    inte räknas fram, så domen står i configen som `admitted: false` + `admission_note`.
    Fältet saknas på en post som passerar; bara ett uttryckligt false lyfter ut den.

    Utlyft post RADERAS INTE. Den står kvar med källa och skäl, men hålls utanför både
    claims-byggandet (pipeline/positions.py) och täckningsnämnaren (scorerun), så källspåret
    finns kvar utan att posten ger poäng.

    tests/test_fas4c.py tvingar att varje admitterad post faktiskt passerar de två
    maskinellt prövbara villkoren. En ny post som inte gör det fäller sviten i stället för
    att tyst falla bort.
    """
    return entry.get("admitted", True) is not False


def admitted_ledger_entries() -> list[dict[str, Any]]:
    """Liggarens poster som passerar grinden. Enda vägen in i B."""
    return [e for e in (evidence_ledger().get("entries") or []) if entry_admitted(e)]


@cache
def party_positions() -> dict[str, Any]:
    return _load("party_positions.yaml")


@cache
def coverage_allowlist() -> dict[str, Any]:
    return _load("coverage_allowlist.yaml")


@cache
def budget_ramar() -> dict[str, Any]:
    return _load("budget_ramar.yaml")


@cache
def a_forankring() -> dict[str, Any]:
    return _load("a_forankring.yaml")


@cache
def skjutningar_sprangningar() -> dict[str, Any]:
    return _load("skjutningar_sprangningar.yaml")


@cache
def personal_varnpliktiga() -> dict[str, Any]:
    return _load("personal_varnpliktiga.yaml")


@cache
def ukraina_stod() -> dict[str, Any]:
    return _load("ukraina_stod.yaml")


@cache
def asyl_handlaggningstid() -> dict[str, Any]:
    return _load("asyl_handlaggningstid.yaml")


@cache
def personalstyrka_forsvarsmakten() -> dict[str, Any]:
    return _load("personalstyrka_forsvarsmakten.yaml")


@cache
def forsvarsvilja() -> dict[str, Any]:
    return _load("forsvarsvilja.yaml")


@cache
def aterfall_i_brott() -> dict[str, Any]:
    return _load("aterfall_i_brott.yaml")


@cache
def hackande_faglar_skog() -> dict[str, Any]:
    return _load("hackande_faglar_skog.yaml")


@cache
def vdem_demokrati() -> dict[str, Any]:
    return _load("vdem_demokrati.yaml")


@cache
def effektbrist() -> dict[str, Any]:
    return _load("effektbrist.yaml")


@cache
def materielleveransutfall() -> dict[str, Any]:
    return _load("materielleveransutfall.yaml")


def party_codes() -> list[str]:
    return [p["code"] for p in categories()["parties"]]


def category_ids() -> list[str]:
    return [c["id"] for c in categories()["categories"]]


class ConfigError(ValueError):
    """Brott mot en modellinvariant i config."""


def _require(present: bool, msg: str) -> None:
    if not present:
        raise ConfigError(msg)


def validate(tolerance: float = 1e-6) -> None:
    """Kontrollerar modellinvarianterna. Höjer ConfigError vid fel (aldrig KeyError)."""
    cats = categories()
    _require("categories" in cats, "categories.yaml saknar 'categories'")
    _require("subscore_weights" in cats, "categories.yaml saknar 'subscore_weights'")

    cat_list = cats["categories"]
    if len(cat_list) != 7:
        raise ConfigError(f"Förväntade 7 kategorier, fann {len(cat_list)}")

    std_sum = 0.0
    for c in cat_list:
        _require("id" in c, "En kategori saknar 'id'")
        for field in ("standard_weight", "submeasures"):
            _require(field in c, f"Kategori '{c.get('id', '?')}' saknar '{field}'")
        std_sum += c["standard_weight"]
    if abs(std_sum - 100) > tolerance:
        raise ConfigError(f"Standardvikterna summerar till {std_sum}, inte 100")

    sub_w = cats["subscore_weights"]
    if abs(sum(sub_w.values()) - 100) > tolerance:
        raise ConfigError(f"Delpoängvikterna (categories) summerar till {sum(sub_w.values())}, inte 100")

    for c in cat_list:
        sub_ids = set()
        for s in c["submeasures"]:
            _require({"id", "weight"} <= s.keys(), f"Submått i '{c['id']}' saknar id/weight")
            sub_ids.add(s["id"])
        wsum = sum(s["weight"] for s in c["submeasures"])
        if abs(wsum - 100) > tolerance:
            raise ConfigError(f"Submåttsvikterna i '{c['id']}' summerar till {wsum}, inte 100")
        for ind in c.get("indicators", []):
            _require(
                {"id", "submeasure"} <= ind.keys(),
                f"Indikator i '{c['id']}' saknar id/submeasure",
            )
            _validate_indicator_direction(c["id"], ind)
            if ind["submeasure"] not in sub_ids:
                raise ConfigError(
                    f"Indikator {c['id']}/{ind['id']} pekar på okänt submått '{ind['submeasure']}'"
                )

    parties = party_codes()
    if len(parties) != len(set(parties)):
        raise ConfigError("Dubbletter i partikoder")

    _validate_ledger_against_exclusions()
    _validate_scoring(sub_w, tolerance)


VALID_DIRECTIONS = frozenset({"up", "down"})

# Uteslutningsskälen och vad vart och ett betyder i klarspråk (ADR 0011 punkt 5). Namnet pekar
# på den regel som fäller, aldrig på symtomet i det enskilda fallet, så det går att återanvända
# på nästa indikator. Mappningen är enda källan: metodrutan läser den, och den giltiga mängden
# ÄR dess nycklar, så ett fjärde skäl kan aldrig passera valideringen utan sin förklaring.
EXCLUSION_REASONS = {
    "gransfel": "frågan ägs redan av en annan delpoäng",
    "giltighetsfel": "utfallet kan inte tillskrivas ett parti",
    "neutralitetsfel": "det bättre hållet går inte att ange utan att ta ett partis parti",
}
VALID_EXCLUSIONS = frozenset(EXCLUSION_REASONS)


def _validate_indicator_direction(cat_id: str, ind: dict[str, Any]) -> None:
    """Riktning eller Uteslutningsskäl, aldrig båda och aldrig ingetdera (ADR 0011 punkt 3-4).

    Riktning är ett besked om indikatorn, alltså vilket håll som är bättre. Uteslutningsskäl
    är ett besked om modellen, alltså varför indikatorn inte poängsätts. Ett fält som bar
    båda dolde det ena med det andra, vilket är precis vad värdet `target` gjorde.

    Formen gör "utesluten utan skäl" omöjlig att skriva: fältet `exclusion` ÄR skälet, och
    varje utesluten indikator bär dessutom `reopen_if`, alltså vad som måste ändras för att
    felet ska vara borta (ADR 0011 punkt 8).
    """
    ref = f"{cat_id}/{ind.get('id', '?')}"
    has_dir, has_exc = "direction" in ind, "exclusion" in ind
    if has_dir and has_exc:
        raise ConfigError(
            f"Indikator {ref} bär både direction och exclusion (ADR 0011: aldrig båda)"
        )
    if not has_dir and not has_exc:
        raise ConfigError(
            f"Indikator {ref} saknar både direction och exclusion (ADR 0011: aldrig ingetdera)"
        )
    if has_dir:
        if ind["direction"] not in VALID_DIRECTIONS:
            raise ConfigError(
                f"Ogiltig riktning '{ind['direction']}' i {ref} "
                f"(tillåtna: {', '.join(sorted(VALID_DIRECTIONS))})"
            )
        return
    if ind["exclusion"] not in VALID_EXCLUSIONS:
        raise ConfigError(
            f"Ogiltigt uteslutningsskäl '{ind['exclusion']}' i {ref} "
            f"(tillåtna: {', '.join(sorted(VALID_EXCLUSIONS))})"
        )
    if not str(ind.get("reopen_if", "")).strip():
        raise ConfigError(
            f"Utesluten indikator {ref} saknar reopen_if, alltså återöppningsvillkoret "
            "(ADR 0011 punkt 8)"
        )


def excluded_indicators() -> dict[tuple[str, str], str]:
    """(kategori, indikator) -> Uteslutningsskäl. Enda källan till vad som är uteslutet."""
    return {
        (cat["id"], ind["id"]): ind["exclusion"]
        for cat in categories()["categories"]
        for ind in cat.get("indicators", [])
        if "exclusion" in ind
    }


def _validate_ledger_against_exclusions() -> None:
    """En utesluten indikator får inte bära en evidenspost (ADR 0011 punkt 7).

    Grinden går på uteslutningsfältet och ALDRIG på om ett syskon råkar bära riktning.
    Utan den beror utfallet på formen: en post mot `inflation` ignorerades tyst, eftersom
    hela dess undermått låg utanför B:s nämnare, medan en post mot
    `forsvarsanslag_andel_bnp` skulle räknas tyst, eftersom syskonindikatorn bär `up`.
    Tyst räkna och tyst ignorera är båda fel svar. Pipen ska säga ifrån.

    Grinden gäller varje post i liggaren, även en utlyft (`admitted: false`). Utlyftningen
    är ADR 0006:s evidensgrind och svarar på en annan fråga, alltså om posten HÅLLER, inte
    om indikatorn går att poängsätta.
    """
    excluded = excluded_indicators()
    if not excluded:
        return
    for e in evidence_ledger().get("entries") or []:
        key = (e.get("category"), e.get("indicator"))
        if key in excluded:
            raise ConfigError(
                f"Evidensposten '{e.get('policy_type')}' pekar på den uteslutna indikatorn "
                f"{key[0]}/{key[1]} ({excluded[key]}). En utesluten indikator poängsätts inte "
                "och får därför inte bära en evidenspost (ADR 0011 punkt 7)."
            )


def _validate_scoring(sub_w: dict[str, Any], tolerance: float) -> None:
    """Invarianter i scoring.yaml som score.py förlitar sig på."""
    s = scoring()
    _require("subscore_weights" in s, "scoring.yaml saknar 'subscore_weights'")
    sc = s["subscore_weights"]
    _require(set("ABCD") <= sc.keys(), "scoring.subscore_weights saknar A/B/C/D")
    if abs(sum(sc.values()) - 1.0) > tolerance:
        raise ConfigError(f"scoring.subscore_weights summerar till {sum(sc.values())}, inte 1.0")
    for letter, key in (("A", "A_agerande"), ("B", "B_evidens"), ("C", "C_ansvar"), ("D", "D_resultat")):
        if abs(sc[letter] * 100 - sub_w[key]) > tolerance:
            raise ConfigError(
                f"scoring.subscore_weights['{letter}'] matchar inte categories['{key}']"
            )

    _require("uncertainty" in s, "scoring.yaml saknar 'uncertainty'")
    unc = s["uncertainty"]
    for field in ("confidence_numeric", "default_subscore_certainty", "max_interval_halfwidth"):
        _require(field in unc, f"scoring.uncertainty saknar '{field}'")
    conf = unc["confidence_numeric"]
    for level, val in conf.items():
        if not (0.0 <= val <= 1.0):
            raise ConfigError(f"confidence_numeric['{level}'] = {val} utanför [0,1]")
    certainty = unc["default_subscore_certainty"]
    if set(certainty) != set("ABCD"):
        raise ConfigError(f"default_subscore_certainty måste ha A/B/C/D, har {sorted(certainty)}")
    for letter, level in certainty.items():
        if level not in conf:
            raise ConfigError(f"default_subscore_certainty['{letter}']='{level}' saknas i confidence_numeric")
    if not isinstance(unc["max_interval_halfwidth"], (int, float)):
        raise ConfigError("max_interval_halfwidth måste vara ett tal")

    # Konfidensnivåer som scorerun läser som overrides måste finnas i confidence_numeric,
    # annars blir det ett bart KeyError djupt i score.resolve_confidence_numeric (jfr A/B/C/D).
    extra_levels = {
        "D_resultat.measured_confidence": s.get("D_resultat", {}).get("measured_confidence"),
        "D_resultat.not_applicable_confidence": s.get("D_resultat", {}).get("not_applicable_confidence"),
        "B_evidens.missing_all_confidence": s.get("B_evidens", {}).get("missing_all_confidence"),
    }
    for name, level in extra_levels.items():
        if level is not None and level not in conf:
            raise ConfigError(f"scoring.{name}='{level}' saknas i confidence_numeric")

    # B5: täckningsmått-läget måste vara ett känt värde — ogiltigt läge får ALDRIG tyst
    # falla tillbaka till legacy (docs/done/b_coverage_krympning_spec.md §7).
    b_mode = s.get("B_evidens", {}).get("coverage_mode")
    if b_mode is not None and b_mode not in ("policy_type_count", "weighted_submeasure_depth"):
        raise ConfigError(
            f"B_evidens.coverage_mode={b_mode!r} är ogiltigt "
            "(tillåtna: policy_type_count, weighted_submeasure_depth)"
        )

    # A normaliseras inte längre (ADR 0005): båda halvorna mäts mot en historisk förankring och
    # avbildas med score.net_support_to_score, samma avbildning som B. En kvarlämnad
    # normalization.per_subscore.A vore en config som beskriver ett beteende koden inte har, och
    # den regeln är hela skälet till att nyckeln en gång lästes här. Den ska alltså vara borta.
    if "A" in (s.get("normalization") or {}).get("per_subscore", {}):
        raise ConfigError(
            "normalization.per_subscore.A finns kvar men A normaliseras inte längre (ADR 0005)"
        )
    # C normaliseras däremot fortfarande, och nyckeln STYR den (scorerun.category_c läser den).
    # Saknad eller felstavad nyckel får aldrig tyst falla tillbaka på rank.
    c_norm = (s.get("normalization") or {}).get("per_subscore", {}).get("C")
    if c_norm not in ("rank", "minmax"):
        raise ConfigError(
            f"normalization.per_subscore.C={c_norm!r} är ogiltigt (tillåtna: rank, minmax)"
        )
    semantics = s.get("scale_semantics") or {}
    if "A" in (semantics.get("relative") or []):
        raise ConfigError("scale_semantics: A är absolut efter ADR 0005, inte relativ")

    # C3: subnationell D-config — validera struktur tidigt (jfr coverage_mode). Frånvaro är OK
    # (legacy nationell D); finns blocket måste det vara välformat.
    subn = s.get("D_resultat", {}).get("subnational")
    if subn is not None:
        if not isinstance(subn.get("enabled"), bool):
            raise ConfigError("D_resultat.subnational.enabled måste vara true/false")
        all_subids = {sm["id"] for c in categories()["categories"] for sm in c["submeasures"]}
        for sid, w in (subn.get("submeasure_level_weights") or {}).items():
            if sid not in all_subids:
                raise ConfigError(f"D_resultat.subnational refererar okänt submått '{sid}'")
            tot = float(w.get("national", 0)) + float(w.get("region", 0))
            if abs(tot - 1.0) > tolerance:
                raise ConfigError(
                    f"D_resultat.subnational.submeasure_level_weights['{sid}'] "
                    f"summerar till {tot}, inte 1.0"
                )
        if subn.get("region_weighting", "equal") not in ("equal", "population"):
            raise ConfigError(
                f"D_resultat.subnational.region_weighting={subn.get('region_weighting')!r} "
                "ogiltigt (tillåtna: equal, population)"
            )

    # neutral i normalisering måste matcha score.py-defaulten (2.5) för att undvika drift.
    neutral = s.get("normalization", {}).get("default", {}).get("neutral")
    if neutral is not None and abs(neutral - 2.5) > tolerance:
        raise ConfigError(f"normalization.default.neutral={neutral}, förväntat 2.5 (score.py-default)")
