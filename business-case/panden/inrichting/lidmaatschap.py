"""
Soorten eigenaren en plekbenutting (16 november 2026).

Vier soorten eigenaar-lid, plus clubleden (abonnees, geen eigenaar):
  vast       eigen bureau met naam, 7 dagen, vaste locker
  flex       onbeperkt flexplek op werkdagen, zonder vaste plek
  flex 3     3 werkdagen per week flexplek (dagtegoed, zie systeem)
  flex 2     2 werkdagen per week flexplek
Avonden en weekenden zijn voor alle eigenaren vrij: dan is er toch plek.

Plekbehoefte per werkdag: elk lid is er met kans p = dagen/5 x 0,85 (vakantie, ziek, elders) x dagfactor; vaste leden 0,70 x dagfactor.
Van wie die dag komt, zit 85% tegelijk op het drukste uur. Flexplekken worden gedimensioneerd op het 95e percentiel (normale benadering
van een som van Bernoulli-variabelen): op 19 van de 20 drukste dagen is er een flexplek, op de overige dag zit je aan de grote tafel,
de raambar of in het café. Vaste bureaus die om 10:00 leeg zijn, gaan die dag naar de flexpool.
Labels: [aanname] tenzij vermeld. Draaien: python3 inrichting/lidmaatschap.py
"""
from __future__ import annotations

import math

DAGFACTOR = {"ma": 0.90, "di": 1.15, "wo": 1.10, "do": 1.15, "vr": 0.70}   # [aanname] dinsdag tot donderdag drukst, vrijdag rustig
AANWEZIG = 0.85
TEGELIJK = 0.85
Z95 = 1.645

SOORTEN = {
    # naam: (werkdagen per week of None voor vast, gewicht in de maandbijdrage, inleg)
    "vast": (None, 1.25, 18_000),
    "flex": (5, 1.00, 15_000),
    "flex 3": (3, 0.80, 11_000),
    "flex 2": (2, 0.60, 8_000),
}


def kans(soort, dag):
    d = SOORTEN[soort][0]
    if d is None or d >= 5:  # vast en flex onbeperkt: gemiddeld 70% van de werkdagen aanwezig, zoals het volle lid in capaciteit.py
        return min(1.0, 0.70 * DAGFACTOR[dag])
    return min(1.0, d / 5 * AANWEZIG * DAGFACTOR[dag])


def behoefte(mix, dag="di"):
    """mix: dict soort -> aantal leden. Geeft vaste bureaus, flexplekken op het 95e percentiel, gemiddeld lege vaste bureaus."""
    vast = mix.get("vast", 0)
    mu = var = 0.0
    for s, n in mix.items():
        if s == "vast":
            continue
        p = kans(s, dag) * TEGELIJK
        mu += n * p
        var += n * p * (1 - p)
    p_vast = kans("vast", dag) * TEGELIJK
    leeg_vast = vast * (1 - p_vast)
    flex95 = math.ceil(mu + Z95 * math.sqrt(var))
    return dict(vaste_bureaus=vast, flex_gemiddeld=round(mu, 1), flex_p95=flex95, leeg_vast=round(leeg_vast, 1),
                totaal_p95=vast + flex95, totaal_met_vrijgave=vast + max(0, flex95 - math.floor(leeg_vast * 0.6)))


def oude_regeling(V, D, dag="di"):
    """Huidige regeling: vol (gemiddeld 70% aanwezig) en deeltijd (3 dagen), allemaal flex; ter vergelijking."""
    mu = (V * 0.70 * DAGFACTOR[dag] + D * 3 / 5 * AANWEZIG * DAGFACTOR[dag]) * TEGELIJK
    return math.ceil(mu)


def bijdragen(mix, totaal_vol_equivalent_fee, vol_eenheden):
    """Verdeel dezelfde totale maandopbrengst over de soorten naar gewicht. totaal = fee_vol x (V + D x 0,711) uit pand_case."""
    totaal = totaal_vol_equivalent_fee * vol_eenheden
    eenheden = sum(n * SOORTEN[s][1] for s, n in mix.items())
    unit = totaal / eenheden
    return {s: round(unit * SOORTEN[s][1]) for s in mix}, sum(n * SOORTEN[s][2] for s, n in mix.items())


if __name__ == "__main__":
    mix = {"vast": 15, "flex": 25, "flex 3": 30, "flex 2": 20}   # 90 eigenaren, voorbeeld Galvanistraat
    for dag in DAGFACTOR:
        print(dag, behoefte(mix, dag))
    print("oude regeling 45 vol + 45 deeltijd, dinsdag, gemiddeld tegelijk:", oude_regeling(45, 45))
    print(bijdragen(mix, 227, 45 + 45 * 320 / 450))


def behoefte_teams(mix, teams, dag="di"):
    """Zoals behoefte(), maar met teams: lijst van (aantal personen, soort). Teamleden komen samen of niet (samen = gecorreleerd),
    dus de spreiding per team is n^2 p (1 - p) in plaats van n p (1 - p). Teamleden zitten in mix niet dubbel."""
    b = behoefte(mix, dag)
    mu = b["flex_gemiddeld"]; var = 0.0
    for s, n in mix.items():
        if s != "vast":
            p = kans(s, dag) * TEGELIJK; var += n * p * (1 - p)
    for n, s in teams:
        p = kans(s, dag) * TEGELIJK
        mu += n * p; var += n * n * p * (1 - p)
    flex95 = math.ceil(mu + Z95 * math.sqrt(var))
    return dict(b, flex_gemiddeld=round(mu, 1), flex_p95=flex95, totaal_met_vrijgave=b["vaste_bureaus"] + max(0, flex95 - math.floor(b["leeg_vast"] * 0.6)))


def vergaderuren(leden_uren, teams, uren_per_team=4.0):
    """Vergaderuren per week: leden plus teams (een klein team vergadert circa 4 uur per week extra [aanname])."""
    return leden_uren + len(teams) * uren_per_team
