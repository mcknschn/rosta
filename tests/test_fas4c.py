"""Fas 4c — testtvingad förregistrerad rubrik (docs/done/fas4c_rubrik.md, version 2).

Dessa invarianter låser de delar av rubriken som kan kontrolleras mekaniskt: den SYMMETRISKA
evidensgrinden (§5), den generaliserade exkluderingsregeln (§7) och att rubrikdokumentet finns
och pinnar grindens trösklar.

Grinden är symmetrisk sedan [ADR 0006](../docs/adr/0006-evidensgrinden-ar-symmetrisk.md): den
gäller varje liggarpost OAVSETT VERKAN, inte bara `direction: negative`. Testerna nedan filtrerar
därför aldrig på verkan.

Godkännandetestet är ett REGELTEST och aldrig ett utfallstest. Ingenting här mäter andelen claims
ur poster med positiv verkan. Ett sådant test vore ett täckningsmål på riktning, och rubriken §8
förbjuder täckningsmål uttryckligen (ADR 0006 punkt 7).
"""

from __future__ import annotations

from pipeline import ROOT, config

_RUBRIK = ROOT / "docs" / "done" / "fas4c_rubrik.md"
_STRONG_LEVELS = {"authority_evaluation", "systematic_review"}
_OK_CONFIDENCE = {"medium", "high"}


def _passes_gate(entry: dict) -> bool:
    """De två maskinellt prövbara villkoren i §5. Villkor 3 (exakt indikator, ingen
    sidoeffekt-proxy) är ett mänskligt omdöme och bärs av `admitted` i configen."""
    return entry["evidence_level"] in _STRONG_LEVELS and entry["confidence"] in _OK_CONFIDENCE


def _excluded() -> set[str]:
    return set(config.scoring()["B_evidens"].get("coverage_exclude", []))


def test_every_admitted_entry_passes_the_symmetric_b_gate() -> None:
    # GODKÄNNANDETESTET (#26): varje liggarpost som får bidra till B passerar SAMMA grind,
    # oavsett verkan. En ny post som inte gör det fäller sviten i stället för att tyst falla
    # bort. Före ADR 0006 gällde grinden bara direction:negative, och 13 av 42 positiva poster
    # hade inte klarat den.
    for e in config.admitted_ledger_entries():
        assert _passes_gate(e), (
            f"post passerar inte den symmetriska grinden: {e['policy_type']} "
            f"(verkan {e['direction']}, {e['evidence_level']}, confidence {e['confidence']})"
        )


def test_lifted_entries_are_flagged_with_a_reason_and_actually_fail_the_gate() -> None:
    # §5 + ADR 0006 punkt 2: en utlyft post raderas inte, den flaggas. Varje utlyft post måste
    # (a) ha ett nedskrivet skäl och (b) faktiskt falla på grinden. Utan (b) vore `admitted`
    # en bakdörr för att lyfta ut en post som klarar grinden, alltså ett ad hoc-undantag.
    for e in config.evidence_ledger()["entries"]:
        if config.entry_admitted(e):
            continue
        assert e["admitted"] is False, (
            f"admitted måste vara exakt false när posten lyfts ut: {e['policy_type']}"
        )
        assert e.get("admission_note", "").strip(), (
            f"utlyft post saknar admission_note med skäl: {e['policy_type']}"
        )
        assert not _passes_gate(e), (
            f"post som passerar grinden får inte lyftas ut: {e['policy_type']}"
        )


def test_all_ledger_entries_document_indicator_bridge() -> None:
    # §5.3: varje post måste skriva ut indikator-bryggan i 'note' (ingen tyst sidoeffekt-proxy).
    # Kravet gällde tidigare bara negativa poster. Efter ADR 0006 gäller det alla, eftersom
    # sidoeffekt-proxy är samma fel oavsett verkan.
    for e in config.evidence_ledger()["entries"]:
        assert e.get("note", "").strip(), (
            f"post saknar 'note' med indikator-brygga: {e['policy_type']}"
        )


def test_lifted_entries_produce_no_claims() -> None:
    # Beteendet, inte bara flaggan: en utlyft post får inte nå B via pipeline/positions.py,
    # inte ens när ett parti har en källbelagd ståndpunkt på åtgärdstypen.
    from pipeline import positions

    lifted = {
        e["policy_type"] for e in config.evidence_ledger()["entries"]
        if not config.entry_admitted(e)
    }
    assert lifted, "inga utlyfta poster — testet skyddar då ingenting"
    claims = positions.build_evidence_effect_claims()
    for cl in claims:
        policy = cl["id"].split(":")[3]
        assert policy not in lifted, f"utlyft post gav ett claim: {policy}"


def test_lifted_entries_are_outside_the_coverage_denominator() -> None:
    # Utlyftet ändrar VAD nämnaren innehåller, aldrig HUR den räknas (B5 rörs inte, #26).
    # En utlyft åtgärdstyp är inte kodbar och får därför inte stå kvar i T_s.
    from pipeline import scorerun

    lifted = {
        e["policy_type"] for e in config.evidence_ledger()["entries"]
        if not config.entry_admitted(e)
    }
    codable = scorerun._b_codable_types_by_submeasure()
    for cat, by_sub in codable.items():
        for sub, types in by_sub.items():
            assert not (types & lifted), (
                f"utlyft åtgärdstyp ligger kvar i täckningsnämnaren: {cat}/{sub} "
                f"{sorted(types & lifted)}"
            )


def test_coverage_exclude_is_principled() -> None:
    # §7: ingen ad hoc-exkludering. Varje exkluderad policy_type måste (a) finnas i liggaren,
    # (b) ha ett dokumenterat skäl i coverage_exclude_reasons och (c) ange en principiell grund.
    # E1 (sidoeffekt-proxy) är RIKTNINGSNEUTRAL efter ADR 0006 punkt 6 och prövas därför inte
    # mot verkan. E2 (inert per konstruktion) prövas fortfarande, eftersom den grunden PÅSTÅR
    # något mekaniskt kontrollerbart: att posten har signed_direction 0.
    b = config.scoring()["B_evidens"]
    excluded = set(b.get("coverage_exclude", []))
    reasons = b.get("coverage_exclude_reasons", {})
    signed = config.claims()["aggregation"]["signed_direction"]
    ledger = {e["policy_type"]: e for e in config.evidence_ledger()["entries"]}
    for pt in excluded:
        assert pt in ledger, f"exkluderad policy_type saknas i liggaren: {pt}"
        reason = reasons.get(pt, "").strip()
        assert reason, f"exkluderad policy_type saknar skäl: {pt}"
        assert reason.startswith(("E1", "E2")), (
            f"exkluderingsskäl anger ingen principiell grund (E1/E2) för {pt}: {reason!r}"
        )
        if reason.startswith("E2"):
            assert signed.get(ledger[pt]["direction"], 0) == 0, (
                f"E2 påstår inert men posten är kodbar: {pt} ({ledger[pt]['direction']})"
            )


def test_lifted_and_coverage_excluded_are_separate_mechanisms() -> None:
    # §5 och §7 är två olika regler. En utlyft post är varken kodbar eller i nämnaren, så den
    # ska inte också stå i coverage_exclude — det vore samma beslut nedskrivet två gånger, och
    # de två kopiorna skulle kunna glida isär.
    lifted = {
        e["policy_type"] for e in config.evidence_ledger()["entries"]
        if not config.entry_admitted(e)
    }
    assert not (lifted & _excluded()), (
        f"åtgärdstyp både utlyft och coverage_exclude: {sorted(lifted & _excluded())}"
    )


def test_rubrik_doc_present_and_pins_symmetric_gate() -> None:
    # Rubriken är den förregistrerade referensen båda spåren citerar. Den får inte tyst
    # försvinna, och grindens trösklar + symmetrin + den riktningsblinda sökregeln ska stå
    # skrivna i den (skydd mot drift).
    assert _RUBRIK.exists(), "docs/done/fas4c_rubrik.md saknas (förregistrerad rubrik)"
    text = _RUBRIK.read_text(encoding="utf-8")
    for needle in (
        "version 2",
        "authority_evaluation",
        "systematic_review",
        "Den symmetriska evidensgrinden",
        "oavsett verkan",
        "Sökregeln: källstyrd och riktningsblind",
        "B-grön-mandatet är avvecklat",
    ):
        assert needle in text, f"rubriken pinnar inte {needle!r}"
