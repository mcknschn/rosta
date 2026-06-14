"""Fas 4c — testtvingad förregistrerad rubrik (docs/done/fas4c_rubrik.md).

Dessa invarianter låser de delar av rubriken som kan kontrolleras mekaniskt:
negativ-riktnings-grinden (§5), den generaliserade exkluderingsregeln (§7) och att
rubrikdokumentet finns och pinnar grindens trösklar. Plan A:s nya liggar-poster måste
passera dessa; Plan B rör inte liggaren men dokumentet ska finnas.
"""

from __future__ import annotations

from pipeline import ROOT, config

_RUBRIK = ROOT / "docs" / "done" / "fas4c_rubrik.md"
_STRONG_LEVELS = {"authority_evaluation", "systematic_review"}
_OK_CONFIDENCE = {"medium", "high"}


def _excluded() -> set[str]:
    return set(config.scoring()["B_evidens"].get("coverage_exclude", []))


def test_negative_direction_entries_pass_b_gate() -> None:
    # §5: en direction:negative-post som FÅR bidra till B (ej exkluderad) måste vila på robust
    # evidens — authority_evaluation/systematic_review + confidence >= medium. Aldrig enskild
    # studie/expertutlåtande för ett negativt (politiskt laddat) B-bidrag.
    excluded = _excluded()
    for e in config.evidence_ledger()["entries"]:
        if e["direction"] != "negative" or e["policy_type"] in excluded:
            continue
        assert e["evidence_level"] in _STRONG_LEVELS, (
            f"negativ post passerar inte grinden (svag evidensnivå): {e['policy_type']} "
            f"({e['evidence_level']})"
        )
        assert e["confidence"] in _OK_CONFIDENCE, (
            f"negativ post passerar inte grinden (låg confidence): {e['policy_type']}"
        )


def test_negative_direction_entries_document_indicator_bridge() -> None:
    # §5.3: varje negativ post måste skriva ut indikator-bryggan i 'note' (ingen tyst sidoeffekt-proxy).
    for e in config.evidence_ledger()["entries"]:
        if e["direction"] != "negative":
            continue
        assert e.get("note", "").strip(), (
            f"negativ post saknar 'note' med indikator-brygga: {e['policy_type']}"
        )


def test_coverage_exclude_is_principled() -> None:
    # §7: ingen ad hoc-exkludering. Varje exkluderad policy_type måste (a) finnas i liggaren,
    # (b) ha ett dokumenterat skäl i coverage_exclude_reasons, och (c) faktiskt motsvara en
    # principiell grund: E1 (direction negative) eller E2 (mixed/unclear -> inert).
    b = config.scoring()["B_evidens"]
    excluded = set(b.get("coverage_exclude", []))
    reasons = b.get("coverage_exclude_reasons", {})
    ledger = {e["policy_type"]: e for e in config.evidence_ledger()["entries"]}
    for pt in excluded:
        assert pt in ledger, f"exkluderad policy_type saknas i liggaren: {pt}"
        assert reasons.get(pt, "").strip(), f"exkluderad policy_type saknar skäl: {pt}"
        direction = ledger[pt]["direction"]
        assert direction in {"negative", "mixed", "unclear"}, (
            f"exkludering ej principiell (E1 negativ / E2 inert) för {pt}: direction={direction}"
        )


def test_rubrik_doc_present_and_pins_negative_gate() -> None:
    # Rubriken är den förregistrerade referensen båda spåren citerar. Den får inte tyst försvinna,
    # och negativ-grindens trösklar ska stå skrivna i den (skydd mot drift).
    assert _RUBRIK.exists(), "docs/done/fas4c_rubrik.md saknas (förregistrerad rubrik)"
    text = _RUBRIK.read_text(encoding="utf-8")
    for needle in ("authority_evaluation", "systematic_review", "negativ-riktnings-grinden"):
        assert needle in text, f"rubriken pinnar inte '{needle}'"
