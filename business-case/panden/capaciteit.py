"""
Capaciteit en schaal (14 november 2026).

1. vraag(V, D, C): wat leden op het drukste moment nodig hebben (werkplekken, vergaderuren, belcellen,
   gym, café, toiletten, douches, lockers).
2. aanbod(slug): wat elk uitgewerkt pand biedt (uit ontwerp/<slug>.json en layout.py).
3. max_leden(slug): hoeveel eigenaren (vol/deeltijd) en clubleden er passen, en welke voorziening knelt.
4. programma(V, D, C) + schaal(...): hoeveel m2 een club van 30 tot 70 eigenaren nodig heeft en wat
   dat per maand kost bij een gegeven aankoopprijs per m2 (model gefit op de vijf uitgewerkte panden).

Labels: [bron] met link in de business case, [aanname] uitgangspunt, [berekend] uit het model.
Draaien: python3 capaciteit.py
"""
from __future__ import annotations

import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# ---------------------------------------------------------------- gebruik
AANWEZIG_VOL = 0.70          # [aanname] gemiddelde aanwezigheid per werkdag, vol lid (vakantie, ziek, elders)
AANWEZIG_DEEL = 3 / 5 * 0.85  # [aanname] 3 dagen per week, 85% daarvan echt aanwezig
DRUKSTE_DAG = 1.15           # [aanname] dinsdag tot donderdag drukker dan gemiddeld
GELIJKTIJDIG = 0.85          # [aanname] deel van de dagbezoekers dat er op het piekuur tegelijk is
GYM_BEZOEK = {"eigenaar": 2.0, "club": 2.5}  # [bron] Multiscope: fitnessabonnees 2,5 x per week; eigenaren lager [aanname]
GYM_SESSIE_U = 1.25          # [aanname] inclusief omkleden
GYM_PIEKUUR = 0.15           # [aanname] deel van de dagbezoeken in het drukste uur (7 tot 8 of 17 tot 19)
GYM_DRUKSTE_DAG = 1.25       # [aanname]
GYM_M2_PP = 10.0             # [aanname] m2 per gelijktijdige sporter incl. racks en platforms
VERGADER_U = {"vol": 1.0, "deel": 0.6}  # [aanname] uur per week per eigenaar
KAMER_U_WEEK = 45 * 0.60     # [aanname] 45 uur open, 60% boekbaar zonder wachtrij
WERKERS_PER_BELCEL = 10      # [aanname] gangbare vuistregel 1 belcel per 8 tot 15 werkplekken
PERS_PER_TOILET = 15         # [aanname] vuistregel 1 toilet per 15 aanwezigen (Bbl en Arbobesluit nakijken)
SPORTERS_PER_DOUCHE = 4      # [aanname]
CLUB_CAFE_BEZOEK = 1.0       # [aanname] cafébezoeken per week per clublid, buiten de gym om


def vraag(V, D, C=0):
    """Behoefte op het drukste moment voor V volle eigenaren, D deeltijdeigenaren en C clubleden."""
    werkers = (AANWEZIG_VOL * V + AANWEZIG_DEEL * D) * DRUKSTE_DAG * GELIJKTIJDIG
    per_lid = lambda bezoek: bezoek / 7 * GYM_DRUKSTE_DAG * GYM_PIEKUUR * GYM_SESSIE_U
    gym = (V + D) * per_lid(GYM_BEZOEK["eigenaar"]) + C * per_lid(GYM_BEZOEK["club"])
    cafe_club = C * CLUB_CAFE_BEZOEK / 7 * 1.3 * 0.2  # drukste dag, 20% in het drukste uur, 1 uur
    vergader_u = VERGADER_U["vol"] * V + VERGADER_U["deel"] * D
    aanwezig = werkers + gym + cafe_club + 2  # +2 voor gasten en beheer
    return dict(
        werkplekken=math.ceil(werkers), zit_sta=math.ceil(0.65 * werkers),
        vergaderkamers=round(vergader_u / KAMER_U_WEEK, 1), vergader_u=round(vergader_u),
        belcellen=math.ceil(werkers / WERKERS_PER_BELCEL),
        gym_tegelijk=round(gym, 1), gym_m2=max(70, math.ceil(gym * GYM_M2_PP)),
        cafe_stoelen=math.ceil(0.5 * werkers + cafe_club + 6),
        toiletten=max(3, math.ceil(aanwezig / PERS_PER_TOILET)), douches=max(2, math.ceil(gym / SPORTERS_PER_DOUCHE)),
        lockers=V + D + math.ceil(gym), aanwezig=round(aanwezig),
    )


# ---------------------------------------------------------------- aanbod per uitgewerkt pand
TOILETTEN = {"den-bosch-eendenkooi-1a": (4, 6), "uden-nijverheidsstraat-4c": (7, 4)}  # [aanname] bestaande kleedkamers: 4 toiletten, 6 douches


def aanbod(slug):
    import pand_case
    from build_ontwerpen import TORENS, telling
    O = json.load(open(os.path.join(HERE, "ontwerp", slug + ".json")))
    t = telling(O)
    r = pand_case.run(slug, torens=TORENS[slug])
    gym_m2 = r["q"]["gym_m2"]
    stoelen_cafe = (sum(1 for e in O["elementen"] if e.get("soort") == "stoel" and not e.get("n")) + 8  # +8 zitkuil
                    + sum(int(e["w"] / 0.6) for e in O["elementen"] if e.get("soort") == "raambar" and not e.get("n")))
    toil, dou = TOILETTEN.get(slug, (4, 4))  # wastoren 3 + invalidentoilet; douchetoren 3 + 1
    return dict(werkplekken=t["werkplekken"], zit_sta=t["bureaus"], vergaderkamers=len(t["vergaderkamers"]),
                belcellen=t["belcellen"], gym_m2=gym_m2, cafe_stoelen=stoelen_cafe, toiletten=toil, douches=dou)


def past(slug, V, D, C):
    v, a = vraag(V, D, C), aanbod(slug)
    tekort = {k: (v[k], a[k]) for k in ("werkplekken", "vergaderkamers", "belcellen", "gym_m2", "cafe_stoelen", "toiletten", "douches") if v[k] > a[k] + 1e-9}
    return not tekort, tekort


def max_leden(slug, aandeel_vol=0.5, C=0):
    """Grootste aantal eigenaren (in de gegeven verhouding vol/deeltijd) waarbij werkplekken en gym passen.
    Vergaderkamers, belcellen, toiletten en douches worden als knelpunt gemeld, niet als harde grens."""
    a = aanbod(slug)
    best = 0
    for n in range(10, 200):
        V = round(n * aandeel_vol); D = n - V
        v = vraag(V, D, C)
        if v["werkplekken"] <= a["werkplekken"] and v["gym_m2"] <= a["gym_m2"]:
            best = n
    V = round(best * aandeel_vol)
    return dict(eigenaren=best, vol=V, deel=best - V, knelt=past(slug, V, best - V, C)[1])


# ---------------------------------------------------------------- ruimteprogramma en schaal
def programma(V, D, C=0):
    """Netto m2 per zone voor een club, plus 12% verkeer. Kengetallen uit de vijf uitgewerkte panden [berekend]."""
    v = vraag(V, D, C)
    z = dict(
        werken=v["werkplekken"] * 4.5,                               # eilanden, grote tafel, looppaden
        vergaderen=math.ceil(v["vergaderkamers"]) * 19 + v["belcellen"] * 2.2,
        cafe_keuken=30 + v["cafe_stoelen"] * 1.6,
        gym=v["gym_m2"],
        sanitair=45 if V + D >= 40 else 32,
        bieb=20, entree=12 + 0.15 * (V + D + C), techniek=15,
    )
    netto = sum(z.values())
    z["verkeer"] = 0.12 * netto
    return {k: round(x) for k, x in z.items()}, round(netto * 1.12), v


def schaal(V, D, C=0, prijs_m2=1_400, staat="opknappen", m2=None, rente=0.055, looptijd=20, fee_deel_ratio=320 / 450,
           tussenvloer=0.0, opex_vast=100_000):
    """Doorrekening voor een generiek pand. staat: 'opknappen' (zoals Utrecht, Voorhout, Maarssen) of 'afgewerkt'.
    tussenvloer: deel van het programma (0 tot 0,35) op een nieuwe tussenvloer in een hal van minstens 6,5 m hoog;
    dan is er minder grondvlak nodig. opex_vast: 100.000 standaard, circa 75.000 sober (schoonmaak 3 dagen, minder events)."""
    _, m2_nodig, v = programma(V, D, C)
    m2 = m2 or m2_nodig
    vloer = m2 * tussenvloer                                       # m2 op de tussenvloer
    grond = m2 - vloer                                             # m2 die je koopt
    koop = prijs_m2 * grond
    pand = koop * 1.104 + 10_000                                   # [bron] 10,4% overdrachtsbelasting, notaris [schatting]
    verb = (760 if staat == "opknappen" else 350) * grond + 650 * vloer  # [berekend] per m2 uit de panden; tussenvloer [schatting] staal + hout, trap, balustrade
    inv = 60_000 + 2_300 * v["werkplekken"]                       # [berekend] vaste inventaris + per werkplek
    bijk = 25_000 + 0.30 * (verb + inv) + 0.015 * pand            # [berekend] advies, onvoorzien, bouwrente
    capex = pand + verb + inv + bijk
    opex = opex_vast + 47 * m2                                     # [berekend] vaste kosten + per m2
    inleg = V * 15_000 + D * 9_000
    lening = max(0.0, capex - inleg)
    last = lening * rente / (1 - (1 + rente) ** -looptijd)
    o_club = C * 119 * 0.95 / 1.15 * 12
    noemer = 12 * 0.95 / 1.18 * (V + D * fee_deel_ratio)
    fee_run = (opex + last - o_club) / noemer

    def dekking(fee):
        over = (V * fee + D * fee * fee_deel_ratio) * 0.95 / 1.18 * 12 + o_club - opex
        s = lening
        for _ in range(5):
            s = max(0.0, s * (1 + rente) - over)
        exitw = koop * 1.02 ** 5 + 0.35 * (verb + inv)
        return (exitw * 0.975 - s) / inleg

    lo, hi = 0.0, 3_000.0
    if dekking(hi) < 1:   # verkoopwaarde na 5 jaar lager dan de totale inleg: inleg terug kan niet, hoe hoog de fee ook is
        hi = None
    else:
        for _ in range(40):
            f = (lo + hi) / 2
            lo, hi = (lo, f) if dekking(f) >= 1 else (f, hi)
    return dict(m2=m2, grondvlak=round(grond), capex=round(capex), opex=round(opex), lening=round(lening), ltv=round(lening / capex, 2),
                fee_run=round(fee_run), fee_inleg=round(hi) if hi else None, werkplekken=v["werkplekken"], gym_m2=v["gym_m2"],
                vergaderkamers=math.ceil(v["vergaderkamers"]), belcellen=v["belcellen"])


if __name__ == "__main__":
    from build_ontwerpen import VOLGORDE
    print("Vraag bij 30 vol + 30 deel, zonder en met 60 en 90 clubleden")
    for C in (0, 60, 90):
        print(C, vraag(30, 30, C))
    print("\nAanbod en maximale leden per pand")
    for s in VOLGORDE:
        a = aanbod(s)
        print(s, a)
        for C in (0, 30, 60):
            print("   club", C, "50/50:", max_leden(s, 0.5, C), "| alleen vol:", max_leden(s, 1.0, C)["eigenaren"], "| alleen deel:", max_leden(s, 0.0, C)["eigenaren"])
    print("\nTussenvloer en sober, 60 eigenaren + 30 clubleden, 1.400 per m2")
    for tv in (0, 0.2, 0.35):
        print("tussenvloer", tv, schaal(30, 30, 30, 1_400, tussenvloer=tv))
    for N in (30, 40):
        for C in (0, N // 2):
            print("sober", N, C, schaal(N // 2, N - N // 2, C, 1_200, opex_vast=75_000))
    print("\nSchaal: eigenaren half vol, half deeltijd")
    for N in (30, 40, 50, 60, 70):
        for C in (0, N // 2):
            for p in (1_200, 1_600):
                r = schaal(N // 2, N - N // 2, C, p)
                print(N, "club", C, "prijs", p, r)
