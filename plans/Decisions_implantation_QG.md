# Décisions d'implantation — Plan du QG des Adorateurs des Ténèbres (Corrésone)

Version du 17 octobre 2026. Fichiers livrés : `Plan_QG_Corresone_final.svg` (vectoriel, autonome, interactif), `Plan_QG_Corresone_apercu.png` (exporté depuis ce SVG), `topologie_qg.json` (graphe), `Structure_QG_etapeB.md` (dossier de validation).

## 1. Ce qui vient des récits (attesté) et comment c'est rendu
- **Église en croix** au centre, 4 accès (N, O, E, S). Dalle sacrificielle bleutée et présentoir dans la branche nord, **cinq sièges** en demi-cercle derrière — ceux des **quatre Cabalistes et du Pape Sombre** (confirmé par l'auteur ; le statut exact de Sœur Psykos, cabaliste ou rôle équivalent/supérieur, reste ouvert) —, bancs de pierre fixes dans la nef sud et les bras.
- **Passage église → cellules des sacrifices** par la porte est (la « droite » de Sam quand il regarde l'autel). Les cellules sont un vrai bloc de geôles (2 × 3 cases à barreaux autour d'un couloir), 3 portes : ouest (église), nord, sud.
- **Oubliettes du Fiel** : fosse ouverte de poison, **aucune porte**, galerie d'approche unique (depuis Pj) qui s'évase en un *renfoncement sans torche* ; le chemin longe le bord sud-ouest de la fosse ; deux paires d'yeux dans l'ombre pour les Pokémon d'Automne.
- **Haute sécurité** : couloir étroit, 2 × 5 cellules exiguës à portes de fer, une seule lampe à l'entrée, **aucune autre ouverture**. Supprimer le nœud « Fiel » du graphe rend ce secteur inaccessible (vérifié).
- **Citerne** ronde, sèche, au bout de la galerie des dortoirs, porte unique, paille, bassines, caisses, robinet.
- **Réserve** au nord, petite, porte verrouillable ; **infirmerie** unique, blanchie, lits et machine de soins.
- **Chambre de Dark** : révisée le 17/10 (21 h) — Dark dort dans l'**aile de la Main** (case 1, en tant que chef de la Main), non plus en D08 ; voir §12 ; il lui arrive, rarement, de passer la nuit dans l'appartement de Psykos quand elle le retient. Aucune pièce dédiée sur le plan.
- **Tunnel de Yumi derrière la toile** : volontairement absent.

## 2. Choix d'aménagement (décisions de l'auteur, non attestés)
- **Toile d'araignée** : 8 rayons (N, S, O, E + 4 diagonales), 3 anneaux irréguliers ; l'anneau extérieur intègre le couloir axial des habitations et s'interrompt dans le secteur Fiel / haute sécurité.
- **Habitations** : 16 alvéoles (D01–D16) au gabarit « lit + table de chevet », couloir axial ouvert aux deux bouts.
- **Aile de service** contre les dortoirs : douches H / F (vestiaires < 10 pers.), WC H / F, salle de vie, self + réserve + cuisines (porte de service), buanderie en face.
- **Bureau du Pape Sombre** (extrême ouest) : vestibule d'entrée (porte unique, gardée, loge attenante), chambre et salle de bain privées au nord, porte sud → passage muré → réduit → **passage secret vers l'ouest** (lecture C de l'annotation « Inverse »).
- **Bureau de Sœur Psykos** (nord-est, au-dessus de l'anneau extérieur) : **vestibule** à l'est du bureau, porte unique ouvrant au sud sur la galerie de l'anneau extérieur, juste avant la jonction Pj (tout trajet vers le Fiel passe devant), chambre et salle de bain à l'ouest, **passage secret depuis la chambre** vers le nord-est.
- **Quartier des Cabalistes** (nord-ouest) : poste de garde / antichambre à l'entrée, couloir privé en impasse, 4 chambres, salle de bain, WC, salon au fond d'où part un **troisième passage secret** (décision du 17/10, 16 h 40) ; occupation intermittente possible.
- **Postes de garde** : devant la réserve (S01), antichambre du quartier des Cabalistes (`cab_garde`), loge du Pape, **garde des geôles** (S25, au sud des cellules), et le **poste de l'entrée** sur GAL. SUD, pièce traversante (porte sud vers l'extérieur, porte nord vers le QG) — idée reprise du plan GPT V1.1.
- **Salle d'entraînement sous grande voûte** (sud-est, polygonale) et **Archives** (S03, sous la réserve) : ajouts non canoniques repris du plan GPT V1.1 à la demande de l'auteur.
- **GAL. SUD = accès principal gardé**, qui mène, par la ville enfouie (grande salle voûtée, boyaux), à l'accès clandestin de la **pizzeria de Dark** (confirmé par l'auteur le 17/10 ; cohérent avec le raid : Yumi entre par la pizzeria, et Jane ne connaît qu'une sortie, gardée) ; **GAL. S-O = prolongement à destination indéterminée**. Le trajet intermédiaire dans la ville n'est pas cartographié.
- **Salles secondaires** (16 : S06, S08, S10, S12, S13, S15, S17–S21, S24, S26, S27 ; S03 = Archives, S25 = garde des geôles) : aucune fonction canonique ; une seule porte chacune (S15/S16 en enfilade), aucune ne crée d'itinéraire alternatif vers la haute sécurité ni vers un bureau.
- Les trois passages secrets mènent **vers l'extérieur** ; leur débouché est inconnu et hors plan (pointillés dorés s'achevant dans la roche).

## 3. Annotations de la dernière image : traitement
Annotations d'atlas ajoutées sur le plan (« 4 accès », « renfoncement sans torche », « chemin longeant la fosse », « passage obligé », « seule galerie d'approche »). Rouge → 3 salles supprimées · croix roses → symboles de porte retirés sans murer · rectangles roses → portes ajoutées à l'interface salle/galerie · bleu → S18, S19, S20 et les salles des boucles converties en volumes clos · vert → parois / court couloir muré de S19 et enfilade S15–S16 · orange → les deux secrets · marron « Inverse » → lecture C validée · rectangles roses de la citerne → **non appliqués** (citerne gardée en cul-de-sac, décision validée).

## 4. Intégration dans l'atlas
- `viewBox="0 0 2160 1681"` (ratio libre accepté). Aucune police, image, script ou `foreignObject` ; style CSS inline uniquement.
- Zones cliquables : `<g class="hot" data-lieu="ID" tabindex="0" role="button" aria-label="Nom">` contenant une forme (`.zone`) et un texte ; survol / focus = liseré doré. Les secteurs proposés portent en plus la classe `hot-tbd`.
- IDs imposés : `eglise reserve cellules fiel hautesecu habitations infirmerie citerne pape psykos acces1 acces2`.
- IDs supplémentaires : `service` (aile de service, un groupe), `buanderie`, `cabale` (quartier, un groupe), `pape_vest pape_chambre pape_sdb pape_reduit psykos_vest psykos_annexe psykos_sdb`, `entrainement`, et chaque salle secondaire / poste de garde (`S03`…`S27`, `S01`, `cab_garde`, `garde_pape`, `garde_sud`).
- Le décor est en `pointer-events:none` ; les zones sont au-dessus et n'altèrent pas le dessin.
- Total : 43 zones cliquables.

## 5. Contrôles effectués
Contrôle géométrique (aucune galerie ne traverse une salle, chaque porte est sur son mur, aucun chevauchement) : 0 problème · XML valide · graphe connexe · église = 4 portes · haute sécurité = 1 lien, inaccessible sans le Fiel · Pape et Psykos = 1 lien public chacun · citerne = 1 lien · Fiel relié uniquement à son arrivée et à son départ · aucune salle sans ouverture · PNG généré depuis le SVG livré.

## 6. Relecture V1.2 de GPT (17/10, 17 h 50) — ce qui a été retenu
Retenu et **réappliqué dans le générateur** (pas dans le SVG édité à la main) : parois réellement mitoyennes pour les neuf portes intérieures (chambres ↔ salles de bain, self ↔ réserve ↔ cuisines) ; suppression des quatre tronçons de l'anneau 1 à l'est des geôles, qui croisaient l'anneau 2 sans jonction ; fosse du Fiel et mare à contours irréguliers, sente de bord sud-ouest ; libellé des trois secrets « vers l'extérieur — débouché inconnu » ; dans le JSON, `transits_interieurs` (pièces traversantes) et `traces_courbes_galeries` (Fa–Fx).
Ajouté au contrôle automatique à cette occasion : test de **croisement galerie/galerie hors nœud** (il retrouve bien les quatre cas signalés) et test de **paroi commune** pour chaque porte intérieure.
Les deux points de lore des notes GPT (cinq sièges = quatre Cabalistes + Pape Sombre ; Dark dans un dortoir ordinaire) ont depuis été **confirmés par l'auteur** et sont consignés en §1.

## 7. Révision du 17/10 (18 h 30) — orientation des salles, rôles proposés, ajouts
- **Orientation** : les salles accrochées à une galerie oblique sont désormais **tournées parallèlement à cette galerie**, avec un court couloir perpendiculaire (générateur : fonction `_attach`). Concernées : Sacristie (ex-S06), Salle des initiés (ex-S10), Salle de réunion des frères (ex-S12), Fourrage et paille (ex-S18), Cave à vivres (ex-S24), Remise (ex-S26), et les trois nouvelles salles ci-dessous. La toile de galeries n'a pas bougé.
- **Nouvelles salles** (propositions) : **Dépôt des effets des sacrifiés** au sud-est des geôles (porte sur le couloir de la porte sud des cellules) — lieu de tri des affaires sans valeur ; les Poké Balls, sacs et cartes de dresseur montent à la **trésorerie**, où le raid les retrouve ; **Scriptorium** (nord-est, entre la réserve et Psykos) ; **Vestiaire des officiants** (nord-est de l'église) ; **Écurie / box des Pokémon de charge** (sud-ouest, près de GAL. S-O).
- **Rôles proposés pour les anciennes salles muettes** (à barrer librement) : S01 poste de garde de la réserve · S03 Archives · S08 réserve d'huile et de torches · S13 lavabos / latrines des visiteurs · S15 garde-manger (salaisons) · S17 chaux et outils du Fiel · S19 réserve de chaînes et fers · S20 poste de veille des abords du Fiel · S21 atelier (réparations) · S25 garde des geôles · S27 cellier (spiritueux — les bouteilles « évaporées » du raid) · Sacristie · Salle des initiés (préparation avant le rituel) · Salle de réunion des frères · Fourrage et paille · Cave à vivres · Remise (outils de corvée). Toutes restent en classe `hot-tbd` (proposition) dans le SVG.
- **Contrôles étendus** : portes et chevauchements testés sur les polygones tournés ; 0 problème.

## 8. Révision du 17/10 (18 h 45) — rôles arbitrés par l'auteur
- **Lavabos / latrines (« visiteurs »)** : guillemets voulus — les visiteurs sont le plus souvent les futurs sacrifiés.
- **Vivres regroupés près des cuisines** : la pièce attenante devient la **réserve alimentaire**, et un **garde-manger** mitoyen est ajouté sous les cuisines (porte intérieure). S15 → cierges et encens ; S24 (près de la salle d'entraînement) → matériel d'entraînement.
- **S20 = chaux et outils du Fiel** (sur la galerie d'approche) ; S17 → poste de veille de la galerie est.
- **Cave à vin** et **cave à fromages** sur la galerie r3k–r3j, entre le corps de garde des Cabalistes et celui de la réserve.
- **S19 = salle d'interrogatoire** (entre Psykos, le Fiel et la haute sécurité).
- **S21 = forge et atelier** (foyer, enclume, établi).
- **Salle d'écoute** (Pokématos, radios, ordinateurs ; adeptes chargés de transmettre ordres et informations) : à l'est de l'épine nord, en pendant des Archives, porte nord sur la galerie Na–r2b — entre la réserve et l'appartement de Psykos.
- **Salle du conseil des hauts gradés** (Pape Sombre, Sœur Psykos, les quatre Cabalistes, les Évêques) dans la grande maille au sud-ouest de l'église : **octogone régulier** (un côté plat tourné vers la galerie r1g–S1, porte au milieu de ce côté), table ovale, dix sièges, quatre torches d'angle.

## 9. Relecture V1.9 de GPT (17/10, 19 h 45) — retenu et réappliqué dans le générateur
- **Forge déplacée dans le secteur est** (ancienne S17 agrandie : foyer, enclume, établi, évent de fumée non praticable vers la roche) ; **S21 redevient l'atelier de réparations** près du pôle résidentiel — bruit et fumées loin des dortoirs, ce que mon premier choix ignorait. **Poste de veille (galerie est)** recréé au nord de la forge, branche terminale depuis r3c2, une seule porte.
- **Zone cliquable du Fiel** alignée sur le polygone irrégulier du décor (16 sommets partagés par le décor, la zone `data-lieu="fiel"` et le JSON ; le cercle de référence est conservé pour les contrôles).
- **Transits intérieurs** complétés dans le JSON : les quatre accès de l'église communiquent par la nef, les trois seuils des geôles par leur couloir interne (pas de nouvelles portes).
- **Vue synthèse / vue détail dans un seul SVG** : les petites étiquettes portent la classe `lbl-s` ; l'atlas les masque en ajoutant la classe `synthese` sur l'élément `<svg>` (règle CSS incluse). Un aperçu PNG de la vue synthèse est fourni. Pas de dépendance JavaScript dans le SVG.
- Taille de la trésorerie inchangée (décision de l'auteur).

## 10. Révision du 17/10 (20 h) — derniers ajouts et habillage
- **Salle des pompes / puits** (sud-ouest, ancienne « écurie », près de la citerne et de son robinet) : source d'eau du QG.
- **Cinq puits d'aération** (décor, non praticables) : au-dessus de la forge, des cuisines, du Fiel, de l'église et du secteur sud-ouest.
- **Quartier des Évêques** (révisé 20 h 05) : aile symétrique de celle des Cabalistes, à l'ouest — depuis la porte ouest de l'antichambre gardée, un couloir privé file vers l'ouest puis remonte vers le nord, **quatre chambres** (deux de chaque côté), WC et salle de bain face à face, **salon des Évêques** au bout ; impasse, aucune autre ouverture, pas d'issue secrète propre (le nombre de chambres est ajustable sans toucher au réseau). L'issue secrète des Cabalistes part désormais du haut de leur salon, droit vers le nord.
- **Police héritée** : l'atlas peut imposer sa typographie en ajoutant `class="atlas-font"` à l'élément `<svg>` (règle `font-family:inherit` incluse), comme `synthese` pour les étiquettes.
- **Habillage** : dallage de l'église, pierre blanchie de l'infirmerie, terre battue des salles secondaires, anneaux de la citerne, bande d'usure au centre des galeries, ombres portées des salles, halos de torches en dégradé, roche plus fine avec fissures. Aucun mur ni nœud modifié ; contrôles à zéro.

## 11. Relecture V2.3 de GPT (17/10, 20 h 30) — validée et réappliquée dans le générateur
- **Aile des Évêques** aux contours irréguliers (même traitement que les salles secondaires), portes et nœuds inchangés.
- **Quatre galeries infléchies** (r3h–r3g, J1–r2g, r2d–r2e, r2c–r2d) : arcs quadratiques décoratifs sans nouveau nœud ; le graphe reste rectiligne. Les arcs sont **échantillonnés par le contrôleur** (distance aux salles, croisements) — deux inflexions proposées se rapprochaient trop de l'infirmerie et du dépôt des effets, leur sens a été inversé. Traces décrites dans `traces_courbes_galeries`.
- **Étiquettes** Réserve / Trésor et Sœur Psykos placées au-dessus des pièces, hors mobilier.
- Fosse, sente et accès du Fiel inchangés.

## 12. Révision du 17/10 (21 h) — aile de la Main
- **La Main** : garde rapprochée de Sœur Psykos, cinq membres lobotomisés par elle et obéissant sans discuter ; **Dark en est le chef** (canon confirmé par l'auteur). Ils ne logent donc pas avec la troupe.
- **Aile de la Main** : bloc unique construit **parallèlement à la galerie r2c–r2d**, dans le vide entre la salle d'interrogatoire, la haute sécurité et la galerie ; entrée unique par un court couloir perpendiculaire depuis la galerie (nœud gM0) ; couloir intérieur, **cinq cases misérables** (paillasse le long de la paroi, guéridon), **WC** et **douche commune** au bout. Case 1 = Dark. Aucune communication avec la haute sécurité ni avec la salle d'interrogatoire (la haute sécurité a été décalée de 8 unités vers l'est pour conserver une paroi de roche pleine).
- **D08** redevient une alvéole ordinaire. Identifiant de zone : `main` (classe `hot-tbd`).

## 13. Relecture V2.7 de GPT (17/10, 21 h 10) — validée
- **Interrogatoire / Main** : exact, un sommet de l'aile de la Main entrait de 3 unités dans l'angle sud-est de S19 (mon test de chevauchement tolérait 2 unités pour accepter les parois mitoyennes). S19 est retaillée en biseau (polygone à cinq sommets, identique dans le décor, la zone cliquable et le JSON) ; écart de roche ≈ 16 unités. L'aile de la Main ne bouge pas.
- Contrôleur durci : tolérance de chevauchement réduite, et nouveau test « paroi de roche trop mince » (0,5 < écart < 8 unités entre deux salles non mitoyennes) — deux ajustements mineurs en ont découlé (poste de garde de la réserve, loge du Pape).
- Vue synthèse : les étiquettes individuelles des cases et le libellé oblique de la Main sont de classe `lbl-s` (masquées), comme le propose GPT.

## 14. Relecture V2.9 de GPT (17/10, 21 h 35) — validée
- **S20 (chaux et outils du Fiel)** : exact, son angle sud-est frôlait le polygone irrégulier de la fosse (1,3 unité) ; mon contrôleur comparait encore au cercle de référence. Coin biseauté, écart porté à 16,3 unités ; le contrôleur teste désormais le polygone réel du Fiel.
- **S19** : pointe du biseau reculée (écart avec la Main 16,1 unités).
- **Trace courbe r2c–r2d** supprimée du JSON : la galerie est scindée en r2c–gM0–r2d (entrée de la Main) et rectiligne.
- Aucune porte, galerie ou sortie nouvelle. État documentaire de référence : ce fichier, sections 1–14.

## 15. Révision du 17/10 (21 h 50)
GAL. SUD étiquetée « accès principal gardé — vers la ville enfouie et la pizzeria de Dark » (canon confirmé par l'auteur). Aucun changement géométrique.

## 16. Galeries annexes (boyaux) — 19/10/2026, V3.2
- **Principe** (auteur) : les « galeries des extrémités » sont remplacées par un réseau de **boyaux** étroits, creusés n'importe comment, qui partent des galeries principales, se croisent, se rejoignent, s'arrêtent à un ou deux mètres d'une galerie ou en cul-de-sac. Jamais dans une salle. Les galeries principales ne changent pas ; seul le passage du bureau du Pape Sombre vers son réduit prend le gabarit boyau.
- **Interdits** (auteur) : aucun boyau n'arrive ni ne part du Fiel, du couloir entre le Fiel et la haute sécurité, ni de la haute sécurité. Le 19/10 à 14 h 25, l'auteur **autorise le débouché sur la galerie d'approche du Fiel** (du carrefour de Psykos au carrefour devant le Fiel) : deux réseaux de l'est y débouchent, dont un au carrefour même.
- **Tracé** : dessiné à main levée par l'auteur sur un calque (rouge = boyaux, or = passages secrets vers l'extérieur), vectorisé. Règle de l'auteur : on ne coupe pas un trait gênant, on le **rétrécit** (passage étroit à 60 % de largeur). Règle de l'auteur : « il n'existe pas de boyau sans entrée » — chaque réseau connexe possède au moins un débouché.
- **Résultat** : 665 tronçons, 83 débouchés (brèches visibles dans la paroi des galeries), 38 culs-de-sac à moins de deux mètres d'une galerie, 6 ponts et 7 prolongements ajoutés pour relier des réseaux isolés, 0 réseau isolé, 0 anomalie au contrôleur.
- **Issues secrètes** : les trois pointillés sont remplacés par les tracés dorés de l'auteur (départs inchangés : réduit du Pape, salon de la Cabale, annexe de Psykos), dessinés au gabarit étroit avec un liseré or.
- **Atlas** : zone cliquable unique `galeries_annexes` (fiche « Galeries annexes (boyaux) », statut aménagement) ; bouton **Carte complète / Couloirs principaux** qui masque le réseau (choix mémorisé). 74 lieux.

## 17. Accès de la pizzeria déplacé sur GAL. S-O — 19/10/2026, 18 h 10 (décision auteur)
L'accès clandestin de la pizzeria de Dark (par la ville enfouie) part désormais de **GAL. S-O**, non gardée, et non plus de GAL. SUD. Motif : le groupe du raid est entré et ressorti sans affronter d'autre obstacle que Dark ; une sortie par l'accès principal aurait impliqué le poste de garde. **GAL. SUD** reste l'accès principal gardé (poste traversant), débouché extérieur non cartographié — « la seule sortie que connaît Jane ». Aucun changement géométrique ; étiquettes du plan, topologie et fiches mises à jour. GAL. S-O passe au statut attesté (13 lieux attestés).

## 18. S27 : serre à baies — 19/10/2026, 19 h 35 (décision auteur)
Le **cellier des spiritueux** faisait double emploi avec la cave à vin (qui garde désormais les alcools forts derrière sa grille). S27 devient une **serre à baies et légumes éclairée par des lampes à huile à réflecteurs de cuivre** — pas d'électricité hors salle d'écoute, pas de Pokémon-lampe. Statut proposition ; même emplacement, même porte.

## 19. Aile de service : ordre des sanitaires — 19/10/2026, 20 h 40 (décision auteur)
Du nord au sud : **Douches H, WC H, WC F, Douches F** (au lieu de Douches H, Douches F, WC H, WC F) — les deux blocs des frères et des sœurs sont ainsi contigus. Les géométries et les portes ne bougent pas, seules les affectations changent ; les noms de nœuds de porte (nDf, nWh, nWf) restent historiques.

## 20. Occupation du repaire — 20/10/2026, 1 h 20 (décision auteur)
Hormis **la Main** et **les prisonniers**, personne ne dort au repaire sauf lorsqu'il est de garde ou de service — Cabalistes et Évêques compris. Les Évêques sont presque toujours dehors à tenir les cellules de l'Ordre (quatre chambres suffisent) ; les chambres des Cabalistes servent surtout les nuits d'office ; les alvéoles de la troupe ne sont occupées que par les équipes de service. L'appartement du Pape est tenu prêt et gardé en permanence. Dans l'atlas : sélecteur « Quartier » (neuf regroupements par locataire ou usage) avec un descriptif qui porte cette règle.
