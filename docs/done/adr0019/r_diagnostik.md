# R-diagnostik (ADR 0019, D5)

- Datum: 2026-09-16, FÖRE omkörningen av stabilitetsanalysen
- **Detta är nivå- och klippningsdiagnostik, ALDRIG rangordningsstabilitet.** ADR 0003:s mått
  saknar strukturellt känslighet för en gemensam positiv skalning före klippning, så att dra R
  mot det måttet hade visat nära hundra procent stabilitet och bevisat ingenting.
- Spannet {2, 3, 4, 5} och redovisningsmåtten är förhandsregistrerade i ADR 0019 D5. Resultatet
  får **inte** användas för att välja R i efterhand: `R = 3` är låst i modellversionen på sitt
  eget normativa skäl, alltså att full skala betyder tre skilda åtgärdstyper som var och en
  bidrar maximalt i samma riktning.
- En faktor i taget och full korsprodukt sammanfaller, eftersom bara R varierar.
- Alternativestimand är en **ej tillämplig gren**: inom-utvärderingssammanvägning fyrar bara när
  flera estimand delar nod, och det finns noll sådana fall. Återöppningsvillkoret är maskinläst,
  eftersom en kollision ger hård fail.

| R | B min | B max | B medel | B spann | celler vid skalans ändpunkt |
|---|---|---|---|---|---|
| 2 | 2.206 | 3.424 | 2.850 | 1.218 | 0 |
| 3 | 2.304 | 3.116 | 2.733 | 0.812 | 0 |
| 4 | 2.353 | 2.962 | 2.675 | 0.609 | 0 |
| 5 | 2.382 | 2.869 | 2.640 | 0.487 | 0 |

Ett större R trycker varje cell närmare neutral, eftersom samma täljare delas med en större
budget. Ett mindre R gör motsatsen och för fler celler mot klippning. Talen ovan är redovisade
som de blev.
