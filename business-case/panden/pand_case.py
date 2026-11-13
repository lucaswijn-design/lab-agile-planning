"""
Stap 3 van de workflow: financiële doorrekening per pand met de hoeveelheden uit
de plattegrond (layout.py). Inventaris (werken, gym, café, sanitair, verlichting)
komt uit budget.py; pand, bouwkundig, buiten en energie volgen uit het pand.
Draaien: python3 business-case/panden/pand_case.py
"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

import budget  # noqa: E402
from layout import LAYOUTS, build  # noqa: E402

ZZP = budget.ZZP


def rows_for(slug, n_vol=None, n_deel=None, n_club=None, torens=False, extra=None):
    L = LAYOUTS[slug]
    _, q = build(slug)
    n_vol = L["leden"]["n_vol"] if n_vol is None else n_vol
    n_deel = L["leden"]["n_deel"] if n_deel is None else n_deel
    n_club = L["leden"]["n_club"] if n_club is None else n_club
    base, _ = budget.items(budget.B(n_vol=n_vol, n_deel=n_deel, n_club=n_club))
    import ontwerp
    if slug in ontwerp.ONTWERPEN:  # bureaus tellen uit de uitgewerkte indeling
        q = dict(q, desks=sum(1 for e in ontwerp.ONTWERPEN[slug]["elementen"] if e["t"] == "bureau"))
    R = []

    def add(g, post, h, e, p, label, gen=0.0):
        R.append(dict(groep=g, post=post, h=h, e=e, prijs=p, totaal=round(h * p), label=label, gen=gen))

    k = L["koop"]
    # --- Pand
    if "totaal" in k:
        add("Pand", "Koopsom (" + k["label"] + ")", 1, "post", k["totaal"], "bron" if "vraagprijs" in k["label"] else "schatting", 1.0)
        koop = k["totaal"]
        add("Pand", "Overdrachtsbelasting 10,4%", koop, "EUR", 0.104, "bron")
    else:
        add("Pand", f'Hal {k["hal_m2"]} m2', k["hal_m2"], "m2", k["hal_prijs_m2"], "schatting", 1.0)
        add("Pand", f'Kantoor {k["kantoor_m2"]} m2', k["kantoor_m2"], "m2", k["kantoor_prijs_m2"], "schatting", 1.0)
        add("Pand", "Bedrijfswoning", 1, "post", k["woning"], "schatting", 1.0)
        bedrijf = k["hal_m2"] * k["hal_prijs_m2"] + k["kantoor_m2"] * k["kantoor_prijs_m2"]
        add("Pand", "Overdrachtsbelasting 10,4% (bedrijfsdeel)", bedrijf, "EUR", 0.104, "bron")
        add("Pand", "Overdrachtsbelasting 8% (woning, geen hoofdverblijf)", k["woning"], "EUR", 0.08, "bron")
    add("Pand", "Notaris, taxatie, bouwkundige keuring", 1, "post", 10_000, "schatting")

    # --- Bouwkundig, uit de plattegrond
    add("Bouwkundig", "Asbestinventarisatie", 1, "post", 1_500, "schatting")
    if L["bouwjaar_risico"]:
        add("Bouwkundig", "Reserve asbestsanering dak (bouwjaar voor 1994)", 1, "post", 25_000, "schatting")
    if L["isoleren"]:
        add("Bouwkundig", "Dakisolatie club PIR 100 mm, materiaal", q["dak_club_m2"], "m2", 25, "bron", 0.6)
        add("Bouwkundig", "Dakisolatie, timmerman 0,4 u/m2", q["dak_club_m2"] * 0.4, "uur", ZZP["timmerman"], "bron", 0.6)
        add("Bouwkundig", "Gevelisolatie binnenzijde tot 4,5 m", q["gevel_isolatie_m2"], "m2", 40, "bron", 0.6)
        add("Bouwkundig", "Lichtstraten", 6, "st", 2_500, "schatting", 0.5)
    if q["brandwand_m2"]:
        add("Bouwkundig", "Brandscheidende wand club / verhuurdeel (EI60)", q["brandwand_m2"], "m2", 90, "schatting", 0.6)
    add("Bouwkundig", "Glazen pui, aluminium HR+++ triple glas", q["pui_m2"], "m2", 1_000, "bron", 0.6)
    if q["nieuwe_vloer_m2"]:
        add("Bouwkundig", "Nieuwe tussenvloer staal + hout, incl. trap en balustrade", q["nieuwe_vloer_m2"], "m2", 650, "schatting", 0.5)
        add("Bouwkundig", "Monumentenadvies, restauratieve aanpassingen, extra vergunning", 1, "post", 40_000, "schatting")
    if q["geluidswal"]:
        add("Buiten", "Groene geluidswal richting A9 (grondwal + beplanting)", 1, "post", 15_000, "schatting", 0.3)
    add("Bouwkundig", "Betonvloer schuren en coaten", q["dak_club_m2"] - q["gym_m2"], "m2", 22, "schatting", 0.3)
    add("Bouwkundig", "Binnenwanden metal stud + OSB", 150, "m2", 60, "schatting", 0.2)
    add("Bouwkundig", "Glazen scheidingswand gym en vergaderruimte", 25, "m2", 320, "schatting", 0.2)
    add("Bouwkundig", "Akoestische plafondeilanden en wandpanelen", 200, "m2", 40, "bron")
    add("Bouwkundig", "Sauswerk wanden en staal", q["club_m2"] * 1.1, "m2", 9, "schatting")

    # --- Inventaris uit budget.py, geschaald naar de capaciteit die in het pand past
    racks = max(2, round(4 * q["gym_cap"] / 20))
    schaal = {"ATX power rack": racks, "Olympische halterstangen": racks + 1, "Bumper plates": 150 * racks,
              "Verstelbare bankjes": max(3, round(6 * q["gym_cap"] / 20)), "Concept2 RowErg": max(1, round(2 * q["gym_cap"] / 20)),
              "Rubber sportvloer": q["gym_m2"], "Zit-sta onderstel": q["desks"], "Bureaublad": q["desks"],
              "Refurbished Steelcase": q["desks"], "Monitor 27 inch met": q["desks"], "Tweede monitor": q["desks"],
              "Dubbele monitorarm": q["desks"], "Bureaulampen": q["desks"]}
    for r in base:
        if r["groep"] == "Sanitair" and L.get("sanitair_bestaand") and not r["post"].startswith("Keuken"):
            continue  # kleedkamers en douches zijn er al
        if r["groep"] in ("Sanitair", "Verlichting", "Werken", "Gym", "Café & bieb"):
            rr = dict(r)
            for key, h in schaal.items():
                if r["post"].startswith(key):
                    rr.update(h=h, totaal=round(h * r["prijs"]))
                    if key == "ATX power rack":
                        rr["post"] = f"ATX power rack PRX-710 ({q['gym_cap']} mensen tegelijk)"
                    if key == "Bumper plates":
                        rr["post"] = f"Bumper plates ({racks} sets van 150 kg)"
            R.append(rr)
        if r["groep"] == "Installaties":
            rr = dict(r)
            if not L["isoleren"] and "Lucht-lucht" in r["post"]:  # energieneutrale hal: verwarming aanwezig
                rr.update(h=1, totaal=round(rr["prijs"]), post=r["post"] + " (alleen koeling werkzone)")
            R.append(rr)
    if torens and not L.get("sanitair_bestaand"):
        import sanitairtorens
        R.extend(sanitairtorens.rows()[0])
    if slug in ontwerp.ONTWERPEN:
        R.extend(ontwerp.inbouw_rows(slug, q["gym_m2"]))
    for r in extra or []:
        R.append(dict(r))
    # sauna geschrapt in versie 8; Wellness-rijen alleen als budget.B(sauna=True)
    for r in base:
        if r["groep"] == "Wellness":
            R.append(dict(r))

    # --- Energie
    if L["pv_kwp"]:
        add("Energie", "Zonnepanelen op het haldak", L["pv_kwp"], "kWp", 750, "schatting", 0.6)
    add("Energie", "Batterij", 30, "kWh", 450, "bron", 0.5)

    # --- Buiten, uit de plattegrond
    if q["tuin_m2"]:
        add("Buiten", "Onttegelen en groen aanleggen", q["tuin_m2"], "m2", 25, "schatting", 0.3)
        add("Buiten", "Buitenwerkplekken: 4 tafels met stroom + buitenrig", 1, "post", 5_500, "schatting")
    add("Buiten", "Terras: houten vlonder met overkapping", q["terras_m2"], "m2", 110, "schatting", 0.3)
    add("Buiten", "Bomen buiten", q["bomen_buiten"], "st", 300, "schatting", 0.3)
    if not q["tuin_m2"]:
        add("Buiten", "Grote plantenbakken langs het terras", 1, "post", 3_000, "schatting")
    add("Buiten", "Fietsenstalling 40 plekken", 1, "post", 3_000, "schatting", 0.3)
    add("Buiten", "Parkeerplaatsen belijnen", 1, "post", 1_000, "schatting")

    # --- Bijkomend
    bouw = sum(r["totaal"] for r in R if r["groep"] != "Pand")
    add("Bijkomend", "Bouwtekeningen en interieurontwerp (familie)", 1, "post", 8_000, "aanname")
    add("Bijkomend", "Constructeur en brandveiligheidsadvies", 1, "post", 6_500, "schatting")
    add("Bijkomend", "Afwijking omgevingsplan: onderbouwing + leges", 1, "post", 15_500, "schatting")
    add("Bijkomend", "Afbouwmanager (vriend), 6 maanden halftime", 600, "uur", 50, "aanname")
    add("Bijkomend", "Bouwplaats: hoogwerker, afvalcontainers", 1, "post", 6_300, "schatting")
    add("Bijkomend", "Notaris en statuten coöperatie", 1, "post", 15_000, "schatting")
    add("Bijkomend", "Projectleiding initiatiefnemer (3%)", bouw, "EUR", 0.03, "aanname")
    zg = sum(r["totaal"] for r in R if r["groep"] != "Pand")
    add("Bijkomend", "Onvoorzien (10% excl. pand)", zg, "EUR", 0.10, "schatting")
    add("Bijkomend", "Bouwrente en afsluitkosten (1,5%)", sum(r["totaal"] for r in R), "EUR", 0.015, "schatting")
    return R, q


def run(slug, n_vol=None, n_deel=None, n_club=None, fee_vol=450, fee_deel=320, fee_club=119,
        inleg_vol=15_000, inleg_deel=9_000, rente=0.055, looptijd=20, groei=0.02, torens=False, extra=None):
    L = LAYOUTS[slug]
    n_vol = L["leden"]["n_vol"] if n_vol is None else n_vol
    n_deel = L["leden"]["n_deel"] if n_deel is None else n_deel
    n_club = L["leden"]["n_club"] if n_club is None else n_club
    R, q = rows_for(slug, n_vol, n_deel, n_club, torens, extra)
    tot = lambda g: sum(r["totaal"] for r in R if r["groep"] == g)
    C = sum(r["totaal"] for r in R)
    pand = tot("Pand")
    gebouw = tot("Bouwkundig") + tot("Sanitair") + tot("Installaties") + tot("Energie") + tot("Buiten")
    inv = tot("Werken") + tot("Gym") + tot("Wellness") + tot("Café & bieb") + tot("Verlichting")
    O = [("Schoonmaak (5 dagen x 4 uur x € 30)", 31_200), ("Management initiatiefnemer", 18_000),
         ("Klusjes en storingen", 6_000 if L["verhuur"] else 5_000), ("Groenbeheer en planten", 4_000 if q["tuin_m2"] else 2_500)]
    pv = L["pv_kwp"] * 900 if L["pv_kwp"] else 60_000  # Birkt: bestaande panelen (energieneutraal) [aanname]
    vraag = q["club_m2"] * 70 + 4_000
    eigen = min(pv * 0.6, vraag)
    O += [("Energie netto", round((vraag - eigen) * 0.24 - (pv - eigen) * 0.05 + 3_000)),

          ("Onderhoud pand en terrein", round((gebouw + pand * 0.3) * 0.015)),
          ("Vervangingsreserve inventaris (10%)", round(inv * 0.10)),
          ("Verzekeringen", round((gebouw + inv + pand * 0.5) * 0.0025)),
          ("OZB, waterschap, riool", round((pand + gebouw) * 0.7 * 0.0035)),
          ("Internet, software, toegangsapp", 5_000), ("Accountant en administratie", 12_000 if L["verhuur"] else 10_000),
          ("Koffie-apparatuur, verbruik", 4_000), ("Community en events", 5_000)]
    if L["verhuur"]:
        O.append(("Verhuurbeheer en leegstandsrisico (8% van de huur)", 0))
    sub = sum(b for _, b in O)
    O.append(("Onvoorzien exploitatie (5%)", round(sub * 0.05)))
    huur = sum(v.get("huur_jaar") or v["m2"] * v["huur_m2"] for v in L["verhuur"])
    if huur:
        O = [(n, round(huur * 0.08) if n.startswith("Verhuurbeheer") else b) for n, b in O]
    Ot = sum(b for _, b in O)
    inleg = n_vol * inleg_vol + n_deel * inleg_deel
    lening = max(0, C - inleg)
    last = lening * rente / (1 - (1 + rente) ** -looptijd)
    b = 0.95
    o_eig = (n_vol * fee_vol + n_deel * fee_deel) * b / 1.18 * 12
    o_club = n_club * fee_club * b / 1.15 * 12
    over = o_eig + o_club + huur - Ot
    noemer = 12 * b / 1.18 * (n_vol + n_deel * fee_deel / fee_vol)
    fee_nodig = (Ot + last - o_club - huur) / noemer
    s_a = s_v = lening
    for _ in range(5):
        s_a = s_a * (1 + rente) - last
        s_v = max(0.0, s_v * (1 + rente) - over)
    exitw = sum(r["totaal"] for r in R if r["groep"] == "Pand" and r["gen"] == 1.0) * (1 + groei) ** 5 \
        + sum(r["totaal"] * r["gen"] for r in R if r["groep"] != "Pand")
    netto = exitw * 0.975
    aandelen = n_vol + 0.6 * n_deel
    jaren = None
    if over > lening * rente:
        s, jaren = lening, 0
        while s > 0 and jaren < 60:
            s = s * (1 + rente) - over
            jaren += 1
    G = {}
    for r in R:
        G[r["groep"]] = G.get(r["groep"], 0) + r["totaal"]
    return dict(slug=slug, capex=C, groepen=G, verbouw_inrichting=C - G["Pand"], opex=Ot, opex_rows=O, huur=huur,
                inleg=inleg, lening=round(lening), ltv=round(lening / C, 2), dscr=round(over / last, 2),
                resultaat=round(over - last), fee_vol_nodig=round(fee_nodig), fee_deel_nodig=round(fee_nodig * fee_deel / fee_vol),
                jaren_schuldvrij=jaren, exitwaarde=round(exitw), exit_per_vol_versneld=round((netto - s_v) / aandelen),
                exit_dekking=round((netto - s_v) / inleg, 2), q=q, rows=R)


def fee_inleg_terug(slug, **kw):
    lo, hi = 0.0, 2000.0
    for _ in range(40):
        f = (lo + hi) / 2
        r = run(slug, fee_vol=f, fee_deel=f * 320 / 450, **kw)
        if r["exit_dekking"] >= 1:
            hi = f
        else:
            lo = f
    return round(hi)


if __name__ == "__main__":
    out = {}
    for s in LAYOUTS:
        r = run(s)
        r["fee_inleg_terug"] = fee_inleg_terug(s)
        extra = LAYOUTS[s]["leden"]["n_club"] + 30
        r["fee_inleg_terug_90"] = fee_inleg_terug(s, n_club=extra)
        r90 = run(s, n_club=extra)
        r["fee_vol_nodig_90"] = r90["fee_vol_nodig"]
        out[s] = r
        print(s, {k: r[k] for k in ("capex", "verbouw_inrichting", "huur", "opex", "lening", "ltv", "dscr", "resultaat",
                                     "fee_vol_nodig", "fee_inleg_terug", "fee_vol_nodig_90", "fee_inleg_terug_90",
                                     "jaren_schuldvrij", "exitwaarde", "exit_per_vol_versneld")})
        print("   ", r["groepen"])
    with open(os.path.join(HERE, "resultaten_panden.json"), "w") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
