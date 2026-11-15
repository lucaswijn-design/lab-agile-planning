"""Ronde 9 (15 november 2026): breed zoeken van klein tot groot, buiten kandidaten6.py, ronde7/kandidaten7.py, ronde8/kandidaten8.py en dossiers/.
Bronnen: bedrijfspand.com (alle typen, koop 250 tot 1.600 m2, 31 plaatsen), oozo.nl (290 tot 1.450 m2, ook 15 randgemeenten) alleen als spoor,
funda in business alleen via zoekmachineresultaten (pagina's zelf niet geopend), BAG via PDOK. Zie ronde9.md.
Zelfde tupelformaat als kandidaten6.py. prijs None = prijs op aanvraag.
META[naam]: klasse (klein / middel / groot naar m2 en past()), zekerheid (A actief te koop op tweede bron, B gezien maar status onzeker),
woningen_in_pand en unit_in_complex uit BAG (verblijfsobject -> pand -> alle verblijfsobjecten), leden_* per pandadres berekend met de code en data
van ronde 7, centrum_* = dichtstbijzijnd centrum uit ronde7_wijken.json, eigenaren_past = past(m2, hoogte) uit ronde7/screen.py,
haalbaar = leden_breed >= 1,2 x eigenaren_past."""

# naam, plaats, url, prijs, m2, hoogte (m, None = onbekend), staat, opmerking, oud (lang aangeboden)
K = [
    ('Kommiezenlaan 27', 'Schiedam', 'https://www.fundainbusiness.nl/bedrijfshal/schiedam/object-89282714-kommiezenlaan-27/', 785000, 425, 4.1, 'opknappen',
     'hal 335 m2 + ca. 90 m2 kantoor op verdieping (wordt toegevoegd), nieuw dak, perceel 3.334 m2; unit in complex (BAG: pand 1950 met 8 bedrijfsunits); 0,3 km van Schiedam Centrum', False),
    ('Spaarneweg 16E', 'Cruquius', 'https://fundainbusiness.nl/bedrijfshal/cruquius/object-89248700-spaarneweg-16-e/brochure/download', 695000, 415, None, 'opknappen',
     'vrijstaand op hoek, ca. 330 m2 bedrijfsruimte + 85 m2 kantoor op begane grond (BAG 439 m2, 1985); brochure zonder datum, oozo toont het ook als huur', False),
    ('Laan van Europa 360', 'Dordrecht', 'https://www.bedrijfspand.com/bedrijfspanden/bedrijfsruimte/laan-van-europa-360-dordrecht/114492/', 795000, 453, 3.73, 'afgewerkt',
     'hoekunit 2023 in bedrijfsverzamelgebouw van 10 units: multifunctioneel 180 + 126 m2, kantoor 52 + 95 m2, 2 lagen, label A+++, min. 30% kantoor volgens bestemming', False),
    ('Roelantdreef 24', 'Utrecht', 'https://www.bedrijfspand.com/bedrijfspanden/winkelruimte/roelantdreef-24-utrecht/117117/', 575500, 361, None, 'opknappen',
     'winkel in overdekt winkelcentrum Overvecht: 218 m2 bg + 143 m2 verdieping, casco, servicekosten 657 per maand; bestemming Centrum (detailhandel, dienstverlening)', False),
    ('A. Hofmanweg 2F', 'Haarlem', 'https://www.bedrijfspand.com/bedrijfspanden/kantoorruimte/a-hofmanweg-2-f-haarlem/119042/', 975000, 510, None, 'afgewerkt',
     'kantoorpand 2000, 266 m2 bg + 244 m2 verdieping, atrium met daklicht, 8 eigen parkeerplaatsen, label A, leeg opgeleverd; geen hal', False),
    ('Dukdalfweg 55', 'Amsterdam', 'https://www.fundainbusiness.nl/en/bedrijfshal/amsterdam/object-43165490-dukdalfweg-55/brochure/download', 895000, 600, None, 'afgewerkt',
     'unit 2020 in bedrijfsverzamelgebouw Zaansepoort (8 units): 375 m2 bedrijfsruimte + 225 m2 kantoor, overheaddeur, 6 eigen + 6 gedeelde parkeerplaatsen; pont naar Zaandam', False),
    ('Edelhertstraat 12', 'Capelle aan den IJssel', 'https://www.fundainbusiness.nl/bedrijfshal/capelle-aan-den-ijssel/object-43216681-edelhertstraat-12/brochure/download', 995000, 662, None, 'opknappen',
     'vrijstaande bedrijfsruimte 1974 (BAG 619 m2), perceel 1.044 m2 eigen grond, bedrijventerrein s-Gravenland naast Rotterdam; splitsing hal/kantoor niet bekend', False),
    ('Van Riemsdijkweg 17', 'Rotterdam', 'https://www.fundainbusiness.nl/bedrijfshal/rotterdam/object-44546024-van-riemsdijkweg-17/', 895000, 717, 5.2, 'opknappen',
     '1957, 1 laag + kantoorverdieping: showroom 159 + hal 404 + kantoor 154 m2, label A+, erfpacht (canon 8.666 per jaar), perceel 690 m2, Waalhaven', False),
    ('Fokkerstraat 475', 'Schiedam', 'https://www.fundainbusiness.nl/bedrijfshal/schiedam/object-43042602-fokkerstraat-475/brochure/download', 840000, 875, None, 'opknappen',
     'bedrijfsruimte 597 m2 + entresol 113 m2 + kantoor 165 m2, perceel 1.082 m2, erfpacht tot 2091; oude advertentie, in 2024 gemelde garage-activiteit', True),
    ('Kapitein Rondairestraat 18', 'Tilburg', 'https://www.bedrijfspand.com/bedrijfspanden/bedrijfsruimte/kapitein-rondairestraat-18-tilburg/120469/', 695000, 682, 3.25, 'opknappen',
     '1969, hal ca. 566 m2 + kantoor 116 m2, lichtstraten (2022 vervangen), overheaddeur, vrije hoogte 3,25 m; Loven-Zuid naast woonwijk', False),
    ('Hastelweg 248', 'Eindhoven', 'https://www.bedrijfspand.com/bedrijfspanden/bedrijfsruimte/hastelweg-248-eindhoven/125413/', 1050000, 1555, None, 'opknappen',
     '1970, hal 1.370 m2 bg + kantoor 185 m2 verdieping, betonbouw, 3 eigen parkeerplaatsen, per direct; De Hurk naast Hastelweg 274 (ronde 8)', False),
]

META = {
    'Kommiezenlaan 27': dict(
        adres='Kommiezenlaan 27, Schiedam', klasse='klein', zekerheid='A', woningen_in_pand=False, unit_in_complex=True,
        hal_m2=335, kantoor_m2=90, bouwjaar=1950, parkeren='niet vermeld; perceel 3.334 m2', station='Schiedam Centrum', station_km=0.32,
        wijk='Schiedam Centrum/Spaland', leden_kern=168, leden_breed=245, leden_breed_auto=292, centrum_kern=159, centrum_breed=238, centrum_auto=281,
        eigenaren_past=40, haalbaar=True, gecontroleerd='2026-11-15',
        status='te koop, vraagprijs 785.000 k.k. (overzichtspagina noemt ook 775.000 en 739.000)',
        bron_status='funda in business, alleen zoekmachineresultaat: status Beschikbaar; niet op bedrijfspand.com; BAG pand 1950 met 8 verblijfsobjecten industriefunctie',
        oordeel='Beste kleine optie: hal naast station Schiedam Centrum in het op een na sterkste gebied, maar unit in een complex en hal/kantoor wordt pas afgemaakt.'),
    'Spaarneweg 16E': dict(
        adres='Spaarneweg 16E, Cruquius (Haarlemmermeer)', klasse='klein', zekerheid='B', woningen_in_pand=False, unit_in_complex=False,
        hal_m2=330, kantoor_m2=85, bouwjaar=1985, parkeren='niet vermeld', station='Heemstede-Aerdenhout', station_km=3.39,
        wijk='Haarlem Noord', leden_kern=126, leden_breed=168, leden_breed_auto=197, centrum_kern=144, centrum_breed=195, centrum_auto=220,
        eigenaren_past=35, haalbaar=True, gecontroleerd='2026-11-15', status='te koop 695.000 k.k. volgens brochure (datum onbekend)',
        bron_status='funda in business brochure via zoekmachine; oozo 55863 noemt het pand als huur (3.250 per maand)',
        oordeel='Vrijstaand en betaalbaar, gelijkvloers; ligt op een bedrijventerrein buiten Haarlem en 3,4 km van een station, status eerst nabellen.'),
    'Laan van Europa 360': dict(
        adres='Laan van Europa 360, 3317 DB Dordrecht', klasse='klein', zekerheid='A', woningen_in_pand=False, unit_in_complex=True,
        hal_m2=306, kantoor_m2=147, bouwjaar=2023, parkeren='5 eigen plaatsen + algemene bezoekersplaatsen', station='Dordrecht Zuid', station_km=2.05,
        wijk='Dordrecht Centrum/Staart', leden_kern=36, leden_breed=62, leden_breed_auto=77, centrum_kern=96, centrum_breed=157, centrum_auto=174,
        eigenaren_past=45, haalbaar=True, gecontroleerd='2026-11-15', status='te koop 795.000 k.k., 2 eenheden beschikbaar, bijgewerkt 13-11-2026',
        bron_status='bedrijfspand.com 114492 (Van Vliet Bedrijfsmakelaars); BAG eigen pand 2023, maar complex van 10 units met mandelige weg en parkeerplaatsen',
        oordeel='Nieuw en direct bruikbaar, maar 3,7 m hoog, verdeeld over twee lagen en op Amstelwijck aan de rand: het adres haalt breed maar circa 62, net genoeg voor 45.'),
    'Roelantdreef 24': dict(
        adres='Roelantdreef 24, 3562 KB Utrecht', klasse='klein', zekerheid='A', woningen_in_pand=False, unit_in_complex=True,
        hal_m2=0, kantoor_m2=0, bouwjaar=1969, parkeren='ruim gratis parkeren in de omgeving (advertentie)', station='Utrecht Overvecht', station_km=0.98,
        wijk='Utrecht Zuilen/Cartesiusweg', leden_kern=130, leden_breed=205, leden_breed_auto=226, centrum_kern=140, centrum_breed=211, centrum_auto=230,
        eigenaren_past=30, haalbaar=True, gecontroleerd='2026-11-15', status='te huur en te koop 575.500 k.k., bijgewerkt 13-11-2026',
        bron_status='bedrijfspand.com 117117 (Brecheisen); BAG eigen pandnummer zonder woningen, maar onderdeel van overdekt winkelcentrum (servicekosten)',
        oordeel='Goedkoopste instap in Utrecht met sterk gebied, maar winkelruimte in een passage, twee lagen en bestemming Centrum: alleen voor de kleinste variant.'),
    'A. Hofmanweg 2F': dict(
        adres='A. Hofmanweg 2F, 2031 BH Haarlem', klasse='middel', zekerheid='A', woningen_in_pand=False, unit_in_complex=False,
        hal_m2=0, kantoor_m2=510, bouwjaar=2000, parkeren='8 eigen parkeerplaatsen', station='Haarlem Spaarnwoude', station_km=1.98,
        wijk='Haarlem Waarderpolder', leden_kern=140, leden_breed=194, leden_breed_auto=233, centrum_kern=143, centrum_breed=192, centrum_auto=228,
        eigenaren_past=60, haalbaar=True, gecontroleerd='2026-11-15', status='te koop 975.000 k.k. en te huur, leeg opgeleverd, bijgewerkt 13-11-2026',
        bron_status='bedrijfspand.com 119042 (FRIS Bedrijfsmakelaars); BAG vrijstaand pand 590 m2 industriefunctie',
        oordeel='Instapklaar en vrijstaand met eigen parkeren in Haarlem; het is een kantoor zonder hal, dus geschikt voor coworking en café, minder voor de gym.'),
    'Dukdalfweg 55': dict(
        adres='Dukdalfweg 55, 1041 BC Amsterdam', klasse='middel', zekerheid='B', woningen_in_pand=False, unit_in_complex=True,
        hal_m2=375, kantoor_m2=225, bouwjaar=2020, parkeren='6 eigen + 6 gemeenschappelijke plaatsen', station='Zaandam', station_km=2.38,
        wijk='Zaandam Oost', leden_kern=143, leden_breed=271, leden_breed_auto=306, centrum_kern=134, centrum_breed=250, centrum_auto=290,
        eigenaren_past=75, haalbaar=True, gecontroleerd='2026-11-15', status='te koop 895.000 k.k. volgens brochure GA Makelaars (datum onbekend); oozo 15-09-2025',
        bron_status='funda in business brochure via zoekmachine; oozo Beschikbaar; BAG pand 2020 met 8 units',
        oordeel='Jonge unit met hal en kantoor en eigen parkeren tegen een lage Amsterdamse prijs; afgelegen in het havengebied, bereikbaar via de pont naar Zaandam.'),
    'Edelhertstraat 12': dict(
        adres='Edelhertstraat 12, 2901 BJ Capelle aan den IJssel', klasse='groot', zekerheid='B', woningen_in_pand=False, unit_in_complex=False,
        hal_m2=None, kantoor_m2=None, bouwjaar=1974, parkeren='niet vermeld; perceel 1.044 m2', station='Rotterdam Stadion', station_km=3.26,
        wijk='Rotterdam Kralingen-Crooswijk', leden_kern=83, leden_breed=159, leden_breed_auto=208, centrum_kern=198, centrum_breed=269, centrum_auto=309,
        eigenaren_past=85, haalbaar=True, gecontroleerd='2026-11-15', status='te koop 995.000 k.k. volgens brochure Parc Makelaars (datum onbekend); oozo sinds 19-01-2026',
        bron_status='funda in business brochure via zoekmachine; oozo Beschikbaar; BAG vrijstaand pand 619 m2',
        oordeel='Vrijstaand, eigen grond en goed geprijsd voor 85 eigenaren; ligt aan de oostrand van Rotterdam (metro Capelle), indeling en hoogte nog onbekend.'),
    'Van Riemsdijkweg 17': dict(
        adres='Van Riemsdijkweg 17, 3088 HB Rotterdam', klasse='groot', zekerheid='B', woningen_in_pand=False, unit_in_complex=False,
        hal_m2=404, kantoor_m2=154, bouwjaar=1957, parkeren='openbaar parkeren voor de deur', station='Schiedam Centrum (trein); metro niet meegeteld', station_km=5.31,
        wijk='Rotterdam West/Merwe-Vierhavens', leden_kern=62, leden_breed=144, leden_breed_auto=191, centrum_kern=171, centrum_breed=252, centrum_auto=296,
        eigenaren_past=95, haalbaar=True, gecontroleerd='2026-11-15', status='te koop 895.000 k.k., aanvaarding in overleg; in een zijbalk ook een label Onder bod',
        bron_status='funda in business object 44546024 via zoekmachine (recent object); BAG pand 1957 met 2 verblijfsobjecten, geen woningen',
        oordeel='Ruim en goedkoop voor groot met 5,2 m hal, maar Waalhaven ligt ver van treinstations en de kern rond het adres is dun (circa 62).'),
    'Fokkerstraat 475': dict(
        adres='Fokkerstraat 475, 3125 BD Schiedam', klasse='groot', zekerheid='B', woningen_in_pand=False, unit_in_complex=False,
        hal_m2=597, kantoor_m2=165, bouwjaar=1992, parkeren='niet vermeld; perceel 1.082 m2', station='Schiedam Centrum', station_km=1.78,
        wijk='Schiedam Centrum/Spaland', leden_kern=156, leden_breed=231, leden_breed_auto=285, centrum_kern=159, centrum_breed=238, centrum_auto=281,
        eigenaren_past=100, haalbaar=True, gecontroleerd='2026-11-15', status='vraagprijs 840.000 k.k. (verlaagd van 875.000) in een oude brochure; status onbekend',
        bron_status='funda in business brochure via zoekmachine (oud objectnummer); gemeentelijke melding 2024 van een garagebedrijf op dit adres; BAG vrijstaand pand 536 m2',
        oordeel='Op papier de beste groot-kandidaat (875 m2, 100 eigenaren, sterk gebied, laag bedrag), maar de advertentie is oud: eerst bellen of het nog te koop is.'),
    'Kapitein Rondairestraat 18': dict(
        adres='Kapitein Rondairestraat 18, 5015 BC Tilburg', klasse='groot', zekerheid='A', woningen_in_pand=False, unit_in_complex=False,
        hal_m2=566, kantoor_m2=116, bouwjaar=1969, parkeren='voldoende gratis parkeren in de omgeving', station='Tilburg', station_km=2.13,
        wijk='Tilburg Noord/Loven', leden_kern=61, leden_breed=83, leden_breed_auto=97, centrum_kern=65, centrum_breed=86, centrum_auto=98,
        eigenaren_past=90, haalbaar=False, gecontroleerd='2026-11-15', status='te koop 695.000 k.k., beschikbaar vanaf 1 maart 2026, bijgewerkt 14-11-2026',
        bron_status='bedrijfspand.com 120469 (Naber); BAG vrijstaand pand 683 m2',
        oordeel='Gebouw past bij 90 eigenaren maar Tilburg levert breed circa 83: alleen als middel club (circa 65 tot 70) die een deel van de hal verhuurt.'),
    'Hastelweg 248': dict(
        adres='Hastelweg 248, 5652 CN Eindhoven', klasse='groot', zekerheid='A', woningen_in_pand=False, unit_in_complex=True,
        hal_m2=1370, kantoor_m2=185, bouwjaar=1970, parkeren='3 eigen plaatsen + parkeerhavens aan de weg', station='Eindhoven Strijp-S', station_km=2.02,
        wijk='Eindhoven Strijp', leden_kern=64, leden_breed=106, leden_breed_auto=119, centrum_kern=73, centrum_breed=115, centrum_auto=126,
        eigenaren_past=100, haalbaar=False, gecontroleerd='2026-11-15', status='te koop 1.050.000 k.k., per direct, 2 eenheden beschikbaar, bijgewerkt 13-11-2026',
        bron_status='bedrijfspand.com 125413 (Q Bedrijfslocaties); BAG pand met 2 verblijfsobjecten (industrie en winkel)',
        oordeel='Veel hal voor weinig geld, maar breed circa 106 haalt de 120 voor 100 eigenaren niet en de hal is groter dan nodig.'),
}
