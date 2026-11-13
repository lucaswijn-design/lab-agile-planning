"""
Eén upload-set per locatie voor ChatGPT: maximaal 10 beelden (zoveel neemt ChatGPT per bericht) plus één PROMPT.txt
die ChatGPT door alle renders leidt. Gebruikt de beelden die render_pakket.py al maakte.

Draaien: SCRATCH=<scratchpad> python3 chatgpt_set.py
"""
from __future__ import annotations

import json
import os
import sys
import zipfile

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build_ontwerpen import VOLGORDE  # noqa: E402
from ontwerp import kleuren_tekst  # noqa: E402
from render_pakket import slugify  # noqa: E402

SCRATCH = os.environ["SCRATCH"]
PAK = os.path.join(SCRATCH, "renderpakketten")
UIT = os.path.join(SCRATCH, "chatgpt")
VOORKEUR = ["café", "gym", "werken", "sanitair", "bieb", "entree", "studio"]

STIJL = ("Style for every image: Berlin warehouse meets Taghazout calm; second hand and a little organized chaos; raw concrete, old brick and black steel stay visible; "
         "oak, walnut, travertine, lime-washed walls; lots of plants and small trees; warm natural daylight; photorealistic, like a professional interior photo. "
         "No people in focus, no text, no labels, no watermarks.")


def jpg(src, dst, maks=1600):
    im = Image.open(src).convert("RGB")
    im.thumbnail((maks, maks))
    im.save(dst, "JPEG", quality=88)


def naast_elkaar(a, b, dst):
    A, B = Image.open(a).convert("RGB"), Image.open(b).convert("RGB")
    h = max(A.height, B.height)
    im = Image.new("RGB", (A.width + B.width + 40, h), "white")
    im.paste(A, (0, 0)); im.paste(B, (A.width + 40, 0))
    im.thumbnail((2000, 2000))
    im.save(dst, "JPEG", quality=88)


def maak(slug):
    O = json.load(open(os.path.join(HERE, "ontwerp", slug + ".json")))
    src = os.path.join(PAK, slug)
    d = os.path.join(UIT, slug)
    os.makedirs(d, exist_ok=True)
    for f in os.listdir(d):
        os.remove(os.path.join(d, f))
    beelden = []  # (bestandsnaam, wat het is, opdracht of None)

    pl0 = os.path.join(src, "05-plattegrond-begane-grond.png"); pl1 = os.path.join(src, "05-plattegrond-verdieping.png")
    if os.path.exists(pl1):
        naast_elkaar(pl0, pl1, os.path.join(d, "01-plattegrond.jpg"))
        beelden.append(("01-plattegrond.jpg", "floor plan, ground floor (left) and upper floor (right): the layout to follow", None))
    else:
        jpg(pl0, os.path.join(d, "01-plattegrond.jpg"), 2000)
        beelden.append(("01-plattegrond.jpg", "floor plan: the layout to follow", None))
    jpg(os.path.join(src, "06-kleur.png"), os.path.join(d, "02-kleurenplan.jpg"))
    beelden.append(("02-kleurenplan.jpg", "colour plan: one colour family from nature per zone", None))

    jpg(os.path.join(src, "01-maquette-dak-eraf.png"), os.path.join(d, "03-maquette-dak-eraf.jpg"))
    beelden.append(("03-maquette-dak-eraf.jpg", "white model with the roof removed",
                    "Photorealistic architectural cutaway render of the whole building from exactly this camera angle, roof removed. Keep every wall, "
                    "round element and piece of furniture exactly where it is in the model; the floor colours in the model show the colour of each zone."))
    jpg(os.path.join(src, "03-maquette-dak-dicht.png"), os.path.join(d, "04-maquette-dak-dicht.jpg"))
    beelden.append(("04-maquette-dak-dicht.jpg", "white model with the roof on",
                    "Photorealistic aerial render from exactly this angle with the roof on. Keep the building shape and the surroundings. " + O["dak"]["tekst_en"]))

    zones = [z for z in O["zones"] if z.get("prompt")]
    zones.sort(key=lambda z: (VOORKEUR.index(z["type"]) if z["type"] in VOORKEUR else 9, z.get("n", 0)))
    eerst, gezien = [], set()  # eerst één ruimte per soort, dan de rest
    for z in zones:
        if z["type"] not in gezien:
            eerst.append(z); gezien.add(z["type"])
    zones = eerst + [z for z in zones if z not in eerst]
    buiten = O.get("renders", {}).get("buiten", [])
    n_kamers = 5 if buiten else 6
    nr = 5
    for z in zones[:n_kamers]:
        k = slugify(z["naam"])
        foto = [f for f in os.listdir(src) if f.endswith(f"-foto-{z['foto']:02d}.jpg") and k in f] if z.get("foto") else []
        kleuren = kleuren_tekst(z["palet"])
        if foto:
            fn = f"{nr:02d}-{k}-foto.jpg"
            jpg(os.path.join(src, foto[0]), os.path.join(d, fn))
            opdracht = (f"This is the existing space today. Keep the architecture, windows, columns, ceiling height and camera angle exactly. "
                        f"Transform it into the {z['naam']} of the club. {z['prompt']} Colours: {kleuren}.")
            wat = f"listing photo of the existing space that becomes: {z['naam']}"
        else:
            m = [f for f in os.listdir(src) if f.endswith("-maquette.png") and k in f]
            fn = f"{nr:02d}-{k}-maquette.jpg"
            jpg(os.path.join(src, m[0]), os.path.join(d, fn))
            opdracht = (f"This is a simple model of this room seen from above. Make an eye-level photorealistic interior photo of it with exactly this layout. "
                        f"{z['prompt']} Colours: {kleuren}.")
            wat = f"model view of: {z['naam']}"
        beelden.append((fn, wat, opdracht))
        nr += 1
    if buiten:
        f_nr, naam, prompt = buiten[0]
        fs = [f for f in os.listdir(src) if f.startswith("07-") and f.endswith(f"-foto-{f_nr:02d}.jpg")]
        if fs:
            fn = f"{nr:02d}-buiten-{slugify(naam)}-foto.jpg"
            jpg(os.path.join(src, fs[0]), os.path.join(d, fn))
            beelden.append((fn, f"listing photo, outside: {naam}", prompt))
    assert len(beelden) <= 10, len(beelden)

    renders = [(fn, wat, o) for fn, wat, o in beelden if o]
    P = [f"I am planning a members club in an existing building: {O['titel']} in the Netherlands. You are my architectural visualiser.",
         "",
         f"I attached {len(beelden)} images. Read all of them first:",
         *[f"- {fn}: {wat}" for fn, wat, _ in beelden],
         "",
         "Concept (in Dutch, please read it carefully):",
         O["concept"],
         "",
         "The club has a book café as its heart (round sofa around a freestanding fireplace, 1,500 books, a three-group espresso machine), workplaces with sit-stand desks "
         "in small islands that are each slightly rotated (never straight rows), round felt phone booths, a functional gym with power racks (no machines), and round "
         "concrete-look bathroom towers, 3 m high and open at the top, with a V-shaped wall inside: the wash trough is on the open side, toilets and showers are hidden "
         "behind the V, and plants hang over the top rim.",
         "",
         STIJL,
         "",
         "Rules:",
         "1. Follow the floor plan and the models exactly: same positions, same round elements, same zones. Do not invent extra rooms.",
         "2. Use the colour plan per zone: book café olive green, plum and travertine; library deep olive and butter yellow; workplaces slate blue and cognac; gym oxblood and blush; studio fig purple and terracotta; entrance sand and palm green. About 60% of every room stays raw (concrete, brick, steel), 30% zone colour, 10% accent.",
         "3. With a listing photo: keep the existing architecture and the camera angle exactly; only change the interior and finishes.",
         "4. Make one image per reply, landscape 3:2. Then wait until I write 'volgende' before making the next one.",
         "",
         f"Make these {len(renders)} images, in this order:"]
    for i, (fn, wat, o) in enumerate(renders, 1):
        P += [f"{i}. Based on {fn}: {o}"]
    P += ["", "Start now with image 1."]
    open(os.path.join(d, "PROMPT.txt"), "w").write("\n".join(P))
    zp = os.path.join(UIT, f"chatgpt-{slug}.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(d)):
            z.write(os.path.join(d, f), f)
    print(zp, len(beelden), "beelden", len(renders), "renders", round(os.path.getsize(zp) / 1e6, 1), "MB", len("\n".join(P)), "tekens")
    return zp


if __name__ == "__main__":
    for s in (sys.argv[1:] or VOLGORDE):
        maak(s)
