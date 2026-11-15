"""
Inrichtingsprogramma (16 november 2026): wat elke club op het drukste moment echt nodig heeft, met strengere normen dan capaciteit.py,
en wat elk uitgewerkt ontwerp daarvan biedt. Normen zijn [aanname] tenzij vermeld; onderbouwing in inrichting/onderzoek.md.

  belcellen      1 per 8 werkers op de piek (hybride werk: veel videobellen), plus 1 focuskamer voor 2 per 25 werkers
  lounge         zachte zitplekken los van het café: 25% van de werkers + 4
  lockers        vaste locker voor elke eigenaar + dagkluisjes voor 2x de sporters op het piekuur + 10 voor gasten
                 kolom van 30 cm breed, 5 hoog: 16 lockers per meter wand
  fietsen        60% van de aanwezigen op de piek
  garderobe      haken voor 60% van de aanwezigen, 8 per meter
  planten        1 grote plant (1,2 tot 2 m) per 20 m2 club, 1 boom (2,5 tot 4 m) per 60 m2, hangplanten waar geen vloer is

Draaien: python3 inrichting/programma.py
"""
from __future__ import annotations

import json
import math
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
from capaciteit import vraag  # noqa: E402

WERKERS_PER_BELCEL = 8
WERKERS_PER_FOCUS = 25
LOCKERS_PER_M = 16


def nodig(V, D, C):
    v = vraag(V, D, C)
    w = v["werkplekken"]
    lockers = V + D + math.ceil(2 * v["gym_tegelijk"]) + 10
    return dict(werkplekken=w, belcellen=math.ceil(w / WERKERS_PER_BELCEL), focuskamers=math.ceil(w / WERKERS_PER_FOCUS),
                vergaderkamers=math.ceil(v["vergaderkamers"]), lounge=math.ceil(0.25 * w) + 4, cafe=v["cafe_stoelen"],
                lockers=lockers, locker_m=round(lockers / LOCKERS_PER_M, 1), fietsen=math.ceil(0.6 * v["aanwezig"]),
                garderobe_m=round(0.6 * v["aanwezig"] / 8, 1), toiletten=v["toiletten"], douches=v["douches"])


def bieden(O):
    E = O["elementen"]
    soort = lambda s: [e for e in E if e.get("soort") == s]
    lounge = 0
    for e in E:
        if e["t"] == "boog" and e.get("soort") == "bank":
            lounge += int(math.radians(abs(e["a1"] - e["a0"])) * e["r"] / 0.6)
        if e.get("soort") in ("fauteuil", "poef"):
            lounge += 1
        if e.get("soort") in ("bank", "hexbank", "zitnis") and e["t"] == "box":
            lounge += int(e["w"] / 0.6)
        if e.get("soort") == "trap" and e.get("kleur") == "#b08a5e" and e["w"] >= 2.5:  # houten zittrap: drie treden zitplek
            lounge += int(e["w"] / 0.6) * 3
    lockers = sum(int(e["w"] * LOCKERS_PER_M) for e in soort("lockers"))
    return dict(belcellen=len(soort("belcel")), focuskamers=len(soort("focuskamer")), lounge=lounge, lockers=lockers,
                planten=sum(1 for e in E if e["t"] == "plant" and e.get("naam") != "klimop"), bomen=sum(1 for e in E if e["t"] == "boom"))


def toets(slug):
    import layout
    L = layout.LAYOUTS.get(slug, {}).get("leden") or dict(n_vol=40, n_deel=40, n_club=30)
    O = json.load(open(os.path.join(HERE, "ontwerp", slug + ".json")))
    n, b = nodig(L["n_vol"], L["n_deel"], L["n_club"]), bieden(O)
    m2 = sum(z["m2"] for z in O["zones"])
    return dict(slug=slug, leden=L, nodig=n, biedt=b, planten_nodig=math.ceil(m2 / 20), bomen_nodig=math.ceil(m2 / 60), m2=m2)


if __name__ == "__main__":
    from build_ontwerpen import VOLGORDE
    for s in VOLGORDE:
        t = toets(s)
        n, b = t["nodig"], t["biedt"]
        print(f'{s[:28]:28} belcel {b["belcellen"]}/{n["belcellen"]} focus {b["focuskamers"]}/{n["focuskamers"]} lounge {b["lounge"]}/{n["lounge"]} '
              f'lockers {b["lockers"]}/{n["lockers"]} ({n["locker_m"]} m) planten {b["planten"]}/{t["planten_nodig"]} bomen {b["bomen"]}/{t["bomen_nodig"]}')
