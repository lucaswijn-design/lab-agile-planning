"""
Rekenmodel community club ("de club").

Alle bedragen in euro. Investeringen exclusief btw (de coöperatie is btw
ondernemer en trekt voorbelasting af). Maandfee van leden is inclusief btw.

Labels per aanname:
  [bron]      gevonden actuele prijs, zie SOURCES onderaan
  [schatting] eigen inschatting, redenering in commentaar
  [berekend]  uitkomst van een rekenstap

Draaien:  python3 business-case/model.py
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass, asdict, field

# ---------------------------------------------------------------------------
# Locaties
# ---------------------------------------------------------------------------
LOCATIONS = {
    "A": dict(
        naam="Groene Hart / Utrecht West (Woerden, Harmelen, Vleuten)",
        # Erf met woning + oude stallen (~1.500 m2) op ~1 ha. Referenties:
        # 2e Polderweg 7 Utrecht 0,47 ha EUR 2,45 mln; Nieuwersluis 4 ha EUR 3,325 mln.
        erf_prijs=2_200_000,  # [schatting]
        grond_per_ha=130_000,  # [schatting] boven landelijk gem. 108.500 [bron] door Randstaddruk
    ),
    "B": dict(
        naam="Rand Amersfoort / Leusden (Gelderse Vallei)",
        erf_prijs=1_500_000,  # [schatting]
        grond_per_ha=110_000,  # [schatting] rond landelijk gemiddelde
    ),
    "C": dict(
        naam="Brabant tussengebied Den Bosch-Eindhoven (Boxtel, Liempde, Vught)",
        # Referentie: voormalig agrarisch erf met loods 2,2 ha Ysselsteyn EUR 950k k.k.
        erf_prijs=1_100_000,  # [schatting]
        grond_per_ha=105_000,  # [schatting]
    ),
}

OVERDRACHTSBELASTING = 0.104  # [bron] niet-woning 2026 en 2027
NOTARIS_TAXATIE = 15_000  # [schatting]


@dataclass
class Inputs:
    leden: int = 150
    fee_incl_btw: float = 450.0
    locatie: str = "B"
    bouw_per_m2: float = 1_300.0  # [schatting] transformatie bestaande schuur naar utiliteit, incl. installaties
    looptijd_lening: int = 20  # jaren annuïtair
    rente: float = 0.055  # [bron] zakelijke vastgoedrente 2026 4,2 tot 7%
    inleg_per_lid: float = 0.0  # eenmalige inleg (ledenkapitaal) per lid
    bezetting: float = 0.95  # gemiddeld gevuld lidmaatschap (wisselingen, wachtlijst)
    btw_mix: float = 0.18  # [schatting] gym 9%, cowork en sauna 21% -> mix
    dev_fee_pct: float = 0.03  # ontwikkelvergoeding initiatiefnemer over bouw+inrichting
    management_fee: float = 30_000  # per jaar, initiatiefnemer als directeur/eindverantwoordelijke
    grond_prijs_factor: float = 1.0  # voor scenario's laag/hoog
    woning_afsplitsen: float = 0.0  # netto opbrengst bij verkoop van de boerderijwoning
    host_fte: float = 1.0  # bemensing; 0,5 bij self-service met app-toegang
    extra_omzet_pct: float = 0.0  # gastenpassen, verhuur vergaderruimte, events, als % van ledenomzet


def program(n: int) -> dict:
    """Leidt het ruimteprogramma af uit het ledenaantal."""
    desks = math.ceil(0.30 * n)  # piek: ~30% van de leden werkt tegelijk [schatting]
    m2 = {
        "werkplekken": desks * 5.5,  # 5,5 m2 per plek incl. looppad [schatting]
        "vergader_en_belruimtes": 40 + 6 * math.ceil(n / 50),
        "gym": max(120, 1.0 * n),  # piek 8% van leden x 12 m2 p.p. ~ 1 m2 per lid
        "kleedkamers_douches": 40 + 0.2 * n,
        "koffiebar_keuken_lounge_bieb": 80 + 0.4 * n,
        "toiletten": 25,
        "techniek_opslag": 40,
    }
    netto = sum(m2.values())
    bruto = netto * 1.10  # verkeersruimte en wanden
    return dict(
        desks=desks,
        belcellen=math.ceil(n / 50),
        m2_detail={k: round(v) for k, v in m2.items()},
        m2_binnen=round(bruto),
        m2_kas=round(150 + 0.5 * n),  # tweedehands tuinbouwkas als seizoenspaviljoen
        m2_zwemvijver=round(200 + 0.5 * n),  # zwemzone + plantenzone (ca. 40/60)
        ha_terrein=round(2 + n / 100, 1),
        pv_kwp=round(0.6 * n),
        batterij_kwh=round(1.2 * n),
        sauna_cabines=1 + max(0, math.ceil((n - 150) / 100)),
    )


def capex(inp: Inputs) -> list[dict]:
    p = program(inp.leden)
    loc = LOCATIONS[inp.locatie]
    g = inp.grond_prijs_factor
    extra_ha = max(0.0, p["ha_terrein"] - 1.0)  # erf is ~1 ha
    rows = []

    def add(groep, post, hoev, eenheid, prijs, label):
        rows.append(dict(groep=groep, post=post, hoeveelheid=hoev, eenheid=eenheid,
                         prijs=prijs, totaal=round(hoev * prijs), label=label))

    # Grond
    add("Grond", "Erf met opstallen (~1 ha)", 1, "erf", loc["erf_prijs"] * g, "schatting")
    add("Grond", "Aanvullende grond", extra_ha, "ha", loc["grond_per_ha"] * g, "schatting")
    grond = loc["erf_prijs"] * g + extra_ha * loc["grond_per_ha"] * g
    add("Grond", "Overdrachtsbelasting 10,4%", grond, "EUR", OVERDRACHTSBELASTING, "bron")
    add("Grond", "Notaris, taxatie, kadaster", 1, "post", NOTARIS_TAXATIE, "schatting")
    if inp.woning_afsplitsen:
        add("Grond", "Woning afsplitsen en doorverkopen (netto)", 1, "post", -inp.woning_afsplitsen, "schatting")

    # Gebouw
    add("Gebouw", "Sloop overtollige stallen + asbestsanering", p["m2_binnen"], "m2", 50, "schatting")
    add("Gebouw", "Transformatie schuur naar clubgebouw", p["m2_binnen"], "m2", inp.bouw_per_m2, "schatting")
    add("Gebouw", "Tweedehands tuinbouwkas als seizoenspaviljoen", p["m2_kas"], "m2", 450, "schatting")

    # Buiten
    add("Buiten", "Natuurzwemvijver (zwem + plantenzone)", p["m2_zwemvijver"], "m2", 280, "bron")
    add("Buiten", "Natuurontwikkeling, paden, bomen, poelen", p["ha_terrein"] - 0.5, "ha", 35_000, "schatting")
    add("Buiten", "Buitenwerkplekken (overdekte pods met stroom)", 4, "stuks", 9_000, "schatting")
    add("Buiten", "Buitengym (rig, kettlebells, sprintstrook)", 1, "post", 18_000, "schatting")

    # Wellness
    add("Wellness", "Grote sauna 12 pers. (cabine, kachel, ventilatie)", p["sauna_cabines"], "stuks", 55_000, "schatting")
    add("Wellness", "Barrelsauna 8 tot 10 pers. (houtgestookt)", 1, "stuks", 13_000, "bron")
    add("Wellness", "Koudwaterbad met koeling", 1, "stuks", 9_000, "schatting")
    add("Wellness", "Houtgestookte hot tub", 2, "stuks", 7_000, "schatting")
    add("Wellness", "Buitendouches, rustplekken, vlonders", 1, "post", 20_000, "schatting")

    # Gym
    add("Gym", "Racks + halters + schijven (refurbished)", max(3, math.ceil(inp.leden / 50)), "stuks", 4_000, "schatting")
    add("Gym", "Dumbbells, bankjes, kabelstation", 1, "post", 16_000, "schatting")
    add("Gym", "Cardio (roeiers, skierg, airbike, loopband)", 1, "post", 14_000, "schatting")
    add("Gym", "Sportvloer", max(120, inp.leden), "m2", 60, "schatting")

    # Werken
    add("Werken", "Werkplek: zit-sta bureau, refurb. ergonomische stoel, 2 schermen, dock", p["desks"], "plekken", 1_600, "schatting")
    add("Werken", "Belcellen (refurbished)", p["belcellen"], "stuks", 4_500, "schatting")
    add("Werken", "Vergaderruimtes AV", 2, "stuks", 3_000, "schatting")

    # Koffie & interieur
    add("Koffie & interieur", "3-groeps espressomachine + 2 molens + waterfilter", 1, "set", 25_000, "schatting")
    add("Koffie & interieur", "Keuken + bar", 1, "post", 30_000, "schatting")
    add("Koffie & interieur", "Tweedehands meubilair, planten, bibliotheek (biophilic)", p["m2_binnen"], "m2", 90, "schatting")
    add("Koffie & interieur", "Lockers, toegang, beveiliging", inp.leden, "leden", 120, "schatting")

    # Energie & tech
    add("Energie & tech", "Zonnepanelen", p["pv_kwp"], "kWp", 850, "schatting")
    add("Energie & tech", "Batterij", p["batterij_kwh"], "kWh", 450, "bron")
    add("Energie & tech", "Warmtepompen lucht-water + afgifte", p["m2_binnen"], "m2", 75, "schatting")
    add("Energie & tech", "Netaansluiting verzwaren", 1, "post", 25_000, "schatting")
    add("Energie & tech", "Glasvezel aanleg + wifi mesh + Starlink backup", 1, "post", 30_000, "schatting")

    bouw_inrichting = sum(r["totaal"] for r in rows if r["groep"] not in ("Grond",))

    # Bijkomend
    add("Bijkomend", "Architect, constructeur, installatieadvies (10%)", bouw_inrichting, "EUR", 0.10, "schatting")
    add("Bijkomend", "Planologisch traject (ruimtelijke onderbouwing, ecologie, stikstof, bodem)", 1, "post", 75_000, "schatting")
    add("Bijkomend", "Leges omgevingsvergunning (~3% bouwsom)", bouw_inrichting, "EUR", 0.03, "schatting")
    add("Bijkomend", "Juridisch: statuten coöperatie, AFM informatiedocument, fiscaal", 1, "post", 35_000, "schatting")
    add("Bijkomend", "Ontwikkelvergoeding initiatiefnemer", bouw_inrichting, "EUR", inp.dev_fee_pct, "aanname")
    zonder_grond = sum(r["totaal"] for r in rows if r["groep"] != "Grond")
    add("Bijkomend", "Onvoorzien (12% excl. grond)", zonder_grond, "EUR", 0.12, "schatting")
    subtotaal = sum(r["totaal"] for r in rows)
    add("Bijkomend", "Bouwrente + afsluitkosten (3%)", subtotaal, "EUR", 0.03, "schatting")
    return rows


def opex(inp: Inputs, capex_rows: list[dict]) -> list[dict]:
    p = program(inp.leden)
    n = inp.leden
    tot = lambda groep: sum(r["totaal"] for r in capex_rows if r["groep"] == groep)
    gebouw = tot("Gebouw") + tot("Buiten") + tot("Energie & tech")
    equipment = tot("Gym") + tot("Werken") + tot("Wellness") + tot("Koffie & interieur")
    grond = tot("Grond")
    rows = []

    def add(post, bedrag, label, toel=""):
        rows.append(dict(post=post, bedrag=round(bedrag), label=label, toelichting=toel))

    add(f"Host / community lead ({inp.host_fte:.1f} fte, loonkosten)", 62_000 * inp.host_fte, "schatting")
    add("Beheer en techniek (0,5 fte)", 30_000, "schatting")
    uren = 2 + 0.02 * n
    add("Schoonmaak", uren * 365 * 32, "schatting", f"{uren:.1f} uur per dag x EUR 32")
    add("Management initiatiefnemer", inp.management_fee, "aanname")
    add("Groenbeheer", p["ha_terrein"] * 5_000, "schatting", "EUR 5.000 per ha extensief")

    # Energie
    vraag = p["m2_binnen"] * 60 + 20 * 6 * 365 * p["sauna_cabines"] + 10_000  # kWh
    pv = p["pv_kwp"] * 900
    eigen = min(pv * 0.65, vraag)
    net_import = vraag - eigen
    export = pv - eigen
    add("Energie (netto)", net_import * 0.24 - export * 0.05 + 4_000, "schatting",
        f"vraag {vraag/1000:.0f} MWh, PV {pv/1000:.0f} MWh, import {net_import/1000:.0f} MWh x 0,24")
    add("Brandhout sauna en hot tubs", 4_000, "schatting")

    add("Onderhoud gebouw en terrein (1,5%)", gebouw * 0.015, "schatting")
    add("Vervangingsreserve inventaris (10%)", equipment * 0.10, "schatting")
    add("Verzekeringen", (gebouw + equipment) * 0.0025, "schatting")
    add("OZB, waterschap, riool", (grond + gebouw) * 0.7 * 0.0035, "schatting", "WOZ ~70% van kostprijs x 0,35%")
    add("Internet, Starlink, software, toegang", 9_000, "schatting")
    add("Accountant, juridisch, administratie", 18_000, "schatting")
    add("Handdoeken, verbruik, schoonmaakmiddelen", n * 1.5 * 52 * 0.9, "schatting", "1,5 bezoek per lid per week x EUR 0,90")
    add("Community, events, ballotage", 15_000, "schatting")
    sub = sum(r["bedrag"] for r in rows)
    add("Onvoorzien exploitatie (5%)", sub * 0.05, "schatting")
    return rows


def annuity(principal: float, rate: float, years: int) -> float:
    if principal <= 0:
        return 0.0
    if rate == 0:
        return principal / years
    return principal * rate / (1 - (1 + rate) ** -years)


def run(inp: Inputs) -> dict:
    cx = capex(inp)
    ox = opex(inp, cx)
    capex_tot = sum(r["totaal"] for r in cx)
    opex_tot = sum(r["bedrag"] for r in ox)
    inleg_tot = inp.inleg_per_lid * inp.leden
    lening = max(0.0, capex_tot - inleg_tot)
    jaarlast = annuity(lening, inp.rente, inp.looptijd_lening)
    leden_betalend = inp.leden * inp.bezetting
    omzet_netto = leden_betalend * inp.fee_incl_btw / (1 + inp.btw_mix) * 12 * (1 + inp.extra_omzet_pct)
    resultaat = omzet_netto - opex_tot - jaarlast
    # benodigde fee om precies quitte te spelen
    k = 12 * leden_betalend * (1 + inp.extra_omzet_pct) / (1 + inp.btw_mix)
    fee_nodig = (opex_tot + jaarlast) / k
    fee_alleen_exploitatie = opex_tot / k
    # aflossing na 5 jaar
    saldo = lening
    aflossing5 = 0.0
    for _ in range(5):
        rente = saldo * inp.rente
        afl = jaarlast - rente
        saldo -= afl
        aflossing5 += afl
    eigen_vermogen_lid_5j = (inleg_tot + aflossing5) / inp.leden
    # jaren tot schuldvrij als het volledige overschot bij deze fee naar aflossing gaat
    overschot = omzet_netto - opex_tot
    jaren_schuldvrij = None
    if lening == 0:
        jaren_schuldvrij = 0
    elif overschot > lening * inp.rente:
        s_, jaren_schuldvrij = lening, 0
        while s_ > 0 and jaren_schuldvrij < 60:
            s_ = s_ * (1 + inp.rente) - overschot
            jaren_schuldvrij += 1
    ltv = lening / capex_tot if capex_tot else 0
    return dict(
        inputs=asdict(inp),
        programma=program(inp.leden),
        capex_totaal=round(capex_tot),
        capex_per_lid=round(capex_tot / inp.leden),
        capex_groepen={g: round(sum(r["totaal"] for r in cx if r["groep"] == g))
                       for g in dict.fromkeys(r["groep"] for r in cx)},
        opex_totaal=round(opex_tot),
        opex_per_lid_pm=round(opex_tot / inp.leden / 12),
        lening=round(lening),
        ltv=round(ltv, 2),
        jaarlast=round(jaarlast),
        omzet_netto=round(omzet_netto),
        resultaat=round(resultaat),
        dscr=round((omzet_netto - opex_tot) / jaarlast, 2) if jaarlast else None,
        fee_nodig_incl_btw=round(fee_nodig),
        fee_alleen_exploitatie_incl_btw=round(fee_alleen_exploitatie),
        aflossing_5j=round(aflossing5),
        eigen_vermogen_per_lid_5j=round(eigen_vermogen_lid_5j),
        jaren_schuldvrij_bij_fee=jaren_schuldvrij,
        capex_rows=cx,
        opex_rows=ox,
    )


def eur(x):
    return f"EUR {x:,.0f}".replace(",", ".")


def naieve_som(leden=50, fee=400, maanden=60):
    return leden * fee * maanden


if __name__ == "__main__":
    out = {}

    # 1. Basisscenario detail
    base = run(Inputs())
    out["basis"] = base
    print("=== BASIS: 150 leden, locatie B, EUR 450 p/m, lening 20 jr ===")
    for r in base["capex_rows"]:
        print(f'{r["groep"]:<20}{r["post"][:58]:<60}{r["hoeveelheid"]:>10.1f} {r["eenheid"]:<8}{r["prijs"]:>12,.2f}{r["totaal"]:>12,}  [{r["label"]}]')
    print("CAPEX", eur(base["capex_totaal"]), "per lid", eur(base["capex_per_lid"]))
    for r in base["opex_rows"]:
        print(f'{r["post"]:<55}{r["bedrag"]:>10,}  [{r["label"]}] {r["toelichting"]}')
    print("OPEX", eur(base["opex_totaal"]), "per lid pm", eur(base["opex_per_lid_pm"]))
    for k in ("lening", "jaarlast", "omzet_netto", "resultaat", "dscr", "fee_nodig_incl_btw",
              "fee_alleen_exploitatie_incl_btw", "aflossing_5j", "eigen_vermogen_per_lid_5j",
              "jaren_schuldvrij_bij_fee"):
        print(k, base[k])

    # 2. Matrix: benodigde fee per locatie x ledenaantal x looptijd
    print("\n=== Benodigde maandfee incl. btw (break even) ===")
    matrix = []
    for loc in "ABC":
        for n in (75, 100, 150, 200, 250):
            for t in (5, 10, 20, 25):
                r = run(Inputs(leden=n, locatie=loc, looptijd_lening=t))
                matrix.append(dict(locatie=loc, leden=n, looptijd=t, capex=r["capex_totaal"],
                                   capex_per_lid=r["capex_per_lid"], opex_pm=r["opex_per_lid_pm"],
                                   fee=r["fee_nodig_incl_btw"],
                                   fee_expl=r["fee_alleen_exploitatie_incl_btw"]))
    out["matrix"] = matrix
    for loc in "ABC":
        print(f"Locatie {loc}: {LOCATIONS[loc]['naam']}")
        for n in (75, 100, 150, 200, 250):
            cells = [m for m in matrix if m["locatie"] == loc and m["leden"] == n]
            print(f"  {n:>3} leden capex {eur(cells[0]['capex']):>16} ({eur(cells[0]['capex_per_lid'])}/lid) "
                  + " ".join(f"{c['looptijd']}j:{c['fee']:>5}" for c in cells)
                  + f"  | alleen expl: {cells[0]['fee_expl']}")

    # 3. Scenario's laag/basis/hoog op de twee grootste aannames (bouwprijs, grondprijs)
    print("\n=== Scenario's laag/basis/hoog (150 leden, B, 20 jr) ===")
    scen = {}
    for naam, bouw, gf in (("laag", 950, 0.85), ("basis", 1300, 1.0), ("hoog", 1900, 1.25)):
        r = run(Inputs(bouw_per_m2=bouw, grond_prijs_factor=gf))
        scen[naam] = dict(bouw_per_m2=bouw, grond_factor=gf, capex=r["capex_totaal"],
                          fee=r["fee_nodig_incl_btw"], resultaat_bij_450=r["resultaat"])
        print(naam, scen[naam])
    out["scenarios"] = scen

    # 4. Financieringsvormen (150 leden, B)
    print("\n=== Financieringsvormen (150 leden, B) ===")
    fin = {}
    for naam, inleg, t in (("alles in 5 jaar afbetalen", 0, 5),
                           ("alleen maandfee, 20 jr lening", 0, 20),
                           ("inleg 10k + 20 jr", 10_000, 20),
                           ("inleg 15k + 20 jr", 15_000, 20),
                           ("inleg 15k + 25 jr", 15_000, 25)):
        r = run(Inputs(inleg_per_lid=inleg, looptijd_lening=t))
        fin[naam] = dict(inleg=inleg, looptijd=t, lening=r["lening"], ltv=r["ltv"],
                         fee=r["fee_nodig_incl_btw"], ev_lid_5j=r["eigen_vermogen_per_lid_5j"],
                         dscr_bij_450=r["dscr"])
        print(naam, fin[naam])
    out["financiering"] = fin

    # 4b. Slimme variant: woning verkopen, lean bemensing, 10% extra omzet
    print("\n=== Slimme variant (inleg 15k, 20 jr) ===")
    slim = {}
    woning = {"A": 900_000, "B": 650_000, "C": 500_000}  # netto na kosten [schatting]
    for loc in "ABC":
        for n in (150, 200):
            for inleg in (0, 15_000):
                r = run(Inputs(leden=n, locatie=loc, inleg_per_lid=inleg, woning_afsplitsen=woning[loc],
                               host_fte=0.6, extra_omzet_pct=0.10))
                slim[f"{loc}-{n}-{inleg}"] = dict(capex=r["capex_totaal"], fee=r["fee_nodig_incl_btw"],
                                                  opex_pm=r["opex_per_lid_pm"], ev_lid_5j=r["eigen_vermogen_per_lid_5j"],
                                                  ltv=r["ltv"])
                print(loc, n, inleg, slim[f"{loc}-{n}-{inleg}"])
    out["slim"] = slim

    # 4c. Aanbevolen opzet
    aanb = run(Inputs(leden=200, locatie="B", fee_incl_btw=450, inleg_per_lid=15_000))
    aanb_slim = run(Inputs(leden=200, locatie="B", fee_incl_btw=450, inleg_per_lid=15_000,
                           woning_afsplitsen=650_000, host_fte=0.6, extra_omzet_pct=0.10))
    out["aanbevolen"] = {k: {kk: v[kk] for kk in ("capex_totaal", "lening", "ltv", "dscr", "fee_nodig_incl_btw",
                                                 "fee_alleen_exploitatie_incl_btw", "jaren_schuldvrij_bij_fee",
                                                 "eigen_vermogen_per_lid_5j", "opex_per_lid_pm")}
                         for k, v in (("basis", aanb), ("slim", aanb_slim))}
    print("\n=== Aanbevolen: 200 leden, B, EUR 450, inleg 15k ===", out["aanbevolen"])

    # 5. Naieve som van de vraag
    n50 = run(Inputs(leden=50, fee_incl_btw=400, looptijd_lening=5))
    out["naief"] = dict(bruto=naieve_som(), netto_na_btw=round(naieve_som() / 1.18),
                        opex_5j_50_leden=n50["opex_totaal"] * 5,
                        vrij_voor_investering=round(naieve_som() / 1.18 - n50["opex_totaal"] * 5),
                        capex_50_leden_B=n50["capex_totaal"])
    print("\n=== Naieve som 50 x 400 x 60 ===", out["naief"])

    with open("business-case/resultaten.json", "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)


SOURCES = {
    "grondprijs": "Kadaster/WUR Q2 2026: gemiddeld EUR 108.500/ha (akker ~123.000, gras ~94.500)",
    "overdrachtsbelasting": "Belastingdienst / Rijksoverheid: niet-woning 10,4% in 2026",
    "zwemvijver": "Werkspot / Homedeal: EUR 100 tot 650 per m2",
    "batterij": "Duitse marktprijs 2026 commercieel >100 kWh: EUR 410 tot 450/kWh",
    "rente": "Zakelijke vastgoedfinanciering 2026: 4,2 tot 7%, LTV 60 tot 70%",
    "barrelsauna": "Azalp barrelsauna 1 tot 10 pers.: EUR 6.089 tot 13.009",
}
