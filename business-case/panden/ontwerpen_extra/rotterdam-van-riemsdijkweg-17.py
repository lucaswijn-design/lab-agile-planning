# ---------------------------------------------------------------- Ronde 9 (16 november 2026): Van Riemsdijkweg 17, Rotterdam Waalhaven
# Bedrijfspand uit 1957 van 40 x 15 m in een rij, label A+, erfpacht. Advertentie: showroom 159 + hal 404 + kantoor 154 m² (kantoor op een verdieping boven de showroom, aanname),
# hal 5,2 m vrij hoog met een lichtstraat (luchtfoto: circa u 16 tot 37, v 6,5 tot 10). Lokaal stelsel: u 0 = straatgevel aan de Van Riemsdijkweg (oost),
# u 40 = achtergevel (west, vrij, kijkt uit op het terrein van de buren), v 0 en v 15 = gemeenschappelijke wanden met de buurpanden (noord en zuid).
# Aanname: showroom en kantoor beslaan de voorste 10,5 m; de hal loopt van u 10,5 tot 40.
RIEMSDIJK = dict(
    titel="Van Riemsdijkweg 17, Rotterdam Waalhaven",
    sub="Bedrijfspand uit 1957 van 40 x 15 m met showroom aan de straat, kantoor erboven en een hal van 5,2 m hoog met lichtstraat; label A+, erfpacht",
    hoogte=6.5, niveaus={"1": 3.6}, pui_h=3.2,
    concept="Een lange strook van straat naar achter, van druk naar stil naar zweet. In de showroom aan de straat het café: raambar achter het glas, keuken langs de wand, "
            "kookeiland, lange tafel en een zeshoekige bank. Daarachter de hal onder de lichtstraat: zes eilanden van vier bureaus, langs de noordwand een vergaderkamer, een sta-kamer "
            "en vijf belcellen, langs de zuidwand lockers en twee focuskamers. Dan de wastoren en de douchetoren als buffer, en achterin de gym met nieuwe ramen in de westgevel. "
            "Boven de showroom het bestaande kantoor als stille verdieping: drie eilanden aan de straatramen, een vergaderkamer, twee focuskamers en twee belcellen. "
            "Sober: de hal uit 1957 blijft zichtbaar, vloer strak schuren en coaten, wanden van oude ramen.",
    geluid="Gym helemaal achterin, 22 m van de straat, met de twee torens en een dichte wand tot het dak (6 m buffer) tussen gym en werken. "
           "De buurpanden aan weerszijden zijn bedrijfspanden in de Waalhaven, geen woningen. 40 mm rubber op een akoestische ondervloer, platforms onder de racks.",
    pui=[[[0.0, 0.5], [0.0, 14.5]], [[40.0, 2.0], [40.0, 13.0]]],
    zones=[
        zone("Café in de showroom", "café", R(0.3, 0.3, 10.5, 14.7),
             "Achter de showroomramen aan de straat: een raambar van 6 m achter het glas, de keuken van 5,6 m langs de noordwand met een kookeiland, een lange tafel voor twaalf en een "
             "zeshoekige bank rond een haard. De trap naar het kantoor staat tegen de achterwand.",
             ["Raambar van 6 m achter de showroomramen", "Keuken van 5,6 m uit tweedehands rvs, kookeiland met espressomachine", "Lange tafel van 4,2 m voor twaalf",
              "Zeshoekige bank met twee open zijden rond een sfeerhaard", "Bank van 3,6 m langs de zuidwand en drie fauteuils", "Toiletgroep bij de entree (twee toiletten en een toegankelijk toilet)"],
             cam=dict(t=[5.2, 7.5], afstand=9, hoek=0),
             prompt="The café of a members club in an old 1950s car showroom with large street windows: an oak window bar with stools behind the glass, an olive green kitchen from second-hand stainless steel worktables along the side wall, "
                    "a reclaimed wood island with an espresso machine, a long oak table for twelve, a hexagonal olive velvet bench around a black fireplace, a strelitzia at the window."),
        zone("Werkzone onder de lichtstraat", "werken", R(10.5, 3.4, 25.0, 12.3),
             "Zes eilanden van vier zit-sta bureaus onder de lichtstraat in de hal van 5,2 m hoog. Pothos hangt aan de spanten boven de eilanden.",
             ["Zes eilanden van vier bureaus 140 x 70", "Bestaande lichtstraat, houtwolplaten tegen de wanden", "Looppaden van 1,1 m of meer"],
             cam=dict(t=[18.0, 8.0], afstand=9, hoek=180),
             prompt="A coworking floor in a 1957 industrial hall 5 m high with a long roof light: six islands of four compact sit-stand desks with oak tops, slate blue chairs, wood wool acoustic panels on the walls, pothos hanging from the trusses, a smooth sealed concrete floor."),
        zone("Kamers langs de wanden", "vergader", R(10.5, 0.3, 25.0, 3.4),
             "Langs de noordwand een vergaderkamer voor zes, een sta-kamer en vijf belcellen; langs de zuidwand een lockerwand en twee focuskamers.",
             ["Vergaderkamer voor zes", "Sta-kamer met statafel", "Vijf belcellen", "Lockerwand van 6 m en twee focuskamers aan de zuidwand"], cam=dict(t=[17.0, 2.0], afstand=7, hoek=90),
             prompt="A row of small rooms with walls of reclaimed steel and timber windows along the wall of a 1957 hall: a meeting room for six, a stand-up meeting room with a round high table, round slate blue felt phone booths."),
        zone("Lockers en focus", "bieb", R(10.5, 12.3, 25.0, 14.7), "Langs de zuidwand: lockerwand van 6 m en twee focuskamers.", ["Lockerwand van 6 m", "Twee focuskamers"],
             cam=dict(t=[17.0, 13.0], afstand=6, hoek=270),
             prompt="A long wall of green lockers with trailing pothos on top and two small glass focus rooms made of reclaimed windows in a 1957 industrial hall."),
        zone("Torens", "sanitair", R(25.0, 0.3, 31.0, 14.7),
             "De wastoren (5,5 m) en de douchetoren (4,5 m) als buffer tussen werken en gym, met lockers op de buitenzijden langs de gang naar de gymdeur.",
             ["Wastoren met drie toiletten en een V-wastrog", "Douchetoren met vier douches, open naar de gym", "Dagkluisjes op beide torens"], cam=dict(t=[28.0, 8.0], afstand=8, hoek=180),
             prompt="Two octagonal concrete-look bathroom towers (flat faces, they still read as round objects), 3 m high, in a 1957 industrial hall with a long roof light, board-marked plaster, a V-shaped wash trough with brass taps, ivy along the top rim, lockers in an outer face."),
        zone("Gym achterin (afsluitbaar)", "gym", R(31.0, 0.3, 39.7, 14.7),
             "Achterin onder de volle hoogte en het eind van de lichtstraat: drie racks op platforms, een groepslesvloer en roeiers bij nieuwe ramen in de westgevel. Dichte wand en deur op toegangspas.",
             ["Drie racks op zwevende platforms", "Groepslesvloer van 5 x 4 m", "Nieuwe ramen in de westgevel", "Douchetoren direct vanuit de gym"],
             cam=dict(t=[35.4, 8.0], afstand=9, hoek=0),
             prompt="A functional gym at the back of a 1957 industrial hall 5 m high under a long roof light, closed off by a solid wall: three black power racks on oak platforms, a mat area, rowing machines facing new steel windows, anthracite rubber floor, one wall oxblood red, plants."),
        dict(zone("Stille verdieping in het kantoor", "werken", R(0.3, 0.3, 10.3, 14.7),
                  "Het bestaande kantoor boven de showroom: drie eilanden aan de straatramen, een vergaderkamer voor zes, twee focuskamers en twee belcellen.",
                  ["Drie eilanden van vier bureaus", "Vergaderkamer voor zes", "Twee focuskamers en twee belcellen"], n=1, cam=dict(t=[4.0, 6.0], afstand=7, hoek=0),
                  prompt="A quiet upper-floor office in a 1957 industrial building turned into a calm work room: islands of compact sit-stand desks at large street windows, a meeting room and small focus rooms with walls of reclaimed windows, plants."), tussenvloer=False),
    ],
    buiten=[dict(naam="Terras aan de straat", poly=R(-5.6, 0.5, -0.3, 9.0), kleur="#d5bd96"), dict(naam="Parkeren en fietsen", poly=R(-5.6, 9.5, -0.3, 14.5), kleur="#c9c3b6"),
            dict(naam="Straat", poly=R(-16.0, -10.0, -6.0, 26.0), kleur="#9a958c")],
    elementen=[
        # café in de showroom
        dict(t="box", soort="raambar", c=[0.55, 7.5], w=6.0, d=0.5, h=1.05, a=90, kleur=HOUT), *keuken([5.0, 0.65], 5.6, 0), *kookeiland([5.0, 2.6], 0),
        *grote_tafel([5.2, 6.4], 4.2, 0), *veelhoekbank([5.4, 10.6], 1.8, 6, open=(1, 4)), dict(t="box", soort="trap", c=[9.5, 3.2], w=1.1, d=4.4, h=0.3, a=0, kleur=STAAL),
        label([9.5, 0.6], "trap"), deur([0.0, 12.6], 90, w=1.4), dict(t="kleed", c=[1.8, 12.6], w=2.0, d=2.4, a=0, kleur="#d5bd96"),
        dict(t="box", soort="fauteuil", c=[8.6, 9.6], w=0.8, d=0.8, h=0.8, a=90, kleur="#5a2741"), dict(t="box", soort="fauteuil", c=[8.6, 10.6], w=0.8, d=0.8, h=0.8, a=90, kleur="#5a2741"),
        dict(t="box", soort="fauteuil", c=[8.6, 11.6], w=0.8, d=0.8, h=0.8, a=90, kleur="#5a2741"),
        dict(t="box", soort="toiletgroep", c=[8.4, 13.4], w=3.6, d=2.4, h=2.6, a=0, kleur="#bdb7aa"), label([8.4, 13.4], "toiletten"),
        plant3([0.9, 2.6], "strelitzia nicolai"), boom3([1.2, 14.0], "kentia"), *[hangplant([u, 6.4], z=3.0) for u in (3.6, 6.8)],
        *zitnis([6.4, 14.45], [2.8, 14.45], tafels=False), *[hangplant([u, 13.6], z=3.0) for u in (3.6, 5.6)], plant3([10.1, 6.6], "monstera"), plant3([9.8, 9.0], "philodendron"),
        # werkzone onder de lichtstraat
        *eiland2([14.0, 6.0], 0), *eiland2([18.4, 6.0], 0), *eiland2([22.8, 6.0], 0), *eiland2([14.0, 10.4], 0), *eiland2([18.4, 10.4], 0), *eiland2([22.8, 10.4], 0),
        *[hangplant([u, v], z=4.2) for u in (14.0, 18.4, 22.8) for v in (6.0, 10.4)], plant3([16.2, 8.2], "zz-plant"), plant3([20.6, 8.2], "zz-plant"), boom3([11.4, 8.2], "kentia"), boom3([24.4, 8.2], "kentia"),
        *[hangplant([u, 12.4], z=4.0) for u in (12.5, 16.2, 20.6, 24.4)], *[hangplant([u, 3.9], z=4.0) for u in (16.2, 20.6, 24.4)],
        # kamers langs de noordwand
        *vergaderkamer([13.1, 1.8], 4.6, 3.0, 0, 6), *stavergaderkamer([17.0, 1.6], 2.4, 2.6, 0, 5), pod2([18.95, 1.0]), pod2([20.35, 1.0]), pod2([21.75, 1.0]), pod2([23.15, 1.0]), pod2([24.55, 1.0]),
        # lockers en focus langs de zuidwand
        *lockerwand([14.0, 14.45], 6.0, 0), *focuskamer([19.4, 13.6], 0), *focuskamer([21.8, 13.6], 0), plant3([23.9, 13.9], "aspidistra"),
        # torens
        *achthoektoren([28.0, 3.2], 2.75, 180, "was", lockers=(6,)), *achthoektoren([28.0, 12.2], 2.25, 0, "douche", lockers=(6,)),
        # gym
        wand([[31.0, 0.3], [31.0, 7.4]], 6.0, gym=True), deur([31.0, 7.9], 90, toegang=True), wand([[31.0, 8.4], [31.0, 9.8]], 6.0, gym=True),
        wand([[31.0, 9.8], [30.2, 9.8]], 3.0, gym=True), wand([[31.0, 14.6], [30.2, 14.6]], 3.0, gym=True),
        *rack([32.6, 1.6], 0), *rack([35.2, 1.6], 0), *rack([37.8, 1.6], 0), dict(t="kleed", c=[35.0, 8.0], w=5.0, d=4.0, a=0, kleur="#c7928a"), label([35.0, 8.0], "groepsles"),
        roeier([38.9, 7.6], 90), roeier([38.0, 7.6], 90), dict(t="box", soort="kettlebells", c=[35.0, 14.45], w=3.0, d=0.5, h=0.9, a=0, kleur=STAAL),
        plant3([39.2, 11.0], "strelitzia nicolai"), plant3([32.0, 13.8], "sansevieria"), boom3([39.0, 4.0], "kentia"), boom3([38.8, 13.6], "kentia"), plant3([32.0, 6.0], "monstera"), plant3([32.0, 10.0], "aspidistra"),
        # verdieping: kantoor boven de showroom
        *eiland2([2.4, 3.0], 0, 1), *eiland2([2.4, 7.4], 0, 1), *eiland2([6.4, 7.4], 0, 1), pod2([6.0, 1.4], 1), pod2([7.5, 1.4], 1), label([9.5, 3.2], "trap", 1),
        *vergaderkamer([7.6, 11.6], 4.6, 3.0, 0, 6, 1), *focuskamer([2.2, 11.2], 0, 1), *focuskamer([2.2, 13.4], 0, 1),
        boom3([4.4, 9.6], "kentia", 1), boom3([9.4, 8.4], "ficus elastica", 1), plant3([9.7, 14.3], "zz-plant", 1), hangplant([6.4, 9.2], z=2.4, n=1), boom3([4.6, 13.7], "kentia", 1), *[hangplant([u, v], z=2.4, n=1) for u, v in ((2.4, 5.2), (4.4, 7.4))],
        # buiten
        *tafeltje([-2.4, 2.6], 0, 4), *tafeltje([-2.4, 6.4], 0, 4), dict(t="box", soort="plantenbak", c=[-5.2, 4.8], w=7.0, d=0.5, h=0.6, a=90, kleur=WALNOOT),
        boom([-4.6, 1.0], 0.9, 3.4), boom([-4.6, 8.6], 0.9, 3.4), boom([-4.8, 13.8], 0.8, 3.0), boom([-2.0, 14.2], 0.8, 3.0), label([-3.0, 12.0], "fietsen + 2 parkeerplaatsen"),
    ],
    dak=dict(soort="pv", terras=None, groen=[], pv=[R(11.0, 0.8, 39.4, 6.0), R(11.0, 10.6, 39.4, 14.2)],
             koepels=[[18.0, 8.2, 0.9], [26.0, 8.2, 0.9], [34.0, 8.2, 0.9], [5.0, 7.5, 0.8]],
             tekst="Plat dak van de hal met de bestaande lichtstraat in het midden; zonnepanelen op de twee stroken ernaast. Op het kantoordeel een lichtkoepel. Geen dakterras: rij van bedrijfspanden.",
             tekst_en="The flat roof of a 1957 industrial hall in a row of similar halls in a port area, a long roof light along the middle, solar panels on both sides; neighbouring halls plain grey, a wide road with parked trucks in front."),
    renders=dict(buiten=[]),
)
ONTWERPEN.update({"rotterdam-van-riemsdijkweg-17": RIEMSDIJK})
LABELS.update({"rotterdam-van-riemsdijkweg-17": {"Café in de showroom": [5.2, 8.7], "Werkzone onder de lichtstraat": [18.4, 8.2], "Kamers langs de wanden": [17.0, 3.7],
                                                "Lockers en focus": [16.0, 13.4], "Torens": [28.0, 7.9], "Gym achterin (afsluitbaar)": [35.0, 11.4],
                                                "Stille verdieping in het kantoor": [5.0, 5.2]}})
