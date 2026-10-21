# QG des Adorateurs des Ténèbres — Proposition de structure (étape B)

Document de travail à corriger ensemble. Rien n'est dessiné « joliment » : seule la topologie compte ici.
Référence visuelle : `schema_validation.png` / `.svg` (les petits codes rouges — N1, J2, Pj… — sont les nœuds de galeries, pour qu'on puisse en parler précisément).

## 1. Ce que l'analyse des sources a fixé (contraintes fermes appliquées)

| Contrainte | Application dans le schéma | Vérifié par le graphe |
|---|---|---|
| Église en croix, **exactement 4 accès** (N, O, E, S) | Portes EN / EW / EE / ES, aucune autre | ✅ 4 portes |
| Sacrifices **dans** l'église | Autel/dalle dans la branche nord de la croix | — |
| Cellules des sacrifices = **geôles**, proches, passage direct église ↔ geôles | Bloc à l'est ; court passage EE → CW (la « droite » de Sam) | ✅ |
| Fiel : **une seule galerie d'approche**, **pas de porte**, chemin **sur le bord** de la fosse | Galerie Pj → Fb → F1 → Fa ; arc de bord Fa → Fx ; aucun symbole de porte | ✅ Fiel relié à Fa et Fx seulement |
| Haute sécurité **uniquement** derrière le Fiel, **cul-de-sac** | Fx → HSN, porte unique ; en retirant le nœud « Fiel », la haute sécurité devient inaccessible | ✅ |
| Petits dortoirs + couloir central | **16 alvéoles** D01–D08 / D09–D16 (2 × 8, décision du 17/10 : le chiffre dix n'était pas une contrainte), porte de chaque alvéole sur le couloir axial, couloir ouvert aux deux bouts (HN, HS) | — |
| Une seule infirmerie | Un bloc, 2 portes (N sur la galerie P1–J1, E sur la galerie des dortoirs) | — |
| Citerne ronde, **sèche**, **cul-de-sac**, au bout de la galerie des dortoirs | Galerie HS → P1 → J1 → Ie → J2 → CIT ; une seule porte (NE) ; GAL. S-O part de J2, pas de la citerne | ✅ 1 seul lien |
| Réserve petite, au nord, porte verrouillable | Petit rectangle en haut de l'épine nord ; symbole de porte « du haut » supprimé (croix rose) | — |
| Pape : 1 entrée ordinaire, petit espace accolé, 1 issue secrète séparée, pas de long couloir | Vestibule d'entrée (porte Pv unique, courte galerie depuis P1) ; **chambre privée accolée** au nord (décision du 17/10 : l'espace accolé est l'appartement, pas un vestibule) ; porte sud → court passage muré → réduit → tunnel orange vers l'ouest | ✅ 1 seul lien public |
| Psykos : 1 entrée ordinaire, annexe accolée, 1 sortie secrète, **pas d'autre porte** | Porte E unique (PE) ; **chambre privée** accolée à l'ouest ; tunnel orange depuis la chambre vers le NE ; ancienne porte SO supprimée (croix rose) | ✅ 1 seul lien public |
| Tunnel de Yumi derrière la toile | **Absent** | — |
| Deux prolongements S-O et S | A1 (GAL. S-O) et A2 (GAL. SUD), libellés « destination indéterminée » | — |
| Un seul niveau, aucun escalier | Aucun escalier dessiné (ni dans la citerne) | — |

## 2. Lecture de vos annotations — appliquées sans doute

- **Rouge** : petite salle isolée à l'extrême ouest + sa galerie verticale → **supprimées** (le vestibule du Pape n'a donc plus de porte nord). Salle rouge au nord-est de l'épine (entre réserve et Psykos) → **supprimée**. Petit renfoncement rouge à porte orpheline à l'ouest de l'église → **supprimé**.
- **Croix roses** : symboles de porte retirés sur la galerie nord (au-dessus de l'église et près de la réserve), sur la galerie en Y sous Psykos, au-dessus de la porte nord des cellules, et sur plusieurs galeries du sud/sud-est. **Aucune circulation n'a été murée** ; les 4 accès de l'église sont conservés.
- **Croix rose sous Psykos** : la porte SO disparaît → entrée unique à l'est.
- **Orange Psykos** : sortie secrète depuis l'annexe nord, sans accès public supplémentaire.
- **Bleu + vert + rose près du Fiel** : nouvelle salle **S19**, parois propres, un seul court couloir muré depuis la galerie d'approche (Fb) ; **aucun lien** avec la haute sécurité ni avec les cellules.
- **Bleu sur la branche nord du Fiel** : la petite salle NE absorbe son ancien couloir d'accès → **S20**, porte unique sur la galerie d'approche (avant la fosse).
- **Bleu entre église et galerie des cellules** : **S18**, salle close avec porte.
- **Bleus des boucles ouest / sud / sud-est** : convertis en salles closes avec une porte chacune : S01, S02, S03, S04, S05, S07, S08, S09, S10, S11, S12, S13.
- **Chaîne de salles du sud-est** (parois vertes + portes roses) : **S15 ↔ S16** reliées par une porte intérieure (enfilade), chacune ayant aussi sa porte sur une galerie.
- **Rectangles roses** autour des petites salles de l'ouest / nord-ouest : chaque salle a maintenant une porte lisible (S21, S22, S23, S26).

## 3. Annotations ambiguës — **tranchées le 17/10/2026** : lecture C du « Inverse », citerne à porte unique, salle rouge NE supprimée avec galerie conservée, S05 à une porte

1. **« Inverse » (marron) près du bureau du Pape.** Trois lectures possibles ; j'ai dessiné la lecture C par défaut :
   - A : échanger les emplacements du bureau et de l'annexe (le bureau viendrait contre la galerie, l'annexe derrière).
   - B : échanger les rôles des deux côtés : l'entrée ordinaire passe du côté où partait l'ancien tunnel, le secret part de l'ancienne entrée.
   - **C (dessinée)** : l'ancien tunnel secret le long du mur est (hachuré de rose) disparaît ; la porte **sud** du bureau donne sur le court passage vert jusqu'au **réduit** (porte rose), et le tunnel orange repart **du réduit** vers l'ouest. Le réduit n'a aucune autre issue, donc le bureau garde une seule entrée ordinaire (vestibule).
2. **Rectangles roses sur la citerne** (côté ouest et côté est) — ils ajouteraient deux portes, ce qui contredit « citerne en cul-de-sac au bout de la galerie des dortoirs ». J'ai dessiné **une seule porte** (NE) et fait partir GAL. S-O de la galerie, pas de la citerne.
3. **Crochet vert dans la salle rouge** au nord-est de l'épine : je l'ai lu comme « la salle disparaît, la galerie en dessous reste une simple galerie ». À confirmer.
4. **Petite salle médiane du centre-sud** avec un rectangle rose en haut **et** en bas : deux portes en feraient une salle traversante entre deux galeries. J'ai mis une seule porte (S05 : porte ouest). À confirmer.

## 4. Éléments repris de l'ancien plan faute d'annotation contraire (à confirmer ou à retirer)

- ~~Cellules : 4 portes~~ → **tranché : 3 portes** (O église, N, S) ; porte E et galerie CE → E1 retirées.
- **Couloir axial des habitations ouvert aux deux bouts** (porte N vers la boucle nord-ouest, porte S vers la galerie du Pape / infirmerie).
- **Infirmerie à 2 portes** (N et E).
- Positions des bureaux du Pape (extrême ouest) et de Psykos (nord-est de l'église) : propositions d'atlas, pas canon.

## 5. Liste des salles et de leurs ouvertures

### Lieux établis / secteurs
| ID atlas | Salle | Ouvertures |
|---|---|---|
| `eglise` | Église souterraine (croix) | N→EN (épine nord), O→EW, E→EE (passage vers geôles), S→ES |
| `reserve` | Réserve / trésor (petite) | S→Rs |
| `habitations` | Bloc **D01–D16** (2 × 8), alvéoles au gabarit « lit + table de chevet », couloir axial | N→HN, S→HS ; 10 portes internes dortoir→couloir |
| `infirmerie` | Infirmerie (unique) | N→IN, E→IE |
| `citerne` | Citerne ronde sèche | NE→CIT (unique) |
| `cellules` | Cellules des sacrifices (geôles, bloc réduit) | O→CW (passage depuis l'église), N→CN, S→CS |
| `fiel` | Oubliettes du Fiel (fosse ouverte) | arrivée Fa (sans porte) ; départ Fx (sans porte) vers haute sécurité |
| `hautesecu` | Haute sécurité **réduite** (couloir étroit, 2 × 5 cellules exiguës, ≥ 10 portes de fer) | N→HSN (unique) |
| `pape` | Bureau du Pape Sombre | porte intérieure ← vestibule ; porte intérieure → chambre ; porte S → passage privé → réduit |
| — | Vestibule d'entrée du Pape | E→Pv (**seule entrée ordinaire du secteur**, gardée) |
| — | Chambre du Pape (appartement privé : lit, mobilier) | uniquement depuis le bureau |
| — | Salle de bain du Pape (douche/baignoire + WC) | uniquement depuis la chambre |
| — | Réduit du Pape | passage privé depuis le bureau ; **tunnel secret** vers l'ouest |
| `psykos` | Bureau de Sœur Psykos | E→PE (**seule entrée ordinaire**) ; porte intérieure → annexe |
| — | Chambre de Psykos (appartement privé : lit, mobilier) | depuis le bureau ; **tunnel secret** vers le nord-est |
| — | Salle de bain de Psykos (douche/baignoire + WC) | uniquement depuis la chambre |
| `acces1` / `acces2` | GAL. S-O (A1) / GAL. SUD (A2) | prolongements, destination indéterminée |

### Aile de service des habitations (demande du 17/10, non canon — à l'est du bloc des dortoirs, le long de la galerie r2i → J1)
| Salle | Ouvertures |
|---|---|
| Douches H / Douches F (deux petits vestiaires superposés, < 10 personnes chacun) | une porte E chacune → nDh / nDf |
| WC H / WC F (deux petits blocs sous les douches) | une porte E chacun → nWh / nWf |
| Salle de vie / détente | E → nV |
| Self (réfectoire) | E → nSf ; portes intérieures vers la réserve et les cuisines |
| Réserve attenante | depuis le self ; porte intérieure vers les cuisines |
| Cuisines | depuis le self ; porte de service E → nCu |
| Buanderie (en face des douches, dans la maille voisine) | N → nBu (court couloir sur la galerie r2i–sNW) |

### Quartier des Cabalistes (proposition du 17/10, non canon — au nord-ouest, au-dessus de l'anneau 3)
Depuis la galerie r3k–HN (nœud nC), on entre d'abord dans le **poste de garde / antichambre de la Cabale** (fusion du poste de garde initialement prévu près de la réserve avec l'entrée du quartier), puis le couloir privé en **impasse** dessert de part et d'autre : Cab. 2 / Cab. 4, Cab. 1 / Cab. 3, salle de bain / WC, et au fond le **salon de détente**. Aucune autre ouverture ; les Cabalistes peuvent n'y séjourner qu'occasionnellement (comme Psykos et le Pape, ils ont sans doute une vie à l'extérieur).

### Salles secondaires (rôles arbitrés le 17/10, non canon)
| ID | Rôle | Porte → nœud |
|---|---|---|
| S03 | Archives | E (court couloir) → n03 |
| S08 | Réserve d'huile et de torches | E (court couloir) → n08 |
| S13 | Lavabos / latrines (« visiteurs ») | O (court couloir) → n13 |
| S15 | Cierges, encens (matériel rituel) | O (court couloir) → n15 |
| S17 | Poste de veille (galerie est) | O (court couloir) → r3c |
| S19 | Salle d'interrogatoire | N (court couloir muré) → Fs19 |
| S20 | Chaux et outils du Fiel | S → NEd |
| S21 | Forge et atelier | E (court couloir) → n21 |
| S27 | Cellier (spiritueux) | E (court couloir) → n05 |
| effets | Dépôt des effets des sacrifiés | O → nEf |
| S06 | Sacristie | court couloir → p_S06 |
| S10 | Salle des initiés | court couloir → p_S10 |
| S12 | Salle de réunion des frères | court couloir → p_S12 |
| S18 | Fourrage et paille (Pokémon) | court couloir → p_S18 |
| S24 | Matériel d'entraînement | court couloir → p_S24 |
| S26 | Remise (outils de corvée) | court couloir → p_S26 |
| cave_vin | Cave à vin | court couloir → p_cave_vin |
| cave_fromages | Cave à fromages | court couloir → p_cave_fromages |
| remise_so | Écurie / box Pokémon de bât | court couloir → p_remise_so |
| S28 | Vestiaire des officiants | court couloir → p_S28 |

## 6. Réseau de galeries — principe « toile d'araignée » (révision du 17/10, 13 h 30)

- **Rayons** : N (église → Na → réserve), S (église → S1 → S2 → S3 → GAL. SUD), O (église → W5 → J1 ; le vestibule du Pape est desservi par P1 depuis la galerie des dortoirs), E (passage église → geôles), et quatre diagonales NE / SE / SO / NO (r1c→r2c→Pj ; r1e→r2e→r3c ; r1g→r2g→J2 ; r1i→sNW→r2i→r3k), rectilignes.
- **Anneau 1** (proche) : N1 – r1b – r1c – CNa | CSa – r1e – S1 – r1g – W5 – r1i. **Ouvert à l'est** depuis la V1.2 (les tronçons contournant les cellules croisaient l'anneau 2 sans jonction) ; les portes N et S des cellules se piquent sur CNa et CSa.
- **Anneau 2** : Na – r2b – r2c – r2d – r2e – r2f – S2 – r2g – J1 – r2i – r2j.
- **Anneau 3** (extérieur, **interrompu** dans le secteur Fiel / haute sécurité) : Pj – r3b – R3n – r3j – r3k – HN – *couloir axial des habitations* – HS – P1 – r3h – r3g – J2 – SW1 – r3f – S3 – r3e – r3d – r3c – r3c2. Le bloc des dortoirs fait partie de l'anneau (d'où ses deux bouts ouverts).
- **Appendices en cul-de-sac** : galerie des dortoirs → citerne (J2 → CIT) ; Pj → Fs19 → F1 → Fa → *bord du Fiel* → Fx → haute sécurité ; spur privé Pj → Ps → porte de Psykos ; vestibule du Pape ; GAL. S-O et GAL. SUD.
- **Cadre dilaté ×1,35** (viewBox 2160 × 1620) pour aérer ; galeries redondantes retirées (r1g–r2g directe, r2f–r2e, J1–sSW).
- **Cellules des sacrifices réduites** à 120 × 110 (au lieu de 190 × 190), 3 portes (O église, N, S).

## 7. Contrôles automatiques exécutés sur le graphe

- Réseau connexe depuis l'église ✅ · 4 portes à l'église ✅ · haute sécurité : 1 lien ✅ · **suppression du nœud Fiel ⇒ haute sécurité inaccessible** ✅ · Pape : 1 lien public ✅ · Psykos : 1 lien public ✅ · Citerne : 1 lien ✅ · Fiel relié uniquement à son arrivée et à son départ ✅ · aucune salle sans ouverture ✅.


## 8. Révision du 17/10 (15 h) — placements
Contrôle géométrique automatique ajouté (`collisions.py` : aucune galerie à moins d'une paroi d'une salle hors ses accès ; chaque porte sur le mur de sa salle ; aucun chevauchement). Corrections : infirmerie descendue (la galerie r3h–r3g la traversait), loge du Pape dégagée, S12 / S15 / S16 / S26 / S03 déplacées, S20 refermée sur sa porte, poste de garde « Cabale » transformé en antichambre du quartier, **S02, S04, S05, S09, S23 supprimées** (pas d'emplacement propre). Résultat : 0 problème.

## 9. Révision du 17/10 (16 h) — galeries
Suppression des coudes en zigzag (nœuds intermédiaires sNE, sSE, sSW retirés : les diagonales sont désormais rectilignes), du crochet devant la porte de Psykos (spur direct PE → Pj), du V redondant J1–r3h ; approche du Fiel redressée (Pj → Fs19 → F1 → Fa en pente continue) ; r2j replacé au croisement réel des galeries r2i–Na et r3j–r1i. Contrôles géométrique et topologique : 0 problème.

## 10. Révision du 17/10 (16 h 40) — apports du dossier GPT V1.1 et arbitrages
Arbitrages confirmés : **16 alvéoles**, **lecture C** du « Inverse », **3 issues secrètes** (Pape, Psykos, Cabalistes). Repris de GPT : poste de garde **traversant** sur GAL. SUD (portes S et N), **salle d'entraînement** sous grande voûte (remplace S16), étiquettes **Archives** (S03) et **garde des geôles** (S25), **vestibule de Psykos**, salles secondaires au contour irrégulier, annotations d'atlas. Non repris : 10 dortoirs, échange bureau/annexe du Pape, fosse sans renfoncement.

## 11. Révision du 17/10 (18 h) — relecture V1.2
Corrections GPT réappliquées dans le modèle (voir `Decisions_implantation_QG.md` §6). Contrôles : 0 collision, 0 croisement hors nœud, 9/9 portes intérieures sur paroi commune, graphe valide.

## 12. Révision du 17/10 (18 h 30)
D08 = couchage de Dark. Salles réorientées parallèlement à leur galerie ; quatre salles ajoutées (dépôt des effets, scriptorium, vestiaire des officiants, écurie/box) ; rôles proposés pour toutes les salles secondaires (voir `Decisions_implantation_QG.md` §7).

## 13. Révision du 17/10 (18 h 45)
Rôles arbitrés par l'auteur (voir `Decisions_implantation_QG.md` §8) ; ajout du garde-manger, des caves à vin et à fromages, de la salle d'écoute et de la salle du conseil. Contrôles : 0 problème.

## 14. Révision du 17/10 (19 h 50) — décisions V1.9
Forge au secteur est (S17 agrandie), atelier S21 à l'ouest, poste de veille est recréé (`veille_est`, branche depuis r3c2), zone cliquable du Fiel = polygone irrégulier, transits intérieurs église/geôles, classe `lbl-s` pour la vue synthèse. Contrôles : 0 problème.

## 15. Révision du 17/10 (20 h)
Salle des pompes, puits d'aération, quartier des Évêques (ev_1, ev_2, ev_sdb via nEv–nEvB–nEvA–nEvS), classes CSS `synthese` et `atlas-font`, habillage. Contrôles : 0 problème.

## 16. Révision du 17/10 (20 h 40) — V2.3
Inflexions contrôlées de quatre galeries, Évêques irréguliers, étiquettes nord déplacées. Contrôles : 0 problème.

## 17. Révision du 17/10 (21 h) — aile de la Main
Bloc `main` parallèle à r2c–r2d (entrée gM0), 5 cases + WC + douche ; Dark = case 1, chef de la Main ; D08 ordinaire ; haute sécurité décalée de 8 unités vers l'est. Contrôles : 0 problème.

## 18. Révision du 17/10 (21 h 15) — V2.7
S19 biseautée (écart ≈ 16 unités avec la Main), contrôleur durci (chevauchement, parois minces). Contrôles : 0 problème.

## 19. Révision du 17/10 (21 h 40) — V2.9
S20 biseautée (16,3 unités du Fiel), S19 ajustée (16,1 de la Main), trace r2c–r2d retirée ; contrôleur : polygone réel du Fiel. Contrôles : 0 problème.

## 20. Révision du 19/10 (15 h) — V3.2, galeries annexes
Couche `#boyaux` (sous les galeries) + `#boyaux-ouvertures` (brèches, dans `#galeries`) : 665 rubans à largeur variable issus du tracé de l'auteur (`trace/boyaux_main_levee.json`, pipeline `vectorise_trace.py` → `nettoie_trace.py` → `collisions.py run_burrows()` → `render_final.py`). Passages secrets = tracés dorés de l'auteur (`trace/secrets_or.json`). Passage privé Pape → réduit au gabarit boyau. Galeries principales et salles inchangées. Contrôles : 0 problème (salles, galeries, interdits, réseaux isolés).
