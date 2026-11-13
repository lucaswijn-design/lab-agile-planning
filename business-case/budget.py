"""
Budgetvariant: bestaande hal van ~600 m2, industrieel afgewerkt, verbouw in eigen
beheer (Lucas als projectmanager, vriend als afbouwmanager, interieurarchitect in
de familie), zzp'ers per vak, geen aannemersmarge. Alles per product of per m2,
arbeid en materiaal apart waar dat relevant is.

Capaciteit (60 eigenaren + 60 clubleden):
  werken   16 zit-sta plekken in eilandjes + 12 aan een lange werktafel + 8 aan de raambar
  gym      20 mensen tegelijk, 150 m2 (7,5 m2 p.p.)
  sauna    zelfgebouwde saunahut 12 pers. + koudwaterbad (geen hot tub: waterbeheer)
  café     espressobar, 1.000 boeken, lounge
Draaien: python3 business-case/budget.py
"""
from __future__ import annotations

import json
from dataclasses import dataclass, asdict

OVB = 0.104  # [bron] niet-woning 2026
ZZP = dict(timmerman=49, elektricien=56, loodgieter=57, schilder=45, hovenier=45)  # [bron] Knab 2026 excl. btw

LOC = {
    "brabant": dict(naam="Brabantse stedenrij: Best, Boxtel, Oirschot, Vught", hal=1_200, grond=175, verhuur=90),
    "randstad": dict(naam="Randstadrand: Woerden, Gouda, Bodegraven", hal=1_650, grond=300, verhuur=120),
    "modern": dict(naam="Moderne energieneutrale hal, Amersfoort De Isselt (785 m2)", hal=1_592, grond=250, verhuur=110),
}


@dataclass
class B:
    loc: str = "brabant"
    hal_m2: int = 600
    n_vol: int = 30
    n_deel: int = 30
    n_club: int = 60
    fee_vol: float = 450
    fee_deel: float = 320
    fee_club: float = 119
    inleg_vol: float = 15_000
    inleg_deel: float = 9_000
    eigen_beheer: bool = True  # False = aannemer: +15% AK/W&R en uitvoering
    sauna: bool = False  # sauna geschrapt in versie 8: het boekencafé is het hart van de club
    rente: float = 0.055
    looptijd: int = 20
    waardegroei: float = 0.02
    bezetting: float = 0.95
    schoonmaak_dagen: int = 5


def items(k: B):
    """Boodschappenlijst: (groep, post, hoeveelheid, eenheid, prijs, label, blijft-bij-exit)."""
    L = LOC[k.loc]
    modern = k.loc == "modern"
    hal = 785 if modern else k.hal_m2
    gevel = 0.0 if modern else 450  # m2 binnenzijde gevel tot 4 m hoogte (100 m omtrek x 4,5 m min openingen)
    R = []

    def add(g, post, h, e, p, label, gen=0.0):
        R.append(dict(groep=g, post=post, h=h, e=e, prijs=p, totaal=round(h * p), label=label, gen=gen))

    # --- Pand
    add("Pand", f"Bestaande hal incl. perceel ~2x pand ({hal} m2)", hal, "m2", L["hal"], "schatting", 1.0)
    extra = hal  # perceel naar ~3x pand
    add("Pand", "Extra buitenterrein naar 3x pandoppervlak", extra, "m2", L["grond"], "schatting", 1.0)
    add("Pand", "Overdrachtsbelasting 10,4%", hal * L["hal"] + extra * L["grond"], "EUR", OVB, "bron")
    add("Pand", "Notaris, taxatie, bouwkundige keuring", 1, "post", 8_000, "schatting")

    # --- Bouwkundig (industrieel: beton blijft, staal blijft zichtbaar)
    add("Bouwkundig", "Asbestinventarisatie", 1, "post", 1_500, "schatting")
    add("Bouwkundig", "Reserve asbestsanering dak (bij bouwjaar voor 1994)", 1, "post", 10_000, "schatting")
    if not modern:
        add("Bouwkundig", "Dakisolatie binnenzijde PIR 100 mm, materiaal", hal, "m2", 25, "bron", 0.6)
        add("Bouwkundig", "Dakisolatie, arbeid timmerman 0,4 u/m2", hal * 0.4, "uur", ZZP["timmerman"], "bron", 0.6)
        add("Bouwkundig", "Gevelisolatie binnenzijde (voorzetwand PIR + OSB)", gevel, "m2", 40, "bron", 0.6)
    add("Bouwkundig", "Glazen pui naar de tuin, aluminium HR+++ triple glas", 24, "m2", 1_000, "bron", 0.6)
    add("Bouwkundig", "Ramen in gevel, aluminium HR+++ triple glas", 0 if modern else 16, "m2", 1_000, "bron", 0.6)
    add("Bouwkundig", "Lichtstraten in het dak (daglicht voor planten)", 0 if modern else 6, "st", 2_500, "schatting", 0.5)
    add("Bouwkundig", "Betonvloer schuren en coaten (industrieel)", hal - 150, "m2", 22, "schatting", 0.3)
    add("Bouwkundig", "Binnenwanden metal stud + OSB (sanitair, vergader, techniek)", 150, "m2", 60, "schatting", 0.2)
    add("Bouwkundig", "Glazen scheidingswand gym en vergaderruimte (staal + glas)", 25, "m2", 320, "schatting", 0.2)
    add("Bouwkundig", "Akoestische plafondeilanden en wandpanelen", 200, "m2", 40, "bron")
    add("Bouwkundig", "Sauswerk wanden en staal, schilder 0,15 u/m2 + verf", 700, "m2", 9, "schatting")

    # --- Sanitair en keuken
    add("Sanitair", "Toiletten incl. 1 invalidentoilet (pot, fontein, scheidingswand)", 4, "st", 900, "schatting", 0.4)
    add("Sanitair", "Douches (thermostaatkraan, regendouche, afvoergoot)", 4, "st", 700, "schatting", 0.4)
    add("Sanitair", "Tegelwerk douches en kleedruimte (materiaal + zetten)", 45, "m2", 75, "schatting")
    add("Sanitair", "Warmtepompboiler 300 liter", 1, "st", 3_500, "schatting", 0.5)
    add("Sanitair", "Leidingwerk en riolering, materiaal", 1, "post", 4_000, "schatting", 0.5)
    add("Sanitair", "Loodgieter", 140, "uur", ZZP["loodgieter"], "bron", 0.5)
    add("Sanitair", "Keuken 6 m + kookeiland (IKEA METOD, composiet blad), 2 vaatwassers, combi-stoomoven, inductie, 2 koelkasten, afzuiging, montage", 1, "post", 16_000, "schatting")

    # --- Installaties
    add("Installaties", "Groepenkast, bekabeling, wandcontacten, data: materiaal", 1, "post", 9_000, "schatting", 0.6)
    add("Installaties", "Elektricien", 220, "uur", ZZP["elektricien"], "bron", 0.6)
    add("Installaties", "Lucht-lucht warmtepompen, 4 buitenunits met 12 binnenunits", 4, "systeem", 5_500, "bron", 0.6)
    add("Installaties", "Industriële plafondventilatoren (luchtmenging)", 2, "st", 2_500, "schatting", 0.4)
    add("Installaties", "WTW-ventilatie, 2 units + kanalen + afzuiging sanitair", 1, "post", 17_500, "schatting", 0.6)
    add("Installaties", "Brandmelders, noodverlichting, blusmiddelen", 1, "post", 6_000, "schatting", 0.5)
    add("Installaties", "Toegangssysteem met app, 6 deuren + 4 camera's", 1, "post", 4_500, "schatting", 0.2)
    add("Installaties", "Wifi: 6 access points, switch, router, Starlink backup", 1, "post", 4_000, "schatting")

    # --- Verlichting
    add("Verlichting", "Industriële LED-hanglampen (1 per 15 m2)", 40, "st", 90, "schatting")
    add("Verlichting", "Sfeerverlichting en spots op rails", 30, "st", 40, "schatting")
    add("Verlichting", "Bureaulampen", 16, "st", 45, "schatting")
    add("Verlichting", "Buitenverlichting", 10, "st", 60, "schatting")
    add("Verlichting", "Groeilampen voor planten", 12, "st", 80, "schatting")

    # --- Energie
    add("Energie", "Zonnepanelen op het haldak, eigen inkoop", 0 if modern else 40, "kWp", 750, "schatting", 0.6)
    add("Energie", "Batterij", 30, "kWh", 450, "bron", 0.5)

    # --- Werken
    add("Werken", "Zit-sta onderstel elektrisch (IKEA MITTZON)", 16, "st", 340, "bron", 0.3)
    add("Werken", "Bureaublad 140 x 70 eiken multiplex", 16, "st", 100, "schatting", 0.2)
    add("Werken", "Refurbished Steelcase Leap V2 (excl. btw)", 16, "st", 500, "bron", 0.4)
    add("Werken", "Monitor 27 inch met USB-C hub (Dell P2725HE, excl. btw)", 16, "st", 219, "bron", 0.3)
    add("Werken", "Tweede monitor 27 inch Full HD", 16, "st", 150, "schatting", 0.3)
    add("Werken", "Dubbele monitorarm", 16, "st", 60, "schatting", 0.2)
    add("Werken", "Raambar met stopcontacten, 8 krukken", 1, "post", 1_900, "schatting")
    add("Werken", "Lange werktafel staal + hout, 12 plekken", 2, "st", 800, "schatting")
    add("Werken", "Stoelen werktafel (tweedehands design)", 12, "st", 120, "schatting")
    add("Werken", "Vergaderruimte: tafel, 8 stoelen, 55 inch scherm", 1, "post", 3_000, "schatting")
    add("Werken", "Belcellen zelfgebouwd (frame, akoestiek, deur, ventilator)", 2, "st", 2_500, "schatting")
    add("Werken", "Lockers", 60, "st", 60, "schatting")

    # --- Gym (20 tegelijk, 150 m2)
    add("Gym", "ATX power rack PRX-710", 4, "st", 800, "bron", 0.3)
    add("Gym", "ATX cable half rack met 2 x 90 kg", 1, "st", 2_950, "bron", 0.3)
    add("Gym", "Olympische halterstangen + 1 trapbar", 5, "st", 240, "schatting", 0.3)
    add("Gym", "Bumper plates (4 sets van 150 kg)", 600, "kg", 3.83, "bron", 0.4)
    add("Gym", "Dumbbells hex 2,5 tot 40 kg (16 paar, 680 kg) + rek", 680, "kg", 4.1, "schatting", 0.4)
    add("Gym", "Kettlebells 8 tot 32 kg (2 sets)", 240, "kg", 3, "schatting", 0.4)
    add("Gym", "Verstelbare bankjes", 6, "st", 250, "schatting", 0.3)
    add("Gym", "Concept2 RowErg", 2, "st", 1_195, "bron", 0.5)
    add("Gym", "Concept2 SkiErg + BikeErg + airbike", 1, "set", 3_250, "schatting", 0.5)
    add("Gym", "Boxen, banden, medicijnballen, ringen, matten, landmine", 1, "post", 2_500, "schatting")
    add("Gym", "Rubber sportvloer 30 mm", 150, "m2", 35, "schatting", 0.2)
    add("Gym", "Spiegels en speaker", 1, "post", 1_000, "schatting")
    add("Gym", "Buitenrig en sprintstrook", 1, "post", 2_500, "schatting", 0.3)

    # --- Wellness (optioneel)
    if k.sauna:
      add("Wellness", "Saunahut 3 x 4 m, 12 pers., thermowood + isolatie + glazen deur", 1, "post", 9_000, "schatting", 0.4)
      add("Wellness", "Harvia Legend 240 houtkachel + stenen + rookkanaal", 1, "post", 2_700, "bron", 0.4)
      add("Wellness", "Bouw saunahut, timmerman", 120, "uur", ZZP["timmerman"], "bron", 0.4)
      add("Wellness", "Koudwaterbad 1.000 l met eenvoudige koeling", 1, "st", 2_500, "schatting", 0.3)
      add("Wellness", "Buitendouches, ligbedden, haken, vlonder rond sauna", 1, "post", 4_000, "schatting")

    # --- Café, lounge en bibliotheek
    add("Café & bieb", "Tweedehands La Marzocco Linea 3-groeps, gereviseerd", 1, "st", 7_500, "schatting", 0.6)
    add("Café & bieb", "2 tweedehands molens (Mazzer of Mahlkönig)", 2, "st", 1_200, "schatting", 0.5)
    add("Café & bieb", "Waterfilter, knockbox, pitchers, kopjes", 1, "post", 1_500, "schatting")
    add("Café & bieb", "Bar zelfgebouwd (staal + hout)", 1, "post", 2_500, "schatting")
    add("Café & bieb", "Boeken tweedehands: self-help, psychologie, geld, biografie, filosofie, romans", 1_500, "st", 6, "aanname")
    add("Café & bieb", "Leesbibliotheek: 8 leesfauteuils, leeslampen, kleden (tweedehands)", 1, "post", 2_400, "schatting")
    add("Café & bieb", "Elektrische sfeerhaard, platenspeler + speakers", 1, "post", 1_800, "schatting")
    add("Café & bieb", "Nieuwe titels die tweedehands lastig zijn", 100, "st", 20, "schatting")
    add("Café & bieb", "Boekenwand staal + steigerhout 12 m x 2,4 m + rolladder", 1, "post", 4_000, "schatting")
    add("Café & bieb", "Lounge: 4 banken, 10 fauteuils, bijzettafels, kleden (tweedehands)", 1, "post", 4_200, "schatting")
    add("Café & bieb", "Cafétafels en 24 stoelen (tweedehands)", 1, "post", 2_100, "schatting")
    add("Café & bieb", "Bomen binnen 2 tot 2,5 m (ficus, strelitzia, olijf)", 10, "st", 250, "bron")
    add("Café & bieb", "Middelgrote planten + hangplanten + potten en bakken", 1, "post", 6_000, "schatting")
    add("Café & bieb", "Stilteleeshoek: akoestisch gordijn, leesstoelen, lampen", 1, "post", 1_500, "schatting")
    add("Café & bieb", "Studio voor yoga en workshops: matten, blokken, spiegelwand, speaker", 1, "post", 2_500, "schatting")
    add("Café & bieb", "AED en EHBO-kast", 1, "post", 1_800, "schatting")
    add("Café & bieb", "Vintage decoratie en kunst", 1, "post", 3_000, "schatting")

    # --- Buiten (perceel 3x pand: ~1.200 m2 buiten)
    add("Buiten", "Onttegelen en groen aanleggen (met ledendag + hovenier)", 600, "m2", 25, "schatting", 0.3)
    add("Buiten", "Bomen en hagen", 1, "post", 3_500, "schatting", 0.3)
    add("Buiten", "Houten vlonder 80 m2 + overkapping 60 m2 (staal + polycarbonaat)", 1, "post", 12_800, "schatting", 0.3)
    add("Buiten", "Buitenwerkplekken: 4 tafels met stroom", 1, "post", 3_000, "schatting")
    add("Buiten", "Fietsenstalling 40 plekken", 1, "post", 3_000, "schatting", 0.3)
    add("Buiten", "Parkeerplaatsen belijnen op bestaande verharding", 1, "post", 1_000, "schatting")

    # --- Bijkomend
    bouw = sum(r["totaal"] for r in R if r["groep"] != "Pand")
    if not k.eigen_beheer:
        add("Bijkomend", "Aannemer: algemene kosten, winst en risico (15%)", bouw, "EUR", 0.15, "schatting")
    add("Bijkomend", "Bouwtekeningen en interieurontwerp (familie, vriendenprijs)", 1, "post", 8_000, "aanname")
    add("Bijkomend", "Constructeur en brandveiligheidsadvies", 1, "post", 5_500, "schatting")
    add("Bijkomend", "Afwijking omgevingsplan: onderbouwing + leges", 1, "post", 15_500, "schatting")
    add("Bijkomend", "Afbouwmanager (vriend), 6 maanden halftime", 600, "uur", 50, "aanname")
    add("Bijkomend", "Bouwplaats: hoogwerker 6 weken, afvalcontainers", 1, "post", 6_300, "schatting")
    add("Bijkomend", "Notaris en statuten coöperatie", 1, "post", 15_000, "schatting")
    add("Bijkomend", "Projectleiding initiatiefnemer (3% van verbouw en inrichting)", bouw, "EUR", 0.03, "aanname")
    zg = sum(r["totaal"] for r in R if r["groep"] != "Pand")
    add("Bijkomend", "Onvoorzien (10% excl. pand)", zg, "EUR", 0.10, "schatting")
    add("Bijkomend", "Bouwrente en afsluitkosten (1,5%, bouwtijd 5 maanden)", sum(r["totaal"] for r in R), "EUR", 0.015, "schatting")
    return R, hal


def opex(k: B, R, hal):
    tot = lambda g: sum(r["totaal"] for r in R if r["groep"] == g)
    pand = tot("Pand")
    gebouw = tot("Bouwkundig") + tot("Sanitair") + tot("Installaties") + tot("Energie") + tot("Buiten")
    inv = tot("Werken") + tot("Gym") + tot("Wellness") + tot("Café & bieb") + tot("Verlichting")
    rows = []

    def add(post, b, label, t=""):
        rows.append(dict(post=post, bedrag=round(b), label=label, t=t))

    add("Schoonmaak", k.schoonmaak_dagen * 4 * 52 * 30, "schatting", f"{k.schoonmaak_dagen} dagen x 4 uur x EUR 30")
    add("Management initiatiefnemer (~1 dag per week)", 18_000, "aanname")
    add("Klusjes en storingen (op afroep)", 5_000, "schatting")
    add("Groenbeheer en planten binnen", 4_000, "schatting")
    pv = (0 if k.loc == "modern" else 40) * 900
    vraag = hal * 70 + 4_000
    eigen = min(pv * 0.6, vraag)
    add("Energie netto", (vraag - eigen) * 0.24 - (pv - eigen) * 0.05 + 3_000, "schatting",
        f"vraag {vraag/1000:.0f} MWh, zon {pv/1000:.0f} MWh")
    if k.sauna:
        add("Brandhout sauna", 5_000, "schatting")
    add("Onderhoud pand en terrein", (gebouw + pand * 0.3) * 0.015, "schatting")
    add("Vervangingsreserve inventaris (10%)", inv * 0.10, "schatting")
    add("Verzekeringen", (gebouw + inv + pand * 0.5) * 0.0025, "schatting")
    add("OZB, waterschap, riool", (pand + gebouw) * 0.7 * 0.0035, "schatting")
    add("Internet, software, toegangsapp", 5_000, "schatting")
    add("Accountant en administratie", 10_000, "schatting")
    add("Koffie-apparatuur onderhoud, verbruik", 4_000, "schatting")
    add("Community en events", 5_000, "schatting")
    add("Onvoorzien exploitatie (5%)", sum(r["bedrag"] for r in rows) * 0.05, "schatting")
    return rows


def run(k: B):
    R, hal = items(k)
    O_rows = opex(k, R, hal)
    C = sum(r["totaal"] for r in R)
    O = sum(r["bedrag"] for r in O_rows)
    # moderne hal is 785 m2: 185 m2 verhuren aan een derde
    verhuur = (hal - k.hal_m2) * LOC[k.loc]["verhuur"] if hal > k.hal_m2 else 0
    inleg = k.n_vol * k.inleg_vol + k.n_deel * k.inleg_deel
    lening = max(0, C - inleg)
    last = 0 if lening <= 0 else lening * k.rente / (1 - (1 + k.rente) ** -k.looptijd)
    b = k.bezetting
    o_eig = (k.n_vol * k.fee_vol + k.n_deel * k.fee_deel) * b / 1.18 * 12
    o_club = k.n_club * k.fee_club * b / 1.15 * 12
    over = o_eig + o_club + verhuur - O
    ratio = k.fee_deel / k.fee_vol
    noemer = 12 * b / 1.18 * (k.n_vol + k.n_deel * ratio)
    fee_nodig = (O + last - o_club - verhuur) / noemer
    s_ann = s_v = lening
    for _ in range(5):
        s_ann = s_ann * (1 + k.rente) - last
        s_v = max(0.0, s_v * (1 + k.rente) - over)
    pand_w = sum(r["totaal"] for r in R if r["groep"] == "Pand" and r["gen"] == 1.0) * (1 + k.waardegroei) ** 5
    exitw = pand_w + sum(r["totaal"] * r["gen"] for r in R if r["groep"] != "Pand")
    netto = exitw * 0.975
    aandelen = k.n_vol + 0.6 * k.n_deel
    jaren = None
    if over > lening * k.rente:
        s, jaren = lening, 0
        while s > 0 and jaren < 60:
            s = s * (1 + k.rente) - over
            jaren += 1
    groepen = {}
    for r in R:
        groepen[r["groep"]] = groepen.get(r["groep"], 0) + r["totaal"]
    return dict(inputs=asdict(k), hal=hal, capex=C, groepen=groepen, inrichting_en_verbouw=C - groepen["Pand"],
                opex=O, verhuur=round(verhuur), inleg=inleg, lening=round(lening), ltv=round(lening / C, 2),
                jaarlast=round(last), omzet_club=round(o_club), resultaat=round(over - last),
                dscr=round(over / last, 2) if last else None, fee_vol_nodig=round(fee_nodig),
                fee_deel_nodig=round(fee_nodig * ratio), jaren_schuldvrij=jaren,
                fee_vol_na_aflossing=round(max(0, (O - o_club - verhuur) / noemer)),
                exitwaarde=round(exitw), exit_per_vol=round((netto - s_ann) / aandelen),
                exit_per_vol_versneld=round((netto - s_v) / aandelen),
                exit_dekking_versneld=round((netto - s_v) / inleg, 2),
                rows=R, opex_rows=O_rows)


def fee_voor_inleg_terug(**kw):
    lo, hi = 100.0, 1500.0
    for _ in range(40):
        f = (lo + hi) / 2
        r = run(B(fee_vol=f, fee_deel=f * 320 / 450, **kw))
        if r["exit_dekking_versneld"] >= 1:
            hi = f
        else:
            lo = f
    return round(hi)


if __name__ == "__main__":
    base = run(B())
    for r in base["rows"]:
        print(f'{r["groep"]:<13}{r["post"][:62]:<64}{r["h"]:>8.0f} {r["e"]:<8}{r["prijs"]:>9,.2f}{r["totaal"]:>10,} [{r["label"]}]')
    print("GROEPEN", base["groepen"])
    print("CAPEX", base["capex"], "waarvan verbouw+inrichting+bijkomend", base["inrichting_en_verbouw"])
    for r in base["opex_rows"]:
        print(f'  {r["post"]:<46}{r["bedrag"]:>8,}')
    keys = ("capex", "inrichting_en_verbouw", "opex", "lening", "ltv", "dscr", "resultaat", "fee_vol_nodig",
            "fee_deel_nodig", "jaren_schuldvrij", "fee_vol_na_aflossing", "exitwaarde", "exit_per_vol",
            "exit_per_vol_versneld", "exit_dekking_versneld", "verhuur")
    print({x: base[x] for x in keys})
    out = {"basis": {x: base[x] for x in keys}, "varianten": {}}
    cases = {
        "Brabant, eigen beheer": dict(),
        "Brabant, met aannemer": dict(eigen_beheer=False),
        "Randstadrand, eigen beheer": dict(loc="randstad"),
        "Moderne hal Amersfoort (185 m2 verhuurd)": dict(loc="modern"),
        "Brabant, 90 clubleden": dict(n_club=90),
        "Brabant, 30 clubleden": dict(n_club=30),
        "Brabant, 25 vol + 25 deel": dict(n_vol=25, n_deel=25),
        "Randstadrand, 90 clubleden": dict(loc="randstad", n_club=90),
    }
    print()
    for n, kw in cases.items():
        r = run(B(**kw))
        d = {x: r[x] for x in keys}
        d["fee_inleg_terug"] = fee_voor_inleg_terug(**kw)
        out["varianten"][n] = d
        print(n, d)
    with open("business-case/resultaten_budget.json", "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
