# Ronde 9: opnieuw breed zoeken, van klein tot groot

Onderzoek voor Lucas, 15 november 2026. Vervolg op ronde7/ronde7.md en ronde8/ronde8.md. Alle bronnen hieronder zijn op 15-11-2026 geraadpleegd.

Labels: **[bron]** betekent dat het getal uit de genoemde bron komt. **[schatting]** betekent een eigen berekening of aanname. In tabellen geldt het label in de kolomkop voor de hele kolom.

## Samenvatting

* Er is opnieuw weinig echt nieuw aanbod. Na een volledige ronde langs bedrijfspand.com (alle typen, 31 plaatsen), ruim 1.700 nog niet bekeken oozo detailpagina's (ook in 15 randgemeenten), BAG controles en circa 40 zoekopdrachten naar funda in business blijven **11 nieuwe panden** over die op een tweede bron te koop staan. Daarvan zijn er **9 haalbaar** volgens de regel van Lucas (breed ≥ 1,2 × eigenaren die passen) [schatting].
* Zekerheid: **5 panden A** (actief te koop op bedrijfspand.com of als 'beschikbaar' op funda in business), **6 panden B** (brochure gevonden, status of datum onduidelijk). Panden die alleen op oozo staan (C) zijn niet opgenomen; dat waren er circa 30 [bron: zie sectie D].
* De BAG controle haalde ruim 40 leads weg omdat er woningen in hetzelfde pand zitten, waaronder een schoolgebouw van 1.563 m² in Rotterdam West met 18 woningen erboven [bron: BAG via PDOK].
* Beste per klasse [schatting]:
  * **Klein:** Kommiezenlaan 27 Schiedam (425 m², € 785.000, 0,3 km van Schiedam Centrum, breed circa 245).
  * **Middel:** A. Hofmanweg 2F Haarlem (510 m² kantoor, € 975.000, 8 eigen parkeerplaatsen, breed circa 194) en Dukdalfweg 55 Amsterdam Noord (600 m², € 895.000, breed circa 271).
  * **Groot:** Fokkerstraat 475 Schiedam (875 m², € 840.000, breed circa 231, maar oude advertentie), Edelhertstraat 12 Capelle aan den IJssel (662 m², € 995.000) en Van Riemsdijkweg 17 Rotterdam (717 m², 5,2 m, € 895.000).
* Geen enkel nieuw pand heeft 6,5 m vrije hoogte of meer. De tussenvloerregel speelt deze ronde dus geen rol.

## Werkwijze

* **bedrijfspand.com.** Voor 31 plaatsen (de vier grote steden, Schiedam, Rijswijk, Haarlem, Leiden, Delft, Dordrecht, Gouda, Zaandam, Hilversum, Amersfoort, Den Bosch, Breda, Tilburg, Eindhoven en 13 randgemeenten) is de koopzoekopdracht gedraaid voor alle typen (bedrijfsruimte, kantoor, winkel, horeca, zorg) van 250 tot 1.600 m². Dat gaf 145 advertenties, waarvan 50 niet in de lijst van ronde 7 stonden. 62 detailpagina's zijn gelezen [bron: https://www.bedrijfspand.com/plaats/<plaats>/].
* **oozo.nl als spoor.** Uit de wijklijsten van ronde 8 (21.107 advertenties) zijn alle bedrijfsruimte, maatschappelijk vastgoed, horeca en beleggingsobjecten van 280 tot 1.500 m² gehaald die nog niet waren geopend (1.003 pagina's, vooral 290 tot 420 m² voor de klasse klein). Daarnaast zijn 15 randgemeenten nieuw gelezen (Amstelveen, Ouder-Amstel, Capelle aan den IJssel, Krimpen, Barendrecht, Ridderkerk, Nieuwegein, Zoetermeer, Haarlemmermeer, Heemstede, Zwijndrecht, Stichtse Vecht, De Bilt, Zeist, Landsmeer): 4.223 advertenties, 682 detailpagina's [bron: https://www.oozo.nl/bedrijfspanden].
* **Tweede bron.** Elk overgebleven adres is gezocht via een zoekmachine. Funda en funda in business zijn niet zelf geopend; alleen zoekresultaten en daarin getoonde brochures zijn gebruikt. Makelaarssites en gemeentelijke vastgoedpagina's (onder meer rotterdam.nl, denhaag.nl, utrecht.nl, amsterdam.nl) zijn vanuit deze omgeving niet bereikbaar.
  * **A:** actief te koop op bedrijfspand.com (bijgewerkt 13 of 14-11-2026) of in een funda in business resultaat met status 'Beschikbaar'.
  * **B:** brochure of vermelding gevonden, maar zonder datum of met tegenstrijdige status.
  * **C:** alleen oozo. Niet in de hoofdlijst.
* **Woningen in het pand.** Per adres: PDOK Locatieserver, dan het verblijfsobject en het pand in de BAG OGC API, dan alle verblijfsobjecten in dat pand met hun gebruiksdoel. Een pand met 'woonfunctie' valt af. Panden met meerdere bedrijfsunits zijn gemarkeerd als unit in een complex (waarschijnlijk een VvE) [bron: https://api.pdok.nl/bzk/locatieserver/search/v3_1/free en https://api.pdok.nl/kadaster/bag/ogc/v2/collections].
* **Verzorgingsgebied.** Per pandadres berekend met exact de code en data van ronde 7 (CBS buurten 2024 en 2023 via PDOK, dezelfde trechter, kern, breed en breed met auto). Het dichtstbijzijnde centrum uit ronde7_wijken.json staat er ter vergelijking bij [schatting].
* **Capaciteit.** past(m2, hoogte) uit ronde7/screen.py (tot 100 eigenaren). Drempels in dit model: 30 eigenaren bij circa 354 m², 45 bij 450 m², 70 bij 579 m² en 100 bij 733 m² [schatting, bestaand model]. Klasse is toegekend op m² volgens de afspraak (klein 300 tot 450, middel 450 tot 650, groot 650 tot 1.100). Maandbijdrage: fee_run uit rij() in screen.py (volledig eigenaar inclusief btw bij die bezetting) [schatting, bestaand model].
* **Niet opnieuw gedaan:** biedboek.nl, Reliplan en Heritage Europe zijn in ronde 8 vandaag volledig gelezen zonder nieuw passend object. Een extra zoekopdracht naar gymzalen en kerken te koop in de focussteden gaf niets nieuws; de kerk aan de Kromme Nieuwegracht in Utrecht heeft een vergunning voor 9 appartementen en een praktijk [bron: https://www.duic.nl/algemeen/bijzonder-kerkgebouw-uit-1863-aan-de-kromme-nieuwegracht-in-utrecht-te-koop/, alleen zoekresultaat].

## A. Klein (30 tot 45 eigenaren, circa 300 tot 450 m²)

| Pand | Plaats | Zekerheid | Vraagprijs [bron] | m² totaal / hal / kantoor [bron] | Vrije hoogte [bron] | Bouwjaar [bron: BAG] | Woningen in pand [bron: BAG] | Unit in complex [bron: BAG] | Parkeren [bron] | Station (km) [schatting] | Kern / breed / auto adres [schatting] | Centrum ronde 7 (kern / breed / auto) [schatting] | Eigenaren past [schatting] | Breed ≥ 1,2 × eigenaren [schatting] | Maandbijdrage [schatting] |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [Kommiezenlaan 27](https://www.fundainbusiness.nl/bedrijfshal/schiedam/object-89282714-kommiezenlaan-27/) | Schiedam | A | € 785.000 k.k. | 425 / 335 / ca. 90 (wordt toegevoegd) | ca. 4,1 m | 1950 | nee | ja, 8 units | niet vermeld; perceel 3.334 m² | Schiedam Centrum 0,3 | 168 / 245 / 292 | Schiedam Centrum/Spaland (159 / 238 / 281) | 40 | 245 ≥ 48: ja | € 534 |
| [Spaarneweg 16E](https://fundainbusiness.nl/bedrijfshal/cruquius/object-89248700-spaarneweg-16-e/brochure/download) | Cruquius | B | € 695.000 k.k. | 415 / ca. 330 / ca. 85 | niet vermeld | 1985 | nee | nee | niet vermeld | Heemstede-Aerdenhout 3,4 | 126 / 168 / 197 | Haarlem Noord (144 / 195 / 220) | 35 | 168 ≥ 42: ja | € 608 |
| [Laan van Europa 360](https://www.bedrijfspand.com/bedrijfspanden/bedrijfsruimte/laan-van-europa-360-dordrecht/114492/) | Dordrecht | A | € 795.000 k.k. | 453 / 306 (2 lagen) / 147 | 3,73 m | 2023 | nee | ja, 10 units | 5 eigen + bezoekersplaatsen | Dordrecht Zuid 2,1 | 36 / 62 / 77 | Dordrecht Centrum/Staart (96 / 157 / 174) | 45 | 62 ≥ 54: ja, krap | € 416 |
| [Roelantdreef 24](https://www.bedrijfspand.com/bedrijfspanden/winkelruimte/roelantdreef-24-utrecht/117117/) | Utrecht | A | € 575.500 k.k. | 361 / geen hal (winkel 218 bg + 143 verdieping) | niet vermeld | 1969 | nee | ja, winkelcentrum | gratis in de omgeving | Utrecht Overvecht 1,0 | 130 / 205 / 226 | Utrecht Zuilen/Cartesiusweg (140 / 211 / 230) | 30 | 205 ≥ 36: ja | € 659 |

Status en bron per pand [bron]:
* Kommiezenlaan 27: funda in business toont het object als 'Beschikbaar', € 785.000 k.k.; overzichtspagina's noemen ook € 775.000 en € 739.000 (prijs mogelijk verlaagd). Er komt circa 90 m² kantoor op de verdieping en een nieuw dak [bron: zoekresultaat https://www.fundainbusiness.nl/bedrijfshal/schiedam/object-89282714-kommiezenlaan-27/].
* Spaarneweg 16E: brochure met vraagprijs € 695.000 k.k., ruim 400 m² op de begane grond, geen datum. oozo noemt het pand als huurobject (€ 3.250 per maand, units vanaf 310 m²) [bron: zoekresultaat brochure en https://www.oozo.nl/bedrijfspanden/haarlemmermeer/cruquius/cruquius/55863/bedrijfsruimte-spaarneweg-16-e-cruquius].
* Laan van Europa 360: bedrijfspand.com, online sinds 16-01-2026, bijgewerkt 13-11-2026, 2 eenheden beschikbaar, makelaar Van Vliet. Bestemming kantoor en bedrijf categorie 1 tot en met 3, minimaal 30 % kantoor [bron: bedrijfspand.com 114492].
* Roelantdreef 24: bedrijfspand.com, online sinds 23-03-2026, bijgewerkt 13-11-2026, makelaar Brecheisen. Bestemming 'Centrum' (detailhandel, dienstverlening) [bron: bedrijfspand.com 117117].

Duiding [schatting]:
1. **Kommiezenlaan 27, Schiedam:** beste kleine optie. Een hal pal naast station Schiedam Centrum in een gebied met kern circa 168. Nadelen: het is een unit in een oud complex van acht bedrijfsunits (VvE waarschijnlijk), 4,1 m hoog en het kantoor moet nog worden gebouwd.
2. **Spaarneweg 16E, Cruquius:** vrijstaand en gelijkvloers, betaalbaar, gebied Haarlem en Heemstede. Ligt op een bedrijventerrein zonder station op loopafstand; status eerst nabellen omdat oozo het als huur toont.
3. **Laan van Europa 360, Dordrecht:** nieuw en direct bruikbaar, maar 3,7 m hoog, in twee lagen en aan de rand van Dordrecht. Rond het adres zelf is breed maar circa 62; het centrum van Dordrecht scoort ruim twee keer zo hoog.
4. **Roelantdreef 24, Utrecht:** goedkoopste instap in Utrecht, maar een winkel in een passage zonder hal, met servicekosten en een centrumbestemming. Alleen voor de kleinste variant van circa 30 eigenaren.

## B. Middel (50 tot 70 eigenaren, circa 450 tot 650 m²)

| Pand | Plaats | Zekerheid | Vraagprijs [bron] | m² totaal / hal / kantoor [bron] | Vrije hoogte [bron] | Bouwjaar [bron: BAG] | Woningen in pand [bron: BAG] | Unit in complex [bron: BAG] | Parkeren [bron] | Station (km) [schatting] | Kern / breed / auto adres [schatting] | Centrum ronde 7 (kern / breed / auto) [schatting] | Eigenaren past [schatting] | Breed ≥ 1,2 × eigenaren [schatting] | Maandbijdrage [schatting] |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [A. Hofmanweg 2F](https://www.bedrijfspand.com/bedrijfspanden/kantoorruimte/a-hofmanweg-2-f-haarlem/119042/) | Haarlem | A | € 975.000 k.k. | 510 / geen hal / 510 (266 bg + 244 verdieping) | niet vermeld | 2000 | nee | nee | 8 eigen plaatsen | Haarlem Spaarnwoude 2,0 (advertentie: circa 1 km) | 140 / 194 / 233 | Haarlem Waarderpolder (143 / 192 / 228) | 60 | 194 ≥ 72: ja | € 308 |
| [Dukdalfweg 55](https://www.fundainbusiness.nl/en/bedrijfshal/amsterdam/object-43165490-dukdalfweg-55/brochure/download) | Amsterdam | B | € 895.000 k.k. | 600 / 375 / 225 | niet vermeld | 2020 | nee | ja, 8 units | 6 eigen + 6 gedeeld | Zaandam 2,4 (pont naar Zaandam) | 143 / 271 / 306 | Zaandam Oost (134 / 250 / 290) | 75 | 271 ≥ 90: ja | € 212 |

Status en bron per pand [bron]:
* A. Hofmanweg 2F: bedrijfspand.com, online sinds 06-05-2026, bijgewerkt 13-11-2026, te koop en te huur, leeg opgeleverd, makelaar FRIS [bron: bedrijfspand.com 119042].
* Dukdalfweg 55: brochure GA Makelaars, € 895.000 k.k., 600 m² (375 bedrijf, 225 kantoor), industrieterrein Zaansepoort; geen datum. oozo 'Beschikbaar' sinds 11-09-2025 [bron: zoekresultaat brochure en oozo].

Duiding [schatting]:
1. **A. Hofmanweg 2F, Haarlem:** vrijstaand, instapklaar, label A en acht eigen parkeerplaatsen in een gebied met kern circa 140. Het is een kantoor zonder hal; coworking, vergaderruimtes en café passen direct, de gym vraagt een sterke vloer en hoogte die er waarschijnlijk niet zijn.
2. **Dukdalfweg 55, Amsterdam Noord:** jonge unit met hal en kantoor voor circa € 1.490 per m², laag voor Amsterdam. past() geeft 75 eigenaren, dus op de grens met groot. Nadeel: Westelijk havengebied, ver van woonwijken in Amsterdam zelf; het gebied telt vooral via Zaandam (pont).

## C. Groot (80 tot 100 eigenaren, circa 650 tot 1.100 m²)

| Pand | Plaats | Zekerheid | Vraagprijs [bron] | m² totaal / hal / kantoor [bron] | Vrije hoogte [bron] | Bouwjaar [bron: BAG] | Woningen in pand [bron: BAG] | Unit in complex [bron: BAG] | Parkeren [bron] | Station (km) [schatting] | Kern / breed / auto adres [schatting] | Centrum ronde 7 (kern / breed / auto) [schatting] | Eigenaren past [schatting] | Breed ≥ 1,2 × eigenaren [schatting] | Maandbijdrage [schatting] |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [Fokkerstraat 475](https://www.fundainbusiness.nl/bedrijfshal/schiedam/object-43042602-fokkerstraat-475/brochure/download) | Schiedam | B | € 840.000 k.k. | 875 / 597 + entresol 113 / 165 | niet vermeld | 1992 | nee | nee | niet vermeld; perceel 1.082 m² | Schiedam Centrum 1,8 | 156 / 231 / 285 | Schiedam Centrum/Spaland (159 / 238 / 281) | 100 | 231 ≥ 120: ja | € 181 |
| [Edelhertstraat 12](https://www.fundainbusiness.nl/bedrijfshal/capelle-aan-den-ijssel/object-43216681-edelhertstraat-12/brochure/download) | Capelle aan den IJssel | B | € 995.000 k.k. | 662 / niet vermeld / niet vermeld | niet vermeld | 1974 | nee | nee | niet vermeld; perceel 1.044 m² | Rotterdam Stadion 3,3 (metro niet meegeteld) | 83 / 159 / 208 | Rotterdam Kralingen-Crooswijk (198 / 269 / 309) | 85 | 159 ≥ 102: ja | € 229 |
| [Van Riemsdijkweg 17](https://www.fundainbusiness.nl/bedrijfshal/rotterdam/object-44546024-van-riemsdijkweg-17/) | Rotterdam | B | € 895.000 k.k. | 717 / 404 + showroom 159 / 154 | 5,2 m | 1957 | nee | nee | openbaar voor de deur | Schiedam Centrum 5,3 (metro niet meegeteld) | 62 / 144 / 191 | Rotterdam West/Merwe-Vierhavens (171 / 252 / 296) | 95 | 144 ≥ 114: ja | € 183 |
| [Kapitein Rondairestraat 18](https://www.bedrijfspand.com/bedrijfspanden/bedrijfsruimte/kapitein-rondairestraat-18-tilburg/120469/) | Tilburg | A | € 695.000 k.k. | 682 / ca. 566 / 116 | 3,25 m | 1969 | nee | nee | gratis in de omgeving | Tilburg 2,1 | 61 / 83 / 97 | Tilburg Noord/Loven (65 / 86 / 98) | 90 | 83 < 108: nee | € 170 |
| [Hastelweg 248](https://www.bedrijfspand.com/bedrijfspanden/bedrijfsruimte/hastelweg-248-eindhoven/125413/) | Eindhoven | A | € 1.050.000 k.k. | 1.555 / 1.370 / 185 | niet vermeld | 1970 | nee | ja, 2 objecten | 3 eigen + parkeerhavens | Eindhoven Strijp-S 2,0 | 64 / 106 / 119 | Eindhoven Strijp (73 / 115 / 126) | 100 | 106 < 120: nee | € 306 |

Status en bron per pand [bron]:
* Fokkerstraat 475: brochure met € 840.000 k.k. (verlaagd van € 875.000), circa 597 m² bedrijfsruimte, 113 m² entresol en 165 m² kantoor, erfpacht tot 2091. Het objectnummer is oud en er is in 2024 bij de gemeente een garage-activiteit op dit adres gemeld; mogelijk is het pand dus in gebruik of al verkocht [bron: zoekresultaten brochure en https://zoek.officielebekendmakingen.nl].
* Edelhertstraat 12: brochure Parc Makelaars, € 995.000 k.k., circa 662 m², perceel 1.044 m² eigen grond met recht van overpad; oozo 'Beschikbaar' sinds 19-01-2026 [bron: zoekresultaat brochure en oozo].
* Van Riemsdijkweg 17: funda in business toont het object als beschikbaar, € 895.000 k.k., 717 m², 5,2 m, label A+, erfpacht met canon € 8.666,40 per jaar. In een zijbalk van dezelfde pagina staat ook 'Onder bod', daarom B [bron: zoekresultaat https://www.fundainbusiness.nl/bedrijfshal/rotterdam/object-44546024-van-riemsdijkweg-17/].
* Kapitein Rondairestraat 18: bedrijfspand.com, online sinds 11-06-2026, bijgewerkt 14-11-2026, makelaar Naber [bron: bedrijfspand.com 120469].
* Hastelweg 248: bedrijfspand.com, online sinds 15-10-2026, bijgewerkt 13-11-2026, per direct, makelaar Q Bedrijfslocaties [bron: bedrijfspand.com 125413].

Duiding [schatting]:
1. **Fokkerstraat 475, Schiedam:** op papier de beste groot-kandidaat: 875 m² met entresol voor circa € 960 per m², sterk gebied (breed circa 231) en 1,8 km van Schiedam Centrum. De advertentie is oud; eerst bellen of het nog te koop en leeg te leveren is.
2. **Edelhertstraat 12, Capelle aan den IJssel:** vrijstaand op eigen grond, ruim genoeg voor 85 eigenaren. Rond het adres is de kern circa 83 (de metro naar Rotterdam telt in deze methode niet mee), breed circa 159.
3. **Van Riemsdijkweg 17, Rotterdam:** goedkoop voor 717 m² met een hal van 5,2 m, maar in het Waalhavengebied ver van treinstations; de kern rond het adres is circa 62, breed circa 144 (haalt 95 eigenaren nog).
4. **Kapitein Rondairestraat 18, Tilburg** en **Hastelweg 248, Eindhoven:** actief te koop en zonder woningen, maar het verzorgingsgebied haalt de regel van Lucas niet voor de capaciteit van het gebouw. Alleen bruikbaar als middel club die een deel van de hal verhuurt.

## D. Afgevallen leads

### Woningen in hetzelfde pand [bron: BAG via PDOK]

| Adres | m² | Prijs | BAG |
|---|---|---|---|
| Zoutziedersstraat 18-20, Rotterdam | 1.421 | inschrijving | school 1926 met 18 woningen in het pand |
| Coolhaven 50, Rotterdam | 356 | € 1.095.000 | pand met 29 woningen |
| Admiraal de Ruyterweg 44a, Rotterdam | 312 | op aanvraag | 7 woningen |
| Rosenveldtstraat 87-95, Rotterdam | 361 | op aanvraag | woning in beide panden |
| Willem de Zwijgerstraat 2, Rotterdam | 400 | op aanvraag | 5 woningen |
| Kleiweg 205A, Rotterdam | 691 | € 1.000.000 | woning in pand; bestemming sluit sportschool uit |
| Pleinweg 136A, Rotterdam | 327 | € 575.000 | 6 woningen |
| Frederiklaan 5, Rijswijk | 319 | € 750.000 | 5 woningen |
| Neherkade 2262, Den Haag | 308 | € 575.000 | complex met 112 woningen |
| Bezuidenhoutseweg 211, Den Haag | 314 | op aanvraag | 3 woningen |
| Jacob Catskade 45H, Amsterdam | 326 | op aanvraag | 4 woningen |
| Burgemeester Röellstraat 24-26, Amsterdam | 381 | € 750.000 | 48 woningen |
| Cruquiusweg 96B, Amsterdam | 327 | € 750.000 | 4 woningen in complex |
| Nicolaas Beetsstraat 82, Amsterdam | 626 | € 1.500.000 | 73 woningen |
| Sloterweg 1206, Amsterdam (religieus) | 317 | inschrijving | pand met woonfunctie; bovendien te klein |
| Molukkenstraat 22A en Mollerusweg 26, Haarlem | 330 en 300 | € 1.095.000 en € 550.000 | 4 en 2 woningen |
| Buitenwatersloot 207, Delft | 303 | op aanvraag | woonfunctie |
| Biltstraat 333, Utrecht | 520 | op aanvraag | 20 woningen; ook volledig verhuurd |
| Admiraal Helfrichlaan 30-40, Utrecht | 1.009 | € 875.000 | VvE met woningen; verhuurd tot eind 2033 |
| Kuiperij 5, Amstelveen | 800 | op aanvraag | 2 woningen; vooral huur |
| Goirkestraat 79, Boerhaavestraat 40, Offenbachstraat 161 en Rielseweg 810, Tilburg | 334 tot 655 | op aanvraag | woonfunctie in pand |
| Goirkekanaaldijk 2a en Nicolaas Pieckstraat 12, Tilburg | 312 en 383 | € 1.050.000 en € 600.000 | woonhuis met bedrijfsruimte (advertentie) |
| Admiraal Lucashof 15, Schiedam | 300 | € 640.000 | bovenwoning (advertentie) |
| Roskam 2 en Oude Baan 66, Breda | 300 | € 750.000 en € 635.000 | woonfunctie |
| Maria Montessorilaan 1N en Voorstraat 220, Dordrecht | 323 en 797 | € 895.000 en op aanvraag | 53 woningen en 1 woning |
| Korvetstraat 1 en Oude Vlijmenseweg 178, Den Bosch | 293 en 300 | € 635.000 en € 895.000 | woonfunctie |
| Groest 138, Hilversum | 338 | op aanvraag | woonfunctie |
| Nijverheidswerf 35, Bussum | 403 | € 449.500 | complex met woning; verhuurd tot eind 2027 |
| Korte Schaft 23A, Houten | 390 | € 895.000 | complex met 4 woningen |
| Industrieweg 2, Nieuwegein | 574 | € 875.000 | woonfunctie |
| Burgemeester de Withstraat 2 en Herenweg 27, De Bilt | 516 en 483 | € 950.000 en € 1.175.000 | woonfunctie |
| Hoofdweg 774, Hoofddorp | 800 | op aanvraag | woonfunctie in pand |
| Willemstraat 182, Ridderkerk; Korenmolen 1, Krimpen; Dorpsstraat 11, Landsmeer | 419 tot 630 | diverse | woonfunctie |
| Zwaaikom 8-10 en Hogeweg 249, Amersfoort; Bijleveldweg 7a, Vleuten; Ginnekenweg 93, Breda | 578 tot 1.250 | diverse | woonfunctie |

Ook afgevallen op woningen volgens de advertentie: Dijkmeerlaan 4 Amsterdam (zorgunit in nieuwbouwcomplex The Starling, Bajeskwartier; bestemming alleen zorg) [bron: bedrijfspand.com 114764].

### Verkocht, uitgesteld of niet te koop [bron: zoekresultaten en advertenties]

* Radonstraat 299 Zoetermeer (991 m², € 1.350.000): verkocht op 08-04-2026 volgens funda in business.
* Gantelstraat 25 Rotterdam (956 m², € 1.375.000): verkocht onder voorbehoud, verkoopdatum 25-09-2025.
* Van Beverenstraat 40 Schiedam (bijeenkomstfunctie 432 m², 1935, geen woningen): in januari 2025 vergunning aangevraagd voor een kinderdagverblijf; waarschijnlijk verkocht.
* D.J. den Hartoglaan 5 Diemen (politiebureau 921 m²): 'de verkoop is tot nader orde uitgesteld' [bron: bedrijfspand.com 120197].
* Kleverlaan 9 Haarlem (Kweekcafé): overname van een huurbedrijf, geen pandverkoop [bron: bedrijfspand.com 120228].
* De Stuwdam 22 Amersfoort: deel van een verhuurd verzamelgebouw van 3.676 m² [bron: bedrijfspand.com 126583].
* Minervum 7368 Breda (kantoor 1.118 m²): alleen kantoorgebruik toegestaan en Breda breed circa 80.
* Donk 7a Barendrecht: brochure noemt circa 326 m² plus 59 m² entresol voor € 1.450.000; te duur voor de klasse klein.

### Te klein (onder circa 330 m²) [bron: advertenties en BAG]

Wateringweg 63 Haarlem (308 m²), Cyclotronweg 27 Delft (310), Flevoweg 39F Leiden (300), Tienlingstraat 10 Zaandam (308), Kombuisweg 25 Amsterdam (305), Nijverheidslaan 36 Weesp (315), Alleenhouderstraat 159 Tilburg (314), Huisbergenweg 10 Rosmalen (325), Laan van Waalhaven 128 Den Haag (296, 3 m hoog), Dekkershoek 23 en 63 Den Haag (211 en 295), Zestienhovensekade 174 Rotterdam (units tot 297), Wieldrechtseweg 52 Dordrecht (306).

### Verzorgingsgebied te dun voor de capaciteit [schatting]

* Ridderkerk Nikkelstraat, Wagenmakerstraat, Rietdekkerstraat en Houtstraat (breed circa 75 tot 87 bij 75 tot 100 eigenaren).
* Nieuwegein Drenthehaven 10, 14, 20 en 26, Montageweg 30, Kruyderlaan 3a, Mondriaanlaan 3-7 (breed circa 54 tot 90).
* Zwijndrecht Houtkopersstraat 10 en 20 (breed circa 85), Vijfhuizerdijk 21 Vijfhuizen (75), Leeuweriklaan 20 Zeist (100 bij 100 eigenaren), Jericholaan 6 Eindhoven (94).

### Alleen op oozo (C), geen tweede bron gevonden [bron: oozo, zoekresultaten zonder vermelding]

Geen woningen in het pand volgens BAG, wel een goed verzorgingsgebied, maar niet te bevestigen. Bellen kan, opnemen niet:
* Klein: Borgerstraat 112 Amsterdam (bijeenkomstfunctie 467 m², 1900, € 525.000, sinds 06-2023), Mgr. de Vetstraat 112 Breda (bijeenkomstfunctie 462 m², op aanvraag), Thurledeweg 73-75 Rotterdam, Pieter Braaijweg 65 Duivendrecht, Samsonweg 62 Wormerveer, Californiëdreef 15a Utrecht, Schepenbergweg 26 en Van Slingelandtplein 13B Amsterdam, Badhoevelaan 31 Badhoevedorp, Kombuisweg 11 Amsterdam (436 m², € 800.000), Westkanaaldijk 19H Maarssen.
* Middel: Jacob de Graeflaan 2 Amstelveen (532 m², € 1.000.000, breed circa 298), Swaneblakestraat 10 Rotterdam, Tingietersweg 38 Haarlem, Lagendijk 281 Ridderkerk, 1e Loswal 2a Hilversum, Graftermeerstraat 45 Hoofddorp, Industrieweg 6, Industrieweg 100 en Radonstraat 179 Zoetermeer, Limburghaven 2a Nieuwegein, Scheepsbouwersweg 9a Landsmeer, Weerenweg 2-4 Zwanenburg.
* Groot: H.J.E. Wenckebachweg 150A Duivendrecht (674 m², € 945.000, breed circa 316), Pieter Braaijweg 91 Duivendrecht (810 m², unit), Pieter Lieftinckweg 14 Zaandam (1.400 m², € 1.500.000), Databankweg 2 Amersfoort (1.324 m², € 1.475.000), Sloterweg 259 Badhoevedorp (horeca 1.400 m²), Tuinweg 6-10 Hoofddorp (836 m²), Abberdaan 2A Amsterdam, Venkelbaan 55 en Cypresbaan 2-6 Capelle aan den IJssel, Oosteinde 2 Barendrecht, Industrieweg 88, Goudstraat 36 en Platinastraat 108 Zoetermeer, Rembrandtlaan 33 en P.C. Staalweg 14 Bilthoven.
* De meeste staan al sinds 2022 tot 2024 online; ronde 8 liet zien dat zulke oozo advertenties meestal al verkocht of verhuurd zijn.

## Beperkingen

* Funda in business is alleen via zoekresultaten gebruikt. Brochures zonder datum kunnen oud zijn; daarom staan die panden op B.
* Makelaarssites en gemeentelijke vastgoedpagina's waren niet bereikbaar, dus de status is niet bij de makelaar zelf gecontroleerd. Bel voor elk pand eerst.
* De BAG geeft het gebruiksdoel per verblijfsobject. Een pand zonder woonfunctie kan nog wel aan woningen grenzen; voor de gym moet de geluidsisolatie ter plekke worden bekeken.
* 'Niet vermeld' betekent onbekend, niet afwezig. Vrije hoogte ontbreekt bij de meeste advertenties.
* Verzorgingsgebied: dezelfde aannames als ronde 7 (hemelsbreed, alleen treinstations, trechter uit werving_onderzoek.md 1.5). Metro en tram tellen niet mee, wat Capelle, Waalhaven en Schiedam onderschat [schatting].
* Bestemming: bij vrijwel alle panden is voor horeca, sport en coworking een omgevingsvergunning voor afwijken nodig [schatting].

## Bestanden

* kandidaten9.py: lijst K (tupelformaat van kandidaten6.py) en META per pand met klasse, zekerheid, woningen_in_pand, unit_in_complex, hal_m2, kantoor_m2, bouwjaar, parkeren, station_km, wijk, leden_kern, leden_breed, leden_breed_auto, centrum_*, eigenaren_past, haalbaar, gecontroleerd, status, bron_status en oordeel.

## Bronnen

* https://www.bedrijfspand.com (koopzoekopdrachten per plaats en detailpagina's, 15-11-2026)
* https://www.oozo.nl/bedrijfspanden (wijklijsten en detailpagina's, alleen als spoor)
* Zoekmachineresultaten van https://www.fundainbusiness.nl (URL per pand hierboven; de site zelf is niet geopend)
* https://api.pdok.nl/bzk/locatieserver/search/v3_1/free
* https://api.pdok.nl/kadaster/bag/ogc/v2/collections (verblijfsobject en pand)
* https://api.pdok.nl/cbs/wijken-en-buurten-2024/ogc/v1 en https://api.pdok.nl/cbs/wijken-en-buurten-2023/ogc/v1
* https://api.pdok.nl/prorail/spoorwegen/ogc/v1/collections/station/items
* https://zoek.officielebekendmakingen.nl (vergunning Van Beverenstraat 40, melding Fokkerstraat 475)
