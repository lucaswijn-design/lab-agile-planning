"""
Sobere industriële variant (15 november 2026): ruw laten waar het kan, strak waar je het elke dag ziet of voelt.
Strak: de vloer, de bureaus, de keuken. Ruw en hergebruikt: kozijnen, binnenwanden, glaswanden, akoestiek, stoelen.
Leden helpen op ledendagen bij isoleren, sauzen en de tuin (eigen arbeid wordt getoond, niet betaald).

toepassen(rows) -> (nieuwe rows, verschillen). Wordt aangeroepen in pand_case.rows_for(..., sober=True) vóór Bijkomend,
zodat onvoorzien en projectleiding meeschalen.
"""
from __future__ import annotations

UURWAARDE_LEDEN = 35  # [aanname] waarde van een uur eigen arbeid, alleen getoond

# prefix van de post -> (nieuwe omschrijving, nieuwe prijs per eenheid, label, reden)
MAP = [
    ("Glazen pui, aluminium", "Glazen pui: hergebruikte stalen of houten kozijnen, nieuw HR++ glas, aanpassen en plaatsen", 550, "schatting",
     "tweedehands kozijn € 0 tot 150 per m², HR++ glas circa € 150, plaatsen en aanpassen circa € 250"),
    ("Glazen scheidingswand", "Glaswand van oude ramen in houten regelwerk (gym en vergaderen)", 160, "schatting",
     "oude ramen via sloop of tweedehands, regelwerk en kit, timmerman circa 2 u per m²"),
    ("Extra vergaderkamers: glazen wand", "Extra vergaderkamers: wand van oude ramen in houten regelwerk", 160, "schatting", "zoals hierboven"),
    ("Glazen binnenwand", "Binnenwand van oude ramen in houten regelwerk", 160, "schatting", "zoals hierboven"),
    ("Akoestische plafondeilanden", "Akoestiek: houtwolplaten en zelfgemaakte vilt- en stofpanelen", 22, "schatting",
     "houtwolplaat circa € 15 per m², bevestiging en eigen arbeid"),
    ("Binnenwanden metal stud", "Binnenwanden houten regelwerk, hergebruikt plaatmateriaal en steigerhout", 45, "schatting",
     "hergebruikt plaatmateriaal is goedkoper dan nieuw OSB; regelwerk en arbeid blijven"),
    ("Betonvloer schuren en coaten", "Betonvloer strak: scheuren repareren, egaliseren waar nodig, machinaal schuren en coaten", 35, "schatting",
     "strakker dan alleen coaten (€ 22); een PU gietvloer kost € 60 tot 85 per m² (slimster), gepolijst beton € 40 tot 60 (bobex)"),
    ("Refurbished Steelcase", "Refurbished bureaustoel (Ahrend 2020)", 300, "bron", "offeco.nl, € 300 excl. btw"),
    ("Tweede monitor", "Tweede monitor: geschrapt (laptop als tweede scherm)", 0, "aanname", "leden werken met laptop + één groot scherm"),
    ("Dubbele monitorarm", "Enkele monitorarm", 30, "schatting", "één scherm per plek"),
    ("Keuken 6 m", "Keuken: tweedehands RVS horecawerkbanken en spoeltafel, oude fronten in hout, nieuwe apparatuur", 11_000, "schatting",
     "apparatuur blijft circa € 7.500; kasten en blad van € 8.500 naar € 3.500"),
]

# arbeid die leden overnemen: prefix -> (nieuwe prijs, uren eigen arbeid per eenheid, omschrijving)
ARBEID = [
    ("Dakisolatie, timmerman", None, 0.5, "Dakisolatie: helft van de uren door leden, timmerman leidt"),
    ("Sauswerk wanden en staal", 3, 0.15, "Sauswerk: leden sauzen, alleen verf en materiaal"),
    ("Onttegelen en groen aanleggen", 12, 0.4, "Tuin: leden onttegelen en planten, hovenier ontwerpt en levert"),
]


def toepassen(rows):
    out, diff, uren = [], [], 0.0
    for r in rows:
        r2 = dict(r)
        for pre, post, prijs, label, reden in MAP:
            if r["post"].startswith(pre):
                r2.update(post=post, prijs=prijs, totaal=round(r["h"] * prijs), label=label)
                diff.append(dict(oud=r["post"], nieuw=post, h=r["h"], e=r["e"], prijs_oud=r["prijs"], prijs_nieuw=prijs,
                                 verschil=r2["totaal"] - r["totaal"], reden=reden))
                break
        for pre, prijs, eigen, post in ARBEID:
            if r["post"].startswith(pre):
                if prijs is None:  # uren: helft blijft betaald
                    eu = r["h"] * eigen
                    r2.update(post=post, h=round(r["h"] - eu, 1), totaal=round((r["h"] - eu) * r["prijs"]))
                else:
                    eu = r["h"] * eigen
                    r2.update(post=post, prijs=prijs, totaal=round(r["h"] * prijs))
                uren += eu
                diff.append(dict(oud=r["post"], nieuw=post, h=r["h"], e=r["e"], prijs_oud=r["prijs"], prijs_nieuw=r2["prijs"],
                                 verschil=r2["totaal"] - r["totaal"], reden=f"{round(eu)} uur eigen arbeid door leden"))
                break
        out.append(r2)
    if uren:
        out.append(dict(groep="Eigen arbeid", post=f"Ledendagen: {round(uren)} uur eigen arbeid (waarde € {UURWAARDE_LEDEN} per uur, niet betaald)",
                        h=round(uren), e="uur", prijs=0, totaal=0, label="aanname", gen=0, waarde=round(uren * UURWAARDE_LEDEN)))
    return out, diff
