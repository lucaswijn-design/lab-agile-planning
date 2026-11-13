"""
Kleine variant: maximaal 50 tot 60 eigenaar-leden, maandfee maximaal EUR 600.

Drie soorten lidmaatschap, iedereen heeft altijd toegang tot alle faciliteiten:
  Eigenaar vol      werkplek 5 dagen + alles, inleg, 1,0 aandeel
  Eigenaar deeltijd werkplek 3 dagen + alles, lagere inleg, 0,6 aandeel
  Clublid           gym, sauna, koffie, bibliotheek, natuur; geen werkplek, geen aandeel

Geschrapt t.o.v. de grote variant: natuurzwemvijver, tuinbouwkas, elektrische
sauna, tweede hot tub, koeling dompelbad, host en beheerder, grote batterij.
Draaien: python3 business-case/klein.py
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass, asdict

OVB = 0.104  # [bron] overdrachtsbelasting niet-woning 2026

LOC = {
    # erf ~1 ha met woning en stallen; woning wordt afgesplitst en verkocht [schatting]
    "A": dict(naam="Groene Hart / Utrecht West", erf=2_000_000, ha=130_000, woning=950_000, huur=90_000),
    "B": dict(naam="Rand Amersfoort / Leusden", erf=1_300_000, ha=110_000, woning=700_000, huur=60_000),
    "C": dict(naam="Brabant, Den Bosch/Eindhoven", erf=950_000, ha=105_000, woning=550_000, huur=45_000),
}


@dataclass
class K:
    loc: str = "B"
    n_vol: int = 30
    n_deel: int = 30
    n_club: int = 60
    fee_vol: float = 595
    fee_deel: float = 425
    fee_club: float = 139
    inleg_vol: float = 20_000
    inleg_deel: float = 12_000
    bouw_m2: float = 1_200  # [schatting] soberder dan grote variant, klusdagen met leden
    rente: float = 0.055
    looptijd: int = 20
    huren: bool = False  # erf huren in plaats van kopen (lange huur, 15+ jaar)
    extra_ha: float = 0.5
    bezetting: float = 0.95
    schoonmaak_dagen: int = 4
    management: float = 18_000  # initiatiefnemer, ~0,2 fte
    dev_fee: float = 0.03
    woning: float = -1  # netto opbrengst woning; -1 = standaard van de locatie
    gym_containers: bool = False  # gym in 2 gekoppelde containerunits van 3 x 12 m in plaats van in de schuur


def programma(k: K) -> dict:
    eig = k.n_vol + k.n_deel
    tot = eig + k.n_club
    desks = math.ceil(0.6 * k.n_vol + 0.4 * k.n_deel)  # piekbezetting op drukste dag [schatting]
    m2 = dict(
        werkplekken=desks * 5.5,
        vergaderruimte=25,
        gym=0 if k.gym_containers else max(80, 0.6 * tot),  # ~6% tegelijk x 10 m2
        kleedruimte_douches=30 + 0.15 * tot,
        koffie_lounge_bieb=60 + 0.4 * eig + 0.2 * k.n_club,
        toiletten=15,
        techniek=20,
    )
    return dict(desks=desks, leden_totaal=tot, eigenaren=eig, m2_detail={a: round(b) for a, b in m2.items()},
                m2=round(sum(m2.values()) * 1.1), ha=1 + k.extra_ha, pv=round(0.8 * eig), bat=round(0.8 * eig),
                saunas=1 if tot <= 130 else 2)


def capex(k: K):
    p = programma(k)
    L = LOC[k.loc]
    rows = []

    def add(g, post, h, e, prijs, label):
        rows.append(dict(groep=g, post=post, h=h, e=e, prijs=prijs, totaal=round(h * prijs), label=label))

    if not k.huren:
        add("Grond", "Erf met woning en stallen (~1 ha)", 1, "erf", L["erf"], "schatting")
        add("Grond", "Aanvullende grond", k.extra_ha, "ha", L["ha"], "schatting")
        add("Grond", "Overdrachtsbelasting 10,4%", L["erf"] + k.extra_ha * L["ha"], "EUR", OVB, "bron")
        add("Grond", "Notaris, taxatie, splitsing", 1, "post", 20_000, "schatting")
        w = L["woning"] if k.woning < 0 else k.woning
        if w:
            add("Grond", "Woning afsplitsen en verkopen (netto)", 1, "post", -w, "schatting")
    add("Gebouw", "Sloop overtollige stallen en asbest", p["m2"], "m2", 50, "schatting")
    add("Gebouw", "Verbouw stal tot clubgebouw", p["m2"], "m2", k.bouw_m2, "schatting")
    add("Buiten", "Natuur: bomen, maaipaden, poel (extensief)", 1 + k.extra_ha - 0.4, "ha", 15_000, "schatting")
    add("Buiten", "Overdekte veranda met buitenwerkplekken", 1, "post", 18_000, "schatting")
    add("Buiten", "Buitengym (rig, kettlebells)", 1, "post", 8_000, "schatting")
    add("Buiten", "Parkeerplaatsen halfverharding (25 m2 x EUR 40)", math.ceil(0.27 * p["leden_totaal"]), "plek", 1_000, "schatting")
    add("Wellness", "Houtgestookte saunahut 10 pers.", p["saunas"], "st", 30_000, "schatting")
    add("Wellness", "Dompelbad zonder koeling", 1, "st", 3_000, "schatting")
    add("Wellness", "Houtgestookte hot tub", 1, "st", 7_000, "schatting")
    add("Wellness", "Buitendouche en vlonders", 1, "post", 8_000, "schatting")
    if k.gym_containers:
        add("Gym", "Containerunit 3 x 12 m, ombouw (isolatie, glazen pui, elektra, airco)", 2, "st", 30_000, "schatting")
    add("Gym", "Racks met halters en schijven (refurbished)", 2, "st", 4_000, "schatting")
    add("Gym", "Dumbbells, bankjes, kabelstation", 1, "post", 10_000, "schatting")
    add("Gym", "Cardio (2 roeiers, airbike, skierg)", 1, "post", 7_000, "schatting")
    add("Gym", "Sportvloer", max(80, round(0.6 * p["leden_totaal"])), "m2", 60, "schatting")
    add("Werken", "Werkplek: zit-sta bureau, refurbished stoel, 2 schermen", p["desks"], "plek", 1_300, "schatting")
    add("Werken", "Belcellen (refurbished)", 2, "st", 4_500, "schatting")
    add("Werken", "Vergaderruimte, scherm en audio", 1, "st", 3_000, "schatting")
    add("Koffie & interieur", "Tweedehands 3-groeps espressomachine + 2 molens", 1, "set", 15_000, "schatting")
    add("Koffie & interieur", "Keuken en bar (tweedehands)", 1, "post", 15_000, "schatting")
    add("Koffie & interieur", "Tweedehands meubilair, planten, boeken", p["m2"], "m2", 70, "schatting")
    add("Koffie & interieur", "Toegangssysteem met app, lockers", 1, "post", 10_000, "schatting")
    add("Energie & tech", "Zonnepanelen", p["pv"], "kWp", 850, "schatting")
    add("Energie & tech", "Batterij", p["bat"], "kWh", 450, "bron")
    add("Energie & tech", "Warmtepomp lucht-water en afgifte", p["m2"], "m2", 75, "schatting")
    add("Energie & tech", "Glasvezel, wifi, Starlink backup", 1, "post", 15_000, "schatting")
    bi = sum(r["totaal"] for r in rows if r["groep"] != "Grond")
    add("Bijkomend", "Architect, constructeur, installatieadvies (8%)", bi, "EUR", 0.08, "schatting")
    add("Bijkomend", "Planologisch traject", 1, "post", 60_000, "schatting")
    add("Bijkomend", "Leges omgevingsvergunning (~3%)", bi, "EUR", 0.03, "schatting")
    add("Bijkomend", "Juridisch: statuten, fiscaal", 1, "post", 25_000, "schatting")
    add("Bijkomend", "Ontwikkelvergoeding initiatiefnemer", bi, "EUR", k.dev_fee, "aanname")
    zg = sum(r["totaal"] for r in rows if r["groep"] != "Grond")
    add("Bijkomend", "Onvoorzien (12% excl. grond)", zg, "EUR", 0.12, "schatting")
    add("Bijkomend", "Bouwrente en afsluitkosten (3%)", sum(r["totaal"] for r in rows), "EUR", 0.03, "schatting")
    return rows


def opex(k: K, cx):
    p = programma(k)
    L = LOC[k.loc]
    tot = lambda g: sum(r["totaal"] for r in cx if r["groep"] == g)
    gebouw = tot("Gebouw") + tot("Buiten") + tot("Energie & tech")
    equip = tot("Gym") + tot("Werken") + tot("Wellness") + tot("Koffie & interieur")
    rows = []

    def add(post, b, label, t=""):
        rows.append(dict(post=post, bedrag=round(b), label=label, t=t))

    if k.huren:
        add("Huur erf en grond", L["huur"], "schatting")
    add("Schoonmaak", k.schoonmaak_dagen * 4 * 52 * 30, "schatting", f"{k.schoonmaak_dagen} dagen x 4 uur x EUR 30")
    add("Management initiatiefnemer", k.management, "aanname")
    add("Klusjes en storingen (oproepbasis)", 6_000, "schatting")
    add("Groenbeheer (deels met leden)", p["ha"] * 3_000, "schatting")
    vraag = p["m2"] * 60 + 6_000
    pv = p["pv"] * 900
    eigen = min(pv * 0.6, vraag)
    add("Energie netto", (vraag - eigen) * 0.24 - (pv - eigen) * 0.05 + 3_000, "schatting")
    add("Brandhout sauna en hot tub", 5_000, "schatting")
    add("Onderhoud gebouw en terrein (1,5%)", gebouw * 0.015, "schatting")
    add("Vervangingsreserve inventaris (10%)", equip * 0.10, "schatting")
    add("Verzekeringen", (gebouw + equip) * 0.0025, "schatting")
    grond = 0 if k.huren else tot("Grond")
    add("OZB, waterschap, riool", (grond + gebouw) * 0.7 * 0.0035, "schatting")
    add("Internet, software, toegangsapp", 6_000, "schatting")
    add("Accountant en administratie", 12_000, "schatting")
    add("Verbruik (eigen handdoek mee)", 4_000, "schatting")
    add("Community en events", 5_000, "schatting")
    add("Onvoorzien exploitatie (5%)", sum(r["bedrag"] for r in rows) * 0.05, "schatting")
    return rows


def annuity(P, r, y):
    return 0 if P <= 0 else P * r / (1 - (1 + r) ** -y)


def run(k: K):
    cx = capex(k)
    ox = opex(k, cx)
    C = sum(r["totaal"] for r in cx)
    O = sum(r["bedrag"] for r in ox)
    inleg = k.n_vol * k.inleg_vol + k.n_deel * k.inleg_deel
    lening = max(0, C - inleg)
    last = annuity(lening, k.rente, k.looptijd)
    b = k.bezetting
    omzet_eig = (k.n_vol * k.fee_vol + k.n_deel * k.fee_deel) * b / 1.18 * 12
    omzet_club = k.n_club * k.fee_club * b / 1.15 * 12  # gym 9%, sauna 21% -> ~15% [schatting]
    omzet = omzet_eig + omzet_club
    over = omzet - O
    jaren = None
    if lening == 0:
        jaren = 0
    elif over > lening * k.rente:
        s, jaren = lening, 0
        while s > 0 and jaren < 60:
            s = s * (1 + k.rente) - over
            jaren += 1
    # benodigde fee vol-eigenaar (deeltijd schaalt mee in dezelfde verhouding)
    ratio = k.fee_deel / k.fee_vol
    kosten_eig = O + last - omzet_club
    fee_vol_nodig = kosten_eig / (12 * b / 1.18 * (k.n_vol + k.n_deel * ratio))
    aandelen = k.n_vol + 0.6 * k.n_deel
    saldo, afl5 = lening, 0
    for _ in range(5):
        a = last - saldo * k.rente
        saldo -= a
        afl5 += a
    ev_vol_5 = k.inleg_vol + afl5 / aandelen
    return dict(inputs=asdict(k), prog=programma(k), capex=C, opex=O, inleg=inleg, lening=lening,
                ltv=round(lening / C, 2) if C else 0, jaarlast=round(last), omzet_eig=round(omzet_eig),
                omzet_club=round(omzet_club), resultaat=round(over - last),
                dscr=round(over / last, 2) if last else None, jaren_schuldvrij=jaren,
                fee_vol_nodig=round(fee_vol_nodig), fee_deel_nodig=round(fee_vol_nodig * ratio),
                ev_vol_5j=round(ev_vol_5), ev_deel_5j=round(0.6 * ev_vol_5),
                fee_vol_na_aflossing=round((O - omzet_club) / (12 * b / 1.18 * (k.n_vol + k.n_deel * ratio))),
                capex_rows=cx, opex_rows=ox)


def exit_na_5(k: K, huur_kantoor=110, bar_kantoor=0.085, huur_slb=120_000, bar_slb=0.075, multiple=6):
    """Waarde bij verkoop na 5 jaar en wat er per vol aandeel naar leden gaat."""
    r = run(k)
    over = r["omzet_eig"] + r["omzet_club"] - r["opex"]
    s_ann = s_vers = r["lening"]
    for _ in range(5):
        s_ann = s_ann * (1 + k.rente) - r["jaarlast"]
        s_vers = max(0.0, s_vers * (1 + k.rente) - over)
    groei = 1.03 ** 5  # grondwaarde +3% per jaar [schatting]
    ha = 1 + k.extra_ha
    w = {
        "Verkoop als kantoor of bedrijfsruimte": r["prog"]["m2"] * huur_kantoor / bar_kantoor + ha * LOC[k.loc]["ha"] * groei,
        "Lopende club verkopen aan een exploitant": multiple * over,
        "Sale-and-leaseback: belegger koopt, club huurt": huur_slb / bar_slb,
        "Noodverkoop: grond plus schuur als opslag": ha * LOC[k.loc]["ha"] * groei + r["prog"]["m2"] * 400,
    }
    aandelen = k.n_vol + 0.6 * k.n_deel
    rows = []
    for naam, waarde in w.items():
        netto = waarde * 0.975  # makelaar en notaris 2,5%
        rows.append(dict(exit=naam, waarde=round(waarde),
                         per_vol_annuitair=round((netto - s_ann) / aandelen),
                         per_vol_versneld=round((netto - s_vers) / aandelen)))
    return dict(capex=r["capex"], restschuld_annuitair=round(s_ann), restschuld_versneld=round(s_vers),
                ebitda=round(over), rows=rows)


if __name__ == "__main__":
    out = {}
    base = run(K())
    out["basis"] = base
    for r in base["capex_rows"]:
        print(f'{r["groep"]:<18}{r["post"][:50]:<52}{r["h"]:>10.1f} {r["e"]:<5}{r["prijs"]:>11,.2f}{r["totaal"]:>11,} [{r["label"]}]')
    print("CAPEX", base["capex"], "programma", base["prog"])
    for r in base["opex_rows"]:
        print(f'{r["post"]:<45}{r["bedrag"]:>9,} {r["t"]}')
    print({k: v for k, v in base.items() if k not in ("capex_rows", "opex_rows", "inputs", "prog")})

    print("\n=== Varianten ===")
    var = {}
    cases = {
        "B koop, 30 vol + 30 deel + 60 club": K(),
        "B koop, 50 vol, geen clubleden": K(n_vol=50, n_deel=0, n_club=0),
        "B koop, 25 vol + 25 deel + 0 club": K(n_vol=25, n_deel=25, n_club=0),
        "B koop, 30+30 + 90 club": K(n_club=90),
        "C koop, 30+30 + 60 club": K(loc="C"),
        "A koop, 30+30 + 60 club": K(loc="A"),
        "B huur, 30+30 + 60 club": K(huren=True),
        "B koop, bouw 1.600/m2": K(bouw_m2=1_600),
        "B koop, woning niet verkocht": K(woning=0),
        "Advies 495/350": K(fee_vol=495, fee_deel=350),
        "Tegenvaller: 495/350, 30 club, bouw 1.600, woning 400k": K(fee_vol=495, fee_deel=350, n_club=30, bouw_m2=1_600, woning=400_000),
        "Geen inleg, 595/425": K(inleg_vol=0, inleg_deel=0),
        "Advies + gym in 2 containers": K(fee_vol=495, fee_deel=350, gym_containers=True),
    }
    for naam, kk in cases.items():
        r = run(kk)
        var[naam] = {x: r[x] for x in ("capex", "lening", "ltv", "dscr", "resultaat", "jaren_schuldvrij",
                                         "fee_vol_nodig", "fee_deel_nodig", "fee_vol_na_aflossing", "ev_vol_5j")}
        print(naam, var[naam])
    out["varianten"] = var
    ex = exit_na_5(K(fee_vol=495, fee_deel=350))
    out["exit"] = ex
    print("\n=== Exit na 5 jaar (advies 495/350) ===", {k_: v for k_, v in ex.items() if k_ != "rows"})
    for row in ex["rows"]:
        print(row)
    with open("business-case/resultaten_klein.json", "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
