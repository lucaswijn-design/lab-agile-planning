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
    # ronde 3: aanbod dat op twee sites als beschikbaar staat (ongedateerd, medium zekerheid)
    dict(slug="boxtel-bosscheweg-85", adres="Bosscheweg 85 Boxtel", regio="Brabantse stedenrij",
         aanbod="Villa Catharina, kantoorvilla 1899, 709 m², tuin 9.866 m² met zwembad; € 2.950.000 k.k."),
    dict(slug="hilversum-heuvellaan-50", adres="Heuvellaan 50 Hilversum", regio="Gooi",
         aanbod="nieuwe kantoorvilla 2026, 637 m² over drie lagen; € 2.700.000 v.o.n."),
    dict(slug="tilburg-bredaseweg-443", adres="Bredaseweg 443 Tilburg", regio="Tilburg",
         aanbod="kantoorvilla 1942 + uitbreiding 2000, circa 1.241 m², terrein circa 8.000 m² bij de Warande; prijs op aanvraag"),
    dict(slug="den-haag-pomonaplein-49", adres="Pomonaplein 49 Den Haag", regio="Den Haag",
         aanbod="voormalige kerk 1936, 961 m² (woning + loft + B&B); € 4.250.000 k.k."),
    dict(slug="amersfoort-stadsring-103", adres="Stadsring 103 Amersfoort", regio="Amersfoort",
         aanbod="kantoorvilla 1887, monument, 431 m²; € 2.200.000 k.k."),
    dict(slug="woerden-wagenmakersweg-2", adres="Wagenmakersweg 2 Woerden", regio="Woerden",
         aanbod="bedrijfscomplex 1976 (kantoor, werkplaats, woning), 529 m², perceel circa 2.000 m²; € 1.495.000 k.k. (oude advertentie)"),
    dict(slug="rotterdam-hillevliet-139", adres="Hillevliet 139 Rotterdam", regio="Rotterdam",
         aanbod="Leger des Heils-kerk 1929 (J.J.P. Oud, rijksmonument), circa 713 m² bvo + woning; € 950.000 k.k. (sinds 2024)"),
    # ronde 7: eerst de wijk, dan het pand; gecontroleerd 15-11-2026
    dict(slug="rotterdam-galvanistraat-122", adres="Galvanistraat 122 Rotterdam", regio="Rotterdam West / Schiedam",
         aanbod="bedrijfshal 2000, hal 425 m² + kantoor 271 m², vrije hoogte 5,9 m, lichtstraten, € 1.125.000 k.k.; beschikbaar sinds 22-05-2026 (oozo, gecontroleerd 15-11-2026)"),
    dict(slug="rotterdam-motorstraat-7", adres="Motorstraat 7 Rotterdam", regio="Rotterdam Zuid",
         aanbod="maatschappelijk vastgoed, 1.057 m², label A+, € 1.250.000 k.k.; beschikbaar sinds 02-12-2025 (oozo, gecontroleerd 15-11-2026)"),
    dict(slug="utrecht-westerdijk-18", adres="Westerdijk 18 Utrecht", regio="Utrecht Pijlsweerd",
         aanbod="bedrijfshal 2020, 618 m², € 1.150.000 k.k.; beschikbaar sinds 18-12-2025 (oozo, gecontroleerd 15-11-2026)"),
    dict(slug="weesp-pampuslaan-153", adres="Pampuslaan 153 Weesp", regio="Weesp / Amsterdam-Oost",
         aanbod="bedrijfshal 1975, 918 m², vrije hoogte 5,8 m, overspanning 9 m, perceel 1.079 m², € 935.000 k.k. (oozo, ronde 7)"),
    dict(slug="schiedam-calandstraat-92", adres="Calandstraat 92 Schiedam", regio="Schiedam",
         aanbod="bedrijfshal 1980, hal 800 + kantoor 200 m², erfpacht, € 825.000 k.k. (oozo, ronde 7)"),
    dict(slug="rotterdam-anthonetta-kuijlstraat-51b", adres="Anthonetta Kuijlstraat 51B Rotterdam", regio="Rotterdam Prins Alexander",
         aanbod="bedrijfshal 1996, hal 560 + kantoor 229 m², perceel 1.073 m², € 595.000 k.k.; aangeboden sinds 23-10-2024 (oozo, gecontroleerd 15-11-2026)"),
    dict(slug="rotterdam-metaalhof-40", adres="Metaalhof 40 Rotterdam", regio="Rotterdam Prins Alexander",
         aanbod="bedrijfshal 1986, hal 340 + kantoor 582 m², vrije hoogte 6 m, 3 parkeerplaatsen, € 1.150.000 k.k. (oozo, ronde 7)"),
    dict(slug="den-haag-zilverstraat-56", adres="Zilverstraat 56 Den Haag", regio="Den Haag Zuidwest",
         aanbod="hal met entresol 1993, BVO 872 m², 6,1 m onder spant, 6 parkeerplaatsen, € 1.299.500 k.k. (bedrijfspand.com, ronde 7)"),
    # ronde 8
    dict(slug="rotterdam-linschotenstraat-20a", adres="Linschotenstraat 20A Rotterdam", regio="Rotterdam Spaanse Polder / Schiedam",
         aanbod="bedrijfshal 2010, hal 452 + kantoor 117 m², vrije hoogte 9 m, overspanning 17 m, lichtstraten, 5 parkeerplaatsen, perceel 506 m², € 899.000 k.k.; online sinds 29-10-2022 (oozo; funda in business status onduidelijk)"),
    dict(slug="rotterdam-koepelstraat-30", adres="Koepelstraat 30 Rotterdam", regio="Rotterdam Noord / Rubroek",
         aanbod="beleggingsobject 1955, 586 m², woonwijk Rubroek, € 655.000 k.k.; online sinds 22-06-2026 (oozo; makelaar Spring Real Estate)"),
    # ronde 6: grootteklassen, gecontroleerd 14-11-2026
    dict(slug="tilburg-ledeboerstraat-29e", adres="Ledeboerstraat 29E Tilburg", regio="Tilburg",
         aanbod="bedrijfshal 2020, 456 m², vrije hoogte 8 m, 2 eenheden beschikbaar, € 575.000 k.k.; te koop op 14-11-2026 (bedrijfspand.com)"),
    dict(slug="pernis-ring-15", adres="Ring 15 Rotterdam", regio="Rotterdam-Pernis",
         aanbod="dorpspand 1852, maatschappelijk vastgoed, 551 m², perceel 935 m², € 590.000 k.k.; beschikbaar sinds 15-07-2026 (oozo)"),
    dict(slug="uden-nijverheidsstraat-4c", adres="Nijverheidsstraat 4C Uden", regio="Uden/Den Bosch",
         aanbod="nieuwbouw bedrijfshal, 846 m², vrije hoogte 9,5 m, € 949.000 v.o.n.; te koop op 14-11-2026 (bedrijfspand.com)"),
    # ronde 5: advertenties met datum vanaf september 2026
    dict(slug="voorhout-dinsdagse-wetering-56a", adres="Dinsdagse Wetering 56A Voorhout", regio="Leiden/Haarlem",
         aanbod="twee werkplaatsen (deels 1933) op 824 m² grond met erf, circa 570 m² vrijwel gelijkvloers, € 699.500 k.k.; online 27-10-2026 (bedrijfspand.com, oozo)"),
    dict(slug="maarssen-herenweg-15", adres="Herenweg 15 Maarssen", regio="Utrecht-noord", vbo_id="0333010000005723",
         aanbod="bedrijfsgebouw 1970 met woning, hal 760 m² + kantoor 80 m², perceel 1.405 m², € 1.085.000 k.k.; online 28-10-2026 (oozo, fundainbusiness)"),
    dict(slug="maassluis-govert-van-wijnkade-18", adres="Govert van Wijnkade 18 Maassluis", regio="Rotterdam-west",
         aanbod="hal + kantoor, 529 m² gelijkvloers, € 850.000 k.k.; aangeboden sinds 15-09-2026 (oozo, Dolphijn)"),
    dict(slug="voorschoten-starrenburglaan-19", adres="Starrenburglaan 19 Voorschoten", regio="Leiden/Den Haag",
         aanbod="bedrijfsunit 2004, 465 m² over twee lagen, € 995.000 k.k.; online 30-10-2026 (bedrijfspand.com)"),
    dict(slug="castricum-bakkummerstraat-56b", adres="Bakkummerstraat 56B Castricum", regio="Noord-Holland",
         aanbod="kantoor/bedrijfsgebouw 1990, 598 m² over twee lagen, perceel 1.099 m², € 850.000 k.k.; aangeboden sinds 26-10-2026 (oozo)"),
    dict(slug="weesp-flevolaan-19b", adres="Flevolaan 19B Weesp", regio="Amsterdam-oost",
         aanbod="bedrijfsunit met showroom 1978, 615 m², € 799.950 k.k., verhuurd tot 1-11-2027; online 14-10-2026 (bedrijfspand.com)"),
    # ronde 4: geopende advertenties op bedrijfspand.com / oozo, november 2026
    dict(slug="den-bosch-eendenkooi-1a", adres="De Eendenkooi 1A 's-Hertogenbosch", regio="Den Bosch",
         aanbod="sport- en fitnessgebouw 1977 + bovenwoning, circa 994 m², € 1.400.000 k.k.; te koop sinds 14-15 oktober 2026 (bedrijfspand.com, oozo)"),
    dict(slug="utrecht-van-heutszstraat-4", adres="Van Heutszstraat 4 Utrecht", regio="Utrecht stad",
         aanbod="bedrijfsgebouw circa 1960 aan binnenterrein in Lombok, 665 m² gelijkvloers, erfpacht afgekocht, € 670.000 k.k.; online sinds 12 maart 2026 (bedrijfspand.com)"),
    dict(slug="helmond-mierloseweg-130", adres="Mierloseweg 130 Helmond", regio="Helmond/Eindhoven",
         aanbod="Villa de Raymaert, monument, 1.032 m², tuin en terras, € 1.450.000 k.k.; online sinds 27 november 2025 (bedrijfspand.com)"),
    dict(slug="amersfoort-computerweg-37", adres="Computerweg 37 Amersfoort", regio="Amersfoort",
         aanbod="kantoor/bedrijfsgebouw 1987, 811 m² (hal 206 m²), label A++, perceel 950 m², € 1.325.000; online sinds 7 juli 2026 (bedrijfspand.com)"),
    dict(slug="capelle-lentedans-50a", adres="Lentedans 50A Capelle aan den IJssel", regio="Rotterdam-oost",
         aanbod="kantoorvilla 1984 in groen kantorenpark, circa 550 m², € 1.075.000 k.k.; online sinds 16 september 2026 (bedrijfspand.com)"),
    dict(slug="den-bosch-rietveldenweg-13", adres="Rietveldenweg 13 's-Hertogenbosch", regio="Den Bosch",
         aanbod="showroom/bedrijfsruimte 1966, 890 m² gelijkvloers + woning, perceel 1.156 m², € 975.000 k.k.; online sinds 5 november 2026 (bedrijfspand.com)"),
    dict(slug="bergen-op-zoom-bosstraat-38", adres="Bosstraat 38 Bergen op Zoom", regio="West-Brabant",
         aanbod="pandcomplex circa 1750 in het centrum, circa 1.000 m² over twee lagen, € 625.000 k.k.; online sinds 4 januari 2026 (bedrijfspand.com)"),
    dict(slug="dordrecht-houttuinen-32a", adres="Houttuinen 32A Dordrecht", regio="Dordrecht",
         aanbod="voormalig Arsenaal, rijksmonument, 838 m² over drie lagen, € 1.550.000 k.k.; online sinds 26 november 2025 (bedrijfspand.com)"),
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
        vbo = get(f"{BAG}/verblijfsobject/items", {"f": "json", "identificatie": p.get("vbo_id") or loc["adresseerbaarobject_id"]})["features"][0]
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
