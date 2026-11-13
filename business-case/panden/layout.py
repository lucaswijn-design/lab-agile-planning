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
    q["werk_cap"] = n_desks + 12 + 8  # eilandjes + werktafel + raambar
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
