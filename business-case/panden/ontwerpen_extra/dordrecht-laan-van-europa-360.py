# ---------------------------------------------------------------- Ronde 9 (15 november 2026): Laan van Europa 360, Dordrecht (Businesspark Amstelwijck)
# Hoekunit uit 2023 van 28 x 9,1 m in een bedrijfsverzamelgebouw van 10 units (BAG: eigen pand 238 m², vbo 415 m² industrie- en kantoorfunctie; buren 340 en 370
# idem, geen woningen). Twee lagen: begane grond 3,73 m vrij (betonvloer 1.500 kg/m²), verdieping 3,80 m vrij met lichtstraat (400 kg/m²).
# u = 0 tot 3,1 is de schuine voorgevel (zuidzuidwest, kantoren en overheaddeur), v = 0 de zijgevel (oostzuidoost) met ramen en een extra entree aan de zijstraat,
# v = 9,1 en u = 28 zijn cellenbeton scheidingswanden met de buurunits. Advertentie: kantoor 52 + 95 m², multifunctioneel 180 + 126 m², 5 parkeerplaatsen.
_DD = 1
DORDRECHT = dict(
    titel="Laan van Europa 360, Dordrecht",
    sub="Nieuwe hoekunit uit 2023 van 28 x 9 m op twee lagen van 3,7 m in bedrijfsverzamelgebouw Amstelwijck, label A+++, 5 eigen parkeerplaatsen. Te koop, bijgewerkt 13-11-2026.",
    hoogte=8.4, niveaus={"1": 4.0}, pui_h=3.2,
    concept="Een smalle, lage strook op twee lagen. Beneden door de nieuwe glazen voorgevel (waar de overheaddeur zat) het café met een lange tafel aan de zijramen, "
            "keuken en kookeiland tegen de buurwand en de trap naar boven. Halverwege de achthoekige wastoren met lockers als buffer, met langs de zijramen de gang naar "
            "de gym achterin, die een eigen deur heeft in de zijgevel. Boven aan de voorkant de werkzone met een raambar langs de zijramen en twee eilanden, in het midden "
            "onder de lichtstraat de stille kamers, en achterin boven de gym de lounge en bieb met de vergaderkamer en de sta-kamer. Sober: alles is nieuw en afgewerkt, "
            "er wordt alleen ingericht, met hergebruikte meubels en wanden van oude ramen.",
    geluid="Gym beneden achterin tegen de buurunit 340 (bedrijf, geen woningen), met een dichte wand tot de verdiepingsvloer en een deur op toegangspas; de wastoren ligt "
           "tussen café en gym. De verdiepingsvloer is beton: 40 mm rubber op een akoestische ondervloer en platforms, geen springen en geen gewichten laten vallen voor 7:00. "
           "Boven de gym alleen lounge, bieb en vergaderen; de werkzone ligt boven het café, 11 m van de gym.",
    pui=[[[0.0, 0.0], [1.7, 4.8]], [[1.7, 4.8], [3.1, 9.1]], [[1.0, 0.0], [15.8, 0.0]], [[17.2, 0.0], [27.0, 0.0]]],
    zones=[
        zone("Café aan de voorgevel", "café", [[0.3, 0.2], [11.0, 0.2], [11.0, 8.9], [3.3, 8.9], [1.8, 4.6]],
             "Door de nieuwe glazen voorgevel kom je in het café: een lange tafel voor twaalf aan de zijramen (ochtendzon), een keuken van 5 m tegen de buurwand, "
             "een kookeiland met de espressomachine en de stalen trap naar de werkzone. Strelitzia en kentia aan het glas.",
             ["Lange tafel van 4,2 m voor twaalf aan de zijramen", "Keuken van 5 m en kookeiland", "Glazen pui waar de overheaddeur zat", "Trap naar de verdieping"],
             cam=dict(t=[6.0, 4.5], afstand=8, hoek=200),
             prompt="The café of a members club in a brand new business unit with a 3.7 m concrete ceiling: a glass front where the roller door used to be, a long oak table for twelve along side windows, "
                    "an olive green kitchen from second-hand stainless steel worktables against the side wall, a reclaimed wood island with an espresso machine, a black steel stair, a strelitzia and a kentia palm."),
        zone("Wastoren en gang", "sanitair", R(11.0, 0.2, 16.5, 8.9),
             "Halverwege de achthoekige wastoren met drie toiletten en lockers in twee buitenzijden, langs de zijramen de gang naar de gym met de deur op toegangspas.",
             ["Wastoren van 4,3 m met drie toiletten", "Lockers in twee zijden van de toren", "Gang van 3,9 m breed langs de zijramen"],
             cam=dict(t=[13.4, 3.0], afstand=6, hoek=90),
             prompt="An octagonal concrete-look bathroom tower (eight flat faces), 3 m high, in a narrow new business unit with a 3.7 m concrete ceiling, a V-shaped concrete wash trough with brass taps, "
                    "dark green lockers built into two outer faces, ivy along the top rim, side windows with morning light."),
        zone("Gym (eigen deur)", "gym", R(16.5, 0.2, 27.8, 8.9),
             "Achterin beneden: twee racks op platforms, twee roeiers, een matvloer en kettlebells, met een eigen deur in de zijgevel en de D-vormige douchetoren in de hoek. "
             "Zijramen voor daglicht, dichte wand naar de gang.",
             ["Twee racks op zwevende platforms", "Twee roeiers", "Matvloer van 3,6 x 3 m", "D-vormige douchetoren met vier douches", "Eigen deur op toegangspas in de zijgevel"],
             cam=dict(t=[22.0, 4.5], afstand=8, hoek=180),
             prompt="A compact functional gym in a narrow new business unit with a 3.7 m concrete ceiling and side windows: two black power racks on oak platforms, two rowing machines, a mat area, "
                    "kettlebells, anthracite rubber floor, one wall oxblood red, a D-shaped concrete-look shower tower against the back wall."),
        dict(zone("Werkzone aan de voorkant", "werken", [[0.3, 0.2], [10.6, 0.2], [10.6, 8.9], [3.3, 8.9], [1.8, 4.6]],
                  "Het kantoor op de verdieping: een raambar van 8,8 m langs de zijramen en twee eilanden van vier zit-sta bureaus met de schermen haaks op het raam, "
                  "met daglicht van voren en van opzij.",
                  ["Raambar van 8,8 m (14 krukken)", "Twee eilanden van vier bureaus 140 x 70", "Ficus en kentia aan het glas"], n=_DD, cam=dict(t=[6.0, 4.5], afstand=8, hoek=200),
                  prompt="A small coworking room on the first floor of a new business unit: a long oak window bar along side windows, two islands of four compact sit-stand desks, "
                         "slate blue chairs, a glass front at the end, wood wool acoustic panels, a ficus and a kentia palm."), tussenvloer=False),
        dict(zone("Stille kamers", "vergader", R(10.6, 0.2, 16.5, 8.9),
                  "Onder de lichtstraat, boven de wastoren: twee focuskamers en vier belcellen, en de lockerwand voor de eigenaren.",
                  ["Twee focuskamers", "Vier belcellen", "Lockerwand van 3,6 m"], n=_DD, cam=dict(t=[13.5, 4.5], afstand=6, hoek=180),
                  prompt="A quiet corridor under a long roof light with two tiny glass focus rooms made of reclaimed windows, round slate blue felt phone booths, a dark green locker wall with pothos on top."), tussenvloer=False),
        dict(zone("Lounge en vergaderen", "bieb", R(16.5, 0.2, 27.8, 8.9),
                  "Achterin boven: een zeshoekige bank rond een sfeerhaard, een zitnis langs de zijramen, een boekenwand tegen de achterwand, een vergaderkamer voor zes en een sta-kamer.",
                  ["Zeshoekige bank", "Zitnis van 3,4 m langs de zijramen", "Boekenwand van 8 m", "Vergaderkamer voor 6 en sta-kamer voor 5"], n=_DD, cam=dict(t=[22.0, 4.5], afstand=8, hoek=180),
                  prompt="A lounge and library on the first floor of a new business unit: a hexagonal olive velvet bench around a fireplace, a built-in bench along side windows, a walnut bookcase wall, "
                         "a meeting room behind reclaimed windows, a roof light above."), tussenvloer=False),
    ],
    buiten=[dict(naam="Terras voor de zijgevel", poly=R(1.0, -3.0, 9.0, -0.2), kleur="#d5bd96"),
            dict(naam="Parkeerplaats en groen", poly=R(-6.0, -11.5, 30.0, -3.2), kleur="#c9c3b6")],
    elementen=[
        # café
        deur([0.85, 2.4], 71, w=1.6), *grote_tafel([6.4, 1.9], 4.2, 0), *keuken([6.5, 8.55], 5.0, 0), *kookeiland([6.5, 6.1], 0),
        dict(t="box", soort="trap", c=[10.0, 5.8], w=1.1, d=4.4, h=0.3, a=0, kleur=STAAL), label([10.0, 3.2], "trap"),
        plant3([1.3, 0.9], "strelitzia nicolai"), boom3([3.4, 6.6], "kentia"), plant3([10.6, 0.9], "monstera"), *[hangplant([u, 1.9], 3.2) for u in (5.2, 7.6)],
        dict(t="box", soort="garderobe", c=[3.3, 4.3], w=1.6, d=0.4, h=1.8, a=0, kleur=WALNOOT),
        # wastoren en gang
        *achthoektoren([13.6, 6.6], 2.3, 270, "was", lockers=(6, 7)), plant3([15.9, 4.0], "sansevieria"), hangplant([13.6, 2.0], 3.2), hangplant([2.8, 6.2], 3.2), plant3([11.4, 4.0], "zz-plant"),
        wand([[16.5, 0.2], [16.5, 1.3]], 3.7, gym=True), deur([16.5, 1.9], 90, toegang=True), wand([[16.5, 2.5], [16.5, 8.9]], 3.7, gym=True),
        # gym
        deur([18.0, 0.0], 0, toegang=True), *rack([26.4, 1.6], 0), *rack([23.5, 1.6], 0), roeier([18.9, 8.3], 0), roeier([18.9, 7.4], 0),
        dict(t="kleed", c=[20.6, 4.2], w=3.6, d=3.0, a=0, kleur="#c7928a"), label([20.6, 4.2], "matvloer"),
        dict(t="box", soort="kettlebells", c=[17.0, 5.4], w=2.4, d=0.5, h=0.9, a=90, kleur=STAAL), *dtoren([27.6, 8.9], [23.0, 8.9], 0.8, "douche"),
        plant3([22.4, 6.6], "sansevieria"), boom3([17.4, 3.3], "dracaena"), boom3([25.0, 4.4], "kentia"), hangplant([20.6, 4.2], 3.2),
        # verdieping: werkzone
        dict(t="box", soort="raambar", c=[5.9, 0.45], w=8.8, d=0.5, h=1.05, a=0, kleur=HOUT, n=_DD), *eiland2([4.6, 4.4], 90, _DD), *eiland2([9.0, 4.4], 90, _DD),
        boom3([2.6, 2.4], "ficus elastica", _DD), boom3([6.8, 8.0], "kentia", _DD), *[hangplant([u, 4.4], 3.3, _DD) for u in (4.6, 9.0)], plant3([3.9, 8.4], "dracaena", _DD),
        # verdieping: stille kamers
        *focuskamer([12.0, 1.35], 0, _DD), *focuskamer([14.3, 1.35], 0, _DD), *[pod2([u, 4.6], _DD) for u in (11.7, 13.2, 14.7)], pod2([15.7, 3.0], _DD),
        *lockerwand([13.6, 8.6], 3.6, 0, _DD), plant3([11.2, 7.6], "aspidistra", _DD), boom3([16.0, 7.4], "kentia", _DD), plant3([11.0, 2.9], "zz-plant", _DD), hangplant([13.2, 3.0], 3.3, _DD),
        # verdieping: lounge en vergaderen
        *vergaderkamer([19.2, 7.2], 4.6, 3.2, 0, 6, _DD), *stavergaderkamer([23.3, 7.2], 3.4, 3.2, 0, 5, _DD),
        *veelhoekbank([20.6, 2.6], 1.7, 6, open=(1, 4), n=_DD), *zitnis([23.6, 0.2], [27.0, 0.2], n=_DD), *kasten(1.2, 5.6, 27.45, a=90, d=0.35, h=2.6, n=_DD),
        dict(t="box", soort="fauteuil", c=[17.4, 4.4], w=0.8, d=0.8, h=0.8, a=20, kleur="#e5d48c", n=_DD), boom3([17.3, 1.4], "ficus elastica", _DD), plant3([26.6, 4.9], "monstera", _DD), plant3([25.4, 4.0], "philodendron", _DD),
        hangplant([20.6, 2.6], 3.3, _DD),
        # buiten
        *tafeltje([3.4, -1.5], 0, 2), *tafeltje([6.6, -1.5], 0, 2), dict(t="box", soort="plantenbak", c=[5.0, -2.8], w=7.6, d=0.4, h=0.6, a=0, kleur=WALNOOT),
        plant3([8.6, -1.2], "olijf"), label([15.0, -6.0], "5 eigen parkeerplaatsen"), boom([-4.0, -9.0], 0.9, 3.0),
    ],
    dak=dict(soort="pv", terras=None, groen=[], pv=[R(1.5, 0.6, 9.5, 8.5), R(21.0, 0.6, 27.4, 8.5)], koepels=[],
             tekst="Nieuw geïsoleerd staaldak uit 2023 met 13 zonnepanelen en een lichtstraat boven het midden; extra panelen erbij. Geen dakterras: unit in een verzamelgebouw met mandelige grond.",
             tekst_en="Flat roof of the corner unit of a new row of ten business units from 2023, a long roof light in the middle, solar panels front and back; "
                      "the other units stay plain grey, a side street with parking along the long facade."),
    renders=dict(buiten=[]),
)
ONTWERPEN.update({"dordrecht-laan-van-europa-360": DORDRECHT})
LABELS.update({"dordrecht-laan-van-europa-360": {"Café aan de voorgevel": [6.6, 4.3], "Wastoren en gang": [13.6, 2.6], "Gym (eigen deur)": [21.8, 6.4],
                                                 "Werkzone aan de voorkant": [6.8, 3.0], "Stille kamers": [13.4, 6.4],
                                                 "Lounge en vergaderen": [22.8, 4.6]}})
