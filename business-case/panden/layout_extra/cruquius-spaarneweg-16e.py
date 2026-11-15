# Ronde 9 (15 november 2026): Spaarneweg 16E, Cruquius. Zie ronde9/uitgewerkt_nh.md.
LAYOUTS.update({
    "cruquius-spaarneweg-16e": dict(
        titel="Spaarneweg 16E, Cruquius", oordeel="kandidaat, status onzeker (brochure zonder datum, oozo noemt huur): eerst nabellen",
        samenvatting="Vrijstaande bedrijfsruimte uit 1985 op een hoek aan de Spaarneweg, BAG 439 m² op één laag (hal 330 + kantoor 85 m²), circa 4 m vrij hoog, eigen erf met parkeren. "
                     "Bedrijventerrein Cruquius-Zuid tussen Haarlem en Hoofddorp, 3,4 km van station Heemstede-Aerdenhout. Geen woningen in het pand; het buurpand op 3,7 m heeft twee bedrijfswoningen.",
        koop=dict(totaal=695_000, label="vraagprijs brochure funda in business (zoekmachine), status onzeker"),
        verhuur=[], leden=dict(n_vol=21, n_deel=21, n_club=30), bouwjaar_risico=True, isoleren=True, pv_kwp=30,
        zones=[dict(type="café", naam="Café, keuken en lounge", r=(10.0, 0.2, 17.0, 17.2)), dict(type="werken", naam="Werkzone", r=(1.5, 0.2, 10.0, 9.0)),
               dict(type="vergader", naam="Stille kamers", r=(1.5, 9.0, 10.0, 17.2)), dict(type="sanitair", naam="Wastoren en lockers", r=(17.0, 0.2, 21.5, 17.2)),
               dict(type="gym", naam="Gym", r=(21.5, 0.2, 26.3, 17.2))],
        pui=dict(kant="v0", u0=1.5, u1=16.8, v=0.0),
        buiten=[dict(type="terras", naam="Terras aan de straat", r=(10.0, -3.0, 16.8, -0.2))], bomen_buiten=[(34.0, 18.0), (34.0, -1.8)],
        extra_rows=[dict(groep="Bouwkundig", post="Glazen pui, aluminium HR+++ (gym aan het erf, 5,4 x 3 m)", h=16, e="m2", prijs=1_000, label="bron", gen=0.6),
                    dict(groep="Bouwkundig", post="Kantoorplafond, kantoorwanden en oude installaties slopen en afvoeren", h=85, e="m2", prijs=15, label="schatting", gen=0.0)],
        opex_extra=[],
    ),
})
