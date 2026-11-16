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

# Ronde 7 (15 november 2026): Voorhout en Uden vallen af op het verzorgingsgebied; de ontwerpen blijven in ontwerp.py staan.
VOLGORDE = ["utrecht-van-heutszstraat-4", "den-bosch-rietveldenweg-13", "den-bosch-eendenkooi-1a", "maarssen-herenweg-15",
            "pernis-ring-15", "rotterdam-galvanistraat-122", "schiedam-calandstraat-92", "rotterdam-metaalhof-40", "rotterdam-linschotenstraat-20a", "nieuwbouw-atriumhal"]
SOBER = True  # sobere industriële afwerking met hergebruikte materialen (sober.py), sinds 15 november 2026
TORENS = {"utrecht-van-heutszstraat-4": True, "den-bosch-rietveldenweg-13": True, "den-bosch-eendenkooi-1a": False,
          "voorhout-dinsdagse-wetering-56a": True, "maarssen-herenweg-15": True,
          "pernis-ring-15": True, "uden-nijverheidsstraat-4c": True, "nieuwbouw-atriumhal": True,
          "rotterdam-galvanistraat-122": True, "schiedam-calandstraat-92": True, "rotterdam-metaalhof-40": True, "rotterdam-linschotenstraat-20a": True}

for _s in sorted(f[:-3] for f in os.listdir(os.path.join(HERE, "ontwerpen_extra")) if f.endswith(".py") and not f.startswith("_")):
    if _s not in ontwerp.ONTWERPEN or _s not in LAYOUTS or not os.path.exists(os.path.join(HERE, "ontwerp", _s + ".json")):
        continue   # nog niet compleet (ontwerp, layout of export ontbreekt)
    if _s not in VOLGORDE:
        VOLGORDE.insert(len(VOLGORDE) - 1, _s)   # voor de nieuwbouw, die blijft achteraan
    TORENS.setdefault(_s, True)

# Omgevingsplan (16-11-2026): panden waar coworking volgens de planregels niet mag, vallen af (omgevingsplan_check.py).
from omgevingsplan_check import GESCHRAPT  # noqa: E402
VOLGORDE[:] = [s for s in VOLGORDE if s not in GESCHRAPT]
if "rotterdam-metaalhof-40" in VOLGORDE:  # sterkste combinatie naar voren
    VOLGORDE.remove("rotterdam-metaalhof-40"); VOLGORDE.insert(1, "rotterdam-metaalhof-40")


def werkplekken(O):
    """Zit-sta bureaus + plekken aan de grote tafel + krukken aan de raambar (60 cm per kruk)."""
    n = sum(1 for e in O["elementen"] if e["t"] == "bureau")
    for e in O["elementen"]:
        if e["t"] == "box" and e.get("soort") in ("grote tafel", "werktafel"):
            n += e.get("pers") or 2 * int(e["w"] / 0.7)
        if e["t"] == "box" and e.get("soort") == "raambar":
            n += int(e["w"] / 0.6)
    return n


def telling(O):
    E = O["elementen"]
    return dict(bureaus=sum(1 for e in E if e["t"] == "bureau"),
                vergaderkamers=[("sta " if e.get("sta") else "") + str(e.get("pers", 8)) for e in E if e.get("soort") == "vergaderkamer"],
                belcellen=sum(1 for e in E if e.get("soort") == "belcel"),
                werkplekken=werkplekken(O))


def pand(slug):
    O = json.load(open(os.path.join(HERE, "ontwerp", slug + ".json")))
    d, fp, noord, ctx = basis(slug)
    G, ctx = gebouwen(O, fp, ctx)
    xs = [p[0] for g in G for p in g["ring"]]; ys = [p[1] for g in G for p in g["ring"]]
    cx, cz = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    size = max(max(xs) - min(xs), max(ys) - min(ys))
    ctx = [c for c in ctx if math.dist(ontwerp_c(c["ring"]), (cx, cz)) < 75]
    plans = [dict(naam=["Begane grond", "Verdieping 3,6 m", "Kroon 7,0 m"][n] if O.get("nieuwbouw") else ["Begane grond", "Verdieping"][n], svg=tekening(slug, n))
             for n in [0] + [int(k) for k in O.get("niveaus", {})]]
    if O.get("nieuwbouw"):  # geen pand_case: bottom-up nieuwbouwmodel (atrium.py), 80 eigenaren + 30 clubleden
        import atrium
        r = atrium.run(40, 40, 30, werkplekken=werkplekken(O))
        kpi = dict(koop=r["groepen"]["Grond"], koop_label="Grond (kavel 1.400 m²)", capex=r["capex"], fee=r["fee_run"], inleg=r["fee_inleg"], ltv=r["ltv"],
                   werkplekken=werkplekken(O), **{k: v for k, v in telling(O).items() if k != 'werkplekken'})
        return dict(slug=slug, footprint=fp, gebouwen=G, context=ctx, ontwerp=O, cx=cx, cz=cz, size=size, noord=noord, kpi=kpi, terras=None, plans=plans)
    t = TORENS[slug]
    r = pand_case.run(slug, torens=t, sober=SOBER)
    kpi = dict(koop=LAYOUTS[slug]["koop"]["totaal"], capex=r["capex"], fee=r["fee_vol_nodig"], inleg=pand_case.fee_inleg_terug(slug, torens=t, sober=SOBER),
               ltv=r["ltv"], ltv_koop=r["ltv_koop"], inleg_vol_nodig=r["inleg_vol_nodig"], inleg_deel_nodig=r["inleg_deel_nodig"],
               dekking=round(min(r["exit_dekking"], 9), 2), dekking_max=round(min(pand_case.dekking_bij(slug, 2000, torens=t, sober=SOBER), 9), 2),
               personeel=sum(b for n, b in r["opex_rows"] if n.startswith(("Host", "Beheer en techniek"))),
               werkplekken=werkplekken(O), **{k: v for k, v in telling(O).items() if k != 'werkplekken'})
    rows = ontwerp.dakterras_rows(slug)
    terras = None
    if rows:
        rt = pand_case.run(slug, torens=t, extra=rows, sober=SOBER)
        terras = dict(rows=rows, totaal=sum(x["totaal"] for x in rows), fee=rt["fee_vol_nodig"], inleg=pand_case.fee_inleg_terug(slug, torens=t, extra=rows, sober=SOBER))
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
