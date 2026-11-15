# Ronde 9 (16 november 2026): Kampenringweg 7 Gouda, vervangt Fokkerstraat 475 Schiedam (in 2024 gemelde garage op dat adres, advertentie oud, niet meer in actueel aanbod).
LAYOUTS.update({
    "gouda-kampenringweg-7": dict(
        titel="Kampenringweg 7, Gouda", oordeel="kandidaat (vervanger), te koop volgens bedrijfspand.com, bijgewerkt 13-11-2026",
        samenvatting="Middelste van drie bedrijfsunits uit 1991 op de Goudse Poort, BVO 637 m² (begane grond 342 met werkplaats 19 x 16 m, verdieping 295 met vier kantoren en een houten entresol). "
                     "Perceel 570 m² met 5 eigen parkeerplaatsen voor en een strook aan de vaart achter. Label A+, 18 zonnepanelen. Servicekosten € 375 per maand. Bestemming bedrijf tot categorie 3.2.",
        koop=dict(totaal=865_000, label="vraagprijs bedrijfspand.com 121602, te koop, bijgewerkt 13-11-2026"),
        verhuur=[], leden=dict(n_vol=33, n_deel=33, n_club=45), bouwjaar_risico=True, isoleren=False, pv_kwp=20, verdieping_m2=200,
        zones=[dict(type="café", naam="Café in de vide", r=(1.2, 0.3, 10.5, 9.8)), dict(type="bieb", naam="Entree", r=(0.3, 9.8, 4.4, 15.8)),
               dict(type="vergader", naam="Stil hoekje", r=(4.4, 9.8, 10.5, 15.8)), dict(type="sanitair", naam="Torens", r=(10.6, 0.3, 15.2, 9.9)),
               dict(type="gym", naam="Gym", r=(15.2, 0.3, 21.3, 15.8)), dict(type="werken", naam="Werkzone verdieping", r=(10.5, 0.3, 15.2, 15.8), niveau=1)],
        pui=dict(kant="u0", v0=0.4, v1=6.3, u=1.1),
        buiten=[dict(type="terras", naam="Terras aan de vaart", r=(21.8, 1.0, 26.5, 15.0))], bomen_buiten=[(25.2, 2.0), (25.6, 14.6), (-5.2, 1.0), (-5.2, 15.0)],
        extra_rows=[
            dict(groep="Bouwkundig", post="Houten entresol boven de gym verwijderen (circa 95 m², hout op staal, deels hergebruikt in de inrichting)", h=95, e="m2", prijs=40, label="schatting", gen=0.0),
            dict(groep="Bouwkundig", post="Nieuwe ramen en deur in de achtergevel naar de vaart (hergebruikte stalen ramen, gevelopening, latei)", h=24, e="m2", prijs=750, label="schatting", gen=0.5),
            dict(groep="Bouwkundig", post="Vijf lichtkoepels in het platte dak", h=5, e="st", prijs=3_000, label="schatting", gen=0.5),
            dict(groep="Bouwkundig", post="Autobrug, wasplaats en olieafscheider verwijderen, vloer herstellen (bodemonderzoek apart)", h=1, e="post", prijs=6_000, label="schatting", gen=0.0),
            dict(groep="Bouwkundig", post="Verkennend bodemonderzoek (autobedrijf in gebruik)", h=1, e="post", prijs=3_500, label="schatting", gen=0.0),
        ],
        opex_extra=[("Servicekosten complex (advertentie: € 375 per maand)", 4_500)],
    ),
})
