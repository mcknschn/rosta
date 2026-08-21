# Granskning B — partiståndpunkter (`config/party_positions.yaml`)

> AUTOGENERERAD av `pipeline/tools/review_packet.py` — ändra inte för hand.
> Källa för betygskonsekvensen är det faktiska join-maskineriet i `pipeline/positions.py`.

**269 ståndpunkter** → 282 evidence_effect-claims. Stance: {'supports': 239, 'opposes': 30}. Konfidens: {'high': 160, 'medium': 77, 'low': 18, 'None': 14}.

Pipelinen joinar **bara** på `party + policy_type + stance`. `supports` behåller evidensens riktning; `opposes` **vänder** den. Övriga fält är spårbarhet.

## Så granskar du

1. Öppna `source_url`, läs `quote` i sitt sammanhang (`.text`-endpoint för riksdagsdok).
2. Bekräfta att (a) citatet är ordagrant, (b) `stance` stämmer med partiets faktiska linje på det **namngivna instrumentet**, (c) `policy_type` är rätt åtgärdstyp.
3. Sätt verdikt i kolumnen **OK?** (✅/✏️/❌) och notera ev. rättelse.

---

## ⚑ Prioriterad granskning (högst betygspåverkan/risk)

119 rader där fel gör störst skada: **opposes** (vänder evidensen), **prop_avslag** (måste verifiera att propositionen ÄR instrumentet), **ny_karnkraft** (laddad fråga), **low_confidence**, **single_member**, **äldre källa**.

| OK? | Parti | Åtgärdstyp | Stance | B-konsekvens | Konf. | doc_id | Datum | Flaggor |
|-----|-------|-----------|--------|--------------|-------|--------|-------|---------|
|  | KD | aktiveringskrav_ekonomiskt_bistand | **supports** | ↑ mot bättre (höjer B) | high | H9024212 | 2021-10-05 | old_source_2021 |
|  | L | aktiveringskrav_ekonomiskt_bistand | **supports** | ↑ mot bättre (höjer B) | high | H9024181 | 2021-10-01 | old_source_2021 |
|  | M | aktiveringskrav_ekonomiskt_bistand | **supports** | ↑ mot bättre (höjer B) | high | H9024033 | 2021-10-05 | old_source_2021 |
|  | V | aktiveringskrav_ekonomiskt_bistand | **opposes** | ↓ mot sämre (sänker B) | high | HD024027 | 2026-04-01 | opposes, prop_avslag |
|  | C | arbetsmarknadsutbildning | **opposes** | ↓ mot sämre (sänker B) | medium | H9024129 | 2021-10-05 | opposes, old_source_2021 |
|  | KD | arbetsmarknadsutbildning | **opposes** | ↓ mot sämre (sänker B) | medium | H8023409 | 2020-10-06 | opposes, old_source_2020 |
|  | L | arbetsmarknadsutbildning | **opposes** | ↓ mot sämre (sänker B) | medium | H9024181 | 2021-10-04 | opposes, old_source_2021 |
|  | M | arbetsmarknadsutbildning | **supports** | ↑ mot bättre (höjer B) | medium | H6022931 | 2018-11-30 | old_source_2018 |
|  | C | ateraktiverad_utokad_varnplikt | **supports** | ↑ mot bättre (höjer B) | high | HD022822 | 2025-10-06 | single_member |
|  | KD | ateraktiverad_utokad_varnplikt | **supports** | ↑ mot bättre (höjer B) | medium | H9023908 | 2021-10-05 | single_member, old_source_2021 |
|  | L | ateraktiverad_utokad_varnplikt | **supports** | ↑ mot bättre (höjer B) | medium | H3022265 | 2015-10-06 | single_member, old_source_2015 |
|  | M | ateraktiverad_utokad_varnplikt | **supports** | ↑ mot bättre (höjer B) | medium | H9023641 | 2021-10-05 | single_member, old_source_2021 |
|  | S | ateraktiverad_utokad_varnplikt | **supports** | ↑ mot bättre (höjer B) | high | HC023023 | 2024-10-04 | single_member |
|  | SD | ateraktiverad_utokad_varnplikt | **supports** | ↑ mot bättre (höjer B) | high | HA02948 | 2022-11-22 | single_member |
|  | V | ateraktiverad_utokad_varnplikt | **supports** | ↑ mot bättre (höjer B) | high | HD02199 | 2025-09-23 | single_member |
|  | L | atgarder_mot_otillaten_paverkan_offentlig_sektor | **supports** | ↑ mot bättre (höjer B) | low | HD022663 | 2025-10-06 | low_confidence |
|  | KD | begransa_biometrisk_realtidsovervakning_rattssakerhet | **opposes** | ↓ mot sämre (sänker B) | medium | HD01JuU28 / votering E6B9D4D1 punkt 1 + A6B8E0C7 punkt 2 | 2026-05-26 | opposes |
|  | L | begransa_biometrisk_realtidsovervakning_rattssakerhet | **opposes** | ↓ mot sämre (sänker B) | medium | HD01JuU28 / votering E6B9D4D1 punkt 1 + A6B8E0C7 punkt 2 | 2026-05-26 | opposes |
|  | M | begransa_biometrisk_realtidsovervakning_rattssakerhet | **opposes** | ↓ mot sämre (sänker B) | medium | HD01JuU28 / votering E6B9D4D1 punkt 1 + A6B8E0C7 punkt 2 | 2026-05-26 | opposes |
|  | S | begransa_biometrisk_realtidsovervakning_rattssakerhet | **opposes** | ↓ mot sämre (sänker B) | medium | HD01JuU28 / votering E6B9D4D1 punkt 1 + A6B8E0C7 punkt 2 | 2026-05-26 | opposes |
|  | SD | begransa_biometrisk_realtidsovervakning_rattssakerhet | **opposes** | ↓ mot sämre (sänker B) | medium | HD01JuU28 / votering E6B9D4D1 punkt 1 + A6B8E0C7 punkt 2 | 2026-05-26 | opposes |
|  | C | behandlingsprogram_kriminalvard | **supports** | ↑ mot bättre (höjer B) | high | H6023062 | 2019-04-10 | old_source_2019 |
|  | KD | behandlingsprogram_kriminalvard | **supports** | ↑ mot bättre (höjer B) | low | HD021560 | 2025-10-02 | low_confidence |
|  | L | behandlingsprogram_kriminalvard | **supports** | ↑ mot bättre (höjer B) | high | H9023974 | 2021-10-05 | old_source_2021 |
|  | M | behandlingsprogram_kriminalvard | **supports** | ↑ mot bättre (höjer B) | high | H9023779 | 2021-09-30 | old_source_2021 |
|  | V | behandlingsprogram_kriminalvard | **supports** | ↑ mot bättre (höjer B) | high | H902916 | 2021-09-29 | old_source_2021 |
|  | MP | dca_avtal_usa | **opposes** | ↓ mot sämre (sänker B) | medium | HCB46 (Ds 2024:6 bilaga 4, avvikande mening MP) + HB01UFöU1 punkt 1 / korroboration: votering A1C914E0-4544-4389-A757-A5BEDDACBFD9 (p5: MP 15 Nej) + A52E4273-06BE-4869-9C8D-078E3607B40F (p3: MP 15 Avstår) | 2024-06-18 | opposes |
|  | V | dca_avtal_usa | **opposes** | ↓ mot sämre (sänker B) | medium | HCB46 (Ds 2024:6 bilaga 4, avvikande mening V) + HB01UFöU1 punkt 1 / korroboration: votering A1C914E0-4544-4389-A757-A5BEDDACBFD9 (p5: V 20 Nej) + A52E4273-06BE-4869-9C8D-078E3607B40F (p3: V 20 Nej) | 2024-06-18 | opposes |
|  | MP | fokuserad_avskrackning_gvi | **supports** | ↑ mot bättre (höjer B) | low | H8022726 | 2020-10-05 | low_confidence, old_source_2020 |
|  | V | fou_avdrag_skatteincitament | **opposes** | ↓ mot sämre (sänker B) | high | HA01SfU19 / votering 198C0FEC-86BA-4075-8020-9D85FE07E2AF | 2023-05-31 | opposes |
|  | L | inkomststarkande_hushallspolitik | **supports** | ↑ mot bättre (höjer B) | medium | H9024240 | 2021-10-27 | old_source_2021 |
|  | M | inkomststarkande_hushallspolitik | **supports** | ↑ mot bättre (höjer B) | medium | H9024253 | 2021-10-29 | old_source_2021 |
|  | SD | inkomststarkande_hushallspolitik | **supports** | ↑ mot bättre (höjer B) | low | HD02522 | 2025-09-30 | low_confidence |
|  | C | insyn_partifinansiering | **supports** | ↑ mot bättre (höjer B) | medium | H501KU19 punkt 1 | 2018-02-02 | old_source_2018 |
|  | KD | insyn_partifinansiering | **supports** | ↑ mot bättre (höjer B) | medium | H501KU19 punkt 1 | 2018-02-02 | old_source_2018 |
|  | L | insyn_partifinansiering | **supports** | ↑ mot bättre (höjer B) | medium | H501KU19 punkt 1 | 2018-02-02 | old_source_2018 |
|  | M | insyn_partifinansiering | **supports** | ↑ mot bättre (höjer B) | medium | H501KU19 punkt 1 | 2018-02-02 | old_source_2018 |
|  | MP | insyn_partifinansiering | **supports** | ↑ mot bättre (höjer B) | medium | H501KU19 punkt 1 | 2018-02-02 | old_source_2018 |
|  | S | insyn_partifinansiering | **supports** | ↑ mot bättre (höjer B) | medium | H501KU19 punkt 1 | 2018-02-02 | old_source_2018 |
|  | SD | insyn_partifinansiering | **supports** | ↑ mot bättre (höjer B) | medium | H501KU19 punkt 1 | 2018-02-02 | old_source_2018 |
|  | V | insyn_partifinansiering | **supports** | ↑ mot bättre (höjer B) | medium | H501KU19 punkt 1 | 2018-02-02 | old_source_2018 |
|  | KD | koldioxidskatt | **supports** | ↑ mot bättre (höjer B) | — | H8022807 | 2020/21 | old_source_2020 |
|  | L | koldioxidskatt | **supports** | ↑ mot bättre (höjer B) | — | H9024199 | 2021/22 | old_source_2021 |
|  | M | koldioxidskatt | **supports** | ↑ mot bättre (höjer B) | — | H9024030 | 2021/22 | old_source_2021 |
|  | SD | koldioxidskatt | **opposes** | ↓ mot sämre (sänker B) | — | HA02998 | 2022/23 | opposes |
|  | KD | kompetensutveckling_larare | **supports** | ↑ mot bättre (höjer B) | high | H9024163 | 2021-10-05 | old_source_2021 |
|  | L | kompetensutveckling_larare | **supports** | ↑ mot bättre (höjer B) | high | H9024181 | 2021-10-05 | old_source_2021 |
|  | M | kompetensutveckling_larare | **supports** | ↑ mot bättre (höjer B) | high | H9023988 | 2021-10-05 | old_source_2021 |
|  | SD | kompetensutveckling_larare | **supports** | ↑ mot bättre (höjer B) | high | H9022542 | 2021-10-01 | old_source_2021 |
|  | C | koncentration_nationell_hogspecialiserad_vard | **supports** | ↑ mot bättre (höjer B) | medium | H501SoU18 punkt 1 | 2018-02-20 | old_source_2018 |
|  | KD | koncentration_nationell_hogspecialiserad_vard | **supports** | ↑ mot bättre (höjer B) | medium | H501SoU18 punkt 1 | 2018-02-20 | old_source_2018 |
|  | L | koncentration_nationell_hogspecialiserad_vard | **supports** | ↑ mot bättre (höjer B) | medium | H501SoU18 punkt 1 | 2018-02-20 | old_source_2018 |
|  | M | koncentration_nationell_hogspecialiserad_vard | **supports** | ↑ mot bättre (höjer B) | medium | H501SoU18 punkt 1 | 2018-02-20 | old_source_2018 |
|  | MP | koncentration_nationell_hogspecialiserad_vard | **supports** | ↑ mot bättre (höjer B) | medium | H501SoU18 punkt 1 | 2018-02-20 | old_source_2018 |
|  | S | koncentration_nationell_hogspecialiserad_vard | **supports** | ↑ mot bättre (höjer B) | medium | H501SoU18 punkt 1 | 2018-02-20 | old_source_2018 |
|  | SD | koncentration_nationell_hogspecialiserad_vard | **supports** | ↑ mot bättre (höjer B) | medium | H501SoU18 punkt 1 | 2018-02-20 | old_source_2018 |
|  | V | koncentration_nationell_hogspecialiserad_vard | **supports** | ↑ mot bättre (höjer B) | medium | H501SoU18 punkt 1 | 2018-02-20 | old_source_2018 |
|  | L | konkurrenskraftig_foretags_och_agarbeskattning | **supports** | ↑ mot bättre (höjer B) | medium | H6022030 | 2018-11-29 | old_source_2018 |
|  | M | konkurrenskraftig_foretags_och_agarbeskattning | **supports** | ↑ mot bättre (höjer B) | high | H9023638 | 2021-10-05 | old_source_2021 |
|  | MP | konkurrenskraftig_foretags_och_agarbeskattning | **opposes** | ↓ mot sämre (sänker B) | medium | HC023220 | 2024-10-04 | opposes |
|  | S | konkurrenskraftig_foretags_och_agarbeskattning | **opposes** | ↓ mot sämre (sänker B) | high | HD023553 | 2025-10-07 | opposes |
|  | V | konkurrenskraftig_foretags_och_agarbeskattning | **opposes** | ↓ mot sämre (sänker B) | high | H5024186 | 2018-05-17 | opposes, old_source_2018 |
|  | KD | kontroller_och_informationsutbyte_mot_valfardsbrott | **supports** | ↑ mot bättre (höjer B) | high | H9024184 | 2021-10-05 | old_source_2021 |
|  | L | kontroller_och_informationsutbyte_mot_valfardsbrott | **supports** | ↑ mot bättre (höjer B) | high | H9023974 | 2021-10-05 | old_source_2021 |
|  | M | kontroller_och_informationsutbyte_mot_valfardsbrott | **supports** | ↑ mot bättre (höjer B) | low | HC023146 | 2024-10-04 | low_confidence, single_member |
|  | KD | minskad_klasstorlek | **supports** | ↑ mot bättre (höjer B) | medium | H2023002 | 2014-11-11 | old_source_2014 |
|  | L | minskad_klasstorlek | **supports** | ↑ mot bättre (höjer B) | medium | H2023002 | 2014-11-11 | old_source_2014 |
|  | M | minskad_klasstorlek | **supports** | ↑ mot bättre (höjer B) | medium | H2023002 | 2014-11-11 | old_source_2014 |
|  | SD | minskad_klasstorlek | **opposes** | ↓ mot sämre (sänker B) | high | H302761 | 2015-10-02 | opposes, old_source_2015 |
|  | V | nato_medlemskap | **opposes** | ↓ mot sämre (sänker B) | high | HA01UU16 / votering 6B63ADBF-B6F8-4CE0-A574-230BEE238A46 punkt 1 | 2023-03-22 | opposes |
|  | V | nedtrappad_ersattningsprofil_akassa | **opposes** | ↓ mot sämre (sänker B) | high | HB01AU9 / votering 20D6BDDC-B9AC-47E8-B286-48CF613D7276; motion HB022881 yrk. 1 | 2024-06-18 | opposes, prop_avslag |
|  | KD | ny_karnkraft | **supports** | ↑ mot bättre (höjer B) | medium | H9024195 | 2021-10-05 | ny_karnkraft, old_source_2021 |
|  | L | ny_karnkraft | **supports** | ↑ mot bättre (höjer B) | medium | H8023242 | 2020-10-06 | ny_karnkraft, old_source_2020 |
|  | M | ny_karnkraft | **supports** | ↑ mot bättre (höjer B) | medium | H9023688 | 2021-10-05 | ny_karnkraft, old_source_2021 |
|  | MP | ny_karnkraft | **opposes** | ↓ mot sämre (sänker B) | high | HD023984 | 2026-03-25 | opposes, prop_avslag, ny_karnkraft |
|  | S | ny_karnkraft | **supports** | ↑ mot bättre (höjer B) | medium | HD023594 | 2025-10-07 | ny_karnkraft |
|  | SD | ny_karnkraft | **supports** | ↑ mot bättre (höjer B) | high | HC021464 | 2024-10-02 | ny_karnkraft |
|  | V | ny_karnkraft | **opposes** | ↓ mot sämre (sänker B) | high | HD023961 | 2026-03-19 | opposes, prop_avslag, ny_karnkraft |
|  | KD | reduktionsplikt_drivmedel | **opposes** | ↓ mot sämre (sänker B) | — | HB01MJU5 / votering 21E8B615-C235-489F-8189-D26CABD56F24 punkt 1 | 2023/24 | opposes |
|  | L | reduktionsplikt_drivmedel | **opposes** | ↓ mot sämre (sänker B) | — | HB01MJU5 / votering 21E8B615-C235-489F-8189-D26CABD56F24 punkt 1 | 2023/24 | opposes |
|  | M | reduktionsplikt_drivmedel | **opposes** | ↓ mot sämre (sänker B) | — | HB01MJU5 / votering 21E8B615-C235-489F-8189-D26CABD56F24 punkt 1 | 2023/24 | opposes |
|  | SD | reduktionsplikt_drivmedel | **opposes** | ↓ mot sämre (sänker B) | — | HB01MJU5 / votering 21E8B615-C235-489F-8189-D26CABD56F24 punkt 1 | 2023/24 | opposes |
|  | KD | riktade_insatser_nyanlanda_elever | **supports** | ↑ mot bättre (höjer B) | medium | H9024163 | 2021-10-05 | old_source_2021 |
|  | L | riktade_insatser_nyanlanda_elever | **supports** | ↑ mot bättre (höjer B) | high | H9024002 | 2021-10-05 | old_source_2021 |
|  | M | riktade_insatser_nyanlanda_elever | **supports** | ↑ mot bättre (höjer B) | high | H9024033 | 2021-10-05 | old_source_2021 |
|  | C | se_over_ansvarsfordelning_atervandande | **supports** | ↑ mot bättre (höjer B) | high | H801SfU6 punkt 2; votering C7DEF4C6-4668-4D8E-AF06-7A820A666C39 (C 5 ja); motion H802311 (Jonny Cato, C) | 2020-11-11 | old_source_2020 |
|  | KD | se_over_ansvarsfordelning_atervandande | **supports** | ↑ mot bättre (höjer B) | high | H801SfU6 punkt 2; votering C7DEF4C6-4668-4D8E-AF06-7A820A666C39 (KD 3 ja); motion H802145 yrk. 3 + motion 2020/21:3663 yrk. 30 | 2020-11-11 | old_source_2020 |
|  | L | se_over_ansvarsfordelning_atervandande | **supports** | ↑ mot bättre (höjer B) | medium | H801SfU6 punkt 2; votering C7DEF4C6-4668-4D8E-AF06-7A820A666C39 (L 3 ja) | 2020-11-11 | old_source_2020 |
|  | M | se_over_ansvarsfordelning_atervandande | **supports** | ↑ mot bättre (höjer B) | high | H801SfU6 punkt 2; votering C7DEF4C6-4668-4D8E-AF06-7A820A666C39 (M 11 ja); motion H802145 yrk. 3 | 2020-11-11 | old_source_2020 |
|  | MP | se_over_ansvarsfordelning_atervandande | **opposes** | ↓ mot sämre (sänker B) | high | H801SfU6 reservation 3 (S,MP); votering C7DEF4C6-4668-4D8E-AF06-7A820A666C39 (MP 3 nej) | 2020-11-11 | opposes, old_source_2020 |
|  | S | se_over_ansvarsfordelning_atervandande | **opposes** | ↓ mot sämre (sänker B) | high | H801SfU6 reservation 3 (S,MP); votering C7DEF4C6-4668-4D8E-AF06-7A820A666C39 (S 15 nej) | 2020-11-11 | opposes, old_source_2020 |
|  | SD | se_over_ansvarsfordelning_atervandande | **supports** | ↑ mot bättre (höjer B) | high | H801SfU6 punkt 2; votering C7DEF4C6-4668-4D8E-AF06-7A820A666C39 (SD 10 ja); motion 2020/21:2552 yrk. 22 | 2020-11-11 | old_source_2020 |
|  | C | sfi_kombinerat_med_praktik | **supports** | ↑ mot bättre (höjer B) | low | HB021255 | 2023-10-04 | low_confidence, single_member |
|  | KD | sfi_kombinerat_med_praktik | **supports** | ↑ mot bättre (höjer B) | low | H9024198 | 2021-10-04 | low_confidence, old_source_2021 |
|  | L | sfi_kombinerat_med_praktik | **supports** | ↑ mot bättre (höjer B) | low | H9023965 | 2021-10-05 | low_confidence, old_source_2021 |
|  | M | sfi_kombinerat_med_praktik | **supports** | ↑ mot bättre (höjer B) | low | H4023372 | 2016-10-05 | low_confidence, old_source_2016 |
|  | KD | situationell_prevention_utomhusbelysning | **supports** | ↑ mot bättre (höjer B) | medium | H3022686 | 2015-10-06 | old_source_2015 |
|  | L | situationell_prevention_utomhusbelysning | **supports** | ↑ mot bättre (höjer B) | medium | H9023974 | 2021-10-05 | old_source_2021 |
|  | SD | situationell_prevention_utomhusbelysning | **supports** | ↑ mot bättre (höjer B) | low | HD02256 | 2025-09-24 | low_confidence |
|  | KD | sprakpraktik_kombinerad_sprakutbildning_och_arbetspraktik | **supports** | ↑ mot bättre (höjer B) | low | HD021563 | 2025-10-02 | low_confidence |
|  | MP | sprakpraktik_kombinerad_sprakutbildning_och_arbetspraktik | **supports** | ↑ mot bättre (höjer B) | medium | GQ02Sf289 | 2002-10-23 | old_source_2002 |
|  | KD | starkt_oberoende_granskning_och_insyn | **supports** | ↑ mot bättre (höjer B) | low | HD021556 | 2025-10-02 | low_confidence |
|  | L | starkt_oberoende_granskning_och_insyn | **supports** | ↑ mot bättre (höjer B) | low | HD023766 | 2025-10-07 | low_confidence, single_member |
|  | M | starkt_oberoende_granskning_och_insyn | **supports** | ↑ mot bättre (höjer B) | low | HD021743 | 2025-10-02 | low_confidence, single_member |
|  | SD | starkt_oberoende_granskning_och_insyn | **supports** | ↑ mot bättre (höjer B) | low | HD021701 | 2025-10-02 | low_confidence |
|  | C | subventionerade_anstallningar | **opposes** | ↓ mot sämre (sänker B) | high | HD023191 | 2025-10-06 | opposes |
|  | KD | subventionerade_anstallningar | **supports** | ↑ mot bättre (höjer B) | high | H9024198 | 2021-10-05 | old_source_2021 |
|  | L | subventionerade_anstallningar | **supports** | ↑ mot bättre (höjer B) | high | H9023952 | 2021-10-05 | old_source_2021 |
|  | M | subventionerade_anstallningar | **supports** | ↑ mot bättre (höjer B) | high | H9024036 | 2021-10-05 | old_source_2021 |
|  | SD | subventionerade_anstallningar | **opposes** | ↓ mot sämre (sänker B) | high | HC022386 | 2024-10-03 | opposes |
|  | L | systematiskt_antikorruptionsarbete_kommuner_regioner | **supports** | ↑ mot bättre (höjer B) | low | HD022663 | 2025-10-06 | low_confidence |
|  | S | systematiskt_antikorruptionsarbete_kommuner_regioner | **supports** | ↑ mot bättre (höjer B) | low | HC02445 | 2024-09-25 | low_confidence |
|  | SD | systematiskt_antikorruptionsarbete_kommuner_regioner | **supports** | ↑ mot bättre (höjer B) | low | HD02247 | 2025-09-24 | low_confidence |
|  | C | tidiga_insatser_lagstadiet | **supports** | ↑ mot bättre (höjer B) | medium | H5024117 | 2018-04-11 | old_source_2018 |
|  | KD | tidiga_insatser_lagstadiet | **supports** | ↑ mot bättre (höjer B) | medium | H5024117 | 2018-04-11 | old_source_2018 |
|  | M | tidiga_insatser_lagstadiet | **supports** | ↑ mot bättre (höjer B) | medium | H5024117 | 2018-04-11 | old_source_2018 |
|  | SD | tidiga_insatser_lagstadiet | **opposes** | ↓ mot sämre (sänker B) | high | H501UbU10 | 2018-05-30 | opposes, prop_avslag, old_source_2018 |
|  | L | tydlig_statlig_styrning_civilt_forsvar | **supports** | ↑ mot bättre (höjer B) | high | H8023429 | 2020-10-06 | old_source_2020 |
|  | M | tydlig_statlig_styrning_civilt_forsvar | **supports** | ↑ mot bättre (höjer B) | high | H9023642 | 2021-10-05 | old_source_2021 |

---

## Alla ståndpunkter per kategori (panelvy)

Granska varje åtgärdstyp som en panel — alla partier sida vid sida, så asymmetrier syns.

### demokrati

#### `atgarder_mot_otillaten_paverkan_offentlig_sektor`

Liggarens effekt: korruption=positive (low)

| OK? | Parti | Stance | B-konsekvens | Konf. | doc_id | Datum |
|-----|-------|--------|--------------|-------|--------|-------|
|  | C | supports | ↑ mot bättre (höjer B) | high | HD023581 | 2025-10-07 |
|  | L ⚑ | supports | ↑ mot bättre (höjer B) | low | HD022663 | 2025-10-06 |
|  | MP | supports | ↑ mot bättre (höjer B) | high | HB022669 | 2023-10-05 |
|  | S | supports | ↑ mot bättre (höjer B) | high | HD023586 | 2025-10-07 |

#### `begransa_biometrisk_realtidsovervakning_rattssakerhet`

Liggarens effekt: overvakning_utan_rattssakerhet=positive (medium)

| OK? | Parti | Stance | B-konsekvens | Konf. | doc_id | Datum |
|-----|-------|--------|--------------|-------|--------|-------|
|  | C | supports | ↑ mot bättre (höjer B) | medium | HD01JuU28 / votering E6B9D4D1-D69A-492F-ADBB-82345B549240 punkt 1 | 2026-05-26 |
|  | KD ⚑ | opposes | ↓ mot sämre (sänker B) | medium | HD01JuU28 / votering E6B9D4D1 punkt 1 + A6B8E0C7 punkt 2 | 2026-05-26 |
|  | L ⚑ | opposes | ↓ mot sämre (sänker B) | medium | HD01JuU28 / votering E6B9D4D1 punkt 1 + A6B8E0C7 punkt 2 | 2026-05-26 |
|  | M ⚑ | opposes | ↓ mot sämre (sänker B) | medium | HD01JuU28 / votering E6B9D4D1 punkt 1 + A6B8E0C7 punkt 2 | 2026-05-26 |
|  | MP | supports | ↑ mot bättre (höjer B) | medium | HD01JuU28 / votering A6B8E0C7 punkt 2 + BC189AC8 punkt 3 | 2026-05-26 |
|  | S ⚑ | opposes | ↓ mot sämre (sänker B) | medium | HD01JuU28 / votering E6B9D4D1 punkt 1 + A6B8E0C7 punkt 2 | 2026-05-26 |
|  | SD ⚑ | opposes | ↓ mot sämre (sänker B) | medium | HD01JuU28 / votering E6B9D4D1 punkt 1 + A6B8E0C7 punkt 2 | 2026-05-26 |
|  | V | supports | ↑ mot bättre (höjer B) | medium | HD01JuU28 / votering A6B8E0C7-CFEE-4359-ABB7-6554F05B22E0 punkt 2 | 2026-05-26 |

#### `grundlagsskydd_domstolarnas_oberoende`

Liggarens effekt: otillborlig_politisering=positive (medium)

| OK? | Parti | Stance | B-konsekvens | Konf. | doc_id | Datum |
|-----|-------|--------|--------------|-------|--------|-------|
|  | C | supports | ↑ mot bättre (höjer B) | high | HD01KU2 / votering 3C8070DF-2ECB-405A-83AD-A14CF2A79C61 punkt 1 | 2025-09-29 |
|  | KD | supports | ↑ mot bättre (höjer B) | high | HD01KU2 / votering 3C8070DF-2ECB-405A-83AD-A14CF2A79C61 punkt 1 | 2025-09-29 |
|  | L | supports | ↑ mot bättre (höjer B) | high | HD01KU2 / votering 3C8070DF-2ECB-405A-83AD-A14CF2A79C61 punkt 1 | 2025-09-29 |
|  | M | supports | ↑ mot bättre (höjer B) | high | HD01KU2 / votering 3C8070DF-2ECB-405A-83AD-A14CF2A79C61 punkt 1 | 2025-09-29 |
|  | MP | supports | ↑ mot bättre (höjer B) | high | HD01KU2 / votering 3C8070DF-2ECB-405A-83AD-A14CF2A79C61 punkt 1 | 2025-09-29 |
|  | S | supports | ↑ mot bättre (höjer B) | high | HD01KU2 / votering 3C8070DF-2ECB-405A-83AD-A14CF2A79C61 punkt 1 | 2025-09-29 |
|  | V | supports | ↑ mot bättre (höjer B) | high | HD01KU2 / votering 3C8070DF-2ECB-405A-83AD-A14CF2A79C61 punkt 1 | 2025-09-29 |

#### `insyn_partifinansiering`

Liggarens effekt: politisk_transparens=positive (low)

| OK? | Parti | Stance | B-konsekvens | Konf. | doc_id | Datum |
|-----|-------|--------|--------------|-------|--------|-------|
|  | C | supports | ↑ mot bättre (höjer B) | medium | H501KU19 punkt 1 | 2018-02-02 |
|  | KD | supports | ↑ mot bättre (höjer B) | medium | H501KU19 punkt 1 | 2018-02-02 |
|  | L | supports | ↑ mot bättre (höjer B) | medium | H501KU19 punkt 1 | 2018-02-02 |
|  | M | supports | ↑ mot bättre (höjer B) | medium | H501KU19 punkt 1 | 2018-02-02 |
|  | MP | supports | ↑ mot bättre (höjer B) | medium | H501KU19 punkt 1 | 2018-02-02 |
|  | S | supports | ↑ mot bättre (höjer B) | medium | H501KU19 punkt 1 | 2018-02-02 |
|  | SD | supports | ↑ mot bättre (höjer B) | medium | H501KU19 punkt 1 | 2018-02-02 |
|  | V | supports | ↑ mot bättre (höjer B) | medium | H501KU19 punkt 1 | 2018-02-02 |

#### `lagstadgat_oberoende_public_service`

Liggarens effekt: mediefrihet=positive (low)

| OK? | Parti | Stance | B-konsekvens | Konf. | doc_id | Datum |
|-----|-------|--------|--------------|-------|--------|-------|
|  | C | supports | ↑ mot bättre (höjer B) | high | HD01KrU2 punkt 1 | 2025-10-22 |
|  | KD | supports | ↑ mot bättre (höjer B) | high | HD01KrU2 punkt 1 | 2025-10-22 |
|  | L | supports | ↑ mot bättre (höjer B) | high | HD01KrU2 punkt 1 | 2025-10-22 |
|  | M | supports | ↑ mot bättre (höjer B) | high | HD01KrU2 punkt 1 | 2025-10-22 |
|  | MP | supports | ↑ mot bättre (höjer B) | high | HD01KrU2 punkt 1 | 2025-10-22 |
|  | S | supports | ↑ mot bättre (höjer B) | high | HD01KrU2 punkt 1 | 2025-10-22 |
|  | SD | supports | ↑ mot bättre (höjer B) | high | HD01KrU2 punkt 1 | 2025-10-22 |
|  | V | supports | ↑ mot bättre (höjer B) | high | HD01KrU2 punkt 1 | 2025-10-22 |

#### `starkt_oberoende_granskning_och_insyn`

Liggarens effekt: korruption=positive (low)

| OK? | Parti | Stance | B-konsekvens | Konf. | doc_id | Datum |
|-----|-------|--------|--------------|-------|--------|-------|
|  | C | supports | ↑ mot bättre (höjer B) | high | HD023583 yrk. 17 | 2025-10-07 |
|  | KD ⚑ | supports | ↑ mot bättre (höjer B) | low | HD021556 | 2025-10-02 |
|  | L ⚑ | supports | ↑ mot bättre (höjer B) | low | HD023766 | 2025-10-07 |
|  | M ⚑ | supports | ↑ mot bättre (höjer B) | low | HD021743 | 2025-10-02 |
|  | MP | supports | ↑ mot bättre (höjer B) | high | HA02181 yrk. 9 | 2022-11-16 |
|  | S | supports | ↑ mot bättre (höjer B) | high | HD024024 | 2026-04-01 |
|  | SD ⚑ | supports | ↑ mot bättre (höjer B) | low | HD021701 | 2025-10-02 |
|  | V | supports | ↑ mot bättre (höjer B) | high | HD023996 | 2026-03-31 |

#### `systematiskt_antikorruptionsarbete_kommuner_regioner`

Liggarens effekt: korruption=positive (low)

| OK? | Parti | Stance | B-konsekvens | Konf. | doc_id | Datum |
|-----|-------|--------|--------------|-------|--------|-------|
|  | C | supports | ↑ mot bättre (höjer B) | medium | HD023581 | 2025-10-07 |
|  | L ⚑ | supports | ↑ mot bättre (höjer B) | low | HD022663 | 2025-10-06 |
|  | S ⚑ | supports | ↑ mot bättre (höjer B) | low | HC02445 | 2024-09-25 |
|  | SD ⚑ | supports | ↑ mot bättre (höjer B) | low | HD02247 | 2025-09-24 |

### ekonomi

#### `arbetsmarknadsutbildning`

Liggarens effekt: sysselsattning=positive (high)

| OK? | Parti | Stance | B-konsekvens | Konf. | doc_id | Datum |
|-----|-------|--------|--------------|-------|--------|-------|
|  | C ⚑ | opposes | ↓ mot sämre (sänker B) | medium | H9024129 | 2021-10-05 |
|  | KD ⚑ | opposes | ↓ mot sämre (sänker B) | medium | H8023409 | 2020-10-06 |
|  | L ⚑ | opposes | ↓ mot sämre (sänker B) | medium | H9024181 | 2021-10-04 |
|  | M | supports | ↑ mot bättre (höjer B) | medium | H6022931 | 2018-11-30 |
|  | MP | supports | ↑ mot bättre (höjer B) | high | HD023525 | 2025-10-07 |
|  | S | supports | ↑ mot bättre (höjer B) | high | HD023590 | 2025-10-07 |
|  | SD | supports | ↑ mot bättre (höjer B) | high | HC022386 | 2024-10-03 |
|  | V | supports | ↑ mot bättre (höjer B) | high | HD023167 | 2025-10-06 |

#### `fou_avdrag_skatteincitament`

Liggarens effekt: produktivitet=positive (medium)

| OK? | Parti | Stance | B-konsekvens | Konf. | doc_id | Datum |
|-----|-------|--------|--------------|-------|--------|-------|
|  | C | supports | ↑ mot bättre (höjer B) | high | HA01SfU19 / votering 198C0FEC-86BA-4075-8020-9D85FE07E2AF | 2023-05-31 |
|  | KD | supports | ↑ mot bättre (höjer B) | high | HA01SfU19 / votering 198C0FEC-86BA-4075-8020-9D85FE07E2AF | 2023-05-31 |
|  | L | supports | ↑ mot bättre (höjer B) | high | HA01SfU19 / votering 198C0FEC-86BA-4075-8020-9D85FE07E2AF | 2023-05-31 |
|  | M | supports | ↑ mot bättre (höjer B) | high | HA01SfU19 / votering 198C0FEC-86BA-4075-8020-9D85FE07E2AF | 2023-05-31 |
|  | MP | supports | ↑ mot bättre (höjer B) | high | HA01SfU19 / votering 198C0FEC-86BA-4075-8020-9D85FE07E2AF | 2023-05-31 |
|  | S | supports | ↑ mot bättre (höjer B) | high | HA01SfU19 / votering 198C0FEC-86BA-4075-8020-9D85FE07E2AF | 2023-05-31 |
|  | SD | supports | ↑ mot bättre (höjer B) | high | HA01SfU19 / votering 198C0FEC-86BA-4075-8020-9D85FE07E2AF | 2023-05-31 |
|  | V ⚑ | opposes | ↓ mot sämre (sänker B) | high | HA01SfU19 / votering 198C0FEC-86BA-4075-8020-9D85FE07E2AF | 2023-05-31 |

#### `inkomststarkande_hushallspolitik`

Liggarens effekt: hushallens_reala_disponibla_inkomst=positive (high)

| OK? | Parti | Stance | B-konsekvens | Konf. | doc_id | Datum |
|-----|-------|--------|--------------|-------|--------|-------|
|  | C | supports | ↑ mot bättre (höjer B) | high | HD023811 | 2025-10-07 |
|  | KD | supports | ↑ mot bättre (höjer B) | medium | HD023474 | 2025-10-07 |
|  | L | supports | ↑ mot bättre (höjer B) | medium | H9024240 | 2021-10-27 |
|  | M | supports | ↑ mot bättre (höjer B) | medium | H9024253 | 2021-10-29 |
|  | MP | supports | ↑ mot bättre (höjer B) | high | HD023538 | 2025-10-07 |
|  | S | supports | ↑ mot bättre (höjer B) | high | HD023589 | 2025-10-07 |
|  | SD ⚑ | supports | ↑ mot bättre (höjer B) | low | HD02522 | 2025-09-30 |
|  | V | supports | ↑ mot bättre (höjer B) | high | HD022781 | 2025-10-06 |

#### `konkurrenskraftig_foretags_och_agarbeskattning`

Liggarens effekt: naringslivets_investeringar=positive (medium)

| OK? | Parti | Stance | B-konsekvens | Konf. | doc_id | Datum |
|-----|-------|--------|--------------|-------|--------|-------|
|  | C | supports | ↑ mot bättre (höjer B) | high | HD022835 | 2025-10-06 |
|  | KD | supports | ↑ mot bättre (höjer B) | medium | HD023474 | 2025-10-07 |
|  | L | supports | ↑ mot bättre (höjer B) | medium | H6022030 | 2018-11-29 |
|  | M | supports | ↑ mot bättre (höjer B) | high | H9023638 | 2021-10-05 |
|  | MP ⚑ | opposes | ↓ mot sämre (sänker B) | medium | HC023220 | 2024-10-04 |
|  | S ⚑ | opposes | ↓ mot sämre (sänker B) | high | HD023553 | 2025-10-07 |
|  | SD | supports | ↑ mot bättre (höjer B) | medium | HC021353 | 2024-10-02 |
|  | V ⚑ | opposes | ↓ mot sämre (sänker B) | high | H5024186 | 2018-05-17 |

#### `nedtrappad_ersattningsprofil_akassa`

Liggarens effekt: arbetsloshet=positive (medium)

| OK? | Parti | Stance | B-konsekvens | Konf. | doc_id | Datum |
|-----|-------|--------|--------------|-------|--------|-------|
|  | C | supports | ↑ mot bättre (höjer B) | high | HB01AU9 / votering 20D6BDDC-B9AC-47E8-B286-48CF613D7276 | 2024-06-18 |
|  | KD | supports | ↑ mot bättre (höjer B) | high | HB01AU9 / votering 20D6BDDC-B9AC-47E8-B286-48CF613D7276 | 2024-06-18 |
|  | L | supports | ↑ mot bättre (höjer B) | high | HB01AU9 / votering 20D6BDDC-B9AC-47E8-B286-48CF613D7276 | 2024-06-18 |
|  | M | supports | ↑ mot bättre (höjer B) | high | HB01AU9 / votering 20D6BDDC-B9AC-47E8-B286-48CF613D7276 | 2024-06-18 |
|  | MP | supports | ↑ mot bättre (höjer B) | high | HB01AU9 / votering 20D6BDDC-B9AC-47E8-B286-48CF613D7276 | 2024-06-18 |
|  | S | supports | ↑ mot bättre (höjer B) | high | HB01AU9 / votering 20D6BDDC-B9AC-47E8-B286-48CF613D7276 | 2024-06-18 |
|  | SD | supports | ↑ mot bättre (höjer B) | high | HB01AU9 / votering 20D6BDDC-B9AC-47E8-B286-48CF613D7276 | 2024-06-18 |
|  | V ⚑ | opposes | ↓ mot sämre (sänker B) | high | HB01AU9 / votering 20D6BDDC-B9AC-47E8-B286-48CF613D7276; motion HB022881 yrk. 1 | 2024-06-18 |

#### `subventionerade_anstallningar`

Liggarens effekt: sysselsattning=positive (medium)

| OK? | Parti | Stance | B-konsekvens | Konf. | doc_id | Datum |
|-----|-------|--------|--------------|-------|--------|-------|
|  | C ⚑ | opposes | ↓ mot sämre (sänker B) | high | HD023191 | 2025-10-06 |
|  | KD | supports | ↑ mot bättre (höjer B) | high | H9024198 | 2021-10-05 |
|  | L | supports | ↑ mot bättre (höjer B) | high | H9023952 | 2021-10-05 |
|  | M | supports | ↑ mot bättre (höjer B) | high | H9024036 | 2021-10-05 |
|  | MP | supports | ↑ mot bättre (höjer B) | high | HB022698 | 2023-10-05 |
|  | S | supports | ↑ mot bättre (höjer B) | high | HD023590 | 2025-2026 |
|  | SD ⚑ | opposes | ↓ mot sämre (sänker B) | high | HC022386 | 2024-10-03 |
|  | V | supports | ↑ mot bättre (höjer B) | high | HB02441 | 2023-09-29 |

### forsvar

#### `ateraktiverad_utokad_varnplikt`

Liggarens effekt: personal_varnpliktiga=positive (high)

| OK? | Parti | Stance | B-konsekvens | Konf. | doc_id | Datum |
|-----|-------|--------|--------------|-------|--------|-------|
|  | C ⚑ | supports | ↑ mot bättre (höjer B) | high | HD022822 | 2025-10-06 |
|  | KD ⚑ | supports | ↑ mot bättre (höjer B) | medium | H9023908 | 2021-10-05 |
|  | L ⚑ | supports | ↑ mot bättre (höjer B) | medium | H3022265 | 2015-10-06 |
|  | M ⚑ | supports | ↑ mot bättre (höjer B) | medium | H9023641 | 2021-10-05 |
|  | S ⚑ | supports | ↑ mot bättre (höjer B) | high | HC023023 | 2024-10-04 |
|  | SD ⚑ | supports | ↑ mot bättre (höjer B) | high | HA02948 | 2022-11-22 |
|  | V ⚑ | supports | ↑ mot bättre (höjer B) | high | HD02199 | 2025-09-23 |

#### `dca_avtal_usa`

Liggarens effekt: nato_interoperabilitet=positive (high)

| OK? | Parti | Stance | B-konsekvens | Konf. | doc_id | Datum |
|-----|-------|--------|--------------|-------|--------|-------|
|  | C | supports | ↑ mot bättre (höjer B) | medium | HB01UFöU1 punkt 1 (huvudvotering saknas i votering-API) / korroboration: votering A1C914E0-4544-4389-A757-A5BEDDACBFD9 (p5) + A52E4273-06BE-4869-9C8D-078E3607B40F (p3) | 2024-06-18 |
|  | KD | supports | ↑ mot bättre (höjer B) | medium | HB01UFöU1 punkt 1 (huvudvotering saknas i votering-API) / korroboration: votering A1C914E0-4544-4389-A757-A5BEDDACBFD9 (p5) + A52E4273-06BE-4869-9C8D-078E3607B40F (p3) | 2024-06-18 |
|  | L | supports | ↑ mot bättre (höjer B) | medium | HB01UFöU1 punkt 1 (huvudvotering saknas i votering-API) / korroboration: votering A1C914E0-4544-4389-A757-A5BEDDACBFD9 (p5) + A52E4273-06BE-4869-9C8D-078E3607B40F (p3) | 2024-06-18 |
|  | M | supports | ↑ mot bättre (höjer B) | medium | HB01UFöU1 punkt 1 (huvudvotering saknas i votering-API) / korroboration: votering A1C914E0-4544-4389-A757-A5BEDDACBFD9 (p5) + A52E4273-06BE-4869-9C8D-078E3607B40F (p3) | 2024-06-18 |
|  | MP ⚑ | opposes | ↓ mot sämre (sänker B) | medium | HCB46 (Ds 2024:6 bilaga 4, avvikande mening MP) + HB01UFöU1 punkt 1 / korroboration: votering A1C914E0-4544-4389-A757-A5BEDDACBFD9 (p5: MP 15 Nej) + A52E4273-06BE-4869-9C8D-078E3607B40F (p3: MP 15 Avstår) | 2024-06-18 |
|  | S | supports | ↑ mot bättre (höjer B) | medium | HB01UFöU1 punkt 1 (huvudvotering saknas i votering-API) / korroboration: votering A1C914E0-4544-4389-A757-A5BEDDACBFD9 (p5) + A52E4273-06BE-4869-9C8D-078E3607B40F (p3) | 2024-06-18 |
|  | SD | supports | ↑ mot bättre (höjer B) | medium | HB01UFöU1 punkt 1 (huvudvotering saknas i votering-API) / korroboration: votering A1C914E0-4544-4389-A757-A5BEDDACBFD9 (p5) + A52E4273-06BE-4869-9C8D-078E3607B40F (p3) | 2024-06-18 |
|  | V ⚑ | opposes | ↓ mot sämre (sänker B) | medium | HCB46 (Ds 2024:6 bilaga 4, avvikande mening V) + HB01UFöU1 punkt 1 / korroboration: votering A1C914E0-4544-4389-A757-A5BEDDACBFD9 (p5: V 20 Nej) + A52E4273-06BE-4869-9C8D-078E3607B40F (p3: V 20 Nej) | 2024-06-18 |

#### `nato_medlemskap`

Liggarens effekt: nato_interoperabilitet=positive (high)

| OK? | Parti | Stance | B-konsekvens | Konf. | doc_id | Datum |
|-----|-------|--------|--------------|-------|--------|-------|
|  | C | supports | ↑ mot bättre (höjer B) | high | HA01UU16 / votering 6B63ADBF-B6F8-4CE0-A574-230BEE238A46 punkt 1 | 2023-03-22 |
|  | KD | supports | ↑ mot bättre (höjer B) | high | HA01UU16 / votering 6B63ADBF-B6F8-4CE0-A574-230BEE238A46 punkt 1 | 2023-03-22 |
|  | L | supports | ↑ mot bättre (höjer B) | high | HA01UU16 / votering 6B63ADBF-B6F8-4CE0-A574-230BEE238A46 punkt 1 | 2023-03-22 |
|  | M | supports | ↑ mot bättre (höjer B) | high | HA01UU16 / votering 6B63ADBF-B6F8-4CE0-A574-230BEE238A46 punkt 1 | 2023-03-22 |
|  | S | supports | ↑ mot bättre (höjer B) | high | HA01UU16 / votering 6B63ADBF-B6F8-4CE0-A574-230BEE238A46 punkt 1 | 2023-03-22 |
|  | SD | supports | ↑ mot bättre (höjer B) | high | HA01UU16 / votering 6B63ADBF-B6F8-4CE0-A574-230BEE238A46 punkt 1 | 2023-03-22 |
|  | V ⚑ | opposes | ↓ mot sämre (sänker B) | high | HA01UU16 / votering 6B63ADBF-B6F8-4CE0-A574-230BEE238A46 punkt 1 | 2023-03-22 |

#### `tydlig_statlig_styrning_civilt_forsvar`

Liggarens effekt: civil_beredskap_niva=positive (low)

| OK? | Parti | Stance | B-konsekvens | Konf. | doc_id | Datum |
|-----|-------|--------|--------------|-------|--------|-------|
|  | L | supports | ↑ mot bättre (höjer B) | high | H8023429 | 2020-10-06 |
|  | M | supports | ↑ mot bättre (höjer B) | high | H9023642 | 2021-10-05 |
|  | S | supports | ↑ mot bättre (höjer B) | high | HD023556 | 2025-10-07 |
|  | SD | supports | ↑ mot bättre (höjer B) | high | HC021407 | 2024-10-02 |
|  | V | supports | ↑ mot bättre (höjer B) | medium | HB0266 | 2023-09-21 |

#### `upptrappning_forsvarsanslag_mot_mal`

Liggarens effekt: forsvarsfinansiering_upptrappning_mot_mal=positive (low)

| OK? | Parti | Stance | B-konsekvens | Konf. | doc_id | Datum |
|-----|-------|--------|--------------|-------|--------|-------|
|  | C | supports | ↑ mot bättre (höjer B) | medium | HC01FöU2 punkt 1 | 2024-12-16 |
|  | KD | supports | ↑ mot bättre (höjer B) | medium | HC01FöU2 punkt 1 | 2024-12-16 |
|  | L | supports | ↑ mot bättre (höjer B) | medium | HC01FöU2 punkt 1 | 2024-12-16 |
|  | M | supports | ↑ mot bättre (höjer B) | medium | HC01FöU2 punkt 1 | 2024-12-16 |
|  | MP | supports | ↑ mot bättre (höjer B) | medium | HC01FöU2 punkt 1 | 2024-12-16 |
|  | S | supports | ↑ mot bättre (höjer B) | medium | HC01FöU2 punkt 1 | 2024-12-16 |
|  | SD | supports | ↑ mot bättre (höjer B) | medium | HC01FöU2 punkt 1 | 2024-12-16 |
|  | V | supports | ↑ mot bättre (höjer B) | medium | HC01FöU2 punkt 1 | 2024-12-16 |

### integration

#### `aktiveringskrav_ekonomiskt_bistand`

Liggarens effekt: bidragsberoende=positive (high); sysselsattningsgap_inrikes_utrikes=positive (medium)

| OK? | Parti | Stance | B-konsekvens | Konf. | doc_id | Datum |
|-----|-------|--------|--------------|-------|--------|-------|
|  | C | supports | ↑ mot bättre (höjer B) | high | HD024032 | 2026-04-01 |
|  | KD | supports | ↑ mot bättre (höjer B) | high | H9024212 | 2021-10-05 |
|  | L | supports | ↑ mot bättre (höjer B) | high | H9024181 | 2021-10-01 |
|  | M | supports | ↑ mot bättre (höjer B) | high | H9024033 | 2021-10-05 |
|  | S | supports | ↑ mot bättre (höjer B) | high | HD024016 | 2026-04-01 |
|  | SD | supports | ↑ mot bättre (höjer B) | high | HA02924 | 2022-11-22 |
|  | V ⚑ | opposes | ↓ mot sämre (sänker B) | high | HD024027 | 2026-04-01 |

#### `riktade_insatser_nyanlanda_elever`

Liggarens effekt: skolresultat_utsatta_omraden=positive (high)

| OK? | Parti | Stance | B-konsekvens | Konf. | doc_id | Datum |
|-----|-------|--------|--------------|-------|--------|-------|
|  | C | supports | ↑ mot bättre (höjer B) | high | HA021880 | 2022-11-23 |
|  | KD | supports | ↑ mot bättre (höjer B) | medium | H9024163 | 2021-10-05 |
|  | L | supports | ↑ mot bättre (höjer B) | high | H9024002 | 2021-10-05 |
|  | M | supports | ↑ mot bättre (höjer B) | high | H9024033 | 2021-10-05 |
|  | SD | supports | ↑ mot bättre (höjer B) | high | HC021447 | 2024-10-02 |
|  | V | supports | ↑ mot bättre (höjer B) | high | HC021932 | 2024-10-03 |

#### `se_over_ansvarsfordelning_atervandande`

Liggarens effekt: atervandande_effektivitet=positive (medium)

| OK? | Parti | Stance | B-konsekvens | Konf. | doc_id | Datum |
|-----|-------|--------|--------------|-------|--------|-------|
|  | C | supports | ↑ mot bättre (höjer B) | high | H801SfU6 punkt 2; votering C7DEF4C6-4668-4D8E-AF06-7A820A666C39 (C 5 ja); motion H802311 (Jonny Cato, C) | 2020-11-11 |
|  | KD | supports | ↑ mot bättre (höjer B) | high | H801SfU6 punkt 2; votering C7DEF4C6-4668-4D8E-AF06-7A820A666C39 (KD 3 ja); motion H802145 yrk. 3 + motion 2020/21:3663 yrk. 30 | 2020-11-11 |
|  | L | supports | ↑ mot bättre (höjer B) | medium | H801SfU6 punkt 2; votering C7DEF4C6-4668-4D8E-AF06-7A820A666C39 (L 3 ja) | 2020-11-11 |
|  | M | supports | ↑ mot bättre (höjer B) | high | H801SfU6 punkt 2; votering C7DEF4C6-4668-4D8E-AF06-7A820A666C39 (M 11 ja); motion H802145 yrk. 3 | 2020-11-11 |
|  | MP ⚑ | opposes | ↓ mot sämre (sänker B) | high | H801SfU6 reservation 3 (S,MP); votering C7DEF4C6-4668-4D8E-AF06-7A820A666C39 (MP 3 nej) | 2020-11-11 |
|  | S ⚑ | opposes | ↓ mot sämre (sänker B) | high | H801SfU6 reservation 3 (S,MP); votering C7DEF4C6-4668-4D8E-AF06-7A820A666C39 (S 15 nej) | 2020-11-11 |
|  | SD | supports | ↑ mot bättre (höjer B) | high | H801SfU6 punkt 2; votering C7DEF4C6-4668-4D8E-AF06-7A820A666C39 (SD 10 ja); motion 2020/21:2552 yrk. 22 | 2020-11-11 |

#### `sfi_kombinerat_med_praktik`

Liggarens effekt: sysselsattningsgap_inrikes_utrikes=positive (high)

| OK? | Parti | Stance | B-konsekvens | Konf. | doc_id | Datum |
|-----|-------|--------|--------------|-------|--------|-------|
|  | C ⚑ | supports | ↑ mot bättre (höjer B) | low | HB021255 | 2023-10-04 |
|  | KD ⚑ | supports | ↑ mot bättre (höjer B) | low | H9024198 | 2021-10-04 |
|  | L ⚑ | supports | ↑ mot bättre (höjer B) | low | H9023965 | 2021-10-05 |
|  | M ⚑ | supports | ↑ mot bättre (höjer B) | low | H4023372 | 2016-10-05 |
|  | S | supports | ↑ mot bättre (höjer B) | high | HD02319 | 2025-09-25 |

#### `sprakpraktik_kombinerad_sprakutbildning_och_arbetspraktik`

Liggarens effekt: sysselsattningsgap_inrikes_utrikes=positive (medium)

| OK? | Parti | Stance | B-konsekvens | Konf. | doc_id | Datum |
|-----|-------|--------|--------------|-------|--------|-------|
|  | C | supports | ↑ mot bättre (höjer B) | high | HD023738 | 2025-10-07 |
|  | KD ⚑ | supports | ↑ mot bättre (höjer B) | low | HD021563 | 2025-10-02 |
|  | MP | supports | ↑ mot bättre (höjer B) | medium | GQ02Sf289 | 2002-10-23 |
|  | V | supports | ↑ mot bättre (höjer B) | high | HA021299 | 2022-11-22 |

#### `uppsokande_forskoleerbjudande_nyanlandas_barn`

Liggarens effekt: skolresultat_utsatta_omraden=positive (medium)

| OK? | Parti | Stance | B-konsekvens | Konf. | doc_id | Datum |
|-----|-------|--------|--------------|-------|--------|-------|
|  | C | supports | ↑ mot bättre (höjer B) | high | H901UbU24 / votering 13F52F92-6597-473E-B912-4C7BB0EEE42F | 2022-06-08 |
|  | L | supports | ↑ mot bättre (höjer B) | high | H901UbU24 / votering 13F52F92-6597-473E-B912-4C7BB0EEE42F | 2022-06-08 |
|  | M | supports | ↑ mot bättre (höjer B) | high | H901UbU24 / votering 13F52F92-6597-473E-B912-4C7BB0EEE42F | 2022-06-08 |
|  | MP | supports | ↑ mot bättre (höjer B) | high | H901UbU24 / votering 13F52F92-6597-473E-B912-4C7BB0EEE42F | 2022-06-08 |
|  | S | supports | ↑ mot bättre (höjer B) | high | H901UbU24 / votering 13F52F92-6597-473E-B912-4C7BB0EEE42F | 2022-06-08 |
|  | V | supports | ↑ mot bättre (höjer B) | high | H901UbU24 / votering 13F52F92-6597-473E-B912-4C7BB0EEE42F | 2022-06-08 |

### klimat

#### `atgarder_mot_invasiva_frammande_arter`

Liggarens effekt: hotade_arter_naturforlust=positive (low)

| OK? | Parti | Stance | B-konsekvens | Konf. | doc_id | Datum |
|-----|-------|--------|--------------|-------|--------|-------|
|  | C | supports | ↑ mot bättre (höjer B) | high | HD01MJU13 punkt 1 | 2026-03-12 |
|  | KD | supports | ↑ mot bättre (höjer B) | high | HD01MJU13 punkt 1 | 2026-03-12 |
|  | L | supports | ↑ mot bättre (höjer B) | high | HD01MJU13 punkt 1 | 2026-03-12 |
|  | M | supports | ↑ mot bättre (höjer B) | high | HD01MJU13 punkt 1 | 2026-03-12 |
|  | MP | supports | ↑ mot bättre (höjer B) | high | HD01MJU13 punkt 1 | 2026-03-12 |
|  | S | supports | ↑ mot bättre (höjer B) | high | HD01MJU13 punkt 1 | 2026-03-12 |
|  | SD | supports | ↑ mot bättre (höjer B) | high | HD01MJU13 punkt 1 | 2026-03-12 |
|  | V | supports | ↑ mot bättre (höjer B) | high | HD01MJU13 punkt 1 | 2026-03-12 |

#### `koldioxidskatt`

Liggarens effekt: territoriella_utslapp=positive (medium); utslappsminskning_per_krona=positive (medium)

| OK? | Parti | Stance | B-konsekvens | Konf. | doc_id | Datum |
|-----|-------|--------|--------------|-------|--------|-------|
|  | KD | supports | ↑ mot bättre (höjer B) | — | H8022807 | 2020/21 |
|  | L | supports | ↑ mot bättre (höjer B) | — | H9024199 | 2021/22 |
|  | M | supports | ↑ mot bättre (höjer B) | — | H9024030 | 2021/22 |
|  | MP | supports | ↑ mot bättre (höjer B) | — | HC022613 | 2024/25 |
|  | SD ⚑ | opposes | ↓ mot sämre (sänker B) | — | HA02998 | 2022/23 |
|  | V | supports | ↑ mot bättre (höjer B) | — | HC021924 | 2024/25 |

#### `ny_karnkraft`

Liggarens effekt: effektbrist=positive (high)

| OK? | Parti | Stance | B-konsekvens | Konf. | doc_id | Datum |
|-----|-------|--------|--------------|-------|--------|-------|
|  | KD ⚑ | supports | ↑ mot bättre (höjer B) | medium | H9024195 | 2021-10-05 |
|  | L ⚑ | supports | ↑ mot bättre (höjer B) | medium | H8023242 | 2020-10-06 |
|  | M ⚑ | supports | ↑ mot bättre (höjer B) | medium | H9023688 | 2021-10-05 |
|  | MP ⚑ | opposes | ↓ mot sämre (sänker B) | high | HD023984 | 2026-03-25 |
|  | S ⚑ | supports | ↑ mot bättre (höjer B) | medium | HD023594 | 2025-10-07 |
|  | SD ⚑ | supports | ↑ mot bättre (höjer B) | high | HC021464 | 2024-10-02 |
|  | V ⚑ | opposes | ↓ mot sämre (sänker B) | high | HD023961 | 2026-03-19 |

#### `reduktionsplikt_drivmedel`

Liggarens effekt: territoriella_utslapp=positive (medium)

| OK? | Parti | Stance | B-konsekvens | Konf. | doc_id | Datum |
|-----|-------|--------|--------------|-------|--------|-------|
|  | C | supports | ↑ mot bättre (höjer B) | — | HB01MJU5 / votering 21E8B615-C235-489F-8189-D26CABD56F24 punkt 1 | 2023/24 |
|  | KD ⚑ | opposes | ↓ mot sämre (sänker B) | — | HB01MJU5 / votering 21E8B615-C235-489F-8189-D26CABD56F24 punkt 1 | 2023/24 |
|  | L ⚑ | opposes | ↓ mot sämre (sänker B) | — | HB01MJU5 / votering 21E8B615-C235-489F-8189-D26CABD56F24 punkt 1 | 2023/24 |
|  | M ⚑ | opposes | ↓ mot sämre (sänker B) | — | HB01MJU5 / votering 21E8B615-C235-489F-8189-D26CABD56F24 punkt 1 | 2023/24 |
|  | MP | supports | ↑ mot bättre (höjer B) | — | HB01MJU5 / votering 21E8B615-C235-489F-8189-D26CABD56F24 punkt 1 | 2023/24 |
|  | S | supports | ↑ mot bättre (höjer B) | — | HB01MJU5 / votering 21E8B615-C235-489F-8189-D26CABD56F24 punkt 1 | 2023/24 |
|  | SD ⚑ | opposes | ↓ mot sämre (sänker B) | — | HB01MJU5 / votering 21E8B615-C235-489F-8189-D26CABD56F24 punkt 1 | 2023/24 |
|  | V | supports | ↑ mot bättre (höjer B) | — | HB01MJU5 / votering 21E8B615-C235-489F-8189-D26CABD56F24 punkt 1 | 2023/24 |

### trygghet

#### `behandlingsprogram_kriminalvard`

Liggarens effekt: aterfall_i_brott=positive (medium)

| OK? | Parti | Stance | B-konsekvens | Konf. | doc_id | Datum |
|-----|-------|--------|--------------|-------|--------|-------|
|  | C | supports | ↑ mot bättre (höjer B) | high | H6023062 | 2019-04-10 |
|  | KD ⚑ | supports | ↑ mot bättre (höjer B) | low | HD021560 | 2025-10-02 |
|  | L | supports | ↑ mot bättre (höjer B) | high | H9023974 | 2021-10-05 |
|  | M | supports | ↑ mot bättre (höjer B) | high | H9023779 | 2021-09-30 |
|  | MP | supports | ↑ mot bättre (höjer B) | medium | HC023268 | 2024-11-20 |
|  | S | supports | ↑ mot bättre (höjer B) | high | HC023264 | 2024-11-20 |
|  | V | supports | ↑ mot bättre (höjer B) | high | H902916 | 2021-09-29 |

#### `fokuserad_avskrackning_gvi`

Liggarens effekt: skjutningar_sprangningar=positive (medium)

| OK? | Parti | Stance | B-konsekvens | Konf. | doc_id | Datum |
|-----|-------|--------|--------------|-------|--------|-------|
|  | MP ⚑ | supports | ↑ mot bättre (höjer B) | low | H8022726 | 2020-10-05 |
|  | S | supports | ↑ mot bättre (höjer B) | high | HC023111 | 2024-10-04 |
|  | V | supports | ↑ mot bättre (höjer B) | high | HD022788 | 2025-10-06 |

#### `lagstadgat_kommunalt_brottsforebyggande_ansvar`

Liggarens effekt: kommunalt_brottsforebyggande_arbete=positive (low)

| OK? | Parti | Stance | B-konsekvens | Konf. | doc_id | Datum |
|-----|-------|--------|--------------|-------|--------|-------|
|  | C | supports | ↑ mot bättre (höjer B) | high | HA01JuU9 punkt 1 | 2023-03-23 |
|  | KD | supports | ↑ mot bättre (höjer B) | high | HA01JuU9 punkt 1 | 2023-03-23 |
|  | L | supports | ↑ mot bättre (höjer B) | high | HA01JuU9 punkt 1 | 2023-03-23 |
|  | M | supports | ↑ mot bättre (höjer B) | high | HA01JuU9 punkt 1 | 2023-03-23 |
|  | MP | supports | ↑ mot bättre (höjer B) | high | HA01JuU9 punkt 1 | 2023-03-23 |
|  | S | supports | ↑ mot bättre (höjer B) | high | HA01JuU9 punkt 1 | 2023-03-23 |
|  | SD | supports | ↑ mot bättre (höjer B) | high | HA01JuU9 punkt 1 | 2023-03-23 |
|  | V | supports | ↑ mot bättre (höjer B) | high | HA01JuU9 punkt 1 | 2023-03-23 |

#### `situationell_prevention_utomhusbelysning`

Liggarens effekt: brottsutsatthet=positive (medium)

| OK? | Parti | Stance | B-konsekvens | Konf. | doc_id | Datum |
|-----|-------|--------|--------------|-------|--------|-------|
|  | KD | supports | ↑ mot bättre (höjer B) | medium | H3022686 | 2015-10-06 |
|  | L | supports | ↑ mot bättre (höjer B) | medium | H9023974 | 2021-10-05 |
|  | MP | supports | ↑ mot bättre (höjer B) | medium | HB022669 | 2023-10-05 |
|  | SD ⚑ | supports | ↑ mot bättre (höjer B) | low | HD02256 | 2025-09-24 |
|  | V | supports | ↑ mot bättre (höjer B) | medium | HA021217 | 2022-11-01 |

#### `snabbforfarande_lagforing`

Liggarens effekt: handlaggningstid=positive (medium)

| OK? | Parti | Stance | B-konsekvens | Konf. | doc_id | Datum |
|-----|-------|--------|--------------|-------|--------|-------|
|  | C | supports | ↑ mot bättre (höjer B) | high | HA01JuU2 punkt 1 | 2022-12-07 |
|  | KD | supports | ↑ mot bättre (höjer B) | high | HA01JuU2 punkt 1 | 2022-12-07 |
|  | L | supports | ↑ mot bättre (höjer B) | high | HA01JuU2 punkt 1 | 2022-12-07 |
|  | M | supports | ↑ mot bättre (höjer B) | high | HA01JuU2 punkt 1 | 2022-12-07 |
|  | MP | supports | ↑ mot bättre (höjer B) | high | HA01JuU2 punkt 1 | 2022-12-07 |
|  | S | supports | ↑ mot bättre (höjer B) | high | HA01JuU2 punkt 1 | 2022-12-07 |
|  | SD | supports | ↑ mot bättre (höjer B) | high | HA01JuU2 punkt 1 | 2022-12-07 |
|  | V | supports | ↑ mot bättre (höjer B) | high | HA01JuU2 punkt 1 | 2022-12-07 |

### valfard

#### `fast_omsorgskontakt`

Liggarens effekt: kontinuitet_i_omsorgen=positive (low)

| OK? | Parti | Stance | B-konsekvens | Konf. | doc_id | Datum |
|-----|-------|--------|--------------|-------|--------|-------|
|  | C | supports | ↑ mot bättre (höjer B) | high | H901SoU24 punkt 2 | 2022-04-25 |
|  | KD | supports | ↑ mot bättre (höjer B) | high | H901SoU24 punkt 2 | 2022-04-25 |
|  | L | supports | ↑ mot bättre (höjer B) | high | H901SoU24 punkt 2 | 2022-04-25 |
|  | M | supports | ↑ mot bättre (höjer B) | high | H901SoU24 punkt 2 | 2022-04-25 |
|  | MP | supports | ↑ mot bättre (höjer B) | high | H901SoU24 punkt 2 | 2022-04-25 |
|  | S | supports | ↑ mot bättre (höjer B) | high | H901SoU24 punkt 2 | 2022-04-25 |
|  | SD | supports | ↑ mot bättre (höjer B) | high | H901SoU24 punkt 2 | 2022-04-25 |
|  | V | supports | ↑ mot bättre (höjer B) | high | H901SoU24 punkt 2 | 2022-04-25 |

#### `kompetensutveckling_larare`

Liggarens effekt: skolresultat=positive (medium)

| OK? | Parti | Stance | B-konsekvens | Konf. | doc_id | Datum |
|-----|-------|--------|--------------|-------|--------|-------|
|  | C | supports | ↑ mot bättre (höjer B) | high | HD023186 | 2025-10-06 |
|  | KD | supports | ↑ mot bättre (höjer B) | high | H9024163 | 2021-10-05 |
|  | L | supports | ↑ mot bättre (höjer B) | high | H9024181 | 2021-10-05 |
|  | M | supports | ↑ mot bättre (höjer B) | high | H9023988 | 2021-10-05 |
|  | MP | supports | ↑ mot bättre (höjer B) | high | HD023364 | 2025-10-06 |
|  | S | supports | ↑ mot bättre (höjer B) | high | HB022687 | 2023-10-05 |
|  | SD | supports | ↑ mot bättre (höjer B) | high | H9022542 | 2021-10-01 |
|  | V | supports | ↑ mot bättre (höjer B) | medium | HC021924 | 2024-10-03 |

#### `koncentration_nationell_hogspecialiserad_vard`

Liggarens effekt: overlevnad_svar_sjukdom=positive (low)

| OK? | Parti | Stance | B-konsekvens | Konf. | doc_id | Datum |
|-----|-------|--------|--------------|-------|--------|-------|
|  | C | supports | ↑ mot bättre (höjer B) | medium | H501SoU18 punkt 1 | 2018-02-20 |
|  | KD | supports | ↑ mot bättre (höjer B) | medium | H501SoU18 punkt 1 | 2018-02-20 |
|  | L | supports | ↑ mot bättre (höjer B) | medium | H501SoU18 punkt 1 | 2018-02-20 |
|  | M | supports | ↑ mot bättre (höjer B) | medium | H501SoU18 punkt 1 | 2018-02-20 |
|  | MP | supports | ↑ mot bättre (höjer B) | medium | H501SoU18 punkt 1 | 2018-02-20 |
|  | S | supports | ↑ mot bättre (höjer B) | medium | H501SoU18 punkt 1 | 2018-02-20 |
|  | SD | supports | ↑ mot bättre (höjer B) | medium | H501SoU18 punkt 1 | 2018-02-20 |
|  | V | supports | ↑ mot bättre (höjer B) | medium | H501SoU18 punkt 1 | 2018-02-20 |

#### `kontroller_och_informationsutbyte_mot_valfardsbrott`

Liggarens effekt: valfardsbrottslighet=positive (medium)

| OK? | Parti | Stance | B-konsekvens | Konf. | doc_id | Datum |
|-----|-------|--------|--------------|-------|--------|-------|
|  | C | supports | ↑ mot bättre (höjer B) | medium | HC023249 | 2024-10-30 |
|  | KD | supports | ↑ mot bättre (höjer B) | high | H9024184 | 2021-10-05 |
|  | L | supports | ↑ mot bättre (höjer B) | high | H9023974 | 2021-10-05 |
|  | M ⚑ | supports | ↑ mot bättre (höjer B) | low | HC023146 | 2024-10-04 |
|  | MP | supports | ↑ mot bättre (höjer B) | high | HB022669 | 2023-10-05 |
|  | SD | supports | ↑ mot bättre (höjer B) | high | HA021147 | 2022-11-22 |
|  | V | supports | ↑ mot bättre (höjer B) | medium | HC023445 | 2025-06-17 |

#### `minskad_klasstorlek`

Liggarens effekt: skolresultat=positive (high)

| OK? | Parti | Stance | B-konsekvens | Konf. | doc_id | Datum |
|-----|-------|--------|--------------|-------|--------|-------|
|  | C | supports | ↑ mot bättre (höjer B) | high | HD023186 | 2025-10-06 |
|  | KD | supports | ↑ mot bättre (höjer B) | medium | H2023002 | 2014-11-11 |
|  | L | supports | ↑ mot bättre (höjer B) | medium | H2023002 | 2014-11-11 |
|  | M | supports | ↑ mot bättre (höjer B) | medium | H2023002 | 2014-11-11 |
|  | S | supports | ↑ mot bättre (höjer B) | high | HD023810 | 2025-10-07 |
|  | SD ⚑ | opposes | ↓ mot sämre (sänker B) | high | H302761 | 2015-10-02 |
|  | V | supports | ↑ mot bättre (höjer B) | high | HD022791 | 2025-10-06 |

#### `tidiga_insatser_lagstadiet`

Liggarens effekt: skolresultat=positive (medium)

| OK? | Parti | Stance | B-konsekvens | Konf. | doc_id | Datum |
|-----|-------|--------|--------------|-------|--------|-------|
|  | C | supports | ↑ mot bättre (höjer B) | medium | H5024117 | 2018-04-11 |
|  | KD | supports | ↑ mot bättre (höjer B) | medium | H5024117 | 2018-04-11 |
|  | M | supports | ↑ mot bättre (höjer B) | medium | H5024117 | 2018-04-11 |
|  | MP | supports | ↑ mot bättre (höjer B) | high | HD023364 | 2025-10-06 |
|  | S | supports | ↑ mot bättre (höjer B) | high | HD023810 | 2025/26 |
|  | SD ⚑ | opposes | ↓ mot sämre (sänker B) | high | H501UbU10 | 2018-05-30 |
