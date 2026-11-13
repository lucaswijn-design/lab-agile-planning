"""
Stap 0 + foto's: open de advertentie, lees de status en haal de foto's op.
Alleen voor eigen referentie (renders); foto's zijn van de makelaar, niet publiceren.
Draaien: python3 business-case/panden/fotos.py
"""
from __future__ import annotations

import json
import os
import re
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
UA = "Mozilla/5.0"

ADVERTENTIES = {
    "utrecht-van-heutszstraat-4": "https://www.bedrijfspand.com/bedrijfspanden/bedrijfsruimte/van-heutszstraat-4-utrecht/116706/",
    "den-bosch-rietveldenweg-13": "https://www.bedrijfspand.com/bedrijfspanden/bedrijfsruimte/rietveldenweg-13-den-bosch/126268/",
    "den-bosch-eendenkooi-1a": "https://www.bedrijfspand.com/bedrijfspanden/bedrijfsruimte/de-eendenkooi-1-a-den-bosch/125406/",
}


def curl(url, out=None):
    args = ["curl", "-sS", "-m", "40", "-A", UA, url]
    if out:
        args += ["-o", out]
    return subprocess.run(args, capture_output=True, text=out is None, check=True).stdout


def status(html):
    txt = re.sub(r"<[^>]+>", " ", html)
    txt = re.sub(r"\s+", " ", txt)
    vonden = {}
    for label, pat in (("online", r"Online sinds:?\s*([0-9-]{8,10})"), ("bijgewerkt", r"Laatst bijgewerkt:?\s*([0-9-]{8,10})"),
                       ("prijs", r"(?:Koopprijs|Vraagprijs|Prijs)\s*:?\s*(€\s?[0-9.]+[^|]{0,20})")):
        m = re.search(pat, txt, re.I)
        vonden[label] = m.group(1).strip() if m else None
    vonden["te_koop"] = bool(re.search(r"\bte koop\b", txt, re.I))
    vonden["verkocht"] = bool(re.search(r"\b(verkocht|onder bod)\b", txt, re.I))
    return vonden


def fotos(slug, url):
    html = curl(url)
    obj = re.search(r"/(\d+)/?$", url).group(1)
    st = status(html)
    urls = sorted(set(re.findall(rf"https://cdn\.bedrijfspand\.com/media/cache/[^\"' ]+_{obj}_(\d+)_[0-9]+\.(?:jpg|jpeg|png|webp)", html)))
    alle = re.findall(rf"(https://cdn\.bedrijfspand\.com/media/cache/[^\"' ]+_{obj}_(\d+)_[0-9]+\.(?:jpg|jpeg|png|webp))", html)
    per_n = {}
    for u, n in alle:
        per_n.setdefault(int(n), set()).add(u)
    map_ = os.path.join(HERE, "dossiers", slug + "-fotos")
    os.makedirs(map_, exist_ok=True)
    tmp = os.path.join(map_, "_tmp")
    bewaard = 0
    for n in sorted(per_n)[:12]:
        beste, grootte = None, 0
        for u in per_n[n]:
            try:
                curl(u, tmp)
            except subprocess.CalledProcessError:
                continue
            g = os.path.getsize(tmp)
            if g > grootte:
                beste, grootte = u, g
                os.replace(tmp, os.path.join(map_, f"foto-{n:02d}.jpg"))
        if beste:
            bewaard += 1
    if os.path.exists(tmp):
        os.remove(tmp)
    st.update(url=url, fotos=bewaard)
    json.dump(st, open(os.path.join(map_, "bron.json"), "w"), ensure_ascii=False, indent=1)
    return st


if __name__ == "__main__":
    for s, u in ADVERTENTIES.items():
        print(s, fotos(s, u))
