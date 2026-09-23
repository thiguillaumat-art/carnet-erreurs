# Ce qu'un typecheck ne voit jamais

Chaque entrée correspond à un défaut réellement rencontré, qui a passé le
compilateur, le linter et le build sans un avertissement.

À parcourir avant d'annoncer qu'un travail visuel est terminé.

---

## 1 · Ce que la cascade CSS produit réellement

```css
nav a   { color: var(--encre) }   /* spécificité 0,0,1,1 */
.bouton { color: var(--fond) }    /* spécificité 0,0,1,0 — perd */
```

**Un bouton dont le texte a la couleur de son fond.** Les deux règles sont
correctes isolément ; c'est leur rencontre qui échoue, et la lecture du HTML ne
révèle rien.

⭐ Vérifier `getComputedStyle(el).color` sur l'élément final, jamais la règle
source.

⚠️ Même mécanisme avec les classes utilitaires : `.gabarit h2` (0,0,1,1)
l'emporte sur `.text-lg` (0,0,1,0). Un `text-sm` demandé peut rendre en 18 px
sans que rien ne le signale.

## 2 · Ce qu'un attribut de présentation SVG accepte

```jsx
fontFamily="var(--ma-police)"   // ⛔ invalide comme attribut SVG
```

Les attributs de présentation SVG **n'interprètent pas `var()`**. La valeur est
rejetée en silence et le rendu retombe sur la police par défaut — une serif.

⭐ Ne rien forcer : laisser les `<text>` hériter du corps de page.

## 3 · Le cadrage réel d'un SVG

`preserveAspectRatio="… slice"` retient **l'échelle la plus grande**. Dans une
boîte large et basse, cela peut n'afficher qu'une fraction du dessin — sans
erreur, sans avertissement, juste du vide.

⭐ Lire l'étendue réelle des tracés (`getBBox()`) avant de cadrer.

## 4 · Un texte qui déborde de son cadre

Un `<text>` SVG dont la position plus la largeur dépasse le `viewBox` **est
coupé net**.

⭐ Ancrer à droite (`textAnchor="end"`) plutôt que calculer une position de
départ.

## 5 · Deux nombres qui se contredisent à l'écran

Un total arrondi au millier, ses composantes à l'euro près : le total devient
plus petit que l'une de ses parties. **Chaque valeur est juste ; leur voisinage
est faux.**

⭐ Toute somme affichée à côté de ses composantes partage leur précision.

## 6 · Un contour invisible sur un élément cliquable

Le contour d'un composant **interactif** doit atteindre **3:1** (WCAG 1.4.11),
pas 4,5:1 mais pas 1,5 non plus. Un gris décoratif de séparateur employé comme
contour de champ plafonne souvent vers 1,3.

⭐ Deux gris, deux usages, deux seuils. Ne jamais employer le gris des filets
pour cerner ce sur quoi on clique.

## 7 · Une police réglée avant un saut de page

```
color(CORPS); font('normal', 9.5)   // ① on choisit la police
place(hauteur)                       // ② peut déclencher une nouvelle page
doc.text(lignes, x, y)               // ③ écrit… en 7,5 pt
```

La création d'une page dessine l'en-tête courant, **et l'en-tête règle la
police**. Tout appelant qui choisissait sa police avant l'appel écrit ensuite
dans celle de l'en-tête.

⭐ Dans tout dessin impératif — Canvas, jsPDF, PDFKit — l'état est global et
survit aux appels : reposer police et couleur **après** un possible saut de
page, jamais avant.

## 8 · Une hauteur maximale pour animer un contenu de longueur inconnue

`max-height: 384px` avec `overflow: hidden` : passe sur grand écran, **coupe
260 px de texte sur un écran de 375** — sans erreur.

⭐ `grid-template-rows: 0fr → 1fr` s'anime aussi bien et se règle sur le
contenu réel.

## 9 · Une coupure de ligne écrite à la main

Un `<br />` posé pour équilibrer un titre n'est juste **qu'à la largeur pour
laquelle il a été écrit**. Plus bas, la ligne se coupe déjà seule et le `<br />`
en ajoute une de plus, souvent pour un mot.

⭐ La désactiver sous le point de rupture, et remettre l'espace.

## 10 · Une phrase composée autour d'une fonction de formatage

```
`estimée entre ${formatRange(a, b)}`   →  « estimée entre entre 0 € et 200 000 € »
```

Le code est correct ligne à ligne ; **c'est la phrase composée qui est fausse**.

⭐ Lire ce qu'une fonction de formatage inclut avant d'écrire du texte autour.

## 11 · Une affirmation d'interface sur l'état du système

Un écran annonçait *« vos réponses sont encore enregistrées sur cet appareil »*
alors que l'effacement avait lieu dans une autre fonction du même fichier.

⭐ **Toute affirmation d'interface sur l'état du système est une assertion à
vérifier**, au même titre qu'un calcul. Chercher **toutes** les écritures de la
clé, pas la première trouvée.

## 12 · Une donnée juste, au mauvais endroit

Écrire dans un tableau par **numéro de ligne** plutôt que par clé : la valeur
est exacte, la ligne est fausse, et **rien ne se déclenche**.

⭐ Dans un jeu de données, **l'erreur d'alignement est plus dangereuse que
l'erreur de valeur** : une valeur fausse finit par choquer quelqu'un, une valeur
juste mal rangée ne choque personne. Écrire par clé, avec refus si la clé est
introuvable.

## 13 · Une recherche de couleur par hexadécimal

Chercher `#c9a84c` ne trouve ni `rgba(201, 168, 76, .3)`, ni
`linear-gradient(…, #A8893E)`, ni `[201, 168, 76]`.

⭐ Chercher **la teinte**, pas la chaîne : couvrir les trois écritures.

## 14 · Ce que le build dit, et qu'on ne lit pas

| Ligne | Ce qu'elle annonce |
| --- | --- |
| `ƒ /page` là où c'était `○` | la page est passée de statique à rendue à chaque requête |
| `⚠ … is deprecated` | une interface en fin de vie |
| `Generating static pages (109/109)` | le nombre de pages a changé |

⭐ **Comparer la sortie du build à la précédente**, pas seulement vérifier
qu'elle se termine.

---

## 15 · 🚨 On vérifie ce qu'on a reçu, jamais ce qu'on vient de produire

**22/09/2026.** Un corpus de mesures devait être publié sans aucun nom de tiers.
Le contrôle a porté sur les **noms de fichiers** — d'où venaient les prénoms — et
ils ont été retirés. ✅ Contrôle passé, corpus déclaré propre, dépôt publié.

⛔ **Trois jours plus tard, quatre noms d'entreprises étaient toujours en
ligne.** Ils n'étaient pas dans les fichiers reçus : ils étaient dans un champ
`theme` **généré pendant la correction**, à partir de ces mêmes noms de
fichiers.

```json
{"etiquette": "s", "theme": "<nom d'une entreprise réelle>"}
```

🚨 `s` signifiait *« suspecté d'être écrit par une IA »*. **La correction a donc
publié une accusation nominative — dans l'opération censée l'empêcher.**

> ⭐ **La sortie qu'on vient d'écrire n'est jamais dans le périmètre du contrôle
> qu'on vient de faire.** On contrôle l'entrée, on se souvient de l'avoir
> nettoyée, et on oublie que le nettoyage a produit quelque chose de neuf.

**Ce qui l'aurait attrapé :** relancer la recherche **sur le résultat**, pas sur
la source. Trente secondes.

| ⛔ Le réflexe | ✅ Ce qu'il faut |
| --- | --- |
| « j'ai retiré les noms des fichiers » | rechercher les noms **dans ce que j'ai écrit** |
| contrôler avant de transformer | contrôler **après**, sur la sortie |
| se fier au contrôle précédent | ⭐ **un contrôle ne couvre que l'état qu'il a vu** |

⚠️ **Et la vraie leçon est plus large que le nettoyage de données :** aucun
typecheck, aucun test, aucun relecteur ne voit cette classe d'erreur. Le fichier
produit est valide, bien formé, et faux — parce qu'il n'a jamais été comparé à
la **demande** : *« aucun nom de tiers »*.

### 🚨 Et corriger ne suffit pas : l'historique garde tout

**Ajouté le 23/09, signalé par une session indépendante.** Le commit de
publication contient **toujours** les noms, et il est sur le dépôt public. La
correction ne les retire que de la **version actuelle**.

> ⛔ **Sur un dépôt public, `git` n'oublie pas.** Un fichier corrigé n'efface
> rien : chaque version précédente reste consultable, et elle est indexée.

⭐ **Conséquence pratique :** pour une donnée personnelle ou une accusation
nominative, corriger **ne suffit pas** — il faut réécrire l'historique, ou
assumer que la version fautive reste lisible. ⚠️ Et cette décision appartient
au propriétaire du dépôt, pas à celui qui a introduit l'erreur.

**Le vrai enseignement est en amont :** le contrôle de confidentialité doit
passer **avant le premier `push`**, pas après. Après, il n'est plus réversible
sans casser l'historique.

---

## 16 · 🚨 Une correction a besoin de ses propres cas de test

**23/09/2026.** Une expression régulière ratait les noms de fichiers nus :
`ENGAGEMENTS.md` n'était pas repéré. Corrigée, testée sur ce cas précis. ✅

⛔ **Et deux autres cas, qui marchaient avant, ont cessé de marcher :**
`~/dev/x.md` et `./a/b.py` ne sortaient plus rien.

Le test de la correction portait sur **le cas qui l'avait motivée**, pas sur
ceux qui fonctionnaient déjà. Personne ne les avait rangés dans un test — ils
marchaient, donc ils étaient invisibles.

> ⭐ **Une correction est une modification comme une autre.** Elle mérite les
> mêmes cas de test que le code d'origine — plus le sien.

**Ce qui l'a rattrapé :** une table de 8 cas, écrite avant la 2ᵉ tentative, et
relancée après. Trente secondes.

| ⛔ Le réflexe | ✅ Ce qu'il faut |
| --- | --- |
| tester le cas qu'on vient de corriger | tester **tous** les cas connus, y compris les anciens |
| « ça marchait avant » | ⭐ **ce qui marchait avant n'est protégé que s'il est écrit quelque part** |

⚠️ Et le motif est plus large : **les régressions se cachent dans ce qui
n'était pas cassé.** Aucun typecheck ne les voit — le code est valide, la
regex compile, et elle ne trouve plus ce qu'elle trouvait hier.

---

## La question à se poser en dernier

> **Qu'est-ce que je n'ai pas regardé ?**

Pas « est-ce que ça marche ». La bonne question désigne l'angle mort, pas la
confiance.

⭐ Et sa jumelle, ajoutée le 22/09 :

> **Est-ce que je viens de produire quelque chose que mon contrôle n'a pas vu ?**
