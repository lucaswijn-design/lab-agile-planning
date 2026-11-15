# ---------------------------------------------------------------- Ronde 9 (16 november 2026): Edelhertstraat 12, Capelle aan den IJssel ('s-Gravenland)
# Vrijstaande hal uit 1974 van 24,4 x 24,2 m op eigen grond (perceel 1.044 m²), vrije hoogte 4,7 m (oozo), vier lichtstraten oost-west over het dak (luchtfoto: v circa 3, 9, 15 en 21).
# Lokaal stelsel: u 0 = oostgevel aan het eigen erf (bestelbussen, parkeren), u 24,4 = westgevel aan de Edelhertstraat (bomenrij, sportpark aan de overkant),
# v 0 = noordgevel (op 0,4 m van een autodemontagebedrijf), v 24,2 = zuidgevel met een eigen strook van 5 m.
# Aanname (indeling onbekend): entree aan de straat, overheaddeur aan het erf.
EDELHERT = dict(
    titel="Edelhertstraat 12, Capelle aan den IJssel",
    sub="Vrijstaande hal uit 1974 van 24 x 24 m op eigen grond, 4,7 m vrij hoog met vier lichtstraten, aan een straat met bomen tegenover een sportpark",
    hoogte=5.8, pui_h=3.2,
    concept="Een vierkante hal in vier kwarten, met de lichtstraten als ritme. Aan de straatkant (west) de werkzone achter een nieuwe glazen gevel met een raambar, "
            "en in de zuidwesthoek het café met keuken, lange tafel en een zitnis in de zon langs de zuidgevel. Aan de erfkant (oost) de gym in de noordoosthoek, met een eigen deur "
            "naar het erf, zodat sporters om 6:00 binnen kunnen. Tussen gym en werken een strook van 6 m met de twee achthoekige torens. In de zuidoosthoek lounge en spel: "
            "pingpong, een zeshoekige bank, boekenkasten en twee focuskamers. Sober: de hal uit 1974 blijft zichtbaar, vloer strak schuren en coaten, wanden van oude ramen.",
    geluid="Gym in de noordoosthoek, tegen het autodemontagebedrijf aan de noordkant; geen woningen in of naast het pand (de woonwijk ligt 60 m noordelijker, achter de bedrijven). "
           "Tussen gym en werkzone de wastoren en de douchetoren in een strook van 6 m, en een dichte wand tot het dak. De gymdeur naar de club zit aan de loungekant. "
           "40 mm rubber op een akoestische ondervloer, platforms onder de racks.",
    pui=[[[24.4, 4.0], [24.4, 18.0]], [[15.0, 24.2], [23.5, 24.2]], [[0.0, 3.5], [0.0, 7.5]]],
    zones=[
        zone("Werkzone aan de straat", "werken", R(14.5, 0.3, 24.1, 14.0),
             "Achter een nieuwe glazen westgevel aan de Edelhertstraat: een raambar van 9 m met vijftien krukken, vier eilanden van vier bureaus onder de lichtstraten, en langs de noordwand "
             "een vergaderkamer voor zes, een sta-kamer en een belcel; aan de cafékant nog vijf belcellen.",
             ["Raambar van 9 m langs de nieuwe glazen westgevel", "Vier eilanden van vier bureaus 140 x 70, scherm haaks op het raam",
              "Vergaderkamer voor zes en sta-kamer aan de noordwand", "Zes belcellen"],
             cam=dict(t=[19.0, 7.5], afstand=9, hoek=0),
             prompt="A coworking zone in a square 1970s industrial hall 4.7 m high with long east-west roof lights: islands of compact sit-stand desks with oak tops, a long oak window bar behind a new glass facade made of reclaimed steel windows, "
                    "trees and a sports park across the street, slate blue chairs, wood wool acoustic panels, a meeting room with reclaimed windows along the back wall."),
        zone("Café in de zuidwesthoek", "café", R(14.5, 14.0, 24.1, 23.9),
             "Op de hoek van de straat en de zonkant: de voordeur, een keuken van 5 m tegen de torenstrook, een kookeiland, een lange tafel voor twaalf, een raambar aan de straat "
             "en een zitnis van 6,5 m langs de zuidgevel met uitzicht op het terras.",
             ["Keuken van 5 m uit tweedehands rvs, kookeiland met espressomachine", "Lange tafel van 4,2 m voor twaalf", "Zitnis van 6,5 m langs de zuidgevel", "Olijfboom en strelitzia in de zon"],
             cam=dict(t=[19.5, 19.0], afstand=9, hoek=0),
             prompt="The café of a members club in the sunny corner of a 1970s industrial hall with roof lights: new glass walls on two sides, an olive green kitchen from second-hand stainless steel worktables, a reclaimed wood island with an espresso machine, "
                    "a long oak table for twelve, an olive velvet bench seat with small tables along the south glass, an olive tree and a strelitzia in the sun, a terrace outside."),
        zone("Torens", "sanitair", R(8.5, 0.3, 14.5, 13.0),
             "Een strook van 6 m tussen gym en werken met de douchetoren (open naar de gym) en de wastoren (open naar de lounge), lockers op de buitenzijden.",
             ["Douchetoren van 4,5 m met vier douches, alleen vanuit de gym", "Wastoren van 5,5 m met drie toiletten en een V-wastrog", "Lockers op de zijden aan de werkzone"],
             cam=dict(t=[11.5, 7.0], afstand=8, hoek=0),
             prompt="Two octagonal concrete-look bathroom towers (flat faces, they still read as round objects), 3 m high, under long roof lights in a 1970s industrial hall, board-marked plaster, a V-shaped wash trough with brass taps, green lockers in an outer face, ivy along the top rim."),
        zone("Gym (eigen ingang aan het erf)", "gym", R(0.3, 0.3, 8.5, 13.0),
             "In de noordoosthoek: drie racks op platforms, een groepslesvloer, roeiers bij een nieuwe glazen deur naar het erf. Eigen ingang en een binnendeur naar de lounge, beide op toegangspas.",
             ["Drie racks op zwevende platforms", "Groepslesvloer van 4,4 x 4 m", "Eigen deur aan het erf op toegangspas", "Douchetoren direct vanuit de gym"],
             cam=dict(t=[4.4, 7.0], afstand=9, hoek=180),
             prompt="A functional gym in a 1970s industrial hall 4.7 m high under a long roof light, closed off by a solid wall: three black power racks on oak platforms, a mat area, rowing machines next to a new glass door to a yard, anthracite rubber floor, one wall oxblood red, plants."),
        zone("Lounge, spel en bieb", "bieb", R(0.3, 13.0, 14.5, 23.9),
             "In de zuidoosthoek naast de gym: pingpong, een zeshoekige bank rond een haard, boekenkasten langs de zuidgevel, lockers tegen de gymwand, een tweede vergaderkamer voor zes en twee glazen focuskamers in de hoek.",
             ["Pingpongtafel, inklapbaar", "Zeshoekige bank rond een sfeerhaard", "Boekenwand van 4 m", "Lockerwand van 5 m", "Vergaderkamer voor zes", "Twee focuskamers", "Toiletgroep naast de gymdeur (twee toiletten en een toegankelijk toilet)"],
             cam=dict(t=[7.0, 18.5], afstand=9, hoek=0),
             prompt="A lounge and game corner in a 1970s industrial hall with long roof lights: a ping pong table, a hexagonal olive velvet bench around a black fireplace, a walnut bookshelf wall, green lockers with trailing pothos, small glass focus rooms made of reclaimed windows, kentia palms."),
    ],
    buiten=[dict(naam="Erf (parkeren, bestelbussen)", poly=R(-10.0, 0.0, -0.3, 24.2), kleur="#c9c3b6"),
            dict(naam="Terras aan de zuidkant", poly=R(12.0, 24.4, 24.4, 29.2), kleur="#d5bd96"),
            dict(naam="Straat met bomenrij", poly=R(24.6, -10.0, 34.0, 34.0), kleur="#9a958c")],
    elementen=[
        # werkzone aan de straat
        dict(t="box", soort="raambar", c=[23.75, 9.0], w=9.0, d=0.5, h=1.05, a=90, kleur=HOUT),
        *eiland2([16.2, 5.2], 90), *eiland2([19.4, 5.2], 90), *eiland2([16.2, 10.2], 90), *eiland2([19.4, 10.2], 90),
        *vergaderkamer([17.5, 1.8], 4.6, 3.0, 0, 6), *stavergaderkamer([21.3, 1.6], 2.4, 2.6, 0, 5), pod2([23.4, 1.0]),
        pod2([15.4, 13.1]), pod2([16.8, 13.1]), pod2([18.2, 13.1]), pod2([19.6, 13.1]), pod2([22.0, 13.1]),
        *[hangplant([u, v], z=4.0) for u in (16.2, 19.4) for v in (5.2, 10.2)], plant3([17.8, 7.7], "zz-plant"), plant3([21.6, 7.7], "monstera"), boom3([23.4, 3.4], "ficus elastica"), *[hangplant([23.6, v], z=3.6) for v in (6.0, 9.0, 12.0)], plant3([14.9, 7.7], "zz-plant"),
        # café in de zuidwesthoek
        *keuken([14.85, 18.4], 5.0, 90), *kookeiland([16.9, 18.4], 90), *grote_tafel([20.2, 16.4], 4.2, 0), *zitnis([23.5, 23.65], [17.0, 23.65]),
        dict(t="box", soort="raambar", c=[23.75, 16.0], w=3.2, d=0.5, h=1.05, a=90, kleur=HOUT), deur([24.4, 19.2], 90, w=1.4), dict(t="kleed", c=[22.6, 19.2], w=2.2, d=2.0, a=0, kleur="#d5bd96"),
        boom3([23.4, 21.6], "olijf"), plant3([15.4, 23.3], "strelitzia nicolai"), boom3([15.6, 14.9], "kentia"), *[hangplant([u, 16.4], z=3.6) for u in (19.0, 21.4)],
        hangplant([16.9, 18.4], z=3.6), dict(t="box", soort="fauteuil", c=[19.6, 20.2], w=0.8, d=0.8, h=0.8, a=0, kleur="#5a2741"), dict(t="box", soort="fauteuil", c=[20.8, 20.2], w=0.8, d=0.8, h=0.8, a=0, kleur="#5a2741"),
        # torens
        *achthoektoren([11.5, 3.3], 2.25, 180, "douche"), *achthoektoren([11.5, 9.4], 2.75, 90, "was", lockers=(7,)),
        wand([[9.42, 2.65], [8.5, 2.65]], 3.0, gym=True), wand([[9.42, 3.95], [8.5, 3.95]], 3.0, gym=True),
        # gym
        wand([[8.5, 0.3], [8.5, 2.65]], 4.7, gym=True), wand([[8.5, 3.95], [8.5, 13.0], [6.6, 13.0]], 4.7, gym=True), deur([6.0, 13.0], 0, toegang=True), wand([[5.4, 13.0], [0.3, 13.0]], 4.7, gym=True),
        deur([0.0, 5.5], 90, toegang=True, w=1.2),
        *rack([1.6, 1.6], 0), *rack([4.2, 1.6], 0), *rack([6.8, 1.6], 0), dict(t="kleed", c=[4.6, 7.4], w=4.4, d=4.0, a=0, kleur="#c7928a"), label([4.6, 7.4], "groepsles"),
        roeier([0.9, 10.6], 90), roeier([1.9, 10.6], 90), dict(t="box", soort="kettlebells", c=[7.0, 12.7], w=2.4, d=0.5, h=0.9, a=0, kleur=STAAL),
        plant3([7.9, 9.8], "sansevieria"), boom3([4.6, 11.8], "kentia"), plant3([0.8, 8.0], "aspidistra"),
        # lounge, spel en bieb
        *lockerwand([2.9, 13.25], 5.0, 0), *pingpong([4.6, 17.6], 0), *veelhoekbank([10.6, 19.9], 1.9, 6, open=(1, 4)), *vergaderkamer([11.6, 15.2], 4.6, 3.0, 0, 6),
        *kasten(5.4, 9.4, 23.65, h=2.4, d=0.4), *focuskamer([1.5, 22.8], 0), *focuskamer([3.9, 22.8], 0),
        dict(t="box", soort="fauteuil", c=[13.4, 22.8], w=0.8, d=0.8, h=0.8, a=0, kleur="#47522a"), dict(t="box", soort="fauteuil", c=[12.2, 22.8], w=0.8, d=0.8, h=0.8, a=0, kleur="#47522a"),
        dict(t="box", soort="toiletgroep", c=[7.9, 14.9], w=2.4, d=3.0, h=2.6, a=0, kleur="#bdb7aa"), label([7.9, 14.9], "toiletten"), plant3([0.9, 19.0], "aspidistra"), *[hangplant([u, 21.0], z=4.0) for u in (5.0, 8.0)], plant3([16.2, 22.6], "philodendron"), hangplant([10.6, 19.9], z=4.0),
        plant3([0.8, 15.2], "zz-plant"), hangplant([4.6, 17.6], z=4.0), plant3([13.9, 17.3], "monstera"), plant3([8.2, 22.6], "sansevieria"),
        # buiten
        *tafeltje([15.0, 26.6], 0, 4), *tafeltje([18.6, 26.6], 0, 4), *tafeltje([22.2, 26.6], 0, 4), dict(t="box", soort="plantenbak", c=[18.2, 28.8], w=12.0, d=0.5, h=0.6, a=0, kleur=WALNOOT),
        boom([13.0, 27.0], 1.0, 3.6), boom([24.0, 26.0], 1.0, 3.6), boom([-1.6, 20.0], 0.9, 3.4), boom([-1.6, 23.0], 0.9, 3.4), boom([-1.6, 2.0], 0.9, 3.4), boom([-1.6, 9.5], 0.9, 3.4), label([-5.0, 12.0], "parkeren op eigen erf (circa 8 plaatsen)"),
    ],
    dak=dict(soort="pv", terras=None, groen=[], pv=[R(1.0, 4.4, 23.4, 8.0), R(1.0, 10.4, 23.4, 14.0), R(1.0, 16.4, 23.4, 20.0)],
             koepels=[],
             tekst="Plat dak met vier bestaande lichtstraten oost-west; zonnepanelen op de stroken ertussen. Geen dakterras: het terras komt op de eigen strook aan de zuidkant.",
             tekst_en="The flat roof of a freestanding square 1970s industrial hall with four long east-west roof lights and solar panels in between; a yard with vans on the east side, a street with a row of trees and a sports field to the west, a car scrapyard to the north."),
    renders=dict(buiten=[]),
)
ONTWERPEN.update({"capelle-edelhertstraat-12": EDELHERT})
LABELS.update({"capelle-edelhertstraat-12": {"Werkzone aan de straat": [19.0, 7.7], "Café in de zuidwesthoek": [20.2, 21.6], "Torens": [11.5, 6.35],
                                            "Gym (eigen ingang aan het erf)": [4.4, 5.0], "Lounge, spel en bieb": [7.0, 21.6]}})
