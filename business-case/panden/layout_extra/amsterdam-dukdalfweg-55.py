# Ronde 9 (15 november 2026): Dukdalfweg 55, Amsterdam Westpoort. Zie ronde9/uitgewerkt_nh.md.
LAYOUTS.update({
    "amsterdam-dukdalfweg-55": dict(
        titel="Dukdalfweg 55, Amsterdam Westpoort", oordeel="kandidaat, status onzeker: eerst nabellen; ligt in havengebied Westhaven (erfpacht Havenbedrijf, verkoop met toestemming), wijkschatting waarschijnlijk te hoog",
        samenvatting="Hoekunit uit 2020 in bedrijfsverzamelgebouw Zaansepoort (8 units, geen woningen), hal 375 + kantoor 225 m² (BAG 621 m²), circa 9 m hoog, overheaddeur, "
                     "6 eigen + 6 gedeelde parkeerplaatsen. Grond in erfpacht van Havenbedrijf Amsterdam: verkoop en gebruik vragen toestemming. Pont naar Zaandam, 2,4 km van station Zaandam.",
        koop=dict(totaal=895_000, label="vraagprijs brochure GA Makelaars (zoekmachine), status onzeker"),
        verhuur=[], leden=dict(n_vol=37, n_deel=37, n_club=30), bouwjaar_risico=False, isoleren=False, pv_kwp=30, verdieping_m2=225,
        zones=[dict(type="café", naam="Café", r=(0.2, 0.2, 9.0, 15.4)), dict(type="werken", naam="Werkzone (verdieping)", r=(0.2, 0.2, 7.2, 15.4), niveau=1),
               dict(type="vergader", naam="Stille kamers (entresol)", r=(7.2, 0.2, 14.4, 15.4), niveau=1), dict(type="sanitair", naam="Wastoren en lockers", r=(9.0, 0.2, 14.4, 15.4)),
               dict(type="bieb", naam="Lounge", r=(14.4, 0.2, 19.5, 15.4)), dict(type="gym", naam="Gym", r=(19.5, 0.2, 26.3, 15.4))],
        pui=dict(kant="v1", u0=7.2, u1=14.2, v=15.6),
        buiten=[dict(type="terras", naam="Terras aan de oostgevel", r=(1.0, 15.8, 7.0, 19.0))], bomen_buiten=[(-12.0, 18.0), (-12.0, 2.0)],
        extra_rows=[dict(groep="Bouwkundig", post="Zijdeur in de oostgevel voor de gym (sandwichpaneel zagen, kozijn, toegangslezer)", h=1, e="post", prijs=4_500, label="schatting", gen=0.3),
                    dict(groep="Bouwkundig", post="Akoestiek hal: houtwolplaten op de wanden en baffles onder het dak (9 m hoog)", h=160, e="m2", prijs=22, label="schatting", gen=0.2)],
        opex_extra=[("Erfpachtcanon Havenbedrijf Amsterdam (aanname, navragen; circa € 20 per m² grond per jaar)", 10_000),
                    ("Bijdrage vereniging van eigenaren bedrijfsverzamelgebouw (aanname, navragen)", 4_000)],
    ),
})
