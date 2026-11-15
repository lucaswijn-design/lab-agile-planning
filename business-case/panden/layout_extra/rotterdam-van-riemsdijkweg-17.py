# Ronde 9 (16 november 2026): Van Riemsdijkweg 17 Rotterdam Waalhaven.
LAYOUTS.update({
    "rotterdam-van-riemsdijkweg-17": dict(
        titel="Van Riemsdijkweg 17, Rotterdam Waalhaven", oordeel="kandidaat, beschikbaar volgens oozo (aangeboden sinds 16-10-2026); zoekresultaat noemde ook 'onder bod'",
        samenvatting="Bedrijfspand uit 1957 van 40 x 15 m in een rij in de Waalhaven: showroom 159 + hal 404 m² (5,2 m vrij, lichtstraat) + kantoor 154 m² op de verdieping, label A+. "
                     "Erfpacht met een canon van € 8.666 per jaar, perceel 690 m² met een strook van 6 m aan de straat. Ver van treinstations (8 km), wel bus en auto.",
        koop=dict(totaal=895_000, label="vraagprijs oozo en funda in business (zoekresultaat), beschikbaar sinds 16-10-2026, erfpacht"),
        verhuur=[], leden=dict(n_vol=42, n_deel=42, n_club=40), bouwjaar_risico=True, isoleren=False, pv_kwp=30, verdieping_m2=150,
        zones=[dict(type="café", naam="Café", r=(0.3, 0.3, 10.5, 14.7)), dict(type="werken", naam="Werkzone", r=(10.5, 3.4, 25.0, 12.3)),
               dict(type="vergader", naam="Kamers", r=(10.5, 0.3, 25.0, 3.4)), dict(type="bieb", naam="Lockers en focus", r=(10.5, 12.3, 25.0, 14.7)),
               dict(type="sanitair", naam="Torens", r=(25.0, 0.3, 31.0, 14.7)), dict(type="gym", naam="Gym", r=(31.0, 0.3, 39.7, 14.7))],
        pui=dict(kant="u1", v0=2.0, v1=13.0, u=40.0),
        buiten=[dict(type="terras", naam="Terras aan de straat", r=(-5.6, 0.5, -0.3, 9.0))], bomen_buiten=[(-4.6, 1.0), (-4.6, 8.6)],
        extra_rows=[
            dict(groep="Bouwkundig", post="Doorbraak tussen showroom en hal (stalen latei, constructeur)", h=1, e="post", prijs=9_000, label="schatting", gen=0.3),
            dict(groep="Bouwkundig", post="Gevelopeningen in de westgevel voor de nieuwe ramen (latei, metselwerk)", h=1, e="post", prijs=6_000, label="schatting", gen=0.3),
        ],
        opex_extra=[("Erfpachtcanon (advertentie, € 8.666 per jaar)", 8_666)],
    ),
})
