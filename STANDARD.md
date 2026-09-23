# Le standard du dépôt

**Fixé le 19/09/2026**, le jour de la première publication. ⛔ Ce n'est pas une
déclaration d'intention : chaque ligne ci-dessous est une condition qui peut
échouer, et dont l'échec bloque.

> *« Que du contenu avec de la qualité et pas fait à l'arrache. Tout doit être
> testé et retesté et amélioré aussi. Ce n'est pas un projet rapide. »*
> — Thibault, 19/09/2026

---

## 🚨 Pourquoi ce fichier existe : ce qui est arrivé le jour même

Le dépôt est parti en ligne avec `evals/evals.json` annonçant trois évaluations
sur trois fichiers — `palette.css`, `accordeon.html`, `rapport.py`. **Aucun des
trois n'était dans le dépôt.** La suite était inexécutable par quiconque.

⭐ **C'est le pire endroit possible pour ce défaut.** Le dossier `evals/` est
précisément celui qui affirme « ceci a été testé ». Un dossier de tests qui ne
tourne pas ment deux fois : sur le test, et sur le sérieux de tout le reste.

⚠️ **Et je ne l'ai pas vu au moment de publier.** J'ai vérifié que les fichiers
étaient en ligne, pas qu'ils étaient *cohérents entre eux*. Même famille
d'erreur que le typecheck : la forme passait, le fond était faux.

---

## Les quatre conditions avant qu'une ligne parte en ligne

### 1 · ⬜ Un chiffre est compté, jamais estimé

Tout nombre publié — durée, ampleur, taux, nombre de mots — a une source
re-mesurable. Les nombres qui ont été écrits avant d'être comptés restent dans
le dépôt **marqués comme les erreurs qu'ils étaient**.

Motif constaté 3 fois : « des semaines », « six jours », « 192 mots ».

### 2 · ⬜ Un test qui ne peut pas échouer n'est pas un test

Une évaluation exige :

- le **prompt** exact ;
- la **fixture**, présente dans le dépôt ;
- l'**attendu**, écrit avant la exécution ;
- le résultat **avec et sans** le skill.

⛔ Sans le comparatif « sans skill », on mesure le modèle, pas le skill.

### 3 · ⬜ Une hypothèse qui échoue reste publiée

`ai-text-markers` publie le tableau qui démonte sa propre prémisse.
`render-check` publie l'évaluation où il n'apporte rien.

⭐ **C'est ce qui distingue un dépôt d'une plaquette.** Tout le monde publie ce
qui marche.

### 4 · ⬜ Aucun outil ne rend un verdict qu'il ne peut pas soutenir

Un faux positif accuse quelqu'un qui n'a aucun moyen de se défendre. Un outil
qui ne peut pas prouver compte et montre — il ne tranche pas.

---

## ⚠️ Le piège de ce standard, nommé avant de tomber dedans

**« Ce n'est pas un projet rapide » peut devenir une raison de ne jamais
publier.** La lenteur n'est pas une preuve de qualité : un dépôt jamais publié
a une qualité de zéro, parce que personne ne l'a mis à l'épreuve.

⭐ **La parade : la barre est un test qui peut échouer, pas un sentiment de
minutie.** Les quatre cases ci-dessus se cochent ou ne se cochent pas. Quand
elles sont cochées, ça part — même si on « pourrait encore améliorer ».

⛔ **Et l'amélioration se fait en public.** Une v0.1.0 publiée qu'on corrige
vaut mieux qu'une v1.0 parfaite qui n'existe pas.

---

## État des lieux — 19/09/2026

| | `render-check` | `ai-text-markers` | `handover` |
| --- | --- | --- | --- |
| Chiffres comptés | ✅ | ✅ | ✅ |
| Évaluations | ✅ 3, fixtures incluses | ⛔ **aucune** | ⚠️ 1 essai réel, [résultat publié](plugins/carnet-erreurs/skills/handover/evals/RESULTS.md) — **les 2 passes non testées** |
| Comparatif sans skill | ✅ 15/15 contre 12/15 | ⛔ — | ⛔ — |
| Hypothèse échouée publiée | ✅ l'éval sans gain | ✅ le tableau n=7 | ✅ l'auto-vérification à 37 % |
| Refus de verdict | — | ✅ | ✅ trois listes, pas un résumé |

🚨 **`ai-text-markers` n'a aucune évaluation.** Il est publié sans preuve qu'il
se déclenche au bon moment ni qu'il apporte quelque chose. C'est la dette la
plus visible du dépôt, et la prochaine chose à faire dessus.
