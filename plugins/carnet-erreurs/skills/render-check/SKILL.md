---
name: render-check
description: >-
  Forbids announcing that visual work is finished without having rendered it and
  looked at it. Provides a render bench to view a PDF, an email, a component or
  a mobile page even without a browser, a list of what a typecheck never
  detects, and a WCAG contrast calculator covering all three thresholds
  including the forgotten one (1.4.11, interactive component outlines). Use
  systematically whenever creating or modifying anything that will be LOOKED AT
  — web page, email, PDF, UI component, share image, stylesheet, layout, mobile
  rendering — and before any phrase like "it's ready", "it's done", "that should
  work". Trigger even when the user does not explicitly ask for verification:
  that is exactly when it gets skipped.
---

# render-check

## Pourquoi cette compétence existe

Un typecheck prouve que le code s'exécute. **Il ne prouve rien sur ce que la
personne voit.**

Cette distinction a produit, sur un seul projet en trois jours : une section
entière absente d'une page, un bouton invisible parce que son texte avait la
couleur de son fond, un motif décoratif jamais affiché, du texte SVG rendu en
serif, un titre tronqué dans son cadre, une puce sur quatre imprimée deux fois
trop petite, et 260 px de texte coupés en silence sur téléphone.

**Aucun de ces défauts n'a été trouvé en relisant du code.** Tous ont été vus.
Plusieurs ont été signalés par l'utilisateur après qu'on lui eut annoncé que
c'était prêt — ce qui est la manière la plus coûteuse de les découvrir.

## La règle

> **Une modification visuelle n'est pas terminée tant qu'elle n'a pas été vue
> rendue.**

Et son corollaire, qui compte autant : **quand le rendu est impossible à
obtenir, le dire.** Ne pas remplacer l'observation par un raisonnement en
espérant que ça tienne. « Je n'ai pas pu voir le résultat » est une information
utile ; « ça devrait marcher » n'en est pas une.

## Le déroulé

1. **Produire** le travail.
2. **Rendre** — voir `references/render-bench.md` pour le moyen adapté au type
   de sortie. Il existe presque toujours un moyen, même sans navigateur.
3. **Regarder** l'image, pas le code.
4. **Parcourir** `references/what-a-typecheck-misses.md`. La liste est
   courte et chaque entrée correspond à un défaut réellement rencontré.
5. **Mesurer** ce qui se mesure — les contrastes avec `scripts/contrast.py`,
   jamais à l'œil.
6. **Vérifier au point de rupture le plus étroit.** Un défaut qui n'apparaît
   qu'à 375 px de large est invisible sur l'écran où l'on travaille.
7. **Alors seulement**, dire que c'est prêt — et dire ce qui n'a pas pu être
   vérifié.

## Ce qui trompe le plus souvent

**Le rendu était bon la dernière fois.** Les défauts visuels n'apparaissent pas
au moment où l'on écrit la ligne fautive ; ils apparaissent quand une autre
règle vient la recouvrir. Reregarder après chaque série de modifications, pas
une fois à la fin.

**Un seul écran a été vérifié.** La largeur est une variable, au même titre que
les données. Un texte qui tient en 306 px sur grand écran en occupe 640 sur un
téléphone — et une hauteur maximale écrite en dur le coupe sans rien signaler.

**Le code est juste, la composition est fausse.** Deux nombres corrects placés
côte à côte peuvent se contredire : un total arrondi au millier au-dessus de sa
propre composante à l'euro près affiche « 78 000 € » au-dessus de « 78 389 € ».
Chaque valeur est exacte ; leur voisinage est faux. Cela ne se voit qu'en
regardant.

**La sortie du build dit quelque chose et personne ne le lit.** Une page passée
de statique à dynamique, une API dépréciée, un nombre de pages qui change :
c'est écrit, ce n'est pas invisible — c'est ignoré. Comparer la sortie à la
précédente, pas seulement vérifier qu'elle se termine.

## Une dernière chose, sur l'honnêteté du compte rendu

Quand le rendu a été vérifié, le dire précisément : *« j'ai regardé les cinq
pages du PDF »*, *« j'ai rendu l'e-mail à 375 px »*. Quand il ne l'a pas été,
le dire aussi précisément.

⚠️ Et quand un rendu est une **approximation** — une transcription HTML d'un
composant React, par exemple —, l'annoncer comme telle. Une approximation
présentée comme le vrai rendu est pire que pas de rendu du tout, parce qu'elle
donne une confiance qui n'est pas méritée.

## Fichiers

- `references/render-bench.md` — comment voir chaque type de sortie
- `references/what-a-typecheck-misses.md` — la liste, à parcourir
- `scripts/contrast.py` — calcul du contraste WCAG entre deux couleurs
