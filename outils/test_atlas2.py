import asyncio, json, pathlib
from playwright.async_api import async_playwright

HTML = pathlib.Path("/home/claude/atlas2/out/Atlas_Noir_Adorateurs_des_Tenebres.html").resolve().as_uri()
SHOTS = pathlib.Path("/home/claude/atlas2/out/captures"); SHOTS.mkdir(exist_ok=True)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1440, "height": 960})
        errors = []
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        reqs = []
        pg.on("request", lambda r: reqs.append(r.url))
        await pg.goto(HTML)
        await pg.wait_for_timeout(600)
        # onglet
        await pg.click('.tab[data-vue="qg"]')
        await pg.wait_for_timeout(400)
        assert await pg.is_visible("#vue-qg"), "vue non visible"
        assert await pg.text_content("#topPageTitle") == "Le repaire sous Corrésone"
        n = await pg.evaluate("document.querySelectorAll('#carte-qg .hot[data-lieu]').length")
        n_ok = await pg.evaluate("[...document.querySelectorAll('#carte-qg .hot[data-lieu]')].filter(g=>LIEUX[g.dataset.lieu]).length")
        print("zones", n, "avec fiche", n_ok); assert n==n_ok==len(await pg.evaluate("Object.keys(LIEUX)"))
        await pg.screenshot(path=str(SHOTS / "01_onglet_repaire.png"))
        # clic sur une zone (église) via JS dispatch (SVG elements)
        await pg.evaluate("document.querySelector('#carte-qg .hot[data-lieu=\"eglise\"]').dispatchEvent(new MouseEvent('click',{bubbles:true}))")
        await pg.wait_for_timeout(400)
        assert await pg.evaluate("document.getElementById('modal').classList.contains('open')")
        h3 = await pg.text_content("#sheet h3"); print("fiche ouverte :", h3)
        assert h3 == "Église souterraine"
        await pg.screenshot(path=str(SHOTS / "02_fiche_eglise.png"))
        # chip personne → dossier Pape
        await pg.click('#sheet [data-persolink="0"]')
        await pg.wait_for_timeout(300)
        print("dossier personne :", await pg.text_content("#sheet h3"))
        # retour lieu via onglet latéral
        await pg.keyboard.press("Escape")
        await pg.click('.side-lieu[data-lieu="fiel"]')
        await pg.wait_for_timeout(300)
        print("side-lieu :", await pg.text_content("#sheet h3"))
        # lien lieu → lieu
        await pg.click('#sheet [data-lieulink="hautesecu"]')
        await pg.wait_for_timeout(200)
        print("lien lieu :", await pg.text_content("#sheet h3"))
        # Voir sur le plan
        await pg.click('#sheet [data-voirplan]')
        await pg.wait_for_timeout(700)
        sel = await pg.evaluate("document.querySelector('#carte-qg .hot.sel')?.dataset.lieu")
        print("surligné :", sel); assert sel == "hautesecu"
        # vue immersive + détail + zoom
        await pg.click("#cvImm"); await pg.click("#cvDetail"); await pg.wait_for_timeout(300)
        assert await pg.evaluate("document.getElementById('carte-qg').classList.contains('vue-immersive')")
        await pg.screenshot(path=str(SHOTS / "03_vue_immersive.png"))
        vis_txt = await pg.evaluate("[...document.querySelectorAll('#carte-qg #plan-technique text')].filter(t=>t.getClientRects().length).length")
        print("textes techniques visibles en immersif :", vis_txt); assert vis_txt == 0
        await pg.click("#czPlus"); await pg.click("#czPlus"); await pg.wait_for_timeout(300)
        w = await pg.evaluate("document.getElementById('carte-qg').getBoundingClientRect().width/document.getElementById('carteFrame').clientWidth")
        print("zoom ×", round(w, 2))
        await pg.screenshot(path=str(SHOTS / "04_zoom2x.png"))
        await pg.click("#czFit"); await pg.click("#cvAnnot"); await pg.click("#cvSynth")
        # index + recherche
        await pg.fill("#qLieu", "garde"); await pg.wait_for_timeout(200)
        print("recherche 'garde' :", await pg.text_content("#lCount"))
        await pg.fill("#qLieu", "")
        await pg.select_option("#fSect", "fiel"); await pg.wait_for_timeout(200)
        print("secteur fiel :", await pg.text_content("#lCount"))
        await pg.select_option("#fSect", "")
        await pg.click('.lieu-btn[data-lieuid="S19"]'); await pg.wait_for_timeout(200)
        print("index :", await pg.text_content("#sheet h3"))
        await pg.keyboard.press("Escape")
        # clavier sur zone
        await pg.focus('#carte-qg .hot[data-lieu="citerne"]'); await pg.keyboard.press("Enter"); await pg.wait_for_timeout(200)
        print("clavier :", await pg.text_content("#sheet h3"))
        await pg.keyboard.press("Escape")
        # les autres onglets fonctionnent toujours
        await pg.click('.tab[data-vue="repertoire"]'); await pg.wait_for_timeout(200)
        print("répertoire :", await pg.text_content("#rCount"))
        await pg.click('.tab[data-vue="pokemons"]'); await pg.wait_for_timeout(200)
        print("pokémons :", await pg.text_content("#pkCount"))
        await pg.click('.tab[data-vue="orga"]'); await pg.click('.card[data-i="8"]'); await pg.wait_for_timeout(200)
        print("orga :", await pg.text_content("#sheet h3"))
        await pg.keyboard.press("Escape"); await pg.click(".tab[data-vue=\"doctrine\"]"); await pg.wait_for_timeout(200); print("doctrine visible :", await pg.is_visible("#vue-doctrine"))
        await pg.click(".tab[data-vue=\"qg\"]"); await pg.evaluate("document.querySelector('#carte-qg .hot[data-lieu=\"infirmerie\"]').dispatchEvent(new MouseEvent('click',{bubbles:true}))"); await pg.wait_for_timeout(200); print("sait infirmerie :", await pg.evaluate("[...document.querySelectorAll('#sheet h4')].map(h=>h.textContent).join(' | ')"))
        # mobile
        await pg.set_viewport_size({"width": 400, "height": 820})
        await pg.keyboard.press("Escape"); await pg.click('.tab[data-vue="qg"]'); await pg.wait_for_timeout(400)
        await pg.screenshot(path=str(SHOTS / "05_mobile.png"))
        # --- V3.2 : galeries annexes ---
        await pg.keyboard.press("Escape"); await pg.set_viewport_size({"width": 1440, "height": 960}); await pg.click('.tab[data-vue="qg"]'); await pg.wait_for_timeout(300)
        await pg.evaluate("setVueCarte(false);setEtiquettes(true);setBoyaux(true)")
        nb = await pg.evaluate("document.querySelectorAll('#carte-qg #tech-boyaux polygon').length"); print("polygones boyaux (technique) :", nb); assert nb > 1000
        vis = await pg.evaluate("getComputedStyle(document.getElementById('tech-boyaux')).display"); assert vis != 'none'
        await pg.evaluate("document.querySelector('#carte-qg .hot[data-lieu=\"galeries_annexes\"] .zone').dispatchEvent(new MouseEvent('click',{bubbles:true}))"); await pg.wait_for_timeout(300)
        print("fiche boyaux :", await pg.text_content("#sheet h3")); assert await pg.text_content("#sheet h3") == "Galeries annexes (boyaux)"
        await pg.keyboard.press("Escape")
        await pg.click("#cvPrincipal"); await pg.wait_for_timeout(200)
        hid = await pg.evaluate("['tech-boyaux','tech-boyaux-ouvertures','scene-boyaux','scene-boyaux-ouvertures'].map(i=>getComputedStyle(document.getElementById(i)).display)"); print("couloirs principaux → calques boyaux :", hid); assert all(h == 'none' for h in hid)
        zhid = await pg.evaluate("getComputedStyle(document.querySelector('#carte-qg .hot[data-lieu=\"galeries_annexes\"]')).display"); assert zhid == 'none'
        await pg.screenshot(path=str(SHOTS / "06_couloirs_principaux.png"))
        print("mémorisé :", await pg.evaluate("localStorage.getItem('adt-carte-boyaux')"))
        await pg.click("#cvComplet"); await pg.click("#cvImm"); await pg.wait_for_timeout(300)
        vis2 = await pg.evaluate("getComputedStyle(document.getElementById('scene-boyaux')).display"); assert vis2 != 'none'
        await pg.screenshot(path=str(SHOTS / "07_immersif_boyaux.png"))
        await pg.click("#cvAnnot")
        # « Voir sur le plan » depuis la fiche boyaux réaffiche le réseau
        await pg.click("#cvPrincipal"); await pg.click('.lieu-btn[data-lieuid="galeries_annexes"]'); await pg.wait_for_timeout(200); await pg.click('#sheet [data-voirplan]'); await pg.wait_for_timeout(500)
        print("voir sur le plan → complet :", await pg.evaluate("!document.getElementById('carte-qg').classList.contains('sans-boyaux')"))
        await pg.screenshot(path=str(SHOTS / "08_zoom_boyaux.png"))
        ext = sorted({u.split('/')[2] for u in reqs if u.startswith('http')})
        print("hôtes externes sollicités :", ext)
        print("erreurs JS :", errors)
        await b.close()
asyncio.run(main())
