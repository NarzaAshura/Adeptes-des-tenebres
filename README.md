# Atlas Noir — Adorateurs des Ténèbres (Pokémon : Kalos du Sud)

Site statique : un seul fichier, `index.html`, qui contient tout (fiches, équipes, Doctrine, plan du QG, images).
Les sprites Pokémon standards sont chargés depuis play.pokemonshowdown.com ; tout le reste est embarqué.

## Mettre en ligne (une fois)

1. Créer un compte sur github.com, puis un dépôt **public** nommé par exemple `kalos-du-sud`.
2. Déposer le contenu de ce dossier dans le dépôt (bouton *Add file → Upload files*, glisser tout le dossier, puis *Commit changes*).
3. Dans le dépôt : *Settings → Pages → Build and deployment → Source : Deploy from a branch → Branch : main, dossier `/ (root)` → Save*.
4. Après une ou deux minutes, le site est à `https://TONPSEUDO.github.io/kalos-du-sud/`.

## Mettre à jour

Remplacer `index.html` par la nouvelle version (*Add file → Upload files*, même nom, *Commit*). Le site se met à jour dans la minute.
Chaque remplacement garde l'ancienne version dans l'historique (*Commits*) : on peut revenir en arrière.

## Contenu du dossier `outils/`

- `build_atlas2.py`, `lieux_data.py`, `atlas_src.html`, `plans/`, `qg_schema/` : outils de GPT pour régénérer l'onglet QG.
- `img/` : illustrations des lieux (WebP).
- `ADT_troufions.xlsx` : tableur des troufions (rang IV) et des trois PJ, source des équipes.
- `portraits.json` : cache des portraits encodés.
- `NOTE_integration_atlas.md` : journal des révisions du QG.

Le fichier `.nojekyll` et la balise `noindex` dans `index.html` sont volontaires : ils évitent respectivement un traitement inutile par GitHub et l'indexation par les moteurs de recherche.
