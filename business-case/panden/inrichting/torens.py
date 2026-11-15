"""
Vormstudie sanitairtoren (16 november 2026): rond, achthoek, D-vorm tegen een wand, vierkant, driehoek.
Zelfde programma voor elke vorm: 3 toiletcabines van 0,95 x 1,60 m, een V-wastrog van 2 x 1,3 m met 1,2 m ervoor, een entree van 1,0 m.
Wanden 3,0 m hoog. Prijzen [schatting]: gebogen metal stud + 2 x gebogen plaat € 114/m2 (sanitairtorens.py), rechte wand met hoeken € 75/m2
(achthoek: korte rechte stukken, 8 hoekprofielen), rechte wand € 60/m2.
'Dode ruimte' = wat rond de toren niet bruikbaar is: de strook van 0,9 m loopruimte die elke vrijstaande vorm nodig heeft, minus wat je tegen
de buitenkant kunt zetten (lockers, bank, kast): op rechte vlakken kan dat met standaardmodules, op een bolle wand alleen met maatwerk.
Draaien: python3 inrichting/torens.py
"""
import math

H = 3.0
PRIJS = {"gebogen": 114, "hoek": 75, "recht": 60}


def rond(R=2.75):
    omtrek = 2 * math.pi * R
    return dict(vorm="Rond, vrijstaand (huidig)", m2=math.pi * R * R, wand_m2=omtrek * H, prijs=omtrek * H * PRIJS["gebogen"],
                ring=math.pi * ((R + 0.9) ** 2 - R * R), buiten_bruikbaar=0.0, vlakke_binnenwand=0.0,
                noot="Mooi object, maar pot, fontein en spiegel willen een vlakke wand: binnen komen voorzetwanden, buiten blijft de ring leeg.")


def achthoek(R=2.75):
    s = 2 * R * math.sin(math.pi / 8)  # zijde bij omgeschreven straal R
    omtrek = 8 * s
    m2 = 2 * (1 + math.sqrt(2)) * s * s
    return dict(vorm="Achthoek, vrijstaand", m2=m2, wand_m2=omtrek * H, prijs=omtrek * H * PRIJS["hoek"],
                ring=(8 * (s + 2 * 0.9 * math.tan(math.pi / 8)) * 0.9) / 2 + 8 * s * 0.9 / 2, buiten_bruikbaar=3 * s, vlakke_binnenwand=8 * s,
                noot=f"Leest nog steeds als rond object, maar elke zijde ({s:.2f} m) is vlak: cabines, spiegels en lockers zijn standaard. "
                     "Drie buitenzijden met lockers geven circa 3 x 2,1 m = 100 lockers.")


def d_vorm(B=4.6, diep=1.7):
    R = B / 2
    m2 = B * diep + math.pi * R * R / 2
    gebogen = math.pi * R
    return dict(vorm="D-vorm, rug tegen een bestaande wand", m2=m2, wand_m2=(gebogen + 2 * diep) * H, prijs=gebogen * H * PRIJS["gebogen"] + 2 * diep * H * PRIJS["recht"],
                ring=(math.pi * ((R + 0.9) ** 2 - R * R) / 2) + 2 * diep * 0.9, buiten_bruikbaar=0.0, vlakke_binnenwand=B,
                noot="Leidingen in de bestaande wand, cabines op een rij langs die wand, de ronde voorkant geeft het karakter. Geen rugruimte die verloren gaat.")


def vierkant(B=4.4):
    return dict(vorm="Vierkant, vrijstaand", m2=B * B, wand_m2=4 * B * H, prijs=4 * B * H * PRIJS["recht"],
                ring=4 * (B + 0.9) * 0.9, buiten_bruikbaar=2 * B, vlakke_binnenwand=4 * B,
                noot="Goedkoopst en het efficiëntst binnen, maar een blok in een open hal: precies wat je niet wilt laten zien.")


def driehoek(B=6.6):
    m2 = math.sqrt(3) / 4 * B * B
    return dict(vorm="Driehoek, vrijstaand", m2=m2, wand_m2=3 * B * H, prijs=3 * B * H * PRIJS["recht"],
                ring=3 * (B + 1.5) * 0.9, buiten_bruikbaar=2 * B * 0.6, vlakke_binnenwand=3 * B,
                noot="Scherpe hoeken binnen zijn onbruikbaar voor cabines (circa 30% verlies); als vorm alleen goed voor de V-wand zelf.")


PROGRAMMA_M2 = 3 * 0.95 * 1.60 + 2.0 * (1.3 + 1.2) + 1.0 * 1.5  # cabines + wastrog met ruimte ervoor + entree [berekend]


def tabel():
    out = []
    for v in (rond(), achthoek(), d_vorm(), vierkant(), driehoek()):
        v = dict(v, efficientie=PROGRAMMA_M2 / v["m2"] * (0.7 if v["vorm"].startswith("Driehoek") else 1.0))  # driehoek: scherpe hoeken onbruikbaar
        out.append(v)
    return out


if __name__ == "__main__":
    print(f"programma netto {PROGRAMMA_M2:.1f} m2")
    for v in tabel():
        print(f'{v["vorm"]:42} {v["m2"]:5.1f} m2  efficiëntie {v["efficientie"]:.0%}  wand € {v["prijs"]:6.0f}  ring {v["ring"]:5.1f} m2  '
              f'buiten bruikbaar {v["buiten_bruikbaar"]:4.1f} m  vlak binnen {v["vlakke_binnenwand"]:4.1f} m')
