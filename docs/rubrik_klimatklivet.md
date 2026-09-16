# Förregistrerad instrumentrubrik: `klimatinvesteringsstod_klimatklivet`

- Status: **FRUSEN** 2026-09-16, före svepet
- Biljett: [#50](https://github.com/mcknschn/rosta/issues/50)
- Bygger på: `docs/done/fas4c_rubrik.md` §1 till §4 och §6, samt
  [ADR 0001](adr/0001-a-mater-prioritering.md) och [ADR 0006](adr/0006-evidensgrinden-ar-symmetrisk.md)

## Varför rubriken är frusen först

Ordningsregeln i `docs/done/fas4c_rubrik.md` §5b kräver att verkan, `effect_strength` och
`evidence_level` låses **innan** partiraderna slås upp. Liggarposten uppfyllde det redan 2026-08-23.
Den här rubriken är motsvarigheten på ståndpunktssidan: **den skrivs och fryses innan någon slår upp
vad partierna tycker.**

Det biter särskilt här. Postens verkan är `negative`, alltså får ett parti som stödjer Klimatklivet
ett negativt led på `utslappsminskning_per_krona`. Rubriken avgör vad som räknas som stöd, och den
får inte formuleras efter att man sett vem den träffar.

**Loggat:** rubriken skrevs utan att någon sökning på partiernas ståndpunkter gjorts. Svepet sker
först efter att den här filen är committad.

## Instrumentet

**Klimatklivet**, alltså det statliga stödet till lokala och regionala klimatinvesteringar som
Naturvårdsverket fördelar till enskilda investeringar.

Avgränsningen är exakt den Riksrevisionen granskade i RiR 2019:1, eftersom det är den evidens posten
vilar på. Exakt författningshänvisning skrivs i `mapping_note` när en källa hittas, aldrig ur minnet.

## Vad som är en ståndpunkt

| stance | krav |
|---|---|
| `supports` | officiell svensk källa där partiet vill **behålla, förlänga eller bygga ut** Klimatklivet som instrument |
| `opposes` | officiell svensk källa där partiet vill **avveckla eller fasa ut** Klimatklivet |

## Vad som inte är en ståndpunkt

1. **Stöd för klimatinvesteringsstöd i allmänhet, eller för utsläppsminskning i allmänhet.** Inte
   instrumentexakt enligt §1. "Vi vill minska utsläppen" räcker inte, lika lite som det räcker för
   koldioxidskatten.

2. **En föreslagen anslagsnivå ensam.** Ett anslagsbelopp är en **omfattning**, och omfattning ägs av
   A ([ADR 0001](adr/0001-a-mater-prioritering.md)). Ett parti som vill ha ett mindre Klimatklivet
   vill fortfarande ha instrumentet. Endast avveckling eller utfasning är `opposes`.

   > **Känd följd, godtagen före frysningen.** Ett parti som vill skära ned Klimatklivet kraftigt
   > utan att avveckla det räknas som `supports` och får därmed det negativa ledet. Alternativet,
   > att räkna en nedskärning som `opposes`, skulle låta B mäta budgetmagnitud, och det är precis
   > den dubbelräkning ADR 0001 drog en gräns mot.

3. **Ett uttalande om Klimatklivets kostnadseffektivitet utan ställningstagande till om det ska
   finnas.** Evidensen **handlar** om kostnadseffektivitet, så ett parti som citerar RiR 2019:1
   kritiskt har inte därmed tagit ställning mot instrumentet.

## Källregler

**Hierarki** (§3): votering > parti-, kommitté- eller budgetmotion > valmanifest. Partiprogram endast
som kontext. Media, intresseorganisationer och internationella index är otillåtna.

**Regeringsproposition är ingen ståndpunktskälla.** Den tillskrivs regeringen, inte varje parti bakom
den. **Voteringen på betänkandet** är föredragen källa, eftersom partitillskrivningen där är direkt
och per parti.

**Bunten-regeln** (§2): en motion som buntar flera klimatinstrument räknas för Klimatklivet om citatet
namnger det. Nyansen skrivs i `mapping_note` och används **aldrig** som skäl att förkasta raden.

**Enskild motion** (§3): endast med `confidence: low`, och bara om ingen partikollektiv källa finns.
Saknas partikollektiv källa och den enskilda är svag, utelämnas raden.

**Tidsregel** (§4): föredra riksmötena 2022/23 till 2025/26. En äldre instrumentexakt källa får
användas med anteckning om att den ligger utanför perioden. Kravet är symmetriskt: ingen får strängare
tidskrav än någon annan.

## Utelämnande

Saknar ett parti instrumentexakt källa **utelämnas raden**. Det är en täckningslucka, aldrig `opposes`
(§6). Prejudikat: `uppsokande_forskoleerbjudande_nyanlandas_barn`, där SD och KD lämnades okodade
eftersom den tillgängliga källan inte var instrumentexakt.

## Om ingen är kodbar

Då är tystnaden **prövad och inte antagen**, vilket ADR 0006 punkt 5 kräver. En ny grund registreras
i taxonomin i `config/scoring.yaml` (`coverage_exclude_reasons`), med sökningen dokumenterad.

Det är den enda vägen till en grund för den här åtgärdstypen, eftersom varken **E1** (sidoeffekt-proxy,
faller på att bryggan är exakt) eller **E2** (inert per konstruktion, faller på att verkan är `negative`)
passar.
