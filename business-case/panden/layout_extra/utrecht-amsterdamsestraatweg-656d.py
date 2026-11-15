# Ronde 9 (15 november 2026): Amsterdamsestraatweg 656D, Utrecht Zuilen, vervangt Roelantdreef 24 (woningen in hetzelfde winkelcentrumcomplex). Zie ronde9/uitgewerkt_nh.md.
LAYOUTS.update({
    "utrecht-amsterdamsestraatweg-656d": dict(
        titel="Amsterdamsestraatweg 656D, Utrecht", oordeel="vervanger voor Roelantdreef 24; status onzeker (oozo beschikbaar, online sinds maart 2025): eerst nabellen",
        samenvatting="Bedrijfsruimte uit 2003 in Zuilen, 1.089 m² op twee lagen (hal 909 + kantoor 180 m²), label A, in een pand met één andere eigenaar (Martin-ovenweg 19, industrie). "
                     "Geen woningen in het pand. Lange zuidoostgevel aan een binnenterrein, straatkop aan de Amsterdamsestraatweg, 1,3 km van station Utrecht Zuilen.",
        koop=dict(totaal=925_000, label="vraagprijs oozo (ronde 7, beschikbaar op 15-11-2026), status onzeker"),
        verhuur=[], leden=dict(n_vol=40, n_deel=40, n_club=30), bouwjaar_risico=False, isoleren=False, pv_kwp=40, verdieping_m2=91,
        zones=[dict(type="bieb", naam="Entree en lockers", r=(1.2, 0.2, 5.2, 22.8)), dict(type="café", naam="Café en tafeltennis", r=(5.2, 0.2, 17.5, 22.8)),
               dict(type="werken", naam="Werkzone", r=(17.5, 9.0, 31.5, 22.8)), dict(type="vergader", naam="Vergaderen", r=(17.5, 0.2, 31.5, 9.0)),
               dict(type="sanitair", naam="Wastoren, toiletten en techniek", r=(31.5, 0.2, 36.3, 22.8)), dict(type="gym", naam="Gym", r=(36.3, 8.0, 45.8, 22.8)),
               dict(type="studio", naam="Studio", r=(36.3, 0.2, 45.8, 8.0)), dict(type="bieb", naam="Bieb en stille kamers (verdieping)", r=(1.2, 0.2, 5.2, 22.8), niveau=1)],
        pui=dict(kant="v1", u0=5.5, u1=31.0, v=23.0),
        buiten=[dict(type="terras", naam="Terras op het binnenterrein", r=(6.0, 23.2, 17.0, 27.5))], bomen_buiten=[(-4.0, 4.0), (18.5, 28.5)],
        extra_rows=[dict(groep="Bouwkundig", post="Lichtkoepels nieuw boven werkzone, café en gym (dakopening, opstand, koepel)", h=8, e="st", prijs=2_500, label="schatting", gen=0.5),
                    dict(groep="Bouwkundig", post="Houten sportvloer studio (hergebruikt, geschuurd en gelakt)", h=74, e="m2", prijs=45, label="schatting", gen=0.3),
                    dict(groep="Bouwkundig", post="Splitsing en afspraken met de eigenaar van Martin-ovenweg 19 (notaris, splitsingstekening, scheidingswand controleren)", h=1, e="post", prijs=6_000, label="schatting", gen=0.0)],
        opex_extra=[("Bijdrage vereniging van eigenaren (twee eigenaren, aanname, navragen)", 3_000)],
    ),
})
