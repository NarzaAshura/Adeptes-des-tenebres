# -*- coding: utf-8 -*-
"""Injecte l'onglet « Repaire de Corrésone » dans Atlas_Noir_Adorateurs_des_Tenebres.html.

Entrées : atlas d'origine, SVG deux vues (GPT V3.0, géométrie V2.9 = V3.1), lieux_data.py.
Sortie : Atlas_Noir_Adorateurs_des_Tenebres.html (nouvelle version) dans ./out/.
"""
import json, re, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from lieux_data import LIEUX, SECTEURS, STATUTS

HERE = pathlib.Path(__file__).parent
SRC_ATLAS = HERE / "atlas_src.html"
SRC_SVG = pathlib.Path("/home/claude/gpt_v30/QG_Corresone_Cartes_Doubles/Carte_QG_Deux_Vues_Atlas.svg")
SRC_TOPO = pathlib.Path("/home/claude/qg_schema/final/topologie_qg.json")
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)

atlas = SRC_ATLAS.read_text(encoding="utf-8")
svg = SRC_SVG.read_text(encoding="utf-8")
topo = json.loads(SRC_TOPO.read_text(encoding="utf-8"))

# ---------- 1. SVG : mise au niveau V3.1 et préparation pour l'inclusion ----------
svg = svg.replace("<?xml version='1.0' encoding='UTF-8'?>\n", "")
old_cap = "accès principal gardé — hypothèse d'atlas"
new_cap = topo["prolongements"]["acces2"]["statut"]
assert svg.count(old_cap) == 5, svg.count(old_cap)  # 2 textes peints, aria-label, <title>, texte caché
svg = svg.replace(old_cap, new_cap)
old_cap1 = "prolongement, destination indéterminée"; new_cap1 = topo["prolongements"]["acces1"]["statut"]
assert svg.count(old_cap1) == 5, svg.count(old_cap1)
svg = svg.replace(old_cap1, new_cap1)
# S27 : le cellier des spiritueux devient la serre à baies (décision auteur, 19/10)
assert svg.count("Cellier (spiritueux)") == 3 and svg.count(">Cellier<") == 2
assert svg.count(">(spiritueux)<") == 2
svg = svg.replace("Cellier (spiritueux)", "Serre à baies").replace(">Cellier<", ">Serre<").replace(">(spiritueux)<", ">à baies<")
# aile de service : ordre nord→sud Douches H, WC H, WC F, Douches F (décision auteur, 19/10) — étiquettes peintes réaffectées par position
for y_, old_, new_ in (("524.0", "Douches F", "WC H"), ("571.0", "WC H", "WC F"), ("614.5", "WC F", "Douches F")):
    pat = re.compile(r'(<text x="461\.0" y="%s"[^>]*>)%s(</text>)' % (re.escape(y_), re.escape(old_)))
    assert len(pat.findall(svg)) == 2, (y_, old_)
    svg = pat.sub(lambda m: m.group(1) + "\x00" + new_ + m.group(2), svg)
svg = svg.replace("\x00", "")
# « Cave à fromages » déborde de sa salle (étiquette plus large que la pièce) → deux lignes, comme les autres étiquettes longues
def _lbl(x, y, t): return (f'<text x="{x}" y="{y}" font-size="11" font-weight="bold" text-anchor="middle" fill="none" stroke="#0f0e13" stroke-width="4" stroke-linejoin="round">{t}</text>'
                           f'<text x="{x}" y="{y}" font-size="11" font-weight="bold" text-anchor="middle" fill="#f1e8cf">{t}</text>')
one = _lbl("796.5", "280.5", "Cave à fromages")
assert svg.count(one) == 1, svg.count(one)
svg = svg.replace(one, _lbl("796.5", "275.0", "Cave à") + "\n" + _lbl("796.5", "287.0", "fromages"))
svg = svg.replace('width="2160" height="1681" ', '')
svg = svg.replace('data-version="V3.0-deux-vues-source-V2.9"', 'data-version="V3.1-atlas"')
svg = svg.replace('class="synthese"', 'id="carte-qg" class="synthese" preserveAspectRatio="xMidYMid meet"')
assert 'id="carte-qg"' in svg
# --- zones d'enveloppe (cabale, service) remplacées par une zone par salle ; salle des pompes ajoutée ---
def zone_svg(lid, label, kind, geom, tbd=True):
    if kind == "rect":
        x0, y0, x1, y1 = geom; cx, cy = (x0+x1)/2, (y0+y1)/2
        shape = f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="#fff" stroke="#f0b43c" stroke-width="0" class="zone"/>'
    else:
        pts = geom[0]; cx = sum(p[0] for p in pts)/len(pts); cy = sum(p[1] for p in pts)/len(pts)
        shape = '<polygon points="' + " ".join(f"{a},{b}" for a, b in pts) + '" fill="#fff" stroke="#f0b43c" stroke-width="0" class="zone"/>'
    lab = label.replace("&", "et")
    return (f'<g class="hot{" hot-tbd" if tbd else ""}" data-lieu="{lid}" tabindex="0" role="button" aria-label="{lab}">'
            f'<title>{lab}</title>{shape}<text x="{cx}" y="{cy}" font-size="1" fill="none">{lab}</text></g>')
SPLIT = {
    "cabale": ["cab_salon", "cab_sdb", "cab_wc", "cab_c1", "cab_c2", "cab_c3", "cab_c4"],
    "service": ["douches_h", "douches_f", "wc_h", "wc_f", "salle_vie", "self", "reserve_cuisine", "cuisines", "garde_manger", "remise_so"],
}
for env, rooms in SPLIT.items():
    m = re.search(r'<g class="hot[^"]*" data-lieu="%s".*?</g>\n?' % env, svg, re.S)
    assert m, env
    repl = "\n".join(zone_svg(r, LIEUX[r]["nom"], topo["salles"][r]["forme"], topo["salles"][r]["geometrie"]) for r in rooms) + "\n"
    svg = svg.replace(m.group(0), repl)
# --- V3.2 : galeries annexes (boyaux main levée), issues secrètes dorées, passage privé au gabarit boyau ---
SRC_FINAL = pathlib.Path("/home/claude/qg_schema/final/Plan_QG_Corresone_final.svg")
fin = SRC_FINAL.read_text(encoding="utf-8")
def grab(src, gid):
    i = src.index(f'id="{gid}"'); i = src.rindex("<g", 0, i); j = src.index("</g>", i)
    assert "<g" not in src[i+2:j], gid   # groupe plat
    return src[i:j+4]
G_BOYAUX = grab(fin, "boyaux"); G_OUV = grab(fin, "boyaux-ouvertures"); G_SECR = grab(fin, "secrets")
inner = lambda g: g[g.index(">")+1:g.rindex("</g>")]
BF, WD, RUB = "#34303b", "#5e586b", "#4a4652"
def recolor_im(x):
    """variante immersive : terre sombre et pierre brune (mêmes géométries)"""
    return (x.replace(f'"{BF}"', '"#2a2521"').replace(f'"{WD}"', '"#4f4740"').replace(f'"{RUB}"', '"#5b5047"')
             .replace('"#5a4a2a"', '"#46381f"').replace('"#f0b43c"', '"#807158"'))
def inject_layer(svg, pfx, name, content, before=None, after=None):
    g = f'<g class="decor" id="{pfx}-{name}">{content}</g>\n'
    if before:
        k = svg.index(f'<g class="decor" id="{pfx}-{before}">'); return svg[:k] + g + svg[k:]
    k = svg.index(f'id="{pfx}-{after}"'); k = svg.index("</g>", k) + 4; return svg[:k] + "\n" + g + svg[k:]
for pfx, fix in (("tech", lambda x: x), ("scene", recolor_im)):
    gal = grab(svg, f"{pfx}-galeries")
    svg = inject_layer(svg, pfx, "boyaux", fix(inner(G_BOYAUX)), before="galeries")
    svg = inject_layer(svg, pfx, "boyaux-ouvertures", fix(inner(G_OUV)), after="galeries")
    # passage privé Pape → réduit : gabarit boyau (paroi 17, sol 11)
    gal2 = re.sub(r'<polyline points="135,1006 135,1100" fill="none" stroke="([^"]+)" stroke-width="30" stroke-linecap="butt"/>',
                  lambda m: f'<polyline class="passage-prive" points="135,1006 135,1100" fill="none" stroke="{fix(chr(34)+WD+chr(34))[1:-1]}" stroke-width="17" stroke-linecap="butt"/>', gal)
    gal2 = re.sub(r'<polyline points="135,1006 135,1100" fill="none" stroke="([^"]+)" stroke-width="18" stroke-linecap="round"/>',
                  lambda m: f'<polyline class="passage-prive" points="135,1006 135,1100" fill="none" stroke="{fix(chr(34)+BF+chr(34))[1:-1]}" stroke-width="11" stroke-linecap="butt"/>', gal2)
    assert gal2 != gal and gal2.count("passage-prive") == 2, pfx
    svg = svg.replace(gal, gal2)
    # issues secrètes : tracés dorés de l'auteur à la place des pointillés (textes conservés côté technique)
    sec = grab(svg, f"{pfx}-secrets")
    sec2 = re.sub(r'<polyline points="[^"]*" fill="none" stroke="[^"]*" stroke-width="4" stroke-dasharray="[^"]*" stroke-linecap="round" opacity="[^"]*"/>\n?', '', sec)
    assert sec2.count("<polyline") == 0, pfx
    newpl = "\n".join(l for l in inner(G_SECR).split("\n") if l.startswith("<polyline"))
    assert newpl.count("<polyline") == 9, newpl.count("<polyline")
    sec2 = sec2.replace(">", ">\n" + fix(newpl) + "\n", 1)
    svg = svg.replace(sec, sec2)
# zone cliquable unique : les sols des boyaux (polygones), sous les zones des salles
# zone = rubans de PAROI (17 unités de large) + trait transparent de 8 unités : ~25 unités cliquables, soit ≈ 13 px à l'écran en vue ajustée
floors = re.findall(r'<polygon points="[^"]+" fill="%s" stroke="%s" stroke-width="0.8" stroke-linejoin="round"/>' % (WD, WD), G_BOYAUX)
assert len(floors) > 400, len(floors)
ZONE_BOYAUX = ('<g class="hot" data-lieu="galeries_annexes" tabindex="0" role="button" aria-label="Galeries annexes (boyaux)"><title>Galeries annexes (boyaux)</title>'
               + "".join(f.replace(f'fill="{WD}" stroke="{WD}" stroke-width="0.8"', 'fill="#fff" stroke="#f0b43c" stroke-width="8" stroke-opacity="0" stroke-linecap="round" class="zone"') for f in floors)
               + '<text x="1080" y="1600" font-size="1" fill="none">Galeries annexes (boyaux)</text></g>\n')
k = svg.index('<g id="interactif"'); k = svg.index(">", k) + 1
svg = svg[:k] + "\n" + ZONE_BOYAUX + svg[k:]
svg = svg.replace("</style>", "svg.sans-boyaux [id$='-boyaux'],svg.sans-boyaux [id$='-boyaux-ouvertures'],svg.sans-boyaux .hot[data-lieu='galeries_annexes']{display:none}svg.vue-immersive #interactif .hot[data-lieu='galeries_annexes'] .zone{pointer-events:all}</style>", 1)
svg = svg.replace('data-version="V3.1-atlas"', 'data-version="V3.2-atlas-boyaux"')
print("boyaux :", G_BOYAUX.count("<polygon")//2, "rubans ;", len(floors), "zones")
# --- cartouche (titre + légende) retiré du plan : il est rendu en HTML sous la carte ---
k = svg.index('id="tech-cartouche"'); k0 = svg.rindex("<g", 0, k); k1 = svg.index("</g>", k) + 4
svg = svg[:k0] + svg[k1:]
assert "tech-cartouche" not in svg
# --- quartiers : chaque zone reçoit data-q, et le plan un voile masqué par les zones du quartier choisi ---
QUARTIERS = [
    ("rituel", "Cœur rituel", ["eglise", "S06", "S28", "S10", "S15", "S12"],
     "L'église et ce qui la sert : sacristie, vestiaire des officiants, salle des initiés, réserve de cierges, salle de réunion des frères. Personne n'y loge ; le quartier ne vit qu'aux heures d'office et de rassemblement, et reste vide et fermé le reste du temps."),
    ("fiel", "Fiel, geôles et haute sécurité", ["cellules", "effets", "S25", "S13", "fiel", "hautesecu", "S20", "S19"],
     "Les cellules des sacrifices et leurs annexes (dépôt des effets, garde des geôles, lavabos des « visiteurs »), puis le Fiel, sa réserve de chaux et la salle d'interrogatoire, et au bout du seul chemin la haute sécurité. Avec la Main, c'est le seul quartier habité en permanence : les prisonniers ne partent pas, et un geôlier veille toujours."),
    ("pape", "Pape Sombre", ["pape", "pape_vest", "pape_chambre", "pape_sdb", "pape_reduit", "garde_pape", "conseil"],
     "L'appartement pontifical — vestibule, bureau, chambre, salle de bain, réduit et son issue secrète — avec la loge de ses gardes et, à part, la salle du Conseil où il siège avec les quatre Cabalistes. L'appartement est tenu prêt en permanence et gardé jour et nuit, même quand le Pape n'est pas à Corrésone."),
    ("psykos", "Psykos et la Main", ["psykos", "psykos_vest", "psykos_annexe", "psykos_sdb", "main"],
     "Le bureau de Sœur Psykos, son vestibule, son annexe avec la deuxième issue secrète, sa salle de bain, et l'aile de la Main, sa garde rapprochée. La Main ne quitte pas le repaire : ses cinq membres y dorment toutes les nuits, Dark en tête — sauf les rares fois où Psykos le retient chez elle."),
    ("cabale", "Cabalistes", ["cab_garde", "cab_salon", "cab_c1", "cab_c2", "cab_c3", "cab_c4", "cab_sdb", "cab_wc"],
     "Derrière l'antichambre gardée, le couloir privé des quatre Cabalistes : quatre chambres identiques, salle de bain et WC qu'on utilise seul, salon commun avec la troisième issue secrète. Comme tous ceux qui ne sont pas de garde, les Cabalistes dorment rarement ici : chacun a une vie au-dehors, et les chambres servent surtout les nuits d'office."),
    ("eveques", "Évêques", ["cab_garde", "ev_salon", "ev_1", "ev_2", "ev_3", "ev_4", "ev_wc", "ev_sdb"],
     "L'autre côté de l'antichambre gardée : le couloir des Évêques, quatre chambres plus simples, douche collective, WC, et un salon-mess pour une dizaine. Les Évêques sont au moins sept et presque toujours dehors, à tenir les cellules de l'Ordre dans Kalos du Sud : quatre chambres suffisent à ceux de passage, et le salon sert surtout de salle de rapport."),
    ("tresor", "Trésor, archives et écoute", ["reserve", "S01", "S03", "ecoute"],
     "La réserve-trésor et son poste de garde, les archives et la salle d'écoute : la mémoire, l'argent et les communications de l'Ordre, groupés au nord-est entre le quartier noble et Psykos. Un garde devant la réserve et une équipe de relais à l'écoute en permanence ; personne n'y dort."),
    ("vie", "Vie quotidienne", ["habitations", "buanderie", "infirmerie", "citerne", "S18", "cave_vin", "cave_fromages", "S27", "douches_h", "douches_f", "wc_h", "wc_f", "salle_vie", "self", "reserve_cuisine", "cuisines", "garde_manger", "remise_so"],
     "Les seize alvéoles des habitations, l'aile de service (douches, WC, salle de vie, self, cuisines et réserves), la buanderie, l'infirmerie, les caves, la serre, le fourrage, la citerne et la salle des pompes. Les frères et sœurs du rang IV n'y dorment que lorsqu'ils sont de service ou de garde ; les autres nuits, les alvéoles restent vides et le self tourne au ralenti."),
    ("galeries", "Galeries, ateliers et accès", ["galeries_annexes", "acces2", "garde_sud", "acces1", "veille_est", "S17", "S21", "S08", "entrainement", "S24", "S26"],
     "Les deux accès — GAL. SUD, gardée, et GAL. S-O, vers la pizzeria de Dark —, le poste de l'entrée, le guet de l'est, la forge, l'atelier, la réserve de torches, la remise des corvées, la grande voûte d'entraînement et le réseau des boyaux. Les postes de garde sont tenus en continu ; les ateliers ne vivent que le jour."),
]
_q_of = {}
for qid, _, rooms, _d in QUARTIERS:
    for r in rooms: _q_of.setdefault(r, []).append(qid)
def _tag_hot(m):
    lid = m.group(1); return m.group(0)[:-1] + ' data-q="%s">' % " ".join(_q_of.get(lid, []))
svg = re.sub(r'<g class="hot[^"]*" data-lieu="([^"]+)"[^>]*>', _tag_hot, svg)
# ids sur les formes de zone (pour le masque) : z-<lieu>-<n>
def _tag_zones(m):
    head, body = m.group(1), m.group(2); lid = re.search(r'data-lieu="([^"]+)"', head).group(1); n = [0]
    def _z(mm):
        n[0] += 1; return mm.group(0)[:-2].rstrip("/") + ' id="z-%s-%d"/>' % (lid, n[0]) if mm.group(0).endswith("/>") else mm.group(0)
    return head + re.sub(r'<(?:rect|polygon)[^>]*class="zone"[^>]*/>', _z, body)
svg = re.sub(r'(<g class="hot[^"]*" data-lieu="[^"]+"[^>]*>)(.*?</g>)', _tag_zones, svg, flags=re.S)
n_z = len(re.findall(r'id="z-', svg)); assert n_z > 700, n_z
# voile + masque, insérés juste avant la couche interactive
k = svg.index('<g id="interactif"')
svg = svg[:k] + ('<defs><mask id="qMask" maskUnits="userSpaceOnUse" x="0" y="0" width="2160" height="1681">'
                 '<rect x="0" y="0" width="2160" height="1681" fill="white"/><g id="qMaskHoles"></g></mask></defs>'
                 '<rect id="qVoile" x="0" y="0" width="2160" height="1681" fill="#0f0e13" opacity="0" mask="url(#qMask)" pointer-events="none"/>\n') + svg[k:]
svg = svg.replace("</style>", "svg.quartier #qVoile{opacity:.78}svg.quartier .hot:not(.q-on) .zone{pointer-events:none}svg.quartier .hot.q-on .zone{fill-opacity:.07;stroke-width:1.5}</style>", 1)
ids = re.findall(r'data-lieu="([^"]+)"', svg)
assert len(ids) == len(set(ids)) == len(LIEUX), (len(ids), len(set(ids)), len(LIEUX))
N_LIEUX = len(ids)
missing = set(ids) - set(LIEUX); extra = set(LIEUX) - set(ids)
assert not missing and not extra, (missing, extra)
# le SVG ne doit contenir ni script ni ressource externe
assert "<script" not in svg and "href=" not in svg and "url(http" not in svg

# ---------- 1b. Illustrations (WebP embarquées) ----------
import base64
IMG_DIR = HERE / "img"
IMGS = {}
for f in sorted(IMG_DIR.glob("*.webp")):
    IMGS[f.stem] = "data:image/webp;base64," + base64.b64encode(f.read_bytes()).decode()
print("illustrations :", ", ".join(IMGS))

# ---------- 2. Données JS ----------
old_m = re.search(r'const LIEUX=(\{.*?\});\n', atlas, re.S)
OLD = json.loads(old_m.group(1))
SAIT_KEEP = {"eglise", "cellules", "fiel", "hautesecu", "acces1", "acces2"}
SAIT_OVERRIDE = {
    "fiel": "La fosse protège l'accès aux cellules de haute sécurité et sert de réserve aux Pokémon de type Poison de Sœur Automne.",
    "eglise": "Centre et cœur du complexe : c'est là que se tiennent les messes noires de la secte, l'introduction des nouveaux membres, les annonces faites aux adeptes et les sacrifices.",
    "cellules": "Plusieurs sacrifices s'en sont échappés au fil du temps : Yumi lorsqu'elle était jeune, Pierre et Melkio, les captifs libérés lors du raid des ADT…",
    "acces1": "Elle débouche, par la ville enfouie, sur l'accès clandestin de la pizzeria de Dark (décision de l'auteur, 19/10) : c'est l'entrée et la sortie du raid, sans garde.",
}
lieux_js = {}
for lid, l in LIEUX.items():
    lieux_js[lid] = {
        "nom": l["nom"], "secteur": l["secteur"], "statut": l["statut"],
        "fonction": l["fonction"], "acces": l["acces"], "desc": l["desc"],
        "occ": l.get("occ", []), "liens": l.get("liens", []), "note": l.get("note", ""),
        "sait": SAIT_OVERRIDE.get(lid, OLD.get(lid, {}).get("sait", "") if lid in SAIT_KEEP else ""),
        "img": l.get("img", ""),
        "galerie": [list(g) for g in l.get("galerie", [])],
    }
# cohérence des liens
for lid, l in lieux_js.items():
    for x in l["liens"]:
        assert x in lieux_js, (lid, x)
n_canon = sum(1 for l in lieux_js.values() if l["statut"] == "canon")

JS_DATA = ("const LIEUX=" + json.dumps(lieux_js, ensure_ascii=False) + ";\n"
           "const LIEUX_IMG=" + json.dumps(IMGS) + ";\n"
           "const SECTEURS=" + json.dumps(SECTEURS, ensure_ascii=False) + ";\n"
           "const STATUTS=" + json.dumps(STATUTS, ensure_ascii=False) + ";\n")

# ---------- 3. CSS ----------
CSS = """
/* ----- Repaire de Corrésone ----- */
.carte-bar{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin:0 0 12px}
.carte-bar .grp{display:flex;gap:4px;align-items:center;background:var(--panel2);border:1px solid var(--line);border-radius:20px;padding:3px}
.carte-bar .grp button{background:none;border:1px solid transparent;color:var(--dim);border-radius:16px;padding:6px 13px;cursor:pointer;font:inherit;font-size:.8rem;white-space:nowrap}
.carte-bar .grp button:hover{color:var(--txt)}
.carte-bar .grp button.active{background:var(--red-d);border-color:var(--red);color:#fff}
.carte-bar .grp.zoom button{padding:6px 10px;min-width:34px}
.carte-bar .hint{color:var(--dim);font-size:.78rem;margin-left:auto;font-style:italic}
.carte-quartier{margin:0 0 10px;padding:10px 14px;border-left:3px solid var(--red);background:var(--panel2);border-radius:0 10px 10px 0}
.carte-quartier b{display:block;font-size:.9rem;color:var(--txt);margin-bottom:3px}
.carte-quartier p{margin:0;font-size:.82rem;color:var(--dim);line-height:1.5}
.carte-frame{position:relative;background:#0f0e13;border:1px solid var(--line);border-radius:10px;overflow:auto;max-height:78vh;box-shadow:inset 0 0 40px #000}
.carte-frame svg{display:block;width:calc(var(--carte-zoom,1) * 100%);height:auto;min-width:320px}
.carte-frame svg .hot.sel .zone{stroke-width:5;fill-opacity:.16}
.carte-frame svg .hot[data-lieu='galeries_annexes'] .zone{stroke-width:8!important;stroke-opacity:0}
.carte-frame svg .hot[data-lieu='galeries_annexes']:hover .zone,.carte-frame svg .hot[data-lieu='galeries_annexes']:focus .zone{fill-opacity:.13}
.carte-frame svg .hot[data-lieu='galeries_annexes'].sel .zone{fill-opacity:.18}
.carte-frame.drag{cursor:grabbing}
.carte-cartouche{margin:12px 2px 0;padding:12px 14px;border:1px solid var(--line);border-radius:10px;background:var(--panel2)}
.carte-titre{display:flex;flex-wrap:wrap;gap:4px 14px;align-items:baseline;margin-bottom:8px}
.carte-titre b{font-size:.95rem;letter-spacing:.04em;text-transform:uppercase;color:var(--txt)}
.carte-titre span{font-size:.76rem;color:var(--dim);font-style:italic}
.carte-legende{display:flex;flex-wrap:wrap;gap:6px 18px;margin:0;color:var(--dim);font-size:.78rem}
.carte-legende-plan{margin-top:8px;padding-top:8px;border-top:1px dashed var(--line)}
.carte-legende i.sw{display:inline-block;width:14px;height:9px;border-radius:1px;margin-right:6px;vertical-align:-1px;background:#3d3a45;border:2px solid #9a95a6}
.carte-legende i.sw-porte{width:7px;height:7px;background:#e3cf8e;border:none}
.carte-legende i.sw-secret{width:22px;height:0;background:none;border:none;border-top:3px dashed #f0b43c;vertical-align:2px}
.carte-legende i.sw-gal{width:22px;height:6px;background:#4b4852;border:2px solid #9a93a8;border-radius:3px}
.carte-legende i.sw-boyau{width:22px;height:4px;background:#34303b;border:2px solid #5e586b;border-radius:3px}
.carte-bar select{background:none;border:1px solid transparent;color:var(--dim);border-radius:16px;padding:6px 10px;font:inherit;font-size:.8rem;cursor:pointer}
.carte-bar select.active{background:var(--red-d);border-color:var(--red);color:#fff}
.carte-bar select option{background:var(--panel);color:var(--txt)}
.carte-legende i{display:inline-block;width:11px;height:11px;border-radius:50%;margin-right:6px;vertical-align:-1px;border:1px solid #0008}
.st-canon{background:#e0567a}.st-amenagement{background:#5fb7c4}.st-proposition{background:#8f8a99}.st-indetermine{background:#c9a24a}
.lieux-index{margin-top:26px}
.lieux-index .rep-bar{margin-bottom:16px}
.lieux-sect{margin-bottom:18px}
.lieux-sect h3{font-family:Georgia,serif;font-size:1.02rem;letter-spacing:.04em;color:#e9dfe6;margin:0 0 9px;padding-bottom:6px;border-bottom:1px solid var(--line)}
.lieux-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:7px}
.lieu-btn{display:flex;align-items:center;gap:9px;text-align:left;background:var(--panel2);border:1px solid var(--line);border-radius:8px;padding:8px 11px;color:var(--txt);cursor:pointer;font:inherit;font-size:.84rem}
.lieu-btn:hover{border-color:#b36b7a;background:#241c28}
.lieu-btn i{flex:0 0 10px;width:10px;height:10px;border-radius:50%;border:1px solid #0008}
.lieu-btn small{display:block;color:var(--dim);font-size:.72rem;margin-top:2px}
.lieu-btn.hidden{display:none}
.lieux-sect.hidden{display:none}
.lieu-fig{margin:0 0 18px;border:1px solid #49323f;border-radius:10px;overflow:hidden;background:#0b0a0d}
.lieu-fig img{display:block;width:100%;height:auto}
.lieu-fig figcaption{padding:7px 11px;font-size:.72rem;color:var(--dim);font-style:italic}
.drawer-avatar.has-img img{width:100%;height:100%;object-fit:cover}
.galeries-strip{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px;margin:16px 0 0}
.galeries-strip figure{margin:0;border:1px solid var(--line);border-radius:10px;overflow:hidden;background:var(--panel)}
.galeries-strip img{display:block;width:100%;height:auto;aspect-ratio:4/3;object-fit:cover}
.galeries-strip figcaption{padding:9px 12px;font-size:.78rem;color:var(--dim);line-height:1.45}
.galeries-strip figcaption b{display:block;color:var(--txt);font-weight:600;margin-bottom:2px}
.lieu-gal{display:grid;grid-template-columns:repeat(auto-fill,minmax(120px,1fr));gap:8px;margin:-8px 0 18px}
.lieu-gal button{padding:0;border:1px solid #49323f;border-radius:8px;overflow:hidden;background:#0b0a0d;cursor:pointer;text-align:left;color:var(--dim);font:inherit;font-size:.7rem}
.lieu-gal button img{display:block;width:100%;aspect-ratio:4/3;object-fit:cover}
.lieu-gal button span{display:block;padding:5px 7px;line-height:1.3}
.lieu-gal button.active{border-color:var(--gold)}
.drawer-glyph{font-family:Georgia,serif;font-size:38px;color:#e9c89b;background:radial-gradient(circle at 40% 35%,#4a2f3a,#1a141d 70%)}
.lieu-statut{display:inline-block;font-size:10px;letter-spacing:.14em;text-transform:uppercase;border:1px solid;border-radius:3px;padding:2px 8px;margin-top:6px}
.lieu-statut.canon{color:#f0a3ba;border-color:#8e3b55}.lieu-statut.amenagement{color:#8fd3dc;border-color:#2f6d75}
.lieu-statut.proposition{color:#b9b3c2;border-color:#55505e}.lieu-statut.indetermine{color:#e2c77a;border-color:#7d6530}
.lieu-note{margin-top:10px;padding:9px 12px;border-left:2px solid var(--gold);background:#1d1822;color:#cbbfca;font-size:.82rem;line-height:1.5}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chips button{background:var(--panel2);border:1px solid var(--line);color:var(--txt);border-radius:16px;padding:5px 11px;cursor:pointer;font:inherit;font-size:.8rem}
.chips button:hover{border-color:#b36b7a}
.chips button.perso::before{content:'✦ ';color:var(--red)}
.chips button.lieu::before{content:'◆ ';color:var(--gold)}
.drawer-actions{display:flex;gap:8px;margin:0 0 18px}
.drawer-actions button{background:var(--red-d);border:1px solid var(--red);color:#fff;border-radius:8px;padding:7px 13px;cursor:pointer;font:inherit;font-size:.8rem}
.drawer-actions button.sec{background:var(--panel2);border-color:var(--line);color:var(--txt)}
.side-lieu{display:flex;align-items:center;gap:9px;text-align:left;padding:8px 12px 8px 18px;background:transparent;color:#aaa0ad;border:0;border-radius:7px;font-size:12px;width:100%;line-height:1.3;cursor:pointer;font-family:inherit;position:relative}
.side-lieu::before{content:'◆';color:var(--gold);font-size:9px}
.side-lieu:hover{background:#231b26;color:#f0e6ee}
@media (max-width:720px){.carte-frame{max-height:62vh}.carte-bar .hint{display:none}}
"""

# ---------- 4. HTML de la vue ----------
def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
index_html = []
for sid, sname in SECTEURS:
    items = [(lid, l) for lid, l in LIEUX.items() if l["secteur"] == sid]
    items.sort(key=lambda kv: ({"canon": 0, "amenagement": 1, "proposition": 2, "indetermine": 3}[kv[1]["statut"]], kv[1]["nom"]))
    btns = "".join(
        f'<button class="lieu-btn" data-lieuid="{lid}" data-txt="{esc((l["nom"]+" "+l["fonction"]).lower())}">'
        f'<i class="st-{l["statut"]}"></i><span>{esc(l["nom"])}<small>{esc(l["fonction"])}</small></span></button>'
        for lid, l in items)
    index_html.append(f'<section class="lieux-sect" data-sect="{sid}"><h3>{esc(sname)} <span class="n" style="font-size:.7rem;color:var(--dim)">({len(items)})</span></h3><div class="lieux-grid">{btns}</div></section>')
index_html = "".join(index_html)

VUE = f"""
<div class="vue" id="vue-qg" hidden>
<section class="view-hero"><div><span class="eyebrow">Dossier · Quartier général</span><h2>Le repaire sous Corrésone</h2><p>Un seul niveau, sans escalier. « Une toile sombre d'un architecte qui tenait plus de l'araignée démente, tissée autour de la croix noire de l'église. » Clique sur une salle pour ouvrir sa fiche ; bascule entre le plan annoté et la vue immersive, entre la carte complète et les seuls couloirs principaux, ou isole un quartier. Le repaire est rarement plein : hormis la Main et les prisonniers, on n'y dort que lorsqu'on est de garde ou de service — Cabalistes et Évêques compris.</p></div><div class="hero-stat-list"><div class="hero-stat"><b>{N_LIEUX}</b><small>Lieux</small></div><div class="hero-stat"><b>{n_canon}</b><small>Attestés</small></div><div class="hero-stat"><b>3</b><small>Issues secrètes</small></div></div></section>
<div class="carte-bar">
 <div class="grp" role="group" aria-label="Rendu"><button id="cvAnnot" class="active" type="button">Plan annoté</button><button id="cvImm" type="button">Vue immersive</button></div>
 <div class="grp" role="group" aria-label="Étiquettes"><button id="cvSynth" class="active" type="button">Synthèse</button><button id="cvDetail" type="button">Détail</button></div>
 <div class="grp" role="group" aria-label="Réseau"><button id="cvComplet" class="active" type="button">Carte complète</button><button id="cvPrincipal" type="button">Couloirs principaux</button></div>
 <div class="grp" role="group" aria-label="Quartier"><select id="cvQuartier" aria-label="Isoler un quartier"><option value="">Tout le repaire</option>{''.join(f'<option value="{q}">{esc(n)}</option>' for q, n, _, _ in QUARTIERS)}</select></div>
 <div class="grp zoom" role="group" aria-label="Zoom"><button id="czMoins" type="button" title="Réduire">−</button><button id="czFit" type="button" title="Ajuster à la largeur">Ajuster</button><button id="czPlus" type="button" title="Agrandir">+</button></div>
 <div class="grp" role="group" aria-label="Export"><button id="cxPng" type="button" title="Télécharger le plan tel qu'affiché (PNG, 4320 px)">PNG</button><button id="cxSvg" type="button" title="Télécharger le plan tel qu'affiché (SVG)">SVG</button></div>
 <span class="hint">Clic sur une salle : fiche · glisser pour déplacer quand le plan est agrandi</span>
</div>
<div class="carte-quartier" id="qDesc" hidden><b id="qDescTitre"></b><p id="qDescTexte"></p></div>
<div class="carte-frame" id="carteFrame">
{svg}
</div>
<div class="carte-cartouche">
 <div class="carte-titre"><b>Corrésone — repaire des Adorateurs des Ténèbres</b><span>niveau principal · plan d'atlas V3.2 · les secteurs en pointillés sont des propositions non attestées par les récits</span></div>
 <div class="carte-legende"><span><i class="st-canon"></i>Lieu attesté par les récits</span><span><i class="st-amenagement"></i>Aménagement décidé par l'auteur</span><span><i class="st-proposition"></i>Fonction proposée (non canon)</span><span><i class="st-indetermine"></i>Destination indéterminée</span></div>
 <div class="carte-legende carte-legende-plan"><span><i class="sw" style="border-color:#c2606f"></i>Lieu attesté par les récits</span><span><i class="sw" style="border-color:#a97be0"></i>Bureaux et appartements</span><span><i class="sw" style="border-color:#6aa06a"></i>Fiel / haute sécurité (passage obligé)</span><span><i class="sw" style="border-color:#9a95a6"></i>Salle secondaire (fonction proposée)</span><span><i class="sw" style="border-color:#4fb3a3"></i>Ajouts demandés (service, entraînement, conseil…)</span><span><i class="sw" style="border-color:#d19a4a"></i>Quartier des Cabalistes et des Évêques</span><span><i class="sw" style="border-color:#b8b25a"></i>Poste de garde</span><span><i class="sw" style="border-color:#c94a7a"></i>Aile de la Main (garde de Psykos)</span><span><i class="sw sw-porte"></i>Porte / ouverture</span><span><i class="sw sw-secret"></i>Passage secret (tracé de l'auteur)</span><span><i class="sw sw-gal"></i>Galerie principale</span><span><i class="sw sw-boyau"></i>Galerie annexe (boyau)</span></div>
</div>
<div class="lieux-index">
<div class="rep-bar"><input id="qLieu" type="search" placeholder="Nom de salle, fonction…" autocomplete="off" aria-label="Chercher un lieu"><select id="fSect" aria-label="Filtrer par secteur"><option value="">Tous les secteurs</option>{''.join(f'<option value="{sid}">{esc(sn)}</option>' for sid, sn in SECTEURS)}</select><span id="lCount" class="rep-count"></span></div>
{index_html}
</div>
</div>
"""

# ---------- 5. JS ----------
JSON_QUARTIERS = json.dumps({q: [n, d] for q, n, _, d in QUARTIERS}, ensure_ascii=False)
JS = JS_DATA + r"""
// ----- Repaire de Corrésone -----
const carteSvg=document.getElementById('carte-qg');
const carteFrame=document.getElementById('carteFrame');
let carteZoom=1;
function setZoom(z){carteZoom=Math.min(3,Math.max(1,z));carteFrame.style.setProperty('--carte-zoom',carteZoom);}
document.getElementById('czPlus').onclick=()=>setZoom(carteZoom+0.5);
document.getElementById('czMoins').onclick=()=>setZoom(carteZoom-0.5);
document.getElementById('czFit').onclick=()=>setZoom(1);
function setVueCarte(imm,remember=true){
 carteSvg.classList.toggle('vue-immersive',imm);
 document.getElementById('cvImm').classList.toggle('active',imm);
 document.getElementById('cvAnnot').classList.toggle('active',!imm);
 if(remember)try{localStorage.setItem('adt-carte',imm?'immersive':'annotee');}catch(e){}
}
document.getElementById('cvAnnot').onclick=()=>setVueCarte(false);
document.getElementById('cvImm').onclick=()=>setVueCarte(true);
function setEtiquettes(synth,remember=true){
 carteSvg.classList.toggle('synthese',synth);
 document.getElementById('cvSynth').classList.toggle('active',synth);
 document.getElementById('cvDetail').classList.toggle('active',!synth);
 if(remember)try{localStorage.setItem('adt-carte-lbl',synth?'synthese':'detail');}catch(e){}
}
document.getElementById('cvSynth').onclick=()=>setEtiquettes(true);
document.getElementById('cvDetail').onclick=()=>setEtiquettes(false);
function setBoyaux(complet,remember=true){
 carteSvg.classList.toggle('sans-boyaux',!complet);
 document.getElementById('cvComplet').classList.toggle('active',complet);
 document.getElementById('cvPrincipal').classList.toggle('active',!complet);
 if(remember)try{localStorage.setItem('adt-carte-boyaux',complet?'complet':'principal');}catch(e){}
}
document.getElementById('cvComplet').onclick=()=>setBoyaux(true);
document.getElementById('cvPrincipal').onclick=()=>setBoyaux(false);
const QUARTIERS=__JSON_QUARTIERS__;
const qMaskHoles=document.getElementById('qMaskHoles');
function setQuartier(q,remember=true){
 const sel=document.getElementById('cvQuartier');sel.value=q||'';sel.classList.toggle('active',!!q);
 const d=document.getElementById('qDesc');if(q&&QUARTIERS[q]){document.getElementById('qDescTitre').textContent=QUARTIERS[q][0];document.getElementById('qDescTexte').textContent=QUARTIERS[q][1];d.hidden=false;}else d.hidden=true;
 carteSvg.classList.toggle('quartier',!!q);
 while(qMaskHoles.firstChild)qMaskHoles.removeChild(qMaskHoles.firstChild);
 carteSvg.querySelectorAll('.hot[data-lieu]').forEach(g=>{
  const on=!!q&&(g.dataset.q||'').split(' ').includes(q);g.classList.toggle('q-on',on);
  if(on)g.querySelectorAll('.zone').forEach(z=>{const c=z.cloneNode(false);c.removeAttribute('id');c.removeAttribute('class');c.setAttribute('fill','black');c.setAttribute('stroke','black');c.setAttribute('stroke-width','14');c.setAttribute('stroke-linejoin','round');qMaskHoles.appendChild(c);});
 });
 if(remember)try{localStorage.setItem('adt-carte-quartier',q||'');}catch(e){}
}
document.getElementById('cvQuartier').onchange=e=>setQuartier(e.target.value);
// --- export du plan tel qu'affiché
function carteSvgTexte(){
 const c=carteSvg.cloneNode(true);c.setAttribute('xmlns','http://www.w3.org/2000/svg');c.setAttribute('width','2160');c.setAttribute('height','1681');c.removeAttribute('id');
 const st=document.createElement('style');
 st.textContent='.hot .zone{fill-opacity:0;stroke-width:0}svg.quartier #qVoile{opacity:.78}svg.quartier .hot.q-on .zone{fill-opacity:.07;stroke:#f0b43c;stroke-width:1.5}';
 c.insertBefore(st,c.firstChild);
 return '<?xml version="1.0" encoding="UTF-8"?>\n'+new XMLSerializer().serializeToString(c);
}
function telecharger(blob,nom){const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=nom;document.body.appendChild(a);a.click();setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove();},2000);}
function nomExport(ext){const v=carteSvg.classList.contains('vue-immersive')?'immersif':'annote';const q=document.getElementById('cvQuartier').value;return 'Plan_QG_Corresone_'+v+(carteSvg.classList.contains('sans-boyaux')?'_principaux':'')+(q?'_'+q:'')+'.'+ext;}
document.getElementById('cxSvg').onclick=()=>telecharger(new Blob([carteSvgTexte()],{type:'image/svg+xml;charset=utf-8'}),nomExport('svg'));
document.getElementById('cxPng').onclick=()=>{
 const b=document.getElementById('cxPng');b.disabled=true;b.textContent='…';
 const img=new Image();const url=URL.createObjectURL(new Blob([carteSvgTexte()],{type:'image/svg+xml;charset=utf-8'}));
 img.onload=()=>{const k=2,cv=document.createElement('canvas');cv.width=2160*k;cv.height=1681*k;const cx=cv.getContext('2d');cx.fillStyle='#0f0e13';cx.fillRect(0,0,cv.width,cv.height);cx.drawImage(img,0,0,cv.width,cv.height);URL.revokeObjectURL(url);
  cv.toBlob(bl=>{telecharger(bl,nomExport('png'));b.disabled=false;b.textContent='PNG';},'image/png');};
 img.onerror=()=>{URL.revokeObjectURL(url);b.disabled=false;b.textContent='PNG';alert('Export PNG impossible dans ce navigateur ; utilisez SVG.');};
 img.src=url;
};
try{if(localStorage.getItem('adt-carte')==='immersive')setVueCarte(true,false);
    const q0=localStorage.getItem('adt-carte-quartier');if(q0)setQuartier(q0,false);
    if(localStorage.getItem('adt-carte-lbl')==='detail')setEtiquettes(false,false);
    if(localStorage.getItem('adt-carte-boyaux')==='principal')setBoyaux(false,false);}catch(e){}
// glisser-déplacer quand le plan est agrandi
(function(){let down=false,sx=0,sy=0,sl=0,st=0,moved=false;
 carteFrame.addEventListener('pointerdown',e=>{if(carteZoom<=1||e.button!==0)return;down=true;moved=false;sx=e.clientX;sy=e.clientY;sl=carteFrame.scrollLeft;st=carteFrame.scrollTop;carteFrame.classList.add('drag');});
 window.addEventListener('pointermove',e=>{if(!down)return;const dx=e.clientX-sx,dy=e.clientY-sy;if(Math.abs(dx)+Math.abs(dy)>4)moved=true;carteFrame.scrollLeft=sl-dx;carteFrame.scrollTop=st-dy;});
 window.addEventListener('pointerup',()=>{down=false;carteFrame.classList.remove('drag');});
 carteFrame.addEventListener('click',e=>{if(moved){e.stopPropagation();e.preventDefault();moved=false;}},true);
})();
let activeLieu=null;
function surlignerLieu(id){
 carteSvg.querySelectorAll('.hot.sel').forEach(g=>g.classList.remove('sel'));
 const g=id?carteSvg.querySelector('.hot[data-lieu="'+id+'"]'):null;
 if(g)g.classList.add('sel');
}
function voirSurPlan(id){
 fermerFiche();afficherVue('qg');if(id==='galeries_annexes')setBoyaux(true);surlignerLieu(id);
 const g=carteSvg.querySelector('.hot[data-lieu="'+id+'"]');if(!g)return;
 requestAnimationFrame(()=>{
  const fr=carteFrame.getBoundingClientRect(),r=g.getBoundingClientRect();
  carteFrame.scrollTo({left:carteFrame.scrollLeft+(r.left+r.width/2)-(fr.left+fr.width/2),top:carteFrame.scrollTop+(r.top+r.height/2)-(fr.top+fr.height/2),behavior:'smooth'});
  carteFrame.scrollIntoView({behavior:'smooth',block:'center'});
  try{g.focus({preventScroll:true});}catch(e){}
 });
}
function ouvrirLieu(id){
 const l=LIEUX[id];if(!l)return;
 activePerson=null;activeLieu=id;surlignerLieu(id);
 document.getElementById('modal').classList.add('open');
 document.body.classList.add('drawer-open');
 const sect=(SECTEURS.find(s=>s[0]===l.secteur)||[,''])[1];
 const glyph={rituel:'✠',fiel:'☠',pouvoir:'♜',vie:'⌂',galeries:'⛏'}[l.secteur]||'◆';
 const im=l.img&&LIEUX_IMG[l.img]?LIEUX_IMG[l.img]:'';
 let c='<div class="drawer-actions"><button type="button" data-voirplan="'+id+'">Voir sur le plan</button></div>';
 if(im)c+='<figure class="lieu-fig"><img id="lieuFigImg" src="'+im+'" alt="'+esc(l.nom)+'"><figcaption id="lieuFigCap">'+esc(l.nom)+' — vue principale</figcaption></figure>';
 if(im&&l.galerie&&l.galerie.length){const vues=[[l.img,l.nom+' — vue principale']].concat(l.galerie);c+='<div class="lieu-gal">'+vues.map((g,i)=>'<button type="button" class="'+(i===0?'active':'')+'" data-gal="'+esc(g[0])+'" data-cap="'+esc(g[1])+'"><img src="'+(LIEUX_IMG[g[0]]||'')+'" alt=""><span>'+esc(g[1])+'</span></button>').join('')+'</div>';}
 c+='<section><h4>Fonction</h4><p class="bio">'+esc(l.fonction)+'</p></section>';
 c+='<section><h4>Accès et liaisons</h4><p class="bio">'+esc(l.acces)+'</p></section>';
 c+='<section><h4>Description</h4><div class="bio">'+esc(l.desc)+'</div>'+(l.note?'<div class="lieu-note">'+esc(l.note)+'</div>':'')+'</section>';
 if(l.sait&&l.sait!=='?')c+='<section><h4>Ce qu\u2019on en sait</h4><div class="bio">'+esc(l.sait)+'</div></section>';
 if(l.occ&&l.occ.length)c+='<section><h4>Personnes liées</h4><div class="chips">'+l.occ.filter(i=>D[i]).map(i=>'<button type="button" class="perso" data-persolink="'+i+'">'+esc(D[i].alias)+'</button>').join('')+'</div></section>';
 if(l.liens&&l.liens.length)c+='<section><h4>Lieux liés</h4><div class="chips">'+l.liens.filter(x=>LIEUX[x]).map(x=>'<button type="button" class="lieu" data-lieulink="'+x+'">'+esc(LIEUX[x].nom)+'</button>').join('')+'</div></section>';
 c+='<section><h4>Statut documentaire</h4><p class="bio">'+esc(STATUTS[l.statut]||l.statut)+'. Source : plan du QG V3.2 (19/10/2026), journal des décisions d’implantation.</p></section>';
 document.getElementById('sheet').innerHTML='<div class="drawer-head"><span class="drawer-avatar '+(im?'has-img':'drawer-glyph')+'" aria-hidden="true">'+(im?'<img src="'+im+'" alt="">':glyph)+'</span><div class="drawer-head-info"><div class="drawer-rank">Repaire de Corrésone · '+esc(sect)+'</div><h3>'+esc(l.nom)+'</h3><span class="lieu-statut '+l.statut+'">'+esc(STATUTS[l.statut]||'')+'</span></div><button type="button" class="drawer-close" aria-label="Fermer">×</button></div>'+
  '<div class="drawer-body" id="drawerBody">'+c+'</div>';
}
document.getElementById('sheet').addEventListener('click',e=>{
 const v=e.target.closest('[data-voirplan]');if(v){voirSurPlan(v.dataset.voirplan);return;}
 const p=e.target.closest('[data-persolink]');if(p){ouvrirPersonne(Number(p.dataset.persolink));return;}
 const q=e.target.closest('[data-lieulink]');if(q){ouvrirLieu(q.dataset.lieulink);return;}
 const g=e.target.closest('[data-gal]');if(g){const im=document.getElementById('lieuFigImg'),cap=document.getElementById('lieuFigCap');if(im&&LIEUX_IMG[g.dataset.gal]){im.src=LIEUX_IMG[g.dataset.gal];cap.textContent=g.dataset.cap;}g.parentElement.querySelectorAll('button').forEach(b=>b.classList.toggle('active',b===g));return;}
});
carteSvg.addEventListener('click',e=>{const g=e.target.closest('.hot[data-lieu]');if(g)ouvrirLieu(g.dataset.lieu);});
carteSvg.addEventListener('keydown',e=>{if(e.key!=='Enter'&&e.key!==' ')return;const g=e.target.closest('.hot[data-lieu]');if(g){e.preventDefault();ouvrirLieu(g.dataset.lieu);}});
document.querySelectorAll('.lieu-btn').forEach(b=>b.onclick=()=>ouvrirLieu(b.dataset.lieuid));
document.querySelectorAll('.side-lieu').forEach(b=>b.onclick=()=>{afficherVue('qg');ouvrirLieu(b.dataset.lieu);});
function renderLieux(){
 const q=norm(document.getElementById('qLieu').value.trim()),fs=document.getElementById('fSect').value;let n=0;
 document.querySelectorAll('.lieux-sect').forEach(s=>{let k=0;
  s.querySelectorAll('.lieu-btn').forEach(b=>{const ok=(!fs||s.dataset.sect===fs)&&(!q||norm(b.dataset.txt).indexOf(q)>=0);b.classList.toggle('hidden',!ok);if(ok)k++;});
  s.classList.toggle('hidden',k===0);n+=k;});
 document.getElementById('lCount').textContent=n+' lieu'+(n>1?'x':'');
}
document.getElementById('qLieu').oninput=renderLieux;document.getElementById('fSect').onchange=renderLieux;renderLieux();
"""

JS = JS.replace("__JSON_QUARTIERS__", JSON_QUARTIERS)
# ---------- 6. Injection (atlas à jour, onglet QG existant) ----------
out = atlas
cro = re.search(r'<details class="plan-croquis">.*?</details>', out, re.S).group(0)
STRIP = ('<div class="galeries-strip"><figure><img src="' + IMGS["couloir_principal"] + '" alt="Galerie principale du repaire" loading="lazy"><figcaption><b>Galeries principales</b>Rayons et anneaux de la toile : voûtes appareillées, dallage usé au centre, torchères à intervalles réguliers.</figcaption></figure>'
         '<figure><img src="' + IMGS["couloir_extremite"] + '" alt="Galerie d\'extrémité" loading="lazy"><figcaption><b>Galeries des extrémités</b>Courts couloirs et prolongements : roche brute, torches rares, rigole d\'eau au sol.</figcaption></figure>'
         '<figure><img src="' + IMGS["boyau"] + '" alt="Galerie annexe (boyau)" loading="lazy"><figcaption><b>Galeries annexes (boyaux)</b>Boyaux étroits creusés sans plan autour des galeries : roche nue, aucune torche, brèches dans les parois, croisements, culs-de-sac. Masquables avec « Couloirs principaux ».</figcaption></figure></div>')
VUE = VUE.replace('<div class="lieux-index">', STRIP + '<div class="plan-croquis-wrap" style="margin-top:14px">' + cro + "<p class=\"plan-note\">Croquis d'origine : VLT, 29/09. Plan V3.1 du 17/10/2026, réconcilié avec les parcours de Sam, de Yumi et de Dark ; les pointillés signalent les secteurs proposés, non arrêtés par les récits.</p></div>\n<div class=\"lieux-index\">")

a = out.find('<div class="vue" id="vue-qg" hidden>'); b = out.find('<div class="vue" id="vue-pokemons" hidden>')
assert 0 < a < b
out = out[:a] + VUE + out[b:]
old_block = re.search(r"const LIEUX=\{.*?\};\nfunction ouvrirLieu\(id\)\{.*?\n\}\ndocument\.querySelectorAll\('\[data-lieu\]'\)[^\n]*\n", out, re.S)
assert old_block, "bloc LIEUX/ouvrirLieu introuvable"
out = out.replace(old_block.group(0), '')
assert 'const LIEUX=' not in out and 'function ouvrirLieu' not in out
tab_old = '<button class="tab" data-vue="qg"><span class="nav-symbol" aria-hidden="true">⌖</span> QG</button>'
assert tab_old in out
out = out.replace(tab_old, '<button class="tab" data-vue="qg"><span class="nav-symbol" aria-hidden="true">⌖</span> QG <span class="n">%d</span></button>' % N_LIEUX)
side_old = '<button class="side-jump" data-jump="annexe">Annexe</button>\n </div>'
assert side_old in out
out = out.replace(side_old, side_old + """
 <div class="side-label">Repaire de Corrésone</div>
 <div class="side-ranks">
  <button class="side-lieu" data-lieu="eglise">Église souterraine</button>
  <button class="side-lieu" data-lieu="cellules">Cellules des sacrifices</button>
  <button class="side-lieu" data-lieu="fiel">Oubliettes du Fiel</button>
  <button class="side-lieu" data-lieu="hautesecu">Haute sécurité</button>
  <button class="side-lieu" data-lieu="pape">Bureau du Pape Sombre</button>
  <button class="side-lieu" data-lieu="psykos">Bureau de Sœur Psykos</button>
  <button class="side-lieu" data-lieu="main">Aile de la Main</button>
 </div>""")
out = out.replace("48 fiches de l'Ordre · accès hors ligne aux dossiers.", "48 fiches de l'Ordre · %d lieux du repaire · accès hors ligne aux dossiers." % N_LIEUX)
out = out.replace(" activePerson=null;\n}", " activePerson=null;\n if(typeof activeLieu!=='undefined'){activeLieu=null;if(typeof surlignerLieu==='function')surlignerLieu(null);}\n}", 1)
assert "surlignerLieu(null)" in out
head_end = out.find("</style></head>")
head = out[:head_end]
n_before = len(head)
head = re.sub(r'[^{}]*\.hot(?:-tbd)?(?:[ :][^{}]*)?\{[^}]*\}', '', head)
head = re.sub(r'\.plan-svg\{[^}]*\}', '', head)
assert '.hot text' not in head and '.hot-tbd circle' not in head, "anciennes règles .hot encore présentes"
print("CSS ancien plan retiré :", n_before - len(head), "caractères")
out = head + out[head_end:]
out = out.replace("</style></head>", CSS + "</style></head>", 1)
js_anchor = "try{const v=localStorage.getItem('adt-vue');if(v)afficherVue(v,false);}catch(e){}"
assert out.count(js_anchor) == 1
out = out.replace(js_anchor, JS + "\n" + js_anchor)
dest = OUT / "Atlas_Noir_Adorateurs_des_Tenebres.html"
dest.write_text(out, encoding="utf-8")
print("écrit", dest, len(out), "octets ;", len(LIEUX), "lieux ;", n_canon, "attestés")
