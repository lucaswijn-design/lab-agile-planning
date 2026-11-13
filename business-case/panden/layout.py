"""
Stap 2 van de workflow: plattegrond-fit per pand.

Coördinaten zijn lokaal in meters: u langs de lange as van de hal, v haaks erop
(zie geo.frame). Zones zijn rechthoeken (u0, v0, u1, v1). Uit de zones volgen de
hoeveelheden voor stap 3 (financieel): m2 club, gevel, glas, dak, tuin, terras.
"""
from __future__ import annotations

import json
import math
import os

from geo import frame, to_local

HERE = os.path.dirname(os.path.abspath(__file__))

ZONEKLEUR = {"café": "#e0a458", "werken": "#7fb3d5", "gym": "#e07a5f", "sanitair": "#b8c4bb",
             "vergader": "#9b8ec4", "techniek": "#8d8d8d", "sauna": "#c96f3b", "verhuur": "#5c6670"}

LAYOUTS = {
    "best-de-run-5": dict(
        titel="De Run 5, Best",
        oordeel="kandidaat",
        samenvatting="Hal uit 1982 van 1.326 m² op 3.074 m² eigen grond, tegen een bosrand. De club gebruikt de westelijke 610 m²; "
                     "de oostelijke 716 m², het kantoor en de bedrijfswoning worden verhuurd.",
        koop=dict(hal_m2=1606, hal_prijs_m2=850, kantoor_m2=131, kantoor_prijs_m2=1200, woning=450_000,
                  label="schatting: 1982, Best, complex in zijn geheel; vraagprijs op aanvraag"),
        verhuur=[dict(naam="Oostelijk halgedeelte", m2=716, huur_m2=75), dict(naam="Kantoor De Run 7", m2=131, huur_m2=120),
                 dict(naam="Bedrijfswoning De Run 3", m2=156, huur_jaar=19_200)],
        bouwjaar_risico=True, isoleren=True, pv_kwp=40,
        zones=[
            dict(type="café", naam="Café, lounge en bibliotheek", r=(0, 6.2, 20, 14)),
            dict(type="werken", naam="Werkzone 24 zit-sta plekken + werktafel", r=(0, 14, 14, 27)),
            dict(type="sanitair", naam="Kleedruimte, 4 douches, 4 toiletten", r=(14, 14, 20, 22)),
            dict(type="vergader", naam="Vergaderruimte en 2 belcellen", r=(14, 22, 20, 27)),
            dict(type="gym", naam="Gym, 20 tegelijk", r=(0, 27, 17, 37.2)),
            dict(type="techniek", naam="Techniek en opslag", r=(17, 27, 20, 37.2)),
            dict(type="verhuur", naam="Verhuur: oostelijk halgedeelte", r=(20, 5.4, 38.1, 37.2), verhuur=True),
        ],
        brandwand=dict(lengte=31.8, hoogte=7.0),
        pui=dict(lengte=14, kant="v0", u0=4, u1=18),
        buiten=[
            dict(type="terras", naam="Houten terras met overkapping", r=(7, 0.3, 21, 5.2)),
            dict(type="sauna", naam="Saunahut 12 pers.", r=(23, -7, 27, -3)),
            dict(type="hottub", naam="Hot tub", c=(30, -4.5), d=2.2),
            dict(type="plunge", naam="Koudwaterbad", r=(32.5, -7, 34.5, -5)),
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
                     "Weinig eigen buitenruimte: alleen de strook aan de voorkant, dus de sauna komt binnen.",
        koop=dict(totaal=1_250_000, label="vraagprijs funda in business"),
        verhuur=[],
        bouwjaar_risico=False, isoleren=False, pv_kwp=0, verdieping_m2=242,
        zones=[
            dict(type="café", naam="Café, lounge en bibliotheek (vide)", r=(0, 0, 10, 21.7)),
            dict(type="sanitair", naam="Kleedruimte, douches, toiletten", r=(10, 0, 16, 9)),
            dict(type="sauna", naam="Binnensauna 10 pers. + koudwaterbad", r=(10, 9, 16, 15)),
            dict(type="techniek", naam="Techniek en trap", r=(10, 15, 16, 21.7)),
            dict(type="gym", naam="Gym, 20 tegelijk", r=(16, 0, 25, 21.7)),
            dict(type="werken", naam="Verdieping: 24 werkplekken, vergaderruimte, belcellen", r=(0, 0, 11, 21.7), niveau=1),
        ],
        pui=dict(lengte=12, kant="u0", v0=4, v1=16),
        buiten=[
            dict(type="terras", naam="Terras met plantenbakken", r=(-8, 3, -0.3, 15)),
            dict(type="parkeren", naam="Parkeren voor de deur", r=(-12, -2, -0.3, 2.5)),
            dict(type="parkeren", naam="Parkeren voor de deur", r=(-12, 15.5, -0.3, 21.7)),
        ],
        bomen_buiten=[(-9.5, 5), (-9.5, 9), (-9.5, 13)],
    ),
}

AFGEVALLEN = {
    "best-de-waal-13": "Nieuw bedrijfsverzamelgebouw (2025) met 14 units van 123 m², verdeeld over twee lagen. "
                       "Geen open ruimte voor een gym of café, en de buitenruimte is gedeeld parkeerterrein.",
    "woerden-marconiweg-5": "Pand uit 1974 met twee units van 244 en 238 m² op twee lagen. Te klein voor het "
                            "programma van circa 600 m², en geen eigen buitenruimte.",
    "best-sonseweg-15": "Pand uit 1930 met woon- en bedrijfsfunctie, 188 m² verblijfsobject. Te klein en een woonbestemming.",
}


def rect_area(r):
    return (r[2]-r[0]) * (r[3]-r[1])


def desks(r, n=60):
    """Zoveel bureaus als er in de werkzone passen: 1,6 x 0,8 m, rijafstand 2,4 m."""
    u0, v0, u1, v1 = r
    out = []
    v = v0 + 1.6
    while v + 0.8 < v1 - 3.2 and len(out) < n:  # laatste 3,2 m voor de werktafel
        u = u0 + 1.0
        while u + 1.6 < u1 - 0.8 and len(out) < n:
            out.append((u, v, 1.6, 0.8))
            u += 1.8
        v += 2.4
    return out


def build(slug):
    L = LAYOUTS[slug]
    d = json.load(open(os.path.join(HERE, "dossiers", slug + ".json")))
    F = frame(d["footprint"])
    loc = lambda ring: [list(map(lambda x: round(x, 2), to_local(p, F))) for p in ring]
    club = [z for z in L["zones"] if not z.get("verhuur")]
    club_m2 = sum(rect_area(z["r"]) for z in club if z.get("niveau", 0) == 0) + L.get("verdieping_m2", 0)
    verhuur_m2 = (d["footprint_m2"] - sum(rect_area(z["r"]) for z in club if z.get("niveau", 0) == 0)
                  if any(z.get("verhuur") for z in L["zones"]) else 0)
    begane = [z["r"] for z in club if z.get("niveau", 0) == 0]
    u0 = min(r[0] for r in begane); v0 = min(r[1] for r in begane)
    u1 = max(r[2] for r in begane); v1 = max(r[3] for r in begane)
    omtrek_extern = 2 * ((u1-u0) + (v1-v0)) - (L["brandwand"]["lengte"] if "brandwand" in L else 0)
    werk = next(z for z in L["zones"] if z["type"] == "werken")
    q = dict(
        club_m2=round(club_m2), verhuur_m2=round(verhuur_m2), dak_club_m2=round(sum(rect_area(r) for r in begane)),
        gevel_isolatie_m2=round(omtrek_extern * 4.5) if L["isoleren"] else 0,
        pui_m2=round(L["pui"]["lengte"] * 3.0),
        brandwand_m2=round(L["brandwand"]["lengte"] * L["brandwand"]["hoogte"]) if "brandwand" in L else 0,
        terras_m2=round(sum(rect_area(b["r"]) for b in L["buiten"] if b["type"] == "terras")),
        tuin_m2=round(sum(rect_area(b["r"]) for b in L["buiten"] if b["type"] == "tuin")),
        bomen_buiten=len(L["bomen_buiten"]),
        buiten_sauna=any(b["type"] == "sauna" for b in L["buiten"]),
        gym_m2=round(sum(rect_area(z["r"]) for z in club if z["type"] == "gym")),
        desks=len(desks(werk["r"])),
        hoogte=d["hoogte"], perceel_m2=(d["perceel"] or {}).get("m2"),
    )
    # capaciteit volgt uit de ruimte; alleen waarschuwen onder de piekvraag (60 eigenaren + 60 clubleden)
    q["gym_cap"] = int(q["gym_m2"] / 7.5)
    q["werk_cap"] = q["desks"] + 12  # + lange werktafel
    q["gym_piek"], q["werk_piek"] = 10, 35
    viewer = dict(
        slug=slug, titel=L["titel"], adres=d["adres"], regio=d.get("regio"), oordeel=L["oordeel"],
        samenvatting=L["samenvatting"], bouwjaar=d["bouwjaar"], hoogte=d["hoogte"], hoogte_bron=d.get("hoogte_bron", "3D BAG"),
        footprint=loc(d["footprint"]), footprint_m2=d["footprint_m2"],
        perceel=loc(d["perceel"]["ring"]) if d["perceel"] and d["perceel"].get("ring") else None,
        context=[dict(ring=loc(c["ring"]), h=c["h"], eigen=bool(c.get("op_perceel"))) for c in d["context"]],
        luchtfoto=dict(file=d["luchtfoto"]["file"], hoeken=[loc([(d["luchtfoto"]["bbox"][0], d["luchtfoto"]["bbox"][1])])[0],
                       loc([(d["luchtfoto"]["bbox"][2], d["luchtfoto"]["bbox"][1])])[0],
                       loc([(d["luchtfoto"]["bbox"][2], d["luchtfoto"]["bbox"][3])])[0],
                       loc([(d["luchtfoto"]["bbox"][0], d["luchtfoto"]["bbox"][3])])[0]]),
        zones=[dict(z, kleur=ZONEKLEUR[z["type"]], m2=round(rect_area(z["r"]))) for z in L["zones"]],
        buiten=L["buiten"], bomen_buiten=L["bomen_buiten"], pui=L["pui"], desks=desks(werk["r"]),
        werkniveau=werk.get("niveau", 0), q=q, pv_kwp=L["pv_kwp"],
    )
    return viewer, q


if __name__ == "__main__":
    for s in LAYOUTS:
        v, q = build(s)
        print(s, q, "desks", len(v["desks"]))
