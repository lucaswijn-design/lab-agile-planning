# ---------------------------------------------------------------- Ronde 9 (16 november 2026): Kommiezenlaan 27, Schiedam Spaanse Polder
# Unit 27: de westelijke beuk van 9,1 x 25,8 m van een bedrijfscomplex uit 1950 (zeven adressen, alle industriefunctie), 300 m na station Schiedam Centrum.
# Lokaal stelsel van de uitgesneden unit (zie dossier 'opmerking'): u 25,8 = straatgevel (noordnoordwest), u 0 = achtergevel (zuidzuidoost),
# v 0 = scheidingswand met de rest van het complex (oostnoordoost), v 9,1 = zijgevel aan het eigen erf (westzuidwest).
# Het perceel (circa 940 m2) loopt door tot v 20 en u -14: een open erf. Daar komt een nieuw gympaviljoen van 10 x 9 m (context 0 in het dossier).
# Vrije hoogte circa 4 m: geen tussenvloer. Gym los van het clubhuis, dus geen geluid naar de werkplekken.
KOMMIEZEN = dict(
    titel="Kommiezenlaan 27, Schiedam",
    sub="Smalle bedrijfsbeuk uit 1950 van 9 x 26 m met een eigen erf van 700 m², op 300 m van station Schiedam Centrum; een tuinkamer erachter en een gympaviljoen op het erf",
    hoogte=4.6, pui_h=3.0,
    extra=[dict(ctx=0, naam="Gympaviljoen", h=4.5), dict(ctx=1, naam="Tuinkamer", h=4.2)],
    concept="De beuk zelf is te klein voor een hele club, het erf is groot. Daarom drie delen: de bestaande beuk met café en werken, een nieuwe tuinkamer van 10 x 9 m "
            "in het verlengde ervan aan de zonkant, en los op het erf een gympaviljoen. Je komt binnen vanaf de straat, direct in het café met keuken, kookeiland en een "
            "zitnis langs de voorgevel. Daarachter de werkzone langs een nieuwe glazen zijgevel op het erf, met aan de dichte kant een rij kamers: vergaderen voor zes, een sta-kamer, "
            "een focuskamer en belcellen. Achterin de wastoren als D-toren tegen de blinde wand en de lockers, en door een brede opening de tuinkamer: een stille werkkamer met een "
            "raambar op het zuiden, een eiland van zes bureaus, een focuskamer en drie belcellen. De gym staat 10 m verderop in een eigen paviljoen met de douchetoren en een deur op toegangspas. "
            "Sober: bestaande vloer strak schuren en coaten, oude stalen ramen in de nieuwe gevels, paviljoen en tuinkamer op een hergebruikt stalen hallenframe.",
    geluid="De gym staat in een eigen paviljoen, 10 m van de tuinkamer en 20 m van de werkzone: geen gedeelde wand of vloer. Paviljoen met een dichte geïsoleerde schil, "
           "40 mm rubber op een akoestische ondervloer en platforms onder de racks. In het clubhuis de volgorde straat, café, werken, kamers, en achterin de stille tuinkamer. "
           "Buren zijn bedrijfsunits, geen woningen in het complex.",
    pui=[[[25.8, 0.4], [25.8, 8.7]], [[4.2, 9.1], [18.0, 9.1]], [[-10.0, 0.3], [-10.0, 8.8]], [[-9.8, 9.1], [-3.0, 9.1]], [[-12.8, 19.2], [-9.6, 19.2]]],
    zones=[
        zone("Café aan de straat", "café", R(18.3, 0.2, 25.6, 8.9),
             "Achter de voorgevel aan de Kommiezenlaan: een keuken van 4,4 m langs de dichte wand, een kookeiland met de espressomachine, een grote tafel voor acht langs het glas "
             "en een zitnis met drie tafeltjes pal achter de nieuwe glazen voorgevel. Kentia en een rubberboom bij de deur, pothos boven de tafels.",
             ["Keuken van 4,4 m uit tweedehands rvs werktafels en oude houten fronten", "Kookeiland van 2,6 m met de espressomachine, ook als bar",
              "Grote tafel van 2,8 m voor acht: lunch en samen werken", "Zitnis van 5 m langs de voorgevel met drie tafeltjes en twee fauteuils"],
             cam=dict(t=[21.8, 4.6], afstand=8, hoek=0),
             prompt="The café of a small members club at the street end of a narrow 1950s industrial bay, 9 m wide and 4 m high: an olive green kitchen made from second-hand stainless steel worktables and old timber fronts along the blind wall, "
                    "a reclaimed wood island with an espresso machine, an oak communal table for eight next to a new glass side facade, an olive velvet bench seat with small tables along the glass street front, a kentia palm and a strelitzia."),
        zone("Werkzone langs het erf", "werken", R(4.0, 3.4, 18.3, 8.9),
             "Vier eilanden van vier zit-sta bureaus haaks op een nieuwe glazen zijgevel van 14 m, die uitkijkt op het terras en de middagzon vangt. Elk bureau 1,5 tot 3 m van het glas, scherm haaks op het raam.",
             ["Vier eilanden van vier bureaus 140 x 70, haaks op het glas", "Nieuwe zijgevel van hergebruikte stalen ramen, onderin te openen", "Looppad van 1,4 m langs de kamers",
              "Pothos boven elk eiland, zz-planten ertussen"],
             cam=dict(t=[11.0, 6.2], afstand=8, hoek=270),
             prompt="A narrow coworking zone in a 1950s industrial bay 4 m high: four islands of four compact sit-stand desks with oak tops placed at right angles to a long new glass side wall made of reclaimed steel windows, "
                    "a timber terrace with planters outside, slate blue chairs, wood wool acoustic panels on the ceiling, pothos hanging above each island, a smooth sealed concrete floor."),
        zone("Kamers aan de dichte wand", "vergader", R(5.6, 0.2, 18.3, 3.4),
             "Langs de blinde wand met de buren een rij kamers van oude ramen: een vergaderkamer voor zes, een sta-kamer, een focuskamer en twee belcellen. Stil aan de dichte kant, licht via het glas van de werkzone.",
             ["Vergaderkamer voor zes met scherm en camera", "Sta-kamer met statafel en whiteboardwand", "Focuskamer voor één of twee", "Belcellen in leisteenblauw vilt"],
             cam=dict(t=[11.5, 1.8], afstand=7, hoek=90),
             prompt="A row of small rooms against a blind brick wall inside a narrow industrial bay: a meeting room for six and a stand-up meeting room with a round high table, both with walls of reclaimed steel and timber windows, "
                    "a small glass focus room and round slate blue felt phone booths, warm light, plants."),
        zone("Wastoren en lockers", "sanitair", R(0.2, 0.2, 4.0, 8.9),
             "Achterin een D-vormige wastoren met de rug tegen de blinde wand (drie toiletten en een wastrog) en de lockerwand, met een brede opening naar de tuinkamer.",
             ["D-toren met drie toiletcabines en een betonnen wastrog", "Lockerwand van 3,6 m met pothos erop", "Opening van 3 m naar de tuinkamer"],
             cam=dict(t=[2.2, 4.5], afstand=6, hoek=0),
             prompt="A D-shaped bathroom tower with its flat back against a blind wall, board-marked plaster, three toilet cabins and a concrete wash trough with brass taps, ivy along the top rim, "
                    "a wall of green lockers with trailing pothos on top, a wide opening to a bright garden room."),
        zone("Tuinkamer: stille werkkamer", "bieb", R(-9.8, 0.2, 0.0, 8.9),
             "Een nieuwe aanbouw van 10 x 9 m aan de zonkant, met glas op het zuiden en westen: een raambar van 8 m met dertien krukken, een eiland van zes bureaus, een bank langs de dichte wand, "
             "een focuskamer en drie belcellen. Stilte: geen bellen buiten de cellen. Strelitzia en ficus in het volle licht.",
             ["Raambar van 8 m op het zuiden, met een pergola met druif buiten tegen de zon", "Eiland van zes zit-sta bureaus", "Bank van 4,6 m langs de dichte wand",
              "Focuskamer en drie belcellen", "Tuindeur naar het erf"],
             cam=dict(t=[-5.0, 4.5], afstand=7, hoek=180),
             prompt="A quiet garden room added behind an old industrial building, a simple reclaimed steel frame with large old steel windows on two sides looking onto a green garden: a long oak window bar with stools, "
                    "an island of six sit-stand desks, an olive bench along the blind wall, a small glass focus room, round felt phone booths, a tall strelitzia and a monstera in full light, a vine pergola outside."),
        zone("Gympaviljoen (afsluitbaar)", "gym", R(-13.5, 19.2, -4.7, 27.2),
             "Een nieuw paviljoen van 8,8 x 8 m en 4,5 m hoog achter op het erf, 10 m van de tuinkamer: twee racks op platforms, een vloer voor groepslessen, roeiers en de douchetoren. "
             "Glas naar de tuin, eigen deur op toegangspas.",
             ["Twee racks op zwevende platforms, 40 mm rubber op akoestische ondervloer", "Douchetoren (D-vorm) met vier douches tegen de achterwand",
              "Groepslesvloer van 2,6 x 4 m", "Eigen deur op toegangspas, open van 6:00 tot 23:00"],
             cam=dict(t=[-9.0, 23.2], afstand=8, hoek=270),
             prompt="A small new gym pavilion in a garden behind an old industrial building, built from a reclaimed steel portal frame with dark corrugated cladding: two black power racks on oak platforms, a mat area, rowing machines, "
                    "anthracite rubber floor, one wall oxblood red, a long low window to the garden, a D-shaped shower tower in board-marked plaster."),
    ],
    buiten=[dict(naam="Terras langs de zijgevel", poly=R(9.5, 9.3, 19.0, 13.6), kleur="#d5bd96"),
            dict(naam="Tuin", poly=[[-13.8, 0.0], [-10.2, 0.0], [-10.2, 9.3], [9.5, 9.3], [9.5, 13.6], [-2.6, 13.6], [-2.6, 19.0], [-13.8, 19.0]], kleur="#9bb07a"),
            dict(naam="Parkeren en fietsen", poly=R(19.2, 9.3, 26.0, 20.0), kleur="#c9c3b6"),
            dict(naam="Straat", poly=R(26.2, -12.0, 34.0, 26.0), kleur="#9a958c")],
    elementen=[
        # café
        *keuken([20.8, 0.55], 4.4, 0), *kookeiland([20.8, 2.55], 0), *grote_tafel([21.0, 6.6], 2.8, 0),
        *zitnis([25.55, 0.3], [25.55, 5.3]), dict(t="box", soort="fauteuil", c=[23.2, 4.4], w=0.8, d=0.8, h=0.8, a=200, kleur="#5a2741"),
        dict(t="box", soort="fauteuil", c=[23.4, 3.3], w=0.8, d=0.8, h=0.8, a=160, kleur="#5a2741"),
        deur([25.8, 7.6], 90, w=1.4), dict(t="kleed", c=[24.6, 7.5], w=1.6, d=2.2, a=0, kleur="#d5bd96"),
        boom3([18.9, 8.3], "kentia"), boom3([24.7, 6.2], "ficus elastica"), hangplant([20.8, 4.2]), hangplant([22.8, 6.6]), hangplant([24.6, 2.8]),
        # werkzone
        *eiland2([5.8, 6.3], 90), *eiland2([9.0, 6.3], 90), *eiland2([12.2, 6.3], 90), *eiland2([15.4, 6.3], 90),
        *[hangplant([u, 6.3]) for u in (5.8, 9.0, 12.2, 15.4)], plant3([7.4, 8.6], "zz-plant"), plant3([10.6, 8.6], "monstera"), plant3([13.8, 8.6], "zz-plant"), plant3([17.2, 8.5], "strelitzia nicolai"),
        # kamers langs de dichte wand
        *vergaderkamer([8.1, 1.7], 4.6, 3.0, 0, 6), *stavergaderkamer([11.7, 1.5], 2.4, 2.6, 0, 5), *focuskamer([14.2, 1.15], 0),
        pod2([16.1, 1.0]), pod2([17.6, 1.0]), plant3([16.85, 2.6], "aspidistra"),
        # achterin: wastoren en lockers, opening naar de tuinkamer
        *dtoren([0.2, 0.2], [5.4, 0.2], 0.8, "was"), *lockerwand([2.2, 8.85], 3.6, 0),
        label([1.2, 5.3], "opening 3 m"), plant3([3.6, 4.4], "sansevieria"),
        # tuinkamer
        dict(t="box", soort="raambar", c=[-9.5, 4.55], w=8.0, d=0.5, h=1.05, a=90, kleur=HOUT), *eiland2([-4.6, 4.55], 90, k=6),
        *zitnis([-8.2, 0.25], [-3.6, 0.25], tafels=False), *focuskamer([-1.3, 7.9], 0), pod2([-0.9, 0.9]), pod2([-0.9, 2.45]), pod2([-2.4, 0.9]),
        dict(t="box", soort="fauteuil", c=[-8.4, 8.3], w=0.8, d=0.8, h=0.8, a=0, kleur="#47522a"), dict(t="box", soort="fauteuil", c=[-6.9, 8.3], w=0.8, d=0.8, h=0.8, a=0, kleur="#47522a"),
        plant3([-3.6, 8.5], "strelitzia nicolai"), plant3([-8.6, 6.9], "monstera"), *[hangplant([-4.6, v]) for v in (3.1, 6.0)], hangplant([-9.5, 4.5]),
        deur([-5.4, 9.1], 0, w=1.2), wand([[0.0, 0.2], [0.0, 3.8]], 4.2, bestaand=True), wand([[0.0, 6.8], [0.0, 8.9]], 4.2, bestaand=True),
        # gympaviljoen op het erf
        *dtoren([-13.3, 25.6], [-13.3, 21.0], 0.5, "douche"),
        *rack([-6.1, 25.6], 0), *rack([-6.1, 22.9], 0), roeier([-11.6, 19.75], 0), roeier([-8.6, 19.75], 0),
        dict(t="kleed", c=[-8.9, 23.4], w=2.6, d=4.0, a=0, kleur="#c7928a"), label([-8.9, 23.4], "groepsles"),
        dict(t="box", soort="kettlebells", c=[-11.9, 26.85], w=2.0, d=0.5, h=0.9, a=0, kleur=STAAL), *lockerwand([-8.8, 26.95], 2.2, 0),
        deur([-6.0, 19.2], 0, toegang=True), plant3([-5.2, 19.8], "sansevieria"), plant3([-10.4, 26.6], "kentia"),
        # buiten: terras, tuin, parkeren
        *tafeltje([12.0, 11.6], 0, 4), *tafeltje([15.4, 11.6], 0, 4), dict(t="box", soort="plantenbak", c=[14.2, 13.4], w=9.0, d=0.5, h=0.6, a=0, kleur=WALNOOT),
        dict(t="box", soort="pergola", c=[-10.9, 4.55], w=8.6, d=1.4, h=2.6, a=90, kleur="#9a8f7a"),
        boom([6.0, 12.0], 1.0, 3.2), boom([-12.4, 2.0], 1.0, 3.0), boom([-12.4, 13.0], 1.1, 3.4), boom([-3.0, 16.5], 0.9, 3.0), boom([1.5, 16.0], 0.9, 3.0), boom([-1.5, 24.0], 0.9, 2.8),
        dict(t="box", soort="bank", c=[-7.0, 15.0], w=2.4, d=0.6, h=0.45, a=0, kleur=HOUT), *tafeltje([-7.0, 12.4], 0, 3),
        label([23.0, 17.0], "3 parkeerplaatsen + fietsen"), label([-8.0, 17.6], "tuin (onttegeld)"),
    ],
    dak=dict(soort="pv", terras=None, groen=[R(-9.8, 0.2, -0.2, 8.9), R(-13.3, 19.4, -4.9, 27.0)], pv=[R(0.6, 0.6, 25.2, 8.5)],
             koepels=[[11.0, 6.3, 0.8], [15.4, 6.3, 0.8], [21.0, 4.5, 0.8], [-4.6, 4.55, 0.9]],
             tekst="Nieuw plat dak van de beuk met zonnepanelen en lichtkoepels boven werkzone en café. Tuinkamer en gympaviljoen krijgen een groen sedumdak. Geen dakterras: unit in een complex.",
             tekst_en="The flat roof of the westernmost bay of a long 1950s row of industrial units, new roofing with solar panels and round roof lights; behind it a low new garden room with a green sedum roof and, further back in a garden, "
                      "a small gym pavilion with a sedum roof. Neighbouring bays stay plain grey, the street in front."),
    renders=dict(buiten=[]),
)
ONTWERPEN.update({"schiedam-kommiezenlaan-27": KOMMIEZEN})
LABELS.update({"schiedam-kommiezenlaan-27": {"Café aan de straat": [22.4, 7.9], "Werkzone langs het erf": [10.6, 8.35], "Kamers aan de dichte wand": [11.5, 3.95],
                                            "Wastoren en lockers": [2.2, 6.6], "Tuinkamer: stille werkkamer": [-5.0, 7.6], "Gympaviljoen (afsluitbaar)": [-9.0, 21.0]}})
