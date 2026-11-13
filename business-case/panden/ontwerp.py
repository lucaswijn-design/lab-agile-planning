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
                "lots of plants and small trees, warm daylight. Colours from nature: {kleuren}. Photorealistic, natural light, no people in focus, no text.")


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
             prompt="A round concrete-look bathroom tower, 5.5 m diameter and 3 m high, board-marked plaster walls, a V-shaped concrete wash trough with brass taps on the open side, toilet cabins hidden behind the V wall, ivy and pothos hanging over the top rim, daylight falling in from a round skylight above."),
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
             prompt="A round concrete-look bathroom tower, 5.5 m diameter and 3 m high, standing free in a black-ceiling hall, board-marked plaster, a V-shaped concrete wash trough with brass taps, ivy hanging over the top rim."),
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
        if z["naam"] in LABELS.get(slug, {}):
            z["label"] = LABELS[slug][z["naam"]]
        if z["prompt"]:
            z["prompt_vol"] = z["prompt"] + " " + BASIS_PROMPT.format(kleuren=kleuren_tekst(z["palet"]))
        zs.append(z)
    out["zones"] = zs
    out["vides"] = VIDES.get(slug, [])
    out["palet"] = PALET
    return out


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
