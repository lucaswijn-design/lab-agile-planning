# ---------------------------------------------------------------- Ronde 9 (15 november 2026): Dukdalfweg 55, Amsterdam Westpoort (Westhaven)
# Hoekunit uit 2020 in een bedrijfsverzamelgebouw van 8 units (BAG: alle industrie- en kantoorfunctie, geen woningen), uitgesneden als 26,5 x 15,6 m
# (zie dossiers/amsterdam-dukdalfweg-55.json, opmerking). u = 0 is de noordgevel aan de Dukdalfweg en het parkeerterrein, v = 15,6 de oostgevel aan het binnenterrein
# (vrij van u 0 tot 15,6), v = 0 en u = 26,5 zijn scheidingswanden met de buurunits (Westhavenweg 115 tot 121). Circa 9,5 m tot het dak (3D BAG).
# Advertentie: hal 375 + kantoor 225 m² (eerste verdieping en entresol), overheaddeur, 6 eigen + 6 gedeelde parkeerplaatsen.
# Aanname: kantoor en entresol vormen samen één verdieping op 3,6 m over de voorste 14,4 m (14,4 x 15,6 = 225 m²); daarachter de hal op volle hoogte.
_DL = 1
DUKDALF = dict(
    titel="Dukdalfweg 55, Amsterdam Westpoort",
    sub="Hoekunit uit 2020 van 26,5 x 15,6 m in bedrijfsverzamelgebouw Zaansepoort, hal 375 + kantoor 225 m², circa 9 m hoog, eigen parkeren, pont naar Zaandam. Status eerst nabellen (brochure zonder datum).",
    hoogte=9.5, niveaus={"1": 3.6}, pui_h=3.2,
    concept="Van de straat naar achteren van druk naar zweet, en naar boven stil. Beneden achter de noordgevel het café met keuken, kookeiland, een lange tafel en een zitnis "
            "langs de oostramen. Onder de verdieping de achthoekige wastoren, de lockerwand en de garderobe als buffer. Daarachter onder de volle hoogte van de hal een lounge "
            "rond een zeshoekige bank en een strelitzia onder de lichtkoepels, en achterin de gym met drie racks, roeiers en de douchetoren, achter een dichte wand tot het dak. "
            "Boven, in het kantoor aan de noordgevel, de werkzone met een raambar van 13 m en drie eilanden; op de entresol de stille kamers: twee vergaderkamers, een sta-kamer, "
            "twee focuskamers en zes belcellen. Sober: de hal blijft kaal, de vloer wordt strak, wanden van oude ramen.",
    geluid="Gym achterin tegen de buurunits (bedrijven, geen woningen), 13 m van de werkzone op de verdieping. Tussen gym en de rest de lounge onder de volle hoogte en "
           "een dichte akoestische wand tot het dak (9 m) met een deur op toegangspas; de stille kamers op de entresol zijn dichte dozen aan de rand naar de hal. "
           "40 mm rubber op een akoestische ondervloer en platforms. De hal is hoog en hard: houtwolplaten op de wanden en baffles onder het dak.",
    pui=[[[0.0, 0.5], [0.0, 15.1]], [[0.5, 15.6], [14.2, 15.6]]],
    zones=[
        zone("Café aan de noordgevel", "café", R(0.2, 0.2, 9.0, 15.4),
             "Je komt binnen aan de Dukdalfweg, direct in het café: een lange tafel voor twaalf aan het noordglas, een zitnis met tafeltjes langs de oostramen, "
             "een keuken van 5,6 m tegen de buurwand met kookeiland en espressomachine, en de trap naar de werkzone. Monstera en kentia (noordlicht), strelitzia bij de oostramen.",
             ["Lange tafel van 4,2 m voor twaalf", "Zitnis van 5 m langs de oostramen", "Keuken van 5,6 m en kookeiland", "Trap naar de verdieping"],
             cam=dict(t=[4.6, 8.0], afstand=9, hoek=180),
             prompt="The café of a members club in a new industrial unit from 2020, behind a glass facade facing north: an olive green kitchen from second-hand stainless steel worktables along the side wall, "
                    "a reclaimed wood island with an espresso machine, a long oak table for twelve, a built-in olive bench with small tables along east windows, a black steel stair to the first floor, "
                    "a monstera and a kentia palm, smooth sealed concrete floor."),
        zone("Wastoren en lockers", "sanitair", R(9.0, 0.2, 14.4, 15.4),
             "Onder de verdieping: de achthoekige wastoren met drie toiletten, een lockerwand van 4 m met pothos erop, de garderobe en de techniek. De buffer tussen café en hal.",
             ["Wastoren van 5,2 m", "Lockerwand van 4 m en lockers in de toren (circa 94)", "Garderobe en techniek"],
             cam=dict(t=[11.7, 8.0], afstand=7, hoek=180),
             prompt="An octagonal concrete-look bathroom tower (eight flat faces, it still reads as round), 3 m high, under a mezzanine in a new industrial unit, board-marked plaster, "
                    "a V-shaped concrete wash trough with brass taps, a dark green locker wall with trailing pothos on top, ivy along the top rim of the tower."),
        zone("Lounge", "bieb", R(14.4, 0.2, 19.5, 15.4),
             "Onder de volle hoogte van de hal: een zeshoekige bank met twee open zijden rond een sfeerhaard, een boekenwand tegen de buurwand, fauteuils en een strelitzia "
             "en olijf onder de lichtkoepels. Een zijdeur in de oostgevel geeft sporters een eigen route naar de gym.",
             ["Zeshoekige bank rond een sfeerhaard", "Boekenwand van 5 m", "Strelitzia en olijf onder de lichtkoepels", "Zijdeur oostgevel voor de gym"],
             cam=dict(t=[17.0, 7.5], afstand=8, hoek=180),
             prompt="A lounge in a 9 m high industrial hall under round roof lights: a hexagonal olive velvet bench around a black fireplace, a walnut bookcase wall, butter yellow armchairs, "
                    "a tall strelitzia and an olive tree under the roof lights, wood wool acoustic panels on the walls, a glass mezzanine edge above."),
        zone("Gym", "gym", R(19.5, 0.2, 26.3, 15.4),
             "Achterin onder de volle hoogte: drie racks met optrekstang op platforms, drie roeiers, een matvloer voor groepslessen en yoga, kettlebells en de douchetoren. "
             "Dichte wand tot het dak en een deur op toegangspas; sporters komen via de zijdeur in de oostgevel.",
             ["Drie racks op zwevende platforms", "Drie roeiers", "Matvloer van 4 x 3,6 m", "Achthoekige douchetoren met vier douches", "Deur op toegangspas"],
             cam=dict(t=[22.9, 7.0], afstand=9, hoek=180),
             prompt="A functional gym at the back of a 9 m high industrial unit, closed off by a solid wall: three black power racks on oak platforms, rowing machines, a mat area for classes, "
                    "kettlebells, anthracite rubber floor, one wall oxblood red, an octagonal concrete-look shower tower in the corner, round roof lights above."),
        dict(zone("Werkzone aan de noordgevel", "werken", R(0.2, 0.2, 7.2, 15.4),
                  "Het kantoor op de verdieping: een raambar van 13 m pal achter de noordgevel (noordlicht, geen schittering) en drie eilanden van vier zit-sta bureaus, "
                  "de schermen haaks op het raam.",
                  ["Raambar van 13 m (21 krukken)", "Drie eilanden van vier bureaus 140 x 70", "Pothos en kentia"], n=_DL, cam=dict(t=[3.6, 8.0], afstand=8, hoek=180),
                  prompt="A coworking floor in the office part of a new industrial unit: a long oak window bar along a north facing glass facade, three islands of four compact sit-stand desks, "
                         "slate blue chairs, wood wool acoustic panels on the ceiling, pothos on a steel rail, a kentia palm."), tussenvloer=False),
        dict(zone("Stille kamers", "vergader", R(7.2, 0.2, 14.4, 15.4),
                  "Op de entresol, tussen de werkzone en de hal: twee vergaderkamers voor zes en een sta-kamer van oude ramen langs de buurwand, twee focuskamers en "
                  "zes belcellen langs de rand naar de hal, als dichte dozen.",
                  ["Twee vergaderkamers voor 6", "Sta-kamer voor 5", "Twee focuskamers", "Zes belcellen"], n=_DL, cam=dict(t=[10.8, 8.0], afstand=8, hoek=180),
                  prompt="A mezzanine in a 9 m high industrial hall with meeting rooms made of reclaimed steel and timber windows, two tiny glass focus rooms and round slate blue felt phone booths along the edge, "
                         "a view down into a lounge with a tall tree, pothos trailing over the edge."), tussenvloer=False),
    ],
    buiten=[dict(naam="Parkeerplaats en groen", poly=R(-14.0, -3.0, -0.2, 20.0), kleur="#c9c3b6"),
            dict(naam="Binnenterrein (6 gedeelde plaatsen)", poly=R(0.0, 15.8, 15.6, 26.0), kleur="#c9c3b6"),
            dict(naam="Terras aan de oostgevel", poly=R(1.0, 15.8, 7.0, 19.0), kleur="#d5bd96")],
    elementen=[
        # café
        deur([0.0, 13.4], 90, w=1.4), *grote_tafel([2.2, 7.4], 4.2, 90), *keuken([4.0, 0.55], 5.6, 0), *kookeiland([4.6, 3.2], 0),
        *zitnis([6.0, 15.4], [1.0, 15.4]), dict(t="box", soort="trap", c=[6.6, 9.8], w=1.1, d=4.4, h=0.3, a=0, kleur=STAAL), label([6.6, 7.2], "trap"),
        boom3([1.2, 1.6], "kentia"), plant3([7.0, 12.9], "strelitzia nicolai"), plant3([0.9, 11.8], "monstera"), boom3([8.3, 5.6], "ficus elastica"),
        *tafeltje([4.6, 11.0], 0, 3), *[hangplant([2.2, v], 3.2) for v in (6.0, 8.8)], plant3([8.5, 1.0], "zz-plant"), boom3([8.1, 14.4], "kentia"), hangplant([4.6, 3.2], 3.2),
        # wastoren, lockers
        *achthoektoren([11.7, 3.0], 2.6, 90, "was", lockers=(4,)), *lockerwand([9.25, 8.4], 4.0, 90), label([10.0, 8.4], "lockers"),
        dict(t="box", soort="garderobe", c=[12.0, 12.0], w=3.0, d=0.4, h=1.8, a=0, kleur=WALNOOT), dict(t="box", soort="techniek", c=[12.9, 14.4], w=2.6, d=1.8, h=2.6, a=0, kleur="#8f8a80"),
        label([12.9, 14.4], "techniek"), plant3([13.8, 6.4], "aspidistra"), plant3([13.9, 9.6], "zz-plant"), plant3([9.4, 14.6], "sansevieria"),
        # lounge
        *veelhoekbank([17.0, 6.8], 1.9, 6, open=(1, 4)), *kasten(14.8, 19.2, 0.45, d=0.35, h=2.6), boom3([15.5, 11.6], "strelitzia nicolai"), boom3([18.3, 11.2], "olijf"),
        dict(t="box", soort="fauteuil", c=[15.3, 3.0], w=0.8, d=0.8, h=0.8, a=20, kleur="#e5d48c"), dict(t="box", soort="fauteuil", c=[18.8, 3.0], w=0.8, d=0.8, h=0.8, a=-20, kleur="#e5d48c"),
        plant3([14.9, 13.6], "monstera"), deur([15.6, 15.6], 0, toegang=True, w=1.0), hangplant([17.0, 6.8], 4.0), plant3([19.1, 8.6], "philodendron"),
        # gym
        wand([[19.5, 0.2], [19.5, 14.2]], 9.0, gym=True), deur([19.5, 14.8], 90, toegang=True), wand([[19.5, 15.4], [19.5, 15.6]], 9.0, gym=True),
        *rack([25.1, 1.5], 0), *rack([25.1, 4.6], 0), *rack([25.1, 7.7], 0), roeier([20.2, 2.3], 90), roeier([21.1, 2.3], 90), roeier([22.0, 2.3], 90),
        dict(t="kleed", c=[21.9, 7.2], w=3.6, d=4.0, a=0, kleur="#c7928a"), label([21.9, 7.2], "groepsles en yoga"),
        dict(t="box", soort="kettlebells", c=[20.0, 11.2], w=2.0, d=0.5, h=0.9, a=90, kleur=STAAL), *achthoektoren([23.9, 12.8], 2.3, 180, "douche"),
        plant3([20.1, 13.6], "sansevieria"), boom3([21.0, 9.9], "kentia"), hangplant([21.9, 7.2], 4.0), *lockerwand([22.6, 0.45], 2.4, 0),
        # verdieping: werkzone
        dict(t="box", soort="raambar", c=[0.45, 7.3], w=13.0, d=0.5, h=1.05, a=90, kleur=HOUT, n=_DL),
        *eiland2([4.1, 2.6], 0, _DL), *eiland2([4.1, 7.0], 0, _DL), *eiland2([4.1, 11.4], 0, _DL),
        boom3([1.2, 14.6], "kentia", _DL), plant3([6.6, 4.8], "zz-plant", _DL), plant3([6.6, 9.2], "zz-plant", _DL), *[hangplant([4.1, v], 2.9, _DL) for v in (2.6, 7.0, 11.4)],
        plant3([6.7, 0.8], "dracaena", _DL), boom3([6.4, 14.6], "ficus elastica", _DL), *[hangplant([0.7, v], 2.9, _DL) for v in (4.0, 10.0)],
        # verdieping: stille kamers
        *vergaderkamer([9.0, 2.6], 4.6, 3.4, 90, 6, _DL), *stavergaderkamer([9.0, 6.6], 3.0, 3.4, 90, 5, _DL), *vergaderkamer([9.0, 10.5], 4.4, 3.4, 90, 6, _DL),
        *focuskamer([13.0, 1.4], 90, _DL), *focuskamer([13.0, 3.7], 90, _DL), *[pod2([13.4, v], _DL) for v in (5.6, 7.1, 8.6, 10.1, 11.6, 13.1)],
        wand([[14.4, 0.2], [14.4, 15.4]], 1.1, glas=True, n=_DL), *[hangplant([14.4, v], 1.1, _DL) for v in (5.0, 9.0, 14.6)], boom3([9.2, 14.2], "ficus elastica", _DL),
        plant3([11.4, 14.8], "aspidistra", _DL),
        # buiten
        *tafeltje([2.6, 17.4], 0, 3), *tafeltje([5.4, 17.4], 0, 3), dict(t="box", soort="plantenbak", c=[4.0, 18.8], w=6.0, d=0.5, h=0.6, a=0, kleur=WALNOOT),
        label([-7.0, 8.0], "6 eigen parkeerplaatsen"), boom([-12.0, 18.0], 0.9, 3.0), boom([-12.0, 2.0], 0.9, 3.0),
    ],
    dak=dict(soort="pv", terras=None, groen=[], pv=[R(0.8, 0.8, 14.0, 14.8), R(20.0, 0.8, 26.0, 14.8)],
             koepels=[[17.0, 4.0, 0.9], [17.0, 11.0, 0.9], [22.9, 7.0, 0.9]],
             tekst="Bestaand plat dak uit 2020; lichtkoepels boven lounge en gym, zonnepanelen op de rest. Geen dakterras: unit in een verzamelgebouw met erfpacht van het havenbedrijf.",
             tekst_en="Flat roof of one corner unit in a long new industrial building from 2020 in a port area, round roof lights above the back half, solar panels on the rest; "
                      "the other units stay plain grey, a parking lot with trees along the street in front."),
    renders=dict(buiten=[]),
)
ONTWERPEN.update({"amsterdam-dukdalfweg-55": DUKDALF})
LABELS.update({"amsterdam-dukdalfweg-55": {"Café aan de noordgevel": [4.6, 5.6], "Wastoren en lockers": [11.7, 6.6], "Lounge": [17.0, 9.6],
                                           "Gym": [22.6, 10.4], "Werkzone aan de noordgevel": [3.6, 9.2], "Stille kamers": [11.4, 14.4]}})
VIDES.update({"amsterdam-dukdalfweg-55": [dict(naam="Vide: hal op volle hoogte", poly=R(14.4, 0.2, 26.3, 15.4), n=1)]})
