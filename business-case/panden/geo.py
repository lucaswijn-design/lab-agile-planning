"""Geometrie-hulpjes: lokaal assenstelsel van de hal (u langs de lange as, v haaks)."""
import math


def hull(pts):
    pts = sorted(set(map(tuple, pts)))
    cross = lambda o, a, b: (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def frame(ring):
    """Minimale omsluitende rechthoek -> (origin, hoek) zodat lokale coords >= 0 zijn."""
    h = hull(ring)
    best = None
    for i in range(len(h)):
        a, b = h[i], h[(i+1) % len(h)]
        ang = math.atan2(b[1]-a[1], b[0]-a[0])
        c, s = math.cos(-ang), math.sin(-ang)
        xs = [p[0]*c-p[1]*s for p in h]
        ys = [p[0]*s+p[1]*c for p in h]
        A = (max(xs)-min(xs))*(max(ys)-min(ys))
        if not best or A < best[0]:
            best = (A, ang, min(xs), min(ys), max(xs)-min(xs), max(ys)-min(ys))
    _, ang, mx, my, L, W = best
    if W > L:  # lange as = u
        ang += math.pi/2
        c, s = math.cos(-ang), math.sin(-ang)
        xs = [p[0]*c-p[1]*s for p in h]
        ys = [p[0]*s+p[1]*c for p in h]
        mx, my, L, W = min(xs), min(ys), max(xs)-min(xs), max(ys)-min(ys)
    return dict(ang=ang, mx=mx, my=my, L=L, W=W)


def to_local(p, F):
    c, s = math.cos(-F["ang"]), math.sin(-F["ang"])
    return (p[0]*c-p[1]*s-F["mx"], p[0]*s+p[1]*c-F["my"])


def to_world(q, F):
    x, y = q[0]+F["mx"], q[1]+F["my"]
    c, s = math.cos(F["ang"]), math.sin(F["ang"])
    return (x*c-y*s, x*s+y*c)
