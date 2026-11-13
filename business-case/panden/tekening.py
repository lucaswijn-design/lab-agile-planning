"""
Architectuurtekening (plattegrond) per locatie uit ontwerp/<slug>.json, als SVG.
tekening(slug, niveau=0) -> svg-string. Draaien: python3 tekening.py -> ontwerp/<slug>-n<niveau>.svg
"""
from __future__ import annotations

import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from geo import frame, to_local  # noqa: E402

INK = "#1d1d1b"
FONT = "Work Sans, Helvetica, Arial, sans-serif"
MONO = "Space Mono, ui-monospace, monospace"


def f(x):
    return f"{x:.2f}"


def pts(p):
    return " ".join(f"{f(a)},{f(b)}" for a, b in p)


def arc_sector(c, r_in, r_out, a0, a1):
    """Annulus-sector als SVG path (graden, tegen de klok in van +u naar +v)."""
    a0r, a1r = math.radians(a0), math.radians(a1)
    large = 1 if (a1 - a0) % 360 > 180 or (a1 - a0) >= 360 else 0
    P = lambda r, a: (c[0] + r * math.cos(a), c[1] + r * math.sin(a))
    o0, o1, i1, i0 = P(r_out, a0r), P(r_out, a1r), P(r_in, a1r), P(r_in, a0r)
    return (f"M{f(o0[0])} {f(o0[1])} A{f(r_out)} {f(r_out)} 0 {large} 1 {f(o1[0])} {f(o1[1])} "
            f"L{f(i1[0])} {f(i1[1])} A{f(r_in)} {f(r_in)} 0 {large} 0 {f(i0[0])} {f(i0[1])} Z")


def rect(c, w, d, a):
    return f'x="{f(c[0]-w/2)}" y="{f(c[1]-d/2)}" width="{f(w)}" height="{f(d)}" transform="rotate({a:.1f} {f(c[0])} {f(c[1])})"'


def toren_svg(c, r, open_deg, soort):
    """Sanitairtoren getekend met opening naar -u, daarna gedraaid naar open_deg."""
    opening = 1.2 if soort == "was" else 1.0
    apex = -0.7 if soort == "was" else -0.5
    end_x, front_x = (0.75, 0.9) if soort == "was" else (0.5, 0.7)
    ys = [-1.65, -0.55, 0.55, 1.65] if soort == "was" else [-1.35, -0.45, 0.45, 1.35]
    s = []
    d = math.asin(opening / 2 / r)
    p1 = (r * math.cos(math.pi + d), r * math.sin(math.pi + d)); p2 = (r * math.cos(math.pi - d), r * math.sin(math.pi - d))
    s.append(f'<circle cx="0" cy="0" r="{r}" fill="#e9e4d8"/>')
    t = math.tan(math.radians(40))
    ends = [(end_x, sg * (end_x - apex) * t) for sg in (-1, 1)]
    s.append(f'<path d="M{f(apex)} 0 L{f(ends[0][0])} {f(ends[0][1])} L{f(front_x)} {f(ys[0])} L{f(math.sqrt(r*r-ys[0]**2))} {f(ys[0])} '
             f'A {r} {r} 0 0 1 {f(math.sqrt(r*r-ys[-1]**2))} {f(ys[-1])} L{f(front_x)} {f(ys[-1])} L{f(ends[1][0])} {f(ends[1][1])} Z" fill="#d6cdb8"/>')
    n = int(2 * math.pi * r / 0.45)
    for i in range(n):
        th = 2 * math.pi * i / n
        if abs(math.atan2(math.sin(th - math.pi), math.cos(th - math.pi))) < d + 0.08:
            continue
        s.append(f'<circle cx="{f(r*math.cos(th))}" cy="{f(r*math.sin(th))}" r="{0.11+0.03*((i*5)%3):.2f}" fill="#5f7a3a" opacity="0.55"/>')
    s.append(f'<path d="M{f(p1[0])} {f(p1[1])} A {r} {r} 0 1 1 {f(p2[0])} {f(p2[1])}" fill="none" stroke="{INK}" stroke-width="0.16"/>')
    for y in ys:
        s.append(f'<line x1="{f(front_x)}" y1="{f(y)}" x2="{f(math.sqrt(r*r-y*y))}" y2="{f(y)}" stroke="{INK}" stroke-width="0.07"/>')
    for i in range(len(ys) - 1):
        y0, y1 = ys[i], ys[i + 1]; ym = (y0 + y1) / 2; xw = math.sqrt(r * r - ym * ym)
        if soort == "was":
            s.append(f'<path d="M{f(front_x)} {f(y0+0.1)} A 0.8 0.8 0 0 0 {f(front_x-0.62)} {f(y0+0.55)}" fill="none" stroke="{INK}" stroke-width="0.025"/>')
            s.append(f'<ellipse cx="{f(xw-0.42)}" cy="{f(ym)}" rx="0.27" ry="0.19" fill="#fff" stroke="{INK}" stroke-width="0.03"/>')
        else:
            s.append(f'<line x1="{f(front_x)}" y1="{f(y0+0.1)}" x2="{f(front_x)}" y2="{f(y1-0.1)}" stroke="#7f9aa8" stroke-width="0.04" stroke-dasharray="0.1 0.07"/>')
            s.append(f'<circle cx="{f(xw-0.5)}" cy="{f(ym)}" r="0.24" fill="none" stroke="#7f9aa8" stroke-width="0.05"/>')
    s.append(f'<path d="M{f(ends[0][0])} {f(ends[0][1])} L{f(apex)} 0 L{f(ends[1][0])} {f(ends[1][1])}" fill="none" stroke="#55514a" stroke-width="0.24" stroke-linejoin="miter"/>')
    if soort == "was":
        for ex, ey in ends:
            L = math.hypot(ex - apex, ey); dx, dy = (ex - apex) / L, ey / L
            nx, ny = -dy, dx
            if nx > 0:
                nx, ny = -nx, -ny
            x1, y1 = apex + dx * 0.5 + nx * 0.36, dy * 0.5 + ny * 0.36
            x2, y2 = apex + dx * (L - 0.1) + nx * 0.36, dy * (L - 0.1) + ny * 0.36
            s.append(f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" stroke="#b9b1a2" stroke-width="0.45"/>')
            s.append(f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" stroke="#7f9aa8" stroke-width="0.16"/>')
    else:
        for sg in (-1, 1):
            a0 = math.radians(180 - sg * 22); a1 = math.radians(180 - sg * 95); rb = r - 0.3
            s.append(f'<path d="M{f(rb*math.cos(a0))} {f(rb*math.sin(a0))} A {rb} {rb} 0 0 {1 if sg == 1 else 0} {f(rb*math.cos(a1))} {f(rb*math.sin(a1))}" fill="none" stroke="#a07a52" stroke-width="0.38"/>')
    return f'<g transform="translate({f(c[0])} {f(c[1])}) rotate({open_deg-180:.1f})">' + "".join(s) + "</g>"


def element_svg(e):
    t = e["t"]; k = e.get("kleur", "#cfc8ba")
    if t == "bureau":
        c, a = e["c"], e["a"]
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        o = e["d"] / 2 + 0.28
        ch = (c[0] + o * sa, c[1] - o * ca)
        return (f'<rect {rect(c, e["w"], e["d"], a)} fill="#efe7d6" stroke="{INK}" stroke-width="0.03"/>'
                f'<circle cx="{f(ch[0])}" cy="{f(ch[1])}" r="0.24" fill="#fff" stroke="{INK}" stroke-width="0.025"/>')
    if t == "wand":
        p = e["pts"]
        if e.get("glas"):
            return (f'<polyline points="{pts(p)}" fill="none" stroke="#5c7a88" stroke-width="0.14"/>'
                    f'<polyline points="{pts(p)}" fill="none" stroke="#fbf9f4" stroke-width="0.05"/>')
        kl = "#55514a" if e.get("bestaand") else INK
        return f'<polyline points="{pts(p)}" fill="none" stroke="{kl}" stroke-width="{max(0.2, e.get("dikte", 0.2))}" stroke-linecap="butt"/>'
    if t == "deur":
        c, a, w = e["c"], math.radians(e["a"]), e.get("w", 1.0)
        ux, uy = math.cos(a), math.sin(a)
        h0 = (c[0] - ux * w / 2, c[1] - uy * w / 2); h1 = (c[0] + ux * w / 2, c[1] + uy * w / 2)
        nx, ny = -uy, ux
        tip = (h0[0] + nx * w, h0[1] + ny * w)
        s = (f'<line x1="{f(h0[0])}" y1="{f(h0[1])}" x2="{f(tip[0])}" y2="{f(tip[1])}" stroke="{INK}" stroke-width="0.04"/>'
             f'<path d="M{f(tip[0])} {f(tip[1])} A {w} {w} 0 0 0 {f(h1[0])} {f(h1[1])}" fill="none" stroke="{INK}" stroke-width="0.025" stroke-dasharray="0.08 0.06"/>')
        if e.get("toegang"):
            s += f'<rect x="{f(h1[0]+nx*0.15-0.09)}" y="{f(h1[1]+ny*0.15-0.09)}" width="0.18" height="0.18" fill="#a8332e"/>'
        return s
    if t == "label":
        return ""
    if t == "box":
        if e.get("glas"):
            return f'<rect {rect(e["c"], e["w"], e["d"], e["a"])} fill="#dfe8ec" fill-opacity="0.5" stroke="#5c7a88" stroke-width="0.08"/>'
        op = 0.35 if e["soort"] in ("platform", "sledebaan") else 0.8
        return f'<rect {rect(e["c"], e["w"], e["d"], e["a"])} fill="{k}" fill-opacity="{op}" stroke="{INK}" stroke-width="0.03"/>'
    if t == "cil":
        if e["soort"] == "belcel":
            return f'<circle cx="{f(e["c"][0])}" cy="{f(e["c"][1])}" r="{e["r"]}" fill="{k}" fill-opacity="0.75" stroke="{INK}" stroke-width="0.1"/>'
        return f'<circle cx="{f(e["c"][0])}" cy="{f(e["c"][1])}" r="{e["r"]}" fill="{k}" fill-opacity="0.85" stroke="{INK}" stroke-width="0.025"/>'
    if t == "kleed":
        if "r" in e:
            return f'<circle cx="{f(e["c"][0])}" cy="{f(e["c"][1])}" r="{e["r"]}" fill="{k}" fill-opacity="0.45"/>'
        return f'<rect {rect(e["c"], e["w"], e["d"], e.get("a", 0))} fill="{k}" fill-opacity="0.4"/>'
    if t == "boog":
        if e["soort"] == "gordijn":
            a0, a1 = math.radians(e["a0"]), math.radians(e["a1"]); r = e["r"]; c = e["c"]
            return (f'<path d="M{f(c[0]+r*math.cos(a0))} {f(c[1]+r*math.sin(a0))} A{r} {r} 0 0 1 {f(c[0]+r*math.cos(a1))} {f(c[1]+r*math.sin(a1))}" '
                    f'fill="none" stroke="{k}" stroke-width="0.12" stroke-dasharray="0.25 0.12"/>')
        return f'<path d="{arc_sector(e["c"], e["r"] - e["d"], e["r"], e["a0"], e["a1"])}" fill="{k}" fill-opacity="0.8" stroke="{INK}" stroke-width="0.03"/>'
    if t == "ring":
        if e.get("dun"):
            return f'<circle cx="{f(e["c"][0])}" cy="{f(e["c"][1])}" r="{e["r"]}" fill="none" stroke="{INK}" stroke-width="0.06" stroke-dasharray="0.3 0.2"/>'
        g = e["gat"] / 2
        return f'<path d="{arc_sector(e["c"], e["r"] - 0.14, e["r"] + 0.08, e["open"] + g, e["open"] + 360 - g)}" fill="{INK}"/>'
    if t == "toren":
        return toren_svg(e["c"], e["r"], e["open"], e["soort"])
    if t == "plant":
        c, r = e["c"], e["r"]
        return f'<circle cx="{f(c[0])}" cy="{f(c[1])}" r="{r}" fill="#7d9a52" fill-opacity="0.7" stroke="#4d6a3a" stroke-width="0.03"/>'
    if t == "boom":
        c, r = e["c"], e["r"]
        sp = "".join(f'<line x1="{f(c[0])}" y1="{f(c[1])}" x2="{f(c[0]+r*0.85*math.cos(a))}" y2="{f(c[1]+r*0.85*math.sin(a))}" stroke="#4d6a3a" stroke-width="0.03"/>'
                     for a in [i * math.pi / 4 for i in range(8)])
        return f'<circle cx="{f(c[0])}" cy="{f(c[1])}" r="{r}" fill="#9bb07a" fill-opacity="0.55" stroke="#4d6a3a" stroke-width="0.04"/>' + sp
    if t == "v":
        c, L, h, o = e["c"], e["arm"], e["hoek"], e["open"]
        p = [(c[0] + L * math.cos(math.radians(o + 180 - h)), c[1] + L * math.sin(math.radians(o + 180 - h))), (c[0], c[1]),
             (c[0] + L * math.cos(math.radians(o + 180 + h)), c[1] + L * math.sin(math.radians(o + 180 + h)))]
        return f'<polyline points="{pts(p)}" fill="none" stroke="#b9b1a2" stroke-width="0.55"/><polyline points="{pts(p)}" fill="none" stroke="#7f9aa8" stroke-width="0.18"/>'
    return ""


def basis(slug):
    d = json.load(open(os.path.join(HERE, "dossiers", slug + ".json")))
    F = frame(d["footprint"])
    loc = lambda ring: [[round(c, 2) for c in to_local(p, F)] for p in ring]
    n0 = to_local(d["centrum"], F); n1 = to_local((d["centrum"][0], d["centrum"][1] + 10), F)
    noord = math.degrees(math.atan2(n1[1] - n0[1], n1[0] - n0[0]))
    ctx = [dict(ring=loc(c["ring"]), h=c["h"]) for c in d["context"]]
    return d, loc(d["footprint"]), noord, ctx


def gebouwen(O, fp, ctx):
    """Hoofdgebouw plus extra gebouwen op het terrein (uit de context, op index). Geeft (gebouwen, context zonder die gebouwen)."""
    G = [dict(naam="Hoofdgebouw", ring=fp, h=O["hoogte"])]
    weg = set()
    for e in O.get("extra", []):
        c = ctx[e["ctx"]]
        G.append(dict(naam=e["naam"], ring=c["ring"], h=e.get("h", c["h"])))
        weg.add(e["ctx"])
    return G, [c for i, c in enumerate(ctx) if i not in weg]


def centroid(p):
    a = cx = cy = 0
    for i in range(len(p)):
        x0, y0 = p[i]; x1, y1 = p[(i + 1) % len(p)]
        cr = x0 * y1 - x1 * y0; a += cr; cx += (x0 + x1) * cr; cy += (y0 + y1) * cr
    if abs(a) < 1e-9:
        return [sum(x for x, _ in p) / len(p), sum(y for _, y in p) / len(p)]
    return [cx / (3 * a), cy / (3 * a)]


def tekening(slug, niveau=0, breedte=1400):
    O = json.load(open(os.path.join(HERE, "ontwerp", slug + ".json")))
    d, fp, noord, ctx = basis(slug)
    G, ctx = gebouwen(O, fp, ctx)
    xs = [p[0] for g in G for p in g["ring"]]; ys = [p[1] for g in G for p in g["ring"]]
    if niveau == 0:
        for b in O["buiten"]:
            if b["naam"] != "Straat":
                xs += [p[0] for p in b["poly"]]; ys += [p[1] for p in b["poly"]]
    m = 3.0
    # lokaal (u, v) is rechtshandig zoals (oost, noord): v tekenen we omhoog, dus SVG-y = -v
    x0, x1 = min(xs) - m, max(xs) + m
    y0, y1 = -(max(ys) + m + 2.5), -(min(ys) - m - 1.5)
    W, H = x1 - x0, y1 - y0
    head = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{f(x0)} {f(y0)} {f(W)} {f(H)}" width="{breedte}" height="{round(breedte*H/W)}" '
            f'font-family="{FONT}" role="img" aria-label="Plattegrond {O["titel"]}">',
            f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(W)}" height="{f(H)}" fill="#fbf9f4"/>', '<g transform="scale(1,-1)">']
    s = []
    # buurpanden (alleen begane grond)
    if niveau == 0:
        for c in ctx:
            s.append(f'<polygon points="{pts(c["ring"])}" fill="#e7e3da" stroke="#cfc9bd" stroke-width="0.05"/>')
        for b in O["buiten"]:
            s.append(f'<polygon points="{pts(b["poly"])}" fill="{b["kleur"]}" fill-opacity="0.35"/>')
    for g in G:
        s.append(f'<polygon points="{pts(g["ring"])}" fill="#ffffff"/>')
    for z in O["zones"]:
        if z.get("n", 0) == niveau:
            s.append(f'<polygon points="{pts(z["poly"])}" fill="{z["kleur"]}" fill-opacity="0.42"/>')
    ann = []
    s.append('<defs><pattern id="arc" width="0.6" height="0.6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
             f'<line x1="0" y1="0" x2="0" y2="0.6" stroke="#b9b3a6" stroke-width="0.06"/></pattern></defs>')
    for vd in O.get("vides", []):
        if vd["n"] == niveau:
            s.append(f'<polygon points="{pts(vd["poly"])}" fill="url(#arc)"/>')
            c = centroid(vd["poly"])
            ann.append(f'<text x="{f(c[0])}" y="{f(-c[1])}" font-size="0.62" text-anchor="middle" fill="#55514a" font-style="italic">{esc(vd["naam"])}</text>')
    # elementen: eerst vloerachtige, dan meubels, dan torens
    orde = {"kleed": 0, "wand": 5, "deur": 5, "label": 9, "box": 2, "bureau": 2, "cil": 3, "boog": 3, "plant": 4, "boom": 5, "ring": 4, "toren": 6, "v": 3}
    els = [e for e in O["elementen"] if e.get("n", 0) == niveau]
    for e in sorted(els, key=lambda e: orde.get(e["t"], 3)):
        binnen = "c" not in e or any(inside(e["c"], g["ring"]) for g in G)
        if e["t"] != "boom" or niveau == 0 or binnen:
            s.append(element_svg(e))
    # gevel en pui
    for g in G:
        s.append(f'<polygon points="{pts(g["ring"])}" fill="none" stroke="{INK}" stroke-width="0.32" stroke-linejoin="miter"/>')
    if niveau == 0:
        for (a, b) in O["pui"]:
            s.append(f'<line x1="{f(a[0])}" y1="{f(a[1])}" x2="{f(b[0])}" y2="{f(b[1])}" stroke="#fbf9f4" stroke-width="0.24"/>'
                     f'<line x1="{f(a[0])}" y1="{f(a[1])}" x2="{f(b[0])}" y2="{f(b[1])}" stroke="{INK}" stroke-width="0.04"/>')
    for e in els:
        if e["t"] == "label":
            ann.append(f'<text x="{f(e["c"][0])}" y="{f(-e["c"][1] + 0.18)}" font-size="0.42" font-family="{MONO}" text-anchor="middle" fill="#55514a" '
                       f'paint-order="stroke" stroke="#fbf9f4" stroke-width="0.12">{esc(e["tekst"])}</text>')
    s = head + s + ["</g>"] + ann
    # labels
    for z in O["zones"]:
        if z.get("n", 0) != niveau or z["type"] == "entree" and niveau == 0 and z["m2"] < 12:
            continue
        c = z.get("label") or centroid(z["poly"])
        naam = z["naam"].replace("Verdieping: ", "")
        s.append(f'<text x="{f(c[0])}" y="{f(-c[1])}" font-size="0.62" font-weight="600" text-anchor="middle" fill="{INK}" '
                 f'paint-order="stroke" stroke="#fbf9f4" stroke-width="0.16">{esc(naam)}</text>'
                 f'<text x="{f(c[0])}" y="{f(-c[1]+0.75)}" font-size="0.48" font-family="{MONO}" text-anchor="middle" fill="#55514a" '
                 f'paint-order="stroke" stroke="#fbf9f4" stroke-width="0.14">{z["m2"]} m² · {z["palet_naam"].lower()}</text>')
    if niveau == 0:
        for b in O["buiten"]:
            if b["naam"] in ("Straat", "Parkeerplaats en groen"):
                continue
            c = centroid(b["poly"])
            s.append(f'<text x="{f(c[0])}" y="{f(-c[1])}" font-size="0.55" font-style="italic" text-anchor="middle" fill="#3b4a2a">{esc(b["naam"])}</text>')
    # schaalstok en noordpijl
    sx, sy = x0 + 1.2, y1 - 1.0
    for i in range(5):
        s.append(f'<rect x="{f(sx+i)}" y="{f(sy)}" width="1" height="0.22" fill="{INK if i % 2 == 0 else "#fbf9f4"}" stroke="{INK}" stroke-width="0.03"/>')
    s.append(f'<text x="{f(sx)}" y="{f(sy-0.25)}" font-size="0.45" font-family="{MONO}" fill="{INK}">0</text>'
             f'<text x="{f(sx+5)}" y="{f(sy-0.25)}" font-size="0.45" font-family="{MONO}" fill="{INK}" text-anchor="middle">5 m</text>')
    nx, ny = x1 - 1.8, y0 + 2.0
    a = -math.radians(noord)
    tip = (nx + 1.0 * math.cos(a), ny + 1.0 * math.sin(a)); tail = (nx - 0.7 * math.cos(a), ny - 0.7 * math.sin(a))
    l = (nx + 0.4 * math.cos(a + 2.4), ny + 0.4 * math.sin(a + 2.4)); r_ = (nx + 0.4 * math.cos(a - 2.4), ny + 0.4 * math.sin(a - 2.4))
    s.append(f'<polygon points="{pts([tip, l, tail, r_])}" fill="{INK}"/><text x="{f(nx + 1.5*math.cos(a))}" y="{f(ny + 1.5*math.sin(a) + 0.2)}" font-size="0.55" font-weight="600" text-anchor="middle">N</text>')
    titel = "Begane grond" if niveau == 0 else "Verdieping"
    s.append(f'<text x="{f(x0+1.2)}" y="{f(y0+1.6)}" font-size="0.9" font-weight="600" fill="{INK}">{esc(O["titel"])}</text>'
             f'<text x="{f(x0+1.2)}" y="{f(y0+2.4)}" font-size="0.5" font-family="{MONO}" fill="#55514a">{titel.upper()} · ONTWERP NOVEMBER 2026 · INDICATIEF</text>')
    s.append("</svg>")
    return "\n".join(s)


def inside(p, poly):
    x, y = p; c = False
    for i in range(len(poly)):
        x0, y0 = poly[i]; x1, y1 = poly[(i + 1) % len(poly)]
        if (y0 > y) != (y1 > y) and x < (x1 - x0) * (y - y0) / (y1 - y0) + x0:
            c = not c
    return c


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;")


if __name__ == "__main__":
    for slug in json.load(open(os.devnull, "w") and os.path.join(HERE, "ontwerp", "x")) if False else \
            [f[:-5] for f in sorted(os.listdir(os.path.join(HERE, "ontwerp"))) if f.endswith(".json")]:
        O = json.load(open(os.path.join(HERE, "ontwerp", slug + ".json")))
        nivs = [0] + [int(k) for k in O.get("niveaus", {})]
        for n in nivs:
            open(os.path.join(HERE, "ontwerp", f"{slug}-n{n}.svg"), "w").write(tekening(slug, n))
            print(slug, n)
