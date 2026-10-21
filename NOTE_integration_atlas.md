# Atlas Noir — intégration du repaire de Corrésone (17/10/2026, base : atlas à jour avec onglet QG, 48 fiches)

## Ce qui change dans `Atlas_Noir_Adorateurs_des_Tenebres.html`
- L'onglet **QG** existant reçoit le vrai plan (73 lieux) à la place du plan de substitution 800 × 800 ; raccourcis latéraux vers les sept lieux majeurs. Le croquis d'origine de VLT (29/09) et la citation du hero sont conservés ; les notes « Ce qu'on en sait » encore valables (église, cellules, Fiel, haute sécurité, infirmerie, deux accès) sont reprises dans les nouvelles fiches. Les règles CSS de l'ancien plan (`.hot text`, `.hot polygon`…) sont retirées : elles écrasaient les attributs du SVG.
- Carte : le SVG « deux vues » de GPT (V3.0), géométrie identique au plan V3.1 (vérifié sur `topologie_qg.json` : seules les étiquettes différaient). Mise au niveau V3.1 : GAL. SUD = « accès principal gardé — vers la ville enfouie et la pizzeria de Dark » (5 occurrences corrigées).
- Commandes : Plan annoté / Vue immersive · Synthèse / Détail (étiquettes) · zoom − / Ajuster / + avec glisser-déplacer ; les choix sont mémorisés (localStorage, comme les autres réglages de l'atlas).
- Chaque zone `data-lieu` ouvre une **fiche de lieu** dans le tiroir existant : fonction, accès et liaisons, description, note, personnes liées (→ dossier du membre), lieux liés (→ autre fiche), statut documentaire (attesté / aménagement / proposition / indéterminé), bouton « Voir sur le plan » qui surligne et centre la salle.
- Index des lieux par secteur sous la carte, avec recherche et filtre.
- Rien n'a été retiré ni modifié dans les 48 dossiers, la Doctrine, le répertoire et les équipes ; aucune ressource externe nouvelle (les sprites Showdown restent les seules).

## Contrôles effectués (Chromium)
73 zones ↔ 73 fiches ; clic et clavier (Entrée) sur les zones ; chips personnes/lieux ; bascule des vues (0 texte technique visible en immersif) ; zoom ×2 ; recherche / filtre de l'index ; les trois autres onglets inchangés ; affichage mobile.

## Limites connues
- Révision 23 h 40 : les enveloppes `cabale` et `service` sont remplacées par une zone par salle (7 + 9), générées depuis `topologie_qg.json` ; la salle des pompes devient cliquable (`remise_so`). 73 zones au total. Les IDs `cabale` et `service` n'existent plus.
- Les textes des fiches sont rédigés d'après le journal des décisions ; les « propositions » restent à barrer librement.

## Régénération
`python3 build_atlas2.py` (atlas à jour `atlas_src.html` + `Carte_QG_Deux_Vues_Atlas.svg` + `lieux_data.py` + `topologie_qg.json`) → `out/Atlas_Noir_Adorateurs_des_Tenebres.html` ; `python3 test_atlas2.py` pour les contrôles.

## Révision du 18/10 (00 h 50) — illustrations
Neuf images fournies par l'auteur, converties en WebP (≤ 1100 px, ~800 Ko au total) et embarquées : fiche illustrée (vignette dans l'en-tête, image pleine largeur en tête du corps) pour Bureau de Psykos, Vestibule du Pape, Bureau du Pape, Infirmerie, Citerne, Oubliettes du Fiel, Haute sécurité et les deux accès (couloir d'extrémité) ; les deux couloirs figurent aussi dans un bandeau « Galeries » sous la carte. Les descriptions de ces fiches reprennent les détails visuels des images. Dossier source : `outils/img/` ; la clé `img` de `lieux_data.py` nomme le fichier.

## Révision du 19/10 (01 h 30) — galeries de vues
Une fiche peut porter plusieurs vues : clé `galerie=[("nom_image", "légende"), …]` dans `lieux_data.py` en plus de `img`. L'atlas affiche la vue principale en grand et des vignettes cliquables dessous (légende mise à jour). Première utilisation : l'église (vue d'ensemble + vue rapprochée de la dalle et des sièges).

## Révision du 19/10 (15 h) — V3.2 : galeries annexes (boyaux)
- Le plan reçoit le réseau de boyaux dessiné à main levée par l'auteur (665 tronçons, 83 débouchés dans les galeries principales, brèches visibles dans les parois), dans les deux rendus (technique : roche grise ; immersif : terre sombre). Les trois issues secrètes sont ses tracés dorés ; le passage du Pape vers son réduit passe au gabarit boyau. Rien d'autre ne bouge sur le plan.
- Nouveau bouton **Carte complète / Couloirs principaux** dans la barre de la carte : masque les boyaux, leurs brèches et leur zone cliquable (choix mémorisé dans `localStorage`, clé `adt-carte-boyaux`). « Voir sur le plan » depuis la fiche des boyaux réaffiche le réseau.
- Nouveau lieu `galeries_annexes` (« Galeries annexes (boyaux) », secteur Galeries, aménagement) : tout le réseau est une seule zone cliquable (surlignage discret au survol), fiche avec règles et chiffres. 74 lieux. Illustration provisoire : extrait du plan (à remplacer par une image GPT).
- Bandeau « Galeries » : troisième vignette « Galeries annexes ».
- Régénération : `python3 build_atlas2.py` lit en plus `qg_schema/final/Plan_QG_Corresone_final.svg` (groupes `#boyaux`, `#boyaux-ouvertures`, `#secrets`). Contrôles Chromium : 74 zones ↔ 74 fiches, calques masqués par le bouton, fiche des boyaux, vue immersive avec boyaux.
- Poids : 11,6 Mo (+2 Mo pour les deux rendus du réseau et sa zone cliquable).
- 14 h 50 : l'image « couloir d'extrémité » illustre désormais la fiche et la vignette des boyaux (décision auteur) ; les deux accès (GAL. SUD, GAL. S-O) n'ont plus d'illustration.
- 14 h 55 : zone cliquable des boyaux élargie (rubans de paroi + trait transparent : ≈ 25 unités, soit ~13 px à l'écran en vue ajustée, au lieu des 11 unités du sol) ; surlignage au survol par le sol seulement.

## Révision du 19/10 (15 h 35) — surnoms des Pokémon (4 membres)
Posés dans la source de l'atlas (`atlas_src.html`, champ surnom des équipes), visibles dans les fiches et l'onglet Pokémon (recherche par surnom) :
- **Frère Pierrot** (Hisoka) : Mimidrive « Étoile », Noctunoir « Larme », M. Mime « Carreau », Excelangue « Cœur », Migalos « Pique », Empiflor « Trèfle ».
- **Frère Maskass** (Harry Osborn) : Hypnomade « Norman », Scalproie « Kingsley », Grahyèna « Flint », Mackogneur « Oz », Ténéfix « Kindred », Corboss « Oscorp ». Décisions auteur : le père (Évêque à créer, inspiré de Norman Osborn, alias prévu **Frère Goblin**) ne donnera aucun surnom à ses Pokémon — pour lui ce sont des outils ; Maskass deviendra **Frère Hobgob** (nouveau masque) dans une suite, d'où Goblin et Hobgob écartés des surnoms.
- **Sœur Vouivre** (Rhea) : Rexillius « Seiros », Libégon « Cichol », Torgamord « Indech », Bruyverne « Macuil » (les Quatre Saints), Crocorible « Nemesis », Séviper « Thalès ».
- **Frère Piqueux** (John Wick) : Démolosse « Baba Yaga », Grahyèna « Charon », Lougaroc « Mustang », Malosse « Daisy ».

## Révision du 19/10 (16 h 45) — Cellules des sacrifices illustrées
Image GPT (prompt corrigé d'après le plan : couloir nord-sud, trois cases par côté, passage ouest à mi-couloir vers la grille de l'église, captifs adultes, geôles peu sécurisées) ; description de la fiche réécrite d'après l'image. 35 fiches illustrées.
- 17 h 05 : Dépôt des effets des sacrifiés illustré (GPT) ; fiche réécrite d'après l'image. 36 fiches illustrées.
- 17 h 20 : Garde des geôles (S25) illustrée (GPT, sans personnage) ; fiche réécrite. 37 fiches illustrées.
- 17 h 40 : Salle des initiés (S10) illustrée (GPT, sans personnage : bancs, pupitre, trois panneaux I-II-III des Articles) ; fiche réécrite. 38 fiches illustrées.
- 17 h 55 : Cierges et encens (S15) illustrée (atelier de cierges noirs) ; nouvelle image propre aux boyaux (`boyau`), le couloir de roche brute revient à GAL. SUD / GAL. S-O ; bandeau à trois vignettes. 39 fiches illustrées.
- 18 h 15 : quatre salles illustrées (Matériel d'entraînement S24, Lavabos « visiteurs » S13, Poste de garde de l'entrée, Salle de réunion S12), fiches réécrites ; **canon** : l'accès de la pizzeria de Dark passe de GAL. SUD à GAL. S-O (non gardée), GAL. SUD reste l'accès principal gardé — étiquettes du plan, topologie, journal §17 et fiches à jour. 43 fiches illustrées, 13 lieux attestés.
- 18 h 35 : GAL. S-O (accès de la pizzeria) reçoit sa propre image : galerie endommagée par le combat Dark / Olivier (image 800 px fournie par l'auteur, non agrandie) ; fiche complétée.
- 19 h 40 : S27 « Cellier (spiritueux) » → « Serre à baies (lampes à réflecteurs) » (doublon avec la cave à vin ; décision auteur, journal §18) : étiquette du plan, fiche, cave à vin ajustée.
- 19 h 50 : cinq salles illustrées (Fourrage S18, Remise S26, Salle des pompes, Serre à baies S27, Atelier S21 renommé « bois, cuir, lampes, électronique ») ; fiches réécrites. 49 fiches illustrées. Réserve : la salle des pompes porte trois étiquettes en anglais (WEST LINE / EAST LINE / PUMPING SHIFTS) à retoucher.
- 20 h 15 : Buanderie et Douches H illustrées (2025 : machines à laver et ampoules sur le câble du groupe, chaudière à bois) ; fiches réécrites. 51 fiches illustrées.
- 20 h 30 : Douches F illustrées (cabines à rideaux noirs, chauffe-eau invisible, plus soignées que les douches H — décision auteur) ; fiche réécrite, douches H complétée. 52 fiches illustrées.
- 20 h 45 : aile de service réordonnée du nord au sud — Douches H, WC H, WC F, Douches F (journal §19) : modèle, topologie, étiquettes des deux vues, zones ; étiquette détaillée de S27 corrigée (« Serre / à baies »).
- 20 h 45 : WC H et WC F illustrés ; fiches réécrites, douches ajustées au nouvel ordre. 54 fiches illustrées.
- 20 h 45 : WC H et WC F illustrés ; fiches réécrites, douches ajustées au nouvel ordre. 54 fiches illustrées.
- 21 h 10 : Habitations (D01–D16) illustrées (couloir + alvéole ouverte) ; fiche réécrite. 55 fiches illustrées.
- 21 h 50 : aile de service complète — Salle de vie, Self, Réserve alimentaire, Cuisines, Garde-manger (chambre froide, nourriture emballée : jamais d'animal reconnaissable, monde Pokémon) ; fiches réécrites. 60 fiches illustrées.
- 22 h 35 : Fiel — deux vues en galerie (galerie d'approche, bord de la fosse) ; Loge du garde (Pape) refaite en poste de surveillance 2025 (caméra, interphone, talkie), fiche et accès corrigés (loge à côté du vestibule, non en face).
- 22 h 40 : étiquette « Cave à fromages » passée sur deux lignes (elle débordait de la salle).
- 23 h 05 : Poste de garde de l'entrée refait (surveillance 2025) ; quartier des Cabalistes complet — antichambre gardée, chambre standard (une image pour les quatre, Cab. 3 = Frère Pommier), salon, salle de bain, WC. 70 fiches illustrées.
- 20/10, 0 h 05 : quartier des Évêques complet — chambre standard (une image pour les quatre), salon-mess pour dix, douche collective (renommée « Douche des Évêques », plus de baignoire), WC. **74 fiches sur 74 illustrées.**
- 0 h 10 : Aile de la Main — seconde vue en galerie (fond du couloir, douche et latrines ouvertes).
- 0 h 55 : quatre vues annexes en galerie — cellule de haute sécurité (intérieur), arène vue des gradins, escalier de la pizzeria (GAL. S-O), alvéole D08. 81 images.

## Révision du 20/10 (1 h 15) — cartouche sorti du plan, sélecteur de quartier
- Le cartouche (titre + légende) n'est plus peint sur le plan : il est rendu en HTML sous la carte (titre, légende des statuts, légende des couleurs du plan, portes, passages secrets, galeries, boyaux). Le coin inférieur droit du plan est libre.
- Nouveau sélecteur **Quartier** dans la barre de la carte (Tout le repaire · Cœur rituel · Fiel, geôles et haute sécurité · Pape Sombre · Psykos et la Main · Cabalistes · Évêques · Trésor, archives et écoute · Vie quotidienne · Galeries, ateliers et accès) : un voile sombre couvre le plan sauf les salles du quartier choisi (masque SVG découpé sur leurs zones), seules celles-ci restent cliquables ; fonctionne dans les deux rendus ; choix mémorisé (`adt-carte-quartier`). L'antichambre gardée appartient aux deux quartiers nobles ; la salle du Conseil au quartier du Pape. Les quartiers sont plus fins que les cinq secteurs de l'index (inchangés).
- 1 h 25 : chaque quartier a un descriptif (encart sous la barre) ; règle d'occupation du repaire (journal §20) portée dans ces descriptifs et dans le texte d'en-tête de l'onglet.
- 1 h 40 : **Export** PNG (4320 px, fond noir) / SVG du plan tel qu'affiché (rendu, boyaux, quartier ou nuit) ; nom de fichier explicite. Pas de ressource externe : l'export fonctionne hors ligne.
- 10 h 50 : mode Jour / Nuit retiré à la demande de l'auteur (testé, non retenu).
