#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compteur de marqueurs — « ce texte sonne-t-il IA ? »

    python3 markers.py mon-texte.txt
    python3 markers.py corpus/*.txt          # comparaison
    cat texte | python3 markers.py -

🚨 CE QUE CET OUTIL NE FAIT PAS, ET NE FERA JAMAIS : dire qui a écrit un texte.

Aucun détecteur ne le peut. Les détecteurs commerciaux annoncent « 94 % généré
par IA » sur des textes humains — un faux positif accuse quelqu'un à tort, et
il n'existe aucun moyen de se disculper. Ce programme ne rend donc AUCUN
verdict. Il compte des marqueurs mesurables et montre où ils sont.

⭐ SON VRAI USAGE : se relire soi-même. Il désigne les phrases à réécrire.
   « Ton paragraphe 4 est une antithèse, comme les paragraphes 2 et 7 » est
   une information utile. « 87 % IA » n'en est pas une.

⚠️ ET LE RÉSULTAT LE PLUS UTILE DU RELEVÉ DU 15/09/2026 : sur LinkedIn, les
   marqueurs dits « IA » sont MASSIVEMENT présents dans des textes écrits par
   des humains. Les modèles ont appris sur ce corpus. Un score élevé ne veut
   donc pas dire « écrit par une machine » — il veut dire « écrit dans le
   registre que la machine imite ». C'est une information sur le STYLE.
"""
import sys, re, glob, statistics as st

# ── Lexique que les modèles sur-produisent en français ───────────────────────
LEXIQUE = [
    "plonge", "paysage", "crucial", "il est important de", "il convient de",
    "en résumé", "en conclusion", "révolutionn", "à l'ère de", "véritable",
    "incontournable", "au cœur de", "riche en", "sans précédent",
    "force est de constater", "il n'en reste pas moins", "en effet,",
    "par ailleurs,", "notamment", "permet de", "offre une", "un atout",
    "la clé", "le secret", "game changer", "état d'esprit", "voilà pourquoi",
]

# ── Registre familier / fautes : présence = indice HUMAIN ───────────────────
FAMILIER = [
    r"\bcon\b", r"\bconne\b", r"à l'arrache", r"\btruc\b", r"\bouais\b",
    r"\bmec\b", r"\bputain\b", r"\bchiant", r"\bbordel\b", r"\bnul\b",
    r"\bgalère", r"\bcarrément\b", r"\bgrave\b", r"\bdu coup\b", r"\bbref\b",
    r"\bn'importe quoi\b", r"la pire idée", r"\bflemme\b", r"\bçui\b",
]

ANTITHESE = re.compile(
    r"\bn['’e]\s?\w*(?:\s+\w+){0,5}\s+pas\b.{0,90}?[,.]\s*(?:c['’]est|mais)\b"
    r"|\bnon pas\b.{0,60}?\bmais\b", re.I | re.S)

# Détail vérifiable : un nombre non rond, une date, un nom propre au milieu
# d'une phrase. ⭐ C'est ce qu'une machine ne peut pas inventer sans risque.
NOMBRE = re.compile(r"\b\d[\d  ]*(?:[,.]\d+)?\s*(?:%|€|px|:1|x\b)?")
PROPRE = re.compile(r"(?<![.!?]\s)(?<!^)\b[A-ZÉÈÀÇ][A-Za-zÉÈÀÂÎÔÛéèàâêîôûç'’-]{2,}\b", re.M)

EMOJI = re.compile("[\U0001F000-\U0001FAFF←-⇿☀-➿⬀-⯿]")


def phrases(t):
    t = re.sub(r"\s+", " ", t)
    p = [s.strip() for s in re.split(r"(?<=[.!?…])\s+", t) if s.strip()]
    return [s for s in p if len(s.split()) > 0]


def analyser(texte):
    mots = texte.split()
    n_mots = len(mots) or 1
    ph = phrases(texte)
    longueurs = [len(s.split()) for s in ph] or [0]
    paras = [p.strip() for p in texte.split("\n") if p.strip()]

    moy = st.mean(longueurs)
    ecart = st.pstdev(longueurs)
    r = {
        "mots": n_mots,
        "phrases": len(ph),
        "moy_mots_phrase": round(moy, 1),
        # ⭐ le marqueur central : l'écriture humaine est IRRÉGULIÈRE
        "irregularite": round(ecart / moy, 2) if moy else 0.0,
        "paras_1_phrase_pct": round(
            100 * sum(1 for p in paras if len(phrases(p)) <= 1) / (len(paras) or 1)),
        "paras_courts_pct": round(
            100 * sum(1 for p in paras if len(p.split()) <= 6) / (len(paras) or 1)),
        "antitheses": len(ANTITHESE.findall(texte)),
        "tirets_cadratins": texte.count("—"),
        "emoji": len(EMOJI.findall(texte)),
        # ⭐ densité de détail vérifiable, pour 100 mots
        "details_100m": round(
            100 * (len(NOMBRE.findall(texte)) + len(PROPRE.findall(texte))) / n_mots, 1),
    }
    # ⭐ la chute aphoristique : dernier paragraphe court, en forme de sentence.
    # C'est LE geste que les modèles produisent le plus, et c'est aussi celui
    # que LinkedIn récompense le plus — d'où la confusion.
    dernier = paras[-1] if paras else ""
    r["chute_aphorisme"] = bool(
        len(dernier.split()) <= 16
        and re.search(r"\bc['’]est\b|\bvoilà\b|\breste\b|:", dernier, re.I))

    # tricolon : 3 lignes consécutives de longueur proche
    tri, série = 0, []
    for p in paras:
        n = len(p.split())
        if série and abs(n - série[-1]) <= 3:
            série.append(n)
        else:
            if len(série) >= 3:
                tri += 1
            série = [n]
    if len(série) >= 3:
        tri += 1
    r["tricolons"] = tri

    r["lexique"] = sorted({m for m in LEXIQUE if m in texte.lower()})
    r["familier"] = sorted({re.search(f, texte, re.I).group(0)
                            for f in FAMILIER if re.search(f, texte, re.I)})

    # anaphores : 2+ lignes consécutives, même premier mot
    ana, prec, suite = [], None, 1
    for p in paras:
        m = p.split()[0].lower().strip(".,:;") if p.split() else ""
        if m and m == prec:
            suite += 1
        else:
            if suite >= 2 and prec:
                ana.append((prec, suite))
            prec, suite = m, 1
    if suite >= 2 and prec:
        ana.append((prec, suite))
    r["anaphores"] = ana
    return r


def afficher(nom, r):
    print(f"\n━━ {nom}  ({r['mots']} mots, {r['phrases']} phrases)")
    irr = r["irregularite"]
    drap = "⚠️  très régulier" if irr < 0.45 else ("· régulier" if irr < 0.60 else "✅ irrégulier")
    print(f"   irrégularité des phrases   {irr:>5.2f}   {drap}")
    print(f"   longueur moyenne           {r['moy_mots_phrase']:>5.1f} mots")
    print(f"   paragraphes d'une phrase   {r['paras_1_phrase_pct']:>4} %")
    print(f"   paragraphes ≤ 6 mots       {r['paras_courts_pct']:>4} %")
    print(f"   antithèses « pas X, c'est Y »  {r['antitheses']}")
    d = r["details_100m"]
    print(f"   détails vérifiables /100 mots  {d:>5.1f}   "
          + ("⚠️  peu ancré" if d < 8 else "✅ ancré"))
    print(f"   tirets cadratins —         {r['tirets_cadratins']}   emoji {r['emoji']}")
    print(f"   tricolons (3 lignes jumelles)  {r['tricolons']}"
          f"   ·  chute aphoristique : {'⚠️  oui' if r['chute_aphorisme'] else 'non'}")
    if r["anaphores"]:
        print("   anaphores                  " +
              ", ".join(f"« {m} » ×{n}" for m, n in r["anaphores"]))
    if r["lexique"]:
        print("   lexique sur-produit        " + ", ".join(r["lexique"]))
    if r["familier"]:
        print("   ✅ registre familier        " + ", ".join(r["familier"]) +
              "   ← indice humain fort")


def main(argv):
    if not argv:
        print(__doc__)
        return 1
    fichiers = []
    for a in argv:
        fichiers += glob.glob(a) if a != "-" else ["-"]
    for f in fichiers:
        texte = sys.stdin.read() if f == "-" else open(f, encoding="utf-8").read()
        afficher(f.split("/")[-1], analyser(texte))
    print("\n🚨 Aucun de ces chiffres ne dit qui a écrit le texte. "
          "Ils disent dans quel registre il est écrit.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
