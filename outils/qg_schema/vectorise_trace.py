# -*- coding: utf-8 -*-
"""Vectorise le calque dessiné à main levée (traits rouges = boyaux) en polylignes dans le repère du plan.
Sortie : trace/boyaux_trace.json  [{id, pts:[(x,y)...], tap_a, tap_b, near, deadend_a, deadend_b}]
"""
import sys, json, math
import numpy as np
from PIL import Image
from skimage.morphology import skeletonize, remove_small_objects, binary_closing, disk
from skimage.measure import label
sys.path.insert(0, "/home/claude/qg_schema")
import qg_model as M

SRC = "/home/claude/qg_schema/trace/calque.jpg"
im = Image.open(SRC).convert("RGB"); a = np.asarray(im).astype(int)
H, W = a.shape[:2]; sx, sy = M.W / W, M.H / H
print("calque", W, H, "→ plan", M.W, M.H, "facteur", round(1/sx, 3), round(1/sy, 3))
r, g, b = a[..., 0], a[..., 1], a[..., 2]
red = (r > 170) & (g < 180) & (b < 180) & (r - g > 35)
red = binary_closing(red, disk(3))
red = remove_small_objects(red, 400)
sk = skeletonize(red)
print("squelette :", int(sk.sum()), "pixels")

# --- graphe du squelette : voisinage 8
ys, xs = np.nonzero(sk)
idx = {(int(y), int(x)): i for i, (y, x) in enumerate(zip(ys, xs))}
nb = [[] for _ in idx]
for (y, x), i in idx.items():
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dy == 0 and dx == 0: continue
            j = idx.get((y+dy, x+dx))
            if j is not None: nb[i].append(j)
deg = np.array([len(n) for n in nb])
# nœuds = extrémités (deg 1) et jonctions (deg >= 3) ; on fusionne les amas de jonctions voisins
is_node = (deg != 2)
# parcours des arêtes entre nœuds
visited_edge = set(); edges = []
pts = np.stack([xs, ys], 1).astype(float)
def walk(start, nxt):
    path = [start, nxt]; prev, cur = start, nxt
    while not is_node[cur]:
        cands = [j for j in nb[cur] if j != prev]
        if not cands: break
        prev, cur = cur, cands[0]; path.append(cur)
        if len(path) > 200000: break
    return path
for i in np.nonzero(is_node)[0]:
    for j in nb[i]:
        key = (min(i, j), max(i, j))
        if key in visited_edge: continue
        p = walk(i, j)
        for u, v in zip(p, p[1:]): visited_edge.add((min(u, v), max(u, v)))
        edges.append(p)
print("arêtes brutes :", len(edges))

# --- fusion des nœuds proches (amas de jonction) : on regroupe les nœuds à < 6 px
node_ids = list(np.nonzero(is_node)[0]); node_pos = pts[node_ids]
parent = {n: n for n in node_ids}
def find(u):
    while parent[u] != u: parent[u] = parent[parent[u]]; u = parent[u]
    return u
from scipy.spatial import cKDTree
tree = cKDTree(node_pos)
for u, v in tree.query_pairs(7.0):
    parent[find(node_ids[u])] = find(node_ids[v])
# arêtes simplifiées (Douglas-Peucker) en coordonnées plan
def rdp(P, eps):
    if len(P) < 3: return P
    (x0, y0), (x1, y1) = P[0], P[-1]
    L = math.hypot(x1-x0, y1-y0) or 1e-9
    d = [abs((x1-x0)*(y0-y)-(x0-x)*(y1-y0))/L for x, y in P]
    k = int(np.argmax(d))
    if d[k] > eps:
        return rdp(P[:k+1], eps)[:-1] + rdp(P[k:], eps)
    return [P[0], P[-1]]
# position commune de chaque amas de nœuds (centroïde) : les bouts des arêtes y sont ramenés,
# sinon trois arêtes d'une même jonction finissent sur trois pixels différents et paraissent « libres »
from collections import defaultdict as _dd
_acc = _dd(list)
for n in node_ids: _acc[find(n)].append(pts[n])
CENT = {r: (float(np.mean([q[0] for q in v])*sx), float(np.mean([q[1] for q in v])*sy)) for r, v in _acc.items()}
polys = []
for p in edges:
    P = [(float(pts[i][0]*sx), float(pts[i][1]*sy)) for i in p]
    P[0] = CENT[find(p[0])]; P[-1] = CENT[find(p[-1])]
    L = sum(math.hypot(x1-x0, y1-y0) for (x0, y0), (x1, y1) in zip(P, P[1:]))
    if L < 6: continue   # barbules du squelette
    a_, b_ = find(p[0]), find(p[-1])
    polys.append(dict(pts=rdp(P, 1.6), na=int(a_), nb=int(b_), L=L))
print("arêtes retenues :", len(polys))

# --- taps : extrémité libre (nœud de degré 1 après fusion) proche d'une galerie principale → raccord
# distance au bord de la galerie : demi-largeur sol 13 + paroi 6 = 19
N = M.NODES
def gal_segments():
    segs = []
    for a, b in M.EDGES:
        pl = M.bend_points(a, b) or [N[a], N[b]]
        for p0, p1 in zip(pl, pl[1:]): segs.append(((a, b), p0, p1))
    for n, p in M.STUBS: segs.append(((n, "stub"), N[n], p))
    return segs
SEGS = gal_segments()
def pt_seg(px, py, ax, ay, bx, by):
    dx, dy = bx-ax, by-ay; L2 = dx*dx+dy*dy
    t = 0 if L2 == 0 else max(0, min(1, ((px-ax)*dx+(py-ay)*dy)/L2))
    return math.hypot(px-(ax+t*dx), py-(ay+t*dy)), (ax+t*dx, ay+t*dy)
def nearest_gal(p):
    best = (1e9, None, None)
    for key, q0, q1 in SEGS:
        d, q = pt_seg(p[0], p[1], *q0, *q1)
        if d < best[0]: best = (d, key, q)
    return best
# degré des nœuds fusionnés
from collections import Counter
degc = Counter()
for pl in polys: degc[pl["na"]] += 1; degc[pl["nb"]] += 1
out = []
for k, pl in enumerate(polys):
    P = pl["pts"]; rec = dict(id=f"t{k:03d}", pts=[(round(x, 1), round(y, 1)) for x, y in P], tap_a=None, tap_b=None, near_a=None, near_b=None, free_a=degc[pl["na"]] == 1, free_b=degc[pl["nb"]] == 1)
    for end, key in ((0, "a"), (-1, "b")):
        if not rec["free_" + key]: continue
        d, gk, q = nearest_gal(P[end])
        if gk is None: continue
        if d <= 24:              # touche ou presque la galerie (bord à 19) → raccord posé sur l'axe
            rec["tap_" + key] = list(gk) if gk[1] != "stub" else None
            if rec["tap_" + key]: rec["pts"][end] = (round(q[0]), round(q[1]))
        elif d <= 48:            # s'arrête juste avant → presque-raccord
            rec["near_" + key] = list(gk) if gk[1] != "stub" else None
    out.append(rec)
json.dump(out, open("/home/claude/qg_schema/trace/boyaux_trace.json", "w"), ensure_ascii=False, indent=0)
nt = sum(1 for r in out if r["tap_a"] or r["tap_b"]); nn = sum(1 for r in out if r["near_a"] or r["near_b"])
print("tronçons :", len(out), "| avec raccord :", nt, "| avec presque-raccord :", nn, "| longueur totale :", round(sum(p["L"] for p in polys)), "px plan")
