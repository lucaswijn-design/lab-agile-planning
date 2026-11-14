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
             prompt="A round concrete-look bathroom tower, 5.5 m diameter and 3 m high, inside an old brick workshop, board-marked plaster, a V-shaped concrete wash trough with brass taps, ivy hanging over the rim, a skylight above."),
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
             prompt="A round concrete-look bathroom tower, 5.5 m diameter and 3 m high, standing free in a high steel hall, board-marked plaster, a V-shaped concrete wash trough with brass taps, ivy hanging over the rim, daylight from a skylight above."),
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


# ---------------------------------------------------------------- Utrecht v2
UTRECHT.update(
    concept="Je komt binnen via de poort, de steeg en de binnentuin, door de punt van het gebouw. Links het boekencafé met de keuken, "
            "een kookeiland met de espressomachine, een grote tafel voor twaalf en een ronde zitkuil rond de haard; daarachter de boekentoren. "
            "Rechts de werkzone met zes eilanden van vier compacte zit-sta bureaus. Achterin twee vergaderkamers waar eerst de studio was. "
            "De gym zit in de achtervleugel, achter de wastoren en de techniek: twee wanden en zes meter tussen sporten en werken, en een deur met toegangspas.",
    geluid="Gym in de achtervleugel, achter de wastoren en techniek: tussen de racks en de dichtstbijzijnde bureaus zit ruim 6 m en twee wanden. "
           "Dichte akoestische wand tot het dak met een deur op toegangspas. Vloer: 40 mm rubber op een akoestische ondervloer, platforms onder de racks.",
    zones=[
        zone("Entree in de punt", "entree", [[13.6, 10.2], [18.4, 15], [23, 10], [26, 10], [26, 8.2], [13.6, 8.2]],
             "De driehoekige punt die de binnentuin in steekt wordt de voordeur, met kluisjes en twee belcellen langs de rand.",
             ["Rond jute kleed, kapstokwand en kluisjes voor 60 leden", "Drie ronde belcellen in leisteenblauw vilt (een vierde naast de wastoren)",
              "Ledenbord en streepjeslijst", "Twee olijfbomen markeren de deur"], foto=8,
             prompt="Turn this old community-centre entrance into the welcoming front door of a members club. Replace the blue door with a large black steel and glass door, fresh lime-washed brick in warm sand tones, two olive trees in big clay pots, a rattan pendant, a small brass plaque instead of the old sign."),
        zone("Boekencafé en keuken", "café", R(0.3, 0.3, 13.6, 8.2),
             "Het hart: een keuken van 4,4 m met een kookeiland waar de espressomachine op staat, een grote tafel voor twaalf aan de pui, de ronde zitkuil rond de haard en een boekenwand van 7,6 m.",
             ["Keuken van 4,4 m: twee vaatwassers, combi-stoomoven, inductie, twee koelkasten", "Kookeiland van 2,6 m met de 3-groeps espressomachine, ook als bar",
              "Grote tafel van 4,2 m voor twaalf: lunch, samen werken, events", "Ronde bank rond de haard, open naar de tuin", "Boekenwand van 7,6 m met rolladder"],
             foto=12, cam=dict(t=[6.5, 4.2], afstand=11, hoek=210),
             prompt="Transform this empty room into the heart of a members club: an olive green kitchen along the back wall with a reclaimed wood island holding a three-group espresso machine, a 4 m long oak communal table for twelve along the glass facade, a round olive-green velvet sofa around a black freestanding fireplace, a walnut bookcase wall full of colourful books with a rolling ladder, big potted trees, the glass facade opening onto a wild courtyard garden."),
        zone("Stille bieb in de boekentoren", "bieb", R(0.3, 8.2, 5.4, 12.4),
             "Een ronde leeskamer van 3,7 m doorsnee, rondom boekenkasten, alleen fauteuils en stilte.",
             ["Ronde wand in diep olijf, walnoten kasten rondom", "Twee fauteuils, leeslamp, lichtkoepel"],
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
             prompt="A round concrete-look bathroom tower, 5.5 m diameter and 3 m high, board-marked plaster walls, a V-shaped concrete wash trough with brass taps on the open side, toilet cabins hidden behind the V wall, ivy and pothos hanging over the top rim, daylight from a round skylight above."),
        zone("Gym (afsluitbaar)", "gym", [[26, 10], [36, 10], [36, 25.4], [34.5, 25.4], [27.2, 22.5], [27.2, 20.4], [26, 20.4]],
             "De achtervleugel wordt de gym: vier racks op platforms, roeiers bij het glas naar de tuin, een vloer voor groepslessen en yoga, de douchetoren in de hoek. Afgesloten met een deur op toegangspas.",
             ["Vier racks op zwevende platforms, 40 mm rubber op akoestische ondervloer", "Drie roeiers met uitzicht op de tuin",
              "Vloer van 4 x 3 m voor groepslessen en yoga", "Douchetoren van 4,5 m doorsnee", "Deur met toegangslezer, gym apart af te sluiten"],
             foto=10, cam=dict(t=[31, 17], afstand=12, hoek=230),
             prompt="Turn this wing into a functional strength gym: four black power racks on oak lifting platforms, anthracite rubber floor, one wall in oxblood red lime paint, rowing machines facing the garden, a mat area for classes, kettlebells on a steel rack, large green plants, glass doors opening to a wild garden."),
    ],
    elementen=[
        dict(t="kleed", c=[18.6, 11.0], r=1.6, kleur="#d5bd96"), boom([17.2, 13.4], 0.7, 2.4), boom([19.8, 13.4], 0.7, 2.4),
        pod2([19.8, 9.1]), pod2([21.6, 9.1]), pod2([23.4, 9.1]), pod2([32.9, 5.6]), dict(t="box", soort="kluisjes", c=[15.6, 8.55], w=3.0, d=0.5, h=2.0, a=0, kleur="#6e4f38"),
        dict(t="box", soort="bank", c=[25.1, 9.1], w=1.4, d=0.6, h=0.45, a=90, kleur="#5a3a22"),
        *kasten(0.6, 8.2, 0.55), *keuken([11.0, 0.65], 4.4), *kookeiland([11.0, 2.8]),
        *zitkuil([4.4, 4.3], 2.0, 90, "#6f7d3a", "#d9ccb0"), *grote_tafel([10.4, 6.5], 4.2),
        *tafeltje([1.2, 6.9]), boom([7.4, 7.2], 0.6, 2.4), plant([0.9, 1.5]), plant([13.0, 7.7]),
        dict(t="box", soort="fauteuil", c=[7.6, 1.7], w=0.85, d=0.85, h=0.8, a=20, kleur="#5a2741"),
        *boekentoren([2.8, 10.3], 1.85, 270),
        *eiland2([15.6, 1.9], -4), *eiland2([19.6, 1.9], 3), *eiland2([23.6, 1.9], -3),
        *eiland2([15.6, 6.2], 4), *eiland2([19.6, 6.2], -3), *eiland2([23.6, 6.2], 5),
        plant([13.95, 4.05], 0.35, 1.4), plant([25.6, 4.05], 0.35, 1.4),
        *vergaderkamer([28.7, 2.45], 4.8, 4.1, 0, 8), *vergaderkamer([33.6, 2.45], 4.6, 4.1, 0, 6),
        *toren([29.2, 7.3], 2.75, 180, "was"), dict(t="box", soort="techniek", c=[34.7, 7.3], w=2.0, d=3.4, h=2.6, a=0, kleur="#8f8a80"),
        wand([[27.2, 10.0], [36, 10.0]], 3.5, gym=True), deur([26.7, 10.0], 0, toegang=True),
        *toren([33.4, 12.7], 2.25, 180, "douche"),
        *rack([34.8, 16.8], 90), *rack([34.8, 19.6], 90), *rack([34.8, 22.4], 90), *rack([30.2, 21.0], 0),
        roeier([27.3, 12.0], 90), roeier([27.3, 14.2], 90), roeier([27.3, 16.4], 90),
        dict(t="box", soort="halterrek", c=[30.2, 10.6], w=2.0, d=0.5, h=0.9, a=0, kleur=STAAL),
        dict(t="kleed", c=[30.6, 16.6], w=4.0, d=3.0, a=0, kleur="#c7928a"), plant([27.8, 19.4]),
        label([30.6, 16.6], "groepsles en yoga"),
        *tafeltje([7.2, 10.4], stoelen=3), *tafeltje([10.4, 10.2], stoelen=3), *tafeltje([8.8, 12.8], stoelen=3),
        dict(t="boog", soort="bank", c=[19.0, 19.0], r=2.2, a0=200, a1=340, d=0.5, h=0.45, kleur=HOUT),
        dict(t="ring", soort="pergola", c=[19.0, 19.0], r=2.6, open=90, gat=0, h=2.6, kleur="#2f3032", dun=True),
        boom([3, 19]), boom([10, 20]), boom([24, 19]), boom([14, 18]), boom([3.4, 14.4], 0.9, 2.6),
    ],
)

# ---------------------------------------------------------------- Rietveldenweg v2
_RV_O = 39.2  # oostgevel loopt schuin: u = 39,2 - (v - 13,2) x 0,279
RIETVELDEN.update(
    concept="Achter de showroomramen het boekencafé met een grote tafel, de zitkuil in een halfronde boekenwand en een open keuken met kookeiland. "
            "Achter het café, rustig en weg van de straat, de werkzone met 24 bureaus, met daarnaast een stille werkkamer met belcellen. "
            "De gym zit in het oostelijke deel, achter een dichte wand met keuken en techniek als buffer naar het café, en kleedruimte als buffer naar "
            "de vergaderkamers. Achterin de boekentoren. Het platte dak boven het café kan een dakterras worden.",
    geluid="De gym ligt tegen de oostgevel. Naar het café zit er een keuken en techniekstrook van 4 m tussen, naar de vergaderkamers een kleedruimte van 3 m. "
           "De werkzone raakt de gym nergens. Dichte akoestische wanden tot het dak, deur op toegangspas, 40 mm rubber op akoestische ondervloer en platforms.",
    zones=[
        zone("Boekencafé achter de showroomramen", "café", R(7.3, 0.3, 19.8, 12.6),
             "Achter 11 meter showroomglas het café, zichtbaar vanaf de straat: halfronde boekenwand om de zitkuil, leesplekken langs het glas en een grote tafel voor twaalf.",
             ["Halfronde boekenwand van 7,2 m doorsnee in walnoot", "Ronde bank in olijfgroen fluweel rond een sfeerhaard",
              "Grote tafel van 4,2 m voor twaalf", "Leesfauteuils langs de ramen; houten vloer en zwarte plafonds blijven"],
             foto=5, cam=dict(t=[13.6, 6.2], afstand=13, hoek=200),
             prompt="Transform this former showroom into a members-club book café: keep the oak floor, black ceiling, grey columns and the natural stone wall. Add a semicircular freestanding walnut bookcase full of books wrapping a round olive-green velvet sofa around a black freestanding fireplace, a long oak communal table for twelve, plum velvet armchairs along the big shop windows, large potted fig and olive trees."),
        zone("Keuken en espresso-eiland", "café", R(19.8, 0.3, 23.8, 8.0),
             "Een open keuken van 6,6 m tegen de gymwand, met een kookeiland waar de espressomachine en de streepjeslijst staan.",
             ["Keuken van 6,6 m: twee vaatwassers, combi-stoomoven, inductie, twee koelkasten", "Kookeiland van 2,6 m met 3-groeps machine",
              "De natuurstenen balie wordt hergebruikt als blad van het eiland", "Dichte wand naar de gym in de rug"],
             foto=7, cam=dict(t=[21.6, 4.0], afstand=7, hoek=200),
             prompt="Keep the natural stone and turn this corner into an open members-club kitchen: a long olive green kitchen against the back wall with open shelves, a kitchen island clad in the existing natural stone with a travertine top and a polished three-group espresso machine, brass pendants, cognac leather stools, a chalkboard tally list."),
        zone("Techniek", "techniek", R(19.8, 8.0, 23.8, 12.6), "Warmtepomp, batterij, meterkast en opslag: buffer tussen café en gym.", []),
        zone("Gym (afsluitbaar)", "gym", [[24.0, 0.3], [42.5, 0.3], [41.6, 3.3], [39.3, 12.6], [24.0, 12.6]],
             "Het oostelijke deel wordt de gym: vijf racks langs de lange wand, een sledebaan van 12 m, roeiers en de douchetoren. Eigen deur op toegangspas.",
             ["Vijf racks op zwevende platforms", "Sledebaan van kunstgras van 12 m", "Douchetoren van 4,3 m doorsnee",
              "40 mm rubber op akoestische ondervloer", "Dichte akoestische wanden tot het dak"],
             foto=9, cam=dict(t=[31, 6.4], afstand=14, hoek=200),
             prompt="Turn this large black-ceiling hall into a functional strength gym: five black power racks on oak platforms along the wall, a 12 m artificial turf sled track, anthracite rubber floor, rowing machines, one wall in oxblood red, a round concrete-look shower tower with plants on its rim, big plants."),
        zone("Kleedruimte en lockers", "sanitair", [[29.2, 12.8], [39.3, 12.8], [38.5, 15.8], [29.2, 15.8]],
             "Lockers en banken tussen gym en vergaderkamers: buffer en omkleedruimte.", ["60 lockers, eiken banken, haken"]),
        zone("Vergaderkamers", "vergader", [[29.2, 15.8], [38.5, 15.8], [36.6, 22.6], [29.2, 22.6]],
             "Een vergaderkamer voor acht en een voor vier, achter de kleedruimte.",
             ["Vergaderkamer voor 8 (25 m²) en voor 4 (12 m²)", "Scherm met camera, akoestische panelen"], cam=dict(t=[33, 19.2], afstand=9, hoek=200),
             prompt="Two meeting rooms behind black steel and glass in a hall with black ceilings: an oak table for eight and a small one for four, slate-blue acoustic panels, a screen with camera, plants."),
        zone("Bieb", "bieb", [[29.2, 22.6], [36.6, 22.6], [35.4, 26.8], [29.2, 26.8]], "De ronde boekentoren in de stille achterhoek.",
             ["Boekentoren van 3,4 m doorsnee"], cam=dict(t=[32.2, 24.6], afstand=7, hoek=200),
             prompt="A round reading room lined with walnut bookshelves, deep olive walls, two olive armchairs and a reading lamp, in the quiet back corner of a hall with black ceilings."),
        zone("Wastoren", "sanitair", R(22, 13, 29.2, 19), "De wastoren midden in de hal, open naar de werkzone.", ["Wastrog langs de V, drie toiletten"],
             cam=dict(t=[25.6, 16], afstand=8, hoek=200),
             prompt="A round concrete-look bathroom tower, 5.5 m diameter and 3 m high, standing free in a black-ceiling hall, board-marked plaster, a V-shaped concrete wash trough with brass taps, ivy hanging over the top rim."),
        zone("Stille werkkamer", "werken", R(22, 19.2, 29.2, 25.8),
             "Achter glas: vier bureaus voor wie echt stil wil werken, en twee belcellen.", ["Eén eiland van vier bureaus", "Twee ronde belcellen", "Glazen wand naar de werkzone"],
             foto=12, cam=dict(t=[25.6, 22.4], afstand=8, hoek=200),
             prompt="A quiet glass-walled work room in a hall with black ceiling: one island of four compact sit-stand desks, two round slate-blue felt phone booths, plants, soft warm light."),
        zone("Werkzone", "werken", R(7.3, 12.8, 22, 25.6),
             "Vierentwintig compacte zit-sta bureaus in zes eilanden, met een loungehoek en drie belcellen, rustig achter het café.",
             ["Zes eilanden van vier zit-sta bureaus 140 x 70", "Looppaden van 1,2 m", "Drie ronde belcellen en een loungebank",
              "Totaal met grote tafel en stille kamer: 40 werkplekken"], foto=8, cam=dict(t=[14.6, 18.6], afstand=12, hoek=210),
             prompt="Turn this long hall with black walls and ceiling into a calm coworking space: six islands of four compact sit-stand desks with oak tops, each slightly rotated, dual monitors, three round slate-blue felt phone booths, a lounge sofa, slate-blue acoustic panels, many plants, keep the wooden floor."),
        zone("Bedrijfswoning (verhuur)", "verhuur", R(0.1, 13.6, 7, 26), "Blijft woning, wordt verhuurd.", []),
    ],
    elementen=[
        dict(t="boog", soort="kast", c=[13.6, 6.2], r=3.6, a0=-80, a1=80, d=0.4, h=2.2, kleur=WALNOOT),
        *zitkuil([13.6, 6.2], 2.3, 180, "#6f7d3a", "#d9ccb0"), *grote_tafel([15.6, 11.3], 4.2),
        *[dict(t="box", soort="fauteuil", c=[8.2, v], w=0.85, d=0.85, h=0.8, a=0, kleur="#5a2741") for v in (2.4, 5.0, 9.6)],
        plant([7.9, 3.7]), plant([7.9, 7.4]), plant([7.9, 11.6]), boom([10.6, 11.0], 1.0, 3.0),
        *tafeltje([18.4, 2.4]), *tafeltje([18.4, 5.0]),
        *[dict(t="cil", soort="kolom", c=[8.7, v], r=0.2, h=4.6, kleur="#9a9890") for v in (3.0, 7.0, 11.0)],
        *keuken([23.45, 4.1], 6.6, 90), *kookeiland([21.4, 4.1], 90),
        dict(t="box", soort="techniek", c=[21.8, 10.3], w=3.6, d=4.2, h=2.6, a=0, kleur="#8f8a80"),
        wand([[24.0, 0.3], [24.0, 12.6]], 4.6, gym=True), wand([[24.0, 12.7], [30.0, 12.7]], 4.6, gym=True), wand([[31.0, 12.7], [39.3, 12.7]], 4.6, gym=True),
        deur([30.5, 12.7], 0, toegang=True),
        *rack([26.2, 1.6], 0), *rack([29.2, 1.6], 0), *rack([32.2, 1.6], 0), *rack([35.2, 1.6], 0), *rack([38.2, 1.6], 0),
        dict(t="box", soort="sledebaan", c=[31.0, 5.6], w=12, d=1.6, h=0.02, a=0, kleur="#5f7a3a"),
        roeier([26.4, 8.6], 0), roeier([26.4, 10.2], 0), roeier([26.4, 11.8], 0),
        dict(t="kleed", c=[30.0, 10.2], w=3.6, d=3.0, a=0, kleur="#c7928a"), *toren([35.6, 9.6], 2.15, 180, "douche"),
        dict(t="box", soort="kluisjes", c=[34.0, 15.45], w=8.0, d=0.5, h=2.0, a=0, kleur="#6e4f38"),
        dict(t="box", soort="bank", c=[34.0, 14.2], w=6.0, d=0.4, h=0.45, a=0, kleur=HOUT),
        *vergaderkamer([31.6, 19.2], 4.6, 5.4, 0, 8), *vergaderkamer([35.3, 18.4], 4.6, 2.4, 90, 4),
        *boekentoren([32.2, 24.6], 1.7, 180),
        *toren([25.6, 16.0], 2.75, 180, "was"),
        wand([[22.0, 19.2], [22.0, 25.6]], 3.0, glas=True), wand([[22.0, 19.15], [27.0, 19.15]], 3.0, glas=True), deur([27.6, 19.15], 0),
        *eiland2([24.4, 21.6], 0), pod2([27.8, 21.0]), pod2([27.8, 23.4]), plant([23.0, 24.8]),
        *eiland2([10.0, 14.9], -4), *eiland2([14.1, 14.9], 3), *eiland2([18.2, 14.9], -3),
        *eiland2([10.0, 19.2], 4), *eiland2([14.1, 19.2], -3), *eiland2([18.2, 19.2], 4),
        pod2([8.6, 24.4]), pod2([10.6, 24.6]), pod2([12.6, 24.4]),
        dict(t="box", soort="bank", c=[17.2, 24.5], w=2.6, d=0.9, h=0.75, a=0, kleur="#44606f"), *tafeltje([17.2, 23.0], stoelen=0),
        plant([21.2, 23.4], 0.5, 1.6), plant([8.0, 13.6]), plant([20.6, 17.0], 0.4, 1.4),
        *tafeltje([3.0, 3.0], stoelen=3), *tafeltje([3.0, 6.6], stoelen=3), *tafeltje([3.0, 10.2], stoelen=3),
        *[dict(t="box", soort="plantenbak", c=[1.0, v], w=0.5, d=2.4, h=0.6, a=0, kleur="#5a3a22") for v in (2.4, 6.6, 10.8)],
        boom([-0.4, 1.5]), boom([-0.4, 12.0]),
    ],
)
RIETVELDEN["dak"]["koepels"] = [[25.6, 16.0, 0.9], [35.6, 9.6, 0.8], [32.2, 24.6, 0.7]]

# ---------------------------------------------------------------- Eendenkooi v2
EENDENKOOI.update(
    concept="De gym hoeft niet gebouwd te worden: de sportzaal is er al, met eigen wanden en een deur op toegangspas. Bij de entree het boekencafé "
            "met de gebogen balie als espressobar, een keuken met kookeiland, de zitkuil en de boekentoren. Boven de hele verdieping als werkzone: "
            "32 bureaus en een raambar met uitzicht over het groen, plus twee vergaderkamers. De verdieping ligt boven café en kleedkamers, niet boven de gym.",
    geluid="De sportzaal is een eigen bouwdeel van bijna 8 m hoog met een bestaande wand naar het café. De werkverdieping ligt boven café, studio en "
           "kleedkamers, niet boven de gym. Deur op toegangspas, rubber op akoestische ondervloer en platforms bij de racks.",
    zones=[
        zone("Gym in de sportzaal (afsluitbaar)", "gym", R(0.3, 0.3, 17.5, 18.1),
             "De bestaande sportzaal: zes racks langs de achterwand, een sledebaan van 15 m, een vloer voor groepslessen. Eigen deur op toegangspas.",
             ["Zes racks op zwevende platforms", "Sledebaan van 15 m", "Groepslesvloer van 9 x 6 m", "Bokszakken blijven", "Deur met toegangslezer"],
             foto=4, cam=dict(t=[9, 9], afstand=16, hoek=210),
             prompt="Transform this dark sports hall into a beautiful functional gym: six black power racks on oak platforms along the back wall, a 15 m artificial turf sled track, a mat area for classes, keep the punching bags, anthracite rubber floor, one wall in oxblood red, the rest warm white, large trees in big pots, warm industrial pendant lights."),
        zone("Boekencafé en keuken", "café", R(17.7, 0.3, 30.4, 10),
             "Bij binnenkomst de gebogen espressobar, daarachter een keuken van 5,6 m met kookeiland, de zitkuil voor de ramen, de boekentoren en een boekenwand naar de studio.",
             ["Gebogen balie als espressobar", "Keuken van 5,6 m met kookeiland", "Ronde bank rond een sfeerhaard", "Raambar van 4,8 m met acht krukken voor lunch", "Boekenwand van 6 m"],
             foto=5, cam=dict(t=[24, 5], afstand=12, hoek=200),
             prompt="Transform this white gym reception into a warm book café: wrap the curved counter in reclaimed wood with a travertine top and a three-group espresso machine, an olive green kitchen with an island behind it, replace red walls with pistachio green lime-wash, a round olive velvet sofa around a black freestanding fireplace in front of the windows, a walnut bookcase wall, plants."),
        zone("Studio (bestaande dansstudio)", "studio", R(17.7, 10, 30.4, 16.9), "De dansstudio blijft, voor yoga en events.",
             ["Houten vloer blijft", "Vijgenpaarse gordijnen"], foto=10, cam=dict(t=[24, 13.4], afstand=9, hoek=200),
             prompt="Keep this wooden-floor dance studio and make it warmer: fig-purple curtains, terracotta rug corner with cushions, plants on the window sills, warm dimmable light."),
        zone("Kleedkamers met V-wastrog", "sanitair", R(30.6, 0.3, 37.2, 14.6),
             "De kleedkamers blijven, met microcement en een V-vormige wastrog in het midden.", ["Microcement in plaats van tegels", "V-wastrog met messing kranen"],
             foto=11, cam=dict(t=[33.9, 7.4], afstand=8, hoek=200),
             prompt="Renovate this tiled changing room: replace all tiles with warm grey microcement and board-marked plaster, a V-shaped concrete wash trough with brass taps in the middle, oak benches and black hooks, ivy and ferns."),
        zone("Verdieping: werkzone", "werken", R(17.7, 0.3, 31.0, 14.6),
             "Acht eilanden van vier compacte zit-sta bureaus en een raambar langs de ramen: 39 werkplekken met uitzicht over het water en het groen.",
             ["Acht eilanden van vier bureaus 140 x 70", "Raambar van 4,2 m met krukken", "Looppaden van 1,2 tot 1,6 m"], foto=8, n=1,
             cam=dict(t=[24.4, 7.4], afstand=13, hoek=200),
             prompt="Turn this white space with columns and windows into a calm coworking floor: eight islands of four compact sit-stand desks with oak tops slightly rotated, dual monitors, a window bar with stools facing the green view, slate-blue acoustic baffles, plants everywhere."),
        zone("Verdieping: vergaderkamers", "vergader", R(31.0, 0.3, 37.2, 14.6),
             "Een vergaderkamer voor acht, een voor zes en vier belcellen.", ["Vergaderkamer voor 8 en voor 6", "Vier ronde belcellen"], n=1,
             cam=dict(t=[34.1, 7.0], afstand=9, hoek=200),
             prompt="Two meeting rooms behind black steel and glass on an upper floor: an oak table for eight and one for six, slate-blue acoustic panels, a screen with camera, plants, daylight from the windows."),
    ],
    elementen=[
        *rack([2.2, 16.6], 0), *rack([5.0, 16.6], 0), *rack([7.8, 16.6], 0), *rack([10.6, 16.6], 0), *rack([13.4, 16.6], 0), *rack([16.0, 16.6], 0),
        dict(t="box", soort="sledebaan", c=[8.6, 1.6], w=15, d=1.6, h=0.02, a=0, kleur="#5f7a3a"),
        roeier([1.4, 6.0], 90), roeier([1.4, 8.6], 90), roeier([1.4, 11.2], 90),
        *[dict(t="cil", soort="bokszak", c=[x, 9.0], r=0.2, h=1.2, z=1.0, kleur="#3a3b3d") for x in (10, 12, 14)],
        dict(t="kleed", c=[9.0, 9.4], w=9, d=6, a=0, kleur="#c7928a"), label([9.0, 7.0], "groepsles"),
        dict(t="box", soort="halterrek", c=[9.0, 13.9], w=4.0, d=0.6, h=0.9, a=0, kleur=STAAL),
        boom([1.6, 1.8], 1.2, 4.2), boom([16.0, 12.6], 1.2, 4.2),
        wand([[17.6, 0.3], [17.6, 7.9]], 7.8, gym=True, bestaand=True), wand([[17.6, 9.1], [17.6, 18.1]], 7.8, gym=True, bestaand=True),
        deur([17.6, 8.5], 90, toegang=True),
        dict(t="boog", soort="bar", c=[19.4, 3.4], r=1.9, a0=-90, a1=90, d=0.7, h=1.1, kleur=HOUT),
        *keuken([29.77, 3.6], 5.6, 90), *kookeiland([27.9, 3.6], 90),
        *zitkuil([24.4, 5.6], 2.0, 270, "#6f7d3a", "#d9ccb0"), *boekentoren([20.4, 7.9], 1.8, 0),
        *kasten(23.4, 29.4, 9.7), *tafeltje([28.6, 8.0]), boom([22.6, 1.2], 0.6, 2.4),
        dict(t="box", soort="raambar", c=[25.2, 0.6], w=4.8, d=0.5, h=1.05, a=0, kleur=HOUT),
        dict(t="kleed", c=[24.0, 13.4], w=5, d=3, a=0, kleur="#b8633f"),
        dict(t="boog", soort="gordijn", c=[24.0, 16.2], r=5.6, a0=240, a1=300, d=0.08, h=3.2, kleur="#4b2339"),
        dict(t="v", c=[33.9, 7.4], arm=2.2, hoek=40, open=180, h=1.2),
        *[dict(t="box", soort="bank", c=[36.6, v], w=0.4, d=3.0, h=0.45, a=0, kleur=HOUT) for v in (3, 11.5)],
        *[dict(t="box", soort="douchewand", c=[31.6 + i * 1.4, 0.9], w=0.08, d=1.2, h=2.1, a=0, kleur="#c9c3b6") for i in range(4)],
        *[dict(t="box", soort="douchewand", c=[31.6 + i * 1.4, 13.9], w=0.08, d=1.2, h=2.1, a=0, kleur="#c9c3b6") for i in range(4)],
        dict(t="box", soort="trap", c=[18.8, 13.6], w=1.2, d=3.4, h=0.3, a=0, kleur="#cfc8ba"),
        dict(t="box", soort="trap", c=[18.8, 13.6], w=1.2, d=3.4, h=0.3, a=0, kleur="#cfc8ba", n=1),
        dict(t="box", soort="raambar", c=[24.4, 0.7], w=4.2, d=0.5, h=1.05, a=0, kleur=HOUT, n=1),
        *eiland2([20.0, 4.0], -4, 1), *eiland2([24.0, 4.0], 3, 1), *eiland2([28.0, 4.0], -3, 1),
        *eiland2([20.0, 8.2], 4, 1), *eiland2([24.0, 8.2], -3, 1), *eiland2([28.0, 8.2], 4, 1),
        *eiland2([24.0, 12.4], -3, 1), *eiland2([28.0, 12.4], 3, 1),
        plant([30.4, 6.1], 0.4, 1.4, 1), plant([21.0, 12.6], 0.4, 1.4, 1),
        *vergaderkamer([34.1, 4.0], 5.8, 4.4, 0, 8, 1), *vergaderkamer([34.1, 9.4], 5.8, 3.6, 0, 6, 1),
        pod2([32.2, 13.3], 1), pod2([34.4, 13.3], 1), pod2([36.4, 13.3], 1), pod2([30.2, 1.4], 1),
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
             prompt="Turn this high workshop part with glazed doors into the entrance of a members club with a round concrete-look bathroom tower standing in the space: board-marked plaster, a V-shaped wash trough with brass taps, black steel and glass doors, a black steel stair to a mezzanine, lockers in old school furniture, olive trees in clay pots."),
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
            "In de hal uit 1970 zit de gym aan de westkant achter een dichte wand tot het dak. Daarnaast een bufferstrook met de vergaderkamer, de belcellen en de twee "
            "torens, met daarboven een vergaderbalkon op een tussenvloer, en aan de oostkant, bij de glazen deuren naar de weilanden, de werkzone met twintig bureaus en een raambar.",
    geluid="De hal is één ruimte van 7 m hoog, dus de gym krijgt een dichte akoestische wand tot het dak. Tussen gym en werkzone zit een strook van 5,6 m met "
           "vergaderkamer, belcellen en de torens. De douchetoren is alleen vanuit de gym bereikbaar. Gym met eigen deur op toegangspas naar de binnenplaats.",
    zones=[
        zone("Boekencafé en keuken in het voorhuis", "café", [[0.3, 0.3], [11.6, 0.3], [11.6, 2.9], [12.4, 2.9], [14.4, 5.0], [14.5, 7.0], [12.0, 9.1], [5.1, 9.1], [5.1, 11.7], [2.8, 11.7], [2.8, 7.7], [0.3, 7.7]],
             "Het woonhuis uit 1931: keuken langs de zijmuur met een kookeiland, een grote tafel voor tien in het midden en een ronde bank in de ronde erker.",
             ["Keuken van 6,4 m met kookeiland en 3-groeps machine", "Grote tafel van 3,5 m voor tien", "Ronde bank die de ronde erker volgt",
              "Originele details uit 1931 blijven", "Glazen tuindeuren naar de binnenplaats"], cam=dict(t=[7, 4.8], afstand=9, hoek=210),
             prompt="A 1930s Dutch brick house turned into the book café of a members club: an olive green kitchen along the side wall with a reclaimed wood island and a three-group espresso machine, a long oak table for ten, a curved olive-green velvet sofa following a round bay window around a black freestanding fireplace, original 1930s doors and mouldings, glass garden doors, plants."),
        zone("Stille bieb op zolder", "bieb", R(0.6, 0.6, 11.4, 7.4),
             "Onder de kap: de stille bieb met lage kasten, fauteuils en dakramen.", ["Lage boekenkasten onder de schuine kap", "Fauteuils in olijf"], n=1,
             cam=dict(t=[6, 4], afstand=8, hoek=210),
             prompt="A quiet attic library under a pitched roof with exposed timber rafters: low walnut bookcases under the slopes, deep olive walls, olive velvet armchairs, butter-yellow lamps, roof windows."),
        zone("Gym (afsluitbaar)", "gym", R(-14.6, 16.4, -6.8, 35.7),
             "De westkant van de hal: vier racks langs de lange wand, roeiers, een vloer voor groepslessen en yoga. Dichte wand tot het dak, eigen deur op toegangspas.",
             ["Vier racks op zwevende platforms", "Groepslesvloer van 5 x 4 m", "Douchetoren alleen vanuit de gym", "Deur met toegangslezer naar de binnenplaats"],
             cam=dict(t=[-10.6, 26], afstand=12, hoek=210),
             prompt="A functional gym inside a 7 m high 1970s steel hall, closed off by a solid wall: four black power racks on oak platforms along the long wall, rowing machines, a mat area for classes, anthracite rubber floor, one wall oxblood red, big plants, daylight from high windows."),
        zone("Vergaderkamer en belcellen", "vergader", R(-6.6, 16.4, -1.0, 23.2),
             "In de bufferstrook: een vergaderkamer voor acht en twee belcellen.", ["Vergaderkamer voor 8 (23 m²)", "Twee ronde belcellen"],
             cam=dict(t=[-3.8, 19.6], afstand=8, hoek=210),
             prompt="A meeting room for eight inside a high steel hall, behind black steel and glass, an oak table, slate-blue acoustic panels, a screen with camera, two round felt phone booths next to it."),
        dict(zone("Vergaderbalkon op de tussenvloer", "vergader", R(-6.6, 16.4, -1.0, 23.2),
             "Boven de vergaderkamer een nieuwe tussenvloer van 38 m² in de 7 m hoge hal: een tweede vergaderkamer voor zes en twee belcellen, met een glazen balustrade naar de werkzone. De rest van de hal blijft hoog en open.",
             ["Tussenvloer staal en hout op 3 m, stalen trap langs de gymwand", "Vergaderkamer voor 6 en twee belcellen", "Glazen balustrade: licht en zicht blijven"], n=1,
             cam=dict(t=[-3.8, 19.8], afstand=8, hoek=20),
             prompt="A steel and timber mezzanine inside a 7 m high 1970s hall: on top a glass-walled meeting room for six and two round felt phone booths behind a glass balustrade, a black steel stair along the wall, below it a meeting room for eight, the rest of the hall stays high, open and full of daylight."), tussenvloer=True),
        zone("Wastoren en douchetoren", "sanitair", R(-6.6, 23.2, -1.0, 35.7),
             "De twee torens in de bufferstrook: de wastoren open naar de werkzone, de douchetoren open naar de gym.", ["Wastoren 5,5 m, douchetoren 4,5 m"],
             cam=dict(t=[-3.8, 29.5], afstand=9, hoek=210),
             prompt="Two round concrete-look bathroom towers, 3 m high, standing in a high steel hall, board-marked plaster, a V-shaped concrete wash trough with brass taps, ivy hanging over the rims, skylights above."),
        zone("Werkzone in de hal", "werken", R(-1.0, 16.4, 4.8, 35.7),
             "Twintig compacte zit-sta bureaus in vijf eilanden en een raambar van 6 m langs de glazen deuren met uitzicht op de weilanden.",
             ["Vijf eilanden van vier bureaus 140 x 70", "Raambar van 6 m met tien krukken", "Met de grote tafel in het voorhuis: 40 werkplekken"],
             cam=dict(t=[1.8, 26], afstand=10, hoek=210),
             prompt="A coworking strip inside a high 1970s hall: five islands of four compact sit-stand desks with oak tops, a long window bar with stools facing big glass doors and green meadows, slate-blue acoustic baffles hanging high, plants."),
        zone("Fietsen en techniek", "techniek", R(5.1, 32.4, 12.6, 35.9), "Fietsen, warmtepomp, batterij en opslag.", []),
    ],
    elementen=[
        *zitkuil([11.6, 6.0], 1.9, 180, "#6f7d3a", "#d9ccb0"), *keuken([0.73, 3.9], 6.4, 90), *kookeiland([2.9, 3.9], 90),
        *grote_tafel([6.6, 4.0], 3.5, 90), plant([10.8, 1.0]), plant([6.2, 8.4]), *tafeltje([9.2, 1.4]),
        *kasten(1.0, 10.0, 1.0, d=0.4, h=1.1, n=1), *kasten(1.0, 10.0, 6.8, d=0.4, h=1.1, n=1),
        *[dict(t="box", soort="fauteuil", c=[u, 4.0], w=0.85, d=0.85, h=0.8, a=0, kleur="#47522a", n=1) for u in (3.0, 6.0, 9.0)],
        *rack([-13.8, 19.4], 90), *rack([-13.8, 22.4], 90), *rack([-13.8, 25.4], 90), *rack([-13.8, 28.4], 90),
        roeier([-8.4, 17.6], 0), roeier([-8.4, 19.2], 0),
        dict(t="kleed", c=[-10.0, 31.8], w=4.6, d=4.0, a=0, kleur="#c7928a"), label([-10.0, 31.8], "groepsles en yoga"), boom([-13.6, 34.6], 0.8, 3.4),
        wand([[-6.7, 16.0], [-6.7, 32.4]], 7.0, gym=True), wand([[-6.7, 33.6], [-6.7, 36.0]], 7.0, gym=True), deur([-10.6, 16.0], 0, toegang=True),
        *vergaderkamer([-3.8, 18.7], 5.4, 4.2, 0, 8), pod2([-3.9, 22.3]), pod2([-2.1, 22.3]),
        dict(t="box", soort="trap", c=[-6.1, 21.9], w=0.9, d=2.6, h=0.3, a=0, kleur="#2f3032"),
        *vergaderkamer([-3.8, 18.7], 5.4, 4.2, 0, 6, 1), pod2([-3.9, 22.3], 1), pod2([-2.1, 22.3], 1),
        wand([[-1.0, 16.4], [-1.0, 23.2]], 1.1, glas=True, n=1),
        *toren([-3.8, 26.6], 2.75, 0, "was"), *toren([-3.8, 33.0], 2.25, 180, "douche"),
        *[e for v in (18.8, 22.6, 26.4, 30.2, 34.0) for e in eiland2([0.9, v], 90 + (3 if int(v) % 2 else -3))],
        dict(t="box", soort="raambar", c=[4.5, 26.0], w=6.0, d=0.5, h=1.05, a=90, kleur=HOUT), plant([4.2, 17.0], 0.4, 1.4), plant([4.2, 34.8], 0.4, 1.4),
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
                                   "Keuken en espresso-eiland": [21.8, 7.4], "Bieb": [33.6, 26.2], "Techniek": [21.8, 12.1], "Kleedruimte en lockers": [34.0, 13.4],
                                   "Vergaderkamers": [33.4, 22.2], "Stille werkkamer": [25.0, 25.2], "Wastoren": [25.6, 18.4]},
    "den-bosch-eendenkooi-1a": {"Gym in de sportzaal (afsluitbaar)": [9.0, 4.4], "Boekencafé en keuken": [24.6, 9.0], "Kleedkamers met V-wastrog": [33.9, 11.4],
                                "Verdieping: werkzone": [24.0, 6.1], "Verdieping: vergaderkamers": [34.1, 6.7]},
    "voorhout-dinsdagse-wetering-56a": {"Boekencafé en keuken": [3.0, 6.6], "Werkzone in A": [16.6, 3.8], "Wastoren en entree": [26.4, 0.8],
                                        "Gym in gebouw B (afsluitbaar)": [26.4, -12.2], "Kleedruimte en techniek": [16.2, -8.4], "Techniek en fietsen": [17.8, -15.8],
                                        "Werkzolder op de entresol": [26.4, 4.2], "Vergaderkamers boven in B": [16.0, -10.0]},
    "maarssen-herenweg-15": {"Boekencafé en keuken in het voorhuis": [6.6, 7.4], "Gym (afsluitbaar)": [-10.6, 25.0], "Werkzone in de hal": [2.0, 36.6],
                             "Vergaderkamer en belcellen": [-3.8, 21.2], "Vergaderbalkon op de tussenvloer": [-3.8, 21.2], "Wastoren en douchetoren": [-3.8, 30.0], "Fietsen en techniek": [8.8, 33.2], "Stille bieb op zolder": [6.0, 4.0]},
})


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
    tv = sum(poly_area(z["poly"]) for z in ONTWERPEN[slug]["zones"] if z.get("tussenvloer"))
    add("Nieuwe tussenvloer staal + hout, incl. trap en glazen balustrade", tv, "m2", 650, "schatting")
    gw_glas = sum(math.dist(w["pts"][i], w["pts"][i + 1]) * w["h"] for w in E if w["t"] == "wand" and w.get("glas") for i in range(len(w["pts"]) - 1))
    add("Glazen binnenwand (stille werkkamer, vergaderverdieping)", gw_glas, "m2", 320, "schatting")
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
