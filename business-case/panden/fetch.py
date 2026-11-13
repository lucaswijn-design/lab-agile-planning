"""
Stap 1 van de workflow: pand-dossier uit open data.

Per adres:
  PDOK Locatieserver  -> verblijfsobject-id
  BAG (PDOK OGC API)  -> pand: footprint (RD, meters), bouwjaar, alle verblijfsobjecten + m2
  3D BAG              -> hoogte maaiveld, dakhoogte, grond-, dak- en gevelopp.
  BRK kadastrale kaart-> perceel waarop het pand staat (contour + m2)
  BAG + 3D BAG bbox   -> omliggende panden met hoogte (context voor 3D)
  PDOK luchtfoto 8 cm -> orthofoto als ondergrond (CC BY 4.0, Beeldmateriaal Nederland)
Draaien: python3 business-case/panden/fetch.py   (schrijft dossiers/<slug>.json en <slug>.jpg)
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "dossiers")
RD = "http://www.opengis.net/def/crs/EPSG/0/28992"
BAG = "https://api.pdok.nl/kadaster/bag/ogc/v2/collections"
BRK = "https://api.pdok.nl/kadaster/brk-kadastrale-kaart/ogc/v1/collections"

PANDEN = [
    dict(slug="amersfoort-birkt-21", adres="Birkt 21 Amersfoort", regio="Randstadrand",
         aanbod="te koop, € 1.250.000, 785 m² vvo, energieneutraal (zoekresultaat funda in business)"),
    dict(slug="best-de-waal-13", adres="De Waal 13 Best", regio="Brabantse stedenrij",
         aanbod="De Waal 13-15A, bedrijfshal te koop, prijs op aanvraag (zoekresultaat)"),
    dict(slug="best-de-run-5", adres="De Run 5 Best", regio="Brabantse stedenrij",
         aanbod="De Run 3-5, complex in zijn geheel te koop, voorwaarden op aanvraag (zoekresultaat)"),
    dict(slug="woerden-marconiweg-5", adres="Marconiweg 5 Woerden", regio="Randstadrand",
         aanbod="vier nieuwe bedrijfsunits te koop op Honthorst (zoekresultaat)"),
    dict(slug="best-sonseweg-15", adres="Sonseweg 15 Best", regio="Brabantse stedenrij",
         aanbod="bedrijfshal, brochure gevonden; status en prijs onbekend"),
    # ronde 2: ook ander vastgoed dan hallen, alleen Randstad, Utrecht en Brabant
    dict(slug="utrecht-gertrudiskerk", adres="Amaliadwarsstraat 1 Utrecht", regio="Utrecht stad", pand_id="0344100000055175",
         aanbod="Sint-Gertrudiskerk, te koop voor herbestemming (DUIC); prijs onbekend"),
    dict(slug="uithoorn-thamerkerk", adres="Amsteldijk Noord 3 Uithoorn", regio="Amsterdam-rand",
         aanbod="Thamerkerk, bieding, vraagprijs € 1.295.000 (funda in business)"),
    dict(slug="zeist-arendsburg", adres="Utrechtseweg 139 Zeist", regio="Utrecht-oost",
         aanbod="gemeentelijk monument Arendsburg, 672 m², te koop of te huur (funda in business)"),
    dict(slug="zeist-utrechtseweg-131", adres="Utrechtseweg 131 Zeist", regio="Utrecht-oost",
         aanbod="monumentale kantoorvilla, 494 m² over vier lagen (funda in business)"),
    dict(slug="haarlem-kampersingel-42", adres="Kampersingel 42 Haarlem", regio="Haarlem",
         aanbod="wonen en werken: voormalige garage + werkplaats met mezzanine, terras 200 m² (funda)"),
    dict(slug="bunnik-regulierenring-29", adres="Regulierenring 29 Bunnik", regio="Utrecht-oost",
         aanbod="bedrijfshal te koop (funda in business), prijs onbekend"),
    dict(slug="bunnik-provincialeweg-1", adres="Provincialeweg 1 Bunnik", regio="Utrecht-oost",
         aanbod="kantoor te koop (funda in business), prijs onbekend"),
    dict(slug="houten-heemsteedseweg-24", adres="Heemsteedseweg 24 Houten", regio="Utrecht-zuid",
         aanbod="kantoor te koop (funda in business), prijs onbekend"),
    dict(slug="zoeterwoude-industrieweg-36", adres="Industrieweg 36 Zoeterwoude", regio="Leiden-rand",
         aanbod="bedrijfshal 36-B te koop (funda in business), prijs onbekend"),
    dict(slug="haarlem-kuipersweg-4", adres="Kuipersweg 4 Haarlem", regio="Haarlem",
         aanbod="bedrijfshal 4-C1 (funda in business), status onbekend"),
    dict(slug="den-bosch-bloemendaal-10", adres="De Bloemendaal 10 Den Bosch", regio="Den Bosch",
         aanbod="vrijstaand bedrijfsgebouw te koop (funda in business), prijs onbekend"),
    dict(slug="uitgeest-molenwerf-15", adres="Molenwerf 15 Uitgeest", regio="Noord-Holland",
         aanbod="circa 600 m² bedrijfsruimte (funda in business), status onbekend"),
    dict(slug="ter-aar-woudsedijk-11", adres="Woudsedijk 11 Ter Aar", regio="Groene Hart",
         aanbod="bedrijfshal (funda in business), status onbekend"),
]


def get(url, params=None):
    if params:
        url += ("&" if "?" in url else "?") + urllib.parse.urlencode(params)
    out = subprocess.run(["curl", "-sS", "-m", "40", url], capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def area(ring):
    s = 0.0
    for (x1, y1), (x2, y2) in zip(ring, ring[1:] + ring[:1]):
        s += x1 * y2 - x2 * y1
    return abs(s) / 2


def centroid(ring):
    xs = [p[0] for p in ring]
    ys = [p[1] for p in ring]
    return sum(xs) / len(xs), sum(ys) / len(ys)


def inside(pt, ring):
    x, y = pt
    c = False
    for (x1, y1), (x2, y2) in zip(ring, ring[1:] + ring[:1]):
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1 + 1e-12) + x1:
            c = not c
    return c


def outer(geom):
    if geom["type"] == "Polygon":
        return [tuple(p[:2]) for p in geom["coordinates"][0]]
    # MultiPolygon: grootste deel
    rings = [[tuple(p[:2]) for p in poly[0]] for poly in geom["coordinates"]]
    return max(rings, key=area)


def dossier(p):
    loc = get("https://api.pdok.nl/bzk/locatieserver/search/v3_1/free",
              {"q": p["adres"], "fq": "type:adres", "rows": 1,
               "fl": "weergavenaam,adresseerbaarobject_id,centroide_rd"})["response"]["docs"][0]
    if p.get("pand_id"):  # adres wijst naar een buurpand: kies het pand direct
        pand = get(f"{BAG}/pand/items", {"f": "json", "crs": RD, "identificatie": p["pand_id"]})["features"][0]
    else:
        vbo = get(f"{BAG}/verblijfsobject/items", {"f": "json", "identificatie": loc["adresseerbaarobject_id"]})["features"][0]
        pand_href = vbo["properties"]["pand.href"][0]
        pand = get(pand_href, {"f": "json", "crs": RD})
    pp = pand["properties"]
    ring = outer(pand["geometry"])
    # alle verblijfsobjecten in het pand
    vbos = []
    for h in pp.get("verblijfsobject.href", []):
        v = get(h, {"f": "json"})["properties"]
        vbos.append(dict(adres=f'{v["openbare_ruimte_naam"]} {v["huisnummer"]}{v.get("huisletter") or ""}{v.get("toevoeging") or ""}',
                         oppervlakte=v["oppervlakte"], gebruiksdoel=v["gebruiksdoel"], status=v["status"]))
    pid = pp["identificatie"]
    try:
        b3 = get(f"https://api.3dbag.nl/collections/pand/items/NL.IMBAG.Pand.{pid}")
        a = b3.get("feature", b3)["CityObjects"][f"NL.IMBAG.Pand.{pid}"].get("attributes", {})
        hoogte = (a.get("b3_h_dak_70p") or 0) - (a.get("b3_h_maaiveld") or 0)
        h_bron = "3D BAG"
    except Exception:  # nieuwbouw staat nog niet in 3D BAG
        a, hoogte, h_bron = {}, 8.0, "aanname (nog niet in 3D BAG)"
    cx, cy = centroid(ring)
    # perceel onder het pand
    d = 25
    pr = get(f"{BRK}/perceel/items", {"f": "json", "crs": RD, "bbox-crs": RD, "limit": 50,
                                       "bbox": f"{cx-d},{cy-d},{cx+d},{cy+d}"})
    perceel = None
    for f in pr.get("features", []):
        r = outer(f["geometry"])
        if inside((cx, cy), r):
            if area(r) > 15 * area(ring):
                perceel = dict(ring=None, m2=None, ongesplitst=round(area(r)),
                               opmerking="perceel nog niet gesplitst (groot terreinperceel)")
                break
            perceel = dict(ring=r, m2=round(area(r)), id=f["properties"].get("identificatie_lokaal_id")
                           or f["properties"].get("perceelnummer"), props={k: f["properties"].get(k) for k in
                           ("kadastrale_gemeente_waarde", "sectie", "perceelnummer", "kadastrale_grootte_waarde")})
            break
    # context: omliggende panden binnen 90 m
    R = 90
    ctx = get(f"{BAG}/pand/items", {"f": "json", "crs": RD, "bbox-crs": RD, "limit": 300,
                                    "bbox": f"{cx-R},{cy-R},{cx+R},{cy+R}"})
    hmap = {}
    url = f"https://api.3dbag.nl/collections/pand/items?bbox={cx-R},{cy-R},{cx+R},{cy+R}&limit=100"
    for _ in range(6):
        try:
            b = get(url)
        except Exception:
            break
        for f in b.get("features", []):
            for k, v in f["CityObjects"].items():
                at = v.get("attributes") or {}
                if "b3_h_dak_70p" in at:
                    hmap[k.replace("NL.IMBAG.Pand.", "")] = round((at["b3_h_dak_70p"] or 0) - (at["b3_h_maaiveld"] or 0), 1)
        nxt = [l["href"] for l in b.get("links", []) if l.get("rel") == "next"]
        if not nxt:
            break
        url = nxt[0]
    context = []
    op_perceel = []
    for f in ctx.get("features", []):
        i = f["properties"]["identificatie"]
        if i == pid:
            continue
        r = outer(f["geometry"])
        item = dict(id=i, ring=r, h=hmap.get(i, 6.0), bouwjaar=f["properties"].get("bouwjaar"), m2=round(area(r)))
        if perceel and perceel.get("ring") and inside(centroid(r), perceel["ring"]):
            item["op_perceel"] = True
            op_perceel.append(dict(id=i, m2=item["m2"], h=item["h"], bouwjaar=item["bouwjaar"]))
        context.append(item)
    # luchtfoto
    os.makedirs(OUT, exist_ok=True)
    img = os.path.join(OUT, p["slug"] + ".jpg")
    wms = ("https://service.pdok.nl/hwh/luchtfotorgb/wms/v1_0?service=WMS&version=1.3.0&request=GetMap"
           f"&layers=Actueel_orthoHR&styles=&crs=EPSG:28992&bbox={cx-R},{cy-R},{cx+R},{cy+R}"
           "&width=1024&height=1024&format=image/jpeg")
    subprocess.run(["curl", "-sS", "-m", "60", "-o", img, wms], check=True)
    return dict(slug=p["slug"], adres=loc["weergavenaam"], regio=p["regio"], aanbod=p["aanbod"],
                pand_id=pid, bouwjaar=pp.get("bouwjaar"), aantal_vbo=pp.get("aantal_verblijfsobjecten"),
                vbos=vbos, vbo_m2_totaal=sum(v["oppervlakte"] for v in vbos),
                footprint=ring, footprint_m2=round(area(ring)), centrum=[cx, cy],
                hoogte=round(hoogte, 1), hoogte_bron=h_bron, h3d={k: a.get(k) for k in ("b3_opp_grond", "b3_opp_dak_plat",
                "b3_opp_dak_schuin", "b3_opp_buitenmuur", "b3_h_maaiveld", "b3_h_dak_70p", "b3_h_dak_max")},
                perceel=perceel, op_perceel=op_perceel, context=context, luchtfoto=dict(bbox=[cx-R, cy-R, cx+R, cy+R], file=os.path.basename(img)))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for p in PANDEN:
        if os.path.exists(os.path.join(OUT, p["slug"] + ".json")) and "--force" not in sys.argv:
            continue
        try:
            d = dossier(p)
        except Exception as e:  # noqa: BLE001
            print("FOUT", p["adres"], e)
            continue
        with open(os.path.join(OUT, p["slug"] + ".json"), "w") as f:
            json.dump(d, f, ensure_ascii=False)
        print(f'{d["adres"]:<34} bouwjaar {d["bouwjaar"]}  footprint {d["footprint_m2"]} m2  hoogte {d["hoogte"]} m  '
              f'vbo {d["aantal_vbo"]} ({d["vbo_m2_totaal"]} m2)  perceel {(d["perceel"] or {}).get("m2") or (d["perceel"] or {}).get("opmerking")}  '
              f'context {len(d["context"])} panden, op perceel {d["op_perceel"]}')
        for v in d["vbos"][:8]:
            print("   ", v)
