"""
Loodsvariant: bestaande bedrijfshal met buitenterrein (3,5 x pandoppervlak),
binnen biophilic ingericht, buiten groen met modulaire sauna en buitenwerkplekken.

Kern: een bedrijfshal is courant vastgoed. Bij een exit verkoop je het pand weer
als bedrijfshal, dus de waarde blijft grotendeels staan. Dat is het verschil met
een verbouwde stal in het buitengebied.

Toets "rond":
  1. benodigde fee vol <= gekozen fee <= EUR 600
  2. bank: DSCR >= 1,2 en lening <= 65% van de kostprijs
  3. exit na 5 jaar: netto verkoopwaarde - restschuld >= totale inleg
Draaien: python3 business-case/loods.py
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass, asdict

OVB = 0.104  # [bron] niet-woning 2026

LOC = {
    # hal_m2: koopprijs bestaande hal incl. normaal perceel (~2x pand) per m2 vvo
    # grond_m2: extra buitenterrein bedrijventerrein per m2; huur: hal per m2 per jaar
    "B": dict(naam="Bedrijventerrein rand Amersfoort/Utrecht", hal_m2=1_450, grond_m2=250, huur_m2=110),
    "C": dict(naam="Bedrijventerrein Den Bosch/Tilburg/Arnhem", hal_m2=1_150, grond_m2=175, huur_m2=90),
    "S": dict(naam="Binnenstedelijk Utrecht of Amsterdam-rand", hal_m2=2_000, grond_m2=450, huur_m2=150),
}


@dataclass
class L:
    loc: str = "B"
    n_vol: int = 30
    n_deel: int = 30
    n_club: int = 60
    fee_vol: float = 495
    fee_deel: float = 350
    fee_club: float = 139
    inleg_vol: float = 20_000
    inleg_deel: float = 12_000
    huren: bool = False
    hal_factor: float = 1.0  # prijs hal t.o.v. locatiebasis
    inbouw_m2: float = 550  # [schatting] wanden, sanitair, vloer, akoestiek in bestaande hal
    rente: float = 0.055
    looptijd: int = 20
    schoonmaak_dagen: int = 4
    waardegroei: float = 0.02  # hal per jaar [schatting]
    bezetting: float = 0.95


def programma(k: L) -> dict:
    eig = k.n_vol + k.n_deel
    tot = eig + k.n_club
    desks = math.ceil(0.6 * k.n_vol + 0.4 * k.n_deel)
    netto = desks * 5.5 + 25 + max(80, 0.6 * tot) + 30 + 0.15 * tot + 60 + 0.4 * eig + 0.2 * k.n_club + 15 + 20
    club_m2 = round(netto * 1.1)
    hal = math.ceil(club_m2 / 0.9 / 10) * 10  # 10% marge voor constructie en techniek
    return dict(desks=desks, tot=tot, eig=eig, club_m2=club_m2, hal_m2=hal,
                buiten_m2=round(hal * 2.5), extra_grond_m2=round(hal * 1.5),
                parkeer=math.ceil(0.27 * tot), pv=round(0.12 * hal), bat=round(0.8 * eig))


def capex(k: L):
    p = programma(k)
    Lc = LOC[k.loc]
    rows = []

    def add(g, post, h, e, prijs, label, generiek=0.0):
        rows.append(dict(groep=g, post=post, h=h, e=e, prijs=prijs, totaal=round(h * prijs), label=label,
                         generiek=generiek))

    if not k.huren:
        hal = p["hal_m2"] * Lc["hal_m2"] * k.hal_factor
        grond = p["extra_grond_m2"] * Lc["grond_m2"] * k.hal_factor
        add("Pand", "Bestaande bedrijfshal incl. perceel (~2x pand)", p["hal_m2"], "m2", Lc["hal_m2"] * k.hal_factor, "schatting", 1.0)
        add("Pand", "Extra buitenterrein (1,5x pand)", p["extra_grond_m2"], "m2", Lc["grond_m2"] * k.hal_factor, "schatting", 1.0)
        add("Pand", "Overdrachtsbelasting 10,4%", hal + grond, "EUR", OVB, "bron")
        add("Pand", "Notaris, taxatie, bouwkundige keuring", 1, "post", 12_000, "schatting")
    add("Verbouw", "Asbestinventarisatie en sanering dak (risicopost)", p["hal_m2"], "m2", 25, "schatting")
    add("Verbouw", "Na-isolatie dak en gevel", p["hal_m2"], "m2", 120, "schatting", 0.6)
    add("Verbouw", "Lichtstraten en glazen pui naar de tuin", 1, "post", 45_000, "schatting", 0.6)
    add("Verbouw", "Installaties: warmtepomp, ventilatie met WTW, elektra", p["hal_m2"], "m2", 200, "schatting", 0.6)
    add("Verbouw", "Inbouw: wanden, sanitair, douches, vloer, akoestiek", p["club_m2"], "m2", k.inbouw_m2, "schatting", 0.1)
    add("Verbouw", "Biophilic: plantenwanden, bomen in bakken, hout", p["club_m2"], "m2", 80, "schatting")
    add("Buiten", "Onttegelen en groen aanleggen", p["buiten_m2"] - p["parkeer"] * 25, "m2", 45, "schatting", 0.3)
    add("Buiten", "Parkeren op bestaande verharding (belijning, groen)", p["parkeer"], "plek", 300, "schatting")
    add("Buiten", "Overdekte veranda met buitenwerkplekken", 1, "post", 18_000, "schatting", 0.3)
    add("Buiten", "Buitengym (rig, kettlebells)", 1, "post", 8_000, "schatting", 0.3)
    add("Wellness", "Houtgestookte saunahut 10 pers. (verplaatsbaar)", 1, "st", 30_000, "schatting", 0.4)
    add("Wellness", "Dompelbad, houtgestookte hot tub, buitendouche", 1, "post", 18_000, "schatting", 0.3)
    if p["tot"] > 130:
        add("Wellness", "Tweede sauna: houtgestookte barrelsauna 8 pers.", 1, "st", 13_000, "bron", 0.4)
    add("Gym", "Apparatuur (racks, dumbbells, kabel, cardio)", 1, "post", 25_000, "schatting", 0.3)
    add("Gym", "Sportvloer", max(80, round(0.6 * p["tot"])), "m2", 60, "schatting")
    add("Werken", "Werkplek: zit-sta bureau, refurbished stoel, 2 schermen", p["desks"], "plek", 1_300, "schatting", 0.3)
    add("Werken", "Belcellen en vergaderruimte", 1, "post", 12_000, "schatting", 0.3)
    add("Koffie & interieur", "Tweedehands 3-groeps espressomachine + 2 molens", 1, "set", 15_000, "schatting", 0.4)
    add("Koffie & interieur", "Keuken en bar (tweedehands)", 1, "post", 15_000, "schatting")
    add("Koffie & interieur", "Tweedehands meubilair, boeken, verlichting", p["club_m2"], "m2", 70, "schatting", 0.1)
    add("Koffie & interieur", "Toegangssysteem met app, lockers", 1, "post", 10_000, "schatting", 0.2)
    add("Energie & tech", "Zonnepanelen op het haldak", p["pv"], "kWp", 800, "schatting", 0.6)
    add("Energie & tech", "Batterij", p["bat"], "kWh", 450, "bron", 0.5)
    add("Energie & tech", "Glasvezel, wifi, Starlink backup", 1, "post", 10_000, "schatting")
    bi = sum(r["totaal"] for r in rows if r["groep"] != "Pand")
    add("Bijkomend", "Architect en installatieadvies (8%)", bi, "EUR", 0.08, "schatting")
    add("Bijkomend", "Afwijking omgevingsplan (sport/horeca op bedrijventerrein)", 1, "post", 25_000, "schatting")
    add("Bijkomend", "Leges omgevingsvergunning (~3%)", bi, "EUR", 0.03, "schatting")
    add("Bijkomend", "Juridisch: statuten, fiscaal", 1, "post", 25_000, "schatting")
    add("Bijkomend", "Ontwikkelvergoeding initiatiefnemer (3%)", bi, "EUR", 0.03, "aanname")
    zg = sum(r["totaal"] for r in rows if r["groep"] != "Pand")
    add("Bijkomend", "Onvoorzien (12% excl. pand)", zg, "EUR", 0.12, "schatting")
    add("Bijkomend", "Bouwrente en afsluitkosten (3%)", sum(r["totaal"] for r in rows), "EUR", 0.03, "schatting")
    return rows


def opex(k: L, cx):
    p = programma(k)
    Lc = LOC[k.loc]
    tot = lambda g: sum(r["totaal"] for r in cx if r["groep"] == g)
    pand = tot("Pand")
    verbouw = tot("Verbouw") + tot("Buiten") + tot("Energie & tech")
    equip = tot("Gym") + tot("Werken") + tot("Wellness") + tot("Koffie & interieur")
    rows = []

    def add(post, b, label, t=""):
        rows.append(dict(post=post, bedrag=round(b), label=label, t=t))

    if k.huren:
        add("Huur hal en terrein", p["hal_m2"] * Lc["huur_m2"] + p["extra_grond_m2"] * 10, "schatting",
            f'{p["hal_m2"]} m2 x EUR {Lc["huur_m2"]} + terrein')
    add("Schoonmaak", k.schoonmaak_dagen * 4 * 52 * 30, "schatting", f"{k.schoonmaak_dagen} dagen x 4 uur x EUR 30")
    add("Management initiatiefnemer", 18_000, "aanname")
    add("Klusjes en storingen (op afroep)", 6_000, "schatting")
    add("Groenbeheer (deels met leden)", p["buiten_m2"] * 2, "schatting")
    vraag = p["hal_m2"] * 80 + 6_000
    pv = p["pv"] * 900
    eigen = min(pv * 0.6, vraag)
    add("Energie netto", (vraag - eigen) * 0.24 - (pv - eigen) * 0.05 + 3_000, "schatting")
    add("Brandhout sauna en hot tub", 5_000, "schatting")
    add("Onderhoud pand en terrein (1,5%)", (verbouw + pand * 0.3) * 0.015, "schatting")
    add("Vervangingsreserve inventaris (10%)", equip * 0.10, "schatting")
    add("Verzekeringen", (verbouw + equip + pand * 0.5) * 0.0025, "schatting")
    add("OZB, waterschap, riool", 0 if k.huren else (pand + verbouw) * 0.7 * 0.0035, "schatting")
    add("Parkmanagement bedrijventerrein", 1_500, "schatting")
    add("Internet, software, toegangsapp", 6_000, "schatting")
    add("Accountant en administratie", 12_000, "schatting")
    add("Verbruik (eigen handdoek mee)", 4_000, "schatting")
    add("Community en events", 5_000, "schatting")
    add("Onvoorzien exploitatie (5%)", sum(r["bedrag"] for r in rows) * 0.05, "schatting")
    return rows


def run(k: L):
    cx = capex(k)
    ox = opex(k, cx)
    C = sum(r["totaal"] for r in cx)
    O = sum(r["bedrag"] for r in ox)
    inleg = k.n_vol * k.inleg_vol + k.n_deel * k.inleg_deel
    lening = max(0, C - inleg)
    last = 0 if lening <= 0 else lening * k.rente / (1 - (1 + k.rente) ** -k.looptijd)
    b = k.bezetting
    o_eig = (k.n_vol * k.fee_vol + k.n_deel * k.fee_deel) * b / 1.18 * 12
    o_club = k.n_club * k.fee_club * b / 1.15 * 12
    over = o_eig + o_club - O
    ratio = k.fee_deel / k.fee_vol
    noemer = 12 * b / 1.18 * (k.n_vol + k.n_deel * ratio)
    fee_nodig = (O + last - o_club) / noemer
    # restschuld na 5 jaar: gewoon en als het hele overschot aflost
    s_ann = s_vers = lening
    for _ in range(5):
        s_ann = s_ann * (1 + k.rente) - last
        s_vers = max(0.0, s_vers * (1 + k.rente) - over)
    # exitwaarde na 5 jaar: pand groeit mee, generieke verbeteringen houden deels hun waarde
    pand_rows = [r for r in cx if r["groep"] == "Pand" and "Overdracht" not in r["post"] and "Notaris" not in r["post"]]
    pand_w = sum(r["totaal"] for r in pand_rows) * (1 + k.waardegroei) ** 5
    gen_w = sum(r["totaal"] * r["generiek"] for r in cx if r["groep"] != "Pand")
    exitwaarde = pand_w + gen_w
    netto_exit = exitwaarde * 0.975
    naar_leden = netto_exit - s_ann
    naar_leden_vers = netto_exit - s_vers
    return dict(inputs=asdict(k), prog=programma(k), capex=C, opex=O, inleg=inleg, lening=round(lening),
                ltv=round(lening / C, 2), jaarlast=round(last), omzet_eig=round(o_eig), omzet_club=round(o_club),
                resultaat=round(over - last), dscr=round(over / last, 2) if last else None,
                fee_vol_nodig=round(fee_nodig), fee_deel_nodig=round(fee_nodig * ratio),
                fee_vol_na_aflossing=round(max(0, (O - o_club) / noemer)),
                exitwaarde=round(exitwaarde), restschuld_5=round(s_ann), restschuld_5_versneld=round(s_vers),
                exit_dekking=round(naar_leden / inleg, 2) if inleg else None,
                exit_dekking_versneld=round(naar_leden_vers / inleg, 2) if inleg else None,
                exit_per_vol=round(naar_leden / (k.n_vol + 0.6 * k.n_deel)) if k.n_vol + k.n_deel else 0,
                exit_per_vol_versneld=round(naar_leden_vers / (k.n_vol + 0.6 * k.n_deel)) if k.n_vol + k.n_deel else 0,
                capex_rows=cx, opex_rows=ox)


def toets(r, fee_vol):
    return dict(exploitatie=r["fee_vol_nodig"] <= fee_vol <= 600,
                bank=(r["dscr"] is None or r["dscr"] >= 1.2) and r["ltv"] <= 0.65,
                exit=(r["exit_dekking"] or 0) >= 1.0)


if __name__ == "__main__":
    out = {}
    base = run(L())
    out["basis"] = base
    for r in base["capex_rows"]:
        print(f'{r["groep"]:<18}{r["post"][:52]:<54}{r["h"]:>9.0f} {r["e"]:<5}{r["prijs"]:>10,.2f}{r["totaal"]:>11,} [{r["label"]}]')
    print("CAPEX", base["capex"], base["prog"])
    for r in base["opex_rows"]:
        print(f'{r["post"]:<48}{r["bedrag"]:>9,}')
    print({k: v for k, v in base.items() if k not in ("capex_rows", "opex_rows", "inputs", "prog")})
    print()
    cases = {
        "Loods B koop (30+30+60, 495/350)": L(),
        "Loods C koop": L(loc="C"),
        "Stad S koop": L(loc="S"),
        "Stad S koop, 90 clubleden": L(loc="S", n_club=90),
        "Loods B huur": L(huren=True),
        "Loods C huur": L(loc="C", huren=True),
        "Loods B koop, 25+25+50": L(n_vol=25, n_deel=25, n_club=50),
        "Loods B koop, geen clubleden, 50 vol, 595": L(n_vol=50, n_deel=0, n_club=0, fee_vol=595, fee_deel=425),
        "Loods B koop, hal 20% duurder": L(hal_factor=1.2),
        "Loods B koop, inbouw 800/m2": L(inbouw_m2=800),
        "Loods B koop, waarde hal daalt 1%/jr": L(waardegroei=-0.01),
        "Loods B koop, tegenvaller (30 club, inbouw 800, hal +20%)": L(n_club=30, inbouw_m2=800, hal_factor=1.2),
        "Loods B koop, 595/425": L(fee_vol=595, fee_deel=425),
    }
    var = {}
    for n, kk in cases.items():
        r = run(kk)
        keys = ("capex", "lening", "ltv", "dscr", "resultaat", "fee_vol_nodig", "fee_deel_nodig",
                "exitwaarde", "restschuld_5", "exit_dekking", "exit_dekking_versneld", "exit_per_vol", "exit_per_vol_versneld")
        var[n] = {x: r[x] for x in keys}
        var[n]["toets"] = toets(r, kk.fee_vol)
        print(n, var[n])
    out["varianten"] = var
    with open("business-case/resultaten_loods.json", "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
