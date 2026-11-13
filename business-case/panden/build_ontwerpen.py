"""
Bouwt ontwerpen.html: maquette (dak eraf, dak dicht, huidig), plattegrond, inrichting per ruimte en dakterrasoptie.
Draaien: python3 ontwerp.py && python3 build_ontwerpen.py
"""
from __future__ import annotations

import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ontwerp  # noqa: E402
import pand_case  # noqa: E402
from tekening import basis, gebouwen, tekening  # noqa: E402
from layout import LAYOUTS  # noqa: E402

VOLGORDE = ["utrecht-van-heutszstraat-4", "den-bosch-rietveldenweg-13", "den-bosch-eendenkooi-1a", "voorhout-dinsdagse-wetering-56a", "maarssen-herenweg-15"]
TORENS = {"utrecht-van-heutszstraat-4": True, "den-bosch-rietveldenweg-13": True, "den-bosch-eendenkooi-1a": False,
          "voorhout-dinsdagse-wetering-56a": True, "maarssen-herenweg-15": True}


def werkplekken(O):
    n = sum(1 for e in O["elementen"] if e["t"] == "bureau")
    for e in O["elementen"]:
        if e["t"] == "box" and e.get("soort") == "werktafel":
            n += 2 * int(e["w"] / 1.0)
        if e["t"] == "box" and e.get("soort") == "raambar":
            n += int(e["w"] / 0.8)
    return n


def pand(slug):
    O = json.load(open(os.path.join(HERE, "ontwerp", slug + ".json")))
    d, fp, noord, ctx = basis(slug)
    G, ctx = gebouwen(O, fp, ctx)
    xs = [p[0] for g in G for p in g["ring"]]; ys = [p[1] for g in G for p in g["ring"]]
    cx, cz = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    size = max(max(xs) - min(xs), max(ys) - min(ys))
    ctx = [c for c in ctx if math.dist(ontwerp_c(c["ring"]), (cx, cz)) < 75]
    t = TORENS[slug]
    r = pand_case.run(slug, torens=t)
    kpi = dict(koop=LAYOUTS[slug]["koop"]["totaal"], capex=r["capex"], fee=r["fee_vol_nodig"], inleg=pand_case.fee_inleg_terug(slug, torens=t),
               ltv=r["ltv"], werkplekken=werkplekken(O))
    rows = ontwerp.dakterras_rows(slug)
    terras = None
    if rows:
        rt = pand_case.run(slug, torens=t, extra=rows)
        terras = dict(rows=rows, totaal=sum(x["totaal"] for x in rows), fee=rt["fee_vol_nodig"], inleg=pand_case.fee_inleg_terug(slug, torens=t, extra=rows))
    plans = [dict(naam="Begane grond", svg=tekening(slug, 0))]
    if O.get("niveaus"):
        plans.append(dict(naam="Verdieping", svg=tekening(slug, 1)))
    return dict(slug=slug, footprint=fp, gebouwen=G, context=ctx, ontwerp=O, cx=cx, cz=cz, size=size, noord=noord, kpi=kpi, terras=terras, plans=plans)


def ontwerp_c(ring):
    return (sum(p[0] for p in ring) / len(ring), sum(p[1] for p in ring) / len(ring))


def main():
    data = [pand(s) for s in VOLGORDE]
    tpl = open(os.path.join(HERE, "maquette_template.html"), encoding="utf-8").read()
    html = tpl.replace("/*__DATA__*/null", json.dumps(data, ensure_ascii=False, separators=(",", ":")))
    out = os.path.join(HERE, "ontwerpen.html")
    open(out, "w", encoding="utf-8").write(html)
    print("geschreven", out, round(len(html) / 1e6, 2), "MB")
    for p in data:
        print(p["slug"], p["kpi"], p["terras"] and (p["terras"]["totaal"], p["terras"]["fee"], p["terras"]["inleg"]))


if __name__ == "__main__":
    main()
