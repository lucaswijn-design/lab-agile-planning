"""
Variant: investeerder in plaats van leden, en commercieel verhuren zoals The Social Hub (maandabonnementen zonder inleg).
Zelfde pand, verbouw en basiskosten als pand_case (sober, startbudget, personeel), aangevuld met wat een commerciële
exploitatie extra kost en oplevert. Alle prijzen excl. btw (commercieel is alles btw-belast en aftrekbaar).
Draaien: python3 commercieel.py -> commercieel.json
"""
from __future__ import annotations

import json
import os

import build_ontwerpen as b
import pand_case as pc

HERE = os.path.dirname(os.path.abspath(__file__))

AANNAMES = dict(
    leden_per_werkplek=1.5,        # [schatting] flexabonnementen per werkplek bij volle bezetting (overboeking)
    arpu=185,                      # [schatting] gemiddelde prijs per werkabonnement p/m excl. btw: vast 275, flex 175, 2-3 dagen 120 (The Social Hub flex 127, vast 270)
    dagpassen_per_dag=4, dagpas=22, werkdagen=250,          # [schatting]
    vergader_uur_week=6, vergader_tarief=30,                # [schatting] externe verhuur per kamer
    events_jaar=10_000,            # [schatting] avondverhuur, workshops
    gymleden=40, gym_prijs=45,     # [schatting] alleen-gym; mag alleen waar sport is toegestaan
    cafe_pacht_jaar=9_600,         # [schatting] alleen waar horeca is toegestaan
    bezetting=(0.55, 0.75, 0.85),  # [schatting] jaar 1, 2, 3 en verder; break-even in de branche ligt rond 70 tot 80%
    community_fte_extra=0.5,       # host van 0,5 naar 1,0 fte
    marketing_jaar=20_000,         # [schatting] werving van onbekenden in plaats van leden die zelf werven
    platform_pct=0.03,             # [schatting] betaal- en boekingskosten
    vpb=0.19,                      # [bron] vpb-tarief tot € 200.000 winst (2026)
    ltv=0.65,                      # [schatting] bank op onderpand bij commerciële exploitatie
    rente=0.06, looptijd=20,       # [schatting] iets hoger dan bij de coöperatie: geen ledenkapitaal als buffer
    extra_capex_pct=0.04,          # [schatting] betaalde arbeid voor wat leden in de coöperatie zelf doen (sauzen, inrichten)
    groei_prijs=0.02, groei_kosten=0.025, groei_pand=0.02,
    rendementseis=0.10,            # [schatting] wat een particuliere investeerder vraagt voor een eenmalige coworkinglocatie
)


def annu(x, r, n):
    return x * r / (1 - (1 + r) ** -n)


def irr(cfs):
    lo, hi = -0.99, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        v = sum(c / (1 + mid) ** t for t, c in enumerate(cfs))
        lo, hi = (mid, hi) if v > 0 else (lo, mid)
    return (lo + hi) / 2


def model(slug, sport_mag, horeca_mag, A=AANNAMES, jaren=10):
    r = pc.run(slug, sober=True, torens=True)
    k = b.pand(slug)["kpi"]
    W = k["werkplekken"]
    kamers = len([v for v in (k.get("vergaderkamers") or []) if v])
    capex = r["capex"] * (1 + A["extra_capex_pct"]) - 15_000 + 3_000   # geen coöperatie-statuten, wel een BV
    lening = min(A["ltv"] * r["onderpand"], capex)
    eigen = capex - lening
    last = annu(lening, A["rente"], A["looptijd"])
    opex_basis = r["opex"] - 18_000 + A["community_fte_extra"] * pc.BEMENSING["host_kost"] + A["marketing_jaar"]
    cfs, rows = [-eigen], []
    schuld = lening
    for j in range(1, jaren + 1):
        bez = A["bezetting"][min(j, 3) - 1]
        p = (1 + A["groei_prijs"]) ** (j - 1)
        leden = W * A["leden_per_werkplek"] * bez
        omzet = (leden * A["arpu"] * 12 + A["dagpassen_per_dag"] * A["dagpas"] * A["werkdagen"] * bez
                 + kamers * A["vergader_uur_week"] * A["vergader_tarief"] * 48 * bez + A["events_jaar"]
                 + (A["gymleden"] * A["gym_prijs"] * 12 * bez if sport_mag else 0) + (A["cafe_pacht_jaar"] if horeca_mag else 0)) * p
        kosten = opex_basis * (1 + A["groei_kosten"]) ** (j - 1) + omzet * A["platform_pct"]
        ebitda = omzet - kosten
        rente_j = schuld * A["rente"]
        schuld = schuld * (1 + A["rente"]) - last
        afschrijving = (capex - r["groepen"]["Pand"]) / 10
        winst = ebitda - rente_j - afschrijving
        belasting = max(0.0, winst) * A["vpb"]
        cf = ebitda - last - belasting
        rows.append(dict(jaar=j, bezetting=bez, leden=round(leden), omzet=round(omzet), kosten=round(kosten), ebitda=round(ebitda),
                         bank=round(last), vpb=round(belasting), cf=round(cf), dscr=round(ebitda / last, 2)))
        cfs.append(cf)
    exitw = r["onderpand"] * (1 + A["groei_pand"]) ** jaren
    cfs[-1] += exitw * 0.975 - max(0.0, schuld)
    stab = rows[2]
    # welke prijs per werkabonnement is nodig voor de rendementseis van de investeerder (stabiel jaar, zonder exit)
    rest_omzet = stab["omzet"] - W * A["leden_per_werkplek"] * 0.85 * A["arpu"] * 12 * (1 + A["groei_prijs"]) ** 2
    nodig = (stab["kosten"] + last + eigen * A["rendementseis"] - rest_omzet) / (W * A["leden_per_werkplek"] * 0.85 * 12 * (1 + A["groei_prijs"]) ** 2 * (1 - A["platform_pct"]))
    # break-even bezetting (EBITDA dekt de bank), stabiele prijzen
    be = None
    for b10 in range(30, 101):
        bez = b10 / 100
        om = (W * A["leden_per_werkplek"] * bez * A["arpu"] * 12 + A["dagpassen_per_dag"] * A["dagpas"] * A["werkdagen"] * bez
              + kamers * A["vergader_uur_week"] * A["vergader_tarief"] * 48 * bez + A["events_jaar"]
              + (A["gymleden"] * A["gym_prijs"] * 12 * bez if sport_mag else 0) + (A["cafe_pacht_jaar"] if horeca_mag else 0))
        if om * (1 - A["platform_pct"]) - opex_basis >= last:
            be = bez
            break
    return dict(slug=slug, titel=b.pand(slug)["ontwerp"]["titel"], werkplekken=W, capex=round(capex), lening=round(lening), eigen=round(eigen),
                bank_jaar=round(last), opex=round(opex_basis), jaren=rows, irr=round(irr(cfs) * 100, 1), exit=round(exitw),
                cash_yield_stabiel=round(stab["cf"] / eigen * 100, 1), arpu_nodig=round(nodig), arpu_nodig_incl=round(nodig * 1.21),
                breakeven_bezetting=be, sport_mag=sport_mag, horeca_mag=horeca_mag,
                club_fee=k["fee"], club_leden=None)


def main():
    out = [model("rotterdam-metaalhof-40", sport_mag=False, horeca_mag=False),
           model("utrecht-van-heutszstraat-4", sport_mag=True, horeca_mag=True),
           model("den-bosch-eendenkooi-1a", sport_mag=True, horeca_mag=True)]
    json.dump(dict(aannames=AANNAMES, panden=out), open(os.path.join(HERE, "commercieel.json"), "w"), ensure_ascii=False, indent=1)
    for m in out:
        s = m["jaren"][2]
        print(f'{m["titel"][:26]:26} W{m["werkplekken"]} capex {m["capex"]} eigen {m["eigen"]} lening {m["lening"]} | jr3 leden {s["leden"]} omzet {s["omzet"]} kosten {s["kosten"]} '
              f'ebitda {s["ebitda"]} bank {s["bank"]} cf {s["cf"]} dscr {s["dscr"]} | cash yield {m["cash_yield_stabiel"]}% irr {m["irr"]}% | '
              f'arpu nodig {m["arpu_nodig"]} excl ({m["arpu_nodig_incl"]} incl) | break-even bez {m["breakeven_bezetting"]}')
        print("   jaar 1-3 cf:", [x["cf"] for x in m["jaren"][:3]])


if __name__ == "__main__":
    main()
