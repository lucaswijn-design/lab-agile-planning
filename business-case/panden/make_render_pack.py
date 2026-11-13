"""
Renderpakket per pand: één referentiebord (PNG) om aan een beeldmodel te geven.
Gebruikt de 3D-viewer (panden3d.html) via Playwright voor de beelden.
Draaien: python3 business-case/panden/make_render_pack.py
Vereist: node + playwright, three.js lokaal in <scratch>/three/package (alleen voor headless renderen).
"""
from __future__ import annotations

import base64
import io
import json
import os
import subprocess
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from layout import LAYOUTS, build  # noqa: E402
from geo import frame  # noqa: E402

OUT = os.path.join(HERE, "renders")
SCRATCH = os.environ.get("SCRATCH", "/tmp")

PANDEN = {
    "rotterdam-hillevliet-139": dict(
        idx=0, kop="Clubhuis in een kerk van J.J.P. Oud",
        gebouw="Voormalige Leger des Heils-kerk, Hillevliet 139 Rotterdam, 1929, architect J.J.P. Oud, rijksmonument. "
               "Rechthoekige kerkzaal circa 27 x 19 m, 9 m hoog; strook tuin op het zuiden.",
        behoud="Gevel, ramen en daklijn blijven zoals ze zijn (monument). Nieuw: houten tussenvloer met stalen balustrade "
               "achterin de zaal, glazen pui naar het terras.",
    ),
    "tilburg-bredaseweg-443": dict(
        idx=1, kop="Clubhuis in een villa op een landgoed",
        gebouw="Kantoorvilla Bredaseweg 443 Tilburg: villa uit 1941 met een vleugel uit 2000, verbonden door een gang. "
               "Op een bosrijk landgoed van circa 8.000 m² aan de rand van de Warande.",
        behoud="Villa en vleugel blijven; nieuw is een glazen pui en een terras aan de bosrand. Verdieping en souterrain van de villa worden verhuurd.",
    ),
}

STIJL = ("Sfeer: ontspannen 'georganiseerde chaos' zoals een Berlijns koffie- en boekencafé. Tweedehands, natuurlijke materialen "
         "(hout, leer, linnen, wol), veel planten en een paar bomen binnen, warm licht. Industrieel waar het kan: zichtbaar staal en beton. "
         "Werkplekken zijn goed en ergonomisch (zit-sta bureaus, twee schermen), maar staan in losse eilandjes en niet in rijen. "
         "Het boekencafé is het hart: een boekenwand van 12 m met rolladder en circa 1.500 boeken, een 3-groeps La Marzocco "
         "aan een zelfgebouwde bar, leesfauteuils, kleden, een sfeerhaard en een platenspeler. Gym: functioneel, met zwarte "
         "racks, rubbervloer, roeiers en kettlebells, geen glimmende apparaten.")


def uri(path_or_bytes, fmt="png"):
    data = path_or_bytes if isinstance(path_or_bytes, bytes) else open(path_or_bytes, "rb").read()
    return f"data:image/{fmt};base64," + base64.b64encode(data).decode()


def luchtfoto(slug):
    d = json.load(open(os.path.join(HERE, "dossiers", slug + ".json")))
    x0, y0, x1, y1 = d["luchtfoto"]["bbox"]
    im = Image.open(os.path.join(HERE, "dossiers", d["luchtfoto"]["file"])).convert("RGB")
    W, H = im.size
    dr = ImageDraw.Draw(im)
    px = lambda p: ((p[0] - x0) / (x1 - x0) * W, (y1 - p[1]) / (y1 - y0) * H)
    if d["perceel"] and d["perceel"].get("ring"):
        dr.line([px(p) for p in d["perceel"]["ring"]] + [px(d["perceel"]["ring"][0])], fill=(255, 220, 0), width=5)
    dr.line([px(p) for p in d["footprint"]] + [px(d["footprint"][0])], fill=(255, 60, 60), width=6)
    im = im.crop((192, 192, 832, 832))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=85)
    return uri(buf.getvalue(), "jpeg"), d


def shots():
    """Maak met Playwright de 3D-beelden en plattegronden uit de viewer."""
    page = os.path.join(SCRATCH, "p3d_render.html")
    html = open(os.path.join(HERE, "panden3d.html"), encoding="utf-8").read()
    open(page, "w", encoding="utf-8").write('<!doctype html><html><head><meta charset="utf-8"></head><body>' + html + "</body></html>")
    js = r"""
const {chromium}=require('playwright');
(async()=>{const [page,three,out,list]=process.argv.slice(2);const items=JSON.parse(list);
const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist']});
const p=await b.newPage({viewport:{width:1400,height:1050},deviceScaleFactor:2});
await p.route('**/three.min.js',r=>r.fulfill({path:three+'/build/three.min.js',contentType:'application/javascript'}));
await p.route('**/OrbitControls.js',r=>r.fulfill({path:three+'/examples/js/controls/OrbitControls.js',contentType:'application/javascript'}));
await p.route('https://fonts.googleapis.com/**',r=>r.abort());
await p.goto('file://'+page);await p.waitForTimeout(2000);
for(const it of items){
  await p.evaluate(i=>window.__v.show(i),it.idx);await p.evaluate(()=>window.__v.setMode('nieuw'));await p.waitForTimeout(1500);
  const view=await p.$('#view');
  await p.evaluate(()=>{document.querySelector('.hud').style.display='none';document.querySelector('.legend').style.display='none';});
  await view.screenshot({path:`${out}/${it.slug}-3d-nieuw.png`});
  await p.evaluate(([x,y,z])=>{const v=window.__v;v.camera.position.set(x,y,z);v.controls.target.set(0,1.5,0);v.controls.update();},it.laag);
  await p.waitForTimeout(800);await view.screenshot({path:`${out}/${it.slug}-3d-nieuw-laag.png`});
  await p.evaluate(()=>window.__v.show(window.__cur||0));
  await p.evaluate(i=>window.__v.show(i),it.idx);await p.evaluate(()=>window.__v.setMode('huidig'));await p.waitForTimeout(1200);
  await p.evaluate(()=>{document.querySelector('.hud').style.display='none';document.querySelector('.legend').style.display='none';});
  await view.screenshot({path:`${out}/${it.slug}-3d-huidig.png`});
  await p.evaluate(()=>window.__v.setMode('nieuw'));await p.waitForTimeout(600);
  const svg=await p.$('#plan svg');await svg.screenshot({path:`${out}/${it.slug}-plattegrond.png`});
}
await b.close();})();
"""
    jsf = os.path.join(SCRATCH, "render_shots.js")
    open(jsf, "w").write(js)
    items = [dict(slug=s, idx=c["idx"], laag=[-6, 7, 34]) for s, c in PANDEN.items()]
    subprocess.run(["node", jsf, page, os.path.join(SCRATCH, "three", "package"), OUT, json.dumps(items)],
                   check=True, cwd=SCRATCH)


def board(slug, cfg):
    v, q = build(slug)
    foto, d = luchtfoto(slug)
    F = frame(d["footprint"])
    zones = "".join(
        f'<tr><td><i style="background:{z["kleur"]}"></i>{z["naam"]}</td><td class="r">{z["m2"]} m²</td></tr>'
        for z in v["zones"])
    img = lambda n: uri(os.path.join(OUT, f"{slug}-{n}.png"))
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
body{{margin:0;background:#f4f1ea;color:#1d2420;font:22px/1.45 'DejaVu Sans',sans-serif}}
.w{{width:2400px;padding:48px;box-sizing:border-box;display:grid;gap:28px}}
h1{{font-size:54px;margin:0}} h2{{font-size:28px;margin:0 0 8px}}
.g2{{display:grid;grid-template-columns:1fr 1fr;gap:24px}} .g3{{display:grid;grid-template-columns:1.25fr 1fr;gap:24px}}
img{{width:100%;display:block;border-radius:10px;border:1px solid #cfc8ba}}
.cap{{font-size:19px;color:#5b5f57;margin-top:6px}}
table{{border-collapse:collapse;width:100%;font-size:21px}} td{{padding:5px 8px;border-bottom:1px solid #ddd5c6}}
td.r{{text-align:right;font-family:'DejaVu Sans Mono',monospace}} i{{display:inline-block;width:16px;height:16px;border-radius:3px;margin-right:10px;vertical-align:-2px}}
.box{{background:#fffdf8;border:1px solid #cfc8ba;border-radius:10px;padding:20px}}
</style></head><body><div class="w">
<div><div style="font-size:20px;letter-spacing:.12em;text-transform:uppercase;color:#7a5a2a">Referentiebord voor renders · ledenclub</div>
<h1>{cfg['kop']}</h1><p style="margin:8px 0 0;max-width:1900px">{cfg['gebouw']}</p></div>
<div class="g2">
 <div><img src="{img('3d-nieuw')}"><div class="cap">Nieuwe situatie, vogelvlucht. Blokmodel: kleuren = zones, glas = pui, oranje lijnen = bestaande gevels. Buren in cyaan.</div></div>
 <div><img src="{img('3d-nieuw-laag')}"><div class="cap">Nieuwe situatie, laag gezichtspunt vanaf het terras.</div></div>
</div>
<div class="g3">
 <div><img src="{img('plattegrond')}"><div class="cap">Plattegrond nieuw (boven = binnen de kleurvlakken). Schaalbalk 10 m, noordpijl rechtsboven.</div></div>
 <div style="display:grid;gap:20px;align-content:start">
  <div class="box"><h2>Zones</h2><table>{zones}</table>
   <p class="cap">Gebouw {F['L']:.0f} × {F['W']:.0f} m, hoogte circa {d['hoogte']:.0f} m, bouwjaar {d['bouwjaar']}. Gym: {q['gym_cap']} mensen tegelijk. Werken: {q['werk_cap']} plekken.</p></div>
  <div class="box"><h2>Wat blijft, wat is nieuw</h2><p style="margin:0">{cfg['behoud']}</p></div>
 </div>
</div>
<div class="g3">
 <div class="box"><h2>Sfeer en inrichting</h2><p style="margin:0">{STIJL}</p></div>
 <div class="g2"><div><img src="{img('3d-huidig')}"><div class="cap">Huidige situatie (3D BAG).</div></div>
  <div><img src="{foto}"><div class="cap">Luchtfoto PDOK: rood = gebouw, geel = perceel.</div></div></div>
</div>
</div></body></html>"""
    hp = os.path.join(SCRATCH, f"board-{slug}.html")
    open(hp, "w", encoding="utf-8").write(html)
    js = os.path.join(SCRATCH, "board.js")
    open(js, "w").write("""const {chromium}=require('playwright');(async()=>{const [hp,out]=process.argv.slice(2);
const b=await chromium.launch();const p=await b.newPage({viewport:{width:2400,height:1200},deviceScaleFactor:1});
await p.goto('file://'+hp);await p.waitForTimeout(500);await p.screenshot({path:out,fullPage:true});await b.close();})();""")
    out = os.path.join(OUT, f"{slug}-renderbord.png")
    subprocess.run(["node", js, hp, out], check=True, cwd=SCRATCH)
    return out


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    shots()
    for s, c in PANDEN.items():
        print(board(s, c))
