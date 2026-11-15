# Ronde 9: vijf panden uitgewerkt (Noord-Holland, Utrecht en Dordrecht)

Uitgewerkt op 15 en 16 november 2026 volgens `inrichting/BRIEF_ONTWERP.md`. Per pand een ontwerp in `ontwerpen_extra/<slug>.py`, een layout met kosten in `layout_extra/<slug>.py` en een dossier in `dossiers/<slug>.json`.
Alle kosten zijn sober doorgerekend met `pand_case.run(slug, torens=True, sober=True)` en `pand_case.fee_inleg_terug(...)`. Alle normen van `inrichting/programma.py` worden gehaald (belcellen, focuskamers, lounge, lockers, planten, bomen).

Roelantdreef 24 in Utrecht valt af: het winkelpand zit wand aan wand aan het hoofdgebouw van winkelcentrum Overvecht, waarin 19 woningen zitten. Vervanger is Amsterdamsestraatweg 656D, ook in Utrecht.

## Overzicht

| Pand | Alles in | Om te draaien (vol lid per maand) | Inleg terug | LTV | Werkplekken | Max eigenaren | Gekozen eigenaren | Verzorgingsgebied breed |
|---|---|---|---|---|---|---|---|---|
| Spaarneweg 16E, Cruquius | € 1.434.127 | € 470 | € 663 | 0,65 | 28 | 47 | 42 (21 vol, 21 deeltijd) + 30 clubleden | 168 (4,0 x) |
| A. Hofmanweg 2F, Haarlem | € 1.636.307 | € 407 | € 536 | 0,62 | 31 | 52 | 52 (26 + 26) + 30 | 194 (3,7 x) |
| Dukdalfweg 55, Amsterdam Noord | € 1.569.728 | € 265 | € 374 | 0,43 | 45 | 76 | 74 (37 + 37) + 30 | 271 (3,7 x) |
| Laan van Europa 360, Dordrecht | € 1.391.679 | € 396 | € 532 | 0,59 | 34 | 57 (gebied: 51) | 48 (24 + 24) + 30 | 62 (1,29 x) |
| Amsterdamsestraatweg 656D, Utrecht (vervangt Roelantdreef 24) | € 1.759.719 | € 262 | € 386 | 0,45 | 57 | 96 (toiletten knellen boven 80) | 80 (40 + 40) + 30 | 202 (2,5 x) |

Max eigenaren is `capaciteit.max_leden(slug, 0.5, 30)`. Het verzorgingsgebied komt uit META `leden_breed` van ronde 9 (Amsterdamsestraatweg uit ronde 7); in alle gevallen is het minstens 1,2 x het gekozen aantal eigenaren.

## Statuscheck en vervanging

* Gecontroleerd met zoekmachines (funda niet geopend) en de pagina's van bedrijfspand.com op 15 november 2026.
* Roelantdreef 24: te koop € 575.500 k.k. en te huur (bedrijfspand.com 117117, bijgewerkt 13-11-2026). Het eigen BAG-pand 0344100000034276 (1969, 216 m², één verblijfsobject winkel en industrie) heeft geen woningen, maar ligt op 0,0 m tegen hoofdpand 0344100000011463 van hetzelfde winkelcentrum (1969, 3.258 m², 33 verblijfsobjecten, waarvan 19 met woonfunctie: Zamenhofdreef 77 en 77A tot en met 77V, adrespunten op 21 tot 29 m van het hart van de unit). Eén aaneengesloten constructie met gedeelde servicekosten, dus geluid van de gym loopt via de constructie naar de woningen. Daarnaast erfpacht tot 20-03-2043 en bestemming Centrum (detailhandel en dienstverlening). Afgevallen.
* Vervangers getoetst in de BAG: Volmerstraat 5 Diemen (verblijfsobject met industrie- en woonfunctie, af), Rosmolenstraat 32A Zaandam (pand uit 1920 met een woning, af), Izaak Enschedeweg 46 Haarlem (geen woningen, maar zelfde verzorgingsgebied als Hofmanweg en geen actuele advertentie gevonden), Amsterdamsestraatweg 656D Utrecht (geen woningen, zelfde verzorgingsgebied als Roelantdreef). Gekozen: Amsterdamsestraatweg 656D.

## 1. Spaarneweg 16E, Cruquius

**Verificatie.** BAG-pand 0394100000228230 (1985) met één verblijfsobject, Spaarneweg 16E, 439 m² industriefunctie. Geen woningen in het pand. Het buurpand Spaarneweg 16C en 16D (2001) ligt op 3,74 m aan de zuidwestkop en heeft twee bedrijfswoningen (16C1 en 16D1, elk 125 m²); de bedrijfshal achter ligt op 5 m. Status: de funda in business brochure noemt het pand te koop (vraagprijs € 695.000 volgens ronde 9), oozo toont het als huur (€ 3.250 per maand, beschikbaar vanaf 1 juli 2026) en noemt bouwjaar 2005. Status onzeker: eerst nabellen.

**Site.** Vrijstaand op een hoek, 25 x 17 m, circa 4,8 m tot het dak. Straatgevel aan de Spaarneweg op het zuidoosten (zon), eigen erf met parkeren aan de noordoostkop, blind naar de buren.

**Ontwerp.** Eén laag, van zweet naar stilte. Gym aan de noordoostkop (82 m²) met een eigen deur op het erf, twee lage racks, roeiers, matvloer en een D-vormige douchetoren; daarnaast de achthoekige wastoren met lockers, een lockerwand en de techniek als buffer. Midden aan de straat het café met een lange tafel voor twaalf aan nieuw glas, zeshoekige bank, zitnis tegen een boekenwand, keuken en kookeiland, en een smal terras op het zuidoosten. Achter een glazen wand van oude ramen de werkzone met vier eilanden haaks op het straatglas, en achterin een vergaderkamer voor zes, een sta-kamer, een focuskamer en vier belcellen. 22 planten en 8 bomen (ficus en strelitzia aan het glas, kentia in het donker).

**Verbetercycli.**
* Start (36 eigenaren): alles in € 1.439.185, om te draaien € 569, inleg terug € 789, LTV 0,70.
* Cyclus 1 (routes, botsingen, daglicht, eigenaren): garderobe stond in de ingang van de wastoren en is verplaatst; voordeur verschoven naar een vrije zone van 2 m tussen lange tafel en toren; werkzone 0,5 m breder zodat het pad tussen de eilanden 1,5 m wordt; vierde belcel; bomen weg van toren en gevel; extra kentia in de donkere achterkant van het café; 42 eigenaren. Resultaat € 1.442.406, € 472, € 667, LTV 0,65.
* Cyclus 2 (kosten en geluid): gymglas aan het erf als hergebruikt kozijn in plaats van aluminium (circa € 7.000 minder); geluid gecontroleerd: gym op meer dan 22 m van de bedrijfswoningen en 12 m van de werkzone, met wastoren en lockers ertussen. 46 eigenaren doorgerekend (€ 420) maar dat vraagt een tweede focuskamer en vult alle 28 werkplekken: 42 gehouden. Eindstand € 1.434.127, € 470, € 663, LTV 0,65.

**Risico's.** Koop of huur onduidelijk; bedrijventerrein buiten Haarlem op 3,4 km van een station; bedrijfswoningen op 3,7 m (gym bewust aan de andere kant); lage hal (racks zonder optrekstang); asbestreserve (bouwjaar voor 1994); omgevingsplan bedrijventerrein vraagt een afwijking; hoogste maandbedrag van de vijf.

## 2. A. Hofmanweg 2F, Haarlem

**Verificatie.** BAG-pand 0392100000061555 (2000) met één verblijfsobject, A. Hofmanweg 2F, 590 m² industriefunctie. Geen woningen. Anders dan META zegt is het niet vrijstaand: het is aan drie kanten aangebouwd tegen panden uit 2000, 2001, 2020 en 2025, alle industrie of kantoor. Status: bedrijfspand.com 119042 (FRIS Bedrijfsmakelaars), online sinds 06-05-2026, bijgewerkt 13-11-2026, te koop € 975.000 k.k. en te huur; bij koop leeg opgeleverd, aanvaarding in overleg (bij huur wordt onderverhuur tot en met 31-12-2027 genoemd). Zoekmachines vonden geen tweede bron voor nummer 2F.

**Site.** 21 x 15 m op twee lagen (266 + 244 m²), circa 6,5 m tot het dak, dus circa 2,9 m vrij zonder systeemplafond. Alleen de zuidgevel aan het eigen parkeerterrein (8 plaatsen) is vrij; achterin een trappenhuis met daklichtkoepel.

**Ontwerp.** Lage plafonds zijn het uitgangspunt: torens van 2,5 m, lage racks zonder optrekstang, bomen tot 2,8 m, hangplanten op 2,4 m, geen hanglampen boven paden. Beneden aan het zuidglas het café met zitnis, lange tafel, keuken en kookeiland, en ernaast de gym (82 m²) met een eigen deur naar buiten en een achthoekige douchetoren. Achterin het atrium met kentia onder het daklicht, de lockerwand, de wastoren en opslag. Boven de gym de lounge en bieb (zeshoekige bank, zitnis aan het raam, boekenwand); boven het café de werkzone met een raambar van 6,6 m en twee eilanden; achterin rond de vide een vergaderkamer voor zes, een sta-kamer, twee focuskamers en vier belcellen. Terras van 27 m² op twee parkeerplaatsen.

**Verbetercycli.**
* Start (50 eigenaren): € 1.650.580, € 431, € 566, LTV 0,64; planten 24 van 29, bomen 5 van 10, lockers 70 van 72.
* Cyclus 1 (botsingen, routes, groen): een label stond op de verkeerde laag; kookeiland en lange tafel verschoven zodat er 1,1 m tussen zit; tien bomen die onder 2,9 m passen (dracaena, ficus, schefflera); lockers in een zijde van de wastoren; 52 eigenaren. € 1.650.820, € 410, € 541, LTV 0,62.
* Cyclus 2 (kosten, daglicht): de zuidgevel heeft al ramen, dus nieuwe pui alleen voor de gymdeur met zijlicht (8 m²) en de caféentree (6 m²) in plaats van 20 m²; daglicht gecontroleerd: de raambar pakt de beste plek, de eilanden staan 4 tot 7 m van het glas en dat kan in dit diepe pand niet beter. Eindstand € 1.636.307, € 407, € 536, LTV 0,62.

**Risico's.** Lage plafonds (gym beperkt, geen springen voor 7:00); diep pand met één gevel; lounge op een betonvloer boven de gym (contactgeluid); hoge prijs per m²; drie Haarlemse kandidaten delen hetzelfde gebied; bestemming bedrijventerrein Waarderpolder.

## 3. Dukdalfweg 55, Amsterdam Noord

**Verificatie.** BAG-pand 0363100012250919 (2020) met acht verblijfsobjecten (Dukdalfweg 49 tot en met 55 en Westhavenweg 115 tot en met 121), alle industrie- en kantoorfunctie. Geen woningen. Unit 55 is 621 m². Uitsnede: noordoosthoek van het complex, 26,5 x 15,6 m (412 m² footprint), westgrens op een hoekpunt in de noordgevel, zuidgrens uit de adrespunten van de buren en de som 412 m² + circa 208 m² kantoorverdieping = 621 m²; footprint_complex bewaard, rest van het complex als context, vijf gesloopte BAG-panden uit 2000 en 2001 uit de context gehaald (zie `opmerking` in het dossier). Status: brochure GA Makelaars via zoekmachine, te koop € 895.000 k.k., 375 m² hal en 225 m² kantoor op de eerste verdieping en entresol; volgens de brochure is toestemming van Haven Amsterdam nodig voor verkoop of verhuur. Geen datum.

**Site.** Noordgevel aan de Dukdalfweg en het parkeerterrein, oostgevel (vrij over 15,6 m) aan het binnenterrein, overige zijden tegen buurunits. Circa 9,5 m tot het dak.

**Ontwerp.** Beneden achter de noordgevel het café met lange tafel, zitnis langs de oostramen, keuken van 5,6 m en kookeiland. Onder de verdieping de achthoekige wastoren, lockerwand, garderobe en techniek als buffer. Daarachter onder de volle hoogte een lounge met zeshoekige bank, boekenwand, strelitzia en olijf onder lichtkoepels, en achterin de gym (103 m²) met drie racks met optrekstang, roeiers, matvloer en douchetoren, achter een dichte wand tot het dak. Sporters komen via een nieuwe zijdeur in de oostgevel. Boven in het kantoor de werkzone met een raambar van 13 m aan het noordglas (geen schittering) en drie eilanden; op de entresol twee vergaderkamers voor zes, een sta-kamer, twee focuskamers en zes belcellen als dichte dozen langs de rand.

**Verbetercycli.**
* Start (70 eigenaren): € 1.571.383, € 288, € 401, LTV 0,47; planten 25 van 31, bomen 9 van 11.
* Cyclus 1 (botsingen, routes): de zitnis aan de oostgevel stond naar buiten gedraaid; de trap kwam boven uit in een vergaderkamer en is verplaatst naar het looppad van de werkzone; strelitzia stond op een zitnis en de olijf tegen de gymwand; roeiers los van de lockerwand; groen op norm.
* Cyclus 2 (eigenaren, dode ruimte): de zitnis in de lounge vervangen door groen (lounge 20 van 15 plekken was ruim genoeg); 74 eigenaren (44 van 45 werkplekken). Eindstand € 1.569.728, € 265, € 374, LTV 0,43.

**Risico's.** Erfpacht van Havenbedrijf Amsterdam (canon aangenomen op € 10.000 per jaar) en toestemming bij verkoop; havenbestemming laat een club met horeca en sport mogelijk niet toe; unitgrens en indeling aangenomen; status niet bevestigd; afgelegen (pont naar Zaandam, 2,4 km van station Zaandam); VvE (aangenomen € 4.000); gym zonder eigen buitendeur op de gym zelf.

## 4. Laan van Europa 360, Dordrecht

**Verificatie.** Eigen BAG-pand 0505100000070365 (2023, 238 m²), één verblijfsobject van 415 m² industrie- en kantoorfunctie; de aangebouwde buren 340 en 370 idem. Geen woningen in het complex van 10 units. Geen uitsnede nodig. Status: bedrijfspand.com 114492 (Van Vliet Bedrijfsmakelaars), te koop € 795.000 k.k. (huur € 4.750 per maand), twee eenheden beschikbaar, bijgewerkt 13-11-2026; zoekmachine vindt ook de funda in business brochure.

**Site.** 28 x 9,1 m op twee lagen van 3,73 en 3,80 m vrij, schuine voorgevel op het zuidzuidwesten met kantoren en overheaddeur, lange zijgevel op het oostzuidoosten met ramen en een extra entree, lichtstraat boven de verdieping, 5 eigen parkeerplaatsen.

**Ontwerp.** Beneden achter een nieuwe glazen pui op de plek van de overheaddeur het café met een lange tafel aan de zijramen, keuken, kookeiland en de trap. Halverwege de wastoren met lockers in twee zijden, met langs de zijramen de gang naar de gym. Achterin de gym (98 m²) met een eigen deur in de zijgevel (bestaande extra entree), twee racks, roeiers, matvloer en een D-vormige douchetoren tegen de buurwand. Boven aan de voorkant de werkzone (raambar van 8,8 m en twee eilanden), onder de lichtstraat twee focuskamers, vier belcellen en lockers, en boven de gym de lounge met zeshoekige bank, zitnis, boekenwand, een vergaderkamer voor zes en een sta-kamer.

**Verbetercycli.**
* Start (48 eigenaren): € 1.391.679, € 396, € 532, LTV 0,59; planten 20 van 23, bomen 5 van 8.
* Cyclus 1 (daglicht, groen): eilanden 1 m dichter bij de zijramen (bureaus 3 tot 5,8 m van het glas in plaats van 4 tot 6,8 m) met 1,4 m looppad achter de raambar; drie bomen en vier planten erbij; langere zonenamen ingekort.
* Cyclus 2 (eigenaren en kosten): 44, 48 en 50 eigenaren doorgerekend (€ 443, € 396, € 375). Bij 50 haalt het gebied (62) maar 1,24 x, dus 48 gehouden. Er valt weinig te schrappen: het pand is nieuw, er wordt alleen ingericht. Eindstand € 1.391.679, € 396, € 532, LTV 0,59.

**Risico's.** Dun verzorgingsgebied (62 breed, kern 36); alleen 3,7 m hoog; gym op een betonvloer onder lounge en vergaderen; bestemming kantoor en bedrijf categorie 1 tot 3 met minimaal 30% kantoor (sport en horeca nakijken); mandelige weg, groen en parkeren (bijdrage aangenomen op € 2.500); ligt in Zuid-Holland, buiten de focus Noord-Holland, Utrecht en Noord-Brabant.

## 5. Amsterdamsestraatweg 656D, Utrecht (vervangt Roelantdreef 24)

**Verificatie.** BAG-pand 0344100000047609 (2003) met twee verblijfsobjecten: 656D (1.020 m²) en Martin-ovenweg 19 (3.402 m²), beide industriefunctie. Geen woningen in het pand; panden binnen 3 m zijn bedrijfspanden (industrie, winkel, overige). Uitsnede: de lichte strook van 23 m breed aan de straatkant, oostgrens aangenomen op 46 m (circa 1.060 m² begane grond, past met de kantoorlaag bij vbo 1.020 m² en de advertentie van 1.089 m²); rest van de strook en de hal van Martin-ovenweg 19 als context. Status: alleen oozo (ronde 7: beschikbaar, online sinds 20-03-2025, € 925.000); zoekmachine vond geen nieuwere bron. Eerst nabellen.

**Site.** Straatkop op het noordoosten aan de Amsterdamsestraatweg (woningen aan de overkant op circa 40 m van de gym), lange gevel op het zuidoosten aan een binnenterrein, blinde gevel op 1,6 m van een bedrijfshal, circa 7,1 m tot het dak.

**Ontwerp.** Aan de straat de entree met twee lockerwanden, garderobe en trap naar de bieb op de kantoorverdieping (drie focuskamers, vier belcellen, boekenwand). Dan het café langs het zonnige glas (lange tafel, zitnis, zeshoekige bank, boekenwand, keuken van 6 m, kookeiland) en tafeltennis aan de blinde kant, met terras op het binnenterrein. Daarna de werkzone met zes eilanden onder acht nieuwe lichtkoepels en een raambar van 13 m, een rij kentia's als groene buffer, en langs de blinde gevel twee vergaderkamers voor zes, een sta-kamer en vier belcellen. Een band van 4,8 m met wastoren, toiletgroep en techniek scheidt werken van sporten. Achterin de gym (141 m²) met vier racks, roeiers, matvloer en douchetoren, eigen deur naar het binnenterrein, en een studio van 74 m² voor yoga en groepslessen.

**Verbetercycli.**
* Start (100 eigenaren, negen eilanden): € 1.772.181, € 188, inleg terug onmogelijk (verkoopwaarde na vijf jaar lager dan € 1,2 mln inleg), LTV 0,32; toiletten knellen (5 nodig, 4 geteld).
* Cyclus 1 (daglicht, dode ruimte, groen): de donkerste rij eilanden (10 m van het glas) eruit en vervangen door een plantenbak met kentia's; groen op norm (55 planten, 19 bomen); dubbele roeier en een monstera op de keuken opgelost.
* Cyclus 2 (eigenaren en kosten): 60 tot 100 eigenaren doorgerekend; bij 90 (€ 222, inleg € 339) knellen de toiletten, bij 100 komt de inleg niet terug. 80 gekozen: € 1.759.719, € 262, € 386, LTV 0,45.

**Risico's.** Status onzeker (advertentie van maart 2025); unitgrens en kantoorindeling aangenomen; pand gedeeld met Martin-ovenweg 19 (splitsing en VvE, aangenomen € 3.000); vrije hoogte niet bekend (6 m aangenomen); diep pand leunt op lichtkoepels; erfpacht niet bekend (in Utrecht vaak erfpacht); woningen aan de overkant van de straat; bestemming nakijken.

## Wat er is aangemaakt

* Ontwerpen: `ontwerpen_extra/cruquius-spaarneweg-16e.py`, `haarlem-hofmanweg-2f.py`, `amsterdam-dukdalfweg-55.py`, `dordrecht-laan-van-europa-360.py`, `utrecht-amsterdamsestraatweg-656d.py`.
* Layouts met kosten: dezelfde namen in `layout_extra/`.
* Dossiers via `fetch.haal` voor alle zes adressen; Dukdalfweg 55 en Amsterdamsestraatweg 656D uitgesneden uit hun complex (footprint_complex en opmerking in het dossier). Het dossier van Roelantdreef 24 blijft staan zonder ontwerp.
* Gecontroleerd met `python3 ontwerp.py`, `python3 tekening.py`, `python3 build_ontwerpen.py`, `python3 inrichting/programma.py` en `capaciteit.max_leden(slug, 0.5, 30)`; plattegronden per laag als png bekeken en botsingen opgelost.
