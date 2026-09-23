#!/usr/bin/env python3
"""
handover/extract.py — passe 1 : sortir les CANDIDATS d'une transcription.

    python3 extract.py transcription.txt > candidats.md
    cat transcription.txt | python3 extract.py -

⛔ Ce script ne décide RIEN. Il ne juge pas la valeur, ne résume pas, ne
reformule pas. Il repère mécaniquement ce qui MÉRITE D'ÊTRE EXAMINÉ, et la
passe 2 tranche.

⭐ Pourquoi cette séparation : un résumé écrit par le modèle qui a produit le
travail garde ses propres conclusions et jette les corrections qu'on lui a
imposées. Mesuré : sur 19 erreurs produites, la machine en a repéré 7 sur
elle-même. 37 %.
"""

import re
import sys

# ── Ce qui a de la valeur et qu'on ne peut PAS reconstituer ─────────────────

# Les mots de l'utilisateur. La matière la plus précieuse, et la seule
# qu'aucun résumé ne peut remplacer sans la trahir.
TOUR_USER = re.compile(r"^\s*(?:user|utilisateur|humain|human)\s*[:>]", re.I)

# Un nombre accompagné d'une unité ou d'un signe : probablement une mesure.
CHIFFRE = re.compile(r"\b\d[\d  .,]*\s*(?:%|:1|€|\$|px|mots?|jours?|mois|ans?|"
                     r"sessions?|clients?|heures?|min|Mo|Ko|/\d+)")

# ⚠️ Corrigé le 23/09 : l'ancienne version exigeait ~ . ou / en tête, donc
# « scripts/contrast.py » devenait « /contrast.py » et « ENGAGEMENTS.md »
# n'était pas vu du tout. Un nom de fichier nu compte aussi.
CHEMIN = re.compile(
    r"(?<![\w@/.~-])"                       # pas au milieu d'un mot ni d'une adresse
    r"(?:~/|\.{1,2}/|/)?"                    # préfixe optionnel : ~/ ./ ../ /
    r"[\w-]+(?:/[\w-]+)*"                   # segments
    r"\.(?:md|py|tsx?|jsx?|json|html|css|sql|jsonl|yml|yaml|txt|toml|sh)\b")
LIEN = re.compile(r"https?://[^\s)>\]]+")

# Les marques du carnet : décisions, interdits, pièges.
MARQUE = re.compile(r"[⛔⭐🚨⚠️✅]")

# ── 🚨 Ce qui NE DOIT PAS passer — le cœur du skill ─────────────────────────
# Une passation qui ne transmet que le bon reconduit les erreurs en silence.

# ⚠️ Corrigé le 23/09 : chaque motif couvre le FRANÇAIS ET L'ANGLAIS. Un test
# sur deux lignes anglaises ne relevait qu'un piège sur trois — alors que la
# `description` du skill est en anglais, donc il se déclenche surtout là.
# ⭐ Et les accords féminins : « sponsorisée » n'était pas vu.
PIEGE = [
    (r"(?i)\b(?:j['’]avais (?:écrit|dit|conclu|affirmé|proposé)"
     r"|i (?:had )?(?:wrote|had written|said|concluded|claimed|assumed))\b",
     "correction d'une erreur passée — ⛔ vérifier que c'est la version CORRIGÉE qui part"),
    (r"(?i)\b(?:c['’]est faux|était fauss?e?s?|se trompait|erreur de ma part|j['’]ai eu tort"
     r"|that(?:'s| is) (?:wrong|false|incorrect)|i was wrong|my mistake|turned out false)\b",
     "une affirmation démentie — ⛔ elle ne doit PAS repartir comme un fait"),
    (r"(?i)\b(?:je (?:choisis|retiens|tranche)|domaine retenu|verrouillé[es]?"
     r"|we(?:'ll| will)? (?:go with|pick|choose)|decision:|locked in|chosen)\b",
     "⛔ une décision — vérifier QUI l'a prise. Une décision prise à la place de "
     "l'utilisateur ne se transmet jamais"),
    (r"(?i)\b(?:probablement|sans doute|il semble|on peut supposer|j['’]imagine|sûrement"
     r"|probably|presumably|it seems|i assume|likely|my guess)\b",
     "⚠️ une supposition — ne jamais la transmettre comme un fait"),
    (r"(?i)\b(?:sponsoris[ée]e?s?|sponsored|publi-rédactionnel|placement payant"
     r"|paid placement|advertorial)\b",
     "⚠️ source commerciale — la conclusion vaut moins que le chiffre"),
    (r"(?i)\b(?:non vérifiée?s?|pas pu vérifier|à confirmer|reste à vérifier"
     r"|je n['’]ai pas (?:vu|pu)|unverified|could ?n[o']t (?:verify|check)"
     r"|not verified|to be confirmed|i did ?n[o']t (?:see|look))\b",
     "⚠️ limite déclarée — ⭐ elle DOIT être transmise, c'est ce qui se perd en premier"),
    (r"(?i)\b(?:clés?|jetons?|token|mot de passe|secrets?|api[_ -]?key|password"
     r"|credentials?|bearer)\b",
     "🚨 un secret possible — ⛔ ne JAMAIS transmettre"),
]

# Des noms propres de tiers : à ne transmettre qu'avec une raison.
TIERS = re.compile(r"\b(?:M\.|Mme|Monsieur|Madame)\s+[A-ZÉÈÀ][\w-]+")


def decouper(texte):
    """Une ligne = une unité. On garde le numéro pour pouvoir re-vérifier."""
    return [(i, l.rstrip()) for i, l in enumerate(texte.split("\n"), 1) if l.strip()]


def analyser(texte):
    lignes = decouper(texte)
    res = {"mots_utilisateur": [], "chiffres": [], "fichiers": set(), "liens": set(),
           "marques": [], "pieges": [], "tiers": []}

    dans_user = False
    for n, l in lignes:
        if TOUR_USER.search(l):
            dans_user = True
            res["mots_utilisateur"].append((n, TOUR_USER.sub("", l).strip()))
            continue
        if re.match(r"^\s*(?:assistant|claude)\s*[:>]", l, re.I):
            dans_user = False
        elif dans_user and l.strip():
            res["mots_utilisateur"].append((n, l.strip()))

        if CHIFFRE.search(l):
            res["chiffres"].append((n, l.strip()[:200]))
        res["fichiers"].update(CHEMIN.findall(l))
        res["liens"].update(LIEN.findall(l))
        if MARQUE.search(l):
            res["marques"].append((n, l.strip()[:200]))
        # ⚠️ Corrigé le 23/09 : il y avait un `break` ici. Sur une ligne qui
        # cumulait 3 motifs — dont « qui a décidé ? » — un seul sortait, et
        # c'était le premier de la liste, pas le plus important.
        touches = [p for motif, p in PIEGE if re.search(motif, l)]
        if touches:
            res["pieges"].append((n, " · ".join(touches), l.strip()[:200]))
        res["tiers"] += [(n, t) for t in TIERS.findall(l)]
    return res


def rendre(r, nom):
    o = [f"# Candidats de passation — {nom}", "",
         "⛔ **Ceci n'est PAS une passation.** C'est la liste de ce qui doit être "
         "examiné. La passe 2 vérifie chaque ligne contre la transcription et tranche.", ""]

    def bloc(titre, items, note=""):
        # ⚠️ `o` est modifiée sur place : jamais réassignée, sinon Python la
        # traite comme une variable locale et lève UnboundLocalError.
        o.append(f"## {titre} — {len(items)}")
        if note:
            o.extend(["", note])
        o.append("")
        for it in items[:80]:
            if len(it) == 3:
                o.append(f"- `L{it[0]}` **{it[1]}**  \n  > {it[2]}")
            else:
                o.append(f"- `L{it[0]}` {it[1]}")
        if len(items) > 80:
            o.append(f"- … et {len(items) - 80} de plus")
        o.append("")

    bloc("🚨 À NE PAS transmettre tel quel", r["pieges"],
         "⭐ **La section la plus importante.** Une passation qui ne transmet que le "
         "bon reconduit les erreurs en silence — elles repartent sans leur correction.")
    bloc("⭐ Les mots de l'utilisateur", r["mots_utilisateur"],
         "⛔ **Ne jamais reformuler.** C'est la seule matière qu'un résumé ne peut pas "
         "remplacer sans la trahir.")
    bloc("Chiffres et mesures", r["chiffres"],
         "⚠️ Chacun doit repartir **avec sa source**. Un chiffre sans source devient "
         "une affirmation au tour suivant.")
    bloc("Lignes marquées", r["marques"])

    o.extend(["## Fichiers écrits — " + str(len(r["fichiers"])), "",
              "⭐ Ce qui est dans un fichier n'a pas besoin d'être transmis : il "
              "suffit de dire où regarder.", ""])
    o.extend([f"- `{f}`" for f in sorted(r["fichiers"])] + [""])
    o.extend(["## Liens — " + str(len(r["liens"])), ""])
    o.extend([f"- {u}" for u in sorted(r["liens"])] + [""])

    if r["tiers"]:
        o.extend(["## ⚠️ Noms de personnes repérés — " + str(len(r["tiers"])), "",
                  "⛔ Ne transmettre que si le travail en dépend.", ""])
        o.extend([f"- `L{n}` {t}" for n, t in r["tiers"][:30]] + [""])
    return "\n".join(o)


def main(argv):
    if not argv:
        print(__doc__)
        return 1
    nom = argv[0]
    texte = sys.stdin.read() if nom == "-" else open(nom, encoding="utf-8").read()
    print(rendre(analyser(texte), nom))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
