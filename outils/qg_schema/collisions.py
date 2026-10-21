# -*- coding: utf-8 -*-
"""Contrôle géométrique : aucune galerie ne doit traverser une salle (hors ses propres accès),
chaque porte doit être sur le mur de sa salle."""
import sys, math
sys.path.insert(0, "/home/claude/qg_schema")
import qg_model as M
from render_final import bbox
HALF = 13 + 6 + 2   # demi-largeur galerie + paroi + marge

def seg_rect_dist(a, b, r):
    x1, y1, x2, y2 = r
    # échantillonnage fin du segment
    (ax, ay), (bx, by) = a, b
    L = math.hypot(bx-ax, by-ay); n = max(2, int(L/3))
    best = 1e9
    for i in range(n+1):
        t = i/n; px, py = ax+(bx-ax)*t, ay+(by-ay)*t
        dx = max(x1-px, 0, px-x2); dy = max(y1-py, 0, py-y2)
        best = min(best, math.hypot(dx, dy))
    return best

def on_boundary(p, r, tol=4):
    x1, y1, x2, y2 = r; px, py = p
    inside_x = x1-tol <= px <= x2+tol; inside_y = y1-tol <= py <= y2+tol
    return inside_x and inside_y and (abs(px-x1) <= tol or abs(px-x2) <= tol or abs(py-y1) <= tol or abs(py-y2) <= tol)

def pt_seg_dist(px, py, ax, ay, bx, by):
    dx, dy = bx-ax, by-ay; L2 = dx*dx+dy*dy
    t = 0 if L2 == 0 else max(0, min(1, ((px-ax)*dx+(py-ay)*dy)/L2))
    return math.hypot(px-(ax+t*dx), py-(ay+t*dy))

def point_in_poly(px, py, poly):
    inside = False; n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]; x2, y2 = poly[(i+1) % n]
        if (y1 > py) != (y2 > py):
            xi = x1 + (py-y1)*(x2-x1)/(y2-y1)
            if px < xi: inside = not inside
    return inside

def seg_poly_dist(a, b, poly):
    (ax, ay), (bx, by) = a, b
    L = math.hypot(bx-ax, by-ay); n = max(2, int(L/3)); best = 1e9
    for i in range(n+1):
        t = i/n; px, py = ax+(bx-ax)*t, ay+(by-ay)*t
        if point_in_poly(px, py, poly): return 0.0
        for k in range(len(poly)):
            best = min(best, pt_seg_dist(px, py, *poly[k], *poly[(k+1) % len(poly)]))
    return best

def parts(r):
    sh = r["shape"]
    if sh[0] == "poly" and len(sh[1]) == 12:   # croix de l'église
        xs = sorted(set(p[0] for p in sh[1])); ys = sorted(set(p[1] for p in sh[1]))
        return [(xs[1], ys[0], xs[2], ys[3]), (xs[0], ys[1], xs[3], ys[2])]
    return [bbox(sh)]

def _ccw(a, b, c): return (c[1]-a[1])*(b[0]-a[0]) > (b[1]-a[1])*(c[0]-a[0])
def seg_cross(a, b, c, d):
    if len({a, b, c, d}) < 4: return False   # extrémité commune = jonction déclarée
    return _ccw(a, c, d) != _ccw(b, c, d) and _ccw(a, b, c) != _ccw(a, b, d)

def crossings():
    N = M.NODES; out = []
    segs = []
    for a, b in M.EDGES:
        pl = edge_polyline(a, b)
        for k, (p0, p1) in enumerate(zip(pl, pl[1:])): segs.append((f"{a}-{b}", a if k == 0 else None, b if k == len(pl)-2 else None, p0, p1))
    for n, p in M.STUBS: segs.append((f"{n}-porte", n, None, N[n], p))
    for i in range(len(segs)):
        for j in range(i+1, len(segs)):
            n1, a1, b1, p0, p1 = segs[i]; n2, a2, b2, q0, q1 = segs[j]
            if n1 == n2: continue
            if {a1, b1} & {a2, b2} - {None}: continue      # jonction déclarée
            if seg_cross(p0, p1, q0, q1): out.append(f"croisement sans jonction : {n1} x {n2}")
    return out

def edge_polyline(a, b):
    N = M.NODES
    pts = M.bend_points(a, b) if hasattr(M, "bend_points") else None
    return pts if pts else [N[a], N[b]]

def run(verbose=True):
    N = M.NODES; problems = []
    stubmap = {}
    for n, p in M.STUBS: stubmap.setdefault(n, []).append(p)
    for rid, r in M.ROOMS.items():
        rb = bbox(r["shape"]); rparts = parts(r)
        own_nodes = {n for n, _ in r["doors"]}
        for a, b in M.EDGES:
            if a in own_nodes or b in own_nodes:
                # une galerie peut aboutir à la porte mais pas traverser : on tolère si une extrémité est la porte
                continue
            pl = edge_polyline(a, b); d = 1e9
            for p0, p1 in zip(pl, pl[1:]):
                if r["shape"][0] == "poly" and len(r["shape"][1]) != 12:
                    d = min(d, seg_poly_dist(p0, p1, r["shape"][1]))
                else:
                    d = min(d, min(seg_rect_dist(p0, p1, rp) for rp in rparts))
            if d < HALF: problems.append(f"{rid}: galerie {a}-{b} à {d:.0f} px (<{HALF})")
        for n, p in M.STUBS:
            if n in own_nodes: continue
            d = seg_rect_dist(N[n], p, rb)
            if d < 13: problems.append(f"{rid}: court couloir {n} à {d:.0f} px")
        # portes
        for n, _ in r["doors"]:
            cands = stubmap.get(n, []) + [N[n]]
            if r["shape"][0] == "circle":
                cx, cy, rr = r["shape"][1:]
                ok = any(abs(math.hypot(p[0]-cx, p[1]-cy)-rr) <= 6 for p in cands)
            elif r["shape"][0] == "poly" and len(r["shape"][1]) != 12:
                poly = r["shape"][1]
                ok = any(min(pt_seg_dist(p[0], p[1], *poly[k], *poly[(k+1) % len(poly)]) for k in range(len(poly))) <= 5 for p in cands)
            else:
                ok = any(any(on_boundary(p, rp) for rp in rparts) for p in cands)
            if not ok:
                problems.append(f"{rid}: porte {n} hors du mur (candidats {cands})")
        # salle ↔ salle
        for rid2, r2 in M.ROOMS.items():
            if rid2 <= rid: continue
            def polyof(rr):
                sh = rr["shape"]
                if rr is M.ROOMS.get("fiel") and hasattr(M, "FIEL_POLY"): return [list(M.FIEL_POLY)]
                if sh[0] == "poly" and len(sh[1]) != 12: return [sh[1]]
                return [[(q[0],q[1]),(q[2],q[1]),(q[2],q[3]),(q[0],q[3])] for q in parts(rr)]
            def shrink(P, d=0.6):
                cx = sum(p[0] for p in P)/len(P); cy = sum(p[1] for p in P)/len(P)
                out = []
                for x, y in P:
                    vx, vy = x-cx, y-cy; L = math.hypot(vx, vy) or 1
                    out.append((x - vx/L*d*1.4, y - vy/L*d*1.4))
                return out
            def overlap(P1, P2):
                P1, P2 = shrink(P1), shrink(P2)
                if any(point_in_poly(x, y, P2) for x, y in P1) or any(point_in_poly(x, y, P1) for x, y in P2): return True
                for i in range(len(P1)):
                    for j in range(len(P2)):
                        if seg_cross(P1[i], P1[(i+1)%len(P1)], P2[j], P2[(j+1)%len(P2)]): return True
                return False
            touching = any(a_ == rid and b_ == rid2 or a_ == rid2 and b_ == rid for a_, b_, _ in M.INTERNAL_DOORS)
            if any(overlap(P1, P2) for P1 in polyof(r) for P2 in polyof(r2)):
                problems.append(f"{rid} chevauche {rid2}")
            elif not touching:
                dmin = 1e9
                for P1 in polyof(r):
                    for P2 in polyof(r2):
                        for p in P1:
                            for k in range(len(P2)): dmin = min(dmin, pt_seg_dist(p[0], p[1], *P2[k], *P2[(k+1) % len(P2)]))
                        for q in P2:
                            for k in range(len(P1)): dmin = min(dmin, pt_seg_dist(q[0], q[1], *P1[k], *P1[(k+1) % len(P1)]))
                if 0.5 < dmin < 8: problems.append(f"{rid} / {rid2} : paroi de roche trop mince ({dmin:.0f} px)")
    problems += crossings()
    for a, b, p in M.INTERNAL_DOORS:
        for rid in (a, b):
            rb = bbox(M.ROOMS[rid]["shape"])
            if not on_boundary(p, rb, tol=2): problems.append(f"porte intérieure {a}/{b} : point {p} hors du mur de {rid}")
    if verbose:
        for p in problems: print("!!", p)
        print(len(problems), "problème(s)")
    return problems

if __name__ == "__main__": run()


# ---------------------------------------------------------------------------
# Galeries annexes (boyaux)
B_ROOM = 10      # distance mini boyau ↔ salle (demi-largeur 5.5 + paroi 3 + un peu de roche)
B_GAL = 18       # distance mini boyau ↔ galerie principale hors raccord
B_KEEP = 10      # zone d'exclusion autour du Fiel et de la haute sécurité (paroi de roche pleine ; aucun raccord possible)
KEEP_ROOMS = ("fiel", "hautesecu")   # seuls le Fiel, sa galerie d'approche (KEEP_EDGES) et la haute sécurité restent interdits
KEEP_EDGES = {("F1","Fa"),("Fa","Fx"),("Fx","HSN"),("Pj","nPs")}   # couloir Fiel ↔ haute sécurité (+ sas Psykos) ; la galerie d'approche du Fiel est autorisée (décision auteur)

def seg_seg_dist(p0, p1, q0, q1):
    if seg_cross(p0, p1, q0, q1) and len({p0, p1, q0, q1}) == 4: return 0.0
    return min(pt_seg_dist(*p0, *q0, *q1), pt_seg_dist(*p1, *q0, *q1), pt_seg_dist(*q0, *p0, *p1), pt_seg_dist(*q1, *p0, *p1))

def room_polys(rid, r):
    sh = r["shape"]
    if rid == "fiel" and hasattr(M, "FIEL_POLY"): return [list(M.FIEL_POLY)]
    if sh[0] == "poly" and len(sh[1]) != 12: return [sh[1]]
    if sh[0] == "circle":
        cx, cy, rr = sh[1:]; return [[(cx+rr*math.cos(2*math.pi*k/24), cy+rr*math.sin(2*math.pi*k/24)) for k in range(24)]]
    return [[(q[0],q[1]),(q[2],q[1]),(q[2],q[3]),(q[0],q[3])] for q in parts(r)]

def seg_polyd(p0, p1, P):
    if any(point_in_poly(x, y, P) for x, y in (p0, p1)): return 0.0
    return min(seg_seg_dist(p0, p1, P[k], P[(k+1) % len(P)]) for k in range(len(P)))

def run_burrows(verbose=True):
    N = M.NODES; problems = []
    B = getattr(M, "BURROWS", [])
    if not B: return []
    # segments principaux
    main = []
    for a, b in M.EDGES:
        pl = edge_polyline(a, b)
        for p0, p1 in zip(pl, pl[1:]): main.append(((a, b), p0, p1))
    for n, p in M.STUBS: main.append(((n, "stub"), N[n], p))
    for pp in M.PRIVATE_PASSAGES:
        for p0, p1 in zip(pp["pts"], pp["pts"][1:]): main.append((("prive", "prive"), p0, p1))
    allpts = {}
    for bw in B:
        for q in bw["pts"]: allpts.setdefault(q, set()).add(bw["id"])
    for bw in B:
        pts = bw["pts"]; segs = list(zip(pts, pts[1:]))
        # taps : les extrémités raccordées doivent être sur l'arête annoncée ; les autres extrémités ne touchent aucune galerie
        for end, tap, p in ((0, bw["tap_a"], pts[0]), (1, bw["tap_b"], pts[-1])):
            if tap:
                if tuple(tap) in KEEP_EDGES or tuple(tap[::-1]) in KEEP_EDGES: problems.append(f"{bw['id']}: raccord interdit sur {tap}")
                pl_ = edge_polyline(*tap)
                if min(pt_seg_dist(*p, *q0, *q1) for q0, q1 in zip(pl_, pl_[1:])) > 1.5: problems.append(f"{bw['id']}: raccord {tap} non posé sur la galerie")
            elif len(allpts[p]) == 1:   # vrai cul-de-sac : loin de tout, sauf « presque-raccord » déclaré
                near = bw.get("near") if end == 1 else None
                if near:
                    pl = edge_polyline(*near); d = min(pt_seg_dist(*p, *q0, *q1) for q0, q1 in zip(pl, pl[1:]))
                    lo, hi = (20, 60) if getattr(M, 'BURROWS_SOURCE', 'auto') == 'main_levee' else (26, 42)
                    if not (lo <= d <= hi): problems.append(f"{bw['id']}: presque-raccord {near} à {d:.0f} px de l'axe (attendu {lo}–{hi})")
                for key, q0, q1 in main:
                    if near and set(key) == set(near): continue
                    if pt_seg_dist(*p, *q0, *q1) < B_GAL: problems.append(f"{bw['id']}: cul-de-sac {p} à {pt_seg_dist(*p,*q0,*q1):.0f} px de la galerie {key}")
        for si, (p0, p1) in enumerate(segs):
            # salles
            for rid, r in M.ROOMS.items():
                d = min(seg_polyd(p0, p1, P) for P in room_polys(rid, r))
                lim = 5.5 if si in bw.get("narrow", ()) else (B_KEEP if rid in KEEP_ROOMS else B_ROOM)   # passage étroit : paroi mince tolérée
                if d < lim: problems.append(f"{bw['id']}: segment {si} à {d:.0f} px de {rid} (<{lim})")
            # galeries principales (hors segment de raccord vis-à-vis de son arête)
            for key, q0, q1 in main:
                is_tap = (si == 0 and bw["tap_a"] and set(key) == set(bw["tap_a"])) or (si == len(segs)-1 and bw["tap_b"] and set(key) == set(bw["tap_b"]))
                # raccord posé sur un nœud de galerie : les arêtes (et amorces) incidentes à ce nœud sont aussi « la galerie de raccord »
                for tp, cond in ((pts[0], si == 0 and bw["tap_a"]), (pts[-1], si == len(segs)-1 and bw["tap_b"])):
                    if cond and key[0] in N and math.hypot(tp[0]-N[key[0]][0], tp[1]-N[key[0]][1]) < 25: is_tap = True
                    if cond and key[1] in N and math.hypot(tp[0]-N[key[1]][0], tp[1]-N[key[1]][1]) < 25: is_tap = True
                d = seg_seg_dist(p0, p1, q0, q1)
                if is_tap:
                    continue
                # tolérance pour le segment voisin du raccord : il part de la galerie
                near_tap = (si == 0 and bw["tap_a"]) or (si == len(segs)-1 and bw["tap_b"])
                # départ en biais : on ignore la partie des segments située à < 32 px du point de raccord
                pp0, pp1 = p0, p1
                for tp, ok in ((pts[0], bw["tap_a"]), (pts[-1], bw["tap_b"])):
                    if not ok: continue
                    d0, d1 = math.hypot(pp0[0]-tp[0], pp0[1]-tp[1]), math.hypot(pp1[0]-tp[0], pp1[1]-tp[1])
                    if d0 < 32 <= d1: t_ = (32-d0)/(d1-d0); pp0 = (pp0[0]+(pp1[0]-pp0[0])*t_, pp0[1]+(pp1[1]-pp0[1])*t_)
                    elif d1 < 32 <= d0: t_ = (32-d1)/(d0-d1); pp1 = (pp1[0]+(pp0[0]-pp1[0])*t_, pp1[1]+(pp0[1]-pp1[1])*t_)
                    elif d0 < 32 and d1 < 32: near_tap = True
                d = seg_seg_dist(pp0, pp1, q0, q1)
                near_miss = si == len(segs)-1 and bw.get("near") and set(key) == set(bw["near"])
                if near_miss:
                    if d < 20: problems.append(f"{bw['id']}: le presque-raccord touche la galerie {key} ({d:.0f} px)")
                    continue
                lim_g = 14 if si in bw.get("narrow", ()) else B_GAL   # passage étroit : paroi commune amincie tolérée
                if d < lim_g and not (near_tap and d > 4):
                    problems.append(f"{bw['id']}: segment {si} à {d:.0f} px de la galerie {key}")
            # issues secrètes : un boyau ne doit pas les frôler
            for sc in M.SECRETS:
                for q0, q1 in zip(sc["pts"], sc["pts"][1:]):
                    if seg_seg_dist(p0, p1, q0, q1) < 40: problems.append(f"{bw['id']}: segment {si} à {seg_seg_dist(p0,p1,q0,q1):.0f} px de l'issue secrète {sc['id']}")
            # autres boyaux : en tracé main levée, les croisements et jonctions sont voulus ; on ne teste rien ici
            if getattr(M, "BURROWS_SOURCE", "auto") != "main_levee":
                for bw2 in B:
                    if bw2["id"] <= bw["id"]: continue
                    for q0, q1 in zip(bw2["pts"], bw2["pts"][1:]):
                        shared = {p0, p1} & {q0, q1}
                        if shared: continue
                        if seg_seg_dist(p0, p1, q0, q1) < 14: problems.append(f"{bw['id']} / {bw2['id']} : trop proches ou croisés hors jonction")
    if verbose:
        for p in problems: print("!!", p)
        print(len(problems), "problème(s) boyaux")
    return problems

if __name__ == "__main__":
    run_burrows()
