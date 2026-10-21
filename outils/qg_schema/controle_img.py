import json, sys
from PIL import Image, ImageDraw
sys.path.insert(0,'/home/claude/qg_schema'); import qg_model as M
im=Image.open('final/Plan_sans_texte_main_levee.png').convert('RGB'); s=im.size[0]/M.W
ct=json.load(open('trace/controle.json')); d=ImageDraw.Draw(im)
def dot(p,col,r=9):
    x,y=p[0]*s,p[1]*s; d.ellipse([x-r,y-r,x+r,y+r],outline=col,width=4)
for p in ct['taps']: dot(p,(0,200,0))
for p in ct['near']: dot(p,(255,210,0))
for p in ct.get('bridge',[]): dot(p,(0,220,255),7)
for p in ct.get('ext',[]): dot(p,(255,0,255),11)
for st in ct['stops']: dot(st['p'],(255,0,0),12)
for ids in ct.get('isolated',[]):
    for r in ids: 
        d.line([(x*s,y*s) for x,y in r], fill=(255,60,60), width=3)
im.save('final/Controle_main_levee.png'); print('controle ok')
