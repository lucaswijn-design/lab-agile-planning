"""
Nieuwbouw: een eigen hal met een open atrium en lagen erin (15 november 2026).

Hal L x B x H (standaard 28 x 20 x 10 m), glasgevel tot 6 m hoog op het zuiden en oosten, galerij op 3,6 m
(L-vorm langs noord en oost), top-niveau op 7,0 m, gym aan de westkant met dakterras erboven.
Kosten bottom-up uit de geometrie, excl. btw. Financiering en exit zoals pand_case / capaciteit.schaal.

Labels: [bron] (link in de business case), [schatting], [aanname], [berekend].
Draaien: python3 atrium.py
"""
from __future__ import annotations

import math

KAVEL = {"brabant": 225, "randstad": 350}  # [schatting] gemeentelijke uitgifteprijs bedrijfskavel per m2 (zie nieuwbouw.py)


def geometrie(L=28.0, B=20.0, H=10.0, glas_h=6.0):
    footprint = L * B
    galerij = (L - 13.4) * 5.5 + 5.4 * (B - 0.2 - 5.5 - 0.2)    # noord-strook 5,5 m diep + oost-strook 5,4 m breed (zie ontwerp.NIEUWBOUW)
    top = 7.0 * 5.5                                                # kroonkamer op 7,0 m
    glas = (L + B) * glas_h                                        # zuid + oost
    dicht = 2 * (L + B) * H - glas
    return dict(footprint=footprint, galerij=round(galerij, 1), top=round(top, 1), bvo=round(footprint + galerij + top),
                glas=glas, dicht=dicht, omtrek=2 * (L + B), L=L, B=B, H=H)


def rows(regio="brabant", kavel_prijs=None, werkplekken=61, dakterras=True, bebouwing=0.40, glas_prijs=850, opslag=1.0, **geo):
    g = geometrie(**geo)
    kp = kavel_prijs or KAVEL[regio]
    kavel = round(g["footprint"] / bebouwing)                           # [aanname] 40% bebouwd, rest terras, tuin, fietsen, parkeren
    R = []

    def add(groep, post, h, e, p, label, gen):
        R.append(dict(groep=groep, post=post, h=round(h, 1), e=e, prijs=p, totaal=round(h * p), label=label, gen=gen))

    # grond
    add("Grond", f"Bouwrijpe kavel {kavel} m2 ({regio})", kavel, "m2", kp, "schatting", 1.0)
    add("Grond", "Notaris en kadaster (btw op bouwterrein in plaats van overdrachtsbelasting)", 1, "post", 4_000, "schatting", 0)
    add("Grond", "Wijziging omgevingsplan of afwijking voor club met gym en café (onderbouwing, onderzoeken)", 1, "post", 15_000, "schatting", 0)
    # casco
    add("Casco", "Sondering en funderingsadvies", 1, "post", 3_500, "schatting", 0)
    add("Casco", "Fundering op palen en geïsoleerde betonvloer", g["footprint"], "m2", 140, "schatting", 0.85)
    add("Casco", "Staalskelet 10 m hoog", g["footprint"], "m2", 150, "schatting", 0.85)
    add("Casco", "Dak geïsoleerd (Rc 6,3) met bitumen, berekend op dakterras boven de gym", g["footprint"], "m2", 120, "schatting", 0.85)
    add("Casco", "Dichte gevel sandwichpanelen Rc 4,7 (noord, west en boven het glas)", g["dicht"], "m2", 120, "schatting", 0.85)
    add("Casco", "Glasgevel aluminium met triple glas tot 6 m hoog, zuid en oost", g["glas"], "m2", glas_prijs, "schatting", 0.85)
    add("Casco", "Lichtstraten boven het atrium en de torens", 30, "m2", 900, "schatting", 0.85)
    add("Casco", "Entreedeuren en nooddeuren", 1, "post", 12_000, "schatting", 0.85)
    # lagen
    add("Lagen", "Galerij staal en hout op 3,6 m", g["galerij"], "m2", 650, "schatting", 0.6)
    add("Lagen", "Top-niveau op 7,0 m (leeskamer)", g["top"], "m2", 650, "schatting", 0.6)
    add("Lagen", "Glazen balustrades", 36, "m1", 450, "schatting", 0.6)
    add("Lagen", "Zittrap hout van café naar galerij, 4 m breed", 1, "post", 15_000, "schatting", 0.5)
    add("Lagen", "Stalen trappen (galerij en top)", 2, "st", 9_000, "schatting", 0.6)
    # installaties en energie
    add("Installaties", "Warmtepomp, vloerverwarming, WTW, elektra en data (nieuwbouw utiliteit)", g["bvo"], "m2", 200, "schatting", 0.7)
    add("Installaties", "Nutsaansluitingen (elektra, water, riool, glasvezel)", 1, "post", 25_000, "schatting", 0.5)
    add("Energie", "Zonnepanelen 50 kWp", 50, "kWp", 900, "schatting", 0.6)
    add("Energie", "Batterij", 1, "post", 15_000, "schatting", 0.4)
    # afbouw
    add("Afbouw", "Betonvloer schuren en coaten", g["footprint"], "m2", 35, "schatting", 0.3)
    add("Afbouw", "Gymwand akoestisch tot het dak + deur met toegangslezer", (g["B"] - 0.6) * g["H"], "m2", 110, "schatting", 0.4)
    add("Afbouw", "Toegangsdeuren gym en club (elektronisch slot, lezer)", 2, "st", 1_800, "schatting", 0.3)
    add("Afbouw", "Akoestische ondervloer en platforms gym", 1, "post", 4_400, "schatting", 0.3)
    add("Afbouw", "Sanitairtorens (was en douche, zie sanitairtorens.py)", 1, "post", 29_400, "berekend", 0.3)
    add("Afbouw", "Sanitair basis: toiletten, douches, boiler, leidingwerk, loodgieter", 1, "post", 26_000, "schatting", 0.3)
    add("Afbouw", "Extra toiletgroep (2 toiletten + toegankelijk toilet)", 1, "st", 14_000, "schatting", 0.3)
    add("Afbouw", "Keuken 6 m + kookeiland, 2 vaatwassers, combi-stoomoven", 1, "post", 16_000, "schatting", 0.3)
    add("Afbouw", "Wanden vergaderkamers (half glas, half dicht)", 150, "m2", 210, "schatting", 0.4)
    add("Afbouw", "Belcellen zelfgebouwd", 5, "st", 2_500, "schatting", 0.3)
    add("Afbouw", "Akoestische baffles onder het dak", 250, "m2", 40, "schatting", 0.3)
    add("Afbouw", "Verlichting", g["bvo"], "m2", 15, "schatting", 0.3)
    add("Buiten", "Terras, tuin, fietsen en parkeren", kavel - g["footprint"], "m2", 55, "schatting", 0.3)
    if dakterras:
        m2 = g["B"] * 7.0 * 0.9
        add("Buiten", "Dakterras boven de gym: houten vlonder op dragers (dak al berekend op belasting)", m2, "m2", 140, "schatting", 0.3)
        add("Buiten", "Dakterras: balustrade staal", 2 * (6.7 + g["B"] - 0.6), "m1", 300, "schatting", 0.3)
        add("Buiten", "Dakterras: buitentrap, pergola en beplanting", 1, "post", 23_000, "schatting", 0.3)
    if opslag != 1.0:  # gevoeligheid: bouwkosten hoger of lager dan geraamd
        for r in R:
            if r["groep"] in ("Casco", "Lagen", "Installaties", "Energie", "Afbouw", "Buiten"):
                r["totaal"] = round(r["totaal"] * opslag)
    # inventaris
    add("Inventaris", "Werkplekken, gym, café, bieb (zoals capaciteit.schaal)", 1, "post", 60_000 + 2_300 * werkplekken, "berekend", 0.3)
    # bijkomend
    bouw = sum(r["totaal"] for r in R if r["groep"] in ("Casco", "Lagen", "Installaties", "Energie", "Afbouw", "Buiten"))
    add("Bijkomend", "Architect, constructeur, bouwfysica en brandveiligheid (10% bouwkosten)", bouw, "EUR", 0.10, "schatting", 0)
    add("Bijkomend", "Leges omgevingsvergunning (circa 2,5% bouwsom)", bouw, "EUR", 0.025, "schatting", 0)
    add("Bijkomend", "Onvoorzien (8%)", bouw, "EUR", 0.08, "schatting", 0)
    add("Bijkomend", "Bouwrente en CAR-verzekering (18 maanden bouw)", bouw + R[0]["totaal"], "EUR", 0.043, "schatting", 0)
    return R, g


def run(V=40, D=40, C=30, regio="brabant", kavel_prijs=None, werkplekken=61, dakterras=True, rente=0.055, looptijd=20,
        inleg_vol=15_000, inleg_deel=9_000, fee_deel_ratio=320 / 450, groei=0.02, bebouwing=0.40, glas_prijs=850, opslag=1.0, **geo):
    R, g = rows(regio, kavel_prijs, werkplekken, dakterras, bebouwing, glas_prijs, opslag, **geo)
    capex = sum(r["totaal"] for r in R)
    opex = 100_000 + 40 * g["bvo"]                     # [berekend] vaste lasten + per m2; nieuwbouw iets lager per m2 (energie, onderhoud)
    inleg = V * inleg_vol + D * inleg_deel
    lening = max(0.0, capex - inleg)
    last = lening * rente / (1 - (1 + rente) ** -looptijd)
    o_club = C * 119 * 0.95 / 1.15 * 12
    noemer = 12 * 0.95 / 1.18 * (V + D * fee_deel_ratio)
    fee_run = (opex + last - o_club) / noemer
    grond = R[0]["totaal"]
    exitw = grond * (1 + groei) ** 5 + sum(r["totaal"] * r["gen"] for r in R[1:])

    def dekking(fee):
        over = (V * fee + D * fee * fee_deel_ratio) * 0.95 / 1.18 * 12 + o_club - opex
        s = lening
        for _ in range(5):
            s = max(0.0, s * (1 + rente) - over)
        return (exitw * 0.975 - s) / inleg

    lo, hi = 0.0, 3_000.0
    if dekking(hi) < 1:
        hi = None
    else:
        for _ in range(40):
            f = (lo + hi) / 2
            lo, hi = (lo, f) if dekking(f) >= 1 else (f, hi)
    G = {}
    for r in R:
        G[r["groep"]] = G.get(r["groep"], 0) + r["totaal"]
    return dict(capex=round(capex), opex=round(opex), lening=round(lening), ltv=round(lening / capex, 2), fee_run=round(fee_run),
                fee_inleg=round(hi) if hi else None, exitwaarde=round(exitw), groepen=G, rows=R, geo=g)


VARIANTEN = [
    ("Basis: Brabant, 80 eigenaren + 30 clubleden", dict()),
    ("Basis: Brabant, 100 eigenaren", dict(V=50, D=50, C=0)),
    ("Randstad (kavel € 350/m²), 80 + 30", dict(regio="randstad")),
    ("Sober: glas 4 m hoog, € 650/m² glas, kavel 60% bebouwd, geen dakterras, 80 + 30", dict(glas_h=4.0, glas_prijs=650, bebouwing=0.60, dakterras=False)),
    ("Sober, 100 eigenaren", dict(V=50, D=50, C=0, glas_h=4.0, glas_prijs=650, bebouwing=0.60, dakterras=False)),
    ("Bouwkosten 15% hoger (aanbesteding valt tegen), 80 + 30", dict(opslag=1.15)),
    ("Kavel € 150/m² (kleine kern Brabant), 80 + 30", dict(kavel_prijs=150)),
]


def varianten():
    out = []
    for naam, kw in VARIANTEN:
        r = run(**kw)
        out.append(dict(naam=naam, capex=r["capex"], fee_run=r["fee_run"], fee_inleg=r["fee_inleg"], ltv=r["ltv"], exitwaarde=r["exitwaarde"]))
    return out


if __name__ == "__main__":
    for v in varianten():
        print(v)
    for regio in ("brabant", "randstad"):
        for (V, D, C) in ((40, 40, 30), (40, 40, 0), (45, 45, 0), (50, 50, 0), (30, 30, 30)):
            r = run(V, D, C, regio)
            print(regio, V + D, C, {k: r[k] for k in ("capex", "opex", "ltv", "fee_run", "fee_inleg", "exitwaarde")})
    r = run()
    print(r["geo"])
    for x in r["rows"]:
        print(f'{x["groep"]:12} {x["post"][:78]:78} {x["h"]:>8} {x["e"]:5} {x["prijs"]:>8} {x["totaal"]:>9} {x["label"]}')
    print(r["groepen"])


# ---------------------------------------------------------------- synthetisch dossier voor maquette en tekening
SLUG = "nieuwbouw-atriumhal"


def dossier(L=28.0, B=20.0):
    """Schrijft dossiers/nieuwbouw-atriumhal.json: een rechthoekige hal op een denkbeeldige kavel op een bedrijventerrein.
    Lokaal assenstelsel: u = oost, v = noord, (0, 0) is de zuidwesthoek van de hal. Buren en straat zijn generiek."""
    import json
    import os
    X0, Y0 = 150_000.0, 400_000.0
    rd = lambda ring: [[round(X0 + u, 3), round(Y0 + v, 3)] for u, v in ring]
    R_ = lambda u0, v0, u1, v1: [[u0, v0], [u1, v0], [u1, v1], [u0, v1], [u0, v0]]
    ctx = [dict(ring=rd(R_(-34, -3, -9, 24)), h=9.0), dict(ring=rd(R_(41, -5, 70, 26)), h=8.0), dict(ring=rd(R_(-20, 27, 55, 52)), h=11.0),
           dict(ring=rd(R_(-30, -46, 5, -27)), h=7.5), dict(ring=rd(R_(14, -48, 52, -27)), h=9.5)]
    d = dict(slug=SLUG, adres="Eigen nieuwbouw op een bedrijfskavel (locatie nog te kiezen)", regio="Brabant of Randstad",
             aanbod="geen: zelf bouwen op een uitgeefbare bedrijfskavel", bouwjaar=2028, footprint=rd(R_(0, 0, L, B)), footprint_m2=L * B,
             centrum=[X0 + L / 2, Y0 + B / 2], hoogte=10.0, hoogte_bron="ontwerp", context=ctx, luchtfoto=None,
             perceel=dict(ring=rd(R_(-4, -14.5, 36, 20.5)), m2=1400), opmerking="Synthetisch dossier: geen bestaand pand.")
    json.dump(d, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "dossiers", SLUG + ".json"), "w"), indent=1)
    return d
