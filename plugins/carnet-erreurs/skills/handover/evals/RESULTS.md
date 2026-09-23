# Première évaluation — 23/09/2026

**Un essai réel, pas un banc de test.** Une conversation de trois jours devait
passer à un autre modèle. Le skill a été exécuté par **une session qui ne
l'avait jamais vu** et qui n'avait pas produit le travail.

> ⭐ **La passation a échoué. Le skill a réussi.** Ce ne sont pas les mêmes
> choses, et c'est tout l'intérêt de cette évaluation.

---

## Ce qui s'est passé

| ⬜ | Étape | Résultat |
| --- | --- | --- |
| ⬜ | Lire les fichiers d'orientation | ✅ |
| ⬜ | Trouver la transcription | ⛔ **outils absents** |
| ⬜ | Passe 1 — `extract.py` | ⛔ non atteinte |
| ⬜ | Passe 2 — vérifier | ⛔ non atteinte |
| ⬜ | Écrire `PASSATION.md` | ⭐ **refusé volontairement** |

## ⭐ Le résultat qui compte : elle a refusé de fabriquer

La session avait **tous les fichiers** de l'ancienne. Elle pouvait produire un
`PASSATION.md` plausible en cinq minutes. Personne n'aurait vu la différence.

Elle s'est arrêtée, et a écrit :

> *« Le skill interdit exactement ça : les vérifications de la passe 2 se font
> contre la transcription, et ce qu'a écrit l'ancienne session est "suspect par
> construction". Une passation construite comme ça serait un résumé déguisé. »*

🚨 **C'est la règle du SKILL.md, appliquée par un modèle qui la découvrait.**
Un skill dont on peut mesurer qu'il fait renoncer à produire quelque chose de
faux vaut plus qu'un skill qui produit toujours quelque chose.

## ⭐⭐ Et l'effet secondaire : deux erreurs trouvées dans la source de vérité

N'ayant pas de transcription, la session a lu les fichiers — et y a trouvé
**deux contradictions que l'auteur n'avait pas vues en trois jours** :

| | Ce qu'elle a relevé |
| --- | --- |
| 1 | Une ligne fixait le domaine (« dans la fiscalité du patrimoine ») **dix lignes après** la correction disant que le domaine est à choisir par l'utilisateur. **La même erreur, reformulée.** |
| 2 | Deux règles rendues fausses par une correction du 21/09 étaient **toujours actives** : « ne jamais proposer une action qui suppose de parler », et la visio classée « refusée » |

⛔ **Une session qui aurait lu ce fichier aurait appliqué des règles périmées en
croyant suivre la source de vérité.**

⭐ **C'est la démonstration du principe sous-jacent**, même sans la
transcription : *un lecteur indépendant voit ce que l'auteur ne voit plus.*
Mesuré ailleurs sur le même projet : la machine repère **7** de ses 19 erreurs.
Un lecteur extérieur en a trouvé **2 de plus en quelques minutes**.

---

## 🚨 Le défaut trouvé, et corrigé le jour même

**Le skill supposait un outil de lecture de sessions.** Il n'existait pas dans
la session cible.

⚠️ **Et un piège que je n'avais pas prévu :** un outil au **nom identique**
répondait — il appartenait à un fournisseur de bacs à sable et listait des
machines, pas des conversations.

> ⭐ **Un nom qui correspond n'est pas l'outil qu'on cherche.**

**Corrigé dans le SKILL.md :** une section *« D'abord : où est la
transcription ? »*, un contrôle en trois cases (l'outil existe · **il rend bien
des conversations, vérifié sur une sortie réelle** · il couvre la session
voulue), et trois voies classées — dont l'**export manuel, présenté comme une
voie normale et non comme un pis-aller**.

⛔ Et la quatrième voie, nommée pour être interdite : reconstruire depuis les
fichiers de l'ancienne session.

## ⚠️ Ce que cette évaluation ne prouve PAS

- **Les deux passes n'ont jamais tourné sur une vraie transcription.** Le cœur
  du skill reste non testé.
- `extract.py` n'a été essayé que sur un échantillon fabriqué de 9 lignes.
- **n = 1.** Un essai, un modèle, un environnement.
- Aucun comparatif « avec et sans skill ». ⛔ On ne sait donc pas encore ce que
  le skill **ajoute** — seulement ce qu'il a **empêché**.

---

# Deuxième relevé — même jour, même session indépendante

**Après la correction du skill, la même session a écrit le README et relu la
sortie du script.** Elle a trouvé **cinq défauts de plus**, tous vérifiés en
exécutant.

| | Défaut | Mesuré avant → après |
| --- | --- | --- |
| 1 | **Un seul piège signalé par ligne** — un `break` dans la boucle | ligne cumulant 3 motifs : **1 → 3**. Le signal « qui a décidé ? » était le 3ᵉ, donc invisible |
| 2 | **« sponsorisée » jamais détecté** — le motif ne connaissait que le masculin | ⛔ → ✅ |
| 3 | **Chemins relatifs mal lus** | `scripts/contrast.py` → `/contrast.py` · `ENGAGEMENTS.md` **pas vu du tout** |
| 4 | 🚨 **Presque aveugle en anglais** | 2 lignes anglaises : **1 piège → 5** |
| 5 | **Liens `LICENSE` morts** dans 2 README publiés | pointaient dans leur propre dossier, où le fichier n'existe pas |

## ⭐ Le 4ᵉ est le plus grave, et il touche à la conception

La `description` du skill est **en anglais** — c'est elle qui décide du
déclenchement. Le skill se déclenchera donc surtout sur des conversations
**anglaises**, et sur de l'anglais il ne voyait **qu'un piège sur trois**.

> 🚨 **Un outil qui se déclenche précisément là où il est aveugle.**

Les sept motifs couvrent désormais les deux langues. ⚠️ **Toujours pas testé
sur une vraie transcription anglaise** — seulement sur deux lignes fabriquées.

## ⚠️ Et la correction du 3 en a cassé une autre

En élargissant la regex pour accepter les noms de fichiers nus, `~/dev/x.md` et
`./a/b.py` ont cessé d'être reconnus. Repris avec **8 cas de test**, dont le
piège de l'adresse e-mail (`thi@gmail.com` ne doit rien produire).

⭐ **Entrée de carnet :** une correction est une modification comme une autre —
elle a besoin de ses propres cas de test, pas seulement du cas qui l'a motivée.

## ⭐⭐ Ce que ce deuxième relevé démontre

**Une session indépendante, en une heure, a trouvé : 2 contradictions dans la
source de vérité, 3 bugs dans le script, 2 liens morts, 1 fichier périmé.**
Tout avait été relu par son auteur, plusieurs fois.

> Rappel du chiffre de référence : la machine repère **7** de ses **19** propres
> erreurs. **37 %.**

🚨 **Un fichier périmé mérite une mention à part.** Un carnet markdown annonçait
encore « 4 domaines en 15 min, décision le 25 octobre » pendant que le tableau
de bord disait « 41 domaines, 30-45 min, décision le 8 novembre ».

> ⭐ **Deux sources qui se contredisent sont pires qu'une source incomplète.**
> On ne sait pas laquelle est fausse — donc on n'en croit aucune, ou on croit la
> mauvaise. Le fichier a été retiré, pas corrigé : une seule source par sujet.

## ⬜ Ce qu'il faut pour la prochaine évaluation

⬜ Une vraie transcription exportée dans un fichier
⬜ Les deux passes exécutées jusqu'au bout
⬜ ⭐ **Le comparatif** : la même transcription résumée **sans** le skill, puis
   avec — et compter ce que le résumé a perdu
⬜ Le test final : *la conversation suivante pourrait-elle refaire l'erreur que
   celle-ci a corrigée ?*
