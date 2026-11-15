"""
Stap 2 van de workflow: plattegrond-fit per pand.

Coördinaten zijn lokaal in meters: u langs de lange as van de hal, v haaks erop
(zie geo.frame). Zones zijn rechthoeken (u0, v0, u1, v1). De capaciteit volgt uit
de ruimte: gym circa 7,5 m2 per persoon, werkplekken als losse eilandjes van vier
zit-sta bureaus plus een lange werktafel en een raambar.
"""
from __future__ import annotations

import json
import math
import os

from geo import frame, to_local

HERE = os.path.dirname(os.path.abspath(__file__))

ZONEKLEUR = {"café": "#e0a458", "werken": "#7fb3d5", "gym": "#e07a5f", "sanitair": "#b8c4bb", "vergader": "#9b8ec4",
             "techniek": "#8d8d8d", "bieb": "#c9a26b", "studio": "#d68fb0", "verhuur": "#5c6670"}

STD_LEDEN = dict(n_vol=30, n_deel=30, n_club=60)

LAYOUTS = {
    "utrecht-van-heutszstraat-4": dict(
        titel="Van Heutszstraat 4, Utrecht",
        oordeel="kandidaat, te koop 13-11-2026",
        samenvatting="Verscholen buurthuis uit 1959 midden in een bouwblok in Lombok, 630 m² op één laag, met een verwilderde binnentuin. "
                     "Bereikbaar via een poort en steeg, op een paar minuten fietsen van Utrecht Centraal. Erfpacht is eeuwigdurend afgekocht. "
                     "Moet helemaal opgeknapt worden. Plafond circa 3,5 m. De verkoper kiest zelf de koper, dus een goed plan telt.",
        koop=dict(totaal=670_000, label="vraagprijs bedrijfspand.com, te koop op 13-11-2026"),
        verhuur=[], leden=dict(n_vol=30, n_deel=30, n_club=90), bouwjaar_risico=True, isoleren=True, pv_kwp=25,
        zones=[
            dict(type="café", naam="Boekencafé aan de tuin", r=(0.3, 0.3, 13.4, 8)),
            dict(type="bieb", naam="Stille leesbibliotheek", r=(0.3, 8.2, 5.2, 12.2)),
            dict(type="werken", naam="Werkzone", r=(13.6, 0.3, 26, 9.8)),
            dict(type="vergader", naam="Belcellen", r=(14.5, 10.2, 22, 12.5)),
            dict(type="vergader", naam="Vergaderkamers", r=(26.2, 0.3, 35.8, 4.5)),
            dict(type="sanitair", naam="Kleedruimte, douches, toiletten", r=(26.2, 4.5, 35.8, 10)),
            dict(type="gym", naam="Gym", r=(26.2, 10.2, 35.8, 25)),
        ],
        pui=dict(kant="v1", u0=6, u1=13.4, v=8.2),
        buiten=[dict(type="terras", naam="Terras in de binnentuin", r=(5.6, 8.6, 13.4, 15)),
                dict(type="tuin", naam="Binnentuin", r=(1, 15.5, 26, 21))],
        bomen_buiten=[(3, 19), (10, 20), (20, 19.5), (24, 18), (16, 17)],
    ),
    "den-bosch-rietveldenweg-13": dict(
        titel="Rietveldenweg 13, Den Bosch",
        oordeel="kandidaat, te koop 13-11-2026",
        samenvatting="Showroom uit 1966 met bedrijfswoning, 890 m² op één laag plus woning, aan de rand van de Rietvelden "
                     "met busverbinding naar Den Bosch Centraal. Binnen al strak afgewerkt (houten vloer, zwarte plafonds): weinig verbouw. "
                     "Buiten alleen het voorterrein aan de weg. De woning wordt verhuurd.",
        koop=dict(totaal=975_000, label="vraagprijs bedrijfspand.com, te koop op 13-11-2026"),
        verhuur=[dict(naam="Bedrijfswoning", m2=127, huur_jaar=15_600)],
        leden=dict(n_vol=33, n_deel=33, n_club=60), bouwjaar_risico=True, isoleren=False, pv_kwp=30,
        zones=[
            dict(type="café", naam="Boekencafé en keuken", r=(7.3, 0.3, 23.8, 12.6)),
            dict(type="werken", naam="Werkzone", r=(7.3, 12.8, 22, 25.6)),
            dict(type="gym", naam="Gym", r=(24, 0.3, 40.4, 12.6)),
            dict(type="sanitair", naam="Wastoren", r=(22, 13, 29.2, 19)),
            dict(type="vergader", naam="Stille werkkamer", r=(22, 19.2, 29.2, 25.8)),
            dict(type="sanitair", naam="Kleedruimte", r=(29.2, 12.8, 38.9, 15.8)),
            dict(type="vergader", naam="Vergaderkamers", r=(29.2, 15.8, 37.5, 22.6)),
            dict(type="bieb", naam="Bieb", r=(29.2, 22.6, 35.9, 26.8)),
            dict(type="verhuur", naam="Bedrijfswoning (verhuur)", r=(0.3, 13.6, 7, 25.8), verhuur=True),
        ],
        pui=dict(kant="u0", v0=1, v1=12.5, u=7),
        buiten=[dict(type="terras", naam="Terras met plantenbakken op het voorterrein", r=(1, 1, 6.6, 12.5))],
        bomen_buiten=[(-2, 3), (-2, 8), (-2, 12)],
    ),
    "voorhout-dinsdagse-wetering-56a": dict(
        titel="Dinsdagse Wetering 56A, Voorhout",
        oordeel="kandidaat, te koop 13-11-2026",
        samenvatting="Twee werkplaatsen van een oud bouwbedrijf (deels 1933, deels 1981 tot 2001), samen circa 570 m² met entresol en verdieping, "
                     "op 824 m² grond met een verhard terrein van circa 300 m². Oude centrum van Voorhout, station op loopafstand.",
        koop=dict(totaal=699_500, label="vraagprijs bedrijfspand.com, te koop op 13-11-2026"),
        verhuur=[], leden=STD_LEDEN, bouwjaar_risico=True, isoleren=True, pv_kwp=20, verdieping_m2=98,
        zones=[
            dict(type="café", naam="Boekencafé", r=(0.3, 0.3, 11.4, 7.3)),
            dict(type="werken", naam="Werkzone", r=(11.6, 0.3, 22.6, 7.3)),
            dict(type="sanitair", naam="Wastoren en entree", r=(22.4, 0.2, 30.1, 8.6)),
            dict(type="techniek", naam="Kleedruimte", r=(11.8, -10.4, 20.6, -4.8)),
            dict(type="techniek", naam="Techniek en fietsen", r=(15, -16.5, 20.6, -10.6)),
            dict(type="gym", naam="Gym", r=(20.9, -15.2, 33.4, -4.8)),
        ],
        pui=dict(kant="v0", u0=1, u1=22, v=0),
        buiten=[dict(type="terras", naam="Tuinstraat", r=(-3, -4.4, 33.6, -0.4))],
        bomen_buiten=[(3.5, -2.4), (12.5, -2.4), (21.5, -2.4), (30, -2.4)],
    ),
    "maarssen-herenweg-15": dict(
        titel="Herenweg 15, Maarssen",
        oordeel="kandidaat, beschikbaar volgens Oozo 13-11-2026",
        samenvatting="Woonhuis uit 1931 met bedrijfshal uit 1970 (advertentie: hal 760 m² en kantoor 80 m², BAG-grondvlak hal 434 m²), "
                     "perceel 1.405 m² aan de rand van de polder van Maarsseveen. Station Maarssen 4,8 km, snelweg 1 km.",
        koop=dict(totaal=1_085_000, label="vraagprijs Oozo, beschikbaar op 13-11-2026"),
        verhuur=[], leden=dict(n_vol=33, n_deel=33, n_club=60), bouwjaar_risico=True, isoleren=True, pv_kwp=40, verdieping_m2=50,
        zones=[
            dict(type="café", naam="Boekencafé in het voorhuis", r=(0.3, 0.3, 11.8, 9.1)),
            dict(type="gym", naam="Gym", r=(-14.6, 16.4, -6.8, 35.7)),
            dict(type="vergader", naam="Vergaderkamer en belcellen", r=(-6.6, 16.4, -1.0, 23.2)),
            dict(type="sanitair", naam="Torens", r=(-6.6, 23.2, -1.0, 35.7)),
            dict(type="werken", naam="Werkzone", r=(-1.0, 16.4, 4.8, 35.7)),
            dict(type="techniek", naam="Fietsen en techniek", r=(5.1, 32.4, 12.6, 35.9)),
        ],
        pui=dict(kant="v0", u0=-13, u1=4.6, v=16),
        buiten=[dict(type="terras", naam="Binnenplaats", r=(-4.6, 12.3, 5.0, 15.8)),
                dict(type="tuin", naam="Tuin naar de weilanden", r=(13, -6, 21.4, 36))],
        bomen_buiten=[(19.8, 0), (20.2, 14), (19.6, 28), (10, 34.8), (-3.6, -2.6), (13, -2.6)],
    ),
    "pernis-ring-15": dict(
        titel="Ring 15, Pernis", oordeel="kandidaat, beschikbaar volgens Oozo 14-11-2026",
        samenvatting="Dorpspand met bijeenkomstfunctie (BAG 1900, advertentie 1852), 520 m², 6,7 m hoog, perceel 935 m² met tuin. Pernis, Rotterdam.",
        koop=dict(totaal=590_000, label="vraagprijs Oozo, beschikbaar op 14-11-2026"),
        verhuur=[], leden=STD_LEDEN, bouwjaar_risico=True, isoleren=True, pv_kwp=15, verdieping_m2=62,
        zones=[dict(type="café", naam="Boekencafé", r=(0.3, 0.3, 11, 10.3)), dict(type="werken", naam="Werkzone", r=(11, 0.3, 25, 10.3)),
               dict(type="sanitair", naam="Wastoren", r=(25, 0.3, 32.2, 10.3)), dict(type="gym", naam="Gym", r=(32.2, 0.3, 42.3, 8.3))],
        pui=dict(kant="v0", u0=1, u1=24, v=0),
        buiten=[dict(type="terras", naam="Terras", r=(0.5, -6, 24, -0.4)), dict(type="tuin", naam="Tuin", r=(24, -8, 42, -0.4))],
        bomen_buiten=[(27, -4.5), (33, -5.5), (39, -4.5), (1.5, -5)],
    ),
    "uden-nijverheidsstraat-4c": dict(
        titel="Nijverheidsstraat 4C, Uden", oordeel="kandidaat, te koop 14-11-2026",
        samenvatting="Nieuwbouwunit in een complex van vier, circa 660 m² grondvlak (808 m² vbo), 8 tot 9,5 m hoog, glazen voorgevel. Bedrijventerrein in Uden.",
        koop=dict(totaal=949_000, label="vraagprijs bedrijfspand.com, v.o.n. (nieuwbouw, btw in de prijs, geen overdrachtsbelasting)", von=True),
        verhuur=[], leden=dict(n_vol=50, n_deel=50, n_club=0), bouwjaar_risico=False, isoleren=False, pv_kwp=60, verdieping_m2=190,
        zones=[dict(type="café", naam="Café", r=(27, 5, 38.4, 20.3)), dict(type="werken", naam="Werkzone", r=(12, 3, 27, 12.5)),
               dict(type="vergader", naam="Vergaderkamers", r=(12, 12.5, 27, 20.3)), dict(type="sanitair", naam="Torens", r=(6, 1.5, 12, 20.3)),
               dict(type="gym", naam="Gym", r=(0.2, 0.5, 6, 20.3))],
        pui=dict(kant="u1", v0=7.2, v1=20.2, u=38.5),
        buiten=[], bomen_buiten=[(41, 6), (41, 19)],
    ),
    "den-bosch-eendenkooi-1a": dict(
        titel="De Eendenkooi 1A, Den Bosch",
        oordeel="kandidaat, te koop 13-11-2026",
        samenvatting="Sportgebouw uit 1977, nu in gebruik als Snap Fitness: gymzaal, dansstudio, kleedkamers en douches zijn er al. "
                     "Verdieping met bovenwoning en dakterras. Groene omgeving aan het water naast sporthal De Schutskamp. "
                     "Vraag na of de huidige huurder blijft of vertrekt. Eigen grond is alleen het gebouw zelf.",
        koop=dict(totaal=1_400_000, label="vraagprijs bedrijfspand.com en oozo, te koop sinds oktober 2026"),
        verhuur=[dict(naam="Bovenwoning", m2=110, huur_jaar=14_400)],
        leden=dict(n_vol=32, n_deel=32, n_club=60), bouwjaar_risico=True, isoleren=False, pv_kwp=30, verdieping_m2=278, sanitair_bestaand=True,
        zones=[
            dict(type="gym", naam="Gym (bestaande sportzaal)", r=(0.3, 0.3, 17.5, 18)),
            dict(type="café", naam="Boekencafé en bieb bij de entree", r=(17.7, 0.3, 30.4, 10)),
            dict(type="studio", naam="Studio (bestaande dansstudio)", r=(17.7, 10, 30.4, 16.8)),
            dict(type="sanitair", naam="Kleedkamers en douches (bestaand)", r=(30.6, 0.3, 37.2, 14.6)),
            dict(type="werken", naam="Verdieping: werkzone en vergaderruimte", r=(17.7, 0.3, 37.2, 14.6), niveau=1),
        ],
        pui=dict(kant="v0", u0=19, u1=29, v=0),
        buiten=[],
        bomen_buiten=[(5, -5), (14, -6), (25, -5), (34, -6)],
    ),
    "rotterdam-hillevliet-139": dict(
        titel="Hillevliet 139, Rotterdam",
        oordeel="kandidaat, status bellen",
        samenvatting="Voormalige Leger des Heils-kerk uit 1929 van J.J.P. Oud, rijksmonument, in Rotterdam-Zuid. Kerkzaal van 530 m² "
                     "en 9 m hoog, met een strook tuin op het zuiden. Vraagprijs € 950.000: de goedkoopste kandidaat tot nu toe. "
                     "Een nieuwe tussenvloer geeft extra werkplekken. Rotterdam is groot genoeg voor 90 clubleden.",
        koop=dict(totaal=950_000, label="vraagprijs Heritage Europe en Reliplan, sinds 2024"),
        verhuur=[], leden=dict(n_vol=30, n_deel=30, n_club=90), bouwjaar_risico=True, isoleren=True, pv_kwp=0,
        verdieping_m2=128, nieuwe_vloer_m2=128, extra_werkplekken=16,
        zones=[
            dict(type="café", naam="Boekencafé onder de kerkramen", r=(0.5, 0.5, 12, 9)),
            dict(type="werken", naam="Werkzone met raambar", r=(12, 0.5, 26, 9)),
            dict(type="bieb", naam="Stille leesbibliotheek", r=(0.5, 9.5, 6, 18.8)),
            dict(type="studio", naam="Studio", r=(6, 9.5, 14, 18.8)),
            dict(type="gym", naam="Gym", r=(14, 9.5, 26, 18.6)),
            dict(type="sanitair", naam="Kleedruimte, douches, toiletten", r=(26.2, 12.5, 30.5, 18)),
            dict(type="vergader", naam="Tussenvloer: vergaderruimte + 16 werkplekken aan tafels", r=(0.5, 9.5, 14, 18.8), niveau=1),
        ],
        pui=dict(kant="v0", u0=2, u1=11, v=0.3),
        buiten=[dict(type="terras", naam="Terras op het zuiden", r=(2, -4.5, 20, -0.4)),
                dict(type="tuin", naam="Tuin", r=(28, -4, 34, 10))],
        bomen_buiten=[(31, 6), (31, -1), (22, -3)],
    ),
    "tilburg-bredaseweg-443": dict(
        titel="Bredaseweg 443, Tilburg",
        oordeel="kandidaat, prijs opvragen",
        samenvatting="Kantoorvilla uit 1941 met een vleugel uit 2000, 1.385 m² over drie lagen, op een landgoed van circa 8.000 m² "
                     "aan de rand van de Warande. De club neemt de begane grond en de verdieping van de nieuwe vleugel. De rest "
                     "(circa 600 m²) wordt verhuurd als kantoor. Prijs op aanvraag: hier gerekend met € 1,8 mln.",
        koop=dict(totaal=1_800_000, label="schatting: prijs op aanvraag"),
        verhuur=[dict(naam="Kantoorruimte villa verdieping + souterrain", m2=600, huur_m2=110)],
        leden=STD_LEDEN, bouwjaar_risico=True, isoleren=False, pv_kwp=20, verdieping_m2=220,
        zones=[
            dict(type="café", naam="Boekencafé in de villa", r=(0.5, 0.5, 12.5, 11)),
            dict(type="bieb", naam="Stille leesbibliotheek", r=(0.5, 11, 6.5, 19.3)),
            dict(type="studio", naam="Studio", r=(6.5, 11, 12.5, 19.3)),
            dict(type="gym", naam="Gym", r=(21.5, 0.5, 33, 11.5)),
            dict(type="sanitair", naam="Kleedruimte, douches, toiletten", r=(33, 0.5, 41.4, 6)),
            dict(type="vergader", naam="Vergaderruimte en belcellen", r=(33, 6, 41.4, 11.5)),
            dict(type="werken", naam="Verdieping nieuwe vleugel: werkzone", r=(21.5, 0.5, 41.4, 11.5), niveau=1),
        ],
        pui=dict(kant="v0", u0=1, u1=12, v=0),
        buiten=[dict(type="terras", naam="Terras aan de bosrand", r=(0, -6, 14, -0.4)),
                dict(type="tuin", naam="Landgoedtuin met buitenwerkplekken", r=(15, -16, 40, -1))],
        bomen_buiten=[(5, -10), (12, -14), (20, -18), (30, -19), (38, -17), (44, -6), (-4, 4), (-4, 14)],
    ),
    "utrecht-gertrudiskerk": dict(
        titel="Kerkcomplex Amaliadwarsstraat, Utrecht",
        oordeel="kandidaat",
        samenvatting="L-vormig complex uit 1923 naast de Sint-Gertrudiskerk in de Rivierenwijk, op 10 minuten fietsen van Utrecht "
                     "Centraal. Ruim 1.100 m² op 2.862 m² grond met binnenplaats en noordtuin. De club neemt de zuidvleugel, "
                     "de westvleugel wordt atelierruimte. In de stad rekenen we met 120 clubleden. Controleer of dit gebouw bij de verkoop van de kerk hoort.",
        koop=dict(totaal=1_900_000, label="schatting: kerkcomplex Utrecht, prijs onbekend"),
        verhuur=[dict(naam="Ateliers westvleugel", m2=231, huur_m2=150)],
        leden=dict(n_vol=30, n_deel=30, n_club=120), bouwjaar_risico=True, isoleren=True, pv_kwp=30,
        zones=[
            dict(type="café", naam="Café, lounge en bibliotheek", r=(0.5, 1.5, 17, 12)),
            dict(type="werken", naam="Werkzone", r=(17, 1.5, 40, 12.3)),
            dict(type="gym", naam="Gym", r=(40, 1, 58.5, 12.3)),
            dict(type="sanitair", naam="Kleedruimte, douches, toiletten", r=(49, 12.5, 57.4, 20)),
            dict(type="vergader", naam="Vergaderruimte en belcellen", r=(6, 12.5, 17, 20)),
            dict(type="studio", naam="Studio voor yoga en workshops", r=(6, 20, 17, 30)),
            dict(type="verhuur", naam="Ateliers (verhuur)", r=(6, 30, 17, 50.5), verhuur=True),
        ],
        pui=dict(kant="v1", u0=19, u1=39, v=12.4),
        buiten=[
            dict(type="terras", naam="Terras op de binnenplaats", r=(18, 13, 32, 19.5)),
            dict(type="tuin", naam="Binnentuin", r=(18, 20, 23.5, 50)),
            dict(type="tuin", naam="Noordtuin met ligbedden", r=(0, 52, 22, 70)),
        ],
        bomen_buiten=[(20.5, 25), (20.5, 33), (20.5, 41), (3, 66), (15, 66), (18, 55)],
        afmeting_buiten_opm="binnenplaats en noordtuin, ongeveer 1.000 m²",
    ),
    "uitgeest-molenwerf-15": dict(
        titel="Molenwerf 15, Uitgeest",
        oordeel="kandidaat, let op A9",
        samenvatting="Hal uit 1991 van 914 m² met verdieping op 4.821 m² grond: veel buitenruimte. Tussen Haarlem, Zaanstad en "
                     "Alkmaar, station Uitgeest op loopafstand. De A9 ligt direct naast het perceel: een groene geluidswal is nodig "
                     "voor tuin en terras.",
        koop=dict(totaal=1_400_000, label="schatting: 1.120 m² × € 1.250, prijs onbekend"),
        verhuur=[dict(naam="Oostelijk halgedeelte + verdieping", m2=400, huur_m2=100)],
        leden=STD_LEDEN, bouwjaar_risico=True, isoleren=True, pv_kwp=40, geluidswal=True,
        zones=[
            dict(type="werken", naam="Werkzone", r=(0.5, 0.5, 16, 12.6)),
            dict(type="café", naam="Café, lounge en bibliotheek", r=(0.5, 12.6, 16, 22.1)),
            dict(type="sanitair", naam="Kleedruimte, douches, toiletten", r=(16, 0.5, 22, 9)),
            dict(type="vergader", naam="Vergaderruimte en belcellen", r=(16, 9, 22, 14)),
            dict(type="studio", naam="Studio", r=(16, 14, 22, 22.1)),
            dict(type="gym", naam="Gym", r=(22, 0.5, 32, 22.1)),
            dict(type="verhuur", naam="Verhuur", r=(32, 0, 40.6, 22.6), verhuur=True),
        ],
        pui=dict(kant="v1", u0=2, u1=15, v=22.6),
        buiten=[
            dict(type="terras", naam="Terras", r=(2, 23, 18, 28)),
            dict(type="tuin", naam="Tuin met ligbedden", r=(0, 29, 30, 42)),
            dict(type="tuin", naam="Groene geluidswal richting A9", r=(42, 2, 56, 40)),
            dict(type="parkeren", naam="Parkeren", r=(-4, -5.5, 30, -0.5)),
        ],
        bomen_buiten=[(45, 6), (45, 14), (45, 22), (45, 30), (52, 10), (52, 26), (8, 38), (20, 38)],
    ),
    "houten-heemsteedseweg-24": dict(
        titel="Heemsteedseweg 24, Houten",
        oordeel="kandidaat, tuin niet eigen",
        samenvatting="Kantoorvilla uit 2006 van 683 m² over twee lagen, midden in de tuinen van kasteel Heemstede. Biofiel van "
                     "zichzelf, maar de tuin hoort bij het landgoed: alleen het terras is eigen. Werken boven, café en bieb beneden.",
        koop=dict(totaal=1_570_000, label="schatting: 683 m² × € 2.300, prijs onbekend"),
        verhuur=[], leden=STD_LEDEN, bouwjaar_risico=False, isoleren=False, pv_kwp=25, verdieping_m2=353,
        zones=[
            dict(type="café", naam="Café, lounge en bibliotheek", r=(0.3, 0.3, 14, 9.1)),
            dict(type="sanitair", naam="Kleedruimte, douches", r=(14, 0.3, 19, 9.1)),
            dict(type="gym", naam="Gym", r=(23, 0.3, 37.2, 9.1)),
            dict(type="werken", naam="Verdieping: werkzone", r=(0.3, 0.3, 25, 9.1), niveau=1),
            dict(type="vergader", naam="Verdieping: vergaderen en studio", r=(25, 0.3, 37.2, 9.1), niveau=1),
        ],
        pui=dict(kant="v0", u0=2, u1=13, v=0),
        buiten=[dict(type="terras", naam="Terras aan de kasteeltuin", r=(1, -7, 15, -0.3))],
        bomen_buiten=[(17, -4), (21, -4)],
    ),
    "uithoorn-thamerkerk": dict(
        titel="Thamerkerk, Uithoorn",
        oordeel="te duur per lid",
        samenvatting="Kerk uit 1834 aan de Amstel, 287 m² en 12 m hoog, met tuin aan het water. Vraagprijs € 1.295.000. Met een "
                     "nieuwe tussenvloer past een kleinere club: 40 eigenaren en 40 clubleden. Mooiste plek, maar te weinig "
                     "leden voor deze investering: een vol lid zou € 665 per maand moeten betalen.",
        koop=dict(totaal=1_295_000, label="vraagprijs funda in business (bieding)"),
        verhuur=[], leden=dict(n_vol=20, n_deel=20, n_club=40), bouwjaar_risico=True, isoleren=True, pv_kwp=0,
        verdieping_m2=190, nieuwe_vloer_m2=190,
        zones=[
            dict(type="café", naam="Café en bibliotheek onder het gewelf", r=(4, 1, 13, 11.5)),
            dict(type="gym", naam="Gym", r=(13, 1, 22, 11.5)),
            dict(type="sanitair", naam="Kleedruimte en douches", r=(22, 2.5, 25.5, 9)),
            dict(type="techniek", naam="Entree, trap, techniek", r=(0.5, 3, 4, 9)),
            dict(type="werken", naam="Tussenvloer: werkzone", r=(4, 1, 17, 11.5), niveau=1),
            dict(type="studio", naam="Tussenvloer: studio", r=(17, 1, 22, 11.5), niveau=1),
        ],
        pui=dict(kant="v0", u0=6, u1=20, v=0),
        buiten=[
            dict(type="terras", naam="Terras aan de Amstel", r=(3, -5.5, 21, -0.5)),
            dict(type="tuin", naam="Tuin", r=(24, -8, 46, 2)),
        ],
        bomen_buiten=[(26, 0), (40, -2), (44, 1)],
    ),
    "best-de-run-5": dict(
        titel="De Run 5, Best",
        oordeel="kandidaat",
        samenvatting="Hal uit 1982 van 1.326 m² op 3.074 m² eigen grond, tegen een bosrand. De club gebruikt de westelijke 620 m²; "
                     "het oostelijke halgedeelte, het kantoor en de bedrijfswoning worden verhuurd.",
        koop=dict(hal_m2=1606, hal_prijs_m2=850, kantoor_m2=131, kantoor_prijs_m2=1200, woning=450_000,
                  label="schatting: 1982, Best, complex in zijn geheel; vraagprijs op aanvraag"),
        verhuur=[dict(naam="Oostelijk halgedeelte", m2=716, huur_m2=75), dict(naam="Kantoor De Run 7", m2=131, huur_m2=120),
                 dict(naam="Bedrijfswoning De Run 3", m2=156, huur_jaar=19_200)],
        leden=STD_LEDEN, bouwjaar_risico=True, isoleren=True, pv_kwp=40,
        zones=[
            dict(type="café", naam="Café, lounge en bibliotheek", r=(0, 6.2, 20, 14)),
            dict(type="werken", naam="Werkzone", r=(0, 14, 14, 27)),
            dict(type="sanitair", naam="Kleedruimte, 4 douches, 4 toiletten", r=(14, 14, 20, 21)),
            dict(type="vergader", naam="Vergaderruimte en belcellen", r=(14, 21, 20, 27)),
            dict(type="gym", naam="Gym", r=(0, 27, 13, 37.2)),
            dict(type="studio", naam="Studio", r=(13, 27, 20, 37.2)),
            dict(type="verhuur", naam="Verhuur: oostelijk halgedeelte", r=(20, 5.4, 38.1, 37.2), verhuur=True),
        ],
        brandwand=dict(lengte=31.8, hoogte=7.0),
        pui=dict(kant="v0", u0=4, u1=18, v=6.2),
        buiten=[
            dict(type="terras", naam="Houten terras met overkapping", r=(7, 0.3, 21, 5.2)),
            dict(type="tuin", naam="Tuin met ligbedden", r=(21, -22, 35, -9)),
            dict(type="tuin", naam="Groene strook met buitenwerkplekken en buitenrig", r=(39, 8, 50, 35)),
            dict(type="parkeren", naam="Parkeren op bestaande verharding", r=(36, -12, 48, 6)),
        ],
        bomen_buiten=[(40.5, 12), (40.5, 20), (40.5, 28), (48.5, 16), (48.5, 31), (24, -18), (32, -20), (22, -12)],
    ),
    "amersfoort-birkt-21": dict(
        titel="Birkt 21, Amersfoort",
        oordeel="kandidaat, krap buiten",
        samenvatting="Nieuwe energieneutrale hal uit 2023, 785 m² inclusief verdieping, vraagprijs € 1.250.000. "
                     "Weinig eigen buitenruimte: alleen de strook aan de voorkant voor een terras.",
        koop=dict(totaal=1_250_000, label="vraagprijs funda in business"),
        verhuur=[], leden=STD_LEDEN, bouwjaar_risico=False, isoleren=False, pv_kwp=0, verdieping_m2=242,
        zones=[
            dict(type="café", naam="Café, lounge en bibliotheek (vide)", r=(0, 0, 10, 21.7)),
            dict(type="sanitair", naam="Kleedruimte, douches, toiletten", r=(10, 0, 16, 9)),
            dict(type="studio", naam="Studio", r=(10, 15, 16, 21.7)),
            dict(type="gym", naam="Gym", r=(16, 0, 25, 21.7)),
            dict(type="werken", naam="Verdieping: werkzone, vergaderen, belcellen", r=(0, 0, 11, 21.7), niveau=1),
        ],
        pui=dict(kant="u0", v0=4, v1=16, u=0),
        buiten=[
            dict(type="terras", naam="Terras met plantenbakken", r=(-8, 3, -0.3, 15)),
            dict(type="parkeren", naam="Parkeren voor de deur", r=(-12, -2, -0.3, 2.5)),
            dict(type="parkeren", naam="Parkeren voor de deur", r=(-12, 15.5, -0.3, 21.7)),
        ],
        bomen_buiten=[(-9.5, 5), (-9.5, 9), (-9.5, 13)],
    ),
}

AFGEVALLEN = {
    "best-de-waal-13": "Bedrijfsverzamelgebouw uit 2025 met 14 units van 123 m² op twee lagen. Geen open ruimte en geen eigen buitenruimte.",
    "woerden-marconiweg-5": "Pand uit 1974 met twee units van 244 en 238 m² op twee lagen. Te klein en geen buitenruimte.",
    "best-sonseweg-15": "Pand uit 1930 met woon- en bedrijfsfunctie, 188 m². Te klein.",
    "zeist-arendsburg": "Monument uit 1872, 721 m² over drie lagen op 669 m² grond aan een drukke weg. Gym past alleen op een verdieping en de tuin is klein.",
    "zeist-utrechtseweg-131": "Kantoorvilla uit 1900 van 506 m² over vier lagen. Te veel trappen voor een gym en een café.",
    "haarlem-kampersingel-42": "Footprint 150 m², 385 m² verdeeld over drie objecten. Te klein.",
    "bunnik-regulierenring-29": "Bedrijfsunit van 197 m². Te klein.",
    "bunnik-provincialeweg-1": "Kantoorpand van 386 m² verdeeld over zes objecten. Te klein.",
    "zoeterwoude-industrieweg-36": "Hal uit 1976 van 792 m², maar ingeklemd in een rij hallen: nauwelijks buitenruimte (perceel 784 m²).",
    "haarlem-kuipersweg-4": "Nieuw bedrijfsverzamelgebouw met 122 units. Geen los pand.",
    "den-bosch-bloemendaal-10": "Pand uit 1978 van 1.066 m² over twee lagen op 800 m² grond. Buitenruimte is alleen parkeerterrein.",
    "ter-aar-woudsedijk-11": "Hal uit 1993 van 1.336 m² in een dorp zonder trein. Te ver van de doelgroep.",
    "boxtel-bosscheweg-85": "Villa Catharina, 723 m² + koetshuis op 9.866 m² tuin met zwembad. Prachtig, maar € 2.950.000: een vol lid zou circa € 695 per maand nodig hebben.",
    "amersfoort-stadsring-103": "Monumentale kantoorvilla, 474 m² voor € 2.200.000. Te klein en te duur: circa € 539 per maand om te draaien.",
    "helmond-mierloseweg-130": "Villa de Raymaert, monument, 773 m², € 1.450.000, te koop sinds november 2025. Circa € 383 per maand om te draaien, lening 68%: net te duur.",
    "amersfoort-computerweg-37": "Kantoor met hal, 832 m², € 1.325.000, te koop sinds juli 2026. Circa € 357 per maand om te draaien, lening 66%.",
    "capelle-lentedans-50a": "Kantoorvilla in groen park, circa 550 m² over twee lagen, € 1.075.000. Circa € 305 per maand, maar weinig ruimte voor een gym.",
    "bergen-op-zoom-bosstraat-38": "Pandcomplex in het centrum, circa 1.000 m² over twee lagen, € 625.000. Rekent goed (circa € 211), maar ver van de Randstad en geen buitenruimte.",
    "dordrecht-houttuinen-32a": "Voormalig Arsenaal, rijksmonument, 838 m² over drie lagen zonder buitenruimte, € 1.550.000. Circa € 404 per maand, lening 70%.",
    "den-haag-pomonaplein-49": "Voormalige kerk met woning, loft en B&B, 1.732 m² voor € 4.250.000. Ook met verhuur van woning en B&B circa € 890 per maand nodig.",
}


def rect_area(r):
    return (r[2]-r[0]) * (r[3]-r[1])


def werkplekken(r, max_desks=20):
    """Losse eilandjes van 4 zit-sta bureaus, afwisselend gedraaid, plus lange werktafel en raambar.
    Geeft meubels als dict(type, c=(u,v), w, d, a=graden)."""
    u0, v0, u1, v1 = r
    L, W = u1-u0, v1-v0
    lang_u = L >= W
    items = []
    # raambar langs de onderrand (v0 of u0), werktafel langs de bovenrand
    if lang_u:
        items.append(dict(type="raambar", c=(u0 + L/2, v0 + 0.45), w=min(L - 2, 10), d=0.5, a=0))
        items.append(dict(type="tafel", c=(u0 + L/2, v1 - 1.6), w=min(L - 3, 7.2), d=1.2, a=0))
        lo, hi = (u0 + 1.0, v0 + 2.0), (u1 - 1.0, v1 - 3.4)
    else:
        items.append(dict(type="raambar", c=(u0 + 0.45, v0 + W/2), w=min(W - 2, 10), d=0.5, a=90))
        items.append(dict(type="tafel", c=(u1 - 1.6, v0 + W/2), w=min(W - 3, 7.2), d=1.2, a=90))
        lo, hi = (u0 + 2.0, v0 + 1.0), (u1 - 3.4, v1 - 1.0)
    desks = []
    hoeken = [-8, 6, 0, 11, -5, 4, 9, -10]  # licht gedraaide eilanden: geen strakke rijen
    k = 0
    if lang_u:
        rij, v = 0, lo[1] + 0.9
        while v + 0.9 <= hi[1] + 0.3 and len(desks) < max_desks:
            u = lo[0] + 1.6 + (2.5 if rij % 2 else 0)
            while u + 1.6 <= hi[0] + 0.2 and len(desks) < max_desks:
                a = hoeken[k % len(hoeken)]; k += 1
                ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
                for du, dv in ((-0.8, -0.4), (0.8, -0.4), (-0.8, 0.4), (0.8, 0.4)):
                    desks.append(dict(type="desk", c=(round(u + du*ca - dv*sa, 2), round(v + du*sa + dv*ca, 2)), w=1.6, d=0.8, a=a))
                u += 5.0
            v += 3.8
            rij += 1
    else:
        rij, u = 0, lo[0] + 0.9
        while u + 0.9 <= hi[0] + 0.3 and len(desks) < max_desks:
            v = lo[1] + 1.6 + (2.5 if rij % 2 else 0)
            while v + 1.6 <= hi[1] + 0.2 and len(desks) < max_desks:
                a = 90 + hoeken[k % len(hoeken)]; k += 1
                ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
                for du, dv in ((-0.8, -0.4), (0.8, -0.4), (-0.8, 0.4), (0.8, 0.4)):
                    desks.append(dict(type="desk", c=(round(u + du*ca - dv*sa, 2), round(v + du*sa + dv*ca, 2)), w=1.6, d=0.8, a=a))
                v += 5.0
            u += 3.8
            rij += 1
    desks = desks[:max_desks]
    return items + desks, len(desks)


def _laad_extra():
    import glob
    for f in sorted(glob.glob(os.path.join(HERE, "layout_extra", "*.py"))):
        try:
            exec(compile(open(f, encoding="utf-8").read(), f, "exec"), globals())
        except Exception as e:  # noqa: BLE001
            import sys
            print("WAARSCHUWING layout_extra", os.path.basename(f), repr(e), file=sys.stderr)


def build(slug):
    L = LAYOUTS[slug]
    d = json.load(open(os.path.join(HERE, "dossiers", slug + ".json")))
    F = frame(d["footprint"])
    loc = lambda ring: [list(map(lambda x: round(x, 2), to_local(p, F))) for p in ring]
    club = [z for z in L["zones"] if not z.get("verhuur")]
    begane = [z["r"] for z in club if z.get("niveau", 0) == 0]
    club_m2 = sum(rect_area(r) for r in begane) + L.get("verdieping_m2", 0)
    verhuur_m2 = sum(v["m2"] for v in L["verhuur"] if "huur_m2" in v)
    u0 = min(r[0] for r in begane); v0 = min(r[1] for r in begane)
    u1 = max(r[2] for r in begane); v1 = max(r[3] for r in begane)
    omtrek_extern = 2 * ((u1-u0) + (v1-v0)) - (L["brandwand"]["lengte"] if "brandwand" in L else 0)
    werk = next(z for z in L["zones"] if z["type"] == "werken")
    meubels, n_desks = werkplekken(werk["r"])
    pui_len = (L["pui"].get("u1", 0) - L["pui"].get("u0", 0)) if L["pui"]["kant"] in ("v0", "v1") else (L["pui"]["v1"] - L["pui"]["v0"])
    gym_m2 = round(sum(rect_area(z["r"]) for z in club if z["type"] == "gym"))
    q = dict(
        club_m2=round(club_m2), verhuur_m2=round(verhuur_m2), dak_club_m2=round(sum(rect_area(r) for r in begane)),
        gevel_isolatie_m2=round(omtrek_extern * 4.5) if L["isoleren"] else 0,
        pui_m2=round(pui_len * 3.0),
        brandwand_m2=round(L["brandwand"]["lengte"] * L["brandwand"]["hoogte"]) if "brandwand" in L else 0,
        terras_m2=round(sum(rect_area(b["r"]) for b in L["buiten"] if b["type"] == "terras")),
        tuin_m2=round(sum(rect_area(b["r"]) for b in L["buiten"] if b["type"] == "tuin")),
        bomen_buiten=len(L["bomen_buiten"]),
        buiten_sauna=any(b["type"] == "sauna" for b in L["buiten"]),
        gym_m2=gym_m2, desks=n_desks, hoogte=d["hoogte"], perceel_m2=(d["perceel"] or {}).get("m2"),
        nieuwe_vloer_m2=L.get("nieuwe_vloer_m2", 0), geluidswal=L.get("geluidswal", False),
    )
    leden = L["leden"]
    q["gym_cap"] = int(gym_m2 / 7.5)
    q["werk_cap"] = n_desks + 12 + 8 + L.get("extra_werkplekken", 0)  # eilandjes + werktafel + raambar (+ tussenvloer)
    tot = leden["n_vol"] + leden["n_deel"] + leden["n_club"]
    q["gym_piek"] = math.ceil(((leden["n_vol"] + leden["n_deel"]) * 2.5 + leden["n_club"] * 3) * 1.25 / 105 * 2.5)
    q["werk_piek"] = math.ceil(0.96 * (0.7 * leden["n_vol"] + 0.5 * leden["n_deel"]))
    viewer = dict(
        slug=slug, titel=L["titel"], oordeel=L["oordeel"], samenvatting=L["samenvatting"],
        zones=[dict(z, kleur=ZONEKLEUR[z["type"]], m2=round(rect_area(z["r"]))) for z in L["zones"]],
        buiten=L["buiten"], bomen_buiten=L["bomen_buiten"], pui=L["pui"], meubels=meubels,
        werkniveau=werk.get("niveau", 0), q=q, pv_kwp=L["pv_kwp"], leden=leden, leden_tot=tot,
    )
    return viewer, q


if __name__ == "__main__":
    for s in LAYOUTS:
        v, q = build(s)
        print(s, {k: q[k] for k in ("club_m2", "verhuur_m2", "gym_m2", "gym_cap", "gym_piek", "desks", "werk_cap", "werk_piek", "tuin_m2", "terras_m2", "pui_m2")})


# Statuscheck 13 november 2026 (zoekmachines; funda in business blokkeert automatische controle)
STATUS = {
    "rotterdam-hillevliet-139": ("verkocht", "Verkocht (gecontroleerd door Lucas, 13 november 2026). Eerdere vermelding: " "Vraagprijs € 950.000 k.k. bij Heritage Europe en Reliplan, aangeboden sinds 2024. "
                                 "Geen verkoopbericht gevonden, maar ook niets recents: eerst bellen."),
    "tilburg-bredaseweg-443": ("niet bevestigd", "Alleen Oozo meldt 'beschikbaar' (sinds 2 december 2024); de site van de makelaar was niet te openen. " "Prijs op aanvraag bij Raimond Weenink en op funda in business als beschikbaar; "
                               "advertentie is circa 589 dagen oud."),
    "amersfoort-birkt-21": ("verkocht", "Verkocht aan Automotive Soest (Comma Vastgoed). Stond te koop voor € 650.000 met 563 m²; "
                            "de eerder gebruikte € 1.250.000 en 785 m² hoorden bij een ander object."),
    "utrecht-gertrudiskerk": ("verkocht", "Kerk verkocht en verbouwd tot Commit Health Club, een sportschool met sauna. "
                              "Bewijs dat het concept in een kerk werkt, maar niet meer beschikbaar."),
    "uitgeest-molenwerf-15": ("niet te koop", "Alleen te huur aangeboden en inmiddels als verhuurd vermeld."),
    "houten-heemsteedseweg-24": ("niet te koop", "Kantoor was te huur en staat als verhuurd vermeld."),
    "best-de-run-5": ("alleen huur", "Te huur sinds maart 2025 voor € 7.500 per maand (circa 1.600 m²). De Run 3 is apart verkocht."),
    "uithoorn-thamerkerk": ("status onbekend", "In 2019 verkocht aan Heem Locaties, in 2021 weer te koop gezet; actuele status niet bevestigd."),
}


# Ronde 7 (15 november 2026): eerst de wijk, dan het pand. Zie ronde7/ronde7.md.
LAYOUTS.update({
    "rotterdam-galvanistraat-122": dict(
        titel="Galvanistraat 122-126, Rotterdam West", oordeel="kandidaat, beschikbaar volgens oozo op 15-11-2026",
        samenvatting="Drie units (2000) in een bedrijfsverzamelgebouw aan een parkeerhof, hal 425 + kantoor 271 m², vrije hoogte 5,9 m, lichtstraten. Nieuw Mathenesse, grens Rotterdam West en Schiedam.",
        koop=dict(totaal=1_125_000, label="vraagprijs oozo, beschikbaar op 15-11-2026"),
        verhuur=[], leden=dict(n_vol=45, n_deel=45, n_club=30), bouwjaar_risico=False, isoleren=False, pv_kwp=25, verdieping_m2=113,
        zones=[dict(type="café", naam="Café", r=(21, 0.2, 29.1, 16)), dict(type="werken", naam="Werkzone", r=(13.6, 0.2, 21, 10.5)),
               dict(type="vergader", naam="Vergaderen", r=(13.6, 10.5, 21, 16)), dict(type="sanitair", naam="Torens", r=(7.8, 0.2, 13.6, 16)),
               dict(type="gym", naam="Gym", r=(0.2, 0.2, 7.8, 16))],
        pui=dict(kant="v1", u0=8.5, u1=23.1, v=16),
        buiten=[dict(type="terras", naam="Terras tussen de portalen", r=(8.5, 16, 23.1, 19.8))], bomen_buiten=[(1, 22), (30, 22)],
        extra_rows=[dict(groep="Bouwkundig", post="Doorbraken in de twee scheidingswanden tussen de units (stalen latei, constructeur)", h=2, e="st", prijs=9_000, label="schatting", gen=0.3)],
        opex_extra=[("VvE-bijdrage bedrijfsverzamelgebouw (aanname, navragen)", 6_000)],
    ),
    "schiedam-calandstraat-92": dict(
        titel="Calandstraat 92, Schiedam", oordeel="kandidaat, beschikbaar volgens oozo (ronde 7, 15-11-2026)",
        samenvatting="Vrijstaande hal uit 1973 van 42 x 24 m (BAG 1.174 m²), hal 800 + kantoor 200 m², circa 5,4 m tot het dak, op de hoek van twee straten. Erfpacht.",
        koop=dict(totaal=825_000, label="vraagprijs oozo, ronde 7 (15-11-2026), erfpacht"),
        verhuur=[], leden=dict(n_vol=55, n_deel=55, n_club=30), bouwjaar_risico=True, isoleren=True, pv_kwp=40, verdieping_m2=96,
        zones=[dict(type="café", naam="Café", r=(0.2, 14.3, 18, 23.8)), dict(type="werken", naam="Werkzone", r=(18, 4, 32, 23.8)),
               dict(type="vergader", naam="Vergaderen", r=(32, 0.2, 41.8, 14)), dict(type="bieb", naam="Entree en bieb", r=(32, 14, 41.8, 23.8)),
               dict(type="sanitair", naam="Torens", r=(12, 0.2, 18, 14.3)), dict(type="gym", naam="Gym", r=(0.2, 0.2, 12, 14))],
        pui=dict(kant="v1", u0=0.5, u1=31.5, v=24),
        buiten=[], bomen_buiten=[],
        extra_rows=[dict(groep="Bouwkundig", post="Glazen pui, aluminium HR+++ triple glas (oostgevel, vergaderkamers)", h=39, e="m2", prijs=1_000, label="bron", gen=0.6)],
        opex_extra=[("Erfpachtcanon (aanname, navragen bij gemeente Schiedam)", 8_000)],
    ),
    "rotterdam-metaalhof-40": dict(
        titel="Metaalhof 40, Rotterdam Het Lage Land", oordeel="kandidaat, beschikbaar volgens oozo (ronde 7, 15-11-2026)",
        samenvatting="Pand uit 1986: kantoor 222 m² beneden en 360 m² boven, hoge bedrijfsruimte maar circa 110 m² (brochure), perceel 849 m² met eigen strook voor terras en 3 parkeerplaatsen. Erfpacht afgekocht tot 2035. 800 m van station Rotterdam Alexander.",
        koop=dict(totaal=1_150_000, label="vraagprijs oozo, ronde 7 (15-11-2026)"),
        verhuur=[], leden=dict(n_vol=50, n_deel=50, n_club=30), bouwjaar_risico=True, isoleren=True, pv_kwp=25, verdieping_m2=357,
        zones=[dict(type="café", naam="Café", r=(9, 0.2, 18.5, 15.8)), dict(type="werken", naam="Werkzone", r=(0.2, 0.2, 9, 15.8)),
               dict(type="vergader", naam="Entree en toiletten", r=(0.2, 16, 8.9, 26.7)), dict(type="sanitair", naam="Torens", r=(18.5, 0.2, 24, 15.8)),
               dict(type="gym", naam="Gym", r=(24, 0.2, 31.4, 15.8))],
        pui=dict(kant="v1", u0=9.5, u1=18, v=16),
        buiten=[dict(type="terras", naam="Terras", r=(9, 16, 20, 22))], bomen_buiten=[(10.5, 25.5)],
    ),
})

# Ronde 8 (15 november 2026)
LAYOUTS.update({
    "rotterdam-linschotenstraat-20a": dict(
        titel="Linschotenstraat 20A, Rotterdam Spaanse Polder", oordeel="kandidaat, status onzeker (online sinds 2022): eerst nabellen",
        samenvatting="Bedrijfsunit uit 2010 in een complex met bouwstroken van 16 m, hal 452 + kantoor 117 m², vrije hoogte 9 m, lichtstraat, perceel 506 m², 5 parkeerplaatsen.",
        koop=dict(totaal=899_000, label="vraagprijs oozo en funda in business (zoekresultaat), status onzeker"),
        verhuur=[], leden=dict(n_vol=40, n_deel=40, n_club=30), bouwjaar_risico=False, isoleren=False, pv_kwp=25, verdieping_m2=154,
        zones=[dict(type="café", naam="Café", r=(0.2, 0.2, 9, 15.8)), dict(type="werken", naam="Werkzone", r=(9, 0.2, 17, 15.8)),
               dict(type="sanitair", naam="Torens", r=(17, 0.2, 23, 15.8)), dict(type="gym", naam="Gym", r=(23, 0.2, 31, 15.8))],
        pui=dict(kant="u0", v0=0.5, v1=15.5, u=0),
        buiten=[dict(type="terras", naam="Terras", r=(-4, 0.5, -0.2, 8))], bomen_buiten=[],
        extra_rows=[dict(groep="Bouwkundig", post="Glazen pui, aluminium HR+++ triple glas (bovenlicht straatgevel tot 5 m)", h=30, e="m2", prijs=1_000, label="bron", gen=0.6)],
        opex_extra=[("VvE-bijdrage bedrijvencomplex (aanname, navragen)", 5_000)],
    ),
})

_laad_extra()
