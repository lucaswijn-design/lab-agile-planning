# Ronde 7: verzorgingsgebieden, nieuwe panden en herbeoordeling

Onderzoek voor Lucas, 15 november 2026. Vervolg op werving_onderzoek.md (hoofdstuk 1) en kandidaten6.py.

Labels: **[bron]** betekent dat het getal uit de genoemde bron komt. **[schatting]** betekent een eigen berekening of aanname, met de redenering erbij. In tabellen staat het label in de kolomkop en geldt het voor de hele kolom.

## Samenvatting

* De sterkste verzorgingsgebieden liggen in de Randstad: Amsterdam West, Noord en Oost, Den Haag Laakhaven/Moerwijk en Binckhorst, Rotterdam Zuid, Kralingen, Noord en West, Schiedam, Rijswijk en Utrecht West/Lombok. Zij halen met de methode van werving_onderzoek.md 1.5 elk 150 tot 270 haalbare eigenaar-leden in kern plus een halte [schatting, zie A].
* Amsterdam scoort het hoogst maar is per m² het duurst (mediaan vraagprijs koop bedrijfsruimte circa € 2.040 per m² op oozo, tegen circa € 1.335 in Utrecht en € 1.515 in Rotterdam) [schatting, steekproef oozo.nl 15-11-2026]. Den Haag Zuid, Rijswijk, Rotterdam en Schiedam combineren een groot verzorgingsgebied met hallen tussen circa € 750 en € 1.650 per m² [schatting, zelfde steekproef].
* Brabant blijft achter: Eindhoven Strijp circa 73, Tilburg circa 65, Breda circa 62 en Den Bosch circa 59 in kern plus een halte [schatting]. Met de bredere regel (tot 8 km fietsen, twee haltes) komen deze steden op circa 84 tot 115 [schatting].
* 25 nieuwe kandidaten zijn op 15-11-2026 op de advertentiepagina als beschikbaar gezien. De beste combinaties van verzorgingsgebied, grootte en prijs: Galvanistraat 122-126 Rotterdam/Schiedam, Zilverstraat 56 Den Haag, Limpergstraat 2 Rijswijk, Anthonetta Kuijlstraat 51B Rotterdam, Calandstraat 92 Schiedam, Westerdijk 18 Utrecht, Rooseveltstraat 54 Leiden en Heulweg 16 Rijswijk (goedkoop, maar 2 lagen).
* Herbeoordeling: Utrecht Van Heutszstraat blijft de beste basislocatie. Maarssen, Pernis en Den Bosch stijgen duidelijk met de bredere regel en worden 'behouden met voorwaarden'. Voorhout en Uden vallen af. Alle zeven basisadvertenties stonden op 15-11-2026 nog als beschikbaar.

## Methode

* Bevolking, leeftijd en woningwaarde: CBS Kerncijfers wijken en buurten 2024 via https://api.pdok.nl/cbs/wijken-en-buurten-2024/ogc/v1 (collectie buurten, 14.668 buurten) [bron]. Aandeel zelfstandigen en inkomen: editie 2023 via https://api.pdok.nl/cbs/wijken-en-buurten-2023/ogc/v1 [bron]. Het gemiddeld inkomen per inwoner is in de editie 2023 maar voor een deel van de buurten gevuld (buurten met circa 8,4 miljoen inwoners) [bron]; daarom staat ook het aandeel personen met een hoog inkomen erbij, dat bijna overal gevuld is [bron].
* Stations: ProRail stationsdataset via https://api.pdok.nl/prorail/spoorwegen/ogc/v1/collections/station/items (425 stations) [bron]. Welke stations intercitystation zijn, is een eigen lijst op basis van het NS lijnennet [schatting]; controleer in de NS Reisplanner.
* Straalmethode zoals in werving_onderzoek.md 1.2: alle buurten waarvan het zwaartepunt binnen de straal ligt [schatting]. Afstanden zijn hemelsbreed.
* Trechter zoals in werving_onderzoek.md 1.5, maar per buurt toegepast (lokale leeftijd en lokaal aandeel zelfstandigen): werkenden = 87,4 % van 25 tot 45 plus 75 % van 45 tot 65; profielpassend = zelfstandigen plus 26 % van de werknemers; daarvan 30 % financieel in staat, 1,5 % serieus geïnteresseerd en 40 % wordt lid [schatting, aannames uit 1.5].
* Vier niveaus [schatting]:
  * **Leden 4,5 km**: alleen de kern (gewicht 1). Dit is direct vergelijkbaar met de kolom 'eigenaar-leden uit kern' in 1.5.
  * **Kern**: 4,5 km plus buurten binnen 1,5 km van stations op een halte buiten 4,5 km, met halve belangstelling (zoals stap 7 in 1.5). 'Een halte' is benaderd als een station binnen 8 km van het eigen station (sprinter), of een intercitystation binnen 23 km van een intercitystation dat zelf binnen 3,5 km ligt.
  * **Breed** (nieuwe regel van Lucas, 30 tot 40 minuten deur tot deur): kern plus de ring 4,5 tot 8 km (circa 25 minuten e-bike) en buurten rond stations op twee haltes of een intercitysprong tot 35 km (circa 20 tot 25 minuten in de trein), alles met gewicht 0,5.
  * **Breed met auto**: breed plus de ring 8 tot 15 km (circa 20 minuten auto) met gewicht 0,25. Dit telt alleen bij een pand met eigen parkeerruimte voor een behoorlijk aantal auto's.
* Ter controle: voor Rietveldenweg 13 geeft deze code exact dezelfde 127.590 inwoners binnen 4,5 km als werving_onderzoek.md 1.2 [bron: zelfde CBS data]. Voor Utrecht Van Heutszstraat komt de kern uit op circa 107 tegen 104 eerder; de kern plus een halte is circa 150 tegen 125 eerder, omdat de nieuwe halte regel meer stations meetelt (onder meer Hilversum en Naarden-Bussum) [schatting]. Vergelijk dus binnen ronde 7, niet met de oude totalen.
* Voorbeeld van de trechter voor Utrecht West/Lombok binnen 4,5 km [schatting]: 158.273 werkenden, 24.388 zelfstandigen, 59.198 profielpassend, 17.759 financieel in staat, 266 serieus geïnteresseerd, circa 107 eigenaar-leden.

## A. Ranglijst verzorgingsgebieden

Centra zijn per wijk gekozen op een adres in of naast een oudere bedrijvenstrook die aan woonbuurten grenst (adres in ronde7_wijken.json, veld 'anker'). De volledige lijst van 34 centra staat in ronde7_wijken.json. Daarnaast is ter controle een grid van alle stations in Noord-Holland, Zuid-Holland, Utrecht en Noord-Brabant en een raster van 1,5 km in vijftien steden doorgerekend; dat bevestigt dezelfde volgorde (Amsterdam, Den Haag Zuid, Rotterdam centrum en Schiedam bovenaan) [schatting].

| # | Verzorgingsgebied | Inwoners 3 km [bron] | Inwoners 4,5 km [bron] | 25 tot 45 [bron] | 45 tot 65 [bron] | Zelfstandigen [bron] | Inkomen per inwoner x € 1.000 [bron] | Hoog inkomen [bron] | IC-station (km) [schatting] | Inwoners rond haltestations [bron] | Leden 4,5 km [schatting] | Kern [schatting] | Breed [schatting] | Breed met auto [schatting] | Vraagprijs per m² gemeente [schatting] |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Amsterdam West/Baarsjes-Sloterdijk | 330.740 | 552.845 | 39,8 % | 22,3 % | 21,7 % | 38,8 | 27,7 % | Amsterdam Lelylaan (1,9) | 319.675 | 215 | 267 | 375 | 401 | € 2.039 |
| 2 | Amsterdam Noord/Buiksloterham | 176.630 | 404.895 | 38,4 % | 23,8 % | 22,4 % | 36,9 | 26,3 % | Amsterdam Centraal (1,7) | 541.590 | 159 | 249 | 333 | 358 | € 2.039 |
| 3 | Den Haag Laakhaven/Moerwijk | 290.320 | 510.605 | 31,8 % | 25,0 % | 21,7 % | 30,5 | 20,1 % | Den Haag HS (0,9) | 431.145 | 180 | 247 | 299 | 321 | € 1.985 |
| 4 | Amsterdam Oost/Cruquius | 156.470 | 364.115 | 37,4 % | 23,2 % | 21,1 % | 38,8 | 27,8 % | Amsterdam Amstel (3,3) | 462.625 | 137 | 214 | 313 | 343 | € 2.039 |
| 5 | Den Haag Binckhorst | 251.835 | 411.085 | 32,4 % | 24,9 % | 21,7 % | 31,3 | 21,7 % | Den Haag Laan van NOI (0,9) | 403.635 | 146 | 209 | 280 | 307 | € 1.985 |
| 6 | Rotterdam Zuid/Katendrecht-Feijenoord | 229.835 | 424.020 | 34,9 % | 22,4 % | 17,4 % | 29,5 | 17,1 % | Rotterdam Blaak (1,9) | 420.885 | 140 | 207 | 266 | 307 | € 1.515 |
| 7 | Rotterdam Kralingen-Crooswijk | 171.865 | 414.770 | 33,7 % | 23,1 % | 17,1 % | 31,5 | 19,6 % | Rotterdam Blaak (1,7) | 389.745 | 135 | 198 | 269 | 309 | € 1.515 |
| 8 | Rotterdam Noord | 219.370 | 346.625 | 35,2 % | 22,4 % | 17,9 % | 33,1 | 21,9 % | Rotterdam Centraal (0,9) | 432.320 | 116 | 184 | 260 | 303 | € 1.515 |
| 9 | Rotterdam West/Merwe-Vierhavens | 151.130 | 286.295 | 37,3 % | 22,7 % | 17,7 % | 31,7 | 19,2 % | Schiedam Centrum (2,0) | 442.480 | 100 | 171 | 252 | 296 | € 1.515 |
| 10 | Schiedam Centrum/Spaland | 95.175 | 228.170 | 32,8 % | 24,1 % | 17,1 % | 29,3 | 17,8 % | Schiedam Centrum (1,5) | 523.285 | 74 | 159 | 238 | 281 | € 1.584 |
| 11 | Rijswijk Plaspoelpolder | 150.610 | 384.825 | 30,0 % | 24,9 % | 20,9 % | 26,9 | 17,8 % | Den Haag HS (3,8) | 151.370 | 129 | 153 | 220 | 261 | n.b. |
| 12 | Utrecht West/Lombok | 224.855 | 324.325 | 38,3 % | 20,5 % | 15,4 % | 35,3 | 26,9 % | Utrecht Centraal (0,8) | 292.775 | 107 | 150 | 216 | 234 | € 1.335 |
| 13 | Haarlem Noord | 133.610 | 193.430 | 27,6 % | 26,9 % | 20,1 % | 43,3 | 27,6 % | Haarlem (0,9) | 465.015 | 63 | 144 | 195 | 220 | € 1.702 |
| 14 | Haarlem Waarderpolder | 102.695 | 178.045 | 28,1 % | 27,1 % | 19,6 % | 42,7 | 27,1 % | Haarlem (1,9) | 487.270 | 58 | 143 | 192 | 228 | € 1.702 |
| 15 | Utrecht Zuilen/Cartesiusweg | 197.830 | 305.330 | 38,7 % | 20,5 % | 15,7 % | 35,6 | 27,5 % | Utrecht Centraal (1,9) | 257.575 | 102 | 140 | 211 | 230 | € 1.335 |
| 16 | Delft Schieoevers | 115.390 | 156.580 | 28,3 % | 23,5 % | 14,5 % | 33,3 | 22,8 % | Delft (1,0) | 583.045 | 44 | 140 | 202 | 274 | € 1.532 |
| 17 | Zaandam Oost | 72.590 | 105.065 | 28,0 % | 26,1 % | 18,0 % | 32,5 | 20,5 % | Zaandam (1,0) | 588.735 | 33 | 134 | 250 | 290 | € 1.399 |
| 18 | Utrecht Oost/Rotsoord | 161.485 | 275.930 | 38,8 % | 19,8 % | 15,1 % | 35,7 | 26,6 % | Utrecht Centraal (1,9) | 269.200 | 90 | 131 | 211 | 225 | € 1.335 |
| 19 | Weesp | 30.765 | 45.710 | 27,3 % | 25,2 % | 18,3 % | 34,0 | 27,0 % | Weesp (0,1) | 576.430 | 14 | 114 | 194 | 242 | € 2.039 |
| 20 | Leiden Morskwartier | 151.245 | 208.600 | 27,9 % | 24,2 % | 14,8 % | 34,4 | 25,0 % | Leiden Lammenschans (0,7) | 335.100 | 59 | 112 | 220 | 245 | € 1.632 |
| 21 | Leiden Zuidoost/Roomburg | 115.805 | 185.430 | 28,4 % | 24,1 % | 14,5 % | 32,7 | 23,4 % | Leiden Lammenschans (1,0) | 337.350 | 52 | 105 | 217 | 242 | € 1.632 |
| 22 | Hilversum Oost | 77.515 | 118.340 | 25,9 % | 27,0 % | 21,3 % | 34,8 | 26,0 % | Hilversum (0,8) | 390.350 | 38 | 102 | 185 | 207 | € 1.811 |

Ter vergelijking, lager in de lijst [schatting]: 
* Dordrecht Centrum/Staart: kern 96, breed 157, met auto 174 (leden 4,5 km 57).
* Gouda Kampenringweg: kern 91, breed 178, met auto 206 (leden 4,5 km 32).
* Amersfoort De Isselt/Soesterkwartier: kern 78, breed 122, met auto 132 (leden 4,5 km 46).
* Utrecht Overvecht/Lage Weide-rand: kern 76, breed 121, met auto 143 (leden 4,5 km 58).
* Eindhoven Strijp: kern 73, breed 115, met auto 126 (leden 4,5 km 66).
* Tilburg Spoorzone/Piushaven: kern 65, breed 85, met auto 97 (leden 4,5 km 48).
* Tilburg Noord/Loven: kern 65, breed 86, met auto 98 (leden 4,5 km 49).
* Breda Spoorzone/Belcrum: kern 62, breed 84, met auto 97 (leden 4,5 km 50).
* Den Bosch West/De Rietvelden: kern 59, breed 84, met auto 97 (leden 4,5 km 40).
* Rotterdam Noordwest/Spaanse Polder-rand: kern 58, breed 127, met auto 210 (leden 4,5 km 58).
* Helmond Centrum-Oost: kern 39, breed 70, met auto 90 (leden 4,5 km 27).
* Eindhoven Woensel/Hurk-rand: kern 27, breed 56, met auto 75 (leden 4,5 km 27).

Bronnen kolommen [bron]: CBS buurten 2024 en 2023 via PDOK (zie Methode). Leeftijd, zelfstandigen en inkomen zijn inwonergewogen gemiddelden binnen 4,5 km. Inkomen per inwoner alleen over buurten met een waarde. Vraagprijs per m²: mediaan van koopadvertenties 'Bedrijfsruimte' 200 tot 2.000 m² op https://www.oozo.nl/bedrijfspanden/<gemeente>, eerste 1.000 advertenties per gemeente, 15-11-2026 [schatting, kleine steekproef; Amsterdam n = 14].

Duiding [schatting]:
* **Amsterdam** (rang 1, 2 en 4) heeft het grootste verzorgingsgebied, maar de prijs per m² ligt circa 50 % boven Utrecht en hallen van 600 tot 1.000 m² onder € 1,4 miljoen zijn zeldzaam. Cruquiusweg 98 W (Oost) vraagt € 2.950.000 voor circa 820 m² [bron: https://www.bedrijfspand.com/bedrijfspanden/bedrijfsruimte/cruquiusweg-98-w-amsterdam/120445/]. Alleen haalbaar met een kleiner of meerlaags pand.
* **Den Haag Laakhaven/Moerwijk, Binckhorst en Rijswijk Plaspoelpolder** hebben veel inwoners, een hoog aandeel zelfstandigen (circa 21 tot 22 %) en relatief betaalbare bedrijfsstroken naast woonwijken. Het inkomen per inwoner ligt wel lager (circa € 27.000 tot € 31.000) dan in Utrecht of Haarlem [bron: CBS 2023], wat de inleg van € 9.000 tot € 15.000 lastiger maakt.
* **Rotterdam en Schiedam** combineren een groot gebied met de laagste prijzen per m² in de Randstad. Het aandeel hoge inkomens is lager (circa 17 tot 22 %) [bron: CBS 2023].
* **Utrecht West/Lombok, Zuilen en Oost** hebben de jongste bevolking (circa 38 tot 39 % 25 tot 45) en hoge inkomens (circa 26 tot 28 % hoog inkomen) [bron: CBS]. Kern circa 131 tot 150 [schatting].
* **Haarlem** heeft het hoogste inkomen per inwoner van de lijst (circa € 43.000) en veel zelfstandigen (circa 20 %) [bron: CBS 2023], maar een kleinere kern (circa 58 tot 66 leden binnen 4,5 km) [schatting]; de rest komt via de trein uit Amsterdam en Leiden.
* **Zaandam, Weesp, Delft, Hilversum en Gouda** scoren vooral door de halte naar een grote stad; hun eigen kern is 14 tot 44 leden [schatting]. Daar woont dus niet de meerderheid op fietsafstand.

## B. Nieuwe kandidaten (gecontroleerd 15-11-2026)

Bronnen: zoekpagina's per stad op bedrijfspand.com (alleen koop, 330 tot 1.350 m²), alle advertentielijsten op oozo.nl/bedrijfspanden voor 22 gemeenten (circa 12.000 advertenties gelezen, gefilterd op koop, 330 tot 1.350 m² en € 150.000 tot € 1.450.000), het volledige aanbod van biedboek.nl via de publieke data van de site, en een webzoekopdracht naar kerkgebouwen. Funda is niet gebruikt. Elke advertentie hieronder is op 15-11-2026 geopend en stond als 'Beschikbaar' (oozo) of 'eenheid beschikbaar' (bedrijfspand.com) [bron: URL in tabel]. Let op: oozo neemt aanbod over van makelaars; bij advertenties die al lang online staan kan de status achterlopen. Bel de makelaar voor een bezichtiging.

Capaciteit: het aantal eigenaren dat volgens past() uit kandidaten6.py in het pand past (maximaal 70 in die functie) [schatting, bestaand model]. Maandbijdrage: fee_run uit capaciteit.schaal() via rij() (maandbijdrage volledig eigenaar inclusief btw bij die bezetting) [schatting, bestaand model].

| Pand | Plaats | Vraagprijs [bron] | m² [bron] | € per m² [schatting] | Vrije hoogte [bron] | Bouwjaar [bron] | Type | Parkeren [bron] | Station (km) [schatting] | Verzorgingsgebied | Kern [schatting] | Breed / met auto [schatting] | Eigenaren passend [schatting] | Maandbijdrage [schatting] | Online sinds [bron] |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [Karel Roosstraat 22](https://www.oozo.nl/bedrijfspanden/s-gravenhage/regentessekwartier/rond-de-energiecentrale/36465/bedrijfsruimte-karel-roosstraat-22-den-haag) | Den Haag | € 645.000 | 458 | € 1.408 | 5,0 m | 1989 | hal | niet vermeld | Den Haag HS (2,2) | Den Haag Laakhaven/Moerwijk | 256 | 300 / 317 | 45 | € 446 | 05-12-2023 |
| [Teniersstraat 15](https://www.oozo.nl/bedrijfspanden/s-gravenhage/schildersbuurt/schildersbuurt-noord/55037/bedrijfsruimte-teniersstraat-15-den-haag) | Den Haag | € 795.000 | 393 | € 2.023 | niet vermeld | 1897 | werkplaats | niet vermeld | Den Haag HS (1,1) | Den Haag Laakhaven/Moerwijk | 251 | 300 / 321 | 35 | € 644 | 17-01-2025 |
| [Laboratoriumstraat 3](https://www.oozo.nl/bedrijfspanden/amsterdam/hoofddorppleinbuurt/bedrijventerrein-schinkel/72735/bedrijfsruimte-laboratoriumstraat-3-amsterdam) | Amsterdam | € 875.000 | 509 | € 1.719 | niet vermeld | 2000 | bedrijfsruimte meerlaags | niet vermeld | Amsterdam Lelylaan (1,7) | Amsterdam West/Baarsjes-Sloterdijk | 247 | 347 / 380 | 60 | € 345 | 17-03-2026 |
| [Jan Wapstraat 9-13](https://www.oozo.nl/bedrijfspanden/s-gravenhage/laakkwartier-en-spoorwijk/laakkwartier-west/75274/bedrijfsruimte-jan-wapstraat-9-13-den-haag) | Den Haag | € 825.000 | 409 | € 2.017 | niet vermeld | 1941 | werkplaats | niet vermeld (woonwijk, betaald/straatparkeren) | Den Haag Moerwijk (1,0) | Den Haag Laakhaven/Moerwijk | 237 | 295 / 321 | 35 | € 661 | 29-05-2026 |
| [Boekelostraat 9](https://www.oozo.nl/bedrijfspanden/s-gravenhage/morgenstond/morgenstond-zuid/63961/bedrijfsruimte-boekelostraat-9-den-haag) | Den Haag | € 575.000 | 380 | € 1.513 | 4,3 m | 1957 | hal | niet vermeld | Den Haag Moerwijk (2,0) | Den Haag Laakhaven/Moerwijk | 196 | 238 / 261 | 35 | € 566 | 30-07-2025 |
| [Limpergstraat 2](https://www.oozo.nl/bedrijfspanden/rijswijk/wijk-05/plaspoelpolder/35432/bedrijfsruimte-limpergstraat-2-rijswijk-zh) | Rijswijk | € 1.295.000 | 1.094 | € 1.184 | 5,3 m | 1985 | hal + kantoor | niet vermeld (perceel 786 m2, bijna volledig bebouwd) | Rijswijk (1,6) | Rijswijk Plaspoelpolder | 184 | 266 / 306 | 70 | € 470 | 27-11-2023 |
| [Heulweg 16](https://www.oozo.nl/bedrijfspanden/rijswijk/wijk-10/pasgeld/57207/bedrijfsruimte-heulweg-16-rijswijk-zh) | Rijswijk | € 395.000 | 502 | € 787 | niet vermeld | 1986 | hal + kantoor | niet vermeld | Rijswijk (1,5) | Rijswijk Plaspoelpolder | 175 | 256 / 304 | 60 | € 252 | 26-02-2025 |
| [Galvanistraat 122-126](https://www.oozo.nl/bedrijfspanden/rotterdam/nieuw-mathenesse/nieuw-mathenesse/63840/bedrijfsruimte-galvanistraat-122-126-rotterdam) | Rotterdam | € 1.125.000 | 696 | € 1.616 | 5,9 m | 2000 | hal + kantoor | niet vermeld | Schiedam Centrum (1,8) | Rotterdam West/Merwe-Vierhavens | 174 | 254 / 299 | 70 | € 353 | 22-05-2026 |
| [Anthonetta Kuijlstraat 51B](https://www.oozo.nl/bedrijfspanden/rotterdam/prins-alexander/prinsenland/51340/bedrijfsruimte-anthonetta-kuijlstraat-51b-rotterdam) | Rotterdam | € 595.000 | 789 | € 754 | niet vermeld | 1996 | hal + kantoor | niet vermeld; perceel 1.073 m2 laat buitenparkeren vermoeden [schatting] | Rotterdam Alexander (2,5) | Rotterdam Kralingen-Crooswijk | 171 | 253 / 293 | 70 | € 288 | 23-10-2024 |
| [Volmerstraat 5](https://www.oozo.nl/bedrijfspanden/diemen/bedrijventerreinen/verrijn-stuart/74248/bedrijfsruimte-volmerstraat-5-diemen) | Diemen | € 825.000 | 500 | € 1.650 | niet vermeld | 1967 | hal | niet vermeld | Diemen Zuid (0,9) | Amsterdam Oost/Cruquius | 167 | 245 / 287 | 60 | € 333 | 29-04-2026 |
| [Metaalhof 40](https://www.oozo.nl/bedrijfspanden/rotterdam/prins-alexander/het-lage-land/64020/bedrijfsruimte-metaalhof-40-rotterdam) | Rotterdam | € 1.150.000 | 922 | € 1.247 | 6,0 m | 1986 | hal + kantoor | 3 eigen parkeerplaatsen (niet overdekt) | Rotterdam Alexander (0,8) | Rotterdam Kralingen-Crooswijk | 162 | 230 / 273 | 70 | € 408 | 01-08-2025 |
| [Calandstraat 92](https://www.oozo.nl/bedrijfspanden/schiedam/industrie/s-gravelandsepolder/34650/bedrijfsruimte-calandstraat-92-schiedam) | Schiedam | € 825.000 | 1.000 | € 825 | niet vermeld | 1980 | hal + kantoor | niet vermeld; perceel 1.019 m2 bijna volledig bebouwd | Schiedam Centrum (1,3) | Schiedam Centrum/Spaland | 159 | 232 / 285 | 70 | € 372 | 02-11-2023 |
| [Westerdijk 18](https://www.oozo.nl/bedrijfspanden/utrecht/noordwest/pijlsweerd-zuid/55998/bedrijfsruimte-westerdijk-18-utrecht) | Utrecht | € 1.150.000 | 618 | € 1.861 | niet vermeld | 2020 | nieuwe bedrijfsruimte | niet vermeld | Utrecht Centraal (1,0) | Utrecht West/Lombok | 146 | 212 / 232 | 70 | € 292 | 18-12-2025 |
| [Izaak Enschedeweg 46](https://www.oozo.nl/bedrijfspanden/haarlem/waarder-en-veerpolder/waarderpolder/64179/bedrijfsruimte-iza-228-k-ensched-233-weg-46-haarlem) | Haarlem | € 670.000 | 495 | € 1.354 | niet vermeld | 1962 | hal | niet vermeld | Haarlem Spaarnwoude (1,1) | Haarlem Waarderpolder | 146 | 196 / 235 | 55 | € 348 | 06-08-2025 |
| [Bandoengstraat 21](https://www.oozo.nl/bedrijfspanden/haarlem/indischewijk/nieuw-guineabuurt/55629/maatschappelijk-vastgoed-bandoengstraat-21-haarlem) | Haarlem | € 825.000 | 430 | € 1.919 | niet vermeld | 1971 | maatschappelijk (school/buurthuis-type) | niet vermeld | Bloemendaal (1,8) | Haarlem Waarderpolder | 139 | 194 / 226 | 40 | € 559 | 29-01-2025 |
| [Jan van Galenstraat 78](https://www.oozo.nl/bedrijfspanden/schiedam/schiedamse-havens/wilhelminahaven/62152/bedrijfsruimte-jan-van-galenstraat-78-schiedam) | Schiedam | € 765.000 | 436 | € 1.755 | niet vermeld | 2001 | hal | 7 eigen parkeerplaatsen | Schiedam Centrum (3,1) | Schiedam Centrum/Spaland | 137 | 183 / 236 | 40 | € 544 | 17-06-2025 |
| [Rosmolenstraat 32A](https://www.oozo.nl/bedrijfspanden/zaanstad/rosmolenwijk/rosmolenbuurt/64203/bedrijfsruimte-rosmolenstraat-32-a-zaandam) | Zaandam | € 485.000 | 500 | € 970 | niet vermeld | 1959 | hal | niet vermeld | Zaandam (1,1) | Zaandam Oost | 137 | 236 / 279 | 60 | € 268 | 25-09-2025 |
| [Zilverstraat 56](https://www.bedrijfspand.com/bedrijfspanden/bedrijfsruimte/zilverstraat-56-den-haag/112848/) | Den Haag | € 1.299.500 | 872 | € 1.490 | 6,1 m | 1993 | hal met entresol | 6 eigen parkeerplaatsen + openbaar langs de weg | Den Haag Moerwijk (3,5) | Den Haag Laakhaven/Moerwijk | 135 | 191 / 219 | 70 | € 421 | 20-11-2025 (oozo) |
| [Amsterdamsestraatweg 656D](https://www.oozo.nl/bedrijfspanden/utrecht/noordwest/prins-bernhardplein-en-omgeving/58340/bedrijfsruimte-amsterdamsestraatweg-656-d-utrecht) | Utrecht | € 925.000 | 1.089 | € 849 | niet vermeld | 2003 | hal + kantoor | niet vermeld | Utrecht Zuilen (1,3) | Utrecht Zuilen/Cartesiusweg | 131 | 202 / 222 | 70 | € 408 | 20-03-2025 |
| [Pampuslaan 153](https://www.oozo.nl/bedrijfspanden/amsterdam/weesp-noordwest/bedrijventerrein-noord/75326/bedrijfsruimte-pampuslaan-153-weesp) | Weesp | € 935.000 | 918 | € 1.019 | 5,8 m | 1975 | hal | niet vermeld | Weesp (1,5) | Weesp | 127 | 198 / 251 | 70 | € 372 | 29-05-2026 |
| [Rooseveltstraat 54](https://www.oozo.nl/bedrijfspanden/leiden/bos-en-gasthuisdistrict/gasthuiswijk/45338/bedrijfsruimte-rooseveltstraat-54-leiden) | Leiden | € 1.295.000 | 1.270 | € 1.020 | 9,0 m | 1976 | hal | niet vermeld | Leiden Lammenschans (0,7) | Leiden Morskwartier | 109 | 223 / 252 | 70 | € 509 | 09-10-2024 |
| [Slikkerveerstraat 5](https://www.oozo.nl/bedrijfspanden/rotterdam/ijsselmonde/lombardijen/54362/bedrijfsruimte-slikkerveerstraat-5-rotterdam) | Rotterdam | € 650.000 | 503 | € 1.292 | 5,7 m | 1970 | hal | niet vermeld; perceel 1.055 m2 (ruim terrein) [schatting] | Rotterdam Lombardijen (0,9) | Rotterdam Zuid/Katendrecht-Feijenoord | 105 | 173 / 214 | 60 | € 300 | 31-12-2024 |
| [Nieuwenhuizenweg 13](https://www.bedrijfspand.com/bedrijfspanden/bedrijfsruimte/nieuwenhuizenweg-13-leiden/125280/) | Leiden | € 795.000 | 487 | € 1.632 | 4,5 m | 1998 | bedrijfsunit | parkeerplaatsen op eigen terrein (aantal niet vermeld) | Leiden Lammenschans (1,0) | Leiden Zuidoost/Roomburg | 105 | 217 / 242 | 55 | € 372 | 12-10-2026 |
| [Meidoornhof 7](https://www.oozo.nl/bedrijfspanden/rotterdam/hillegersberg-schiebroek/schiebroek/80179/bedrijfsruimte-meidoornhof-7-rotterdam) | Rotterdam | € 495.000 | 445 | € 1.112 | 3,2 m | 1955 | werkplaats | 5 eigen parkeerplaatsen (niet overdekt) | Rotterdam Noord (2,0) | Rotterdam Noordwest/Spaanse Polder-rand | 102 | 180 / 227 | 45 | € 403 | 09-10-2026 |
| [Kampenringweg 7](https://www.bedrijfspand.com/bedrijfspanden/bedrijfsruimte/kampenringweg-7-gouda/121602/) | Gouda | € 865.000 | 637 | € 1.358 | niet vermeld | 1991 | werkplaats + kantoor | 5 eigen parkeerplaatsen | Waddinxveen Triangel (1,7) | Gouda Kampenringweg | 91 | 178 / 206 | 70 | € 297 | 08-07-2026 (oozo) |

Bestemming: alleen in drie advertenties vermeld [bron]: Zilverstraat 56 'bedrijfsdoeleinden' (bestemmingsplan ZKD 2015), Nieuwenhuizenweg 13 'Bedrijf t/m categorie 4.2', Kampenringweg 7 'Bedrijf t/m categorie 3.2 en perifere detailhandel'. Bij de overige panden staat geen bestemming in de advertentie. Voor horeca, sport en coworking op een bedrijfsbestemming is vrijwel altijd een omgevingsvergunning voor afwijken van het omgevingsplan nodig [schatting]; vraag dat vooraf bij de gemeente na.

### Beste combinaties [schatting]

1. **Galvanistraat 122-126, Rotterdam (Nieuw-Mathenesse)**: € 1.125.000 voor 696 m² in één laag, hal met lichtstraten en 5,9 m vrije hoogte, 1,8 km van Schiedam Centrum. Kern circa 174. Grenst aan Spangen, Bospolder en Schiedam Oost.
2. **Zilverstraat 56, Den Haag (Kerketuinen)**: € 1.299.500 voor 872 m² BVO met 6,1 m onder het spant en 6 eigen parkeerplaatsen; bestemming bedrijfsdoeleinden. Kern circa 135, breed met auto circa 219. Station Moerwijk op 3,5 km, tram 6 op loopafstand.
3. **Limpergstraat 2, Rijswijk (Plaspoelpolder)**: € 1.295.000 voor 1.094 m² (hal 889 m², 5,3 m). Kern circa 184. Lang in aanbod (sinds november 2023): ruimte voor onderhandeling, maar status nabellen.
4. **Anthonetta Kuijlstraat 51B, Rotterdam (Prinsenland)**: € 595.000 voor 789 m² op een perceel van 1.073 m². Kern circa 171, laagste prijs per m² (circa € 754) van de lijst. Twee lagen, vrije hoogte niet vermeld.
5. **Calandstraat 92, Schiedam**: € 825.000 voor 1.000 m² (hal 800 m²), erfpacht. Kern circa 159; metro op circa 1 km.
6. **Westerdijk 18, Utrecht (Pijlsweerd)**: € 1.150.000 voor 618 m², bouwjaar 2020, in een woonwijk op 1 km van Utrecht Centraal. Kern circa 146. Nieuw en dus duurder per m², minder 'rauw'.
7. **Rooseveltstraat 54, Leiden**: € 1.295.000 voor 1.270 m² hal met 9 m vrije hoogte en 23 m overspanning aan het water, 0,7 km van Leiden Lammenschans. Kern circa 109, breed circa 223. Ideaal voor een tussenvloer; wel lang in aanbod (sinds oktober 2024).
8. **Heulweg 16, Rijswijk**: € 395.000 voor 502 m² in twee lagen (hal 313 m²). Kern circa 175. Goedkoopste instap, maar te klein voor 70 eigenaren zonder extra ruimte (circa 60).

Gezien maar niet opgenomen [bron, advertentiepagina's 15-11-2026]:
* Ammandreef 1 Utrecht (858 m², € 1.000.000): status 'Onder bod' op oozo.
* Lodewijk van Deysselstraat 16 Amsterdam (voormalig politiebureau 1956, 1.159 m², ook op biedboek.nl): online veiling was gepland op 17-09-2026; de advertentie staat nog online maar de status na de veiling is niet te verifiëren.
* Erich Salomonstraat 90 Amsterdam: 'Verkocht onder voorbehoud' op oozo.
* Veldkersweg 16 Rotterdam (circa 190 m²) en Petroleumhavenweg 24 Amsterdam (circa 278 m²): te klein.
* Westvlietweg 85 Den Haag (€ 1.445.000 voor 462 m²) en Cruquiusweg 98 W Amsterdam (€ 2.950.000): te duur.
* De Watering 1 Zaandam (horeca, 1.311 m², € 650.000): net boven 1.300 m² en eigen kern circa 37 [schatting]; eventueel als reserve.
* Limmerick 86 Amsterdam (480 m², € 575.000, 3 parkeerplaatsen): ligt aan de westrand bij Halfweg, kern circa 63 [schatting].
* Biedboek.nl had op 15-11-2026 binnen de vier provincies geen passend gebouw tussen 350 en 1.300 m² behalve twee politiebureaus (Amsterdam, hierboven, en P.A. de Genestetstraat 60 Dordrecht, 738 m², bouwjaar 2002, prijs via inschrijving) [bron: https://www.biedboek.nl]. Dordrecht scoort met kern circa 96 matig [schatting].
* Kerken: de webzoekopdracht vond geen kerk te koop in Den Haag, Rotterdam, Utrecht, Haarlem of Leiden; het aanbod van kerkmakelaar Reliplan is niet machinaal leesbaar [bron: https://www.reliplan.nl/aanbod/]. Dit blijft een open spoor.

## C. Herbeoordeling bestaande locaties

### Basislocaties

| Locatie | Eerdere schatting (1.5) [schatting] | Leden 4,5 km [schatting] | Kern [schatting] | Breed [schatting] | Breed met auto [schatting] | Parkeren [bron] | Advertentie 15-11-2026 [bron] | Oordeel |
|---|---|---|---|---|---|---|---|---|
| Van Heutszstraat 4, Utrecht | 125 | 107 | 150 | 216 | 234 | geen eigen terrein genoemd; betaald parkeren voor de deur (advertentie) | [te koop: bedrijfspand.com advertentie 116706 (online 12-03-2026, bijgewerkt 13-11-2026, 1 eenheid beschikbaar) en oozo 72387 Beschikbaar](https://www.bedrijfspand.com/bedrijfspanden/bedrijfsruimte/van-heutszstraat-4-utrecht/116706/) | **behouden** |
| Rietveldenweg 13, 's-Hertogenbosch | 60 | 40 | 59 | 84 | 97 | circa 8 auto's op eigen terrein plus openbaar aan voor- en zijkant (advertentie) | [te koop: bedrijfspand.com 126268 (online 05-11-2026, bijgewerkt 14-11-2026, 2 eenheden beschikbaar)](https://www.bedrijfspand.com/bedrijfspanden/bedrijfsruimte/rietveldenweg-13-den-bosch/126268/) | **behouden met voorwaarden** |
| De Eendenkooi 1A, 's-Hertogenbosch | 57 | 36 | 56 | 82 | 96 | geen eigen terrein genoemd; openbaar en gratis bij sporthal De Schutskamp (advertentie) | [te koop: bedrijfspand.com 125406 (online 15-10-2026, bijgewerkt 13-11-2026, 1 eenheid beschikbaar)](https://www.bedrijfspand.com/bedrijfspanden/bedrijfsruimte/de-eendenkooi-1-a-den-bosch/125406/) | **behouden met voorwaarden** |
| Dinsdagse Wetering 56A, Voorhout | 38 | 30 | 36 | 69 | 83 | ruim voldoende parkeerplaatsen op eigen terrein, buitenterrein circa 300 m2 (advertentie) | [te koop: bedrijfspand.com 125825 (online 27-10-2026, bijgewerkt 14-11-2026, 1 eenheid beschikbaar)](https://www.bedrijfspand.com/bedrijfspanden/bedrijfsruimte/dinsdagse-wetering-56-a-voorhout/125825/) | **verwijderen** |
| Herenweg 15, Maarssen | 52 | 25 | 60 | 101 | 123 | niet vermeld; perceel 1.405 m2 met circa 840 m2 bebouwing laat ruimte voor eigen parkeren [schatting] | [te koop: oozo 80890 Beschikbaar, aangeboden sinds 28-10-2026](https://www.oozo.nl/bedrijfspanden/stichtse-vecht/maarssen/maarsseveen/80890/bedrijfsruimte-herenweg-15-maarssen) | **behouden met voorwaarden** |
| Ring 15, Pernis | 55 | 57 | 57 | 126 | 178 | niet vermeld; perceel 935 m2 [onbekend of er eigen parkeerplaatsen zijn] | [te koop: oozo 77099 Beschikbaar, aangeboden sinds 15-07-2026](https://www.oozo.nl/bedrijfspanden/rotterdam/pernis/pernis/77099/maatschappelijk-vastgoed-ring-15-pernis-rotterdam) | **behouden met voorwaarden** |
| Nijverheidsstraat 4C, Uden | 13 | 12 | 12 | 20 | 32 | niet gecontroleerd in advertentietekst | [te koop: bedrijfspand.com 114412 (online 15-01-2026, bijgewerkt 15-11-2026, 2 eenheden beschikbaar)](https://www.bedrijfspand.com/bedrijfspanden/bedrijfsruimte/nijverheidsstraat-4-c-uden/114412/) | **verwijderen** |

* **Van Heutszstraat 4** (behouden): Enige basislocatie die de 70 tot 100 al in de kern haalt (circa 107 binnen 4,5 km, circa 150 met een halte); lage hal (3,5 m) en betaald parkeren zijn de zwakke punten.
* **Rietveldenweg 13** (behouden met voorwaarden): Kern circa 59 blijft onder 70; met de bredere regel (8 km fiets, 2 haltes) circa 84 en met auto circa 97, en dankzij 8 eigen parkeerplaatsen telt die autoring hier echt mee. Voorwaarde: regionale werving (Vught, Rosmalen, Oss, Tilburg) en bestemming bedrijventerrein laten verruimen.
* **De Eendenkooi 1A** (behouden met voorwaarden): Zelfde verzorgingsgebied als Rietveldenweg maar iets zwakker (kern circa 56, breed circa 82) en vraagprijs op het plafond; alleen houden als de prijs zakt, het gebouw (7,8 m hoog, sport) past wel goed.
* **Dinsdagse Wetering 56A** (verwijderen): Kern circa 36 en breed circa 69; ook met auto (circa 83) leunt alles op Leiden, en in Leiden zelf staan nu panden met een twee tot drie keer grotere kern (Rooseveltstraat 54, Nieuwenhuizenweg 13).
* **Herenweg 15** (behouden met voorwaarden): Stijgt het sterkst door de bredere regel: kern circa 60, breed circa 101, met auto circa 123 omdat Utrecht Noordwest binnen 8 km ligt; voorwaarde is dat eigen parkeren op het perceel bevestigd wordt en dat Utrecht actief mee wordt geworven.
* **Ring 15** (behouden met voorwaarden): Kern circa 57 (de metro naar Schiedam en Vlaardingen telt in deze methode niet mee), breed circa 126 en met auto circa 178; stijgt dus duidelijk, maar alleen als leden echt via metro, fietstunnel of auto komen en er parkeerruimte is.
* **Nijverheidsstraat 4C** (verwijderen): Kern circa 12, breed circa 20 en met auto circa 32: ook de bredere regel brengt Uden nergens in de buurt van 70; het gebouw is goed maar de plek niet.

Wat verandert door de bredere regel [schatting]: Maarssen stijgt van circa 60 naar circa 101 (breed) en circa 123 met auto, omdat Utrecht Noordwest binnen 8 km valt. Pernis stijgt van circa 57 naar circa 126 en 178, omdat Schiedam, Vlaardingen en Rotterdam West binnen 8 km liggen. Den Bosch stijgt van circa 56 tot 59 naar circa 82 tot 84 en circa 96 tot 97 met auto; Rietveldenweg heeft als enige van de drie bevestigde eigen parkeerplaatsen (circa 8). Voorhout stijgt naar circa 69 en 83 met auto, maar Leiden zelf scoort beter. Uden blijft onder 35. Utrecht blijft koploper maar wint relatief het minst, omdat het al in de kern sterk is.

### Ronde 6 lijst K (kandidaten6.py)

| Pand | Plaats | Leden 4,5 km [schatting] | Kern [schatting] | Breed [schatting] | Breed met auto [schatting] | Eigenaren passend [schatting] | Status 15-11-2026 | Oordeel | Reden |
|---|---|---|---|---|---|---|---|---|---|
| Hoge Larenseweg 202A | Hilversum | 38 | 102 | 185 | 207 | 25 | bedrijfspand.com 123486: 1 eenheid beschikbaar, bijgewerkt 13-11-2026; parkeren in de bedrijfsruimte zelf | **behouden met voorwaarden** | goed verzorgingsgebied (kern circa 102) maar pand te klein voor 70 eigenaren (circa 25); alleen als kleinere club of met extra ruimte; kleiner dan 350 m2 |
| Langendijkstraat 9-ZW | Haarlem | 66 | 148 | 197 | 221 | 35 | oozo 52951: Beschikbaar, aangeboden sinds 26-10-2026 | **behouden met voorwaarden** | goed verzorgingsgebied (kern circa 148) maar pand te klein voor 70 eigenaren (circa 35); alleen als kleinere club of met extra ruimte |
| Boschstraat 96-BIS | Breda | 46 | 60 | 82 | 96 | 35 | niet opnieuw gecontroleerd in ronde 7 (behalve waar vermeld) | **verwijderen** | kern circa 60 onder 90 en pand te klein (circa 35 eigenaren) |
| Zevenend 26 | Laren | 28 | 28 | 52 | 83 | 20 | niet opnieuw gecontroleerd in ronde 7 (behalve waar vermeld) | **verwijderen** | verzorgingsgebied te dun (kern circa 28, breed circa 52); kleiner dan 350 m2 |
| Noordhaven 46 | Zevenbergen | 4 | 10 | 21 | 36 | 45 | niet opnieuw gecontroleerd in ronde 7 (behalve waar vermeld) | **verwijderen** | verzorgingsgebied te dun (kern circa 10, breed circa 21) |
| Stationsstraat 2 | Zevenbergen | 4 | 10 | 21 | 36 | 35 | niet opnieuw gecontroleerd in ronde 7 (behalve waar vermeld) | **verwijderen** | verzorgingsgebied te dun (kern circa 10, breed circa 21) |
| Plein 1 | Dordrecht | 50 | 91 | 137 | 157 | 30 | niet opnieuw gecontroleerd in ronde 7 (behalve waar vermeld) | **behouden met voorwaarden** | goed verzorgingsgebied (kern circa 91) maar pand te klein voor 70 eigenaren (circa 30); alleen als kleinere club of met extra ruimte |
| Concordiastraat 29 | Alphen a/d Rijn | 24 | 30 | 70 | 91 | 0 | niet opnieuw gecontroleerd in ronde 7 (behalve waar vermeld) | **verwijderen** | verzorgingsgebied te dun (kern circa 30, breed circa 70); kleiner dan 350 m2 |
| Industrieweg 99B | Rotterdam | 92 | 168 | 245 | 295 | 0 | niet opnieuw gecontroleerd in ronde 7 (behalve waar vermeld) | **verwijderen** | verzorgingsgebied sterk (kern circa 168) maar 306 m2 is te klein voor het programma, ook met entresol; met auto circa 295, maar dan woont de meerderheid buiten fietsafstand en is eigen parkeren niet bevestigd |
| Nijverheidstraat 9 | Katwijk | 34 | 34 | 65 | 84 | 70 | niet opnieuw gecontroleerd in ronde 7 (behalve waar vermeld) | **verwijderen** | verzorgingsgebied te dun (kern circa 34, breed circa 65) |
| Sweelincksingel 3-7 | Schiedam | 56 | 151 | 219 | 273 | 70 | oozo 59572: Beschikbaar, aangeboden sinds 16-04-2025 | **behouden** | kern circa 151 en breed circa 219; pand biedt ruimte voor circa 70 eigenaren |
| Hoogmadeseweg 62 | Leiderdorp | 42 | 99 | 209 | 235 | 50 | oozo 7085: Beschikbaar, aangeboden sinds 14-12-2023 (lang) | **behouden met voorwaarden** | goed verzorgingsgebied (kern circa 99) maar pand te klein voor 70 eigenaren (circa 50); alleen als kleinere club of met extra ruimte |
| Helderseweg 50 | Alkmaar | 36 | 58 | 135 | 143 | 65 | niet opnieuw gecontroleerd in ronde 7 (behalve waar vermeld) | **behouden met voorwaarden** | kern circa 58 blijft onder 90, breed circa 135; alleen met regionale werving of goed eigen parkeren |
| Dijklaan 131-133 | Breda | 47 | 59 | 81 | 94 | 70 | niet opnieuw gecontroleerd in ronde 7 (behalve waar vermeld) | **behouden met voorwaarden** | kern circa 59 blijft onder 90, breed circa 81; alleen met regionale werving of goed eigen parkeren |
| Zaanenstraat 22 | Haarlem | 60 | 142 | 195 | 225 | 50 | oozo 46366: Beschikbaar, aangeboden sinds 04-07-2024 | **behouden met voorwaarden** | goed verzorgingsgebied (kern circa 142) maar pand te klein voor 70 eigenaren (circa 50); alleen als kleinere club of met extra ruimte |
| Heulweg 1 | Pijnacker | 38 | 38 | 87 | 204 | 55 | niet opnieuw gecontroleerd in ronde 7 (behalve waar vermeld) | **verwijderen** | verzorgingsgebied te dun (kern circa 38, breed circa 87); met auto circa 204, maar dan woont de meerderheid buiten fietsafstand en is eigen parkeren niet bevestigd |
| Celebesstraat 17 | Wormerveer | 30 | 42 | 111 | 153 | 65 | niet opnieuw gecontroleerd in ronde 7 (behalve waar vermeld) | **behouden met voorwaarden** | kern circa 42 blijft onder 90, breed circa 111; alleen met regionale werving of goed eigen parkeren |
| Drilleveld 1 | Nieuwegein | 42 | 42 | 89 | 117 | 70 | niet opnieuw gecontroleerd in ronde 7 (behalve waar vermeld) | **verwijderen** | verzorgingsgebied te dun (kern circa 42, breed circa 89) |
| Enschotsebaan 8 | Berkel-Enschot | 37 | 37 | 53 | 71 | 70 | niet opnieuw gecontroleerd in ronde 7 (behalve waar vermeld) | **verwijderen** | verzorgingsgebied te dun (kern circa 37, breed circa 53) |
| Nieuw-Loosdrechtsedijk 82a | Loosdrecht | 20 | 20 | 31 | 89 | 70 | niet opnieuw gecontroleerd in ronde 7 (behalve waar vermeld) | **verwijderen** | verzorgingsgebied te dun (kern circa 20, breed circa 31) |
| Hooge Zijde 29 | Eindhoven | 27 | 27 | 56 | 75 | 70 | niet opnieuw gecontroleerd in ronde 7 (behalve waar vermeld) | **verwijderen** | verzorgingsgebied te dun (kern circa 27, breed circa 56) |
| Stirlingweg 12 | Veghel | 13 | 13 | 20 | 40 | 70 | niet opnieuw gecontroleerd in ronde 7 (behalve waar vermeld) | **verwijderen** | verzorgingsgebied te dun (kern circa 13, breed circa 20) |
| Woestduinlaan 35a | Doorn | 10 | 10 | 20 | 54 | 70 | niet opnieuw gecontroleerd in ronde 7 (behalve waar vermeld) | **verwijderen** | verzorgingsgebied te dun (kern circa 10, breed circa 20) |
| Motorstraat 7-9 | Rotterdam-Zuid | 120 | 138 | 194 | 237 | 70 | oozo 68926: Beschikbaar, aangeboden sinds 02-12-2025 | **behouden** | kern circa 138 en breed circa 194; pand biedt ruimte voor circa 70 eigenaren |
| Ledeboerstraat 29E | Tilburg | 44 | 55 | 83 | 97 | 70 | niet opnieuw gecontroleerd in ronde 7 (behalve waar vermeld) | **behouden met voorwaarden** | kern circa 55 blijft onder 90, breed circa 83; alleen met regionale werving of goed eigen parkeren |

De advertenties van ronde 6 zijn niet allemaal opnieuw geopend; waar de status wel is gezien staat dat in de tabel [bron: oozo.nl en bedrijfspand.com, 15-11-2026].

## Beperkingen

* Hemelsbrede stralen en een eigen intercitylijst zijn een benadering; de 'halte' regel kan stations op een andere lijn meetellen. Controleer reistijden in de NS Reisplanner of 9292 [schatting].
* Metro en tram tellen niet mee (de ProRail dataset bevat alleen treinstations). Pernis, Schiedam, Rotterdam en Den Haag worden daardoor eerder onderschat dan overschat [schatting].
* De trechterpercentages (30 %, 1,5 %, 40 %) zijn aannames uit werving_onderzoek.md 1.5; absolute getallen zijn indicatief, de volgorde is robuuster [schatting].
* Inkomen per inwoner ontbreekt voor een deel van de buurten in CBS 2023 [bron]; het aandeel hoge inkomens is daarom ook gegeven.
* oozo toont maximaal 50 pagina's per gemeente; in Amsterdam, Rotterdam, Den Haag en Utrecht zijn dus niet alle advertenties gelezen [bron: oozo.nl]. bedrijfspand.com gaf per stad maar enkele koopresultaten. Funda in business is bewust niet gebruikt, dus er kan meer aanbod zijn.
* Vrije hoogte, bestemming en parkeren staan vaak niet in de advertentie; 'niet vermeld' betekent onbekend, niet afwezig.

## Bestanden

* ronde7_wijken.json: alle 34 verzorgingsgebieden met metrieken en schattingen.
* ronde7_kandidaten.py: lijst K (zelfde tupelformaat als kandidaten6.py) en META per pand.
* ronde7_herbeoordeling.json: oordeel per bestaande locatie.

## Bronnen

* https://api.pdok.nl/cbs/wijken-en-buurten-2024/ogc/v1
* https://api.pdok.nl/cbs/wijken-en-buurten-2023/ogc/v1
* https://api.pdok.nl/prorail/spoorwegen/ogc/v1/collections/station/items
* https://api.pdok.nl/bzk/locatieserver/search/v3_1/free
* https://api.pdok.nl/kadaster/bestuurlijkegebieden/ogc/v1
* https://www.oozo.nl/bedrijfspanden
* https://www.bedrijfspand.com
* https://www.biedboek.nl
* https://www.reliplan.nl/aanbod/
* Advertentie URL's per pand: zie tabellen en ronde7_kandidaten.py.
