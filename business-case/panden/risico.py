"""
Risico's voor leden: wat kost het de andere eigenaren als één lid niet betaalt, failliet gaat of vertrekt,
met en zonder spelregels. Basis: Galvanistraat (90 eigenaren) en Van Heutszstraat Utrecht (60 eigenaren),
fee op 'om te draaien' (build_ontwerpen, sober, achthoektorens).
Draaien: python3 risico.py -> risico.json
"""
from __future__ import annotations

import json
import os

import build_ontwerpen as b
import layout
import pand_case as pc

HERE = os.path.dirname(os.path.abspath(__file__))
RENTE, LOOPTIJD = 0.055, 20


def nl(x, d=0):
    t = f"{x:,.{d}f}"
    return t.replace(",", "_").replace(".", ",").replace("_", ".")


def annu(x):
    return x * RENTE / (1 - (1 + RENTE) ** -LOOPTIJD)


def basis(slug):
    k = b.pand(slug)["kpi"]
    f = k["fee"]
    r = pc.run(slug, fee_vol=f, fee_deel=f * 320 / 450, sober=True, torens=True)
    L = layout.LAYOUTS[slug]["leden"]
    V, D = L["n_vol"], L["n_deel"]
    last = annu(r["lening"])
    noemer = 12 * 0.95 / 1.18 * (V + D * 320 / 450)   # zelfde noemer als pand_case: euro fee_vol per euro jaarlast
    return dict(slug=slug, titel=b.pand(slug)["ontwerp"]["titel"], V=V, D=D, n=V + D, fee=f, fee_deel=round(f * 320 / 450),
                inleg_vol=15_000, inleg_deel=9_000, ledenkapitaal=r["inleg"], lening=r["lening"], capex=round(r["capex"]),
                opex=r["opex"], annuiteit=round(last), maand_vast=round((r["opex"] + last) / 12), noemer=noemer)


def scenarios(B):
    n, f, fd = B["n"], B["fee"], B["fee_deel"]
    gem_fee = (B["V"] * f + B["D"] * fd) / n
    gem_inleg = B["ledenkapitaal"] / n
    per = lambda bedrag, rest=n - 1: round(bedrag / rest)        # eenmalig per overgebleven eigenaar
    pm = lambda jaarbedrag: round(jaarbedrag / B["noemer"], 1)    # euro per maand op de vaste fee (incl. btw)
    S = []
    # 1. wanbetaler
    gemist = 6 * f
    S.append(dict(id="wanbetaler", titel="Eén eigenaar betaalt zes maanden niet",
                  zonder=f"{nl(gemist)} euro gemist, gedeeld door {n-1} anderen: {nl(per(gemist))} euro per persoon", zonder_eur=per(gemist),
                  met="Verrekend met zijn inleg van 15.000 euro: 0 euro voor de anderen. Na 14 dagen gaat zijn pas dicht, na 60 dagen volgt opzegging.",
                  met_eur=0, reken=f"6 x {f} = {gemist}"))
    # 2. faillissement en curator eist inleg
    S.append(dict(id="failliet", titel="Eigenaar gaat failliet en de curator wil de inleg nu terug",
                  zonder=f"15.000 euro direct uit de kas, of bijlenen: {nl(per(15000))} euro per persoon of {nl(pm(annu(15000)),1)} euro per maand extra",
                  zonder_eur=per(15000),
                  met="De curator krijgt niet meer rechten dan het lid zelf had: terugbetaling pas als er een vervanger is of na de statutaire termijn, in termijnen, minus wat hij nog schuldig is. 0 euro extra.",
                  met_eur=0, reken="15.000 / (n-1)"))
    # 3. team-BV failliet
    team = 5 * f * 6
    S.append(dict(id="team", titel="Een BV met vijf plekken gaat failliet tijdens de opzegtermijn van zes maanden",
                  zonder=f"5 x {f} x 6 = {nl(team)} euro gemist: {nl(per(team, n-5))} euro per persoon", zonder_eur=per(team, n - 5),
                  met="De vijf mensen zijn zelf lid en blijven de bijdrage verschuldigd. De BV betaalt alleen. Plus een borg van drie maanden van de BV. 0 euro voor de anderen.",
                  met_eur=0, reken=f"5 x {f} x 6"))
    # 4. vertrekgolf 10%
    k = round(n * 0.10)
    terug = round(k * gem_inleg)
    fee_weg = round(k * gem_fee * 12 * 0.95 / 1.18)
    S.append(dict(id="vertrek", titel=f"{k} eigenaren (10%) zeggen tegelijk op en er is geen wachtlijst",
                  zonder=f"{nl(terug)} euro inleg direct terug: {nl(per(terug, n-k))} euro per persoon, plus {nl(pm(fee_weg),1)} euro per maand hogere fee voor de rest",
                  zonder_eur=per(terug, n - k),
                  met=f"Twaalf maanden opzegtermijn, dus de bijdrage loopt nog een jaar door. Terugbetaling alleen uit de inleg van nieuwe leden of uit de uittredingsreserve, maximaal 5% van het ledenkapitaal per jaar ({nl(B['ledenkapitaal']*0.05)} euro). Blijven de plekken leeg, dan stijgt de fee na een jaar met {nl(pm(fee_weg),1)} euro per maand voor iedereen, tot de club de plekken weer vult. Geen eenmalige rekening.",
                  met_eur=0, reken=f"{k} x {round(gem_inleg)} gemiddelde inleg"))
    # 5. persoonlijke borg
    S.append(dict(id="borg", titel="De bank vraagt een persoonlijke borg van het bestuur",
                  zonder=f"Wie tekent, staat hoofdelijk borg voor de hele lening van {nl(B['lening'])} euro: één persoon kan alles moeten betalen",
                  zonder_eur=B["lening"],
                  met=f"Niemand tekent een persoonlijke borg. Zekerheid voor de bank: hypotheek op het pand en {round(B['ledenkapitaal']/B['capex']*100)}% eigen inleg (lening {round(B['lening']/B['capex']*100)}% van de investering). Lukt dat niet: kleinere lening of een andere bank, niet tekenen.",
                  met_eur=0, reken="lening uit pand_case"))
    # 6. bestuurder tekent fout contract
    S.append(dict(id="contract", titel="Eén bestuurder tekent een contract van 50.000 euro zonder overleg",
                  zonder=f"{nl(per(50000, n))} euro per persoon", zonder_eur=per(50000, n),
                  met="De coöperatie wordt alleen vertegenwoordigd door twee bestuurders samen. Boven 10.000 euro beslist het voltallige bestuur, boven 50.000 euro de ledenvergadering. Bankrekening met twee handtekeningen. Een contract dat buiten die grenzen is getekend, kan de coöperatie tegenhouden.",
                  met_eur=0, reken="50.000 / n"))
    # 7. schadeclaim
    S.append(dict(id="claim", titel="Iemand raakt gewond in de gym en eist 100.000 euro",
                  zonder=f"{nl(per(100000, n))} euro per persoon", zonder_eur=per(100000, n),
                  met="Aansprakelijkheidsverzekering van de coöperatie, huisregels en een gym-introductie per lid. Eigen risico 500 tot 1.000 euro.",
                  met_eur=0, reken="100.000 / n"))
    return S


def reserves(B):
    liq = 3 * B["maand_vast"]
    uit = round(B["ledenkapitaal"] * 0.05)
    tot = liq + uit
    opbouw3 = round(tot / 3)
    vooraf = round(annu(tot) / B["noemer"], 1)
    jaarlijks = round(opbouw3 / B["noemer"], 1)
    liq_vooraf = round(annu(liq) / B["noemer"], 1)          # liquiditeitsreserve meefinancieren in de start
    uit_5j = round(uit / 5 / B["noemer"], 1)                 # uittredingsreserve in vijf jaar opbouwen uit de fee
    return dict(liquiditeit=liq, uittreding=uit, totaal=tot, opbouw_per_jaar_3j=opbouw3,
                fee_extra_vooraf=vooraf, fee_extra_opbouw=jaarlijks, fee_liq_vooraf=liq_vooraf, fee_uit_5j=uit_5j,
                advies_fee=round(liq_vooraf + uit_5j, 1),
                rijen=[("Liquiditeitsreserve", "3 maanden", "maand vaste lasten incl. bank", B["maand_vast"], liq, "berekend"),
                       ("Uittredingsreserve", "5%", "van het ledenkapitaal", B["ledenkapitaal"], uit, "berekend")])


def kosten_juridisch():
    # [schatting] notaris en jurist voor een coöperatie met maatwerk uittredingsregels; verzekeringen per jaar
    return [("Statuten coöperatie U.A. bij notaris, maatwerk", 1, "akte", 2_500, 2_500, "schatting: standaard 750 tot 1.500, maatwerk uittreding en verrekening erbij"),
            ("Jurist coöperatierecht: ledenovereenkomst, reglement, toets bankvoorwaarden", 16, "uur", 200, 3_200, "schatting"),
            ("Huishoudelijk reglement en huisregels", 1, "stuk", 0, 0, "zelf schrijven op basis van de jurist"),
            ("Bestuurdersaansprakelijkheidsverzekering", 1, "jaar", 750, 750, "schatting: kleine coöperatie, dekking 500.000"),
            ("Aansprakelijkheidsverzekering bedrijven (gym, café)", 1, "jaar", 1_500, 1_500, "schatting; zit deels al in 'Verzekeringen' van de exploitatie")]


def noodverkoop(B, pand_pct=0.90, verbouw_pct=0.25):
    """Club stopt in jaar 1: pand verkocht, verbouw grotendeels verloren. [schatting] percentages."""
    koop = b.pand(B["slug"])["kpi"]["koop"]
    opbrengst = koop * pand_pct + (B["capex"] - koop) * verbouw_pct
    netto = opbrengst * 0.975 - B["lening"]          # 2,5% verkoopkosten, bank eerst
    terug = max(0.0, netto) / B["ledenkapitaal"]
    r = pc.run(B["slug"], fee_vol=B["fee"], fee_deel=B["fee"] * 320 / 450, sober=True, torens=True)
    return dict(koop=koop, opbrengst=round(opbrengst), netto=round(netto), terug_pct=round(terug * 100),
                terug_vol=round(15_000 * terug), jaar5_dekking_pct=round(min(r["exit_dekking"], 9) * 100),
                pand_pct=pand_pct, verbouw_pct=verbouw_pct)


def main():
    out = []
    for s in ("rotterdam-galvanistraat-122", "utrecht-van-heutszstraat-4"):
        B = basis(s)
        out.append(dict(basis={k: v for k, v in B.items() if k != "noemer"}, scenarios=scenarios(B), reserves=reserves(B), nood=noodverkoop(B)))
    J = dict(panden=out, juridisch=kosten_juridisch())
    json.dump(J, open(os.path.join(HERE, "risico.json"), "w"), ensure_ascii=False, indent=1)
    tpl = os.path.join(HERE, "risico_template.html")
    if os.path.exists(tpl):
        html = open(tpl, encoding="utf-8").read().replace("/*__DATA__*/null", json.dumps(J, ensure_ascii=False))
        open(os.path.join(HERE, "..", "risico.html"), "w", encoding="utf-8").write(html)
    for p in out:
        B = p["basis"]
        print("   nood", p["nood"])
        print(B["titel"], B["n"], "eigenaren, fee", B["fee"], "maand vast", B["maand_vast"], "ledenkapitaal", B["ledenkapitaal"], "lening", B["lening"])
        for sc in p["scenarios"]:
            print("  ", sc["titel"], "| zonder:", sc["zonder_eur"], "| met:", sc["met_eur"])
        print("   reserves", p["reserves"]["totaal"], "=", p["reserves"]["liquiditeit"], "+", p["reserves"]["uittreding"],
              "| advies liq vooraf +", p["reserves"]["fee_liq_vooraf"], "uit 5j +", p["reserves"]["fee_uit_5j"], "| fee +", p["reserves"]["fee_extra_vooraf"], "vooraf of +", p["reserves"]["fee_extra_opbouw"], "3 jaar opbouw")


if __name__ == "__main__":
    main()
