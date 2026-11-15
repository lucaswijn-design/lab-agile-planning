# ---------------------------------------------------------------- Ronde 9 (16 november 2026): Kampenringweg 7, Gouda Goudse Poort (vervangt Fokkerstraat 475 Schiedam)
# Middelste van drie bedrijfsunits uit 1991, 16,1 x 21,6 m, begane grond 342 m² BVO (werkplaats 19 x 16 m) en verdieping 295 m² (vier kantoren aan de voorkant,
# houten entresol van 10 x 16 m achterin). Vide van circa 6 x 9 m achter de overheaddeur. Lokaal stelsel: u 0 = voorgevel aan het parkeerhof (noordwest),
# u 21,6 = achtergevel richting de vaart (zuidoost), v 0 en v 16,1 = scheidingswanden met de buurunits. De overheaddeur zit op u 1,1, v 0,3 tot 6,3.
# Ontwerpkeuze: de entresol boven de gym (u 15,2 tot 21,3) gaat eruit, zodat de gym 6 m hoog wordt en licht krijgt van boven en van de achtergevel.
KAMPEN = dict(
    titel="Kampenringweg 7, Gouda",
    sub="Bedrijfsunit uit 1991 met kantoren aan de voorkant en een werkplaats van 19 x 16 m, 5 eigen parkeerplaatsen, achterkant op de vaart; 1,7 km van station Waddinxveen Triangel",
    hoogte=6.8, niveaus={"1": 3.2}, pui_h=4.5,
    concept="Van voor naar achter: druk, rustig, zweet. De overheaddeur wordt een glazen pui van 6 m breed en daarachter, in de hoge vide, het café met een zitnis langs het glas, "
            "de keuken langs de buurwand, een kookeiland en een lange tafel; onder de kantoren een zeshoekige bank. Door de bestaande voordeur kom je in de entree met lockers en de trap. "
            "Halverwege staan de twee achthoekige torens: de wastoren aan de cafékant, de douchetoren aan de gymkant. Achterin de gym, 6 m hoog doordat de houten entresol daar weggaat, "
            "met nieuwe ramen en een deur naar een terras aan de vaart. Boven: vier kantoren aan de voorkant worden werkkamers, een vergaderkamer en een sta-kamer, en op de entresol boven "
            "de torens een stille werkzone met lichtkoepels, met lockers en kasten als buffer naar de gym. Sober: bestaande kantoren en trap blijven, vloer strak, wanden van oude ramen.",
    geluid="Gym achterin, tegen de vaart; de buren zijn bedrijfsunits, geen woningen in het complex. Tussen gym en café de twee torens; op de verdieping een dichte wand tot het dak "
           "met lockers en bergkasten ervoor, en de bureaus beginnen pas 1,4 m daarvoor. Boven de gym geen vloer meer. 40 mm rubber op een akoestische ondervloer, platforms onder de racks.",
    pui=[[[1.1, 0.4], [1.1, 6.3]], [[21.6, 2.0], [21.6, 14.0]]],
    zones=[
        zone("Café in de vide", "café", R(1.2, 0.3, 10.5, 9.8),
             "Achter de nieuwe glazen pui op de plek van de overheaddeur, 6 m hoog: een raambar van 5,6 m langs het glas, de keuken langs de buurwand, een kookeiland met de espressomachine "
             "en een lange tafel voor tien. Onder de kantoren een zeshoekige bank rond een haard. Kentia en strelitzia aan het glas, pothos over de balustrade.",
             ["Glazen pui van 6 x 4,5 m op de plek van de overheaddeur", "Keuken van 5 m uit tweedehands rvs, kookeiland van 2,6 m", "Lange tafel van 3,5 m voor tien",
              "Raambar met negen krukken langs het glas, zeshoekige bank onder de kantoren", "Belcel bij de torens"],
             cam=dict(t=[5.5, 4.0], afstand=9, hoek=180),
             prompt="The café of a members club in a 6 m high void behind a large new glass front that replaced an overhead door, in a 1990s industrial unit with grey cladding: an oak window bar with stools along the glass, "
                    "an olive green kitchen from second-hand stainless steel worktables along the side wall, a reclaimed wood island with an espresso machine, a long oak table, a hexagonal bench around a black fireplace under a low office floor, "
                    "pothos trailing over a glass balustrade, a kentia palm."),
        zone("Entree met lockers", "entree", R(0.3, 9.8, 4.4, 15.8),
             "Door de bestaande voordeur: een lockerwand van 3,8 m, kapstokken en de trap naar de kantoren.", ["Lockerwand van 3,8 m", "Kapstokwand en ledenbord", "Bestaande trap naar boven"],
             cam=dict(t=[2.4, 12.8], afstand=6, hoek=0),
             prompt="A small entrance hall in a 1990s office front: a wall of green lockers with trailing pothos on top, coat hooks of reclaimed wood, a timber stair, a kentia palm."),
        zone("Stil hoekje onder de kantoren", "vergader", R(4.4, 9.8, 10.5, 15.8),
             "Onder de kantoren, naast de trap: een focuskamer, een sta-kamer en twee belcellen.", ["Focuskamer", "Sta-kamer met statafel", "Twee belcellen"],
             cam=dict(t=[7.5, 12.8], afstand=6, hoek=0),
             prompt="Small glass rooms made from reclaimed windows under a low office floor: a focus room and a stand-up meeting room with a round high table, two round felt phone booths, warm light."),
        zone("Wastoren en douchetoren", "sanitair", R(10.6, 0.3, 15.2, 9.9),
             "Twee achthoekige torens van 4,5 m doorsnee halverwege: de wastoren opent naar het café, de douchetoren naar de gym. Ertussen de gang naar de gymdeur met lockers op de torens.",
             ["Wastoren met drie toiletten en een V-wastrog", "Douchetoren met vier douches, alleen vanuit de gym", "Dagkluisjes op de douchetoren, aan de gang naar de gym"],
             cam=dict(t=[12.9, 7.6], afstand=7, hoek=90),
             prompt="Two octagonal concrete-look bathroom towers (flat faces, they still read as round objects) under a timber mezzanine in a 1990s industrial unit, board-marked plaster, a V-shaped concrete wash trough with brass taps, "
                    "green lockers built into an outer face, ivy along the top rim."),
        zone("Gym aan de vaart (afsluitbaar)", "gym", [[15.2, 0.3], [21.3, 0.3], [21.3, 15.8], [10.6, 15.8], [10.6, 9.9], [15.2, 9.9]],
             "Achterin, 6 m hoog waar de entresol weggaat, met nieuwe ramen en een deur naar een terras aan de vaart: twee racks op platforms, een groepslesvloer, roeiers met uitzicht op het water, "
             "de douchetoren in de hoek. Deur op toegangspas.",
             ["Twee racks op zwevende platforms", "Groepslesvloer van 4,6 x 3,2 m", "Roeiers aan het raam op de vaart", "Entresol boven de gym verwijderd, twee lichtkoepels"],
             cam=dict(t=[18.2, 7.0], afstand=8, hoek=0),
             prompt="A functional gym at the back of a 1990s industrial unit, 6 m high, with new windows looking out on a canal with reeds: two black power racks on oak platforms, a mat area, rowing machines facing the water, "
                    "anthracite rubber floor, one wall oxblood red, round roof lights, plants."),
        dict(zone("Werkkamers in de kantoren", "werken", R(0.3, 6.5, 10.5, 15.8),
                  "De vier bestaande kantoren aan de voorkant: twee werkkamers met een eiland van vier bureaus aan de ramen, een derde werkkamer en een vergaderkamer voor zes achter. Bestaand toilet en pantry blijven.",
                  ["Drie werkkamers met elk een eiland van vier", "Vergaderkamer voor zes", "Bestaand toilet en pantry"], n=1, cam=dict(t=[2.2, 11.0], afstand=6, hoek=180),
                  prompt="Small existing offices on the upper floor of a 1990s industrial unit turned into calm work rooms: islands of four compact sit-stand desks with oak tops at large windows, slate blue chairs, plants, a meeting room with a screen."), tussenvloer=False),
        dict(zone("Stille werkzone op de entresol", "werken", R(10.5, 0.3, 15.2, 15.8),
                  "Op de houten entresol boven de torens: drie eilanden van vier bureaus onder nieuwe lichtkoepels, een focuskamer, twee belcellen en langs de gymwand lockers en kasten als buffer.",
                  ["Drie eilanden van vier bureaus", "Lockerwand van 4 m en 10 m bergkasten tegen de gymwand", "Focuskamer en twee belcellen", "Glazen balustrade naar de vide"], n=1, cam=dict(t=[12.4, 8.0], afstand=7, hoek=180),
                  prompt="A quiet work floor on a timber mezzanine in a 1990s industrial unit: three islands of compact sit-stand desks under round roof lights, a long wall of green lockers and walnut cupboards with pothos on top, a small glass focus room, round felt phone booths, a glass balustrade over a café void."), tussenvloer=False),
    ],
    buiten=[dict(naam="Parkeren (5 eigen plaatsen)", poly=R(-6.0, 0.0, -0.2, 16.1), kleur="#c9c3b6"),
            dict(naam="Terras aan de vaart", poly=R(21.8, 1.0, 26.5, 15.0), kleur="#d5bd96"),
            dict(naam="Oever", poly=R(26.5, 0.0, 29.5, 16.1), kleur="#9bb07a")],
    elementen=[
        # café in de vide
        dict(t="box", soort="raambar", c=[1.55, 3.4], w=5.6, d=0.5, h=1.05, a=90, kleur=HOUT), *keuken([8.0, 0.65], 5.0, 0), *kookeiland([8.0, 2.6], 0), *grote_tafel([6.2, 5.0], 3.5, 0),
        *veelhoekbank([7.6, 8.3], 1.5, 6, open=(1, 4)), dict(t="box", soort="fauteuil", c=[3.2, 8.9], w=0.8, d=0.8, h=0.8, a=0, kleur="#5a2741"),
        dict(t="box", soort="fauteuil", c=[2.0, 8.9], w=0.8, d=0.8, h=0.8, a=0, kleur="#5a2741"),
        plant3([1.8, 0.5], "strelitzia nicolai"), plant3([10.1, 9.2], "monstera"), pod2([10.0, 7.2]), *[hangplant([u, 6.5], z=3.3) for u in (3.0, 5.5, 8.0)],
        # entree
        deur([0.3, 12.6], 90, w=1.2), *lockerwand([2.3, 15.55], 3.8, 0), dict(t="box", soort="trap", c=[5.15, 12.7], w=1.1, d=4.4, h=0.3, a=0, kleur=HOUT), label([5.15, 10.2], "trap"),
        dict(t="kleed", c=[2.2, 12.4], w=2.4, d=2.4, a=0, kleur="#d5bd96"), plant3([0.9, 10.4], "aspidistra"), boom3([3.4, 10.7], "kentia"),
        # stil hoekje
        *focuskamer([8.4, 11.2], 0), *stavergaderkamer([8.6, 14.2], 2.4, 2.6, 0, 5), pod2([6.6, 15.0]), pod2([6.6, 10.6]),
        # torens
        *achthoektoren([12.9, 3.2], 2.25, 180, "was", H=2.8), *achthoektoren([12.9, 12.6], 2.25, 0, "douche", lockers=(6,), H=2.8),
        # gym
        wand([[15.2, 0.3], [15.2, 7.2]], 6.6, gym=True), deur([15.2, 7.7], 90, toegang=True), wand([[15.2, 8.2], [15.2, 9.9]], 6.6, gym=True),
        wand([[15.2, 9.9], [10.6, 9.9], [10.6, 15.8]], 3.0, gym=True),
        *rack([16.8, 1.6], 0), *rack([19.6, 1.6], 0), dict(t="kleed", c=[18.2, 6.6], w=4.6, d=3.2, a=0, kleur="#c7928a"), label([18.2, 6.6], "groepsles"),
        roeier([20.6, 11.0], 90), roeier([19.6, 11.0], 90), dict(t="box", soort="kettlebells", c=[17.0, 15.5], w=2.0, d=0.5, h=0.9, a=0, kleur=STAAL),
        deur([21.6, 13.6], 90, w=1.2), plant3([20.9, 4.6], "strelitzia nicolai"), plant3([20.9, 8.9], "monstera"), plant3([16.0, 15.3], "sansevieria"), boom3([20.4, 15.0], "kentia"),
        # verdieping: werkkamers en vergaderen in de kantoren
        wand([[0.3, 10.9], [4.1, 10.9]], 2.7, n=1), wand([[4.1, 6.5], [4.1, 15.8]], 2.7, n=1), wand([[6.6, 6.5], [6.6, 13.2]], 2.7, n=1),
        *eiland2([2.2, 8.7], 0, 1), *eiland2([2.2, 13.3], 0, 1), *eiland2([8.5, 11.5], 0, 1), *vergaderkamer([8.5, 8.1], 3.6, 3.0, 0, 6, 1),
        dict(t="box", soort="toiletgroep", c=[8.5, 14.5], w=3.6, d=2.4, h=2.6, a=0, kleur="#bdb7aa", n=1), label([8.5, 14.5], "toilet en pantry", 1),
        plant3([0.8, 6.9], "monstera", 1), plant3([0.8, 15.3], "zz-plant", 1), plant3([5.3, 7.0], "dracaena", 1),
        # verdieping: entresol boven de torens
        wand([[1.2, 6.5], [10.5, 6.5], [10.5, 0.3]], 1.1, glas=True, n=1),
        *eiland2([12.4, 2.4], 0, 1), *eiland2([12.4, 6.0], 0, 1), *eiland2([12.4, 9.6], 0, 1), *focuskamer([12.0, 12.2], 0, 1), pod2([11.4, 14.6], 1), pod2([12.9, 14.6], 1),
        *lockerwand([14.95, 3.0], 4.0, 90, n=1), *kasten(5.2, 15.2, 14.95, a=90, d=0.5, h=2.4, n=1), wand([[15.2, 0.3], [15.2, 15.8]], 3.6, gym=True, n=1),
        *[hangplant([12.4, v], z=2.4, n=1) for v in (2.4, 6.0, 9.6)], plant3([6.0, 15.4], "zz-plant", 1), boom3([1.9, 7.3], "kentia"), plant3([14.1, 14.6], "aspidistra", 1),
        *[hangplant([10.5, v], z=1.1, n=1) for v in (1.5, 3.5, 5.5)],
        # buiten
        label([-3.0, 8.0], "5 parkeerplaatsen"), dict(t="box", soort="fietsenrek", c=[-1.0, 12.0], w=3.0, d=0.6, h=0.9, a=90, kleur=STAAL),
        *tafeltje([23.4, 4.0], 0, 4), *tafeltje([23.4, 8.0], 0, 4), dict(t="box", soort="bank", c=[25.8, 11.0], w=3.0, d=0.6, h=0.45, a=90, kleur=HOUT),
        boom([25.2, 2.0], 0.9, 3.4), boom([25.6, 14.6], 0.9, 3.4), boom([22.6, 1.4], 0.8, 3.0), boom([22.6, 14.8], 0.8, 3.0), boom([-5.2, 1.0], 0.8, 3.0), boom([-5.2, 15.0], 0.8, 3.0),
    ],
    dak=dict(soort="pv", terras=None, groen=[], pv=[R(0.8, 7.0, 10.0, 15.4), R(15.6, 0.8, 21.0, 15.4)],
             koepels=[[12.4, 4.2, 0.8], [12.4, 9.6, 0.8], [17.0, 5.0, 0.8], [19.8, 10.6, 0.8], [5.6, 3.4, 0.8]],
             tekst="Plat dak met de bestaande 18 zonnepanelen, aangevuld tot circa 20 kWp, en vijf lichtkoepels: boven de stille werkzone, de gym en de vide van het café. Geen dakterras: middelste unit van drie.",
             tekst_en="The flat roof of the middle unit in a row of three 1990s industrial units with grey cladding, solar panels and five round roof lights; a parking court in front, a canal with trees behind, neighbouring units plain grey."),
    renders=dict(buiten=[]),
)
ONTWERPEN.update({"gouda-kampenringweg-7": KAMPEN})
LABELS.update({"gouda-kampenringweg-7": {"Café in de vide": [4.4, 3.4], "Entree met lockers": [2.3, 14.4], "Stil hoekje onder de kantoren": [7.4, 9.4],
                                        "Wastoren en douchetoren": [12.9, 7.2], "Gym aan de vaart (afsluitbaar)": [18.2, 9.0],
                                        "Werkkamers in de kantoren": [5.3, 11.0], "Stille werkzone op de entresol": [12.4, 11.9]}})
VIDES.update({"gouda-kampenringweg-7": [dict(naam="Vide boven het café", poly=R(1.2, 0.3, 10.5, 6.5), n=1), dict(naam="Gym 6 m hoog (entresol weg)", poly=R(15.2, 0.3, 21.3, 15.8), n=1)]})
