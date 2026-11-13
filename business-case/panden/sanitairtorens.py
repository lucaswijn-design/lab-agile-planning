"""Sanitairtorens: ronde sanitairkernen met een V-wand (stijlinput november 2026).

Idee uit de referentie (ronde badkamer met driehoekige wand): het meest publieke deel
(wastrog) ligt open aan de buitenkant van de V, het meest verborgen deel (toiletten,
douches) ligt erachter. Bovenop de ronde wand een plantenrand die naar beneden groeit.

Twee torens vervangen de rechthoekige sanitairblokken:
  Wastoren   diameter 5,5 m: open wastrog met 3 kranen + 3 toiletcabines achter de V
  Douchetoren diameter 4,5 m: bank en haken + 3 douches achter de V
  Invalidentoilet met douche blijft een gewone rechthoekige ruimte (maten Bouwbesluit).
Aantal toiletten (4) en douches (4) blijft gelijk aan budget.py, dus die rijen blijven staan.
"""
import math

ZZP_TIMMERMAN = 49   # [bron] budget.ZZP
STUKADOOR = 48       # [schatting] ZZP stukadoor, vergelijkbaar met timmerman

TORENS = [  # naam, diameter, opening, hoogte wand, hoogte V-wand
    dict(naam="Wastoren", d=5.5, opening=1.2, h=3.0, hv=2.4),
    dict(naam="Douchetoren", d=4.5, opening=1.0, h=3.0, hv=2.4),
]


def maten():
    rond = sum((math.pi * t["d"] - t["opening"]) * t["h"] for t in TORENS)       # m2 ronde wand
    rand = sum(math.pi * t["d"] - t["opening"] for t in TORENS)                   # m1 plantenrand
    v = sum(2 * (t["d"] / 2) * t["hv"] for t in TORENS)                           # m2 V-wand (2 armen = straal)
    scheid = 4 * 1.6 * 2.4                                                        # 2 tussen toiletten, 2 tussen douches
    d = TORENS[1]
    nat = (math.pi * d["d"] - d["opening"]) * d["h"] + 2 * 2 * (d["d"] / 2) * d["hv"] + 2 * 2 * 1.6 * 2.4
    afw = 2 * rond + 2 * v + 2 * scheid                                           # beide zijden zichtbaar
    vloer_nat = math.pi * (d["d"] / 2) ** 2 + 0.5 * math.pi * (TORENS[0]["d"] / 2) ** 2 * 0.5
    return dict(rond=rond, rand=rand, v=v, scheid=scheid, afw=afw, nat=nat, droog=afw - nat, vloer_nat=vloer_nat)


def rows(rond_prijs=114, droog_prijs=55, nat_prijs=85):
    """Meerkosten en besparingen ten opzichte van rechthoekige sanitairblokken (excl. btw)."""
    m = maten()
    R = []

    def add(post, h, e, p, label):
        R.append(dict(groep="Sanitair", post=post, h=round(h, 1), e=e, prijs=p, totaal=round(h * p), label=label, gen=0.3))

    add("Torens: ronde wand metal stud flexrail + 2 zijden gebogen cementplaat (mat. 45 + 1,4 u timmerman)",
        m["rond"], "m2", rond_prijs, "schatting")
    add("Torens: V-wanden en cabinescheidingen recht, cementplaat 2 zijden (mat. 35 + 0,8 u)",
        m["v"] + m["scheid"], "m2", 75, "schatting")
    add("Torens: microcement nat (douchetoren binnen, V, scheidingen; mat. 45 + 0,8 u stukadoor)",
        m["nat"], "m2", nat_prijs, "schatting")
    add("Torens: kalkstuc betonlook droog met plankstructuur (mat. 25 + 0,6 u stukadoor)",
        m["droog"], "m2", droog_prijs, "schatting")
    add("Torens: microcement vloer douchetoren en natte deel wastoren", m["vloer_nat"], "m2", nat_prijs, "schatting")
    add("Torens: stalen plantenbak op de rand + substraat", m["rand"], "m1", 60, "schatting")
    add("Torens: hangplanten (3 per m1: klimop, scindapsus, varens)", m["rand"] * 3, "st", 12, "schatting")
    add("Torens: druppelirrigatie op de rand", 1, "post", 400, "schatting")
    add("Torens: wastrog 3,5 m (gestort beton of tweedehands stenen trog) + 3 kranen", 1, "post", 1_950, "schatting")
    add("Torens: lichtlijn in de rand en pendels", 2, "st", 300, "schatting")
    add("Vervalt: tegelwerk douches en kleedruimte", -45, "m2", 75, "berekend")
    add("Vervalt: rechte sanitairwanden metal stud + OSB (deel van 150 m2)", -60, "m2", 60, "aanname")
    add("Vervalt: losse fonteintjes (wastrog vervangt ze)", -3, "st", 150, "schatting")
    return R, m


if __name__ == "__main__":
    for naam, kw in [("laag", dict(rond_prijs=90, droog_prijs=15)), ("basis", {}), ("hoog", dict(rond_prijs=150, droog_prijs=75))]:
        R, m = rows(**kw)
        print(naam, sum(r["totaal"] for r in R))
    R, m = rows()
    print({k: round(v, 1) for k, v in m.items()})
    for r in R:
        print(f'{r["post"][:90]:90} {r["h"]:>7} {r["e"]:5} {r["prijs"]:>6} {r["totaal"]:>8} {r["label"]}')
