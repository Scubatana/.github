# .github : la page de l'organisation Scubatana

Ce dépôt ne contient pas de code applicatif. Il porte la page que GitHub affiche
sur [le profil de l'organisation](https://github.com/Scubatana), et les scripts
qui en dessinent les animations.

Le projet lui-même est dans [**scubanion**](https://github.com/Scubatana/scubanion).

## Ce qu'il y a dedans

```
profile/
  README.md              la page affichée sur le profil de l'organisation
  assets/
    logo-scubanion.svg   logo animé
    banniere.svg         le parcours complet, de la marche à la récompense
    boucle.svg           la boucle du jeu, en cinq étapes
    equipe-<pseudo>.svg  une carte par membre
    logo-app.png         le logo de l'application, embarqué dans les animations
    avatars/             les avatars GitHub, embarqués dans les cartes
scripts/
  gen_assets.py          génère tous les SVG ci-dessus
```

## Régénérer les animations

Aucune dépendance : le script n'utilise que la bibliothèque standard.

```bash
python scripts/gen_assets.py profile/assets profile/assets/avatars
```

Tout est dessiné à la main dans le script, sauf la mascotte : c'est le logo de
l'application (`scubatana.frontend/public/img/logo.png` dans scubanion), réduit
dans `profile/assets/logo-app.png` et embarqué tel quel. Les animations sont
en SMIL, le seul format d'animation que GitHub joue dans un README.

## Modifier l'équipe

La liste est en haut de `gen_assets.py`, dans `EQUIPE` : pseudo GitHub, nom,
lot et sous-titre. Pour ajouter quelqu'un, récupérer d'abord son avatar :

```bash
curl -sL "https://github.com/<pseudo>.png?size=200" -o profile/assets/avatars/<pseudo>.jpg
```

## Pourquoi des SVG générés plutôt que des GIF

Un SVG animé pèse quelques kilo-octets, reste net à toutes les tailles, et se
relit comme du texte dans une revue de code. Un GIF de la même scène pèserait
plusieurs méga-octets et serait impossible à corriger sans tout refaire.
