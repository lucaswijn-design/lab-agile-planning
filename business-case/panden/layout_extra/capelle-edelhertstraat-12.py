# Ronde 9 (16 november 2026): Edelhertstraat 12 Capelle aan den IJssel, vrijstaande hal op eigen grond.
LAYOUTS.update({
    "capelle-edelhertstraat-12": dict(
        titel="Edelhertstraat 12, Capelle aan den IJssel", oordeel="kandidaat, beschikbaar volgens oozo (aangeboden sinds 19-01-2026)",
        samenvatting="Vrijstaande hal uit 1974 van 24 x 24 m (BAG 619 m², advertentie 662 m²) op 1.044 m² eigen grond, vrije hoogte 4,7 m, vier lichtstraten. "
                     "Bedrijventerrein 's-Gravenland aan de oostrand van Rotterdam; metro Capelle en station Rotterdam Alexander op fietsafstand. Indeling hal en kantoor niet bekend.",
        koop=dict(totaal=995_000, label="vraagprijs oozo en brochure Parc Makelaars, beschikbaar sinds 19-01-2026, eigen grond"),
        verhuur=[], leden=dict(n_vol=40, n_deel=40, n_club=40), bouwjaar_risico=True, isoleren=True, pv_kwp=35,
        zones=[dict(type="werken", naam="Werkzone", r=(14.5, 0.3, 24.1, 14.0)), dict(type="café", naam="Café", r=(14.5, 14.0, 24.1, 23.9)),
               dict(type="sanitair", naam="Torens", r=(8.5, 0.3, 14.5, 13.0)), dict(type="gym", naam="Gym", r=(0.3, 0.3, 8.5, 13.0)),
               dict(type="bieb", naam="Lounge, spel en bieb", r=(0.3, 13.0, 14.5, 23.9))],
        pui=dict(kant="u1", v0=4.0, v1=18.0, u=24.4),
        buiten=[dict(type="terras", naam="Terras aan de zuidkant", r=(12.0, 24.4, 24.4, 29.2))], bomen_buiten=[(13.0, 27.0), (24.0, 26.0), (-1.6, 20.0), (-1.6, 23.0), (-1.6, 2.0), (-1.6, 9.5)],
        extra_rows=[
            dict(groep="Bouwkundig", post="Glas in de zuidgevel bij het café (hergebruikte stalen ramen, gevelopening, latei)", h=25, e="m2", prijs=750, label="schatting", gen=0.5),
            dict(groep="Bouwkundig", post="Gevelopeningen in de westgevel voor de nieuwe glazen gevel (lateien, constructeur)", h=1, e="post", prijs=8_000, label="schatting", gen=0.3),
            dict(groep="Bouwkundig", post="Glazen deur naar het erf als eigen ingang van de gym", h=1, e="post", prijs=4_000, label="schatting", gen=0.5),
        ],
        opex_extra=[],
    ),
})
