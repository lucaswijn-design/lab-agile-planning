# Ronde 9 (15 november 2026): Laan van Europa 360, Dordrecht. Zie ronde9/uitgewerkt_nh.md.
LAYOUTS.update({
    "dordrecht-laan-van-europa-360": dict(
        titel="Laan van Europa 360, Dordrecht", oordeel="kandidaat, te koop volgens bedrijfspand.com (bijgewerkt 13-11-2026); verzorgingsgebied dun",
        samenvatting="Nieuwe hoekunit uit 2023 in een bedrijfsverzamelgebouw van 10 units op Businesspark Amstelwijck, 453 m² op twee lagen (bg 52 kantoor + 180 multifunctioneel, "
                     "verdieping 95 + 126), 3,73 m vrij, label A+++, geen gas, 5 eigen parkeerplaatsen, 325 m² eigen grond plus aandelen in mandelige weg, groen en parkeren. "
                     "Bestemming kantoor en bedrijf categorie 1 tot 3, minimaal 30% kantoor. Geen woningen in het complex.",
        koop=dict(totaal=795_000, label="vraagprijs bedrijfspand.com (Van Vliet Bedrijfsmakelaars), te koop op 13-11-2026"),
        verhuur=[], leden=dict(n_vol=24, n_deel=24, n_club=30), bouwjaar_risico=False, isoleren=False, pv_kwp=15, verdieping_m2=221,
        zones=[dict(type="café", naam="Café", r=(0.3, 0.2, 11.0, 8.9)), dict(type="werken", naam="Werkzone (verdieping)", r=(0.3, 0.2, 10.6, 8.9), niveau=1),
               dict(type="vergader", naam="Stille kamers (verdieping)", r=(10.6, 0.2, 16.5, 8.9), niveau=1), dict(type="bieb", naam="Lounge en vergaderen (verdieping)", r=(16.5, 0.2, 27.8, 8.9), niveau=1),
               dict(type="sanitair", naam="Wastoren en gang", r=(11.0, 0.2, 16.5, 8.9)), dict(type="gym", naam="Gym", r=(16.5, 0.2, 27.8, 8.9))],
        pui=dict(kant="u0", v0=0.0, v1=4.8, u=0.0),
        buiten=[dict(type="terras", naam="Terras voor de zijgevel", r=(1.0, -3.0, 9.0, -0.2))], bomen_buiten=[(-4.0, -9.0)],
        extra_rows=[dict(groep="Installaties", post="Verwarming en koeling multifunctionele ruimten (nu onverwarmd): extra binnenunits", h=4, e="st", prijs=1_500, label="schatting", gen=0.5)],
        opex_extra=[("Bijdrage mandelige weg, groen en parkeerplaatsen bedrijfsverzamelgebouw (aanname, navragen)", 2_500)],
    ),
})
