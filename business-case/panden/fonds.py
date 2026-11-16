"""
Uitkoopfonds en geleidelijk inkopen: Monte Carlo per maand over 20 jaar.
Vertrekkers krijgen hun inleg uit het fonds na de opzegtermijn; nieuwe leden storten een deel vooraf en de rest in termijnen
(dat vult het fonds weer). Vergelijking met 'alleen uitbetalen bij een vervanger'. Basis: Galvanistraat (90 eigenaren).
Draaien: python3 fonds.py -> fonds.json
"""
from __future__ import annotations

import json
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
RENTE, LOOPTIJD = 0.055, 20
N, INLEG = 90, (15_000, 9_000)       # helft vol, helft deel
NOEMER = 743.9                        # Galvanistraat: euro jaarlast per euro fee_vol (uit risico.py/pand_case)


def annu(x):
    return x * RENTE / (1 - (1 + RENTE) ** -LOOPTIJD)


def sim(p_jaar, ontwerp, wachtlijst, nooit=0.0, runs=400, jaren=20, seed=1):
    """ontwerp: dict(fonds0, bijdrage_pm, plafond, vooraf, termijnen, opzeg) of None (alleen bij vervanger)."""
    rnd = random.Random(seed)
    M = jaren * 12
    wachten, leeg_mnd, fonds_min, vorder_max, wacht_lang = [], [], [], [], 0
    n_exit = 0
    for _ in range(runs):
        F = ontwerp["fonds0"]
        opzeg = ontwerp["opzeg"]
        queue, termijn, aankomst, fmin, vmax = [], [], [], F, 0.0
        for t in range(M):
            # nieuwe vertrekkers (opzegging nu, uitbetaling na opzegtermijn)
            k = sum(1 for _ in range(N) if rnd.random() < p_jaar / 12)
            for _ in range(k):
                inl = INLEG[rnd.random() < 0.5]
                vertraging = 1 if rnd.random() < wachtlijst else 1 + int(rnd.expovariate(1 / 6))
                if rnd.random() >= nooit:                         # een deel van de plekken blijft leeg (club krimpt)
                    aankomst.append((t + vertraging, inl))       # vervanger komt binnen
                queue.append([t + opzeg, inl, t + opzeg])        # [vanaf, bedrag, vervaldatum]
                n_exit += 1
            # vervangers storten
            nieuw = [a for a in aankomst if a[0] == t]
            aankomst = [a for a in aankomst if a[0] > t]
            for _, inl in nieuw:
                F += inl * ontwerp["vooraf"]
                rest = inl * (1 - ontwerp["vooraf"])
                if rest > 0:
                    termijn.append([rest / ontwerp["termijnen"], ontwerp["termijnen"]])
            if True:
                for tm in termijn:
                    F += tm[0]
                    tm[1] -= 1
                termijn = [tm for tm in termijn if tm[1] > 0]
                if F < ontwerp["plafond"]:
                    F += ontwerp["bijdrage_pm"]
            # uitbetalen, oudste eerst
            rest_q = []
            for q in sorted(queue):
                if q[0] <= t and F >= q[1]:
                    F -= q[1]
                    w = t - q[2]
                    wachten.append(w)
                    wacht_lang += w > 6
                else:
                    rest_q.append(q)
            queue = rest_q
            fmin = min(fmin, F)
            if True:
                vmax = max(vmax, sum(tm[0] * tm[1] for tm in termijn))
        fonds_min.append(fmin)
        vorder_max.append(vmax)
        for q in queue:                                         # aan het eind nog wachtend
            wachten.append(M - q[2])
    wachten.sort()
    pct = lambda a, x: a[min(len(a) - 1, int(len(a) * x))]
    return dict(gem_wacht=round(sum(wachten) / len(wachten), 1), p95_wacht=pct(wachten, 0.95), p_lang=round(100 * sum(1 for w in wachten if w > 6) / len(wachten), 1),
                vorder_max=round(sorted(vorder_max)[int(len(vorder_max) * 0.95)]))


ONTWERPEN = {
    # A: wat in de spelregels stond. Uitbetalen uit de inleg van de vervanger; zonder vervanger uit een uittredingsreserve van 5% (in 5 jaar opgebouwd).
    "A. alleen bij vervanger, 12 mnd opzeg": dict(fonds0=0, bijdrage_pm=900, plafond=54_000, vooraf=1.0, termijnen=1, opzeg=12),
    "B. fonds 54k, 50% vooraf, 36 mnd": dict(fonds0=54_000, bijdrage_pm=0, plafond=54_000, vooraf=0.5, termijnen=36, opzeg=6),
    "C. fonds 54k, 25% vooraf, 60 mnd": dict(fonds0=54_000, bijdrage_pm=0, plafond=54_000, vooraf=0.25, termijnen=60, opzeg=6),
    "D. fonds 108k, 33% vooraf, 36 mnd": dict(fonds0=108_000, bijdrage_pm=0, plafond=108_000, vooraf=1 / 3, termijnen=36, opzeg=6),
    "E. fonds 108k + 900 pm, 33% vooraf, 36 mnd": dict(fonds0=108_000, bijdrage_pm=900, plafond=108_000, vooraf=1 / 3, termijnen=36, opzeg=6),
}


def kosten(o):
    return round(annu(o["fonds0"]) / NOEMER + o["bijdrage_pm"] * 12 / NOEMER, 1)


def ingroei_last(inleg, vooraf, termijnen, rente=0.04):
    rest = inleg * (1 - vooraf)
    # annuïteit over het nog niet gestorte deel (ingroeirente, eerlijk naar wie alles vooraf betaalde)
    r = rente / 12
    return round(rest * r / (1 - (1 + r) ** -termijnen))


def main():
    res = []
    for naam, o in ONTWERPEN.items():
        for p in (0.05, 0.08, 0.12):
            for wl, nooit, wl_naam in ((0.8, 0.0, "wachtlijst"), (0.2, 0.25, "geen wachtlijst")):
                r = sim(p, o, wl, nooit)
                res.append(dict(ontwerp=naam, vertrek=p, wachtlijst=wl_naam, fee_pm=kosten(o), **r))
                print(f"{naam:42} vertrek {int(p*100):>2}% {wl_naam:16} gem {r['gem_wacht']:>5} mnd p95 {r['p95_wacht']:>3} >6 mnd {r['p_lang']:>5}%  vorderingen p95 {r['vorder_max']:>7}  fee +{kosten(o)}")
    ing = {f"{v} vol, {int(vf*100)}% vooraf, {t} mnd": dict(vooraf=round(15_000 * vf), pm=ingroei_last(15_000, vf, t), pm_deel=ingroei_last(9_000, vf, t))
           for vf, t in ((0.25, 60), (1 / 3, 36), (0.5, 36)) for v in ("15.000",)}
    print(ing)
    json.dump(dict(simulatie=res, ingroei=ing), open(os.path.join(HERE, "fonds.json"), "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
