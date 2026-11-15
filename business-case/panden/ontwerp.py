"""
Uitgewerkt ontwerp per locatie (november 2026): indeling, ronde elementen, meubels,
inrichting per ruimte, daken en camerastandpunten. Alles in het lokale assenstelsel
(u, v in meters) van geo.frame(footprint), net als layout.py.

Gebruik: python3 ontwerp.py  -> schrijft ontwerp/<slug>.json (input voor maquette en tekening)
"""
from __future__ import annotations

import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# Kleuren uit de natuur (zie infographics/Kleur.dc.html)
PALET = {
    "pistache": dict(naam="Pistache", vloer="#d9ccb0", hoofd="#6f7d3a", tweede="#b3bb6c", accent="#5a2741"),
    "avocado": dict(naam="Avocado", vloer="#e5d48c", hoofd="#47522a", tweede="#6b4428", accent="#e5d48c"),
    "rots": dict(naam="Rotskust", vloer="#e3e6e2", hoofd="#44606f", tweede="#6e4f38", accent="#1f3441"),
    "granaat": dict(naam="Granaatappel", vloer="#8d8380", hoofd="#6c1d22", tweede="#a8332e", accent="#e2b6a2"),
    "vijg": dict(naam="Vijg", vloer="#b8633f", hoofd="#4b2339", tweede="#b5525e", accent="#b8633f"),
    "kokos": dict(naam="Kokos", vloer="#d5bd96", hoofd="#5a3a22", tweede="#f2ece1", accent="#4d6a3a"),
    "beton": dict(naam="Beton en mos", vloer="#c9c3b6", hoofd="#a7a296", tweede="#5f7a3a", accent="#8f8a80"),
    "verhuur": dict(naam="Verhuur", vloer="#d0ccc4", hoofd="#9a958c", tweede="#9a958c", accent="#9a958c"),
}
ZONEPALET = {"café": "pistache", "bieb": "avocado", "werken": "rots", "gym": "granaat", "studio": "vijg",
             "entree": "kokos", "sanitair": "beton", "techniek": "beton", "verhuur": "verhuur", "vergader": "rots"}
HOUT, WALNOOT, STAAL, WIT, GROEN = "#b08a5e", "#6b4428", "#2f3032", "#f4f1ea", "#5f7a3a"


def R(u0, v0, u1, v1):
    return [[u0, v0], [u1, v0], [u1, v1], [u0, v1]]


# ---------------------------------------------------------------- bouwstenen
def eiland(c, a, n=0):
    """4 zit-sta bureaus rug aan rug met dubbele schermen, licht gedraaid."""
    out = []
    ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
    for du, dv, rot in ((-0.8, -0.4, 0), (0.8, -0.4, 0), (-0.8, 0.4, 180), (0.8, 0.4, 180)):
        x, y = c[0] + du * ca - dv * sa, c[1] + du * sa + dv * ca
        out.append(dict(t="bureau", c=[round(x, 2), round(y, 2)], w=1.6, d=0.8, a=a + rot, n=n))
    return out


def zitkuil(c, r, open_deg, kleur_bank, kleur_kleed, n=0):
    """Ronde bank rond een sfeerhaard, open naar één kant."""
    return [
        dict(t="kleed", c=c, r=r + 0.2, kleur=kleur_kleed, n=n),
        dict(t="boog", soort="bank", c=c, r=r, a0=open_deg + 40, a1=open_deg + 320, d=0.85, h=0.75, kleur=kleur_bank, n=n),
        dict(t="cil", soort="haard", c=c, r=0.45, h=0.5, kleur="#3a3b3d", n=n),
        dict(t="cil", soort="poef", c=[c[0] + 0.9 * math.cos(math.radians(open_deg + 60)), c[1] + 0.9 * math.sin(math.radians(open_deg + 60))], r=0.3, h=0.42, kleur="#5a2741", n=n),
        dict(t="cil", soort="poef", c=[c[0] + 0.9 * math.cos(math.radians(open_deg - 60)), c[1] + 0.9 * math.sin(math.radians(open_deg - 60))], r=0.3, h=0.42, kleur="#5a2741", n=n),
    ]


def boekentoren(c, r, open_deg, n=0):
    """Ronde leeskamer: wand van 2,6 m met boekenkast rondom, opening van 0,9 m, twee fauteuils en een leeslamp."""
    gat = math.degrees(0.9 / r)
    return [
        dict(t="ring", soort="boekentoren", c=c, r=r, open=open_deg, gat=gat, h=2.6, kleur="#47522a", n=n),
        dict(t="boog", soort="kast", c=c, r=r - 0.12, a0=open_deg + gat / 2 + 6, a1=open_deg + 360 - gat / 2 - 6, d=0.35, h=2.3, kleur=WALNOOT, n=n),
        dict(t="kleed", c=c, r=r - 0.6, kleur="#e5d48c", n=n),
        dict(t="box", soort="fauteuil", c=[c[0] + 0.55 * math.cos(math.radians(open_deg + 150)), c[1] + 0.55 * math.sin(math.radians(open_deg + 150))], w=0.8, d=0.8, h=0.8, a=open_deg + 150, kleur="#47522a", n=n),
        dict(t="box", soort="fauteuil", c=[c[0] + 0.55 * math.cos(math.radians(open_deg - 150)), c[1] + 0.55 * math.sin(math.radians(open_deg - 150))], w=0.8, d=0.8, h=0.8, a=open_deg - 150, kleur="#47522a", n=n),
        dict(t="cil", soort="lamp", c=[c[0] + 0.7 * math.cos(math.radians(open_deg + 180)), c[1] + 0.7 * math.sin(math.radians(open_deg + 180))], r=0.12, h=1.5, kleur="#e5d48c", n=n),
    ]


def toren(c, r, open_deg, soort, n=0):
    """Sanitairtoren met V-wand (zie sanitairtorens.py). soort: 'was' of 'douche'."""
    return [dict(t="toren", c=c, r=r, open=open_deg, soort=soort, h=3.0, n=n)]


def pod(c, n=0):
    return dict(t="cil", soort="belcel", c=c, r=0.75, h=2.3, kleur="#44606f", n=n)


def plant(c, r=0.45, h=1.2, n=0):
    return dict(t="plant", c=c, r=r, h=h, n=n)


def boom(c, r=1.1, h=3.2, n=0):
    return dict(t="boom", c=c, r=r, h=h, n=n)


def rack(c, a, n=0):
    return [dict(t="box", soort="rack", c=c, w=1.4, d=1.4, h=2.3, a=a, kleur=STAAL, n=n),
            dict(t="box", soort="platform", c=c, w=2.4, d=2.4, h=0.05, a=a, kleur="#6b4428", n=n)]


def roeier(c, a, n=0):
    return dict(t="box", soort="roeier", c=c, w=2.4, d=0.6, h=0.5, a=a, kleur=STAAL, n=n)


def kasten(u0, u1, v, a=0, d=0.4, h=2.4, n=0, kleur=WALNOOT):
    """Boekenwand als rij kasten van 1 m tussen u0 en u1 op lijn v (a=0) of tussen v0 en v1 op lijn u (a=90)."""
    out = []
    k = int(abs(u1 - u0))
    for i in range(k):
        m = u0 + (i + 0.5) * (u1 - u0) / k
        out.append(dict(t="box", soort="kast", c=[m, v] if a == 0 else [v, m], w=abs(u1 - u0) / k - 0.02, d=d, h=h, a=a, kleur=kleur, n=n))
    return out


def tafeltje(c, n=0, stoelen=2):
    out = [dict(t="cil", soort="ronde tafel", c=c, r=0.4, h=0.74, kleur=HOUT, n=n)]
    for i in range(stoelen):
        a = math.radians(90 + i * 360 / stoelen)
        out.append(dict(t="cil", soort="stoel", c=[c[0] + 0.65 * math.cos(a), c[1] + 0.65 * math.sin(a)], r=0.22, h=0.45, kleur="#5a3a22", n=n))
    return out


def zone(naam, type_, poly, beschrijving, details, foto=None, prompt="", n=0, cam=None, palet=None):
    return dict(naam=naam, type=type_, poly=poly, palet=palet or ZONEPALET[type_], beschrijving=beschrijving,
                details=details, foto=foto, prompt=prompt, n=n, cam=cam)


BASIS_PROMPT = ("Keep the existing architecture exactly: walls, windows, columns, ceiling height and camera angle. "
                "Interior style: Berlin warehouse meets Taghazout calm, second hand and organized chaos, raw concrete, old brick and black steel stay visible, "
                "lots of plants and small trees, warm daylight. Low-budget industrial finish: a smooth sealed concrete floor, sleek compact sit-stand desks with oak tops, "
                "glass partitions made from reclaimed old steel and timber windows, reclaimed wood, scaffolding boards and old doors reused with care, wood wool acoustic panels, "
                "nothing glossy or high-end. Colours from nature: {kleuren}. Photorealistic, natural light, no people in focus, no text.")


# ---------------------------------------------------------------- Utrecht
UTRECHT = dict(
    titel="Van Heutszstraat 4, Utrecht",
    sub="Verscholen buurthuis uit 1959 in Lombok, 630 m² op één laag rond een verwilderde binnentuin",
    hoogte=3.5,
    concept="Je komt binnen via de poort, de steeg en de binnentuin. De punt van het gebouw die de tuin in steekt wordt de entree. "
            "Links het boekencafé met een ronde zitkuil rond de haard, daarachter een ronde boekentoren als stille bieb. "
            "Rechts de werkzone met losse eilanden, en in het scharnier tussen werken en sporten de wastoren. De gym zit in de "
            "achtervleugel met de douchetoren ernaast. Het dak wordt groen met zonnepanelen en ronde lichtkoepels boven de torens.",
    pui=[[[6, 8.2], [13.4, 8.2]], [[26, 12], [26, 19]], [[0, 3], [0, 9]], [[14, 8.2], [13.6, 8.2]]],
    zones=[
        zone("Entree in de punt", "entree", [[13.6, 10.2], [18.4, 15], [23, 10], [26, 10], [26, 8.2], [13.6, 8.2]],
             "De driehoekige punt die de binnentuin in steekt wordt de voordeur. Je loopt over het tuinpad naar binnen en ziet meteen groen, licht en de espressobar in de verte.",
             ["Rond jute kleed van 3,5 m, een lange leren bank van de kringloop en een kapstokwand van steigerhout",
              "Ledenbord met wie er is, streepjeslijst voor de koffie, kluisjes in oud schoolmeubel",
              "Kokospalet: bast, zand, kokoswit en palmgroen; rotan lamp boven de deur",
              "Twee grote olijfbomen in potten markeren de deur in de punt"], foto=8,
             prompt="Turn this old community-centre entrance into the welcoming front door of a members club. Replace the blue door with a large black steel and glass door, fresh lime-washed brick in warm sand tones, two olive trees in big clay pots, a rattan pendant, a small brass plaque instead of the old sign."),
        zone("Boekencafé aan de tuin", "café", R(0.3, 0.3, 13.6, 8.2),
             "Het hart van de club. Een ronde zitkuil met een vrijstaande sfeerhaard, een gebogen espressobar in de hoek en een boekenwand van 9 meter met 1.500 boeken. De glazen pui kijkt uit op de binnentuin.",
             ["Ronde bank van 4,6 m doorsnee in olijfgroen fluweel, open naar de tuin, sfeerhaard in het midden",
              "Gebogen espressobar van hergebruikt hout met travertin blad, 3-groeps machine, streepjeslijst aan de wand",
              "Boekenwand van 9 m in walnoot, met een rolladder; boekenruggen als 10% accent",
              "Pruimkleurige poefs en fauteuils, kleine ronde tafels voor twee, werktafel voor acht bij de pui",
              "Kalkverf in pistache op de achterwand, betonvloer geschuurd, plafond open met zichtbare installaties in zwart"],
             foto=12, cam=dict(t=[6.5, 4.2], afstand=11, hoek=210),
             prompt="Transform this empty room into the heart of a members club: a round sunken-looking conversation sofa in olive green velvet around a freestanding black fireplace, a curved espresso bar of reclaimed wood with a travertine top and a three-group espresso machine, a 9 metre walnut bookcase full of colourful books with a rolling ladder, plum velvet armchairs and poufs, small round wooden tables, big potted trees, the glass facade opening onto a wild green courtyard garden."),
        zone("Stille bieb in de boekentoren", "bieb", R(0.3, 8.2, 5.4, 12.4),
             "Een ronde leeskamer van 3,7 m doorsnee, rondom boekenkasten tot 2,3 m, een smalle opening naar het café. Binnen alleen twee fauteuils, een lamp en stilte.",
             ["Ronde wand in diep olijf kalkverf, binnen walnoten kasten rondom",
              "Twee fauteuils in olijf, botergele plaid, een staande leeslamp",
              "Stilteregel: geen laptops, geen bellen", "Bovenin een ronde lichtkoepel"],
             cam=dict(t=[2.8, 10.2], afstand=7, hoek=240),
             prompt="A small round reading room, 3.7 m in diameter, walls lined with walnut bookshelves all around, deep olive lime-wash, two olive velvet armchairs, butter-yellow throw, a brass reading lamp, a round skylight above, very calm."),
        zone("Werkzone met eilanden", "werken", R(13.6, 0.3, 26, 8.2),
             "Twintig zit-sta bureaus met twee schermen in vijf losse eilandjes die elk een beetje anders staan, plus twee ronde belcellen. Geen rijen, wel rust.",
             ["Vijf eilanden van vier bureaus, licht gedraaid, eiken bladen op zwarte onderstellen",
              "Refurbished Steelcase stoelen, schermarmen, bureaulamp per plek",
              "Twee ronde belcellen van 1,5 m in leisteenblauw vilt",
              "Akoestische vilten baffles in rotskust-blauw onder het plafond, planten tussen de eilanden",
              "Cognac leren stoelen bij de belcellen"],
             cam=dict(t=[19.5, 4.2], afstand=11, hoek=200),
             prompt="An open coworking area in a 1960s community building: five islands of four sit-stand desks with oak tops and black frames, each island slightly rotated, dual monitors, refurbished office chairs, two round phone booths in slate-blue felt, slate-blue acoustic baffles, plants between the desks, calm and focused."),
        zone("Studio", "studio", R(26.2, 0.3, 36, 4.6),
             "Ruimte voor yoga, mobiliteit, workshops en kleine events, met een gebogen gordijn dat de ruimte zacht afsluit.",
             ["Gebogen verduisterend gordijn in vijgenpaars, ook voor de akoestiek",
              "Terracotta vloerkleed, matten en blokken in een open kast", "Spiegel aan één wand, warm dimbaar licht"],
             cam=dict(t=[31, 2.4], afstand=8, hoek=190),
             prompt="A small studio for yoga and workshops with a curved floor-to-ceiling curtain in deep fig purple, terracotta rug, wooden floor, mats in an open shelf, warm dimmable light."),
        zone("Wastoren", "sanitair", R(26.2, 4.6, 36, 10),
             "De wastoren van 5,5 m doorsnee staat in het scharnier tussen werken, café en gym. Aan de open kant de wastrog langs de V, erachter drie toiletcabines.",
             ["Ronde wand 3 m hoog in kalkstuc met plankstructuur", "V-vormige wastrog in beton met drie messing kranen",
              "Plantenbak op de rand met klimop en scindapsus", "Lichtkoepel erboven zodat daglicht in de toren valt"],
             cam=dict(t=[29.2, 7.3], afstand=8, hoek=210),
             prompt="An octagonal concrete-look bathroom tower (eight flat faces, still reads as a round object), 5.5 m diameter and 3 m high, board-marked plaster walls, a V-shaped concrete wash trough with brass taps on the open side, toilet cabins hidden behind the V wall, ivy and pothos hanging over the top rim, daylight falling in from a round skylight above."),
        zone("Gym in de achtervleugel", "gym", [[26, 10], [36, 10], [36, 25.4], [34.5, 25.4], [27.2, 22.5], [27.2, 20.4], [26, 20.4]],
             "Een functionele gym zonder machines: vijf racks met platform, roeiers, halters en kettlebells, met een glazen wand naar de binnentuin. Douchetoren direct ernaast.",
             ["Vijf ATX racks op eiken platforms, rubber vloer in antraciet",
              "Eén wand in ossenbloed kalkverf, verder wit en zwart staal", "Drie roeiers bij het glas met uitzicht op de tuin",
              "Douchetoren van 4,5 m doorsnee met drie douches achter de V", "Blosroze handdoeken, grote palm in de hoek"],
             foto=10, cam=dict(t=[31, 17], afstand=12, hoek=230),
             prompt="Turn this wing into a functional strength gym: five black power racks on oak lifting platforms, anthracite rubber floor, one wall in oxblood red lime paint, rowing machines facing the garden, kettlebells on a steel rack, large green plants, glass doors opening to a wild garden."),
        zone("Terras en binnentuin", "entree", R(5.6, 8.6, 13.4, 15), "",
             [], n=-1),
    ],
    buiten=[
        dict(naam="Terras", poly=R(5.6, 8.6, 13.4, 14.5), kleur="#b08a5e"),
        dict(naam="Binnentuin", poly=[[5.6, 14.5], [13.6, 14.5], [18.4, 17.5], [26, 20.4], [26, 22], [1, 22], [1, 12.6], [5.6, 12.6]], kleur="#9bb07a"),
    ],
    elementen=[
        # entree
        dict(t="kleed", c=[18.6, 10.8], r=1.75, kleur="#d5bd96"), boom([17.2, 13.4], 0.7, 2.4), boom([19.8, 13.4], 0.7, 2.4),
        dict(t="box", soort="bank", c=[22.6, 9.3], w=2.2, d=0.8, h=0.75, a=0, kleur="#5a3a22"),
        # café
        *zitkuil([5.6, 4.2], 2.3, 90, "#6f7d3a", "#d9ccb0"),
        dict(t="boog", soort="bar", c=[13.4, 4.2], r=2.3, a0=110, a1=250, d=0.7, h=1.1, kleur=HOUT),
        *kasten(0.6, 9.6, 0.55), *tafeltje([1.6, 6.6]), *tafeltje([1.6, 2.4]), *tafeltje([9.6, 2.4]),
        dict(t="box", soort="werktafel", c=[10.2, 7.2], w=3.6, d=1.0, h=0.75, a=0, kleur=HOUT),
        boom([9.2, 5.0], 0.9, 2.8), plant([12.8, 7.6]), plant([0.8, 7.8]),
        dict(t="box", soort="fauteuil", c=[8.6, 1.6], w=0.85, d=0.85, h=0.8, a=20, kleur="#5a2741"),
        # bieb
        *boekentoren([2.8, 10.3], 1.85, 270),
        # werken
        *eiland([15.8, 2.0], -8), *eiland([19.8, 1.9], 5), *eiland([23.8, 2.4], -6), *eiland([16.6, 5.7], 10), *eiland([21.4, 5.6], -4),
        pod([24.6, 7.4]), pod([14.8, 7.6]), plant([13.9, 4.6], 0.5, 1.6), plant([25.4, 0.9]), plant([13.9, 0.9]),
        # studio
        dict(t="boog", soort="gordijn", c=[31.1, 6.4], r=6.0, a0=243, a1=297, d=0.08, h=3.2, kleur="#4b2339"),
        dict(t="kleed", c=[31.1, 2.2], w=6, d=2.8, a=0, kleur="#b8633f"),
        # sanitair
        *toren([29.2, 7.3], 2.75, 180, "was"), *toren([33.4, 12.7], 2.25, 180, "douche"),
        # gym
        *rack([34.8, 16.8], 90), *rack([34.8, 19.6], 90), *rack([34.8, 22.4], 90), *rack([29.8, 21.0], 0), *rack([32.0, 23.6], 22),
        dict(t="box", soort="techniek", c=[34.7, 7.3], w=2.0, d=3.4, h=2.6, a=0, kleur="#8f8a80"),
        dict(t="kleed", c=[29.8, 16.4], w=4.2, d=3.2, a=0, kleur="#c7928a"),
        roeier([27.3, 12.0], 90), roeier([27.3, 14.2], 90), roeier([27.3, 16.4], 90),
        dict(t="box", soort="halterrek", c=[30.5, 10.6], w=2.4, d=0.5, h=0.9, a=0, kleur=STAAL), boom([28.2, 21.2], 0.8, 2.6),
        # terras en tuin
        *tafeltje([7.2, 10.4], stoelen=3), *tafeltje([10.4, 10.2], stoelen=3), *tafeltje([8.8, 12.8], stoelen=3),
        dict(t="boog", soort="bank", c=[19.0, 19.0], r=2.2, a0=200, a1=340, d=0.5, h=0.45, kleur=HOUT),
        dict(t="ring", soort="pergola", c=[19.0, 19.0], r=2.6, open=90, gat=0, h=2.6, kleur="#2f3032", dun=True),
        boom([3, 19]), boom([10, 20]), boom([24, 19]), boom([14, 18]), boom([3.4, 14.4], 0.9, 2.6),
    ],
    dak=dict(soort="groen", terras=None,
             groen=[R(0.3, 0.3, 13.6, 12.4), R(26, 10, 36, 25)], pv=[R(13.8, 0.6, 25.8, 8.0), R(26.4, 0.6, 35.6, 4.4)],
             koepels=[[29.2, 7.3, 0.9], [33.4, 12.7, 0.8], [2.8, 10.3, 0.7], [5.6, 4.2, 0.9]],
             tekst_en="Green sedum roof on both wings, solar panels on the middle part, four round skylights above the two bathroom towers, the round reading room and the fireplace seating. No roof terrace.",
             tekst="Licht dak uit 1959 en woningen rondom: geen dakterras (constructie en inkijk). Wel een groen dak met sedum op de vleugels, zonnepanelen op de middenstrook en ronde lichtkoepels boven de twee torens, de boekentoren en de zitkuil."),
    renders=dict(buiten=[(9, "Binnentuin en terras", "Turn this overgrown courtyard into a lush members-club garden: a wooden terrace with round tables along the glass facade, wild planting, existing trees kept, a round black steel pergola with a curved wooden bench, gravel paths, warm evening light. Repaint the blue panels in deep olive green and the frames in black."),
                         (6, "Poort en steeg", "Make this gate and alley the subtle entrance of a members club: black steel gate with a small brass sign, climbing plants on both walls, warm wall lights, clean gravel path leading into a green courtyard. Keep the surrounding houses unchanged."),
                         (5, "Luchtfoto met nieuw dak", "Keep this aerial photo exactly, only change the flat roof of the long low building in the middle of the block: sedum green roof on the wings, solar panels on the middle part, four round skylights, and a lush green courtyard garden with a round pergola.")]),
)

# ---------------------------------------------------------------- Rietveldenweg
RIETVELDEN = dict(
    titel="Rietveldenweg 13, Den Bosch",
    sub="Showroom uit 1966 met bedrijfswoning, 890 m² op één laag aan de rand van de Rietvelden",
    hoogte=4.6,
    concept="De showroomramen aan de straat worden de etalage van de club: daarachter het boekencafé met een halfronde boekenwand "
            "om de zitkuil en de bestaande natuurstenen balie als espressobar. De werkzone ligt achter het café, rustig van de straat af. "
            "Midden in de hal staat de wastoren, de gym neemt de lichte oostkant met de douchetoren in de hoek. Achterin de "
            "boekentoren en de studio. Het platte deel boven het café kan een dakterras worden.",
    pui=[[[7, 1], [7, 12.5]]],
    zones=[
        zone("Boekencafé achter de showroomramen", "café", R(7.3, 0.3, 22, 12.6),
             "Achter 11 meter showroomglas ligt het café, zichtbaar vanaf de straat. Een halfronde boekenwand omarmt de zitkuil met haard. De bestaande natuurstenen balie wordt de espressobar.",
             ["Halfronde vrijstaande boekenwand van 7,6 m doorsnee in walnoot, open naar de ramen",
              "Ronde bank in olijfgroen fluweel rond een sfeerhaard",
              "Bestaande natuurstenen balie hergebruikt als espressobar, travertin blad erop",
              "Leesfauteuils en planten in de vensterbank langs het glas; de houten vloer en zwarte plafonds blijven",
              "Grote ficus en olijfboom in potten, pistache kalkverf op de achterwand"],
             foto=5, cam=dict(t=[14, 6], afstand=13, hoek=200),
             prompt="Transform this former showroom into a members-club book café: keep the oak floor, black ceiling, grey columns and the natural stone wall. Add a semicircular freestanding walnut bookcase full of books wrapping a round olive-green velvet sofa around a black freestanding fireplace, plum velvet armchairs along the big shop windows, large potted fig and olive trees, small round wooden tables."),
        zone("Espressobar", "café", R(16.5, 8.5, 22, 12.6),
             "De balie in natuursteen blijft staan en krijgt een travertin blad, een 3-groeps machine en de streepjeslijst.",
             ["Natuurstenen balie bestaand, travertin blad nieuw", "Messing hanglampen, kopjes op open plank",
              "Barkrukken in cognac leer", "Streepjeslijst op een krijtbord"], foto=7, cam=dict(t=[19, 10.5], afstand=7, hoek=300),
             prompt="Keep this natural stone counter and turn it into a warm espresso bar: travertine top, a polished three-group espresso machine, brass pendants, open shelves with cups, cognac leather bar stools, a chalkboard tally list, plants, the long black-ceiling hall behind it softly lit."),
        zone("Werkzone", "werken", R(7.3, 12.8, 22, 25.6),
             "Twintig bureaus in vijf eilanden, drie ronde belcellen en een lange werktafel, rustig achter het café en van de straat af.",
             ["Vijf eilanden van vier zit-sta bureaus, licht gedraaid", "Drie ronde belcellen in leisteenblauw vilt langs de achterwand",
              "Werktafel van 6 m voor twaalf, eiken blad", "Akoestische panelen in blauwgrijs op de zwarte wanden, planten tussen de eilanden"],
             foto=8, cam=dict(t=[14.5, 19], afstand=12, hoek=210),
             prompt="Turn this long hall with black walls and ceiling into a calm coworking space: islands of four sit-stand desks with oak tops, each slightly rotated, dual monitors, three round slate-blue felt phone booths, a 6 m oak communal table, slate-blue acoustic panels, many plants, keep the wooden floor."),
        zone("Gym", "gym", [[22, 0.3], [42.5, 0.3], [41.6, 3.3], [39.4, 12.8], [22, 12.8]],
             "De grootste open ruimte: zes racks, een sledebaan en roeiers. De douchetoren staat in de hoek.",
             ["Zes racks op eiken platforms langs de lange wand", "Sledebaan van kunstgras van 12 m",
              "Rubber vloer in antraciet over de houten vloer", "Ossenbloed accentwand, douchetoren van 4,5 m"],
             foto=9, cam=dict(t=[30, 6], afstand=14, hoek=200),
             prompt="Turn this large black-ceiling hall into a functional strength gym: six black power racks on oak platforms along the wall, a 12 m artificial turf sled track, anthracite rubber floor, rowing machines, one wall in oxblood red, big plants, round concrete-look shower tower with plants on its rim in the corner."),
        zone("Wastoren", "sanitair", R(22, 13, 29.2, 19), "De wastoren midden in de hal, open naar de werkzone.",
             ["Wastrog langs de V, drie toiletten erachter", "Plantenrand bovenop, lichtstraat erboven"],
             cam=dict(t=[25.6, 16], afstand=8, hoek=200),
             prompt="An octagonal concrete-look bathroom tower (eight flat faces, still reads as a round object), 5.5 m diameter and 3 m high, standing free in a black-ceiling hall, board-marked plaster, a V-shaped concrete wash trough with brass taps, ivy hanging over the top rim."),
        zone("Studio", "studio", R(22, 19, 29.2, 25.8), "Studio voor yoga en events achter een gebogen gordijn.",
             ["Gordijn in vijgenpaars", "Terracotta vloerkleed, matten"], foto=12, cam=dict(t=[25.6, 22.4], afstand=8, hoek=200),
             prompt="A yoga and event studio behind a curved floor-to-ceiling fig-purple curtain, terracotta rug on the wooden floor, warm light, mats on open shelves."),
        zone("Bieb", "bieb", [[29.2, 13], [38.9, 13], [36.7, 22], [35.4, 26.8], [29.2, 26.8]],
             "Ronde boekentoren en een lange leestafel in diep olijf.",
             ["Boekentoren van 4,2 m doorsnee", "Leestafel voor tien met groene bankierslampen"], cam=dict(t=[32, 19], afstand=9, hoek=200),
             prompt="A quiet library corner: a round reading room lined with walnut bookshelves, deep olive walls, a long oak reading table with green banker's lamps."),
        zone("Techniek en opslag", "techniek", R(36.5, 0.6, 41, 5.5), "Warmtepomp, batterij, meterkast en opslag.", []),
        zone("Bedrijfswoning (verhuur)", "verhuur", R(0.1, 13.6, 7, 26), "Blijft woning, wordt verhuurd.", []),
    ],
    buiten=[dict(naam="Voorterras", poly=R(0.8, 0.8, 6.8, 12.8), kleur="#b08a5e"),
            dict(naam="Straat", poly=R(-9, -4, -1.5, 30), kleur="#9a9890")],
    elementen=[
        dict(t="boog", soort="kast", c=[14.4, 6.2], r=3.8, a0=-80, a1=80, d=0.4, h=2.2, kleur=WALNOOT),
        *zitkuil([14.4, 6.2], 2.4, 180, "#6f7d3a", "#d9ccb0"),
        dict(t="box", soort="bar", c=[19.4, 10.6], w=3.4, d=0.9, h=1.1, a=0, kleur="#8f8a80"),
        *[dict(t="box", soort="fauteuil", c=[8.2, v], w=0.85, d=0.85, h=0.8, a=0, kleur="#5a2741") for v in (2.4, 5.0, 9.6)],
        plant([7.9, 3.7]), plant([7.9, 7.4]), plant([7.9, 11.6]), boom([10.6, 11.0], 1.0, 3.0), boom([20.8, 1.6], 1.0, 3.0),
        *tafeltje([19.8, 4.4]), *tafeltje([19.8, 7.2]), *tafeltje([10.4, 1.6]),
        *[dict(t="cil", soort="kolom", c=[8.7, v], r=0.2, h=4.6, kleur="#9a9890") for v in (3.0, 7.0, 11.0)],
        # werken
        *eiland([10.6, 15.2], -8), *eiland([15.0, 15.0], 6), *eiland([19.2, 15.8], -5), *eiland([11.8, 19.4], 9), *eiland([16.8, 19.6], -6),
        pod([8.6, 24.4]), pod([10.6, 24.6]), pod([12.6, 24.4]),
        dict(t="box", soort="werktafel", c=[18.4, 23.6], w=6.0, d=1.2, h=0.75, a=0, kleur=HOUT), plant([21.3, 20.4], 0.5, 1.6), plant([8.0, 13.6]),
        # gym
        *rack([24.2, 1.6], 0), *rack([27.2, 1.6], 0), *rack([30.2, 1.6], 0), *rack([33.2, 1.6], 0), *rack([36.2, 1.6], 0), *rack([23.6, 9.4], 90),
        dict(t="box", soort="sledebaan", c=[30.0, 5.2], w=12, d=1.6, h=0.02, a=0, kleur="#5f7a3a"),
        roeier([27.0, 8.6], 0), roeier([27.0, 10.4], 0), roeier([27.0, 12.0], 0), boom([38.4, 7.0], 0.9, 2.8),
        *toren([34.2, 10.0], 2.25, 180, "douche"),
        # sanitair, studio, bieb
        *toren([25.6, 16.0], 2.75, 180, "was"),
        dict(t="boog", soort="gordijn", c=[25.6, 26.6], r=6.4, a0=232, a1=308, d=0.08, h=3.4, kleur="#4b2339"),
        dict(t="kleed", c=[25.6, 23.4], w=6, d=4, a=0, kleur="#b8633f"),
        *boekentoren([32.2, 16.6], 2.1, 180), dict(t="box", soort="leestafel", c=[32.0, 22.6], w=1.1, d=4.6, h=0.75, a=0, kleur=HOUT),
        # voorterras
        *tafeltje([3.0, 3.0], stoelen=3), *tafeltje([3.0, 6.6], stoelen=3), *tafeltje([3.0, 10.2], stoelen=3),
        *[dict(t="box", soort="plantenbak", c=[1.0, v], w=0.5, d=2.4, h=0.6, a=0, kleur="#5a3a22") for v in (2.4, 6.6, 10.8)],
        boom([-0.4, 1.5]), boom([-0.4, 12.0]),
    ],
    dak=dict(soort="terras", terras=R(8.0, 1.0, 20.0, 11.6), trap_buiten=[6.0, 12.4],
             groen=[R(22.5, 13.5, 35, 26)], pv=[R(22.5, 0.8, 38, 12.4)], koepels=[[25.6, 16.0, 0.9], [34.2, 10.0, 0.8], [32.2, 16.6, 0.8]],
             tekst_en="A roof terrace of about 125 m2 above the book café: wooden decking, a black steel pergola with climbing plants, planters with grasses and small trees, a black steel railing and an outdoor steel stair from the forecourt. Solar panels on the gym roof, sedum at the back, round skylights.",
             tekst="Het platte dak boven het café (circa 125 m²) kan een dakterras worden met pergola, plantenbakken en een buitentrap vanaf het voorterrein. "
                   "Eerst een constructeur: een showroomdak uit 1966 is meestal licht. Zonnepanelen op het dak boven de gym, sedum achter."),
    renders=dict(buiten=[(1, "Gevel aan de straat", "Turn this grey 1960s showroom with house into the street front of a members club: keep the building shape, paint the brick in warm sand lime-wash, black steel window frames, the showroom windows showing a warm book café with plants inside, a wooden terrace with planters and small trees on the forecourt, a subtle brass sign, a roof terrace with pergola and greenery visible on the flat roof part."),
                         (2, "Voorterrein en dak", "Keep the building, turn the paved forecourt into a planted terrace with round tables and three trees in planters, add a black steel outdoor stair to a roof terrace with pergola and plants on the flat roof above the showroom.")]),
)

# ---------------------------------------------------------------- Eendenkooi
EENDENKOOI = dict(
    titel="De Eendenkooi 1A, Den Bosch",
    sub="Sportgebouw uit 1977 aan het water, gymzaal, studio en kleedkamers zijn er al",
    hoogte=7.8, niveaus={"1": 3.9},
    concept="Hier hoeft de gym niet gebouwd te worden: de sportzaal is er. Bij de entree komt het boekencafé met een gebogen espressobar "
            "(de huidige balie), een ronde zitkuil en een boekentoren. De dansstudio blijft studio. De kleedkamers krijgen microcement "
            "en een V-vormige wastrog in het midden. Boven komt de werkzone met uitzicht over het groen. Op het dak boven het café kan een dakterras.",
    pui=[[[19, 0], [29, 0]]],
    zones=[
        zone("Gym in de sportzaal", "gym", R(0.3, 0.3, 17.5, 18.1),
             "De bestaande sportzaal van bijna 8 m hoog. Racks langs de achterwand, een sledebaan van 15 m en een vrije vloer voor groepslessen.",
             ["Zes racks met platforms langs de achterwand", "Sledebaan van kunstgras van 15 m langs de gevel",
              "Roeiers en skiërgs langs de kopse wand", "Ossenbloed accentwand, bokszakken blijven hangen",
              "Grote bomen in potten in de hoeken voor groen in de hoogte"], foto=4, cam=dict(t=[9, 9], afstand=16, hoek=210),
             prompt="Transform this dark sports hall into a beautiful functional gym: six black power racks on oak platforms along the back wall, a 15 m artificial turf sled track, rowing machines, keep the punching bags, anthracite rubber floor, one wall in oxblood red, the rest warm white, large trees in big pots, warm industrial pendant lights, daylight through the high windows."),
        zone("Boekencafé bij de entree", "café", R(17.7, 0.3, 30.4, 10),
             "Bij binnenkomst de gebogen espressobar (de huidige balie in een nieuw jasje), een ronde zitkuil met haard voor de ramen en een boekentoren.",
             ["Bestaande balie bekleed met hergebruikt hout en travertin blad", "Ronde bank in olijfgroen fluweel rond een sfeerhaard",
              "Boekenwand langs de wand naar de kleedkamers", "Rode Snap-wanden worden pistache en kokoswit",
              "Leesplekken in de vensterbank met uitzicht op het groen"], foto=5, cam=dict(t=[24, 5], afstand=12, hoek=200),
             prompt="Transform this white gym reception into a warm book café: wrap the counter in reclaimed wood with a travertine top and a three-group espresso machine, replace red walls with pistachio green lime-wash, a round olive velvet sofa around a black freestanding fireplace in front of the windows, a walnut bookcase wall full of books, plum armchairs, many plants and small trees."),
        zone("Entree en ontvangst", "entree", R(22, 0.3, 26, 2.6), "Waar nu de Snap-balie staat komt de ontvangst met ledenbord en streepjeslijst.",
             ["Jute kleed, rotan lamp, olijfbomen bij de deur"], foto=3, cam=dict(t=[24, 2], afstand=7, hoek=200),
             prompt="Turn this red fitness reception into a calm members-club entrance: sand and palm-green tones instead of red, a curved reclaimed wood counter with a travertine top, rattan pendant, olive trees in clay pots, a small chalkboard with today's events."),
        zone("Studio (bestaande dansstudio)", "studio", R(17.7, 10, 30.4, 16.9), "De dansstudio blijft, met vijgenpaarse gordijnen en terracotta accenten.",
             ["Houten vloer blijft", "Gordijnen in vijgpaars rondom, dimbaar warm licht"], foto=10, cam=dict(t=[24, 13.4], afstand=9, hoek=200),
             prompt="Keep this wooden-floor dance studio and make it warmer: fig-purple curtains, terracotta rug corner with cushions, plants on the window sills, warm dimmable light."),
        zone("Kleedkamers met V-wastrog", "sanitair", R(30.6, 0.3, 37.2, 14.6),
             "De kleedkamers en douches blijven waar ze zijn, maar de tegels gaan eruit: microcement, eiken banken en in het midden een V-vormige wastrog.",
             ["Microcement op wand en vloer in plaats van tegels", "V-vormige wastrog in beton met messing kranen",
              "Eiken banken en haken, planten bij het raam"], foto=11, cam=dict(t=[33.9, 7.4], afstand=8, hoek=200),
             prompt="Renovate this tiled changing room: replace all tiles with warm grey microcement and board-marked plaster, a V-shaped concrete wash trough with brass taps in the middle, oak benches and black hooks, ivy and ferns, soft daylight."),
        zone("Verdieping: werkzone", "werken", R(17.7, 0.3, 37.2, 14.6),
             "De hele verdieping wordt werkzone met uitzicht over het water en het groen: vijf eilanden, belcellen en een vergaderkamer achter glas.",
             ["Vijf eilanden van vier bureaus", "Drie ronde belcellen", "Vergaderkamer achter staal en glas",
              "Raambar van 10 m langs de gevel met uitzicht"], foto=8, n=1, cam=dict(t=[27, 7], afstand=13, hoek=200),
             prompt="Turn this white space with columns and windows into a calm coworking floor: islands of four sit-stand desks with oak tops slightly rotated, dual monitors, round slate-blue felt phone booths, a meeting room behind black steel and glass, a long window bar with stools facing the green view, plants everywhere."),
    ],
    buiten=[dict(naam="Parkeerplaats en groen", poly=R(-2, -12, 40, -1), kleur="#a7a49a")],
    elementen=[
        # gym
        *rack([2.2, 16.6], 0), *rack([5.0, 16.6], 0), *rack([7.8, 16.6], 0), *rack([10.6, 16.6], 0), *rack([13.4, 16.6], 0), *rack([16.0, 16.6], 0),
        dict(t="box", soort="sledebaan", c=[8.6, 1.6], w=15, d=1.6, h=0.02, a=0, kleur="#5f7a3a"),
        roeier([1.4, 6.0], 90), roeier([1.4, 8.6], 90), roeier([1.4, 11.2], 90),
        *[dict(t="cil", soort="bokszak", c=[x, 9.0], r=0.2, h=1.2, z=1.0, kleur="#3a3b3d") for x in (10, 12, 14)],
        boom([1.6, 1.8], 1.2, 4.2), boom([16.0, 12.6], 1.2, 4.2),
        dict(t="kleed", c=[9.0, 9.4], w=9, d=6, a=0, kleur="#c7928a"),
        dict(t="box", soort="halterrek", c=[9.0, 13.9], w=4.0, d=0.6, h=0.9, a=0, kleur=STAAL),
        dict(t="box", soort="kettlebells", c=[4.0, 13.9], w=2.0, d=0.5, h=0.9, a=0, kleur=STAAL),
        dict(t="box", soort="trap", c=[18.8, 13.6], w=1.2, d=3.4, h=0.3, a=0, kleur="#cfc8ba"),
        dict(t="box", soort="trap", c=[18.8, 13.6], w=1.2, d=3.4, h=0.3, a=0, kleur="#cfc8ba", n=1),
        # café
        dict(t="boog", soort="bar", c=[19.4, 3.4], r=1.9, a0=-90, a1=90, d=0.7, h=1.1, kleur=HOUT),
        *zitkuil([26.4, 5.4], 2.3, 270, "#6f7d3a", "#d9ccb0"),
        *kasten(0.8, 9.4, 30.1, a=90),
        *boekentoren([20.4, 7.9], 1.8, 0),
        *tafeltje([23.4, 8.8]), *tafeltje([29.0, 1.4]), boom([22.6, 1.4], 0.8, 2.6), boom([29.4, 9.0], 0.8, 2.6),
        # studio
        dict(t="kleed", c=[24.0, 13.4], w=5, d=3, a=0, kleur="#b8633f"),
        dict(t="boog", soort="gordijn", c=[24.0, 16.2], r=5.6, a0=240, a1=300, d=0.08, h=3.2, kleur="#4b2339"),
        # kleedkamers
        dict(t="v", c=[33.9, 7.4], arm=2.2, hoek=40, open=180, h=1.2),
        *[dict(t="box", soort="bank", c=[36.6, v], w=0.4, d=3.0, h=0.45, a=0, kleur=HOUT) for v in (3, 11.5)],
        *[dict(t="box", soort="douchewand", c=[31.6 + i * 1.4, 0.9], w=0.08, d=1.2, h=2.1, a=0, kleur="#c9c3b6") for i in range(4)],
        *[dict(t="box", soort="douchewand", c=[31.6 + i * 1.4, 13.9], w=0.08, d=1.2, h=2.1, a=0, kleur="#c9c3b6") for i in range(4)],
        # verdieping werkzone
        *eiland([20.6, 3.4], -8, 1), *eiland([24.8, 3.2], 6, 1), *eiland([29.0, 3.8], -5, 1), *eiland([21.8, 8.0], 9, 1), *eiland([26.4, 8.2], -6, 1),
        pod([33.0, 2.4], 1), pod([35.4, 2.4], 1), pod([33.0, 4.8], 1),
        dict(t="box", soort="glaswand", c=[34.2, 10.8], w=6.0, d=7.4, h=2.8, a=0, kleur="#9fb3bd", glas=True, n=1),
        dict(t="box", soort="vergadertafel", c=[34.2, 10.8], w=3.6, d=1.2, h=0.75, a=0, kleur=HOUT, n=1),
        dict(t="box", soort="raambar", c=[24.0, 0.7], w=10, d=0.5, h=1.05, a=0, kleur=HOUT, n=1),
        plant([31.2, 7.2], 0.5, 1.6, 1), plant([18.4, 13.6], 0.5, 1.6, 1), plant([30.0, 13.4], 0.5, 1.6, 1),
        # buiten
        boom([3, -5], 1.6, 6), boom([12, -6], 1.6, 6), boom([24, -5.4], 1.6, 6), boom([34, -6], 1.6, 6),
    ],
    dak=dict(soort="terras", terras=R(18.4, 1.0, 29.6, 9.4),
             groen=[], pv=[R(0.8, 0.8, 17.2, 17.6)], koepels=[[24.0, 5.0, 0.0]],
             tekst_en="A club roof terrace of about 95 m2 above the café corner with wooden decking, a black steel pergola, planters and a railing. Light-weight solar panels across the sports hall roof.",
             tekst="De verdieping heeft al een bovenwoning met dakterras (wordt verhuurd). Optie: een clubdakterras van circa 95 m² op het dak boven het café, met trap vanaf de verdieping. "
                   "Zonnepanelen in lichte uitvoering op het dak van de sportzaal (staaldak, ballast beperken)."),
    renders=dict(buiten=[(2, "Gevel en entree", "Keep this two-storey sports building and the big trees, make it a members club: grey steel cladding repainted deep olive green, the red accents replaced by warm wood, a wooden entrance canopy with plants, the parking turned into a planted forecourt with a terrace and benches, a roof terrace with pergola and greenery visible at the top.")]),
)

ONTWERPEN = {"utrecht-van-heutszstraat-4": UTRECHT, "den-bosch-rietveldenweg-13": RIETVELDEN, "den-bosch-eendenkooi-1a": EENDENKOOI}


def poly_area(p):
    return abs(sum(p[i][0] * p[(i + 1) % len(p)][1] - p[(i + 1) % len(p)][0] * p[i][1] for i in range(len(p)))) / 2


def kleuren_tekst(palet):
    p = PALET[palet]
    return {"pistache": "olive green velvet, pistachio, plum and travertine",
            "avocado": "deep olive, butter yellow and walnut",
            "rots": "slate blue, deep sea blue, cognac leather and stone",
            "granaat": "oxblood red, pomegranate red, blush pink and cream",
            "vijg": "fig purple, raspberry flesh and terracotta",
            "kokos": "coconut husk brown, sand, coconut white and palm green",
            "beton": "board-marked concrete grey with moss green",
            "verhuur": "neutral"}[palet] if p else ""


LABELS = {
    "utrecht-van-heutszstraat-4": {"Boekencafé aan de tuin": [5.6, 7.35], "Stille bieb in de boekentoren": [2.8, 13.3], "Werkzone met eilanden": [20.0, 3.95],
                                   "Wastoren": [29.2, 7.0], "Gym in de achtervleugel": [30.6, 18.8], "Studio": [31.1, 3.0], "Entree in de punt": [18.4, 12.2]},
    "den-bosch-rietveldenweg-13": {"Boekencafé achter de showroomramen": [14.0, 11.7], "Gym": [30.4, 7.2], "Werkzone": [15.2, 22.3], "Espressobar": [19.4, 12.1],
                                   "Bieb": [32.2, 20.0], "Techniek en opslag": [38.6, 4.6]},
    "den-bosch-eendenkooi-1a": {"Gym in de sportzaal": [9.0, 9.4], "Boekencafé bij de entree": [25.0, 9.3], "Kleedkamers met V-wastrog": [33.9, 11.4],
                                "Verdieping: werkzone": [25.0, 5.9]},
}
VIDES = {"den-bosch-eendenkooi-1a": [dict(naam="Vide boven de sportzaal", poly=R(0.3, 0.3, 17.5, 18.1), n=1)]}


def export(slug):
    O = ONTWERPEN[slug]
    out = dict(O)
    zs = []
    for z in O["zones"]:
        if z.get("n", 0) < 0:
            continue
        z = dict(z, m2=round(poly_area(z["poly"])), kleur=PALET[z["palet"]]["vloer"], palet_naam=PALET[z["palet"]]["naam"])
        if z.get("details") is None:
            z["details"] = []
        if z["naam"] in LABELS.get(slug, {}):
            z["label"] = LABELS[slug][z["naam"]]
        if z["prompt"]:
            z["prompt_vol"] = z["prompt"] + " " + BASIS_PROMPT.format(kleuren=kleuren_tekst(z["palet"]))
        zs.append(z)
    out["zones"] = zs
    out["vides"] = VIDES.get(slug, [])
    out["palet"] = PALET
    return out



# ---------------------------------------------------------------- Voorhout
VOORHOUT = dict(
    titel="Dinsdagse Wetering 56A, Voorhout",
    sub="Twee werkplaatsen van een oud bouwbedrijf (deels 1933) met een verharde tuinstraat ertussen, station op loopafstand",
    hoogte=3.9, niveaus={"1": 3.0},
    extra=[dict(ctx=156, naam="Gebouw A, hoge deel"), dict(ctx=143, naam="Gebouw B")],
    concept="Vanaf de straat loop je de tuinstraat in tussen de twee werkplaatsen: grind wordt groen, met bomen, bankjes en een lange tafel buiten. "
            "Gebouw A (de lange werkplaats uit 1933 met de blauwe glazen gevel) wordt boekencafé en werkzone, met een boekenwand als scheiding. "
            "In het hoge deel aan het eind komt de entree met de boekentoren, en op de bestaande entresol een werkzolder. "
            "Gebouw B wordt de gym, met de wastoren in het lage deel en de douchetoren in de werkplaats. Boven in B komt een kleine studio.",
    pui=[[[1, 0], [22, 0]], [[0, 0.6], [0, 7]], [[21, -4.6], [33, -4.6]]],
    zones=[
        zone("Boekencafé in de werkplaats van 1933", "café", R(0.3, 0.3, 11.4, 7.3),
             "De oudste werkplaats wordt het café: lang, laag en licht door de blauwe glasgevel aan de tuinstraat. Een ronde bank rond de haard, een lange espressobar tegen de achterwand en een dubbele boekenkast die het café van de werkzone scheidt.",
             ["Ronde bank van 3,8 m doorsnee in olijfgroen fluweel, open naar het glas en de tuinstraat",
              "Espressobar van 3,5 m langs de achterwand, steigerhout met travertin blad",
              "Dubbelzijdige boekenkast van 6 m als scheiding met de werkzone: 1.500 boeken",
              "Blauwe kozijnen blijven, alleen opnieuw in diep olijf gelakt; houten spanten zichtbaar",
              "Pruimkleurige fauteuils en kleine ronde tafels bij het glas"],
             foto=6, cam=dict(t=[5.8, 3.8], afstand=9, hoek=210),
             prompt="Transform this long low workshop with blue glazed facade into the book café of a members club: keep the long glass facade and the low roof, repaint the blue frames deep olive green. Inside: a round olive-green velvet sofa around a black freestanding fireplace, a long espresso bar of reclaimed wood with travertine top against the back wall, a double-sided walnut bookcase full of books dividing the space, plum armchairs by the glass, plants and small trees."),
        zone("Werkzone achter de boekenwand", "werken", R(11.6, 0.3, 22.6, 7.3),
             "Zestien zit-sta bureaus in vier eilanden achter de boekenwand, met daglicht van de glasgevel en een ronde belcel aan het eind.",
             ["Vier eilanden van vier bureaus, licht gedraaid", "Eén ronde belcel in leisteenblauw vilt",
              "Akoestische panelen in blauwgrijs tussen de spanten", "Planten in de vensterbank langs het glas"],
             foto=7, cam=dict(t=[17, 3.8], afstand=9, hoek=210),
             prompt="Turn this long workshop with a glass facade into a calm coworking room: islands of four sit-stand desks with oak tops, each slightly rotated, dual monitors, a round slate-blue felt phone booth at the end, slate-blue acoustic panels between the timber trusses, plants along the glass."),
        zone("Entree en boekentoren", "entree", [[22.8, 0.0], [22.8, 7.6], [24.7, 7.6], [24.7, 8.6], [30.1, 8.6], [30.2, 0.0]],
             "Het hoge deel van gebouw A wordt de voordeur aan de tuinstraat. Je komt binnen bij de ronde boekentoren; de trap gaat naar de werkzolder op de bestaande entresol.",
             ["Ronde boekentoren van 3,8 m doorsnee met walnoten kasten rondom", "Kokospalet: jute kleed, rotan lamp, leren bank",
              "Ledenbord en streepjeslijst bij de deur", "Stalen trap naar de entresol"],
             foto=5, cam=dict(t=[26.4, 4.2], afstand=7, hoek=220),
             prompt="Turn this high workshop part with glazed doors into the entrance of a members club: black steel and glass doors, a round reading room with walnut bookshelves all around standing in the space, jute rug, rattan pendant, a leather bench, a black steel stair to a mezzanine, olive trees in clay pots."),
        zone("Wastoren", "sanitair", [[11.8, -4.8], [20.6, -4.8], [20.6, -10.4], [14.8, -10.4], [12.6, -10.4], [12.6, -7.6], [11.8, -7.6]],
             "In het lage deel van gebouw B staat de wastoren, met de opening naar de tuinstraat.",
             ["Wastoren van 5,5 m doorsnee, wastrog langs de V, drie toiletten erachter", "Lichtstraat erboven, planten op de rand"],
             cam=dict(t=[17, -7.6], afstand=7, hoek=210),
             prompt="An octagonal concrete-look bathroom tower (eight flat faces, still reads as a round object), 5.5 m diameter and 3 m high, inside an old brick workshop, board-marked plaster, a V-shaped concrete wash trough with brass taps, ivy hanging over the rim, a skylight above."),
        zone("Gym in gebouw B", "gym", R(20.9, -15.2, 33.4, -4.8),
             "De machinale werkplaats van gebouw B wordt de gym: vier racks, roeiers, een vrije vloer en de douchetoren in de hoek. De glazen gevel kijkt uit op de tuinstraat.",
             ["Vier racks op eiken platforms", "Drie roeiers bij het glas", "Douchetoren van 4,5 m doorsnee",
              "Ossenbloed accentwand, rubber vloer"], foto=10, cam=dict(t=[27, -10], afstand=10, hoek=210),
             prompt="Turn this brick workshop with large blue-framed windows into a functional gym: four black power racks on oak platforms, rowing machines facing the windows, anthracite rubber floor, one wall in oxblood red, a round concrete-look shower tower with plants on its rim in the corner, big plants. Repaint the blue frames black."),
        zone("Techniek en fietsen", "techniek", R(15, -16.5, 20.6, -10.6), "Warmtepomp, batterij, fietsen en opslag.", []),
        zone("Werkzolder op de entresol", "werken", [[22.9, 0.2], [30.1, 0.2], [30.1, 8.5], [24.8, 8.5], [24.8, 7.5], [22.9, 7.5]],
             "Op de bestaande entresol: zes werkplekken aan een lange tafel en twee belcellen, met uitzicht in de hoge ruimte.",
             ["Lange werktafel voor zes", "Twee ronde belcellen", "Stalen balustrade met plantenbak"], n=1, cam=dict(t=[26.4, 4.2], afstand=7, hoek=220),
             prompt="A mezzanine work loft in a high old workshop: a long oak table for six with lamps, two round slate-blue felt phone booths, a black steel balustrade with planters, view down into the entrance with a round bookshelf room."),
        zone("Studio boven in gebouw B", "studio", R(15, -16.5, 20.6, -10.6),
             "Op de verdieping van gebouw B (nu kantoor en kantine) komt een kleine studio voor yoga en mobiliteit.",
             ["Vijgenpaarse gordijnen, terracotta kleed", "Ruimte voor zes tot acht matten"], n=1, cam=dict(t=[17.8, -13.5], afstand=6, hoek=210),
             prompt="A small attic studio for yoga with fig-purple curtains, a terracotta rug, wooden floor, mats on an open shelf, warm light."),
    ],
    buiten=[dict(naam="Tuinstraat", poly=R(-3, -4.4, 33.6, -0.4), kleur="#cdbf9f"),
            dict(naam="Erf", poly=R(30.6, -4.6, 38.5, 0), kleur="#cdbf9f")],
    elementen=[
        *zitkuil([4.4, 3.8], 1.9, 270, "#6f7d3a", "#d9ccb0"),
        dict(t="box", soort="bar", c=[8.4, 6.9], w=3.6, d=0.7, h=1.1, a=0, kleur=HOUT),
        *kasten(0.8, 6.8, 11.5, a=90, d=0.5, h=2.2),
        *tafeltje([8.6, 1.5]), *tafeltje([9.2, 4.0]), boom([1.0, 6.6], 0.8, 2.6), plant([7.0, 0.8]), plant([10.8, 0.8]),
        dict(t="box", soort="fauteuil", c=[1.2, 1.2], w=0.85, d=0.85, h=0.8, a=30, kleur="#5a2741"),
        *eiland([14.2, 2.1], -5), *eiland([18.8, 2.0], 6), *eiland([15.2, 5.4], 8), *eiland([19.7, 5.3], -4),
        pod([22.0, 3.7]), plant([12.2, 0.8]), plant([21.6, 0.8]),
        *boekentoren([26.4, 4.4], 1.9, 270), dict(t="kleed", c=[26.4, 1.4], w=3, d=1.6, a=0, kleur="#d5bd96"),
        dict(t="box", soort="trap", c=[29.4, 4.6], w=1.0, d=3.4, h=0.3, a=0, kleur="#cfc8ba"),
        boom([23.6, 1.2], 0.6, 2.4),
        *toren([17.0, -7.6], 2.75, 90, "was"),
        *rack([32.4, -13.6], 90), *rack([32.4, -11.0], 90), *rack([25.0, -14.2], 0), *rack([27.8, -14.2], 0),
        roeier([23.0, -6.0], 0), roeier([25.6, -6.0], 0), roeier([28.2, -6.0], 0),
        dict(t="kleed", c=[25.6, -10.0], w=5, d=3.2, a=0, kleur="#c7928a"),
        *toren([31.2, -7.0], 2.15, 180, "douche"),
        dict(t="box", soort="techniek", c=[17.8, -13.6], w=4.4, d=4.6, h=2.4, a=0, kleur="#8f8a80"),
        # werkzolder (n=1)
        dict(t="box", soort="werktafel", c=[26.4, 2.2], w=3.6, d=1.0, h=0.75, a=0, kleur=HOUT, n=1),
        pod([24.2, 6.2], 1), pod([28.4, 6.8], 1), plant([29.5, 1.0], 0.4, 1.2, 1),
        # studio (n=1)
        dict(t="kleed", c=[17.8, -13.6], w=4.4, d=4.4, a=0, kleur="#b8633f", n=1),
        dict(t="boog", soort="gordijn", c=[17.8, -6.0], r=5.0, a0=245, a1=295, d=0.08, h=2.4, kleur="#4b2339", n=1),
        # tuinstraat
        *[boom([u, -2.4], 0.9, 3.0) for u in (3.5, 12.5, 21.5, 30.0)],
        dict(t="box", soort="buitentafel", c=[8.0, -2.4], w=4.0, d=0.9, h=0.75, a=0, kleur=HOUT),
        *[dict(t="box", soort="bank", c=[x, -3.6], w=2.0, d=0.5, h=0.45, a=0, kleur=HOUT) for x in (16.6, 26.0)],
        *[dict(t="box", soort="plantenbak", c=[x, -0.9], w=2.4, d=0.5, h=0.6, a=0, kleur="#5a3a22") for x in (6, 10, 15, 19)],
        dict(t="box", soort="fietsenrek", c=[35.0, -2.4], w=4, d=0.6, h=0.9, a=90, kleur=STAAL),
    ],
    dak=dict(soort="pv", terras=None, groen=[], pv=[R(0.8, 0.6, 22.2, 3.6), R(21.4, -15.0, 33.0, -10.6)],
             koepels=[[17.0, -7.6, 0.9], [15.4, 3.8, 0.7], [20.0, 3.8, 0.7]],
             tekst_en="The pitched roofs stay; solar panels on the south-facing slopes of both workshops and skylights above the bathroom tower and the workspace. The gravel strip between the buildings becomes a green garden street with small trees, a long outdoor table and benches.",
             tekst="De daken zijn schuin (3D BAG): geen dakterras. Zonnepanelen op de zuidkanten van A en B, lichtstraten boven de wastoren en de werkzone. "
                   "De buitenruimte is de tuinstraat tussen de gebouwen, met bomen, een lange tafel en bankjes."),
    renders=dict(buiten=[(6, "Gevel aan de tuinstraat", "Keep this long single-storey workshop with its glass facade and the gravel yard, turn it into a members club: frames repainted deep olive green, the gravel yard becomes a green garden street with four small trees, planters, a long wooden outdoor table and benches, warm string lights. Keep the neighbouring houses unchanged."),
                         (8, "Tuinstraat tussen A en B", "Turn this gravel strip between two workshops into a green garden street of a members club: small trees, climbing plants on the brick walls, planters, wooden benches, bike racks at the end, frames repainted olive green and black, warm evening light."),
                         (1, "Vanaf de straat", "Keep this street view and the houses exactly; make the old workshop gate the subtle entrance of a members club: black steel gate with a small brass sign, climbing plants and a small tree, a glimpse of a green garden street behind it.")]),
)

# ---------------------------------------------------------------- Maarssen
MAARSSEN = dict(
    titel="Herenweg 15, Maarssen",
    sub="Woonhuis uit 1931 met een bedrijfshal uit 1970 erachter, aan de rand van de polder",
    hoogte=5.8, niveaus={"1": 3.0},
    extra=[dict(ctx=4, naam="Bedrijfshal 1970", h=7.0)],
    concept="Het voorhuis uit 1931 wordt het boekencafé, met een ronde bank in de ronde erker en de bieb op zolder. Via een kleine binnenplaats "
            "loop je naar de hal uit 1970: gym aan de westkant, werkzone en wastoren in het midden. De hal krijgt grote glazen deuren naar het erf "
            "en de tuin met uitzicht over de weilanden. Op het dak van de hal komen zonnepanelen.",
    pui=[[[5.1, 9.4], [12.0, 9.4]], [[-13, 16.0], [4.6, 16.0]], [[5.05, 17], [5.05, 31.5]]],
    zones=[
        zone("Boekencafé in het voorhuis", "café", [[0.3, 0.3], [11.6, 0.3], [11.6, 2.9], [12.4, 2.9], [14.4, 5.0], [14.5, 7.0], [12.0, 9.1], [5.1, 9.1], [5.1, 11.7], [2.8, 11.7], [2.8, 7.7], [0.3, 7.7]],
             "Het woonhuis uit 1931 wordt het café. In de ronde erker komt een ronde bank rond de haard, de oude keuken wordt de espressobar en tegen de zijmuur staat de boekenwand. Nieuwe tuindeuren aan de achterkant.",
             ["Ronde bank in olijfgroen fluweel die de ronde erker volgt", "Espressobar in de oude keuken, travertin blad",
              "Boekenwand van vloer tot plafond tegen de zijmuur", "Originele details uit 1931 blijven: deuren, lijsten, vloer waar het kan",
              "Glazen tuindeuren naar de binnenplaats"], cam=dict(t=[7, 4.8], afstand=9, hoek=210),
             prompt="A 1930s Dutch brick house turned into the book café of a members club: a curved olive-green velvet sofa following a round bay window around a black freestanding fireplace, an espresso bar with travertine top in the old kitchen, a floor-to-ceiling walnut bookcase, plum armchairs, original 1930s doors and mouldings, glass garden doors at the back, plants."),
        zone("Stille bieb op zolder", "bieb", R(0.6, 0.6, 11.4, 7.4),
             "Onder de kap van het voorhuis: de stille bieb met lage kasten, fauteuils en dakramen.",
             ["Lage boekenkasten onder de schuine kap", "Fauteuils in olijf, botergele lampen", "Dakramen voor daglicht"], n=1,
             cam=dict(t=[6, 4], afstand=8, hoek=210),
             prompt="A quiet attic library under a pitched roof with exposed timber rafters: low walnut bookcases under the slopes, deep olive walls, olive velvet armchairs, butter-yellow lamps, roof windows with daylight."),
        zone("Gym in de hal", "gym", R(-14.6, 16.4, -4.6, 35.7),
             "De westkant van de hal van 7 m hoog: vier racks langs de lange wand, roeiers, een vrije vloer voor groepslessen en de douchetoren in de hoek.",
             ["Vier racks op eiken platforms langs de westwand", "Groepslesvloer met een gebogen gordijn voor yoga",
              "Douchetoren van 4,5 m doorsnee", "Ossenbloed accentwand, hoge ramen"], cam=dict(t=[-9.6, 26], afstand=12, hoek=210),
             prompt="A functional gym inside a 7 m high 1970s steel hall: four black power racks on oak platforms along the long wall, rowing machines, an open floor for classes with a curved fig-purple curtain, anthracite rubber floor, one wall oxblood red, a round concrete-look shower tower with plants on its rim, big plants, daylight from high windows and big glass doors."),
        zone("Werkzone in de hal", "werken", R(-4.4, 16.4, 4.8, 27.8),
             "Zestien bureaus in vier eilanden achter de nieuwe glazen deuren, met uitzicht over het erf en de weilanden. Twee ronde belcellen.",
             ["Vier eilanden van vier bureaus", "Twee ronde belcellen", "Glazen hefdeuren naar het oosten, uitzicht op de polder"],
             cam=dict(t=[0.2, 22], afstand=10, hoek=210),
             prompt="A coworking area inside a high 1970s hall: islands of four sit-stand desks with oak tops slightly rotated, two round slate-blue felt phone booths, big glass doors opening to a green yard and meadows, slate-blue acoustic baffles hanging high, plants."),
        zone("Wastoren", "sanitair", R(-4.4, 27.8, 4.8, 35.7), "De wastoren in het midden van de hal, open naar de werkzone.",
             ["Wastoren van 5,5 m doorsnee", "Lichtstraat erboven"], cam=dict(t=[0.2, 32], afstand=8, hoek=210),
             prompt="An octagonal concrete-look bathroom tower (eight flat faces, still reads as a round object), 5.5 m diameter and 3 m high, standing free in a high steel hall, board-marked plaster, a V-shaped concrete wash trough with brass taps, ivy hanging over the rim, daylight from a skylight above."),
        zone("Fietsen en techniek", "techniek", R(5.1, 32.4, 12.6, 35.9), "Fietsen, warmtepomp, batterij en opslag.", []),
    ],
    buiten=[dict(naam="Binnenplaats", poly=R(-4.6, 12.3, 5.0, 15.8), kleur="#b08a5e"),
            dict(naam="Tuin naar de weilanden", poly=[[14.8, -6.0], [21.4, -6.0], [21.6, 36.5], [7.2, 36.2], [7.2, 31.8], [13.0, 31.8], [13.0, 9.6], [14.8, 9.6]], kleur="#9bb07a"),
            dict(naam="Parkeren", poly=R(-4.6, -9.8, 14.6, -0.6), kleur="#c9c3b6")],
    elementen=[
        *zitkuil([11.6, 6.0], 1.9, 180, "#6f7d3a", "#d9ccb0"),
        dict(t="box", soort="bar", c=[3.9, 9.6], w=2.0, d=0.7, h=1.1, a=90, kleur=HOUT),
        *kasten(0.8, 7.0, 0.5, a=90, d=0.4, h=2.6),
        *tafeltje([4.0, 2.2]), *tafeltje([7.2, 2.2]), *tafeltje([4.6, 5.4]),
        dict(t="box", soort="fauteuil", c=[8.6, 1.4], w=0.85, d=0.85, h=0.8, a=-20, kleur="#5a2741"), plant([10.8, 1.0]), plant([6.2, 8.4]),
        # zolder
        *kasten(1.0, 10.0, 1.0, d=0.4, h=1.1, n=1), *kasten(1.0, 10.0, 6.8, d=0.4, h=1.1, n=1),
        *[dict(t="box", soort="fauteuil", c=[u, 4.0], w=0.85, d=0.85, h=0.8, a=0, kleur="#47522a", n=1) for u in (3.0, 6.0, 9.0)],
        # gym
        *rack([-13.8, 19.4], 90), *rack([-13.8, 22.4], 90), *rack([-13.8, 25.4], 90), *rack([-13.8, 28.4], 90),
        roeier([-8.0, 17.4], 0), roeier([-8.0, 19.0], 0),
        dict(t="kleed", c=[-9.0, 24.6], w=5, d=6, a=0, kleur="#c7928a"),
        dict(t="boog", soort="gordijn", c=[-9.0, 21.0], r=4.6, a0=60, a1=120, d=0.08, h=3.0, kleur="#4b2339"),
        *toren([-7.0, 33.2], 2.25, 270, "douche"), boom([-13.6, 34.4], 0.9, 3.4),
        # werkzone
        *eiland([-1.8, 19.2], -6), *eiland([2.4, 19.4], 7), *eiland([-1.6, 23.8], 9), *eiland([2.6, 24.0], -5),
        pod([3.9, 27.0]), pod([-3.4, 27.0]), plant([4.2, 17.0], 0.5, 1.6),
        *toren([0.2, 31.8], 2.75, 270, "was"),
        dict(t="box", soort="fietsenrek", c=[9.0, 34.2], w=5, d=0.6, h=0.9, a=0, kleur=STAAL),
        # buiten
        *tafeltje([-1.6, 14.0], stoelen=3), *tafeltje([2.2, 14.0], stoelen=3), boom([-3.6, 14.4], 0.8, 2.8),
        dict(t="ring", soort="pergola", c=[17.6, 20.0], r=2.6, open=90, gat=0, h=2.6, kleur="#2f3032", dun=True),
        dict(t="boog", soort="bank", c=[17.6, 20.0], r=2.2, a0=200, a1=340, d=0.5, h=0.45, kleur=HOUT),
        *tafeltje([17.0, 5.0], stoelen=3), *tafeltje([18.6, 9.0], stoelen=3),
        boom([19.8, 0.0]), boom([20.2, 14.0]), boom([19.6, 28.0]), boom([16.0, 33.6], 0.9, 3.0), boom([-3.6, -2.6]), boom([13.0, -2.6]),
    ],
    dak=dict(soort="pv", terras=None, groen=[], pv=[R(-14.4, 16.6, 4.6, 27.4), R(-14.4, 29.0, -9.6, 35.6)],
             koepels=[[0.2, 31.8, 0.9], [-7.0, 33.2, 0.8]],
             tekst_en="The 1931 house keeps its red clay tiles. The flat roof of the 1970 hall gets light-weight solar panels and two round skylights above the towers. The yard and garden towards the meadows get trees, a round black steel pergola with a curved bench and a terrace.",
             tekst="Het voorhuis houdt zijn rode pannen. Op het platte dak van de hal komen lichtgewicht zonnepanelen en twee ronde lichtkoepels boven de torens. "
                   "Geen dakterras: de tuin naar de weilanden is groot genoeg en een staaldak uit 1970 draagt meestal weinig."),
    renders=dict(buiten=[]),
)

ONTWERPEN.update({"voorhout-dinsdagse-wetering-56a": VOORHOUT, "maarssen-herenweg-15": MAARSSEN})
LABELS.update({
    "voorhout-dinsdagse-wetering-56a": {"Boekencafé in de werkplaats van 1933": [5.8, 6.6], "Werkzone achter de boekenwand": [17.0, 3.8],
                                        "Entree en boekentoren": [26.4, 1.0], "Wastoren": [17.0, -5.4], "Gym in gebouw B": [27.0, -9.6],
                                        "Techniek en fietsen": [17.8, -13.6], "Werkzolder op de entresol": [26.4, 4.4], "Studio boven in gebouw B": [17.8, -13.6]},
    "maarssen-herenweg-15": {"Boekencafé in het voorhuis": [5.6, 4.0], "Gym in de hal": [-9.6, 27.0], "Werkzone in de hal": [0.2, 21.6],
                             "Wastoren": [0.2, 29.0], "Fietsen en techniek": [8.8, 33.2], "Stille bieb op zolder": [6.0, 4.0]},
})


# ================================================================ Herontwerp v2 (13 november 2026)
# Eisen: 36 tot 40 werkplekken (piek bij 30 vol + 30 deeltijd = circa 36 tegelijk), compacte zit-sta bureaus 140 x 70,
# een grote tafel, vergaderkamers, een goede keuken, de gym afsluitbaar en akoestisch gescheiden van de werkplekken.
# Maatvoering: 90 cm achter de stoel, looppaden 110 tot 120 cm, vergaderkamer 2 tot 2,5 m2 per persoon,
# gymvloer 30 tot 40 mm rubber op akoestische ondervloer met platforms onder de racks, buffer tussen gym en werken.
# De v1-indelingen hierboven blijven staan als vorige ronde; ONTWERPEN gebruikt v2.

def eiland2(c, a, n=0, k=4):
    """k (4 of 6) compacte zit-sta bureaus 140 x 70 rug aan rug, licht gedraaid."""
    out = []
    ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
    xs = [-0.7, 0.7] if k == 4 else [-1.4, 0, 1.4]
    for du in xs:
        for dv, rot in ((-0.35, 0), (0.35, 180)):
            x, y = c[0] + du * ca - dv * sa, c[1] + du * sa + dv * ca
            out.append(dict(t="bureau", c=[round(x, 2), round(y, 2)], w=1.4, d=0.7, a=a + rot, n=n))
    return out


def grote_tafel(c, lengte, a=0, n=0):
    """Lange werktafel van 1 m breed, 70 cm per persoon aan beide kanten."""
    pers = 2 * int(lengte / 0.7)
    out = [dict(t="box", soort="grote tafel", c=c, w=lengte, d=1.0, h=0.75, a=a, kleur=HOUT, pers=pers, n=n)]
    ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
    k = pers // 2
    for i in range(k):
        du = -lengte / 2 + 0.35 + i * (lengte - 0.7) / max(1, k - 1)
        for dv in (-0.72, 0.72):
            out.append(dict(t="cil", soort="stoel", c=[round(c[0] + du * ca - dv * sa, 2), round(c[1] + du * sa + dv * ca, 2)], r=0.22, h=0.45, kleur="#5a3a22", n=n))
    return out


def vergaderkamer(c, w, d, a=0, pers=8, n=0):
    """Vergaderkamer: wanden half glas, half dicht; tafel 2,4 x 1,0 voor 8 (1,6 x 0,9 voor 4), scherm aan de kopse kant."""
    tl = 2.4 if pers >= 8 else (2.0 if pers >= 6 else 1.4)
    ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
    out = [dict(t="box", soort="vergaderkamer", c=c, w=w, d=d, h=2.6, a=a, kleur="#9fb3bd", glas=True, pers=pers, n=n),
           dict(t="box", soort="vergadertafel", c=c, w=tl, d=1.0, h=0.75, a=a, kleur=HOUT, n=n),
           dict(t="box", soort="scherm", c=[c[0] + (w / 2 - 0.15) * ca, c[1] + (w / 2 - 0.15) * sa], w=0.08, d=1.4, h=1.6, a=a, kleur="#1f2022", n=n)]
    k = pers // 2
    for i in range(k):
        du = -tl / 2 + 0.3 + i * (tl - 0.6) / max(1, k - 1)
        for dv in (-0.75, 0.75):
            out.append(dict(t="cil", soort="stoel", c=[round(c[0] + du * ca - dv * sa, 2), round(c[1] + du * sa + dv * ca, 2)], r=0.24, h=0.45, kleur="#44606f", n=n))
    return out


def keuken(c, lengte, a=0, n=0):
    """Keukenblok tegen de wand: 65 cm diep, met een hoge kast (koelkast, combi-stoomoven) aan het eind."""
    ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
    return [dict(t="box", soort="keuken", c=c, w=lengte, d=0.65, h=0.92, a=a, kleur="#47522a", n=n),
            dict(t="box", soort="hoge kast", c=[c[0] + (lengte / 2 - 0.65) * ca, c[1] + (lengte / 2 - 0.65) * sa], w=1.2, d=0.66, h=2.2, a=a, kleur="#3a4423", n=n),
            dict(t="label", c=c, tekst="keuken", n=n)]


def kookeiland(c, a=0, n=0, lengte=2.6):
    return [dict(t="box", soort="kookeiland", c=c, w=lengte, d=1.0, h=0.92, a=a, kleur=HOUT, n=n),
            dict(t="cil", soort="espressomachine", c=c, r=0.25, h=1.4, kleur="#c9c3b6", n=n)]


def wand(pts, h, glas=False, gym=False, bestaand=False, n=0, t=0.2):
    return dict(t="wand", pts=pts, h=h, glas=glas, gym=gym, bestaand=bestaand, n=n, dikte=t)


def deur(c, a, toegang=False, n=0, w=1.0):
    return dict(t="deur", c=c, a=a, w=w, toegang=toegang, n=n)


def label(c, tekst, n=0):
    return dict(t="label", c=c, tekst=tekst, n=n)


def pod2(c, n=0):
    return dict(t="cil", soort="belcel", c=c, r=0.7, h=2.3, kleur="#44606f", n=n)


# ================================================================ Bouwstenen v3 (16 november 2026): inrichting verdiept
# Zie inrichting/torens.py (vormstudie) en inrichting/programma.py (normen). Torens worden achthoekig (vlakke zijden binnen en buiten),
# of D-vormig met de rug tegen een bestaande wand. Banken worden veelhoeken met open zijden, zitnissen langs wanden, lockers op vlakke vlakken.
BETON, LOCKER = "#bdb6a8", "#5f6b5c"
PLANTEN = {  # naam: (straal kroon, hoogte, licht) [schatting], zie inrichting/onderzoek.md
    "kentia": (0.7, 2.4, "laag tot middel"), "ficus elastica": (0.6, 2.2, "middel"), "strelitzia nicolai": (0.8, 2.6, "hoog"),
    "monstera": (0.7, 1.6, "middel"), "zz-plant": (0.35, 0.8, "laag"), "sansevieria": (0.3, 0.9, "laag"), "dracaena": (0.4, 1.8, "laag tot middel"),
    "schefflera": (0.6, 2.0, "middel"), "olijf": (0.8, 2.6, "zeer hoog"), "aspidistra": (0.35, 0.7, "laag"), "philodendron": (0.5, 1.2, "middel"),
}


def plant3(c, soort="monstera", n=0, z=0.0):
    r, h, _ = PLANTEN[soort]
    return dict(t="plant", c=c, r=r * 0.8, h=h, n=n, z=z, naam=soort)


def boom3(c, soort="kentia", n=0):
    r, h, _ = PLANTEN[soort]
    return dict(t="boom", c=c, r=r * 1.3, h=h + 0.6, n=n, naam=soort)


def hangplant(c, z=3.0, n=0, soort="pothos"):
    """Hangplant aan een balk of kabel; z is de hoogte boven de vloer van het niveau."""
    return dict(t="plant", c=c, r=0.35, h=0.4, n=n, z=z, naam=soort, hang=True)


def _pt(c, R, a):
    return [round(c[0] + R * math.cos(math.radians(a)), 3), round(c[1] + R * math.sin(math.radians(a)), 3)]


def achthoektoren(c, R, open_deg, soort="was", n=0, lockers=(), H=3.0):
    """Achthoekige sanitairtoren (omgeschreven straal R), opening gecentreerd op open_deg.
    soort 'was': drie toiletcabines tegen de drie achterste zijden en een V-wastrog bij de entree.
    soort 'douche': vier douches tegen zijden 2, 3, 5, 6 en een bank tegen de achterzijde.
    lockers: zijde-indexen (1..7, 0 = entree) waar aan de buitenkant een lockerkast komt (circa 33 lockers per zijde).
    Bovenop een rand met klimop en varens (zelfwatergevende bakken)."""
    s = 2 * R * math.sin(math.pi / 8)
    ri = R * math.cos(math.pi / 8)                     # afstand hart tot zijde
    hoek = lambda k: open_deg + 22.5 + 45 * k          # hoekpunt na zijde k
    gat = 1.2 / s / 2                                  # halve opening als fractie van de zijde
    A, B = _pt(c, R, open_deg - 22.5), _pt(c, R, open_deg + 22.5)
    l = lambda t: [round(A[0] + (B[0] - A[0]) * t, 3), round(A[1] + (B[1] - A[1]) * t, 3)]
    pts = [l(0.5 + gat), B] + [_pt(c, R, hoek(k)) for k in range(1, 8)] + [l(0.5 - gat)]
    out = [dict(t="wand", pts=pts, h=H, glas=False, gym=False, bestaand=False, n=n, dikte=0.15, soort="torenwand")]
    zijde = lambda k, d: (_pt(c, ri - d, open_deg + 45 * k), open_deg + 45 * k)   # middelpunt op afstand d binnen de zijde, normaal
    if soort == "was":
        for k in (3, 4, 5):
            m, a = zijde(k, 0.8)
            out.append(dict(t="box", soort="toiletcabine", c=m, w=0.95, d=1.5, h=2.3, a=a + 90, kleur="#d6cdb8", n=n))
        for sgn in (-1, 1):
            m = _pt(c, 0.55, open_deg + sgn * 50)
            out.append(dict(t="box", soort="wastrog", c=m, w=1.5, d=0.45, h=0.9, a=open_deg + sgn * 40, kleur=BETON, n=n))
        out.append(dict(t="box", soort="spiegel", c=_pt(c, 0.0, 0), w=0.1, d=0.1, h=0.1, a=0, kleur=BETON, n=n))
    else:
        for k in (2, 3, 5, 6):
            m, a = zijde(k, 0.5)
            out.append(dict(t="box", soort="douche", c=m, w=0.95, d=0.95, h=2.2, a=a + 90, kleur="#9fb3bd", n=n))
        m, a = zijde(4, 0.3)
        out.append(dict(t="box", soort="bank", c=m, w=1.6, d=0.4, h=0.44, a=a + 90, kleur=HOUT, n=n))
    for k in lockers:
        m, a = zijde(k, -0.3)
        out.append(dict(t="box", soort="lockers", c=m, w=s - 0.2, d=0.5, h=2.0, a=a + 90, kleur=LOCKER, n=n))
    for k in range(8):
        out.append(dict(t="plant", c=_pt(c, R - 0.25, open_deg + 22.5 + 45 * k), r=0.32, h=0.5, n=n, z=H, naam="klimop"))
    return out


def dtoren(p0, p1, diep, soort="was", n=0, H=3.0):
    """D-vormige sanitairtoren met de rug tegen een bestaande wand van p0 naar p1; de bolle kant ligt links van p0 -> p1.
    Leidingen in de bestaande wand, cabines (was) of douches op een rij langs de rug, ronde voorkant met de entree in het midden."""
    B = math.dist(p0, p1); ux, uy = (p1[0] - p0[0]) / B, (p1[1] - p0[1]) / B; nx, ny = -uy, ux
    a_rug = math.degrees(math.atan2(uy, ux))
    m0 = [p0[0] + nx * diep, p0[1] + ny * diep]; m1 = [p1[0] + nx * diep, p1[1] + ny * diep]
    cm = [(m0[0] + m1[0]) / 2, (m0[1] + m1[1]) / 2]; R = B / 2
    a_n = math.degrees(math.atan2(ny, nx)); gat = math.degrees(1.2 / R) / 2
    out = [wand([p0, m0], H, n=n, t=0.15), wand([p1, m1], H, n=n, t=0.15),
           dict(t="boog", soort="torenwand", c=cm, r=R, a0=a_n - 90, a1=a_n - gat, d=0.15, h=H, kleur="#e9e4d8", n=n),
           dict(t="boog", soort="torenwand", c=cm, r=R, a0=a_n + gat, a1=a_n + 90, d=0.15, h=H, kleur="#e9e4d8", n=n)]
    k = 3 if soort == "was" else 4
    w = 0.95
    for i in range(k):
        t = (i + 0.5) / k
        m = [p0[0] + ux * B * t + nx * 0.8, p0[1] + uy * B * t + ny * 0.8]
        out.append(dict(t="box", soort="toiletcabine" if soort == "was" else "douche", c=m, w=w, d=1.5 if soort == "was" else 0.95, h=2.3,
                        a=a_rug, kleur="#d6cdb8" if soort == "was" else "#9fb3bd", n=n))
    if soort == "was":
        out.append(dict(t="box", soort="wastrog", c=[cm[0] + nx * 0.6, cm[1] + ny * 0.6], w=min(2.4, B - 1.2), d=0.45, h=0.9, a=a_rug, kleur=BETON, n=n))
    for i in range(7):
        a = a_n - 90 + i * 30
        out.append(dict(t="plant", c=_pt(cm, R - 0.25, a), r=0.3, h=0.5, n=n, z=H, naam="klimop"))
    return out


def veelhoekbank(c, R, zijden=6, open=(0,), draai=0, kleur="#6f7d3a", haard=True, n=0):
    """Veelhoekige bank (zes- of achthoek) met open zijden om tussendoor te lopen, rug aan de buitenkant, haard in het midden.
    Circa 1 plek per 0,6 m zitlengte."""
    s = 2 * R * math.sin(math.pi / zijden); ri = R * math.cos(math.pi / zijden)
    out = [dict(t="kleed", c=c, r=R + 0.3, kleur="#d9ccb0", n=n)]
    for k in range(zijden):
        if k in open:
            continue
        a = draai + k * 360 / zijden
        m = _pt(c, ri - 0.3, a); mr = _pt(c, ri - 0.03, a)
        out.append(dict(t="box", soort="hexbank", c=m, w=s - 0.12, d=0.6, h=0.44, a=a + 90, kleur=kleur, n=n))
        out.append(dict(t="box", soort="rugleuning", c=mr, w=s - 0.12, d=0.1, h=0.85, a=a + 90, kleur=kleur, n=n))
    if haard:
        out.append(dict(t="cil", soort="haard", c=c, r=0.45, h=0.5, kleur="#3a3b3d", n=n))
        out.append(dict(t="cil", soort="tafeltje", c=_pt(c, R * 0.45, draai + 180 / zijden), r=0.28, h=0.42, kleur=HOUT, n=n))
    return out


def zitnis(p0, p1, tafels=True, kleur="#6f7d3a", n=0):
    """Bank langs een wand van p0 naar p1 (zit aan de linkerkant), met tafeltjes van 70 x 70 om de 1,4 m en losse stoelen ertegenover.
    Een zitnis haalt circa 1,7 plekken per meter tegen circa 1,2 met losse tafels."""
    L = math.dist(p0, p1); ux, uy = (p1[0] - p0[0]) / L, (p1[1] - p0[1]) / L; nx, ny = -uy, ux
    a = math.degrees(math.atan2(uy, ux))
    mid = lambda t, d: [round(p0[0] + ux * L * t + nx * d, 3), round(p0[1] + uy * L * t + ny * d, 3)]
    out = [dict(t="box", soort="zitnis", c=mid(0.5, 0.3), w=L, d=0.55, h=0.44, a=a, kleur=kleur, n=n),
           dict(t="box", soort="rugleuning", c=mid(0.5, 0.06), w=L, d=0.1, h=1.0, a=a, kleur=kleur, n=n)]
    if tafels:
        k = int(L / 1.4)
        for i in range(k):
            t = (i + 0.5) / k
            out.append(dict(t="box", soort="tafel", c=mid(t, 0.95), w=0.7, d=0.7, h=0.74, a=a, kleur=HOUT, n=n))
            out.append(dict(t="cil", soort="stoel", c=mid(t, 1.55), r=0.22, h=0.45, kleur="#5a3a22", n=n))
    return out


def focuskamer(c, a=0, n=0):
    """Glazen focuskamer voor 1 tot 2 personen, 2,2 x 1,9 m, tafel en twee krukken (oude ramen in houten regelwerk)."""
    ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
    return [dict(t="box", soort="focuskamer", c=c, w=2.2, d=1.9, h=2.5, a=a, kleur="#9fb3bd", glas=True, n=n),
            dict(t="box", soort="tafel", c=[c[0] + 0.45 * sa, c[1] - 0.45 * ca], w=1.4, d=0.6, h=0.74, a=a, kleur=HOUT, n=n),
            dict(t="cil", soort="stoel", c=[c[0] - 0.4 * ca, c[1] - 0.4 * sa], r=0.22, h=0.45, kleur="#44606f", n=n),
            dict(t="cil", soort="stoel", c=[c[0] + 0.4 * ca, c[1] + 0.4 * sa], r=0.22, h=0.45, kleur="#44606f", n=n)]


def lockerwand(c, w, a=0, n=0, h=2.0):
    """Lockerkast van w meter breed, 50 cm diep: kolommen van 30 cm, 5 hoog = circa 16 lockers per meter.
    Bovenop een doorlopende plantenbak met hangende pothos: de dode ruimte boven de kast wordt groen (water geven met een gieter met lange tuit)."""
    out = [dict(t="box", soort="lockers", c=c, w=w, d=0.5, h=h, a=a, kleur=LOCKER, n=n)]
    ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
    k = max(1, int(w / 1.2))
    for i in range(k):
        t = -w / 2 + (i + 0.5) * w / k
        out.append(dict(t="plant", c=[round(c[0] + t * ca, 3), round(c[1] + t * sa, 3)], r=0.3, h=0.4, n=n, z=h, naam="pothos"))
    return out


def groenwand(p0, p1, h=3.0, rots=False, n=0):
    """Groene wand: rotswand met plantvakken (rots=True) of klimwand van staalkabels met pothos en philodendron. Zonder water."""
    L = math.dist(p0, p1); ux, uy = (p1[0] - p0[0]) / L, (p1[1] - p0[1]) / L; nx, ny = -uy, ux
    a = math.degrees(math.atan2(uy, ux))
    out = [dict(t="box", soort="rotswand" if rots else "klimwand", c=[(p0[0] + p1[0]) / 2 + nx * 0.25, (p0[1] + p1[1]) / 2 + ny * 0.25],
                w=L, d=0.5 if rots else 0.08, h=h, a=a, kleur="#7a746a" if rots else "#5f7a3a", n=n)]
    k = max(2, int(L / 0.9))
    for i in range(k):
        t = (i + 0.5) / k
        z = (0.6 + (i % 3) * 0.9) if rots else 0.0
        out.append(dict(t="plant", c=[p0[0] + ux * L * t + nx * 0.55, p0[1] + uy * L * t + ny * 0.55], r=0.32, h=0.5 if rots else 1.0, n=n, z=z,
                        naam="varen" if rots else "pothos"))
    return out


def pingpong(c, a=0, n=0):
    """Tafeltennistafel 2,74 x 1,525 m; speelzone circa 5 x 8 m. Inklapbaar model, overdag tegen de wand."""
    return [dict(t="box", soort="pingpong", c=c, w=2.74, d=1.525, h=0.76, a=a, kleur="#2f5e46", n=n),
            dict(t="kleed", c=c, w=6.0, d=3.6, a=a, kleur="#d5bd96", n=n)]


def pooltafel(c, a=0, n=0):
    """Pooltafel 7 ft (2,1 x 1,2 m) met eettafelblad: speelzone circa 4 x 5 m; met blad erop een tafel voor acht."""
    return [dict(t="box", soort="pooltafel", c=c, w=2.1, d=1.2, h=0.8, a=a, kleur="#2f5e46", n=n)]


def stavergaderkamer(c, w, d, a=0, pers=5, n=0):
    """Sta-vergaderkamer: ronde statafel van 1,1 m hoog en circa 1,0 m doorsnee, een whiteboardwand, twee leunkrukken, geen stoelen.
    Stand-up vergaderingen duren circa een derde korter bij gelijke besluitkwaliteit (Bluedorn, Turban en Love 1999). Telt als vergaderkamer."""
    ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
    return [dict(t="box", soort="vergaderkamer", c=c, w=w, d=d, h=2.6, a=a, kleur="#9fb3bd", glas=True, pers=pers, sta=True, n=n),
            dict(t="cil", soort="statafel", c=c, r=0.5, h=1.1, kleur=HOUT, n=n),
            dict(t="box", soort="whiteboard", c=[c[0] - (w / 2 - 0.08) * ca, c[1] - (w / 2 - 0.08) * sa], w=0.04, d=min(d - 0.4, 2.4), h=1.3, a=a, kleur="#f4f1ea", n=n),
            dict(t="cil", soort="leunkruk", c=[c[0] + 0.8 * ca, c[1] + 0.8 * sa], r=0.18, h=0.75, kleur="#44606f", n=n),
            dict(t="cil", soort="leunkruk", c=[c[0] + 0.8 * sa, c[1] - 0.8 * ca], r=0.18, h=0.75, kleur="#44606f", n=n)]


def toren(c, r, open_deg, soort, n=0):  # noqa: F811  (vervangt de ronde toren: zie inrichting/torens.py)
    return achthoektoren(c, r, open_deg, soort, n=n)


# ---------------------------------------------------------------- Utrecht v2
UTRECHT.update(
    concept="Je komt binnen via de poort, de steeg en de binnentuin, door de punt van het gebouw. Links het boekencafé met de keuken, "
            "een kookeiland met de espressomachine, een grote tafel voor twaalf en een zeshoekige bank met twee open zijden rond de haard; daarachter de bieb met boekenwanden en twee focuskamers. "
            "Rechts de werkzone met zes eilanden van vier compacte zit-sta bureaus, met pothos boven de eilanden. Achterin een vergaderkamer voor zes en een sta-kamer waar eerst de studio was. De entree in de punt wordt de lockerlobby met een rotswand. "
            "De gym zit in de achtervleugel, achter de wastoren en de techniek: twee wanden en zes meter tussen sporten en werken, en een deur met toegangspas.",
    geluid="Gym in de achtervleugel, achter de wastoren en techniek: tussen de racks en de dichtstbijzijnde bureaus zit ruim 6 m en twee wanden. "
           "Dichte akoestische wand tot het dak met een deur op toegangspas. Vloer: 40 mm rubber op een akoestische ondervloer, platforms onder de racks.",
    zones=[
        zone("Entree in de punt", "entree", [[13.6, 10.2], [18.4, 15], [23, 10], [26, 10], [26, 8.2], [13.6, 8.2]],
             "De driehoekige punt die de binnentuin in steekt wordt de voordeur en de lockerlobby: links een lockerwand van 4,4 m langs de schuine muur, rechts een rotswand met varens, langs de rand drie belcellen.",
             ["Lockers voor circa 150 leden: 4,4 m langs de schuine wand, 3 m langs de rand en een zijde van de wastoren", "Rotswand met plantvakken (varens, geen water), kentia in de punt", "Drie ronde belcellen in leisteenblauw vilt (twee meer bij de werkzone en de wastoren)",
              "Ledenbord en streepjeslijst", "Twee olijfbomen markeren de deur"], foto=8,
             prompt="Turn this old community-centre entrance into the welcoming front door of a members club. Replace the blue door with a large black steel and glass door, fresh lime-washed brick in warm sand tones, two olive trees in big clay pots, a rattan pendant, a small brass plaque instead of the old sign."),
        zone("Boekencafé en keuken", "café", R(0.3, 0.3, 13.6, 8.2),
             "Het hart: een keuken van 4,4 m met een kookeiland waar de espressomachine op staat, een grote tafel voor twaalf aan de pui, een zeshoekige bank met twee open zijden rond de haard en een boekenwand van 7,6 m. Strelitzia en ficus staan aan het glas, pothos hangt boven de bank.",
             ["Keuken van 4,4 m: twee vaatwassers, combi-stoomoven, inductie, twee koelkasten", "Kookeiland van 2,6 m met de 3-groeps espressomachine, ook als bar",
              "Grote tafel van 4,2 m voor twaalf: lunch, samen werken, events", "Ronde bank rond de haard, open naar de tuin", "Boekenwand van 7,6 m met rolladder"],
             foto=12, cam=dict(t=[6.5, 4.2], afstand=11, hoek=210),
             prompt="Transform this empty room into the heart of a members club: an olive green kitchen along the back wall with a reclaimed wood island holding a three-group espresso machine, a 4 m long oak communal table for twelve along the glass facade, a round olive-green velvet sofa around a black freestanding fireplace, a walnut bookcase wall full of colourful books with a rolling ladder, big potted trees, the glass facade opening onto a wild courtyard garden."),
        zone("Bieb met focuskamers", "bieb", R(0.3, 8.2, 5.4, 12.4),
             "Geen ronde toren meer (die liet vier dode hoeken over), maar boekenwanden langs de muren en twee glazen focuskamers voor één of twee personen, met een leesstoel ertussen.",
             ["Boekenwanden van walnoot langs twee wanden", "Twee focuskamers van oude ramen, 2,2 x 1,9 m", "Leesstoel en leeslamp"],
             cam=dict(t=[2.8, 10.2], afstand=7, hoek=240),
             prompt="A small round reading room, 3.7 m in diameter, walls lined with walnut bookshelves all around, deep olive lime-wash, two olive velvet armchairs, butter-yellow throw, a brass reading lamp, a round skylight above, very calm."),
        zone("Werkzone met eilanden", "werken", R(13.6, 0.3, 26, 8.2),
             "Vierentwintig compacte zit-sta bureaus van 140 x 70 in zes eilanden van vier, elk een paar graden gedraaid, met looppaden van 1,1 m.",
             ["Zes eilanden van vier zit-sta bureaus 140 x 70, twee schermen per plek", "Looppad van 1,1 m tussen de rijen, 90 cm achter elke stoel",
              "Vilten baffles in rotskust-blauw, planten tussen de eilanden", "Samen met de grote tafel in het café: 36 werkplekken"],
             cam=dict(t=[19.8, 4.2], afstand=11, hoek=200),
             prompt="A compact but airy coworking room in a 1960s community building: six islands of four compact sit-stand desks (140 x 70 cm) with oak tops and black frames, each island rotated a few degrees, dual monitors, refurbished office chairs, slate-blue acoustic felt baffles, plants between the islands, clear 1.1 m walkways."),
        zone("Vergaderkamers", "vergader", R(26.2, 0.3, 36, 4.6),
             "Waar eerst de studio was: een vergaderkamer voor acht en een voor zes, met glas naar de gang en een scherm met camera.",
             ["Vergaderkamer voor 8 (21 m²) en voor 6 (19 m²)", "Tafel van 2,4 m, scherm met camera en microfoon", "Akoestische panelen in leisteenblauw"],
             cam=dict(t=[31, 2.4], afstand=8, hoek=200),
             prompt="Two small meeting rooms side by side behind black steel and glass walls: an oak table for eight and one for six, slate-blue acoustic wall panels, a screen with camera at the end wall, plants, warm light."),
        zone("Wastoren en techniek", "sanitair", R(26.2, 4.6, 36, 10),
             "De wastoren en de techniekruimte vormen de buffer tussen werken en sporten.",
             ["Wastoren van 5,5 m doorsnee met drie toiletten", "Techniek: warmtepomp, batterij, meterkast"],
             cam=dict(t=[29.2, 7.3], afstand=8, hoek=210),
             prompt="An octagonal concrete-look bathroom tower (eight flat faces, still reads as a round object), 5.5 m diameter and 3 m high, board-marked plaster walls, a V-shaped concrete wash trough with brass taps on the open side, toilet cabins hidden behind the V wall, ivy and pothos hanging over the top rim, daylight from a round skylight above."),
        zone("Gym (afsluitbaar)", "gym", [[26, 10], [36, 10], [36, 25.4], [34.5, 25.4], [27.2, 22.5], [27.2, 20.4], [26, 20.4]],
             "De achtervleugel wordt de gym: vier racks op platforms, roeiers bij het glas naar de tuin, een vloer voor groepslessen en yoga, de douchetoren in de hoek. Afgesloten met een deur op toegangspas.",
             ["Vier racks op zwevende platforms, 40 mm rubber op akoestische ondervloer", "Drie roeiers met uitzicht op de tuin",
              "Vloer van 4 x 3 m voor groepslessen en yoga", "Douchetoren van 4,5 m doorsnee", "Deur met toegangslezer, gym apart af te sluiten"],
             foto=10, cam=dict(t=[31, 17], afstand=12, hoek=230),
             prompt="Turn this wing into a functional strength gym: four black power racks on oak lifting platforms, anthracite rubber floor, one wall in oxblood red lime paint, rowing machines facing the garden, a mat area for classes, kettlebells on a steel rack, large green plants, glass doors opening to a wild garden."),
    ],
    elementen=[
        dict(t="kleed", c=[18.6, 11.0], r=1.6, kleur="#d5bd96"), *lockerwand([15.95, 12.3], 4.4, 45), *groenwand([22.3, 10.8], [19.0, 14.2], 3.0, rots=True), boom3([18.4, 13.6], "kentia"),
        pod2([19.8, 9.1]), pod2([21.6, 9.1]), pod2([23.4, 9.1]), pod2([32.9, 5.6]), pod2([25.6, 4.05]), *lockerwand([15.6, 8.55], 3.0, 0),
        dict(t="box", soort="bank", c=[25.1, 9.1], w=1.4, d=0.6, h=0.45, a=90, kleur="#5a3a22"),
        *kasten(0.6, 8.2, 0.55), *keuken([11.0, 0.65], 4.4), *kookeiland([11.0, 2.8]),
        *veelhoekbank([4.4, 4.3], 2.1, 6, open=(1, 4), draai=0), *grote_tafel([10.4, 6.5], 4.2),
        *tafeltje([1.2, 6.9]), boom3([7.6, 7.4], "ficus elastica"), plant3([0.9, 1.5], "strelitzia nicolai"), plant3([13.0, 7.7], "monstera"), hangplant([6.0, 2.0]), hangplant([8.6, 2.2]),
        dict(t="box", soort="fauteuil", c=[7.6, 1.7], w=0.85, d=0.85, h=0.8, a=20, kleur="#5a2741"),
        *kasten(0.6, 5.0, 12.15, h=2.4, d=0.3), *[dict(t="box", soort="kast", c=[0.55, v], w=1.0, d=0.3, h=2.4, a=90, kleur=WALNOOT) for v in (9.3, 10.3, 11.3)], *focuskamer([2.2, 9.35], 0), *focuskamer([4.5, 10.9], 90), dict(t="box", soort="fauteuil", c=[1.4, 11.3], w=0.8, d=0.8, h=0.8, a=0, kleur="#47522a"),
        *eiland2([15.6, 1.9], -4), *eiland2([19.6, 1.9], 3), *eiland2([23.6, 1.9], -3),
        *eiland2([15.6, 6.2], 4), *eiland2([19.6, 6.2], -3), *eiland2([23.6, 6.2], 5),
        plant3([13.95, 4.05], "zz-plant"), plant3([17.6, 4.05], "zz-plant"), plant3([21.6, 4.05], "zz-plant"), *[hangplant([u, v]) for u in (15.6, 19.6, 23.6) for v in (1.9, 6.2)],
        *vergaderkamer([28.7, 2.45], 4.8, 4.1, 0, 6), *stavergaderkamer([33.6, 2.45], 4.6, 4.1, 0, 6),
        *achthoektoren([29.2, 7.3], 2.75, 180, "was", lockers=(4,)), dict(t="box", soort="techniek", c=[34.7, 7.3], w=2.0, d=3.4, h=2.6, a=0, kleur="#8f8a80"),
        wand([[27.2, 10.0], [36, 10.0]], 3.5, gym=True), deur([26.7, 10.0], 0, toegang=True),
        *toren([33.4, 12.7], 2.25, 180, "douche"),
        *rack([34.8, 16.8], 90), *rack([34.8, 19.6], 90), *rack([34.8, 22.4], 90), *rack([30.2, 21.0], 0),
        roeier([27.3, 12.0], 90), roeier([27.3, 14.2], 90), roeier([27.3, 16.4], 90),
        dict(t="box", soort="halterrek", c=[30.2, 10.6], w=2.0, d=0.5, h=0.9, a=0, kleur=STAAL),
        dict(t="kleed", c=[30.6, 16.6], w=4.0, d=3.0, a=0, kleur="#c7928a"), plant3([27.8, 19.4], "strelitzia nicolai"), plant3([27.8, 11.0], "sansevieria"),
        label([30.6, 16.6], "groepsles en yoga"),
        *tafeltje([7.2, 10.4], stoelen=3), *tafeltje([10.4, 10.2], stoelen=3), *tafeltje([8.8, 12.8], stoelen=3),
        dict(t="boog", soort="bank", c=[19.0, 19.0], r=2.2, a0=200, a1=340, d=0.5, h=0.45, kleur=HOUT),
        dict(t="ring", soort="pergola", c=[19.0, 19.0], r=2.6, open=90, gat=0, h=2.6, kleur="#2f3032", dun=True),
        boom([3, 19]), boom([10, 20]), boom([24, 19]), boom([14, 18]), boom([3.4, 14.4], 0.9, 2.6), *pingpong([7.6, 16.6], 0),
    ],
)

# ---------------------------------------------------------------- Rietveldenweg v2
_RV_O = 39.2  # oostgevel loopt schuin: u = 39,2 - (v - 13,2) x 0,279
RIETVELDEN.update(
    concept="Achter de showroomramen het boekencafé met een grote tafel, de zitkuil in een halfronde boekenwand en een open keuken met kookeiland. "
            "Achter het café, rustig en weg van de straat, de werkzone met 24 bureaus, met daarnaast een stille werkkamer met belcellen. "
            "De gym zit in het oostelijke deel, achter een dichte wand met keuken en techniek als buffer naar het café, en een kleedruimte met 128 lockers als buffer naar "
            "de vergaderkamers. Achterin, waar het het stilst is, de bieb met twee focuskamers. Het platte dak boven het café kan een dakterras worden.",
    geluid="De gym ligt tegen de oostgevel. Naar het café zit er een keuken en techniekstrook van 4 m tussen, naar de vergaderkamers een kleedruimte van 3 m. "
           "De werkzone raakt de gym nergens. Dichte akoestische wanden tot het dak, deur op toegangspas, 40 mm rubber op akoestische ondervloer en platforms.",
    zones=[
        zone("Boekencafé achter de showroomramen", "café", R(7.3, 0.3, 19.8, 12.6),
             "Achter 11 meter showroomglas het café, zichtbaar vanaf de straat: een halfronde boekenwand om een achthoekige bank, leesplekken langs het glas, een grote tafel voor twaalf en een zitnis langs de blinde zuidwand. Strelitzia's staan aan het glas, kentia en ficus dieper in de zaal.",
             ["Halfronde boekenwand van 7,2 m doorsnee in walnoot", "Achthoekige bank in olijfgroen, open naar de ramen, rond een sfeerhaard",
              "Grote tafel van 4,2 m voor twaalf", "Zitnis van 4,2 m met drie tafeltjes langs de blinde wand", "Leesfauteuils en strelitzia's langs de ramen; houten vloer en zwarte plafonds blijven"],
             foto=5, cam=dict(t=[13.6, 6.2], afstand=13, hoek=200),
             prompt="Transform this former showroom into a members-club book café: keep the oak floor, black ceiling, grey columns and the natural stone wall. Add a semicircular freestanding walnut bookcase full of books wrapping an octagonal olive-green sofa with one open side around a black freestanding fireplace, a long oak communal table for twelve, a built-in bench with small tables along the blind side wall, plum velvet armchairs and bird-of-paradise plants along the big shop windows, a rubber fig tree, pothos hanging from the beams."),
        zone("Keuken en espresso-eiland", "café", R(19.8, 0.3, 23.8, 8.0),
             "Een open keuken van 6,6 m tegen de gymwand, met een kookeiland waar de espressomachine en de streepjeslijst staan.",
             ["Keuken van 6,6 m: twee vaatwassers, combi-stoomoven, inductie, twee koelkasten", "Kookeiland van 2,6 m met 3-groeps machine",
              "De natuurstenen balie wordt hergebruikt als blad van het eiland", "Dichte wand naar de gym in de rug"],
             foto=7, cam=dict(t=[21.6, 4.0], afstand=7, hoek=200),
             prompt="Keep the natural stone and turn this corner into an open members-club kitchen: a long olive green kitchen against the back wall with open shelves, a kitchen island clad in the existing natural stone with a travertine top and a polished three-group espresso machine, brass pendants, cognac leather stools, a chalkboard tally list."),
        zone("Techniek", "techniek", R(19.8, 8.0, 23.8, 12.6), "Warmtepomp, batterij, meterkast en opslag: buffer tussen café en gym.", []),
        zone("Gym (afsluitbaar)", "gym", [[24.0, 0.3], [42.5, 0.3], [41.6, 3.3], [39.3, 12.6], [24.0, 12.6]],
             "Het oostelijke deel wordt de gym: vijf racks langs de lange wand, een sledebaan van 12 m, roeiers en een D-vormige douchetoren met de rug tegen de wand naar de kleedruimte. Eigen deur op toegangspas.",
             ["Vijf racks op zwevende platforms", "Sledebaan van kunstgras van 12 m", "D-vormige douchetoren van 4,4 m breed tegen de wand: leidingen in de wand, geen dode strook erachter", "Kentia's en sansevieria in de hoeken",
              "40 mm rubber op akoestische ondervloer", "Dichte akoestische wanden tot het dak"],
             foto=9, cam=dict(t=[31, 6.4], afstand=14, hoek=200),
             prompt="Turn this large black-ceiling hall into a functional strength gym: five black power racks on oak platforms along the wall, a 12 m artificial turf sled track, anthracite rubber floor, rowing machines, one wall in oxblood red, a D-shaped concrete-look shower tower with its flat back against the wall and ivy on its rim, kentia palms in the corners."),
        zone("Kleedruimte en lockers", "sanitair", [[29.2, 12.8], [39.3, 12.8], [38.5, 15.8], [29.2, 15.8]],
             "Een lockerwand van 8 m en een bank tussen gym en vergaderkamers: buffer, omkleedruimte en de vaste locker van elke eigenaar.",
             ["Lockerwand van 8 m: 128 lockers, met pothos in een bak erbovenop", "Eiken bank van 6 m, haken", "Kentia bij de schuine gevel"]),
        zone("Vergaderkamers", "vergader", [[29.2, 15.8], [38.5, 15.8], [36.6, 22.6], [29.2, 22.6]],
             "Een vergaderkamer voor zes, een sta-kamer en een kamer voor vier, achter de kleedruimte. Een kamer voor acht is bij deze club niet nodig.",
             ["Vergaderkamer voor 6 (19 m²) en voor 4 (11 m²)", "Sta-vergaderkamer voor 5 met statafel en whiteboardwand (12 m²)", "Scherm met camera, akoestische panelen"], cam=dict(t=[33, 19.2], afstand=9, hoek=200),
             prompt="Three small meeting rooms behind black steel and glass in a hall with black ceilings: an oak table for six, a standing room with a round high table and a whiteboard wall, and a small room for four, slate-blue acoustic panels, a screen with camera, plants."),
        zone("Bieb met focuskamers", "bieb", [[29.2, 22.6], [36.6, 22.6], [35.4, 26.8], [29.2, 26.8]],
             "Geen ronde boekentoren meer (die liet dode hoeken over in deze schuine hoek), maar boekenkasten langs de schuine gevel, een leesstoel onder de lichtkoepel en twee glazen focuskamers voor één of twee personen tegen de achterwand.",
             ["Twee focuskamers van oude ramen, 2,2 x 1,9 m", "Boekenkasten van walnoot langs de schuine wand", "Leesstoel onder de lichtkoepel, zz-plant en aspidistra"],
             cam=dict(t=[32.2, 24.6], afstand=7, hoek=200),
             prompt="A quiet library corner in a hall with black ceilings: walnut bookshelves along a slanted wall, an olive armchair with a reading lamp under a round skylight, two small glass focus rooms made from reclaimed windows in oak frames, each with a desk and two stools, low-light plants."),
        zone("Wastoren", "sanitair", R(22, 13, 29.2, 19), "De wastoren midden in de hal, open naar de werkzone. Iets naar het noorden geschoven, zodat tussen toren en gymwand een looppad van 1,2 m vrij is van het café naar de kleedruimte en de gymdeur.", ["Wastrog langs de V, drie toiletten", "Looppad van 1,2 m langs de gymwand"],
             cam=dict(t=[25.6, 16], afstand=8, hoek=200),
             prompt="An octagonal concrete-look bathroom tower (eight flat faces, still reads as a round object), 5.5 m diameter and 3 m high, standing free in a black-ceiling hall, board-marked plaster, a V-shaped concrete wash trough with brass taps, ivy hanging over the top rim."),
        zone("Stille werkkamer", "werken", R(22, 19.2, 29.2, 25.8),
             "Achter glas: vier bureaus voor wie echt stil wil werken, en twee belcellen tegen de achterwand, zodat de doorloop naar bieb en focuskamers vrij blijft.",
             ["Eén eiland van vier bureaus", "Twee ronde belcellen tegen de achterwand", "Glazen wand naar de werkzone", "Pothos boven het eiland, zz-plant in de hoek"],
             foto=12, cam=dict(t=[25.6, 22.4], afstand=8, hoek=200),
             prompt="A quiet glass-walled work room in a hall with black ceiling: one island of four compact sit-stand desks, two round slate-blue felt phone booths, plants, soft warm light."),
        zone("Werkzone", "werken", R(7.3, 12.8, 22, 25.6),
             "Vierentwintig compacte zit-sta bureaus in zes eilanden, met een loungehoek en drie belcellen, rustig achter het café. De hal heeft hier geen ramen, dus komen er drie lichtkoepels boven de looppaden tussen de eilanden. Langs de blinde wand naar de woning een klimwand met pothos; kentia's en dracaena, die weinig licht nodig hebben, staan tussen de eilanden.",
             ["Zes eilanden van vier zit-sta bureaus 140 x 70", "Looppaden van 1,2 m", "Drie ronde belcellen en een loungebank",
              "Drie nieuwe lichtkoepels boven de werkzone", "Klimwand van 10 m langs de blinde wand, pothos boven elk eiland", "Totaal met grote tafel en stille kamer: 40 werkplekken"], foto=8, cam=dict(t=[14.6, 18.6], afstand=12, hoek=210),
             prompt="Turn this long hall with black walls and ceiling into a calm coworking space: six islands of four compact sit-stand desks with oak tops, each slightly rotated, dual monitors, three round slate-blue felt phone booths, a lounge sofa, slate-blue acoustic panels, a green wall of steel cables with pothos along the blind side wall, kentia palms between the islands, three round skylights, keep the wooden floor."),
        zone("Bedrijfswoning (verhuur)", "verhuur", R(0.1, 13.6, 7, 26), "Blijft woning, wordt verhuurd.", []),
    ],
    elementen=[
        dict(t="boog", soort="kast", c=[13.6, 6.2], r=3.6, a0=-80, a1=80, d=0.4, h=2.2, kleur=WALNOOT),
        *veelhoekbank([13.6, 6.2], 2.3, 8, open=(4,), draai=0), *grote_tafel([15.6, 11.3], 4.2),
        *[dict(t="box", soort="fauteuil", c=[8.2, v], w=0.85, d=0.85, h=0.8, a=0, kleur="#5a2741") for v in (2.4, 5.0, 9.6)],
        plant3([7.9, 3.7], "strelitzia nicolai"), boom3([8.0, 7.6], "strelitzia nicolai"), plant3([7.9, 11.6], "monstera"), boom3([10.6, 11.0], "ficus elastica"),
        *zitnis([15.4, 0.35], [19.6, 0.35]), *tafeltje([18.4, 4.6]), boom3([19.3, 7.6], "kentia"), hangplant([16.4, 1.4]), hangplant([18.6, 1.4]),
        hangplant([12.4, 11.3]), hangplant([18.8, 11.3]), hangplant([13.6, 6.2], 3.4), hangplant([21.4, 6.4]),
        *[dict(t="cil", soort="kolom", c=[8.7, v], r=0.2, h=4.6, kleur="#9a9890") for v in (3.0, 7.0, 11.0)],
        *keuken([23.45, 4.1], 6.6, 90), *kookeiland([21.4, 4.1], 90),
        dict(t="box", soort="techniek", c=[21.8, 10.3], w=3.6, d=4.2, h=2.6, a=0, kleur="#8f8a80"),
        wand([[24.0, 0.3], [24.0, 12.6]], 4.6, gym=True), wand([[24.0, 12.7], [30.0, 12.7]], 4.6, gym=True), wand([[31.0, 12.7], [39.3, 12.7]], 4.6, gym=True),
        deur([30.5, 12.7], 0, toegang=True),
        *rack([26.2, 1.6], 0), *rack([29.2, 1.6], 0), *rack([32.2, 1.6], 0), *rack([35.2, 1.6], 0), *rack([38.2, 1.6], 0),
        dict(t="box", soort="sledebaan", c=[31.0, 5.6], w=12, d=1.6, h=0.02, a=0, kleur="#5f7a3a"),
        roeier([26.4, 8.6], 0), roeier([26.4, 10.2], 0), roeier([26.4, 11.8], 0),
        dict(t="kleed", c=[30.0, 10.2], w=3.6, d=3.0, a=0, kleur="#c7928a"), *dtoren([37.0, 12.55], [32.6, 12.55], 0.6, "douche"),
        boom3([40.3, 2.4], "kentia"), boom3([38.6, 11.0], "kentia"), plant3([38.4, 8.0], "sansevieria"), plant3([24.7, 7.0], "zz-plant"), plant3([38.2, 14.0], "kentia"),
        *lockerwand([34.0, 15.45], 8.0, 0), dict(t="box", soort="bank", c=[34.0, 14.2], w=6.0, d=0.4, h=0.45, a=0, kleur=HOUT), hangplant([32.0, 14.0], 3.2), hangplant([36.0, 14.0], 3.2),
        *vergaderkamer([31.6, 17.95], 4.6, 4.1, 0, 6), *stavergaderkamer([31.6, 21.3], 4.6, 2.5, 180, 5), *vergaderkamer([35.3, 18.4], 4.6, 2.4, 90, 4),
        *focuskamer([30.4, 25.75], 180), *focuskamer([32.7, 25.75], 180),
        *[dict(t="box", soort="kast", c=[39.2 - (v - 13.2) * 0.279 - 0.45, v], w=0.95, d=0.3, h=2.4, a=106, kleur=WALNOOT) for v in (23.3, 24.3, 25.3)],
        dict(t="box", soort="fauteuil", c=[34.4, 23.4], w=0.8, d=0.8, h=0.8, a=200, kleur="#47522a"), plant3([34.6, 26.2], "zz-plant"), plant3([29.7, 23.2], "aspidistra"), plant3([35.8, 21.6], "zz-plant"),
        *achthoektoren([25.5, 16.4], 2.6, 180, "was"),
        wand([[22.0, 19.2], [22.0, 25.6]], 3.0, glas=True), wand([[22.0, 19.15], [27.0, 19.15]], 3.0, glas=True), deur([27.6, 19.15], 0),
        *eiland2([24.4, 21.6], 0), pod2([22.9, 24.8]), pod2([24.9, 24.9]), hangplant([24.4, 21.6]), plant3([26.6, 25.2], "zz-plant"),
        *eiland2([10.0, 14.9], -4), *eiland2([14.1, 14.9], 3), *eiland2([18.2, 14.9], -3),
        *eiland2([10.0, 19.2], 4), *eiland2([14.1, 19.2], -3), *eiland2([18.2, 19.2], 4),
        *[hangplant([u, v]) for u in (10.0, 14.1, 18.2) for v in (14.9, 19.2)],
        *groenwand([7.3, 23.3], [7.3, 13.2]),
        pod2([8.6, 24.4]), pod2([10.6, 24.6]), pod2([12.6, 24.4]),
        dict(t="box", soort="bank", c=[17.2, 24.5], w=2.6, d=0.9, h=0.75, a=0, kleur="#44606f"), *tafeltje([17.2, 23.0], stoelen=0),
        boom3([21.0, 23.6], "kentia"), boom3([14.8, 24.4], "kentia"), boom3([20.9, 13.7], "kentia"), hangplant([17.2, 23.0]), plant3([20.9, 17.0], "dracaena"), plant3([12.05, 17.05], "zz-plant"), plant3([16.15, 17.05], "zz-plant"),
        *tafeltje([3.0, 3.0], stoelen=3), *tafeltje([3.0, 6.6], stoelen=3), *tafeltje([3.0, 10.2], stoelen=3),
        *[dict(t="box", soort="plantenbak", c=[1.0, v], w=0.5, d=2.4, h=0.6, a=0, kleur="#5a3a22") for v in (2.4, 6.6, 10.8)],
        boom([-0.4, 1.5]), boom([-0.4, 12.0]), boom([5.6, 0.9], 0.9, 2.8), boom([5.6, 12.4], 0.9, 2.8),
    ],
)
RIETVELDEN["dak"]["koepels"] = [[25.5, 16.4, 0.9], [34.8, 10.6, 0.8], [32.0, 23.7, 0.7], [10.0, 17.05, 0.9], [14.1, 17.05, 0.9], [18.2, 17.05, 0.9]]
RIETVELDEN["dak"]["tekst"] += " Drie nieuwe lichtkoepels boven de werkzone, die verder geen ramen heeft."
RIETVELDEN["dak"]["tekst_en"] += " Three new round skylights above the work zone."

# ---------------------------------------------------------------- Eendenkooi v2
EENDENKOOI.update(
    concept="De gym hoeft niet gebouwd te worden: de sportzaal is er al, met eigen wanden en een deur op toegangspas. Bij de entree het boekencafé "
            "met de gebogen balie als espressobar, een keuken met kookeiland, een zeshoekige bank rond de haard en een boekenwand van 11 m met een zitnis. In de kleedkamers een lockerwand voor alle leden. "
            "Boven de hele verdieping als werkzone: 32 bureaus en een raambar met uitzicht over het groen, twee vergaderkamers voor zes, een sta-kamer, twee focuskamers en vijf belcellen. "
            "De verdieping ligt boven café en kleedkamers, niet boven de gym.",
    geluid="De sportzaal is een eigen bouwdeel van bijna 8 m hoog met een bestaande wand naar het café. De werkverdieping ligt boven café, studio en "
           "kleedkamers, niet boven de gym. Deur op toegangspas, rubber op akoestische ondervloer en platforms bij de racks.",
    zones=[
        zone("Gym in de sportzaal (afsluitbaar)", "gym", R(0.3, 0.3, 17.5, 18.1),
             "De bestaande sportzaal: zes racks langs de achterwand, een sledebaan van 15 m, een vloer voor groepslessen. Langs de blinde kopse wand achter de roeiers en naast de deur klimwanden van 4,5 m hoog. Eigen deur op toegangspas.",
             ["Zes racks op zwevende platforms", "Sledebaan van 15 m", "Groepslesvloer van 9 x 6 m", "Bokszakken blijven", "Klimwanden van staalkabel met pothos (11 m en 5 m), kentia in de hoeken", "Deur met toegangslezer"],
             foto=4, cam=dict(t=[9, 9], afstand=16, hoek=210),
             prompt="Transform this dark sports hall into a beautiful functional gym: six black power racks on oak platforms along the back wall, a 15 m artificial turf sled track, a mat area for classes, keep the punching bags, anthracite rubber floor, one wall in oxblood red, the rest warm white, a tall green wall of steel cables with pothos behind the rowing machines, kentia palms in big pots in the corners, warm industrial pendant lights."),
        zone("Boekencafé en keuken", "café", R(17.7, 0.3, 30.4, 10),
             "Bij binnenkomst de gebogen espressobar, daarachter een keuken van 5,6 m met kookeiland, een zeshoekige bank voor de ramen en een boekenwand van 11 m naar de studio met een zitnis ervoor. De ronde boekentoren is weg: die liet dode hoeken over en kostte zitplekken. Een strelitzia staat aan het glas, pothos hangt boven de raambar.",
             ["Gebogen balie als espressobar", "Keuken van 5,6 m met kookeiland", "Zeshoekige bank rond een sfeerhaard, open naar de ramen", "Raambar van 4,8 m met acht krukken voor lunch", "Tafel van 2,8 m voor acht bij de keuken", "Boekenwand van 11 m met een zitnis van 4,2 m en drie tafeltjes", "Strelitzia, monstera en kentia, pothos aan de balken"],
             foto=5, cam=dict(t=[24, 5], afstand=12, hoek=200),
             prompt="Transform this white gym reception into a warm book café: wrap the curved counter in reclaimed wood with a travertine top and a three-group espresso machine, an olive green kitchen with an island behind it, replace red walls with pistachio green lime-wash, a hexagonal olive green sofa with one open side around a black freestanding fireplace in front of the windows, an 11 m walnut bookcase wall with a built-in bench and small tables in front of it, a bird-of-paradise plant at the glass, pothos hanging above the window bar."),
        zone("Studio (bestaande dansstudio)", "studio", R(17.7, 10, 30.4, 16.9), "De dansstudio blijft, voor yoga en events, met planten in de hoeken.",
             ["Houten vloer blijft", "Vijgenpaarse gordijnen", "Kentia, monstera en philodendron"], foto=10, cam=dict(t=[24, 13.4], afstand=9, hoek=200),
             prompt="Keep this wooden-floor dance studio and make it warmer: fig-purple curtains, terracotta rug corner with cushions, plants on the window sills, warm dimmable light."),
        zone("Kleedkamers met V-wastrog", "sanitair", R(30.6, 0.3, 37.2, 14.6),
             "De kleedkamers blijven, met microcement en een V-vormige wastrog in het midden. Tegen de lange blinde wand een lockerwand van 5,6 m tussen de banken en een kortere bij de deur naar het café: de vaste locker van elke eigenaar en dagkluisjes voor sporters.",
             ["Microcement in plaats van tegels", "V-wastrog met messing kranen", "Lockerwanden van 5,6 en 2 m: 121 lockers met pothos erbovenop", "Aspidistra in de hoeken (verdraagt weinig licht en vocht)"],
             foto=11, cam=dict(t=[33.9, 7.4], afstand=8, hoek=200),
             prompt="Renovate this tiled changing room: replace all tiles with warm grey microcement and board-marked plaster, a V-shaped concrete wash trough with brass taps in the middle, oak benches and black hooks, a wall of dark green lockers with trailing pothos on top, ferns."),
        zone("Verdieping: werkzone", "werken", R(17.7, 0.3, 31.0, 14.6),
             "Acht eilanden van vier compacte zit-sta bureaus, haaks op de ramen zodat niemand tegen het licht in kijkt, en een raambar langs de ramen: 39 werkplekken met uitzicht over het water en het groen. Bij de trap twee belcellen, pothos hangt boven elk eiland.",
             ["Acht eilanden van vier bureaus 140 x 70, schermen haaks op het raam", "Raambar van 4,2 m met krukken", "Looppaden van 1,1 tot 1,4 m", "Twee belcellen bij de trap, een bij de raambar", "Ficus aan het raam, kentia en dracaena verderop"], foto=8, n=1,
             cam=dict(t=[24.4, 7.4], afstand=13, hoek=200),
             prompt="Turn this white space with columns and windows into a calm coworking floor: eight islands of four compact sit-stand desks with oak tops placed at right angles to the windows, dual monitors, a window bar with stools facing the green view, slate-blue acoustic baffles, round felt phone booths, pothos hanging above every island, a rubber fig at the window."),
        zone("Verdieping: vergaderkamers", "vergader", R(31.0, 0.3, 37.2, 14.6),
             "Twee vergaderkamers voor zes aan de ramen, een sta-kamer, en achter een gangetje twee focuskamers en twee belcellen. Een kamer voor acht is niet nodig.",
             ["Twee vergaderkamers voor 6 (22 en 21 m²)", "Sta-vergaderkamer voor 5 met statafel en whiteboardwand", "Twee focuskamers van oude ramen, 2,2 x 1,9 m", "Twee ronde belcellen"], n=1,
             cam=dict(t=[34.1, 7.0], afstand=9, hoek=200),
             prompt="Two meeting rooms behind black steel and glass on an upper floor, each with an oak table for six, a standing meeting room with a round high table and a whiteboard wall, two small glass focus rooms made from reclaimed windows, slate-blue acoustic panels, a screen with camera, plants, daylight from the windows."),
    ],
    elementen=[
        *rack([2.2, 16.6], 0), *rack([5.0, 16.6], 0), *rack([7.8, 16.6], 0), *rack([10.6, 16.6], 0), *rack([13.4, 16.6], 0), *rack([16.0, 16.6], 0),
        dict(t="box", soort="sledebaan", c=[8.6, 1.6], w=15, d=1.6, h=0.02, a=0, kleur="#5f7a3a"),
        roeier([1.4, 6.0], 90), roeier([1.4, 8.6], 90), roeier([1.4, 11.2], 90),
        *[dict(t="cil", soort="bokszak", c=[x, 9.0], r=0.2, h=1.2, z=1.0, kleur="#3a3b3d") for x in (10, 12, 14)],
        dict(t="kleed", c=[9.0, 9.4], w=9, d=6, a=0, kleur="#c7928a"), label([9.0, 7.0], "groepsles"),
        dict(t="box", soort="halterrek", c=[9.0, 13.9], w=4.0, d=0.6, h=0.9, a=0, kleur=STAAL),
        boom([1.6, 1.8], 1.2, 4.2), boom([16.0, 12.6], 1.2, 4.2), boom3([1.3, 14.2], "kentia"), plant3([16.9, 10.2], "sansevieria"),
        *groenwand([0.3, 14.0], [0.3, 3.0], 4.5), *groenwand([17.45, 2.6], [17.45, 7.6], 4.5),
        wand([[17.6, 0.3], [17.6, 7.9]], 7.8, gym=True, bestaand=True), wand([[17.6, 9.1], [17.6, 18.1]], 7.8, gym=True, bestaand=True),
        deur([17.6, 8.5], 90, toegang=True),
        dict(t="boog", soort="bar", c=[19.4, 3.4], r=1.9, a0=-90, a1=90, d=0.7, h=1.1, kleur=HOUT),
        *keuken([29.77, 3.6], 5.6, 90), *kookeiland([27.9, 3.6], 90),
        *veelhoekbank([24.4, 5.6], 2.0, 6, open=(4,), draai=30), *zitnis([22.6, 9.45], [18.4, 9.45]), *tafeltje([20.0, 6.6]),
        *kasten(18.4, 29.4, 9.7), *grote_tafel([27.75, 7.3], 2.8, 90), boom3([21.9, 1.1], "strelitzia nicolai"), plant3([23.2, 8.6], "kentia"), plant3([28.9, 1.0], "monstera"),
        hangplant([23.6, 0.9]), hangplant([26.6, 0.9]), hangplant([24.4, 5.6], 3.4), hangplant([19.0, 3.4]), hangplant([27.9, 3.6]),
        boom3([29.5, 16.0], "kentia"), plant3([29.8, 11.0], "philodendron"), plant3([20.4, 16.3], "monstera"),
        dict(t="box", soort="raambar", c=[25.2, 0.6], w=4.8, d=0.5, h=1.05, a=0, kleur=HOUT),
        dict(t="kleed", c=[24.0, 13.4], w=5, d=3, a=0, kleur="#b8633f"),
        dict(t="boog", soort="gordijn", c=[24.0, 16.2], r=5.6, a0=240, a1=300, d=0.08, h=3.2, kleur="#4b2339"),
        dict(t="v", c=[33.9, 7.4], arm=2.2, hoek=40, open=180, h=1.2),
        *[dict(t="box", soort="bank", c=[36.6, v], w=0.4, d=2.8, h=0.45, a=0, kleur=HOUT) for v in (2.95, 11.75)], *lockerwand([36.9, 7.35], 5.6, 90),
        plant3([36.9, 0.8], "aspidistra"), plant3([36.9, 14.0], "aspidistra"), *lockerwand([30.9, 11.4], 2.0, 90),
        *[dict(t="box", soort="douchewand", c=[31.6 + i * 1.4, 0.9], w=0.08, d=1.2, h=2.1, a=0, kleur="#c9c3b6") for i in range(4)],
        *[dict(t="box", soort="douchewand", c=[31.6 + i * 1.4, 13.9], w=0.08, d=1.2, h=2.1, a=0, kleur="#c9c3b6") for i in range(4)],
        dict(t="box", soort="trap", c=[18.8, 13.6], w=1.2, d=3.4, h=0.3, a=0, kleur="#cfc8ba"),
        dict(t="box", soort="trap", c=[18.8, 13.6], w=1.2, d=3.4, h=0.3, a=0, kleur="#cfc8ba", n=1),
        dict(t="box", soort="raambar", c=[24.4, 0.7], w=4.2, d=0.5, h=1.05, a=0, kleur=HOUT, n=1),
        *[e for u, v, a in ((20.2, 3.4, 87), (24.5, 3.4, 93), (28.8, 3.4, 87), (20.2, 7.6, 93), (24.5, 7.6, 87), (28.8, 7.6, 93), (24.5, 11.8, 93), (28.8, 11.8, 87))
          for e in eiland2([u, v], a, 1)],
        *[hangplant([u, v], 2.8, 1) for u, v in ((20.2, 3.4), (24.5, 3.4), (28.8, 3.4), (20.2, 7.6), (24.5, 7.6), (28.8, 7.6), (24.5, 11.8), (28.8, 11.8), (23.2, 0.8), (25.6, 0.8))],
        boom3([18.6, 5.5], "kentia", 1), boom3([18.6, 1.0], "ficus elastica", 1), plant3([30.7, 9.7], "dracaena", n=1),
        *vergaderkamer([34.1, 2.3], 5.8, 3.8, 0, 6, 1), *vergaderkamer([34.1, 6.15], 5.8, 3.6, 0, 6, 1), *stavergaderkamer([33.0, 9.7], 4.0, 3.2, 180, 5, 1),
        pod2([36.2, 10.4], 1), plant3([36.3, 8.7], "zz-plant", n=1),
        *focuskamer([32.2, 13.6], 180, 1), *focuskamer([34.5, 13.6], 180, 1), pod2([36.4, 13.7], 1),
        pod2([30.3, 1.1], 1), pod2([21.3, 13.8], 1), pod2([21.3, 12.2], 1),
        boom([3, -5], 1.6, 6), boom([12, -6], 1.6, 6), boom([24, -5.4], 1.6, 6), boom([34, -6], 1.6, 6),
    ],
)

# ---------------------------------------------------------------- Voorhout v2
_A2 = [[22.9, 0.1], [30.1, 0.1], [30.1, 8.5], [24.8, 8.5], [24.8, 7.5], [22.9, 7.5]]
_BW = [[11.8, -4.8], [20.7, -4.8], [20.7, -10.4], [14.8, -10.4], [12.6, -10.4], [12.6, -7.6], [11.8, -7.6]]
VOORHOUT.update(
    niveaus={"1": 3.3},
    concept="De tuinstraat tussen de twee werkplaatsen is de ontvangst. Werkplaats A wordt café en werken: het café met keuken en kookeiland aan de straatkant, "
            "dan een dubbele boekenkast, dan de werkzone met drie eilanden en een grote tafel voor twaalf. Het hoge deel krijgt de wastoren en op de entresol "
            "een werkzolder met twaalf bureaus. Werkplaats B is helemaal sport: de gym, met kleedruimte en techniek als buffer, en boven een vergaderkamer. "
            "Sporten en werken zitten zo in twee aparte gebouwen.",
    geluid="Gym en werken zitten in twee aparte gebouwen met de tuinstraat ertussen: de beste scheiding van alle panden. Gebouw B gaat apart op slot met een "
           "deur op toegangspas; binnen B zit de kleedruimte als buffer tussen gym en vergaderkamer.",
    zones=[
        zone("Boekencafé en keuken", "café", R(0.3, 0.3, 10.4, 7.3),
             "De oudste werkplaats: ronde bank rond de haard aan de straatkant, een keuken van 5,6 m langs de achterwand met een kookeiland en de espressomachine, en een dubbele boekenkast als scheiding met de werkzone.",
             ["Keuken van 5,6 m met twee vaatwassers, combi-stoomoven, inductie", "Kookeiland met 3-groeps machine",
              "Ronde bank van 3,6 m doorsnee", "Dubbele boekenkast van 4 m als scheiding", "Blauwe kozijnen in diep olijf gelakt"],
             foto=6, cam=dict(t=[5.2, 3.8], afstand=9, hoek=210),
             prompt="Transform this long low workshop with blue glazed facade into the book café of a members club: keep the long glass facade and the low roof, repaint the blue frames deep olive green. Inside: a round olive-green velvet sofa around a black freestanding fireplace, an olive green kitchen against the back wall, a reclaimed wood kitchen island with a three-group espresso machine, a double-sided walnut bookcase dividing the space, plants and small trees."),
        zone("Werkzone in A", "werken", R(10.6, 0.3, 22.6, 7.3),
             "Twaalf compacte zit-sta bureaus in drie eilanden langs het glas, een grote tafel voor twaalf en twee belcellen.",
             ["Drie eilanden van vier bureaus 140 x 70", "Grote tafel van 4,2 m voor twaalf", "Twee ronde belcellen", "Looppad van 1,2 m"],
             foto=7, cam=dict(t=[16.6, 3.8], afstand=9, hoek=210),
             prompt="Turn this long workshop with a glass facade into a compact coworking room: three islands of four compact sit-stand desks with oak tops along the glass, a long oak communal table for twelve, two round slate-blue felt phone booths, slate-blue acoustic panels between the timber trusses, plants along the glass."),
        zone("Wastoren en entree", "sanitair", _A2,
             "Het hoge deel van A: de voordeur aan de tuinstraat, de wastoren met drie toiletten en de trap naar de werkzolder.",
             ["Wastoren van 5,5 m doorsnee onder de entresol", "Kapstok en kluisjes bij de deur", "Stalen trap naar boven"],
             foto=5, cam=dict(t=[26.4, 4.2], afstand=8, hoek=220),
             prompt="Turn this high workshop part with glazed doors into the entrance of a members club with a octagonal concrete-look bathroom tower standing in the space: board-marked plaster, a V-shaped wash trough with brass taps, black steel and glass doors, a black steel stair to a mezzanine, lockers in old school furniture, olive trees in clay pots."),
        zone("Werkzolder op de entresol", "werken", _A2,
             "Op de bestaande entresol: drie eilanden van vier bureaus, licht van boven.", ["Twaalf bureaus 140 x 70", "Stalen balustrade met plantenbak"], n=1,
             cam=dict(t=[26.4, 4.2], afstand=8, hoek=220),
             prompt="A mezzanine work loft in a high old workshop: three islands of four compact sit-stand desks with oak tops, lamps, a black steel balustrade with planters, timber roof trusses, skylights."),
        zone("Gym in gebouw B (afsluitbaar)", "gym", R(20.9, -15.2, 33.4, -4.8),
             "De machinale werkplaats van B wordt de gym: vier racks, roeiers bij het glas, een vrije vloer en de douchetoren. Gebouw B gaat apart op slot.",
             ["Vier racks op zwevende platforms", "Drie roeiers bij het glas", "Douchetoren van 4,3 m doorsnee", "Deur met toegangslezer"],
             foto=10, cam=dict(t=[27, -10], afstand=10, hoek=210),
             prompt="Turn this brick workshop with large blue-framed windows into a functional gym: four black power racks on oak platforms, rowing machines facing the windows, anthracite rubber floor, one wall in oxblood red, a round concrete-look shower tower with plants on its rim in the corner, big plants. Repaint the blue frames black."),
        zone("Kleedruimte en techniek", "techniek", _BW, "Lockers, banken en fietsen: buffer tussen gym en vergaderkamer.", ["60 lockers, banken"]),
        zone("Techniek en fietsen", "techniek", R(15, -16.5, 20.6, -10.6), "Warmtepomp, batterij, fietsen.", []),
        zone("Vergaderkamers boven in B", "vergader", _BW,
             "Op de verdieping van B (nu kantoor en kantine): een vergaderkamer voor acht, een voor vier en een belcel.", ["Vergaderkamer voor 8 en voor 4", "Eén belcel"], n=1,
             cam=dict(t=[16.2, -7.6], afstand=7, hoek=210),
             prompt="A meeting room for eight on the upper floor of an old brick workshop: an oak table, slate-blue acoustic panels, a screen with camera, timber roof, plants."),
    ],
    elementen=[
        *zitkuil([2.6, 3.8], 1.8, 270, "#6f7d3a", "#d9ccb0"), *keuken([7.4, 6.97], 5.6), *kookeiland([7.4, 4.6]),
        *kasten(0.8, 4.8, 10.5, a=90, d=0.5, h=2.2), *tafeltje([6.0, 1.6]), *tafeltje([8.8, 1.6]),
        plant([4.9, 1.0]), dict(t="box", soort="fauteuil", c=[0.9, 6.6], w=0.85, d=0.85, h=0.8, a=30, kleur="#5a2741"),
        *eiland2([12.8, 2.0], -3), *eiland2([16.7, 2.0], 4), *eiland2([20.6, 2.0], -3),
        *grote_tafel([16.6, 5.6], 4.2), pod2([11.8, 5.6]), pod2([21.6, 5.6]),
        *toren([26.3, 4.4], 2.75, 180, "was"), dict(t="box", soort="trap", c=[29.6, 5.6], w=0.9, d=3.4, h=0.3, a=0, kleur="#cfc8ba"),
        dict(t="box", soort="kluisjes", c=[25.4, 0.45], w=3.0, d=0.5, h=2.0, a=0, kleur="#6e4f38"),
        *eiland2([24.9, 2.2], -3, 1), *eiland2([28.4, 2.2], 3, 1), *eiland2([25.6, 6.0], 4, 1), plant([29.6, 7.8], 0.4, 1.2, 1),
        *rack([32.4, -13.6], 90), *rack([32.4, -11.0], 90), *rack([25.0, -14.2], 0), *rack([27.8, -14.2], 0),
        roeier([23.0, -6.0], 0), roeier([25.6, -6.0], 0), roeier([28.2, -6.0], 0),
        dict(t="kleed", c=[25.6, -10.0], w=5, d=3.2, a=0, kleur="#c7928a"), *toren([31.2, -7.0], 2.15, 180, "douche"),
        wand([[20.85, -15.4], [20.85, -6.9]], 5.8, gym=True), wand([[20.85, -5.7], [20.85, -4.6]], 5.8, gym=True), deur([20.85, -6.3], 90, toegang=True),
        dict(t="box", soort="kluisjes", c=[16.2, -5.3], w=4.0, d=0.5, h=2.0, a=0, kleur="#6e4f38"),
        dict(t="box", soort="bank", c=[16.2, -6.6], w=3.0, d=0.4, h=0.45, a=0, kleur=HOUT),
        dict(t="box", soort="fietsenrek", c=[13.4, -8.6], w=2.4, d=0.6, h=0.9, a=90, kleur=STAAL),
        dict(t="box", soort="techniek", c=[17.8, -13.6], w=4.4, d=4.6, h=2.4, a=0, kleur="#8f8a80"),
        *vergaderkamer([15.6, -7.6], 4.6, 4.4, 0, 8, 1), *vergaderkamer([19.3, -7.6], 3.4, 2.6, 90, 4, 1), pod2([12.8, -5.6], 1),
        *[boom([u, -2.4], 0.9, 3.0) for u in (3.5, 12.5, 21.5, 30.0)],
        dict(t="box", soort="buitentafel", c=[8.0, -2.4], w=4.0, d=0.9, h=0.75, a=0, kleur=HOUT),
        *[dict(t="box", soort="bank", c=[x, -3.6], w=2.0, d=0.5, h=0.45, a=0, kleur=HOUT) for x in (16.6, 26.0)],
        *[dict(t="box", soort="plantenbak", c=[x, -0.9], w=2.4, d=0.5, h=0.6, a=0, kleur="#5a3a22") for x in (6, 10, 15, 19)],
        dict(t="box", soort="fietsenrek", c=[35.0, -2.4], w=4, d=0.6, h=0.9, a=90, kleur=STAAL),
    ],
)
VOORHOUT["dak"]["koepels"] = [[14.8, 3.8, 0.7], [18.6, 3.8, 0.7], [27.0, -10.0, 0.8]]

# ---------------------------------------------------------------- Maarssen v2
MAARSSEN.update(
    concept="Het voorhuis uit 1931 wordt boekencafé met de keuken: een kookeiland, een grote tafel voor tien en een ronde bank in de ronde erker. De bieb komt op zolder. "
            "In de hal uit 1970 zit de gym aan de westkant achter een dichte wand tot het dak, met de douchetoren als D tegen die wand. Daarnaast een bufferstrook met een vergaderkamer voor zes, "
            "een sta-kamer, de belcellen, de wastoren, twee focuskamers en de lockers, met daarboven een vergaderbalkon op een tussenvloer, en aan de oostkant, bij de glazen deuren naar de weilanden, "
            "de werkzone met twintig bureaus en een raambar.",
    geluid="De hal is één ruimte van 7 m hoog, dus de gym krijgt een dichte akoestische wand tot het dak. Tussen gym en werkzone zit een strook van 5,6 m met "
           "vergaderkamers, belcellen, de wastoren en de lockers. De douchetoren staat in de gym tegen de wand, dus de gymwand heeft geen opening meer en de toren dempt "
           "naar de focuskamers erachter. Gym met eigen deur op toegangspas naar de binnenplaats.",
    zones=[
        zone("Boekencafé en keuken in het voorhuis", "café", [[0.3, 0.3], [11.6, 0.3], [11.6, 2.9], [12.4, 2.9], [14.4, 5.0], [14.5, 7.0], [12.0, 9.1], [5.1, 9.1], [5.1, 11.7], [2.8, 11.7], [2.8, 7.7], [0.3, 7.7]],
             "Het woonhuis uit 1931: keuken langs de zijmuur met een kookeiland, een grote tafel voor tien in het midden en een ronde bank in de ronde erker (hier past rond beter dan een veelhoek). Een ficus in de achteruitbouw, strelitzia bij de tuindeuren, pothos boven de tafel.",
             ["Keuken van 6,4 m met kookeiland en 3-groeps machine", "Grote tafel van 3,5 m voor tien", "Ronde bank die de ronde erker volgt",
              "Originele details uit 1931 blijven", "Glazen tuindeuren naar de binnenplaats"], cam=dict(t=[7, 4.8], afstand=9, hoek=210),
             prompt="A 1930s Dutch brick house turned into the book café of a members club: an olive green kitchen along the side wall with a reclaimed wood island and a three-group espresso machine, a long oak table for ten, a curved olive-green velvet sofa following a round bay window around a black freestanding fireplace, original 1930s doors and mouldings, glass garden doors, plants."),
        zone("Stille bieb op zolder", "bieb", R(0.6, 0.6, 11.4, 7.4),
             "Onder de kap: de stille bieb met lage kasten, fauteuils en dakramen.", ["Lage boekenkasten onder de schuine kap", "Fauteuils in olijf", "Zz-plant en sansevieria (weinig licht nodig)"], n=1,
             cam=dict(t=[6, 4], afstand=8, hoek=210),
             prompt="A quiet attic library under a pitched roof with exposed timber rafters: low walnut bookcases under the slopes, deep olive walls, olive velvet armchairs, butter-yellow lamps, roof windows."),
        zone("Gym (afsluitbaar)", "gym", R(-14.6, 16.4, -6.8, 35.7),
             "De westkant van de hal: vier racks langs de lange wand, roeiers bij het glas, een vloer voor groepslessen en yoga in het midden en een D-vormige douchetoren met de rug tegen de gymwand. Dichte wand tot het dak zonder opening, eigen deur op toegangspas.",
             ["Vier racks op zwevende platforms", "Groepslesvloer van 5 x 4,6 m", "D-vormige douchetoren met vier douches tegen de gymwand, alleen vanuit de gym", "Klimwand met pothos langs de kopse wand, kentia en strelitzia",
              "Deur met toegangslezer naar de binnenplaats"],
             cam=dict(t=[-10.6, 26], afstand=12, hoek=210),
             prompt="A functional gym inside a 7 m high 1970s steel hall, closed off by a solid wall: four black power racks on oak platforms along the long wall, rowing machines, a mat area for classes, a D-shaped concrete-look shower tower against the wall with ivy on its rim, anthracite rubber floor, one wall oxblood red, a green wall of steel cables with pothos, kentia palms, daylight from high windows."),
        zone("Vergaderkamers en belcellen", "vergader", R(-6.6, 16.4, -1.0, 23.2),
             "In de bufferstrook aan het glas: een vergaderkamer voor zes en een sta-kamer voor vier, met twee belcellen erachter. Waar eerst een kamer voor acht stond.",
             ["Vergaderkamer voor 6 (12 m²)", "Sta-vergaderkamer voor 4 met statafel en whiteboardwand (8 m²)", "Twee ronde belcellen"],
             cam=dict(t=[-3.8, 19.6], afstand=8, hoek=210),
             prompt="Inside a high steel hall, behind black steel and glass: a meeting room with an oak table for six and next to it a small standing meeting room with a round high table and a whiteboard wall, slate-blue acoustic panels, a screen with camera, two round felt phone booths behind them."),
        dict(zone("Vergaderbalkon op de tussenvloer", "vergader", R(-6.6, 16.4, -1.0, 23.2),
             "Boven de vergaderkamers een nieuwe tussenvloer van 38 m² in de 7 m hoge hal: een tweede vergaderkamer voor zes en drie belcellen, met een glazen balustrade naar de werkzone waar pothos overheen hangt. De rest van de hal blijft hoog en open.",
             ["Tussenvloer staal en hout op 3 m, stalen trap langs de gymwand", "Vergaderkamer voor 6 en drie belcellen", "Glazen balustrade met hangende pothos: licht en zicht blijven"], n=1,
             cam=dict(t=[-3.8, 19.8], afstand=8, hoek=20),
             prompt="A steel and timber mezzanine inside a 7 m high 1970s hall: on top a glass-walled meeting room for six and three round felt phone booths behind a glass balustrade with trailing pothos, a black steel stair along the wall, below it a meeting room for eight, the rest of the hall stays high, open and full of daylight."), tussenvloer=True),
        zone("Wastoren", "sanitair", R(-6.6, 23.2, -1.0, 30.9),
             "De wastoren in de bufferstrook, open naar het looppad tussen twee bureau-eilanden. Op de zijde naar de belcellen een lockerkast. De douchetoren staat nu in de gym, zodat de gymwand helemaal dicht kan tot het dak.",
             ["Wastoren 5,5 m met drie toiletten en V-wastrog", "Lockerkast op de buitenzijde: 30 lockers"],
             cam=dict(t=[-3.8, 28.3], afstand=9, hoek=210),
             prompt="An octagonal concrete-look bathroom tower (flat faces, it still reads as a round object), 3 m high, standing in a high steel hall, board-marked plaster, a V-shaped concrete wash trough with brass taps, ivy and ferns in planters along the top rim, a locker wall built into one outer face, a skylight above."),
        zone("Focuskamers en lockers", "werken", R(-6.6, 30.9, -1.0, 35.7),
             "Waar eerst de douchetoren stond: twee glazen focuskamers voor één of twee personen en een lockerwand van 4,6 m. Aan de andere kant van de dichte gymwand staat de douchetoren als buffer.",
             ["Twee focuskamers van oude ramen, 2,2 x 1,9 m", "Lockerwand van 4,6 m: 73 lockers, pothos erbovenop", "Aspidistra in de hoek"],
             cam=dict(t=[-3.4, 33.3], afstand=7, hoek=210),
             prompt="In a high steel hall: two small glass focus rooms made from reclaimed windows in oak frames, each with a desk and two stools, opposite a wall of dark green lockers with trailing pothos on top, warm light, concrete floor."),
        zone("Werkzone in de hal", "werken", R(-1.0, 16.4, 4.8, 35.7),
             "Twintig compacte zit-sta bureaus in vijf eilanden en een raambar van 6 m langs de glazen deuren met uitzicht op de weilanden. Tegenover de wastoren is het looppad tussen twee eilanden 1,4 m breed.",
             ["Vijf eilanden van vier bureaus 140 x 70", "Raambar van 6 m met tien krukken", "Met de grote tafel in het voorhuis: 40 werkplekken", "Strelitzia en ficus in de lichte hoeken, monstera aan het glas, pothos boven elk eiland"],
             cam=dict(t=[1.8, 26], afstand=10, hoek=210),
             prompt="A coworking strip inside a high 1970s hall: five islands of four compact sit-stand desks with oak tops, a long window bar with stools facing big glass doors and green meadows, slate-blue acoustic baffles hanging high, a bird-of-paradise and a rubber fig in the bright corners, pothos hanging above the islands."),
        zone("Fietsen en techniek", "techniek", R(5.1, 32.4, 12.6, 35.9), "Fietsen, warmtepomp, batterij en opslag.", []),
    ],
    elementen=[
        *zitkuil([11.6, 6.0], 1.9, 180, "#6f7d3a", "#d9ccb0"), *keuken([0.73, 3.9], 6.4, 90), *kookeiland([2.9, 3.9], 90),
        *grote_tafel([6.6, 4.0], 3.5, 90), plant3([10.8, 1.0], "kentia"), plant3([6.2, 8.4], "monstera"), *tafeltje([9.2, 1.4]),
        boom3([3.9, 10.6], "ficus elastica"), plant3([12.3, 8.4], "strelitzia nicolai"), hangplant([6.6, 2.8]), hangplant([6.6, 5.2]), hangplant([2.9, 3.9]), hangplant([11.6, 6.0], 2.6),
        *kasten(1.0, 10.0, 1.0, d=0.4, h=1.1, n=1), *kasten(1.0, 10.0, 6.8, d=0.4, h=1.1, n=1),
        plant3([10.8, 2.2], "zz-plant", n=1), plant3([1.2, 4.0], "sansevieria", n=1), plant3([10.8, 5.8], "zz-plant", n=1),
        *[dict(t="box", soort="fauteuil", c=[u, 4.0], w=0.85, d=0.85, h=0.8, a=0, kleur="#47522a", n=1) for u in (3.0, 6.0, 9.0)],
        *rack([-13.8, 19.4], 90), *rack([-13.8, 22.4], 90), *rack([-13.8, 25.4], 90), *rack([-13.8, 28.4], 90),
        roeier([-8.4, 17.6], 0), roeier([-8.4, 19.2], 0),
        dict(t="kleed", c=[-9.8, 24.4], w=4.6, d=5.0, a=0, kleur="#c7928a"), label([-9.8, 22.6], "groepsles en yoga"),
        boom3([-12.2, 32.4], "kentia"), plant3([-7.4, 28.6], "sansevieria"), plant3([-13.8, 17.1], "strelitzia nicolai"), *groenwand([-10.2, 35.55], [-14.4, 35.55], 4.0),
        wand([[-6.7, 16.0], [-6.7, 36.0]], 7.0, gym=True), deur([-10.6, 16.0], 0, toegang=True),
        *dtoren([-6.8, 30.2], [-6.8, 35.2], 0.3, "douche"),
        *vergaderkamer([-4.85, 18.55], 3.9, 3.2, 90, 6), *stavergaderkamer([-2.15, 18.55], 3.9, 2.1, 270, 4), pod2([-3.9, 22.3]), pod2([-2.1, 22.3]),
        dict(t="box", soort="trap", c=[-6.1, 21.9], w=0.9, d=2.6, h=0.3, a=0, kleur="#2f3032"),
        *vergaderkamer([-3.8, 18.7], 5.4, 4.2, 0, 6, 1), pod2([-4.95, 22.3], 1), pod2([-3.45, 22.3], 1), pod2([-1.85, 22.3], 1),
        wand([[-1.0, 16.4], [-1.0, 23.2]], 1.1, glas=True, n=1), *[hangplant([-0.85, v], 0.9, 1) for v in (17.4, 19.6, 21.8)],
        *achthoektoren([-3.8, 28.3], 2.75, 0, "was", lockers=(6,)),
        *focuskamer([-5.6, 32.05], 90), *focuskamer([-5.6, 34.4], 90), *lockerwand([-1.6, 33.3], 4.6, 90), plant3([-3.0, 35.2], "aspidistra"),
        *[e for v in (18.6, 22.4, 26.2, 30.4, 34.2) for e in eiland2([0.9, v], 90 + (3 if int(v) % 2 else -3))],
        *[hangplant([0.9, v]) for v in (18.6, 22.4, 26.2, 30.4, 34.2)],
        dict(t="box", soort="raambar", c=[4.5, 26.0], w=6.0, d=0.5, h=1.05, a=90, kleur=HOUT), boom3([4.0, 17.4], "strelitzia nicolai"), boom3([4.0, 34.6], "ficus elastica"),
        plant3([4.3, 21.6], "monstera"), plant3([4.3, 30.4], "monstera"), hangplant([4.5, 24.0]), hangplant([4.5, 28.0]), plant3([-1.6, 24.4], "zz-plant"),
        dict(t="box", soort="fietsenrek", c=[9.0, 34.2], w=5, d=0.6, h=0.9, a=0, kleur=STAAL),
        *tafeltje([-1.6, 14.0], stoelen=3), *tafeltje([2.2, 14.0], stoelen=3), boom([-3.6, 14.4], 0.8, 2.8),
        dict(t="ring", soort="pergola", c=[17.6, 20.0], r=2.6, open=90, gat=0, h=2.6, kleur="#2f3032", dun=True),
        dict(t="boog", soort="bank", c=[17.6, 20.0], r=2.2, a0=200, a1=340, d=0.5, h=0.45, kleur=HOUT),
        *tafeltje([17.0, 5.0], stoelen=3), *tafeltje([18.6, 9.0], stoelen=3),
        boom([19.8, 0.0]), boom([20.2, 14.0]), boom([19.6, 28.0]), boom([16.0, 33.6], 0.9, 3.0), boom([-3.6, -2.6]), boom([13.0, -2.6]),
    ],
)
MAARSSEN["dak"]["koepels"] = [[-3.8, 26.6, 0.9], [-3.8, 33.0, 0.8]]

LABELS.update({
    "utrecht-van-heutszstraat-4": {"Boekencafé en keuken": [5.0, 7.45], "Stille bieb in de boekentoren": [2.8, 13.3], "Werkzone met eilanden": [19.6, 4.05],
                                   "Wastoren en techniek": [29.2, 9.4], "Gym (afsluitbaar)": [31.4, 18.9], "Vergaderkamers": [31.1, 4.9], "Entree in de punt": [18.4, 12.2]},
    "den-bosch-rietveldenweg-13": {"Boekencafé achter de showroomramen": [11.2, 11.7], "Gym (afsluitbaar)": [30.4, 7.2], "Werkzone": [14.1, 22.6],
                                   "Keuken en espresso-eiland": [21.8, 7.4], "Bieb met focuskamers": [32.4, 23.7], "Techniek": [21.8, 12.1], "Kleedruimte en lockers": [34.0, 13.4],
                                   "Vergaderkamers": [33.6, 16.3], "Stille werkkamer": [25.2, 23.65], "Wastoren": [25.6, 18.4]},
    "den-bosch-eendenkooi-1a": {"Gym in de sportzaal (afsluitbaar)": [9.0, 4.4], "Boekencafé en keuken": [24.6, 9.0], "Kleedkamers met V-wastrog": [33.9, 11.4],
                                "Verdieping: werkzone": [24.0, 6.1], "Verdieping: vergaderkamers": [33.6, 12.0]},
    "voorhout-dinsdagse-wetering-56a": {"Boekencafé en keuken": [3.0, 6.6], "Werkzone in A": [16.6, 3.8], "Wastoren en entree": [26.4, 0.8],
                                        "Gym in gebouw B (afsluitbaar)": [26.4, -12.2], "Kleedruimte en techniek": [16.2, -8.4], "Techniek en fietsen": [17.8, -15.8],
                                        "Werkzolder op de entresol": [26.4, 4.2], "Vergaderkamers boven in B": [16.0, -10.0]},
    "maarssen-herenweg-15": {"Boekencafé en keuken in het voorhuis": [6.6, 7.4], "Gym (afsluitbaar)": [-10.4, 29.0], "Werkzone in de hal": [2.0, 36.6],
                             "Vergaderkamers en belcellen": [-3.8, 24.2], "Vergaderbalkon op de tussenvloer": [-3.8, 21.2], "Wastoren": [-3.8, 26.9], "Focuskamers en lockers": [-3.3, 33.2],
                             "Fietsen en techniek": [8.8, 33.2], "Stille bieb op zolder": [6.0, 4.0]},
})


# ---------------------------------------------------------------- Ronde 6: Pernis (circa 60) en Uden (circa 100)
PERNIS = dict(
    titel="Ring 15, Pernis (Rotterdam)",
    sub="Dorpspand uit circa 1900 met bijeenkomstfunctie, 445 m² grondvlak en 6,7 m hoog, met een tuin op het zuiden",
    hoogte=6.7, niveaus={"1": 3.2},
    concept="Een lang, hoog dorpsgebouw aan de Ring van Pernis. Aan de westkant het boekencafé met keuken, grote tafel en een achthoekige bank. In het midden de werkzone "
            "met 24 bureaus haaks op de tuinramen; boven de noordhelft van de werkzone een vergaderbalkon op een nieuwe tussenvloer, zodat de zuidhelft hoog en licht blijft. "
            "Dan een bufferstrook met de wastoren als D tegen de noordwand, twee focuskamers, belcellen en de lockerwand, en aan de oostkant de gym achter een dichte wand. "
            "Buiten een terras en tuin over de hele lengte.",
    geluid="Gym aan de oostkant, achter de bufferstrook: 7 m tussen werkzone en gym, de lockerwand tegen de dichte gymwand en aan de gymkant de douchetoren tegen diezelfde wand. "
           "Dichte wand tot het dak met deur op toegangspas. Vergaderkamers zitten boven de werkzone, ver van de gym. 40 mm rubber op akoestische ondervloer en platforms onder de racks.",
    pui=[[[1, 0], [24, 0]], [[33, 0], [41.5, 0]]],
    zones=[
        zone("Boekencafé en keuken", "café", R(0.3, 0.3, 11, 10.3),
             "Aan de westkant het café: keuken langs de noordwand, kookeiland met de espressomachine, een grote tafel voor twaalf en een achthoekige bank rond de haard, open naar de tuinramen. Strelitzia's aan het glas, een kentia in de hoek bij de keuken.",
             ["Keuken van 5,4 m met kookeiland", "Grote tafel van 4,2 m voor twaalf", "Achthoekige bank rond een sfeerhaard, open naar de tuin", "Boekenwand langs de westgevel", "Pothos aan de spanten boven tafel en bank"],
             cam=dict(t=[5.6, 5.2], afstand=9, hoek=230),
             prompt="An old Dutch village meeting hall, about 6.7 m high with exposed roof trusses, turned into a members-club book café: an olive green kitchen with a reclaimed wood island and a three-group espresso machine, a long oak table for twelve, an octagonal olive green sofa with one open side around a black freestanding fireplace by the garden windows, a walnut bookcase wall, bird-of-paradise plants by the windows, pothos hanging from the trusses."),
        zone("Werkzone", "werken", R(11, 0.3, 25, 10.3),
             "Vierentwintig compacte zit-sta bureaus in twee rijen eilanden, haaks op de tuinramen zodat niemand tegen het licht in kijkt. De zuidrij werkt onder de volle hoogte op 1,5 tot 3 m van het glas, de noordrij onder het vergaderbalkon.",
             ["Zes eilanden van vier bureaus 140 x 70, schermen haaks op het raam", "Looppad van 2,6 m tussen de rijen", "Stalen trap naar het balkon", "Strelitzia's aan het glas, pothos boven elk eiland"],
             cam=dict(t=[18, 5.2], afstand=10, hoek=230),
             prompt="A coworking hall in an old high village building: two rows of islands of four compact sit-stand desks with oak tops placed at right angles to the tall garden windows, the south row under the full 6.7 m height, bird-of-paradise plants by the windows, pothos hanging above the islands, the north row under a steel and timber mezzanine with glass balustrade, slate-blue felt panels, plants."),
        dict(zone("Vergaderbalkon", "vergader", R(11, 5.9, 25, 10.3),
                  "Een tussenvloer van 62 m² boven de noordhelft van de werkzone: twee vergaderkamers voor zes, een sta-kamer en twee belcellen, met een gang van 1,1 m langs de glazen balustrade waar de trap uitkomt.",
                  ["Tussenvloer staal en hout op 3,2 m", "Twee vergaderkamers voor 6 (13 m²) en een sta-kamer voor 4", "Twee belcellen", "Glazen balustrade met hangende pothos naar de werkzone"], n=1,
                  cam=dict(t=[18, 8.1], afstand=8, hoek=250),
                  prompt="A steel and timber mezzanine along one side of a high old hall, with two glass meeting rooms for six, a small standing meeting room with a high round table and two round felt phone booths along a corridor behind a glass balustrade with trailing pothos, overlooking a coworking floor below, timber trusses above."), tussenvloer=True),
        zone("Bufferstrook: wastoren, focus en lockers", "sanitair", R(25, 0.3, 32.2, 10.3),
             "De strook van 7 m tussen werken en sporten. De wastoren staat nu als D met de rug tegen de noordwand (leidingen in de wand, geen dode hoek erachter), zodat ervoor plek is voor twee focuskamers tegen de blinde zuidmuur, drie belcellen en een lockerwand van 5,5 m tegen de gymwand.",
             ["D-vormige wastoren met drie toiletten en wastrog", "Twee focuskamers van oude ramen, 2,2 x 1,9 m", "Drie ronde belcellen", "Lockerwand van 5,5 m: 88 lockers met pothos erbovenop"],
             cam=dict(t=[28.5, 5.3], afstand=8, hoek=230),
             prompt="Inside an old high hall with timber trusses: a D-shaped concrete-look bathroom tower with its flat back against the wall, 3 m high, board-marked plaster, ivy hanging over the rim; in front of it two small glass focus rooms made from reclaimed windows, round felt phone booths and a wall of dark green lockers with trailing pothos on top."),
        zone("Gym (afsluitbaar)", "gym", [[32.2, 0.3], [42.3, 0.3], [42.4, 8.3], [37.1, 8.3], [37.1, 11.6], [32.4, 11.6], [32.4, 10.4], [32.2, 10.4]],
             "De oostkant wordt de gym: racks, roeiers aan de tuinramen, een vloer voor groepslessen en een D-vormige douchetoren tegen de gymwand. Eerst stond hier een ronde toren met de opening tegen die wand; nu is de toren goed bereikbaar en de vloer groter. Techniek in de aanbouw.",
             ["Twee racks op platforms en een kabelrek", "Twee roeiers aan de ramen", "D-vormige douchetoren met vier douches tegen de gymwand", "Kentia en sansevieria", "Deur op toegangspas vanuit de club en een eigen deur naar de tuin"],
             cam=dict(t=[37.5, 5], afstand=9, hoek=230),
             prompt="A small functional gym in the end of an old high village hall: black power racks on oak platforms, rowing machines by tall windows onto a garden, anthracite rubber floor, one wall oxblood red, a D-shaped concrete-look shower tower against the wall with ivy on its rim, a kentia palm."),
    ],
    buiten=[dict(naam="Terras", poly=R(0.5, -6, 24, -0.4), kleur="#b08a5e"), dict(naam="Tuin", poly=R(24, -8, 42, -0.4), kleur="#9bb07a")],
    elementen=[
        *keuken([3.8, 9.97], 5.4), *kookeiland([4.0, 7.8]), *grote_tafel([3.0, 4.0], 4.2, 90), *veelhoekbank([7.8, 4.2], 2.0, 8, open=(6,), draai=0),
        *kasten(1.0, 7.0, 0.55, a=90, d=0.4, h=2.4), *tafeltje([8.8, 8.6]), boom3([10.2, 1.2], "strelitzia nicolai"), plant3([10.4, 9.6], "kentia"),
        boom3([1.1, 8.6], "kentia"), plant3([5.4, 0.9], "strelitzia nicolai"), hangplant([3.0, 3.0], 3.6), hangplant([3.0, 5.0], 3.6), hangplant([4.0, 7.8], 3.6), hangplant([7.8, 4.2], 3.8),
        *eiland2([13.8, 2.9], 87), *eiland2([18.1, 2.9], 93), *eiland2([22.4, 2.9], 87),
        *eiland2([13.8, 8.3], 93), *eiland2([18.1, 8.3], 87), *eiland2([22.4, 8.3], 93),
        *[hangplant([u, 2.9], 3.6) for u in (13.8, 18.1, 22.4)], *[hangplant([u, 8.3], 2.7) for u in (13.8, 18.1, 22.4)],
        plant3([15.95, 0.8], "strelitzia nicolai"), plant3([20.25, 0.8], "strelitzia nicolai"), plant3([16.0, 9.9], "zz-plant"),
        dict(t="box", soort="trap", c=[11.6, 4.4], w=1.0, d=3.0, h=0.3, a=0, kleur="#2f3032"),
        *vergaderkamer([13.3, 8.6], 4.2, 3.2, 0, 6, 1), *stavergaderkamer([16.65, 8.6], 2.3, 3.2, 0, 4, 1), *vergaderkamer([20.0, 8.6], 4.2, 3.2, 0, 6, 1),
        pod2([22.85, 9.4], 1), pod2([24.3, 9.4], 1),
        wand([[11, 5.9], [25, 5.9]], 1.1, glas=True, n=1), *[hangplant([u, 5.75], 0.9, 1) for u in (13.0, 16.5, 20.0, 23.5)],
        *dtoren([31.6, 10.6], [27.0, 10.6], 0.4, "was"), pod2([25.9, 9.7]), pod2([27.4, 4.6]), pod2([29.0, 4.6]),
        *focuskamer([26.2, 1.3], 0), *focuskamer([28.5, 1.3], 0), *lockerwand([31.8, 4.85], 5.5, 90), plant3([25.6, 7.4], "aspidistra"),
        wand([[32.2, 2.0], [32.2, 10.4]], 6.7, gym=True), deur([32.2, 1.2], 90, toegang=True),
        *dtoren([32.3, 9.0], [32.3, 4.0], 0.3, "douche"), *rack([40.8, 1.8], 0), *rack([40.8, 4.9], 0),
        roeier([34.2, 1.1], 0), roeier([37.0, 1.1], 0), deur([38.9, 0.0], 0, toegang=True), dict(t="kleed", c=[37.4, 5.4], w=3.4, d=3.6, a=0, kleur="#c7928a"),
        boom3([41.5, 7.4], "kentia"), plant3([36.6, 7.9], "sansevieria"),
        dict(t="box", soort="techniek", c=[35.9, 10.5], w=2.0, d=1.8, h=2.4, a=0, kleur="#8f8a80"),
        *tafeltje([4, -3], stoelen=3), *tafeltje([9, -3], stoelen=3), *tafeltje([14, -3], stoelen=3), *tafeltje([19, -3], stoelen=3),
        boom([27, -4.5]), boom([33, -5.5]), boom([39, -4.5]), boom([1.5, -5.0], 0.9, 3.0), boom([21.6, -4.6], 0.9, 3.0),
        dict(t="ring", soort="pergola", c=[30.0, -4.4], r=2.4, open=90, gat=0, h=2.6, kleur="#2f3032", dun=True),
    ],
    dak=dict(soort="pv", terras=None, groen=[], pv=[R(1, 0.6, 31, 4.6)], koepels=[[28.5, 5.3, 0.9], [35.0, 5.4, 0.8]],
             tekst="Het oude dak blijft. Zonnepanelen op het zuidvlak als de constructie dat toelaat, lichtkoepels boven de twee torens. De buitenruimte is de tuin aan de zuidkant.",
             tekst_en="The old roof stays; solar panels on the south slope if the structure allows, skylights above the two round towers. A long garden terrace along the south facade with trees and a round pergola."),
    renders=dict(buiten=[]),
)

UDEN = dict(
    titel="Nijverheidsstraat 4C, Uden",
    sub="Nieuwbouwunit van circa 660 m² grondvlak en 8 m hoog met glazen voorgevel, de meerlaagse variant voor circa 100 eigenaren",
    hoogte=8.0, niveaus={"1": 3.6},
    concept="Een hoge, lichte nieuwbouwhal waarin de club in lagen wordt opgebouwd. Achter de glazen voorgevel het café met keuken en een brede zittrap "
            "die naar de galerij leidt. Langs de tussenwand met de buren loopt een werkgalerij met daaronder drie vergaderkamers en belcellen. Langs de "
            "gevel met nieuwe ramen de werkzone op de begane grond, onder de volle hoogte. Achterin de torens als buffer en de gym achter een dichte wand. "
            "Boven het café een leesgalerij. Zo passen circa 60 werkplekken en 100 eigenaren in een pand dat licht en hoog blijft.",
    geluid="Gym achterin de unit, achter de wastoren en de douchetoren (6 m buffer) en een dichte wand tot het dak met deur op toegangspas. "
           "De werkgalerij ligt aan de andere kant van de hal. 40 mm rubber op akoestische ondervloer en platforms. Let op: in een open hal van 8 m draagt geluid; "
           "akoestische baffles onder het dak zijn nodig.",
    pui=[[[38.5, 7.2], [38.5, 20.2]], [[12, 2.15], [24.0, 4.27]], [[1, 0.18], [5.5, 0.98]]],
    zones=[
        zone("Café, keuken en zittrap", "café", [[27, 4.9], [32.7, 5.8], [38.4, 6.9], [38.4, 20.3], [27, 20.3]],
             "Achter de glazen voorgevel: keuken onder de galerij, kookeiland, een grote tafel voor twaalf, een ronde bank en een brede zittrap van 3 m die naar de galerij omhoog loopt.",
             ["Keuken van 6,4 m onder de galerij, kookeiland met 3-groeps machine", "Grote tafel van 4,2 m voor twaalf", "Zittrap van 3 m breed als tribune en trap",
              "Ronde bank rond een sfeerhaard"], foto=8, cam=dict(t=[32.5, 12], afstand=11, hoek=330),
             prompt="Turn this new industrial unit with a two-storey glass facade into the entrance and café of a members club: a wide wooden seating stair leading up to a gallery, an olive green kitchen under the gallery with a reclaimed wood island and a three-group espresso machine, a long oak table for twelve, a round olive velvet sofa around a black fireplace, big trees in pots, warm light against the dark steel cladding."),
        zone("Werkzone begane grond", "werken", [[12, 2.15], [24.2, 4.3], [24.8, 4.3], [27, 4.7], [27, 12.5], [12, 12.5]],
             "Vierentwintig zit-sta bureaus in zes eilanden langs de gevel met nieuwe ramen, onder de volle hoogte van 8 m.",
             ["Zes eilanden van vier bureaus", "Nieuwe ramen in de zijgevel", "Akoestische baffles onder het dak"],
             cam=dict(t=[19.5, 8.4], afstand=11, hoek=250),
             prompt="A coworking floor inside an 8 m high new steel hall: six islands of four compact sit-stand desks with oak tops, new tall windows in the side wall, a timber and steel work gallery on the other side, large slate-blue acoustic baffles hanging under the roof, trees in pots."),
        zone("Vergaderkamers onder de galerij", "vergader", R(12, 12.5, 27, 20.3),
             "Onder de werkgalerij langs de tussenwand: twee vergaderkamers voor acht, een voor zes en vier belcellen.",
             ["Vergaderkamers voor 8, 8 en 6", "Vier ronde belcellen"], cam=dict(t=[19.5, 16.4], afstand=9, hoek=250),
             prompt="Three glass meeting rooms in a row under a steel and timber gallery inside a high hall: oak tables, slate-blue acoustic panels, screens with cameras, round felt phone booths, plants."),
        dict(zone("Werkgalerij", "werken", [[12, 12.5], [27, 12.5], [27, 14], [38.4, 14], [38.4, 20.3], [12, 20.3]],
                  "Een tussenvloer van 190 m² op 3,6 m: zestien bureaus en een werkbank langs de wand boven de vergaderkamers, en boven het café een leesgalerij met boeken en twee belcellen.",
                  ["Vier eilanden van vier bureaus", "Werkbank van 6 m langs de wand", "Leesgalerij boven het café", "Glazen balustrade naar de vide"], n=1,
                  cam=dict(t=[24, 16.4], afstand=10, hoek=250),
                  prompt="A long steel and timber work gallery 3.6 m above the floor of a high new hall: islands of compact sit-stand desks, a long workbench along the wall, a reading gallery with bookshelves and armchairs at the far end, glass balustrade overlooking the coworking floor and café below, skylights."), tussenvloer=True),
        zone("Wastoren en douchetoren", "sanitair", [[6, 1.2], [12, 2.15], [12, 20.3], [6, 20.3]],
             "De twee torens als buffer tussen werken en de gym.", ["Wastoren 5,5 m, douchetoren 4,5 m (alleen vanuit de gym)", "Extra toiletgroep met twee toiletten en een toegankelijk toilet"],
             cam=dict(t=[9, 10.5], afstand=9, hoek=250),
             prompt="Two octagonal concrete-look bathroom towers (flat faces, they still read as round objects), 3 m high, standing in an 8 m high steel hall, board-marked plaster, a V-shaped concrete wash trough with brass taps, ivy and ferns in planters along the top rim, a locker wall built into one outer face, skylights above."),
        zone("Gym (afsluitbaar)", "gym", [[0.2, 0.3], [6, 1.2], [6, 20.3], [0.2, 20.3]],
             "Achterin de unit: vier racks langs de achterwand, een vloer voor groepslessen, roeiers. Dichte wand tot het dak, deur op toegangspas.",
             ["Vier racks op platforms", "Groepslesvloer van 3 x 6 m", "Douchetoren vanuit de gym"], cam=dict(t=[3, 10], afstand=10, hoek=0),
             prompt="A functional gym at the back of a high new steel hall, closed off by a solid wall: four black power racks on oak platforms along the back wall, a mat area, rowing machines, anthracite rubber floor, one wall oxblood red, plants."),
    ],
    buiten=[dict(naam="Voorterrein", poly=R(39, 4, 46, 21), kleur="#c9c3b6")],
    elementen=[
        *keuken([31.2, 19.97], 6.4), *kookeiland([31.2, 17.4]), *grote_tafel([31.8, 12.3], 4.2), *zitkuil([29.6, 8.4], 1.8, 270, "#6f7d3a", "#d9ccb0"),
        dict(t="box", soort="trap", c=[36.4, 11.6], w=3.0, d=4.0, h=0.3, a=0, kleur="#b08a5e"), dict(t="kleed", c=[36.8, 8.2], w=2.4, d=1.6, a=0, kleur="#d5bd96"),
        boom([37.6, 18.6], 0.9, 3.4), boom([27.8, 15.8], 0.8, 3.0), plant([34.6, 7.6]),
        *eiland2([14.0, 6.6], -3), *eiland2([18.0, 6.6], 3), *eiland2([22.0, 6.6], -3),
        *eiland2([14.0, 10.9], 3), *eiland2([18.0, 10.9], -3), *eiland2([22.0, 10.9], 3), plant([25.6, 8.6], 0.4, 1.4),
        *vergaderkamer([15.0, 16.4], 5.0, 4.6, 0, 8), *vergaderkamer([20.4, 16.4], 5.0, 4.6, 0, 8), *vergaderkamer([25.0, 16.4], 3.6, 4.6, 0, 6),
        pod2([14.0, 19.6]), pod2([16.0, 19.6]), pod2([18.0, 19.6]), pod2([20.0, 19.6]),
        *eiland2([14.6, 15.4], 0, 1), *eiland2([18.6, 15.4], 0, 1), *eiland2([22.6, 15.4], 0, 1), *eiland2([26.4, 15.6], 0, 1),
        dict(t="box", soort="raambar", c=[18.0, 19.9], w=6.0, d=0.5, h=1.05, a=0, kleur=HOUT, n=1),
        *kasten(29.0, 37.0, 19.9, n=1, h=2.2), *[dict(t="box", soort="fauteuil", c=[u, 17.4], w=0.85, d=0.85, h=0.8, a=0, kleur="#47522a", n=1) for u in (30.0, 32.4, 34.8)],
        pod2([37.4, 15.2], 1), pod2([37.4, 17.6], 1), wand([[12, 12.5], [27, 12.5], [27, 14], [34.8, 14]], 1.1, glas=True, n=1),
        *toren([9.0, 6.4], 2.75, 0, "was"), *toren([9.0, 14.6], 2.25, 180, "douche"),
        wand([[6, 1.2], [6, 14.0]], 8.0, gym=True), wand([[6, 15.2], [6, 16.0]], 8.0, gym=True), wand([[6, 17.0], [6, 20.3]], 8.0, gym=True), deur([6, 16.5], 90, toegang=True),
        dict(t="box", soort="toiletgroep", c=[9.4, 18.7], w=5.0, d=3.0, h=2.6, a=0, kleur="#bdb7aa"), label([9.4, 18.7], "extra toiletten"),
        *rack([1.6, 4.6], 90), *rack([1.6, 7.7], 90), *rack([1.6, 10.8], 90), *rack([1.6, 13.9], 90),
        roeier([4.4, 3.4], 90), dict(t="kleed", c=[4.2, 9.2], w=2.6, d=6.0, a=0, kleur="#c7928a"),
        dict(t="box", soort="kettlebells", c=[3.6, 18.9], w=2.0, d=0.5, h=0.9, a=0, kleur=STAAL),
        boom([41, 6], 0.9, 3.0), boom([41, 19], 0.9, 3.0),
    ],
    dak=dict(soort="pv", terras=None, groen=[], pv=[R(13, 5.5, 37.8, 19.6), R(0.8, 1.5, 5.6, 19.6)],
             koepels=[[15.0, 8.6, 0.9], [19.0, 8.6, 0.9], [23.0, 8.6, 0.9], [9.0, 6.4, 0.9], [9.0, 14.6, 0.8]],
             tekst="Nieuw plat dak: zonnepanelen over bijna het hele dak en vijf lichtkoepels boven de werkzone en de torens. Geen dakterras: het is een unit in een complex.",
             tekst_en="New flat roof: solar panels across almost the whole roof and five round skylights above the coworking floor and the two towers. Neighbouring units stay simple grey massing."),
    renders=dict(buiten=[(7, "Gevel en entree (impressie ontwikkelaar)", "Keep this new industrial building and its glass facade, make the end unit the entrance of a members club: warm wood around the entrance, large planters and two trees, a bench, a subtle brass sign instead of LOGO, warm interior light visible through the glass showing a wooden seating stair and plants.")]),
)

ONTWERPEN.update({"pernis-ring-15": PERNIS, "uden-nijverheidsstraat-4c": UDEN})
LABELS.update({
    "pernis-ring-15": {"Boekencafé en keuken": [5.6, 6.6], "Werkzone": [17.6, 5.2], "Vergaderbalkon": [18.0, 6.4], "Bufferstrook: wastoren, focus en lockers": [28.4, 6.6], "Gym (afsluitbaar)": [38.4, 3.4]},
    "uden-nijverheidsstraat-4c": {"Café, keuken en zittrap": [33.0, 15.0], "Werkzone begane grond": [19.5, 8.75], "Vergaderkamers onder de galerij": [20.0, 13.4],
                                  "Werkgalerij": [20.0, 13.4], "Wastoren en douchetoren": [9.0, 10.5], "Gym (afsluitbaar)": [3.2, 16.0]},
})


# ---------------------------------------------------------------- Nieuwbouw: eigen hal met atrium (15 november 2026)
# Hal 28 x 20 m, 10 m hoog. Glasgevel tot 6 m op het zuiden (v=0) en oosten (u=28). Galerij op 3,6 m (noord en oost), kroon op 7,0 m.
# West: gym met dakterras erboven. Buffer: entree, wastoren, douchetoren. Midden: atrium met café, zittrap en boom. Oost: werken op twee lagen.
_GB = [[13.4, 19.8], [13.4, 14.3], [17.8, 14.3]]
NIEUWBOUW = dict(
    titel="Eigen nieuwbouwhal met atrium (concept)",
    sub="Zelf bouwen op een bedrijfskavel: een hal van 28 x 20 m en 10 m hoog met glasgevels op het zuiden en oosten, en drie lagen rond een open atrium",
    hoogte=10.0, niveaus={"1": 3.6, "2": 7.0}, pui_h=6.0, nieuwbouw=True,
    concept="Geen bestaand pand verbouwen, maar vanaf nul een hal neerzetten die precies past. Een eenvoudige staalhal met een glasgevel van 6 m hoog op het zuiden en "
            "oosten. Je komt binnen in de entree tussen de gym en het atrium. Het hart is een open atrium van 10 m hoog met een grote boom, het café met een achthoekige bank, de keuken onder de galerij "
            "en een brede zittrap die naar de galerij op 3,6 m leidt. De galerij loopt als een L langs de noordwand (vergaderkamer, sta-kamer, focuskamers) en langs de oostgevel (werkplekken met "
            "uitzicht door het glas). Bovenin, op 7 m, hangt de kroonkamer: een stille vergader- en leeskamer onder een lichtstraat. De gym zit aan de westkant achter een dichte "
            "wand, met de douchetoren als D tegen die wand en aan de clubkant de wastoren, lockers en belcellen als buffer, en op het dak boven de gym ligt het dakterras. Alles is vanaf het begin zo ontworpen: geen compromissen met kolommen, "
            "ramen of vloerhoogtes van een oud pand.",
    geluid="Gym aan de westkant achter een dichte akoestische wand tot het dak (19,6 x 10 m) zonder opening: de douchetoren staat als D in de gym tegen die wand, aan de clubkant "
           "een strook van 5,8 m met de wastoren, lockers en belcellen. De werkplekken zitten "
           "aan de andere kant van de hal, 15 m verder. Ingang van de gym vanuit de entree op toegangspas, zodat de gym om 6:00 open kan terwijl de club dicht is. "
           "40 mm rubber op akoestische ondervloer en zwevende platforms onder de racks, en omdat het nieuwbouw is kan de gymvloer los van de rest van de vloer gestort worden. "
           "Let op: in een atrium van 10 m hoog draagt elk geluid. Akoestische baffles onder het dak, houten lamellen en veel planten zijn nodig.",
    pui=[[[0.3, 0], [27.7, 0]], [[28, 0.3], [28, 19.7]]],
    zones=[
        zone("Atrium met café", "café", R(13.4, 0.2, 22.6, 19.8),
             "Het hart van de club onder 10 m hoogte: een grote boom, een achthoekige bank rond een sfeerhaard, open naar het zuidglas, een lange tafel voor twaalf, een raambar langs de glasgevel en "
             "de zittrap van 4 m breed met boekenkasten in de zijkant. Onder de galerij de keuken van 6,4 m en het kookeiland. Strelitzia's aan het zuidglas, kentia's onder de galerij, pothos aan kabels.",
             ["Zittrap van 4 m breed naar de galerij, met boeken in de zijkant", "Lange tafel van 4,2 m voor twaalf", "Raambar van 8 m langs het zuidglas (13 krukken)",
              "Keuken van 6,4 m onder de galerij, kookeiland met espressomachine", "Achthoekige bank rond een sfeerhaard", "Boom van 6 m hoog in het atrium"],
             cam=dict(t=[18.0, 8.0], afstand=14, hoek=300),
             prompt="The heart of a members club inside a brand-new 10 m high steel hall: a full-height open atrium with a 6 m tall indoor tree, a 4 m wide oak seating stair with built-in bookshelves leading up to a gallery at 3.6 m, an olive green kitchen under the gallery with a reclaimed wood island and an espresso machine, a long oak table for twelve, an octagonal olive green sofa with one open side around a black fireplace, a long bar with stools along a 6 m high glass facade with bird-of-paradise plants, pothos hanging from cables, timber acoustic slats and skylights above."),
        zone("Werkzone", "werken", R(22.6, 0.2, 28, 19.8),
             "Langs de oostgevel van glas: drie eilanden van vier zit-sta bureaus onder de galerij, haaks op het glas zodat niemand tegen het licht in kijkt, met een vrij looppad langs de gevel. De stalen trap naar boven langs het glas, en achterin twee belcellen en de toiletgroep.",
             ["Drie eilanden van vier zit-sta bureaus 140 x 70, schermen haaks op het glas", "Stalen trap naar de galerij langs het glas", "Twee ronde belcellen", "Toiletgroep met twee toiletten en een toegankelijk toilet", "Kentia in de hoek, pothos boven de eilanden"],
             cam=dict(t=[25.3, 7.0], afstand=9, hoek=200),
             prompt="A coworking zone along a tall glass facade, under a timber and steel gallery at 3.6 m: three islands of four compact sit-stand desks with oak tops and slate blue chairs placed at right angles to the glass, a black steel staircase along the glass, round felt phone booths, plants, morning light from the east."),
        zone("Entree", "entree", R(7.6, 0.2, 13.4, 5.8),
             "Binnenkomen door de glasgevel: een mat, een bank, een garderobe en de deur naar de gym op toegangspas.",
             ["Gymdeur op toegangspas, ook buiten openingstijden", "Garderobe en bank"], cam=dict(t=[10.5, 3.0], afstand=7, hoek=270),
             prompt="The entrance of a members club in a new steel hall: a coir mat, a long wooden bench, a coat rack, sand coloured walls with palm green accents, a black steel door with a card reader to the gym, a view into the high atrium with a tree."),
        zone("Torens", "sanitair", R(7.6, 5.8, 13.4, 19.8),
             "De wastoren als buffer tussen de gym en het atrium, open naar het atrium. Waar eerst de douchetoren stond (met een opening in de gymwand) nu lockerwanden langs de noordwand en de gymwand, en twee belcellen.",
             ["Wastoren 5,5 m met V-wastrog", "Lockerwanden van 5 m en 3,6 m: 137 lockers met pothos erbovenop", "Twee ronde belcellen"], cam=dict(t=[10.5, 12.0], afstand=9, hoek=0),
             prompt="An octagonal concrete-look bathroom tower (flat faces, it still reads as a round object), 3 m high, standing inside a 10 m high new steel hall next to an open atrium, board-marked plaster, a V-shaped concrete wash trough with brass taps, ivy and ferns in planters along the top rim; behind it walls of dark green lockers with trailing pothos on top and two round felt phone booths, skylights above."),
        zone("Gym (afsluitbaar)", "gym", R(0.2, 0.2, 7.6, 19.8),
             "De hele westkant: vier racks langs de westwand, een vloer voor groepslessen, roeiers aan het zuidglas en een D-vormige douchetoren tegen de oostwand. Dichte wand tot het dak, deur op toegangspas vanuit de entree.",
             ["Vier racks op zwevende platforms", "Groepslesvloer van 2,6 x 7 m", "Twee roeiers met uitzicht door het glas", "D-vormige douchetoren met vier douches tegen de gymwand", "Strelitzia aan het glas, kentia in de hoek"],
             cam=dict(t=[3.9, 10.0], afstand=10, hoek=0),
             prompt="A functional gym in the west end of a new 10 m high steel hall, closed off by a solid acoustic wall: four black power racks on oak platforms along the wall, a mat area, two rowing machines facing a tall glass facade, a D-shaped concrete-look shower tower against the wall with ivy on its rim, anthracite rubber floor, one wall oxblood red, a bird-of-paradise by the glass."),
        dict(zone("Galerij: vergaderen", "vergader", R(13.4, 14.3, 28, 19.8),
                  "Op 3,6 m langs de noordwand: twee focuskamers, een vergaderkamer voor zes, een sta-kamer, twee belcellen, en de trap naar de kroonkamer. Pothos hangt over de balustrade het atrium in.",
                  ["Vergaderkamer voor 6 en sta-vergaderkamer voor 5, half glas, half dicht", "Twee focuskamers van oude ramen", "Twee ronde belcellen", "Glazen balustrade met hangende pothos naar het atrium"], n=1,
                  cam=dict(t=[19.0, 17.0], afstand=9, hoek=270),
                  prompt="A gallery 3.6 m above the floor of a new high hall: a meeting room for six and a standing meeting room with half glass walls, two small glass focus rooms, slate blue acoustic panels, round phone booths, a glass balustrade with trailing pothos overlooking an atrium with a tall tree."), tussenvloer=True),
        dict(zone("Galerij: werken aan het glas", "werken", R(22.6, 0.2, 28, 14.3),
                  "Op 3,6 m langs de oostgevel: drie eilanden van vier bureaus haaks op het glas en een raambar van 7,6 m pal achter het glas. Hier zit je tussen het atrium en het uitzicht.",
                  ["Drie eilanden van vier zit-sta bureaus, schermen haaks op het glas", "Raambar van 7,6 m langs het glas (12 krukken)", "Glazen balustrade met hangende pothos naar het atrium"], n=1,
                  cam=dict(t=[25.3, 7.0], afstand=9, hoek=180),
                  prompt="A work gallery 3.6 m up along a tall glass facade of a new steel hall: islands of compact sit-stand desks, a long oak bar with stools directly against the glass, a glass balustrade on the other side overlooking an atrium with a tree and a seating stair, acoustic timber slats overhead."), tussenvloer=True),
        dict(zone("Kroonkamer", "bieb", R(21.0, 14.3, 28, 19.8),
                  "Op 7 m, onder een lichtstraat: een stille kamer voor zes met boeken langs de wand, te boeken als vergaderkamer, met uitzicht over het hele atrium.",
                  ["Vergaderkamer voor zes, ook stille leeskamer", "Boekenwand langs de noordwand", "Lichtstraat erboven"], n=2,
                  cam=dict(t=[24.5, 17.0], afstand=8, hoek=270),
                  prompt="A quiet reading and meeting room hanging 7 m high in a new steel hall, under a skylight: deep olive walls, a walnut bookshelf wall, a table for six, butter yellow armchairs, a glass balustrade with a view down into a full-height atrium with a tree."), tussenvloer=True),
    ],
    buiten=[dict(naam="Terras op het zuiden", poly=R(0, -6, 28, 0), kleur="#d5bd96"), dict(naam="Tuin", poly=R(28.3, -6, 36, 20.5), kleur="#8ea36a"),
            dict(naam="Parkeerplaats en groen", poly=R(-4, -14.5, 36, -6), kleur="#c9c3b6"), dict(naam="Straat", poly=R(-40, -26, 75, -16), kleur="#9a958c")],
    elementen=[
        # atrium
        *keuken([18.0, 19.47], 6.4), *kookeiland([18.0, 16.9]),
        dict(t="box", soort="trap", c=[15.6, 11.8], w=4.0, d=5.0, h=0.3, a=0, kleur=HOUT), label([15.6, 8.9], "zittrap"), label([27.3, 5.6], "trap"),
        *kasten(9.3, 14.3, 13.45, a=90, d=0.3, h=2.0), *grote_tafel([20.4, 10.0], 4.2, 90), *veelhoekbank([17.0, 5.0], 2.0, 8, open=(6,), draai=0),
        dict(t="box", soort="raambar", c=[18.0, 0.6], w=8.0, d=0.5, h=1.05, a=0, kleur=HOUT),
        boom([21.0, 4.2], 1.6, 6.5), plant3([13.9, 1.6], "strelitzia nicolai"), boom3([22.0, 15.0], "kentia"), plant3([22.2, 1.3], "strelitzia nicolai"),
        boom3([14.4, 15.6], "kentia"), plant3([21.6, 17.0], "monstera"), hangplant([17.0, 5.0], 5.0), hangplant([20.4, 8.8], 3.2), hangplant([20.4, 11.2], 3.2),
        # werken begane grond: eilanden haaks op de oostgevel
        *eiland2([25.0, 2.8], 0), *eiland2([25.0, 7.1], 0), *eiland2([25.0, 11.4], 0), *[hangplant([25.0, v], 3.2) for v in (2.8, 7.1, 11.4)],
        dict(t="box", soort="trap", c=[27.3, 3.0], w=1.2, d=4.4, h=0.3, a=0, kleur=STAAL),
        pod2([23.6, 15.4]), pod2([25.3, 15.4]), dict(t="box", soort="toiletgroep", c=[25.3, 18.8], w=5.0, d=2.0, h=2.6, a=0, kleur="#bdb7aa"), label([25.3, 18.8], "toiletten"),
        boom3([27.3, 15.8], "kentia"), plant3([22.9, 9.25], "monstera"),
        # entree, torens, gym
        dict(t="kleed", c=[10.5, 1.6], w=2.4, d=1.6, a=0, kleur="#d5bd96"), dict(t="box", soort="bank", c=[12.6, 3.4], w=0.5, d=2.4, h=0.45, a=0, kleur=HOUT),
        dict(t="box", soort="garderobe", c=[8.2, 4.8], w=0.6, d=1.6, h=1.8, a=0, kleur=WALNOOT), plant3([12.8, 0.9], "kentia"), boom3([8.5, 1.1], "olijf"), hangplant([10.5, 3.0], 3.2),
        *achthoektoren([10.5, 9.0], 2.75, 0, "was"),
        *lockerwand([10.5, 19.45], 5.0, 0), *lockerwand([7.95, 16.8], 3.6, 90), pod2([11.4, 16.2]), pod2([9.6, 13.3]), plant3([12.9, 18.4], "aspidistra"),
        wand([[7.6, 0.2], [7.6, 2.4]], 10.0, gym=True), deur([7.6, 3.0], 90, toegang=True), wand([[7.6, 3.6], [7.6, 19.8]], 10.0, gym=True),
        *dtoren([7.5, 15.0], [7.5, 19.6], 0.3, "douche"),
        *rack([1.6, 6.0], 90), *rack([1.6, 9.5], 90), *rack([1.6, 13.0], 90), *rack([1.6, 16.5], 90),
        roeier([3.4, 2.0], 90), roeier([5.0, 2.0], 90), dict(t="kleed", c=[4.8, 11.0], w=2.6, d=7.0, a=0, kleur="#c7928a"),
        dict(t="box", soort="kettlebells", c=[3.8, 19.3], w=2.0, d=0.5, h=0.9, a=0, kleur=STAAL), boom3([6.8, 1.0], "strelitzia nicolai"), plant3([6.9, 6.0], "sansevieria"), boom3([1.2, 18.9], "kentia"),
        # galerij 3,6 m
        wand([[17.8, 14.3], [22.6, 14.3], [22.6, 0.2]], 1.1, glas=True, n=1), wand(_GB[:2], 1.1, glas=True, n=1),
        *[hangplant([22.75, v], 0.9, 1) for v in (2.0, 5.0, 8.0, 11.0)], *[hangplant([u, 14.15], 0.9, 1) for u in (18.6, 20.6)], hangplant([13.55, 17.0], 0.9, 1),
        pod2([14.2, 16.0], 1), pod2([14.2, 18.4], 1), *focuskamer([16.2, 18.8], 180, 1), *focuskamer([18.5, 18.8], 180, 1),
        *vergaderkamer([21.8, 17.75], 4.0, 4.0, 0, 6, 1), *stavergaderkamer([25.2, 17.75], 2.6, 4.0, 0, 5, 1),
        dict(t="box", soort="trap", c=[27.3, 16.6], w=1.2, d=4.4, h=0.3, a=0, kleur=STAAL, n=1), label([27.3, 13.9], "trap", 1),
        *eiland2([24.4, 2.8], 0, 1), *eiland2([24.4, 7.1], 0, 1), *eiland2([24.4, 11.4], 0, 1), *[hangplant([24.4, v], 2.9, 1) for v in (2.8, 7.1, 11.4)],
        dict(t="box", soort="raambar", c=[27.65, 9.8], w=7.6, d=0.5, h=1.05, a=90, kleur=HOUT, n=1), plant3([23.2, 13.6], "kentia", n=1), plant3([17.4, 16.4], "zz-plant", n=1),
        # kroon 7,0 m
        wand([[21.0, 19.8], [21.0, 14.3], [26.6, 14.3]], 1.1, glas=True, n=2),
        *vergaderkamer([23.6, 16.9], 4.8, 4.4, 0, 6, 2), *kasten(21.4, 26.4, 19.55, n=2, h=2.2, d=0.3),
        dict(t="box", soort="fauteuil", c=[27.2, 15.4], w=0.8, d=0.8, h=0.8, a=0, kleur="#e5d48c", n=2), plant3([26.5, 17.6], "zz-plant", n=2),
        *[hangplant([u, 14.15], 0.9, 2) for u in (22.0, 24.0, 26.0)],
        # buiten
        boom([30.5, 3.0], 1.2, 4.0), boom([33.5, 12.0], 1.2, 4.0), boom([31.0, 17.5], 1.0, 3.5), boom([2.0, -4.0], 1.0, 3.5), boom([33.6, -3.2], 1.0, 3.5), boom([25.5, -4.0], 1.0, 3.5),
        *tafeltje([8.0, -3.0], 0, 4), *tafeltje([14.0, -3.2], 0, 4), *tafeltje([20.0, -3.0], 0, 4),
    ],
    dak=dict(soort="pv", terras=R(0.6, 0.6, 7.2, 19.4), trap_buiten=[-0.9, 6.0], groen=[], pv=[R(13.6, 0.8, 27.4, 6.0), R(23.0, 7.5, 27.4, 19.2)],
             koepels=[[17.5, 9.0, 1.2], [17.5, 4.0, 1.2], [24.5, 17.0, 1.0], [10.5, 9.0, 0.9], [9.9, 15.2, 0.8]],
             tekst="Plat dak met zonnepanelen boven het atrium en de werkzone, lichtstraten boven het atrium, de kroonkamer en de torens, en het dakterras van 120 m² boven de gym "
                   "met een buitentrap aan de westgevel. Het dak boven de gym is vanaf het begin berekend op een terras, dus geen versterking achteraf.",
             tekst_en="Flat roof with solar panels above the atrium and the work zone, round skylights above the atrium and the towers, and a 120 m² wooden roof terrace above the gym on the west side with a black steel balustrade, planters, a pergola and an external steel stair along the west facade."),
    renders=dict(buiten=[]),
)
ONTWERPEN.update({"nieuwbouw-atriumhal": NIEUWBOUW})
LABELS.update({"nieuwbouw-atriumhal": {"Atrium met café": [19.2, 15.3], "Werkzone": [25.3, 13.5], "Entree": [10.5, 5.0],
                                       "Torens": [10.5, 12.65], "Gym (afsluitbaar)": [4.0, 18.0], "Galerij: vergaderen": [18.5, 15.15],
                                       "Galerij: werken aan het glas": [25.0, 8.95], "Kroonkamer": [23.6, 14.9]}})
VIDES.update({"nieuwbouw-atriumhal": [dict(naam="Vide: atrium 10 m hoog", poly=R(13.4, 0.2, 22.6, 14.3), n=1),
                                      dict(naam="Vide: atrium", poly=R(13.4, 0.2, 22.6, 14.3), n=2)]})


# ---------------------------------------------------------------- Ronde 7 (15 november 2026): eerst de wijk, dan het pand
# Galvanistraat 122-126 Rotterdam West: drie units in een bedrijfsverzamelgebouw, 29,3 x 16 m met twee entreeportalen aan het parkeerhof (v 16 tot 19,8),
#   vrije hoogte 5,9 m, lichtstraten, entresol aan de voorkant (v 10,5 tot 16, op 3,2 m). Buren zijn bedrijfsunits: geen woningen boven of naast de gym.
GALVANI = dict(
    titel="Galvanistraat 122-126, Rotterdam West",
    sub="Drie bedrijfsunits uit 2000 met lichtstraten en een entresol, aan een parkeerhof op de grens van Rotterdam West en Schiedam",
    hoogte=6.8, niveaus={"1": 3.2},
    concept="Drie units worden één club. Je komt binnen door het noordelijke portaal, direct in het café met keuken, een lange tafel en een zittrap naar de entresol. "
            "In het midden de werkzone onder de lichtstraten, met onder de entresol een vergaderkamer en belcellen. Daarachter de twee ronde torens als buffer, en aan de "
            "zuidkant de gym met een eigen ingang door het zuidelijke portaal, zodat sporters om 6:00 naar binnen kunnen. Boven, op de entresol, een stille werkgalerij en een "
            "tweede vergaderkamer. Tussen de twee portalen komt een terras met plantenbakken aan het parkeerhof. Alles sober: de scheidingswanden tussen de units gaan er deels uit, "
            "de lichtstraten blijven, de vloer wordt strak geschuurd en gecoat.",
    geluid="Gym aan de zuidkant, tegen de bedrijfsunit van de buren; geen woningen in het gebouw. Tussen gym en werken de wastoren en de douchetoren (5,8 m buffer) en een "
           "dichte wand tot het dak. 40 mm rubber op een akoestische ondervloer en platforms onder de racks. De entresol boven de werkzone, niet boven de gym.",
    pui=[[[8.5, 16.0], [23.1, 16.0]], [[3.3, 19.8], [8.5, 19.8]], [[23.1, 19.8], [28.3, 19.8]]],
    zones=[
        zone("Café, keuken en zittrap", "café", [[21.0, 0.2], [29.1, 0.2], [29.1, 16.0], [28.3, 16.0], [28.3, 19.6], [23.1, 19.6], [23.1, 16.0], [21.0, 16.0]],
             "Door het noordelijke portaal kom je in het café: keuken langs de wand van de buren, een kookeiland, een lange tafel voor twaalf onder de lichtstraten en een zittrap van 3 m naar de entresol. Onder de entresol een ronde bank.",
             ["Keuken van 5,6 m langs de muur, kookeiland met espressomachine", "Lange tafel van 4,2 m voor twaalf", "Zittrap van 3 m naar de entresol", "Ronde bank onder de entresol"],
             cam=dict(t=[25.0, 7.0], afstand=10, hoek=200),
             prompt="The café of a members club inside a simple industrial unit from 2000 with round roof lights: an olive green kitchen made from second-hand stainless steel worktables and old timber fronts along the side wall, a reclaimed wood island with an espresso machine, a long oak table for twelve, a wooden seating stair up to a mezzanine, a round olive velvet sofa, plants."),
        zone("Werkzone onder de lichtstraten", "werken", R(13.6, 0.2, 21.0, 10.5),
             "Zes eilanden van vier zit-sta bureaus onder de volle hoogte en de lichtstraten.",
             ["Zes eilanden van vier bureaus 140 x 70", "Lichtstraten blijven, akoestiek van houtwolplaten"],
             cam=dict(t=[17.3, 5.3], afstand=9, hoek=180),
             prompt="A coworking floor in a simple industrial unit with round roof lights: six islands of four compact sit-stand desks with oak tops, slate blue chairs, wood wool acoustic panels between the steel beams, a smooth sealed concrete floor, plants, a mezzanine with a glass balustrade at the front."),
        zone("Vergaderen onder de entresol", "vergader", R(13.6, 10.5, 21.0, 16.0),
             "Onder de entresol een vergaderkamer voor acht met wanden van oude ramen, en twee belcellen.",
             ["Vergaderkamer voor acht", "Twee ronde belcellen"], cam=dict(t=[17.3, 13.2], afstand=7, hoek=270),
             prompt="A meeting room for eight under a mezzanine, its walls made from reclaimed old steel and timber windows, an oak table, slate blue acoustic panels, round felt phone booths next to it."),
        zone("Torens en toiletten", "sanitair", R(7.8, 0.2, 13.6, 16.0),
             "De wastoren en de douchetoren tussen gym en werken, met onder de entresol de toiletgroep.",
             ["Wastoren 5,5 m, douchetoren 4,5 m (alleen vanuit de gym)", "Toiletgroep onder de entresol"], cam=dict(t=[10.7, 6.0], afstand=8, hoek=180),
             prompt="Two octagonal concrete-look bathroom towers (flat faces, they still read as round objects), 3 m high, in a simple industrial unit with roof lights, board-marked plaster, a V-shaped concrete wash trough with brass taps, ivy and ferns along the top rim, lockers built into an outer face."),
        zone("Gym (eigen ingang)", "gym", [[0.2, 0.2], [7.8, 0.2], [7.8, 16.0], [8.5, 16.0], [8.5, 19.6], [3.3, 19.6], [3.3, 16.0], [0.2, 16.0]],
             "Aan de zuidkant, met een eigen ingang door het zuidelijke portaal: drie racks, een vloer voor groepslessen, roeiers bij het portaal.",
             ["Drie racks op zwevende platforms", "Eigen ingang op toegangspas", "Douchetoren direct vanuit de gym"], cam=dict(t=[4.0, 8.0], afstand=9, hoek=0),
             prompt="A functional gym in an industrial unit with round roof lights, closed off by a solid wall: three black power racks on oak platforms, a mat area, rowing machines near a glass entrance portal, anthracite rubber floor, one wall oxblood red, plants."),
        dict(zone("Entresol: stille werkgalerij", "werken", R(7.8, 10.5, 29.1, 15.8),
                  "De bestaande kantoorentresol wordt een stille werkgalerij: twee eilanden van vier bureaus, een raambar van 11 m pal achter de voorgevel (19 krukken), twee glazen focuskamers, een vergaderkamer voor zes en twee belcellen. Pothos hangt over de balustrade naar beneden.",
                  ["Twee eilanden van vier bureaus", "Raambar van 11 m langs de voorgevel", "Twee focuskamers voor één of twee personen", "Vergaderkamer voor zes", "Twee belcellen"], n=1, cam=dict(t=[17.0, 13.2], afstand=9, hoek=270),
                  prompt="A quiet work mezzanine 3.2 m above an industrial floor: islands of compact sit-stand desks, a glass balustrade overlooking a café and coworking floor below, a meeting room with walls of reclaimed windows, round roof lights."), tussenvloer=False),
    ],
    buiten=[dict(naam="Terras tussen de portalen", poly=R(8.5, 16.0, 23.1, 19.8), kleur="#d5bd96"), dict(naam="Parkeerplaats en groen", poly=R(-2, 19.8, 31.3, 32), kleur="#c9c3b6")],
    elementen=[
        *keuken([28.77, 7.3], 5.6, 90), *kookeiland([26.8, 7.4], 90), *grote_tafel([25.6, 2.3], 4.2),
        dict(t="box", soort="trap", c=[22.8, 8.0], w=3.0, d=5.0, h=0.3, a=0, kleur=HOUT), label([22.8, 5.2], "zittrap"),
        *veelhoekbank([26.5, 13.2], 1.7, 6, open=(1, 4)), boom3([22.0, 1.4], "kentia"), plant3([28.5, 1.2], "ficus elastica"), plant3([21.5, 15.2], "strelitzia nicolai"), *focuskamer([23.5, 14.85], 0), pod2([21.7, 11.3]), pod2([21.7, 13.0]), *[hangplant([u, 10.2]) for u in (14.0, 17.0, 20.0, 25.0, 28.0)],
        *eiland2([15.6, 2.0], 0), *eiland2([19.2, 2.0], 0), *eiland2([15.6, 5.3], 0), *eiland2([19.2, 5.3], 0), *eiland2([15.6, 8.6], 0), *eiland2([19.2, 8.6], 0), plant3([17.4, 3.65], "zz-plant"), plant3([17.4, 6.95], "zz-plant"), *groenwand([13.8, 0.25], [20.8, 0.25], 3.0),
        *vergaderkamer([15.3, 13.2], 4.6, 3.0, 90, 6), *stavergaderkamer([18.0, 13.2], 2.4, 4.6, 0, 5), pod2([20.2, 11.6]), pod2([20.2, 14.5]),
        *toren([10.7, 3.0], 2.75, 0, "was"), *toren([10.25, 8.2], 2.25, 180, "douche"),
        dict(t="box", soort="toiletgroep", c=[10.7, 12.0], w=5.0, d=2.0, h=2.6, a=0, kleur="#bdb7aa"), label([10.7, 12.0], "toiletten"), *lockerwand([10.85, 15.3], 5.2, 0), label([10.85, 14.6], "lockers"),
        wand([[7.8, 0.2], [7.8, 7.6]], 6.8, gym=True), wand([[7.8, 8.8], [7.8, 12.8]], 6.8, gym=True), deur([7.8, 13.5], 90, toegang=True), wand([[7.8, 14.2], [7.8, 16.0]], 6.8, gym=True),
        deur([5.9, 19.8], 0, toegang=True), deur([25.7, 19.8], 0),
        *rack([1.6, 3.2], 90), *rack([1.6, 6.6], 90), *rack([1.6, 10.0], 90), dict(t="kleed", c=[5.2, 7.0], w=2.4, d=6.5, a=0, kleur="#c7928a"),
        roeier([4.6, 13.6], 0), roeier([4.6, 14.8], 0), *lockerwand([3.65, 17.8], 3.0, 90), dict(t="box", soort="kettlebells", c=[5.0, 1.0], w=2.0, d=0.5, h=0.9, a=0, kleur=STAAL), plant3([7.2, 15.2], "sansevieria"), plant3([6.8, 1.0], "kentia"),
        wand([[7.8, 10.5], [21.3, 10.5]], 1.1, glas=True, n=1), wand([[24.3, 10.5], [29.1, 10.5]], 1.1, glas=True, n=1),
        pod2([8.55, 12.0], 1), pod2([8.55, 14.4], 1), *focuskamer([10.3, 12.6], 0, 1), *focuskamer([12.6, 12.6], 0, 1), *eiland2([15.2, 13.15], 0, 1), *eiland2([19.0, 13.15], 0, 1), dict(t="box", soort="raambar", c=[15.3, 15.55], w=11.4, d=0.5, h=1.05, a=0, kleur=HOUT, n=1),
        *vergaderkamer([27.0, 13.15], 4.0, 4.6, 90, 6, 1), pod2([23.2, 14.8], 1),
        dict(t="box", soort="plantenbak", c=[15.8, 19.3], w=14.0, d=0.5, h=0.6, a=0, kleur=WALNOOT), *tafeltje([12.0, 17.8], 0, 4), *tafeltje([16.0, 17.8], 0, 4), *tafeltje([20.0, 17.8], 0, 4),
        boom([1.0, 22.0], 0.9, 3.0), boom([30.0, 22.0], 0.9, 3.0),
    ],
    dak=dict(soort="pv", terras=None, groen=[], pv=[R(13.8, 0.8, 28.6, 9.6)],
             koepels=[[16.5, 4.0, 0.8], [20.5, 4.0, 0.8], [24.5, 4.0, 0.8], [4.0, 4.0, 0.8], [4.0, 11.0, 0.8], [10.7, 3.0, 0.8]],
             tekst="Bestaand plat dak met lichtstraten; zonnepanelen boven café en werkzone. Geen dakterras: het is een unit in een verzamelgebouw.",
             tekst_en="Existing flat roof of a long row of industrial units with round roof lights; solar panels above the club's café and work zone. Neighbouring units stay plain grey."),
    renders=dict(buiten=[]),
)

# Calandstraat 92 Schiedam: vrijstaande hal uit 1973 van 42 x 24 m, circa 5,4 m tot het dak, op de hoek van twee straten met bomen aan de noordkant (v = 24).
#   Hal 800 + kantoor 200 m² (aanname: kantoor in twee lagen op de noordoosthoek). Erfpacht. Kavel is het gebouw: buiten alleen de stoep en parkeren langs de straat.
CALAND = dict(
    titel="Calandstraat 92, Schiedam",
    sub="Vrijstaande hal uit 1973 van 1.000 m² op de hoek van twee straten. LET OP: de makelaar biedt het nu ook te huur aan (€ 6.900 per maand); bel of het nog te koop is.",
    hoogte=5.4, niveaus={"1": 2.8},
    concept="Een grote, eenvoudige hal waarin de club voor circa 110 eigenaren ruim op één laag past. Aan de straatkant met bomen komen nieuwe ramen van hergebruikte kozijnen: "
            "daarachter het café met keuken, lange tafel, een achthoekige bank en een raambar van 10 m. De werkzone ligt in het midden van de hal, met zes eilanden van zes bureaus "
            "onder vier lichtstraten en een lockerwand van 9,6 m tegen de blinde zuidmuur. Langs de oostgevel, tegen het glas, drie vergaderkamers, een sta-kamer en belcellen. "
            "In de zuidwesthoek, tegen de buren, de gym achter een dichte wand met de wastoren, de toiletten en een zitnis als buffer. Het kantoordeel op de hoek wordt entree en "
            "bieb, met boven een stille verdieping met drie focuskamers.",
    geluid="Gym in de zuidwesthoek tegen de bedrijfshal van de buren. De douchetoren staat nu als D in de gym tegen de wand, zodat de gymwand zonder opening tot het dak doorloopt; "
           "aan de clubkant een strook van 6 m met wastoren, toiletten en een zitnis. De werkplekken liggen 6 tot 20 m verder. Er wonen geen mensen in of naast het gebouw. "
           "40 mm rubber op akoestische ondervloer.",
    pui=[[[0.5, 24.0], [31.5, 24.0]], [[42.0, 0.5], [42.0, 13.5]]],
    zones=[
        zone("Café aan de straat", "café", R(0.2, 14.3, 18.0, 23.8),
             "Achter nieuwe ramen aan de straat met bomen: keuken langs de westwand, kookeiland, lange tafel voor twaalf, een achthoekige bank open naar de ramen en een raambar van 10 m. Tegen de gymwand klimwanden met pothos, aan het glas strelitzia en ficus.",
             ["Keuken van 6,4 m en kookeiland", "Lange tafel voor twaalf", "Raambar van 10 m (16 krukken)", "Achthoekige bank rond een sfeerhaard", "Klimwanden van 9 m tegen de blinde gymwand"],
             cam=dict(t=[9.0, 19.0], afstand=11, hoek=300),
             prompt="The café of a members club in a plain 1970s industrial hall, behind new windows made from reclaimed steel frames facing a street with trees: an olive green kitchen from second-hand stainless steel worktables along the wall, a reclaimed wood island, a long oak table, an octagonal olive green sofa with one open side around a black fireplace, a long bar with stools at the windows, a green wall of steel cables with pothos, a bird-of-paradise and a rubber fig by the windows."),
        zone("Werkzone in de hal", "werken", R(18.0, 4.0, 32.0, 23.8),
             "Zes eilanden van zes zit-sta bureaus in het midden van de hal, met akoestiek van houtwolplaten onder het dak en daglicht van de straatkant en vier lichtstraten. Tegen de blinde zuidmuur een lockerwand van 9,6 m met de werkbank voor printer en post ervoor; kentia's en ficus langs de randen. Van de entree naar het café loop je langs de straatgevel, met 2 m afstand tot de bureaus.",
             ["Zes eilanden van zes bureaus 140 x 70", "Nieuwe lichtstraten boven de werkzone", "Lockerwand van 9,6 m: 153 lockers, pothos erbovenop", "Drie belcellen in de hoeken", "Kentia, ficus en zz-planten, pothos boven elk eiland"], cam=dict(t=[25.0, 13.5], afstand=11, hoek=200),
             prompt="A coworking floor in a plain industrial hall: six islands of six compact sit-stand desks with oak tops, slate blue chairs, wood wool acoustic panels under the roof, new skylights, a smooth sealed concrete floor, kentia palms and a rubber fig in pots, a long wall of dark green lockers with trailing pothos on top."),
        zone("Vergaderen langs de oostgevel", "vergader", R(32.0, 0.2, 41.8, 14.0),
             "Drie vergaderkamers voor 6, 6 en 4 met wanden van oude ramen, nu tegen de glazen oostgevel geschoven zodat ze daglicht hebben. Op de vrijgekomen strook een sta-kamer en drie belcellen. Een kamer voor acht is niet nodig.",
             ["Vergaderkamers voor 6 (2x, 25 m²) en 4", "Sta-vergaderkamer voor 5 met statafel en whiteboardwand", "Drie belcellen"],
             cam=dict(t=[37.0, 7.0], afstand=9, hoek=180),
             prompt="Three meeting rooms in a row against the glass side facade of an industrial hall, walls made from reclaimed windows in timber frames, oak tables for six and four, a small standing meeting room with a high round table and a whiteboard wall, slate blue acoustic panels, round felt phone booths, plants."),
        zone("Entree en bieb", "bieb", R(32.0, 14.0, 41.8, 23.8),
             "Het kantoordeel op de hoek: entree aan de straat, garderobe en een bieb met boekenwand en leesstoelen, een belcel, een kentia en een ficus.", ["Entree op de hoek", "Boekenwand en leesstoelen", "Een ronde belcel", "Kentia en ficus"],
             cam=dict(t=[37.0, 19.0], afstand=8, hoek=270),
             prompt="A small library and entrance in the office corner of an industrial building: a walnut bookshelf wall, butter yellow armchairs, deep olive walls, a coat rack, plants."),
        zone("Torens en toiletten", "sanitair", R(12.0, 0.2, 18.0, 14.3),
             "De wastoren en de toiletgroep tussen gym en werken. Waar eerst de douchetoren stond, met een opening in de gymwand, staat nu een zitnis van 5 m tegen de dichte gymwand met een kentia ernaast.",
             ["Wastoren met drie toiletten en V-wastrog", "Toiletgroep met drie toiletten: samen zes", "Zitnis van 5 m met drie tafeltjes tegen de blinde gymwand"], cam=dict(t=[15.0, 7.0], afstand=8, hoek=180),
             prompt="An octagonal concrete-look bathroom tower (flat faces, it still reads as a round object) in an industrial hall, board-marked plaster, a V-shaped concrete wash trough with brass taps, ivy and ferns along the top rim; next to it a long built-in bench with small tables against a solid wall, a kentia palm."),
        zone("Gym (afsluitbaar)", "gym", R(0.2, 0.2, 12.0, 14.0), "Zuidwesthoek: vier racks, een groepslesvloer en roeiers, een D-vormige douchetoren tegen de oostwand, dichte wanden en een deur op toegangspas.",
             ["Vier racks op zwevende platforms", "Groepslesvloer", "D-vormige douchetoren met vier douches tegen de gymwand", "Klimwand met pothos, kentia's in de hoeken"], cam=dict(t=[6.0, 7.0], afstand=9, hoek=0),
             prompt="A functional gym in the corner of a plain industrial hall, closed off by solid walls: four black power racks on oak platforms, a mat area, rowing machines, a D-shaped concrete-look shower tower against the wall with ivy on its rim, anthracite rubber floor, one wall oxblood red, a green wall with pothos, kentia palms."),
        dict(zone("Stille verdieping", "bieb", R(32.0, 14.0, 41.8, 23.8),
                  "De kantoorverdieping wordt een stille kamer met acht studieplekken, een kamer voor vier, drie focuskamers en twee belcellen.", ["Acht studieplekken", "Kamer voor vier", "Drie focuskamers van oude ramen", "Twee belcellen"], n=1,
                  cam=dict(t=[37.0, 19.0], afstand=7, hoek=270),
                  prompt="A quiet study room on the upper office floor of an industrial building: timber study tables, green desk lamps, bookshelves, a small meeting room and three small focus rooms with walls of reclaimed windows, low-light plants."), tussenvloer=False),
    ],
    buiten=[dict(naam="Stoep en bomen", poly=R(-2, 24.0, 44, 30), kleur="#c9c3b6"), dict(naam="Straat", poly=R(-10, 30, 52, 38), kleur="#9a958c")],
    elementen=[
        *keuken([0.55, 18.6], 6.4, 90), *kookeiland([3.4, 18.6], 90), *grote_tafel([8.6, 17.6], 4.2), *veelhoekbank([14.4, 18.3], 2.0, 8, open=(2,), draai=0),
        dict(t="box", soort="raambar", c=[10.5, 23.5], w=10.0, d=0.5, h=1.05, a=0, kleur=HOUT), boom3([6.0, 22.2], "strelitzia nicolai"), boom3([16.9, 22.4], "ficus elastica"), plant3([17.4, 15.0], "monstera"),
        *[hangplant([u, 23.3]) for u in (7.0, 10.5, 14.0)], hangplant([7.2, 17.6], 3.6), hangplant([10.0, 17.6], 3.6), hangplant([3.4, 18.6], 3.6), boom3([1.3, 23.0], "kentia"), plant3([0.8, 14.8], "zz-plant"),
        *groenwand([1.3, 14.05], [5.4, 14.05], 3.0), *groenwand([6.8, 14.05], [11.8, 14.05], 3.0),
        wand([[0.2, 14.0], [5.5, 14.0]], 5.4, gym=True), deur([6.1, 14.0], 0, toegang=True), wand([[6.7, 14.0], [12.0, 14.0]], 5.4, gym=True),
        wand([[12.0, 0.2], [12.0, 14.0]], 5.4, gym=True),
        *toren([15.0, 3.4], 2.75, 0, "was"), *dtoren([11.9, 9.0], [11.9, 13.8], 0.3, "douche"), dict(t="box", soort="toiletgroep", c=[15.0, 13.0], w=5.0, d=2.0, h=2.6, a=0, kleur="#bdb7aa"),
        label([15.0, 13.0], "toiletten"), *zitnis([12.1, 11.6], [12.1, 6.6]), boom3([16.9, 8.8], "kentia"), plant3([17.3, 11.4], "aspidistra"), hangplant([13.05, 7.8], 3.0), hangplant([13.05, 10.4], 3.0),
        *rack([1.6, 3.0], 90), *rack([1.6, 6.4], 90), *rack([1.6, 9.8], 90), *rack([5.0, 1.6], 0), dict(t="kleed", c=[7.4, 8.0], w=3.0, d=6.5, a=0, kleur="#c7928a"),
        roeier([10.6, 4.0], 90), roeier([10.6, 7.0], 90), dict(t="box", soort="kettlebells", c=[3.6, 13.4], w=2.0, d=0.5, h=0.9, a=0, kleur=STAAL),
        boom3([1.2, 12.8], "kentia"), boom3([11.1, 1.3], "kentia"), *groenwand([6.6, 0.25], [9.8, 0.25], 3.0),
        *eiland2([21.6, 7.5], 0, k=6), *eiland2([28.2, 7.5], 0, k=6), *eiland2([21.6, 12.7], 0, k=6), *eiland2([28.2, 12.7], 0, k=6),
        *eiland2([21.6, 17.9], 0, k=6), *eiland2([28.2, 17.9], 0, k=6), *[hangplant([u, v]) for u in (21.6, 28.2) for v in (7.5, 12.7, 17.9)],
        plant3([24.9, 21.8], "monstera"), boom3([31.1, 22.4], "ficus elastica"), boom3([31.2, 10.1], "kentia"), boom3([31.2, 15.3], "kentia"), boom3([18.8, 15.3], "kentia"),
        plant3([18.8, 4.8], "zz-plant"), plant3([24.9, 10.1], "zz-plant"), plant3([24.9, 15.3], "zz-plant"), plant3([18.9, 10.1], "dracaena"),
        *lockerwand([25.0, 0.45], 9.6, 0), dict(t="box", soort="werkbank", c=[25.0, 3.0], w=4.0, d=0.7, h=0.9, a=0, kleur=HOUT), label([25.0, 2.1], "lockers, printer en post"),
        *vergaderkamer([39.0, 2.6], 5.6, 4.4, 0, 6), *vergaderkamer([39.0, 7.3], 5.6, 4.4, 0, 6), *vergaderkamer([39.9, 11.8], 3.6, 3.6, 0, 4),
        *stavergaderkamer([33.6, 1.9], 2.8, 3.2, 0, 5), plant3([35.6, 0.8], "zz-plant"), plant3([37.6, 13.6], "kentia"), plant3([32.6, 13.4], "philodendron"), *[plant3([41.4, v], "zz-plant") for v in (0.8, 5.5, 10.4)],
        pod2([36.9, 10.8]), pod2([36.9, 12.5]), pod2([33.0, 7.0]), pod2([19.0, 2.2]), pod2([30.8, 2.2]), pod2([18.9, 21.6]), pod2([34.0, 15.4], 1), pod2([33.3, 22.6], 1),
        *kasten(33.0, 39.0, 23.55, h=2.4), dict(t="box", soort="fauteuil", c=[34.5, 20.0], w=0.85, d=0.85, h=0.8, a=0, kleur="#47522a"),
        boom3([40.3, 23.0], "kentia"), boom3([32.9, 20.0], "ficus elastica"), plant3([32.6, 22.9], "zz-plant"), pod2([35.0, 15.0]), plant3([41.3, 15.2], "sansevieria"),
        dict(t="box", soort="fauteuil", c=[36.5, 20.0], w=0.85, d=0.85, h=0.8, a=0, kleur="#47522a"), dict(t="kleed", c=[35.5, 19.6], w=3.0, d=2.0, a=0, kleur="#e5d48c"),
        dict(t="box", soort="garderobe", c=[41.3, 18.0], w=0.6, d=2.4, h=1.8, a=0, kleur=WALNOOT), deur([42.0, 21.0], 90), dict(t="box", soort="trap", c=[33.0, 16.0], w=1.1, d=3.6, h=0.3, a=0, kleur=STAAL),
        dict(t="box", soort="werktafel", c=[36.5, 19.0], w=3.0, d=1.0, h=0.75, a=0, kleur=HOUT, pers=6, n=1), dict(t="box", soort="werktafel", c=[36.5, 22.5], w=3.0, d=0.8, h=0.75, a=0, kleur=HOUT, pers=2, n=1),
        *vergaderkamer([39.6, 16.3], 4.0, 4.0, 90, 4, 1), *focuskamer([40.8, 19.6], 90, 1), *focuskamer([40.8, 21.85], 90, 1), *focuskamer([36.0, 15.3], 0, 1),
        plant3([38.6, 23.3], "zz-plant", n=1), plant3([34.6, 23.3], "sansevieria", n=1), hangplant([36.5, 19.0], 2.4, 1),
        boom([4.0, 27.0], 1.0, 4.0), boom([16.0, 27.0], 1.0, 4.0), boom([28.0, 27.0], 1.0, 4.0), boom([40.0, 27.0], 1.0, 4.0),
    ],
    dak=dict(soort="pv", terras=None, groen=[], pv=[R(0.8, 0.8, 41.2, 13.4)], koepels=[[21.5, 10.0, 0.9], [28.5, 10.0, 0.9], [21.5, 16.0, 0.9], [28.5, 16.0, 0.9], [15.0, 3.4, 0.8]],
             tekst="Plat dak vol zonnepanelen op de zuidhelft en vier nieuwe lichtstraten boven de werkzone. Geen dakterras: het dak is licht gebouwd (1973).",
             tekst_en="Flat roof with solar panels on the southern half and four new round skylights above the work zone; plain 1970s hall on a street corner with trees."),
    renders=dict(buiten=[]),
)

# Metaalhof 40 Rotterdam (Het Lage Land): pand uit 1986 van 31,6 x 16 m met een kopblok (u 0 tot 8,9, v 16 tot 26,9). Voor de hal een open strook van 245 m² op eigen grond
#   (3 parkeerplaatsen, terras). Buren zijn bedrijfspanden. Volgens de brochure is maar circa 110 m² hoog; de rest is laag: 222 m² kantoor beneden en 360 m² boven.
#   Aanname (16-11-2026, na te meten bij bezichtiging): de hoge ruimte is het noordeinde (u 24 tot 31,6, circa 115 m²); de verdieping van 360 m² ligt boven het kantoordeel
#   en de kop (u 0 tot 9) en boven de eerste 8 m van de hal (u 9 tot 17); daartussen (u 17 tot 24) een lage strook van één laag.
METAAL = dict(
    titel="Metaalhof 40, Rotterdam Het Lage Land",
    sub="Pand uit 1986: kantoor in twee lagen, een lage strook en een hoge hal van circa 110 m², met eigen buitenruimte. Ontwerp naar de brochure: alleen de gym staat in de hoge ruimte; erfpacht afgekocht tot 2035.",
    hoogte=6.5, niveaus={"1": 3.0},
    concept="Volgens de brochure is maar circa 110 m² van het pand hoog; de rest is laag kantoor, 222 m² beneden en 360 m² boven. Dus hangt niets meer aan een grote hal. "
            "Beneden in het kantoordeel de werkzone met zes eilanden. Daarnaast, onder de verdieping, het café met keuken, lange tafel en een zeshoekige bank achter een nieuwe glazen pui naar het eigen terras. "
            "In de lage strook daarachter de wastoren, de lockers, belcellen en een zitnis als buffer. Alleen de gym krijgt de hoge ruimte aan het noordeinde, met een eigen deur naar het terras. "
            "Boven vergaderkamers, een sta-kamer, drie focuskamers, belcellen en een stille werkvloer boven het café. Aanname: de hoge hal ligt aan het noordeinde; na te meten bij de bezichtiging.",
    geluid="Gym in de hoge ruimte aan het noordeinde, achter een lage strook van 7 m met wastoren, lockers en zitnis, en een dichte wand tot het dak zonder opening: "
           "de douchetoren staat als D in de gym tegen die wand. De werkplekken beneden zitten 15 m verder, achter het café en een bestaande wand; boven ligt de werkvloer niet boven de gym. "
           "Buren zijn bedrijfspanden. 40 mm rubber op akoestische ondervloer.",
    pui=[[[9.5, 16.0], [18.0, 16.0]]],
    zones=[
        zone("Café onder de kantoorvloer", "café", R(9.0, 0.2, 17.0, 15.8),
             "Het café hoeft geen hoge hal: het zit in het lage deel onder de verdieping, met een nieuwe glazen pui en een eigen deur naar het terras, zodat niemand door de werkzone naar het café hoeft. Keuken langs de achterwand, kookeiland, een lange tafel voor twaalf, "
             "een zeshoekige bank aan het glas en een raambar. Strelitzia en ficus aan de pui, pothos aan de balken.",
             ["Keuken van 6,4 m en kookeiland", "Lange tafel voor twaalf", "Zeshoekige bank, open naar het terras", "Raambar van 4,2 m", "Glazen pui van hergebruikte kozijnen met een deur naar het terras"],
             cam=dict(t=[13.0, 8.0], afstand=10, hoek=180),
             prompt="The café of a members club in the low ground floor of a 1980s industrial building, under an exposed timber and steel ceiling about 3 m high: an olive green kitchen from second-hand stainless steel worktables along the back wall, a reclaimed wood island, a long oak table for twelve, a hexagonal olive green sofa with one open side by a new glass front made from reclaimed steel windows opening to a terrace, a bird-of-paradise and a rubber fig at the glass, pothos hanging from the beams."),
        zone("Werken in het kantoordeel", "werken", R(0.2, 0.2, 9.0, 15.8),
             "De begane grond van het kantoordeel: zes eilanden van vier zit-sta bureaus in twee rijen, met een middenpad van 1,4 m.", ["Zes eilanden van vier bureaus 140 x 70", "Middenpad van 1,4 m, 90 cm achter elke stoel", "Pothos boven elk eiland, kentia en zz-plant in de hoeken"],
             cam=dict(t=[4.6, 8.0], afstand=8, hoek=0),
             prompt="A coworking floor in the ground floor office part of an industrial building: six islands of four compact sit-stand desks with oak tops, slate blue chairs, wood wool acoustic ceiling panels, kentia palms, pothos hanging above the islands, windows."),
        zone("Entree en toiletten", "entree", R(0.2, 16.0, 8.9, 26.7), "Het kopblok: entree vanaf het terras voor wie gaat werken, garderobe, twee leesstoelen, de trap naar boven en de toiletgroep. Het café heeft een eigen deur in de glazen pui.",
             ["Entree en garderobe", "Twee fauteuils bij de trap", "Toiletgroep", "Trap naar de verdieping", "Kentia bij de deur"], cam=dict(t=[4.5, 21.0], afstand=7, hoek=270),
             prompt="The entrance of a members club in a small office block: coir mat, long wooden bench, coat rack, a steel staircase, sand coloured walls with palm green accents, a kentia palm."),
        zone("Wastoren, lockers en zitnis", "sanitair", R(17.0, 0.2, 24.0, 15.8),
             "De lage strook tussen café en gym is de buffer: de wastoren open naar het café, met lockerkasten op drie buitenzijden, een lockerwand tegen de dichte gymwand, twee belcellen in de donkere kern "
             "en een zitnis langs de blinde gevel bij de gymdeur.",
             ["Wastoren met drie toiletten en V-wastrog", "Lockers: 90 op de toren, 41 in de wand tegen de gym", "Twee ronde belcellen", "Zitnis van 4,2 m met tafeltjes", "Lichtkoepel boven de toren, kentia en aspidistra"],
             cam=dict(t=[20.5, 8.0], afstand=8, hoek=180),
             prompt="A low single-storey zone in a 1980s industrial building: an octagonal concrete-look bathroom tower (flat faces, it still reads as a round object), board-marked plaster, a V-shaped wash trough with brass taps, dark green locker cabinets built into three outer faces, a long locker wall with trailing pothos on top, two round felt phone booths, a built-in bench with small tables, a skylight above."),
        zone("Gym in de hoge hal (afsluitbaar)", "gym", R(24.0, 0.2, 31.4, 15.8),
             "De enige hoge ruimte (circa 110 m², 6 m hoog) is de gym: drie racks, een groepslesvloer, roeiers en een D-vormige douchetoren tegen de gymwand. Dichte wand tot het dak, deur op toegangspas vanuit de club en een eigen deur naar het terras.",
             ["Drie racks op zwevende platforms", "D-vormige douchetoren met vier douches tegen de gymwand", "Eigen ingang vanaf het terras op toegangspas", "Lichtkoepel, kentia en strelitzia"],
             cam=dict(t=[27.7, 8.0], afstand=9, hoek=180),
             prompt="A functional gym in the only high part (6 m) of a 1980s industrial building, closed off by a solid wall: three black power racks on oak platforms, a mat area, rowing machines, a D-shaped concrete-look shower tower against the wall with ivy on its rim, anthracite rubber floor, one wall oxblood red, a kentia palm, a skylight."),
        dict(zone("Verdieping: vergaderen en stil werken", "vergader", [[0.2, 0.2], [9.0, 0.2], [9.0, 26.7], [0.2, 26.7]],
                  "De kantoorverdieping: twee vergaderkamers voor zes, een kamer voor vier, vier belcellen en twee eilanden van vier bureaus.",
                  ["Vergaderkamers voor 6 (2x) en voor 4", "Vier belcellen", "Twee eilanden van vier bureaus"], n=1, cam=dict(t=[4.6, 13.0], afstand=9, hoek=0),
                  prompt="The upper office floor of an industrial building turned into meeting rooms and a quiet work floor: walls of reclaimed windows, oak tables for six, slate blue acoustic panels, compact sit-stand desks, round felt phone booths, plants."), tussenvloer=False),
        dict(zone("Verdieping: stille werkvloer boven het café", "werken", R(9.0, 0.2, 17.0, 15.8),
                  "Het deel van de verdieping boven het café: vier eilanden van vier bureaus, een sta-kamer, drie focuskamers en twee belcellen, met daglicht van een lichtkoepel.",
                  ["Vier eilanden van vier bureaus 140 x 70", "Sta-vergaderkamer voor 5", "Drie focuskamers van oude ramen", "Twee belcellen", "Kentia en dracaena, pothos boven de eilanden"], n=1,
                  cam=dict(t=[13.0, 7.0], afstand=9, hoek=180),
                  prompt="A quiet upper work floor in a 1980s industrial building: four islands of four compact sit-stand desks with oak tops, a standing meeting room with a round high table, three small glass focus rooms made from reclaimed windows, round felt phone booths, kentia palms, a skylight."), tussenvloer=False),
    ],
    buiten=[dict(naam="Terras en parkeren", poly=R(9.0, 16.0, 31.6, 26.9), kleur="#d5bd96"), dict(naam="Straat", poly=R(-6, 27, 38, 34), kleur="#9a958c")],
    elementen=[
        # café onder de kantoorvloer
        *keuken([12.8, 0.55], 6.4, 0), *kookeiland([12.8, 3.2], 0), *grote_tafel([12.8, 7.4], 4.2), *veelhoekbank([11.2, 12.4], 1.7, 6, open=(1,), draai=30),
        dict(t="box", soort="raambar", c=[15.0, 15.5], w=4.2, d=0.5, h=1.05, a=0, kleur=HOUT), deur([12.4, 16.0], 0, w=1.2), boom3([9.9, 15.0], "strelitzia nicolai"), boom3([16.2, 11.0], "ficus elastica"),
        plant3([9.7, 4.6], "kentia"), boom3([9.9, 9.6], "kentia"), plant3([16.4, 3.2], "monstera"), hangplant([10.6, 15.3], 2.8), hangplant([13.0, 15.3], 2.8), hangplant([11.4, 7.4], 2.8), hangplant([14.2, 7.4], 2.8), hangplant([12.8, 3.2], 2.8), hangplant([15.0, 15.2], 2.8),
        # werken in het kantoordeel
        *eiland2([2.3, 2.6], 90), *eiland2([6.9, 2.6], 90), *eiland2([2.3, 7.8], 90), *eiland2([6.9, 7.8], 90), *eiland2([2.3, 13.0], 90), *eiland2([6.9, 13.0], 90),
        *[hangplant([u, v], 2.6) for u in (2.3, 6.9) for v in (2.6, 7.8, 13.0)], plant3([4.6, 0.6], "zz-plant"), plant3([4.6, 15.4], "zz-plant"), boom3([0.9, 15.1], "kentia"),
        wand([[9.0, 0.2], [9.0, 6.6]], 3.0, bestaand=True), deur([9.0, 7.3], 90, w=1.2), wand([[9.0, 8.0], [9.0, 15.8]], 3.0, bestaand=True),
        # entree en toiletten
        dict(t="box", soort="toiletgroep", c=[2.8, 25.4], w=5.0, d=2.4, h=2.6, a=0, kleur="#bdb7aa"), label([2.8, 25.4], "toiletten"),
        dict(t="box", soort="trap", c=[7.6, 20.5], w=1.2, d=4.4, h=0.3, a=0, kleur=STAAL), dict(t="box", soort="garderobe", c=[1.0, 19.0], w=0.6, d=2.4, h=1.8, a=0, kleur=WALNOOT),
        deur([8.9, 18.0], 90), plant3([5.0, 17.0], "kentia"), *[dict(t="box", soort="fauteuil", c=[u, 18.4], w=0.8, d=0.8, h=0.8, a=180, kleur="#6f7d3a") for u in (3.6, 4.8)], plant3([1.0, 22.6], "aspidistra"), boom3([5.8, 23.3], "kentia"), plant3([1.0, 16.9], "zz-plant"), hangplant([4.4, 20.0], 2.6),
        # lage strook: wastoren, lockers, belcellen, zitnis
        *achthoektoren([20.5, 4.0], 2.75, 180, "was", lockers=(5, 6, 7)),
        *lockerwand([23.65, 11.9], 2.6, 90), pod2([18.0, 9.4]), pod2([18.0, 11.0]), plant3([23.4, 8.6], "zz-plant"), *zitnis([22.6, 15.75], [18.4, 15.75]),
        plant3([17.6, 0.8], "aspidistra"), boom3([20.4, 10.2], "kentia"), boom3([16.3, 6.4], "kentia"), hangplant([18.0, 10.2], 2.8), hangplant([21.8, 9.0], 2.8), hangplant([20.5, 13.2], 2.8), hangplant([19.4, 14.8], 2.8), hangplant([21.6, 14.8], 2.8),
        # gym in de hoge hal
        wand([[24.0, 0.2], [24.0, 13.6]], 6.5, gym=True), deur([24.0, 14.4], 90, toegang=True), wand([[24.0, 15.1], [24.0, 15.8]], 6.5, gym=True),
        deur([29.8, 16.0], 0, toegang=True), *dtoren([24.1, 5.4], [24.1, 0.6], 0.3, "douche"),
        *rack([30.0, 3.0], 90), *rack([30.0, 6.6], 90), *rack([30.0, 10.2], 90), dict(t="kleed", c=[26.6, 9.6], w=2.4, d=5.0, a=0, kleur="#c7928a"), label([26.6, 9.6], "groepsles"),
        roeier([27.0, 13.6], 0), roeier([27.0, 14.8], 0), dict(t="box", soort="kettlebells", c=[30.2, 12.6], w=2.0, d=0.5, h=0.9, a=0, kleur=STAAL),
        boom3([25.0, 15.0], "kentia"), boom3([30.9, 14.9], "strelitzia nicolai"), *groenwand([27.2, 0.25], [31.2, 0.25], 4.0),
        # verdieping: kantoordeel
        *vergaderkamer([3.0, 2.6], 5.4, 4.4, 0, 6, 1), *vergaderkamer([3.0, 7.3], 5.4, 4.2, 0, 6, 1), pod2([8.2, 2.0], 1), pod2([8.2, 3.7], 1),
        *eiland2([2.4, 12.6], 90, 1), *eiland2([6.9, 12.6], 90, 1), hangplant([2.4, 12.6], 2.6, 1), hangplant([6.9, 12.6], 2.6, 1), plant3([8.3, 9.6], "zz-plant", n=1), boom3([8.2, 6.4], "kentia", 1), plant3([0.8, 10.2], "zz-plant", n=1), plant3([8.4, 15.6], "sansevieria", n=1), hangplant([7.3, 18.0], 2.6, 1),
        *vergaderkamer([4.6, 21.4], 4.0, 3.8, 0, 4, 1), pod2([1.3, 25.3], 1), pod2([3.1, 25.3], 1), plant3([7.6, 25.6], "zz-plant", n=1), plant3([0.8, 17.0], "sansevieria", n=1),
        # verdieping: stille werkvloer boven het café
        *eiland2([11.0, 2.3], 0, 1), *eiland2([15.2, 2.3], 0, 1), *eiland2([11.0, 6.6], 0, 1), *eiland2([15.2, 6.6], 0, 1),
        *[hangplant([u, v], 2.6, 1) for u in (11.0, 15.2) for v in (2.3, 6.6)],
        *stavergaderkamer([11.0, 10.9], 3.2, 2.8, 0, 5, 1), *focuskamer([13.75, 10.9], 90, 1), boom3([15.8, 10.9], "kentia", 1), plant3([16.6, 13.2], "dracaena", n=1), hangplant([13.1, 13.0], 2.6, 1),
        *focuskamer([10.3, 14.8], 180, 1), *focuskamer([12.6, 14.8], 180, 1), pod2([14.6, 15.0], 1), pod2([16.2, 15.0], 1),
        # buiten
        *tafeltje([12.5, 19.0], 0, 4), *tafeltje([16.5, 19.0], 0, 4), dict(t="box", soort="plantenbak", c=[14.5, 21.8], w=10.0, d=0.6, h=0.6, a=0, kleur=WALNOOT),
        dict(t="box", soort="fietsenrek", c=[22.0, 25.8], w=6.0, d=1.2, h=1.0, a=0, kleur=STAAL), label([27.5, 21.5], "3 parkeerplaatsen"), boom([10.5, 25.5], 1.0, 3.5), boom([21.2, 21.8], 0.9, 3.0), *[boom3([u, 21.8], "olijf") for u in (11.0, 14.5, 18.0)],
    ],
    dak=dict(soort="pv", terras=None, groen=[], pv=[R(9.5, 0.8, 31.0, 15.2)], koepels=[[13.0, 8.0, 0.9], [20.5, 4.0, 0.8], [20.5, 11.5, 0.7], [27.5, 8.0, 0.9]],
             tekst="Zonnepanelen op de platte daken, met nieuwe lichtkoepels boven de stille werkvloer, de wastoren, de zitnis en de gym. Het kantoordeel houdt zijn dak.",
             tekst_en="Flat roofs of a 1980s building with solar panels and four new round skylights; a two-storey office part, a low single-storey strip and a higher hall of about 110 m2 at the far end, a small paved terrace with planters and three parking spaces in front."),
    renders=dict(buiten=[]),
)
ONTWERPEN.update({"rotterdam-galvanistraat-122": GALVANI, "schiedam-calandstraat-92": CALAND, "rotterdam-metaalhof-40": METAAL})
LABELS.update({
    "rotterdam-galvanistraat-122": {"Café, keuken en zittrap": [25.0, 11.5], "Werkzone onder de lichtstraten": [17.3, 0.9], "Vergaderen onder de entresol": [16.5, 10.9],
                                    "Torens en toiletten": [10.7, 6.0], "Gym (eigen ingang)": [4.4, 13.0], "Entresol: stille werkgalerij": [17.0, 10.9]},
    "schiedam-calandstraat-92": {"Café aan de straat": [9.0, 15.2], "Werkzone in de hal": [25.0, 5.0], "Vergaderen langs de oostgevel": [34.4, 4.9],
                                 "Entree en bieb": [37.0, 21.6], "Torens en toiletten": [15.0, 6.4], "Gym (afsluitbaar)": [6.0, 12.5], "Stille verdieping": [36.0, 21.0]},
    "rotterdam-metaalhof-40": {"Café onder de kantoorvloer": [13.0, 5.3], "Werken in het kantoordeel": [4.6, 5.2], "Entree en toiletten": [4.5, 21.0], "Wastoren, lockers en zitnis": [20.5, 7.9],
                               "Gym in de hoge hal (afsluitbaar)": [28.0, 12.0], "Verdieping: vergaderen en stil werken": [4.6, 17.6], "Verdieping: stille werkvloer boven het café": [13.0, 8.8]},
})
VIDES.update({"rotterdam-galvanistraat-122": [dict(naam="Vide boven werkzone en café", poly=R(13.6, 0.2, 29.1, 10.5), n=1)]})


# ---------------------------------------------------------------- Ronde 8 (15 november 2026): Linschotenstraat 20A, Rotterdam Spaanse Polder
# Unit 20A: de straatkant van een bouwstrook van 16 m breed in een complex met lichtstraten. u 0 = straatgevel (noordwest), u 31,2 = grens met de unit erachter,
# v 0 en v 16 zijn scheidingswanden met de buren (bedrijfsunits). Vrije hoogte 9 m. Werkgalerij op 3,6 m boven de torens.
LINSCHOTEN = dict(
    titel="Linschotenstraat 20A, Rotterdam Spaanse Polder",
    sub="Bedrijfsunit uit 2010 van 16 x 31 m en 9 m vrije hoogte, met lichtstraat en 5 eigen parkeerplaatsen, op 1,3 km van station Schiedam Centrum. Status eerst nabellen (online sinds 2022).",
    hoogte=10.0, niveaus={"1": 3.6}, pui_h=5.0,
    concept="Een lange, hoge strook die je van voor naar achter doorloopt, van druk naar stil naar zweet. Achter een nieuwe glazen straatgevel van 5 m hoog het café met keuken, "
            "lange tafel en ronde bank. Daarna de werkzone onder de lichtstraat, met een vergaderkamer en de trap naar de werkgalerij. Dan de twee ronde torens als buffer, "
            "met daarboven op 3,6 m de werkgalerij, en helemaal achterin de gym onder de volle hoogte. Sober: de bestaande hal blijft zichtbaar, de vloer wordt strak, de wanden "
            "van de vergaderkamers komen van oude ramen.",
    geluid="Gym helemaal achterin, tegen de bedrijfsunit erachter en 23 m van de straat. Tussen werken en gym de wastoren en de douchetoren (6 m buffer) en een dichte wand "
           "tot het dak. Naast en achter de unit zitten bedrijven, geen woningen. In een strook van 9 m hoog draagt geluid: houtwolplaten tegen de wanden en baffles onder het dak.",
    pui=[[[0.0, 0.5], [0.0, 15.5]]],
    zones=[
        zone("Café achter de glazen gevel", "café", R(0.2, 0.2, 9.0, 15.8),
             "Achter een nieuwe glazen straatgevel van 5 m hoog: een zitnis met drie tafeltjes langs het glas, een zeshoekige bank met twee open zijden rond de haard, de lockerwand langs de muur, de lange tafel en onder het leesbalkon de keuken met kookeiland. Kentia en strelitzia aan het glas.",
             ["Glazen straatgevel van hergebruikte stalen kozijnen", "Keuken van 6,4 m en kookeiland", "Lange tafel voor twaalf", "Ronde bank rond een sfeerhaard"],
             cam=dict(t=[4.6, 8.0], afstand=10, hoek=180),
             prompt="The café of a members club at the street end of a long, 9 m high industrial unit, behind a new 5 m high glass front made from reclaimed steel windows: an olive green kitchen from second-hand stainless steel worktables along the side wall, a reclaimed wood island, a long oak table for twelve, a round olive velvet sofa around a black fireplace, a tall tree, a long roof light above."),
        zone("Werkzone onder de lichtstraat", "werken", R(9.0, 0.2, 17.0, 15.8),
             "Zes eilanden van vier zit-sta bureaus onder de lichtstraat, een vergaderkamer voor acht van oude ramen en de stalen trap naar de werkgalerij.",
             ["Zes eilanden van vier bureaus 140 x 70", "Vergaderkamer voor acht", "Stalen trap naar de werkgalerij"],
             cam=dict(t=[13.0, 8.0], afstand=9, hoek=180),
             prompt="A coworking floor in a long, 9 m high industrial unit under a roof light: six islands of four compact sit-stand desks with oak tops, slate blue chairs, a meeting room with walls of reclaimed windows, a black steel stair to a gallery, wood wool acoustic panels on the walls."),
        zone("Torens en toiletten", "sanitair", R(17.0, 0.2, 23.0, 15.8), "De wastoren en de douchetoren, met daartussen de toiletgroep en daarboven de werkgalerij.",
             ["Wastoren 5,5 m, douchetoren 4,5 m (alleen vanuit de gym)", "Toiletgroep tussen de torens"], cam=dict(t=[20.0, 8.0], afstand=8, hoek=180),
             prompt="Two octagonal concrete-look bathroom towers (flat faces, they still read as round objects), 3 m high, standing under a timber gallery in a long industrial unit, board-marked plaster, a V-shaped wash trough with brass taps, ivy and ferns along the top rim, lockers built into an outer face."),
        zone("Gym (afsluitbaar)", "gym", R(23.0, 0.2, 31.0, 15.8), "Achterin onder de volle hoogte: drie racks, een groepslesvloer en roeiers, dichte wand en deur op toegangspas.",
             ["Drie racks op zwevende platforms", "Groepslesvloer", "Douchetoren vanuit de gym"], cam=dict(t=[27.0, 8.0], afstand=9, hoek=180),
             prompt="A functional gym at the back of a long, 9 m high industrial unit, closed off by a solid wall: three black power racks on oak platforms, a mat area, rowing machines, anthracite rubber floor, one wall oxblood red, a roof light above."),
        dict(zone("Leesbalkon", "bieb", R(2.0, 11.0, 9.0, 15.8),
                  "Een balkon van 34 m² op 3,6 m in de hoge voorkant, boven de keuken: boekenwand, leesstoel, twee glazen focuskamers en een belcel, met uitzicht door de glazen gevel.",
                  ["Twee focuskamers voor één of twee personen", "Boekenwand langs de muur", "Belcel en leesstoel"], n=1, cam=dict(t=[5.5, 13.4], afstand=7, hoek=180),
                  prompt="A small reading balcony 3.6 m up inside a 9 m high industrial unit, above an olive green kitchen: a walnut bookshelf wall, two small glass focus rooms made of reclaimed windows, a butter yellow armchair, a glass balustrade with pothos trailing down, view through a tall glass street facade."), tussenvloer=True),
        dict(zone("Werkgalerij", "werken", R(15.5, 0.2, 23.0, 15.8),
                  "Een nieuwe tussenvloer van 120 m² op 3,6 m boven de torens: vier eilanden van vier bureaus, een vergaderkamer voor zes en drie belcellen, met een glazen balustrade naar de werkzone.",
                  ["Vier eilanden van vier bureaus", "Vergaderkamer voor zes", "Drie belcellen"], n=1, cam=dict(t=[19.2, 8.0], afstand=8, hoek=180),
                  prompt="A steel and timber work gallery 3.6 m up in a 9 m high industrial unit: islands of compact sit-stand desks, a meeting room with reclaimed windows, round felt phone booths, a glass balustrade looking down on a coworking floor and café, a roof light above."), tussenvloer=True),
    ],
    buiten=[dict(naam="Parkeren en terras", poly=R(-6.0, 0.0, -0.2, 16.0), kleur="#c9c3b6"), dict(naam="Straat", poly=R(-14.0, -10, -6.0, 30), kleur="#9a958c")],
    elementen=[
        *keuken([4.7, 15.47], 6.4, 0), *kookeiland([4.7, 12.9], 0), *grote_tafel([4.6, 7.6], 4.2), *veelhoekbank([4.0, 3.6], 1.5, 6, open=(0, 3)), *lockerwand([3.2, 0.45], 5.6, 0), label([3.2, 1.1], "lockers"),
        boom3([1.3, 11.8], "kentia"), boom3([1.3, 3.8], "ficus elastica"), plant3([1.2, 14.6], "strelitzia nicolai"), plant3([7.9, 4.6], "monstera"), *zitnis([0.25, 9.6], [0.25, 5.2]), dict(t="box", soort="trap", c=[8.45, 9.0], w=1.1, d=4.4, h=0.3, a=0, kleur=STAAL), plant3([12.9, 3.6], "zz-plant"), plant3([12.9, 7.2], "zz-plant"), pod2([8.3, 1.1]), pod2([8.3, 2.8]), deur([0.0, 11.4], 90, w=1.6),
        *eiland2([10.8, 1.8], 0), *eiland2([15.0, 1.8], 0), *eiland2([10.8, 5.4], 0), *eiland2([15.0, 5.4], 0), *eiland2([10.8, 9.0], 0), *eiland2([15.0, 9.0], 0),
        *vergaderkamer([10.8, 13.2], 4.6, 3.0, 90, 6), *stavergaderkamer([13.5, 13.2], 2.4, 4.6, 0, 5), dict(t="box", soort="trap", c=[16.2, 13.4], w=1.1, d=4.4, h=0.3, a=0, kleur=STAAL), label([16.2, 10.9], "trap"),
        *toren([19.8, 4.0], 2.75, 180, "was"), *toren([20.2, 11.6], 2.25, 0, "douche"),
        dict(t="box", soort="toiletgroep", c=[20.0, 8.05], w=4.0, d=2.4, h=2.6, a=0, kleur="#bdb7aa"), label([20.0, 8.05], "toiletten"),
        wand([[23.0, 0.2], [23.0, 11.0]], 10.0, gym=True), wand([[23.0, 12.2], [23.0, 14.0]], 10.0, gym=True), deur([23.0, 14.7], 90, toegang=True), wand([[23.0, 15.4], [23.0, 15.8]], 10.0, gym=True),
        *rack([29.8, 3.0], 0), *rack([29.8, 6.6], 0), *rack([29.8, 10.2], 0), dict(t="kleed", c=[26.0, 7.0], w=2.6, d=6.5, a=0, kleur="#c7928a"),
        roeier([25.2, 14.4], 0), roeier([28.0, 14.4], 0), dict(t="box", soort="kettlebells", c=[30.4, 14.6], w=0.5, d=2.0, h=0.9, a=0, kleur=STAAL), *lockerwand([24.6, 0.45], 2.6, 0), plant3([30.4, 12.0], "sansevieria"),
        wand([[15.5, 0.2], [15.5, 13.6]], 1.1, glas=True, n=1),
        *eiland2([17.4, 2.0], 90, 1), *eiland2([21.0, 2.0], 90, 1), *eiland2([17.4, 6.0], 90, 1), *eiland2([21.0, 6.0], 90, 1),
        *vergaderkamer([18.6, 11.6], 4.4, 4.2, 0, 6, 1), pod2([22.3, 10.0], 1), pod2([22.3, 11.8], 1), pod2([22.3, 13.6], 1), plant3([17.0, 15.0], "zz-plant", 1), *[hangplant([15.3, v]) for v in (2.0, 5.0, 8.0, 11.0)], *[hangplant([u, 10.8]) for u in (3.0, 6.0)], wand([[2.0, 15.8], [2.0, 11.0], [7.85, 11.0]], 1.1, glas=True, n=1), *focuskamer([3.3, 13.6], 0, 1), *focuskamer([5.7, 13.6], 0, 1), *kasten(2.2, 8.8, 15.55, n=1, h=2.2, d=0.3), dict(t="box", soort="fauteuil", c=[7.6, 12.6], w=0.8, d=0.8, h=0.8, a=0, kleur="#47522a", n=1), pod2([8.3, 14.4], 1),
        *tafeltje([-2.5, 3.0], 0, 4), *tafeltje([-2.5, 7.0], 0, 2), label([-3.0, 12.5], "5 parkeerplaatsen"),
    ],
    dak=dict(soort="pv", terras=None, groen=[], pv=[R(0.8, 0.8, 30.4, 5.6), R(0.8, 10.4, 30.4, 15.2)],
             koepels=[[8.0, 8.0, 1.0], [13.0, 8.0, 1.0], [18.0, 8.0, 1.0], [27.0, 8.0, 1.0]],
             tekst="Bestaand zadeldak met een lange lichtstraat in het midden; zonnepanelen op de twee dakvlakken. Geen dakterras: het is een unit in een complex.",
             tekst_en="Existing long industrial roof of one bay in a row of identical bays, a long roof light along the ridge, solar panels on both sides; neighbouring bays stay plain grey, the street and a parking strip in front."),
    renders=dict(buiten=[]),
)
ONTWERPEN.update({"rotterdam-linschotenstraat-20a": LINSCHOTEN})
LABELS.update({"rotterdam-linschotenstraat-20a": {"Café achter de glazen gevel": [4.6, 10.4], "Werkzone onder de lichtstraat": [13.0, 10.9], "Torens en toiletten": [20.0, 6.6],
                                                  "Gym (afsluitbaar)": [26.5, 11.2], "Werkgalerij": [19.2, 8.4]}})


# ---------------------------------------------------------------- extra ontwerpen (één bestand per pand, parallel te bewerken)
import glob as _glob
for _f in sorted(_glob.glob(os.path.join(HERE, "ontwerpen_extra", "*.py"))):
    try:
        exec(compile(open(_f, encoding="utf-8").read(), _f, "exec"), globals())
    except Exception as _e:  # noqa: BLE001  een kapot extra ontwerp mag de rest niet stilleggen
        import sys as _sys
        print("WAARSCHUWING ontwerpen_extra", os.path.basename(_f), repr(_e), file=_sys.stderr)


# ---------------------------------------------------------------- inbouw uit het ontwerp, bottom-up (bovenop budget.py)
def inbouw_rows(slug, gym_m2):
    """Kosten die uit de v2-indeling volgen en niet al in budget.py zitten (excl. btw).
    budget.py dekt al: 1 vergaderinrichting, 25 m2 glazen wand, 2 belcellen, 1 lange werktafel voor 12, keuken 6 m + eiland."""
    E = ONTWERPEN[slug]["elementen"]
    R_ = []

    def add(post, h, e, p, label, gen=0.3, groep="Bouwkundig"):
        if h:
            R_.append(dict(groep=groep, post=post, h=round(h, 1), e=e, prijs=p, totaal=round(h * p), label=label, gen=gen))

    kamers = [e for e in E if e.get("soort") == "vergaderkamer"]
    extra = kamers[1:]
    wand_m2 = sum(2 * (k["w"] + k["d"]) * 2.6 for k in extra)
    add("Extra vergaderkamers: glazen wand (helft van de omtrek)", wand_m2 / 2, "m2", 320, "schatting")
    add("Extra vergaderkamers: dichte akoestische wand (andere helft)", wand_m2 / 2, "m2", 100, "schatting")
    add("Extra vergaderkamers: tafel, stoelen, scherm met camera en microfoon", len(extra), "st", 3_000, "schatting", groep="Werken")
    add("Extra belcellen zelfgebouwd", max(0, sum(1 for e in E if e.get("soort") == "belcel") - 2), "st", 2_500, "schatting", groep="Werken")
    tafels = [e for e in E if e.get("soort") == "grote tafel"]
    add("Extra grote tafel staal + hout", max(0, len(tafels) - 1), "st", 800, "schatting", groep="Werken")
    add("Stoelen extra grote tafels", sum(t["pers"] for t in tafels[1:]), "st", 120, "schatting", groep="Werken")
    gw = sum(math.dist(w["pts"][i], w["pts"][i + 1]) * w["h"] for w in E if w["t"] == "wand" and w.get("gym") and not w.get("bestaand")
             for i in range(len(w["pts"]) - 1))
    add("Gymwand akoestisch tot het dak (dubbel metal stud, 2 x 2 gips, wol)", gw, "m2", 110, "schatting")
    add("Deur met elektronisch slot en toegangslezer (koppeling met leden-app)", sum(1 for e in E if e["t"] == "deur" and e.get("toegang")), "st", 1_800, "schatting")
    add("Akoestische ondervloer onder het gymrubber", gym_m2, "m2", 18, "schatting", groep="Gym")
    add("Zwevend platform onder elk rack (hout op rubberdempers)", sum(1 for e in E if e.get("soort") == "rack"), "st", 450, "schatting", groep="Gym")
    add("Extra toiletgroep (2 toiletten + toegankelijk toilet, leidingwerk)", sum(1 for e in E if e.get("soort") == "toiletgroep"), "st", 14_000, "schatting", groep="Sanitair")
    tv = sum(poly_area(z["poly"]) for z in ONTWERPEN[slug]["zones"] if z.get("tussenvloer"))
    add("Nieuwe tussenvloer staal + hout, incl. trap en glazen balustrade", tv, "m2", 650, "schatting")
    gw_glas = sum(math.dist(w["pts"][i], w["pts"][i + 1]) * w["h"] for w in E if w["t"] == "wand" and w.get("glas") for i in range(len(w["pts"]) - 1))
    add("Glazen binnenwand (stille werkkamer, vergaderverdieping)", gw_glas, "m2", 320, "schatting")
    # inrichting v3 (16-11-2026): lockers, focuskamers, veelhoekbanken, zitnissen, groen, spel [schatting], zie inrichting/onderzoek.md
    lock = sum(int(e["w"] * 16) for e in E if e.get("soort") == "lockers")
    add("Lockers boven de 60 uit budget.py (kolommen van 30 cm, 5 hoog, met plantenbak erop)", max(0, lock - 60), "st", 70, "schatting", groep="Werken")
    add("Focuskamer van oude ramen in houten regelwerk, tafel, krukken, ventilator", sum(1 for e in E if e.get("soort") == "focuskamer"), "st", 3_500, "schatting", groep="Werken")
    hb = sum(e["w"] for e in E if e.get("soort") == "hexbank")
    add("Veelhoekige bank zelfgebouwd (hout, schuim, stof, rugleuning)", hb, "m1", 450, "schatting", groep="Café & bieb")
    add("Zitnis langs de wand met tafeltjes (hout, kussens)", sum(e["w"] for e in E if e.get("soort") == "zitnis"), "m1", 400, "schatting", groep="Café & bieb")
    rw = sum(e["w"] * e["h"] for e in E if e.get("soort") == "rotswand")
    add("Rotswand zonder water: steen op stalen frame met potnissen en geconserveerd mos (geen onderhoud)", rw, "m2", 350, "schatting", groep="Café & bieb")
    add("Klimwand: staalkabels, bakken en klimplanten", sum(e["w"] * e["h"] for e in E if e.get("soort") == "klimwand"), "m2", 60, "schatting", groep="Café & bieb")
    add("Tafeltennistafel (buiten: beton, binnen: inklapbaar)", sum(1 for e in E if e.get("soort") == "pingpong"), "st", 1_800, "schatting", groep="Café & bieb")
    PRIJS = {"kentia": 120, "ficus elastica": 200, "strelitzia nicolai": 250, "monstera": 90, "zz-plant": 45, "sansevieria": 40, "dracaena": 120,
             "schefflera": 150, "olijf": 400, "aspidistra": 40, "philodendron": 70, "pothos": 30, "klimop": 20, "varen": 25}
    planten = sum(PRIJS.get(e.get("naam"), 0) for e in E if e["t"] in ("plant", "boom")) + sum(30 for e in E if e.get("soort") in ("lockers",))
    add("Planten volgens plantplan, met zelfwatergevende bakken (boven de € 8.500 die al in budget.py zit)", max(0, planten * 1.6 - 8_500), "EUR", 1, "schatting", groep="Café & bieb")
    return R_


if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "ontwerp"), exist_ok=True)
    for s in ONTWERPEN:
        o = export(s)
        json.dump(o, open(os.path.join(HERE, "ontwerp", s + ".json"), "w"), ensure_ascii=False, indent=1)
        print(s, len(o["elementen"]), "elementen,", len(o["zones"]), "zones", sum(z["m2"] for z in o["zones"] if z.get("n", 0) == 0), "m2 begane grond")


# ---------------------------------------------------------------- dakterras (optie), bottom-up
def dakterras_rows(slug):
    """Kostenregels dakterras als optie, excl. btw. Leeg als er geen terras is ontworpen."""
    O = ONTWERPEN[slug]
    t = O["dak"].get("terras")
    if not t:
        return []
    m2 = poly_area(t)
    omtrek = sum(math.dist(t[i], t[(i + 1) % len(t)]) for i in range(len(t)))
    trap = 14_000 if slug == "den-bosch-rietveldenweg-13" else 22_000
    trap_post = ("Buitentrap staal vanaf het voorterrein" if trap == 14_000 else "Dakopening, dakopbouw en trap vanaf de verdieping")
    rows = [
        ("Constructeur: onderzoek en berekening dak", 1, "post", 3_500, "schatting"),
        ("Versterking dakconstructie (staalprofielen, aanname)", m2, "m2", 150, "aanname"),
        ("Dakbedekking en drukvaste isolatie onder het terras", m2, "m2", 85, "schatting"),
        ("Tegeldragers en houten vlonder (thermowood)", m2, "m2", 140, "schatting"),
        ("Balustrade staal met gaas, 1,1 m", omtrek, "m1", 300, "schatting"),
        (trap_post, 1, "post", trap, "schatting"),
        ("Pergola staal met klimplanten", 1, "post", 6_000, "schatting"),
        ("Plantenbakken en beplanting", 1, "post", 3_000, "schatting"),
    ]
    return [dict(groep="Bouwkundig", post="Dakterras: " + p, h=round(h, 1), e=e, prijs=pr, totaal=round(h * pr), label=l, gen=0.3) for p, h, e, pr, l in rows]
