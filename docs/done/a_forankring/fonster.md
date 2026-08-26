# Förankringsfönstret för delpoäng A (ADR 0005 punkt 7)

> AUTOGENERERAD av `python -m pipeline.tools.a_forankring_transcribe --window`.
> Redigera aldrig för hand. Talen är utfallet av två gränser som skrevs FÖRE
> hämtningen, och de har inte rörts efteråt.

Fönstret blev **2011-2025**: a1-gränsen ger 2008, a2-gränsen ger 2011, och fönstret börjar vid den senare av dem.

## Gränserna

- **a1 förankring**: FiU1:s rambeslutstabell listar utgiftsområde 1-27.
- **a1 täljare** (ADR 0007 punkt 2): alla åtta partier har en citerbar ram som listar utgiftsområde 1-27; citerbar betyder egen budgetmotion, regeringsställning, eller uppslutning bakom en gemensam ram belagd med votering. Faller ut till **2011**.
- **a2**: alla åtta partier har minst en motion i varje utskott mappningen använder.

a1:s TÄLJARE mäts alltså över 2011-2025, och dess förankring över samma år (ADR 0007 punkt 1).

## År för år

| År | a1 förankring | a1 täljare | a2 | a2:s nollor |
| --- | --- | --- | --- | --- |
| 2008 | ja | nej: SD: ingen citerbar ram (ingen egen kolumn, ej regeringsparti, ingen rad i voteringen mot regeringens ['Ja']) | nej | SD:AU, SD:CU, SD:FiU, SD:FöU, SD:JuU, SD:KU, SD:KrU, SD:MJU, SD:NU, SD:SfU, SD:SkU, SD:SoU, SD:TU, SD:UU, SD:UbU |
| 2009 | ja | nej: SD: ingen citerbar ram (ingen egen kolumn, ej regeringsparti, ingen rad i voteringen mot regeringens ['Ja']) | nej | SD:AU, SD:CU, SD:FiU, SD:FöU, SD:JuU, SD:KU, SD:KrU, SD:MJU, SD:NU, SD:SfU, SD:SkU, SD:SoU, SD:TU, SD:UU, SD:UbU |
| 2010 | ja | nej: SD: ingen citerbar ram (ingen egen kolumn, ej regeringsparti, ingen rad i voteringen mot regeringens ['Ja']) | nej | SD:CU |
| 2011 | ja | ja | ja | - |
| 2012 | ja | ja | ja | - |
| 2013 | ja | ja | nej | L:FöU |
| 2014 | ja | ja | ja | - |
| 2015 | ja | ja | nej | V:SkU |
| 2016 | ja | ja | ja | - |
| 2017 | ja | ja | ja | - |
| 2018 | ja | ja | ja | - |
| 2019 | ja | ja | nej | MP:FiU |
| 2020 | ja | ja | nej | MP:FiU |
| 2021 | ja | ja | ja | - |
| 2022 | ja | ja | nej | L:KrU |
| 2023 | ja | ja | nej | L:FöU |
| 2024 | ja | ja | nej | L:AU, L:FöU |
| 2025 | ja | ja | ja | - |

## a1:s täljare: vem står bakom vilken ram

Attributionen är citerbar per parti (ADR 0007 punkt 2), aldrig gissad.
`egen_ram` = egen eller gemensam budgetmotion, `regeringsstallning` = partiet står
bakom propositionen, `votering` = partiet röstade som regeringen i rambeslutet.

| År | S | M | SD | C | V | KD | L | MP |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2008 | S<br>egen_ram | regeringen<br>regeringsstallning | - | regeringen<br>regeringsstallning | V<br>egen_ram | regeringen<br>regeringsstallning | regeringen<br>regeringsstallning | MP<br>egen_ram |
| 2009 | S<br>egen_ram | regeringen<br>regeringsstallning | - | regeringen<br>regeringsstallning | V<br>egen_ram | regeringen<br>regeringsstallning | regeringen<br>regeringsstallning | MP<br>egen_ram |
| 2010 | S<br>egen_ram | regeringen<br>regeringsstallning | - | regeringen<br>regeringsstallning | V<br>egen_ram | regeringen<br>regeringsstallning | regeringen<br>regeringsstallning | MP<br>egen_ram |
| 2011 | S_MP_V<br>egen_ram | regeringen<br>regeringsstallning | SD<br>egen_ram | regeringen<br>regeringsstallning | S_MP_V<br>egen_ram | regeringen<br>regeringsstallning | regeringen<br>regeringsstallning | S_MP_V<br>egen_ram |
| 2012 | S<br>egen_ram | regeringen<br>regeringsstallning | SD<br>egen_ram | regeringen<br>regeringsstallning | V<br>egen_ram | regeringen<br>regeringsstallning | regeringen<br>regeringsstallning | MP<br>egen_ram |
| 2013 | S<br>egen_ram | regeringen<br>regeringsstallning | SD<br>egen_ram | regeringen<br>regeringsstallning | V<br>egen_ram | regeringen<br>regeringsstallning | regeringen<br>regeringsstallning | MP<br>egen_ram |
| 2014 | S<br>egen_ram | regeringen<br>regeringsstallning | SD<br>egen_ram | regeringen<br>regeringsstallning | V<br>egen_ram | regeringen<br>regeringsstallning | regeringen<br>regeringsstallning | MP<br>egen_ram |
| 2015 | regeringen<br>regeringsstallning | M_C_L_KD<br>egen_ram | SD<br>egen_ram | M_C_L_KD<br>egen_ram | regeringen<br>votering | M_C_L_KD<br>egen_ram | M_C_L_KD<br>egen_ram | regeringen<br>regeringsstallning |
| 2016 | regeringen<br>regeringsstallning | M<br>egen_ram | SD<br>egen_ram | C<br>egen_ram | regeringen<br>votering | KD<br>egen_ram | L<br>egen_ram | regeringen<br>regeringsstallning |
| 2017 | regeringen<br>regeringsstallning | M<br>egen_ram | SD<br>egen_ram | C<br>egen_ram | regeringen<br>votering | KD<br>egen_ram | L<br>egen_ram | regeringen<br>regeringsstallning |
| 2018 | regeringen<br>regeringsstallning | M<br>egen_ram | SD<br>egen_ram | C<br>egen_ram | regeringen<br>votering | KD<br>egen_ram | L<br>egen_ram | regeringen<br>regeringsstallning |
| 2019 | regeringen<br>regeringsstallning | M<br>egen_ram | SD<br>egen_ram | C<br>egen_ram | regeringen<br>votering | KD<br>egen_ram | L<br>egen_ram | regeringen<br>regeringsstallning |
| 2020 | regeringen<br>regeringsstallning | M<br>egen_ram | SD<br>egen_ram | regeringen<br>votering | V<br>egen_ram | KD<br>egen_ram | regeringen<br>votering | regeringen<br>regeringsstallning |
| 2021 | regeringen<br>regeringsstallning | M<br>egen_ram | SD<br>egen_ram | regeringen<br>votering | V<br>egen_ram | KD<br>egen_ram | regeringen<br>votering | regeringen<br>regeringsstallning |
| 2022 | regeringen<br>regeringsstallning | M<br>egen_ram | SD<br>egen_ram | C<br>egen_ram | V<br>egen_ram | KD<br>egen_ram | L<br>egen_ram | regeringen<br>regeringsstallning |
| 2023 | S<br>egen_ram | regeringen<br>regeringsstallning | regeringen<br>votering | C<br>egen_ram | V<br>egen_ram | regeringen<br>regeringsstallning | regeringen<br>regeringsstallning | MP<br>egen_ram |
| 2024 | S<br>egen_ram | regeringen<br>regeringsstallning | regeringen<br>votering | C<br>egen_ram | V<br>egen_ram | regeringen<br>regeringsstallning | regeringen<br>regeringsstallning | MP<br>egen_ram |
| 2025 | S<br>egen_ram | regeringen<br>regeringsstallning | regeringen<br>votering | C<br>egen_ram | V<br>egen_ram | regeringen<br>regeringsstallning | regeringen<br>regeringsstallning | MP<br>egen_ram |

## Utgiftsområdenas namn per år

Namnen grindar inte (se verktygets modulkommentar). De står här för att en
omdöpning ska synas i efterhand.

| UO | 2008 | 2009 | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Rikets styrelse | Rikets styrelse | Rikets styrelse | Rikets styrelse | Rikets styrelse | Rikets styrelse | Rikets styrelse | Rikets styrelse | Rikets styrelse | Rikets styrelse | Rikets styrelse | Rikets styrelse | Rikets styrelse | Rikets styrelse | Rikets styrelse | Rikets styrelse | Rikets styrelse | Rikets styrelse |
| 2 | Samhällsekonomi och finansförvaltning | Samhällsekonomi och finansförvaltning | Samhällsekonomi och finansförvaltning | Samhällsekonomi och finansförvaltning | Samhällsekonomi och finansförvaltning | Samhällsekonomi och finansförvaltning | Samhällsekonomi och finansförvaltning | Samhällsekonomi och finansförvaltning | Samhällsekonomi och finansförvaltning | Samhällsekonomi och finansförvaltning | Samhällsekonomi och finansförvaltning | Samhällsekonomi och finansförvaltning | Samhällsekonomi och finansförvaltning | Samhällsekonomi och finansförvaltning | Samhällsekonomi och finansförvaltning | Samhällsekonomi och finansförvaltning | Samhällsekonomi och finansförvaltning | Samhällsekonomi och finansförvaltning |
| 3 | Skatt, tull och exekution | Skatt, tull och exekution | Skatt, tull och exekution | Skatt, tull och exekution | Skatt, tull och exekution | Skatt, tull och exekution | Skatt, tull och exekution | Skatt, tull och exekution | Skatt, tull och exekution | Skatt, tull och exekution | Skatt, tull och exekution | Skatt, tull och exekution | Skatt, tull och exekution | Skatt, tull och exekution | Skatt, tull och exekution | Skatt, tull och exekution | Skatt, tull och exekution | Skatt, tull och exekution |
| 4 | Rättsväsendet | Rättsväsendet | Rättsväsendet | Rättsväsendet | Rättsväsendet | Rättsväsendet | Rättsväsendet | Rättsväsendet | Rättsväsendet | Rättsväsendet | Rättsväsendet | Rättsväsendet | Rättsväsendet | Rättsväsendet | Rättsväsendet | Rättsväsendet | Rättsväsendet | Rättsväsendet |
| 5 | Internationell samverkan | Internationell samverkan | Internationell samverkan | Internationell samverkan | Internationell samverkan | Internationell samverkan | Internationell samverkan | Internationell samverkan | Internationell samverkan | Internationell samverkan | Internationell samverkan | Internationell samverkan | Internationell samverkan | Internationell samverkan | Internationell samverkan | Internationell samverkan | Internationell samverkan | Internationell samverkan |
| 6 | Försvar samt beredskap mot sårbarhet | Försvar och samhällets krisberedskap | Försvar och samhällets krisberedskap | Försvar och samhällets krisberedskap | Försvar och samhällets krisberedskap | Försvar och samhällets krisberedskap | Försvar och samhällets krisberedskap | Försvar och samhällets krisberedskap | Försvar och samhällets krisberedskap | Försvar och samhällets krisberedskap | Försvar och samhällets krisberedskap | Försvar och samhällets krisberedskap | Försvar och samhällets krisberedskap | Försvar och samhällets krisberedskap | Försvar och samhällets krisberedskap | Försvar och samhällets krisberedskap | Försvar och samhällets krisberedskap | Försvar och samhällets krisberedskap |
| 7 | Internationellt bistånd | Internationellt bistånd | Internationellt bistånd | Internationellt bistånd | Internationellt bistånd | Internationellt bistånd | Internationellt bistånd | Internationellt bistånd | Internationellt bistånd | Internationellt bistånd | Internationellt bistånd | Internationellt bistånd | Internationellt bistånd | Internationellt bistånd | Internationellt bistånd | Internationellt bistånd | Internationellt bistånd | Internationellt bistånd |
| 8 | Migration | Migration | Migration | Migration | Migration | Migration | Migration | Migration | Migration | Migration | Migration | Migration | Migration | Migration | Migration | Migration | Migration | Migration |
| 9 | Hälsovård, sjukvård och social omsorg | Hälsovård, sjukvård och social omsorg | Hälsovård, sjukvård och social omsorg | Hälsovård, sjukvård och social omsorg | Hälsovård, sjukvård och social omsorg | Hälsovård, sjukvård och social omsorg | Hälsovård, sjukvård och social omsorg | Hälsovård, sjukvård och social omsorg | Hälsovård, sjukvård och social omsorg | Hälsovård, sjukvård och social omsorg | Hälsovård, sjukvård och social omsorg | Hälsovård, sjukvård och social omsorg | Hälsovård, sjukvård och social omsorg | Hälsovård, sjukvård och social omsorg | Hälsovård, sjukvård och social omsorg | Hälsovård, sjukvård och social omsorg | Hälsovård, sjukvård och social omsorg | Hälsovård, sjukvård och social omsorg |
| 10 | Ekonomisk trygghet vid sjukdom och handikapp | Ekonomisk trygghet vid sjukdom och handikapp | Ekonomisk trygghet vid sjukdom och handikapp | Ekonomisk trygghet vid sjukdom och handikapp | Ekonomisk trygghet vid sjukdom och handikapp | Ekonomisk trygghet vid sjukdom och funktionsnedsättning | Ekonomisk trygghet vid sjukdom och | Ekonomisk trygghet vid sjukdom och funktionsnedsättning | Ekonomisk trygghet vid sjukdom och funktionsnedsättning | Ekonomisk trygghet vid sjukdom och funktionsnedsättning | Ekonomisk trygghet vid sjukdom och funktionsnedsättning | Ekonomisk trygghet vid sjukdom och funktionsnedsättning | Ekonomisk trygghet vid sjukdom och funktionsnedsättning | Ekonomisk trygghet vid sjukdom och funktionsnedsättning | Ekonomisk trygghet vid sjukdom och funktionsnedsättning | Ekonomisk trygghet vid sjukdom och funktionsnedsättning | Ekonomisk trygghet vid sjukdom och funktionsnedsättning | Ekonomisk trygghet vid sjukdom och funktionsnedsättning |
| 11 | Ekonomisk trygghet vid ålderdom | Ekonomisk trygghet vid ålderdom | Ekonomisk trygghet vid ålderdom | Ekonomisk trygghet vid ålderdom | Ekonomisk trygghet vid ålderdom | Ekonomisk trygghet vid ålderdom | Ekonomisk trygghet vid ålderdom | Ekonomisk trygghet vid ålderdom | Ekonomisk trygghet vid ålderdom | Ekonomisk trygghet vid ålderdom | Ekonomisk trygghet vid ålderdom | Ekonomisk trygghet vid ålderdom | Ekonomisk trygghet vid ålderdom | Ekonomisk trygghet vid ålderdom | Ekonomisk trygghet vid ålderdom | Ekonomisk trygghet vid ålderdom | Ekonomisk trygghet vid ålderdom | Ekonomisk trygghet vid ålderdom |
| 12 | Ekonomisk trygghet för familjer och barn | Ekonomisk trygghet för familjer och barn | Ekonomisk trygghet för familjer och barn | Ekonomisk trygghet för familjer och barn | Ekonomisk trygghet för familjer och barn | Ekonomisk trygghet för familjer och barn | Ekonomisk trygghet för familjer och barn | Ekonomisk trygghet för familjer och barn | Ekonomisk trygghet för familjer och barn | Ekonomisk trygghet för familjer och barn | Ekonomisk trygghet för familjer och barn | Ekonomisk trygghet för familjer och barn | Ekonomisk trygghet för familjer och barn | Ekonomisk trygghet för familjer och barn | Ekonomisk trygghet för familjer och barn | Ekonomisk trygghet för familjer och barn | Ekonomisk trygghet för familjer och barn | Ekonomisk trygghet för familjer och barn |
| 13 | Arbetsmarknad | Integration och jämställdhet | Integration och jämställdhet | Integration och jämställdhet | Integration och jämställdhet | Integration och jämställdhet | Integration och jämställdhet | Integration och jämställdhet | Jämställdhet och nyanlända invandrares etablering | Jämställdhet och nyanlända invandrares etablering | Jämställdhet och nyanlända invandrares etablering | Jämställdhet och nyanlända invandrares etablering | Jämställdhet och nyanlända invandrares etablering | Jämställdhet och nyanlända invandrares etablering | Jämställdhet och nyanlända invandrares etablering | Jämställdhet och nyanlända invandrares etablering | Integration och jämställdhet | Integration och jämställdhet |
| 14 | Arbetsliv | Arbetsmarknad och arbetsliv | Arbetsmarknad och arbetsliv | Arbetsmarknad och arbetsliv | Arbetsmarknad och arbetsliv | Arbetsmarknad och arbetsliv | Arbetsmarknad och arbetsliv | Arbetsmarknad och arbetsliv | Arbetsmarknad och arbetsliv | Arbetsmarknad och arbetsliv | Arbetsmarknad och arbetsliv | Arbetsmarknad och arbetsliv | Arbetsmarknad och arbetsliv | Arbetsmarknad och arbetsliv | Arbetsmarknad och arbetsliv | Arbetsmarknad och arbetsliv | Arbetsmarknad och arbetsliv | Arbetsmarknad och arbetsliv |
| 15 | Studiestöd | Studiestöd | Studiestöd | Studiestöd | Studiestöd | Studiestöd | Studiestöd | Studiestöd | Studiestöd | Studiestöd | Studiestöd | Studiestöd | Studiestöd | Studiestöd | Studiestöd | Studiestöd | Studiestöd | Studiestöd |
| 16 | Utbildning och universitetsforskning | Utbildning och universitetsforskning | Utbildning och universitetsforskning | Utbildning och universitetsforskning | Utbildning och universitetsforskning | Utbildning och universitetsforskning | Utbildning och universitetsforskning | Utbildning och universitetsforskning | Utbildning och universitetsforskning | Utbildning och universitetsforskning | Utbildning och universitetsforskning | Utbildning och universitetsforskning | Utbildning och universitetsforskning | Utbildning och universitetsforskning | Utbildning och universitetsforskning | Utbildning och universitetsforskning | Utbildning och universitetsforskning | Utbildning och universitetsforskning |
| 17 | Kultur, medier, trossamfund och fritid | Kultur, medier, trossamfund och fritid | Kultur, medier, trossamfund och fritid | Kultur, medier, trossamfund och fritid | Kultur, medier, trossamfund och fritid | Kultur, medier, trossamfund och fritid | Kultur, medier, trossamfund och fritid | Kultur, medier, trossamfund och fritid | Kultur, medier, trossamfund och fritid | Kultur, medier, trossamfund och fritid | Kultur, medier, trossamfund och fritid | Kultur, medier, trossamfund och fritid | Kultur, medier, trossamfund och fritid | Kultur, medier, trossamfund och fritid | Kultur, medier, trossamfund och fritid | Kultur, medier, trossamfund och fritid | Kultur, medier, trossamfund och fritid | Kultur, medier, trossamfund och fritid |
| 18 | Samhällsplanering, bostadsförsörjning, byggande | Samhällsplanering, bostadsförsörjning, byggande samt konsumentpolitik | Samhällsplanering, bostadsförsörjning m.m. | Samhällsplanering, bostadsförsörjning, byggande samt konsumentpolitik | Samhällsplanering, bostadsförsörjning, byggande samt konsumentpolitik | Samhällsplanering, bostadsförsörjning och byggande samt konsumentpolitik | Samhällsplanering, bostadsförsörjning | Samhällsplanering, bostadsförsörjning och byggande samt konsumentpolitik | Samhällsplanering, bostadsförsörjning och byggande samt konsumentpolitik | Samhällsplanering, bostadsförsörjning och byggande samt konsumentpolitik | Samhällsplanering, bostadsförsörjning och byggande samt | Samhällsplanering, bostadsförsörjning och byggande samt | Samhällsplanering, bostadsförsörjning och byggande samt konsumentpolitik | Samhällsplanering, bostadsförsörjning och byggande samt konsumentpolitik | Samhällsplanering, bostadsförsörjning och byggande samt konsumentpolitik | Samhällsplanering, bostadsförsörjning och byggande samt konsumentpolitik | Samhällsplanering, bostadsförsörjning och byggande samt konsumentpolitik | Samhällsplanering, bostadsförsörjning och byggande samt konsumentpolitik |
| 19 | Regional utveckling | Regional tillväxt | Regional tillväxt | Regional tillväxt | Regional tillväxt | Regional tillväxt | Regional tillväxt | Regional tillväxt | Regional tillväxt | Regional tillväxt | Regional tillväxt | Regional tillväxt | Regional tillväxt | Regional utveckling | Regional utveckling | Regional utveckling | Regional utveckling | Regional utveckling |
| 20 | Allmän miljö- och naturvård | Allmän miljö- och naturvård | Allmän miljö- och naturvård | Allmän miljö- och naturvård | Allmän miljö- och naturvård | Allmän miljö- och naturvård | Allmän miljö- och naturvård | Allmän miljö- och naturvård | Allmän miljö- och naturvård | Allmän miljö- och naturvård | Allmän miljö- och naturvård | Allmän miljö- och naturvård | Allmän miljö- och naturvård | Allmän miljö- och naturvård | Allmän miljö- och naturvård | Allmän miljö- och naturvård | Klimat, miljö och natur | Klimat, miljö och natur |
| 21 | Energi | Energi | Energi | Energi | Energi | Energi | Energi | Energi | Energi | Energi | Energi | Energi | Energi | Energi | Energi | Energi | Energi | Energi |
| 22 | Kommunikationer | Kommunikationer | Kommunikationer | Kommunikationer | Kommunikationer | Kommunikationer | Kommunikationer | Kommunikationer | Kommunikationer | Kommunikationer | Kommunikationer | Kommunikationer | Kommunikationer | Kommunikationer | Kommunikationer | Kommunikationer | Kommunikationer | Kommunikationer |
| 23 | Jord- och skogsbruk, fiske med anslutande näring | Jord- och skogsbruk, fiske med anslutande näringar | Areella näringar, landsbygd och livsmedel | Areella näringar, landsbygd och livsmedel | Areella näringar, landsbygd och livsmedel | Areella näringar, landsbygd och livsmedel | Areella näringar, landsbygd och livs- | Areella näringar, landsbygd och livsmedel | Areella näringar, landsbygd och livsmedel | Areella näringar, landsbygd och livsmedel | Areella näringar, landsbygd och livsmedel | Areella näringar, landsbygd och livsmedel | Areella näringar, landsbygd och livsmedel | Areella näringar, landsbygd och livsmedel | Areella näringar, landsbygd och livsmedel | Areella näringar, landsbygd och livsmedel | Areella näringar, landsbygd och livsmedel | Areella näringar, landsbygd och livsmedel |
| 24 | Näringsliv | Näringsliv | Näringsliv | Näringsliv | Näringsliv | Näringsliv | Näringsliv | Näringsliv | Näringsliv | Näringsliv | Näringsliv | Näringsliv | Näringsliv | Näringsliv | Näringsliv | Näringsliv | Näringsliv | Näringsliv |
| 25 | Allmänna bidrag till kommuner | Allmänna bidrag till kommuner | Allmänna bidrag till kommuner | Allmänna bidrag till kommuner | Allmänna bidrag till kommuner | Allmänna bidrag till kommuner | Allmänna bidrag till kommuner | Allmänna bidrag till kommuner | Allmänna bidrag till kommuner | Allmänna bidrag till kommuner | Allmänna bidrag till kommuner | Allmänna bidrag till kommuner | Allmänna bidrag till kommuner | Allmänna bidrag till kommuner | Allmänna bidrag till kommuner | Allmänna bidrag till kommuner | Allmänna bidrag till kommuner | Allmänna bidrag till kommuner |
| 26 | Statsskuldsräntor m.m. | Statsskuldsräntor m.m. | Statsskuldsräntor m.m. | Statsskuldsräntor m.m. | Statsskuldsräntor m.m. | Statsskuldsräntor m.m. | Statsskuldsräntor m.m. | Statsskuldsräntor m.m. | Statsskuldsräntor m.m. | Statsskuldsräntor m.m. | Statsskuldsräntor m.m. | Statsskuldsräntor m.m. | Statsskuldsräntor m.m. | Statsskuldsräntor m.m. | Statsskuldsräntor m.m. | Statsskuldsräntor m.m. | Statsskuldsräntor m.m. | Statsskuldsräntor m.m. |
| 27 | Avgiften till Europeiska gemenskapen | Avgiften till Europeiska gemenskapen | Avgiften till Europeiska gemenskapen | Avgiften till Europeiska unionen | Avgiften till Europeiska unionen | Avgiften till Europeiska unionen | Avgiften till Europeiska unionen | Avgiften till Europeiska unionen | Avgiften till Europeiska unionen | Avgiften till Europeiska unionen | Avgiften till Europeiska unionen | Avgiften till Europeiska unionen | Avgiften till Europeiska unionen | Avgiften till Europeiska unionen | Avgiften till Europeiska unionen | Avgiften till Europeiska unionen | Avgiften till Europeiska unionen | Avgiften till Europeiska unionen |

## Den beslutade ramen per budgetår

Vilken tabell som gäller läses ur betänkandet självt, aldrig av gissning.

| År | Vinnare | Tabell |
| --- | --- | --- |
| 2011 | utskottet | Förslag till utgiftsramar 2011 |
| 2012 | utskottet | Förslag till utgiftsramar 2012 |
| 2013 | utskottet | Förslag till utgiftsramar 2013 |
| 2014 | utskottet | Utskottets förslag till utgiftsramar 2014 |
| 2015 | reservationen | Reservanternas förslag till utgiftsramar för 2015 (M, C, FP, KD) |
| 2016 | utskottet | Utskottets förslag till utgiftsramar 2016 |
| 2017 | utskottet | Utskottets förslag till utgiftsramar 2017 |
| 2018 | utskottet | Utskottets förslag till utgiftsramar 2018 |
| 2019 | reservation 5 | Reservanternas förslag till utgiftsramar 2019 (M, KD) |
| 2020 | utskottet | Regeringens förslag till utgiftsramar 2020 |
| 2021 | utskottet | Regeringens förslag till utgiftsramar 2021 |
| 2022 | utskottet | Utskottets förslag till utgiftsramar 2022 |
| 2023 | utskottet | Regeringens förslag till utgiftsramar 2023 |
| 2024 | utskottet | Regeringens förslag till utgiftsramar 2024 |
| 2025 | utskottet | Regeringens förslag till utgiftsramar 2025 |
