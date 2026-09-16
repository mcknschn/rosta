# Löftesspårets form

Spårets bärande beslut. Grillningen i biljett
[#52](https://github.com/mcknschn/rosta/issues/52) avgjorde dem, och biljettens sex öppna frågor
är stängda.

- Datum: **2026-09-16**
- Beslutad av: projektägaren i [#52](https://github.com/mcknschn/rosta/issues/52)
- Reglerna i kort form: [`loften/CLAUDE.md`](../../CLAUDE.md)
- Förebild: Thomson, Royed, Naurin med flera (2017), *The Fulfillment of Parties' Election
  Pledges*, AJPS 61(3). Källan ligger i
  [`docs/research/vikter_avsikt_vs_utfall.md`](../../../docs/research/vikter_avsikt_vs_utfall.md)
  punkt 11.

**Detta dokument är ingen ADR.** ADR-serien är numrerad för modellens delpoäng. Spåret väger 0,
och en ADR om det skulle sudda ut gränsen som beslut 1 och beslut 2 drar.

## Anspråket

Spåret svarar på en fråga: **vad lovade partiet, och arbetade det sedan med löftet?** Aldrig om
löftet var bra för Sverige. Den frågan äger delpoäng B och D.

---

## A. Spårets ställning

**1. Spåret väger 0 och rör ingenting annat.** Inga betyg, band eller rangordningar. `dist/`
skrivs aldrig härifrån. Vikterna 0,30 A + 0,50 B + 0,20 D med C = 0 står orörda (ADR 0002).

*Skäl:* spåret mäter avsikt mot handling och prövar aldrig om åtgärden var klok. En vikt över 0
skulle låta ett uppfyllt löfte höja betyget utan att någon prövat nyttan.

**2. Modellens sju kategorier rörs inte.** En utökning är en egen biljett med egen ADR.

*Skäl:* varje kategori i [`config/categories.yaml`](../../../config/categories.yaml) bär ett
`standard_weight`, och `test_standard_weights_sum_to_100` kräver att de sju summerar till 100. En
åttonde kategori tar vikt från de sju, och **varje partis betyg rör sig**.
`test_seven_categories` låser dessutom antalet. En ny kategori behöver därtill undermått,
indikatorer med officiell källa, evidens på B-sidan och utfall på D-sidan, annars står den tom.

---

## B. Löftessidan

**3. Posten följer dokumentets egen struktur.** Samma regel för båda årgångarna, alltså den regel
2026 års mappning redan använde: numrerade löften hos SD och L, punktlistor hos M, KD och MP,
numrerade punkter hos C, fetstilt rubrik per förslag hos V och S.

*Skäl:* årgångarna ska gå att jämföra, och det går bara om posten betyder samma sak i båda. Varje
post är dessutom en rubrik eller punkt som står ordagrant i PDF:en, så en andra genomgång kan slå
upp den. Låter man kodaren dra gränsen mäter differenstalet mest hur olika två kodare styckar text.

**4. Atomisering ligger i ett eget lager ovanpå extraktionen.** En post som bär flera skilda
åtgärder styckas till en post per åtgärd. Provet är: **kan det här bli två skilda motioner?**
Ursprungspostens id står kvar. Tummen sätts på den atomära posten.

*Skäl:* ett parti som buntar tio åtgärder i en punkt får en post, ett parti som listar dem var för
sig får tio. Ett enda papper räcker då för buntaren men inte för listaren, så tummen betyder olika
saker för olika partier. Ingen nämnare rättar det felet. Lagret läggs ovanpå och inte i
extraktionen, så att dokumentets egen post finns kvar, den frysta korpusen är fortfarande jämförbar
som tredje genomgång, och låsningen i beslut 8 gäller extraktionen medan lagret låses för sig.

**5. Registret dras om ur PDF:erna, med full lydelse och sidnummer.** Den frysta korpusen ändras
aldrig. Där en registerpost svarar mot en korpuspost bärs korpusens id som referens, och
skillnaden mellan listorna räknas och redovisas.

*Skäl:* biljetten krävde full lydelse i korpusen och förbjöd samtidigt varje ändring av den. Båda
kan inte gälla. Korpusen är dessutom en genomgång gjord för ett nedlagt mått, med en annan
urvalsregel. Jämförd mot de två blinda genomgångarna blir den en **tredje oberoende genomgång**,
och tre genomgångar säger något om kompletthet som två inte kan säga.

**6. Prövbart löfte avgörs av handlingsprovet.** Posten ska namnge en åtgärd som går att lägga på
papper: en lag, ett anslag, ett uppdrag, ett förbud eller ett avtal. Bortfallet redovisas per parti.

*Skäl:* storhetsprovet, alltså kravet på både storhet och period, är redan mätt mot materialet och
klarades av **2 poster av 1 073**. Det lämnar inget spår. Att räkna allt gör talet meningslöst,
eftersom ett värdepåstående aldrig kan arbetas med och varje parti då straffas i proportion till
hur mycket stämningsprosa dess manifest bär. Piloten kodade 112 rena värdepåståenden av 200
utsagor, så ett stort bortfall är väntat. Olika bortfall mellan partier är ett fel i sig och måste
därför synas.

**7. Kompletthet beläggs med två blinda genomgångar.** Skilda kontexter, samma instruktion, ingen
ser den andras utdata. Tre tal redovisas per dokument: poster bara A har, poster bara B har, och
poster båda har men lagt olika. Projektägaren avgör varje differens innan låsning.

*Skäl:* pilotens tre kodare hittade motsägelsen i kodboken därför att de arbetade isär. En ensam
genomgång kan aldrig visa vad den missade, och ett kompletthetspåstående blir prövbart först när
det finns två genomgångar att jämföra. I granskningsläge, där den andra ser den första, mäter
differenstalet bara hur väl den andra höll med om ett svar den redan sett.

**8. Registret låses hårt.** Hashpinnat, med PDF-hashen i hämtmanifestet och ett prov som faller på
en ändrad bokstav. Enda öppningen: ett avskrivningsfel som går att belägga mot PDF:en rättas som
**errata-rad** med datum och skäl, aldrig genom att ändra posten.

*Skäl:* projektet gör redan så två gånger. Ett register som får röra sig medan kodningen pågår
låter kodningen forma registret, vilket är efterhandsval i ren form.

**9. Alla löften räknas, också de utanför de sju kategorierna.**

*Skäl:* andelen utanför skiljer sig sexfaldigt mellan partierna, från M 2,2 procent till SD 13,2
procent. Gallras de bort blir nämnaren en annan sak för SD än för M, av ett skäl som inte har med
partiet att göra utan med vad Rösta valde att mäta.

**10. Spåret får en egen, längre kategorilista.** Fältet heter `kategori`, och varje post bär om
kategorin är en av modellens sju eller en kandidat.

*Skäl:* en kandidat är samma slags sak som de sju så snart den bär undermått och indikatorer, så
ordet får delas. Men modellens lista kan inte växa inifrån ett spår som väger 0 (beslut 2).

**11. Listan bestäms först när 2022 är mappat.** Underlaget är 2022-registret plus den frysta
korpusens 1 073 poster som 2026-bild. Extraktionen bär **inget kategorifält alls**. Listan skrivs
ned med antal per kategori och låses innan en enda post kategoriseras.

*Skäl:* en lista som sätts i förväg formas efter gissningar, och en lista som växer under
kodningen formas efter materialet i efterhand. Korpusen är redan en fullständig genomgång av 2026
års åtta dokument, så ett fullt 2026-register behöver inte inväntas.

**12. En ärlig rest är tillåten.** En post hamnar i resten bara när ingen kategori passar utan att
töjas. Resten läses igenom efter kodningen, och växer den är det beskedet att en kategori fattas.

*Skäl:* en påtvingad etikett är sämre än en rest, eftersom den döljer att kategorin saknas. Resten
är underlaget till biljetten i beslut 2.

**13. Båda årgångarna visas.** 2022 med tummar. 2026 som ren karta, **utan kolumn för
uppfyllelse, inte ens en tom**.

*Skäl:* frysningen till 2030-09-08 hindrar prövning mot ett utfall, inte läsning, och att visa vad
ett parti lovar är ingen prövning. En tom kolumn ber om att fyllas i.

---

## C. Handlingssidan

**14. Författarskap, med instrumentet efter positionen.** Opposition mäts på egna motioner och egen
budgetmotion. Regering mäts på regeringens propositioner och budgetproposition.

*Skäl:* strikt eget författarskap ger M, KD och L noll på budgetkanalen 2023 till 2025, eftersom
ingen av dem har en egen ram de åren. Att i stället räkna att löftet blev av, oavsett vem som skrev
pappret, låter regeringspartier uppfylla per konstruktion och gör att opposition inte kan uppfylla
något alls. Då mäter spåret makt och inte vilja. Två instrument efter position kräver ingen
justering i efterhand.

**15. En regeringsproposition bärs kollektivt av alla regeringspartier.**

*Skäl:* regeringsärenden avgörs av regeringen vid regeringssammanträde (RF 7 kap. 3 §), så ett
departement lägger ingen proposition för egen räkning.
[`config/budget_ramar.yaml`](../../../config/budget_ramar.yaml) gör redan så: M, KD och L bär alla
ramen `regeringen` med `basis: regeringsstallning`. Att i stället tillskriva ansvarigt statsråd
straffar det lilla regeringspartiet två gånger, först för få departement och sedan för få
propositioner, utan att någon källa belägger att partiet inte drev saken.

**16. Partiets eget papper är partimotion och kommittémotion. Enskild motion räknas aldrig.**

*Skäl:* en enskild motion är en ledamots papper och bär inget besked om partiets prioritering.
Talen är entydiga. Riksmötet 2023/24, fullständigt räknat ur data.riksdagen.se 2026-09-16: SD 571
motioner varav 175 kommittémotioner och 396 enskilda, M 613 varav **1** kommittémotion och 612
enskilda, S 800 varav 72 kommitté, 1 parti och 727 enskilda, V 124 varav 86 kommitté, 37 parti och
1 enskild. Räknas allt får V 124 träffar mot M:s 613, fast V lade 123 papper på partinivå och M
ett enda. Fältet `subtyp` i dokumentlistan bär skillnaden, och en följdmotion behöver ingen egen
regel eftersom den bär samma fält.

**Avvikelse:** detta skiljer sig från hur `a2` räknar i modellen i dag, där alla motioner ingår.
Om `a2` bär samma fel är en egen fråga för en egen biljett. Spåret drar inte modellen med sig.

**17. Ett stödparti mäts som opposition.** Den saknade budgetkanalen är en **lucka, aldrig en
nolla**, och en saknad kanal går aldrig in i nämnaren.

*Skäl:* SD bär varken `egen_ram` eller `regeringsstallning` 2023 till 2025, utan `votering`, det
fält ADR 0017 punkt 3 pekade ut som ett giltighetsfel. Men SD skriver egna motioner, 9 031 stycken
2011 till 2025. Att mäta SD som regering river gränsen mot uppslutning som beslut 14 satte. Att
lämna SD utanför tystar det tredje största motionsflödet i riksdagen.

**18. Tidöavtalet hör inte till handlingssidan.** Om det hör till löftessidan är en öppen fråga.

**19. Framlagt räknas, genomröstat räknas inte.** Nedröstad straffas aldrig.

**20. Budgeten läses som text, aldrig som ramtal.** Budgetmotionen och budgetpropositionen är
dokument som alla andra.

*Skäl:* att pröva ett löfte mot en ram kräver ett omdöme om hur mycket en höjning ska vara för att
svara mot löftet, alltså en magnitud, och beslut 24 avvisar magnitud. Ett löfte om ett starkare
försvar mot en ram som stiger 2 procent går inte att avgöra utan en gräns som ingen källa bär.
`budget_ramar.yaml` är dessutom modellens a1-kanal, bunden av flera ADR:er.

**Följd:** budgetåret 2026 ur bet. 2025/26:FiU1 **behövs inte** av spåret. Modellens a1 behöver det
fortfarande, men det är en annan biljett.

**21. Perioden är hela mandatperioden 2022 till 2026.**

*Skäl:* löftesdokumentet gäller en mandatperiod, så mätperioden ska vara samma period, annars mäter
täljaren och nämnaren olika saker. Kapas sista året faller bortfallet skevt åt ett håll, eftersom
ett sista år före ett val är när en regering levererar.

**22. Löften som inget riksdagspapper kan bära räknas bort ur nämnaren**, och antalet redovisas per
parti. Gränsen är snäv: löften till kommuner, regioner eller EU ligger **innanför**, eftersom
partiet kan väcka en motion om en lag, ett statsbidrag eller ett tillkännagivande i just den saken.
Utanför ligger bara löften om partiets eget arbete och löften som kräver att en annan stat handlar.

*Skäl:* tumme ned för dessa straffar partiet för att **vi** inte kan mäta. Samma regel som beslut
17. En vid gräns blir en nödutgång som används olika mellan partier. Mycket av det faller dessutom
redan på beslut 6: "Ukrainas sak är vår" är ett värdepåstående och når aldrig hit.

**23. Pappret hittas genom sökning från löftet, plus ett omvänt stickprov som mäter vad sökningen
missar.**

*Skäl:* en ren sökning på löftets egna ord hittar bara papper som talar manifestets språk, och då
mäts ordlikhet i stället för handling utan att det syns. Att läsa alla partiets papper är mest
fullständigt men dyrt, och det sätter kodaren framför löftet och pappret samtidigt, vilket bjuder
in till att få dem att passa ihop. Stickprovet sätter ett mätt tal på vad den billiga vägen missar.

**24. Tummen är binär.** Framlagt eller inte. Kopplingen mellan löfte och papper bär dokumentets id.

*Skäl:* "delvis" kräver ett omdöme om hur stor del av löftet pappret täcker, alltså en magnitud,
och projektet prövade och förkastade viktad magnitud 2026-06-07 på just det skälet: källan bär inte
omdömet. Att räkna antalet framläggningar smugglar in samma sak, eftersom fem motioner om samma
löfte inte är fem gånger mer arbete. Dokument-id gör att en läsare kan slå upp kopplingen och pröva
tummen själv.

**25. Uppfyllelsen kodas i två blinda genomgångar**, samma regim som beslut 7.

*Skäl:* beslut 23 lägger redan ett stickprov i botten. Läggs ett stickprov till ovanpå vilar hela
måttet på två skattningar ur två olika urval, och då går osäkerheten inte att uttrycka i en mening
en läsare förstår. En ensam kodare kan inte visa vad hen missade.

---

## D. Redovisning

**26. Talen räknas per parti och kategori**, i **absoluta tal**, aldrig som andel i datat. En cell
utan löften skriver "inget löfte", vilket är ett annat besked än noll av fem.

*Skäl:* absoluta tal är ärliga vid varje storlek och går att summera, så en hopslagning till ett
tal per parti är definierad när den frågan tas. Andelar räknas fram vid presentationen. Cellerna är
tunna: redan före gallringen fylls 60 celler av 64, minsta cellen bär 1 post, medianen 10, åtta
celler bär färre än 5, och V saknar fyra kategorier helt.

**27. Maktläget står som etikett per parti och år.** Ett partis regeringsår poolas aldrig med dess
oppositionsår i ett tal.

*Skäl:* etiketten är metodredovisning och ingen maktkorrigering. Beslut 14 ger två olika instrument,
och utan etiketten kan en läsare inte se att två tal kommer ur olika mätningar. Det är samma sak
som `basis`-fältet i budgetramarna. En justering mot förväntad uppfyllelse vore däremot en
maktkorrigering i efterhand, och den skulle kräva en förväntad grad som ingen svensk källa bär.

**28. Antalet konkreta förslag publiceras per parti**, som upplysning om nämnaren. Partier
rangordnas aldrig efter det, och meningen om vad talet inte säger står intill varje gång.

*Skäl:* talet måste fram ändå, eftersom nämnaren skiljer sig mellan partier. Men det mäter
dokumentets form lika mycket som partiets vilja: C fick 328 poster och SD 68 för 2026 därför att C
skriver numrerade punkter och SD numrerade löften i ett kortare dokument, inte därför att C lovar
fem gånger mer. Ett parti kan dessutom lägga sina konkreta förslag i ett annat program.

**29. Datat ligger i två filer per årgång.** Ett **register**, en rad per löfte med lydelse,
sidnummer, parti, kategori, prövbar eller inte, utanför instrumentet eller inte. Ett **utfall**, en
rad per löfte med tumme och dokument-id. Celltalen räknas fram i kod till spårets egen utfil,
aldrig till `dist/`.

*Skäl:* registret låses medan utfallet växer under kodningens gång, så de kan inte ligga i samma
fil. Ett lagrat celltal kan glida isär från det det härleddes ur, och projektet skiljer redan på
transkriberade källvärden i `config/` och härledda tal i `pipeline/`.

**30. Spåret visas i en egen sektion på webbplatsen.** Sektionen bär sitt eget anspråk högst upp.
Designen är en egen biljett.

---

## E. Kvalitet

**31. Tre förhandsregistrerade prov.** Kodaröverensstämmelse på tummen, missgraden ur det omvända
stickprovet i beslut 23, och **korsprovet**.

Korsprovet går till så här. Ta ett slumpat urval löften och kör exakt samma sökning mot **ett annat
partis** papper. Hittas nästan lika mycket där läser sökningen ämne och inte författarskap.

*Skäl:* Samstämmighet klarade alla tre sina trösklar och mätte ändå fel sak. Profilavståndet
korrelerade 0,998 med retorikens egen koncentration. Trösklar som bara prövar hur talen fördelar
sig kan inte se var talen kommer ifrån. Korsprovet kan.

**32. Faller ett prov läggs spåret inte ned.** Talet publiceras inte, metoden lagas och körs om.
**Spärren:** varje omkörning får en egen förhandsregistrering med eget datum, ändringen mot den
förra skrivs ned i klartext, och den fällda körningen ligger kvar i arkivet.

*Skäl:* att frågan går att besvara är redan visat, Thomson med flera kodade löfte mot åtgärd i tolv
länder med Sverige bland dem. Proven prövar inte frågan utan **vår** sökning. Utan spärr blir "laga
och kör om" samma sak som att köra tills det passerar.

**33. Trösklarnas siffror sätts i förhandsregistreringen**, som skrivs innan en enda kodning görs.

---

## F. Bygget

**34. Ordningen:**

1. **Mappa alla åtta valmanifest 2022.** Hela registret, ingen pilot. Registerarbetet prövas alltså
   inte i liten skala först, vilket är priset för ordningen.
2. **Kategorilistan** ur 2022-registret plus korpusen, och **flödestestet på KD** från löfte till
   tumme. KD är ett regeringsparti, så det instrument som bär mest ny maskin prövas: propositioner
   hämtas inte av någon kod i projektet i dag, medan motioner redan hämtas för a2.

**Följd:** oppositionsinstrumentet och stödpartiets fall står oprövade fram till den stora
körningen.

---

## Vad som prövades och förkastades

Förslagen nedan ska inte läggas fram på nytt utan nytt underlag.

- **Strikt eget författarskap utan hänsyn till position.** Ger M, KD och L noll på budgetkanalen de
  år de styrde landet. Beslut 14.
- **Uppfyllelse mätt som att löftet blev av.** Mäter makt och inte vilja. Beslut 14.
- **Tillskrivning till ansvarigt statsråd.** Strider mot RF 7 kap. 3 § och straffar det lilla
  regeringspartiet två gånger. Beslut 15.
- **Storhetsprovet som prövbarhetskrav.** 2 löften av 1 073. Beslut 6.
- **Tre steg i stället för binär tumme, och räknade framläggningar.** Båda bär en magnitud.
  Beslut 24.
- **Budgeten läst som ramtal.** Samma magnitudproblem, och det drar in modellens a1. Beslut 20.
- **Justering mot förväntad uppfyllelse givet maktläge.** Maktkorrigering i efterhand utan källa.
  Beslut 27.
- **Nedläggning som utfall av ett fällt prov.** Fel inramning för det här spåret. Beslut 32.
- **Ett mått utan trösklar.** Ett mått som inte kan falla kan heller aldrig sägas ha hållit.
  Beslut 31.

## Uppskjutet med avsikt

- Kategorilistans innehåll (beslut 11).
- Trösklarnas siffror (beslut 33).
- Kodbokens gränsfall. Två regler ligger redan fast: ett papper får svara mot flera löften, och ett
  löfte får ha flera papper.
- Presentationen och designen (beslut 30).
- Om modellen ska utökas med nya kategorier (beslut 2).
- Om Tidöavtalet hör till löftessidan (beslut 18).
- Om `a2` bär samma fel som beslut 16 rättar i spåret.
