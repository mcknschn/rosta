# Migrationsdiff: gammal form mot ny (ADR 0019, biljett #50)

- Datum: 2026-09-16
- **ICKE-LONGITUDINELL.** Den här diffen jämför två OLIKA MÄTSKALOR och är inget besked om att
  något parti rört sig i sak. Den är ett **migrationsbevis**: den visar att omkörningen ger det
  avsedda skalbrottet och inga oavsiktliga ändringar därutöver.
- Efter den här diffen skrivs driftbaslinjen om. Den gamla baslinjen står kvar i
  versionshistorien (`git show HEAD:dist/scores.snapshot.json` från commiten före bygget).

## Vad som ändrades

Formen byttes från ett kvalitetsviktat medel över hela cellen till poolning inom åtgärdstyp plus
summa över åtgärdstyper mot en fast budget `K = R x max(effect_strength)` med `R = 3`.

**Rangordningen står still:** M > KD > L > S > C > MP > SD > V, samma som före bytet. Samtliga
betyg komprimeras mot neutral, vilket är formens förutsagda följd: de flesta celler fyller bara
en liten del av den tillåtna evidensbudgeten. Det är inte ett fel om budgeten verkligen är full
kapacitet; det är ett besked om hur tunt underlaget är.

Den nya flaggan `B_terms_n` är antalet åtgärdstyper som bildade led i summan (D6 punkt 5).

## Rader

```
TOTAL C: +2.868 -> +2.708 (-0.160)
TOTAL KD: +2.957 -> +2.771 (-0.186)
TOTAL L: +2.919 -> +2.724 (-0.195)
TOTAL M: +2.973 -> +2.780 (-0.193)
TOTAL MP: +2.824 -> +2.701 (-0.123)
TOTAL S: +2.893 -> +2.720 (-0.173)
TOTAL SD: +2.793 -> +2.657 (-0.136)
TOTAL V: +2.622 -> +2.568 (-0.054)
BETYG C/demokrati: 2.911 -> 2.686 (-0.225)
FLAGGOR C/demokrati: +['B_terms_2']
BETYG C/ekonomi: 2.881 -> 2.666 (-0.215)
FLAGGOR C/ekonomi: +['B_terms_5']
BETYG C/forsvar: 3.061 -> 2.836 (-0.225)
FLAGGOR C/forsvar: +['B_terms_3']
BETYG C/integration: 3.103 -> 2.923 (-0.180)
FLAGGOR C/integration: +['B_terms_6']
BETYG C/klimat: 2.706 -> 2.617 (-0.089)
FLAGGOR C/klimat: +['B_terms_1']
BETYG C/trygghet: 2.732 -> 2.557 (-0.175)
FLAGGOR C/trygghet: +['B_terms_2']
BETYG C/valfard: 2.781 -> 2.724 (-0.057)
FLAGGOR C/valfard: +['B_terms_4']
BETYG KD/demokrati: 2.562 -> 2.537 (-0.025)
FLAGGOR KD/demokrati: +['B_terms_2']
BETYG KD/ekonomi: 2.863 -> 2.604 (-0.259)
FLAGGOR KD/ekonomi: +['B_terms_5']
BETYG KD/forsvar: 3.248 -> 3.023 (-0.225)
FLAGGOR KD/forsvar: +['B_terms_3']
BETYG KD/integration: 3.109 -> 2.929 (-0.180)
FLAGGOR KD/integration: +['B_terms_5']
BETYG KD/klimat: 2.905 -> 2.625 (-0.280)
TÄCKNING KD/klimat: 0.782 -> 0.820 (+0.038)
FLAGGOR KD/klimat: +['B_shrink_70/85', 'B_terms_3'] -['B_shrink_62.5/85']
BETYG KD/trygghet: 3.119 -> 2.894 (-0.225)
FLAGGOR KD/trygghet: +['B_terms_3']
BETYG KD/valfard: 2.815 -> 2.758 (-0.057)
FLAGGOR KD/valfard: +['B_terms_4']
BETYG L/demokrati: 2.641 -> 2.616 (-0.025)
FLAGGOR L/demokrati: +['B_terms_2']
BETYG L/ekonomi: 2.94 -> 2.681 (-0.259)
FLAGGOR L/ekonomi: +['B_terms_5']
BETYG L/forsvar: 3.186 -> 2.961 (-0.225)
FLAGGOR L/forsvar: +['B_terms_3']
BETYG L/integration: 3.024 -> 2.829 (-0.195)
FLAGGOR L/integration: +['B_terms_5']
BETYG L/klimat: 2.834 -> 2.555 (-0.279)
TÄCKNING L/klimat: 0.762 -> 0.800 (+0.038)
FLAGGOR L/klimat: +['B_shrink_70/85', 'B_terms_3'] -['B_shrink_62.5/85']
BETYG L/trygghet: 2.973 -> 2.748 (-0.225)
FLAGGOR L/trygghet: +['B_terms_3']
BETYG L/valfard: 2.76 -> 2.667 (-0.093)
FLAGGOR L/valfard: +['B_terms_3']
BETYG M/demokrati: 2.524 -> 2.499 (-0.025)
FLAGGOR M/demokrati: +['B_terms_2']
BETYG M/ekonomi: 3.048 -> 2.725 (-0.323)
FLAGGOR M/ekonomi: +['B_terms_5']
BETYG M/forsvar: 3.05 -> 2.825 (-0.225)
FLAGGOR M/forsvar: +['B_terms_3']
BETYG M/integration: 3.124 -> 2.929 (-0.195)
FLAGGOR M/integration: +['B_terms_5']
BETYG M/klimat: 2.984 -> 2.704 (-0.280)
TÄCKNING M/klimat: 0.782 -> 0.820 (+0.038)
FLAGGOR M/klimat: +['B_shrink_70/85', 'B_terms_3'] -['B_shrink_62.5/85']
BETYG M/trygghet: 3.074 -> 2.899 (-0.175)
FLAGGOR M/trygghet: +['B_terms_2']
BETYG M/valfard: 2.848 -> 2.791 (-0.057)
FLAGGOR M/valfard: +['B_terms_4']
BETYG MP/demokrati: 2.912 -> 2.687 (-0.225)
FLAGGOR MP/demokrati: +['B_terms_2']
BETYG MP/ekonomi: 3.043 -> 2.867 (-0.176)
FLAGGOR MP/ekonomi: +['B_terms_5']
BETYG MP/forsvar: 2.658 -> 2.696 (+0.038)
FLAGGOR MP/forsvar: +['B_terms_1']
BETYG MP/integration: 2.735 -> 2.622 (-0.113)
FLAGGOR MP/integration: +['B_terms_3']
BETYG MP/klimat: 2.712 -> 2.784 (+0.072)
TÄCKNING MP/klimat: 0.782 -> 0.820 (+0.038)
FLAGGOR MP/klimat: +['B_shrink_70/85', 'B_terms_3'] -['B_shrink_62.5/85']
BETYG MP/trygghet: 2.969 -> 2.594 (-0.375)
FLAGGOR MP/trygghet: +['B_terms_4']
BETYG MP/valfard: 2.701 -> 2.611 (-0.090)
FLAGGOR MP/valfard: +['B_terms_3']
BETYG S/demokrati: 2.557 -> 2.532 (-0.025)
FLAGGOR S/demokrati: +['B_terms_2']
BETYG S/ekonomi: 3.019 -> 2.843 (-0.176)
FLAGGOR S/ekonomi: +['B_terms_5']
BETYG S/forsvar: 3.094 -> 2.869 (-0.225)
FLAGGOR S/forsvar: +['B_terms_3']
BETYG S/integration: 2.747 -> 2.613 (-0.134)
FLAGGOR S/integration: +['B_terms_4']
BETYG S/klimat: 3.016 -> 2.71 (-0.306)
FLAGGOR S/klimat: +['B_terms_2']
BETYG S/trygghet: 2.886 -> 2.561 (-0.325)
FLAGGOR S/trygghet: +['B_terms_3']
BETYG S/valfard: 2.742 -> 2.736 (-0.006)
FLAGGOR S/valfard: +['B_terms_3']
BETYG SD/demokrati: 2.439 -> 2.539 (+0.100)
FLAGGOR SD/demokrati: +['B_terms_1']
BETYG SD/ekonomi: 2.863 -> 2.583 (-0.280)
FLAGGOR SD/ekonomi: +['B_terms_5']
BETYG SD/forsvar: 3.154 -> 2.929 (-0.225)
FLAGGOR SD/forsvar: +['B_terms_3']
BETYG SD/integration: 2.919 -> 2.757 (-0.162)
FLAGGOR SD/integration: +['B_terms_3']
BETYG SD/klimat: 2.452 -> 2.38 (-0.072)
TÄCKNING SD/klimat: 0.753 -> 0.790 (+0.037)
FLAGGOR SD/klimat: +['B_shrink_70/85', 'B_terms_3'] -['B_shrink_62.5/85']
BETYG SD/trygghet: 3.049 -> 2.899 (-0.150)
FLAGGOR SD/trygghet: +['B_terms_2']
BETYG SD/valfard: 2.545 -> 2.515 (-0.030)
FLAGGOR SD/valfard: +['B_terms_4']
BETYG V/demokrati: 2.83 -> 2.605 (-0.225)
FLAGGOR V/demokrati: +['B_terms_2']
BETYG V/ekonomi: 2.238 -> 2.453 (+0.215)
FLAGGOR V/ekonomi: +['B_terms_5']
BETYG V/forsvar: 2.703 -> 2.578 (-0.125)
FLAGGOR V/forsvar: +['B_terms_3']
BETYG V/integration: 2.544 -> 2.591 (+0.047)
FLAGGOR V/integration: +['B_terms_4']
BETYG V/klimat: 2.464 -> 2.536 (+0.072)
TÄCKNING V/klimat: 0.562 -> 0.600 (+0.038)
FLAGGOR V/klimat: +['B_shrink_70/85', 'B_terms_3'] -['B_shrink_62.5/85']
BETYG V/trygghet: 3.071 -> 2.696 (-0.375)
FLAGGOR V/trygghet: +['B_terms_4']
BETYG V/valfard: 2.666 -> 2.574 (-0.092)
FLAGGOR V/valfard: +['B_terms_3']
```
