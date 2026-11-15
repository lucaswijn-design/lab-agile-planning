# Ronde 9 (16 november 2026): Zilverstraat 56 Den Haag, uit ronde 7 (kandidaten7.py), uitgewerkt als ontwerp.
LAYOUTS.update({
    "den-haag-zilverstraat-56": dict(
        titel="Zilverstraat 56, Den Haag", oordeel="kandidaat, te koop volgens bedrijfspand.com (bijgewerkt 13-11-2026)",
        samenvatting="Bedrijfsruimte uit 1993 in een bedrijfsverzamelgebouw (16 units, VvE niet actief), BVO 872 m²: begane grond 499 + betonnen entresol 373 m². "
                     "Vrije hoogte 6,1 m in de vide en 3,2 m onder de entresol. Erfpacht eeuwigdurend afgekocht, 6 eigen parkeerplaatsen, dak vernieuwd in 2023. Tram 6 op 5 minuten. De zes nieuwe lichtkoepels zitten in de post Lichtstraten (isoleren).",
        koop=dict(totaal=1_299_500, label="vraagprijs bedrijfspand.com 112848, te koop, bijgewerkt 13-11-2026"),
        verhuur=[], leden=dict(n_vol=43, n_deel=43, n_club=40), bouwjaar_risico=False, isoleren=True, pv_kwp=30, verdieping_m2=373,
        zones=[dict(type="gym", naam="Gym in de vide", r=(0.3, 0.3, 8.3, 17.7)), dict(type="café", naam="Entreehal", r=(8.3, 0.3, 12.5, 12.0)),
               dict(type="sanitair", naam="Wastoren", r=(8.3, 12.0, 14.1, 17.7)), dict(type="vergader", naam="Vergaderen", r=(12.5, 0.3, 21.3, 3.4)),
               dict(type="café", naam="Lounge, spel en keuken", r=(14.1, 3.4, 21.3, 17.7)), dict(type="café", naam="Café", r=(21.3, 0.3, 28.2, 17.7)),
               dict(type="werken", naam="Werkzone verdieping", r=(21.6, 0.3, 28.2, 17.7), niveau=1)],
        pui=dict(kant="v0", u0=0.4, u1=4.4, v=0.0),
        buiten=[dict(type="terras", naam="Bankje en plantenbakken aan het hof", r=(0.0, -2.0, 12.0, -0.2))], bomen_buiten=[],
        extra_rows=[
            dict(groep="Bouwkundig", post="Overheaddeur vervangen door glazen pui met deur op toegangspas (eigen ingang gym)", h=1, e="post", prijs=6_000, label="schatting", gen=0.5),
            dict(groep="Bouwkundig", post="Gymvloer op de begane grond: zwevende dekvloer onder de racks tegen contactgeluid naar het verzamelgebouw", h=40, e="m2", prijs=60, label="schatting", gen=0.3),
        ],
        opex_extra=[("Bijdrage verzamelgebouw (VvE niet actief; reservering gezamenlijk onderhoud, aanname)", 2_500)],
    ),
})
