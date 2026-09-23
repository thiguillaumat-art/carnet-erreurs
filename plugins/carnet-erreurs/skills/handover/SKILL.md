---
name: handover
description: Carry a long conversation over to a new one — a different model, a fresh context window, another assistant — without losing what matters and without carrying mistakes forward. Two passes by design: one extracts candidates, a second verifies them against the original transcript and corrects. Use when switching model mid-project, when a context window is about to fill, when handing work to someone else, or whenever a conversation must end and its work must not. Produces three lists: carry, carry with a caveat, and do NOT carry.
---

# handover — passer le relais sans perdre ni recopier les erreurs

## 🚨 Le problème que ça règle

Quand une conversation doit s'arrêter — changement de modèle, contexte plein,
passage à quelqu'un d'autre — on demande d'habitude un résumé. **Et un résumé
est produit par celui qui a fait le travail.**

⭐ **C'est exactement le défaut mesuré :** sur 19 erreurs produites dans un
projet réel, la machine en a repéré **7 sur elle-même**. Un humain en a repéré
12. **37 %.**

Un résumé auto-produit garde donc ses propres conclusions, **et jette les
corrections qu'on lui a imposées.** L'erreur repart intacte au tour suivant,
débarrassée de son démenti.

> ⛔ **Une passation n'est pas un résumé. C'est un tri, en deux passes, dont la
> seconde ne fait pas confiance à la première.**

## 🚨 Qui lance ce skill — corrigé le 22/09 par le test

> ⛔ **Ce n'est PAS la conversation qui se termine. C'est celle qui commence.**

Découvert en l'essayant : **une session ne peut pas lire sa propre
transcription** — elle n'apparaît pas dans les sessions inspectables tant
qu'elle tourne.

⭐ **Et c'est la bonne architecture, pas une limite.** Une passation écrite par
celui qui a fait le travail est précisément ce que ce skill existe pour
éviter. La nouvelle conversation lit l'ancienne : **un autre modèle, un travail
qu'il n'a pas produit, aucune conclusion à défendre.**

**Le déroulé réel :**

| | |
| --- | --- |
| 1 | L'ancienne conversation **écrit ses fichiers** et s'arrête. ⭐ Elle ne rédige PAS la passation |
| 2 | On ouvre la nouvelle, **avec le modèle voulu** |
| 3 | La nouvelle liste les sessions, trouve l'ancienne, lit sa transcription |
| 4 | Passe 1 · passe 2 · `PASSATION.md` |

⚠️ **Si l'ancienne conversation a quand même écrit une passation**, elle se lit
comme un candidat parmi d'autres — pas comme une source. Elle est suspecte par
construction.

## 🚨 D'ABORD : où est la transcription ? — corrigé le 23/09 par le test

⛔ **Ce skill suppose un outil de lecture de sessions. Il n'existe pas partout.**
Première leçon du premier essai réel : la session cible n'avait ni
`list_sessions` ni `read_transcript`.

⚠️ **Et pire : elle a trouvé un homonyme.** Un outil nommé `list_sessions`
répondait — il appartenait à un fournisseur de bacs à sable et listait des
machines, pas des conversations. ⭐ **Un nom qui correspond n'est pas l'outil
qu'on cherche.**

### Le contrôle, avant de commencer

| ⬜ | |
| --- | --- |
| ⬜ | L'outil existe-t-il ? |
| ⬜ | ⭐ **Rend-il des CONVERSATIONS ?** Vérifier sur une sortie réelle, pas sur son nom — un titre, une date, un interlocuteur |
| ⬜ | Couvre-t-il la session voulue ? Une session **en cours** n'est jamais lisible |

### Les trois voies, dans cet ordre

| | Voie | Quand |
| --- | --- | --- |
| **1** | Outil de lecture de sessions | ✅ le cas idéal |
| **2** | ⭐ **Export ou copier-coller** de la transcription dans un fichier | quand l'outil manque — **c'est une voie normale, pas un pis-aller** |
| **3** | Relancer depuis un environnement qui a l'outil | si l'export est impossible |

⛔ **Et une quatrième qui n'en est pas une :** reconstruire la passation à
partir des fichiers écrits par l'ancienne session. ⭐ **C'est exactement ce que
ce skill existe pour empêcher** — ces fichiers sont sa production, donc
suspects par construction. Un résumé déguisé en passation.

> 🚨 **Sans transcription, il n'y a pas de passation. Le dire, et s'arrêter.**
> ⭐ Au premier essai, la session cible s'est arrêtée d'elle-même et a demandé
> la transcription. **C'est le comportement attendu.**

## Les deux passes

### Passe 1 — extraire, sans juger

```bash
python3 scripts/extract.py transcription.txt > candidats.md
```

Le script ne décide rien : il repère mécaniquement ce qui mérite examen — les
mots de l'utilisateur, les chiffres, les fichiers écrits, les lignes marquées,
et **les pièges**.

⚠️ **Où trouver la transcription.** Elle n'est pas toujours un fichier sur le
disque. Selon l'outil, elle s'obtient par une commande de lecture de session
(`read_transcript` et équivalents), ou par copier-coller. ⛔ **Écrire la
transcription dans un fichier avant de lancer le script** — ne pas la
paraphraser.

### Passe 2 — vérifier chaque candidat CONTRE la transcription

⭐ **La passe 2 ne relit pas `candidats.md`. Elle relit la transcription.**
C'est tout l'intérêt : vérifier contre la source, pas contre le travail
intermédiaire.

Pour **chaque** candidat, quatre questions, dans cet ordre :

| ⬜ | Question | Si non |
| --- | --- | --- |
| 1 | **Est-ce que ça figure vraiment dans la transcription ?** | ⛔ jeter |
| 2 | **Est-ce un fait, ou une conclusion de l'assistant ?** | ⚠️ marquer comme conclusion, jamais comme fait |
| 3 | **A-t-il été démenti plus tard dans la conversation ?** | ⛔ transmettre **la correction**, pas l'affirmation |
| 4 | **Qui a décidé — l'utilisateur, ou l'assistant ?** | ⛔ une décision prise à la place de l'utilisateur ne se transmet jamais |

## Les trois sorties

Le fichier produit — `PASSATION.md` — a **trois** sections. Pas une.

### ✅ À transmettre

- **Les mots de l'utilisateur, textuels.** ⛔ Jamais reformulés : une
  reformulation est plus jolie et n'a aucun effet.
- **Les décisions qu'il a prises**, avec leur date et leur raison.
- **Les chiffres mesurés, avec leur source.** ⚠️ Un chiffre sans source devient
  une affirmation au tour suivant.
- **Les chemins des fichiers.** ⭐ Ce qui est dans un fichier n'a pas besoin
  d'être transmis : il suffit de dire où regarder. C'est le meilleur taux de
  compression qui existe.
- **Les règles établies** et pourquoi elles l'ont été.

### ⚠️ À transmettre AVEC la réserve

- Les hypothèses non testées — **avec le mot « hypothèse »**.
- Les chiffres d'une source commerciale ou non vérifiée.
- **Ce qui n'a pas pu être vérifié.** ⭐ C'est la première chose qui disparaît
  dans un résumé, et la plus coûteuse à perdre : la conversation suivante
  reprend une limite pour un acquis.

### ⛔ À NE PAS transmettre

- **Les conclusions démenties plus tard** — sauf pour dire qu'elles l'ont été.
- **Les décisions prises à la place de l'utilisateur.** 🚨 Elles se découvrent
  trois semaines plus tard, quand personne ne se souvient qui les a prises.
- Les chiffres écrits sans avoir été comptés.
- Les noms de personnes tierces, sauf si le travail en dépend.
- ⛔ **Toute clé, jeton ou secret.** Jamais, sous aucune forme.
- Les pistes abandonnées **sans leur raison** — sinon elles reviennent.

## ⭐ Le test qui vaut pour toute la passation

> **Est-ce que la conversation suivante pourrait refaire l'erreur que celle-ci
> a corrigée ?**

Si oui, la passation est ratée — même si tout le reste est juste.

## ⛔ Ce que ce skill ne fait pas

- **Il ne résume pas.** Une passation peut être plus longue qu'un résumé, et
  c'est normal : elle porte les réserves en plus des résultats.
- **Il ne juge pas la valeur du travail.** Il trie ce qui se transmet.
- **Il ne remplace pas les fichiers.** ⭐ La meilleure passation est celle qui
  n'a presque rien à dire, parce que tout est déjà écrit quelque part.

## Fichiers

- `scripts/extract.py` — passe 1, mécanique, ne décide rien
- `references/ce-qui-se-perd.md` — ce qui disparaît en premier dans un résumé
