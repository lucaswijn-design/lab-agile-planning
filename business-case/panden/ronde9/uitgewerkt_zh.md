# Ronde 9: vijf panden uitgewerkt (Zuid-Holland)

Uitgewerkt op 15 en 16 november 2026 volgens `inrichting/BRIEF_ONTWERP.md`. Per pand een ontwerp in `ontwerpen_extra/<slug>.py`, een layout met kosten in `layout_extra/<slug>.py` en een dossier in `dossiers/<slug>.json`.
Alle kosten zijn sober doorgerekend met `pand_case.run(slug, torens=True, sober=True)` en `pand_case.fee_inleg_terug(...)`. Alle normen van `inrichting/programma.py` worden gehaald (belcellen, focuskamers, lounge, lockers, planten, bomen). Plattegronden per laag zijn gerenderd en nagelopen op botsingen, looppaden en daglicht.

Fokkerstraat 475 in Schiedam valt af: op 11 november 2024 is op dat adres een melding voor motorvoertuigenherstel gedaan (gemeenteblad Schiedam), de brochure is oud en het pand staat niet meer in het actuele aanbod. Vervanger is Kampenringweg 7 in Gouda.

## Overzicht

| Pand | Alles in | Om te draaien (vol lid per maand) | Inleg terug | LTV | Werkplekken | Max eigenaren | Gekozen eigenaren | Verzorgingsgebied breed |
|---|---|---|---|---|---|---|---|---|
| Kommiezenlaan 27, Schiedam | € 1.723.810 | € 319 | € 479 | 0,54 | 43 | 67 | 66 (33 vol, 33 deeltijd) + 30 clubleden | 245 (3,7 x) |
| Van Riemsdijkweg 17, Rotterdam | € 1.667.542 | € 215 | € 332 | 0,40 | 58 | 98 | 84 (42 + 42) + 40 | 144 (1,7 x) |
| Edelhertstraat 12, Capelle aan den IJssel | € 1.858.800 | € 237 | € 359 | 0,48 | 48 | 81 | 80 (40 + 40) + 40 | 159 (2,0 x) |
| Zilverstraat 56, Den Haag | € 2.142.248 | € 262 | € 361 | 0,52 | 52 | 87 | 86 (43 + 43) + 40 | 191 (2,2 x) |
| Kampenringweg 7, Gouda (vervangt Fokkerstraat 475) | € 1.614.088 | € 269 | € 405 | 0,51 | 43 | 72 | 66 (33 + 33) + 45 | 178 (2,7 x) |

Max eigenaren is `capaciteit.max_leden(slug, 0.5, n_club)` met het gekozen aantal clubleden. Het verzorgingsgebied komt uit META `leden_breed` van ronde 9 (Zilverstraat en Kampenringweg uit ronde 7); overal minstens 1,2 x het gekozen aantal eigenaren.
Clubleden zijn zo gekozen dat de gym op het drukste uur hooguit circa 90% vol zit (bij Kommiezenlaan begrenst het paviljoen van 70 m² dat op 30).
Waar de capaciteitscheck 5 toiletten vraagt en er 4 telt (wastoren plus toegankelijk toilet), is een extra toiletgroep ingetekend (Zilverstraat, Van Riemsdijkweg, Edelhertstraat); `capaciteit.aanbod` telt die niet mee, dus de melding blijft staan.

## Statuscheck en vervanging

* Gecontroleerd op 15 november 2026 met zoekmachines (funda niet geopend), oozo.nl en bedrijfspand.com.
* Kommiezenlaan 27: oozo 57658, Beschikbaar, aangeboden sinds 9 oktober 2026, € 775.000 k.k., 335 m², hal 211 m², vrije hoogte 4 m, overspanning 10 m, perceel 993 m². Doorgerekend met € 785.000 (ronde 9), dus aan de veilige kant.
* Van Riemsdijkweg 17: oozo 80401, Beschikbaar, aangeboden sinds 16 oktober 2026, € 895.000 k.k., hal 563 + kantoor 154 m². In ronde 9 stond bij een zoekresultaat ook het label Onder bod: eerst nabellen.
* Edelhertstraat 12: oozo 70332, Beschikbaar, aangeboden sinds 19 januari 2026, € 995.000 k.k., 662 m², vrije hoogte 4,7 m.
* Zilverstraat 56: bedrijfspand.com 112848, te koop, online sinds 21 november 2025, bijgewerkt 13 november 2026, € 1.299.500 k.k.
* Fokkerstraat 475: BAG-pand 0606100000005183 (1992), één verblijfsobject van 536 m² industriefunctie, geen woningen. Maar: melding motorvoertuigenherstel op Fokkerstraat 475 van 11 november 2024 in het gemeenteblad, brochure met een oud objectnummer zonder datum, en op de actuele oozo-lijst van Schiedam Industrie staan wel Fokkerstraat 549 en 551 maar niet 475. Conclusie: vrijwel zeker verkocht of verhuurd aan een garagebedrijf. Afgevallen; het dossier blijft staan.
* Vervangers bekeken: Sweelincksingel 3 tot en met 7 Schiedam (boerderijcomplex Landvreugd, BAG: twee panden uit 1905 met bijeenkomst- en kantoorfunctie, geen woningen; maar gemeentelijk monument met restauratieplicht, label G, verkoop bij inschrijving sinds april 2025 en twee losse gebouwen met lage verdiepingen) en Kampenringweg 7 Gouda (BAG-pand 0513100011130710, 1991, één verblijfsobject van 485 m² industriefunctie, geen woningen; bedrijfspand.com 121602, te koop € 865.000 k.k., online sinds 9 juli 2026, bijgewerkt 13 november 2026). Gekozen: Kampenringweg 7, omdat de status vast staat en het pand zonder monumentenwerk bruikbaar is. Sweelincksingel blijft een optie als de inschrijving nog open is.

## 1. Kommiezenlaan 27, Schiedam

**Verificatie.** BAG-pand 0606100000017938 (1950, 63,8 x 30 m) met acht verblijfsobjecten op zeven adressen (Kommiezenlaan 15 tot en met 27), alle industriefunctie, geen woningen. Nummer 27 is verblijfsobject 0606010000018780, 300 m², status Verbouwing.
Uitsnede: het BAG-adrespunt van nummer 27 ligt aan de straat in de westelijke beuk; het oude BAG-pand 0606100000009450 (1958, 238 m²) beslaat precies die beuk, en BRK-perceel 6785 (circa 940 m², oozo 993 m²) heeft zijn oostgrens op de beukgrens. Unit = 9,1 x 25,8 m (235 m²), footprint vervangen, `footprint_complex` bewaard, de rest van het complex als context, oude overlappende BAG-panden uit 1957 en 1958 uit de context gehaald, perceel 6785 als perceel. Het perceel omvat een open erf van circa 700 m² aan de west- en achterkant. Context 0 en 1 zijn het nieuwe gympaviljoen en de nieuwe tuinkamer (ontwerp). Zie `opmerking` in het dossier.

**Site.** Straatgevel op het noordnoordwesten aan de Kommiezenlaan, 300 m van station Schiedam Centrum. Oostkant blind tegen de buurbeuk. Westgevel aan het eigen erf (middagzon), achterkant op het zuidzuidoosten (zon). Vrije hoogte circa 4 m: geen tussenvloer mogelijk.

**Ontwerp.** De beuk is te klein voor de hele club, het erf is groot. Daarom drie delen. In de beuk aan de straat het café met keuken, kookeiland, lange tafel voor acht en een zitnis achter een nieuwe glazen voorgevel; dan de werkzone met vier eilanden haaks op een nieuwe glazen zijgevel van 14 m aan het erf; langs de blinde wand vergaderkamer voor zes, sta-kamer, focuskamer en twee belcellen; achterin een D-vormige wastoren en lockers. Door een opening van 3 m de nieuwe tuinkamer van 10 x 9 m aan de zonkant: raambar van 8 m op het zuiden met een pergola, eiland van zes, bank, focuskamer en drie belcellen. Los op het erf, 10 m verder, het gympaviljoen van 8,8 x 8 m met twee racks, groepslesvloer, roeiers, een D-vormige douchetoren en een eigen deur op toegangspas. Terras langs de zijgevel, tuin, 3 parkeerplaatsen. 24 planten en 8 bomen; groen sedumdak op tuinkamer en paviljoen.

**Verbetercycli.**
* Start (alleen de beuk plus een gympaviljoen, 36 eigenaren en 20 clubleden): alles in € 1.593.037, om te draaien € 675, inleg terug € 907, LTV 0,73; 24 werkplekken, max 40 eigenaren. Veel te duur: de vaste lasten vallen op te weinig eigenaren.
* Cyclus 1 (eigenaren en ruimte): tuinkamer van 91 m² in het verlengde van de beuk toegevoegd (19 werkplekken erbij), gympaviljoen naar de zuidwesthoek van het erf zodat er 10 m tussen gym en tuinkamer zit, derde belcel en tweede focuskamer in de tuinkamer; 64 eigenaren en 30 clubleden. € 1.752.559, € 338, € 511, LTV 0,56; 43 werkplekken, max 67.
* Cyclus 2 (routes, daglicht, kosten): rubberboom uit de draairichting van de voordeur, strelitzia naar het zuidglas, monstera in plaats van een boom voor de raambar, de doorgang als open opening van 3 m in plaats van een deur; asbestreserve geschrapt omdat het dak nieuw is (verbouwing, label A++), de asbestinventarisatie blijft; 66 eigenaren. Eindstand € 1.723.810, € 319, € 479, LTV 0,54.

**Risico's.** Hoogste maandbedrag van de vijf door het extra bouwwerk (tuinkamer € 118.300 en paviljoen € 87.500 als schatting) op een klein pand. Vergunning nodig voor aanbouw en paviljoen op het erf (bebouwingsregels bedrijventerrein onbekend). Lage hal van 4 m. Of het erf echt bij nummer 27 hoort is afgeleid uit de BRK en de 993 m² van oozo: in de koopakte nakijken. Eigendom of erfpacht onbekend (aanname € 3.000 per jaar). Prijs wisselt tussen € 739.000 en € 785.000 in de bronnen.

## 2. Van Riemsdijkweg 17, Rotterdam Waalhaven

**Verificatie.** BAG-pand 0599100000768226 (1957) met twee verblijfsobjecten: Van Riemsdijkweg 17, 717 m² kantoorfunctie, in gebruik, en 17BG, 564 m² overige gebruiksfunctie, ingetrokken. Geen woningen. Buurpanden aan weerszijden zijn bedrijfspanden uit 1957. Geen complex: eigen pand op een eigen perceel van 690 m² (erfpacht, canon € 8.666 per jaar).

**Site.** 40 x 15 m in een rij. Straatgevel op het oosten aan de Van Riemsdijkweg met een eigen strook van 6 m, achtergevel op het westen vrij (kijkt uit op het terrein van de buren). Lichtstraat in de hal (luchtfoto, circa u 16 tot 37). Showroom 159 m² aan de straat, kantoor 154 m² erboven (aanname), hal 404 m² met 5,2 m vrije hoogte.

**Ontwerp.** Van straat naar achter: druk, rustig, zweet. In de showroom het café met een raambar van 6 m achter het glas, keuken, kookeiland, lange tafel voor twaalf, zeshoekige bank, een bank langs de zuidwand, drie fauteuils en een toiletgroep bij de entree. Daarachter onder de lichtstraat zes eilanden van vier bureaus, langs de noordwand vergaderkamer voor zes, sta-kamer en vijf belcellen, langs de zuidwand een lockerwand van 6 m en twee focuskamers. Dan de achthoekige wastoren en douchetoren als buffer van 6 m, en achterin de gym met drie racks, groepslesvloer, roeiers en nieuwe ramen in de westgevel. Boven de showroom een stille verdieping met drie eilanden, vergaderkamer, twee focuskamers en twee belcellen. Terras aan de straat. 36 planten en 12 bomen.

**Verbetercycli.**
* Start (76 eigenaren, 40 clubleden): € 1.646.912, € 247, € 368, LTV 0,45; lounge 12 van 16, planten 23 van 36, bomen 7 van 12.
* Cyclus 1 (lounge, groen, routes): bank langs de zuidwand van het café, zeshoekige bank verschoven naar het midden zodat er 1,4 m vrij blijft achter de stoelen van de lange tafel, hangplanten aan de spanten onder de lichtstraat, kentia tussen werkzone en torens, extra bomen aan de straat.
* Cyclus 2 (eigenaren, toiletten, belcellen): 84 eigenaren (42 + 42), toiletgroep bij de entree, vijfde belcel aan de noordwand, rubberboom weg uit de looproute. Eindstand € 1.667.542, € 215, € 332, LTV 0,40. Bij 90 eigenaren zakt het naar € 190, maar dan schieten lounge en belcellen tekort, en boven 96 eigenaren is inleg terug onmogelijk (verkoopwaarde lager dan alle inleg); 84 gehouden omdat de kern rond het adres dun is (circa 62).

**Risico's.** Ver van treinstations (circa 5 tot 8 km), kern van het verzorgingsgebied dun; de club leunt op fiets, bus en auto. Mogelijk al onder bod. Indeling showroom, hal en kantoor is aangenomen (geen plattegrond gezien). Erfpacht (canon en looptijd navragen). Asbestreserve (1957). Waalhaven is een havenbedrijventerrein: omgevingsplan voor sport en horeca nakijken.

## 3. Edelhertstraat 12, Capelle aan den IJssel

**Verificatie.** BAG-pand 0502100000021506 (1974) met één verblijfsobject, Edelhertstraat 12, 619 m² overige gebruiksfunctie. Geen woningen. Vrijstaand op een eigen perceel (BRK 1.019 m², advertentie 1.044 m², eigen grond). Ten noorden op 0,4 m een autodemontagebedrijf, ten zuiden op 5 m een bedrijfsverzamelgebouw.

**Site.** Vierkante hal van 24 x 24 m, vrije hoogte 4,7 m, vier lichtstraten oost-west. Westgevel aan de Edelhertstraat met een bomenrij en een sportpark aan de overkant; oostkant een eigen erf van 10 m (parkeren); zuidkant een eigen strook van 5 m in de zon. Indeling van hal en kantoor niet bekend (aanname: entree aan de straat).

**Ontwerp.** Vier kwarten. Noordwest aan de straat de werkzone achter een nieuwe glazen westgevel: raambar van 9 m, vier eilanden haaks op het glas, vergaderkamer voor zes en sta-kamer aan de noordwand, zes belcellen. Zuidwest het café met keuken, kookeiland, lange tafel voor twaalf, een raambar aan de straat en een zitnis van 6,5 m langs nieuw glas in de zuidgevel, met een terras ervoor. Noordoost de gym (104 m²) met een eigen deur aan het erf, drie racks, groepslesvloer en roeiers. Tussen gym en werken een strook van 6 m met de achthoekige douchetoren (open naar de gym) en wastoren (open naar de lounge). Zuidoost lounge en spel: pingpong, zeshoekige bank, boekenwand, lockerwand, een tweede vergaderkamer, twee focuskamers en een toiletgroep naast de gymdeur. 29 planten en 10 bomen.

**Verbetercycli.**
* Start (76 eigenaren, 40 clubleden): € 1.831.494, € 251, € 373, LTV 0,50; maar twee vergaderkamers waar er drie nodig zijn, lockers 100 van 103, planten 18 van 29, bomen 8 van 10.
* Cyclus 1 (routes, geluid, groen): lockers van de wastoren zaten op een zijde tussen toren en gymwand en waren onbereikbaar, nu op de zijde naar de lounge; tweede vergaderkamer in de lounge; lockerwand 5 m; zeshoekige bank verschoven; hangplanten boven de raambar, planten naar licht (olijf en strelitzia in de zon, kentia en aspidistra in de lounge); bomen op het erf.
* Cyclus 2 (eigenaren, toiletten): 80 eigenaren (40 + 40), toiletgroep naast de gymdeur, boom op het terras weg uit de plantenbak. Eindstand € 1.858.800, € 237, € 359, LTV 0,48.

**Risico's.** Indeling en kantoorgedeelte onbekend, plattegrond opvragen. Autodemontagebedrijf ernaast (stof, uitstraling). Hal uit 1974: asbestreserve en isolatie meegenomen. Station op circa 3 km (metro Capelle dichterbij). Status sinds januari 2026 beschikbaar: vraag naar onderhandelingsruimte.

## 4. Zilverstraat 56, Den Haag

**Verificatie.** BAG-pand 0518100000326892 (1993) met één verblijfsobject, Zilverstraat 56, 580 m² industriefunctie. Geen woningen. Juridisch een appartementsrecht (49/576 aandeel) in een bedrijfsverzamelgebouw van 16 bedrijfsruimten en 54 parkeerplaatsen; VvE niet actief; erfpacht eeuwigdurend afgekocht. Het eigen BAG-pand is de unit zelf, dus geen uitsnede nodig. Woningen liggen aan de overkant van de sloot, circa 30 m van de achtergevel.

**Site.** 17,4 x 27,8 m binnenwerks, begane grond 499 m² BVO, betonnen entresol 373 m² BVO op circa 3,4 m rond een vide met 6,1 m vrije hoogte (plattegrond van de makelaar), 3,2 m onder en 3,0 m boven de entresol. Gevel aan het parkeerhof (overheaddeur 4 x 4 m, deur, ramen) alleen over de eerste 12 m; achtergevel met ramen op beide lagen naar een groenstrook met sloot.

**Ontwerp.** De hoge vide aan de hofkant wordt de gym (139 m², 6,1 m hoog) met de overheaddeur als glazen eigen ingang, drie racks, groepslesvloer, roeiers en een D-vormige douchetoren in de lage hoek. Ernaast de clubdeur, een hoge entreehal met 6,8 m lockers en de trap. Midden onder de tweede vide een zeshoekige bank, pingpong, keuken en kookeiland, en tegen de blinde wand vergaderkamer voor zes, sta-kamer en drie belcellen. Achterin het café aan de ramen: zitnis van 6 m, raambar van 6,6 m, lange tafel voor twaalf. Boven: werkzone met vier eilanden langs de achtergevel, werkzone met raambar en twee eilanden aan de hofkant onder nieuwe lichtkoepels, drie focuskamers, een vergaderkamer in het bestaande kantoortje, stille bieb met belcellen, en boven de lage hoeken van de gym alleen techniek, berging en een toiletgroep. 44 planten en 16 bomen.

**Verbetercycli.**
* Start (70 eigenaren, 30 clubleden): € 2.168.698, € 374, € 492, LTV 0,61; 41 werkplekken waar 42 nodig zijn, planten 28 van 44, bomen 6 van 15.
* Cyclus 1 (routes, daglicht, groen): racks stonden in de looproute van de gymdeur en zijn opgeschoven; raambar van 6,6 m aan de achterramen (52 werkplekken); werkzone boven loopt niet meer over de vide; pothos langs de balustrades, bomen naar licht (olijf aan de achterramen, kentia in de donkere delen).
* Cyclus 2 (eigenaren, toiletten): 86 eigenaren en 40 clubleden, toiletgroep op de verdieping boven de gymhoek, derde focuskamer en zevende belcel. € 2.184.798, € 267, € 373.
* Cyclus 3 (kosten): zes lichtkoepels stonden dubbel in de begroting (ook in de post lichtstraten bij isoleren) en zijn geschrapt; asbestreserve weg (bouwjaar 1993, dak vernieuwd december 2023). Eindstand € 2.142.248, € 262, € 361, LTV 0,52.

**Risico's.** Hoogste koopsom; appartementsrecht in een VvE die slapend is (onderhoud aan dak en gevel samen regelen, aanname € 2.500 per jaar). Lage verdiepingen (2,7 m tot de balken boven, 2,9 m beneden). Contactgeluid van de gym naar de buren in het verzamelgebouw (zwevende vloer onder de racks begroot). Tram en bus op loopafstand, station Moerwijk op 3,5 km.

## 5. Kampenringweg 7, Gouda (vervanger)

**Verificatie.** BAG-pand 0513100011130710 (1991) met één verblijfsobject, Kampenringweg 7, 485 m² industriefunctie. Geen woningen. Middelste van drie units met servicekosten (€ 375 per maand); eigen BAG-pand en eigen perceel van 570 m², dus geen uitsnede nodig. Status: bedrijfspand.com 121602, te koop € 865.000 k.k., 2 eenheden beschikbaar, bijgewerkt 13 november 2026; nu in gebruik als autobedrijf (autobrug en wasplaats).

**Site.** 16,1 x 21,6 m. Voorgevel op het noordwesten aan een parkeerhof met 5 eigen plaatsen, achterkant op het zuidoosten naar een strook aan de vaart. Begane grond 342 m² met werkplaats van 19 x 16 m en een vide van circa 6 x 9 m achter de overheaddeur; verdieping 295 m² met vier kantoren aan de voorkant en een houten entresol van 10 x 16 m achterin.

**Ontwerp.** De overheaddeur wordt een glazen pui van 6 m breed met daarachter, 6 m hoog, het café: raambar langs het glas, keuken langs de buurwand, kookeiland, lange tafel voor tien en een zeshoekige bank onder de kantoren. Entree met lockers en de bestaande trap; onder de kantoren een focuskamer, een sta-kamer en belcellen. Halverwege twee achthoekige torens: wastoren naar het café, douchetoren naar de gym. Achterin de gym (95 m²), 6 m hoog doordat de houten entresol daar weggaat, met twee racks, groepslesvloer, roeiers aan nieuwe ramen en een deur naar een terras aan de vaart. Boven: drie werkkamers en een vergaderkamer voor zes in de bestaande kantoren, en op de entresol boven de torens een stille werkzone met drie eilanden, een focuskamer en twee belcellen, met lockers en bergkasten als buffer tegen de dichte gymwand. 26 planten en 9 bomen.

**Verbetercycli.**
* Start (56 eigenaren, 30 clubleden): € 1.625.702, € 381, € 537, LTV 0,59; 34 werkplekken (knelt), belcellen 4 van 5, focus 1 van 2, bomen 6 van 9, en een lockerwand van 15 m (346 lockers, circa € 20.000 te veel).
* Cyclus 1 (werkplekken, routes, kosten): raambar van 5,6 m langs de nieuwe pui in plaats van een zitnis (43 werkplekken), focuskamer op de entresol, belcel bij de torens, lockerwand 4 m plus 10 m bergkasten, wastoren zonder lockers, fauteuils en kentia uit elkaars weg en uit de looproute naar de voordeur; 66 eigenaren. € 1.614.088, € 301, € 437, LTV 0,51. Bij 70 eigenaren knelt de derde vergaderkamer: 66 gehouden.
* Cyclus 2 (clubleden): de gym van 95 m² kan meer sporters aan dan 30 clubleden; 45 clubleden (gym op het piekuur 82 m²). Eindstand € 1.614.088, € 269, € 405, LTV 0,51.

**Risico's.** Kleinste vloer per eigenaar en twee lagen. Huidig gebruik als autobedrijf: bodemonderzoek en verwijderen van autobrug en wasplaats begroot (€ 9.500). Houten entresol: contactgeluid, daarom geen werkplekken boven de gym en de entresol daar eruit. Servicekosten en mandeligheid van het parkeerhof navragen. Station Waddinxveen Triangel op 1,7 km, Gouda op 2,4 km. Bestemming bedrijf tot categorie 3.2: afwijking nodig voor horeca en sport.

## Bestanden

* Ontwerpen: `ontwerpen_extra/schiedam-kommiezenlaan-27.py`, `rotterdam-van-riemsdijkweg-17.py`, `capelle-edelhertstraat-12.py`, `den-haag-zilverstraat-56.py`, `gouda-kampenringweg-7.py`.
* Layouts en kosten: dezelfde namen in `layout_extra/`.
* Dossiers: `dossiers/schiedam-kommiezenlaan-27.json` (uitgesneden), `rotterdam-van-riemsdijkweg-17.json`, `capelle-edelhertstraat-12.json`, `schiedam-fokkerstraat-475.json` (afgevallen), `gouda-kampenringweg-7.json`; `den-haag-zilverstraat-56.json` bestond al.
* Bronnen: oozo.nl (Kommiezenlaan 27, Van Riemsdijkweg 17, Edelhertstraat 12, Sweelincksingel 3 tot en met 7), bedrijfspand.com (Zilverstraat 56, Kampenringweg 7, met plattegronden), gemeenteblad Schiedam (melding Fokkerstraat 475, november 2024), BAG en BRK via PDOK.
