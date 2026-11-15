# ---------------------------------------------------------------- Ronde 9 (16 november 2026): Zilverstraat 56, Den Haag Kerketuinen
# Bedrijfsruimte uit 1993 (appartementsrecht 49/576 in een bedrijfsverzamelgebouw van 16 units, VvE niet actief), 17,4 x 27,8 m binnenwerks,
# begane grond 499 m² BVO en een betonnen entresol van 373 m² BVO op circa 3,4 m. Vrije hoogte 6,1 m alleen in de vide, 3,2 m onder de entresol (2,9 m tot de balken),
# 3,0 m boven de entresol. Lokaal stelsel: u 0 = noordwestwand (buren), u 28,5 = achtergevel met ramen op beide lagen (zuidoost, groenstrook met sloot),
# v 0 = gevel aan het parkeerhof (alleen u 0 tot 12 vrij, met overheaddeur en deur), v 18 = wand met het grote buurpand.
# Vide (uit de plattegrond van de makelaar): A = u 0-4,8 x v 0-8,6; B = u 4,8-11 x v 3,9-11,9; C = u 11-17,5 x v 8,9-14,5.
_ZV_GYMVIDE = [[0.3, 0.3], [4.8, 0.3], [4.8, 3.9], [8.3, 3.9], [8.3, 11.9], [4.8, 11.9], [4.8, 8.6], [0.3, 8.6]]
_ZV_VIDE = [[8.3, 3.9], [11.0, 3.9], [11.0, 8.9], [17.5, 8.9], [17.5, 14.5], [11.0, 14.5], [11.0, 11.9], [8.3, 11.9]]
ZILVER = dict(
    titel="Zilverstraat 56, Den Haag",
    sub="Hal uit 1993 van 17 x 28 m met een betonnen entresol rond een vide van 6,1 m, 6 eigen parkeerplaatsen, achtergevel met ramen op een groenstrook",
    hoogte=7.0, niveaus={"1": 3.4}, pui_h=4.0,
    concept="Twee lagen rond een hoge vide. De vide aan de hofkant wordt de gym: 6,1 m hoog, met de overheaddeur als glazen eigen ingang, zodat sporters om 6:00 binnen kunnen "
            "zonder door de club te lopen. Ernaast de clubdeur en een hoge entreehal met de lockers en de trap. Midden onder de tweede vide een zeshoekige bank en de pingpongtafel, "
            "daarachter de keuken, en tegen de achtergevel met ramen op de groenstrook het café met een zitnis langs het glas en een lange tafel. "
            "Boven ligt het werk: een werkzone met vier eilanden langs de ramen van de achtergevel, een tweede werkzone met raambar aan de hofkant, "
            "focuskamers, een vergaderkamer in het bestaande kantoortje en een stille bieb met belcellen. Boven de lage hoeken van de gym alleen techniek en berging. "
            "Sober: de staalconstructie en de betonnen entresol blijven zichtbaar, vloer strak schuren en coaten, wanden van oude ramen, nieuwe lichtkoepels boven de werkplekken.",
    geluid="Gym in de vide aan de hofkant, met een dichte wand van vloer tot dak langs de entreehal en dichte wanden langs de vide-randen op de verdieping. "
           "Boven de lage hoeken van de gym liggen alleen techniek en berging, nooit werkplekken. Tussen gym en werken de entreehal met lockers, de wastoren en 6 m afstand. "
           "40 mm rubber op een akoestische ondervloer, platforms onder de racks. In het verzamelgebouw zitten bedrijven, geen woningen; de woningen aan de overkant van de sloot "
           "liggen circa 30 m van de achtergevel, en de gym zit aan de andere kant van het pand.",
    pui=[[[0.4, 0.0], [4.4, 0.0]], [[28.5, 1.6], [28.5, 17.2]]],
    zones=[
        zone("Gym in de vide (eigen ingang)", "gym", R(0.3, 0.3, 8.3, 17.7),
             "De hoge vide aan de hofkant, 6,1 m vrij: drie racks op platforms langs de blinde wand, een vloer voor groepslessen, roeiers bij de glazen overheaddeur. "
             "In de lage hoek de douchetoren (D-vorm tegen de buurwand) en dagkluisjes. Eigen ingang door de overheaddeur, die een glazen pui met deur op toegangspas wordt.",
             ["Drie racks op zwevende platforms onder 6,1 m", "Groepslesvloer van 3,2 x 5 m", "Douchetoren met vier douches in de lage hoek",
              "Eigen ingang op toegangspas aan het parkeerhof, binnendeur naar de entreehal"],
             cam=dict(t=[4.0, 6.0], afstand=9, hoek=0),
             prompt="A functional gym in the 6 m high part of a 1990s industrial unit with a concrete mezzanine around it, blue-grey steel columns and beams, closed off by a solid wall: three black power racks on oak platforms, "
                    "a mat area, rowing machines near a large glass door that replaced the overhead door, anthracite rubber floor, one wall oxblood red, a D-shaped shower tower in board-marked plaster in the low corner."),
        zone("Entreehal met lockers", "entree", R(8.3, 0.3, 12.5, 12.0),
             "Door de clubdeur aan het parkeerhof kom je in een hal van 6,1 m hoog onder de vide: links de lockerwand van 6,8 m tegen de gymwand, rechts de stalen trap naar boven.",
             ["Lockerwand van 6,8 m (circa 108 lockers) met pothos erop", "Bestaande stalen trap naar de entresol", "Kapstokwand en ledenbord"],
             cam=dict(t=[10.4, 6.0], afstand=7, hoek=90),
             prompt="A double-height entrance hall in a 1990s industrial unit: a long wall of green lockers with trailing pothos on top, a black steel stair up to a concrete mezzanine with a glass balustrade, coat hooks, a kentia palm."),
        zone("Lounge en spel onder de vide", "café", R(12.5, 3.4, 21.3, 17.7),
             "Onder de tweede vide een zeshoekige bank rond een haard en de pingpongtafel, met een nieuwe lichtkoepel erboven. Ertegen de keuken van 5,6 m met een kookeiland. "
             "Tegen de blinde wand de vergaderkamer voor zes, de sta-kamer en drie belcellen.",
             ["Zeshoekige bank met twee open zijden rond een sfeerhaard", "Pingpongtafel, inklapbaar", "Keuken van 5,6 m uit tweedehands rvs, kookeiland met espressomachine"],
             cam=dict(t=[16.5, 11.0], afstand=8, hoek=0),
             prompt="A lounge under a 6 m high void in a 1990s industrial unit: a hexagonal olive velvet bench around a black fireplace, a ping pong table, an olive green kitchen from second-hand stainless steel worktables with a reclaimed wood island, "
                    "a concrete mezzanine with a glass balustrade above, a round roof light."),
        zone("Vergaderen beneden", "vergader", R(12.5, 0.3, 21.3, 3.4),
             "Langs de blinde wand onder de entresol een vergaderkamer voor zes en een sta-kamer, wanden van oude ramen.",
             ["Vergaderkamer voor zes met scherm en camera", "Sta-kamer met statafel en whiteboardwand"], cam=dict(t=[16.5, 2.0], afstand=7, hoek=90),
             prompt="Two small meeting rooms under a low concrete mezzanine, walls of reclaimed steel and timber windows, an oak table for six and a round high table with a whiteboard wall, slate blue acoustic panels."),
        zone("Café aan de achtergevel", "café", R(21.3, 0.3, 28.2, 17.7),
             "Achterin, achter de bestaande ramen op de groenstrook en de sloot: een zitnis van 6 m langs het glas, een lange tafel voor twaalf, tafeltjes en fauteuils. Olijf en strelitzia in het volle licht.",
             ["Zitnis van 6 m langs de ramen met drie tafeltjes", "Raambar van 6,6 m met elf krukken", "Lange tafel van 4,2 m voor twaalf", "Olijfboom en strelitzia aan het glas"],
             cam=dict(t=[24.5, 9.0], afstand=8, hoek=180),
             prompt="The café of a members club at the back of a 1990s industrial unit, under a low concrete mezzanine, a long row of existing windows looking out on a green strip with a ditch and trees: an olive velvet bench seat with small tables along the glass, "
                    "a long oak table for twelve, plum armchairs, an olive tree and a strelitzia, warm light."),
        zone("Wastoren", "sanitair", R(8.3, 12.0, 14.1, 17.7), "Achthoekige wastoren van 5,5 m doorsnee onder de entresol, tussen entreehal, lounge en gym.",
             ["Drie toiletcabines en een V-wastrog", "Toren 2,7 m hoog (onder de balken van de entresol)"], cam=dict(t=[11.3, 14.8], afstand=7, hoek=0),
             prompt="An octagonal concrete-look bathroom tower (eight flat faces, still reads as round), 2.7 m high under a concrete mezzanine, board-marked plaster, a V-shaped concrete wash trough with brass taps, ivy along the top rim."),
        dict(zone("Werkzone aan de achtergevel", "werken", R(21.6, 0.3, 28.2, 17.7),
                  "Boven het café, langs de ramen van de achtergevel: vier eilanden van vier zit-sta bureaus, schermen haaks op het glas, 1 tot 4 m van het raam.",
                  ["Vier eilanden van vier bureaus 140 x 70", "Bestaande ramen, onderin te openen", "Pothos boven de eilanden"], n=1, cam=dict(t=[24.5, 9.0], afstand=8, hoek=180),
                  prompt="A bright work floor on the upper level of a 1990s industrial unit, a long row of windows looking onto trees: four islands of compact sit-stand desks with oak tops, slate blue chairs, wood wool acoustic panels on the low ceiling, pothos hanging above."), tussenvloer=False),
        dict(zone("Werkzone aan de hofkant", "werken", [[8.3, 0.3], [17.5, 0.3], [17.5, 8.9], [11.0, 8.9], [11.0, 3.9], [8.3, 3.9]],
                  "Op de entresol aan de hofkant: een raambar langs de ramen aan het parkeerhof en twee eilanden onder nieuwe lichtkoepels, met een glazen balustrade naar de vide.",
                  ["Raambar van 3,2 m aan de hofkant", "Twee eilanden van vier bureaus", "Twee nieuwe lichtkoepels"], n=1, cam=dict(t=[13.0, 4.6], afstand=7, hoek=270),
                  prompt="A work mezzanine in a 1990s industrial unit: two islands of compact sit-stand desks under new round roof lights, a short oak window bar, a glass balustrade over a 6 m high void with a hexagonal bench below."), tussenvloer=False),
        dict(zone("Focus en vergaderen", "vergader", R(17.5, 0.3, 21.6, 14.5),
                  "Een strook tussen de twee werkzones: drie focuskamers, een belcel, de vergaderkamer voor zes in het bestaande kantoortje en de tweede trap.",
                  ["Drie focuskamers van oude ramen", "Belcel", "Vergaderkamer voor zes in het bestaande kantoor", "Tweede trap (vluchtweg)"], n=1, cam=dict(t=[19.5, 7.0], afstand=6, hoek=0),
                  prompt="Small focus rooms and a meeting room with walls of reclaimed windows on a concrete mezzanine, warm light, plants."), tussenvloer=False),
        dict(zone("Stille bieb", "bieb", [[8.3, 11.9], [11.0, 11.9], [11.0, 14.5], [21.6, 14.5], [21.6, 17.7], [8.3, 17.7]],
                  "Boven de wastoren, waar de trap uitkomt: boekenkasten langs de buurwand, leesstoelen en drie belcellen. Stilte.",
                  ["Boekenwand van 8 m", "Drie belcellen", "Leesstoelen"], n=1, cam=dict(t=[13.0, 16.0], afstand=6, hoek=270),
                  prompt="A quiet library corner on a concrete mezzanine: a long walnut bookshelf wall, two butter yellow reading chairs, round slate blue felt phone booths, a glass balustrade over a void."), tussenvloer=False),
        dict(zone("Techniek en berging boven de gym", "techniek", [[0.3, 8.6], [4.8, 8.6], [4.8, 11.9], [8.3, 11.9], [8.3, 17.7], [0.3, 17.7]],
                  "Boven de lage hoek van de gym: warmtepomp, ventilatie, batterij, berging en een toiletgroep voor de verdieping. Geen werkplekken boven de gym.", ["Warmtepomp en WTW", "Toiletgroep met twee toiletten en een toegankelijk toilet", "Berging en stoelen"], n=1), tussenvloer=False),
        dict(zone("Techniek boven de gymhoek", "techniek", R(4.8, 0.3, 8.3, 3.9), "Kleine berging boven de lage hoek van de gym.", [], n=1), tussenvloer=False),
    ],
    buiten=[dict(naam="Parkeerhof (6 eigen plaatsen)", poly=R(-2.0, -11.0, 12.0, -0.2), kleur="#c9c3b6"),
            dict(naam="Groenstrook en sloot", poly=R(28.7, -4.0, 36.0, 24.0), kleur="#9bb07a")],
    elementen=[
        # gym in de vide
        *rack([1.7, 2.2], 90), *rack([1.7, 4.8], 90), *rack([1.7, 7.4], 90), dict(t="kleed", c=[6.3, 7.8], w=3.2, d=5.0, a=0, kleur="#c7928a"), label([6.3, 7.8], "groepsles"),
        roeier([6.4, 1.0], 0), roeier([6.4, 2.0], 0), dict(t="box", soort="kettlebells", c=[2.6, 11.5], w=3.0, d=0.5, h=0.9, a=0, kleur=STAAL),
        *dtoren([5.6, 17.5], [0.6, 17.5], 0.6, "douche", H=2.7), *lockerwand([7.0, 12.3], 2.4, 0), dict(t="box", soort="bank", c=[7.9, 14.6], w=2.0, d=0.45, h=0.45, a=90, kleur=HOUT),
        deur([3.9, 0.0], 0, toegang=True, w=1.0), plant3([4.6, 3.4], "strelitzia nicolai"), boom3([0.9, 10.0], "kentia"), hangplant([6.0, 5.0], z=4.0),
        wand([[8.3, 0.3], [8.3, 3.9]], 3.2, gym=True), wand([[8.3, 3.9], [8.3, 10.8]], 7.0, gym=True), wand([[8.3, 11.9], [8.3, 17.7]], 3.2, gym=True), deur([8.3, 11.35], 90, toegang=True),
        # entreehal
        deur([9.0, 0.0], 0, w=1.0), *lockerwand([8.55, 7.2], 6.8, 90), dict(t="box", soort="trap", c=[10.6, 9.7], w=1.1, d=4.4, h=0.3, a=0, kleur=STAAL), label([10.6, 6.9], "trap"),
        dict(t="kleed", c=[10.6, 2.0], w=2.4, d=2.0, a=0, kleur="#d5bd96"), boom3([11.8, 4.6], "kentia"),
        # wastoren
        *achthoektoren([11.3, 14.8], 2.75, 0, "was", H=2.7),
        # vergaderen beneden en belcellen
        *vergaderkamer([15.3, 1.85], 4.6, 3.0, 0, 6), *stavergaderkamer([20.1, 1.6], 2.4, 2.6, 0, 5), dict(t="box", soort="trap", c=[18.3, 2.9], w=1.1, d=4.4, h=0.3, a=0, kleur=STAAL),
        pod2([13.6, 4.4]), pod2([15.1, 4.4]), pod2([16.6, 4.4]),
        # lounge, spel, keuken
        *pingpong([17.0, 7.2], 0), *veelhoekbank([16.2, 11.4], 1.8, 6, open=(1, 4)), *keuken([18.0, 17.35], 5.6, 0), *kookeiland([18.0, 15.3], 0),
        hangplant([14.8, 11.7], z=4.5), hangplant([13.0, 10.0], z=4.5), boom3([20.6, 13.2], "ficus elastica"), boom3([13.0, 6.2], "kentia"), plant3([21.0, 4.3], "aspidistra"), plant3([12.2, 0.9], "sansevieria"),
        # café aan de achtergevel
        *zitnis([28.0, 1.0], [28.0, 7.0]), *grote_tafel([24.5, 12.0], 4.2, 90), *tafeltje([24.0, 3.0], 0, 3), *tafeltje([24.0, 6.4], 0, 3),
        dict(t="box", soort="fauteuil", c=[22.3, 15.2], w=0.85, d=0.85, h=0.8, a=0, kleur="#5a2741"), dict(t="box", soort="fauteuil", c=[22.3, 16.6], w=0.85, d=0.85, h=0.8, a=0, kleur="#5a2741"),
        dict(t="box", soort="raambar", c=[27.95, 12.8], w=6.6, d=0.5, h=1.05, a=90, kleur=HOUT),
        boom3([27.4, 8.3], "olijf"), plant3([27.6, 17.1], "strelitzia nicolai"), boom3([21.9, 0.9], "kentia"), plant3([21.6, 8.0], "philodendron"), plant3([20.8, 10.2], "zz-plant"), plant3([12.0, 11.2], "aspidistra"), boom3([23.6, 17.0], "ficus elastica"), boom3([26.0, 17.0], "ficus elastica"), boom3([12.3, 2.4], "kentia", 1), hangplant([24.5, 12.0], z=2.6),
        # verdieping: werkzone achter
        *eiland2([25.6, 2.6], 0, 1), *eiland2([25.6, 6.6], 0, 1), *eiland2([25.6, 10.6], 0, 1), *eiland2([25.6, 14.6], 0, 1),
        *[hangplant([25.6, v], z=2.5, n=1) for v in (4.6, 8.6, 12.6)], plant3([22.2, 0.9], "zz-plant", 1), boom3([22.2, 17.0], "kentia", 1), plant3([27.7, 8.6], "strelitzia nicolai", 1), plant3([17.2, 0.8], "zz-plant", 1),
        # verdieping: strook focus en vergaderen
        *focuskamer([20.4, 1.6], 90, 1), *focuskamer([20.4, 4.0], 90, 1), *focuskamer([20.4, 6.4], 90, 1), pod2([19.0, 13.4], 1), *vergaderkamer([19.4, 10.4], 4.0, 3.6, 0, 6, 1), label([18.3, 2.9], "trap", 1),
        plant3([18.6, 7.2], "aspidistra", 1),
        # verdieping: werkzone hofkant
        dict(t="box", soort="raambar", c=[10.2, 0.55], w=3.2, d=0.5, h=1.05, a=0, kleur=HOUT, n=1), *eiland2([12.8, 4.6], 90, 1), *eiland2([16.0, 4.6], 90, 1),
        boom3([9.2, 3.0], "ficus elastica", 1), *[hangplant([u, 4.6], z=2.5, n=1) for u in (12.8, 16.0)],
        # verdieping: bieb
        *kasten(8.6, 16.6, 17.4, h=2.4, d=0.3, n=1), pod2([13.0, 15.4], 1), pod2([14.5, 15.4], 1), pod2([16.0, 15.4], 1),
        dict(t="box", soort="fauteuil", c=[9.2, 13.4], w=0.8, d=0.8, h=0.8, a=0, kleur="#47522a", n=1), dict(t="box", soort="fauteuil", c=[9.2, 14.9], w=0.8, d=0.8, h=0.8, a=0, kleur="#47522a", n=1),
        dict(t="box", soort="fauteuil", c=[18.6, 15.8], w=0.8, d=0.8, h=0.8, a=0, kleur="#47522a", n=1), plant3([20.6, 16.9], "kentia", 1),
        # verdieping: techniek boven de gym, dichte wanden langs de vide van de gym
        dict(t="box", soort="techniek", c=[2.6, 14.2], w=4.0, d=3.0, h=2.6, a=0, kleur="#8f8a80", n=1), label([2.6, 11.0], "berging", 1),
        dict(t="box", soort="techniek", c=[6.55, 2.1], w=3.0, d=3.0, h=2.6, a=0, kleur="#8f8a80", n=1),
        dict(t="box", soort="toiletgroep", c=[6.5, 15.4], w=3.2, d=3.6, h=2.6, a=0, kleur="#bdb7aa", n=1), label([6.5, 15.4], "toiletten", 1), deur([8.3, 16.4], 90, n=1),
        plant3([22.2, 8.6], "zz-plant", 1), plant3([22.2, 12.6], "zz-plant", 1), plant3([17.2, 17.1], "aspidistra", 1),
        wand([[4.8, 0.3], [4.8, 3.9], [8.3, 3.9]], 2.7, gym=True, n=1), wand([[0.3, 8.6], [4.8, 8.6], [4.8, 11.9], [8.3, 11.9]], 2.7, gym=True, n=1),
        wand([[8.3, 0.3], [8.3, 3.9]], 2.7, n=1), wand([[8.3, 11.9], [8.3, 17.7]], 2.7, n=1),
        # verdieping: glazen balustrade rond de vide (trapgat open)
        wand([[8.3, 3.9], [11.0, 3.9], [11.0, 8.9], [17.5, 8.9], [17.5, 14.5], [11.0, 14.5], [11.0, 11.9]], 1.1, glas=True, n=1), wand([[8.3, 11.9], [10.0, 11.9]], 1.1, glas=True, n=1),
        *[hangplant(p, z=1.1, n=1) for p in ([11.0, 4.6], [11.0, 6.4], [11.0, 8.2], [12.4, 8.9], [14.0, 8.9], [15.6, 8.9], [17.2, 8.9], [17.5, 10.6], [17.5, 12.4], [16.4, 14.5], [14.6, 14.5], [12.8, 14.5], [9.2, 11.9])],
        # buiten
        label([5.0, -5.0], "6 parkeerplaatsen"), dict(t="box", soort="fietsenrek", c=[10.5, -1.2], w=3.0, d=0.6, h=0.9, a=0, kleur=STAAL),
        dict(t="box", soort="plantenbak", c=[6.0, -0.5], w=2.4, d=0.5, h=0.6, a=0, kleur=WALNOOT), boom([0.9, -1.0], 0.8, 3.0), boom([7.9, -1.6], 0.8, 3.0), boom([30.5, 4.0], 1.2, 5.0), boom([30.5, 12.0], 1.2, 5.0), boom([31.0, 19.0], 1.1, 4.5),
    ],
    dak=dict(soort="pv", terras=None, groen=[], pv=[R(19.5, 0.8, 28.0, 17.2)],
             koepels=[[12.8, 4.6, 0.8], [16.0, 4.6, 0.8], [25.6, 4.6, 0.8], [25.6, 12.6, 0.8], [14.6, 11.7, 0.9], [4.0, 5.0, 0.8]],
             tekst="Plat dak, bitumen vernieuwd in december 2023: zonnepanelen op het achterste deel, zes nieuwe lichtkoepels boven de werkplekken, de vide en de gym. Geen dakterras: unit in een verzamelgebouw.",
             tekst_en="The flat bitumen roof of one unit in a long row of 1990s industrial units, solar panels on the rear half, six new round roof lights; neighbouring units stay plain grey, a parking court in front and a green strip with a ditch behind."),
    renders=dict(buiten=[]),
)
ONTWERPEN.update({"den-haag-zilverstraat-56": ZILVER})
LABELS.update({"den-haag-zilverstraat-56": {"Gym in de vide (eigen ingang)": [5.2, 10.6], "Entreehal met lockers": [10.6, 1.2], "Lounge en spel onder de vide": [16.4, 13.6],
                                           "Vergaderen beneden": [16.0, 3.7], "Café aan de achtergevel": [23.6, 8.4], "Wastoren": [11.3, 17.2],
                                           "Werkzone aan de achtergevel": [23.0, 8.6], "Werkzone aan de hofkant": [14.4, 7.8], "Focus en vergaderen": [19.4, 8.1],
                                           "Stille bieb": [11.5, 16.2], "Techniek en berging boven de gym": [2.6, 16.6], "Techniek boven de gymhoek": [6.55, 0.9]}})
VIDES.update({"den-haag-zilverstraat-56": [dict(naam="Vide boven de gym", poly=_ZV_GYMVIDE, n=1), dict(naam="Vide boven entree en lounge", poly=_ZV_VIDE, n=1)]})
