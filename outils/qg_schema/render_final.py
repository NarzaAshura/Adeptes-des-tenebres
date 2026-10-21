# -*- coding: utf-8 -*-
"""
Rendu FINAL : SVG autonome et interactif du QG des Adorateurs des Ténèbres,
construit à partir des mêmes données de topologie que le schéma de validation.
- aucune ressource externe, aucun script ; style inline ; groupes <g class="hot">
- décor en pointer-events:none, zones cliquables au-dessus
"""
import math, random, sys, html
sys.path.insert(0, "/home/claude/qg_schema")
import qg_model as M
from render_schema import build_graph, check, centroid

CW = 26          # largeur de galerie (sol)
WT = 6           # épaisseur de paroi dessinée
SW = 18          # largeur des courts couloirs
P = dict(
    rock="#0f0e13", rock2="#17161d", rock3="#1d1b24",
    wall="#9a93a8", wall_dark="#5e586b",
    floor="#4b4852", floor2="#55515c", room="#3d3a45", room_est="#463a43",
    etabli="#c2606f", bureau="#a97be0", special="#6aa06a", secondaire="#9a95a6",
    service="#4fb3a3", cabale="#d19a4a", garde="#b8b25a", main="#c94a7a",
    door="#e3cf8e", secret="#f0b43c", text="#f1e8cf", text_dim="#b9b0a0",
    poison="#6f9e2d", poison2="#9fd141", blood="#8c1f2f", wood="#8a5a3c", linen="#d9d2c3",
    iron="#6c6f78", water="#4f7f9b",
)
rng = random.Random(42)

def esc(t): return html.escape(t, quote=True)

def bbox(shape):
    t = shape[0]
    if t == "rect": return shape[1], shape[2], shape[3], shape[4]
    if t == "circle": cx, cy, r = shape[1:]; return cx-r, cy-r, cx+r, cy+r
    xs = [p[0] for p in shape[1]]; ys = [p[1] for p in shape[1]]
    return min(xs), min(ys), max(xs), max(ys)

def shape_el(shape, fill, stroke, sw, extra=""):
    t = shape[0]
    if t == "rect":
        x1, y1, x2, y2 = shape[1:]
        return f'<rect x="{x1}" y="{y1}" width="{x2-x1}" height="{y2-y1}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'
    if t == "circle":
        cx, cy, r = shape[1:]
        return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'
    pts = " ".join(f"{x},{y}" for x, y in shape[1])
    return f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'

def text(x, y, s, size=13, weight="bold", fill=None, anchor="middle", dim=False):
    fill = fill or (P["text_dim"] if dim else P["text"])
    s = esc(s)
    return (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" '
            f'fill="none" stroke="{P["rock"]}" stroke-width="4" stroke-linejoin="round">{s}</text>'
            f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{fill}">{s}</text>')

def rect(x, y, w, h, fill, stroke="none", sw=1, rx=0, op=1):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" opacity="{op}"/>'

def circ(x, y, r, fill, stroke="none", sw=1, op=1):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" opacity="{op}"/>'

# ---------------------------------------------------------------------------
# Mobilier par salle (sobre)
# ---------------------------------------------------------------------------
def bed(x, y, w=16, h=26, vertical=True):
    if not vertical: w, h = h, w
    o = [rect(x, y, w, h, P["wood"], P["rock"], 1, 2), rect(x+2, y+2, w-4, h-4, P["linen"])]
    if vertical: o.append(rect(x+2, y+2, w-4, 6, "#c9b7a2"))
    else: o.append(rect(x+2, y+2, 6, h-4, "#c9b7a2"))
    return "".join(o)

def crate(x, y, s=10):
    return rect(x, y, s, s, P["wood"], P["rock"], 1) + f'<line x1="{x}" y1="{y}" x2="{x+s}" y2="{y+s}" stroke="{P["rock"]}" stroke-width="0.8"/>'

def torch(x, y, rh=16):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rh}" fill="url(#halo)"/>' + circ(x, y, 2.6, "#ffd27a")

def irregular(rid, r):
    """Polygone irrégulier inscrit dans le rectangle d'une salle secondaire ; les coins proches d'une porte restent droits."""
    sh = r["shape"]
    if sh[0] != "rect" or not (r["kind"] == "secondaire" or rid.startswith("ev_")): return sh
    x1, y1, x2, y2 = sh[1:]
    doors = []
    stubmap = {}
    for n, p in M.STUBS: stubmap.setdefault(n, []).append(p)
    for n, _ in r["doors"]:
        doors += stubmap.get(n, []) + [M.NODES[n]]
    rr = random.Random(sum(map(ord, rid)))
    corners = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]
    pts = []
    for i, (cx, cy) in enumerate(corners):
        near = any(math.hypot(cx-dx, cy-dy) < 34 for dx, dy in doors)
        if near or rr.random() < 0.35:
            pts.append((cx, cy)); continue
        c = 10 + rr.random()*16
        nx, ny = corners[(i+1) % 4], corners[(i-1) % 4]
        # deux points : vers le coin suivant et vers le coin précédent
        p_prev = (cx + (ny[0]-cx)/abs(ny[0]-cx)*c if ny[0] != cx else cx, cy + (ny[1]-cy)/abs(ny[1]-cy)*c if ny[1] != cy else cy)
        p_next = (cx + (nx[0]-cx)/abs(nx[0]-cx)*c if nx[0] != cx else cx, cy + (nx[1]-cy)/abs(nx[1]-cy)*c if nx[1] != cy else cy)
        pts += [p_prev, p_next]
    return ("poly", pts)

def furniture(rid, r):
    sh = r["shape"]; x1, y1, x2, y2 = bbox(sh); w, h = x2-x1, y2-y1; cx, cy = (x1+x2)/2, (y1+y2)/2
    o = []
    if rid == "eglise":
        # piliers au croisement
        for px, py in [(x1+135*M.SCALE, y1+100*M.SCALE), (x2-135*M.SCALE, y1+100*M.SCALE), (x1+135*M.SCALE, y2-100*M.SCALE), (x2-135*M.SCALE, y2-100*M.SCALE)]:
            pass
        # bancs de pierre : branche sud et bras est/ouest
        top_south = cy + 50*M.SCALE
        for i in range(6):
            yy = top_south + i*18
            o.append(rect(cx-52, yy, 44, 8, "#7d7570", P["rock"], 1)); o.append(rect(cx+8, yy, 44, 8, "#7d7570", P["rock"], 1))
        for sx in (x1+14, x2-14-60):
            for i in range(3):
                o.append(rect(sx, cy-28+i*20, 60, 8, "#7d7570", P["rock"], 1))
        # dalle sacrificielle (nord) + présentoir + 5 sièges en demi-cercle
        ay = y1 + 62*M.SCALE
        o.append(rect(cx-30, ay-12, 60, 24, "#6c8ea8", P["rock"], 1.5, 2))
        o.append(rect(cx-22, ay-8, 44, 4, P["blood"], op=0.8))
        o.append(rect(cx-10, ay-34, 20, 10, "#8a8580", P["rock"], 1))
        for k in range(5):
            a = math.pi*(0.2 + 0.6*k/4)
            sx, sy = cx - 54*math.cos(a), y1 + 30 + 22*math.sin(a)
            o.append(rect(sx-6, sy-6, 12, 12, "#5a3a4a", P["rock"], 1, 2))
        for px, py in [(x1+40, y1+40), (x2-40, y1+40), (cx-45, cy), (cx+45, cy), (x1+40, y2-40), (x2-40, y2-40)]:
            o.append(torch(px, py))
    elif rid == "habitations":
        NR = M.DORM_ROWS; cw = 30*M.SCALE; mx = cx; rowh = (h-20*M.SCALE)/NR; dw = mx-cw/2-x1-8
        o.append(rect(mx-cw/2, y1, cw, h, P["floor"]))
        for i in range(NR):
            yy = y1 + 10*M.SCALE + i*rowh
            for k, sx in enumerate((x1+6, mx+cw/2+4)):
                o.append(rect(sx, yy+2, dw, rowh-5, P["room_est"], P["wall_dark"], 1.2))
                bx = sx+4 if k == 0 else sx+dw-4-14
                lab = f"D{(i+1) if k==0 else (i+1+NR):02d}"
                o.append(bed(bx, yy+5, 14, rowh-12))

                nx = sx+dw-10 if k == 0 else sx+5
                o.append(rect(nx, yy+rowh/2-3, 6, 6, P["wood"]))
                dx = (mx-cw/2) if k == 0 else (mx+cw/2)
                o.append(rect(dx-2.5, yy+rowh/2-6, 5, 12, P["door"]))
                o.append(text(sx+dw/2, yy+rowh/2+3, lab, 8, "normal", dim=True))
    elif rid == "hautesecu":
        mx = cx; rowh = (h-30*M.SCALE/1.35)/5
        o.append(rect(mx-20, y1, 40, h-8, "#2c2a31"))
        rowh = (h-26)/5
        for i in range(5):
            yy = y1+18+i*rowh
            for k, sx in enumerate((x1+6, mx+22)):
                cwid = (mx-20-x1-6) if k == 0 else (x2-6-(mx+22))
                o.append(rect(sx, yy, cwid, rowh-5, "#26242b", P["iron"], 1.2))
                o.append(rect(sx+3 if k == 0 else sx+cwid-9, yy+3, 6, rowh-11, "#5a5448"))
                dx = (mx-20) if k == 0 else (mx+20)
                o.append(rect(dx-2.5, yy+rowh/2-7, 5, 12, P["iron"]))
        o.append(torch(mx, y1+10))
    elif rid == "infirmerie":
        for k in range(3):
            o.append(bed(x1+16+k*34, y1+14, 18, 34))
        o.append(rect(x2-44, y1+14, 30, 22, "#c9d2d6", P["rock"], 1, 3))
        o.append(circ(x2-29, y1+25, 5, "#d9534f"))
        o.append(rect(x1+16, y2-30, 60, 14, P["wood"], P["rock"], 1))
        o.append(torch(cx, y1+8))
    elif rid == "citerne":
        ccx, ccy, rr = sh[1:]
        o.append(circ(ccx, ccy, rr-12, "#36333d", P["wall_dark"], 1.5))
        for k in range(1, 4): o.append(circ(ccx, ccy, (rr-12)*k/4, "none", "#44414b", 1))
        for k in range(7):
            a = k*0.9; o.append(circ(ccx+(rr-40)*math.cos(a), ccy+(rr-40)*math.sin(a), 9, "#8c7a3a", op=0.55))
        o.append(circ(ccx-30, ccy+28, 8, "#5d6b74", P["rock"], 1)); o.append(circ(ccx-12, ccy+36, 8, "#5d6b74", P["rock"], 1))
        o.append(crate(ccx+22, ccy+26)); o.append(crate(ccx+34, ccy+20))
        o.append(rect(ccx+rr-26, ccy-6, 8, 12, P["iron"]))  # robinet
    elif rid == "fiel":
        ccx, ccy, rr = sh[1:]
        rf = random.Random(7)
        def blob(radius, n, jit, dx=0, dy=0):
            pts = []
            for k in range(n):
                a = 2*math.pi*k/n + rf.random()*0.25
                d = radius*(1-jit+2*jit*rf.random())
                pts.append(f"{ccx+dx+d*math.cos(a):.1f},{ccy+dy+d*math.sin(a):.1f}")
            return " ".join(pts)
        # berge rocheuse, puis parois de la fosse, puis mare de poison : contours irréguliers
        o.append(f'<polygon points="{blob(rr-12, 14, 0.08)}" fill="#2a3a16" stroke="#415a22" stroke-width="2"/>')
        o.append(f'<polygon points="{blob(rr-28, 12, 0.12)}" fill="{P["poison"]}"/>')
        o.append(f'<polygon points="{blob(rr-46, 10, 0.18, 5, -3)}" fill="{P["poison2"]}" opacity="0.7"/>')
        for k in range(9):
            a = k*0.7+0.3; d = (rr-56)*rf.random()
            o.append(circ(ccx+d*math.cos(a), ccy+d*math.sin(a), 2+3*rf.random(), "#c6e86a", op=0.6))
        # sente de bord (sud-ouest), de l'arrivée Fa au départ Fx, le long de la berge
        a1 = math.atan2(M.NODES["Fa"][1]-ccy, M.NODES["Fa"][0]-ccx); a2 = math.atan2(M.NODES["Fx"][1]-ccy, M.NODES["Fx"][0]-ccx)
        steps = 12; pts = []
        for k in range(steps+1):
            t = k/steps; a = a1 + (a2-a1)*t if a2 > a1 else a1 - (a1-a2)*t
            rp = rr-7 + 3*math.sin(t*6.3)
            pts.append(f"{ccx+rp*math.cos(a):.1f},{ccy+rp*math.sin(a):.1f}")
        o.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="#716d7c" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>')
        o.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{P["wall_dark"]}" stroke-width="2" stroke-dasharray="4 6"/>')
        for ex, ey in [(ccx-rr+22, ccy+rr-58), (ccx+rr-30, ccy-rr+40)]:
            o.append(circ(ex, ey, 1.6, "#ffd54a")); o.append(circ(ex+6, ey, 1.6, "#ffd54a"))
    elif rid == "reserve":
        for k in range(3):
            o.append(rect(x1+8, y1+8+k*18, 28, 8, P["wood"], P["rock"], 1))
        o.append(rect(x2-40, y1+10, 26, 16, "#b58a3c", P["rock"], 1, 2))
        for k in range(4): o.append(crate(x1+44+k*12, y2-20, 9))
    elif rid == "psykos":
        o.append(rect(cx-36, cy-16, 72, 32, "#3a2a4a", P["rock"], 1.5, 3))
        o.append(rect(cx-28, cy-10, 22, 14, "#e9dcc0", op=0.8)); o.append(rect(cx+4, cy-12, 20, 16, "#d8c9a8", op=0.8))
        o.append(circ(x2-34, y2-34, 22, "none", "#8b6cc0", 1.5)); o.append(circ(x2-34, y2-34, 10, "none", "#8b6cc0", 1))
        for k in range(8):
            a = k*math.pi/4; o.append(f'<line x1="{x2-34}" y1="{y2-34}" x2="{x2-34+22*math.cos(a):.1f}" y2="{y2-34+22*math.sin(a):.1f}" stroke="#8b6cc0" stroke-width="1"/>')
        o.append(rect(x1+10, y1+12, 14, 30, "#6b4b7e", P["rock"], 1, 2)); o.append(rect(x1+10, y2-40, 30, 12, P["wood"], P["rock"], 1))
        o.append(torch(cx, y1+10))
    elif rid == "pape":
        o.append(rect(cx-30, cy-10, 60, 26, "#5a3a22", P["rock"], 1.5, 3))
        o.append(rect(cx-24, cy-6, 18, 12, "#e9dcc0", op=0.8)); o.append(rect(cx+6, cy-6, 16, 12, "#8fb0c8", op=0.8))
        o.append(rect(x1+18, y1+18, 40, 14, "#2e1f2a", P["rock"], 1)); o.append(circ(x1+28, y1+14, 2.2, "#f0a640", op=0.5)); o.append(circ(x1+48, y1+14, 2.2, "#f0a640", op=0.5))
        o.append(rect(x2-40, y2-40, 24, 22, "#4a3a5a", P["rock"], 1, 2))
    elif rid in ("pape_chambre", "psykos_annexe") or rid.startswith("cab_c") or rid.startswith("ev_") and rid not in ("ev_wc", "ev_sdb", "ev_salon"):
        o.append(bed(x1+6, y1+6, 16, min(h-12, 28)))
        o.append(rect(x1+26, y1+6, 8, 8, P["wood"]))
        if w > 60: o.append(rect(x2-26, y2-16, 20, 10, P["wood"], P["rock"], 1))
    elif rid.endswith("_sdb") or rid in ("cab_sdb", "ev_sdb"):
        o.append(rect(x1+5, y1+5, min(26, w/2-6), h-10, "#c9d2d6", P["rock"], 1, 4))
        o.append(circ(x2-12, cy, 5, "#dfe6ea", P["rock"], 1)); o.append(rect(x2-24, y1+5, 10, 8, "#dfe6ea", P["rock"], 1, 2))
    elif rid.startswith("wc_") or rid in ("cab_wc", "ev_wc"):
        n = max(1, int(w//16))
        for k in range(n): o.append(circ(x1+9+k*16, cy, 4.5, "#dfe6ea", P["rock"], 1))
    elif rid.startswith("douches"):
        n = max(1, int(w//14))
        for k in range(n): o.append(circ(x1+8+k*14, cy, 3, "#8fb0c8")); o.append(circ(x1+8+k*14, cy, 6, "#8fb0c8", op=0.25))
    elif rid == "salle_vie":
        o.append(rect(cx-24, cy-8, 48, 16, P["wood"], P["rock"], 1, 2))
        for k in range(4): o.append(rect(cx-22+k*13, cy+12, 8, 8, "#6b4b3a", P["rock"], 1))
        o.append(rect(x1+8, y1+8, 10, 24, "#5a3a4a", P["rock"], 1, 2))
    elif rid == "self":
        for k in range(3): o.append(rect(x1+12+k*(w-24)/3, cy-7, (w-24)/3-8, 14, P["wood"], P["rock"], 1))
    elif rid == "cuisines":
        o.append(rect(x1+6, y1+6, w-12, 10, P["iron"], P["rock"], 1)); o.append(circ(x1+14, y1+11, 3, "#f0a640")); o.append(circ(x1+26, y1+11, 3, "#f0a640"))
    elif rid in ("reserve_cuisine",):
        for k in range(3): o.append(crate(x1+6+k*12, cy-5, 9))
    elif rid == "buanderie":
        for k in range(3): o.append(circ(x1+12+k*16, cy-6, 6, "#c9d2d6", P["rock"], 1))
        o.append(f'<line x1="{x1+6}" y1="{y2-12}" x2="{x2-6}" y2="{y2-12}" stroke="{P["linen"]}" stroke-width="1.2"/>')
    elif rid in ("cab_salon", "ev_salon"):
        o.append(rect(cx-26, cy-7, 52, 14, "#5a3a4a", P["rock"], 1, 3))
        for k in range(2): o.append(rect(x1+10+k*(w-30), cy-6, 10, 12, "#6b4b3a", P["rock"], 1, 2))
    elif r["kind"] == "garde":
        o.append(rect(cx-10, cy-5, 20, 10, P["wood"], P["rock"], 1)); o.append(rect(x1+5, y1+5, 6, 14, P["iron"])); o.append(torch(x2-8, y1+8))
    elif rid == "cellules":
        # geôles : deux rangées de cases à barreaux autour d'un couloir central
        mx = cx; o.append(rect(mx-16, y1, 32, h, P["floor"]))
        n = 3; rowh = (h-16)/n
        for i in range(n):
            yy = y1+8+i*rowh
            for k, sx in enumerate((x1+6, mx+18)):
                cwid = (mx-18-x1-6) if k == 0 else (x2-6-(mx+18))
                o.append(rect(sx, yy, cwid, rowh-6, "#2e262b", P["iron"], 1))
                bx = (mx-18) if k == 0 else (mx+18)
                for b in range(4):
                    o.append(f'<line x1="{bx-1 if k==0 else bx+1}" y1="{yy+2+b*(rowh-8)/3}" x2="{bx-1 if k==0 else bx+1}" y2="{yy+2+b*(rowh-8)/3+3}" stroke="{P["iron"]}" stroke-width="1.5"/>')
                o.append(f'<line x1="{bx}" y1="{yy}" x2="{bx}" y2="{yy+rowh-6}" stroke="{P["iron"]}" stroke-width="2" stroke-dasharray="2 3"/>')
        o.append(torch(cx, y1+6)); o.append(torch(cx, y2-6))
    elif rid == "main":
        F = M.MAIN_FRAME; Wf = F["W"]; s0c, s1c, d0c, d1c = F["cor"]; cd0, cd1 = F["cell_d"]
        pts = " ".join(f"{x},{y}" for x, y in (Wf(s0c, d0c), Wf(s1c, d0c), Wf(s1c, d1c), Wf(s0c, d1c)))
        o.append(f'<polygon points="{pts}" fill="{P["floor"]}"/>')
        for lab, a_, b_ in F["cells"]:
            cp = " ".join(f"{x},{y}" for x, y in (Wf(a_, cd0), Wf(b_, cd0), Wf(b_, cd1), Wf(a_, cd1)))
            o.append(f'<polygon points="{cp}" fill="#2e262b" stroke="{P["wall_dark"]}" stroke-width="1.2"/>')
            m = (a_+b_)/2
            dx, dy = Wf(m, cd0); o.append(rect(dx-3, dy-3, 6, 6, P["door"], P["rock"], 0.8, 1))
            if lab.startswith("Main"):
                # paillasse (le long de la paroi) + guéridon
                p1, p2, p3, p4 = Wf(a_+4, cd0+9), Wf(a_+13, cd0+9), Wf(a_+13, cd1-4), Wf(a_+4, cd1-4)
                o.append(f'<polygon points="{p1[0]},{p1[1]} {p2[0]},{p2[1]} {p3[0]},{p3[1]} {p4[0]},{p4[1]}" fill="#8a7a5a" stroke="{P["rock"]}" stroke-width="0.8"/>')
                gx, gy = Wf(b_-7, cd1-8); o.append(circ(gx, gy, 3.2, P["wood"], P["rock"], 0.8))
                tx, ty = Wf(m, cd1+10); o.append('<g class="lbl-s">' + text(tx, ty, lab, 7, "normal", dim=True) + '</g>')
            elif lab == "WC":
                cx_, cy_ = Wf(m, (cd0+cd1)/2); o.append(circ(cx_, cy_, 4, "#dfe6ea", P["rock"], 1))
            else:
                cx_, cy_ = Wf(m, (cd0+cd1)/2); o.append(circ(cx_, cy_, 3, "#8fb0c8")); o.append(circ(cx_, cy_, 6, "#8fb0c8", op=0.25))
        tx, ty = Wf((s0c+s1c)/2, (d0c+d1c)/2+3); ax_, ay_ = Wf(0, 0); bx_, by_ = Wf(100, 0)
        ang = math.degrees(math.atan2(by_-ay_, bx_-ax_))
        o.append(f'<g class="lbl-s" transform="rotate({ang:.1f} {tx} {ty})">' + text(tx, ty, "AILE DE LA MAIN — garde rapprochée de Psykos", 8, "bold") + '</g>')
        o.append(f'<g class="lbl-synth" transform="rotate({ang:.1f} {tx} {ty})">' + text(tx, ty, "LA MAIN", 10, "bold") + '</g>')
    elif rid == "S17":   # forge (secteur est)
        o.append(rect(x1+8, y1+8, 32, 26, "#4a3a32", P["rock"], 1.5, 2)); o.append(circ(x1+24, y1+21, 7, "#f0a640")); o.append(circ(x1+24, y1+21, 14, "#f0a640", op=0.25))
        o.append(rect(x1+52, y1+16, 16, 9, P["iron"], P["rock"], 1)); o.append(rect(cx-16, y2-24, 44, 12, P["wood"], P["rock"], 1))
        o.append(rect(x2-26, y1+10, 12, 28, "#5d6b74", P["rock"], 1, 3))
        for k in range(3): o.append(f'<line x1="{x2-4}" y1="{y1+14+k*6}" x2="{x2+4}" y2="{y1+14+k*6}" stroke="{P["iron"]}" stroke-width="1.5"/>')   # grille d'évacuation des fumées
        o.append(text(x2+6, y1+40, "évent", 7, "normal", dim=True, anchor="start"))
    elif rid == "S21":   # atelier (réparations)
        o.append(rect(x1+10, y1+10, 40, 12, P["wood"], P["rock"], 1)); o.append(rect(x1+56, y1+8, 14, 8, P["iron"], P["rock"], 1))
        o.append(f'<line x1="{x1+14}" y1="{y1+30}" x2="{x1+30}" y2="{y1+40}" stroke="{P["iron"]}" stroke-width="2"/>')
    elif rid == "S21_old":
        o.append(rect(x1+8, y1+8, 30, 24, "#4a3a32", P["rock"], 1.5, 2)); o.append(circ(x1+23, y1+20, 6, "#f0a640")); o.append(circ(x1+23, y1+20, 12, "#f0a640", op=0.25))
        o.append(rect(x1+48, y1+14, 14, 8, P["iron"], P["rock"], 1)); o.append(rect(cx+10, cy+4, 40, 12, P["wood"], P["rock"], 1))
        o.append(rect(x2-24, y1+10, 10, 26, "#5d6b74", P["rock"], 1, 3))
    elif rid == "ecoute":
        o.append(rect(cx-26, cy-6, 52, 14, "#3a3a4a", P["rock"], 1, 2))
        for k in range(3): o.append(rect(cx-22+k*17, cy-3, 10, 7, "#8fb0c8", op=0.9))
        o.append(f'<line x1="{cx+30}" y1="{cy-16}" x2="{cx+30}" y2="{cy-2}" stroke="{P["iron"]}" stroke-width="1.5"/><circle cx="{cx+30}" cy="{cy-18}" r="2" fill="{P["door"]}"/>')
    elif rid == "conseil":
        o.append(f'<ellipse cx="{cx}" cy="{cy}" rx="30" ry="18" fill="#4a3a3a" stroke="{P["rock"]}" stroke-width="1.5"/>')
        for k in range(10):
            a = 2*math.pi*k/10 + math.pi/10; o.append(rect(cx+42*math.cos(a)-4, cy+30*math.sin(a)-4, 8, 8, "#5a3a4a", P["rock"], 1, 2))
        for k in range(4):
            a = math.pi/4 + k*math.pi/2; o.append(torch(cx+50*math.cos(a), cy+50*math.sin(a), 14))
    elif rid == "remise_so":   # salle des pompes / puits
        o.append(circ(cx-10, cy, 12, "#2a2a33", P["wall"], 2)); o.append(circ(cx-10, cy, 7, P["water"]))
        o.append(rect(cx+8, cy-12, 10, 24, P["iron"], P["rock"], 1, 2)); o.append(f'<line x1="{cx+13}" y1="{cy-12}" x2="{cx+26}" y2="{cy-22}" stroke="{P["iron"]}" stroke-width="2.5"/>')
    elif rid == "garde_manger":
        for k in range(4): o.append(circ(x1+9+k*13, cy, 4, "#9a7a4a", P["rock"], 1))
    elif rid == "entrainement":
        for k in range(3): o.append(circ(x1+40+k*44, cy-10, 7, "#7a6a55", P["rock"], 1.2))   # mannequins / cibles
        o.append(circ(cx+30, cy+28, 22, "none", "#8a7f74", 1.5)); o.append(circ(cx+30, cy+28, 8, "none", "#8a7f74", 1))
        o.append(rect(x1+12, y2-26, 34, 10, P["wood"], P["rock"], 1))
        o.append(torch(x1+14, y1+14)); o.append(torch(x2-14, y1+14))
    elif rid == "S03":
        for k in range(3): o.append(rect(x1+6, y1+6+k*9, w-12, 5, P["wood"], P["rock"], 0.8))
    elif rid == "pape_reduit":
        o.append(crate(x1+8, y1+8)); o.append(crate(x1+20, y1+8)); o.append(rect(x1+8, y2-20, 30, 10, P["wood"], P["rock"], 1))
    else:
        # salle secondaire : 1-3 caisses ou une table, déterministe
        rr = random.Random(sum(map(ord, rid)))
        k = rr.randint(1, 3)
        if sh[0] == "poly":
            for i in range(k): o.append(crate(cx-20+i*13, cy-18+(i % 2)*3, 9))
            return "".join(o)
        for i in range(k):
            o.append(crate(x1+8+i*13, y1+8+(i % 2)*3, 9))
        if w > 60 and rr.random() > 0.5: o.append(rect(cx-12, cy+4, 24, 10, P["wood"], P["rock"], 1))
        if rr.random() > 0.5: o.append(torch(x2-9, y2-9))
    return "".join(o)

# ---------------------------------------------------------------------------
# Étiquettes
# ---------------------------------------------------------------------------
LABEL_POS = {  # positions avant mise à l'échelle (x, y) -> converties
    "habitations": (110, 237), "fiel": (1400, 128), "hautesecu": (1345, 560), "eglise": (800, 548),
    "citerne": (300, 1005), "reserve": (800, 90), "pape": (100, 690), "psykos": (1015, 60), "psykos_vest": (1097, 118), "garde_sud": (800, 1085),
    "cellules": (1060, 595), "pape_vest": (182, 606), "pape_chambre": (82, 560), "pape_sdb": (82, 512), "psykos_sdb": (927, 167),
    "S20": (1232, 120),
}
def label_xy(rid, r):
    if rid in LABEL_POS:
        x, y = LABEL_POS[rid]; return x*M.SCALE, (y+M.OY)*M.SCALE
    return centroid(r["shape"])

def label_size(rid, r):
    if r["kind"] in ("etabli", "special") or rid in ("pape", "psykos"): return 15
    if rid in ("pape_vest", "pape_reduit", "pape_chambre", "psykos_annexe", "reserve", "pape_sdb", "psykos_sdb", "cab_salon"): return 10
    if r["kind"] in ("service", "cabale", "garde") or rid.startswith("douches") or rid.startswith("wc_"): return 9
    return 11

DISPLAY = {"reserve": "RÉSERVE / TRÉSOR", "citerne": "CITERNE (sèche)", "habitations": "HABITATIONS (D01–D16)"}

# ---------------------------------------------------------------------------
def render(path):
    N, E, R = M.NODES, M.EDGES, M.ROOMS
    W, H = M.W, M.H
    o = []
    o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Georgia, \'DejaVu Serif\', serif" role="img" aria-labelledby="titre">')
    o.append('<title id="titre">Corrésone — Repaire des Adorateurs des Ténèbres (plan du niveau principal)</title>')
    o.append('<style>'
             '.decor{pointer-events:none}'
             '.hot{cursor:pointer;outline:none}'
             '.hot .zone{fill:#ffffff;fill-opacity:0;stroke:#f0b43c;stroke-width:0;transition:stroke-width .15s,fill-opacity .15s}'
             '.hot:hover .zone,.hot:focus .zone{stroke-width:4;fill-opacity:.08}'
             '.hot-tbd .zone{stroke-dasharray:6 4}'
             'svg.synthese .lbl-s{display:none}'
             '.lbl-synth{display:none} svg.synthese .lbl-synth{display:inline}'
             'svg.atlas-font, svg.atlas-font text{font-family:inherit}'
             '</style>')
    # --- définitions (dégradé de torche, dallages)
    o.append('<defs>'
             '<radialGradient id="halo"><stop offset="0" stop-color="#f6b24a" stop-opacity="0.55"/><stop offset="0.45" stop-color="#f0a640" stop-opacity="0.18"/><stop offset="1" stop-color="#f0a640" stop-opacity="0"/></radialGradient>'
             f'<pattern id="dalles" width="22" height="22" patternUnits="userSpaceOnUse"><rect width="22" height="22" fill="{P["room_est"]}"/><path d="M0 11 H22 M11 0 V11 M0 11 V22 M22 11 V22" stroke="#3a2f36" stroke-width="1"/><path d="M0 22 H22 M0 0 V11" stroke="#3a2f36" stroke-width="1"/></pattern>'
             '<pattern id="chaux" width="16" height="16" patternUnits="userSpaceOnUse"><rect width="16" height="16" fill="#6a6670"/><path d="M0 8 H16 M8 0 V16" stroke="#5e5a66" stroke-width="0.8"/></pattern>'
             f'<pattern id="terre" width="14" height="14" patternUnits="userSpaceOnUse"><rect width="14" height="14" fill="{P["room"]}"/><circle cx="4" cy="5" r="0.9" fill="#4a4650"/><circle cx="11" cy="10" r="0.7" fill="#4a4650"/></pattern>'
             '</defs>')
    # --- fond de roche
    o.append(f'<rect width="{W}" height="{H}" fill="{P["rock"]}"/>')
    o.append('<g class="decor" id="roche">')
    for i in range(720):
        x, y = rng.random()*W, rng.random()*H
        r_ = 12+rng.random()*48; n = rng.randint(5, 8)
        pts = []
        for k in range(n):
            a = 2*math.pi*k/n + rng.random()*0.5; d = r_*(0.6+0.5*rng.random())
            pts.append(f"{x+d*math.cos(a):.0f},{y+d*math.sin(a):.0f}")
        col = P["rock2"] if rng.random() > 0.5 else P["rock3"]
        o.append(f'<polygon points="{" ".join(pts)}" fill="{col}" opacity="0.9"/>')
    for i in range(90):   # fissures
        x, y = rng.random()*W, rng.random()*H; pts = [f"{x:.0f},{y:.0f}"]
        for k in range(rng.randint(2, 4)):
            x += (rng.random()-0.5)*60; y += (rng.random()-0.5)*60; pts.append(f"{x:.0f},{y:.0f}")
        o.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="#0a090d" stroke-width="1.2" opacity="0.8"/>')
    o.append('</g>')

    # --- galeries : parois puis sol
    def seg(a, b, w, c, cap="round"):
        (x1, y1), (x2, y2) = N[a], N[b]
        bp = M.bend_points(a, b)
        if bp:
            mx, my = bp[len(bp)//2]; cx_, cy_ = 2*mx-(x1+x2)/2, 2*my-(y1+y2)/2
            return f'<path d="M{x1},{y1} Q{cx_:.1f},{cy_:.1f} {x2},{y2}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="{cap}"/>'
        return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}" stroke-linecap="{cap}"/>'
    # --- galeries annexes (boyaux de roche brute) : sous les galeries principales
    import random as _rb
    def rough(pts, jit, seed):
        """Tronçons légèrement tremblés (boyau irrégulier), extrémités fixes : liste de polylignes, une par segment."""
        rr = _rb.Random(seed); segs = []
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            L = math.hypot(x1-x0, y1-y0); n = max(1, int(L//22)); out = [(x0, y0)]
            for k in range(1, n):
                t = k/n; nx, ny = -(y1-y0)/L, (x1-x0)/L; j = (rr.random()-0.5)*2*jit
                out.append((x0+(x1-x0)*t+nx*j, y0+(y1-y0)*t+ny*j))
            out.append((x1, y1)); segs.append(out)
        return segs
    o.append('<g class="decor" id="boyaux">')
    BW, BWT = M.BURROW_W, M.BURROW_WT
    def chaikin(pts, n=2):
        P = list(pts)
        for _ in range(n):
            if len(P) < 3: break
            Q = [P[0]]
            for (x0, y0), (x1, y1) in zip(P, P[1:]):
                Q.append((0.75*x0+0.25*x1, 0.75*y0+0.25*y1)); Q.append((0.25*x0+0.75*x1, 0.25*y0+0.75*y1))
            Q.append(P[-1]); P = Q
        return P
    HAND = getattr(M, "BURROWS_SOURCE", "auto") == "main_levee"
    BF = "#34303b"      # sol des boyaux (roche nue, plus sombre que les galeries dallées)
    def _k3(q): return (round(q[0]/2), round(q[1]/2))
    _ENDCOUNT = {}
    for _b in getattr(M, "BURROWS", []):
        for _q in _b["pts"]: _ENDCOUNT[_k3(_q)] = _ENDCOUNT.get(_k3(_q), 0) + 1
    def _shared_end(bw, end):
        return _ENDCOUNT.get(_k3(end), 0) > 1
    def ribbon(pl, w_fn, seed, jit=0.9):
        """Ruban à largeur variable autour de la polyligne pl : liste de sommets du polygone (gauche puis droite inversée).
        w_fn(k, n) → largeur au sommet k ; bords légèrement tremblés (boyau creusé à la main)."""
        rr = _rb.Random(seed); n = len(pl)
        # bruit lisse pour le tremblé des bords : marche aléatoire moyennée
        def smooth_noise(m):
            raw = [(rr.random()-0.5)*2 for _ in range(m)]
            return [sum(raw[max(0, k-2):k+3])/len(raw[max(0, k-2):k+3]) for k in range(m)]
        nl, nr = smooth_noise(n), smooth_noise(n)
        L_, R_ = [], []
        for k, (x, y) in enumerate(pl):
            (xa, ya) = pl[max(0, k-1)]; (xb, yb) = pl[min(n-1, k+1)]
            tx, ty = xb-xa, yb-ya; tl = math.hypot(tx, ty) or 1e-9; nx, ny = -ty/tl, tx/tl
            h = w_fn(k, n)/2
            L_.append((x+nx*(h+nl[k]*jit), y+ny*(h+nl[k]*jit))); R_.append((x-nx*(h+nr[k]*jit), y-ny*(h+nr[k]*jit)))
        def _rdp(Pq, eps):
            if len(Pq) < 3: return Pq
            (x0, y0), (x1, y1) = Pq[0], Pq[-1]; Lq = math.hypot(x1-x0, y1-y0) or 1e-9
            d = [abs((x1-x0)*(y0-y)-(x0-x)*(y1-y0))/Lq for x, y in Pq]; k = max(range(len(d)), key=lambda i: d[i])
            return _rdp(Pq[:k+1], eps)[:-1] + _rdp(Pq[k:], eps) if d[k] > eps else [Pq[0], Pq[-1]]
        return _rdp(L_, 0.35) + _rdp(R_[::-1], 0.35)
    def width_fn(bw, pl, base_full, base_narrow, seed):
        """largeur par sommet du lissé : gabarit (étroit ou non) × ondulation 0.86–1.14 × effilement aux culs-de-sac"""
        rr = _rb.Random(seed); n = len(pl); P0 = bw["pts"]; nar = set(bw.get("narrow", ()))
        # abscisse curviligne cumulée + correspondance sommet lissé → segment d'origine (par projection)
        cum = [0.0]
        for (x0, y0), (x1, y1) in zip(pl, pl[1:]): cum.append(cum[-1] + math.hypot(x1-x0, y1-y0))
        total = cum[-1] or 1e-9
        def seg_of(q):
            return min(range(len(P0)-1), key=lambda s: pt_seg_dist(q[0], q[1], *P0[s], *P0[s+1])) if len(P0) > 2 else 0
        segidx = [seg_of(q) for q in pl]
        # ondulation lente : somme de deux sinus de phase aléatoire
        ph1, ph2 = rr.random()*6.283, rr.random()*6.283; f1, f2 = 1/(70+rr.random()*50), 1/(23+rr.random()*20)
        taper_a = not bw["tap_a"] and not _shared_end(bw, P0[0]); taper_b = not bw["tap_b"] and not _shared_end(bw, P0[-1])
        out_ = []
        for k in range(n):
            base = base_narrow if segidx[k] in nar else base_full
            wav = 1 + 0.09*math.sin(cum[k]*6.283*f1+ph1) + 0.05*math.sin(cum[k]*6.283*f2+ph2)
            tap_ = 1.0
            if taper_a and cum[k] < 16: tap_ = min(tap_, 0.55 + 0.45*cum[k]/16)
            if taper_b and total-cum[k] < 16: tap_ = min(tap_, 0.55 + 0.45*(total-cum[k])/16)
            out_.append(base*wav*tap_)
        return out_
    def pt_seg_dist(px, py, ax, ay, bx, by):
        dx, dy = bx-ax, by-ay; L2 = dx*dx+dy*dy
        t_ = 0 if L2 == 0 else max(0, min(1, ((px-ax)*dx+(py-ay)*dy)/L2))
        return math.hypot(px-(ax+t_*dx), py-(ay+t_*dy))
    _RIB = {}
    def bw_lines(bw, i, w_full, w_narrow, color):
        if HAND:
            if i not in _RIB:
                pl = chaikin(bw["pts"], 3)
                W_ = width_fn(bw, pl, BW, BW*0.6, 300+i)
                _RIB[i] = (pl, W_)
            pl, W_ = _RIB[i]
            extra = (w_full - BW)          # 0 pour le sol, 2*BWT pour la paroi
            poly = ribbon(pl, lambda k, n: W_[k] + extra, 400+i, jit=0.9 if extra == 0 else 1.3)
            pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in poly)
            o.append(f'<polygon points="{pts}" fill="{color}" stroke="{color}" stroke-width="0.8" stroke-linejoin="round"/>')
            return
        for si, sg in enumerate(rough(bw["pts"], 2.2, 100+i)):
            w = w_narrow if si in bw.get("narrow", ()) else w_full
            pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in sg)
            o.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="{w:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')
    for i, bw in enumerate(getattr(M, "BURROWS", [])): bw_lines(bw, i, BW+2*BWT, BW*0.6+2*BWT, P["wall_dark"])
    def _seal(color, extra):
        """disque au droit de chaque bout partagé (jonction entre tronçons) pour masquer la couture entre rubans"""
        if not HAND: return
        for i, bw in enumerate(M.BURROWS):
            pl, W_ = _RIB[i]
            for end, k in ((bw["pts"][0], 0), (bw["pts"][-1], -1)):
                if _shared_end(bw, end):
                    o.append(circ(end[0], end[1], (W_[k]+extra)/2, color))
    _seal(P["wall_dark"], 2*BWT)
    for i, bw in enumerate(getattr(M, "BURROWS", [])):
        bw_lines(bw, i, BW, BW*0.6, BF)
    _seal(BF, 0)
    for i, bw in enumerate(getattr(M, "BURROWS", [])):
        pl = chaikin(bw["pts"]) if HAND else [q for sg in rough(bw["pts"], 2.2, 100+i) for q in sg]
        # éboulis / cailloux épars
        rr = _rb.Random(200+i)
        for (x, y) in pl[::3]:
            if rr.random() < 0.35: o.append(circ(x+(rr.random()-0.5)*4, y+(rr.random()-0.5)*4, 0.7+rr.random()*0.8, "#4a4652"))
        # cul-de-sac : petit éboulement
        for end, tap in ((bw["pts"][0], bw["tap_a"]), (bw["pts"][-1], bw["tap_b"])):
            shared = sum(1 for b2 in M.BURROWS for q in b2["pts"] if q == end) > 1
            if not tap and not shared:
                for k in range(5):
                    o.append(circ(end[0]+(rr.random()-0.5)*9, end[1]+(rr.random()-0.5)*9, 1.4+rr.random()*1.6, P["wall_dark"]))
    o.append('</g>')
    o.append('<g class="decor" id="galeries">')
    for a, b in E: o.append(seg(a, b, CW+2*WT, P["wall"]))
    for n, p in M.STUBS:
        (x1, y1), (x2, y2) = N[n], p
        o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{P["wall"]}" stroke-width="{SW+2*WT}" stroke-linecap="butt"/>')
    for pp in M.PRIVATE_PASSAGES:
        pts = " ".join(f"{x},{y}" for x, y in pp["pts"])
        o.append(f'<polyline class="passage-prive" points="{pts}" fill="none" stroke="{P["wall_dark"]}" stroke-width="{M.BURROW_W+2*M.BURROW_WT}" stroke-linecap="butt"/>')
    # renfoncement sans torche devant le Fiel
    fx, fy = N["Fa"]; f1x, f1y = N["F1"]
    o.append(f'<ellipse cx="{(fx*0.6+f1x*0.4):.0f}" cy="{(fy*0.6+f1y*0.4):.0f}" rx="34" ry="24" fill="{P["wall"]}"/>')
    for a, b in E: o.append(seg(a, b, CW, P["floor"]))
    for n, p in M.STUBS:
        (x1, y1), (x2, y2) = N[n], p
        o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{P["floor"]}" stroke-width="{SW}" stroke-linecap="round"/>')
    for pp in M.PRIVATE_PASSAGES:
        pts = " ".join(f"{x},{y}" for x, y in pp["pts"])
        o.append(f'<polyline class="passage-prive" points="{pts}" fill="none" stroke="{BF}" stroke-width="{M.BURROW_W}" stroke-linecap="butt"/>')
    o.append(f'<ellipse cx="{(fx*0.6+f1x*0.4):.0f}" cy="{(fy*0.6+f1y*0.4):.0f}" rx="28" ry="18" fill="#3a3740"/>')
    o.append('<g class="decor" id="boyaux-ouvertures">')
    # ouvertures des boyaux dans la paroi des galeries : on re-dessine le sol du boyau sur ses derniers 30 px,
    # par-dessus le mur de la galerie → brèche visible, sol du boyau qui rejoint le sol de la galerie
    def _tail(pl, frm_end, lo=CW/2-1, hi=CW/2+WT+9):
        """Portion de la polyligne située entre lo et hi px (abscisse curviligne) du point de raccord ; le raccord est en dernier."""
        P_ = list(pl) if frm_end == "b" else list(pl)[::-1]   # P_[-1] = point de raccord
        R_ = P_[::-1]; out_ = []; acc = 0.0
        def at(p, q, s): 
            d = math.hypot(q[0]-p[0], q[1]-p[1]); t_ = s/d if d else 0; return (p[0]+(q[0]-p[0])*t_, p[1]+(q[1]-p[1])*t_)
        for p, q in zip(R_, R_[1:]):
            d = math.hypot(q[0]-p[0], q[1]-p[1])
            if acc + d > lo and not out_: out_.append(at(p, q, lo-acc))
            if out_ and acc + d >= hi: out_.append(at(p, q, hi-acc)); break
            if out_: out_.append(q)
            acc += d
        return out_[::-1]
    for bw in getattr(M, "BURROWS", []):
        pl = chaikin(bw["pts"]) if HAND else bw["pts"]
        nseg = len(bw["pts"])-1
        for end, tap, nar in (("a", bw["tap_a"], 0 in bw.get("narrow", ())), ("b", bw["tap_b"], (nseg-1) in bw.get("narrow", ()))):
            if not tap: continue
            T_ = _tail(pl, end); w = M.BURROW_W*0.6 if nar else M.BURROW_W
            pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in T_)
            o.append(f'<polyline points="{pts}" fill="none" stroke="{P["wall_dark"]}" stroke-width="{w+2*M.BURROW_WT:.1f}" stroke-linecap="butt" stroke-linejoin="round"/>')
            o.append(f'<polyline points="{pts}" fill="none" stroke="{BF}" stroke-width="{w:.1f}" stroke-linecap="butt" stroke-linejoin="round"/>')
            # seuil : petit éboulis clair au débouché
            if len(T_) < 2: continue
            tx, ty = T_[-1]
            rr_ = _rb.Random(hash((bw["id"], end)) & 0xffff)
            for k in range(3): o.append(circ(tx+(rr_.random()-0.5)*8, ty+(rr_.random()-0.5)*8, 0.9+rr_.random()*0.9, "#4a4652"))
    o.append('</g>')
    for a, b in E: o.append(seg(a, b, 8, P["floor2"]))   # bande d'usure au centre
    # dallage discret des galeries (points)
    for a, b in E:
        pl = M.bend_points(a, b) or [N[a], N[b]]
        for (x1, y1), (x2, y2) in zip(pl, pl[1:]):
            L = math.hypot(x2-x1, y2-y1)
            for k in range(max(1, int(L//34))):
                t = (k+0.5)*34/L if L > 34 else 0.5
                o.append(circ(x1+(x2-x1)*t, y1+(y2-y1)*t, 1.2, P["floor2"]))
    # torches le long des galeries (aux jonctions principales)
    for n in ("N1", "S1", "J1", "J2", "Pj", "r2c", "r2e", "r2g", "r2i", "r3h", "r3c", "SW1", "S3", "Na", "NEa", "r1c", "r1e", "r1g", "r1i", "CSa", "CNa", "r3k", "r3b", "r3f", "r3e", "r3d", "sNE", "sSE", "sSW", "sNW"):
        if n not in N: continue
        x, y = N[n]; o.append(torch(x, y, 22))
    o.append('</g>')

    # --- salles
    o.append('<g class="decor" id="ombres" opacity="0.55">')
    for rid, r in R.items():
        shp = ("poly", M.FIEL_POLY) if rid == "fiel" else irregular(rid, r)
        o.append(f'<g transform="translate(4,5)">{shape_el(shp, "#000", "none", 0)}</g>')
    o.append('</g>')
    o.append('<g class="decor" id="salles">')
    for rid, r in R.items():
        k = r["kind"]; col = P[k]
        fill = P["room_est"] if k in ("etabli", "bureau", "special") else P["room"]
        if rid == "eglise": fill = "url(#dalles)"
        elif rid == "infirmerie": fill = "url(#chaux)"
        elif k == "secondaire": fill = "url(#terre)"
        elif rid in ("citerne",): fill = "#3b3942"
        elif rid == "hautesecu": fill = "#2a272e"
        if rid == "fiel":
            pts = " ".join(f"{x},{y}" for x, y in M.FIEL_POLY)
            o.append(f'<polygon points="{pts}" fill="{fill}" stroke="{col}" stroke-width="4"/>')
        else:
            o.append(shape_el(irregular(rid, r), fill, col, 4))
        o.append(furniture(rid, r))
    o.append('</g>')

    # --- ouvertures (brèches dans les parois) + vantaux
    o.append('<g class="decor" id="portes">')
    stubmap = {}
    for n, p in M.STUBS: stubmap.setdefault(n, []).append(p)
    def opening(p, big=False):
        x, y = p
        return circ(x, y, 10 if big else 8.5, P["floor"]) + rect(x-3, y-3, 6, 6, P["door"], P["rock"], 0.8, 1)
    for rid, r in R.items():
        if rid == "fiel": continue
        for node, _ in r["doors"]:
            pts = stubmap.get(node)
            if pts:
                # choisir le stub le plus proche de la salle
                bx1, by1, bx2, by2 = bbox(r["shape"])
                cxr, cyr = (bx1+bx2)/2, (by1+by2)/2
                p = min(pts, key=lambda q: (q[0]-cxr)**2+(q[1]-cyr)**2)
            else:
                p = N[node]
            o.append(opening(p, rid in ("eglise", "hautesecu")))
    for a, b, p in M.INTERNAL_DOORS: o.append(opening(p))
    for pp in M.PRIVATE_PASSAGES: o.append(opening(pp["door_a"])); o.append(opening(pp["door_b"]))
    o.append('</g>')

    # --- passages secrets
    o.append('<g class="decor" id="secrets">')
    for s in M.SECRETS:
        if getattr(M, "SECRETS_HAND", False):
            # tracé de l'auteur : boyau au gabarit étroit, paroi sombre + sol teinté or discret
            pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in chaikin(s["pts"]))
            o.append(f'<polyline points="{pts}" fill="none" stroke="{P["wall_dark"]}" stroke-width="{BW*0.6+2*BWT:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')
            o.append(f'<polyline points="{pts}" fill="none" stroke="#5a4a2a" stroke-width="{BW*0.6:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')
            o.append(f'<polyline points="{pts}" fill="none" stroke="{P["secret"]}" stroke-width="1.6" stroke-dasharray="6 6" stroke-linecap="round" opacity="0.85"/>')
            continue
        pts = " ".join(f"{x},{y}" for x, y in s["pts"])
        o.append(f'<polyline points="{pts}" fill="none" stroke="{P["secret"]}" stroke-width="4" stroke-dasharray="9 7" stroke-linecap="round" opacity="0.9"/>')
        ex, ey = s["pts"][-1]
        lx, ly = {"secret_pape": (14, ey+26), "secret_psykos": (ex+8, ey+30), "secret_cabale": (ex+14, 16)}[s["id"]]
        o.append(text(lx, ly, "passage secret " + s["note"], 10, "normal", P["secret"], "start"))
    o.append('</g>')

    # --- prolongements
    o.append('<g class="decor" id="prolongements">')
    for aid, (node, lab, note) in M.ACCES.items():
        x, y = N[node]
        o.append(f'<path d="M{x-9},{y-6} L{x},{y+10} L{x+9},{y-6}" fill="none" stroke="{P["door"]}" stroke-width="2.5" stroke-linecap="round"/>')
        o.append(text(x, y+34, lab, 14))
        o.append(text(x, y+50, note, 10, "normal", dim=True))
    o.append('</g>')

    # --- étiquettes
    o.append('<g class="decor" id="etiquettes">')
    for rid, r in R.items():
        x, y = label_xy(rid, r); fs = label_size(rid, r)
        lab = DISPLAY.get(rid, r["label"])
        lines = lab.split("|")
        cls = ' class="lbl-s"' if fs <= 11 and r["kind"] not in ("etabli", "special") else ""
        o.append(f'<g{cls}>')
        for i, ln in enumerate(lines):
            o.append(text(x, y+4+i*fs*1.2-(len(lines)-1)*fs*0.6, ln, fs, "bold" if fs >= 11 else "normal"))
        o.append('</g>')
    o.append('</g>')

    # --- puits d'aération (décor, non praticables)
    o.append('<g class="decor" id="aerations">')
    for ax_, ay_ in M.AERATIONS:
        o.append(circ(ax_, ay_, 9, "#1c1a21", P["wall_dark"], 2))
        for k in (-4, 0, 4): o.append(f'<line x1="{ax_-7}" y1="{ay_+k}" x2="{ax_+7}" y2="{ay_+k}" stroke="{P["iron"]}" stroke-width="1.4"/>')
        o.append(text(ax_, ay_+20, "aération", 8, "normal", dim=True))
    o.append('</g>')
    # --- annotations d'atlas
    o.append('<g class="decor" id="annotations">')
    ex, ey = centroid(R["eglise"]["shape"]); o.append(text(ex, ey+26, "4 accès : N · O · E · S", 10, "normal", dim=True))
    o.append(text(ex, ey+42, "5 sièges : 4 Cabalistes + Pape Sombre", 9, "normal", dim=True))
    fx_, fy_ = N["Fa"]; o.append(text(fx_-30, fy_-30, "renfoncement sans torche", 9, "normal", dim=True, anchor="end"))
    fcx, fcy, fr = R["fiel"]["shape"][1:]; o.append(text(fcx, fcy+fr+18, "chemin longeant la fosse (≈ 20 pas)", 9, "normal", dim=True))
    hx, hy = N["Fx"]; h2x, h2y = N["HSN"]; o.append(text((hx+h2x)/2+14, (hy+h2y)/2, "passage obligé", 9, "normal", dim=True, anchor="start"))
    pjx, pjy = N["Pj"]; o.append(text(pjx+8, pjy-24, "seule galerie d'approche du Fiel →", 9, "normal", dim=True, anchor="start"))
    o.append('</g>')
    # --- titre + légende
    o.append('<g class="decor" id="cartouche">')
    o.append(text(W/2, 30, "CORRÉSONE — REPAIRE DES ADORATEURS DES TÉNÈBRES", 22))
    o.append(text(W/2, 50, "niveau principal · plan d'atlas · les secteurs en pointillés sont des propositions non attestées par les récits", 11, "normal", dim=True))
    lx, ly = W-640, H-150
    o.append(rect(lx-12, ly-22, 630, 140, P["rock"], P["wall_dark"], 1, 4, 0.92))
    L = [("etabli", "lieu attesté par les récits"), ("bureau", "bureaux et appartements (1 entrée + 1 secret)"),
         ("special", "Fiel / haute sécurité (passage obligé)"), ("secondaire", "salle secondaire (fonction proposée, non canon)"),
         ("service", "ajouts demandés (service, entraînement, conseil…)"), ("cabale", "quartier des Cabalistes et des Évêques (proposition)"), ("garde", "poste de garde (proposition)"), ("main", "aile de la Main (garde de Psykos)")]
    for i, (k, t) in enumerate(L):
        xx = lx + (0 if i < 4 else 330); yy = ly + (i % 4)*22 if i < 8 else ly + 4*22
        o.append(rect(xx, yy-9, 18, 12, P["room"], P[k], 3)); o.append(text(xx+26, yy+1, t, 10, "normal", anchor="start"))
    yy = ly + 4*22
    o.append(rect(lx, yy-9, 6, 6, P["door"])); o.append(text(lx+26, yy, "porte / ouverture", 10, "normal", anchor="start"))
    o.append(f'<line x1="{lx+150}" y1="{yy-6}" x2="{lx+190}" y2="{yy-6}" stroke="{P["secret"]}" stroke-width="3" stroke-dasharray="7 5"/>'); o.append(text(lx+198, yy, "passage secret (proposition)", 10, "normal", anchor="start"))
    o.append(f'<line x1="{lx+380}" y1="{yy-6}" x2="{lx+420}" y2="{yy-6}" stroke="{P["wall"]}" stroke-width="12"/><line x1="{lx+380}" y1="{yy-6}" x2="{lx+420}" y2="{yy-6}" stroke="{P["floor"]}" stroke-width="7"/>'); o.append(text(lx+428, yy, "galerie", 10, "normal", anchor="start"))
    o.append('</g>')

    # --- zones interactives (au-dessus de tout)
    o.append('<g id="interactif">')
    def hot(lid, name, shape, tbd=False, lx=None, ly=None):
        cls = "hot hot-tbd" if tbd else "hot"
        g = [f'<g class="{cls}" data-lieu="{lid}" tabindex="0" role="button" aria-label="{esc(name)}">']
        g.append(f'<title>{esc(name)}</title>')
        g.append(shape_el(shape, "#fff", "#f0b43c", 0, 'class="zone"'))
        if lx is None: lx, ly = centroid(shape)
        g.append(f'<text x="{lx}" y="{ly}" font-size="1" fill="none">{esc(name)}</text>')
        g.append('</g>')
        return "".join(g)
    main_ids = {"eglise": "Église souterraine", "reserve": "Réserve / Trésor", "cellules": "Cellules des sacrifices",
                "fiel": "Oubliettes du Fiel", "hautesecu": "Quartier de haute sécurité", "habitations": "Habitations (D01–D16)",
                "infirmerie": "Infirmerie", "citerne": "Citerne", "pape": "Bureau du Pape Sombre", "psykos": "Bureau de Sœur Psykos"}
    for lid, name in main_ids.items():
        o.append(hot(lid, name, ("poly", M.FIEL_POLY) if lid == "fiel" else R[lid]["shape"]))
    # bureaux : chambres, salles de bain, vestibule, réduit
    for lid, name in [("pape_vest", "Vestibule du Pape Sombre"), ("pape_chambre", "Chambre du Pape Sombre"), ("pape_sdb", "Salle de bain du Pape Sombre"),
                      ("pape_reduit", "Réduit du Pape Sombre (départ du passage secret)"), ("psykos_annexe", "Chambre de Sœur Psykos"), ("psykos_sdb", "Salle de bain de Sœur Psykos"), ("psykos_vest", "Vestibule de Sœur Psykos")]:
        o.append(hot(lid, name, R[lid]["shape"], tbd=True))
    # aile de service : un seul groupe (enveloppe)
    svc = [r for k, r in R.items() if r["kind"] == "service" and k not in ("buanderie", "entrainement", "ecoute", "conseil")]
    xs1 = min(bbox(r["shape"])[0] for r in svc); ys1 = min(bbox(r["shape"])[1] for r in svc); xs2 = max(bbox(r["shape"])[2] for r in svc); ys2 = max(bbox(r["shape"])[3] for r in svc)
    o.append(hot("service", "Aile de service (douches, WC, salle de vie, self, cuisines)", ("rect", xs1-4, ys1-4, xs2+4, ys2+4), tbd=True))
    o.append(hot("buanderie", "Buanderie", R["buanderie"]["shape"], tbd=True))
    o.append(hot("main", "Aile de la Main (garde rapprochée de Psykos ; Dark, chef)", R["main"]["shape"], tbd=True))
    o.append(hot("entrainement", "Salle d'entraînement (grande voûte)", R["entrainement"]["shape"], tbd=True))
    o.append(hot("ecoute", "Salle d'écoute (Pokématos, radios)", R["ecoute"]["shape"], tbd=True))
    o.append(hot("conseil", "Salle du conseil (Pape Sombre, Psykos, Cabale, Évêques)", R["conseil"]["shape"], tbd=True))
    cab = [r for k, r in R.items() if r["kind"] == "cabale"]
    xs1 = min(bbox(r["shape"])[0] for r in cab); ys1 = min(bbox(r["shape"])[1] for r in cab); xs2 = max(bbox(r["shape"])[2] for r in cab); ys2 = max(bbox(r["shape"])[3] for r in cab)
    o.append(hot("cabale", "Quartier des Cabalistes et des Évêques", ("rect", xs1-4, ys1-4, xs2+4, ys2+4), tbd=True))
    for lid, name in [("ev_1", "Chambre d'Évêque 1"), ("ev_2", "Chambre d'Évêque 2"), ("ev_3", "Chambre d'Évêque 3"), ("ev_4", "Chambre d'Évêque 4"), ("ev_wc", "WC des Évêques"), ("ev_sdb", "Salle de bain des Évêques"), ("ev_salon", "Salon des Évêques")]:
        o.append(hot(lid, name, R[lid]["shape"], tbd=True))
    for lid, r in R.items():
        if r["kind"] in ("secondaire", "garde"):
            o.append(hot(lid, DISPLAY.get(lid, r["label"]).replace("|", " "), irregular(lid, r), tbd=True))
    for aid, (node, lab, note) in M.ACCES.items():
        x, y = N[node]
        o.append(hot(aid, f"{lab} — {note}", ("circle", x, y+8, 26), tbd=True))
    o.append('</g>')
    o.append('</svg>')
    open(path, "w", encoding="utf-8").write("\n".join(o))

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/qg_schema/final/Plan_QG_Corresone_final.svg"
    import os; os.makedirs(os.path.dirname(out), exist_ok=True)
    render(out)
    import xml.etree.ElementTree as ET; ET.parse(out)
    import cairosvg
    cairosvg.svg2png(url=out, write_to=out.replace("_final.svg", "_apercu.png"), output_width=2600)
    ok = all(res for _, res, _ in check())
    print("XML OK ; GRAPHE", "VALIDE" if ok else "ERREURS", ";", os.path.getsize(out)//1024, "Ko")
