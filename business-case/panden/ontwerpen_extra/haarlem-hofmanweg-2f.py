# ---------------------------------------------------------------- Ronde 9 (15 november 2026): A. Hofmanweg 2F, Haarlem Waarderpolder
# Kantoorpand uit 2000 van 21 x 15 m op twee lagen (BAG 590 m² industriefunctie, 1 verblijfsobject; advertentie 266 m² bg + 244 m² verdieping, label A),
# circa 6,5 m tot het dak (3D BAG): twee lagen van circa 3,2 m, na het weghalen van het systeemplafond circa 2,9 m vrij. Lage plafonds: geen racks met optrekstang,
# torens van 2,5 m, geen hanglampen boven looppaden, hangplanten op 2,4 m.
# u = 21 is de enige vrije gevel (zuid, aan het eigen parkeerterrein en de A. Hofmanweg); noord (u = 0), west (v = 0) en oost (v = 15) zijn aangebouwd tegen
# bedrijfspanden uit 2000, 2001 en 2025 (alle industriefunctie, geen woningen). Het trappenhuis met daklichtkoepel staat achterin (u 1 tot 6, v 5 tot 10, uit de luchtfoto).
_HL = 1  # verdieping
HOFMAN = dict(
    titel="A. Hofmanweg 2F, Haarlem",
    sub="Instapklaar kantoorpand uit 2000 op twee lagen van 21 x 15 m met atrium en daklicht, 8 eigen parkeerplaatsen, 2 km van station Haarlem Spaarnwoude. Te koop en te huur, bijgewerkt 13-11-2026.",
    hoogte=6.5, niveaus={"1": 3.25}, pui_h=2.6,
    concept="Een kantoor zonder hal wordt een club op twee lagen rond het bestaande atrium. Beneden aan de zonnige parkeerkant het café met keuken, kookeiland, "
            "een lange tafel en een zitnis aan het glas, en ernaast de gym achter een dichte wand met een eigen deur naar buiten. Achterin, onder de daklichtkoepel, "
            "het atrium met de trap, een kentia en de lockerwand, en de achthoekige wastoren. Boven, boven de gym, de lounge en bieb met een zeshoekige bank; "
            "boven het café de werkzone met een raambar aan het zuidglas. Achterin boven: vergaderkamer, sta-kamer, twee focuskamers en belcellen rond de vide. "
            "Sober: systeemplafonds eruit (circa 30 cm meer hoogte), beton en staal zichtbaar, kantoorwanden hergebruikt als glaswanden.",
    geluid="Geen woningen in of naast het pand. De gym ligt beneden aan de straatkant, achter een dichte akoestische wand tot de verdiepingsvloer en een deur op toegangspas, "
           "met 40 mm rubber op een akoestische ondervloer en platforms. Boven de gym de lounge (volgorde gym, lounge, werken), met tussen lounge en werkzone een boekenwand en glas. "
           "Lage plafonds: houtwolplaten tegen het betonplafond, stoffen panelen op de wanden, geen groepslessen met springen voor 7:00.",
    pui=[[[21.0, 0.3], [21.0, 14.8]]],
    zones=[
        zone("Café en keuken aan het zuidglas", "café", R(6.4, 7.8, 20.8, 14.8),
             "Door de nieuwe glazen deur aan het parkeerterrein kom je in het café: een zitnis met twee tafeltjes langs het zuidglas, een lange tafel voor twaalf, "
             "achterin een keuken van 5 m tegen de buurwand met een kookeiland en de espressomachine. Strelitzia aan het glas, pothos boven de tafel op 2,4 m.",
             ["Zitnis van 4 m aan het zuidglas", "Lange tafel van 4,2 m voor twaalf", "Keuken van 5 m en kookeiland met espressomachine", "Terras van 27 m² op twee parkeerplaatsen"],
             cam=dict(t=[14.0, 11.3], afstand=9, hoek=180),
             prompt="The café of a members club inside a simple office building from 2000 with a low ceiling of 2.9 m, the suspended ceiling removed so the concrete slab shows: "
                    "a built-in olive green bench with small tables along a sunny glass front, a long oak table for twelve, an olive green kitchen from second-hand stainless steel worktables "
                    "against the side wall, a reclaimed wood island with an espresso machine, a strelitzia at the glass, pothos trailing from a low steel rail."),
        zone("Atrium, trap en lockers", "entree", R(0.2, 4.8, 6.4, 10.2),
             "Het bestaande trappenhuis met daklichtkoepel wordt het hart van de achterkant: een kentia onder het daklicht, de lockerwand langs de achterwand en de trap naar boven.",
             ["Daklichtkoepel en vide blijven", "Lockerwand van 4,4 m (circa 70 lockers) met pothos erop", "Kentia van 3 m onder het daklicht"],
             cam=dict(t=[3.0, 7.5], afstand=6, hoek=0),
             prompt="A small atrium at the back of an office building from 2000, a round roof light above a two storey void, a black steel stair, a tall kentia palm under the roof light, "
                    "a dark green locker wall with trailing pothos on top, smooth sealed concrete floor, warm light."),
        zone("Wastoren", "sanitair", R(0.2, 0.2, 6.4, 4.8),
             "Een achthoekige wastoren van 4,6 m met drie toiletten en een V-wastrog, open naar de gang, 2,5 m hoog onder het lage plafond.",
             ["Wastoren met drie toiletten", "Techniek achterin rechts: warmtepomp, ventilatie, meterkast"],
             cam=dict(t=[3.3, 2.6], afstand=6, hoek=0),
             prompt="A low octagonal concrete-look bathroom tower (eight flat faces), 2.5 m high under a 2.9 m concrete ceiling, board-marked plaster, a V-shaped concrete wash trough with brass taps, "
                    "ivy along the top rim, inside a simple office building."),
        zone("Gang", "sanitair", R(6.4, 0.2, 10.0, 7.8),
             "Tussen wastoren en gym: de garderobe, een bank om schoenen te wisselen en de deur op toegangspas.",
             ["Garderobe en wisselbank", "Deur op toegangspas"], cam=dict(t=[8.2, 4.0], afstand=5, hoek=0),
             prompt="A short corridor in a simple office building with a coat rack made of steel pipes, a wooden bench, a solid door with a card reader, a zz plant."),
        zone("Opslag", "techniek", R(0.2, 10.2, 6.4, 14.8),
             "Achterin rechts: techniek, opslag voor de gym en het café, en een plek voor fietsonderhoud.",
             ["Warmtepomp, ventilatie, meterkast", "Opslag stoelen, matten, voorraad café"], cam=dict(t=[3.3, 12.5], afstand=5, hoek=0),
             prompt="A tidy storage and plant room in an office building, steel shelving, a heat pump unit, bike tools on a wall board."),
        zone("Gym (eigen deur)", "gym", R(10.0, 0.2, 20.8, 7.8),
             "Beneden aan de zuidkant, met een eigen deur naar het parkeerterrein: twee lage racks op platforms (2,3 m, geen optrekstang), twee roeiers, een matvloer, "
             "kettlebells en de douchetoren in de hoek. Dichte wand tot de vloer erboven en een deur op toegangspas.",
             ["Twee lage racks op zwevende platforms", "Twee roeiers en kettlebells", "Matvloer van 4,8 x 2,6 m", "Achthoekige douchetoren met vier douches", "Eigen deur op toegangspas"],
             cam=dict(t=[16.0, 4.0], afstand=8, hoek=180),
             prompt="A compact functional gym inside an office building with a low 2.9 m concrete ceiling: two low black squat racks on oak platforms, rowing machines, kettlebells, "
                    "anthracite rubber floor, one wall oxblood red, a low octagonal concrete-look shower tower in the corner, big windows to a sunny parking lot, a sansevieria."),
        dict(zone("Lounge en bieb boven de gym", "bieb", R(10.0, 0.2, 20.8, 7.8),
                  "Boven de gym, aan het zuidglas: een zeshoekige bank rond een sfeerhaard, een zitnis langs het raam, een boekenwand van 4 m en twee fauteuils. "
                  "De lounge buffert tussen de gym beneden en de werkzone ernaast.",
                  ["Zeshoekige bank rond een sfeerhaard", "Zitnis van 6,4 m langs het zuidglas", "Boekenwand van 4 m", "Ficus aan het glas"], n=1,
                  cam=dict(t=[15.0, 4.0], afstand=8, hoek=180),
                  prompt="A calm lounge and library on the first floor of an office building from 2000, low 2.9 m concrete ceiling with wood wool panels, a hexagonal olive velvet bench around a fireplace, "
                         "a long built-in bench along a sunny window, a walnut bookcase wall, two butter yellow armchairs, a ficus at the glass."), tussenvloer=False),
        dict(zone("Werkzone aan het zuidglas", "werken", R(10.0, 7.8, 20.8, 14.8),
                  "Boven het café: een raambar van 6,6 m pal achter het zuidglas en drie eilanden van vier zit-sta bureaus met de schermen haaks op het raam.",
                  ["Raambar van 6,6 m (11 krukken)", "Drie eilanden van vier bureaus 140 x 70", "Glaswand met boekenkasten naar de lounge"], n=1,
                  cam=dict(t=[15.0, 11.3], afstand=8, hoek=180),
                  prompt="A coworking room on the first floor of an office building from 2000 with a low concrete ceiling: a long oak window bar along a sunny glass front, three islands of four compact sit-stand desks, "
                         "slate blue chairs, wood wool acoustic panels on the ceiling, a glass wall of reclaimed windows to a lounge, pothos on a low rail."), tussenvloer=False),
        dict(zone("Stille kamers rond de vide", "vergader", [[0.2, 0.2], [10.0, 0.2], [10.0, 14.8], [0.2, 14.8], [0.2, 10.2], [4.7, 10.2], [4.7, 4.8], [0.2, 4.8]],
                  "Achterin boven, rond de vide met het daklicht: een vergaderkamer voor zes, een sta-kamer, twee focuskamers en vier belcellen.",
                  ["Vergaderkamer voor 6", "Sta-kamer voor 5", "Twee focuskamers", "Vier belcellen"], n=1, cam=dict(t=[5.0, 7.5], afstand=7, hoek=0),
                  prompt="The quiet back of the first floor of an office building around a void with a round roof light: a meeting room for six behind reclaimed windows, a standing meeting room, "
                         "two tiny glass focus rooms, round felt phone booths, a glass balustrade with trailing pothos."), tussenvloer=False),
    ],
    buiten=[dict(naam="Terras op het zuiden", poly=R(21.2, 7.8, 25.0, 14.8), kleur="#d5bd96"),
            dict(naam="Parkeerplaats en groen", poly=R(21.2, 0.0, 36.0, 15.0), kleur="#c9c3b6")],
    elementen=[
        # begane grond: wastoren, atrium, techniek
        *achthoektoren([3.2, 2.6], 2.3, 0, "was", lockers=(2,), H=2.5), *lockerwand([0.45, 7.5], 4.6, 90, h=2.0), boom3([2.6, 7.5], "kentia"),
        dict(t="box", soort="trap", c=[5.4, 7.2], w=1.2, d=4.4, h=0.3, a=0, kleur=STAAL), label([5.4, 4.6], "trap"),
        dict(t="box", soort="techniek", c=[1.8, 13.2], w=3.0, d=2.8, h=2.4, a=0, kleur="#8f8a80"), label([1.8, 13.2], "techniek"),
        *kasten(3.6, 6.2, 14.55, d=0.4, h=2.2, kleur=STAAL), plant3([5.6, 11.0], "aspidistra"),
        # gang naar de gym
        dict(t="box", soort="garderobe", c=[6.65, 4.0], w=3.0, d=0.4, h=1.8, a=90, kleur=WALNOOT), dict(t="box", soort="bank", c=[9.6, 3.0], w=1.6, d=0.4, h=0.45, a=90, kleur=HOUT),
        plant3([7.4, 1.0], "zz-plant"), plant3([9.4, 7.2], "sansevieria"), boom3([7.1, 6.9], "dracaena"), plant3([5.8, 13.4], "sansevieria"),
        wand([[10.0, 0.2], [10.0, 4.4]], 3.2, gym=True), deur([10.0, 5.0], 90, toegang=True), wand([[10.0, 5.6], [10.0, 7.8], [21.0, 7.8]], 3.2, gym=True),
        # gym
        *achthoektoren([12.4, 2.6], 2.1, 90, "douche", H=2.5), *rack([19.4, 1.6], 0), *rack([16.5, 1.6], 0),
        roeier([12.9, 6.9], 0), roeier([16.0, 6.9], 0), dict(t="kleed", c=[17.9, 4.8], w=4.8, d=2.6, a=0, kleur="#c7928a"), label([17.9, 4.8], "matvloer"), hangplant([17.9, 4.8], 2.4),
        dict(t="box", soort="kettlebells", c=[20.45, 4.7], w=1.8, d=0.5, h=0.9, a=90, kleur=STAAL), deur([21.0, 6.8], 90, toegang=True),
        plant3([14.8, 5.0], "sansevieria"), boom3([11.0, 6.6], "dracaena"),
        # café
        deur([21.0, 13.9], 90, w=1.2), *zitnis([20.8, 8.1], [20.8, 12.4]), plant3([20.2, 12.9], "strelitzia nicolai"), *grote_tafel([16.0, 10.6], 4.2, 0),
        *keuken([10.4, 14.45], 5.0, 0), *kookeiland([11.0, 12.0], 0), boom3([7.4, 9.0], "ficus elastica"), boom3([13.0, 8.45], "dracaena"), hangplant([8.6, 9.6], 2.4), plant3([13.6, 14.2], "monstera"),
        *[hangplant([u, 10.6], 2.4) for u in (14.9, 17.1)], *tafeltje([7.7, 12.4], 0, 3), plant3([18.4, 14.2], "philodendron"),
        # verdieping: vide, lounge, werken, stille kamers
        wand([[1.0, 5.0], [4.7, 5.0], [4.7, 10.0], [1.0, 10.0]], 1.1, glas=True, n=_HL), *[hangplant([u, 5.0], 1.1, _HL) for u in (2.0, 3.6)],
        *vergaderkamer([2.7, 2.5], 4.6, 3.2, 0, 6, _HL), *stavergaderkamer([8.2, 2.3], 3.4, 3.6, 0, 5, _HL), pod2([7.3, 5.9], _HL), pod2([9.0, 5.9], _HL),
        *focuskamer([1.35, 11.4], 90, _HL), *focuskamer([1.35, 13.65], 90, _HL), pod2([3.4, 14.0], _HL), pod2([4.9, 14.0], _HL),
        plant3([5.9, 12.2], "zz-plant", _HL), boom3([9.2, 9.4], "ficus elastica", _HL), plant3([0.6, 4.5], "aspidistra", _HL), plant3([9.4, 13.9], "kentia", _HL), dict(t="box", soort="toiletgroep", c=[8.2, 11.6], w=3.0, d=2.4, h=2.4, a=0, kleur="#bdb7aa", n=_HL), label([8.2, 11.6], "toiletten, pantry", _HL),
        wand([[10.0, 7.8], [15.0, 7.8]], 2.9, glas=True, n=_HL), deur([15.6, 7.8], 0, n=_HL), wand([[16.2, 7.8], [21.0, 7.8]], 2.9, glas=True, n=_HL),
        *veelhoekbank([14.4, 3.8], 1.8, 6, open=(1, 4), n=_HL), *zitnis([20.8, 0.4], [20.8, 6.8], n=_HL), *kasten(10.3, 14.3, 0.45, d=0.35, h=2.2, n=_HL),
        *kasten(10.3, 15.0, 7.55, d=0.3, h=1.2, n=_HL),
        dict(t="box", soort="fauteuil", c=[11.4, 2.4], w=0.8, d=0.8, h=0.8, a=30, kleur="#e5d48c", n=_HL), dict(t="box", soort="fauteuil", c=[11.4, 5.4], w=0.8, d=0.8, h=0.8, a=-30, kleur="#e5d48c", n=_HL),
        boom3([17.6, 6.6], "ficus elastica", _HL), boom3([10.9, 3.9], "schefflera", _HL), plant3([20.3, 7.3], "philodendron", _HL), boom3([18.6, 8.8], "ficus elastica", _HL), plant3([17.3, 1.0], "monstera", _HL), *[hangplant([u, 3.8], 2.4, _HL) for u in (13.4, 15.4)],
        dict(t="box", soort="raambar", c=[20.45, 11.2], w=6.6, d=0.5, h=1.05, a=90, kleur=HOUT, n=_HL),
        *eiland2([12.4, 11.3], 0, _HL), *eiland2([15.8, 11.3], 0, _HL),
        plant3([10.6, 9.4], "dracaena", _HL), plant3([10.6, 14.2], "zz-plant", _HL), *[hangplant([u, 11.3], 2.4, _HL) for u in (12.4, 15.8)],
        # buiten
        dict(t="box", soort="plantenbak", c=[25.0, 11.3], w=7.0, d=0.5, h=0.6, a=90, kleur=WALNOOT), *tafeltje([22.6, 9.4], 0, 3), *tafeltje([22.6, 12.4], 0, 3),
        plant3([24.2, 8.2], "olijf"), label([29.5, 4.0], "6 parkeerplaatsen"), boom([35.0, 14.0], 0.9, 3.0),
    ],
    dak=dict(soort="pv", terras=None, groen=[], pv=[R(7.0, 1.0, 20.5, 14.0)], koepels=[[2.85, 7.5, 1.4]],
             tekst="Bestaand plat dak uit 2000 met de daklichtkoepel boven het atrium; zonnepanelen op het voorste deel. Geen dakterras: het pand is aan drie kanten aangebouwd en het dak is licht gebouwd.",
             tekst_en="Flat roof of a two storey office building from 2000, attached on three sides to other business buildings, a large roof light above the atrium at the back, "
                      "solar panels on the front part, a small parking lot with eight spaces in front of the only glass facade."),
    renders=dict(buiten=[]),
)
ONTWERPEN.update({"haarlem-hofmanweg-2f": HOFMAN})
LABELS.update({"haarlem-hofmanweg-2f": {"Café en keuken aan het zuidglas": [14.6, 9.0], "Atrium, trap en lockers": [3.2, 9.7], "Wastoren": [3.3, 0.7],
                                        "Gang": [8.2, 6.6], "Opslag": [4.9, 11.6], "Gym (eigen deur)": [14.6, 3.2],
                                        "Lounge en bieb boven de gym": [15.2, 6.6], "Werkzone aan het zuidglas": [15.2, 9.0], "Stille kamers rond de vide": [7.0, 9.2]}})
VIDES.update({"haarlem-hofmanweg-2f": [dict(naam="Vide: atrium met daklicht", poly=R(1.0, 5.0, 4.7, 10.0), n=1)]})
