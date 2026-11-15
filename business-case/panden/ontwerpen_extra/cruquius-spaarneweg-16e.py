# ---------------------------------------------------------------- Ronde 9 (15 november 2026): Spaarneweg 16E, Cruquius (Haarlemmermeer)
# Vrijstaande bedrijfsruimte uit 1985 van 25,2 x 17,4 m (BAG 439 m², 1 verblijfsobject industriefunctie), hal 330 + kantoor 85 m² op de begane grond,
# circa 4,8 m tot het dak (3D BAG). u langs de straat (Spaarneweg, zuidoost op v = 0), v naar achteren (noordwest, v = 17,4).
# Zuidwest (u = 0) op 3,7 m het pand Spaarneweg 16C/16D met twee bedrijfswoningen: daar komt het stille deel, de gym gaat naar de andere kop (noordoost, u = 26,5)
# met een eigen deur op het erf. Noordoost ligt het eigen erf met parkeren (perceel tot u 35,7). Achter (v = 17,4) op 5 m een bedrijfshal.
CRUQUIUS = dict(
    titel="Spaarneweg 16E, Cruquius",
    sub="Vrijstaande hal uit 1985 van 25 x 17 m en circa 4 m vrij hoog op de hoek van de Spaarneweg, met eigen erf. Status eerst nabellen (brochure zonder datum, oozo noemt ook huur).",
    hoogte=4.8, niveaus={}, pui_h=3.0,
    concept="Eén lage hal die je van de ene kop naar de andere doorloopt, van zweet naar stilte. Je komt binnen aan de Spaarneweg, midden in het café: een lange tafel aan het nieuwe glas, "
            "keuken en kookeiland achterin, een zeshoekige bank en een zitnis tegen de boekenwand. Rechts staat de achthoekige wastoren met lockers als buffer, daarachter de gym "
            "met een eigen deur op het erf, zodat sporters om 6:00 naar binnen kunnen. Links achter een glazen wand de werkzone met vier eilanden aan het straatglas, en achterin de "
            "stille kamers: vergaderkamer voor zes, sta-kamer, focuskamer en drie belcellen. Sober: de hal blijft zichtbaar, de vloer wordt geschuurd en gecoat, "
            "de glazen wanden komen van oude ramen, het kantoorplafond gaat eruit.",
    geluid="Gym aan de noordoostkop, op meer dan 22 m van de bedrijfswoningen van Spaarneweg 16C/16D (zuidwest) en 12 m van de werkzone. Tussen gym en café de wastoren, "
           "de lockerwand en de techniek (4,5 m buffer) en een dichte akoestische wand tot het dak met een deur op toegangspas. 40 mm rubber op een akoestische ondervloer en "
           "platforms onder de racks. Tussen café en werken een glazen wand en een dichte boekenwand.",
    pui=[[[1.5, 0.0], [16.8, 0.0]], [[26.5, 1.0], [26.5, 6.4]]],
    zones=[
        zone("Werkzone aan de straat", "werken", R(1.5, 0.2, 10.0, 9.0),
             "Achter een glazen wand van oude ramen: vier eilanden van vier zit-sta bureaus haaks op het nieuwe straatglas, zodat niemand tegen het licht in kijkt. "
             "Een ficus aan het glas, pothos boven de eilanden.",
             ["Vier eilanden van vier bureaus 140 x 70 (16 plekken)", "Schermen haaks op het raam, looppad van 1,3 m tussen de eilanden",
              "Glazen wand naar het café van hergebruikte stalen ramen", "Houtwolplaten tegen de achterwand"],
             cam=dict(t=[5.5, 4.6], afstand=8, hoek=200),
             prompt="A small coworking room in a low 1985 industrial hall behind a new glass street front: four islands of four compact sit-stand desks with oak tops, set at right angles to the windows, "
                    "slate blue refurbished chairs, a glass partition made of reclaimed steel windows, a ficus at the glass, pothos trailing from a steel cable above the desks, a smooth sealed concrete floor."),
        zone("Stille kamers", "vergader", R(1.5, 9.0, 10.0, 17.2),
             "Achterin, in het donkere deel: een vergaderkamer voor zes en een sta-kamer van oude ramen, een focuskamer voor één of twee en vier ronde belcellen op een rij.",
             ["Vergaderkamer voor 6 met scherm en camera", "Sta-kamer voor 4 tot 6 met whiteboardwand", "Focuskamer voor 1 tot 2 personen", "Vier belcellen in leisteenblauw vilt"],
             cam=dict(t=[5.5, 13.0], afstand=7, hoek=270),
             prompt="The quiet back corner of a low industrial hall: a meeting room for six and a standing meeting room with walls of reclaimed timber and steel windows, a tiny glass focus room, "
                    "a row of four round slate blue felt phone booths, an aspidistra and a zz plant in clay pots, warm task lights."),
        zone("Café, keuken en lounge", "café", R(10.0, 0.2, 17.0, 17.2),
             "Je komt binnen aan de straat, midden in het café: een lange tafel voor twaalf aan het glas, een zeshoekige bank met twee open zijden, een zitnis tegen de boekenwand "
             "en achterin de keuken van 5 m met kookeiland en espressomachine. Strelitzia aan het glas, kentia en ficus als bomen.",
             ["Lange tafel van 4,2 m voor twaalf aan het straatglas", "Zeshoekige bank rond een sfeerhaard", "Zitnis van 3,8 m met twee tafeltjes tegen de boekenwand",
              "Keuken van 5 m en kookeiland met espressomachine", "Smal terras aan de straat op het zuidoosten"],
             cam=dict(t=[13.2, 7.0], afstand=10, hoek=250),
             prompt="The café of a members club in a low 1985 industrial hall with a new glass front to the street: a long oak table for twelve along the glass, a hexagonal olive velvet bench around a black fireplace, "
                    "a built-in bench with small tables against a walnut bookcase wall, an olive green kitchen made from second-hand stainless steel worktables at the back, a reclaimed wood island with an espresso machine, "
                    "a strelitzia and a kentia palm, warm afternoon light."),
        zone("Wastoren", "sanitair", R(17.0, 0.2, 21.5, 17.2),
             "De achthoekige wastoren met drie toiletten en een V-wastrog, met lockers in een buitenzijde; daarachter de lockerwand tegen de gymwand en de techniek. Samen de buffer tussen café en gym.",
             ["Wastoren 4,8 m met drie toiletten", "Lockers in de toren en een lockerwand van 3 m (circa 78)", "Techniek: warmtepomp, batterij, meterkast"],
             cam=dict(t=[19.2, 4.2], afstand=7, hoek=200),
             prompt="An octagonal concrete-look bathroom tower (eight flat faces, it still reads as a round object), 3 m high, inside a low industrial hall, board-marked plaster, a V-shaped concrete wash trough with brass taps "
                    "at the open side, dark green lockers built into one outer face, ivy and ferns along the top rim, a locker wall with trailing pothos on top."),
        zone("Gym", "gym", R(21.5, 0.2, 26.3, 17.2),
             "Aan de noordoostkop, met een eigen deur op het erf en glas naar het parkeerterrein: twee racks op platforms, twee roeiers, een matvloer voor groepslessen en yoga, "
             "kettlebells en de D-vormige douchetoren in de hoek. Dichte wand tot het dak en een deur op toegangspas.",
             ["Twee racks op zwevende platforms (laag model van 2,3 m)", "Twee roeiers aan het glas", "Matvloer van 3,6 x 3,4 m", "D-vormige douchetoren met vier douches", "Eigen ingang op toegangspas"],
             cam=dict(t=[24.0, 8.0], afstand=8, hoek=180),
             prompt="A compact functional gym at the end of a low industrial hall: two black power racks on oak platforms, two rowing machines facing a glass wall to a yard, a mat area for classes and yoga, "
                    "kettlebells on a steel rack, anthracite rubber floor, one wall oxblood red, a D-shaped concrete-look shower tower in the corner, a kentia palm."),
    ],
    buiten=[dict(naam="Terras aan de straat", poly=R(10.0, -3.0, 16.8, -0.2), kleur="#d5bd96"),
            dict(naam="Erf en parkeren", poly=R(26.7, -3.0, 35.5, 19.8), kleur="#c9c3b6"),
            dict(naam="Straat", poly=R(-12.0, -12.0, 40.0, -3.2), kleur="#9a958c")],
    elementen=[
        # werkzone
        *eiland2([3.4, 2.6], 90), *eiland2([8.1, 2.6], 90), *eiland2([3.4, 6.6], 90), *eiland2([8.1, 6.6], 90),
        boom3([5.75, 1.0], "ficus elastica"), plant3([1.95, 4.6], "dracaena"), boom3([2.4, 9.1], "kentia"), *[hangplant([u, v]) for u in (3.4, 8.1) for v in (2.6, 6.6)], hangplant([5.75, 4.6]),
        wand([[10.0, 0.2], [10.0, 7.7]], 3.0, glas=True), deur([10.0, 8.35], 90, w=1.1), wand([[10.0, 9.0], [10.0, 17.2]], 3.0),
        # stille kamers
        *focuskamer([2.8, 11.2], 0), pod2([4.75, 11.2]), pod2([6.25, 11.2]), pod2([7.75, 11.2]), pod2([9.25, 11.2]),
        *vergaderkamer([4.0, 15.6], 4.6, 3.0, 0, 6), *stavergaderkamer([8.1, 15.6], 3.3, 3.0, 0, 5), plant3([1.95, 13.25], "aspidistra"), plant3([9.4, 13.3], "zz-plant"), plant3([4.9, 13.1], "aspidistra"),
        # café
        deur([16.0, 0.0], 0, w=1.2), *grote_tafel([12.9, 2.5], 4.2, 0), plant3([10.55, 0.95], "strelitzia nicolai"), boom3([15.95, 7.3], "kentia"), *[hangplant([u, 2.5]) for u in (11.6, 14.2)],
        *veelhoekbank([13.2, 7.7], 1.8, 6, open=(1, 4)), dict(t="box", soort="fauteuil", c=[15.9, 9.5], w=0.8, d=0.8, h=0.8, a=20, kleur="#5a2741"),
        boom3([16.1, 11.6], "ficus elastica"),
        *kasten(9.7, 13.6, 10.25, a=90, d=0.3, h=2.6), *zitnis([10.55, 13.4], [10.55, 9.6]),
        *keuken([13.3, 16.85], 5.0, 0), *kookeiland([13.3, 14.4], 0), hangplant([12.3, 7.7]), hangplant([14.1, 7.7]), boom3([16.3, 15.3], "kentia"),
        dict(t="box", soort="garderobe", c=[16.75, 13.2], w=1.6, d=0.4, h=1.8, a=90, kleur=WALNOOT),
        # wastoren, lockers, techniek
        *achthoektoren([19.25, 4.2], 2.4, 180, "was", lockers=(6,)), *lockerwand([21.2, 9.0], 3.0, 90), 
        dict(t="box", soort="techniek", c=[19.3, 15.9], w=3.6, d=2.4, h=2.6, a=0, kleur="#8f8a80"), label([19.3, 15.9], "techniek"), plant3([17.6, 12.6], "aspidistra"), plant3([17.6, 7.3], "zz-plant"),
        # gym
        wand([[21.5, 0.2], [21.5, 11.0]], 4.5, gym=True), deur([21.5, 11.6], 90, toegang=True), wand([[21.5, 12.2], [21.5, 17.2]], 4.5, gym=True),
        deur([26.5, 11.6], 90, toegang=True, w=1.1),
        *rack([25.0, 1.6], 0), *rack([25.0, 4.9], 0), roeier([22.2, 2.6], 90), roeier([23.1, 2.6], 90),
        dict(t="kleed", c=[23.7, 8.5], w=3.6, d=3.4, a=0, kleur="#c7928a"), label([23.7, 8.5], "groepsles en yoga"),
        dict(t="box", soort="kettlebells", c=[26.0, 8.5], w=2.4, d=0.5, h=0.9, a=90, kleur=STAAL),
        *dtoren([26.3, 17.2], [21.7, 17.2], 0.9, "douche"), plant3([22.1, 13.3], "sansevieria"), boom3([22.5, 5.0], "kentia"), hangplant([23.7, 8.5]),
        # buiten
        dict(t="box", soort="plantenbak", c=[13.2, -2.6], w=6.8, d=0.5, h=0.6, a=0, kleur=WALNOOT), *tafeltje([11.6, -1.3], 0, 2), *tafeltje([14.6, -1.3], 0, 2), plant3([10.3, -2.0], "olijf"), plant3([16.4, -2.0], "olijf"),
        boom([34.0, 18.0], 0.9, 3.0), boom([34.0, -1.8], 0.9, 3.0), label([31.0, 9.0], "6 parkeerplaatsen en fietsen"),
    ],
    dak=dict(soort="pv", terras=None, groen=[], pv=[R(2.0, 1.0, 16.5, 16.4), R(22.0, 1.0, 26.0, 13.5)],
             koepels=[[5.5, 4.6, 0.8], [13.0, 7.5, 0.8], [19.25, 4.2, 0.8], [5.5, 13.0, 0.6]],
             tekst="Bestaand plat dak uit 1985: isoleren, nieuwe lichtkoepels boven werkzone, café en wastoren, zonnepanelen op de rest. Geen dakterras: te licht gebouwd en een eigen erf is er al.",
             tekst_en="A low flat-roofed industrial building from 1985 on a corner plot, a few new round roof lights, solar panels on the rest of the roof; a paved yard with parking on one side, "
                      "neighbouring industrial halls stay plain grey."),
    renders=dict(buiten=[]),
)
ONTWERPEN.update({"cruquius-spaarneweg-16e": CRUQUIUS})
LABELS.update({"cruquius-spaarneweg-16e": {"Werkzone aan de straat": [5.65, 4.6], "Stille kamers": [6.4, 13.3], "Café, keuken en lounge": [13.6, 11.6],
                                           "Wastoren": [19.3, 11.4], "Gym": [23.9, 12.5]}})
