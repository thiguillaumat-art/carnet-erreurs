# -*- coding: utf-8 -*-
"""Génère un rapport d'une page. Dépendance : reportlab."""
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generer(sortie="rapport.pdf", titre="Estimation des droits de succession 2026",
            prenom="Jean-Marie", montant="481 000 €"):
    W, H = A4
    c = canvas.Canvas(sortie, pagesize=A4)
    M = 20 * 2.83465

    c.setFont("Helvetica-Bold", 27)
    c.drawString(M, H - 80, titre)

    c.setFont("Helvetica", 10)
    c.drawString(M, H - 110, f"Établi pour {prenom}")

    # L'encadré du montant
    c.setFillColorRGB(0.89, 0.902, 0.902)
    c.roundRect(M, H - 230, W - 2 * M, 90, 6, stroke=0, fill=1)
    c.setFillColorRGB(0.082, 0.094, 0.102)
    c.setFont("Helvetica-Bold", 26)
    c.drawString(M + 26, H - 195, montant)
    c.setFont("Helvetica", 8)
    c.drawString(M + 26, H - 215, "Fourchette : entre 442 000 € et 519 000 €")

    c.save()
    return sortie

if __name__ == "__main__":
    print(generer())
