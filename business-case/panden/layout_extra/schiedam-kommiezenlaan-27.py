# Ronde 9 (16 november 2026): Kommiezenlaan 27 Schiedam, unit 27 uit een complex van 1950, met een tuinkamer erachter en een gympaviljoen op het eigen erf.
LAYOUTS.update({
    "schiedam-kommiezenlaan-27": dict(
        titel="Kommiezenlaan 27, Schiedam", oordeel="kandidaat (klein pand, groot erf), beschikbaar volgens oozo, aangeboden sinds 09-10-2026",
        samenvatting="Westelijke beuk (9,1 x 25,8 m, circa 235 m² vloer, vrije hoogte circa 4 m) van een bedrijfscomplex uit 1950 met zeven adressen, nieuw dak en label A++, "
                     "met een eigen erf van circa 700 m² (perceel circa 940 m²). Op 300 m van station Schiedam Centrum. De beuk is te klein voor de hele club: "
                     "een nieuwe tuinkamer van 91 m² erachter en een gympaviljoen van 70 m² op het erf maken het af.",
        koop=dict(totaal=785_000, label="vraagprijs funda in business (zoekresultaat, ronde 9); oozo noemt € 775.000, beschikbaar sinds 09-10-2026"),
        verhuur=[], leden=dict(n_vol=33, n_deel=33, n_club=30), bouwjaar_risico=False, isoleren=False, pv_kwp=20,
        zones=[dict(type="café", naam="Café", r=(18.3, 0.2, 25.6, 8.9)), dict(type="werken", naam="Werkzone", r=(4.0, 3.4, 18.3, 8.9)),
               dict(type="vergader", naam="Kamers", r=(5.6, 0.2, 18.3, 3.4)), dict(type="sanitair", naam="Wastoren en lockers", r=(0.2, 0.2, 4.0, 8.9)),
               dict(type="bieb", naam="Tuinkamer (nieuw)", r=(-9.8, 0.2, 0.0, 8.9)),
               dict(type="gym", naam="Gympaviljoen (nieuw)", r=(-13.5, 19.2, -4.7, 27.2))],
        pui=dict(kant="v1", u0=4.2, u1=18.0, v=9.1),
        buiten=[dict(type="terras", naam="Terras langs de zijgevel", r=(9.5, 9.3, 19.0, 13.6)),
                dict(type="tuin", naam="Tuin", r=(-13.8, 9.3, -2.6, 19.0))],
        bomen_buiten=[(6.0, 12.0), (-12.4, 2.0), (-12.4, 13.0), (-3.0, 16.5), (1.5, 16.0), (-1.5, 24.0)],
        extra_rows=[
            dict(groep="Bouwkundig", post="Tuinkamer 10 x 9 m achter de unit: fundering, hergebruikt stalen frame, geïsoleerde gevels met oude stalen ramen, betonvloer, sedumdak (sober)",
                 h=91, e="m2", prijs=1_300, label="schatting", gen=0.5),
            dict(groep="Bouwkundig", post="Gympaviljoen 8,8 x 8 m op het erf: fundering, hergebruikt stalen portaalframe, sandwichpanelen, betonvloer, sedumdak (sober)",
                 h=70, e="m2", prijs=1_250, label="schatting", gen=0.5),
            dict(groep="Bouwkundig", post="Doorbraak van 3 m in de achtergevel naar de tuinkamer (stalen latei, constructeur)", h=1, e="post", prijs=9_000, label="schatting", gen=0.3),
            dict(groep="Bouwkundig", post="Leidingen, riolering en stroom naar het paviljoen (sleuf over het erf)", h=1, e="post", prijs=9_000, label="schatting", gen=0.3),
            dict(groep="Bouwkundig", post="Glazen voorgevel en glas in de tuinkamer (hergebruikte stalen ramen, deuren)", h=50, e="m2", prijs=650, label="schatting", gen=0.5),
            dict(groep="Bouwkundig", post="Vergunning aanbouw en paviljoen (omgevingsplan, bouwen op het erf): leges en tekeningen", h=1, e="post", prijs=8_000, label="schatting", gen=0.0),
            dict(groep="Buiten", post="Pergola met druif voor de raambar op het zuiden", h=1, e="post", prijs=2_500, label="schatting", gen=0.3),
        ],
        opex_extra=[("Erfpacht of beheer complex (aanname, navragen bij gemeente Schiedam en verkoper)", 3_000)],
    ),
})
