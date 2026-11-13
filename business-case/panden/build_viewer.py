"""
Stap 4: zet dossiers + plattegronden + financiën in één pagina met 3D-viewer.
Draaien: python3 business-case/panden/build_viewer.py  -> panden3d.html
"""
from __future__ import annotations

import base64
import io
import json
import math
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from geo import frame, to_local  # noqa: E402
from layout import AFGEVALLEN, LAYOUTS, STATUS, build  # noqa: E402
import pand_case  # noqa: E402
from build_ontwerpen import TORENS  # noqa: E402

VOLGORDE = ["utrecht-van-heutszstraat-4", "den-bosch-rietveldenweg-13", "den-bosch-eendenkooi-1a"]  # alleen aanbod dat op 13-11-2026 als te koop staat
AFGEVALLEN_TONEN = ["bergen-op-zoom-bosstraat-38", "capelle-lentedans-50a", "amersfoort-computerweg-37", "helmond-mierloseweg-130", "dordrecht-houttuinen-32a", "amersfoort-stadsring-103", "boxtel-bosscheweg-85", "den-haag-pomonaplein-49"]


def img_uri(path, size=768):
    im = Image.open(path).convert("RGB").resize((size, size))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=76, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def basic(slug):
    d = json.load(open(os.path.join(HERE, "dossiers", slug + ".json")))
    F = frame(d["footprint"])
    loc = lambda ring: [[round(c, 2) for c in to_local(p, F)] for p in ring]
    bb = d["luchtfoto"]["bbox"]
    hoeken = [to_local(p, F) for p in ((bb[0], bb[1]), (bb[2], bb[1]), (bb[2], bb[3]), (bb[0], bb[3]))]
    n0 = to_local(d["centrum"], F)
    n1 = to_local((d["centrum"][0], d["centrum"][1] + 10), F)
    noord = math.degrees(math.atan2(n1[1] - n0[1], n1[0] - n0[0]))
    return d, dict(
        slug=slug, adres=d["adres"], regio=d.get("regio"), aanbod=d.get("aanbod"), bouwjaar=d["bouwjaar"],
        hoogte=d["hoogte"], hoogte_bron=d.get("hoogte_bron", "3D BAG"), footprint=loc(d["footprint"]),
        footprint_m2=d["footprint_m2"], vbos=d["vbos"], vbo_m2=d["vbo_m2_totaal"],
        perceel=loc(d["perceel"]["ring"]) if d["perceel"] and d["perceel"].get("ring") else None,
        perceel_m2=(d["perceel"] or {}).get("m2"), perceel_opm=(d["perceel"] or {}).get("opmerking"),
        context=[dict(ring=loc(c["ring"]), h=c["h"], eigen=bool(c.get("op_perceel"))) for c in d["context"]],
        hoeken=[[round(a, 2), round(b, 2)] for a, b in hoeken], noord=round(noord, 1),
        foto=img_uri(os.path.join(HERE, "dossiers", d["luchtfoto"]["file"])),
    )


def main():
    panden = []
    afgevallen = []
    for slug, reden in [(k, AFGEVALLEN[k]) for k in AFGEVALLEN_TONEN]:
        d = json.load(open(os.path.join(HERE, "dossiers", slug + ".json")))
        afgevallen.append(dict(adres=d["adres"], regio=d.get("regio"), bouwjaar=d["bouwjaar"], footprint_m2=d["footprint_m2"],
                               vbo_m2=d["vbo_m2_totaal"], perceel_m2=(d["perceel"] or {}).get("m2"), reden=reden))
    for slug in VOLGORDE:
        d, b = basic(slug)
        if slug in LAYOUTS:
            v, q = build(slug)
            r = pand_case.run(slug, torens=TORENS.get(slug, False))
            r90 = pand_case.run(slug, n_club=LAYOUTS[slug]["leden"]["n_club"] + 30, torens=TORENS.get(slug, False))
            fin = {k: r[k] for k in ("capex", "verbouw_inrichting", "huur", "opex", "lening", "ltv", "dscr", "resultaat",
                                     "fee_vol_nodig", "fee_deel_nodig", "jaren_schuldvrij", "exitwaarde",
                                     "exit_per_vol_versneld", "groepen")}
            fin["fee_inleg_terug"] = pand_case.fee_inleg_terug(slug, torens=TORENS.get(slug, False))
            extra = LAYOUTS[slug]["leden"]["n_club"] + 30
            fin["fee_inleg_terug_90"] = pand_case.fee_inleg_terug(slug, n_club=extra, torens=TORENS.get(slug, False))
            fin["fee_vol_nodig_90"] = r90["fee_vol_nodig"]
            fin["extra_club"] = extra
            fin["opex_rows"] = r["opex_rows"]
            fin["rows"] = [dict(groep=x["groep"], post=x["post"].replace("m2", "m²"), h=x["h"], e=x["e"].replace("m2", "m²"),
                                prijs=x["prijs"], totaal=x["totaal"], label=x["label"]) for x in r["rows"]]
            b.update(titel=v["titel"], oordeel=v["oordeel"], samenvatting=v["samenvatting"], zones=v["zones"],
                     buiten=v["buiten"], bomen=v["bomen_buiten"], pui=v["pui"], meubels=v["meubels"], leden=v["leden"],
                     werkniveau=v["werkniveau"], pv=v["pv_kwp"], q=q, fin=fin, verhuur=LAYOUTS[slug]["verhuur"],
                     koop=LAYOUTS[slug]["koop"])
            if slug in STATUS:
                b.update(oordeel=STATUS[slug][0], aanbod=STATUS[slug][1])
        else:
            b.update(titel=d["adres"].split(",")[0], oordeel="valt af", samenvatting=AFGEVALLEN[slug])
        panden.append(b)
    tpl = open(os.path.join(HERE, "viewer_template.html"), encoding="utf-8").read()
    html = tpl.replace("/*__DATA__*/null", json.dumps(panden, ensure_ascii=False, separators=(",", ":"))) \
              .replace("/*__AF__*/null", json.dumps(afgevallen, ensure_ascii=False, separators=(",", ":")))
    out = os.path.join(HERE, "panden3d.html")
    open(out, "w", encoding="utf-8").write(html)
    print("geschreven", out, round(len(html) / 1e6, 2), "MB")


if __name__ == "__main__":
    main()
