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
def skjutningar_sprangningar() -> dict[str, Any]:
    return _load("skjutningar_sprangningar.yaml")


@cache
def personal_varnpliktiga() -> dict[str, Any]:
    return _load("personal_varnpliktiga.yaml")


@cache
def ukraina_stod() -> dict[str, Any]:
    return _load("ukraina_stod.yaml")


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

    valid_dirs = {"up", "down", "target"}
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
                {"id", "direction", "submeasure"} <= ind.keys(),
                f"Indikator i '{c['id']}' saknar id/direction/submeasure",
            )
            if ind["direction"] not in valid_dirs:
                raise ConfigError(f"Ogiltig riktning '{ind['direction']}' i {c['id']}/{ind['id']}")
            if ind["submeasure"] not in sub_ids:
                raise ConfigError(
                    f"Indikator {c['id']}/{ind['id']} pekar på okänt submått '{ind['submeasure']}'"
                )

    parties = party_codes()
    if len(parties) != len(set(parties)):
        raise ConfigError("Dubbletter i partikoder")

    _validate_scoring(sub_w, tolerance)


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

    # neutral i normalisering måste matcha score.py-defaulten (2.5) för att undvika drift.
    neutral = s.get("normalization", {}).get("default", {}).get("neutral")
    if neutral is not None and abs(neutral - 2.5) > tolerance:
        raise ConfigError(f"normalization.default.neutral={neutral}, förväntat 2.5 (score.py-default)")
