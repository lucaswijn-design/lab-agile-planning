"""Ronde 6 (14 november 2026): kandidaten in drie grootteklassen, snel doorgerekend met capaciteit.schaal().
Per pand: hoeveel eigenaren (half vol, half deeltijd, plus de helft aan clubleden) passen er, en wat kost dat."""
from capaciteit import programma, schaal

# naam, plaats, url, prijs, m2, hoogte (m, None = onbekend), staat, opmerking, oud (lang aangeboden)
K = [
    ("Hoge Larenseweg 202A", "Hilversum", "https://www.bedrijfspand.com/bedrijfspanden/bedrijfsruimte/hoge-larenseweg-202-a-hilversum/123486/", 425_000, 334, 4.0, "opknappen", "hal uit 1910, bestemming bedrijf", False),
    ("Langendijkstraat 9-ZW", "Haarlem", "https://www.oozo.nl/bedrijfspanden/haarlem/zijlwegkwartier/hasselaersbuurt/52951/bedrijfsruimte-langendijkstraat-9-zw-haarlem", 549_000, 407, None, "opknappen", "1895, woonwijk", False),
    ("Boschstraat 96-BIS", "Breda", "https://www.oozo.nl/bedrijfspanden/breda/breda-centrum/valkenberg/81096/bedrijfsruimte-boschstraat-96-bis-breda", 450_000, 379, None, "opknappen", "1950, centrum bij station", False),
    ("Zevenend 26", "Laren", "https://www.oozo.nl/bedrijfspanden/laren/laren/laren-centrum/41916/bedrijfsruimte-zevenend-26-laren-nh", 475_000, 315, None, "opknappen", "1924, centrum", True),
    ("Noordhaven 46", "Zevenbergen", "https://www.bedrijfspand.com/bedrijfspanden/bedrijfsruimte/noordhaven-46-zevenbergen/121810/", 489_500, 442, None, "opknappen", "rijksmonument, 4 lagen, dakterras", False),
    ("Stationsstraat 2", "Zevenbergen", "https://www.oozo.nl/bedrijfspanden/moerdijk/zevenbergen/centrum/58772/maatschappelijk-vastgoed-stationsstraat-2-zevenbergen", 500_000, 385, None, "opknappen", "1910, maatschappelijk", True),
    ("Plein 1", "Dordrecht", "https://www.oozo.nl/bedrijfspanden/dordrecht/staart/plein-1940-1945-en-omgeving/41665/maatschappelijk-vastgoed-plein-1-dordrecht", 475_000, 364, None, "opknappen", "1948, maatschappelijk, buitenruimte", True),
    ("Concordiastraat 29", "Alphen a/d Rijn", "https://www.oozo.nl/bedrijfspanden/alphen-aan-den-rijn/lage-zijde/van-boetzelaerstraat/40183/bedrijfsruimte-concordiastraat-29-alphen-aan-den-rijn", 285_000, 279, None, "opknappen", "1920, centrum", True),
    ("Industrieweg 99B", "Rotterdam", "https://www.bedrijfspand.com/bedrijfspanden/bedrijfsruimte/industrieweg-99-b-rotterdam/122516/", 495_000, 306, 6.0, "opknappen", "hal met lichtstraat en entresol, bedrijventerrein", False),
    ("Ring 15", "Pernis", "https://www.oozo.nl/bedrijfspanden/rotterdam/pernis/pernis/77099/maatschappelijk-vastgoed-ring-15-pernis-rotterdam", 590_000, 551, None, "opknappen", "1852, maatschappelijk, label G", False),
    ("Nijverheidstraat 9", "Katwijk", "https://www.bedrijfspand.com/bedrijfspanden/bedrijfsruimte/nijverheidstraat-9-katwijk/126346/", 699_000, 610, 2.8, "opknappen", "oude bakkerij, 2 lagen, laag plafond", False),
    ("Sweelincksingel 3-7", "Schiedam", "https://www.oozo.nl/bedrijfspanden/schiedam/groenoord-en-kethel/groenoord-zuid/59572/maatschappelijk-vastgoed-sweelincksingel-3-7-schiedam", 460_000, 695, None, "opknappen", "monument 1905, inschrijving gemeente", False),
    ("Hoogmadeseweg 62", "Leiderdorp", "https://www.oozo.nl/bedrijfspanden/leiderdorp/wijk-00/kerkwijk/7085/maatschappelijk-vastgoed-hoogmadeseweg-62-leiderdorp", 495_000, 476, None, "opknappen", "1959, maatschappelijk, perceel 2.022 m2", True),
    ("Helderseweg 50", "Alkmaar", "https://www.oozo.nl/bedrijfspanden/alkmaar/west/bergerhof-en-blaeustraatkwartier/68320/bedrijfsruimte-helderseweg-50-alkmaar", 795_000, 536, 4.8, "opknappen", "1927, label G", False),
    ("Dijklaan 131-133", "Breda", "https://www.oozo.nl/bedrijfspanden/breda/breda-west/tuinzigt/44970/bedrijfsruimte-dijklaan-131-133-breda", 950_000, 675, None, "opknappen", "werkplaats 1925, woonwijk", True),
    ("Zaanenstraat 22", "Haarlem", "https://www.oozo.nl/bedrijfspanden/haarlem/indischewijk/molukkenbuurt/46366/bedrijfsruimte-zaanenstraat-22-haarlem", 750_000, 481, None, "opknappen", "werkplaats 1932 met lichtstraten", True),
    ("Heulweg 1", "Pijnacker", "https://www.bedrijfspand.com/bedrijfspanden/bedrijfsruimte/heulweg-1-pijnacker/122494/", 645_000, 494, 6.0, "opknappen", "hal met lichtstraten, bedrijvenpark", False),
    ("Celebesstraat 17", "Wormerveer", "https://www.oozo.nl/bedrijfspanden/zaanstad/wormerveer/wormerveer-zuid/67314/bedrijfsruimte-celebesstraat-17-wormerveer", 545_000, 565, None, "opknappen", "werkplaats 1931, woonwijk", False),
    ("Drilleveld 1", "Nieuwegein", None, 695_000, 608, None, "opknappen", "1959, woonwijk", False),
    ("Enschotsebaan 8", "Berkel-Enschot", "https://www.oozo.nl/bedrijfspanden/tilburg/berkel-enschot/enschotse-akkers/60070/bedrijfsruimte-enschotsebaan-8-berkel-enschot", 1_050_000, 929, None, "opknappen", "1928, perceel 4.735 m2, label G", False),
    ("Nieuw-Loosdrechtsedijk 82a", "Loosdrecht", "https://www.oozo.nl/bedrijfspanden/wijdemeren/nieuw-loosdrecht/nieuw-loosdrechtsedijk/40426/bedrijfsruimte-nieuw-loosdrechtsedijk-82a-loosdrecht", 895_000, 841, 5.0, "opknappen", "1920, plassen, geen station", True),
    ("Hooge Zijde 29", "Eindhoven", "https://www.bedrijfspand.com/bedrijfspanden/bedrijfsruimte/hooge-zijde-29-eindhoven/115825/", 1_350_000, 1035, 7.0, "afgewerkt", "hal 7 m met lichtstraten + kantoor, bedrijventerrein", False),
    ("Stirlingweg 12", "Veghel", "https://www.bedrijfspand.com/bedrijfspanden/bedrijfsruimte/stirlingweg-12-veghel/123340/", 995_000, 940, None, "afgewerkt", "kantoor + hal, bedrijventerrein", False),
    ("Woestduinlaan 35a", "Doorn", "https://www.oozo.nl/bedrijfspanden/utrechtse-heuvelrug/doorn/doorn-west/72404/bedrijfsruimte-woestduinlaan-35-a-doorn", 995_000, 1051, None, "opknappen", "1955, 2 lagen, provincie Utrecht", False),
    ("Motorstraat 7-9", "Rotterdam-Zuid", "https://www.oozo.nl/bedrijfspanden/rotterdam/feijenoord/vreewijk/68926/maatschappelijk-vastgoed-motorstraat-7-9-rotterdam", 1_250_000, 1057, None, "afgewerkt", "maatschappelijk, label A+", False),
    ("Ledeboerstraat 29E", "Tilburg", "https://www.bedrijfspand.com/bedrijfspanden/bedrijfsruimte/ledeboerstraat-29-e-tilburg/123405/", 575_000, 456, 8.0, "afgewerkt", "nieuwe hal 8 m hoog (2020)", False),
    ("Nijverheidsstraat 4C", "Uden", "https://www.bedrijfspand.com/bedrijfspanden/bedrijfsruimte/nijverheidsstraat-4-c-uden/114412/", 949_000, 846, 9.5, "afgewerkt", "nieuwbouwhal 9,5 m hoog", False),
]


def past(m2, hoogte):
    """Grootste aantal eigenaren (stappen van 5, max 70) waarvan het programma past; in een hal van minstens 6,5 m
    mag tot 35% op een tussenvloer. Geeft (N, tussenvloer-aandeel)."""
    hoog = (hoogte or 0) >= 6.5
    best = None
    for N in range(20, 75, 5):
        _, nodig, _ = programma(N // 2, N - N // 2, N // 2)
        if nodig <= m2 * 1.02:
            best = (N, 0.0)
        elif hoog and nodig * 0.65 <= m2 * 1.02:
            best = (N, round(1 - m2 / nodig, 2))
    return best


def rij(k):
    naam, plaats, url, prijs, m2, h, staat, opm, oud = k
    p = past(m2, h)
    basis = dict(naam=naam, plaats=plaats, url=url, prijs=prijs, m2=m2, hoogte=h, opm=opm, oud=oud)
    if not p:
        return dict(basis, eigenaren=0)
    N, tv = p
    totaal = m2 / (1 - tv) if tv else m2          # programma incl. tussenvloer; grondvlak = hele pand
    r = schaal(N // 2, N - N // 2, N // 2, prijs_m2=prijs / m2, staat=staat, m2=round(totaal), tussenvloer=tv)
    return dict(basis, eigenaren=N, clubleden=N // 2, tussenvloer=tv, fee_run=r["fee_run"], fee_inleg=r["fee_inleg"],
                ltv=r["ltv"], capex=r["capex"])


if __name__ == "__main__":
    for k in K:
        print(rij(k))
