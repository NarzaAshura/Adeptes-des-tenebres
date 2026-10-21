# -*- coding: utf-8 -*-
"""
Modèle topologique du QG des Adorateurs des Ténèbres (Corrésone) — version « toile d'araignée ».
Principe : l'église au centre, des RAYONS qui partent vers l'extérieur, trois ANNEAUX irréguliers
qui les relient, et des salles logées dans les mailles. viewBox 0 0 1600 1200.
"""
W, H = 1600, 1200
DORM_ROWS = 8   # 2 colonnes x 8 = 16 alvéoles

NODES = {
    # ----- épine nord (rayon N) -----
    "Rs": (800, 165),  "R3n": (800, 205), "Na": (800, 255), "N1": (800, 340), "EN": (800, 410),
    # ----- rayon sud -----
    "ES": (800, 710), "S1": (800, 790), "S2": (800, 900), "S3": (800, 1010), "A2": (800, 1140),
    # ----- église O/E -----
    "EW": (650, 560), "W5": (560, 570), "EE": (950, 560), "CW": (1000, 560),
    # ----- anneau 1 (proche) -----
    "r1b": (905, 345), "r1c": (995, 400), "CNa": (1060, 427),
    "CSa": (1060, 713), "r1e": (1000, 745),
    "r1g": (615, 760), "r1i": (612, 380),
    # ----- anneau 2 -----
    "r2b": (960, 262), "r2c": (1090, 330), "r2d": (1205, 560), "r2e": (1130, 785),
    "r2f": (975, 905), "r2g": (585, 835), "J1": (395, 605), "r2i": (400, 300), "r2j": (632, 272),
    # ----- anneau 3 (interrompu dans le secteur Fiel / haute sécurité) -----
    "Pj": (1125, 190), "r3b": (960, 228), "r3j": (640, 205), "r3k": (470, 215), "HN": (195, 250),
    "HS": (195, 560), "P1": (250, 600), "Pv": (232, 640), "r3h": (300, 650), "IN": (300, 725),
    "r3g": (480, 780), "Ie": (430, 778), "IE": (370, 778), "J2": (470, 850), "CIT": (357, 923),
    "SW1": (470, 1000), "A1": (380, 1140), "r3f": (640, 1060), "r3e": (990, 1075), "r3d": (1230, 960),
    "r3c": (1340, 790), "r3c2": (1300, 650),
    # ----- Psykos -----
    
    # ----- Fiel / haute sécurité -----
    "F1": (1222, 228), "Fa": (1270, 225), "Fx": (1345, 300), "HSN": (1345, 390),
    "Fs19": (1165, 208), "NEd": (1215, 195), "Bd": (1170, 290),
    # ----- cellules -----
    "CN": (1060, 505), "CS": (1060, 615),
    # ----- rayons diagonaux : nœuds intermédiaires -----
    "sNW": (560, 300),       # entre r1i et r2i
    # ----- portes de salles secondaires (nœuds de piquage) -----
    "n01": (700, 205), "n03": (800, 300),
    "n05": (578, 505), "n08": (1324, 715),
    "n25": (1060, 675),
    "n13": (800, 950), "n15": (981, 972),
    
    "nDh": (400, 304), "nDf": (399, 340), "nWh": (399, 375), "nWf": (398, 407), "nV": (397, 460), "nSf": (396, 522), "nCu": (395, 572), "nBu": (465, 300), "nEf": (1060, 650), "nEc": (857, 257), "nPs": (1098, 196), "vE": (1350, 650), "nEvD": (245, 190), "nEv": (150, 190), "nEvB": (150, 140), "nEvA": (150, 90), "nEvS": (150, 40), "EvTop": (150, 10), "gN": (800, 1060), "gS": (800, 1110), "nT": (1180, 787), "nC": (330, 232), "nA": (330, 158), "Cj": (330, 18), "nK1": (330, 44), "nK2": (330, 88), "nK3": (330, 132), "n21": (600, 425), 
}

RING1 = ["N1", "r1b", "r1c", "CNa", None, "CSa", "r1e", "S1", "r1g", "W5", "r1i", "N1"]   # ouvert à l'est (V1.2 : croisements supprimés)
RING2 = ["Na", "r2b", "r2c", "r2d", "r2e", "r2f", "S2", "r2g", "J1", "r2i", "r2j", "Na"]
RING3 = ["Pj", "r3b", "R3n", "r3j", "r3k", "HN",          # HN -> couloir axial des habitations -> HS
         None, "HS", "P1", "r3h", "r3g", "J2", "SW1", "r3f", "S3", "r3e", "r3d", "r3c", "r3c2"]

def _ring(seq):
    out = []
    for a, b in zip(seq, seq[1:]):
        if a is None or b is None: continue
        out.append((a, b))
    return out

EDGES = _ring(RING1) + _ring(RING2) + _ring(RING3) + [
    # rayon N
    ("Rs", "R3n"), ("R3n", "Na"), ("Na", "N1"), ("N1", "EN"),
    # rayon S
    ("ES", "S1"), ("S1", "S2"), ("S2", "S3"), ("S3", "gN"), ("gS", "A2"),
    # rayon O
    ("EW", "W5"), ("W5", "J1"),
    # rayon E (passage église -> geôles)
    ("EE", "CW"),
    # cellules : piquages N et S sur l'anneau 1
    ("CN", "CNa"), ("CS", "CSa"),
    # rayons diagonaux
    ("r1c", "r2c"), ("r2c", "Pj"),
    ("r1e", "r2e"), ("r2e", "r3c"),
    ("r1g", "r2g"), ("r2g", "J2"),
    ("r1i", "sNW"), ("sNW", "r2i"), ("r2i", "r3k"),
    ("r1b", "r2b"), ("r2b", "r3b"), ("r2d", "r3c2"), ("r2f", "r3e"),
    ("r2j", "r3j"), ("r1i", "r2j"),
    # chemins secondaires / cordes
    ("r2g", "r3g"), ("r3g", "Ie"), ("Ie", "IE"), ("J2", "CIT"), ("SW1", "A1"),
    ("P1", "Pv"), ("r3h", "IN"), 
    
    # Quartier des Cabalistes : couloir privé en impasse
    ("nA", "nK3"), ("nK3", "nK2"), ("nK2", "nK1"), ("nK1", "Cj"),
    ("r3c2", "vE"), ("nEvD", "nEv"), ("nEv", "nEvB"), ("nEvB", "nEvA"), ("nEvA", "nEvS"), ("nEvS", "EvTop"),
    # Psykos : spur privé unique
    # Fiel : galerie d'approche unique depuis Pj
    ("Pj", "Fs19"), ("Fs19", "F1"), ("F1", "Fa"), ("F1", "NEd"), ("Fs19", "Bd"),
    ("Fa", "Fx"),      # chemin sur le bord de la fosse (interne au Fiel)
    ("Fx", "HSN"),
]

# nœuds de piquage insérés sur une arête existante : (nœud, arête (a,b))
INSERTS = [
    ("n01", ("R3n", "r3j")), ("n03", ("Na", "N1")),
    ("n05", ("W5", "r1i")), ("n08", ("r3c2", "r3c")),
    ("n25", ("CS", "CSa")), 
    ("n13", ("S2", "S3")), ("n15", ("r2f", "r3e")),
    
    ("nDh", ("r2i", "J1")), ("nDf", ("nDh", "J1")), ("nWh", ("nDf", "J1")), ("nWf", ("nWh", "J1")), ("nV", ("nWf", "J1")), ("nBu", ("r2i", "sNW")), ("nEf", ("CS", "n25")), ("nEc", ("Na", "r2b")), ("nPs", ("Pj", "r3b")), ("nC", ("r3k", "HN")), ("nT", ("r2e", "r3c")), ("n21", ("n05", "r1i")), ("nSf", ("nV", "J1")), ("nCu", ("nSf", "J1")), 
]
for n, (a, b) in INSERTS:
    if (a, b) in EDGES: EDGES.remove((a, b))
    elif (b, a) in EDGES: EDGES.remove((b, a))
    else: raise SystemExit(f"arête introuvable pour {n}: {a}-{b}")
    EDGES += [(a, n), (n, b)]

# courts couloirs d'accès (nœud galerie -> point de porte)
STUBS = [
    ("Fs19", (1165, 262)),
    ("n01", (700, 170)), ("n03", (775, 300)), 
    ("n08", (1285, 715)), 
    ("n13", (830, 950)), ("n15", (1010, 972)), ("nDh", (365, 304)), ("nDf", (365, 340)), ("nWh", (365, 375)), ("nWf", (365, 407)), ("nV", (365, 460)), ("nSf", (365, 522)), ("nCu", (365, 572)), ("Pv", (205, 640)), ("Pv", (224, 674)), ("nT", (1180, 822)), ("nBu", (465, 320)), ("nPs", (1098, 168)), ("vE", (1368, 650)), ("nEvB", (140, 140)), ("nEvB", (160, 140)), ("nEvA", (140, 90)), ("nEvA", (160, 90)), ("nEvS", (140, 40)), ("nEvS", (160, 40)), ("nEf", (1085, 650)), ("nEc", (857, 278)), ("nK1", (312, 44)), ("nK1", (348, 44)), ("nK2", (312, 88)), ("nK2", (348, 88)), ("nK3", (312, 132)), ("nK3", (348, 132)), ("n21", (560, 425)), ("n05", (540, 505)),
    ("r3c", (1370, 795)), ("n25", (1040, 675)), ("nC", (330, 200)),
]

ROOMS = {
    "eglise": dict(label="ÉGLISE SOUTERRAINE", kind="etabli",
        shape=("poly", [(750,410),(850,410),(850,510),(950,510),(950,610),(850,610),
                        (850,710),(750,710),(750,610),(650,610),(650,510),(750,510)]),
        doors=[("EN","N"),("ES","S"),("EW","O"),("EE","E → passage vers les geôles")]),
    "reserve": dict(label="RÉSERVE", kind="etabli", shape=("rect", 745,100,855,165), doors=[("Rs","S (verrouillable)")]),
    "habitations": dict(label="HABITATIONS (D01–D16)", kind="etabli", shape=("rect", 135,250,255,560),
        doors=[("HN","N (bout du couloir axial)"),("HS","S (bout du couloir axial)")]),
    "infirmerie": dict(label="INFIRMERIE", kind="etabli", shape=("rect", 180,725,370,830),
        doors=[("IN","N"),("IE","E")]),
    "citerne": dict(label="CITERNE (sèche)", kind="etabli", shape=("circle", 300,980,80),
        doors=[("CIT","NE (unique)")]),
    "cellules": dict(label="CELLULES|DES SACRIFICES", kind="etabli", shape=("rect", 1000,505,1120,615),
        doors=[("CW","O ← passage depuis l'église"),("CN","N"),("CS","S")]),
    "fiel": dict(label="OUBLIETTES DU FIEL", kind="special", shape=("circle", 1345,225,75),
        doors=[("Fa","arrivée (sans porte)"),("Fx","vers haute sécurité (sans porte)")]),
    "hautesecu": dict(label="HAUTE SÉCURITÉ", kind="special", shape=("rect", 1298,390,1408,540),
        doors=[("HSN","N (unique)")]),
    "pape": dict(label="PAPE SOMBRE", kind="bureau",
        shape=("poly", [(65,580),(135,580),(160,605),(160,675),(135,700),(65,700),(40,675),(40,605)]), doors=[]),
    "pape_chambre": dict(label="chambre", kind="bureau", shape=("rect", 45,535,120,580), doors=[]),
    "pape_sdb": dict(label="s. de bain", kind="bureau", shape=("rect", 45,490,120,535), doors=[]),
    "psykos_sdb": dict(label="s. de bain", kind="bureau", shape=("rect", 895,140,960,185), doors=[]),
    # ---- quartier des Cabalistes (proposition, non canon) ----
    "cab_salon": dict(label="Salon des Cabalistes", kind="cabale", shape=("rect", 262,-26,398,18), doors=[("Cj","S")]),
    "cab_sdb": dict(label="s. de bain", kind="cabale", shape=("rect", 245,26,312,62), doors=[("nK1","E")]),
    "cab_wc": dict(label="WC", kind="cabale", shape=("rect", 348,26,415,62), doors=[("nK1","O")]),
    "cab_c1": dict(label="Cab. 1", kind="cabale", shape=("rect", 245,70,312,106), doors=[("nK2","E")]),
    "cab_c3": dict(label="Cab. 3", kind="cabale", shape=("rect", 348,70,415,106), doors=[("nK2","O")]),
    "cab_c2": dict(label="Cab. 2", kind="cabale", shape=("rect", 245,114,312,150), doors=[("nK3","E")]),
    "cab_garde": dict(label="Poste de garde|antichambre de la Cabale", kind="garde", shape=("rect", 245,158,415,200), doors=[("nC","S"),("nA","N (vers le couloir privé)"),("nEvD","O (vers les Évêques)")]),
    "cab_c4": dict(label="Cab. 4", kind="cabale", shape=("rect", 348,114,415,150), doors=[("nK3","O")]),
    "ev_1": dict(label="Évêque 1", kind="cabale", shape=("rect", 85,120,140,160), doors=[("nEvB","E")]),
    "ev_2": dict(label="Évêque 2", kind="cabale", shape=("rect", 85,70,140,110), doors=[("nEvA","E")]),
    "ev_wc": dict(label="WC", kind="cabale", shape=("rect", 85,20,140,60), doors=[("nEvS","E")]),
    "ev_3": dict(label="Évêque 3", kind="cabale", shape=("rect", 160,120,215,160), doors=[("nEvB","O")]),
    "ev_4": dict(label="Évêque 4", kind="cabale", shape=("rect", 160,70,215,110), doors=[("nEvA","O")]),
    "ev_sdb": dict(label="s. de bain", kind="cabale", shape=("rect", 160,20,215,60), doors=[("nEvS","O")]),
    "ev_salon": dict(label="Salon des Évêques", kind="cabale", shape=("rect", 100,-30,200,10), doors=[("EvTop","S")]),
    "pape_vest": dict(label="vestibule", kind="bureau", shape=("rect", 160,615,205,665), doors=[("Pv","E (entrée unique, gardée)")]),
    "pape_reduit": dict(label="réduit", kind="bureau", shape=("rect", 65,770,135,830), doors=[]),
    "psykos": dict(label="SŒUR PSYKOS", kind="bureau", shape=("rect", 960,70,1080,170), doors=[]),
    "psykos_vest": dict(label="vest.", kind="bureau", shape=("rect", 1080,128,1115,168), doors=[("nPs","S (entrée unique)")]),
    "psykos_annexe": dict(label="chambre", kind="bureau", shape=("rect", 895,85,960,140), doors=[]),
    # ---- salles secondaires ----
    "S01": dict(label="Poste de garde|(réserve)", kind="garde", shape=("rect", 660,110,735,170), doors=[("n01","S")]),
    "S03": dict(label="Archives", kind="secondaire", shape=("rect", 705,288,775,322), doors=[("n03","E (court couloir)")]),
    "S08": dict(label="Réserve d'huile|et de torches", kind="secondaire", shape=("rect", 1225,690,1285,740), doors=[("n08","E (court couloir)")]),
    "S13": dict(label="Lavabos / latrines|(« visiteurs »)", kind="secondaire", shape=("rect", 830,925,900,975), doors=[("n13","O (court couloir)")]),
    "S15": dict(label="Cierges, encens|(matériel rituel)", kind="secondaire", shape=("rect", 1010,945,1080,1000), doors=[("n15","O (court couloir)")]),
    "entrainement": dict(label="Salle d'entraînement|(grande voûte)", kind="service", shape=("poly", [(1110,822),(1245,822),(1250,870),(1205,938),(1120,948)]), doors=[("nT","N (court couloir)")]),
    "S17": dict(label="Forge|(secteur est)", kind="secondaire", shape=("rect", 1370,745,1460,845), doors=[("r3c","O (court couloir)")]),
    "veille_est": dict(label="Poste de veille|(galerie est)", kind="garde", shape=("rect", 1368,622,1432,678), doors=[("vE","O (court couloir)")]),
    "S19": dict(label="Salle|d'interrogatoire", kind="secondaire", shape=("poly", [(1130,262),(1215,262),(1215,305),(1180,339),(1130,345)]), doors=[("Fs19","N (court couloir muré)")]),
    "S20": dict(label="Chaux et outils|du Fiel", kind="secondaire", shape=("poly", [(1190,110),(1275,110),(1275,177),(1256,195),(1190,195)]), doors=[("NEd","S")]),
    # ---- aile de service des habitations (demande utilisateur, non canon) ----
    "douches_h": dict(label="Douches H", kind="service", shape=("rect", 318,290,365,318), doors=[("nDh","E")]),
    # ordre nord→sud décidé par l'auteur (19/10) : Douches H, WC H, WC F, Douches F — les noms des nœuds de porte (nDf/nWh/nWf) sont historiques
    "wc_h": dict(label="WC H", kind="service", shape=("rect", 318,326,365,354), doors=[("nDf","E")]),
    "wc_f": dict(label="WC F", kind="service", shape=("rect", 318,362,365,388), doors=[("nWh","E")]),
    "douches_f": dict(label="Douches F", kind="service", shape=("rect", 318,394,365,420), doors=[("nWf","E")]),
    "salle_vie": dict(label="Salle de vie", kind="service", shape=("rect", 255,432,365,487), doors=[("nV","E")]),
    "self": dict(label="Self", kind="service", shape=("rect", 255,497,365,547), doors=[("nSf","E")]),
    "buanderie": dict(label="Buanderie", kind="service", shape=("rect", 430,320,500,372), doors=[("nBu","N (court couloir)")]),
    "S21": dict(label="Atelier|(réparations)", kind="secondaire", shape=("rect", 430,390,560,460), doors=[("n21","E (court couloir)")]),
    "S27": dict(label="Serre à baies|(lampes à réflecteurs)", kind="secondaire", shape=("rect", 430,478,540,532), doors=[("n05","E (court couloir)")]),
    "reserve_cuisine": dict(label="réserve|alim.", kind="service", shape=("rect", 270,547,307,590), doors=[]),
    "cuisines": dict(label="Cuisines", kind="service", shape=("rect", 307,547,365,590), doors=[("nCu","E (service)")]),
    "garde_pape": dict(label="loge", kind="garde", shape=("rect", 200,674,248,706), doors=[("Pv","N")]),
    "garde_sud": dict(label="Poste de garde|de l'entrée", kind="garde", shape=("rect", 760,1060,840,1110), doors=[("gN","N (vers le QG)"),("gS","S (vers l'extérieur)")]),
    "ecoute": dict(label="Salle d'écoute|(Pokématos, radios)", kind="service", shape=("rect", 822,278,892,322), doors=[("nEc","N")]),
    "effets": dict(label="Dépôt des effets|des sacrifiés", kind="secondaire", shape=("rect", 1085,625,1145,680), doors=[("nEf","O")]),
    "garde_manger": dict(label="garde-|manger", kind="service", shape=("rect", 307,590,365,628), doors=[]),
    "S25": dict(label="Garde|des geôles", kind="garde", shape=("rect", 985,650,1040,700), doors=[("n25","E")]),
}
# S19 : porte N = extrémité du court couloir depuis Fs19 (nœud Bd non utilisé comme nœud de graphe)
NODES.pop("Bd", None)
EDGES = [e for e in EDGES if "Bd" not in e]

INTERNAL_DOORS = [
    ("pape", "pape_chambre", (82, 580)), ("pape", "pape_vest", (160, 640)), ("pape_chambre", "pape_sdb", (82, 535)), ("psykos_annexe", "psykos_sdb", (927, 140)),
    ("psykos", "psykos_annexe", (960, 112)), ("psykos", "psykos_vest", (1080, 148)),
    ("self", "reserve_cuisine", (288, 547)), ("self", "cuisines", (336, 547)), ("reserve_cuisine", "cuisines", (307, 570)), ("cuisines", "garde_manger", (336, 590)),
]
PRIVATE_PASSAGES = [
    dict(a="pape", b="pape_reduit", pts=[(100,700),(100,770)], door_a=(100,700), door_b=(100,770)),
]
SECRETS = [
    dict(id="secret_pape", frm="pape_reduit", pts=[(65,800),(30,815),(0,830)], note="vers l'extérieur — débouché inconnu"),
    dict(id="secret_cabale", frm="cab_salon", pts=[(300,-26),(296,-38),(292,-46)], note="vers l'extérieur — débouché inconnu"),
    dict(id="secret_psykos", frm="psykos_annexe", pts=[(927,85),(915,50),(900,15)], note="vers l'extérieur — débouché inconnu"),
]
ACCES = {"acces1": ("A1", "GAL. S-O", "accès de la pizzeria de Dark — non gardé"), "acces2": ("A2", "GAL. SUD", "accès principal gardé — débouché extérieur non cartographié")}


# ---------------------------------------------------------------------------
# Salles orientées parallèlement à leur galerie (court couloir perpendiculaire)
# ---------------------------------------------------------------------------
import math as _m
def _attach(rid, label, kind, cx, cy, w, h, a, b, doors_note="court couloir"):
    """Rectangle w×h centré en (cx,cy), tourné selon l'arête a-b ; porte au milieu du côté
    tourné vers la galerie ; nœud de piquage = pied de la perpendiculaire sur la galerie."""
    global EDGES
    (ax, ay), (bx, by) = NODES[a], NODES[b]
    ux, uy = bx-ax, by-ay; L = _m.hypot(ux, uy); ux, uy = ux/L, uy/L
    nx, ny = -uy, ux                                  # normale
    # côté de la galerie par rapport au centre
    sgn = 1 if ((cx-ax)*nx + (cy-ay)*ny) < 0 else -1  # direction centre -> galerie
    t = ((cx-ax)*ux + (cy-ay)*uy)
    foot = (round(ax+ux*t), round(ay+uy*t))
    door = (round(cx+sgn*nx*h/2), round(cy+sgn*ny*h/2))
    pts = []
    for sx, sy in ((-1,-1),(1,-1),(1,1),(-1,1)):
        pts.append((round(cx+ux*sx*w/2+nx*sy*h/2), round(cy+uy*sx*w/2+ny*sy*h/2)))
    node = "p_"+rid
    NODES[node] = foot
    # insérer le nœud sur l'arête courante qui contient le pied (chaîne colinéaire à a-b)
    def on_line(p): return abs((p[0]-ax)*ny + (p[1]-ay)*nx*(-1)) < 1.5 or abs(((p[0]-ax)*(-ny)) + ((p[1]-ay)*nx)) < 1.5
    best = None
    for e in list(EDGES):
        p, q = NODES[e[0]], NODES[e[1]]
        # colinéarité approximative
        d1 = abs((p[0]-ax)*uy - (p[1]-ay)*ux); d2 = abs((q[0]-ax)*uy - (q[1]-ay)*ux)
        if d1 > 1.5 or d2 > 1.5: continue
        t1 = (p[0]-ax)*ux + (p[1]-ay)*uy; t2 = (q[0]-ax)*ux + (q[1]-ay)*uy
        if min(t1, t2) - 0.5 <= t <= max(t1, t2) + 0.5: best = e; break
    if best is None: raise SystemExit(f"_attach {rid}: pied hors de l'arête {a}-{b}")
    EDGES.remove(best); EDGES.append((best[0], node)); EDGES.append((node, best[1]))
    STUBS.append((node, door))
    ROOMS[rid] = dict(label=label, kind=kind, shape=("poly", pts), doors=[(node, doors_note)])

_attach("S06", "Sacristie", "secondaire", 705, 420, 62, 48, "r1i", "N1")
_attach("S10", "Salle des initiés", "secondaire", 905, 822, 72, 52, "S1", "r1e")
_attach("S12", "Salle de réunion|des frères", "secondaire", 700, 930, 80, 50, "r2g", "S2")
_attach("S18", "Fourrage et|paille (Pokémon)", "secondaire", 560, 937, 80, 56, "J2", "r2g")
_attach("S24", "Matériel|d'entraînement", "secondaire", 1190, 1065, 80, 52, "r3e", "r3d")
_attach("S26", "Remise (outils|de corvée)", "secondaire", 600, 1105, 72, 50, "SW1", "r3f")
_attach("cave_vin", "Cave à vin", "secondaire", 505, 166, 68, 46, "r3k", "r3j")
_attach("cave_fromages", "Cave à|fromages", "secondaire", 590, 160, 68, 46, "r3k", "r3j")
_attach("conseil", "Salle du conseil|(hauts gradés)", "service", 683, 690, 100, 88, "r1g", "S1")
# Salle du conseil : octogone régulier, un côté plat face à la galerie (porte au milieu de ce côté)
def _octogone(rid, apothem):
    node = "p_"+rid
    pts = ROOMS[rid]["shape"][1]
    cx = sum(p[0] for p in pts)/4; cy = sum(p[1] for p in pts)/4
    door = next(p for n, p in STUBS if n == node)
    nx, ny = door[0]-cx, door[1]-cy; L = _m.hypot(nx, ny); nx, ny = nx/L, ny/L
    R = apothem/_m.cos(_m.pi/8); th = _m.atan2(ny, nx)
    poly = [(round(cx+R*_m.cos(th+_m.pi/8+k*_m.pi/4)), round(cy+R*_m.sin(th+_m.pi/8+k*_m.pi/4))) for k in range(8)]
    ROOMS[rid]["shape"] = ("poly", poly)
    new_door = (round(cx+apothem*nx), round(cy+apothem*ny))
    STUBS[:] = [(n, (new_door if n == node else p)) for n, p in STUBS]
_octogone("conseil", 48)
_attach("remise_so", "Salle des pompes|(puits)", "service", 505, 1085, 72, 48, "SW1", "r3f")
_attach("S28", "Vestiaire des|officiants", "secondaire", 935, 418, 70, 46, "r1b", "r1c")

# ---------------------------------------------------------------------------
# Aile de la Main (garde rapprochée de Psykos) : bloc parallèle à la galerie r2c–r2d
# ---------------------------------------------------------------------------
def _aile_main():
    global EDGES, MAIN_FRAME
    (ax, ay), (bx, by) = NODES["r2c"], NODES["r2d"]
    L = _m.hypot(bx-ax, by-ay); ux, uy = (bx-ax)/L, (by-ay)/L
    nx, ny = uy, -ux                       # normale vers l'est
    W = lambda s_, d_: (round(ax+ux*s_+nx*d_, 1), round(ay+uy*s_+ny*d_, 1))
    NODES["gM0"] = W(72, 0)
    for e in list(EDGES):
        if set(e) == {"r2c", "r2d"}:
            EDGES.remove(e); EDGES += [("r2c", "gM0"), ("gM0", "r2d")]; break
    S0, S1, D0, D1 = 60, 244, 34, 92
    ROOMS["main"] = dict(label="", kind="main", shape=("poly", [W(S0, D0), W(S1, D0), W(S1, D1), W(S0, D1)]), doors=[("gM0", "O (entrée unique)")])
    STUBS.append(("gM0", W(72, D0)))
    cells = [("Main 1 · Dark", 66, 92), ("Main 2", 94, 120), ("Main 3", 122, 148), ("Main 4", 150, 176), ("Main 5", 178, 204), ("WC", 206, 222), ("douche", 224, 240)]
    MAIN_FRAME = dict(W=W, cells=cells, cor=(S0+4, S1-4, D0+6, D0+22), cell_d=(D0+26, D1-4))
_aile_main()

# ---------------------------------------------------------------------------
# Dilatation homothétique (aération) : tout est multiplié par SCALE, sauf la
# largeur des galeries et les textes (gérés par le rendu).
# ---------------------------------------------------------------------------
SCALE = 1.35
OY = 45  # marge haute (titre)
def _p(p): return (round(p[0]*SCALE), round((p[1]+OY)*SCALE))
def _shape(sh):
    if sh[0] == "rect": return ("rect", *(_p(sh[1:3]) + _p(sh[3:5])))
    if sh[0] == "circle": return ("circle", *_p(sh[1:3]), round(sh[3]*SCALE))
    return ("poly", [_p(q) for q in sh[1]])
W, H = round(W*SCALE), round((H+OY)*SCALE)
NODES = {k: _p(v) for k, v in NODES.items()}
STUBS = [(n, _p(p)) for n, p in STUBS]
for r in ROOMS.values(): r["shape"] = _shape(r["shape"])
INTERNAL_DOORS = [(a, b, _p(p)) for a, b, p in INTERNAL_DOORS]
for pp in PRIVATE_PASSAGES:
    pp["pts"] = [_p(q) for q in pp["pts"]]; pp["door_a"] = _p(pp["door_a"]); pp["door_b"] = _p(pp["door_b"])
for sc in SECRETS: sc["pts"] = [_p(q) for q in sc["pts"]]
MAIN_FRAME['W'] = (lambda W0: (lambda s_, d_: _p(W0(s_, d_))))(MAIN_FRAME['W'])
AERATIONS = [_p(q) for q in [(1480, 735), (290, 615), (1400, 150), (860, 455), (560, 1025)]]   # puits d'aération (décor)

# Pièces traversantes : (salle, nœud d'entrée, nœud de sortie)
TRANSITS = [("garde_sud", "gS", "gN"), ("cab_garde", "nC", "nA"), ("cab_garde", "nC", "nEvD"), ("habitations", "HN", "HS")]

import random as _r
def _fiel_poly():
    cx, cy, rr = ROOMS["fiel"]["shape"][1:]
    rf = _r.Random(11); pts = []
    for k in range(16):
        a = 2*_m.pi*k/16; d1 = rr*(0.97+0.06*rf.random()); d2 = rr*(0.97+0.06*rf.random())
        pts.append((round(cx+d1*_m.cos(a), 1), round(cy+d2*_m.sin(a), 1)))
    return pts
FIEL_POLY = _fiel_poly()
TRANSITS += [("eglise", "EN", "ES"), ("eglise", "EW", "EE"), ("cellules", "CW", "CN"), ("cellules", "CN", "CS")]

# Inflexions (décor + contrôle) : arête -> flèche perpendiculaire au milieu, en unités finales (après mise à l'échelle)
BENDS = {("r3h", "r3g"): -14, ("J1", "r2g"): -20, ("r2d", "r2e"): -16}   # r2c–r2d est désormais scindée en gM0 : droite
def bend_points(a, b, n=12):
    """Polyligne approchant l'arc quadratique de l'arête a-b (vide si pas d'inflexion)."""
    key = (a, b) if (a, b) in BENDS else ((b, a) if (b, a) in BENDS else None)
    if key is None: return None
    f = BENDS[key] * (1 if key == (a, b) else -1)
    (ax, ay), (bx, by) = NODES[a], NODES[b]
    mx, my = (ax+bx)/2, (ay+by)/2; L = _m.hypot(bx-ax, by-ay); nx, ny = -(by-ay)/L, (bx-ax)/L
    cx, cy = mx+2*f*nx, my+2*f*ny          # point de contrôle (flèche réelle = f)
    return [((1-t)**2*ax+2*(1-t)*t*cx+t*t*bx, (1-t)**2*ay+2*(1-t)*t*cy+t*t*by) for t in [i/n for i in range(n+1)]]

# ---------------------------------------------------------------------------
# Galeries annexes (« boyaux ») : couche séparée du graphe principal, en coordonnées finales.
# Boyaux étroits de roche brute qui partent d'une galerie principale (jamais d'une salle),
# se rejoignent ou retombent sur une autre galerie, ou finissent en cul-de-sac. Aucun ne dessert une salle.
BURROW_W = 11          # largeur de sol
BURROW_WT = 3          # paroi
def _proj(p, a, b):
    """Projection du point p sur le segment a-b (point de raccord exact à la galerie)."""
    (ax, ay), (bx, by) = NODES[a], NODES[b]
    dx, dy = bx-ax, by-ay; L2 = dx*dx+dy*dy
    t = max(0.05, min(0.95, ((p[0]-ax)*dx+(p[1]-ay)*dy)/L2))
    return (round(ax+t*dx), round(ay+t*dy))
_BURROWS_RAW = [
    # id, points, raccord début (arête | None), raccord fin (arête | None), options
    #   options : near=(arête) → le cul-de-sac final s'arrête à 1–2 m de cette galerie sans la rejoindre ; narrow={n° de segments rétrécis}
    ("by_nord",       [(600,355),(606,318),(588,282),(604,236),(584,196),(618,160),(672,164),(700,128),(760,140),(820,122),(846,154),(900,132),(944,98),(990,116),(1012,150),(1060,140),(1140,162)], ("r3k","nC"), None, dict(narrow={2,9})),
    ("by_nord_b",     [(672,164),(640,110),(602,72),(578,30)], None, None, dict(narrow={1})),
    ("by_nord_c",     [(846,154),(868,200),(866,250),(862,300),(900,338)], None, ("n01","r3j"), dict(narrow={2})),
    ("by_nord_d",     [(900,338),(912,372),(940,384)], ("n01","r3j"), None, dict(near=("r2j","Na"))),
    ("by_centre_nord",[(640,454),(655,405),(720,398),(790,372),(826,380)], ("r2i","r2j"), None, dict(near=("r2j","r3j"), narrow={2})),
    ("by_ouest",      [(380,383),(350,350),(290,338),(230,348),(170,345),(120,380),(80,450),(60,560),(92,620),(72,655)], ("nC","HN"), None, dict(narrow={5})),
    ("by_sudouest",   [(560,1256),(520,1222),(468,1240),(420,1206),(352,1230),(300,1212),(252,1250),(224,1300),(236,1350),(196,1392),(214,1446),(262,1472),(286,1526)], ("J2","CIT"), None, dict(narrow={3,8})),
    ("by_sudouest_b", [(252,1250),(190,1262),(130,1290),(80,1340)], None, None, {}),
    ("by_sudouest_c", [(214,1446),(160,1480),(150,1540)], None, None, dict(narrow={1})),
    ("by_sud",        [(888,1218),(850,1300),(848,1390),(900,1420),(929,1472)], ("p_S12","r2g"), ("r3f","S3"), dict(narrow={1})),
    ("by_nef_ne",     [(1140,523),(1150,560),(1180,598)], ("N1","r1b"), None, {}),
    ("by_nef_se",     [(1280,1082),(1265,1030),(1230,980),(1200,930)], ("r1e","p_S10"), None, dict(narrow={1})),
    ("by_nef_o",      [(830,822),(840,770),(858,720)], ("EW","W5"), None, {}),
    ("by_x_sud_o",    [(1000,1114),(1020,1160),(1050,1200),(1080,1210)], ("S1","p_conseil"), ("S1","S2"), {}),
    ("by_x_sud_e",    [(1080,1210),(1110,1225),(1130,1248)], ("S1","S2"), None, dict(near=("S2","r2f"))),
    ("by_sud_d",      [(929,1472),(940,1520),(905,1570),(930,1620)], ("r3f","S3"), None, dict(narrow={1})),
    ("by_x_centre_e", [(868,1093),(880,1140),(850,1180),(806,1148)], ("p_conseil","r1g"), ("r1g","r2g"), {}),
    ("by_x_centre_o", [(806,1148),(788,1122),(794,1092)], ("r1g","r2g"), None, {}),
    ("by_nordest",    [(1140,162),(1130,100),(1160,40),(1260,22),(1340,40),(1410,58),(1470,90),(1520,140),(1560,180)], None, None, dict(narrow={1,6})),
    ("by_nordest_b",  [(1140,162),(1181,200),(1182,260),(1180,352)], None, ("R3n","r3b"), {}),
    ("by_nordest_c",  [(1380,458),(1368,412),(1420,396),(1440,372)], ("r2b","r2c"), None, dict(near=("nPs","r3b"))),
    ("by_nordest_d",  [(1495,410),(1530,395),(1548,384)], ("r2c","Pj"), None, {}),
    ("by_sud_b",      [(1080,1300),(1040,1310),(1030,1390),(980,1420)], ("S2","n13"), None, dict(near=("r3f","S3"))),
    ("by_sud_est_nef",[(1250,1280),(1262,1340),(1250,1400),(1290,1450)], ("S2","r2f"), None, dict(near=("n15","r3e"))),
    ("by_est",        [(1794,1058),(1830,1020),(1870,1000),(1960,1010),(2030,960),(2060,860),(2050,740),(2010,640),(1990,560)], ("n08","r3c"), None, dict(narrow={2,6})),
    ("by_est_b",      [(2030,960),(2100,1010),(2120,1120),(2080,1220),(1960,1300)], None, None, {}),
    ("by_est_c",      [(1430,537),(1452,600),(1470,660),(1500,715),(1530,700)], ("r1c","r2c"), None, dict(near=("gM0","r2d"))),
    ("by_est_d",      [(1700,886),(1660,920),(1640,965),(1626,966)], ("r2d","r3c2"), None, dict(near=("r2d","r2e"))),
    ("by_sudest",     [(1734,1242),(1800,1250),(1880,1225),(1960,1300),(1930,1400),(1850,1470),(1790,1530)], ("r3d","r3c"), None, dict(narrow={4})),
    ("by_nef_est",    [(1421,1201),(1400,1150),(1360,1120),(1340,1130)], ("r2e","r2f"), None, {}),
    ("by_citerne",    [(586,1487),(520,1470),(462,1520),(466,1560)], ("SW1","A1"), None, {}),
    ("by_centre",     [(644,854),(662,918),(700,975),(722,1012),(786,1036)], ("W5","J1"), None, dict(narrow={2}, near=("r1g","W5"))),
    ("by_ouest_b",    [(380,383),(392,430),(384,510),(394,600),(388,616)], ("nC","HN"), None, dict(narrow={2})),
    ("by_ouest_c",    [(230,348),(214,366),(244,374)], None, None, dict(near=("nC","HN"))),
    ("by_sud_c",      [(1250,1483),(1245,1545),(1310,1585),(1385,1545),(1430,1467)], ("r3e","S3"), ("r3e","p_S24"), dict(narrow={1})),
    ("by_est_e",      [(1990,560),(2040,470),(2080,380),(2060,290)], None, None, dict(narrow={2})),
    ("by_sudouest_d", [(150,1540),(200,1596),(300,1626),(400,1620),(519,1591)], None, ("SW1","A1"), dict(narrow={1})),
]
BURROWS = []
for bid, pts, ta, tb, opt in _BURROWS_RAW:
    pts = list(pts)
    if ta: pts[0] = _proj(pts[0], *ta)
    if tb: pts[-1] = _proj(pts[-1], *tb)
    BURROWS.append(dict(id=bid, pts=pts, tap_a=ta, tap_b=tb, near=opt.get("near"), narrow=set(opt.get("narrow", ()))))
# Source des boyaux : "main_levee" (tracé de l'auteur, vectorisé) ou "auto" (mes 37 boyaux)
BURROWS_SOURCE = "main_levee"
SECRETS_HAND = False
if BURROWS_SOURCE == "main_levee":
    import json as _j, os as _os
    _f = _os.path.join(_os.path.dirname(__file__), "trace", "boyaux_main_levee.json")
    if _os.path.exists(_f):
        BURROWS = [dict(id=r["id"], pts=[tuple(q) for q in r["pts"]], tap_a=tuple(r["tap_a"]) if r["tap_a"] else None,
                        tap_b=tuple(r["tap_b"]) if r["tap_b"] else None, near=tuple(r["near"]) if r["near"] else None, narrow=set(r.get("narrow", ()))) for r in _j.load(open(_f))]
    # passages secrets vers l'extérieur : tracés dorés de l'auteur (même calque), rattachés à l'issue existante la plus proche
    _g = _os.path.join(_os.path.dirname(__file__), "trace", "secrets_or.json")
    if _os.path.exists(_g):
        SECRETS_HAND = True
        for _rec in _j.load(open(_g)):
            _p0 = _rec["pts"][0]
            _sc = min(SECRETS, key=lambda sc: (sc["pts"][0][0]-_p0[0])**2 + (sc["pts"][0][1]-_p0[1])**2)
            _sc["pts"] = [tuple(_sc["pts"][0])] + [tuple(q) for q in _rec["pts"][1:]]   # on garde le départ exact à la salle
# jonctions entre boyaux : un point partagé exactement (vérifié par le contrôleur)
