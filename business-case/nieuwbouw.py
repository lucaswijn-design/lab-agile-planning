"""
Variant: kale bedrijfskavel kopen (of tijdelijk huren) en zelf bouwen.

Zelfde programma, inventaris en exploitatie als budget.py (hal 600 m2, perceel
1.800 m2, 60 eigenaren + 60 clubleden). Verschil zit in grond en casco:
  koop   bouwrijpe bedrijfskavel + nieuwe staalhal met sandwichpanelen (casco door
         staalbouwer, afbouw in eigen beheer)
  huur   gemeentegrond tijdelijk huren (10 jaar, 5% van de grondwaarde per jaar)
         + demontabele hal die bij vertrek mee kan of verkocht wordt
Draaien: python3 business-case/nieuwbouw.py
"""
from __future__ import annotations

import json
from dataclasses import dataclass, asdict

import budget

KAVEL = {"brabant": 225, "randstad": 350}  # [schatting] gemeentelijke uitgifteprijs per m2; oost-NL 2026: 110-200 [bron]


@dataclass
class N:
    regio: str = "brabant"
    vorm: str = "koop"  # koop of huur
    hal_m2: int = 600
    kavel_m2: int = 1_800
    casco_m2: float = 650  # [schatting] staalhal incl. fundering, vloer, sandwichpanelen dak en gevel
    n_vol: int = 30
    n_deel: int = 30
    n_club: int = 60
    fee_vol: float = 450
    fee_deel: float = 320
    fee_club: float = 119
    inleg_vol: float = 15_000
    inleg_deel: float = 9_000
    rente: float = 0.055
    looptijd: int = 20
    groei: float = 0.02


def rows(k: N):
    base, _ = budget.items(budget.B(n_vol=k.n_vol, n_deel=k.n_deel, n_club=k.n_club))
    R = []

    def add(g, post, h, e, p, label, gen=0.0):
        R.append(dict(groep=g, post=post, h=h, e=e, prijs=p, totaal=round(h * p), label=label, gen=gen))

    kp = KAVEL[k.regio]
    if k.vorm == "koop":
        add("Grond", f"Bouwrijpe bedrijfskavel {k.kavel_m2} m2", k.kavel_m2, "m2", kp, "schatting", 1.0)
        add("Grond", "Btw op bouwterrein (21%, terug te vragen) in plaats van overdrachtsbelasting", 1, "post", 0, "aanname")
        add("Grond", "Notaris en kadaster", 1, "post", 4_000, "schatting")
        casco_gen = 0.85
    else:
        casco_gen = 0.40  # demontabele hal: verkoop of verhuizen bij einde huur
    # --- Casco nieuw
    add("Casco", "Sondering en funderingsadvies", 1, "post", 3_500, "schatting")
    add("Casco", "Staalhal casco: fundering, vloer, staal, sandwichpanelen Rc 4,7/6,3" if k.vorm == "koop"
        else "Demontabele hal casco: staal, geïsoleerde panelen, vloer", k.hal_m2, "m2",
        k.casco_m2 if k.vorm == "koop" else 480, "schatting", casco_gen)
    add("Casco", "Glazen pui en ramen, aluminium HR+++ triple glas", 40, "m2", 1_000, "bron", 0.6)
    add("Casco", "Lichtstraten", 6, "st", 2_500, "schatting", 0.5)
    add("Casco", "Nutsaansluitingen: elektra, water, riool, glasvezel", 1, "post", 30_000, "schatting", 0.5)
    add("Casco", "Parkeren en paden: klinkers 15 plekken + looproutes", 450, "m2", 45, "schatting", 0.5)
    add("Casco", "Binnenwanden metal stud + OSB", 150, "m2", 60, "schatting", 0.2)
    add("Casco", "Glazen scheidingswand gym en vergaderruimte", 25, "m2", 320, "schatting", 0.2)
    add("Casco", "Akoestische plafondeilanden en wandpanelen", 200, "m2", 40, "bron")
    add("Casco", "Vloer coaten", k.hal_m2 - 150, "m2", 15, "schatting", 0.3)
    # --- Inventaris en installaties uit budget.py
    for r in base:
        if r["groep"] in ("Sanitair", "Installaties", "Verlichting", "Energie", "Werken", "Gym", "Wellness", "Café & bieb"):
            R.append(dict(r))
        if r["groep"] == "Buiten" and not r["post"].startswith("Onttegelen") and not r["post"].startswith("Parkeerplaatsen"):
            R.append(dict(r))
    add("Buiten", "Tuin aanleggen op kale grond (grond, gras, beplanting)", k.kavel_m2 - k.hal_m2 - 450, "m2", 15, "schatting", 0.3)
    # --- Bijkomend
    bouw = sum(r["totaal"] for r in R if r["groep"] != "Grond")
    add("Bijkomend", "Architect, constructeur, BENG-berekening (nieuwbouw)", 1, "post", 25_000, "schatting")
    add("Bijkomend", "Kwaliteitsborger Wkb (gevolgklasse 1)", 1, "post", 8_000, "schatting")
    add("Bijkomend", "Leges omgevingsvergunning (~3% bouwsom)", bouw, "EUR", 0.03, "schatting")
    add("Bijkomend", "Afwijking omgevingsplan voor sport en horeca", 1, "post", 7_500, "schatting")
    add("Bijkomend", "Afbouwmanager (vriend), 8 maanden halftime", 800, "uur", 50, "aanname")
    add("Bijkomend", "Bouwplaats en afvalcontainers", 1, "post", 5_000, "schatting")
    add("Bijkomend", "Notaris en statuten coöperatie", 1, "post", 15_000, "schatting")
    add("Bijkomend", "Projectleiding initiatiefnemer (3%)", bouw, "EUR", 0.03, "aanname")
    zg = sum(r["totaal"] for r in R if r["groep"] != "Grond")
    add("Bijkomend", "Onvoorzien (10% excl. grond)", zg, "EUR", 0.10, "schatting")
    add("Bijkomend", "Bouwrente en afsluitkosten (3%, bouwtijd 10 maanden)", sum(r["totaal"] for r in R), "EUR", 0.03, "schatting")
    return R


def run(k: N):
    R = rows(k)
    C = sum(r["totaal"] for r in R)
    tot = lambda g: sum(r["totaal"] for r in R if r["groep"] == g)
    grond = tot("Grond")
    gebouw = tot("Casco") + tot("Sanitair") + tot("Installaties") + tot("Energie") + tot("Buiten")
    inv = tot("Werken") + tot("Gym") + tot("Wellness") + tot("Café & bieb") + tot("Verlichting")
    O = [("Schoonmaak", 31_200), ("Management initiatiefnemer", 18_000), ("Klusjes en storingen", 4_000),
         ("Groenbeheer en planten", 4_500), ("Energie netto (nieuwbouw, 40 kWp)", 6_000), ("Brandhout", 5_000),
         ("Onderhoud (1%, nieuw)", round(gebouw * 0.01)), ("Vervangingsreserve inventaris (10%)", round(inv * 0.10)),
         ("Verzekeringen", round((gebouw + inv) * 0.0025)), ("OZB, waterschap, riool", round((grond + gebouw) * 0.7 * 0.0035)),
         ("Internet, software, toegang", 5_000), ("Accountant en administratie", 10_000),
         ("Koffie-apparatuur, verbruik", 4_000), ("Community en events", 5_000)]
    if k.vorm == "huur":
        O.append(("Grondhuur (5% van grondwaarde)", round(k.kavel_m2 * KAVEL[k.regio] * 0.05)))
    O.append(("Onvoorzien exploitatie (5%)", round(sum(b for _, b in O) * 0.05)))
    Ot = sum(b for _, b in O)
    inleg = k.n_vol * k.inleg_vol + k.n_deel * k.inleg_deel
    lening = max(0, C - inleg)
    last = lening * k.rente / (1 - (1 + k.rente) ** -k.looptijd)
    b = 0.95
    o_eig = (k.n_vol * k.fee_vol + k.n_deel * k.fee_deel) * b / 1.18 * 12
    o_club = k.n_club * k.fee_club * b / 1.15 * 12
    over = o_eig + o_club - Ot
    noemer = 12 * b / 1.18 * (k.n_vol + k.n_deel * k.fee_deel / k.fee_vol)
    s_v = lening
    for _ in range(5):
        s_v = max(0.0, s_v * (1 + k.rente) - over)
    exitw = sum(r["totaal"] * r["gen"] * ((1 + k.groei) ** 5 if r["groep"] == "Grond" else 1) for r in R)
    jaren = None
    if over > lening * k.rente:
        s, jaren = lening, 0
        while s > 0 and jaren < 60:
            s = s * (1 + k.rente) - over
            jaren += 1
    G = {}
    for r in R:
        G[r["groep"]] = G.get(r["groep"], 0) + r["totaal"]
    return dict(capex=C, groepen=G, opex=Ot, lening=round(lening), ltv=round(lening / C, 2), dscr=round(over / last, 2),
                fee_vol_nodig=round((Ot + last - o_club) / noemer), jaren_schuldvrij=jaren, exitwaarde=round(exitw),
                exit_per_vol=round((exitw * 0.975 - s_v) / (k.n_vol + 0.6 * k.n_deel)),
                exit_dekking=round((exitw * 0.975 - s_v) / inleg, 2), rows=R, opex_rows=O)


def fee_inleg_terug(**kw):
    lo, hi = 0.0, 2000.0
    for _ in range(40):
        f = (lo + hi) / 2
        if run(N(fee_vol=f, fee_deel=f * 320 / 450, **kw))["exit_dekking"] >= 1:
            hi = f
        else:
            lo = f
    return round(hi)


if __name__ == "__main__":
    base = run(N())
    for r in base["rows"]:
        print(f'{r["groep"]:<12}{r["post"][:66]:<68}{r["h"]:>8.0f} {r["e"]:<5}{r["prijs"]:>9,.2f}{r["totaal"]:>10,} [{r["label"]}]')
    print(base["groepen"])
    out = {}
    cases = {
        "Kavel Brabant, nieuwe staalhal": dict(),
        "Kavel Brabant, casco € 850/m2": dict(casco_m2=850),
        "Kavel Brabant, 90 clubleden": dict(n_club=90),
        "Kavel Randstadrand, nieuwe staalhal": dict(regio="randstad"),
        "Tijdelijke grond Brabant (10 jr), demontabele hal": dict(vorm="huur"),
        "Tijdelijke grond Randstadrand (10 jr)": dict(regio="randstad", vorm="huur"),
    }
    vergelijk = budget.run(budget.B())
    print("REFERENTIE bestaande hal Brabant:", {x: vergelijk[x] for x in ("capex", "fee_vol_nodig", "jaren_schuldvrij", "exit_per_vol_versneld")},
          "inleg terug", budget.fee_voor_inleg_terug())
    for n, kw in cases.items():
        r = run(N(**kw))
        d = {x: r[x] for x in ("capex", "opex", "lening", "ltv", "dscr", "fee_vol_nodig", "jaren_schuldvrij", "exitwaarde", "exit_per_vol", "exit_dekking")}
        d["fee_inleg_terug"] = fee_inleg_terug(**kw)
        d["groepen"] = r["groepen"]
        out[n] = d
        print(n, {x: d[x] for x in d if x != "groepen"})
    with open("business-case/resultaten_nieuwbouw.json", "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
