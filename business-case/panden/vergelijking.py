"""
Vergelijking van alle uitgewerkte panden (17 november 2026): één tabel met wat Lucas nodig heeft om te kiezen.
Bronnen: build_ontwerpen (kosten, sober), layout (leden), capaciteit.max_leden, inrichting/programma.toets, ronde7/8/9 (wijk, status),
inrichting/omgevingsplan.json (kans omgevingsplan), inrichting/lidmaatschap (soorten).
Draaien: python3 vergelijking.py -> vergelijking.html
"""
from __future__ import annotations

import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "ronde7"))
sys.path.insert(0, os.path.join(HERE, "ronde8"))
sys.path.insert(0, os.path.join(HERE, "ronde9"))
sys.path.insert(0, os.path.join(HERE, "inrichting"))

import build_ontwerpen as b  # noqa: E402
import capaciteit  # noqa: E402
import layout  # noqa: E402
import ontwerp  # noqa: E402
import programma  # noqa: E402

MIX = {"vast": 1 / 6, "flex": 5 / 18, "flex 3": 1 / 3, "flex 2": 2 / 9}   # verdeling zoals in de business case (15/25/30/20 van 90)
GEWICHT = {"vast": 1.25, "flex": 1.0, "flex 3": 0.8, "flex 2": 0.6}


def wijkdata():
    """Verzamel kern/breed/status per adres uit alle rondes."""
    out = {}
    try:
        H = json.load(open(os.path.join(HERE, "ronde7", "ronde7_herbeoordeling.json")))["locaties"]
        for x in H:
            m = x["metrics"]
            out[x["naam"].lower()] = dict(kern=m.get("leden_kern"), breed=m.get("leden_breed"), auto=m.get("leden_breed_auto"),
                                          status=x.get("status"), parkeren=x.get("parkeren"), station_km=m.get("station_km"))
    except Exception:  # noqa: BLE001
        pass
    for modnaam in ("kandidaten7", "kandidaten8", "kandidaten9"):
        try:
            mod = __import__(modnaam)
        except Exception:  # noqa: BLE001
            continue
        for naam, m in mod.META.items():
            out[naam.lower()] = dict(kern=m.get("leden_kern"), breed=m.get("leden_breed"), auto=m.get("leden_breed_auto"),
                                     status=m.get("status") or m.get("bron_status"), parkeren=m.get("parkeren"), station_km=m.get("station_km"),
                                     zekerheid=m.get("zekerheid"))
    return out


def omgevingsplan():
    p = os.path.join(HERE, "inrichting", "omgevingsplan.json")
    if not os.path.exists(p):
        return {}
    return {x["adres"].split(",")[0].strip().lower(): x for x in json.load(open(p))}


def zoek(dic, titel):
    t = titel.split(",")[0].lower()
    for k, v in dic.items():
        if k and (k in t or t.startswith(k) or k.startswith(t)):
            return v
    # eerste woord + nummer
    w = t.split()
    for k, v in dic.items():
        if len(w) >= 2 and w[0] in k and w[-1].split("-")[0] in k:
            return v
    return {}


def rij(slug, W, OP):
    p = b.pand(slug)
    O, k = p["ontwerp"], p["kpi"]
    L = layout.LAYOUTS.get(slug) or dict(leden=dict(n_vol=40, n_deel=40, n_club=30), oordeel="concept: zelf bouwen op een bedrijfskavel", samenvatting="")
    le = L["leden"]
    V, D, C = le["n_vol"], le["n_deel"], le["n_club"]
    try:
        ml = capaciteit.max_leden(slug, 0.5, C)
    except Exception:  # noqa: BLE001
        ml = dict(eigenaren=None, knelt={})
    t = programma.toets(slug)
    n_, bi = t["nodig"], t["biedt"]
    normen = {kk: (bi[kk], n_[kk]) for kk in ("belcellen", "focuskamers", "lounge", "lockers")}
    ok = sum(1 for a, c in normen.values() if a >= c)
    titel = O["titel"]
    w = zoek(W, titel)
    op = zoek(OP, titel)
    if slug == "nieuwbouw-atriumhal":
        op = next((v for kk, v in OP.items() if "nieuw" in kk or "kavel" in kk), {})
    m2 = sum(z["m2"] for z in O["zones"])
    # soorten: zelfde totale opbrengst als fee_vol x (V + 0,711 D)
    n = V + D
    units = sum(n * MIX[s] * GEWICHT[s] for s in MIX)
    unit = k["fee"] * (V + D * 320 / 450) / units if units else 0
    soorten = {s: round(unit * GEWICHT[s]) for s in MIX}
    klasse = "klein" if n <= 45 else ("middel" if n <= 70 else "groot")
    nieuw = slug == "nieuwbouw-atriumhal"
    return dict(slug=slug, titel=titel, sub=O.get("sub", ""), klasse=klasse, prijs=k["koop"], prijs_label=k.get("koop_label") or "Vraagprijs",
                m2=m2, hoogte=O.get("hoogte"), eigenaren=n, vol=V, deel=D, club=C, max_eigenaren=ml.get("eigenaren"), werkplekken=k["werkplekken"],
                vergaderkamers=k.get("vergaderkamers"), belcellen=k.get("belcellen"), capex=k["capex"], fee=k["fee"], inleg=k["inleg"], ltv=k["ltv"], ltv_koop=k.get("ltv_koop"), inleg_vol_nodig=k.get("inleg_vol_nodig"),
                inleg_deel_nodig=k.get("inleg_deel_nodig"), dekking=k.get("dekking"), dekking_max=k.get("dekking_max"), personeel=k.get("personeel"),
                soorten=soorten, kern=w.get("kern"), breed=w.get("breed"), auto=w.get("auto"), status=(w.get("status") or L.get("oordeel") or "")[:160],
                zekerheid=w.get("zekerheid"), parkeren=(w.get("parkeren") or "")[:80], station_km=w.get("station_km"),
                op_kans=op.get("kans"), op_route=op.get("route"), op_onderbouwing=(op.get("onderbouwing") or "")[:260], op_tip=(op.get("tip") or "")[:200],
                op_bestemming=op.get("bestemming"), normen=normen, normen_ok=ok, oordeel=L.get("oordeel", ""), samenvatting=L.get("samenvatting", ""),
                nieuwbouw=nieuw, concept=O.get("concept", "")[:600])


def main():
    W, OP = wijkdata(), omgevingsplan()
    rows = []
    for s in b.VOLGORDE:
        try:
            rows.append(rij(s, W, OP))
        except Exception as e:  # noqa: BLE001
            print("FOUT", s, repr(e))
    tpl = open(os.path.join(HERE, "vergelijking_template.html"), encoding="utf-8").read()
    html = tpl.replace("/*__DATA__*/[]", json.dumps(rows, ensure_ascii=False))
    open(os.path.join(HERE, "vergelijking.html"), "w", encoding="utf-8").write(html)
    for r in rows:
        print(f'{r["titel"][:40]:40} {r["klasse"]:6} {r["eigenaren"]:>3} € {r["fee"]:>4} / {r["inleg"]} kern {r["kern"]} breed {r["breed"]} op {r["op_kans"]} normen {r["normen_ok"]}/4')


if __name__ == "__main__":
    main()
