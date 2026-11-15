# Ronde 9 (15 november 2026): A. Hofmanweg 2F, Haarlem Waarderpolder. Zie ronde9/uitgewerkt_nh.md.
LAYOUTS.update({
    "haarlem-hofmanweg-2f": dict(
        titel="A. Hofmanweg 2F, Haarlem", oordeel="kandidaat, te koop en te huur volgens bedrijfspand.com (bijgewerkt 13-11-2026)",
        samenvatting="Kantoorpand uit 2000 van 21 x 15 m op twee lagen (266 m² bg + 244 m² verdieping, BAG 590 m²), label A, turn-key, centraal trappenhuis met daklicht, "
                     "8 eigen parkeerplaatsen. Aan drie kanten aangebouwd tegen bedrijfspanden: alleen de zuidgevel aan het parkeerterrein is vrij. Lage plafonds (circa 2,9 m zonder systeemplafond). "
                     "Waarderpolder, 2 km van station Haarlem Spaarnwoude.",
        koop=dict(totaal=975_000, label="vraagprijs bedrijfspand.com (FRIS Bedrijfsmakelaars), te koop op 13-11-2026"),
        verhuur=[], leden=dict(n_vol=26, n_deel=26, n_club=30), bouwjaar_risico=False, isoleren=False, pv_kwp=20, verdieping_m2=244,
        zones=[dict(type="café", naam="Café en keuken", r=(6.4, 7.8, 20.8, 14.8)), dict(type="werken", naam="Werkzone (verdieping)", r=(10.0, 7.8, 20.8, 14.8), niveau=1),
               dict(type="vergader", naam="Stille kamers (verdieping)", r=(0.2, 0.2, 10.0, 14.8), niveau=1), dict(type="bieb", naam="Lounge en bieb (verdieping)", r=(10.0, 0.2, 20.8, 7.8), niveau=1),
               dict(type="sanitair", naam="Wastoren, atrium en gang", r=(0.2, 0.2, 10.0, 7.8)), dict(type="techniek", naam="Techniek en opslag", r=(0.2, 7.8, 6.4, 14.8)),
               dict(type="gym", naam="Gym", r=(10.0, 0.2, 20.8, 7.8))],
        pui=dict(kant="u1", v0=12.8, v1=14.8, u=21.0),
        buiten=[dict(type="terras", naam="Terras op het zuiden", r=(21.2, 7.8, 25.0, 14.8))], bomen_buiten=[(35.0, 14.0)],
        extra_rows=[dict(groep="Bouwkundig", post="Systeemplafonds, kantoorwanden en vloerbedekking verwijderen (twee lagen)", h=510, e="m2", prijs=12, label="schatting", gen=0.0),
                    dict(groep="Sanitair", post="Afvoeren wastoren en douchetoren in de bestaande kantoorvloer (sleuven, vuilwaterpomp)", h=1, e="post", prijs=6_000, label="schatting", gen=0.3),
                    dict(groep="Bouwkundig", post="Glazen pui, aluminium HR+++ (eigen gymdeur met zijlicht in de bestaande zuidgevel)", h=8, e="m2", prijs=1_000, label="bron", gen=0.6)],
        opex_extra=[("Parkmanagement Waarderpolder (aanname, navragen)", 600)],
    ),
})
