# -*- coding: utf-8 -*-
"""Nettoyage de la vectorisation du tracé main levée — version « on garde tout ».
Règles :
  - aucun trait n'est supprimé (hors barbules du squelette < 16 px et poussières isolées < 30 px) ;
  - un trait qui passe près d'une salle (< 11 px du mur) n'est pas coupé : le tronçon est RÉTRÉCI (largeur 60 %) ;
  - un trait qui ENTRE dans une salle est arrêté au mur (cul-de-sac contre la paroi, signalé) ;
  - interdits absolus (le trait est arrêté avant) : galerie d'approche du Fiel (30 px), issues secrètes (40 px) ; Fiel et haute sécurité = salles ordinaires (rétréci à < 11 px, arrêté au mur), jamais de raccord ;
  - raccord = tout endroit où le trait touche/croise une galerie principale (bout ou milieu de trait) ;
  - presque-raccord = bout de trait à moins de 60 px d'une galerie, laissé où il est.
Sortie : trace/boyaux_main_levee.json + trace/controle.json (points à montrer)."""
import sys, json, math
sys.path.insert(0, "/home/claude/qg_schema")
import qg_model as M, collisions as C
from collections import defaultdict
T = json.load(open("trace/boyaux_trace.json"))
N = M.NODES

def L(P): return sum(math.hypot(x1-x0, y1-y0) for (x0,y0),(x1,y1) in zip(P,P[1:]))
def key(p): return (round(p[0]/3), round(p[1]/3))
def densify(P, step=4):
    out = [tuple(P[0])]
    for (x0,y0),(x1,y1) in zip(P,P[1:]):
        n = max(1, int(math.hypot(x1-x0,y1-y0)//step))
        for k in range(1, n+1): out.append((x0+(x1-x0)*k/n, y0+(y1-y0)*k/n))
    return out
def rdp(P, eps):
    if len(P) < 3: return P
    (x0,y0),(x1,y1) = P[0], P[-1]; Lx = math.hypot(x1-x0,y1-y0) or 1e-9
    d = [abs((x1-x0)*(y0-y)-(x0-x)*(y1-y0))/Lx for x,y in P]; k = max(range(len(d)), key=lambda i: d[i])
    return rdp(P[:k+1], eps)[:-1] + rdp(P[k:], eps) if d[k] > eps else [P[0], P[-1]]
def merge_chains(segs):
    degm = defaultdict(list)
    for i, P in enumerate(segs): degm[key(P[0])].append(i); degm[key(P[-1])].append(i)
    used = [False]*len(segs); out_ = []
    for i, P0 in enumerate(segs):
        if used[i]: continue
        P = list(P0); used[i] = True
        for direction in (1, -1):
            while True:
                end = P[-1] if direction == 1 else P[0]; k = key(end)
                others = [j for j in degm[k] if not used[j]]
                if len(degm[k]) != 2 or not others: break
                j = others[0]; Q = list(segs[j]); used[j] = True
                if key(Q[0]) != k: Q.reverse()
                P = P + Q[1:] if direction == 1 else Q[::-1][:-1] + P
        out_.append(P)
    return out_

# ---------- 0. soudure des bouts voisins ----------
# un croisement en X de deux traits donne deux jonctions en Y distantes d'une largeur de trait (4-6 px plan) :
# on soude les bouts de tronçons situés à < 6 px (liaison simple, centroïde du groupe) pour qu'ils ne fassent qu'un nœud
segs = [[tuple(q) for q in r["pts"]] for r in T]
from scipy.spatial import cKDTree as _KD
_ends = [P[0] for P in segs] + [P[-1] for P in segs]
_par = list(range(len(_ends)))
def _f(i):
    while _par[i] != i: _par[i] = _par[_par[i]]; i = _par[i]
    return i
for a, b in _KD(_ends).query_pairs(6.0): _par[_f(a)] = _f(b)
_grp = defaultdict(list)
for i, p in enumerate(_ends): _grp[_f(i)].append(p)
_cent = {r: (sum(p[0] for p in v)/len(v), sum(p[1] for p in v)/len(v)) for r, v in _grp.items()}
n_ = len(segs); _w = 0
for i, P in enumerate(segs):
    c0, c1 = _cent[_f(i)], _cent[_f(i+n_)]
    if c0 != P[0]: P[0] = c0; _w += 1
    if c1 != P[-1]: P[-1] = c1; _w += 1
print("bouts soudés :", _w, "| groupes :", sum(1 for v in _grp.values() if len(v) > 1))
segs = [P for P in segs if L(P) > 0.5]

# ---------- 1. barbules + fusion ----------
for it in range(6):
    deg = defaultdict(int)
    for P in segs: deg[key(P[0])] += 1; deg[key(P[-1])] += 1
    keep = []
    for P in segs:
        free = (deg[key(P[0])] == 1) + (deg[key(P[-1])] == 1)
        if free >= 1 and L(P) < 16: continue
        if free == 2 and L(P) < 30: continue
        keep.append(P)
    segs = merge_chains(keep)
print("après barbules :", len(segs), "tronçons,", round(sum(L(P) for P in segs)), "px")

# ---------- 2. géométrie des salles / interdits ----------
polys = {rid: C.room_polys(rid, r) for rid, r in M.ROOMS.items()}
def room_info(p):
    """(rid, dist) de la salle la plus proche ; dist=0 si à l'intérieur."""
    best = (None, 1e9)
    for rid, PP in polys.items():
        for P in PP:
            if C.point_in_poly(p[0], p[1], P): return (rid, 0.0)
            d = min(C.pt_seg_dist(p[0], p[1], *P[k], *P[(k+1) % len(P)]) for k in range(len(P)))
            if d < best[1]: best = (rid, d)
    return best
KEEP = [(N[a], N[b]) for a, b in [("F1","Fa"),("Fa","Fx"),("Fx","HSN")]]   # couloir Fiel ↔ haute sécurité uniquement (la galerie d'approche est autorisée)
def forbidden(p):
    rid, d = room_info(p)
    if any(C.pt_seg_dist(p[0], p[1], *q0, *q1) < 30 for q0, q1 in KEEP): return "couloir Fiel-HS"
    if any(C.pt_seg_dist(p[0],p[1],*q0,*q1) < 40 for sc in M.SECRETS for q0,q1 in zip(sc["pts"], sc["pts"][1:])): return "issue secrète"
    return None

# ---------- 3. arrêt au mur des salles et aux interdits ; marquage des zones étroites ----------
stops = []   # points de contrôle (rouge) : trait arrêté
pieces = []  # (points densifiés, flags étroits par point)
for P in segs:
    D = densify(P, 4); cur = []; cur_narrow = []
    def flush():
        if len(cur) >= 2: pieces.append((list(cur), list(cur_narrow)))
    for p in D:
        why = forbidden(p); rid, d = room_info(p)
        inside = d == 0.0
        if why or inside:
            if cur:
                stops.append(dict(p=cur[-1], why=why or f"mur de {rid}"))
            flush(); cur = []; cur_narrow = []
            continue
        cur.append(p); cur_narrow.append(d < 11)
    flush()
print("après arrêt aux salles :", len(pieces), "tronçons ;", len(stops), "arrêts")

# ---------- 4. traversées de galeries → scission avec raccord des deux côtés ----------
GAL = []
for a, b in M.EDGES:
    pl = M.bend_points(a, b) or [N[a], N[b]]
    for p0, p1 in zip(pl, pl[1:]): GAL.append(((a, b), p0, p1))
def seg_cross_pt(p0, p1, q0, q1):
    (x1,y1),(x2,y2),(x3,y3),(x4,y4) = p0,p1,q0,q1
    den = (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)
    if abs(den) < 1e-9: return None
    t = ((x1-x3)*(y3-y4)-(y1-y3)*(x3-x4))/den; u = -((x1-x2)*(y1-y3)-(y1-y2)*(x1-x3))/den
    if 0 <= t <= 1 and 0 <= u <= 1: return (x1+t*(x2-x1), y1+t*(y2-y1))
    return None
def nearest_gal(p):
    best = (1e9, None, None)
    for k, q0, q1 in GAL:
        d = C.pt_seg_dist(p[0], p[1], *q0, *q1)
        if d < best[0]:
            dx, dy = q1[0]-q0[0], q1[1]-q0[1]; L2 = dx*dx+dy*dy or 1e-9; t = max(0.03, min(0.97, ((p[0]-q0[0])*dx+(p[1]-q0[1])*dy)/L2))
            best = (d, k, (round(q0[0]+t*dx), round(q0[1]+t*dy)))
    return best
split = []
for D, NW in pieces:
    cur = [D[0]]; cur_n = [NW[0]]; tap_start = None
    for (p0, n0), (p1, n1) in zip(zip(D, NW), zip(D[1:], NW[1:])):
        hits = []
        for k, q0, q1 in GAL:
            x = seg_cross_pt(p0, p1, q0, q1)
            if x: hits.append((math.hypot(x[0]-p0[0], x[1]-p0[1]), (round(x[0]), round(x[1])), k))
        hits.sort()
        for _, x, k in hits:
            cur.append(x); cur_n.append(False)
            split.append((cur, cur_n, tap_start, k)); cur = [x]; cur_n = [False]; tap_start = k
        cur.append(p1); cur_n.append(n1)
    split.append((cur, cur_n, tap_start, None))
# un tronçon qui LONGE une galerie (dans sa bande) n'est pas un boyau : on le retire sauf s'il relie deux raccords
def in_band(p): return nearest_gal(p)[0] < 20
final = []
for D, NW, ta, tb in split:
    frac = sum(1 for p in D if in_band(p)) / len(D)
    if frac > 0.7 and not (ta and tb): continue
    # rogner les points de tête/queue situés dans la bande d'une galerie (hors raccord déclaré)
    while len(D) > 2 and ta is None and in_band(D[0]): D.pop(0); NW.pop(0)
    while len(D) > 2 and tb is None and in_band(D[-1]): D.pop(); NW.pop()
    if L(D) < 3 or (L(D) < 10 and not (ta and tb)): continue
    final.append((D, NW, ta, tb))
print("traversées : tronçons", len(final))

# ---------- 5. raccords aux bouts, presque-raccords, puis simplification en gardant les flags ----------
deg = defaultdict(int)
for D, _, _, _ in final: deg[key(D[0])] += 1; deg[key(D[-1])] += 1
FORBID = {frozenset(("Pj","nPs")), frozenset(("F1","Fa")), frozenset(("Fa","Fx")), frozenset(("Fx","HSN"))}
out = []; ctrl_taps = []; ctrl_near = []
for i, (D, NW, ta, tb) in enumerate(final):
    taps = [ta, tb]; near = None
    for end, e in ((0, 0), (1, -1)):
        if taps[end]: continue
        if deg[key(D[e])] != 1: continue
        d, gk, q = nearest_gal(D[e])
        if gk is None or frozenset(gk) in FORBID: continue
        if d <= 30: taps[end] = gk; D[e] = q   # le trait a été dessiné sous la carte : il s'arrête au mur de la galerie → raccord
        elif gk == taps[1-end]: pass   # court moignon qui repart de sa propre galerie : simple cul-de-sac
        elif d <= 60 and end == 1: near = gk
        elif d <= 60 and end == 0:
            D.reverse(); NW.reverse(); taps = [taps[1], taps[0]]; near = gk
    # simplification : RDP sur les points, puis flags « étroit » par segment (vrai si un des points du segment l'était)
    S = rdp(D, 1.8)
    if L(S) < 3: continue
    narrow_pts = {(round(p[0],1), round(p[1],1)) for p, n in zip(D, NW) if n}
    # un segment simplifié est étroit si > 40 % des points densifiés qu'il recouvre sont étroits
    narrow = set()
    for si, (a_, b_) in enumerate(zip(S, S[1:])):
        # étroit dès que le segment simplifié passe à moins de 11 px d'un mur de salle
        if any(room_info(q)[1] < 11 for q in densify([a_, b_], 3)): narrow.add(si)
        # ... ou longe une galerie de trop près (paroi commune amincie)
        elif any(nearest_gal(q)[0] < 20 and math.hypot(q[0]-S[0][0], q[1]-S[0][1]) > 30 and math.hypot(q[0]-S[-1][0], q[1]-S[-1][1]) > 30 for q in densify([a_, b_], 3)): narrow.add(si)
    P = [(round(x,1), round(y,1)) for x, y in S]
    rec = dict(id=f"m{i:03d}", pts=P, tap_a=list(taps[0]) if taps[0] else None, tap_b=list(taps[1]) if taps[1] else None, near=list(near) if near else None, narrow=sorted(narrow))
    out.append(rec)
    for end, k in ((0, "tap_a"), (-1, "tap_b")):
        if rec[k]: ctrl_taps.append(P[end])
    if near: ctrl_near.append(P[-1])
# ---------- 6. aucun réseau isolé : chaque composante connexe doit posséder au moins un raccord ----------
# (règle de l'auteur : « on ne creuse pas un passage à partir de nulle part »)
par = list(range(len(out)))
def fnd(i):
    while par[i] != i: par[i] = par[par[i]]; i = par[i]
    return i
byk = defaultdict(list)
for i, r in enumerate(out):
    for q in (r["pts"][0], r["pts"][-1]): byk[key(q)].append(i)
for ids in byk.values():
    for j in ids[1:]: par[fnd(ids[0])] = fnd(j)
comps = defaultdict(list)
for i in range(len(out)): comps[fnd(i)].append(i)
def crosses_room(p, q):
    return any(room_info(x)[1] < 5.5 for x in densify([p, q], 3)[1:-1])
def gal_candidates(p, kmax=6):
    """galeries les plus proches de p (une entrée par arête), triées par distance"""
    best = {}
    for k, q0, q1 in GAL:
        d = C.pt_seg_dist(p[0], p[1], *q0, *q1)
        if d < best.get(k, (1e9,))[0]:
            dx, dy = q1[0]-q0[0], q1[1]-q0[1]; L2 = dx*dx+dy*dy or 1e-9; t = max(0.03, min(0.97, ((p[0]-q0[0])*dx+(p[1]-q0[1])*dy)/L2))
            best[k] = (d, k, (round(q0[0]+t*dx), round(q0[1]+t*dy)))
    return sorted(best.values())[:kmax]
def ext_clear(p, q, gk):
    """le prolongement p→q ne doit croiser ni frôler une autre galerie, la zone du Fiel ou une issue secrète"""
    for x in densify([p, q], 3)[:-1]:
        dq = math.hypot(x[0]-q[0], x[1]-q[1])
        if dq >= 26:
            for k, q0, q1 in GAL:
                if gk is not None and set(k) == set(gk): continue
                if C.pt_seg_dist(x[0], x[1], *q0, *q1) < 20: return False
        if dq >= 34 and forbidden(x): return False
    return True
ctrl_ext = []; ctrl_bridge = []; isolated = []
# 6a. ponts : un réseau isolé dont un bout libre passe à < 45 px d'un AUTRE boyau y est rattaché (petit trait de jonction)
def comp_of(i): return fnd(i)
def proj_poly(p, P):
    best = (1e9, None)
    for a_, b_ in zip(P, P[1:]):
        d = C.pt_seg_dist(p[0], p[1], *a_, *b_)
        if d < best[0]:
            dx, dy = b_[0]-a_[0], b_[1]-a_[1]; L2 = dx*dx+dy*dy or 1e-9; t = max(0.0, min(1.0, ((p[0]-a_[0])*dx+(p[1]-a_[1])*dy)/L2))
            best = (d, (round(a_[0]+t*dx, 1), round(a_[1]+t*dy, 1)))
    return best
changed = True
while changed:
    changed = False
    comps = defaultdict(list)
    for i in range(len(out)): comps[fnd(i)].append(i)
    for root, ids in list(comps.items()):
        if fnd(ids[0]) != root: continue   # déjà fusionné lors de cette passe
        if any(out[i]["tap_a"] or out[i]["tap_b"] for i in ids): continue
        best = None
        for i in ids:
            for end in (0, -1):
                p = out[i]["pts"][end]
                if len(byk[key(p)]) != 1: continue
                for j, r2 in enumerate(out):
                    if fnd(j) == root: continue
                    d, q = proj_poly(p, r2["pts"])
                    if d < 45 and (best is None or d < best[0]) and nearest_gal(q)[0] > 24 and not crosses_room(p, q) and ext_clear(p, q, None): best = (d, i, end, j, q)
        if best is None: continue
        d, i, end, j, q = best; r = out[i]
        _m = [v for v in out[j]["pts"] if key(v) == key(q)]
        if _m: q = tuple(_m[0])
        if end == 0: r["pts"].insert(0, list(q)); r["narrow"] = [k+1 for k in r["narrow"]]
        else: r["pts"].append(list(q)); r["near"] = None
        # le point q devient un sommet du boyau j (jonction exacte, comme les croisements)
        P2 = out[j]["pts"]; k_ = min(range(len(P2)-1), key=lambda k: C.pt_seg_dist(q[0], q[1], *P2[k], *P2[k+1]))
        if all(key(q) != key(v) for v in P2): P2.insert(k_+1, list(q)); out[j]["narrow"] = [k if k <= k_ else k+1 for k in out[j]["narrow"]] + ([k_+1] if k_ in out[j]["narrow"] else [])
        byk[key(q)].append(i); byk[key(q)].append(j)
        par[fnd(i)] = fnd(j); ctrl_bridge.append(list(q)); changed = True
print("ponts entre réseaux :", len(ctrl_bridge))
comps = defaultdict(list)
for i in range(len(out)): comps[fnd(i)].append(i)
for root, ids in comps.items():
    if any(out[i]["tap_a"] or out[i]["tap_b"] for i in ids): continue
    cands = []
    for i in ids:
        for end in (0, -1):
            p = out[i]["pts"][end]
            if len(byk[key(p)]) != 1: continue      # pas un bout libre
            for d, gk, q in gal_candidates(p):
                if d > 100 or frozenset(gk) in FORBID or crosses_room(p, q): continue
                if not ext_clear(p, q, gk): continue
                cands.append((d, i, end, gk, q)); break
    if not cands:
        print("  !! composante sans issue possible :", [out[i]["id"] for i in ids]); isolated.append([out[i]["pts"] for i in ids]); continue
    d, i, end, gk, q = min(cands)
    r = out[i]
    p = r["pts"][end]; nar_new = any(room_info(x)[1] < 11 for x in densify([p, q], 3))
    if end == 0:
        r["pts"].insert(0, [q[0], q[1]]); r["tap_a"] = list(gk); r["narrow"] = ([0] if nar_new else []) + [k+1 for k in r["narrow"]]
    else:
        r["pts"].append([q[0], q[1]]); r["tap_b"] = list(gk)
        if nar_new: r["narrow"] = sorted(set(r["narrow"]) | {len(r["pts"])-2})
        if r.get("near"): r["near"] = None
    ctrl_taps.append([q[0], q[1]]); ctrl_ext.append([q[0], q[1]])
    ctrl_near[:] = [c for c in ctrl_near if key(c) != key(r["pts"][-1 if end else 0])]
print("réseaux isolés raccordés :", len(ctrl_ext), "(prolongement jusqu'à la galerie la plus proche)")
json.dump(out, open("trace/boyaux_main_levee.json", "w"), ensure_ascii=False)
json.dump(dict(taps=ctrl_taps, near=ctrl_near, stops=stops, ext=ctrl_ext, bridge=ctrl_bridge, isolated=isolated), open("trace/controle.json", "w"), ensure_ascii=False)
nn = sum(1 for r in out if r["narrow"])
print("final :", len(out), "tronçons | raccords :", len(ctrl_taps), "| presque :", len(ctrl_near), "| arrêts au mur :", len(stops), "| tronçons avec passage étroit :", nn)
