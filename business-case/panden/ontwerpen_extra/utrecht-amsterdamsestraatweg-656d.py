# ---------------------------------------------------------------- Ronde 9 (15 november 2026): Amsterdamsestraatweg 656D, Utrecht Zuilen (vervangt Roelantdreef 24)
# Bedrijfsruimte uit 2003 in een pand met twee verblijfsobjecten (656D 1.020 m² en Martin-ovenweg 19, 3.402 m², beide industriefunctie, geen woningen).
# Uitgesneden als de lichte strook van 46 x 23 m aan de straatkant (zie dossiers/utrecht-amsterdamsestraatweg-656d.json, opmerking). Circa 7,1 m tot het dak (3D BAG),
# aangenomen 6 m vrij. Advertentie (oozo): 1.089 m² op twee lagen, hal 909 + kantoor 180 m², label A. Aanname: het kantoor zit in twee lagen aan de straatkop (u 1,2 tot 5,2).
# u = 1,2 is de straatgevel (noordoost, Amsterdamsestraatweg), v = 23 de lange gevel op het zuidoosten aan het binnenterrein, v = 0 ligt op 1,6 m van een bedrijfshal (blind),
# u = 46 grenst aan de rest van de strook en de hal van Martin-ovenweg 19.
_AS = 1
AMSTERDAMSESTRAATWEG = dict(
    titel="Amsterdamsestraatweg 656D, Utrecht",
    sub="Bedrijfsruimte uit 2003 van 46 x 23 m en circa 6 m vrij hoog in Zuilen, met kantoor in twee lagen aan de straat, label A, 1,3 km van station Utrecht Zuilen. Vervangt Roelantdreef 24. Status eerst nabellen (oozo sinds maart 2025).",
    hoogte=7.1, niveaus={"1": 3.4}, pui_h=3.0,
    concept="Een lange hal die je van de straat naar achteren doorloopt, van druk naar stil naar zweet. Aan de straatkop de entree met lockers en de trap naar de bieb op de kantoorverdieping. "
            "Dan het grote café langs de zonnige zuidoostgevel met een lange tafel, een zitnis, een zeshoekige bank en de keuken met kookeiland, en aan de blinde kant tafeltennis. "
            "Daarna de werkzone met zes eilanden onder nieuwe lichtkoepels en een raambar van 13 m aan het glas, met langs de blinde gevel twee vergaderkamers, een sta-kamer en belcellen. "
            "Een band met de wastoren, toiletten en techniek scheidt werken van sporten. Achterin de gym met vier racks en de douchetoren, met een eigen deur naar het binnenterrein, "
            "en ernaast een studio voor yoga en groepslessen. Sober: de hal blijft kaal, de vloer strak, wanden van oude ramen.",
    geluid="Gym en studio achterin, tegen de hal van Martin-ovenweg 19 (industrie, geen woningen) en ruim 40 m van de straat met woningen aan de overkant. Tussen werken en gym een band van 4,8 m "
           "met wastoren, toiletgroep en techniek en een dichte akoestische wand tot het dak met deuren op toegangspas. 40 mm rubber op een akoestische ondervloer en platforms. "
           "Café en tafeltennis aan de straatkant, stille kamers op de kantoorverdieping boven de entree.",
    pui=[[[5.5, 23.0], [31.0, 23.0]], [[37.0, 23.0], [45.5, 23.0]], [[1.2, 9.0], [1.2, 22.5]]],
    zones=[
        zone("Entree en lockers", "entree", R(1.2, 0.2, 5.2, 22.8),
             "Aan de straatkop, in het onderste deel van het kantoor: de voordeur aan de Amsterdamsestraatweg, twee lockerwanden, de garderobe en de trap naar de bieb.",
             ["Voordeur aan de straat met fietsparkeren ervoor", "Twee lockerwanden (circa 120 lockers) met pothos erop", "Garderobe", "Trap naar de bieb"],
             cam=dict(t=[3.2, 14.0], afstand=6, hoek=0),
             prompt="The entrance of a members club in the office part of an industrial building from 2003: a black steel and glass front door, dark green locker walls with trailing pothos on top, "
                    "a coat rack of steel pipes, a black steel stair, two olive trees in clay pots, smooth sealed concrete floor."),
        zone("Café, keuken en tafeltennis", "café", R(5.2, 0.2, 17.5, 22.8),
             "Langs de zonnige zuidoostgevel het café: een lange tafel voor twaalf aan het nieuwe glas, een zitnis met tafeltjes, een zeshoekige bank rond de haard en een boekenwand. "
             "Aan de blinde kant de keuken van 6 m met kookeiland en de tafeltennistafel. Strelitzia en olijf aan het glas, kentia en ficus in het midden.",
             ["Lange tafel van 4,2 m voor twaalf aan het glas", "Zitnis van 5 m langs de gevel", "Zeshoekige bank rond een sfeerhaard", "Keuken van 6 m en kookeiland",
              "Tafeltennis (inklapbaar)", "Terras op het binnenterrein"],
             cam=dict(t=[11.0, 14.0], afstand=12, hoek=200),
             prompt="The café of a members club in a 6 m high industrial hall from 2003 with a new glass facade facing south east: a long oak table for twelve along the glass, an olive green built-in bench with small tables, "
                    "a hexagonal olive velvet bench around a black fireplace, a walnut bookcase wall, an olive green kitchen from second-hand stainless steel worktables with a reclaimed wood island and an espresso machine, "
                    "a folding ping pong table, a strelitzia and an olive tree at the glass, round roof lights."),
        zone("Werkzone onder de lichtkoepels", "werken", R(17.5, 9.0, 31.5, 22.8),
             "Zes eilanden van vier zit-sta bureaus met de schermen haaks op het glas, onder nieuwe lichtkoepels, en een raambar van 13 m pal achter de zuidoostgevel. "
             "Een rij kentia's in een lange plantenbak scheidt de werkzone van de vergaderkamers langs de blinde gevel.",
             ["Zes eilanden van vier bureaus 140 x 70 (24 plekken)", "Raambar van 13 m (21 krukken)", "Acht nieuwe lichtkoepels", "Rij kentia's als groene buffer", "Looppaden van 1,4 tot 1,6 m"],
             cam=dict(t=[24.5, 16.0], afstand=12, hoek=200),
             prompt="A large coworking floor in a 6 m high industrial hall: six islands of four compact sit-stand desks with oak tops at right angles to a new glass facade, a long oak window bar along the glass, "
                    "slate blue chairs, round roof lights, wood wool acoustic baffles, pothos trailing from steel cables, kentia palms between the rows, smooth sealed concrete floor."),
        zone("Vergaderen langs de blinde gevel", "vergader", R(17.5, 0.2, 31.5, 9.0),
             "Langs de gevel zonder ramen: twee vergaderkamers voor zes en een sta-kamer van oude ramen, en vier ronde belcellen.",
             ["Twee vergaderkamers voor 6", "Sta-kamer voor 5", "Vier belcellen"], cam=dict(t=[24.5, 4.5], afstand=9, hoek=270),
             prompt="A row of meeting rooms with walls made of reclaimed steel and timber windows along a blind wall in an industrial hall, a standing meeting room with a whiteboard wall, "
                    "round slate blue felt phone booths, aspidistra and zz plants."),
        zone("Wastoren, toiletten en techniek", "sanitair", R(31.5, 0.2, 36.3, 22.8),
             "De buffer tussen werken en sporten: de achthoekige wastoren met lockers, een toiletgroep met een toegankelijk toilet en de techniek.",
             ["Wastoren van 4,4 m met drie toiletten", "Toiletgroep (twee toiletten en een toegankelijk toilet)", "Techniek: warmtepomp, batterij, meterkast"],
             cam=dict(t=[33.9, 12.0], afstand=8, hoek=180),
             prompt="An octagonal concrete-look bathroom tower (eight flat faces, it still reads as round), 3 m high, in a 6 m high industrial hall, board-marked plaster, a V-shaped concrete wash trough with brass taps, "
                    "dark green lockers in two outer faces, ivy and ferns along the top rim."),
        zone("Gym (eigen deur)", "gym", R(36.3, 8.0, 45.8, 22.8),
             "Achterin onder de volle hoogte: vier racks met optrekstang op platforms tegen de achterwand, drie roeiers aan het glas, een matvloer, kettlebells en de douchetoren. "
             "Eigen deur naar het binnenterrein, dichte wand tot het dak en een deur op toegangspas.",
             ["Vier racks op zwevende platforms", "Drie roeiers aan het glas", "Matvloer van 4 x 4 m", "Achthoekige douchetoren met vier douches", "Eigen deur op toegangspas"],
             cam=dict(t=[41.0, 15.0], afstand=10, hoek=180),
             prompt="A functional gym at the back of a 6 m high industrial hall, closed off by a solid wall: four black power racks on oak platforms, rowing machines facing a glass facade, a mat area, kettlebells, "
                    "anthracite rubber floor, one wall oxblood red, an octagonal concrete-look shower tower in the corner, round roof lights."),
        zone("Studio", "studio", R(36.3, 0.2, 45.8, 8.0),
             "Naast de gym, achter een eigen deur: een studio voor yoga, mobiliteit en groepslessen, ook te gebruiken voor events en workshops. Houten vloer, spiegelwand, matten in een kast.",
             ["Houten sportvloer van 74 m²", "Spiegelwand en matten", "Ook voor events en workshops"], cam=dict(t=[41.0, 4.0], afstand=8, hoek=270),
             prompt="A calm studio for yoga and group classes in an industrial hall: a warm wooden floor, a mirror wall, rolled mats on a wooden rack, terracotta lime-wash, plants, soft daylight from roof lights."),
        dict(zone("Bieb en stille kamers", "bieb", R(1.2, 0.2, 5.2, 22.8),
                  "Op de kantoorverdieping aan de straat: drie focuskamers, vier belcellen, een boekenwand en leesplekken aan de straatramen. Het stilste deel van de club, ver van de gym.",
                  ["Drie focuskamers", "Vier belcellen", "Boekenwand en leesstoelen aan het raam"], n=_AS, cam=dict(t=[3.2, 15.0], afstand=7, hoek=0),
                  prompt="A quiet library on the first floor of the office part of an industrial building: three tiny glass focus rooms made of reclaimed windows, round felt phone booths, a walnut bookcase wall, "
                         "butter yellow reading chairs at the street windows, a kentia palm."), tussenvloer=False),
    ],
    buiten=[dict(naam="Terras op het binnenterrein", poly=R(6.0, 23.2, 17.0, 27.5), kleur="#d5bd96"),
            dict(naam="Parkeerplaats en groen", poly=R(17.5, 23.2, 46.0, 30.0), kleur="#c9c3b6"),
            dict(naam="Straat", poly=R(-16.0, -6.0, -6.0, 32.0), kleur="#9a958c")],
    elementen=[
        # entree
        deur([1.2, 16.0], 90, w=1.6), dict(t="box", soort="trap", c=[3.4, 4.0], w=1.1, d=4.4, h=0.3, a=0, kleur=STAAL), label([3.4, 1.4], "trap"),
        *lockerwand([3.25, 22.55], 3.6, 0), *lockerwand([4.95, 12.0], 4.0, 90), dict(t="box", soort="garderobe", c=[1.5, 11.0], w=2.4, d=0.4, h=1.8, a=90, kleur=WALNOOT),
        plant3([2.0, 19.6], "olijf"), plant3([2.0, 13.0], "olijf"), boom3([2.4, 8.0], "kentia"), plant3([4.7, 2.0], "kentia"),
        # café
        *grote_tafel([9.0, 21.2], 4.2, 0), *zitnis([17.0, 22.8], [12.0, 22.8]), *veelhoekbank([10.0, 15.0], 2.0, 6, open=(1, 4)),
        *keuken([9.0, 0.55], 6.0, 0), *kookeiland([9.0, 3.4], 0), *pingpong([14.4, 6.6], 90), *kasten(9.5, 15.5, 5.45, a=90, d=0.35, h=2.4),
        plant3([5.9, 22.2], "strelitzia nicolai"), boom3([16.6, 19.6], "olijf"), boom3([6.2, 16.8], "ficus elastica"), boom3([13.6, 15.2], "kentia"), boom3([6.4, 6.4], "kentia"),
        dict(t="box", soort="fauteuil", c=[13.2, 12.6], w=0.8, d=0.8, h=0.8, a=20, kleur="#5a2741"), dict(t="box", soort="fauteuil", c=[7.0, 12.4], w=0.8, d=0.8, h=0.8, a=-20, kleur="#47522a"),
        *[hangplant([u, 21.2], 3.2) for u in (7.6, 10.4)], hangplant([10.0, 15.0], 3.5), plant3([12.8, 1.2], "monstera"), plant3([16.9, 10.4], "monstera"), plant3([5.8, 1.0], "zz-plant"),
        *tafeltje([8.0, 9.6], 0, 3), *tafeltje([11.6, 9.4], 0, 3), *[hangplant(c, 3.2) for c in ([9.0, 3.4], [8.0, 9.6], [11.6, 9.4])], boom3([16.9, 14.0], "ficus elastica"),
        # werkzone
        dict(t="box", soort="raambar", c=[24.5, 22.55], w=13.0, d=0.5, h=1.05, a=0, kleur=HOUT),
        *[x for u in (19.6, 24.4, 29.2) for v in (14.5, 18.9) for x in eiland2([u, v], 90)],
        *[boom3([u, 16.7], "kentia") for u in (22.0, 26.8)], *[plant3([u, 11.2], "zz-plant") for u in (22.0, 26.8)], *[hangplant([u, v], 3.5) for u in (19.6, 24.4, 29.2) for v in (14.5, 18.9)],
        *[boom3([u, 11.2], "kentia") for u in (19.6, 24.4, 29.2)], *[hangplant([u, 22.55], 3.0) for u in (19.0, 21.2, 23.4, 25.6, 27.8, 30.0)], plant3([31.1, 12.4], "monstera"),
        dict(t="box", soort="plantenbak", c=[24.4, 11.2], w=12.0, d=0.5, h=0.5, a=0, kleur=WALNOOT), plant3([17.9, 7.6], "aspidistra"),
        boom3([31.0, 20.6], "ficus elastica"), plant3([18.0, 21.2], "dracaena"),
        # vergaderen
        *vergaderkamer([20.2, 1.9], 4.6, 3.4, 0, 6), *vergaderkamer([25.0, 1.9], 4.6, 3.4, 0, 6), *stavergaderkamer([29.3, 1.9], 3.6, 3.4, 0, 5),
        *[pod2([u, 5.9]) for u in (19.0, 20.6, 22.2, 23.8)], plant3([26.0, 6.0], "aspidistra"), boom3([28.6, 6.4], "dracaena"), plant3([30.9, 6.2], "aspidistra"),
        # torens, toiletten, techniek
        *achthoektoren([33.9, 15.4], 2.4, 180, "was", lockers=(2, 6)), dict(t="box", soort="toiletgroep", c=[33.9, 5.6], w=4.0, d=2.4, h=2.6, a=0, kleur="#bdb7aa"), label([33.9, 5.6], "toiletten"),
        dict(t="box", soort="techniek", c=[33.9, 21.3], w=3.6, d=2.4, h=2.6, a=0, kleur="#8f8a80"), label([33.9, 21.3], "techniek"), plant3([32.0, 9.4], "sansevieria"), plant3([35.9, 9.4], "zz-plant"), hangplant([33.9, 9.6], 3.5), plant3([31.8, 1.0], "zz-plant"), plant3([35.8, 1.0], "zz-plant"),
        wand([[36.3, 0.2], [36.3, 3.4]], 6.0, gym=True), deur([36.3, 4.0], 90, toegang=True), wand([[36.3, 4.6], [36.3, 10.4]], 6.0, gym=True), deur([36.3, 11.0], 90, toegang=True),
        wand([[36.3, 11.6], [36.3, 22.8]], 6.0, gym=True), wand([[36.3, 8.0], [45.8, 8.0]], 6.0, gym=True),
        # gym
        deur([42.0, 23.0], 0, toegang=True, w=1.2), *[x for v in (9.6, 12.7, 15.8) for x in rack([44.6, v], 0)], *rack([41.4, 9.6], 0),
        *[roeier([38.4, v], 0) for v in (20.2, 21.1, 22.0)],
        dict(t="kleed", c=[39.6, 14.6], w=4.0, d=4.0, a=0, kleur="#c7928a"), label([39.6, 14.6], "matvloer"),
        dict(t="box", soort="kettlebells", c=[36.8, 14.6], w=2.4, d=0.5, h=0.9, a=90, kleur=STAAL), *achthoektoren([43.4, 20.2], 2.25, 180, "douche"),
        boom3([41.0, 17.6], "kentia"), plant3([37.0, 9.0], "sansevieria"), hangplant([44.6, 12.7], 4.0), plant3([36.8, 18.4], "sansevieria"), hangplant([39.6, 14.6], 4.0), boom3([45.0, 18.6], "dracaena"),
        # studio
        dict(t="kleed", c=[40.6, 4.0], w=7.0, d=6.0, a=0, kleur="#b8633f"), dict(t="box", soort="spiegelwand", c=[41.0, 0.35], w=8.0, d=0.1, h=2.2, a=0, kleur="#c9c3b6"),
        dict(t="box", soort="mattenrek", c=[45.4, 4.0], w=2.0, d=0.5, h=1.6, a=90, kleur=HOUT), boom3([37.4, 7.0], "kentia"), plant3([45.2, 7.2], "philodendron"), plant3([45.3, 1.2], "aspidistra"), hangplant([40.6, 4.0], 4.0),
        # verdieping: bieb en stille kamers
        *focuskamer([2.35, 9.0], 90, _AS), *focuskamer([2.35, 11.3], 90, _AS), *focuskamer([2.35, 13.6], 90, _AS), *[pod2([4.35, v], _AS) for v in (9.1, 10.6, 12.1, 13.6)],
        *kasten(1.5, 5.0, 22.45, d=0.35, h=2.4, n=_AS), dict(t="box", soort="fauteuil", c=[1.9, 20.0], w=0.8, d=0.8, h=0.8, a=0, kleur="#e5d48c", n=_AS),
        dict(t="box", soort="fauteuil", c=[1.9, 17.4], w=0.8, d=0.8, h=0.8, a=0, kleur="#e5d48c", n=_AS), *tafeltje([3.8, 18.6], _AS, 2),
        boom3([4.0, 15.6], "kentia", _AS), plant3([1.8, 1.0], "aspidistra", _AS), plant3([4.6, 21.4], "monstera", _AS), plant3([1.8, 15.6], "zz-plant", _AS), hangplant([1.6, 6.0], 2.6, _AS), plant3([4.6, 7.0], "philodendron", _AS),
        # buiten
        *tafeltje([8.0, 25.2], 0, 4), *tafeltje([11.4, 25.2], 0, 4), *tafeltje([14.8, 25.2], 0, 4), dict(t="box", soort="plantenbak", c=[11.5, 27.2], w=11.0, d=0.5, h=0.6, a=0, kleur=WALNOOT),
        label([-3.0, 16.0], "fietsen"), boom([-4.0, 4.0], 0.9, 3.0), boom([18.5, 28.5], 0.9, 3.0),
    ],
    dak=dict(soort="pv", terras=None, groen=[], pv=[R(6.0, 1.0, 17.0, 22.0), R(36.8, 1.0, 45.4, 22.0)],
             koepels=[[19.6, 12.3, 0.8], [24.4, 12.3, 0.8], [29.2, 12.3, 0.8], [19.6, 16.7, 0.8], [24.4, 16.7, 0.8], [29.2, 16.7, 0.8], [10.0, 15.0, 0.8], [41.0, 15.0, 0.8]],
             tekst="Bestaand plat dak uit 2003 met enkele lichtkoepels; acht nieuwe koepels boven werkzone, café en gym, zonnepanelen boven café en gym. Geen dakterras: gedeeld pand met Martin-ovenweg 19.",
             tekst_en="A long flat-roofed industrial strip from 2003 attached to a large dark industrial hall, a row of new round roof lights above the middle, solar panels at both ends; "
                      "a street with trees at the short end and a paved courtyard with parking along the long glass facade."),
    renders=dict(buiten=[]),
)
ONTWERPEN.update({"utrecht-amsterdamsestraatweg-656d": AMSTERDAMSESTRAATWEG})
LABELS.update({"utrecht-amsterdamsestraatweg-656d": {"Entree en lockers": [3.2, 17.4], "Café, keuken en tafeltennis": [11.4, 18.4], "Werkzone onder de lichtkoepels": [24.4, 16.7],
                                                     "Vergaderen langs de blinde gevel": [24.4, 7.6], "Wastoren, toiletten en techniek": [33.9, 10.4], "Gym (eigen deur)": [41.0, 11.6],
                                                     "Studio": [40.6, 5.0], "Bieb en stille kamers": [3.2, 6.4]}})
VIDES.update({"utrecht-amsterdamsestraatweg-656d": [dict(naam="Vide: hal op volle hoogte", poly=R(5.2, 0.2, 45.8, 22.8), n=1)]})
