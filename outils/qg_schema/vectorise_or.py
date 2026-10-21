# -*- coding: utf-8 -*-
"""Traits dorés du calque = passages secrets vers l'extérieur. Sortie : trace/secrets_or.json [{pts}]"""
import json, math, sys
import numpy as np
from PIL import Image
from skimage.morphology import skeletonize, closing, disk, remove_small_objects
from skimage.measure import label
sys.path.insert(0, "/home/claude/qg_schema"); import qg_model as M
a = np.asarray(Image.open("trace/calque.jpg").convert("RGB")).astype(int); H, W = a.shape[:2]; sx, sy = M.W/W, M.H/H
r, g, b = a[..., 0], a[..., 1], a[..., 2]
gold = (r > 140) & (g > 110) & (g - b > 25) & (r - b > 40) & (r - g < 80)
gold = closing(gold, disk(6)); gold = remove_small_objects(gold, 300)
lab = label(gold); print("composantes :", lab.max())
out = []
for k in range(1, lab.max()+1):
    comp = lab == k
    if comp.sum() < 300: continue
    sk = skeletonize(comp); ys, xs = np.nonzero(sk)
    pts = sorted(zip(xs, ys), key=lambda q: (q[1], q[0]))
    # ordonner le squelette : départ au point le plus proche du bord de l'image ... on part d'une extrémité (voisin unique)
    S = set(zip(xs.tolist(), ys.tolist()))
    def nb(p): return [(p[0]+dx, p[1]+dy) for dx in (-1,0,1) for dy in (-1,0,1) if (dx or dy) and (p[0]+dx, p[1]+dy) in S]
    from collections import deque
    def bfs(src):
        prev = {src: None}; dq = deque([src]); last = src
        while dq:
            cur = dq.popleft(); last = cur
            for q in nb(cur):
                if q not in prev: prev[q] = cur; dq.append(q)
        return last, prev
    e1, _ = bfs(next(iter(S))); e2, prev = bfs(e1)
    path = []; cur = e2
    while cur is not None: path.append(cur); cur = prev[cur]
    # on part du bout intérieur (le plus loin du bord de l'image)
    if min(path[0][0], path[0][1], W-1-path[0][0], H-1-path[0][1]) < min(path[-1][0], path[-1][1], W-1-path[-1][0], H-1-path[-1][1]): path.reverse()
    P = [(x*sx, y*sy) for x, y in path]
    def rdp(P, eps):
        if len(P) < 3: return P
        (x0,y0),(x1,y1) = P[0], P[-1]; L = math.hypot(x1-x0,y1-y0) or 1e-9
        d = [abs((x1-x0)*(y0-y)-(x0-x)*(y1-y0))/L for x,y in P]; i = int(np.argmax(d))
        return rdp(P[:i+1], eps)[:-1] + rdp(P[i:], eps) if d[i] > eps else [P[0], P[-1]]
    P = rdp(P, 2.0)
    out.append(dict(pts=[(round(x,1), round(y,1)) for x, y in P], L=round(sum(math.hypot(q[0]-p[0], q[1]-p[1]) for p, q in zip(P, P[1:])))))
    print(k, "longueur", out[-1]["L"], "de", out[-1]["pts"][0], "à", out[-1]["pts"][-1])
json.dump(out, open("trace/secrets_or.json", "w"))
