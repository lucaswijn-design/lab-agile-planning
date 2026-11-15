"""Ronde 7 (15 november 2026): nieuwe kandidaten en de herbeoordeelde panden, sober doorgerekend (capaciteit.schaal(sober=True)).
Per pand het grootste aantal eigenaren (tot 100, half vol, half deeltijd, de helft daarvan als clubleden) dat past,
naast het verzorgingsgebied: kern (4,5 km + een halte), breed (8 km fiets, 2 haltes) en breed met auto. Zie ronde7.md."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from capaciteit import programma, schaal  # noqa: E402
import kandidaten6  # noqa: E402
import kandidaten7  # noqa: E402


def past(m2, hoogte, nmax=100):
    hoog = (hoogte or 0) >= 6.5
    best = None
    for N in range(20, nmax + 5, 5):
        _, nodig, _ = programma(N // 2, N - N // 2, N // 2)
        if nodig <= m2 * 1.02:
            best = (N, 0.0)
        elif hoog and nodig * 0.65 <= m2 * 1.02:
            best = (N, round(1 - m2 / nodig, 2))
    return best


def rij(k, sober=True, nmax=100):
    naam, plaats, url, prijs, m2, h, staat, opm, oud = k
    p = past(m2, h, nmax)
    out = dict(naam=naam, plaats=plaats, url=url, prijs=prijs, m2=m2, hoogte=h, opm=opm, oud=oud, eigenaren=0)
    if not p:
        return out
    N, tv = p
    tot = m2 / (1 - tv) if tv else m2
    r = schaal(N // 2, N - N // 2, N // 2, prijs_m2=prijs / m2, staat=staat, m2=round(tot), tussenvloer=tv, sober=sober)
    return dict(out, eigenaren=N, clubleden=N // 2, tussenvloer=tv, fee_run=r["fee_run"], fee_inleg=r["fee_inleg"], ltv=r["ltv"], capex=r["capex"])


def alles():
    H = {(x["naam"], x["plaats"]): x for x in json.load(open(os.path.join(HERE, "ronde7_herbeoordeling.json")))["locaties"]}
    rows = []
    for k in kandidaten7.K:
        m = kandidaten7.META[k[0]]
        rows.append(dict(rij(k), bron="nieuw", kern=m["leden_kern"], breed=m["leden_breed"], auto=m["leden_breed_auto"],
                         parkeren=m.get("parkeren"), station_km=m.get("station_km"), wijk=m.get("wijk"), oordeel=None))
    for k in kandidaten6.K:
        h = H.get((k[0], k[1]))
        if not h:
            continue
        m = h["metrics"]
        rows.append(dict(rij(k), bron="ronde 6", kern=m["leden_kern"], breed=m["leden_breed"], auto=m["leden_breed_auto"],
                         parkeren=h.get("parkeren"), station_km=m.get("station_km"), wijk=None, oordeel=h["oordeel"], reden=h["reden"]))
    for r in rows:  # leden die het gebied kan leveren (kern telt vol, de brede ring half, zoals in de methode) tegen wat het pand nodig heeft
        r["haalbaar"] = bool(r["eigenaren"]) and r["breed"] >= r["eigenaren"] * 1.2
    return rows


if __name__ == "__main__":
    for r in sorted(alles(), key=lambda r: (not r["haalbaar"], r.get("fee_run") or 9999)):
        print(f'{r["bron"]:7} {r["naam"][:26]:26} {r["plaats"][:12]:12} {r["prijs"]:>9} {r["m2"]:>5} N{r["eigenaren"]:>3} run {r.get("fee_run")} inleg {r.get("fee_inleg")} '
              f'| kern {r["kern"]} breed {r["breed"]} auto {r["auto"]} | {"OK" if r["haalbaar"] else "--"} {r.get("oordeel") or ""}')
