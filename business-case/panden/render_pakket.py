"""
Renderpakket per locatie voor ChatGPT: maquettebeelden (dak eraf, andere kant, dak dicht, per ruimte),
plattegronden, advertentiefoto's per ruimte en een LEESMIJ met prompts. Eindigt als zip.

Draaien: SCRATCH=<scratchpad> python3 render_pakket.py   (vereist node + playwright, three.js in $SCRATCH/three/package)
Foto's zijn van de makelaar: alleen voor eigen gebruik, niet publiceren (ze blijven buiten git).
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build_ontwerpen import VOLGORDE  # noqa: E402
from ontwerp import BASIS_PROMPT, kleuren_tekst  # noqa: E402

SCRATCH = os.environ["SCRATCH"]
UIT = os.path.join(SCRATCH, "renderpakketten")
KLEURBORD = [os.path.join(SCRATCH, "stijl", "Kleur.png"), os.path.join(SCRATCH, "stijl", "Sanitair.png")]

MAQ_STIJL = ("Late afternoon sun, soft shadows, warm natural light. Neighbouring buildings stay simple light-grey massing. "
             "Materials: raw concrete floor, old brick, black steel, oak and walnut, lime-washed walls, lots of plants and small trees. "
             "Colours per zone exactly as the floor colours in the model: olive green velvet, plum and travertine in the book café, slate blue in the workspace, "
             "oxblood and blush in the gym, fig purple and terracotta in the studio, sand and palm green at the entrance.")


def slugify(t):
    import re
    return re.sub(r"[^a-z0-9]+", "-", t.lower().replace("é", "e")).strip("-")[:40]


def main():
    os.makedirs(UIT, exist_ok=True)
    html = os.path.join(HERE, "ontwerpen.html")
    three = os.path.join(SCRATCH, "three", "package")
    for p, slug in enumerate(VOLGORDE):
        O = json.load(open(os.path.join(HERE, "ontwerp", slug + ".json")))
        d = os.path.join(UIT, slug)
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)
        lv = bool(O.get("niveaus"))
        items = [dict(p=p, mode="open", view="axo", naam="01-maquette-dak-eraf"),
                 dict(p=p, mode="open", view="axo2", naam="02-maquette-dak-eraf-andere-kant"),
                 dict(p=p, mode="dak", view="axo", naam="03-maquette-dak-dicht"),
                 dict(p=p, mode="open", view="boven", naam="04-maquette-bovenaanzicht")]
        if lv:
            items.append(dict(p=p, mode="open", view="axo", l1=False, naam="01b-maquette-begane-grond-zonder-verdieping"))
        kamers = []
        for j, z in enumerate(O["zones"]):
            if not z.get("prompt"):
                continue
            k = f"{10 + len(kamers)}-{slugify(z['naam'])}"
            items.append(dict(p=p, mode="open", view=j, l1=bool(z.get("n")), naam=k + "-maquette"))
            kamers.append((k, z))
        subprocess.run(["node", os.path.join(HERE, "render_maquette.js"), html, three, d, json.dumps(items), "1600", "1200"], check=True, cwd="/tmp")
        # plattegronden
        nivs = [0] + [int(x) for x in O.get("niveaus", {})]
        for n in nivs:
            svg = os.path.join(HERE, "ontwerp", f"{slug}-n{n}.svg")
            subprocess.run(["node", os.path.join(HERE, "render_svg.js"), svg, os.path.join(d, f"05-plattegrond-{'begane-grond' if n == 0 else 'verdieping'}.png"), "2000"], check=True, cwd="/tmp")
        for f in KLEURBORD:
            if os.path.exists(f):
                shutil.copy(f, os.path.join(d, "06-" + os.path.basename(f).lower()))
        fotomap = os.path.join(HERE, "dossiers", slug + "-fotos")
        bron = json.load(open(os.path.join(fotomap, "bron.json")))
        # LEESMIJ
        L = [f"# Renderpakket {O['titel']}", "",
             f"Status advertentie bij het maken van dit pakket: {'te koop' if bron.get('te_koop') else 'ONBEKEND'}, vraagprijs {bron.get('prijs')}, bron {bron.get('url')}.",
             "Foto's met 'foto' in de naam zijn van de makelaar: alleen voor eigen gebruik, niet publiceren.", "",
             "## Zo gebruik je dit in ChatGPT",
             "1. Start een nieuw gesprek. Upload eerst 06-kleur.png en 05-plattegrond: schrijf 'Dit is het kleurenplan en de plattegrond, onthoud ze voor alle beelden.'",
             "2. Doe daarna één beeld per bericht: upload het genoemde bestand en plak de prompt eronder.",
             "3. Klopt de indeling niet, zeg dan precies wat er anders moet ('de ronde bank staat links van de haard, niet rechts').",
             "4. De prompts zijn in het Engels omdat de beeldgenerator daar het nauwkeurigst op reageert.", "",
             "## Concept", O["concept"], "",
             "## Overzichtsbeelden", "",
             "### A. Hele gebouw met het dak eraf",
             "Bestand: 01-maquette-dak-eraf.png (of 02 voor de andere kant)", "",
             "```", "This is a simple white architectural model of a members club inside an existing building, with the roof removed. "
             "Turn it into a photorealistic architectural cutaway render from exactly the same camera angle. Keep every wall, round element and piece of furniture "
             "where it is: the round seating around the fireplace, the round bookshelf room, the two round bathroom towers with plants on top, the desk islands, the gym racks. "
             + MAQ_STIJL, "```", "",
             "### B. Hele gebouw met het dak dicht",
             "Bestand: 03-maquette-dak-dicht.png", "", "```",
             "Turn this simple white model into a photorealistic aerial render from exactly the same angle. Keep the building shape and the surroundings. "
             f"Roof: {O['dak']['tekst']} " + MAQ_STIJL.split(" Materials")[0], "```", ""]
        for nr, naam, prompt in O.get("renders", {}).get("buiten", []):
            src = os.path.join(fotomap, f"foto-{nr:02d}.jpg")
            fn = f"07-buiten-{slugify(naam)}-foto-{nr:02d}.jpg"
            if os.path.exists(src):
                shutil.copy(src, os.path.join(d, fn))
            L += [f"### Buiten: {naam}", f"Bestand: {fn}", "", "```", prompt + " Photorealistic, natural light, no text.", "```", ""]
        L += ["## Ruimte voor ruimte", ""]
        for k, z in kamers:
            L += [f"### {z['naam']} ({z['m2']} m², {z['palet_naam'].lower()})", z["beschrijving"], ""]
            L += [f"- {x}" for x in z["details"]] + [""]
            if z.get("foto"):
                src = os.path.join(fotomap, f"foto-{z['foto']:02d}.jpg")
                fn = f"{k}-foto-{z['foto']:02d}.jpg"
                if os.path.exists(src):
                    shutil.copy(src, os.path.join(d, fn))
                L += [f"**Beeld 1, vanuit de advertentiefoto.** Bestand: {fn}", "", "```", z["prompt_vol"], "```", ""]
                L += [f"**Beeld 2, vanuit de maquette.** Bestand: {k}-maquette.png", ""]
            else:
                L += [f"**Vanuit de maquette** (geen advertentiefoto van deze ruimte). Bestand: {k}-maquette.png", ""]
            L += ["```", "This is a simple 3D model of one room, seen from above. Create a photorealistic eye-level interior photo of this room with exactly this layout and furniture. "
                  + z["prompt"] + " " + BASIS_PROMPT.format(kleuren=kleuren_tekst(z["palet"])).replace("Keep the existing architecture exactly: walls, windows, columns, ceiling height and camera angle. ", ""), "```", ""]
        open(os.path.join(d, "00-LEESMIJ.md"), "w").write("\n".join(L))
        zp = os.path.join(UIT, f"renderpakket-{slug}.zip")
        with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(os.listdir(d)):
                z.write(os.path.join(d, f), f"renderpakket-{slug}/{f}")
        print(zp, round(os.path.getsize(zp) / 1e6, 1), "MB", len(os.listdir(d)), "bestanden")


if __name__ == "__main__":
    main()
