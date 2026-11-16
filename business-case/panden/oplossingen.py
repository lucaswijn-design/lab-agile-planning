"""
Problemen uit de councils (16-11-2026) en oplossingen, doorgerekend voor de top vijf.
Basis is het aangepaste model: personeel (host 0,5 + beheer 0,2 fte), DSCR 1,2, lening max 70% van onderpand
(koopsom + 50% gebouwgebonden verbouw), startbudget (batterij en extra's naar fase 2), sober, achthoektorens.
Draaien: python3 oplossingen.py -> oplossingen.json
"""
from __future__ import annotations

import json
import os

import layout
import pand_case as pc

HERE = os.path.dirname(os.path.abspath(__file__))
TOP = ["utrecht-van-heutszstraat-4", "rotterdam-metaalhof-40", "den-bosch-eendenkooi-1a", "pernis-ring-15", "dordrecht-laan-van-europa-360"]
OUD = {  # vergelijking van 16-11 vóór de councils: om te draaien / inleg terug
    "pernis-ring-15": (228, 399), "utrecht-van-heutszstraat-4": (162, 316), "rotterdam-metaalhof-40": (215, 320),
    "rotterdam-galvanistraat-122": (230, 329), "den-bosch-eendenkooi-1a": (327, 427),
    "dordrecht-laan-van-europa-360": (396, 532)}
KW = dict(sober=True, torens=True)
RESERVE = 18          # liquiditeitsreserve + uitkoopfonds, euro per maand op de fee vol [berekend in risico.py]
OPP = 0.03            # gemiste opbrengst op de inleg (spaarrente/beleggen) [schatting]


def annu(x, r=0.055, n=20):
    return x * r / (1 - (1 + r) ** -n)


def titel(slug):
    import ontwerp
    return ontwerp.ONTWERPEN[slug]["titel"]


def pand(slug):
    r = pc.run(slug, **KW)
    f = r["fee_vol_nodig"]
    terug = pc.fee_inleg_terug(slug, **KW)
    dek = pc.dekking_bij(slug, f, **KW)
    L = layout.LAYOUTS[slug]["leden"]
    noemer = r["noemer"]

    # 1. personeel: drie modellen
    pers = {}
    for naam, kw in (("Host 0,5 + beheer 0,2 (basis)", {}),
                     ("Café verpachten aan een ondernemer, host 0,2 + beheer 0,2", dict(host_fte=0.2, extra_opbrengst=9_600)),
                     ("Volle bezetting: host 1,0 + beheer 0,5", dict(host_fte=1.0, beheer_fte=0.5)),
                     ("Zonder personeel (oude model)", dict(host_fte=0.0, beheer_fte=0.0))):
        pers[naam] = pc.run(slug, **KW, **kw)["fee_vol_nodig"]

    # 2. de lening die de bank niet geeft: extra inleg of achtergestelde ledenlening (4%, 10 jaar) [schatting]
    tekort = r["inleg_tekort"]
    ledenlening_fee = None
    if tekort > 0:
        r_open = pc.run(slug, **KW, ltv_max=5)   # zonder leengrens: zelfde inleg als nu
        # fee als de bank het tekort niet leent maar leden het achtergesteld lenen tegen 4% in 10 jaar
        bank_zonder_tekort = r_open["lening"] - tekort
        ledenlening_fee = round((r_open["opex"] + 1.2 * annu(bank_zonder_tekort) + annu(tekort, 0.04, 10)
                                 - L["n_club"] * 119 * 0.95 / 1.15 * 12 - r_open["huur"]) / noemer)

    # 3. clubleden: helft minder
    club_half = pc.run(slug, **KW, n_club=L["n_club"] // 2)["fee_vol_nodig"]

    # 4. eigenaar of huurlid: wat kost het per maand, vol lid
    inleg = r["inleg_vol_nodig"]
    erosie = max(0.0, inleg * (1 - dek) / 60)
    eigenaar = f + RESERVE + inleg * OPP / 12 + erosie
    basis_huur = terug if terug else f + erosie
    huurlid = (basis_huur + inleg * 0.055 / 12) * 1.10
    # 5. groen dak (sedum 200 m2 + constructieve check) [schatting]
    groen = round(annu(200 * 55 + 1_500) / noemer, 1)
    return dict(slug=slug, titel=titel(slug), eigenaren=L["n_vol"] + L["n_deel"], club=L["n_club"],
                oud_fee=OUD[slug][0], oud_terug=OUD[slug][1], fee=f, prijs=f + RESERVE, terug=terug, dekking=round(dek, 2),
                inleg_vol=inleg, inleg_deel=r["inleg_deel_nodig"], ltv_koop=r["ltv_koop"], lening=r["lening"], koop=r["koop"],
                tekort=tekort, tekort_pp=round(tekort / (L["n_vol"] + L["n_deel"])) if tekort else 0, ledenlening_fee=ledenlening_fee,
                personeel=pers, club_half=club_half, eigenaar=round(eigenaar), huurlid=round(huurlid), erosie=round(erosie),
                groen_dak_pm=groen, capex=round(r["capex"]))


def startbudget():
    """Wat het startbudget scheelt bij Metaalhof."""
    pc.START = False
    a = pc.run("rotterdam-metaalhof-40", **KW)
    pc.START = True
    b = pc.run("rotterdam-metaalhof-40", **KW)
    rows = [dict(post=r["post"], totaal=r["totaal"]) for r in b["rows"] if "[start:" in r["post"]]
    oud = {r["post"]: r["totaal"] for r in a["rows"]}
    for x in rows:
        x["was"] = oud.get(x["post"].split(" [start:")[0])
    return dict(capex_oud=round(a["capex"]), capex_nieuw=round(b["capex"]), fee_oud=a["fee_vol_nodig"], fee_nieuw=b["fee_vol_nodig"], rijen=rows)


def main():
    P = [pand(s) for s in TOP]
    from omgevingsplan_check import OORDEEL
    import ontwerp as _o
    plan = [dict(slug=s, titel=_o.ONTWERPEN[s]["titel"] if s in _o.ONTWERPEN else s, status=v[0], bestemming=v[1], regels=v[2], gevolg=v[3]) for s, v in OORDEEL.items()]
    J = dict(panden=P, start=startbudget(), omgevingsplan=plan, uitgangspunten=dict(pc.BEMENSING, dscr=pc.DSCR, ltv_max=pc.LTV_MAX, onderpand_verbouw=pc.ONDERPAND_VERBOUW,
                                                                reserve=RESERVE, opp=OPP))
    json.dump(J, open(os.path.join(HERE, "oplossingen.json"), "w"), ensure_ascii=False, indent=1)
    tpl = open(os.path.join(HERE, "oplossingen_template.html"), encoding="utf-8").read()
    open(os.path.join(HERE, "..", "oplossingen.html"), "w", encoding="utf-8").write(tpl.replace("/*__DATA__*/null", json.dumps(J, ensure_ascii=False)))
    for p in P:
        print(f'{p["titel"][:28]:28} oud {p["oud_fee"]}/{p["oud_terug"]} -> {p["fee"]}/{p["terug"]} prijs {p["prijs"]} dek {p["dekking"]} inleg {p["inleg_vol"]} ltv_koop {p["ltv_koop"]} '
              f'tekort pp {p["tekort_pp"]} ll {p["ledenlening_fee"]} | pers {list(p["personeel"].values())} | club/2 {p["club_half"]} | eig {p["eigenaar"]} huur {p["huurlid"]} | groen +{p["groen_dak_pm"]}')
    print(J["start"]["capex_oud"], "->", J["start"]["capex_nieuw"], J["start"]["fee_oud"], "->", J["start"]["fee_nieuw"])


if __name__ == "__main__":
    main()
