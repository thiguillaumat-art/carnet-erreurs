#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Contraste WCAG entre deux couleurs — parce qu'un contraste ne s'estime pas à
l'œil. Un écran calibré, une pièce bien éclairée et de bons yeux font paraître
acceptable un rapport de 2,8:1 qui est illisible pour beaucoup de gens.

    python3 contrast.py "#5d6061" "#15181A"
    python3 contrast.py "#5d6061" "#15181A" "#33403F" "#FFFFFF"   # toutes les paires

⚠️ TROIS SEUILS, ET ON LES CONFOND SOUVENT :
    4,5:1  texte courant
    3,0:1  grand texte (≥ 24 px, ou ≥ 18,7 px en gras)
    3,0:1  CONTOUR D'UN COMPOSANT INTERACTIF (WCAG 1.4.11) — champ, bouton,
           case à cocher. C'est celui qu'on oublie : un gris de séparateur
           employé comme contour de champ plafonne souvent vers 1,3:1.

⭐ ET LA RÈGLE QUI ÉVITE LA MOITIÉ DES ERREURS : calculer une couleur de texte
contre la surface la PLUS SOMBRE où elle sera posée, pas contre le fond de page.
Un gris à 4,55 sur le fond tombe à 3,96 dès qu'on le pose sur une carte teintée.
"""
import sys
from itertools import combinations


def luminance(hexa: str) -> float:
    """Luminance relative, formule WCAG 2.1."""
    h = hexa.lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    if len(h) != 6:
        raise ValueError(f"Couleur invalide : {hexa}")
    canaux = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in canaux]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contraste(a: str, b: str) -> float:
    la, lb = luminance(a), luminance(b)
    haut, bas = max(la, lb), min(la, lb)
    return (haut + 0.05) / (bas + 0.05)


def verdict(r: float) -> str:
    """Ce que le rapport autorise, du plus exigeant au moins."""
    if r >= 7:    return "✅ texte courant · grand texte · contour interactif  (AAA)"
    if r >= 4.5:  return "✅ texte courant · grand texte · contour interactif"
    if r >= 3:    return "⚠️  grand texte et contour interactif seulement — PAS le texte courant"
    return "⛔ insuffisant pour tout usage"


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 1
    couleurs = argv
    if len(couleurs) == 2:
        paires = [(couleurs[0], couleurs[1])]
    else:
        paires = list(combinations(couleurs, 2))

    largeur = max(len(f"{a} sur {b}") for a, b in paires)
    for a, b in paires:
        r = contraste(a, b)
        print(f"{a} sur {b}".ljust(largeur + 2) + f"{r:6.2f}:1   {verdict(r)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
